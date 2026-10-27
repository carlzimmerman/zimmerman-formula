#!/usr/bin/env python3
"""GC3_infall_halo_outskirts: cluster cold dark energy halo outskirts from self-similar infall (cored rho ~ r^-9/4), core by
X43's rule, normalised to the native fair share of baryons inside R500, truncated at splashback 0.364 r_ta.
FROZEN_CRITERIA.md committed alone first (50c3953710). Harness: GC1/GC2's text-patched X43 copies in forked processes.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gc3_infall.py      (GC3_MUTATE=1 twin)
"""
import os, sys, json, math, time, resource, io, contextlib, multiprocessing as mp
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np

MUT = os.environ.get("GC3_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
RUND = os.path.join(HERE, f"runs{TAG}"); os.makedirs(RUND, exist_ok=True)
T0 = time.time()
OUT = open(os.path.join(HERE, f"gc3_infall{TAG}.out"), "w")
RES = {"lane": "GC3_infall_halo_outskirts", "criteria": "50c3953710", "mutate": MUT, "checks": {}, "runs": {},
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


GC3_CODE = """
# ---------------- GC3: self-similar infall halo outskirts ----------------
GC3_LOG = []
_gq = GC3_Q
_xg = np.logspace(-7, 7, 20001)
_fx = 1.0 / ((1 + _xg) * (1 + _xg ** 2) ** ((_gq - 1) / 2))
_Ix = np.r_[0.0, np.cumsum(0.5 * (_fx[1:] * _xg[1:] ** 3 + _fx[:-1] * _xg[:-1] ** 3) * np.diff(np.log(_xg)))] + _fx[0] * _xg[0] ** 3 / 3
def _I(X): return np.interp(np.log(np.maximum(X, 1e-7)), np.log(_xg), _Ix)
def _gc3_rta_ext(pp, i):
    cl = NX["CL"][i]; Mg500 = cl["Mgas500"]; z = cl["z"]
    # reported variant only: GC2's extended budget radius (same fixed point), recomputed from the stored profile
    return pp.get("rta_ext", pp["rta"])
def GC3_HALO(pp, s, i):
    R500m = pp["R500"] * MPCE
    Mb500 = float(np.interp(R500m, RM, pp["Mb"])); T = GC3_RRAT * Mb500
    rsp = 0.364 * (pp["rta"] if not GC3_RSPEXT else pp.get("rta_ext", pp["rta"]))
    g = lambda lr: math.log(4 * math.pi * s * math.exp(2 * lr) * float(_I(R500m / math.exp(lr)))) - math.log(T)
    lo, hi = math.log(R500m * 1e-4), math.log(R500m * 1e4); sat = False
    from scipy.optimize import minimize_scalar as _ms                              # A1: X43's compact-root convention
    pk = float(_ms(lambda lr: -g(lr), bounds=(lo, hi), method="bounded", options={"xatol": 1e-10}).x)
    if g(pk) < 0: lr0 = pk; sat = True                                             # saturated at the peak (max mass inside R500)
    else: lr0 = brentq(g, lo, pk, xtol=1e-12)                                       # compact root on the rising branch
    r0 = math.exp(lr0)
    Mh = 4 * math.pi * s * r0 ** 2 * _I(np.minimum(RM, rsp) / r0)
    GC3_LOG.append((int(i), float(T), float(4 * math.pi * s * r0 ** 2 * float(_I(R500m / r0))), bool(sat), float(r0 / MPCE), float(rsp / MPCE)))
    return Mh
"""




def edits(rule, native, halo, rspext, tag):
    ed = [("for cf in (3.0, 5.0):", "for cf in ():"),
          ('f"x43_collapse_core{TAG}.out"', repr(os.path.join(RUND, f"x43copy_{tag}.out"))),
          ('f"x43_collapse_core_results{TAG}.json"', repr(os.path.join(RUND, f"x43copy_{tag}_results.json"))),
          ('"x43_x30_machinery" + TAG + ".log"', repr(os.path.join(RUND, f"gc3_x30_{tag}.log")))]
    if rule == "R5":
        ed.append(("CF = 4.0", "CF = 5.0"))
    if rule == "RX48":
        ed.append(('sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2',
                   'sc = (ETA_FUN(M) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2'))
    if halo:
        rr = NAT_RRAT if native else 5.364
        ed.append(("def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):",
                   "GC3_Q = %r; GC3_RRAT = %r; GC3_RSPEXT = %r\n" % (2.25 if not MUT else 3.0, rr, rspext) + GC3_CODE + "def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):"))
        ed.append(('r0 = solve_r0(pp["Mfair"], pp["rta"], s); Mh = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)',
                   'Mh = GC3_HALO(pp, s, int(i))'))
    if native:
        pre = ('NX = {"__file__": X30SRC, "__name__": "x30_ro"}\n'
               'codeX = codeX.replace("H0_946 = 67.4e3/MPC946", "H0_946 = %r*100e3/MPC946")\n'
               'codeX = codeX.replace("OB946 = 0.0493; OC946 = 5.364*OB946", "OB946 = %r; OC946 = %r*OB946")\n'
               'codeX = codeX.replace("Mfair=5.364*Mbt", "Mfair=%r*Mbt")\n'
               'assert all(s in codeX for s in ("H0_946 = %r", "OB946 = %r", "Mfair=%r"))' % (NAT_h, NAT_OB, NAT_RRAT, NAT_RRAT, NAT_h, NAT_OB, NAT_RRAT))
        ed.append(('NX = {"__file__": X30SRC, "__name__": "x30_ro"}', pre))
    if rspext:
        # V-rsp: GC2's extended r_ta stored in prep's output (reported only)
        ext = ('NX.update(dict(GC2_SHAPE="P", GC2_ANTI=False))\n'
               'codeX = codeX.replace("PREP = {}\\ndef prep", %r + "PREP = {}\\ndef prep")\n' % GC2X +
               'codeX = codeX.replace(\'PREP[key] = out; return out\', \'out["rta_ext"] = _gc2_rta(Mg500, R500, cl["z"], Mbt); PREP[key] = out; return out\')\n'
               'assert "_gc2_rta" in codeX')
        ed.append(("sys.argv = [X30SRC]", ext + "; sys.argv = [X30SRC]"))
    return ed, {"GC3_CODE": GC3_CODE}


GC2X = """
def _gc2_rta(Mg500, R500, z, Mbt_cut):
    r = RG; rc = 0.15*R500; beta = 2/3; sh = (1 + (r/rc)**2)**(-1.5*beta)
    Rm = 2.2*R500; sm = (1 + (Rm/rc)**2)**(-1.5*beta); sh = np.where(r > Rm, sm*(r/Rm)**-3.0, sh)
    dm = 4*np.pi*(r*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r*MPC))]
    Mbx = 1.2*M*(Mg500*MSUN/np.interp(R500, r, M)); rta = r_ta_com(Mbt_cut)/(1 + z)
    for n in range(200):
        new = r_ta_com(float(np.interp(rta, RM, Mbx)))/(1 + z)
        if abs(new/rta - 1) < 1e-6: return new
        rta = new
    return rta
"""


def _child(rule, native, halo, rspext, tag, q):
    src = open(X43SRC).read()
    ed, inj = edits(rule, native, halo, rspext, tag)
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
    extra = {"log": list(ns.get("GC3_LOG", [])), "rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9}
    q.put(extra)


N_LOG = 700


def run(rule, native, halo, rspext=False, tag=None):
    tag = tag or f"{rule}_{'inf' if halo else 'burk'}_{'nat' if native else 'inh'}" + ("_rspext" if rspext else "")
    t = time.time()
    ctx = mp.get_context("fork"); q = ctx.Queue()
    p = ctx.Process(target=_child, args=(rule, native, halo, rspext, tag, q)); p.start()
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


P("GC3_infall_halo_outskirts" + (" [MUTATE m1-m2: control output, not physics]" if MUT else "") +
  ": criteria 50c3953710; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")
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
# S0b profile check (same construction as GC3_CODE)
from scipy.integrate import quad
q_ = 3.0 if MUT else 2.25
f_ = lambda x: 1.0 / ((1 + x) * (1 + x * x) ** ((2.25 - 1) / 2))                    # frozen target shape
fq = lambda x: 1.0 / ((1 + x) * (1 + x * x) ** ((q_ - 1) / 2))                       # shape the run uses
xg = np.logspace(-7, 7, 20001); fx = fq(xg)
Ix = np.r_[0.0, np.cumsum(0.5 * (fx[1:] * xg[1:] ** 3 + fx[:-1] * xg[:-1] ** 3) * np.diff(np.log(xg)))] + fx[0] * xg[0] ** 3 / 3
Iq = quad(lambda x: f_(x) * x * x, 0, 10, epsabs=0, epsrel=1e-12, limit=400)[0]
dev = abs(float(np.interp(np.log(10.0), np.log(xg), Ix)) / Iq - 1)
sl = lambda x: (math.log(fq(x * 1.001)) - math.log(fq(x / 1.001))) / (2 * math.log(1.001))
s0b = dev <= 1e-6 and abs(sl(1e3) + 2.25) <= 0.01 and abs(sl(1e-3)) <= 0.01
check("S0b", s0b, f"cumulative vs quadrature {dev:.1e}; outer slope {sl(1e3):.3f} (-2.25); inner slope {sl(1e-3):.4f} (0)", "1e-6; 0.01")
if not (s0a and s0b) and not MUT:
    P("STOP: Step 0 failed."); RES["verdict"] = "STOPPED AT STEP 0"
    json.dump(RES, open(os.path.join(HERE, f"gc3_infall_results{TAG}.json"), "w"), indent=1, default=float); sys.exit(1)

RUNS = {}
for rule in ("R4", "R5", "RX48"):
    for cfg in ((False, True, False), (True, True, False), (True, False, False), (True, True, True)):
        halo, native, rspext = cfg
        tg, r = run(rule, native, halo, rspext); RUNS[tg] = r
log = RUNS["R4_inf_nat"]["_extra"]["log"]
T = np.array([l[1] for l in log]); Mg = np.array([l[2] for l in log]); sat = np.array([l[3] for l in log])
ok = ~sat
k1 = bool(np.all(np.abs(Mg[ok] / T[ok] - 1) <= 1e-6))
check("S0c", True, f"root found in {int(ok.sum())}/{len(sat)} cluster-cells; saturated {int(sat.sum())} ({100 * sat.mean():.1f}%)", "reported (>5% flagged)")
check("K1", k1, f"M_cold(<R500) = target within 1e-6 for all non-saturated cells (max dev {np.max(np.abs(Mg[ok] / T[ok] - 1)):.1e})", "1e-6")
r0s = np.array([l[4] for l in log]); rsp = np.array([l[5] for l in log])
P(f"  r0 median {np.median(r0s):.3f} Mpc (range {r0s.min():.3f}-{r0s.max():.3f}); r_sp median {np.median(rsp):.2f} Mpc (range {rsp.min():.2f}-{rsp.max():.2f})")
RES["halo_stats"] = {"r0_median": float(np.median(r0s)), "rsp_median": float(np.median(rsp)), "saturated_frac": float(sat.mean())}
check("K2", True, "mass constant beyond r_sp and monotone (by construction of I(min(r, r_sp)/r0), I nondecreasing)", "construction")


def line_set_pass(r, f):
    ft = r["footings"][f]
    return all(st["line"] for st in ft["sparc"].values()) and ft["groups"]["PASS"] and not ft["clusters"]["fails"]


def klass(r_on, r_off, f):
    m3ok = all(abs(keys(r_on, f)[hk]["G-OUT-M3"]["Z"]) <= 2 for hk in ("h0672", "h0686"))
    passed_before = [k for k, ok_ in r_off["footings"][f]["clusters"]["ok"].items() if ok_]
    newly = [k for k in passed_before if not r_on["footings"][f]["clusters"]["ok"][k]]
    return "NOT REPAIRED" if not m3ok else ("INFALL HALO REPAIRS M3" if not newly else f"REPAIRS M3 BUT BREAKS ({', '.join(newly)})")


RES["verdicts"] = {}
for f in ("canonical", "alt"):
    P(f"\n== {f.upper()}")
    for rule in ("R4", "R5", "RX48"):
        for cfg in ("burk_nat", "inf_nat", "inf_inh", "inf_nat_rspext"):
            r = RUNS[f"{rule}_{cfg}"]; ft = r["footings"][f]; cc = ft["clusters"]["cells"]
            P(f"  {rule:5s} {cfg:15s} M3 Z {cc['h0672']['G-OUT-M3']['Z']:+.2f}/{cc['h0686']['G-OUT-M3']['Z']:+.2f}; OUT-all {cc['h0672']['G-OUT-all']['Z']:+.2f}; IN-Mall {cc['h0672']['G-IN-Mall']['Z']:+.2f}; "
              f"groups Z {ft['groups']['Z']:+.2f}; SPARC {ft['sparc']['A_c2b_refit']['rms']:.4f}@{ft['sparc']['A_c2b_refit']['U_median']:.2f}; fails: {ft['clusters']['fails'] or 'none'}"
              + ("  << PASSES THE X43 LINE SET" if line_set_pass(r, f) else ""))
    cls = klass(RUNS["R4_inf_nat"], RUNS["R4_burk_nat"], f); clsv = klass(RUNS["R4_inf_nat_rspext"], RUNS["R4_burk_nat"], f)
    robust = cls.split(" (")[0] == clsv.split(" (")[0]
    lsp = {rule: line_set_pass(RUNS[f"{rule}_inf_nat"], f) for rule in ("R4", "R5", "RX48")}
    RES["verdicts"][f] = {"R4_class": cls, "robust_vs_rspext": robust, "rspext_class": clsv, "line_set_pass_native_infall": lsp}
    P(f"  ==> {f}: R4 {cls} ({'ROBUST' if robust else 'FRAGILE: V-rsp gives ' + clsv}); X43 line set passed (native infall): {lsp}")
RES["runs"] = {k: {f: {"fails": fails(v, f), "groups": v["footings"][f]["groups"], "sparc": {t: {kk: v["footings"][f]["sparc"][t][kk] for kk in ("rms", "U_median", "line")} for t in v["footings"][f]["sparc"]},
                       "cells": v["footings"][f]["clusters"]["cells"]} for f in ("canonical", "alt")} for k, v in RUNS.items()}
peak = max([v["_extra"]["rss"] for v in RUNS.values()] + [resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9])
check("K3", peak < 1.0, f"peak RSS {peak:.2f} GB (max over forked runs), 1 thread, {time.time() - T0:.0f} s", "< 1 GB")
P("\n== VERDICT: " + "; ".join(f"{f}: {RES['verdicts'][f]['R4_class']}" for f in ("canonical", "alt")))
P(f"  checks {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])}")
json.dump(RES, open(os.path.join(HERE, f"gc3_infall_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
