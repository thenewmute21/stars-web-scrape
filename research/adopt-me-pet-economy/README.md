# Adopt Me! / Roblox Pet-Economy: OSINT, Exploit Taxonomy & Defensive Engineering

**Execution date: 2026-10-19 (UTC).** Research horizon: Adopt Me! launch (2017) to the execution date.
Purpose: authorized **defensive** research for designing a secure, original Roblox pet-collection and trading game.
Nothing here was tested against, or exploits, any live third-party experience.

## Hero summary

**Real pets were only ever created or duplicated through the game's own server code, its persistence layer, or people and credentials.** Pet "spawners" and imported Blender models give you visuals or asset IDs, not inventory. For our game, the dangerous weaknesses are:

1. **Persistence races:** saving after a failed load, and gaps in session locks.
2. **Non-atomic two-player trades.**
3. **Duplicate purchase receipts.**
4. **Privileged paths:** owner, collaborator, Toolbox, Open Cloud key and support tooling.
5. **Refunds and account-takeover rollbacks** that touch pets which have already been traded on.

Start with [`00_EXECUTIVE_BRIEF.md`](00_EXECUTIVE_BRIEF.md).

## Files

| File | What it is |
|---|---|
| [00_EXECUTIVE_BRIEF.md](00_EXECUTIVE_BRIEF.md) | Top 10 risks, verified Adopt Me! findings vs general Roblox risks, highest-ROI defenses, P0 checklist |
| [01_EVIDENCE_LEDGER.csv](01_EVIDENCE_LEDGER.csv) | 218 material claims (OFF-/AM-/RBX-/IMP-/ECO-/FU-) with outcome A–H, confidence, status, verification basis, defensive implication |
| [02_HISTORICAL_TIMELINE.md](02_HISTORICAL_TIMELINE.md) | Year by year, 2017–2026, in three lanes (Adopt Me!, platform, other games); gaps marked explicitly; corrections table |
| [03_ATTACK_SURFACE_MATRIX.md](03_ATTACK_SURFACE_MATRIX.md) | 55 acquisition and abuse channels covering every prompt category 1–14, sorted by risk to our game; creator-motive analysis |
| [04_EXTERNAL_ASSET_IMPORT_REALITY_CHECK.md](04_EXTERNAL_ASSET_IMPORT_REALITY_CHECK.md) | Visual asset vs real entitlement; import mechanisms; provenance controls AP-01..AP-11 |
| [05_SECURE_ARCHITECTURE.md](05_SECURE_ARCHITECTURE.md) | 11 Mermaid diagrams, data model, receipt/mint/trade/audit/recovery/permissions design, typed Luau reference modules, P0 checklist, MVP sequence, post-research addendum §A |
| [06_TEST_PLAN.md](06_TEST_PLAN.md) | Private test-universe harness: fault-injecting FakeDataStore, FakeSession, FakeClock; tests T01–T37 plus AP tests; exit criteria |
| [07_BACKLOG.csv](07_BACKLOG.csv) | 44 ordered items (17 × P0) with complexity, estimated cost, dependencies, owner, acceptance test, evidence |
| [08_SOURCE_INDEX.md](08_SOURCE_INDEX.md) | Annotated sources, coverage by category, empty searches, limitations, re-verification queue |
| [09_PREMORTEM_POSTMORTEM.md](09_PREMORTEM_POSTMORTEM.md) | Pre-mortem (16 failure modes), post-mortem scoring, corrections, open questions, residual risk |
| `_notes/` | Raw research notes per workstream, partial ledgers, agent brief, follow-up verification |

## Labels

- **Outcomes:**
  - A: legitimate persistent pet
  - B: legitimate pet obtained without direct Robux
  - C: unauthorized server-issued pet or balance
  - D: duplication or replayed grant
  - E: client-only visual or spoof
  - F: external asset that is not an entitlement
  - G: compromised, fraudulent, reversed or support-issued
  - H: unverified or fabricated
- **Confidence:** CONFIRMED / STRONGLY CORROBORATED / PLAUSIBLE / UNVERIFIED / DEBUNKED.
- **Status:** live-active / historical-patched / historical-unresolved / status-unknown / n/a-intended-design.
- **Priority:** P0 (launch-blocking) to P3.

## Coverage and limitations (read before citing)

- **Network:** this research ran in a sandbox whose egress policy blocked create.roblox.com, devforum.roblox.com, help centres, web.archive.org, x.com, playadopt.me and most press sites.
- **Roblox platform facts** were verified **verbatim** against Roblox's official docs source (`github.com/Roblox/creator-docs` @ `70a0110`, 2026-10-17). create.roblox.com renders from this source.
- **All Adopt Me!, press, DevForum and community claims are search-snippet-only.** They are capped at STRONGLY CORROBORATED and queued for re-verification in `08`.
- **Some planned searches never ran:** a shared search budget ran out mid-research. The list is in `08`.
- **The Luau has not been run:** there is no toolchain in this environment. Treat it as reference code. **A passing test harness does not make a production game secure.**
- **No claim is "live-active" solely because a video or listing advertises it.** No insider or backdoor allegation is made without primary evidence, and none was found for Uplift.
