#!/usr/bin/env python3
"""X37_orbit_conversion: does cold dark energy converting to dark energy as exp(-N_orb/N*) survive the cluster bands?

Frozen criteria: FROZEN_CRITERIA.md (204001f8ad); AMENDMENT_A1.md (pre-result: MUTATE bites K1). X30's machinery is
executed read-only up to its STEP 0 (its log redirected here); N* comes from SPARC only (X19, X22). One thread, minutes.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x37_orbit_conversion.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x37_orbit_conversion.py --mutate   -> f = min(exp(+N/N*), 1) (K1 must fail)
"""
import os, sys, csv, json, math, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X30_MUTATE", None)
import numpy as np

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ X30 machinery, read-only, up to its STEP 0
X30SRC = os.path.join(REB, "X30_sheet_cluster_profile", "x30_sheet_cluster_profile.py")
TX = open(X30SRC).read()
cut = TX.index("# ============================================================== STEP 0")
code = TX[:cut]
old = 'OUTF = open(os.path.join(HERE, f"x30_sheet_cluster_profile{TAG}.out"), "w")'
assert code.count(old) == 1
code = code.replace(old, f'OUTF = open({os.path.join(HERE, "x37_x30_machinery" + TAG + ".log")!r}, "w")')
NS = {"__file__": X30SRC, "__name__": "x30_ro"}
argv0 = sys.argv; sys.argv = [X30SRC]
exec(compile(code, X30SRC, "exec"), NS)
sys.argv = argv0
for k in ("np", "math", "FEET", "HK", "CELLS", "BN", "M", "MEAS", "DC", "I", "TID", "T3M", "ALLI", "N", "X1m", "wls1", "bsum", "dvec",
          "prep", "gfun", "PREP", "RG", "RM", "MPC", "MSUN", "G", "X7J", "X22J", "rss"):
    globals()[k] = NS[k]
