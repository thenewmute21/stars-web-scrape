# 02 — Historical Timeline: Adopt Me!, the Roblox platform, and comparable economies (pre-2017 to 2026-10-19)

Compiled 2026-10-19 from `_notes/*.md` and `01_EVIDENCE_LEDGER.csv` (210 rows). No new web research was done for this file. Every entry cites ledger IDs. Where a fact appears only in a note and has no ledger row, the entry says "notes only".

## Hero summary

- **Only one Adopt Me! duplication incident is confirmed by a first-party post: 2022-09-02** (AM-024). Uplift posted that it had removed duplicate items "from clearly exploiting users". This contradicts the later Uplift help-center line that "pet duplication is not possible" (AM-029). The help-center line is best read as guidance that dupe offers are scams.
- **Uplift has posted about four other first-party loss or abuse events:** the 2020-04-22 data loss (0.3% of players, up to 2 days; AM-014), the 2020-09-30 trading shutdown over items disappearing (AM-016), the 2020-10-20 privatisation that Uplift blamed on Roblox DataStore servers (AM-018), and the 2025-04-11 Sakura Swoop currency-exploit ban wave (AM-034). Root cause, scale and fix details were never published for any of them.
- **Anti-scam controls were added in steps:** the Trade License, 30-day history and two-stage trade (2020-11-05; AM-019), a 2-hour playtime gate for new accounts (2025-05-16; AM-035), and the cross-server Trading Hub with listing locks (2026-07-31; AM-037).
- **No evidence was found** of Adopt Me! dupes, rollbacks or ban waves in 2017, 2018, 2023, 2024 or 2026. No evidence was found of Adopt Me!-specific loss in the October 2021 Roblox outage. No primary evidence was found of insider or backdoor misconduct at Uplift.
- **Platform lesson (docs-verified):** current Roblox docs name "trade, leave, save fails" as a duplication vector (OFF-005). They also say receipts can run on two servers at once (OFF-012), and they offer no cross-key DataStore transactions (OFF-023). The classes of incident in this timeline remain possible today.
- **Evidence caveat:** only OFF- rows and the doc-quoted IMP- rows (60 rows) were verified verbatim, against `Roblox/creator-docs` commit `70a0110` (2026-10-17). **All 150 other rows are snippet-only.** That covers Uplift posts, press, DevForum, X, help-center pages and wikis: each was seen as a search-result title or summary, the page was never opened, and `link_checked` failed. In the post-mortem, 40 rows that were CONFIRMED were downgraded to STRONGLY CORROBORATED (18 AM-, 15 RBX-, 6 ECO-, 1 IMP-). This file marks them **"SC — CONFIRMED by first-party post (snippet-only)"** or **"SC — CONFIRMED pre-post-mortem (snippet-only)"**.

## How to read the entries

| Field | Values |
|---|---|
| Outcome A–H | A legit server pet; B legit pet without direct Robux; C unauthorized server-issued pet / inflated balance; D duplication / replayed grant; E client-only visual spoof; F external asset, not an entitlement; G compromised / fraudulent / reversed / support-issued; H unverified / misunderstood / fabricated; `n/a` = context, control or loss event |
| Confidence | Current ledger value: CONFIRMED / SC (STRONGLY CORROBORATED) / PLAUSIBLE / UNVERIFIED / DEBUNKED. A "(1P snippet)" suffix means a CONFIRMED-before-post-mortem row that rests on a first-party post seen only as a snippet |
| Status | live-active / historical-patched / historical-unresolved / status-unknown / n/a-intended-design |
| Basis | **[V]** docs-verified (creator-docs@70a0110) · **[S]** snippet-only |
| Doc dates | For OFF-/IMP- rows, dates are the **first appearance of the text in the creator-docs repo** (`git log -S`). They are not platform release dates. Repo history begins 2023-08-29, so a date of 2023-08-29 or 2023-11-02 means "already present when the repo began" |

---

## Strand 0 — Pre-2017 comparables (other games and platforms)

These entries are context for design choices only. None are Roblox or Adopt Me! evidence.

| Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|
| 2007 (Dec, per ledger) | RuneScape (Jagex) removes unbalanced free trade and the Wilderness "to curb botting, gold farming and item scamming" | B (trade restriction) | SC | historical-patched | [S] | ECO-006 |
| 2011-01-14 / 2011-01-17 | RuneScape player vote, ~91% Yes, to restore free trade (announced 14 Jan; return confirmed 17 Jan) | B | SC | historical-patched | [S] | ECO-006 |
| 2011-02-01 | RuneScape free trade and the Wilderness return. A wiki reports a "sudden and dramatic increase in the number of bots" afterwards | B | PLAUSIBLE (bot surge) | historical-unresolved | [S] | ECO-006, ECO-007 |
| 2012-01-04 | RuneScape notifies players when a partner declines or exits a trade, "in response to ongoing scams". The second confirmation screen highlights changed items in red | G (anti-scam control) | PLAUSIBLE | n/a-intended-design | [S] | ECO-008 |
| 2013-09-17 → 2014-03-18 | Blizzard announces, then carries out, the closure of the Diablo III gold and real-money auction houses ("ultimately undermines Diablo's core game play") | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-patched | [S] | ECO-009 |
| 2014 | EVE Online Fanfest talk (Dr. Eyjólfur Guðmundsson): net ISK injection ~20–25T/month, described as not inflationary | n/a | not rated | n/a | [S] | notes only (economy_social.md); no ledger row |
| 2015-10 (published 2015-10-12) | Valve says ~77,000 Steam accounts are hijacked and pillaged each month | G | SC | historical-unresolved | [S] | ECO-002 |
| 2015-12-09 | Steam trade holds: up to 3 days, or 1 day for friends of at least a year, unless the Mobile Authenticator has been on for 7+ days. Cancelling a held trade starts a cooldown | G (control) | SC | n/a-intended-design | [S] | ECO-001 |
| 2016-03-09 | Steam extends holds to up to 15 days for users without the authenticator | G (control) | PLAUSIBLE | n/a-intended-design | [S] | ECO-003 |

