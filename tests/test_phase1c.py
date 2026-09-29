"""Mocked retrieval, independent consensus, date arithmetic and atomic commit."""
import copy
import json
import re
import sys

import pytest

MILESTONE = "https://www.python.org/milestone"
EVIDENCE = "https://blog.python.org/evidence"
OTHER = "https://discuss.python.org/evidence"
TEXT = ("Project agrees to deliver Release for Client on 2026-01-01. "
        "Release delivered 2026-01-11. External outage from 2026-01-01 to 2026-01-06 "
        "prevented delivery; independent records corroborate it. "
        "Owner rework also delayed Release. Outage from 2026-01-04 to 2026-01-09. "
        "External outage from 2025-12-01 to 2026-02-01 prevented delivery.")


def fact(value, source=0):
    return dict(source=source, quote=TEXT, value=value)


def assessment(cause="EXTERNAL"):
    return dict(obligation=fact("Release delivery"), deadline=fact("2026-01-01"),
                completion=fact("2026-01-11", 1),
                owner_cause=fact("Owner rework delayed Release", 1) if cause in ("OWNER", "MIXED") else None,
                blockers=[dict(source=1, quote=TEXT, start="2026-01-01", end="2026-01-06")]
                if cause in ("EXTERNAL", "MIXED") else [], conflict=False)


@pytest.fixture
def env(direct_deploy, direct_vm, monkeypatch):
    if "genlayer.contract" in sys.modules:
        sys.modules["genlayer.contract"].__known_contract__ = None
    contract = direct_deploy("contracts/DeadlineCheck.py")
    module = sys.modules[contract._instance.__class__.__module__]
    gl = module.gl
    state = dict(answers=[assessment(), assessment()], prompts=[], calls=[], closures=[])
    for url in (MILESTONE, EVIDENCE, OTHER):
        direct_vm.mock_web(re.escape(url) + "$", {"response": {
            "status": 200, "headers": {"content-type": b"text/plain; charset=utf-8"},
            "body": TEXT.encode()}})
    real_get = gl.nondet.web.get

    def get(url):
        assert direct_vm._in_nondet
        state["calls"].append(url)
        return real_get(url)

    def prompt(text, *, response_format):
        assert direct_vm._in_nondet
        assert response_format == "text"
        state["prompts"].append(text)
        answer = state["answers"].pop(0)
        if isinstance(answer, Exception):
            raise answer
        return json.dumps(answer) if type(answer) is dict else answer

    def consensus(leader, validator):
        # The host direct runner bypasses VM serialization. Inspect captures;
        # actual GenVM serialization is not asserted by this mocked harness.
        for fn in (leader, validator):
            assert all(cell.cell_contents is not contract._instance for cell in (fn.__closure__ or ()))
        state["closures"] = [leader, validator]
        direct_vm._in_nondet = True
        try:
            result = leader()
            assert contract._instance is not None
            if not validator(gl.vm.Return(result)):
                raise gl.vm.UserError("CONSENSUS_DISAGREEMENT")
            return result
        finally:
            direct_vm._in_nondet = False

    monkeypatch.setattr(gl.nondet.web, "get", get)
    monkeypatch.setattr(gl.nondet, "exec_prompt", prompt)
    monkeypatch.setattr(gl.vm, "run_nondet", consensus)
    return contract, module, state, direct_vm


def submit(env, days=7, second=""):
    env[0].evaluate_delay("case-001", MILESTONE, EVIDENCE, second, days)
    return json.loads(env[0].get_case("case-001"))


def set_answers(env, value):
    env[2]["answers"] = [copy.deepcopy(value), copy.deepcopy(value)]


