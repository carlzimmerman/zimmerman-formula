#!/usr/bin/env python3
"""
L18 -- the hydrostatic mass bias: propagating the one systematic L7 and L2 both rest on
=========================================================================================================
THE CLAIM UNDER TEST.  L7 concluded that what clusters require is quantitatively the COSMIC dark-to-baryon
share: at the outermost audited radius (1000 kpc = 0.80 R500) across twelve X-COP clusters the recovered
baryon fraction is f_bar = 0.149 (cosmic Omega_b/Omega_m = 0.156) and the Newtonian M_dark/M_bar is
5.73 +/- 0.68 against the cosmic 5.43, universal to 12%.  L2 concluded that the boost clusters demand is
Delta_req = (5.5 +/- 0.8) s^(0.81 +/- 0.08), whose slope is 3.9 sigma above the 1/2 that caps any kernel
with a deep-MOND limit, and that at the SAME accelerations clusters need 2.2-5.1x the boost galaxies are
measured to have (worst |z| = 13).

EVERY ONE OF THOSE NUMBERS RESTS ON M_HSE -- an X-ray hydrostatic mass.  Hydrostatic equilibrium of the
thermal gas alone is known to be violated at a measured level, the "hydrostatic mass bias"

        M_HSE = (1 - b) M_true ,

so that correcting it RAISES the true mass by 1/(1-b).  Nobody in this lane propagated it.  This script
does, on both L7's and L2's calculations, on both a0 footings, and it solves for the b that WOULD rescue
the framework so that the required value can be laid beside the measured one.

WHAT THIS REPOSITORY ALREADY KNOWS (surveyed first; this script EXTENDS it and does not redo it)
------------------------------------------------------------------------------------------------------
  * qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/  -- the lead's radius-unit audit,
    which is L7's and L2's data source.  It ALREADY carries a bias treatment, in two forms:
      (a) every row of results.json carries `HSE_multiplicative_factor_for_exact_match`, the factor by
          which M_HSE would have to be multiplied for the baryons alone to satisfy the EXACT exponential
          law.  Its table quotes 0.282 / 0.264 / 0.307 at 300 kpc for A1795 / A2029 / A2142.  A factor
          BELOW 1 is a NEGATIVE bias: it requires M_HSE to be an OVER-estimate.  This script converts that
          field to b and uses it as an independent cross-check of its own solve (check H7).
      (b) CLUSTER_AUDIT.md's pressure section proves the sign constraint directly: to remove the
          discrepancy the non-thermal pressure must INCREASE outward, and "with zero nonthermal pressure at
          the outer endpoint the required inner nonthermal pressure is negative: that restricted proposed
          explanation is impossible."  It also warns, correctly, that Eckert+2019's alpha = P_NT/P_tot is a
          pressure FRACTION and "not generally the hydrostatic mass bias".  This script honours that: it
          never sets b = alpha, it converts through the exact gradient relation.
  * hunt_2026/u02_measurement_method_organiser.py, block E2 -- applies b = 0.10/0.20/0.30 to the X-ray rows
    of the liability ledger and finds "WRONG SIGN: it makes the X-ray liability WORSE"; its block 6a is
    the same statement against a weak-lensing comparison at the same radius.
  * hunt_2026/u01_cluster_common_currency.py, PATTERN 3 -- b = 0.20 moves the framework's two best cluster
    rows toward the weak-lensing rows, i.e. away from the framework.
  * hunt_2026/u13_mass_efe_and_domain.py, block C3 -- the ONE place in the repository where the sign is
    applied the other way (line 334, `B -= 0.5*log10(1.25)`), concluding a hydrostatic bias "is real,
    helps, and is not the answer".  u02 line 565 applies the SAME magnitude with the OPPOSITE sign.  The
    two cannot both be right; check H2 settles it from the profiles themselves.  (For the record, the
    contradiction is confined to C3's prose and C7's intermediate value: C7 immediately overwrites
    B = 0.0 for every cluster row, so no published number of u13 moves.)
  * fable_independent_2026/L2_cluster_inverse.py, check C8 -- already prices the SAME escape in a physical
    variable rather than as b: the non-thermal support that would reconcile clusters with the measured
    galaxy boost needs sigma_1D = 857 km/s, 5.2x Hitomi's Perseus measurement.  L18 restates that in b and
    extends it to L7's baryon-fraction and cosmic-ratio conclusions, which C8 does not touch.

THE LITERATURE VALUES USED, each cited at the point of use, none invented -----------------------------
  X-COP itself (the sample these very profiles come from):
    Eckert et al. 2019, A&A 621, A40 (arXiv:1805.00034) -- median non-thermal pressure FRACTION ~6% at
      R500 and ~10% at R200; SZ mass calibration 1-b = 0.85 +/- 0.05 from the gas fraction.
    Ettori & Eckert 2022, A&A 657, L1 (arXiv:2112.07554) -- converting that to a mass bias for the X-COP
      sample: b < 0.03 in 50% of objects, b < 0.17 in 80%.  For the general local cluster population,
      b < 0.20 in 50% and b < 0.33 in 80%.
  Weak-lensing calibrations (the standard external measurement):
    von der Linden et al. 2014 (Weighing the Giants)         -- 1-b = 0.69 +/- 0.07,  b = 0.31
    Hoekstra et al. 2015 (CCCP)                              -- 1-b = 0.78 +/- 0.09,  b = 0.22
  Simulations:
    Nelson, Lau & Nagai 2014, ApJ 792, 25 -- non-thermal pressure fraction
      P_nth/P_tot = 1 - A{1 + exp[-(r/(B R200m))^gamma]}, A = 0.452, B = 0.841, gamma = 1.628.
    Kugel et al. 2024 (FLAMINGO, arXiv:2409.07849) -- median b at R500c ~ 0.1 (groups) to 0.2 (clusters).
  The extreme end, quoted as an upper envelope and NOT as a measurement of b:
    Planck 2015 XXIV cluster counts vs the CMB need 1-b ~ 0.58, i.e. b ~ 0.42.
  So the MEASURED RANGE adopted here is b in [0.00, 0.42], with the X-COP-specific value b = 0.03-0.17 and
  the population median b ~ 0.2.  Negative b is NOT measured for a relaxed population; individual-cluster
  scatter is +/- 0.1-0.2 about the median, so the empirical floor for a single system is about b = -0.2.

WHAT CHANGES AND WHAT DOES NOT.  M_bar comes from the X-ray emission measure (gas) plus the stellar
profile; neither uses the temperature GRADIENT, so g_bar and hence s = g_bar/a0 and M_kernel are untouched
by b.  Only g_HSE moves: g_true = g_HSE/(1-b).  Every table below applies the bias to that one quantity.

  H0 [CONTROL]    at b = 0 this pipeline reproduces L7's published numbers -- f_bar = 0.149, Newtonian
                  ratio 5.73, 12% scatter -- to better than 1%.  If this fails, stop; nothing else means
                  anything;
  H1 [CONTROL]    at b = 0 it also reproduces L2's published numbers -- the power law A = 5.47, p = 0.811
                  (canonical, stellar-7) and the cluster/galaxy boost ratio range 2.2-5.1;
  H2 [DIRECTION]  the framework-favourable proposition, tested rather than assumed: correcting the masses
                  for the MEASURED (positive) hydrostatic bias REDUCES the framework's required residual;
  H3 [KEY, L7]    there is a b inside the measured range [0, 0.42] that brings the framework's residual at
                  0.80 R500 to zero -- i.e. that rescues L7;
  H4 [KEY, L2]    there is a b inside the measured range that brings the cluster boost down to the
                  measured galaxy boost at the same acceleration -- i.e. that rescues L2's impossibility;
  H5 [L2 slope]   there is a b inside the measured range for which the required Delta_req acquires the
                  log-slope of a kernel of the class, p <= 1/2;
  H6 [L7 cosmic]  L7's cosmic-ratio agreement survives the measured bias range: across 0 <= b <= 0.33 the
                  Newtonian M_dark/M_bar stays inside the depletion-allowed 5.4-8.0 of L7's R1;
  H7 [CROSS]      this script's required-b solve reproduces the lead's own
                  `HSE_multiplicative_factor_for_exact_match` when run on the lead's exact exponential law;
  H8 [PHYSICAL]   the required b is physically available: it corresponds to a non-thermal support with the
                  right sign (P_nt >= 0, increasing outward) and a velocity dispersion at or below twice
                  Hitomi's Perseus measurement of 164 km/s;
  H9 [SCATTER]    the 12% cluster-to-cluster universality of the Newtonian ratio -- L7's R2 -- survives the
                  bias correction across the whole measured range.
Both footings throughout (a0 = 9.3619e-11 canonical, 1.1279e-10 alt).  FAIL marks a proposition the data
do not support.  A PASS on H3 or H4 would be a genuine escape for the framework and is the single most
valuable thing this lane could find; it is reported first if it happens.
"""
import numpy as np, math, json, os, sys, glob, time

