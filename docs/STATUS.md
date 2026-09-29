# Phase status

## Latest DeadlineCheck evaluation verified read-only — 2026-09-29

Public Studio-dev sender history (`sim_getTransactionsForAddress`) on chain
**61997** contains one matching `evaluate_delay` call to
`0x661F31a2017CFC3Cd48D0D6b6978415FAf0A6c59` with the exact case ID
`python-3130-final-1790441362822`. The sender is the documented authorized
`0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`. The matching transaction,
discovered from public history, is
`0xab0d76161b329074a8294da16719de56ac9a3f5b5e21eb82f64c7a1c514cebb9`
(nonce **15**, created **2026-09-29 11:33:45 UTC**).

The SDK transaction is **FINALIZED / code 7**; stored and projected lifecycle
statuses are both Finalized. Execution is **FINISHED_WITH_RETURN / code 1**,
and the envelope receipt status is `0x1`. The executing leader and three
executing validators each report `SUCCESS`, null return (`AAA=`), and no
execution errors. One idle leader and one idle validator were cancelled after
quorum; neither cancellation is a failed contract execution.

After confirming finalization, read-only `get_case` for the exact case ID
returned these stored values:

| Field | Stored value |
| --- | --- |
| `verdict` | `INSUFFICIENT_EVIDENCE` |
| `responsible_party` | `UNKNOWN` |
| `reason_code` | `EXTRACTION_FAILED` |
| `approved_days` | `0` |
| `explanation` | `The model assessment could not be parsed or its extracted facts failed strict validation.` |

This is a **fail-closed** outcome, not a substantive decision on responsibility
or extension days. The separate [public read-only evidence](../deployments/evidence/evaluation-ab0d7616-2026-09-29.json)
contains the matching history row and calldata, transaction, receipt,
lifecycle, and raw and parsed case read. No wallet access, transaction,
retry, code change, or test rerun occurred.

## Latest DeadlineCheck deployment verified read-only — 2026-09-29

Transaction `0xd135ca65b420c70f1c12fb427091d1adccb93ae8d5f1cbe35b04684815b2965b`
on Studio-dev (chain ID **61997**) is **FINALIZED / code 7**; stored and
projected lifecycle statuses are both Finalized. The SDK transaction identifies
contract `0x661F31a2017CFC3Cd48D0D6b6978415FAf0A6c59` and the documented
authorized sender `0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`.
The envelope receipt matches the transaction and sender and has status `0x1`.
Its `contractAddress` field is null, as in prior Studio-dev deployments.

Constructor execution is **FINISHED_WITH_RETURN / code 1**. The executing
leader and three agreeing validators each returned `SUCCESS`, null (`AAA=`),
and no execution errors. One idle leader and one idle validator were cancelled
after quorum; neither was counted as an executed constructor receipt. The
deployed code, submitted source, and local `contracts/DeadlineCheck.py` are
each **21,785 bytes / SHA-256
`e1590172ff6211243a67c8d9a83da5813adcb02988253604c3fde9efc186ddfb`**.

The live schema matches the documented ABI: a no-argument constructor, write
`evaluate_delay(case_id, milestone_url, evidence_url_1, evidence_url_2,
requested_days)`, and read-only `get_case(case_id) -> string`. Read-only
`get_case("verify-missing-1790680429789")` returned the empty string for a fresh
unused ID, as documented. The separate [public read-only evidence](../deployments/evidence/deployment-d135ca65-1790680430517.json)
records the receipt, lifecycle, source hashes, schema, and missing-case read.
The existing deployment verifier was reused with the new public identifiers
and idle leader receipts excluded from the executed count. No wallet access,
transaction submission, `evaluate_delay`, redeployment, code change, or test
rerun occurred.

## Smaller model assessment schema prepared locally — 2026-09-28

The local contract now requests only `obligation`, `deadline`, `completion`,
`owner_cause`, `blockers`, and `conflict` from each independent model assessment.
The optional owner cause is one quoted fact; each of at most four flat external
blocker intervals has one source, one quote supporting both dates and causal
effect, and start/end ISO dates that must occur verbatim in that quote. This
conservative rule can reject natural-language interval dates. Source 0 must
support the original obligation and deadline. Every supplied fact still has an
exact source index and literal quote checked against the fetched body. The model
does not supply a verdict, party, days, or explanation. Contract code derives
all four canonical fields and a fixed explanation, clips and merges supported
external intervals, and caps positive days at the request. Missing or conflicting
evidence produces zero days; malformed assessment facts produce the existing
`EXTRACTION_FAILED` zero-day result. Each leader and validator still fetches and
assesses independently before canonical agreement and the single storage write.

Focused checks: `tests/test_phase1c.py` **72 passed**; pinned semantic/schema
check passed; source-packaging test and offline source-packaging check passed.
The public `evaluate_delay` and `get_case` ABI and stored record schema remain
unchanged. New local contract source: **21,785 bytes / SHA-256
`e1590172ff6211243a67c8d9a83da5813adcb02988253604c3fde9efc186ddfb`**.
This source was subsequently deployed and verified above. Both prior finalized
live evaluations stored `EXTRACTION_FAILED`; their raw model outputs remain
unavailable, so no specific root cause or live improvement is proven. Hosted
model compliance, independent validator agreement, and a substantive live
decision still require a separately authorized evaluation of this deployment.
No wallet access, transaction,
redeployment, dependency change, frontend build, or unrelated test run occurred.

## Latest DeadlineCheck evaluation verified read-only — 2026-09-28

Public Studio-dev sender history (`sim_getTransactionsForAddress`) on chain
**61997** identified one `evaluate_delay` call to
`0x82f868B5aCAfAe5a60d560e442a63B7d22eD26D7` containing the exact case ID
`python-3130-final-1790441362822`. It came from the documented authorized
sender `0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`, with nonce **13**,
created **2026-09-28 11:42:00 UTC**. The matching public transaction hash is
`0x9290fb18eaf651779a2ed081af5d73c061f6ce88b93638016419d90234cbbe36`.
This hash was discovered from history, not inferred from the manual output.

The SDK transaction and stored protocol status are **FINALIZED / code 7**;
stored and projected lifecycle status are both Finalized. Execution is
**FINISHED_WITH_RETURN / code 1** and the envelope receipt has status `0x1`.
The two executing leader receipts and two executing validator receipts report
`SUCCESS`, null return (`AAA=`), and no execution errors. Two idle validators
were cancelled after quorum; their cancellation is not a failed contract call.

After confirming finalization, read-only `get_case` for the exact ID returned:

| Field | Stored value |
| --- | --- |
| `verdict` | `INSUFFICIENT_EVIDENCE` |
| `responsible_party` | `UNKNOWN` |
| `reason_code` | `EXTRACTION_FAILED` |
| `approved_days` | `0` |
| `explanation` | `The model assessment could not be parsed or its extracted facts failed strict validation.` |

This is an **EXTRACTION_FAILED fail-closed result**, not a substantive decision
on the release delay. The separate [public read-only evidence](../deployments/evidence/evaluation-9290fb18-1790596039368.json)
records the matching history row and calldata, transaction, receipt, lifecycle,
and raw and parsed case read. No wallet access, new transaction, retry, contract
change, or test rerun occurred.

## Latest DeadlineCheck deployment verified read-only — 2026-09-28

Transaction `0x6441f29961be9b541d2846a636423b2bdad09cd5fd1fecec396e71c463ff160c`
on Studio-dev (chain ID **61997**) is **FINALIZED / code 7**, with both stored
and projected lifecycle status Finalized. The SDK transaction identifies the
deployed contract as `0x82f868B5aCAfAe5a60d560e442a63B7d22eD26D7` and
the documented authorized sender as
`0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`. The envelope receipt has
status `0x1` and matches the transaction hash and sender; its `contractAddress`
field is null, as in the prior deployment.

Constructor execution is **FINISHED_WITH_RETURN / code 1**. The executing
leader and three agreeing validators each report `SUCCESS`, return `AAA=`
(null), and have no execution errors. One idle leader and one idle validator
were cancelled after quorum; these are not constructor failures. The deployed
code, submitted source, and local `contracts/DeadlineCheck.py` are each
**22,199 bytes / SHA-256
`45153fa51cd744458fa62367102f9ebd164d88820939745c2e2cd54ebcce8dbb`**.

The live schema matches the documented ABI: a no-argument constructor, write
`evaluate_delay(case_id, milestone_url, evidence_url_1, evidence_url_2,
requested_days)`, and read-only `get_case(case_id) -> string`. A read-only
`get_case("verify-missing-1790595218854")` returned the empty string for a
fresh unused ID, as documented.

The separate [public deployment record](../deployments/studio-dev-2026-09-28-6441f299.json)
links to its [read-only evidence](../deployments/evidence/deployment-6441f299-1790595219571.json).
The prior verifier was reused with idle leader receipts excluded from the
executing receipt count. No wallet access, transaction submission,
`evaluate_delay`, redeployment, contract change, or test rerun occurred.

## Bounded Discourse JSON preprocessing implemented locally — 2026-09-28

The local contract now recognizes only the official Discourse topic
`/t/<id>.json` `post_stream.posts` and individual `/posts/<id>.json` shapes on
the existing `discuss.python.org` allowlisted host. It checks IDs, author,
UTC `created_at`, and complete selected post text. Topic responses supply every
post's `cooked` text; individual responses supply their authored `raw` text.
Malformed JSON/shape, missing fields, more than 16 posts, post text above 8192
UTF-8 bytes, or a normalized source above 20000 bytes is unavailable evidence.
No post text is silently truncated. Other existing allowed source handling is
unchanged.

The model receives source index, URL, author, timestamp, post text, and
non-exhaustive short quote candidates verified to be literal substrings of the
original fetched body. The original body remains the authority for every
model-supplied quote in `_fact`; wrong-source, rendered, normalized, or invented
quotes still fail strict validation. Timestamps provide publication context,
not delivery dates. Each leader/validator independently fetches and evaluates;
the canonical tuple, ABI, storage schema, and `EXTRACTION_FAILED` behavior are
unchanged. There is one model call per assessment and no new host.

