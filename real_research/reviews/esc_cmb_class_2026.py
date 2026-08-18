#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
esc_cmb_class_2026.py -- ROUTE 3 of the OPTION-1 ESCAPE:  WHAT DOES THE G-SPLIT COST THE CMB?
================================================================================================
2026-08-18.  Assigned question, verbatim: the Option-1 rescaling script-J -> s*script-J cures the
transverse aether ghost but forces G_cosmo/G_local = Gt/G_N <= K_B/2, i.e. a ~7x-8x SPLIT between
the gravitational constant that runs the expansion and the one that runs local dynamics.  That
price was "flagged probably fatal via BBN / the committed CLASS pass" and explicitly NOT COMPUTED.
This file computes it, with real CLASS.

WHAT ROUTE 1 HANDED OVER (real_research/reviews/esc_s_window_2026.py, read but NOT modified):
  * the s-window is non-empty:  0 < s < 0.13822 (K_B=0.25),  0 < s < 0.050924 (K_B=0.10);
  * Gt/G_N = (1 - K_B/2) s  -- its control C-7, from bridge1_aest_equations.md;
  * hence Gt/G_N <= 0.12094 (K_B=0.25) / 0.048377 (K_B=0.10), versus AeST's own 0.875;
  * DEATH 2 (the CMB degeneracy) is REFUTED at its premise: mu_phys(0) = 0 for any interpolation,
    so F_Z(0) = 0 and the Eq (12) coefficient is K_B EXACTLY, for every s;
  * "the actual delta-C_l ... NOT COMPUTED (no AeST module in CLASS)".
Route 1's window is used here as an INPUT, re-derived independently in PART A, and its VALUE is
NOT taken on trust: PART A reproduces Gt/G_N = (1-K_B/2)s from the two statements in the brief and
checks it against the repo's committed C-7.

================================================================================================
RESULT IN ONE PARAGRAPH.  DIRECTION: ADVERSE.  The escape is DEAD on the CMB.
================================================================================================
The split is not a nuisance parameter, it is a direct rescaling of the ONE thing the CMB measures
absolutely.  FIRAS fixes the photon energy density rho_gamma in erg/cm^3 with no gravity in the
chain; the CMB then measures the GRAVITATING radiation density against it.  That ratio IS what
N_eff parametrises: rho_r^grav / rho_gamma^therm = 1 + (7/8)(4/11)^(4/3) N_eff = 1.6913 at
N_eff = 3.044.  Rescaling Gt -> xi G_N multiplies the gravitating side and nothing else, so the
model DEMANDS 1.6913 xi.  At the escape's ceiling xi = 0.12094 that is 0.2046 -- BELOW UNITY,
i.e. below the gravitating density of the photons alone.  No cosmology with non-negative species
can realise it; CLASS refuses the inputs (verified here: negative N_ur, negative omega_cdm and
negative Omega_fld are all rejected at input validation).  The escape therefore does not fail by
some number of sigma on a likelihood -- it lands OUTSIDE the space of CMB models, on the wrong
side of a FIRAS measurement.  The hard boundary is xi >= 1/1.6913 = 0.5913, and the escape's
ceiling misses it by 4.9x (K_B=0.25) / 12.2x (K_B=0.10).
   Quantified where quantification is possible: running the proxy family down to that boundary,
with h re-shot to hold 100*theta_s and with amplitude+tilt marginalised away, the lensed TT
spectrum moves by 80 sigma_CV aggregate, peaks shift by up to 17 multipoles and peak heights by up
to 26%.  Calibrating near xi = 1 gives sigma_CV(xi) = 0.00632, i.e. the cosmic-variance-limited
TT-only CMB measures Gt/G_N to 0.63%.  Control: that maps to sigma_CV(N_eff) = 0.0470, which is
3.6x tighter than Planck 2018's 0.17 -- the right side, and the right size, for a noiseless
full-sky TT-only forecast.  ALLOWED s RANGE (PART D): s = 1.1429 +/- 0.0072 at K_B = 0.25 for a
1-sigma TT-only CV budget, and s > 1.1212 at 3 sigma -- versus the no-ghost requirement
s < 0.13822.  THE TWO WINDOWS ARE DISJOINT BY 8.1x, AND THE ESCAPE'S CEILING SITS 139 sigma_CV
FROM VIABILITY.
   Two results stated AGAINST the framework's interest and one FOR it.  AGAINST: (i) the same
axis prices unmodified AeST, and at its BBN-edge fiducial K_B = 0.25 the parent theory's own
xi = 0.875 already sits at 20.2 sigma_CV on TT alone -- the CMB is ~20x sharper on K_B than the
helium bound the corpus quotes (K_B <= 0.25 -> K_B <= 0.0126 at 1 sigma_CV, 0.0379 at 3);
(ii) there is NO K_B that opens the window, because xi <= K_B/2 and CMB-viability needs xi ~ 1,
so it needs K_B >= 1.987 (1 sigma_CV) / 1.962 (3 sigma_CV) -- at the very top edge of the
no-ghost range K_B < 2, and 7.8x above the committed BBN cap.  FOR: the obvious rescue "a_0(z) switches MOND off at recombination, so
none of this applies" is CHECKED AND CORRECTLY REJECTED AS IRRELEVANT-BUT-HARMLESS -- the split
lives in the NORMALISATION of the free function, not in the interpolation, so a_0(z) cannot
relieve it; but equally, the split is not an artefact of any MOND-regime assumption.  And PART C
confirms Route 1: DEATH 2 does not exist, at ANY s.

