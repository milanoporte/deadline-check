# Revised first live evaluation preview — not submitted

> **Historical preparation record.** This preview predates the verified deployment and evaluation. Its expected substantive verdict did not occur: the latest live case stored `INSUFFICIENT_EVIDENCE / EXTRACTION_FAILED / 0`. Do not use its manual write command as reviewer instructions. See [README.md](../README.md) and [STATUS.md](STATUS.md) for the current read-only review.

Replaces the source-unavailable candidate. Only this preview and its JSON record
were revised. Search stopped after eight candidate URLs (seven direct GETs,
one initial web review using existing direct-GET evidence).

Same recorded Python 3.13.0 final-release delay, using official Python Discourse
JSON, with no mirror, proxy, synthetic page, client extraction or truncation.
Exact ordered evaluate_delay arguments:

```json
[
  "python-3130-final-1790441362822",
  "https://discuss.python.org/t/62694.json",
  "https://discuss.python.org/posts/195069.json",
  "https://discuss.python.org/posts/196505.json",
  7
]
```

| Source | Raw bytes | Purpose |
| --- | ---: | --- |
| [0](https://discuss.python.org/t/62694.json) | 21504 | Original final-release obligation and October 1, 2024 deadline |
| [1](https://discuss.python.org/posts/195069.json) | 18582 | October 1 explanation: incremental GC regression and project decision to revert |
| [2](https://discuss.python.org/posts/196505.json) | 18604 | October 7 announcement of completed stable final release |

Every exact URL returned HTTP 200, no Location/redirect, application/json with
UTF-8 charset, strictly valid UTF-8, and a complete raw body below 32768 bytes.
Direct GET disabled redirect following. Headers, sizes, SHA-256 and all bounded
candidate results are retained in [preview JSON](../deployments/first-evaluation-preview.json).
Full topic and commitment-post JSON alternatives were oversized and rejected.

Source 0 is the official release-team thread: Łukasz Langa's September 7 post
quotes his original announcement and retains the complete final-release deadline
clause. This site-generated attributed quotation is not a client-truncated page.
The thread also discusses rc2: the intended milestone is explicitly **3.13.0 final**.
Its dated post metadata supplies the year. Source 1 records release-manager
Thomas Wouters's decision to revert project code; source 2 is his dated final-release
announcement. Links embedded in JSON are evidence context, not extra fetch inputs.

Expected: **NON_EXCUSABLE_DELAY / MILESTONE_OWNER / OWNER_CONTROLLED / 0**.
The proved final-release delay is six calendar days, October 1 to October 7;
requested seven days is a cap, not proof of any extension. No incomplete blocker
interval or revised target is presented as positive-extension evidence.

Uncertainty: source 0 uses an attributed quotation inside an rc2 thread rather
than the entire original announcement. Assessments must distinguish milestones
and use dated metadata; unresolved identity/date/cause produces insufficient
evidence. GenVM retrieval may differ. JSON escaping means model quotations must
match the fetched JSON literally. Independent models may disagree, return invalid
output or exhaust resources, storing nothing. Hosted web/LLM behavior remains
unverified; this is a meaningful candidate, not guaranteed execution success.

Read-only get_case for `python-3130-final-1790441362822` again returned `""` at
2026-09-26T17:04:05.834Z; chain 61997 and unchanged live fee policy verified.
Retained the previous pinned-SDK generic write distribution and deposit:
leader/validator 100/200, rotations [3], appeals 0, execution budget per round
25000000000000000 wei, message fees 0, caps 2/300000000/300000000.
SDK deposit **100000000000010352 wei (0.100000000000010352 GEN)**.
Previously observed balance **9999289511249991534 wei**, as of
2026-09-26T16:49:31.198Z; balance was not refreshed. Budget is an explicitly unmeasured
fallback for evaluation, not a constructor-derived sufficiency claim.

## Manual command — only after explicit approval

Private interactive Bash terminal, project root; authorized default signer
`0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a`. The pinned CLI's keystore path uses a masked password
prompt unless a matching key is already cached. Supply no password in flags,
files, environment or chat. Preserve the public transaction hash and track the
same transaction if waiting fails; never resubmit merely for a timeout.

```bash
set -o pipefail
node node_modules/genlayer/dist/index.js write 0xe6f388C923b148C02Bf156357AaE19eBd7A350bb evaluate_delay --wallet keystore --rpc https://studio-dev.genlayer.com/api --fees '{"distribution":{"leaderTimeunitsAllocation":"100","validatorTimeunitsAllocation":"200","appealRounds":"0","executionBudgetPerRound":"25000000000000000","executionConsumed":"0","totalMessageFees":"0","rotations":["3"],"maxPriceGenPerTimeUnit":"2","storageFeeMaxGasPrice":"300000000","receiptFeeMaxGasPrice":"300000000"}}' --args python-3130-final-1790441362822 https://discuss.python.org/t/62694.json https://discuss.python.org/posts/195069.json https://discuss.python.org/posts/196505.json 7 | tee deployments/first-evaluation-manual.log
```

The command submits once and logs Write Transaction Hash before waiting.
No command was run, wallet decrypted, transaction submitted, dependencies or
contract changed, deployment performed or passing test repeated. Refresh balance,
policy, source suitability and unused case ID if approval is delayed.
