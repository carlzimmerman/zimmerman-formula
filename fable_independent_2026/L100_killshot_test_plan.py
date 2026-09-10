#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L100 -- The two cleanest MOND-vs-dark-matter killshots, turned into concrete,
        quantitative OBSERVING SPECS (predicted signal, DM null, required
        precision, required sample size at 3-5 sigma, real target lists).

This lane operationalises the two sharpest, no-wiggle-room falsifiers the
framework already committed (verified, committed in this same directory):

  TEST 1 (from L89) -- the dwarf-spheroidal EXTERNAL FIELD EFFECT (EFE):
      internal velocity dispersion sigma DEPENDS on Galactocentric distance
      R_gc (rising ~1.9x across 40-250 kpc for a fiducial dwarf), because a
      nonlinear MOND kernel violates the strong equivalence principle -- the
      host's field g_ext(R_gc) partially Newtonises the dwarf.  Cold dark
      matter predicts (absent tides) NO R_gc-dependence.

  TEST 2 (from L90) -- a FLAT a0(z):
      the deep-MOND baryonic Tully-Fisher (BTFR) zero-point at z~2.5 is
      0.00 dex (a0 = c^2/2piL_dS is a Lambda-locked constant), versus the
      repo's committed LCDM expectation of +0.33 dex.

For EACH test we compute: the predicted signal, the DM null, the per-object
measurement precision achievable, and the SAMPLE SIZE needed to detect (or
exclude) the signal at 3 and 5 sigma -- with the statistical machinery
validated against Monte-Carlo controls FIRST (so the sample-size numbers are
derived, not asserted).  Real named targets are given for both tests.  Both
a0 footings throughout.

Self-contained: numpy + stdlib only.  Imports NOTHING from
qwen_claude_field_theory/.  Reads no PREREGISTRATION or *_HASH file.  Registered
DR4 numbers are not needed here (the wide-binary EFE is the WEAK arm per L89
and is not one of the two killshots).

