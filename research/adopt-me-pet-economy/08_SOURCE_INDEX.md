# 08 — Source Index, Search Coverage and Re-verification Queue

Compiled 2026-10-19 from `_notes/*.md` and `01_EVIDENCE_LEDGER.csv` (210 rows). No new web research was done. URLs are copied exactly from the ledger or notes; none were added.

## Verification basis (read first)

| Basis | Meaning | Rows |
|---|---|---|
| **docs-verified** | Quote checked verbatim against the official Roblox documentation source repo, `github.com/Roblox/creator-docs`, at commit **`70a0110fee0c0900103e545fcaee69a8bd2a942f`** (dated 2026-10-17, "update Open Source Docs from Roblox internal teams"). This repo is what create.roblox.com/docs renders. The create.roblox.com URL is the canonical citation. The GitHub blob under `https://github.com/Roblox/creator-docs/blob/70a0110fee0c0900103e545fcaee69a8bd2a942f/content/en-us/` is the archive. The live create.roblox.com site itself was **not** reachable | 60 (OFF-001..040 except OFF-041; IMP-001, 003–013, 015, 016, 021, 023, 025–028) |
| **snippet-only** | Seen only as a WebSearch result title or summary. The page was never opened, and `link_checked` failed (egress 403 / DNS ENOTFOUND). Quotes are search-summary text, not verified page text | 150 (all AM-, RBX-, ECO-; OFF-041; IMP-002, 014, 017–020, 022, 024, 029) |

**Confidence downgrade:** the post-mortem moved 40 snippet-only rows from CONFIRMED to STRONGLY CORROBORATED (SC). Their original value is in `confidence_pre_postmortem`:
- AM-: 014, 016, 018, 019, 020, 021, 023, 024, 025, 026, 027, 029, 030, 031, 032, 034, 035, 045
- RBX-: 005, 006, 007, 008, 015, 016, 017, 018, 019, 021, 042, 043, 044, 045, 048
- ECO-: 009, 012, 024, 025, 030, 034
- IMP-: 029

Where the underlying source is a first-party post (Uplift, Roblox, Valve, CCP, SEC filing, court record), this index labels it **"CONFIRMED by first-party post (snippet-only)"**.

**Snippet-only rows that point at create.roblox.com:** RBX-021, RBX-024, RBX-048, ECO-030 and OFF-041 cite create.roblox.com but were *not* checked against the repo. RBX-021 and RBX-048 cover the same pages as docs-verified OFF-035 and OFF-027/028. RBX-024 (Secrets Store) and ECO-030 (BanAsync) can be verified offline against creator-docs@70a0110 with no egress, so they are quick wins.

---

## 1. Roblox official documentation (creator-docs @ 70a0110)

| URL | Publisher | Supports (ledger IDs) | Basis |
|---|---|---|---|
| https://github.com/Roblox/creator-docs (commit 70a0110fee0c0900103e545fcaee69a8bd2a942f, 2026-10-17) | Roblox | Source of every docs-verified row | docs-verified |
| https://create.roblox.com/docs/reference/engine/classes/Workspace | Roblox Creator Docs | OFF-001 (FilteringEnabled discontinued) | docs-verified |
| https://create.roblox.com/docs/scripting/security/access-control | Roblox Creator Docs | OFF-002, OFF-010, IMP-021, IMP-023 (server-authoritative instances; decompilation; subplace access) | docs-verified |
| https://create.roblox.com/docs/scripting/security/security-tactics | Roblox Creator Docs | OFF-003, IMP-009 ("never trust the client"); OFF-041 (no Hyperion mention; that row is snippet-only, UNVERIFIED) | docs-verified (OFF-041 snippet-only) |
| https://create.roblox.com/docs/scripting/security/client-server-boundary | Roblox Creator Docs | OFF-004 (NaN trade offer), OFF-005 (trade+leave+failed-save dupe), OFF-006 (token bucket), OFF-007 (prompt/detector) | docs-verified |
| https://create.roblox.com/docs/scripting/security/network-ownership | Roblox Creator Docs | OFF-008 | docs-verified |
| https://create.roblox.com/docs/projects/server-authority | Roblox Creator Docs | OFF-009 (beta) | docs-verified |
| https://create.roblox.com/docs/reference/engine/classes/MarketplaceService | Roblox Creator Docs | OFF-011, 012, 013, 014, 015, 018, 019; IMP-013 | docs-verified |
| https://create.roblox.com/docs/production/monetization/robux-transfers | Roblox Creator Docs | OFF-016 | docs-verified |
| https://create.roblox.com/docs/production/monetization/passes | Roblox Creator Docs | OFF-017 | docs-verified |
| https://create.roblox.com/docs/production/monetization/subscriptions | Roblox Creator Docs | notes only (official_platform.md §2; no ledger row) | docs-verified (notes) |
| https://create.roblox.com/docs/cloud/webhooks/webhook-notifications | Roblox Creator Docs | OFF-020, OFF-021 | docs-verified |
| https://create.roblox.com/docs/reference/engine/classes/GlobalDataStore | Roblox Creator Docs | OFF-022, OFF-023 | docs-verified |
| https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits | Roblox Creator Docs | OFF-024 | docs-verified |
| https://create.roblox.com/docs/cloud-services/data-stores/versioning-listing-and-caching | Roblox Creator Docs | OFF-025, OFF-026 | docs-verified |
| https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing | Roblox Creator Docs | OFF-027, OFF-028 (verified); RBX-048 (snippet-only) | docs-verified / snippet-only |
| https://create.roblox.com/docs/cloud-services/data-stores | Roblox Creator Docs | IMP-010, IMP-011 | docs-verified |
| https://create.roblox.com/docs/cloud-services/memory-stores | Roblox Creator Docs | OFF-029 | docs-verified |
| https://create.roblox.com/docs/reference/engine/classes/MemoryStoreHashMap | Roblox Creator Docs | notes only (official_platform.md §3) | docs-verified (notes) |
| https://create.roblox.com/docs/reference/engine/classes/MessagingService | Roblox Creator Docs | OFF-030 | docs-verified |
| https://create.roblox.com/docs/cloud/auth/api-keys | Roblox Creator Docs | OFF-031, IMP-027 | docs-verified |
| https://create.roblox.com/docs/cloud/guides/secrets-store | Roblox Creator Docs | RBX-024 | **snippet-only** |
| https://create.roblox.com/docs/reference/engine/classes/InsertService | Roblox Creator Docs | OFF-032, IMP-006 | docs-verified |
| https://create.roblox.com/docs/reference/engine/classes/AssetService | Roblox Creator Docs | OFF-033, IMP-007 | docs-verified |
| https://create.roblox.com/docs/projects/assets/privacy | Roblox Creator Docs | OFF-034, IMP-005 (rules verified; launch date UNVERIFIED) | docs-verified |
| https://create.roblox.com/docs/scripting/security/third-party-vulnerabilities | Roblox Creator Docs | OFF-035, IMP-025 (verified); RBX-021 (snippet-only) | docs-verified / snippet-only |
| https://create.roblox.com/docs/reference/engine/classes/PolicyService | Roblox Creator Docs | OFF-036 | docs-verified |
| https://create.roblox.com/docs/production/monetization/paid-random-items | Roblox Creator Docs | OFF-037, OFF-038 | docs-verified |
| https://create.roblox.com/docs/reference/engine/classes/Player | Roblox Creator Docs | OFF-039 | docs-verified |
| https://create.roblox.com/docs/production/publishing/kids-and-select | Roblox Creator Docs | OFF-040 | docs-verified |
| https://create.roblox.com/docs/production/promotion/content-maturity | Roblox Creator Docs | notes only (official_platform.md §7) | docs-verified (notes) |
| https://create.roblox.com/docs/safety | Roblox Creator Docs | notes only (official_platform.md §6) | docs-verified (notes) |
| https://create.roblox.com/docs/projects/collaboration | Roblox Creator Docs | notes only (official_platform.md §4) | docs-verified (notes) |
| https://create.roblox.com/docs/physics/network-ownership | Roblox Creator Docs | notes only (official_platform.md §1) | docs-verified (notes) |
| https://create.roblox.com/docs/studio/properties ; https://create.roblox.com/docs/scripting/attributes ; https://create.roblox.com/docs/scripting/events/remote | Roblox Creator Docs | notes only (official_platform.md §1) | docs-verified (notes) |
| https://create.roblox.com/docs/reference/engine/classes/Players/BanAsync | Roblox Creator Docs | ECO-030 | **snippet-only** |
| https://create.roblox.com/docs/studio/importer | Roblox Creator Docs | IMP-001 | docs-verified |
| https://create.roblox.com/docs/cloud/guides/usage-assets | Roblox Creator Docs | IMP-003 | docs-verified |
| https://create.roblox.com/docs/projects/assets | Roblox Creator Docs | IMP-004 | docs-verified |
| https://create.roblox.com/docs/reference/engine/classes/EditableMesh | Roblox Creator Docs | IMP-008 (rules verified; Studio beta date from a snippet) | docs-verified |
| https://create.roblox.com/docs/projects/client-server | Roblox Creator Docs | IMP-012 | docs-verified |
| https://create.roblox.com/docs/marketplace/marketplace-fees-and-commissions | Roblox Creator Docs | IMP-015 | docs-verified |
| https://create.roblox.com/docs/projects/assets/in-experience-asset-creation | Roblox Creator Docs | IMP-016 | docs-verified |
| https://create.roblox.com/docs/projects/assets/packages | Roblox Creator Docs | IMP-026 | docs-verified |
| https://create.roblox.com/docs/cloud/guides/usage-place-publishing | Roblox Creator Docs | IMP-028 | docs-verified |

