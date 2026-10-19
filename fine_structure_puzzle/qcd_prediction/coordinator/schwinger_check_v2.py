#!/usr/bin/env python3
"""Finite checks of a tilted-torus spectral normalization; no 4D QCD inference."""
import argparse, json, math
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy import special

parser=argparse.ArgumentParser()
parser.add_argument("--output",required=True)
args=parser.parse_args()
mp.mp.dps=50
checks=[]; rows=[]
def check(label,condition):
    checks.append({"label":label,"passed":bool(condition)})
    if not condition: raise AssertionError(label)

def F_series(a):
    a=mp.mpf(str(a)); nmax=1000
    value=mp.fsum(1/mp.mpf(n)-1/mp.sqrt(n*n+a*a) for n in range(1,nmax+1))
    for k in range(1,7):
        coeff=(-1)**(k+1)*mp.binomial(2*k,k)/(4**k)
        value+=coeff*a**(2*k)*mp.zeta(2*k+1,nmax+1)
    k=7
    error=abs(mp.binomial(2*k,k)/(4**k)*a**(2*k)*mp.zeta(2*k+1,nmax+1))
    return float(value),float(error)

def log_eta_abs_squared(z):
    z=mp.mpc(z.real,z.imag)
    value=-mp.pi*z.imag/6
    for n in range(1,101):
        value+=2*mp.log(abs(1-mp.exp(2j*mp.pi*z*n)))
    return float(value)

def parts(x,t1,t0):
    norm=math.hypot(t1,t0); a=x*norm/(2*math.pi)
    f,ferr=F_series(a)
    n=np.arange(1,301,dtype=float); r=np.sqrt(n*n+a*a)
    b=2*math.pi*t0*r/norm**2
    theta=2*math.pi*t1*n/norm**2
    z=np.exp(-b+1j*theta)
    bsum=float(np.sum(2*np.real(z/(1-z))/r))
    coth=1/math.tanh(x*t0/(2*norm))
    zerogreen=coth/(2*x*norm)
    wronggreen=coth/(2*x*t0)
    eta=log_eta_abs_squared(-1/complex(t1,t0))
    kernel=-zerogreen+1/(x*x*t0)+(-eta+f-bsum)/(2*math.pi)
    wrong=kernel+zerogreen-wronggreen
    log_ratio=-math.pi*coth/(x*norm)+f-bsum-math.log(x*norm/(4*math.pi))-float(mp.euler)
    return kernel,wrong,log_ratio,ferr

def images(x,t1,t0,nmax=32):
    ns=np.arange(-nmax,nmax+1,dtype=float)
    n0,n1=np.meshgrid(ns,ns,indexing="ij")
    radii=np.hypot(n1+t1*n0,t0*n0)
    z=x*radii[radii>0]
    logarithm=-float(np.sum(special.k0(z)))
    derivative=1+float(np.sum(z*special.k1(z)))
    # lambda_min(g)>=det(g)/trace(g), a conservative singular-value bound.
    sigma=t0/math.sqrt(t1*t1+t0*t0+1)
    b=x*sigma; s=nmax+1; q=mp.exp(-mp.mpf(str(b)))
    bound=8*mp.sqrt(mp.pi/(2*b))*q**s*(mp.sqrt(s)/(1-q)+q/(2*mp.sqrt(s)*(1-q)**2))
    return logarithm,derivative,max(float(bound),1e-280) # conservative floor avoids recording an underflowed zero bound

def direct_kernel(x,t1,t0,nmax=384):
    ns=np.arange(-nmax,nmax+1,dtype=float)
    n0,n1=np.meshgrid(ns,ns,indexing="ij")
    r2=((n0-t1*n1)**2+t0*t0*n1*n1)/(t0*t0)
    r2=r2[r2>0]
    p2=(2*math.pi/x)**2*r2 # m=1, L=x
    value=float(np.sum(1/(p2*(p2+1)))/(x*x*t0))
    trace=t1*t1+t0*t0+1
    b=(2*math.pi/x)**2/trace
    tail=4/(x*x*t0*b*b*nmax*nmax)
    return value,tail