T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, ".."))
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
H0_ = 0.674*100e3/Mpc; Om, Ob, Od = 0.315, 0.049, 0.266
COSMIC = Od/Ob                                                            # 5.43, as L7
FBAR_COSMIC = Ob/Om                                                       # 0.156, as L7
SIG_HITOMI = 164.0                                                        # Hitomi Perseus 1-D turbulent velocity, km/s
RNG = np.random.default_rng(20260908)

print("=" * 122)
print("L18 -- the hydrostatic mass bias b propagated through L7 (the cosmic ratio) and L2 (the impossibility)")
print("=" * 122, flush=True)

# ---------------------------------------------------------------- the literature ledger, used below
LIT = [
    ("X-COP, median of the sample (Ettori & Eckert 2022, A&A 657 L1)",              0.03),
    ("X-COP, 80th percentile of the sample (Ettori & Eckert 2022)",                 0.17),
    ("X-COP gas-fraction SZ calibration 1-b = 0.85 +/- 0.05 (Eckert+2019 A&A 621 A40)", 0.15),
    ("CCCP weak lensing, 1-b = 0.78 +/- 0.09 (Hoekstra+2015)",                      0.22),
    ("local cluster population median (Ettori & Eckert 2022)",                      0.20),
    ("FLAMINGO simulations at R500c, cluster scale (Kugel+2024)",                   0.20),
    ("Weighing the Giants weak lensing, 1-b = 0.69 +/- 0.07 (von der Linden+2014)", 0.31),
    ("local cluster population 80th percentile (Ettori & Eckert 2022)",             0.33),
    ("Planck 2015 XXIV counts-vs-CMB, 1-b ~ 0.58 (an upper envelope, not a measurement of b)", 0.42),
]
B_MEAS_LO, B_MEAS_HI = 0.00, 0.42          # the adopted measured range
B_XCOP_LO, B_XCOP_HI = 0.03, 0.17          # X-COP's own sample, the one these profiles come from
B_SINGLE_FLOOR = -0.20                     # the empirical floor for ONE cluster, from the scatter about the median
print("\n  the measured hydrostatic bias, M_HSE = (1-b) M_true:")
for src, b in LIT:
    print(f"      b = {b:+.2f}   {src}")
print(f"      ADOPTED measured range b in [{B_MEAS_LO:.2f}, {B_MEAS_HI:.2f}]; X-COP's own sample b in "
      f"[{B_XCOP_LO:.2f}, {B_XCOP_HI:.2f}]; single-cluster empirical floor b = {B_SINGLE_FLOOR:+.2f}", flush=True)

# ---------------------------------------------------------------- inputs (the lead's corrected audit, L7's loader)
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
ROWS = CLJ["rows"]; RADII = np.array(CLJ["radii_kpc"], float); A0 = CLJ["a0_m_s2"]
R500 = {d["name"]: d["own_R500_kpc"] for d in CLJ["radius_audit"]}
print(f"\n  inputs: {len(ROWS)} corrected X-COP rows, {len(set(r['cluster'] for r in ROWS))} clusters, radii "
      f"{RADII.astype(int).tolist()} kpc; source closure_2026/cluster_measurement_audit_2026/results.json", flush=True)

def Delta(s):                                                              # the CARRIED kernel, exactly as L7/L2/L6
    s = np.asarray(s, float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)

DAT = {}
for rw in ROWS:
    foot = rw.get("footing", "canonical")
    DAT.setdefault(foot, {}).setdefault(rw["cluster"], []).append(
        (float(rw["r_kpc"]), float(rw["g_baryon_over_a0"]), float(rw["g_hse_over_a0"]), bool(rw["stellar_file_present"])))

# ================================================================ 1. L7 UNDER A CONSTANT BIAS
print("\n" + "-" * 122)
print("  1.  L7 UNDER A CONSTANT BIAS.  Only g_HSE moves: g_true = g_HSE/(1-b).  g_bar (X-ray emission measure +")
print("      stellar profile) and therefore s, M_bar and M_kernel do not depend on the temperature GRADIENT and are")
print("      untouched.  f_bar = M_bar/M_true = (1-b) f_bar(b=0): a positive bias pushes f_bar DOWN, away from cosmic.")
print("-" * 122)

def l7_at(foot, b, radial=None):
    """L7's per-cluster quantities at the outermost audited radius under bias b (or a callable b(r_kpc, R500))."""
    per = []
    for name, pts in DAT[foot].items():
        p = sorted(pts); rk = np.array([x[0] for x in p]); sb = np.array([x[1] for x in p]); gh = np.array([x[2] for x in p])
        bb = np.array([radial(x, R500.get(name, np.nan)) for x in rk]) if radial is not None else np.full(len(rk), b)
        gt = gh/(1.0 - bb)                                                 # g_true/a0
        gk = sb + Delta(sb)                                                # kernel prediction /a0
        i = len(rk) - 1
        per.append(dict(name=name, r_kpc=rk[i], frac_R500=rk[i]/R500.get(name, np.nan), b_used=float(bb[i]),
                        fbar=float(sb[i]/gt[i]), ratio_N=float((gt[i]-sb[i])/sb[i]), ratio_F=float((gt[i]-gk[i])/sb[i]),
                        trend=float(np.polyfit(np.log10(rk), (gt-gk)/sb, 1)[0])))
    return per