## 2. Roblox official, non-docs (newsroom, help center, about.roblox.com, SEC, staff DevForum posts)

All are snippet-only. These hosts were egress-blocked.

| URL | Publisher | Supports | Basis |
|---|---|---|---|
| https://about.roblox.com/newsroom/2022/01/roblox-return-to-service-10-28-10-31-2021 (secondary: https://www.infoworld.com/article/3648414/robloxs-cloud-native-catastrophe-a-post-mortem.html) | Roblox newsroom | RBX-008 (73-hour outage, Consul) | snippet-only; CONFIRMED by first-party post (snippet-only) |
| https://about.roblox.com/frauds-and-scams | Roblox | ECO-019 | snippet-only |
| https://en.help.roblox.com/hc/en-us/articles/203312390 | Roblox Help Center | ECO-018 (off-window deals not reversed) | snippet-only |
| https://en.help.roblox.com/hc/en-us/articles/203312650 | Roblox Help Center | ECO-026 (unauthorized charges) | snippet-only |
| https://en.help.roblox.com/hc/en-us/articles/203313310-Trading-System | Roblox Help Center | AM-038 (age check for platform trading) | snippet-only |
| https://www.sec.gov/Archives/edgar/data/1315098/000131509823000035/rblx-20221231.htm | Roblox Corp, FY2022 10-K | ECO-024 (chargebacks ≈3.16% of bookings) | snippet-only; CONFIRMED by first-party filing (snippet-only) |
| https://www.sec.gov/Archives/edgar/data/1315098/000131509826000024/rblx-20251231.htm | Roblox Corp, FY2025 10-K | ECO-025 | snippet-only; CONFIRMED by first-party filing (snippet-only) |
| https://devforum.roblox.com/t/welcoming-byfron-to-roblox/2018233 (secondary: https://piunikaweb.com/2023/04/28/roblox-byfron-anti-cheat-update-leaves-many-cheaters-worried/) | Roblox DevForum announcement; PiunikaWeb | RBX-011 | snippet-only |
| https://devforum.roblox.com/t/script-injection-vulnerability/221954 (secondary: https://devforum.roblox.com/t/how-to-detect-when-a-player-has-denied-script-injection-permission-on-a-plugin/1375400) | DevForum (staff reply per summary) | RBX-022 | snippet-only |

## 3. Uplift Games / Adopt Me! official

All are snippet-only. Dates for X posts were decoded from status-ID snowflakes (`(id >> 22) + 1288834974657` ms), which is exact. The TikTok date comes from `id >> 32`.

