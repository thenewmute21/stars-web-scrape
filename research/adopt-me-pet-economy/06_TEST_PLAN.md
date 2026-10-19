# 06 — Test Plan: Economy Integrity (Our Own Experience Only)

Execution date: 2026-10-19. This plan pairs with `05_SECURE_ARCHITECTURE.md`. Section references
like "F4" point to the verified platform facts table in 05 §1.

> **Read first**
> - **A passing harness ≠ production secure.** These tests check our *reference* logic against
>   *simulated* platform behaviour. Real Roblox services can behave in ways no fake reproduces: throttling shapes,
>   redelivery timing, lock-expiry skew, and undocumented limits. Treat a green suite as *necessary, not sufficient*,
>   and pair it with staging soak tests, reconciliation jobs (05 §11) and an external review.
> - **Run tests ONLY against our own private test universe and local mocks.** Never against any third-party
>   game, live production data stores, other creators' experiences, or Roblox services beyond normal use of our
>   own staging universe. No exploit tooling or executors are used or needed. Every "attack" here is an innocuous
>   simulated input sent by our own test code into our own functions.

---

## 1. Test environment setup

### 1.1 Separate universes

| Environment | Purpose | Data stores | Who publishes |
|---|---|---|---|
| `Local` (Studio, unpublished or offline) | Unit and fault-injection tests with **FakeDataStore** only | None; injected fakes | Any developer |
| `Staging` universe, separate experience and group-owned | Integration, multi-client, soak, BindToClose tests | Staging data stores. "Enable Studio Access to API Services" is ON here only (F15). | CI from `main` |
| `Prod` universe | Live | Prod data stores. Studio API access is **OFF**. | CI release gate only |

- Staging uses **distinct DataStore names** as well, such as `Profiles_v1_stg`, as defence in depth in case a place file is ever
  published to the wrong universe. The boot script asserts `game.GameId == EXPECTED_GAME_ID[env]` and refuses to
  start the economy if they don't match.
- **Synthetic accounts:** use a small pool of team-owned test accounts in a private group with test roles.
  Never use real players' accounts or data. In unit tests, UserIds are fake integers such as `-1001` and `-1002`. Roblox
  Studio local test players already use negative ids.
- Developer products in staging are separate products. Purchases in Studio test mode are simulated by the engine.
  For receipt logic, call the handler directly with synthetic receipt tables, as in §4.

### 1.2 Multi-client and local server testing

- Studio **Test → Server & Clients** runs a local server plus N clients for trade UI and race testing. The docs
  also describe `StudioTestService` for programmatic multi-client simulation, with up to 8 simulated clients, mid-session joins
  and triggered client disconnects. Source: https://create.roblox.com/docs/studio/testing-modes (verified in the
  creator-docs source at commit 70a0110, 2026-10-17; create.roblox.com itself was unreachable from this environment).
- **Multiple servers** cannot be simulated in one Studio session. For "two servers process the same receipt" and
  "lock steal" tests, instantiate **two server-side module instances** (`ServerA` and `ServerB`), each with its own `serverLockId`, that share one
  `FakeDataStore` backend. Confirm in staging with two live servers by joining, leaving and rejoining with synthetic accounts.

### 1.3 Test framework, status as of 2026-10-19

| Option | Status found | Notes |
|---|---|---|
| **Jest-Lua** (`jsdotlua/jest-lua`) | Active community fork. The latest tag I saw is `v3.10.0`, and its README describes it as production-ready and run inside Roblox. | Recommended. Jest-style API with `describe`, `it`, `expect` and mocks. |
| `Roblox/jest-roblox` | The Roblox org lists it as a **read-only mirror**. The latest tag I saw is `v3.8.0`. | Use the jsdotlua fork instead. |
| **TestEZ** (`Roblox/testez`) | Search results show the Roblox org marking it **archived**. The latest tag is `v0.4.2`. | Still works, but is unmaintained. Fine for legacy code; avoid for new code. |
| Roblox Studio Assistant "unit tests" skill | The docs list a skill that detects Jest-Lua or TestEZ, with a built-in fallback harness. | https://create.roblox.com/docs/assistant/skills |

