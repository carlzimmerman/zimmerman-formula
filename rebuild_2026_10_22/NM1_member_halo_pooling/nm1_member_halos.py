#!/usr/bin/env python3
"""NM1_member_halo_pooling -- frozen criteria FROZEN_CRITERIA.md (f78650692e).

X38's machinery (EM1 + X30, read-only, up to X38's K0) is executed in a namespace; the cluster halo is split into the
members' a0-cored halos (distributed like cluster galaxies, NFW c_g) plus X38's Burkert halo for the rest.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 nm1_member_halos.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 nm1_member_halos.py --mutate   -> no nesting (must equal X38)
"""
import os, sys, io, json, math, time, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.integrate import quad

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ---- X38 machinery up to its K0 (read-only; X38 in its normal mode)
X38SRC = os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos.py"); TX = open(X38SRC).read()
code = TX[:TX.index("# K0")]
code = code.replace('os.path.join(HERE, "x38_x30_machinery" + TAG + ".log")', repr(os.path.join(HERE, "nm1_x30_machinery.log")))
NS = {"__file__": X38SRC, "__name__": "x38_ro"}; argv0 = sys.argv; sys.argv = [X38SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, X38SRC, "exec"), NS)
sys.argv = argv0
for k in ("B", "solve_r0", "SIG", "FEET", "HK", "BN", "M", "DC", "I", "TID", "T3M", "ALLI", "N", "X1m", "wls1", "bsum",
          "prep", "PREP", "RM", "X7J", "GE", "MSUNE", "NX"):
    globals()[k] = NS[k]
O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
P(f"NM1_member_halo_pooling {'MUTATE (no nesting)' if MUTATE else 'normal run'}  (frozen f78650692e)")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; not theory closed")

# ---- member share R from X38's halo relation over a Schechter SMF
def Rratio(a, b, lMs=10.9, alpha=-1.2):
    phi = lambda lm: (10 ** (lm - lMs)) ** (alpha + 1) * math.exp(-10 ** (lm - lMs))      # dn/dlog m (shape)
    num = quad(lambda lm: phi(lm) * 10 ** (a + b * (lm - 10)), 8, 13, limit=400, epsrel=1e-11)[0]
    den = quad(lambda lm: phi(lm) * 10 ** lm, 8, 13, limit=400, epsrel=1e-11)[0]
    return num / den
def Rratio_grid(a, b, lMs=10.9, alpha=-1.2, n=200001):
    lm = np.linspace(8, 13, n); phi = (10 ** (lm - lMs)) ** (alpha + 1) * np.exp(-10 ** (lm - lMs))
    return np.trapz(phi * 10 ** (a + b * (lm - 10)), lm) / np.trapz(phi * 10 ** lm, lm)

def nfw_frac(r, rmax, c):
    m = lambda x: np.log1p(x) - x / (1 + x)
    return m(c * np.minimum(r, rmax) / rmax) / m(c)

def halo_mass(i, foot, hk, Rm, cg):
    pp = prep(i, foot, hk); Mfair = pp["Mfair"]; rta = pp["rta"]
    Mmem = 0.0 if (MUTATE or Rm == 0) else min(Rm * float(pp["Mb"][-1]) / 6.0, Mfair)
    Mrest = Mfair - Mmem
    r0 = solve_r0(Mrest, rta, SIG[foot])
    Mh = math.pi * SIG[foot] * r0 ** 2 * B(np.minimum(RM, rta) / r0)
    if Mmem > 0: Mh = Mh + Mmem * nfw_frac(RM, rta, cg)
    return Mh, Mmem / Mfair

def dvecN(i, foot, hk, Msrc):
    pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
    So = O_(P_(rho), pp["dmpc"]); Pp = A_(DS_(So)) / KG; fr, _ = RF(hk, i, SB(So)); return DAT[hk]["W"][i] * (Pp * fr)