| URL | Publisher | Supports | Basis |
|---|---|---|---|
| https://x.com/AdoptMeSupport/status/1136864164314378240 | @AdoptMeSupport (2019-06-07) | AM-013 (duping-glitch definition; 20k R$ bounty in one summary only) | snippet-only |
| https://x.com/playadoptme/status/1253042740524388352 | @PlayAdoptMe (2020-04-22); follow-up status 1253334125521469440 | AM-014 (0.3% data loss) | CONFIRMED by first-party post (snippet-only) |
| https://x.com/PlayAdoptMe/status/1311101494939262977 | @PlayAdoptMe (2020-09-30) | AM-016 (trading disabled, items disappearing) | CONFIRMED by first-party post (snippet-only) |
| https://x.com/PlayAdoptMe/status/1318613836782620673 | @PlayAdoptMe (2020-10-20); follow-up status 1319019782788861956 | AM-018 (private over Roblox DataStore bug) | CONFIRMED by first-party post (snippet-only) |
| https://www.playadopt.me/news/trade-changes-and-scam-prevention-update | playadopt.me news (2020-11-05) | AM-019 (Trade License, 30-day history) | CONFIRMED by first-party post (snippet-only) |
| https://www.tiktok.com/@playadoptme/video/6968484968469236997 | @playadoptme TikTok (2021-05-31) | AM-020 (60-day hacked restore) | CONFIRMED by first-party post (snippet-only) |
| https://help.playadopt.me/hc/en-us/articles/360055530574-What-to-do-when-your-Account-is-Hacked | help.playadopt.me | AM-021 (once only, within 30 days) | CONFIRMED by first-party page (snippet-only) |
| https://x.com/PlayAdoptMe/status/1565618479293759489 | @PlayAdoptMe (2022-09-02) | **AM-024 (only confirmed dupe)** | CONFIRMED by first-party post (snippet-only) |
| https://x.com/AdoptMeSupport/status/1584620745673658371 | @AdoptMeSupport (2022-10-24) | AM-026 (hacked tickets closed) | CONFIRMED by first-party post (snippet-only) |
| https://upliftgames.zendesk.com/hc/en-us/articles/39529601838740-Dealing-with-a-Scammed-Account | Uplift Zendesk | AM-029 ("duplication is not possible") | CONFIRMED by first-party page (snippet-only) |
| https://upliftgames.zendesk.com/hc/en-us/articles/39526349517204-Bans | Uplift Zendesk | AM-030 (anomaly trade blocks) | CONFIRMED by first-party page (snippet-only) |
| https://upliftgames.zendesk.com/hc/en-us/articles/39521932900244-Trading-Problems | Uplift Zendesk | AM-031 | CONFIRMED by first-party page (snippet-only) |
| https://upliftgames.zendesk.com/hc/en-us/articles/39522252445972-Inappropriate-Trading-Conduct | Uplift Zendesk | AM-032 | CONFIRMED by first-party page (snippet-only) |
| https://x.com/PlayAdoptMe/status/1910695619816988944 | @PlayAdoptMe (2025-04-11) | AM-034 (Sakura Swoop ban wave) | CONFIRMED by first-party post (snippet-only) |
| https://x.com/PlayAdoptMe/status/1923171658430546299 | @PlayAdoptMe (2025-05-16) | AM-035 (2-hour trade gate) | CONFIRMED by first-party post (snippet-only) |
| https://www.playadopt.me/news/trading-hub-notes | playadopt.me (2026-07-31) | AM-037 (Trading Hub) | snippet-only (SC) |
| https://www.uplift.games/careers/gameplay-engineer | uplift.games | AM-047 (no security role found) | snippet-only (SC) |

Not official, but relays an Uplift press release: https://x.com/Bloxy_News/status/1383068710567485441 (AM-008, 1.92M CCU; press release via mynewsdesk; snippet-only).

## 4. Press, legal and regulatory