**Roblox pre-2017:** no ledger rows are dated before 2017. The ledger's earliest Roblox-platform item is the ~2017 multi-key UpdateAsync request (RBX-047).

---

## 2017

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| **Adopt Me! (claim, secondary)** | 2017-07 (fan guide: 2017-07-14) | Adopt Me! released on Roblox by DreamCraft (NewFissy and Bethink) | n/a | SC | n/a-intended-design | [S] | AM-001 |
| Roblox platform | ~2017 (thread 38833) | DevForum feature request for a multi-key UpdateAsync. DataStores cannot commit a cross-player trade atomically | D (design gap) | PLAUSIBLE | n/a-intended-design | [S] | RBX-047 |
| Roblox platform | 2017–2020 (attendee years) | RDC 2017–2020 attendee data, later breached (see 2020 and 2023) | n/a | — | — | [S] | RBX-006 |
| Other games | 2017 | Murder Mystery 2: alt-account duping glitch. Nikilis shuts down trading and bans some users (fan wiki only) | D | PLAUSIBLE | historical-patched | [S] | RBX-025 |

**Gaps (2017):** no evidence found of Adopt Me! trading, dupes or incidents. The date FilteringEnabled became mandatory could not be verified from an official source. The docs only say the property is "discontinued" (OFF-001 [V]).

## 2018

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| Adopt Me! | — | **No evidence found** of 2018 security or economy events | — | — | — | — | (adoptme_osint.md chronology) |
| Roblox platform | 2018 | DevForum thread describes Roblox restoring a compromised account's valuables only once per account | G | SC | status-unknown | [S] | ECO-029 |
| Roblox platform | ~2018–19 (thread 221954) | Malicious Studio plugins inject scripts into hidden services. A per-plugin Script Injection permission prompt follows. That prompt is **not** in creator-docs at 70a0110 | n/a (supply chain) | PLAUSIBLE | n/a-intended-design | [S] | RBX-022 |
| Roblox platform | 2018–2025 (thread range) | BindToClose / PlayerRemoving data-loss threads: shutdown waits ~30 s, so saves must run concurrently | D | PLAUSIBLE | n/a-intended-design | [S] | RBX-049 |
| Roblox platform | "commonly 2018" | FilteringEnabled made mandatory. **UNVERIFIED date**; the current docs confirm only that the property no longer has any effect | E | CONFIRMED (state) / date unverified | n/a-intended-design | [V] | OFF-001 |
| Other games | 2018–2019 | Murder Mystery 2 Icewing glitch: pack purchase duplicated, game pass removed | D | PLAUSIBLE | historical-patched | [S] | RBX-026 |

**Gaps (2018):** no evidence was found of the 2018 Kotaku/Ubisoft "R6 trading disabled for laundering" article. The search surfaced an unrelated Dec 2025 R6 Siege breach instead (economy_social.md).

## 2019

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| **Adopt Me! (first-party claim)** | 2019-06-07 | @AdoptMeSupport defines a "duping glitch" and asks players to report it. One search summary mentions a 20k Robux reward; a re-search could not reconfirm it | D | PLAUSIBLE | historical-unresolved | [S] | AM-013 |
| Adopt Me! (secondary) | 2019-06-15 | 440k concurrent users (fandom) | n/a | not rated | — | [S] | notes only (adoptme_osint.md §7) |
| Adopt Me! (secondary) | summer 2019 | Pets added (eggs, hatching). Trading of pets, cars and toys dates from this period. **No primary evidence found of the exact trading launch date** | B | PLAUSIBLE | n/a-intended-design | [S] | AM-002 |
| Adopt Me! (secondary) | 2019-07 | Neon pets: 4 fully grown pets of the same kind make 1 Neon | B | SC | n/a-intended-design | [S] | AM-003 |
| Adopt Me! (secondary) | 2019-10 / 2019-12 | Shadow Dragon (Halloween) and Frost Dragon (Christmas), 1,000 R$ each. Both are now obtainable only by trading, so non-payers can legitimately own Robux-origin pets | B | SC | n/a-intended-design | [S] | AM-006, ECO-017 |
| Adopt Me! (secondary) | 2019 | DevForum "Player Support Representatives, $25K/yr" posting | n/a | not rated | — | [S] | notes only (adoptme_osint.md §6) |
| Roblox platform | ~2019–20 (thread 412384) | User report: a catalog purchase endpoint with no cooldown gave duplicate hat grants | D | UNVERIFIED | historical-unresolved | [S] | RBX-038 |
| Other / industry | 2019-01 | Sixgill / The Independent: stolen cards buy Fortnite V-Bucks, which are resold at a discount to launder money | G | SC | historical-unresolved | [S] | ECO-033 |
| Other / industry | ~2019-10-28 | Valve makes newly bought CS:GO keys untradeable: "worldwide fraud networks have recently shifted to using CS:GO keys…". Valve concedes it "will impact some legitimate users" | G (control) | SC | n/a-intended-design | [S] | ECO-004, ECO-005 |

**Gaps (2019):** no primary text of the dupe bounty. Whether any 2019–2020 Adopt Me! dupe was confirmed is unknown. No 2019 Roblox support-abuse reports were found; the support-panel story is from 2020 (see Corrections).

