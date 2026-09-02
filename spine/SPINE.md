# PairwisePM — Spine

spine_version: 0.1
changelog:
  - 2026-08-30 · v0.1 · Initial Spine authored from the refined product definition (Hari, working session).

## The Problem

"When I compare two ideas on a Monday I pick one. Give me the same two ideas on Thursday and I'm honestly not sure I'd pick the same one. And when two of us score them with RICE, the spreadsheet says 47.3 versus 44.1 as if that gap means something."

Product managers deciding between competing Generative AI ideas produce noisy judgments: the same PM disagrees with themselves across occasions, different PMs disagree with each other, and the standard scorecards (RICE, ICE, WSJF) multiply soft 1–10 guesses into false-precision totals that hide the noise instead of removing it.

## The User

A product manager working on Generative AI applications, choosing between two competing ideas — either searching for product-market fit (0→1) or allocating a release under finite resources (1→N). Works solo or in a small team. Is not a statistician and should never need to be.

## Solution Direction

A mechanical pairwise judge. Two ideas enter on one standard questionnaire, on one screen, in one sitting; out comes the winner, a win probability with an interval, and the specific levers that would flip the verdict. The runtime model is a traditional offline model — weights and a bias term, no LLM, no API key. The LLM's contribution happened at build time: research, factor identification, and this repository. The model applies the PM's own policy more consistently than the PM can — it removes the Tuesdays.

## Success Metrics

- A PM completes a full A-vs-B comparison, from blank questionnaire to verdict card, in under 5 minutes.
- The tool runs entirely offline after download: no API key, no server-side storage, log fully in the user's hands.
- Model-of-the-judge activates from the user's own log by roughly decision 10; ζ (transitivity) and Brier accumulate from decision 1.
- The verdict is honest by construction: intervals shown always, "too close to call" when the interval straddles 50%, and 0→1 mode never claims predictive accuracy.

## Scope Boundaries

**In:** pairwise valuation of exactly two ideas; two modes (0→1 search, 1→N allocation) with GenAI-specific factor sets; decision log (JSONL, downloadable); leverage panel ("path to parity", lever-vs-fact filter, fragility flag); Hugging Face Gradio Space plus pip-installable repo.

**Out — refused, deliberately:** any LLM in the runtime loop; ranking more than two ideas at once (v1 is strictly A-vs-B); portfolio/knapsack automation (flagged, not decided); accuracy claims in 0→1 mode; evaluative factors (brand, strategic fit) inside the mechanical score — they are captured and displayed as labeled override inputs only; server-side storage of any user data.

A judge that overstates its confidence is worse than no judge, because PMs learn to ignore it — or worse, obey it. Every Leaf must preserve that refusal.

## Traceability Anchor

Every element of every Leaf maps back to a commitment on this page. The Compliance Leaf holds the matrix; anything in a Leaf that does not map back is scope creep or a missing Spine update.
