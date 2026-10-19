# Follow-up verification: Adopt Me! high-impact claims (2026-10-19)

**Scope:** a targeted post-mortem follow-up on the re-verification queue in `08_SOURCE_INDEX.md` §13, plus queries that were never run.

**Method:** WebSearch only. Page fetching was blocked, so **no page was opened**. Every item below is a search result title or a search-tool summary, so nothing is upgraded to CONFIRMED.

**Dates:** dates marked "(snowflake)" are decoded from X status IDs: `(id>>22)+1288834974657` ms gives UTC. TikTok IDs are decoded as `id>>32` seconds.

**Budget:** 38 of the 40-search cap were used. Two calls returned API 400 because the domain filter included blocked domains (bbc.co.uk/bbc.com, polygon.com, theverge.com and gamesindustry.biz in one call; reddit.com in another). The remaining 36 returned results.

**Proposed edits** are in `_notes/followup_ledger_changes.csv` (17 field changes) and `_notes/followup_new_rows.csv` (8 FU- rows). `01_EVIDENCE_LEDGER.csv` was not edited.

## Excluded sources (SEO spam, script-promo or scraped mirrors; logged and not used)
- monitoring.toky.co (?p=11491, 12251, 12187)
- perks.theseniorlist.com/news/adopt-me-exploits
- worker-monitor.api.hlthd.tsl.io (?p=17895, 14746, 13616)
- 2fwww.arktimes.com, nwww.arktimes.com
- jira.phpfox.com (a scraped copy of the Distractify article)
- rustdesk.crownring.com, gsdms.csir.co.za
- Pet-sim "dupe" farms: nest.point-broadband.com, archive-helpline.vetlife.org.uk, dorm.tsot.edu, next.ecardwidget.com, vipsites.publisherdesk.com
- marix.app, mobi.gg (low-quality explainers)
- YouTube "how to duplicate / hack" titles (`3y98BMNOiyU`, `3-Hwu37-b6c`, `nMueCOOexd8`, `pHMTalgl3uo`). These were not opened and are not described. They are not evidence.
- Gameflip, u7buy and u4gm are account and item sellers with a commercial bias. They count as weak corroboration only.

---

## AM-024: 2022-09-02 dupe removal
**Queries:**
1. `Adopt Me duplicate items fix exploiting users September 2022` (open web). No Adopt Me result; all spam.
2. `"Adopt Me" "remove duplicate items" exploiting` (x.com, twitter.com). Found the official tweet only.
3. `Adopt Me duplicated pets claim glitch removed suspicious activity September 2022`. **API 400**: reddit.com is not allowed as a filter domain.
4. `Adopt Me duplicated pets claim glitch removed exploiting September 2022` (fandom, devforum, press, tiktok, youtube). Returned only generic dupe-video titles and fandom opinion threads. Nothing dated.
5. `Adopt Me aware of bug duplicate items investigating September 1 2022` (x.com). Found no "we're aware" pre-announcement, only the same fix tweet.

**New sources:** none independent. The tweet (status 1565618479293759489, 2022-09-02 08:31 UTC) and its player replies are all there is.

**Root cause:** not stated anywhere. The only hint is a player reply about a double "claim" click, which points to a non-idempotent claim or grant. That is a **hypothesis**.

**Independent corroboration:** NOT FOUND.

**Recommended confidence:** keep STRONGLY CORROBORATED, but only for the claim "Uplift stated it removed duplicates". The mechanism is UNVERIFIED.

## AM-016: 2020-09-30 trading disabled
**Queries:**
1. `Adopt Me trading disabled bug items disappear September 2020` (open web)
2. `Adopt Me trading re-enabled October 2020 trading back` (x, twitter, playadopt.me, PGG, Distractify)
3. `Adopt Me trading disabled September 2020 trading is back enabled again` (x, twitter, fandom)
4. `Adopt Me trading purchasing disabled bug items disappear` (x, twitter, playadopt.me)

**Sources:**
- Official tweet 1311101494939262977, 2020-09-30 00:32 UTC (snowflake). This is 2020-09-29 in US time, which resolves the "29/30" ambiguity.
- Distractify, "Why Is Trading Disabled in 'Adopt Me'?" (undated in snippet). It says the bug "seems to stem from issues on the Adopt Me developers' end instead of Roblox's". That is **journalist inference**.
- Pro Game Guides, "Why did Adopt Me disable trading?", which gives the 2020-09-29 date.
- Fandom threads 4400000000001404936, 1405298, 1406318 and 1404946 (all 2020-09-30). They speculate about ghost megas and Blue Dog. That speculation is unverified (see AM-017).