| URL | Publisher | Supports | Basis |
|---|---|---|---|
| https://vice.com/en/article/how-these-developers-hope-to-build-a-100-person-game-studio-inside-roblox | Vice | AM-010 | snippet-only |
| https://www.vice.com/en/article/88gd4a/roblox-beaming-hackers (secondary: https://it.slashdot.org/story/22/02/16/1555256/how-roblox-beamers-get-rich-stealing-from-children) | Motherboard/Vice | RBX-002, RBX-003, RBX-004, ECO-021, ECO-022 | snippet-only |
| https://boingboing.net/2020/05/04/roblox-hacker-got-100-mill.html | Boing Boing relaying Motherboard (Joseph Cox); SC Magazine | RBX-001 (2020 support-panel abuse) | snippet-only |
| https://www.pcgamer.com/au/this-roblox-game-about-adopting-pets-had-more-players-this-week-than-mount-and-blade-ii-bannerlord | PC Gamer | AM-009 | snippet-only |
| https://kidscreen.com/2024/05/21/adopt-me-digital-pets-move-from-roblox-to-the-toy-aisle/ | Kidscreen (Dubit estimate) | AM-011 | snippet-only |
| https://www.npr.org/2021/10/31/1050972129/the-video-game-platform-roblox-is-still-down-but-the-company-says-it-has-a-fix | NPR | AM-023 | snippet-only |
| https://www.pocketgamer.biz/news/79643/adopt-me-shuts-down-in-belgium-and-the-netherlands/ | PocketGamer.biz; Game Developer | AM-025 | snippet-only |
| https://entertainment-focus.com/2020/05/26/some-of-the-worst-scams-in-adopt-me-on-roblox/ | Entertainment Focus | AM-044 | snippet-only |
| https://www.ghacks.net/2023/07/20/roblox-data-leak/ (secondary: https://www.hackread.com/roblox-data-breach-developers-pii-data-stolen) | gHacks; Hackread | RBX-006 | snippet-only |
| https://www.bleepingcomputer.com/news/security/roblox-vendor-data-breach-exposes-dev-conference-attendee-info/ | BleepingComputer | RBX-007 | snippet-only |
| https://therecord.media/ukraine-police-detain-hackers-suspected-of-stealing-roblox-accounts (secondary: https://www.bleepingcomputer.com/news/security/hackers-arrested-for-hijacking-and-selling-610-000-roblox-accounts/amp/) | The Record; BleepingComputer | RBX-015 | snippet-only |
| https://404media.co/hackers-are-hijacking-entire-roblox-games-now | 404 Media | RBX-019 | snippet-only |
| https://itsfoss.com/news/roblox-linux-end/ (secondary: https://www.gamingonlinux.com/2024/02/we-can-probably-say-a-final-goodbye-to-roblox-on-linux-with-wine-soon/page=1) | It's FOSS; GamingOnLinux | RBX-012 | snippet-only |
| https://techcrunch.com/2023/08/18/roblox-children-gambling-class-action-lawsuit-robux/amp (secondary: https://www.rollingstone.com/culture/culture-news/roblox-child-gambling-lawsuit-1234808313/) | TechCrunch; Rolling Stone | RBX-042 | snippet-only |
| https://news.bloomberglaw.com/ip-law/roblox-sues-gamer-marketplace-over-sales-of-in-game-money-goods (secondary: https://localnewsmatters.org/2025/02/08/roblox-puts-its-virtual-currency-to-the-test-in-real-world-lawsuit-against-online-reseller-site/) | Bloomberg Law; Local News Matters | RBX-043 | snippet-only |
| https://gameworldobserver.com/2024/10/09/hindenburg-research-roblox-report-inflated-dau-child-safety | Game World Observer | RBX-044 | snippet-only |
| https://www.kwtx.com/2025/11/17/texas-sues-roblox-alleging-online-gaming-platform-endangers-children/ (secondary: https://www.wsmv.com/2025/08/15/state-attorney-general-sues-roblox-alleging-child-exploitation-safety-failures/) | KWTX; WSMV | RBX-045 | snippet-only |
| https://san.com/cc/get-your-kids-off-roblox-kentucky-ag-sues-platform-over-child-safety-concerns/ | SAN | ECO-036 | snippet-only |
| https://www.calcalistech.com/ctechnews/article/dj4lxef8r | Calcalist CTech | RBX-032 | snippet-only |
| https://www.pockettactics.com/roblox/blade-ball-10k-reward (secondary: https://www.levelup.com/en/news/roblox-will-give-you-a-10000-usd-prize-if-you-find-and-report-this-bug/) | Pocket Tactics; LevelUp | RBX-035 | snippet-only |
| https://www.sportskeeda.com/roblox-news/why-pet-gifting-disabled-grow-garden (secondary: https://roonby.com/2025/07/25/why-pet-gifting-is-disabled-in-grow-a-garden/) | Sportskeeda; roonby | RBX-031 | snippet-only |
| https://piunikaweb.com/2022/02/01/pet-simulator-x-unknown-error-when-trying-to-withdraw-gems-and-pets/ | PiunikaWeb | RBX-029 | snippet-only |
| https://gamerjournalist.com/pet-simulator-x-hell-update/ | Gamer Journalist (secondary relay) | RBX-028 | snippet-only |
| https://deltiasgaming.com/?p=189558 | Deltia's Gaming | RBX-033 | snippet-only |
| https://www.engadget.com/2019-10-30-csgo-fraud-loot-box-key-trades.html | Engadget (quoting Valve) | ECO-004 | snippet-only |
| https://www.gamingonlinux.com/2019/10/valve-ends-counter-strike-global-offensive-container-key-trading-and-selling/page=1/ | GamingOnLinux | ECO-005 | snippet-only |
| https://www.engadget.com/2013-09-17-diablo-iii-shutting-down-auction-houses-next-march.html | Engadget (Blizzard) | ECO-009 | CONFIRMED by first-party statement relayed (snippet-only) |
| https://lowyat.net/2015/84753/steam-introduces-trade-holds-protects-items-from-scammers | Lowyat (Valve) | ECO-001 | snippet-only |
| https://www.tweaktown.com/news/48903/77-000-steam-accounts-hacked-month-valve/index.html | TweakTown (Valve) | ECO-002 | snippet-only |
| https://www.pcworld.com/article/2851576/steam-thwarts-counter-strike-scammers-with-new-trade-reversal-system.html | PCWorld | ECO-011 | snippet-only |
| https://www.occrp.org/en/news/independent-credit-card-thieves-use-fortnite-to-launder-money | OCCRP (The Independent / Sixgill) | ECO-033 | snippet-only |
| https://www.govinfo.gov/content/pkg/USCOURTS-rid-1_24-cv-00166/pdf/USCOURTS-rid-1_24-cv-00166-0.pdf | US District Court D.R.I. (govinfo) | AM-045 | CONFIRMED by first-party court record (snippet-only) |
| https://www.hunton.com/privacy-and-cybersecurity-law-blog/ftc-announces-520-million-in-settlements-with-epic-games | Hunton (FTC v. Epic) | ECO-034 | snippet-only |
| https://www.skadden.com/insights/publications/2025/01/ftc-finalizes-long-awaited-child-online-privacy | Skadden (FTC COPPA) | ECO-035 | snippet-only |
| https://parentzone.org.uk/article/adopt-me | Parent Zone | AM-046 | snippet-only |

## 5. Other first-party game publishers (comparables)

| URL | Publisher | Supports | Basis |
|---|---|---|---|
| https://store.steampowered.com/oldnews/20631 | Valve | ECO-003 (15-day holds) | snippet-only |
| https://steamcommunity.com/discussions/forum/0/4843149419125509891/ | Steam forum quoting Valve | ECO-010 | snippet-only |
| https://www.eveonline.com/news/view/monthly-economic-report-november-2024 | CCP Games | ECO-012 | CONFIRMED by first-party post (snippet-only) |

## 6. Security vendors and breach trackers

| URL | Publisher | Supports | Basis |
|---|---|---|---|
| https://www.malwarebytes.com/blog/news/2022/07/roblox-breached-internal-documents-posted-online-by-unknown-attackers | Malwarebytes | RBX-005 | snippet-only |
| https://www.malwarebytes.com/blog/scams/2026/06/roblox-developers-are-losing-entire-games-to-malware-attacks | Malwarebytes | RBX-019 (secondary) | snippet-only |
| https://www.sonatype.com/blog/fake-npm-roblox-api-package-installs-ransomware-spooky-surprise (secondary: https://thehackernews.com/2021/10/malicious-npm-libraries-caught.html) | Sonatype; The Hacker News | RBX-016 | snippet-only |
| https://reversinglabs.com/blog/fake-roblox-api-packages-luna-grabber-npm (secondary: https://thehackernews.com/2023/08/over-dozen-malicious-npm-packages.html) | ReversingLabs; THN | RBX-017 | snippet-only |
| https://checkmarx.com/blog/year-long-campaign-of-malicious-npm-packages-targeting-roblox-users.md (secondary: https://thehackernews.com/2024/09/malicious-npm-packages-mimicking.html) | Checkmarx; THN | RBX-018 | snippet-only |
| https://www.scworld.com/brief/fake-roblox-xeno-executor-installers-distribute-malware | SC Media (Bitdefender); ANY.RUN | RBX-014 | snippet-only |
| https://blog.talosintelligence.com/roblox-scam-overview/ | Cisco Talos | ECO-020 | snippet-only |
| https://haveibeenpwned.com/Breach/AdoptMeTradingValues | Have I Been Pwned | AM-027 | snippet-only |
| https://haveibeenpwned.com/Breach/RobloxDeveloperConference2024 | Have I Been Pwned | RBX-007 (secondary) | snippet-only |
| https://www.urlert.com/domains/adoptme.kr | urlert.com; Gridinsoft | AM-043, IMP-019 | snippet-only |
| https://www.superawesome.com/?p=17913 (secondary: https://devforum.roblox.com/t/how-to-award-ugc-limiteds-ingame/2500187) | SuperAwesome; DevForum | RBX-036 | snippet-only |

