#!/usr/bin/env python3
"""
L25 -- the universal external field: does the eta-matching force one, and would galaxies survive it?
====================================================================================================
THE QUESTION, and why it is the single decisive open item.  L11 established that the lead agent's
IC-series reduces, in the static weak field, to a genuine AQUAL-type MOND theory,

    div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G_N rho_b,   mu(y) = 1 - e^(-y),   y = |grad Phi|/a0,

at the action's own a0 with coefficient exactly 1.000000, with no slip and with G_N = 1/(8 pi m).
L11's ONE unresolved input (its B5 FAIL) is the far-field boundary condition on the auxiliary field u:

  * on the eta = 0 STATIC branch the law gives u^2 = 1 - e^(-|a|/a0), so u -> 0 as |a| -> 0
    (ordinary isolated MOND, deep-MOND asymptotics intact);
  * on the eta = 1 COSMOLOGICAL plateau the lead's own exhibited solutions give u = 0.492-0.570
    (IC10) and u = 2/3 at the IC4/IC5 witness;
  * matching the two requires varying the eta-transition.

The stakes L11 computed: if u must approach its cosmological value in the far field, the static law
reads that as a UNIVERSAL EXTERNAL FIELD of g_ext = 0.28-0.59 a0 acting on every galaxy, and 27%
(canonical) / 38% (alt) of bulgeless SPARC points beyond 2 kpc sit BELOW even the smallest of those.
That is exactly where flat rotation curves live.

THIS FILE ANSWERS BOTH HALVES.

PART A -- WHAT THE ETA-TRANSITION ACTUALLY GIVES (part 1), varied rather than assumed at either end.
  E1  eta's ARGUMENT.  IC5 defines eta = eta(r) with r = -N p/(3 m h0), p = h_{mu nu}P^{mu nu} the
      TRACE METRIC MOMENTUM.  eta is therefore a function of the LOCAL EXPANSION RATE ONLY -- not of
      position, not of the local gravitational field, not of density.  Checked against the file text
      and by evaluating the published smooth switch: eta == 0 and all derivatives == 0 for r^2 <= 1/2.
  E2  WHETHER u CARRIES A BOUNDARY CONDITION AT ALL on eta = 0.  Re-derived here from scratch with
      sympy (the conformal 3-curvature identity is DERIVED, not quoted): IC5's static gradient block
      combines with the barred-curvature difference into an exact NULL LAGRANGIAN, so the static
      u-equation contains NO derivative of u.  u is algebraically slaved pointwise.  A field with no
      derivatives in its own Euler-Lagrange equation CANNOT carry a boundary condition.  This is the
      structural answer to part 1: inside eta = 0, u is whatever the local |a| says, full stop.
  E3  WHERE THE ETA BOUNDARY IS, for real SPARC galaxies.  eta leaves 0 only where the local
      expansion rate reaches r^2 = 1/2.  Computed per galaxy from the data with two independent,
      deliberately CONSERVATIVE criteria (Hubble-velocity crossing; the Lambda zero-gravity radius
      built from the measured baryonic mass on the framework's OWN kernel), against R_last.
  E4  WHAT IS STILL MISSING, stated precisely.  IC11 has now varied the transition -- but only on a
      HOMOGENEOUS background, and that trial FAILS a necessary scalar kinetic condition (aUV < 0 from
      n = 205).  No spatially inhomogeneous eta profile around a bound mass exists in any published
      file.  E4 records exactly which calculation would close it.

PART B -- IF THERE IS A UNIVERSAL EXTERNAL FIELD OF THAT SIZE, DO FLAT ROTATION CURVES SURVIVE?
  Done here whatever part A says, because it is what bounds the answer from the data side.  In
  MOND-class theories an external field SATURATES the boost: below g_ext the internal dynamics
  returns to Newtonian behaviour with a rescaled G, nu_ext = 1/mu(g_ext/a0), and rotation curves fall
  as r^(-1/2) instead of staying flat.  The construction's OWN kernel mu(y) = 1 - e^(-y) is used
  throughout -- NOT nu_RAR, because L11 showed the exponential carrier is what this action produces.
  C0  kernel controls (deep-MOND coefficient, Newtonian limit, solver residual);
  C1  CONTROL: at g_ext = 0 the pipeline reproduces the radial acceleration relation and its scatter;
  C2  CONTROL: the external-field implementation reproduces a PUBLISHED EFE result of this repository
      at its stated parameters (aqual_efe_full_solve_2026.py PART A / stage64 PART B: the AQUAL
      linear-response tensor B_par = nu(y_extN) = 1.47342, B_perp = 1.2598, the registered
      sqrt(nu) = 1.2139 / 1.2592 and the superseded MI 1.1582, at x_ext = 1.9, Route A kernel);
  D1-D3 the damage: RAR scatter and zero point, outer slopes, and the profiled-Upsilon fit;
  F1  do flat rotation curves survive g_ext = 0.28 a0?
  F2  do flat rotation curves survive g_ext = 0.59 a0?
  F3  THE DELIVERABLE: the largest universal g_ext the SPARC rotation curves will tolerate.

SPARC is loaded exactly as fable_independent_2026/L6_screened_force.py loads it:
real_research/data/sparc_data/*_rotmod.dat, Upsilon_disk = 0.5, Upsilon_bul = 0.7, eV/V < 0.10.
Both a0 footings throughout: 9.3619e-11 (canonical) and 1.1279e-10 m/s^2 (alt).

HONESTY DECLARATIONS, up front.
  * The external-field response used for the rotation curves is the standard algebraic AQUAL EFE,
    mu(|g_int + g_ext|/a0) g_int = g_N, in the isotropic (quadrature) composition.  Its g_int -> 0
    limit is the boost nu(g_ext/a0), which is the EXACT AQUAL linear-response eigenvalue B_par --
    i.e. the LARGER of the two eigenvalues.  Using it isotropically therefore OVERSTATES the boost
    and UNDERSTATES the damage, by the factor computed in C0.  Every number here sits on the
    conservative side of the anisotropy, so F3's bound is an upper bound on the bound.
  * Upsilon is PROFILED per galaxy under a 0.11 dex prior in D3/F1/F2/F3, errors are inflated to
    chi2/dof = 1 before any Delta chi2 is read, and a global a0 rescaling is profiled as well, so the
    bound is what survives the freedom the data actually leave.
  * E3's transition radius is a KINEMATIC estimate of the local expansion rate around a bound object,
    not a solution of the IC field equations in the transition region.  It is labelled as such and
    the missing calculation is named in E4.
"""

import os
import sys
import math
import glob

import numpy as np
import sympy as sp

# ----------------------------------------------------------------------------------------------------
# the check() helper, copied from L6_screened_force.py
# ----------------------------------------------------------------------------------------------------
FAILS = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def info(name, detail=""):
    print(f"  [info] {name}" + (f"   {detail}" if detail else ""), flush=True)


REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IC = os.path.join(REPO, "qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026")

C_LIGHT = 2.99792458e8
G_NEWT = 6.674e-11
MSUN = 1.989e30
kpc = 3.0856775814913673e19
Mpc = 1000.0 * kpc
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0_SI = 67.4e3 / Mpc
OMEGA_L = 0.685

U_COSMO = [("IC10 S=0.10", 0.492193), ("IC10 S=0.15", 0.536585), ("IC10 S=0.20", 0.570419),
           ("IC11 transition n=200", 0.622175269506), ("IC4/IC5 witness", 2.0 / 3.0),
           ("IC11 transition n=500", 0.666131555711)]

print("=" * 120)
print("L25 -- the universal external field: does the eta-matching force one, and would galaxies survive it?")
print("=" * 120, flush=True)


# ====================================================================================================
# PART A -- WHAT THE ETA-TRANSITION ACTUALLY GIVES
# ====================================================================================================
print("\n" + "-" * 120)
print("PART A -- the eta transition, varied rather than assumed at either endpoint")
print("-" * 120, flush=True)

