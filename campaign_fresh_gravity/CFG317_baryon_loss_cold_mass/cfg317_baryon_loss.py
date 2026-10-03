#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG317 -- does the cold component keep the collapse mass of the baryons a system ORIGINALLY had?  M_c = R M_b,now / f_b, R = M_b,init / M_b,now.

Criteria frozen and committed before any new score: campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/FROZEN_CRITERIA.md (c29d82477).
  harness   CFG313's native-rule harness exec'd read-only (CFG45, CFG58 d2, CFG55, CFG111, CFG39 behind it); the ONLY change is the native hook:
            M_c = R x M_b / f_b (f_b = 0.157126 unchanged, (1 - f_b) unchanged).  V1 = Dutton-Maccio NFW, V2 = isothermal truncated at the law's r_ta.
  (A)       R_need per population / footing / profile from a global grid log R = 0..6 (0.05 dex), and per satellite object.
  (B)       R_ind from the ONLY non-dynamical estimator on disk: a leaky-box effective yield from LVD / Collins+13 stellar [Fe/H] and HI
            (log y_Fe/Z_Fe,sun = -0.2, bracket -0.5..+0.1; a LOWER bound where gas left unprocessed).  SFH quench epochs and every elliptical
            estimator are NOT on disk (named in the criteria).
  (C)       T1 sign test, T2 per-object Spearman (p < 0.01, permutation) with a positive population-level rho, T3 |median log R_need/R_ind| <= 0.3.
  (D)       re-score with M_c = R_ind M_b / f_b (satellites; R = 1 where no estimator exists), V1/V2, both footings, three yields.
CONTROLS  C1 R = 1 reproduces CFG313's native table; C2 identity at R = R_need; C3 the estimator; C4 synthetic positive control (+ shuffle).
MUTATE=1: R_ind shuffled across satellite objects (seed 317) -- T2 must fail and T1' or T1 must fail.
kappa = 1/2 is FITTED.  The cold mass is still required; no dark-matter particle.  Nothing here says the theory is closed.
CHANGED AFTER THE FIRST MAIN RUN, BEFORE ANY INTERPRETATION (disclosed): C3's last clause was coded against the wrong test case (a yield 0.2507 dex above
  solar, where the closed box sits exactly at [Fe/H] = 0, so floating point gave eta = 4e-5) instead of the frozen case (solar [Fe/H], no gas, y = Z_sun);
  it now runs the frozen case.  No estimator value, test, threshold or verdict changed (the estimator code is untouched).
