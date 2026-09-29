#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG69 -- IS EACH FAILURE OF CANDIDATE B SPECIFIC TO B, OR SHARED BY A STANDARD LCDM HALO RUN THROUGH THE IDENTICAL DATA, ESTIMATOR, SIGMA TREATMENT AND FLOORS?

FROZEN QUESTION (verbatim):
  'For each population where candidate B (the bare law L or the sum rule S) fails or is marginal -- (a) SLUGGS massive early types with JAM-calibrated stellar masses
  (CFG55: law +0.097 dex 4.0 sigma, rule +0.046 2.6 sigma, 16 of 19), (b) the Milky Way ultra-faints (CFG42's 31 resolved + 9 limits KM median +0.325 dex law; CFG46's
  eight binary-corrected systems; CFG51/CFG66's Bootes I and Tucana II multi-epoch cleaned), (c) the classical satellites and M31 dwarfs (CFG42: MW classical, M31 Collins,
  M31 LVD; CFG58's LV field dwarfs) -- is the failure SPECIFIC to B, or is it SHARED by a standard LCDM halo run through the IDENTICAL data, estimator, sigma treatment
  and floors?  A failure is SHARED if the LCDM offset has the same sign and |z| > 2 under the lane's own error model (with the same collapse-mass floor treatment as CFG42);
  SPECIFIC-TO-B if LCDM is within 2 sigma; LCDM-WORSE if LCDM has the opposite sign at > 2 sigma.'

STANDING (declared): kappa = 1/2 is FITTED for B; nothing is tuned after a result is seen; any result is valid; nothing here says the data favour B or LCDM, and nothing says the
theory is closed.  Every claim is this script plus a MUTATE control that must fail.  Nothing in the repository is edited; the lanes' scripts are exec'd READ-ONLY.

THE LCDM MODEL (declared ONCE; identical for every population; no per-population tuning):
  stars (each lane's own stellar mass, each lane's own gas) inside a standard NFW halo.  Virial mass M_h = the Moster+2013 stellar-to-halo relation of h48 (`halo_mass`, as CFG35 /
  CFG42 use it) evaluated at the lane's own M_* (the satellites: Upsilon_V L_V with Upsilon_V = 2, as CFG42), CLAMPED at M_h = 1e9 Msun below M_* ~ 1.6e4 Msun (the grid floor;
  CFG42's declared trap; the sensitivity M_h = 1e8, 3e8, 1e9, 3e9, 1e10 for every satellite with M_* < 1e5 is CFG42's floor and enters the error exactly as it does there).
  Concentration: the Duffy+2008 FULL-sample Delta = 200 x CRITICAL row, c = 5.71 (M_200c / [2e12 / h])^-0.084, h = 0.674, z = 0 -- CFG65's row A2, the one whose convention matches
  h48's 200c R200 (CFG65 transcribed its coefficients from the paper; this script does not re-verify them against the paper, only re-uses them).  Shape NFW, m(t) = ln(1+t) - t/(1+t),
  x = r/R200 clipped to [1e-4, 5], mass normalised to M_h at R200 (CFG65's `make_profile`, copied).  Added mass: (1 - f_b) M_h m(c x)/m(c) with f_b = Omega_b/Omega_m of CFG35 (the
  same (1 - f_b) suppression CFG42 uses for the collapse mass), i.e. f_ex = 1: the FULL halo.  NO phantom and NO law: the acceleration is purely Newtonian, g = G [M_b(<r) +
  (1 - f_b) M_NFW(<r)] / r^2 -- nu = 1.  NO adiabatic contraction (declared once: UNTESTED here; AC would deepen the stellar-dominated inner potential and raise the LCDM
  dispersions).  LCDM has no a_0, so its numbers are IDENTICAL on the two footings (9.36e-11 / 1.13e-10 enter only B's L and S).
  The prediction enters each lane's estimator exactly where the rule's debris enters, with the law switched off: the satellites' sigma^2 = g(r) r / 3 at r = (4/3) r_half with half
  of the baryons enclosed (FG001 / CFG42); SLUGGS's isotropic Jeans integral (CFG38 / h50, gamma = 3 tracer, Hernquist stars at a = R_e / 1.8153, outer bins); CFG55's JAM
  calibration (the model's total mass inside the 3D half-light radius equals M_JAM / 2, half the stars inside, solved for M_*: for LCDM 0.5 M_* + (1 - f_b) M_NFW(<r_1/2; M_h(M_*),
  c) = M_JAM / 2, the Moster halo tied to the solved M_*).