## 2020

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| Adopt Me! (secondary) | 2020-04-17 | Mega Neon added (4 Luminous Neons make 1 Mega Neon) | B | SC | n/a-intended-design | [S] | AM-003 |
| Adopt Me! (secondary) | 2020-04 | ~683,404 CCU at the April Fools update (PC Gamer). The "Dress Your Pets" update reportedly hit 1.6M–1.786M (conflicting figures) | n/a | PLAUSIBLE | n/a | [S] | AM-009 |
| **Adopt Me! (first-party)** | **2020-04-22** | Data loss "only affected 0.3% of our players… up to 2 days". Affected players got an in-game message. Cause not given | n/a (loss) | SC — CONFIRMED by first-party post (snippet-only) | historical-patched | [S] | AM-014 |
| Adopt Me! (press) | 2020-05-26 | Press coverage of trust trades, last-second swaps, fake middlemen, "I can clone your pet" offers, impersonation | G | SC | live-active | [S] | AM-044 |
| Adopt Me! (secondary) | 2020-09-16 | Trading disabled for Korean players for legal compliance; gifting still allowed | n/a | PLAUSIBLE | status-unknown | [S] | AM-015 |
| **Adopt Me! (first-party)** | **2020-09-30** | Trading disabled to investigate "a serious trading bug which was causing items to disappear". Cause and re-enable date not found | n/a (loss) | SC — CONFIRMED by first-party post (snippet-only) | historical-patched | [S] | AM-016 |
| Adopt Me! (fan claim) | 2020-09 | Fan speculation of a "Blue Dog dupe" or a hacked admin panel / dev account. **Hypothesis only** | H | UNVERIFIED | status-unknown | [S] | AM-017, AM-048 |
| Adopt Me! (fan claim) | 2020 (claimed) | French SEO article claims "Frost dupe" and "Shadow dupe" collapsed values | H | UNVERIFIED | status-unknown | [S] | AM-050 |
| **Adopt Me! (first-party; platform cause)** | **2020-10-20 / 2020-10-21** | Game set private over "a critical bug with Roblox's Datastore Servers"; a support form was offered on 2020-10-21. Ledger classes this as RobloxPlatform | n/a (loss) | SC — CONFIRMED by first-party post (snippet-only) | historical-patched | [S] | AM-018 |
| **Adopt Me! (first-party)** | **2020-11-05** | "Trade Changes & Scam Prevention": a Trade License quiz (3 scenarios) to trade Ultra-Rare and Legendary pets; 30-day trade history; in-game scam reports; two-stage trade with a fairness warning; 9 trade slots | n/a (control) | SC — CONFIRMED by first-party post (snippet-only) | n/a-intended-design | [S] | AM-019, ECO-013, ECO-014 |
| Roblox platform | 2020 (reported 2020-05-04) | Motherboard: an insider was bribed, then a support rep phished. The panel could reset passwords, remove 2FA, ban users and grant currency. Roblox said a "small number of accounts" were affected | G | SC | historical-patched | [S] | RBX-001, RBX-002 (PLAUSIBLE) |
| Roblox platform | 2020-12-18 | Breach of data on ~3,943 RDC 2017–2020 attendees (per HIBP). It **surfaced only in July 2023** | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-unresolved | [S] | RBX-006 |
| Roblox platform (community) | 2020 onward | Community consensus forms on session locking (ProfileService, later ProfileStore) | D (mitigation) | SC | n/a-intended-design | [S] | RBX-046 |
| Other games | — | No 2020 other-game rows in the ledger | — | — | — | — | — |

**Gaps (2020):** root cause of the 2020-09-30 bug. **No evidence found** of when trading was re-enabled. No count of items restored after 2020-10-20. Fan claims of 2020 Frost or Shadow dupes have no primary support.

## 2021

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| Adopt Me! (first-party press release via secondary) | 2021-04-16 | Peak of 1.92M CCU (Ocean Egg). The Uplift careers page says 1.94M; no source for 1.94M was found | n/a | SC | n/a | [S] | AM-008 |
| Adopt Me! (secondary) | 2021-05-10 | DreamCraft rebrands to Uplift Games. ~40 staff (Vice) | n/a | SC | n/a | [S] | AM-001, AM-010 |
| **Adopt Me! (first-party)** | **2021-05-31** | Official TikTok: "If you've been hacked in the past 60 days, we may be able to restore your pets now!" | G | SC — CONFIRMED by first-party post (snippet-only) | historical-unresolved | [S] | AM-020 |
| Adopt Me! | 2021-10-28..31 | **No evidence found** of Adopt Me!-specific pet loss or rollback during the Roblox outage | n/a | SC — CONFIRMED pre-post-mortem (outage); no AM impact | historical-patched | [S] | AM-023 |
| Roblox platform | 2021-10-28..31 | ~73-hour outage caused by Consul streaming contention and a BoltDB issue. Roblox reports no user data loss and no intrusion | n/a | SC — CONFIRMED by first-party post (Roblox newsroom; snippet-only) | historical-patched | [S] | RBX-008 |
| Roblox platform | 2021-10 | noblox.js typosquats on npm carrying a trojan and ransomware (Sonatype) | n/a (supply chain) | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-patched | [S] | RBX-016 |
| Other games | ~2021–22 | Pet Simulator X "Hell Update" Dupe Patch: trading code revamped, new datastore version, duped diamonds reverted, stash accounts banned (secondary relay) | D | PLAUSIBLE | historical-patched | [S] | RBX-028 |

**Gaps (2021):** no 2021 "internal admin panel" Motherboard story was found; the only match is the 2020 one.

