"""Declared refinement of the first-screen candidates, plus invariants."""
import argparse
import json
from pathlib import Path
import numpy as np
from response import Response
from cassini_response import physical,quadrupole,baseline


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    selected=[(Response('simple'),.5)]
    selected += [(Response('cutoff',scale=1.5,power=6),e) for e in [.15,.25,.30,.40,.50]]
    selected += [(Response('cutoff',scale=1.5,power=4),.25),(Response('rational',scale=1.5,power=6),.5)]
    presets=[('medium',dict(nr=10000,nm=200)),('fine',dict(nr=20000,nm=400)),
             ('expanded',dict(nr=20000,nm=400,rmin=1e-8,rmax=1e6))]
    rows=[];checks={}
    for response,e in selected:
        for foot in baseline.A0:
            series={name:physical(response,foot,e,**opts) for name,opts in presets}
            ref=series['expanded'];key=f'{response.name}|{foot}|{e}'
            spread=max(abs(row['x_ceiling']-ref['x_ceiling']) for row in series.values())
            diff=max(abs(row['flux_density_difference']) for row in series.values())
            checks[key]=dict(passed=bool(spread<2e-4 and diff<2e-6),maximum_absolute_ceiling_spread=spread,
                             maximum_absolute_q_flux_density_difference=diff,
                             tolerance_ceiling=2e-4,tolerance_q=2e-6)
            rows.append(dict(response=response.metadata,footing=foot,epsilon=e,series=series))
            print(key,'ratio',ref['x_ceiling'],'signed q',ref['q_hessian_signed'],'spread',spread,'qdiff',diff,flush=True)
    newton=quadrupole(Response('newtonian'),baseline.GEXT/baseline.A0['canonical'],.3,nr=1000,nm=40)
    checks['newtonian_exact_zero']=dict(passed=newton['q_hessian_signed']==newton['q_density_signed']==0.)
    plain=quadrupole(Response('simple'),baseline.GEXT/baseline.A0['canonical'],0,nr=10000,nm=200)
    old=baseline.quadrupole(baseline.GEXT/baseline.A0['canonical'],0,0,nr=10000,nm=200)
    checks['plain_qumond_control']=dict(passed=abs(plain['q_hessian_signed']-old['q_hessian_signed'])<1e-12,
                                       absolute_q_difference=abs(plain['q_hessian_signed']-old['q_hessian_signed']))
    checks['simple_KT33_control']=dict(passed=abs(rows[0]['series']['expanded']['x_ceiling']-1.09159062581)<1e-8)
    out=dict(rows=rows,checks=checks,all_checks_pass=all(r['passed'] for r in checks.values()),
             outcome='Conditional on numerical tolerance; response and epsilon are exploratory model parameters, not fitted baryons')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    if not out['all_checks_pass']: raise SystemExit(1)


if __name__=='__main__':main()
