# Official Roblox platform facts for securing a pet inventory, trading and purchase economy

Agent prefix: OFF- | Execution date: 2026-10-19 | Ledger: `ledger_official.csv`

## Method and source provenance (read first)

- **Live access was blocked.** `create.roblox.com`, `devforum.roblox.com`, `en.help.roblox.com`, `about.roblox.com`, `corp.roblox.com`, `www.roblox.com` and `web.archive.org` all returned proxy 403 (CONNECT rejected) on 2026-10-19. WebFetch got ENOTFOUND for create.roblox.com.
- **WebSearch was not available.** The shared per-turn search budget was already used up when I tried, so I ran no web searches. In particular, I made no searches for Hyperion/Byfron, FilteringEnabled 2018, age-check or trading announcements. See "Could not verify".
- **Primary source used:** the official open-source documentation repo `github.com/Roblox/creator-docs`, which create.roblox.com renders. I used HEAD commit `70a0110fee0c0900103e545fcaee69a8bd2a942f`, dated 2026-10-17. Every quote below is verbatim from that commit. Each claim is cited with the create.roblox.com URL that corresponds to its file. Ledger `link_checked` = `verified-via-creator-docs@70a0110`.
- **Dating changes:** I unshallowed the repo (blobless) and used `git log -S` to find when a statement first appeared. Those dates are the doc-repo commit dates, not necessarily the feature release dates. Repo history only starts on **2023-08-29**, so any date of 2023-08-29 or 2023-11-02 means "already present when the repo was opened" and could be much older.

---

## 1. Client-server boundary, replication, server authority