## 2022

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| Adopt Me! (third party) | 2022-07 | "Adopt Me Trading Values" value-list site breached: 86.1k accounts. Added to HIBP on 2025-02-10. **Not Uplift** | G | SC — CONFIRMED pre-post-mortem (HIBP; snippet-only) | historical-unresolved | [S] | AM-027 |
| **Adopt Me! (first-party) — ONLY CONFIRMED DUPE** | **2022-09-01 (bug) / 2022-09-02 (post)** | "We rolled out a fix to remove duplicate items from clearly exploiting users — this shouldn't affect players who accidentally found the bug last night, or traded for duplicate pets." A player reply says a double-click on "claim" gave duplicates, later removed with a "suspicious activity" note. Mechanism, scale and bans not disclosed | **D** | SC — CONFIRMED by first-party post (snippet-only) | historical-patched | [S] | AM-024 |
| Adopt Me! (secondary) | 2022-09-13 | Disabled in Belgium and the Netherlands over loot-box (paid random egg) rules | n/a | SC — CONFIRMED pre-post-mortem (press; snippet-only) | status-unknown | [S] | AM-025 |
| **Adopt Me! (first-party)** | **2022-10-24** | @AdoptMeSupport closes Hacked ticket intake "for the foreseeable future" and plans to re-evaluate policy and security | G | SC — CONFIRMED by first-party post (snippet-only) | historical-unresolved | [S] | AM-026 |
| Adopt Me! (community claim) | ~2022 (est. ~2022-10) | DevForum community tutorial names Adopt Me! as hit by "a wide-spread duplication exploit using a rollback", using malformed data to force a failed save. **Not an Uplift statement** | D | PLAUSIBLE | status-unknown | [S] | AM-028 |
| Roblox platform | ~2022-01 | DevForum: 3–7 day trade holds after suspected compromise. Robux and limiteds are reimbursed, in-game items are not | G | PLAUSIBLE | status-unknown | [S] | RBX-040 |
| Roblox platform | 2022-02 | Motherboard on "beaming": hijacked accounts emptied, items sold on Discord for USD or crypto. Roblox bans third-party trading sites and gives one rollback per account | G | SC | live-active | [S] | RBX-003, RBX-004, ECO-021, ECO-022 |
| Roblox platform | ~2022-03 (from 2022-03-08) | .ROBLOSECURITY cookie bound to IP region; it resets on region change | G (control) | SC | n/a-intended-design | [S] | RBX-010, ECO-023 |
| Roblox platform | 2022-07 | Employee phished; ~4GB of internal documents with creator PII posted after an extortion attempt | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-patched | [S] | RBX-005 |
| Roblox platform | 2022-10 | Roblox acquires Byfron (DevForum "Welcoming Byfron to Roblox") | n/a | SC | n/a-intended-design | [S] | RBX-011 |
| Roblox platform | FY2022 (10-K filed 2023-02) | Stolen-card Robux resold at a discount. Chargebacks from this fraud ≈3.16% of bookings | G | SC — CONFIRMED pre-post-mortem (SEC filing; snippet-only) | historical-unresolved | [S] | ECO-024 |
| Other games | 2022-02-01 | Pet Simulator X bank: missing gems and pets with "Unknown error" | H | UNVERIFIED | historical-unresolved | [S] | RBX-029 |
| Other games | 2022-03-27 | Pet Simulator X content-deleted, then quickly reversed (no reason given) | H | UNVERIFIED | historical-unresolved | [S] | RBX-030 |
| Other games | 2022-10-16 | Murder Mystery 2 deletes most duplicated Icewing and shop-item stacks | D | PLAUSIBLE | historical-patched | [S] | RBX-027 |
| Other / industry | 2022-12-19 | FTC v. Epic: refunds finalized 2023-03-14 plus a $275M COPPA penalty. Requires express informed consent, and bars locking accounts that dispute charges | G | SC — CONFIRMED pre-post-mortem (snippet-only) | n/a-intended-design | [S] | ECO-034 |

**Gaps (2022):** root cause, scale and ban count for the 2022-09-02 dupe. No primary source was found for a 2022 Pet Simulator X "Huge" wipe.

## 2023

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| Adopt Me! (guide) | by 2023 | 18 trade slots (Bloxswaps guide) | n/a | not rated | — | [S] | notes only (adoptme_osint.md §2) |
| Adopt Me! | — | **No evidence found** of incidents or ban waves in 2023 | — | — | — | — | (adoptme_osint.md) |
| Roblox platform | 2023 | Free UGC Limited claims drained by clients firing prompts. Fix: a final server-side eligibility check | C | SC | historical-patched | [S] | RBX-036 |
| Roblox platform | ~2023-05 (PiunikaWeb 2023-04-28) | Hyperion ships with the 64-bit Windows client; Synapse X and other paid executors stop sales. **Not in official docs** (OFF-041 UNVERIFIED) | n/a | SC (RBX-011) / UNVERIFIED from official (OFF-041) | n/a-intended-design | [S] | RBX-011, OFF-041 |
| Roblox platform | 2023-07-19/20 | The Dec 2020 RDC attendee breach surfaces publicly (gHacks, HIBP) | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-unresolved | [S] | RBX-006 |
| Roblox platform | 2023-08 | More than 12 noblox.js-impersonating npm packages deliver Luna Grabber (963 downloads) | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-patched | [S] | RBX-017 |
| Roblox platform | 2023-08 → 2024-08 | Year-long noblox.js npm campaign (Checkmarx: starjacking, postinstall hooks, Quasar RAT) | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-patched | [S] | RBX-018 |
| Roblox platform | 2023-08-18 | Class action over child gambling naming RBXFlip, Bloxflip and RBLXWild; Roblox denies. No outcome found | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-unresolved | [S] | RBX-042 |
| Roblox platform (docs) | 2023-08-29 | creator-docs repo history begins. The "Security tactics" page is already present | — | CONFIRMED | — | [V] | OFF-003 (method note) |
| Roblox platform (docs) | ≤2023-11-02 | FilteringEnabled documented as "discontinued and no longer takes effect" | E | CONFIRMED | n/a-intended-design | [V] | OFF-001 |
| Roblox platform | ≤ late 2023 | glTF import beta in the 3D Importer (Khronos; DevForum 3D Import Recap Aug–Oct). **Exact date UNVERIFIED** | F | SC | n/a-intended-design | [S] | IMP-002 |
| Other / industry | 2023-03-14 | FTC v. Epic $245M refunds finalized | G | SC — CONFIRMED pre-post-mortem | n/a-intended-design | [S] | ECO-034 |

