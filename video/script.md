# Demo script — RedFlag evidence-gate prototype

> Use this script only for the current implementation. Do not claim that model routing, GPSR analysis, recall matching, or sandbox validation is live.

| Time | Visual | Narration |
|---|---|---|
| 0:00–0:20 | Show the input form and prototype label | “This is an early local prototype for checking evidence integrity. It is not a product-compliance assessment.” |
| 0:20–0:55 | Submit a quote that appears exactly in source text, then submit a mismatched quote | “The API checks whether the quote is an exact substring. This verifies text presence only—it does not show that the quote supports a claim.” |
| 0:55–1:25 | Select a GPSR rule and run a check | “The statutory source data is not yet verified. The gate returns UNDETERMINED instead of suggesting a legal conclusion.” |
| 1:25–1:55 | Check a valid GTIN, then an invalid check digit | “The current PASS and FAIL states are limited to this internal check-digit calculation. They do not mean that a product is compliant or safe.” |
| 1:55–2:25 | Show the placeholder check and test results | “The prototype also checks for a small set of common template placeholders. These are narrow software checks, not legal review.” |
| 2:25–2:50 | Show README limitations and proposed SPEC status note | “The larger system is a proposal. Listing ingestion, recall matching, verified legal rules, model calls, and sandbox validation remain future work.” |