def grade(foot, Rm, cg):
    out = {}; fm = []
    for hk in HK:
        V = np.zeros((N, 8))
        for i in ALLI:
            Mh, f = halo_mass(int(i), foot, hk, Rm, cg); fm.append(f)
            V[i] = dvecN(int(i), foot, hk, prep(int(i), foot, hk)["Mb"] + Mh)
        PREP.clear()
        o = M[f"{foot}|{hk}"]; vB = bsum(V); vC = bsum(DC[(foot, hk)]); kt, ktC = vB[I], vC[I]; g = {}
        for bi, b in enumerate(BN):
            At = [float(kt[TID == t, bi].sum() / ktC[TID == t, bi].sum()) for t in range(3)]; Aa = float(kt[:, bi].sum() / ktC[:, bi].sum())
            bp = float(wls1(kt[:, bi], ktC[:, bi], X1m)[1])
            if b == "MID":
                for t in range(3): g[f"G-MID-T{t+1}"] = (o["KT_terc|MID"][t]["A"], o["KT_terc|MID"][t]["s"], At[t])
                g["G-MID-b"] = (o["KT_b|MID"]["b"], o["KT_b|MID"]["s_b"], bp)
            if b == "OUTER":
                g["G-OUT-all"] = (o["KT_all|OUTER"]["A"], o["KT_all|OUTER"]["s"], Aa)
                for t in range(3): g[f"G-OUT-T{t+1}"] = (o["KT_terc|OUTER"][t]["A"], o["KT_terc|OUTER"][t]["s"], At[t])
                g["G-OUT-b"] = (o["KT_b|OUTER"]["b"], o["KT_b|OUTER"]["s_b"], bp)
            if b == "INNER":
                g["G-IN-all"] = (o["KT_all|INNER"]["A"], o["KT_all|INNER"]["s_IN"], Aa)
        cl = f"{foot}|{hk}"; r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]
        Am = [[float(vB[T3M == t, bi].sum() / vC[T3M == t, bi].sum()) for t in range(3)] for bi in range(3)]
        Aall = [float(vB[:, bi].sum() / vC[:, bi].sum()) for bi in range(3)]
        g["G-OUT-Mall"] = (a7["OUTER"]["A_CAL"], a7["OUTER"]["s_CAL"], Aall[2])
        for t in range(3): g[f"G-OUT-M{t+1}"] = (r7[t]["OUTER"]["A_CAL"], r7[t]["OUTER"]["s_CAL"], Am[2][t])
        g["G-IN-Mall"] = (o["M_all|INNER"]["A"], o["M_all|INNER"]["s_IN"], Aall[0])
        out[hk] = {k: dict(meas=v[0], s=v[1], pred=v[2], Z=(v[0] - v[2]) / v[1]) for k, v in g.items()}
    ok = {k: all(abs(out[hk][k]["Z"]) <= 2 for hk in HK) for k in out["h0672"]}
    return out, ok, float(np.median(fm))

