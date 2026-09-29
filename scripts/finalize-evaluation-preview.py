"""Offline preview documentation and exact manual command; executes no submission."""
import json
import shlex
from pathlib import Path

p = Path('deployments/first-evaluation-preview.json')
data = json.loads(p.read_text())
data['expectedOutcomeIfCurrentBodiesReachGenVM'] = dict(
    verdict='INSUFFICIENT_EVIDENCE', responsible_party='UNKNOWN',
    reason_code='SOURCE_UNAVAILABLE', approved_days=0)
data['expectedOutcomeFromUsableFactsOnly'] = data.pop('expectedOutcome')
data['retrievalReady'] = False
data['approvalScope'] = 'Candidate final-release source-unavailable smoke test only; beta case is not recorded and substantive evidence evaluation is not retrieval-ready.'
fees = json.dumps({'distribution': data['feeEstimate']['distribution']}, separators=(',', ':'))
command = shlex.join([
    'node', 'node_modules/genlayer/dist/index.js', 'write', data['contractAddress'],
    'evaluate_delay', '--wallet', 'keystore', '--rpc', data['rpc'], '--fees', fees,
    '--args', *map(str, data['args'])])
data['manualCommand'] = command
p.write_text(json.dumps(data, indent=2) + '\n')
doc = f'''# First evaluation preview — not submitted

Prepared {data['preparedAt']}. Reuses finalized deployment metadata and completed
checks. The beta-release case and incomplete blocker interval are not recorded
in this workspace. Candidate below uses only the real final-release URLs recorded
in PLAN.md, subject to approval of that case substitution.

Exact ordered arguments and current RPC evidence: [preview](../deployments/first-evaluation-preview.json).
Case ID `{data['args'][0]}` is valid; read-only get_case returned `""`.
Signer `{data['authorizedSigner']}`; Studio-dev chain 61997;
contract `{data['contractAddress']}`.

## Source suitability and outcome

All three exact URLs have permitted hosts and valid HTTPS syntax. Direct GET with
redirect following disabled returned 200, UTF-8 HTML and no Location header.
Body sizes in argument order: 116917, 39851, 49464 bytes. **All exceed 32768 bytes**;
these exact sources are not currently retrieval-ready for substantive evaluation.
No truncation, synthetic replacement or alternate source was used. GenVM's HTTP
service may return different bodies; its redirect/final-destination behavior
remains unverified. Browser-extracted text size does not establish raw-body size.

Expected if those bodies reach GenVM: **INSUFFICIENT_EVIDENCE / UNKNOWN /
SOURCE_UNAVAILABLE / 0**. If all facts were usable, the recorded final case
supports an October 1 commitment, October 7 completion and project-controlled GC
regression rework: conditional NON_EXCUSABLE_DELAY / MILESTONE_OWNER /
OWNER_CONTROLLED / 0. Sources: [commitment]({data['args'][1]}),
[manager explanation]({data['args'][2]}), [completion]({data['args'][3]}).
No incomplete blocker interval or revised target establishes a positive extension.
Model disagreement, invalid output or resource exhaustion can fail execution and
store nothing. This candidate can at most be approved as a source-unavailable
smoke test; it cannot demonstrate substantive web/LLM assessment with these bodies.

## Funding

SDK generic write fallback: leader 100, validator 200, rotations [3], appeals 0,
execution budget per round 25000000000000000 wei, executionConsumed 0,
message fees 0, price caps 2 / 300000000 / 300000000. These are the pinned SDK
defaults: three permitted rotations, no appeals; no contract messages are emitted.
Policy quote is 1 wei per timeunit, storage/receipt 250000000, overlay 1500 bps.
Caps apply 20% price headroom. Budget is max(500000, admission floor
76548000000000, receipt price × 100000000), also above startup floor
78852000000000. Time allocations fall within the live 30–600 policy bounds.

SDK deposit **100000000000010352 wei (0.100000000000010352 GEN)**;
balance **9999289511249991534 wei (9.999289511249991534 GEN)**.
Balance covers the deposit. Four possible funded rounds do not mean four
submissions. No profile measures evaluation sufficiency, web/LLM consumption,
storage/receipt size or timing. Constructor success is not an evaluation profile.
No evaluate_delay or targeted simulation was run to produce this quote.

## User-only manual command after explicit approval

Run once in a private interactive Bash terminal from `/home/ehsan/deadline-check`.
Verify active account remains `default` with the authorized public address before
running; the pinned write command has no --account option. The existing keystore
path prompts with masked password input when no matching key is cached; a matching
OS keychain entry skips the password prompt. Do not pass a password via flags,
files, environment or chat. No unlock/cache operation is needed.

```bash
set -o pipefail
{command} | tee deployments/first-evaluation-manual.log
```

The CLI invokes writeContract once and prints `Write Transaction Hash:` before
waiting. Tee preserves that public hash and masked CLI output, not the password.
Omitted --fee-value lets SDK calculate the deposit from current policy. Refresh
chain/balance/policy and unused-ID read if approval is delayed; re-review any fee
change. After any submission attempt, preserve the hash/log and track that same
transaction through FINALIZED, inspect execution, then read get_case. A timeout,
error or missing stored case is not authorization to resubmit. If transport fails
without a hash, reconcile sender transaction history before considering another.

No command above was executed, wallet decrypted, transaction submitted, contract
or dependency changed, or passing test suite repeated.
'''
Path('docs/FIRST_LIVE_EVALUATION.md').write_text(doc)
print('Saved candidate preview and manual command; no submission.')
