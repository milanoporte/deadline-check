"""Focused direct tests for the deterministic Phase 1B contract boundary."""

import json
import sys

import pytest


CONTRACT = "contracts/DeadlineCheck.py"
MILESTONE = "https://www.python.org/downloads/release/python-3130/"
EVIDENCE_1 = "https://blog.python.org/2024/09/python-3130rc2/"
EVIDENCE_2 = "https://discuss.python.org/t/release/66306"


@pytest.fixture
def contract(direct_deploy, monkeypatch):
    # The RC direct loader reloads the file but does not reset the SDK's
    # one-contract-per-module registration between isolated test VMs.
    if "genlayer.contract" in sys.modules:
        sys.modules["genlayer.contract"].__known_contract__ = None
    deployed = direct_deploy(CONTRACT)
    import genlayer as gl
    def unavailable(*args):
        raise gl.vm.UserError("EVALUATION_UNAVAILABLE")
    monkeypatch.setattr(gl.vm, "run_nondet", unavailable)
    module = sys.modules[deployed._instance.__class__.__module__]
    monkeypatch.setattr(module, "_SOURCE_HOSTS", module._SOURCE_HOSTS | {"a.co"})
    return deployed


def _submit(contract, case_id="case-001", milestone=MILESTONE, first="", second="", days=7):
    return contract.evaluate_delay(case_id, milestone, first, second, days)


def _store(contract, case_id="case-001"):
    contract._commit_case(
        case_id, MILESTONE, EVIDENCE_1, "", 7,
        "NON_EXCUSABLE_DELAY", 0, "MILESTONE_OWNER", "OWNER_CONTROLLED",
        "The documented cause was project-controlled rework.",
    )


@pytest.mark.parametrize("case_id", ["abc", "a" * 64, "a-1", "a_1"])
@pytest.mark.parametrize("days", [1, 30])
def test_valid_bounds_failed_evaluation_without_storage(contract, case_id, days):
    with pytest.raises(Exception, match="EVALUATION_UNAVAILABLE"):
        _submit(contract, case_id, MILESTONE, EVIDENCE_1, EVIDENCE_2, days)
    assert contract.get_case(case_id) == ""


@pytest.mark.parametrize("case_id", ["", "ab", "a" * 65, "Upper", "a.b", "a b", "éab", 123])
def test_bad_ids_rejected(contract, case_id):
    with pytest.raises(Exception, match="INVALID_CASE_ID"):
        _submit(contract, case_id)


@pytest.mark.parametrize("days", [0, 31, True, False, 1.5, "7", None])
def test_bad_days_rejected(contract, days):
    # Floats fail even earlier in the direct runner's production-style
    # calldata encoder; all other values reach the contract guard.
    error = "not calldata encodable" if type(days) is float else "INVALID_REQUESTED_DAYS"
    with pytest.raises(Exception, match=error):
        _submit(contract, days=days)


@pytest.mark.parametrize("url", [
    "", "http://python.org/release", "https://localhost/release",
    "https://127.0.0.1/release", "https://[::1]/release",
    "https://user@python.org/release", "https://python.org/release#part",
    "https://python.org:444/release", "https://python.org:443:/release",
    "https://python.org/release\n", "https://python.org/release\\foo",
    "https://python.org/%zz", "https://python.local/release",
    "https://a/release", "https://-bad.org/release", "https://bad_.org/release",
    "https://python.org/" + "x" * 222,
])
def test_bad_urls_rejected(contract, url):
    with pytest.raises(Exception, match="INVALID_URL"):
        _submit(contract, milestone=url)


def test_url_length_edges_and_optional_urls(contract):
    # 12 ASCII bytes is the shortest valid HTTPS URL under the DNS policy.
    shortest = "https://a.co"
    longest = "https://a.co/" + "x" * (240 - len("https://a.co/"))
    for url in (shortest, longest):
        with pytest.raises(Exception, match="EVALUATION_UNAVAILABLE"):
            _submit(contract, milestone=url)
    with pytest.raises(Exception, match="EVIDENCE_URL_GAP"):
        _submit(contract, second=EVIDENCE_2)
    with pytest.raises(Exception, match="DUPLICATE_URL"):
        _submit(contract, first=MILESTONE)
    with pytest.raises(Exception, match="DUPLICATE_URL"):
        _submit(contract, first="https://WWW.PYTHON.ORG:443/downloads/release/python-3130/")
    with pytest.raises(Exception, match="EVALUATION_UNAVAILABLE"):
        _submit(contract, first=EVIDENCE_1)


def test_missing_case_and_invalid_read_id(contract):
    assert contract.get_case("missing-001") == ""
    with pytest.raises(Exception, match="INVALID_CASE_ID"):
        contract.get_case("bad id")


def test_private_storage_serialization_and_duplicate_protection(contract):
    _store(contract)
    raw = contract.get_case("case-001")
    record = json.loads(raw)
    assert list(record) == [
        "schema_version", "case_id", "milestone_url", "evidence_url_1",
        "evidence_url_2", "requested_days", "verdict", "approved_days",
        "responsible_party", "reason_code", "explanation",
    ]
    assert record["schema_version"] == 1
    assert record["milestone_url"] == MILESTONE
    assert record["approved_days"] == 0
    assert contract.get_case("case-001") == raw
    with pytest.raises(Exception, match="DUPLICATE_CASE_ID"):
        _store(contract)
    with pytest.raises(Exception, match="DUPLICATE_CASE_ID"):
        _submit(contract)
    assert contract.get_case("case-001") == raw


@pytest.mark.parametrize("verdict,approved,party,reason,explanation,error", [
    ("UNKNOWN", 0, "UNKNOWN", "INSUFFICIENT_RECORD", "No record.", "INVALID_DECISION"),
    ("NON_EXCUSABLE_DELAY", 1, "MILESTONE_OWNER", "OWNER_CONTROLLED", "Owner cause.", "INVALID_APPROVED_DAYS"),
    ("EXCUSABLE_DELAY", 8, "EXTERNAL_PARTY", "EXTERNAL_BLOCKER", "Blocker.", "INVALID_APPROVED_DAYS"),
    ("EXCUSABLE_DELAY", 0, "EXTERNAL_PARTY", "EXTERNAL_BLOCKER", "Blocker.", "INVALID_APPROVED_DAYS"),
    ("INSUFFICIENT_EVIDENCE", True, "UNKNOWN", "UNDATED_RECORD", "Undated.", "INVALID_APPROVED_DAYS"),
    ("INSUFFICIENT_EVIDENCE", 0, "UNKNOWN", "UNDATED_RECORD", "", "INVALID_EXPLANATION"),
])
def test_private_result_schema_rejects_bad_records(
    contract, verdict, approved, party, reason, explanation, error,
):
    with pytest.raises(Exception, match=error):
        contract._commit_case(
            "case-001", MILESTONE, "", "", 7,
            verdict, approved, party, reason, explanation,
        )
    assert contract.get_case("case-001") == ""