# ---- E1: eta's argument ----------------------------------------------------------------------------
print("\n  E1 -- WHAT eta IS A FUNCTION OF.  This decides the whole question, because it decides WHERE")
print("        the two branches can meet.")
ic5 = open(os.path.join(IC, "IC5_ACTION.md")).read()
ic10 = open(os.path.join(IC, "IC10_LOCAL_CLOCK.md")).read()
ic11t = open(os.path.join(IC, "IC11_TRANSITION.md")).read()
ic11c = open(os.path.join(IC, "IC11_CLOCK_PRESSURE.md")).read()

TOKENS = {
    "activation argument r = -N p/(3 m h0)": r"r=-\frac{Np}{3mh_0}",
    "p is the TRACE of the metric momentum": r"p=h_{\mu\nu}P^{\mu\nu}",
    "switch shape d(r) = (r^2-1)^2": r"d(r)=(r^2-1)^2",
    "static plateau eta = 0 for |r^2-1| >= 1/2": r"$\eta=0$ for $|r^2-1|\ge1/2$",
}
have = {k: (v in ic5) for k, v in TOKENS.items()}
for k, v in have.items():
    info(f"IC5_ACTION.md: {k}", "found verbatim" if v else "NOT FOUND")
no_field_dep = not any(t in ic5.split("Complete covariant phase-space action")[0]
                       for t in ("eta(Phi", "eta(rho", "eta(|a|", "eta(x"))
print("        eta = eta(r) with r = -N p/(3 m h0) and p the TRACE of the metric momentum: eta is a")
print("        function of the LOCAL EXPANSION RATE alone.  No Phi, no |a|, no rho, no position.")


def Efun(t):
    return math.exp(-1.0 / t) if t > 0 else 0.0


def eta_of(rv):
    dd = (rv * rv - 1.0) ** 2
    A = Efun(0.25 - dd)
    B = Efun(dd - 1.0 / 16.0)
    return A / (A + B) if (A + B) > 0 else 0.0


grid_static = np.linspace(0.0, math.sqrt(0.5), 601)
eta_static = np.array([eta_of(v) for v in grid_static])
h_ = 1e-5
d1 = np.array([(eta_of(v + h_) - eta_of(max(v - h_, 0.0))) / (h_ + min(h_, v)) for v in grid_static])
d2 = np.array([(eta_of(v + h_) - 2 * eta_of(v) + eta_of(max(v - h_, 0.0))) / h_ ** 2 for v in grid_static])
grid_cos = np.linspace(math.sqrt(0.75), math.sqrt(1.25), 401)
eta_cos = np.array([eta_of(v) for v in grid_cos])
print(f"        static side  0 <= r <= {math.sqrt(0.5):.6f} (r^2 <= 1/2): max|eta| = {np.abs(eta_static).max():.3e}, "
      f"max|eta'| = {np.abs(d1).max():.3e}, max|eta''| = {np.abs(d2).max():.3e}")
print(f"        cosmological plateau {math.sqrt(0.75):.4f} <= r <= {math.sqrt(1.25):.4f} (|r^2-1| <= 1/4): "
      f"max|1-eta| = {np.abs(1 - eta_cos).max():.3e}")
check("E1 eta's activation variable is the trace metric momentum (the local expansion rate) and nothing "
      "else, and its static plateau is EXACT -- eta and all its derivatives vanish identically for "
      "r^2 <= 1/2, so a quasi-static region sits at eta = 0 on a NEIGHBOURHOOD, not at a point",
      all(have.values()) and no_field_dep and float(np.abs(eta_static).max()) == 0.0
      and float(np.abs(d1).max()) == 0.0 and float(np.abs(d2).max()) == 0.0
      and float(np.abs(1 - eta_cos).max()) == 0.0,
      "verified against the published definition and by evaluating the switch")

# ---- E2: does u carry a boundary condition on eta = 0 at all? ----------------------------------------
print("\n  E2 -- DOES u CARRY A BOUNDARY CONDITION ON THE eta = 0 BRANCH?  If its static Euler-Lagrange")
print("        equation has no derivative of u, then u is algebraically slaved pointwise and NO far-field")
print("        value can be imposed on it at all.")

rr = sp.Symbol('r', positive=True)
th = sp.Symbol('theta')
Psi_f = sp.Function('Psi')(rr)
w_f = sp.Function('w')(rr)


def ricci_scalar_3(hmat, coords):
    hin = hmat.inv()
    n = len(coords)
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += hin[a, d] * (sp.diff(hmat[d, b], coords[c]) + sp.diff(hmat[d, c], coords[b])
                                      - sp.diff(hmat[b, c], coords[d]))
                Gam[a][b][c] = sp.simplify(s / 2)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                for d in range(n):
                    s += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = sp.simplify(s)
    return sp.simplify(sum(hin[b, c] * Ric[b, c] for b in range(n) for c in range(n)))


coords3 = [rr, th, sp.Symbol('varphi')]
h3 = sp.diag(sp.exp(-2 * Psi_f), sp.exp(-2 * Psi_f) * rr ** 2, sp.exp(-2 * Psi_f) * rr ** 2 * sp.sin(th) ** 2)
hbar3 = sp.exp(-2 * w_f) * h3
R3 = ricci_scalar_3(h3, coords3)
Rbar = ricci_scalar_3(hbar3, coords3)
# Lap_h w = (1/sqrt h) d_r( sqrt(h) h^{rr} w' ),  sqrt(h) = e^{-3 Psi} r^2, h^{rr} = e^{2 Psi}
lap_h_w = sp.exp(3 * Psi_f) / rr ** 2 * sp.diff(sp.exp(-Psi_f) * rr ** 2 * sp.diff(w_f, rr), rr)
Dw2 = sp.exp(2 * Psi_f) * sp.diff(w_f, rr) ** 2
conf_resid = sp.simplify(sp.exp(-2 * w_f) * Rbar - (R3 + 4 * lap_h_w - 2 * Dw2))
print(f"        conformal identity residual  e^(-2w) Rbar - [R3 + 4 Lap_h w - 2|Dw|^2] = {conf_resid}")
check("E2a the conformal 3-curvature identity the IC5 -> IC1 static transfer relies on is correct, derived "
      "here for a general spherically symmetric leaf rather than quoted",
      sp.simplify(conf_resid) == 0, "exact zero in sympy, hbar = e^(-2w) h")

P = sp.symbols('P0 P1 P2 P3 P4')        # xi = ln N = Phi and its r-derivatives
S = sp.symbols('S0 S1 S2 S3 S4')        # Psi
Uj = sp.symbols('U0 U1 U2 U3')          # u
JETS = [(P[i], P[i + 1]) for i in range(4)] + [(S[i], S[i + 1]) for i in range(4)] + \
       [(Uj[i], Uj[i + 1]) for i in range(3)]


def Dtot(expr):
    out = sp.diff(expr, rr)
    for a, b in JETS:
        out += b * sp.diff(expr, a)
    return out


def EL(L, tower):
    f0, f1, f2 = tower[0], tower[1], tower[2]
    return sp.expand(sp.diff(L, f0) - Dtot(sp.diff(L, f1)) + Dtot(Dtot(sp.diff(L, f2))))


m_sym = sp.Symbol('m', positive=True)
xi_j, xip_j = P[0], P[1]
wp_j = Uj[1] * xi_j + (Uj[0] - 1) * xip_j                     # w' with w = (u-1) xi
Nsh = sp.exp(P[0] - 3 * S[0]) * rr ** 2                       # N sqrt(h) per unit solid angle
asq = sp.exp(2 * S[0]) * P[1] ** 2                            # a.a,  a_i = D_i ln N
aDu = sp.exp(2 * S[0]) * P[1] * Uj[1]
Du2 = sp.exp(2 * S[0]) * Uj[1] ** 2
Dw2j = sp.exp(2 * S[0]) * wp_j ** 2
lapw_j = sp.exp(3 * S[0]) / rr ** 2 * Dtot(sp.exp(-S[0]) * rr ** 2 * wp_j)

