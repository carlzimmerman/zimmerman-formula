#!/usr/bin/env python3
"""Literal potential vs dual-force controls for the new constitutive MW solver."""
import argparse,json,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import constitutive as C
M,E,np=C.M,C.E,C.np
HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    start=time.monotonic();cells=E.population();gm=M.gas_mass()
    datasets=[json.loads((HERE/x/'results.json').read_text()) for x in ('constitutive_grid_001','constitutive_continuation_001')]
    out=dict(cases=[],invariants={},simple_controls={})
    for foot,a0 in M.C.A0.items():
        g,mu=M.make_grid(a0,2,1);sol=C.Solver(g,mu,a0,C.Response('simple'))
        baseline=M.Solver(g,mu,a0)
        # Same literal density and same operator; altered constitutive plumbing
        # must reproduce the pre-existing simple response.
        old=baseline.solve(cells[1350],3.,128,120)['corrected']
        new=sol.solve(cells[1350],3.,128,120)['corrected']
        error=max(abs(old[k]-new[k]) for k in ('vc','K0','cK','cO','h'))
        assert error<1e-7;out['simple_controls'][foot]=error
        for data in datasets:
            for case in data['cases']:
                if case['footing']!=foot:continue
                d=case['response'];sol.response=C.Response(d['family'],scale=d['scale'],power=d['power'])
                idx=int(np.argmax(case['all_vc']));sig=E.width(case['epsilon'],E.rm(cells[idx],foot,gm))
                q=sol.solve(cells[idx],sig,128,120)['corrected'];err=abs(q['vc']-case['all_vc'][idx])
                assert err<1e-7
                out['cases'].append(dict(footing=foot,epsilon=case['epsilon'],response=d,index=idx,
                                         literal_scores=q,dual_vc=case['all_vc'][idx],difference=err))
        sol.response=C.Response('cutoff',scale=1.5,power=6)
        inv=M.invariant_checks(sol,sigma=3.,lmax=128,cut=120)
        assert min(x['relative'] for x in inv['reciprocity'])<1e-6
        assert inv['nu_one_phantom_max']==0 and inv['xi_zero_identity_error']==0
        out['invariants'][foot]=inv
        print(foot,'controls passed',flush=True)
    out['passed']=True;out['runtime_seconds']=time.monotonic()-start
    Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False))


if __name__=='__main__':main()
