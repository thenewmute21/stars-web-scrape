# Economy design, abuse classes and social engineering (non-code-defect routes)

Agent: ECO (economy/social). Execution date: 2026-10-19. Ledger: `ledger_economy.csv` (ECO-001..ECO-036).

## Method and limits (read first)
- I used only WebSearch. In this session, **WebFetch and curl could not reach any target host.** I tried store.steampowered.com, engadget.com, en.help.roblox.com, www.roblox.com, create.roblox.com, devforum.roblox.com and web.archive.org, and each attempt failed with DNS ENOTFOUND or a proxy CONNECT 403. So I did not open any page directly. The quotes below are search-result excerpts of the named URL. In the ledger, every row has `link_checked_2026_10_19 = failed(egress blocked; search-snippet only)`. A later pass with working egress should confirm the exact wording.
- No exploit tooling was visited. Pages titled as script, pet stealer or "spawner" guides appeared in the results. I did not open them or use them. Many results were SEO/spam mirror domains (for example `*.wizehire.com`, `cannacompanionusa.com`, `monitoring.toky.co`, `compagnie-des-sens.fr`), and I excluded them as evidence.
- Searches that found nothing usable are listed in the section "Negative / unverified searches".

## 1. Economy design: intended arbitrage, value lists, scarcity

### Adopt Me! specifics
- **Robux→pet→trade arbitrage is intended design.** Pets bought with Robux, or hatched from Robux-bought eggs, can be traded for pets other players earned through play. A player who gets a high-value pet "below list price" by trading is mostly in outcome **B**. This is legitimate, not a defect.
- **No official price exists. Values come from community lists.** Search-summarized guides say: "Every pet's worth is determined by player consensus, tracked through community-maintained value lists" (rowatcher.com, 2026). Elvebredd and AMVGG are the trackers cited most often. A Discord bot shows "AMVGG and Elvebredd side by side" (top.gg). The *"Frost Dragon serves as the economy's benchmark currency"* claim comes from a low-authority site, so treat it as UNVERIFIED.
  - Design implication: third-party value lists act as an off-platform price oracle that the game developer does not control. A new list or a manipulated one moves trade outcomes without any code change. In-game "fairness" meters that rely on these lists import the same manipulation risk.
- **Limited-time / event scarcity drives value.** The 2019 Halloween Shadow Dragon is described as never returning and among the top-valued pets. One guide says "limited-time pets released during special events often become more valuable over time" (gfinityesports.com). I could not verify the original Robux price, so it is not stated here.
- **Neon/Mega Neon crafting** consumes several copies of a pet to make one higher-tier pet. This acts as a supply sink and multiplies value (rowatcher.com, low authority).
- **Trade License (Nov 2020).** Wikipedia says Adopt Me "released several new features focused on combating scams in November 2020, including the introduction of 'trade licenses' that are required to be earned before one can trade pets above rare rarity." The fandom wiki adds that the license unlocks ultra-rare and legendary trades, "view their trade history from the last 30 days, and report scammers". The license is earned through a quiz with three scam/not-scam scenarios.
- **Trade-window delay.** A community wiki (r/AdoptMeTradingRoblox) says Adopt Me "gives 15 seconds before you're allowed to hit confirm". I found no official patch note for this.

### Comparables: evidence-based safeguards
| Year | Platform | Change | Stated rationale (as reported) |
|---|---|---|---|
| 2007 → 1 Feb 2011 | RuneScape (Jagex) | Unbalanced free trade and the Wilderness were removed in 2007 and restored after a player vote (~91% Yes, announced 14 Jan 2011; return confirmed 17 Jan 2011). | Removal was "to curb botting, gold farming and item scamming". After the return, a wiki reports "a sudden and dramatic increase in the number of bots" (runescape.wiki Update:Wilderness_and_Free_Trade_Vote; engadget 2011-01-17). |
| 2012-01-04 | RuneScape | The player is notified when a trading partner declines or exits the trade screen. | The wiki says this was "made in response to ongoing scams" (runescape.wiki/w/Trade). The second confirmation screen marks changed items in red. |
| Announced Sep 2013; closed 18 Mar 2014 | Diablo III (Blizzard) | Gold and real-money auction houses closed. | The AH "ultimately undermines Diablo's core game play: kill monsters to get cool loot" (gamebanshee, engadget, gamedeveloper). |
| 9 Dec 2015 | Steam | Trade holds of up to 3 days, or 1 day for friends of at least a year, unless the Mobile Authenticator has been on for at least 7 days. Cancelling a held trade starts a trading cooldown. | About 77,000 accounts were hijacked per month (Valve, Oct 2015, via tweaktown/gamewatcher/lowyat). From 9 Mar 2016 the hold was 15 days for users without the authenticator. |
| ~28 Oct 2019 | CS:GO | Newly bought container keys can't be traded or sold. | "worldwide fraud networks have recently shifted to using CS:GO keys to liquidate their gains"; "nearly all key purchases that end up being traded or sold on the marketplace are believed to be fraud-sourced"; "this change will impact some legitimate users" (bit-tech, kitguru, engadget, pcgamesinsider, gamingonlinux). |
| 2 Oct 2024 | CS2/Steam | 7-day re-trade and re-market restriction on items from the in-game store, trade offers and the Market. | Fraud prevention (forum quotes of the Valve announcement; steamdb). PARTLY UNVERIFIED. |
| 16 Jul 2025 | CS2/Steam | "Trade Protection": traded items are protected for 7 days. The account owner can reverse **all** trades from the last 7 days. Reversal is reported to trigger a 30-day trade/market cooldown. | Helps users who "lost control of their account" (pcworld, csdb.gg, siege.gg, bitdefender). |

