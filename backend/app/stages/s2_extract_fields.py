"""S2 listing-field extraction with exact source-span enforcement.

The deterministic extractor always runs first. Nemotron Nano is an optional,
configured enrichment pass; no model ID is guessed and no model-provided quote
is trusted until it is found verbatim in the source text.
"""

from __future__ import annotations

import json
import math
import os
import re
from collections.abc import Callable
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = ROOT / "schemas" / "core-schemas.json"
MODEL_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"
MAX_INPUT_CHARS = 100_000
FIELD_KEYS = (
    "product_identifier",
    "manufacturer_identity",
    "manufacturer_contact_postal",
    "manufacturer_contact_electronic",
    "responsible_person_identity",
    "responsible_person_postal",
    "responsible_person_electronic",
    "product_image_present",
    "warnings_or_safety_info",
    "instructions_language_ok",
)

BLOCK_TAGS = {"address", "article", "br", "div", "li", "p", "section", "tr"}


class _VisibleHTML(HTMLParser):
    """Create text while retaining an index map back to the original HTML."""

    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=False)
        self.source = source
        self.parts: list[str] = []
        self.offsets: list[int | None] = []
        self.line_starts = [0]
        self.line_starts.extend(index + 1 for index, char in enumerate(source) if char == "\n")

    def _raw_index(self) -> int:
        line, column = self.getpos()
        return self.line_starts[line - 1] + column

    def _separator(self) -> None:
        if self.parts and not self.parts[-1].endswith(("\n", " ")):
            self.parts.append("\n")
            self.offsets.append(None)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in BLOCK_TAGS:
            self._separator()

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in BLOCK_TAGS:
            self._separator()

    def handle_data(self, data: str) -> None:
        start = self._raw_index()
        self.parts.append(data)
        self.offsets.extend(range(start, start + len(data)))

    def handle_entityref(self, name: str) -> None:
        start = self._raw_index()
        token = self.source[start : self.source.find(";", start) + 1]
        if not token.endswith(";"):
            token = f"&{name};"
        self.parts.append(token)
        self.offsets.extend(range(start, start + len(token)))

    def handle_charref(self, name: str) -> None:
        start = self._raw_index()
        token = self.source[start : self.source.find(";", start) + 1]
        if not token.endswith(";"):
            token = f"&#{name};"
        self.parts.append(token)
        self.offsets.extend(range(start, start + len(token)))

    def text_and_offsets(self) -> tuple[str, list[int | None]]:
        return "".join(self.parts), self.offsets


class _Source:
    def __init__(self, raw: str, source_format: str) -> None:
        self.raw = raw
        self.source_format = source_format
        if source_format == "html":
            parser = _VisibleHTML(raw)
            parser.feed(raw)
            parser.close()
            self.text, self.offsets = parser.text_and_offsets()
        elif source_format == "text":
            self.text = raw
            self.offsets = list(range(len(raw)))
        else:
            raise ValueError("source_format must be 'text' or 'html'")

    def span(self, start: int, end: int, source: str = "description") -> dict[str, Any] | None:
        if start < 0 or end <= start or end > len(self.offsets):
            return None
        mapped = [offset for offset in self.offsets[start:end] if offset is not None]
        if not mapped:
            return None
        raw_start, raw_end = min(mapped), max(mapped) + 1
        quote = self.raw[raw_start:raw_end]
        if not quote:
            return None
        return {
            "source": source,
            "quote": quote,
            "char_start": raw_start,
            "char_end": raw_end,
        }

    def span_for_raw(self, start: int, end: int, source: str) -> dict[str, Any] | None:
        if start < 0 or end <= start or end > len(self.raw):
            return None
        return {
            "source": source,
            "quote": self.raw[start:end],
            "char_start": start,
            "char_end": end,
        }


def _field(
    status: str = "ABSENT",
    value: Any = None,
    confidence: float = 0.65,
    evidence_span: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "status": status,
        "value": value,
        "evidence_span": evidence_span,
        "confidence": confidence,
        "extra": extra or {},
    }


