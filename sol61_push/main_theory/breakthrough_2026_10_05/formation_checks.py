"""Exact local internal-state checks and bounded transition/ramp controls.
No assertion here certifies the assembled gravitational action.
"""
import hashlib,json,platform,subprocess,time,sys
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as s
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
checks={}
def check(key,value):
    checks[key]=bool(value)
    if not value: raise AssertionError(key)
n,K,I,m,Qn,c,k,w,B,F2=s.symbols('n K I m Qn c k w B F2',positive=True)
b=K/I; D=n*n*K*Qn**2/m; A=c*c*k*k; G=D*k*k
poly=(A+G-w)*(b-w)-G*b
check('perfect_square_dispersion',s.expand(poly-((A-w)*(b-w)-G*w))==0)
check('positive_root_product',s.expand(poly).coeff(w,0)==A*b)
check('positive_discriminant_identity',s.expand((A+G+b)**2-4*A*b-((A-b)**2+2*G*(A+b)+G*G))==0)
limit=b/s.Integer(9)-A/s.Integer(10)
check('ten_percent_low_branch_boundary',s.simplify(poly.subs({w:9*A/10,G:limit}))==0)
check('finite_inertia_fidelity_limit',s.simplify(D/b-n*n*I*Qn**2/m)==0)
# Explicit constrained first-order reduction: primary constraints p_lambda=0,
# p_q-J lambda=0 have nonzero bracket J, so q,p_q survive as a canonical pair.
J,pq,lam,R=s.symbols('J pq lam R',real=True)
constraint_bracket=s.Matrix([[0,J],[-J,0]])
check('multiplier_constraints_second_class',constraint_bracket.det()==J*J)
# General density-dependent internal energy, frozen B (no constitutive response).
z=s.symbols('z',real=True); N=s.symbols('N',positive=True)
Q=s.Function('Q')(N); f=s.Function('f')(z); e=s.Function('e')(N)
E=e+N*K*(z-Q)**2/2-B*f
Enn=s.diff(E,N,2); Enq=s.diff(E,N,z); Eqq=s.diff(E,z,2)
check('zero_B_schur_cancel',s.simplify((Enn-Enq**2/Eqq).subs(B,0).subs(z,Q)-s.diff(e,N,2))==0)
check('gate_curvature_is_present',s.simplify(Eqq-(N*K-B*s.diff(f,z,2)))==0)
# Local bounded scan: continuous scalar minimizer connected to Q; endpoints
# bracketed near Q, K is intentionally large so no scalar tachyon is required.
def sm(x):
    x=np.clip(x,0.,1.); return 10*x**3-15*x**4+6*x**5
def dsm(x):
    return 30*x*x*(1-x)**2 if 0<x<1 else 0.
def ddsm(x):
    return 60*x*(1-x)*(1-2*x) if 0<x<1 else 0.
kn=100.; bn=.01; inert=.01
rows=[]
for gas in (0.,.05,.5):
 for nv in np.linspace(1.01,1.99,99):
    x=nv-1; q0=sm(x); qp=dsm(x); qpp=ddsm(x)
    qv=brentq(lambda v:nv*kn*(v-q0)-bn*dsm(v),q0,min(1.,q0+.01),xtol=1e-14)
    delta=qv-q0
    eeqq=nv*kn-bn*ddsm(qv)
    eenq=kn*delta-nv*kn*qp
    eenn=gas-2*kn*delta*qp+nv*kn*qp*qp-nv*kn*delta*qpp
    schur=eenn-eenq*eenq/eeqq
    # At k=10, mass matrix diag(rho=n, internal=n I).
    kval=10.; stiff=np.array([[nv*nv*eenn*kval*kval,nv*eenq*kval], [nv*eenq*kval,eeqq]])
    inv=np.diag([1/np.sqrt(nv),1/np.sqrt(nv*inert)])
    roots=np.linalg.eigvalsh(inv@stiff@inv)
    rows.append(dict(n=nv,gas_epp=gas,q=qv,scalar_stiffness=eeqq,schur=schur,w2=roots.tolist()))