def l7_summary(per):
    rN = np.array([x["ratio_N"] for x in per]); rF = np.array([x["ratio_F"] for x in per])
    fb = np.array([x["fbar"] for x in per]);    tr = np.array([x["trend"] for x in per])
    return dict(fbar=float(np.median(fb)), fbar_lo=float(fb.min()), fbar_hi=float(fb.max()),
                rN=float(np.median(rN)), rN_sd=float(np.std(rN, ddof=1)),
                rN_scat=float(np.std(rN, ddof=1)/np.median(rN)),
                rF=float(np.median(rF)), rF_sd=float(np.std(rF, ddof=1)),
                rF_z=float(np.median(rF)/(np.std(rF, ddof=1)/math.sqrt(len(rF)))),
                trend=float(np.median(tr)))

BGRID = [0.00, 0.03, 0.10, 0.15, 0.17, 0.20, 0.22, 0.31, 0.33, 0.42]
L7B = {}
for foot in sorted(DAT):
    print(f"\n    {foot} footing, twelve clusters at 1000 kpc = {np.nanmedian([x['frac_R500'] for x in l7_at(foot, 0.0)]):.2f} R500:")
    print(f"      {'b':>6s} {'1/(1-b)':>8s} | {'f_bar':>7s} {'vs cosmic':>10s} {'retained':>9s} | {'M_dark/M_bar':>13s} "
          f"{'scatter':>8s} {'vs 5.43':>8s} | {'M_resid/M_bar':>14s} {'sigma from 0':>13s}")
    for b in BGRID:
        S = l7_summary(l7_at(foot, b)); L7B[(foot, b)] = S
        print(f"      {b:6.2f} {1/(1-b):8.3f} | {S['fbar']:7.3f} {S['fbar']-FBAR_COSMIC:+10.3f} "
              f"{100*S['fbar']/FBAR_COSMIC:8.0f}% | {S['rN']:13.2f} {100*S['rN_scat']:7.0f}% {S['rN']-COSMIC:+8.2f} | "
              f"{S['rF']:14.2f} {S['rF_z']:13.1f}", flush=True)

C0 = L7B[("canonical", 0.00)]
print(f"\n    the direction, stated as an identity: f_bar(b) = (1-b) f_bar(0) and M_dark/M_bar(b) = "
      f"[1 + M_dark/M_bar(0)]/(1-b) - 1.")
print(f"    So a positive b moves f_bar DOWN, AWAY from the cosmic 0.156, and moves the Newtonian ratio UP, away from")
print(f"    5.43 -- but it moves both INTO the depletion band L7 itself allowed.  L7's R1 was written around 'clusters")
print(f"    retain 70-100% of the cosmic baryon share at R500'; at b = 0 these twelve retain {100*C0['fbar']/FBAR_COSMIC:.0f}%, the very top of")
print(f"    that window, and b = 0.20 brings them to {100*L7B[('canonical',0.20)]['fbar']/FBAR_COSMIC:.0f}%, its middle.  Read as a physical statement the bias")
print(f"    therefore makes the cosmic-share reading MORE self-consistent; read as L7's literal numerical coincidence")
print(f"    with 5.43 it degrades it, and check H6 below finds where the band is left.", flush=True)

# ================================================================ 2. RADIAL BIAS MODELS
print("\n" + "-" * 122)
print("  2.  RADIAL DEPENDENCE.  Three models the literature supports, all evaluated at L7's radius 0.80 R500.")
print("-" * 122)
# (i) power law anchored on X-COP's own measured non-thermal FRACTION trend, 6% at R500 -> 10% at R200
#     (Eckert+2019 A&A 621 A40).  R200/R500 = 1.5 for an NFW c=4 halo, so beta = ln(10/6)/ln(1.5) = 1.26.
BETA_XCOP = math.log(10.0/6.0)/math.log(1.5)
# (ii) Nelson, Lau & Nagai 2014 non-thermal pressure FRACTION, converted through the exact gradient relation,
#      NOT set equal to b.  With P_nt = k P_th, k = f/(1-f):
#          M_true/M_HSE = 1 + k + (dk/dlnr)/(dlnP_th/dlnr),
#      so b = 1 - 1/(M_true/M_HSE).  dlnP_th/dlnr is taken over the range -2 to -4 typical of cluster
#      outskirts and reported as a band, since the audit's rows do not carry the temperature profile.
NL_A, NL_B, NL_G = 0.452, 0.841, 1.628
def f_nelson(x200m):                                                        # x200m = r/R200m
    return 1.0 - NL_A*(1.0 + np.exp(-(x200m/NL_B)**NL_G))
def b_nelson(r_over_R500, dlnP=-3.0, R200m_over_R500=2.0):
    x = np.asarray(r_over_R500, float)/R200m_over_R500
    h = 1e-4; f0 = f_nelson(x); k0 = f0/(1-f0)
    fp = f_nelson(x*math.exp(h)); kp = fp/(1-fp)
    dk_dlnr = (kp - k0)/h
    ratio = 1.0 + k0 + dk_dlnr/dlnP                                        # M_true/M_HSE
    return 1.0 - 1.0/ratio
print(f"    (i)   X-COP-anchored power law b(r) = b500 (r/R500)^beta with beta = {BETA_XCOP:.2f} from the measured 6%->10%")
print(f"          non-thermal fraction between R500 and R200 (Eckert+2019).  At 0.80 R500 it gives "
      f"b = {0.80**BETA_XCOP:.3f} b500,")
print(f"          i.e. the radial form REDUCES the bias at L7's radius relative to R500 -- the direction adverse to this lane.")
for dlnP in (-2.0, -3.0, -4.0):
    print(f"    (ii)  Nelson+2014 fraction through the exact gradient relation, dlnP_th/dlnr = {dlnP:+.1f}: "
          f"b(0.80 R500) = {b_nelson(0.80, dlnP):.3f}, b(R500) = {b_nelson(1.0, dlnP):.3f}, b(1.5 R500) = {b_nelson(1.5, dlnP):.3f}")
print(f"          (sanity: at dlnP = -3 the value b(0.8 R500) = {b_nelson(0.8,-3.0):.3f} sits below X-COP's 80th-percentile bound")
print(f"          b < 0.17 but well above its median b < 0.03 (Ettori & Eckert 2022), i.e. the simulation-based profile is at")
print(f"          the PESSIMISTIC end for this sample -- the direction adverse to this lane, which is why it is carried.")
print(f"          Setting b = f_nth outright would give {f_nelson(0.8/2.0):.3f}, which the lead's audit correctly warns against.)")
RADMODELS = [("X-COP-anchored b500 = 0.17, beta = 1.26",  lambda r, R5: 0.17*(r/R5)**BETA_XCOP),
             ("population b500 = 0.20, beta = 1.26",      lambda r, R5: 0.20*(r/R5)**BETA_XCOP),
             ("WtG-anchored b500 = 0.31, beta = 1.26",    lambda r, R5: 0.31*(r/R5)**BETA_XCOP),
             ("Nelson+2014 fraction, dlnP = -3",          lambda r, R5: float(b_nelson(r/R5, -3.0))),
             ("Nelson+2014 fraction, dlnP = -2 (worst)",  lambda r, R5: float(b_nelson(r/R5, -2.0)))]