shapes=[(0.,1.),(.5,1.),(1.,1.),(.3,1.4)]
for t1,t0 in shapes:
    for x in [4.,8.,12.,24.,48.]:
        kernel,wrong,logratio,ferr=parts(x,t1,t0)
        image,dlog,tail=images(x,t1,t0)
        check("F omitted-tail bound below 1e-20",ferr<1e-20)
        check("eta/F representation agrees with massive Green images",abs(logratio-image)<3e-13+tail)
        row={"mL":x,"tau1":t1,"tau0":t0,"log_condensate_ratio":image,"mL_times_log_ratio":x*image,
             "coupling_log_derivative":dlog,"image_tail_bound":tail,
             "correct_m2K":kernel,"printed_m2K":wrong,
             "wrong_large_L_coefficient":-math.pi*(1/t0-1/math.hypot(t1,t0))}
        if x<=12:
            direct,bound=direct_kernel(x,t1,t0)
            check("correct kernel lies within positive spectral-tail bracket",direct-2e-13<=kernel<=direct+bound+2e-13)
            if t1!=0:
                check("printed prefactor rejected by full spectral bracket",wrong<direct-2e-13)
            row.update({"direct_partial_m2K":direct,"spectral_tail_bound":bound})
        rows.append(row)
    image,_,bound=images(8.,t1,t0)
    shifted,_,bound2=images(8.,t1+1,t0)
    check("massive images invariant under tau -> tau+1 basis change",abs(image-shifted)<1e-13+bound+bound2)
    step=1e-5
    left=images(8*math.exp(-step),t1,t0)[0]-step
    right=images(8*math.exp(step),t1,t0)[0]+step
    fd=(right-left)/(2*step)
    check("coupling response agrees with independent finite difference",abs(fd-images(8,t1,t0)[1])<3e-8)

small=[]
for x in [.1,.03,.01]:
    correct,wrong,_,_=parts(x,.5,1.)
    direct,bound=direct_kernel(x,.5,1.)
    check("small-m exact spectral positivity",direct>0 and correct>=direct-2e-11 and correct<=direct+bound+2e-11)
    check("printed small-m kernel is negative",wrong<0)
    small.append({"mL":x,"correct_m2K":correct,"printed_m2K":wrong,"positive_spectral_partial":direct,"tail_bound":bound})
# Elementary zero-slice sum independently finite with an integral tail bound.
for x,t1,t0 in [(4.,.5,1.),(8.,1.,1.),(.1,.5,1.)]:
    norm=math.hypot(t1,t0); nmax=20000
    ns=np.arange(-nmax,nmax+1,dtype=float)
    p2=(2*math.pi/x)**2*norm**2*ns*ns/(t0*t0)
    finite=float(np.sum(1/(p2+1))/(x*x*t0))
    analytic=1/(2*x*norm*math.tanh(x*t0/(2*norm)))
    tail=t0/(2*math.pi**2*norm**2*nmax)
    check("raw massive zero-slice prefactor from direct integer sum",finite<=analytic+1e-11 and analytic<=finite+tail+1e-11)

result={"claim_id":"QCD-S","parent":"FSP-002","checks":checks,"check_count":len(checks),"passed":True,
        "rows":rows,"small_mass_counterexamples":small,
        "scope":"Finite numerical comparisons of exact 2D spectral/condensate identities with analytic truncation bounds plus floating tolerances; no interval arithmetic, 4D c_H or alpha0 prediction",
        "software":{"numpy":np.__version__,"mpmath":mp.__version__},
        "source_correction":"General-tau zero-slice denominator |tau| replaces printed tau0; mathematical source adjudication additionally requires the independent proof review."}
Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"passed":True,"checks":len(checks),"rows":len(rows),"small_mass_examples":len(small)}))
