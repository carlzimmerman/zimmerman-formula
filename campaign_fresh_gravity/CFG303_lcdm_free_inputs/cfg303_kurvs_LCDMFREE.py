#!/usr/bin/env python3
"""CFG303 R4 -- KURVS with the measured outer markers (CFG189) and the LCDM-free analytic pressure models (CFG141's P0-P3) in place of
Kretschmer+2021's VELA-calibrated alpha(x) (P4, LCDM-MODEL).  CFG189's own machinery (marker loader, Sample.pred, pooled, DS, anchor, klass)
is exec'd from its committed source; only the pressure coefficient is replaced.
Frozen criteria: FROZEN_CRITERIA.md (52976ec22) + ADDENDUM_1 + ADDENDUM_2 (section A2.1), written before any replaced cell was computed.
kappa = 1/2 FITTED.  The cold mass is still required; no dark-matter particle is added.  No sentence here says the data favour a law.
Run:  python3 campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_kurvs_LCDMFREE.py
Outputs: cfg303_kurvs_LCDMFREE.out, cfg303_kurvs_LCDMFREE_results.json (this lane only).
"""
import os, sys, io, json, math, copy, contextlib, time, hashlib
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

T0 = time.time()
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
os.environ.pop("MUTATE", None)
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


P(__doc__.split("Run:")[0].strip())
for f in ("FROZEN_CRITERIA.md", "FROZEN_CRITERIA_ADDENDUM_1.md", "FROZEN_CRITERIA_ADDENDUM_2.md"):
    P(f"  {f}: sha256 {sha(os.path.join(LANE, f))}")
F189 = os.path.join(CFG, "CFG189_kurvs_measured_markers", "cfg189_measured_markers.py")
src = open(F189).read()
STOP = "# ================================================================== per disc"
assert src.count(STOP) == 1
ns = {"__file__": F189, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(STOP)], "cfg189[upto per disc]", "exec"), ns)
P(f"  CFG189 (sha {sha(F189)[:12]}) exec'd up to its per-disc block")
J189 = json.load(open(os.path.join(CFG, "CFG189_kurvs_measured_markers", "cfg189_measured_markers_results.json")))["numbers"]["results"]
J141 = json.load(open(os.path.join(CFG, "CFG141_kurvs_measured_sigma_results.json")))["numbers"]
build, Sample, pooled, DS, klass, terms = ns["build"], ns["Sample"], ns["pooled"], ns["DS"], ns["klass"], ns["terms"]
SP, KU2, LAWN, alpha_k21 = ns["SP"], ns["KU2"], ns["LAWN"], ns["alpha_k21"]
gbar, gpred, slope, A0, LAWS, FOOT = ns["gbar"], ns["gpred"], ns["slope"], ns["A0"], ns["LAWS"], ns["FOOT"]
KU_tab = {o["name"]: o for o in ns["g141"]["g140"]["KU"]}          # CFG140's objects: sig = the tabulated sigma0, esig = its error


def alpha_arr(objs, mode):
    """the pressure coefficient per object, so that V_c^2 = V^2 + alpha * sig^2 in CFG189's DS (with sig possibly replaced for P1)."""
    R = np.array([o["R"] for o in objs]); Rd = np.array([o["Rd"] for o in objs])
    if mode == "K21":
        return np.array([alpha_k21(o["R"] / (1.68 * o["Rd"]) - 1.0) for o in objs])
    if mode == "P0":
        return np.zeros(len(objs))
    if mode in ("P1", "P2"):
        return 2.0 * R / Rd
    if mode == "P3":
        sg = np.array([o["sig"] for o in objs]); gr = np.array([o.get("grad", 0.0) for o in objs])
        return np.maximum(0.0, R / Rd - R * gr / np.where(sg > 0, sg ** 2, np.inf))
    raise ValueError(mode)


def T_for(objs, mode):
    T = terms(objs)
    T["ak"] = alpha_arr(objs, mode)
    if mode == "P1":
        T["sg"] = np.array([KU_tab[o["name"]]["sig"] if o["name"] in KU_tab else o["sig"] for o in objs])
        T["es"] = np.array([KU_tab[o["name"]]["esig"] if o["name"] in KU_tab else o["esig"] for o in objs])
    return T


TS_by = {m: T_for(SP, m) for m in ("K21", "P0", "P1", "P2", "P3")}
for m in ("P1",):                                        # SPARC has no tabulated sigma0: P1 uses the declared 10 km/s (as CFG140/141's anchor)
    TS_by[m]["sg"] = np.array([o["sig"] for o in SP]); TS_by[m]["es"] = np.array([o["esig"] for o in SP])
