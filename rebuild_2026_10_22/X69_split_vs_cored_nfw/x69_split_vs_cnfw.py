#!/usr/bin/env python3
"""X69_split_vs_cored_nfw: X43 (core Sigma = max(a0/(2 pi G), eta Sigma_coll), c_f = 4 EXTERNAL) with the halo shape replaced by
T1-A split Burkert or T1-B cored NFW, r_s = S r_c, S = max(1, Sigma_core/Sigma_M) (the external spec's own choice, ties the outer
halo to a0). Frozen criteria 0d708a4e49 (committed alone). Machinery read-only: X68 (99028a0bb8) up to its main loop (X30 shear
stack, groups, SPARC) and HO1 (91cc5c3bd4) up to its grade block (X-COP hydrostatic masses).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x69_split_vs_cnfw.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x69_split_vs_cnfw.py --mutate   -> S -> 2 S, _MUTATE outputs
"""
import os, sys, io, json, math, time, resource, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad

T0 = time.time()
MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ------------------------------------------------------------------ X68 namespace (read-only, up to its main loop)
X68SRC = os.path.join(REB, "X68_split_scale_halo", "x68_split_scale.py"); T = open(X68SRC).read()
code68 = T[:T.index("\nfor f in FEET:\n    SLOG.clear()")]
for old, new in (('MUTATE = "--mutate" in sys.argv', "MUTATE = False"), ('"x68_x30_machinery"', '"x69_x30_machinery"')):
    assert code68.count(old) == 1; code68 = code68.replace(old, new)
N8 = {"__file__": os.path.join(HERE, "x68_ro.py"), "__name__": "x68_ro"}; argv0 = sys.argv; sys.argv = [X68SRC]
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(code68, X68SRC, "exec"), N8)
sys.argv = argv0
L68 = buf.getvalue().splitlines()
P(f"X69_split_vs_cored_nfw  {'MUTATE run (S -> 2 S)' if MUTATE else 'normal run'}  [c_f EXTERNAL; S = Sigma_core/Sigma_M ties r_s to a0]")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian), core Sigma = max(a0/(2 pi G), eta Sigma_coll), eta 14.83 not refit; not theory closed")
P(f"X68 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]; its checks: " + "; ".join(l.strip() for l in L68 if l.startswith("K")))
FEET, SIG, SIG_PC, GE, MSUNE, HK = (N8[k] for k in ("FEET", "SIG", "SIG_PC", "GE", "MSUNE", "HK"))
burk_M = N8["halo_M"]; N8["MODE"]["split"] = False                           # burk_M is now exactly X43's Burkert call
k0x43 = [l for l in L68 if l.startswith("K0x43")]; k0a = bool(k0x43) and k0x43[0].endswith("PASS")
checks = [("K0x68", k0a)]

# ------------------------------------------------------------------ the two shapes (x = r/r_c, S = r_s/r_c)
def M_sb(r, rc, S, Sig):
    x = np.asarray(r, float) / rc
    return 4 * math.pi * Sig * rc ** 2 * S ** 2 / (S ** 2 + 1) * (np.log1p(x) + 0.5 * S ** 2 * np.log1p((x / S) ** 2) - S * np.arctan(x / S))
def M_cn(r, rc, S, Sig):
    x = np.asarray(r, float) / rc
    if abs(S - 1.0) < 1e-4:
        return 4 * math.pi * Sig * rc ** 2 * (np.log1p(x) + 2 / (1 + x) - 0.5 / (1 + x) ** 2 - 1.5)
    return 4 * math.pi * Sig * rc ** 2 * S ** 2 / (S - 1) ** 2 * (np.log1p(x) + (S ** 2 - 2 * S) * np.log1p(x / S) - S * (S - 1) * x / (x + S))
def rho_sb(r, rc, S, Sig): rs = S * rc; return Sig * rs ** 2 / ((r + rc) * (r * r + rs * rs))
def rho_cn(r, rc, S, Sig): rs = S * rc; return Sig * rs ** 2 / ((r + rc) * (r + rs) ** 2)
SHAPES = {"T1A_split_burkert": M_sb, "T1B_cored_nfw": M_cn}
SFAC = 2.0 if MUTATE else 1.0
CUR = {"shape": None}; LOG = {}
def solve_rc(Mf, Mtot, Rout, S, Sig):
    """Compact root (r_c below the mass peak), the same convention as X43's solve_r0; None if the peak is below Mtot."""
    lm = lambda l: math.log(float(Mf(Rout, math.exp(l), S, Sig)))
    lo, hi = math.log(Rout * 1e-7), math.log(Rout * 1e3)
    pk = minimize_scalar(lambda l: -lm(l), bounds=(lo, hi), method="bounded", options={"xatol": 1e-10}); lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot) or lm(lo) > math.log(Mtot): return None
    return math.exp(brentq(lambda l: lm(l) - math.log(Mtot), lo, lpk, xtol=1e-14))
