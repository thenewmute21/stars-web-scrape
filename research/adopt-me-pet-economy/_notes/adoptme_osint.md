# Adopt Me! OSINT evidence base (2017 to 2026-10-19)

Agent prefix: AM-. Ledger: `ledger_adoptme.csv` (52 rows, AM-001 to AM-052).

## Method and limits (read first)
- **Direct page fetching was not possible in this session.** WebFetch returned `getaddrinfo ENOTFOUND` for every domain (wikipedia, fandom, playadopt.me, devforum, pockettactics), web.archive.org was blocked, and curl through the egress proxy got `403 connect_rejected`. All evidence below comes from **WebSearch result titles and summaries**, not from pages I opened. Every ledger row says this in `link_checked_2026_10_19`.
- **Wayback (web.archive.org) was not reachable**, so the archive_url column is mostly empty.
- **Dates for X/Twitter posts** come from decoding the status-ID snowflake: `(id >> 22) + 1288834974657` ms. That is exact to the millisecond. The TikTok video ID date comes from `id >> 32` (Unix seconds).
- The WebSearch budget (shared across agents, 200 calls) ran out before I could run the BBC, Pocket Tactics free-pets and gifting queries.
- I did not download, open or run any scripts or executors. Script listings were read as search titles and descriptions only.

## 1. Legitimate pet routes without Robux (outcome B, n/a-intended-design)
- **Bucks:** earned from pet and baby care needs, the daily task board, the daily login reward track, job stands (Hot Dog and Lemonade), and the Money Tree (1,450 Bucks to buy, max 100 Bucks per 24h). Sources are guides only: commonsensegamer, mobilematters. (AM-005)
- **Eggs bought with Bucks:** Cracked ~350, Pet ~600, Royal ~1,450 Bucks. Legendary odds are about 1.5%, 3% and 8% (Pro Game Guides, Sportskeeda, robloxden; undated). Event eggs and ticket eggs also exist; for example, Aug 2026 Basic and Crystal eggs are listed at 0.25% and 5.9% legendary. (AM-004)
- **Starter Egg** from Sir Woofington (CharlieIntel). **Event currencies:** for example, Cherry Blossom 2025: Bakeneko 3,650 and Kage Crow 75,000 blossoms. **Promo codes** exist (low-quality sources). (AM-005, AM-007)
- **Neon:** 4 fully-grown pets of the same species make 1 Neon (added Jul 2019). **Mega Neon:** 4 Luminous Neons make 1 Mega Neon (added 2020-04-17). Fandom and guides agree. (AM-003)
- **Robux pets that can be traded:** Shadow Dragon (Halloween 2019, 1,000 R$) and Frost Dragon (Christmas 2019, 1,000 R$) can now only be obtained by trading. A non-payer can therefore legitimately own a Robux-origin pet. I found no source saying Robux pets are untradable. (AM-006)
- **Gifting** is allowed. Korea's 2020 restriction kept gifting while blocking trading (AM-015).

## 2. Trading system evolution
| Date | Change | Source quality |
|---|---|---|
| summer 2019 | Pets added; trading of pets, cars and toys appears from this period. **Exact trading launch date: no primary evidence found.** | Wikipedia + fan (AM-002) |
| 2019-06-07 | Official support defines a "duping glitch" and asks for reports (summary mentions a 20k Robux reward) | X @AdoptMeSupport (AM-013) |
| 2020-09-16 | Trading disabled for Korean players for legal compliance; gifting still allowed | NamuWiki / support summary (AM-015) |
| 2020-09-30 | Trading temporarily disabled because of a "serious trading bug which was causing items to disappear" | Official X (AM-016) |
| 2020-11-05 | **Trade License** quiz (3 scenarios) needed to trade Ultra-Rare and Legendary pets; **30-day trade history**; in-game scam reporting; **two-stage trade with fairness warning**; 9 trade slots; staff and influencer marks | Official playadopt.me news + Entertainment Focus (AM-019) |
| by 2023 | 18 trade slots | Bloxswaps guide |
| 2025-05 (tweet 2025-05-16) | **2-hour playtime restriction** before a new account can trade; Uplift says its tests show fewer scam reports | Official X (AM-035) |
| ~2025 | Help center: no reversal of accidental trades; item lock; anomaly-based automatic trade block ("assuming you may have duplicated your item") | Uplift Zendesk (AM-030, AM-031) |
| 2026-07-31 | **Trading Hub**: cross-server listings by Trading Phone; unlock needs ~2h playtime, Trade License and a Neon; listing costs 100 Bucks; listed pets **locked**; imbalance guardrail that is "not a true value system" | playadopt.me "Trading Hub Notes" + guides (AM-037) |
| 2026 | Roblox age checks: mandatory for chat from Jan 2026; Roblox help says an age check is required for *platform* (Limited items) trading. **No evidence found that Adopt Me in-game trading is gated by age check.** | (AM-038) |