def _make_field_from_match(
    source: _Source,
    match: re.Match[str] | None,
    value_group: str = "value",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if match is None:
        return _field()
    value = match.group(value_group).strip()
    span = source.span(match.start(), match.end())
    if not value or span is None:
        return _field("UNPARSEABLE", None, 0.0, None, extra)
    return _field("PRESENT", value, 0.86, span, extra)


def _label_match(text: str, labels: str, *, value_pattern: str = r"[^\r\n]+") -> re.Match[str] | None:
    pattern = re.compile(
        rf"(?im)^[ \t]*(?P<label>{labels})[ \t]*[:：=\-][ \t]*(?P<value>{value_pattern})[ \t]*$"
    )
    return pattern.search(text)


def _language_codes(text: str) -> list[str]:
    explicit = re.search(r"\(([a-z]{2})\)", text, re.IGNORECASE)
    if explicit:
        return [explicit.group(1).lower()]
    labels = (
        ("nl", ("waarschuwing", "let op", "buiten bereik")),
        ("en", ("warning", "keep away", "do not")),
        ("de", ("achtung", "warnung", "von kindern")),
        ("fr", ("avertissement", "tenir hors", "ne pas")),
        ("es", ("advertencia", "mantener fuera", "no utilizar")),
        ("it", ("avvertenza", "tenere lontano", "non utilizzare")),
        ("pl", ("ostrzeżenie", "trzymać z dala", "nie używać")),
    )
    lowered = text.casefold()
    return [code for code, cues in labels if any(cue in lowered for cue in cues)]


def _find_image(source: _Source) -> dict[str, Any]:
    if source.source_format == "html":
        match = re.search(r"<img\b[^>]*>", source.raw, re.IGNORECASE | re.DOTALL)
        if match:
            return _field("PRESENT", True, 0.95, source.span_for_raw(match.start(), match.end(), "images"))
    return _field("AMBIGUOUS", None, 0.0)


def _deterministic_fields(source: _Source) -> dict[str, dict[str, Any]]:
    text = source.text
    fields: dict[str, dict[str, Any]] = {}

    identifier_match = re.search(
        r"(?im)^[ \t]*(?P<label>EAN(?:-?13|-?8)?|GTIN(?:-?12|-?13|-?14)?|barcode|product\s*(?:id|identifier)|SKU|model(?:\s*(?:number|no\.?))?|batch(?:\s*(?:number|no\.?))?|serial(?:\s*(?:number|no\.?))?)[ \t]*[:：=#\-][ \t]*(?P<value>[A-Za-z0-9][A-Za-z0-9._/ -]{2,38})[ \t]*$",
        text,
    )
    identifier_extra: dict[str, Any] = {"identifier_kind": "none"}
    if identifier_match:
        label = identifier_match.group("label").casefold().replace("-", "")
        value = identifier_match.group("value").strip()
        if label.startswith("ean"):
            size = len(re.sub(r"\D", "", value))
            kind = "ean8" if size == 8 else "ean13" if size == 13 else "other"
        elif label.startswith("gtin"):
            size = len(re.sub(r"\D", "", value))
            kind = "ean8" if size == 8 else "ean13" if size == 13 else f"gtin{size}" if size in (12, 14) else "other"
        elif label.startswith(("sku", "model")): 
            kind = "model"
        elif label.startswith("batch"):
            kind = "batch"
        elif label.startswith("serial"):
            kind = "serial"
        else:
            kind = "other"
        identifier_extra["identifier_kind"] = kind
    fields["product_identifier"] = _make_field_from_match(
        source, identifier_match, extra=identifier_extra
    )

    fields["manufacturer_identity"] = _make_field_from_match(
        source,
        _label_match(text, r"manufacturer(?:\s+name)?|producer|produced\s+by|made\s+by"),
    )
    fields["manufacturer_contact_postal"] = _make_field_from_match(
        source,
        _label_match(
            text,
            r"manufacturer(?:\s+postal)?\s+address|manufacturer\s+postal\s+contact|manufacturer\s+address",
        ),
    )
    fields["manufacturer_contact_electronic"] = _make_field_from_match(
        source,
        _label_match(
            text,
            r"manufacturer\s+(?:e-?mail|electronic\s+contact|contact\s+url)|manufacturer\s+contact",
        ),
    )
    fields["responsible_person_identity"] = _make_field_from_match(
        source,
        _label_match(
            text,
            r"(?:EU\s+)?responsible\s+person(?:\s+name)?|EU\s+responsible\s+operator|responsible\s+economic\s+operator",
        ),
    )
    fields["responsible_person_postal"] = _make_field_from_match(
        source,
        _label_match(
            text,
            r"(?:EU\s+)?responsible\s+person\s+(?:postal\s+)?address|responsible\s+operator\s+address",
        ),
    )
    fields["responsible_person_electronic"] = _make_field_from_match(
        source,
        _label_match(
            text,
            r"(?:EU\s+)?responsible\s+person\s+(?:e-?mail|electronic\s+contact|contact\s+url)|responsible\s+operator\s+contact",
        ),
    )

    warning_match = _label_match(
        text,
        r"safety\s+warnings?(?:\s+\([a-z]{2}\))?|warnings?(?:\s+\([a-z]{2}\))?|safety\s+information",
    )
    warning = _make_field_from_match(source, warning_match)
    warning_text = warning["value"] or ""
    language_evidence = warning_match.group(0) if warning_match else warning_text
    warning["extra"] = {
        "languages_detected": _language_codes(language_evidence),
        "explicit_none_claimed": bool(re.search(r"(?i)\b(no|none|not applicable|geen|keine)\s+(?:safety\s+)?warnings?\b", warning_text)),
    }
    fields["warnings_or_safety_info"] = warning
    fields["product_image_present"] = _find_image(source)
    fields["instructions_language_ok"] = _field(
        "AMBIGUOUS", None, 0.0, None, {"reason": "Destination country and instruction text were not assessed"}
    )
    return fields


def _model_schema() -> dict[str, Any]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    return {
        "$schema": contract["$schema"],
        "$defs": {
            key: contract["$defs"][key]
            for key in ("EvidenceSpan", "FieldExtraction", "ListingFields")
        },
        "$ref": "#/$defs/ListingFields",
    }


def _call_nano(text: str, listing_id: str, api_key: str, model: str) -> dict[str, Any]:
    """Call the documented OpenAI-compatible Token Factory chat-completions API."""
    schema = _model_schema()
    prompt = (
        "Extract only fields explicitly present in this product listing. Do not infer missing values. "
        "Return one JSON object conforming to the supplied ListingFields JSON Schema. "
        "Every PRESENT field must include an exact evidence_span.quote copied from listing_text; "
        "use null evidence_span for absent or ambiguous fields. Set listing_id exactly as provided. "
        "Use status PRESENT, ABSENT, AMBIGUOUS, or UNPARSEABLE and confidence between 0 and 1.\n"
        f"listing_id: {listing_id}\nlisting_text:\n{text}"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You extract product-listing fields. Never invent evidence."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "listing_fields", "strict": True, "schema": schema},
        },
    }
    base_url = os.getenv("NEBIUS_BASE_URL", MODEL_BASE_URL).rstrip("/")
    request = Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    content = result["choices"][0]["message"]["content"]
    if isinstance(content, list):
        content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    data = json.loads(content) if isinstance(content, str) else content
    if not isinstance(data, dict):
        raise TypeError("Nano returned a non-object response")
    return data