Run: python3 campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/cfg317_baryon_loss.py   (MUTATE=1 for the control)
"""
import os, sys, io, csv, math, json, contextlib
import numpy as np
from scipy.special import exp1
from scipy.optimize import brentq
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("cfg317_baryon_loss", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: R_ind shuffled across satellite objects (seed 317) -- T2 must FAIL and T1'/T1 must FAIL ***")
FOOTS = ("canonical", "alt")
PROFS = ("nfw", "sis")
PNAME = {"nfw": "V1", "sis": "V2"}
GAMMA_E = 0.5772156649015329
LOGY0, LOGY_BR = -0.2, (-0.5, 0.1)
MDF_ALLOW = 0.1
GRID = np.round(np.arange(0.0, 6.0001, 0.05), 4)

# ================================================================================================ load CFG313's harness (read-only)
p313 = os.path.join(LANES, "CFG313_native_collapse_mass", "cfg313_native_rescore.py")
src = open(p313).read()
src = src[:src.index("MODES = {}")]
ns = {"__file__": p313, "__name__": "cfg313_prefix"}
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "cfg313_prefix", "exec"), ns)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
FB0 = float(ns["FB0"]); CFG = ns["CFG"]
SC = dict(mode="global", R=1.0, lookup={}, cur=1.0)


def mc_native317(Mb):                       # called directly by CFG313's CFG55/CFG111 and CFG39 hooks (SLUGGS JAM routes, SPARC rms)
    r = SC["R"] if SC["mode"] == "global" else 1.0
    return r * Mb / (FB0 * CFG["fbx"])


def make_mc317(committed_fn):               # CFG45's hook: (M*_committed, colour, M_b) -> M_c
    def hook(Ms, colour, Mb):
        r = SC["R"] if SC["mode"] == "global" else SC["lookup"].get(float(Ms), 1.0)
        SC["cur"] = r
        return r * Mb / (FB0 * CFG["fbx"])
    return hook


def make_floor317():                        # CFG313's native floor: (floor_mh/1e9) x the native M_c of the same object
    def hook(floor_mh, Mb):
        r = SC["R"] if SC["mode"] == "global" else SC["cur"]
        return (floor_mh / 1e9) * r * Mb / (FB0 * CFG["fbx"])
    return hook


ns["mc_native"], ns["make_mc"], ns["make_floor"] = mc_native317, make_mc317, make_floor317


def g_uf(b, f): v = b["UF"][(f, "S")]; return v["km"], v["z"]
def g_cl(key): return lambda b, f: (b["CL"][(key, f, "S")]["med"], b["CL"][(key, f, "S")]["z"])
def g_d2(b, f): v = b["D2"][(f, "S")]; return v["med"], v["z"]
def g_ugc(b, f): v = b["U2"][(f, "S")]; return v["off"], v["z"]
def g_s0(b, f): v = b["DT"][(f, "S")]; return v["s0"]["corr"], v["s0z"]
def g_dt(b, f): v = b["DT"][(f, "S")]["all"]; return v["corr"], v["z"]
def g_sl(b, f): v = b["SL"][(f, "S")]; return v["mean"], v["z"]
def g_c55(k): return lambda b, f: (b["C55"][f][k]["mean"], b["C55"][f][k]["z"])
def g_c111(b, f): v = b["C111"][f]["rule"]; return v["mean"], v["z"]
def g_xr(b, f): v = b["XR"][(f, "S")]; return v["mean"], v["z"]
def g_og(b, f): v = b["OG"][(f, "S")]; return v["mean"], v["z"]


absz = lambda zc, za: abs(zc) < 2 and abs(za) < 2
above = lambda zc, za: zc > -2 and za > -2
ROWS = [("P1", "MW ultra-faints", g_uf, absz), ("P2a", "MW classical", g_cl("cls"), above), ("P2b", "M31 Collins+13", g_cl("col"), above),
        ("P2c", "M31 LVD", g_cl("m31"), above), ("P2d", "LV field dwarfs", g_d2, absz), ("P4a", "UGC 2487", g_ugc, absz),
        ("P4b", "Di Teodoro four S0", g_s0, lambda zc, za: zc > -2), ("P4b'", "Di Teodoro all 15 (reported)", g_dt, None),
        ("P5", "SLUGGS h50 masses", g_sl, absz), ("P5J", "SLUGGS JAM gamma 3", g_c55("rule"), absz), ("P5S", "SLUGGS SLUGGS masses", g_c55("rule_sl"), absz),
        ("P5L", "SLUGGS JAM literature gamma", g_c111, absz), ("P6", "X-ray ellipticals", g_xr, absz), ("P7", "Ogle super spirals (reported)", g_og, None)]
RID = [r[0] for r in ROWS]
SAT = {"P1": "ufd", "P2a": "cls", "P2b": "col", "P2c": "m31", "P2d": "fld"}
LABEL = {"P1": "HIGH", "P5": "HIGH", "P5J": "HIGH", "P5S": "HIGH", "P5L": "HIGH", "P6": "HIGH", "P2b": "LOW", "P2c": "LOW", "P2d": "LOW", "SPARC": "LOW"}


def sparc_ok(b):
    a3 = b["SP"][("dwarf", "S")]["frac_lt003"] >= 0.9 and b["SP"][("spiral", "S")]["frac_lt003"] >= 0.9
    return a3 and (b["C39"]["rms1"] - b["C39"]["rms0"]) < 0.005


def samples(n45):
    return {"ufd": n45["SAMPLES"]["ufd"], "cls": n45["SAMPLES"]["cls"], "col": n45["SAMPLES"]["col"], "m31": n45["SAMPLES"]["m31"],
            "fld": n45["g42"]["ns"]["fld"]}


def per_object(n45, prof):
    """per-object offsets log sigma_obs/sigma_pred (reading S) for the resolved satellites, both footings, at the current hook state."""
    CFG.update(mode="native", prof=prof)
    S = samples(n45); out = {}
    for key, smp in S.items():
        for f in FOOTS:
            out[(key, f)] = np.array([math.log10(d["sig"] / n45["sigma_read"](d, f, "S", gas=(key in ("cls", "col", "m31")))[0]) for d in smp])
    CFG.update(mode="committed", prof="nfw")
    return out


def run(prof):
    b, n45 = ns["run_mode"]("native", prof)
    return b, n45


def extract(b):
    row = {rid: {f: tuple(map(float, gt(b, f))) for f in FOOTS} for rid, _, gt, _ in ROWS}
    row["SPARC"] = dict(ok=bool(sparc_ok(b)), dwarf=b["SP"][("dwarf", "S")]["frac_lt003"], spiral=b["SP"][("spiral", "S")]["frac_lt003"],
                        drms=b["C39"]["rms1"] - b["C39"]["rms0"])
    return row


# ================================================================================================ (A) the scans
R.banner("(A)  THE R_need SCANS: one global R, log R = 0..6 in 0.05 dex, V1 and V2, both footings")
SCAN, OBJ = {}, {}
N45 = None
for prof in PROFS:
    SCAN[prof], OBJ[prof] = [], []
    for lr in GRID:
        SC.update(mode="global", R=float(10 ** lr))
        b, n45 = run(prof)
        SCAN[prof].append(extract(b)); OBJ[prof].append(per_object(n45, prof))
        N45 = n45
    P(f"    {PNAME[prof]}: {len(GRID)} grid points done {R.el()}")
SC.update(mode="global", R=1.0)
S_ALL = samples(N45)
NAMES = {k: [d["name"] for d in v] for k, v in S_ALL.items()}


def first_cross(lr, y, level=0.0):
    """smallest log R where y crosses `level` going down (y decreasing); returns 0 if y[0] <= level, inf if never."""
    if y[0] <= level:
        return 0.0
    for i in range(1, len(y)):
        if y[i] <= level:
            return float(lr[i - 1] + (lr[i] - lr[i - 1]) * (y[i - 1] - level) / (y[i - 1] - y[i]))
    return float("inf")


def interval(lr, mask):
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return None
    contiguous = bool(np.all(np.diff(idx) == 1))
    return [float(lr[idx[0]]), float(lr[idx[-1]]), contiguous]


NEED = {}
for prof in PROFS:
    for f in FOOTS:
        for rid, lab, gt, gate in ROWS:
            s = np.array([row[rid][f][0] for row in SCAN[prof]]); z = np.array([row[rid][f][1] for row in SCAN[prof]])
            mono = bool(np.all(np.diff(s) <= 1e-12))
            onset = next((float(GRID[i]) for i in range(1, len(GRID)) if abs(s[i] - s[0]) > 1e-9), float("inf"))
            gmask = np.array([gate(row[rid]["canonical"][1], row[rid]["alt"][1]) for row in SCAN[prof]]) if gate else None
            NEED[(prof, f, rid)] = dict(lr0=first_cross(GRID, s), s1=float(s[0]), z1=float(z[0]), mono=mono, onset=onset,
                                        one_sigma=interval(GRID, np.abs(z) <= 1), gate=(interval(GRID, gmask) if gate else None),
                                        s=s.tolist(), z=z.tolist())
        sp = [row["SPARC"]["ok"] for row in SCAN[prof]]
        NEED[(prof, f, "SPARC")] = dict(lr0=0.0, s1=0.0, z1=0.0, Rmax=(float(GRID[np.where(sp)[0][-1]]) if sp[0] else None),
                                        contiguous=bool(all(sp[:int(np.sum(sp))])) if sp[0] else None)

fmtlr = lambda x: (">6" if not np.isfinite(x) else f"{x:.2f}")
P(f"\n    log10 R_need,0 (statistic crosses zero; 0 = no extra mass needed) | onset (first grid R that moves the statistic) | 1-sigma interval | gate interval (both footings)")
for prof in PROFS:
    for f in FOOTS:
        P(f"  -- {PNAME[prof]} {f}")
        for rid, lab, gt, gate in ROWS:
            n = NEED[(prof, f, rid)]
            P(f"    {rid:5s} {lab:30s} s(R=1) {n['s1']:+.3f} z {n['z1']:+.2f} | log R_need,0 {fmtlr(n['lr0']):>5s} | onset {fmtlr(n['onset']):>5s} | 1sig {n['one_sigma']} | gate {n['gate']} | monotone {n['mono']}")
        n = NEED[(prof, f, "SPARC")]
        P(f"    SPARC control: both clauses hold up to log R_max = {n['Rmax']} (contiguous from 0: {n['contiguous']})")

# per-object R_need (satellites)
OBJNEED = {}
for prof in PROFS:
    for f in FOOTS:
        for key in S_ALL:
            arr = np.array([o[(key, f)] for o in OBJ[prof]])          # grid x objects
            OBJNEED[(prof, f, key)] = [min(first_cross(GRID, arr[:, j]), 6.0) for j in range(arr.shape[1])]

# R_LCDM (reported) and per-object analytic R_switch
hm, col = N45["halo_mass"], N45["collapse"]; UPS = N45["UPS_V"]; inf_gas = N45["infall_gas"]; ei = N45["edge_info"]


def mb_lane(d, key):
    Ms = UPS * d["LV"]
    return Ms + (max(1.33 * d["MHI"], inf_gas(d)) if key in ("cls", "col", "m31") else 1.33 * d["MHI"])


RSW, RLCDM = {}, {}
for key, smp in S_ALL.items():
    RSW[key] = {f: [math.log10(ei(mb_lane(d, key), f)[0] / ((1 - FB0) * mb_lane(d, key) / FB0)) for d in smp] for f in FOOTS}
    RLCDM[key] = [math.log10(float(hm(UPS * d["LV"])) * FB0 / mb_lane(d, key)) for d in smp]
RLCDM["P5"] = [math.log10(col(r["Mstar"], "red") * FB0 / r["Mstar"]) for r in N45["RES50"]]
RLCDM["P6"] = [math.log10(col(g["uk"] * g["LK"], "red") * FB0 / (g["uk"] * g["LK"])) for g in N45["GAL"]]
P("\n    reported: median log R implied by the committed LCDM collapse masses (M_c,committed f_b / M_b): " +
  "; ".join(f"{k} {np.median(v):.2f}" for k, v in RLCDM.items()))
P("    reported: median per-object analytic log R_switch (canonical): " + "; ".join(f"{k} {np.median(RSW[k]['canonical']):.2f}" for k in RSW))

# ================================================================================================ (B) the estimator
R.banner("(B)  R_ind: leaky-box effective yield from stellar [Fe/H] and HI (data on disk only)")
DSPH = os.path.join(C.REPO, "real_research", "data", "dsph")


def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DSPH, fn))):
        fe = fnum(r["metallicity"]); em, ep = fnum(r["metallicity_em"]), fnum(r["metallicity_ep"])
        err = 0.5 * (em + ep) if (em is not None and ep is not None) else (em or ep or 0.2)
        mh = fnum(r["mass_HI"])
        LVD[r["name"].strip()] = dict(feh=fe, efeh=err if err > 0 else 0.2, MHI=(10 ** mh if mh is not None else 0.0), src="LVD " + (r["metallicity_type"] or "-"))
COLL = {}
for line in open(os.path.join(DSPH, "collins2013_m31_dsph.tsv"), encoding="latin-1"):
    if line.startswith("#") or not line.strip():
        continue
    f_ = line.split("\t")
    if len(f_) < 30 or not f_[0].strip().isdigit():
        continue
    COLL[f_[1].strip()] = dict(feh=fnum(f_[28]), efeh=fnum(f_[29]) or 0.2)


def collins_name(lvd_name):
    if lvd_name == "Cassiopeia II":
        return "And XXX"
    return lvd_name.replace("Andromeda ", "And ") if lvd_name.startswith("Andromeda ") else None


def metal_of(name, key):
    if key == "col":
        c = COLL.get(name)
        return (c["feh"], c["efeh"], "Collins+13") if c and c["feh"] is not None else (None, None, "-")
    m = LVD.get(name)
    if m and m["feh"] is not None:
        return m["feh"], m["efeh"], m["src"]
    if key == "m31":
        c = COLL.get(collins_name(name) or "")
        if c and c["feh"] is not None:
            return c["feh"], c["efeh"], "Collins+13 (fallback)"
    return None, None, "-"


def elnx(X):
    """E[ln x] for x ~ e^-x truncated to (0, X): (-gamma - E1(X) - e^-X ln X) / (1 - e^-X); X = inf -> -gamma."""
    if not np.isfinite(X):
        return -GAMMA_E
    return (-GAMMA_E - exp1(X) - math.exp(-X) * math.log(X)) / (1.0 - math.exp(-X))


def leaky(feh, Ms, Mg, logy):
    """solve the mass loading eta so that the model's mean log10 Z (solar units) equals the observed mean [Fe/H]; returns (eta, R_ind, residual)."""
    def model(eta):
        p = logy - math.log10(1.0 + eta)
        X = float("inf") if Mg <= 0 else math.log((Mg + (1.0 + eta) * Ms) / Mg)
        return p + elnx(X) / math.log(10)
    g = lambda le: model(10 ** le - 1.0) - feh                 # in log10(1 + eta)
    if g(0.0) <= 0:
        return 0.0, 1.0, 0.0
    hi = 7.0
    grid = np.linspace(0, hi, 141); vals = [g(x) for x in grid]
    k = next(i for i in range(1, len(grid)) if vals[i] <= 0)
    le = brentq(g, grid[k - 1], grid[k], xtol=1e-13, rtol=1e-13)
    eta = 10 ** le - 1.0
    return eta, ((1 + eta) * Ms + Mg) / (Ms + Mg), g(le)


