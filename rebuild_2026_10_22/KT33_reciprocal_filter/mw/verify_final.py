#!/usr/bin/env python3
"""Resolve diagnosed numerical defects; preserve first failed validation run.

Final representation uses lmax48 on doubled spatial grid. The arbitrary gauge
test is scored at observed radii (4--30kpc); all-grid cancellation is reported
against its floating-point differentiation bound, not a radius-independent
absolute tolerance. No mass density is clipped.
"""
import argparse
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import mw_reciprocal as M
import verify_refinement as V
import numpy as np


def gauge_check(sol,c,sigma,lmax,cut):
    g=sol.g;S=sol.get_filter(sigma,lmax,cut)
    rf,_=M.rho_cell(c);rho=g.rho_axisym(lambda R,z:rf(R,z)/sol.mu,nq=4)
    ph=sol.phantom(sol.LU.newton(S.forward(rho)))
    p=S.adjoint(ph);pc=S.adjoint(ph+12345.)
    dr,dt=g.grad_cells(p);er,et=g.grad_cells(pc)
    m=(g.r2d>=4)&(g.r2d<=30)
    error=np.maximum(np.abs(er-dr),np.abs(et-dt))
    norm=np.maximum(np.asarray(abs(g.Crr).sum(axis=1)).ravel(),np.asarray(abs(g.Cth).sum(axis=1)).ravel())
    # Conservative 128-operation floating bound: contraction, normalization,
    # subtraction and sparse differentiation, for a fixed known gauge offset.
    bound=128*np.finfo(float).eps*(12345.+np.max(np.abs(ph)))*norm
    return dict(observed_radii_max_error=float(error[m].max()),all_grid_max_error=float(error.max()),all_grid_max_error_over_roundoff_bound=float(np.max(error/np.maximum(bound,1e-300))),outer_constant_max_error=float(np.max(np.abs(S.adjoint(np.ones(g.n))-1))))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    base=json.loads((M.HERE/'grid_run/results.json').read_text());saved=json.loads((M.HERE/'saved_run/results.json').read_text())
    out={'resolution':'doubled spatial grid, even l through48, cut120kpc; selected x3/l64 controls','failed_preliminary_validation_preserved':'refinement_run/manifest.json','thresholds':dict(negative_mass_fraction=1e-5,anisotropic_gaussian_relative_peak=.001,analytic_reciprocity=1e-8,gauge_observed_absolute=1e-8,gauge_roundoff_ratio=1.),'footings':{},'failures':[]}
    for foot,b in base['footings'].items():
        rows=b['rows'];old=saved['footings'][foot]['rows'][0]['cell'];best=b['summary']['corrected']['best']['cell']
        lo=min(rows,key=lambda r:r['xi'])['cell'];hi=max(rows,key=lambda r:r['xi'])['cell']
        targets=[('best_original',old),('best_corrected',best),('minimum_xi',lo),('maximum_xi',hi)]
        records=[]
        for name,nr,nt,ell,cut in [('final2',2,2,48,120),('fine3',3,3,64,180)]:
            g,mu=V.custom_grid(M.C.A0[foot],nr,nt,1);sol=M.Solver(g,mu,M.C.A0[foot])
            for label,c in targets if name=='final2' else targets[:2]:
                sigma=M.width(c,foot);x=V.extended_checks(sol,c,sigma,ell,cut);gauge=gauge_check(sol,c,sigma,ell,cut);scores=sol.solve(c,sigma,ell,cut,plain=True)
                for key,lim in [('negative_density_mass_fraction',1e-5),('gaussian_l2_relative_peak',.001)]:
                    if x[key]>lim:out['failures'].append(foot+':'+name+':'+label+':'+key)
                if x['reciprocity_analytic']['relative']>1e-8:out['failures'].append(foot+': analytic reciprocity')
                if gauge['observed_radii_max_error']>1e-8 or gauge['all_grid_max_error_over_roundoff_bound']>1:out['failures'].append(foot+': gauge')
                records.append(dict(variant=name,candidate=label,scores=scores,checks=x,gauge=gauge));print(foot,name,label,x,gauge,flush=True)
            if name=='final2':
                # Extend the same radial lattice, retaining EVERY existing inner
                # cell; regenerating log_edges would confound domain and spacing.
                ratio=g.re[-1]/g.re[-2];n=int(np.ceil(np.log(2)/np.log(ratio)))
                re=np.r_[g.re,g.re[-1]*ratio**np.arange(1,n+1)]
                gx=M.C.PS.Grid(re,g.te);sx=M.Solver(gx,mu,M.C.A0[foot]);sigma=M.width(best,foot)
                records.append(dict(variant='same_lattice_domain2',candidate='best_corrected',scores=sx.solve(best,sigma,ell,cut,plain=True)))
        out['footings'][foot]=records
    out['passed']=not out['failures'];Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False));print('FAILURES',out['failures'],flush=True)
    raise SystemExit(0 if out['passed'] else 1)


if __name__=='__main__':main()