P(f"X37_orbit_conversion  {'MUTATE run (f = min(exp(+N/N*), 1))' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy (w ~ 0, not matter); raw eRASS1 x KiDS bands via X30's machinery (read-only); not theory closed")
P(f"X30 machinery executed up to STEP 0 [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ N* from SPARC (frozen section 1)
X19 = list(csv.DictReader(open(os.path.join(REB, "X19_selector_rank_test", "x19_classes.csv"))))
N16 = min(float(r["N_orb_p16"]) for r in X19 if r["class"] in ("SPARC small", "SPARC large") and r["footing"] == "canonical")
CAP = float(X22J["step3A"]["canonical"]["alpha_NF"]["captured_T2_min_p16_p50_p84_max"][2])
FMAX = {f: float(X22J["step2"]["per_footing"][f]["f_max"]) for f in FEET}
NSTAR = {f: N16 / math.log(CAP / FMAX[f]) for f in FEET}
P(f"N16 (SPARC, X19) {N16:.3f}; cap (X22 alpha_NF median) {CAP:.4f}; f_max {FMAX}; N* = {({f: round(v, 3) for f, v in NSTAR.items()})}")
TAGE = 13.8e9 * 365.25 * 86400.0

def retained_mass(i, foot, hk, nstar, slope=2.25):
    """M_c(<r) on X30's grid: rho0 ~ r^-slope inside r_ta, M0(<r_ta) = Mfair; f = exp(-N_orb/N*) (or the mutation)."""
    pp = prep(i, foot, hk); rta, Mf = pp["rta"], pp["Mfair"]; e = 3.0 - slope
    u = np.minimum(RM / rta, 1.0) ** e                                        # M0(<r)/Mf = (r/rta)^(3-slope)
    M0 = Mf * u
    g = gfun(pp["Mb"] + M0, foot); V = np.sqrt(g * RM); Norb = TAGE * V / (2 * math.pi * RM)
    if nstar == float("inf"):
        fr = np.ones_like(RM)
    elif nstar == 0.0:
        fr = np.zeros_like(RM) if not MUTATE else np.ones_like(RM)
    else:
        fr = np.minimum(np.exp(+Norb / nstar), 1.0) if MUTATE else np.exp(-Norb / nstar)
    # A2 (post-result, implementation): no zeroing outside r_ta; du = 0 there already (u capped at 1), so the edge cell is no longer half-weighted
    du = np.diff(np.r_[0.0, u]); fm = np.r_[fr[0], 0.5 * (fr[1:] + fr[:-1])]
    Mc = Mf * np.cumsum(fm * du)
    return Mc, Norb, Mf

def grade(foot, nstar, slope=2.25, label=""):
    out = {}
    for hk in HK:
        V = np.zeros((N, 8)); prof = []
        for i in ALLI:
            Mc, Norb, Mf = retained_mass(int(i), foot, hk, nstar, slope)
            V[i] = dvec(int(i), foot, hk, Mc)
            if int(i) in set(I.tolist()):
                tot = float(Mc[-1])
                prof.append(dict(ret=tot / Mf, f015=float(np.interp(0.15, RG, Mc)) / max(tot, 1e-300), f05=float(np.interp(0.5, RG, Mc)) / max(tot, 1e-300),
                                 N_at_0548=float(np.interp(0.548, RG, Norb))))
        PREP.clear()
        cl = f"{foot}|{hk}"; o = M[cl]; vB = bsum(V); vC = bsum(DC[(foot, hk)])
        kt, ktC = vB[I], vC[I]; g = {}
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
        r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]
        Am = [[float(vB[T3M == t, bi].sum() / vC[T3M == t, bi].sum()) for t in range(3)] for bi in range(3)]
        Aall = [float(vB[:, bi].sum() / vC[:, bi].sum()) for bi in range(3)]
        g["G-OUT-Mall"] = (a7["OUTER"]["A_CAL"], a7["OUTER"]["s_CAL"], Aall[2])
        for t in range(3): g[f"G-OUT-M{t+1}"] = (r7[t]["OUTER"]["A_CAL"], r7[t]["OUTER"]["s_CAL"], Am[2][t])
        g["G-IN-Mall"] = (o["M_all|INNER"]["A"], o["M_all|INNER"]["s_IN"], Aall[0])
        out[hk] = dict(keys={k: dict(meas=v[0], s=v[1], pred=v[2], Z=(v[0] - v[2]) / v[1]) for k, v in g.items()},
                       prof={f"T{t+1}": {k: float(np.median([p[k] for p, tt in zip(prof, TID) if tt == t])) for k in ("ret", "f015", "f05", "N_at_0548")} for t in range(3)},
                       MID_all_pred=float(kt[:, 1].sum() / ktC[:, 1].sum()))
    keys = list(out["h0672"]["keys"])
    ok = {k: all(abs(out[hk]["keys"][k]["Z"]) <= 2 for hk in HK) for k in keys}
    bad = [k for k in keys if not ok[k]]
    if not bad: cls = "OC PASSES CLUSTERS"
    elif all(k in ("G-IN-all", "G-IN-Mall") for k in bad): cls = "OC INNER-ONLY"
    else:
        sgn = {k: ("OVER" if out["h0672"]["keys"][k]["pred"] > out["h0672"]["keys"][k]["meas"] else "UNDER") for k in bad}
        cls = "OC FAILS CLUSTERS: " + ", ".join(f"{k} ({sgn[k]})" for k in bad)
    return dict(cells=out, ok=ok, fails=bad, cls=cls)

def show(f, gr, tag):
    c0, c1 = gr["cells"]["h0672"]["keys"], gr["cells"]["h0686"]["keys"]
    P(f"  [{f}] {tag}: {gr['cls']}")
    for k in c0:
        P(f"     {k:10s} meas {c0[k]['meas']:+.3f}+-{c0[k]['s']:.3f} pred {c0[k]['pred']:+.3f} Z {c0[k]['Z']:+.2f} | h0.686 pred {c1[k]['pred']:+.3f} Z {c1[k]['Z']:+.2f}"
          + ("" if gr["ok"][k] else "  FAIL"))
    pr = gr["cells"]["h0672"]["prof"]
    P("     profile (KT tercile medians, h0.672): " + "; ".join(f"{t}: retained {v['ret']:.3f} of fair share, f(<0.15) {v['f015']:.3f}, f(<0.5) {v['f05']:.3f}, N_orb(0.548) {v['N_at_0548']:.2f}" for t, v in pr.items()))
    P(f"     MID all-KT pred {gr['cells']['h0672']['MID_all_pred']:.3f} (meas {M[f'{f}|h0672']['KT_all|MID']['A']:.3f})")

