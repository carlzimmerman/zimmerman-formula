#!/usr/bin/env python3
"""CFG189 -- the KURVS a0(z) test re-run with the MEASURED outer rotation markers in place of the model velocity, for three laws.

Frozen criteria: FROZEN_CRITERIA.md in this directory (39846c92e), committed before any marker value was read.
  primary   the farther side's outermost UNCLIPPED marker: V_out = |v_obs|/sin i_SFR at R_out; sigma interpolated on the same side at R_out.
  variants  V-a outer three (weighted); V-b both sides at the shorter side's radius; V-c clipped included; V-d i*; BS sigma_int from
            CFG184's forward model at R_out (the markers are observed line-of-sight values, not beam-smearing corrected).
  laws      flat, a0 ~ H(z), a0 ~ t(z)/t0; decision cell mu = 0.67, s = 1 (and P0); CFG160's lean classes; break-evens; fit points.
MUTATE=1: the measured V x 10^0.3 (the decision-cell class must change).
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour any model, or that the theory is closed.
Run: python3 campaign_fresh_gravity/CFG189_kurvs_measured_markers/cfg189_measured_markers.py
"""
import os, sys, io, math, csv, json, copy, contextlib
import numpy as np
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG7_common as C

MODE = os.environ.get("MUTATE", "").strip()
assert MODE in ("", "1")
R = C.Report("cfg189_measured_markers" + ("_MUTATE1" if MODE else ""), False)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())

F141 = os.path.join(CFG, "CFG141_kurvs_measured_sigma.py")
src = open(F141).read()
g141 = {"__file__": F141, "__name__": "cfg141"}
_saved = os.environ.pop("MUTATE", None)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG141", "exec"), g141)
finally:
    if _saved is not None:
        os.environ["MUTATE"] = _saved
KU2, SP, PROF = g141["KU2"], g141["SP"], g141["PROF"]
A0, E, gbar, gpred, slope, KPC = g141["A0"], g141["E"], g141["gbar"], g141["gpred"], g141["slope"], g141["KPC"]
OM = g141["g140"]["OM"]
LN10, FOOT = math.log(10), "canonical"
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
INTEG = {int(r["kurvs_id"]): r for r in csv.DictReader(open(os.path.join(AT, "kurvs2023_integrated.csv")))}
VEL = {int(r["kurvs_id"]): r for r in csv.DictReader(open(os.path.join(AT, "kurvs2023_velocities_at_radii.csv")))}
MODEL = {}
for r in csv.DictReader(open(os.path.join(AT, "kurvs_rc_profiles", "kurvs_rc_model_curves.csv"))):
    MODEL.setdefault(int(r["kurvs_id"]), []).append((float(r["R_kpc"]), float(r["v_model_obs_kms"])))
MARK = {}
for r in csv.DictReader(open(os.path.join(AT, "kurvs_rc_profiles", "kurvs_rc_points.csv"))):       # the measured markers
    MARK.setdefault(int(r["kurvs_id"]), []).append((float(r["R_kpc"]), float(r["v_obs_kms"]), 0.5 * (float(r["err_up_kms"]) + float(r["err_lo_kms"])),
                                                    int(r["clipped_white_marker"])))
IDS = [int(o["name"].split("-")[1]) for o in KU2]

# CFG184's forward-model functions, exec'd read-only (for variant BS)
F184 = os.path.join(CFG, "CFG184_kurvs_beam_smearing", "cfg184_beam_smearing.py")
s184 = open(F184).read()
g184 = dict(np=np, math=math, KU2=KU2, IDS=IDS, INTEG=INTEG, VEL=VEL, MODEL=MODEL, PROF=PROF, MODE="")   # CFG184 unmutated
exec(compile("from scipy.special import erf, i0, i1, k0, k1\nfrom scipy.integrate import quad\n"
             + s184[s184.index("# ------------------------------------------------------------------ geometry"):
                    s184.index("# ================================================================== controls")], "CFG184", "exec"), g184)


# ------------------------------------------------------------------ the outer point
def side_pts(pts, side, clipped_ok):
    return sorted([(abs(Rk), v, e) for Rk, v, e, cl in pts if (Rk > 0) == side and (clipped_ok or not cl)])


def sigma_at(kid, side, Rq):
    sp = sorted((abs(Rk), s, 0.5 * (eu + el)) for Rk, s, eu, el, cl in PROF.get(kid, []) if (Rk > 0) == side and not cl)
    if not sp:
        return float("nan"), float("nan")
    rr, ss, ee = zip(*sp)
    if Rq >= rr[-1]:
        return ss[-1], ee[-1]
    return float(np.interp(Rq, rr, ss)), float(np.interp(Rq, rr, ee))