I verified tags with `git ls-remote`. The archive and read-only status comes from web search and the GitHub org listing, and **I did not
open the repos' GitHub pages directly**, so re-check before adopting. The fixtures below are framework-agnostic, using plain
`assert`, so they port to either.

Runner: Rojo syncs `src/` and `tests/` into a test place, and CI runs the suite in a headless Roblox runner. Options
include Open Cloud Luau Execution against a **staging** place, or `run-in-roblox`. Pick per team. Verify the current
CI-runner availability yourself, because I did not verify it here.

---

## 2. Global invariants checked after every test

| ID | Invariant |
|---|---|
| INV-1 | Every `PetRecord` has `mintSource` in the enum and a `mintRef` present in that profile's `mintRefs` or ledger, or it arrived through a trade ledger entry. |
| INV-2 | No `petId` is `Owned` in more than one profile across all fake profiles. |
| INV-3 | Every `PurchaseId` that returned `PurchaseGranted` exists in the **persisted** profile, and each produced exactly one grant. |
| INV-4 | No profile has `trades[tradeId]` while the trade record is in a terminal state, once `recover()` has run. |
| INV-5 | Total pets of each kind is conserved by trades: Σ before = Σ after, counting only `Owned`. |
| INV-6 | Currency is finite, an integer and ≥ 0 in every persisted profile. |
| INV-7 | An errored session never wrote to the store. Checked against the FakeDataStore write log. |

A helper `assertInvariants(fakeStore)` decodes all `u_*` and `t_*` keys and checks INV-1 to INV-7.

---

## 3. Deterministic test matrix

Columns: **Setup** · **Simulated input**, which is innocuous and generated by our own test code · **Invariant** ·
**Expected deny/recovery** · **Logging** · **Pass criterion**.

