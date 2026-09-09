#!/usr/bin/env python3
"""Unbinned official-covariance shape test; all outputs stay in this new folder."""
import datetime as dt
import hashlib
import gzip
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import cho_factor,cho_solve
from scipy.optimize import minimize_scalar,brentq
from numpy.polynomial.legendre import leggauss

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
C=299792458.;MPC=3.0856775814913673e22;Z=np.sqrt(32*np.pi/3)
FOOTINGS={'input_9p4':9.4e-11,'old_canonical_cosmology_defined':9.354769736111044e-11,
          'old_SPARC_GLS':1.1814381247770623e-10,'old_SPARC_median':9.725607106012755e-11}

def main():
    started=dt.datetime.now(dt.timezone.utc).isoformat();tic=time.monotonic()
    table=np.genfromtxt(HERE/'release.dat',names=True,dtype=None,encoding=None)
    raw=np.loadtxt(HERE/'PantheonPlusSH0ES_STAT_SYS.cov.gz')
    n=int(raw[0]);cov=raw[1:].reshape(n,n)
    assert len(table)==n==1701
    asymmetry=float(np.max(abs(cov-cov.T)))
    assert asymmetry<1e-7
    cov=(cov+cov.T)/2 # Release text rounding leaves a maximum 3e-8 asymmetry.
    outputs={}
    for label,mask in [('official_zcut',table['zHD']>.01),('legacy_noncal_cut',(table['zHD']>.01)&(table['IS_CALIBRATOR']==0))]:
        z,zh,y=table['zHD'][mask],table['zHEL'][mask],table['m_b_corr'][mask]
        cc=cov[np.ix_(mask,mask)]
        chol=cho_factor(cc,lower=True,check_finite=True)
        one=np.ones(len(z));io=cho_solve(chol,one);norm=np.sum(one*io)
        nodes,weights=leggauss(48)
        zz=z[:,None]*(nodes+1)/2
        def template(om,ol=None,w0=-1.,wa=0.,order=48):
            ol=1-om if ol is None else ol
            ok=1-om-ol
            if order==48:grid=zz;wg=weights
            else:
                nd,wg=leggauss(order);grid=z[:,None]*(nd+1)/2
            rho=(1+grid)**(3*(1+w0+wa))*np.exp(-3*wa*grid/(1+grid))
            e2=om*(1+grid)**3+ok*(1+grid)**2+ol*rho
            if np.min(e2)<=0:return None
            dc=z/2*np.sum(wg/np.sqrt(e2),axis=1)
            dm=dc if abs(ok)<1e-12 else (np.sinh(np.sqrt(ok)*dc)/np.sqrt(ok) if ok>0 else np.sin(np.sqrt(-ok)*dc)/np.sqrt(-ok))
            if np.min(dm)<=0:return None
            return 5*np.log10((1+zh)*dm)
        def score(om,ol=None,w0=-1.,wa=0.):
            pred=template(om,ol,w0,wa)
            if pred is None:return 1e100
            r=y-pred;off=np.sum(io*r)/norm;res=r-off
            return float(np.sum(res*cho_solve(chol,res)))
        fit=minimize_scalar(score,bounds=(.01,.99),method='bounded',options={'xatol':1e-10})
        assert fit.success
        om=float(fit.x);best=float(fit.fun)
        lo=brentq(lambda v:score(v)-best-1,.01,om)
        hi=brentq(lambda v:score(v)-best-1,om,.99)
        cpl=minimize_scalar(lambda v:score(v,w0=-.83,wa=-.75),bounds=(.01,.99),method='bounded')
        assert cpl.success and np.isfinite(cpl.fun)
        quadrature_error=float(np.max(abs(template(om)-template(om,order=96))))
        assert quadrature_error<1e-10
        joint={}
        for h0 in (67.4,73.):
            def penalty(v):
                a=C/Z*(h0*1000/MPC)*np.sqrt(1-v)
                return score(v)+(np.log(a/FOOTINGS['old_SPARC_GLS'])/(1.9026066078649394e-11/FOOTINGS['old_SPARC_GLS']))**2
            jf=minimize_scalar(penalty,bounds=(.01,.99),method='bounded')
            assert jf.success and np.isfinite(jf.fun)
            joint[str(h0)]=dict(Omega_m=float(jf.x),delta_chi2_plus_inherited_log_prior=float(jf.fun-best),
                interpretation='Illustrative independent log-Gaussian old galaxy budget only; not joint calibration or exponential-law fit')
        rows=[]
        for name,a0 in FOOTINGS.items():
            for h0 in (67.4,73.):
                ol=(Z*a0/(C*h0*1000/MPC))**2
                flat_om=1-ol
                curved=minimize_scalar(lambda v:score(v,ol),bounds=(.001,.99),method='bounded')
                assert curved.success and np.isfinite(curved.fun) and curved.fun<1e99
                rows.append(dict(footing=name,a0=a0,H0=h0,Omega_Lambda=ol,
                    literal_flat_Omega_m=flat_om,literal_flat_delta_chi2=(score(flat_om)-best if flat_om>=0 else None),
                    curved_profile_Omega_m=float(curved.x),curved_profile_Omega_k=float(1-curved.x-ol),
                    curved_profile_delta_chi2=float(curved.fun-best),
                    old_formula_equivalent_flat_Omega_m=.334/(.334+ol),
                    old_formula_equivalent_delta_chi2=score(.334/(.334+ol))-best))
        hpred={name:dict(H0_kms_Mpc=Z*a0/C*MPC/1000/np.sqrt(1-om),
                         shape_only_H0_profile_interval=[Z*a0/C*MPC/1000/np.sqrt(1-v) for v in (lo,hi)])
               for name,a0 in FOOTINGS.items()}
        agrid={str(h0):dict(a0=C/Z*(h0*1000/MPC)*np.sqrt(1-om),
                           shape_only_interval=[C/Z*(h0*1000/MPC)*np.sqrt(1-v) for v in (hi,lo)]) for h0 in (67.4,73.)}
        outputs[label]=dict(n=int(mask.sum()),flat_LCDM=dict(Omega_m=om,chi2=best,profile_delta_chi2_one=[lo,hi]),
            fixed_CPL_profile=dict(w0=-.83,wa=-.75,Omega_m=float(cpl.x),delta_chi2=float(cpl.fun-best)),
            fixed_CPL_comparison_by_Omega_m={str(v):score(v,w0=-.83,wa=-.75)-score(v) for v in (.29,.315,.35)},
            footings=rows,conditional_H0_prediction=hpred,conditional_a0_at_H0=agrid,
            inherited_GLS_prior_profiles=joint,quadrature_48_vs_96_max_magnitude_difference=quadrature_error,
            offset_invariance=abs(score(om)-float(np.sum(((y-template(om)-100)-(np.sum(io*(y-template(om)-100))/norm))*cho_solve(chol,(y-template(om)-100)-(np.sum(io*(y-template(om)-100))/norm))))))
        assert outputs[label]['offset_invariance']<1e-8
    for local in ('prep_2026/sne_lambda/pantheonplus_full.dat','real_research/data_cache/PantheonPlusSH0ES.dat'):
        outputs['release_matches_'+local]=(ROOT/local).read_bytes()==(HERE/'release.dat').read_bytes()
    result=dict(scope='Published-correction baseline only: full-covariance flat/curved FLRW shape profiles conditional on the posited a0-Lambda law; no action-derived SNe prediction, significance conversion, or test of alternative age/redshift-frame corrections',
        public_release_revision='c447f0fea703fcd0fff57de5000947b5ca81286b',
        uncompressed_covariance_sha256=hashlib.sha256(gzip.decompress((HERE/'PantheonPlusSH0ES_STAT_SYS.cov.gz').read_bytes())).hexdigest(),
        release_covariance_max_asymmetry=asymmetry,results=outputs)
    out=HERE/'results.json';out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    sha=lambda p:dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    inputs=[Path(__file__),HERE/'release.dat',HERE/'PantheonPlusSH0ES_STAT_SYS.cov.gz',ROOT/'prep_2026/a0_line/fire_slope_results.json']
    manifest=dict(schema_version=1,claim_id='supernova-full-covariance-reaudit',repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),dirty=True),
        command=sys.executable+' -B '+str(Path(__file__).relative_to(ROOT)),environment=dict(software=['Python '+platform.python_version(),'NumPy '+np.__version__,'SciPy '+scipy.__version__],hardware=platform.machine()),
        mathematics=dict(assertion_tested=result['scope'],coefficient_domain='IEEE754 float64',conventions='Official zHD integration and zHEL luminosity prefactor; full STAT+SYS covariance; analytic free magnitude intercept; GR FLRW; no radiation',inputs=[sha(p) for p in inputs],bounds={'total_rows':1701,'quadrature_order':48,'Omega_m_profile':[.01,.99],'H0_choices':[67.4,73.],'w0_wa_fixed':[-.83,-.75]},non_claims=['No standalone H0 or absolute a0 measurement from uncalibrated SNe','No diagonal-error significance','No new a0 measurement or jointly propagated galaxy distance calibration','No inferred IC13/14 cosmology']),
        randomness=dict(used=False,generator='',seed=None),run=dict(started_at=started,runtime_seconds=time.monotonic()-tic,exit_status=0),outputs=[sha(out)],checks=[dict(name='covariance dimension, symmetry and Cholesky positive definiteness',passed=True),dict(name='constant-intercept invariance',passed=all(v['offset_invariance']<1e-8 for v in outputs.values() if isinstance(v,dict)))],result='Conditional full-covariance shape and calibration profiles',residual_risks=['Legacy v1 manifest does not enforce resource caps','Galaxy footings inherited, not remeasured; distance and interpolation systematics need joint treatment','Curved profiles bounded to nonnegative matter fraction; no global cosmology exploration'])
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