_an = {}


def anchor(mode, law):
    if (mode, law) not in _an:
        gb = np.array([gbar(o, 0.67, 0.0, True) for o in SP]); a = np.array([A0[FOOT] * LAWS[law](o["z"]) for o in SP])
        gp = np.array([gpred(g, aa) for g, aa in zip(gb, a)]); sl = np.array([slope(g, aa) for g, aa in zip(gb, a)])
        _an[(mode, law)] = pooled(*DS(TS_by[mode], 1.0, gp, sl))
    return _an[(mode, law)]


def delta(S, T, mode, mu, law):
    gp, sl = S.pred(mu, law)
    k, ek = pooled(*DS(T, 1.0, gp, sl))
    an, ea = anchor(mode, law)
    return k - an, math.hypot(ek, ea)


def cell(objs, mode, mu=0.67):
    S = Sample(objs); T = T_for(objs, mode)
    c = {law: delta(S, T, mode, mu, law) for law in LAWN}
    return c, klass(c["flat"][0] / c["flat"][1], c["rival"][0] / c["rival"][1]), S, T


GRID = np.exp(np.linspace(math.log(0.01), math.log(30.0), 36))


def break_even(objs, mode, law):
    S = Sample(objs); T = T_for(objs, mode)
    fn = lambda mu: delta(S, T, mode, mu, law)[0]
    vals = [fn(m) for m in GRID]
    for lo_, hi_, flo, fhi in zip(GRID[:-1], GRID[1:], vals[:-1], vals[1:]):
        if flo * fhi < 0:
            return float(brentq(fn, lo_, hi_, xtol=1e-6, rtol=1e-6))
    return float("nan")


# ================================================================== controls
P("\nCONTROLS")
objs, info = build("primary")
ck = cell(objs, "K21")[0]
dK = max(abs(ck[l][0] - J189["primary"]["cell"]["1.00"][l][0]) for l in LAWN)
c0 = cell(objs, "P0")[0]
d0 = max(abs(c0[l][0] - J189["primary"]["cell"]["0.00"][l][0]) for l in LAWN)
check("C-i(a) the replacement path with alpha = K21 (and alpha = 0) reproduces CFG189's committed primary cells at s = 1 and s = 0", f"max |diff| {dK:.1e} (s 1), {d0:.1e} (s 0)",
      dK <= 1e-9 and d0 <= 1e-9)
S189 = Sample(objs)
ck2 = {l: S189.delta(0.67, 1.0, l) for l in LAWN}
dc = max(abs(ck2[l][0] - J189["primary"]["cell"]["1.00"][l][0]) for l in LAWN)
check("C-ii CFG189's exec'd pipeline (Sample.delta) reproduces its committed decision cell", f"max |diff| {dc:.1e}", dc <= 1e-9)
cm2 = cell(KU2, "P2")[0]
ref = J141["P2"]["0.67|0.0|canonical"]
dP2 = max(abs(cm2["flat"][0] - ref["df"]), abs(cm2["rival"][0] - ref["dh"]))
check("C-i(b) the P2 mapping with CFG141's model-velocity objects reproduces CFG141's committed P2 cell (mu 0.67, delta 0, canonical; 1e-4)",
      f"flat {cm2['flat'][0]:+.5f} vs {ref['df']:+.5f}; rival {cm2['rival'][0]:+.5f} vs {ref['dh']:+.5f}", dP2 <= 1e-4)
cm3 = cell(KU2, "P3")[0]
ref3 = J141["P3"]["0.67|0.0|canonical"]
dP3 = max(abs(cm3["flat"][0] - ref3["df"]), abs(cm3["rival"][0] - ref3["dh"]))
check("C-i(c) (reported) the P3 mapping with CFG141's model-velocity objects against CFG141's committed P3 cell (errors propagated as CFG189's DS, not CFG141's dlog3)",
      f"flat {cm3['flat'][0]:+.5f} vs {ref3['df']:+.5f}; rival {cm3['rival'][0]:+.5f} vs {ref3['dh']:+.5f}; max |diff| {dP3:.1e}", True)

