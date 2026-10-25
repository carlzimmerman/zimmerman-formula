import argparse,json
from pathlib import Path
from kinetic import Kinetic,PROFILES
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out={'screen_threshold':1/3,'rows':[]}
    for p in range(4):
        _,mass,b,_=PROFILES[p]
        for f in (0.,.95):
            s=Kinetic(mass,b,f=f);s.cross_section*=100;v=s.snapshot(0)['max_cell_width_over_mfp']
            out['rows'].append(dict(profile_index=p,f=f,opacity_proxy=v,initial_screen_pass=bool(v<=1/3)))
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
