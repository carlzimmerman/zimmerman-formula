#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG71 -- DOES CFG59's NO, AND THE SLUGGS-LVD CONFLICT, SURVIVE REPLACING SLUGGS'S OWN STELLAR MASSES BY CFG55'S DYNAMICAL (JAM-CALIBRATED) ONES?
(a descriptive consistency question; NOT a search for a rule that passes)

FROZEN QUESTION (verbatim):
  'CFG59 asked whether a single universal fraction phi of the sum rule's leftover debris reconciles ten populations and answered NO (the binding conflict: SLUGGS phi >= 0.81
  against M31 LVD phi <= 0.30). CFG55 then found that with dynamical (JAM-calibrated) stellar masses the SLUGGS deficit survives and grows: law +0.097 dex (4.0 sigma), rule
  +0.046 (2.6 sigma) on 16 of the 19 galaxies. Does CFG59's answer, and the SLUGGS-LVD conflict, survive replacing SLUGGS's own stellar masses by CFG55's dynamical ones? Report
  SLUGGS's phi_needed and 1-sigma interval under the dynamical masses (both footings), the size of the SLUGGS-LVD gap (lower edge of SLUGGS minus upper edge of LVD; if SLUGGS has
  no phi in [0,1] within 1 sigma, report the extended root on [0,6] as CFG59 did), and whether the universal-phi answer changes (it can only change from NO to YES if the SLUGGS
  interval moves to intersect all others; declare that check).'

STANDING (from the program): kappa = 1/2 is FITTED; nothing here says the theory is closed; no tuning after seeing a result; every claim is this committed-style script plus a
MUTATE control that must fail.  A YES would mean only "consistent with a universal fraction"; a NO means the sum's over-prediction and the bare law's under-prediction are not two
ends of ONE knob on these lanes.  Neither is a derived rule.

