#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG78 -- INDEPENDENT RE-DERIVATION of CFG46's binary-corrected ultra-faint offsets.   (FROZEN BEFORE THE FIRST RUN)

QUESTION.  Does an independent implementation, written from the CFG46/CFG42/CFG35 README model statements and the data files only (no exec/import of
CFG46/CFG42/CFG36/FG001 code), reproduce CFG46's headline numbers: the bare isolated law's median offset log10(sigma_obs/sigma_law) over the 8 scorable
ultra-faints using Arroyo-Polonio+2026 dispersions: f = 0 +0.295 +- 0.163 (+1.81 sigma), f free +0.206 (+1.26), f = 0.7 +0.171 (+0.99), and the sum rule
(f free) -0.151 (-1.17 sigma)?  Alt footing: +0.275, +0.186, +0.150.

DATA.  real_research/data/arroyopolonio2026_ufd_binary_corrected.tsv (sig_fz, sig_f, sig_f7 posterior medians; _p1/_m1 = 1-sigma errors; _p3/_m3 = 3-sigma);
real_research/data/dsph/lvd_dwarf_mw.csv (M_V, rhalf_sph_physical [pc; falls back to rhalf_physical], mass_HI).  Scored = the 9 tsv names that map to the LVD
table, minus Crater II (M_V <= -7.7): Boo I, Car II, Hyd I, Leo IV, Leo V, Ret II, Seg 1, Wil 1.  All have empty mass_HI (gas = 0).

MODEL (from the READMEs).  Stars only (+1.33 M_HI, = 0 here): M_b = Upsilon_V L_V, Upsilon_V = 2, L_V = 10^(0.4 (4.83 - M_V)).  Half of the baryons enclosed at
r = (4/3) r_half:  g_N = G (M_b/2)/r^2;  law g = g_N nu(g_N/a0);  sigma^2 = g r / 3.  KERNEL USED: the exponential RAR kernel nu(y) = 1/(1 - exp(-sqrt y))
(CFG64's note: what CFG46 actually ran; agrees with nu_mono to 3e-9 for y <= 0.1; nu_mono itself is NOT reimplemented, so the rule's edge-phantom uses the
RAR kernel too).  FOOTINGS: a0 = 9.36e-11 (canonical) and 1.13e-10 (alt) m/s^2.  Constants G = 6.674e-11, Msun = 1.989e30, pc = 3.0857e16 m.
SUM RULE (CFG35/CFG42 statement): g += G f_ex (1-f_b) M_NFW(<r)/r^2, f_ex = max(0, 1 - M_ph,edge/[(1-f_b) M_coll]); f_b = 0.02237/(0.02237+0.1200);
M_coll = Moster+13 (z=0: N=0.0351, logM1=11.590, beta=1.376, gamma=0.608) inverted at M_* = Upsilon_V L_V on a grid log M_h = 9.0..15.5 (so it CLAMPS at 1e9,
as CFG42 declares); NFW with Dutton-Maccio c = 10^(0.905 - 0.101 (log10(0.674 M_h) - 12)), R200 from rho_crit (H0 = 67.4), 200 rho_crit; M_ph,edge = M_law(x_e r_ta)
- M_b with x_e = 0.40, r_ta = radius where the law's untruncated mean enclosed density = (1 + delta_ta) rho_m(a=1), 1 + delta_ta from MY OWN LCDM spherical
top-hat solve (Om = 0.3153, h = 0.6736, turnaround at a = 1, age from the analytic LCDM formula, radiation neglected).
STATISTIC.  Median over the scored systems of log10(sigma_obs/sigma_law).  ERROR (CFG46's stated recipe, my code, my seeds): sqrt(bootstrap^2 + measurement^2
+ floor^2): bootstrap = std of 2000 resampled medians; measurement = std of 2000 medians with each dispersion drawn from a split normal (p1/m1 1-sigma errors,
floored at 0.05 km/s); floor = half the range of the median over {Upsilon_V = 1, 2, 4, and the pure deep-MOND estimator sigma^4 = (4/81) G M_b a0}.
Z = median / total.

