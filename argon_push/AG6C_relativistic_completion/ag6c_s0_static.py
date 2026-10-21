"""AG6C gate S0 (S0.1, S0.2, S0.3, S0.5): does candidate C1 ('dielectric cold dust') reduce to PAPER49's static action?

Criteria: FROZEN_CRITERIA.md (committed alone first, e926935c3).
C1 static equations (isolated or with a uniform rigid neutralising background rhobar):
  Poisson  lap Phi = K (rho_b + rho_c - rhobar);  Gauss  div D = K (rho_c - rhobar);
  dust at rest  grad Phi = E_vec - gamma grad rho_c;  E_vec curl-free;  D = Dfun(|E|) E/|E|,  Dfun(E) = a0 E/(a0 + E).
PAPER49 (L49) Euler-Lagrange equations:
  div(grad Phi - K P) = K rho_b;   grad Phi - K P = R(u) P/|P| - gamma lap P,  u = K|P|,  R(u) = u^2/(a0 - u).
Run: python3 ag6c_s0_static.py      (AG6C_MUTATE=1: charge ratio q^2 = 1.01 and the W_full double count; must fail)
"""
import json
import os
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

MUT = os.environ.get("AG6C_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag6c_s0_static{SUF}.out"), "w")
RES = {"lane": "AG6C", "script": "ag6c_s0_static", "mutate": MUT, "checks": {}, "numbers": {}}
FAILS = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


P("AG6C S0  static weak-field match of C1 (dielectric cold dust) to PAPER49" + ("  [MUTATE]" if MUT else ""))
a0, K = sp.symbols("a0 K", positive=True)
E, u, e = sp.symbols("E u e", positive=True)
qq = sp.Rational(101, 100) if MUT else sp.Integer(1)   # charge ratio squared q^2 (BPS = 1)
q = sp.sqrt(qq)

# ---------------------------------------------------------------- S0.1 Legendre duality
P("\nS0.1  L_dark(E) = (a0^2/K)[e - ln(1+e)] is the Legendre dual of W_full")
W_full = (a0 ** 2 / K) * (-u / a0 - sp.log(1 - u / a0))          # K dW_full/du = a0 u/(a0-u)
chk_W = sp.simplify(K * sp.diff(W_full, u) - a0 * u / (a0 - u))
L_dark = (a0 ** 2 / K) * (E / a0 - sp.log(1 + E / a0))
Dfun = sp.simplify(K * sp.diff(L_dark, E))                      # D in acceleration units
Ham = sp.simplify(E * Dfun / K - L_dark)                         # energy density E.D - L
if MUT:  # double count: pair the completed square with W_full instead of W_rem -> effective E(u) = u + K W_full'(u)
    Efun_49 = u + a0 * u / (a0 - u)
else:
    Efun_49 = u + u ** 2 / (a0 - u)                               # PAPER49: |grad Phi| = u + R(u) at gamma = 0
s01a = sp.simplify(Dfun - a0 * E / (a0 + E))
s01b = sp.simplify(Ham - W_full.subs(u, Dfun))
s01c = sp.simplify(Efun_49.subs(u, Dfun) - E)                    # E(D(E)) = E  <=>  dual matches L49's tether
P(f"  K dW_full/du - a0 u/(a0-u) = {chk_W}")
P(f"  D(E) = K dL/dE = {Dfun};   D - a0E/(a0+E) = {s01a}")
P(f"  (E.D - L) - W_full(D) = {s01b}")
P(f"  L49 tether |grad Phi| = u + R(u) at u = D(E), minus E = {s01c}")
check("S0.1 Legendre identity", chk_W == 0 and s01a == 0 and s01b == 0 and s01c == 0,
      "D = a0E/(a0+E), E.D - L = W_full(D), and L49's u + R(u) inverts D(E) exactly" if (s01c == 0)
      else f"mismatch {s01c}")