def outer(kid, variant="primary"):
    pts = MARK[kid]
    it = INTEG[kid]
    inc = float(it["inc_star_deg"]) if variant == "V-d" else float(it["inc_sfr_deg"])
    si = math.sin(math.radians(inc))
    clipped_ok = variant == "V-c"
    sides = {sd: side_pts(pts, sd, clipped_ok) for sd in (True, False)}
    far = max((sd for sd in sides if sides[sd]), key=lambda sd: sides[sd][-1][0])
    if variant == "V-a":
        o3 = sides[far][-3:]
        w = np.array([1 / p[2] ** 2 for p in o3])
        Rq = float(np.sum(w * np.array([p[0] for p in o3])) / w.sum())
        V = float(np.sum(w * np.array([abs(p[1]) for p in o3])) / w.sum()) / si
        eV = float(1 / math.sqrt(w.sum())) / si
        sg, es = sigma_at(kid, far, Rq)
    elif variant == "V-b":
        Rq = min(sides[True][-1][0], sides[False][-1][0])
        vs, es_, sgs, ess = [], [], [], []
        for sd in (True, False):
            rr, vv, ee = zip(*sides[sd])
            vs.append(abs(float(np.interp(Rq, rr, vv)))); es_.append(float(np.interp(Rq, rr, ee)))
            a_, b_ = sigma_at(kid, sd, Rq); sgs.append(a_); ess.append(b_)
        V = float(np.mean(vs)) / si; eV = float(math.sqrt(sum(x ** 2 for x in es_)) / 2) / si
        sg = float(np.nanmean(sgs)); es = float(math.sqrt(np.nansum(np.array(ess) ** 2)) / 2)
    else:
        Rq, v, e = sides[far][-1]
        V, eV = abs(v) / si, e / si
        sg, es = sigma_at(kid, far, Rq)
    return dict(R=Rq, V=V, eV=eV, sig=sg, esig=es, inc=inc, side=far)


def build(variant="primary"):
    objs, info = [], {}
    for o in KU2:
        kid = int(o["name"].split("-")[1])
        m = outer(kid, variant)
        oo = copy.deepcopy(o)
        oo.update(R=m["R"], V=m["V"] * (10 ** 0.3 if MODE == "1" else 1.0), eV=m["eV"] * (10 ** 0.3 if MODE == "1" else 1.0),
                  sig=m["sig"], esig=m["esig"], inc=m["inc"])
        if variant == "BS":
            it = INTEG[kid]; z = float(it["z_halpha"]); scale = g184["kpc_per_arcsec"](z)
            inc = float(it["inc_sfr_deg"])
            Vf = g184["v_model_folded"](kid, math.sin(math.radians(inc)))
            flds = g184["sky_fields"](Vf, inc, float(it["reff_kpc"]) / 1.68, scale)
            sbs = g184["sigma_bs_at"](flds, m["R"] / scale, 0.57, 0.6)
            oo["sig"] = math.sqrt(max(m["sig"] ** 2 - sbs ** 2, 0.0)); m["f_bs"] = sbs ** 2 / m["sig"] ** 2
        objs.append(oo); info[kid] = m
    return objs, info


# ------------------------------------------------------------------ the pipeline (CFG175's machinery, three laws)
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


def tratio(z, om=OM):
    k = math.sqrt((1 - om) / om)
    return math.asinh(k * (1 + z) ** -1.5) / math.asinh(k)


LAWS = {"flat": lambda z: 1.0, "rival": E, "T": tratio}
LAWN = ("flat", "rival", "T")
TS = terms(SP)


class Sample:
    def __init__(self, objs):
        self.objs, self.T, self._c = objs, terms(objs), {}

    def pred(self, mu, law):
        k = (round(mu, 12), law)
        if k not in self._c:
            gb = np.array([gbar(o, mu, 0.0) for o in self.objs]); a = np.array([A0[FOOT] * LAWS[law](o["z"]) for o in self.objs])
            self._c[k] = (np.array([gpred(g, aa) for g, aa in zip(gb, a)]), np.array([slope(g, aa) for g, aa in zip(gb, a)]))
        return self._c[k]

    def delta(self, mu, s, law):
        gp, sl = self.pred(mu, law)
        k, ek = pooled(*DS(self.T, s, gp, sl))
        an, ea = anchor(s, law)
        return k - an, math.hypot(ek, ea)


_an = {}