@pytest.mark.parametrize("cause,verdict,party,reason,days", [
    ("OWNER", "NON_EXCUSABLE_DELAY", "MILESTONE_OWNER", "OWNER_CONTROLLED", 0),
    ("EXTERNAL", "EXCUSABLE_DELAY", "EXTERNAL_PARTY", "EXTERNAL_BLOCKER", 5),
    ("MIXED", "SHARED_RESPONSIBILITY", "SHARED", "MIXED_CAUSES", 5),
    ("UNKNOWN", "INSUFFICIENT_EVIDENCE", "UNKNOWN", "INSUFFICIENT_RECORD", 0),
])
def test_four_verdicts_independent_fetch_and_commit(env, cause, verdict, party, reason, days):
    set_answers(env, assessment(cause))
    result = submit(env)
    assert (result["verdict"], result["responsible_party"], result["reason_code"], result["approved_days"]) == (verdict, party, reason, days)
    assert env[2]["calls"] == [MILESTONE, EVIDENCE] * 2
    assert len(env[2]["prompts"]) == 2
    before = env[0].get_case("case-001")
    with pytest.raises(Exception, match="DUPLICATE_CASE_ID"):
        submit(env)
    assert env[0].get_case("case-001") == before
    assert len(env[2]["calls"]) == 4


@pytest.mark.parametrize("field", ["obligation", "deadline", "completion"])
def test_missing_required_fact_is_insufficient(env, field):
    a = assessment()
    a[field] = None
    set_answers(env, a)
    result = submit(env)
    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert result["approved_days"] == 0


def test_no_proven_delay(env):
    a = assessment()
    a["completion"] = fact("2026-01-01", 1)
    set_answers(env, a)
    assert submit(env)["reason_code"] == "NO_PROVEN_DELAY"


def test_conflicting_records(env):
    a = assessment()
    a["conflict"] = True
    set_answers(env, a)
    result = submit(env)
    assert result["reason_code"] == "CONTRADICTORY_RECORD"
    assert result["approved_days"] == 0


@pytest.mark.parametrize("status,headers,body", [
    (404, {"content-type": b"text/plain"}, b"missing"),
    (302, {"location": b"https://localhost/", "content-type": b"text/plain"}, b"redirect"),
    (200, {"content-type": b"image/png"}, b"image"),
    (200, {"content-type": b"text/plain"}, b"x" * 32769),
    (200, {"content-type": b"text/plain"}, b"\xff"),
    (200, {}, b"unknown media"),
])
def test_unavailable_milestone_no_llm(env, status, headers, body):
    env[3].clear_mocks()
    env[3].mock_web(".*", {"response": dict(status=status, headers=headers, body=body)})
    result = submit(env)
    assert result["reason_code"] == "SOURCE_UNAVAILABLE"
    assert env[2]["prompts"] == []


@pytest.mark.parametrize("complete,reason", [(True, "EXTERNAL_BLOCKER"), (False, "SOURCE_UNAVAILABLE")])
def test_unavailable_optional_page_only_ignored_if_independently_sufficient(env, complete, reason):
    env[3]._web_mocks.pop()
    env[3].mock_web(re.escape(OTHER), {"response": dict(status=503, headers={}, body=b"")})
    a = assessment()
    if not complete:
        a["completion"] = None
    set_answers(env, a)
    assert submit(env, second=OTHER)["reason_code"] == reason
    assert env[2]["calls"] == [MILESTONE, EVIDENCE, OTHER] * 2


@pytest.mark.parametrize("days,expected", [(3, 3), (30, 8)])
def test_overlap_union_and_extension_cap(env, days, expected):
    a = assessment()
    a["blockers"].append(dict(source=1, quote=TEXT, start="2026-01-04", end="2026-01-09"))
    set_answers(env, a)
    assert submit(env, days)["approved_days"] == expected


def test_blockers_clipped_to_actual_delay(env):
    a = assessment()
    a["blockers"][0]["start"] = "2025-12-01"
    a["blockers"][0]["end"] = "2026-02-01"
    set_answers(env, a)
    assert submit(env, 30)["approved_days"] == 10


@pytest.mark.parametrize("field", ["blockers", "owner_cause"])
def test_unproved_duration_or_causal_link(env, field):
    a = assessment("EXTERNAL" if field == "blockers" else "OWNER")
    a[field] = [] if field == "blockers" else None
    set_answers(env, a)
    result = submit(env)
    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert result["approved_days"] == 0


