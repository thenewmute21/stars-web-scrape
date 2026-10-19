# Roblox-wide and other-game incidents relevant to pet/item economies

Agent: Roblox-wide incidents (ledger prefix RBX-). Execution date: 2026-10-19. Read-only OSINT.
Companion ledger: `ledger_roblox.csv` (52 rows, RBX-001..RBX-052).

## Method and important limitation
- **No page could be opened.** WebFetch and curl were refused by the sandbox egress proxy (403 CONNECT for
  devforum.roblox.com, create.roblox.com, wikipedia, archive.org, press sites). All evidence below comes from
  **WebSearch result titles, URLs and search-engine summaries**. I did not read any source page in full.
  Every ledger row is therefore marked `link_checked = no(egress-blocked...)`, and quotes are short
  snippets from search summaries, not verified page text. A follow-up pass with fetch access should
  re-check every URL, and especially quotes and dates.
- No executors, scripts or exploit pages were opened. Pages that offer dupe or exploit methods appeared in
  results (SEO spam, GitHub script listings). They were not used and are not linked.
- None of the findings are Adopt Me!-specific. No Adopt Me! items were recorded.

## Chronological table

| Date | Event | Class | Key source(s) | Confidence | Ledger |
|---|---|---|---|---|---|
| 2017 | MM2 dupe via alt accounts. Nikilis shut down trading and banned some users | trade dupe, kill-switch | MM2 Fandom wiki | PLAUSIBLE | RBX-025 |
| ~2017 | DevForum request for a multi-key UpdateAsync, because DataStores can't commit a cross-player trade in one atomic call | platform design gap | devforum.roblox.com/t/multikey-updateasync/38833 | PLAUSIBLE | RBX-047 |
| ~2018-19 | Malicious Studio plugins injected scripts into hidden services. A per-plugin Script Injection permission prompt followed | plugin supply chain | devforum.roblox.com/t/script-injection-vulnerability/221954 | PLAUSIBLE | RBX-022 |
| 2018-19 | MM2 Icewing pack purchase duplicated. Game pass removed | purchase-grant replay | MM2 Fandom wiki | PLAUSIBLE | RBX-026 |
| ~2019-20 | User report: a catalog purchase endpoint with no cooldown gave duplicate hat grants | missing idempotency | devforum.roblox.com/t/roblox-hat-duplication-bug/412384 | UNVERIFIED | RBX-038 |
| 2020-05 | Insider bribed, then a support rep phished. The support panel could reset passwords, remove 2FA and grant currency. Roblox says few accounts were affected | insider / support-tool abuse | Motherboard via boingboing.net/2020/05/04/...; SC Magazine | STRONGLY CORROBORATED | RBX-001/002 |
| 2020-12-18 / 2023-07 | Data on about 3,943 RDC 2017-2020 attendees leaked (surfaced July 2023) | vendor/data leak | HIBP; ghacks 2023-07-20; Hackread | CONFIRMED | RBX-006 |
| 2021-10 | noblox.js typosquats on npm carrying trojans and ransomware | npm supply chain | Sonatype; THN 2021-10 | CONFIRMED | RBX-016 |
| 2021-10-28..31 | 73-hour outage. Root causes: Consul streaming contention and a BoltDB issue. Roblox reports no user data loss | availability | about.roblox.com/newsroom/2022/01/roblox-return-to-service-10-28-10-31-2021 | CONFIRMED | RBX-008 |
| ~2021-22 | PSX "Hell Update" Dupe Patch: trading code revamped, new datastore version, duped diamonds reverted, stash accounts banned | trade/datastore dupe | gamerjournalist.com/pet-simulator-x-hell-update/ (secondary) | PLAUSIBLE | RBX-028 |
| 2022-01 | Community post on account theft: 3-7 day trade holds after suspected compromise. Roblox reimburses Robux and limiteds but not in-game items | recovery gap | devforum.roblox.com/t/combatting-account-theft/1645586 | PLAUSIBLE | RBX-040 |
| 2022-02 | Motherboard on "beaming": stolen limiteds resold on Discord for USD or crypto. Roblox bans third-party trading sites and offers one rollback per account | ATO + RMT | vice.com/en/article/88gd4a/roblox-beaming-hackers | STRONGLY CORROBORATED | RBX-003/004 |
| 2022-02 | PSX bank: missing gems and pets, "Unknown error" | shared-storage integrity | piunikaweb 2022-02-01 | UNVERIFIED | RBX-029 |
| ~2022-03 | .ROBLOSECURITY tied to IP region. The cookie resets when the region changes | session hardening | noblox.js docs; DevForum 2231529 | STRONGLY CORROBORATED | RBX-010 |
| 2022-07 | Employee phished. 4GB of internal docs with creator PII posted after an extortion attempt | staff phishing | Malwarebytes 2022-07; Motherboard | CONFIRMED | RBX-005 |
| 2022-10 | Roblox acquires Byfron | anti-tamper | DevForum "Welcoming Byfron to Roblox" | STRONGLY CORROBORATED | RBX-011 |
| 2022-10-16 | MM2 removes most duplicated Icewing and shop-item stacks | dupe remediation | MM2 Fandom wiki | PLAUSIBLE | RBX-027 |
| 2023 | Free UGC Limited claims drained by clients firing prompts. Fix: a final server-side eligibility check | client-trusted reward | superawesome.com; DevForum 2500187 | STRONGLY CORROBORATED | RBX-036 |
| 2023-05 | Hyperion ships with the 64-bit Windows client. Synapse X and other paid executors halt sales | anti-tamper | PiunikaWeb 2023-04-28; wikis | STRONGLY CORROBORATED | RBX-011 |
| 2023-08 | More than 12 noblox.js-impersonating npm packages delivering Luna Grabber (963 downloads) | npm supply chain | ReversingLabs; THN 2023-08 | CONFIRMED | RBX-017 |
| 2023-08-18 | Class action over child gambling naming RBXFlip, Bloxflip and RBLXWild. Roblox denies | RMT/gambling | TechCrunch 2023-08-18; Rolling Stone | CONFIRMED | RBX-042 |
| 2023-08..2024-08 | Year-long noblox.js npm campaign (starjacking, postinstall hook, Quasar RAT) | npm supply chain | Checkmarx; THN 2024-09 | CONFIRMED | RBX-018 |
| 2024-03 | Roblox blocks Wine/Linux, citing cheating and reverse engineering of Hyperion | anti-tamper | It's FOSS; GamingOnLinux | STRONGLY CORROBORATED | RBX-012 |
| 2024-07 | Breach at FNTech (RDC registration vendor) exposes 10,386 emails from RDC 2022-24 | vendor breach | BleepingComputer; HIBP; Cyber Daily 2024-07-09 | CONFIRMED | RBX-007 |
| 2024 | Executor scene moves to Mac/Android plus a few Windows tools, many of them scams | executor ecosystem | Reddit mirror (low quality) | PLAUSIBLE | RBX-013 |
| 2024-10-08 | Hindenburg short report alleging inflated DAU and child-safety failures | reputational | GameWorldObserver 2024-10-09 | CONFIRMED | RBX-044 |
| 2024-10..2025-07 | Fake "executor" downloads delivering Lumma Stealer and a Java RAT (fake Xeno installers) | malware/ATO | ANY.RUN; SC Media (Bitdefender) | STRONGLY CORROBORATED | RBX-014 |
| 2025-02 | Roblox sues PlayerAuctions over RMT of Roblox goods (trademark claims) | RMT enforcement | Bloomberg Law; Local News Matters 2025-02-08 | CONFIRMED | RBX-043 |
| 2025-03/04 | Fisch disables trading after the Second Sea update. No reason given | kill-switch | Deltia's Gaming | UNVERIFIED | RBX-033 |
| 2025-07 | Grow a Garden disables pet gifting/trading over a lag-based pet dupe. First fix reportedly didn't hold. Some accounts restricted or banned | gift/trade race dupe | Sportskeeda; roonby 2025-07-25 | STRONGLY CORROBORATED | RBX-031 |
| 2025 | Grow a Garden off-platform black market (Discord and websites; rare pets sold for more than $200) | RMT | Calcalist CTech | PLAUSIBLE | RBX-032 |
| 2025-08..11 | State AGs sue Roblox over child safety: Louisiana, Kentucky, Texas (filed 2025-11-07) | regulatory | WSMV 2025-08-15; KWTX 2025-11-17 | CONFIRMED | RBX-045 |
| 2025-09 | Blox Fruits trading disabled, reportedly over auto-accept/"freeze trade" scams | trade-confirmation abuse | roonby 2025-09-05 (low quality) | UNVERIFIED | RBX-034 |
| 2025-10..2026-01 | Infostealers and session-cookie replay hit more than 610k accounts. Ukrainian police arrest 3 (announced April 2026) | ATO at scale | The Record; BleepingComputer; Security Affairs 2026-04-30 | CONFIRMED | RBX-015 |
| 2025-11 | Creator Store filter reportedly moderates models using require(id), loadstring, etc. | supply-chain mitigation | DevForum 4051504 | PLAUSIBLE | RBX-023 |
| 2025-12 | Reported platform incident in which some games saved empty data | error handling | allthings.how | UNVERIFIED | RBX-009 |
| 2026 | Blade Ball offers $10k for a working dupe before launching trading | pre-launch bounty | Pocket Tactics; LevelUp | STRONGLY CORROBORATED | RBX-035 |
| 2026-04..06 | Fake job offers lead developers to run malware. Their accounts are used to transfer games and groups. Roblox restored a game only after press contact | dev ATO / game hijack | 404 Media; Malwarebytes 2026-06-17; Help Net Security 2026-06-18 | CONFIRMED | RBX-019/020 |
| 2026 (n/d) | User report: traders abuse Roblox account-recovery rollbacks to keep both sides of a trade | recovery abuse | DevForum 4820634 | UNVERIFIED | RBX-039 |
| 2026-11-01 (claimed) | Policy reportedly making receipt of stolen items grounds for termination | policy | techwiser.com (third-party only) | UNVERIFIED | RBX-041 |
| ongoing | Backdoored free models and plugins using require(assetId). Official docs recommend sandboxing with Script Capabilities | asset supply chain | create.roblox.com/docs/scripting/security/third-party-vulnerabilities | CONFIRMED | RBX-021 |