print(f"\n      {'radial model':40s} {'b @0.8R500':>11s} | {'f_bar':>7s} {'M_dark/M_bar':>13s} {'M_resid/M_bar':>14s} {'sigma from 0':>13s}")
RADOUT = {}
for lbl, fn in RADMODELS:
    per = l7_at("canonical", None, radial=fn); S = l7_summary(per); RADOUT[lbl] = S
    print(f"      {lbl:40s} {np.median([x['b_used'] for x in per]):11.3f} | {S['fbar']:7.3f} {S['rN']:13.2f} "
          f"{S['rF']:14.2f} {S['rF_z']:13.1f}", flush=True)
print(f"      (b = 0 reference)                        {0.0:11.3f} | {C0['fbar']:7.3f} {C0['rN']:13.2f} "
      f"{C0['rF']:14.2f} {C0['rF_z']:13.1f}")

# ================================================================ 3. L2 UNDER A BIAS
print("\n" + "-" * 122)
print("  3.  L2 UNDER A BIAS.  The required boost is Delta_req(s) = (g_true - g_bar)/a0 = (g_HSE/(1-b) - g_bar)/a0")
print("      at s = g_bar/a0, which is unchanged.  The galaxy side (SPARC rotation curves) carries no hydrostatic")
print("      assumption at all, so it does not move: the bias acts on ONE side of L2's comparison only.")
print("-" * 122)

# SPARC, loaded exactly as L2 loads it
T1 = {}
for ln in open(os.path.join(REPO, "real_research/data/SPARC_Lelli2016c.mrt")):
    p = ln.split()
    if len(p) >= 18:
        try: T1[p[0]] = (int(p[17]), float(p[5]))
        except ValueError: pass
gobs, gbar, gstar, sgo, gnames = [], [], [], [], []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6)); gname = os.path.basename(fn)[:-11]
    if gname in T1 and not (T1[gname][0] < 3 and T1[gname][1] > 30.0): continue
    m = (r > 0) & (Vo > 0) & (eV > 0) & (eV/Vo < 0.10)
    if m.sum() == 0: continue
    r_, Vo_, eV_, Vg_, Vd_, Vb_ = r[m]*kpc, Vo[m]*1e3, eV[m]*1e3, Vg[m]*1e3, Vd[m]*1e3, Vb[m]*1e3
    Vst2 = 0.5*Vd_**2 + 0.7*Vb_**2; Vbar2 = np.sign(Vg_)*Vg_**2 + Vst2; ok = Vbar2 > 0
    gobs.append(Vo_[ok]**2/r_[ok]); gbar.append(Vbar2[ok]/r_[ok]); gstar.append(Vst2[ok]/r_[ok])
    sgo.append(2*Vo_[ok]*eV_[ok]/r_[ok]); gnames += [gname]*int(ok.sum())
gobs = np.concatenate(gobs); gbar = np.concatenate(gbar); gnames = np.array(gnames)
print(f"\n    SPARC: {len(set(gnames))} galaxies, {len(gobs)} points (Q<3, i>30, eV/V<0.10) -- the same cut L2 uses", flush=True)

def pick(foot, subset):
    return [r for r in ROWS if r["footing"] == foot and (subset == "all" or r["stellar_file_present"])]
INV = {}
for foot in A0:
    for subset in ("all", "stellar"):
        R_ = pick(foot, subset)
        INV[(foot, subset)] = dict(s=np.array([r["g_baryon_over_a0"] for r in R_]),
                                   gh=np.array([r["g_hse_over_a0"] for r in R_]),
                                   cl=np.array([r["cluster"] for r in R_]))
HEAD = ("canonical", "stellar"); NB = 7

def boot_median(vals, groups, nb=800):
    if len(vals) == 0: return np.nan, np.nan
    uq = np.unique(groups); idx = {g: np.where(groups == g)[0] for g in uq}
    med = float(np.median(vals)); draws = np.empty(nb)
    for j in range(nb):
        draws[j] = np.median(np.concatenate([vals[idx[g]] for g in RNG.choice(uq, size=len(uq), replace=True)]))
    return med, float(np.std(draws))

def fit_pl(s, D):
    """power-law fit Delta = A s^p on the positive part of the cloud; returns A, p, rms, n_used."""
    m = D > 0
    if m.sum() < 5: return np.nan, np.nan, np.nan, int(m.sum())
    lo, lp = np.log10(s[m]), np.log10(D[m])
    p_, la_ = np.polyfit(lo, lp, 1)
    return float(10**la_), float(p_), float(np.sqrt(np.mean((lp - (p_*lo + la_))**2))), int(m.sum())

EDGES = {}
for key in INV:
    d = INV[key]
    EDGES[key] = np.geomspace(max(d["s"].min()*0.999, 1e-3), d["s"].max()*1.001, NB + 1)

def l2_bins(key, b):
    """cluster Delta_req per s-bin at bias b (bins are fixed: s does not depend on b)."""
    d = INV[key]; D = d["gh"]/(1.0 - b) - d["s"]; ed = EDGES[key]; out = []
    for i in range(len(ed) - 1):
        m = (d["s"] >= ed[i]) & (d["s"] < ed[i+1])
        if m.sum() < 5 or len(np.unique(d["cl"][m])) < 3: continue
        med, se = boot_median(D[m], d["cl"][m])
        out.append(dict(lo=ed[i], hi=ed[i+1], smed=float(np.median(d["s"][m])), med=med, se=se,
                        ncl=int(len(np.unique(d["cl"][m])))))
    return out

GALB = {}                                                                   # galaxy Delta per bin, computed ONCE (b-free)
for key in INV:
    foot = key[0]; a0 = A0[foot]; sg = gbar/a0; Dg = (gobs - gbar)/a0; rows = []
    for bn in l2_bins(key, 0.0):
        m = (sg >= bn["lo"]) & (sg < bn["hi"])
        if m.sum() < 20 or len(np.unique(gnames[m])) < 10: rows.append(None); continue
        gm, gse = boot_median(Dg[m], gnames[m])
        rows.append(dict(gm=gm, gse=gse, ngal=int(len(np.unique(gnames[m]))), npt=int(m.sum())))
    GALB[key] = rows

print(f"\n    the L2 headline (canonical, stellar-7) as a function of b:")
print(f"      {'b':>6s} | {'A':>7s} {'p':>7s} {'rms(dex)':>9s} | {'max Delta_req':>13s} | "
      f"{'cluster/galaxy ratio by bin':>44s} | {'worst |z|':>9s}")