- **EVE Online (CCP)** publishes Monthly Economic Reports that include ISK faucet/sink charts (eveonline.com/news/view/monthly-economic-report-november-2024, which reports a data gap and a later correction to sink/faucet totals). A 2014 Fanfest talk by Dr. Eyjólfur Guðmundsson put the net ISK injection at about 20–25T/month and called it not inflationary (engadget tag pages). The design lesson is to publish telemetry on currency and item supply so that inflation is visible.
- **Diablo III and RuneScape history** show that removing or limiting trade can reduce RMT and scams. Both also cost something. Diablo III lost revenue from the real-money AH, and RuneScape's restrictions were unpopular enough that a player vote reversed them. After the 2011 return, bots came back.

## 2. Bots, alts, farming
- **Roblox platform signal.** The official `Players:BanAsync` documentation says by default a ban propagates "to suspected alt accounts" unless `ExcludeAltAccounts=true` (create.roblox.com/docs/reference/engine/classes/Players/BanAsync). DevForum users report that detection can be bypassed and misses newly made alts (devforum t/3753671, t/4138945). This is CONFIRMED that the feature exists and UNVERIFIED on how well it works.
- **Adopt Me-specific bot/alt farming:** I found no official Uplift statement or primary report. The search results were only script-promo SEO pages, which I excluded. For referral or promo-code farming, I found no Adopt Me primary evidence. A generic claim that Roblox ToS forbids alts used to "farm daily rewards, exploit promotional codes" came from an SEO page and is UNVERIFIED.
- **Comparable evidence:** RuneScape's 2011 free-trade return was followed by a bot surge (runescape.wiki). Valve's 2015 hold targeted automated theft and resale of hijacked inventories.
- **Design implications for daily, login, AFK and referral rewards:**
  1. Rewards earned through AFK play or alts should be untradeable, or "trade-locked until account age/engagement threshold".
  2. Rate-limit rewards per device and per payment instrument, not per account.
  3. Flag star-topology transfers, where many young accounts send items into one receiver.
  4. Use Roblox's alt-propagating ban by default.