## 2024

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| Adopt Me! (court record) | 2024-04-26 (filed) / 2024-12-23 (ruling) | Impulse Communications v. Uplift Games et al., D.R.I. 1:24-cv-00166 (trademark) | n/a | SC — CONFIRMED pre-post-mortem (govinfo; snippet-only) | status-unknown | [S] | AM-045 |
| Adopt Me! (press estimate) | 2024-05-21 | Dubit, via Kidscreen, estimates revenue above US$50M per year. No audited figure exists | n/a | UNVERIFIED | n/a | [S] | AM-011 |
| Adopt Me! (third-party values) | 2024-08 → | Frost Dragon value low (~134 pts) then ~+130% (value list only) | n/a | UNVERIFIED | n/a | [S] | AM-049 |
| Adopt Me! | — | **No evidence found** of a 2024 dupe, rollback or ban wave | — | — | — | — | (adoptme_osint.md) |
| Roblox platform | 2024-02/03 | Wine/Linux blocked; staff cite cheating and reverse engineering of Hyperion | n/a | SC | n/a-intended-design | [S] | RBX-012 |
| Roblox platform | 2024-07 (2024-07-09) | Breach at FNTech, the RDC registration vendor: 10,386 emails from RDC 2022–24 (HIBP). **Separate from RBX-006** | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-unresolved | [S] | RBX-007 |
| Roblox platform | 2024 | Executor scene moves to Mac and Android; many tools are scams (low-quality source) | n/a | PLAUSIBLE | status-unknown | [S] | RBX-013 |
| Roblox platform | 2024-09-25 (snippet) | Mesh & Image APIs (EditableMesh) Studio beta: not yet usable in published games | E | CONFIRMED (current doc rules) / date from snippet | n/a-intended-design | [V]/[S] | IMP-008 |
| Roblox platform | 2024-10-08 | Hindenburg short report alleges inflated DAU and child-safety failures; Roblox disputes it | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | n/a-intended-design | [S] | RBX-044 |
| Roblox platform (docs) | 2024-10-08 (repo) | DataStore 4 MB per-key value limit text | n/a | CONFIRMED | n/a-intended-design | [V] | OFF-024 |
| Roblox platform | 2024-10 → 2025-07 | Fake "executor" downloads (e.g. fake Xeno installers) deliver Lumma Stealer and a Java RAT | G | SC | live-active | [S] | RBX-014 |
| Roblox platform | 2024 | Players:BanAsync propagates bans to suspected alt accounts by default | B (control) | SC — CONFIRMED pre-post-mortem (create.roblox.com, but snippet-only) | live-active | [S] | ECO-030 |
| Other / industry | 2024-10-02 | CS2/Steam 7-day re-trade and re-market restriction | G (control) | PLAUSIBLE | status-unknown | [S] | ECO-010 |
| Other / industry | 2024-11 (published 2024-12) | EVE Online Monthly Economic Report with faucet/sink data, including a data-gap correction | n/a | SC — CONFIRMED pre-post-mortem (CCP; snippet-only) | live-active | [S] | ECO-012 |

**Gaps (2024):** the brief's "2024 asset permissions system" is **not confirmed**; the thread-ID range suggests 2025 (IMP-005). No official 2024–2025 Roblox DataStore data-loss incident report was found.

## 2025

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| Adopt Me! (third party) | 2025-02-10 | HIBP adds the 2022 value-site breach | G | SC — CONFIRMED pre-post-mortem | historical-unresolved | [S] | AM-027 |
| Adopt Me! (guides) | 2025-04 → 2025-05-02 | Cherry Blossom event currency buys pets without Robux (Bakeneko 3,650; Kage Crow 75,000) | B | SC | n/a-intended-design | [S] | AM-007 |
| **Adopt Me! (first-party)** | **2025-04-11** | Ban wave for Sakura Swoop minigame exploiting, in three tiers (3-day bans; bans until the currency can no longer be spent; a few permanent). Currency caps already added; "We won't share our detection methods". A guide gives the same day as the event start (discrepancy) | **C** | SC — CONFIRMED by first-party post (snippet-only) | historical-patched | [S] | AM-034 |
| **Adopt Me! (first-party)** | **2025-05-16** | "2 hour playtime restriction before a new account can trade with others"; Uplift says scam reports fell in its tests | n/a (control) | SC — CONFIRMED by first-party post (snippet-only) | live-active | [S] | AM-035 |
| **Adopt Me! (first-party help center)** | ~2025 (est. ~2025-07) | Uplift Zendesk: "pet duplication is not possible within Adopt Me, and any methods of duplication found are almost immediately patched". **Conflicts with AM-024** (see Corrections) | H | SC — CONFIRMED by first-party page (snippet-only) | live-active | [S] | AM-029 |
| Adopt Me! (first-party help center) | ~2025 | "Bans": trade bans for cross-trading, gambling and exploits. Anomaly-based blocks ("assuming you may have duplicated your item") | D (detection) | SC — CONFIRMED by first-party page (snippet-only) | live-active | [S] | AM-030 |
| Adopt Me! (first-party help center) | ~2025 | "Trading Problems": no reversal of accidental trades; lock items; avoid macros | n/a (control) | SC — CONFIRMED by first-party page (snippet-only) | live-active | [S] | AM-031 |
| Adopt Me! (first-party help center) | ~2025 | "Inappropriate Trading Conduct": cross-trading for Robux or cash, middlemen, eBay and Facebook Marketplace are bannable | G | SC — CONFIRMED by first-party page (snippet-only) | live-active | [S] | AM-032 |
| Adopt Me! (fan claim) | 2025 (manual patch ~2025-07) | House-cloning glitch and script; fans say partly patched | D | PLAUSIBLE | status-unknown | [S] | AM-036 |
| Adopt Me! (fan) | 2025-11 | Fan worries about Roblox age checks affecting trading | n/a | UNVERIFIED | status-unknown | [S] | AM-038 |
| Roblox platform (docs) | 2025-01-21 (repo) | Unresolved developer-product purchases "are not removed or refunded after the escrow period expires". `ProductPurchaseChannel` added | G / A | CONFIRMED | n/a-intended-design | [V] | OFF-013, OFF-014 |
| Roblox platform | 2025-02 (2025-02-08) | Roblox sues PlayerAuctions (trademark) over RMT of Roblox goods | n/a | SC — CONFIRMED pre-post-mortem (snippet-only) | historical-unresolved | [S] | RBX-043 |
| Roblox platform (docs) | 2025-04-07 (repo) | GetAsync 4 s cache with `UseCache=false` opt-out | D | CONFIRMED | n/a-intended-design | [V] | OFF-025 |
| Roblox platform | 2025-08 → 2025-11-07 | State AG suits over child safety: Louisiana (Aug), Kentucky, Florida, Texas (2025-11-07) | n/a | SC — CONFIRMED pre-post-mortem (RBX-045) / SC (ECO-036) | historical-unresolved | [S] | RBX-045, ECO-036 |
| Roblox platform (docs) | 2025-10-22 (repo) | `AssetService:LoadAssetAsync` "modern replacement": sandboxed by default, third-party loading opt-in | F | CONFIRMED | n/a-intended-design | [V] | OFF-033, IMP-007 |
| Roblox platform | 2025-10 → 2026-01 (activity) | Infostealers and session-cookie replay hit more than 610k accounts (arrests in 2026) | G | SC — CONFIRMED pre-post-mortem (snippet-only) | live-active | [S] | RBX-015 |
| Roblox platform | 2025-11 | Community report: Creator Store filter moderates models using require(id), loadstring, etc. | n/a | PLAUSIBLE | status-unknown | [S] | RBX-023 |
| Roblox platform (docs) | 2025-12-09 (repo) | Server authority model (beta); covers movement and physics only | n/a | CONFIRMED | status-unknown | [V] | OFF-009 |
| Roblox platform | 2025-12 | Third-party report: during a platform incident some games saved empty data | H | UNVERIFIED | status-unknown | [S] | RBX-009 |
| Other / industry | 2025-01-16 | FTC finalizes COPPA amendments (retention policy; no indefinite retention). Effective status after the Jan 2025 freeze is unverified | n/a | SC | status-unknown | [S] | ECO-035 |
| Other games | 2025-03/04 (~2025-03-31) | Fisch disables trading after the Second Sea update; no reason given | H | UNVERIFIED | status-unknown | [S] | RBX-033 |
| Other games | 2025-07 (early July) | Grow a Garden disables pet gifting and trading over a lag-based pet dupe. First fix reportedly didn't hold; some bans | D | SC | historical-patched | [S] | RBX-031 |
| Other games | 2025 | Grow a Garden off-platform black market (rare pets sold for more than $200) | n/a (RMT) | PLAUSIBLE | live-active | [S] | RBX-032 |
| Other / industry | 2025-07-16 | Valve CS2 "Trade Protection": 7-day protection, the owner can reverse **all** recent trades, and a reported 30-day cooldown follows | G (control) | SC | n/a-intended-design | [S] | ECO-011 |
| Other games | 2025-09 (2025-09-05) | Blox Fruits trading disabled, reportedly over auto-accept / "freeze trade" scams; no dupe confirmed | G | UNVERIFIED | status-unknown | [S] | RBX-034 |