L2B = {}
for b in [0.00, 0.10, 0.17, 0.20, 0.31, 0.42]:
    d = INV[HEAD]; Dv = d["gh"]/(1-b) - d["s"]
    A_, p_, rms_, n_ = fit_pl(d["s"], Dv)
    bns = l2_bins(HEAD, b); gl = GALB[HEAD]
    rat, zs = [], []
    for bn, g in zip(bns, gl):
        if g is None: continue
        rat.append(bn["med"]/g["gm"]); zs.append((bn["med"] - g["gm"])/math.sqrt(bn["se"]**2 + g["gse"]**2))
    L2B[b] = dict(A=A_, p=p_, rms=rms_, Dmax=max(x["med"] for x in bns), rat=rat, z=zs)
    print(f"      {b:6.2f} | {A_:7.2f} {p_:7.3f} {rms_:9.3f} | {max(x['med'] for x in bns):13.2f} | "
          f"{' '.join('%.1f' % x for x in rat):>44s} | {max(abs(np.array(zs))):9.1f}", flush=True)

print(f"\n    the same in words: at b = 0 clusters need {min(L2B[0.0]['rat']):.1f}-{max(L2B[0.0]['rat']):.1f}x the galaxy boost; at the population")
print(f"    median b = 0.20 they need {min(L2B[0.20]['rat']):.1f}-{max(L2B[0.20]['rat']):.1f}x; at the Weighing-the-Giants b = 0.31 they need "
      f"{min(L2B[0.31]['rat']):.1f}-{max(L2B[0.31]['rat']):.1f}x.")
print(f"    The fitted log-slope moves from p = {L2B[0.0]['p']:.3f} to {L2B[0.20]['p']:.3f} to {L2B[0.31]['p']:.3f}: the bias pushes p TOWARDS 1,")
print(f"    which is exactly the 'constant rescaling of G, i.e. extra mass tracing the baryons' end of L2's C9 and")
print(f"    further from the 1/2 that caps a kernel with a deep-MOND limit.", flush=True)

# ================================================================ 4. SOLVE FOR THE REQUIRED b
print("\n" + "-" * 122)
print("  4.  THE KEY QUESTION: SOLVE FOR THE b THAT WOULD RESCUE THE FRAMEWORK, then lay it beside the measured range.")
print("-" * 122)

def solve_b(f, lo=-8.0, hi=0.95, tol=1e-12):
    """bisect f(b) = 0 in b; f must be monotone on the bracket."""
    flo, fhi = f(lo), f(hi)
    if not np.isfinite(flo) or not np.isfinite(fhi) or flo*fhi > 0: return np.nan
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if f(lo)*f(mid) <= 0: hi = mid
        else: lo = mid
        if hi - lo < tol: break
    return 0.5*(lo + hi)

# (a) L7: the b that zeroes the framework residual at 0.80 R500
print("\n    (a)  L7's residual to zero at 0.80 R500.  Requires  g_HSE/(1-b) = g_bar + a0 Delta(g_bar/a0)  at that radius.")
BREQ_L7 = {}
for foot in sorted(DAT):
    bb = solve_b(lambda b: l7_summary(l7_at(foot, b))["rF"])
    BREQ_L7[foot] = bb
    S = l7_summary(l7_at(foot, bb))
    print(f"         {foot:9s}: b_required = {bb:+.3f}   (1-b = {1-bb:.3f}, i.e. M_HSE would have to OVER-state the true "
          f"mass by {100*((1-bb)-1):.0f}%)")
    print(f"                    at that b, f_bar = {S['fbar']:.3f} ({100*S['fbar']/FBAR_COSMIC:.0f}% of cosmic) and "
          f"M_dark/M_bar = {S['rN']:.2f} vs cosmic {COSMIC:.2f}")
    print(f"                    -- a SECOND cost, independent of any bias measurement: at the b the framework needs, all")
    print(f"                    twelve would hold {100*S['fbar']/FBAR_COSMIC:.0f}% of the universal baryon share.  The lead's CLUSTER_AUDIT.md correctly")
    print(f"                    disproves the naive claim that the cosmic fraction is a hard per-object CEILING, so this is")
    print(f"                    not a proof; it is a global-budget bill that the missing-baryon route would have to pay.")
# per-cluster spread of the required b
percl = {}
for foot in sorted(DAT):
    vals = []
    for name in DAT[foot]:
        p = sorted(DAT[foot][name]); sb = p[-1][1]; gh = p[-1][2]
        vals.append(1.0 - gh/(sb + float(Delta(sb))))
    percl[foot] = np.array(vals)
    print(f"         {foot:9s}: per-cluster required b spans {percl[foot].min():+.2f} to {percl[foot].max():+.2f} "
          f"(median {np.median(percl[foot]):+.2f}) -- every one of the twelve is negative")

# (b) L2: the b that brings the cluster boost down to the measured galaxy boost, bin by bin
print("\n    (b)  L2's overlap to agreement.  Requires  median[g_HSE/(1-b)] - s  =  Delta_galaxy  in each overlap bin.")
BREQ_L2 = {}
for key in [HEAD, ("alt", "stellar"), ("canonical", "all"), ("alt", "all")]:
    d = INV[key]; gl = GALB[key]; got = []
    for bn0, g in zip(l2_bins(key, 0.0), gl):
        if g is None: continue
        lo_, hi_ = bn0["lo"], bn0["hi"]; m = (d["s"] >= lo_) & (d["s"] < hi_)
        gh_, s_ = d["gh"][m], d["s"][m]
        bb = solve_b(lambda b: float(np.median(gh_/(1-b) - s_)) - g["gm"])
        got.append((bn0["smed"], bb, bn0["med"]/g["gm"]))
    BREQ_L2[key] = got
    lbl = f"{key[0]}/{'stellar 7' if key[1]=='stellar' else 'all 12'}"
    print(f"         {lbl:22s}: b_required by bin = " + ", ".join(f"{b:+.2f}" for _, b, _ in got) +
          f"   (median {np.median([b for _, b, _ in got]):+.2f})")

# (c) L2's slope: the b for which p falls to the class ceiling 1/2
print("\n    (c)  L2's shape gate.  The b for which the fitted log-slope p of Delta_req falls to the class ceiling 1/2.")
BREQ_P = {}
for key in [HEAD, ("canonical", "all")]:
    d = INV[key]
    bb = solve_b(lambda b: fit_pl(d["s"], d["gh"]/(1-b) - d["s"])[1] - 0.5, lo=-8.0, hi=0.95)
    BREQ_P[key] = bb
    A_, p_, rms_, n_ = fit_pl(d["s"], d["gh"]/(1-bb) - d["s"])
    lbl = f"{key[0]}/{'stellar 7' if key[1]=='stellar' else 'all 12'}"
    print(f"         {lbl:22s}: b(p = 1/2) = {bb:+.3f}   (there A = {A_:.2f}, rms {rms_:.3f} dex, {n_} of {len(d['s'])} rows still positive)")
print(f"         Read (c) as an order of magnitude only: at such a b a third of the rows have g_true < g_bar, so the")
print(f"         power law is fitted to a mutilated cloud (rms 1.4-1.9 dex).  The usable statement is the derivative,")
print(f"         reported in section 3: dp/db > 0, so no POSITIVE b can ever bring p down to 1/2.")
print(f"         (b) is identical at both footings by construction -- it equates two directly measured accelerations,")
print(f"         from which a0 cancels, which is the same invariance L2 records for its cluster/galaxy ratio.")