MACHINERY (declared).  This script is CFG59's harness COPIED (scratch dir, no repo file edited) with ONE population swapped.  CFG45 / CFG51 are exec'd read-only exactly as CFG59 does;
populations U1-U4 and U6-U10 are CFG59's own functions, unchanged.  U5 (SLUGGS) is replaced by U5d, CFG55's estimator with a debris scale phi:
  CFG55's prefix (its CFG38 machinery, the ATLAS3D JAM table, the SLUGGS table, the sample G16 = the 16 of CFG38's 19 that are in ATLAS3D, JAM quality >= 1) is exec'd read-only up to
  its own '# --- the models' marker, with MUTATE forced to '0' for that exec (CFG55's own MUTATE, JAM masses halved, is NOT this script's control); CFG55's collapse / edge_phantom /
  nfw_enclosed / nu_h / sigma_r2 / sigma_los are then used as they are.
  For each galaxy and footing, with the collapse mass M_h = collapse(M_*, 'red') x MCF (MCF = 1; 0.01 in MUTATE, CFG59's control) and f_ex(M_*) = max(0, 1 - phi_edge(M_*)/((1 - f_b) M_h)):
    calibration (CFG55 rule_mass, frac = 1/2):   nu(g_N/a0) x frac x M_* + phi x f_ex (1 - f_b) M_NFW(< r_1/2; M_h) = M_JAM/2      -> M_*(phi)  (NaN if the phi-scaled debris alone
                                                exceeds M_JAM/2 at both ends of the bracket [1e8, 10^13.5]: that galaxy is excluded at that phi, count reported)
    prediction (CFG55 sigma_pred):               Hernquist stars at a = R_e/1.8153 with SLUGGS's R_e, isotropic Jeans, gamma = 3 tracer, nu_mono; g = g_law + phi x f_ex (1 - f_b) G M_NFW(<r)/r^2
    offset o(phi) = mean over galaxies of the outer-bin mean of log10(sigma_obs/sigma_pred) (outer bins R > max(R_e, 2 kpc)); error e(phi) = std(ddof=1)/sqrt(n) over the galaxies, both
    re-evaluated at every phi.  phi = 0 is CFG55's JAM-calibrated LAW (M_* from nu M_*/2 = M_JAM/2); phi = 1 is CFG55's JAM-calibrated RULE.  phi enters ONLY as that multiplier, in
    BOTH the calibration and the prediction (the 'exactly as CFG59 scales the debris' reading: CFG59 scales the debris acceleration; here the same debris also enters the calibrating
    mass, which is what CFG55's rule does).  Nothing is re-fitted.
  Reference only (not part of the answer): U5o = CFG59's original SLUGGS population (19 galaxies, SLUGGS masses), and U5s = the same 16 galaxies with SLUGGS's own masses (CFG55 R1),
  scanned with the same grid, to say what the swap changed.

POPULATIONS (declared; exactly ten): U1 MW ultra-faints, U2 MW classical dSphs, U3 M31 Collins+13, U4 M31 LVD, U5d SLUGGS (dynamical masses, 16), U6 X-ray ellipticals, U7 DT23 four S0/S0a,
  U8 UGC 2487, U9 Bootes I, U10 Tucana II -- U1-U4 and U6-U10 exactly as CFG59 declared them (both footings, errors re-evaluated at each phi where CFG59 does).

DEFINITIONS (as CFG59): phi_needed = root of o(phi) = 0 on [0,1] (brentq); phi_needed_ext = root on [0,6]; interval = {phi in [0,1] : |o| <= e} on the 101-point grid (edges by linear
  interpolation of e - |o|); ANSWER per footing = YES iff all ten intervals are non-empty and have a common intersection; OVERALL = YES iff both footings YES.  Also reported: the extended
  1-sigma band of U5d on [0,6] (grid step 0.05), which is informational.

PRE-DECLARED CLASSIFICATION (fixed before the first run).
  'the conflict SURVIVES'  iff the U5d interval (or, if it is empty on [0,1], its extended root on [0,6]) lies ENTIRELY ABOVE 0.30 on BOTH footings.  ('Above 0.30' is the literal number; the
                          harness also prints the gap against U4's computed upper edge, 0.301 canonical / 0.221 alt, from the recomputed table.)
  'the conflict is RESOLVED' iff a common phi exists (the ten-population intersection is non-empty on both footings); the answer can change from NO to YES ONLY that way, and only if the
                          U5d interval reaches down to intersect every other population's interval.  (That check is the ANSWER block of the harness, both footings.)
  Anything else is reported as 'mixed'.
  SLUGGS-LVD gap := lower edge of the U5d interval minus the upper edge of U4's interval (CFG59's hull definition); if the U5d interval is empty on [0,1], the extended root minus the U4
  upper edge is reported and labelled a ROOT gap (no 1-sigma statement).

CONTROLS
  C1a CONTROL  phi = 1 and phi = 0 reproduce CFG45's (S) and (L) for the nine unchanged populations (offsets and errors, both footings, 1e-9) -- as CFG59.
  C1b CONTROL  (non-MUTATE) U5d at phi = 1 / phi = 0 reproduces CFG55's COMMITTED rule / law per-galaxy offsets, means and errors (both footings) to 1e-6; and the nine unchanged populations'
               offsets, errors, phi_needed, phi_ext and 1-sigma intervals reproduce CFG59's COMMITTED table to 1e-6 (offsets/phi) with the intervals to 1e-6.
  C1c CONTROL  (reported) U5o reproduces CFG59's committed SLUGGS row (o(0), o(1), interval) to 1e-6, so the harness copy is CFG59's.
  C2  CONTROL  every offset (all ten, both footings) is non-increasing in phi on the 101-point grid (tolerance 1e-9 dex).  If U5d is NOT monotone this is reported as a FAIL and kept, and
               the root/interval logic is then flagged as possibly non-unique (a per-galaxy calibration adds a phi-dependence to the mass that CFG59's pure debris scaling lacks).
  C3  CONTROL  MUTATE: every collapse mass / 100 (CFG45's MCF, the CFG51 rule, and U5d's collapse mass); see H1.  Under it U5d must have no solution.
  H1  [HEADLINE; MUTATE must fail] the harness solves: phi_needed exists in [0,1] for U1 (KM median), both footings (CFG59's own H1, unchanged: it certifies that the harness solves).  In the MUTATE
      run the debris is 1/100: no phi closes the ultra-faints' bare-law failure, U1 has no solution, and H1 must FAIL (rc = 1).
  H2  (reported) the table, the YES/NO per footing and overall, the classification, the gap.
  H3  (reported) MUTATE: U5d has no phi_needed in [0,1] (the control that SLUGGS has no solution when the debris is removed); reported as a statement about the run.
MUTATE=1: collapse masses / 100.
ADDED AFTER THE FIRST MAIN RUN, BEFORE INTERPRETATION (disclosed; reported only): R2 (U5d's z at phi = 0.30 / U4's upper edge, its smallest |z| on [0,1]) and the disclosure that the classification
  is undefined when U5d has neither a 1-sigma interval nor a root (the code's extended-band fallback was in the code, not the docstring; the printed verdict is what the code gave).
Nothing is selected, fitted or recommended; no grid, threshold or population is changed after the first run.
Run: python3 cfg71_universal_fraction_dynamical_sluggs.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib, json
import numpy as np
from scipy.optimize import brentq
from scipy.stats import spearmanr

sys.dont_write_bytecode = True
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
OUT = os.environ.get("CFG71_OUT", os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LANES)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG71_universal_fraction_dynamical_sluggs", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every collapse mass / 100 -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")


def exec_prefix(fname, marker):
    """exec a committed script read-only up to `marker`, stdout suppressed (CFG45's own helper, copied)."""
    src = open(os.path.join(LANES, fname)).read()
    g = {"__file__": os.path.join(LANES, fname), "__name__": fname}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index(marker)], fname, "exec"), g)
    return g


_menv = os.environ.get("MUTATE")
g45 = exec_prefix("CFG45_rule_readings.py", 'R.banner("C1  CONTROLS')            # honours MUTATE via the environment (MCF = 0.01)
os.environ["MUTATE"] = "0"
g51 = exec_prefix("CFG51_walker_ufd.py", 'R.banner("C1  CONTROL")')
g55 = exec_prefix("CFG55_sluggs_dynamical_masses.py", "# ------------------------------------------------------------------ the models")   # MUTATE forced 0 (CFG55's own control is not ours)
if _menv is None:
    os.environ.pop("MUTATE")
else:
    os.environ["MUTATE"] = _menv
MCF = g45["MCF"]
assert (MCF == 0.01) == MUTATE

# ---------------------------------------------------------------------------------------------------------------- the phi-aware reading "P"
PHI = [1.0]
_orig_extra = g45["extra_acc"]
SI_H10 = g45["SI_H10"]


def extra_acc_phi(reading, r_kpc, g_law, gN, Mh, fex, r_e_kpc, consts=SI_H10):
    if reading == "P":
        return PHI[0] * _orig_extra("S", r_kpc, g_law, gN, Mh, fex, r_e_kpc, consts)
    return _orig_extra(reading, r_kpc, g_law, gN, Mh, fex, r_e_kpc, consts)


g45["extra_acc"] = extra_acc_phi                        # the exec'd lane functions look this name up in g45's globals

SAMPLES, UL, UPS_V, halo_mass, infall_gas, edge_info, FB = (g45[k] for k in ("SAMPLES", "UL", "UPS_V", "halo_mass", "infall_gas", "edge_info", "FB"))
ufd_stat, boot, offs, FLOORS = g45["ufd_stat"], g45["boot"], g45["offs"], g45["FLOORS"]
collapse, NU, A0SI, G_, MSUN, KPC = g45["collapse"], g45["NU"], g45["A0SI"], g45["G_"], g45["MSUN"], g45["KPC"]
g10, UGC, SIG_UGC = g45["g10"], g45["UGC"], g45["SIG_UGC"]
stat41, offs41, S0f, GALS41, BIAS, DBIAS, colour_of = (g45[k] for k in ("stat41", "offs41", "S0f", "GALS41", "BIAS", "DBIAS", "colour_of"))
RES50, sluggs_sigma, GAL = g45["RES50"], g45["sluggs_sigma"], g45["GAL"]
xray_gal, xsample, RADII = g45["xray_gal"], g45["xsample"], g45["RADII"]
extra_acc = g45["extra_acc"]


# ---------------------------------------------------------------------------------------------------------------- populations: (offset, error) at PHI
def set_phi(phi):
    PHI[0] = float(phi)


def p_ufd(foot, rd, full=True):
    m, x, xu = ufd_stat(foot, rd)
    if not full:
        return m, None
    err = boot(x, xu)
    ups_var = [ufd_stat(foot, rd, ups=u)[0] for u in (1.0, 4.0)]
    f_ups = 0.5 * abs(ups_var[1] - ups_var[0])
    flo = [ufd_stat(foot, rd, floor_mh=fm)[0] for fm in FLOORS]
    f_mh = 0.5 * (max(flo) - min(flo))
    return m, math.sqrt(err ** 2 + f_ups ** 2 + f_mh ** 2)


def p_sat(key):
    def f(foot, rd, full=True):
        x = offs(SAMPLES[key], foot, rd, gas=True); med = float(np.median(x))
        if not full:
            return med, None
        ups = [offs(SAMPLES[key], foot, rd, gas=True, ups=u) for u in (1.0, 4.0)]
        f_ups = 0.5 * abs(float(np.median(ups[1])) - float(np.median(ups[0])))
        flo = [float(np.median(offs(SAMPLES[key], foot, rd, gas=True, floor_mh=fm))) for fm in FLOORS]
        err = 1.2533 * float(np.std(x)) / math.sqrt(len(x))
        return med, math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
    return f


def p_sluggs(foot, rd, full=True):
    off = np.array([float(np.mean(np.log10(r["Sb"][r["out"]] / sluggs_sigma(r, foot, rd)[0][r["out"]]))) for r in RES50])
    return float(off.mean()), (float(off.std(ddof=1) / math.sqrt(len(off))) if full else None)


# ---- U5d: CFG55's estimator with a debris scale phi (calibration AND prediction).  G16, nu_h, nfw_enclosed, collapse, edge_phantom, sigma_r2, sigma_los are CFG55's (read-only exec).
G16, nu55, nfw55, collapse55, edgeph55, sr2_55, slos55, GAMMA55 = (g55[k] for k in ("G16", "nu_h", "nfw_enclosed", "collapse", "edge_phantom", "sigma_r2", "sigma_los", "GAMMA"))
A0SI55, FB55, G55, KPC55, MSUN55 = g55["A0SI"], g55["FB"], g55["G_"], g55["KPC"], g55["MSUN"]
assert len(G16) == 16 and abs(FB55 - FB) < 1e-15


def debris_phi(Ms, foot):
    Mh = collapse55(Ms, "red") * MCF
    return max(0.0, 1.0 - edgeph55(Ms, foot, 0.40) / ((1 - FB55) * Mh)), Mh


def calib_mass_phi(g, foot, phi, frac=0.5):
    a0 = A0SI55[foot]

    def tot(lm):
        Ms = 10 ** lm; gN = G55 * frac * Ms * MSUN55 / (g["r12"] * KPC55) ** 2
        fx, Mh = debris_phi(Ms, foot)
        return frac * Ms * float(nu55(gN / a0)) + phi * fx * (1 - FB55) * float(nfw55(Mh, g["r12"]))
    fr = lambda lm: math.log10(tot(lm)) - math.log10(g["Mjam"] / 2)
    if fr(8.0) * fr(13.5) > 0:
        return float("nan")
    return 10 ** brentq(fr, 8.0, 13.5, xtol=1e-12)


def off_phi(g, foot, Ms, phi):
    r = g["r"]; a0 = A0SI55[foot]; a_h = r["Re"] / 1.8153
    fx, Mh = debris_phi(Ms, foot)

    def gf(rr):
        Mb = Ms * MSUN55 * rr ** 2 / (rr + a_h) ** 2; gN = G55 * Mb / (rr * KPC55) ** 2
        out = gN * nu55(gN / a0)
        if phi * fx > 0:
            out = out + phi * fx * (1 - FB55) * G55 * np.asarray(nfw55(Mh, rr), float) * MSUN55 / (rr * KPC55) ** 2
        return out
    s_ = slos55(r["Rb"], sr2_55(gf, GAMMA55), GAMMA55)
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s_[r["out"]])))


