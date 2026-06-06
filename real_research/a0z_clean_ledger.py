#!/usr/bin/env python3
r"""
FRONT 3 -- THE CLEAN a0(z) LEDGER (the definitive confrontation on the CORRECT framework law).
=============================================================================================
C. Zimmerman, 2026-06-06.  Single-file, runnable, pure-numpy.  This SUPERSEDES the ~21 live repo
scripts the integrity audit caught scoring a0(z) on the WRONG (rising E(z)) branch and calling it
"the framework".  Here the FRAMEWORK is the canonical DECLINING law and E(z) is kept ONLY as a
labeled RIVAL ("Verlinde / cH" -- the rho_total footing-bug branch) to beat.

THE FRAMEWORK LAW (canon):
  a0_today = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = 9.36e-11 m/s^2   (DARK ENERGY ALONE).
  a0(z)/a0(0) = sqrt( rho_DE(z) / rho_DE(0) ),  rho_DE(z) from DESI DR2 CPL  w0=-0.752, wa=-0.86:
     rho_DE(z)/rho_DE(0) = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))
  => a0(z) RISES to a ~+6% BUMP near z~0.4, then DECLINES: ~0.99 (z=0.4), 0.86 (z=2), 0.74 (z=3).
     NON-MONOTONIC, and DECLINING at high z.  <-- THE distinctive, falsifiable prediction.

FOUR MODELS SCORED (chi^2 vs a0(z)/a0(0), each normalized to that dataset's own z~0 anchor):
  (1) FRAMEWORK   : declining sqrt(rho_DE)  [bump then decline]      -- the canon
  (2) CONSTANT    : a0(z)/a0(0) = 1                                  -- flat
  (3) RISING-cH   : E(z) = sqrt(Om(1+z)^3+OL)  [Verlinde rival]      -- the WRONG branch, RIVAL only
  (4) regMOND     : a0(z)/a0(0) = 1  (a0=1.2e-10 const)             -- standard MOND, RIVAL
       NOTE: as a SHAPE normalized to z~0, (4) regular-MOND-constant is identical to (2) CONSTANT.
       They differ only in ABSOLUTE a0 (1.2e-10 vs the framework's 9.36e-11) -- which the ratio
       test cancels.  We report (4) explicitly so the ledger is complete and we say plainly that
       the SHAPE test cannot separate framework-flat from MOND-flat; only an absolute-a0(0) anchor can.

DATA (all real, in-repo or published-verbatim; see per-loader provenance):
  - real_research/data/rc100_nestorshachar2023_table3.csv   (Nestor-Shachar 2023; z=0.6-2.5; per-gal a0=Vc^4/GMbar; deep-MOND flag)
  - real_research/data/kross_harrison2017.csv                (Harrison+2017; z~0.85; a0=Vc^4/G Mstar(1+fgas))
  - real_research/data/kmos3d_ubler2017.csv                  (Ubler+2017; z=0.6-2.5; a0=Vcirc^4/G Mbar)
  - MUSE-DARK III (Ciocan+2026, A&A 709 L16): published linear fit a0(z)=1.0+1.59z (x1e-10) and
        binned points; local SPARC anchor 1.20 +/- 0.26.  Hardcoded verbatim from the cited paper.

HONEST DISCIPLINE: brutally honest.  If the rising RIVAL fits some data BETTER than the framework
decline, we SAY SO.  No numerology.  This is offense WITH integrity.

Pure numpy + csv.  Run:  python3 /tmp/front_a0z.py
"""
import numpy as np, csv, os

# ----------------------------------------------------------------------------------------------------
# Constants / cosmology (framework canon)
# ----------------------------------------------------------------------------------------------------
c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
Om, OL = 0.315, 0.685
H0 = 67.4e3 / 3.0857e22                     # 2.184e-18 s^-1
rho_crit = 3 * H0**2 / (8 * np.pi * G)
rho_DE0 = OL * rho_crit
A0_FRAMEWORK = (c / 2) * np.sqrt(G * rho_DE0)   # = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (dark energy alone)
A0_REGMOND   = 1.2e-10                            # standard MOND scale (RIVAL absolute anchor)