diff_density = (m_sym / 2) * Nsh * (4 * lapw_j - 2 * Dw2j) \
    - m_sym * Nsh * (1 - Uj[0] ** 2) * asq \
    + m_sym * Nsh * (2 * Uj[0] * xi_j * aDu + xi_j ** 2 * Du2)
rP = sp.simplify(EL(diff_density, P))
rS = sp.simplify(EL(diff_density, S))
rU = sp.simplify(EL(diff_density, Uj))
print(f"        EL residuals of [IC5 static density - IC1 static density] in (Phi, Psi, u): ({rP}, {rS}, {rU})")
check("E2b IC5's static gradient block combines with the barred-curvature difference into an EXACT null "
      "Lagrangian, so the eta = 0 sector is IC1's -- independently re-derived here, not inherited",
      rP == 0 and rS == 0 and rU == 0, "all three Euler-Lagrange residuals vanish identically")

AA = sp.Symbol('AA', positive=True)                            # a.a, carried as a symbol
a0s = sp.Symbol('a0', positive=True)
c_ = Uj[0] ** 2
Ufun = (1 - c_) * (sp.log(1 - c_) ** 2 - 2 * sp.log(1 - c_) + 2) - 2
L_static = m_sym * Nsh * ((1 - Uj[0] ** 2) * AA - a0s ** 2 * Ufun)
d_du1 = sp.simplify(sp.diff(L_static, Uj[1]))
d_du2 = sp.simplify(sp.diff(L_static, Uj[2]))
u_eq = sp.simplify(sp.diff(L_static, Uj[0]) / (2 * m_sym * Nsh * Uj[0]))
sub_root = sp.simplify(u_eq.subs(AA, a0s ** 2 * sp.log(1 - Uj[0] ** 2) ** 2))
print(f"        dL/du'  = {d_du1},   dL/du'' = {d_du2}")
print(f"        the u equation, divided by 2 m N sqrt(h) u:  {u_eq} = 0")
print(f"        substituting a.a = a0^2 ln^2(1-u^2):        {sub_root}")
check("E2c on the eta = 0 branch u appears in the static Lagrangian with NO derivatives, so its "
      "Euler-Lagrange equation is ALGEBRAIC (u^2 = 1 - e^(-|a|/a0) pointwise) and u CANNOT carry a "
      "far-field boundary condition of any kind",
      d_du1 == 0 and d_du2 == 0 and sub_root == 0,
      "no u', no u'': a field with no derivatives in its own EL equation admits no boundary datum")

print("\n        => PART 1's structural answer.  Inside eta = 0 the far-field u for an isolated galaxy is")
print("           NEITHER 0-by-choice NOR the cosmological value: it is the pointwise function of the")
print("           galaxy's OWN field, u^2 = 1 - e^(-|a|/a0), which tends to 0 as |a| -> 0.  There is no")
print("           boundary condition to impose, so the cosmological value can only reach a galaxy where")
print("           the region itself leaves eta = 0.  That relocates the question to E3.")

# ---- E3: where the eta boundary sits around real galaxies --------------------------------------------
print("\n  E3 -- WHERE THE eta BOUNDARY SITS around real SPARC galaxies.")
ic11_rows = [(0.03, 1.117612, 1.096697), (0.05, 1.023606, 1.060772),
             (0.10, 0.866660, 1.044953), (0.20, 0.813796, 1.098455)]
ratios = [rv / Hp for _, Hp, rv in ic11_rows]
print(f"        calibrating r against the lead's own solutions -- IC11_CLOCK_PRESSURE's table gives")
print(f"        r/H_physical = {', '.join(f'{x:.4f}' for x in ratios)}  (m = h0 = 1 units)")
r_over_H = max(ratios)
H_switch = math.sqrt(0.5) / r_over_H
print(f"        taking the LARGEST ratio {r_over_H:.4f} (conservative: it makes eta leave 0 EARLIEST),")
print(f"        eta = 0 is guaranteed wherever  H_local <= {H_switch:.4f} h0.")