NEXCL = {}


def per_gal_dyn(foot, phi):
    out = []
    for g in G16:
        m = calib_mass_phi(g, foot, phi)
        out.append(float("nan") if not np.isfinite(m) else off_phi(g, foot, m, phi))
    return np.array(out)


def p_sluggs_dyn(foot, rd, full=True):
    off = per_gal_dyn(foot, PHI[0]); ok = np.isfinite(off); NEXCL[(foot, round(PHI[0], 6))] = int((~ok).sum()); off = off[ok]
    return float(off.mean()), (float(off.std(ddof=1) / math.sqrt(len(off))) if full else None)


def p_sluggs_own16(foot, rd, full=True):
    """reference U5s: the same 16 galaxies with SLUGGS's own masses (CFG55 R1), debris phi-scaled in the prediction only (CFG59's reading)."""
    off = np.array([off_phi(g, foot, g["r"]["Mstar"], PHI[0]) for g in G16])
    return float(off.mean()), (float(off.std(ddof=1) / math.sqrt(len(off))) if full else None)


def p_xray(foot, rd, full=True):
    b = xsample(foot, rd)
    if not full:
        return b["mean"], None
    s = xsample(foot, rd, ups="us"); r4 = xsample(foot, rd, radii=(5.0, 10.0, 20.0, 40.0))
    return b["mean"], math.hypot(b["err"], math.hypot(s["mean"] - b["mean"], r4["mean"] - b["mean"]))


def p_s0(foot, rd, full=True):
    if not full:
        return float(offs41(foot, rd, S0f).mean()) - BIAS, None
    s = stat41(foot, rd, S0f)
    s0err = math.sqrt(np.std(np.array(s["per"]), ddof=1) ** 2 / s["n"] + s["mod"] ** 2 + s["ms"] ** 2 + s["mg"] ** 2 + s["rr"] ** 2 + DBIAS ** 2)
    return s["corr"], s0err


def p_ugc(foot, rd, full=True):
    Ms = 0.61 * UGC["L36"] * 1e9; Mb = Ms + 1.33 * UGC["MHI"] * 1e9
    Mh = collapse(Ms, "blue" if UGC["T"] >= 1 else "red") * MCF
    ph, r_e = edge_info(Mb, foot); fex = max(0.0, 1.0 - ph / ((1 - FB) * Mh))
    r = UGC["RHI"]; gb = G_ * Mb * MSUN / (r * KPC) ** 2; gl = NU(gb / A0SI[foot]) * gb
    g = gl + float(extra_acc(rd, r, gl, gb, Mh, fex, r_e))
    vp = math.sqrt(g * r * KPC) / 1e3
    return math.log10(UGC["Vflat"] / vp), (SIG_UGC if full else None)


# CFG51's two systems (rule term re-written with phi; err_dex as CFG51's, on the cleaned dispersion, phi-independent)
GAL51 = {g["name"]: g for g in g51["GAL"]}
A0H51, UPS51, a_int51, G51, Msun51 = g51["A0H"], g51["UPS_V"], g51["a_int"], g51["G"], g51["Msun"]
edge_phantom51, nfw51, halo51, spred51 = g51["edge_phantom"], g51["nfw_enclosed"], g51["halo_mass"], g51["spred"]


def spred51_phi(g, foot, rd):
    """CFG51's sigma_pred; rd 'L' (bare), 'S' (its rule, phi = 1), 'P' (phi-scaled debris).  Collapse mass x MCF (MUTATE)."""
    a0 = A0H51[foot]; Ms = UPS51 * g["LV"]; Mb = Ms + 1.33 * g["MHI"]
    rh_pc = (4.0 / 3.0) * g["rh"]; rh = rh_pc * 3.0857e16
    gg = a_int51(G51 * 0.5 * Mb * Msun51 / rh ** 2, 0.0, a0)
    if rd != "L":
        Mh = float(halo51(UPS51 * g["LV"])) * MCF
        fex = max(0.0, 1.0 - edge_phantom51(Mb, foot, 0.40) / ((1 - FB) * Mh))
        w = 1.0 if rd == "S" else PHI[0]
        gg += w * G51 * fex * (1 - FB) * float(nfw51(Mh, rh_pc / 1000.0)) * Msun51 / rh ** 2
    return math.sqrt(gg * rh / 3.0) / 1e3


def err51(g, foot):
    e = 0.5 * (math.log10(1 + g["clean_p"] / g["clean"]) + abs(math.log10(max(1 - g["clean_m"] / g["clean"], 1e-3))))
    o = lambda **kw: math.log10(g["clean"] / spred51(g, foot, **kw))
    ofs = [o(ups=u) for u in (1.0, 2.0, 4.0)] + [o(deep=True)]
    return math.sqrt(e ** 2 + (0.5 * (max(ofs) - min(ofs))) ** 2)