Third-party value lists (adoptmevalues.app, adoptfrom.me, Elvebredd-type sites) are not official. Uplift says explicitly that the Hub guardrail is not a value system. One value-list site, "Adopt Me Trading Values", was breached in July 2022: 86.1k accounts per HIBP. (AM-027, AM-049)

## 3. Incidents: dupes, rollbacks, data loss, ban waves
**CONFIRMED (primary: official X posts, dates from status IDs):**
- **2020-04-22**: data loss "only affected 0.3% of our players, and the data lost was only up to 2 days"; affected players got an in-game message (status 1253042740524388352; follow-up 1253334125521469440). Cause not given. (AM-014)
- **2020-09-30**: trading disabled to investigate a "serious trading bug which was causing items to disappear" (1311101494939262977). Cause and re-enable date not found. Fan claims of a "blue dog dupe" or "admin panel hacked" are **UNVERIFIED (H)**. (AM-016, AM-017)
- **2020-10-20**: "Adopt Me has temporarily been turned private due to a critical bug with Roblox's Datastore Servers… your inventory will return to normal once the issue's been fixed." On 2020-10-21 a support form was offered for lost items. (AM-018)
- **2022-09-02**: "We rolled out a fix to remove duplicate items from clearly exploiting users - this shouldn't affect players who accidentally found the bug last night, or traded for duplicate pets." A player reply says a double-click on "claim" gave duplicates, which were later removed with a "suspicious activity" note. **This is the only primary-confirmed Adopt Me duplication incident found** (outcome D, historical-patched). Mechanism, scale and bans were not disclosed. (AM-024)
- **2022-10-24**: hacked-ticket intake closed "for the foreseeable future", with plans to re-evaluate policies and security methods. (AM-026)
- **2025-04-11**: ban wave for **Sakura Swoop** minigame exploiting, with a three-tier response (3-day bans; bans until Cherry Blossom currency can no longer be spent; a few permanent bans). Uplift said "We won't share our detection methods" and that currency caps had already been added. This is outcome C (inflated currency balance). A guide's event start date is the same day as the tweet, which is a small discrepancy. (AM-034)

**Official statements about dupes:** In ~2025 the Uplift Zendesk said "pet duplication is not possible within Adopt Me, and any methods of duplication found are almost immediately patched" (AM-029). This conflicts with the 2022 confirmed dupe; it is best read as "trade-window dupe offers are scams". The Zendesk "Bans" page admits automated anomaly detection for possibly duplicated items (AM-030).

**PLAUSIBLE / UNVERIFIED:**
- A community DevForum tutorial (~2022) names Adopt Me as hit by "a wide-spread duplication exploit using a rollback": save failures forced by malformed data, which reverts the save after a trade. It is not an Uplift statement. (AM-028)
- 2019 bounty of 20k Robux for a verifiable dupe; the amount comes from a single search summary. (AM-013)
- House-cloning glitch and script in 2025; fans report a partial patch ~July 2025. (AM-036)
- "Frost dupe" and "Shadow dupe" in 2020: an unsourced SEO article only. (AM-050)
- Sept 2026 DataStore errors: one player report. (AM-051)

**Roblox Oct 28-31 2021 outage:** Roblox said the cause was internal and there was no intrusion. **No evidence found of Adopt Me-specific pet loss or rollback.** (AM-023)

**No evidence found:** any Uplift or Roblox postmortem; any mass removal of "hacked pets" apart from the 2022-09-02 clawback; any 2023 or 2024 ban wave; any rollback of the whole game economy.