## 7. DevForum and developer community

These are class evidence or user reports, not Roblox or Uplift statements unless noted. All are snippet-only.

| URL | What it is | Supports |
|---|---|---|
| https://devforum.roblox.com/t/exploiting-how-to-prevent-exploiters-from-abusing-data-store-rollbacks-and-sanitizing-against-data-store-vulnerabilities/2019989 (gist: https://gist.github.com/TheGreatSageEqualToHeaven/e0e1dc2698307c93f6013b9825705899) | Community tutorial naming an Adopt Me! rollback dupe | AM-028 |
| https://devforum.roblox.com/t/datastore-on-games-etc-erlc-adopt-me/4852475 | Player bug report (Sept 2026) | AM-051 |
| https://devforum.roblox.com/t/platform-vulnerability-allowing-server-side-execution-and-datastore-modification/4766625 | Bug report (July 2026) | AM-052 |
| https://devforum.roblox.com/t/my-games-were-stolen-and-now-8500-usd-is-not-eligible-for-devex/4773705 | User post | RBX-020 |
| https://devforum.roblox.com/t/solved-the-word-require-made-any-model-not-distributed-on-creator-store/4051504 | User post | RBX-023 |
| https://devforum.roblox.com/t/virus-affecting-scripts/3045755 | Thread (archive for RBX-021) | RBX-021 |
| https://devforum.roblox.com/t/ugc-item-exploit-issue/4691750 | User post | RBX-037 |
| https://devforum.roblox.com/t/roblox-hat-duplication-bug/412384 | User post | RBX-038 |
| https://devforum.roblox.com/t/traders-on-roblox-are-reportedly-abusing-rollbacks/4820634 | User bug report | RBX-039, ECO-028 |
| https://devforum.roblox.com/t/combatting-account-theft/1645586 | Community post | RBX-040 |
| https://devforum.roblox.com/t/one-time-restoration/122309 | User post (2018) | ECO-029 |
| https://devforum.roblox.com/t/profilestore/3190543 ; https://github.com/MadStudioRoblox/ProfileService | Session-locking libraries (loleris / MadStudio) | RBX-046 |
| https://devforum.roblox.com/t/datastore-session-locking/740302 ; https://devforum.roblox.com/t/2620454 | Session lock / trade escrow threads | notes only (roblox_wide_incidents.md §6) |
| https://devforum.roblox.com/t/multikey-updateasync/38833 | Feature request | RBX-047 |
| https://devforum.roblox.com/t/bindtoclose-data-loss-risk/135693 (also https://devforum.roblox.com/t/bindtoclose-does-not-fire-on-reserved-server/2577701) | Data-loss threads | RBX-049 |
| https://devforum.roblox.com/t/roblox-data-rollback/3253350 | Versioning rollback thread | RBX-050 |
| https://devforum.roblox.com/t/making-games-more-secure/231579 | Remote validation consensus | RBX-052 |
| https://devforum.roblox.com/t/2231529 ; https://noblox.js.org/tutorial-Authentication.html | IP-bound cookie threads; noblox.js docs | RBX-010, ECO-023 |
| https://devforum.roblox.com/t/theft-of-game-content-using-saveinstance/3050674 | saveinstance thread | IMP-022 |
| https://devforum.roblox.com/t/3d-import-recap-aug-oct/2701407 | 3D Import Recap (2023) | IMP-002 (archive) |
| DevForum thread IDs cited without slug in the notes: t/2979668 (3D Import Recap Mar–Apr 2024), t/2057539 (3D Importer full release), t/3905928 (glTF export beta), t/3641687 (Expanded Sharing for Assets), t/1701697 (audio privacy), t/2725284 (Mesh & Image APIs beta), t/4779401 (EditableMesh batching beta), t/3753671 and t/4138945 (BanAsync alt-detection bypass) | Announcements and threads | notes only (asset_import.md, economy_social.md); no ledger rows except IMP-002 and IMP-008 context |
| https://lr.sudovanilla.org/r/robloxhackers/comments/1f4y9w7/what_the_happened_exactly | Reddit mirror (low quality) | RBX-013 |
| https://www.reddit.com/r/AdoptMeTradingRoblox/wiki/commonscams | Subreddit wiki | ECO-015 |

## 8. Wikis, guides and other third-party sites

All are snippet-only and serve as corroboration only.