PASS LINES (frozen).
 REPRODUCE (per number; canonical and alt): |my median - CFG46's| <= 0.010 dex AND my total error within 10% of CFG46's AND |my z - CFG46's z| <= 0.15.
   CFG46 targets (canonical): f=0 +0.295/0.163/+1.81; f free +0.206/0.164/+1.26; f=0.7 +0.171/0.172/+0.99; rule f free -0.151/0.129/-1.17.
   Alt (medians only): +0.275, +0.186, +0.150.  If any target fails it is reported as NOT REPRODUCED with the cause; nothing is retuned.
 H1' (CFG46's H1 on my numbers): f-free law z > 2 on both footings.  Expected (from CFG46) FAIL.   H2': f=0.7 z > 1 both footings.   H3': rule f free |z| < 2.
 C1 Newtonian/deep-MOND closed forms: a0 -> 1e-40: sigma^2 = G M_b/(6 r) to 1e-9 relative; a0 -> 1e+40 (deep): sigma^4 = G M_b a0/18 to 1e-4 relative.
 C2 median and bootstrap: my median == hand-sorted median on 1000 random arrays (n = 7, 8) exactly; MC bootstrap std (2000) vs EXACT enumeration of all 8^8 index
   resamples: within 10% (the exact std is the brute-force alternative); a 2e6-draw MC agrees with the exact std within 1%.
 C3 LEAVE-ONE-OUT: drop each system, recompute median (and z with the same recipe) for f = 0, f free, f = 0.7 (canonical).  A system DRIVES the result if its removal
   moves the f-free median by more than 0.05 dex (about a third of the total error) or changes the sign of a >1 sigma verdict; reported, no pass/fail.
 C4 WEIGHTS (reported, no pass/fail; my reading of 'reported heteroscedastic weights': the paper's per-system 1-sigma measurement errors, converted to dex): the
   unweighted median vs the inverse-variance weighted median with w = 1/s_i^2 (s_i = symmetrised dex error), with w = 1/(s_i^2 + floor_i^2 [0.076 dex... my floor]),
   and the weighted mean; plus an alternate inflation: split-normal errors replaced by (p3, m3)/3 (the 3-sigma columns scaled) in the measurement term.
 MUTATE=1: every observed dispersion x 0.5.  Must: (i) shift every per-system offset and every median by exactly log10(0.5) (1e-12) at fixed model; (ii) FAIL the
   headline (no reproduction of CFG46's medians; H1' fail; the law offsets become negative).  MUTATE exit code 1 is the intended outcome.
PROGRAMME RULES.  Never says the data favour the framework; kappa = 1/2 is fitted; non-reproduction is a valid outcome.  Nothing tuned after seeing results.
"""
import os, sys, math, csv, json, itertools
import numpy as np

MUTATE = os.environ.get("MUTATE", "0") == "1"
SF = 0.5 if MUTATE else 1.0
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
TSV = f"{REPO}/real_research/data/arroyopolonio2026_ufd_binary_corrected.tsv"
LVDF = f"{REPO}/real_research/data/dsph/lvd_dwarf_mw.csv"
OUT = []
def P(s=""):
    print(s); OUT.append(s)
FAILS = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")
    if not ok: FAILS.append(name)

G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
UPS = 2.0
FOOTS = ("canonical", "alt")
FB = 0.02237 / (0.02237 + 0.1200)
KEYS = (("sig_fz", "f = 0"), ("sig_f", "f free"), ("sig_f7", "f = 0.7"))

# ---------------------------------------------------------------- data
rows = [l.rstrip("\n").split("\t") for l in open(TSV) if l.strip() and not l.startswith("#")]
hdr = rows[0]; TAB = {r[0]: dict(zip(hdr, r)) for r in rows[1:]}
MAP = {"Boo I": "Bootes I", "Car II": "Carina II", "Cra II": "Crater II", "Hyd I": "Hydrus I", "Leo IV": "Leo IV", "Leo V": "Leo V",
       "Ret II": "Reticulum II", "Seg 1": "Segue 1", "Wil 1": "Willman 1"}
LVD = {r["name"]: r for r in csv.DictReader(open(LVDF))}
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None
GAL = []
for k, lv in MAP.items():
    r = LVD[lv]; t = TAB[k]
    MV = fl(r["M_V"]); rh = fl(r["rhalf_sph_physical"]) or fl(r["rhalf_physical"]); mhi = fl(r["mass_HI"])
    d = dict(name=k, MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=(10 ** mhi if mhi is not None else 0.0))
    for kk in ("sig_fz", "sig_f", "sig_f7"):
        d[kk] = float(t[kk]); d[kk + "_p1"] = float(t[kk + "_p1"]); d[kk + "_m1"] = float(t[kk + "_m1"])
        d[kk + "_p3"] = float(t[kk + "_p3"]); d[kk + "_m3"] = float(t[kk + "_m3"])
    GAL.append(d)
SCORED = [g for g in GAL if g["MV"] > -7.7]
P(f"scored ({len(SCORED)}): " + ", ".join(g["name"] for g in SCORED) + "; excluded by M_V cut: " + ", ".join(g["name"] for g in GAL if g["MV"] <= -7.7))

# ---------------------------------------------------------------- law
def nu(y):
    y = max(float(y), 1e-300)
    return 1.0 / (-math.expm1(-math.sqrt(y)))     # 1/(1 - e^{-sqrt y}), expm1 for accuracy at tiny y
def sig_law_kms(g, a0, ups=UPS, deep_est=False, extra_g=0.0):
    Mb = ups * g["LV"] + 1.33 * g["MHI"]
    if deep_est:
        return (4.0 / 81.0 * G * Mb * MSUN * a0) ** 0.25 / 1e3
    r = (4.0 / 3.0) * g["rh"] * PC
    gN = G * 0.5 * Mb * MSUN / r ** 2
    gg = gN * nu(gN / a0) + extra_g
    return math.sqrt(gg * r / 3.0) / 1e3

# ---------------------------------------------------------------- rule pieces
_LMH = np.linspace(9.0, 15.5, 1301)
def _moster_ms(lmh):
    x = 10 ** (lmh - 11.590)
    return 10 ** lmh * 2 * 0.0351 / (x ** (-1.376) + x ** 0.608)
_LMS = np.log10(_moster_ms(_LMH))
def mcoll(Mstar):
    return float(10 ** np.interp(math.log10(Mstar), _LMS, _LMH))
H0_KMS = 67.4; MPC_M = 3.0857e22
RHO_C = 3 * (H0_KMS * 1e3 / MPC_M) ** 2 / (8 * math.pi * G) / MSUN * MPC_M ** 3   # Msun / Mpc^3
def nfw_enc(Mh, r_kpc):
    c = 10 ** (0.905 - 0.101 * (math.log10(Mh * 0.674) - 12.0))
    R200 = (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.0) * 1000.0
    x = min(max(r_kpc / R200, 1e-4), 5.0)
    m = lambda t: math.log1p(t) - t / (1 + t)
    return Mh * m(c * x) / m(c)

# my own LCDM spherical top-hat at turnaround a = 1 (independent of CFG7_common)
from scipy.optimize import brentq
from scipy.integrate import quad
OM, HH = 0.3153, 0.6736; OL = 1 - OM
GMPC = 4.30091727e-9; H0M = 100 * HH                         # km/s/Mpc
RHOM0 = OM * 3 * H0M ** 2 / (8 * math.pi * GMPC)              # Msun/Mpc^3
AGE = 2.0 / (3.0 * H0M * math.sqrt(OL)) * math.asinh(math.sqrt(OL / OM))   # Mpc/(km/s)
def _tta(rta, M=1.0):
    # time from r=0 to turnaround: v^2 = 2GM(1/r - 1/rta) + (Lam/3)(r^2 - rta^2), Lam/3 = OL H0^2
    L3 = OL * H0M ** 2
    f = lambda r: 1.0 / math.sqrt(max(2 * GMPC * M * (1 / r - 1 / rta) + L3 * (r * r - rta * rta), 1e-300))
    v, _ = quad(f, 0, rta, limit=400)
    return v
def _one_plus_delta():
    M = 1.0e6
    fn = lambda lr: _tta(math.exp(lr), M) - AGE
    lr = brentq(fn, math.log(1e-4), math.log(50.0), xtol=1e-12)
    rta = math.exp(lr)
    return M / (4 * math.pi / 3 * rta ** 3) / RHOM0
DELTA_TA = None
def edge_phantom(Mb, a0, xe=0.40):
    global DELTA_TA
    if DELTA_TA is None:
        DELTA_TA = _one_plus_delta()
    Mlaw = lambda r: Mb * nu(GMPC * Mb / r ** 2 / (a0 * MPC_M / 1e6))
    fn = lambda lr: math.log(Mlaw(math.exp(lr)) / (4 * math.pi / 3 * math.exp(3 * lr) * RHOM0)) - math.log(DELTA_TA)
    rta = math.exp(brentq(fn, math.log(1e-5), math.log(1e3), xtol=1e-13))
    return Mlaw(xe * rta) - Mb
def sig_rule_kms(g, a0):
    Mb = UPS * g["LV"] + 1.33 * g["MHI"]
    Mh = mcoll(UPS * g["LV"])
    fex = max(0.0, 1.0 - edge_phantom(Mb, a0) / ((1 - FB) * Mh))
    rh_pc = (4.0 / 3.0) * g["rh"]; r = rh_pc * PC
    extra = G * fex * (1 - FB) * nfw_enc(Mh, rh_pc / 1000.0) * MSUN / r ** 2
    return sig_law_kms(g, a0, extra_g=extra), fex, Mh

# ---------------------------------------------------------------- statistics
def my_median(v):
    s = sorted(v); n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])
def wmedian(v, w):
    o = np.argsort(v); v = np.asarray(v)[o]; w = np.asarray(w)[o]; c = np.cumsum(w) / w.sum()
    i = int(np.searchsorted(c, 0.5))
    if abs(c[i] - 0.5) < 1e-12 and i + 1 < len(v):
        return 0.5 * (v[i] + v[i + 1])
    return float(v[i])
def split_normal(rng, m, p, mn):
    z = rng.standard_normal()
    return max(m + z * p if z >= 0 else m + z * mn, 0.05)

NB = 2000
def offsets(smp, key, foot, kind="law"):
    a0 = A0[foot]
    if kind == "rule":
        return np.array([math.log10(SF * g[key] / sig_rule_kms(g, a0)[0]) for g in smp])
    return np.array([math.log10(SF * g[key] / sig_law_kms(g, a0)) for g in smp])

def stat(smp, key, foot, kind="law", seed=78, err_cols=("_p1", "_m1"), pred_cache=None):
    a0 = A0[foot]
    if kind == "rule":
        pred = np.array([sig_rule_kms(g, a0)[0] for g in smp])
    else:
        pred = np.array([sig_law_kms(g, a0) for g in smp])
    obs = np.array([SF * g[key] for g in smp]); base = np.log10(obs / pred); m0 = my_median(list(base))
    rng = np.random.default_rng(seed); n = len(smp)
    bs = np.array([my_median(list(base[rng.integers(0, n, n)])) for _ in range(NB)])
    mc = []
    for _ in range(NB):
        v = np.array([split_normal(rng, g[key], g[key + err_cols[0]], g[key + err_cols[1]] / (3.0 if err_cols[0] == "_p3" else 1.0) * (1.0) ) if False else 0.0 for g in smp]) if False else None
        vals = []
        for g in smp:
            p, mn = g[key + err_cols[0]], g[key + err_cols[1]]
            if err_cols[0] == "_p3":
                p, mn = p / 3.0, mn / 3.0
            vals.append(split_normal(rng, g[key], p, mn))
        mc.append(my_median(list(np.log10(SF * np.array(vals) / pred))))
    mc = np.array(mc)
    if kind == "law":
        fl_ = [my_median([math.log10(SF * g[key] / sig_law_kms(g, a0, ups=u)) for g in smp]) for u in (1.0, 2.0, 4.0)]
        fl_.append(my_median([math.log10(SF * g[key] / sig_law_kms(g, a0, deep_est=True)) for g in smp]))
    else:   # CFG46: for the rule the floor list's 4th entry repeats the Upsilon=2 value; Upsilon variants of the rule need the collapse mass moved too -- mirror: law-only Upsilon in g
        fl_ = [my_median([math.log10(SF * g[key] / sig_rule_kms(g, a0)[0]) for g in smp])] * 4
        # CFG46 (README): floor for the rule uses the same ups scan applied to the rule's spred with ups override (halo mass still at UPS_V); mirror that:
        fl_ = []
        for u in (1.0, 2.0, 4.0):
            vv = []
            for g in smp:
                Mb2 = u * g["LV"]; Mh = mcoll(UPS * g["LV"])
                fex = max(0.0, 1.0 - edge_phantom(Mb2, a0) / ((1 - FB) * Mh))
                rhp = (4.0 / 3.0) * g["rh"]; r = rhp * PC
                ex = G * fex * (1 - FB) * nfw_enc(Mh, rhp / 1000.0) * MSUN / r ** 2
                gN = G * 0.5 * Mb2 * MSUN / r ** 2
                s = math.sqrt((gN * nu(gN / a0) + ex) * r / 3.0) / 1e3
                vv.append(math.log10(SF * g[key] / s))
            fl_.append(my_median(vv))
        fl_.append(fl_[1])
    floor = 0.5 * (max(fl_) - min(fl_))
    tot = math.sqrt(bs.std() ** 2 + mc.std() ** 2 + floor ** 2)
    return dict(med=m0, boot=float(bs.std()), meas=float(mc.std()), floor=floor, tot=tot, z=m0 / tot, base=base)

# ================================================================= C1 closed forms
P("\n=== C1  closed forms ===")
g0 = SCORED[0]
for foot in FOOTS:
    Mb = UPS * g0["LV"]; r = (4 / 3) * g0["rh"] * PC
    sN = sig_law_kms(g0, 1e-40); cN = math.sqrt(G * Mb * MSUN / (6 * r)) / 1e3
    sD = sig_law_kms(g0, 1e40); cD = (G * Mb * MSUN * 1e40 / 18.0) ** 0.25 / 1e3
    check(f"C1 Newtonian limit ({foot}, {g0['name']})", abs(sN / cN - 1) < 1e-9, f"code {sN:.6f} closed {cN:.6f} rel {sN / cN - 1:+.1e}")
    check(f"C1 deep-MOND limit ({foot})", abs(sD / cD - 1) < 1e-4, f"code {sD:.6e} closed {cD:.6e} rel {sD / cD - 1:+.1e}")
    break

# ================================================================= per-system table
P("\n=== per-system (canonical) ===")
for g in SCORED:
    a0 = A0["canonical"]; sl = sig_law_kms(g, a0)
    P(f"  {g['name']:7s} M_V {g['MV']:6.2f} rh {g['rh']:7.2f} pc  sigma_law {sl:5.3f}   obs f0 {g['sig_fz']:.2f} ffree {g['sig_f']:.2f} f7 {g['sig_f7']:.2f}   "
      f"offsets {math.log10(SF*g['sig_fz']/sl):+.3f} / {math.log10(SF*g['sig_f']/sl):+.3f} / {math.log10(SF*g['sig_f7']/sl):+.3f}")
if not MUTATE:
    pass
# mutate shift check (exact, model-fixed)
for key, lab in KEYS:
    for foot in FOOTS:
        pred = np.array([sig_law_kms(g, A0[foot]) for g in SCORED]); obs = np.array([g[key] for g in SCORED])
        o1 = np.log10(obs / pred); o5 = np.log10(0.5 * obs / pred)
        assert np.max(np.abs((o5 - o1) - math.log10(0.5))) < 1e-12
        assert abs(my_median(list(o5)) - my_median(list(o1)) - math.log10(0.5)) < 1e-12
check("MUTATE-shift identity: x0.5 shifts every per-system offset and the median by exactly log10(0.5) (<1e-12), all keys/footings", True, "asserted on the model at fixed inputs")

# ================================================================= headline
P("\n=== HEADLINE ===")
RES = {}
for foot in FOOTS:
    for key, lab in KEYS:
        RES[(foot, key, "law")] = stat(SCORED, key, foot)
    RES[(foot, "sig_f", "rule")] = stat(SCORED, "sig_f", foot, kind="rule")
    for key, lab in KEYS:
        v = RES[(foot, key, "law")]
        P(f"  {foot:9s} law  {lab:7s}: {v['med']:+.3f} +- {v['tot']:.3f} (boot {v['boot']:.3f} meas {v['meas']:.3f} floor {v['floor']:.3f}) -> {v['z']:+.2f} sigma")
    v = RES[(foot, "sig_f", "rule")]
    P(f"  {foot:9s} rule f free: {v['med']:+.3f} +- {v['tot']:.3f} (boot {v['boot']:.3f} meas {v['meas']:.3f} floor {v['floor']:.3f}) -> {v['z']:+.2f} sigma")
# rule diagnostics
a0 = A0["canonical"]
P("  rule diagnostics (canonical): " + "; ".join(f"{g['name']} fex {sig_rule_kms(g, a0)[1]:.2f} Mcoll {sig_rule_kms(g, a0)[2]:.1e} sig_rule {sig_rule_kms(g, a0)[0]:.2f}" for g in SCORED))
P(f"  my 1+delta_ta (LCDM, a_ta=1) = {DELTA_TA:.4f}")

TGT = {("canonical", "sig_fz", "law"): (0.295, 0.163, 1.81), ("canonical", "sig_f", "law"): (0.206, 0.164, 1.26), ("canonical", "sig_f7", "law"): (0.171, 0.172, 0.99),
       ("canonical", "sig_f", "rule"): (-0.151, 0.129, -1.17)}
TGT_ALT = {"sig_fz": 0.275, "sig_f": 0.186, "sig_f7": 0.150}
if not MUTATE:
    for k, (m, e, z) in TGT.items():
        v = RES[k]; ok = abs(v["med"] - m) <= 0.010 and abs(v["tot"] / e - 1) <= 0.10 and abs(v["z"] - z) <= 0.15
        check(f"REPRODUCE canonical {k[1]} {k[2]}", ok, f"mine {v['med']:+.3f} +- {v['tot']:.3f} ({v['z']:+.2f}) vs CFG46 {m:+.3f} +- {e:.3f} ({z:+.2f}); dmed {v['med']-m:+.4f}")
    for key, m in TGT_ALT.items():
        v = RES[("alt", key, "law")]
        check(f"REPRODUCE alt {key} law median", abs(v["med"] - m) <= 0.010, f"mine {v['med']:+.3f} vs {m:+.3f}")
else:
    for k, (m, e, z) in TGT.items():
        v = RES[k]
        check(f"MUTATE: canonical {k[1]} {k[2]} must NOT reproduce CFG46", not (abs(v["med"] - m) <= 0.010), f"mine {v['med']:+.3f} vs {m:+.3f}")
h1 = all(RES[(f, "sig_f", "law")]["z"] > 2 for f in FOOTS)
h2 = all(RES[(f, "sig_f7", "law")]["z"] > 1 for f in FOOTS)
h3 = all(abs(RES[(f, "sig_f", "rule")]["z"]) < 2 for f in FOOTS)
check("H1' law f-free z > 2 both footings (CFG46 expected FAIL)", h1 == False if not MUTATE else (not h1), f"h1={h1}")
check("H2' law f=0.7 z > 1 both footings (CFG46 expected FAIL)", h2 == False if not MUTATE else (not h2), f"h2={h2}  [check is 'agrees with CFG46's verdict']" if not MUTATE else f"h2={h2}")
check("H3' rule f-free |z| < 2 both footings", h3 if not MUTATE else (not h3), f"h3={h3}")

# ================================================================= C2 median and bootstrap checks
P("\n=== C2  median / bootstrap implementation vs brute force ===")
rng = np.random.default_rng(1); ok = True
for _ in range(1000):
    n = int(rng.choice([7, 8])); a = rng.standard_normal(n)
    if my_median(list(a)) != float(np.median(a)): ok = False
check("C2a hand-sorted median == numpy median on 1000 random arrays (n = 7, 8)", ok)
def exact_boot_std(base):
    n = len(base); N = n ** n; s1 = 0.0; s2 = 0.0; cnt = 0
    grid = np.indices((n,) * (n - 2)).reshape(n - 2, -1).T if n > 2 else None
    for a in range(n):
        for b in range(n):
            idx = np.concatenate([np.full((grid.shape[0], 1), a), np.full((grid.shape[0], 1), b), grid], axis=1)
            v = np.sort(base[idx], axis=1)
            med = 0.5 * (v[:, n // 2 - 1] + v[:, n // 2]) if n % 2 == 0 else v[:, n // 2]
            s1 += med.sum(); s2 += (med ** 2).sum(); cnt += med.size
    mu = s1 / cnt
    return math.sqrt(s2 / cnt - mu * mu), mu
EX = {}
for key, lab in KEYS:
    base = RES[("canonical", key, "law")]["base"]
    sd, mu = exact_boot_std(base); EX[key] = sd
    rr = np.random.default_rng(99); big = np.array([np.median(base[rr.integers(0, 8, 8)]) for _ in range(2_000_000)]) if False else None
    rr = np.random.default_rng(99); ii = rr.integers(0, 8, (2_000_000, 8)); big = np.median(base[ii], axis=1)
    mc2000 = RES[("canonical", key, "law")]["boot"]
    check(f"C2b bootstrap std, {lab}", abs(mc2000 / sd - 1) < 0.10 and abs(big.std() / sd - 1) < 0.01,
          f"exact(8^8) {sd:.5f}; 2000-MC {mc2000:.5f} ({mc2000/sd-1:+.1%}); 2e6-MC {big.std():.5f} ({big.std()/sd-1:+.2%})")

# ================================================================= C3 leave-one-out
P("\n=== C3  leave-one-out (canonical) ===")
LOO = {}
for key, lab in KEYS:
    full = RES[("canonical", key, "law")]
    P(f"  {lab}: full median {full['med']:+.3f} z {full['z']:+.2f}")
    for i, g in enumerate(SCORED):
        sub = [x for j, x in enumerate(SCORED) if j != i]
        v = stat(sub, key, "canonical", seed=780 + i)
        LOO[(key, g["name"])] = v
        P(f"    drop {g['name']:7s}: median {v['med']:+.3f} (shift {v['med']-full['med']:+.3f}) +- {v['tot']:.3f} -> {v['z']:+.2f} sigma")
mx = max(abs(LOO[("sig_f", g["name"])]["med"] - RES[("canonical", "sig_f", "law")]["med"]) for g in SCORED)
drv = [g["name"] for g in SCORED if abs(LOO[("sig_f", g["name"])]["med"] - RES[("canonical", "sig_f", "law")]["med"]) > 0.05]
P(f"  max |shift| of the f-free median = {mx:.3f} dex; drivers (>0.05 dex): {drv or 'none'}")

# ================================================================= C4 weights
P("\n=== C4  weighting (canonical; reported only) ===")
FLOOR_SYS = None
for key, lab in KEYS:
    pred = np.array([sig_law_kms(g, A0["canonical"]) for g in SCORED]); obs = np.array([SF * g[key] for g in SCORED]); off = np.log10(obs / pred)
    # symmetrised 1-sigma error in dex from the paper's asymmetric errors
    s = np.array([0.5 * (math.log10(1 + g[key + "_p1"] / g[key]) - math.log10(max(1 - g[key + "_m1"] / g[key], 1e-3))) for g in SCORED])
    fl_ = RES[("canonical", key, "law")]["floor"]
    w1 = 1 / s ** 2; w2 = 1 / (s ** 2 + fl_ ** 2)
    P(f"  {lab:7s} sym dex errors " + " ".join(f"{x:.2f}" for x in s))
    P(f"    unweighted median {np.median(off):+.3f} | IVW median (1/s^2) {wmedian(off, w1):+.3f} | IVW median (1/(s^2+floor^2)) {wmedian(off, w2):+.3f} | IVW mean {np.sum(w1*off)/w1.sum():+.3f} +- {1/math.sqrt(w1.sum()):.3f} ({np.sum(w1*off)/w1.sum()*math.sqrt(w1.sum()):+.2f} sigma stat-only) | unweighted mean {off.mean():+.3f}")
    v3 = stat(SCORED, key, "canonical", err_cols=("_p3", "_m3"), seed=781)
    v1 = RES[("canonical", key, "law")]
    P(f"    measurement term with (3-sigma cols)/3: meas {v3['meas']:.3f} vs {v1['meas']:.3f}; total {v3['tot']:.3f} vs {v1['tot']:.3f}; z {v3['z']:+.2f} vs {v1['z']:+.2f}")

# ================================================================= seed sensitivity
P("\n=== seed sensitivity of the total error (canonical f free) ===")
zs = [stat(SCORED, "sig_f", "canonical", seed=s) for s in (1, 2, 3, 4, 5)]
P("  totals: " + ", ".join(f"{v['tot']:.3f}" for v in zs) + "; z: " + ", ".join(f"{v['z']:+.2f}" for v in zs))

P("\nFAILS: " + (", ".join(FAILS) if FAILS else "none"))
json.dump(dict(mutate=MUTATE, fails=FAILS, res={f"{a}|{b}|{c}": {k: v for k, v in r.items() if k != "base"} for (a, b, c), r in RES.items()}),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg78_results" + ("_MUTATE" if MUTATE else "") + ".json"), "w"), indent=1)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg78" + ("_MUTATE" if MUTATE else "") + ".out"), "w").write("\n".join(OUT))
sys.exit(1 if FAILS else 0)