**Re-enable date / root cause:** NOT FOUND after 3 attempts.

**Independent corroboration:** yes for the suspension (two press outlets). No for the cause.

**Recommended confidence:** STRONGLY CORROBORATED (unchanged).

## AM-018: 2020-10-20 game made private (DataStore)
**Queries:**
1. `Adopt Me private Roblox datastore bug October 2020 pets lost` (open web)
2. `Adopt Me Roblox datastore bug game private October 2020 inventory restored` (x, twitter, devforum, status.roblox.com, Distractify, PGG)

**New sources:**
- **Roblox DevForum "DataStores Incident Report"**, https://devforum.roblox.com/t/datastores-incident-report/829962 (Roblox, Oct 2020). Summary: "Roblox released a game server update which caused issues when requesting GlobalDataStore through GetDataStores. The version has been rolled back…", and "Since rolling back to version 452, the default scope was corrected and players appeared to have their 'lost data' restored."
- DevForum bug reports 829121 ("GetDataStore erroring 400: Invalid Operation") and 829116 ("Problems with datastores, again"). Developers report nil data with no error, "indistinguishable from a new player".
- RTC (@Roblox_RTC) status 1318614255608922115, 2020-10-20 18:05 UTC. It says Adopt Me, Shinobi Life 2 and others went private temporarily.
- Pro Game Guides, "A critical bug is currently affecting Roblox's Datastore Servers".

**Root cause (stated, first-party Roblox):** a Roblox game-server regression in the GetDataStore default scope, fixed by rolling back to version 452.

**Independent corroboration:** YES. This is the best-supported Adopt Me incident. It is a separate first-party channel (Roblox) and agrees with Uplift's attribution.

**Recommended confidence:** STRONGLY CORROBORATED. Add new row FU-004.

## AM-014: 2020-04-22 data loss (0.3%, up to 2 days)
**Queries:**
1. `Adopt Me data loss 0.3% players April 2020` (open web). Zero relevant results.
2. `Adopt Me data loss affected players in-game message April 2020` (x, twitter, PGG, PC Gamer, Distractify, devforum)

**Sources:**
- Official 1253042740524388352 (2020-04-22 19:27 UTC) and 1253334125521469440 (2020-04-23). Both are the same channel.
- MiniToon (@darealminitoon) status 1246500542945189890, 2020-04-04 18:11 UTC: "ROBLOX is having some big Data Store issues… even Adopt Me closed because of this". This is a creator account, about 18 days earlier, and possibly a **different incident**.

**Root cause:** not stated.

**Independent corroboration:** NOT FOUND for the 0.3% / 2-day figures.

**Recommended confidence:** keep STRONGLY CORROBORATED, noting it rests on a single first-party channel. Do not upgrade.

## AM-019: Nov 2020 Trade License
**Queries:**
1. `Adopt Me trade license scam prevention update November 2020 trading history report scammers` (blocked x, twitter and playadopt.me to force independent sources)
2. `Adopt Me Trading License quiz November 2020 update news` (Entertainment Focus, PGG, Sportskeeda, Distractify, Dexerto, PC Gamer)

**New sources:**
- Entertainment Focus, "New 'Adopt Me' Update Adds Features To Help Stop Scammers", **2020-11-05**. Snippet: "To get the licence you'll have to answer a few very simple questions". It mentions 9 slots, 30-day history and a two-step trade warning.
- Pro Game Guides, "Adopt Me! adds methods to avoid being scammed" and "How to get a Trade License": three scenarios at the Safety Hub.
- Sportskeeda, "New trading update and pets".
- @PlayAdoptMe 1324455923956490245 (update-notes link) and 1324504467522441217 (2020-11-06 00:10 UTC, which is 11-05 in US time).
- Fandom Trade System / Trade License pages.

**Independent corroboration:** YES (contemporaneous press).

**New minor contradiction:** Entertainment Focus says that without the license only **common and uncommon** pets can be traded, which would also gate Rare. The ledger says Ultra-Rare/Legendary.

**Recommended confidence:** STRONGLY CORROBORATED.

