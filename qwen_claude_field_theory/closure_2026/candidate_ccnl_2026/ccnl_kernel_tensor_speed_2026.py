#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ccnl_kernel_tensor_speed_2026.py -- SECOND, INDEPENDENT KILL of the R_uu-coupled nonlocal kernel: c_T != c on galaxy backgrounds.
=================================================================================================================================
The localised kernel is  xi (Box X - R_mn u^m u^n).  On Minkowski / uniform-gradient backgrounds xi_bar = 0 and the TT sector is
untouched (R^(1)_uu[h^TT] = 0): this is the basis of every "c_T = c" certification of Deffayet-Woodard-type kernels so far.
But on a REAL galaxy background the multiplier has a nonzero background value: its static equation is
      lap xi_bar = 8 div( f'(Z_bar) grad X_bar )  = 8 x (1/2)(lap Psi_bar - 4 pi G rho_b) = 16 pi G rho_phantom      (c=1, 16piG=1 units)
i.e. xi_bar is sourced by the MOND PHANTOM density and is of order 4 Psi_phantom ~ v^2/c^2 ~ 1e-7 in every MOND zone.
A background xi_bar multiplies R_uu at SECOND order in the TT graviton, R^(2)_00[h^TT] != 0, which modifies the tensor kinetic
term and hence c_T.  This is the luminality no-go of the curvature-coupled clock class (Case 3a of the 09-01 verdict,
c_T^2 = 1/(1 - 2 lambda), lambda ~ -v^2/c^2, GW170817-excluded by 1e7-1e9), which the localised nonlocal kernel inherits.
Computed here: (A) R^(2)_00 of a TT plane wave, exactly; (B) the TT quadratic action of sqrt(-g)[R + xi_bar R_uu] -> c_T^2(xi_bar);
(C) xi_bar from the static multiplier equation on an exponential-law MOND galaxy; (D) the GW170817 comparison; (E) control xi_bar -> 0.
"""
import sys, math
import sympy as sp
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)

# ---------------------------------------------------------------- (A) exact metric with a TT wave, second-order Ricci
t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True)
hp = sp.Function('h_p')(t, z); hx = sp.Function('h_x')(t, z)      # GENERAL profiles (an exact t-z wave makes the EH part a total derivative)
g = sp.Matrix([[-1, 0, 0, 0], [0, 1 + eps*hp, eps*hx, 0], [0, eps*hx, 1 - eps*hp, 0], [0, 0, 0, 1]])
coords = [t, x, y, z]; ginv = g.inv()
def christoffel(g, ginv):
    return [[[sp.Rational(1, 2)*sum(ginv[a, d]*(sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d])) for d in range(4))
              for c in range(4)] for b in range(4)] for a in range(4)]
Gam = christoffel(g, ginv)
def ricci(Gam):
    R = sp.zeros(4, 4)
    for b in range(4):
        for c in range(4):
            R[b, c] = sum(sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                          + sum(Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a] for d in range(4)) for a in range(4))
    return R
Ric = ricci(Gam)
u_up = [1, 0, 0, 0]                                             # the clock frame at rest
R_uu = sp.expand(sp.series(sum(Ric[a, b]*u_up[a]*u_up[b] for a in range(4) for b in range(4)), eps, 0, 3).removeO())
R1 = sp.simplify(R_uu.coeff(eps, 1)); R2 = sp.simplify(R_uu.coeff(eps, 2))
check("A1 R^(1)_uu[h^TT] = 0 (the linear statement behind every 'c_T = c' certification)", R1 == 0)
check("A2 R^(2)_uu[h^TT] != 0: the SECOND-order 00-Ricci of a TT wave is nonzero", R2 != 0, f"R^(2)_00 = {sp.simplify(R2.subs(hx, 0))}")

# ---------------------------------------------------------------- (B) TT quadratic action with a background multiplier
xib = sp.symbols('xi_b', real=True)
sqrtg = sp.sqrt(-g.det())
Rs = sum(ginv[a, b]*Ric[a, b] for a in range(4) for b in range(4))
L = sp.expand(sp.series(sqrtg*(Rs + xib*sum(Ric[a, b]*u_up[a]*u_up[b] for a in range(4) for b in range(4))), eps, 0, 3).removeO().coeff(eps, 2))
# reduce to a single polarisation, general profile h(t,z) to read kinetic and gradient coefficients
hgen = hp
Lp = sp.expand(L.subs(hx, 0).doit())
# Euler-Lagrange for h(t,z) (second-order Lagrangian): use the manual operator
def EL(Lag, q, vars_=(t, z)):
    syms = {}
    for (v1, v2) in [(t, t), (t, z), (z, z)]:
        syms[sp.Derivative(q, v1, v2)] = sp.Symbol(f"__d2_{v1}{v2}")
    for v in vars_: syms[sp.Derivative(q, v)] = sp.Symbol(f"__d1_{v}")
    syms[q] = sp.Symbol("__q")
    Ls = Lag
    for d in sorted(syms, key=lambda e: -len(str(e))): Ls = Ls.subs(d, syms[d])
    back = {v_: k_ for k_, v_ in syms.items()}
    rest = lambda e: e.subs(back)
    res = rest(sp.diff(Ls, syms[q]))
    for v in vars_: res -= sp.diff(rest(sp.diff(Ls, syms[sp.Derivative(q, v)])), v)
    for (v1, v2) in [(t, t), (t, z), (z, z)]: res += sp.diff(rest(sp.diff(Ls, syms[sp.Derivative(q, v1, v2)])), v1, v2)
    return sp.expand(res)
eq = EL(Lp, hgen)
w, k = sp.symbols('omega k', real=True)
A = sp.symbols('A')
disp = sp.expand(sp.simplify(eq.subs(hgen, A*sp.exp(sp.I*(k*z - w*t))).doit()/(A*sp.exp(sp.I*(k*z - w*t)))))
cw = sp.simplify(disp.coeff(w, 2)); ck = sp.simplify(disp.coeff(k, 2))
cT2 = sp.simplify(-ck/cw)
info(f"TT dispersion with background xi_bar: {sp.factor(disp)} = 0  ->  c_T^2 = {cT2}")
check("B1 with xi_bar = 0 the graviton is luminal, c_T^2 = 1 (control)", sp.simplify(cT2.subs(xib, 0) - 1) == 0)
dcT2 = sp.simplify(sp.diff(cT2, xib).subs(xib, 0))
check("B2 a background multiplier changes the tensor speed at FIRST order: d(c_T^2)/d(xi_bar)|_0 != 0", dcT2 != 0, f"d c_T^2/d xi_bar = {dcT2}")
kin_sign = sp.simplify(cw)
info(f"   TT kinetic coefficient (of omega^2 h^2): {kin_sign}; gradient coefficient: {ck}")

# ---------------------------------------------------------------- (C) xi_bar on a MOND galaxy background (exponential law)
# static multiplier equation (c = 1, 16 pi G = 1, action sqrt(-g)[R + a0^2 f(Z) + xi(Box X - R_uu)]):
#   EL_X:  Box xi = 8 div(f'(Z) grad X)   with X = Psi (static), and  div((1 - 2f') grad Psi) = rho_b/2  (16piG=1: lap Psi = rho/2 ... normalisation cancels below)
# => lap xi_bar = 8 div(f' grad Psi) = 4 [lap Psi - lap Psi_N] = 4 lap(Psi - Psi_N) = 4 lap Psi_phantom   =>   xi_bar = 4 Psi_phantom (+ harmonic, set by the same BCs as Psi)
G = 6.674e-11; c = 2.99792458e8; Msun = 1.989e30; kpc = 3.0857e19
a0 = 9.36e-11
Mb = 6e10*Msun
import numpy as np
r = np.geomspace(0.5*kpc, 200*kpc, 4000)
gN = G*Mb/r**2
# exponential law: mu(y) = 1 - e^{-y}, y = g/a0, solve mu(g/a0) g = gN for g
def g_of_gN(gn):
    lo, hi = gn, gn + 2*np.sqrt(a0*gn) + 2*a0
    for _ in range(80):
        mid = 0.5*(lo + hi); mu = 1 - np.exp(-mid/a0)
        if mu*mid > gn: hi = mid
        else: lo = mid
    return 0.5*(lo + hi)
g = np.array([g_of_gN(v) for v in gN])
Psi = -np.concatenate([[0], np.cumsum(0.5*(g[1:] + g[:-1])*np.diff(r))])[::-1]  # potential from infinity (relative), inward integral
Psi = -(np.cumsum(g[::-1]*np.gradient(r)[::-1])[::-1])                              # Psi(r) = -int_r^inf g dr'
PsiN = -G*Mb/r
Psi_ph = Psi - PsiN
xi_bar = 4*Psi_ph/c**2                                                               # dimensionless, relative to the EH coefficient
i8 = np.argmin(np.abs(r - 8*kpc)); i30 = np.argmin(np.abs(r - 30*kpc))
info(f"MW-like galaxy (M_b = 6e10 Msun, exponential law): y(8 kpc) = {g[i8]/a0:.2f}, phantom potential Psi_ph/c^2 = {Psi_ph[i8]/c**2:.2e} at 8 kpc, {Psi_ph[i30]/c**2:.2e} at 30 kpc")
info(f"   => xi_bar = 4 Psi_ph/c^2 = {xi_bar[i8]:.2e} (8 kpc), {xi_bar[i30]:.2e} (30 kpc); max over 0.5-200 kpc = {np.max(np.abs(xi_bar)):.2e}")
check("C1 the multiplier's background value on a MOND galaxy is O(1e-7) (v^2/c^2 scale), not zero", 1e-8 < np.max(np.abs(xi_bar)) < 1e-5)

# ---------------------------------------------------------------- (D) GW170817
dcT = float(abs(dcT2))*np.max(np.abs(xi_bar))/2                                    # |c_T - 1| ~ |d c_T^2/d xi| xi_bar / 2
bound = 7e-16
info(f"|c_T/c - 1| along a path through the MOND zone ~ {dcT:.1e}  vs GW170817 |c_T/c - 1| < {bound:.0e}  ->  excess factor {dcT/bound:.1e}")
check("D1 the R_uu-coupled kernel violates the GW170817 tensor-speed bound in galactic MOND zones by > 1e6 (the Case-3a luminality kill, inherited)", dcT/bound > 1e6)
info("D2 scope: c=1, 16piG=1; xi_bar from the static multiplier equation with the exponential law; the O(1) coefficient d c_T^2/d xi_bar is exact (B2);")
info("        a path-averaged delay would reduce the number by the zone's fractional path length (order 1e-2..1e-1 for a Mpc-scale host), not by 1e6.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