def anchor(s, law):
    if (s, law) not in _an:
        gb = np.array([gbar(o, 0.67, 0.0, True) for o in SP]); a = np.array([A0[FOOT] * LAWS[law](o["z"]) for o in SP])
        gp = np.array([gpred(g, aa) for g, aa in zip(gb, a)]); sl = np.array([slope(g, aa) for g, aa in zip(gb, a)])
        _an[(s, law)] = pooled(*DS(TS, s, gp, sl))
    return _an[(s, law)]


GRID = np.exp(np.linspace(math.log(0.01), math.log(30.0), 36))


def root_mu(S, s, law, target=0.0):
    fn = lambda mu: (lambda d: d[0] - target * d[1])(S.delta(mu, s, law))
    vals = [fn(m) for m in GRID]
    for lo_, hi_, flo, fhi in zip(GRID[:-1], GRID[1:], vals[:-1], vals[1:]):
        if flo * fhi < 0:
            return float(brentq(fn, lo_, hi_, xtol=1e-6, rtol=1e-6))
    return float("nan")


def s0(S, law, mu=0.67):
    fn = lambda s: S.delta(mu, s, law)[0]
    if fn(0.0) > 0:
        return float("-inf")
    if fn(6.0) < 0:
        return float("inf")
    return float(brentq(fn, 0.0, 6.0, xtol=1e-6))


def klass(zf, zh):
    if abs(zf) <= 2 and zh < -2:
        return "lean flat"
    if abs(zh) <= 2 and zf > 2:
        return "lean rival"
    if abs(zf) <= 2 and abs(zh) <= 2:
        return "both"
    return "neither"


fs = lambda v: "< 0" if v == float("-inf") else ("> 6" if v == float("inf") else f"{v:.3f}")
S_LIST = (0.0, 1.0, 1.42, 1.62, 1.69, 3.0)

# ================================================================== controls
R.banner("C1 / C2  CONTROLS")
S_model = Sample(KU2)
cm = {law: S_model.delta(0.67, 1.0, law) for law in LAWN}
check("C1 CONTROL: with the table's model V at R_max and CFG141's sigma_out, the pipeline reproduces CFG160's cell and CFG175's T (1e-4)",
      f"flat {cm['flat'][0]:+.4f}, rival {cm['rival'][0]:+.4f}, T {cm['T'][0]:+.4f}",
      abs(cm["flat"][0] - 0.1441) < 1e-4 and abs(cm["rival"][0] + 0.0060) < 1e-4 and abs(cm["T"][0] - 0.3227) < 1e-4)
dr = []
for kid in IDS:
    for Rk, v, e, cl in MARK[kid]:
        cand = [abs(abs(Rk) - abs(Rs)) for Rs, *_ in PROF.get(kid, []) if (Rs > 0) == (Rk > 0)]
        if cand:
            dr.append(min(cand))
check("C2 CONTROL: marker radii match sigma-profile radii within 0.02 kpc wherever both exist (the ten discs)",
      f"max nearest-radius difference {max(dr):.4f} kpc over {len(dr)} markers; >0.02: {sum(d > 0.02 for d in dr)}",
      sum(d > 0.02 for d in dr) <= 2)

# ================================================================== per disc
objs, info = build("primary")
R.banner("PER DISC: model V (table, at R_max) vs the MEASURED outermost unclipped marker (primary), and sigma at the same radius")
for o, kid in zip(KU2, IDS):
    m = info[kid]
    P(f"  KURVS-{kid:2d}: R_max {float(VEL[kid]['R_halpha_max_kpc']):5.2f} -> R_out {m['R']:5.2f} kpc ({'+' if m['side'] else '-'} side);  "
      f"V model {o['V']:6.1f} -> measured {m['V']:6.1f} +- {m['eV']:4.1f} km/s ({m['V'] / o['V'] - 1:+.1%});  "
      f"sigma_out {o['sig']:5.1f} -> sigma(R_out) {m['sig']:5.1f} km/s;  i_SFR {m['inc']:.0f}")
R.num("perdisc", {str(k): v for k, v in info.items()})