def p_walker(name):
    def f(foot, rd, full=True):
        g = GAL51[name]
        return math.log10(g["clean"] / spred51_phi(g, foot, rd)), (err51(g, foot) if full else None)
    return f


POPS = [("U1 MW ultra-faints (KM median)", p_ufd), ("U2 MW classical dSphs", p_sat("cls")), ("U3 M31 Collins+13", p_sat("col")), ("U4 M31 LVD", p_sat("m31")),
        ("U5 SLUGGS (dynamical masses, 16)", p_sluggs_dyn), ("U6 X-ray ellipticals", p_xray), ("U7 DT23 four S0/S0a", p_s0), ("U8 UGC 2487", p_ugc),
        ("U9 Bootes I (multi-epoch)", p_walker("Bootes I")), ("U10 Tucana II (multi-epoch)", p_walker("Tucana II"))]
NAMES = [p[0] for p in POPS]


def evaluate(fn, foot, phi, full=True):
    set_phi(phi)
    return fn(foot, "P", full)


# ---------------------------------------------------------------------------------------------------------------- per-population object metadata (median log M_*, log M_ph,edge/M_c, f_ex)
def meta(idx, foot):
    rows = []                                          # (log Ms, log10(ph/Mh), fex)

    def add(Ms, Mb, Mh):
        ph, _ = edge_info(Mb, foot)
        rows.append((math.log10(Ms), math.log10(max(ph, 1e-300) / Mh), max(0.0, 1.0 - ph / ((1 - FB) * Mh))))
    if idx == 0:
        for d in list(SAMPLES["ufd"]) + list(UL):
            Ms = UPS_V * d["LV"]; add(Ms, Ms + 1.33 * d["MHI"], float(halo_mass(Ms)) * MCF)
    elif idx in (1, 2, 3):
        for d in SAMPLES[("cls", "col", "m31")[idx - 1]]:
            Ms = UPS_V * d["LV"]; add(Ms, Ms + max(1.33 * d["MHI"], infall_gas(d)), float(halo_mass(Ms)) * MCF)
    elif idx == 4:
        for g in G16:                                   # descriptive only: SLUGGS's own stellar masses of the 16
            r = g["r"]; add(r["Mstar"], r["Mstar"], collapse(r["Mstar"], "red") * MCF)
    elif idx == 5:
        for g in GAL:
            Ms = g["uk"] * g["LK"]; add(Ms, Ms, collapse(Ms, "red") * MCF)
    elif idx == 6:
        for g in GALS41:
            if S0f(g):
                Ms = 10 ** g["lMs"]; add(Ms, Ms + 10 ** g["lMg"], collapse(Ms, colour_of(g)) * MCF)
    elif idx == 7:
        Ms = 0.61 * UGC["L36"] * 1e9; add(Ms, Ms + 1.33 * UGC["MHI"] * 1e9, collapse(Ms, "blue" if UGC["T"] >= 1 else "red") * MCF)
    else:
        g = GAL51[("Bootes I", "Tucana II")[idx - 8]]; Ms = UPS51 * g["LV"]; add(Ms, Ms + 1.33 * g["MHI"], float(halo51(Ms)) * MCF)
    a = np.array(rows)
    return dict(logMs=float(np.median(a[:, 0])), logratio=float(np.median(a[:, 1])), fex=float(np.median(a[:, 2])), n=len(a))


# ---------------------------------------------------------------------------------------------------------------- the scan
GRID = np.round(np.linspace(0.0, 1.0, 101), 10)
SCAN = {}                                              # (pop idx, foot) -> dict(o=..., e=...)
for i, (nm, fn) in enumerate(POPS):
    for foot in FOOTS:
        oo, ee = [], []
        for ph in GRID:
            o, e = evaluate(fn, foot, ph)
            oo.append(o); ee.append(e)
        SCAN[(i, foot)] = dict(o=np.array(oo), e=np.array(ee))
    P(f"    scanned {nm}   {R.el()}")


def segments(phis, o, e):
    """maximal segments of {phi : |o| <= e}, edges by linear interpolation of f = e - |o| between grid points."""
    f = e - np.abs(o); segs = []; start = None
    for k in range(len(phis)):
        if f[k] >= 0 and start is None:
            start = phis[k] if k == 0 else phis[k - 1] + (phis[k] - phis[k - 1]) * (0 - f[k - 1]) / (f[k] - f[k - 1])
        if f[k] < 0 and start is not None:
            segs.append((float(start), float(phis[k - 1] + (phis[k] - phis[k - 1]) * f[k - 1] / (f[k - 1] - f[k])))); start = None
    if start is not None:
        segs.append((float(start), float(phis[-1])))
    return segs


def intersect(a, b):
    out = []
    for (x0, x1) in a:
        for (y0, y1) in b:
            lo, hi = max(x0, y0), min(x1, y1)
            if lo <= hi:
                out.append((lo, hi))
    return out


def solve(fn, foot, lo, hi):
    f = lambda ph: evaluate(fn, foot, ph, full=False)[0]
    a, b = f(lo), f(hi)
    if a * b > 0:
        return None
    return float(brentq(f, lo, hi, xtol=1e-9))


TAB = {}
for i, (nm, fn) in enumerate(POPS):
    for foot in FOOTS:
        s = SCAN[(i, foot)]
        TAB[(i, foot)] = dict(o0=float(s["o"][0]), o1=float(s["o"][-1]), e0=float(s["e"][0]), e1=float(s["e"][-1]), phi=solve(fn, foot, 0.0, 1.0),
                              phi_ext=solve(fn, foot, 0.0, 6.0), segs=segments(GRID, s["o"], s["e"]), meta=meta(i, foot))
    P(f"    solved {nm}   {R.el()}")
set_phi(1.0)

# ---------------------------------------------------------------------------------------------------------------- controls
R.banner("C1  CONTROLS: phi = 1 is CFG45's (S), phi = 0 is its (L); committed results")
devs = []
for i, (nm, fn) in enumerate(POPS):
    if i == 4:
        continue                                        # U5d has no CFG45 reading letter; it is checked against CFG55's committed file in C1b
    for foot in FOOTS:
        for ph, rd in ((1.0, "S"), (0.0, "L")):
            set_phi(ph); a = fn(foot, "P", True); b = fn(foot, rd, True)
            devs.append((f"{nm} {foot} phi={ph:g} vs {rd}: offset", abs(a[0] - b[0]), 1e-9)); devs.append((f"{nm} {foot} phi={ph:g} vs {rd}: error", abs(a[1] - b[1]), 1e-9))
        k = SCAN[(i, foot)]
        devs.append((f"{nm} {foot}: grid phi=1 vs scan", abs(k["o"][-1] - TAB[(i, foot)]["o1"]), 1e-12))