| ID | Scenario | Setup | Simulated input | Invariant | Expected deny / recovery | Logging | Pass criterion |
|---|---|---|---|---|---|---|---|
| T01 | Parallel trade requests | A owns pet P. Two trades are proposed: A↔B and A↔C. | P is offered in both and both confirm in the same frame, using `task.spawn` ×2. | INV-2, INV-5 | The first prepare sets P to `EscrowOut`. The second prepare fails `isTradeable`, so that trade is Aborted and compensated. | `trade_abort reason=NotTradeable` | Exactly one trade is Committed and P is Owned by exactly one user. |
| T02a | Disconnect before Committing | Trade in `Locked` | B's session is removed, simulating PlayerRemoving | INV-5 | The in-memory trade is dropped and nothing is persisted. | `trade_cancel reason=left` | No `t_` key exists and the profiles are unchanged. |
| T02b | Crash after the trade record is created | Fault: the process stops after `t_` is created | Kill the coroutine | INV-4 | The record stays `Committing`. After the deadline, recovery CASes it to Aborted, and the profiles have no markers. | `trade_recover action=abort` | Profiles are unchanged and the record is Aborted. |
| T02c | Crash after A is prepared, before B | Fault: stop after `saveA` | — | INV-2, INV-5 | On A's reload past the deadline: CAS to Aborted, then compensate, so P returns to `Owned` in A and PendingIn is removed. | `trade_recover action=compensate` | Same as the starting state |
| T02d | Crash after both are prepared, before the CAS | Same, stop after `saveB` | — | INV-2 | The deadline passes, recovery aborts, and both are compensated. | — | Same as the starting state |
| T02e | Crash after the CAS to Committed, before finalize | Stop after the CAS | — | INV-2, INV-5 | On reload both roll forward and finalize. | `trade_recover action=finalize` | Items are swapped exactly once. |
| T02f | Crash after finalize A, before finalize B save | Stop after `saveA` in finalize | — | INV-4 | B's reload finalizes. A is unchanged on replay because finalize is idempotent. | — | Swapped once and no markers remain. |
| T03 | Repeated purchase receipt | Profile loaded | Same receipt table delivered ×5, sequentially | INV-3 | The first delivery grants and saves, returning Granted. Deliveries 2 to 5 return Granted with no new mint. | `receipt_dup pid=…` | Exactly 1 pet and `mintRefs` has 1 entry. |
| T04 | Receipt delivered to multiple servers | ServerA holds the lock. ServerB shares the fake store. | The same receipt goes to A and B concurrently. | INV-3 | B cannot get the lock and returns NotProcessedYet. A returns Granted. If A then releases, B loads, sees the PurchaseId and returns Granted without minting. | `receipt_nolock server=B` | One grant in total |
| T05 | DataStore transient failure or throttle | `FakeDataStore.failNext(n, "Throttled")` | Save during a receipt | INV-3, INV-7 | The receipt returns NotProcessedYet. The item stays held (`holdUntilPersisted`). The next autosave succeeds, and redelivery returns Granted with no re-mint. | `ds_error code=…` | One pet, persisted, and the hold is cleared. |
| T06 | Save replay, a stale write | ServerA saves v1, then ServerB steals the lock and saves v2. | A replays an old queued save. | INV-2, INV-7 | A's lock check fails, so the write is cancelled, and A's session becomes errored. | `lock_lost` | The store holds v2 and A's write count is unchanged. |
| T07 | Invalid or malformed currency | Shop remote handler | Amounts: `0/0` (NaN), `math.huge`, `-math.huge`, `-5`, `1e308`, `2^53+1`, `"100"`, `{}`, `nil`, `true`, `1.5` | INV-6 | `Validation.int` returns nil, so the call is denied with no state change. | `validation_fail field=amount` | Coins are unchanged for all 11 inputs. |
| T08 | Missing pet ID | Trade in Proposed | `setOffer({nil, id})`, `{}` with holes, `{[1]=id,[3]=id}`, `{foo=id}` | INV-5 | `petIdList` returns nil, so the call is denied. | `validation_fail field=offer` | The offer is unchanged. |
| T09 | Incorrect ownership | A in a trade | A offers B's pet id, or a random GUID | INV-2 | `isTradeable` is false, so the call is denied. | `trade_deny NotOwnedOrHeld` | The offer is unchanged. |
| T10 | Forged client UI state | Trade in Locked at v=3 | Client sends `confirm(v=2)`, `confirm(v=99)`, or confirm for a trade id it doesn't belong to | — | Ignored because of the version mismatch or the participant check. | `trade_stale_confirm` | The state stays Locked. |
| T11 | Unpublished or unauthorized imported asset id | Catalog has `fox_basic` | Remote sends `kind="rbxassetid://123"`, an unknown kind, or a numeric asset id | INV-1 | Rejected, because mint only accepts catalog kinds and no code path calls `LoadAsset` with input. A CI lint test also scans the source for dynamic `LoadAsset` calls. | `mint_deny BadKind` | No pet is minted and the lint passes. |
| T12 | Unauthorized role or admin call | Prod build profile | Call any admin remote name from the client harness | — | The remote doesn't exist in the prod build. In staging, the role check denies it. | `admin_deny userId=…` | No state change, and a test asserts the remotes are absent from the prod build. |
| T13 | Restore / regrant replay | Restore inbox ticket R1 | Process R1 twice, and on two servers | INV-1, INV-2 | `mintRefs["Restore:R1:1"]` makes it idempotent, and the original id is revoked on load. | `restore_dup` | One restored pet, and the original shows as Revoked wherever it appears. |
| T14 | Account or schema migration | Fixture profiles v0, v1, and a "future" v99 | Load each | INV-1, INV-6 | v0 and v1 migrate idempotently: running twice gives the same result. v99 is refused, the session is errored, and nothing is saved. | `schema_refuse v=99` | Migrated equality holds and v99 is untouched. |
| T15 | Promotion stacking | Two promos active | Claim promo A and B repeatedly, including concurrently | INV-1 | The server rule allows one promo per type. Claims are idempotent by `Event:promoId:userId`. | `promo_deny stacked` | Exactly the allowed grants |
| T16 | Event-rate spikes | Rate limiter config | 1,000 `TradeEdit` calls in 1 s from one player | — | At most burst plus rate×t calls are allowed; the rest are dropped cheaply. Other players are unaffected. | Sampled `ratelimit_drop` | Allowed count ≤ 10 + 5×1, and server time per call stays bounded. |
| T17 | Lag and race between offer change and confirm | Locked | B changes the offer between A's confirm and B's confirm, with an injected yield | INV-5 | The change resets to Proposed, and A's earlier confirm is invalid. | `trade_reset` | No commit with a mismatched offer |
| T18 | Server shutdown during save (BindToClose) | 20 sessions, fake latency of 0.5 to 5 s | Trigger the shutdown handler | INV-3, INV-7 | Parallel saves, stale queued writes skipped, done in under 30 s (F8). Sessions not saved keep their lock, which expires. | `shutdown_save ok=… fail=…` | All saved within the simulated 30 s budget. Any failures are recoverable on the next load. |
| T19 | Session-lock steal | A holds the lock. The fake clock advances past `LOCK_TTL` without a refresh. | ServerB loads and acquires the lock. A then tries to save. | INV-7 | A detects the stolen lock and goes errored, read-only and kick. B is authoritative. | `lock_stolen` | The store holds B's writes only. |
| T20 | Trade expiry | Proposed or Locked | No action for longer than the session timeout, or a Committing record past its deadline | INV-4 | In-memory trades abort. Durable records are aborted on recover. | `trade_expire` | Terminal states, no frozen items left |
| T21 | Double-accept | Locked | The same player confirms ×3 quickly | — | Idempotent, with one commit spawned. The `t_` create-if-absent rule prevents a second record. | — | One record, one swap |
| T22 | Item changed after accept | A confirmed | A removes or adds a pet | INV-5 | `setOffer` resets both confirmations and version++. | `trade_reset` | Needs a fresh double confirm |
| T23 | Teleport between places mid-trade | Committing in progress | The player teleports (session save and release) and the destination loads the profile | INV-2, INV-4 | The destination load runs `recover()`. Items stay frozen until the decision. Gameplay teleport is blocked in Locked and later. | `trade_recover` | Converges to the same final state as T02 cases |
| T24 | Trade record write fails | `failNext` on `t_` create | Commit | INV-5 | No profile changes and the trade is Aborted. | `trade_abort reason=coord` | Profiles are unchanged. |
| T25 | Coordinator CAS returns unknown, e.g. DataStore down | Fail the CAS repeatedly | Commit | INV-2 | Items stay frozen and nothing is guessed. Recover resolves once the service returns. | `trade_unknown` | Never Owned in two places |