Focused checks: `tests/test_phase1c.py` **70 passed**; semantic/schema check
passed; source-packaging test and source-packaging check passed. The three
current official JSON responses were also checked against the local selector:
22,688/18,582/18,604 fetched bytes became 4,115/6,779/6,486 normalized
bytes, respectively, with the commitment, regression, and completion phrases
present as literal quote candidates. These current bodies are not a record of
the historical GenVM fetch or model response. Host mocked tests do not prove
live model compliance, validator consensus, or a substantive on-chain result.

New local source: **22,199 bytes / SHA-256
`45153fa51cd744458fa62367102f9ebd164d88820939745c2e2cd54ebcce8dbb`**.
The prior deployed source and finalized `EXTRACTION_FAILED` case remain as
recorded below. No wallet access, transaction, redeployment, dependency
change, frontend build, or unrelated suite run occurred.

## New DeadlineCheck evaluation verified read-only — 2026-09-28

Transaction `0x606648df853503e689b426ea126d61d494a8a2fb4b890d3d4deb0e78f93badee`
on Studio-dev (`https://studio-dev.genlayer.com/api`, chain ID **61997**)
targets contract `0x205489BCFb115DE0956974d96e30c6C79CA9361d`.
The SDK transaction is **FINALIZED / code 7**; protocol lifecycle stored and
projected status are both Finalized / code 7. Its execution result is
**FINISHED_WITH_RETURN / code 1**. The envelope receipt status is `0x1`.

The executing leader receipt reports **SUCCESS**, return `AAA=` (null), empty
stdout/stderr, and null raw error, error code, and error description. Three
validators voted **agree** and one voted **disagree**; all four executing
validator receipts report SUCCESS, the same null return, and no execution
errors. One idle validator and one idle leader receipt show
`CONSENSUS_VALIDATOR_QUORUM_REACHED` cancellation after quorum. These idle
cancellations are distinct from execution failures. The disagreement does not
change the observed finalized, successful transaction result.

Only after confirming finalization, a read-only `get_case` call for the exact ID
`python-3130-final-1790441362822` returned a stored JSON string with:

| Field | Exact returned value |
| --- | --- |
| `verdict` | `INSUFFICIENT_EVIDENCE` |
| `responsible_party` | `UNKNOWN` |
| `reason_code` | `EXTRACTION_FAILED` |
| `approved_days` | `0` |
| `explanation` | `The model assessment could not be parsed or its extracted facts failed strict validation.` |

This is an **EXTRACTION_FAILED** outcome recorded by the new contract, not a
substantive decision about responsibility or extension days and not
`SOURCE_UNAVAILABLE`. The new contract's stored record is separate from the
earlier finalized attempt against the old contract, which stored no case.
The [public read-only evidence](../deployments/evidence/evaluation-606648df-1790592208833.json)
contains the raw `get_case` string, parsed fields, lifecycle, receipt, votes,
and execution summaries; the [verification script](../deployments/evidence/verify-evaluation-606648df.mjs)
uses no account or write method. No wallet access, transaction submission,
contract change, or test rerun occurred.

## New DeadlineCheck deployment verified read-only — 2026-09-28

Transaction `0xe8b418de1d8d13793b5c5d524878148d37729a34bce460e14f5f14f36dc1da1f`
on Studio-dev (`https://studio-dev.genlayer.com/api`, chain ID **61997**)
is **FINALIZED / code 7**. The SDK transaction identifies contract
`0x205489BCFb115DE0956974d96e30c6C79CA9361d` and sender
`0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`, the documented authorized
account. The transaction lifecycle is stored and projected Finalized. The
envelope receipt has status `0x1` and the same sender and transaction hash;
as in the prior deployment, its `contractAddress` field is null, so the SDK
transaction supplies the deployed address.

Constructor execution is `FINISHED_WITH_RETURN / code 1`. All four executing
leader/validator receipts report `SUCCESS`, return `AAA=` (null), and have no
execution errors; two idle validator receipts were cancelled after quorum.
The deployed code, submitted base64-decoded source, and local
`contracts/DeadlineCheck.py` are each **18,592 bytes / SHA-256
`c6c53b3897a5458fc65f5924c2bcad312c509246f1e80b76749eb15a94ee740c`**.
The live constructor has no parameters. The live schema matches the prior
documented ABI: write `evaluate_delay(case_id, milestone_url, evidence_url_1,
evidence_url_2, requested_days)` and read-only `get_case(case_id) -> string`.
A read-only call to `get_case("verify-missing-1790587473191")` returned the
empty string as specified for a valid unused ID.

New record: [studio-dev-2026-09-28-e8b418de.json](../deployments/studio-dev-2026-09-28-e8b418de.json).
The [read-only evidence](../deployments/evidence/deployment-e8b418de-1790587473984.json)
and [verification script](../deployments/evidence/verify-deployment-e8b418de.mjs)
are separate from prior deployment evidence. No wallet access, transaction,
`evaluate_delay`, redeployment, dependency change, or test suite run occurred.

## Latest deployment transport failure diagnosed read-only — 2026-09-26

Checks at approximately **18:57–19:00 UTC** against
`https://studio-dev.genlayer.com/api`: the reported `sim_getFeeConfig` failure
occurred before signing/submission in the pinned deployment flow. **Submission
by that failed invocation is ruled out by the flow; live sender history shows no
newer deployment. Connectivity is intermittently available, not reliably restored.**
No deployment retry is warranted by this diagnosis alone.

Connectivity observations (bounded calls, no transport retries configured):

- Restricted sandbox: curl could not resolve the host; Node DNS and all SDK reads
  returned EAI_AGAIN. These sandbox failures do not establish endpoint downtime.
- Outside the sandbox, Node 24.20.0 resolved IPv4 `104.21.53.84` /
  `172.67.210.182` and IPv6 `2606:4700:3033::6815:3554` /
  `2606:4700:3037::ac43:d2b6`.
- Installed pinned `genlayer-js@2.0.0-rc.1` succeeded at `eth_chainId`,
  `sim_getFeeConfig` and `eth_getTransactionCount`. Chain returned **0xf22d /
  61997**; nonce returned **0xa / 10**. No account/provider was supplied.
- Independent curl 8.18.0 with IPv4 returned HTTP 200 for chain ID and fee
  policy via `104.21.53.84`, and sender history via `172.67.210.182`.
  Both SDK and curl confirmed enabled=true, genPerTimeUnit=1,
  storageUnitPrice=250000000, receiptGasPrice=250000000,
  messageFeeParamsBudgetFloor=76548000000000 and
  genvmStartBudgetFloor=78852000000000. Fee policy is available when reachable;
  the original error was transport failure, not a policy rejection.
- A later SDK history call reproduced **ETIMEDOUT on both IPv4 addresses** and
  **ENETUNREACH on both IPv6 addresses**. Independent curl IPv6 also failed to
  connect. IPv6 routing failure alone does not explain the original failure:
  IPv4 connectivity also failed. Successful SDK reads rule out a persistent
  Node-only inability to reach this endpoint, but do not prove stable networking.
- Independent IPv4 HTTPS control `https://example.com` returned HTTP 200.
  General VM IPv4 HTTPS works; Studio RPC also served successful responses.
  Evidence supports intermittent VM-to-endpoint transport failure, without
  locating it to VM egress, an intermediate path or the endpoint edge. There is
  no demonstrated sustained endpoint outage or proven Node-specific root cause.

Pinned flow inspection: installed CLI `genlayer@0.40.0-rc.3`
(`node_modules/genlayer/dist/index.js:60613`) resolves fees before calling
deployContract; it prints the deployment hash only after deployContract returns.
The SDK (`node_modules/genlayer-js/dist/index.js:1459`) awaits
_resolveTransactionFees before encoding/sending. Studio fee resolution
(`:2735`, `:2401`) awaits sim_getFeeConfig. Only afterward does _sendTransaction
(`:3195`) obtain the nonce, estimate gas, read gas price, sign (`:3277`) and
submit eth_sendRawTransaction (`:3278`). A thrown fee-config fetch error exits
before these steps; absence of a printed hash alone would not prove this.
This does not assert that the original CLI had never unlocked its account.

Sender reconciliation for `0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`:
the SDK-declared optional `from` filter was rejected with -32602 / “Too many
parameters provided.” One corrected SDK address-only read timed out as above;
one independent curl address-only read succeeded. The returned list contains
10 records: nine outgoing transactions and one incoming faucet credit. All are
FINALIZED; outgoing nonces are 0,1,2,3,4,6,7,8,9. Nonce 5 is absent from this
Studio list, so it is not claimed to be a complete envelope archive.

- Latest outgoing record: nonce 9, existing evaluation
  `0x7e49a6705c10e6e1dbb0a622b1ea1985722b29fc7e56ff06fd75154a5e6c374d`,
  created 2026-09-26T17:22:14.496038Z, matching saved evaluation evidence.
- Latest deployment: nonce 8,
  `0xd0e53afb5dadfcb9d0f478aefc0990b3e9c617abe7e6bad3f8793f3a530ae739`,
  created 2026-09-26T16:13:22.072034Z, matching the verified contract
  `0xe6f388C923b148C02Bf156357AaE19eBd7A350bb`. Base64-decoded source is
  18050 bytes, SHA-256
  `0a3127c911c1b812e3d8880906c38253ec4e24adc5c9b125e9652cbcba9547e3`.
- Older deployments are nonces 7/6 (the documented failed source without the
  runner header) and nonce 0 (older contract). No deployment contains the
  current extraction-failure patch (SHA-256 c6c53b3897a5458fc65f5924c2bcad312c509246f1e80b76749eb15a94ee740c).

The live history and next nonce corroborate the pre-submission failure; no
unnoticed deployment was found. This conclusion is scoped to the reported
invocation and the observed RPC snapshot, not a global guarantee about other
clients or unindexed envelopes. Successful reads mean submission status need
not remain unconfirmed solely because of endpoint inaccessibility.
Raw public read responses and the diagnostic script were retained under `/tmp`
(`deadline-transport-results.json`, `deadline-sender-history-http.json`,
`deadline-transport-check.mjs`); this status entry is the durable record.
Only docs/STATUS.md changed in the project. No transactions, signing, wallet
access/decryption, network/system changes, installation, simulation or tests
were performed. HTTP calls used 8-second connect and 12–15-second total limits;
SDK processes used a 25-second deadline and the pinned transport's retryCount=0.

