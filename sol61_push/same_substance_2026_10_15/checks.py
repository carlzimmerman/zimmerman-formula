"""Bounded self-check of one canonical complex field; no galaxy-law fit."""
import json
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

out = Path(__file__).parent / 'run_v1' / 'results.json'
r, m, lam, L, k, z = s.symbols('r m lam L k z', positive=True)
mu2 = m*m + lam*r*r
V = L + m*m*r*r/2 + lam*r**4/4
rho = s.expand(mu2*r*r/2 + V)
p = s.expand(mu2*r*r/2 - V)
D = 2*m*m + 3*lam*r*r
checks = {}
def exact(name, expr):
    checks[name] = s.simplify(expr) == 0
exact('energy', rho-L-m*m*r*r-3*lam*r**4/4)
exact('pressure', p+L-lam*r**4/4)
exact('enthalpy', rho+p-mu2*r*r)
exact('sound_speed', s.diff(p,r)/s.diff(rho,r)-lam*r*r/D)
det = (z-k*k-2*lam*r*r)*(z-k*k)-4*mu2*z
exact('mode_polynomial', det-(z*z-2*(k*k+D)*z+k*k*(k*k+2*lam*r*r)))
exact('mode_positivity_certificate', (k*k+D)**2-(D*D+4*mu2*k*k)-k*k*(k*k+2*lam*r*r))
b, q, c, u = s.symbols('b q c u', positive=True)
exact('density_relation', ((u+3*u*u/4)/b).subs({u:lam*r*r/(m*m),b:lam*L/m**4})-(rho-L)/L)
exact('coldness_bound', (u+3*u*u/4).subs(u,2*c/(1-3*c))-(2*c-3*c*c)/(1-3*c)**2)
# Uniform claims use the displayed algebraic certificates, not this finite grid.
grid = []
for lv in [0., 1e-8, 1e-3, 1.]:
    for rv in [.01, 1., 10.]:
        for kv in [0., 1e-3, 1., 10.]:
            dv = 2+3*lv*rv*rv
            # Rationalized small root avoids cancellation near k=0.
            plus = kv*kv+dv+np.sqrt(dv*dv+4*(1+lv*rv*rv)*kv*kv)
            minus = kv*kv*(kv*kv+2*lv*rv*rv)/plus
            assert minus >= 0 and plus > 0
            grid.append([lv,rv,kv,float(minus),float(plus)])
# Full Cartesian KG + Friedmann, rather than a phase-only fluid evolution.
Mp, mv, lv, vac = 100., 1., 1e-3, .1
om = np.sqrt(mv*mv+lv)
h0 = np.sqrt((.5*om*om+.5*mv*mv+lv/4+vac)/(3*Mp*Mp-1.125))
y0 = [1.,1.,0.,-1.5*h0,-om]
def rhs(t,y):
    a,x,yf,vx,vy = y
    rr=x*x+yf*yf
    en=.5*(vx*vx+vy*vy)+vac+.5*mv*mv*rr+lv*rr*rr/4
    H=np.sqrt(en/(3*Mp*Mp))
    return [a*H,vx,vy,-3*H*vx-(mv*mv+lv*rr)*x,-3*H*vy-(mv*mv+lv*rr)*yf]
def stop(t,y): return y[0]-3.
stop.terminal=True
sol=solve_ivp(rhs,[0,1500],y0,rtol=2e-10,atol=2e-12,max_step=.1,events=stop)
assert sol.success and len(sol.t_events[0])==1
a,x,yf,vx,vy=sol.y
rr=x*x+yf*yf
charge=a**3*(yf*vx-x*vy)
energy=.5*(vx*vx+vy*vy)+vac+.5*mv*mv*rr+lv*rr*rr/4
press=.5*(vx*vx+vy*vy)-vac-.5*mv*mv*rr-lv*rr*rr/4
nr=dict(scale_factor=[float(a[0]),float(a[-1])],steps=len(sol.t),
    charge_relative_drift=float(np.max(np.abs(charge/charge[0]-1))),
    max_cold_density_error=float(np.max(np.abs((energy-vac)/(mv*charge[0]/a**3)-1))),
    max_cold_pressure_fraction=float(np.max(np.abs((press+vac)/(energy-vac)))))
assert nr['charge_relative_drift'] < 1e-6
assert nr['max_cold_density_error'] < .002
assert nr['max_cold_pressure_fraction'] < .002
single_scale=[]
for qv in [.4,1.,1e5]:
    uv=2*qv/(np.sqrt(16+12*qv)+4)
    single_scale.append(dict(cold_to_vacuum=qv,u=uv,cs2=uv/(2+3*uv)))
assert all(checks.values())
result=dict(exact=checks,mode_grid_cases=len(grid),FLRW=nr,
    single_scale=single_scale,beta_bound_at_q1e5_cs2_1e6=(2e-6-3e-12)/(1e5*(1-3e-6)**2),
    software=dict(sympy=s.__version__,scipy=scipy.__version__),
    nonclaims=['No observed field identification','No MOND matching','No abundance prediction',
               'No cosmological perturbation likelihood','No nonlinear or quantum-gravity stability theorem'])
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
