#!/usr/bin/env python3
"""Bounded exact quadratic-response checks, not a population simulation."""
import json
import platform
import sys
from pathlib import Path
import sympy as S

checks = []


def exact(name, expression):
    if isinstance(expression, S.MatrixBase):
        reduced = expression.applyfunc(S.simplify)
        ok = reduced == S.zeros(*expression.shape)
    else:
        reduced = S.factor(expression)
        ok = reduced == 0
    checks.append({"name": name, "passed": bool(ok)})
    if not ok:
        raise AssertionError((name, str(reduced)))


def positive(name, value):
    ok = bool(value > 0)
    checks.append({"name": name, "passed": ok})
    if not ok:
        raise AssertionError((name, str(value)))


# Independent Cartesian differentiation of the original conservative RWA energy.
f, beta, c, kc, mu, delta = S.symbols("f beta c kc mu delta", positive=True)
u1, ub1, u2, ub2 = ur = S.symbols("u1 ub1 u2 ub2", real=True)
v1, vb1, v2, vb2 = vi = S.symbols("v1 vb1 v2 vb2", real=True)
energy = 0
densities = []
for u, ub, v, vb in [(u1, ub1, v1, vb1), (u2, ub2, v2, vb2)]:
    ar, ai, br, bi = f + u, v, -beta + ub, vb
    n, nb = ar**2 + ai**2, br**2 + bi**2
    densities.append(n)
    energy += delta * nb + 2*c*(br*(ar**2-ai**2)+2*bi*ar*ai)
    energy += kc*n**2 - mu*(n+2*nb)
energy += 4*kc*densities[0]*densities[1]
zero = dict.fromkeys(ur + vi, 0)
stationary = {delta: 2*mu+c*f**2/beta, mu: 6*kc*f**2-2*c*beta}


def on_branch(expr):
    return expr.subs(stationary, simultaneous=False).applyfunc(S.simplify)


for index, var in enumerate(ur):
    exact("Cartesian stationarity %d" % index,
          S.simplify(S.diff(energy, var).subs(zero).subs(delta, 2*mu+c*f**2/beta)
                     .subs(mu, 6*kc*f**2-2*c*beta)))
KR = on_branch(S.hessian(energy, ur).subs(zero))
KI = on_branch(S.hessian(energy, vi).subs(zero))
T = S.Matrix([[1,0,1,0],[0,1,0,1],[1,0,-1,0],[0,1,0,-1]])/S.sqrt(2)
KRP, KIP = T*KR*T.T, T*KI*T.T
density_map = S.diag(2*f, -2*beta)
phase_map = S.diag(f, -beta)
r, v = S.Matrix([1,2]), S.Matrix([2,-1])
J = 2*c*f**2*beta
for parity, atom_entry, start in [("even",6*kc,0),("odd",-2*kc,2)]:
    expected_A = S.Matrix([[atom_entry,-c/beta],[-c/beta,c*f**2/(2*beta**3)]])
    exact(parity+" density Hessian",
          density_map.inv()*KRP[start:start+2,start:start+2]*density_map.inv()-expected_A)
    exact(parity+" phase Hessian",
          phase_map*KIP[start:start+2,start:start+2]*phase_map-J*v*v.T)
exact("real parity blocks decouple",KRP[:2,2:])
exact("phase parity blocks decouple",KIP[:2,2:])

# General exact response, including both quantum-pressure gradients.
a, b, D, da, db, z, s, mass, JJ = S.symbols("a b D da db z s mass J", real=True)
A = S.Matrix([[a,b],[b,D]])
B = z*S.diag(da,db)+JJ*v*v.T
d = da+4*db
L = D+4*a-4*b
t = a*da+D*db
B_inv = (JJ*r*r.T+z*S.diag(db,da))/(z*(JJ*d+z*da*db))
exact("phase inverse", B*B_inv-S.eye(2))
exact("phase determinant",B.det()-z*(JJ*d+z*da*db))
exact("dynamical trace",S.trace(B*A)-(JJ*L+z*t))
denominator = s**2-s*(JJ*L+z*t)+A.det()*z*(JJ*d+z*da*db)
exact("dynamical determinant",(B*A-s*S.eye(2)).det()-denominator)
numerator = 2*mass**2*z*(d*(JJ*L-s)+z*da*db*L)
chi = 2*mass**2*(r.T*(B*A-s*S.eye(2)).adjugate()*B*r)[0]/denominator
exact("conserved-density numerator",chi-numerator/denominator)
exact("static density susceptibility",(numerator/denominator).subs(s,0)-2*mass**2*L/A.det())
exact("fixed-frequency conservation limit",S.limit(numerator/denominator/z,z,0)+2*mass**2*d/s)
exact("Goldstone sound coefficient",A.det()*JJ*d/(JJ*L)-d*A.det()/L)
# The total conserved density has no k=0 conversion oscillator strength.
exact("uniform conserved density conversion overlap",(r.T*v)[0])

# Fully matched dilute neutral contact difference, without using bare-RWA coefficients.
M, m, g, lr = S.symbols("M m g lambda_rep",positive=True)
lt = lr+g**2/(M**2-4*m**2)
g_same = lr/(2*m**2)
g_cross = (lt-g**2/M**2)/m**2
exact("matched demixing interaction difference",
      g_cross-g_same-(lr/(2*m**2)+4*g**2/(M**2*(M**2-4*m**2))))

# An exact rational input from the original microscopic parameter family.
p = {"m": S.Rational(1), "M": S.Rational(201,100),
     "c3": S.Rational(1,100), "lambda_rep": S.Rational(1),
     "Delta": S.Rational(1,200)}
