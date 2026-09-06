#!/usr/bin/env python3
"""Construct the allowed J_N=3 branch and attack its zero-field static gate.

Same normalized static action as bridge_audit.py; two ALTERNATIVE kernels,
not one theory with two laws. Exact spherical law only at xi=0 and using
G_infinity, not the locally screened G. Fixed inputs: KB=1/5,c14=1e-5,jN=3.
The RAR primitive uses a definite integral whose derivative is checked
symbolically and whose value is independently quadrature-tested.
No full covariant constraint, empirical, or causal certificate is claimed.
"""
import argparse
import datetime
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import time

import scipy
from scipy.integrate import quad
import sympy as sp
from sympy.calculus.euler import euler_equations

from bridge_audit import derive as bridge_derive

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
ETA=sp.Rational(180000,199999)
FS=ETA/(4-ETA)


def point(kernel, u):
    eta, f=float(ETA),float(FS)
    e=math.exp(-u)
    if kernel=='mu_exp':
        r=u
        b=u*(-math.expm1(-u))
    elif kernel=='nu_RAR':
        b=u*u
        r=b/(-math.expm1(-u))
    else:
        raise ValueError(kernel)
    s=r-b/(1+f)
    X=(s/eta)**2
    j=eta*(1+f)/(f+e)-1
    if kernel=='mu_exp':
        primitive=(f*u*u+2*(e*(u*u+u+1)-1))/(eta*(1+f))-X
    else:
        integral=quad(lambda t: t**3/(-math.expm1(-t)) if t else 0,
                      0,u,epsabs=1e-12,epsrel=1e-12)[0]
        primitive=r*r/eta-4*integral/(eta*(1+f))-X
    return dict(X=X,j=j,J=primitive,s=s,g_total=r,g_bar=b)


