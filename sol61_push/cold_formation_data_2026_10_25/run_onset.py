"""Explicit finite sequential v4 onset batch. No background monitor."""
import subprocess,json
from pathlib import Path
P=Path(__file__).resolve().parent
for gal in ['Draco','Sextans','Fornax','LeoI']:
 for res in ['base','fine']:
  case=gal+'_'+res+'_v4';rc=subprocess.call(['/opt/homebrew/bin/python3',str(P/'run_registered.py'),case]);print(case,'exit',rc,flush=True)
  if rc:raise SystemExit(rc)
  d=json.loads((P/case/'result.json').read_text());print(json.dumps({k:d[k] for k in ['galaxy','status','t','seconds','stellar_numerics_valid','maxima']}),flush=True)
