# 09 — Pre-mortem and Post-mortem

Execution date 2026-10-19. Part 1 was written before evidence collection; Part 2 after it, including one targeted follow-up research pass.

## Part 1 — Pre-mortem (written 2026-10-19, before evidence collection; unchanged)

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

### Refined evidence standard
- CONFIRMED: first-party statement (Uplift/Roblox/other developer) or official docs, or ≥2 independent reputable outlets citing first-party.
- STRONGLY CORROBORATED: ≥2 independent non-first-party sources with consistent specifics (date, mechanism, response).
- PLAUSIBLE: technically consistent with documented platform behavior; single or weak source.
- UNVERIFIED: claim exists, no reliable support.
- DEBUNKED: contradicted by primary evidence or technical impossibility per docs.

### Refined search plan
1. Official platform docs first (fix the technical baseline). 2. First-party Adopt Me!/Uplift statements. 3. Reputable press. 4. DevForum post-mortems from other games (class evidence, not Adopt Me! evidence). 5. Community sources only as corroboration and to enumerate claims to test.

---

## Part 2 — Post-mortem (written after the investigation, 2026-10-19)

The review below assumes the important conclusions might be wrong and checks them.

### 2.1 Did the pre-mortem failure modes happen?

| # | Failure mode | Outcome | Evidence |
|---|---|---|---|
| 1 | Scams treated as exploits | Avoided | Spawner and generator claims classed E/H. SEO and script-promo domains excluded (IMP-029, follow-up). |
| 2 | UI replicas mistaken for inventory | Avoided | 04 chain diagram; script listings themselves say "client-side" (AM-039). |
| 3 | Impossible cross-experience imports | Avoided | `LoadAsset` owner rules quoted verbatim from docs (IMP-, OFF-032..034). |
| 4 | Hallucinated Adopt Me! incidents | **Partly at risk** | No fabricated rows found in review. However, **every** AM- row is snippet-only (pages blocked), so a misquoted or misdated snippet cannot be ruled out. Mitigated by the confidence cap and the re-verification queue in 08. |
| 5 | Historical confused with active | Mostly avoided | 34 rows "live-active", mostly platform-design facts and policies that apply today. No exploit is labelled live-active on the strength of an advertisement alone. |
| 6 | Normal gameplay read as payment bypass | Avoided | 99+ rows `n/a-intended-design`; outcome B used for trading and earning. |
| 7 | Single viral video trusted | Avoided | No video-only claim rose above PLAUSIBLE. |
| 8 | Cross-server races missed | Avoided | Receipts on two servers (OFF-012), session-lock steal, teleport mid-trade tests (06). |
| 9 | Purchase-id dedup omitted | Avoided, and found a trap | Roblox's own simple developer-products sample does not dedupe. 05 dedupes inside the grant write. |
| 10 | Unjustified insider allegations | Avoided | AM-048 = no evidence. FU-003 is a second-hand report of a *compromised* staff account, labelled PLAUSIBLE. |
| 11 | Unsafe reproduction | Avoided | No scripts fetched or run. Tests target our own universe and mocks only. |
| 12 | Generic recommendations | Avoided | Typed modules, 37+ tests, 44 costed backlog items with acceptance tests. |
| 13 | Scope sprawl | Mild | Child-safety lawsuits are kept only as context rows, marked as not about trading design. |
| 14 | Obsolete API guidance | **Caught real changes** | `BindReceiptHandler`, Robux transfers, refund webhook, cross-game sales shutdown (2026), `FilteringEnabled` discontinued. |
| 15 | Circular sourcing | Partly at risk | Fan-wiki dupe histories for other games (RBX-025..035) may share upstream sources; kept at PLAUSIBLE. |
| 16 | Platform risk presented as Adopt Me!-specific | Avoided | `game_specificity` column; separate tables in 00 §1a/§1b. |

### 2.2 Skeptical questions

- **Can a skeptical engineer replicate the bug classes safely?** Yes. Each class in 03 maps to a test in 06 on a fault-injecting FakeDataStore, FakeSession and FakeClock, plus staging soak tests. **Caveat:** the Luau was never executed here, so the first run will surface syntax and API errors.
- **Is every Adopt Me!-specific case really confirmed?** No. None is page-verified. The strongest is the 2020-10-20 outage: an official post plus Roblox's own DevForum incident report (FU-004). The 2022-09-02 dupe rests on one first-party post with no independent corroboration.
- **Weak, duplicated or circular sources:**
  - other-game dupe histories (fan wikis);
  - cookie IP-binding ("community docs");
  - one-sided rollback abuse (a single DevForum report, ECO-028/RBX-039);
  - Adopt Me! revenue (estimates vary roughly 10×);
  - the Adopt Me! confirm delay (~15 s, community-reported only).
- **Which "loopholes" are intended gameplay or social engineering?**
  - Intended: trading Robux pets for earned ones; Neon/Mega crafting; events; gifting.
  - Social engineering: trust trades, phishing, beaming.
  - Policy or rule violations rather than code defects: event-currency farming (2025) and real-money trading.
- **Did we overstate present-day activity or possibility?**
  - We found no evidence of any currently working Adopt Me! duplication method and say so.
  - The 2026 FU-002 and FU-003 items are fan-reported only and labelled PLAUSIBLE.
- **Counterexamples to our leading hypotheses:**
  1. Uplift's help-center line "duplication is not possible" (AM-029) contradicts AM-024 and FU-001. We treat it as player-facing messaging about dupe-offer scams, not as a technical claim.
  2. The Oct 2020 incident was a **Roblox platform** fault (FU-004), not a game-code defect. Some loss events are outside the developer's control, which supports investing in recovery (ledger and restore tooling), not only prevention.
