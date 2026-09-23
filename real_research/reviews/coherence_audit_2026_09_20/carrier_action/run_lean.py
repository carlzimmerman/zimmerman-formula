"""Run the new exact obligations using the repository's pinned Lean project."""
from pathlib import Path
import json
import subprocess
import sys

root=Path(__file__).resolve().parents[4]
target=Path(__file__).with_name('CarrierIdentities.lean').resolve()
proc=subprocess.run(['/opt/homebrew/bin/lake','env','lean',str(target)],
                    cwd=root/'fable_independent_2026/lean_2026',
                    text=True,capture_output=True,timeout=90)
print(proc.stdout,end='')
print(proc.stderr,end='',file=sys.stderr)
Path(sys.argv[1]).write_text(json.dumps({'exit_code':proc.returncode,
    'stdout':proc.stdout,'stderr':proc.stderr,
    'scope':'Nine exact lemmas, including parameterized derivative composition; no PDE or metric-variation formalization.'},indent=2)+'\n')
sys.exit(proc.returncode)