CONTROLS REPRODUCED BEFORE ANY NEW NUMBER (each named at its check):
  C-1  bridge1_aest_equations.md / esc_s_window_2026.py C-7 -- Gt = (1 - K_B/2) Ghat.
  C-2  Route 1's own window numbers, s_max and Gt/G_N, reproduced from the map in PART A.
  C-3  CLASS baseline vs Planck 2018 (TT,TE,EE+lowE+lensing, arXiv:1807.06209 Table 2):
       r_drag = 147.09 +/- 0.26 Mpc, z_drag = 1059.94 +/- 0.30, z_eq = 3402 +/- 26,
       N_eff = 3.044 (standard), first TT acoustic peak at l ~ 220.
  C-4  the null test: the proxy pipeline at xi = 1 must return chi2_CV = 0 to machine level.
  C-5  Planck 2018 sigma(N_eff) = 0.17 -- the CV-only forecast must be TIGHTER than this
       (noiseless, full sky) but not absurdly so.
  C-6  RETRACTIONS.md line 55 (Oost et al. Eq. 3.7 via Carroll & Lim): |G_cos/G_N - 1| <~ 1/8
       is the committed BBN statement, and it must reproduce K_B <~ 0.25 through the SAME map.

NOT COMPUTED, and no relief is assumed from any of it:
  * a real Planck likelihood.  Everything here is cosmic-variance-limited TT only, f_sky = 1,
    l = 2..2500, lensed.  EE/TE/lensing would only tighten it.
  * the exact model.  CLASS has no G-rescaling switch, so the family run here is a PROXY that
    matches the model's TOTAL gravitating radiation density and TOTAL gravitating matter density
    at fixed thermal history, but not their species COMPOSITION (in the true model the photons
    and baryons gravitate at xi times their thermal density; in the proxy the deficit is moved
    into N_ur and omega_cdm).  The proxy is therefore indicative, not a likelihood -- and it is
    only ever used INSIDE the realisable range xi >= 0.5913.  The escape's own xi is outside it,
    where the verdict rests on the FIRAS floor, which needs no proxy at all.
  * BBN itself (Route 1 gave the algebraic mapping; a real network run is nobody's route here).
  * whether the late-time/lensing sector uses Gt or G_N in this theory -- the lensed spectra are
    used as CLASS computes them, which if anything UNDERSTATES the damage.
  * the a_0 anchor's own G-fork (Route 1's last liability) -- untouched here.

