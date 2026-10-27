"""Bounded exact and finite checks for the rational constitutive completion.

This script tests explicitly changed dipole ensembles as such. It does not
identify those ensembles with the original Phi/X carrier. All matrix sectors
are complete homogeneous two-mode Q sectors, not continuum spatial solutions.
"""
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as s

checks = []


def check(name, passed, detail=None):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})
    if not passed:
        raise AssertionError((name, detail))


a, E, z, L, ell, K, p = s.symbols("a E z L ell K p", positive=True)
pmax = a / K
w = pmax * a * z / (a*a + z*z)**s.Rational(3, 2)
primitive = a / (a*a-E*E) * s.sqrt((z*z+E*E)/(z*z+a*a))
integrand = a*z / ((a*a+z*z)**s.Rational(3, 2)*s.sqrt(z*z+E*E))
check("elementary spectral antiderivative", s.simplify(s.diff(primitive, z)-integrand) == 0)
check("full spectral integral endpoint difference", s.simplify(a/(a*a-E*E)*(1-E/a)-1/(a+E)) == 0)
check("removable E=a integral", s.integrate(a*z/(a*a+z*z)**2, (z, 0, s.oo)) == 1/(2*a))
check("positive total gap weight", s.integrate(w, (z, 0, s.oo)) == pmax)
check("linear susceptibility moment", s.integrate(w/z, (z, 0, s.oo)) == pmax/a)
check("soft-gap linear weight", s.limit(w/z, z, 0) == pmax/(a*a))
check("large-gap inverse-square weight", s.limit(w*z*z, z, s.oo) == pmax*a)

F = (a*E-a*a*s.log(1+E/a))/K
response = a*E/(K*(a+E))
W = (-a*K*p-a*a*s.log(1-K*p/a))/K
field_of_p = a*K*p/(a-K*p)
check("F derivative is response", s.simplify(s.diff(F,E)-response) == 0)
check("W derivative is inverse field", s.simplify(s.diff(W,p)-field_of_p) == 0)
check("Legendre pair", s.simplify((E*p-F-W).subs(p, response)) == 0)
check("residual derivative", s.simplify(s.diff(W-K*p*p/2,p)-(K*p)**2/(a-K*p)) == 0)
check("small field coefficients", s.simplify(s.series(response,E,0,5).removeO()-(E/K-E**2/(K*a)+E**3/(K*a*a)-E**4/(K*a**3))) == 0)
check("large field inverse first power deficit", s.limit(E*(pmax-response),E,s.oo) == a*pmax)
check("small polarization cubic residual", s.limit((W-K*p*p/2)/p**3,p,0) == K*K/(3*a))

w0 = pmax*a*z*(4*a*a+z*z)/(a*a+z*z)**s.Rational(5, 2)
check("isotropic inverse density identity", s.simplify(w0-(3*w+z*s.diff(w,z))) == 0)
check("isotropic inventory is twice saturation", s.integrate(w0, (z,0,s.oo)) == 2*pmax)
t_angle = s.symbols("t_angle", positive=True)
# t_angle=tan(theta), 0<theta<pi/2. Work in the positive tangent
# coordinate so SymPy does not extend sqrt(cos(theta)^2) outside that chart.
check("geometric parameterization in positive tangent chart", s.simplify(w.subs(z,a*t_angle)*a-pmax*t_angle/(1+t_angle*t_angle)**s.Rational(3,2)) == 0)

R = s.sqrt((z*z+E*E)/(z*z+a*a))
cutoff = pmax*E*a/(a*a-E*E)*(R.subs(z,L)-R.subs(z,ell))
cutoff_a = pmax*a*a/2*(1/(ell*ell+a*a)-1/(L*L+a*a))
check("cutoff E=a removable limit", s.simplify(s.limit(cutoff,E,a)-cutoff_a) == 0)
weight_primitive = -pmax*a/s.sqrt(a*a+z*z)
check("cutoff weight primitive", s.simplify(s.diff(weight_primitive,z)-w) == 0)
m2_primitive = pmax*a*(s.sqrt(a*a+z*z)+a*a/s.sqrt(a*a+z*z))
check("cutoff second-moment primitive", s.simplify(s.diff(m2_primitive,z)-w*z*z) == 0)

