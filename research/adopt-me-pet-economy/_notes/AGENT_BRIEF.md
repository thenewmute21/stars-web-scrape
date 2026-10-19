# Shared brief for research agents (execution date: 2026-10-19)

Project: defensive research to design a secure ORIGINAL Roblox pet-collection/trading game, informed by
OSINT on Adopt Me! (Uplift Games) and Roblox generally. Read-only public research only.

## Hard safety rules
- Do NOT download/run executors, scripts, "pet spawners", cheat binaries, or any sample. Read public pages only.
- Do NOT visit/interact with illicit markets beyond reading public descriptions; never purchase anything.
- Do NOT write operational exploit steps for live games. Describe mechanism at architecture level
  (trust boundary, failure mode, detectable signal, defense).
- Do NOT allege insider misconduct/backdoors without primary evidence; label as hypotheses.
- Never fabricate URLs, dates, incidents or stats. If you could not verify, say so. Record searches that found nothing.
- Prefer primary sources (create.roblox.com, devforum.roblox.com official posts, Uplift Games / playadopt.me /
  official Adopt Me! accounts, Roblox newsroom/SEC filings, reputable press). Wikis/Reddit/YouTube = corroboration only.

## Outcome ontology (column outcome_AH)
A legit persistent server pet; B legit pet without direct Robux (trade/gift/event/earn); C unauthorized server-issued
pet/inflated balance; D duplication/replayed grant of legit asset; E client-only visual/UI spoof/fake screenshot;
F external model/asset uploaded but not an inventory entitlement; G compromised/fraudulent/reversed/support-issued;
H unverified/misunderstood/fabricated.

Confidence: CONFIRMED / STRONGLY CORROBORATED / PLAUSIBLE / UNVERIFIED / DEBUNKED
Status: live-active / historical-patched / historical-unresolved / status-unknown / n/a-intended-design
game_specificity: AdoptMe / OtherRobloxGame:<name> / RobloxPlatform / Generic

## Evidence ledger CSV schema (write rows with a header, RFC4180 quoting)
id,claim,event_date,published_date,publisher_author,url,archive_url,exploit_class,outcome_AH,game_specificity,evidence,counterevidence,confidence,status,defensive_implication,link_checked_2026_10_19

Use your assigned id prefix. One row per material claim. link_checked = yes/no/failed(reason).