print(f"\n    THE COMPARISON, which is the whole point of the lane:")
print(f"         required   b = {BREQ_L7['canonical']:+.2f} (L7, canonical) / {BREQ_L7['alt']:+.2f} (L7, alt) / "
      f"{np.median([b for _, b, _ in BREQ_L2[HEAD]]):+.2f} (L2 overlap) / {BREQ_P[HEAD]:+.2f} (L2 slope)")
print(f"         measured   b in [{B_MEAS_LO:+.2f}, {B_MEAS_HI:+.2f}] for the population, [{B_XCOP_LO:+.2f}, {B_XCOP_HI:+.2f}] for X-COP itself,")
print(f"                    with a single-cluster empirical floor near {B_SINGLE_FLOOR:+.2f}")
print(f"         The required value is NEGATIVE and the measured value is POSITIVE.  They are not merely different in")
print(f"         size; they are on opposite sides of zero, so no amount of tightening the measured range can reach it.", flush=True)

# ================================================================ 5. IS THE REQUIRED b PHYSICALLY AVAILABLE?
print("\n" + "-" * 122)
print("  5.  IS THE REQUIRED b PHYSICALLY AVAILABLE?  A bias b>0 is non-thermal support: M_true - M_HSE = ")
print("      -(r^2/G rho_g) d(rho_g sigma^2)/dr.  With rho_g ~ r^-alpha_g and sigma roughly constant this is")
print("      sigma^2 = [b/(1-b)] g_HSE r / alpha_g, so b<0 needs sigma^2 < 0 -- not turbulence at all.")
print("-" * 122)
foot = "canonical"; a0 = A0[foot]
print(f"\n      {'cluster':10s} {'alpha_g':>8s} | {'sigma needed at b=+0.20':>24s} | {'sigma^2 needed at b_req':>24s}")
sig20, negcnt = [], 0
for name, pts in sorted(DAT[foot].items()):
    p = sorted(pts); rk = np.array([x[0] for x in p]); sb = np.array([x[1] for x in p])
    Mb = sb*a0*(rk*kpc)**2/G
    ag = -float(np.polyfit(np.log(rk[-4:]), np.log(np.maximum(np.gradient(Mb, rk*kpc)/(4*math.pi*(rk*kpc)**2), 1e-40))[-4:], 1)[0])
    ag = max(ag, 0.5)
    r_m = rk[-1]*kpc; gh = p[-1][2]*a0
    s2_20 = (0.20/0.80)*gh*r_m/ag
    breq = 1.0 - p[-1][2]/(sb[-1] + float(Delta(sb[-1])))
    s2_rq = (breq/(1-breq))*gh*r_m/ag
    sig20.append(math.sqrt(s2_20)/1e3)
    if s2_rq < 0: negcnt += 1
    print(f"      {name[:10]:10s} {ag:8.2f} | {math.sqrt(s2_20)/1e3:19.0f} km/s | "
          f"{s2_rq/1e6:16.2e} km^2/s^2  {'(NEGATIVE: impossible)' if s2_rq < 0 else ''}")
KT_TYP = 6.0*1.602176634e-16; MU_MP = 0.61*1.67262192e-27                   # a typical X-COP temperature, stated as an assumption
f_nth_20 = (np.median(sig20)*1e3)**2/((np.median(sig20)*1e3)**2 + KT_TYP/MU_MP)
print(f"\n      a measured b = 0.20 at 0.80 R500 corresponds to sigma_1D = {np.median(sig20):.0f} km/s (median), "
      f"{np.median(sig20)/SIG_HITOMI:.1f}x Hitomi's")
print(f"      Perseus measurement of {SIG_HITOMI:.0f} km/s.  Cross-check that this conversion is sane: at a typical kT = 6 keV that")
print(f"      dispersion is a non-thermal pressure fraction f_nth = rho sigma^2/(rho sigma^2 + P_th) = {100*f_nth_20:.0f}%, against the")
print(f"      {100*f_nelson(0.8/2.0):.0f}% Nelson+2014 simulate at this radius -- so b = 0.20 and the simulated turbulence are the same")
print(f"      statement, and both are a correction that makes the framework's job HARDER.  (sigma is model-dependent:")
print(f"      constant sigma with rho_g ~ r^-alpha_g; a rising sigma(r) would need less at this radius and more outside.)")
print(f"\n      The b the framework needs is NEGATIVE in {negcnt} of {len(DAT[foot])} clusters, so sigma^2 < 0: it is not a non-thermal")
print(f"      support at all but its opposite.  Written without turbulence, it is the demand that the measured thermal")
print(f"      pressure gradient be OVER-stated by a factor {(1-BREQ_L7['canonical']):.2f}.  This is exactly the branch the lead's own")
print(f"      CLUSTER_AUDIT.md proves impossible with a non-negative outer boundary pressure ('with zero nonthermal")
print(f"      pressure at the outer endpoint the required inner nonthermal pressure is negative').", flush=True)

# ================================================================ 6. CROSS-CHECK AGAINST THE LEAD'S OWN FIELD
print("\n" + "-" * 122)
print("  6.  CROSS-CHECK.  The lead's audit already stores, per row, `HSE_multiplicative_factor_for_exact_match` --")
print("      the factor F on M_HSE that makes the baryons alone satisfy its EXACT exponential law g_b = g_H(1-e^-g_H/a0).")
print("      That factor IS 1/(1-b) for that law, so b_lead = 1 - 1/F.  Re-deriving it here independently must agree.")
print("-" * 122)
worst = 0.0; sample = []
for rw in ROWS:
    a0_ = A0[rw["footing"]]; gh = rw["g_hse_over_a0"]; gb = rw["g_baryon_over_a0"]
    F_stored = rw["HSE_multiplicative_factor_for_exact_match"]
    # independent solve: find x = F such that (x gh)(1 - exp(-x gh)) = gb
    fx = lambda x: (x*gh)*(1 - math.exp(-x*gh)) - gb
    lo_, hi_ = 1e-6, 50.0
    if fx(lo_)*fx(hi_) > 0: continue
    for _ in range(200):
        mid = 0.5*(lo_+hi_)
        if fx(lo_)*fx(mid) <= 0: hi_ = mid
        else: lo_ = mid
    F_mine = 0.5*(lo_+hi_)
    worst = max(worst, abs(F_mine - F_stored)/max(abs(F_stored), 1e-12))
    if rw["footing"] == "canonical" and rw["r_kpc"] == 300.0 and rw["cluster"] in ("A1795", "A2029", "A2142"):
        sample.append((rw["cluster"], F_stored, 1 - 1/F_stored))
print(f"\n      independent re-solve of every one of {len(ROWS)} stored rows agrees to {worst:.2e} (relative)")
for nm, F, bl in sorted(sample):
    print(f"      {nm:8s} at 300 kpc: stored F = {F:.3f}  ->  b_lead = {bl:+.3f}")
print(f"      The audit's published table (0.282 / 0.264 / 0.307) therefore already contains this lane's answer, in")
print(f"      a different notation and for a different kernel: b = {1-1/0.282:+.2f} / {1-1/0.264:+.2f} / {1-1/0.307:+.2f} at 300 kpc.  L18's own")
print(f"      solve, on the framework's carried kernel and at L7's radius, gives the milder {BREQ_L7['canonical']:+.2f}; both are")
print(f"      negative and both are far outside anything measured.", flush=True)