## Section notes

### 1. Dupes and rollbacks in other trading games
- **MM2 (Nikilis):** has the best-documented history, but only on the fan wiki. 2017: alt-account dupe, so
  trading was shut down. 2019: Icewing pack purchase replayed, so the game pass was pulled. 2022: shop-item
  dupe, and most duplicated stacks were deleted on 2022-10-16. The pattern is a kill-switch, then targeted
  deletion, then a value crash.
- **Pet Simulator X (BIG Games):** a secondary relay of the "Hell Update" changelog lists a "Dupe Patch".
  It describes revamped trading code, a move to a new datastore version, bans for top exploiters and
  dupe-stash accounts, and reverting duped diamonds. Snippet: "duping situation (especially mythical pets)
  became very severe". No BIG Games primary post was found. **I found no reliable evidence of a 2022 Huge
  wipe or a PS99 Trading Plaza dupe closure.**
- **Grow a Garden (2025):** pet gifting was disabled around early July 2025 because of a pet-duplication
  exploit. Developers acknowledged it on Discord (relayed second-hand). Reports describe a server-lag-based
  dupe of rare pets, a first fix that "didn't hold", and trade restrictions or bans on some accounts. The
  root-cause class is a non-atomic transfer under latency (inferred, not stated by the developer).
- **Blade Ball (2026):** the developer offered a $10k bounty for a dupe of a "sword / trade token"
  before launching trading. This is a useful pre-launch practice.