# Deterministic independent high-precision quadrature, including E=a and
# nonuniform logarithmic regimes; exact proof is supplied in the note.
mp.mp.dps = 50
field_grid = [mp.mpf(t) for t in ["0.0001", "0.01", "0.1", "0.5", "1", "2", "10", "100"]]
quad_rows = []
for ee in field_grid:
    # z=tan(theta) makes the compact integration weight sin(theta).
    val = mp.quad(lambda th: mp.sin(th)*ee/mp.sqrt(mp.tan(th)**2+ee**2),
                  [0, mp.atan(ee), mp.pi/4, mp.pi/2] if ee < 1 else
                  [0, mp.pi/4, mp.atan(ee), mp.pi/2])
    exact = ee/(1+ee)
    rel = abs(val-exact)/exact
    check("continuum quadrature E="+str(ee), rel < mp.mpf("1e-42"), str(rel))
    quad_rows.append({"E_over_a":float(ee), "response_over_pmax":float(val), "relative_error":str(rel)})

# Check the isotropic random-axis inversion by a separate order of integration.
isotropic_rows = []
for ee in [mp.mpf("0.1"),mp.mpf("1"),mp.mpf("10")]:
    def orientation_kernel(zz):
        # Exact average int_0^1 c^2 E/sqrt(z^2+E^2 c^2) dc.
        if zz == 0:
            return mp.mpf("0.5")
        return (ee*mp.sqrt(ee*ee+zz*zz)-zz*zz*mp.asinh(ee/zz))/(2*ee*ee)
    val = mp.quad(lambda zz: zz*(4+zz*zz)/(1+zz*zz)**mp.mpf("2.5")*orientation_kernel(zz),
                  [0,ee,1,mp.inf] if ee < 1 else [0,1,ee,mp.inf])
    rel = abs(val-ee/(1+ee))/(ee/(1+ee))
    check("isotropic axis response E="+str(ee), rel < mp.mpf("1e-40"), str(rel))
    isotropic_rows.append({"E_over_a":float(ee),"response_over_pmax":float(val),"relative_error":str(rel)})

def cut_value(ee, lo, hi):
    if ee == 1:
        return mp.mpf("0.5")*(1/(1+lo*lo)-1/(1+hi*hi))
    return ee/(1-ee*ee)*(mp.sqrt((hi*hi+ee*ee)/(hi*hi+1))-mp.sqrt((lo*lo+ee*ee)/(lo*lo+1)))

cutoff_rows = []
for lo,hi in [(mp.mpf("0"),mp.mpf("10")),(mp.mpf("0.01"),mp.mpf("100")),(mp.mpf("0.1"),mp.mpf("10"))]:
    for ee in [mp.mpf(t) for t in ["0.001","0.1","1","10","1000"]]:
        val = cut_value(ee,lo,hi)
        quadrature = mp.quad(lambda zz: zz/(1+zz*zz)**mp.mpf("1.5")*ee/mp.sqrt(zz*zz+ee*ee), [lo,hi])
        check("finite cutoff quadrature "+str((lo,hi,ee)), abs(val-quadrature)<mp.mpf("1e-43"))
        target = ee/(1+ee)
        irbound = 1-1/mp.sqrt(1+lo*lo)
        uvbound = ee/(2*hi*hi)
        check("cutoff absolute error bound "+str((lo,hi,ee)), -mp.mpf("1e-45") <= target-val <= irbound+uvbound+mp.mpf("1e-43"))
        cutoff_rows.append({"IR_gap_over_a":float(lo),"UV_gap_over_a":float(hi),"E_over_a":float(ee),
                            "response_over_pmax":float(val),"target":float(target),"relative_deficit":float((target-val)/target)})

