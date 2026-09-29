#!/usr/bin/env python3
"""CFG175 -- a third a0(z) law, a0 ~ t(z)/t0 (CFG174's accumulation reading), through the KURVS/KROSS pipeline under P0, P4 and CFG162's s-axis.

Frozen criteria: CFG175_FROZEN_CRITERIA.md (cc39c2055).  Data already seen by many lanes; the law was written with KURVS known (both disclosed).
  laws      flat a0; rival a0 E(z); T a0 t(z)/t0 (flat LCDM age on the pipeline's own background, Omega_m = 0.315).
  pipeline  CFG141's, exec'd read-only and unmutated; CFG160's P4 alpha verbatim; SPARC anchor at the same s under the same law.
  reported  decision cell, (s, mu) map, break-evens (1-sigma), the fit point s0 at mu = 0.67, T's two-epoch ratio -- for all three laws.
  rule      'gas-excluded' if the KURVS break-even's lower 1-sigma edge > 3.47 (or it under-predicts at mu = 30), applied to all three laws.
MUTATE=1: T := flat (rows must equal flat's, headline must change).  MUTATE=2: T := rival (rows must equal the rival's).
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour any model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG175_t_law_a0z.py   (MUTATE=1 or MUTATE=2 for the pinned controls)
"""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C

MODE = os.environ.get("MUTATE", "").strip()
assert MODE in ("", "1", "2")
TAG = "CFG175_t_law_a0z"
R = C.Report(TAG + (f"_MUTATE{MODE}" if MODE else ""), False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())