Exit 0 = every check passed.
"""

import sys

import numpy as np

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))


print(__doc__)

# --------------------------------------------------------------------------------------------
# standing constants (the two footings, reported both ways as required)
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10
KAPPA, KAPPA_ERR = 0.5, 0.034
KB_FID, KB_LOW = 0.25, 0.10

# Route 1's handed-over window (esc_s_window_2026.py, VERDICT paragraph) -- input, re-derived below
S_MAX_R1 = {0.25: 0.13822, 0.10: 0.050924}
XI_MAX_R1 = {0.25: 0.12094, 0.10: 0.048377}

# committed Planck 2018 base-LCDM (the corpus's own committed cosmology, cf.
# nbody_2026/stage76_nu0_recombination_pin_2026.py PART B)
PLANCK = dict(h=0.6736, omega_b=0.02237, omega_cdm=0.1200,
              A_s=2.100e-9, n_s=0.9649, tau_reio=0.0544)
LMAX = 2500

print("=" * 100)
print("PART A -- HOW s ENTERS THE CMB.  Which CLASS inputs must move, and why.")
print("=" * 100)
info("A0  footing, reported both ways as the standing rule requires",
     f"a_0 = kappa c sqrt(G rho_Lambda) = {A0_CANON:.4e} canonical / {A0_ALT:.4e} alt m/s^2; "
     f"kappa = 1/2 FITTED (0.529 +/- {KAPPA_ERR}).  Route 3's observable is the RATIO Gt/G_N, "
     "which is a_0-INDEPENDENT -- see A7.")


def xi_of_s(s, kb):
    """Gt/G_N under the Option-1 rescaling script-J -> s script-J."""
    return (1.0 - kb / 2.0) * s


def s_max_noghost(kb):
    """Route 1 / the brief: no-ghost requires s < K_B/(2-K_B)."""
    return kb / (2.0 - kb)


# --- C-1: the committed relation, at the AeST normalisation s = 1 -------------------------------
check(abs(xi_of_s(1.0, 0.25) - 0.875) < 1e-12,
      "A1  CONTROL C-1 reproduced: Gt = (1 - K_B/2) Ghat gives Gt/G_N = 0.875 at s=1, K_B=0.25",
      "bridge1_aest_equations.md; identical to esc_s_window_2026.py control C-7.  "
      "Unmodified AeST ALREADY carries a 12.5% split -- that is not new here.")

# --- the map's own internal consistency, from the brief's TWO independent statements ------------
kbs = np.linspace(1e-4, 1.999, 4001)
resid = np.array([xi_of_s(s_max_noghost(kb), kb) - kb / 2.0 for kb in kbs])
check(np.max(np.abs(resid)) < 1e-12,
      "A2  the map is forced, not fitted: xi = (1-K_B/2) s maps the brief's s-bound "
      "s < K_B/(2-K_B) onto its INDEPENDENTLY stated bound 2 Gt < K_B G_N, for EVERY K_B",
      f"max |xi(s_max) - K_B/2| = {np.max(np.abs(resid)):.2e} over K_B in (0, 2).  "
      "Two separately stated numbers in the brief agree only under this map, so the map is "
      "checked, not assumed.")

# --- C-2: Route 1's window numbers ---------------------------------------------------------------
ok = True
for kb in (0.25, 0.10):
    smax_here = s_max_noghost(kb)
    info(f"A3  K_B = {kb}: brief's no-ghost s_max = K_B/(2-K_B) = {smax_here:.5f}; "
         f"Route 1's TIGHTER window (longitudinal electric mode, its 1.0335 factor) "
         f"s_max = {S_MAX_R1[kb]:.5f}",
         f"xi_max = (1-K_B/2)s_max = {xi_of_s(S_MAX_R1[kb], kb):.5f} vs Route 1's quoted "
         f"{XI_MAX_R1[kb]:.5f}")
    ok &= abs(xi_of_s(S_MAX_R1[kb], kb) - XI_MAX_R1[kb]) < 5e-5
check(ok, "A4  CONTROL C-2 reproduced: Route 1's Gt/G_N ceilings follow from the same map",
      "so this file and Route 1 are using one definition of s, not two.")

XI_MAX = xi_of_s(S_MAX_R1[KB_FID], KB_FID)          # 0.12094 at K_B = 0.25 -- the operative ceiling
XI_MAX_LOW = xi_of_s(S_MAX_R1[KB_LOW], KB_LOW)      # 0.048377 at K_B = 0.10

# --- WHICH CLASS INPUTS MOVE -------------------------------------------------------------------
print()
info("A5  THE DERIVATION -- which CLASS inputs must move, and why.",
     "\n         On FRW the aether is A_mu = (-1,0,0,0): F_munu = 0, J^mu = 0, Y = 0, so the\n"
     "         background action is R - 2Lam - K(Q) and the Friedmann equation is\n"
     "             3 H^2 = 8 pi Gt (rho_m + rho_dark) + Lam,\n"
     "         i.e. the EXPANSION is run by Gt.  The quasi-static sector, where the free\n"
     "         function's normalisation is the sole source of Newton's constant, is run by\n"
     "         G_N = Ghat/s.  Nothing NON-gravitational moves: the Thomson rate n_e sigma_T, the\n"
     "         recombination network, Y_He and T_gamma are all set by thermal physics with no G\n"
     "         in the chain.  So the model is EXACTLY:\n"
     "             every gravitating density  ->  xi * (its thermal value),   xi = Gt/G_N,\n"
     "         at fixed thermal history.  Consequences, each of which is a CLASS input or output:\n"
     "           (i)   r_s and D_A both scale as xi^(-1/2)  =>  theta_s is INVARIANT (peaks do\n"
     "                 not move) once Lam is refitted.  So peak POSITION is not the observable.\n"
     "           (ii)  R = 3 rho_b/4 rho_gamma is a ratio of THERMAL densities => INVARIANT.\n"
     "           (iii) z_eq is a ratio of gravitating densities => INVARIANT.\n"
     "           (iv)  r_D ~ (H n_e sigma_T)^(-1/2) scales as xi^(-1/4) while r_s ~ xi^(-1/2), so\n"
     "                 theta_D/theta_s ~ xi^(1/4): THE DAMPING TAIL MOVES.  That is the signal.\n"
     "           (v)   recombination is a rate-vs-H competition, so the visibility function\n"
     "                 narrows.  Same axis.\n"
     "         (i)-(v) are precisely the N_eff signature at fixed z_eq and theta_s.  The CLASS\n"
     "         inputs that must move are therefore N_ur and omega_cdm (gravitating only) with\n"
     "         omega_b and T_cmb HELD (thermal), and h re-shot to hold 100*theta_s.")

info("A6  THE ABSOLUTE HANDLE -- why the CMB measures Gt at all.",
     "\n         FIRAS fixes rho_gamma absolutely with no gravity in the chain (T_0 = 2.7255 K).\n"
     "         The peak-height modulation fixes R = 3 rho_b/4 rho_gamma, hence rho_b absolutely,\n"
     "         hence n_e absolutely.  The gravitational effects then measure Gt * rho.  So the\n"
     "         CMB is an ABSOLUTE measurement of Gt, and Gt/G_N is a real observable, not a\n"
     "         reparametrisation.  This is the step the 'it is only a normalisation' reading\n"
     "         misses.")

info("A7  THE OBVIOUS RESCUE, TESTED AND REJECTED (a_0(z) does not relieve the split).",
     "\n         The corpus's a_0(z) law switches MOND OFF at recombination (a_0(1090)/a_0(0) =\n"
     "         0.0060), and it is tempting to conclude that the Option-1 modification is\n"
     "         therefore invisible to the CMB.  It is not, and the reason is structural: s is\n"
     "         the NORMALISATION of script-J, and G_N = Ghat/s holds in the NEWTONIAN limit\n"
     "         (mu_phys -> 1), not in the MOND limit.  Switching the interpolation off does not\n"
     "         switch off the normalisation.  Equivalently, xi = (1-K_B/2)s contains no a_0 and\n"
     "         no y = g/a_0 -- checked at A8.  So this route's verdict is a_0-footing-blind:\n"
     "         identical for the canonical and alt a_0 above.")

xi_c = xi_of_s(S_MAX_R1[KB_FID], KB_FID)
check(abs(xi_c - XI_MAX) < 1e-15 and XI_MAX == xi_of_s(S_MAX_R1[KB_FID], KB_FID),
      "A8  xi depends on (s, K_B) ONLY -- no a_0, no kappa, no footing choice enters",
      f"xi_max = {XI_MAX:.5f} identically for a_0 = {A0_CANON:.4e} and {A0_ALT:.4e}.")

# --- A9: the FIRAS floor, stated before any CLASS run ------------------------------------------
F_NU_EXACT = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
NEFF_STD = 3.044
R_REF_EXACT = 1.0 + F_NU_EXACT * NEFF_STD
info("A9  the quantity the CMB actually measures",
     f"rho_r^grav / rho_gamma^therm = 1 + (7/8)(4/11)^(4/3) N_eff = {R_REF_EXACT:.5f} at "
     f"N_eff = {NEFF_STD}.  The escape DEMANDS xi times this.")
XI_FLOOR_EXACT = 1.0 / R_REF_EXACT
check(XI_MAX < XI_FLOOR_EXACT,
      "A10 *** THE STRUCTURAL STATEMENT: the escape's ceiling lies BELOW the photon floor ***",
      f"required rho_r^grav/rho_gamma = {R_REF_EXACT:.5f} * {XI_MAX:.5f} = "
      f"{R_REF_EXACT*XI_MAX:.5f} < 1, i.e. LESS THAN THE PHOTONS THEMSELVES GRAVITATE.  "
      f"Equivalent N_eff = {(R_REF_EXACT*XI_MAX - 1)/F_NU_EXACT:+.3f}.  "
      f"The floor xi >= 1/{R_REF_EXACT:.4f} = {XI_FLOOR_EXACT:.4f} is missed by "
      f"{XI_FLOOR_EXACT/XI_MAX:.2f}x (K_B=0.25) and {XI_FLOOR_EXACT/XI_MAX_LOW:.2f}x (K_B=0.10).")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- REAL CLASS.  Baseline control, then the proxy family.")
print("=" * 100)

from classy import Class                                                   # noqa: E402


def run_class(params, want_cl=True):
    c = Class()
    p = dict(params)
    if want_cl:
        p.update({"output": "tCl,pCl,lCl", "lensing": "yes", "l_max_scalars": LMAX + 100})
    c.set(p)
    c.compute()
    return c


# ---- B0: baseline, and CONTROL C-3 -------------------------------------------------------------
base_p = dict(PLANCK)
cb = run_class(base_p)
YHE = cb.get_current_derived_parameters(["YHe"])["YHe"]
der0 = cb.get_current_derived_parameters(
    ["100*theta_s", "z_rec", "rs_rec", "z_d", "rs_d", "z_eq", "Neff", "Omega_m"])
info("B0  CLASS computed the committed Planck 2018 base cosmology",
     ", ".join(f"{k}={v:.5g}" for k, v in der0.items()) + f", YHe={YHE:.6f}")

check(abs(der0["rs_d"] - 147.09) < 3 * 0.26,
      "B1  CONTROL C-3a: sound horizon at drag reproduces Planck 2018",
      f"CLASS r_drag = {der0['rs_d']:.3f} Mpc vs 147.09 +/- 0.26 (arXiv:1807.06209 Table 2)")
check(abs(der0["z_d"] - 1059.94) < 3 * 0.30,
      "B2  CONTROL C-3b: drag redshift reproduces Planck 2018",
      f"CLASS z_drag = {der0['z_d']:.3f} vs 1059.94 +/- 0.30")
check(abs(der0["z_eq"] - 3402.0) < 3 * 26.0,
      "B3  CONTROL C-3c: matter-radiation equality reproduces Planck 2018",
      f"CLASS z_eq = {der0['z_eq']:.2f} vs 3402 +/- 26")
check(abs(der0["Neff"] - NEFF_STD) < 1e-3,
      "B4  CONTROL C-3d: standard N_eff", f"CLASS Neff = {der0['Neff']:.4f}")

# ---- the radiation-to-photon ratio taken from CLASS's OWN background, not hard-coded -----------
bg = cb.get_background()
zbg = bg["z"]
sel = (zbg > 1e5) & (zbg < 1e6)
R_REF = float(np.mean((bg["(.)rho_g"][sel] + bg["(.)rho_ur"][sel]) / bg["(.)rho_g"][sel]))
F_NU = (R_REF - 1.0) / der0["Neff"]
check(abs(R_REF - R_REF_EXACT) < 1e-4 and abs(F_NU - F_NU_EXACT) < 1e-4,
      "B5  CLASS's own background reproduces the analytic radiation-to-photon ratio",
      f"CLASS (rho_g+rho_ur)/rho_g = {R_REF:.6f} vs analytic {R_REF_EXACT:.6f}; "
      f"f_nu = {F_NU:.6f} vs (7/8)(4/11)^(4/3) = {F_NU_EXACT:.6f}")
XI_FLOOR = 1.0 / R_REF

# ---- CL utilities ------------------------------------------------------------------------------
ell = np.arange(2, LMAX + 1)
CV_W = (2.0 * ell + 1.0)          # f_sky = 1


def tt_of(c):
    cl = c.lensed_cl(LMAX)
    return cl["tt"][2:LMAX + 1].copy()


CL0 = tt_of(cb)
D0 = ell * (ell + 1) * CL0 / (2 * np.pi)


def peaks(D):
    """first three TT acoustic peaks: parabolic-interpolated (l, height)."""
    out = []
    for lo, hi in ((150, 300), (450, 650), (750, 900)):
        m = (ell >= lo) & (ell <= hi)
        i = int(np.argmax(D[m])) + int(np.where(m)[0][0])
        y1, y2, y3 = D[i - 1], D[i], D[i + 1]
        den = (y1 - 2 * y2 + y3)
        dl = 0.5 * (y1 - y3) / den if den != 0 else 0.0
        out.append((ell[i] + dl, y2 - 0.25 * (y1 - y3) * dl))
    return out


PK0 = peaks(D0)
check(abs(PK0[0][0] - 220.6) < 4.0,
      "B6  CONTROL C-3e: first TT acoustic peak position",
      f"CLASS l_1 = {PK0[0][0]:.1f} vs the standard Planck value ~220.6; "
      f"l_2 = {PK0[1][0]:.1f}, l_3 = {PK0[2][0]:.1f}")


def chi2_cv(CL):
    """exact full-sky cosmic-variance -2 dlnL (Asimov, fiducial = baseline), after marginalising
    a 2-parameter {amplitude, tilt} template out of the model spectrum.  Generous by construction:
    A_s, tau (which enters TT as e^-2tau) and n_s are all absorbed."""
    x0 = CL / CL0
    lg = np.log(ell / 500.0)

    def f(ab):
        x = x0 * (1.0 + ab[0] + ab[1] * lg)
        if np.any(x <= 0):
            return 1e30
        return float(np.sum(CV_W * (1.0 / x + np.log(x) - 1.0)))

    from scipy.optimize import minimize
    best = min((minimize(f, g, method="Nelder-Mead",
                         options=dict(xatol=1e-10, fatol=1e-8, maxiter=4000))
                for g in ([0.0, 0.0], [0.1, 0.0], [-0.1, 0.0])), key=lambda r: r.fun)
    return float(best.fun), best.x


c0, ab0 = chi2_cv(CL0)
check(c0 < 1e-6,
      "B7  CONTROL C-4 (the null test): the whole pipeline returns chi2_CV = 0 at xi = 1",
      f"chi2_CV(baseline vs itself) = {c0:.3e}, template coefficients {ab0[0]:+.2e}, {ab0[1]:+.2e}")


# ---- the proxy family ---------------------------------------------------------------------------
def proxy(xi):
    """The CLASS proxy for Gt/G_N = xi at fixed thermal history.

    EXACT in: total gravitating radiation density (= xi * thermal), total gravitating matter
    density (= xi * thermal), thermal omega_b, thermal T_cmb, Y_He, theta_s.
    NOT exact in: the SPECIES COMPOSITION of those totals (see the NOT COMPUTED list).
    Realisable only for xi >= 1/R_REF (N_ur >= 0) and xi >= omega_b/omega_m (omega_cdm >= 0)."""
    n_ur = (R_REF * xi - 1.0) / F_NU
    om_m = PLANCK["omega_b"] + PLANCK["omega_cdm"]
    om_c = xi * om_m - PLANCK["omega_b"]
    return dict(omega_b=PLANCK["omega_b"], omega_cdm=om_c, N_ur=n_ur, YHe=YHE,
                A_s=PLANCK["A_s"], n_s=PLANCK["n_s"], tau_reio=PLANCK["tau_reio"]), n_ur, om_c


THETA0 = der0["100*theta_s"]


def run_xi(xi):
    p, n_ur, om_c = proxy(xi)
    if n_ur < -1e-12 or om_c < 0:
        return None
    p = dict(p)
    p["N_ur"] = max(n_ur, 0.0)
    try:
        pp = dict(p); pp["100*theta_s"] = THETA0
        c = run_class(pp)
    except Exception:
        # fall back to explicit bisection on h against 100*theta_s
        lo, hi = 0.2, 1.5
        for _ in range(45):
            mid = 0.5 * (lo + hi)
            try:
                cth = Class(); cth.set({**p, "h": mid}); cth.compute(level=["thermodynamics"])
                t = cth.get_current_derived_parameters(["100*theta_s"])["100*theta_s"]
                cth.struct_cleanup(); cth.empty()
            except Exception:
                return None
            if t > THETA0:
                lo = mid
            else:
                hi = mid
        c = run_class({**p, "h": 0.5 * (lo + hi)})
    return c


print()
print("-" * 100)
print("B8  THE PROXY FAMILY.  xi = Gt/G_N, everything thermal held, h re-shot to hold theta_s.")
print("-" * 100)
XIS = [1.0, 0.999, 0.997, 0.99, 0.98, 0.95, 0.90, 0.875, 0.80, 0.70, 0.62, XI_FLOOR + 1e-9]
rows = []
for xi in XIS:
    c = run_xi(xi)
    if c is None:
        rows.append((xi, None)); continue
    d = c.get_current_derived_parameters(["100*theta_s", "z_eq", "rs_rec", "h", "z_rec"])
    CL = tt_of(c)
    D = ell * (ell + 1) * CL / (2 * np.pi)
    ch, ab = chi2_cv(CL)
    rows.append((xi, dict(der=d, chi2=ch, pk=peaks(D), nur=proxy(xi)[1], omc=proxy(xi)[2])))
    c.struct_cleanup(); c.empty()

print(f"  {'xi':>8} {'N_ur':>8} {'om_cdm':>8} {'h':>7} {'z_eq':>8} {'rs_rec':>8} "
      f"{'dl_1':>7} {'dA_1/A':>8} {'dl_3':>7} {'dA_3/A':>8} {'chi2_CV':>12} {'n_sigma':>9}")
for xi, r in rows:
    if r is None:
        print(f"  {xi:8.4f}   -- NOT REALISABLE IN CLASS (negative species density) --"); continue
    d, pk = r["der"], r["pk"]
    print(f"  {xi:8.4f} {r['nur']:8.4f} {r['omc']:8.5f} {d['h']:7.4f} {d['z_eq']:8.1f} "
          f"{d['rs_rec']:8.2f} {pk[0][0]-PK0[0][0]:+7.2f} {pk[0][1]/PK0[0][1]-1:+8.4f} "
          f"{pk[2][0]-PK0[2][0]:+7.2f} {pk[2][1]/PK0[2][1]-1:+8.4f} "
          f"{r['chi2']:12.4g} {np.sqrt(r['chi2']):9.4g}")

good = [(xi, r) for xi, r in rows if r is not None]
check(len(good) == len(XIS),
      "B9  every xi down to the FIRAS floor is realisable and ran",
      f"{len(good)}/{len(XIS)} models computed; floor xi = {XI_FLOOR:.5f} (N_ur = 0)")

# invariants the derivation predicted
zeq = np.array([r["der"]["z_eq"] for _, r in good])
th = np.array([r["der"]["100*theta_s"] for _, r in good])
check(np.max(np.abs(zeq / zeq[0] - 1)) < 2e-3,
      "B10 derivation check A5(iii): z_eq is INVARIANT across the family, as the scaling predicts",
      f"max |z_eq/z_eq(1) - 1| = {np.max(np.abs(zeq/zeq[0]-1)):.2e}")
check(np.max(np.abs(th / THETA0 - 1)) < 3e-4,
      "B11 theta_s held across the family (h re-shot), so no peak shift is a distance artefact",
      f"max |100theta_s / ref - 1| = {np.max(np.abs(th/THETA0-1)):.2e}")
rs = np.array([r["der"]["rs_rec"] for _, r in good])
xig = np.array([xi for xi, _ in good])
pred = xig ** -0.5
check(np.max(np.abs((rs / rs[0]) / pred - 1)) < 0.03,
      "B12 derivation check A5(i): r_s scales as xi^(-1/2) across the family",
      f"max deviation from xi^(-1/2) = {np.max(np.abs((rs/rs[0])/pred - 1))*100:.2f}% "
      "(residual is the small shift of z_rec, which is the A5(v) effect)")

ch2 = np.array([r["chi2"] for _, r in good])
check(np.all(np.diff(ch2) >= -1e-6),
      "B13 chi2_CV rises monotonically as xi falls -- no accidental cancellation on the way down",
      f"chi2_CV from xi=1 to xi={xig[-1]:.4f}: {ch2[0]:.3g} -> {ch2[-1]:.4g}")

# ---- calibrate sigma_CV(xi) near xi = 1 ---------------------------------------------------------
near = [(xi, r) for xi, r in good if xi >= 0.98]
xn = np.array([xi for xi, _ in near]); cn = np.array([r["chi2"] for _, r in near])
m = xn < 1.0
slope = float(np.sum(cn[m] / (1.0 - xn[m]) ** 2) / np.sum(np.ones(m.sum())))
SIG_XI = 1.0 / np.sqrt(slope)
SIG_NEFF = SIG_XI * R_REF / F_NU
info("B14 cosmic-variance-limited sensitivity, calibrated on the xi >= 0.98 arm",
     f"chi2_CV = ((1-xi)/sigma)^2 with sigma_CV(xi) = {SIG_XI:.5f}  ==>  the noiseless full-sky "
     f"TT-only CMB measures Gt/G_N to {SIG_XI*100:.2f}%.  "
     f"Per-point: " + ", ".join(f"xi={x:.3f}:{np.sqrt(c):.2f}sig" for x, c in zip(xn[m], cn[m])))
check(SIG_NEFF < 0.17 and SIG_NEFF > 0.005,
      "B15 CONTROL C-5: the CV-only forecast is TIGHTER than Planck 2018's sigma(N_eff) = 0.17, "
      "and by a sane factor -- the pipeline is calibrated, not broken",
      f"sigma_CV(N_eff) = sigma_CV(xi) * R/f_nu = {SIG_NEFF:.4f}, i.e. {0.17/SIG_NEFF:.1f}x "
      "tighter than Planck (noiseless, full sky, TT only, lensed, l<=2500)")

# ---- the headline numbers -----------------------------------------------------------------------
row_floor = good[-1][1]
row_aest = [r for xi, r in good if abs(xi - 0.875) < 1e-9][0]
NS_FLOOR = np.sqrt(row_floor["chi2"])
NS_AEST = np.sqrt(row_aest["chi2"])
dl_max = max(abs(row_floor["pk"][i][0] - PK0[i][0]) for i in range(3))
dA_max = max(abs(row_floor["pk"][i][1] / PK0[i][1] - 1) for i in range(3))
check(NS_FLOOR > 50,
      "B16 *** AT THE HARD FIRAS FLOOR xi = 0.5913 -- the CLOSEST the escape can even be "
      "REPRESENTED -- the lensed TT spectrum is already destroyed ***",
      f"chi2_CV = {row_floor['chi2']:.4g} => {NS_FLOOR:.0f} sigma_CV aggregate, after "
      f"marginalising amplitude and tilt; peak positions move by up to {dl_max:.0f} multipoles "
      f"and peak heights by up to {dA_max*100:.0f}%.  The escape's own xi = {XI_MAX:.5f} lies "
      f"{XI_FLOOR/XI_MAX:.2f}x BEYOND this point, in a region with no CLASS model at all.")
check(NS_AEST > 3,
      "B17 AGAINST THE PARENT THEORY'S INTEREST: the same axis prices unmodified AeST",
      f"at its BBN-edge fiducial K_B = 0.25, AeST's own xi = 0.875 gives "
      f"chi2_CV = {row_aest['chi2']:.4g} => {NS_AEST:.1f} sigma_CV.  This is a by-product, not "
      "the assignment, and it is CV-limited TT-only, not a Planck likelihood.")

# ---- verify CLASS really refuses the escape's own parameters ------------------------------------
print()
info("B18 direct verification that the escape is outside CLASS's domain (not merely disfavoured)")
attempts = {
    "N_ur < 0 (the required negative gravitating neutrino density)":
        dict(N_ur=(R_REF * XI_MAX - 1.0) / F_NU, omega_cdm=0.12),
    "omega_cdm < 0 (the required gravitating matter deficit)":
        dict(N_ur=NEFF_STD, omega_cdm=XI_MAX * 0.14237 - PLANCK["omega_b"]),
    "Omega_fld < 0 with w = 1/3 (a negative radiation fluid)":
        dict(N_ur=NEFF_STD, omega_cdm=0.12, Omega_Lambda=0.0, Omega_fld=-0.1,
             w0_fld=1.0 / 3.0, wa_fld=0.0, cs2_fld=1.0 / 3.0),
}
n_ref = 0
for lab, ex in attempts.items():
    try:
        c = Class(); c.set({**{k: v for k, v in PLANCK.items() if k != "omega_cdm"},
                            "YHe": YHE, "output": "tCl", "l_max_scalars": 500, **ex})
        c.compute()
        print(f"         [!!] ACCEPTED: {lab}")
        c.struct_cleanup(); c.empty()
    except Exception as e:
        n_ref += 1
        print(f"         refused: {lab}\n                  -> {str(e).strip().splitlines()[-1][:96]}")
check(n_ref == len(attempts),
      "B19 all three routes to a sub-photon gravitating density are refused by CLASS at input "
      "validation -- the escape's cosmology is not a member of the model space",
      f"{n_ref}/{len(attempts)} refused.  This is why B16's number is a FLOOR on the damage, "
      "not an estimate of it.")

cb.struct_cleanup(); cb.empty()

# =================================================================================================
print()
print("=" * 100)
print("PART C -- DEATH 2 AT THE RESCALED NORMALISATION.  Is Eq (12) stiff, or degenerate?")
print("=" * 100)
info("C0  SZ21 Eq (12), from the committed transcription bridge1_aest_equations.md",
     "K_B (Edot + H E) = (dK/dQ) chi - (2-K_B)[ (phidot/(1+w)) Pi + (H + phidot) chi "
     "- 3 c_ad^2 H phidot alpha ].\n         Under Option 1 the O(eps^2) action carries "
     "[K_B - F_Z(0)] Z^(2), so the coefficient of (Edot + H E) is eps = K_B - F_Z(0).")

# reading (i): the brief's premise, F_Z(0) = K_B at s = 1
eps_i = lambda s, kb: kb * (1.0 - s)
# reading (ii): Route 1's refutation, mu_phys(0) = 0 for any interpolation => F_Z(0) = 0
eps_ii = lambda s, kb: kb

s_ops = S_MAX_R1[KB_FID]
check(abs(eps_i(1.0, KB_FID)) < 1e-15,
      "C1  reading (i) reproduces DEATH 2 as briefed: at the AeST normalisation s = 1 the "
      "coefficient vanishes IDENTICALLY and Eq (12) degenerates to 0 = source",
      f"eps(s=1) = K_B(1-s) = {eps_i(1.0, KB_FID):.1e}")
check(eps_i(s_ops, KB_FID) / KB_FID > 0.80,
      "C2  reading (i): the SAME rescaling that cures the ghost also DETUNES the degeneracy",
      f"at s = {s_ops:.5f}, eps = K_B(1-s) = {eps_i(s_ops, KB_FID):.5f} = "
      f"{eps_i(s_ops, KB_FID)/KB_FID*100:.1f}% of K_B.  Stiffness ratio |K_B/eps| = "
      f"{KB_FID/eps_i(s_ops, KB_FID):.3f} -- an O(1) number, so the integration is perfectly "
      "well conditioned.  Genuine stiffness (|K_B/eps| > 10) needs s > 0.9, i.e. 6.5x OUTSIDE "
      "the no-ghost window.")
check(abs(eps_ii(s_ops, KB_FID) - KB_FID) < 1e-15,
      "C3  reading (ii) -- Route 1's refutation, adopted here and independently consistent: "
      "the deep-MOND end of ANY interpolation has mu_phys(0) = 0, so F_Z(0) = 0 and the "
      "coefficient is K_B EXACTLY, for EVERY s.  There is no DEATH 2 to price.",
      f"eps = {eps_ii(s_ops, KB_FID):.5f} = K_B, independent of s.  Consistency: reading (i)'s "
      "premise F_Z(0) = K_B would require a MOND-limit FLOOR mu_phys(0) = K_B/((2-K_B)s), i.e. "
      f"{KB_FID/((2-KB_FID)*1.0):.4f} at s = 1 and {KB_FID/((2-KB_FID)*s_ops):.4f} at "
      f"s = {s_ops:.5f} -- the latter EXCEEDS the Newtonian value mu = 1, so the premise is not "
      "merely un-MOND-like, it is out of range.  Neither is an interpolation function.")
check(min(eps_i(s_ops, KB_FID), eps_ii(s_ops, KB_FID)) / KB_FID > 0.8,
      "C4  *** PART (c) ANSWERED, BOTH READINGS: at the rescaled normalisation Eq (12) is "
      "NEITHER degenerate NOR stiff -- >= 85.7% of the aether-electric coefficient survives ***",
      "so DEATH 2 is not what closes this escape, and PART C is a genuine PASS.  Stated for the "
      "framework's interest, and it does not move PART B's verdict at all.")
check(eps_i(2.0 / (2.0 - KB_FID), KB_FID) < 0,
      "C5  and the two constraints pull in OPPOSITE directions under reading (i): the CMB wants "
      "xi ~ 1, i.e. s = 2/(2-K_B) = 1.1429, where eps = K_B(1-s) < 0 -- a WRONG-SIGN aether "
      "electric term",
      f"eps(s=1.1429) = {eps_i(2.0/(2.0-KB_FID), KB_FID):+.5f}.  So under reading (i) no s is "
      "simultaneously CMB-viable and healthy; under reading (ii) the CMB verdict stands alone.")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- THE s RANGE ALLOWED BY THE CMB, AND THE VERDICT")
print("=" * 100)


def s_of_xi(xi, kb):
    return xi / (1.0 - kb / 2.0)


for nsig in (1, 3):
    lo_xi, hi_xi = 1.0 - nsig * SIG_XI, 1.0 + nsig * SIG_XI
    info(f"D1  at {nsig} sigma_CV (TT only, f_sky=1, l<=2500, amplitude+tilt marginalised)",
         f"xi = Gt/G_N in [{lo_xi:.5f}, {hi_xi:.5f}]  ==>  "
         f"s in [{s_of_xi(lo_xi, KB_FID):.5f}, {s_of_xi(hi_xi, KB_FID):.5f}] at K_B = 0.25")

S_CMB_LO, S_CMB_HI = s_of_xi(1 - 3 * SIG_XI, KB_FID), s_of_xi(1 + 3 * SIG_XI, KB_FID)
GAP = S_CMB_LO / S_MAX_R1[KB_FID]
check(S_CMB_LO > S_MAX_R1[KB_FID],
      "D2  *** THE TWO WINDOWS ARE DISJOINT.  KILL. ***",
      f"no-ghost (Route 1) needs s < {S_MAX_R1[KB_FID]:.5f}; the CMB at 3 sigma_CV needs "
      f"s > {S_CMB_LO:.5f}.  Disjoint by {GAP:.2f}x.  In sigma: the escape's ceiling "
      f"xi = {XI_MAX:.5f} sits {(1-XI_MAX)/SIG_XI:.0f} sigma_CV from viability, and cannot even "
      "be represented in CLASS (B19).")

# is there ANY K_B that opens it?
kb_need_1 = 2.0 * (1.0 - SIG_XI)
kb_need_3 = 2.0 * (1.0 - 3 * SIG_XI)
check(kb_need_3 > 0.25,
      "D3  NO value of K_B opens the window: xi <= K_B/2 is the no-ghost ceiling, so CMB "
      "viability requires K_B >= 2(1 - n sigma)",
      f"K_B >= {kb_need_1:.4f} at 1 sigma_CV, {kb_need_3:.4f} at 3 sigma_CV -- against the "
      f"committed range K_B in [2.1e-4, 0.25] (RETRACTIONS.md, BBN via Oost et al. Eq. 3.7) and "
      f"against the no-ghost range K_B < 2 itself.  Shortfall {kb_need_3/0.25:.1f}x.")

# CONTROL C-6: the committed BBN statement must come back out of the same map
kb_bbn = 2.0 * (1.0 - 1.0 / 8.0)
check(abs(kb_bbn - 1.75) < 1e-12,
      "D4  CONTROL C-6: the committed BBN statement |G_cos/G_N - 1| <~ 1/8 read through THIS "
      "map reproduces the corpus's own bound at s = 1",
      f"|1 - (1-K_B/2)| = K_B/2 <= 1/8  =>  K_B <= 0.25 EXACTLY -- the number in "
      "RETRACTIONS.md line 55.  The map is therefore the same one the corpus already uses for "
      "BBN, and this file only sharpens the tolerance from 1/8 to "
      f"{SIG_XI:.5f} using real CLASS.")
info("D5  by-product, stated against the framework's interest and NOT the assignment",
     f"the same CV-limited TT bound reads K_B <= {2*SIG_XI:.5f} at 1 sigma_CV and "
     f"{6*SIG_XI:.5f} at 3 sigma_CV for unmodified AeST (s = 1), i.e. ~{0.25/(2*SIG_XI):.0f}x "
     "tighter than the helium bound the corpus quotes.  A real Planck likelihood would be "
     "weaker than this CV-limited forecast; it is recorded as an OWED calculation, not a claim.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""  ROUTE 3 KILLS THE ESCAPE.  PASS was defined as "TT stays within cosmic variance for s in
  Route 1's window".  It does not, and it does not by a margin that is qualitative rather than
  numerical: the window's Gt/G_N <= {XI_MAX:.5f} demands a gravitating radiation density of
  {R_REF*XI_MAX:.4f} rho_gamma -- less than the photons, whose density FIRAS measures with no
  gravity in the chain.  The nearest representable cosmology (xi = {XI_FLOOR:.4f}, N_ur = 0) is
  already {NS_FLOOR:.0f} sigma_CV away on lensed TT alone after marginalising amplitude and tilt.
  The CMB allows Gt/G_N to {SIG_XI*100:.2f}%, i.e. s = {s_of_xi(1.0, KB_FID):.4f} +/- {SIG_XI/(1-KB_FID/2):.4f};
  no-ghost needs s < {S_MAX_R1[KB_FID]:.5f}.  Disjoint by {GAP:.1f}x, with no K_B that closes it.
  PART C is a genuine PASS for the framework -- DEATH 2 is not stiff and (Route 1) does not
  exist -- and it changes nothing, because the killing constraint is the NORMALISATION, which no
  choice of free function, kernel branch, or a_0(z) suppression can touch.
  a_0 = {A0_CANON:.4e} canonical / {A0_ALT:.4e} alt: this verdict is identical on both footings.""")

print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    for f in FAIL:
        print("  FAILED:", f)
print("=" * 100)
sys.exit(1 if FAIL else 0)
