"""Finite explicit batch; sequential one-shot bounded runs."""
import subprocess,sys,json
from pathlib import Path
P=Path(__file__).resolve().parent
for case in ['Sextans_fine_v2','Fornax_base_v2','Fornax_fine_v2','LeoI_base_v2','LeoI_fine_v2']:
 rc=subprocess.call(['/opt/homebrew/bin/python3',str(P/'run_registered.py'),case]);print(case,'exit',rc,flush=True)
 if rc:raise SystemExit(rc)
 d=json.loads((P/case/'result.json').read_text());print(json.dumps({k:d[k] for k in ['galaxy','status','t','seconds','stellar_numerics_valid','maxima']}),flush=True)