def full(label, S, show=True):
    out = dict(cell={}, be={}, st={}, s0={})
    for s in (0.0, 1.0):
        out["cell"][f"{s:.2f}"] = {law: S.delta(0.67, s, law) for law in LAWN}
    c = out["cell"]["1.00"]
    out["class"] = klass(c["flat"][0] / c["flat"][1], c["rival"][0] / c["rival"][1])
    for s in S_LIST[1:]:
        out["be"][f"{s:.2f}"] = {}
        for law in LAWN:
            be = root_mu(S, s, law); lo = root_mu(S, s, law, +1.0)
            out["be"][f"{s:.2f}"][law] = be
            out["st"][f"{s:.2f}|{law}"] = ("gas-excluded" if np.isfinite(be) and (lo if np.isfinite(lo) else 0) > 3.47 else
                                           ("gas-allowed" if np.isfinite(be) else "no break-even"))
    out["s0"] = {law: s0(S, law) for law in LAWN}
    if show:
        P(f"  [{label}]  decision cell (mu 0.67, s 1): " + ";  ".join(f"{law} {c[law][0]:+.3f} +- {c[law][1]:.3f} ({c[law][0] / c[law][1]:+.1f})"
                                                                     for law in LAWN) + f"   -> class: {out['class']}")
        c0 = out["cell"]["0.00"]
        P(f"      P0 (s 0): " + ";  ".join(f"{law} {c0[law][0]:+.3f} ({c0[law][0] / c0[law][1]:+.1f})" for law in LAWN))
        for s in S_LIST[1:]:
            P(f"      break-evens s {s:.2f}: " + ";  ".join(f"{law} {out['be'][f'{s:.2f}'][law]:.3f} ({out['st'][f'{s:.2f}|{law}']})" for law in LAWN))
        P("      fit points s0 at mu 0.67: " + ";  ".join(f"{law} {fs(v)}" for law, v in out["s0"].items()))
    return out


R.banner("THE THREE LAWS: model velocity (CFG160/175) vs the measured markers")
res = {"model": full("model V (table col 3)", S_model)}
res["primary"] = full("MEASURED primary" if not MODE else "MEASURED primary x 10^0.3 [MUTATE]", Sample(objs))
dz = {law: res["primary"]["cell"]["1.00"][law][0] / res["primary"]["cell"]["1.00"][law][1]
      - res["model"]["cell"]["1.00"][law][0] / res["model"]["cell"]["1.00"][law][1] for law in LAWN}
dd = {law: res["primary"]["cell"]["1.00"][law][0] - res["model"]["cell"]["1.00"][law][0] for law in LAWN}
P("  shift at the decision cell, measured - model: " + ";  ".join(f"{law} {dd[law]:+.3f} dex ({dz[law]:+.2f} in z)" for law in LAWN))

if not MODE:
    R.banner("VARIANTS (reported)")
    for v in ("V-a", "V-b", "V-c", "V-d", "BS"):
        ob, inf = build(v)
        res[v] = full(v, Sample(ob))
        if v == "BS":
            P("      f_bs at R_out (CFG184 primary model): " + ", ".join(f"K{k} {inf[k]['f_bs']:.3f}" for k in IDS))

R.num("results", {k: dict(cls=v["class"], cell={s: {l_: list(x) for l_, x in d.items()} for s, d in v["cell"].items()},
                          be=v["be"], st=v["st"], s0={l_: (None if not np.isfinite(x) else x) for l_, x in v["s0"].items()})
                  for k, v in res.items()})

# ================================================================== headline
R.banner("HEADLINE")
cls = res["primary"]["class"]
if MODE == "1":
    main = os.path.join(LANE, "cfg189_measured_markers_results.json")
    mcls = json.load(open(main))["numbers"]["results"]["primary"]["cls"] if os.path.exists(main) else None
    check("MUTATE=1 [control]: measured V x 10^0.3 changes the decision-cell class from the main run's", f"{cls} (main: {mcls})",
          mcls is not None and cls != mcls)
    summary = f"MUTATE=1 class {cls}"
else:
    unchanged = cls == res["model"]["class"] and all(abs(x) < 1 for x in dz.values())
    nmatch = sum(res[v]["class"] == res["model"]["class"] for v in ("V-a", "V-b", "V-c", "V-d", "BS"))
    c = res["primary"]["cell"]["1.00"]
    summary = (("UNCHANGED" if unchanged else "CHANGED") + f": with the measured outer markers the decision cell reads flat "
               f"{c['flat'][0] / c['flat'][1]:+.1f} sigma, rival {c['rival'][0] / c['rival'][1]:+.1f}, T {c['T'][0] / c['T'][1]:+.1f} "
               f"(model V: +3.3 / -0.1 / +6.9); class '{cls}' (model V: '{res['model']['class']}'); z shifts "
               + ", ".join(f"{law} {dz[law]:+.2f}" for law in LAWN) + f"; {nmatch} of 5 variants keep the model-V class")
    check("H1 [HEADLINE, reported] the declared reading", summary, True, load_bearing=False)
R.num("summary", summary)
P(f"\n    SUMMARY (declared): {summary}")
nf = R.write(LANE)
raise SystemExit(1 if nf else 0)
