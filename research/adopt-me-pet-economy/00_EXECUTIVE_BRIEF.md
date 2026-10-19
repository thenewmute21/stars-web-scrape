# 00 — Executive Brief

**Adopt Me! / Roblox pet economy: what we found, and how to secure our own pet game**

Execution date **2026-10-19** · Scope: launch of Adopt Me! (2017) to the execution date · Purpose: defensive design of an original Roblox pet-collection and trading game.

---

## Hero summary

**Nobody in the evidence got a real pet without paying through Roblox's asset system or through client-side tricks.** Every confirmed or strongly corroborated case where pets were *really* created, duplicated or lost went through one of three routes:

1. the game's own **server code and persistence** (data loss, trade bugs, one first-party-acknowledged dupe);
2. **people and credentials**: stolen accounts, phished support staff, compromised developer or owner accounts;
3. **intended mechanics**: trading, earning, events, farming that was within or near the rules.

"Pet spawners", "pet generators" and imported Blender models produce **client-only visuals (outcome E)** or **assets that are not entitlements (outcome F)**. They are not inventory.

| Snapshot | Count / status |
|---|---|
| Evidence-ledger claims | **210** (60 docs-verified against Roblox's official docs source @ 2026-10-17; 150 search-snippet-only) |
| Adopt Me!-specific claims | 60 (none page-verified, because all source pages were blocked; best first-party items are STRONGLY CORROBORATED) |
| Adopt Me! duplication incidents acknowledged by Uplift | **1** (2022-09-02, AM-024). Root cause was never published. |
| Primary evidence of Uplift insider abuse or backdoors | **None** (AM-048) |
| Attack-surface rows / backlog items / test cases | 55 (ASM) / 44 (17 × P0) / T01–T37 + AP-01–AP-11 + soak tests |

Confidence labels: CONFIRMED / STRONGLY CORROBORATED / PLAUSIBLE / UNVERIFIED / DEBUNKED. Snippet-only items never exceed STRONGLY CORROBORATED. See `09_PREMORTEM_POSTMORTEM.md`.

---

## 1. Verified Adopt Me! findings vs general Roblox risks

### 1a. Adopt Me!-specific findings, all first-party posts seen via search snippet only

| Date | What happened | Outcome | Confidence | Ledger |
|---|---|---|---|---|
| 2020-04-22 | Data loss for "0.3% of our players… only up to 2 days". No cause given. | loss | STRONGLY CORROBORATED | AM-014 |
| 2020-09-30 | Trading disabled for a "serious trading bug which was causing items to disappear". | loss | STRONGLY CORROBORATED | AM-016 |
| 2020-10-20 | Game made private over "a critical bug with Roblox's Datastore Servers". Inventories to be restored. | loss / G | STRONGLY CORROBORATED | AM-018 |
| 2020-11-05 | Trade License quiz, 30-day trade history, scam reporting, two-step trade with fairness warning. | control | STRONGLY CORROBORATED | AM-019 |
| **2022-09-02** | **Dupe acknowledged:** "remove duplicate items from clearly exploiting users", sparing accidental finders and downstream traders. | **D** | STRONGLY CORROBORATED | AM-024 |
| 2022-10-24 | Support stopped accepting hacked-account tickets "for the foreseeable future". | G | STRONGLY CORROBORATED | AM-026 |
| 2025-04-11 | Ban wave for event-currency farming (Sakura Swoop) with tiered bans and caps. | C (farming) | STRONGLY CORROBORATED | AM-034 |
| 2025-05-16 | New accounts need 2 h playtime before trading. | control | STRONGLY CORROBORATED | AM-035 |
| 2026-07-31 | Cross-server Trading Hub. Listed pets are locked; the imbalance check is "not a true value system". | control | STRONGLY CORROBORATED | AM-037 |
| ~2025 | Help center says "pet duplication is not possible". This **contradicts** AM-024. It also mentions automatic trade blocks on suspected duplicates. | H vs D | contradiction | AM-024 vs AM-029 |

**What is *not* established for Adopt Me!:**
- root causes of any incident;
- the date trading launched in 2019;
- any 2023–2024 incident;
- any working "spawner" that creates tradable pets (UNVERIFIED/DEBUNKED class E/H);
- any insider or backdoor activity.

### 1b. General Roblox risks. These are evidence about classes of problem, not about Adopt Me!

- **Platform docs explicitly describe our core failure modes** (docs-verified):
  - `ProcessReceipt` may run on two servers at once and can be redelivered after `PurchaseGranted` (OFF-012).
  - `UpdateAsync` is atomic per key only; there is no cross-key transaction (OFF-022, OFF-023, OFF-027).
  - Roblox's own security page describes the trade-then-leave-then-failed-save dupe and a NaN bypass in a trade handler (OFF-005, OFF-004).
- **Other games:**
  - Grow a Garden disabled gifting over a lag-related dupe (Jul 2025, RBX).
  - MM2 and Pet Simulator X wiped duplicates (secondary sources only).
  - 2023 free UGC limiteds were claimable without eligibility until a server check was added.
- **People and credentials:**
  - Roblox support panel abused via bribery and phishing (May 2020, RBX-001).
  - Phished employee leading to a document leak (Jul 2022).
  - Account theft at scale: 610k+ accounts, arrests in Apr 2026 (RBX-015).
  - Developer and owner accounts hijacked via fake job offers (2026).
- **Supply chain:** fake `noblox.js` npm packages (2021, 2023, 2023–24). Roblox's docs say Toolbox moderation is "not guaranteed to remove all" malicious scripts (OFF-035, RBX-016..018, RBX-021).
- **New in 2026** (docs-verified):
  - `BindReceiptHandler` (OFF-015).
  - In-game player-to-player Robux transfers, `PromptRobuxTransferAsync` (OFF-016, OFF-017). This creates an official route for selling pets for Robux.
  - The Transaction Refunded webhook (OFF-020). Developer-product refunds are **not** clawed back by Roblox.
  - `IsPaidItemTradingAllowed`, which requires per-player gating of paid-item trades (OFF-036..038).

---

## 2. Top 10 realistic risks to OUR game

Ranked by risk to our game, not by how sensational they are. Full matrix: `03_ATTACK_SURFACE_MATRIX.md`.

| # | Risk | Outcome | Why it is realistic | Fix | Priority |
|---|---|---|---|---|---|
| 1 | **Saving after a failed or stale load; session-lock gaps across server hops/teleports** → dupes or wipes | D / loss | Documented by Roblox; matches Adopt Me! 2020 loss events | Session-locked profiles, Errored state never saves (05 §A.7, BL-01..04) | P0 |
| 2 | **Non-atomic two-player trade commit** | D / loss | No cross-key transactions; 2020 "items disappearing" | Presumed-abort saga with coordinator key, `recover()` that tells a read failure apart from an absent record (05 §6, §A.9; BL-08..10) | P0 |
| 3 | **Duplicate or concurrent purchase receipts** | D | Documented: two servers, redelivery after Granted | PurchaseId dedup in the same `UpdateAsync` as the grant (05 §5; BL-05) | P0 |
| 4 | **Remote handlers trusting client values** (NaN, negative, ids, prices) | C | Roblox's own NaN-trade example | Positive validation and token buckets on every remote (05 §13; BL-07) | P0 |
| 5 | **Privileged paths**: owner, collaborator, Toolbox, plugin, Open Cloud key, support tooling | C / G | 2020 support panel; 2026 owner hijacks; supply-chain packages | Group-owner 2SV account, CI-only publish, sandboxed third-party content, scoped keys, dual-approval restores (BL-14..16, BL-20) | P0 |
| 6 | **Refunds and chargebacks on pets already traded on** | G | Roblox doesn't claw back developer products; 2022 10-K chargebacks ≈3.16% of bookings | Webhook → inbox → taint-and-revoke along the ledger (05 §A.1; BL-13) | P0 |
| 7 | **Paid-item trading policy** (`IsPaidItemTradingAllowed`) and the Robux-transfer route for selling pets | compliance / G | Policy requirement; new 2026 API | `paid` flag, fail-closed TradeGate, don't link transfers to pets (05 §A.3; BL-12) | P0 |
| 8 | **Account takeover plus one-sided rollbacks** turning support into a dupe channel | G / D | 610k-account case; user reports of one-sided reversal abuse | Two-sided reversal from the ledger, one restore per period, cooldowns (05 §A.5; BL-18/19) | P1 |
| 9 | **Bots, alts and event-currency farming** | C (soft) | Adopt Me! 2025 ban wave | Server-side caps, account-age/playtime gates, anomaly alerts (05 §A, BL) | P1 |
| 10 | **Scams and social engineering** (switch at the last second, fake proof, phishing) | G / H | Trade License history; Talos double-trade research | Change-reset, confirm delay, imbalance warning, trade history, reporting (05 §6.1) | P1 |

Not top-10, but often over-feared: **imported Blender meshes and client "spawners"**. They cannot create inventory in a game that keeps its pet catalog on the server (`04`).

---

## 3. Highest-ROI defenses (cheap and high impact)

1. **PurchaseId dedup inside the grant write.** Hours of work; closes receipt replay.
2. **Session lock plus "never save an errored profile".** Closes the most common dupe and wipe class.
3. **Single `PetMint.mint` path** with a closed source enum, GUID ids and a CI lint against direct inventory writes. This makes every pet traceable, which is the safety invariant.
4. **Positive validation and rate limits on every remote.**
5. **Trading kill switch** that works without a deploy (05 §A.6). It buys time during any incident, as Adopt Me! did in 2020.
6. **Append-only ledger plus a daily mint-vs-receipt reconciliation.** This turns silent dupes into alerts and makes cleanups targeted, like the 2022 Adopt Me! response.

**Safety invariant:** no valid persistent pet-inventory change without a uniquely traceable server-authorized source and a reconciled ownership transition. Because Roblox has no multi-key transactions, trades, gifts, refunds and restores keep this invariant through **application-level compensation** (05 §6.2), not atomicity.

---

## 4. P0 launch-blocking checklist (condensed)

Full list: `05_SECURE_ARCHITECTURE.md` §14 and §A.11.

- [ ] Session-locked profiles; errored or unloaded profiles never save and cannot purchase.
- [ ] Receipt handler bound once; PurchaseId dedup persisted with the grant; `PurchaseGranted` returned only after a successful save.
- [ ] Single mint path; GUID pet ids; idempotent `mintRefs`; CI lint.
- [ ] Trade state machine with change-reset, confirm delay and `offerVersion`; presumed-abort commit; `recover()` on load that treats a read error differently from an absent record.
- [ ] Every remote has argument-count, type, range, NaN/inf and length validation plus a token bucket. No client→server grant, currency or inventory setters. No admin remotes in prod.
- [ ] Outbox → ledger idempotent; daily export to WORM storage; mint-vs-receipt and duplicate-id reconciliation live.
- [ ] `BindToClose` parallel save within 30 s, load-tested.
- [ ] Separate staging and prod universes; CI-only prod publish; scoped, expiring Open Cloud keys; no runtime `LoadAsset` of non-constant ids; third-party models sandboxed.
- [ ] Refund webhook → clawback (including pets already traded on); `paid` flag plus a fail-closed `IsPaidItemTradingAllowed` gate.
- [ ] Trading/gifting kill switch; support restores through dual approval and the single mint path, revoking the original id.
- [ ] `06_TEST_PLAN.md` passes in staging. This is **necessary, not sufficient**. A passing harness does not make production secure.

**MVP order:**
1. Data foundation.
2. Money path, with no trading yet.
3. Remote hardening.
4. Same-server trading.
5. Observability.
6. Support tooling.
7. Cross-server trading, only if needed.

See 05 §15 and `07_BACKLOG.csv`.

---

## 5. Confidence and coverage limits

- **Network:** the environment's egress policy blocked create.roblox.com, devforum.roblox.com, the help centres, web.archive.org, x.com, playadopt.me and press sites. Roblox facts were verified verbatim from the official docs source repo (`Roblox/creator-docs` @ `70a0110`, 2026-10-17). **Everything else is search-snippet-only.**
- **Searches not run:** the shared search budget ran out mid-research, so some queries never ran (listed in `08`).
- **Code:** none of the Luau has been executed (no toolchain in this environment). It is reference code.
- **Revenue:** no audited Adopt Me! revenue figures exist; estimates vary roughly 10×.
