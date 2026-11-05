"""Exact rounded final MW candidates: both unchanged Solar footings."""
import argparse,json
from pathlib import Path
from response import Response,finite_admissibility
from cassini_response import physical


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    selected=[(1.587,6.3,.24),(1.5815,6.3,.25),(1.564,6.2,.26),(1.543,6.1,.27)]
    rows=[];checks={};admissibility={}
    for t,power,e in selected:
        response=Response('cutoff',scale=t,power=power);adm=finite_admissibility(response)
        admissibility[response.name]=adm
        for foot in ['canonical','alt']:
            series={name:physical(response,foot,e,**opts) for name,opts in [
                ('medium',dict(nr=20000,nm=400)),('fine',dict(nr=40000,nm=800)),
                ('expanded',dict(nr=40000,nm=800,rmin=1e-8,rmax=1e6))]}
            ref=series['expanded'];spread=max(abs(r['x_ceiling']-ref['x_ceiling']) for r in series.values())
            diff=max(abs(r['flux_density_difference']) for r in series.values())
            key=f'{response.name}|{foot}|{e}'
            checks[key]=dict(passed=spread<2e-4 and diff<2e-6 and adm['passed'],
                             maximum_absolute_ceiling_spread=spread,maximum_absolute_q_flux_density_difference=diff,
                             tolerance_ceiling=2e-4,tolerance_q=2e-6)
            rows.append(dict(response=response.metadata,epsilon=e,footing=foot,series=series))
            print(key,'ratio',ref['x_ceiling'],'spread',spread,'qdiff',diff,flush=True)
    out=dict(rows=rows,checks=checks,admissibility=admissibility,all_checks_pass=all(x['passed'] for x in checks.values()),
             qualification='Observational pass labels use unchanged Cassini ceiling; no MW claim. p6.3 has separate exact global monotonicity certificate; other exponents have finite admissibility checks.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
