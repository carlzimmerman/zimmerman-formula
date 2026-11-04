"""Declared joint-search continuation after canonical MW missed vc by 0.41 km/s."""
import argparse
import json
from pathlib import Path
from response import Response,finite_admissibility
from cassini_response import physical


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    rows=[];responses=[]
    for power in [5,6,7]:
        for scale in [1.52,1.55,1.6,1.65,1.7]:
            response=Response('cutoff',scale=scale,power=power);adm=finite_admissibility(response)
            responses.append(dict(response.metadata,admissibility=adm))
            if not adm['passed']:
                print(response.name,'REJECT',adm['minimum_total_slope'],flush=True);continue
            for epsilon in [.18,.20,.22,.25,.28,.30]:
                for foot in ['canonical','alt']:
                    row=physical(response,foot,epsilon,nr=4000,nm=160)
                    row['response']=response.metadata;rows.append(row)
            good=[r for r in rows if r['response']['name']==response.name and r['cassini_pass']]
            print(response.name,[(r['footing'],r['epsilon'],round(r['x_ceiling'],7)) for r in good],flush=True)
    out=dict(assertion_tested='Bounded constitutive scale/exponent continuation prompted by simultaneous MW screen',
             rows=rows,responses=responses,settings=dict(nr=4000,nm=160,rmin=1e-7,rmax=1e5),
             non_claims=['No MW pass','No global parameter optimization or exhaustive intervals','Exploratory quadrature needs refinement'])
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