**Gaps (2025):** no Uplift or Roblox statement specific to "pet generators" was found (AM-041 rests on guides). No official Uplift statement on bot, alt or AFK farming was found (ECO-031). No 2025 ban wave other than Sakura Swoop was found.

## 2026 (to 2026-10-19)

| Lane | Date | Event | Outcome | Confidence | Status | Basis | Ledger |
|---|---|---|---|---|---|---|---|
| Adopt Me! / platform | 2026-01 | Roblox facial age checks become mandatory for chat. Roblox help says an age check is needed for *platform* Limiteds trading. **No evidence found that Adopt Me! in-game trading is age-gated** | n/a | UNVERIFIED | status-unknown | [S] | AM-038 |
| Adopt Me! (first-party site) | 2026-04-28 | Uplift posts Gameplay and Senior Gameplay Engineer roles. **No security, anti-cheat or T&S role found** | n/a | SC | n/a | [S] | AM-047 |
| Adopt Me! (third-party scanner) | 2026-07-30 | Lookalike phishing domain adoptme.kr registered and flagged; playingadopt.me flagged as suspicious | G | PLAUSIBLE | live-active | [S] | AM-043, IMP-019 |
| **Adopt Me! (first-party site)** | **2026-07-31** | Trading Hub: cross-server listings through the Trading Phone. Unlock needs ~2h playtime, a Trade License and a Neon pet. Listings cost 100 Bucks and listed pets are locked. Imbalance guardrail is "not a true value system" | n/a (control) | SC | live-active | [S] | AM-037 |
| Adopt Me! (guides) | 2026-08 | New ticket eggs (Basic 0.25%, Crystal 5.9% legendary) | B | SC | n/a-intended-design | [S] | AM-004 |
| Adopt Me! (player report) | 2026-09 | DevForum player report of DataStore errors affecting Adopt Me! and ERLC; mixed replies | n/a (loss) | UNVERIFIED | status-unknown | [S] | AM-051 |
| Adopt Me! | 2026 | **No evidence found** of a 2026 dupe or rollback. No evidence of any player pet-import or UGC-pet feature (IMP-017) or of leaked test pets (IMP-024) | — | UNVERIFIED (absence) | — | [S] | IMP-017, IMP-024 |
| Roblox platform (docs) | 2026-01-14 (repo) | New client-server boundary page: the NaN trade-offer example; "trade + leave + failed save" named as duplication; token-bucket rate limiting; prompt/detector caveats | C / D | CONFIRMED | n/a-intended-design | [V] | OFF-004, OFF-005, OFF-006, OFF-007 |
| Roblox platform (docs) | 2026-02-18 (repo) | "Secure within universe only" place access control (server-initiated teleports only) | E | CONFIRMED | n/a-intended-design | [V] | OFF-010, IMP-023 |
| Roblox platform | 2026-02 | FY2025 10-K: Roblox "unable to control or stop all unauthorized, fraudulent, or illegal transactions" | G | SC — CONFIRMED pre-post-mortem (SEC; snippet-only) | live-active | [S] | ECO-025 |
| Roblox platform (docs) | 2026-04-02 / 2026-05-04 (repo) | `BindReceiptHandler` and `Enum.ReceiptDecision` | A | CONFIRMED | n/a-intended-design | [V] | OFF-015 |
| Roblox platform | 2026-04-30 (announced) | Ukrainian police arrest 3 over the 610k+ account infostealer and cookie campaign | G | SC — CONFIRMED pre-post-mortem (snippet-only) | live-active | [S] | RBX-015 |
| Roblox platform | 2026-04 → 06 | Fake job offers lead developers to run malware; games and groups are transferred out; a game restored after press contact | G | SC — CONFIRMED pre-post-mortem (snippet-only) | live-active | [S] | RBX-019, RBX-020 (UNVERIFIED) |
| Roblox platform (docs) | 2026-05-04 (repo) | Robux transfers (Plus subscribers, 10–500 R$, game earns 10%) | B | CONFIRMED | n/a-intended-design | [V] | OFF-016 |
| Roblox platform (docs) | 2026-05-19 (repo) | Account tiers: Roblox Kids, Select, and Roblox (age-checked 16+) | n/a | CONFIRMED | n/a-intended-design | [V] | OFF-040 |
| Roblox platform (docs) | 2026-05-27 (repo) | Paid random items page: "Hatch an egg for a pet" requires disclosed odds. `IsPaidItemTradingAllowed=false` blocks paid-item trading | n/a | CONFIRMED | n/a-intended-design | [V] | OFF-037, OFF-038 |
| Roblox platform (docs) | 2026-05-30 (effective; text 2026-07-07) | Cross-game pass and developer product sales disabled | n/a | CONFIRMED | n/a-intended-design | [V] | OFF-017 |
| Roblox platform (docs) | 2026-07-14 (repo) | DataStore storage limit: 500 MB + 1 MB × lifetime users | n/a | CONFIRMED | n/a-intended-design | [V] | OFF-024 |
| Roblox platform | 2026-07 | DevForum report of a platform vulnerability allowing server-side execution and DataStore modification (**not Adopt Me!-specific**); reported patched | C | UNVERIFIED | historical-patched | [S] | AM-052 |
| Roblox platform (docs) | 2026-08-11 (repo) | `Player.AgeChecked` and `PromptAgeCheck` | n/a | CONFIRMED | n/a-intended-design | [V] | OFF-039 |
| Roblox platform (docs) | 2026-09-03 / 2026-10-01 (repo) | "Transaction Refunded" webhook. Passes and avatar items refunded by customer service are auto-revoked; developer products are the game's job | G | CONFIRMED | n/a-intended-design | [V] | OFF-020, OFF-021 |
| Roblox platform | 2026 (n/d) | DevForum user report: traders abuse account-recovery rollbacks so that only their side is reversed | G | UNVERIFIED (RBX-039) / PLAUSIBLE (ECO-028) | status-unknown | [S] | RBX-039, ECO-028 |
| Roblox platform | 2026? | DevForum: UGC Limited prize stock bypassed within minutes | C | UNVERIFIED | status-unknown | [S] | RBX-037 |
| Roblox platform | 2026-10-17 | creator-docs commit `70a0110`, the verification baseline for all [V] rows | — | — | — | [V] | OFF-*, IMP-* |
| Roblox platform | 2026-11-01 (claimed) | Third-party blog claims a policy making receipt of stolen items grounds for termination | n/a | UNVERIFIED | status-unknown | [S] | RBX-041 |
| Other games | 2026 | Blade Ball developer offers up to $10k for a working dupe before launching trading | n/a (control) | SC | n/a-intended-design | [S] | RBX-035 |