| URL | Publisher | Supports |
|---|---|---|
| https://en.wikipedia.org/wiki/Adopt_Me! | Wikipedia | AM-001, AM-002, AM-012, ECO-013 |
| https://en.namu.wiki/w/%EC%9E%85%EC%96%91%ED%95%98%EC%84%B8%EC%9A%94!/%EB%85%BC%EB%9E%80%20%EB%B0%8F%20%EC%82%AC%EA%B1%B4%20%EC%82%AC%EA%B3%A0 | NamuWiki | AM-015 |
| https://adoptme.fandom.com/f/p/4400000000001405298 | Adopt Me fandom discussion | AM-017 |
| https://adoptme.fandom.com/f/p/4400000000007938025 | Adopt Me fandom discussion | AM-036 |
| https://adoptme.fandom.com/wiki/Safety_Hub | Adopt Me fandom wiki | IMP-018, IMP-019 |
| https://adoptme.fandom.com/wiki/Trade_License | Adopt Me fandom wiki | ECO-014 |
| https://murder-mystery-2.fandom.com/wiki/The_Duping_Glitch_(2017) ; https://murder-mystery-2.fandom.com/wiki/The_Icewing_Glitch_(2018-2019) ; https://murder-mystery-2.fandom.com/wiki/The_Duping_Glitch_(2022) | MM2 fandom wiki | RBX-025, RBX-026, RBX-027 |
| https://roblox.fandom.com/wiki/BIG_Games_Pets/Pet_Simulator_X | Roblox fandom wiki | RBX-030 |
| https://runescape.wiki/w/Update:Wilderness_and_Free_Trade_Vote ; https://runescape.wiki/w/Trade | RuneScape Wiki | ECO-006, ECO-007, ECO-008 |
| https://www.khronos.org/news/permalink/roblox-announces-3d-importer-support-for-gltf-files-beta | Khronos Group | IMP-002 |
| https://progameguides.com/roblox/how-to-make-a-neon-pet-in-adopt-me ; https://progameguides.com/roblox/rarest-eggs-in-roblox-adopt-me/ ; https://progameguides.com/roblox/is-starpets-gg-real-or-a-scam-roblox/ | Pro Game Guides | AM-003, AM-004, ECO-032 |
| https://www.charlieintel.com/games/how-to-get-free-pets-in-adopt-me-206128/ | CharlieIntel | AM-005 |
| https://sportskeeda.com/roblox-news/how-get-shadow-dragon-in-roblox-adopt-me ; https://www.sportskeeda.com/roblox-news/adopt-me-sakura-swoop-guide | Sportskeeda | AM-006, AM-007 |
| https://www.gfinityesports.com/roblox/adopt-me-trade-values | Gfinity | ECO-017 |
| https://rowatcher.com/news/adopt-me-trading-values-in-2026-pet-economics-rising-legendaries-scam-prevention | rowatcher (low authority) | ECO-016 |
| https://www.adoptmevalues.app/values/frost-dragon | Value list (non-official) | AM-049 |
| https://pixeltwelve.com/articles/adopt-me-trade-license-safe-trading-guide | Pixeltwelve | AM-033 |
| https://adopt-me.click/safety/scams/ | Fan safety guide | AM-041 |
| https://screenwiseapp.com/guides/roblox-scams-how-kids-get-tricked-out-of-their-accounts | Screenwise parent guide | AM-042 |
| https://marix.app/library/games/adopt-me-scam-methods-list | marix.app (low authority) | IMP-020 |
| https://imperial-beard.fr/dupe-adopt/ | French SEO article (H claim only) | AM-050 |
| https://www.tiktok.com/discover/tutorial-on-how-to-contact-adopt-me-and-get-all-your-pets-back-when-you-het-hacked | TikTok player posts | AM-022 |
| https://allthings.how/roblox-error-9007-service-instances-unavailable-explained/ | allthings.how | RBX-009 |
| https://techwiser.com/roblox-terms-of-service-rules/ | TechWiser | RBX-041 |
| https://www.creation.dev/learn/can-you-refund-robux | creation.dev | ECO-027 |
| https://roonby.com/2025/09/05/why-cant-you-trade-in-blox-fruits-right-now/ | roonby (low quality) | RBX-034 |
| https://rscripts.net/script/adopt-me-visual-pet-spawner-VkFo | Script listing: **title and description only, not opened, nothing downloaded** | AM-039 |
| https://www.youtube.com/watch?v=335Rr2jtta8 | Promotional YouTube title; **not opened** | AM-040 |

## 9. Excluded domains (not used as evidence)

| Domain | Reason |
|---|---|
| `*.wizehire.com`, `cannacompanionusa.com`, `monitoring.toky.co`, `smtp.compagnie-des-sens.fr` / `compagnie-des-sens.fr` | SEO-spam mirrors carrying "free pets / dupe / script" content (economy_social.md, asset_import.md) |
| `nwww.arktimes.com`, `worker-monitor.api.hlthd.tsl.io`, `rustdesk.crownring.com` | SEO-spam mirrors (asset_import.md). **Conflict:** economy_social.md cites "arktimes" for the fake-middleman pattern; treat as low authority |
| `chartlocal.com` | SEO pages on Steal a Brainrot dupes (roblox_wide_incidents.md) |
| itch.io devlog (incoherent) and SEO "how to dupe" pages | Returned for the PSX Huge-wipe query; unusable |
| GitHub script listings, executor download pages, password-protected executables | Safety rule: not opened or linked; the names in AM-040 count as an H signal only |
| All "Adopt Me fake pets / duplicator / steal script" spam results | Recorded as the negative-quality signal IMP-029 |

---

## 10. Search coverage by prompt category (1–14)

Categories are the 14 from section 3 of the research prompt (labels abbreviated). [V] = docs-verified; all other IDs are snippet-only.

| # | Prompt category (verbatim scope) | Coverage | Strongest support | Main gap |
|---|---|---|---|---|
| 1 | Official free/earned pets, eggs, tasks, logins, events, promotions, referrals, gifts, codes | Partial | AM-002..007, ECO-017 (guides, snippet-only) | No first-party economy page; gifting / Starter Egg / promo-code queries never run |
| 2 | Trading, gifts, multi-account transfers, cross-server, resellers, account sales, RMT | Covered | AM-019, AM-035, AM-037; ECO-016, ECO-024..026; OFF Robux-transfer rows | Roblox ToS RMT text unread; third-party marketplace volumes unknown |
| 3 | Trade state-machine flaws (concurrency, cancel timing, disconnect, rejoin, partial commit, migration) | Covered (platform) / Partial (Adopt Me!) | OFF-022..030 [V]; RBX-046..050; AM-016, AM-024 | No published Adopt Me! root cause for 2020 trading bug or 2022 dupe |
| 4 | Inventory/data persistence faults (UpdateAsync, session locks, NaN, overflow, migration, DR) | Covered | OFF-022..030 [V] incl. NaN trade example; RBX-046..050 | No official multi-key transaction (absence by grep); version history is not an audit log |
| 5 | Shop and entitlement logic, receipts, refunds, game pass vs dev product | Covered | OFF-011..021, OFF-028 [V]; ECO-024 | Receipt redelivery timing and BindReceiptHandler concurrency undocumented |
| 6 | RemoteEvents/RemoteFunctions access control, validation, rate limiting, replay | Covered (platform docs) | OFF-001..010 [V] | No platform remote rate limit documented; no Adopt Me!-specific remote incident found |
| 7 | Asset-model cloning vs genuine acquisition | Covered | IMP-001..016 [V]; OFF-032..034 [V]; see 04 | glTF / asset-privacy launch dates unverified |
| 8 | Creator/admin/support powers, debug flags, staging leakage, plugins, backdoored models, supply chain | Covered (platform) / No evidence (Adopt Me!) | RBX-001, RBX-005, RBX-016..023; OFF-031, OFF-035; IMP-025..028 [V] | No Uplift insider/backdoor evidence (AM-048); no Open Cloud key incident (RBX-024) |
| 9 | Bots, AFK/macro farming, account farms, referral/promo farming, cap bypass | Partial | AM-034 (2025 event-currency ban wave); ECO bot rows | No Uplift statement on alts/AFK farming; detection methods withheld |
| 10 | Social engineering, phishing, session theft, impersonation, support-restoration abuse | Covered | RBX-003, 014, 015; ECO-018..023, ECO-028; AM-020, 021, 041..044 | One-sided rollback abuse is user-reported only (UNVERIFIED) |
| 11 | Dupe / pet-generator claims across video, Discord, GitHub, DevForum, Reddit | Partial | AM-039 (listings say client-only); IMP-017..020, IMP-029 | YouTube/Reddit debunks not found; spam domains excluded |
| 12 | Monetization/economy design mistakes (stacking, resale, tradable paid items, alts) | Partial | ECO-001..017; OFF paid-random-item / IsPaidItemTradingAllowed rows [V] | No audited revenue; inflation evidence weak (AM-049) |
| 13 | Platform/ops realities (outages, retries, latency, legacy, support overrides) | Partial | RBX outage rows (Oct 2021); AM-014, AM-018 (2020 incidents); OFF MemoryStore/Messaging rows [V] | No Adopt Me!-specific 2021-outage impact evidence |
| 14 | New/historically patched classes (first seen / last verified / remediation) | Partial | 02 timeline; RBX-025..035 other-game dupes (mostly secondary) | No developer primary for PSX/PS99/Jailbreak/Bee Swarm/Royale High/Blox Fruits (RBX-051) |