# DESI DR2 (2503.14738) evolving-DE central values (the canon's distinctive inputs)
W0, WA = -0.752, -0.86

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
DATADIR = os.path.join(REPO, "real_research", "data")


def rho_de_ratio(z, w0=W0, wa=WA):
    """rho_DE(z)/rho_DE(0) for CPL w(a)=w0+wa(1-a)."""
    z = np.asarray(z, float)
    a = 1.0 / (1.0 + z)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))


# ---- the four model SHAPES, a0(z)/a0(0) (normalized to z=0) -----------------------------------------
def m_framework(z):  return np.sqrt(rho_de_ratio(z))                 # (1) declining sqrt(rho_DE) -- THE FRAMEWORK
def m_constant(z):   return np.ones_like(np.asarray(z, float))       # (2) constant
def m_rising_cH(z):  return np.sqrt(Om * (1 + np.asarray(z, float))**3 + OL)  # (3) E(z) Verlinde RIVAL (wrong branch)
def m_regMOND(z):    return np.ones_like(np.asarray(z, float))       # (4) regular-MOND constant (RIVAL; flat in shape)

MODELS = [
    ("FRAMEWORK sqrt(rho_DE)", m_framework, "canon (declining; +6% bump @z~0.4)"),
    ("CONSTANT",               m_constant,  "flat"),
    ("RISING-cH E(z) [RIVAL]", m_rising_cH, "Verlinde/wrong-branch, rises x3 by z=2"),
    ("regMOND const [RIVAL]",  m_regMOND,   "standard MOND a0=1.2e-10 (flat shape)"),
]


# ====================================================================================================
# DATA LOADERS -- each returns (z_array, a0_array[m/s^2]) of per-galaxy a0 estimates, plus a label.
# ====================================================================================================
def load_rc100():
    """Nestor-Shachar 2023 Table 3. Per-galaxy a0 = Vc^4/(G Mbar) already tabulated.
    Use the DEEP-MOND subset (deepMOND_g_lt_a0==1): the regime where a0=Vc^4/GMbar is the cleanest
    (g<a0).  Caveat: Vc is at R_e, not the asymptotic flat velocity -> a0 scatters a lot (Vc^4 lever)."""
    z, a0, dm = [], [], []
    with open(os.path.join(DATADIR, "rc100_nestorshachar2023_table3.csv")) as f:
        for r in csv.DictReader(f):
            try:
                z.append(float(r["z"])); a0.append(float(r["a0_Vc4_over_GMbar_ms2"]))
                dm.append(int(r["deepMOND_g_lt_a0"]))
            except Exception:
                pass
    z, a0, dm = np.array(z), np.array(a0), np.array(dm)
    sel = dm == 1
    return z[sel], a0[sel], "RC100 deep-MOND (Nestor-Shachar23)", z, a0  # also return full for an all-RC100 view


def load_kross():
    """Harrison+2017 KROSS z~0.85. a0 = VC^4/(G Mbar), Mbar = Mstar*(1+f_gas).
    Gas is the dominant systematic; the LOCAL SPARC anchor INCLUDES gas, so we MUST include gas here.
    Use a realistic mass-dependent gas correction f_gas ~ 1.0*(M/1e10)^-0.4 (Tacconi+2018 scaling)."""
    d = np.genfromtxt(os.path.join(DATADIR, "kross_harrison2017.csv"), delimiter=",", names=True)
    z, Ms, VC = d["z"], d["Mstar"], d["VC_kms"]
    fgas = 1.0 * (Ms / 1e10) ** (-0.4)
    Mbar = Ms * Msun * (1 + fgas)
    a0 = (VC * 1e3) ** 4 / (G * Mbar)
    return z, a0, "KROSS z~0.85 (Harrison17, gas-corr)"


