#!/usr/bin/env python3
"""Bounded checks: particle-derived thermal compression and quantum protocol.

This is not a gravitational dipole construction. Source is a trap stiffness.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import gammaln

checks=[];rows=[]
def check(name,error,tol):
    checks.append({'name':name,'error':float(error),'tolerance':tol})
    assert abs(error)<tol,(name,error,tol)

# Independent canonical Gamma-coordinate integrations, not a gap ensemble.
L,kappa,T=2.,.75,3.
a0=L*kappa
for N in (1,2,4):
    nu=1.5*N;theta=T/a0;Q0=nu*theta
    def probability(Q):
        if Q==0:return 0.
        return math.exp((nu-1)*math.log(Q)-Q/theta-gammaln(nu)-nu*math.log(theta))
    for E in (0.,.3,2.,8.):
        Z=quad(lambda Q:probability(Q)*math.exp(-E*Q/T),0,np.inf,epsabs=1e-13,epsrel=2e-12)[0]
        moment=quad(lambda Q:Q*probability(Q)*math.exp(-E*Q/T),0,np.inf,epsabs=1e-13,epsrel=2e-12)[0]
        exactZ=(1+E/a0)**(-nu)
        exactQ=Q0/(1+E/a0)
        check('Gamma partition N%d E%g'%(N,E),Z/exactZ-1,2e-8)
        check('actual reweighted moment N%d E%g'%(N,E),(moment/Z)/exactQ-1,2e-8)
        check('induced rational response N%d E%g'%(N,E),(Q0-moment/Z)-Q0*E/(a0+E),1e-8)
        rows.append({'N':N,'E':E,'Z_ratio':Z,'Q':moment/Z,'induced_p':Q0-moment/Z})

# Quantum x² source: actual n->n+2 transition and diagonal population terms.
# hbar=1; finite thermal matrix uses complete levels up to119 with tiny tail.
quantum=[]
for omega in (.7,1.,2.):
 for temp in (.4,1.2,2.5):
    beta=1/temp;x=beta*omega/2;n=np.arange(120,dtype=float)
    probs=np.exp(-beta*omega*n);probs/=sum(probs)
    qdiag=(2*n+1)/(4*L*omega)
    mean=float(probs@qdiag)
    qmean=1/(4*L*omega*math.tanh(x))
    qoff2=(n[:-2]+1)*(n[:-2]+2)/(16*L*L*omega*omega)
    off=float(np.sum((probs[:-2]-probs[2:])*qoff2)/omega)
    diagonal=beta*float(probs@qdiag**2-mean**2)
    exactoff=1/(8*L*L*omega**3*math.tanh(x))
    exactdiag=x/(8*L*L*omega**3*math.sinh(x)**2)
    check('quantum actual Q mean '+str((omega,temp)),mean/qmean-1,2e-11)
    check('n to n+2 Kubo line '+str((omega,temp)),off/exactoff-1,2e-11)
    check('population diagonal susceptibility '+str((omega,temp)),diagonal/exactdiag-1,2e-10)
    # Numerical derivative of exact mean at fixed temperature, source changes omega².
    eps=1e-5;Delta=eps/(2*L*omega)
    f=lambda w:1/(4*L*w*math.tanh(beta*w/2))
    derivative=-(f(omega+Delta)-f(omega-Delta))/(2*eps)
    check('full isothermal response '+str((omega,temp)),derivative/(off+diagonal)-1,2e-8)
    quantum.append({'omega':omega,'T':temp,'gap_of_Q_source':2*omega,'mean_Q':mean,'Kubo_offdiagonal':off,'population_term':diagonal})

for x in (.001,.03,.2,1.,5.):
    error=x/math.tanh(x)-1
    assert 0<=error<=x*x/3+1e-14
    checks.append({'name':'classical coordinate-moment error bound '+str(x),'error':error,'upper_bound':x*x/3})

# Finite positive heat-capacity receiver: actual reversible entropy balance.
N=5.;Cs=3*N;T0=2.;Q0=1.5*N*T0/a0
bath=[]
for ratio in (0.,1.,10.,100.):
    Cb=ratio*Cs;eta=Cs/(2*(Cs+Cb));power=1-eta
    for E in (.2,2.,20.):
        s=1+E/a0;temp=T0*s**eta
        entropy=(Cs+Cb)*math.log(temp/T0)-(Cs/2)*math.log(s)
        check('finite bath entropy '+str((ratio,E)),entropy,1e-10)
        Q=Q0*s**(-power)
        # Actual first law: dU/dE=(Cs+Cb)dT/dE equals the conjugate width.
        dUdE=(Cs+Cb)*eta*temp/(a0*s)
        check('finite receiver first law '+str((ratio,E)),dUdE/Q-1,1e-12)
        bath.append({'Cb_over_Cs':ratio,'E':E,'T':temp,'deficit_exponent':power,'Q':Q,'induced_p':Q0-Q})

# Continuum canonical TF strong-source moment constants in a quadratic well.
# R=1,K=1, source curvature g/L chosen by mass normalization of a parabola.
M=1.;K=1.;L=1.;R=1.;E=15*K*M*L/(2*math.pi*R**5)
rho=lambda r:E/(4*K*L)*(R*R-r*r)
mass=4*math.pi*quad(lambda r:r*r*rho(r),0,R)[0]
moment=4*math.pi*quad(lambda r:r**4*rho(r),0,R)[0]
check('TF strong-source mass',mass/M-1,1e-12)
check('TF deficit constant',moment/(2*L)-3*M*R*R/(14*L),1e-12)
S=4*math.pi*K*quad(lambda r:r*r*rho(r)**2,0,R)[0]
V=E*moment/(2*L)
check('TF harmonic virial',2*V/(3*S)-1,1e-12)

pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args()
out={'status':'passed','check_count':len(checks),'checks':checks,'Gamma_rows':rows,'quantum_rows':quantum,'finite_bath_rows':bath,'scope':'Canonical stiffness/compression source, not an acceleration-conjugate internal dipole. Conditional thermal and TF comparisons; no universal G or occupation selection.'}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'passed','checks':len(checks),'quantum_source_transition':'2*hbar*omega','positive_finite_bath_exponent_range':[.5,1.]}))
