#!/usr/bin/env python3
"""Same C-H action: nonlinear lift/range obstruction, not a full theory gate.

See REPORT.md for the continuum argument. Finite spectral calculations do
not prove divergence, and failure of a C2 auxiliary response is not by
itself a proof of ghost/causality failure or absence of exact solutions.
"""
import argparse
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.special import logsumexp
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
KERNEL_PATH=HERE.parent/'two_body_frequency_2026'/'binary_frequency.py'
spec=importlib.util.spec_from_file_location('exact_kernel',KERNEL_PATH)
kernel=importlib.util.module_from_spec(spec); spec.loader.exec_module(kernel)


@lru_cache(None)
def symbolic_checks():
    y=sp.symbols('y',positive=True)
    s=y*(1-sp.exp(-y))
    q=2-2*(1+y)*sp.exp(-y)-y*y*sp.exp(-2*y)
    f=sp.factor(sp.diff(q,y)/sp.diff(s,y)/2)
    lam=sp.diff(s,y)
    peak=sp.solve(sp.diff(lam,y),y)[0]
    f_min=sp.simplify((sp.diff(f,y)/lam).subs(y,peak))
    x=sp.symbols('x',real=True)
    jump=sp.limit(sp.diff(sp.sin(x)**2,x,2),x,0,dir='+')-sp.limit(sp.diff(-sp.sin(x)**2,x,2),x,0,dir='-')
    n=sp.symbols('n',positive=True,integer=True)
    # For odd n, integrate the product-to-sum identity on (0,pi).
    coefficient=sp.factor(2/sp.pi*(1/n-sp.Rational(1,2)/(n+2)-sp.Rational(1,2)/(n-2)))
    trig=sp.trigsimp(sp.sin(x)**2*sp.sin(n*x)-
        (sp.sin(n*x)/2-sp.sin((n+2)*x)/4-sp.sin((n-2)*x)/4),method='fu')
    return dict(flux_identity_residual=sp.simplify(f-y*sp.exp(-y)),
        flux_small_s_coefficient=sp.limit(f/sp.sqrt(s),y,0,dir='+'),
        q_small_s_coefficient=sp.limit(q/s**sp.Rational(3,2),y,0,dir='+'),
        cusp_second_derivative_jump=jump,odd_fourier_coefficient=coefficient,
        product_to_sum_residual=trig,
        lambda_derivative=sp.factor(sp.diff(lam,y)),lambda_peak_y=peak,
        flux_derivative_minimum=f_min,
        averaged_sine_cube=sp.integrate(sp.sin(x)**3,(x,0,sp.pi))/sp.pi)


def cusp_coefficient(n):
    return 0.0 if n%2==0 else float(8/(np.pi*n*(4-n*n)))


def quadrature_coefficient(n):
    # Split at the sign change; independent adaptive weighted integration.
    positive=quad(lambda x: np.sin(x)**2,0,np.pi,weight='sin',wvar=n,
                  epsabs=2e-14,epsrel=2e-14)[0]
    negative=quad(lambda x: -np.sin(x)**2,np.pi,2*np.pi,weight='sin',wvar=n,
                  epsabs=2e-14,epsrel=2e-14)[0]
    return (positive+negative)/np.pi


def spectral_norm(width,cutoff,kind='gaussian'):
    ns=np.arange(1,cutoff+1,2,dtype=float)
    coeff=8/(np.pi*ns*(4-ns*ns))
    if kind=='gaussian':
        logS=-.5*width*width*ns*ns; logS1=-.5*width*width
    elif kind=='helmholtz':
        logS=-np.log1p(width*width*ns*ns); logS1=-np.log1p(width*width)
    else:
        raise ValueError('unsupported control filter')
    # Required derivative coefficients: -b_n/(alpha S_1^2 S_n), alpha=1.
    logd=np.log(np.abs(coeff))-2*logS1-logS
    return dict(width=width,cutoff=cutoff,filter=kind,
        log10_gradient_rms=float((logsumexp(2*logd)-np.log(2))/(2*np.log(10))),
        last_log10_derivative_coefficient=float(logd[-1]/np.log(10)))


def cubic_infimum(width):
    # Pointwise Legendre minimum; independent real quadrature for its integral.
    average=quad(lambda x: abs(np.sin(x))**3,0,2*np.pi,
                 points=[np.pi],epsabs=1e-13,epsrel=1e-13)[0]/(2*np.pi)
    return float(-4/3*np.exp(1.5*width*width)*average)