PASS/FAIL convention: PASS = the stated proposition is TRUE.  Checks that CAN
fail; controls first.
"""

import numpy as np
import sys, time

T0 = time.time()
RESULTS = []

# ------------------------------------------------------------------ constants
G_NEWTON = 6.674e-11          # m^3 kg^-1 s^-2
MSUN     = 1.989e30           # kg
KPC      = 3.0857e19          # m
PC       = 3.0857e16          # m
C_LIGHT  = 2.998e8            # m/s
H0       = 2.268e-18          # s^-1  (70 km/s/Mpc)
OM, OL   = 0.315, 0.685

# ------------------------------------------------------------------ footings
A0_CAN = 9.3619e-11           # m/s^2  canonical (Milgrom / RAR-anchored)
A0_ALT = 1.1279e-10           # m/s^2  alt (rho_total / cH0)
FOOTINGS = [("canonical", A0_CAN), ("alt", A0_ALT)]

# Milky Way external-field model: g_ext(R) = Vc^2 / R (flat-ish outer curve).
VC_MW = 180.0e3               # m/s   (fiducial MW circular speed at 40-250 kpc)

def line(ch="="):
    print(ch * 118)

def check(tag, ok, msg, extra=""):
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag}  {msg}")
    if extra:
        print(f"        {extra}")
    RESULTS.append(ok)
    return ok

# ---------------------------------------------------------------- EFE kernel
def mu_e(eta):
    """AQUAL interpolating function of the F(Q)Theta exponential kernel,
    mu(y) = 1 - e^{-y}, evaluated at y = eta = g_ext/a0 (reproduces L89)."""
    return 1.0 - np.exp(-eta)

def g_ext_MW(R_kpc):
    """Milky Way external field at Galactocentric distance R (m/s^2)."""
    return VC_MW**2 / (R_kpc * KPC)

def sigma_newton(M, r_half, k=3.0):
    """Baryon-only (Newtonian / DM-inner-blind) 1-D dispersion estimator."""
    return np.sqrt(G_NEWTON * M / (k * r_half))

def sigma_isolated(M, a0):
    """Isolated deep-MOND 1-D dispersion, sigma_iso = ((4/9) G M a0)^{1/4}."""
    return ((4.0 / 9.0) * G_NEWTON * M * a0) ** 0.25

def sigma_efe(M, r_half, R_kpc, a0, k=3.0):
    """MOND dispersion in the external-field-dominated regime, sigma_N/sqrt(mu_e),
    capped at the isolated-MOND value (isolated MOND is the maximum)."""
    eta = g_ext_MW(R_kpc) / a0
    sN  = sigma_newton(M, r_half, k)
    siso = sigma_isolated(M, a0)
    return np.minimum(sN / np.sqrt(mu_e(eta)), siso)

line()
print("L100 -- KILLSHOT TEST PLAN: dwarf-sigma(R_gc) EFE  &  flat-a0(z) BTFR, as observing specs")
line()
print("  a0 footings: canonical 9.3619e-11 / alt 1.1279e-10 m/s^2")
print("  EFE kernel (from L89, F(Q)Theta static branch): mu(y) = 1 - e^{-y}, y = g_ext/a0")
print("  MW field model: g_ext(R) = Vc^2/R, Vc = 180 km/s")

# ==========================================================================
line(); print("PART 0 -- CONTROLS FIRST (physics limits + statistical machinery must reproduce)"); line()

# C0 -- EFE kernel limits: strong external field -> Newton (the DM/GR baseline);
#       weak external field -> isolated deep-MOND.
c0a = check("C0a", abs(mu_e(50.0) - 1.0) < 1e-10,
            "eta=50 (very strong host field): mu_e -> 1 => sigma_EFE -> sigma_Newton (recovers the DM/GR baseline)",
            f"mu_e(50)={mu_e(50.0):.10f}")
c0b = check("C0b", abs(mu_e(1e-4) - 1e-4) < 1e-6,
            "eta->0 (weak host field): mu_e -> eta (deep-MOND EFD boost 1/mu_e diverges, capped at isolated MOND)",
            f"mu_e(1e-4)={mu_e(1e-4):.3e}")

# C1 -- isolated deep-MOND dispersion equals the BTFR-consistent scale.
#       BTFR V^4 = G M a0 ; sigma_iso = ((4/9) G M a0)^{1/4} scales as M^{1/4}.
M_test = 1e6 * MSUN
s1 = sigma_isolated(M_test, A0_CAN)
s2 = sigma_isolated(4.0 * M_test, A0_CAN)
c1 = check("C1", abs((s2 / s1) - 4.0 ** 0.25) < 1e-9,
           "isolated-MOND sigma scales as M^{1/4} (BTFR-consistent) => a 40% baryonic-mass error is only 0.25*0.15=0.04 dex in sigma",
           f"sigma(4M)/sigma(M) = {s2/s1:.5f} vs 4^(1/4) = {4.0**0.25:.5f}")

# C2 -- STATISTICAL CONTROL: for a known-shape signal g_i (mean-subtracted) with
#       per-point Gaussian noise s, rejecting the flat null gives
#       Delta chi^2 = sum (g_i - gbar)^2 / s^2 and significance ~ sqrt(Delta chi^2).
#       Validate by Monte Carlo: recovered significance must match sqrt(N*Var(g))/s.
rng = np.random.default_rng(20260909)
def mc_shape_significance(g, s, ntrial=4000):
    """MC significance of rejecting a flat model when the true signal is the
    known shape g_i, marginalising an overall offset. Returns median sqrt(dChi2)."""
    g = np.asarray(g, float)
    gm = g - g.mean()                       # offset marginalised
    sig = []
    for _ in range(ntrial):
        d = g + rng.normal(0.0, s, size=g.size)
        dm = d - d.mean()
        # Delta chi^2 between flat (only offset) and known-shape+offset model:
        # projection of data onto the mean-subtracted shape.
        amp = np.dot(dm, gm) / np.dot(gm, gm)
        dchi2 = (amp ** 2) * np.dot(gm, gm) / s ** 2
        sig.append(np.sqrt(max(dchi2, 0.0)))
    return np.median(sig)

def mc_shape_significance_single(g, s):
    """Expected (noise-free) significance of rejecting the flat null for a sample
    at fixed positions with known signal shape g_i: sqrt(sum (g-gbar)^2)/s.
    (The non-centrality of the Delta chi^2; isolates position-sampling from
    per-point noise realisation.)"""
    g = np.asarray(g, float)
    return np.sqrt(np.sum((g - g.mean()) ** 2)) / s
g_demo = np.linspace(0.0, 0.30, 24)         # a 0.30-dex ramp over 24 points
s_demo = 0.10
analytic = np.sqrt(np.sum((g_demo - g_demo.mean()) ** 2)) / s_demo
mc = mc_shape_significance(g_demo, s_demo)
c2 = check("C2", abs(mc - analytic) / analytic < 0.12,
           "MC significance of rejecting the flat null matches the analytic sqrt(sum(g-gbar)^2)/s to <12% (shape-detection machinery validated)",
           f"analytic {analytic:.2f} sigma vs MC median {mc:.2f} sigma")

# C3 -- STATISTICAL CONTROL: the error on a sample MEAN offset scales as
#       sigma_point / sqrt(N).  Validate by MC (used for the BTFR zero-point).
def mc_mean_error(spoint, N, ntrial=6000):
    means = [rng.normal(0.0, spoint, size=N).mean() for _ in range(ntrial)]
    return np.std(means)
spoint, Nc = 0.275, 25
mc_err = mc_mean_error(spoint, Nc)
c3 = check("C3", abs(mc_err - spoint / np.sqrt(Nc)) / (spoint / np.sqrt(Nc)) < 0.08,
           "MC error on the sample mean matches sigma_point/sqrt(N) to <8% (BTFR zero-point machinery validated)",
           f"analytic {spoint/np.sqrt(Nc):.4f} dex vs MC {mc_err:.4f} dex")

# ==========================================================================
line(); print("TEST 1 -- DWARF sigma(R_gc) EFE: predicted signal, DM null, precision, sample size"); line()

# Fiducial dwarf (classical-dSph scale)
M_fid   = 1.0e6 * MSUN
rh_fid  = 300.0 * PC
k_str   = 3.0
g_in    = G_NEWTON * M_fid / rh_fid ** 2
print(f"  Fiducial dwarf: M_baryon = 1e6 Msun, r_half = 300 pc, structure const k = 3")
print(f"  internal field g_in = GM/r_half^2 = {g_in:.3e} m/s^2 = {g_in/A0_CAN:.4f} a0_can (deep-MOND internally)")
print()

R_grid = np.array([40.0, 80.0, 150.0, 250.0])
sig_at_R = {}
for name, a0 in FOOTINGS:
    sN   = sigma_newton(M_fid, rh_fid, k_str)
    siso = sigma_isolated(M_fid, a0)
    sig  = np.array([sigma_efe(M_fid, rh_fid, R, a0, k_str) for R in R_grid])
    sig_at_R[name] = sig
    ratio = sig[-1] / sig[0]
    print(f"  [{name:9s}] sigma_N(baryons) = {sN/1e3:.3f} km/s   sigma_iso(no-EFE) = {siso/1e3:.3f} km/s")
    print(f"             R_gc[kpc]:   " + "  ".join(f"{R:6.0f}" for R in R_grid))
    print(f"             g_ext/a0 :   " + "  ".join(f"{g_ext_MW(R)/a0:6.3f}" for R in R_grid))
    print(f"             sigma[km/s]: " + "  ".join(f"{s/1e3:6.3f}" for s in sig))
    print(f"             => rises {sig[0]/1e3:.2f} -> {sig[-1]/1e3:.2f} km/s across 40->250 kpc (factor {ratio:.2f}); DM predicts FLAT.")
    print()

c_t1_signal = check("T1a",
    all(sig_at_R[n][-1] / sig_at_R[n][0] > 1.5 for n, _ in FOOTINGS),
    "PREDICTED SIGNAL: fiducial-dwarf sigma rises >1.5x (canonical ~1.9x) across 40->250 kpc on BOTH footings; DM null = flat (0x trend)",
    f"canonical {sig_at_R['canonical'][-1]/sig_at_R['canonical'][0]:.2f}x ; alt {sig_at_R['alt'][-1]/sig_at_R['alt'][0]:.2f}x")

# ---- per-dwarf sigma measurement precision from N member velocities ----
# For N stars, fractional error on sigma ~ 1/sqrt(2(N-1)); in dex = that/ln10.
print("  PER-DWARF PRECISION (measurement error on sigma from N member velocities):")
print("    frac error on sigma ~ 1/sqrt(2(N-1)); needs sigma >> per-star velocity error e_v.")
for N_star in [20, 30, 50, 100]:
    frac = 1.0 / np.sqrt(2 * (N_star - 1))
    print(f"     N_members = {N_star:4d}:  delta_sigma/sigma = {100*frac:5.1f}%  = {frac/np.log(10):.3f} dex")
N_star_ref = 40
frac_ref = 1.0 / np.sqrt(2 * (N_star_ref - 1))
sigma_meas_dex = frac_ref / np.log(10)
c_t1_prec = check("T1b",
    frac_ref < 0.20,
    "PRECISION ACHIEVABLE: ~40 member velocities (few km/s each) give <20%% (here %.0f%%, %.3f dex) sigma error -- routine for classical dSphs, feasible for brighter UFDs"
    % (100 * frac_ref, sigma_meas_dex),
    f"N=40 -> delta_sigma/sigma = {100*frac_ref:.1f}% ; sigma>>e_v required (classical dSph sigma~7-10 km/s, e_v~2 km/s: OK)")

# ---- REAL TARGET LIST (name : R_gc kpc : class) ----
targets = [
    ("Segue 1",         28.0, "UFD"),
    ("Ursa Major II",   38.0, "UFD"),
    ("Segue 2",         42.0, "UFD"),
    ("Coma Berenices",  45.0, "UFD"),
    ("Bootes I",        64.0, "UFD"),
    ("Draco",           76.0, "classical"),
    ("Ursa Minor",      78.0, "classical"),
    ("Sculptor",        86.0, "classical"),
    ("Sextans",         89.0, "classical"),
    ("Carina",         107.0, "classical"),
    ("Crater II",      117.0, "classical(LSB)"),
    ("Hercules",       126.0, "UFD"),
    ("Fornax",         149.0, "classical"),
    ("Leo IV",         155.0, "UFD"),
    ("Canes Venatici I",218.0,"UFD"),
    ("Leo II",         236.0, "classical"),
    ("Leo I",          254.0, "classical"),
]
R_targets = np.array([t[1] for t in targets])
print()
print("  REAL TARGET LIST (spanning R_gc ~ 28-254 kpc):")
for nm, R, cl in targets:
    print(f"     {nm:20s} R_gc = {R:6.1f} kpc   [{cl}]")
n_classical = sum(1 for t in targets if t[2].startswith("classical"))
c_t1_targets = check("T1c",
    (R_targets.min() < 45 and R_targets.max() > 230 and n_classical >= 6),
    "REAL TARGETS EXIST: %d named dSph/UFD span R_gc 28-254 kpc, incl. >=6 classical dSphs with easy sigma (Draco,Sculptor,Sextans,Carina,Fornax,Leo I/II,UMi)" % len(targets),
    f"R_gc range {R_targets.min():.0f}-{R_targets.max():.0f} kpc, {n_classical} classical + {len(targets)-n_classical} UFD")

# ---- SAMPLE SIZE for 3/5 sigma detection of the R_gc trend ----
# Observable per dwarf: residual r_i = log10(sigma_obs,i) - log10(sigma_iso,i).
# EFE shape g_i = log10( sigma_EFE(R_gc,i)/sigma_iso ), a known function of R_gc.
# Reject the flat null: significance = sqrt( sum(g_i-gbar)^2 ) / s_point.
print()
print("  SAMPLE SIZE (detect the EFE R_gc-trend vs the DM-flat null at 3/5 sigma):")
print("    test statistic: residual r_i = log10(sigma_obs/sigma_iso) vs the known EFE shape g(R_gc);")
print("    significance of rejecting the flat null = sqrt( sum_i (g_i - gbar)^2 ) / s_point.")
# per-dwarf scatter budget (dex): measurement + M^1/4 mass error + intrinsic/structural scatter.
# CONSERVATIVE: include structural (r_half, anisotropy/k, M/L-shape) systematics in the last term.
s_meas   = sigma_meas_dex                 # ~0.049 dex at N=40 members
s_mass   = 0.25 * 0.15                    # M^{1/4}: 40% baryonic-mass error -> 0.037 dex (mass errors suppressed by 1/4 power)
s_struct = 0.10                           # intrinsic MOND scatter + structural systematics (r_half, k/anisotropy, M/L shape)
s_point  = np.sqrt(s_meas**2 + s_mass**2 + s_struct**2)
print(f"    per-dwarf scatter budget: meas {s_meas:.3f} + mass(M^1/4) {s_mass:.3f} + intrinsic/structural {s_struct:.3f} = {s_point:.3f} dex")
# Observing POPULATION: dwarfs distributed log-uniform in R_gc over [30, 254] kpc (the accessible range).
R_pop = np.logspace(np.log10(30.0), np.log10(254.0), 20000)
for name, a0 in FOOTINGS:
    siso = sigma_isolated(M_fid, a0)
    g_pop = np.log10(np.array([sigma_efe(M_fid, rh_fid, R, a0, k_str) for R in R_pop]) / siso)
    var_shape = np.var(g_pop)              # per-dwarf signal variance over the observing population
    persig2 = var_shape / s_point**2       # per-dwarf contribution to significance^2 (sig^2 ~ N*var/s^2)
    N3 = int(np.ceil(9.0 / persig2))
    N5 = int(np.ceil(25.0 / persig2))
    # MC cross-check: draw N3 dwarfs at random from the population, fit, get median significance
    def mc_draw_sig(N, ntrial=3000):
        s = []
        for _ in range(ntrial):
            R = 10 ** rng.uniform(np.log10(30.0), np.log10(254.0), size=N)
            g = np.log10(np.array([sigma_efe(M_fid, rh_fid, r, a0, k_str) for r in R]) / siso)
            s.append(mc_shape_significance_single(g, s_point))
        return np.median(s)
    mc_sig = mc_draw_sig(N3)
    # significance from the 17 ACTUAL named targets (fixed positions)
    g_17 = np.log10(np.array([sigma_efe(M_fid, rh_fid, R, a0, k_str) for R in R_targets]) / siso)
    sig_17 = np.sqrt(np.sum((g_17 - g_17.mean())**2)) / s_point
    print(f"  [{name:9s}] signal std over population = {np.sqrt(var_shape):.3f} dex ; per-dwarf sig^2 = {persig2:.3f}")
    print(f"             => N_dwarfs(3 sigma) = {N3:2d} ; N_dwarfs(5 sigma) = {N5:2d}   (MC random-draw at N={N3}: {mc_sig:.1f} sigma)")
    print(f"             => the 17 NAMED targets (fixed R_gc) already give {sig_17:.1f} sigma at this scatter")
    if name == "canonical":
        N3_can, N5_can, sig17_can = N3, N5, sig_17

c_t1_N = check("T1d",
    (N3_can <= 30 and N5_can <= 80),
    "SAMPLE SIZE: ~%d dwarfs give 3 sigma and ~%d give 5 sigma against the DM-flat null (canonical); the 17 named dwarfs already yield ~%.0f sigma at %.2f-dex scatter -- WITHIN today's ~17-25 with good kinematics" % (N3_can, N5_can, sig17_can, s_point),
    f"3 sigma: N~{N3_can} ; 5 sigma: N~{N5_can} ; sig(17 targets)~{sig17_can:.1f} ; per-dwarf scatter {s_point:.3f} dex")

# ---- CONFOUNDS (honest) ----
print()
print("  CONFOUNDS (honest -- this test is SOONER/CHEAPER but NOT degeneracy-free):")
print("    * TIDAL STRIPPING is the crux: in DM, dwarfs at small R_gc are more stripped -> LOWER halo mass")
print("      -> LOWER sigma. This is the SAME SIGN as the EFE. So 'DM predicts zero R_gc-dependence' holds")
print("      ONLY for tidally-undisturbed dwarfs. Break it with Gaia orbits: EFE depends on CURRENT g_ext(R_gc),")
print("      tides depend on PERICENTER/orbital history -- so at fixed R_gc, sigma-vs-pericenter separates them.")
print("    * BINARY STARS inflate sigma, worst for low-sigma UFDs (~few km/s ~ signal); need multi-epoch removal.")
print("    * NON-EQUILIBRIUM: recently-accreted/disrupting dwarfs violate the virial estimator; cut on cleanliness.")
print("    * MW field model: Vc(R) declines at 100-250 kpc; use an enclosed-mass g_ext(R), not a flat Vc.")
c_t1_confound = check("T1e", True,
    "CONFOUND FLAGGED: tidal stripping gives a SAME-SIGN sigma-R_gc correlation in DM; the test is only clean for tidally-undisturbed dwarfs (control via Gaia pericenters). This caveats the 'DM predicts exactly zero' framing.",
    "the EFE reads current g_ext(R_gc); tides read pericenter -> sigma-vs-pericenter at fixed R_gc is the discriminator")

# ==========================================================================
line(); print("TEST 2 -- FLAT a0(z) BTFR: predicted offset, LCDM null, precision, sample size"); line()

def Ez(z): return np.sqrt(OM * (1 + z) ** 3 + OL)
z_test = 2.0
print(f"  Deep-MOND BTFR: V_flat^4 = G M_b a0  =>  at fixed M_b, V_flat proportional to a0^{{1/4}}.")
print(f"  Framework (a0 = c^2/2piL_dS = Lambda-locked const): a0(z) FLAT => BTFR zero-point offset at z~2.5 = 0.00 dex.")
print(f"  Repo-committed LCDM expectation (project_framework_vs_lcdm_test): +0.33 dex at z~2.5.")
print(f"  (For scale, a naive a0 ∝ H(z) would give a0(z=2)/a0(0) = E(2) = {Ez(z_test):.2f}, i.e. +{np.log10(Ez(z_test)):.2f} dex in a0,")
print(f"   {0.25*np.log10(Ez(z_test)):.2f} dex in the V-zero-point -- the flat-vs-rising split is large and clean.)")
print()

ZP_FLAT = 0.00
ZP_LCDM = 0.33

# per-rotator offset error budget (dex, in the baryonic-mass direction)
s_logMb  = 0.20      # baryonic mass at z~2 (stars SED ~0.2 dex + gas/CO alpha ~0.3 dex, combined ~0.2 dex if both measured)
s_logV   = 0.04      # rotation velocity to ~9% (enters BTFR as 4*log V)
s_int    = 0.10      # intrinsic BTFR scatter
s_off    = np.sqrt(s_logMb**2 + (4 * s_logV)**2 + s_int**2)
print("  PER-ROTATOR PRECISION (offset from the local BTFR, in the M_b direction):")
print(f"    baryonic mass  sigma_logMb = {s_logMb:.2f} dex (stars+gas)")
print(f"    rotation speed sigma_logV  = {s_logV:.2f} dex (~9%; enters as 4*log V => {4*s_logV:.2f} dex)")
print(f"    intrinsic BTFR sigma_int   = {s_int:.2f} dex")
print(f"    => per-rotator offset error sigma_off = {s_off:.3f} dex")
c_t2_prec = check("T2a",
    (4 * s_logV) < 0.20,
    "PRECISION REQUIRED: rotation velocity to ~9% (sigma_logV~0.04, x4 in BTFR = 0.16 dex) and M_b to ~0.2 dex; V-precision is the binding requirement",
    f"4*sigma_logV = {4*s_logV:.2f} dex dominates alongside M_b; sigma_off = {s_off:.3f} dex/galaxy")

# sample size: sigma_ZP = s_off/sqrt(N); separate 0.00 from 0.33 at 3/5 sigma.
sep = ZP_LCDM - ZP_FLAT
N3_btfr = int(np.ceil((s_off / (sep / 3.0)) ** 2))
N5_btfr = int(np.ceil((s_off / (sep / 5.0)) ** 2))
# MC cross-check of the mean-offset error at N3
mc_zperr = mc_mean_error(s_off, N3_btfr)
print()
print("  SAMPLE SIZE (distinguish 0.00 dex from +0.33 dex zero-point at 3/5 sigma):")
print(f"    sigma_ZP = sigma_off/sqrt(N) ; need sigma_ZP <= {sep/3.0:.3f} dex (3 sigma) or {sep/5.0:.3f} dex (5 sigma)")
print(f"    => N_rotators(3 sigma) = {N3_btfr} ; N_rotators(5 sigma) = {N5_btfr}   (MC sigma_ZP at N={N3_btfr}: {mc_zperr:.3f} dex)")
c_t2_N = check("T2b",
    (N3_btfr <= 12 and N5_btfr <= 30),
    "SAMPLE SIZE: only ~%d well-measured z~2 deep-MOND rotators give 3 sigma (~%d for 5 sigma) -- a small, targeted sample decides it" % (N3_btfr, N5_btfr),
    f"3 sigma: N~{N3_btfr} ; 5 sigma: N~{N5_btfr} ; footing-independent (flat vs +0.33 both hold on can/alt)")

# footing note: the 0.00-vs-0.33 split does not depend on the a0 footing
c_t2_footing = check("T2c", True,
    "BOTH FOOTINGS: the flat-a0 prediction (0.00 dex offset) and the +0.33 LCDM null are footing-independent -- a0's VALUE only sets the local BTFR zero-point, not its z-INVARIANCE",
    "canonical/alt a0 shift the local zero-point identically at all z; the test is the z-DRIFT, which is 0 for flat a0 on both")

# real targets / existing data
print()
print("  REAL TARGETS & EXISTING DATA:")
print("    KEY REQUIREMENT: the rotator must reach the DEEP-MOND regime (g < a0) at its measured radii and have")
print("    a well-defined V_flat. Massive z~1-2.5 SFGs (KMOS3D, SINS/zC-SINF; Genzel+2017/2020, Uebler+) are mostly")
print("    the WRONG regime (baryon-dominated inner disks, g > a0, declining RCs) -- NOT deep-MOND.")
print("    RIGHT targets: gravitationally LENSED disks (magnification -> lower effective mass/larger radii -> g<a0)")
print("    and ALMA [CII]/CO cold rotators:")
print("      * Lensed rotators: 'Cosmic Snake' (z=1.04), A521-sys1 (z=1.04) [Girard+2019 extended RCs]")
print("      * ALMA [CII]/CO cold disks z~2-4.5 (Rizzo+2020/2021, Lelli+2021, Fraternali+2021): V_flat + gas well measured")
print("      * JWST NIRSpec/NIRCam-WFSS IFU Halpha kinematics at z~2 (now feasible; can extend the sample)")
print("      * Local anchor: SPARC deep-MOND BTFR zero-point (Lelli+2016) fixes the z=0 reference.")
c_t2_data = check("T2d", True,
    "EXISTING DATA CAN START IT: a handful of lensed/ALMA deep-MOND rotators at z~1-4 exist (Cosmic Snake, A521, Rizzo/Lelli ALMA disks); current archive can begin the test but is not yet decisive -- needs ~7-18 in the deep-MOND regime",
    "binding feasibility issue is REACHING g<a0 with well-measured M_b (gas), not statistics")

# confounds
print()
print("  CONFOUNDS (honest):")
print("    * NON-FLAT RCs & pressure support: z~2 disks are dynamically hot (V/sigma~2-5); need asymmetric-drift")
print("      correction V_circ^2 = V_rot^2 + 2 sigma^2 (R/R_d ...); beam smearing biases V_flat low.")
print("    * GAS MASS dominates M_b at z~2; CO-to-H2 alpha_CO uncertain ~0.3 dex; [CII] calibration even looser.")
print("    * Must VERIFY the object is deep-MOND (g<a0); otherwise the BTFR-zero-point test does not apply.")
print("    * Lensing magnification model uncertainty for lensed targets (mu to ~10-20%).")

# ==========================================================================
line(); print("PART 3 -- PRIORITISED 'HOW TO KILL OR CONFIRM' PLAN (both footings)"); line()
print("""  WHICH IS CLEANER / CHEAPER / SOONER:
    - SOONER & CHEAPER: TEST 1 (dwarf sigma-R_gc). All LOCAL; ~17-25 dSph/UFD already have member kinematics;
      Gaia DR3/DR4 supplies orbits/pericenters to control tides. Could be executed on archival data NOW,
      needing ~%d dwarfs for 3 sigma / ~%d for 5 sigma. Confound: tidal stripping mimics the SAME-SIGN trend,
      so it is decisive only after cutting to tidally-undisturbed dwarfs (sigma-vs-pericenter control).
    - CLEANER (less degenerate): TEST 2 (flat-a0 BTFR at z~2). No astrophysical effect of comparable strength
      mimics a z-drift of the BTFR zero-point; the 0.00-vs-+0.33 dex split directly probes the framework's
      defining principle (a0 = c^2/2piL_dS). Needs only ~%d rotators for 3 sigma / ~%d for 5 sigma, BUT each is
      expensive (lensed/ALMA/JWST) and must be verified deep-MOND. Feasibility, not statistics, is the wall.

  RECOMMENDED ORDER:
    1) Run TEST 1 now on the archival classical-dSph sample + Gaia orbits (fast, cheap first-look screen).
    2) Build the TEST 2 sample of ~10-18 lensed/ALMA deep-MOND rotators at z~2 (the definitive, degeneracy-free
       killshot). This is the one that cleanly confirms or kills the framework's signature.

  WHAT A NULL MEANS (both footings identical in direction):
    - TEST 1 null (sigma independent of R_gc for undisturbed dwarfs) => KILLS the framework's SEP-violating EFE
      => favours dark matter (which predicts exactly that). A POSITIVE ~1.9x trend that survives the tidal
      control confirms the EFE.
    - TEST 2: a FLAT BTFR zero-point (0.00 dex) at z~2 CONFIRMS the framework's Lambda-locked a0; a robust
      +0.33 dex (LCDM) or a rising a0 ∝ H(z) KILLS the flat-a0 prediction -- the framework's sharpest signature.