set_phi(1.0)
check("C1a CONTROL: reading P at phi = 1 equals CFG45's S and at phi = 0 its L (offsets and errors, every population, both footings) to 1e-9 (CFG51 systems: its spred with rule=True / False)",
      f"{len(devs)} comparisons; worst ratio to tolerance {max(d[1] / d[2] for d in devs):.2e} ({max(devs, key=lambda t: t[1] / t[2])[0]})", all(d[1] <= d[2] for d in devs))
if not MUTATE:
    J = lambda n: json.load(open(os.path.join(LANES, n)))["numbers"]
    c45, c51 = J("CFG45_rule_readings_results.json"), J("CFG51_walker_ufd_results.json")
    d2 = []
    for foot in FOOTS:
        for ph, rd in ((1.0, "S"), (0.0, "L")):
            o = lambda i: TAB[(i, foot)]["o1"] if ph == 1.0 else TAB[(i, foot)]["o0"]
            d2.append((f"UF {foot} {rd}", abs(o(0) - c45["UF"][f"{foot}|{rd}"]["km"]), 1e-6))
            for j, key in ((1, "cls"), (2, "col"), (3, "m31")):
                d2.append((f"CL {key} {foot} {rd}", abs(o(j) - c45["CL"][f"{key}|{foot}|{rd}"]["med"]), 1e-6))
            d2.append((f"XRAY {foot} {rd}", abs(o(5) - c45["XRAY"][f"{foot}|{rd}"]["mean"]), 1e-6))
            d2.append((f"S0 {foot} {rd}", abs(o(6) - c45["DT23"][f"{foot}|{rd}"]["s0"]["corr"]), 1e-6))
            d2.append((f"UGC {foot} {rd}", abs(o(7) - c45["UGC2487"][f"{foot}|{rd}"]["off"]), 1e-6))
            for j, nm in ((8, "Bootes I"), (9, "Tucana II")):
                d2.append((f"{nm} {foot} {rd}", abs(o(j) - c51["RES"][f"{nm}|{foot}|{'rule' if rd == 'S' else 'clean'}"]["off"]), 1e-6))
    c55 = J("CFG55_sluggs_dynamical_masses_results.json"); d3 = []
    for foot in FOOTS:
        for ph, key in ((1.0, "rule"), (0.0, "law")):
            set_phi(ph); off = per_gal_dyn(foot, ph); ok = np.isfinite(off)
            ref = np.array(c55["RES"][foot][key]["per"])
            d3.append((f"U5d {foot} {key} n", 0.0 if ok.sum() == len(ref) == 16 else 1.0, 1e-6))
            d3.append((f"U5d {foot} {key} per-galaxy", float(np.max(np.abs(off[ok] - ref))) if ok.sum() == len(ref) else 1.0, 1e-6))
            m_, e_ = off[ok].mean(), off[ok].std(ddof=1) / math.sqrt(ok.sum())
            d3.append((f"U5d {foot} {key} mean", abs(m_ - c55["RES"][foot][key]["mean"]), 1e-6)); d3.append((f"U5d {foot} {key} err", abs(e_ - c55["RES"][foot][key]["err"]), 1e-6))
    set_phi(1.0)
    c59 = json.load(open(os.path.join(LANES, "CFG59_universal_debris_fraction_results.json")))["numbers"]["TAB"]; d4 = []
    OLDNAMES = {i: nm for i, nm in enumerate(NAMES)}; OLDNAMES[4] = "U5 SLUGGS"
    for i, nm in enumerate(NAMES):
        if i == 4:
            continue
        for foot in FOOTS:
            r59 = c59[f"{OLDNAMES[i]}|{foot}"]; t = TAB[(i, foot)]
            for kk in ("o0", "o1", "e0", "e1"):
                d4.append((f"{nm} {foot} {kk}", abs(t[kk] - r59[kk]), 1e-6))
            for kk in ("phi", "phi_ext"):
                d4.append((f"{nm} {foot} {kk}", (0.0 if t[kk] is None and r59[kk] is None else 1.0 if (t[kk] is None) != (r59[kk] is None) else abs(t[kk] - r59[kk])), 1e-6))
            ok_ = len(t["segs"]) == len(r59["segs"])
            d4.append((f"{nm} {foot} intervals", (max(abs(a - b) for x, y in zip(t["segs"], r59["segs"]) for a, b in zip(x, y)) if ok_ and t["segs"] else (0.0 if ok_ else 1.0)), 1e-6))
    check("C1b CONTROL: U5d at phi = 1 / 0 reproduces CFG55's COMMITTED rule / law (16 galaxies, per-galaxy offsets, mean and error, both footings) to 1e-6",
          f"{len(d3)} comparisons; worst {max(d3, key=lambda t: t[1])[0]} {max(t[1] for t in d3):.1e}", all(d[1] <= d[2] for d in d3))
    check("C1b' CONTROL: the nine unchanged populations reproduce CFG59's COMMITTED table (o(0), o(1), e(0), e(1), phi_needed, phi_ext, 1-sigma intervals) to 1e-6",
          f"{len(d4)} comparisons; worst {max(d4, key=lambda t: t[1])[0]} {max(t[1] for t in d4):.1e}", all(d[1] <= d[2] for d in d4))
    check("C1b'' CONTROL: the endpoints reproduce the committed CFG45 / CFG51 results files to 1e-6 (UF, CL x3, X-ray, S0, UGC 2487, Bootes I, Tucana II; both footings, S and L)",
          f"{len(d2)} comparisons; worst {max(d2, key=lambda t: t[1])[0]} {max(t[1] for t in d2):.1e}", all(d[1] <= d[2] for d in d2))
else:
    check("C1b CONTROL: skipped in the MUTATE run (the committed results are for the unmutated rule)", "-", True, load_bearing=False)
mono = [(NAMES[i], foot, float(np.max(np.diff(SCAN[(i, foot)]["o"])))) for i in range(len(POPS)) for foot in FOOTS]
check("C2 CONTROL: every offset is non-increasing in phi on the 101-point grid (max increment <= 1e-9 dex)",
      f"largest increment {max(m[2] for m in mono):.2e} ({max(mono, key=lambda t: t[2])[0]} {max(mono, key=lambda t: t[2])[1]})", all(m[2] <= 1e-9 for m in mono))

# ---------------------------------------------------------------------------------------------------------------- the table
R.banner("THE TABLE (plot-free): per population and footing -- offset at phi = 0 and 1 [dex, and in sigma], phi_needed, 1-sigma interval")
fmt = lambda x: "  --  " if x is None else f"{x:6.3f}"
P(f"    {'population':30s}{'foot':>10s}{'o(0)':>8s}{'z(0)':>7s}{'o(1)':>8s}{'z(1)':>7s}{'phi_need':>10s}{'phi_ext':>9s}  1-sigma interval(s) within [0,1]")
for i, nm in enumerate(NAMES):
    for foot in FOOTS:
        t = TAB[(i, foot)]
        if t["phi"] is not None:
            pn = f"{t['phi']:.3f}"
        else:
            pn = "none" + ("(+,+)" if t["o0"] > 0 and t["o1"] > 0 else "(-,-)" if t["o0"] < 0 and t["o1"] < 0 else "")
        iv = " U ".join(f"[{a:.3f},{b:.3f}]" for a, b in t["segs"]) or "empty"
        P(f"    {nm:30s}{foot:>10s}{t['o0']:+8.3f}{t['o0'] / t['e0']:+7.2f}{t['o1']:+8.3f}{t['o1'] / t['e1']:+7.2f}{pn:>10s}{(fmt(t['phi_ext']) if t['phi_ext'] is not None else 'none'):>9s}  {iv}")
