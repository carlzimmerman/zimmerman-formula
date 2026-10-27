import argparse,json
from pathlib import Path
from field_exact_self import ExactSelfField
from run_exact_self import ExactSelfSimulation
import checks,active_controls
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--mode',choices=['checks','active'],required=True);a=ap.parse_args()
    if a.mode=='checks':
        checks.Field3D=ExactSelfField
        out=checks.main()
    else:
        active_controls.Simulation=ExactSelfSimulation
        out=active_controls.main()
    Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='seeded_transport'},indent=2))