**Gaps (2026):** whether Adopt Me! trading checks Roblox age checks; whether hacked-restored pets are untradeable (AM-022 UNVERIFIED); whether trade reversals now trace downstream trades (AM-033 UNVERIFIED); whether the Server Authority beta went GA after 2026-10-17.

---

## Undated or ongoing items (not placed in a year)

| Lane | Event | Outcome | Confidence | Basis | Ledger |
|---|---|---|---|---|---|
| Adopt Me! | Bucks earning routes (tasks, daily login, job stands, Money Tree); eggs bought with Bucks at 1.5% / 3% / 8% legendary | B | SC | [S] | AM-004, AM-005 |
| Adopt Me! | Rare pets sold off-platform for up to US$100–300; Eldorado and StarPets complaints | G | SC / PLAUSIBLE | [S] | AM-012, ECO-032 |
| Adopt Me! | Official hacked-account help article: one restoration only, within 30 days, proof required | G | SC — CONFIRMED by first-party page (snippet-only) | [S] | AM-021 |
| Adopt Me! | "Visual pet spawner" scripts are self-described as client-side only | E | SC | [S] | AM-039 |
| Adopt Me! | "Tradable spawner", "force accept", "trade freeze" claims; some distribute executables | H | UNVERIFIED | [S] | AM-040 |
| Adopt Me! | Pet generators and free-pet sites harvest credentials and cookies; "beaming" | G | SC / PLAUSIBLE | [S] | AM-041, AM-042 |
| Adopt Me! | "Clone your pet" services are scams; fake proof via edited media | H / E | SC / UNVERIFIED | [S] | IMP-018, IMP-020 |
| Adopt Me! | ~15 s confirm delay in the trade window (community wiki only) | n/a | UNVERIFIED | [S] | ECO-015 |
| Adopt Me! | Values set by third-party lists (Elvebredd, AMVGG); no official price | B | SC | [S] | ECO-016 |
| Roblox platform | Backdoored Toolbox models and plugins using require(assetId) | C | SC — CONFIRMED pre-post-mortem (RBX-021) / CONFIRMED [V] (OFF-035, IMP-025) | [S]/[V] | RBX-021, OFF-035, IMP-025 |
| Roblox platform | Talos: fake free-Robux pages, HAR-file cookie theft, "double trade" balance drain | G | SC | [S] | ECO-020 |
| Roblox platform | Help center: off-window deals are not reversed; unauthorized charges can close accounts | G | SC | [S] | ECO-018, ECO-026 |
| Roblox platform | Chargebacks produce negative Robux balances (third party) | G | UNVERIFIED | [S] | ECO-027 |
| Roblox platform | No public leaked Open Cloud key incident found | H | UNVERIFIED | [S] | RBX-024 |
| Generic | No developer-confirmed dupe or rollback found for PS99, Steal a Brainrot, Jailbreak, Bee Swarm, Royale High | H | UNVERIFIED | [S] | RBX-051 |

---

## Corrections and reconciliations