def leading_minimum(width,modes,npoints):
    """Minimize J_M in filtered-gradient coordinates, not inverse-heat ones."""
    x=(np.arange(npoints)+.5)*2*np.pi/npoints
    sine=np.sin(x[:,None]*np.arange(1,modes+1)[None,:])
    A=np.exp(.5*width*width)
    def value_gradient(coeff):
        p=sine@coeff
        value=2*A*coeff[0]+8/3*np.mean(np.abs(p)**1.5)
        gradient=4*sine.T@(np.sign(p)*np.sqrt(np.abs(p)))/npoints
        gradient[0]+=2*A
        return float(value),gradient
    r=minimize(value_gradient,np.zeros(modes),jac=True,method='BFGS',
               options=dict(gtol=2e-9,maxiter=1500))
    v,g=value_gradient(r.x)
    return dict(width=width,modes=modes,npoints=npoints,value=v,
        gradient_norm=float(np.linalg.norm(g)),optimizer_success=bool(r.success),
        optimizer_message=str(r.message))


def problem(amplitude,width,modes,npoints):
    if amplitude<=0 or width<0 or modes<1 or npoints<4*modes:
        raise ValueError('positive amplitude, nonnegative width, resolved modes required')
    x=(np.arange(npoints)+.5)*2*np.pi/npoints
    ns=np.arange(1,modes+1)
    sine=np.sin(x[:,None]*ns[None,:])
    gains=np.exp(-.5*width*width*ns*ns)
    scale=np.sqrt(amplitude+gains*gains)
    D=sine/scale[None,:]; SD=D*gains[None,:]
    lapse=np.exp(amplitude*np.cos(x)); a1=-np.sin(x)
    def value_gradient(v):
        d=D@v; p=SD@v
        q=kernel.dual_q_array(amplitude*amplitude*np.abs(p))
        flux=kernel.flux((amplitude*amplitude*p)[:,None])[:,0]/amplitude
        value=np.mean(lapse*(2*amplitude*d*d-4*d*a1+2*q/amplitude**3))
        gradient=4*(D.T@(lapse*(amplitude*d-a1))+SD.T@(lapse*flux))/npoints
        return float(value),gradient
    return value_gradient,dict(x=x,ns=ns,sine=sine,D=D,SD=SD,lapse=lapse,
        a1=a1,scale=scale,gains=gains)


def gradient_check():
    f,_=problem(.003,.3,6,1024)
    v=np.array([-.5,.04,.1,.03,.02,-.01]); direction=np.array([.2,.6,-.1,.4,-.3,.12])
    h=1e-6
    analytic=float(f(v)[1]@direction)
    numerical=(f(v+h*direction)[0]-f(v-h*direction)[0])/(2*h)
    return dict(analytic=analytic,finite_difference=numerical,
        relative_error=float(abs(analytic-numerical)/max(abs(analytic),abs(numerical),1e-12)))


def nonuniform_trial(k,width,npoints=4096):
    """Exact trial U=lnN, not a stationary solve; alpha=1, xi fixed, k integer."""
    # Phase coordinates integrate every integer-k period without aliasing.
    phase=(np.arange(npoints)+.5)*2*np.pi/npoints
    t2=width*width*k*k
    d=np.exp(-t2); amplitude=d/k
    lapse=np.exp(amplitude*np.cos(phase)); acc=-d*np.sin(phase)
    U_prime=acc.copy()
    filtered=np.exp(-t2/2)*U_prime
    square=float(np.mean(2*lapse*(U_prime-acc)**2))
    trial=square+float(np.mean(2*lapse*kernel.dual_q_array(np.abs(filtered))))
    baseline=float(np.mean(2*lapse*acc*acc))
    sine_moment=quad(lambda x: np.sin(x)**1.5,0,np.pi,
                     epsabs=1e-13,epsrel=1e-13)[0]/np.pi
    return dict(k=k,width=width,amplitude=float(amplitude),
        log_lapse_H1_norm=float(amplitude*np.sqrt((1+k*k)/2)),
        squared_gradient_term=square,trial_energy=trial,baseline_energy=baseline,
        minimum_ratio_upper_bound=trial/baseline,
        asymptotic_upper_bound=float(8/3*sine_moment*np.exp(-t2/4)))