def r_ind_obj(d, key, logy):
    fe, efe, srcm = metal_of(d["name"], key)
    if fe is None:
        return None
    Ms = UPS * d["LV"]; Mg = 1.33 * (LVD.get(d["name"], {}).get("MHI", 0.0) if key != "col" else 0.0)
    eta, Rv, res = leaky(fe, Ms, Mg, logy)
    s = math.hypot(efe, MDF_ALLOW)
    lo = math.log10(leaky(fe + s, Ms, Mg, logy)[1]); hi_ = math.log10(leaky(fe - s, Ms, Mg, logy)[1])
    return dict(feh=fe, efeh=efe, src=srcm, Mg=Mg, Ms=Ms, eta=eta, lR=math.log10(Rv), elR=0.5 * abs(hi_ - lo), res=res)


EST = {}
for logy in (LOGY0,) + LOGY_BR:
    for key, smp in S_ALL.items():
        EST[(logy, key)] = [r_ind_obj(d, key, logy) for d in smp]
    EST[(logy, "ul")] = [r_ind_obj(d, "ufd", logy) for d in N45["UL"]]

# C3 the estimator
e_inf = math.log10(10 ** LOGY0) + elnx(float("inf")) / math.log(10)
c3a = abs((e_inf - LOGY0) - (-0.2507)) < 1e-4 and abs(elnx(float("inf")) + GAMMA_E) < 1e-15
# numerical check of the closed form against direct quadrature at a finite truncation
from scipy.integrate import quad
Xt = 2.3; num = quad(lambda x: math.log(x) * math.exp(-x), 0, Xt, limit=200)[0] / (1 - math.exp(-Xt))
c3b = abs(num - elnx(Xt)) < 1e-6
c3c = abs(elnx(60.0) + GAMMA_E) < 1e-6
allobj = [o for k, v in EST.items() for o in v if o is not None]
res_max = max(abs(o["res"]) for o in allobj); rmin = min(o["lR"] for o in allobj)
eta0, R0, _ = leaky(0.0, 1e6, 0.0, 0.0)                 # the frozen test: solar [Fe/H], no gas, y = Z_sun -> eta = 0, R = 1
check("C3 CONTROL: the estimator -- E[log Z] at mu'=0 is log p - 0.2507 (1e-4 printed precision; -gamma exact); the closed form equals quadrature (1e-6); "
      "every root residual < 1e-8 dex; R_ind >= 1 for every object; a closed box at its own yield returns eta = 0, R = 1",
      f"E[ln x](inf) + gamma = {elnx(float('inf')) + GAMMA_E:.1e}; quad vs closed form at X=2.3: {abs(num - elnx(Xt)):.1e}; X=60: {abs(elnx(60.0) + GAMMA_E):.1e}; "
      f"max |residual| {res_max:.1e} over {len(allobj)} object-yield evaluations; min log R_ind {rmin:.3f}; closed-box test eta {eta0:.2e}, R {R0:.12f}",
      c3a and c3b and c3c and res_max < 1e-8 and rmin >= -1e-12 and abs(R0 - 1) < 1e-9)