---

## 4. Fixtures

### 4.1 `FakeDataStore.luau`, fault injection

```lua
--!strict
-- TEST FIXTURE ONLY. Simulates UpdateAsync/GetAsync semantics we rely on (F4, F5):
--  * UpdateAsync transform gets (value, keyInfo) and may return nil to cancel
--  * transform must not yield (we enforce by running it in a coroutine and erroring on yield)
--  * metadata + userIds round-trip
--  * injectable failures, throttle, latency, and a concurrent-writer hook that forces a re-run
local HttpService = game:GetService("HttpService")

export type Fault = { kind: "Error" | "Throttled" | "Dropped", count: number }
local Fake = {}
Fake.__index = Fake

function Fake.new(clock: (() -> number)?)
	local self = setmetatable({}, Fake)
	self.data = {} :: { [string]: string }            -- JSON-encoded, like the real store
	self.meta = {} :: { [string]: { [string]: any } }
	self.version = {} :: { [string]: number }
	self.updatedAt = {} :: { [string]: number }
	self.faults = {} :: { Fault }
	self.latency = 0
	self.writeLog = {} :: { { key: string, by: string? } }
	self.beforeCommit = nil :: ((key: string) -> ())?  -- hook to simulate a racing writer
	self.clock = clock or os.time
	return self
end

function Fake:failNext(count: number, kind: ("Error" | "Throttled" | "Dropped")?)
	table.insert(self.faults, { kind = kind or "Error", count = count })
end

local function maybeFail(self: any)
	local f = self.faults[1]
	if f then
		f.count -= 1
		if f.count <= 0 then table.remove(self.faults, 1) end
		error(("FakeDataStore %s"):format(f.kind))     -- callers must pcall, like the real API
	end
	if self.latency > 0 then task.wait(self.latency) end
end

local function keyInfo(self: any, key: string)
	local meta = table.clone(self.meta[key] or {})
	return {
		Version = tostring(self.version[key] or 0),
		UpdatedTime = (self.updatedAt[key] or 0) * 1000,
		GetMetadata = function() return table.clone(meta) end,
		GetUserIds = function() return {} end,
	}
end

local function runNoYield(fn: (...any) -> ...any, ...: any): ...any
	local co = coroutine.create(fn)
	local res = table.pack(coroutine.resume(co, ...))
	if not res[1] then error(res[2]) end
	if coroutine.status(co) ~= "dead" then error("UpdateAsync transform yielded") end
	return table.unpack(res, 2, res.n)
end

function Fake:UpdateAsync(key: string, transform: (any, any) -> (any, any?, any?))
	assert(#key <= 50, "key too long")                 -- F5
	maybeFail(self)
	for _ = 1, 5 do                                     -- re-run on concurrent write (F4)
		local seenVersion = self.version[key] or 0
		local current = self.data[key] and HttpService:JSONDecode(self.data[key]) or nil
		local newValue, _userIds, newMeta = runNoYield(transform, current, if current then keyInfo(self, key) else nil)
		if newValue == nil then return nil, nil end     -- cancelled
		if self.beforeCommit then self.beforeCommit(key) end
		if (self.version[key] or 0) == seenVersion then
			local encoded = HttpService:JSONEncode(newValue)
			assert(#encoded <= 4194304, "value too large")
			assert(utf8.len(encoded) ~= nil, "invalid utf8")
			self.data[key] = encoded
			self.meta[key] = newMeta or {}
			self.version[key] = seenVersion + 1
			self.updatedAt[key] = self.clock()
			table.insert(self.writeLog, { key = key, by = newMeta and newMeta.LockId })
			return newValue, keyInfo(self, key)
		end
	end
	error("FakeDataStore contention")
end

function Fake:GetAsync(key: string): any
	maybeFail(self)
	local raw = self.data[key]
	return if raw then HttpService:JSONDecode(raw) else nil
end

return Fake
```

