"""Bounded declared response/Cassini screen; output selection is not a MW pass."""
import argparse
import json
from pathlib import Path
import numpy as np
from response import candidates, finite_admissibility
from cassini_response import physical


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args(); rows=[]; responses=[]
    for response in candidates():
        adm=finite_admissibility(response)
        meta=dict(response.metadata,admissibility=adm,nu_samples={str(y):float(response.nu(y)) for y in [.1,.3,1,2,3,5,10]})
        responses.append(meta)
        if not adm['passed']:
            print(response.name,'REJECT nonmonotone total response',adm['minimum_total_slope'],flush=True)
            continue
        for epsilon in [.15,.25,.30,.40,.50]:
            for foot in ['canonical','alt']:
                row=physical(response,foot,epsilon)
                row.update(response=response.metadata)
                rows.append(row)
        for foot in ['canonical','alt']:
            good=[r for r in rows if r['response']['name']==response.name and r['footing']==foot and r['cassini_pass']]
            print(response.name,foot,'passing epsilon',[r['epsilon'] for r in good],
                  'ratios',[round(r['x_ceiling'],5) for r in good],flush=True)
    disagreements=[abs(r['flux_density_difference']) for r in rows]
    out=dict(assertion_tested='Finite declared constitutive family and corrected equal-Gaussian Cassini screen; no MW score',
             settings=dict(nr=3000,nm=80,rmin=1e-7,rmax=1e5),responses=responses,rows=rows,
             max_flux_density_absolute_q_difference=max(disagreements),
             qualification='Exploratory screen; each observational survivor requires quadrature refinement and joint MW result')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print('rows',len(rows),'max flux-density difference',max(disagreements),flush=True)


if __name__=='__main__': main()