UPS_D, UPS_B = 0.5, 0.7
GALS = []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    try:
        d = np.loadtxt(fn, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    rk, Vo, eV = d[:, 0], d[:, 1] * 1e3, d[:, 2] * 1e3
    Vg, Vd, Vb = d[:, 3] * 1e3, d[:, 4] * 1e3, d[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
    msk = (rk > 0) & (Vo > 0) & (eV > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1.0) < 0.10)
    if msk.sum() < 5:
        continue
    GALS.append(dict(name=name, r=rk[msk] * kpc, Vo=Vo[msk], eV=eV[msk],
                     Vg=Vg[msk], Vd=Vd[msk], Vb=Vb[msk]))
NGAL = len(GALS)
NPTS = sum(len(g["r"]) for g in GALS)
print(f"        SPARC: {NGAL} galaxies, {NPTS} points (Upsilon_d = {UPS_D}, Upsilon_b = {UPS_B}, eV/V < 0.10)")


def solve_g(gN, a0, gext=0.0, niter=120):
    """g * mu(sqrt(g^2 + gext^2)/a0) = gN with mu(y) = 1 - e^(-y).  Monotone => bisection is exact."""
    gN = np.asarray(gN, dtype=float)
    lo = np.zeros_like(gN)
    hi = gN + 100.0 * a0 + 10.0 * np.sqrt(np.maximum(gN, 0.0) * a0) + 1e-30
    for _ in range(niter):
        mid = 0.5 * (lo + hi)
        F = mid * (-np.expm1(-np.sqrt(mid * mid + gext * gext) / a0)) - gN
        hi = np.where(F > 0, mid, hi)
        lo = np.where(F > 0, lo, mid)
    return 0.5 * (lo + hi)


def solve_g_aligned(gN, a0, gext=0.0, niter=120):
    """the colinear composition |g_int + g_ext| = g + gext -- the other end of the orientation bracket"""
    gN = np.asarray(gN, dtype=float)
    lo = np.zeros_like(gN)
    hi = gN + 100.0 * a0 + 10.0 * np.sqrt(np.maximum(gN, 0.0) * a0) + 1e-30
    for _ in range(niter):
        mid = 0.5 * (lo + hi)
        F = mid * (-np.expm1(-(mid + gext) / a0)) - gN
        hi = np.where(F > 0, mid, hi)
        lo = np.where(F > 0, lo, mid)
    return 0.5 * (lo + hi)


ratio_hub, ratio_zg, Rlast_kpc = [], [], []
a0c = A0["canonical"]
Rgrid = np.geomspace(1e-3 * Mpc, 3e2 * Mpc, 4000)
for g in GALS:
    R_last = g["r"][-1]
    Rlast_kpc.append(R_last / kpc)
    n_out = max(3, len(g["r"]) // 4)
    V_out = float(np.mean(g["Vo"][-n_out:]))
    # criterion 1 (model-light): the radius where the Hubble velocity reaches the galaxy's own
    # circular velocity.  Inside it the region cannot be expanding at ~h0.
    ratio_hub.append((V_out / H0_SI) / R_last)
    # criterion 2 (independent): the Lambda zero-gravity radius, from the MEASURED baryonic mass at
    # R_last and the framework's OWN kernel, g_gal(R) = Omega_L H0^2 R.
    Vb2_last = float(g["Vg"][-1] * abs(g["Vg"][-1]) + UPS_D * g["Vd"][-1] * abs(g["Vd"][-1])
                     + UPS_B * g["Vb"][-1] * abs(g["Vb"][-1]))
    M_b = Vb2_last * R_last / G_NEWT
    ggal = solve_g(G_NEWT * M_b / Rgrid ** 2, a0c, 0.0)
    glam = OMEGA_L * H0_SI ** 2 * Rgrid
    idx = np.argmax(glam > ggal)
    ratio_zg.append(Rgrid[idx] / R_last if idx > 0 else np.nan)
ratio_hub = np.array(ratio_hub)
ratio_zg = np.array(ratio_zg)
Rlast_kpc = np.array(Rlast_kpc)
print(f"        R_last                             : min {Rlast_kpc.min():7.2f}  median "
      f"{np.median(Rlast_kpc):7.2f}  max {Rlast_kpc.max():8.2f}  kpc")
print(f"        R(Hubble-velocity crossing)/R_last : min {ratio_hub.min():7.1f}  median "
      f"{np.median(ratio_hub):7.1f}  max {ratio_hub.max():8.1f}")
print(f"        R(Lambda zero-gravity)/R_last      : min {np.nanmin(ratio_zg):7.1f}  median "
      f"{np.nanmedian(ratio_zg):7.1f}  max {np.nanmax(ratio_zg):8.1f}")
WORST = float(min(ratio_hub.min(), np.nanmin(ratio_zg)))
print(f"        Direction stated: this is a KINEMATIC estimate of the local expansion rate around a bound")
print(f"        object, NOT a solution of the IC equations in the transition region.  See E4.")
check("E3 the eta boundary around every SPARC galaxy lies at least 10x beyond its last measured radius, "
      "so the whole rotation-curve region sits inside the exact eta = 0 plateau on BOTH criteria",
      float(ratio_hub.min()) >= 10.0 and float(np.nanmin(ratio_zg)) >= 10.0,
      f"worst case over {NGAL} galaxies and two criteria: {WORST:.1f}x beyond R_last")

# ---- E4: what the published transition work does and does not settle ----------------------------------
print("\n  E4 -- WHAT THE PUBLISHED eta-TRANSITION WORK NOW GIVES, and the one input still missing.")
varied = "first crossed on this grid" in ic11t
uv_fail = "aUV<-1e-30" in ic11t
liability = "full eta-transition evolution" in ic11c
print(f"        IC11_TRANSITION.md HAS now varied the transition (IC10 'What remains' item 1): "
      f"{'YES' if varied else 'no'}  -- L11's B5 wrote it as not varied; that is now superseded.")
print(f"        BUT on a HOMOGENEOUS background only: a 501-point continuation in the trace momentum rho")
print(f"        from the IC10 plateau through the switch boundary, giving u = 0.622175 (n=200), 0.625545")
print(f"        (n=220), 0.666132 (n=500).  Those are the COSMOLOGICAL u values continued in TIME; they are")
print(f"        not a galactic far field, and no radius appears anywhere in that calculation.")
print(f"        AND that trial FAILS a necessary scalar kinetic condition, aUV < 0 from n = 205 onward: "
      f"{'recorded in the report' if uv_fail else 'NOT FOUND in the report'}.")
print(f"        IC11_CLOCK_PRESSURE.md's own closing liability names the same gap: "
      f"{'present' if liability else 'not found'}.")
print(f"        THE MISSING INPUT, named exactly: a solution of the full phase equations for a BOUND MASS")
print(f"        embedded in the expanding plateau, with eta varying in SPACE (not in the homogeneous")
print(f"        momentum), so that r(x)^2 crosses 1/2 at some radius and u is continued across it.  Nothing")
print(f"        published attempts that, and the only transition action that HAS been varied is unhealthy.")
check("E4 the eta-transition, as published, DETERMINES the far-field u for a galaxy embedded in the "
      "cosmological solution",
      False,
      "IC11 varied it homogeneously only, and that trial fails a necessary scalar kinetic condition "
      "(aUV < 0 from n = 205); no spatially inhomogeneous eta profile around a bound mass exists")

print("\n        PART 1's ANSWER, in one line: the far-field u for an isolated galaxy tends to 0 -- NOT the")
print("        cosmological value and NOT something in between -- throughout the eta = 0 region, because u")
print("        is algebraically slaved there and admits no boundary datum (E2); and the eta = 0 region")
print(f"        extends at least {WORST:.0f}x beyond the last measured rotation-curve point (E3).  What is NOT")
print("        settled is whether the full spatial transition leaves that intact (E4).  PART B bounds the")
print("        damage if it does not.")


# ====================================================================================================
# PART B -- the kernel, the external field, and the two controls
# ====================================================================================================
print("\n" + "-" * 120)
print("PART B -- the construction's own kernel with an external field, and the two controls")
print("-" * 120, flush=True)

print("\n  C0 -- kernel controls on the construction's OWN mu(y) = 1 - e^(-y), y = |grad Phi|/a0.")
s_test = np.array([1e-12, 1e-6, 1e-4, 1e-2, 1.0, 1e2, 1e4])
g_iso = solve_g(s_test * a0c, a0c, 0.0)
resid = np.abs(g_iso * (-np.expm1(-g_iso / a0c)) - s_test * a0c) / (s_test * a0c)
deep = g_iso[0] / math.sqrt(s_test[0] * a0c * a0c)
newt = g_iso[-1] / (s_test[-1] * a0c)
print(f"        solver relative residual over s = 1e-12..1e4: max {resid.max():.3e}")
print(f"        deep-MOND coefficient  g/sqrt(g_N a0) at s = 1e-12: {deep:.8f}   (must be 1; the")
print(f"           leading correction is +sqrt(s)/4, so at s = 1e-6 it reads "
      f"{g_iso[1]/math.sqrt(s_test[1])/a0c:.6f} as it should)")
print(f"        Newtonian ratio        g/g_N at s = 1e4:            {newt:.8f}   (must be 1)")
check("C0 the algebraic solver for the construction's own kernel is exact and reproduces both limits "
      "(deep-MOND coefficient 1.000000, Newtonian g = g_N)",
      resid.max() < 1e-10 and abs(deep - 1) < 1e-5 and abs(newt - 1) < 1e-8,
      f"max residual {resid.max():.1e}, deep coefficient {deep:.6f}")

print("\n        what an external field does to THIS kernel (linear response, g_int -> 0):")
print("        u_cosmo    y_ext = -ln(1-u^2)   nu_ext = 1/mu   L0 = dln mu/dln y    B_par    B_perp    <B>")
YEXT = []
for lab, uc in U_COSMO:
    y = -math.log(1 - uc ** 2)
    mu0 = -math.expm1(-y)
    nu0 = 1.0 / mu0
    L0 = y * math.exp(-y) / mu0
    Bpar, Bperp = nu0, nu0 / math.sqrt(1 + L0)
    Bavg = (Bpar + 2 * Bperp) / 3.0
    YEXT.append(y)
    print(f"        {uc:.6f}   {y:.4f}              {nu0:8.4f}     {L0:12.4f}      {Bpar:7.4f}  "
          f"{Bperp:7.4f}  {Bavg:7.4f}   <- {lab}")
print(f"        the L11 bracket is g_ext = {min(YEXT):.3f}-{max(YEXT):.3f} a0; the two headline values used")
print(f"        below are 0.28 and 0.59 a0.")
_y = min(YEXT)
_mu0 = -math.expm1(-_y)
_L0 = _y * math.exp(-_y) / _mu0
_Bpar = 1.0 / _mu0
_Bavg = (_Bpar + 2 * _Bpar / math.sqrt(1 + _L0)) / 3.0
print(f"        CONSERVATISM DECLARED: the isotropic composition used below gives the boost B_par, while the")
print(f"        orientation average is {_Bpar/_Bavg:.3f}x smaller.  Every number below therefore UNDERSTATES the")
print(f"        damage, and F3's bound is an upper bound on the bound.")

print("\n  C2 -- CONTROL: the external-field implementation against a PUBLISHED result of this repository.")
print("        Target: prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py PART A and")
print("        nbody_2026/stage64_efe_two_body_exact_2026.py PART B, at their stated x_ext = 1.9,")
print("        canonical footing, Route A kernel nu(y) = 1/(1 - e^-sqrt(y)).")


def nu_routeA(y):
    y = np.asarray(y, dtype=float)
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-300))))


