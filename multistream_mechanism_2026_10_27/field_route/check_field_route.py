#!/usr/bin/env python3
"""Finite checks of reciprocal stress-gate terms; no halo evolution or fit."""
import json, math, pathlib, sys
import numpy as np
import sympy as s

ROOT = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT / 'run' / 'results.json'
A, Pstar, rhoref = .4, 1., .7
p = np.array([[i,j,k] for i in (-1.,1.) for j in (-1.,1.) for k in (-1.,1.)])
w = np.array([.8,1.1,.9,1.2,1.3,.7,1.05,.95]) / 8

def state(weights, momenta):
    rho=weights.sum(); mean=(weights[:,None]*momenta).sum(0)/rho
    offsets=momenta-mean
    Pi=np.einsum('n,ni,nj->ij',weights,offsets,offsets)
    I=np.linalg.det(Pi)**(1/3)
    u=-A*(math.log(rho/rhoref)+1)
    gate=I**3/(Pstar**3+I**3)
    gp=3*I**2*Pstar**3/(Pstar**3+I**3)**2
    energy=(weights*np.sum(momenta*momenta,axis=1)).sum()/2+u*gate
    return rho,mean,offsets,Pi,I,u,gate,gp,energy

rho,mean,off,Pi,I,u,g,gp,E=state(w,p)
h=np.sum(p*p,axis=1)/2-g*A/rho+u*gp*I/3*np.einsum('ni,ij,nj->n',off,np.linalg.inv(Pi),off)
errs=[]
for i in range(len(w)):
    eps=1e-6; wp=w.copy(); wm=w.copy(); wp[i]+=eps; wm[i]-=eps
    fd=(state(wp,p)[-1]-state(wm,p)[-1])/(2*eps)
    errs.append(abs(fd-h[i]))
assert max(errs)<2e-9

# Affine adiabatic dilation: volume a^3, density a^-3, canonical momenta a^-1.
def interaction_energy(a):
    st=state(w/a**3,p/a)
    return a**3*st[5]*st[6]
eps=1e-6
P_fd=-(interaction_energy(1+eps)-interaction_energy(1-eps))/(6*eps)
P_exact=g*A*math.log(rho/rhoref)+(5/3)*I*gp*u
assert abs(P_fd-P_exact)<2e-9

# Scalar kinetic parent: positive kinetic metric Achi, exact Legendre transform.
chi,m2,M2,beta,lam,K,V0=s.symbols('chi m2 M2 beta lam K V0', positive=True)
Achi=1+beta*chi**2/(3*M2)
W=V0+K/Achi+m2*chi**2/2+lam*chi**4/4
mass2=s.simplify(s.diff(W,chi,2).subs(chi,0))
threshold=s.solve(mass2,K)[0]
assert s.simplify(threshold-3*m2*M2/(2*beta))==0
assert s.diff(mass2,V0)==0

# Bare-potential shortcut instead is unbounded in large kinetic pressure.
Ip=s.symbols('Ip', positive=True)
Wbad=3*Ip/2+V0-(beta*Ip/M2-m2)**2/(4*lam)
bad_quadratic=s.expand(Wbad).coeff(Ip,2)
assert s.simplify(bad_quadratic+beta**2/(4*lam*M2**2))==0

reference_rows=[]
for logref in (-10.,0.,10.):
    uu=-A*(1-logref)  # rho=I=Pstar=1, g'=3/4
    reference_rows.append(dict(log_rhoref=logref,u=uu,kinetic_coefficient=1+uu/2))
assert reference_rows[0]['kinetic_coefficient']<0

# X54 xi=0 DES-SN5YR refit, solely an illustrative native-background ratio.
h0=.6847; wc=.11859; Om=.3009
ratio=(wc/h0**2)/(1-Om)
qstar=.826107036001911/(16*math.pi**2)
c=299792458.
primordial=[]
for z in (1090.,50000.):
    sig0=c*math.sqrt(qstar/(ratio*(1+z)**5))
    primordial.append(dict(z=z,sigma_today_m_s=sig0,sigma_at_z_m_s=sig0*(1+z)))

result=dict(assertion_tested='finite gate variation, compression, mediator threshold and primordial scaling checks',
    max_functional_derivative_abs_error=max(errs),pressure_finite_difference=P_fd,pressure_formula=P_exact,
    omitted_pressure_term=(5/3)*I*gp*u,scalar_effective_mass_squared=str(mass2),
    scalar_K_threshold=str(threshold),unbounded_shortcut_I_squared_coefficient=str(bad_quadratic),
    reference_shift_examples=reference_rows,canonical_pressure_fraction=qstar,
    native_background_rho_c_over_rho_de=ratio,primordial_bounds=primordial,
    non_claims=['No field-to-kinetic derivation','No covariant completion','No halo or cosmology evolution',
                'No Lambda normalization or attractor derived','No ghost-free claim for arbitrary stress gates'])
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
