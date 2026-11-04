"""Refine all six p6 canonical survivors of the declared continuation."""
import argparse,json
from pathlib import Path
from response import Response
from cassini_response import physical


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    selected=[(1.52,e) for e in [.20,.22,.25,.28]]+[(1.55,e) for e in [.22,.25]]
    rows=[];checks={}
    for t,e in selected:
        response=Response('cutoff',scale=t,power=6)
        series={name:physical(response,'canonical',e,**opts) for name,opts in [
            ('medium',dict(nr=20000,nm=400)),('fine',dict(nr=40000,nm=800)),
            ('expanded',dict(nr=40000,nm=800,rmin=1e-8,rmax=1e6))]}
        ref=series['expanded'];spread=max(abs(r['x_ceiling']-ref['x_ceiling']) for r in series.values())
        diff=max(abs(r['flux_density_difference']) for r in series.values())
        key=f'{response.name}|canonical|{e}'
        checks[key]=dict(passed=spread<2e-4 and diff<2e-6,maximum_absolute_ceiling_spread=spread,
                         maximum_absolute_q_flux_density_difference=diff)
        rows.append(dict(response=response.metadata,epsilon=e,footing='canonical',series=series))
        print(key,ref['x_ceiling'],'spread',spread,'qdiff',diff,flush=True)
    out=dict(rows=rows,checks=checks,all_checks_pass=all(x['passed'] for x in checks.values()))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    if not out['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