cold=[r for r in rows if r['gas_epp']==0.]
check('cold_transition_negative_schur_exists',any(r['schur']<-.001 for r in cold))
check('scalar_curvature_positive_everywhere_scanned',all(r['scalar_stiffness']>0 for r in rows))
check('warm_pressure_control_stable',all(r['schur']>0 for r in rows if r['gas_epp']==.5))
# Same full local gate: a finite tuned pressure/inertia control for positivity
# AND gas fidelity, contrasted with the pressureless failure above.
fidelity_rows=[]
for nv in np.linspace(1.01,1.99,99):
    x=nv-1; q0=sm(x); qp=dsm(x); qpp=ddsm(x)
    qv=brentq(lambda v:nv*kn*(v-q0)-bn*dsm(v),q0,min(1.,q0+.01),xtol=1e-14)
    delta=qv-q0; gas=5.; ii=1e-8
    eeqq=nv*kn-bn*ddsm(qv)
    eenq=kn*delta-nv*kn*qp
    eenn=gas-2*kn*delta*qp+nv*kn*qp*qp-nv*kn*delta*qpp
    for kval in (1.,10.):
        aa=nv*eenn*kval*kval; bb=eeqq/(nv*ii)
        mix2=nv*eenq*eenq*kval*kval/(nv*ii)
        trace=aa+bb; prod=aa*bb-mix2
        # Rationalized low root avoids catastrophic cancellation at small I.
        low=2*prod/(trace+np.sqrt((aa-bb)**2+4*mix2))
        base=nv*gas*kval*kval
        fidelity_rows.append(dict(n=nv,k=kval,I=ii,epp=gas,low_w2=low,
            high_w2=trace-low,baseline_w2=base,fractional_change=abs(low/base-1)))
check('full_gate_costed_control_positive_roots',all(r['low_w2']>0 and r['high_w2']>0 for r in fidelity_rows))
check('full_gate_costed_control_gas_fidelity',all(r['fractional_change']<.1 for r in fidelity_rows))
# Bare internal-sector ramp control ONLY: B=0 (or f prime=0 all along).
# This is not the full gate-crossing solution and is not a damping process.
ramps=[]
for W in (.1,1.,10.,100.):
    qend=1-np.sin(W)/W; vend=(1-np.cos(W))/W
    amp=np.hypot(qend-1,vend)
    exact=2*abs(np.sin(W/2))/W
    check(f'ramp_amplitude_{W}',abs(amp-exact)<1e-12)
    ramps.append(dict(omega_T=W,q_end=qend,qdot_end_over_omega=vend,
                      persistent_amplitude=amp,energy_over_nK=amp*amp/2))
# A simple arbitrary-p counterfamily after second-class reduction.
linear_energies=[dict(p=p,H=p*.1-.01*.5) for p in (-1.,-10.,-100.,-1000.)]
check('production_hamiltonian_counterfamily',all(linear_energies[i+1]['H']<linear_energies[i]['H'] for i in range(3)))
inputs=['sol61_push/main_theory/README.md','sol61_push/main_theory/switch_checks.py',
'sol61_push/CLOSURE_ROADMAP_2026-10-05.md','campaign_fresh_gravity/STANDING_2026-09-29.md',
'campaign_fresh_gravity/CFG347_first_principles_switch/FROZEN_CRITERIA.md',
'campaign_fresh_gravity/CFG348_energy_reading_switch/FROZEN_CRITERIA.md',
'campaign_fresh_gravity/CFG48_gap1_switch/README.md',
'campaign_fresh_gravity/CFG48_gap1_switch/G3_history_action_causality.py',
'campaign_fresh_gravity/CFG60_dispersion_provenance/CFG60_dispersion_provenance.md']
record=dict(checks=checks,transition_scan=rows,costed_fidelity_control=fidelity_rows,ramp_controls=ramps,
production_counterfamily=linear_energies,
provenance=dict(base='a36191815030afddf1277d413f488fb0c3ac520f',observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
python=platform.python_version(),sympy=s.__version__,numpy=np.__version__,scipy=scipy.__version__,
input_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
command='python3 sol61_push/main_theory/breakthrough_2026_10_05/formation_checks.py',
run_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())),
summary=dict(cold_negative_count=int(sum(r['schur']<0 for r in cold)),cold_count=len(cold),
min_cold_schur=min(r['schur'] for r in cold),
max_costed_fidelity_change=max(r['fractional_change'] for r in fidelity_rows),
min_scalar_curvature=min(r['scalar_stiffness'] for r in rows),
min_warm_schur=min(r['schur'] for r in rows if r['gas_epp']==.5)))
result_dir=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else OUT
(result_dir/'results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(checks=checks,summary=record['summary'],ramps=ramps),indent=2))
