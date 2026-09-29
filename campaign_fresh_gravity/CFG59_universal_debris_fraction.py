#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG59 -- DOES A SINGLE UNIVERSAL FRACTION phi OF THE COLLAPSE DEBRIS RECONCILE EVERY POPULATION B'S SUM RULE HAS BEEN SCORED ON?
(a descriptive consistency question; NOT a search for a rule that passes)

FROZEN QUESTION (verbatim):
  'Across the populations where B's derived cold-mass rule (the sum, reading S of CFG45) has been scored, does a SINGLE universal fraction phi of the leftover
  collapse debris reconcile them all? For each population, scale the debris acceleration (the rule's added term G f_ex (1-f_b) M_NFW(<r)/r^2) by phi in [0,1]
  (phi=0 is the bare law, phi=1 is the sum) and find phi_needed = the value at which the population's declared offset is zero, with the interval of phi whose
  offset lies within 1 sigma of zero (the lane's own error model). The answer is YES only if the intervals of ALL populations in the declared set have a
  non-empty common intersection; otherwise NO, and the harness reports which populations conflict and by how much. No phi is selected, fitted or recommended;
  a YES would be recorded as consistency with a universal fraction, not as a derived rule.'

STANDING (from the program): kappa = 1/2 is FITTED; nothing here says the theory is closed; no tuning after seeing a result; every claim is this committed-style script
plus a MUTATE control that must fail.  A YES would mean only "consistent with a universal fraction"; a NO means the sum's over-prediction and the bare law's
under-prediction are not two ends of ONE knob on these lanes.  Neither is a derived rule.

MACHINERY (declared).  CFG45_rule_readings.py is exec'd READ-ONLY up to its own controls (its prefix, MUTATE handled by the environment exactly as CFG45 does), which
exec's the lane scripts (CFG42, CFG36/CFG35, CFG38, CFG40, CFG41) read-only.  Its function `extra_acc` is REPLACED IN THE EXEC NAMESPACE (no repo file is edited) by a
version with one added reading, "P": g_extra(P) = phi x g_extra(S), phi a global set by this harness.  Every lane estimator (sigma_read, sluggs_sigma, xray_gal, pred41,
stat41, ufd_stat, boot, offs, km_median ...) is then CFG45's own function, called with reading "P".  CFG51's prefix is exec'd read-only the same way (its FG001 slices,
its Walker+2023 reduced table, its spred); its rule term is re-written here with the same phi.  Nothing is re-fitted: phi enters ONLY as that multiplier.

POPULATIONS (declared; exactly these ten; each with the lane's own declared offset and error model, both footings 'canonical' | 'alt'):
  U1  MW ultra-faints (CFG42 H1): Kaplan-Meier median of log10(sigma_obs/sigma_pred) with the 9 upper limits; error = sqrt(bootstrap(1000, seed 42)^2 + Upsilon_V floor^2
      (half the |shift| for Upsilon_V 1 -> 4) + collapse-mass floor^2 (half the range over M_c = 1e8..1e10 for the M_* < 1e5 systems)).  The error model is RE-EVALUATED at
      every phi (the floors and the bootstrap use the phi-scaled reading).
  U2  MW classical dSphs (14), U3 M31 Collins+13 (14), U4 M31 LVD (34): CFG42 H2 with the infall gas; sample median offset; error = sqrt((1.2533 std/sqrt n)^2 + Upsilon floor^2 +
      collapse floor^2) re-evaluated at every phi.
  U5  SLUGGS (19 early types, CFG38 H1): mean over galaxies of the outer-bin mean of log10(sigma_obs/sigma_pred) (h50 machinery, red relation); error std/sqrt(19), re-evaluated.
  U6  X-ray ellipticals (7, CFG36 H1): per-galaxy median over 5,10,20,40,70 kpc of log10(M_total/M_pred); sample mean; error = sqrt(err^2 + Salpeter-shift^2 + (radii <= 40 kpc)-shift^2)
      re-evaluated at every phi.
  U7  the four Di Teodoro+2023 S0/S0a (CFG41 H2b): mean corrected offset (log10(v_flat/v_pred) - B, B = 0.076), point-mass headline; error = CFG45's s0err (sample sem, model, M_*, M_gas,
      radius, B floors) re-evaluated at every phi.
  U8  UGC 2487 (SPARC's S0): offset log10(V_flat / v_pred(R_HI)); error as CFG45 declared it (SIG_UGC: measurement, 0.5 x 0.1003 law rms, 0.25 x 0.2 M_*), phi-independent.
  U9  Bootes I and U10 Tucana II (CFG51, Walker+2023 multi-epoch, binary-cleaned dispersion): offset log10(sigma_clean / sigma_pred), sigma_pred = FG001's estimator with the
      phi-scaled CFG42 sum term (Moster collapse mass, clamped by halo_mass, M_c as CFG51); error = CFG51's err_dex on the cleaned dispersion (reduction interval + Upsilon/deep-MOND floor),
      phi-independent.  U9, U10 are two SEPARATE populations (two objects each: no sample statistic); they share stars/galaxies with U1 only through the ultra-faint class.
  (SPARC dwarfs, SPARC >= 10 and Ogle are NOT in the set: CFG45 scored them as an unchanged-by-the-rule constraint (A3) or reported-only, not as an offset with an error model
  that the sum is compared to.  They are not used here.)

DEFINITIONS (declared before the first run).
  offset o_p(phi, footing); error e_p(phi, footing) = the lane's model evaluated with the phi-scaled reading.  All o_p are non-increasing in phi (a larger debris term raises the
  predicted sigma / v / mass ratio ... see the monotonicity control), so the zero is unique.
  phi_needed[p] = the root of o_p(phi) = 0 on [0,1] (brentq, xtol 1e-9 on the offset alone).  'no solution in [0,1]' if o_p(0) and o_p(1) have the same sign; the signs are reported.
  phi_needed_ext[p] (reported only, NOT part of the YES/NO) = the root on [0, 6] if it exists (only to say how far outside [0,1] a no-solution population sits).
  interval[p] = { phi in [0,1] : |o_p(phi)| <= e_p(phi) } from a grid of 101 points (step 0.01, both o and e evaluated at every grid point), the edges by linear
  interpolation of e - |o| between adjacent grid points.  It may be empty, and it may exist when phi_needed does not (the zero lies outside [0,1] but the 1-sigma band reaches in).
  ANSWER (per footing) = YES iff every one of the ten intervals is non-empty and the ten intervals have a non-empty common intersection; otherwise NO, with: the empty-interval
  populations; the binding pair (the largest lower edge, the smallest upper edge, their gap in phi); every disjoint pair.  OVERALL = YES iff both footings are YES.  (Also
  reported: the intersection of all twenty footing-population intervals.)
  GROUPED (DESCRIPTIVE SPLIT, declared): populations are assigned to log M_* bins by the population's median log10 M_* (the lane's own stellar mass): < 7, 7-10, > 10.  The
  intersection is reported per bin and footing (an empty bin is reported as empty, not as YES).
  SPEARMAN (descriptive only): rank correlation of phi_needed (populations with a root in [0,1]; and separately phi_needed_ext) with (a) the population's median log10 M_*, (b) the
  population's median log10(M_phantom,edge / M_c) (M_phantom,edge = the law's phantom inside r_e = 0.40 r_ta, CFG35's, and M_c the collapse mass, both as each lane uses them).
  scipy.stats.spearmanr; n and p reported; at n <= 10 nothing here is a significance claim.

