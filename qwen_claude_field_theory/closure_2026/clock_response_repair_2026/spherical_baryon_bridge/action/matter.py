#!/usr/bin/env python3
"""Spherical irrotational dust: exact action, sources and moving evolution."""
import json
import platform
import time
import sympy as s

start = time.monotonic()
t, r = s.symbols("t r", positive=True)
N,v,A,R,rho,theta,p = [s.Function(z)(t,r) for z in ("N","v","A","R","rho","theta","p")]
q = s.diff(theta,r)
tht = s.diff(theta,t)
U = (tht-v*q)/N
Z = q/A
Cnorm = U**2-Z**2-1
Ls = rho*Cnorm/2
L = N*A*R**2*Ls
checks = {}


def check(name, residual):
    checks[name] = s.simplify(s.expand(residual)) == 0
    if not checks[name]:
        raise AssertionError(name+": "+str(s.simplify(residual)))


def euler(Lag, f):
    return s.diff(Lag,f)-s.diff(s.diff(Lag,s.diff(f,t)),t)-s.diff(s.diff(Lag,s.diff(f,r)),r)


sources = {N:-A*R**2*rho*(U**2+Z**2+1)/2,
           v:-A*R**2*rho*U*q,
           A:N*R**2*rho*(U**2+Z**2-1)/2,
           R:N*A*R*rho*Cnorm}
for field,expected in sources.items():
    check("full_action_source_"+str(field.func),euler(L,field)-expected)
check("multiplier_normalization",euler(L,rho)-N*A*R**2*Cnorm/2)
pd = A*R**2*rho*U
cd = -v-N*q/(A**2*U)
jd = -v*pd-N*R**2*rho*q/A
check("current_time",s.diff(L,tht)-pd)
check("current_radial",s.diff(L,q)-jd)
check("current_advection",jd-pd*cd)
check("theta_continuity",euler(L,theta)+s.diff(pd,t)+s.diff(jd,r))

# Independent metric variation through the stress tensor, including the
# off-shell L_s g^{mu nu} term; angular stress is L_s before normalization.
g = s.Matrix([[-N**2+A**2*v**2,A**2*v],[A**2*v,A**2]])
gi = s.Matrix([[-1/N**2,v/N**2],[v/N**2,1/A**2-v**2/N**2]])
grad = gi*s.Matrix([tht,q])
T = rho*(grad*grad.T)+Ls*gi
for field in (N,v,A):
    via_T = N*A*R**2*sum(T[i,j]*s.diff(g[i,j],field) for i in range(2) for j in range(2))/2
    check("stress_tensor_source_"+str(field.func),via_T-sources[field])
check("stress_tensor_source_R",2*N*A*R*Ls-sources[R])
check("four_velocity_normalization",(grad.T*g*grad)[0]+1+Cnorm)

# Choose future branch U>0. Canonical reduction is performed by eliminating
# rho from p=AR²rho U and its multiplier constraint, not by substituting L=0.
U0 = s.sqrt(1+q**2/A**2)
H = p*(v*q+N*U0)
Lc = p*tht-H
constraint = {tht:v*q+N*U0,rho:p/(A*R**2*U0)}
for field in (N,v,A,R):
    check("canonical_source_"+str(field.func),euler(Lc,field)-sources[field].subs(constraint,simultaneous=True))
check("canonical_theta_evolution",euler(Lc,p)-(tht-v*q-N*U0))
check("canonical_mass_evolution",euler(Lc,theta)+s.diff(p,t)-s.diff(p*(v+N*q/(A**2*U0)),r))
qdot = s.diff(v*q+N*U0,r)
transport_rhs = q*s.diff(v,r)+U0*s.diff(N,r)-N*q**2*s.diff(A,r)/(A**3*U0)
check("radial_momentum_transport",qdot-(v+N*q/(A**2*U0))*s.diff(q,r)-transport_rhs)

# Independent FLRW rest-mass and stress-tensor background conservation.
a,n,d = (s.Function(z)(t) for z in ("a","n","d"))
mass_balance = s.diff(a**3*d,t)/a**3
Ttt = d/n**2
div_T_t = s.diff(Ttt,t)+(s.diff(n,t)/n+3*s.diff(a,t)/a)*Ttt+s.diff(n,t)/n*Ttt
check("FLRW_stress_vs_mass_conservation",n**2*div_T_t-mass_balance)
check("FLRW_dilution",mass_balance-s.diff(d,t)-3*s.diff(a,t)*d/a)

# Exact moving radial geodesic dust in a prescribed Minkowski shell t>r>0.
# This is a matter-kinematics benchmark, not an Einstein+dust solution.
m = s.symbols("m", positive=True)
sigma = s.sqrt(t**2-r**2)
theta_m, rho_m = sigma,m/sigma**3
Um, qm = s.diff(theta_m,t),s.diff(theta_m,r)
pm, jm = r**2*rho_m*Um,-r**2*rho_m*qm
eps, flux, stress = rho_m*Um**2,-rho_m*Um*qm,rho_m*qm**2
check("moving_Minkowski_normalization",Um**2-qm**2-1)
check("moving_Minkowski_mass",s.diff(pm,t)+s.diff(jm,r))
check("moving_Minkowski_energy",s.diff(eps,t)+s.diff(r**2*flux,r)/r**2)
check("moving_Minkowski_momentum",s.diff(flux,t)+s.diff(r**2*stress,r)/r**2)
check("moving_Minkowski_velocity",jm/pm-r/t)

# Deliberately wrong frozen/rest-density assumptions must leave nonzero terms.
nr, d0, z0 = s.symbols("N_r rho_0 Z_0", nonzero=True)
negative = {
    "frozen_radial_momentum": -nr,
    "rest_density_as_normal_density": -A*R**2*d0*z0**2,
    "constant_rest_density_in_expanding_FLRW": 3*s.diff(a,t)*d0/a,
}
check("frozen_dust_residual_from_actual_equation",(-transport_rhs).subs({q:0,s.diff(v,r):0,s.diff(N,r):nr})+nr)
check("rest_density_error_from_actual_source",(sources[N]+A*R**2*rho).subs({tht:v*q+N*U0})+A*R**2*rho*Z**2)
check("frozen_FLRW_density_from_actual_balance",mass_balance.subs(d,d0).doit()-negative["constant_rest_density_in_expanding_FLRW"])
check("initial_rest_acceleration",s.diff(-q/(A*U0),t).subs({q:0,s.diff(q,t):nr},simultaneous=True)/N+nr/(N*A))
if any(s.simplify(value)==0 for value in negative.values()):
    raise AssertionError("Negative control accidentally passed")
print(json.dumps({"status":"passed","checks":checks,"check_count":len(checks),
    "negative_controls_rejected":{key:str(value) for key,value in negative.items()},
    "domain":"exact local smooth spherical dust before caustics; N,A,R>0, rho>=0, U>0",
    "python":platform.python_version(),"sympy":s.__version__,
    "runtime_seconds":round(time.monotonic()-start,3),
    "non_claims":["no static finite-mass dust equilibrium","no multi-stream matter closure",
                  "no Einstein solution inferred from prescribed-metric matter benchmark"]},indent=2))
