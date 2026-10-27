import { useEffect, useState, type FormEvent } from 'react';
import { DEMO_PRODUCTS, UNVERIFIED_ALERT_REFERENCE, type DemoProduct } from './demoData';
import './static-demo.css';

type ScreenedDemo = {
  title: string;
  category: string;
  attributes: string[];
  matchingSample: DemoProduct | undefined;
};

function getWords(text: string): string[] {
  return [...new Set(text.toLowerCase().match(/[a-z0-9]+/g) ?? [])];
}

export default function StaticDemoDashboard() {
  const [selectedId, setSelectedId] = useState(DEMO_PRODUCTS[0].id);
  const [listingText, setListingText] = useState(DEMO_PRODUCTS[0].title);
  const [screened, setScreened] = useState<ScreenedDemo | null>(null);
  const [offline, setOffline] = useState(!navigator.onLine);
  const [copyMessage, setCopyMessage] = useState('');

  useEffect(() => {
    const update = () => setOffline(!navigator.onLine);
    window.addEventListener('online', update);
    window.addEventListener('offline', update);
    return () => {
      window.removeEventListener('online', update);
      window.removeEventListener('offline', update);
    };
  }, []);

  function chooseSample(product: DemoProduct) {
    setSelectedId(product.id);
    setListingText(product.title);
    setScreened(null);
    setCopyMessage('');
  }

  function screenListing(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const sample = DEMO_PRODUCTS.find((product) => product.title === listingText.trim());
    setScreened({
      title: listingText.trim(),
      category: sample?.category ?? 'User-entered demo text; category not classified',
      attributes: sample?.demoAttributes ?? getWords(listingText.trim()).slice(0, 8),
      matchingSample: sample,
    });
  }

  async function copyDraft() {
    if (!screened) return;
    const draft = [
      'SYNTHETIC STATIC-DEMO LISTING SUMMARY — NOT A COMPLIANCE PACK',
      `Product title: ${screened.title}`,
      `Demo category: ${screened.category}`,
      `Title terms: ${screened.attributes.join(', ')}`,
      'Manufacturer and EU responsible-person contacts: not supplied in this demo input.',
      'No legal conclusion or product-publication recommendation is provided.',
    ].join('\n');
    try {
      await navigator.clipboard.writeText(draft);
      setCopyMessage('Demo summary copied. It is not a compliance pack.');
    } catch {
      setCopyMessage('Clipboard is unavailable in this browser.');
    }
  }

  return (
    <main className="shell static-demo">
      <header className="topbar">
        <a className="brand" href="./" aria-label="RedFlag home"><span className="brand-mark">R</span> REDFLAG <span className="brand-tag">STATIC DEMO</span></a>
        <span className={`demo-network ${offline ? 'is-offline' : ''}`}><span className="live-dot" />{offline ? 'OFFLINE — LOCAL SIMULATION' : 'NO API / CLIENT-SIDE DEMO'}</span>
      </header>

      <section className="marketplace-intro">
        <p className="eyebrow">EU PRODUCT-SAFETY / MARKETPLACE PREVIEW</p>
        <h1>Screen the evidence.<br /><span>Keep uncertainty visible.</span></h1>
        <p className="intro-copy">A static walkthrough of listing-field extraction and recall review. All three listings are synthetic title-only examples; no official legal or recall decision is made.</p>
      </section>

      <aside className="source-caveat" aria-label="Unverified statistic and date">
        <strong>PROJECT NOTES — SOURCE CHECK PENDING</strong>
        <p>The project specification records 13 December 2024 as the GPSR applicability date and cites a 58% figure for offers displaying manufacturer, EU responsible-person, and product-ID information together. The primary sources and exact wording have not been verified here; these claims do not drive this demo.</p>
      </aside>

      <div className={`static-banner ${screened ? 'static-banner-hold' : ''}`} role="status" aria-live="polite">
        <span className="alert-mark" aria-hidden="true">!</span>
        <div>
          <strong>{screened ? 'DEMO HOLD — CONTACT EVIDENCE NOT SUPPLIED' : 'STATIC DEMO — NO LEGAL SCREENING RESULT'}</strong>
          <p>{screened
            ? 'This title-only example contains no verified manufacturer or EU responsible-person contact documents. Publication is paused in this demonstration only; legal applicability and CE-documentation requirements are not assessed.'
            : 'Choose a sample and select “Screen listing” to see simulated S2 extraction. This page uses no API and does not establish compliance, danger, or recall status.'}</p>
        </div>
      </div>

      <section className="sample-section" aria-labelledby="sample-title">
        <div className="section-heading"><div><p className="eyebrow">01 / SYNTHETIC SAMPLE LISTINGS</p><h2 id="sample-title">Choose a marketplace card</h2></div><span className="step-number">3 DEMO INPUTS</span></div>
        <div className="sample-grid">
          {DEMO_PRODUCTS.map((product, index) => <article className={`sample-card ${selectedId === product.id ? 'sample-selected' : ''}`} key={product.id}>
            <div className="sample-card-top"><span>DEMO PRODUCT {index + 1}</span><span>{product.category}</span></div>
            <h3>{product.title}</h3>
            <p>{product.note}</p>
            <button className="sample-pick" type="button" onClick={() => chooseSample(product)}>{selectedId === product.id ? 'Selected' : 'Use this sample'}</button>
          </article>)}
        </div>
      </section>

      <div className="static-dashboard-grid">
        <section className="panel static-input-panel" aria-labelledby="input-title">
          <div className="panel-heading"><div><p className="eyebrow">02 / LISTING INGESTION</p><h2 id="input-title">Listing text</h2></div><span className="step-number">SYNTHETIC</span></div>
          <form onSubmit={screenListing}>
            <label htmlFor="demo-listing">Raw title / listing text</label>
            <textarea id="demo-listing" rows={4} maxLength={10000} value={listingText} onChange={(event) => { setListingText(event.target.value); setScreened(null); }} />
            <button className="primary-action" type="submit">Screen Listing <span aria-hidden="true">→</span></button>
          </form>
          <div className="demo-local-note">Client-side simulation · No network request · No external listing fetch</div>
        </section>

        <section className="panel static-twin-panel" aria-labelledby="twin-title">
          <div className="panel-heading"><div><p className="eyebrow">03 / RECALL TWIN REVIEW</p><h2 id="twin-title">Safety Gate reference</h2></div><span className="step-number">NOT VERIFIED</span></div>
          {!screened ? <div className="corpus-empty"><strong>Awaiting a demo screen</strong><p>Run the local simulation to see extracted title terms and the unverified reference notice.</p></div> : <div>
            <div className="comparison-grid">
              <article className="comparison-side listing-side">
                <span className="comparison-label">SELECTED DEMO LISTING</span>
                <h3>{screened.title}</h3>
                <p>{screened.category}</p>
                <div className="term-pills">{screened.attributes.map((term) => <span key={term}>{term}</span>)}</div>
                <small>Title-term extraction only; not a risk classification.</small>
              </article>
              {screened.matchingSample?.id === 'magnetic-spheres' ? <article className="comparison-side alert-side">
                <span className="comparison-label">UNVERIFIED REFERENCE FROM TASK</span>
                <h3>Alert ref: {UNVERIFIED_ALERT_REFERENCE.alertNumber}</h3>
                <p>{UNVERIFIED_ALERT_REFERENCE.riskDescription}</p>
                <div className="unverified-note">{UNVERIFIED_ALERT_REFERENCE.sourceStatus}</div>
                <div className="term-overlap">Text overlap: “magnetic” appears in both labels. This is not an official alert match, vector match, or finding that products share a defect.</div>
              </article> : <article className="comparison-side alert-side">
                <span className="comparison-label">RECALL DATA STATUS</span>
                <h3>No verified alert comparison</h3>
                <p>No official sample corpus is bundled in this Pages demo.</p>
                <div className="unverified-note">No comparison made for this product example. No conclusion about recall status or safety.</div>
              </article>}
            </div>
            <p className="static-recall-disclaimer">The prompt-supplied alert reference is not represented as an official EU record and is not used to determine product safety.</p>
          </div>}
        </section>
      </div>

      {screened && <section className="panel static-extraction" aria-labelledby="extract-title">
        <div className="panel-heading"><div><p className="eyebrow">04 / SIMULATED S2 FIELD EXTRACTION</p><h2 id="extract-title">Evidence snapshot</h2></div><span className="step-number">LOCAL MOCK</span></div>
        <dl className="static-field-list">
          <div><dt>Product title terms</dt><dd>{screened.attributes.join(' · ') || 'No title terms found'}</dd></div>
          <div><dt>Product identifier / GTIN</dt><dd>Not supplied in this title-only sample</dd></div>
          <div><dt>Manufacturer / EU responsible person</dt><dd>Not supplied in this title-only sample</dd></div>
          <div><dt>Contact / CE documents</dt><dd>Not supplied; CE obligations are not assessed</dd></div>
          <div><dt>Legal rule status</dt><dd>UNDETERMINED — this static demo performs no statutory evaluation</dd></div>
        </dl>
        <button className="copy-action" type="button" onClick={copyDraft}>Copy draft demo summary <span aria-hidden="true">⎘</span></button>
        {copyMessage && <p className="copy-state" role="status">{copyMessage}</p>}
      </section>}

      <section className="static-limitations" aria-labelledby="limits-title">
        <p className="eyebrow">LIMITS / READ BEFORE REUSE</p>
        <h2 id="limits-title">What this demo cannot verify</h2>
        <ul>
          <li>No official Safety Gate sample corpus or confirmed recall match is bundled.</li>
          <li>No live EUR-Lex synchronization, marketplace fetch, or legal evaluation is performed.</li>
          <li>The alert reference is prompt-supplied and unverified; the three product titles are synthetic examples.</li>
          <li>Offline playback is a static browser simulation, not a sandbox network-isolation test.</li>
        </ul>
      </section>

      <footer><span>REDFLAG / STATIC CLIENT-SIDE DEMO</span><span>Not legal advice · No verified alert records · No official determination</span></footer>
    </main>
  );
}
