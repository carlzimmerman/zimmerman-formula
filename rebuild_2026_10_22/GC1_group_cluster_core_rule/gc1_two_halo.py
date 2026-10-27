#!/usr/bin/env python3
"""GC1_group_cluster_core_rule: is the universal G-OUT-M3 deficit the projected correlated structure beyond each cluster's
turnaround radius? Zero-parameter term (CLASS linear xi, Mo & White bias, r > r_ta only) added to X43's cluster chain, with
the cluster halo normalisation moved to the native background (5.2715). FROZEN_CRITERIA.md committed alone first (d1da6b8185).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gc1_two_halo.py      (GC1_MUTATE=1 twin)
Each configuration runs a text-patched copy of X43 in a forked process (X62's pattern); X43's own files are never written.
"""
import os, sys, json, math, time, resource, io, contextlib, multiprocessing as mp
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np

MUT = os.environ.get("GC1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
RUND = os.path.join(HERE, f"runs{TAG}"); os.makedirs(RUND, exist_ok=True)
T0 = time.time()
OUT = open(os.path.join(HERE, f"gc1_two_halo{TAG}.out"), "w")
RES = {"lane": "GC1_group_cluster_core_rule", "criteria": "d1da6b8185", "mutate": MUT, "checks": {}, "runs": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


NAT_OM, NAT_h, NAT_wb = 0.2976016, 0.6856427, 0.0223081
NAT_OB = NAT_wb / NAT_h ** 2
NAT_RRAT = (NAT_OM - NAT_OB) / NAT_OB
X43SRC = os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")
X48TAB = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_regrade_ng48.json")))["table"]

M2H_CODE = '''
# ---------------- GC1: correlated structure beyond r_ta (zero parameters) ----------------
_bgA = BGSE["A_c2b_refit"]; _cA = _bgA["c"]; _hA = _bgA["h"]
_kk = np.logspace(-4, np.log10(140.0), 6000)                                   # 1/Mpc (CLASS table ends at 141)
_PK = np.array([_cA.pk_lin(float(x), 0.0) for x in _kk])                       # Mpc^3
_rx = np.logspace(np.log10(0.5), np.log10(400.0), 500)                          # comoving Mpc
_lk = np.log(_kk); _damp = np.exp(-(_kk * 0.05) ** 2)
_XI = np.array([np.trapz(_kk ** 3 * _PK * np.sinc(_kk * r / np.pi) * _damp, _lk) / (2 * np.pi ** 2) for r in _rx])
_e = EPS["A_c2b_refit"]
_OMA = float(_cA.Omega_m()); _RHOC0 = _bgA["rhoc"](0.0)                        # kg/m^3
GC1_LOG = []
def _bias(Mmsun, z):
    s = math.sqrt(float(np.interp(math.log10(Mmsun), _e["lMg"], _e["s2"]))) * float(np.interp(z, _e["zg"], _e["Dg"]))
    nu = DC / s
    if GC1_BIAS == "ST":
        a, p = 0.707, 0.3; an2 = a * nu * nu
        return 1 + (an2 - 1) / DC + 2 * p / (DC * (1 + an2 ** p)), nu
    return 1 + (nu * nu - 1) / DC, nu
def M2H(i, pp, Mtot):
    if not GC1_TWOH: return 0.0
    z = float(NX["CL"][i]["z"]); b, nu = _bias(Mtot, z); D = float(np.interp(z, _e["zg"], _e["Dg"]))
    rmpc = RM / MPCE; xi = np.interp(np.log(rmpc * (1 + z)), np.log(_rx), _XI) * D * D
    rhobar = _OMA * _RHOC0 * (1 + z) ** 3
    rho = np.where(RM > GC1_CUT * pp["rta"], GC1_SIGN * b * rhobar * xi, 0.0)
    dm = 4 * np.pi * RM ** 2 * rho
    M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RM))]
    GC1_LOG.append((int(i), float(z), float(Mtot), float(b), float(nu), float(pp["rta"] / MPCE), float(M[-1] / MSUNE)))
    return M
'''


def edits(rule, native, twoh, cut, bias, sign, tag):
    ed = [("for cf in (3.0, 5.0):", "for cf in ():"),
          ('f"x43_collapse_core{TAG}.out"', repr(os.path.join(RUND, f"x43copy_{tag}.out"))),
          ('f"x43_collapse_core_results{TAG}.json"', repr(os.path.join(RUND, f"x43copy_{tag}_results.json"))),
          ('"x43_x30_machinery" + TAG + ".log"', repr(os.path.join(RUND, f"gc1_x30_{tag}.log"))),
          ("def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):", M2H_CODE + "def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):"),
          ('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh + M2H(int(i), pp, Mtot))')]
    if rule == "R5":
        ed.append(("CF = 4.0", "CF = 5.0"))
    if rule == "RX48":
        ed.append(('sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2',
                   'sc = (ETA_FUN(M) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2'))
    if native:
        ed.append(('NX = {"__file__": X30SRC, "__name__": "x30_ro"}',
                   'NX = {"__file__": X30SRC, "__name__": "x30_ro"}\n'
                   'codeX = codeX.replace("H0_946 = 67.4e3/MPC946", "H0_946 = %r*100e3/MPC946")\n'
                   'codeX = codeX.replace("OB946 = 0.0493; OC946 = 5.364*OB946", "OB946 = %r; OC946 = %r*OB946")\n'
                   'codeX = codeX.replace("Mfair=5.364*Mbt", "Mfair=%r*Mbt")\n'
                   'assert all(s in codeX for s in ("H0_946 = %r", "OB946 = %r", "Mfair=%r"))' % (NAT_h, NAT_OB, NAT_RRAT, NAT_RRAT, NAT_h, NAT_OB, NAT_RRAT)))
    return ed, {"GC1_TWOH": twoh, "GC1_CUT": cut, "GC1_BIAS": bias, "GC1_SIGN": sign}


def _child(rule, native, twoh, cut, bias, sign, tag, q):
    src = open(X43SRC).read()
    ed, inj = edits(rule, native, twoh, cut, bias, sign, tag)
    for old, new in ed:
        assert src.count(old) == 1, (old[:70], src.count(old)); src = src.replace(old, new)
    B1 = 3 * math.log(2) - math.pi / 2
    LMk, CFk = np.array(X48TAB["lgM"]), np.array(X48TAB["cf"])
    inj["ETA_FUN"] = lambda M: 4.0 / (3.0 * B1) * float(np.interp(math.log10(M), LMk, CFk)) ** 1.25
    ns = {"__file__": os.path.join(REB, "X43_collapse_core_floor", f"gc1copy_{tag}.py"), "__name__": "x43copy"}; ns.update(inj)   # path resolution only; nothing is written there
    sys.argv = [ns["__file__"]]
    os.chdir(RUND)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            exec(compile(src, X43SRC, "exec"), ns)
        except SystemExit:
            pass
    extra = {"log": ns.get("GC1_LOG", [])[:N_LOG] if ns.get("GC1_LOG") else [], "rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9}
    if tag == "S0b":
        c = ns["BGSE"]["A_c2b_refit"]["c"]; h = ns["BGSE"]["A_c2b_refit"]["h"]
        kk = np.logspace(-4, math.log10(150.0), 6000); Pk = np.array([c.pk_lin(float(x) * h, 0.0) for x in kk]) * h ** 3
        x = 8 * kk; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        extra["s8_mine"] = float(np.sqrt(np.trapz(kk ** 3 * Pk * W ** 2 / (2 * math.pi ** 2), np.log(kk))))
        extra["s8_em1"] = float(ns["BGSE"]["A_c2b_refit"]["s8"])
        b1 = ns["_bias"](1e14, 0.0)
        # nu = 1 mass
        e = ns["EPS"]["A_c2b_refit"]; lM1 = float(np.interp(-1.0, -np.sqrt(e["s2"]) / ns["DC"], e["lMg"]))
        extra["b_at_nu1"] = ns["_bias"](10 ** lM1, 0.0)[0]
        extra["b_mono"] = all(np.diff([ns["_bias"](10 ** l, 0.3)[0] for l in (13, 13.5, 14, 14.5, 15)]) > 0)
    q.put(extra)


N_LOG = 700


def run(rule, native, twoh, cut=1.0, bias="MW", sign=1.0, tag=None):
    tag = tag or f"{rule}_{'nat' if native else 'inh'}_{'2h' if twoh else 'no2h'}" + ("" if cut == 1.0 else f"_cut{cut}") + ("" if bias == "MW" else f"_{bias}")
    t = time.time()
    ctx = mp.get_context("fork"); q = ctx.Queue()
    p = ctx.Process(target=_child, args=(rule, native, twoh, cut, bias, sign, tag, q)); p.start()
    import queue as _qm
    extra = None
    while extra is None:
        try: extra = q.get(timeout=30)
        except _qm.Empty:
            if not p.is_alive(): raise RuntimeError(f"child for {tag} died (exit {p.exitcode})")
    p.join()
    r = json.load(open(os.path.join(RUND, f"x43copy_{tag}_results.json")))
    r["_extra"] = extra
    P(f"  run {tag}: {time.time() - t:.0f} s, child RSS {extra['rss']:.2f} GB")
    return tag, r


def keys(r, f):
    return r["footings"][f]["clusters"]["cells"]


def fails(r, f):
    return r["footings"][f]["clusters"]["fails"]


P("GC1_group_cluster_core_rule" + (" [MUTATE m1-m2: control output, not physics]" if MUT else "") +
  ": criteria d1da6b8185; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")
P(f"native normalisation: Omega_c/Omega_b = {NAT_RRAT:.4f} (inherited 5.364); h {NAT_h}, Omega_m {NAT_OM}")

# ============================================================== STEP 0
P("\n== STEP 0 (stop rule)")
tg, r0 = run("R4", False, False, tag="S0a")
RES["runs"]["S0a"] = r0
c = r0["footings"]["canonical"]
tgt = {"M3_h0672": 1.120 * (1.01 if MUT else 1.0), "M3_h0686": 1.108, "groups_Z": 2.05, "sparc": 0.0782}
got = {"M3_h0672": c["clusters"]["cells"]["h0672"]["G-OUT-M3"]["pred"], "M3_h0686": c["clusters"]["cells"]["h0686"]["G-OUT-M3"]["pred"],
       "groups_Z": c["groups"]["Z"], "sparc": c["sparc"]["A_c2b_refit"]["rms"]}
s0a = all(abs(got[k] - tgt[k]) <= (5e-4 if k != "groups_Z" else 5e-3) for k in tgt)
check("S0a", s0a, "; ".join(f"{k} {got[k]:.4f}/{tgt[k]:.4f}" for k in tgt), "X43 committed numbers to 3 decimals")
tg, rb = run("R4", True, True, tag="S0b")
ex = rb["_extra"]
s0b = abs(ex["s8_mine"] / ex["s8_em1"] - 1) <= 0.01
check("S0b", s0b, f"sigma8 from pk_lin {ex['s8_mine']:.5f} vs EM1 {ex['s8_em1']:.5f}", "within 1%")
s0c = abs(ex["b_at_nu1"] - 1) <= 1e-3 and ex["b_mono"]
check("S0c", s0c, f"Mo-White b(nu=1) = {ex['b_at_nu1']:.5f}; increasing with M: {ex['b_mono']}", "b(nu=1) = 1; monotone")
if not (s0a and s0b and s0c) and not MUT:
    P("STOP: Step 0 failed."); RES["verdict"] = "STOPPED AT STEP 0"
    json.dump(RES, open(os.path.join(HERE, f"gc1_two_halo_results{TAG}.json"), "w"), indent=1, default=float); sys.exit(1)

# K2: native Mfair ratio (per cluster, from the patched constants)
check("K2", abs(NAT_RRAT / 5.364 - 0.98275) < 2e-4, f"Mfair_native / Mfair_inherited = {NAT_RRAT / 5.364:.5f} (5.2715/5.364)", "exact ratio by construction")

# ============================================================== runs
SIGN = -1.0 if MUT else 1.0                                                     # m1
RUNS = {}
for rule in ("R4", "R5", "RX48"):
    for native in (False, True):
        for twoh in (False, True):
            tg, r = run(rule, native, twoh, sign=SIGN if twoh else 1.0); RUNS[tg] = r
    tg, r = run(rule, True, True, cut=1.5, sign=SIGN); RUNS[tg] = r
tg, r = run("R4", True, True, bias="ST", sign=SIGN); RUNS[tg] = r

# K1: term positive at OUTER (pred with >= pred without for every OUTER key, both footings, primary)
k1 = True
for rule in ("R4", "R5", "RX48"):
    for f in ("canonical", "alt"):
        a, b = keys(RUNS[f"{rule}_nat_2h"], f), keys(RUNS[f"{rule}_nat_no2h"], f)
        for hk in a:
            for k in a[hk]:
                if "OUT" in k and k != "G-OUT-b" and a[hk][k]["pred"] < b[hk][k]["pred"] - 1e-9:
                    k1 = False
check("K1", k1, "correlated-structure term raises every OUTER prediction (both footings, all rules)", "term >= 0 at OUTER")

# ============================================================== report + verdict
def line_set_pass(r, f):
    ft = r["footings"][f]
    return all(st["line"] for st in ft["sparc"].values()) and ft["groups"]["PASS"] and not ft["clusters"]["fails"]


RES["verdicts"] = {}
for f in ("canonical", "alt"):
    P(f"\n== {f.upper()}")
    for rule in ("R4", "R5", "RX48"):
        for cfg in ("inh_no2h", "inh_2h", "nat_no2h", "nat_2h", "nat_2h_cut1.5"):
            r = RUNS[f"{rule}_{cfg}"]; ft = r["footings"][f]; m3 = [ft["clusters"]["cells"][hk]["G-OUT-M3"] for hk in ("h0672", "h0686")]
            P(f"  {rule:5s} {cfg:14s} M3 pred {m3[0]['pred']:.3f}/{m3[1]['pred']:.3f} Z {m3[0]['Z']:+.2f}/{m3[1]['Z']:+.2f}; groups Z {ft['groups']['Z']:+.2f}; "
              f"SPARC {ft['sparc']['A_c2b_refit']['rms']:.4f}@{ft['sparc']['A_c2b_refit']['U_median']:.2f}; cluster fails: {ft['clusters']['fails'] or 'none'}"
              + ("  << PASSES THE X43 LINE SET" if line_set_pass(r, f) else ""))
    r_on, r_off = RUNS["R4_nat_2h"], RUNS["R4_nat_no2h"]
    m3ok = all(abs(keys(r_on, f)[hk]["G-OUT-M3"]["Z"]) <= 2 for hk in ("h0672", "h0686"))
    passed_before = [k for k, ok in r_off["footings"][f]["clusters"]["ok"].items() if ok]
    newly = [k for k in passed_before if not r_on["footings"][f]["clusters"]["ok"][k]]
    cls = "NOT REPAIRED" if not m3ok else ("TWO-HALO REPAIRS M3" if not newly else f"REPAIRS M3 BUT BREAKS ({', '.join(newly)})")
    rc = RUNS["R4_nat_2h_cut1.5"]
    m3c = all(abs(keys(rc, f)[hk]["G-OUT-M3"]["Z"]) <= 2 for hk in ("h0672", "h0686"))
    newc = [k for k in passed_before if not rc["footings"][f]["clusters"]["ok"][k]]
    clsc = "NOT REPAIRED" if not m3c else ("TWO-HALO REPAIRS M3" if not newc else f"REPAIRS M3 BUT BREAKS ({', '.join(newc)})")
    robust = clsc.split(" (")[0] == cls.split(" (")[0]
    lsp = {rule: line_set_pass(RUNS[f"{rule}_nat_2h"], f) for rule in ("R4", "R5", "RX48")}
    st = RUNS["R4_nat_2h_ST"]["footings"][f]["clusters"]["cells"]["h0672"]["G-OUT-M3"]
    frac = {k: 1 - keys(r_off, f)["h0672"][k]["pred"] / keys(r_on, f)["h0672"][k]["pred"] for k in ("G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-OUT-all", "G-IN-Mall")}
    RES["verdicts"][f] = {"R4_class": cls, "robust_vs_cut1.5": robust, "cut1.5_class": clsc, "line_set_pass_native_2h": lsp,
                          "ST_M3_Z_h0672_reported": st["Z"], "term_fraction_h0672": frac}
    P(f"  ==> {f}: R4 {cls} ({'ROBUST' if robust else 'FRAGILE: V-cut1.5 gives ' + clsc}); X43 line set passed (native + term): {lsp}")
    P(f"     term share of prediction (h0672): " + ", ".join(f"{k} {v:.3f}" for k, v in frac.items()) + f"; Sheth-Tormen (reported) M3 Z {st['Z']:+.2f}")
log = RUNS["R4_nat_2h"]["_extra"]["log"]
if log:
    bs = np.array([l[3] for l in log]); RES["bias_range"] = [float(bs.min()), float(np.median(bs)), float(bs.max())]
    P(f"\n  bias (Mo-White) over clusters: min {bs.min():.2f}, median {np.median(bs):.2f}, max {bs.max():.2f}")
RES["runs"] = {k: {f: {"fails": fails(v, f), "groups_Z": v["footings"][f]["groups"]["Z"],
                       "M3": [v["footings"][f]["clusters"]["cells"][hk]["G-OUT-M3"] for hk in ("h0672", "h0686")],
                       "cells": v["footings"][f]["clusters"]["cells"]} for f in ("canonical", "alt")} for k, v in RUNS.items()}
peak = max([v["_extra"]["rss"] for v in RUNS.values()] + [resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9])
check("K3", peak < 1.0, f"peak RSS {peak:.2f} GB (max over forked runs), 1 thread, {time.time() - T0:.0f} s", "< 1 GB")
P("\n== VERDICT: " + "; ".join(f"{f}: {RES['verdicts'][f]['R4_class']}" for f in ("canonical", "alt")))
P(f"  checks {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])}")
json.dump(RES, open(os.path.join(HERE, f"gc1_two_halo_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
