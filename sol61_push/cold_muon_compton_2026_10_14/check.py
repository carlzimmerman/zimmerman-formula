"""Direct Yukawa semi-Compton cold-tail calculation, free muon at rest."""
import json
import math
from pathlib import Path
import sys

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[2]
beam=json.loads((ROOT/'sol61_push/lab_cold_photon_acceptance_2026_10_13/run/results.json').read_text())
source=json.loads((ROOT/'sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())
mmu=105658375.5; me=510998.95; MR=2e6+2e-9
y=source['reduced_muon_case']['yukawa']; alpha=1/137.035999084
hc=1.973269804e-7; e2y2=4*math.pi*alpha*y*y
Kstar=1e-9; Kcut=1e-8; mphi=1e6
r=math.sqrt(2*mphi*Kstar); R=math.sqrt(2*mphi*Kcut)
Pall=2*(R-r); Pmax=2*math.sqrt(R*R-r*r)
checks=[]


def check(name,value):
    checks.append({'name':name,'passed':bool(value)})
    assert value,name


I2=np.eye(2,dtype=complex); zero=np.zeros((2,2),dtype=complex)
pauli=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
G=[np.block([[I2,zero],[zero,-I2]])]+[np.block([[zero,s],[-s,zero]]) for s in pauli]
I4=np.eye(4,dtype=complex)


def slash(p):
    return p[0]*G[0]-sum(p[j]*G[j] for j in range(1,4))


def tensor(p,k,q,eps):
    ds=2*k[0]  # initial muon momentum (1,0,0,0); all momenta divided by mmu
    du=q[0]**2-np.dot(q[1:],q[1:])-2*q[0]
    return (slash(p+k)+I4)@slash(eps)/ds+slash(eps)@(slash(p-q)+I4)/du


def trace_for(k,q):
    p=np.array([1.,0,0,0]); pf=p+k-q
    total=0.0
    for eps in [np.array([0.,1,0,0]),np.array([0.,0,1,0])]:
        A=tensor(p,k,q,eps)
        total+=np.trace((slash(pf)+I4)@A@(slash(p)+I4)@G[0]@A.conj().T@G[0]).real/4
    return total


def momenta(P,u):
    ER=math.sqrt(MR*MR+P*P)
    w=(2*mmu*ER-MR*MR)/(2*(mmu-ER+P*u))
    return np.array([w,0,0,w])/mmu, np.array([ER,P*math.sqrt(max(0,1-u*u)),0,P*u])/mmu


def accept(P):
    if P<=Pall: return 1.0
    if P>=Pmax: return 0.0
    return (R*R-r*r-P*P/4)/(P*r)


check('Dirac Clifford algebra',all(np.max(np.abs(G[i]@G[j]+G[j]@G[i]-
      (2*(1 if i==0 else -1)*I4 if i==j else 0*I4)))<1e-14 for i in range(4) for j in range(4)))
w0=MR*(2*mmu-MR)/(2*(mmu-MR))
trace0=MR*MR/(mmu*(mmu-MR))
check('rest scalar analytic spin trace',abs(trace_for(*momenta(0,0))/trace0-1)<2e-8)

for P,u in [(0,0),(Pmax,-1),(Pmax,0),(Pmax,.6),(Pmax,1)]:
    k,q=momenta(P,u); p=np.array([1.,0,0,0]); pf=p+k-q
    ward=(slash(pf)+I4)@tensor(p,k,q,k)@(slash(p)+I4)
    check('Ward identity '+str((P,u)),np.max(np.abs(ward))<1e-10)

# Independent primary-source benchmark: massless outgoing scalar, Eq (5a)
# in Caputo/Raffelt/Vitagliano PRD 105 035022. Keep recoil in this check.
mp.mp.dps=65
massless_rows=[]
for x in [.01,.1,1.]:
    def angular(u):
        qenergy=x/(1+x*(1-u))
        k=np.array([x,0,0,x])
        q=np.array([qenergy,qenergy*math.sqrt(1-u*u),0,qenergy*u])
        return trace_for(k,q)*qenergy/(x*(1+x*(1-u)))
    ratio=3/8*quad(angular,-1,1,epsabs=1e-10,epsrel=1e-9)[0]
    s=1+2*mp.mpf(str(x))
    literature=mp.mpf(3)/4*((1-3*s)/(2*s*s)-16/(s-1)**2+(s+3)**2/(s-1)**3*mp.log(s))
    check('massless integrated cross section '+str(x),abs(ratio/float(literature)-1)<1e-7)
    massless_rows.append({'photon_energy_over_mmu':x,'sigma_over_scalar_Thomson':ratio,'source_value':float(literature)})

volume=beam['accepted_momentum_volume_eV3']
den0=mmu*w0*MR*(mmu-MR)
beam_rms=5000.; flux=1e8; area=1e-6
spectral_areal=flux/(area*math.sqrt(2*math.pi)*beam_rms)
rate0=hc*hc*spectral_areal*.5*e2y2*trace0/(64*math.pi**2*den0)*volume


def integrate(order):
    nodes,weights=leggauss(order)
    total=0.
    for lo,hi in [(0,Pall),(Pall,Pmax)]:
        for xn,xw in zip(nodes,weights):
            P=(hi+lo)/2+(hi-lo)*xn/2
            angular=0.
            for u,uw in zip(nodes,weights):
                k,q=momenta(P,u); w=k[0]*mmu; ER=q[0]*mmu
                den=mmu*w*ER*(mmu-ER+P*u)
                weight=math.exp(-.5*((w-w0)/beam_rms)**2)
                angular+=uw*trace_for(k,q)/trace0*den0/den*weight
            total+=xw*(hi-lo)/2*2*math.pi*P*P*accept(P)*angular
    return total/volume


ratio16=integrate(16); ratio32=integrate(32)
check('cold momentum quadrature refinement',abs(ratio16-ratio32)<2e-7)
check('cold region constant-amplitude approximation',abs(ratio32-1)<2e-6)
per_muon=rate0*ratio32
lifetime=2.1969803e-6
muon_delivery=1e8
inventory=muon_delivery*lifetime
p_electron_min=(MR*MR-me*me)/(2*me)
check('free electron light-cone bound above cold momentum',p_electron_min>Pmax)

out={'all_pass':all(c['passed'] for c in checks),'checks':checks,
     'parameters':{'mmu_eV':mmu,'MR_eV':MR,'y_mu':y,'photon_flux_per_s':flux,'beam_area_m2':area,
                   'photon_RMS_eV':beam_rms,'ideal_stopped_muon_delivery_per_s':muon_delivery,
                   'muon_lifetime_s':lifetime,'carrier_branch':.5},
     'massless_cross_section_controls':massless_rows,
     'analytic_rest_trace_divided_by_e2y2':trace0,
     'photon_energy_for_rest_source_eV':w0,
     'photon_energy_threshold_eV':MR+MR*MR/(2*mmu),
     'cold_integral_over_rest_limit':ratio32,'quadrature_refinement_difference':abs(ratio16-ratio32),
     'cold_pair_rate_per_muon_per_s':per_muon,'ideal_steady_muon_inventory':inventory,
     'cold_pair_rate_for_ideal_inventory_per_s':per_muon*inventory,
     'free_rest_electron_min_source_momentum_eV':p_electron_min,
     'cold_source_momentum_max_eV':Pmax,
     'non_claims':['Free stationary muons; no demonstration of stopping/overlap or treatment of bound muons',
                   'Tree direct Yukawa contribution only, hypothetical mediator not empirically certified',
                   'No cooling, trapping, backgrounds or finite detector acceptance',
                   'Electron bound applies to a free initially resting electron in the two-body channel only']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
