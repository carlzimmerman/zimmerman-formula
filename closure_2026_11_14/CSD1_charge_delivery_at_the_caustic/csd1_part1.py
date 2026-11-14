#!/usr/bin/env python3
"""CSD1 Part 1 (FROZEN_CRITERIA.md section 1): P1a the static balance of FLD1's shell equation is the law; P1b the
interface condition and its advective reduction; KA1, KA2, KA6; twins TW1, TW2 (with argument 'mutate').
  python3 -I -B csd1_part1.py [mutate] -> csd1_part1.json / .out  (csd1_part1_MUTATE.json / .out)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
import numpy as np
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "fable52_push", "COL1_clock_collapse"))
import col1_lib as L                                            # read-only (G, law_g, a0_of)
MUT = len(sys.argv) > 1 and sys.argv[1] == "mutate"
OUT = []; RES = {}
def P(*x):
    s = " ".join(str(y) for y in x); print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- P1a, sympy
a0, gN, y, g = sp.symbols("a0 g_N y g", positive=True)
U = a0 * y / (a0 + y) if MUT else a0 * y / (a0 - y)            # TW1 flips the cap's sign
bal = sp.Eq(-gN - y + U, 0)
ysol = [s for s in sp.solve(bal, y)]
P("P1a sympy: roots of -g_N - y + U(y) = 0 for y:", ysol)
ok_sym = False
for ys in ysol:
    gg = gN + ys
    resid = sp.simplify(gg ** 2 / (a0 + gg) - gN)
    P("   root", ys, "-> residual of g^2/(a0+g) - g_N with g = g_N + y:", resid)
    if resid == 0: ok_sym = True
# converse: g on the law -> y = g - g_N satisfies the balance
glaw = (gN + sp.sqrt(gN ** 2 + 4 * gN * a0)) / 2
conv = sp.simplify(sp.radsimp(-gN - (glaw - gN) + U.subs(y, glaw - gN)))
P("P1a sympy converse: balance residual at y = g_law - g_N:", conv)
ok_sym = ok_sym and conv == 0
RES["P1a_sympy"] = dict(roots=[str(s) for s in ysol], pass_=bool(ok_sym))

# ---------------------------------------------------------------- P1a, numeric (the shell equation's own U and law_g)
worst = 0.0; worst_m = 0.0
for foot in ("canonical", "alt"):
    A0 = L.a0_of(foot)
    Uf = (lambda yy: A0 * yy / (A0 + np.abs(yy))) if MUT else (lambda yy: A0 * yy / (A0 - np.abs(yy)))
    x = np.logspace(-6, 3, 2000) * A0
    # solve the balance for y in (0, a0) by bisection in high precision floats
    lo = np.zeros_like(x); hi = np.full_like(x, A0 * (1 - 1e-15))
    for _ in range(200):
        mid = 0.5 * (lo + hi); f = -x - mid + Uf(mid)
        lo = np.where(f < 0, mid, lo); hi = np.where(f < 0, hi, mid)
    yb = 0.5 * (lo + hi); gb = x + yb
    dev = np.max(np.abs(gb * gb / (A0 + gb) - x) / x); worst = max(worst, float(dev))
    # the enclosed excess at balance against FLD1's Mph, log M_b 8 and 11.5, r 1 to 1000 kpc
    EPS = 1.0
    for lM in (8.0, 11.5):
        Mb = 10 ** lM; R = np.logspace(0, 3, 400)
        gn = L.G * Mb * R / (R * R + EPS * EPS) ** 1.5
        lo = np.zeros_like(R); hi = np.full_like(R, A0 * (1 - 1e-15))
        for _ in range(200):
            mid = 0.5 * (lo + hi); f = -gn - mid + Uf(mid)
            lo = np.where(f < 0, mid, lo); hi = np.where(f < 0, hi, mid)
        m_bal = 0.5 * (lo + hi) * R * R / L.G
        mph = R * R * (L.law_g(gn, A0) - gn) / L.G
        worst_m = max(worst_m, float(np.max(np.abs(m_bal / mph - 1))))
P(f"P1a numeric: max |g^2/(a0+g) - g_N|/g_N over g_N/a0 in [1e-6, 1e3], both footings: {worst:.2e}; "
  f"max |m_balance / Mph - 1|: {worst_m:.2e} (line 1e-12)")
ka1 = ok_sym and worst <= 1e-12 and worst_m <= 1e-12
P("KA1 (static balance = the law):", "PASS" if ka1 else "FAIL")
RES["P1a_numeric"] = dict(max_law_dev=worst, max_mass_dev=worst_m); RES["KA1"] = bool(ka1)

# ---------------------------------------------------------------- P1b, sympy: the distributional current condition
t, r = sp.symbols("t r", real=True)
R = sp.Function("R")(t)
Jti, Jto, Jri, Jro = (sp.Function(n)(t, r) for n in ("Jt_in", "Jt_out", "Jr_in", "Jr_out"))
F = r - R
H = sp.Heaviside
Jt = Jti * H(-F) + Jto * H(F); Jr = Jri * H(-F) + Jro * H(F)
div = sp.diff(r ** 2 * Jt, t) + sp.diff(r ** 2 * Jr, r)
div = sp.expand(div)
# collect the delta coefficient (DiracDelta(r - R) and DiracDelta(R - r) are the same distribution)
d1 = sp.DiracDelta(r - R); d2 = sp.DiracDelta(-r + R)
coef = sp.simplify(div.coeff(d1) + div.coeff(d2))
Rd = sp.diff(R, t)
sign = -1 if MUT else 1                                          # TW2 flips the sign of Rdot in the claimed condition
claim = r ** 2 * ((Jro - Jri) - sign * Rd * (Jto - Jti))
resid_b = sp.simplify(coef - claim)
P("P1b sympy: delta(F) coefficient of d_t(r^2 J^t) + d_r(r^2 J^r):", coef)
P("P1b residual against r^2([J^r] - Rdot [J^t]):", resid_b)
ok_b = resid_b == 0
# advective reduction and the standing interior
Ni, No, vi, vo, Rdt = sp.symbols("N_in N_out v_in v_out Rdot", real=True)
cond = (No * vo - Ni * vi) - sign * Rdt * (No - Ni)
red = sp.simplify(cond - (No * (vo - Rdt) - Ni * (vi - Rdt)))
P("P1b advective reduction residual N_out(v_out - Rdot) - N_in(v_in - Rdot):", red)
vreq = sp.solve(cond.subs(vi, 0), vo)
P("P1b standing interior (v_in = 0): v_out =", vreq)
RES["P1b"] = dict(delta_coefficient=str(coef), residual=str(resid_b), reduction_residual=str(red), v_out_required=[str(v) for v in vreq])
# KA2: the junction note's rational example
rr = sp.symbols("rr", positive=True)
CB, CR, Rs, T = rr, rr ** 2, sp.Rational(1, 2), 1
tt = (T - CB.subs(rr, Rs)) / (T - CR.subs(rr, Rs))
Nin_ = sp.diff(CB, rr).subs(rr, Rs); Nout_ = tt * sp.diff(CR, rr).subs(rr, Rs)       # common 4 pi R^2 cancels
c_ok = cond.subs({vi: 0, Ni: Nin_, No: Nout_, Rdt: 2, vo: -1})
c_stat = cond.subs({vi: 0, Ni: Nin_, No: Nout_, Rdt: 0, vo: -1})
P(f"KA2: t = {tt}, N_in/N_out = {sp.nsimplify(Nin_ / Nout_)}; (Rdot, v_out) = (2, -1) -> condition residual {c_ok}; "
  f"(0, -1) -> {c_stat}")
ka2 = ok_b and red == 0 and tt == sp.Rational(2, 3) and sp.nsimplify(Nin_ / Nout_) == sp.Rational(3, 2) and c_ok == 0 and c_stat != 0
P("KA2 (interface condition and the rational example):", "PASS" if ka2 else "FAIL")
RES["KA2"] = bool(ka2)
# integrated form: d/dt C_in(<R(t)) with a standing interior equals the flux delivered across the moving boundary
Cin = sp.Function("C_in")(r)
lhs = sp.diff(Cin.subs(r, R), t)                                  # = C_in'(R) Rdot = 4 pi R^2 N_in Rdot
P("P1b integrated: d/dt C_in(R(t)) =", lhs, "= C_in'(R) Rdot = 4 pi R^2 N_in Rdot; with v_in = 0 the condition makes this "
  "4 pi R^2 N_out (Rdot - v_out), the charge carried across the moving boundary per unit time")

# ---------------------------------------------------------------- KA6: units, independent SI
Gsi, kpc, Msun = 6.674e-11, 3.0857e19, 1.989e30
foot = "canonical"; a0si = 9.3603e-11; Mb = 10 ** 10.7; Rk = 100.0
gn = Gsi * Mb * Msun * (Rk * kpc) / ((Rk * kpc) ** 2 + kpc ** 2) ** 1.5
gl = 0.5 * (gn + math.sqrt(gn * gn + 4 * gn * a0si))
mph_si = (Rk * kpc) ** 2 * (gl - gn) / Gsi / Msun
gk = L.G * Mb * Rk / (Rk * Rk + 1.0) ** 1.5
mph_k = Rk * Rk * (L.law_g(gk, L.a0_of(foot)) - gk) / L.G
ka6 = abs(mph_si / mph_k - 1) <= 1e-3
P(f"KA6: C_law(100 kpc, log M_b 10.7, canonical) SI {mph_si:.6e} M_sun, FLD1 units {float(mph_k):.6e}; rel {abs(mph_si / mph_k - 1):.1e} "
  f"(line 1e-3) -> {'PASS' if ka6 else 'FAIL'}")
RES["KA6"] = dict(mph_si=mph_si, mph_fld1=float(mph_k), pass_=bool(ka6))

name = "csd1_part1" + ("_MUTATE" if MUT else "")
RES["mutate"] = MUT; RES["note"] = "Adopts nothing. kappa = 1/2 FITTED; not theory closed."
json.dump(RES, open(os.path.join(HERE, name + ".json"), "w"), indent=1, default=str)
OUT.append("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, name + ".out"), "w").write("\n".join(OUT) + "\n")
