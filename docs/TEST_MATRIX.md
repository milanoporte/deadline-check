# DeadlineCheck test matrix

Phase 1B uses `.venv/bin/pytest -q tests/test_phase1b.py` for direct deterministic tests only. The pinned `genlayer-test==0.30.0rc2` direct loader uses the project-local `.genvm-cache` with GenVM `v0.6.0-rc3`; its one-contract registration is reset between isolated test VMs. Phase 1C will use the official [GenLayer test guide](https://docs.genlayer.com/api-references/genlayer-test) for mocked web responses. The RC [migration guide](https://docs.genlayer.com/developers/consensus-v06-migration) calls for measured fee profiles before fee-funded writes.

Phase 1B focused cases cover accepted ID/URL/day boundaries, invalid scalars and URLs, evidence gaps and duplicates, missing-case reads, private storage serialization and duplicate IDs, result-schema rejection, and the public fail-closed path. All 49 direct cases passed on 2026-09-23. Syntax compilation, standard-library whitespace lint, SDK ABI/storage semantic checks, and actual schema generation also passed. The pinned toolchain does not include a dedicated GenVM linter; that additional lint check remains unavailable. Phase 1C now implements mocked D/E/C/R cases; lifecycle L1 remains unimplemented.

| ID | Fixture / check | Expected result |
| --- | --- | --- |
| V1 | ID and URL at exact bounds; 1 and 30 days | Accepted by deterministic validation |
| V2 | Duplicate ID, bad scheme/host/redirect, duplicate URLs, evidence URL gap, 0/31 days, bool/float days, oversized input | User error; no stored case and no fetch for invalid inputs |
| D1 | Original due date equals actual release date | `NON_EXCUSABLE_DELAY` / `NONE` / `NO_PROVEN_DELAY` / 0 |
| D2 | Proved owner-controlled late delivery | `NON_EXCUSABLE_DELAY` / `MILESTONE_OWNER` / `OWNER_CONTROLLED` / 0 |
| D3 | External blocker of 4 proved overlapping days, request 7 | `EXCUSABLE_DELAY` / `EXTERNAL_PARTY` / `EXTERNAL_BLOCKER` / 4 |
| D4 | External blocker 12 proved days, request 7 | Same verdict; cap at 7 |
| D5 | Mixed causes, 2 separable external days, request 7 | `SHARED_RESPONSIBILITY` / `SHARED` / `MIXED_CAUSES` / 2 |
| D6 | External or mixed cause established, duration undated | Corresponding verdict / `DURATION_UNPROVEN` / 0 |
| E1 | Commitment unavailable, ambiguous or undated | `INSUFFICIENT_EVIDENCE` / `UNKNOWN` / appropriate reason / 0 |
| E2 | Materially contradictory dated sources | `INSUFFICIENT_EVIDENCE` / `UNKNOWN` / `CONTRADICTORY_RECORD` / 0 |
| E3 | Optional page unavailable but remaining pages sufficient, then insufficient | Decisive verdict in first case; `SOURCE_UNAVAILABLE` or `INSUFFICIENT_RECORD` in second |
| C1 | Same canonical fields, different explanation wording | Validator agrees; explanation may differ |
| C2 | Changed verdict, reason, responsibility, or one approved day | Validator disagrees |
| R1 | Read known and unknown case; repeat known read | Fixed JSON schema and stable logical content; unknown returns `""` |
| L1 | Submission, provisional acceptance, failed execution, appeal/finalization | UI counts success only with successful execution; follows original transaction ID; final read agrees |

## When to run

- During Phase 1 ABI or validation implementation, run the narrow `gltest` file or selected cases for the changed rule after each meaningful edit. A pure documentation edit needs only link and consistency review.
- After changing nondeterministic fetch, prompt, equivalence, date arithmetic, storage schema, or dependencies, run all targeted D/E/C/R tests, including independent validator behavior. Regenerate a fee profile when a branch's execution cost materially changes.
- Run the full local `gltest` suite once before the first Studio-dev deployment or write, and again before any later live demo after contract/toolchain changes. Do not run it for every wording tweak in the explanation.
- On Studio-dev, perform one read-only chain/preset check first. If a live transaction is later authorized, verify the fee estimate and lifecycle through `Finalized`, including `FINISHED_WITH_RETURN`, then call `get_case`. A timeout resumes tracking the same transaction rather than submitting another.

The focused direct suite exists; no live integration configuration or lifecycle test exists.

## Phase 1C gate

42 mocked cases cover all four verdicts, missing original obligation/deadline and
completion, no proved delay, unavailable milestone/optional sources, visible
redirects, oversized/nontext/invalid UTF-8 bodies, contradictions, undated evidence,
missing causal intervals/support, overlap merging, delay clipping, extension caps,
malformed/oversized JSON, invalid extraction/result fields, independently changed
validator decisions/days/sources, explanation-only differences, and atomic storage
including preservation of an existing case. The consensus harness runs both roles
before commit; the default direct runner otherwise executes only the leader.

Final contract gate on 2026-09-26: 91 passed (49 Phase 1B + 42 Phase 1C).
Compilation, whitespace lint, pinned SDK semantic checks, and SDK schema generation
passed. Actual GenVM serialization and hosted resource policy remain unverified;
see [STATUS.md](STATUS.md). No live LLM calls or transactions were used.
