import React, { FormEvent, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './tokens.css';
import './app.css';

type Rule = {
  rule_id: string;
  title: string;
  severity: string | null;
  verified: boolean;
  legal: boolean;
  evaluator_available: boolean;
};

type AssessmentResult = {
  verdict: 'PASS' | 'FAIL' | 'UNDETERMINED' | string;
  reason: string;
  rule_id: string;
  evidence_verified: boolean;
  rule_verified: boolean;
  legal_compliance_verdict: string;
};

function App() {
  const [rules, setRules] = useState<Rule[]>([]);
  const [ruleId, setRuleId] = useState('RF-ART19-02');
  const [rawSource, setRawSource] = useState('');
  const [evidenceQuote, setEvidenceQuote] = useState('');
  const [claim, setClaim] = useState('');
  const [identifier, setIdentifier] = useState('');
  const [artifactText, setArtifactText] = useState('');
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    fetch('/v1/rules')
      .then(async (response) => {
        if (!response.ok) throw new Error(`Rules request failed (${response.status})`);
        return response.json();
      })
      .then((body: { rules: Rule[] }) => {
        setRules(body.rules);
        if (body.rules.length && !body.rules.some((rule) => rule.rule_id === ruleId)) {
          setRuleId(body.rules[0].rule_id);
        }
      })
      .catch((reason: Error) => setError(`${reason.message}. Start the API with “make serve”.`));
  }, []);

  const selectedRule = rules.find((rule) => rule.rule_id === ruleId);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError('');
    setResult(null);
    const assertion: Record<string, string> = {};
    if (claim.trim()) assertion.claim = claim.trim();
    if (ruleId === 'RF-ID-CHK') assertion.value = identifier.trim();
    if (ruleId === 'RF-PLACEHOLDER') assertion.artifact_text = artifactText;

    try {
      const response = await fetch('/v1/assessments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rule_id: ruleId,
          raw_source: rawSource,
          evidence_quote: evidenceQuote || null,
          assertion,
        }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail?.[0]?.msg ?? `Assessment failed (${response.status})`);
      setResult(body as AssessmentResult);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Request failed');
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="RedFlag home"><span className="brand-mark">R</span> REDFLAG <span className="brand-tag">PROTOTYPE</span></a>
        <span className="mode-indicator"><span className="live-dot" /> LOCAL CHECKS ONLY</span>
      </header>

      <section className="intro">
        <p className="eyebrow">PRODUCT-SAFETY EVIDENCE WORKBENCH</p>
        <h1>Check the evidence.<br /><span>Know what is not known.</span></h1>
        <p className="intro-copy">Verify whether a quote appears in the supplied text and run a small set of deterministic checks. Unverified legal rules abstain rather than imply compliance.</p>
      </section>

      <div className="notice" role="note">
        <strong>Prototype — not a compliance assessment.</strong> GPSR source rules are not yet verified. This tool does not determine whether a product may be sold, provide legal advice, or certify compliance.
      </div>

      <div className="workbench">
        <form className="panel form-panel" onSubmit={submit}>
          <div className="panel-heading"><div><p className="eyebrow">01 / INPUT</p><h2>Evidence check</h2></div><span className="step-number">01</span></div>

          <label htmlFor="rule">Rule or check</label>
          <select id="rule" value={ruleId} onChange={(event) => { setRuleId(event.target.value); setResult(null); }} disabled={!rules.length}>
            {rules.map((rule) => <option key={rule.rule_id} value={rule.rule_id}>{rule.rule_id} — {rule.title}{rule.verified ? '' : ' [UNVERIFIED]'}</option>)}
          </select>
          {selectedRule && <p className="field-hint">{selectedRule.verified ? 'Deterministic check available.' : 'Source not verified. This rule will return UNDETERMINED.'}</p>}

          <label htmlFor="source">Source text</label>
          <textarea id="source" value={rawSource} onChange={(event) => setRawSource(event.target.value)} required maxLength={100000} rows={6} placeholder="Paste the listing text or other source you want to check." />

          <label htmlFor="quote">Evidence quote <span className="optional">(exact substring)</span></label>
          <textarea id="quote" value={evidenceQuote} onChange={(event) => setEvidenceQuote(event.target.value)} maxLength={20000} rows={3} placeholder="Paste the exact wording to verify against the source." />
          <p className="field-hint">A matching quote establishes only that the text exists. It does not prove that it supports a legal claim.</p>

          {ruleId === 'RF-ID-CHK' && <><label htmlFor="identifier">GTIN / EAN to check</label><input id="identifier" value={identifier} onChange={(event) => setIdentifier(event.target.value)} inputMode="numeric" placeholder="e.g. 4006381333931" required /></>}
          {ruleId === 'RF-PLACEHOLDER' && <><label htmlFor="artifact">Artifact text to scan</label><textarea id="artifact" value={artifactText} onChange={(event) => setArtifactText(event.target.value)} rows={3} placeholder="Text to scan for common template placeholders." required /></>}
          {ruleId !== 'RF-ID-CHK' && ruleId !== 'RF-PLACEHOLDER' && <><label htmlFor="claim">Claim to review <span className="optional">(not semantically verified)</span></label><input id="claim" value={claim} onChange={(event) => setClaim(event.target.value)} placeholder="Optional claim text" /></>}

          <button type="submit" disabled={busy || !rules.length}>{busy ? 'Checking…' : 'Run evidence check'} <span aria-hidden="true">→</span></button>
          {error && <p className="error-message" role="alert">{error}</p>}
        </form>

        <section className="panel result-panel" aria-labelledby="result-title" aria-live="polite">
          <div className="panel-heading"><div><p className="eyebrow">02 / DETERMINISTIC RESULT</p><h2 id="result-title">Assessment</h2></div><span className="step-number">02</span></div>
          {!result ? <div className="empty-state"><div className="empty-icon">?</div><h3>Awaiting input</h3><p>Submit source text and a rule to see what this prototype can verify—and where it abstains.</p></div> : <div className="result-content">
            <div className={`verdict verdict-${result.verdict.toLowerCase()}`}><span className="verdict-label">{result.verdict}</span><span className="verdict-context">{result.rule_id}</span></div>
            <p className="result-reason">{result.reason}</p>
            <dl className="check-list">
              <div><dt>Exact quote found</dt><dd>{result.evidence_verified ? 'YES' : 'NO'}</dd></div>
              <div><dt>Rule verified</dt><dd>{result.rule_verified ? 'YES' : 'NO'}</dd></div>
              <div><dt>Legal compliance verdict</dt><dd>{result.legal_compliance_verdict}</dd></div>
            </dl>
            <p className="result-disclaimer">PASS/FAIL applies only to the supported local checksum or placeholder checks. It is not a GPSR compliance verdict.</p>
          </div>}
          <div className="result-footer"><span>NO MODEL CALLS</span><span>DETERMINISTIC / FAIL-CLOSED</span></div>
        </section>
      </div>

      <footer><span>REDFLAG / LOCAL EVIDENCE GATE</span><span>Human review required for legal decisions.</span></footer>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
