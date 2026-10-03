"""EXT01 check: independent re-derivation of the algebra downstream of the stated inputs in
EXT01_gauge_vacuum_identity_and_clock_2026-10-02.md (an external note; see README.md here).

What this script does NOT do: it does not derive the helicity velocity Lagrangian (note section 2)
or the three-field clock action L_S,UV (note section 5) -- those are TAKEN AS STATED. It checks
that everything the note derives from them follows, and that the Poynting-square Hessian and the
Ward-identity solution follow from their definitions.

Run:            python3 ext01_check.py            (exit 0 iff all checks pass)
Mutation run:   MUTATE=1 python3 ext01_check.py   (a coefficient of the claimed scalar polynomial is
                                                   changed; the run MUST fail, exit 1)
"""
import os
import sys

import numpy as np
import sympy as sp

MUTATE = os.environ.get("MUTATE") == "1"
results = []


def check(name, ok):
    results.append((name, bool(ok)))
    print(("PASS  " if ok else "FAIL  ") + name)


# ---- 1. Ward-identity solution (note section 1) -------------------------------------------
E, B, pE, pB, ZE, ZB, ZEB = sp.symbols("E B pE pB ZE ZB ZEB")
eqs = [
    E**2 * ZE + 2 * E * B * ZEB + B**2 * ZB - (E * pE + B * pB),
    B**2 * ZE - 2 * E * B * ZEB + E**2 * ZB + (E * pE + B * pB),
    E * B * (ZE - ZB) + (B**2 - E**2) * ZEB - (B * pE - E * pB),
]
sol = sp.solve(eqs, [ZE, ZB, ZEB], dict=True)[0]
N = E**2 + B**2
check("1a Z_E = (E pE - B pB)/(E^2+B^2)", sp.simplify(sol[ZE] - (E * pE - B * pB) / N) == 0)
check("1b Z_B = -Z_E", sp.simplify(sol[ZB] + sol[ZE]) == 0)
check("1c Z_EB = (B pE + E pB)/(E^2+B^2)", sp.simplify(sol[ZEB] - (B * pE + E * pB) / N) == 0)
l, lE, lB = sp.symbols("l lE lB")
rho = E * lE - l
p = l - (E * lE + 2 * B * lB) / 3
check("1d Z_E = (rho+p)/(2(E^2+B^2)) with pE=lE/3, pB=lB/3",
      sp.simplify(((rho + p) / (2 * N)).subs({lE: 3 * pE, lB: 3 * pB}) - sol[ZE]) == 0)

# ---- 2. vector Schur complement (note section 2) ------------------------------------------
A, D, M, k, m, Bv, v, u, w = sp.symbols("A D M k m Bv v u w", real=True)
for sg in (1, -1):
    L = (A / 4 * (v - k * u) ** 2
         + D / 4 * (-v + (2 * sg * m - k) * u - 2 * Bv * w) ** 2
         + M**2 * k**2 / 4 * w**2)
    s = sp.solve([sp.diff(L, u), sp.diff(L, w)], [u, w], dict=True)[0]
    Kred = sp.simplify(2 * L.subs(s) / v**2)
    Kclaim = (2 * A * D * M**2 * (k - sg * m) ** 2
              / (4 * A * Bv**2 * D + M**2 * (A * k**2 + D * (k - 2 * sg * m) ** 2)))
    check(f"2a K_sigma closed form, sigma={sg:+d}", sp.simplify(Kred - Kclaim) == 0)
    check(f"2b dK/dD at D=0 = 2(k-sigma m)^2/k^2, sigma={sg:+d}",
          sp.simplify(sp.diff(Kclaim, D).subs(D, 0) - 2 * (k - sg * m) ** 2 / k**2) == 0)
    check(f"2c K -> 2AD/(A+D) as k->oo, sigma={sg:+d}",
          sp.simplify(sp.limit(Kclaim, k, sp.oo) - 2 * A * D / (A + D)) == 0)
