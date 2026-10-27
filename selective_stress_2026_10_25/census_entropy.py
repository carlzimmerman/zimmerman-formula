import argparse,json
from pathlib import Path
import virial_entropy as v
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
v.ratio=53.6432722396066
r=v.initial_entropy(1.);out={'state':r,'changed_mass_assumption':'Prior baryon-retention census median53.643 Mb, not original no-loss5.364 Mb; used only as a separate benchmark hypothesis'};Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:x for k,x in r.items() if not isinstance(x,list)},flush=True)
