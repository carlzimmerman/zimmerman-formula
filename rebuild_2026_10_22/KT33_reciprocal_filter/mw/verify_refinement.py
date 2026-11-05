#!/usr/bin/env python3
"""Gated independent checks and refinement of unchanged best candidate cells."""
import argparse
import json
import math
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import mw_reciprocal as M
import numpy as np


def extended_checks(sol,c,sigma,lmax=24,cut=120):
    g=sol.g;w=g.vol;S=sol.get_filter(sigma,lmax,cut)
    r,t=g.r2d,g.t2d
    dot=lambda a,b:float(np.dot(w*a,b))
    # Anisotropic solid harmonic times a Gaussian has a closed convolution.
    a=6.;v=a*a+sigma*sigma
    p2=.5*(3*np.cos(t)**2-1)
    f=r*r*p2*np.exp(-r*r/(2*a*a))
    exact=(a*a/v)**3.5*r*r*p2*np.exp(-r*r/(2*v))
    m=r<30
    l2=float(np.max(np.abs(S.forward(f)[m]-exact[m]))/np.max(np.abs(exact[m])))
    rho0=.05*np.exp(-r*r/100)*(1+.3*np.cos(2*t))
    u=np.exp(-r*r/40)*np.cos(2*t);v0=np.exp(-r*r/120)*np.cos(4*t)
    u-=np.exp(-r*r/40)*dot(u,np.ones(g.n))/dot(np.exp(-r*r/40),np.ones(g.n))
    v0-=np.exp(-r*r/120)*dot(v0,np.ones(g.n))/dot(np.exp(-r*r/120),np.ones(g.n))
    p=sol.LU.newton(S.forward(rho0));ur,ut=g.grad_cells(p)
    q=np.hypot(ur,ut);q=np.maximum(q,1e-100)
    nu=M.C.nu(q);dn=-.5/(q*q*np.sqrt(.25+1/q))
    def J(h):
        ph=sol.LU.newton(S.forward(h));vr,vt=g.grad_cells(ph)
        mix=dn*(ur*vr+ut*vt)/q
        ar=(nu-1)*vr+mix*ur;at=(nu-1)*vt+mix*ut
        b=-(g.Crr.T@(w*ar)+g.Cth.T@(w*at))/w
        return sol.LU.newton(h)+S.adjoint(sol.LU.lu.solve(b))
    aa,bb=dot(v0,J(u)),dot(u,J(v0))
    rec=abs(aa-bb)/max(abs(aa),abs(bb),1e-300)
    rf,_=M.rho_cell(c)
    rho=g.rho_axisym(lambda R,z:rf(R,z)/sol.mu,nq=4);rx=S.forward(rho)
    neg=float(-np.dot(w,np.minimum(rx,0))/np.dot(w,rx))
    pos=float(np.max(rx));minratio=float(np.min(rx)/pos)
    pn=sol.LU.newton(rx);ph=sol.phantom(pn)
    p1=S.adjoint(ph);p2v=S.adjoint(ph+12345.)
    dr,dt=g.grad_cells(p1);er,et=g.grad_cells(p2v)
    gauge=float(max(np.max(np.abs((er-dr)[m])),np.max(np.abs((et-dt)[m]))))
    return dict(gaussian_l2_relative_peak=l2,reciprocity_analytic=dict(a=aa,b=bb,relative=rec),negative_density_mass_fraction=neg,minimum_density_over_peak=minratio,gauge_added_constant=12345.,gauge_gradient_absolute_error_inner30=gauge)


