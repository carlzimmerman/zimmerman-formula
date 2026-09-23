#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KM1 -- CAN THE L297 KHRONON CARRY A MOVING GALAXY'S PHANTOM?  The first computation named in
real_research/reviews/THE_THEORY_AS_IT_STANDS_2026-09-22.md sec. 4 ("whether [L297's khronon, lambda - 1 = c2 ~ 2.5e-5]
can carry a galaxy's phantom at 100-300 km/s inside the alpha_1 and alpha_2 bounds"), which L330 left OPEN.
Support computation (the field-theory lane is led elsewhere; no file of that lane is edited).

SETUP.  Khronometric gravity in unitary gauge (Blas-Pujolas-Sibiryakov), the khronon of L297 at c13 = 0:
    S = (1/16 pi G) Int N sqrt(gamma) [ K_ij K^ij - lambda K^2 + xi R3 + alpha a_i a^i ] + S_m,
    lambda - 1 = eps = c2, alpha = c14, xi = 1; L280's equal-speed locus c2 = c14/(1 - 2 c14) (alpha_2 = 0 exactly,
    alpha_1 = -4 c14), c14 in [1e-5, 2.5e-5].
  Scalar perturbations: N = 1 + phi, N_i = d_i B, gamma_ij = (1 - 2 psi) delta_ij + 2 d_i d_j E.  Matter couples as
  -rho phi + J.grad(B) (+ O(w^2) stresses).  THE PHANTOM: an energy density rho_ph that moves with the galaxy but
  carries NO momentum in the preferred frame (the leaf-projected MOND scalar, T^phi_0i = 0 -- L330 M5), and no
  anisotropic stress (L279: lensing = dynamics, static).

WHAT THIS LANE SHOWS
  C1 THE QUADRATIC ACTION AND ITS EQUATIONS, derived symbolically (R3 from the conformally flat 3-metric, no hand
     expansion); E enters only through sigma = B - E_dot (spatial-gauge invariance), so its equation is the time
     derivative of the sigma equation.
  C2 CONTROL (reproduces L330): at lambda = 1 a moving phantom without momentum drops out of the leaf curvature
     psi and is pushed into the lapse with a 1/alpha amplitude (at alpha = 0 there is no solution at all): the
     dynamics would see it x 1/alpha, lensing not at all -- L330's frozen-phantom pathology.
  C3 AT lambda = 1 + eps THE SYSTEM IS SOLVABLE for any velocity: the shift sigma carries a 1/eps-enhanced piece,
     sigma_enh = -(8 pi G/eps) rho_ph_dot / k^4 (the foliation expansion K = 2 w.g_ph/(eps c^2), sec. C6), and the
     lapse phi carries an equal and opposite enhanced piece.
  C4 THE ENHANCED PIECES ARE PURE GAUGE.  The gauge-invariant potentials (Phi_B = phi + sigma_dot, Psi_B = psi; the
     invariance is checked symbolically) contain NO 1/eps term: matter feels -grad Phi_B and light Phi_B + Psi_B,
     and both equal the boosted static values up to O(w^2/c^2) (not enhanced).  Lensing = dynamics survives for
     moving sources.
  C5 WHAT THE CARRYING COSTS: a strongly deformed preferred foliation.  Numbers, both footings, both ends of the
     c14 window: the required expansion K ~ 2 w g_ph/(eps c^2) (6-60 H0 at r_M), the aether-flow perturbation ~ K r
     (0.5-80 km/s for galaxies), and the leading NONLINEAR residual -- the pointwise (not globally integrable)
     khronon energy (d_i d_j B)^2 - (lap B)^2 relative to the phantom, (w v_f/(eps c^2))^2: <= 3% for galaxies, but
     8-55% for clusters, whose aether flow is comparable to w: every massive cluster sits at or past the onset
     w v_f = eps c^2 = (0.95-1.5e3 km/s)^2, and the linear result does not cover them.
  C6 PPN: alpha_1 = -4 c14 and alpha_2 = 0 are properties of the same coefficients (L280) and are not changed by the
     channel; the MW's own carried-phantom aether flow at the Sun is a few km/s against w ~ 370-630 km/s.
  C7 CORRECTION (L333 R2, reproduced): the 1/eps lapse is the aether's own acceleration, the MOND sector's input,
     distorted by D cos^2(theta), D = 2 w^2/(eps c^2): D/3 = 0.11-0.28 at 620 km/s.  a0 would track CMB-frame speed.
  READING.  At linear order the L297 khronon DOES carry a moving galaxy's phantom, inside the preferred-frame bounds,
  and the metric potentials matter and light feel are velocity-independent -- but the aether acceleration the MOND
  sector reads is not (C7): the carrying costs an O(10-30%) CMB-velocity dependence of a0, or c2 >> 1e-4.  This is a necessary condition, not the theory:
  the MOND scalar's own equations in the moving frame, the leafwise Cassini filter, the absence of a wrong-sign
  auxiliary, and the nonlinear khronon regime (w v_f ~ eps c^2) are untouched here.
  MUTATE=1 sets eps = 0 (lambda = 1): the moving phantom no longer gravitates; C3 and C4 must FAIL and rc = 1.