## AM-034: 2025 Sakura Swoop ban wave
**Queries:**
1. `Adopt Me Sakura Swoop exploit ban wave Cherry Blossom` (open web, spam blocked)
2. `Adopt Me Cherry Blossom Festival 2025 release date Sakura Swoop update` (playadopt.me, x, twitter, fandom)

**Sources:**
- Official ban tweet 1910695619816988944 (2025-04-11 14:05 UTC). It describes a three-tier response and says detection methods won't be shared.
- playadopt.me/news/cherry-blossom-festival, dated **Fri 2025-04-04**, 4-week event.
- @PlayAdoptMe launch tweet 1908177272613310563 (2025-04-04 15:18 UTC).
- @playadoptme TikTok 7489477573852908832 (2025-04-04).
- Fandom event page.

**Discrepancy RESOLVED:** the event launched on 2025-04-04, so the ban wave came one week in. The guide date of 2025-04-11 was wrong.

**Independent press:** none found.

**Recommended confidence:** STRONGLY CORROBORATED.

## AM-035: 2025 two-hour playtime trade gate
**Queries:**
1. `Adopt Me 2 hour playtime trade restriction new accounts scam reports` (open web)
2. `Adopt Me 2 hour playtime restriction before new account can trade` (first-party domains)
3. `Adopt Me new accounts must play 2 hours before trading 2025 update` (press and fandom)

**Sources:**
- Official 1923171658430546299 (2025-05-16 00:20 UTC): "Earlier this week we released a 2 hour playtime restriction before a new account can trade… our tests show it [reduces scam reports significantly]". The end of the quote is from a search summary; the snippet was truncated.
- Fandom thread 4400000000007895772 (~Feb 2025), "account too new to trade" popup. This may be an earlier **test** phase.

**Independent corroboration:** NOT FOUND. Press searches return only the separate 2026 Trading Hub unlock, which also requires 2 hours. Do not conflate the two.

**Recommended confidence:** STRONGLY CORROBORATED (single first-party). Event date narrowed to 2025-05-12..15.

## AM-037: 2026 Trading Hub
**Query:** `Adopt Me Trading Hub notes Trading Phone listing` (playadopt.me, x, Sportskeeda, Dexerto and others). Two other queries also returned it.

**Sources:**
- playadopt.me/news/trading-hub-notes. Search-summary quotes: unlock needs 2h of play, the Trade License and a first Neon pet; 100 Bucks per listing; 2 slots (+1 for 49 Robux); listed and offered pets are locked; "isn't intended to create a genuine value system".
- **Second first-party channel:** @PlayAdoptMe 2082859777860698468 (2026-07-30 16:04 UTC): "Learn about cross-server trading and offers in the Trading Hub, coming to Adopt Me tomorrow!" This confirms the 2026-07-31 launch.
- Sportskeeda patch-notes article.
- playadopt.me/discover/toys/trading-hub-phone. This is a separate cosmetic toy.
- Fan posts: Test Lab beta (2082208252771672125, cic4567) and an "offer button" addition (AMNews_Updates 2095895789125894590, 2026-09-04).

**New minor contradiction:** u7buy says the 2h is cumulative, while allthings.how says one unbroken session.

**Recommended confidence:** STRONGLY CORROBORATED.

## AM-029: help centre says duplication is "not possible"
**Queries:**
1. `"pet duplication is not possible" Adopt Me` (open web). **Zero relevant results**; spam only.
2. `Uplift Games Zendesk dealing with scammed account duplication patched dupe offers` (zendesk, help.playadopt.me, playadopt.me)

**Source:** upliftgames.zendesk.com article 39529601838740 (search summary): "pet duplication isn't possible in Adopt Me, and any duplication methods are almost immediately patched upon being found… players who are caught with knowingly duplicated items have their game access restricted". It also says that if a "duplicator" can actually duplicate, "all players involved will be banned". The same summary adds: trades reported through the Trade License are automatically reversed if the report leads to a permanent ban, and there is no reversal for regret trades or device-security compromise.

**Verbatim string:** still unconfirmed. The tool paraphrases.

**New contradiction context:**
- FU-001: in Feb 2025 an exploit let a few players mint Subscription Rewards. It was patched over about a weekend.
- FU-003: the July 2026 Bat Dragon event was called a "dupe" by the community, then reportedly re-attributed to a staff-account compromise.