checks = []
# K1
ra, rg = Rratio(11.18, 0.9), Rratio_grid(11.18, 0.9)
x = np.linspace(1e20, 3e22, 7); k1 = abs(nfw_frac(np.array([3e22]), 3e22, 2.9)[0] - 1) < 1e-8 and abs(ra / rg - 1) < 1e-6
P(f"K1 R (bg A) quad {ra:.5f} vs grid {rg:.5f}; NFW normalisation ok: {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))
RES = dict(frozen="f78650692e", mutate=MUTATE, R_bgA=ra, footings={}, checks={})
classes = {}
for foot in FEET:
    x38c = X38J["footings"][foot]["clusters"]["cells"]; x38ok = X38J["footings"][foot]["clusters"]["ok"]
    if foot == "canonical" or MUTATE:
        c0, _, _ = grade(foot, 0.0, 2.9)                              # K0 / MUTATE reproduction of X38
        d0 = max(abs(c0["h0672"][k]["pred"] - x38c["h0672"][k]["pred"]) for k in c0["h0672"])
        k0 = d0 < 1e-6
        P(f"[{foot}] {'MUTATE no-nesting' if MUTATE else 'K0 M_mem = 0'} vs X38 max |dpred| {d0:.2e}: {'PASS' if k0 else 'FAIL'}")
        checks.append((f"K0[{foot}]", k0))
        if MUTATE: continue
    cells, ok, fmem = grade(foot, ra, 2.9)
    failing38 = [k for k in x38ok if not x38ok[k]]
    sumZ38 = sum(max(abs(x38c[h][k]["Z"]) for h in HK) for k in failing38)
    sumZ = sum(max(abs(cells[h][k]["Z"]) for h in HK) for k in failing38)
    newfail = [k for k in ok if x38ok.get(k, True) and not ok[k]]
    cls = "NM PASSES CLUSTERS" if all(ok.values()) else ("NM IMPROVES" if not newfail and sumZ <= 0.5 * sumZ38 else "NM FAILS")
    classes[foot] = cls
    P(f"\n=== [{foot}] member share M_mem/M_fair median {fmem:.3f}; R {ra:.2f}")
    for k in cells["h0672"]:
        a, b_ = cells["h0672"][k], x38c["h0672"][k]
        P(f"   {k:10s} meas {a['meas']:+.3f}+-{a['s']:.3f} pred {a['pred']:+.3f} Z {a['Z']:+.2f} (X38 pred {b_['pred']:+.3f} Z {b_['Z']:+.2f})"
          + ("" if ok[k] else "  FAIL"))
    P(f"   X38-failing cells summed |Z|: {sumZ38:.2f} -> {sumZ:.2f}; new failures: {newfail or 'none'}")
    P(f"   CLASS [{foot}]: {cls}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    var = {}
    for lab, kw in (("c_g 2.0", dict(cg=2.0, Rm=ra)), ("c_g 4.0", dict(cg=4.0, Rm=ra)),
                    ("alpha -1.0", dict(cg=2.9, Rm=Rratio(11.18, 0.9, alpha=-1.0))), ("alpha -1.4", dict(cg=2.9, Rm=Rratio(11.18, 0.9, alpha=-1.4))),
                    ("bg B", dict(cg=2.9, Rm=Rratio(11.2, 0.9)))):
        cv, okv, fv = grade(foot, kw["Rm"], kw["cg"])
        var[lab] = dict(fails=[k for k in okv if not okv[k]], MID_T3_Z=cv["h0672"]["G-MID-T3"]["Z"], MID_b_Z=cv["h0672"]["G-MID-b"]["Z"],
                        OUT_M3_Z=cv["h0672"]["G-OUT-M3"]["Z"], fmem=fv)
        P(f"   variant {lab}: fmem {fv:.3f}; MID T3 Z {var[lab]['MID_T3_Z']:+.2f}, MID b Z {var[lab]['MID_b_Z']:+.2f}, OUT M3 Z {var[lab]['OUT_M3_Z']:+.2f}; fails {var[lab]['fails']}")
    RES["footings"][foot] = dict(cls=cls, fmem=fmem, cells=cells, ok=ok, sumZ_x38=sumZ38, sumZ=sumZ, new_fail=newfail, variants=var)

if not MUTATE:
    RES["verdict"] = classes["canonical"] if classes["canonical"] == classes["alt"] else f"UNDECIDED (footings disagree: {classes})"
    P(f"\n=== VERDICT: {RES['verdict']}")
checks.append(("K2", rss() < 2.0))
n = sum(ok for _, ok in checks); P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks)
                                  + f"; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
RES["checks"] = {k: bool(v) for k, v in checks}
open(os.path.join(HERE, f"nm1_member_halos{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"nm1_member_halos_results{TAG}.json"), "w"), indent=1, default=float)
if MUTATE: sys.exit(1 if n == len(checks) else 0)
sys.exit(0 if n == len(checks) else 1)