p["delta"] = p["M"]-2*p["m"]
p["g_squared"] = 8*p["m"]**2*p["M"]*p["c3"]**2
p["lambda_tot"] = p["lambda_rep"]+p["g_squared"]/(p["M"]**2-4*p["m"]**2)
p["kc"] = p["lambda_tot"]/(4*p["m"]**2)
p["mu"] = (p["delta"]-p["Delta"])/2
p["n"] = p["mu"]/(2*(3*p["kc"]-p["c3"]**2/p["Delta"]))
p["beta"] = p["c3"]*p["n"]/p["Delta"]
p["s"] = p["beta"]**2
p["J"] = 2*p["c3"]*p["n"]*p["beta"]
p["da"] = p["n"]/p["m"]
p["db"] = p["s"]/p["M"]
p["rho_ref"] = 2*p["m"]*(p["n"]+2*p["s"])
p["rho_inertia"] = 2*p["m"]**2*(p["da"]+4*p["db"])
positive("input density",p["n"])
positive("input detuning",p["Delta"])
positive("input bare matched repulsion",p["lambda_rep"])
exact("input atom stationarity",p["mu"]-6*p["kc"]*p["n"]+2*p["c3"]*p["beta"])
exact("input molecule stationarity",p["Delta"]*p["beta"]-p["c3"]*p["n"])
rows = []
for parity, atom_entry in [("even",6*p["kc"]),("odd",-2*p["kc"])]:
    ap = S.Matrix([[atom_entry,-p["c3"]/p["beta"]],
                   [-p["c3"]/p["beta"],p["c3"]*p["n"]/(2*p["beta"]**3)]])
    ell = (v.T*ap*v)[0]
    sound = (p["da"]+4*p["db"])*ap.det()/ell
    gap = p["J"]*ell
    positive(parity+" conversion gap squared",gap)
    positive(parity+" static determinant sign",ap.det() if parity=="even" else -ap.det())
    positive(parity+" sound sign",sound if parity=="even" else -sound)
    row = {"parity":parity,"A0":str(ap),"gap_squared":str(gap),
           "gap":str(S.N(S.sqrt(gap),18)),"sound_squared":str(S.N(sound,18)),
           "static_chi_reference":str(S.N(2*p["m"]**2*ell/ap.det(),18)),"finite_k":[]}
    for kval in [S.Rational(1,10000),S.Rational(1,1000),S.Rational(1,100),S.Rational(1,20)]:
        zz=kval**2
        ak=ap+zz*S.diag(1/(4*p["m"]*p["n"]),1/(4*p["M"]*p["s"]))
        bk=zz*S.diag(p["da"],p["db"])+p["J"]*v*v.T
        tr=S.trace(bk*ak)
        det=(bk*ak).det()
        disc=tr**2-4*det
        positive(parity+" real finite-k squared frequencies at "+str(kval),disc)
        om_lo=(tr-S.sqrt(disc))/2
        om_hi=(tr+S.sqrt(disc))/2
        row["finite_k"].append({"k":str(kval),"omega_squared_low":str(S.N(om_lo,18)),
                                "omega_squared_high":str(S.N(om_hi,18)),
                                "det_A_sign":int(S.sign(ak.det()))})
        if parity=="even":
            positive("even stable density Hessian at "+str(kval),ak.det())
            # Matrix inversion at a non-pole imaginary frequency is orthogonal to normal-mode roots.
            wE=S.Rational(1,1000)
            chi_direct=2*p["m"]**2*(r.T*(ak+wE**2*bk.inv()).inv()*r)[0]
            aa,bb,DD=ak[0,0],ak[0,1],ak[1,1]
            substitutions={a:aa,b:bb,D:DD,da:p["da"],db:p["db"],z:zz,
                           s:-wE**2,mass:p["m"],JJ:p["J"]}
            exact("finite imaginary-frequency response at "+str(kval),
                  chi_direct-(numerator/denominator).subs(substitutions))
    rows.append(row)

# Full single-component Bogoliubov spectral change of variables.
k, cs, rho = S.symbols("k cs rho",positive=True)
omega=S.sqrt(cs**2*k**2+k**4/(4*m**2))
spectral_P = rho*k**2/(4*S.pi**2*omega*S.diff(omega,k))
exact("Bogoliubov P spectral measure",spectral_P-rho*k/(4*S.pi**2*(cs**2+k**2/(2*m**2))))
exact("Bogoliubov P IR coefficient",S.limit(spectral_P/omega,k,0)-rho/(4*S.pi**2*cs**3))
exact("Bogoliubov P particle-regime coefficient",
      S.limit(spectral_P*S.sqrt(omega),k,S.oo)-rho*m*S.sqrt(2*m)/(4*S.pi**2))

result={"assertion_tested":"Exact quadratic Hessians, dynamic density response, one original-action rational parameter state, and harmonic spectral-weight identities.",
        "software":{"python":platform.python_version(),"sympy":S.__version__},
        "checks":checks,"count":len(checks),"all_passed":all(c["passed"] for c in checks),
        "parameters":{name:{"exact":str(value),"decimal":str(S.N(value,18))} for name,value in p.items()},
        "collective_blocks":rows,
        "non_claims":["No actual population or condensate established", "No all-loop or full relativistic stability theorem", "No positive static tether or rational nonlinear law constructed", "No fit or simulation"]}
out=Path(sys.argv[1])
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"checks":len(checks),"all_passed":result["all_passed"],"output":str(out)}))
