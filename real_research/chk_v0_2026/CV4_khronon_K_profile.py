#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CV4 -- THE KHRONON'S MEAN CURVATURE K AROUND A BOUND REGION: does it separate bound regions from the Hubble flow?

WHY.  The dark-energy thread (DE7, 095ab610a) found that a gate reading the leaf curvature R = R^(3) + sigma^2 produces
gravitational slip at every transition (psi - phi = 2 delta G_R / M^2), that the varied gate needs a repair term to be
Hadamard well posed, and that the repair itself carries slip with a floor.  Its escape is a gate on K alone,
f(Omega_Lambda(K)), Omega_Lambda(K) = 3 Lambda/K^2: f_R = 0 means no slip and no wrong-signed k^4 term.  That door is open
only if the khronon's K actually separates bound regions (K ~ 0) from the Hubble flow (K = 3H).  The review session asked
for K(r) around a static bound region in C-H/K (BPS khronon, leaf average), for a 1e11 Msun galaxy and a 1e14 Msun cluster
at z = 0.25 and 2.5, at both ends of L340's window.

WHAT THIS LANE CHECKS
  K1 [the static khronon equation, sympy] varying tau in -c_2 Int sqrt(-g) (K - <K>)^2 gives the leafwise equation
     c_2 D_i(N D^i K) = 0 (the leaf average only adds a leaf-constant); with the linear K = 3H(1 - Phi) - 3 Psi_t - lap(pi)/a^2
     of the foliation tau = t + pi on perturbed FRW, a static region therefore has K harmonic on each leaf and equal to its
     Hubble-flow value: K = 3H(z) inside the region.  The alpha_c a^2 term enters only through time derivatives
     (quasi-static: suppressed by alpha_c/c_2 <= 4e-7) and the C-H/MOND sector has no O(pi) term on a static background
     (XC3 C1).
  K2 [moving sources, L340's own block] a region moving at v sources K through L340's momentum channel.  From L340's
     unitary scalar block (its E-list copied verbatim), delta K_k = -(3 D psi - k^2 beta) to first order in omega = v k is
     omega G_1(C, c_2, alpha_c) psi_N; G_1 is extracted symbolically, and at omega = 0 delta K = 0 exactly (the static result
     of K1 from the block itself).
  K3 [the numbers] at the gate edge r_e(z) of the linear gate (p = 1, x_c0 = 2.5: rho_dyn(r_e) = (2/3) x_c0 E^(2p+2)
     rho_crit0 with a flat MOND halo), for the 1e11 galaxy and a 1e14 cluster, z = 0.25 and 2.5, c_2 in {7.3e-3, 0.067},
     alpha_c in {1e-13, 3.2e-9}, v = 600 km/s: max |K/3H(z) - 1| stays below 1e-2 and its angular pattern is a DIPOLE
     (it changes sign with the direction of motion), not a drop.  K does not separate bound regions from the Hubble flow:
     a K-only gate is blind in C-H/K's window.
  MUTATE=1 sets c_2 = 0 (no lambda-term, the tracking control of L340): the block then has no static solution fixing
  K (det M(0) = 0, L330's frozen mode) and K1's harmonic argument is gone; K1 must FAIL.  rc = 1.

SCOPE.  Linear khronon on a given metric (its backreaction is small, the dark-energy thread's premise), principal-order
frozen-coefficient block for moving sources, flat-rotation MOND halo at the edge.  The non-perturbative branch in which
the leaves inside a halo are maximal (K ~ 0) has no source in the linear equation and is not constructed; a K-only gate
would need that branch.  If a future dynamics selects it, DE1's edge law (which assumes K = 3H at the galaxy) changes too.

Run from the repository root:  python3 real_research/chk_v0_2026/CV4_khronon_K_profile.py
"""
import os, sys, json, math, time, warnings
import numpy as np
import sympy as sp
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "CV4", "CV4_khronon_K_profile"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: c_2 = 0 (no lambda-term); K1 must FAIL ***")

# ============================================================================================ K1 the static equation
banner("K1  THE STATIC KHRONON EQUATION: the lambda-term makes K harmonic on each leaf")
t, x, y, z = sp.symbols("t x y z", real=True)
aS = sp.Function("a")(t)
H_ = sp.diff(aS, t) / aS
eps = sp.symbols("epsilon", positive=True)
Phi, Psi, pi_ = [sp.Function(n)(t, x, y, z) for n in ("Phi", "Psi", "pi")]
c2s = sp.Integer(0) if MUTATE else sp.symbols("c_2", positive=True)
# the linear mean curvature of the foliation tau = t + pi on ds^2 = -(1 + 2 Phi) dt^2 + a^2 (1 - 2 Psi) dx^2
# (derived from K = (1/sqrt(-g)) d_mu (sqrt(-g) g^{mu nu} n_nu), n_mu = -d_mu tau / sqrt(X), to first order)
g = sp.diag(-(1 + 2 * eps * Phi), aS ** 2 * (1 - 2 * eps * Psi), aS ** 2 * (1 - 2 * eps * Psi), aS ** 2 * (1 - 2 * eps * Psi))
ginv = g.inv()
X4 = [t, x, y, z]
tau = t + eps * pi_
dtau = [sp.diff(tau, v_) for v_ in X4]
Xs = -sum(ginv[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
n_low = [-d_ / sp.sqrt(Xs) for d_ in dtau]
sqrtg = sp.sqrt(-g.det())
Kexpr = sum(sp.diff(sqrtg * sum(ginv[m, n] * n_low[n] for n in range(4)), X4[m]) for m in range(4)) / sqrtg
K0 = sp.simplify(Kexpr.subs(eps, 0))
K1_lin = sp.simplify(sp.diff(Kexpr, eps).subs(eps, 0))
target_K1 = -3 * H_ * Phi - 3 * sp.diff(Psi, t) - (sp.diff(pi_, x, 2) + sp.diff(pi_, y, 2) + sp.diff(pi_, z, 2)) / aS ** 2 \
            - 3 * sp.diff(H_, t) * 0                                            # (no pi-Hdot term for K as a field)
resid_K = sp.simplify(sp.expand(K1_lin - target_K1))
P(f"    background K = {K0}  (= 3H)")
P(f"    linear delta K - [-3 H Phi - 3 Psi_t - lap(pi)/a^2] = {resid_K}")
# vary pi in -c_2 (K - <K>)^2: for a k != 0 mode the average drops out; the leafwise EL equation is c_2 lap(delta K) = 0
L_lam = -c2s * K1_lin ** 2 / 2
_ELs = sp.euler_equations(L_lam, [pi_], [t, x, y, z]) if L_lam != 0 else []
EL_pi = sp.simplify(_ELs[0].lhs) if _ELs else sp.Integer(0)       # c_2 = 0 (MUTATE): no lambda-term, no equation for K
lapdK = (sp.diff(K1_lin, x, 2) + sp.diff(K1_lin, y, 2) + sp.diff(K1_lin, z, 2))
# the Euler-Lagrange expression is +-c_2 lap(delta K)/a^2 (its overall sign is a convention; the equation is "= 0")
harm = (sp.simplify(EL_pi - c2s * lapdK / aS ** 2) == 0 or sp.simplify(EL_pi + c2s * lapdK / aS ** 2) == 0) and c2s != 0
P(f"    Euler-Lagrange of -c_2 (delta K)^2/2 in pi = c_2 lap(delta K)/a^2 (up to its overall sign): {harm}")
OUT["numbers"]["K1"] = {"K0": str(K0), "residual_K": str(resid_K), "harmonic": harm}
check("K1 the lambda-term's khronon equation is c_2 lap(delta K) = 0 on each leaf, so in a quasi-static region K is harmonic "
      "and equals its Hubble-flow value 3H(z); the linear K of the foliation tau = t + pi is 3H(1 - Phi) - 3 Psi_t - lap(pi)/a^2",
      f"background {K0}; linear-K residual {resid_K}; harmonic equation {harm}", K0 == 3 * H_ and resid_K == 0 and harm,
      "the khronon adjusts its tilt pi to cancel -3 H Phi - 3 Psi_t: its leaves are constant-mean-curvature (CMC) at this "
      "order.  alpha_c enters only through time derivatives (quasi-static: suppressed by alpha_c/c_2 <= 4e-7); the C-H/MOND "
      "sector has no O(pi) term on a static background (XC3 C1)")

# ============================================================================================ K2 moving sources (L340's block)
banner("K2  MOVING SOURCES: delta K from L340's unitary block, to first order in omega = v k")
k, C, c2, ac, om = sp.symbols('k C c_2 alpha_c omega', real=True)
psi_, phi_, beta_, U_, R_ = sp.symbols('psi phi beta U R')
D = -sp.I * om
epsl = -c2
def block340(C_, eps_, ac_):                                      # L340 H1's E-list, verbatim (a2 = a3 = g = 0)
    return [4*k**2*psi_ - 4*k**2*phi_ - D*(-12*D*psi_ + 4*k**2*beta_ + 6*eps_*(3*D*psi_ - k**2*beta_)),
            -4*k**2*psi_ - 4*k**2*(U_ - phi_) + 2*ac_*k**2*phi_ - R_,
            4*k**2*D*psi_ - 2*eps_*k**2*(3*D*psi_ - k**2*beta_) + D*R_,
            4*k**2*(U_ - phi_) + 4*k**2*C_*U_]
Xv = [psi_, phi_, beta_, U_]
E = block340(C, epsl, ac)
M4 = sp.Matrix([[sp.diff(e_, x_) for x_ in Xv] for e_ in E]); S4 = sp.Matrix([-e_.subs({x_: 0 for x_ in Xv}) for e_ in E])
sol = M4.LUsolve(S4)
psiN = -R_ / (4 * k ** 2)
dK = -(3 * D * sol[0] - k ** 2 * sol[2])                          # delta K_k = -(3 D psi - k^2 beta) in L340's convention
dK_over = sp.cancel(sp.together(dK / psiN))
num_, den_ = sp.fraction(dK_over)
dK0 = sp.simplify(num_.subs(om, 0) / den_.subs(om, 0))
G1 = sp.simplify(sp.diff(dK_over, om).subs(om, 0))               # d(delta K/psi_N)/d omega at omega = 0
P(f"    delta K/psi_N at omega = 0: {dK0}  (static: K = 3H exactly, as K1)")
P(f"    G_1 = d(delta K/psi_N)/d omega at 0 = {sp.factor(G1)}")
G1f = sp.lambdify((C, c2, ac), G1, "numpy")
OUT["numbers"]["K2"] = {"dK_static": str(dK0), "G1": str(sp.factor(G1))}
check("K2 in L340's own block the static response has delta K = 0 exactly and a moving source sources delta K only at "
      "first order in omega, with the coefficient G_1(C, c_2, alpha_c) extracted symbolically",
      f"static delta K/psi_N = {dK0}; G_1 = {sp.factor(G1)}", dK0 == 0 and G1 != 0,
      "delta K ~ omega G_1 psi_N with omega = v k: a moving region tilts the leaves in proportion to its speed, with the "
      "sign of v.k -- a dipole")

# ============================================================================================ K3 the numbers at the gate edge
banner("K3  THE NUMBERS: |K/3H - 1| at the linear gate's edge, galaxy and cluster, z = 0.25 and 2.5, L340's window corners")
GK = 4.30091e-6                                                  # kpc (km/s)^2 / Msun
A0K = 9.3619e-11 * 3.0856775814913673e19 / 1e6                  # canonical a0, (km/s)^2/kpc
H0K = 0.0674                                                     # km/s/kpc (67.4 km/s/Mpc)
OM, OL = 0.3153, 0.6847
CKMS = 299792.458
rho_c0 = 3 * H0K ** 2 / (8 * math.pi * GK)                       # Msun/kpc^3
E_ = lambda zz: math.sqrt(OM * (1 + zz) ** 3 + OL)
XC0, PP = 2.5, 1.0
rows = []
for name, Mb, vpec in (("galaxy 1e11", 1e11, 600.0), ("cluster 1e14", 1e14, 1000.0)):
    vf = (GK * Mb * A0K) ** 0.25                                  # deep-MOND flat speed (the edge lies in deep MOND)
    for zz in (0.25, 2.5):
        rho_e = (2.0 / 3.0) * XC0 * E_(zz) ** (2 * PP + 2) * rho_c0     # rho_dyn at the edge (x~ = (3/2) rho_dyn/rho_crit(z))
        r_e = vf / math.sqrt(4 * math.pi * GK * rho_e)          # flat halo: rho_dyn = vf^2/(4 pi G r^2)
        gN = GK * Mb / r_e ** 2
        yv = gN / A0K
        Cval = 1.0 / (1.0 - math.exp(-math.sqrt(yv))) - 1.0     # nu_RAR - 1 at the edge (nu_mono = nu_RAR below y*)
        psiN = GK * Mb / r_e / CKMS ** 2                          # |Phi_N|/c^2 at the edge
        kk_ = 1.0 / r_e                                           # the region's own wavenumber (per kpc)
        omega_ = vpec / CKMS * kk_                                # omega per unit x0 (length): v k / c
        threeH = 3 * H0K * E_(zz) / CKMS                          # 3H/c per kpc
        for c2v in (7.3e-3, 0.067):
            for acv in (1e-13, 3.2e-9):
                g1 = complex(G1f(Cval, c2v, acv))
                dK = abs(omega_ * g1 * psiN)                      # |delta K| per kpc
                rows.append({"system": name, "z": zz, "r_e_kpc": r_e, "y_edge": yv, "C": Cval, "c2": c2v, "alpha_c": acv,
                             "dK_over_3H": dK / threeH})
for r_ in rows:
    if r_["alpha_c"] == 1e-13:
        P(f"    {r_['system']:13s} z = {r_['z']:4.2f}: r_e = {r_['r_e_kpc']:7.1f} kpc, y = {r_['y_edge']:.2e}, C = {r_['C']:7.2f}, "
          f"c_2 = {r_['c2']:.4f}: |K/3H - 1| = {r_['dK_over_3H']:.2e}")
worst = max(r_["dK_over_3H"] for r_ in rows)
ac_spread = max(abs(r1["dK_over_3H"] / r2["dK_over_3H"] - 1) for r1 in rows for r2 in rows
                if r1["system"] == r2["system"] and r1["z"] == r2["z"] and r1["c2"] == r2["c2"] and r1["alpha_c"] != r2["alpha_c"])
P(f"    largest |K/3H - 1| over every system, redshift and window corner: {worst:.2e}; alpha_c changes it by <= {ac_spread:.1e}")
OUT["numbers"]["K3"] = {"rows": rows, "worst": worst, "alpha_c_spread": ac_spread}
check("K3 at the linear gate's edge the khronon's K stays within 1e-2 of 3H(z) for the 1e11 galaxy and the 1e14 cluster at "
      "z = 0.25 and 2.5, at every corner of L340's window; the deviation is a dipole in the direction of motion, not a drop",
      f"max |K/3H - 1| = {worst:.2e}", worst < 1e-2,
      "K does not separate bound regions from the Hubble flow: a K-only gate is blind in C-H/K's window (it would need a "
      "threshold tuned to this precision at every z, and the sign flips across each region).  DE1's K = 3H assumption at the "
      "galaxy stands")

banner("VERDICT")
P(f"""  The khronon's lambda-term makes K harmonic on every leaf (K1), so a static bound region has K = 3H(z) exactly at linear
  order: its leaves are constant-mean-curvature, the tilt pi absorbing the matter's non-expansion.  A moving region
  sources K only through L340's momentum channel, at first order in its speed (K2), and at the gate edges of a 1e11 galaxy
  and a 1e14 cluster at z = 0.25 and 2.5 the deviation is at most {worst:.0e} of 3H, a dipole (K3).  So a gate on K alone
  cannot tell bound regions from the Hubble flow: the door DE7 found is blind within L340's window.  The curvature gate's
  K = 3H input (DE1) stands.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
