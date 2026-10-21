"""AG6C gates (i) lensing = dynamics and (ii) GW speed, for candidate C1 (dielectric cold dust).

Criteria: FROZEN_CRITERIA.md (committed alone first, e926935c3).
(i)  Static spherical GR with anisotropic matter: lensing (spatial) mass m(r) from T_00; dynamical mass
     M_dyn = m + 4 pi r^3 p_r / c^2 (TOV, weak field); M_lens = (m + M_dyn)/2.  Law halo of a point mass:
     g_N = GM/r^2, g_N = g^2/(g + a0), u = D = g - g_N, E = g; rho_c = d(r^2 u)/dr / (K r^2);
     dark T_00 = H = W_full(u), T_rr = L - E D/K = -H, T_thth = L; dust p = pi G L*^2 rho_c^2 (n = 1 polytrope).
(ii) sympy: second-order expansion in a TT perturbation of sqrt(-g) L_dark(X) and of the dust action; c_T = c iff no
     derivative of h appears (principal symbol = Einstein-Hilbert's).
Run: python3 ag6c_gates_i_ii.py   (AG6C_MUTATE=1: non-lensing response; photon = dark U(1). Both must fail.)
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp

MUT = os.environ.get("AG6C_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag6c_gates_i_ii{SUF}.out"), "w")
RES = {"lane": "AG6C", "script": "ag6c_gates_i_ii", "mutate": MUT, "checks": {}, "numbers": {}}
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


G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
K = 4 * math.pi * G
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTAR = 1.0 * KPC           # window top: largest dust pressure

P("AG6C gates (i) and (ii) for C1" + ("  [MUTATE: non-lensing response; photon = dark U(1)]" if MUT else ""))

# ================================================================== (i) lensing = dynamics
P("\n(i) L2  law halos of point masses, r from r_M/100 to 100 r_M, L* = 1 kpc")


def halo(Mb, a0, n=6000):
    rM = math.sqrt(G * Mb / a0)
    r = np.logspace(math.log10(rM / 1e4), math.log10(100 * rM), n)
    gN = G * Mb / r ** 2
    g = 0.5 * (gN + np.sqrt(gN ** 2 + 4 * gN * a0))
    e = g / a0
    u = a0 * e / (1 + e)                         # D = K|P| = g - g_N, written stably (first run subtracted: NaN at r -> 0)
    x = e / (1 + e)
    H = (a0 ** 2 / K) * (-x + np.log1p(e))       # W_full(D) = E.D - L  (J/m^3); -ln(1 - x) = ln(1 + e)
    Ld = (a0 ** 2 / K) * (e - np.log1p(e))       # L_dark(E)
    r2u = r ** 2 * u
    rho_c = np.gradient(r2u, r) / (K * r ** 2)
    eint = math.pi * G * LSTAR ** 2 * rho_c ** 2
    # T_00/c^2 contributions beyond the rest mass
    dens_extra = (H + eint) / C ** 2
    # cumulative masses: rest mass of cold energy exactly r^2 u/G (Gauss); extra by trapezoid from r[0] (inner part tiny)
    Mc = r2u / G
    integrand = 4 * math.pi * r ** 2 * dens_extra
    Mextra = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(r))])
    m = Mb + Mc + Mextra
    p_r = (Ld - g * u / K) + eint               # = -H + dust pressure
    Mdyn = m + 4 * math.pi * r ** 3 * p_r / C ** 2
    if MUT:  # non-lensing response: the metric's spatial part sees baryons only; dynamics sees the full law
        Mlens = 0.5 * (Mdyn + Mb)
    else:
        Mlens = 0.5 * (m + Mdyn)
    sel = r >= rM / 100
    ratio = Mdyn[sel] / Mlens[sel] - 1
    chk = np.max(np.abs(Ld - g * u / K + H) / H)   # identity T_rr = -H
    return dict(rM_kpc=rM / KPC, max_abs=float(np.max(np.abs(ratio))), at_r_over_rM=float(r[sel][np.argmax(np.abs(ratio))] / rM),
                sign=float(np.sign(ratio[np.argmax(np.abs(ratio))])), Trr_identity=float(chk),
                rest_vs_extra=float(np.max(Mextra[sel] / m[sel])))


worst = 0.0
tab = {}
for fo, a0 in A0.items():
    for lm in (8, 10, 12, 14):
        h = halo(10.0 ** lm * MSUN, a0)
        tab[f"{fo}_1e{lm}"] = h
        worst = max(worst, h["max_abs"])
        P(f"  {fo:9s} M_b 1e{lm:2d} Msun: r_M {h['rM_kpc']:9.2f} kpc, max |M_dyn/M_lens - 1| = {h['max_abs']:.3e} "
          f"(at {h['at_r_over_rM']:.3g} r_M, sign {h['sign']:+.0f}); field+internal energy / m <= {h['rest_vs_extra']:.2e}; "
          f"T_rr + H check {h['Trr_identity']:.1e}")
RES["numbers"]["L2"] = tab
if MUT:
    check("(i) L2 lensing = dynamics [MUTATE]", worst <= 1e-3, f"max |M_dyn/M_lens - 1| = {worst:.3f}")
    P(f"  MUTATE tooth {'bites' if worst > 0.5 else 'DID NOT BITE'} (needs > 0.5)")
else:
    check("(i) L2 lensing = dynamics", worst <= 1e-3, f"max |M_dyn/M_lens - 1| = {worst:.2e} over 4 masses x 2 footings "
          f"(pass line 1e-3; measured SPARC-KiDS ratio 1.02)")

# ================================================================== (ii) GW speed
P("\n(ii) G1  sympy: matter action to second order in a TT wave h(t,z) on a uniform dark-field background")
t, x, y, z, eps = sp.symbols("t x y z epsilon", real=True)
E1, E3, B3, Bx = sp.symbols("E1 E3 B3 Bx", real=True)
hp = sp.Function("hp")(t, z)
hx = sp.Function("hx")(t, z)
eta = sp.diag(-1, 1, 1, 1)
hmat = sp.zeros(4, 4)
hmat[1, 1], hmat[2, 2], hmat[1, 2], hmat[2, 1] = hp, -hp, hx, hx
gmet = eta + eps * hmat
ginv = eta - eps * eta * hmat * eta + eps ** 2 * eta * hmat * eta * hmat * eta     # exact to O(eps^2)
# background field strength F_{mu nu}: electric (E1 along x, E3 along z), magnetic (B3 along z, Bx along x)
F = sp.zeros(4, 4)
F[0, 1], F[1, 0] = -E1, E1
F[0, 3], F[3, 0] = -E3, E3
F[1, 2], F[2, 1] = B3, -B3
F[2, 3], F[3, 2] = Bx, -Bx
Xs = sp.Rational(-1, 4) * sum(ginv[m_, a_] * ginv[n_, b_] * F[m_, n_] * F[a_, b_]
                              for m_ in range(4) for n_ in range(4) for a_ in range(4) for b_ in range(4))
Xs = sp.expand(sp.series(Xs, eps, 0, 3).removeO())
detg = sp.expand(sp.series(gmet.det(), eps, 0, 3).removeO())
sqrtg = sp.expand(sp.series(sp.sqrt(-detg), eps, 0, 3).removeO())
f0, f1, f2 = sp.symbols("f0 f1 f2", real=True)     # L(X0), L_X(X0), L_XX(X0): a generic L(X)
X0 = Xs.subs(eps, 0)
dX = sp.expand(Xs - X0)
Lm = sp.expand(sqrtg * (f0 + f1 * dX + sp.Rational(1, 2) * f2 * dX ** 2))
L2 = sp.expand(Lm.coeff(eps, 2))
derivs = [a for a in sp.preorder_traversal(L2) if isinstance(a, sp.Derivative) and a.expr in (hp, hx)]
P(f"  O(eps^2) dark-sector Lagrangian has {len(derivs)} derivative(s) of h; X(g) = {sp.simplify(X0)}")
# dust: Brown-type action L = -m c^2 sqrt(-g_{mu nu} N^mu N^nu), N^mu = (N0, 0, 0, 0) (dust at rest)
N0 = sp.symbols("N0", positive=True)
Ld_dust = -sp.sqrt(-(gmet[0, 0] * N0 ** 2))
L2d = sp.expand(sp.series(Ld_dust, eps, 0, 3).removeO()).coeff(eps, 2)
P(f"  O(eps^2) dust Lagrangian (TT wave, dust at rest): {L2d}")
# mass-like coefficient for h+ only (E along x, propagation along z): numerical size of delta c / c
mass_hp = sp.simplify(L2.subs({hx: 0}).coeff(hp, 2))
P(f"  h+ mass-like coefficient (no derivatives): {mass_hp}")
# |delta c/c| ~ 32 pi G C_m /(c^4 k^2) with C_m ~ energy density; use the larger of dust rho c^2 (1e-20 kg/m^3)
# and the dark field's energy at e = 1e4 a0 (canonical a0)
om = 2 * math.pi * 100.0
k = om / C
rho_test = 1e-20
a0c = A0["canonical"]
ee = 1e4
Wdark = (a0c ** 2 / K) * (ee ** 2 / (1 + ee) - ee + math.log1p(ee))
Cm = max(rho_test * C ** 2, Wdark, (a0c ** 2 / K) * ee)
dcc = 32 * math.pi * G * Cm / (C ** 4 * k ** 2)
P(f"  |delta c/c| <~ 32 pi G C_m/(c^4 k^2) = {dcc:.2e} at 100 Hz (C_m = {Cm:.2e} J/m^3)")
RES["numbers"]["G1"] = dict(n_derivatives=len(derivs), delta_c_over_c=dcc)
check("(ii) G1 c_T = c", len(derivs) == 0 and L2d == 0 and dcc <= 1e-15,
      f"no derivative of h in the matter action at O(h^2); |delta c/c| <= {dcc:.1e} (GW170817: 1e-15)")
P("  G2: light couples only to g (no dark U(1) coupling, no kinetic mixing) => same cone as GWs => zero delay "
  "(CFG665 shared-metric certificate)")

# MUTATE / report: if the visible photon WERE the dark U(1), the extraordinary polarization would run at v^2 = 1 + e
e_halo = 1.0
Lh = 30 * KPC
dt_ext = (Lh / C) * (1 - 1 / math.sqrt(1 + e_halo))
P(f"\n  [{'MUTATE' if MUT else 'report'}] photon = dark U(1): extraordinary light leads by {dt_ext:.2e} s over 30 kpc at "
  f"e = 1 (GW170817 bound 1.7 s)")
RES["numbers"]["photon_is_dark_delay_s"] = dt_ext
if MUT:
    check("(ii) G2 shared cone [MUTATE photon = dark U(1)]", dt_ext <= 1.7, f"lead {dt_ext:.1e} s")
    P(f"  MUTATE tooth {'bites' if dt_ext > 1.7 else 'DID NOT BITE'}")

RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"ag6c_gates_i_ii_results{SUF}.json"), "w"), indent=1, default=float)
P("\nFAILS:", FAILS if FAILS else "none")
OUT.close()
sys.exit(1 if FAILS else 0)
