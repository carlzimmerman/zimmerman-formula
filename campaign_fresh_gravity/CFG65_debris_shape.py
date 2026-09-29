#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG65 -- IS THE SUM RULE'S DEBRIS TERM ROBUST TO THE HALO SHAPE AND CONCENTRATION IT ASSUMES?  (a robustness test; NOT a search for a shape that passes)

FROZEN QUESTION (verbatim):
  'The sum rule's debris term uses an NFW shape with the Dutton-Maccio concentration c(M) (h48_h69b_relative_isolation.py nfw_enclosed). Repeated review flagged the NFW
  cusp and c(M) as the fragile assumption behind both the ultra-faint closure (CFG42: +0.325 -> -0.059 dex) and the classical-satellite over-prediction (CFG42/45: M31 LVD
  -2.67 sigma; CFG59: SLUGGS wants phi >= 0.81, LVD phi <= 0.30). Are those two results robust to the halo-shape and concentration assumption? Test three alternatives
  declared in advance, each with NO free parameter fitted to the data: (A) NFW with the Duffy+2008 relaxed/full-sample c(M) already used in campaign_fresh_gravity/CFG23
  (read how it defines c); (B) the SAME NFW mass M200 but a cored profile of the Burkert form whose core radius is set by the fixed scaling r_core = r_s (declare: this is a
  one-shot declared choice, not scanned), normalised to the same total M200; (C) the Einasto profile with alpha = 0.17 and the same M200 and r_-2 = r_s of the Dutton-Maccio
  NFW. A verdict is SHAPE-ROBUST if the UFD offset stays within 2 sigma of zero AND the LVD/classical over-prediction stays beyond -2 sigma or remains within the same 0.05
  dex under the alternative; otherwise SHAPE-SENSITIVE. Report, for each alternative: the ultra-faint KM median (with the CFG42 error model), the classical, Collins and LVD
  medians, SLUGGS and X-ray ellipticals offsets (as CFG45 scores them) and phi_needed for the LVD and SLUGGS (as CFG59), both footings.'

STANDING: kappa = 1/2 is FITTED; nothing here says the theory is closed; no tuning after seeing a result; any robustness result (robust, sensitive, mixed) is valid; every
claim is this script plus a MUTATE control that must fail.  Nothing here selects, fits or recommends a shape.

