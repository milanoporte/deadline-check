"""Offline Phase 1 contract gate using the cached pinned GenVM SDK."""
import ast
import json
import os
import py_compile
import tabnanny
import typing
from pathlib import Path

from gltest.direct import sdk_loader
from gltest.direct.loader import load_contract_class
from gltest.direct.vm import VMContext

root = Path(__file__).resolve().parents[1]
os.chdir(root)
sdk_loader.CACHE_DIR = root / ".genvm-cache"
sdk_loader.BUNDLE_CACHE_DIR = sdk_loader.CACHE_DIR / "bundles-v2"
sdk_loader.TREE_CACHE_DIR = sdk_loader.CACHE_DIR / "trees-v2"
os.environ["GENVM_VERSION"] = "v0.6.0-rc3"
for path in (root / "contracts/DeadlineCheck.py", *sorted((root / "tests").glob("*.py")), Path(__file__)):
    py_compile.compile(str(path), doraise=True)
    tabnanny.check(str(path))
print("Compilation and standard-library whitespace lint: PASS")
with VMContext().activate() as vm:
    contract = load_contract_class(root / "contracts/DeadlineCheck.py", vm)
    import genlayer as gl
    from genlayer._internal.get_schema import get_schema
    schema = get_schema(contract)
    assert set(schema["methods"]) == {"evaluate_delay", "get_case"}
    write = schema["methods"]["evaluate_delay"]
    assert write["params"] == [["case_id", "string"], ["milestone_url", "string"],
                               ["evidence_url_1", "string"], ["evidence_url_2", "string"],
                               ["requested_days", "int"]]
    assert write["ret"] == "null" and write["readonly"] is False
    read = schema["methods"]["get_case"]
    assert read["params"] == [["case_id", "string"]]
    assert read["ret"] == "string" and read["readonly"] is True
    assert schema["ctor"]["params"] == []
    storage = typing.get_type_hints(contract)["cases"]
    assert typing.get_origin(storage) is gl.storage.TreeMap
    assert typing.get_args(storage) == (str, str)
    tree = ast.parse((root / "contracts/DeadlineCheck.py").read_text())
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "evaluate_delay")
    for closure in (n for n in method.body if isinstance(n, ast.FunctionDef)):
        assert not any(isinstance(n, ast.Name) and n.id == "self" for n in ast.walk(closure))
    assert hasattr(gl.vm, "run_nondet") and hasattr(gl.vm, "Return")
    assert hasattr(gl.nondet.web, "Response")
    print("Pinned SDK ABI/storage/closure semantic checks: PASS")
    print(json.dumps(schema, indent=2))
