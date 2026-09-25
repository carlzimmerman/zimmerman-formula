#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Z2ETA -- the redshift exponent eta of a0: bound it from the repo's committed high-z evidence.

The parameter:  a0_eff(z) = a0_0 * (H(z)/H0)^eta = a0_0 * E(z)^eta.
   framework: eta = 0 (rho_Lambda constant -> a0 flat in z);  rival: a0 ~ H(z) -> eta = 1.

Committed inputs (read-only):
  1. real_research/virial_floor_2026/highz_sigma_mstar.csv        (116 published z >= 4 galaxies, L328's table)
     + L328_virial_floor_highz_results.json                        (committed S values, for reproduction checks)
     The virial floor (Lean I22):  sigma^4 >= (4/81) G M a0  for every isolated equilibrium system, so
     S(eta) = < sigma^2 / floor(eta)^2 > >= 1 must hold with floor ~ (G M a0 E^eta)^(1/4).  L328 committed
     S(0) = 10.13 [8.71, 13.71], S(1) = 3.30 [2.80, 4.38] (canonical footing).  This lane reconstructs the
     per-object s_i(0) = (sigma_i/floor_i(0))^2 and extrapolates S(eta) = mean_i s_i(0) * E(z_i)^(-eta/2),
     which is EXACT for the L328 statistic (floor ~ E^(eta/4) => sigma^2/floor^2 ~ E^(-eta/2)).
  2. real_research/data/kmos3d_ubler2017.csv                      (135 KMOS3D discs, z = 0.60-2.53, Ubler+2017)
     -> the registered deep-rotator BTFR zero-point test proxy (z ~ 2-2.6 rotation data on disk).
  3. real_research/data/a0_of_z.csv                               (committed direct a0(z) points)
  4. prep_2026/a0z_crossscale/highz_target_ledger_verified_2026.out (committed gate state of the 21-object ledger)

STATEMENT OF ASSUMPTIONS (every one, as demanded):
  A1  Per-object data are the committed L328 table; its construction rules (R1-R4 of build_table.py) are
      carried as-is; M_* in place of M_b makes the floor conservative.
  A2  E(z) = sqrt(Om(1+z)^3 + OL), Om = 0.3153, OL = 0.6847 (the L328 cosmology); eta is defined by E = H/H0.
  A3  s_i(eta) = s_i(0) * E(z_i)^(-eta/2) exactly (floor ~ a0^(1/4) and a0 ~ E^eta).
  A4  Gaussian approximation for the population statistic S(eta): sigma_S(eta) from the SAME bootstrap design
      as L328 (seed 20260923, 4000 resamples, object resampling + gaussian per-object errors on sigma and
      log M*).  Evidence ratio -> likelihood ratio: the floor hypothesis is one-sided (S_true >= 1), so
      p(eta) = Phi((1 - S(eta))/sigma_S(eta)); inside the allowed region the profile likelihood is saturated
      (any S_true >= 1 fits), so the data carry NO two-sided information on eta: the region is a one-sided
      UPPER bound.  "1-sigma" = S(eta) - 1 sigma_S(eta) >= 1 ; "2-sigma" = S(eta) - 2 sigma_S(eta) >= 1.
  A5  No lower bound on eta exists from this statistic (negative eta lowers the floor, S grows, always
      consistent); the region is reported as [0, eta_max(k sigma)] with a note.
  A6  Control: synthetic s_i injected at known eta_true with multiplicative lognormal scatter (E[u]=1 exactly,
      variance from the observed log-dispersion of s_i(0)); the estimator is the SAME monotone root used for
      the bound (S(eta)=1).  In expectation the root of unbiased data is eta_true, so |mean(eta_hat) - eta_true|
      <= 2 std(eta_hat) must hold for eta_true = 0 and 1.  No tuning toward the framework: eta=1 injection must
      return ~1.
  A7  Registered deep-rotator test (STANDING rev 9; OBSERVING_CASE_A0Z_2026.md; PAPER14 v2, DOI
      10.5281/zenodo.22961490): BTFR zero-point shift at z ~ 2.5: framework 0.00 dex vs a0~H(z) +0.33 dex
      (v1 convention, still quoted in STANDING rev 9) / +0.58 dex (v2, log10 E(2.5) = 0.576); per-object
      precision <= 0.13 dex; decision needs 2-4 clean rotators (v2: 3 at +-0.10 or 4 at +-0.20 dex).  Gate:
      deep-MOND g_bar < 0.3 a0 both footings at the upper mass end, V/sigma > 1.5 (pref > 2), lens control
      delta log mu <= 0.05, 35 < i < 75 deg, >= 5 source-plane resolution elements, z >= 2 (window relaxed
      from 2.32-3.12 to z >= 2 in v2).
  A8  The g_bar gate for the KMOS3D z >= 2 discs is evaluated at R_out = 3 R_e with R_e = 2.5 kpc (labelled
      size assumption; robustness row at R_e = 4 kpc): g_bar ~ G M_bar / R_out^2.  These discs are
      high-acceleration; they are CONTROLS, not the registered test objects.
  A9  MUSE folding: only the committed aggregate points of a0_of_z.csv are used.  Per-galaxy MUSE re-derivation
      is NOT attempted: the committed opus48 M03 lane found the released per-galaxy products cannot reconstruct
      the RAR a0 (halo-based proxy slopes with the WRONG sign, -0.263 dex/z vs observed +0.43).  The M01/M02
      asymmetric-drift reconciliation is NOT cited: STANDING rev 9 records a units slip and a per-galaxy AD
      contribution of only ~0.01 dex, so it cannot rescue MUSE's rise.  MUSE's rising a0(z) remains a live
      threat; the Magneticum degeneracy (apparent-a0 rise x3 by z=2 in LCDM, Mayer+2023) keeps the RAR arm
      non-diagnostic of a FUNDAMENTAL a0(z).
  A10 Both footings (canonical 9.3619e-11, alt 1.1279e-10) are carried wherever the committed analysis used
      both; load-bearing checks are stated on the canonical footing with the alt reported.

Run from the repository root:
  python3 real_research/z2_eta_2026/Z2ETA_eta_bound_a0.py
Writes real_research/z2_eta_2026/Z2ETA_results.json
"""
import os, sys, csv, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SLUG = "Z2ETA_results"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "Z2ETA", "checks": {}, "numbers": {}}


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


P(__doc__)
G, MSUN = 6.6743e-11, 1.98892e30
Om, OL = 0.3153, 0.6847
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KMS = 1e3


def Ez(z):
    z = np.asarray(z, dtype=float)
    return np.sqrt(Om * (1 + z) ** 3 + OL)


def floor_kms(logM, a0): return ((4 / 81) * G * 10 ** logM * MSUN * a0) ** 0.25 / KMS


def read_rows(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                rows.append(dict(name=r["name"], z=float(r["z"]), sig=float(r["sigma"]),
                                 esig=float(r["sigma_err"] or 0), lm=float(r["logMstar"]),
                                 elm=float(r["logMstar_err"] or 0.3)))
            except (ValueError, KeyError):
                continue
    return rows


def S_stat(rows, eta, footing, rng=None, nboot=0):
    """Population mean of s_i(eta) = (sigma/floor(eta))^2, with bootstrap.

    Bootstrap design IDENTICAL to L328 (object resampling with replacement + gaussian per-object errors on
    sigma and log M*, same seed 20260923); the computation is vectorised so the draws are not the same random
    numbers as L328's sequential loop, but the distribution and design are the same (Gaussian approx. A4).
    """
    sig = np.array([r["sig"] for r in rows]); esig = np.array([r["esig"] for r in rows])
    lm = np.array([r["lm"] for r in rows]); elm = np.array([r["elm"] for r in rows])
    Z = np.array([r["z"] for r in rows])
    flo = ((4 / 81) * G * 10 ** lm * MSUN * A0[footing] * Ez(Z) ** eta) ** 0.25 / KMS
    s0 = float(np.mean((sig / flo) ** 2))
    if not nboot:
        return s0, None
    N = len(rows)
    idx = rng.integers(0, N, (nboot, N))
    sigm = np.maximum(sig[idx] + esig[idx] * rng.normal(0.0, 1.0, (nboot, N)), 1e-3)
    lmm = lm[idx] + elm[idx] * rng.normal(0.0, 1.0, (nboot, N))
    flom = ((4 / 81) * G * 10 ** lmm * MSUN * A0[footing] * Ez(Z)[idx] ** eta) ** 0.25 / KMS
    bs = np.mean((sigm / flom) ** 2, axis=1)
    return s0, (float(np.std(bs)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)),
                float(np.mean(bs < 1.0)))

# ----------------------------------------------------------------------------
banner("E-SECTION: ETA FROM THE L328 VIRIAL-FLOOR EVIDENCE (116 published z >= 4 galaxies)")
CSV = os.path.join(REPO, "real_research", "virial_floor_2026", "highz_sigma_mstar.csv")
if not os.path.exists(CSV):
    P("PRE-REGISTERED, AWAITING DATA: highz_sigma_mstar.csv missing -- no verdict possible.")
    sys.exit(2)
rows = read_rows(CSV)
OUT["numbers"]["N_L328"] = len(rows)
P(f"   objects with (z, sigma, log M_*): {len(rows)}")

# --- reproduction of the committed S values ---------------------------------
committed = json.load(open(os.path.join(REPO, "real_research", "virial_floor_2026",
                                        "L328_virial_floor_highz_results.json")))["numbers"]["population"]
S0c = S_stat(rows, 0.0, "canonical")[0]
S1c = S_stat(rows, 1.0, "canonical")[0]
S0a = S_stat(rows, 0.0, "alt")[0]
S1a = S_stat(rows, 1.0, "alt")[0]
dev0 = abs(S0c - committed["framework_canonical"]["S"])
dev1 = abs(S1c - committed["rival_canonical"]["S"])
OUT["numbers"]["reproduction"] = {"S_calc_eta0_can": S0c, "S_committed_eta0_can": committed["framework_canonical"]["S"],
                                  "S_calc_eta1_can": S1c, "S_committed_eta1_can": committed["rival_canonical"]["S"]}
check("E1 reconstruction reproduces the committed statistic (|S_calc - S_committed| <= 0.02, canonical, eta=0 and 1)",
      f"dev eta=0: {dev0:.4f} (S={S0c:.4f} vs {committed['framework_canonical']['S']:.4f}); dev eta=1: {dev1:.4f} "
      f"(S={S1c:.4f} vs {committed['rival_canonical']['S']:.4f})", dev0 <= 0.02 and dev1 <= 0.02,
      "validates the exact reconstruction s_i(eta) = s_i(0) E(z)^(-eta/2) used for the whole lane")

# --- S(eta) over a grid, with bootstrap sigma ---------------------------------
rng = np.random.default_rng(20260923)          # L328's own seed
ETA = np.arange(-3.0, 6.01, 0.02)
grid = {}
for foot in A0:
    Sg, sgL, loL, hiL, pL = [], [], [], [], []
    for eta in ETA:
        s0, ci = S_stat(rows, float(eta), foot, rng, 4000)
        Sg.append(s0)
        if foot == "canonical":
            sgL.append(ci[0]); loL.append(ci[1]); hiL.append(ci[2]); pL.append(ci[3])
    grid[foot] = {"S": np.array(Sg)}
    if foot == "canonical":
        grid[foot].update({"sigma": np.array(sgL), "CI95lo": np.array(loL), "CI95hi": np.array(hiL),
                           "P(S<1)": np.array(pL)})
i0, i1, i2 = (np.argmin(abs(ETA - e)) for e in (0.0, 1.0, 2.0))
P(f"   canonical: S(eta=0) = {grid['canonical']['S'][i0]:.2f}  S(eta=1) = "
  f"{grid['canonical']['S'][i1]:.2f}  S(eta=2) = "
  f"{grid['canonical']['S'][i2]:.2f}")
P(f"   sigma_S:   eta=0: {grid['canonical']['sigma'][i0]:.3f}   eta=1: "
  f"{grid['canonical']['sigma'][i1]:.3f}   eta=2: "
  f"{grid['canonical']['sigma'][i2]:.3f}")

def S_point(eta, foot="canonical"):
    return float(np.mean([(r["sig"] / floor_kms(r["lm"], A0[foot] * Ez(r["z"]) ** eta)) ** 2 for r in rows]))

def sig_S(eta, foot="canonical"):
    i = min(range(len(ETA)), key=lambda k: abs(ETA[k] - eta))
    return float(grid[foot]["sigma"][i])

def root_of(g, lo=-2.0, hi=5.0, tol=1e-9):
    """Monotone root of g(eta)=0 by bisection on [lo, hi]."""
    glo, ghi = g(lo), g(hi)
    assert glo * ghi < 0, f"root not bracketed: g({lo})={glo}, g({hi})={ghi}"
    while hi - lo > tol:
        m = 0.5 * (lo + hi)
        if g(m) * glo <= 0:
            hi = m
        else:
            lo, glo = m, g(m)
    return 0.5 * (lo + hi)

eta_sep = root_of(lambda e: S_point(e) - 1.0)                      # 0-sigma saturation boundary
eta_max1 = root_of(lambda e: S_point(e) - sig_S(e) - 1.0)          # 1-sigma upper bound
eta_max2 = root_of(lambda e: S_point(e) - 2.0 * sig_S(e) - 1.0)    # 2-sigma upper bound
z1 = (S_point(1.0) - 1.0) / sig_S(1.0)
OUT["numbers"]["eta_floor"] = {"eta_sep_saturation": eta_sep, "eta_max_1sigma": eta_max1,
                               "eta_max_2sigma": eta_max2, "S(1)_z_score_above_floor": z1,
                               "region_1sigma": [0.0, eta_max1], "region_2sigma": [0.0, eta_max2]}

S1_lo_can = committed["rival_canonical"]["CI95"][0]
S0_lo_can = committed["framework_canonical"]["CI95"][0]
S1_lo_alt = committed["rival_alt"]["CI95"][0]
S0_lo_alt = committed["framework_alt"]["CI95"][0]
OUT["numbers"]["floor_hold"] = {"S0_can_CI95lo": S0_lo_can, "S1_can_CI95lo": S1_lo_can,
                                "S0_alt_CI95lo": S0_lo_alt, "S1_alt_CI95lo": S1_lo_alt}
check("E2 the framework's floor holds at eta=0 (95% CI lower on S(0) >= 1, both footings)",
      f"canonical: S={S0c:.2f} [lo {S0_lo_can:.2f}]; alt: S={S0a:.2f} [lo {S0_lo_alt:.2f}]",
      S0_lo_can >= 1.0 and S0_lo_alt >= 1.0,
      "a failure at eta=0 would falsify the flat-a0 virial floor at z > 4")
check("E3 the a0 ~ H(z) rival's floor holds at eta=1 -- the rival SURVIVES the floor (95% CI lower on S(1) >= 1, "
      "both footings)",
      f"canonical: S={S1c:.2f} [lo {S1_lo_can:.2f}]; alt: S={S1a:.2f} [lo {S1_lo_alt:.2f}]",
      S1_lo_can >= 1.0 and S1_lo_alt >= 1.0,
      "rival surviving is a RESULT, not a pass for the framework: at z >= 4 the galaxies are too high-acceleration "
      "for the floor to separate flat from rising a0 (committed L328 R1-R3 reached the same conclusion)")
check("E4 eta = 1 lies inside the 2-sigma inclusion region of the floor (eta_max_2sigma >= 1)",
      f"eta_max_2sigma = {eta_max2:.3f} (1-sigma bound {eta_max1:.3f}); z(eta=1) = (S(1)-1)/sigma = {z1:.2f}",
      eta_max2 >= 1.0,
      "the registered rival (eta=1) is NOT excluded by the high-z virial floor at 2 sigma; the floor only caps eta "
      "from above")
check("E5 (reported) eta inclusion region at 1-2 sigma and the best-separating value (0-sigma saturation "
      "boundary, no lower bound)",
      f"1-sigma: [0, {eta_max1:.3f}]; 2-sigma: [0, {eta_max2:.3f}]; separation value eta_sep (S(eta)=1 point "
      f"estimate) = {eta_sep:.3f}", True,
      "negative eta is unconstrained (it lowers the floor, S grows); the floor cannot separate eta=0 from eta=1 "
      "(both clear it by > 5 sigma); eta_sep is the value at which the population would exactly saturate the floor",
      load_bearing=False)

# ----------------------------------------------------------------------------
banner("C-SECTION: CONTROL -- inject eta_true = {0, 1}, estimator must recover it")
lns = np.log(np.array([(r["sig"] / floor_kms(r["lm"], A0["canonical"])) ** 2 for r in rows]))
sig_ln = float(np.std(lns))                                        # observed log-scatter of s_i(0)
OUT["numbers"]["control"] = {"log_scatter_s": sig_ln}
P(f"   observed log-scatter of s_i(0): {sig_ln:.3f}")

def control_run(eta_true, n_real=400, seed=None):
    rng = np.random.default_rng(seed)
    hits = []
    for _ in range(n_real):
        u = np.exp(rng.normal(0.0, sig_ln, len(rows)) - 0.5 * sig_ln ** 2)   # E[u] = 1 exactly
        s_i = u  # s_i(eta_true) = 1 * u by construction (sigma_mock = floor(eta_true)*sqrt(u))
        def S_mock(eta):
            return float(np.mean(s_i * np.array([Ez(r["z"]) ** ((eta_true - eta) / 2.0) for r in rows])))
        hits.append(root_of(lambda e: S_mock(e) - 1.0, lo=-2.5, hi=5.5))
    return np.mean(hits), np.std(hits), float(np.percentile(hits, 2.5)), float(np.percentile(hits, 97.5))

c0 = control_run(0.0, seed=424242)
c1 = control_run(1.0, seed=242424)
OUT["numbers"]["control"]["eta_true_0"] = {"mean": c0[0], "std": c0[1], "CI95": [c0[2], c0[3]]}
OUT["numbers"]["control"]["eta_true_1"] = {"mean": c1[0], "std": c1[1], "CI95": [c1[2], c1[3]]}
check("C1 control at eta_true = 0: estimator returns 0 within 2 std",
      f"eta_hat = {c0[0]:.3f} +/- {c0[1]:.3f} (95% [{c0[2]:.2f}, {c0[3]:.2f}])", abs(c0[0]) <= 2 * c0[1],
      "injected flat-a0 data must come back flat-a0")
check("C2 control at eta_true = 1: estimator returns 1 within 2 std",
      f"eta_hat = {c1[0]:.3f} +/- {c1[1]:.3f} (95% [{c1[2]:.2f}, {c1[3]:.2f}])", abs(c1[0] - 1.0) <= 2 * c1[1],
      "injected a0 ~ H(z) data must come back eta ~ 1 -- the estimator is not tuned toward the framework")

# ----------------------------------------------------------------------------
banner("D-SECTION: THE REGISTERED DEEP-ROTATOR BTFR ZERO-POINT TEST (z ~ 2.5)")
P("   Registered statistic (STANDING rev 9; OBSERVING_CASE_A0Z_2026.md; PAPER14 v2 10.5281/zenodo.22961490):")
P("   BTFR zero-point shift at z ~ 2.5: framework 0.00 dex vs a0~H(z) +0.33 dex (v1 / STANDING) / +0.58 dex")
P("   (v2, = log10 E(2.5) = 0.576); per-object +-0.13 dex; 2-4 clean rotators decide (v2: 3 at +-0.10 or")
P("   4 at +-0.20 dex).  Gate: deep-MOND g_bar < 0.3 a0 both footings at the upper mass end, V/sigma > 1.5,")
P("   lens delta log mu <= 0.05, i in (35, 75) deg, >= 5 kinematic elements, z >= 2, gas measured.")

KMO = os.path.join(REPO, "real_research", "data", "kmos3d_ubler2017.csv")
krows = []
with open(KMO) as f:
    for r in csv.DictReader(f):
        try:
            krows.append(dict(z=float(r["z"]), lM=float(r["logMbar"]), V=float(r["Vcirc_kms"]),
                              s0=float(r["sigma0_kms"])))
        except (ValueError, KeyError):
            continue
z2 = [r for r in krows if r["z"] >= 2.0 and r["V"] / r["s0"] > 1.5]
OUT["numbers"]["kmos3d"] = {"N_total": len(krows), "N_z2_rotating_Vsig>1.5": len(z2),
                            "z_range": [min(r["z"] for r in krows), max(r["z"] for r in krows)]}
P(f"   KMOS3D on disk: {len(krows)} discs, z = {min(r['z'] for r in krows):.2f}-{max(r['z'] for r in krows):.2f}; "
  f"z >= 2 rotators (V/sigma > 1.5): {len(z2)}")

def M_local(V, a0):                       # log10 M_bar (Msun) at V (km/s) on the frozen local deep-MOND TF
    return math.log10((V * KMS) ** 4 / (G * MSUN * a0))

deltas = {f: [] for f in A0}
gates = {f: [] for f in A0}
RE_OUT = [2.5, 4.0]
for r in z2:
    for f in A0:
        d = M_local(r["V"], A0[f]) - r["lM"]
        deltas[f].append(d)
        g = G * 10 ** r["lM"] * MSUN / (3.0 * RE_OUT[0] * 3.0857e19) ** 2 / A0[f]   # R_out = 3 R_e, R_e = 2.5 kpc
        gates[f].append(g)
OUT["numbers"]["kmos3d"]["delta_z2_median"] = {f: float(np.median(deltas[f])) for f in A0}
OUT["numbers"]["kmos3d"]["delta_z2_scatter"] = {f: float(np.std(deltas[f])) for f in A0}
OUT["numbers"]["kmos3d"]["gbar_a0_out"] = {f: [round(min(gates[f]), 2), round(max(gates[f]), 2)] for f in A0}
P(f"   z >= 2 rotators, median BTFR displacement 4logV - logM_bar - C0(local): canonical "
  f"{np.median(deltas['canonical']):+.3f} dex (scatter {np.std(deltas['canonical']):.3f}); alt "
  f"{np.median(deltas['alt']):+.3f} dex")
P(f"   g_bar(R_out=3Re, Re=2.5kpc)/a0 range over z >= 2 rotators: canonical {min(gates['canonical']):.2f}-"
  f"{max(gates['canonical']):.2f}  (deep-MOND gate demands < 0.3)")

# --- committed ledger gate state (read-only parse) ------------------------------
ledger = os.path.join(REPO, "prep_2026", "a0z_crossscale", "highz_target_ledger_verified_2026.out")
ledger_lines = [l for l in open(ledger) if "confirmed deep-MOND" in l or "window z >= 2" in l]
n_clean = 0
for l in ledger_lines:
    P("   ledger: " + l.strip())
n_ledger_gated = sum(1 for l in ledger_lines if "window z >= 2" in l and "13 objects" in l)  # informational
OUT["numbers"]["deep_rotator_gate"] = {"clean_rotators_on_disk_passing_all_gates": n_clean,
                                       "ledger_confirmed_deepMOND": 0,
                                       "ledger_in_window_deepMOND_plausible_optimistic_only": 1 if any(
                                           "OLAS M0717-02064" in l for l in ledger_lines) else 0}
check("D1 DATA GATE for the registered test: >= 2 clean deep-MOND rotators (g_bar < 0.3 a0 both footings at the "
      "upper mass end, V/sigma > 1.5, lens control, gas measured, z in [2, 2.6]) exist on disk",
      f"0 / 2 required (KMOS3D z>=2 rotators all high-acceleration, g_bar/a0 >= {min(gates['canonical']):.2f} > "
      f"0.3; committed ledger: confirmed deep-MOND objects = 0; the only z >= 2 optimistic-corner candidate "
      f"(OLAS M0717-02064, g_bar/a0 [0.17, 1.29]) fails the committed upper-end rule and has no measured gas)",
      n_clean >= 2, "REGISTERED TEST IS PENDING DATA, not scored.  Required sample (committed): 2-4 clean "
      "rotators (STANDING rev 9); PAPER14 v2: 3 galaxies at +-0.10 dex or 4 at +-0.20 dex; per-object <= 0.13 dex "
      "(deltaV/V < 5%, delta log M_b < 0.10); each must pass the gate above.  JWST/NIRSpec G235H/F170LP Stage 1, "
      "ALMA Band 3 CO(3-2) Stage 2 (funnel, DOI 10.5281/zenodo.22563139).", load_bearing=False)

# --- reported proxy: z >= 2 KMOS3D rotators vs the frozen zero point -------------
med = float(np.median(deltas["canonical"]))
scat = float(np.std(deltas["canonical"]))
se = scat / math.sqrt(len(z2))
check("D2 (reported) on-disk proxy: median BTFR displacement of z >= 2 KMOS3D rotators vs the frozen zero point "
      "0.00 (framework) / +0.33 (v1 rival) / +0.58 (v2, a0 ~ H)",
      f"median +- se = {med:+.3f} +- {se:.3f} dex (scatter {scat:.3f}; N={len(z2)}); framework 0.00, rival +0.33, "
      f"rival(eta=1) +0.58", True,
      "NOT the registered test: high-acceleration regime suppresses the deep-MOND displacement, the absolute "
      "offset is zero-point-anchored (committed ground_highz_btfr_realdata.py calls it a constant systematic), "
      "and there is no lens/gas-stage control.  Reported for completeness only.", load_bearing=False)

# --- z-trend (the committed anchor-free discriminator) -> eta_kin -----------------
def ols(x, y):
    """OLS slope, intercept of y on x (committed-script convention: returns (slope, intercept))."""
    b = np.linalg.lstsq(np.vstack([np.ones_like(x), x]).T, y, rcond=None)[0]
    return b[1], b[0]

def boot_slope(x, y, n=5000, seed=12345):
    rng = np.random.default_rng(seed); N = len(x)
    return float(np.std([ols(x[i], y[i])[0] for i in (rng.integers(0, N, N) for _ in range(n))]))

def ctrl_slope(y, zz, covars, n=5000, seed=24680):
    def fit(yy, zzz, cc): return np.linalg.lstsq(np.column_stack([np.ones_like(yy), zzz] + cc), yy, rcond=None)[0][1]
    c = fit(y, zz, covars); rng = np.random.default_rng(seed); N = len(y)
    bs = [fit(y[i], zz[i], [cv[i] for cv in covars]) for i in (rng.integers(0, N, N) for _ in range(n))]
    return c, float(np.std(bs))

zs = np.array([r["z"] for r in krows]); lMs = np.array([r["lM"] for r in krows])
Mb = 10 ** lMs * MSUN; Vobs = np.array([r["V"] for r in krows]); sg0 = np.array([r["s0"] for r in krows])
dlogV = np.log10(Vobs) - np.log10((G * Mb * 1.2e-10) ** 0.25 / KMS)        # committed script's definition
slope, icpt = ols(zs, dlogV); slope_err = boot_slope(zs, dlogV)
adr = sg0 / Vobs
aslope, aerr = ctrl_slope(dlogV, zs, [adr], seed=777)
RSLOPE = 0.0561                                                             # committed rising-branch slope
eta_kin = slope / RSLOPE; eta_kin_e = slope_err / RSLOPE
eta_kin_ad = aslope / RSLOPE; eta_kin_ad_e = aerr / RSLOPE
OUT["numbers"]["eta_kinematics"] = {"slope_dexz": slope, "slope_err": slope_err,
                                    "eta_kin": eta_kin, "eta_kin_err": eta_kin_e,
                                    "eta_kin_ADcontrolled": eta_kin_ad, "eta_kin_AD_err": eta_kin_ad_e}
reprod_ok = abs(slope - (-0.0286)) <= 0.001 and abs(aslope - (-0.0166)) <= 0.0015
check("D3 (reported) KMOS3D z-trend reproduces the committed slope and maps it to eta (anchor-free, "
      "AD-controlled rows carried)",
      f"slope = {slope:+.4f} +/- {slope_err:.4f} dex/z -> eta_kin = {eta_kin:+.2f} +/- {eta_kin_e:.2f}; "
      f"AD-controlled slope = {aslope:+.4f} +/- {aerr:.4f} -> eta_kin_AD = {eta_kin_ad:+.2f} +/- "
      f"{eta_kin_ad_e:.2f}; reproduction of committed values: {'OK' if reprod_ok else 'MISMATCH'}", reprod_ok,
      "the committed script's verdict is carried: negatively sloped (declining a0) but LambdaCDM-degenerate "
      "(dark-matter + gas-fraction growth give the same sign) and AD-absorbed to 1.3 sigma -> UNDECIDED, "
      "systematics-limited; under the a0-only reading it excludes eta=1 at ~5.7 sigma",
      load_bearing=False)

# ----------------------------------------------------------------------------
banner("M-SECTION: FOLDING THE COMMITTED DIRECT a0(z) POINTS (MUSE arm)")
A0Z = os.path.join(REPO, "real_research", "data", "a0_of_z.csv")
pts = []
with open(A0Z) as f:
    for line in f:
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("z,"):
            continue
        p = s.split(",")
        try:
            pts.append((float(p[0]), float(p[1]), float(p[2]), p[3].strip()))
        except ValueError:
            continue
OUT["numbers"]["a0z_points"] = [{"z": p[0], "a0e10": p[1], "sig": p[2], "src": p[3]} for p in pts]
P(f"   committed a0(z) points: {[(p[0], p[1], p[2], p[3]) for p in pts]}")

def wls_fit(idx):
    xs = [math.log10(Ez(pts[i][0])) for i in idx]
    ys = [math.log10(pts[i][1]) for i in idx]
    ws = [1.0 / (pts[i][2] / (pts[i][1] * math.log(10.0))) ** 2 for i in idx]
    W = np.array(ws); X = np.vstack([np.ones(len(idx)), xs]).T
    Y = np.array(ys)
    sw = np.sqrt(W)                                  # weighted LS: minimise sum w r^2
    beta, *_ = np.linalg.lstsq(X * sw[:, None], Y * sw, rcond=None)
    cov = np.linalg.inv(X.T @ (W[:, None] * X))
    return beta[1], math.sqrt(cov[1, 1]), beta[0]

eta_pts, eta_pts_e, c0pt = wls_fit([0, 1, 2])
eta_muse, eta_muse_e, _ = wls_fit([0, 2])          # SPARC anchor + MUSE point only (Varashteanu flagged
                                                   # inter-method: A0Z_MUSE_DARK_III_CONFRONTATION.md)
OUT["numbers"]["eta_direct_points"] = {"eta_3pt_WLS": eta_pts, "err": eta_pts_e,
                                       "eta_SPARC_MUSE_2pt": eta_muse, "err_2pt": eta_muse_e}
check("M1 (reported) weighted fit of the committed a0(z) points: a0(z) = a0(0) E(z)^eta",
      f"eta = {eta_pts:+.2f} +/- {eta_pts_e:.2f} (3 points); SPARC+MUSE only: {eta_muse:+.2f} +/- "
      f"{eta_muse_e:.2f}; a0(0) = 10^{c0pt:.3f} x1e-10", True,
      "the RAR arm leans RISING (eta ~ 0.76 from all three committed points, ~1.3 from SPARC+MUSE); this arm is "
      "committed-graded NON-DIAGNOSTIC of a fundamental a0(z): the fitted RAR "
      "scale rises x3 by z=2 in LCDM with no a0 at all (Mayer+2023, Magneticum); MUSE's rise is 'faster than "
      "H(z)' and cannot come from any background-density law", load_bearing=False)
check("M2 (reported) method-split carried: MUSE reconciliation dead, rise remains a live threat",
      "STANDING rev 9: opus48 M01/M02 asymmetric-drift reconciliation has a units slip; the real per-galaxy AD "
      "contribution is ~0.01 dex and cannot rescue the rise; per-galaxy re-derivation invalid (M03: halo-based "
      "proxy slope -0.263 dex/z, wrong sign)", True,
      "no per-galaxy MUSE a0 is folded because none can be reconstructed from the released products (committed "
      "M03); the committed points are folded as-is with their caveats; the two arms (RAR: rising; BTFR/"
      "kinematics: flat-to-declining) remain split and neither is clean", load_bearing=False)

# ----------------------------------------------------------------------------
banner("VERDICT")
verdict = (f"eta inclusion from the committed high-z evidence: "
           f"L328 floor bounds eta <= {eta_max1:.2f} (1-sigma) / eta <= {eta_max2:.2f} (2-sigma), "
           f"no lower bound (region [0, {eta_max2:.2f}] at 2-sigma; saturation boundary eta_sep = {eta_sep:.2f}); "
           f"direct a0(z) points: eta = {eta_pts:.2f} +/- {eta_pts_e:.2f} (RAR arm, committed-graded "
           f"non-diagnostic); KMOS3D z-trend: eta = {eta_kin:.2f} +/- {eta_kin_e:.2f} raw, "
           f"{eta_kin_ad:.2f} +/- {eta_kin_ad_e:.2f} AD-controlled (LambdaCDM-degenerate, undecided).  "
           f"Flat (eta=0) vs H(z) (eta=1): BOTH inside the floor's 2-sigma region (S(1) clears the floor by "
           f"{z1:.1f} sigma), so the high-z virial floor does NOT discriminate -- verdict = measured range, "
           f"UNDECIDED, with the two direct arms straddling (RAR ~ +0.8, kinematics ~ -0.3).  "
           f"Registered deep-rotator BTFR test: DATA GATE NOT MET (0/2-4 clean rotators) -- pending "
           f"JWST/NIRSpec + ALMA Band 3; per-object +-0.13 dex, 3 at +-0.10 or 4 at +-0.20 dex required.")
OUT["verdict"] = verdict
OUT["numbers"]["eta_central_combined"] = {"eta_central_direct_points": eta_pts,
                                          "eta_region_2sigma": [0.0, eta_max2],
                                          "eta_region_1sigma": [0.0, eta_max1],
                                          "eta_sep_saturation": eta_sep}
P(verdict)
lb = [c for c in CH if c[2]]
npass = sum(1 for c in CH if c[1])
nlb = sum(1 for c in lb if c[1])
banner(f"VERDICT  ({nlb}/{len(lb)} load-bearing PASS; {npass}/{len(CH)} total PASS)")
with open(os.path.join(HERE, f"{SLUG}.json"), "w") as f:
    json.dump(OUT, f, indent=1, default=float)
P(f"\nZ2ETA COMPLETE: {npass}/{len(CH)} checks PASS.")
sys.exit(0 if nlb == len(lb) else 1)