PKEYS = ["P1", "P2a", "P2b", "P2c", "P2d"]


def pop_rind(logy, perm=None):
    """population median log R_ind (P1 includes its 9 limits) and a bootstrap error; perm = shuffled per-object values (MUTATE)."""
    out = {}
    for rid in PKEYS:
        key = SAT[rid]
        vals = [o["lR"] for o in EST[(logy, key)] if o is not None]
        if rid == "P1":
            vals += [o["lR"] for o in EST[(logy, "ul")] if o is not None]
        if perm is not None:
            vals = perm[rid]
        v = np.array(vals); rng = np.random.default_rng(317)
        bs = [np.median(v[rng.integers(0, len(v), len(v))]) for _ in range(2000)]
        out[rid] = dict(med=float(np.median(v)), err=float(np.std(bs)), n=len(v), n_total=len(S_ALL[key]) + (len(N45["UL"]) if rid == "P1" else 0))
    return out


# MUTATE: shuffle R_ind across all satellite objects (seed 317), keeping each population's count
SHUF = None
if MUTATE:
    rng = np.random.default_rng(317)
    pool, slots = [], []
    for rid in PKEYS:
        key = SAT[rid]
        lst = [("obj", key, j) for j, o in enumerate(EST[(LOGY0, key)]) if o is not None]
        if rid == "P1":
            lst += [("ul", "ul", j) for j, o in enumerate(EST[(LOGY0, "ul")]) if o is not None]
        for s_ in lst:
            pool.append((EST[(LOGY0, s_[1])][s_[2]])["lR"]); slots.append((rid,) + s_)
    perm = rng.permutation(len(pool))
    SHUF = {sl: pool[perm[i]] for i, sl in enumerate(slots)}