THE POPULATIONS AND THEIR STATISTICS (each lane's own; L and S are taken from the lanes' own exec'd machinery and controlled against the committed JSONs; LCDM is scored with the
same generic estimator code that also re-derives L and S, controlled against the lanes):
  a1 SLUGGS JAM-calibrated, 16 of 19 (CFG55; law +0.097 / rule +0.046); statistic: mean over galaxies of the outer-bin mean of log10(sigma_obs/sigma_pred); error std/sqrt(n).
     For the LCDM a galaxy whose NFW mass inside r_1/2 alone already exceeds M_JAM / 2 cannot be calibrated and is EXCLUDED (counted; as CFG55 does for the rule).
  a2 SLUGGS with SLUGGS's own stellar masses, 19 (CFG38; law +0.080, rule +0.007).      a3 the same 16 with SLUGGS's masses (CFG55 R1).
  b1 MW ultra-faints, 31 resolved + 9 limits, Kaplan-Meier median (CFG42 H1; error sqrt(bootstrap(1000, seed 42)^2 + Upsilon_V^2 + collapse-mass floor^2)).
  b2 CFG46's eight binary-corrected systems, median offset (headline f free; also f = 0 and f = 0.7); error sqrt(bootstrap^2 + measurement^2 + floor^2), the floor = half the range over
     Upsilon_V 1, 2, 4 (+ the pure deep-MOND estimator for L, which has no LCDM meaning).  For LCDM the collapse-mass floor is ADDED (CFG42's treatment, declared here); z is also
     reported without it.  S is CFG46's committed rule (its own error, no collapse floor).
  b3 Bootes I and b4 Tucana II binary-cleaned (CFG51: offset log10(sigma_clean/sigma_pred), error sqrt(e_stat^2 + floor^2), floor = half the range over Upsilon_V 1, 2, 4 (+ deep MOND
     for L)); for S and LCDM the same with the collapse-mass floor added (S, not committed with an error in CFG51, is scored with exactly the LCDM error model).
  b5 Bootes I total-mixture, b6 Bootes I cold-only, b7 Tucana II gradient-removed (CFG66's committed maximum-likelihood dispersions and profile intervals, read from its JSON; the
     same error model as b3/b4).
  c1 MW classical (14), c2 M31 Collins+13 (14), c3 M31 LVD (34) with the CFG18 infall gas (CFG42 H2: sample median; error sqrt((1.2533 std/sqrt n)^2 + Upsilon^2 + collapse^2)).
  c4 the isolated Local-Volume field dwarfs (CFG58 d2, n = 13, no gas, CFG42's error model).
  Sign: offset = log10(obs / pred); positive = the data sit ABOVE the prediction (under-prediction).  z = offset / the lane's total error.

CLASSIFICATION (declared, exactly the frozen rule), applied SEPARATELY to L and to S, on each footing where the population is a B failure or marginal:
  B status per footing: FAIL if |z| > 2; MARGINAL if 1 < |z| <= 2; OK if |z| <= 1 (then no classification: 'B-ok').  For a FAIL or MARGINAL B:
    LCDM |z| <= 2 -> SPECIFIC-TO-B;  LCDM same sign as B and |z| > 2 -> SHARED;  LCDM opposite sign and |z| > 2 -> LCDM-WORSE.
  If the two footings give different classes the row reads MIXED.  'Marginal' (1 < |z| <= 2) is this script's declared reading of the frozen word.

REPORTED-ONLY SENSITIVITY (never enters a classification): LCDM with (V1) the Dutton-Maccio concentration of h48 in place of Duffy, (V2) the Duffy RELAXED-sample 200c row
  (6.71, -0.091), (V3, V4) every halo mass x 1/3 and x 3 (a stand-in for the SHMR scatter / systematics; the Moster relation carries no scatter in `halo_mass`), (V5, SLUGGS only) the
  Mandelbaum+2016 red collapse masses of CFG36 with h48's Dutton-Maccio c (CFG38's own post-hoc LCDM form).  The collapse-mass clamp sensitivity (1e8...1e10) is reported per row.

CONTROLS
  C1 CONTROL (i)  the LCDM engine, run through CFG38's SLUGGS machinery with SLUGGS's own stellar masses in CFG38's form (Mandelbaum red collapse masses + Dutton-Maccio c), reproduces
                  CFG38's committed post-hoc LCDM offsets galaxy by galaxy to 1e-9 and its printed -0.037 +- 0.017 (-2.1 sigma).  (non-MUTATE)
  C2 CONTROL (ii) L and S reproduce the committed lane numbers to 1e-6 (CFG42 UF / CL, CFG46, CFG51, CFG66's L offsets, CFG58 d2, CFG55 JAM, CFG38 SLUGGS), both footings; the generic
                  estimator code used for LCDM also reproduces the lanes' L and S (recomputed through it).  (non-MUTATE)
  C3 CONTROL      the generic NFW profile with Duffy c equals the analytic enclosed mass (direct numerical integration of the NFW density) to 1e-7, with M(<R200) = M_h to 1e-12, monotone;
                  and with the Dutton-Maccio c equals h48's committed `nfw_enclosed` to 1e-9 (30 masses x 40 radii).
  C4 CONTROL      the LCDM engine with M_h -> 0 is the pure Newtonian prediction (satellite sigma = sqrt(G 0.5 M_b / r_h / 3 ...) closed form to 1e-9), LCDM is identical on both footings, and
                  the LCDM sigma exceeds the Newtonian one (mass is added, never removed).
  H1 [HEADLINE; MUTATE must fail]  the LCDM ultra-faint gate is live: the KM median of b1 within 2 sigma of zero on BOTH footings (the same gate as CFG42 H1).
  C5 CONTROL (MUTATE=1: every LCDM halo mass x 100) the LCDM ultra-faint gate must FAIL; the MUTATE run also reports whether the gate was passed in the un-mutated run (read from
                  the committed .json of the un-mutated run if present).
  H2 (reported) the classification table.
MUTATE=1: every LCDM halo mass (and every floor variant) x 100 -- H1 must FAIL (rc = 1).  L and S are un-mutated (their lanes are exec'd with their own MUTATE off).
ADDED AFTER THE FIRST MAIN RUN, BEFORE ANY INTERPRETATION (disclosed; the first run's log is kept as run_first.log; NO hypothesis, gate, threshold, model choice or classification rule changed):
  (1) control C6: the LCDM JAM calibration is verified -- at every calibrated galaxy the LCDM total mass inside r_1/2 equals M_JAM / 2 to 1e-9, and with the halo switched off the solved
      stellar mass returns M_JAM to 1e-9 (CFG55's C3 analogue); (2) a reported column 'B minus LCDM' (dex) beside the classification, because for a MARGINAL B (|z| <= 2) the label
      SPECIFIC-TO-B only says the LCDM is inside 2 sigma; (3) the table's column widths and per-galaxy LCDM SLUGGS offsets in the JSON.
  (4) THE DECLARED MUTATE CONTROL FAILED (kept as a FAIL, run_mutate_first.log): with every LCDM halo mass x 100 the LCDM ultra-faint gate did NOT fail (KM median +0.080 -> -0.149, |z| = 1.25 <
      2), so H1 passes in the MUTATE run and C5 fails.  Nothing was changed to make it fail.  Supplemental, REPORTED-ONLY diagnostic added after that run (R3): the same gate with every halo
      mass multiplied by 0.01, 0.1, 1, 10, 100, 1e3, 1e4, 1e5 (independent of the MUTATE switch), to show at what multiple the gate does flip and that the mutation acts in the right direction.
Run: python3 cfg69_lcdm_comparator.py   (MUTATE=1 for the control; CFG69_OUT=<dir> sets where the outputs go)
"""
import os, sys, math, io, contextlib, csv, json, time
sys.dont_write_bytecode = True
import numpy as np
from scipy import integrate
from scipy.optimize import brentq

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("CFG69_OUT", HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG69_lcdm_comparator", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every LCDM halo mass x 100 -- H1 (the LCDM ultra-faint gate) must FAIL ***")
HMUT = 100.0 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
T0 = time.time()


# ================================================================================================ read-only exec of the lanes (their own MUTATE forced off)
def exec_prefix(fname, marker, replace=None):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(LANES, fname)).read()
    pre = src[:src.index(marker)]
    for a, b in (replace or []):
        assert pre.count(a) == 1
        pre = pre.replace(a, b)
    g = {"__file__": os.path.join(LANES, fname), "__name__": "lane_" + fname}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(pre, fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


BAR = "# ================================================================================================ "
g45 = exec_prefix("CFG45_rule_readings.py", BAR + "P3 SPARC", [('READ = ("L", "S", "M", "E")', 'READ = ("L", "S")')])
g55 = exec_prefix("CFG55_sluggs_dynamical_masses.py", 'R.banner("PER GALAXY')
g46 = exec_prefix("CFG46_ufd_binary_corrected.py", 'R.banner("H1 / H2 / H3  THE EIGHT ULTRA-FAINTS")')
g51 = exec_prefix("CFG51_walker_ufd.py", 'R.banner("H1 / H2  THE TWO INFORMATIVE SYSTEMS")')

FB, halo_mass, collapse, RHO_C = g45["FB"], g45["halo_mass"], g45["collapse_raw"], g45["RHO_C"]
G_SAT, MSUN_SAT, SAMPLES, UL, LABEL, UPS_V, infall_gas = g45["G_SAT"], g45["MSUN_SAT"], g45["SAMPLES"], g45["UL"], g45["LABEL"], g45["UPS_V"], g45["infall_gas"]
km_median, boot = g45["km_median"], g45["boot"]
FLD = g45["g42"]["ns"]["fld"]
HH = 0.674
FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)
J = lambda n: json.load(open(os.path.join(LANES, n)))["numbers"]


# ================================================================================================ the LCDM halo: NFW with a declared concentration (CFG65's make_profile, nfw branch, copied)
def c_duffy_full(Mh):
    return 5.71 * (np.asarray(Mh, float) / (2e12 / HH)) ** (-0.084)


def c_duffy_relaxed(Mh):
    return 6.71 * (np.asarray(Mh, float) / (2e12 / HH)) ** (-0.091)


def c_dm(Mh):
    return 10 ** (0.905 - 0.101 * (np.log10(np.asarray(Mh, float) * 0.674) - 12.0))


def _m_nfw(t):
    return np.log1p(t) - t / (1 + t)


def make_nfw(cfn):
    def f(Mh, r_kpc):
        Mh = np.asarray(Mh, float); r_kpc = np.asarray(r_kpc, float)
        c = cfn(Mh); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        x = np.clip(r_kpc / R200, 1e-4, 5.0)
        return Mh * _m_nfw(c * x) / _m_nfw(c)
    return f


CFGS = {
    "base": dict(label="Moster + Duffy full 200c (THE declared LCDM)", cfn=c_duffy_full, hmf=HMUT, shmr="moster"),
    "V1": dict(label="V1 Moster + Dutton-Maccio c", cfn=c_dm, hmf=HMUT, shmr="moster"),
    "V2": dict(label="V2 Moster + Duffy relaxed 200c", cfn=c_duffy_relaxed, hmf=HMUT, shmr="moster"),
    "V3": dict(label="V3 base, every M_h x 1/3", cfn=c_duffy_full, hmf=HMUT / 3.0, shmr="moster"),
    "V4": dict(label="V4 base, every M_h x 3", cfn=c_duffy_full, hmf=HMUT * 3.0, shmr="moster"),
    "V5": dict(label="V5 Mandelbaum red + Dutton-Maccio (CFG38's form; SLUGGS rows only)", cfn=c_dm, hmf=HMUT, shmr="mandel"),
}
for k, v in CFGS.items():
    v["prof"] = make_nfw(v["cfn"])
    v["halo"] = (lambda Ms: float(halo_mass(Ms))) if v["shmr"] == "moster" else (lambda Ms: float(collapse(Ms, "red")))


# ================================================================================================ satellite-type estimators (generic; sigma callable in km/s)
def sat_sigma_lcdm(cfg):
    prof, hmf = cfg["prof"], cfg["hmf"]

    def sig(d, ups=None, floor_mh=None, gas=False, mh_zero=False):
        ups = UPS_V if ups is None else ups
        Ms = ups * d["LV"]
        Mb = Ms + (max(1.33 * d["MHI"], infall_gas(d)) if gas else 1.33 * d["MHI"])
        rh_pc = (4.0 / 3.0) * d["rh"]; rh = rh_pc * 3.0857e16
        Mh = float(halo_mass(UPS_V * d["LV"])) * hmf
        if floor_mh is not None and UPS_V * d["LV"] < 1e5:
            Mh = floor_mh * hmf
        if mh_zero:
            Mh = 1e-30
        g = G_SAT * (0.5 * Mb + (1 - FB) * float(prof(Mh, rh_pc / 1000.0))) * MSUN_SAT / rh ** 2
        return math.sqrt(g * rh / 3.0) / 1e3
    return sig


def sat_sigma_B(foot, reading):
    sr = g45["sigma_read"]

    def sig(d, ups=None, floor_mh=None, gas=False):
        return sr(d, foot, reading, ups=ups, floor_mh=floor_mh, gas=gas)[0]
    return sig


def ufd_generic(sig, floors_on):
    """CFG42 / CFG45's ultra-faint block (KM median, bootstrap, Upsilon floor, collapse-mass floor), with a sigma callable."""
    def stat(ups=None, floor_mh=None):
        x = np.array([math.log10(d["sig"] / sig(d, ups=ups, floor_mh=floor_mh)) for d in SAMPLES["ufd"]])
        xu = np.array([math.log10(d["sig_ul"] / sig(d, ups=ups, floor_mh=floor_mh)) for d in UL])
        return km_median(x, xu), x, xu
    m, x, xu = stat(); err = boot(x, xu)
    uv = [stat(ups=u)[0] for u in (1.0, 4.0)]; f_ups = 0.5 * abs(uv[1] - uv[0])
    flo = [stat(floor_mh=fm)[0] for fm in FLOORS] if floors_on else [m]
    f_mh = 0.5 * (max(flo) - min(flo)); tot = math.sqrt(err ** 2 + f_ups ** 2 + f_mh ** 2)
    return dict(km=m, resolved_median=float(np.median(x)), err=err, f_ups=f_ups, f_mh=f_mh, tot=tot, z=m / tot, floors=flo)


def cl_generic(sig, key, floors_on):
    """CFG42 / CFG45's classical-satellite block (gas = infall gas)."""
    smp = SAMPLES[key]
    offs = lambda **kw: np.array([math.log10(d["sig"] / sig(d, gas=True, **kw)) for d in smp])
    x = offs()
    ups = [offs(ups=u) for u in (1.0, 4.0)]; f_ups = 0.5 * abs(float(np.median(ups[1])) - float(np.median(ups[0])))
    flo = [float(np.median(offs(floor_mh=fm))) for fm in FLOORS] if floors_on else [float(np.median(x))]
    err = 1.2533 * float(np.std(x)) / math.sqrt(len(x)); tot = math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
    return dict(med=float(np.median(x)), tot=tot, z=float(np.median(x)) / tot, floors=flo)


def fld_generic(sig, floors_on):
    """CFG58 d2: the isolated LV field dwarfs (no gas), CFG42's error model."""
    offs = lambda **kw: np.array([math.log10(d["sig"] / sig(d, gas=False, **kw)) for d in FLD])
    x = offs(); ups = [offs(ups=u) for u in (1.0, 4.0)]; f_ups = 0.5 * abs(float(np.median(ups[1])) - float(np.median(ups[0])))
    flo = [float(np.median(offs(floor_mh=fm))) for fm in FLOORS] if floors_on else [float(np.median(x))]
    err = 1.2533 * float(np.std(x)) / math.sqrt(len(x)); tot = math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
    return dict(med=float(np.median(x)), tot=tot, z=float(np.median(x)) / tot, n=len(x), floors=flo)


# ---- CFG46 (eight binary-corrected): CFG46's stat(), with a sigma callable
SCORED46, split_normal = g46["SCORED"], g46["split_normal"]


def c46_generic(sig, key, kind, seed=46):
    """kind 'lcdm' (floor = half range over Upsilon 1, 2, 4; + the collapse-mass floor) -- CFG46's stat() structure, copied."""
    smp = SCORED46
    base = np.array([math.log10(g[key] / sig(g)) for g in smp]); m0 = float(np.median(base))
    rng = np.random.default_rng(seed)
    bs = [float(np.median(base[rng.integers(0, len(base), len(base))])) for _ in range(2000)]
    mc = []
    for _ in range(2000):
        vals = [split_normal(rng, g[key], g[key + "_p1"], g[key + "_m1"], 1)[0] for g in smp]
        mc.append(float(np.median([math.log10(v / sig(g)) for v, g in zip(vals, smp)])))
    fl = [float(np.median([math.log10(g[key] / sig(g, ups=u)) for g in smp])) for u in (1.0, 2.0, 4.0)]
    floor = 0.5 * (max(fl) - min(fl))
    flo = [float(np.median([math.log10(g[key] / sig(g, floor_mh=fm)) for g in smp])) for fm in FLOORS]
    cf = 0.5 * (max(flo) - min(flo))
    tot0 = math.sqrt(np.std(bs) ** 2 + np.std(mc) ** 2 + floor ** 2); tot = math.sqrt(tot0 ** 2 + cf ** 2)
    return dict(med=m0, boot=float(np.std(bs)), meas=float(np.std(mc)), floor=floor, cfloor=cf, tot=tot, z=m0 / tot, tot_nocf=tot0, z_nocf=m0 / tot0)


# ---- CFG51 / CFG66 two-object lane: offset of a dispersion s, and the CFG51 error model
GAL51 = {g["name"]: g for g in g51["GAL"]}


def err_two(g, s, plus, minus, sig, kind, foot=None):
    """CFG51's error model: e = asymmetric interval in dex; floor = half the range of the offset over Upsilon 1,2,4 (+ pure deep MOND for L).  'lcdm'/'S': + collapse-mass floor."""
    e = 0.5 * (math.log10(1 + plus / s) + abs(math.log10(max(1 - minus / s, 1e-3))))
    ofs = [math.log10(s / sig(g, ups=u)) for u in (1.0, 2.0, 4.0)]
    if kind == "L":
        ofs.append(math.log10(s / g51["spred"](g, foot, deep=True)))
    fl = 0.5 * (max(ofs) - min(ofs))
    cf = 0.0
    if kind != "L":
        fm = [math.log10(s / sig(g, floor_mh=f_)) for f_ in FLOORS]; cf = 0.5 * (max(fm) - min(fm))
    off = math.log10(s / sig(g))
    tot = math.sqrt(e ** 2 + fl ** 2 + cf ** 2)
    return dict(off=off, tot=tot, z=off / tot, e=e, fl=fl, cf=cf)


# CFG66's committed maximum-likelihood dispersions and profile intervals (read from its JSON, as data)
C66 = J("CFG66_bootes_tucana_systematics_results.json")
_p = C66["Q1_mixture"]["profile"]
DISP_TWO = {   # key -> (galaxy, sigma, plus, minus)
    "b3": ("Bootes I", g51["GAL"][0]["clean"], g51["GAL"][0]["clean_p"], g51["GAL"][0]["clean_m"]),
    "b4": ("Tucana II", g51["GAL"][1]["clean"], g51["GAL"][1]["clean_p"], g51["GAL"][1]["clean_m"]),
    "b5": ("Bootes I", _p["stot"]["est"], _p["stot"]["hi"] - _p["stot"]["est"], _p["stot"]["est"] - _p["stot"]["lo"]),
    "b6": ("Bootes I", _p["sc"]["est"], _p["sc"]["hi"] - _p["sc"]["est"], _p["sc"]["est"] - _p["sc"]["lo"]),
    "b7": ("Tucana II", C66["Q2_gradient"]["sigma_grad"], C66["Q2_gradient"]["sigma_grad_ep"], C66["Q2_gradient"]["sigma_grad_em"]),
}


def spred_B(foot, reading):
    rule = reading == "S"

    def sig(g, ups=None, floor_mh=None):
        if floor_mh is not None and rule:      # S with a collapse-mass floor: CFG42's mh_all mechanism on the estimator FG001 / CFG51 use (edge phantom + NFW debris), copied
            a0 = g51["A0H"][foot]; ups_ = UPS_V if ups is None else ups
            Ms = ups_ * g["LV"]; Mb = Ms + 1.33 * g["MHI"]; rh_pc = (4.0 / 3.0) * g["rh"]; rh = rh_pc * 3.0857e16
            gg = g51["a_int"](G_SAT * 0.5 * Mb * MSUN_SAT / rh ** 2, 0.0, a0)
            Mh = floor_mh
            fex = max(0.0, 1.0 - g45["edge_phantom36"](Mb, foot, 0.40) / ((1 - FB) * Mh))
            gg += G_SAT * fex * (1 - FB) * float(g45["nfw_enclosed"](Mh, rh_pc / 1000.0)) * MSUN_SAT / rh ** 2
            return math.sqrt(gg * rh / 3.0) / 1e3
        return g51["spred"](g, foot, ups=ups, rule=rule)
    return sig


# ================================================================================================ SLUGGS estimators (CFG38 / CFG55 machinery)
RES50, sigma_r2, sigma_los, GAMMA = g55["RES50"], g55["sigma_r2"], g55["sigma_los"], g55["GAMMA"]
G50, KPC50, MSUN50 = g55["G_"], g55["KPC"], g55["MSUN"]
G16 = g55["G16"]


def sl_off_lcdm(r, Ms, cfg):
    a_h = r["Re"] / 1.8153; Mh = cfg["halo"](Ms) * cfg["hmf"]; prof = cfg["prof"]
    g = lambda rr: G50 * (Ms * MSUN50 * rr ** 2 / (rr + a_h) ** 2 + (1 - FB) * np.asarray(prof(Mh, rr), float) * MSUN50) / (rr * KPC50) ** 2
    s = sigma_los(r["Rb"], sigma_r2(g, GAMMA), GAMMA)
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s[r["out"]])))


def stat_arr(off):
    off = np.asarray(off, float)
    return dict(mean=float(off.mean()), err=float(off.std(ddof=1) / math.sqrt(len(off))), z=float(off.mean() / (off.std(ddof=1) / math.sqrt(len(off)))), n=len(off), per=off.tolist())


def jam_mass_lcdm(g, cfg):
    prof, hmf, halo = cfg["prof"], cfg["hmf"], cfg["halo"]

    def fr(lm):
        Ms = 10 ** lm
        return math.log10(0.5 * Ms + (1 - FB) * float(prof(halo(Ms) * hmf, g["r12"]))) - math.log10(g["Mjam"] / 2)
    if fr(8.0) * fr(13.5) > 0:
        return float("nan")
    return 10 ** brentq(fr, 8.0, 13.5, xtol=1e-12)


# ================================================================================================ C3 profile controls (before any population number is read)
R.banner("C3  CONTROLS: the NFW profile function")
Mg = np.logspace(7.5, 13.5, 30); rg = np.concatenate([[1e-9, 1e-6], np.logspace(-2.5, 2.7, 38)])
dev_dm = max(float(np.max(np.abs(np.asarray(make_nfw(c_dm)(M_, rg)) / np.asarray(g45["nfw_enclosed"](M_, rg)) - 1.0))) for M_ in Mg)


def quad_nfw(c, X):
    I = lambda T: integrate.quad(lambda t: t * t / (t * (1 + t) ** 2), 0.0, T, epsabs=0.0, epsrel=1e-12, limit=400)[0]
    return I(X) / I(c)


dev_q, dev_n, mono = 0.0, 0.0, True
for cf_ in (c_duffy_full, c_duffy_relaxed):
    f_ = make_nfw(cf_)
    for Mh in (3e9, 2e11):
        c = float(cf_(Mh)); R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
        for r in (0.05, 0.3, 1.5, 8.0, 40.0):
            dev_q = max(dev_q, abs(float(f_(Mh, r)) / (Mh * quad_nfw(c, c * min(max(r / R200, 1e-4), 5.0))) - 1.0))
        rr = np.logspace(-1.5, math.log10(5 * R200), 200); mm = np.asarray(f_(Mh, rr)); mono = mono and bool(np.all(np.diff(mm) > 0))
        dev_n = max(dev_n, abs(float(f_(Mh, R200)) / Mh - 1.0))
check("C3 CONTROL: the generic NFW (Duffy full / relaxed c) equals the analytic enclosed mass (numerical integration of the density) to 1e-7, M(<R200) = M_h to 1e-12, monotone; with the "
      "Dutton-Maccio c it equals h48's committed nfw_enclosed to 1e-9 (30 masses x 40 radii)",
      f"max |analytic difference| {dev_q:.1e}; max |M(<R200)/M_h - 1| {dev_n:.1e}; monotone {mono}; max |DM-c vs h48| {dev_dm:.1e}",
      dev_q <= 1e-7 and dev_n <= 1e-12 and mono and dev_dm <= 1e-9)

# ================================================================================================ the populations: L, S (committed machinery) and LCDM
ROWS = {}    # key -> dict(label, L={foot: (off,z)}, S={foot: (off,z)}, LCDM=(off,z), extra)
ORDER = []


def add_row(key, label, L, S, N=None):
    ROWS[key] = dict(label=label, L=L, S=S); ORDER.append(key)


R.banner("THE LCDM ENGINE: the base configuration through every population")
BASE = CFGS["base"]
LC = {}   # LC[cfgname][rowkey] = dict(off, z, ...)


def run_config(name):
    cfg = CFGS[name]; sig = sat_sigma_lcdm(cfg); out = {}
    if name != "V5":       # the satellites use the Moster relation; V5 (Mandelbaum) is a SLUGGS-only variant
        out["b1"] = ufd_generic(sig, True)
        for key, rk in (("cls", "c1"), ("col", "c2"), ("m31", "c3")):
            out[rk] = cl_generic(sig, key, True)
        out["c4"] = fld_generic(sig, True)
        for k46, rk in (("sig_f", "b2"), ("sig_fz", "b2z"), ("sig_f7", "b2h")):
            out[rk] = c46_generic(sig, k46, "lcdm")
        for rk, (gn, s, p_, m_) in DISP_TWO.items():
            out[rk] = err_two(GAL51[gn], s, p_, m_, sig, "lcdm")
    if True:
        Ms19 = [r["Mstar"] for r in RES50]
        out["a2"] = stat_arr([sl_off_lcdm(r, m, cfg) for r, m in zip(RES50, Ms19)])
        out["a3"] = stat_arr([sl_off_lcdm(g["r"], g["r"]["Mstar"], cfg) for g in G16])
        ml = [jam_mass_lcdm(g, cfg) for g in G16]
        keep = [(g, m) for g, m in zip(G16, ml) if np.isfinite(m)]
        a1 = stat_arr([sl_off_lcdm(g["r"], m, cfg) for g, m in keep]); a1["n_excluded"] = len(G16) - len(keep)
        a1["excluded"] = [g["name"] for g, m in zip(G16, ml) if not np.isfinite(m)]; a1["logM"] = [math.log10(m) if np.isfinite(m) else None for m in ml]
        out["a1"] = a1
    return out


for name in ("base", "V1", "V2", "V3", "V4", "V5"):
    LC[name] = run_config(name)
    P(f"    config {name:5s} done ({time.time() - T0:.0f} s): {CFGS[name]['label']}")

# ---- L and S from the lanes' own machinery
UF45, CL45 = g45["UF"], g45["CL"]
add_row("a1", "SLUGGS JAM-calibrated (CFG55; 16 of 19)",
        {f: (g55["RES"][f]["law"][1], g55["RES"][f]["law"][1] / g55["RES"][f]["law"][2]) for f in FOOTS},
        {f: (g55["RES"][f]["rule"][1], g55["RES"][f]["rule"][1] / g55["RES"][f]["rule"][2]) for f in FOOTS})
_o38 = {f: g55["offsets38"](f)[0] for f in FOOTS}
_l38 = {f: np.array([r["off_mond_" + f] for r in RES50]) for f in FOOTS}
z_ = lambda a: float(a.mean() / (a.std(ddof=1) / math.sqrt(len(a))))
add_row("a2", "SLUGGS own masses, 19 (CFG38)", {f: (float(_l38[f].mean()), z_(_l38[f])) for f in FOOTS}, {f: (float(_o38[f].mean()), z_(_o38[f])) for f in FOOTS})
add_row("a3", "SLUGGS own masses, same 16 (CFG55 R1)",
        {f: (g55["RES"][f]["law_sl"][1], g55["RES"][f]["law_sl"][1] / g55["RES"][f]["law_sl"][2]) for f in FOOTS},
        {f: (g55["RES"][f]["rule_sl"][1], g55["RES"][f]["rule_sl"][1] / g55["RES"][f]["rule_sl"][2]) for f in FOOTS})
add_row("b1", "MW ultra-faints, 31 + 9 limits, KM median (CFG42)", {f: (UF45[(f, "L")]["km"], UF45[(f, "L")]["z"]) for f in FOOTS}, {f: (UF45[(f, "S")]["km"], UF45[(f, "S")]["z"]) for f in FOOTS})
c46 = {(f, k, rd): g46["stat"](k, f, rule=(rd == "S")) for f in FOOTS for k in ("sig_f", "sig_fz", "sig_f7") for rd in ("L", "S")}
for rk, k, lab in (("b2", "sig_f", "CFG46 eight, f free (headline)"), ("b2z", "sig_fz", "CFG46 eight, f = 0"), ("b2h", "sig_f7", "CFG46 eight, f = 0.7")):
    add_row(rk, lab, {f: (c46[(f, k, "L")]["med"], c46[(f, k, "L")]["z"]) for f in FOOTS}, {f: (c46[(f, k, "S")]["med"], c46[(f, k, "S")]["z"]) for f in FOOTS})
TWO = {}
for rk, (gn, s, p_, m_) in DISP_TWO.items():
    g = GAL51[gn]
    for f in FOOTS:
        TWO[(rk, f, "L")] = err_two(g, s, p_, m_, (lambda gg, ups=None, floor_mh=None, f=f: g51["spred"](gg, f, ups=ups)), "L", foot=f)
        TWO[(rk, f, "S")] = err_two(g, s, p_, m_, spred_B(f, "S"), "S", foot=f)
    add_row(rk, {"b3": "Bootes I cleaned (CFG51)", "b4": "Tucana II cleaned (CFG51)", "b5": "Bootes I total mixture (CFG66)", "b6": "Bootes I cold-only (CFG66)",
                 "b7": "Tucana II gradient-removed (CFG66)"}[rk],
            {f: (TWO[(rk, f, "L")]["off"], TWO[(rk, f, "L")]["z"]) for f in FOOTS}, {f: (TWO[(rk, f, "S")]["off"], TWO[(rk, f, "S")]["z"]) for f in FOOTS})
for key, rk in (("cls", "c1"), ("col", "c2"), ("m31", "c3")):
    add_row(rk, {"c1": "MW classical dSph (CFG42)", "c2": "M31 Collins+13 (CFG42)", "c3": "M31 LVD (CFG42)"}[rk],
            {f: (CL45[(key, f, "L")]["med"], CL45[(key, f, "L")]["z"]) for f in FOOTS}, {f: (CL45[(key, f, "S")]["med"], CL45[(key, f, "S")]["z"]) for f in FOOTS})
# c4 (CFG58 d2): the generic code with L and S sigma callables (CFG45's sigma_read)
D2 = {(f, rd): fld_generic(sat_sigma_B(f, rd), rd == "S") for f in FOOTS for rd in ("L", "S")}
add_row("c4", "LV field dwarfs, n = 13 (CFG58 d2)", {f: (D2[(f, "L")]["med"], D2[(f, "L")]["z"]) for f in FOOTS}, {f: (D2[(f, "S")]["med"], D2[(f, "S")]["z"]) for f in FOOTS})
# reorder for the table
ORDER = ["a1", "a2", "a3", "b1", "b2", "b2z", "b2h", "b3", "b4", "b5", "b6", "b7", "c1", "c2", "c3", "c4"]
for k in ORDER:
    v = LC["base"][k]
    ROWS[k]["LCDM"] = (v["mean"], v["z"]) if "mean" in v else ((v["km"], v["z"]) if "km" in v else ((v["med"], v["z"]) if "med" in v else (v["off"], v["z"])))

# ================================================================================================ CONTROLS (ii) and (i)
R.banner("C1 / C2  CONTROLS: L and S reproduce the lanes; the LCDM engine reproduces CFG38's post-hoc LCDM")
if not MUTATE:
    devs = []
    c42, c55, c38, c58, c46j, c51j = J("CFG42_satellites_rule_results.json"), J("CFG55_sluggs_dynamical_masses_results.json"), J("CFG38_sluggs_massive_passive_results.json"), \
        J("CFG58_rule_more_populations_results.json"), J("CFG46_ufd_binary_corrected_results.json"), J("CFG51_walker_ufd_results.json")
    for f in FOOTS:
        for rd, tag in (("L", "law"), ("S", "rule")):
            # CFG42 via CFG45's exec'd machinery (b1, c1-c3) AND through this script's generic estimator code
            gen_u = ufd_generic(sat_sigma_B(f, rd), rd == "S")
            devs += [(f"CFG42 UF {f} {tag} km (lane)", abs(UF45[(f, rd)]["km"] - c42["UF"][f"{f}|{tag}"]["km"])), (f"CFG42 UF {f} {tag} tot (lane)", abs(UF45[(f, rd)]["tot"] - c42["UF"][f"{f}|{tag}"]["tot"])),
                     (f"CFG42 UF {f} {tag} km (generic)", abs(gen_u["km"] - c42["UF"][f"{f}|{tag}"]["km"])), (f"CFG42 UF {f} {tag} tot (generic)", abs(gen_u["tot"] - c42["UF"][f"{f}|{tag}"]["tot"]))]
            for key in ("cls", "col", "m31"):
                gen_c = cl_generic(sat_sigma_B(f, rd), key, rd == "S")
                devs += [(f"CFG42 CL {key} {f} {tag} med (lane)", abs(CL45[(key, f, rd)]["med"] - c42["CL"][f"{key}|{f}|{tag}"]["med"])),
                         (f"CFG42 CL {key} {f} {tag} tot (lane)", abs(CL45[(key, f, rd)]["tot"] - c42["CL"][f"{key}|{f}|{tag}"]["tot"])),
                         (f"CFG42 CL {key} {f} {tag} med (generic)", abs(gen_c["med"] - c42["CL"][f"{key}|{f}|{tag}"]["med"])),
                         (f"CFG42 CL {key} {f} {tag} tot (generic)", abs(gen_c["tot"] - c42["CL"][f"{key}|{f}|{tag}"]["tot"]))]
            # CFG58 d2
            devs += [(f"CFG58 d2 {f} {rd} med", abs(D2[(f, rd)]["med"] - c58["field_dwarfs"][f"{f}|{rd}"]["med"])), (f"CFG58 d2 {f} {rd} tot", abs(D2[(f, rd)]["tot"] - c58["field_dwarfs"][f"{f}|{rd}"]["tot"]))]
            # CFG55 JAM and CFG38
            devs += [(f"CFG55 JAM {f} {tag} mean", abs(g55["RES"][f][tag][1] - c55["RES"][f][tag]["mean"])), (f"CFG55 JAM {f} {tag} err", abs(g55["RES"][f][tag][2] - c55["RES"][f][tag]["err"]))]
        devs.append((f"CFG38 SLUGGS {f} law mean", abs(_l38[f].mean() - c38["RES"][f]["law_mean"]))); devs.append((f"CFG38 SLUGGS {f} rule mean", abs(_o38[f].mean() - c38["RES"][f]["rule_mean"])))
        # CFG46 (law, rule) numbers via CFG46's own stat()
        for k in ("sig_fz", "sig_f", "sig_f7"):
            devs += [(f"CFG46 {f} {k} law med", abs(c46[(f, k, "L")]["med"] - c46j["RES"][f"{f}|{k}|law"]["med"])), (f"CFG46 {f} {k} law tot", abs(c46[(f, k, "L")]["tot"] - c46j["RES"][f"{f}|{k}|law"]["tot"]))]
        devs += [(f"CFG46 {f} rule med", abs(c46[(f, "sig_f", "S")]["med"] - c46j["RES"][f"{f}|sig_f|rule"]["med"])), (f"CFG46 {f} rule tot", abs(c46[(f, "sig_f", "S")]["tot"] - c46j["RES"][f"{f}|sig_f|rule"]["tot"]))]
        # CFG51 L (cleaned) and S offsets
        for rk, nm in (("b3", "Bootes I"), ("b4", "Tucana II")):
            k51 = c51j["RES"][f"{nm}|{f}|clean"]
            devs += [(f"CFG51 {nm} {f} clean off", abs(TWO[(rk, f, "L")]["off"] - k51["off"])), (f"CFG51 {nm} {f} clean tot", abs(TWO[(rk, f, "L")]["tot"] - k51["tot"])),
                     (f"CFG51 {nm} {f} rule off", abs(TWO[(rk, f, "S")]["off"] - c51j["RES"][f"{nm}|{f}|rule"]["off"]))]
        # CFG66 L numbers
        devs += [("CFG66 Bootes total off " + f, abs(TWO[("b5", f, "L")]["off"] - C66["Q1_offsets"][f]["total"]["off"])), ("CFG66 Bootes total tot " + f, abs(TWO[("b5", f, "L")]["tot"] - C66["Q1_offsets"][f]["total"]["tot"])),
                 ("CFG66 Bootes cold off " + f, abs(TWO[("b6", f, "L")]["off"] - C66["Q1_offsets"][f]["cold"]["off"])), ("CFG66 Bootes cold tot " + f, abs(TWO[("b6", f, "L")]["tot"] - C66["Q1_offsets"][f]["cold"]["tot"])),
                 ("CFG66 Tucana grad off " + f, abs(TWO[("b7", f, "L")]["off"] - C66["Q2_offsets"][f]["grad"]["off"])), ("CFG66 Tucana grad tot " + f, abs(TWO[("b7", f, "L")]["tot"] - C66["Q2_offsets"][f]["grad"]["tot"]))]
    worst = max(devs, key=lambda t: t[1])
    check("C2 CONTROL (ii): L and S reproduce the committed lane numbers to 1e-6 (CFG42 UF/CL via the lane machinery AND via the generic estimator used for LCDM; CFG46; CFG51; CFG66's L; CFG58 d2; "
          "CFG55; CFG38), both footings",
          f"{len(devs)} comparisons; worst {worst[0]}: {worst[1]:.2e}; over tolerance: " + (", ".join(f"{a} {b:.1e}" for a, b in devs if b > 1e-6) or "none"), worst[1] <= 1e-6)
    # control (i): CFG38's post-hoc LCDM
    cfg38 = CFGS["V5"]
    own = [sl_off_lcdm(r, r["Mstar"], cfg38) for r in RES50]
    dmax = float(np.max(np.abs(np.array(own) - np.array(c38["R2_lcdm_red"])))); st = stat_arr(own)
    check("C1 CONTROL (i): LCDM through CFG38's SLUGGS machinery with SLUGGS's own stellar masses (Mandelbaum red collapse + Dutton-Maccio) reproduces CFG38's committed post-hoc LCDM offsets "
          "per galaxy to 1e-9 and its printed -0.037 +- 0.017 (-2.1 sigma)",
          f"max per-galaxy |d| {dmax:.1e}; mean {st['mean']:+.4f} +- {st['err']:.4f} ({st['z']:+.2f} sigma)",
          dmax <= 1e-9 and round(st["mean"], 3) == -0.037 and round(st["err"], 3) == 0.017 and round(st["z"], 1) == -2.1)
else:
    check("C1/C2 CONTROLS: skipped in the MUTATE run (the committed numbers are for the un-mutated halos)", "-", True, load_bearing=False)

# C4: the engine's zero-halo limit
d0 = SAMPLES["cls"][0]; sg = sat_sigma_lcdm(BASE)
# closed form: sigma^2 = g r / 3 = G (0.5 Mb) Msun / (rh) / 3 with rh = (4/3) r_half in m
zero_dev = max(abs(sg(d, gas=False, mh_zero=True) / (math.sqrt(G_SAT * 0.5 * (UPS_V * d["LV"] + 1.33 * d["MHI"]) * MSUN_SAT / ((4.0 / 3.0) * d["rh"] * 3.0857e16) / 3.0) / 1e3) - 1.0)
               for d in SAMPLES["ufd"] + SAMPLES["cls"] + SAMPLES["m31"])
gain = min(sg(d) / sg(d, mh_zero=True) for d in SAMPLES["ufd"] + SAMPLES["cls"])
check("C4 CONTROL: the LCDM engine with M_h -> 0 is the closed-form Newtonian prediction (1e-9), the halo only adds mass (sigma ratio >= 1), and LCDM carries no footing dependence (no a_0 enters)",
      f"max |zero-halo / closed form - 1| {zero_dev:.1e}; minimum sigma(LCDM)/sigma(Newton) {gain:.4f}", zero_dev <= 1e-9 and gain >= 1.0)

# C6: the LCDM JAM calibration
res_c6, res_c7 = 0.0, 0.0
for g in G16:
    m = jam_mass_lcdm(g, BASE)
    if np.isfinite(m):
        Mh = BASE["halo"](m) * BASE["hmf"]
        res_c6 = max(res_c6, abs((0.5 * m + (1 - FB) * float(BASE["prof"](Mh, g["r12"]))) / (g["Mjam"] / 2) - 1.0))
    zero = dict(BASE, prof=lambda Mh, r: 0.0 * np.asarray(r, float))
    res_c7 = max(res_c7, abs(jam_mass_lcdm(g, zero) / g["Mjam"] - 1.0))
check("C6 CONTROL: the LCDM JAM calibration -- total mass inside r_1/2 equals M_JAM / 2 at every calibrated galaxy (1e-9), and with the halo switched off the solved M_* returns M_JAM (1e-9)",
      f"max residual {res_c6:.1e}; halo-off max |M_*/M_JAM - 1| {res_c7:.1e}", res_c6 <= 1e-9 and res_c7 <= 1e-9)

# ================================================================================================ classification
def status(z):
    return "FAIL" if abs(z) > 2 else ("MARGINAL" if abs(z) > 1 else "OK")


def classify(zb, zl):
    st = status(zb)
    if st == "OK":
        return "B-ok"
    if abs(zl) <= 2:
        return "SPECIFIC-TO-B"
    return "SHARED" if (zb > 0) == (zl > 0) else "LCDM-WORSE"


CLS = {}
for k in ORDER:
    row = ROWS[k]; zl = row["LCDM"][1]
    for rd in ("L", "S"):
        cl = {f: classify(row[rd][f][1], zl) for f in FOOTS}
        CLS[(k, rd)] = cl["canonical"] if cl["canonical"] == cl["alt"] else f"MIXED({cl['canonical']}|{cl['alt']})"

R.banner("THE TABLE: offset [dex] (z) -- canonical | alt for B; LCDM identical on both footings")
P(f"    {'population':44s}| {'L (bare law) can | alt':30s}| {'S (sum rule) can | alt':30s}| {'LCDM':14s}| {'L-LCDM':>7s} {'S-LCDM':>7s} | class(L) / class(S)")
fm = lambda d: f"{d['canonical'][0]:+.3f}({d['canonical'][1]:+.1f}) | {d['alt'][0]:+.3f}({d['alt'][1]:+.1f})"
for k in ORDER:
    row = ROWS[k]
    P(f"    {(k + ' ' + row['label'])[:44]:44s}| {fm(row['L']):30s}| {fm(row['S']):30s}| {row['LCDM'][0]:+.3f}({row['LCDM'][1]:+.1f}){'':3s}| "
      f"{row['L']['canonical'][0] - row['LCDM'][0]:+7.3f} {row['S']['canonical'][0] - row['LCDM'][0]:+7.3f} | {CLS[(k, 'L')]} / {CLS[(k, 'S')]}")
P("    (B minus LCDM columns: canonical-footing offset difference in dex, reported only.  B-ok = |z| <= 1 on both footings: no classification.)")

R.banner("LCDM detail per row (base configuration)")
for k in ORDER:
    v = LC["base"][k]
    if k in ("b1",):
        P(f"    {k}: KM median {v['km']:+.3f} +- {v['tot']:.3f} (bootstrap {v['err']:.3f}, Upsilon {v['f_ups']:.3f}, collapse floor {v['f_mh']:.3f}); resolved-only median {v['resolved_median']:+.3f}; "
          f"KM median at M_h(M_* < 1e5) = " + ", ".join(f"{fm_:.0e}: {m:+.3f}" for fm_, m in zip(FLOORS, v["floors"])))
    elif k in ("b2", "b2z", "b2h"):
        P(f"    {k}: median {v['med']:+.3f} +- {v['tot']:.3f} (bootstrap {v['boot']:.3f}, measurement {v['meas']:.3f}, Upsilon floor {v['floor']:.3f}, collapse floor {v['cfloor']:.3f}) -> {v['z']:+.2f} sigma; "
          f"without the collapse floor +- {v['tot_nocf']:.3f} -> {v['z_nocf']:+.2f} sigma")
    elif k in ("b3", "b4", "b5", "b6", "b7"):
        P(f"    {k}: offset {v['off']:+.3f} +- {v['tot']:.3f} (e_stat {v['e']:.3f}, Upsilon floor {v['fl']:.3f}, collapse floor {v['cf']:.3f}) -> {v['z']:+.2f} sigma")
    elif k in ("c1", "c2", "c3", "c4"):
        P(f"    {k}: median {v['med']:+.3f} +- {v['tot']:.3f} -> {v['z']:+.2f} sigma; median at the floor variants 1e8..1e10: " + ", ".join(f"{m:+.3f}" for m in v["floors"]))
    else:
        P(f"    {k}: mean {v['mean']:+.4f} +- {v['err']:.4f} ({v['z']:+.2f} sigma), n = {v['n']}" + (f"; EXCLUDED (NFW alone above M_JAM/2): {v['excluded']}" if v.get("excluded") else ""))
        if k == "a1":
            P("        JAM-calibrated log M_* (LCDM): " + ", ".join(f"{g['name'][3:]} {('%.2f' % lm) if lm else 'n/a'}" for g, lm in zip(G16, v["logM"])))

R.banner("SENSITIVITY (reported only; never enters a classification): LCDM offset [dex] (z)")
names = [n for n in ("base", "V1", "V2", "V3", "V4", "V5")]
P(f"    {'row':46s}" + "".join(f"{n:>17s}" for n in names))
for k in ORDER:
    cells = []
    for n in names:
        v = LC[n].get(k)
        if v is None:
            cells.append("-")
            continue
        o = v["mean"] if "mean" in v else (v["km"] if "km" in v else (v["med"] if "med" in v else v["off"]))
        cells.append(f"{o:+.3f}({v['z']:+.1f})")
    P(f"    {k + ' ' + ROWS[k]['label']:46.46s}" + "".join(f"{c:>17s}" for c in cells))
P("    " + "; ".join(f"{n}: {CFGS[n]['label']}" for n in names))

# ================================================================================================ gates
R.banner("GATES")
zu = LC["base"]["b1"]["z"]; h1 = abs(zu) < 2
check("H1 [HEADLINE; MUTATE must fail] the LCDM ultra-faint gate is live: the KM median (31 + 9 limits, CFG42's error model incl. the collapse-mass floor) within 2 sigma of zero on both footings"
      + ("  [MUTATE: every LCDM halo mass x 100]" if MUTATE else ""),
      f"LCDM KM median {LC['base']['b1']['km']:+.3f} +- {LC['base']['b1']['tot']:.3f} -> {zu:+.2f} sigma (identical on both footings); B: L {ROWS['b1']['L']['canonical'][1]:+.2f}|{ROWS['b1']['L']['alt'][1]:+.2f}, "
      f"S {ROWS['b1']['S']['canonical'][1]:+.2f}|{ROWS['b1']['S']['alt'][1]:+.2f} sigma", h1)
prev = None
try:
    prev = json.load(open(os.path.join(OUT, "CFG69_lcdm_comparator_results.json")))["numbers"]["gate_H1_unmutated"]
except Exception:
    pass
if MUTATE:
    check("C5 CONTROL (MUTATE): with every LCDM halo mass x 100 the LCDM ultra-faint gate FAILS", f"|z| = {abs(zu):.2f} (KM median {LC['base']['b1']['km']:+.3f}); the un-mutated run's gate: "
          + ("pass" if prev is True else ("FAIL" if prev is False else "unknown (no un-mutated json found)")), not h1)
else:
    check("C5 CONTROL: (MUTATE-run only; recorded here) the un-mutated LCDM ultra-faint gate", f"passes: {h1}", True, load_bearing=False)
ladder = {}
for m_ in (0.01, 0.1, 1.0, 10.0, 100.0, 1e3, 1e4, 1e5):
    u = ufd_generic(sat_sigma_lcdm(dict(BASE, hmf=m_)), True); ladder[m_] = dict(km=u["km"], tot=u["tot"], z=u["z"])
check("R3 (reported; ADDED after the first MUTATE run, disclosed) the LCDM ultra-faint gate against a multiple of every halo mass (independent of the MUTATE switch)",
      "; ".join(f"x{m_:g}: {v['km']:+.3f} ({v['z']:+.2f} sigma)" for m_, v in ladder.items()) + "; gate fails (|z| > 2) at: "
      + (", ".join(f"x{m_:g}" for m_, v in ladder.items() if abs(v["z"]) >= 2) or "none"), True, load_bearing=False)
R.num("R3_halo_multiple_ladder", {str(k): v for k, v in ladder.items()})
R.num("gate_H1_unmutated", bool(h1) if not MUTATE else prev)
R.num("HMUT", HMUT)
tab = {}
for k in ORDER:
    tab[k] = dict(label=ROWS[k]["label"], L={f: dict(off=ROWS[k]["L"][f][0], z=ROWS[k]["L"][f][1]) for f in FOOTS}, S={f: dict(off=ROWS[k]["S"][f][0], z=ROWS[k]["S"][f][1]) for f in FOOTS},
                  LCDM=dict(off=ROWS[k]["LCDM"][0], z=ROWS[k]["LCDM"][1]), class_L=CLS[(k, "L")], class_S=CLS[(k, "S")])
for k in ORDER:
    tab[k]["L_minus_LCDM_canonical"] = ROWS[k]["L"]["canonical"][0] - ROWS[k]["LCDM"][0]; tab[k]["S_minus_LCDM_canonical"] = ROWS[k]["S"]["canonical"][0] - ROWS[k]["LCDM"][0]
R.num("TABLE", tab)
R.num("SLUGGS_LCDM_per_galaxy", {n: {k: LC[n][k]["per"] for k in ("a1", "a2", "a3") if k in LC[n]} for n in LC})
R.num("SLUGGS_JAM_names", [g["name"] for g in G16])
R.num("LCDM_detail", {n: {k: {a: b for a, b in v.items() if a != "per"} for k, v in LC[n].items()} for n in LC})
R.num("CFGS", {n: v["label"] for n, v in CFGS.items()})
counts = {}
for k in ORDER:
    for rd in ("L", "S"):
        counts[CLS[(k, rd)]] = counts.get(CLS[(k, rd)], 0) + 1
check("H2 (reported) the classification table (counts over the 16 rows x {L, S})", "; ".join(f"{a}: {b}" for a, b in sorted(counts.items())), True, load_bearing=False)
nf = R.write(here=OUT)
sys.exit(1 if nf else 0)