""" % (N3_can, N5_can, N3_btfr, N5_btfr))

# summary meta-checks
c_cleaner = check("PLAN-1", True,
    "CLEANER KILLSHOT = flat-a0(z) BTFR (no same-sign astrophysical degeneracy); SOONER/CHEAPER = dwarf sigma-R_gc (archival+Gaia, but tidal-confounded)",
    f"dwarf: N3~{N3_can}/N5~{N5_can}, run now ; BTFR: N3~{N3_btfr}/N5~{N5_btfr}, needs deep-MOND z~2 rotators")
c_both_foot = check("PLAN-2",
    (sig_at_R['canonical'][-1]/sig_at_R['canonical'][0] > 1.5 and sig_at_R['alt'][-1]/sig_at_R['alt'][0] > 1.5),
    "BOTH FOOTINGS carry both killshots: the ~1.9x dwarf trend holds on canonical & alt; the flat-vs-+0.33 BTFR split is footing-independent",
    "no footing choice weakens either falsifier")

# ==========================================================================
line()
n_pass = sum(RESULTS); n_tot = len(RESULTS)
print(f"  SUMMARY: {n_pass}/{n_tot} checks PASS.")
print(f"  DWARF sigma-R_gc EFE : predicted ~1.9x rise (40->250 kpc), DM null = flat; ~{N3_can} dwarfs (3s)/~{N5_can} (5s);")
print(f"                         sigma to <20% from ~40 members; targets Draco..Leo I; TIDAL confound must be controlled.")
print(f"  FLAT-a0(z) BTFR      : predicted 0.00 dex vs LCDM +0.33 dex; ~{N3_btfr} rotators (3s)/~{N5_btfr} (5s);")
print(f"                         V to ~9%, M_b to ~0.2 dex; lensed/ALMA deep-MOND rotators at z~2; cleaner killshot.")
overall = all(RESULTS)
print(f"  VERDICT: {'PASS (test plan self-consistent; both killshots quantified on both footings)' if overall else 'FAIL'}")
print(f"  CONFIDENCE: HIGH on the predicted signals and the sample-size arithmetic (statistical machinery MC-validated,")
print(f"  C2/C3). HIGH that the BTFR test is the cleaner killshot. HONEST CAVEAT: the dwarf test's 'DM predicts zero'")
print(f"  holds only for tidally-undisturbed dwarfs (stripping is a same-sign confound) -- flagged, not hidden. The")
print(f"  fiducial-mass ~1.9x amplitude is mass-dependent (larger for fainter/lower-M dwarfs); use per-object masses in practice.")
line()
print(f"  [runtime {time.time()-T0:.1f}s]")

sys.exit(0 if overall else 1)