@pytest.mark.parametrize("raw,error", [("[]", "EXTRACTION_FAILED"), ("x" * 8193, "OUTPUT_TOO_LARGE")])
def test_malformed_or_oversized_json_atomic(env, raw, error):
    env[2]["answers"] = [raw, raw]
    if error == "OUTPUT_TOO_LARGE":
        with pytest.raises(Exception, match=error):
            submit(env)
        assert env[0].get_case("case-001") == ""
    else:
        assert submit(env)["reason_code"] == error


@pytest.mark.parametrize("change,error", [
    (lambda a: a.update(cause="EXCUSE"), "EXTRACTION_FAILED"),
    (lambda a: a.update(approved_days=7), "EXTRACTION_FAILED"),
    (lambda a: a.update(conflict=1), "EXTRACTION_FAILED"),
    (lambda a: a["deadline"].update(value="2026-02-30"), "EXTRACTION_FAILED"),
    (lambda a: a["blockers"][0].update(extra="invented"), "EXTRACTION_FAILED"),
])
def test_invalid_extraction_fields_fail_closed(env, change, error):
    a = assessment()
    change(a)
    set_answers(env, a)
    assert submit(env)["reason_code"] == error


def test_validator_disagreement_atomic(env):
    env[2]["answers"] = [assessment("EXTERNAL"), assessment("OWNER")]
    with pytest.raises(Exception, match="CONSENSUS_DISAGREEMENT"):
        submit(env)
    assert env[0].get_case("case-001") == ""
    assert len(env[2]["calls"]) == 4


def test_validator_changed_day_atomic(env):
    env[2]["answers"][1]["blockers"][0]["end"] = "2026-01-04"
    with pytest.raises(Exception, match="CONSENSUS_DISAGREEMENT"):
        submit(env)
    assert env[0].get_case("case-001") == ""


def test_validator_changed_sources_atomic(env):
    real_get = env[1].gl.nondet.web.get
    count = 0
    def get(url):
        nonlocal count
        count += 1
        if count == 3:
            raise env[1].gl.nondet.NondetException(["unavailable"], {})
        return real_get(url)
    from unittest.mock import patch
    with patch.object(env[1].gl.nondet.web, "get", get):
        with pytest.raises(Exception, match="CONSENSUS_DISAGREEMENT"):
            submit(env)
    assert env[0].get_case("case-001") == ""


def test_failed_new_case_preserves_existing_storage(env):
    old = submit(env)
    env[2]["answers"] = ["{bad", assessment()]
    with pytest.raises(Exception, match="CONSENSUS_DISAGREEMENT"):
        env[0].evaluate_delay("case-002", MILESTONE, EVIDENCE, "", 7)
    assert json.loads(env[0].get_case("case-001")) == old
    assert env[0].get_case("case-002") == ""


@pytest.mark.parametrize("raw", ["{bad", '{"cause":1,"cause":2}',
                                '{"cause":NaN}', '"' + "x" * 100,
                                "```json\n{}\n```", '{} trailing'])
def test_extraction_parse_failure_independent_agreement(env, raw):
    env[2]["answers"] = [raw, raw]
    result = submit(env)
    assert env[1]._canonical(result) == ("INSUFFICIENT_EVIDENCE", 0, "UNKNOWN", "EXTRACTION_FAILED")
    assert result["explanation"] == env[1]._extraction_failed()["explanation"]
    assert env[2]["calls"] == [MILESTONE, EVIDENCE] * 2
    assert len(env[2]["prompts"]) == 2


@pytest.mark.parametrize("change", [
    lambda a: a["obligation"].update(source=1),
    lambda a: a["deadline"].update(quote="fabricated quotation"),
    lambda a: a["completion"].update(source=True),
    lambda a: a["completion"].update(value=""),
    lambda a: a["completion"].update(extra="invented"),
    lambda a: a["blockers"][0].update(quote="fabricated blocker"),
    lambda a: a["blockers"][0].update(source=True),
    lambda a: a["blockers"][0].update(end="2026-01-10"),
])
def test_invalid_fact_independent_agreement_preserves_strict_check(env, change):
    a = assessment()
    change(a)
    with pytest.raises(env[1].gl.vm.UserError, match="INVALID_FACT"):
        env[1]._derive_decision(a, (TEXT, TEXT), 7)
    set_answers(env, a)
    assert submit(env)["reason_code"] == "EXTRACTION_FAILED"
    assert env[2]["calls"] == [MILESTONE, EVIDENCE] * 2
    assert len(env[2]["prompts"]) == 2