**Recommended confidence:** STRONGLY CORROBORATED that the statement exists. The claim itself is contradicted by history (AM-024, FU-001).

## 2019 trading launch date
**Queries:**
1. `Adopt Me trading added 2019 update when was trading introduced` (open web)
2. `Adopt Me Support trade 2019 trading pets scam refund trade menu` (x, twitter)

**Result:** no changelog or launch date found. Upper bounds from first-party sources:
- @AdoptMeSupport 1136864164314378240 (2019-06-07) defines duping as getting items "without having to obtain the item by trading or buying it".
- @AdoptMeSupport 1166892519931576320 (2019-08-29) mentions the "trade menu".

So **trading existed by 2019-06-07**, before the pets update (summer 2019). This qualifies AM-002. One search summary claimed "trading existed before 2019", but it gave no source, so it is **not adopted**.

**Recommended confidence:** PLAUSIBLE (unchanged). Add row FU-008.

## Queries that had never been run
- **Starter Egg / gifting.** Queries: `Adopt Me Starter Egg gifting pets gift feature` (first-party domains) and `Uplift Games help Free Pets gifting pets giveaway` (zendesk, help).
  - The Starter Egg exists: @PlayAdoptMe reply 1550140225892007936 (2022-07-21) says "The starter egg isn't being changed".
  - The help-centre "Free Pets" article (FU-007) says support never gives free pets. Unpaid gifts and trades are acceptable. Giveaways that require Robux or a pet count as gambling and can lead to a permanent ban.
  - No first-party description of a dedicated gift mechanic was found.
- **"adopt me neon dupe"** (open web, spam blocked): **zero relevant results**. It returned only the legitimate "Copycat" pet (fandom says it was released 2026-10-16) and Gameflip listings.
- **BBC coverage.** A first attempt used a filter that included bbc.co.uk and bbc.com and returned **API 400**. The unfiltered query `BBC Adopt Me Roblox pets scam children` found **no BBC article**. It returned Parent Zone, **Hwb (Welsh Government) "In the know: Adopt Me"** (hwb.gov.wales/keeping-safe-online/in-the-know/adopt-me, a new government-grade parent source on trust-trade scams), gfinityesports ("Roblox Dad"), and Wikipedia (an AUD ~8,000 child-spending case).

## NEW incidents found that were not in the ledger (high impact)
1. **FU-003, 2026-07-15 Bat Dragon event.**
   - At 02:27 UTC, amvgg reported trading disabled over a "duping incident" involving "Mega and Neon No Potion Bat Dragons".
   - At 10:57 UTC, amvgg reported trading re-enabled: Uplift "revealed that a staff member's account got compromised and that it was in fact NOT duping".
   - TikTok and a fandom thread are consistent with this.
   - **No Uplift statement was found** in 6 targeted queries, so this is PLAUSIBLE.
   - This is reported as an *external compromise of a staff account*. It is not an allegation of insider misconduct.
   - It is the strongest real-world evidence in the project that admin tooling is a mint path (outcome C).
2. **FU-001, 2025-02-25 official:** a Subscription Rewards generation exploit. Trading on those items was blocked, the accounts were banned, and fewer than 100 extra Diamond Hummingbirds entered circulation. It was patched.
3. **FU-002, 2026-06-30:** a fan news account reports that purchasing and trading were disabled over a bug. No first-party source was found. PLAUSIBLE.
4. **FU-004:** the Roblox incident report for AM-018 (above).
5. **FU-005, 2025-07-01 official:** players were kicked by "bug detection", meaning anti-exploit false positives.
6. **FU-006, 2025-06-30 official:** report-based item returns, plus help-centre reversal rules.
7. **FU-008:** the 2019-08-29 trade-menu refund policy.

