# DeadlineCheck decision rules

The contract evaluates evidence for a single named milestone against the original public commitment. A later edited schedule is not automatically the original promise. A party is responsible only when public evidence attributes a dated blocker or delay to it. If the commitment, milestone identity, dates, causal link, or blocker duration cannot be established, use `INSUFFICIENT_EVIDENCE`; do not infer missing dates. The requested days are a cap, never evidence of duration.

## Canonical values and decision table

| Proven facts from the allowed URLs | Verdict | Responsible party | Reason code | Approved days |
| --- | --- | --- | --- | --- |
| Original dated commitment and actual milestone date show no delay | `NON_EXCUSABLE_DELAY` | `NONE` | `NO_PROVEN_DELAY` | 0 |
| Delay proved; evidence attributes it to owner-controlled planning, implementation, or avoidable rework | `NON_EXCUSABLE_DELAY` | `MILESTONE_OWNER` | `OWNER_CONTROLLED` | 0 |
| Delay proved; dated outside blocker beyond owner's control is causally linked to milestone and its duration is established | `EXCUSABLE_DELAY` | `EXTERNAL_PARTY` | `EXTERNAL_BLOCKER` | `min(requested_days, proved_blocker_days, proved_delay_days)` |
| Delay proved; both external blocker and owner-controlled cause materially contributed, with separable dated external blocker interval | `SHARED_RESPONSIBILITY` | `SHARED` | `MIXED_CAUSES` | `min(requested_days, proved_external_days, proved_delay_days)` |
| Same shared causation, but external interval cannot be separated and measured | `SHARED_RESPONSIBILITY` | `SHARED` | `DURATION_UNPROVEN` | 0 |
| External cause established but its duration or actual delay duration is not established | `EXCUSABLE_DELAY` | `EXTERNAL_PARTY` | `DURATION_UNPROVEN` | 0 |
| Commitment, actual milestone, causation, source identity, or attribution unresolved; or material sources conflict | `INSUFFICIENT_EVIDENCE` | `UNKNOWN` | `INSUFFICIENT_RECORD` or `CONTRADICTORY_RECORD` | 0 |
| Required page inaccessible, non-text, oversized, undated where date is necessary, or cannot be verified | `INSUFFICIENT_EVIDENCE` | `UNKNOWN` | `SOURCE_UNAVAILABLE` or `INSUFFICIENT_RECORD` | 0 |
| Model response fails strict JSON parsing or bounded assessment validation | `INSUFFICIENT_EVIDENCE` | `UNKNOWN` | `EXTRACTION_FAILED` | 0 |

Reason codes are exactly `NO_PROVEN_DELAY`, `OWNER_CONTROLLED`, `EXTERNAL_BLOCKER`, `MIXED_CAUSES`, `DURATION_UNPROVEN`, `INSUFFICIENT_RECORD`, `CONTRADICTORY_RECORD`, `SOURCE_UNAVAILABLE`, `UNDATED_RECORD`, `EXTRACTION_FAILED`. Responsibility values are exactly `NONE`, `MILESTONE_OWNER`, `EXTERNAL_PARTY`, `SHARED`, `UNKNOWN`.

Count calendar days from dated interval endpoints, with an end-exclusive convention: `[start_date, end_date)`. Count only days that overlap the proved delay interval after the original due date. Merge overlapping intervals before counting; no double counting. If only a vague statement such as “several days” is available, approved days are zero. If a source supplies a clear numeric duration but not calendar endpoints, require an equally clear causal link to this milestone and a proved actual delay interval; otherwise zero. A declared revised target is not proof that the blocker lasted until that date.

## Evidence handling

1. The milestone URL must establish a specific software deliverable and dated original commitment, or return `INSUFFICIENT_EVIDENCE`. Public assertions in the two optional URLs must refer to the same milestone. A release record can prove actual completion; a status note can prove a blocker; neither alone proves causation.
2. Prefer dated primary project records and release pages. A later source may verify history, but conflicting contemporaneous records are not resolved by source popularity. Material contradictions in original deadline, completion, cause, or blocker endpoints produce `CONTRADICTORY_RECORD` unless one record explicitly corrects the other with a dated correction.
3. A missing optional page is ignored only when cited facts from the remaining pages establish the complete decision. A missing milestone page produces `SOURCE_UNAVAILABLE`. An absent needed date or unclear assertion produces `INSUFFICIENT_RECORD` (or `SOURCE_UNAVAILABLE` if a page was unavailable). The `UNDATED_RECORD` enum remains valid but is not emitted by this extraction path.
4. `NON_EXCUSABLE_DELAY` requires affirmative evidence of no delay or an owner-controlled cause. Mere absence of proof for an external blocker leads to `INSUFFICIENT_EVIDENCE`, not an adverse verdict.
5. Apply deterministic bounds after model output: valid enum combination; integer days; `0 <= approved_days <= requested_days`; zero on insufficient or non-excusable decisions; no approved days without a proved dated duration. Invalid output is rejected, never silently corrected. Only the explicitly handled extraction failures below become a distinguishable zero-day outcome.