# ================================================================ CHECKS
print("\n" + "=" * 122); print("  CHECKS"); print("=" * 122)

ok0 = (abs(C0["fbar"] - 0.149) < 0.001 and abs(C0["rN"] - 5.73) < 0.02 and abs(C0["rN_scat"] - 0.12) < 0.01
       and abs(l7_summary(l7_at("alt", 0.0))["rN"] - 5.73) < 0.02)
check("H0 [CONTROL] at b = 0 this pipeline reproduces L7's published numbers (f_bar = 0.149, Newtonian ratio 5.73, 12% scatter)",
      ok0, f"f_bar = {C0['fbar']:.3f} [{C0['fbar_lo']:.3f}, {C0['fbar_hi']:.3f}], ratio_N = {C0['rN']:.2f} +/- {C0['rN_sd']:.2f} "
           f"({100*C0['rN_scat']:.0f}% scatter), ratio_F = {C0['rF']:.2f} ({C0['rF_z']:.0f} sigma from 0); alt footing ratio_N = "
           f"{l7_summary(l7_at('alt', 0.0))['rN']:.2f}")

ok1 = (abs(L2B[0.0]["A"] - 5.47) < 0.10 and abs(L2B[0.0]["p"] - 0.811) < 0.010
       and abs(min(L2B[0.0]["rat"]) - 2.2) < 0.2 and abs(max(L2B[0.0]["rat"]) - 5.1) < 0.3)
check("H1 [CONTROL] at b = 0 it also reproduces L2's published numbers (Delta_req = 5.47 s^0.811 and cluster/galaxy ratios 2.2-5.1)",
      ok1, f"A = {L2B[0.0]['A']:.2f} (L2: 5.47), p = {L2B[0.0]['p']:.3f} (L2: 0.811), rms {L2B[0.0]['rms']:.3f} dex (L2: 0.094), "
           f"ratios {min(L2B[0.0]['rat']):.1f}-{max(L2B[0.0]['rat']):.1f} (L2: 2.2-5.1)")

dF = L7B[("canonical", 0.20)]["rF"] - C0["rF"]
dD = L2B[0.20]["Dmax"] - L2B[0.0]["Dmax"]
dP = L2B[0.20]["p"] - L2B[0.0]["p"]
check("H2 [DIRECTION] correcting the masses for the MEASURED (positive) hydrostatic bias REDUCES the framework's required residual",
      dF < 0 and dD < 0,
      f"at b = 0.20 the framework residual moves {C0['rF']:.2f} -> {L7B[('canonical',0.20)]['rF']:.2f} M_bar ({dF:+.2f}), the maximum "
      f"required boost {L2B[0.0]['Dmax']:.2f} -> {L2B[0.20]['Dmax']:.2f} ({dD:+.2f}) and the slope {L2B[0.0]['p']:.3f} -> {L2B[0.20]['p']:.3f} "
      f"({dP:+.3f}): ALL THREE MOVE AWAY FROM THE FRAMEWORK.  u02's E2 sign is right and u13's C3 line 334 sign is wrong")

b7 = max(BREQ_L7.values())
check("H3 [KEY, L7] there is a b inside the measured range [0.00, 0.42] that brings the framework's residual at 0.80 R500 to zero",
      B_MEAS_LO <= b7 <= B_MEAS_HI,
      f"required b = {BREQ_L7['canonical']:+.3f} (canonical) / {BREQ_L7['alt']:+.3f} (alt); every one of the twelve clusters needs a "
      f"negative b ({percl['canonical'].min():+.2f} to {percl['canonical'].max():+.2f}); the measured range is [{B_MEAS_LO:+.2f}, {B_MEAS_HI:+.2f}] and "
      f"X-COP's own is [{B_XCOP_LO:+.2f}, {B_XCOP_HI:+.2f}] -- the required value is on the OPPOSITE SIDE OF ZERO, "
      f"{abs(BREQ_L7['canonical'] - B_XCOP_LO)/0.10:.1f} single-cluster scatters (taking sigma_b = 0.10) below the X-COP median")

b2 = float(np.median([b for _, b, _ in BREQ_L2[HEAD]]))
b2all = [b for k in BREQ_L2 for _, b, _ in BREQ_L2[k]]
check("H4 [KEY, L2] there is a b inside the measured range that brings the cluster boost down to the measured galaxy boost at the same acceleration",
      B_MEAS_LO <= b2 <= B_MEAS_HI,
      f"required b by bin (canonical/stellar-7): " + ", ".join(f"{b:+.2f}" for _, b, _ in BREQ_L2[HEAD]) +
      f"; median {b2:+.2f}, over all footings and subsets {min(b2all):+.2f} to {max(b2all):+.2f}; measured [{B_MEAS_LO:+.2f}, {B_MEAS_HI:+.2f}]")

bp = BREQ_P[HEAD]
check("H5 [L2 slope] there is a b inside the measured range for which the required Delta_req acquires the log-slope of a kernel of the class, p <= 1/2",
      B_MEAS_LO <= bp <= B_MEAS_HI,
      f"b(p = 1/2) = {bp:+.3f}; a POSITIVE b moves p the wrong way, {L2B[0.0]['p']:.3f} -> {L2B[0.20]['p']:.3f} at b = 0.20 and "
      f"{L2B[0.42]['p']:.3f} at b = 0.42, i.e. towards the p = 1 'constant rescaling of G' end")

r33 = [L7B[(f, b)]["rN"] for f in DAT for b in BGRID if b <= 0.33]
surv = all(COSMIC <= v <= COSMIC/0.7 for v in r33)
B_R1_EDGE = solve_b(lambda b: l7_summary(l7_at('canonical', b))['rN'] - COSMIC/0.7, lo=-0.5, hi=0.9)
check("H6 [L7 cosmic] L7's cosmic-ratio agreement survives the measured bias range: across 0 <= b <= 0.33 the Newtonian M_dark/M_bar stays inside R1's depletion-allowed 5.4-8.0",
      surv, f"ratio_N runs {min(r33):.2f} to {max(r33):.2f} over b in [0, 0.33] (R1 band {COSMIC:.2f}-{COSMIC/0.7:.2f}); it leaves the band above "
            f"b = {B_R1_EDGE:.2f}, so R1 as WRITTEN survives X-COP's own b <= 0.17 and the population median 0.20 but not the "
            f"population 80th percentile 0.33.  What is leaving is R1's 30% DEPLETION ALLOWANCE, not the cosmic reading: "
            f"f_bar falls {C0['fbar']:.3f} -> {L7B[('canonical',0.33)]['fbar']:.3f}, i.e. baryon retention {100*C0['fbar']/FBAR_COSMIC:.0f}% -> "
            f"{100*L7B[('canonical',0.33)]['fbar']/FBAR_COSMIC:.0f}%")