# Finite Q original two-mode Hamiltonian in the same stated RWA convention as
# the original regulated carrier. Each sector j=0,...,floor(Q/2) is complete.
u = 0.02
mass = 1.0
M = 2*math.sqrt(1+u*u)
delta = 2*u*u/(math.sqrt(1+u*u)+1)
g = 0.002168
lambda_rep = 2*g*g/(4*u*u)
lambda_tot = lambda_rep+g*g/(4*u*u)
kc = lambda_tot/4
c3 = g/(2*math.sqrt(2*M))
sector_rows = []
for Q in [2,4,8,16]:
    J = Q//2
    js = np.arange(J+1)
    na = Q-2*js
    H = np.diag(delta*js+kc*na*(na-1))
    for j in range(J):
        t = c3*math.sqrt((j+1)*(Q-2*j)*(Q-2*j-1))
        H[j,j+1] = H[j+1,j] = t
    ev,U = np.linalg.eigh(H)
    check("complete fixed Q sector "+str(Q), H.shape == (Q//2+1, Q//2+1))
    # Uniform leading NR gravity is m Phi Q times identity.
    probe = .173
    evg,Ug = np.linalg.eigh(H+mass*probe*Q*np.eye(J+1))
    overlap = abs(float(np.dot(U[:,0],Ug[:,0])))
    check("uniform fixed-Q gravitational eigenstate "+str(Q), abs(overlap-1)<3e-14)
    check("uniform fixed-Q gravitational eigenvalue "+str(Q), abs((evg[0]-ev[0])-mass*probe*Q)<2e-14)
    # Properly redshift the complete Hamiltonian for a constant lapse.
    lapse=1.021
    evN,UN=np.linalg.eigh(lapse*(mass*Q*np.eye(J+1)+H))
    check("constant lapse full Hamiltonian eigenstate "+str(Q), abs(abs(float(np.dot(U[:,0],UN[:,0])))-1)<3e-14)
    # A hypothetical differential source h*j is kept explicitly distinct.
    def occupation(h):
        e,v=np.linalg.eigh(H+h*np.diag(js))
        return float(np.dot(v[:,0]*v[:,0],js))
    bias=delta-2*kc
    if Q==2:
        t=math.sqrt(2)*c3
        for hh in [-.1,-.01,0,.01,.1]:
            exact=.5*(1-(bias+hh)/math.sqrt((bias+hh)**2+4*t*t))
            check("Q2 exact square-root occupation h="+str(hh), abs(occupation(hh)-exact)<5e-15)
    high_E=10.0
    deficiency=J-occupation(-high_E)
    last_t=c3*math.sqrt(J*(Q-2*(J-1))*(Q-2*(J-1)-1))
    prediction=last_t*last_t/high_E**2
    # Endpoint perturbation is independently checked at a clearly large field;
    # 1/E corrections to the asymptotic coefficient are allowed by this gate.
    check("finite inventory inverse-square saturation Q="+str(Q), abs(deficiency/prediction-1)<.02)
    sector_rows.append({"Q":Q,"dimension":J+1,"nonzero_gap":float(ev[1]-ev[0]),
                        "uniform_gravity_overlap":overlap,"source_occupation_at_zero":occupation(0),
                        "favorable_probe_E":high_E,"occupation_deficit":deficiency,
                        "asymptotic_deficit":prediction})

# Classical bounded two-state thermal occupancy is logistic in a gravitational
# energy source. Rational Langmuir form requires activity E/a, hence log source.
x = s.symbols("x", real=True)
check("thermal symmetric dipole oddness", s.simplify(s.tanh(-x)+s.tanh(x)) == 0)
check("classical orientation weak-field coefficients", s.series(s.coth(x)-1/x,x,0,6).removeO() == x/3-x**3/45+2*x**5/945)

out = {
    "claim_id":"CE-GRAV-RATIONAL-2026-10-19",
    "n_checks":len(checks),"checks":checks,
    "continuum_gap_density":"w(Delta)=pmax*a*Delta/(a^2+Delta^2)^(3/2)",
    "isotropic_axis_gap_density":"w0(Delta)=pmax*a*Delta*(4*a^2+Delta^2)/(a^2+Delta^2)^(5/2)",
    "continuum_quadrature":quad_rows,"isotropic_quadrature":isotropic_rows,
    "cutoff_comparisons":cutoff_rows,"fixed_Q_sectors":sector_rows,
    "carrier_parameters":{"m":mass,"M":M,"delta":delta,"g":g,"c3":c3,"kc":kc,"lambda_rep":lambda_rep,"lambda_tot":lambda_tot},
    "non_claims":["Changed dipole ensemble is not derived from the original scalar action", "No a0 or Newton-constant calibration is predicted", "No original particle gravitational internal dipole is established", "Fixed-Q matrices are homogeneous RWA finite-mode models, not spatial gravity solutions", "Numerical quadrature is finite evidence; elementary integral and inversion are proved in the note"]
}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"n_checks":len(checks),"all_passed":True,"fixed_Q_sectors":sector_rows},indent=2))
