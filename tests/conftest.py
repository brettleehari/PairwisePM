"""Pytest path setup: make the repo root importable so `import pairwisepm`
works no matter where pytest is invoked from. No fixtures beyond that — the
suite runs against the real package, no mocks of the engine (compliance rule).
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
