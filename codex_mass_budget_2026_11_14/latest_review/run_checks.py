#!/usr/bin/env python3
"""Reproduce the bounded audit in a new directory: python3 -B run_checks.py run_006."""
import json
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
name=sys.argv[1]
if not name.startswith("run_") or "/" in name or "\\" in name:
    raise SystemExit("Use a new simple run_NNN name")
base=str(HERE.relative_to(ROOT))
skill=Path.home()/".codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit"
contract=json.loads((HERE/"contract.json").read_text())
argv=[sys.executable,str(skill/"scripts/run_experiment.py"),"--root",str(ROOT),
      "--contract",str(HERE/"contract.json"),"--output",f"{base}/{name}",
      "--result",f"{base}/{name}/junction_checks.json","--timeout","120",
      "--max-output-bytes","1048576","--max-cpu-seconds","110","--max-threads","1"]
for path in contract["execution_artifacts"]:
    argv += ["--input",path]
argv += ["--",sys.executable,"-B",f"{base}/check_junction.py",f"{base}/{name}/junction_checks.json"]
raise SystemExit(subprocess.run(argv,cwd=ROOT).returncode)