def test_different_extraction_failures_same_canonical_outcome(env):
    a = assessment()
    a["deadline"]["quote"] = "invented"
    env[2]["answers"] = ["{bad", a]
    assert submit(env)["approved_days"] == 0
    assert env[2]["calls"] == [MILESTONE, EVIDENCE] * 2


def test_json_parser_recursion_failure(env, monkeypatch):
    def exhausted(*args, **kwargs):
        raise RecursionError("parser depth")
    monkeypatch.setattr(env[1].json, "loads", exhausted)
    env[2]["answers"] = ["{}", "{}"]
    env[0].evaluate_delay("case-001", MILESTONE, EVIDENCE, "", 7)
    stored = env[0].get_case("case-001")
    assert '"reason_code":"EXTRACTION_FAILED"' in stored
    assert env[2]["calls"] == [MILESTONE, EVIDENCE] * 2


@pytest.mark.parametrize("kind", ["runtime", "unrelated_user"])
def test_derivation_errors_not_converted(env, monkeypatch, kind):
    error = RuntimeError("unexpected derivation") if kind == "runtime" else env[1].gl.vm.UserError("UNRELATED_ERROR")
    def broken(*args):
        raise error
    monkeypatch.setattr(env[1], "_derive_decision", broken)
    with pytest.raises(Exception, match="unexpected derivation|UNRELATED_ERROR"):
        submit(env)
    assert env[0].get_case("case-001") == ""


@pytest.mark.parametrize("reverse", [False, True])
def test_extraction_failure_vs_valid_decision_disagrees_atomic(env, reverse):
    answers = ["{bad", assessment("UNKNOWN")]
    env[2]["answers"] = answers[::-1] if reverse else answers
    with pytest.raises(Exception, match="CONSENSUS_DISAGREEMENT"):
        submit(env)
    assert env[0].get_case("case-001") == ""
    assert env[2]["calls"] == [MILESTONE, EVIDENCE] * 2


@pytest.mark.parametrize("error", [RuntimeError("runtime failure"), "user", "nondet"])
def test_validator_execution_failure_after_leader_extraction_failure_atomic(env, error):
    if error == "user":
        error = env[1].gl.vm.UserError("UNRELATED_ERROR")
    elif error == "nondet":
        error = env[1].gl.nondet.NondetException(["model unavailable"], {})
    env[2]["answers"] = ["{bad", error]
    with pytest.raises(Exception):
        submit(env)
    assert env[0].get_case("case-001") == ""
    assert len(env[2]["prompts"]) == 2


def test_non_return_leader_error_still_rejected(env):
    submit(env)
    before = len(env[2]["calls"])
    validator = env[2]["closures"][1]
    assert validator(env[1].gl.vm.UserError("INVALID_FACT")) is False
    assert len(env[2]["calls"]) == before


def test_extraction_failure_cannot_store_positive_days(env, monkeypatch):
    result = env[1]._extraction_failed()
    result["approved_days"] = 1
    monkeypatch.setattr(env[1].gl.vm, "run_nondet", lambda *_: result)
    with pytest.raises(Exception, match="INVALID_APPROVED_DAYS"):
        submit(env)
    assert env[0].get_case("case-001") == ""


def test_explanation_difference_accepted(env):
    assert submit(env)["explanation"] == "Cited dated external blockers delayed the milestone."


def test_execution_error_atomic(env):
    env[2]["answers"] = [RuntimeError("mock execution error")]
    with pytest.raises(Exception, match="mock execution error"):
        submit(env)
    assert env[0].get_case("case-001") == ""