| # | Common or earlier framing | What the evidence shows | Ledger |
|---|---|---|---|
| 1 | "Roblox support/admin panel abuse in 2019" or "in 2021" | The Motherboard-reported bribed insider and phished support rep date to **2020** (reported 2020-05-04). No 2019 support-abuse report and no 2021 "internal admin panel" story were found | RBX-001, RBX-002 |
| 2 | "2023 RDC data leak" | The breach is dated **2020-12-18** (HIBP) and **surfaced in July 2023**. It is separate from the **July 2024 FNTech** vendor breach (10,386 emails, RDC 2022–24) | RBX-006, RBX-007 |
| 3 | Uplift help center: "pet duplication is not possible within Adopt Me" | Uplift's own post of **2022-09-02** confirms a dupe and its clean-up. The help-center line (~2025) is best read as "dupe offers in trade are scams". The same help center's "Bans" page admits anomaly detection for possibly duplicated items | AM-029 vs AM-024, AM-030 |
| 4 | 2020-10-20 loss counted as an Adopt Me! bug | Uplift blamed "Roblox's Datastore Servers", so the ledger classes it as RobloxPlatform | AM-018 |
| 5 | Oct 2021 Roblox outage caused Adopt Me! pet loss | No evidence of Adopt Me!-specific loss. Roblox reported no user data loss | AM-023, RBX-008 |
| 6 | 2020 "Frost / Shadow dupe"; Sept 2020 "admin panel hacked" | Single SEO article and fan speculation only; held as H hypotheses | AM-050, AM-017, AM-048 |
| 7 | Hacked-restore window | 60 days (TikTok, 2021-05-31), later 30 days and once only (help article, undated). This is a policy change, not a contradiction; the order is inferred | AM-020, AM-021 |
| 8 | Sakura Swoop ban-wave timing | The tweet (2025-04-11, from the status ID) falls on the same day a guide gives as the event start. Either a soft launch or a guide error | AM-034 |
| 9 | Peak CCU 1.94M | Only 1.92M (April 2021) is sourced; 1.94M appears only on the Uplift careers page | AM-008 |
| 10 | FilteringEnabled mandatory "in 2018" | Date not verified from an official source. The docs confirm only that it is "discontinued" | OFF-001 |
| 11 | Hyperion rollout dates | SC from press and DevForum snippets (RBX-011). The official docs do not mention it (OFF-041 UNVERIFIED) | RBX-011, OFF-041 |
| 12 | "2024 asset permissions system" | Not confirmed; the thread-ID range suggests 2025. Rules are docs-verified, the date is not | IMP-005 |
| 13 | Unresolved dev-product receipts are auto-refunded | Docs now say they are "not removed or refunded after the escrow period expires" (text first in repo 2025-01-21) | OFF-013 |
| 14 | Robux-bought pets are untradeable | No source says so; Shadow and Frost Dragons are tradeable | AM-006 |
| 15 | 40 rows rated CONFIRMED | Downgraded to SC in the post-mortem because they were seen only as snippets (18 AM-, 15 RBX-, 6 ECO-, 1 IMP-). Original value kept in `confidence_pre_postmortem` | ledger |
| 16 | "arktimes" as a scam-pattern source | economy_social.md cites arktimes for fake-middleman patterns, while asset_import.md lists `nwww.arktimes.com` as an excluded SEO-spam mirror. Treat any arktimes citation as low authority until re-checked | notes only |

## Consolidated Adopt Me! "no evidence found" list

- Exact date trading launched (2019).
- Primary text of the 2019 dupe bounty; whether any 2019–2020 dupe was confirmed.
- Root cause of the 2020-09-30 trading bug; the date trading was re-enabled.
- Root cause, scale and bans for the 2022-09-02 dupe.
- Any Uplift or Roblox postmortem; any game-wide economy rollback; any mass "hacked pet" removal other than the 2022-09-02 clean-up.
- Ban waves in 2023 or 2024; any 2026 dupe or rollback.
- Adopt Me!-specific loss in the Oct 2021 outage.
- Uplift security, anti-cheat or T&S hires; insider or backdoor misconduct (no primary evidence).
- An Uplift statement on generators, or on bot, alt, AFK or promo farming.
- Age-check gating of Adopt Me! trading; untradeability of restored pets.
- A player pet-import or UGC-pet feature; leaked developer test pets.
- Any audited revenue figure; any FTC or regulator action on fraud or security.
- Any Uplift layoff or acquisition news for 2025–2026.

---

## Post-mortem follow-up additions (2026-10-19)

From `_notes/followup_verification.md`. All entries are snippet-only.

| Date | Lane | Event | Outcome | Confidence | Ledger |
|---|---|---|---|---|---|
| by 2019-06-07 | Adopt Me! | Two support posts show trading already existed. The launch date is still unknown. | n/a | STRONGLY CORROBORATED | AM-002 |
| 2019-08-29 | Adopt Me! | Support stops refunding scams for items traded outside the trade menu. | G | STRONGLY CORROBORATED | FU-008 |
| 2020-10-20 | Platform → Adopt Me! | Roblox DevForum incident report: a game-server update broke DataStore reads and was rolled back. This is the independent cause of AM-018. | platform | STRONGLY CORROBORATED | FU-004 |
| 2025-02 | Adopt Me! | Subscription Rewards exploit: a few players generated large numbers of reward items; trading of them blocked, accounts banned. | C | STRONGLY CORROBORATED | FU-001 |
| 2025-04-04 → 04-11 | Adopt Me! | Sakura Swoop event launches on 04-04; the ban wave follows on 04-11. This resolves an earlier date conflict. | C | STRONGLY CORROBORATED | AM-034 |
| ~2025-06-23 | Adopt Me! | Improved in-game report system can return pets after reported scams. | G | STRONGLY CORROBORATED | FU-006 |
| 2025-07-01 | Adopt Me! | Players kicked by "bug detection"; Uplift investigates. Shows the false-positive cost of anti-exploit. | n/a | STRONGLY CORROBORATED | FU-005 |
| 2026-06-30 | Adopt Me! | Purchasing and trading reportedly paused over a bug. Fan account only. | H | PLAUSIBLE | FU-002 |
| 2026-07-15 | Adopt Me! | Bat Dragon surge; trading paused the same day. A fan account relays that Uplift said a staff account was compromised and it was not a dupe. | C / G | PLAUSIBLE | FU-003 |
| 2026-07-31 | Adopt Me! | Trading Hub launch date fixed by a second official post on 2026-07-30. | control | STRONGLY CORROBORATED | AM-037 |