- **Fisch and Blox Fruits:** both disabled trading, but there is no developer-confirmed dupe. The Blox
  Fruits reports point to auto-accept scripts and "freeze trade" scams (abuse of the trade-confirmation
  step).
- **Roblox catalog limiteds / UGC:** no confirmed platform-wide limited dupe was found. The confirmed
  class is 2023 **free UGC limited claim draining**, where clients could trigger prompts for rewards they
  weren't eligible for. The fix was a server-side eligibility check. There is an older user report of a
  purchase endpoint with no cooldown.

### 2. Platform security
- **Insider and support-tool abuse:** the reports date from 2020, not 2019 or 2021. Motherboard
  (Joseph Cox) reported an insider who was bribed, followed by a support rep who was phished. The panel
  could reset passwords, remove 2FA, ban users and grant currency. Roblox said "small number of
  accounts". This is the clearest primary evidence that **support/admin paths can mint or move items**.
- **Employee phishing:** in July 2022, internal documents were posted after an extortion attempt.
  No "internal admin panel 2021" Motherboard story was found apart from the 2020 one.
- **Developer data:** the "2023 RDC leak" was in fact a December 2020 breach that surfaced in July 2023
  (about 3,943 people). A separate July 2024 FNTech vendor breach exposed 10,386 emails.
- **Outage:** the October 2021 outage lasted 73 hours (Consul). Roblox reported no data loss. The lesson
  for games is to fail closed when backends are degraded.
- **Account takeover / beaming:** Motherboard 2022 on beaming. Later, infostealers spread as fake
  executors (Lumma, Xeno-themed RAT). The 2026 Ukrainian arrests covered more than 610k accounts
  compromised through infostealers and session cookies. Sessions are bound to IP region (~2022 per
  community docs). No official Roblox source was found for an "Account Session Protection" or
  device-binding feature. Pages describing it were SEO content.
- **Anti-tamper:** Byfron was acquired in October 2022, Hyperion shipped in 2023, and Wine was blocked in
  March 2024.

### 3. Supply chain
- **npm:** noblox.js typosquats in 2021 (Sonatype), August 2023 (ReversingLabs, Luna Grabber) and
  2023-2024 (Checkmarx, Quasar RAT, postinstall hooks, starjacking). **No Roblox-targeting PyPI report from
  Checkmarx was found.** The 2026 game-hijack cases involved a Python "database tool" package delivered by
  social engineering.