- **Omissions that would change priorities:**
  - **Refund clawback** and the **paid-item trading policy** were missing from the first architecture draft. They are now P0 (05 §A.1, §A.3).
  - The **new Robux-transfer API** could become a sanctioned route for selling pets for Robux; this needs a product decision.
  - The FU-003 compromised-staff-account report and FU-005 (anti-exploit kicking legitimate players) raise the priority of staff-account hardening and of measuring false positives.
- **What we can enforce in our own code versus what the platform constrains:**
  - Enforceable in our code: validation, dedup, session locks, sagas, ledger, kill switch, gates.
  - Platform-constrained: no multi-key transactions; best-effort MessagingService; non-durable MemoryStore; receipt-redelivery timing; refund-webhook id mapping (verify in staging); account-takeover prevention (we can only reduce its blast radius).
- **Are costs, UX effects and false positives represented?** Partly.
  - The backlog costs are estimates, not evidence.
  - UX costs are tabulated for trade holds, confirm delay and imbalance warnings (05).
  - False positives are evidenced by FU-005.
  - Privacy: data minimisation and retention for child users (ECO-034..036).
- **Could a developer implement the top fixes from these files alone?** Mostly yes. 05 §13 has the modules, §14 and §A.11 the checklist, and 06 the fixtures and tests. Gaps: the Luau is unexecuted, the CI runner is unspecified, and webhook hosting (off-platform) needs separate infrastructure decisions.

### 2.3 Scores (0–5)

| Dimension | Before follow-up | After follow-up | Notes |
|---|---|---|---|
| Evidence quality | 2 | **3** | Platform facts verified verbatim (CONFIRMED). All non-docs evidence is snippet-only. Follow-up added independent corroboration for 4 Adopt Me! claims. **Still below 4.** Fixing this needs page access, not more searching. |
| Breadth | 4 | 4 | All 14 categories touched. Bots/farming, spawner debunks and Uplift insider evidence remain partial. |
| Currency | 5 | 5 | Docs source dated 2026-10-17; 2026 API and policy changes captured. |
| Adopt Me! specificity | 2 | **3** | 68 AM-/FU- rows and a first-party chronology. Root causes are mostly unpublished by Uplift, which is an inherent ceiling. **Still below 4.** |
| Technical accuracy | 4 | 4 | Docs-verified facts. Several of our own design defects found and fixed (A.9 recover() read-failure, clock injection). Luau unexecuted. |
| Safe reproducibility | 4 | 4 | Owned-fixture tests only. Not yet executed. |
| Architectural specificity | 5 | 5 | Concrete data model, saga, dedup, mint, permissions, 11 diagrams. |
| Implementation usefulness | 4 | 4 | Costed P0 backlog with acceptance tests; MVP sequence. |

**Two dimensions remain below 4 after the revision pass.** We did not inflate them. The corrective action is outside this sandbox. See 2.5.

### 2.4 Before → after corrections made during this project

| Defect found | Correction |
|---|---|
| 40 rows marked CONFIRMED on the strength of search snippets | Downgraded to STRONGLY CORROBORATED; `verification_basis` and `confidence_pre_postmortem` columns added. |
| The prompt's premises: "2019/2021 support abuse", "2023 RDC leak" | Corrected: May 2020 support-panel abuse; Dec 2020 breach that surfaced Jul 2023 (02 corrections table). |
| The prompt's seed mention of `BindReceiptHandler` was unverified | Verified as real (2026) and documented with fallthrough semantics (OFF-015). |
| 08 coverage table used reconstructed categories | Replaced with the prompt's actual 14 categories. |
| Trade-timing tests depended on the wall clock | Injectable Clock and FakeClock added; deterministic expiry and recovery tests. |
| `recover()` treated a failed read like an absent record, which could compensate a committed trade and create a dupe | 05 §A.9, BL-08 (P0), test added. |
| No refund clawback, paid flag, kill switch, two-sided rollback or craft source in the design | 05 §A.1–A.8, tests T26–T37. |
| AP provenance tests were not linked from the test plan | 06 §8.4. |
| AM-034 date conflict | Resolved (event 2025-04-04, bans 2025-04-11). |

### 2.5 Open questions (corrected follow-ups)

1. **Re-open the 25-item re-verification queue (08)** from an environment that can reach x.com, playadopt.me, the Uplift help centre, devforum.roblox.com and web.archive.org. Upgrade or downgrade each row. Highest value: AM-024, AM-016, AM-029, FU-001, FU-003.
2. Did Uplift ever publish the mechanism behind the 2020-09-30 trading bug or the 2022-09-02 dupe? (Ask Uplift directly if necessary.)
3. Does the Transaction Refunded webhook's receipt id equal the `ProcessReceipt` `PurchaseId`? Verify in our staging universe.
4. How does `BindReceiptHandler` behave under concurrent delivery? Verify in staging.
5. Product decision: allow, ignore, or explicitly decouple `PromptRobuxTransferAsync` from pet trading?
6. Run the Luau through a real toolchain (Luau analyzer, plus the test runner the team picks) and fix what breaks.
7. Get Roblox ToS and Community Standards wording on real-money and off-platform trading verbatim.

### 2.6 Residual risks

- Account takeover can't be prevented at the game layer. We can only limit its blast radius (trade holds, two-sided reversal, kill switch).
- Platform incidents like the Oct 2020 DataStore fault can cause loss regardless of our code. Recovery tooling is the mitigation.
- Insider or compromised-staff risk persists even with dual approval: two colluding staff, or a compromised group owner.
- Detection thresholds will have false positives (FU-005). They need human review and a player appeal path.
- **A passing test harness is not proof of production security.** External review and staged rollout are still required.