## 3. Social engineering and scams (mechanism level only)
- **Trust trades / deals off the trade window.** The Roblox help center says: "if you made a deal with another player and they backed out we are not able to reverse it or return your items or currency". It flags "deals where one of the sides has to go first" (en.help.roblox.com/hc/en-us/articles/203312390). about.roblox.com/frauds-and-scams says the same about deals outside the official Trade/Sell features.
- **Last-second swap / item switch.** The countermeasures are a second review screen with changed items highlighted (RuneScape), a confirm delay (Adopt Me's reported 15 s), and a reset of both parties' "accept" whenever the offer changes.
- **"Double trade" scam.** Talos describes it: the scammer proposes two trades, one in each direction. The scammer then drains their own Robux so the trade that favors the victim fails, and only the bad one completes (blog.talosintelligence.com/roblox-scam-overview). Mitigation: make trades atomic, check each trade's terms against current balances at commit time, and warn on lopsided trades.
- **Fake middleman.** Guides describe second accounts run by the scammer posing as a "middleman" (securityscientist.net; arktimes). The architectural fix is that the game itself acts as escrow (atomic two-sided commit), which makes a human middleman unnecessary.
- **Phishing, "free Robux/pets" sites and session token theft.** Talos documents fake Robux pages that harvest credentials. It also describes a fake tutorial that tricks users into exporting a HAR file containing the session cookie. Motherboard/Vice (Feb 2022, "beaming") reports that hijacked accounts are emptied by trading to an attacker-controlled account, and the items are sold for USD or crypto on Discord marketplaces. The Vice report also says "Roblox only offers one rollback per account". A third-party tutorial says Roblox locks the `.ROBLOSECURITY` cookie to an IP region from 8 Mar 2022. DevForum confirms that the cookie resets on IP change. That makes it **STRONGLY CORROBORATED**.
- **Staff impersonation.** about.roblox.com says to report anyone claiming to be staff without the Roblox Admin badge. Roblox "will never ask for your password outside its login page". Adopt Me uses in-game identity markers (Verified Friend, Uplift staff icon), but my only source is a third-party guide, so this is UNVERIFIED.
- **Fake giveaway streams (2025).** Looped "live" YouTube streams send viewers to claim sites for Grow a Garden and Steal a Brainrot (roonby.com, low authority).
- **Chargeback fraud.** The Roblox FY2022 10-K says: "some users have made fraudulent use of credit cards owned by others on our Platform to purchase Robux and offer the purchased Robux for sale at a discount on a third-party website. For the year ended December 31, 2022, total chargebacks to us from this fraud was approximately 3.16% of bookings." The FY2025 10-K says Roblox is "unable to control or stop all unauthorized, fraudulent, or illegal transactions". The Roblox help center says unauthorized charges "may result in the permanent closure of the associated user account(s)" and that a refund cannot be issued once a charge is disputed (articles/203312650). Third-party sources say a chargeback can create a negative Robux balance, which is UNVERIFIED against official text.
- **Support / rollback abuse (outcome G).** A DevForum report, "Traders on Roblox are reportedly abusing rollbacks" (devforum t/4820634), describes a trader accepting a trade, claiming afterwards that the account was hacked, and getting **only their side** reversed. The counterparty loses what they sent. Roblox reportedly assigned it for review. This is user-reported, so PLAUSIBLE. A 2018 thread describes the once-per-account restoration policy (t/122309). Steam's 2025 design reverses **all** of the claimant's trades and adds a 30-day cooldown, which is a structural deterrent to the one-sided abuse.

## 4. Real-money trading (RMT) and laundering
- **Roblox position.** A Roblox spokesperson told Motherboard: "Users cannot exchange in-game virtual currency for real-world currency on Roblox outside of our developer exchange program and we specifically ban the use of third-party trading sites" (vice.com/en/article/88gd4a/roblox-beaming-hackers).
- **Third-party pet marketplaces.** Eldorado and StarPets are named as places selling Adopt Me pets. A review aggregator records complaints about non-delivery and account hacks after purchase (progameguides, malwaretips). eBay.de has listings for Steal a Brainrot items. I did not visit or interact with any marketplace.
- **Laundering through game currency.** Sixgill/The Independent (Jan 2019) reported that stolen cards were used to buy V-Bucks, which were then resold at a discount, with Sixgill saying "Criminals are executing carding fraud and getting money in and out of the Fortnite system with relative impunity" (occrp.org). The Valve CS:GO key decision (2019) is the clearest primary precedent. The Roblox 10-K describes the same pattern for Robux (stolen card → Robux → discounted resale).
- **Cash-out path.** In a pet game, RMT turns stolen-card purchases into tradable pets and then into cash. A fresh purchase that can be traded immediately is the laundering primitive. The mitigation, following Valve, is to delay tradability of new purchases until the chargeback window has mostly passed, or to make some purchases permanently untradeable.

## 5. Anti-fraud UX, costs, child safety, privacy
- **Proven patterns:** second confirmation screen, with diffs highlighted (RuneScape); acceptance reset plus a confirm countdown (Adopt Me, community-reported); a quiz gate before high-tier trading (Adopt Me Trade License); 30-day trade history (Adopt Me); trade holds that the authenticator shortens (Steam); untradeable purchases (CS:GO keys); a 7-day hold after acquisition (CS2 2024); whole-account reversal plus a cooldown (CS2 2025); alt ban propagation (Roblox BanAsync); IP-bound session cookies (Roblox).
- **Costs and false positives:**
  - Valve said openly that the key change "will impact some legitimate users".
  - Holds slow down legitimate trading, and RuneScape players voted ~91% to undo restrictions.
  - IP-bound cookies log out legitimate users who travel or use mobile networks and break developer tooling (DevForum).
  - Value-imbalance warnings depend on unofficial price lists that can be manipulated, and they can make children feel shamed or anxious. They should inform the player, not block the trade.
  - Rollbacks that reverse one side only create a new scam (G).
  - The Diablo III AH closure gave up revenue.
- **Child safety and consumer protection.** The FTC v. Epic settlement (Dec 2022; refunds of $245M finalized Mar 2023; separate $275M COPPA penalty) requires "affirmative, express, informed consent" for charges. It also **prohibits locking accounts for disputing unauthorized charges** (venable, hunton, pymnts). This directly constrains "ban on chargeback" policies. A 3.16%-of-bookings fraud rate, as in Roblox's 10-K, still has to be handled without punishing parents who dispute charges for real unauthorized use. US state AGs (Kentucky, Florida, 2025) have sued Roblox over child safety and cite Robux as a grooming and exploitation vector. Trade, gifting and transfer telemetry is therefore also safety telemetry.
- **Privacy.** The FTC COPPA amendments were finalized 16 Jan 2025. They require a written data-retention policy and bar indefinite retention of children's data (skadden, bgov). Whether and when the rule took effect after the Jan 2025 regulatory freeze was UNVERIFIED in my searches. Design implications:
  - Collect trade telemetry at the minimum granularity needed for fraud detection (item IDs, counterparties, timestamps, coarse device/risk scores).
  - Avoid raw chat or PII.
  - Set retention limits, for example 90–180 days for raw events and aggregates after that.
  - Write the purpose limitation (fraud and safety) into the retention policy.
  - Do not use precise geolocation. Roblox's IP-region approach shows that coarse location is enough.

## Mechanism table
| mechanism | intended? | code defect? | outcome A-H | mitigation | UX cost |
|---|---|---|---|---|---|
| Buy Robux pet/egg, trade for earned pets ("Robux arbitrage") | Yes | No | A (buyer) / B (receiver) | None needed; publish odds; keep trade atomic | None |
| Trading up via value-list knowledge (buying "below list") | Yes (player skill) | No | B | Optional value hints that inform but don't block | Low; risk of anxiety for kids |
| Value-list manipulation / hype pumping by third-party sites or influencers | No (emergent) | No | B (economically harmful) | Publish first-party supply/rarity stats; don't hard-wire third-party values | Low |
| Event-exclusive / limited-time scarcity, legacy pets | Yes | No | A/B | Telegraph retirement; avoid surprise re-releases that crash value | Medium (FOMO; ethics for minors) |
| Gifting (Robux-bought gifts) | Yes | No | A/B; G if card stolen | Gift tradability hold; spend limits; parental controls | Low–medium |
| Neon/crafting sinks | Yes | No | A/B | Sink telemetry (EVE-style MER) | None |
| AFK / auto-farm of earnable currency | No (ToS) | No (automation of legit actions) | B (illegitimately earned) | Engagement/human checks; diminishing returns; untradeable earned rewards until thresholds | Low–medium |
| Alt farms (daily/login/referral/promo rewards funnelled to main) | No | No | B/G | Device/payment-scoped limits; account-age trade gates; graph detection; BanAsync alt propagation | Medium (siblings sharing a device = false positives) |
| Trust trade (one side goes first off-window) | No | No | G | In-game escrow only; license quiz; education | Low |
| Last-second item swap | No | No | G | Diff-highlighted second screen; accept-reset; confirm countdown | Low (seconds) |
| Double-trade / balance-drain | No | No (design gap) | G | Atomic commit; re-validate at commit; one pending trade at a time | Low |
| Fake middleman | No | No | G | Platform escrow; verified-friend / staff badges | Low |
| Phishing / "free pets" sites / HAR/cookie theft → beaming | No | No (platform-side mitigations) | G | 2SV/passkeys; IP-bound sessions; new-device trade hold; high-value trade notification | Medium (re-login, delays) |
| Staff impersonation | No | No | G | Unforgeable in-game staff badges; "staff never ask" messaging | Low |
| Account selling / RMT marketplace purchase | No (ToS) | No | G (if stolen/fraud-sourced) / B-ish | Ownership-change heuristics; recovery-flag holds; cease-and-desist | Low |
| Stolen-card Robux → discounted resale / pet laundering | No | No | G | Untradeable-on-purchase window ≥ chargeback window; risk models on large/abnormal purchases | Medium (legit buyers wait) |
| Chargeback after spending ("friendly fraud") | No | No | G | Claw back items, and hold items received in trade from the charged-back account; do NOT blanket-lock disputing accounts (FTC/Epic) | Low–medium |
| One-sided rollback / support restoration abuse | No | No (policy defect) | G | Reverse all trades both ways for the claimant + cooldown (Steam 2025 model); one restoration per account; evidence requirement | Medium |
| Fake screenshots / "proof" of pets | No | No | E/H | Verifiable in-game inspect/trade history | None |

## Negative / unverified searches
- I found no official Uplift Games help-center or patch-note page reachable via search on trade-window timing, pet restoration, bots or alts.
- I found no primary source on Roblox's chargeback negative-balance mechanics. Only third-party claims came up.
- I found no 2018 Kotaku/Ubisoft "R6 trading disabled for laundering" article. The search instead surfaced a Dec 2025 R6 Siege breach and rollback, which is a code/backend incident and out of scope.
- I found no primary BIG Games (Pet Simulator 99) account-age trade gate.
- I found no GDC Vault talk via search. GDC Vault should be searched directly.
- I found no FTC consumer alert specific to Roblox. A Nevada AG Fortnite warning (2019) and Action Fraud UK reports exist.
- Roblox Community Standards wording on RMT and account sales was not retrieved verbatim, apart from the Vice spokesperson quote.