- **Assets and plugins:** Roblox's official docs state that Creator Store moderation "is not guaranteed
  to remove all such scripts". They recommend sandboxing models with Script Capabilities and being careful
  with Network, DataStore, AssetRequire, CapabilityControl and LoadString. DevForum threads show the
  require(assetId) backdoor pattern, introduced by plugins and free models.
- **Group and game takeover (2026):** developers were lured with fake job offers, ran malware, and
  ownership of their game or group was transferred. Roblox support was slow until press got involved.
  For an economy, a hijacked owner account means arbitrary server code and DataStore writes.
- **Open Cloud keys:** no public incident was found.

### 4. Executors (high level)
Hyperion caused paid Windows executors (incl. Synapse X) to stop sales in 2023. The 2024 community picture
is Mac/Android tools plus a few Windows tools, many of them scams or detected (low-quality sources). The
largest documented harm from 2024 to 2026 is **malware posing as executors**, which fuels account
takeover. I did not verify any claimed Synapse–Roblox partnership. No download links are recorded.

### 5. RMT and gambling
- The August 2023 class action names RBXFlip, Bloxflip and RBLXWild. Roblox denies the claims, and no
  outcome was found.
- February 2025: Roblox v. PlayerAuctions, built on trademark claims. Roblox's ToS forbid off-platform
  sale.
- Grow a Garden has an off-platform market (Calcalist).
- Hindenburg (October 2024) and the state AG suits (2025) are about child safety and metrics, not
  trading. They matter only because off-platform middleman and trading Discords are a contact vector.
- A third-party blog claims a stolen-item termination rule from 2026-11-01. It is unverified.

### 6. DevForum defensive consensus on dupe classes
1. **Stale-load race ("trade then rejoin before save" / server hop):** session-lock every profile.
   Use ProfileService or ProfileStore (loleris), or UpdateAsync with a stored session/job ID that refuses
   foreign writers. Have a lock expiry or force-steal policy (about 90s is debated).
   https://devforum.roblox.com/t/profilestore/3190543 , https://github.com/MadStudioRoblox/ProfileService ,
   https://devforum.roblox.com/t/datastore-session-locking/740302
2. **Cross-player trades are not atomic** (no multi-key UpdateAsync): use server-side escrow, a unique
   trade ID and record, commit both sides under session locks, and make it idempotent with
   reconciliation. Give items UUIDs. https://devforum.roblox.com/t/multikey-updateasync/38833 ,
   https://devforum.roblox.com/t/2620454
3. **Shutdown and teleport:** save and release before teleport. BindToClose waits about 30s, so run saves
   concurrently. Evidence for a direct teleport dupe is anecdotal.
   https://devforum.roblox.com/t/bindtoclose-data-loss-risk/135693
4. **Remote validation:** server-authoritative checks on type, range and argument count, rate limits,
   and no admin actions over remotes. https://devforum.roblox.com/t/making-games-more-secure/231579
5. **Purchases:** keep data in server memory and persist it on purchase. Official doc:
   https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing
6. **Remediation:** DataStore versioning (ListVersionsAsync, about 30 days) for per-key rollback. Add an
   append-only grant ledger so cleanup can be targeted (as in MM2 and PSX).
7. **Recovery:** a rollback must revert both sides of a trade (RBX-039).

## Searches that produced no reliable evidence
- PSX 2022 dupe that ended in a Huge-pet wipe. No primary source. Only SEO "how to dupe" pages and an incoherent itch.io devlog.
- Preston / BIG Games statement on a PS99 dupe or rollback. Nothing found. A PS99 Trading Plaza closure over a dupe: nothing found.
- Steal a Brainrot dupe or wipe: nothing reliable (chartlocal.com SEO pages ignored). Only the October 2025 Spyder Games copyright suit.
- Jailbreak vehicle dupe in 2024: nothing. Bee Swarm sticker or trade dupe: nothing. Royale High dupe or rollback: nothing.
- Blox Fruits dupe or Gamer Robot statement: nothing (only scam-related trade disables).
- Official Roblox statement on any catalog/UGC limited-serial duplication: nothing.
- "Roblox internal admin panel" Motherboard story from 2021: not found (the match is the 2020 one). 2019 support-abuse reports: not found.
- Roblox announcement of an official "Account Session Protection" or device binding: not found (SEO pages only).
- 2SV required for trading limiteds: not found. Official trade-hold policy page: not found.
- Leaked Roblox Open Cloud API key incident: not found.
- Checkmarx PyPI packages targeting Roblox: not found (npm only).
- 2024-2025 official Roblox DataStore data-loss incident report: not found.
- Synapse X / Roblox partnership confirmed by a primary source: not found.
- Eldorado/Etsy listings of Grow a Garden pets: not found.