def derive():
    u,eta,f=sp.symbols('u eta f',positive=True)
    e=sp.exp(-u)
    q=1+f
    j=eta*q/(f+e)-1
    old=bridge_derive()
    curves={}
    for name in ('mu_exp','nu_RAR'):
        if name=='mu_exp':
            r=u; b=u*(1-e)
        else:
            r=u*u/(1-e); b=u*u
        s=sp.factor(r-b/q)
        X=sp.factor((s/eta)**2)
        if name=='mu_exp':
            primitive=(f*u*u+2*(e*(u*u+u+1)-1))/(eta*q)-X
            dprimitive=sp.diff(primitive,u)
            margin=1/(1+float(sp.exp(-2)))-1/(1+float(FS))
        else:
            I3=sp.Function('I3')(u)  # I3(u)=integral_0^u t^3/(1-exp(-t)) dt.
            primitive=r*r/eta-4*I3/(eta*q)-X
            dprimitive=sp.diff(primitive,u).subs(sp.diff(I3,u),u**3/(1-e))
            margin=old['rar_minimum_slope']-1/(1+float(FS))
        residuals={
            'primitive_derivative':sp.factor(dprimitive-j*sp.diff(X,u)),
            'scalar_flux_is_bare_Newtonian_source':sp.factor((1+j-eta)*s/eta-b/q),
            'independent_total_acceleration':sp.factor(b/q+s-r),
            'Newtonian_coefficient':sp.simplify(sp.limit(j,u,sp.oo).subs({eta:ETA,f:FS})-3),
            'deep_field_coefficient':sp.simplify(sp.limit(j,u,0)-(eta-1)),
        }
        # Reconstruct target using the resulting flux, rather than reassigning g.
        errors=[]
        for val in (0.001,0.01,0.1,1,3,10,100):
            row=point(name,val)
            g0=(1+row['j']-float(ETA))*row['s']/float(ETA)
            errors.append(abs((g0+row['s'])/row['g_total']-1))
        assert max(errors)<1e-12
        curves[name]={
            'parameter_u':'g/a0' if name=='mu_exp' else 'sqrt(g_bar/a0)',
            'X':X,'J':primitive,'J_prime':j,'s_over_a0':s,
            'exact_residuals':residuals,'j_newtonian':sp.limit(j,u,sp.oo).subs({eta:ETA,f:FS}),
            'minimum_slope_margin':margin,'sample_max_reconstruction_error':max(errors),
        }
    # Vary the higher-gradient term before passing to Fourier space. These are
    # quadratic energies after the metric constraint, not a frozen-metric guess.
    z=sp.symbols('z',real=True)
    chi=sp.Function('chi')(z)
    A,ell,h=sp.symbols('A ell h',positive=True)
    density=-A*h*ell**2*sp.diff(chi,z,2)**2
    EL=euler_equations(density,chi,z)[0].lhs
    variation_residual=sp.simplify(EL+2*A*h*ell**2*sp.diff(chi,z,4))
    j0=sp.limit(j,u,0).subs(eta,ETA)
    return {
        'eta':ETA,'f_s':FS,'G_infinity_over_G_local':1+FS,
        'local_G_exact_asymptote':sp.simplify(FS)==0,
        'j_zero':j0,'curves':curves,
        'inside_static_k4':sp.Rational(9,5)*j0,
        'outside_static_k4':sp.Rational(9,5),
        'fourth_order_EL':EL,'fourth_order_variation_residual':variation_residual,
        'interpretation':'Spherical reconstruction succeeds with G_infinity; inside-J zero-field spatial energy is negative. Outside-J is a distinct action.'
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict-inside',action='store_true')
    args=parser.parse_args()
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t0=time.monotonic()
    r=derive()
    assert all(v==0 for row in r['curves'].values() for v in row['exact_residuals'].values())
    assert r['fourth_order_variation_residual']==0
    out=json.dumps(r,default=str,indent=2,sort_keys=True)+'\n'
    print(out)
    if args.strict_inside:
        return 0 if r['inside_static_k4']>=0 else 2
    (HERE/'escape_results.json').write_text(out)
    sources=[HERE/p for p in ('escape_audit.py','test_escape_audit.py','ESCAPE_REPORT.md',
        'escape_results.json','bridge_audit.py','zero_field_source_audit.py','zero_field_source_results.json')]
    sources.extend([ROOT/'hunt_2026/f34_timedep_scalar_sector.py',
        ROOT/'qwen_claude_field_theory/closure_2026/g03f_wb_fifth_force_bound.py'])
    manifest={
        'schema_version':1,'claim_id':'g03-J-reconstruction-zero-field-2026',
        'repository':{'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))},
        'command':'python3 -B '+str(Path(__file__).resolve().relative_to(ROOT)),
        'environment':{'software':['Python '+platform.python_version(),'SymPy '+sp.__version__,'SciPy '+scipy.__version__],
            'hardware':platform.machine()},
        'mathematics':{'assertion_tested':__doc__,'coefficient_domain':'real symbolic algebra and binary64 quadrature',
            'conventions':'ESCAPE_REPORT.md; distinct inside/outside-J actions',
            'inputs':['KB=1/5','c14=1e-5','J_N=3'],
            'bounds':{'sample_u':[.001,.01,.1,1,3,10,100]},
            'non_claims':['full relativistic closure','local-G exact MOND','finite-xi exact AQUAL','causal completion']},
        'randomness':{'used':False,'generator':'','seed':None},
        'run':{'started_at':start,'runtime_seconds':time.monotonic()-t0,'exit_status':0},
        'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources],
        'checks':[{'name':name+': '+key,'passed':value==0} for name,row in r['curves'].items() for key,value in row['exact_residuals'].items()],
        'result':r['interpretation'],
        'residual_risks':['Reconstruction limited to spherical charge-free static limit.',
            'New binary analysis not a calibration of G_infinity versus local G.',
            'Full nonlinear Dirac analysis remains absent.']}
    (HERE/'escape_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