# ---------------------------------------------------------------- S0.2 field-equation map, any geometry
P("\nS0.2  field equations for an ARBITRARY non-spherical potential (gamma = 0)")
x, y, z = sp.symbols("x y z", real=True)
# a non-spherical test potential: two softened deep-ish masses + a uniform external field (generic, no symmetry)
r1 = sp.sqrt((x - 1) ** 2 + y ** 2 + z ** 2 + sp.Rational(1, 4))
r2 = sp.sqrt((x + sp.Rational(1, 2)) ** 2 + (y - sp.Rational(1, 3)) ** 2 + z ** 2 + sp.Rational(1, 5))
Phi = -1 / r1 - sp.Rational(1, 2) / r2 + sp.Rational(3, 10) * z + sp.Rational(1, 7) * sp.log(r1 * r2)
gradPhi = sp.Matrix([sp.diff(Phi, v) for v in (x, y, z)])
gmag = sp.sqrt(sum(c ** 2 for c in gradPhi))
# C1: dust at rest => E_vec = grad Phi; constitutive D = q-scaled: Gauss div D = q K rho_c, force q E_vec
#   with charge q: grad Phi = q E_vec, |D| = Dfun(|E_vec|) => K P := D/q (so that div(KP) = K rho_c)
Evec = gradPhi / q
Dvec = Dfun.subs(E, gmag / q) * Evec / (gmag / q)
KP_C1 = Dvec / q
uC1 = sp.sqrt(sum(c ** 2 for c in KP_C1))
# L49 P-equation residual evaluated on C1's configuration
Rexpr = uC1 ** 2 / (a0 - uC1)
res_vec = gradPhi - KP_C1 - Rexpr * KP_C1 / uC1
R_ = sp.Rational
# exact rational points and constants (first run used Python floats, which capped the test at double precision)
pts = [(R_(3, 10), R_(-7, 10), R_(2, 5)), (R_(2), R_(1, 2), R_(-11, 10)), (R_(-13, 10), R_(17, 10), R_(1, 5)),
       (R_(1, 20), R_(1, 50), R_(3)), (R_(-2, 5), R_(-3, 10), R_(-3, 5))]
subs_num = {a0: sp.Integer(1), K: sp.Integer(1)}
maxres = 0.0
for pt in pts:
    sv = {x: pt[0], y: pt[1], z: pt[2], **subs_num}
    rv = [float(sp.N(c.subs(sv), 40)) for c in res_vec]
    gv = float(sp.N(gmag.subs(sv), 40))
    maxres = max(maxres, max(abs(t) for t in rv) / gv)
P(f"  max |L49 P-eq residual| / |grad Phi| on C1's field at 5 generic points (40-digit, exact rational inputs): {maxres:.3e}")
# the divergence equation: L49's rho_b := div(grad Phi - K P)/K  vs  C1's rho_b := (lap Phi - K rho_c)/K, K rho_c = div(D)/q
rho_b_49 = sum(sp.diff(gradPhi[i] - KP_C1[i], v) for i, v in enumerate((x, y, z)))
rho_b_C1 = sum(sp.diff(gradPhi[i], v) for i, v in enumerate((x, y, z))) - sum(
    sp.diff(Dvec[i] / q, v) for i, v in enumerate((x, y, z)))
maxdiv = 0.0
for pt in pts:
    sv = {x: pt[0], y: pt[1], z: pt[2], **subs_num}
    maxdiv = max(maxdiv, abs(float(sp.N((rho_b_49 - rho_b_C1).subs(sv), 40))))
P(f"  max |rho_b(L49) - rho_b(C1)| at the same points: {maxdiv:.3e}")
ok02 = maxres < 1e-20 and maxdiv < 1e-20
check("S0.2 EL map at gamma = 0 (any geometry)", ok02,
      f"P-eq residual {maxres:.1e}, divergence-eq difference {maxdiv:.1e} (40-digit arithmetic, rational inputs)")
RES["numbers"]["S0.2"] = dict(max_peq_residual=maxres, max_div_diff=maxdiv)

# ---------------------------------------------------------------- S0.3 stiffness operators
P("\nS0.3  stiffness: EL of (gamma/2)(div P)^2 [C1: n=1 polytrope]  vs  EL of (gamma/2)|grad P|^2 [L49]")
rr = sp.sqrt(x ** 2 + y ** 2 + z ** 2)
qf = sp.Function("q")
Prad = sp.Matrix([qf(rr) * c / rr for c in (x, y, z)])


def vec_lap(Pv):
    return sp.Matrix([sum(sp.diff(Pv[i], v, 2) for v in (x, y, z)) for i in range(3)])


def grad_div(Pv):
    d = sum(sp.diff(Pv[i], v) for i, v in enumerate((x, y, z)))
    return sp.Matrix([sp.diff(d, v) for v in (x, y, z)])