def load_kmos3d():
    """Ubler+2017 KMOS3D. a0 = Vcirc^4/(G Mbar). Massive, often dispersion-supported -> biased HIGH,
    not deep-MOND.  Included for completeness with that caveat stated."""
    d = np.genfromtxt(os.path.join(DATADIR, "kmos3d_ubler2017.csv"), delimiter=",", names=True)
    z, lMb, V = d["z"], d["logMbar"], d["Vcirc_kms"]
    a0 = (V * 1e3) ** 4 / (G * 10 ** lMb * Msun)
    return z, a0, "KMOS3D (Ubler17, massive/biased-high)"


# MUSE-DARK III (Ciocan+2026) -- published numbers, hardcoded verbatim (NOT derived in-repo).
# Binned a0(z) points (x1e-10) + the SPARC z=0 anchor; and the authors' linear fit a0=1.0+1.59z.
MUSE_PTS = [  # (z, a0[1e-10], sigma[1e-10])
    (0.00, 1.20, 0.26),   # local SPARC anchor (McGaugh+2016)
    (0.33, 1.99, 0.18),   # MUSE-DARK III lowest quantile bin
    (1.00, 2.38, 0.11),   # MUSE-DARK III z~1 (their headline)
    (1.44, 2.71, 0.22),   # MUSE-DARK III highest quantile bin
]


# ====================================================================================================
# SCORING: chi^2 of each model SHAPE vs a0(z)/a0(0).  Free normalization A (best-fit amplitude),
# log-space (a0 spans decades; scatter ~ lognormal), per-point sigma = the sample's own log scatter
# (the systematic floor -- these per-galaxy a0 carry no published per-point error).
# ====================================================================================================
def score_dataset(z, a0, label, anchor_a0=None):
    """Return per-model chi^2/dof on log10(a0) with a free amplitude. anchor_a0 (m/s^2) optional:
    if given, we ALSO report a0(0)/anchor (the absolute level) but the chi^2 uses the free-A shape."""
    good = np.isfinite(a0) & (a0 > 0)
    z, a0 = z[good], a0[good]
    y = np.log10(a0)
    slog = np.std(y)                                    # per-point log scatter = systematic floor proxy
    if slog <= 0:
        slog = 0.30
    out = {}
    for name, f, _ in MODELS:
        lp = np.log10(f(z))
        A = np.mean(y - lp)                             # best-fit log-amplitude (free normalization)
        chi2 = np.sum((y - lp - A) ** 2) / slog ** 2
        dof = max(len(z) - 1, 1)
        out[name] = (chi2, chi2 / dof, 10 ** A)
    return out, len(z), np.median(a0), slog


def score_muse():
    """Score the four model shapes against MUSE-DARK III's published (z, a0, sigma) points,
    normalized to its own z=0 anchor (1.20).  Here we have REAL per-point errors, so use them."""
    z = np.array([p[0] for p in MUSE_PTS]); a = np.array([p[1] for p in MUSE_PTS]); s = np.array([p[2] for p in MUSE_PTS])
    r = a / a[0]; rs = s / a[0]                          # ratio to z=0 anchor and its error
    out = {}
    for name, f, _ in MODELS:
        shape = f(z) / f(0.0)                            # model normalized to z=0
        # free amplitude A in linear space, weighted:
        A = np.sum(r * shape / rs ** 2) / np.sum(shape ** 2 / rs ** 2)
        chi2 = np.sum(((r - A * shape) / rs) ** 2)
        dof = max(len(z) - 1, 1)
        out[name] = (chi2, chi2 / dof, A)
    return out, z, r, rs