# table values (q=B=g=M=1, k=10, beta=1/6, zeta=1/2): D = 1 - E + (2/3)(E^2-1), A = 1 + E + (2/3)(E^2-1)
def K_num(Ev, sg):
    Dn = 1 - Ev + (2 / 3) * (Ev**2 - 1)
    An = 1 + Ev + (2 / 3) * (Ev**2 - 1)
    kk, mm, BB = 10.0, 1.0, 1.0
    return (2 * An * Dn * (kk - sg * mm) ** 2) / (4 * An * BB**2 * Dn + (An * kk**2 + Dn * (kk - 2 * sg * mm) ** 2))
check("2d table E=0.999 (D=-3.326667e-4, K-=-8.05257e-4, K+=-5.38985e-4)",
      abs(K_num(0.999, -1) + 0.0008052571490) < 1e-9 and abs(K_num(0.999, +1) + 0.0005389846158) < 1e-9
      and abs((1 - 0.999 + (2 / 3) * (0.999**2 - 1)) + 0.0003326666667) < 1e-12)
check("2e table E=1.001 (D=3.34e-4, K-=8.08075e-4, K+=5.41015e-4)",
      abs(K_num(1.001, -1) - 0.0008080751047) < 1e-9 and abs(K_num(1.001, +1) - 0.0005410150158) < 1e-9)

# ---- 3. homogeneous-flow numbers (note section 3) -----------------------------------------
q, Ee = sp.symbols("q Ee")
Dq = 1 - Ee + sp.Rational(2, 3) * (Ee**2 - q**4)         # B = g q^2, benchmark beta=1/6, zeta=1/2
check("3a dD/dq=-8/3, dD/dE=1/3 at q=E=1",
      sp.diff(Dq, q).subs({q: 1, Ee: 1}) == sp.Rational(-8, 3) and sp.diff(Dq, Ee).subs({q: 1, Ee: 1}) == sp.Rational(1, 3))
J = sp.Matrix([[-2, sp.Rational(1, 6)], [sp.Rational(44, 5), -1]])
check("3b tr J = -3, det J = 8/15", J.trace() == -3 and J.det() == sp.Rational(8, 15))
ev = [complex(sp.N(e)) for e in J.eigenvals()]
check("3c both homogeneous eigenvalues negative real", all(abs(e.imag) < 1e-12 and e.real < 0 for e in ev))
check("3d d/dt(delta D) on D=0 is 92/45 delta q", sp.Rational(124, 15) - sp.Rational(7, 9) * 8 == sp.Rational(92, 45))
Eb = lambda qq: (3 + sp.sqrt(16 * qq**4 - 15)) / 4
check("3e E_b(q) solves D=0", sp.simplify(Dq.subs(Ee, Eb(q))) == 0)
q0 = sp.Float("0.999")
D0 = float(Dq.subs({q: q0, Ee: Eb(q0) + sp.Float("1e-5")}))
check("3f D(q=0.999, E=E_b+1e-5) = 3.2251e-6", abs(D0 - 3.2251e-6) < 5e-10)
# extra (mine, not in the note): on the slow eigendirection D carries the sign of delta q
lam_slow = max(ev, key=lambda e: e.real).real
v2 = 6 * (2 + lam_slow)                                   # (J - lam) v = 0 with v1 = 1
dD_slow = -8 / 3 + v2 / 3
check("3g (extra) slow eigendirection has dD = +0.95 per unit delta q (D has the sign of delta q)",
      abs(dD_slow - 0.953) < 5e-3)

# ---- 4. Poynting-square Hessian (note section 4), from the definition ----------------------
e, b, lam = sp.symbols("e b lam")
# S_i = eps_ijk E_aj B_ak, E = E 1 + e J, B = B 1 + b J, J_jk = eps_jkl j_l (||J||^2 = 2) => S = 2 (E b - e B) j
dL = sp.expand(lam / 2 * 4 * (E * b - e * B) ** 2)
at1 = {E: 1, B: 1}
check("4a dZ_E=2lam, dZ_B=2lam, dZ_EB=-2lam at E=B=1",
      dL.coeff(e, 2).subs(at1) == 2 * lam and dL.coeff(b, 2).subs(at1) == 2 * lam
      and sp.Rational(1, 2) * dL.coeff(e, 1).coeff(b, 1).subs(at1) == -2 * lam)
