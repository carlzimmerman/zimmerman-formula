#!/usr/bin/env python3
"""SC1_self_coupled_core_law -- frozen criteria FROZEN_CRITERIA.md (b5e95b9c9e).

X38's route-E Burkert halos with a per-system core surface density Sigma_i = Sigma_a0 (sigma_i/sigma_ref)^q, q = 1/3.
X38's machinery (EM1 + X30, read-only, up to X38's K0) runs in a namespace.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 sc1_core_law.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 sc1_core_law.py --mutate   -> sigma = sigma_ref everywhere (= X38)
"""
import os, sys, io, json, math, time, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

X38SRC = os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos.py"); TX = open(X38SRC).read()
code = TX[:TX.index("# K0")]
code = code.replace('os.path.join(HERE, "x38_x30_machinery" + TAG + ".log")', repr(os.path.join(HERE, "sc1_x30_machinery.log")))
NS = {"__file__": X38SRC, "__name__": "x38_ro"}; argv0 = sys.argv; sys.argv = [X38SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, X38SRC, "exec"), NS)
sys.argv = argv0
for k in ("B", "solve_r0", "SIG", "SAT", "FEET", "HK", "BN", "M", "DC", "I", "TID", "T3M", "ALLI", "N", "X1m", "wls1", "bsum",
          "prep", "PREP", "RM", "X7J", "GE", "MSUNE", "MPCE", "NX", "GALS", "fit_one", "pooled", "line", "LAW"):
    globals()[k] = NS[k]
O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
P(f"SC1_self_coupled_core_law {'MUTATE (sigma = sigma_ref)' if MUTATE else 'normal run'}  (frozen b5e95b9c9e)")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; not theory closed")

# ---- dispersions (X19 V2)
SIG_G = np.array([float(q["Vobs"][q["Vobs"] > 0][-1]) / math.sqrt(2) for q in GALS])          # km/s
SREF = float(np.median(SIG_G))
KT = np.asarray(NX["KT"], float); SKT = np.full(N, np.nan)
okk = np.isfinite(KT) & (KT > 0); SKT[okk] = np.sqrt(KT[okk] * NX["KEV"] / (0.6 * NX["MP"])) / 1e3
fill = SKT.copy()
for t in range(3):
    m = T3M == t; fill[m & ~okk] = float(np.nanmedian(SKT[m & okk]))
SIG_C = fill
k1 = abs(float(np.median(SKT[I])) - 517.1) <= 0.5
P(f"sigma_ref (median SPARC V_last/sqrt2) = {SREF:.2f} km/s over {len(GALS)} galaxies; SPARC sigma 5/50/95%: "
  + " / ".join(f"{v:.0f}" for v in np.percentile(SIG_G, [5, 50, 95])))
P(f"K1 median sigma_KT {np.median(SKT[I]):.2f} km/s (517.1 +- 0.5): {'PASS' if k1 else 'FAIL'}; clusters filled by tercile: {int((~okk).sum())}")

def sig_factor(s, q):
    return 1.0 if MUTATE else (s / SREF) ** q

def sparc(f, a, b, h, q):
    rc = 3 * (100 * h * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []
    for j, g in enumerate(GALS):
        lM = a + b * (g["lMb"] - 10); M200 = 10 ** lM * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
        Sg = SIG[f] * sig_factor(SIG_G[j], q)
        r0 = solve_r0(M200, R200, Sg); gh = GE * math.pi * Sg * r0 ** 2 * B(g["Rm"] / r0) / g["Rm"] ** 2
        rows.append(fit_one(g, np.log10(np.maximum(g["GB"] + gh[:, None], 1e-300))))
    return pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])

def dvecN(i, foot, hk, Msrc):
    pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
    So = O_(P_(rho), pp["dmpc"]); Pp = A_(DS_(So)) / KG; fr, _ = RF(hk, i, SB(So)); return DAT[hk]["W"][i] * (Pp * fr)

def grade(foot, q, age=1.0):
    out = {}
    for hk in HK:
        V = np.zeros((N, 8))
        for i in ALLI:
            pp = prep(int(i), foot, hk); Sg = SIG[foot] * sig_factor(SIG_C[i], q) * (age if not MUTATE else 1.0)
            r0 = solve_r0(pp["Mfair"], pp["rta"], Sg)
            Mh = math.pi * Sg * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
            V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)
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
    return out, ok