RIND = {logy: pop_rind(logy) for logy in (LOGY0,) + LOGY_BR}
if MUTATE:
    pp = {rid: [v for sl, v in SHUF.items() if sl[0] == rid] for rid in PKEYS}
    RIND[LOGY0] = pop_rind(LOGY0, perm=pp)


def lr_obj(key, j, logy=LOGY0):
    """per-object log R_ind used by the tests and the re-score (shuffled in MUTATE)."""
    if MUTATE and logy == LOGY0:
        rid = [r for r in PKEYS if SAT[r] == key][0]
        return SHUF.get((rid, "obj", key, j))
    o = EST[(logy, key)][j]
    return None if o is None else o["lR"]


P(f"    yield log y_Fe/Z_Fe,sun = {LOGY0} (bracket {LOGY_BR}); MDF-shape allowance {MDF_ALLOW} dex; Upsilon_V = {UPS}; gas = 1.33 M_HI (LVD), 0 for Collins rows")
for rid in PKEYS:
    key = SAT[rid]; lst = EST[(LOGY0, key)]
    P(f"  -- {rid} {S_ALL and dict(P1='MW ultra-faints', P2a='MW classical', P2b='M31 Collins+13', P2c='M31 LVD', P2d='LV field')[rid]}: "
      f"median log R_ind {RIND[LOGY0][rid]['med']:.2f} +- {RIND[LOGY0][rid]['err']:.2f} (n = {RIND[LOGY0][rid]['n']} of {RIND[LOGY0][rid]['n_total']}); "
      f"at yield -0.5 / +0.1: {RIND[-0.5][rid]['med']:.2f} / {RIND[0.1][rid]['med']:.2f}")
    for d, o in zip(S_ALL[key], lst):
        if o is None:
            P(f"       {d['name']:22s} no [Fe/H] on disk")
        else:
            P(f"       {d['name']:22s} [Fe/H] {o['feh']:+.2f} +- {o['efeh']:.2f} ({o['src']}); M* {o['Ms']:.2e}; M_gas {o['Mg']:.2e}; eta {o['eta']:8.1f}; log R_ind {o['lR']:.2f} +- {o['elR']:.2f}")
    if rid == "P1":
        for d, o in zip(N45["UL"], EST[(LOGY0, "ul")]):
            P(f"       {d['name'] + ' (limit)':22s} " + ("no [Fe/H] on disk" if o is None else f"[Fe/H] {o['feh']:+.2f}; log R_ind {o['lR']:.2f} +- {o['elR']:.2f}"))
P("    no estimator on disk: SLUGGS (all routes), X-ray ellipticals, SPARC (and UGC 2487, Di Teodoro, Ogle): R = 1 in (D)")

# ================================================================================================ (C) the tests
R.banner("(C)  THE TESTS: T1 sign, T2 correlation, T3 ratio; decision per footing x profile")


def perm_p(x, y, n=10000, seed=317):
    x = np.asarray(x, float); y = np.asarray(y, float)
    r0 = spearmanr(x, y).correlation
    if not np.isfinite(r0):
        return float("nan"), 1.0
    rng = np.random.default_rng(seed); cnt = 0
    for _ in range(n):
        r = spearmanr(x, rng.permutation(y)).correlation
        cnt += (np.isfinite(r) and r >= r0 - 1e-15)
    return float(r0), (cnt + 1) / (n + 1)


def exact_pop_p(x, y):
    import itertools
    x = np.asarray(x, float); y = np.asarray(y, float); r0 = spearmanr(x, y).correlation
    if not np.isfinite(r0):
        return float("nan"), 1.0
    rs = [spearmanr(x, np.array(pm)).correlation for pm in itertools.permutations(y)]
    return float(r0), float(np.mean([np.isfinite(r) and r >= r0 - 1e-15 for r in rs]))