## Search log (38 calls)
| # | Query | Filter | Outcome |
|---|---|---|---|
| 1 | Adopt Me duplicate items fix exploiting users September 2022 | none | spam only; 0 relevant |
| 2 | "Adopt Me" "remove duplicate items" exploiting | x/twitter | official AM-024 tweet |
| 3 | Adopt Me trading disabled bug items disappear September 2020 | none | Distractify, PGG |
| 4 | Adopt Me trading re-enabled October 2020 trading back | x, twitter, playadopt, PGG, Distractify | no 2020 re-enable; found the 2026 incidents |
| 5 | Adopt Me private Roblox datastore bug October 2020 pets lost | none | PGG datastore article |
| 6 | Adopt Me data loss 0.3% players April 2020 | none | 0 relevant |
| 7 | Adopt Me trading disabled 2026 staff account compromised | none | 0 relevant (HIBP AMTV 2022 breach, unrelated) |
| 8 | Adopt Me trading purchasing disabled bug items disappear | x, twitter, playadopt | AMNews 2026-06-30; amvgg 2026-07-15; AdoptMeSupport 2025-06-30 |
| 9 | Adopt Me Uplift Games compromised account trading paused 2026 | press list incl. BBC, Polygon, Verge | **API 400** |
| 10 | PlayAdoptMe staff account compromised Bat Dragon trading re-enabled | first-party | amvgg only; no Uplift post |
| 11 | Adopt Me Bat Dragon dupe July 2026 trading disabled | spam blocked | amvgg, fandom, TikTok |
| 12 | "Adopt Me!" on X trading enabled again compromised account items removed July 2026 | x/twitter | found FU-001 (Feb 2025) |
| 13 | Adopt Me 2 hour playtime trade restriction new accounts scam reports | none | guides only |
| 14 | Adopt Me Sakura Swoop exploit ban wave Cherry Blossom | spam blocked | official tweet, TikTok |
| 15 | Adopt Me Subscription Rewards exploit February 2025 banned accounts trading blocked | spam blocked | FU-001 text |
| 16 | Adopt Me 2 hour playtime restriction before new account can trade | first-party | AM-035 tweet |
| 17 | Adopt Me Trading Hub notes Trading Phone listing | first-party + press | AM-037 + 2026-07-30 tweet |
| 18 | "pet duplication is not possible" Adopt Me | none | 0 relevant |
| 19 | Adopt Me trade license scam prevention update November 2020 … | blocked first-party | fandom + guides |
| 20 | Adopt Me data loss affected players in-game message April 2020 | x, press, devforum | official + MiniToon |
| 21 | Uplift Games Zendesk dealing with scammed account duplication patched dupe offers | zendesk/help | AM-029 text |
| 22 | Adopt Me Roblox datastore bug game private October 2020 inventory restored | x, devforum, status, press | **Roblox incident report 829962** |
| 23 | Adopt Me trading added 2019 update when was trading introduced | spam blocked | no launch date |
| 24 | Adopt Me duplicated pets claim glitch removed suspicious activity September 2022 | incl. reddit | **API 400** |
| 25 | adopt me neon dupe | spam blocked | 0 relevant |
| 26 | Adopt Me Starter Egg gifting pets gift feature | first-party | Starter Egg reply only |
| 27 | Adopt Me duplicated pets claim glitch removed exploiting September 2022 | fandom, press, yt | 0 relevant |
| 28 | BBC Adopt Me Roblox pets scam children | none | no BBC; Hwb, Parent Zone |
| 29 | Adopt Me trading disabled September 2020 trading is back enabled again | x, fandom | no re-enable date |
| 30 | Adopt Me aware of bug duplicate items investigating September 1 2022 | x/twitter | nothing new |
| 31 | Adopt Me Cherry Blossom Festival 2025 release date Sakura Swoop update | first-party, fandom | 2025-04-04 launch |
| 32 | Adopt Me Support trade 2019 trading pets scam refund trade menu | x/twitter | 2019-08-29 tweet |
| 33 | Adopt Me trading disabled Bat Dragon incident staff account July 2026 | press | 0 relevant |
| 34 | Adopt Me disabled purchasing and trading bug June 2026 | x, playadopt, fandom | no official post |
| 35 | Uplift Games help Free Pets gifting pets giveaway | zendesk/help | FU-007 |
| 36 | Adopt Me new accounts must play 2 hours before trading 2025 update | press, fandom | no 2025 press; fandom popup thread |
| 37 | Adopt Me Trading License quiz November 2020 update news | press | Entertainment Focus 2020-11-05 |
| 38 | Adopt Me staff member account compromised Bat Dragons trading re-enabled not duping | fandom, amvgg, first-party, tiktok, yt | TikTok + fandom; no Uplift post |

**Still open:**
- An official Uplift statement on the 2026-07-15 incident and the 2026-06-30 pause.
- The 2020 trading re-enable date.
- Verbatim help-centre text.
- An independent source for AM-024 and AM-035.
- The exact trading launch date.
