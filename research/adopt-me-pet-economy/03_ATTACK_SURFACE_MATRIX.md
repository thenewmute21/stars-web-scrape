# 03 — Attack Surface Matrix (red team / blue team)

Execution date: 2026-10-19. Scope: **our own original pet-collection / trading game**. Adopt Me! (Uplift Games) and other
Roblox games appear only as evidence. This is an architecture-level document: it names trust boundaries, failure modes,
detectable signals and fixes. It contains no operational steps against any live game.

Sources: `01_EVIDENCE_LEDGER.csv` (confidence values are the **post-postmortem** values; 40 snippet-only rows were downgraded
from CONFIRMED to STRONGLY CORROBORATED, including the 2022-09-02 Adopt Me! dupe, AM-024),
`05_SECURE_ARCHITECTURE.md` (cited as "05 §n"; "05 §A.n" is the post-research addendum), `06_TEST_PLAN.md` (test IDs T01–T37,
S1–S5; T26–T37 are added in 06 §8). No new web research was done for this file.

---

## 0. Hero summary

**Bottom line.** Every confirmed or strongly corroborated way that pets were minted or duplicated, in Adopt Me! or in
comparable Roblox games, went through **our own server code, our own persistence, or our own people and credentials**. None
went through the Roblox asset system or client visuals. The highest risks for our game are:

1. **Persistence faults that become dupes or wipes.** These are failed-load-then-save, stale sessions across server hops, and
   non-atomic two-key trades. Roblox documents all three (OFF-005, OFF-023, OFF-027). They match the only first-party Adopt Me!
   loss and dupe events we found (AM-014, AM-016, AM-018, AM-024).
2. **Money-path idempotency and reversals.** Receipts can run on two servers and can be redelivered after `PurchaseGranted`
   (OFF-011, OFF-012). The new **Transaction Refunded** webhook (OFF-020) makes developer-product refunds visible, but
   **Roblox claws back nothing for developer products**. Pets bought and already traded on need our own taint-and-revoke
   policy. 05 had no such policy; the addendum §A.1 adds one.
3. **Platform policy we must enforce per player.** `IsPaidItemTradingAllowed` requires gating trades by item provenance
   (paid vs earned) (OFF-036, OFF-038). 05 tracked only per-kind `tradeable`. The addendum §A.3 adds the paid flag.
4. **Privileged paths: owners, collaborators, Toolbox/plugins, Open Cloud keys, support tooling.** A hijacked owner account
   or a backdoored model gives arbitrary server writes (RBX-019, RBX-021, OFF-031, OFF-035). Roblox's own support panel was
   abused in 2020 (RBX-001).
5. **Account takeover, plus rollbacks that reverse only one side.** These are the main G-outcome volume (RBX-015 >610k
   accounts; ECO-028/RBX-039 one-sided rollback abuse). Without a two-sided reversal policy, our support desk becomes a
   duplication channel (05 §A.5).

**Ranking method.** Likelihood (H/M/L) is the **inherent** chance that this channel is attempted against, or fails in, our
game in year one, *before* the 05 mitigations. That is what the mitigations must beat. Impact is the economy, safety or
compliance harm if it succeeds. Priority is the urgency of the fix (P0 = launch-blocking). Rows are sorted by priority, then
by likelihood × impact.

**Weaknesses found in our own design (05).** These are fixed in 05 §A:

- No refund clawback.
- No paid-provenance flag.
- No trading or gifting kill switch.
- No two-sided rollback rule.
- No gifting or crafting path. The `Source` enum has no `Craft`.
- The revocation lookup in 05 §8 is not specified and would not scale.
- `TradeService.recover()` treats a *missing* coordinator record and a *failed read* the same way. If an implementation
  swallows read errors as `nil`, it would compensate a trade that was actually committed, which is a dupe.
- No event-currency caps.

---

## 1. Outcome and likelihood legend

Outcomes (from the brief): **A** legit persistent pet · **B** legit without direct Robux · **C** unauthorized server-issued
pet or balance · **D** duplication or replayed grant · **E** client-only visual or spoof · **F** external asset, not an
entitlement · **G** compromised, fraudulent, reversed or support-issued · **H** unverified or fabricated. "Loss" marks data
loss, which has no outcome letter.

Category tags in the Channel column: [C1] legit free/earned · [C2] trading, gifting, alts, RMT · [C3] trade state machine
races · [C4] DataStore persistence · [C5] shop, receipt, refund, Robux transfer, paid-trading policy · [C6] remote
validation · [C7] asset cloning and import (E/F) · [C8] creator, admin and support powers, supply chain · [C9] bots and
farming · [C10] social engineering, ATO, rollback abuse · [C11] fake spawners · [C12] economy design · [C13] platform and ops
· [C14] MemoryStore / MessagingService.

---

## 2. Matrix