## Extraction-failure robustness implemented locally — 2026-09-26

Local `contracts/DeadlineCheck.py` now converts strict extraction JSON parse
failures (ValueError/RecursionError, including duplicate keys and nonfinite
constants) and only `INVALID_FACT` from decision derivation into
**INSUFFICIENT_EVIDENCE / UNKNOWN / EXTRACTION_FAILED / 0**. Fixed explanation:
“The model assessment could not be parsed or its extracted facts failed strict
validation.” The new reason distinguishes extraction failure from substantive
insufficient evidence and source retrieval failure.

These are returned outcomes within nondet. Every validator still retrieves the
allowed URLs and runs its own evaluation before exact canonical comparison.
Different handled extraction failures may agree on this category; a valid outcome
with another reason disagrees, even if it also approves zero days. Non-Return
leader errors are still rejected. Other assessment/date/blocker/explanation
errors, oversized/non-string output, and unrelated execution errors still abort.
Strict fact/quote/date checks, public ABI, storage fields/schema version and
commit-after-consensus validation are preserved. No prompt change, JSON repair,
fragment acceptance, retry or extra model call was introduced.

Focused verification:

- `.venv/bin/python -m pytest tests/test_phase1c.py -q`: **60 passed**.
  Includes malformed/fenced/trailing/duplicate/nonfinite JSON, parser recursion,
  invalid facts, independent retrieval and agreement/disagreement, unchanged
  date/schema rejection, unexpected runtime/user/model errors, non-Return
  rejection, zero-day enforcement and preservation of previously stored cases.
  Initial run: 57 passed, one depth-fixture failure; the host accepted that depth.
  Replaced the host-dependent fixture with explicit parser RecursionError injection.
- `.venv/bin/python scripts/check-contract.py`: compilation/whitespace and pinned
  SDK ABI/storage/closure semantic checks passed; generated schema unchanged.
- `node --test tests/test_source_packaging.mjs`: passed (runner reports one file
  containing three checks). The packaging test now checks current source/header
  and serialization rather than requiring logic to match an old failed deployment.
- `node scripts/check-source-packaging.mjs`: pinned header and exact serialized
  source bytes preserved; **18592 bytes**, SHA-256
  `c6c53b3897a5458fc65f5924c2bcad312c509246f1e80b76749eb15a94ee740c`.
- Changed-file whitespace checks passed. `git diff --check` was unavailable
  because the exposed workspace is not a Git repository.

The affected tests use mocked retrieval/model responses and consensus; they do
not establish hosted VM execution or live consensus success. The semantic gate
checks closure captures/schema but does not execute real GenVM serialization.
Raw responses/offending facts from the finalized evaluation remain unavailable;
no proven prompt/parser root cause is claimed. The correction makes an identified
failure category reviewable and independently verifiable, not a successful
substantive assessment. Additional extraction-validation error categories remain
unhandled by design. Consumers of stored reasons must recognize EXTRACTION_FAILED.

Stopped before deployment. Existing on-chain contract and finalized transaction
are unchanged; deployed source retains SHA-256
`0a3127c911c1b812e3d8880906c38253ec4e24adc5c9b125e9652cbcba9547e3`.
No wallet decryption, RPC submission, retry, redeployment, dependency upgrade,
frontend build or entire-suite run occurred. Decision behavior is documented in
[DECISION_RULES.md](DECISION_RULES.md). Next step is review of the local patch;
deployment requires separate authorization.

## Existing live evaluation diagnosed read-only — 2026-09-26

Transaction `0x7e49a6705c10e6e1dbb0a622b1ea1985722b29fc7e56ff06fd75154a5e6c374d`,
contract `0xe6f388C923b148C02Bf156357AaE19eBd7A350bb`, case
`python-3130-final-1790441362822`: **FINALIZED / code 7**, stored/projected
Finalized, action NoOp; consensus decision remains **UNDETERMINED**.
Live RPC chain `0xf22d` (61997) verified. First poll was terminal; no further
polling needed. Envelope receipt status `0x1` does not establish evaluation success.

The existing transaction's round 0 used its initial leader plus three automatic
leader rotations. This diagnosis submitted nothing. History: PENDING → PROPOSING
→ COMMITTING → REVEALING, repeated with rotations, then UNDETERMINED and FINALIZED.
Decision materialized at 1790443382, appeal deadline 1790443412, finalized at
1790443412.744853. No appeal occurred.

| Existing attempt | Exact leader and executing validator payload | Outcome |
| --- | --- | --- |
| 0 | `MALFORMED_ASSESSMENT` | Leader Rotation |
| 1 | `INVALID_FACT` | Leader Rotation |
| 2 | `INVALID_FACT` | Leader Rotation |
| 3 | `MALFORMED_ASSESSMENT` | Undetermined |

All leaders report ERROR; top-level FINISHED_WITH_ERROR / code 2. Exact encoded
payloads are `AU1BTEZPUk1FRF9BU1NFU1NNRU5U` (hex
`014d414c464f524d45445f4153534553534d454e54`) and
`AUlOVkFMSURfRkFDVA==` (hex `01494e56414c49445f46414354`). The leading
`01` is a user-error tag. Each attempt has three disagree votes with the same
error as its leader and two idle cancellations. Cancellations: `AmlkbGU=` / hex
`0269646c65`, stderr `Validator execution cancelled after quorum`, raw_error
`{"fatal":false,"causes":["VALIDATOR_QUORUM_REACHED"]}`, code
`CONSENSUS_VALIDATOR_QUORUM_REACHED`. These are consensus cancellations.
Executing leader/validator stdout/stderr are empty; raw_error, error_code and
error_description are null. No raw model response or Python traceback is exposed.

Earliest evidenced failure: attempt 0's leader raises MALFORMED_ASSESSMENT in the
strict JSON parse guard (ValueError or RecursionError, including duplicate keys
and nonfinite constants), before fact derivation or canonical comparison.
Attempts 1/2 reach `_fact` and fail shape/type/index/quote/value validation;
which fact/check failed is unavailable. Markdown fences, escaped-quote mismatch,
truncation and malformed model JSON are possible, not established causes.

Consensus cause is explicit error rejection: pinned SDK decodes the leader's
UserError and passes it to the custom validator; `if not isinstance(proposed,
gl.vm.Return): return False` exits before independent evaluation. Validators
report NOTIFY_NONDET_DISAGREEMENT at index 0 with no LLM token statistics.
Thus identical execution-error payloads can accompany disagree votes. There is
no evidence of competing canonical verdict/day/party/reason tuples. The leader
LLM token counts (input/output) are 24456/711, 21352/1491, 21291/411, 26110/450;
all leaders reached LLM execution. Host call counts omit nested web/LLM activity,
so their absence alone cannot establish no retrieval. Final leader processing
5362 ms; validators 790/907/1496 ms. Full per-attempt statistics/logs are saved.

No demonstrated exhaustion: final GenVM execution consumed 78964000000000,
remaining 24921036000000000 of 25000000000000000; nondet output consumed 92 bytes.
Report executionBudgetExceeded=false, overrun=0. Charged historical execution
314824000000000 across four attempts; storage/message charges zero. Aggregate
leader/validator timeunits 41/16, max validator 2, allocations 100/200.
Deposit 100000000000010352; refunded 99685176000007705; primary spent
314824000002647. No leader timeouts or deterministic violations recorded.
No higher fee recommendation is supported.

Fresh read-only `get_case` returns **`""`**: no result stored for this case.
Current source hash matches verified deployment metadata:
`0a3127c911c1b812e3d8880906c38253ec4e24adc5c9b125e9652cbcba9547e3`.
Actual calldata uses the three Discourse JSON URLs in the revised preview,
not the superseded oversized HTML candidate. Prior prepared/not-submitted
status below is historical and superseded by this diagnosis.

Next proposed action: obtain the existing raw leader responses and underlying
parse exceptions/offsets (attempts 0/3), plus offending facts and actual fetched
page bytes (attempts 1/2), from existing execution traces. These are missing from
public RPC logs; the smallest exact parser/prompt correction is not established.
A separate small robustness correction could represent bounded extraction failures
explicitly within nondet and have validators independently verify that failure,
preventing automatic rejection solely because a leader returns UserError. It
must preserve strict evidence checks; accepting every leader error or treating
malformed output as SOURCE_UNAVAILABLE is not justified. No patch applied.

Public evidence saved separately: [RPC responses](../deployments/evidence/evaluation-readonly-1790443612132.json),
[decoded history, source/SDK excerpts and diagnosis](../deployments/evidence/evaluation-diagnosis-1790443612132.json),
[read-only collection script](../deployments/evidence/diagnose-evaluation.mjs).
SDK JSON parsing may round very large numeric fields in historical responses;
exact current fee strings and encoded error payloads are preserved.
No transaction, retry, wallet access/decryption, contract change, dependency
upgrade, simulation or passing-suite rerun occurred. Initial sandbox RPC transport
failed; authorized read-only network access succeeded.


## First live evaluation prepared — not submitted (2026-09-26)

Saved [exact arguments, unused-ID read, source sizes and live fee/balance quote](../deployments/first-evaluation-preview.json)
and [reviewable manual command and limitations](FIRST_LIVE_EVALUATION.md).
Reused verified deployment and completed checks. No recorded beta case with an
incomplete blocker interval was found; the candidate uses the real Python 3.13.0
final-release URLs already in PLAN.md, explicitly subject to case approval.

Fresh case `python-3130-final-1790441362822` returned `""` through read-only
get_case on chain 61997. All three hosts are allowed, but current direct raw HTML
sizes are 116917 / 39851 / 49464 bytes: every source exceeds 32768 bytes.
Substantive source evaluation is therefore not retrieval-ready. If GenVM receives
the same bodies, expected result is INSUFFICIENT_EVIDENCE / UNKNOWN /
SOURCE_UNAVAILABLE / 0. No incomplete interval establishes positive approved days.
GenVM may receive different bodies; live retrieval behavior remains unverified.

