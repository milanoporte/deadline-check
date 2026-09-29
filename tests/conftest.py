"""Keep direct GenVM artifacts pinned and cached only inside this project."""

import os
from pathlib import Path

from gltest.direct import sdk_loader


_ROOT = Path(__file__).resolve().parents[1]
sdk_loader.CACHE_DIR = _ROOT / ".genvm-cache"
sdk_loader.BUNDLE_CACHE_DIR = sdk_loader.CACHE_DIR / "bundles-v2"
sdk_loader.TREE_CACHE_DIR = sdk_loader.CACHE_DIR / "trees-v2"
os.environ["GENVM_VERSION"] = "v0.6.0-rc3"