F141 = os.path.join(HERE, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
_saved = os.environ.pop("MUTATE", None)                         # the exec'd pipeline runs unmutated in every mode of this lane
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
finally:
    if _saved is not None:
        os.environ["MUTATE"] = _saved
KU2, SP, KR = g141["KU2"], g141["SP"], g141["g140"]["KR"]
A0, E, gbar, gpred, slope, KPC = g141["A0"], g141["E"], g141["gbar"], g141["gpred"], g141["slope"], g141["KPC"]
OM = g141["g140"]["OM"]
assert abs(E(1.5) - math.sqrt(OM * 2.5 ** 3 + 1 - OM)) < 1e-12 and abs(OM - 0.315) < 1e-12
LN10, FOOT = math.log(10), "canonical"


def tratio(z, om=OM):
    k = math.sqrt((1 - om) / om)
    return math.asinh(k * (1 + z) ** -1.5) / math.asinh(k)


LAWS = {"flat": lambda z: 1.0, "rival": E, "T": tratio}
if MODE == "1":
    LAWS["T"] = LAWS["flat"]
elif MODE == "2":
    LAWS["T"] = LAWS["rival"]
LAWN = ("flat", "rival", "T")


def alpha_k21(x):                                                # CFG160's, verbatim
    x = min(max(x, 0.0), 4.0)
    return -0.146 * x * x + 1.204 * x + 1.475


def pooled(d, s):                                                # CFG140's
    w = 1 / s ** 2
    m = float(np.sum(w * d) / np.sum(w)); e = float(1 / math.sqrt(np.sum(w)))
    chi = float(np.sum(w * (d - m) ** 2)); dof = max(len(d) - 1, 1)
    if chi / dof > 1:
        e *= math.sqrt(chi / dof)
    return m, e


def terms(objs):
    V = np.array([o["V"] for o in objs]); eV = np.array([o["eV"] for o in objs]); sg = np.array([o["sig"] for o in objs])
    es = np.array([o["esig"] for o in objs]); Rr = np.array([o["R"] for o in objs]); sm = np.array([o["sm"] for o in objs])
    inc = [math.radians(o["inc"]) if np.isfinite(o["inc"]) and o["inc"] > 1 else math.radians(60) for o in objs]
    ti = np.array([2 * o["V"] ** 2 * o["einc"] / math.tan(i) for o, i in zip(objs, inc)])
    ak = np.array([alpha_k21(o["R"] / (1.68 * o["Rd"]) - 1.0) for o in objs])
    return dict(V=V, eV=eV, sg=sg, es=es, R=Rr, sm=sm, ti=ti, ak=ak)


def DS(T, s, gp, sl):
    al = s * T["ak"]
    vc2 = T["V"] ** 2 + al * T["sg"] ** 2
    go = vc2 * 1e6 / (T["R"] * KPC)
    dlog = np.sqrt((2 * T["V"] * T["eV"]) ** 2 + (2 * al * T["sg"] * T["es"]) ** 2 + T["ti"] ** 2) / vc2 / LN10
    return np.log10(go / gp), np.hypot(dlog, sl * T["sm"])


TK, TR, TS = terms(KU2), terms(KR), terms(SP)
SAMP = {"KURVS": (KU2, TK), "KROSS": (KR, TR)}
S_LIST = (0.0, 1.00, 1.42, 1.62, 1.69, 3.00)
S_NAME = {0.0: "P0 none", 1.00: "P4 Kretschmer", 1.42: "Dalcanton&Stilp", 1.62: "P3 fixed height", 1.69: "Price n=1", 3.00: "P2 self-grav"}
MU_BR = (0.25, 0.67, 1.5, 4.0)
CEIL = 3.47
_pred, _anp = {}, {}


def pred(name, mu, law):
    key = (name, round(mu, 12), law)
    if key not in _pred:
        objs = SAMP[name][0] if name != "SPARC" else SP
        gb = np.array([gbar(o, 0.67, 0.0, True) if name == "SPARC" else gbar(o, mu, 0.0) for o in objs])
        a = np.array([A0[FOOT] * LAWS[law](o["z"]) for o in objs])
        _pred[key] = (np.array([gpred(g, aa) for g, aa in zip(gb, a)]), np.array([slope(g, aa) for g, aa in zip(gb, a)]))
    return _pred[key]


def anchor(s, law):
    gp, sl = pred("SPARC", 0.67, law)
    return pooled(*DS(TS, s, gp, sl))


def delta(name, mu, s, law):
    gp, sl = pred(name, mu, law)
    k, ek = pooled(*DS(SAMP[name][1], s, gp, sl))
    an, ea = anchor(s, law)
    return k - an, math.hypot(ek, ea)


GRID = np.exp(np.linspace(math.log(0.01), math.log(30.0), 36))


def root_mu(name, s, law, target):
    fn = lambda mu: (lambda d: d[0] - target * d[1])(delta(name, mu, s, law))
    vals = [fn(m) for m in GRID]
    for lo, hi, flo, fhi in zip(GRID[:-1], GRID[1:], vals[:-1], vals[1:]):
        if flo == 0:
            return float(lo)
        if flo * fhi < 0:
            return float(brentq(fn, lo, hi, xtol=1e-6, rtol=1e-6))
    return float("nan")


def breakeven(name, s, law):
    return root_mu(name, s, law, 0.0), root_mu(name, s, law, +1.0), root_mu(name, s, law, -1.0)   # (mu_be, mu_lo, mu_hi)


def status(name, s, law, be):
    if np.isfinite(be[0]):
        lo = be[1] if np.isfinite(be[1]) else 0.0                # a missing +sigma root lies below 0.01: open side
        return "gas-excluded" if lo > CEIL else "gas-allowed"
    if delta(name, 0.01, s, law)[0] < 0:
        return "over-predicts"
    return "gas-excluded" if delta(name, 30.0, s, law)[0] > 0 else "no break-even"


def s0(name, law, mu=0.67):
    fn = lambda s: delta(name, mu, s, law)[0]
    f0, f6 = fn(0.0), fn(6.0)
    if f0 > 0:
        return float("-inf")
    if f6 < 0:
        return float("inf")
    return float(brentq(fn, 0.0, 6.0, xtol=1e-6))


def fs(v):
    return "< 0" if v == float("-inf") else ("> 6" if v == float("inf") else f"{v:.3f}")


# ================================================================== controls
R.banner("C1 / C2 / C3  CONTROLS")
c1 = {z: math.log10(tratio(z, 0.3111)) for z in (0.85, 1.5, 2.5)}
check("C1 CONTROL: t(z)/t0 with CFG174's cosmology (Omega_m = 0.3111) reproduces its Q3 values -0.33/-0.51/-0.72 dex (0.01 dex)",
      "  ".join(f"z {z}: {v:+.4f}" for z, v in c1.items()) + "   | at the pipeline's Omega_m = 0.315: "
      + "  ".join(f"z {z}: {math.log10(tratio(z)):+.4f}" for z in (0.85, 1.5, 2.5)),
      all(abs(c1[z] - t) < 0.01 for z, t in ((0.85, -0.33), (1.5, -0.51), (2.5, -0.72))))
dcf, dch = delta("KURVS", 0.67, 1.0, "flat"), delta("KURVS", 0.67, 1.0, "rival")
j170 = json.load(open(os.path.join(HERE, "CFG170_two_epoch_gas_ratio_results.json")))["numbers"]
t170 = j170["table"]
bk = {(n, law): root_mu(n, 1.0, law, 0.0) for n in ("KURVS", "KROSS") for law in ("flat", "rival")}
ref = {("KURVS", "flat"): t170["1.00|flat"]["kurvs"][0], ("KURVS", "rival"): t170["1.00|rival"]["kurvs"][0],
       ("KROSS", "flat"): t170["1.00|flat"]["kross"][0], ("KROSS", "rival"): t170["1.00|rival"]["kross"][0]}
check("C2 CONTROL: flat and rival at the KURVS decision cell reproduce CFG160 (+0.1441 / -0.0060) and their s = 1 break-evens CFG170's (1e-3)",
      f"cell {dcf[0]:+.4f} / {dch[0]:+.4f};  break-evens " + ", ".join(f"{n} {law} {bk[(n, law)]:.4f} (CFG170 {ref[(n, law)]:.4f})" for n, law in bk),
      round(dcf[0], 4) == 0.1441 and round(dch[0], 4) == -0.0060 and all(abs(bk[k] - ref[k]) < 1e-3 for k in bk))
adiff = max(abs(anchor(s, "T")[0] - anchor(s, "flat")[0]) for s in S_LIST)
check("C3 CONTROL: T's SPARC anchor differs from flat's by < 0.01 dex at every placed s (the anchor sits at z ~ 0)", f"max |diff| = {adiff:.5f} dex",
      adiff < 0.01)

# ================================================================== power and the decision cell
R.banner("R0 POWER and THE KURVS DECISION CELL (mu = 0.67, delta = 0, canonical)")
dct = delta("KURVS", 0.67, 1.0, "T")
check("R0 (reported) POWER: Delta'_T - Delta'_flat at the decision cell against sigma", f"{dct[0] - dcf[0]:+.4f} dex vs sigma {dct[1]:.4f}  "
      f"({(dct[0] - dcf[0]) / dct[1]:+.2f} sigma)", True, load_bearing=False)
cell = {}
for s in (1.0, 0.0):
    for law in LAWN:
        d, e = delta("KURVS", 0.67, s, law)
        cell[f"{s:.2f}|{law}"] = dict(d=d, e=e, z=d / e)
    P(f"  s {s:.2f} ({S_NAME[s]:13s}): " + ";  ".join(f"{law} {cell[f'{s:.2f}|{law}']['d']:+.4f} +- {cell[f'{s:.2f}|{law}']['e']:.4f} "
                                                      f"(z {cell[f'{s:.2f}|{law}']['z']:+.2f})" for law in LAWN))
R.num("cell", cell)

# ================================================================== the map
R.banner("THE MAP: KURVS Delta' (z) per law over the gas bracket; KROSS at mu = 0.67")
mp = {}
for s in S_LIST:
    for mu in MU_BR:
        row = {law: delta("KURVS", mu, s, law) for law in LAWN}
        mp[f"KURVS|{s:.2f}|{mu}"] = {law: dict(d=v[0], e=v[1]) for law, v in row.items()}
        P(f"  KURVS s {s:4.2f} mu {mu:4.2f}: " + ";  ".join(f"{law} {v[0]:+.3f} ({v[0] / v[1]:+.1f})" for law, v in row.items()))
    row = {law: delta("KROSS", 0.67, s, law) for law in LAWN}
    mp[f"KROSS|{s:.2f}|0.67"] = {law: dict(d=v[0], e=v[1]) for law, v in row.items()}
    P(f"  KROSS s {s:4.2f} mu 0.67: " + ";  ".join(f"{law} {v[0]:+.3f} ({v[0] / v[1]:+.1f})" for law, v in row.items()))
R.num("map", mp)

# ================================================================== break-evens, status, two-epoch ratio
R.banner("BREAK-EVENS mu_be [1-sigma] and STATUS (gas ceiling 3.47)  |  T's two-epoch ratio vs CFG170's brackets")
be, st = {}, {}
rin, rlit = j170["R_obs"]["in_repo_2sigma"], j170["R_obs"]["literature_bracket"]
for s in S_LIST:
    for law in LAWN:
        for n in ("KURVS", "KROSS"):
            be[(n, s, law)] = breakeven(n, s, law)
        st[(s, law)] = status("KURVS", s, law, be[("KURVS", s, law)])
        k, r = be[("KURVS", s, law)], be[("KROSS", s, law)]
        P(f"  s {s:4.2f} ({S_NAME[s]:15s}) {law:5s}: KURVS {k[0]:.3f} [{k[1]:.3f}, {k[2]:.3f}] -> {st[(s, law)]:14s} KROSS {r[0]:.3f} [{r[1]:.3f}, {r[2]:.3f}]"
          + (f";  R_T = {k[0] / r[0]:.3f} (in-repo [{rin[0]:.2f}, {rin[1]:.2f}], literature [{rlit[0]:.2f}, {rlit[1]:.2f}])"
             if law == "T" and np.isfinite(k[0]) and np.isfinite(r[0]) and r[0] > 0 else ""))
R.num("breakevens", {f"{n}|{s:.2f}|{law}": list(v) for (n, s, law), v in be.items()})
R.num("status", {f"{s:.2f}|{law}": v for (s, law), v in st.items()})

# ================================================================== the fit point on the s-axis
R.banner("THE FIT POINT s0 (Delta'_law(s) = 0 at mu = 0.67), s in [0, 6]")
sp = {}
for n in ("KURVS", "KROSS"):
    sp[n] = {law: s0(n, law) for law in LAWN}
    P(f"  {n}: " + ";  ".join(f"{law} s0 = {fs(v)}" for law, v in sp[n].items()))
R.num("s0", {n: {law: (None if not np.isfinite(v) else v) for law, v in d.items()} for n, d in sp.items()})

# ================================================================== headline
PUB = (1.00, 1.42, 1.62, 1.69, 3.00)
excl_all = all(st[(s, "T")] == "gas-excluded" for s in PUB)
if excl_all:
    summary = "T is gas-excluded under every published prescription" + (
        " and gas-allowed only without pressure support" if st[(0.0, "T")] == "gas-allowed" else "")
else:
    summary = "T's status by prescription: " + ", ".join(f"s {s:.2f} {st[(s, 'T')]}" for s in (0.0,) + PUB)
strong = excl_all and cell["1.00|T"]["z"] > 3
summary += ("; STRONGLY DISFAVOURED by the declared rule (z at the decision cell %+.1f)" % cell["1.00|T"]["z"]) if strong else \
           ("; not 'strongly disfavoured' by the declared rule (z at the decision cell %+.1f)" % cell["1.00|T"]["z"])
R.banner("HEADLINE")
P("  status matrix (KURVS; flat and the rival printed alongside, the rule is not aimed at T):")
for s in S_LIST:
    P(f"    s {s:4.2f} ({S_NAME[s]:15s}): " + ";  ".join(f"{law} {st[(s, law)]}" for law in LAWN))
if MODE == "1":
    same = max(abs(mp[k]["T"]["d"] - mp[k]["flat"]["d"]) for k in mp)
    main = os.path.join(HERE, TAG + "_results.json")
    msum = json.load(open(main))["numbers"]["summary"] if os.path.exists(main) else None
    check("MUTATE=1 [pinned control]: T := flat -> T's rows equal flat's (1e-9) and the headline changes from the main run's",
          f"max |T - flat| = {same:.2e}; summary now: {summary} | main: {msum}", same < 1e-9 and msum is not None and msum != summary)
elif MODE == "2":
    same = max(abs(mp[k]["T"]["d"] - mp[k]["rival"]["d"]) for k in mp)
    check("MUTATE=2 [pinned control]: T := rival -> T's rows equal the rival's (1e-9)", f"max |T - rival| = {same:.2e}", same < 1e-9)
else:
    check("H1 [HEADLINE, reported] the declared summary", summary, True, load_bearing=False)
R.num("summary", summary)
P(f"\n    SUMMARY (declared): {summary}")
nf = R.write()
raise SystemExit(1 if nf else 0)