Pinned SDK generic write fallback: leader/validator 100/200, rotations [3],
appeals 0, execution budget per round 25000000000000000, message fees 0,
caps 2/300000000/300000000. SDK-calculated deposit 100000000000010352 wei;
current signer balance 9999289511249991534 wei. This covers funding but is not a
measured web/LLM evaluation budget. Constructor funding is not evidence of write
sufficiency. No targeted simulation or evaluate_delay occurred.

Next step: approve or revise the candidate case and scope. Current exact sources
can support a source-unavailable smoke test, not a substantive evidence demo.
The manual command requests a masked password for the locked keystore, sends once
and logs the public transaction hash; it was not run. No wallet decryption,
transactions, contract/dependency changes or repeated passing suites occurred.

## Corrected deployment verified read-only — 2026-09-26

Contract `0xe6f388C923b148C02Bf156357AaE19eBd7A350bb`, transaction
`0xd0e53afb5dadfcb9d0f478aefc0990b3e9c617abe7e6bad3f8793f3a530ae739`,
is **FINALIZED / code 7**, accepted. Pinned `genlayer-js@2.0.0-rc.1`
verified live Studio-dev RPC chain `0xf22d` (61997) and transaction/receipt
sender `0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`, matching the authorized
default. Finalized on the first poll; bounded policy allowed at most seven
checks at ten-second intervals. Stored and projected lifecycle are Finalized,
resolution action NoOp.

Constructor **FINISHED_WITH_RETURN / code 1**, return `null` (receipt
`AAA=`, hex `0000`). Leader and agreeing validators report SUCCESS, empty
stderr and null raw_error/error_code/error_description. Idle validators cancelled
after quorum are consensus cancellations, not constructor failures. Envelope
receipt status is `0x1`; its null contractAddress is not relied upon: transaction
recipient matches the reported address and deployed code/schema/read are available.

Deployed source, submitted source and current local source match exactly:
18050 bytes, SHA-256
`0a3127c911c1b812e3d8880906c38253ec4e24adc5c9b125e9652cbcba9547e3`.
Deployed schema matches ABI_SPEC.md: no constructor arguments; evaluate_delay
has four string parameters and one int, readonly false, return null; get_case
has one string parameter, readonly true, return string; no extra public methods.
This demonstrates hosted runner loading and successful construction for this
source; exact hosted build and full runner inventory remain unknown.

Fresh missing-ID get_case returned **`""`**, without an error. This matches the
corrected source and documented ABI; the requested missing-case error does not
exist for valid unknown IDs. Public metadata is saved in
[studio-dev.json](../deployments/studio-dev.json), with full read-only evidence in
[verification evidence](../deployments/evidence/new-deployment-verification-1790439620503.json).
Previous deployment evidence and status history are preserved.

Next step: review a separately authorized evaluate_delay smoke test and fee
budget. Write-path evaluation and external web/LLM behavior remain unverified.
No wallet decryption, transaction submission, deployment, evaluate_delay,
contract/dependency changes, simulation or rerun of passing tests occurred.
Offline assertions checked the saved public responses before writing metadata.

## Bounded hosted runner-support check — 2026-09-26

Outcome **2: release compatibility established; actual hosted support remains
unverified and will be checked through a separately authorized deployment**.
Reused the completed provenance and focused checks below; did not repeat them.
Runner under consideration remains
`py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng`.