## 4. Scams (no operational detail)
- **Official guidance (help.playadopt.me, Uplift Zendesk):** hacked-account restoration happens once only, within 30 days, and requires proof that Roblox restored the account (AM-021). The May 2021 TikTok announced a 60-day window (AM-020). Cross-trading for Robux or cash, middlemen, and eBay or Facebook Marketplace buying are bannable (AM-032). Accidental trades are not reversed (AM-031). Players should check the verified Uplift group (AM-029).
- **Patterns** (Entertainment Focus 2020, GameRant, Parent Zone, Inven Global): trust trades, last-second swaps, fake middlemen, "I can clone your pet" offers, and staff or NPC impersonation (AM-044).
- **Pet generators and free-pet sites:** guides agree these are credential and cookie theft (AM-041). **No Uplift or Roblox statement specific to generators was found.**
- **"Beaming"** (session-cookie account takeover, often through Discord "verify" lures) (AM-042). Lookalike domains: adoptme.kr (registered 2026-07-30, flagged as phishing) and playingadopt.me (AM-043).
- **Real-money trading:** Wikipedia says rare pets sell for up to US$100-300 off-platform. Many shops exist (eldorado.gg, u7buy, bloxultra), all against Uplift's terms (AM-012).

## 5. Client-side "pet spawner" scripts
- The script listings describe themselves as **"visual" / "client-side"** pets for showcasing or recording. They are not in the server inventory and not visible to others (outcome **E**, STRONGLY CORROBORATED) (AM-039).
- Claims of "tradable spawner", "force accept" or "trade freeze" appear only in promotional YouTube and GitHub titles. Some distribute password-protected executables, which suggests malware or account-theft lures. Outcome **H**, UNVERIFIED (AM-040). A visual pet shown in a trade window is a fake-screenshot or social-engineering risk, not a real transfer.

## 6. Uplift company and security facts
- Founded as DreamCraft by NewFissy and Bethink; rebranded to Uplift Games on 2021-05-10. Self-funded; ~40 staff in 2021 (Vice: "four to 40 in less than two years"); the site and fandom say 60 (fandom: April 2026). Remote-first, US/UK. (AM-001, AM-010)
- Careers (2026-04-28): Gameplay and Senior Gameplay Engineer roles; earlier a Data Engineer and Head of Engineering (2022). **No security, anti-cheat or T&S role found.** (AM-047) In 2019 DevForum had a "Player Support Representatives, $25K/yr" posting.
- Anti-exploit statements: currency caps and a refusal to disclose detection (2025), anomaly-based trade blocks, and "dupes patched almost immediately".
- **Insider or backdoor:** no primary evidence. The only lead is fan speculation in Sept 2020 about an admin panel, kept as an **H hypothesis** (AM-017, AM-048).
- **Legal:** Impulse Communications v. Uplift Games et al., D.R.I. 1:24-cv-00166 (trademark; filed 2024-04-26; ruling 2024-12-23). Netherlands and Belgium access disabled from 2022-09-13 over loot boxes. **No FTC or regulator action on fraud or security found.** (AM-025, AM-045, AM-046)

## 7. Economy data
- Concurrent players: 440k (2019-06-15, fandom); 683,404 (Apr 2020, PC Gamer); 1.6-1.786M ("Dress Your Pets", 2020); **1.92M (Apr 2021, Ocean Egg; Uplift press release)**; Uplift careers page says 1.94M; ~100k average (Sept 2022, Wikipedia); 500-550k claimed for May 2026 (low-quality source). Visits: 40.8B (Nov 2025, Wikipedia); 43B+ sessions (Uplift 2026).
- Revenue: no audited figure; no Bloomberg or Forbes figure was found. Dubit via Kidscreen (2024-05-21) estimates >US$50M per year; Wikipedia says ~US$60M per year; other estimates span $19M-$500M.
- Rarity: legendary 1.5% / 3% / 8% (Cracked / Pet / Royal); 4x and 16x crafting multipliers.
- Inflation: only third-party value-list evidence (e.g., Frost Dragon low in Aug 2024, then about +130%). Neon trades at ~1.8x base against a 4x crafting cost. Evidence is weak.

