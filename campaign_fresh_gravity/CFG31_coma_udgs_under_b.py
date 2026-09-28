#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG31 -- THE COMA ULTRA-DIFFUSE GALAXIES UNDER CANDIDATE B: is the recorded 4.9-sigma liability (B2) a failure of B, or of the
external-field reading that B dropped?

WHY.  FAILURES_EXECUTIVE_SUMMARY_2026-09-28 row B2: eleven Coma UDGs (Freundlich+2022; dispersions from Chilingarian+2019, DF44 and
DFX1 from van Dokkum+) sit +1.16 dex (canonical) / +1.11 (alt) in acceleration ABOVE the framework's external-field prediction --
4.9 / 4.7 sigma with L23's systematic floor (fable_independent_2026/L23_udg_verify.py).  That prediction applied Coma's external field.
Candidate B does not: under FG001's ownership a UDG that fell into Coma is ACCRETED, and an accreted system obeys the ISOLATED law of
its INFALL baryons (class A -- the rule CFG18 applied to the Local Group's satellites, where it removed the M31 tension).  L23 already
computed the isolated offset with stars only: +0.397 / +0.357 dex, statistical error only.  So this lane is a RE-SCORING under B's own
rule, not a blind test: the stars-only number was known; the infall-gas number and the recomputed floor were not.

THE METHOD (declared before this script's first run)
  * Data and estimator: L23's, exec'd read-only (the 11 UDGs rebuilt from L, M/L, R_e and sigma; r_1/2 = 4 R_e/3; g_obs = 3 sigma^2 /
    r_1/2; g_bar = G (M_b/2) / r_1/2^2; the per-galaxy errors and the inverse-variance weighted mean exactly as L23 carried them).
    This is FG001's own convention for accreted systems (sigma_pred = sqrt(nu g_N r_1/2 / 3)), so the offsets below are B's.
  * B's prediction: the isolated law, no external field, kernel nu_mono (the contract kernel; P2 reported); both a0 footings.
  * Infall baryons: M_* + the infall gas, the gas-to-star ratio drawn per galaxy from its 5 nearest members of CFG18's calibration set
    (the 42 LVD field dwarfs, M_* = 2.0 L_V, gas = 1.33 M_HI) in log M_*, uniformly; HI non-detections as ZERO gas (the headline,
    CFG18's conservative bracket) or at their upper limits (reported).  The gas follows the stars (half inside r_1/2), as in FG001 and
    CFG18.  2000 realisations (seed 31).
  * The systematic floor, recomputed for the isolated law by re-running the pipeline on L23's entries: stellar M/L (x 1.41), aperture
    + anisotropy (L23's 0.12), the instrumental term (L23's formula, 9 of 11), the Wolf-vs-virial estimator, the distance (+-5%).  The
    external-field entries (the Coma mass model and the 3-D position) do not apply and are dropped; the footings are reported
    separately.  The spread over realisations is added in quadrature.

PRE-DECLARED
  C1  CONTROL  L23's committed isolated offsets (nu_RAR, stars only) reproduced: +0.3965 canonical, +0.357 alt.
  C2  CONTROL  CFG18's calibration set rebuilt: 42 dwarfs, 32 HI detections, log M_* 4.98-9.65.
  H1  [HEADLINE; MUTATE must fail] UNDER CANDIDATE B THE COMA UDGs ARE NOT A 2-SIGMA FAILURE: with the isolated law, no external field
      and the infall baryons (non-detections as zero), the weighted-mean offset lies within 2 sigma of the total error (statistical +
      the recomputed floor + the realisation spread), both footings.
  H2  DF44 ALONE (33 hr of Keck/KCWI, the best-measured UDG) lies within 2 sigma under the same prediction (its own error + the
      per-object floor: M/L, aperture, estimator, distance).
  H3  THE ACCRETED CLASS IS ONE CLASS: the UDGs' offset in dispersion (half the acceleration offset) agrees with CFG18's M31 LVD
      dwarfs under the same rule (+0.078 / +0.060 dex in sigma) within 2 sigma combined, both footings.
  R1-R7 (reported): stars only (the current baryons); non-detections at their limits; the P2 kernel; the Milgrom-1994 virial
      estimator; the Chilingarian nine against the Keck two; the infall gas-to-star ratio that would null the offset, against the
      calibration dwarfs at the UDGs' masses; the external-field rival for comparison (L23: +1.159 / +1.112 dex, 4.9 / 4.7 sigma).
  READING (declared): H1 PASS -> the 4.9-sigma Coma liability belongs to the external-field reading, not to candidate B.  H1 FAIL ->
  the Coma UDGs remain a failure of B even under its own rule.
MUTATE=1: every dispersion doubled (g_obs x 4) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG31_coma_udgs_under_b.py   (MUTATE=1 for the control; ~10 s)
"""
import os, sys, math, json, csv, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG31_coma_udgs_under_b", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every dispersion doubled -- H1 must FAIL ***")
SIGF = 2.0 if MUTATE else 1.0
FOOTS = ("canonical", "alt")

# ------------------------------------------------------------------------------------------------ L23, exec'd read-only
L23P = os.path.join(C.REPO, "fable_independent_2026", "L23_udg_verify.py")
g23, _ = C4.exec_slices(L23P, [(None, 'H("2. CONTROL A')], name="l23_prefix")
UDG, A0L, nus_L, wmean, G_, MSUN = g23["UDG"], g23["A0_H9"], g23["nus"], g23["wmean"], g23["G"], g23["MSUN"]  # L23 printed its isolated lines with h9's a0
NAMES = [u["name"] for u in UDG]
MST = np.array([u["Mst"] for u in UDG]); R12 = np.array([u["r12"] for u in UDG])
GOBS0 = np.array([u["gobs"] for u in UDG]); ERR = np.array([u["err"] for u in UDG]); SIG = np.array([u["sig"] for u in UDG])
W = 1.0 / ERR ** 2
STAT = float(1.0 / math.sqrt(W.sum()))
A0B = C.A0_SI                                                                        # the campaign's footings
KERN = {"nu_mono": C.nu_mono, "P2": C.nu_p2}
P(f"\n  L23's sample (exec'd read-only): {len(UDG)} Coma UDGs ({', '.join(NAMES)}); statistical error on the weighted mean {STAT:.3f} dex")


def offsets(a0, kern="nu_mono", ratio=None, ml=1.0, dist=1.0, sigf=SIGF, estimator="wolf"):
    """log10(g_obs / g_pred) per galaxy, dex in acceleration; ratio = infall gas-to-star ratio, shape (n,) or (N, n)."""
    rat = np.zeros(len(UDG)) if ratio is None else np.asarray(ratio, float)
    mb = MST * ml * (1.0 + rat)
    gobs = GOBS0 * sigf ** 2 / dist
    if estimator == "wolf":
        gb = G_ * (mb / 2.0) / R12 ** 2
        gp = KERN[kern](gb / a0) * gb
    else:                                                                        # Milgrom 1994: sigma^4 = (4/81) G M_b a0
        gp = 3.0 * np.sqrt((4.0 / 81.0) * G_ * mb * a0) / R12
    return np.log10(gobs) - np.log10(gp)


def wm(off):
    off = np.asarray(off, float)
    return np.sum(W * off, axis=-1) / W.sum()


# ================================================================================================ C1
R.banner("C1  CONTROL: L23's committed isolated offsets (nu_RAR, stars only)")
o23 = open(os.path.join(C.REPO, "fable_independent_2026", "L23_udg_verify.out")).read()
c_can = float(re.search(r"canonical isolated ([+-][0-9.]+)", o23).group(1))
c_alt = float(re.search(r"alt\s+ISOLATED ([+-][0-9.]+)", o23).group(1))
mine = {}
for f in FOOTS:
    off = [math.log10(u["gobs"]) - math.log10(nus_L(u["gbar"] / A0L[f]) * u["gbar"]) for u in UDG]
    mine[f] = wmean(off, ERR)[0]
dev1 = max(abs(mine["canonical"] - c_can), abs(mine["alt"] - c_alt))
check("C1 CONTROL: L23's committed isolated offsets (nu_RAR, stars only, at h9's a0 as L23 printed them) reproduced",
      f"canonical {mine['canonical']:+.4f} (committed {c_can:+.4f}); alt {mine['alt']:+.4f} (committed {c_alt:+.3f})", dev1 <= 6e-4)

# ================================================================================================ C2 the calibration set
R.banner("C2  CONTROL: CFG18's calibration set (LVD field dwarfs)")
UPS_V = 2.0


def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


CAL = []
for r in csv.DictReader(open(os.path.join(C.REPO, "real_research", "data", "dsph", "lvd_dwarf_local_field.csv"))):
    MV = fnum(r["M_V"]); mh = fnum(r["mass_HI"]); ul = fnum(r["mass_HI_ul"])
    if MV is None or (mh is None and ul is None):
        continue
    ms = UPS_V * 10 ** (0.4 * (4.83 - MV)); det = mh is not None
    CAL.append((math.log10(ms), 1.33 * 10 ** (mh if det else ul) / ms, det))
CAL.sort()
LCAL = np.array([c[0] for c in CAL]); RAT = np.array([c[1] for c in CAL]); DET = np.array([c[2] for c in CAL])
C18 = json.load(open(os.path.join(HERE, "CFG18_satellite_infall_gas_results.json")))["numbers"]
cal18 = C18["calibration"]
ok2 = len(CAL) == cal18["n"] and int(DET.sum()) == cal18["n_det"] and abs(LCAL.min() - cal18["logMs_range"][0]) < 1e-9 and \
    abs(LCAL.max() - cal18["logMs_range"][1]) < 1e-9
LMU = np.log10(MST / MSUN)
check("C2 CONTROL: CFG18's calibration set rebuilt exactly (count, detections, stellar-mass range)",
      f"{len(CAL)} dwarfs, {int(DET.sum())} detections, log M_* {LCAL.min():.2f}-{LCAL.max():.2f} (CFG18: {cal18['n']}, {cal18['n_det']}, "
      f"{cal18['logMs_range'][0]:.2f}-{cal18['logMs_range'][1]:.2f}); the UDGs' log M_* {LMU.min():.2f}-{LMU.max():.2f} lie inside", ok2
      and LMU.min() >= LCAL.min() and LMU.max() <= LCAL.max())

K, NREAL = 5, 2000


def draws(bracket, seed=31):
    rng = np.random.default_rng(seed)
    out = np.zeros((NREAL, len(UDG)))
    for j, lm in enumerate(LMU):
        nn = np.argsort(np.abs(LCAL - lm))[:K]
        r_ = np.where(DET[nn], RAT[nn], RAT[nn] if bracket == "limit" else 0.0)
        out[:, j] = r_[rng.integers(0, K, NREAL)]
    return out


RZ, RL = draws("zero"), draws("limit")
for j, n_ in enumerate(NAMES):
    nn = np.argsort(np.abs(LCAL - LMU[j]))[:K]
    P(f"    {n_:18s} log M_* {LMU[j]:.2f}: the 5 nearest calibration dwarfs' gas/star " + ", ".join(
        f"{RAT[i]:.2f}{'' if DET[i] else ' (limit)'}" for i in nn))

# ================================================================================================ the floor for the isolated law
R.banner("THE SYSTEMATIC FLOOR, recomputed for the isolated law")
FLOOR = {}
for f in FOOTS:
    a0 = A0B[f]
    base = wm(offsets(a0))
    sysd = {"stellar M/L and IMF (x 1.41)": abs(wm(offsets(a0, ml=1.41)) - base),
            "aperture + orbital anisotropy on sigma_eff (L23's carried value)": 0.12}
    sig_inst = 2.99792458e5 / (4800 * 2.3548)
    prop = [(sig_inst / u["sig"]) ** 2 * 0.05 for u in UDG if u["name"] not in ("DF44", "DFX1")]
    sysd["velocity-dispersion instrumental term (9 of 11)"] = float(2 * np.median(prop) / math.log(10)) * (9 / 11.)
    s_wolf = np.sqrt(KERN["nu_mono"](G_ * (MST / 2) / R12 ** 2 / a0) * G_ * (MST / 2) / R12 ** 2 * R12 / 3.0)
    s_vir = ((4 / 81.) * G_ * MST * a0) ** 0.25
    rr = 2 * np.log10(s_wolf / s_vir)
    sysd["sigma -> acceleration estimator (Wolf vs Milgrom virial)"] = float(np.std(rr) + abs(np.mean(rr)))
    sysd["distance to Coma (+-5%)"] = abs(wm(offsets(a0, dist=1.05)) - base)
    FLOOR[f] = dict(entries=sysd, total=float(math.sqrt(sum(v ** 2 for v in sysd.values()))))
    P(f"    {f:9s}: " + "; ".join(f"{k} {v:.3f}" for k, v in sysd.items()) + f"  ->  floor {FLOOR[f]['total']:.3f} dex "
      f"(L23's EFE-reading floor 0.227)")

# ================================================================================================ H1
R.banner("H1  THE COMA UDGs UNDER CANDIDATE B: the isolated law of their infall baryons")
RES = {}
for f in FOOTS:
    a0 = A0B[f]
    for lab, rat in (("stars only", None), ("infall gas, non-detections zero", RZ), ("infall gas, non-detections at limit", RL)):
        if rat is None:
            m_ = np.array([wm(offsets(a0))]); spread = 0.0
        else:
            m_ = wm(offsets(a0, ratio=rat)); spread = float(np.std(m_))
        tot = math.sqrt(STAT ** 2 + FLOOR[f]["total"] ** 2 + spread ** 2)
        RES[(f, lab)] = dict(mean=float(m_.mean()), p16=float(np.percentile(m_, 16)), p84=float(np.percentile(m_, 84)), spread=spread,
                             tot=tot, z=float(m_.mean() / tot))
        v = RES[(f, lab)]
        P(f"    {f:9s} {lab:36s}: offset {v['mean']:+.3f} dex (68% {v['p16']:+.3f}..{v['p84']:+.3f}) +- {v['tot']:.3f} -> {v['z']:+.2f} sigma")
h1 = all(abs(RES[(f, "infall gas, non-detections zero")]["z"]) < 2.0 for f in FOOTS)
check("H1 [HEADLINE] UNDER CANDIDATE B THE COMA UDGs ARE NOT A 2-SIGMA FAILURE: the isolated law, no external field, the infall baryons "
      "(non-detections as zero) -- within 2 sigma of the total error, both footings" + ("  [MUTATE: dispersions doubled]" if MUTATE else ""),
      "; ".join(f"{f}: {RES[(f, 'infall gas, non-detections zero')]['mean']:+.3f} +- {RES[(f, 'infall gas, non-detections zero')]['tot']:.3f} dex "
                f"({RES[(f, 'infall gas, non-detections zero')]['z']:+.2f} sigma)" for f in FOOTS), h1)

# ================================================================================================ H2 DF44
R.banner("H2  DF44 ALONE")
jd = NAMES.index("DF44")
H2 = {}
for f in FOOTS:
    a0 = A0B[f]
    od = offsets(a0, ratio=RZ)[:, jd]
    fl = FLOOR[f]["entries"]
    per_ml = abs(offsets(a0, ml=1.41)[jd] - offsets(a0)[jd])
    per = math.sqrt(per_ml ** 2 + fl["aperture + orbital anisotropy on sigma_eff (L23's carried value)"] ** 2
                    + fl["sigma -> acceleration estimator (Wolf vs Milgrom virial)"] ** 2 + fl["distance to Coma (+-5%)"] ** 2)
    tot = math.sqrt(ERR[jd] ** 2 + per ** 2 + float(np.std(od)) ** 2)
    H2[f] = dict(mean=float(od.mean()), err=float(ERR[jd]), floor=per, tot=tot, z=float(od.mean() / tot),
                 stars_only=float(offsets(a0)[jd]))
check("H2 DF44 ALONE (Keck/KCWI, sigma = 33 +- 3 km/s) lies within 2 sigma under B's prediction (its own error + the per-object floor)",
      "; ".join(f"{f}: {v['mean']:+.3f} +- {v['tot']:.3f} dex ({v['z']:+.2f} sigma; stars only {v['stars_only']:+.3f})" for f, v in H2.items()),
      all(abs(v["z"]) < 2 for v in H2.values()))

# ================================================================================================ H3 the accreted class
R.banner("H3  ONE ACCRETED CLASS: the Coma UDGs against CFG18's M31 LVD dwarfs (dex in sigma)")
H3 = {}
for f in FOOTS:
    u_ = RES[(f, "infall gas, non-detections zero")]
    m31 = C18["RES"][f"m31|zero|{f}"]
    z = (0.5 * u_["mean"] - m31["mean"]) / math.hypot(0.5 * u_["tot"], m31["err"])
    H3[f] = dict(udg_sigma_dex=0.5 * u_["mean"], udg_err=0.5 * u_["tot"], m31=m31["mean"], m31_err=m31["err"], z=float(z))
check("H3 THE ACCRETED CLASS IS ONE CLASS: the UDGs' dispersion offset agrees with CFG18's M31 LVD dwarfs under the same rule within 2 "
      "sigma, both footings",
      "; ".join(f"{f}: UDGs {v['udg_sigma_dex']:+.3f} +- {v['udg_err']:.3f} vs M31 LVD {v['m31']:+.3f} +- {v['m31_err']:.3f} ({v['z']:+.2f} sigma)"
                for f, v in H3.items()), all(abs(v["z"]) < 2 for v in H3.values()))

# ================================================================================================ reported
R.banner("R1-R7  REPORTED")
REP = {}
REP["R1_stars_only"] = {f: RES[(f, "stars only")] for f in FOOTS}
REP["R2_limits"] = {f: RES[(f, "infall gas, non-detections at limit")] for f in FOOTS}
REP["R3_P2"] = {f: float(wm(offsets(A0B[f], kern="P2", ratio=RZ)).mean()) for f in FOOTS}
REP["R4_virial"] = {f: float(wm(offsets(A0B[f], ratio=RZ, estimator="virial")).mean()) for f in FOOTS}
keck = np.array([n_ in ("DF44", "DFX1") for n_ in NAMES])
REP["R5_split"] = {}
for f in FOOTS:
    oz = offsets(A0B[f], ratio=RZ).mean(axis=0)
    mk, ek = wmean(oz[keck], ERR[keck]); mc, ec = wmean(oz[~keck], ERR[~keck])
    REP["R5_split"][f] = dict(keck=mk, keck_err=ek, chil=mc, chil_err=ec)
REP["R6_null_ratio"] = {}
for f in FOOTS:
    lo_, hi_ = 0.0, 1000.0
    for _ in range(80):
        mid = 0.5 * (lo_ + hi_)
        lo_, hi_ = (mid, hi_) if wm(offsets(A0B[f], ratio=np.full(len(UDG), mid))) > 0 else (lo_, mid)
    REP["R6_null_ratio"][f] = 0.5 * (lo_ + hi_)
near = np.unique(np.concatenate([np.argsort(np.abs(LCAL - lm))[:K] for lm in LMU]))
REP["R6_calibration_at_udg_mass"] = dict(ratios=[float(RAT[i]) for i in near], det=[bool(DET[i]) for i in near],
                                         max_detected=float(RAT[near][DET[near]].max()) if DET[near].any() else None)
efe_c = float(re.search(r"corrected EFE, equilibrium at the Einasto mean 3-D radius, canonical\s+([+-][0-9.]+)\s+([0-9.]+)", o23).group(1))
efe_cz = float(re.search(r"corrected EFE, equilibrium at the Einasto mean 3-D radius, canonical\s+([+-][0-9.]+)\s+([0-9.]+)", o23).group(2))
efe_a = re.search(r"corrected EFE, equilibrium, alt footing\s+([+-][0-9.]+)\s+([0-9.]+)", o23)
REP["R7_efe_rival"] = dict(canonical=(efe_c, efe_cz), alt=(float(efe_a.group(1)), float(efe_a.group(2))))
check("R1 (reported) stars only (the current baryons: FG001-H4-like)",
      "; ".join(f"{f}: {v['mean']:+.3f} +- {v['tot']:.3f} ({v['z']:+.2f} sigma)" for f, v in REP["R1_stars_only"].items()), True, load_bearing=False)
check("R2 (reported) infall gas with the non-detections at their upper limits",
      "; ".join(f"{f}: {v['mean']:+.3f} +- {v['tot']:.3f} ({v['z']:+.2f} sigma)" for f, v in REP["R2_limits"].items()), True, load_bearing=False)
check("R3/R4 (reported) the P2 kernel; the Milgrom-1994 virial estimator (both with infall gas, non-detections zero)",
      "; ".join(f"{f}: P2 {REP['R3_P2'][f]:+.3f}, virial {REP['R4_virial'][f]:+.3f}" for f in FOOTS), True, load_bearing=False)
check("R5 (reported) the Keck pair (DF44, DFX1) against the Chilingarian nine (infall gas, non-detections zero; statistical errors)",
      "; ".join(f"{f}: Keck {v['keck']:+.3f} +- {v['keck_err']:.3f}, Chilingarian {v['chil']:+.3f} +- {v['chil_err']:.3f}" for f, v in REP["R5_split"].items()),
      True, load_bearing=False)
check("R6 (reported) the common infall gas-to-star ratio that would null the offset, against the calibration dwarfs at the UDGs' masses",
      "; ".join(f"{f}: {v:.2f}" for f, v in REP["R6_null_ratio"].items()) + f"; the calibration dwarfs nearest the UDGs: gas/star "
      + ", ".join(f"{r_:.2f}{'' if d_ else ' (limit)'}" for r_, d_ in zip(REP["R6_calibration_at_udg_mass"]["ratios"], REP["R6_calibration_at_udg_mass"]["det"])),
      True, load_bearing=False)
check("R7 (reported) the external-field rival for comparison (L23, committed): the reading candidate B drops",
      f"canonical {efe_c:+.3f} dex ({efe_cz} sigma); alt {float(efe_a.group(1)):+.3f} ({efe_a.group(2)} sigma)", True, load_bearing=False)

# ================================================================================================ reading
reading = ("the 4.9-sigma Coma liability belongs to the external-field reading, not to candidate B: under B's ownership rule the UDGs sit "
           + " / ".join(f"{RES[(f, 'infall gas, non-detections zero')]['mean']:+.2f} dex ({RES[(f, 'infall gas, non-detections zero')]['z']:.1f} sigma)" for f in FOOTS)
           if h1 else "the Coma UDGs remain a failure of candidate B even under its own ownership rule")
P(f"\n    READING (declared): {reading}")
R.num("C1", dict(mine=mine, committed=dict(canonical=c_can, alt=c_alt)))
R.num("floor", FLOOR); R.num("stat", STAT)
R.num("RES", {f"{k[0]}|{k[1]}": v for k, v in RES.items()})
R.num("H2", H2); R.num("H3", H3); R.num("reported", REP); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