RES = dict(frozen="204001f8ad", amendment="A1 pre-result (MUTATE bites K1)", mutate=MUTATE, N16=N16, cap=CAP, f_max=FMAX, N_star=NSTAR, footings={}, checks={})
checks = []
# K0
o = M["canonical|h0672"]
k0a = abs(o["KT_all|OUTER"]["A"] - 0.72) < 0.006 and abs(o["KT_all|MID"]["A"] - 1.67) < 0.006
v0 = dvec(0, "canonical", "h0672", None); PREP.clear(); k0b = float(np.max(np.abs(v0 - DC[("canonical", "h0672")][0]))) == 0.0
k0 = k0a and k0b
P(f"K0 X30 measured KT-all OUTER {o['KT_all|OUTER']['A']:.4f} / MID {o['KT_all|MID']['A']:.4f} (README 0.72 / 1.67); C* vector exact {k0b}: {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0))
# K1
Mi, _, Mf = retained_mass(0, "canonical", "h0672", float("inf")); k1a = abs(Mi[-1] / Mf - 1) < 1e-6
M0z, _, _ = retained_mass(0, "canonical", "h0672", 0.0); vz = dvec(0, "canonical", "h0672", M0z); PREP.clear()
k1b = float(np.max(np.abs(vz - DC[("canonical", "h0672")][0]))) == 0.0
k1 = k1a and k1b
P(f"K1 N* -> inf retains the fair share ({Mi[-1] / Mf:.8f}); N* -> 0 returns C* exactly ({k1b}): {'PASS' if k1 else 'FAIL'}"); checks.append(("K1", k1))
# K2 closed form vs quadrature, f = 1
pp = prep(0, "canonical", "h0672"); rta = pp["rta"]; u = np.minimum(RM / rta, 1.0) ** 0.75
Mq = pp["Mfair"] * np.cumsum(np.diff(np.r_[0.0, u])); Mcf = pp["Mfair"] * u; PREP.clear()
k2 = float(np.max(np.abs(Mq - Mcf)) / pp["Mfair"]) < 1e-6
P(f"K2 r^-9/4 closed form vs quadrature (f = 1): {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

for f in FEET:
    P(f"\n=== [{f}] N* = {NSTAR[f]:.3f}")
    gr = grade(f, NSTAR[f]); show(f, gr, "PRIMARY r^-9/4")
    rep = {}
    for tag, ns, sl in (("r^-2 variant", NSTAR[f], 2.0), ("N* x 1/2", NSTAR[f] / 2, 2.25), ("N* x 2", NSTAR[f] * 2, 2.25)):
        g2 = grade(f, ns, sl); rep[tag] = dict(cls=g2["cls"], fails=g2["fails"],
                                             OUT_all_pred=g2["cells"]["h0672"]["keys"]["G-OUT-all"]["pred"], MID_all_pred=g2["cells"]["h0672"]["MID_all_pred"])
        P(f"  (reported) {tag}: {g2['cls']}; OUTER all pred {rep[tag]['OUT_all_pred']:.3f}, MID all pred {rep[tag]['MID_all_pred']:.3f}")
    RES["footings"][f] = dict(primary=gr, reported=rep, verdict=gr["cls"])
    P(f"  VERDICT [{f}]: {gr['cls']}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

base = {f: RES["footings"][f]["verdict"].split(":")[0] for f in FEET}
RES["verdict"] = (RES["footings"]["canonical"]["verdict"] if base["canonical"] == base["alt"] else f"UNDECIDED (footings disagree: {base})")
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
checks.append(("K3", rss() < 2.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x37_orbit_conversion{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x37_orbit_conversion_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