P("    (phi_need 'none(+,+)' = offset positive at phi = 0 and 1: the data want MORE debris than the sum; 'none(-,-)' = negative at both: LESS than none; phi_ext = the root on [0,6], reported only.)")
P("    per-population medians (canonical):  log M_*  |  log10(M_ph,edge/M_c)  |  median f_ex  |  n objects")
for i, nm in enumerate(NAMES):
    m = TAB[(i, "canonical")]["meta"]
    P(f"      {nm:30s} {m['logMs']:6.2f}   {m['logratio']:7.2f}   {m['fex']:5.2f}   {m['n']}")

# ---------------------------------------------------------------------------------------------------------------- the answer
R.banner("THE ANSWER: does a single universal phi lie inside every population's 1-sigma interval?")
ANS = {}
for foot in FOOTS:
    inter = [(0.0, 1.0)]; empties = []
    for i in range(len(POPS)):
        segs = TAB[(i, foot)]["segs"]
        if not segs:
            empties.append(NAMES[i])
        inter = intersect(inter, segs)
    hull = [(NAMES[i], (min(a for a, b in TAB[(i, foot)]["segs"]), max(b for a, b in TAB[(i, foot)]["segs"]))) for i in range(len(POPS)) if TAB[(i, foot)]["segs"]]
    if hull:
        lo_p = max(hull, key=lambda t: t[1][0]); hi_p = min(hull, key=lambda t: t[1][1]); gap = lo_p[1][0] - hi_p[1][1]
    else:
        lo_p = hi_p = None; gap = None
    hl = lambda i: (min(a for a, b in TAB[(i, foot)]["segs"]), max(b for a, b in TAB[(i, foot)]["segs"]))
    pairs = [(NAMES[i], NAMES[j], max(hl(i)[0], hl(j)[0]) - min(hl(i)[1], hl(j)[1]))
             for i in range(len(POPS)) for j in range(i + 1, len(POPS)) if TAB[(i, foot)]["segs"] and TAB[(j, foot)]["segs"]
             and not intersect(TAB[(i, foot)]["segs"], TAB[(j, foot)]["segs"])]
    yes = bool(inter) and not empties
    ANS[foot] = dict(yes=yes, intersection=inter, empties=empties, binding=(lo_p, hi_p, gap), disjoint_pairs=pairs)
    P(f"  [{foot}] ANSWER: {'YES' if yes else 'NO'}   intersection of all ten intervals: " + (" U ".join(f"[{a:.3f},{b:.3f}]" for a, b in inter) if inter else "empty"))
    if empties:
        P(f"      populations with NO phi in [0,1] within 1 sigma, even alone: {', '.join(empties)}")
    if lo_p is not None:
        P(f"      binding pair (hulls): largest lower edge {lo_p[0]} at phi = {lo_p[1][0]:.3f}; smallest upper edge {hi_p[0]} at phi = {hi_p[1][1]:.3f}; gap {gap:+.3f} (positive = they do not overlap)")
    if pairs:
        P(f"      disjoint pairs ({len(pairs)}): " + "; ".join(f"{a} vs {b} (gap {g:.3f})" for a, b, g in sorted(pairs, key=lambda t: -t[2])[:12]) + (" ..." if len(pairs) > 12 else ""))
    order = sorted(range(len(POPS)), key=lambda i: (TAB[(i, foot)]["phi"] if TAB[(i, foot)]["phi"] is not None else (9.0 if TAB[(i, foot)]["o1"] > 0 else -9.0)))
    P("      phi_needed ordering (low -> high; 'more than sum' = +9 marker, 'bare law already too high' = -9): " + " < ".join(
        f"{NAMES[i].split(' ')[0]}" + (f"={TAB[(i, foot)]['phi']:.2f}" if TAB[(i, foot)]["phi"] is not None else (">1" if TAB[(i, foot)]["o1"] > 0 else "<0")) for i in order))
overall = all(ANS[f]["yes"] for f in FOOTS)
allsegs = [(0.0, 1.0)]
for foot in FOOTS:
    for i in range(len(POPS)):
        allsegs = intersect(allsegs, TAB[(i, foot)]["segs"])
P(f"\n  OVERALL (YES iff both footings YES): {'YES' if overall else 'NO'};  intersection of all twenty footing-population intervals: "
  + (" U ".join(f"[{a:.3f},{b:.3f}]" for a, b in allsegs) if allsegs else "empty"))

R.banner("CFG71 SPECIFIC: U5d (SLUGGS, dynamical masses), the reference rows, the SLUGGS-LVD gap, the pre-declared classification")
REF = {}
for lab, fn in (("U5o SLUGGS original (19, SLUGGS masses; = CFG59's U5)", p_sluggs), ("U5s same 16, SLUGGS masses (CFG55 R1)", p_sluggs_own16)):
    for foot in FOOTS:
        oo, ee = [], []
        for ph in GRID:
            o, e = evaluate(fn, foot, ph); oo.append(o); ee.append(e)
        REF[(lab, foot)] = dict(o0=float(oo[0]), o1=float(oo[-1]), e0=float(ee[0]), e1=float(ee[-1]), phi=solve(fn, foot, 0.0, 1.0), phi_ext=solve(fn, foot, 0.0, 6.0),
                                segs=segments(GRID, np.array(oo), np.array(ee)))
set_phi(1.0)
ivs = lambda segs: " U ".join(f"[{a:.3f},{b:.3f}]" for a, b in segs) or "empty"
fm = lambda x: "none" if x is None else f"{x:.3f}"
if not MUTATE:
    c59 = json.load(open(os.path.join(LANES, "CFG59_universal_debris_fraction_results.json")))["numbers"]["TAB"]; dref = []
    for foot in FOOTS:
        t = REF[("U5o SLUGGS original (19, SLUGGS masses; = CFG59's U5)", foot)]; r59 = c59[f"U5 SLUGGS|{foot}"]
        dref += [abs(t["o0"] - r59["o0"]), abs(t["o1"] - r59["o1"]), abs(t["e0"] - r59["e0"]), abs(t["e1"] - r59["e1"]), abs(t["phi_ext"] - r59["phi_ext"])]
        dref += [abs(a - b) for x, y in zip(t["segs"], r59["segs"]) for a, b in zip(x, y)] + ([] if len(t["segs"]) == len(r59["segs"]) else [1.0])
    check("C1c CONTROL (reported): U5o reproduces CFG59's committed SLUGGS row (o(0), o(1), e(0), e(1), phi_ext, interval) to 1e-6", f"worst {max(dref):.1e}", max(dref) <= 1e-6, load_bearing=False)
