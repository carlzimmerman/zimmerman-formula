#!/usr/bin/env python3
"""Final result gate: exact population, unchanged cuts/widths, all-source tails.

Also writes explicit radial/angular contributions to the complete vertical
force for the old and new best fixed cells; no force component is dropped.
"""
import argparse
import json
import math
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import mw_reciprocal as M
import numpy as np


def components(sol,c,sigma):
    g=sol.g;rf,_=M.rho_cell(c);rho=g.rho_axisym(lambda R,z:rf(R,z)/sol.mu,nq=4)
    pn=sol.LU.newton(rho);S=sol.get_filter(sigma,48,120)
    ph=sol.phantom(sol.LU.newton(S.forward(rho)));phi=pn+S.adjoint(ph)
    dr,dt=g.grad_cells(phi);R=np.r_[M.C.R0,M.C.BR_R];z=np.full_like(R,1.1)
    gr=g.interp_cells(dr,R,z);gt=g.interp_cells(dt,R,z)
    # Match inherited observable: transform on cells, then interpolate.
    zrad=g.interp_cells(np.cos(g.t2d)*dr,R,z)
    zang=g.interp_cells(-np.sin(g.t2d)*dt,R,z)
    radial=g.interp_cells(np.sin(g.t2d)*dr+np.cos(g.t2d)*dt,R,z)
    unit=sol.a0/(2*math.pi*M.C.PS.G_SI)/(M.C.PS.MSUN/(M.C.PS.KPC/1e3)**2)
    obs=sol.evaluate(phi)
    return dict(cell=c,xi=sigma,R_kpc=R.tolist(),z_kpc=z.tolist(),g_r_over_a0=gr.tolist(),g_theta_over_a0=gt.tolist(),g_R_over_a0=radial.tolist(),g_z_radial_part_over_a0=zrad.tolist(),g_z_angular_part_over_a0=zang.tolist(),K_radial_part=(zrad*unit).tolist(),K_angular_part=(zang*unit).tolist(),K_total=((zrad+zang)*unit).tolist(),scores=obs)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    scan=json.loads((M.HERE/'grid_refined_run/results.json').read_text())
    prelim=json.loads((M.HERE/'grid_run/results.json').read_text())
    checks=json.loads((M.HERE/'final_checks_run/results.json').read_text())
    saved=json.loads((M.HERE/'saved_run/results.json').read_text())
    expected=[c for c in M.cells() if M.C.L.RD_TAG[0]<=c['rd']<=M.C.L.RD_TAG[1] and M.C.L.MSTAR_TAG[0]<=M.rho_cell(c)[1]<=M.C.L.MSTAR_TAG[1]]
    assert len(expected)==1375
    failures=[];out={'outcome':'conditional on floating numerical resolution and finite harmonic projection','final_grid':'grid_refined_run/results.json','final_checks_passed':checks['passed'],'footings':{}}
    if not checks['passed']:failures.append('final numerical checks failed')
    for foot,f in scan['footings'].items():
        rows=f['rows'];ch=f['checks']
        if [r['cell'] for r in rows]!=expected:failures.append(foot+': population mismatch')
        for k,lim in [('adjoint_relative',1e-10),('source_mass_relative',1e-10),('outer_constant_error',1e-10),('gaussian_max_absolute_over_peak',1e-4),('laplacian_weighted_symmetry_relative',1e-12),('nu_one_phantom_max',1e-14),('xi_zero_identity_error',1e-14)]:
            if ch[k]>lim:failures.append(foot+': '+k)
        if min(r['relative'] for r in ch['reciprocity'])>1e-6:failures.append(foot+': finite reciprocity')
        g,mu=M.make_grid(M.C.A0[foot],2,1);sol=M.Solver(g,mu,M.C.A0[foot])
        maxneg=-1.;worst=None;minrel=0.;masserr=0.;widtherr=0.;scoreerr=0.
        for i,r in enumerate(sorted(rows,key=lambda r:r['xi'])):
            c=r['cell'];sigma=r['xi'];widtherr=max(widtherr,abs(sigma-M.width(c,foot)))
            rf,_=M.rho_cell(c);rho=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4);S=sol.get_filter(sigma,48,120);rx=S.forward(rho)
            mass=float(np.dot(g.vol,rx));negative=float(-np.dot(g.vol,np.minimum(rx,0))/mass)
            if negative>maxneg:maxneg=negative;worst=c
            minrel=min(minrel,float(np.min(rx)/np.max(rx)));masserr=max(masserr,abs(mass/np.dot(g.vol,rho)-1))
            for form in ['newton','source_only','corrected']:
                q=r[form];re=M.C.lines(q['vc'],q['K'],q['K0'],q['vc_Ou'])
                if any(q[k]!=re[k] for k in (*M.GATE,'Lh')):failures.append(foot+': cuts mismatch')
                scoreerr=max(scoreerr,max(abs(q[k]-re[k]) for k in ('cK','cO','h','D')))
            if i%250==0:print(foot,'source audit',i+1,'/',len(rows),'max negative mass',maxneg,flush=True)
        if maxneg>1e-5:failures.append(foot+': negative source tails exceed tolerance')
        if widtherr>1e-14 or masserr>1e-10 or scoreerr>1e-10:failures.append(foot+': width/mass/score mismatch')
        old=saved['footings'][foot]['rows'][0]['cell'];best=f['summary']['corrected']['best']['cell']
        out['footings'][foot]=dict(n_tested=len(rows),summary=f['summary'],negative_source_mass_fraction_max=maxneg,negative_worst_cell=worst,minimum_density_over_peak_all_cells=minrel,source_mass_relative_error_max=masserr,width_absolute_error_max=widtherr,score_recalculation_absolute_error_max=scoreerr,components=[components(sol,c,M.width(c,foot)) for c in (old,best)],base_to_refined_max_dvc=max(abs(a['corrected']['vc']-b['corrected']['vc']) for a,b in zip(prelim['footings'][foot]['rows'],rows)),base_to_refined_max_dK=max(abs(a['corrected']['K0']-b['corrected']['K0']) for a,b in zip(prelim['footings'][foot]['rows'],rows)),base_to_refined_max_dcO=max(abs(a['corrected']['cO']-b['corrected']['cO']) for a,b in zip(prelim['footings'][foot]['rows'],rows)))
    out['failures']=failures;out['passed']=not failures;Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False));print('FAILURES',failures,flush=True)
    raise SystemExit(0 if out['passed'] else 1)


if __name__=='__main__':main()