## 11. Queries that returned no reliable evidence (consolidated)

**Adopt Me!** (adoptme_osint.md, asset_import.md, economy_social.md):
- "adopt me dupe glitch Uplift Games duped pets removed" (SEO spam only)
- "Adopt Me Uplift Games Bloomberg revenue" (trackers only)
- "playadopt.me news hacked/duped pets statement"; "site:playadopt.me news trade"; "site:playadopt.me scam OR exploiters" (domain not indexed)
- "upliftgames.zendesk trade history report scammer"; zendesk "Free Pets"; zendesk "Dealing with a Scammed Account" (not re-surfaced); zendesk "Trading Safety"
- "trading introduced 2019 Pets Update"; "trading re-enabled Oct 2020"
- "BBC/Guardian/Verge children scammed" (only Parent Zone and Entertainment Focus)
- "pets disappeared inventory bug restored"; "restored pets untradable" (anecdote)
- "Sakura Swoop ban wave April 2025" (guides only); "2 hour playtime restriction" re-search; "AdoptMeSupport 20k Robux reward" re-search
- "1.94 million concurrent" (only 1.92M)
- "devforum Sept 2026 datastore Adopt Me"
- "ban wave 2023/2024" (only 2025)
- "Uplift news 2025/2026 layoffs/acquisition"
- "trade scam script trade freeze" (promo titles only)
- Adopt Me! player pet-import / UGC pets; developer test pets leaking; a Reddit client-side fake-pet video; named YouTube debunk videos; an official Uplift fake-pet debunk
- Uplift help-center pages on trade-window timing, restoration, bots or alts; Adopt Me! bot, alt or referral farming

**Roblox-wide and other games** (roblox_wide_incidents.md):
- PSX 2022 Huge-pet wipe; Preston / BIG Games statement on a PS99 dupe; PS99 Trading Plaza dupe closure; BIG Games account-age trade gate
- Steal a Brainrot dupe or wipe; Jailbreak 2024 vehicle dupe; Bee Swarm sticker or trade dupe; Royale High dupe; Blox Fruits dupe or Gamer Robot statement
- Official Roblox statement on catalog / UGC limited-serial duplication
- Motherboard "Roblox internal admin panel" 2021; 2019 support-abuse reports
- Official "Account Session Protection" or device binding; 2SV required for trading limiteds; official trade-hold policy page
- Leaked Open Cloud API key incident; Checkmarx PyPI packages targeting Roblox
- Official 2024–2025 Roblox DataStore data-loss incident report
- Synapse X / Roblox partnership from a primary source
- Eldorado or Etsy listings of Grow a Garden pets

**Economy and industry** (economy_social.md):
- Primary source on Roblox chargeback negative-balance mechanics
- 2018 Kotaku/Ubisoft "R6 trading disabled for laundering"
- GDC Vault talks (search engine did not surface them)
- FTC consumer alert specific to Roblox
- Roblox Community Standards wording on RMT and account sales (verbatim)

## 12. Research limitations

| Limitation | Detail |
|---|---|
| Egress block | Proxy 403 (CONNECT rejected) or DNS ENOTFOUND for: **create.roblox.com**, **devforum.roblox.com**, **en.help.roblox.com**, about.roblox.com, corp.roblox.com, www.roblox.com, **web.archive.org**, wikipedia.org, adoptme.fandom.com, playadopt.me, pockettactics.com, engadget.com, store.steampowered.com, khronos.org and other **press sites**. No page in the ledger was opened |
| Archive | Wayback was unreachable, so `archive_url` is mostly empty. Where filled, it holds a secondary outlet or the creator-docs blob, not an archive snapshot |
| Search budget | The shared 200-call WebSearch budget ran out. The OFF- agent ran **zero** searches. The AM- agent stopped before several planned queries |
| Docs workaround | Official docs were verified from the creator-docs GitHub repo, not the live site. Change dates are repo commit dates; history starts 2023-08-29 |
| Date sources | X dates come from snowflake decoding, which is exact. Most other dates come from search summaries |
| Circularity | Wikipedia, fandom and guides may relay each other. Pre-mortem rule #15 (trace to the origin) could not be applied without opening pages |

**Queries never run:**
- BBC Adopt Me! scam coverage
- Pocket Tactics free-pets coverage
- Gifting and Starter Egg
- "adopt me pet generator", "adopt me fake pet", "adopt me trade history" (standalone), "adopt me neon dupe" and "adopt me 2020 dupe" as exact strings; these were covered only partly by combined queries
- Hyperion/Byfron official dates, FilteringEnabled 2018, age-check and trading announcements, Robux transfers / BindReceiptHandler announcement posts (OFF- agent had no budget)
- GDC Vault direct search
- All Wayback lookups