WHAT IS SWAPPED, AND ONLY THAT.  The committed harnesses are exec'd READ-ONLY: CFG45_rule_readings.py's prefix (everything up to its own controls; it exec's CFG42, CFG36/CFG35,
CFG38, CFG40, CFG41 read-only), with ONE source edit in the exec'd text (no repo file is edited): the name `nfw_enclosed` in CFG45's namespace, which every reading-(S)
estimator (sigma_read for the satellites, sluggs_sigma, xray_gal, ...) looks up, is bound to this script's profile function instead of h48's; and READ is cut to
("L", "S") for speed (the (M), (E) readings are not needed; (E) uses the Dutton-Maccio c internally and is not touched).  The rule's structure is untouched: f_ex = max(0,
1 - M_phantom,edge/[(1-f_b) M_c]) from the Moster collapse mass M_c = M_200c (clamped at 1e9, CFG42's declared trap), the added acceleration is G f_ex (1-f_b) M_prof(<r)/r^2, the
estimators, samples, Kaplan-Meier statistic, bootstrap (seed 42), Upsilon_V floor, collapse-mass floor (M_c = 1e8...1e10 for M_* < 1e5) and error models are CFG42's / CFG45's
own, evaluated with the swapped enclosed-mass function.  The phi analysis (LVD and SLUGGS only) is CFG59's `p_sat("m31")` and `p_sluggs` with its phi-scaled reading, its 101-
point grid, brentq root and 1-sigma interval definition, copied line for line.

THE PROFILES (declared before the first run; all: total mass M200 = the rule's M_h, R200 = h48's (200 x critical density, H0 = 67.4), r_s = R200 / c_DM with c_DM the Dutton-
Maccio concentration of h48, c_DM = 10^(0.905 - 0.101 [log10(0.674 M_h) - 12]); x = r/R200 is clipped to [1e-4, 5] exactly as h48 does; mass normalised so M_prof(<R200) = M200):
  DM  the committed NFW + Dutton-Maccio, re-expressed by this script's generic function (control: bit-identical to h48's function to 1e-9).
  (A) NFW with a Duffy et al. 2008 concentration, c = A (M_h / [2e12 / h])^B (1+z)^C with h = 0.674 (as h48's) and z = 0 (the satellite samples are at z = 0; CFG23's (1+z_l)^C
      factor, z_l = 0.25, is the KiDS lens redshift and is not applicable).  CFG23 defines c as a function of M200m, the mean-density mass: c_duffy(M200m) = 10.14 (M/(2e12/h))^-0.081
      (1+z)^-1.01, the FULL-sample Delta = 200 x mean-density row.  Three sub-variants are declared (exactly these): A1 = CFG23's row literally (A, B, C = 10.14, -0.081, -1.01; the
      argument is the rule's M_h, so this is the literal CFG23 function applied at z = 0, a convention mismatch with the 200c mass that is DISCLOSED, not corrected); A2 = the
      Duffy FULL-sample Delta = 200 x CRITICAL row (5.71, -0.084, -0.47), the row whose convention matches h48's 200c R200; A3 = the Duffy RELAXED-sample 200c row (6.71, -0.091,
      -0.44).  (Duffy's coefficients were first transcribed from memory of the paper's Table 1 and were VERIFIED against the paper's Table 1 after the run (all three rows match exactly; CFG65_README.md); A1's are CFG23's committed numbers.)  Shape: NFW, m(t) = ln(1+t) - t/(1+t).
  (B) Burkert, rho = rho0 r0^3 / [(r + r0)(r^2 + r0^2)], core radius r0 = r_s = R200/c_DM (a ONE-SHOT declared choice, not scanned; no other core radius is run); enclosed mass
      M(<r) = M200 f(r/r0)/f(c_DM), f(t) = ln(1+t^2) + 2 ln(1+t) - 2 arctan t.
  (C) Einasto, alpha = 0.17, rho = rho_-2 exp{-(2/alpha)[(r/r_-2)^alpha - 1]}, r_-2 = r_s = R200/c_DM; enclosed mass M(<r) = M200 P(3/alpha, s)/P(3/alpha, s200), s = (2/alpha)(r/r_-2)^alpha,
      P the regularised lower incomplete gamma function.
  ABSURD (control only, never scored as an alternative): DM x 100 everywhere.

THE STATISTICS (CFG45's, unchanged; each with both footings canonical | alt):
  U   MW ultra-faint KM median offset (9 upper limits) and its error sqrt(bootstrap^2 + Upsilon_V^2 + collapse-mass-floor^2); z = median/error.
  CL  MW classical dSph (14), M31 Collins+13 (14), M31 LVD (34): sample median offset with the CFG18 infall gas, error as CFG42's; z = median/error.
  SL  SLUGGS (19): mean outer-bin offset, error std/sqrt(19).       XR  X-ray ellipticals (7): mean offset, CFG36's error.
  PHI phi_needed for the M31 LVD and SLUGGS as CFG59 (root of the offset on [0,1], None if the signs agree; the 1-sigma interval {phi in [0,1]: |o| <= e} on the 101-point grid).

VERDICT RULES (declared before the first run; per alternative, then per family):
  V-UFD  the UFD result is SHAPE-ROBUST for an alternative iff |z_UFD| < 2 on BOTH footings.  (Reference: the DM/NFW rule's own values, CFG42: +0.325 -> -0.059 canonical.)
  V-LVD  the M31 LVD over-prediction result is SHAPE-ROBUST for an alternative iff on EACH footing: z_LVD <= -2 (the over-prediction stays beyond -2 sigma) OR
         |median_alt - median_DM| <= 0.05 dex (the offset is unchanged within 0.05 dex).  MW classical and Collins+13 are reported with the same two numbers but are NOT part of the
         verdict (the -2.67 sigma headline is the LVD's).
  V-ALL  the alternative is SHAPE-ROBUST iff V-UFD and V-LVD both hold; otherwise SHAPE-SENSITIVE (and the report says which of the two results moved).  Family (A) is SHAPE-ROBUST
         iff A1, A2 and A3 all are; otherwise SHAPE-SENSITIVE, naming the sub-variants.
  V-PHI  (declared companion reading of CFG59's conflict; not in the frozen rule): the phi conflict "no universal phi" is robust iff the LVD upper edge < the SLUGGS lower edge (the 1-sigma
         intervals stay disjoint) on both footings; reported per alternative.
  Reported only (no verdict): SLUGGS and X-ray offsets in dex and sigma against zero (2-sigma reading, as CFG45's A4/A5), the enclosed-mass ratio of each profile to the DM NFW at the
  radii the satellites probe (0.03, 0.1, 0.3, 1, 3 kpc; M_h = 1e9, 1e10, 1e11).

CONTROLS
  C1  CONTROL  (non-MUTATE) the DM configuration reproduces CFG45's committed results (UF, CL, SLUGGS, X-ray; reading S and L; both footings) to 1e-6: the swap reaches every
               estimator and the exec'd machinery is CFG45's.
  C2  CONTROL  the generic profile function, configured as NFW + Dutton-Maccio, equals h48's committed nfw_enclosed to 1e-9 (relative) over a grid of 30 halo masses x 40 radii
               (including the clip limits).
  C3  CONTROL  every profile (DM, A1-A3, B, C) reproduces the ANALYTIC enclosed-mass formula, written independently as direct numerical integration of the density (scipy quad),
               at 5 test radii for each of two halos (M_h = 3e9, 2e11), to relative 1e-7; and M_prof(<R200) = M200 to 1e-12, and the profile is monotone in r.
  C4  CONTROL  the bare law is shape-independent: the (L) reading's UF/CL/SLUGGS/X-ray numbers are identical across every configuration (only the debris term is swapped).
  C5  CONTROL  (non-MUTATE) the DM configuration's phi analysis reproduces CFG59's committed LVD and SLUGGS numbers (offsets at phi = 0 and 1, phi_needed, the 1-sigma intervals) to 1e-6.
  C6  CONTROL  the ABSURD profile (DM x 100) flips the UFD gate: the DM reference passes it (both footings |z| < 2) and the ABSURD profile fails it on at least one footing (non-MUTATE run).
  H1  [HEADLINE; MUTATE must fail] the harness's UFD gate is live on its reference: the DM-configured rule closes the ultra-faint failure (|z| < 2, both footings; CFG42 H1).  In the
      MUTATE run every profile's enclosed mass is multiplied by 100, the DM reference over-predicts, and H1 must FAIL (rc = 1).
  R   (reported, no gate) the per-alternative verdicts above and the full table.
MUTATE=1: every configuration's enclosed mass x 100 (the ABSURD control config is skipped) -- H1 must FAIL (rc = 1).
FIRST-RUN DISCLOSURE: before this docstring was final I ran ONLY a timing test of CFG45's prefix with h48's unmodified function (no output read: it printed the elapsed time and four
  dictionary keys); no result of any profile was seen before the declarations above.
CHANGED AFTER THE FIRST MAIN RUN, BEFORE ANY INTERPRETATION (disclosed): control C3's monotonicity clause first FAILED on a bug of mine -- it demanded a STRICTLY increasing enclosed mass on a
  radius grid that starts at 0.01 kpc, but h48's function clips x = r/R200 at 1e-4 (for M_h = 2e11, R200 ~ 110 kpc, so r < 0.011 kpc is on the constant clip plateau).  The clause now demands
  non-decreasing everywhere and strictly increasing on the unclipped range; the tolerance of every other clause (1e-7 analytic, 1e-12 normalisation) is unchanged.  The first run's log is kept
  (run_main_FIRSTRUN_C3fail.log).  Its C3 analytic-formula difference was 1.6e-11 and every other control passed; no hypothesis, verdict rule or number in the table changed.
Run: python3 cfg65_debris_shape.py   (MUTATE=1 for the control; outputs to the script's own directory, or $CFG65_OUT)
"""
import os, sys, math, io, contextlib, json, time
import numpy as np
from scipy import integrate, special
from scipy.optimize import brentq

sys.dont_write_bytecode = True
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("CFG65_OUT", HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG65_debris_shape", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every configuration's enclosed mass x 100 -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")
MFAC = 100.0 if MUTATE else 1.0

# ================================================================================================ h48's committed function and constants (exec'd read-only as CFG35 does)
with contextlib.redirect_stdout(io.StringIO()):
    g48, _ = C.C4.exec_slices(os.path.join(C.REPO, "hunt_2026", "h48_h69b_relative_isolation.py"), [(None, 'P("="*122); P("PART 1')], name="h48")
NFW_COMMITTED, RHO_C = g48["nfw_enclosed"], g48["_RHO_C"]
HH = 0.674


# ================================================================================================ the profiles
def c_dm(Mh):
    return 10 ** (0.905 - 0.101 * (np.log10(Mh * 0.674) - 12.0))


def c_duffy(A, B, Cz):
    return lambda Mh: A * (np.asarray(Mh, float) / (2e12 / HH)) ** B * 1.0 ** Cz          # z = 0: (1+z)^C = 1


def _m_nfw(t):
    return np.log1p(t) - t / (1 + t)


def _f_burkert(t):
    return np.log1p(t * t) + 2.0 * np.log1p(t) - 2.0 * np.arctan(t)


ALPHA = 0.17


def _P_einasto(t):
    """P(3/alpha, s) with s = (2/alpha) t^alpha: the un-normalised Einasto enclosed mass at t = r / r_-2."""
    return special.gammainc(3.0 / ALPHA, (2.0 / ALPHA) * np.power(t, ALPHA))


def make_profile(shape, cfn, mult=1.0, r_scale_cfn=None):
    """M_prof(<r) [Msun] for M200 = Mh [Msun] at r [kpc].  shape in nfw / burkert / einasto; cfn = the concentration c = R200/r_s used for the mass normalisation and (for nfw) the
    scale radius; for burkert / einasto the scale radius is r_s = R200 / c_DM (r_scale_cfn), the normalisation is at R200 (c_DM as the profile's own concentration)."""
    def f(Mh, r_kpc):
        Mh = np.asarray(Mh, float); r_kpc = np.asarray(r_kpc, float)
        c = cfn(Mh)
        R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        x = np.clip(r_kpc / R200, 1e-4, 5.0)
        if shape == "nfw":
            out = Mh * _m_nfw(c * x) / _m_nfw(c)
        elif shape == "burkert":
            out = Mh * _f_burkert(c * x) / _f_burkert(c)
        elif shape == "einasto":
            out = Mh * _P_einasto(c * x) / _P_einasto(c)
        else:
            raise ValueError(shape)
        return out * mult if mult != 1.0 else out
    return f


PROFILES = {"DM": ("nfw", c_dm), "A1": ("nfw", c_duffy(10.14, -0.081, -1.01)), "A2": ("nfw", c_duffy(5.71, -0.084, -0.47)), "A3": ("nfw", c_duffy(6.71, -0.091, -0.44)),
            "B": ("burkert", c_dm), "C": ("einasto", c_dm)}
LABELS = {"DM": "DM (NFW, Dutton-Maccio c: the committed rule)", "A1": "A1 NFW + Duffy full 200m (CFG23's row, z=0)", "A2": "A2 NFW + Duffy full 200c",
          "A3": "A3 NFW + Duffy relaxed 200c", "B": "B  Burkert, r_core = r_s", "C": "C  Einasto alpha=0.17, r_-2 = r_s"}
CONFIGS = ["DM", "A1", "A2", "A3", "B", "C"]
FUN = {k: make_profile(PROFILES[k][0], PROFILES[k][1], MFAC) for k in CONFIGS}
FUN_ABSURD = make_profile("nfw", c_dm, 100.0)

# ================================================================================================ C2 / C3 controls on the profile functions
R.banner("C2 / C3  CONTROLS: the profile function against h48's and against the analytic formulas")
rng = np.random.default_rng(65)
Mg = np.logspace(7.5, 13.5, 30); rg = np.concatenate([[1e-9, 1e-6], np.logspace(-2.5, 2.7, 38)])
dev2 = 0.0
f_id = make_profile("nfw", c_dm)
for M_ in Mg:
    a = np.asarray(f_id(M_, rg), float); b = np.asarray(NFW_COMMITTED(M_, rg), float)
    dev2 = max(dev2, float(np.max(np.abs(a / b - 1.0))))
check("C2 CONTROL: the generic function configured as NFW + Dutton-Maccio equals h48's committed nfw_enclosed to 1e-9 (30 masses x 40 radii incl. the clip limits)",
      f"max relative difference {dev2:.1e}", dev2 <= 1e-9)


def rho_shape(name, cfun, Mh):
    """the unnormalised density (in units of r_s) of each profile, for the independent numerical integration"""
    if name == "nfw":
        return lambda t: 1.0 / (t * (1 + t) ** 2)
    if name == "burkert":
        return lambda t: 1.0 / ((1 + t) * (1 + t * t))
    if name == "einasto":
        return lambda t: math.exp(-(2.0 / ALPHA) * (t ** ALPHA - 1.0))


def quad_enclosed(name, c, X):
    rho = rho_shape(name, None, None)
    I = lambda T: integrate.quad(lambda t: t * t * rho(t), 0.0, T, epsabs=0.0, epsrel=1e-12, limit=400)[0]
    return I(X) / I(c)


dev3, worst3, mono_ok, norm_dev = 0.0, "", True, 0.0
TEST_R = (0.05, 0.3, 1.5, 8.0, 40.0)
for key in ["DM", "A1", "A2", "A3", "B", "C"]:
    shape, cfn = PROFILES[key]; fn = make_profile(shape, cfn)
    for Mh in (3e9, 2e11):
        c = float(cfn(Mh)); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        # the profile's scale radius: nfw uses its own c; burkert / einasto use c_DM
        cs = c if shape == "nfw" else float(c_dm(Mh))
        for r in TEST_R:
            x = min(max(r / R200, 1e-4), 5.0)
            ana = Mh * quad_enclosed(shape, cs, cs * x)
            d = abs(float(fn(Mh, r)) / ana - 1.0)
            if d > dev3:
                dev3, worst3 = d, f"{key} M_h {Mh:.0e} r {r}"
        rr = np.logspace(-2, math.log10(5 * R200), 200)
        mm = np.asarray(fn(Mh, rr))
        unclipped = (rr / R200 >= 1e-4) & (rr / R200 <= 5.0)
        mono_ok = mono_ok and bool(np.all(np.diff(mm) >= 0)) and bool(np.all(np.diff(mm[unclipped]) > 0))
        norm_dev = max(norm_dev, abs(float(fn(Mh, R200)) / Mh - 1.0))
check("C3 CONTROL: each profile equals the analytic enclosed mass (direct numerical integration of its density) at 5 radii x 2 halos to 1e-7; M(<R200) = M200 to 1e-12; monotone in r",
      f"max relative difference {dev3:.1e} ({worst3}); max |M(<R200)/M200 - 1| {norm_dev:.1e}; monotone {mono_ok}", dev3 <= 1e-7 and norm_dev <= 1e-12 and mono_ok)

# ================================================================================================ the machinery run for one profile
ANCHOR = 'FB, nfw_enclosed, collapse_raw, edge_phantom36 = g36["FB"], g36["nfw_enclosed"], g36["collapse"], g36["edge_phantom"]'
READ_LINE = 'READ = ("L", "S", "M", "E")'
SRC45 = open(os.path.join(LANES, "CFG45_rule_readings.py")).read()
PRE45 = SRC45[:SRC45.index('R.banner("C1  CONTROLS')]
assert PRE45.count(ANCHOR) == 1 and PRE45.count(READ_LINE) == 1
PRE45 = PRE45.replace(ANCHOR, ANCHOR + "\nnfw_enclosed = PROFILE_FN").replace(READ_LINE, 'READ = ("L", "S")')
CODE45 = compile(PRE45, "CFG45_prefix_swapped", "exec")


def run_machinery(fn):
    """exec CFG45's prefix read-only with nfw_enclosed bound to fn.  MUTATE is forced off inside (the mutation here is on the enclosed mass, not on the collapse mass)."""
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    g = {"__file__": os.path.join(LANES, "CFG45_rule_readings.py"), "__name__": "cfg45_swapped", "PROFILE_FN": fn}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(CODE45, g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    assert g["MCF"] == 1.0 and g["nfw_enclosed"] is fn
    return g


# ---- phi analysis (CFG59's p_sat("m31") and p_sluggs, and its scan / segments / solve, copied)
GRID = np.round(np.linspace(0.0, 1.0, 101), 10)


def segments(phis, o, e):
    f = e - np.abs(o); segs = []; start = None
    for k in range(len(phis)):
        if f[k] >= 0 and start is None:
            start = phis[k] if k == 0 else phis[k - 1] + (phis[k] - phis[k - 1]) * (0 - f[k - 1]) / (f[k] - f[k - 1])
        if f[k] < 0 and start is not None:
            segs.append((float(start), float(phis[k - 1] + (phis[k] - phis[k - 1]) * f[k - 1] / (f[k - 1] - f[k])))); start = None
    if start is not None:
        segs.append((float(start), float(phis[-1])))
    return segs


def phi_analysis(g):
    PHI = [1.0]; orig = g["extra_acc"]; SI_H10 = g["SI_H10"]

    def extra_acc_phi(reading, r_kpc, g_law, gN, Mh, fex, r_e_kpc, consts=SI_H10):
        if reading == "P":
            return PHI[0] * orig("S", r_kpc, g_law, gN, Mh, fex, r_e_kpc, consts)
        return orig(reading, r_kpc, g_law, gN, Mh, fex, r_e_kpc, consts)
    g["extra_acc"] = extra_acc_phi
    SAMPLES, FLOORS, offs = g["SAMPLES"], g["FLOORS"], g["offs"]
    RES50, sluggs_sigma = g["RES50"], g["sluggs_sigma"]

    def p_lvd(foot, full=True):
        x = offs(SAMPLES["m31"], foot, "P", gas=True); med = float(np.median(x))
        if not full:
            return med, None
        ups = [offs(SAMPLES["m31"], foot, "P", gas=True, ups=u) for u in (1.0, 4.0)]
        f_ups = 0.5 * abs(float(np.median(ups[1])) - float(np.median(ups[0])))
        flo = [float(np.median(offs(SAMPLES["m31"], foot, "P", gas=True, floor_mh=fm))) for fm in FLOORS]
        err = 1.2533 * float(np.std(x)) / math.sqrt(len(x))
        return med, math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)

    def p_slu(foot, full=True):
        off = np.array([float(np.mean(np.log10(r["Sb"][r["out"]] / sluggs_sigma(r, foot, "P")[0][r["out"]]))) for r in RES50])
        return float(off.mean()), (float(off.std(ddof=1) / math.sqrt(len(off))) if full else None)

    out = {}
    for nm, fn in (("LVD", p_lvd), ("SLUGGS", p_slu)):
        for foot in FOOTS:
            oo, ee = [], []
            for ph in GRID:
                PHI[0] = float(ph); o, e = fn(foot); oo.append(o); ee.append(e)
            oo, ee = np.array(oo), np.array(ee)

            def fo(ph):
                PHI[0] = float(ph); return fn(foot, False)[0]
            a, b = fo(0.0), fo(1.0)
            root = None if a * b > 0 else float(brentq(fo, 0.0, 1.0, xtol=1e-9))
            out[f"{nm}|{foot}"] = dict(o0=float(oo[0]), o1=float(oo[-1]), e0=float(ee[0]), e1=float(ee[-1]), phi=root, segs=segments(GRID, oo, ee))
    PHI[0] = 1.0
    return out


def collect(g):
    d = dict(UF={}, CL={}, SL={}, XR={})
    for foot in FOOTS:
        for rd in ("L", "S"):
            u = g["UF"][(foot, rd)]
            d["UF"][f"{foot}|{rd}"] = dict(km=u["km"], tot=u["tot"], z=u["z"], resolved=u["resolved_median"])
            for key in ("cls", "col", "m31"):
                c = g["CL"][(key, foot, rd)]
                d["CL"][f"{key}|{foot}|{rd}"] = dict(med=c["med"], tot=c["tot"], z=c["z"], fex=c["fex"])
            s = g["SL"][(foot, rd)]
            d["SL"][f"{foot}|{rd}"] = dict(mean=s["mean"], err=s["err"], z=s["z"])
            x = g["XR"][(foot, rd)]
            d["XR"][f"{foot}|{rd}"] = dict(mean=x["mean"], tot=x["tot"], z=x["z"])
    return d


RES, PHIR = {}, {}
t0 = time.time()
for key in CONFIGS:
    g = run_machinery(FUN[key])
    RES[key] = collect(g)
    PHIR[key] = phi_analysis(g)
    P(f"    machinery run for {key:3s} done ({time.time() - t0:.0f} s)")
if not MUTATE:
    gA = run_machinery(FUN_ABSURD)
    RES["ABSURD"] = collect(gA)

# ================================================================================================ C1, C4, C5, C6
R.banner("C1 / C4 / C5 / C6  CONTROLS: the swap reaches the estimators; the law is shape-blind; CFG59's intervals; the absurd profile")
if not MUTATE:
    c45 = json.load(open(os.path.join(LANES, "CFG45_rule_readings_results.json")))["numbers"]
    devs = []
    for foot in FOOTS:
        for rd in ("L", "S"):
            devs.append((f"UF {foot} {rd} km", abs(RES["DM"]["UF"][f"{foot}|{rd}"]["km"] - c45["UF"][f"{foot}|{rd}"]["km"])))
            devs.append((f"UF {foot} {rd} tot", abs(RES["DM"]["UF"][f"{foot}|{rd}"]["tot"] - c45["UF"][f"{foot}|{rd}"]["tot"])))
            for key in ("cls", "col", "m31"):
                devs.append((f"CL {key} {foot} {rd} med", abs(RES["DM"]["CL"][f"{key}|{foot}|{rd}"]["med"] - c45["CL"][f"{key}|{foot}|{rd}"]["med"])))
                devs.append((f"CL {key} {foot} {rd} tot", abs(RES["DM"]["CL"][f"{key}|{foot}|{rd}"]["tot"] - c45["CL"][f"{key}|{foot}|{rd}"]["tot"])))
            devs.append((f"SLUGGS {foot} {rd} mean", abs(RES["DM"]["SL"][f"{foot}|{rd}"]["mean"] - c45["SLUGGS"][f"{foot}|{rd}"]["mean"])))
            devs.append((f"SLUGGS {foot} {rd} err", abs(RES["DM"]["SL"][f"{foot}|{rd}"]["err"] - c45["SLUGGS"][f"{foot}|{rd}"]["err"])))
            devs.append((f"XRAY {foot} {rd} mean", abs(RES["DM"]["XR"][f"{foot}|{rd}"]["mean"] - c45["XRAY"][f"{foot}|{rd}"]["mean"])))
            devs.append((f"XRAY {foot} {rd} tot", abs(RES["DM"]["XR"][f"{foot}|{rd}"]["tot"] - c45["XRAY"][f"{foot}|{rd}"]["tot"])))
    w = max(devs, key=lambda t: t[1])
    check("C1 CONTROL: the DM configuration reproduces CFG45's committed UF / CL / SLUGGS / X-ray numbers (readings S and L, both footings) to 1e-6",
          f"{len(devs)} comparisons; worst {w[0]} {w[1]:.1e}", w[1] <= 1e-6)
else:
    check("C1 CONTROL: skipped in the MUTATE run (the committed numbers are for the unmutated rule)", "-", True, load_bearing=False)

dL = 0.0
for key in CONFIGS[1:]:
    for sect in ("UF", "CL", "SL", "XR"):
        for k, v in RES[key][sect].items():
            if k.endswith("|L"):
                for f_, val in v.items():
                    dL = max(dL, abs(val - RES["DM"][sect][k][f_]))
check("C4 CONTROL: the bare law (reading L) is identical across every configuration -- only the debris term was swapped", f"max |difference| over every UF / CL / SLUGGS / X-ray number {dL:.1e}", dL <= 1e-12)

if not MUTATE:
    c59 = json.load(open(os.path.join(LANES, "CFG59_universal_debris_fraction_results.json")))["numbers"]["TAB"]
    d5 = []
    for nm, lab in (("LVD", "U4 M31 LVD"), ("SLUGGS", "U5 SLUGGS")):
        for foot in FOOTS:
            m = PHIR["DM"][f"{nm}|{foot}"]; t = c59[f"{lab}|{foot}"]
            for k in ("o0", "o1", "e0", "e1"):
                d5.append((f"{nm} {foot} {k}", abs(m[k] - t[k])))
            d5.append((f"{nm} {foot} phi", abs(m["phi"] - t["phi"]) if (m["phi"] is not None and t["phi"] is not None) else (0.0 if m["phi"] == t["phi"] else 9.0)))
            d5.append((f"{nm} {foot} nseg", 0.0 if len(m["segs"]) == len(t["segs"]) else 9.0))
            for (a, b), (a2, b2) in zip(m["segs"], t["segs"]):
                d5.append((f"{nm} {foot} seg lo", abs(a - a2))); d5.append((f"{nm} {foot} seg hi", abs(b - b2)))
    w = max(d5, key=lambda t: t[1])
    check("C5 CONTROL: the DM configuration's phi analysis reproduces CFG59's committed LVD and SLUGGS numbers (o(0), o(1), errors, phi_needed, 1-sigma intervals) to 1e-6",
          f"{len(d5)} comparisons; worst {w[0]} {w[1]:.1e}", w[1] <= 1e-6)
else:
    check("C5 CONTROL: skipped in the MUTATE run", "-", True, load_bearing=False)

ufd_gate = lambda key: all(abs(RES[key]["UF"][f"{f}|S"]["z"]) < 2 for f in FOOTS)
if not MUTATE:
    check("C6 CONTROL: the ABSURD profile (DM x 100) flips the UFD gate: the DM reference passes it, ABSURD fails it",
          f"DM z {RES['DM']['UF']['canonical|S']['z']:+.2f}/{RES['DM']['UF']['alt|S']['z']:+.2f}: gate {'pass' if ufd_gate('DM') else 'FAIL'}; ABSURD z "
          f"{RES['ABSURD']['UF']['canonical|S']['z']:+.2f}/{RES['ABSURD']['UF']['alt|S']['z']:+.2f}: gate {'pass' if ufd_gate('ABSURD') else 'FAIL'}",
          ufd_gate("DM") and not ufd_gate("ABSURD"))
else:
    check("C6 CONTROL: skipped in the MUTATE run (the mutation IS the absurd profile)", "-", True, load_bearing=False)

check("H1 [HEADLINE; MUTATE must fail] THE HARNESS'S UFD GATE IS LIVE ON ITS REFERENCE: the DM-configured rule closes the ultra-faint failure (|z| < 2, both footings)"
      + ("  [MUTATE: enclosed mass x 100]" if MUTATE else ""),
      "; ".join(f"{f}: KM {RES['DM']['UF'][f'{f}|L']['km']:+.3f} (law) -> {RES['DM']['UF'][f'{f}|S']['km']:+.3f} (rule), z {RES['DM']['UF'][f'{f}|S']['z']:+.2f}" for f in FOOTS), ufd_gate("DM"))

# ================================================================================================ the table
R.banner("THE TABLE (both footings: canonical | alt).  offsets in dex +- error [sigma]")
LAB = {"cls": "MW classical (14)", "col": "M31 Collins+13 (14)", "m31": "M31 LVD (34)"}
for key in CONFIGS + ([] if MUTATE else ["ABSURD"]):
    r = RES[key]
    P(f"\n  ---- {LABELS.get(key, 'ABSURD (control): DM x 100')}")
    u = lambda f, rd: r["UF"][f"{f}|{rd}"]
    P(f"    MW ultra-faint KM median  law {u('canonical', 'L')['km']:+.3f}|{u('alt', 'L')['km']:+.3f} ({u('canonical', 'L')['z']:+.2f}|{u('alt', 'L')['z']:+.2f} sigma)   RULE "
      f"{u('canonical', 'S')['km']:+.3f}+-{u('canonical', 'S')['tot']:.3f}|{u('alt', 'S')['km']:+.3f}+-{u('alt', 'S')['tot']:.3f}  ->  {u('canonical', 'S')['z']:+.2f}|{u('alt', 'S')['z']:+.2f} sigma")
    for k in ("cls", "col", "m31"):
        c = lambda f, rd: r["CL"][f"{k}|{f}|{rd}"]
        P(f"    {LAB[k]:24s} law {c('canonical', 'L')['med']:+.3f}|{c('alt', 'L')['med']:+.3f}   RULE {c('canonical', 'S')['med']:+.3f}+-{c('canonical', 'S')['tot']:.3f}|"
          f"{c('alt', 'S')['med']:+.3f}+-{c('alt', 'S')['tot']:.3f}  ->  {c('canonical', 'S')['z']:+.2f}|{c('alt', 'S')['z']:+.2f} sigma")
    s = lambda f, rd: r["SL"][f"{f}|{rd}"]
    P(f"    {'SLUGGS (19)':24s} law {s('canonical', 'L')['mean']:+.3f}|{s('alt', 'L')['mean']:+.3f}   RULE {s('canonical', 'S')['mean']:+.3f}+-{s('canonical', 'S')['err']:.3f}|"
      f"{s('alt', 'S')['mean']:+.3f}+-{s('alt', 'S')['err']:.3f}  ->  {s('canonical', 'S')['z']:+.2f}|{s('alt', 'S')['z']:+.2f} sigma")
    x = lambda f, rd: r["XR"][f"{f}|{rd}"]
    P(f"    {'X-ray ellipticals (7)':24s} law {x('canonical', 'L')['mean']:+.3f}|{x('alt', 'L')['mean']:+.3f}   RULE {x('canonical', 'S')['mean']:+.3f}+-{x('canonical', 'S')['tot']:.3f}|"
      f"{x('alt', 'S')['mean']:+.3f}+-{x('alt', 'S')['tot']:.3f}  ->  {x('canonical', 'S')['z']:+.2f}|{x('alt', 'S')['z']:+.2f} sigma")
    if key in PHIR:
        for nm in ("LVD", "SLUGGS"):
            row = []
            for f in FOOTS:
                p = PHIR[key][f"{nm}|{f}"]
                row.append((f"phi_needed {p['phi']:.3f}" if p["phi"] is not None else f"phi_needed none ({'+,+' if p['o0'] > 0 and p['o1'] > 0 else '-,-' if p['o0'] < 0 and p['o1'] < 0 else '?'})")
                            + " 1sig " + (" U ".join(f"[{a:.3f},{b:.3f}]" for a, b in p["segs"]) or "empty") + f" (o0 {p['o0']:+.3f}, o1 {p['o1']:+.3f})")
            P(f"    phi {nm:6s}: canonical: {row[0]}   |   alt: {row[1]}")

# ================================================================================================ the verdicts
R.banner("VERDICTS (rules declared in the docstring; reported, no gate)")
VER = {}
for key in CONFIGS[1:]:
    r = RES[key]; ref = RES["DM"]
    v_ufd = all(abs(r["UF"][f"{f}|S"]["z"]) < 2 for f in FOOTS)
    lvd = {}
    for f in FOOTS:
        z = r["CL"][f"m31|{f}|S"]["z"]; d = abs(r["CL"][f"m31|{f}|S"]["med"] - ref["CL"][f"m31|{f}|S"]["med"])
        lvd[f] = dict(z=z, dmed=d, beyond=z <= -2, within=d <= 0.05, ok=(z <= -2) or (d <= 0.05))
    v_lvd = all(lvd[f]["ok"] for f in FOOTS)
    cl_rep = {}
    for k in ("cls", "col"):
        cl_rep[k] = {f: dict(z=r["CL"][f"{k}|{f}|S"]["z"], dmed=abs(r["CL"][f"{k}|{f}|S"]["med"] - ref["CL"][f"{k}|{f}|S"]["med"])) for f in FOOTS}
    v_phi = all(PHIR[key][f"LVD|{f}"]["segs"] and PHIR[key][f"SLUGGS|{f}"]["segs"] and
                max(b for a, b in PHIR[key][f"LVD|{f}"]["segs"]) < min(a for a, b in PHIR[key][f"SLUGGS|{f}"]["segs"]) for f in FOOTS)
    VER[key] = dict(ufd=v_ufd, lvd=v_lvd, all=v_ufd and v_lvd, phi_conflict_persists=bool(v_phi), lvd_detail=lvd, classical_reported=cl_rep)
    P(f"  {LABELS[key]:46s}: UFD {'ROBUST ' if v_ufd else 'SENSITIVE'} (z {r['UF']['canonical|S']['z']:+.2f}|{r['UF']['alt|S']['z']:+.2f});  LVD {'ROBUST ' if v_lvd else 'SENSITIVE'} "
      f"(z {lvd['canonical']['z']:+.2f}|{lvd['alt']['z']:+.2f}; |d median vs DM| {lvd['canonical']['dmed']:.3f}|{lvd['alt']['dmed']:.3f} dex);  ->  "
      f"{'SHAPE-ROBUST' if v_ufd and v_lvd else 'SHAPE-SENSITIVE'};  phi conflict (LVD upper < SLUGGS lower) {'persists' if v_phi else 'does NOT persist'}")
    P(f"      reported: MW classical z {cl_rep['cls']['canonical']['z']:+.2f}|{cl_rep['cls']['alt']['z']:+.2f} (d median vs DM {cl_rep['cls']['canonical']['dmed']:.3f}|{cl_rep['cls']['alt']['dmed']:.3f}); "
      f"Collins z {cl_rep['col']['canonical']['z']:+.2f}|{cl_rep['col']['alt']['z']:+.2f} (d {cl_rep['col']['canonical']['dmed']:.3f}|{cl_rep['col']['alt']['dmed']:.3f}); "
      f"SLUGGS z {r['SL']['canonical|S']['z']:+.2f}|{r['SL']['alt|S']['z']:+.2f}; X-ray z {r['XR']['canonical|S']['z']:+.2f}|{r['XR']['alt|S']['z']:+.2f}")
famA = [k for k in ("A1", "A2", "A3")]
FAM = {"A": dict(members=famA, ufd=all(VER[k]["ufd"] for k in famA), lvd=all(VER[k]["lvd"] for k in famA), all=all(VER[k]["all"] for k in famA)),
       "B": dict(members=["B"], ufd=VER["B"]["ufd"], lvd=VER["B"]["lvd"], all=VER["B"]["all"]), "C": dict(members=["C"], ufd=VER["C"]["ufd"], lvd=VER["C"]["lvd"], all=VER["C"]["all"])}
P("")
for fam, v in FAM.items():
    P(f"  FAMILY ({fam}): UFD {'ROBUST' if v['ufd'] else 'SENSITIVE'}, LVD {'ROBUST' if v['lvd'] else 'SENSITIVE'}  =>  "
      f"{'SHAPE-ROBUST' if v['all'] else 'SHAPE-SENSITIVE'}" + ("" if v["all"] or len(v["members"]) == 1 else "   (sub-variants robust: " + ", ".join(k for k in v["members"] if VER[k]["all"]) + "; sensitive: " +
                                                                  ", ".join(k for k in v["members"] if not VER[k]["all"]) + ")"))

# ================================================================================================ enclosed-mass ratios (reported)
R.banner("ENCLOSED-MASS RATIO to the DM NFW at the radii the satellites probe (reported)")
RAT = {}
radii = (0.03, 0.1, 0.3, 1.0, 3.0)
P(f"    {'profile':46s}{'M_h':>8s}" + "".join(f"{r_:>10.2f}" for r_ in radii) + "   kpc")
for key in CONFIGS[1:]:
    for Mh in (1e9, 1e10, 1e11):
        rr = [float(FUN[key](Mh, r_) / FUN["DM"](Mh, r_)) for r_ in radii]
        RAT[f"{key}|{Mh:.0e}"] = rr
        P(f"    {LABELS[key]:46s}{Mh:8.0e}" + "".join(f"{v_:10.3f}" for v_ in rr))
P("    concentrations used (M_h = 1e9 / 1e10 / 1e11): " + "; ".join(f"{k}: " + "/".join(f"{float(PROFILES[k][1](M_)):.1f}" for M_ in (1e9, 1e10, 1e11)) for k in CONFIGS))

P("\n  READING (declared): a SHAPE-ROBUST verdict means the result survives that alternative on the frozen rule; SHAPE-SENSITIVE means the shape/concentration assumption carries it.  Nothing here says the "
  "theory is closed; no profile is selected, fitted or recommended.")


def ser(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else "|".join(map(str, k))): ser(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [ser(v) for v in o]
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    return o


R.num("RES", ser(RES)); R.num("PHI", ser(PHIR)); R.num("VERDICT", ser(VER)); R.num("FAMILY", ser(FAM)); R.num("RATIOS", ser(RAT))
R.num("controls", dict(c2=dev2, c3=dev3, norm=norm_dev))
nf = R.write(here=OUT)
sys.exit(1 if nf else 0)
