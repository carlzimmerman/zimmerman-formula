#!/usr/bin/env python3
"""Bounded single-grid AQUAL solve at a correctly matched external field.

Run separately at two resolutions; preserve every result in a fresh directory.
The baryons are the historical point source Mb=6.681e10 Msun, on both footings.
This does not reproduce a full disk+bulge Jeans likelihood or choose a completion.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
sys.dont_write_bytecode=True
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from corrected_core import (G, MSUN, KPC, MB_MSUN, A0, Y_EXTERNAL,
                            physical_external_from_newtonian, aqual_asymptote,
                            qumond_monopole, qumond_asymptote)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ns',type=int,required=True)
    ap.add_argument('--nt',type=int,required=True)
    ap.add_argument('--itmax',type=int,default=400)
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args()
    lane=Path(__file__).resolve().parent
    out=args.output_dir.resolve()
    if lane not in out.parents: raise SystemExit('Output must be a child of correction lane')
    out.mkdir(parents=True,exist_ok=True)
    frozen=lane/'archive/qwen_claude_field_theory/theory_2026/aqual_solver_2026.py'
    spec=importlib.util.spec_from_file_location('frozen_aqual_solver',frozen)
    solver=importlib.util.module_from_spec(spec); spec.loader.exec_module(solver)
    grid=solver.Grid(1e-4,1e4,args.ns,args.nt)
    x=physical_external_from_newtonian(Y_EXTERNAL)
    print(json.dumps(dict(grid=[args.ns,args.nt],y_newtonian=Y_EXTERNAL,x_physical=x,
                          kernel='simple mu',aqual_analytic=aqual_asymptote(x))),flush=True)
    start=time.monotonic()
    u,phi,it,du=solver.solve(grid,solver.MU['mu1'],x,tol=1e-11,itmax=args.itmax,relax=.55,verbose=True)
    elapsed=time.monotonic()-start
    # Log-radius derivative; interpolate mass at fixed radii, never nearest bins.
    duds=np.gradient(u,grid.ds,axis=0,edge_order=2)
    dphids=np.gradient(phi,grid.ds,axis=0,edge_order=2)
    weights=grid.sin*grid.dt; weights/=weights.sum()
    mratio=grid.r*(duds @ weights)
    gradmag=solver.grads(grid,phi)
    flux=grid.r**2*((solver.MU['mu1'](gradmag)*dphids/grid.r[:,None]) @ weights)
    # Independent nonlinear residual after the final iteration, on actual final phi.
    matrix,rhs=solver.build(grid,solver.MU['mu1'],phi,x)
    ue=-x*grid.r[:,None]*grid.mu_c[None,:]
    actual_rhs=-(matrix @ ue.ravel())
    actual_rhs[:args.nt]=rhs[:args.nt]; actual_rhs[-args.nt:]=0
    residual=(matrix @ u.ravel()-actual_rhs).reshape(args.ns,args.nt)
    scale=(np.abs(matrix) @ np.abs(u.ravel())+np.abs(actual_rhs)).reshape(args.ns,args.nt)
    interior=(grid.r>1)&(grid.r<100)
    scaled_resid=float(np.max(np.abs(residual[interior])/np.maximum(scale[interior],1e-30)))
    flux_error=float(np.max(np.abs(flux[interior]-1)))
    interp=PchipInterpolator(np.log(grid.r),mratio)
    radial_kpc=[20.,40.,60.,80.,100.,150.,200.,300.]
    physical={}
    H0=67.4e3/(1000*KPC)
    rho_critical=3*H0**2/(8*math.pi*G)
    for footing,a0 in A0.items():
        rM=math.sqrt(G*MB_MSUN*MSUN/a0)/KPC
        radii=np.asarray(radial_kpc)/rM
        aqual=np.asarray(interp(np.log(radii)))*MB_MSUN
        qumond=qumond_monopole(radii,Y_EXTERNAL,order=512)*MB_MSUN
        q1024=qumond_monopole(radii,Y_EXTERNAL,order=1024)*MB_MSUN
        # Operational effective-M200c: spherical monopole density crossing.
        # This is NOT a direct measurement and is not a cold-rest-mass definition.
        def crossing(rkpc):
            mass=float(interp(math.log(rkpc/rM)))*MB_MSUN*MSUN
            return mass/(4*math.pi/3*(rkpc*KPC)**3)/(200*rho_critical)-1
        r200=brentq(crossing,50.,500.,xtol=1e-9)
        m200=float(interp(math.log(r200/rM)))*MB_MSUN
        physical[footing]=dict(rM_kpc=rM,radii_kpc=radial_kpc,
            aqual_effective_mass_msun=aqual.tolist(),qumond_effective_mass_msun=qumond.tolist(),
            qumond_quadrature_max_rel=float(np.max(np.abs(q1024/qumond-1))),
            M80_direct_comparison=dict(model_msun=float(aqual[3]),observed_msun=6.36e11,
                observed_sigma_msun=.50e11,conditional_pull=float((aqual[3]-6.36e11)/(.50e11)),
                caveat='Fixed point-baryon proxy, no baryonic/model/covariance systematics included'),
            effective_overdensity=dict(r200c_kpc=r200,M200c_effective_msun=m200,H0_km_s_Mpc=67.4,
                crossing_residual=crossing(r200),comparison_to_NFW_extrapolation=None,
                interpretation='Operational spherical-monopole overdensity, not independent observed halo mass'))
    sample=np.array([10.,20.,50.,100.,300.,600.])
    plateau=np.asarray(interp(np.log(sample)))
    result=dict(grid=dict(ns=args.ns,nt=args.nt,rmin=1e-4,rmax=1e4),
        y_external_newtonian=Y_EXTERNAL,x_external_physical=x,kernel='mu=x/(1+x)',
        baryons='point mass 6.681e10 Msun',iterations=it+1,iteration_limit=args.itmax,
        last_relative_update=float(du),update_tolerance=1e-11,update_converged=bool(du<1e-11),
        elapsed_seconds=elapsed,nonlinear_residual_max_scaled_r1_100=scaled_resid,
        gauss_flux_max_rel_error_r1_100=flux_error,physical=physical,
        far_field=dict(radii_rM=sample.tolist(),numerical_mass_ratios=plateau.tolist(),
            aqual_analytic=aqual_asymptote(x),qumond_analytic=qumond_asymptote(Y_EXTERNAL)),
        scope='Finite-grid conditional point-source calculation; independent completion derivation absent',
        non_claims=['No density-slope test','No full Milky Way baryon model','No calibrated M200c exclusion',
                    'No universal modified-inertia result','No theory closure'])
    np.savez_compressed(out/'profiles.npz',r=grid.r,mratio=mratio,gauss_flux=flux,u=u,phi=phi)
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    # A scientifically failed convergence flag remains available in the record.
    if not result['update_converged'] or not np.isfinite(mratio).all(): raise SystemExit(1)


if __name__=='__main__': main()
