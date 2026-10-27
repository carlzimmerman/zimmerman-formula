"""Exact species Ward identities and positive-charge mass dictionary checks.

Finite numerical model: complete homogeneous Fock sectors Q<=16, no spatial
continuum or irreversible capture claim. Microscopic coefficients are those
of the original Phi/X NR action, in m=1 and volume*m^3=1 units.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
import sympy as s

checks=[]
def ck(name,value,detail=None):
    checks.append(dict(name=name,passed=bool(value),detail=detail))
    if not value:raise AssertionError((name,detail))

m0,M0,g0=s.symbols('m M g',positive=True)
delta0=M0-2*m0
ck('source propagator frequency decomposition',s.simplify(1/(4*m0*m0-M0*M0)-(1/(2*m0-M0)-1/(2*m0+M0))/(2*M0))==0)
correction=g0*g0/(2*M0*(M0+2*m0))
ck('RWA minus matched threshold coefficient',s.simplify(g0*g0/(M0*M0-4*m0*m0)-g0*g0/(2*M0*(M0-2*m0))-correction)==0)
ck('charge weighted rest-mass excess',s.expand(m0*s.Symbol('nd')+M0*s.Symbol('ns')-(m0*(s.Symbol('nd')+2*s.Symbol('ns'))+delta0*s.Symbol('ns')))==0)

m=1.;u=.02;M=2*math.sqrt(1+u*u)
delta=2*u*u/(math.sqrt(1+u*u)+1) # stable M-2m with m=1
g=.002168;gap=4*u*u;lambda_min=g*g/gap
lambda_rep=2*lambda_min;lambda_tot=lambda_min+lambda_rep
c3=g/(2*math.sqrt(2*M));kc=lambda_tot/4
k_eff_RWA=kc-c3*c3/delta
lambda_RWA=4*k_eff_RWA
negative_frequency_shift=g*g/(2*M*(M+2))
ck('positive finite-regulator coefficient',k_eff_RWA>0)
ck('RWA threshold reconciliation',math.isclose(lambda_RWA-lambda_rep,negative_frequency_shift,rel_tol=3e-10))
ck('matched threshold after negative-frequency term',math.isclose(lambda_RWA-negative_frequency_shift,lambda_rep,rel_tol=2e-14))

Qmax=16
states=[(n,b) for b in range(Qmax//2+1) for n in range(Qmax-2*b+1)]
index={q:i for i,q in enumerate(states)};N=len(states)
a=np.zeros((N,N));b=np.zeros((N,N))
for j,(n,x) in enumerate(states):
    if n:a[index[(n-1,x)],j]=math.sqrt(n)
    if x:b[index[(n,x-1)],j]=math.sqrt(x)
nd=a.T@a;ns=b.T@b;Q=nd+2*ns
A=b.T@a@a
pair=a.T@a.T@a@a
H=delta*ns+c3*(A+A.T)+kc*pair
R=1j*c3*(A-A.T)
rho_rest=m*nd+M*ns
def dot(op):return 1j*(H@op-op@H)
def norm(op):return float(np.max(abs(op)))
ck('complete sector cardinality',N==81)
ck('weighted charge operator is exact',norm(Q-np.diag([n+2*x for n,x in states]))<1e-13)
ck('Hermitian Hamiltonian and reaction source',norm(H-H.T)<1e-14 and norm(R-R.conj().T)<1e-14)
ck('species daughter Ward source',norm(dot(nd)-2*R)<1e-12)
ck('species source Ward sink',norm(dot(ns)+R)<1e-12)
ck('conserved total U1 charge',norm(dot(Q))<1e-12)
ck('rest mass change is detuning work',norm(dot(rho_rest)+delta*R)<1e-12)
interaction=H-delta*ns
ck('interaction energy compensates rest mass work',norm(dot(interaction)-delta*R)<1e-12)
B=b+(c3/delta)*(a@a)
square=delta*B.T@B+k_eff_RWA*pair
ck('positive square identity at fixed regulator',norm(H-square)<1e-12)
ck('nonnegative excess Hamiltonian eigenvalues',float(np.linalg.eigvalsh(H).min())>-1e-12)

phase_rows=[]
for sign in [-1,1]:
    vec=np.zeros(N,dtype=complex)
    vec[index[(2,0)]]=1/math.sqrt(2)
    vec[index[(0,1)]]=sign*1j/math.sqrt(2)
    expect=lambda op:float(np.vdot(vec,op@vec).real)
    phase_rows.append(dict(sign=sign,daughter_number=expect(nd),source_number=expect(ns),
                           charge=expect(Q),excess_energy=expect(H),reaction_source=expect(R)))
ck('same densities and energy do not fix coherent exchange',
   all(math.isclose(phase_rows[0][k],phase_rows[1][k],rel_tol=1e-13,abs_tol=1e-14) for k in ['daughter_number','source_number','charge','excess_energy']))
ck('relative phase reverses source at same densities',phase_rows[0]['reaction_source']*phase_rows[1]['reaction_source']<0)

trajectories=[]
for charge in [2,4,8,16]:
    ids=[i for i,(n,x) in enumerate(states) if n+2*x==charge]
    HH=H[np.ix_(ids,ids)];ev,U=np.linalg.eigh(HH)
    initial=np.zeros(len(ids),dtype=complex);initial[ids.index(index[(0,charge//2)])]=1
    coeff=U.T@initial;energies=[];charges=[];rest=[];other=[];rates=[]
    for t in np.linspace(0,20000,101):
        v=U@(np.exp(-1j*ev*t)*coeff)
        ex=lambda op:float(np.vdot(v,op[np.ix_(ids,ids)]@v).real)
        energies.append(float(np.vdot(v,HH@v).real));charges.append(ex(Q))
        rest.append(ex(rho_rest));other.append(ex(interaction));rates.append(ex(R))
    ck('finite-sector energy conservation Q='+str(charge),max(energies)-min(energies)<1e-12)
    ck('finite-sector charge conservation Q='+str(charge),max(abs(x-charge) for x in charges)<1e-11)
    ledger=np.asarray(rest)+np.asarray(other)
    ck('rest-plus-interaction energy ledger Q='+str(charge),float(np.ptp(ledger))<1e-11)
    bound=delta/(2+delta)
    max_error=max((rr-m*qq)/rr for rr,qq in zip(rest,charges))
    ck('positive-sector charge-mass dictionary bound Q='+str(charge),max_error<=bound+2e-14)
    trajectories.append(dict(charge=charge,sector_dimension=len(ids),max_relative_rest_vs_charge_mass=max_error,
                             energy_variation=max(energies)-min(energies),min_reaction_source=min(rates),max_reaction_source=max(rates)))

out=dict(claim_id='CE-PARTICLE-CURRENT-2026-10-18',n_checks=len(checks),checks=checks,
         parameters=dict(m=m,M=M,u_star=u,g=g,delta=delta,c3=c3,kc=kc,lambda_rep=lambda_rep,lambda_tot=lambda_tot,
                         lambda_NR_RWA=lambda_RWA,negative_frequency_matching_shift=negative_frequency_shift,
                         relative_RWA_shift_vs_lambda_rep=(lambda_RWA-lambda_rep)/lambda_rep),
         density_dictionary=dict(rho_rest='m q + delta n_source',q='n_daughter+2n_source',
                                 positive_branch_relative_error_max=delta/M,
                                 neutral_counterexample='n_particle=n_antiparticle=1 gives net charge0 and positive rest mass2m'),
         opposite_coherent_sources=phase_rows,finite_sector_trajectories=trajectories,
         non_claims=['Homogeneous finite-volume NR sectors are not continuum decay or irreversible capture','RWA regulated Hamiltonian is not fully relativistic threshold matching','Positive charge density is not total inertial mass of a neutral particle-antiparticle bath','Source/daughter species are not settled/free populations','No rational polarization energy, MOND law, physical halo or cosmological preparation derived'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