Notes:
- JSON round-tripping catches non-serialisable values such as Instances, NaN and mixed tables, the same way the real store would reject them.
  Note that `HttpService:JSONEncode` behaviour on NaN and inf differs from DataStore. Keep the explicit validation tests (T07) as well.
- `beforeCommit` lets a test simulate "another server wrote between read and write", which forces the documented
  transform re-run (F4).
- The fake clock is injected, so lock expiry (T19) and trade deadlines (T20, T02b) are deterministic. In the fixture, also route
  `os.time` uses in modules through an injected clock.

### 4.2 `FakeSession.luau`

```lua
--!strict
-- TEST FIXTURE. Minimal session over FakeDataStore using SessionStore.lockedTransform.
local SessionStore = require(script.Parent.Parent.src.SessionStore)
local FakeSession = {}

function FakeSession.load(store: any, userId: number, serverLockId: string, seed: any?)
	local key = "u_" .. userId
	local out = { ok = false }
	local prevId = SessionStore.serverLockId
	SessionStore.serverLockId = serverLockId          -- simulate a distinct server
	local ok, value = pcall(store.UpdateAsync, store, key, SessionStore.lockedTransform(function(cur)
		return cur or seed or { schema = 1, userId = userId, coins = 0, ledgerSeq = 0,
			pets = {}, purchases = {}, mintRefs = {}, trades = {}, outbox = {} }
	end, false, out))
	SessionStore.serverLockId = prevId
	local s: any = { profile = value, loaded = ok and out.ok, errored = not (ok and out.ok), unsavedPurchases = {} }
	function s.save(self: any): boolean
		if self.errored then return false end           -- INV-7
		local o = { ok = false }
		local prev = SessionStore.serverLockId
		SessionStore.serverLockId = serverLockId
		local okSave = pcall(store.UpdateAsync, store, key, SessionStore.lockedTransform(function()
			return self.profile
		end, false, o))
		SessionStore.serverLockId = prev
		if okSave and not o.ok then self.errored = true end   -- lock lost/stolen (T06, T19)
		return okSave and o.ok
	end
	return s
end

return FakeSession
```