P(f"    {'population':52s}{'foot':>10s}{'o(0)':>8s}{'z(0)':>7s}{'o(1)':>8s}{'z(1)':>7s}{'phi_need':>10s}{'phi_ext':>9s}  interval")
for lab in ("U5o SLUGGS original (19, SLUGGS masses; = CFG59's U5)", "U5s same 16, SLUGGS masses (CFG55 R1)"):
    for foot in FOOTS:
        t = REF[(lab, foot)]
        P(f"    {lab:52s}{foot:>10s}{t['o0']:+8.3f}{t['o0'] / t['e0']:+7.2f}{t['o1']:+8.3f}{t['o1'] / t['e1']:+7.2f}{fm(t['phi']):>10s}{fm(t['phi_ext']):>9s}  {ivs(t['segs'])}")
for foot in FOOTS:
    t = TAB[(4, foot)]
    P(f"    {'U5d SLUGGS dynamical masses (16)  <-- THE POPULATION':52s}{foot:>10s}{t['o0']:+8.3f}{t['o0'] / t['e0']:+7.2f}{t['o1']:+8.3f}{t['o1'] / t['e1']:+7.2f}{fm(t['phi']):>10s}{fm(t['phi_ext']):>9s}  {ivs(t['segs'])}")
P("    galaxies excluded from U5d's mean (phi-scaled debris alone exceeds M_JAM/2) at phi = 0, 0.5, 1 : " + "; ".join(
    f"{f}: " + "/".join(str(int(np.isnan(per_gal_dyn(f, ph)).sum())) for ph in (0.0, 0.5, 1.0)) for f in FOOTS))
# extended band on [0, 6]
EXT = {}
for foot in FOOTS:
    pg = np.round(np.arange(0.0, 6.0001, 0.05), 10); oo, ee, nn = [], [], []
    for ph in pg:
        set_phi(ph); off = per_gal_dyn(foot, ph); ok = np.isfinite(off)
        oo.append(float(off[ok].mean()) if ok.sum() >= 3 else float("nan")); ee.append(float(off[ok].std(ddof=1) / math.sqrt(ok.sum())) if ok.sum() >= 3 else float("nan")); nn.append(int(ok.sum()))
    oo, ee = np.array(oo), np.array(ee); good = np.isfinite(oo)
    fneg = np.where(good & (oo <= 0))[0]
    EXT[foot] = dict(phi=pg.tolist(), o=oo.tolist(), e=ee.tolist(), n=nn, first_nonpositive=(float(pg[fneg[0]]) if len(fneg) else None),
                     band=(segments(pg[good], oo[good], ee[good])))
    P(f"    [{foot}] extended scan phi in [0,6] step 0.05: n galaxies {min(nn)}-{max(nn)}; first grid phi with o <= 0: {EXT[foot]['first_nonpositive']}; 1-sigma band on [0,6] (informational): {ivs(EXT[foot]['band'])}")
    P("        o(phi) at phi = 0, 1, 2, 3, 4, 5, 6: " + ", ".join(f"{oo[k]:+.3f}(n{nn[k]})" for k in (0, 20, 40, 60, 80, 100, 120)))
set_phi(1.0)
CLS = {}
for foot in FOOTS:
    t = TAB[(4, foot)]; u4 = TAB[(3, foot)]
    u4hi = max(b for a, b in u4["segs"]) if u4["segs"] else None
    if t["segs"]:
        lo, basis = min(a for a, b in t["segs"]), "1-sigma interval lower edge"
    elif t["phi_ext"] is not None:
        lo, basis = t["phi_ext"], "extended ROOT (no 1-sigma statement)"
    elif EXT[foot]["band"]:
        lo, basis = min(a for a, b in EXT[foot]["band"]), "extended 1-sigma band lower edge on [0,6]"
    else:
        lo, basis = None, "no root or band on [0,6]"
    above = (lo is not None) and lo > 0.30
    CLS[foot] = dict(lo=lo, basis=basis, u4hi=u4hi, gap=(None if lo is None or u4hi is None else lo - u4hi), above030=above, interval=t["segs"], phi=t["phi"], phi_ext=t["phi_ext"])
    P(f"  [{foot}] U5d: phi_needed in [0,1] {fm(t['phi'])}; phi_needed_ext {fm(t['phi_ext'])}; interval {ivs(t['segs'])}; basis for the gap: {basis} = {fm(lo)}; "
      f"U4 (LVD) upper edge {fm(u4hi)}; SLUGGS-LVD gap {('n/a' if CLS[foot]['gap'] is None else f'{CLS[foot][chr(103)+chr(97)+chr(112)]:+.3f}')} (CFG59: canonical +0.507, alt +0.460); entirely above 0.30: {above}")
survives = all(CLS[f]["above030"] for f in FOOTS)
resolved = overall
verdict = "RESOLVED" if resolved else ("SURVIVES" if survives else "MIXED")
P(f"\n  PRE-DECLARED CLASSIFICATION: the conflict {verdict}.   universal-phi answer: canonical {'YES' if ANS['canonical']['yes'] else 'NO'}; alt {'YES' if ANS['alt']['yes'] else 'NO'}; OVERALL {'YES' if overall else 'NO'} (CFG59: NO/NO/NO)")
for foot in FOOTS:
    if ANS[foot]["binding"][2] is not None:
        b = ANS[foot]["binding"]; P(f"    [{foot}] binding pair in the CFG71 table: largest lower edge {b[0][0]} at {b[0][1][0]:.3f}; smallest upper edge {b[1][0]} at {b[1][1][1]:.3f}; hull gap {b[2]:+.3f}")
    P(f"    [{foot}] disjoint pairs: " + "; ".join(f"{a.split(' ')[0]}-{b_.split(' ')[0]} {g_:.3f}" for a, b_, g_ in sorted(ANS[foot]['disjoint_pairs'], key=lambda t_: -t_[2])[:8]))

R.banner("R2 (added after the first main run, before interpretation; reported only, no gate/grid/threshold/population changed)")
P("    U5d's z = o/e on the [0,1] grid: at phi = 0.30 and at U4's upper edge, and its smallest |z| over [0,1].  DISCLOSURE: the docstring's classification is undefined when U5d has no interval AND no root on [0,6];")
P("    the code's fallback (the extended 1-sigma band, informational) was written before the first run but not declared in the docstring, and gives 'MIXED' when one footing has no band; read the verdict with this in mind.")
R2 = {}
for foot in FOOTS:
    o_, e_ = SCAN[(4, foot)]["o"], SCAN[(4, foot)]["e"]; z_ = np.abs(o_) / e_; k30 = int(np.argmin(np.abs(GRID - 0.30))); u4hi = CLS[foot]["u4hi"]; ku = int(np.argmin(np.abs(GRID - u4hi)))
    R2[foot] = dict(z_at_030=float(o_[k30] / e_[k30]), z_at_u4hi=float(o_[ku] / e_[ku]), min_absz=float(z_.min()), phi_at_min=float(GRID[int(np.argmin(z_))]))
    P(f"    [{foot}] o/e at phi = {GRID[k30]:.2f}: {R2[foot]['z_at_030']:+.2f}; at phi = {GRID[ku]:.2f} (U4 upper edge {u4hi:.3f}): {R2[foot]['z_at_u4hi']:+.2f}; smallest |o/e| on [0,1]: {R2[foot]['min_absz']:.2f} at phi = {R2[foot]['phi_at_min']:.2f} (a 1-sigma interval would need <= 1)")
