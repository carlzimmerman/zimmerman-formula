"""PN28: bounded instantaneous transport diagnostics; no time evolution.

Dimensionless units A=Delta_m=4*pi*G=1. The ODE is the MC27 compact
Poisson equilibrium. Additional integrals independently give the required
radial heat flux and integrated cooling obligation for a prescribed theta.
"""
import json
import math
import sys
from pathlib import Path

import scipy
from scipy.integrate import quad, solve_ivp

XT = math.exp(-1.0/3.0)
CENTERS = [0.03, 0.1, 0.2, 0.249, 0.5, 0.8]

def rho(x):
    return 1/x if x <= 1 else max(3-x, 0)**2/4

def pressure(x):
    return -math.log(x)+2/3 if x <= 1 else max(3-x, 0)**3/12

def coefficient(x):
    # 5p - 3*rho*dp/drho, with the finite completion's own EOS outside.
    p = pressure(x)
    return 5*p-3 if x <= 1 else p/2

def tprime(x, xp):
    return (pressure(x)-1)*xp if x <= 1 else -xp/3

def profile(xc, tight=False):
    rc, pc, cc = rho(xc), pressure(xc), coefficient(xc)
    r0 = min(1e-7, xc*1e-5)
    def rhs(r, y):
        x,m,jc,jp = y
        return [m/r**2, r*r*rho(x), r*r*coefficient(x), r*r*pressure(x)]
    def event_x(target, terminal=False):
        def event(r,y): return y[0]-target
        event.terminal=terminal; event.direction=1
        return event
    def quarter(r,y): return rho(y[0])/rc-.25
    quarter.direction=-1
    events=[event_x(3,True),event_x(1),event_x(XT),quarter]
    initial=[xc+rc*r0*r0/6,rc*r0**3/3,cc*r0**3/3,pc*r0**3/3]
    sol=solve_ivp(rhs,[r0,1000],initial,method='DOP853',rtol=2e-12 if tight else 2e-10,
                  atol=2e-14 if tight else 2e-12,max_step=.025 if tight else .05,
                  events=events,dense_output=True)
    assert sol.success and len(sol.t_events[0])==1
    re=float(sol.t_events[0][0]); xe,me,jce,jpe=map(float,sol.y_events[0][0])
    rmatch=float(sol.t_events[1][0])
    rt=float(sol.t_events[2][0]) if len(sol.t_events[2]) else None
    rq=float(sol.t_events[3][0])
    # A direct quadrature on the dense equilibrium cross-checks the ODE integral.
    jq=quad(lambda r: r*r*coefficient(float(sol.sol(max(r,r0))[0])),0,re,
            points=[rmatch],epsabs=1e-9,epsrel=1e-9)[0]
    probes=[]
    for frac in [.001,.05,.25,.5,.9]:
        r=frac*(rt or rmatch); x,m,jc,jp=map(float,sol.sol(r)); tp=tprime(x,m/r**2)
        qc=jc/(2*r*r); qe=-qc
        probes.append(dict(r=r,x=x,T_prime=tp,q_required_compression=qc,q_required_expansion=qe,
                           kappa_required_compression=-qc/tp,kappa_required_expansion=-qe/tp))
    pole=[]
    if rt:
        x,m,jc,jp=map(float,sol.sol(rt)); xp=m/rt**2
        qexp=-jc/(2*rt**2); t2=-xp*xp/XT
        limit=abs(qexp/t2)
        for eps in [1e-3,1e-4]:
            for side in [-1,1]:
                r=rt*(1+side*eps); x,m,jc,jp=map(float,sol.sol(r)); tp=tprime(x,m/r**2)
                ke=jc/(2*r*r*tp)
                pole.append(dict(relative_offset=side*eps,expansion_kappa=ke,
                                 scaled=(rt-r)*ke,expected_limit=limit))
    rbound=min(rq,rt) if rt else None
    jcb=float(sol.sol(rbound)[2]) if rbound else None
    return dict(xc=xc,pc_over_A=pc,rho_c=rc,Cc_over_A=cc,edge_radius=re,edge_mass=me,
                matching_radius=rmatch,temperature_max_radius=rt,quarter_radius=rq,
                quarter_inside_cool_center=bool(rt and rq<=rt),
                J_C_full=jce,J_C_direct_quadrature=jq,quadrature_relative_error=abs(jq/jce-1),
                edge_required_flux_compression=jce/(2*re**2),
                full_zero_flux_cooling_power_over_4pi_A_l3_absTheta=jce/2,
                center_min_loss_over_A_absTheta=cc/2,
                center_loss_with_kappa_hat_001=cc/2+.01*rc*(pc-1),
                central_energy_loss_time_over_inverse_absTheta=3*pc/cc,
                center_expansion_kappa_hat_limit=cc/(2*rc*(pc-1)),
                protected_radius=rbound,protected_min_cooling_power_over_4pi_A_l3_absTheta=jcb/2 if jcb else None,
                probes=probes,temperature_max_pole=pole)

rows=[profile(x) for x in CENTERS]
tight=[profile(x,True) for x in [.03,.249,.8]]
convergence=[]
for b in tight:
    a=next(r for r in rows if r['xc']==b['xc'])
    convergence.append(dict(xc=a['xc'],max_relative_error=max(abs(a[k]/b[k]-1) for k in
        ['edge_radius','edge_mass','J_C_full','center_min_loss_over_A_absTheta'])))

checks={
    'compact_halos_reach_finite_zero_density_edge':all(0<r['edge_radius']<1000 and r['edge_mass']>0 for r in rows),
    'C_positive_every_tested_region':all(r['Cc_over_A']>0 and all(p['q_required_compression']>0 for p in r['probes']) for r in rows),
    'compression_requires_negative_conductivity_in_hot_pressure_center':all(all(p['kappa_required_compression']<0 for p in r['probes']) for r in rows if r['xc']<XT),
    'expansion_conductivity_changes_sign_across_temperature_max':all(all(p['expansion_kappa']>0 if p['relative_offset']<0 else p['expansion_kappa']<0 for p in r['temperature_max_pole']) for r in rows if r['xc']<XT),
    'pole_coefficient_matches':all(abs(p['scaled']/p['expected_limit']-1)<.02 for r in rows for p in r['temperature_max_pole']),
    'shallow_center_is_not_falsely_excluded_for_compression':all(p['kappa_required_compression']>0 for r in rows if r['xc']>XT for p in r['probes']),
    'quadrature_and_flux_integral_agree':max(r['quadrature_relative_error'] for r in rows)<2e-7,
    'tighter_solve_stable':max(r['max_relative_error'] for r in convergence)<2e-7,
    'full_compact_zero_flux_closure_needs_nonzero_net_exchange':all(r['edge_required_flux_compression']>0 for r in rows),
}
result={'checks':checks,'temperature_max_x':XT,'rows':rows,'convergence':convergence,
        'software':{'Python':sys.version.split()[0],'SciPy':scipy.__version__},
        'non_claims':['No time evolution or invariant pressure closure','No derived conductivity, cooling mechanism, A or central density',
                      'No exclusion of nonlocal or anisotropic transport with different dynamics or boundary conditions',
                      'Finite-boundary integral uses the completion fixed as a material EOS, an extra hypothesis']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'summary':[{k:r[k] for k in ['xc','pc_over_A','temperature_max_radius','quarter_radius',
      'center_min_loss_over_A_absTheta','full_zero_flux_cooling_power_over_4pi_A_l3_absTheta']} for r in rows]},indent=2))
assert all(checks.values())
