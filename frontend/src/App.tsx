import { useState, type FormEvent } from 'react';

type ListingField = {
  status: string;
  value: unknown;
  confidence: number;
  evidence_span?: { quote: string; source: string } | null;
};

type ListingFields = {
  listing_id: string;
  fields: Record<string, ListingField>;
};

type RecallCandidate = {
  alert_number: string;
  publication_date: string;
  notifying_country: string;
  category: string;
  product: string;
  risk_types: string[];
  danger_verbatim: string;
  alert_url: string;
  similarity: number;
  similarity_basis: string;
};

type ScreenResult = {
  listing_fields: ListingFields;
  verdict: {
    verdict: string;
    headline: string;
    action_first: { primary: string };
    gate: { abstain: boolean; abstain_reason: string | null };
    disclaimer: string;
  };
  recall_twin: {
    candidates: RecallCandidate[];
    shared_failure_mode: { verdict: string; reasoning: string; cited_alert_numbers: string[] };
  };
  risk_correlations: Array<{
    alert_number: string;
    matched_hazards: string[];
    alert_risk_types: string[];
  }>;
  recall_corpus_available: boolean;
  warnings: Array<{ code: string; alert_number: string; message: string }>;
};

const FIELD_LABELS: Record<string, string> = {
  product_identifier: 'Product identifier',
  manufacturer_identity: 'Manufacturer',
  manufacturer_contact_postal: 'Manufacturer postal contact',
  manufacturer_contact_electronic: 'Manufacturer electronic contact',
  responsible_person_identity: 'EU responsible person',
  responsible_person_postal: 'Responsible person postal contact',
  responsible_person_electronic: 'Responsible person electronic contact',
  product_image_present: 'Product image',
  warnings_or_safety_info: 'Warnings / safety information',
  instructions_language_ok: 'Instructions language',
};

function displayValue(field: ListingField): string {
  if (field.status !== 'PRESENT' || field.value === null || field.value === undefined) {
    return field.status === 'ABSENT' ? 'Not found in supplied text' : `Not determined (${field.status})`;
  }
  if (typeof field.value === 'boolean') return field.value ? 'Present' : 'Not present';
  return String(field.value);
}

function bannerText(verdict: string, headline: string): string {
  switch (verdict) {
    case 'WOULD_BE_SUPPRESSED':
      return `WOULD BE SUPPRESSED — ${headline}`;
    case 'AT_RISK':
      return `REVIEW NEEDED — ${headline}`;
    case 'COMPLIANT':
      return `NO FLAG FOUND — ${headline}`;
    default:
      return `UNDETERMINED — ${headline || 'Legal source rules are unverified; no compliance conclusion was made.'}`;
  }
}