def tests(prof, foot, logy=LOGY0, need_override=None, obj_override=None):
    rind = RIND[logy]
    # T1 sign
    rows = {}
    for rid, lab in LABEL.items():
        if rid == "SPARC":
            nd = "~1" if NEED[(prof, foot, "SPARC")]["Rmax"] is not None else "large"
        else:
            nd = "large" if NEED[(prof, foot, rid)]["z1"] > 1 else "~1"
        ri = rind.get(rid)
        ic = None if ri is None else ("large" if ri["med"] > 0.5 else "~1")
        want = "large" if lab == "HIGH" else "~1"
        rows[rid] = dict(label=lab, need=nd, rind=ic, ok=(nd == want and ic == want))
    t1 = all(r["ok"] for r in rows.values())
    t1p = all(r["ok"] for r in rows.values() if r["rind"] is not None)
    hi = [rind[r]["med"] for r in rind if LABEL.get(r) == "HIGH"]; lo = [rind[r]["med"] for r in rind if LABEL.get(r) == "LOW"]
    order = bool(hi and lo and min(hi) > max(lo))
    # T2 per object
    xs, ys, xu, yu = [], [], [], []
    for rid in PKEYS:
        key = SAT[rid]
        nds = obj_override[key] if obj_override else OBJNEED[(prof, foot, key)]
        for j, nd in enumerate(nds):
            li = lr_obj(key, j, logy)
            if li is None:
                continue
            xs.append(li); ys.append(nd)
            if key == "ufd":
                xu.append(li); yu.append(nd)
    rho, p = perm_p(xs, ys); rho_u, p_u = perm_p(xu, yu)
    popn = need_override or {rid: NEED[(prof, foot, rid)]["lr0"] for rid in PKEYS}
    px = [rind[r]["med"] for r in PKEYS]; py = [min(popn[r], 6.0) for r in PKEYS]
    rho_pop, p_pop = exact_pop_p(px, py)
    t2 = (p < 0.01) and (rho_pop > 0)
    # T3 ratio
    lr = np.array([min(popn[r], 6.0) - rind[r]["med"] for r in PKEYS])
    objr = np.array(ys) - np.array(xs)
    med = float(np.median(lr)); t3 = abs(med) <= 0.3
    partial = (not (t1 and t2 and t3)) and t1p and ((p < 0.05 and rho > 0) or t3)
    dec = "SUPPORTED" if (t1 and t2 and t3) else ("PARTIAL" if partial else "NOT SUPPORTED")
    return dict(T1=t1, T1p=t1p, order=order, sign_rows=rows, T2=t2, rho=rho, p=p, n_obj=len(xs), rho_ufd=rho_u, p_ufd=p_u, n_ufd=len(xu),
                rho_pop=rho_pop, p_pop=p_pop, T3=t3, ratio_pop=dict(zip(PKEYS, lr.tolist())), ratio_med=med, ratio_std=float(np.std(lr)),
                ratio_obj_med=float(np.median(objr)), ratio_obj_std=float(np.std(objr)), frac_obj_need_ge_ind=float(np.mean(objr >= 0)), decision=dec)


TEST = {(prof, f): tests(prof, f) for prof in PROFS for f in FOOTS}
for (prof, f), t in TEST.items():
    P(f"  -- {PNAME[prof]} {f}: decision {t['decision']}")
    P("       sign rows: " + "; ".join(f"{k} [{v['label']}] need {v['need']} / R_ind {v['rind'] or 'NONE'} -> {'ok' if v['ok'] else 'X'}" for k, v in t["sign_rows"].items()))
    P(f"       T1 {t['T1']} | T1' (populations with an R_ind) {t['T1p']} | relative order (HIGH R_ind > every LOW) {t['order']}")
    P(f"       T2 per-object rho {t['rho']:+.3f}, p {t['p']:.4f} (n {t['n_obj']}); within ultra-faints rho {t['rho_ufd']:+.3f}, p {t['p_ufd']:.4f} (n {t['n_ufd']}); "
      f"population rho {t['rho_pop']:+.3f}, exact p {t['p_pop']:.3f} -> T2 {t['T2']}")
    P(f"       T3 log(R_need,0/R_ind) by population: " + ", ".join(f"{k} {v:+.2f}" for k, v in t["ratio_pop"].items()) +
      f"; median {t['ratio_med']:+.2f} (std {t['ratio_std']:.2f}); per object median {t['ratio_obj_med']:+.2f} (std {t['ratio_obj_std']:.2f}); "
      f"fraction of objects with R_need >= R_ind {t['frac_obj_need_ge_ind']:.2f} -> T3 {t['T3']}")
TB = {(prof, f, ly): tests(prof, f, ly) for prof in PROFS for f in FOOTS for ly in LOGY_BR}
P("    reported, yield bracket ends: " + "; ".join(f"{PNAME[p_]} {f} y{ly:+.1f}: T3 median {t['ratio_med']:+.2f}, {t['decision']}" for (p_, f, ly), t in TB.items()))

prim = TEST[("nfw", "canonical")]
check("T1 THE SIGN TEST (V1 canonical, frozen): every labelled population's need class and R_ind class equal its label (a missing R_ind cannot pass)",
      "; ".join(f"{k}: need {v['need']}, R_ind {v['rind'] or 'NONE'} [{v['label']}]" for k, v in prim["sign_rows"].items()) +
      f" | T1' {prim['T1p']} | other combos T1: {[TEST[k]['T1'] for k in TEST]}", prim["T1"])
check("T2 THE CORRELATION (V1 canonical, frozen): per-object Spearman log R_need,0 vs log R_ind over the satellites, one-sided permutation p < 0.01, AND population rho > 0",
      f"rho {prim['rho']:+.3f}, p {prim['p']:.4f} (n {prim['n_obj']}); population rho {prim['rho_pop']:+.3f}; other combos p: " +
      ", ".join(f"{PNAME[k[0]]} {k[1]} {TEST[k]['p']:.4f}" for k in TEST), prim["T2"])
check("T3 THE RATIO (V1 canonical, frozen): |median over populations of log(R_need,0 / R_ind)| <= 0.3 dex",
      f"median {prim['ratio_med']:+.2f} dex (std {prim['ratio_std']:.2f}); ultra-faints {prim['ratio_pop']['P1']:+.2f}; other combos: " +
      ", ".join(f"{PNAME[k[0]]} {k[1]} {TEST[k]['ratio_med']:+.2f}" for k in TEST), prim["T3"])
decs = sorted(set(t["decision"] for t in TEST.values()))
headline = decs[0] if len(decs) == 1 else "SPLIT: " + ", ".join(f"{PNAME[k[0]]} {k[1]} {TEST[k]['decision']}" for k in TEST)
check("DECISION (reported; frozen rule, all four footing x profile combinations)", headline, True, load_bearing=False)