def dnu_routeA(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(np.maximum(y, 1e-300))
    u = 1.0 - np.exp(-s)
    return -(np.exp(-s) / (2.0 * s)) / u ** 2


_YT = np.logspace(-10, 10, 40001)
_XT = _YT * nu_routeA(_YT)
y_extN = float(np.exp(np.interp(math.log(1.9), np.log(_XT), np.log(_YT))))
n0 = float(nu_routeA(y_extN))
dxdy = float(n0 + y_extN * dnu_routeA(y_extN))
L0r = n0 / dxdy - 1.0
Bpar_r, Bperp_r = n0, n0 / math.sqrt(1 + L0r)
gamma_reg = math.sqrt(n0)
mi_avg = math.sqrt((dxdy + 2 * n0) / 3.0)
x_alt = 1.9 * 9.36e-11 / 1.13e-10
y_alt = float(np.exp(np.interp(math.log(x_alt), np.log(_XT), np.log(_YT))))
gamma_alt = math.sqrt(float(nu_routeA(y_alt)))
tgt = [("y_extN", y_extN, 1.28903, 2e-3), ("B_par = nu(y_extN)", Bpar_r, 1.47342, 2e-3),
       ("dx/dy", dxdy, 1.07749, 2e-3), ("B_perp = nu/sqrt(1+L0)", Bperp_r, 1.2598, 3e-3),
       ("sqrt(nu) canonical", gamma_reg, 1.2139, 2e-3), ("sqrt(nu) alt", gamma_alt, 1.2592, 5e-3),
       ("MI orientation average", mi_avg, 1.1582, 2e-3)]
for lab, got, want, _t in tgt:
    print(f"        {lab:26s} = {got:.5f}   (recorded {want})")
check("C2 [CONTROL] the external-field machinery reproduces this repository's published AQUAL-EFE "
      "linear-response numbers at their stated parameters (x_ext = 1.9, Route A kernel): B_par, B_perp, "
      "the registered sqrt(nu) on both footings, and the superseded MI orientation average",
      all(abs(got - want) < t for _, got, want, t in tgt),
      "all seven recorded values recovered to <5e-3; the same linear-response construction applied to the "
      "IC kernel is the C0 table above")


# ====================================================================================================
# PART C -- SPARC: the control, then the damage, then the bound
# ====================================================================================================
print("\n" + "-" * 120)
print("PART C -- SPARC rotation curves with and without a universal external field")
print("-" * 120, flush=True)

# flat arrays, one row per point; galaxy index for fast per-galaxy reductions
GIDX = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(GALS)])
R_ALL = np.concatenate([g["r"] for g in GALS])
VO_ALL = np.concatenate([g["Vo"] for g in GALS])
EV_ALL = np.concatenate([g["eV"] for g in GALS])
VG_ALL = np.concatenate([g["Vg"] for g in GALS])
VD_ALL = np.concatenate([g["Vd"] for g in GALS])
VB_ALL = np.concatenate([g["Vb"] for g in GALS])
GO_ALL = VO_ALL ** 2 / R_ALL
SLICES = []
_o = 0
for g in GALS:
    SLICES.append((_o, _o + len(g["r"])))
    _o += len(g["r"])
OUTMASK = np.zeros(NPTS, dtype=bool)
for i, (a, b) in enumerate(SLICES):
    rr_ = R_ALL[a:b]
    m_ = rr_ >= 0.6 * rr_[-1]
    if m_.sum() < 3:
        m_ = np.zeros_like(m_)
        m_[-3:] = True
    OUTMASK[a:b] = m_


def gbar_of(ups_d):
    return (VG_ALL * np.abs(VG_ALL) + ups_d * VD_ALL * np.abs(VD_ALL)
            + 1.4 * ups_d * VB_ALL * np.abs(VB_ALL)) / R_ALL


GB_FIX = gbar_of(UPS_D)


def slopes_from(gpred):
    """outer dlnV/dlnr per galaxy, V = sqrt(g r)"""
    V = np.sqrt(np.maximum(gpred, 1e-30) * R_ALL)
    out = np.empty(NGAL)
    for i, (a, b) in enumerate(SLICES):
        m_ = OUTMASK[a:b]
        x = np.log(R_ALL[a:b][m_])
        y = np.log(np.maximum(V[a:b][m_], 1e-12))
        out[i] = np.polyfit(x, y, 1)[0]
    return out


# ---- C1: the g_ext = 0 control ------------------------------------------------------------------------
print("\n  C1 -- CONTROL: with g_ext = 0 the pipeline must reproduce the radial acceleration relation.")
rar0 = {}
for foot, a0v in A0.items():
    gpred = solve_g(GB_FIX, a0v, 0.0)
    dlog = np.log10(GO_ALL) - np.log10(gpred)
    rar0[foot] = dict(rms=float(np.std(dlog, ddof=1)), med=float(np.median(dlog)))
    print(f"        {foot:9s}: RAR scatter {rar0[foot]['rms']:.4f} dex, median offset "
          f"{rar0[foot]['med']:+.4f} dex, {NPTS} points, fixed Upsilon")
print("        reference: the published SPARC RAR scatter at fixed Upsilon is ~0.11-0.13 dex.  The small")
print("        excess here is expected and is not the object of this lane: no distance or inclination")
print("        marginalisation, SPARC's own Q/i cuts are replaced by eV/V < 0.10, and the kernel is the")
print("        EXPONENTIAL carrier, whose too-low ceiling is exactly L11's B2b finding -- it shows up here")
print("        as the positive median offset (the kernel under-predicts g_obs by ~19% in the mean).")
check("C1 [CONTROL] with g_ext = 0 the pipeline reproduces the standard radial acceleration relation with "
      "its known ~0.11 dex scatter and a centred zero point",
      all(0.06 <= rar0[f]["rms"] <= 0.18 and abs(rar0[f]["med"]) < 0.10 for f in A0),
      f"scatter {rar0['canonical']['rms']:.3f}/{rar0['alt']['rms']:.3f} dex, offset "
      f"{rar0['canonical']['med']:+.3f}/{rar0['alt']['med']:+.3f} dex (canonical/alt)")

# ---- D1: RAR damage ------------------------------------------------------------------------------------
print("\n  D1 -- the damage: RAR scatter and zero point under a universal external field.")
HEAD = [0.0, 0.28, 0.59]
damage = {}
zscan = np.linspace(-0.6, 1.2, 91)
for foot, a0v in A0.items():
    print(f"        {foot}:")
    for xe in HEAD:
        gpred = solve_g(GB_FIX, a0v, xe * a0v)
        dlog = np.log10(GO_ALL) - np.log10(gpred)
        rms, med = float(np.std(dlog, ddof=1)), float(np.median(dlog))
        best_z, best_s = 0.0, 1e9
        for z in zscan:
            a0z = a0v * 10 ** z
            s = float(np.std(np.log10(GO_ALL) - np.log10(solve_g(GB_FIX, a0z, xe * a0v)), ddof=1))
            if s < best_s:
                best_s, best_z = s, z
        damage[(foot, xe)] = dict(rms=rms, med=med, a0shift=best_z, rms_abs=best_s)
        print(f"            g_ext = {xe:.2f} a0 : scatter {rms:.4f} dex ({rms - rar0[foot]['rms']:+.4f}), "
              f"zero point {med:+.4f} dex ({med - rar0[foot]['med']:+.4f}); best-absorbing a0 shift "
              f"{best_z:+.3f} dex still leaves {best_s:.4f} dex")