def shape_M(Mtot, Rout, Sig, Msun_mass, rr, clip, cell, foot):
    burk = burk_M(Mtot, Rout, Sig, Msun_mass, rr, clip, cell, foot)
    if CUR["shape"] is None: return burk
    lg = LOG.setdefault(cell, dict(n=0, fallback=0, S=[])); lg["n"] += 1
    S = max(1.0, Sig / SIG[foot]) * SFAC; Mf = SHAPES[CUR["shape"]]
    if CUR["shape"] == "T1A_split_burkert" and S == 1.0: lg["S"].append(1.0); return burk
    rc = solve_rc(Mf, Mtot, Rout, S, Sig)
    if rc is None: lg["fallback"] += 1; lg["S"].append(float("nan")); return burk
    lg["S"].append(S); rq = np.minimum(rr, Rout) if clip else rr
    return Mf(rq, rc, S, Sig)
N8["halo_M"] = shape_M

# K1 closed forms vs quadrature; T1-A at S = 1 is Burkert
k1 = True; rc_, Sg_, R_ = 3.0857e19, SIG["canonical"], 20 * 3.0857e19
for nm, Mf, rf in (("T1A", M_sb, rho_sb), ("T1B", M_cn, rho_cn)):
    for S_ in (1.0, 3.0, 10.0):
        q_ = quad(lambda r: 4 * math.pi * r * r * rf(r, rc_, S_, Sg_), 0, R_, epsabs=0, epsrel=1e-12, limit=400)[0]
        d_ = float(Mf(R_, rc_, S_, Sg_)) / q_ - 1; k1 &= abs(d_) < 1e-6
        P(f"K1 {nm} S = {S_:g}: closed form vs quadrature {d_:+.1e}")
d_ = float(M_sb(R_, rc_, 1.0, Sg_)) / (math.pi * Sg_ * rc_ ** 2 * float(N8["B"](R_ / rc_))) - 1; k1 &= abs(d_) < 1e-10
d2_ = float(M_cn(R_, rc_, 1.0 + 2e-4, Sg_)) / float(M_cn(R_, rc_, 1.0, Sg_)) - 1
P(f"K1 T1A at S = 1 vs X43 Burkert {d_:+.1e}; T1B S = 1+2e-4 vs S = 1 branch {d2_:+.1e} (continuity, O(1e-4) expected)")
checks.append(("K1", k1 and abs(d2_) < 1e-3))
k2 = True
for nm, Mf in SHAPES.items():
    Mt_, Rt_ = 1e14 * MSUNE, 2.0e22; Sg2 = 3 * SIG["canonical"]
    rc2 = solve_rc(Mf, Mt_, Rt_, 3.0, Sg2); d_ = float(Mf(Rt_, rc2, 3.0, Sg2)) / Mt_ - 1 if rc2 else float("inf"); k2 &= abs(d_) < 1e-8
    P(f"K2 {nm}: solved r_c {rc2 / 3.0857e19 if rc2 else float('nan'):.1f} kpc returns the mass {d_:+.1e}")
checks.append(("K2", k2))

# ------------------------------------------------------------------ HO1 namespace (read-only, up to its grade block): X-COP
HO1SRC = os.path.join(REB, "HO1_xcop_hotgas_heldout", "ho1_heldout.py")
src = open(HO1SRC).read(); src = src[:src.index("# ------------------------------------------------------------------ 6. grade per footing")]
for old, new in (("            Mh = math.pi * s * r0 ** 2 * float(Bk(min(rm, rta) / r0))",
                  "            Mh = HALOX(Mfair, rta, s, Mtot, min(rm, rta), foot)"),
                 ("            if x > 0.75: continue", "            if x > XMAX: continue"),
                 ("    d = np.array(d); xs = [x for c in XC for x, *_ in c[\"rows\"] if x <= 0.75]",
                  "    d = np.array(d); xs = [x for c in XC for x, *_ in c[\"rows\"] if x <= XMAX]"),
                 ("for x in (0.1, 0.2, 0.3, 0.5, 0.7)}", "for x in (0.1, 0.2, 0.3, 0.5, 0.7, 1.0) if x <= XMAX}")):
    assert src.count(old) == 1, old; src = src.replace(old, new)
