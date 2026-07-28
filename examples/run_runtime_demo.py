from __future__ import annotations

import json

from cogsys.runtime.demo import run_demo

print(json.dumps(run_demo(), indent=2))