## 13. Re-verification queue (top 25 snippet-only claims, highest impact first)

Re-open each URL, confirm the quote and date, then archive it. If the row is confirmed against the live page, restore CONFIRMED where `confidence_pre_postmortem` says so.

| Rank | Ledger | Claim to re-check | URL to open first | Why it matters |
|---|---|---|---|---|
| 1 | AM-024 | 2022-09-02 dupe-removal wording and the player reply about a double-click on "claim" | https://x.com/PlayAdoptMe/status/1565618479293759489 | The only confirmed Adopt Me! dupe; anchors the D-class narrative |
| 2 | AM-029 | "pet duplication is not possible…" wording and page date | https://upliftgames.zendesk.com/hc/en-us/articles/39529601838740-Dealing-with-a-Scammed-Account | The central contradiction in the timeline |
| 3 | AM-030 | Anomaly-based trade block text ("assuming you may have duplicated your item") | https://upliftgames.zendesk.com/hc/en-us/articles/39526349517204-Bans | Evidence that Uplift runs dupe detection |
| 4 | AM-016 | 2020-09-30 "items to disappear" text; any follow-up on cause or re-enable | https://x.com/PlayAdoptMe/status/1311101494939262977 | Second-largest Adopt Me! incident; re-enable date still unknown |
| 5 | AM-034 | Sakura Swoop tiers, currency caps, the "won't share detection" quote; event-date discrepancy | https://x.com/PlayAdoptMe/status/1910695619816988944 | The only confirmed C-class (inflated balance) event |
| 6 | AM-014 | 0.3% / 2-day data loss | https://x.com/playadoptme/status/1253042740524388352 | Loss-scale baseline |
| 7 | AM-018 | "critical bug with Roblox's Datastore Servers"; 2020-10-21 support form | https://x.com/PlayAdoptMe/status/1318613836782620673 | Attributes cause to the platform |
| 8 | AM-019 | Trade License scope (Ultra-Rare / Legendary), 30-day history, two-stage trade | https://www.playadopt.me/news/trade-changes-and-scam-prevention-update | Core control design reference |
| 9 | AM-037 | Trading Hub unlock rules, listing lock, "not a true value system" | https://www.playadopt.me/news/trading-hub-notes | Newest control (2026); cross-server design |
| 10 | AM-035 | 2-hour new-account trade gate; claimed fall in scam reports | https://x.com/PlayAdoptMe/status/1923171658430546299 | Evidence for an account-age gate |
| 11 | AM-013 | 2019 duping-glitch definition and the 20k Robux bounty | https://x.com/AdoptMeSupport/status/1136864164314378240 | The bounty amount rests on a single summary |
| 12 | AM-021 / AM-020 | Restore policy: 30 days and once only vs 60 days (2021) | https://help.playadopt.me/hc/en-us/articles/360055530574-What-to-do-when-your-Account-is-Hacked | Recovery-policy design (G) |
| 13 | AM-026 | Hacked-ticket intake closed 2022-10-24; whether it reopened | https://x.com/AdoptMeSupport/status/1584620745673658371 | Support-capacity signal |
| 14 | AM-028 | Exact DevForum text naming the Adopt Me! rollback dupe and its date | https://devforum.roblox.com/t/exploiting-how-to-prevent-exploiters-from-abusing-data-store-rollbacks-and-sanitizing-against-data-store-vulnerabilities/2019989 | Possible second dupe; currently PLAUSIBLE |
| 15 | AM-038 | Whether Roblox age checks gate trading, and the scope (Limiteds only?) | https://en.help.roblox.com/hc/en-us/articles/203313310-Trading-System | Child-safety gating decision |
| 16 | RBX-001 | 2020 support-panel capabilities (grant currency, remove 2FA) and Roblox's "small number" statement | https://boingboing.net/2020/05/04/roblox-hacker-got-100-mill.html | The primary precedent that admin paths can mint items |
| 17 | RBX-039 / ECO-028 | One-sided rollback abuse report and Roblox's response | https://devforum.roblox.com/t/traders-on-roblox-are-reportedly-abusing-rollbacks/4820634 | Drives the "reverse both sides" recovery design |
| 18 | RBX-008 | Outage root cause and the "no data loss" statement | https://about.roblox.com/newsroom/2022/01/roblox-return-to-service-10-28-10-31-2021 | First-party platform postmortem |
| 19 | RBX-031 | Grow a Garden gifting disable, dupe mechanism, failed first fix | https://www.sportskeeda.com/roblox-news/why-pet-gifting-disabled-grow-garden | Closest modern pet-dupe analogue |
| 20 | ECO-024 | 3.16%-of-bookings chargeback figure, verbatim | https://www.sec.gov/Archives/edgar/data/1315098/000131509823000035/rblx-20221231.htm | Quantifies the stolen-card laundering risk |
| 21 | ECO-011 | CS2 Trade Protection: reverse-all scope and 30-day cooldown | https://www.pcworld.com/article/2851576/steam-thwarts-counter-strike-scammers-with-new-trade-reversal-system.html | Recovery-design template |
| 22 | ECO-030 | BanAsync alt propagation default | https://create.roblox.com/docs/reference/engine/classes/Players/BanAsync (verifiable offline in creator-docs@70a0110) | Quick win; used in the architecture |
| 23 | RBX-021 / RBX-024 | Backdoor require(assetId) guidance; Secrets Store | https://create.roblox.com/docs/cloud/guides/secrets-store (verifiable offline in creator-docs@70a0110) | Quick win; supply-chain controls |
| 24 | RBX-011 / OFF-041 | Byfron acquisition and Hyperion ship dates from an official post | https://devforum.roblox.com/t/welcoming-byfron-to-roblox/2018233 | Currently unverified from official sources |
| 25 | RBX-041 | Claimed 2026-11-01 stolen-item termination policy | https://techwiser.com/roblox-terms-of-service-rules/ (then locate the Roblox primary source) | Takes effect within two weeks of this report, if real |

Also worth doing if budget allows: AM-008 (1.92M vs 1.94M), AM-025 (NL/BE date), AM-045 (court docket), RBX-006 and RBX-007 (HIBP breach dates), and the FilteringEnabled mandatory date (OFF-001).