| ID | Channel | Intended? | Outcome | Preconditions | Server-side trust boundary | Failure mode | Detectable signal | Lik. | Impact | Fix (05 §) | Test (06) | Evidence | Pri |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ASM-01 | [C4] Failed load then save (default/empty profile overwrites real data) | No | Loss; D if it is combined with a later restore | DataStore read error or outage during join; save path doesn't check the load result | `UpdateAsync` load result → session `errored` flag | Server treats a failed read as a new player, then autosave, PlayerRemoving or BindToClose writes the defaults over real data | Sharp drop in pets/coins on save vs loaded snapshot; spike of "new profiles" for old accounts; DataStore error rate | M | Critical | §1 F7, §14, §A.7 (shrink guard, errored = no save, no purchase, no trade) | T14, **T26** | OFF-027, RBX-048, RBX-009, AM-014, AM-018, AM-051 | P0 |
| ASM-02 | [C4] Missing or broken session lock: server hop, stale load, lock steal | No | D | Player is loaded on two servers (fast rejoin or teleport) and the old server still saves | LockId in key metadata written in the same `UpdateAsync` as the load | The old server's stale save overwrites a newer state, or both servers act on one profile, so a traded pet comes back | `lock_lost` / `lock_stolen` logs; the same pet Owned in two profiles; version jumps | M | Critical | §13.4, §14 | T06, T19, S2 | OFF-027, RBX-046, OFF-005, AM-028 | P0 |
| ASM-03 | [C3/C4] Non-atomic two-party commit (trade, then leave, then one save fails) | No | D or Loss | No cross-key transaction (two profile keys) | Trades_v1 coordinator record plus per-profile idempotent prepare, finalize and compensate | One side persists and the other doesn't, so the item exists twice or neither side has it | Stuck `Committing` records; INV-2/INV-5 violations; ledger TransferOut without TransferIn | M | Critical | §6.2, §13.7 | T02a–T02f, T23–T25 | OFF-005, OFF-023, RBX-047, RBX-031, AM-016, AM-028 | P0 |
| ASM-04 | [C5] Duplicate or concurrent receipt (two servers; Granted but not recorded; rejoin redelivery) | No | D | Handler grants without PurchaseId dedup in the same write | `PurchaseId` stored in the profile in the same `UpdateAsync` as the grant; `PurchaseGranted` only after the save succeeds | A redelivered receipt mints again, or a second server grants in parallel | Mint(Purchase) count > distinct PurchaseIds; reconciliation vs sales | M | Critical | §4, §13.6, §14 | T03, T04, T05, S1, S4 | OFF-011, OFF-012, OFF-013, OFF-028, RBX-026, RBX-038 | P0 |
| ASM-05 | [C6] Remote argument abuse (NaN/inf, type confusion, table-for-Instance, holes, oversize strings) | No | C | Any remote that does arithmetic or lookups on client input | Remote gateway positive validation plus token bucket (§13.2–13.3) | NaN passes `<`/`>` range checks and poisons balances or trade offers; tables pass as items | `validation_fail` per remote; non-finite values in persisted profiles (INV-6) | H | High | §13.2, §13.3, §14 | T07, T08, T16 | OFF-003, OFF-004, OFF-006, RBX-052 | P0 |
| ASM-06 | [C5/C6] Client-trusted grant signal (purchase-finished event, client "claim" remote, double-click claim) | No | C / D | The server grants on a client event, or a claim isn't idempotent | Grants only from receipts, server timers or server-validated state; idempotent `mintRefs` | Free items, or repeated claims of a one-time reward | Claims per user > 1 per claim id; claim bursts | H | High | §2, §5, §13.5, §14 | T11, T15, T21 | OFF-019, RBX-036, AM-024 | P0 |
| ASM-07 | [C8] Owner or collaborator account takeover (malware-delivering fake job offers; group transfer) | No | C (arbitrary mint) | Attacker controls an account with Edit or publish rights, or the group owner | Publish rights; CI-only prod publish; separate prod-publish role | Malicious server code or a direct DataStore write mints at will; the game is hijacked | Place version not matching a CI-signed release; out-of-hours publish; mint spike without receipts | M | Critical | §9, §10, §A.10 | **T37** (release-provenance check), S4 | RBX-019, RBX-020, OFF-031, AM-017 (rumour only) | P0 |
| ASM-08 | [C8] Backdoored Toolbox models or plugins (`require(assetId)`, loadstring) | No | C | A developer inserts an unvetted model or plugin | Script Capabilities sandbox; vetted allowlist; CI lint | A hidden server script gives the attacker remote execution, and with it DataStore writes | CI finds `require(<number>)`, `loadstring`, `getfenv`; unexpected Scripts in Workspace | M | Critical | §10, F12 | T11 (lint), **T37** | OFF-035, RBX-021, RBX-022, RBX-023, IMP-025 | P0 |
| ASM-09 | [C5] Developer-product refund with no clawback (incl. pets already traded on) | No | G | A refund via Roblox CS; the game ignores the Transaction Refunded webhook | Off-platform webhook receiver → inbox → server-side revoke via single path | The refunded value persists and circulates; laundering through innocent recipients | Refund events with no matching Revoke in the ledger; refunded PurchaseIds whose pets have Transfer entries | M | High | **§A.1** | **T27, T28** | OFF-020, OFF-021, ECO-024, ECO-026, ECO-034 | P0 |
| ASM-10 | [C5/C12] Paid-item trading where `IsPaidItemTradingAllowed` is false | No (compliance) | n/a (policy breach) | A player under that policy trades a Robux-derived pet or one made from paid currency | PolicyService per player (fail closed) plus a `paid` provenance flag on the pet | A platform policy violation; region shutdown precedent (NL/BE loot-box rules) | Committed trades with `paid=true` where either party's policy was false (INV-8) | H | High | **§A.3** | **T29** | OFF-036, OFF-037, OFF-038, AM-025, AM-015 | P0 |
| ASM-11 | [C13] No trading/gifting kill switch | n/a (ops gap) | Amplifies D | A live dupe is found; we have to ship a new build to stop it | Durable config key read by every server; dual-approved flip | Hours of dupe circulation while a patch is built; precedents disabled trading first | Time-to-freeze after an alert | M | High | **§A.6** | **T32** | AM-016, AM-018, RBX-025, RBX-031, RBX-033, RBX-034 | P0 |
| ASM-12 | [C4] Our reference `recover()` conflating read failure with a missing record | No (our bug) | D | An implementation wraps `GetAsync` in pcall and returns nil on error | Coordinator record read in `TradeService.recover` | A committed trade is compensated on one side while the other side finalizes, so the pet exists in both profiles | INV-2 violations after DataStore incidents | M | Critical | **§A.9** (corrects §13.7) | **T36** | OFF-023, OFF-025, RBX-047 | P0 |
| ASM-13 | [C13] Reconciliation or monitoring gap (dupes found by players first) | n/a | Amplifies C/D | No mint-vs-receipt or duplicate-id jobs on day 1 | Off-platform WORM export plus nightly reconciliation | The scale of a dupe is unknown, so cleanup is broad or impossible | Reconciliation job freshness; alert latency | M | High | §7, §11 | S4 | AM-024, AM-030, RBX-027, RBX-028, RBX-050 | P0 |
| ASM-14 | [C3] Trade window races: last-second swap, stale confirm, forged UI state, double accept | No | G (scam) / D | Server accepts a confirm without an offer version, or doesn't reset on change | `offerVersion`, change-reset, confirm delay, participant check | The victim confirms a different offer than the one shown | `trade_reset` right before confirm; stale-confirm logs | H | Medium | §6.1, §13.7 | T10, T17, T21, T22 | AM-044, ECO-008, ECO-015, ECO-020, RBX-034, AM-040 | P0 |
| ASM-15 | [C3] Same pet offered in parallel trades | No | D | Ownership checked only at offer time | `isTradeable` re-checked at prepare; EscrowOut state | Both trades commit the same pet | INV-2; `trade_abort NotTradeable` | M | High | §6, §13.7 | T01 | OFF-005, RBX-025 | P0 |
| ASM-16 | [C4] Shutdown save loss (BindToClose 30 s) | No | Loss / D | Sequential saves; slow DataStore | BindToClose parallel saves; lock left to expire | Recent trades or purchases lost; with a weak lock, a dupe | `shutdown_save fail` count | M | High | §14, F8 | T18, S3 | RBX-049, OFF-027 | P0 |
| ASM-17 | [C10] Account takeover / "beaming" (session cookie theft, fake executors, infostealers) | No | G | A victim's Roblox session is stolen (outside our trust boundary) | We see only a legitimate session; controls are holds and anomaly review | The inventory is stripped by trades to a mule account and resold for cash | Burst of outgoing high-value trades from an old account to a young one; star topology | H | High | §11, §12, §A.5 | **T31** | AM-042, RBX-003, RBX-014, RBX-015, ECO-021, ECO-023 | P1 |
| ASM-18 | [C10] One-sided rollback / hacked-restore abuse | No | G / D | Restore reverses only the claimant's side, or doesn't revoke the original | Support tool: two-person approval, ledger-computed reversal set | A fair-trade partner loses their item, or a "lost" pet is restored while the original still circulates | Restores per account > 1; restore after a fair trade; restored-and-original both Owned | M | High | §8, **§A.5** | T13, **T31** | ECO-028, RBX-039, ECO-029, ECO-011, AM-021, AM-022, AM-026 | P1 |
| ASM-19 | [C5/C10] Stolen-card purchase or chargeback, then immediate trade (laundering) | No | G | Paid pets tradeable immediately after purchase | Tradability hold on paid-provenance items | Fraud-funded pets are converted to clean earned pets or cash | Paid pets traded within hours of purchase; refund rate per cohort | M | High | §12 (hold), **§A.1**, **§A.3** | T05, **T27** | ECO-024, ECO-033, ECO-004, ECO-010, ECO-026 | P1 |
| ASM-20 | [C5/C2] `PromptRobuxTransferAsync` as an in-game RMT or trust-trade rail | Platform-intended; coupling is our choice | G (if coupled badly) / B | We implement transfers; players settle pet deals with Robux | Default: no coupling to items. If coupled: escrow keyed by transfer receipt, paid-trading policy on both sides | "Pay first" scams on an official rail; pet-for-Robux markets that breach paid-trading policy; game takes 10% | Transfers between pairs who also trade lopsided; disputes citing transfers | M | Medium | **§A.2** | **T33** | OFF-015, OFF-016, OFF-017, OFF-038 | P1 |
| ASM-21 | [C9] Event-currency or minigame farming (Sakura Swoop class) | No (abuse of intended path) | C (inflated balance) / B | Client-reported scores, no caps, tradeable event outputs | Server-computed rewards, per-day caps, plausibility bounds | Event pets minted far above the design rate | Currency per hour far above the server-derived max; distribution tails | H | Medium | §12, **§A.8** | T15, **T35** | AM-034, AM-007, ECO-031 | P1 |
| ASM-22 | [C9] AFK or bot farming of earn paths (daily, login, care tasks) | No (ToS) | B (illegitimately earned) | Unbounded faucets, no engagement signals | Server faucets with diminishing returns; caps | Inflation; bot farms feed RMT | Earn rate per account vs human ceiling; identical session patterns | H | Medium | §11, §12, **§A.8** | T16, **T35** | AM-005, ECO-006, ECO-007, ECO-031 | P1 |
| ASM-23 | [C2/C9] Alt farms funnelling rewards to a main account | No | B / G | Free accounts; tradeable starter or daily rewards | Account-age and playtime trade gate; graph detection | Unlimited "free" supply via alts | Many young accounts → one receiver | H | Medium | §11, §12 | **T30** (gate), T16 | AM-035, ECO-030, RBX-025 | P1 |
| ASM-24 | [C8] Support or admin power abuse (insider, phished agent, over-broad tooling) | No | G / C | Support can write inventories directly | Dual approval; restore inbox; capped volume; no in-game admin writes | Silent minting or transfers through support tooling | Restorations per agent spike; restores without a ticket | L | High | §8, §9, §11 | T12, T13 | RBX-001, RBX-002, RBX-005, AM-048 (no Uplift evidence) | P1 |
| ASM-25 | [C8] Open Cloud API key leak (DataStore write scope) | No | C | A key with write scope leaks (repo, laptop, CI logs) | Scoped keys (§9 K1–K4), IP allowlist, expiry, Secrets Store | Out-of-band writes to profiles; shared budget starved | Writes from unexpected IPs; budget drops | L | Critical | §9, F13 | **T37** (key audit) | OFF-031, IMP-027, RBX-024 (no incident found) | P1 |
| ASM-26 | [C8] npm or tooling supply chain (noblox.js typosquats, postinstall hooks) | No | G → C (via stolen creds/keys) | Our Node/Python tooling installs unpinned packages | Lockfiles, allowlist, no secrets on dev machines | Developer credentials or Open Cloud keys stolen | New dependency diffs; postinstall scripts in lockfile | M | High | §10, **§A.10** | **T37** | RBX-016, RBX-017, RBX-018, RBX-019 | P1 |
| ASM-27 | [C2] Gifting path (one-sided transfer) built outside the trade saga | Intended feature | D / G | Gift implemented as "delete here, add there" | The same §6.2 saga with an empty counter-offer | A lag- or race-based gift dupe | INV-2/INV-5 on gift ops | M | High | **§A.8** (gift = saga) | **T34** | RBX-031, AM-015 | P1 |
| ASM-28 | [C1/C4] Crafting (consume N, mint 1) not atomic; no `Craft` source | Intended feature | D | Inputs consumed and output minted in different writes | Single profile `UpdateAsync`; `Source=Craft`, ref = hash of consumed ids | Output minted and inputs not consumed (or the reverse) | Craft outputs without matching consumes in the ledger | M | High | §5, **§A.8** | **T34** | AM-003 | P1 |
| ASM-29 | [C4] Teleport mid-trade or mid-save | No | D / Loss | Teleport before save and release | Block gameplay teleport in Locked+; save and release before teleport; `recover()` on load | The destination loads a stale profile | `trade_recover` after teleport | M | High | §6.2, F16 | T23 | RBX-049, OFF-027 | P1 |
| ASM-30 | [C13/C4] DataStore budget or throttle exhaustion (incl. Open Cloud sharing the budget) | No | Loss / delayed grants | Ledger flush, analytics or exports compete with saves | Budget-aware batching; throttled exporter | Saves dropped (queue > 30), receipts stuck | `NotProcessedYet` share; 301–306 errors | M | Medium | §7, §11, F5 | T05, S5 | OFF-024 | P1 |
| ASM-31 | [C4] Reordered or stale autosave writes | No | Loss / D | Naive retries | Per-key FIFO queue (DataStoreWrapper pattern); lock check | An older snapshot overwrites a newer one | Version regressions | M | High | §13.4 note, §14 | T06 | OFF-027 | P1 |
| ASM-32 | [C4/C13] Schema migration or rollback deploy truncating data | No | Loss | An old build loads a newer schema and saves | `schema > CURRENT` → errored, no save | Fields silently dropped | `schema_refuse` logs | M | High | §3, §14 | T14 | OFF-027 | P1 |
| ASM-33 | [C6] ProximityPrompt, ClickDetector or Touched reward claims (distance bypass, network ownership) | No | C (currency) | Rewards on detector events without server checks | Server distance/state checks; server-owned parts; token bucket | Remote farming of world rewards | Claims from implausible positions or rates | H | Medium | §13.3, **§A.8** | T16, **T35** | OFF-007, OFF-008, OFF-006 | P1 |
| ASM-34 | [C5/C12] Egg hatch: client-influenced RNG or undisclosed paid odds | Intended feature (paid random item) | C / policy breach | RNG or odds on the client; no odds UI; `ArePaidRandomItemsRestricted` ignored | Server-side RNG; odds table in the server catalog; per-player policy | Biased hatches; compliance breach | Hatch distribution vs configured odds (chi-square) | M | High | §5, **§A.3** | **T29** | OFF-037, OFF-036, AM-004, AM-025 | P1 |
| ASM-35 | [C7] Runtime `LoadAsset` of a client-supplied id | No | C / F | Code loads arbitrary ids | Catalog allowlist; CI lint; `AllowInsertFreeAssets` off | Attacker content loaded server-side; a lookalike mapped to a kind | CI lint failure; unknown kind requests | L | High | §10, F12 | T11 | OFF-032, OFF-033, IMP-006, IMP-007 | P1 |
| ASM-36 | [C7/C13] Staging or subplace leak (debug pets, shared DataStores) | No | E / H; C if stores are shared | Subplaces joinable; staging shares prod stores | "Secure within universe only"; separate universes and store names; GameId assert | Unreleased pets data-mined; debug grants hit prod | Joins to non-start places via client teleport | M | Medium | §10, 06 §1.1 | **T37** | OFF-010, IMP-023 | P1 |
| ASM-37 | [C13] Platform outage or DataStore incident | No (external) | Loss | Roblox backend degraded | Fail closed: errored sessions, kill switch, purchases NotProcessedYet | Mass resets if we save defaults; trades half-done | DataStore error rate; spike in errored sessions | M | High | §14, **§A.6**, **§A.7** | T25, **T26**, **T32** | AM-018, RBX-008, AM-023, RBX-009 | P1 |
| ASM-38 | [C8] Revocation lookup not specified (05 §8 "sees revocation on load") | No (our design gap) | G / D | Revoked pet held by another user | Holder-directed inbox computed from ledger; nightly scan | The revoked original keeps circulating | Revoked id Owned anywhere (INV-9) | M | Medium | **§A.5** (corrects §8) | **T31** | RBX-050, RBX-027 | P1 |
| ASM-39 | [C10/C13] Remediation overreach (cleanup hits innocent downstream holders) | n/a (policy) | G | Blanket deletion of duplicated ids | Ledger-scoped cleanup; exploiter vs recipient classification; review | Innocent traders lose items, so trust collapses | Appeals volume after cleanup | M | Medium | §8, **§A.1**, **§A.5** | **T27**, **T31** | AM-024, RBX-027, RBX-028 | P1 |
| ASM-40 | [C2] Off-platform RMT and cross-trading (marketplaces, Discord) | No (ToS) | G / B | Tradeable high-value pets | We can't see the payment; only trade-graph signals | Economy priced in USD; scams; child-safety exposure | Lopsided trades between unrelated accounts; trade cycles | H | Medium | §11, §12 | **T30** | AM-012, AM-032, ECO-022, ECO-032, RBX-032, RBX-043 | P2 |
| ASM-41 | [C10] Social engineering: trust trades, fake middleman, staff impersonation | No | G | Deals made outside the trade window | Atomic in-game escrow makes middlemen unnecessary; unforgeable staff badge | Victims hand items over outside protections | Reports; "middleman" chat patterns (no chat logging by default) | H | Medium | §6, §12 | T10, T17 | AM-044, ECO-018, ECO-019, ECO-020 | P2 |
| ASM-42 | [C10] Phishing, "free pet generators", lookalike domains | No | G | Off-platform lures | None in game (outside the boundary); education and reporting | Credential and cookie theft → ASM-17 | Spikes in ATO reports | H | Medium | §12 (education), §A.5 | n/a (ops) | AM-041, AM-043, IMP-019, RBX-014 | P2 |
| ASM-43 | [C11] "Pet spawner" or client visual shown as real (incl. in the trade window) | No | E (claims of "tradable": H) | Exploit client renders local models | Trade window contents come **only** from server state; inspect shows server provenance | Victims believe a visual pet is real and pay first | Reports citing pets that the server shows as not owned | H | Low | §2, §6.1 | T09, T11 | AM-039, AM-040, OFF-002, IMP-009 | P2 |
| ASM-44 | [C14] Cross-server trade hub or listings on MemoryStore | Intended (if built) | D / Loss (if MemoryStore is authoritative) | Listing state or locks only in MemoryStore | MemoryStore = discovery only; durable escrow in profile and Trades_v1 | Evicted or expired entries unlock listed pets twice | Listings without a durable escrow marker | M | High | §2, §15 step 7 | **T32** (freeze), NEW: hub fault suite before building | OFF-029, AM-037 | P2 |
| ASM-45 | [C14] MessagingService as the commit or grant carrier | No | Loss / D | Cross-server gift or trade relies on delivery | Messages are nudges only; durable record is truth | Dropped message, so a half-applied transfer | Unacked nudges; stuck records | L | High | §2, F10 | T25 | OFF-030 | P2 |
| ASM-46 | [C12/C10] No age or verification gates on high-risk features | Design choice | G (safety) | Young or unverified accounts in high-value trading or Robux transfers | `IsVerified()`, `AgeChecked`, account tiers (server-read) as configurable gates | Child-safety and fraud exposure; regulatory risk | Trades by Kids/Select tiers (if exposed) | M | Medium | **§A.4** | **T30** | OFF-039, OFF-040, AM-038, RBX-045, ECO-036 | P2 |
| ASM-47 | [C3] Double-trade balance drain (currency in trades) | No | G | Two crossing trades; balance checked only at offer | Currency escrow at prepare; re-validate at commit; one pending trade per user | The favourable trade fails and the bad one completes | Paired trades aborted for insufficient funds | L | Medium | §6.2 (escrowCoins) | T01 (+ currency variant in **T34**) | ECO-020 | P2 |
| ASM-48 | [C7] Mapping catalog/UGC ownership to in-game pets | Only if we build it | C | `PlayerOwnsAssetAsync` with an unpinned id list | Server-only check; allowlisted creator ids; grant ledger | Anyone who publishes or acquires a matching asset mints | Grants with source=Catalog from non-allowlisted ids | L | High | §10 | T11 | IMP-013, IMP-014 | P2 |
| ASM-49 | [C1/C12] Promo-code or promotion stacking | Intended (bounded) | C / B | Multiple promos claimable | Server rule, one per type; idempotent `Event:promoId:userId` | Stacked free mints | Claims per user per promo > 1 | M | Low | §12 | T15 | ECO-031 | P2 |
| ASM-50 | [C4] Clock skew between servers (lock TTL, trade deadlines) | No | D (edge) | `os.time` drift between servers | Generous TTL vs autosave interval; CAS decides, not clocks | Premature lock steal or abort while the holder is still writing | `lock_stolen` while the holder was healthy | L | Medium | §1 gaps, §13.4 | T19 (skew variant via `skewWall`) | OFF-027 | P2 |
| ASM-51 | [C12] Third-party value-list manipulation / hype pumping | Emergent | B (economically harmful) | Values set off-platform | None (outside the boundary); first-party supply stats | Kids pushed into bad trades by manipulated lists | Sudden trade-ratio shifts for one kind | M | Low | §12 (warn, don't block) | n/a | ECO-016, AM-049, AM-027 | P3 |
| ASM-52 | [C7] External mesh / Blender upload claimed as "imported pet" | No | F (H if claimed real) | Attacker uploads a lookalike asset | Inventory = server records keyed by catalog kind; no asset-id entitlement | None for inventory; scam narrative only | n/a | H (claims) | Low | §10 | T11 | IMP-001, IMP-003, IMP-010, IMP-011, IMP-013, OFF-032, OFF-034 | P3 |
| ASM-53 | [C7/C11] Decompiled client, saveinstance lookalike games, fake screenshots | No | E / H | Replicated UI and models | Nothing server-only replicates | Convincing fake "proof" and phishing clones | Lookalike games reported | H | Low | §10, F-boundary | n/a | IMP-021, IMP-022, IMP-020, IMP-018, IMP-029 | P3 |
| ASM-54 | [C1] Legit free and earned paths (care tasks, Bucks eggs, events, crafting) | Yes | A / B | — | Server faucets and sinks | Over-generous faucets cause inflation | Faucet/sink telemetry (EVE-style) | n/a | Medium (economy) | §11, §12 | T15 | AM-004, AM-005, AM-007, AM-003, ECO-012 | P3 |
| ASM-55 | [C12] Robux → pet → trade arbitrage | Yes | A (buyer) / B (receiver) | Paid pets tradeable | Policy gate (ASM-10) and hold (ASM-19) only | None (intended) | n/a | n/a | n/a | §A.3 | T29 | AM-006, ECO-016 | P3 |

**How to read "NEW".** IDs T26–T37 are new tests added in 06 §8 by this pass. "n/a (ops)" means the control is operational
(education, reporting, platform) and has no automated test in our harness.

---

## 3. Red-team notes on our own design (05), with corrections now in 05 §A

| # | Finding | Why it matters | Fixed in |
|---|---|---|---|
| R1 | `TradeService.recover` maps `rec == nil` to Aborted. If `readRecord` hides errors as nil, a Committed trade gets compensated on this side. | This is a dupe path during exactly the DataStore incidents in ASM-37. | §A.9, T36 |
| R2 | §8 says a holder "sees the revocation on load", but no lookup is specified. Per-pet `GetAsync` on load would exhaust budget (F5) for large inventories. | Revoked originals keep circulating. | §A.5, T31 |
| R3 | The `Source` enum has no `Craft` or `Gift` concept, and gifting isn't designed. | Teams build gifts and crafting outside the saga. That is the class behind the Grow a Garden gifting dupe (RBX-031). | §A.8, T34 |
| R4 | `holdUntilPersisted` is the only tradability hold. Paid pets become tradeable as soon as they are saved. | Refunds and stolen-card purchases can be laundered immediately (ECO-004, ECO-024). | §A.1, §A.3, T27, T29 |
| R5 | There is a single `coins` balance. Robux-bought and earned currency are fungible. | Paid-item trading policy covers indirect purchases through Robux-bought currency (OFF-037/038). The provenance is lost. | §A.3, T29 |
| R6 | There is no runtime kill switch. §15 defers ops tooling to week 6+. | Every precedent response to a dupe started with disabling trading (AM-016, RBX-025, RBX-031). | §A.6, T32 |
| R7 | Receipt handling covers developer products only. `BindReceiptHandler` also delivers Robux-transfer receipts (OFF-015). | If transfers are ever enabled, receipts need an explicit, idempotent handler and ledger entry. | §A.2, T33 |
| R8 | Nothing stops a save that shrinks a profile drastically. | This is the RBX-009-style "saved empty data" class (UNVERIFIED for any specific incident, but the mechanism is documented in OFF-027). | §A.7, T26 |

---

## 4. Creator-motive analysis (Adopt Me! "open doors")

**Purpose.** For each publicly visible Adopt Me! failure or claim, rank the competing explanations by the evidence we
actually hold. Explanation labels: intended mechanic · trust-boundary error · datastore consistency · legacy · supply chain
· staff compromise · platform limitation · rollout · monitoring gap · support workflow · UI illusion · rumor. Root causes
were **never published** by Uplift for any of these events (no postmortem found; see `_notes/adoptme_osint.md` §3). Rankings
are therefore inferences, ordered by fit with the stated facts, and they are not findings.

**Plain statement.** **There is no primary evidence of intentional backdoors or insider abuse at Uplift Games.** The only
lead is fan speculation in September 2020 about an "admin panel" (AM-017, UNVERIFIED, outcome H). AM-048 records that no
primary evidence was found. Platform-level insider and support-panel abuse did happen at **Roblox** in 2020 (RBX-001,
STRONGLY CORROBORATED), and developer-account hijacks hit **other** Roblox studios in 2026 (RBX-019). That makes these a
generic risk class for every studio, ours included. It is not evidence about Uplift.

| Open door (date) | Ledger / confidence | Ranked explanations (most → least supported) | Evidence for the top ranks | What it teaches our design |
|---|---|---|---|---|
| Data loss, 0.3% of players, up to 2 days (2020-04-22) | AM-014 SC | 1. datastore consistency (a failed or stale save path) · 2. platform limitation · 3. rollout (Mega Neon shipped 2020-04-17; timing only, no causal evidence) · 4. monitoring gap · *staff compromise / rumor: no evidence* | "Up to 2 days" of loss for a small share fits stale-profile overwrite or failed autosave. The official post gave no cause. | Errored-never-saves, shrink guard (ASM-01); versioned backups are hourly, not per trade (OFF-026). |
| Trading disabled, "items disappearing" (2020-09-30) | AM-016 SC; AM-017 UNVERIFIED | 1. trust-boundary or commit error in trading (one side applied, the other not) · 2. datastore consistency · 3. rollout · 4. rumor ("blue dog dupe", "admin panel hacked") | Official wording describes loss, not creation: a non-atomic transfer pattern (OFF-005, OFF-023). The fan admin-panel claims have no support. | Saga commit (ASM-03), kill switch first (ASM-11). |
| Game set private over "a critical bug with Roblox's Datastore Servers" (2020-10-20) | AM-018 SC | 1. platform limitation (first-party attribution to Roblox) · 2. datastore consistency in the game's error handling (whether failed loads showed defaults is unknown) · 3. monitoring (they detected and acted fast) | The first-party post names Roblox DataStore. A support form for lost items followed the next day. | Fail closed, errored sessions, kill switch (ASM-37). Going private is a coarse kill switch. |
| Duplicate items removed from "clearly exploiting users" (2022-09-02) | AM-024 **STRONGLY CORROBORATED** (first-party post seen via snippet only) | 1. trust-boundary error: a non-idempotent claim (a player reply says double-clicking "claim" gave duplicates; single non-first-party source) · 2. rollout ("bug last night" suggests a recent change; inference) · 3. monitoring worked (cleanup within about a day) · 4. legacy · *staff compromise / supply chain: no evidence* | The only primary-corroborated Adopt Me! dupe. Its remediation deliberately spared players who "accidentally found the bug" or "traded for duplicate pets". | Idempotent claims (ASM-06), ledger-scoped cleanup that protects downstream holders (ASM-39). |
| Sakura Swoop exploiting ban wave (2025-04-11) | AM-034 SC | 1. intended mechanic abused via automation or client-trusted results (trust-boundary error) · 2. monitoring (detected, tiered bans; "currency caps had already been added") · 3. bots/farming | First-party: tiered bans, currency caps, and "We won't share our detection methods." Outcome C (inflated currency), not a pet dupe. | Server-computed event rewards with caps (ASM-21). |
| Hacked-account restores: 60-day, then once only within 30 days; hacked tickets paused (2021-05-31 / ~2025 / 2022-10-24) | AM-020, AM-021, AM-026 SC; AM-022 UNVERIFIED | 1. support workflow (capacity and abuse limits) · 2. platform limitation (ATO happens at the Roblox account layer: RBX-010, RBX-015) · 3. "restored pets untradable" is a rumor (UNVERIFIED) | The policy tightened over time, and intake closed "for the foreseeable future" in 2022. | Two-sided reversal, once-per-account, dual approval (ASM-18). One-sided restores are a known abuse class (ECO-028). |
| Help-center line "pet duplication is not possible" (~2025) | AM-029 SC; AM-030 SC | 1. support workflow / messaging (anti-scam framing aimed at "I can clone your pet" offers) · 2. UI illusion (the claims it addresses are visual scams) · *not* evidence that dupes never occurred | It conflicts literally with AM-024. The same help center admits automated duplicate-item anomaly blocks (AM-030). | Don't claim impossibility. Publish "dupes are patched and cleaned up" plus anomaly detection. |
| "Pet spawner" claims (2020–2026) | AM-039 SC (E); AM-040 UNVERIFIED (H) | 1. UI illusion (scripts self-describe as visual/client-side) · 2. rumor / scam lure (password-protected executables; fake executors deliver infostealers: RBX-014) · 3. trust-boundary error: **no evidence** any spawner produced server inventory | Client-created instances don't replicate (OFF-002, IMP-009). | Trade window rendered only from server state (ASM-43); education (ASM-42). |
| Insider / backdoor rumors (2020 onward) | AM-017, AM-048 UNVERIFIED | 1. rumor · 2. (generic class only) staff compromise / supply chain, which happened at *Roblox* (RBX-001, RBX-005) and to *other* developers (RBX-019) | No primary evidence at Uplift. Uplift careers show no dedicated security role (AM-047). That is an absence of a signal, not evidence of misconduct. | Assume the class anyway: dual approval, CI-only publish, key scoping (ASM-07, -08, -24, -25). |

---

## 5. Coverage check against the requested categories

| Category | Rows |
|---|---|
| Legit free/earned paths | ASM-54, ASM-28, ASM-49, ASM-55 |
| Trading, gifting, alts, RMT | ASM-23, ASM-27, ASM-40, ASM-20 |
| Trade state machine races | ASM-03, ASM-14, ASM-15, ASM-47 |
| DataStore persistence (session locks, failed-load-then-save, BindToClose, teleport) | ASM-01, ASM-02, ASM-12, ASM-16, ASM-29, ASM-31, ASM-32, ASM-50 |
| Shop/receipt (duplicate and concurrent receipts, BindReceiptHandler, refund webhook and clawback, Robux transfers, IsPaidItemTradingAllowed) | ASM-04, ASM-06, ASM-09, ASM-10, ASM-19, ASM-20, ASM-34 |
| Remote validation incl. NaN | ASM-05, ASM-33 |
| Asset cloning / import (E/F) | ASM-35, ASM-48, ASM-52, ASM-53, ASM-36 |
| Creator/admin/support powers and supply chain (Toolbox, plugins, npm, collaborators, Open Cloud, owner takeover) | ASM-07, ASM-08, ASM-24, ASM-25, ASM-26, ASM-38 |
| Bots, farming, event-currency farming | ASM-21, ASM-22, ASM-23 |
| Social engineering, ATO, one-sided rollback abuse | ASM-17, ASM-18, ASM-41, ASM-42, ASM-39 |
| Fake spawners | ASM-43 |
| Economy design | ASM-10, ASM-34, ASM-51, ASM-55 |
| Platform / ops realities | ASM-11, ASM-13, ASM-30, ASM-37, ASM-46 |
| MemoryStore / MessagingService non-durability | ASM-44, ASM-45 |

Effort figures in `07_BACKLOG.csv` are engineering estimates by the author of this file. They are not evidence.
