"""Full-component finite-threshold controls of the exact hierarchy reduction."""
import os
import sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import json
import math
from pathlib import Path
import resource
import time
import mpmath as mp
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from pressure_scan import cw
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/gapless_charge'))
from gaugino_threshold import build_model,ext_basis,threshold,summarize
mp.mp.dps=60
Z=mp.mpf('7.3671437212785083116194')


def main(path):
    start=time.monotonic()
    units=json.loads((ROOT/'reviews/radial_ir_cold_2026_11_01/run_units/result.json').read_text())
    C=units['photino_mass_coefficient']
    K=math.sqrt(31)*C
    refs={}
    e=mp.mpf('.003')
    for t in ('1','1.16','1.26'):
        c=e/31
        refs[t]=cw(Z*mp.mpf(t)*mp.sqrt(c)/e,e,e,mp.sqrt(mp.mpf(29)/200)*e)/(c*c)
    rows=[]
    for hh in ('.0003','.003','.03'):
        for ll in ('.0003','.003','.03'):
            h,lam=mp.mpf(hh),mp.mpf(ll)
            delta=30*h*h+lam*lam
            c=lam*lam*h/delta
            Fhat=lam/mp.sqrt(delta)
            for t in ('1','1.16','1.26'):
                X=Z*mp.mpf(t)*mp.sqrt(c)/h
                val=cw(X,h,lam,mp.sqrt(mp.mpf(29)/200)*lam)/(c*c)
                model=build_model(float(X),float(h),float(lam),math.sqrt(29/200)*float(lam),vertices=False)
                ext,labels=ext_basis(model)
                groups,deg=summarize(threshold(model,ext),labels)
                mass=groups['U1']['signed_mass']
                alt,_=summarize(threshold(model,ext,Q2=7.),labels)
                k=mass/(float(lam)**2*math.sqrt(float(c)))
                rows.append(dict(h=float(h),lam=float(lam),z_over_min=float(t),X=float(X),
                                 CW_scaled=float(val),CW_scaling_relative_error=float(abs(val/refs[t]-1)),
                                 finite_mass_hat=mass,Kchi=k,Fhat=float(Fhat),
                                 threshold_Q_relative_error=abs(alt['U1']['signed_mass']/mass-1),
                                 subgroup_degeneracy=deg,
                                 mass_over_sqrtF=mass/math.sqrt(float(Fhat))))
    for t in ('1','1.16','1.26'):
        subset=[r for r in rows if r['z_over_min']==float(t)]
        ref=next(r for r in subset if r['h']==.003 and r['lam']==.003)['Kchi']
        for r in subset:r['threshold_scaling_relative_error']=abs(r['Kchi']/ref-1)
    h,l=sp.symbols('h l',positive=True)
    D=30*h*h+l*l
    P=l**10*h*h/D
    dh=sp.simplify(sp.diff(P,h))
    dl=sp.simplify(sp.diff(P,l))
    rho=units['constants']['rho_DE_GeV4']
    maxmass=C*(31*rho)**.25*.03**2.5
    checks={
        'twentyseven_full_component_cases':len(rows)==27,
        'complete_CW_scaling_60digits':max(r['CW_scaling_relative_error'] for r in rows)<1e-40,
        'threshold_scaling':max(r['threshold_scaling_relative_error'] for r in rows)<1e-5,
        'threshold_Q_independence':max(r['threshold_Q_relative_error'] for r in rows)<1e-5,
        'minimum_coefficient_matches_prior':max(abs(r['Kchi']/K-1) for r in rows if r['z_over_min']==1.)<1e-5,
        'positive_h_derivative':sp.simplify(dh-2*h*l**12/D**2)==0,
        'positive_lambda_derivative':sp.simplify(dl-l**9*h*h*(300*h*h+8*l*l)/D**2)==0,
        'source_mass_max_at_equal_upper_couplings':max(r['mass_over_sqrtF'] for r in rows if r['z_over_min']==1.)==next(r['mass_over_sqrtF'] for r in rows if r['h']==.03 and r['lam']==.03 and r['z_over_min']==1.),
    }
    result=dict(claim_id='TP06_UNEQUAL_YUKAWA_SOURCE_BOUND',checks={k:bool(v) for k,v in checks.items()},
                cases=rows,Kchi_at_min=K,maximum_mass_for_raw_DE_GeV=maxmass,
                max_threshold_scaling_error=max(r['threshold_scaling_relative_error'] for r in rows),
                dh=str(dh),dl=str(dl),
                scope='Uniform leading scaling reduction at fixedz andcriticalg/lambda; finite27case fullmatrix controls; maxsourcebound at universalCWminimum. No arbitrarygauge/background/newmasssource theorem.',
                runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(path).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
