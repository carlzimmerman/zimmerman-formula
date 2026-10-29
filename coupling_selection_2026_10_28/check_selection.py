"""Exact CS28 identities and nine bounded one-loop UV trajectories."""
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as S

u, v, w, k = S.symbols('u v w k', positive=True)
R = S.Rational
gx, ga, gb = k*12*u, k*(u+R(21,10)*v-10*w), k*(R(21,20)*v-10*w)
flow = S.Matrix([2*u*(gx+2*ga), 2*v*(gb+2*ga), -10*k*w*w])
checks = {}

def check(name, assertion):
    checks[name] = bool(assertion)
    if not checks[name]:
        raise AssertionError(name)

check('flows_from_anomalous_dimensions', (flow - S.Matrix([
    2*k*u*(14*u+R(21,5)*v-20*w),
    2*k*v*(2*u+R(21,4)*v-30*w), -10*k*w*w])).applyfunc(S.expand) == S.zeros(3,1))
vac = {w:R(29,200)*v}
check('vacuum_beta_h', S.simplify((gx+2*ga).subs(vac)-k*(14*u+R(13,10)*v)) == 0)
check('vacuum_beta_lambda', S.simplify((gb+2*ga).subs(vac)-k*(2*u+R(9,10)*v)) == 0)
check('vacuum_yukawa_ratio_drift', S.simplify((gx-gb).subs(vac)-k*(12*u+R(2,5)*v)) == 0)
p,q = S.symbols('p q')
ratio_flow = S.Matrix([S.diff(u/w,z) for z in (u,v,w)]).dot(flow)
check('running_gauge_ray_equation', S.simplify(ratio_flow.subs({u:p*w,v:q*w})-2*k*w*p*(14*p+R(21,5)*q-15)) == 0)
ray = S.solve([14*p+R(21,5)*q-15,2*p+R(21,4)*q-25],(p,q))
check('interior_ray_is_unphysical', ray == {p:-R(25,62),q:R(3200,651)})
fixed = S.solve([14*p+R(21,5)*q-20,2*p+R(21,4)*q-30],(p,q))
check('yukawa_fixed_point_is_unphysical', fixed == {p:-R(10,31),q:R(3800,651)})
rx,ra,rb=S.symbols('rx ra rb')
rcharges=S.solve([rx+2*ra-2, rb+2*ra-2,5+5*(ra-1)+5*(rb-1)],(rx,ra,rb))
check('superconformal_linear_constraints', rcharges == {rx:0,ra:1,rb:0})
check('singlet_unitarity_violation', rcharges[rx] < R(2,3))
H=S.diag(1,1,1,1,1,-5)/S.sqrt(30)
check('embedding_generator_normalization', S.trace(H)==0 and S.trace(H*H)==1)
# Arbitrary traceless diagonal A,B suffice to check this block identity;
# H is scalar on the whole upper block, so it also holds for non-diagonal A.
a1,a2,a3,a4,b1,b2,b3,b4,x=S.symbols('a1 a2 a3 a4 b1 b2 b3 b4 x')
A=S.diag(a1,a2,a3,a4,-a1-a2-a3-a4,0)
B=S.diag(b1,b2,b3,b4,-b1-b2-b3-b4,0)
check('embedding_trace_identity', S.simplify(S.trace(A*A*(B+x*H))-S.trace(A*A*B)-x*S.trace(A*A)/S.sqrt(30))==0)
ratio=R(29,12)*k*k*u*v*(16*u+13*v)/(v+30*u)
check('embedding_stiffness_coefficient', S.simplify(ratio.subs(u,v/30)-R(5887,10800)*k*k*v*v)==0)
dx,da,db=S.symbols('dx da db')
wstar=S.solve((gx+2*ga)/k+dx+2*da,w)[0]
residual=S.expand(((gb-gx)/k+db-dx).subs(w,wstar))
check('necessary_new_anomalous_dimension', S.simplify(residual-(db-da-R(3,2)*dx-19*u-R(21,20)*v))==0)
# At w/v <=29/200 the excess over the comparison flow is nonnegative.
excess=S.expand((flow[1]-R(9,5)*k*v*v).subs(w,R(29,200)*v))
check('uv_comparison_boundary', excess==4*k*u*v)

kn=1/(16*math.pi**2)
def rhs(t,state):
    un,vn,wn=state
    return [2*kn*un*(14*un+4.2*vn-20*wn),
            2*kn*vn*(2*un+5.25*vn-30*wn),-10*kn*wn*wn]
def stop(t,state):
    return max(state)-4.0
stop.terminal=True
stop.direction=1
rows=[]
for h0 in (.3,.6,1.):
    for l0 in (.3,.6,1.):
        initial=np.array([h0*h0,l0*l0,29*l0*l0/200])
        bound=5/(9*kn*initial[1])
        sol=solve_ivp(rhs,(0,bound),initial,events=stop,rtol=2e-11,atol=2e-13,dense_output=True,max_step=.5)
        assert sol.success and len(sol.t_events[0])==1
        ts=np.linspace(0,sol.t[-1],101)
        values=sol.sol(ts)
        comparison=1/initial[1]-(9/5)*kn*ts
        assert np.max(1/values[1]-comparison)<1e-8
        assert np.all(np.diff(values[1])>0)
        assert np.all(np.diff(values[2]/values[1])<0)
        assert sol.t[-1]<bound
        rows.append({'h_star':h0,'lambda_star':l0,
                     'log_scale_to_first_squared_coupling_4':float(sol.t[-1]),
                     'one_loop_blowup_upper_bound':float(bound),
                     'endpoint_squared_couplings':values[:,-1].tolist()})
check('nine_uv_exit_trajectories',len(rows)==9)
output={'status':'passed','checks':checks,'trajectory_count':len(rows),'trajectories':rows,
        'fixed_ray':{str(z):str(val) for z,val in ray.items()},
        'fixed_yukawa_ratios':{str(z):str(val) for z,val in fixed.items()},
        'embedding_B_over_V_at_lambda_1':5887/(10800*(16*math.pi**2)**2),
        'software':{'Python':platform.python_version(),'NumPy':np.__version__,
                    'SciPy':scipy.__version__,'SymPy':S.__version__},
        'interpretation':'Exact identities plus finite one-loop ODE checks; cutoff 4 is a diagnostic, not a derived physical boundary. No selected numerical vacuum ratio.'}
text=json.dumps(output,indent=2)+'\n'
Path(sys.argv[1]).write_text(text)
print(text,end='')
