"""Positive interior pole-window matching and a smooth-profile error bound.

This is a controlled one-pole mathematical patch, not the full thermal
multichannel RIS subtraction. Physical profile derivatives and phase-space
boundary patches remain to be supplied.
"""
import json
import math
import sys
from pathlib import Path
from scipy.integrate import quad

out=Path(sys.argv[1]);assert out.is_dir()
p=Path(__file__).parent
parent=json.loads((p/'thermal_charge_run_002/results.json').read_text())
parameters=next(r['parameters'] for r in parent['phase_rows'] if r['parameters']['m']==.002)
m,M,g=parameters['m'],parameters['M'],parameters['g']
Gamma=g*g/(8*math.pi*M)*math.sqrt(1-4*m*m/(M*M))
a_physical=M*Gamma
L_physical=parameters['gap']/4
epsilon_physical=a_physical/L_physical
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)});assert value,name

rows=[]
for epsilon in (.01,.0001,1e-6,1e-8,epsilon_physical):
    # Normalize L=R=1. Smooth positive profile w(D)=exp(-D/L).
    a=epsilon;W=math.sqrt(a);R=1.
    theta=math.atan(W/a)
    on_weight=2*theta/math.pi
    for B in (0.,.5,-.5,3.):
        pole_delta=2*R*R*quad(lambda x:2*math.sinh(W*x/2)**2*W/(W*W*x*x+a*a),
                             0,1,epsabs=1e-16,epsrel=2e-11,limit=200)[0]
        cross_delta=-4*R*B*quad(lambda x:math.sinh(W*x)*W*W*x/(W*W*x*x+a*a),
                                0,1,epsabs=1e-16,epsrel=2e-11,limit=200)[0]
        error=pole_delta+cross_delta
        absolute_bound=math.exp(W)*(R*R+4*abs(R*B))*(W-a*theta)
        retained_pole=2*R*R*theta/a
        check('smooth matching error bound '+str((epsilon,B)),abs(error)<=absolute_bound*(1+1e-12))
        check('positive real-state weight '+str((epsilon,B)),0<on_weight<1)
        if epsilon==.01:
            # Independent direct integration of the full window after
            # D=a tan(theta), compared to matched positive background.
            fn=lambda z:2*math.cosh(a*math.tan(z))*(B*B*a/math.cos(z)**2+R*R/a)-4*R*B*math.sinh(a*math.tan(z))*math.tan(z)
            full=quad(fn,0,theta,epsabs=1e-10,epsrel=2e-12,limit=200)[0]
            matched=2*B*B*math.sinh(W)+retained_pole
            check('independent full-window integration '+str(B),abs((full-matched)-error)<1e-9)
        rows.append(dict(a_over_L=epsilon,B_times_L_over_R=B,W_over_L=W,
            real_state_spectral_weight=on_weight,exact_model_window_error=error,
            absolute_error_bound=absolute_bound,
            window_error_over_retained_pole=error/retained_pole))

Wphysical=math.sqrt(a_physical*L_physical)
check('physical chosen window inside lower threshold gap',Wphysical<parameters['gap'])
check('physical separation of width and window',Wphysical/a_physical>100)
result=dict(verdict='Positive cut collision plus retained real-state spectral weight has a bounded one-pole interior matching error under the stated smooth real-amplitude assumptions',
 physical_scales=dict(m_GeV=m,M_GeV=M,Gamma_GeV=Gamma,
     a_MGamma_GeV2=a_physical,L_assigned_gap_quarter_GeV2=L_physical,
     W_GeV2=Wphysical,W_over_gap=Wphysical/parameters['gap'],
     W_over_MGamma=Wphysical/a_physical,
     retained_real_state_weight=2/math.pi*math.atan(Wphysical/a_physical)),
 rows=rows,checks=checks,
 non_claims=['The exponential profile is a declared mathematical benchmark, not the actual thermal phase-space density',
            'Actual smoothness constants, boundary patches and overlapping source poles are not matched here',
            'Not a completed multiparticle RIS subtraction or abundance correction',
            'No global novelty or full theory closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('rows','checks')},indent=2))
print('All %d bounded matching controls passed.'%len(checks))