---

## 5. Example tests (framework-agnostic, using `assert`)

```lua
--!strict
-- tests/Receipt.spec.luau  (TEST CODE; synthetic receipts; no real purchases)
local Fake = require(script.Parent.fixtures.FakeDataStore)
local FakeSession = require(script.Parent.fixtures.FakeSession)
local ReceiptHandler = require(script.Parent.Parent.src.ReceiptHandler)

local GRANTED = Enum.ProductPurchaseDecision.PurchaseGranted
local NOT_YET = Enum.ProductPurchaseDecision.NotProcessedYet

local function receipt(pid: string)
	return { PurchaseId = pid, PlayerId = -1001, ProductId = 0000001, CurrencySpent = 0,
		CurrencyType = Enum.CurrencyType.Robux, PlaceIdWherePurchased = 0 }
end
local function countPets(p: any) local n = 0; for _ in p.pets do n += 1 end; return n end

-- T03: repeated receipt
do
	local store = Fake.new()
	local s = FakeSession.load(store, -1001, "server-A")
	ReceiptHandler.start(function() return s end)
	for _ = 1, 5 do
		assert(ReceiptHandler._process(receipt("pid-1")) == GRANTED)
	end
	assert(countPets(s.profile) == 1, "T03: exactly one grant")
	local persisted = store:GetAsync("u_-1001")
	assert(persisted.purchases["pid-1"] ~= nil, "T03: PurchaseId persisted with grant")
end

-- T04: same receipt on two servers sharing one store; only the lock holder grants
do
	local store = Fake.new()
	local a = FakeSession.load(store, -1001, "server-A")
	local b = FakeSession.load(store, -1001, "server-B")       -- lock held by A -> errored
	assert(a.loaded and not b.loaded, "T04: B must not acquire lock")
	ReceiptHandler.start(function() return b end)
	assert(ReceiptHandler._process(receipt("pid-2")) == NOT_YET, "T04: B must not grant")
	ReceiptHandler.start(function() return a end)
	assert(ReceiptHandler._process(receipt("pid-2")) == GRANTED)
	assert(countPets(a.profile) == 1)
end

-- T05: transient failure on save -> NotProcessedYet, held, then granted without re-mint
do
	local store = Fake.new()
	local s = FakeSession.load(store, -1001, "server-A")
	ReceiptHandler.start(function() return s end)
	store:failNext(1, "Throttled")
	assert(ReceiptHandler._process(receipt("pid-3")) == NOT_YET)
	local petId = next(s.profile.pets)
	assert(s.profile.pets[petId].holdUntilPersisted, "T05: held until persisted")
	assert(ReceiptHandler._process(receipt("pid-3")) == GRANTED, "T05: redelivery persists")
	assert(countPets(s.profile) == 1, "T05: no re-mint")
end
print("Receipt specs passed (harness only; not a production guarantee)")
```

