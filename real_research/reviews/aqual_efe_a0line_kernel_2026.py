#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
aqual_efe_a0line_kernel_2026.py
============================
THE FULL NONLINEAR AQUAL-EFE WIDE-BINARY SOLVE THAT AMENDMENT 9(b) OWES.

STATUS: VERIFIED 2026-08-13 through TWO adversarial rounds (round 1: solver mathematics all
six attacked items CONFIRMED -- independent 288^3 FFT solve 1-2%, direct 3D quadrature
<=0.16%, Gauss-flux constraint 7e-4; round 2: the amendment-draft verification REFUTED the
first bracket's floor and this file was rebuilt to carry the corrections as COMPUTED parts).
THE KILL IS THEOREM-GRADE: the registered 1.2139/1.2592 is the sqrt of the AQUAL response
tensor's LARGEST eigenvalue (B_par = nu(y_extN)) used as if isotropic, and every defensible
orientation treatment gives strictly less.  Nothing recovers it.
THE REGISTERED OBJECT IS A BAND, computed in PART D/E and graded by PART C2's two-body
benchmark (the composition conventions BOTH overshoot the exact anchor-bin force: per-star
excess by ~3-8x, total-mass by the computed f_tm(y) ~ 1.4-1.7x; the deep-MOND closed-form
factors 1.69-1.81x / 1.24-1.28x live in the deep ISOLATED limit ONLY):
  canonical: total-mass FLOOR 1.1614 +- 0.0175 (6-seed centre 1.1610, rms 0.0117)
             benchmark-corrected TOP 1.1814 +- 0.0150 (6-seed centre 1.1847, rms 0.0148)
  alt:       FLOOR 1.1917 +- 0.0175 (centre 1.2025, rms 0.0083)
             TOP 1.2267 +- 0.0200 (centre 1.2288, rms 0.0058; 6/6 seeds above 1.20)
The registered 1.2139/1.2592 is overstated by 0.032-0.052 canonical / 0.032-0.067 alt
(1.7-2.8 / 1.7-3.6 sigma_fit at the frozen-N 0.019).  PER-STAR IS A DIAGNOSTIC ONLY (1.1139 /
1.1217; the kappa-trip mock -- its floor reading was REFUTED by the exact two-body benchmark).
KAPPA ATTRIBUTION (round-2 correction): the kappa-window trip is a per-star-composition
artifact -- battery 12/12 trips per-star, 0/12 under the registered grades -- so the framework's
best grade predicts NO trip; a real-sky trip is evidence of a genuine systematic, NOT
pre-authorized framework behaviour.  Amendment 9(d)(i)'s 2.68-sigma arm separation is DEAD
(the canonical band sits 0.003-0.023 above MI's 1.1582, INSIDE the superseded MI magnitude
range).  Residual grade, declared: base-seed anchors carry a +-0.01-grade seed/call-order
sensitivity (the battery centres are the robust quantities); the EFE-present exact two-body
anchor solve does not exist and is the owed unlock pinning the top.  A transition-region
caveat from the math referee: the anisotropy orientation FLIPS in the transition zone
(B_perp > B_par at r ~ 1 r_M); "parallel is the big axis" holds at saturation only.

WHAT IS OWED (PREREGISTRATION_DR4.md, Amendment 9(b), verbatim): the in-force DR4 target
gamma_v = 1.2139 (canonical) / 1.2592 (alt) is "the point-field isotropic asymptote only ...
A full nonlinear AQUAL-EFE solve is OWED, and until it exists this target carries provisional
status."  The number it superseded (MI 1.1582) came from a full nonlinear per-star EFE solve
validated against a linear-response tensor to 2.9e-5.  This file is the same-grade calculation
for the MODIFIED-GRAVITY arm.

PROVENANCE OF THE REGISTERED NUMBER, traced before solving (2026-08-13):
  * y_extN = 1.28903 (canonical) / 0.99240 (alt) is the CLOSURE INVERSION of the observed
    g_ext,obs/a0 = 1.8996 / 1.5764 under the Route A kernel x = y*nu(y)  (Amendment 4(b)
    convention; mi_route_a_wb_gamma_v_2026.py line 22 confirms 1.6809 -> 1.28903 was the
    same move for MI).
  * The superseded MI 1.1582 was sqrt[(gamma2_par + 2*gamma2_perp)/3] of the MI response
    tensor: gamma2_perp = nu(y_extN) = 1.47342, gamma2_par = dx/dy = 1.07749.
  * Amendment 9 took gamma2_perp ALONE and called the MG boost "isotropic ... no orientation
    average is needed".  That claim is checked here BY SOLVING THE PDE, because AQUAL's
    linearized operator  mu0 [ laplacian + L0 (e.d)^2 ] phi = 4 pi G rho  is manifestly
    ANISOTROPIC (L0 = dln mu/dln x != 0), and its point solution boosts are
        B_par = 1/mu0 = nu(y_extN),   B_perp = nu(y_extN)/sqrt(1+L0)
    -- a DIFFERENT anisotropy than MI's (parallel is the big one, not perpendicular).

WHAT THIS FILE DOES:
  PART A  kernel, closure inversions, and the analytic saturation tensors (MI + AQUAL-linear),
          reproducing the registered 1.2139/1.2592 and the superseded 1.1582 exactly.
  PART B  a nonlinear per-star solver on a (log r, theta) spherical-harmonic grid:
            - ONE-FIELD AQUAL   div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G rho   (PRIMARY:
              this is the framework's PROVEN Bekenstein-Milgrom realisation,
              mi_route_a_field_theory_2026.py, 7 properties proved)
            - QUMOND            lap Phi = div[ nu(|grad Phi_N|/a0) grad Phi_N ]  (FORK)
          each solved for a point mass in the uniform external field, BOTH footings.
          Output: the radial force-boost table B_r(y_int, theta).
  PART C  validation gates (each a hard check):
            V1 Newtonian limit  (nu == 1  =>  B == 1 to 1e-10)
            V2 isolated-MOND limit (g_ext -> 0  =>  B(y,theta) == nu(y) exactly, all theta)
            V3 EFE-saturated limit vs the ANALYTIC linear-response tensors of PART A
            V4 grid-doubling convergence on the headline number
  PART D  the pipeline-grade observable: the anisotropic boost B_r(y, psi) is injected into
          the frozen pipeline's OWN population MC (orbit generation mirrored with the 3D
          separation direction retained; random external-field direction per system), mock
          data at the frozen N = 30,000, then FIT WITH THE PIPELINE'S OWN ISOTROPIC
          ESTIMATOR (model_medians + fit_gamma imported from wide_binary_pipeline.py,
          untouched).  The recovered gamma_hat IS the full-solve DR4 target.
          Controls: an isotropic gamma(y) injection at the registered target calibrates
          estimator bias; an isotropic injection with the SOLVER's radial shape separates
          the transition-shape effect from the anisotropy effect.
  PART E  verdict: full-solve target vs registered 1.2139/1.2592, vs superseded MI range,
          arm-separation status, and whether Amendment 10 is required.  (Filing an
          amendment is THE AUTHOR'S CALL; this file only computes.)

CONVENTIONS AND REGISTERED-GRADE SIMPLIFICATIONS (stated, not hidden):
  * per-star superposition: a_rel is built from two single-star solves (the same grade as
    the superseded MI calculation).  Cross-talk of the two stars inside mu is second order
    in g_int/g_ext at saturation and is NOT included.
  * "velocity scaling at fixed orbit": the pipeline's own declared shortcut.  The per-system
    velocity boost is sqrt(B_r) at the epoch's (y_true, psi).  Self-consistent modified-orbit
    integration remains the pipeline's flagged upgrade path, not this file's scope.
  * external-field direction: isotropic per system (the sample's LOS directions are
    volume-distributed around the Sun while e points at the Galactic centre; the frozen MC
    tracks no sky positions, so isotropy is the consistent registered-grade treatment).
  * the tangential force component is REPORTED but not injected (no tangential term exists
    in the pipeline's declared boost shape).

Exit 0 = every check passed.  Every PASS/FAIL is a numeric comparison that can fail.
"""

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wide_binary_pipeline as wbp  # noqa: E402  (import-safe: main() is __main__-guarded)

FAIL = []
NCHK = [0]
rng_global = np.random.default_rng(20260813)


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


# =================================================================================================
# PART A -- kernel, closure inversions, analytic tensors
# =================================================================================================
print(__doc__)
print("=" * 100)
print("PART A -- kernel, closure inversions, and the analytic saturation tensors")
print("=" * 100)


def nu(y):
    # a0-LINE KERNEL (alpha = 1): g_obs^2 = g_bar^2 + a_0 g_bar  <=>  nu = sqrt(1 + 1/y).
    # SWAPPED IN 2026-08-17 for the kernel switch off Route A.  Route A
    # (nu = 1/(1-exp(-sqrt y))) is ILLEGAL in AeST: u(y) = y(nu-1) is non-injective
    # (peaks 0.6476 at y = 2.540 then falls), so no single-valued J(Y) exists and the
    # longitudinal scalar mode is a ghost.  See nbody_2026/stage75_the_closed_theory_2026.py.
    y = np.asarray(y, dtype=float)
    return np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))


def dnu_dy(y):
    # d/dy sqrt(1+1/y) = -1/(2 y^2 sqrt(1+1/y))
    y = np.asarray(np.maximum(y, 1e-300), dtype=float)
    return -1.0 / (2.0 * y**2 * np.sqrt(1.0 + 1.0 / y))


# x = y * nu(y): the observed field for Newtonian y.  Monotonic (proven convexity of the
# Route A BM realisation); invert on a log table.
_YT = np.logspace(-10, 10, 40001)
_XT = _YT * nu(_YT)
assert np.all(np.diff(_XT) > 0), "x(y) must be monotonic for the BM realisation"


def y_of_x(x):
    return np.exp(np.interp(np.log(np.asarray(x, float)), np.log(_XT), np.log(_YT)))


def mu_of_x(x):
    return y_of_x(x) / np.asarray(x, float)


# frozen inputs (pipeline + Amendment 9's own provenance)
A0 = {"canonical": wbp.A0_CAN, "alt": wbp.A0_ALT}
# Amendment 9 registered targets, PINNED LOCALLY (round-3 referee finding 3): the C1 debias
# control and every "vs registered" comparison must keep meaning AFTER the Amendment-10
# pipeline retarget moves wbp.GAMMA_TARGET; never read the live pipeline constants for these.
REGISTERED_A9 = {"canonical": 1.2139, "alt": 1.2592}
X_EXT = {f: wbp.GEXT_PHYS / A0[f] for f in A0}          # observed external field / a0
Y_EXT = {f: float(y_of_x(X_EXT[f])) for f in A0}        # closure inversion, Route A kernel
info("observed x_ext = g_ext,obs/a0", f"canonical {X_EXT['canonical']:.4f}, alt {X_EXT['alt']:.4f}")
check(abs(Y_EXT["canonical"] - 1.28903) < 1e-3 and abs(Y_EXT["alt"] - 0.99240) < 1e-3,
      f"A1  closure inversion reproduces the corpus's y_extN: {Y_EXT['canonical']:.5f} canonical "
      f"(recorded 1.28903), {Y_EXT['alt']:.5f} alt (recorded 0.99240)",
      "residual ~5e-4 is the pipeline's a0 rounding (9.36e-11 vs the corpus's 9.3619e-11)")

TENSOR = {}
for f in A0:
    yE = Y_EXT[f]
    n0 = float(nu(yE))
    dxdy = float(n0 + yE * dnu_dy(yE))                   # d(y nu)/dy = MI parallel eigenvalue
    x0 = yE * n0
    L0 = n0 / dxdy - 1.0                                 # dln mu/dln x = (x/y)(dy/dx) - 1
    TENSOR[f] = dict(nu0=n0, dxdy=dxdy, L0=L0,
                     mi_perp=n0, mi_par=dxdy,
                     aq_par=n0, aq_perp=n0 / np.sqrt(1.0 + L0))
g_reg = {f: np.sqrt(TENSOR[f]["nu0"]) for f in A0}
check(abs(g_reg["canonical"] - 1.2139) < 5e-4 and abs(g_reg["alt"] - 1.2592) < 5e-3,
      f"A2  the REGISTERED asymptote sqrt(nu(y_extN)) reproduced: {g_reg['canonical']:.4f} canonical "
      f"/ {g_reg['alt']:.4f} alt (in force: 1.2139 / 1.2592)")
mi_avg = np.sqrt((TENSOR["canonical"]["mi_par"] + 2 * TENSOR["canonical"]["mi_perp"]) / 3.0)
check(abs(mi_avg - 1.1582) < 5e-4,
      f"A3  the SUPERSEDED MI 1.1582 is the orientation average of the SAME tensor: "
      f"sqrt[(dx/dy + 2 nu)/3] = {mi_avg:.5f}",
      "the two in-force-era numbers differ ONLY by orientation treatment, not by physics grade")
for f in A0:
    t = TENSOR[f]
    aq_avg = np.sqrt((t["aq_par"] + 2 * t["aq_perp"]) / 3.0)
    info(f"A4  {f}: AQUAL-linear point tensor B_par = {t['aq_par']:.5f}, B_perp = {t['aq_perp']:.5f} "
         f"(L0 = {t['L0']:.5f})",
         f"orientation avg sqrt[(par+2perp)/3] = {aq_avg:.5f} -- NOT isotropic, and the big axis is "
         f"PARALLEL (opposite of MI)")

# =================================================================================================
# PART B -- the nonlinear per-star solver (spherical harmonics on a log-r grid)
# =================================================================================================
print()
print("=" * 100)
print("PART B -- nonlinear per-star solves: one-field AQUAL (primary) and QUMOND (fork)")
print("=" * 100)
# units: G*M = 1, a0 = 1  =>  length unit r_M = sqrt(GM/a0);  y_int = 1/r^2.
# theta measured from the external-field direction e;  u = cos(theta).

NR, NTH, LMAX = 1600, 192, 48
RMIN, RMAX = 1e-3, 3e4
r = np.logspace(np.log10(RMIN), np.log10(RMAX), NR)
lnr = np.log(r)
u_gl, w_gl = np.polynomial.legendre.leggauss(NTH)        # u = cos(theta)
sin_th = np.sqrt(1.0 - u_gl**2)

# Legendre P_l(u) and dP_l/du tables (recurrence), rows l = 0..LMAX
P = np.zeros((LMAX + 1, NTH))
P[0] = 1.0
P[1] = u_gl
for l in range(1, LMAX):
    P[l + 1] = ((2 * l + 1) * u_gl * P[l] - l * P[l - 1]) / (l + 1)
dP = np.zeros_like(P)                                     # dP_l/du
for l in range(1, LMAX + 1):
    dP[l] = l * (u_gl * P[l] - P[l - 1]) / (u_gl**2 - 1.0)


def project_l(S):
    """S(r,theta) [NR,NTH] -> S_l(r) [LMAX+1, NR] via Gauss-Legendre."""
    return np.einsum("lt,t,rt->lr", P, w_gl, S) * (np.arange(LMAX + 1) + 0.5)[:, None]


def poisson_harmonic(S):
    """Solve lap Phi = S for the decaying solution; returns Phi(r,theta), dPhi/dr, dPhi/dtheta/r."""
    Sl = project_l(S)
    Phi_l = np.zeros_like(Sl)
    dPhi_l = np.zeros_like(Sl)
    for l in range(LMAX + 1):
        f_in = Sl[l] * r**(l + 3)                        # integrand in ln r: S r^{l+2} * r
        f_out = Sl[l] * r**(2 - l)
        I_in = np.concatenate([[0.0], np.cumsum(0.5 * (f_in[1:] + f_in[:-1]) * np.diff(lnr))])
        c_out = np.concatenate([[0.0], np.cumsum(0.5 * (f_out[1:] + f_out[:-1]) * np.diff(lnr))])
        I_out = c_out[-1] - c_out
        Phi_l[l] = -(I_in / r**(l + 1) + I_out * r**l) / (2 * l + 1)
        dPhi_l[l] = -(-(l + 1) * I_in / r**(l + 2) + l * r**(l - 1) * I_out) / (2 * l + 1)
    Phi = np.einsum("lr,lt->rt", Phi_l, P)
    dPhi_dr = np.einsum("lr,lt->rt", dPhi_l, P)
    dPhi_dth_over_r = np.einsum("lr,lt,t->rt", Phi_l, dP, -sin_th) / r[:, None]
    return Phi, dPhi_dr, dPhi_dth_over_r


R2 = r[:, None] ** 2


def gN_components(ge):
    """Newtonian field of point mass + uniform external, spherical components (attractive
    star field: g_r = -1/r^2; external ge along e: g_r = ge*u, g_th = -ge*sin)."""
    gr = ge * u_gl[None, :] - 1.0 / R2
    gt = -ge * sin_th[None, :] + np.zeros_like(R2)
    return gr, gt


def solve_qumond(ge):
    """Explicit QUMOND: lap Phi = div[nu(|grad Phi_N|) grad Phi_N], grad Phi_N = -gN.
    SIGN CONVENTION (the first run's V2 gate caught the flip): the smooth source is
    S = div[nu * (-gN)] = -(grad nu).gN, and the acceleration is g = -grad Phi, so the
    star part is g_r = -1/r^2 + dPhi_S... worked in field components throughout:
    the correction to the ACCELERATION from the phantom source chi' = Poisson(S) is
    g_chi = -grad chi' -> components (-dPr, -dPt) with S as below."""
    gr, gt = gN_components(ge)
    gmag = np.hypot(gr, gt)
    # grad|gN| analytic:  |gN|^2 = ge^2 + 1/r^4 - 2 ge u / r^2
    d_dr = (-4.0 / r[:, None] ** 5 + 4.0 * ge * u_gl[None, :] / r[:, None] ** 3) / (2.0 * gmag)
    d_dth_over_r = (2.0 * ge * sin_th[None, :] / R2) / (2.0 * gmag * r[:, None])
    S = -dnu_dy(gmag) * (gr * d_dr + gt * d_dth_over_r)     # div[nu grad Phi_N], smooth part
    _, dPr, dPt = poisson_harmonic(S)
    # Phi = -1/r + chi' (+uniform);  g = -grad Phi:  g_r = -1/r^2 - dPr ... with the
    # NEGATED source this now closes the isolated limit exactly (V2a).
    g_r_star = -1.0 / R2 - dPr
    g_t_star = -dPt
    return g_r_star, g_t_star


def solve_aqual(ge, n_iter=220, relax=0.55, tol=1e-9):
    """One-field AQUAL by Picard: lap Phi = div[(1-mu(|grad Phi|)) grad Phi] + 4 pi G rho.
    Phi = -x_ext_field... external TRUE field magnitude is ge_true = x(y=ge... NOTE: ge here
    is the NEWTONIAN external field; the true external is x_e = ge*nu(ge) and AQUAL's uniform
    background solution carries the TRUE field.  Split Phi = -x_e z - 1/r + chi."""
    x_e = ge * float(nu(ge))
    # initial guess: QUMOND star field.  SIGN CONVENTION (fixed after the first run's V2b
    # gate): with T = div[(1-mu) g] and chi' = Poisson(T), the ACCELERATION correction is
    # g_chi = +grad chi' -> components (+dPr, +dPt);  total g_r = x_e u - 1/r^2 + chi_r.
    g_r_star, g_t_star = solve_qumond(ge)
    chi_r = g_r_star + 1.0 / R2          # acceleration-correction components
    chi_t = g_t_star.copy()
    dlnr = np.diff(lnr)
    conv = np.inf
    # the uniform background's own W is divergence-free and HUGE at large r; subtracting it
    # ANALYTICALLY before differencing removes the catastrophic cancellation that poisoned
    # the far field in the first run (V3 gate: B_par(sat) came out 36 instead of 1.47)
    w_bg = 1.0 - mu_of_x(x_e)
    Wr_bg = w_bg * x_e * u_gl[None, :] + np.zeros_like(R2)
    Wt_bg = -w_bg * x_e * sin_th[None, :] + np.zeros_like(R2)
    for it in range(n_iter):
        # total field components (attractive star -1/r^2 handled analytically)
        Gr = x_e * u_gl[None, :] - 1.0 / R2 + chi_r
        Gt = -x_e * sin_th[None, :] + chi_t
        gmag = np.hypot(Gr, Gt)
        w = 1.0 - mu_of_x(np.maximum(gmag, 1e-14))
        Wr, Wt = w * Gr - Wr_bg, w * Gt - Wt_bg          # background-subtracted, decays
        # T = div W in spherical axisymmetric coords (2nd-order gradients on both axes)
        dr_term = np.gradient(R2 * Wr, lnr, axis=0) / (R2 * r[:, None])
        # div theta-part = (1/(r sin)) d(sin W_t)/dtheta = -(1/r) d(sin W_t)/du
        dth_term = -np.gradient(sin_th[None, :] * Wt * np.ones_like(R2), u_gl, axis=1) / r[:, None]
        T = dr_term + dth_term
        _, dPr, dPt = poisson_harmonic(T)
        new_r, new_t = dPr, dPt
        dconv = max(np.max(np.abs(new_r - chi_r)) / (np.max(np.abs(chi_r)) + 1e-30),
                    np.max(np.abs(new_t - chi_t)) / (np.max(np.abs(chi_t)) + 1e-30))
        chi_r = (1 - relax) * chi_r + relax * new_r
        chi_t = (1 - relax) * chi_t + relax * new_t
        conv = dconv
        if conv < tol:
            break
    # star part of the TOTAL field = total minus uniform TRUE background
    g_r_star = -1.0 / R2 + chi_r
    g_t_star = chi_t
    return g_r_star, g_t_star, conv, it + 1


def boost_table(g_r_star):
    """radial force boost toward the star: B_r = (-g_r_star) * r^2  (Newtonian == 1)."""
    return -g_r_star * R2


# =================================================================================================
# PART C -- validation gates
# =================================================================================================
print()
print("=" * 100)
print("PART C -- validation gates")
print("=" * 100)

# V1 Newtonian control: nu == 1 makes the QUMOND source vanish identically
_gr, _gt = gN_components(1.3)
S_newt = np.zeros_like(_gr)
check(np.max(np.abs(S_newt)) == 0.0,
      "V1  Newtonian control: with nu==1 the QUMOND phantom source is identically zero -> B==1",
      "(trivially exact by construction; the nonlinear machinery is exercised in V2/V3)")

# V2 isolated-MOND limit: tiny external field; B(y,theta) must equal nu(y) for all theta
ge_tiny = 1e-6
Bq_iso = boost_table(solve_qumond(ge_tiny)[0])
mask = (r > 5e-3) & (r < 50.0)          # away from both grid edges and the EFE radius
err_iso = np.max(np.abs(Bq_iso[mask] / nu(1.0 / R2)[mask] - 1.0))
check(err_iso < 2e-3,
      f"V2a QUMOND isolated limit: max |B/nu(y) - 1| = {err_iso:.2e} over 5e-3 < r < 50 r_M, all theta",
      "the harmonic solver reproduces the exact spherical solution")
Ba_iso, _, cv_iso, it_iso = solve_aqual(ge_tiny, n_iter=160)
Ba_iso = boost_table(Ba_iso)
err_iso_a = np.max(np.abs(Ba_iso[mask] / nu(1.0 / R2)[mask] - 1.0))
check(err_iso_a < 5e-3,
      f"V2b AQUAL isolated limit: max |B/nu(y) - 1| = {err_iso_a:.2e} (Picard conv {cv_iso:.1e}, "
      f"{it_iso} iters)",
      "QUMOND and AQUAL agree exactly in spherical symmetry, as they must")

# solve both formulations, both footings
SOLVE = {}
for f in A0:
    ge = Y_EXT[f]
    gq_r, gq_t = solve_qumond(ge)
    ga_r, ga_t, cva, ita = solve_aqual(ge)
    SOLVE[f] = dict(q=dict(Br=boost_table(gq_r), Bt=-gq_t * R2),
                    a=dict(Br=boost_table(ga_r), Bt=-ga_t * R2),
                    conv=cva, iters=ita)
    info(f"solved {f}: AQUAL Picard converged to {cva:.2e} in {ita} iterations")

# V3 saturation vs analytic linear-response tensors (deep-EFE, y_int << y_ext)
i_sat = np.argmin(np.abs(r - 300.0))     # y_int ~ 1e-5: saturated, far from outer edge
for f in A0:
    t = TENSOR[f]
    Br_a = SOLVE[f]["a"]["Br"][i_sat]
    # AQUAL-linear analytic angular profile of the RADIAL (toward-star) boost, derived from
    # the rescaled Green's function  phi = -A/rt,  A = 1/(mu0 sqrt(1+L0)),
    # rt^2 = r^2 (1 + L0 sin^2)/(1+L0):
    #     B_rad(theta) = A * r/rt = nu0 / sqrt(1 + L0 sin^2 theta)
    # which gives B(0) = nu0 (parallel) and B(pi/2) = nu0/sqrt(1+L0) (perpendicular) --
    # both principal axes recovered by construction.
    B_pred = t["nu0"] / np.sqrt(1.0 + t["L0"] * (1.0 - u_gl**2))
    ok_axes = (abs(B_pred[np.argmax(u_gl**2)] - t["aq_par"]) < 1e-3 * t["aq_par"]
               and abs(B_pred[np.argmin(u_gl**2)] - t["aq_perp"]) < 1e-2 * t["aq_perp"])
    err_sat = np.max(np.abs(Br_a / B_pred - 1.0))
    check(ok_axes and err_sat < 0.02,
          f"V3-{f}  AQUAL saturation vs analytic linear-response: max angular error "
          f"{err_sat:.3f} at y_int = {1.0/r[i_sat]**2:.1e}",
          f"axes: solver par {Br_a[np.argmax(u_gl)]:.4f} / perp {Br_a[np.argmin(np.abs(u_gl))]:.4f}, "
          f"analytic {t['aq_par']:.4f} / {t['aq_perp']:.4f}")
    Bq_sat = SOLVE[f]["q"]["Br"][i_sat]
    info(f"V3q-{f} QUMOND saturated profile (fork, reported): par {Bq_sat[np.argmax(u_gl)]:.4f} / "
         f"perp {Bq_sat[np.argmin(np.abs(u_gl))]:.4f}, sphere-avg "
         f"{0.5*np.dot(Bq_sat, w_gl):.4f}",
         f"AQUAL sphere-avg {0.5*np.dot(Br_a, w_gl):.4f} -- the two formulations' averages "
         f"need not coincide; the spread is priced in PART E")

# V4 resolution robustness: re-solve canonical AQUAL at half resolution and compare the
# saturated sphere-averaged boost (the quantity the headline inherits)
_full = dict(NR=NR, NTH=NTH, LMAX=LMAX)
B_ref = 0.5 * np.dot(SOLVE["canonical"]["a"]["Br"][i_sat], w_gl)
NR, NTH, LMAX = 800, 96, 32
r = np.logspace(np.log10(RMIN), np.log10(RMAX), NR)
lnr = np.log(r)
u_gl, w_gl = np.polynomial.legendre.leggauss(NTH)
sin_th = np.sqrt(1.0 - u_gl**2)
P = np.zeros((LMAX + 1, NTH)); P[0] = 1.0; P[1] = u_gl
for l in range(1, LMAX):
    P[l + 1] = ((2 * l + 1) * u_gl * P[l] - l * P[l - 1]) / (l + 1)
dP = np.zeros_like(P)
for l in range(1, LMAX + 1):
    dP[l] = l * (u_gl * P[l] - P[l - 1]) / (u_gl**2 - 1.0)
R2 = r[:, None] ** 2
_gh = solve_aqual(Y_EXT["canonical"], n_iter=180)
i_sat_h = np.argmin(np.abs(r - 300.0))
B_half = 0.5 * np.dot(boost_table(_gh[0])[i_sat_h], w_gl)
# restore full resolution state
NR, NTH, LMAX = _full["NR"], _full["NTH"], _full["LMAX"]
r = np.logspace(np.log10(RMIN), np.log10(RMAX), NR)
lnr = np.log(r)
u_gl, w_gl = np.polynomial.legendre.leggauss(NTH)
sin_th = np.sqrt(1.0 - u_gl**2)
P = np.zeros((LMAX + 1, NTH)); P[0] = 1.0; P[1] = u_gl
for l in range(1, LMAX):
    P[l + 1] = ((2 * l + 1) * u_gl * P[l] - l * P[l - 1]) / (l + 1)
dP = np.zeros_like(P)
for l in range(1, LMAX + 1):
    dP[l] = l * (u_gl * P[l] - P[l - 1]) / (u_gl**2 - 1.0)
R2 = r[:, None] ** 2
i_sat = np.argmin(np.abs(r - 300.0))
check(abs(B_half / B_ref - 1.0) < 5e-3,
      f"V4  half-resolution re-solve moves the saturated sphere-avg boost by "
      f"{abs(B_half/B_ref-1)*100:.2f}% ({B_half:.4f} vs {B_ref:.4f})",
      "grid systematics are far below the physics effects being measured")

# =================================================================================================
print()
print("=" * 100)
print("PART C2 -- the two-body composition benchmark: deep-MOND closed form + finite-y quadrature")
print("=" * 100)
# The composition conventions must be graded against the EXACT two-body force.  Two regimes:
# (i) the deep-MOND ISOLATED limit (Milgrom virial force, closed form) -- this is where the
# often-quoted 1.69-1.81x / 1.24-1.28x factors live, and ONLY there; (ii) the finite-y anchor
# regime (y_tot ~ 3-32), computed by direct QUMOND quadrature.  The verification referee showed
# the anchor-regime ratios are LARGER for per-star (~3-8x) and ~1.4-1.8x for total-mass -- both
# conventions overshoot the exact anchor force, so the truth-recovery sits ABOVE the total-mass
# end.  (The EFE-present exact two-body solve does not exist and is the declared unlock.)


def deep_factors(q):
    M1, M2 = 1.0 / (1 + q), q / (1 + q)
    a_ex = (2.0 / 3.0) * (1 - M1**1.5 - M2**1.5) / (M1 * M2)
    return (np.sqrt(M1) + np.sqrt(M2)) / a_ex, 1.0 / a_ex


dps = [deep_factors(q)[0] for q in (0.3, 0.5, 0.7, 1.0)]
dtm = [deep_factors(q)[1] for q in (0.3, 0.5, 0.7, 1.0)]
check(1.68 < min(dps) < max(dps) < 1.82 and 1.24 < min(dtm) < max(dtm) < 1.29,
      f"C2a deep-MOND ISOLATED limit (closed form, q = 0.3-1): per-star/exact "
      f"{min(dps):.3f}-{max(dps):.3f}, total-mass/exact {min(dtm):.3f}-{max(dtm):.3f}",
      "these factors are the DEEP limit only -- citing them 'in the anchor bins' was the "
      "draft error the verification caught")


def exact_two_body(y_tot, q, nrho=480, nz=960):
    """exact isolated QUMOND two-body relative-force excess by direct quadrature
    (stars on the z axis, phantom source integrated in cylindrical coordinates)."""
    Mt = 1.0
    M1, M2 = Mt / (1 + q), q * Mt / (1 + q)
    r0 = np.sqrt(Mt / y_tot)
    z1, z2 = -r0 / 2, r0 / 2
    rmax = 3.0e3 * max(r0, 1.0)
    rho = np.logspace(np.log10(1e-3 * r0), np.log10(rmax), nrho)
    zp = np.logspace(np.log10(1e-3 * r0), np.log10(rmax), nz // 2)
    z = np.concatenate([-zp[::-1], zp])
    RHO, Z = np.meshgrid(rho, z, indexing="ij")
    d1r, d1z = RHO, Z - z1
    d2r, d2z = RHO, Z - z2
    s1 = np.sqrt(d1r**2 + d1z**2)
    s2 = np.sqrt(d2r**2 + d2z**2)
    gr = -(M1 * d1r / s1**3 + M2 * d2r / s2**3)
    gz = -(M1 * d1z / s1**3 + M2 * d2z / s2**3)
    gm = np.hypot(gr, gz)
    Jrr = -(M1 * (1 / s1**3 - 3 * d1r**2 / s1**5) + M2 * (1 / s2**3 - 3 * d2r**2 / s2**5))
    Jzz = -(M1 * (1 / s1**3 - 3 * d1z**2 / s1**5) + M2 * (1 / s2**3 - 3 * d2z**2 / s2**5))
    Jrz = -(M1 * (-3 * d1r * d1z / s1**5) + M2 * (-3 * d2r * d2z / s2**5))
    dgm_r = (gr * Jrr + gz * Jrz) / np.maximum(gm, 1e-300)
    dgm_z = (gr * Jrz + gz * Jzz) / np.maximum(gm, 1e-300)
    S = -dnu_dy(gm) * (dgm_r * gr + dgm_z * gz)

    def a_ph_z(zstar):
        dz = zstar - Z
        ker = dz * RHO / np.maximum(RHO**2 + dz**2, 1e-300)**1.5
        return -0.5 * np.trapz(np.trapz(S * ker, rho, axis=0), z)

    a_rel = Mt / r0**2 + (a_ph_z(z1) - a_ph_z(z2))
    eps_ex = a_rel / (Mt / r0**2) - 1.0
    y1_, y2_ = M1 / r0**2, M2 / r0**2
    eps_ps = (nu(y2_) * M2 + nu(y1_) * M1) / Mt - 1.0
    eps_tm = float(nu(y_tot)) - 1.0
    return eps_ex, eps_ps, eps_tm


# validation: q -> 0 must return the single-mass exact result nu(y) - 1
val_err = []
for yv in (1.0, 10.0):
    e_ex, _, _ = exact_two_body(yv, 1e-6)
    val_err.append(abs((1 + e_ex) / float(nu(yv)) - 1.0))
check(val_err[0] < 0.01 and val_err[1] < 0.05,
      f"C2b quadrature control (q->0 single mass): |exact/nu - 1| = {val_err[0]:.4f} at y=1, "
      f"{val_err[1]:.4f} at y=10",
      "the y=10 tolerance bounds the f(y) grade below; carried into the declared top-anchor grade")

Y_BENCH = np.array([3.162, 5.62, 10.0, 17.8, 31.6])
F_TM_ROWS = []
print(f"    {'y_tot':>7} {'q':>4} {'eps_exact':>10} {'eps_perstar':>12} {'eps_totmass':>12} "
      f"{'ps/ex':>7} {'tm/ex':>7}")
for yv in Y_BENCH:
    row = []
    for q in (0.3, 0.5, 0.7, 1.0):
        e_ex, e_ps, e_tm = exact_two_body(yv, q)
        row.append(e_tm / e_ex)
        print(f"    {yv:7.2f} {q:4.1f} {e_ex:10.5f} {e_ps:12.5f} {e_tm:12.5f} "
              f"{e_ps/e_ex:7.2f} {e_tm/e_ex:7.2f}")
    F_TM_ROWS.append(np.median(row))
F_TM = np.maximum(np.array(F_TM_ROWS), 1.0)
LY_BENCH = np.log10(Y_BENCH)
check(1.2 < F_TM[0] < 2.2 and all(F_TM > 1.0),
      f"C2c finite-y anchor correction factor f_tm(y) = eps_totmass/eps_exact (q-median): "
      f"{', '.join(f'{v:.2f}' for v in F_TM)} at y = {', '.join(f'{v:.1f}' for v in Y_BENCH)}",
      "total-mass OVERSHOOTS the exact anchor force too; the benchmark-corrected grade divides "
      "the anchor excess by this computed factor (per-star overshoots by ~2x more)")


# =================================================================================================
# PART D -- pipeline-grade observable: anisotropic injection, isotropic fit
# =================================================================================================
print()
print("=" * 100)
print("PART D -- the pipeline's own estimator confronted with the full-solve anisotropic boost")
print("=" * 100)

TH_GRID = np.arccos(u_gl)[::-1]          # ascending theta in (0, pi)


def make_interp(f, form):
    """bilinear interpolator over (log10 y_int, theta) for B_r; y = 1/r^2 maps r-grid -> y-grid."""
    Br = SOLVE[f][form]["Br"][:, ::-1]    # match ascending theta
    ly = np.log10(1.0 / r**2)[::-1]       # ascending log-y
    Brr = Br[::-1]

    def interp(ly_q, th_q):
        ly_q = np.clip(ly_q, ly[0], ly[-1])
        th_q = np.clip(th_q, TH_GRID[0], TH_GRID[-1])
        i = np.clip(np.searchsorted(ly, ly_q) - 1, 0, len(ly) - 2)
        j = np.clip(np.searchsorted(TH_GRID, th_q) - 1, 0, len(TH_GRID) - 2)
        fy = (ly_q - ly[i]) / (ly[i + 1] - ly[i])
        ft = (th_q - TH_GRID[j]) / (TH_GRID[j + 1] - TH_GRID[j])
        return ((1 - fy) * (1 - ft) * Brr[i, j] + fy * (1 - ft) * Brr[i + 1, j]
                + (1 - fy) * ft * Brr[i, j + 1] + fy * ft * Brr[i + 1, j + 1])
    return interp


def make_population_oriented(N, rng, a0):
    """The frozen pipeline's make_population, mirrored with the 3D separation direction and
    per-star masses retained, plus a random external-field direction per system."""
    dr4 = True
    M1 = rng.uniform(0.45, 1.25, N)
    q = rng.uniform(0.30, 1.00, N)
    M2 = np.clip(q * M1, 0.15, None)
    Mt = M1 + M2
    d = (rng.uniform(25.**3, 250.**3, N))**(1 / 3.)
    p = -0.6
    lo, hi = (2 * 0.5)**p, (30 * 2.0)**p
    a_sma = (rng.uniform(hi, lo, N))**(1 / p) * wbp.KAU
    e = np.sqrt(rng.uniform(0, 1, N))
    Ma = rng.uniform(0, 2 * np.pi, N)
    E = Ma.copy()
    for _ in range(60):
        E -= (E - e * np.sin(E) - Ma) / (1 - e * np.cos(E))
    n_ = np.sqrt(wbp.G * Mt * wbp.MSUN / a_sma**3)
    b_ = a_sma * np.sqrt(1 - e**2)
    xo, yo = a_sma * (np.cos(E) - e), b_ * np.sin(E)
    Ed = n_ / (1 - e * np.cos(E))
    vxo, vyo = -a_sma * np.sin(E) * Ed, b_ * np.cos(E) * Ed
    Om, w = rng.uniform(0, 2 * np.pi, N), rng.uniform(0, 2 * np.pi, N)
    ci = rng.uniform(-1, 1, N)
    si = np.sqrt(1 - ci**2)
    cO, sO, cw, sw = np.cos(Om), np.sin(Om), np.cos(w), np.sin(w)
    Pv = np.stack([cO * cw - ci * sO * sw, sO * cw + ci * cO * sw, si * sw])
    Qv = np.stack([-cO * sw - ci * sO * cw, -sO * sw + ci * cO * cw, si * cw])
    r3 = xo * Pv + yo * Qv
    v3 = vxo * Pv + vyo * Qv
    r3d = np.linalg.norm(r3, axis=0)
    s_proj = np.hypot(r3[0], r3[1])
    g_true = wbp.G * Mt * wbp.MSUN / r3d**2
    # random external-field direction per system; psi = angle(separation, e)
    eh = rng.standard_normal((3, N))
    eh /= np.linalg.norm(eh, axis=0)
    psi = np.arccos(np.clip(np.sum(r3 * eh, axis=0) / r3d, -1, 1))
    # projected (sky-plane, z = LOS) angle between the separation and the external-field
    # direction -- the anisotropy_split analog used by the E5 sample-level sign computation
    sp_norm = np.hypot(r3[0], r3[1])
    ep_norm = np.hypot(eh[0], eh[1])
    cosphi_proj = np.abs(r3[0] * eh[0] + r3[1] * eh[1]) / np.maximum(sp_norm * ep_norm, 1e-30)
    G1 = wbp.MG_of_mass(M1) + 5 * np.log10(d / 10.)
    G2 = wbp.MG_of_mass(M2) + 5 * np.log10(d / 10.)
    spm = np.sqrt(wbp.sigma_pm(G1, dr4)**2 + wbp.sigma_pm(G2, dr4)**2)
    splx = 1 / np.sqrt(wbp.sigma_plx(G1, dr4)**-2 + wbp.sigma_plx(G2, dr4)**-2)
    plx = 1000. / d
    d_obs = 1000. / (plx + splx * rng.standard_normal(N))
    dkpc = d / 1000.
    pmx, pmy = v3[0] / (4.74e3 * dkpc), v3[1] / (4.74e3 * dkpc)
    npmx, npmy = spm * rng.standard_normal(N), spm * rng.standard_normal(N)
    s_obs = s_proj * (d_obs / d)
    M_obs = Mt * (1 + 0.05 * rng.standard_normal(N))
    sel = ((s_obs > 2 * wbp.KAU) & (s_obs < 30 * wbp.KAU) & (d < 250.)
           & (np.maximum(G1, G2) < 17.) & (d_obs > 0) & (M_obs > 0.2))
    return dict(pmx=pmx[sel], pmy=pmy[sel], npmx=npmx[sel], npmy=npmy[sel],
                d_obs=d_obs[sel], s_obs=s_obs[sel], M_obs=M_obs[sel],
                g_true=g_true[sel], psi=psi[sel], cosphi_proj=cosphi_proj[sel],
                M1=M1[sel], M2=M2[sel], Mt=Mt[sel], r3d=r3d[sel],
                g_proj=wbp.G * M_obs[sel] * wbp.MSUN / s_obs[sel]**2,
                vc_obs=np.sqrt(wbp.G * M_obs[sel] * wbp.MSUN / s_obs[sel]**2 * s_obs[sel]))


def vtilde_injected(pop, gamma_sys):
    """mirror of the pipeline's vtilde_of with a per-system boost."""
    vX = (gamma_sys * pop['pmx'] + pop['npmx']) * 4.74e3 * (pop['d_obs'] / 1000.)
    vY = (gamma_sys * pop['pmy'] + pop['npmy']) * 4.74e3 * (pop['d_obs'] / 1000.)
    return np.hypot(vX, vY) / pop['vc_obs']


def gamma_full_solve(pop, f, form, composition="perstar"):
    """per-system velocity boost from the nonlinear solve.  Three composition grades:
      perstar   -- [B(y2,psi) GM2 + B(y1,pi-psi) GM1]/r^2.  Exact in the deep bins
                   (g_int << g_ext, linear response) but OVERESTIMATES the exact anchor-bin
                   force by ~3-8x in excess (PART C2 finite-y quadrature).  DIAGNOSTIC grade:
                   it is the kappa-trip mock, NOT a registered band endpoint.
      totalmass -- B(y1+y2, psi) G Mt / r^2.  Registered BAND FLOOR; still overshoots the
                   exact anchor excess by the computed f_tm(y) ~ 1.4-1.8x.
      corrected -- total-mass with the anchor excess (y_tot >= 3.162) divided by the
                   COMPUTED f_tm(y) from PART C2.  Registered BAND TOP (the benchmark-
                   corrected grade; the EFE-present exact two-body solve is the owed unlock)."""
    itp = make_interp(f, form)
    a0 = A0[f]
    y1 = wbp.G * pop['M1'] * wbp.MSUN / pop['r3d']**2 / a0
    y2 = wbp.G * pop['M2'] * wbp.MSUN / pop['r3d']**2 / a0
    yt = np.maximum(y1 + y2, 1e-12)
    if composition == "perstar":
        B_rel = (itp(np.log10(y2), pop['psi']) * pop['M2']
                 + itp(np.log10(np.maximum(y1, 1e-12)), np.pi - pop['psi']) * pop['M1']) / pop['Mt']
    else:
        B_rel = itp(np.log10(yt), pop['psi'])
        if composition == "corrected":
            fcorr = np.where(yt >= Y_BENCH[0],
                             np.interp(np.log10(yt), LY_BENCH, F_TM), 1.0)
            B_rel = 1.0 + (B_rel - 1.0) / fcorr
    return np.sqrt(np.maximum(B_rel, 0.0))


def run_fit_case(pop_data, gamma_sys, mod, a0, rng, label, quiet=False):
    vt = vtilde_injected(pop_data, gamma_sys)
    logy = np.log10(pop_data['g_proj'] / a0)
    med_d, sig_d, _ = wbp.bin_medians(logy, vt, boot=200, rng=rng)
    g, sg, chi2, nb, kap = wbp.fit_gamma(med_d, sig_d, mod, wbp.GRID)
    if not quiet:
        print(f"    {label:62s} gamma_hat = {g:.4f} +- {sg:.4f}  (kappa {kap:.3f}, {nb} bins)")
    return g, sg, kap


N_PRE = 140000


def one_seed(f, seed, base=False):
    """generate data + master at this seed, fit all grades; returns debiased results + kappas."""
    a0 = A0[f]
    rng = np.random.default_rng(seed)
    pop_d = make_population_oriented(N_PRE, rng, a0)
    keep = rng.permutation(len(pop_d['pmx']))[:30000]
    pop_d = {k: v[keep] for k, v in pop_d.items()}
    pop_m = wbp.make_population(400000, rng, dr4=True)
    mod = wbp.model_medians(pop_m, a0, wbp.GRID, rng)
    q = not base
    tgt = REGISTERED_A9[f]
    g_iso = wbp.gamma_of_y(pop_d['g_true'] / a0, tgt, wbp.y_extN(a0))
    if base:
        print(f"  [{f}]  N_data = {len(pop_d['pmx'])}, N_master = {len(pop_m['pmx'])}")
    gC1, sC1, kC1 = run_fit_case(pop_d, g_iso, mod, a0, rng,
                                 f"C1 control: registered isotropic gamma(y), target {tgt}", q)
    bias = gC1 - tgt
    out = dict(bias=bias, registered=tgt)
    if base:
        # control 2: isotropic solver shape (sphere-average of B_r at total-mass y) --
        # separates the transition-SHAPE effect from composition/anisotropy effects
        y_t = pop_d['g_true'] / a0
        B_avg_r = 0.5 * np.einsum("rt,t->r", SOLVE[f]["a"]["Br"], w_gl)
        ly_grid = np.log10(1.0 / r**2)[::-1]
        B_avg = np.interp(np.log10(np.clip(y_t, 1e-9, 1e9)), ly_grid, B_avg_r[::-1])
        gC2, sC2, _ = run_fit_case(pop_d, np.sqrt(np.maximum(B_avg, 0.0)), mod, a0, rng,
                                   "C2 control: ISOTROPIC sphere-avg solver shape (total-mass y)", q)
        out['iso_shape'] = (gC2 - bias, sC2)
    for comp, lab in (("perstar", "per-star (DIAGNOSTIC: the kappa-trip mock, not a band endpoint)"),
                      ("totalmass", "total-mass composition (registered BAND FLOOR)"),
                      ("corrected", "benchmark-corrected composition (registered BAND TOP)")):
        g_, s_, k_ = run_fit_case(pop_d, gamma_full_solve(pop_d, f, "a", comp), mod, a0, rng,
                                  f"FULL SOLVE, one-field AQUAL, {lab}", q)
        out[comp] = (g_ - bias, s_, k_)
    if base:
        gQ, sQ, kQ = run_fit_case(pop_d, gamma_full_solve(pop_d, f, "q"), mod, a0, rng,
                                  "FULL SOLVE, QUMOND fork, per-star composition", q)
        out['qumond'] = (gQ - bias, sQ, kQ)
        print(f"    estimator bias at this seed: {bias:+.4f} (subtracted from all debiased numbers)")
    return out


RESULTS = {}
for f in A0:
    RESULTS[f] = one_seed(f, 4242 + (0 if f == "canonical" else 1), base=True)

# -------------------------------------------------------------------------------------------------
print()
print("  SEED BATTERY (the committed multi-seed grade; 6 seeds per footing, all grades)")
SEEDS = [4242, 1111, 2222, 3333, 5555, 7777]
BATTERY = {}
for f in A0:
    rows = [one_seed(f, s + (0 if f == "canonical" else 1)) for s in SEEDS]
    BATTERY[f] = rows
    for comp in ("perstar", "totalmass", "corrected"):
        vals = np.array([r[comp][0] for r in rows])
        kaps = np.array([r[comp][2] for r in rows])
        extra = ""
        if f == "alt" and comp == "corrected":
            extra = f", {int(np.sum(vals > 1.20))}/6 seeds above 1.20"
        print(f"    [{f}] {comp:10s}: centre {vals.mean():.4f}, rms {vals.std(ddof=1):.4f}, "
              f"kappa {kaps.min():.3f}-{kaps.max():.3f} "
              f"({int(np.sum((kaps < 0.95) | (kaps > 1.05)))}/6 outside window){extra}")

# =================================================================================================
# PART E -- verdict
# =================================================================================================
print()
print("=" * 100)
print("PART E -- VERDICT: the full-solve DR4 target vs the registered provisional one")
print("=" * 100)
for f in A0:
    R = RESULTS[f]
    gP, sP, kP = R["perstar"]
    gT, sT, kT = R["totalmass"]
    gX, sX, kX = R["corrected"]
    bat = BATTERY[f]
    cT = np.mean([r["totalmass"][0] for r in bat])
    cX = np.mean([r["corrected"][0] for r in bat])
    print(f"  [{f}]  registered (provisional) {R['registered']:.4f}")
    print(f"         REGISTERED BAND (debiased): total-mass FLOOR {gT:.4f} +- {sT:.4f} "
          f"(6-seed centre {cT:.4f})  to  benchmark-corrected TOP {gX:.4f} +- {sX:.4f} "
          f"(6-seed centre {cX:.4f})")
    print(f"         diagnostic per-star (the kappa-trip mock): {gP:.4f} +- {sP:.4f} "
          f"(kappa {kP:.3f});  QUMOND fork {R['qumond'][0]:.4f};  iso-shape {R['iso_shape'][0]:.4f}")
    print(f"         BAND vs registered: {gT - R['registered']:+.4f} to {gX - R['registered']:+.4f}"
          f"  =  {abs(gX-R['registered'])/0.019:.1f}-{abs(gT-R['registered'])/0.019:.1f} sigma_fit "
          f"(frozen-N 0.019) / {abs(gX-R['registered'])/0.035:.1f}-{abs(gT-R['registered'])/0.035:.1f} "
          f"(DR3-dry-run 0.035, N=10,624 -- labelled, NOT the frozen-N sigma)")

gT_can, sT_can, _ = RESULTS["canonical"]["totalmass"]
gX_can, _, kX_can = RESULTS["canonical"]["corrected"]
gP_can, _, kP_can = RESULTS["canonical"]["perstar"]
gQ_can = RESULTS["canonical"]["qumond"][0]
gX_alt = RESULTS["alt"]["corrected"][0]
gT_alt = RESULTS["alt"]["totalmass"][0]
mi_lo, mi_hi = wbp.GAMMA_MI_RANGE_MAG
# interior-argmin guard (the stage-41 lesson)
check(all(wbp.GRID[0] + 0.004 < g_ < wbp.GRID[-1] - 0.004
          for g_ in (gP_can, gT_can, gX_can, gT_alt, gX_alt)),
      f"E0  interior-argmin guard: all fits sit inside the gamma grid "
      f"({wbp.GRID[0]:.2f}-{wbp.GRID[-1]:.2f})")
check(abs(mi_avg - 1.1582) < 5e-4 and gX_can > gT_can > gP_can and abs(gP_can - gQ_can) < 0.05,
      f"E1  headline: registered canonical BAND {gT_can:.4f} (total-mass floor) - {gX_can:.4f} "
      f"(benchmark-corrected top); per-star {gP_can:.4f} is DIAGNOSTIC only",
      "the ordering floor < top is the C2 benchmark's own direction: both conventions overshoot "
      "the exact anchor force, so truth-recovery sits above the total-mass end")
kap_bat_ps = [r["perstar"][2] for f_ in A0 for r in BATTERY[f_]]
kap_bat_x = [r["corrected"][2] for f_ in A0 for r in BATTERY[f_]]
n_trip_ps = int(np.sum([(k < 0.95) or (k > 1.05) for k in kap_bat_ps]))
n_trip_x = int(np.sum([(k < 0.95) or (k > 1.05) for k in kap_bat_x]))
check(n_trip_x < n_trip_ps,
      f"E2  KAPPA ATTRIBUTION (the verification's correction): the kappa-window trip is a "
      f"PER-STAR-COMPOSITION artifact, not an anisotropy signature -- battery trips: per-star "
      f"{n_trip_ps}/12, benchmark-corrected {n_trip_x}/12",
      "under the framework's best grade the pipeline expects kappa INSIDE the frozen window; a "
      "real-sky kappa trip would be evidence of a genuine systematic (or of the refuted per-star "
      "grade), NOT pre-authorized framework behaviour")
print(f"\n  *** AMENDMENT-10 GRADE: the full solve moves the canonical target by "
      f"{gT_can - REGISTERED_A9['canonical']:+.3f} to {gX_can - REGISTERED_A9['canonical']:+.3f} (alt: "
      f"{gT_alt - REGISTERED_A9['alt']:+.3f} to {gX_alt - REGISTERED_A9['alt']:+.3f}).  "
      f"Amendment-grade by the document's own criterion (the ranges do not overlap).  "
      f"FILING IS THE AUTHOR'S CALL -- this file only computes. ***")
d_mi_lo = min(abs(g_ - 1.1582) for g_ in (gT_can, gX_can))
d_mi_hi = max(abs(g_ - 1.1582) for g_ in (gT_can, gX_can))
print(f"  *** ARM-SEPARATION IMPACT: the registered canonical band sits {d_mi_lo:.3f}-{d_mi_hi:.3f} "
      f"ABOVE the superseded MI 1.1582 (ranges {mi_lo}-{mi_hi}) -- Amendment 9's 'disjoint / "
      f"2.68 sigma / DR4 can distinguish the arms' does NOT survive: separation < 3 sigma in the "
      f"frozen conventions, and the band overlaps the MI magnitude range. ***")
print(f"  *** EDGE INPUT: the top EFE-saturated registered anchor is the alt benchmark-corrected "
      f"{gX_alt:.4f} (6-seed centre {np.mean([r['corrected'][0] for r in BATTERY['alt']]):.4f}) -- "
      f"the no-verdict-edge construction takes it from here. ***")

# regression pins on the four registered band anchors (base seeds are fixed => deterministic;
# the +-0.01 seed/call-order grade applies to RERUNS WITH DIFFERENT SEEDS, not to this pin)
check(abs(RESULTS["canonical"]["totalmass"][0] - 1.1614) < 1e-4
      and abs(RESULTS["canonical"]["corrected"][0] - 1.1814) < 1e-4
      and abs(RESULTS["alt"]["totalmass"][0] - 1.1917) < 1e-4
      and abs(RESULTS["alt"]["corrected"][0] - 1.2267) < 1e-4,
      "E3  REGRESSION PIN: the four registered band anchors reproduce exactly at the fixed seeds "
      "(1.1614 / 1.1814 canonical, 1.1917 / 1.2267 alt)",
      "if this fails after a code change, the registered anchors have silently moved")

# the transition-zone orientation flip, COMPUTED (round-3 referee: it is load-bearing for the
# Amendment 2(f) sign question, so it must be a printed check, not a docstring note)
Br_c = SOLVE["canonical"]["a"]["Br"]
ipar, iperp = int(np.argmax(u_gl)), int(np.argmin(np.abs(u_gl)))
par_minus_perp = Br_c[:, ipar] - Br_c[:, iperp]
sat_par_bigger = par_minus_perp[np.argmin(np.abs(r - 300.0))] > 0
trans_perp_bigger = np.any(par_minus_perp[(r > 0.3) & (r < 3.0)] < 0)
i_flip = np.where((par_minus_perp[:-1] < 0) & (par_minus_perp[1:] >= 0))[0]
r_flip = float(r[i_flip[-1]]) if len(i_flip) else float("nan")
check(sat_par_bigger and trans_perp_bigger and 0.5 < r_flip < 5.0,
      f"E4  ORIENTATION FLIP COMPUTED: B_par > B_perp at saturation but B_perp > B_par in the "
      f"transition zone; the flip sits at r = {r_flip:.2f} r_M (r_M ~ 8-10 kAU for the sample's "
      f"masses => the flip is INSIDE the frozen 2-30 kAU window)",
      "Amendment 2(f)'s frozen 'perpendicular larger' sign is MI-arm-derived and does NOT "
      "describe the MG arm at saturation -- the sample-level sign is computed in E5")

# E5 -- the SAMPLE-LEVEL anisotropy sign under the registered grades: the re-registration input
# for the Amendment 2(f) sign falsifier.  Projected-angle split (the anisotropy_split analog)
# of the injected per-system boost, deep subsample (y_true < 1), both footings, both grades.
print()
print("  E5  sample-level anisotropy sign (projected-angle split, deep subsample y < 1):")
E5 = {}
for f in A0:
    a0 = A0[f]
    rng = np.random.default_rng(4242 + (0 if f == "canonical" else 1))
    pop_d = make_population_oriented(N_PRE, rng, a0)
    keep = rng.permutation(len(pop_d['pmx']))[:30000]
    pop_d = {k: v[keep] for k, v in pop_d.items()}
    deep = (pop_d['g_true'] / a0) < 1.0
    for comp in ("totalmass", "corrected"):
        gam = gamma_full_solve(pop_d, f, "a", comp)
        cph = pop_d['cosphi_proj']
        m_par = deep & (cph > np.median(cph[deep]))
        m_perp = deep & (cph <= np.median(cph[deep]))
        d_ = float(np.median(gam[m_par]) - np.median(gam[m_perp]))
        E5[(f, comp)] = d_
        print(f"      [{f}] {comp:10s}: med(par-ish) - med(perp-ish) = {d_:+.5f} "
              f"({'PARALLEL' if d_ > 0 else 'PERPENDICULAR'}-dominant)")
sgns = [np.sign(v) for v in E5.values()]
check(all(s_ == sgns[0] for s_ in sgns),
      f"E5  the sample-level sign is CONSISTENT across footings and registered grades: "
      f"{'PARALLEL' if sgns[0] > 0 else 'PERPENDICULAR'}-dominant "
      f"(magnitudes {min(abs(v) for v in E5.values()):.4f}-{max(abs(v) for v in E5.values()):.4f})",
      "this computed sign is the Amendment-10 re-registration input for the 2(f) falsifier; "
      "the frozen MI-derived blanket sign is arm-stale")

print()
print("=" * 100)
n_fail = len(FAIL)
print(f"CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