One bounded read-only review examined the public upstream
[Studio RPC registration](https://github.com/genlayerlabs/genlayer-studio/blob/main/backend/protocol_rpc/rpc_methods.py)
and [deployment configuration](https://github.com/genlayerlabs/genlayer-studio/blob/main/docker-compose.yml),
alongside the already inspected registration and pinned SDK surfaces. No supported
runtime-metadata method exposing an installed-runner inventory or this hash's
availability was identified. Fee policy and consensus metadata do not supply
runner availability. gen_getContractSchemaForCode performs source execution for
schema extraction; it is not a runtime-metadata inventory and was not invoked.

The public compose configuration accepts GENVM_TAG, GENVM_REF,
GENVM_SOURCE_MODE and GENVM_EXECUTOR_VERSION_NAME as deployment overrides and
mounts a GenVM cache. It does not disclose the actual Studio-dev override values,
running build or installed runner inventory. Upstream main is not a verified
manifest of the hosted instance; web retrieval also has cached crawl dates, so it
cannot establish live configuration. No authoritative hosted configuration tying
this runner hash to the running service was exposed by these sources.

No supported read-only metadata route found in this check can confirm hosted
availability. Stopped here without speculative RPC names, further searches or
execution probes. Missing metadata is **not evidence of incompatibility** and is
not an additional prerequisite for considering a separately authorized deployment.
That deployment must inspect constructor success and lifecycle before claiming
usable hosted support. Only STATUS.md changed; no tests, installation, wallet
access, simulation, deployment, transaction or evaluate_delay occurred.

## Runner-header correction implemented — 2026-09-26

Prepended exactly one line to contracts/DeadlineCheck.py:

```python
# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }
```

The remaining source bytes match the latest failed deployment's submitted code
exactly. Contract logic and all dependency pins are preserved. New source is
18050 bytes; SHA-256
`0a3127c911c1b812e3d8880906c38253ec4e24adc5c9b125e9652cbcba9547e3`.
This supersedes the proposed-only header correction below; historical deployment
evidence continues to describe the old 17966-byte source.

Runner selection is established for the cached pinned GenVM SDK v0.6.0-rc3:
the authoritative [GenVM manager release](https://github.com/genlayerlabs/genvm-manager/releases/tag/v0.6.0-rc3)
publishes genvm-universal.tar.xz with SHA-256
`bd30580f911338d5533460eca8ed714dec371de5803c04e41dbb96430aea7b6e`,
matching the cached bundle. The runner archive in that verified bundle is
`runners/py-genlayer/5j/ycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng.zip`;
its extracted bytes match the cache, SHA-256
`2cbcc8389744c4321852d2c0b4bfcef0729bfd22467e2aaf0d4d204cf6f015eb`.
The runner manifest selects py-lib-genlayer-std
`kzr02ndm9et4qkmbqpq5djjt5sme2yt76n7sz1qbzax0knt6mam0`, the cached SDK
used by the semantic gate, alongside immutable cloudpickle and cpython runners.
Public metadata, digests and manifest are saved in
[runner provenance](../deployments/evidence/runner-header-provenance-v0.6.0-rc3.json).

The [official migration guide](https://docs.genlayer.com/developers/consensus-v06-migration)
places pinned JS 2.0 RC / Python 0.19 RC / CLI 0.40 RC in the Studio v0.123 RC
family and identifies Studio-dev chain 61997. This establishes intended release
compatibility, not proof that the hosted service has this runner installed.
Exact hosted runtime build, runner availability and successful GenVM construction
remain unverified. The old documentation example hash and latest/test aliases
were not substituted.

Added offline scripts/check-source-packaging.mjs and focused
tests/test_source_packaging.mjs. The parser check follows the inspected executor
text rules: byte-zero comment prefix (#, // or --), contiguous comment block,
optional first version line, concatenated JSON contents. GenVM permits version
comments and multiline initialization JSON; the narrower first-line Depends
requirement is this project's explicit packaging policy, not an invented GenVM
restriction. Blank/BOM prefixes fail the actual byte-zero rule. Whitespace inside
the header, CRLF and no final newline are accepted. Exact pinned runner is checked.
The byte check uses pinned SDK abi.transactions.serialize, matching deployContract's
code/calldata/leaderOnly serialization, and verifies the decoded code equals the
raw file. It constructs no client/account and sends nothing.

Checks run only for this edit:

- `node tests/test_source_packaging.mjs`: 3 focused tests passed, including
  missing/misplaced/malformed/wrong/aliased headers, supported parser forms,
  unchanged source body and deployment serialization byte preservation.
- `node --test tests/test_source_packaging.mjs`: file check passed (runner reports
  one file); direct invocation above explicitly reports all three tests.
- `node scripts/check-source-packaging.mjs`: pinned header and all 18050 submitted
  bytes preserved; hash as above.
- `.venv/bin/python scripts/check-contract.py`: compilation/whitespace,
  pinned SDK ABI/storage/closure semantics and generated schema passed.

No full 91-test suite, simulation stack, dependency change, wallet decryption,
deployment, transaction or evaluate_delay occurred. Next step: establish hosted
runner availability/runtime identity, then verify actual construction through a
separately authorized compatible runtime check. This fix is not evidence of a
successful deployment and does not justify another budget increase.

## Latest deployment — finalized runner-header failure (2026-09-26T14:58:24Z)

Transaction `0xeab2054ab177ebf75e211d4b51e28170e79078f69d10c40ad009aa910ef3bc0b`
is **FINALIZED / code 7**, constructor **FINISHED_WITH_ERROR / code 2**.
Pinned `genlayer-js@2.0.0-rc.1`, Studio-dev endpoint and live chain ID
`0xf22d` (61997) verified. Lifecycle stored/projected Finalized, action NoOp.
No polling required. Envelope receipt status `0x1` and consensus Accepted mean
acceptance/agreement on the error, not successful construction.

Exact constructor result: **`invalid_contract runner absent`**. Leader result
`AmludmFsaWRfY29udHJhY3QgcnVubmVyIGFic2VudA==` decodes to tag `0x02`
plus that UTF-8 payload (hex
`02696e76616c69645f636f6e74726163742072756e6e657220616273656e74`).
Agreeing validators return the same error. Leader stdout/stderr empty;
raw_error/error_code/error_description null. No stack trace is exposed.
Idle validator quorum cancellations are separate. The envelope has one public
acceptance event; full consensus history and execution statistics are saved.
Leader reports seven STORAGE_READ calls, host handling 2 ms, manager attempt
1 ms. No web/LLM/message calls appear in the reported call counts.

No usable contract exists at intended recipient
`0x5dB0223F9eeC2fB0AFE5e95851C6904d2Fa8e630`:
supported SDK getContractCode returns -32001, exact message
`Contract 0x5dB0223F9eeC2fB0AFE5e95851C6904d2Fa8e630 not found`.
Leader state is empty, state hash null; envelope contractAddress null.
Schema/missing-case read therefore not attempted.

| Resource | Verified amount |
| --- | ---: |
| Submitted executionBudgetPerRound | 25000000000000000 |
| GenVM execution_data_gas consumed | 78992750000000 |
| GenVM execution_data_gas remaining | 24921007250000000 |
| nondet_outputs bytes consumed | 64 |
| Chargeable receipt executionConsumed | 78628000000000 |
| Storage/message fees, submitted message bytes/count | 0 |
| Leader/validator timeunits used | 1 / 3 (allocations 100 / 200) |
| Deposit | 25000000000002588 |
| Settled primary_fee_spent (including time/overlay) | 78628000000823 |
| Total refund | 24921372000001765 |

Execution fee report explicitly says executionBudgetExceeded=false, overrun=0.
The previous `out_of receipt nondet_output` attempt failed startup reservation
with only 2048000000000 left against 4352000000000 required. This attempt
passes that boundary and reaches source runner parsing; it is a different cause.
No budget increase is supported. Fee report's recommended_fee_preset is based
on this failed execution and does not establish successful-constructor cost.

Submitted source remains 17966 bytes, SHA-256
`4f87bcd143e079dc1c4e3f87dd5e3561de879417a3a98fda492a1b99d16ff636`,
matching local bytes; constructor calldata decodes to `0x06`.
Only the relevant source header and offline loader/check were inspected:
DeadlineCheck.py begins with a docstring and has no runner magic comment.
Executor source at commit `c698f5551d52852b32b4975f437322f171ce4efe`,
[parse.rs](https://github.com/genlayerlabs/genvm-executor/blob/c698f5551d52852b32b4975f437322f171ce4efe/executor/src/runners/parse.rs),
rejects text not beginning with a supported comment prefix; the corresponding
ABI defines exactly `invalid_contract runner absent`. This mechanism matches
submitted bytes/error, identifying a missing source runner header before Python
module/constructor execution. Exact hosted build is still unknown.
[Official contract guide](https://docs.genlayer.com/developers/intelligent-contracts/first-contract)
requires a first-line Depends magic comment with an immutable runner hash.
Offline gates loaded the cached SDK via GENVM_VERSION and host Python; they did
not verify GenVM source runner parsing and therefore missed this defect.

Smallest correction, proposed ONLY: prepend
`# { "Depends": "py-genlayer:<verified immutable runner hash>" }` before the
docstring. Preserve all contract logic and dependencies. Local v0.6.0-rc3 bundle
contains candidate `py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng`;
hosted availability/compatibility is unverified, so do not claim it is deployable
or copy an unrelated documentation hash. Next action: verify the matching
Studio-dev runner identifier, then review the one-line patch and focused tests.
Proposed tests: detect the current missing header, validate first-line JSON and
exact pinned Depends ID, reject leading blank/BOM/malformed or misplaced header,
and check submitted-byte preservation. A matching transaction-free GenVM
constructor simulation should then verify runner loading/construction and no
external calls; host tests alone are insufficient. No tests were run or added.

Separate evidence, created exclusively without overwriting previous attempts:

- [Full live RPC/lifecycle/constructor/log/resource/contract-absence evidence](../deployments/evidence/latest-deployment-1790434704236.json).
- [Diagnosis, submitted-byte comparison, exact authoritative parser/ABI source and proposed checks](../deployments/evidence/latest-deployment-diagnosis-1790434704236.json).
- [Initial sandbox transport failures](../deployments/evidence/latest-deployment-1790434678885.json); these are transport failures, not transaction results.

No retry, transaction, wallet decryption, dependency change, contract correction,
simulation execution or repeated passing test suite occurred.


## Constructor budget quote — 2026-09-26T14:33:13Z

No matching transaction-free constructor simulation environment is available.
Read-only Docker inventory still contains/runs Studio v0.65.0, with no v0.123 RC
stack cached. No GenVM executable is on PATH. Hosted exact runtime identity is
still unestablished; source support for sim_call deploy does not establish a
matching available simulation. No simulation, provisioning, or installation ran.

Reused the finalized failure diagnosis and passing gates. Current source matches
saved submitted bytes exactly: 17966 bytes, SHA-256
4f87bcd143e079dc1c4e3f87dd5e3561de879417a3a98fda492a1b99d16ff636,
constructor calldata 0x06. The smallest sufficient constructor budget remains
unknown: 78852000000000 is startup only, leaving no construction headroom.

Fresh read-only pinned SDK quote and live fee policy/balance are saved in
[constructor budget evidence](../deployments/evidence/constructor-budget-quote-1790433193182.json).
The [reproducible quote script](../deployments/evidence/quote-constructor-budget.mjs)
uses no account/signing/submission API. Chain ID is 61997; policy and existing
price caps/time allocations/rotations remain unchanged and compatible.
Public sender balance is 9999446909999993180 wei (9.999446909999993180 GEN).

Pinned genlayer-js generic fallback (dist/index.js lines 2293–2296, 2440–2447):
max(500000, admission floor, receiptGasPrice * 100000000) = 25000000000000000.
With all other submitted fields preserved, SDK deposit = 25000000000002588 wei
(0.025000000000002588 GEN). Headroom above startup is 24921148000000000.
This is an implementation-documented generic fallback, NOT a measured constructor
minimum or verified sufficient budget. The startup-only SDK deposit is
78852000002588 wei; that quote does not establish deployment readiness.

Official fee-profiling guidance recommends measuring construction/receipt/storage
requirements and applying headroom. Pinned simulation-derived estimator uses
execution_fee_consumed + execution_fee_report.totalEstimatedFee, with 20% default
headroom and the policy admission floor. A future matching successful simulation
must also confirm the startup floor is covered. Applying 20% to startup alone or
using this failed receipt as a complete construction profile is unjustified.

Conditional manual command for a separately approved generic-fallback attempt
(not a claim of minimum/sufficient construction funding; NOT executed):

```sh
node node_modules/genlayer/dist/index.js deploy --wallet keystore --contract contracts/DeadlineCheck.py --rpc https://studio-dev.genlayer.com/api --fees '{"distribution":{"leaderTimeunitsAllocation":"100","validatorTimeunitsAllocation":"200","appealRounds":"0","executionBudgetPerRound":"25000000000000000","executionConsumed":"0","totalMessageFees":"0","rotations":["0"],"maxPriceGenPerTimeUnit":"2","storageFeeMaxGasPrice":"300000000","receiptFeeMaxGasPrice":"300000000"}}'
```

Omit --fee-value so the pinned SDK calculates the deposit at submission. This is
only a reviewable fallback candidate; approval is required before deployment.
No wallet decryption, transaction, evaluate_delay, tests, frontend/GitHub work,
contract/dependency/ABI change or other fee-setting change occurred.

## Finalized constructor failure diagnosis — 2026-09-26T12:53Z

Transaction `0x1bb3e4088bacc109aece6110d2c5f3559f3a10b32b060ff8371104f5f2541dc5`:
**receipt startup allocation is insufficient before contract execution**. This
explains the exact `out_of receipt nondet_output` error; unsupported contract
behavior is not implicated by this failure. Successful construction and subsequent
runtime compatibility remain unverified. The recorded recipient remains unusable.

Read-only supported RPCs were refreshed through pinned `genlayer-js@2.0.0-rc.1`
at `https://studio-dev.genlayer.com/api`: `gen_getStudioTransactionByHash(hash,
true)`, `gen_getTransactionStatusDetails(hash)`, and `sim_getFeeConfig()`.
Status remains FINALIZED / code 7, constructor FINISHED_WITH_ERROR. The full
transaction API supplies constructor receipts, execution statistics, fee policy
snapshot, budget totals/remaining/consumed, and error fields. Leader stdout/stderr
are empty; raw_error, error_code and error_description are null; call_counts is
empty, host handling time is zero, and manager attempt duration is 1 ms. Agreeing
validators have the same budget/error; idle quorum cancellations are separate.
No additional constructor stack trace is exposed in these responses. Inspected
Studio RPC registration supplies no separate executor trace/log retrieval method;
operator-side logs and exact live runtime build identity remain unavailable.
Fresh responses are retained in `/tmp/deadline-diagnosis-rpc.json`; persistent
saved evidence already contains the transaction-specific figures below in
[the full transaction response](../deployments/evidence/corrected-deployment-1790426600795.json).

| Receipt allocation evidence | Amount |
| --- | ---: |
| Submitted executionBudgetPerRound / admission floor | 76548000000000 |
| Initial message-receipt reservation consumed | 74500000000000 |
| Execution-data budget remaining | 2048000000000 |
| Required nondet-output startup reservation | 4352000000000 |
| Startup total / live genvmStartBudgetFloor | 78852000000000 |
| Startup shortfall | 2304000000000 |

Receipt price is locked at 250000000; calldata costs 16 gas/byte. Snapshot
receiptWrapperBytes=1024. Exact arithmetic:
`(210000 + 21000 + 60000 + 7*1000)*250000000 = 74500000000000`;
`(1024 + 64)*16*250000000 = 4352000000000`.
The nondet-output **byte** bucket remains UINT256_MAX, consumed zero. Thus the
error identifies the receipt operation whose shared **execution_data_gas**
reservation failed, not a large LLM response or exhausted output-byte cap.
Message fee budget/consumption and storage fee consumption are zero; submitted
message count allowance is 20, consumed zero. Snapshot zero byte-limit fields
are mapped to unmetered buckets by Studio source, not zero-byte allowances.
Leader/validator time use is 1/3 against allocation 100/200; no time exhaustion is
reported. Fee accounting executionConsumed=78628000000000 is distinct from the
GenVM bucket consumption and is not a successful-construction budget estimate.

Authoritative source inspected (downloaded for reading only into /tmp):

- Studio v0.123.0-rc.7, commit `a0300c398528f743465c4e060c80877ced3873c5`:
  [fees.py](https://github.com/genlayerlabs/genlayer-studio/blob/a0300c398528f743465c4e060c80877ced3873c5/backend/protocol_rpc/fees.py#L472)
  distinguishes minimum proposed-receipt admission from GenVM startup;
  lines 2010–2065 map shared execution budget and unmetered byte buckets.
  Live policy still advertises default execution budget equal to the lower
  admission floor, despite advertising the higher startup floor.
- That release pins GenVM manager v0.6.0-rc5, commit
  `be0bbe88be13431096e66ab018a09e68a0044283`, whose v0.3 executor is
  `c698f5551d52852b32b4975f437322f171ce4efe`.
  [Executor configuration](https://github.com/genlayerlabs/genvm-executor/blob/c698f5551d52852b32b4975f437322f171ce4efe/executor/install/config/genvm.yaml#L140)
  specifies exactly the two reservations above and shares execution_data_gas
  with nondet_outputs. [consume_initial](https://github.com/genlayerlabs/genvm-executor/blob/c698f5551d52852b32b4975f437322f171ce4efe/executor/src/rt/fees.rs#L510)
  charges these before execution and returns the failing operation's error;
  [public ABI](https://github.com/genlayerlabs/genvm-executor/blob/c698f5551d52852b32b4975f437322f171ce4efe/executor/crates/sdk-rs/src/abi/consts.rs#L335)
  defines this exact string. This authoritative mechanism matches the observed
  counters exactly; it does not establish the hosted runtime's exact version.

Submitted contract_code decodes to 17966 bytes and matches the local contract
SHA-256 `4f87bcd143e079dc1c4e3f87dd5e3561de879417a3a98fda492a1b99d16ff636`;
constructor calldata is `0x06` (empty encoded map). Constructor body is `pass`.
Module initialization imports json/re/date/urlsplit/genlayer, compiles two regexes,
builds constants, defines functions and applies contract/decorator registration.
Cached pinned SDK v0.6.0-rc3 Contract.__init_subclass__ generates storage and
registers the class; web/LLM/run_nondet closures belong to evaluate_delay and are
not called by construction. Host Python/cloudpickle is not used by the JS source
submission path. Startup failure precedes proving any of those module/runtime
operations work in hosted GenVM.

Pinned JS extractStudioFeePolicy uses messageFeeParamsBudgetFloor for its
executionBudgetFloor and does not read genvmStartBudgetFloor. Thus neither the
advertised defaults nor an admission-minimum preset establishes execution
readiness. Evidence supports a default/estimation allocation mismatch, not a
random executor crash or a demonstrated SDK/contract incompatibility.

Smallest proposed correction: change only the deployment fee distribution's
executionBudgetPerRound to a measured constructor requirement, at least the
refreshed genvmStartBudgetFloor **plus measured construction/receipt headroom**;
retain code, dependencies, time allocations and price caps. Let the SDK recompute
the corresponding deposit; increasing --fee-value alone leaves the failing
resource bucket unchanged. Merely setting 78852000000000 covers startup only
and is NOT a verified sufficient deployment budget.

Exact next step, proposed only: use a compatible isolated local Studio/GenVM
with the same policy and pinned submitted bytes to perform snapshot constructor
simulation with full receipt (`sim_call`, type `deploy`, supported in inspected
Studio endpoints.py). Compare the recorded budget against a startup-covered
budget, then measure successful constructor receipt costs and verify completion,
storage/code output and absence of external calls before choosing a final budget.
Use identical constructor calldata and source hash; do not substitute host tests
or schema generation. Obtain matching runtime/policy identity first. Simulation
support is source-verified, not yet exercised on the hosted endpoint; hosted
execution simulation and deployment retry were not performed. Successful future
finalized deployment must separately verify code/schema and missing-case read.

Only STATUS.md was changed in the project. No transaction, simulation execution,
contract/dependency change, wallet access, passing-suite repetition, implementation
or retry occurred. Temporary source downloads and read-only RPC artifacts are
outside the project. Stop here before implementation or retry.


## Corrected manual deployment — inspected 2026-09-26T12:44Z

The corrected manual submission is distinct from the earlier fee-reverted attempt.
Read-only inspection used installed `genlayer-js@2.0.0-rc.1` and
`https://studio-dev.genlayer.com/api`; live `eth_chainId` returned `0xf22d`
(61997). No transaction was submitted during inspection.

- Printed hash / envelope hash:
  `0x1bb3e4088bacc109aece6110d2c5f3559f3a10b32b060ff8371104f5f2541dc5`.
  Pinned SDK `_sendTransaction` returns the envelope hash for Studio chains.
- `eth_getTransactionReceipt`: **success**, status `0x1`; contractAddress null.
  Receipt log topic identifies the same transaction hash. This confirms envelope
  acceptance, not successful GenVM construction.
- `gen_getStudioTransactionByHash(hash, true)` retrieves the linked deployment
  (type 1); `tx_id` and `hash` equal the printed envelope hash. Studio reuses the
  hash; there is no distinct linked GenLayer hash in these responses.
- `gen_getTransactionStatus`: **FINALIZED**. Pinned
  `advanced.getTransactionLifecycle` confirms stored/projected **Finalized**,
  resolution action **NoOp**. Already terminal; no pending polling was needed.
- Constructor execution: `txExecutionResult=2`,
  `txExecutionResultName=FINISHED_WITH_ERROR`; leader execution_result **ERROR**.
  Exact decoded result: **`out_of receipt nondet_output`**. Raw leader result
  `Am91dF9vZiByZWNlaXB0IG5vbmRldF9vdXRwdXQ=` decodes to result tag byte `0x02`
  followed by that exact UTF-8 error. Leader stderr/stdout are empty and
  raw_error/error_code/error_description are null. Consensus `MAJORITY_AGREE`
  denotes agreement on this execution error, not constructor success. Idle
  validator quorum-cancellation errors are separate from the leader error.
- No contract created: recorded intended recipient
  `0xB5533eB812e9a4A84B54fe67F7Af719BfCB1DB31` is NOT a successful deployed
  address. Supported SDK `getContractCode` returns RPC -32001 with exact message
  `Contract 0xB5533eB812e9a4A84B54fe67F7Af719BfCB1DB31 not found`.
  Leader contract_state is empty and contract_state_hash null.

Public evidence was saved with exclusive creation, preserving existing files:

- [Receipt, transaction and status responses](../deployments/evidence/corrected-deployment-1790426600795.json).
- [Lifecycle and contract absence](../deployments/evidence/corrected-deployment-followup-1790426645209.json).
- [Initial sandbox transport errors](../deployments/evidence/corrected-deployment-1790426589223.json)
  are retained separately; they are not evidence of transaction failure. Network
  inspection then succeeded with sandbox escalation.

The CLI's detail-free `Error:` does not establish the outcome; the above RPC
execution record does. Root cause beyond the exact runtime error was not inferred.
Schema verification and missing-case read were conditional on successful finalized
construction and were therefore not performed. Local source `get_case` returns
an empty string for a valid missing ID, rather than a missing-case exception;
that is source behavior only, not verified deployed behavior.
No retry, wallet decryption, write/evaluate_delay call, contract change, dependency
upgrade, or test-suite repetition occurred. Historical entries below remain as
records of their respective earlier phases.

## Failed manual Studio-dev deployment — verified 2026-09-26

This supersedes the later historical statements that no deployment was submitted
and the manual handoff's fee advice. A manual deployment WAS submitted:
`0x0b47a5bcc06253c4514719707f8a95706029429a3890e40d0f224b9849c81704`.
Do not treat it as an unsubmitted deployment or retry without new approval.

Read-only requests to the configured `https://studio-dev.genlayer.com/api`:

- `eth_getTransactionReceipt`: status `0x0`, revertReason
  `FeeValueMustBeNonZero(1)`, contractAddress null, logs empty.
- `eth_getTransactionByHash`: existing envelope, authorized sender
  `0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`, nonce `0x5`, value
  `0x0`, destination `0xb7278a61aa25c888815afc32ad3cc52ff24fe575`.
  That destination is the envelope target, NOT a resulting contract address.
  RPC returns input `0x` and zero signature/gas placeholders; original signed
  calldata is not available from this response and was not decoded.
- `gen_getTransactionStatus` and `gen_getStudioTransactionByHash(hash, true)`:
  both return -32001, Transaction not found. No GenLayer transaction/contract
  was created; no constructor or GenVM execution result exists.

Exact error meaning: field index 1 is `leaderTimeunitsAllocation`, NOT the
deposit amount or validator count. Official Studio v0.123.0-rc.7 source,
commit `a0300c398528f743465c4e060c80877ced3873c5`,
[`backend/protocol_rpc/fees.py` lines 1706–1719](https://github.com/genlayerlabs/genlayer-studio/blob/a0300c398528f743465c4e060c80877ced3873c5/backend/protocol_rpc/fees.py#L1706),
explicitly maps 1=leader allocation, 2=validator allocation, 3=execution budget,
4=time-unit price cap, 5=storage price cap, 6=receipt price cap, and raises this
error for a nonpositive required field. Exact hosted release is not established;
the live error agrees with this authoritative RC mapping. The official
[error reference](https://docs.genlayer.com/developers/error-reference) identifies
the uint256 argument as a field index and selector `0x632be5a1`.

Cause: omitted fee options in the manual handoff. Pinned CLI 0.40.0-rc.3
`dist/index.js` parseTransactionFees (60329ff), resolveTransactionFees (60359ff)
and DeployAction.deploy (60599ff) pass no fees when neither --fees, --fee-profile
nor --fee-value is supplied. Both its embedded SDK and project genlayer-js
2.0.0-rc.1 have the same behavior: normalizeTransactionFees creates zero numeric
distribution fields and rotations [0]; _resolveTransactionFees returns feeValue
0 before reading Studio policy when the distribution requires no deposit
calculation; deployContract sets userValue=0; _encodeAddTransactionData sends
userValue+feeValue=0 with the modern fee-bearing tuple. Relevant project SDK
locations: dist/index.js 980–1140, 1459–1500, 2291, 2734–2811; embedded CLI
counterparts include 53157–53234. Thus the prior advice that merely omitting
--fee-value obtains live defaults was incomplete: an explicit nonzero distribution
is needed. This is CLI no-fees defaults plus SDK normalization/early-return
behavior, not evidence of an incompatible endpoint or a contract failure.
The zero leader allocation is confirmed by the live revert; all other zero
distribution fields are reconstructed from the documented command and installed
source, not recovered from original calldata. Submitted value zero is RPC verified.

Live sim_getFeeConfig: enabled=true; policy genPerTimeUnit=1,
storageUnitPrice=receiptGasPrice=250000000, timeUnitOverlayBps=1500,
messageFeeParamsBudgetFloor=76548000000000,
genvmStartBudgetFloor=78852000000000. Advertised default distribution:
leader=100, validator=200, appealRounds=0, executionBudgetPerRound=76548000000000,
executionConsumed=totalMessageFees=0, rotations=[0], maxPriceGenPerTimeUnit=2,
storageFeeMaxGasPrice=receiptFeeMaxGasPrice=300000000;
default feeValue=76548000002588 wei. These differ from the earlier generic
estimator's preset; that historical estimate was not the submitted envelope.

Smallest supported correction, proposed only: retain pinned packages, endpoint,
contract and keystore flow; add the complete live distribution with --fees,
omitting --fee-value so the SDK calculates the deposit using current policy:

```sh
--fees '{"distribution":{"leaderTimeunitsAllocation":"100","validatorTimeunitsAllocation":"200","appealRounds":"0","executionBudgetPerRound":"76548000000000","executionConsumed":"0","totalMessageFees":"0","rotations":["0"],"maxPriceGenPerTimeUnit":"2","storageFeeMaxGasPrice":"300000000","receiptFeeMaxGasPrice":"300000000"}}'
```

Installed deploy --help and source verify --fees JSON and --fee-value support.
--fee-value alone does not populate the six required distribution fields and
cannot correct this error. Refresh fee configuration before any authorized retry;
the preset/deposit is not a source simulation or a guarantee of runtime success.
No package upgrade, code/config/wallet change, secret access, submission, retry,
evaluate_delay, or passing-test repetition occurred. Only STATUS.md was updated.
Implementation and retry await explicit approval.

2026-09-26: Phase 1C implementation and mocked contract gate complete. Phase 1B
remains complete. No deployment, transaction, live LLM call, frontend, dependency
installation, or publication was performed.

- Full contract gate: `.venv/bin/pytest -q tests/test_phase1b.py tests/test_phase1c.py --tb=short` — 91 passed (49 boundary/storage and 42 retrieval/consensus cases).
- During edits: 39 Phase 1C cases passed, then 3 added affected cases passed.
- `.venv/bin/python scripts/check-contract.py` — compilation, standard-library
  whitespace lint, installed SDK ABI/storage semantics, closure inspection, and
  SDK schema generation passed once at the final gate. ABI unchanged;
  `gl.storage.TreeMap[str, str]` remains supported. No dedicated linter installed.
- Mocked consensus executes both roles independently before commit. The pinned
  direct runner normally skips validator execution, so these tests use an explicit
  leader/validator harness. This verifies contract logic, not network consensus.

Verified SDK: cached GenVM v0.6.0-rc3 `web.get` returns `Response(status, headers,
body)` with byte headers/body; `exec_prompt` supports text and parsed JSON modes;
`vm.run_nondet(leader, validator)` supplies `vm.Return.calldata` to validators.
Extraction uses text mode to reject >8192 UTF-8 bytes before strict JSON parsing.
Each independent role fetches each supplied nonempty URL once, without crawling.
Text used for assessment is at most 32768 bytes per source.

Limits: the SDK has no request timeout, transfer-size cap, redirect control,
resolved-IP/final-URL metadata, or LLM token/output cap. Bounds are checked after
receiving data; they do not bound upstream transfer, generation, time, or VM
memory. Visible redirects are rejected. Exact primary-source host allowlist:
www.python.org, blog.python.org, discuss.python.org. This is the ABI's prescribed
fallback, not proof about service-side redirects or DNS. Execution failures abort;
reported source unavailability may yield a consensus insufficient-evidence record.

A serialization probe using the already cached GenVM cloudpickle library failed
with recursion under host Python 3.14; no package was installed or upgraded. The
mocked gate checks immutable closure captures and no self/storage capture. Actual
GenVM serialization/execution remains unverified by this host test environment.

Next: run an offline pinned GenVM runtime integration with mocked web/LLM host
responses to verify closure serialization and leader/validator execution, including
redirect behavior and failure atomicity. Confirm service-side destination policy
and resource limits before any separately authorized deployment or live evaluation.

## Bounded runtime verification — 2026-09-26

Stopped at the supported-path gate. Actual GenVM runtime verification is BLOCKED;
Phase 1C's 91 passing host tests do not establish GenVM compatibility or deployment
readiness. Contract code and dependencies were left unchanged; no contract suite
or schema checks were repeated.

Serialization cause: cached GenVM cloudpickle `3.1.0.dev0` imports the private
`pickle._getattribute` helper and calls it with a dotted-name string, expecting
`(object, parent)`. Host Python `3.14.4` instead accepts a list of path components
and returns only the object. Direct inspection reproduced an AttributeError for
`_getattribute(module, "_make_function")`; the new list form returns a function.
The serializer then fails to recognize helpers as importable references and falls
back to recursively serializing them. Integer serialization succeeded; a probe
with a plain lambda and no contract imports crashed with a segmentation fault.
This demonstrates a host-tool incompatibility independent of this contract. It
does NOT prove that the contract's closures serialize inside GenVM.

Versions inspected: Python 3.14.4, genlayer-test 0.30.0rc2, cached GenVM SDK/runners
v0.6.0-rc3, cached executor runner tree v0.2.17, cloudpickle 3.1.0.dev0. No actual
GenVM executor was run. No Python 3.12/3.13 was found on PATH, /usr/bin,
/usr/local/bin, or the inspected standard pyenv/uv installation locations. No
alternate environment was created. No `genvm` executable was on PATH; the cached
executor tree contains runner archives, not an installed executable/test host.

Installed `gltest.direct` substitutes host Python execution for `run_nondet`.
Installed `glsim` uses that same direct engine and bypasses cloudpickle for
callables. Official [glsim documentation](https://docs.genlayer.com/api-references/genlayer-test/glsim)
confirms that it runs without WASM. Neither is actual GenVM verification.
The supported [Studio integration route](https://github.com/genlayerlabs/genlayer-testing-suite/blob/main/docs/studio-runner.md)
uses local Studio, full consensus, and mocked validator web/LLM responses. It
requires deployment/write transactions, excluded by this phase. No supported
transaction-free offline GenVM execution host/harness was identified in the
installed pinned testing tools. No custom runner or speculative workaround built.

Actual GenVM local construction, closure serialization, independent retrieval,
valid-result storage/readback, rejected/runtime-failed evaluation atomicity, and
insufficient-evidence zero-day storage are all NOT RUN, not passing checks.

Allowlist inspection (no retrieval): 9 host-only expectations passed. All three
exact hostnames and uppercase hostname/default :443 form pass the syntactic
boundary; suffix spoofing, nested subdomains, bare python.org, HTTP, and credentials
fail. This proves initial-host matching only, not remote accessibility or public
DNS resolution. The allowlist DOES NOT constrain redirect destinations. Actual
GenVM host redirect-following behavior remains unverified; the SDK exposes no
redirect policy or final-URL metadata. Installed glsim's optional HTTP client uses
`follow_redirects=True`, but this is NOT evidence about the actual GenVM host.
If the actual host follows a redirect and returns a final 200 response, this
contract cannot detect or restrict that destination. Visible 3xx/Location responses
are rejected, without manually following them.

The 32768-byte body limit is checked after `web.get` returns the complete body;
the 8192-byte model-text limit is checked after `exec_prompt` returns. Neither is
a transfer, generation, elapsed-time, or memory cap.

Smallest supported verification route: obtain a compatible local Studio runtime
for the pinned GenVM family, then use existing gltest Studio-mode mocked validators
with leader-only disabled. This requires separately authorizing LOCAL test
construction/deployment and write transactions; it must not use hosted providers
or public-chain transactions. That authorization is absent here. If zero
transactions remains mandatory, an official transaction-free GenVM harness with
mock host services must first be provided; the installed tools do not supply one.

## Local Studio readiness — 2026-09-26

Local-only deployment/write authorization is now present; hosted transactions are
still forbidden. Readiness check stopped before deployment because a compatible
local Studio release is not installed or cached. No runtime installation,
container mutation, wallet creation, network-setting change, or transaction occurred.

- Docker client and daemon are available/running: Engine 29.8.0. Read-only daemon
  inspection required sandbox escalation and succeeded.
- Running Studio services use `yeagerai/simulator-{jsonrpc,frontend}:v0.65.0`;
  cached hardhat/database-migration images also use v0.65.0. Docker image inventory
  has no Studio v0.123 RC images. Other cached images are postgres:17-alpine and
  genlayer-genvm-webdriver:0.0.3. Existing containers were preserved.
- The jsonrpc container advertises port 4000 (bound on all interfaces), giving a
  candidate loopback URL `http://127.0.0.1:4000/api`; it was NOT contacted and no
  RPC/chain/runtime identity was verified. No compatible test endpoint was used.
- The [official compatibility table](https://docs.genlayer.com/developers/consensus-v06-migration)
  requires Studio v0.123 RC and consensus/node v0.6 RC with the project's CLI
  v0.40 RC, Python SDK v0.19 RC, and matching gltest prerelease family. The available
  v0.65.0 installation is outside that family and was not used for these tests.
- Official Studio integration supports mock-validator web and LLM responses.
  Installed `ValidatorFactory.create_mock_validator` accepts `mock_web_response`
  and `mock_llm_response`; plugin configuration maps web requests and exec_prompt
  to their mock responses. The [official Studio runner guide](https://github.com/genlayerlabs/genlayer-testing-suite/blob/main/docs/studio-runner.md)
  documents the full consensus route.
- Host Python 3.14.4 imported the pinned Studio ContractFactory and ValidatorFactory
  successfully. The inspected Studio RPC client path has no cloudpickle references;
  it submits contract source for serialization/execution inside server-side GenVM.
  Thus the prior host cloudpickle incompatibility is bypassed by this route in
  design, but end-to-end runtime success is not verified. No environment changes.

Integration checks actually performed: NONE. Closure serialization, independent
leader/validator execution, case write/readback, failure atomicity, and consensus
insufficient-evidence storage remain unverified in actual GenVM. Redirect behavior
was not exercised; existing redirect/final-destination and post-download-size
limitations remain. Contract source unchanged; neither the 91-test suite nor schema
checks were repeated.

Exact missing component: an installed/cached official Studio v0.123 RC stack with
matching consensus/node v0.6 RC and compatible GenVM, available for isolated local
mock-validator testing. Smallest setup required: provision that compatible official
release in a separate Compose project with dedicated volumes and an unused
loopback-only RPC port, preserving the existing v0.65.0 project. This requires a
new local runtime setup, explicitly excluded by the current instruction, so no
installation was attempted. Once supplied, use existing project-local gltest in
an isolated directory, disposable test account/local funds, full consensus and
complete mocks. Audit all client fallback endpoints as well as deploy/write RPCs:
installed ContractFactory contains a hosted schema fallback that must never be
allowed to contact a hosted endpoint during these local-only checks.

## Bounded Studio-dev protocol investigation — 2026-09-26

Result: end-to-end compatibility UNCONFIRMED; no protocol mismatch demonstrated.
The official [network configuration](https://docs.genlayer.com/developers/networks)
lists https://studio-dev.genlayer.com/api, chain 61997, for the RC Studio-dev
profile. The [release compatibility table](https://docs.genlayer.com/developers/consensus-v06-migration)
places the installed CLI 0.40.0-rc.3, JS 2.0.0-rc.1, Python 0.19.0rc2 and matching
gltest prerelease in the intended v0.6 / Studio v0.123 RC families. This table
establishes intended compatibility, not the live server's exact release.

Read-only live checks in this investigation: eth_chainId returned 0xf22d (61997);
sim_getFeeConfig returned enabled=true, fee policy/default distribution and
message-fee capabilities; sim_getConsensusContract("ConsensusMain") returned the
legacy nonpayable five-argument addTransaction ABI. That ABI came from LIVE SERVER
metadata at this exact endpoint, not from the bundled JS SDK or another endpoint.
The prior web3_clientVersion check returned Method not found: server version is
unavailable through that method, not established as incompatible. No guessed RPC
methods, unrelated-address probes, wallets or transactions were used.

Backend: Studio simulation/GenVM service with Ethereum-shaped RPC envelopes,
not deployment to ordinary EVM consensus bytecode. Installed JS studioDevnet has
isStudio=true. deployContract encodes source/constructor calldata and a fee-bearing
addTransaction tuple, obtains Studio fees through sim_getFeeConfig, and submits a
signed envelope through eth_sendRawTransaction (provider accounts may instead use
eth_sendTransaction). Studio handling does not require EVM NewTransaction logs.
Host Python/cloudpickle is absent from this JS submission path.

Official Studio [RPC source](https://github.com/genlayerlabs/genlayer-studio/blob/c94072951e483510329670aa427fba3fa6944f45/backend/protocol_rpc/rpc_methods.py)
explicitly returns "0x" for ALL eth_getCode addresses because Studio contracts
aren't EVM bytecode. Thus the previously observed empty code is expected and is
not evidence of incompatibility. sim_getConsensusContract is marked deprecated:
consensus metadata now comes from genlayer-js chain configuration. Official
[transaction parser](https://github.com/genlayerlabs/genlayer-studio/blob/c94072951e483510329670aa427fba3fa6944f45/backend/protocol_rpc/transactions_parser.py)
supports the fee-bearing tuple AND legacy five-argument form; the
[RPC implementation](https://github.com/genlayerlabs/genlayer-studio/blob/c94072951e483510329670aa427fba3fa6944f45/backend/protocol_rpc/endpoints.py)
decodes signed envelopes and persists Studio transactions. These sources at commit
c94072951e483510329670aa427fba3fa6944f45 explain the architecture; they do not prove
the hosted service runs that commit. Legacy metadata alone does not demonstrate
failure of the modern tuple submission path. No package/endpoint correction is
currently justified.

Supported candidate deployment path is the existing project-local CLI with the
explicit canonical RPC (see TOOLCHAIN.md). It was NOT executed. Controlled,
separately authorized deployment must still verify acceptance of the pinned
fee-bearing envelope, GenVM constructor success, deployed schema/readability and
transaction completion. A subsequent authorized evaluation must verify closure
serialization, independent validator assessment and atomic storage in actual
GenVM. The Python release case is valid for this insufficient-evidence verification;
a positive-extension fixture is not a prerequisite. Redirect destinations remain
unenforceable when the host follows redirects invisibly, and response bounds remain
post-download/post-generation checks rather than network transfer limits.

Only STATUS.md and TOOLCHAIN.md changed. No tests/schema checks repeated, source
changes, dependency changes, wallet inspection, evidence search or transactions.
Exact next step: obtain explicit hosted deployment authorization and a specifically
authorized DeadlineCheck account, then perform one controlled Studio-dev deployment
through the pinned CLI and inspect its lifecycle/GenVM result before evaluation.

## Authorized Studio-dev deployment preflight — 2026-09-26T09:16:42.163457+00:00

Stopped before submission as instructed: the pinned CLI lists the existing active
`default` keystore as 0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a, matching the
explicit authorization, but does not report it unlocked. No cached signing key is
reported accessible; cryptographic signer derivation has not yet been verified.
The project-local wrapper has no accounts because it redirects the CLI home to
.tool-home. The existing wallet must instead use the pinned CLI directly, without
copying keystores or secrets into this project.

Verified supported interactive unlock command, from this project root:

```sh
node node_modules/genlayer/dist/index.js account unlock --account default
```

This prompts locally for the password and caches the key in the supported OS
keychain. Do not pass --password or provide passwords in chat. Unlock was not
attempted. The CLI's account list startup required sandbox escalation for its
routine directory-permission operation on the existing ~/.genlayer directory;
no account/network selection or config-value change was performed.

Read-only live preflight: https://studio-dev.genlayer.com/api returned chain ID
0xf22d (61997). Authorized address balance: 9999523457999994003 wei,
9.999523457999994003 GEN. No fee estimate or contract-specific simulation was run
after identifying the locked-wallet gate. Installed estimate-fees supports a
generic estimate and targeted existing-contract write simulation; its CLI does
not expose a source-deployment simulation option.

Contract was not modified. Current SHA-256:
4f87bcd143e079dc1c4e3f87dd5e3561de879417a3a98fda492a1b99d16ff636.
Source modification timestamp precedes the recorded gate/test-cache timestamps;
no historical gate hash exists in the inspected records, so a cryptographic
comparison to the passing source cannot be claimed. No unchanged tests repeated.

No deployment submitted: no transaction hash, final status, constructor result,
contract address or missing-case RPC read exists. deployments/studio-dev.json was
not created because there are no actual deployment details to record. Existing
runtime/closure/consensus limitations remain unverified.

Exact next step: user runs the interactive unlock command above, then resume this
same authorized deployment. Verify the unlocked derived signer, obtain a generic
fee estimate (explicitly not a source simulation), and resolve source provenance
before the single permitted submission. Do not submit evaluate_delay.

## Manual deployment handoff — 2026-09-26T11:20:20Z

Supersedes the account-unlock next step above. No deployment was initiated.
Existing project files and status records contain no deployment receipt, transaction
hash or contract address; there is no deployments directory. No known submitted
transaction exists to track. Contract and dependencies remain unchanged.

Pinned CLI 0.40.0-rc.3 deploy help and installed implementation confirm direct
interactive keystore decryption: DeployAction.deploy -> getClient -> getAccount
-> decryptKeystore -> promptPassword. The prompt uses Inquirer password input
masked with `*`. Missing/unavailable keychain returns null and falls through to
the prompt. This path keeps the decrypted signing key in process memory and does
not call storePrivateKey. `account unlock` requires OS keychain caching and is
unnecessary. No password was requested or supplied in this turn.

Existing user CLI configuration selects activeAccount=default (network=studionet).
The default keystore public address matches the authorized signer:
0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a. This is public keystore metadata
verification, not cryptographic derivation from a decrypted key. Explicit --rpc
overrides the endpoint; resolveRpcChain queries eth_chainId and replaces the
configured Studio chain ID with the live ID. No wallet configuration was changed.

Read-only live RPC at https://studio-dev.genlayer.com/api returned 0xf22d (61997)
and balance 9999523457999994003 wei (9.999523457999994003 GEN). Node HTTP requests
succeeded; sandbox Python DNS failed and its escalated HTTP request received 403.
Pinned CLI generic estimate-fees --json returned feeValue=100000000000010352 wei
(0.100000000000010352 GEN), leader allocation 100, validator allocation 200,
rotations [3], appeal rounds 0, execution budget per round 25000000000000000 wei.
This is a generic fee preset, NOT a source-deployment simulation or guaranteed
deployment cost. CLI estimate-fees exposes existing-contract write simulation
only; no deployment simulation was performed.

Provenance gate rerun once for the current unchanged contract:

- `.venv/bin/pytest -q tests/test_phase1b.py tests/test_phase1c.py --tb=short`: 91 passed.
- `.venv/bin/python scripts/check-contract.py`: compilation, whitespace lint,
  pinned SDK ABI/storage/closure semantics and schema generation passed.
- SHA-256 checked after both gates and again before handoff:
  `4f87bcd143e079dc1c4e3f87dd5e3561de879417a3a98fda492a1b99d16ff636`.

Actual GenVM/runtime limitations documented above remain unverified. No hosted
evaluate_delay call, unrelated tests, dependency changes or publication occurred.

User-only next command, in a private interactive terminal from this project root:

```sh
node node_modules/genlayer/dist/index.js deploy --wallet keystore --contract contracts/DeadlineCheck.py --rpc https://studio-dev.genlayer.com/api
```

Deploy has no --account option; it uses the verified active default account.
Use the pinned CLI directly: the project wrapper selects a separate wallet home
without the authorized keystore. Enter the password only at the masked terminal
prompt. Omit --fee-value so the SDK derives the current deposit. Preserve any
printed Deployment Transaction Hash and inspect that transaction if waiting
fails; do not resubmit merely because the command times out.