```lua
--!strict
-- tests/Validation.spec.luau  (T07, T08)
local V = require(script.Parent.Parent.src.Validation)
local bad: { any } = { 0/0, math.huge, -math.huge, -5, 1e308, 2^53 + 1, "100", {}, true, 1.5 }
for i, v in bad do
	assert(V.int(v, 0, 1e9) == nil, "T07 case " .. i)
end
assert(V.int(nil, 0, 1e9) == nil)
assert(V.int(250, 0, 1e9) == 250)

local g = "123e4567-e89b-42d3-a456-426655440000"
assert(V.petIdList({ g }, 9) ~= nil)
assert(V.petIdList({ [1] = g, [3] = g }, 9) == nil, "T08: holes")
assert(V.petIdList({ foo = g } :: any, 9) == nil, "T08: non-array")
assert(V.petIdList({ g, g }, 9) == nil, "T08: duplicates")
assert(V.str("\255", 10) == nil, "invalid UTF-8")
print("Validation specs passed")
```

```lua
--!strict
-- tests/TradeRecovery.spec.luau  (T02c: crash after A prepared, before B)
local Fake = require(script.Parent.fixtures.FakeDataStore)
local FakeSession = require(script.Parent.fixtures.FakeSession)
local TradeService = require(script.Parent.Parent.src.TradeService)

local now = 1_000_000
local store = Fake.new(function() return now end)
TradeService.init({ update = function(k, fn)
	return pcall(store.UpdateAsync, store, k, fn)
end })
-- Seed: A has pet P (Owned) and a marker for trade T; record T is Committing with deadline=now+120.
local P = "123e4567-e89b-42d3-a456-426655440000"
local a = FakeSession.load(store, -1001, "server-A")
a.profile.pets[P] = { id = P, kind = "fox_basic", state = "EscrowOut", tradeId = "T",
	mintSource = "Hatch", mintRef = "egg1", mintedAt = 0, originUserId = -1001 }
a.profile.trades["T"] = "Prepared"
assert(a:save())
store:UpdateAsync("t_T", function() return { state = "Committing", deadline = now + 120 } end)

now += 121  -- coordinator "crashed"; deadline passes (fake clock must also drive os.time in src)
TradeService.recover(a, function(k) return store:GetAsync(k) end)
assert(a.profile.pets[P].state == "Owned", "T02c: compensated back to Owned")
assert(a.profile.trades["T"] == nil, "T02c: marker cleared")
assert(store:GetAsync("t_T").state == "Aborted", "T02c: presumed abort recorded")
print("TradeRecovery spec passed")
```

> Note: the reference `TradeService` calls `os.time()` directly. For T02b, T02c and T20 to be deterministic, inject a
> clock in the real module (`TradeService.init(store, clock)`). Leaving `os.time` hard-coded is a known gap in the
> reference code.

---

## 6. Staging-only integration and soak tests (synthetic accounts)

| ID | What | How | Pass |
|---|---|---|---|
| S1 | Real receipt redelivery on rejoin | Buy a staging-only test product with a team account. Kill the server before save using a debug flag present only in staging. Rejoin. | Exactly one grant. The ledger shows a single Mint for that PurchaseId. |
| S2 | Lock behaviour across real servers | Two staging servers. Quick leave→join hop with a synthetic account. | No double load. Logs show `NotProcessedYet` or a retry, never a duplicate. |
| S3 | BindToClose under load | 30 bots or test accounts. Use "Shut down all servers" in the staging universe. | All profiles saved within 30 s. No lost data on reload. |
| S4 | Reconciliation jobs | Run the export and reconciliation on staging after S1 to S3 | Mint vs receipt match, no duplicate Owned ids |
| S5 | Budget headroom | Soak with autosave plus ledger flush at target CCU per server | No `DatastoreThrottled` or `KeyThrottled` above the agreed threshold (F5). Queue never above 30. |

**Out of scope, deliberately:** testing other developers' games, live production data, probing Roblox services
beyond documented use, or running any third-party exploit tooling.

---

## 7. Exit criteria

- All T-tests and S-tests pass. INV-1 to INV-7 hold after every test. The P0 checklist in 05 §14 is fully ticked.
- **And** an independent reviewer has read the commit, recovery and receipt paths.
- **And** reconciliation alerts are live in production on day 1.
- Reminder: **a passing harness ≠ production secure.** It reduces known-bug risk. It does not prove the absence of others.
