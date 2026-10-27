#!/usr/bin/env python3
"""GS1_measured_gas_outskirts: measure the X-COP gas density slope beyond R500 and regrade GC2's turnaround budget with it.
FROZEN_CRITERIA.md committed alone first (17064b9844). Harness: GC2 (3db544593b / 8f1554e920).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gs1_gas_slope.py      (GS1_MUTATE=1 twin)
"""
import os, sys, json, math, time, resource, io, contextlib, multiprocessing as mp
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np

MUT = os.environ.get("GS1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
RUND = os.path.join(HERE, f"runs{TAG}"); os.makedirs(RUND, exist_ok=True)
T0 = time.time()
OUT = open(os.path.join(HERE, f"gs1_gas_slope{TAG}.out"), "w")
RES = {"lane": "GS1_measured_gas_outskirts", "criteria": "17064b9844", "mutate": MUT, "checks": {}, "runs": {},
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
    sh = np.where(r > Rm, sm*(r/Rm)**-GC2_SLOPE, sh)
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



def edits(rule, native, ext, shape, anti, tag, slope=3.0):
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
    pre += 'NX.update(dict(GC2_EXT=%r, GC2_SHAPE=%r, GC2_ANTI=%r, GC2_SLOPE=%r))\n' % (ext, shape, anti, slope)
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


def _child(rule, native, ext, shape, anti, tag, q, slope=3.0):
    src = open(X43SRC).read()
    ed, inj = edits(rule, native, ext, shape, anti, tag, slope)
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


def run(rule, native, ext, shape="P", anti=False, tag=None, slope=3.0):
    tag = tag or f"{rule}_{'nat' if native else 'inh'}_{'ext' if ext else 'cut'}" + ("" if shape == "P" else f"_{shape}") + ("" if slope == 3.0 else f"_s{slope:.3f}")
    t = time.time()
    ctx = mp.get_context("fork"); q = ctx.Queue()
    p = ctx.Process(target=_child, args=(rule, native, ext, shape, anti, tag, q, slope)); p.start()
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


P("GS1_measured_gas_outskirts" + (" [MUTATE m1-m2: control output, not physics]" if MUT else "") +
  ": criteria 17064b9844; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")
P(f"native normalisation: Omega_c/Omega_b = {NAT_RRAT:.4f} (inherited 5.364); h {NAT_h}, Omega_m {NAT_OM}")

# ============================================================== A. measurement
from astropy.io import fits
XD = os.path.join(REB, "..", "real_research", "data", "xcop")
P("\n== A. X-COP gas density slope beyond R500")
def slope_fit(x, M, lo, hi):
    """density slope s = 3 - d ln(dM/dln r)/d ln r, least squares on the tabulated points in [lo, hi]."""
    lr = np.log(x); dM = np.diff(M) / np.diff(lr); xm = np.exp(0.5 * (lr[1:] + lr[:-1]))
    m = (xm >= lo) & (xm <= hi) & (dM > 0)
    if m.sum() < 3: return None
    b = np.polyfit(np.log(xm[m]), np.log(dM[m]), 1)[0]
    return 3.0 - b
# S0c: synthetic r^-2.5 on a real radial sampling
t0 = fits.open(os.path.join(XD, "A1795", "A1795_fgas_profile.fits"))[1].data
xs = np.asarray(t0["RADIUS"], float) * (1.5 if MUT else 1.0)
Msyn = xs ** 0.5
s0c = abs(slope_fit(np.asarray(t0["RADIUS"], float), Msyn, 1.0, 9.0) - 2.5) <= 0.01 and not MUT
SL, SLin, EXC = {}, {}, []
for d in sorted(os.listdir(XD)):
    p = os.path.join(XD, d, f"{d}_fgas_profile.fits")
    if not os.path.exists(p): continue
    t = fits.open(p)[1].data; x = np.asarray(t["RADIUS"], float) * (1.5 if MUT else 1.0); M = np.asarray(t["MGAS"], float)
    if x.max() < 1.5: EXC.append((d, float(x.max()))); continue
    SL[d] = slope_fit(x, M, 1.0, x.max()); SLin[d] = slope_fit(x, M, 0.5, 1.0)
vals = np.array(list(SL.values())); s_meas = float(np.median(vals))
rng = np.random.default_rng(0); bs = np.array([np.median(rng.choice(vals, len(vals))) for _ in range(10000)])
s16, s84 = (float(v) for v in np.quantile(bs, [0.16, 0.84]))
P("  per cluster s(1..x_max): " + ", ".join(f"{k} {v:.2f}" for k, v in SL.items()))
P(f"  excluded (x_max < 1.5): {EXC}")
P(f"  s_meas (median) {s_meas:.3f}, bootstrap 16-84% [{s16:.3f}, {s84:.3f}]; reported s(0.5..1) median {np.median(list(SLin.values())):.3f}")
RES["slope"] = {"per_cluster": SL, "s_meas": s_meas, "s16": s16, "s84": s84, "excluded": EXC, "s_inner_median": float(np.median(list(SLin.values())))}
check("S0b", len(SL) >= 10, f"{len(SL)} of {len(SL) + len(EXC)} clusters with x_max >= 1.5", ">= 10")
check("S0c", s0c, "synthetic r^-2.5 on A1795's sampling recovered within 0.01", "0.01")
check("K1", 1.0 <= s_meas <= 5.0, f"s_meas {s_meas:.3f}", "[1, 5]")
# ============================================================== B. regrade
P("\n== B. regrade (GC2 harness, tail rho ~ r^-s from R500, counted to r_ta, native)")
tg, r0 = run("R5", True, True, shape="R5", tag="S0a", slope=3.0)
c = r0["footings"]["canonical"]; m3 = [c["clusters"]["cells"][hk]["G-OUT-M3"]["Z"] for hk in ("h0672", "h0686")]
tgt = (0.49 * (1.01 if MUT else 1.0), 0.33, 1.82)
s0a = abs(m3[0] - tgt[0]) <= 0.005 and abs(m3[1] - tgt[1]) <= 0.005 and abs(c["groups"]["Z"] - tgt[2]) <= 0.005
check("S0a", s0a, f"s = 3 reproduces GC2 V-R5shape R5: M3 {m3[0]:+.2f}/{m3[1]:+.2f}, groups {c['groups']['Z']:+.2f}", "+0.49/+0.33, +1.82")
check("K2", True, "tail continuous at R500 by construction (sm = beta-model value at R500)", "construction")
if not (s0a and s0c) and not MUT:
    P("STOP: Step 0 failed."); RES["verdict"] = "STOPPED AT STEP 0"
    json.dump(RES, open(os.path.join(HERE, f"gs1_gas_slope_results{TAG}.json"), "w"), indent=1, default=float); sys.exit(1)
RUNS = {}
for rule in ("R4", "R5", "RX48"):
    for lab, s in (("meas", s_meas), ("s16", s16), ("s84", s84)):
        tg, r = run(rule, True, True, shape="R5", tag=f"{rule}_{lab}", slope=s); RUNS[f"{rule}_{lab}"] = r


def line_set_pass(r, f):
    ft = r["footings"][f]
    return all(st["line"] for st in ft["sparc"].values()) and ft["groups"]["PASS"] and not ft["clusters"]["fails"]


RES["verdicts"] = {}
for f in ("canonical", "alt"):
    P(f"\n== {f.upper()}")
    for k, r in RUNS.items():
        ft = r["footings"][f]; cc = ft["clusters"]["cells"]
        P(f"  {k:10s} M3 Z {cc['h0672']['G-OUT-M3']['Z']:+.2f}/{cc['h0686']['G-OUT-M3']['Z']:+.2f}; OUT-all {cc['h0672']['G-OUT-all']['Z']:+.2f}; IN-Mall {cc['h0672']['G-IN-Mall']['Z']:+.2f}; "
          f"groups {ft['groups']['Z']:+.2f}; SPARC {ft['sparc']['A_c2b_refit']['rms']:.4f}@{ft['sparc']['A_c2b_refit']['U_median']:.2f}; fails: {ft['clusters']['fails'] or 'none'}"
          + ("  << PASSES THE X43 LINE SET" if line_set_pass(r, f) else ""))
    passm = [rule for rule in ("R4", "R5", "RX48") if line_set_pass(RUNS[f"{rule}_meas"], f)]
    rob = {rule: (line_set_pass(RUNS[f"{rule}_s16"], f), line_set_pass(RUNS[f"{rule}_s84"], f)) for rule in passm}
    v = ("MEASURED SLOPE PASSES (" + ", ".join(passm) + ")") if passm else "MEASURED SLOPE FAILS"
    if passm:
        v += " " + ("ROBUST" if all(all(x) for x in rob.values()) else "FRAGILE (bootstrap edges: " + "; ".join(f"{k} s16 {a} s84 {b}" for k, (a, b) in rob.items()) + ")")
    RES["verdicts"][f] = {"class": v, "passing_rules": passm, "edges": rob}
    P(f"  ==> {f}: {v}")
RES["runs"] = {k: {f: {"fails": fails(v, f), "groups": v["footings"][f]["groups"], "cells": v["footings"][f]["clusters"]["cells"]} for f in ("canonical", "alt")} for k, v in RUNS.items()}
peak = max([v["_extra"]["rss"] for v in RUNS.values()] + [resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9])
check("K3", peak < 1.0, f"peak RSS {peak:.2f} GB, 1 thread, {time.time() - T0:.0f} s", "< 1 GB")
P("\n== VERDICT: " + "; ".join(f"{f}: {RES['verdicts'][f]['class']}" for f in ("canonical", "alt")))
P(f"  checks {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])}")
json.dump(RES, open(os.path.join(HERE, f"gs1_gas_slope_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