# ================================================================== the LCDM-free cells
P("\nTHE DECISION CELL (mu 0.67, canonical, anchor-corrected) WITH THE MEASURED MARKERS, BY PRESSURE MODEL  [Delta' +- sigma (z)]")
RES = {}
for variant in ("primary", "V-a", "V-b", "V-c", "V-d", "BS"):
    ob, inf = build(variant)
    RES[variant] = {}
    for mode in ("P0", "P1", "P2", "P3", "K21"):
        c, kl, _, _ = cell(ob, mode)
        RES[variant][mode] = dict(cell={l: list(c[l]) for l in LAWN}, cls=kl)
    line = "; ".join(f"{m}{' (LCDM-MODEL)' if m == 'K21' else ''}: flat {RES[variant][m]['cell']['flat'][0]:+.3f} ({RES[variant][m]['cell']['flat'][0] / RES[variant][m]['cell']['flat'][1]:+.1f}), "
                     f"rival {RES[variant][m]['cell']['rival'][0]:+.3f} ({RES[variant][m]['cell']['rival'][0] / RES[variant][m]['cell']['rival'][1]:+.1f}), "
                     f"T {RES[variant][m]['cell']['T'][0]:+.3f} -> {RES[variant][m]['cls']}" for m in ("P2", "P3", "P1", "P0", "K21"))
    P(f"  {variant:7s}: {line}")
model_cells = {m: dict(cell={l: list(v) for l, v in cell(KU2, m)[0].items()}, cls=cell(KU2, m)[1]) for m in ("P0", "P1", "P2", "P3", "K21")}
P("  model V (Table B1 col 3; MODEL-OTHER), for reference: " + "; ".join(f"{m}: flat {model_cells[m]['cell']['flat'][0]:+.3f}, rival {model_cells[m]['cell']['rival'][0]:+.3f} -> {model_cells[m]['cls']}"
                                                                      for m in ("P2", "P3", "P1", "P0", "K21")))
BE = {m: {l: break_even(objs, m, l) for l in LAWN} for m in ("P1", "P2", "P3")}
P("  break-even total gas mu (Delta' = 0), measured markers: " + "; ".join(f"{m}: " + ", ".join(f"{l} {BE[m][l]:.2f}" for l in LAWN) for m in BE))
cls_free = {v: {m: RES[v][m]["cls"] for m in ("P0", "P1", "P2", "P3")} for v in RES}
P("  classes over the 6 marker sets x 4 LCDM-free prescriptions: " + ", ".join(f"{k} {sum(1 for v in cls_free.values() for c in v.values() if c == k)}"
                                                                           for k in ("lean flat", "lean rival", "both", "neither")))

# ================================================================== MUTATE (C-iii)
P("\nC-iii MUTATE: measured V x 10^0.1")
okm = True
for mode in ("P2", "P3", "P1"):
    ob, _ = build("primary")
    T0_ = T_for(ob, mode)
    obm = copy.deepcopy(ob)
    for o in obm:
        o["V"] *= 10 ** 0.1; o["eV"] *= 10 ** 0.1
    T1_ = T_for(obm, mode)
    gp, sl = Sample(ob).pred(0.67, "flat")
    d0_, _ = DS(T0_, 1.0, gp, sl); d1_, _ = DS(T1_, 1.0, gp, sl)
    V2 = T0_["V"] ** 2; aS = T0_["ak"] * T0_["sg"] ** 2
    ind = np.log10((10 ** 0.2 * V2 + aS) / (V2 + aS))
    e_ind = float(np.max(np.abs((d1_ - d0_) - ind)))
    c0m = cell(ob, mode)[0]; c1m = cell(obm, mode)[0]
    up = all(c1m[l][0] > c0m[l][0] for l in LAWN)
    okm &= e_ind <= 1e-12 and up
    P(f"  {mode}: per-disc log g_obs shift vs independent formula max |err| {e_ind:.1e}; Delta' rises for every law: {up} "
      f"(flat {c0m['flat'][0]:+.3f} -> {c1m['flat'][0]:+.3f}, rival {c0m['rival'][0]:+.3f} -> {c1m['rival'][0]:+.3f}; class {cell(obm, mode)[1]})")
check("C-iii MUTATE: every disc's log g_obs moves by the independently computed amount and every law's Delta' rises (P1, P2, P3)", "see lines above", okm)

npass = sum(CHK)
P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")
json.dump(dict(cells=RES, model_cells=model_cells, break_even=BE, classes_free=cls_free, perdisc={str(k): v for k, v in info.items()},
               committed=dict(primary_K21=J189["primary"]["cell"]["1.00"], primary_P0=J189["primary"]["cell"]["0.00"], cfg141_P2=ref, cfg141_P3=ref3),
               checks=dict(passed=npass, n=len(CHK))), open(os.path.join(LANE, "cfg303_kurvs_LCDMFREE_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg303_kurvs_LCDMFREE.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)
