"""Fetch EUR-Lex rule sources and stage verbatim article text in gpsr-rules.v0.json.

This script never marks a rule as human-verified. A reviewer must check that the
selected article supports the rule and then record that review separately.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES = REPO_ROOT / "data" / "gpsr-rules.v0.json"
ALLOWED_HOST = "eur-lex.europa.eu"
MAX_DOCUMENT_BYTES = 20 * 1024 * 1024
BLOCK_TAGS = {"article", "br", "div", "li", "p", "section", "tr"}
ARTICLE_HEADING = re.compile(r"^Article\s+(\d+)\s*$", re.IGNORECASE)
ARTICLE_REF = re.compile(r"\bArt(?:icle)?\.?\s*(\d+)\b", re.IGNORECASE)


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def html_to_text(document: str) -> str:
    parser = _TextExtractor()
    parser.feed(document)
    parser.close()
    lines = [re.sub(r"\s+", " ", line).strip() for line in "".join(parser.parts).splitlines()]
    return "\n".join(line for line in lines if line)


def extract_articles(document: str) -> dict[int, str]:
    """Return article heading through next article heading, preserving source wording."""
    text = html_to_text(document)
    lines = text.splitlines()
    starts: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        match = ARTICLE_HEADING.fullmatch(line.strip())
        if match:
            starts.append((index, int(match.group(1))))

    articles: dict[int, str] = {}
    for item_index, (start, number) in enumerate(starts):
        end = starts[item_index + 1][0] if item_index + 1 < len(starts) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        if number in articles:
            raise ValueError(f"Duplicate Article {number} heading in fetched document")
        articles[number] = body
    return articles


def fetch_document(url: str, timeout: float = 30.0) -> tuple[bytes, str]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
        raise ValueError(f"Refusing non-EUR-Lex source URL: {url}")
    request = Request(
        url,
        headers={"User-Agent": "RedFlag-EUR-Lex-source-fetch/1.0", "Accept": "text/html,application/xhtml+xml"},
    )
    with urlopen(request, timeout=timeout) as response:
        final_url = urlparse(response.geturl())
        if final_url.scheme != "https" or final_url.hostname != ALLOWED_HOST:
            raise ValueError(f"EUR-Lex redirected to an untrusted host: {response.geturl()}")
        if response.status != 200:
            raise OSError(f"EUR-Lex returned HTTP {response.status} for {url}")
        raw = response.read(MAX_DOCUMENT_BYTES + 1)
    if len(raw) > MAX_DOCUMENT_BYTES:
        raise ValueError(f"EUR-Lex response exceeded {MAX_DOCUMENT_BYTES} bytes")
    return raw, hashlib.sha256(raw).hexdigest()


def update_rule_sources(
    document: dict[str, Any], fetched: dict[str, tuple[bytes, str, str]]
) -> tuple[int, list[str]]:
    """Fill TODO quotes from the referenced official article; leave verification human-owned."""
    updated = 0
    unresolved: list[str] = []
    for rule in document.get("rules", []):
        quote = rule.get("source_quote")
        if not isinstance(quote, str) or not quote.lstrip().startswith("TODO_VERIFY"):
            continue

        rule_id = str(rule.get("rule_id", "<unknown>"))
        url = rule.get("source_url")
        reference = (rule.get("legal_basis") or {}).get("article_ref", "")
        matches = ARTICLE_REF.findall(reference)
        if not url or not matches:
            unresolved.append(f"{rule_id}: missing source_url or article_ref")
            continue
        source = fetched.get(url)
        if source is None:
            unresolved.append(f"{rule_id}: no fetched source for {url}")
            continue

        raw, digest, retrieved_at = source
        try:
            encoding = "utf-8-sig"
            html = raw.decode(encoding)
            articles = extract_articles(html)
        except (UnicodeDecodeError, ValueError) as error:
            unresolved.append(f"{rule_id}: cannot parse source: {error}")
            continue

        # The first article reference belongs to the primary instrument named by
        # this rule's source_url. Related-instrument citations need their own rule.
        article_number = int(matches[0])
        article_quote = articles.get(article_number)
        if not article_quote:
            unresolved.append(f"{rule_id}: Article {article_number} not found at {url}")
            continue

        rule["source_quote"] = article_quote
        rule["source_url"] = url
        rule["source_retrieved_at"] = retrieved_at
        rule["source_sha256"] = digest
        # Deliberately do not set human_verified, human_verified_by, or
        # human_verified_at. Fetching a source is not a human legal review.
        updated += 1
    return updated, unresolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--dry-run", action="store_true", help="Fetch and report, but do not write the rules file")
    args = parser.parse_args(argv)

    try:
        document = json.loads(args.rules.read_text(encoding="utf-8"))
        urls = sorted(
            {
                rule["source_url"]
                for rule in document.get("rules", [])
                if isinstance(rule.get("source_quote"), str)
                and rule["source_quote"].lstrip().startswith("TODO_VERIFY")
                and rule.get("source_url")
            }
        )
        fetched: dict[str, tuple[bytes, str, str]] = {}
        for url in urls:
            raw, digest = fetch_document(url, timeout=args.timeout)
            retrieved_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            fetched[url] = (raw, digest, retrieved_at)
            print(f"Fetched {url}: sha256={digest} bytes={len(raw)} at={retrieved_at}")

        updated, unresolved = update_rule_sources(document, fetched)
        for item in unresolved:
            print(f"UNRESOLVED: {item}", file=sys.stderr)
        if unresolved:
            return 1
        print(f"Prepared {updated} verbatim article quotes. Human verification flags were not changed.")
        if not args.dry_run:
            args.rules.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Updated {args.rules}")
        return 0
    except (OSError, URLError, ValueError, json.JSONDecodeError) as error:
        print(f"EUR-Lex fetch failed; rule data was not written: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