# C4 synthetic positive control
rng4 = np.random.default_rng(317)
syn_obj, syn_pop = {}, {}
for rid in PKEYS:
    key = SAT[rid]
    syn_obj[key] = [((lr_obj(key, j) if lr_obj(key, j) is not None else 0.0) + rng4.normal(0, 0.15)) for j in range(len(S_ALL[key]))]
for rid in PKEYS:
    key = SAT[rid]; v = [syn_obj[key][j] for j in range(len(S_ALL[key])) if lr_obj(key, j) is not None]
    syn_pop[rid] = float(np.median(v))
t4 = tests("nfw", "canonical", need_override=syn_pop, obj_override=syn_obj)
rng5 = np.random.default_rng(318)
flat = [(k, j) for k in syn_obj for j in range(len(syn_obj[k]))]; vals = [syn_obj[k][j] for k, j in flat]; pm = rng5.permutation(len(vals))
sh_obj = {k: list(v) for k, v in syn_obj.items()}
for i, (k, j) in enumerate(flat):
    sh_obj[k][j] = vals[pm[i]]
t5 = tests("nfw", "canonical", need_override=syn_pop, obj_override=sh_obj)
check("C4 CONTROL (synthetic): R_need,syn = R_ind x 10^N(0,0.15) gives T2 pass (p < 0.01) and T3 pass; the same values shuffled across objects give T2 FAIL",
      f"synthetic: rho {t4['rho']:+.3f}, p {t4['p']:.4f}, pop rho {t4['rho_pop']:+.2f}, T3 median {t4['ratio_med']:+.3f}; shuffled: rho {t5['rho']:+.3f}, p {t5['p']:.3f}",
      t4["T2"] and t4["T3"] and not t5["T2"])

# ================================================================================================ C1 (R = 1) and C2 (identity)
R.banner("C1 / C2  CONTROLS: R = 1 reproduces CFG313; R = R_need,0 reproduces the data by construction")
c313 = json.load(open(os.path.join(LANES, "CFG313_native_collapse_mass", "cfg313_native_rescore_results.json")))["numbers"]["TABLE"]
dev = []
for prof in PROFS:
    row0 = SCAN[prof][0]; vn = "native_V1" if prof == "nfw" else "native_V2"
    for rid in RID:
        for f in FOOTS:
            dev.append((f"{rid} {PNAME[prof]} {f}", max(abs(row0[rid][f][0] - c313[rid][vn][f][0]), abs(row0[rid][f][1] - c313[rid][vn][f][1]))))
    for kind in ("dwarf", "spiral"):
        dev.append((f"SPARC {kind} {PNAME[prof]}", abs(row0["SPARC"][kind] - c313["P3 " + kind]["V1" if prof == "nfw" else "V2"])))
    dev.append((f"SPARC rms {PNAME[prof]}", abs(row0["SPARC"]["drms"] + c313["P8"]["law"] - c313["P8"]["V1" if prof == "nfw" else "V2"])))
w = max(dev, key=lambda t: t[1])
check("C1 CONTROL: at R = 1 every population statistic and z (V1, V2, both footings), SPARC A3 fractions and rms reproduce CFG313's committed native table to 1e-9",
      f"{len(dev)} comparisons; worst {w[0]}: {w[1]:.1e}", w[1] <= 1e-9)

idn = []
for rid in RID:
    lr0 = NEED[("nfw", "canonical", rid)]["lr0"]
    if 0 < lr0 < 6:
        SC.update(mode="global", R=float(10 ** lr0))
        b, _ = run("nfw")
        idn.append((rid, lr0, ROWS[RID.index(rid)][2](b, "canonical")[0]))
SC.update(mode="global", R=1.0)
wi = max(idn, key=lambda t: abs(t[2])) if idn else ("-", 0, 0.0)
check("C2 CONTROL (identity): re-run at exactly R = R_need,0 (V1 canonical), every population with 1 < R_need,0 < 1e6 has |statistic| < 0.005 dex",
      "; ".join(f"{a} log R {b_:.2f}: {c_:+.4f}" for a, b_, c_ in idn) + f" | worst {wi[0]} {wi[2]:+.4f}", bool(idn) and abs(wi[2]) < 0.005)

# ================================================================================================ (D) the re-score with R_ind
R.banner("(D)  RE-SCORE with M_c = R_ind x M_b,now / f_b (satellites; R = 1 where no estimator exists), V1/V2, both footings, three yields")


def lookup_for(logy):
    lk, coll = {}, []
    for rid in PKEYS:
        key = SAT[rid]
        medpop = RIND[logy][rid]["med"]
        objs = list(S_ALL[key]) + (list(N45["UL"]) if key == "ufd" else [])
        for j, d in enumerate(objs):
            if key == "ufd" and j >= len(S_ALL[key]):
                jj = j - len(S_ALL[key])
                if MUTATE and logy == LOGY0:
                    li = SHUF.get((rid, "ul", "ul", jj))
                else:
                    o = EST[(logy, "ul")][jj]; li = None if o is None else o["lR"]
            else:
                li = lr_obj(key, j, logy)
            if li is None:
                li = medpop
            k = float(UPS * d["LV"]); r = 10 ** li
            if k in lk and abs(math.log10(lk[k]) - li) > 1e-12:
                coll.append((d["name"], key)); lk[k] = 10 ** (0.5 * (math.log10(lk[k]) + li))
            else:
                lk[k] = r
    return lk, coll