## Explicit extraction failure handling

Strict `json.loads` failures (`ValueError`, including invalid JSON, duplicate keys
and nonfinite constants, or `RecursionError`) and bounded assessment validation
failures (`INVALID_ASSESSMENT`, `INVALID_FACT`, `INVALID_DATE`,
`INVALID_BLOCKER`, or parsed `OUTPUT_TOO_LARGE`) produce `INSUFFICIENT_EVIDENCE` / `UNKNOWN` /
`EXTRACTION_FAILED` / 0. The fixed explanation is: “The model assessment could
not be parsed or its extracted facts failed strict validation.” This records
failed extraction, not a substantive judgment that the public records themselves
are insufficient. No source-unavailable substitution, fact repair, JSON fragment
selection, fence stripping, retry, or extra model call occurs. The later bounded
Discourse JSON prompt preprocessing is recorded in [STATUS.md](STATUS.md).

The raw type/8192-byte guard and unrelated runtime/model errors still abort.
Fact shape, source index, exact quote membership and value bounds remain strict.
Each validator retrieves and evaluates the evidence independently for a returned failure just
as for any other canonical result. Parse failure and invalid fact may agree on
the same extraction-failure category; extraction failure versus another reason
(even another zero-day insufficient outcome) disagrees. Non-Return leader errors
remain rejected. Storage happens only after canonical agreement and deterministic
revalidation. Public method signatures and stored record fields/schema version
are unchanged; the reason-code vocabulary gains `EXTRACTION_FAILED`.

Both finalized evaluations stored `EXTRACTION_FAILED`, but their raw model
responses are unavailable. This smaller response schema is a focused attempt to
reduce extraction failures, not a proven fix for a known root cause.

## Validator equivalence

Leader and validators each fetch the same allowed URLs and independently derive the canonical four-field decision. Validators require exact agreement on `verdict`, `approved_days`, `responsible_party`, and `reason_code`, plus the deterministic input fields and schema version. No numeric tolerance is allowed for days. They verify enum consistency and bounds before comparison. The contract supplies a fixed explanation for each derived result; it is validated but not compared. A schema-only validator is insufficient because it would trust the leader's conclusion. The [Equivalence Principle guide](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle) describes independent verification with `gl.vm.run_nondet` (the pinned SDK name; current examples call it `run_nondet_unsafe`); the [LLM guide](https://docs.genlayer.com/developers/intelligent-contracts/features/calling-llms) shows JSON output. LLM text is evidence analysis, not authority to invent a date or override these rules.

## Phase 1C conservative date requirement

For this phase, missing required completion or causal interval dates produces
`INSUFFICIENT_EVIDENCE` / `UNKNOWN` / `INSUFFICIENT_RECORD` / 0 when sources are
available; an unavailable source can produce `SOURCE_UNAVAILABLE`. This follows the
Phase 1C instructions. The frozen `DURATION_UNPROVEN` values remain valid stored
enums, but this implementation does not emit those table branches or approve
from numeric durations lacking calendar endpoints. No delivery is inferred from
silence. Source 0 must establish both the obligation and agreed original deadline.

The model now returns exactly six fields: `obligation`, `deadline`, `completion`,
`owner_cause`, `blockers`, and `conflict`. `owner_cause` is one optional fact;
`blockers` contains at most four flat external intervals with one source index,
one literal quote supporting the causal effect and containing both `start`/`end`
ISO dates verbatim. This conservative interval rule can reject natural-language
date statements even when a person could normalize them. The model does not
supply parties, verdict, approved days, or the stored explanation. A missing
owner cause and no supported interval cannot produce an adverse or positive
decision. Material conflicts fail closed.

Each extracted fact carries a source index and exact supporting quotation, checked
against the fetched record; dates must be valid ISO calendar dates. Independent
model assessment verifies the meaning and support of those quotations, including
corroboration of causal attribution; quote membership alone is not a semantic
proof. All available sources are supplied together to both independent assessments
so material contradictions cannot be dropped by selecting only favorable pages.
An unavailable optional source is ignored only if the remaining records establish
the complete decision.

The model extracts facts, not approved days. Deterministic code clips each proved
external blocker to `[original_deadline, actual_completion)`, merges overlapping
or touching intervals, sums their calendar-day lengths, and caps at requested
days. This already caps at the proved delay. A zero relevant interval or absent
causal support yields insufficient evidence. Owner-controlled rework and proved
no-delay cases approve zero. Leader and validators compare the canonical four
fields exactly; the fixed explanation is not part of that comparison. The
deterministic path validates the accepted schema and enum/day bounds again before
the sole storage write.
