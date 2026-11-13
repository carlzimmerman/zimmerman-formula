#!/usr/bin/env python3
"""Probe the historical zero outer boundary against AQUAL's Green boundary.

The finite-box Dirichlet perturbation uses the first-order external-field Green
function. Its nonlinear correction is small at the outer box, not set to zero by
assertion. Two boxes with similar logarithmic resolution are compared later.
"""
import argparse,importlib.util,json,math,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from corrected_core import aqual_asymptote,mu_simple


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rmax',type=float,required=True)
    ap.add_argument('--ns',type=int,required=True)
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args(); lane=Path(__file__).resolve().parent; out=args.output_dir.resolve()
    if lane not in out.parents: raise SystemExit('Output must be inside correction lane')
    out.mkdir(parents=True,exist_ok=True)
    path=lane/'archive/qwen_claude_field_theory/theory_2026/aqual_solver_2026.py'
    spec=importlib.util.spec_from_file_location('frozen_solver',path)
    solver=importlib.util.module_from_spec(spec); spec.loader.exec_module(solver)
    x=brentq(lambda z:aqual_asymptote(z)-60.5,.001,.1,xtol=1e-15)
    mu=float(mu_simple(x)); L=1/(1+x)
    grid=solver.Grid(1e-4,args.rmax,args.ns,128)
    r=grid.r[:,None]; ct=grid.mu_c[None,:]
    ue=-x*r*ct; outer=-1/(mu*grid.r[-1]*np.sqrt(1+L*grid.sin**2))
    u=-1/r*np.ones((grid.ns,grid.nt)); phi=u+ue
    start=time.monotonic()
    for iteration in range(400):
        matrix,rhs=solver.build(grid,solver.MU['mu1'],phi,x)
        target=-(matrix @ ue.ravel()); target[:grid.nt]=rhs[:grid.nt]; target[-grid.nt:]=outer
        updated=solver.spl.spsolve(matrix,target).reshape(grid.ns,grid.nt)
        du=np.max(np.abs(updated-u))/max(1.,np.max(np.abs(updated)))
        u=.45*u+.55*updated; phi=u+ue
        if du<1e-11: break
    weight=grid.sin*grid.dt; weight/=weight.sum()
    mass=grid.r*(np.gradient(u,grid.ds,axis=0,edge_order=2) @ weight)
    interpolator=PchipInterpolator(np.log(grid.r),mass)
    sample=np.array([.5,1.,2.,3.,5.,10.,20.,30.])/x
    vals=interpolator(np.log(sample)); deriv=interpolator.derivative()(np.log(sample))
    result=dict(x_external=x,total_enhancement=60.5,RE_rM=1/x,grid=[args.ns,128],
        rmax=args.rmax,outer_boundary='first-order anisotropic AQUAL Green potential',
        outer_internal_over_external=(1+x)/(args.rmax*x)**2,
        iterations=iteration+1,last_update=float(du),converged=bool(du<1e-11),
        elapsed_seconds=time.monotonic()-start,radii_rM=sample.tolist(),
        mass_ratios=vals.tolist(),d_mass_d_logr=deriv.tolist(),
        non_claims=['No nonlinear positivity theorem','No arbitrary-large-radius numerical guarantee'])
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(out/'profiles.npz',r=grid.r,mratio=mass)
    print(json.dumps(result,indent=2),flush=True)
    if not result['converged']: raise SystemExit(1)


if __name__=='__main__': main()