CONTROLS
  C1  CONTROL  phi = 1 reproduces CFG45's reading (S) and phi = 0 its (L) for every population, both footings, to 1e-9 (offsets and errors, computed here against the same functions with
               the reading letters "S" / "L"); and (non-MUTATE run) the committed CFG45 / CFG51 results files to 1e-6 (CFG42 UF/CL, CFG36 X-ray, CFG38 SLUGGS, CFG41 S0, CFG45 UGC 2487,
               CFG51 Bootes I / Tucana II offsets, bare and rule).
  C2  CONTROL  every o_p(phi) is non-increasing on the 101-point grid (tolerance 1e-9 dex) for every population and footing.
  C3  CONTROL  the MUTATE run: every collapse mass divided by 100 (CFG45's MCF, and the CFG51 rule); see H1.
  H1  [HEADLINE; MUTATE must fail] the ultra-faint populations have a solution: phi_needed exists in [0,1] for U1 (KM median, both footings).  In the MUTATE run the debris is 1/100:
      the bare-law failure cannot be closed by any phi, U1 has no solution, and H1 must FAIL (rc = 1).
  H2  (reported) the table, the YES/NO per footing and overall, the groups, the Spearman correlations.
MUTATE=1: collapse masses / 100 (CFG45's MCF; and the collapse mass in the CFG51 systems' rule).
ADDED AFTER THE FIRST MAIN RUN, BEFORE ANY INTERPRETATION (disclosed; reported only, no gate, grid, threshold or population changed): R1, an exhaustive search over the 2^10 sub-collections
  for the SMALLEST number of populations whose removal makes the common intersection non-empty (per footing, and per mass bin).  It says which populations carry the conflict; it selects no phi.
Nothing is selected, fitted or recommended; no grid, threshold or population is changed after the first run.
Run: python3 CFG59_universal_debris_fraction.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib, json
import numpy as np
from scipy.optimize import brentq
from scipy.stats import spearmanr

sys.dont_write_bytecode = True
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
OUT = os.environ.get("CFG59_OUT", os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LANES)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG59_universal_debris_fraction", MUTATE)
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
        ("U5 SLUGGS", p_sluggs), ("U6 X-ray ellipticals", p_xray), ("U7 DT23 four S0/S0a", p_s0), ("U8 UGC 2487", p_ugc),
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
        for r in RES50:
            add(r["Mstar"], r["Mstar"], collapse(r["Mstar"], "red") * MCF)
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
            d2.append((f"SLUGGS {foot} {rd}", abs(o(4) - c45["SLUGGS"][f"{foot}|{rd}"]["mean"]), 1e-6))
            d2.append((f"XRAY {foot} {rd}", abs(o(5) - c45["XRAY"][f"{foot}|{rd}"]["mean"]), 1e-6))
            d2.append((f"S0 {foot} {rd}", abs(o(6) - c45["DT23"][f"{foot}|{rd}"]["s0"]["corr"]), 1e-6))
            d2.append((f"UGC {foot} {rd}", abs(o(7) - c45["UGC2487"][f"{foot}|{rd}"]["off"]), 1e-6))
            for j, nm in ((8, "Bootes I"), (9, "Tucana II")):
                d2.append((f"{nm} {foot} {rd}", abs(o(j) - c51["RES"][f"{nm}|{foot}|{'rule' if rd == 'S' else 'clean'}"]["off"]), 1e-6))
    check("C1b CONTROL: the endpoints reproduce the committed CFG45 / CFG51 results files to 1e-6 (UF, CL x3, SLUGGS, X-ray, S0, UGC 2487, Bootes I, Tucana II; both footings, S and L)",
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
R.num("MINSETS", ser(MINSETS)); R.num("ANS", ser(ANS)); R.num("overall", overall); R.num("GROUPS", ser(GROUPS)); R.num("SPEARMAN", ser(SP)); R.num("allsegs", allsegs)
R.num("scan", ser({f"{NAMES[i]}|{f}": dict(phi=GRID, o=v["o"], e=v["e"]) for (i, f), v in SCAN.items()}))
nf = R.write(here=OUT)
sys.exit(1 if nf else 0)