RES = {}
for logy in (LOGY0,) + LOGY_BR:
    lk, coll = lookup_for(logy)
    SC.update(mode="perobj", lookup=lk)
    for prof in PROFS:
        b, n45 = run(prof)
        RES[(logy, prof)] = extract(b)
    RES[(logy, "collisions")] = coll
SC.update(mode="global", R=1.0, lookup={})
P("    key collisions (two objects with the same committed M*): " + str({ly: RES[(ly, 'collisions')] for ly in (LOGY0,) + LOGY_BR}))
MOVES = {}
P(f"    {'tile':34s} {'R = 1 (CFG313)':>26s} {'R_ind V1':>26s} {'R_ind V2':>26s}   gate R=1 / V1 / V2   [yield -0.5 | +0.1 V1]")
for rid, lab, gt, gate in ROWS:
    r1 = SCAN["nfw"][0][rid]; a1 = RES[(LOGY0, "nfw")][rid]; a2 = RES[(LOGY0, "sis")][rid]
    lo1, hi1 = RES[(-0.5, "nfw")][rid], RES[(0.1, "nfw")][rid]
    fz = lambda d: f"{d['canonical'][0]:+.3f} ({d['canonical'][1]:+.2f}|{d['alt'][1]:+.2f})"
    gs = (lambda d: ("P" if gate(d["canonical"][1], d["alt"][1]) else "F")) if gate else (lambda d: "-")
    P(f"    {rid + ' ' + lab:34s} {fz(r1):>26s} {fz(a1):>26s} {fz(a2):>26s}   {gs(r1)} / {gs(a1)} / {gs(a2)}   [{fz(lo1)} | {fz(hi1)}]")
    if gate:
        for tag, d in (("V1", a1), ("V2", a2), ("V1 y-0.5", lo1), ("V1 y+0.1", hi1), ("V2 y+0.1", RES[(0.1, "sis")][rid])):
            if gs(r1) != gs(d):
                MOVES.setdefault(tag, []).append(f"{rid} {'red->green' if gs(d) == 'P' else 'green->red'}")
for prof in PROFS:
    P(f"    SPARC control {PNAME[prof]}: clauses hold {RES[(LOGY0, prof)]['SPARC']['ok']} (R = 1 by construction: no estimator)")
shift = max(abs(RES[(LOGY0, p_)][rid][f][0] - SCAN[p_][0][rid][f][0]) for p_ in PROFS for rid in RID for f in FOOTS)
shift_hi = max(abs(RES[(0.1, p_)][rid][f][0] - SCAN[p_][0][rid][f][0]) for p_ in PROFS for rid in RID for f in FOOTS)
check("D1 (reported) tile moves under R_ind against R = 1 (CFG313 native)", f"moves: {MOVES or 'none'}; largest statistic shift {shift:.2e} dex (nominal yield), {shift_hi:.2e} (yield +0.1)",
      True, load_bearing=False)

# PF1 prediction
pf = []
for rid in PKEYS:
    on = NEED[("nfw", "canonical", rid)]["onset"]
    pf.append((rid, RIND[LOGY0][rid]["med"], on))
nobj_over = sum(1 for key in S_ALL for j in range(len(S_ALL[key])) if lr_obj(key, j) is not None and lr_obj(key, j) > RSW[key]["canonical"][j])
check("PF1 [pre-flight prediction; can fail]: every satellite population's median R_ind lies below the R at which its statistic first moves (V1 canonical), "
      "so the (D) re-score moves no satellite tile",
      "; ".join(f"{a}: log R_ind {b_:.2f} vs onset {fmtlr(c_)}" for a, b_, c_ in pf) + f"; objects whose own R_ind exceeds their analytic R_switch: {nobj_over}; satellite tile moves (V1/V2 nominal): "
      f"{[m for t in ('V1', 'V2') for m in MOVES.get(t, []) if m.split()[0] in PKEYS]}",
      all(b_ < c_ for _, b_, c_ in pf) and not [m for t in ("V1", "V2") for m in MOVES.get(t, []) if m.split()[0] in PKEYS])

if MUTATE:
    R.banner("MUTATE CHECK: with R_ind shuffled across objects, T2 must fail and T1' or T1 must fail")
    check("MUTATE CHECK (V1 canonical): T2 FAILS and (T1' or T1) FAILS under the shuffle", f"T2 {prim['T2']} (p {prim['p']:.3f}); T1 {prim['T1']}; T1' {prim['T1p']}",
          (not prim["T2"]) and ((not prim["T1p"]) or (not prim["T1"])))


def jk(d):
    if isinstance(d, dict):
        return {("|".join(map(str, k)) if isinstance(k, tuple) else str(k)): jk(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)):
        return [jk(x) for x in d]
    if isinstance(d, (np.floating, np.integer)):
        return d.item()
    return d


R.num("grid_logR", GRID.tolist())
R.num("NEED", jk(NEED)); R.num("OBJNEED", jk(OBJNEED)); R.num("NAMES", NAMES)
R.num("R_switch_analytic_log", jk(RSW)); R.num("R_LCDM_log", jk(RLCDM))
R.num("EST", jk({k: v for k, v in EST.items()})); R.num("RIND", jk(RIND))
R.num("TEST", jk(TEST)); R.num("TEST_yield_bracket", jk(TB)); R.num("C4", dict(synthetic=jk(t4), shuffled=jk(t5)))
R.num("RESCORE", jk({k: v for k, v in RES.items()})); R.num("MOVES", MOVES); R.num("headline", headline)
if MUTATE:
    R.num("SHUF", jk(SHUF))
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
