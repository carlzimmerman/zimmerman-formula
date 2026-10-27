"""Bounded independent-harmonic-site production calculation; natural units."""
import json, sys, math
import numpy as np
from scipy.special import gammaln
from numpy.polynomial.legendre import leggauss
M, MR, mass = 2e11, 2e6, 1e6
alpha, g, Z, hc = 1/137.035999084, 2.93129374869688e-15, 82, 1.973269804e-7
column, flux, width, branching = 3e25, 1e8, 5000., .5
r, R = math.sqrt(.002), math.sqrt(.02)
pall, pmax = 2*(R-r), 2*math.sqrt(R*R-r*r)
checks = []
def check(name, value, limit):
    assert value <= limit, (name, value, limit)
    checks.append(dict(name=name, error=float(value), tolerance=limit))
def accept(p):
    return np.minimum(1., np.maximum(0., (R*R-r*r-p*p/4)/(p*r)))
def spectrum(w):
    return flux/(math.sqrt(2*math.pi)*width)*np.exp(-.5*((w-MR-10)/width)**2)
def mink(a,b): return a[0]*b[0]-np.dot(a[1:],b[1:])
# Independently contract the scalar-photon tensor with conserved currents.
for p,u,n,om in [(0.,0.,100,.1),(.1,.3,333,.03),(.25,-.8,1000,.01)]:
    er=math.sqrt(MR*MR+p*p)
    for transverse in [False,True]:
        delta=(n+int(transverse))*om
        w=er+delta
        qv=np.array([-p*math.sqrt(1-u*u),0.,w-p*u])
        q2=np.dot(qv,qv); qnorm=math.sqrt(q2)
        k=np.array([w,0.,0.,w]); q=np.r_[delta,qv]; t=mink(q,q)
        eps=[np.array([0.,1.,0.,0.]),np.array([0.,0.,1.,0.])]
        if transverse:
            basis=[np.array([qv[2],0.,-qv[0]])/qnorm,np.array([0.,1.,0.])]
            currents=[np.r_[0.,v] for v in basis]
            reduced=(mink(k,q)**2-w*w*p*p*(1-u*u)*t/(2*q2))/t**2
        else:
            currents=[np.r_[1.,delta*qv/q2]]
            reduced=w*w*p*p*(1-u*u)/(2*q2*q2)
        direct=sum((mink(k,q)*mink(e,j)-mink(k,j)*mink(e,q))**2/t**2
                   for e in eps for j in currents)/2
        check('tensor_%s_%s'%(transverse,p),abs(direct-reduced)/max(abs(reduced),1e-50),2e-12)
        for j in currents:
            check('continuity',abs(mink(q,j))/max(qnorm,1),1e-14)
            check('photon_Ward',abs(mink(k,q)*mink(k,j)-mink(k,j)*mink(k,q)),0.)
# Oscillator operator verification: finite matrices, test low excited states.
# rho=exp(iQx) computed independently from a Hermitian eigendecomposition.
N=100; a=np.diag(np.sqrt(np.arange(1,N)),1)
x=(a+a.T)/math.sqrt(2); pop=1j*(a.T-a)/math.sqrt(2)
vals,vec=np.linalg.eigh(x)
for eta in [.1,1.,5.]:
    Q=math.sqrt(2*eta)
    rho=(vec*np.exp(1j*Q*vals))@vec.T
    j=(pop@rho+rho@pop)/2
    for n in range(12):
        exact=np.exp(-eta/2)*(1j*math.sqrt(eta))**n/math.sqrt(math.factorial(n))
        check('oscillator_density',abs(rho[n,0]-exact),3e-14)
        check('oscillator_continuity',abs(n*rho[n,0]-Q*j[n,0]),2e-13)
    check('transverse_current_ground',abs(pop[1,0]-1j/math.sqrt(2)),1e-15)

def rate(om, order, extra=0):
    eta0=MR*MR/(2*M*om)
    nmax=int(math.ceil(eta0+15*math.sqrt(eta0)+100))+extra
    n=np.arange(nmax+1)
    logfac=gammaln(n+1)
    weights=np.exp(-eta0+n*np.log(eta0)-logfac)
    check('poisson_norm',abs(weights.sum()-1),2e-12)
    check('poisson_mean',abs(np.dot(weights,n)/eta0-1),2e-12)
    nodes,ws=leggauss(order)
    total=np.zeros(2)
    pref=column*hc*hc*branching*alpha*g*g*Z*Z/(8*math.pi)
    for lo,hi in [(0,pall),(pall,pmax)]:
        ps=lo+(nodes+1)*(hi-lo)/2
        pw=ws*(hi-lo)/2
        for p,wp in zip(ps,pw):
            er=math.sqrt(MR*MR+p*p)
            for u,wu in zip(nodes,ws):
                qt2=p*p*(1-u*u)
                for channel in [0,1]:
                    delta=(n+channel)*om
                    w=er+delta
                    q2=w*w+p*p-2*w*p*u
                    t=delta*delta-q2
                    eta=q2/(2*M*om)
                    wn=np.exp(-eta+n*np.log(eta)-logfac)
                    if channel==0:
                        kernel=w/er*qt2/q2**2
                    else:
                        kernel=om/M*w/er*((er-p*u)**2-qt2*t/(2*q2))/t**2
                    total[channel]+=pref*2*math.pi*p*p*wp*wu*accept(p)*np.sum(spectrum(w)*wn*kernel)
    return total
nodes,ws=leggauss(64)
I4=VA=0.
for lo,hi in [(0,pall),(pall,pmax)]:
    ps=lo+(nodes+1)*(hi-lo)/2; pw=ws*(hi-lo)/2
    I4+=sum(pw*ps**4*accept(ps)); VA+=4*math.pi*sum(pw*ps**2*accept(ps))
common=column*hc*hc*branching*spectrum(MR+10)*alpha*g*g*Z*Z
leadL=common/(3*MR**4)*I4
rows=[]
for om in [.01,.03,.1]:
    coarse=rate(om,12); fine=rate(om,24); extended=rate(om,24,100)
    check('quadrature_refinement',float(max(abs(coarse/fine-1))),1e-10)
    check('spectral_cutoff_refinement',float(max(abs(extended/fine-1))),1e-12)
    leadT=common*om/(8*math.pi*M*MR**2)*VA
    check('small_momentum_longitudinal',abs(fine[0]/leadL-1),1e-4)
    check('small_momentum_transverse',abs(fine[1]/leadT-1),1e-4)
    rows.append(dict(omega_eV=om,longitudinal_pairs_per_s=float(fine[0]),
                     transverse_pairs_per_s=float(fine[1]),total_pairs_per_s=float(sum(fine)),
                     transverse_over_longitudinal=float(fine[1]/fine[0]),
                     leading_transverse_pairs_per_s=float(leadT)))
result=dict(model='Independent isotropic ground-state harmonic sites; no real material supplied',
            assumptions=dict(M_eV=M,MR_eV=MR,g_per_eV=g,Z=Z,column_per_m2=column,
                             photon_flux_per_s=flux,photon_RMS_eV=width,branching=branching,
                             daughter_Kstar_eV=1e-9,daughter_Kcut_eV=1e-8),
            acceptance_volume_eV3=VA,I4_eV5=I4,leading_longitudinal_pairs_per_s=float(leadL),
            rows=rows,checks=checks,passed=len(checks))
with open(sys.argv[1],'w') as f: json.dump(result,f,indent=2); f.write('\n')
print(json.dumps({k:result[k] for k in ['rows','passed']},indent=2))