def solve_auxiliary(amplitude,width,modes,npoints):
    f,r=problem(amplitude,width,modes,npoints)
    solution=minimize(f,np.zeros(modes),jac=True,method='BFGS',
                      options=dict(gtol=2e-9,maxiter=1500))
    value,gradient=f(solution.x)
    d=r['D']@solution.x; p=r['SD']@solution.x
    # Independent FFT application of S to the lapse-weighted exact flux.
    ff=kernel.flux((amplitude*amplitude*p)[:,None])[:,0]/amplitude
    freq=np.fft.rfftfreq(npoints,1/npoints)
    outer=np.fft.irfft(np.fft.rfft(r['lapse']*ff)*np.exp(-.5*width*width*freq*freq),npoints)
    total_flux=r['lapse']*(amplitude*d-r['a1'])+outer
    projected=2*r['sine'].T@total_flux/npoints
    target=-np.exp(width*width)*np.sin(r['x'])*np.abs(np.sin(r['x']))
    return dict(amplitude=amplitude,width=width,modes=modes,npoints=npoints,
        optimizer_success=bool(solution.success),optimizer_message=str(solution.message),
        iterations=int(solution.nit),scaled_gradient_norm=float(np.linalg.norm(gradient)),
        energy_correction=float(value),relaxed_cubic_infimum=cubic_infimum(width),
        scaled_gradient_rms=float(np.sqrt(np.mean(d*d))),
        gradient_rms=float(amplitude*amplitude*np.sqrt(np.mean(d*d))),
        filtered_gradient_target_relative_error=float(np.linalg.norm(p-target)/np.linalg.norm(target)),
        projected_flux_residual_rms=float(np.linalg.norm(projected)/np.sqrt(2)),
        full_flux_residual_rms=float(np.std(total_flux)),
        scaled_gradient_coefficients=(solution.x/r['scale']).tolist())


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=HERE)
    parser.add_argument('--require-closed',action='store_true')
    args=parser.parse_args(); started=time.time(); checks=[]
    def check(name,ok):
        checks.append(dict(name=name,passed=bool(ok)))
        print(f'[{"PASS" if ok else "FAIL"}] {name}',flush=True)
    symbolic=symbolic_checks()
    check('exact q first variation and small-field power',
        symbolic['flux_identity_residual']==0 and symbolic['flux_small_s_coefficient']==1 and
        symbolic['q_small_s_coefficient']==sp.Rational(4,3))
    check('necessary leading filtered profile is not C2',symbolic['cusp_second_derivative_jump']!=0)
    check('exact flux lower bound gives positive small-lapse convexity margin',
        all(np.exp(-e)+float(symbolic['flux_derivative_minimum'])*np.exp(e)>0 for e in (.01,.5,1)))
    coeffs=[dict(n=n,exact=cusp_coefficient(n),quadrature=quadrature_coefficient(n)) for n in range(1,34)]
    check('Fourier coefficients from independent integrals',symbolic['product_to_sum_residual']==0 and
          max(abs(r['exact']-r['quadrature']) for r in coeffs)<2e-12)
    spectra=[spectral_norm(w,n,f) for f in ('gaussian','helmholtz') for w in (0,.2,.5) for n in (15,31,63,127)]
    check('identity-filter Parseval control',abs(10**(2*spectral_norm(0,101)['log10_gradient_rms'])-3/8)<1e-9)
    check('inverse Gaussian growth contrasts with algebraic control',
        spectral_norm(.5,41)['log10_gradient_rms']-spectral_norm(.5,21)['log10_gradient_rms']>50 and
        abs(spectral_norm(.5,201,'helmholtz')['log10_gradient_rms']-spectral_norm(.5,101,'helmholtz')['log10_gradient_rms'])<.002)
    grad=gradient_check()
    check('exact lapse-weighted functional gradient',grad['relative_error']<2e-6)
    runs=[solve_auxiliary(e,w,32,2048) for w in (.2,.5) for e in (1e-2,1e-4,1e-6,1e-8)]
    refinement=[solve_auxiliary(e,.5,m,n) for e in (1e-6,1e-8)
                for m,n in ((16,2048),(32,4096),(64,4096))]
    leading=[leading_minimum(.5,m,4096) for m in (4,8,16,32)]
    fixed_mode=solve_auxiliary(1e-8,.5,8,4096)
    check('fixed-mode amplitude limit uses its own cubic stationary target',
        all(r['gradient_norm']<3e-6 for r in leading) and
        all(leading[i]['value']>leading[i+1]['value']>cubic_infimum(.5) for i in range(3)) and
        abs(fixed_mode['energy_correction']-leading[1]['value'])<2e-6)
    check('nonlinear stationary residuals resolved in tested modes',
        all(r['scaled_gradient_norm']<3e-6 and r['projected_flux_residual_rms']<3e-7 for r in runs+refinement))
    check('small-amplitude cubic energies approach independent relaxed infimum',
        all(abs(runs[i+3]['energy_correction']/cubic_infimum(w)-1)<.02 and
            abs(runs[i+3]['energy_correction']/cubic_infimum(w)-1)<abs(runs[i]['energy_correction']/cubic_infimum(w)-1)
            for i,w in ((0,.2),(4,.5))))
    check('amplitude-normalized auxiliary response grows over resolved range',
        all(runs[i+3]['scaled_gradient_rms']>runs[i+2]['scaled_gradient_rms']>runs[i+1]['scaled_gradient_rms'] for i in (0,4)))
    check('quadrature and spectral refinement agree at fixed amplitude',
        all(abs(r['energy_correction']-next(a for a in runs if a['width']==.5 and a['amplitude']==r['amplitude'])['energy_correction'])<2e-5 and
            abs(r['scaled_gradient_rms']/next(a for a in runs if a['width']==.5 and a['amplitude']==r['amplitude'])['scaled_gradient_rms']-1)<.002
            for r in refinement if r['modes']>=32))
    nonuniform=[nonuniform_trial(k,.5) for k in (4,8,12,16,20)]
    check('exact trial disproves uniform extrapolation of fixed-k quadratic energy',
        all(r['squared_gradient_term']==0 for r in nonuniform) and
        all(nonuniform[i+1]['minimum_ratio_upper_bound']<nonuniform[i]['minimum_ratio_upper_bound'] for i in range(4)) and
        nonuniform[-1]['minimum_ratio_upper_bound']<1e-9)
    failed=any(not r['passed'] for r in checks)
    rc=1 if failed else (2 if args.require_closed else 0)
    data=dict(theory_status='OPEN',regular_quadratic_auxiliary_lift='OBSTRUCTED under the hypotheses in REPORT.md',
        symbolic={k:str(v) for k,v in symbolic.items()},coefficients=coeffs,spectral_norms=spectra,
        exact_gradient_check=grad,nonlinear_runs=runs,refinement=refinement,
        finite_mode_cubic=leading,fixed_mode_amplitude_limit=fixed_mode,
        nonuniform_trials=nonuniform,checks=checks)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    output=args.output_dir/'results.json'; output.write_text(json.dumps(data,indent=2)+'\n')
    sources=[HERE/'nonlinear_lift.py',HERE/'test_nonlinear_lift.py',HERE/'CONTRACT.md',HERE/'REPORT.md',KERNEL_PATH,
        HERE.parent/'g03_covariant_action_2026'/'ACTION.md',HERE.parent/'g03_flrw_scalar_2026'/'REPORT.md']
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    manifest=dict(schema_version=1,claim_id='C-H-singular-nonlinear-auxiliary-lift',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))),
        command='python3 -B '+str((HERE/'nonlinear_lift.py').relative_to(ROOT))+
            (' --require-closed' if args.require_closed else '')+
            (' --output-dir <output-directory>' if args.output_dir!=HERE else ''),
        environment=dict(software=[platform.python_version(),'numpy '+np.__version__,'scipy '+scipy.__version__,'sympy '+sp.__version__],hardware=platform.machine(),
                         openblas_num_threads=os.environ.get('OPENBLAS_NUM_THREADS')),
        mathematics=dict(assertion_tested='Necessary leading nonlinear auxiliary equation; heat range obstruction; bounded spectral stationary solves',
            coefficient_domain='SymPy exact; float64 quadrature/minimization; log-domain spectra',
            conventions='alpha=1 numerically, period2pi, spatial averages, epsilon>0, mean U=0',
            inputs=[dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sources],
            bounds=dict(widths=[.2,.5],amplitudes=[1e-2,1e-4,1e-6,1e-8],modes=[16,32,64],nodes=[1024,2048,4096],spectral_cutoffs=[15,31,63,127],
                        leading_cubic=dict(width=.5,modes=[4,8,16,32],nodes=4096),
                        gradient_check=dict(amplitude=.003,width=.3,modes=6,nodes=1024),
                        spectral_controls=dict(widths=[0,.5],cutoffs=[21,41,101,201]),
                        coefficient_quadrature=dict(n_min=1,n_max=33),
                        joint_limit_trial=dict(width=.5,k=[4,8,12,16,20],amplitude='exp(-width^2*k^2)/k')),
            non_claims=['no exact nonlinear solutions','ghost or acausality theorem','full nonlinear Dirac closure','new empirical law','global novelty','new filter theory validated']),
        randomness=dict(used=False,generator='',seed=None),
        run=dict(started_at=datetime.fromtimestamp(started,timezone.utc).isoformat(),runtime_seconds=time.time()-started,exit_status=rc),
        outputs=[dict(path=str(output.relative_to(ROOT)) if output.is_relative_to(ROOT) else output.name,sha256=digest(output))],
        checks=checks,result='FAILED_DIAGNOSTIC' if failed else 'REGULAR_LIFT_OBSTRUCTED_FULL_THEORY_OPEN',
        residual_risks=['singular response is not itself a proof of physical ill-posedness','finite stationary solves do not prove continuum convergence'])
    (args.output_dir/'computation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Regular auxiliary lift: OBSTRUCTED; full theory: OPEN; exit',rc)
    return rc


if __name__=='__main__':
    raise SystemExit(main())