checks = [("K1", k1)]
RES = dict(frozen="b5e95b9c9e", mutate=MUTATE, sigma_ref=SREF, footings={})
classes = {}
for foot in FEET:
    x38 = X38J["footings"][foot]; x38c = x38["clusters"]["cells"]; x38ok = x38["clusters"]["ok"]
    if MUTATE:
        c0, _ = grade(foot, 1 / 3)
        d0 = max(abs(c0["h0672"][k]["pred"] - x38c["h0672"][k]["pred"]) for k in c0["h0672"])
        s0 = {t: sparc(foot, bg["a"], bg["b"], bg["h"], 1 / 3) for t, bg in BGS.items()}
        ds = max(abs(s0[t]["rms"] - x38["sparc"][t]["rms"]) for t in BGS)
        okm = d0 < 1e-6 and ds < 1e-9
        P(f"[{foot}] MUTATE (sigma = sigma_ref): cluster |dpred| {d0:.1e}, SPARC |drms| {ds:.1e} vs X38: {'REPRODUCES' if okm else 'DIFFERS'}")
        checks.append((f"MUT[{foot}]", okm)); continue
    # K0
    c0, _ = grade(foot, 0.0)
    d0 = max(abs(c0["h0672"][k]["pred"] - x38c["h0672"][k]["pred"]) for k in c0["h0672"])
    s0 = {t: sparc(foot, bg["a"], bg["b"], bg["h"], 0.0) for t, bg in BGS.items()}
    ds = max(max(abs(s0[t]["rms"] - x38["sparc"][t]["rms"]), abs(s0[t]["U_median"] - x38["sparc"][t]["U_median"])) for t in BGS)
    k0 = d0 < 1e-6 and ds < 1e-9
    P(f"\n=== [{foot}] K0 q = 0 vs X38: cluster |dpred| {d0:.1e}, SPARC |d| {ds:.1e}: {'PASS' if k0 else 'FAIL'}")
    checks.append((f"K0[{foot}]", k0))
    # primary q = 1/3
    sp = {t: sparc(foot, bg["a"], bg["b"], bg["h"], 1 / 3) for t, bg in BGS.items()}
    spass = all(line(v) for v in sp.values())
    for t, v in sp.items():
        P(f"   SPARC [{t}] rms {v['rms']:.4f}, median U {v['U_median']:.2f} -> line {'PASS' if line(v) else 'FAIL'}   (X38 {x38['sparc'][t]['rms']:.4f} @ {x38['sparc'][t]['U_median']:.2f})")
    cells, ok = grade(foot, 1 / 3)
    for k in cells["h0672"]:
        a, b_ = cells["h0672"][k], x38c["h0672"][k]
        P(f"   {k:10s} meas {a['meas']:+.3f}+-{a['s']:.3f} pred {a['pred']:+.3f} Z {a['Z']:+.2f} (X38 pred {b_['pred']:+.3f} Z {b_['Z']:+.2f})" + ("" if ok[k] else "  FAIL"))
    failing38 = [k for k in x38ok if not x38ok[k]]
    sZ38 = sum(max(abs(x38c[h][k]["Z"]) for h in HK) for k in failing38)
    sZ = sum(max(abs(cells[h][k]["Z"]) for h in HK) for k in failing38)
    newfail = [k for k in ok if x38ok.get(k, True) and not ok[k]]
    if not spass: cls = "SC FAILS SPARC"
    elif all(ok.values()): cls = "SC PASSES"
    elif not newfail and sZ <= 0.5 * sZ38: cls = "SC PASSES SPARC, IMPROVES CLUSTERS"
    else: cls = "SC PASSES SPARC ONLY"
    classes[foot] = cls
    terc = {f"T{t+1}": float(np.median((SIG_C[I][TID == t] / SREF) ** (1 / 3))) for t in range(3)}
    P(f"   cluster Sigma/Sigma_a0 by KT tercile (median): {terc}; X38-failing summed |Z| {sZ38:.2f} -> {sZ:.2f}; new fails {newfail or 'none'}")
    P(f"   CLASS [{foot}]: {cls}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    rep = {}
    for lab, q, age in (("age 0.5 (x sqrt2)", 1 / 3, math.sqrt(2)), ("q 1/4", 1 / 4, 1.0), ("q 1/2", 1 / 2, 1.0)):
        cv, okv = grade(foot, q, age)
        spv = {t: sparc(foot, bg["a"], bg["b"], bg["h"], q) for t, bg in BGS.items()} if age == 1.0 else sp
        rep[lab] = dict(sparc={t: dict(rms=v["rms"], U=v["U_median"], line=line(v)) for t, v in spv.items()},
                        fails=[k for k in okv if not okv[k]], MID_T3_Z=cv["h0672"]["G-MID-T3"]["Z"], MID_b_Z=cv["h0672"]["G-MID-b"]["Z"],
                        OUT_M3_Z=cv["h0672"]["G-OUT-M3"]["Z"])
        P(f"   reported {lab}: SPARC " + ", ".join(f"{t[:1]} {v['rms']:.4f}@{v['U']:.2f}{'' if v['line'] else ' FAIL'}" for t, v in rep[lab]["sparc"].items())
          + f"; MID T3 Z {rep[lab]['MID_T3_Z']:+.2f}, MID b Z {rep[lab]['MID_b_Z']:+.2f}, OUT M3 Z {rep[lab]['OUT_M3_Z']:+.2f}; fails {rep[lab]['fails']}")
    RES["footings"][foot] = dict(cls=cls, sparc={t: dict(rms=v["rms"], U=v["U_median"], line=line(v)) for t, v in sp.items()},
                                 cells=cells, ok=ok, sumZ_x38=sZ38, sumZ=sZ, new_fail=newfail, tercile_Sigma=terc, reported=rep)

if not MUTATE:
    RES["verdict"] = classes["canonical"] if classes["canonical"] == classes["alt"] else f"UNDECIDED (footings disagree: {classes})"
    P(f"\n=== VERDICT: {RES['verdict']}")
checks.append(("K2", rss() < 2.0))
n = sum(v for _, v in checks); P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks)
                                + f"; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
RES["checks"] = {k: bool(v) for k, v in checks}
open(os.path.join(HERE, f"sc1_core_law{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"sc1_core_law_results{TAG}.json"), "w"), indent=1, default=float)
if MUTATE: sys.exit(1 if n == len(checks) else 0)
sys.exit(0 if n == len(checks) else 1)