## Year-by-year chronology
- **2017:** July release (DreamCraft). No evidence found of trading, dupes or incidents.
- **2018:** **No evidence found** (no searches returned 2018 Adopt Me security or economy events).
- **2019:** 2019-06-07 support "duping glitch" call and possible bounty (AM-013); 2019-06-15 440k CCU; summer: pets added, Neon (July); Oct and Dec: Shadow and Frost Dragon Robux event pets; a DevForum Player Support hiring post.
- **2020:** 2020-04-17 Mega Neon; 2020-04-22 data loss (0.3%, ≤2 days); Apr 683k CCU; Dress Your Pets record; 2020-05-26 press scam coverage; 2020-09-16 Korea trading off; 2020-09-30 trading disabled (items disappearing); 2020-10-20 game made private (Roblox datastore bug); 2020-11-05 Trade License, trade history and two-stage trade.
- **2021:** 2021-04-16 1.92M CCU; 2021-05-10 Uplift rebrand; 2021-05-31 hacked-restore policy (60 days); 2021-10-28..31 Roblox outage (**no Adopt Me-specific loss evidence**).
- **2022:** July: third-party value-site breach (86.1k); **2022-09-02 confirmed dupe clawback**; 2022-09-13 NL/BE shutdown; 2022-10-24 hacked tickets paused; ~2022 DevForum tutorial naming an Adopt Me rollback dupe.
- **2023:** 18 trade slots (guide). **No evidence found** of incidents or ban waves.
- **2024:** 2024-04-26 trademark suit; 2024-05 Dubit revenue estimate; 2024-12-23 court ruling. **No evidence found** of a dupe, rollback or ban wave.
- **2025:** 2025-02-10 HIBP adds the value-site breach; **2025-04-11 Sakura Swoop ban wave**; **2025-05-16 2-hour new-account trade restriction**; ~mid-2025 Uplift Zendesk help center (dupe denial, anomaly blocks, cross-trade rules); house-cloning glitch and scripts (fan reports, partial patch ~July); Nov: fan worries about Roblox age checks.
- **2026:** Jan: Roblox chat age checks; 2026-04-28 Uplift engineering hires; July: platform DataStore vulnerability report (not Adopt Me); 2026-07-30 adoptme.kr phishing domain; **2026-07-31 Trading Hub**; Aug: new ticket eggs; Sept: player report of DataStore errors; Oct: Halloween event. **No evidence found** of a 2026 dupe or rollback.

