#!/usr/bin/env python3
"""GC2_turnaround_baryon_budget: count the record's own gas profile to the self-consistent turnaround radius (not the
3 Mpc cut) when setting the cold dark energy halo normalisation; native background. FROZEN_CRITERIA.md committed alone
first (3db544593b). Harness: GC1's (d1da6b8185) text-patched X43 copies in forked processes.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gc2_budget.py      (GC2_MUTATE=1 twin)
Each configuration runs a text-patched copy of X43 in a forked process (X62's pattern); X43's own files are never written.
"""
import os, sys, json, math, time, resource, io, contextlib, multiprocessing as mp
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np

MUT = os.environ.get("GC2_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
RUND = os.path.join(HERE, f"runs{TAG}"); os.makedirs(RUND, exist_ok=True)
T0 = time.time()
OUT = open(os.path.join(HERE, f"gc2_budget{TAG}.out"), "w")
RES = {"lane": "GC2_turnaround_baryon_budget", "criteria": "3db544593b", "mutate": MUT, "checks": {}, "runs": {},
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


GC2_EXT_CODE = """
GC2_LOG = []
def _gc2_ext(Mg500, R500, z, Mbt_cut):
    r = RG; rc = 0.15*R500; beta = 2/3; sh = (1 + (r/rc)**2)**(-1.5*beta)
    Rm = R500 if GC2_SHAPE == "R5" else 2.2*R500; sm = (1 + (Rm/rc)**2)**(-1.5*beta)
    sh = np.where(r > Rm, sm*(r/Rm)**-3.0, sh)
    if GC2_ANTI: sh = np.where(r > 2.0, 0.0, sh)
    dm = 4*np.pi*(r*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r*MPC))]
    Mbx = 1.2*M*(Mg500*MSUN/np.interp(R500, r, M))
    rta = r_ta_com(Mbt_cut)/(1 + z); n = 0
    for n in range(1, 200):
        Mbt = float(np.interp(rta, RM, Mbx)); new = r_ta_com(Mbt)/(1 + z)
        if abs(new/rta - 1) < 1e-6: rta = new; break
        rta = new
    Mbt = float(np.interp(rta, RM, Mbx))
    GC2_LOG.append((float(Mg500), float(Mbt/Mbt_cut), int(n), float(rta/MPC)))           # A1: Mg500 is already in Msun
    return np.where(RM <= rta, Mbx, Mbt), Mbt
"""



def edits(rule, native, ext, shape, anti, tag):
    ed = [("for cf in (3.0, 5.0):", "for cf in ():"),
          ('f"x43_collapse_core{TAG}.out"', repr(os.path.join(RUND, f"x43copy_{tag}.out"))),
          ('f"x43_collapse_core_results{TAG}.json"', repr(os.path.join(RUND, f"x43copy_{tag}_results.json"))),
          ('"x43_x30_machinery" + TAG + ".log"', repr(os.path.join(RUND, f"gc2_x30_{tag}.log")))]
    if rule == "R5":
        ed.append(("CF = 4.0", "CF = 5.0"))
    if rule == "RX48":
        ed.append(('sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2',
                   'sc = (ETA_FUN(M) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2'))
    pre = 'NX = {"__file__": X30SRC, "__name__": "x30_ro"}\n'
    pre += 'NX.update(dict(GC2_EXT=%r, GC2_SHAPE=%r, GC2_ANTI=%r))\n' % (ext, shape, anti)
    old_prep = '    Mg500 = cl["Mgas500"]*qd**2.5; R500 = cl["R500"]*qd; Mg, rho_g = gas(Mg500, R500, "P"); Mb = Mg*(1 + 0.20); Mbt = float(Mb[-1])'
    new_prep = old_prep + '\n    if GC2_EXT: Mb, Mbt = _gc2_ext(Mg500, R500, cl["z"], Mbt)'
    pre += 'assert codeX.count(%r) == 1\n' % old_prep
    pre += 'codeX = codeX.replace(%r, %r)\n' % (old_prep, new_prep)
    pre += 'codeX = codeX.replace("PREP = {}\\ndef prep", GC2_EXT_CODE + "PREP = {}\\ndef prep")\n'
    pre += 'assert "def _gc2_ext" in codeX\n'
    if native:
        pre += ('codeX = codeX.replace("H0_946 = 67.4e3/MPC946", "H0_946 = %r*100e3/MPC946")\n'
                'codeX = codeX.replace("OB946 = 0.0493; OC946 = 5.364*OB946", "OB946 = %r; OC946 = %r*OB946")\n'
                'codeX = codeX.replace("Mfair=5.364*Mbt", "Mfair=%r*Mbt")\n'
                'assert all(s in codeX for s in ("H0_946 = %r", "OB946 = %r", "Mfair=%r"))\n' % (NAT_h, NAT_OB, NAT_RRAT, NAT_RRAT, NAT_h, NAT_OB, NAT_RRAT))
    ed.append(('NX = {"__file__": X30SRC, "__name__": "x30_ro"}', pre.rstrip("\n")))
    return ed, {"GC2_EXT_CODE": GC2_EXT_CODE}


def _child(rule, native, ext, shape, anti, tag, q):
    src = open(X43SRC).read()
    ed, inj = edits(rule, native, ext, shape, anti, tag)
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
    extra = {"log": list(ns["NX"].get("GC2_LOG", []))[:N_LOG], "rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9}
    q.put(extra)


N_LOG = 700


def run(rule, native, ext, shape="P", anti=False, tag=None):
    tag = tag or f"{rule}_{'nat' if native else 'inh'}_{'ext' if ext else 'cut'}" + ("" if shape == "P" else f"_{shape}")
    t = time.time()
    ctx = mp.get_context("fork"); q = ctx.Queue()
    p = ctx.Process(target=_child, args=(rule, native, ext, shape, anti, tag, q)); p.start()
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


P("GC2_turnaround_baryon_budget" + (" [MUTATE m1-m2: control output, not physics]" if MUT else "") +
  ": criteria 3db544593b; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")
P(f"native normalisation: Omega_c/Omega_b = {NAT_RRAT:.4f} (inherited 5.364); h {NAT_h}, Omega_m {NAT_OM}")

# ============================================================== STEP 0
P("\n== STEP 0 (stop rule)")
tg, r0 = run("R4", False, False, tag="S0a")
c = r0["footings"]["canonical"]
tgt = {"M3_h0672": 1.120 * (1.01 if MUT else 1.0), "M3_h0686": 1.108, "groups_Z": 2.05, "sparc": 0.0782}
got = {"M3_h0672": c["clusters"]["cells"]["h0672"]["G-OUT-M3"]["pred"], "M3_h0686": c["clusters"]["cells"]["h0686"]["G-OUT-M3"]["pred"],
       "groups_Z": c["groups"]["Z"], "sparc": c["sparc"]["A_c2b_refit"]["rms"]}
s0a = all(abs(got[k] - tgt[k]) <= (5e-4 if k != "groups_Z" else 5e-3) for k in tgt)
check("S0a", s0a, "; ".join(f"{k} {got[k]:.4f}/{tgt[k]:.4f}" for k in tgt), "X43 committed numbers to 3 decimals")
ANTI = MUT                                                                         # m1
RUNS = {}
for rule in ("R4", "R5", "RX48"):
    for native in (False, True):
        for ext in (False, True):
            tg, r = run(rule, native, ext, anti=(ANTI and ext)); RUNS[tg] = r
    tg, r = run(rule, True, True, shape="R5", anti=ANTI); RUNS[tg] = r
log = RUNS["R4_nat_ext"]["_extra"]["log"]
uniq = {}
for mg, ratio, n, rta in log: uniq[float("%.6e" % mg)] = (ratio, n, rta)
mg = np.array(sorted(uniq)); rat = np.array([uniq[m][0] for m in mg]); nit = np.array([uniq[m][1] for m in mg])
s0b = bool(np.all(nit < 50)) and len(mg) > 100
t1, t2 = np.quantile(mg, [1 / 3, 2 / 3])
med = [float(np.median(rat[mg <= t1])), float(np.median(rat[(mg > t1) & (mg <= t2)])), float(np.median(rat[mg > t2]))]
check("S0b", s0b, f"fixed point converged for {len(mg)} clusters (max iterations {nit.max()}); Mbt_ext/Mbt_cut median {np.median(rat):.3f}, "
      f"by Mgas500 tercile {med[0]:.3f} / {med[1]:.3f} / {med[2]:.3f}, min {rat.min():.3f}, max {rat.max():.3f}", "converges < 50")
RES["budget_ratio"] = {"median": float(np.median(rat)), "terciles": med, "min": float(rat.min()), "max": float(rat.max())}
if not (s0a and s0b) and not MUT:
    P("STOP: Step 0 failed."); RES["verdict"] = "STOPPED AT STEP 0"
    json.dump(RES, open(os.path.join(HERE, f"gc2_budget_results{TAG}.json"), "w"), indent=1, default=float); sys.exit(1)
check("K1", bool(np.all(rat >= 1 - 1e-9)), f"extended Mbt >= cut Mbt for every cluster (min ratio {rat.min():.4f})", ">= 1")
check("K2", med[2] > med[0], f"budget ratio top-tercile median {med[2]:.3f} vs bottom {med[0]:.3f}", "rises with Mgas500 (predicted direction)")


def line_set_pass(r, f):
    ft = r["footings"][f]
    return all(st["line"] for st in ft["sparc"].values()) and ft["groups"]["PASS"] and not ft["clusters"]["fails"]


def klass(r_on, r_off, f):
    m3ok = all(abs(keys(r_on, f)[hk]["G-OUT-M3"]["Z"]) <= 2 for hk in ("h0672", "h0686"))
    passed_before = [k for k, ok in r_off["footings"][f]["clusters"]["ok"].items() if ok]
    newly = [k for k in passed_before if not r_on["footings"][f]["clusters"]["ok"][k]]
    return "NOT REPAIRED" if not m3ok else ("TURNAROUND BUDGET REPAIRS M3" if not newly else f"REPAIRS M3 BUT BREAKS ({', '.join(newly)})")


RES["verdicts"] = {}
for f in ("canonical", "alt"):
    P(f"\n== {f.upper()}")
    for rule in ("R4", "R5", "RX48"):
        for cfg in ("inh_cut", "inh_ext", "nat_cut", "nat_ext", "nat_ext_R5"):
            r = RUNS[f"{rule}_{cfg}"]; ft = r["footings"][f]; m3 = [ft["clusters"]["cells"][hk]["G-OUT-M3"] for hk in ("h0672", "h0686")]
            P(f"  {rule:5s} {cfg:11s} M3 pred {m3[0]['pred']:.3f}/{m3[1]['pred']:.3f} (meas {m3[0]['meas']:.3f}) Z {m3[0]['Z']:+.2f}/{m3[1]['Z']:+.2f}; groups Z {ft['groups']['Z']:+.2f}; "
              f"SPARC {ft['sparc']['A_c2b_refit']['rms']:.4f}@{ft['sparc']['A_c2b_refit']['U_median']:.2f}; cluster fails: {ft['clusters']['fails'] or 'none'}"
              + ("  << PASSES THE X43 LINE SET" if line_set_pass(r, f) else ""))
    cls = klass(RUNS["R4_nat_ext"], RUNS["R4_nat_cut"], f); clsv = klass(RUNS["R4_nat_ext_R5"], RUNS["R4_nat_cut"], f)
    robust = cls.split(" (")[0] == clsv.split(" (")[0]
    lsp = {rule: line_set_pass(RUNS[f"{rule}_nat_ext"], f) for rule in ("R4", "R5", "RX48")}
    lspv = {rule: line_set_pass(RUNS[f"{rule}_nat_ext_R5"], f) for rule in ("R4", "R5", "RX48")}
    RES["verdicts"][f] = {"R4_class": cls, "robust_vs_R5shape": robust, "R5shape_class": clsv, "line_set_pass_native_ext": lsp, "line_set_pass_R5shape": lspv}
    P(f"  ==> {f}: R4 {cls} ({'ROBUST' if robust else 'FRAGILE: V-R5shape gives ' + clsv}); X43 line set passed (native + extended): {lsp}; V-R5shape: {lspv}")
RES["runs"] = {k: {f: {"fails": fails(v, f), "groups": v["footings"][f]["groups"], "sparc": {t: {kk: v["footings"][f]["sparc"][t][kk] for kk in ("rms", "U_median", "line")} for t in v["footings"][f]["sparc"]},
                       "cells": v["footings"][f]["clusters"]["cells"]} for f in ("canonical", "alt")} for k, v in RUNS.items()}
peak = max([v["_extra"]["rss"] for v in RUNS.values()] + [resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9])
check("K3", peak < 1.0, f"peak RSS {peak:.2f} GB (max over forked runs), 1 thread, {time.time() - T0:.0f} s", "< 1 GB")
P("\n== VERDICT: " + "; ".join(f"{f}: {RES['verdicts'][f]['R4_class']}" for f in ("canonical", "alt")))
P(f"  checks {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])}")
json.dump(RES, open(os.path.join(HERE, f"gc2_budget_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