def custom_grid(a0,nr,nt,outer):
    mu=M.C.PS.mass_unit(a0)
    re=M.C.PS.log_edges(.005,outer*300*max(60,math.sqrt(6.6e10/mu)),30*nr)
    return M.C.PS.Grid(re,M.C.PS.theta_edges(48*nt,full=False,stretch_min=.002/nt)),mu


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    args=ap.parse_args()
    base=json.loads((M.HERE/'grid_run/results.json').read_text())
    saved=json.loads((M.HERE/'saved_run/results.json').read_text())
    old=json.loads((M.RB/'KT25_eps_equals_kappa/kt25.json').read_text())
    result={'checks':{},'refinement':{},'thresholds':dict(adjoint=1e-10,mass=1e-10,constant=1e-10,gaussian_l0=1e-4,gaussian_l2=.01,analytic_reciprocity=1e-8,negative_mass_fraction=1e-5,gauge_gradient_absolute_inner30=1e-7)}
    failures=[]
    for foot,f in base['footings'].items():
        if f['n_tested']!=1375: failures.append(foot+': coverage count')
        ch=f['checks']
        for key,lim in [('adjoint_relative',1e-10),('source_mass_relative',1e-10),('outer_constant_error',1e-10),('gaussian_max_absolute_over_peak',1e-4),('laplacian_weighted_symmetry_relative',1e-12),('nu_one_phantom_max',1e-14),('xi_zero_identity_error',1e-14)]:
            if not ch[key]<=lim: failures.append(foot+': '+key)
        if min(x['relative'] for x in ch['reciprocity'])>1e-6: failures.append(foot+': finite difference reciprocity')
        if abs(ch['gas_mass']['corrected_accounting_ratio']-1)>1e-5: failures.append(foot+': full gas mass')
        if not .499<ch['gas_mass']['inherited_ratio']<.501: failures.append(foot+': inherited halfspace reproduction')
        sr=saved['footings'][foot]['rows'];orows=old[f'mw|{foot}|0.5']['passing']
        legacy_error=max(abs(r['legacy_source_only'][k]-o[k]) for r,o in zip(sr,orows) for k in ('vc','K0','cK','cO','h'))
        if len(sr)!=len(orows) or legacy_error>1e-5:failures.append(foot+': legacy reproduction')
        result['checks'][foot]={'legacy_saved_max_absolute_score_error':legacy_error,'saved_cells':len(sr),'all_original_cells':len(f['rows'])}
        candidates=[('best_original',sr[0]['cell']),('best_corrected',f['summary']['corrected']['best']['cell'])]
        variants=[('base',1,1,1,24,120),('l16',1,1,1,16,120),('l32',1,1,1,32,120),('l40',1,1,1,40,120),('cut80',1,1,1,24,80),('cut180',1,1,1,24,180),('outer2',1,1,2,24,120),('radial2',2,1,1,24,120),('angular2',1,2,1,24,120),('spatial2',2,2,1,32,120),('spatial3',3,3,1,40,180)]
        rows=[]
        for name,nr,nt,outer,ell,cut in variants:
            g,mu=custom_grid(M.C.A0[foot],nr,nt,outer);sol=M.Solver(g,mu,M.C.A0[foot])
            for label,c in candidates:
                sigma=M.width(c,foot)
                o=sol.solve(c,sigma,ell,cut,plain=True)
                ex=extended_checks(sol,c,sigma,ell,cut)
                if name in ('base','spatial2','spatial3'):
                    for key,lim in [('gaussian_l2_relative_peak',.01),('negative_density_mass_fraction',1e-5),('gauge_gradient_absolute_error_inner30',1e-7)]:
                        if not ex[key]<=lim: failures.append(foot+': '+name+': '+label+': '+key)
                    if ex['reciprocity_analytic']['relative']>1e-8:failures.append(foot+': '+name+': '+label+': analytic reciprocity')
                rows.append(dict(variant=name,candidate=label,parameters=dict(radial=nr,angular=nt,outer=outer,lmax=ell,cut=cut),scores=o,extra_checks=ex))
                print(foot,name,label,{k:o['corrected'][k] for k in ('vc','K0','cK','cO','h')},ex,flush=True)
        result['refinement'][foot]=rows
    result['failures']=failures;result['passed']=not failures
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False))
    print('FAILURES',failures,flush=True)
    raise SystemExit(1 if failures else 0)


if __name__=='__main__':main()