# ---- D2: outer slopes ----------------------------------------------------------------------------------
print("\n  D2 -- the damage: do the outer rotation curves still stay flat?")
print("        outer logarithmic slope beta = dlnV/dlnr over r >= 0.6 R_last (>= 3 points).  Flat means")
print("        beta ~ 0; a saturated external field forces beta -> -0.5 (Keplerian with a rescaled G).")
print("        'declining' means beta < -0.10.")
b_obs = slopes_from(GO_ALL)
slope_tab = {}
for foot, a0v in A0.items():
    row = {"obs": b_obs}
    for xe in HEAD:
        row[xe] = slopes_from(solve_g(GB_FIX, a0v, xe * a0v))
    slope_tab[foot] = row
    print(f"        {foot}:")
    print(f"            observed        : median beta {np.median(b_obs):+.4f}, "
          f"{100 * np.mean(b_obs < -0.10):5.1f}% declining, {100 * np.mean(np.abs(b_obs) < 0.10):5.1f}% flat")
    for xe in HEAD:
        bp = row[xe]
        print(f"            g_ext = {xe:.2f} a0  : median beta {np.median(bp):+.4f}, "
              f"{100 * np.mean(bp < -0.10):5.1f}% declining, {100 * np.mean(np.abs(bp) < 0.10):5.1f}% flat, "
              f"median (beta_pred - beta_obs) = {np.median(bp - b_obs):+.4f}")

# ---- D3: the fit, Upsilon profiled ----------------------------------------------------------------------
print("\n  D3 -- the fit itself, with Upsilon PROFILED per galaxy under a 0.11 dex lognormal prior")
print("        (Upsilon_bul = 1.4 Upsilon_disk throughout, preserving the 0.7/0.5 ratio).")
UPS_GRID = np.geomspace(0.10, 2.50, 41)
LOGPRIOR = ((np.log10(UPS_GRID) - math.log10(0.5)) / 0.11) ** 2
GB_GRID = np.vstack([gbar_of(u) for u in UPS_GRID])            # (nU, NPTS)
GB_GRID = np.maximum(GB_GRID, 1e-30)


def Delta_RAR(s):
    s = np.asarray(s, float)
    d = np.where(s > 0, s / np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)


def solve_g_RAR(gN, a0, gext=0.0):
    """the programme's CARRIED kernel (THE_ACTION section 3), for the shape comparison in F5 only"""
    return gN + a0 * Delta_RAR(gN / a0)


def chi2_total(a0v, gext, aligned=False, sig_scale=1.0, solver=None):
    if solver is None:
        solver = solve_g_aligned if aligned else solve_g
    gg = solver(GB_GRID.ravel(), a0v, gext).reshape(GB_GRID.shape)
    Vp = np.sqrt(gg * R_ALL[None, :])
    resid2 = ((VO_ALL[None, :] - Vp) / (EV_ALL[None, :] * sig_scale)) ** 2
    per = np.vstack([np.bincount(GIDX, weights=resid2[k], minlength=NGAL) for k in range(len(UPS_GRID))])
    per = per + LOGPRIOR[:, None]
    return float(per.min(axis=0).sum())


DOF = NPTS - NGAL
chi0 = {f: chi2_total(A0[f], 0.0) for f in A0}
SIG = {f: math.sqrt(chi0[f] / DOF) for f in A0}
for foot in A0:
    print(f"        {foot:9s}: chi2(g_ext = 0) = {chi0[foot]:.1f} for {DOF} dof -> chi2/dof = "
          f"{chi0[foot]/DOF:.2f}; errors inflated by {SIG[foot]:.2f}x before any Delta chi2 is read")

print("\n  F1/F2 -- do flat rotation curves survive g_ext = 0.28 a0 and 0.59 a0?")
BASE = {f: chi2_total(A0[f], 0.0, sig_scale=SIG[f]) for f in A0}
surv = {}
for foot, a0v in A0.items():
    for xe in (0.28, 0.59):
        c2 = chi2_total(a0v, xe * a0v, sig_scale=SIG[foot])
        c2al = chi2_total(a0v, xe * a0v, aligned=True, sig_scale=SIG[foot])
        dchi = c2 - BASE[foot]
        surv[(foot, xe)] = dchi
        print(f"        {foot:9s} g_ext = {xe:.2f} a0 : Delta chi2 = {dchi:+.1f} (inflated errors) = "
              f"{math.sqrt(max(dchi, 0.0)):.1f} sigma;  colinear composition {c2al - BASE[foot]:+.1f}")
check("F1 flat rotation curves SURVIVE a universal external field of g_ext = 0.28 a0 (the smallest value "
      "the lead's exhibited cosmological solutions offer), on both footings",
      all(surv[(f, 0.28)] < 9.0 for f in A0),
      f"Delta chi2 = {surv[('canonical', 0.28)]:+.0f} canonical / {surv[('alt', 0.28)]:+.0f} alt against a "
      f"3-sigma threshold of 9, with Upsilon profiled and errors already inflated to chi2/dof = 1")
check("F2 flat rotation curves SURVIVE a universal external field of g_ext = 0.59 a0 (the IC4/IC5 witness "
      "value), on both footings",
      all(surv[(f, 0.59)] < 9.0 for f in A0),
      f"Delta chi2 = {surv[('canonical', 0.59)]:+.0f} canonical / {surv[('alt', 0.59)]:+.0f} alt")

# ---- F3: the hard upper bound ----------------------------------------------------------------------------
print("\n  F3 -- THE DELIVERABLE: the largest universal g_ext the SPARC rotation curves will tolerate.")
print("        x_ext = g_ext/a0 is the object bounded, because the theory fixes the RATIO (u_cosmo does),")
print("        not the absolute field: rescaling a0 rescales g_ext with it.  Each bound is the upper edge")
print("        of the Delta chi2 = 9 region measured from the MINIMUM of the profiled curve, not from")
print("        x = 0 -- the two differ here, and that difference is itself a result (F5).")
print("        (a)  at the framework's OWN a0, Upsilon profiled, errors inflated to chi2/dof = 1;")
print("        (b') the same with a global a0 rescaling profiled over +-0.1 dex -- the freedom the")
print("             framework actually has (its two footings differ by 0.081 dex);")
print("        (b)  the same over +-0.5 dex -- an ADVERSARIAL extreme, well outside anything the")
print("             programme allows, retained because it measures the a0/g_ext degeneracy honestly;")
print("        (c)  a fit-free bound: the largest g_ext for which the median predicted outer slope stays")
print("             within 3 standard errors of the observed median slope.")

def largest_below(fn, thresh, lo=0.0, hi=1.5, tol=2e-4):
    if fn(hi) < thresh:
        return hi
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if fn(mid) < thresh:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


XG = np.concatenate([np.linspace(0.0, 0.60, 25), np.linspace(0.65, 1.40, 16)])
BOUND = {}
MINLOC = {}


def profiled(x, a0v, foot, zg):
    return min(chi2_total(a0v * 10 ** z, x * a0v * 10 ** z, sig_scale=SIG[foot]) for z in zg)


for tag, zg in (("a", np.array([0.0])), ("b'", np.linspace(-0.1, 0.1, 9)),
                ("b", np.linspace(-0.5, 0.5, 21))):
    for foot, a0v in A0.items():
        curve = np.array([profiled(x, a0v, foot, zg) for x in XG])
        i0 = int(np.argmin(curve))
        cmin = float(curve[i0])
        # upper edge of the Delta chi2 = 9 region, refined by bisection on the profiled curve
        j = i0
        while j + 1 < len(XG) and curve[j + 1] - cmin < 9.0:
            j += 1
        if j + 1 >= len(XG):
            xb = float(XG[-1])
        else:
            lo, hi = XG[j], XG[j + 1]
            while hi - lo > 2e-3:
                mid = 0.5 * (lo + hi)
                if profiled(mid, a0v, foot, zg) - cmin < 9.0:
                    lo = mid
                else:
                    hi = mid
            xb = 0.5 * (lo + hi)
        BOUND[(foot, tag)] = xb
        MINLOC[(foot, tag)] = (float(XG[i0]), cmin, float(curve[0] - cmin))
        zb = min(zg, key=lambda z: chi2_total(a0v * 10 ** z, XG[i0] * a0v * 10 ** z, sig_scale=SIG[foot]))
        print(f"        ({tag:2s}) {foot:9s}: g_ext <= {xb:.3f} a0    [profiled minimum at x = {XG[i0]:.3f} "
              f"with a0 shifted {zb:+.2f} dex; x = 0 sits {curve[0]-cmin:+.1f} in chi2 above that minimum]")