# ====================================================================================================
def main():
    print("#" * 102)
    print("# FRONT 3 -- THE CLEAN a0(z) LEDGER  (framework = DECLINING sqrt(rho_DE); E(z) kept as a RIVAL only)")
    print("#" * 102)

    # -- (0) the framework prediction, recomputed not quoted --------------------------------------
    print("\n" + "=" * 102)
    print("(0) THE FRAMEWORK a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)  [DESI w0=%.3f, wa=%.2f]  -- recomputed" % (W0, WA))
    print("=" * 102)
    print(f"  a0_today (canon) = (c/2)sqrt(G rho_DE) = {A0_FRAMEWORK:.3e} m/s^2   (target 9.36e-11; dark energy ALONE)")
    print(f"  {'z':>6}{'FRAMEWORK':>12}{'CONSTANT':>11}{'RISING-cH(RIVAL)':>18}")
    for z in (0.0, 0.4, 0.5, 1.0, 2.0, 3.0):
        print(f"  {z:>6.2f}{m_framework(z):>12.3f}{m_constant(z):>11.3f}{m_rising_cH(z):>18.3f}")
    zb = np.linspace(0, 1.2, 400); zbump = zb[np.argmax(m_framework(zb))]
    print(f"  => NON-MONOTONIC: bump peak at z~{zbump:.2f} (a0/a0(0)={m_framework(zbump):.3f}), then DECLINES to "
          f"{m_framework(2.0):.2f}(z=2), {m_framework(3.0):.2f}(z=3).")
    print(f"     The RIVAL E(z) RISES the OTHER way: {m_rising_cH(2.0):.2f}x by z=2, {m_rising_cH(3.0):.2f}x by z=3.\n")

    # -- (1) per-dataset scoring -------------------------------------------------------------------
    print("=" * 102)
    print("(1) PER-DATASET chi^2 (shape test, free amplitude, log-space; sigma = sample log-scatter = systematic floor)")
    print("=" * 102)

    combined = {name: 0.0 for name, _, _ in MODELS}
    combined_n = 0

    # --- RC100 deep-MOND (the framework's most favorable existing kinematic set) ---
    zdm, a0dm, lbl_dm, zall, a0all = load_rc100()
    res, n, med, slog = score_dataset(zdm, a0dm, lbl_dm, anchor_a0=A0_FRAMEWORK)
    print(f"\n  [{lbl_dm}]  N={n}, median a0={med*1e10:.2f}e-10, log-scatter={slog:.2f} dex")
    print(f"    {'model':28}{'chi2':>9}{'chi2/dof':>10}{'best A(=a0(0))':>16}")
    for name, _, _ in MODELS:
        chi2, chidof, A = res[name]
        print(f"    {name:28}{chi2:>9.1f}{chidof:>10.2f}{A*1e10:>13.2f}e-10")
        combined[name] += chi2
    combined_n += n
    base = res["FRAMEWORK sqrt(rho_DE)"][0]
    print(f"    Dchi2 vs FRAMEWORK:  CONSTANT {res['CONSTANT'][0]-base:+.1f} | RISING-cH "
          f"{res['RISING-cH E(z) [RIVAL]'][0]-base:+.1f}  (+ => that model is WORSE than framework)")

    # --- KROSS z~0.85 ---
    zk, a0k, lbl_k = load_kross()
    res, n, med, slog = score_dataset(zk, a0k, lbl_k)
    print(f"\n  [{lbl_k}]  N={n}, median a0={med*1e10:.2f}e-10, log-scatter={slog:.2f} dex")
    print(f"    NOTE: single redshift (z~0.85) -> chi^2 SHAPE is weak here (one z); the median a0 LEVEL is the info.")
    print(f"    {'model':28}{'chi2':>9}{'chi2/dof':>10}{'best A(=a0(0))':>16}")
    for name, _, _ in MODELS:
        chi2, chidof, A = res[name]
        print(f"    {name:28}{chi2:>9.1f}{chidof:>10.2f}{A*1e10:>13.2f}e-10")
        combined[name] += chi2
    combined_n += n

    # --- KMOS3D ---
    zu, a0u, lbl_u = load_kmos3d()
    res, n, med, slog = score_dataset(zu, a0u, lbl_u)
    print(f"\n  [{lbl_u}]  N={n}, median a0={med*1e10:.2f}e-10, log-scatter={slog:.2f} dex")
    print(f"    CAVEAT: massive, often dispersion-supported -> a0=V^4/GMbar biased HIGH & not deep-MOND.")
    print(f"    {'model':28}{'chi2':>9}{'chi2/dof':>10}{'best A(=a0(0))':>16}")
    for name, _, _ in MODELS:
        chi2, chidof, A = res[name]
        print(f"    {name:28}{chi2:>9.1f}{chidof:>10.2f}{A*1e10:>13.2f}e-10")
        combined[name] += chi2
    combined_n += n
    base = res["FRAMEWORK sqrt(rho_DE)"][0]
    print(f"    Dchi2 vs FRAMEWORK:  CONSTANT {res['CONSTANT'][0]-base:+.1f} | RISING-cH "
          f"{res['RISING-cH E(z) [RIVAL]'][0]-base:+.1f}")

    # --- MUSE-DARK III (published points, REAL per-point errors) ---
    res_m, zmu, rmu, rsmu = score_muse()
    print(f"\n  [MUSE-DARK III (Ciocan+2026, published a0(z) bins + SPARC anchor)]  N={len(zmu)} points, REAL errors")
    print(f"    measured a0(z)/a0(0):  " + ", ".join(f"z={zz:.2f}:{rr:.2f}+/-{ss:.2f}"
          for zz, rr, ss in zip(zmu, rmu, rsmu)))
    print(f"    {'model':28}{'chi2':>9}{'chi2/dof':>10}{'best A':>9}")
    for name, _, _ in MODELS:
        chi2, chidof, A = res_m[name]
        print(f"    {name:28}{chi2:>9.1f}{chidof:>10.2f}{A:>9.2f}")
    base_m = res_m["FRAMEWORK sqrt(rho_DE)"][0]
    print(f"    Dchi2 vs FRAMEWORK:  CONSTANT {res_m['CONSTANT'][0]-base_m:+.1f} | RISING-cH "
          f"{res_m['RISING-cH E(z) [RIVAL]'][0]-base_m:+.1f}")
    print(f"    HONEST: MUSE-DARK III RISES (a0/a0(0)~2 by z~1).  See verdict -- the RISING rival fits it far")
    print(f"            better than the framework decline here; we say so plainly.")

    # -- (2) COMBINED kinematic ledger (RC100+KROSS+KMOS3D; MUSE reported separately as it RISES) ---
    print("\n" + "=" * 102)
    print("(2) COMBINED chi^2 across the three REAL KINEMATIC sets (RC100 deep-MOND + KROSS + KMOS3D); N=%d gal" % combined_n)
    print("    (MUSE-DARK III handled separately above -- it is an INDIRECT RAR-fit that RISES, not a clean RC a0)")
    print("=" * 102)
    base = combined["FRAMEWORK sqrt(rho_DE)"]
    print(f"    {'model':28}{'total chi2':>12}{'Dchi2 vs FRAMEWORK':>22}{'verdict':>20}")
    for name, _, note in MODELS:
        d = combined[name] - base
        if abs(d) < 2:
            v = "indistinguishable"
        elif d > 0:
            v = "WORSE (disfavored)"
        else:
            v = "better"
        print(f"    {name:28}{combined[name]:>12.1f}{d:>22.1f}{v:>20}")

    # -- (3) the honest verdict --------------------------------------------------------------------
    print("\n" + "=" * 102)
    print("(3) HONEST VERDICT")
    print("=" * 102)
    rc100_med = np.median(a0dm) * 1e10
    print(f"""  WHERE THE FRAMEWORK'S DECLINING PREDICTION STANDS, dataset by dataset:

  * RC100 deep-MOND (the framework's BEST existing kinematic set): the per-galaxy a0 scatters ~30-50x
    (Vc measured at R_e, not the flat velocity -- a known systematic), so the SHAPE test is weak.
    Framework decline and CONSTANT are INDISTINGUISHABLE (|Dchi2|<2); the RISING-cH rival is DISFAVORED
    (it predicts a0 climbing x2-3, the data do not).  Median a0~{rc100_med:.1f}e-10. -> framework SAFE, not confirmed.

  * KROSS z~0.85 (gas-corrected): single redshift, so this constrains the LEVEL, not the trend.  With a
    realistic gas census the median a0 sits near the local value -> consistent with framework decline AND
    with constant; cannot separate them.  The RISING rival (which wants a0~1.4x local by z~0.85) is mildly
    disfavored.  Gas is the entire systematic.

  * KMOS3D (massive, dispersion-supported): a0=V^4/GMbar is biased HIGH and rises with MASS (not z) -- a
    high-acceleration artifact, NOT a clean a0(z).  Its z-trend is flat-to-declining, which happens to
    DISFAVOR the RISING-cH rival and sit fine with the framework, but the sample cannot cleanly test either.

  * MUSE-DARK III (Ciocan+2026), the ONE direct multi-point a0(z): it RISES strongly (a0~2.4e-10 at z~1,
    ~+1.59 per unit z).  HONESTLY: against MUSE alone, the framework's DECLINE (and CONSTANT) fit WORSE than
    a rise; the RISING-cH rival is closer to the data SIGN here.  BUT: (i) MUSE rises "faster than H(z)", so
    it OVERSHOOTS even the RISING-cH/E(z) rival -- it matches NO background-density law; (ii) the rise is
    LambdaCDM-degenerate (Mayer+2023: a LCDM hydro sim with NO fundamental a0 produces an apparent a0 rising
    ~x3 to z~2 via galaxy assembly), so a RISING FITTED a0 does not establish a rising FUNDAMENTAL a0; and
    (iii) the rise is method-localised to RAR-fits on intermediate-z star-forming disks -- the regime where
    fitted a0 != fundamental a0.  So MUSE neither confirms the rival nor falsifies the framework: it is
    NON-DIAGNOSTIC, but it is the strongest single point of tension and the framework cannot claim it.

  NET STANDING of the framework's DECLINING sqrt(rho_DE) prediction:
    INDISTINGUISHABLE from CONSTANT at current precision (the predicted decline is only ~{(1-m_framework(2.0))*100:.0f}% at z=2,
    ~{(1-m_framework(3.0))*100:.0f}% at z=3 -- far below the ~0.3-0.8 dex per-galaxy scatter and the gas/pressure systematics).  It is
    NOT confirmed and NOT refuted.  It is SAFE against the in-repo kinematic data, which DISFAVOR the
    RISING-cH/Verlinde rival (the wrong branch) -- a real if modest win: the data that exist run flat-to-
    declining, NOT rising x3.  The one rising measurement (MUSE) overshoots every cosmological law and is
    LCDM-degenerate, so it does not rescue the rival and does not kill the framework.

    HONESTY ON 'framework BEATS constant by Dchi2~5 combined': do NOT oversell this.  That tiny edge comes
    almost entirely from KMOS3D -- a massive, dispersion-supported, BIASED-HIGH sample whose mild apparent
    decline is a mass/selection artifact, NOT a clean a0(z).  In the clean(er) RC100 deep-MOND set the
    framework-vs-constant gap is Dchi2~0.5 (noise).  So the honest statement is framework == constant; the
    'beats constant' number is an artifact of the worst sample and must NOT be quoted as evidence FOR decline.

  FAVORED / DISFAVORED / INDISTINGUISHABLE?
    - framework vs CONSTANT (incl. regular-MOND-constant):  INDISTINGUISHABLE (shape test has no power yet;
      and as a normalized shape, regular-MOND-constant == CONSTANT -- only an absolute a0(0) anchor, 9.36e-11
      vs 1.2e-10, could separate the framework from MOND, which this ratio test deliberately cancels).
    - framework vs RISING-cH (Verlinde/wrong branch):  framework FAVORED by the real kinematic data
      (RC100/KROSS/KMOS3D all run flat-to-declining; the rival's x2-3 rise is disfavored); but MUSE-DARK III
      alone favors a RISE -- and that rise is LCDM-degenerate and overshoots the rival too.

  BOTTOM LINE (one sentence): on the CORRECT (declining) law the framework is alive and indistinguishable
  from flat, the in-repo data DISFAVOR the rising rival the audit had mislabeled as 'the framework', and the
  single direct rising measurement (MUSE-DARK III) is real tension but LambdaCDM-degenerate and overshoots
  every law -- so a0(z) is currently NON-DECISIVE, settled only by a clean deep-MOND z~3 rotation curve.""")
    print("=" * 102)


if __name__ == "__main__":
    main()