R.num("R2", R2)

R.banner("GROUPED by the population's median log M_* (descriptive split declared in advance): < 7, 7-10, > 10")
BINS = (("logM* < 7", lambda m: m < 7), ("7 <= logM* <= 10", lambda m: 7 <= m <= 10), ("logM* > 10", lambda m: m > 10))
GROUPS = {}
for bn, pr in BINS:
    mem = [i for i in range(len(POPS)) if pr(TAB[(i, "canonical")]["meta"]["logMs"])]
    for foot in FOOTS:
        inter = [(0.0, 1.0)]
        for i in mem:
            inter = intersect(inter, TAB[(i, foot)]["segs"])
        GROUPS[(bn, foot)] = dict(members=[NAMES[i] for i in mem], inter=inter)
        P(f"  {bn:18s} [{foot:9s}] n_pop {len(mem)}: " + (("common intersection " + (" U ".join(f"[{a:.3f},{b:.3f}]" for a, b in inter)) if inter else "EMPTY (no common phi)") if mem else "no populations")
          + ("   members: " + ", ".join(n.split(' ')[0] for n in GROUPS[(bn, foot)]["members"]) if foot == "canonical" else ""))

R.banner("R1 (added after the first main run, before interpretation; reported only): the smallest sets of populations whose removal leaves a common intersection")
import itertools
MINSETS = {}


def minsets(members, foot):
    for k in range(0, len(members) + 1):
        out = []
        for rem in itertools.combinations(members, k):
            inter = [(0.0, 1.0)]
            for i in members:
                if i not in rem:
                    inter = intersect(inter, TAB[(i, foot)]["segs"])
            if inter and len(rem) < len(members):
                out.append((rem, inter))
        if out:
            return k, out
    return None, []


for lab, mem in (("all ten", list(range(len(POPS)))),) + tuple((bn, [i for i in range(len(POPS)) if pr(TAB[(i, "canonical")]["meta"]["logMs"])]) for bn, pr in BINS):
    for foot in FOOTS:
        if not mem:
            continue
        k, out = minsets(mem, foot)
        MINSETS[(lab, foot)] = dict(k=k, sets=[([NAMES[i] for i in rem], inter) for rem, inter in out])
        P(f"  {lab:18s} [{foot:9s}] minimal removals k = {k}: " + ("; ".join("drop {" + ", ".join(NAMES[i].split(' ')[0] for i in rem) + "} -> " + " U ".join(f"[{a:.3f},{b:.3f}]" for a, b in inter) for rem, inter in out[:8])
                                                             + (f" (+{len(out) - 8} more)" if len(out) > 8 else "")))

R.banner("SPEARMAN (descriptive only; n <= 10)")
SP = {}
for foot in FOOTS:
    for lab, key in (("phi_needed in [0,1]", "phi"), ("phi_needed_ext (root on [0,6])", "phi_ext")):
        idx = [i for i in range(len(POPS)) if TAB[(i, foot)][key] is not None]
        for xn, xf in (("log M_*", lambda i: TAB[(i, foot)]["meta"]["logMs"]), ("log(M_ph,edge/M_c)", lambda i: TAB[(i, foot)]["meta"]["logratio"])):
            if len(idx) >= 4:
                rho, p = spearmanr([TAB[(i, foot)][key] for i in idx], [xf(i) for i in idx])
                SP[(foot, lab, xn)] = dict(rho=float(rho), p=float(p), n=len(idx))
                P(f"  [{foot:9s}] {lab:32s} vs {xn:20s}: rho {rho:+.2f}  (p {p:.2f}, n = {len(idx)})")
            else:
                SP[(foot, lab, xn)] = dict(rho=None, p=None, n=len(idx)); P(f"  [{foot:9s}] {lab:32s} vs {xn:20s}: n = {len(idx)} < 4, not computed")

# ---------------------------------------------------------------------------------------------------------------- headline
R.banner("HEADLINE / REPORT")
u1 = all(TAB[(0, f)]["phi"] is not None for f in FOOTS)
check("H1 [HEADLINE; MUTATE must fail] THE ULTRA-FAINTS HAVE A SOLUTION: phi_needed exists in [0,1] for U1 (KM median), both footings" + ("  [MUTATE: collapse masses / 100]" if MUTATE else ""),
      "; ".join(f"{f}: o(0) {TAB[(0, f)]['o0']:+.3f}, o(1) {TAB[(0, f)]['o1']:+.3f}, phi_needed " + (f"{TAB[(0, f)]['phi']:.3f}" if TAB[(0, f)]["phi"] is not None else "none") for f in FOOTS), u1)
check("H2 (reported) the universal-phi answer", f"canonical {'YES' if ANS['canonical']['yes'] else 'NO'}; alt {'YES' if ANS['alt']['yes'] else 'NO'}; OVERALL {'YES' if overall else 'NO'}", True, load_bearing=False)
check("H3 (reported) U5d has no phi_needed in [0,1], both footings" + (" [expected in the MUTATE run]" if MUTATE else ""),
      "; ".join(f"{f}: {fm(TAB[(4, f)]['phi'])} (ext {fm(TAB[(4, f)]['phi_ext'])})" for f in FOOTS), all(TAB[(4, f)]["phi"] is None for f in FOOTS), load_bearing=False)
check("H4 (reported) the pre-declared classification", f"the conflict {verdict}", True, load_bearing=False)
P("\n  READING (declared): YES would be consistency with a universal debris fraction on these lanes, not a derived rule; NO means the lanes' offsets are not reconciled by one multiplier "
  "of the sum's debris term.  Nothing here says the theory is closed; no phi is selected, fitted or recommended.")


def ser(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else "|".join(map(str, k))): ser(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [ser(v) for v in o]
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


R.num("TAB", ser({f"{NAMES[i]}|{f}": v for (i, f), v in TAB.items()}))
R.num("MINSETS", ser(MINSETS)); R.num("CLS", ser(CLS)); R.num("EXT", ser(EXT)); R.num("REF", ser({f"{k[0]}|{k[1]}": v for k, v in REF.items()})); R.num("verdict", verdict); R.num("ANS", ser(ANS)); R.num("overall", overall); R.num("GROUPS", ser(GROUPS)); R.num("SPEARMAN", ser(SP)); R.num("allsegs", allsegs)
R.num("scan", ser({f"{NAMES[i]}|{f}": dict(phi=GRID, o=v["o"], e=v["e"]) for (i, f), v in SCAN.items()}))
nf = R.write(here=OUT)
sys.exit(1 if nf else 0)