## Search query log
WebSearch only; WebFetch failed on every domain. Reliable means a primary or reputable source surfaced.
| Query (abridged) | Reliable evidence? |
|---|---|
| adopt me dupe glitch Uplift Games duped pets removed | No (SEO spam) |
| adopt me trading license introduced | Partial (fandom/guides; Trading Hub date) |
| Adopt Me Uplift Games Bloomberg revenue | No (trackers only) |
| Wikipedia release July 2017 / trading 2019 / CCU record | Yes (Wikipedia, Bloxy, playadopt.me) |
| 1.6 million concurrent / Fly Ride | Partial (PC Gamer, press release) |
| Uplift team size Bloomberg Polygon | Yes (Vice, MCV, uplift.games) |
| playadopt.me news hacked/duped pets statement | No |
| "Adopt Me" rollback servers pets lost Uplift statement | Yes (Uplift Zendesk dupe statement) |
| duplication exploit 2020 neon duped ban wave | Partial (Wikipedia Nov 2020; SEO claim) |
| upliftgames.zendesk scammed/hacked restore | Yes (TikTok official) |
| upliftgames.zendesk trade history report scammer | No |
| Nov 2020 anti-scam update trade license | **Yes** (playadopt.me official news) |
| help.playadopt.me hacked account restore | **Yes** (official help article) |
| site:playadopt.me news trade | No (index lacks domain) |
| site:playadopt.me scam OR exploiters | No |
| AdoptMeSupport hacked ticket closing 2022 | **Yes** (official X) |
| pet generator / free pets scam warning | Partial (guides; no official) |
| pets sold real money eBay / cross-trading | **Yes** (Uplift Zendesk) |
| zendesk Trading Problems / Trade Ban | **Yes** (Uplift Zendesk) |
| Trading Hub July 2026 | **Yes** (playadopt.me Trading Hub Notes) |
| trading age check Roblox 2025 2026 | Partial (Roblox help; nothing Adopt Me-specific) |
| NamuWiki controversies dupe hack rollback | Partial (DevForum tutorial lead) |
| zendesk "Free Pets" | No |
| zendesk "Dealing with a Scammed Account" | No (not re-surfaced) |
| pet spawner script visual only | Partial (vendor self-descriptions) |
| trade scam script trade freeze | No (promo titles only) |
| Roblox outage Oct 2021 Adopt Me data lost | Yes (outage); No (Adopt Me impact) |
| revenue Forbes/Bloomberg/BI | Partial (Kidscreen/Dubit) |
| BBC/Guardian/Verge children scammed | No (Parent Zone, Entertainment Focus only) |
| trading introduced 2019 Pets Update | No |
| Uplift careers anti-cheat/security | Partial (careers; no security roles) |
| pets disappeared inventory bug restored | No |
| Uplift lawsuit/court/regulator/FTC | **Yes** (govinfo D.R.I.) |
| PlayAdoptMe tweet exploiters banned | **Yes** (Sakura Swoop; 2h restriction) |
| restored pets untradable | No (anecdote) |
| Vice 100-person studio | Yes |
| trading temporarily disabled serious bug 2020 | **Yes** (official X) |
| Sakura Swoop ban wave April 2025 | No (guides only) |
| "2 hour playtime restriction" | No (re-search failed; original tweet found earlier) |
| dupe 2025/2026 house cloning | Partial (fan threads) |
| beaming cookie logger | Partial (parent guide) |
| legendary chance / neon / mega neon | Partial (guides) |
| Royal Egg 8% odds | Partial (guides) |
| earn bucks tasks paycheck daily login | Partial (guides) |
| Robux pets tradable Shadow/Bat Dragon | Partial (guides) |
| "1.94 million" concurrent | No (only 1.92M) |
| devforum Uplift exploit/security/datastore | Partial (community tutorial; player report) |
| "Trade Changes & Scam Prevention" quiz | Partial |
| "prevent exploiters from abusing data store rollbacks" | Partial (community tutorial) |
| TheGreatSage gist Adopt Me | Partial (led to datastore-private tweet) |
| devforum Sept 2026 datastore Adopt Me | No |
| "critical bug … Data Store" Adopt Me private | **Yes** (official X 2020-10-20) |
| game set private data loss 2020 | **Yes** (official X 2020-04-22) |
| HIBP Adopt Me Trading Values | **Yes** (HIBP) |
| April 2020 data loss 0.3% | **Yes** (official X) |
| NamuWiki problems controversies | Partial (Korea 2020-09-16) |
| PlayAdoptMe "duplicat" pets removed | **Yes** (official X 2022-09-02; 2019 support) |
| trading re-enabled Oct 2020 | No |
| Sept 2022 "remove duplicate items" | **Yes** (confirmation + player reply) |
| AdoptMeSupport 20k Robux reward | No (re-search failed) |
| Korea trading disabled Sept 2020 | Partial |
| Frost Dragon value history / value lists | Partial (third-party) |
| NL/BE loot boxes 2022 | **Yes** (PocketGamer.biz, Game Developer) |
| Dress Your Pets record | Partial (conflicting) |
| Trading Hub "not a true value system" | Partial |
| ban wave 2023/2024 | No (only 2025) |
| zendesk Trading Safety | No |
| fake Adopt Me copies / verified badge | Partial (domain scanners) |
| Uplift news 2025/2026 layoffs/acquisition | No (none found) |
| Roblox 2026 age check trading | Partial (Roblox help) |
| lock pets feature | Partial (Hub lock; Zendesk "lock items") |
| Neon / Mega Neon dates | Partial (fandom) |
| BBC Adopt Me scam; Starter Egg / gifting | **Not run** (search budget exhausted) |

Not done: "adopt me pet generator", "adopt me fake pet", "adopt me trade history" (standalone), "adopt me neon dupe" and "adopt me 2020 dupe" as exact strings; these were covered only partly by the combined queries above. Wayback lookups were blocked.

## Biggest gaps
1. Root causes of the 2020-09-30 trading bug and the 2022-09-02 dupe, and when trading was re-enabled in 2020.
2. Primary text of the 2019 dupe bounty, and whether a 2019-2020 dupe was ever confirmed.
3. Whether Adopt Me trading consults Roblox age checks (2026).
4. Whether hacked-restored pets are untradable, and whether trade reversals now trace downstream trades.
5. No primary or archived page verification at all, because fetch and Wayback were blocked. Re-fetch the official URLs before citing them externally.