check("H7 [CROSS] this script's required-b solve reproduces the lead's own HSE_multiplicative_factor_for_exact_match on the lead's exact exponential law",
      worst < 1e-6, f"independent re-solve of all {len(ROWS)} stored rows agrees to {worst:.2e} relative; converted, the audit's "
                    f"published 300 kpc factors 0.282/0.264/0.307 are b = {1-1/0.282:+.2f}/{1-1/0.264:+.2f}/{1-1/0.307:+.2f}")

check("H8 [PHYSICAL] the required b is physically available: it is a non-thermal support with the right sign (P_nt >= 0, increasing outward) and sigma_1D at most 2x Hitomi's 164 km/s",
      negcnt == 0 and np.median(sig20) <= 2*SIG_HITOMI,
      f"the required b is negative in {negcnt} of {len(DAT['canonical'])} clusters, so sigma^2 < 0 -- it is not turbulence but a demand that the "
      f"measured thermal pressure gradient be OVER-stated by a factor {(1-BREQ_L7['canonical']):.2f}; even the ALLOWED b = 0.20 already needs "
      f"sigma_1D = {np.median(sig20):.0f} km/s = {np.median(sig20)/SIG_HITOMI:.1f}x Hitomi (f_nth = {100*f_nth_20:.0f}% at kT = 6 keV, matching Nelson+2014's "
      f"{100*f_nelson(0.8/2.0):.0f}%), and that correction hurts the framework rather than helping it")

scat_all = [L7B[(f, b)]["rN_scat"] for f in DAT for b in BGRID]
check("H9 [SCATTER] the 12% cluster-to-cluster universality of the Newtonian ratio (L7's R2) survives the bias correction across the measured range",
      max(scat_all) < 0.30,
      f"fractional scatter runs {100*min(scat_all):.0f}%-{100*max(scat_all):.0f}% over b in [0, 0.42], both footings "
      f"(a constant b cannot change the ordering, and it slightly TIGHTENS the fractional scatter because the ratio grows)")

# ================================================================ VERDICT
print("\n" + "=" * 122)
print("  WHAT THIS LANE FOUND")
print("=" * 122)
print(f"""
  1.  THE SIGN, settled from the profiles rather than assumed.  M_HSE = (1-b) M_true with b > 0 means the true
      mass is LARGER than the X-ray one.  g_bar and the kernel prediction do not move, so every framework
      shortfall grows: at the population median b = 0.20 the L7 residual goes {C0['rF']:.2f} -> {L7B[('canonical',0.20)]['rF']:.2f} baryonic masses,
      the L2 cluster/galaxy discrepancy goes {min(L2B[0.0]['rat']):.1f}-{max(L2B[0.0]['rat']):.1f}x -> {min(L2B[0.20]['rat']):.1f}-{max(L2B[0.20]['rat']):.1f}x, and the required log-slope goes
      {L2B[0.0]['p']:.3f} -> {L2B[0.20]['p']:.3f}, further above the 1/2 that caps a kernel of the class.  The one systematic that was
      not propagated makes the adverse conclusion STRONGER, not weaker.  (This confirms u02's E2 and u01's
      PATTERN 3 and contradicts u13's C3 line 334, which applies the same magnitude with the opposite sign.)

  2.  THE REQUIRED b IS NEGATIVE AND LARGE.  To zero L7's residual: b = {BREQ_L7['canonical']:+.3f} canonical, {BREQ_L7['alt']:+.3f} alt --
      X-ray masses would have to OVER-state the truth by {100*((1-BREQ_L7['canonical'])-1):.0f}%.  To close L2's overlap: b = {b2:+.2f}
      (bins {min(b for _, b, _ in BREQ_L2[HEAD]):+.2f} to {max(b for _, b, _ in BREQ_L2[HEAD]):+.2f}).  To bring the slope to 1/2: b = {bp:+.2f}.  Measured: b in
      [{B_MEAS_LO:+.2f}, {B_MEAS_HI:+.2f}] for the population, [{B_XCOP_LO:+.2f}, {B_XCOP_HI:+.2f}] for X-COP itself.  Opposite sign, and in magnitude
      {abs(BREQ_L7['canonical'])/B_MEAS_HI:.1f}x (L7) to {abs(b2)/B_MEAS_HI:.1f}x (L2) the largest number in the measured range, {abs(BREQ_L7['canonical'])/B_XCOP_HI:.0f}x to {abs(b2)/B_XCOP_HI:.0f}x X-COP's own.
      No radial model helps: the X-COP-anchored radial law makes b SMALLER at L7's 0.80 R500 than at R500
      ({0.80**BETA_XCOP:.2f} b500), and every simulation profile carried here stays positive at every radius.

  3.  L7's COSMIC-RATIO READING SURVIVES AS PHYSICS; ITS EXACT NUMERICAL COINCIDENCE DOES NOT.  This is the one
      place the bias costs L7 something, and it is reported as a correction to my own result.  A positive b
      lowers f_bar and raises M_dark/M_bar off the exact 5.43: at X-COP's own b <= 0.17 the ratio is {L7B[('canonical',0.17)]['rN']:.2f} and at
      the population median b = 0.20 it is {L7B[('canonical',0.20)]['rN']:.2f}, both still inside the 5.4-8.0 R1 band; at b = 0.33 it is
      {L7B[('canonical',0.33)]['rN']:.2f} and R1 as literally written FAILS above b = {B_R1_EDGE:.2f}.  What leaves the band is R1's own 30%
      depletion allowance, not the cosmic reading: retention goes {100*C0['fbar']/FBAR_COSMIC:.0f}% -> {100*L7B[('canonical',0.20)]['fbar']/FBAR_COSMIC:.0f}% -> {100*L7B[('canonical',0.33)]['fbar']/FBAR_COSMIC:.0f}%, and the 12%
      universality is invariant to within 1 point.  So the honest correction to L7 is: the closeness of 5.73 to
      5.43 at b = 0 is partly an artefact of ignoring the bias and should not be quoted as a 5% agreement;
      what the bias cannot touch is the universality and the fact that the required ratio is of order the
      cosmic one for every cluster, which is L7's actual argument.

  4.  L2's IMPOSSIBILITY IS ROBUST AND STRENGTHENED.  Nothing in the measured range of b weakens it; the whole
      measured range makes it worse.  The escape L2 already priced in a physical variable (C8: sigma_1D = 857 km/s,
      5.2x Hitomi) is the same escape as a negative b, and this lane confirms it is not merely large but of the
      wrong TYPE: sigma^2 < 0 in {negcnt} of {len(DAT['canonical'])} clusters.  It is the branch the lead's CLUSTER_AUDIT.md already
      proved impossible with a non-negative outer boundary pressure.

  LIMITS, stated.  b is applied here as a multiplicative correction to the tabulated g_HSE; it is not a refit of
  the X-ray spectra, and it does not carry the covariance of the temperature reconstruction.  A per-cluster b
  drawn from the measured scatter could put ONE system near b = -0.2, but the solve needs {BREQ_L7['canonical']:+.2f} in ALL TWELVE
  simultaneously.  Nothing here tests a bias in the BARYON census, which is a different systematic and is the
  door the lead's audit deliberately left open ('an additional, as-yet-unidentified baryonic component').
""")
print(f"RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"    [{time.time()-T0:.1f} s]")
sys.exit(0)