Run from the repository root:  python3 real_research/khronon_momentum_2026/KM1_khronon_carries_phantom.py
"""
import os, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "KM1_khronon_carries_phantom"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "KM1", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
    P("\n" + "=" * 104); P(t); P("=" * 104)


t, x = sp.symbols("t x", real=True)
G, lam, alp, xi = sp.symbols("G lambda alpha xi", positive=True)
eps = sp.symbols("epsilon", positive=True)
phi, sig, psi = [sp.Function(n)(t, x) for n in ("phi", "sigma", "psi")]
rho_m, rho_ph, J = [sp.Function(n)(t, x) for n in ("rho_m", "rho_ph", "J")]

# ============================================================================================ C1
banner("C1  THE QUADRATIC ACTION IN UNITARY GAUGE (1D reduction along the wavevector) AND ITS EQUATIONS")
# R3 of gamma_ij = exp(2 zeta(x)) delta_ij in 3D, from the Christoffel symbols (no hand formula)
zeta = sp.Function("zeta")(x)
X = sp.symbols("X Y Z")
gmat = sp.diag(*([sp.exp(2 * zeta.subs(x, X[0]))] * 3))
ginv = gmat.inv()
Gam = [[[sum(ginv[a, d] * (sp.diff(gmat[d, b], X[c]) + sp.diff(gmat[d, c], X[b]) - sp.diff(gmat[b, c], X[d]))
             for d in range(3)) / 2 for c in range(3)] for b in range(3)] for a in range(3)]
Ric = sp.zeros(3)
for b in range(3):
    for c in range(3):
        Ric[b, c] = sum(sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
                        + sum(Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a] for d in range(3))
                        for a in range(3))
R3 = sp.simplify(sum(ginv[b, c] * Ric[b, c] for b in range(3) for c in range(3))).subs(X[0], x)
R3_expected = -sp.exp(-2 * zeta) * (4 * sp.diff(zeta, x, 2) + 2 * sp.diff(zeta, x) ** 2)
P(f"    R3[exp(2 zeta(x)) delta] = {sp.simplify(R3)};  matches -e^(-2 zeta)(4 zeta'' + 2 zeta'^2): "
  f"{sp.simplify(R3 - R3_expected) == 0}")
# second-order N sqrt(gamma) R3 with zeta = -psi, N = 1 + phi  (drop total derivatives by integrating by parts in L)
epsl = sp.symbols("e_l")
NRg = ((1 + epsl * phi) * sp.exp(3 * (-epsl * psi)) * R3.subs(zeta, -epsl * psi).doit())
NR2 = sp.expand(sp.series(NRg, epsl, 0, 3).removeO().coeff(epsl, 2))
# K_ij (linear): gamma_dot/2 = -psi_dot delta + d d E_dot ; minus d_(i N_j) = -d d B  ->  -psi_dot delta - d d sigma
Kxx = -sp.diff(psi, t) - sp.diff(sig, x, 2)
Kyy = -sp.diff(psi, t)
KK = Kxx ** 2 + 2 * Kyy ** 2
Ktr = Kxx + 2 * Kyy
L_grav = (KK - lam * Ktr ** 2 + xi * NR2 + alp * sp.diff(phi, x) ** 2) / (16 * sp.pi * G)
L_m = -rho_m * phi - rho_ph * phi + J * sp.diff(sig, x)            # J: matter momentum only (phantom: none)
L = L_grav + L_m
eqs = sp.euler_equations(L, [phi, sig, psi], [t, x])
E_phi, E_sig, E_psi = [sp.simplify(e.lhs) for e in eqs]
P(f"    d/d phi  : {sp.simplify(E_phi * 16 * sp.pi * G)} = 0")
P(f"    d/d sigma: {sp.simplify(E_sig * 16 * sp.pi * G)} = 0")
P(f"    d/d psi  : {sp.simplify(E_psi * 16 * sp.pi * G)} = 0")
# gauge check: t -> t + T(t,x): phi -> phi - T_t, sigma -> sigma + T, psi -> psi (flat background)
T = sp.Function("T")(t, x)
PhiB = phi + sp.diff(sig, t)
gauge_ok = sp.simplify((phi - sp.diff(T, t)) + sp.diff(sig + T, t) - PhiB) == 0
OUT["numbers"]["C1"] = {"R3_ok": str(sp.simplify(R3 - R3_expected) == 0), "PhiB": "phi + sigma_t",
                        "E_phi": str(sp.simplify(E_phi * 16 * sp.pi * G)), "E_sig": str(sp.simplify(E_sig * 16 * sp.pi * G)),
                        "E_psi": str(sp.simplify(E_psi * 16 * sp.pi * G))}
check("C1 the quadratic action's equations derived symbolically (R3 from Christoffels); Phi_B = phi + sigma_dot is "
      "invariant under the time reparametrisation", f"R3 ok {sp.simplify(R3 - R3_expected) == 0}; gauge ok {gauge_ok}",
      sp.simplify(R3 - R3_expected) == 0 and gauge_ok,
      "E enters only through sigma = B - E_dot, so the E-equation is the time derivative of the sigma-equation")

# ============================================================================================ C2-C4
banner("C2-C4  A GALAXY (MATTER + PHANTOM) MOVING AT w THROUGH THE PREFERRED FRAME: ONE FOURIER MODE")
k, om = sp.symbols("k omega", positive=True)          # plane wave e^{i(k x - omega t)}, omega = k w_parallel (c = 1)
rm, rp = sp.symbols("rho_m_hat rho_ph_hat")
fh, sh, ph_ = sp.symbols("phi_hat sigma_hat psi_hat")
w = om / k
subsF = {}


def fourier(expr):
    """Replace every field and derivative by (i k)^n (-i omega)^m times its amplitude."""
    rep = {}
    for F, A in ((phi, fh), (sig, sh), (psi, ph_), (rho_m, rm), (rho_ph, rp), (J, rm * w)):
        for nt in range(0, 3):
            for nx in range(0, 5):
                d = F
                if nt:
                    d = sp.diff(d, t, nt)
                if nx:
                    d = sp.diff(d, x, nx)
                rep[d] = A * (-sp.I * om) ** nt * (sp.I * k) ** nx
    return sp.simplify(sp.expand(expr).xreplace(rep))     # top-down: derivative nodes replaced whole


Ef = [fourier(sp.expand(e * 16 * sp.pi * G)) for e in (E_phi, E_sig, E_psi)]
lam_val = 1 if MUTATE else 1 + eps
sub = {xi: 1, lam: lam_val}
Ef = [sp.simplify(e.subs(sub)) for e in Ef]
# C2 control: lambda = 1 (alpha = c14 kept independent): L330's dichotomy
Ef1 = [sp.simplify(fourier(sp.expand(q * 16 * sp.pi * G)).subs({xi: 1, lam: 1})) for q in (E_phi, E_sig, E_psi)]
sol1 = sp.solve(Ef1, [fh, sh, ph_], dict=True)
sol1a = sol1[0] if sol1 else {}
psi1 = sp.simplify(sol1a.get(ph_, sp.nan)); phi1 = sp.simplify(sol1a.get(fh, sp.nan))
psi_has_ph = sp.simplify(sp.diff(psi1, rp)) if sol1 else sp.nan
phi_ph_coef = sp.simplify(sp.diff(phi1, rp) * alp * k ** 2) if sol1 else sp.nan
PhiB1 = sp.simplify(phi1 + (-sp.I * om) * sp.simplify(sol1a.get(sh, sp.nan))) if sol1 else sp.nan
PhiB1_ph = sp.simplify(sp.diff(PhiB1, rp)) if sol1 else sp.nan
sol1_a0 = sp.solve([e.subs(alp, 0) for e in Ef1], [fh, sh, ph_], dict=True)
P(f"    lambda = 1: psi_hat = {psi1}  (d psi/d rho_ph = {psi_has_ph}: the leaf curvature does not see the moving phantom)")
P(f"    lambda = 1: phi_hat = {phi1}  (rho_ph coefficient x alpha k^2 = {phi_ph_coef}: the lapse carries it, x 1/alpha)")
P(f"    lambda = 1: gauge-invariant Phi_B = phi + sigma_dot = {PhiB1}  (d Phi_B/d rho_ph = {PhiB1_ph})")
P(f"    lambda = 1 and alpha = 0: solutions {sol1_a0}")
OUT["numbers"]["C2"] = {"psi_hat": str(psi1), "phi_hat": str(phi1), "alpha0_solutions": str(sol1_a0)}
check("C2 CONTROL (L330): at lambda = 1 a moving phantom with no momentum does not gravitate at all -- it is absent "
      "from both gauge-invariant potentials (the 1/alpha lapse is cancelled by the shift); at alpha = 0 there is no "
      "solution", f"d Psi_B/d rho_ph = {psi_has_ph}; d Phi_B/d rho_ph = {PhiB1_ph}; lapse coefficient "
      f"{phi_ph_coef}/(alpha k^2) (gauge); alpha = 0: {sol1_a0}",
      sol1 != [] and psi_has_ph == 0 and PhiB1_ph == 0 and sol1_a0 == [],
      "L330's frozen phantom, reproduced exactly: a phantom that moves without momentum is left out of gravity")
# C3: lambda = 1 + eps
rr = sp.symbols("r", positive=True)                     # alpha = r eps  (equal-speed locus: r = 1 - 2 c14 ~ 1)
Ef = [sp.simplify(e.subs(alp, rr * eps)) for e in Ef]
sol = sp.solve(Ef, [fh, sh, ph_], dict=True)
if not sol:
    check("C3 at lambda = 1 + eps the moving galaxy has a solution", "no solution", False)
else:
    s0 = sol[0]
    sig_hat = sp.simplify(s0[sh]); phi_hat = sp.simplify(s0[fh]); psi_hat = sp.simplify(s0[ph_])
    sig_lead = sp.simplify(sp.limit(sig_hat * eps, eps, 0))
    phi_lead = sp.simplify(sp.limit(phi_hat * eps, eps, 0))
    sig_pred = sp.simplify(-(8 * sp.pi * G) * (-sp.I * om) * rp / k ** 4)   # -(8 pi G) rho_ph_dot / k^4 (lap^2 -> k^4)
    P(f"    sigma_hat x eps -> {sig_lead}   (prediction -(8 pi G) rho_ph_dot/k^4 = {sig_pred})")
    P(f"    phi_hat   x eps -> {phi_lead}")
    ratio_w0 = sp.simplify(sp.limit(sig_lead / sig_pred, om, 0)) if sig_lead != 0 else 0
    exact_fac = sp.simplify(sig_lead / sig_pred) if sig_lead != 0 else 0
    check("C3 at lambda = 1 + eps the moving galaxy is solvable; the shift carries a 1/eps piece equal to "
          "-(8 pi G/eps) rho_ph_dot/k^4 x 1/(1 - r w^2/c^2), and the lapse an exactly equal and opposite one",
          f"eps*sigma / prediction = {exact_fac} (-> {ratio_w0} as w -> 0); eps*(phi + sigma_dot) = "
          f"{sp.simplify(phi_lead + (-sp.I * om) * sig_lead)}",
          sig_lead != 0 and ratio_w0 == 1 and sp.simplify(phi_lead + (-sp.I * om) * sig_lead) == 0,
          "the constraint mismatch that froze the phantom at lambda = 1 is absorbed by the shift; the factor "
          "1/(1 - r w^2/c^2) is the khronon's own propagation speed (c on the equal-speed locus)")
    PhiB_hat = sp.simplify(phi_hat + (-sp.I * om) * sig_hat)
    PsiB_hat = psi_hat
    target = sp.simplify(-4 * sp.pi * G * (rm + rp) / k ** 2)        # static Newtonian potential of the total, boosted
    dPhi = sp.simplify((PhiB_hat - target) / target)
    dPsi = sp.simplify((PsiB_hat - target) / target)
    enhPhi = sp.simplify(sp.limit(dPhi * eps, eps, 0))
    enhPsi = sp.simplify(sp.limit(dPsi * eps, eps, 0))
    dPhi_ser = sp.simplify(sp.series(sp.limit(dPhi, eps, 0), om, 0, 3).removeO())
    dPsi_ser = sp.simplify(sp.series(sp.limit(dPsi, eps, 0), om, 0, 3).removeO())
    P(f"    (Phi_B - target)/target: 1/eps coefficient = {enhPhi};  eps -> 0 limit, to O(w^2): {dPhi_ser}")
    P(f"    (Psi_B - target)/target: 1/eps coefficient = {enhPsi};  eps -> 0 limit, to O(w^2): {dPsi_ser}")
    OUT["numbers"]["C3"] = {"sigma_hat": str(sig_hat), "phi_hat": str(phi_hat), "psi_hat": str(psi_hat)}
    OUT["numbers"]["C4"] = {"dPhi_over_target": str(dPhi), "dPsi_over_target": str(dPsi), "enh_Phi": str(enhPhi),
                            "enh_Psi": str(enhPsi), "dPhi_series": str(dPhi_ser), "dPsi_series": str(dPsi_ser)}
    lensdyn = sp.simplify(sp.limit(sp.limit((PhiB_hat - PsiB_hat) / target, eps, 0), om, 0))
    full_Phi = sp.simplify(sp.limit(sp.limit(dPhi, eps, 0), om, 0))     # 0 <=> the phantom is fully in Phi_B
    full_Psi = sp.simplify(sp.limit(sp.limit(dPsi, eps, 0), om, 0))
    check("C4 the gauge-invariant potentials carry NO 1/eps term: the enhanced shift and lapse cancel in Phi_B, and "
          "Psi_B is untouched; both equal the boosted static potential up to O(w^2/c^2)",
          f"1/eps coefficients: Phi_B {enhPhi}, Psi_B {enhPsi}; (Phi_B - target)/target, (Psi_B - target)/target at "
          f"w -> 0: {full_Phi}, {full_Psi}; (Phi_B - Psi_B)/target: {lensdyn}",
          enhPhi == 0 and enhPsi == 0 and full_Phi == 0 and full_Psi == 0 and lensdyn == 0,
          "matter feels -grad Phi_B, light Phi_B + Psi_B: no velocity-dependent effect of order w^2/(eps c^2)")

# ============================================================================================ C5
banner("C5  WHAT THE CARRYING COSTS: THE DEFORMED FOLIATION, IN NUMBERS")
c, Gn, MSUN, KPC = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 67.4e3 / 3.0857e22
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
systems = [("dwarf", 1e9, 150e3), ("Milky Way", 6e10, 370e3), ("massive spiral", 3e11, 600e3), ("cluster", 1e14, 600e3)]
rows5 = {}
for foot, a0 in A0.items():
    for c14 in (1.0e-5, 2.5e-5):
        e = c14 / (1 - 2 * c14)
        for name, Mb, wv in systems:
            vf = (Gn * Mb * MSUN * a0) ** 0.25
            rM = math.sqrt(Gn * Mb * MSUN / a0)
            gph = vf ** 2 / rM                                   # phantom field at r_M (isothermal: v_f^2/r)
            K = 2 * wv * gph / (e * c ** 2)
            du = K * rM                                          # aether-flow perturbation across r_M
            nl = (wv * vf / (e * c ** 2)) ** 2                   # pointwise khronon energy / phantom density
            rows5[f"{foot}/c14={c14:g}/{name}"] = {"v_f_kms": vf / 1e3, "w_kms": wv / 1e3, "K_over_H0": K / H0,
                                                   "aether_flow_kms": du / 1e3, "nonlinear_ratio": nl}
            if foot == "canonical" or name == "cluster":
                P(f"    {foot:9s} c14 = {c14:.1e} {name:15s} v_f = {vf / 1e3:6.1f} km/s, w = {wv / 1e3:5.0f} km/s: "
                  f"K = {K / H0:7.2f} H0, aether flow {du / 1e3:8.2f} km/s, nonlinear ratio {nl:.2e}")
onset = {f"c14={c14:g}": math.sqrt(c14 / (1 - 2 * c14) * c ** 2) / 1e3 for c14 in (1e-5, 2.5e-5)}
P(f"    nonlinear onset w v_f = eps c^2  ->  sqrt(eps) c = {onset} km/s")
OUT["numbers"]["C5"] = {"rows": rows5, "onset_sqrt_w_vf_kms": onset}
gal_max = max(v["nonlinear_ratio"] for kk, v in rows5.items() if "cluster" not in kk)
cl = {kk: v["nonlinear_ratio"] for kk, v in rows5.items() if "cluster" in kk}
cl_flow = {kk: v["aether_flow_kms"] / v["w_kms"] for kk, v in rows5.items() if "cluster" in kk}
check("C5 galaxies stay linear (nonlinear khronon energy <= 3% of the phantom at both ends of the c14 window); "
      "CLUSTERS DO NOT: 8-55% of the phantom, with aether flows comparable to w -- the linear result does not "
      "cover clusters", f"galaxy max {gal_max:.1e}; clusters {({k_: f'{v:.2f}' for k_, v in cl.items()})}; "
      f"cluster aether flow / w {({k_: f'{v:.2f}' for k_, v in cl_flow.items()})}",
      gal_max < 0.05 and min(cl.values()) > 0.05,
      "the onset w v_f = eps c^2 = (0.95-1.5e3 km/s)^2: every massive cluster is at or past it; the khronon is "
      "dragged along with the cluster there, and this lane says nothing about it")

# ============================================================================================ C6
banner("C6  PPN: THE SAME COEFFICIENTS, UNCHANGED BOUNDS")
rows6 = {}
for c14 in (1.0e-5, 2.5e-5):
    c2 = c14 / (1 - 2 * c14)
    a1 = -4 * c14
    a2 = c14 * (c14 * (1 + 2 * c2) - c2) / (c2 * (2 - c14))          # L280 closed form
    rows6[f"c14={c14:g}"] = {"c2": c2, "alpha1": a1, "alpha2": a2}
    P(f"    c14 = {c14:.1e}, c2 = {c2:.6e}: alpha_1 = {a1:.1e} (LLR |alpha_1| < 1e-4), alpha_2 = {a2:.1e} (bound 4e-7)")
mw = rows5["canonical/c14=2.5e-05/Milky Way"]
P(f"    the MW's own carried-phantom aether flow ~ {mw['aether_flow_kms']:.1f} km/s against w ~ 370-630 km/s: "
  f"alpha-type effects shift by ~{2 * mw['aether_flow_kms'] / 370 * 100:.1f}% of already-bounded values")
OUT["numbers"]["C6"] = rows6
check("C6 alpha_1 = -4 c14 inside the LLR bound and alpha_2 = 0 on the equal-speed locus (L280): the momentum "
      "channel is the same coefficient set, so the bounds are unchanged", rows6,
      all(abs(v["alpha1"]) <= 1e-4 and abs(v["alpha2"]) < 1e-12 for v in rows6.values()),
      "the channel needs no Solar-System screening: its large part is gauge")

# ============================================================================================ C7
banner("C7  CORRECTION (L333 R2): THE ENHANCED LAPSE IS THE AETHER'S OWN ACCELERATION -- THE MOND SECTOR'S INPUT")
# The 1/eps lapse of C3 cancels from Phi_B (what matter and light feel), but a_i = d_i phi is the covariant acceleration
# of the aether congruence, and in the L297/clock construction the MOND sector reads it.  From C3:
#   phi_enh / Phi_ph = [-(8 pi G/eps) omega^2 rho_ph/(k^2 (k^2 - r omega^2))] / [-4 pi G rho_ph/k^2]
#                    = 2 (omega/k)^2 / (eps (1 - r w^2)) -> D cos^2(theta),   D = 2 w^2/(eps c^2)
if sol:
    Phi_ph = -4 * sp.pi * G * rp / k ** 2
    ratio_lapse = sp.simplify(sp.limit(phi_hat * eps, eps, 0) / eps / Phi_ph)
    ratio_w0 = sp.simplify(sp.series(ratio_lapse * eps, om, 0, 3).removeO())
    P(f"    phi_enh / Phi_ph = {ratio_lapse}  ->  eps x ratio to O(w^2): {ratio_w0}  (= 2 w_par^2 / c^2)")
    rows7 = {}
    for c14 in (1.0e-5, 2.5e-5):
        e = c14 / (1 - 2 * c14)
        for wv in (300e3, 620e3):
            Dv = 2 * wv ** 2 / (e * c ** 2)
            rows7[f"c14={c14:g}/w={wv / 1e3:.0f}"] = {"D": Dv, "D_over_3": Dv / 3}
            P(f"    c14 = {c14:.1e} (eps = {e:.3e}), w = {wv / 1e3:.0f} km/s: D = {Dv:.3f}, sphere-averaged D/3 = {Dv / 3:.3f}")
    OUT["numbers"]["C7"] = {"lapse_ratio": str(ratio_lapse), "rows": rows7,
                            "L333": "D/3 = 0.29 at c14 = 1e-5, 620 km/s; 0.11 at eps = 2.5e-5"}
    d3_lg = rows7["c14=1e-05/w=620"]["D_over_3"]; d3_hi = rows7["c14=2.5e-05/w=620"]["D_over_3"]
    check("C7 the enhanced lapse, invisible to matter and light, distorts the aether acceleration the MOND sector reads "
          "by D cos^2(theta), D = 2 w^2/(eps c^2): at the Local Group's 620 km/s through the CMB frame, D/3 = 0.28-0.11 "
          "across the c14 window -- independently reproducing L333's 0.29 / 0.11", f"{ratio_w0}; D/3(620 km/s) = "
          f"{d3_lg:.3f} (c14 = 1e-5), {d3_hi:.3f} (c14 = 2.5e-5)",
          sp.simplify(ratio_w0 - 2 * om ** 2 / k ** 2) == 0 and abs(d3_lg - 0.29) < 0.02 and abs(d3_hi - 0.11) < 0.01,
          "KM1's C4 'no velocity-dependent effect' holds for Phi_B and Psi_B only: a0 would track each galaxy's speed "
          "through the CMB frame at 10-30%, unless c2 >> 1e-4 (then alpha_2 forces c14 <~ 8e-7, L280/L333)")

# ============================================================================================ verdict
banner("VERDICT")
P("""  The first computation on the breakthrough list, at linear order: the L297 khronon DOES carry a moving galaxy's
  phantom (C3-C4: matter and light see the boosted static field, lensing = dynamics, alpha_1/alpha_2 unchanged; at
  lambda = 1 the moving phantom does not gravitate at all, C2).  The price is NOT invisible (C7, the parallel lane
  L333's R2, reproduced here): the 1/eps lapse that cancels from the metric potentials is the aether's own
  acceleration, which is what the MOND sector reads, and it is distorted by D cos^2(theta), D = 2 w^2/(eps c^2) --
  10-30% at the Local Group's 620 km/s.  Either a0 tracks each galaxy's speed through the CMB frame (a falsifiable
  prediction, likely under strain from the RAR's tightness) or c2 >> 1e-4 with c14 <~ 8e-7.  Clusters are nonlinear
  (C5) and outside this lane.  This lane independently reproduces L333 (R1, R2); L333 is the fuller record.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