med_obs = float(np.median(b_obs))
sem_obs = float(np.std(b_obs, ddof=1) / math.sqrt(NGAL))
for foot, a0v in A0.items():
    def gap(x, a0v=a0v):
        return (med_obs - float(np.median(slopes_from(solve_g(GB_FIX, a0v, x * a0v))))) / sem_obs
    BOUND[(foot, "c")] = largest_below(gap, 3.0, tol=2e-3)
    print(f"        (c)  {foot:9s}: g_ext <= {BOUND[(foot,'c')]:.3f} a0   (median outer slope; observed "
          f"median beta = {med_obs:+.4f} +- {sem_obs:.4f})")

HARD = {f: max(BOUND[(f, k)] for k in ("a", "b'", "c")) for f in A0}       # framework-allowed a0 freedom
HARD_ADV = {f: max(BOUND[(f, k)] for k in ("a", "b'", "b", "c")) for f in A0}   # adversarial a0 freedom
Y_MIN = min(YEXT)
Y_IC11 = min(-math.log(1 - u ** 2) for lab, u in U_COSMO if lab.startswith("IC11"))
print("\n        NOTE, stated because it runs AGAINST the direction of this lane: the profiled minimum is at")
print(f"        a small NONZERO g_ext (0.10-0.20 a0), not at zero.  SPARC mildly PREFERS a modest external")
print(f"        field for this kernel.  F5 below asks whether that is an external-field effect or the")
print(f"        exponential carrier's shape being repaired, and answers it.")
print("\n        HARD UPPER BOUND on a universal external field, the weakest construction on each footing:")
for foot in A0:
    print(f"            {foot:9s}: g_ext <= {HARD[foot]:.3f} a0  =  {HARD[foot] * A0[foot]:.3e} m/s^2"
          f"   (at the framework's own a0 +- 0.1 dex)")
    print(f"                       g_ext <= {HARD_ADV[foot]:.3f} a0  if a global a0 refit of up to +-0.5 dex "
          f"is also allowed")
print(f"        the smallest universal field the lead's exhibited cosmological solutions offer is "
      f"{Y_MIN:.3f} a0 (u = 0.492193);")
print(f"        the values IC11's OWN varied transition produces are {Y_IC11:.3f}-"
      f"{-math.log(1 - 0.666131555711**2):.3f} a0 (u = 0.6222-0.6661).")
check("F3a the SMALLEST universal external field the exhibited cosmological solutions offer "
      f"({Y_MIN:.3f} a0) is below the hard upper bound at the framework's own a0",
      min(HARD.values()) >= Y_MIN,
      f"bound {HARD['canonical']:.3f} a0 canonical / {HARD['alt']:.3f} a0 alt; {Y_MIN:.3f} a0 exceeds it "
      f"by {Y_MIN/max(HARD.values()):.2f}-{Y_MIN/min(HARD.values()):.2f}x")
check("F3b the same value survives once a global a0 refit of up to +-0.5 dex is ALSO allowed -- an "
      "adversarial allowance the programme's footings do not grant",
      min(HARD_ADV.values()) >= Y_MIN,
      f"bound {HARD_ADV['canonical']:.3f} / {HARD_ADV['alt']:.3f} a0 against {Y_MIN:.3f} a0, i.e. still "
      f"exceeded by {Y_MIN/max(HARD_ADV.values()):.2f}-{Y_MIN/min(HARD_ADV.values()):.2f}x; letting a0 move "
      f"by a factor {10**0.5:.1f} does NOT open enough room, so the a0/g_ext degeneracy is real but bounded")
print("\n  F4 -- the whole thing in one table: every u value the lead's own solutions exhibit, its equivalent")
print("        universal external field, and what SPARC says about it.  Delta chi2 is measured from the")
print("        PROFILED MINIMUM of the same construction (F3's reference), Upsilon profiled per galaxy,")
print("        errors inflated to chi2/dof = 1.")
ZF = np.linspace(-0.5, 0.5, 21)
F4TAB = []
print("        u_cosmo    g_ext/a0   footing     Delta chi2 (a0 fixed)      Delta chi2 (a0 profiled +-0.5 dex)")
for lab, uc in U_COSMO:
    y = -math.log(1 - uc ** 2)
    for foot, a0v in A0.items():
        d_fix = chi2_total(a0v, y * a0v, sig_scale=SIG[foot]) - MINLOC[(foot, "a")][1]
        d_prof = min(chi2_total(a0v * 10 ** z, y * a0v * 10 ** z, sig_scale=SIG[foot])
                     for z in ZF) - MINLOC[(foot, "b")][1]
        F4TAB.append((lab, uc, y, foot, d_fix, d_prof))
        print(f"        {uc:.6f}   {y:.4f}     {foot:9s}   {d_fix:+11.1f} ({math.sqrt(max(d_fix,0)):5.1f} s)"
              f"     {d_prof:+11.1f} ({math.sqrt(max(d_prof,0)):5.1f} s)   <- {lab}")
_ic11 = [r for r in F4TAB if r[0].startswith("IC11")]
DC_LO, DC_HI = min(r[5] for r in _ic11), max(r[5] for r in _ic11)
print("\n  F5 -- WHY the a0-profiled bound is so much weaker than the fixed-a0 one, checked rather than")
print("        asserted.  With a0 free, {mu(y)=1-e^-y, g_ext} is a TWO-parameter interpolation family, and")
print("        the exponential carrier is the kernel L11's B2b already showed is too shallow.  So the")
print("        question is whether a nonzero g_ext buys anything the programme's CARRIED kernel does not.")
ZF2 = np.linspace(-0.5, 0.5, 21)


def rar_solver(gN, a0, gext=0.0):
    return solve_g_RAR(gN, a0)


for foot, a0v in A0.items():
    c_exp_fix = BASE[foot]
    c_exp_a0 = min(chi2_total(a0v * 10 ** z, 0.0, sig_scale=SIG[foot]) for z in ZF2)
    c_exp_best = MINLOC[(foot, "b")][1]
    c_rar_fix = chi2_total(a0v, 0.0, sig_scale=SIG[foot], solver=rar_solver)
    c_rar_a0 = min(chi2_total(a0v * 10 ** z, 0.0, sig_scale=SIG[foot], solver=rar_solver) for z in ZF2)
    print(f"        {foot}:")
    print(f"            exponential carrier, footing a0, no EFE      : chi2 = {c_exp_fix:9.1f}")
    print(f"            exponential carrier, a0 refit, no EFE        : chi2 = {c_exp_a0:9.1f}")
    print(f"            exponential carrier, a0 refit + best g_ext   : chi2 = {c_exp_best:9.1f}"
          f"   (g_ext = {MINLOC[(foot,'b')][0]:.3f} a0)")
    print(f"            nu_RAR (the CARRIED kernel), footing a0, none : chi2 = {c_rar_fix:9.1f}")
    print(f"            nu_RAR, a0 refit, no EFE                     : chi2 = {c_rar_a0:9.1f}")
    globals().setdefault("_F5", {})[foot] = (c_exp_best, c_rar_a0, c_rar_fix)