os.environ.pop("HO1_MUTATE", None)
NH = {"__file__": os.path.join(HERE, "ho1_ro.py"), "__name__": "ho1_ro", "XMAX": 0.75}
NH["HALOX"] = lambda Mfair, rta, s, Mtot, r, foot: math.pi * s * NH["solve_r0"](Mfair, rta, s) ** 2 * float(NH["Bk"](r / NH["solve_r0"](Mfair, rta, s)))
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(src, HO1SRC, "exec"), NH)
try: os.remove(os.path.join(HERE, "x62_x43copy.py"))
except OSError: pass
P(f"HO1 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
xcop = NH["xcop_cl2"]
g0 = {f: xcop(f) for f in FEET}
k0b = all(abs(g0[f]["mean"] - (-0.002)) < 0.0015 and abs(g0[f]["rms"] - 0.126) < 0.0015 for f in FEET)
P(f"K0 HO1(a) reproduced with CL2's rule (mean -0.002, rms 0.126): " + ", ".join(f"[{f}] {g0[f]['mean']:+.4f}/{g0[f]['rms']:.4f}" for f in FEET) + f": {'PASS' if k0b else 'FAIL'}")
checks.append(("K0ho1", k0b))
NH["sig_core"] = lambda foot, tag, M: N8["sig_core"](foot, "A_c2b_refit", M)        # X43's rule (c_f = 4), not CL2's c_f(M)
def halox(Mfair, rta, s, Mtot, r, foot):
    return float(np.atleast_1d(shape_M(Mfair, rta, s, Mtot, np.array([r]), False, "xcop", foot))[0])
NH["HALOX"] = halox; NH["XMAX"] = 1.0

# ------------------------------------------------------------------ grade
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
MIDOUT = [k for k in ("G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3", "G-OUT-b",
                      "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3")]
INNER = ["G-IN-all", "G-IN-Mall"]
def run(shape, foot):
    CUR["shape"] = shape; LOG.clear()
    sp = {t: N8["sparc"](foot, t) for t in N8["BGS"]}
    for st in sp.values(): st["line"] = bool(N8["line"](st))
    gr = N8["grade_groups"](foot); gc = N8["grade_clusters"](foot); xc = xcop(foot)
    lg = {c: dict(n=v["n"], fallback=v["fallback"], S_median=float(np.nanmedian(v["S"])) if np.isfinite(v["S"]).any() else None,
                  S_p90=float(np.nanpercentile(v["S"], 90)) if np.isfinite(v["S"]).any() else None) for c, v in LOG.items()}
    CUR["shape"] = None
    return dict(sparc={t: dict(rms=v["rms"], line=v["line"]) for t, v in sp.items()}, groups=dict(Z=gr["Z"], mean=gr["mean"], verdict=gr["verdict"]),
                clusters=gc["cells"], cluster_fails=gc["fails"], xcop=dict(mean=xc["mean"], rms=xc["rms"], by_x=xc["by_x"], per_cluster=xc["per_cluster"]), S_log=lg)
RES = dict(frozen="0d708a4e49", mutate=MUTATE, Sigma_Msun_pc2=SIG_PC, footings={})
for f in FEET:
    P(f"\n=== [{f}] Sigma_M {SIG_PC[f]:.1f} Msun/pc^2")
    base = run(None, f)
    P(f"  X43 Burkert baseline: X-COP by_x " + ", ".join(f"{k}:{v:+.3f}" for k, v in base["xcop"]["by_x"].items()) + f"; mean {base['xcop']['mean']:+.3f} rms {base['xcop']['rms']:.3f}")
    xf = X43J["footings"][f]
    kb = max(abs(base["clusters"][hk][k]["pred"] - xf["clusters"]["cells"][hk][k]["pred"]) for hk in HK for k in base["clusters"][hk])
    P(f"  baseline cluster preds vs X43 committed: max |d| {kb:.1e}"); checks.append((f"K0base_{f}", kb < 1e-6))
    inner0 = float(np.mean([base["xcop"]["by_x"]["0.1"], base["xcop"]["by_x"]["0.2"]]))
    RES["footings"][f] = dict(baseline=base, shapes={})
    for sh in SHAPES:
        o = run(sh, f)
        cl = o["clusters"]; zok = lambda k: all(abs(cl[hk][k]["Z"]) <= 2 for hk in HK)
        sg = lambda k: "OVER" if cl["h0672"][k]["pred"] > cl["h0672"][k]["meas"] else "UNDER"
        x1 = o["xcop"]["by_x"]["1"]; inner = float(np.mean([o["xcop"]["by_x"]["0.1"], o["xcop"]["by_x"]["0.2"]]))
        G1 = abs(x1) <= 0.05
        G2 = [k for k in MIDOUT if not zok(k)]
        G3k = [k for k in INNER if not zok(k)]; G3x = abs(inner) <= abs(inner0) + 0.05
        nfb = sum(v["fallback"] for c, v in o["S_log"].items() if c in ("clusters", "xcop")); ntot = sum(v["n"] for c, v in o["S_log"].items() if c in ("clusters", "xcop"))
        fails = ([] if G1 else [f"G1 X-COP R500 {x1:+.3f} ({'halo light' if x1 > 0 else 'halo heavy'})"]) + [f"G2 {k} ({sg(k)})" for k in G2] \
              + [f"G3 {k} ({sg(k)})" for k in G3k] + ([] if G3x else [f"G3 X-COP inner {inner:+.3f} vs X43 {inner0:+.3f}"])
        v = "PASSES" if not fails else "FAILS"
        if ntot and nfb / ntot > 0.25: v = "UNDECIDED"; fails.append(f"{100 * nfb / ntot:.0f}% cluster/X-COP fallbacks")
        o.update(verdict=v, failing=fails, gates=dict(G1=G1, G2=not G2, G3=(not G3k) and G3x), xcop_R500=x1, xcop_inner=inner, xcop_inner_X43=inner0)
        RES["footings"][f]["shapes"][sh] = o
        P(f"  --- {sh}")
        P(f"    S: " + "; ".join(f"{c} median {v_['S_median'] if v_['S_median'] is None else round(v_['S_median'], 2)}, p90 {v_['S_p90'] if v_['S_p90'] is None else round(v_['S_p90'], 2)}, fallbacks {v_['fallback']}/{v_['n']}" for c, v_ in o["S_log"].items()))
        P(f"    SPARC (reported): " + ", ".join(f"[{t}] rms {s_['rms']:.4f} line {'PASS' if s_['line'] else 'FAIL'}" for t, s_ in o["sparc"].items())
          + f"; groups (reported) Z {o['groups']['Z']:+.2f} {o['groups']['verdict']} (X43 {xf['groups']['Z']:+.2f})")
        P(f"    X-COP by_x " + ", ".join(f"{k}:{v_:+.3f}" for k, v_ in o["xcop"]["by_x"].items()) + f"; 0.1-0.7 + 1.0 mean {o['xcop']['mean']:+.3f} rms {o['xcop']['rms']:.3f}")
        for k in cl["h0672"]:
            P(f"     {k:10s} meas {cl['h0672'][k]['meas']:+.3f}+-{cl['h0672'][k]['s']:.3f} pred {cl['h0672'][k]['pred']:+.3f} Z {cl['h0672'][k]['Z']:+.2f}"
              f"  (X43 {xf['clusters']['cells']['h0672'][k]['Z']:+.2f})" + ("" if zok(k) else "  FAIL"))
        P(f"    GATES G1 {'PASS' if G1 else 'FAIL'} | G2 {'PASS' if not G2 else 'FAIL'} | G3 {'PASS' if (not G3k) and G3x else 'FAIL'} -> {sh} {v}" + (f"  (failing: {'; '.join(fails)})" if fails else ""))
    P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
RES["verdict"] = {}
for sh in SHAPES:
    V = {f: RES["footings"][f]["shapes"][sh]["verdict"] for f in FEET}
    RES["verdict"][sh] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
    P(f"\n=== VERDICT {sh} (both footings): {RES['verdict'][sh]} [c_f EXTERNAL]")
checks.append(("K3", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(bool(ok) for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
if MUTATE and os.path.exists(os.path.join(HERE, "x69_split_vs_cnfw_results.json")):
    NJ = json.load(open(os.path.join(HERE, "x69_split_vs_cnfw_results.json")))
    dm = max(abs(RES["footings"][f_]["shapes"][s_]["clusters"][hk_][k_]["pred"] - NJ["footings"][f_]["shapes"][s_]["clusters"][hk_][k_]["pred"])
             for f_ in FEET for s_ in SHAPES for hk_ in HK for k_ in RES["footings"][f_]["shapes"][s_]["clusters"][hk_])
    P(f"MUTATE sensitivity: max cluster pred change vs normal run {dm:.3f} ({'sensitive' if dm > 0.01 else 'HARNESS INSENSITIVE'})"); RES["mutate_max_dpred"] = dm
open(os.path.join(HERE, f"x69_split_vs_cnfw{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
json.dump(RES, open(os.path.join(HERE, f"x69_split_vs_cnfw_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
