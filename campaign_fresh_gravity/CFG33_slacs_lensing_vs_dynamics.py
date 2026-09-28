#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG33 -- THE SLACS EINSTEIN RADII UNDER CANDIDATE B: is B7 ("14-18% short") a failure of B's law, or the heavier stellar IMF that
B's own dynamics need anyway?  A lensing-versus-dynamics consistency test inside B.

WHY.  B7: under the law, 70 SLACS lenses (Auger+2009) get only 79-85% of their Einstein mass at a Salpeter IMF and 49-54% at Chabrier
(hunt_2026/h53_h54_slacs_lenses.py); the predicted Einstein radius is 14-18% short.  At the Einstein radius (~4 kpc) g_N ~ 10 a0,
deep in the kernel's Newtonian part, so the phantom adds only 14-20%.  B's prediction here IS the law: T5 makes galaxies phantom-
dominated (CFG32 H3: the cluster max rule applied at each radius over-predicts an elliptical's inner mass several-fold) and ownership
gives no external field.  h53 itself called the result "a liability AT the level of the stellar-mass systematic, NOT a clean kill":
the shortfall is 0.07-0.10 dex at Salpeter, and the IMF of massive ellipticals is uncertain at that level.  So the question is not
whether a Salpeter IMF fits.  It is whether the IMF the lenses need under B equals the IMF B's own law needs to fit the DYNAMICS of the
same kind of galaxy at the same velocity dispersion.  B treats Upsilon as a nuisance of the data -- one nuisance per population, not
one per probe.

THE TEST (declared before this script's first run)
  lensing   alpha_lens, relative to Auger's Salpeter stellar masses: per lens, the normalisation at which B's law gives mean
            convergence 1 at the observed Einstein radius, alpha f_*,Salp B(alpha M_Salp) = 1 -- h53's machinery exec'd read-only (de
            Vaucouleurs stars, the law's projected phantom, Auger's measured f_*), the kernel nu_mono, both bands (V, I) for R_e.
  dynamics  alpha_dyn, relative to ATLAS3D's Salpeter population M/L: per early type, the stellar mass at which B's law reproduces the
            published JAM mass inside the half-light sphere, M_JAM = nu(g_N(r_1/2)/a0) M_*, g_N = G (M_*/2) / r_1/2^2 (h9's
            convention, M_JAM ~ 2 M_1/2), JAM quality >= 1.
  match     log alpha_dyn fitted linearly in log sigma_e over ATLAS3D and evaluated at each lens's dispersion; the statistic is the
            median over lenses of log alpha_lens - log alpha_dyn(sigma), bootstrap error (lenses and ATLAS3D resampled, the fit redone).
  floor     0.10 dex, declared up front: two stellar-population libraries, two bands and two IMF implementations (Auger's and
            ATLAS3D's Salpeter zero points are not the same number), plus the SDSS-fibre vs sigma_e aperture difference.

PRE-DECLARED
  C1  CONTROL  h53's committed Salpeter kappa_bar (canonical 0.825 V / 0.794 I; alt 0.854 / 0.812) reproduced with its own kernel.
  C2  CONTROL  h9's ATLAS3D sample rebuilt (258 galaxies) and its Wolf / JAM ratio reproduced (+0.21 dex).
  H1  B's KERNEL KEEPS THE RECORDED SHORTFALL: with nu_mono, kappa_bar at Salpeter < 0.90 in both bands, both footings.
  H2  [HEADLINE; MUTATE must fail] LENSING AND DYNAMICS AGREE UNDER B's LAW: |median log(alpha_lens / alpha_dyn(sigma))| < 2 sigma
      (bootstrap error and the 0.10-dex floor in quadrature), both bands, both footings.
  H3  B's DYNAMICS NEED AN IMF THAT GROWS WITH DISPERSION: over ATLAS3D, d log alpha_dyn / d log sigma_e > 0 at > 3 sigma (bootstrap),
      canonical.
  R1-R4 (reported): H2 without the floor; alpha_lens and alpha_dyn in dispersion bins; the Chabrier-equivalent normalisations; the P2
      kernel; the lenses' own slope.
  READING (declared): H2 PASS -> B7 is not a failure of B: the lenses need the stellar mass B's law needs for the dynamics of galaxies
  of the same dispersion, and the shortfall at a fixed Salpeter IMF was the IMF, not the law.  H2 FAIL -> B fails the lensing-dynamics
  consistency: at the same dispersion its lenses need a different stellar mass than its dynamics.
MUTATE=1: every Einstein mass doubled (f_* halved) -- H2 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG33_slacs_lensing_vs_dynamics.py   (MUTATE=1 for the control; ~1-2 min)
"""
import os, sys, math, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG33_slacs_lensing_vs_dynamics", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every Einstein mass doubled (f_* halved) -- H2 must FAIL ***")
FMUT = 0.5 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
BANDS = ("V", "I")
FLOOR = 0.10

HUNT = os.path.join(C.REPO, "hunt_2026")
sys.path.insert(0, HUNT)
# ------------------------------------------------------------------------------------------------ h53, exec'd read-only (its own kernel)
H53P = os.path.join(HUNT, "h53_h54_slacs_lenses.py")
g53, _ = C4.exec_slices(H53P, [(None, 'P(""); P("="*118); P("ITEM 53')], name="h53_prefix")
S, boost, R54 = g53["S"], g53["boost"], g53["R54"]
MSUN, KPC, A0H = g53["Msun"], g53["kpc"], g53["A0"]
P(f"\n  h53's lenses (exec'd read-only): {len(S)}; median sigma {np.median([d['sig'] for d in S]):.0f} km/s")

# ================================================================================================ C1
R.banner("C1  CONTROL: h53's committed Salpeter kappa_bar (its own kernel, nu_RAR)")
o53 = open(os.path.join(HUNT, "h53_h54_slacs_lenses.out")).read()
com = {}
for f in FOOTS:
    m_ = re.search(rf"{f}\s+g_N\(R_E\)/a_0 =.*?SALPETER ([0-9.]+) / ([0-9.]+)", o53)
    com[f] = (float(m_.group(1)), float(m_.group(2)))
dev1 = max(abs(round(R54[(f, b)][1], 3) - com[f][i]) for f in FOOTS for i, b in enumerate(BANDS))
check("C1 CONTROL: h53's committed Salpeter kappa_bar reproduced (both footings, both bands)",
      "; ".join(f"{f}: V {R54[(f, 'V')][1]:.4f} / I {R54[(f, 'I')][1]:.4f} (committed {com[f][0]:.3f} / {com[f][1]:.3f})" for f in FOOTS), dev1 <= 1e-9)

# ------------------------------------------------------------------------------------------------ B's kernel in h53's machinery
KERN = {"nu_mono": C.nu_mono, "P2": C.nu_p2}
A0B = C.A0_SI


def lens_alpha(kern, a0, band, fmut=FMUT):
    """per lens: kappa_bar at Salpeter and the normalisation alpha (vs Auger's Salpeter mass) that makes it 1, under B's law."""
    g53["nu"] = KERN[kern]
    kap, alp = [], []
    for d in S:
        Ms = 10 ** d["lMs"] * MSUN; fs = d["Fs"] * fmut; Re = d["Re_" + band]; Rm = d["RE"] * KPC
        kap.append(fs * boost(Ms, Re, a0, Rm))
        a = 1.0 / kap[-1]
        for _ in range(8):
            a = 1.0 / (fs * boost(a * Ms, Re, a0, Rm))
        alp.append(a)
    return np.array(kap), np.array(alp)


LENS = {}
for f in FOOTS:
    for b in BANDS:
        LENS[(f, b)] = lens_alpha("nu_mono", A0B[f], b)
SIG_L = np.array([d["sig"] for d in S])

# ================================================================================================ C2 ATLAS3D
R.banner("C2  CONTROL: h9's ATLAS3D sample and its Wolf / JAM calibration")
rw = [l.rstrip("\n").split("\t") for l in open(os.path.join(C.REPO, "real_research", "data", "atlas3d_fj_table.tsv")) if l.strip() and not l.startswith("#")]
ah = {h: i for i, h in enumerate(rw[0])}


def fl(s):
    try:
        return float(s)
    except Exception:
        return float("nan")


ARCSEC = 1 / 206264.806
ET = []
for d in rw[1:]:
    e = dict(name=d[ah["name"]], lsig=fl(d[ah["logsig_e"]]), lmljam=fl(d[ah["logML_JAM"]]), qual=fl(d[ah["qual"]]), lr12=fl(d[ah["logr12"]]),
             lL=fl(d[ah["logL"]]), lmlsalp=fl(d[ah["logML_Salp"]]), D=fl(d[ah["Dist_Mpc"]]))
    if not all(np.isfinite(e[k]) for k in ("D", "lsig", "lmlsalp", "lr12", "lL", "lmljam")):
        continue
    e["r12"] = 10 ** e["lr12"] * ARCSEC * e["D"] * 1e3
    e["sig"] = 10 ** e["lsig"] * 1e3
    e["Msalp"] = 10 ** (e["lmlsalp"] + e["lL"])
    e["Mjam"] = 10 ** (e["lmljam"] + e["lL"])
    ET.append(e)
G_ = g53["G"]
wolf = np.array([3 * e["sig"] ** 2 * (e["r12"] * KPC) / G_ / MSUN for e in ET]) / (0.5 * np.array([e["Mjam"] for e in ET]))
o9 = open(os.path.join(HUNT, "h9_h11_pressure_supported.out")).read()
n9 = int(re.search(r"(\d+) ATLAS3D early-type galaxies with sigma_e", o9).group(1))
w9 = float(re.search(r"it runs ([0-9.]+) dex \(a factor", o9).group(1))
check("C2 CONTROL: h9's ATLAS3D sample rebuilt and its Wolf / JAM ratio reproduced",
      f"N = {len(ET)} (h9 {n9}); median log M_Wolf/(M_JAM/2) {math.log10(np.median(wolf)):+.3f} dex (h9 +{w9:.2f})",
      len(ET) == n9 and abs(math.log10(np.median(wolf)) - w9) < 0.005)
Q = np.array([e["qual"] for e in ET]) >= 1
LSIG_A = np.array([e["lsig"] for e in ET])


def dyn_alpha(kern, a0):
    out = []
    for e in ET:
        M = e["Mjam"]
        for _ in range(60):
            gN = G_ * (M / 2) * MSUN / (e["r12"] * KPC) ** 2
            M = e["Mjam"] / float(KERN[kern](np.array([gN / a0]))[0])
        out.append(M / e["Msalp"])
    return np.array(out)


DYN = {f: dyn_alpha("nu_mono", A0B[f]) for f in FOOTS}

# ================================================================================================ H1
R.banner("H1  B's KERNEL ON THE RECORDED SHORTFALL (Salpeter kappa_bar, nu_mono)")
kmed = {(f, b): float(np.median(LENS[(f, b)][0])) for f in FOOTS for b in BANDS}
check("H1 B's KERNEL KEEPS THE RECORDED SHORTFALL: kappa_bar at Salpeter < 0.90 in both bands, both footings (nu_mono)",
      "; ".join(f"{f} {b}: {kmed[(f, b)]:.3f}" for f in FOOTS for b in BANDS), all(v < 0.90 for v in kmed.values()))

# ================================================================================================ H2 / H3
R.banner("H2 / H3  LENSING AGAINST DYNAMICS UNDER B's LAW, matched in velocity dispersion")
rng = np.random.default_rng(33)
LSIG_L = np.log10(SIG_L)
PIV = 2.3


def fit(lsig, la):
    b_, a_ = np.polyfit(lsig - PIV, la, 1)
    return a_, b_


def stat(alp_l, alp_d, idx_l=None, idx_d=None):
    il = np.arange(len(alp_l)) if idx_l is None else idx_l
    idd = np.where(Q)[0] if idx_d is None else idx_d
    a_, b_ = fit(LSIG_A[idd], np.log10(alp_d[idd]))
    return float(np.median(np.log10(alp_l[il]) - (a_ + b_ * (LSIG_L[il] - PIV)))), b_


RES = {}
for f in FOOTS:
    ad = DYN[f]
    qidx = np.where(Q)[0]
    for b in BANDS:
        al = LENS[(f, b)][1]
        d0, slope0 = stat(al, ad)
        bs = [stat(al, ad, rng.integers(0, len(al), len(al)), rng.choice(qidx, len(qidx)))[0] for _ in range(2000)]
        err = float(np.std(bs))
        tot = math.hypot(err, FLOOR)
        RES[(f, b)] = dict(delta=d0, err=err, tot=tot, z=d0 / tot, z_nofloor=d0 / err, lens_med=float(np.median(np.log10(al))),
                           dyn_at_lens=float(np.median(fit(LSIG_A[qidx], np.log10(ad[qidx]))[0] + fit(LSIG_A[qidx], np.log10(ad[qidx]))[1] * (LSIG_L - PIV))))
        P(f"    {f:9s} {b}: median log alpha_lens {RES[(f, b)]['lens_med']:+.3f} (x{10 ** RES[(f, b)]['lens_med']:.2f} Salpeter); alpha_dyn at the lenses' "
          f"dispersions {RES[(f, b)]['dyn_at_lens']:+.3f} (x{10 ** RES[(f, b)]['dyn_at_lens']:.2f}); difference {d0:+.3f} +- {err:.3f} (stat) -> "
          f"{RES[(f, b)]['z']:+.2f} sigma with the {FLOOR} dex floor ({RES[(f, b)]['z_nofloor']:+.1f} without)")
check("H2 [HEADLINE] LENSING AND DYNAMICS AGREE UNDER B's LAW: the lenses' stellar-mass normalisation equals the dynamics' at the same "
      "dispersion within 2 sigma (bootstrap + the 0.10-dex floor), both bands, both footings" + ("  [MUTATE: Einstein masses doubled]" if MUTATE else ""),
      "; ".join(f"{f} {b}: {v['delta']:+.3f} +- {v['tot']:.3f} dex ({v['z']:+.2f} sigma)" for (f, b), v in RES.items()),
      all(abs(v["z"]) < 2 for v in RES.values()))
qidx = np.where(Q)[0]
sl = [fit(LSIG_A[i_], np.log10(DYN["canonical"][i_]))[1] for i_ in (rng.choice(qidx, len(qidx)) for _ in range(2000))]
sl0 = fit(LSIG_A[qidx], np.log10(DYN["canonical"][qidx]))[1]
check("H3 B's DYNAMICS NEED AN IMF THAT GROWS WITH DISPERSION: d log alpha_dyn / d log sigma_e > 0 at > 3 sigma over ATLAS3D (canonical)",
      f"slope {sl0:+.3f} +- {np.std(sl):.3f} ({sl0 / np.std(sl):+.1f} sigma); alpha_dyn at sigma = 100 / 200 / 300 km/s: "
      + " / ".join(f"x{10 ** (fit(LSIG_A[qidx], np.log10(DYN['canonical'][qidx]))[0] + sl0 * (math.log10(s_) - PIV)):.2f}" for s_ in (100, 200, 300)),
      sl0 / np.std(sl) > 3)

# ================================================================================================ reported
R.banner("R1-R4  REPORTED")
bins = [(2.20, 2.35), (2.35, 2.45), (2.45, 2.60)]
rows = []
for lo, hi in bins:
    ml = (LSIG_L >= lo) & (LSIG_L < hi); md = Q & (LSIG_A >= lo) & (LSIG_A < hi)
    rows.append(f"log sigma {lo:.2f}-{hi:.2f}: lenses {int(ml.sum())} x{10 ** np.median(np.log10(LENS[('canonical', 'V')][1][ml])):.2f}, "
                f"ATLAS3D {int(md.sum())} x{10 ** np.median(np.log10(DYN['canonical'][md])):.2f}" if ml.sum() and md.sum() else f"log sigma {lo:.2f}-{hi:.2f}: too few")
check("R1 (reported) alpha_lens and alpha_dyn in dispersion bins (canonical, V; relative to each survey's Salpeter)", "; ".join(rows), True, load_bearing=False)
check("R2 (reported) the same statistic without the declared floor (statistical only)",
      "; ".join(f"{f} {b}: {v['z_nofloor']:+.1f} sigma" for (f, b), v in RES.items()), True, load_bearing=False)
LP2 = lens_alpha("P2", A0B["canonical"], "V"); DP2 = dyn_alpha("P2", A0B["canonical"])
d_p2 = stat(LP2[1], DP2)[0]
check("R3 (reported) the P2 kernel (canonical, V)", f"kappa_bar at Salpeter {np.median(LP2[0]):.3f}; difference {d_p2:+.3f} dex", True, load_bearing=False)
ls_slope = float(np.polyfit(LSIG_L - PIV, np.log10(LENS[("canonical", "V")][1]), 1)[0])
check("R4 (reported) the lenses' own slope d log alpha_lens / d log sigma (canonical, V); Chabrier-equivalent normalisations (x 10^0.25)",
      f"lens slope {ls_slope:+.2f} over log sigma {LSIG_L.min():.2f}-{LSIG_L.max():.2f}; median alpha_lens x{10 ** RES[('canonical', 'V')]['lens_med']:.2f} Salpeter "
      f"= x{10 ** (RES[('canonical', 'V')]['lens_med'] + 0.25):.2f} Chabrier-like", True, load_bearing=False)

h2 = all(abs(v["z"]) < 2 for v in RES.values())
reading = ("B7 is not a failure of B: the lenses need the stellar mass B's law needs for the dynamics of galaxies of the same dispersion; the "
           "shortfall at a fixed Salpeter IMF was the IMF, not the law" if h2 else
           "B fails the lensing-dynamics consistency: at the same dispersion its lenses need a different stellar mass than its dynamics")
P(f"\n    READING (declared): {reading}")
R.num("C1", dict(committed=com, mine={f"{f}|{b}": R54[(f, b)][1] for f in FOOTS for b in BANDS}))
R.num("H1", {f"{f}|{b}": v for (f, b), v in kmed.items()})
R.num("H2", {f"{f}|{b}": v for (f, b), v in RES.items()})
R.num("H3", dict(slope=sl0, err=float(np.std(sl))))
R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
