# DeadlineCheck ABI and case schema

## Public methods

```python
@gl.public.write
def evaluate_delay(self, case_id: str, milestone_url: str, evidence_url_1: str, evidence_url_2: str, requested_days: int) -> None:
    ...

@gl.public.view
def get_case(self, case_id: str) -> str:
    ...
```

Exactly one write per new `case_id`; duplicates raise a user error before fetching evidence. `get_case` returns an empty string for an unknown ID; otherwise it returns a JSON string with the exact fields below. Optional evidence URLs use `""` sentinels, with no gap (`evidence_url_2` requires `evidence_url_1`). This keeps all ABI arguments scalar. There is no update, retry, admin, or second read method. A failed transaction does not create a case; a client must track its transaction ID before considering another submission.

The [official first-contract example](https://docs.genlayer.com/developers/intelligent-contracts/first-contract) documents `@gl.public.write`, `@gl.public.view`, and `str`; the [primitive types guide](https://docs.genlayer.com/developers/intelligent-contracts/types/primitive) documents public `int` arguments and `str` returns. The pinned GenVM v0.6.0-rc3 contract SDK generates persistent `TreeMap[str, str]` storage keyed by `case_id`; Python `dict` and `list` are not storage annotations. Phase 1A confirmed that the pinned Python client round-trips the proposed scalar method arguments through its calldata encoder; see [toolchain check](TOOLCHAIN.md). The sole signature correction is the explicit `-> None` on `evaluate_delay`: the SDK otherwise emits an `any` return type for an unannotated method, although this write returns no value. The intended generated return type is `null`.

The generated GenVM `v0.6.0-rc3` schema confirms `evaluate_delay` has four `string` arguments and one `int`, `readonly: false`, `ret: "null"`; `get_case` has one `string` argument, `readonly: true`, `ret: "string"`. The constructor has no arguments. No private method appears in the schema.

Phase 1C independently retrieves and assesses the bounded sources in leader and validator execution, then compares the canonical four-field decision. After consensus, the deterministic path validates the result again and invokes the private persistence helper. Missing original obligation, deadline, completion, or required causal dates produces `INSUFFICIENT_EVIDENCE` with zero days. Malformed responses, disagreement, and execution errors write nothing. See [phase status and runtime limitations](STATUS.md).

## Stored JSON, version 1

The JSON below is a historical illustrative schema example, **not** the result of the verified live case. The actual stored case is documented in [STATUS.md](STATUS.md) and [evaluation evidence](../deployments/evidence/evaluation-ab0d7616-2026-09-29.json).

```json
{
  "schema_version": 1,
  "case_id": "python-3130-final-delay",
  "milestone_url": "https://blog.python.org/2024/09/python-3130rc2-3126-31110-31015-3920/",
  "evidence_url_1": "https://discuss.python.org/t/python-3-12-7-and-3-13-0rc3-released/66306",
  "evidence_url_2": "https://www.python.org/downloads/release/python-3130/",
  "requested_days": 7,
  "verdict": "NON_EXCUSABLE_DELAY",
  "approved_days": 0,
  "responsible_party": "MILESTONE_OWNER",
  "reason_code": "OWNER_CONTROLLED",
  "explanation": "The final release moved six days after the original date because the project reverted a performance regression."
}
```

The canonical decision is the four-field tuple `(verdict, approved_days, responsible_party, reason_code)`. The explanation is stored for display but excluded from canonical equivalence. Input fields and `schema_version` are deterministic and must reproduce exactly. JSON is emitted with fixed keys and normalized encoding; the read returns the same logical record on every call. `approved_days` is always an integer in `[0, requested_days]`.

## Input and output limits

| Field | Rule |
| --- | --- |
| `case_id` | 3–64 ASCII characters, regex `[a-z0-9][a-z0-9_-]{2,63}`; exact-match unique, no whitespace |
| URLs | Absolute HTTPS only; 12–240 ASCII bytes each; host must be a public DNS name; no credentials, fragment, IP literal, localhost, or private destination; no redirects to disallowed destinations; no duplicate URL; no control characters |
| `milestone_url` | Required, must identify one specific milestone and an original dated commitment |
| `evidence_url_1`, `evidence_url_2` | Each either empty or a valid URL; at most two additional URLs; `evidence_url_2` cannot be populated alone |
| `requested_days` | Python `int`, excluding `bool`; whole number 1–30, no coercion from strings/floats |
| Fetched content | At most 32 KiB UTF-8 text per URL used for evaluation; non-text, oversized, inaccessible, or ambiguous content is unavailable evidence |
| `explanation` | 1–280 UTF-8 characters, one sentence, no unsupported factual assertion or pasted page text |
| Output enums | Only values in `DECISION_RULES.md`; no free-form verdict/reason/responsibility |

All URL checks happen before any network fetch. URL destination validation must also cover redirects and resolved public addresses, subject to what GenVM web access supports; if this cannot be enforced in Phase 1, narrow allowed hosts to an explicit public-source allowlist. Evidence is untrusted data, never instructions to the contract or LLM. Input text is bounded by URL and ID limits; the caller cannot supply a prose claim.

The [web access guide](https://docs.genlayer.com/developers/intelligent-contracts/features/web-access) documents `gl.nondet.web.get`; the [prompt guide](https://docs.genlayer.com/developers/intelligent-contracts/crafting-prompts) documents `gl.nondet.exec_prompt(..., response_format="json")`. Both run inside a nondeterministic block, with the storage write only after equivalence consensus per the [nondeterminism guide](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism). Phase 1 must verify actual SDK behavior for response bytes, redirects, size handling, and JSON parsing before implementation.

## Verified Phase 1C SDK limits

The cached GenVM v0.6.0-rc3 API uses `response.status`, not the current web
guide's `status_code`. `response.headers` values and `response.body` are bytes.
`web.get(url)` has only headers/sign options; no timeout, redirect, size, or
resolved-address options are exposed. Visible non-200/redirect responses, missing
or unsupported media types, invalid UTF-8, and bodies above 32768 bytes are
unavailable evidence. Content is not truncated because omitted text could change
the decision. The exact host allowlist is `www.python.org`, `blog.python.org`,
`discuss.python.org`; other syntactically valid public URLs raise
`SOURCE_HOST_NOT_ALLOWED` before retrieval. This narrows the Phase 1B URL boundary
according to the prescribed allowlist fallback. Service-side redirect/DNS behavior
is unverified; no final-URL metadata is available.

`exec_prompt(..., response_format="json")` returns already parsed JSON in this SDK.
The implementation uses supported text mode, checks 8192 UTF-8 bytes, then parses
strict JSON without duplicate keys/nonfinite constants. Neither mode exposes a
token cap. Both content and output bounds apply after reception, not to transfer,
generation, memory, or elapsed time. Prompt input is limited to at most three
bounded records. Calls stay inside `gl.vm.run_nondet(leader, validator)`; this
pinned SDK does not expose the documentation example's `run_nondet_unsafe`.

Runtime-verification clarification: the three-host allowlist constrains only the
initial URL hostname. It does **not** constrain redirect destinations. Actual
GenVM service redirect behavior could not be exercised with the installed offline
tools. If redirects are followed service-side and only the final response is
returned, final destination enforcement is unavailable to this contract. Visible
redirect rejection is not proof of redirect safety. See [STATUS.md](STATUS.md).