check("4b K_V = 4 lam/(1+lam) (A_s=2, D=2 lam, k->oo)", sp.simplify(2 * 2 * (2 * lam) / (2 + 2 * lam) - 4 * lam / (1 + lam)) == 0)

# ---- 5. scalar principal part (note section 5), L_S,UV TAKEN AS STATED ---------------------
t, kk, mu, om, ss = sp.symbols("t k mu omega s", positive=True)
lam_ = sp.Symbol("lam_", positive=True)
X, Y, P = [sp.Function(n)(t) for n in "XYP"]
Ls = (sp.Rational(30, 17) * sp.diff(X, t) ** 2 - sp.Rational(4, 17) * kk * Y * sp.diff(X, t)
      + sp.Rational(110, 153) * kk**2 * Y**2
      + 2 * lam_ * (sp.diff(Y, t) + kk * X - 2 * kk * P) ** 2 + 2 * mu * sp.diff(P, t) ** 2)
EL = [sp.diff(sp.diff(Ls, sp.diff(f, t)), t) - sp.diff(Ls, f) for f in (X, Y, P)]
a1, a2, a3 = sp.symbols("a1 a2 a3")
ex = sp.exp(-sp.I * om * t)
rows = [sp.expand(ei.subs({X: a1 * ex, Y: a2 * ex, P: a3 * ex}).doit() / ex) for ei in EL]
Mx = sp.Matrix([[sp.diff(r, a) for a in (a1, a2, a3)] for r in rows])
det = sp.simplify(Mx.det().subs(om, sp.sqrt(ss) * kk))
c_mid = 47 if MUTATE else 48                              # MUTATE: 48 -> 47 in the claimed polynomial
claim = 135 * lam_ * mu * ss**2 + mu * (c_mid - 18 * lam_) * ss + lam_ * (55 * mu + 192)
ratio = sp.simplify(det / claim)
check("5a det = (-64 k^6 s/153) * claimed quadratic", sp.simplify(ratio + 64 * kk**6 * ss / 153) == 0)
lv, mv = sp.Rational(2, 3), sp.Rational(1, 10)
s_free = sp.Symbol("s_free")                              # the roots are complex, so solve over an unrestricted symbol
rts = [complex(sp.N(r, 12)) for r in sp.solve(claim.subs({lam_: lv, mu: mv, ss: s_free}), s_free)]
check("5b roots at lam=2/3, mu=1/10: -0.2 +- 3.81964 i",
      all(abs(r.real + 0.2) < 1e-6 and abs(abs(r.imag) - 3.81964) < 1e-5 for r in rts))
check("5c Gamma/k = 1.41860 (max |Im sqrt s|)", abs(max(abs(np.sqrt(r).imag) for r in rts) - 1.41860) < 1e-5)
bad = 0
for lv_ in np.linspace(0.01, 0.99, 60):
    for mv_ in np.logspace(-3, 3, 60):
        r = np.roots([135 * lv_ * mv_, mv_ * (48 - 18 * lv_), lv_ * (55 * mv_ + 192)])
        bad += any(abs(z.imag) < 1e-12 and z.real >= 0 for z in r)
check("5d no non-negative real root anywhere on 0<lam<1, 1e-3<mu<1e3 grid (3600 points)", bad == 0)

n_ok = sum(ok for _, ok in results)
print(f"\n{n_ok}/{len(results)} checks pass" + ("  [MUTATE=1: a failure is REQUIRED]" if MUTATE else ""))
sys.exit(0 if n_ok == len(results) else 1)
