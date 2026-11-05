#!/usr/bin/env python3
"""Replay selected mixture maxima on common grids and audit finite LP dual."""
import argparse
import json
import math
from pathlib import Path
import sys
import time
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / 'KT34_reciprocal_epsilon_scan/mw'))
import scan as E
M, np = E.M, E.np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    started = time.monotonic()
    scan = json.loads((Path(__file__).parent/'scan_001/results.json').read_text())
    cells = E.population()
    gm = M.gas_mass()
    out = dict(outcome='selected mixture maxima verified conditional on numerical resolution; finite-support LP dual audited', footings={})
    for foot, f in scan['footings'].items():
        best = f['maximizer']; cell = cells[best['index']]
        assert cell == best['cell']
        eps = [best['epsilon_1'], best['epsilon_2']]
        weights = np.array([best['weight_1'], best['weight_2']])
        qs = np.array([r['x_ceiling'] for r in f['cassini']])
        vs = np.array(f['component_max_vc'])
        i, j = [f['widths'].index(e) for e in eps]
        slope = (vs[i]**2-vs[j]**2)/(qs[i]-qs[j])
        intercept = vs[i]**2 - slope*qs[i]
        slack = intercept+slope*qs-vs**2
        assert slope > 0 and min(slack) > -1e-8
        # This is a transparent robustness allowance, not a certified error bar.
        robust_max = 0.
        for a,qa in enumerate(qs):
            if qa<=1: robust_max=max(robust_max,(vs[a]+1)**2)
            for b,qb in enumerate(qs):
                if qa>1 and qb<1:
                    w=(1-qb)/(qa-qb)
                    robust_max=max(robust_max,w*(vs[a]+1)**2+(1-w)*(vs[b]+1)**2)
        row = dict(dual_intercept=intercept, dual_slope=slope,
                   dual_slack_per_width=slack.tolist(),
                   dual_upper_vc=math.sqrt(intercept+slope),
                   max_vc_with_every_component_increased_1_km_s=math.sqrt(robust_max),
                   refinements=[])
        out['footings'][foot]=row
        for refine,lmax,cut in [(2,96,120),(3,128,120),(3,128,600)]:
            g,mu=M.make_grid(M.C.A0[foot],refine,1)
            sol=M.Solver(g,mu,M.C.A0[foot])
            rf,_=M.rho_cell(cell)
            rho=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4)
            pn=sol.LU.newton(rho)
            phis=[]; components=[]; negative=[]; mass_error=[]
            for e in eps:
                sig=E.width(e,E.rm(cell,foot,gm))
                S=sol.get_filter(sig,lmax,cut)
                rx=S.forward(rho)
                ph=sol.phantom(sol.LU.newton(rx))
                phi=pn+S.adjoint(ph)
                phis.append(phi);components.append(sol.evaluate(phi))
                mass=float(np.dot(g.vol,rx))
                negative.append(float(-np.dot(g.vol,np.minimum(rx,0))/mass))
                mass_error.append(abs(mass/np.dot(g.vol,rho)-1))
            mixture=sol.evaluate(sum(w*p for w,p in zip(weights,phis)))
            expected_vc2=sum(w*r['vc']**2 for w,r in zip(weights,components))
            expected_K=sum(w*np.array(r['K']) for w,r in zip(weights,components))
            expected_Ou2=sum(w*np.array(r['vc_Ou'])**2 for w,r in zip(weights,components))
            residuals=dict(vc2=abs(mixture['vc']**2-expected_vc2),
                           K=float(np.max(np.abs(np.array(mixture['K'])-expected_K))),
                           Ou_vc2=float(np.max(np.abs(np.array(mixture['vc_Ou'])**2-expected_Ou2))))
            assert max(negative)<1e-5 and max(mass_error)<1e-10
            assert residuals['vc2']<1e-6 and residuals['K']<1e-7 and residuals['Ou_vc2']<1e-6
            assert not mixture['L1']
            row['refinements'].append(dict(refine=refine,lmax=lmax,cut=cut,negative_mass_fractions=negative,
                mass_relative_errors=mass_error,affine_residuals=residuals,components=components,mixture=mixture))
            print(foot,refine,lmax,cut,'vc',mixture['vc'],'affine',residuals,flush=True)
    out['runtime_seconds']=time.monotonic()-started
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')


if __name__ == '__main__':
    main()