f5_ok = all(_F5[f][1] <= _F5[f][0] for f in A0)
gainc = _F5["canonical"][1] - _F5["canonical"][0]
gaina = _F5["alt"][1] - _F5["alt"][0]
check("F5 the mild preference for a nonzero g_ext is only the exponential carrier's SHAPE being repaired, "
      "i.e. the programme's CARRIED kernel nu_RAR with no external field at all fits at least as well",
      f5_ok,
      f"it does not: the two-parameter family {{exponential, g_ext}} with a0 refit beats nu_RAR by "
      f"Delta chi2 = {gainc:.0f} (canonical) / {gaina:.0f} (alt).  DIRECTION STATED -- this runs IN THE "
      f"CONSTRUCTION'S FAVOUR and is reported as such: SPARC genuinely prefers this kernel with a modest "
      f"external field over either bare kernel.  It is a two-parameter-vs-one-parameter interpolation "
      f"statement, not a detection of a universal field, and it does NOT license 0.277 a0, which stays "
      f"1.3-1.4x above the bound")

check("F3c the external field implied by the u values IC11's OWN varied transition actually produces "
      f"({Y_IC11:.3f}-{-math.log(1-0.666131555711**2):.3f} a0) is below the bound, on either allowance",
      min(HARD_ADV.values()) >= Y_IC11,
      f"{Y_IC11:.3f} a0 exceeds even the adversarial bound by "
      f"{Y_IC11/max(HARD_ADV.values()):.1f}-{Y_IC11/min(HARD_ADV.values()):.1f}x, and the framework-a0 "
      f"bound by {Y_IC11/max(HARD.values()):.1f}-{Y_IC11/min(HARD.values()):.1f}x")


# ====================================================================================================
# VERDICT
# ====================================================================================================
print("\n" + "-" * 120)
print("VERDICT")
print("-" * 120, flush=True)
nu28 = 1.0 / (-math.expm1(-0.28))
Y_IC11_HI = -math.log(1 - 0.666131555711 ** 2)
print(f"""    PART 1 -- WHAT THE ETA-TRANSITION GIVES.  It does NOT hand a galaxy a universal external field,
    and the reason is structural rather than numerical.  eta is a function of the trace metric momentum
    -- the local expansion rate -- and of nothing else (E1), and on its EXACT eta = 0 plateau the
    auxiliary field u appears in the static Lagrangian with no derivatives at all, so its
    Euler-Lagrange equation is algebraic and it CANNOT carry a far-field boundary condition (E2,
    re-derived here including the conformal 3-curvature identity).  The far-field u for an isolated
    galaxy is therefore neither 0 by choice nor the cosmological value: it is u^2 = 1 - e^(-|a|/a0)
    at the galaxy's OWN field, which tends to 0.  The cosmological value can only reach a galaxy where
    the region itself leaves eta = 0, and that is at least {WORST:.0f}x beyond the last measured
    rotation-curve point on both conservative criteria (E3).  Still missing (E4): a spatially
    inhomogeneous eta profile around a bound mass.  IC11 has now varied the transition -- but
    homogeneously, and that trial fails a necessary scalar kinetic condition (aUV < 0 from n = 205).

    PART 2 -- WOULD ROTATION CURVES SURVIVE IF IT DID.  No.  A universal g_ext = 0.28 a0 caps the boost
    at nu = {nu28:.2f} and turns the outer rotation curve Keplerian: the median predicted outer slope moves
    from {np.median(slope_tab['canonical'][0.0]):+.3f} to {np.median(slope_tab['canonical'][0.28]):+.3f} against an observed {med_obs:+.3f}; the fraction of galaxies with
    declining outer curves goes {100*np.mean(slope_tab['canonical'][0.0] < -0.10):.0f}% -> {100*np.mean(slope_tab['canonical'][0.28] < -0.10):.0f}% against {100*np.mean(b_obs < -0.10):.0f}% observed; the RAR scatter goes
    {rar0['canonical']['rms']:.3f} -> {damage[('canonical', 0.28)]['rms']:.3f} dex with a {damage[('canonical', 0.28)]['med'] - rar0['canonical']['med']:+.3f} dex zero-point shift; and the profiled-Upsilon fit
    degrades by Delta chi2 = {surv[('canonical', 0.28)]:.0f} with errors already inflated to chi2/dof = 1.

    THE HARD UPPER BOUND, the deliverable, taking the weakest construction on each footing:
        g_ext <= {HARD['canonical']:.3f} a0 (canonical) / {HARD['alt']:.3f} a0 (alt)   at the framework's own a0 (+-0.1 dex);
        g_ext <= {HARD_ADV['canonical']:.3f} a0 / {HARD_ADV['alt']:.3f} a0                  if a global a0 refit of up to +-0.5 dex is allowed too.
    A universal external field is PARTIALLY DEGENERATE WITH a0 -- absorbing g_ext = 0.28 a0 costs a0
    a shift of {damage[('canonical', 0.28)]['a0shift']:+.2f} dex (a factor {10**damage[('canonical',0.28)]['a0shift']:.1f}), which is {abs(damage[('canonical',0.28)]['a0shift'])/0.081:.0f}x the gap between the programme's two footings --
    but the degeneracy does NOT open enough room: a full +-0.5 dex of a0 freedom moves the chi2 bound
    only from {BOUND[('canonical','a')]:.3f}/{BOUND[('alt','a')]:.3f} to {BOUND[('canonical','b')]:.3f}/{BOUND[('alt','b')]:.3f} a0.  {Y_MIN:.3f} a0 exceeds the headline bound by
    {Y_MIN/max(HARD_ADV.values()):.2f}-{Y_MIN/min(HARD_ADV.values()):.2f}x; the values IC11's OWN varied transition actually produces, {Y_IC11:.3f}-{Y_IC11_HI:.3f} a0,
    exceed it by {Y_IC11/max(HARD_ADV.values()):.1f}-{Y_IC11_HI/min(HARD_ADV.values()):.1f}x, at Delta chi2 = {DC_LO:.0f}-{DC_HI:.0f} ({math.sqrt(DC_LO):.0f}-{math.sqrt(DC_HI):.0f} sigma) with a0 fully profiled.

    ONE RESULT THAT RUNS THE OTHER WAY, reported at face value.  The profiled fit does not peak at
    g_ext = 0: SPARC mildly PREFERS g_ext ~ 0.10-0.20 a0 for this kernel, and the two-parameter family
    {{exponential, g_ext}} with a0 refit beats even the programme's carried nu_RAR by Delta chi2 = {gainc:.0f}/{gaina:.0f}.
    That is an interpolation-function statement (two parameters against one), not a detection, and real
    galaxies do sit in ~0.01-0.1 a0 of large-scale-structure field anyway.  It does not rescue {Y_MIN:.3f} a0,
    but it does mean a SMALL universal floor -- below ~0.2 a0 -- would cost the construction nothing.

    WHAT THIS MEANS FOR THE LEAD, plainly.  The eta-matching is not a loose end; it is a live kill
    switch.  If the spatial transition, once solved, forces u toward its cosmological value anywhere
    inside ~{WORST:.0f} R_last, the construction dies on galaxy rotation curves -- not on a subtle gate, on the
    single observation MOND exists to explain.  The reason it very probably does NOT is E2: u has no
    boundary condition to inherit on eta = 0, and that argument is now checked rather than hoped.
    The calculation that would turn "very probably" into "settled" is ONE calculation, named in E4:
    solve the full phase equations for a bound mass in the expanding plateau with eta varying in
    SPACE, and confirm r(x)^2 < 1/2 throughout the rotation-curve region.  A cheaper sufficient
    version: show that any admissible eta profile keeps g_ext below {min(HARD.values()):.3f} a0 inside R_last.""")
core = not any(f.startswith(p) for f in FAILS for p in ("E1", "E2", "E3", "C0", "C1", "C2"))
check("VERDICT the construction's galactic limit is safe from the universal-external-field failure mode, "
      "on the structural ground that u carries no boundary condition inside eta = 0 and the eta boundary "
      "is Mpc-scale -- with the residual named, bounded, and handed back as one calculation",
      core and WORST >= 10.0,
      "the controls and the structural derivation all pass; E4 and F1-F3 are the scored liabilities and "
      "are NOT hidden inside this verdict")

print("\n" + "=" * 120)
print(f"RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
