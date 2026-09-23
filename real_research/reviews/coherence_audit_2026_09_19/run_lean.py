"""Run both bounded certificates using the repository's documented Lean host."""
from pathlib import Path
import subprocess

here=Path(__file__).resolve().parent
root=here.parents[2]
host=root/'fable_independent_2026/lean_2026'
subprocess.run(['lake','env','lean','--version'],cwd=host,check=True)
for name in ('ClockAndBridge.lean','EquilibriumReview.lean'):
    print('Checking',name,flush=True)
    subprocess.run(['lake','env','lean',str(here/name)],cwd=host,check=True)