### FilteringEnabled
- `Workspace.FilteringEnabled` summary: "Determines whether changes made from the client will replicate to the server or not." Its description is now: **"This property is discontinued and no longer takes effect."** (https://create.roblox.com/docs/reference/engine/classes/Workspace, first in repo 2023-11-02).
- The docs give no date for when FE became mandatory. The commonly cited 2018 date for "Experimental Mode" removal **could not be verified** from an official source in this session (DevForum blocked, no search budget).
- Practical meaning today: the client→server boundary always applies, and there is no opt-out.

### What replicates and what doesn't (Access control page)
https://create.roblox.com/docs/scripting/security/access-control
- "Instances are server-authoritative, meaning that for an instance to replicate between all participants (the server and all connected clients) **it must be created on the server**."
- "Instance properties are also server-authoritative, which means most properties must be changed on the server for the changes to be visible on all clients."
- "Any content that replicates to a client can be extracted and data-mined by an exploiter."
- "Any `LocalScript`, `Script` with `RunContext::Client`, or `ModuleScript` can be decompiled by an exploiter once replicated to their client, even if such scripts are disabled, never required, or never run on the client. Server-only Scripts and ModuleScripts stored in `ServerStorage` or `ServerScriptService` cannot be decompiled."
- Client-side teleport: "A client can teleport to any subplace if they can access a single place". There is a newer mitigation, **"Secure within universe only"** place access control, which "restricts all non-start places to server-initiated teleports only" (statement first in repo 2026-02-18).

### Remote argument semantics
https://create.roblox.com/docs/scripting/events/remote
- "the first parameter of the event handler on the server is always the `Player` object of the client that calls it". This sender identity is the one trustworthy input.
- "if you create a part in a `LocalScript` and try to pass it to a `Script`, the server will see `nil` because the part isn't replicable for the server." So **client-created instances do not replicate**, and passing one in a remote arrives as nil.

### Attributes
- The docs state replication direction server→client: CollectionService tags "replicate from the server to the client" (https://create.roblox.com/docs/studio/properties). The general rule above means client-set properties and attributes don't propagate to the server.
- The docs also note: "The Roblox Engine doesn't guarantee the order in which objects (and changes to objects) are replicated from the server to the client" (https://create.roblox.com/docs/scripting/attributes).
- The security page's own example gates a spell on `player:GetAttribute("HasLightningSpell")` read **on the server**. Attributes are safe only when the server is the writer.

### Securing the client-server boundary (page first in repo 2026-01-14; supersedes older guidance)
https://create.roblox.com/docs/scripting/security/client-server-boundary
- "Every piece of data sent from a client must be validated by the server before it's used."
- Validation layers: context/permission, type/structure, value.
  - Spoofed tables: "Another common attack ... involves sending tables in place of an Instance." Check `typeof(item) == "Instance"` and `IsDescendantOf(itemDataFolder)`.
  - "both `inf` and NaN are valid number types ... Use `math.isfinite()` to detect and reject them".
  - There is an explicit **NaN trade-offer example**: "The exploiter successfully created a trade offer without having any gold ... this single NaN value will now poison any other system that tries to use it, and even spread to other players through the offer."
- **Rate limiting (official guidance now exists):** "never rely solely on a client-sided rate limit", with a reference token-bucket module (`TokenBucket.new(capacity, windowSeconds)`). This also applies to Touched, ProximityPrompt, ClickDetector and DragDetector.
- ProximityPrompt: "An exploiter can fire any event even if `Enabled` is false on the server" and "Only the `Triggered` event has a server-side distance check." ClickDetector: "There are no checks at all on the server for any events."
- Network-ownership caveat: if prompts or detectors are under unanchored parts, "an exploiter can take network ownership of the parent parts and move them directly to their character, bypassing distance checks."
- **Trading duplication is named explicitly:** "A player initiates a trade, sends their item to another player, then immediately leaves the game. If the trade completes but their DataStore save fails due to invalid data, they rejoin with their original items while the other player keeps the traded items - resulting in duplication."
  - Prevention: "Use transaction-like patterns where all players' data is validated before committing any changes".
- DataStore input hygiene: Instances can't be serialized, "Table indices cannot be NaN or nil", "DataStores can only accept valid UTF-8 characters" (use `utf8.len()`), and cap string lengths.
- MarketplaceService: "Never trust a client-side signal, such as `PromptProductPurchaseFinished`, to confirm a purchase ... be prepared to handle cases where a product has already been granted for a given receipt."

### Security tactics
https://create.roblox.com/docs/scripting/security/security-tactics (page first in repo 2023-08-29; content revised since)
- "Never trust the client". Exploiters can "Fire or invoke RemoteEvents and RemoteFunctions at any frequency with arbitrary arguments (besides the first Player argument)", "Change anything in their local DataModel without firing any expected events", "Take network ownership of their character and any unanchored parts".
- "Keep logic and data in ServerScriptService from day one. Never place them in replicated containers like ReplicatedStorage or Workspace."

### Network ownership
https://create.roblox.com/docs/scripting/security/network-ownership
- "By default, the server grants network ownership of unanchored parts to clients with nearby player characters". The owning client can replicate Inf/NaN CFrames, extreme velocities, and "Manipulate the firing of Touched events, including not firing Touched at all."
- Mitigation is `BasePart:SetNetworkOwner(nil)` (server ownership) or anchoring. See https://create.roblox.com/docs/physics/network-ownership.

### Server authority (beta)
https://create.roblox.com/docs/projects/server-authority (page first in repo 2025-12-09)
- "In a server authority model, the server is the single source of truth for the entire game state, and clients are only trusted to report their own inputs." It uses client prediction plus rollback and resimulation.
- Setup: `Workspace.AuthorityMode = Server`, which auto-sets NextGenerationReplication, PlayerScriptsUseInputActionSystem, SignalBehavior = Deferred, UseFixedSimulation and StreamingEnabled.
- Status per the network-ownership page: "Server authority is currently in beta and will be released soon." That statement is still present at commit 70a0110 (first added 2026-01-14).
- Relevance: this addresses movement/physics exploits only, **not** inventory or trade logic.

---

## 2. MarketplaceService and receipts

https://create.roblox.com/docs/reference/engine/classes/MarketplaceService

### ProcessReceipt (legacy but still valid)
- "You should only set the `ProcessReceipt` callback one time in a single server-side Script."
- When it is called, for all unresolved purchases: "A user successfully completes the purchase", "A successful developer product purchase prompt appears to the user", "A user joins the server."
- Resolved means: the callback returns `PurchaseGranted` **and** "The purchase is successfully recorded on Roblox's backend."
- "Unresolved developer product purchases are not removed or refunded after the escrow period expires." (statement first in repo 2025-01-21; this changed earlier community belief that unresolved purchases were auto-refunded)
- **Retries:** "`ProcessReceipt` has no time-based retry mechanism." After `NotProcessedYet`, it is called again only if "The user successfully initiates another developer product purchase" or "The user re-joins any server under the same experience."
- **No timeout:** "A `ProcessReceipt` callback can yield for as long as the server is running".
- Limitations, verbatim:
  - "If you don't implement a `ProcessReceipt` callback, your receipts will be auto-acknowledged."
  - "called in a non-deterministic order"
  - "The user must be on the server for the `ProcessReceipt` callback to be invoked."
  - **"The `ProcessReceipt` callback for a specific purchase might run on two different servers at the same time if the user joins the second server before the callback returns on the first server."**
  - **"The `ProcessReceipt` callback might still fail to be recorded on the backend, even if it returns ... `PurchaseGranted`. When this happens, the purchase remains unresolved."** The receipt can therefore be redelivered after a grant, so grants must be idempotent on `PurchaseId`.
- receiptInfo fields: `PurchaseId` ("A unique identifier for the specific purchase"), `PlayerId`, `ProductId`, `PlaceIdWherePurchased`, `CurrencySpent`, `CurrencyType` (always Robux), and `ProductPurchaseChannel` (InExperience / ExperienceDetailsPage / AdReward / CommerceProduct; first in repo 2025-01-21).
  - Purchases from the **experience details page Store tab** happen while the user is outside the game, so they arrive on the next join.

### BindReceiptHandler (NEW; verified to exist)
- `MarketplaceService:BindReceiptHandler(receiptType, handler, filter?)` returns an RBXScriptConnection. It is "a newer alternative that processes developer product receipts (and Robux transfer receipts) through one or more bound handlers instead of the single `ProcessReceipt` callback."
  - First in repo: `Enum.ReceiptDecision` on 2026-04-02 and MarketplaceService text on 2026-05-04.
- Handlers return `Enum.ReceiptDecision.Processed` or `NotProcessedYet`. "A bound handler takes precedence; if no bound handler matches a developer product receipt, it falls through to `ProcessReceipt`."
- Filtered (per product-ID) and catch-all handlers. It "throws an error if: A handler is already registered for the same ReceiptType and product ID combination" or a duplicate catch-all.
- `NotProcessedYet` per the ReceiptDecision enum: "keeps the receipt unresolved so it will be redelivered to the user's handler later, either during their existing session or the next time they join a server".
- Receipt types: DeveloperProduct, RobuxTransferSender, RobuxTransferReceiver.

### Robux transfers (NEW, 2026; directly relevant to trading)
https://create.roblox.com/docs/production/monetization/robux-transfers (first in repo 2026-05-04)
- "**Robux transfers** let Roblox Plus subscribers send Robux directly to other users." Started server-side with `MarketplaceService:PromptRobuxTransferAsync(sender, receiverUserId, amount)`.
- "your game earns 10% of the Robux sent and the recipient receives the remaining 90%". The amount must be "between 10 and 500 Robux per transaction". "All Robux transfers are processed and managed by the Roblox platform ... through a Roblox-controlled UI".
- Receipts go to both sides and may be delayed by "parental consent" approval. "Receipt is delivered to whichever server the user is currently in (the user does not need to rejoin)".
- Related: "Starting May 30, 2026, cross-game pass sales will be disabled", with the same rule for developer products. Roblox recommends Robux transfers instead (https://create.roblox.com/docs/production/monetization/passes).
- **Design implication:** an official, in-game Robux-for-anything rail now exists. A pet-for-Robux trade could be built on it, which interacts with paid-item-trading policy (section 7) and scam/escrow design. An experience must decide deliberately whether to tie item handoff to transfer receipts, using an escrow keyed by `TransferRequestId`.

### Passes, developer products, subscriptions
- Passes: "charge users a one-time Robux fee" (https://create.roblox.com/docs/production/monetization/passes). Developer products are for repeatable purchases such as currency.
- `UserOwnsGamePassAsync` caching: "The results of this function are cached ... When `PromptGamePassPurchaseFinished` fires, the cache gets updated ... If the user purchases a game pass outside of the experience while remaining in the same session, the cache is eventually updated, but this process might take several minutes to propagate. When a user first enters a server after purchasing a game pass, this functions always returns true." It is callable on client and server, so check on the server. It is "Transparent Batching capable".
- `PromptProductPurchaseFinished`: "Do not use this event to process purchases ... The firing of this event does not mean that a user has successfully purchased an item."
- Subscriptions: "Subscriptions purchased with Robux are not eligible for refunds", while local-currency refunds within the 30-day hold cancel payout (https://create.roblox.com/docs/production/monetization/subscriptions). The check is `GetUserSubscriptionStatusAsync`.

### Refunds and reversals (NEW webhook)
https://create.roblox.com/docs/cloud/webhooks/webhook-notifications
- **"Transaction Refunded"** trigger (first in repo 2026-09-03; customer-service revocation text 2026-10-01): "covers developer products, passes, private servers, and paid access. It doesn't include subscriptions."
  - Payload includes buyer user ID, product type and ID, Robux amount ("the product's original price"), universe and place, "transaction or receipt ID", and refund time.
  - **"When a pass or avatar item is refunded through Roblox Customer Service, Roblox automatically revokes ownership of the item. For developer products, the benefit exists only in your experience's code, so you need to use this notification to remove the granted benefit, such as currency or boosts, from the player's save data yourself."**
- Webhook security: optional secret yields `roblox-signature: t=<timestamp>,v1=<HMAC-SHA256 base64>`. Docs suggest a ~10-minute replay window. Retries happen "5 times using a fixed window size". Commerce events may duplicate, so deduplicate.
  - "For group-owned games, only group owners can configure and receive webhook notifications."
- Design implication: pets bought with Robux, or with currency bought from Robux, that have since been **traded** to another player create a clawback problem. Roblox revokes nothing for dev products, and the game must define its own policy (debt, negative balance, quarantine of descendant items).

---

## 3. DataStores, MemoryStores, MessagingService, Open Cloud

### UpdateAsync
https://create.roblox.com/docs/reference/engine/classes/GlobalDataStore
- "In cases where another game server updated the key in the short timespan between retrieving the key's current value and setting the key's value, `UpdateAsync()` will call the function again, discarding the result of the previous call. The function will be called as many times as needed until the data is saved **or** until the callback function returns `nil`."
  - This is optimistic concurrency per key.
- "The callback function cannot yield". Returning `nil` cancels the write.
- The callback returns (value, userIds, metadata). "`DataStoreKeyInfo:GetUserIds()` should be returned unless the existing IDs are being changed; otherwise all existing IDs will be cleared." The same applies to metadata.
- `SetAsync` "may cause data inconsistency if two servers attempt to set the same key at the same time".
- **No cross-key transactions.** No multi-key atomic API exists in the engine or Open Cloud data store reference at this commit; I grepped for "transaction" in the data store and memory store references and found nothing relevant. `BatchGetAsync` exists but "is currently only supported on `OrderedDataStore`" and is read-only.
  - A two-party trade is therefore at minimum two independent key writes. You must design an escrow or two-phase pattern, or a single trade-record key with idempotent apply.

### Limits (current numbers, commit 70a0110)
https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits
- Value **4,194,304 characters per key** (4 MB). Name, key and scope 50 chars each. Metadata value 250 chars and 300 chars total.
- Per-key throughput: **read 25 MB/min, write 4 MB/min**, measured over 60 s with KB rounding up.
- Experience-wide standard data stores: Read 300 + 40×CCU, Write 300 + 20×CCU, List 300 + 2×CCU, Remove 300 + 40×CCU per minute. "UpdateAsync() consumes from both the read and write request budgets".
  - **"Game server and Open Cloud share a budget"**, so an external tool can starve the live game.
- Queues: "Each queue has a limit of 30 requests" and overflow fails with codes 301-306.
- **Storage limit (new):** "Total latest version storage limit = 500 MB + 1 MB × lifetime user count", counted on compressed latest versions (first in repo 2026-07-14).
- Server-level controls: `DataStoreService:SetRateLimitForRequestType()` and `GetRequestBudgetForRequestType()`.

### Versioning and caching
https://create.roblox.com/docs/cloud-services/data-stores/versioning-listing-and-caching
- Versioned backups use "the first write to each key in each UTC hour. Successive writes to a key in the same UTC hour permanently overwrite the previous data." "Versioned backups expire 30 days after a new write overwrites them."
  - Rollback granularity is about 1 hour, so it is **not** a per-trade audit log.
- `RemoveAsync` leaves a tombstone, and older versions stay retrievable. A once-a-day Snapshot Data Stores Open Cloud API is recommended before schema-changing updates.
- Caching: "By default, the engine uses `GetAsync()` to store values ... in a local cache for **four seconds**". Use `DataStoreGetOptions.UseCache = false` "For immediate verification reads after a write". The cache is "local to a particular data store instance".
  - The 4 s figure is unchanged from the historical value. `UseCache` is the newer opt-out.

### Session locking and purchase recipe (official)
https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing
- Problem statement: "Session Locking: If a single player's data is loaded and in-memory on multiple servers ... This can lead to data loss and **common item duplication loopholes**." Also: "Some malicious users might even attempt to abuse this behavior ... This can be particularly impactful in games that allow players to trade and is a common source of item duplication exploits."
- Mechanism: on first read the server "atomically writes a lock to the key's metadata inside the same `UpdateAsync()` call". There is a `LockId` GUID plus expiry and a refresh on autosave. Every op goes through UpdateAsync. Writes are retried in per-key FIFO order (`DataStoreWrapper`), because naive retries reorder writes.
- Receipt recipe, before returning `PurchaseGranted`:
  1. Verify `PurchaseId` not already recorded.
  2. Award in memory.
  3. Record `PurchaseId`.
  4. Save to DataStore.

  If `PurchaseId` is recorded but not yet saved, return `NotProcessedYet`.
- The docs warn: "if the player's data fails to save in step 5, the player receives the purchase for free for the duration of the session." The sample is caveated as "has not proven itself over a long period of time in a popular game".
- Failed-load handling: use default data and mark the profile "errored" so it is **never written back**. This prevents overwriting real data.

### MemoryStoreService
https://create.roblox.com/docs/cloud-services/memory-stores
- "suitable for frequent and ephemeral data that ... don't need to be durable". Max TTL 3,888,000 s (45 days).
- Memory quota 64 KB + 1.2 KB × users, with an 8-day lookback when shrinking. Requests 1000 + 120 × CCU units/min.
- Hash maps: key ≤ 128 chars, value ≤ 32 KB, per-key ~5,000 write / 15,000 read units/min. `MemoryStoreHashMap:UpdateAsync` is compare-and-retry ("The new value is saved only if the key was not updated ... since the moment it was read"; https://create.roblox.com/docs/reference/engine/classes/MemoryStoreHashMap).
- Queues: invisibility timeout default 30 s, and items reappear if not removed. That is **at-least-once** processing, so consumers must be idempotent.
- Implication: MemoryStore is usable for cross-server trade locks, matchmaking or a trade mailbox, but **never as the system of record** for pets.

### MessagingService
https://create.roblox.com/docs/reference/engine/classes/MessagingService
- "**Delivery is best effort and not guaranteed.** Make sure to architect your experience so delivery failures are not critical." Typical latency is 1-2 s.
- Limits: 1 kB messages, 600 + 240×players sends/server/min, and others in the table.
- Never use it as the only carrier of a cross-server trade or gift commit.

### Open Cloud API keys
https://create.roblox.com/docs/cloud/auth/api-keys
- "An API key's access is determined by the permissions of the user who owns it ... Some scopes can be restricted to specific games, but not all." "Restrict by Experience" can be disabled, which grants all current and future games.
- Optional IP CIDR allowlist ("Do not use IP address restrictions when using your API key in Roblox places") and optional expiry. **Auto-expire after 60 days unused.**
  - Statuses include "Revoked" (group keys whose creator lost permission), "Moderated" ("A Roblox admin changed the key's secret for security reasons") and "User Moderated".
- Recommends "a separate API key on a dedicated alternate account with access strictly limited to the target group". Store keys in a secrets manager, and inside places use the Secrets Store (`HttpService:GetSecret`).
- Implication: any Open Cloud key with data store write scope on the universe is an **out-of-band item-minting capability**. Treat it like a production DB root credential.

---

## 4. Asset ownership, permissions, and "uploaded mesh → inventory item?"

### InsertService / AssetService loading
- `InsertService:LoadAsset` Security Check (https://create.roblox.com/docs/reference/engine/classes/InsertService). "An asset loaded by this function must meet one of the following: The asset must be **created or owned** by the game creator. The asset must be **shared** by the asset owner. The asset must be owned by Roblox." Also, "benign asset types such as t-shirts, shirts, pants and avatar accessories are loadable from any game as they are `OpenUse`."
- **New:** `AssetService:LoadAssetAsync` is "the modern replacement for `InsertService:LoadAsset()`" (https://create.roblox.com/docs/reference/engine/classes/AssetService).
  - The returned Model "is sandboxed by default (`Sandboxed` is `true`) and has no script Capabilities".
  - `AssetService.AllowInsertFreeAssets` is off by default and settable only in Studio's "Allow Loading Third Party Assets". When true it "can additionally load any public free asset on the Creator Store". (first in repo 2025-10-22)

### Asset privacy (current model)
https://create.roblox.com/docs/projects/assets/privacy
- Two states: "Restricted — Creators or games can only use the asset after the asset owner grants permission" and "Open Use — Any creator or game can use the asset."
- "Asset Privacy controls only the default privacy state assigned to **Images**, **Decals**, and **Meshes** when they are created." "By default, Images, Decals, and Meshes are created as Open Use" unless the creator opts in.
- "Open Use is irreversible." "Game grants are permanent." "If a creator or game doesn't have permission to use an asset, it cannot load".
- Grants to individuals require the creator to be a friend. Group grants go to members with Edit.

### Answer: can a third party make an uploaded mesh become a pet in someone else's game?
**No, not through the asset system.** An uploaded mesh or model is only content. Per the docs:
- The target game can only load it at runtime if the game's creator owns it, it is shared with them, it is Roblox-owned, or the game opted into third-party loading.
- Even then, the game's code has to choose to load it.

"Inventory" in an experience like a pet game is **the experience's own DataStore records**. Nothing on the asset side writes those records. A mesh lookalike shown in a third party's own game, place copy or screenshot is outcome **F** (external model, not an entitlement). If shown only on the viewer's client, it is outcome **E**.

The real risks are:
- a game that loads asset IDs supplied by clients (the security docs say "Take extreme care in dynamically loading any assets ... based on the arguments of remote functions/events");
- backdoored Toolbox models;
- compromised collaborator, Open Cloud or plugin access.

### Third-party models, plugins, collaborators
- https://create.roblox.com/docs/scripting/security/third-party-vulnerabilities
  - "Third-party assets from the Creator Store (Toolbox) are a common source of security risks, as they can contain malicious scripts called backdoors."
  - Defense: Workspace `SandboxedInstance = Experimental`, Model `Sandboxed = true`, minimal Capabilities. "Be especially cautious about granting Network, DataStore, AssetRequire, CapabilityControl, or LoadString capabilities".
  - "In the future, we plan to automatically sandbox all assets from the Creator Store". The Capabilities feature is still labeled beta.
- Collaborators: permission levels Owner / Edit / Play / No Access. Group games get Edit through role permissions (https://create.roblox.com/docs/projects/collaboration). There are new age-based Team Create constraints: "After completing an age check, you can only collaborate with creators in compatible age groups by default." Anyone with Edit can publish server code, which is equivalent to unlimited item minting.
- The **plugin "Script Injection" permission** prompt is not documented in creator-docs at this commit (grep found nothing). See "Could not verify".

---

## 5. Anti-cheat platform (Hyperion/Byfron)
- creator-docs at 70a0110 contains **no mention** of Hyperion, Byfron or "anti-cheat" (grep across all .md and .yaml files). Official docs treat client integrity as untrusted regardless ("Never trust the client").
- I ran no official-source verification for Hyperion dates in this session (DevForum blocked, no search budget). Sibling ledger rows RBX-011 and RBX-012 (in `roblox_wide_incidents.md`) record:
  - Byfron acquisition in Oct 2022 (DevForum "Welcoming Byfron to Roblox");
  - Hyperion shipping with the 64-bit Windows client in 2023;
  - the Wine block in 2024.

  Cross-reference those; I do not re-assert them here.
- Design implication: anti-tamper raises cost but is not a trust boundary. Every economy check must still be server-side.

## 6. Anti-abuse signals
- `Player.AccountAge`: "how long ago a player's account was registered in days ... set using `SetAccountAge()`, which cannot be accessed by scripts." (https://create.roblox.com/docs/reference/engine/classes/Player)
- `Player:IsVerified(level?)`: "Verification uses concrete, real-world signals, including, but not limited to, phone number or government ID verification." Server-only, and false in Studio. The safety page lists "protecting the integrity of in-game ranking and trading" as a use case (https://create.roblox.com/docs/safety).
- **New (first in repo 2026-08-11):** `Player.AgeChecked` (an `Enum.AgeCheckStatus`, "set by the server and cannot be changed by scripts") and `Player:PromptAgeCheck()`.
- `PolicyService:GetPolicyInfoForPlayerAsync` current fields: AreAdsAllowed, **ArePaidRandomItemsRestricted**, IsContentSharingAllowed, IsEligibleToPurchaseCommerceProduct, IsEligibleToPurchaseSubscription, **IsPaidItemTradingAllowed**, IsPhotoToAvatarAllowed, IsSubjectToChinaPolicies, AllowedExternalLinkReferences ("legacy field. It always returns an empty array"), IsEndlessContentLoadAllowed, IsEndlessContentAutoplayAllowed. (https://create.roblox.com/docs/reference/engine/classes/PolicyService)
- Remote rate limits: there is **no platform-enforced per-remote rate limit** in the docs. The official guidance is developer-implemented server-side token buckets (section 1). Roblox backend APIs have their own limits.
- `Players:BanAsync` (Ban API) is recommended for players failing validation (access-control page).

## 7. Policy
- **Paid random items** (https://create.roblox.com/docs/production/monetization/paid-random-items; page first in repo 2026-05-27, consolidating earlier guidance).
  - Examples explicitly include **"Hatch an egg for a pet"**, plus "Luck boosts", "Pity systems" and combination items.
  - "you must indicate all possible outcomes and the actual numerical odds". Percentages sum to 100%, the (i) icon alone is insufficient, and odds must be updated dynamically for luck boosts and limited-instance outcomes. The rule also applies to indirect purchases via Robux-bought currency.
  - Free-earned randomness needs no disclosure.
  - When `ArePaidRandomItemsRestricted` is true, the game must apply one listed treatment (free earnable path, deterministic order, direct purchase, hide, block or teleport away).
  - When `IsPaidItemTradingAllowed` is false: "creators must not allow them to access the ability to trade the resulting outcome of a paid random item or other paid items." This means pet trading must be **gated per player and per item provenance** (paid versus earned).
- Maturity questionnaire: "If your game includes paid item trading ... you must disclose it within the Maturity & Compliance Questionnaire" (https://create.roblox.com/docs/production/promotion/content-maturity).
- **Account tiers (new, first in repo 2026-05-19):** https://create.roblox.com/docs/production/publishing/kids-and-select
  - "Roblox Kids" (self-declared or checked age 5-8), "Roblox Select" (self-declared 9+ until age-checked, or checked 9-15) and "Roblox" (age-checked 16+).
  - Chat is off for self-declared Select accounts. Games for under-16s must pass an evaluation.
  - Parents have "Visibility into friends, screen time, and spending available through age 18."
- Off-platform and real-money trading prohibitions in the ToS and Community Standards: the docs link to them (`about.roblox.com/community-standards#roblox-economy-paid-random-items`) but I could **not read** them (blocked). Not verified verbatim.
- Subscriptions guidance: "using the Roblox app to direct users to purchase elsewhere is prohibited."

---

## Changed/deprecated guidance (vs. ~2019 common practice)

| Topic | Old belief/practice | Current (commit 70a0110) | First in docs repo* |
|---|---|---|---|
| FilteringEnabled | Toggle per place | "discontinued and no longer takes effect" | ≤2023-11-02 |
| Receipt handling | Only `ProcessReceipt` | `BindReceiptHandler` + `Enum.ReceiptDecision` (falls through to ProcessReceipt) | 2026-04-02 / 2026-05-04 |
| Unresolved receipts | Often believed auto-refunded after ~3 days | "not removed or refunded after the escrow period expires" | 2025-01-21 |
| Purchase channel | All in-game | `ProductPurchaseChannel` (Store tab, AdReward, CommerceProduct) | 2025-01-21 |
| Refund handling | No signal for dev products | "Transaction Refunded" webhook; passes auto-revoked by CS | 2026-09-03 / 2026-10-01 |
| Player→player Robux | Not possible in-game (group payouts/gamepass tricks) | `PromptRobuxTransferAsync` (Plus subscribers, 10-500 R$, 10% to game) | 2026-04/05 |
| Cross-game pass/product sales | Used as donation workaround | Disabled from 2026-05-30 | 2026-07-07 |
| InsertService:LoadAsset | Primary loader | `AssetService:LoadAssetAsync` "modern replacement", sandboxed by default; opt-in third-party | 2025-10-22 |
| Asset privacy | Audio privacy 2022; all public otherwise | Restricted/Open Use for Images/Decals/Meshes (opt-in); Open Use irreversible; game grants permanent | (page current) |
| Security docs | Single "Security tactics" page | Multi-page: client-server boundary (NaN, rate-limit token bucket, trading dupe), access control, network ownership, third-party | 2026-01-14 |
| Rate limiting | Folk practice | Official token-bucket reference | 2026-01-14 |
| Subplace access | Kick-on-join | "Secure within universe only" platform setting | 2026-02-18 |
| Movement anti-cheat | Heuristics | Server authority model (beta) | 2025-12-09 |
| DataStore storage | Unlimited in practice | 500 MB + 1 MB × lifetime users | 2026-07-14 |
| GetAsync cache | 4 s, no opt-out | 4 s, `UseCache=false` opt-out | 2025-04-07 (text) |
| Age signals | AccountAge only | `IsVerified`, `AgeChecked`, `PromptAgeCheck`, Kids/Select tiers | 2023-11 / 2026-08-11 / 2026-05-19 |
| Paid random items | Odds disclosure in Community Standards | Dedicated page; "Hatch an egg for a pet" listed; pity/luck count | page 2026-05-27; "actual numerical odds" text and IsPaidItemTradingAllowed/ArePaidRandomItemsRestricted present since ≤2023-08-29 (repo start) |

*Doc-repo commit date (history begins 2023-08-29). This is not necessarily the platform release date.

## Could not verify
- The exact date FilteringEnabled became mandatory (commonly cited as 2018). There is no official source reachable, and the docs carry no date.
- Hyperion/Byfron rollout dates and executor landscape from official sources. I made no searches (budget exhausted) and the docs have no mention. Defer to RBX-011 and RBX-012.
- Verbatim ToS and Community Standards text on real-money trading, off-platform sales or account trading. Pages are blocked, and the docs only link to them.
- Any 2024-2026 DevForum or newsroom announcement wording or dates (age checks for chat, parental controls, Robux transfers launch post, BindReceiptHandler announcement). The docs confirm the features exist but not the announcement dates.
- The Studio plugin "Script Injection" permission. It is not in creator-docs at this commit.
- Live rendering of create.roblox.com (blocked). The content was verified from its source repo instead.
- Whether the Server authority beta has gone GA after 2026-10-17. The docs still say beta.
- Whether `IsPaidItemTradingAllowed` or `ArePaidRandomItemsRestricted` are true or false for specific regions or ages. The docs don't enumerate this.