# Minimal snapshots of the three official Discourse response shapes used by the
# Python 3.13.0 evaluation: one topic post stream and two individual posts.
DISCOURSE_URLS = (
    "https://discuss.python.org/t/62694.json",
    "https://discuss.python.org/posts/195069.json",
    "https://discuss.python.org/posts/196505.json",
)
ORIGINAL_QUOTE = "before we bless and release 3.13.0 final on October 1st."
CAUSE_QUOTE = "The incremental GC had more significant performance regressions in specific workloads than we expected."
OWNER_QUOTE = "We decided to revert back to the old GC in 3.13."
COMPLETION_QUOTE = "This is the stable release of Python 3.13.0"


def discourse_bodies():
    return (
        {"id": 62694, "post_stream": {"posts": [
            {"id": 188238, "topic_id": 62694, "username": "thomas",
             "created_at": "2024-09-03T12:49:08.858Z",
             "cooked": "<p>We’ve decided to push 3.13.0rc2 to this Friday, September 6.</p>"},
            {"id": 189134, "topic_id": 62694, "username": "ambv",
             "created_at": "2024-09-07T10:04:47.311Z",
             "cooked": "<blockquote>Final opportunity to test and find any show-stopper bugs "
                       + ORIGINAL_QUOTE + "</blockquote>"},
        ]}},
        {"id": 195069, "topic_id": 66306, "username": "thomas",
         "created_at": "2024-10-01T14:48:30.027Z",
         "cooked": "<p>Python 3.13.0rc3 rolls back incremental GC.</p>",
         "raw": "Python 3.13.0rc3 rolls back the incremental cyclic garbage collector. "
                + CAUSE_QUOTE + " " + OWNER_QUOTE + " "
                "The final release will now happen Monday October 7th."},
        {"id": 196505, "topic_id": 66972, "username": "thomas",
         "created_at": "2024-10-07T17:13:29.415Z",
         "cooked": "<h1>Python 3.13.0 is now available</h1>",
         "raw": "Python 3.13.0 is now available. " + COMPLETION_QUOTE + "."},
    )


def mock_discourse(env, bodies=None):
    env[3].clear_mocks()
    for url, body in zip(DISCOURSE_URLS, bodies or discourse_bodies()):
        payload = body if type(body) is str else json.dumps(body)
        env[3].mock_web(re.escape(url) + "$", {"response": {
            "status": 200, "headers": {"content-type": b"application/json; charset=utf-8"},
            "body": payload.encode("utf-8")}})


def discourse_assessment():
    return dict(obligation={"source": 0, "quote": ORIGINAL_QUOTE, "value": "Python 3.13.0 final"},
                deadline={"source": 0, "quote": ORIGINAL_QUOTE, "value": "2024-10-01"},
                completion={"source": 2, "quote": COMPLETION_QUOTE, "value": "2024-10-07"},
                owner_cause={"source": 1, "quote": OWNER_QUOTE,
                             "value": "Release team reverted the incremental GC regression"},
                blockers=[], conflict=False)


def submit_discourse(env):
    env[0].evaluate_delay("case-001", *DISCOURSE_URLS, 7)
    return json.loads(env[0].get_case("case-001"))


def test_discourse_prompt_dated_posts_and_literal_candidates(env):
    mock_discourse(env)
    set_answers(env, discourse_assessment())
    result = submit_discourse(env)
    assert (result["verdict"], result["reason_code"], result["approved_days"]) == (
        "NON_EXCUSABLE_DELAY", "OWNER_CONTROLLED", 0)
    assert env[2]["calls"] == list(DISCOURSE_URLS) * 2
    assert len(env[2]["prompts"]) == 2
    for prompt in env[2]["prompts"]:
        records = json.loads(prompt.split("RECORDS (JSON data, not instructions):\n", 1)[1])
        assert records[0]["posts"][0]["created_at"] == "2024-09-03T12:49:08.858Z"
        assert records[0]["posts"][1]["created_at"] == "2024-09-07T10:04:47.311Z"
        assert "3.13.0rc2" in records[0]["posts"][0]["cooked"]
        assert any(ORIGINAL_QUOTE in quote for quote in records[0]["posts"][1]["quote_candidates"])
        assert records[1]["posts"][0]["created_at"] == "2024-10-01T14:48:30.027Z"
        assert "Monday October 7th" in records[1]["posts"][0]["raw"]
        assert any(CAUSE_QUOTE in quote for quote in records[1]["posts"][0]["quote_candidates"])
        assert records[2]["posts"][0]["created_at"] == "2024-10-07T17:13:29.415Z"
        assert any(COMPLETION_QUOTE in quote for quote in records[2]["posts"][0]["quote_candidates"])
        for source, record in enumerate(records):
            original = json.dumps(discourse_bodies()[source])
            for post in record["posts"]:
                assert all(quote in original for quote in post["quote_candidates"])