diff_rad = sp.simplify(vec_lap(Prad) - grad_div(Prad))
P(f"  radial P = q(r) r_hat:  lap P - grad div P = {list(diff_rad)}")
Ptest = sp.Matrix([y * sp.exp(-rr ** 2), 0, 0])                      # non-radial (has curl)
diff_nr = vec_lap(Ptest) - grad_div(Ptest)                           # = -curl curl P
val_nr = [float(sp.N(c.subs({x: 0.3, y: 0.4, z: 0.1}))) for c in diff_nr]
P(f"  non-radial test P = (y e^-r^2, 0, 0): (lap - grad div)P at (0.3,0.4,0.1) = {[f'{v:.4f}' for v in val_nr]} (= -curl curl P)")
check("S0.3 radial stiffness identity", all(sp.simplify(c) == 0 for c in diff_rad),
      "identical for radial P; non-radial P differs by gamma curl curl P (C1 does not carry L49's curl stiffness)")
RES["numbers"]["S0.3_nonradial_difference"] = val_nr

# ---------------------------------------------------------------- S0.5 BPS tolerance
P("\nS0.5  charge-ratio tolerance: q^2 = 1 + delta  =>  g_N = q Efun(q w) - w,  w = cold field, g = g_N + w")


def nu_of(yv, delta):
    """spherical: Gauss D = q w, force balance g = q E(D); E(D) = D/(1 - D) (a0 = 1); returns nu = g/g_N."""
    qv = np.sqrt(1 + delta)
    f = lambda w: qv * (qv * w) / (1 - qv * w) - w - yv
    wmax = 1 / qv * (1 - 1e-15)
    # for delta >= 0, f is increasing from -y at w=0; for delta < 0 it dips negative first: take the stable (largest) root
    ws = np.linspace(0, wmax, 20001)[1:]
    fv = f(ws)
    idx = np.where(np.sign(fv[:-1]) != np.sign(fv[1:]))[0]
    if len(idx) == 0:
        return np.nan
    i = idx[-1]
    w = brentq(f, ws[i], ws[i + 1], xtol=1e-16, rtol=1e-15)
    return (yv + w) / yv


def nu_law(yv):
    g = 0.5 * (yv + np.sqrt(yv * yv + 4 * yv))
    return g / yv


tol = {}
for yv in (1e-4, 6e-4):
    nl = nu_law(yv)
    n0 = nu_of(yv, 0.0)
    grid = np.logspace(-7, -0.5, 400)
    good_pos = [d for d in grid if abs(nu_of(yv, d) / nl - 1) <= 0.01]
    good_neg = [d for d in grid if (not np.isnan(nu_of(yv, -d))) and abs(nu_of(yv, -d) / nl - 1) <= 0.01]
    dpos = max(good_pos) if good_pos else 0.0
    dneg = max(good_neg) if good_neg else 0.0
    tol[yv] = dict(nu_law=nl, nu_bps=n0, delta_max_pos=dpos, delta_max_neg=dneg)
    P(f"  y = {yv:.0e}: nu_law {nl:.4f}, nu(delta=0) {n0:.4f}; 1% tolerance: delta <= +{dpos:.2e}, delta >= -{dneg:.2e}")
RES["numbers"]["S0.5"] = {str(k): v for k, v in tol.items()}
bps_ok = all(abs(v["nu_bps"] / v["nu_law"] - 1) < 1e-10 for v in tol.values())
check("S0.5 BPS (delta = 0) reproduces the law", bps_ok, "nu(delta=0) = nu_law to 1e-10 at y = 1e-4 and 6e-4")
P("  sign rule: delta < 0 gives R_delta(w) = q^2 w/(1 - q w) - w < 0 for small w (net self-attraction): Jeans-class,"
  " see ag6c_gate_iv H4 MUTATE (c)")

if MUT:
    P("\nMUTATE tooth: q^2 = 1.01 and the W_full double count must break S0.1/S0.2")
    bite = ("S0.1 Legendre identity" in FAILS) or ("S0.2 EL map at gamma = 0 (any geometry)" in FAILS)
    P(f"  tooth {'bites' if bite else 'DID NOT BITE'}")
    nmut = nu_of(1e-4, 0.01) / nu_law(1e-4) - 1
    P(f"  q^2 = 1.01 at y = 1e-4: nu/nu_law - 1 = {nmut:+.3f}")
RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"ag6c_s0_static_results{SUF}.json"), "w"), indent=1, default=float)
P("\nFAILS:", FAILS if FAILS else "none")
OUT.close()
sys.exit(1 if FAILS else 0)
