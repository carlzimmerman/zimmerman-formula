#!/usr/bin/env python3
"""Independent literal-source refinements of frozen universal-length witnesses."""
import argparse
import json
import sys
import time
from pathlib import Path
sys.dont_write_bytecode = True
import search as U
M, E, np = U.M, U.E, U.np


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True)
    args=p.parse_args(); start=time.monotonic()
    selected={'canonical':1374,'alt':1227}; cells=E.population()
    out=dict(width_kpc=3., selected=selected, coverage='Two frozen witnesses; not a complete refined population scan',footings={})
    for foot,idx in selected.items():
        f=dict(cell=cells[idx],cases=[]); out['footings'][foot]=f
        for refine,cut,outer in [(2,120,1),(3,120,1),(4,120,1),(5,120,1),(3,240,1),(3,120,2)]:
            g,mu=M.make_grid(M.C.A0[foot],refine,outer)
            sol=M.Solver(g,mu,M.C.A0[foot])
            row=sol.solve(cells[idx],3.,192,cut)
            rf,_=M.rho_cell(cells[idx]); rho=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4)
            S=sol.get_filter(3.,192,cut); rx=S.forward(rho)
            mass=float(np.dot(g.vol,rx)); neg=float(-np.dot(g.vol,np.minimum(rx,0))/mass)
            err=abs(mass/np.dot(g.vol,rho)-1)
            rec=M.C.lines(row['corrected']['vc'],row['corrected']['K'],row['corrected']['K0'],row['corrected']['vc_Ou'])
            assert all(row['corrected'][k]==rec[k] for k in (*M.GATE,'Lh'))
            assert neg<1e-5 and err<1e-10
            record=dict(refine=refine,lmax=192,cut=cut,outer_factor=outer,
                        nr=g.Nr,nt=g.Nt,negative_mass_fraction=neg,mass_relative_error=err,row=row)
            if refine==3 and cut==120 and outer==1:
                record['invariants']=M.invariant_checks(sol,sigma=3.,lmax=192,cut=120)
                q=record['invariants']
                assert q['adjoint_relative']<1e-12 and q['source_mass_relative']<1e-12
                assert q['outer_constant_error']<1e-12 and q['laplacian_weighted_symmetry_relative']<1e-12
                assert min(x['relative'] for x in q['reciprocity'])<1e-6
            f['cases'].append(record)
            print(foot,refine,cut,outer,{k:row['corrected'][k] for k in ('vc','K0','cO','cK','h','all_four')},flush=True)
            Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
        f['all_refinements_pass']=all(x['row']['corrected']['all_four'] for x in f['cases'])
    out['runtime_seconds']=time.monotonic()-start
    out['passed']=all(f['all_refinements_pass'] for f in out['footings'].values())
    Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))


if __name__=='__main__':main()
