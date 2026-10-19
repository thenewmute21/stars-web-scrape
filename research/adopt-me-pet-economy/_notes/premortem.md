# Pre-mortem (written 2026-10-19, before evidence collection)

Premise: assume the finished package is misleading or unsafe. Why?

| # | Failure mode | Early warning sign | Prevention | Quality gate / test | Owner |
|---|---|---|---|---|---|
| 1 | Treating scams as exploits | "Free pets" site or video counted as a dupe | Outcome ontology A–H applied to every row; scams default to E/G/H | Every ledger row has outcome_AH; no row with outcome C/D lacks a primary source | Fraud analyst |
| 2 | Mistaking UI replicas for server inventory | Evidence is a screenshot/video of an inventory screen | Require a server-side signal (trade completed with third party, official removal, dev statement) for C/D | C/D rows need ≥1 primary source or are downgraded to PLAUSIBLE/UNVERIFIED | OSINT lead |
| 3 | Claiming impossible cross-experience imports | Text says "upload a mesh and it becomes a pet in Adopt Me!" | Asset-chain diagram with authorization at each hop, grounded in create.roblox.com docs | 04 file cites docs for each hop | Asset-pipeline engineer |
| 4 | Hallucinating Adopt Me! incidents | An AM- row with no resolving URL | Agents told never to fabricate; links checked | link_checked column; AM- rows reviewed in post-mortem | OSINT lead |
| 5 | Confusing historical with active | Old 2020 dupe labeled live | Status column separate from confidence; "active" needs recent independent verification | No live-active label based only on an ad/video | Threat intel |
| 6 | Interpreting normal gameplay as payment bypass | Trading/earning flagged as an exploit | Outcome B + n/a-intended-design status | Category 1/2/12 rows reviewed for intent | Economy analyst |
| 7 | Trusting a single viral video | One YouTube/TikTok source for a claim | Corroboration rule: ≥2 independent sources for STRONGLY CORROBORATED | Confidence audit in post-mortem | OSINT lead |
| 8 | Missing cross-server races | Trade design assumes single server | Explicit tests for receipt to multiple servers, session-lock steal, teleport mid-trade | 06 test IDs cover cross-server | QA lead |
| 9 | Omitting purchase-id deduplication | ProcessReceipt sample grants without stored PurchaseId | Dedup inside the same UpdateAsync/profile write as the grant | Receipt-replay test in 06; P0 checklist item | Payment engineer |
| 10 | Unjustified insider allegations | "Staff gave pets"/"backdoor" asserted | Allegations = hypotheses unless primary evidence; separate generic risk from incident | Motive analysis (section 5) ranks with evidence | Lead |
| 11 | Unsafe reproduction | Steps/scripts that work on a live game | Architecture-level descriptions only; tests only on our own universe/mocks | Safety review of 03/06 before publish | Red/blue QA lead |
| 12 | Low-value generic recommendations | "Validate inputs" with no concrete check | Concrete module code, invariants, acceptance tests, P0 list | Post-mortem "could a dev implement from this alone?" ≥4/5 | Architect |
| 13 | Research scope sprawl | Notes drift into unrelated Roblox drama | Every row must map to a category 1–14 and a defensive implication | Ledger column defensive_implication non-empty | Lead |
| 14 | Obsolete API guidance (e.g., old ProcessReceipt sample, DataStore limits) | Numbers without dated citation | Re-verify on create.roblox.com as of execution date | OFF- rows link-checked 2026-10-19 | Architect |
| 15 | Circular sourcing (wiki citing Reddit citing video) | Same phrasing in multiple "sources" | Trace to originating post; count as one source | Post-mortem circularity review | OSINT lead |
| 16 | Overstating platform-generic risk as Adopt Me!-specific | RBX- incident cited in Adopt Me! section | game_specificity column; separate sections in brief | Brief keeps "verified Adopt Me!" vs "general Roblox" tables apart | Lead |

## Refined evidence standard
- CONFIRMED: first-party statement (Uplift/Roblox/other developer) or official docs, or ≥2 independent reputable outlets citing first-party.
- STRONGLY CORROBORATED: ≥2 independent non-first-party sources with consistent specifics (date, mechanism, response).
- PLAUSIBLE: technically consistent with documented platform behavior; single or weak source.
- UNVERIFIED: claim exists, no reliable support.
- DEBUNKED: contradicted by primary evidence or technical impossibility per docs.

## Refined search plan
1. Official platform docs first (fix the technical baseline). 2. First-party Adopt Me!/Uplift statements. 3. Reputable press. 4. DevForum post-mortems from other games (class evidence, not Adopt Me! evidence). 5. Community sources only as corroboration and to enumerate claims to test.