export default function App() {
  const [inputMode, setInputMode] = useState<'text' | 'url'>('text');
  const [listingUrl, setListingUrl] = useState('');
  const [listingText, setListingText] = useState('');
  const [category, setCategory] = useState('');
  const [result, setResult] = useState<ScreenResult | null>(null);
  const [error, setError] = useState('');
  const [copyState, setCopyState] = useState('');
  const [busy, setBusy] = useState(false);

  async function screenListing(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setCopyState('');
    setResult(null);
    if (!listingText.trim()) {
      setError(inputMode === 'url'
        ? 'URL fetching is not enabled. Paste the visible listing text below to screen it locally.'
        : 'Paste listing text before screening.');
      return;
    }
    setBusy(true);
    try {
      const response = await fetch('/v1/listings/screen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          listing_text: listingText,
          source_format: 'text',
          product_category: category || null,
          description: listingText,
        }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail?.[0]?.msg ?? `Screening failed (${response.status})`);
      setResult(body as ScreenResult);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Request failed');
    } finally {
      setBusy(false);
    }
  }

  async function copyPack() {
    if (!result) return;
    const fields = Object.entries(result.listing_fields.fields)
      .map(([key, field]) => `${FIELD_LABELS[key] ?? key}: ${displayValue(field)}`)
      .join('\n');
    const content = [
      'REDFLAG — DRAFT PRODUCT INFORMATION PACK',
      'Marketplace targets: Amazon / bol.com',
      `Listing reference: ${listingUrl || 'Not supplied'}`,
      `Screening status: ${result.verdict.verdict}`,
      '',
      fields,
      '',
      'Draft extracted from seller-supplied listing text. Verify all information and applicable legal requirements before use.',
      'Not legal advice, certification, or a determination that a product may be sold.',
    ].join('\n');
    try {
      await navigator.clipboard.writeText(content);
      setCopyState('Draft information pack copied. Review it before use.');
    } catch {
      setCopyState('Clipboard access is unavailable in this browser.');
    }
  }

  const bannerVerdict = result?.verdict.verdict ?? 'UNDETERMINED';
  const bannerHeadline = result?.verdict.headline ?? 'Legal source rules are unverified; no compliance conclusion is available.';
  const candidates = result?.recall_twin.candidates ?? [];
  const correlationByAlert = new Map((result?.risk_correlations ?? []).map((item) => [item.alert_number, item]));

  return (
    <main className="shell marketplace-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="RedFlag home"><span className="brand-mark">R</span> REDFLAG <span className="brand-tag">MARKETPLACE PREVIEW</span></a>
        <span className="mode-indicator"><span className="live-dot" /> LOCAL SCREENING / HUMAN REVIEW</span>
      </header>

      <section className="marketplace-intro">
        <p className="eyebrow">SELLER LISTING PRE-FLIGHT</p>
        <h1>One listing.<br /><span>Evidence before exposure.</span></h1>
        <p className="intro-copy">Review extracted listing details alongside local recall leads. Unverified statutory rules abstain; this preview is not a product-compliance decision.</p>
      </section>

      <div className={`top-alert top-alert-${bannerVerdict.toLowerCase()}`} role="status" aria-live="polite">
        <span className="alert-mark" aria-hidden="true">!</span>
        <div><strong>{bannerText(bannerVerdict, bannerHeadline)}</strong><p>{result?.verdict.action_first.primary ?? 'Submit listing text to see the evidence screen. Missing or unverified evidence will not be treated as a legal failure.'}</p></div>
      </div>

      <div className="marketplace-grid">
        <section className="panel listing-panel" aria-labelledby="listing-title">
          <div className="panel-heading"><div><p className="eyebrow">01 / MOCK MARKETPLACE LISTING</p><h2 id="listing-title">Listing details</h2></div><span className="step-number">SELLER VIEW</span></div>
          <div className="input-tabs" role="group" aria-label="Listing input type">
            <button type="button" className={inputMode === 'text' ? 'tab-active' : ''} onClick={() => setInputMode('text')}>Raw text</button>
            <button type="button" className={inputMode === 'url' ? 'tab-active' : ''} onClick={() => setInputMode('url')}>Listing URL</button>
          </div>
          <form onSubmit={screenListing}>
            {inputMode === 'url' && <>
              <label htmlFor="listing-url">Listing URL <span className="optional">(reference only; not fetched)</span></label>
              <input id="listing-url" type="url" value={listingUrl} onChange={(event) => setListingUrl(event.target.value)} placeholder="https://marketplace.example/product/…" />
              <p className="field-hint">External page fetching is not enabled. Paste the page's visible text below; the URL is included only as a reference.</p>
            </>}
            <label htmlFor="category">Product category <span className="optional">(optional)</span></label>
            <input id="category" value={category} onChange={(event) => setCategory(event.target.value)} placeholder="e.g. toys, charger, cosmetics" />
            <label htmlFor="listing-text">{inputMode === 'url' ? 'Visible listing text' : 'Paste listing text'}</label>
            <textarea id="listing-text" value={listingText} onChange={(event) => setListingText(event.target.value)} required maxLength={100000} rows={9} placeholder={'Product: Example item\nEAN: 4006381333931\nManufacturer: Example GmbH\n'} />
            <button className="primary-action" type="submit" disabled={busy}>{busy ? 'Screening…' : 'Screen listing'} <span aria-hidden="true">→</span></button>
            {error && <p className="error-message" role="alert">{error}</p>}
          </form>
          <div className="marketplace-facts"><span>Input stays in this local prototype</span><span>No live marketplace fetch</span></div>
        </section>

        <section className="panel twin-panel" aria-labelledby="twin-title">
          <div className="panel-heading"><div><p className="eyebrow">02 / SAFETY GATE RETRIEVAL</p><h2 id="twin-title">Recalled twin</h2></div><span className="step-number">LOCAL CORPUS</span></div>
          {!result ? <div className="empty-state"><div className="empty-icon">↔</div><h3>Awaiting a listing</h3><p>Screen a listing to compare its category and risk signals with the locally available alert corpus.</p></div> : !result.recall_corpus_available ? <div className="corpus-empty" role="status"><strong>No local alert corpus available</strong><p>No recall comparison was made. This is not evidence that the product has no recall twin or is safe.</p></div> : candidates.length === 0 ? <div className="corpus-empty"><strong>No candidate retrieved</strong><p>The local keyword search returned no candidates. A negative sample search does not establish product safety.</p></div> : <div className="candidate-list">
            {candidates.map((candidate) => {
              const correlation = correlationByAlert.get(candidate.alert_number);
              return <article className="candidate-card" key={candidate.alert_number}>
                <div className="candidate-heading"><span className="candidate-label">RECALL LEAD</span><span className="candidate-score">{candidate.similarity_basis} · {Math.round(candidate.similarity * 100)}%</span></div>
                <h3>{candidate.product}</h3>
                <p className="alert-meta">{candidate.alert_number} · {candidate.category} · {candidate.notifying_country} · {candidate.publication_date}</p>
                <div className="hazard-comparison"><div><span>Alert risk</span><strong>{candidate.risk_types.join(', ') || 'Not listed'}</strong></div><div><span>Listing overlap</span><strong>{correlation?.matched_hazards.join(', ') || 'No keyword overlap identified'}</strong></div></div>
                <blockquote>{candidate.danger_verbatim}</blockquote>
                <p className="lead-warning">Keyword similarity is a review lead, not a finding that the listing is the same product or has the same defect.</p>
                <a className="alert-link" href={candidate.alert_url} target="_blank" rel="noreferrer">Open alert source <span aria-hidden="true">↗</span></a>
              </article>;
            })}
            <p className="recall-summary">{result.recall_twin.shared_failure_mode.verdict}: {result.recall_twin.shared_failure_mode.reasoning}</p>
          </div>}
        </section>
      </div>

      {result && <section className="panel details-panel" aria-labelledby="fields-title">
        <div className="panel-heading"><div><p className="eyebrow">03 / EXTRACTED FIELDS</p><h2 id="fields-title">Article 19 information snapshot</h2></div><span className="step-number">{result.listing_fields.listing_id}</span></div>
        <dl className="field-grid">{Object.entries(result.listing_fields.fields).map(([key, field]) => <div className="field-row" key={key}><dt>{FIELD_LABELS[key] ?? key}</dt><dd className={field.status === 'PRESENT' ? 'field-present' : 'field-unknown'}>{displayValue(field)}</dd></div>)}</dl>
        <button className="copy-action" type="button" onClick={copyPack}>Copy Article 19 Pack for Amazon / bol.com <span aria-hidden="true">⎘</span></button>
        {copyState && <p className="copy-state" role="status">{copyState}</p>}
        <p className="result-disclaimer">This is a draft of extracted information only. It is not a compliance pack, legal advice, or certification. Verify each field and source with a qualified reviewer.</p>
      </section>}

      {result?.warnings?.length ? <section className="review-warnings" aria-label="Recall review warnings"><h2>Manual review leads</h2>{result.warnings.map((warning) => <p key={`${warning.code}-${warning.alert_number}`}><strong>{warning.code}</strong> · {warning.alert_number} — {warning.message}</p>)}</section> : null}

      <footer><span>REDFLAG / LOCAL EVIDENCE SCREEN</span><span>Not legal advice. No product sale determination. Human review required.</span></footer>
    </main>
  );
}
