# Project-local Studio-dev toolchain (Phase 1A)

> **Historical toolchain record.** Statements below about no deployment, unconfirmed runtime compatibility, or future deployment commands describe the earlier phases. The current deployed contract and read-only reviewer instructions are in [README.md](../README.md) and [STATUS.md](STATUS.md). Do not use the old deployment commands for review.

Verified on 2026-09-23. This setup has not contacted Studio-dev or sent a transaction.

| Component | Exact local pin | Evidence |
| --- | --- | --- |
| CLI | `genlayer@0.40.0-rc.3` | [npm release](https://www.npmjs.com/package/genlayer/v/0.40.0-rc.3); local `network list` and `network info` |
| JavaScript client | `genlayer-js@2.0.0-rc.1` | [npm release](https://www.npmjs.com/package/genlayer-js/v/2.0.0-rc.1); local `studioDevnet` import |
| Python client | `genlayer-py==0.19.0rc2` | [PyPI release](https://pypi.org/project/genlayer-py/0.19.0rc2/); local `studio_devnet` import |
| Test runner | `genlayer-test==0.30.0rc2` | [PyPI release](https://pypi.org/project/genlayer-test/0.30.0rc2/); local import and pytest entry point |
| Python | `3.14.4` in `.venv` | Both Python RCs require `>=3.12`; their published classifiers list 3.12/3.13, while dependency resolution, imports, and `pip check` succeeded on 3.14.4 |

The [official v0.6 migration guide](https://docs.genlayer.com/developers/consensus-v06-migration) requires the CLI 0.40, JS 2.0, Python client 0.19, and matching test-profile RC families. The older CLI candidate `0.40.0-rc2` was published in July; `0.40.0-rc.3` was published September 3 alongside the Python RCs and exposes `studio-dev` locally. The global CLI remains `0.39.1` and was not changed.

## Install and inspect locally

Run from this project root:

```sh
npm ci --ignore-scripts
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python -m pip check
node scripts/genlayer-local.mjs --version
node scripts/genlayer-local.mjs network list
node scripts/genlayer-local.mjs network set studio-dev
node scripts/genlayer-local.mjs network info
.venv/bin/python -m pip show genlayer-py genlayer-test
```

`package.json` and `package-lock.json` pin the npm dependency tree. `requirements-toolchain.txt` lists direct Python pins; `requirements-lock.txt` records the resolved Python packages from this environment. Python 3.14.4 resolved compatible wheels and passed import checks; full contract and Studio execution remain untested. The local CLI writes its config under `.tool-home/.genlayer` through `scripts/genlayer-local.mjs`, keeping it inside this project without changing the user's `HOME`. The project-local active network alias is `studio-dev`; no wallet was created. `.venv`, `node_modules`, and `.tool-home` are ignored for any future version control, though Git has not been initialized.

## Preset check

| Tool | Preset | Chain ID | RPC |
| --- | --- | --- | --- |
| Local CLI | `studio-dev` | `61997` | `https://studio-dev.genlayer.com/api` |
| JavaScript SDK | `studioDevnet` | `61997` | `https://studio-dev.genlayer.com/api` |
| Python SDK | `studio_devnet` | `61997` | `https://studio-dev.genlayer.com/api` |

The CLI result came from `node scripts/genlayer-local.mjs network info`; JS and Python values came from importing their installed chain definitions. No RPC reachability, remote chain identity, or consensus deployment was queried in Phase 1A. The [official network reference](https://docs.genlayer.com/developers/networks) lists the same endpoint and ID.

## ABI capability result

The installed Python client accepts `str` and `int` as `CalldataEncodable`, and its encoder/decoder round-tripped both planned calls: `evaluate_delay` with four strings and one integer, and `get_case` with one string. `read_contract` and `write_contract` both expose `function_name` and `args` parameters. This verifies client-side argument encoding only. The GenVM contract SDK (`import genlayer`) is not supplied by these host packages, so the generated contract schema, decorators, storage type, and return behavior require an isolated contract-SDK/GenVM check in Phase 1B before implementation.

## Phase 1C offline gate

Use existing tools only:

```sh
.venv/bin/pytest -q tests/test_phase1b.py tests/test_phase1c.py --tb=short
.venv/bin/python scripts/check-contract.py
```

The check script loads the cached GenVM v0.6.0-rc3 SDK, compiles sources, checks
standard-library whitespace lint, verifies storage/ABI semantics, inspects closure
captures, and generates the SDK schema. It does not contact an RPC. SDK signatures
and decoding were inspected against the cached `genlayer/nondet/web.py`,
`genlayer/nondet/__init__.py`, and `genlayer/vm/__init__.py`. Official reference
examples: [web access](https://docs.genlayer.com/developers/intelligent-contracts/features/web-access),
[LLM calls](https://docs.genlayer.com/developers/intelligent-contracts/features/calling-llms),
and [independent equivalence](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle).
Installed source takes precedence where current examples use different API names.
See [status](STATUS.md) for unsupported limits and the host serializer limitation.

## Runtime verification boundary

The installed direct engine and glsim execute host Python, not GenVM/WASM; neither
is a substitute for actual runtime checks. The cached cloudpickle 3.1.0.dev0 uses
the pre-3.14 private pickle helper interface and fails on host Python 3.14.4 even
without contract imports. No compatible 3.12/3.13 interpreter or supported
transaction-free offline execution harness was found. The supported Studio-mode
mock-validator integration route requires local deployment/write transactions,
which remain unauthorized for this phase. See [STATUS.md](STATUS.md) for observed
results and the precise remaining verification route. Do not rerun the 91-test
suite or schema gate for these documentation-only findings.

## Studio-dev transport compatibility — 2026-09-26

The current official [network reference](https://docs.genlayer.com/developers/networks)
and [v0.6 release table](https://docs.genlayer.com/developers/consensus-v06-migration)
match this endpoint/chain and the pinned RC package families. Live read-only RPC
confirmed eth_chainId=61997 and sim_getFeeConfig support. Exact server release is
unavailable (the previous web3_clientVersion request was unsupported). Intended
compatibility is supported; actual deployment/runtime compatibility is UNCONFIRMED,
with no confirmed mismatch and no package or endpoint change required yet.

Installed JS/CLI Studio-dev transport uses isStudio=true, Studio fee RPC and an
Ethereum-shaped signed envelope via eth_sendRawTransaction, carrying the modern
fee-bearing addTransaction tuple. It does not execute deployment against ordinary
EVM bytecode or depend on EVM consensus event logs. The supported CLI command,
for a future separately authorized deployment from this project root, is:

```sh
node scripts/genlayer-local.mjs deploy --contract contracts/DeadlineCheck.py --rpc https://studio-dev.genlayer.com/api
```

Do not run this command during a read-only investigation. Account authorization
and transaction completion/GenVM success remain separate verification gates. This
JS source submission path does not invoke host Python/cloudpickle.

The five-argument legacy ABI was returned by live
sim_getConsensusContract("ConsensusMain") at this endpoint. It is not the pinned
JS deployment ABI. Official Studio source marks that metadata method deprecated,
uses chain-config metadata for modern clients, and its parser supports both forms.
See [RPC registration](https://github.com/genlayerlabs/genlayer-studio/blob/c94072951e483510329670aa427fba3fa6944f45/backend/protocol_rpc/rpc_methods.py),
[parser](https://github.com/genlayerlabs/genlayer-studio/blob/c94072951e483510329670aa427fba3fa6944f45/backend/protocol_rpc/transactions_parser.py)
and [implementation](https://github.com/genlayerlabs/genlayer-studio/blob/c94072951e483510329670aa427fba3fa6944f45/backend/protocol_rpc/endpoints.py).
The RPC registration intentionally returns empty eth_getCode for every address;
empty EVM code is expected for this Studio backend, not a compatibility test.
The inspected official source commit is not an established live server version.

A controlled deployment must verify modern envelope decoding/fee handling and
actual GenVM constructor execution, followed by a separately authorized evaluation
for closures/consensus/storage. The Python release insufficient-evidence case is
sufficient for that runtime test. Existing redirect-destination and post-download
response-size limitations remain unchanged; see STATUS.md. No checks were repeated
and no tooling/configuration changes were applied in this investigation.

## Existing authorized keystore: private manual deployment

Verified 2026-09-26 against pinned deploy help and implementation. The wrapper
above uses `.tool-home` and cannot access the existing authorized default wallet.
Use the pinned CLI directly from `/home/ehsan/deadline-check`:

```sh
node node_modules/genlayer/dist/index.js deploy --wallet keystore --contract contracts/DeadlineCheck.py --rpc https://studio-dev.genlayer.com/api
```

The verified active default public address is
0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a. Deploy does not support --account.
Its explicit RPC resolves live Studio chain ID 61997 even though the existing
user network configuration is studionet. No configuration change is needed.
When the OS keychain is unavailable, getAccount falls back to a masked interactive
password prompt and decrypts the keystore in process memory without caching it.
Do not run account unlock first or supply a password through flags/files/env/chat.
This command is a user-only handoff and was not executed by Codex.

The read-only generic fee estimate was 100000000000010352 wei; it is not a
deployment simulation. The current source SHA-256 and the once-repeated 91-test
and semantic/schema gates are recorded in STATUS.md under manual deployment
handoff. Actual GenVM execution remains unverified until a deployment succeeds.
