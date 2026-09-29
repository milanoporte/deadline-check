# DeadlineCheck — Phase 0 plan

> **Historical plan.** This document records early assumptions and proposed writes. The latest contract is deployed, a read-only frontend now exists, and the verified live case stored `INSUFFICIENT_EVIDENCE / EXTRACTION_FAILED / 0`. Use [README.md](README.md) and [docs/STATUS.md](docs/STATUS.md) for current reviewer instructions and evidence. Do not run the proposed write commands below as reviewer steps.

Status: Phase 1C implementation and mocked contract gate complete, 2026-09-26; actual GenVM runtime integration remains next. See [phase status](docs/STATUS.md). No frontend, wallet, deployment, or transaction exists. See [toolchain details](docs/TOOLCHAIN.md).

## MVP boundary

One GenLayer Intelligent Contract evaluates one publicly documented software milestone per case. One `evaluate_delay` write evaluates and stores the case; one `get_case` view reads it. Inputs are one public original commitment URL, zero to two additional public evidence URLs, and a requested extension of 1–30 whole days. A later single-page frontend may submit and read cases. No backend, database, payment, escrow, uploads, dashboard, or second chain.

## Tool inventory after Phase 1A

| Tool | Installed finding | Studio-dev result |
| --- | --- | --- |
| GenLayer CLI | Project-local `0.40.0-rc.3`; global CLI remains `0.39.1` | Local `studio-dev` alias resolves to RPC and chain ID |
| `genlayer-js` | Project-local `2.0.0-rc.1`; global CLI still bundles `1.1.8` | Imported `studioDevnet` resolves to RPC and chain ID |
| Python client `genlayer-py` | `0.19.0rc2` in project `.venv` (Python 3.14.4) | Imported `studio_devnet` resolves to RPC and chain ID |
| Contract Python SDK `genlayer` | Not importable in host `.venv`; provided by GenVM contract environment | Generated contract schema still unverified |
| `genlayer-test` / `gltest`, pytest | `0.30.0rc2` / `9.1.1` in project `.venv` | Imports succeeded; suite not run |
| Foundry `forge` | 1.7.1; unrelated EVM test tool | Not a GenLayer contract test runner |
| Node / npm | 24.20.0 / 11.19.0 | Runtime inventory only |

Official [Consensus v0.6 migration guidance](https://docs.genlayer.com/developers/consensus-v06-migration) specifies Studio v0.123 RC, node/consensus v0.6 RC, `genlayer-js` v2.0 RC, `genlayer-py` v0.19 RC, CLI v0.40 RC, and matching `gltest` fee profiles. The [network guide](https://docs.genlayer.com/developers/networks) fixes the canonical preview RPC as `https://studio-dev.genlayer.com/api`, chain ID `61997`; stable Studionet is `61999`. Phase 1A selected CLI `0.40.0-rc.3` in place of the older `0.40.0-rc2` candidate. The exact local pins, installation commands, and check results are in [docs/TOOLCHAIN.md](docs/TOOLCHAIN.md).

## Lifecycle acceptance criteria

The write submission and the Intelligent Contract decision are separate. A submitted EVM transaction is not proof that the case was stored. `Accepted` is provisional and may be appealed; `Finalized` records the end of the appeal path. Both consensus status (`Accepted` or `Finalized`) **and** execution result `FINISHED_WITH_RETURN` are required for success. Poll `gen_getTransactionStatus` or SDK wait helpers; use `gen_getTransactionLifecycle` for stored/projected status and `resolutionAction`, never a fabricated readiness status. Resume tracking the original transaction ID after a timeout; do not send another evaluation. Read `get_case` after success, and prefer finalization before presenting an irreversible outcome. See [migration](https://docs.genlayer.com/developers/consensus-v06-migration), [finality](https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy/finality), and [status reference](https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/transactions/transaction-statuses).

## Phase 1 start

Phase 1B adds a fail-closed contract boundary: syntactic input checks, the SDK-supported `TreeMap[str, str]` storage model, one write and one read, and private serialization for later evidence-backed decisions. The public write never commits or returns a placeholder decision in this phase. The GenVM v0.6.0-rc3 SDK requires an explicit `-> None` annotation to generate the intended `null` write return type; see [ABI specification](docs/ABI_SPEC.md). Phase 1C must add real bounded web retrieval, enforce public destinations and redirects, establish the original obligation and deadline from the milestone URL, derive a decision under [decision rules](docs/DECISION_RULES.md), verify canonical equivalence independently, then invoke the private commit path. Run the targeted D/E/C/R tests before any hosted write.

## Public live-demo candidate (not submitted)

Use the Python 3.13.0 final release delay. The [September 7, 2024 Python Insider announcement](https://blog.python.org/2024/09/python-3130rc2-3126-31110-31015-3920/) says final release was planned for October 1. The [release manager's October 1 explanation](https://discuss.python.org/t/python-3-12-7-and-3-13-0rc3-released/66306) attributes the one-week postponement to an incremental-GC performance regression and says final release moved to October 7. The [official final release page](https://www.python.org/downloads/release/python-3130/) dates it October 7. Proposed input: case ID `python-3130-final-delay`, requested days `7`, commitment URL plus both evidence URLs. Expected `NON_EXCUSABLE_DELAY`, `OWNER_CONTROLLED`, `MILESTONE_OWNER`, zero approved days: the public explanation describes project-controlled rework, not an external blocker. This is an analytical classification for a demo, not a judgment about the release team's conduct. Confirm all three pages are accessible to GenVM before any later live demo. No transaction has been sent.