def _model_fields(
    source: _Source, deterministic: dict[str, dict[str, Any]], response: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    candidates = response.get("fields", response)
    if not isinstance(candidates, dict):
        return deterministic
    result = dict(deterministic)
    for key in FIELD_KEYS:
        candidate = candidates.get(key)
        if not isinstance(candidate, dict):
            continue
        status = candidate.get("status")
        if status not in {"PRESENT", "ABSENT", "AMBIGUOUS", "UNPARSEABLE"}:
            result[key] = _field("UNPARSEABLE", None, 0.0)
            continue
        confidence = candidate.get("confidence", 0.0)
        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.0
        if not math.isfinite(confidence) or confidence < 0 or confidence > 1:
            confidence = 0.0

        # Model absence is not observable evidence. Keep the deterministic
        # result for absent fields rather than converting a model guess into a
        # missing-field compliance finding.
        if status == "ABSENT":
            continue
        # Image presence is measured from HTML and instruction-language
        # applicability needs destination metadata not included in this stage.
        if key in {"product_image_present", "instructions_language_ok"}:
            continue
        span_data = candidate.get("evidence_span")
        quote = span_data.get("quote") if isinstance(span_data, dict) else None
        if status == "PRESENT":
            if not isinstance(quote, str) or not quote:
                result[key] = _field("UNPARSEABLE", None, 0.0)
                continue
            visible_start = source.text.find(quote)
            if visible_start < 0:
                result[key] = _field("UNPARSEABLE", None, 0.0)
                continue
            value = candidate.get("value")
            if key == "warnings_or_safety_info" and isinstance(value, list):
                supported_value = all(isinstance(item, str) and item.strip() in quote for item in value)
            else:
                supported_value = isinstance(value, str) and bool(value.strip()) and value.strip() in quote
            if not supported_value:
                result[key] = _field("UNPARSEABLE", None, 0.0)
                continue
            span = source.span(visible_start, visible_start + len(quote), "description")
            if span is None:
                result[key] = _field("UNPARSEABLE", None, 0.0)
                continue
            raw_extra = candidate.get("extra")
            extra: dict[str, Any] = raw_extra if isinstance(raw_extra, dict) else {}
            if key == "product_identifier":
                valid_kinds = {"ean13", "ean8", "gtin12", "gtin14", "model", "batch", "serial", "other", "none"}
                if extra.get("identifier_kind") not in valid_kinds:
                    extra["identifier_kind"] = "other"
            if key == "warnings_or_safety_info":
                extra["languages_detected"] = _language_codes(quote)
                extra["explicit_none_claimed"] = bool(
                    re.search(
                        r"(?i)\b(no|none|not applicable|geen|keine)\s+(?:safety\s+)?warnings?\b",
                        quote,
                    )
                )
            result[key] = _field("PRESENT", value, confidence, span, extra)
        elif status == "AMBIGUOUS":
            result[key] = _field("AMBIGUOUS", candidate.get("value"), confidence, None,
                                 candidate.get("extra") if isinstance(candidate.get("extra"), dict) else {})
        else:
            result[key] = _field("UNPARSEABLE", None, 0.0)
    return result


def _validate_fields(fields: dict[str, dict[str, Any]], source: _Source) -> bool:
    if set(fields) != set(FIELD_KEYS):
        return False
    for field in fields.values():
        if field.get("status") not in {"PRESENT", "ABSENT", "AMBIGUOUS", "UNPARSEABLE"}:
            return False
        confidence = field.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            return False
        span = field.get("evidence_span")
        if field["status"] == "PRESENT":
            if not isinstance(span, dict):
                return False
            start, end, quote = span.get("char_start"), span.get("char_end"), span.get("quote")
            if not isinstance(start, int) or not isinstance(end, int) or not isinstance(quote, str):
                return False
            if source.raw[start:end] != quote:
                return False
    return True


def extract_fields(
    listing_text: str,
    *,
    source_format: str = "text",
    use_model: bool = True,
    model_call: Callable[[str, str, str, str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Extract ListingFields; demote every unsupported model quote to UNPARSEABLE."""
    if not isinstance(listing_text, str) or not listing_text.strip():
        raise ValueError("listing_text must be a non-empty string")
    if len(listing_text) > MAX_INPUT_CHARS:
        raise ValueError(f"listing_text exceeds {MAX_INPUT_CHARS} characters")
    source = _Source(listing_text, source_format)
    listing_id = f"ls_{uuid4().hex}"
    fields = _deterministic_fields(source)
    model = "deterministic"
    model_name = os.getenv("MODEL_NANO", "").strip()
    api_key = os.getenv("NEBIUS_API_KEY", "").strip()
    if use_model and api_key and model_name:
        caller = model_call or _call_nano
        try:
            response = caller(source.text, listing_id, api_key, model_name)
            fields = _model_fields(source, fields, response)
            model = model_name
        except (OSError, ValueError, KeyError, IndexError, TypeError):  # Deterministic fallback.
            model = f"deterministic_fallback:{model_name}"

    min_confidence = min((float(field["confidence"]) for field in fields.values()), default=0.0)
    output = {
        "listing_id": listing_id,
        "fields": fields,
        "model": model,
        "schema_ok": False,
        "min_confidence": min_confidence,
        "ledger_id": "led_s2_local",
    }
    output["schema_ok"] = _validate_fields(fields, source)
    if not output["schema_ok"]:
        raise ValueError("S2 produced a result that violates the ListingFields contract")
    return output
