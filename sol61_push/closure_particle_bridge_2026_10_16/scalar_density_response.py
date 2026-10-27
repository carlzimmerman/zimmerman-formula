"""Density-vertex response of a homogeneous gapped nodal patch.

Distinct from the previous mass/polarization vertex. Neutral zero-T patch;
imaginary frequencies compared to direct interband projectors. No physical
galaxy damping time or finite-band/isotropic completion is inferred.
"""
import cmath
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import roots_legendre

out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name

def analytic(gap,Q,Omega):
    ss=Q*Q+Omega*Omega
    if Q==0:return 0.
    root=math.sqrt(ss)
    return Q*Q*(gap/(2*ss)+(ss-4*gap*gap)*math.atan(root/(2*gap))/(4*root**3))
def feynman(gap,Q,Omega):
    return Q*Q*quad(lambda x:x*(1-x)/math.sqrt(gap*gap+x*(1-x)*(Q*Q+Omega*Omega)),0,1,epsabs=1e-13,epsrel=1e-12)[0]
def direct(gap,Q,Omega,N,ntheta):
    # Density vertex identity has interband overlap (1-hat d+ dot hat d-)/2.
    # Both directions of the spectral transition give the factor2 cancelling1/2.
    zz,ww=roots_legendre(N);t=(zz+1)/2;ww=ww/2
    scale=max(gap,Q,Omega)
    p=scale*t/(1-t);jac=scale/(1-t)**2
    angle=2*math.pi*np.arange(ntheta)/ntheta
    cosine=np.cos(angle)[None,:];sine=np.sin(angle)[None,:]
    pp=p[:,None]
    ep=np.sqrt(pp*pp+Q*Q/4+gap*gap+pp*Q*cosine)
    em=np.sqrt(pp*pp+Q*Q/4+gap*gap-pp*Q*cosine)
    product=ep*em;dd=pp*pp+gap*gap-Q*Q/4
    overlap=Q*Q*(gap*gap+pp*pp*sine*sine)/(product*(product+dd))
    total=ep+em
    average=np.mean(overlap*total/(total*total+Omega*Omega),axis=1)
    return float(ww@(p*jac*average))

rows=[]
for gap,Q,Omega in ((.1,.05,0.),(.1,1.,0.),(.1,1.,.4),(.3,.2,.4),(1.,.05,.2),(1.,1.,1.)):
    a=analytic(gap,Q,Omega);f=feynman(gap,Q,Omega)
    d=direct(gap,Q,Omega,192,384);ref=direct(gap,Q,Omega,384,768)
    check('closed vs Feynman '+str((gap,Q,Omega)),abs(a/f-1)<2e-10)
    check('direct interband normalization '+str((gap,Q,Omega)),abs(ref/a-1)<2e-5)
    check('direct integration refinement '+str((gap,Q,Omega)),abs(d/ref-1)<2e-5)
    rows.append(dict(gap=gap,Q_energy=Q,imaginary_frequency=Omega,chi_over_A=a,
        direct_interband_over_A=ref,relative_refinement=d/ref-1))
for gap in (.1,.3,1.):
    for Omega in (0.,.1,1.):check('uniform density Ward zero '+str((gap,Omega)),analytic(gap,0.,Omega)==0)
    Q=gap*1e-3
    check('gapped density low-momentum coefficient '+str(gap),abs(analytic(gap,Q,0)/(Q*Q/(6*gap))-1)<1e-6)

# Real-frequency absorption by continuation of the same closed function.
absorption=[]
for gap,Q,ratio in ((.1,.2,1.2),(.3,.5,2.),(1.,.1,3.)):
    omega=ratio*math.sqrt(Q*Q+4*gap*gap)
    z=complex(omega,1e-9);ss=Q*Q-z*z;root=cmath.sqrt(ss)
    value=Q*Q*(gap/(2*ss)+(ss-4*gap*gap)*cmath.atan(root/(2*gap))/(4*root**3))
    tt=math.sqrt(omega*omega-Q*Q)
    imag=math.pi*Q*Q*(tt*tt+4*gap*gap)/(8*tt**3)
    check('positive density absorption '+str((gap,Q,ratio)),value.imag>0)
    check('continued absorption coefficient '+str((gap,Q,ratio)),abs(value.imag/imag-1)<1e-6)
    absorption.append(dict(gap=gap,Q_energy=Q,omega=omega,Im_chi_over_A=value.imag,analytic_Im_chi_over_A=imag))

# Static RPA bound: no physical A/gap is selected by the illustrative scan.
parent=json.loads((base/'neutral_scalar_bridge_run_001/results.json').read_text())
rpa=[]
for p in parent['rows']:
    ms,aa,bb,u0=p['mediator_mass_GeV'],p['a_GeV'],p['b'],p['bare_u0_GeVminus2']
    lam=parent['parameters']['rep'];barecold=2*(lam+p['extra_bare_quartic'])
    lower=ms*ms-aa*aa/barecold-bb*bb/u0
    check('full scalar conservative static Schur margin '+str(ms),lower>0)
    for chi in np.geomspace(1e-12,1e12,25):
        kernel=ms*ms-aa*aa/barecold-bb*bb*chi/(1+u0*chi)
        check('static RPA all-wavevector surrogate '+str((ms,float(chi))),kernel>=lower*(1-1e-10))
    rpa.append(dict(mediator_mass_GeV=ms,lower_static_kernel_GeV2=lower,
        lower_static_kernel_over_vacuum_mass_squared=lower/(ms*ms)))
result=dict(rows=rows,absorption=absorption,static_RPA=rpa,checks=checks,
    conventions='chi>0 responds density to chemical source -mu q in H; exp(-iomega t); Q is energy-valued axial momentum; divide response by nodal DOS A; zero T/mu',
    non_claims=['No density-response equality to old mass-vertex Pi','No k=0 medium absorption from a conserved density vertex','No full finite-band, isotropic, doped, finite-temperature, cold momentum-response, global dynamic stability or physical damping time'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(controls=len(checks),rows=rows,static_RPA=rpa),indent=2))