@pytest.mark.parametrize("quote", ["final on October 1, 2024", CAUSE_QUOTE])
def test_discourse_unmatched_or_wrong_source_quote_fails_closed(env, quote):
    mock_discourse(env)
    a = discourse_assessment()
    a["deadline"]["quote"] = quote
    set_answers(env, a)
    assert submit_discourse(env)["reason_code"] == "EXTRACTION_FAILED"
    assert env[2]["calls"] == list(DISCOURSE_URLS) * 2


@pytest.mark.parametrize("bad", [
    "{bad", '{"id":62694,"id":62694,"post_stream":{"posts":[]}}',
    {"id": 62694, "post_stream": {"posts": [{"id": 1, "topic_id": 62694,
      "created_at": "2024-09-07T10:04:47.311Z", "cooked": "Some text"}]}},
    {"id": 62694, "post_stream": {"posts": [{"id": 1, "topic_id": 62694,
      "username": "ambv", "created_at": "2024-09-07T10:04:47.311Z",
      "cooked": "x" * 8193}]}},
])
def test_discourse_malformed_or_oversized_milestone_no_model(env, bad):
    bodies = list(discourse_bodies())
    bodies[0] = bad
    mock_discourse(env, bodies)
    assert submit_discourse(env)["reason_code"] == "SOURCE_UNAVAILABLE"
    assert env[2]["prompts"] == []


def test_discourse_total_content_bound_does_not_truncate_posts(env):
    bodies = list(discourse_bodies())
    bodies[0]["post_stream"]["posts"] = [
        {"id": 189134 + i, "topic_id": 62694, "username": "ambv",
         "created_at": "2024-09-07T10:04:47.311Z", "cooked": "Evidence. " * 700}
        for i in range(4)
    ]
    mock_discourse(env, bodies)
    assert submit_discourse(env)["reason_code"] == "SOURCE_UNAVAILABLE"
    assert env[2]["prompts"] == []


def test_discourse_missing_optional_post_text_requires_other_evidence(env):
    bodies = list(discourse_bodies())
    del bodies[1]["raw"]
    mock_discourse(env, bodies)
    a = discourse_assessment()
    a["owner_cause"] = None
    a["completion"] = None
    set_answers(env, a)
    assert submit_discourse(env)["reason_code"] == "SOURCE_UNAVAILABLE"


def test_discourse_validator_disagreement_keeps_storage_empty(env):
    mock_discourse(env)
    other = discourse_assessment()
    other["owner_cause"] = None
    env[2]["answers"] = [discourse_assessment(), other]
    with pytest.raises(Exception, match="CONSENSUS_DISAGREEMENT"):
        submit_discourse(env)
    assert env[0].get_case("case-001") == ""
    assert env[2]["calls"] == list(DISCOURSE_URLS) * 2


def test_unallowed_host_no_fetch(env):
    with pytest.raises(Exception, match="SOURCE_HOST_NOT_ALLOWED"):
        env[0].evaluate_delay("case-001", "https://arbitrary.org/page", "", "", 7)
    assert env[2]["calls"] == []
    assert env[0].get_case("case-001") == ""


def test_accepted_result_revalidated_before_commit(env, monkeypatch):
    monkeypatch.setattr(env[1].gl.vm, "run_nondet", lambda *_: dict(
        verdict="EXCUSABLE_DELAY", approved_days=True, responsible_party="EXTERNAL_PARTY",
        reason_code="EXTERNAL_BLOCKER", explanation="Unsupported result."))
    with pytest.raises(Exception, match="INVALID_APPROVED_DAYS"):
        submit(env)
    assert env[0].get_case("case-001") == ""
