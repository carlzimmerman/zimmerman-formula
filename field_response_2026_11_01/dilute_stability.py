#!/usr/bin/env python3
"""Three frozen dilute controls using unchanged reviewed calculations."""
import importlib.util
import json
import resource
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent


def load(name):
    s=importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m


def main():
    out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
    r=load('radial_stability_v2');k=load('kinetic_screen_v2')
    src=r.source_module();result={'assertion_tested':'Three dilute-state controls at fixed epsilon .01, no state fitting.','cases':[]}
    try:
        for pc in [.2,.4,.6]:
            fluid,_=r.run_case(pc,.01,src);kinetic=k.one_case(r,pc,.01)
            result['cases'].append({'psi_c':pc,'epsilon':.01,'fluid':fluid,'kinetic':kinetic})
            print(pc,fluid['verdict'],kinetic['verdict'],flush=True)
        result['all_controls_pass']=all(all(x['fluid']['checks'].values()) and x['kinetic']['controls_pass'] for x in result['cases'])
    except Exception as exc:
        import traceback
        result['exception']=repr(exc);result['traceback']=traceback.format_exc();result['all_controls_pass']=False
    result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out.write_text(json.dumps(result,indent=2,allow_nan=False,default=r.json_default)+'\n')
    return 0 if result['all_controls_pass'] else 1


if __name__=='__main__':sys.exit(main())
