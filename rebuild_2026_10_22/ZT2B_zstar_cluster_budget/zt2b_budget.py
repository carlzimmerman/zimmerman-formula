#!/usr/bin/env python3
"""ZT2B_zstar_cluster_budget: is Z-star's cluster-core failure a profile or a budget problem?
Z-T2's committed script is exec'd from its source with only the free-excess profile patched: NFW (control), PM (free excess as a
central Plummer, r_c 10 kpc), ALLPM (all supply S as a central Plummer).  A central mass bounds the MID lift of any profile of the
same mass (lemma, check KL).

Criteria: FROZEN_CRITERIA.md (12df931233, committed alone first).  kappa = 1/2 FITTED.  Not "theory closed".
Run:   OMP_NUM_THREADS=1 nice -n 15 python3 zt2b_budget.py [--mutate]      (runs the three modes as subprocesses, then summarises)
"""
import os, sys, json, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
ZT2 = os.path.join(REB, "ZT_zstar_tests", "zt2_cluster_terciles.py")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
MODES = ("NFW", "PM", "ALLPM")
LADDER = ("NFWx2", "NFWx4", "NFWx8", "NFWx16")       # reported: concentration needed (frozen sec. Classes)


def patched(mode):
    s = open(ZT2).read()
    reps = [
        ("        shape, dm = DEB[key]; Mf = Ef * shape\n",
         "        shape, dm = DEB[key]; Mf = Ef * (shape if MODE == 'NFW' else (cshape(dm, float(MODE[4:])) if MODE.startswith('NFWx') else PLUM))\n"
         "        meta['deb_c'] = float(dm['c'])\n"),
        ("    rich = Ro < rs\n",
         "    rich = Ro < rs\n    if MODE == 'ALLPM' and not inactive:\n"
         "        return Mb + S * PLUM, Mb, Mlaw, dict(R_own=Ro, r_s=rs, rich=bool(rich), Mb_own=Mb_own / MSUN, S=S / MSUN)\n"),
        ("DEB = {}\n", "DEB = {}\n"
         "def cshape(dm, sc):                                          # ZT2B ladder: CFG930's NFW with c -> sc c (same r_b)\n"
         "    m_ = lambda x: np.log1p(x) - x / (1 + x); rs = dm['rs'] / sc; rb = dm['rb']\n"
         "    return m_(np.minimum(RG * 1000.0, rb) / rs) / m_(rb / rs)\n"
         "PLUM = RG ** 3 / (RG ** 2 + 0.01 ** 2) ** 1.5           # ZT2B: central Plummer, r_c = 10 kpc, M(<r)/M\n"),
        ('f"zt2_cluster_terciles{TAG}.out"', 'f"zt2b_{MODE}{TAG}.out"'),
        ('f"zt2_cluster_terciles_results{TAG}.json"', 'f"zt2b_{MODE}_results{TAG}.json"'),
        ("sys.exit(0 if npass == len(CHECKS) else 1)", "ZT2_EXIT = 0 if npass == len(CHECKS) else 1"),
    ]
    for a, b in reps:
        assert s.count(a) == 1, (mode, a)
        s = s.replace(a, b)
    return s


if "--mode" in sys.argv:
    mode = sys.argv[sys.argv.index("--mode") + 1]
    ns = {"__file__": os.path.join(HERE, "zt2_cluster_terciles.py"), "__name__": "zt2b", "MODE": mode}
    sys.argv = [ns["__file__"]] + (["--mutate"] if MUT else [])
    exec(compile(patched(mode), ZT2, "exec"), ns)
    out = {"exit": ns["ZT2_EXIT"]}
    if mode == "NFW":                                   # KL: the lemma on one real cluster, canonical, h 0.672, 200c / cap
        i = int(np.argmax([c["Mgas500"] for c in ns["CL"]])); cl = ns["CL"][i]
        Mt, Mb, Ml, meta = ns["zstar_mass"](i, cl, "canonical", "h0672", "P", "200c", "cap")
        m = 1e14 * ns["MSUN"]
        key = [k for k in ns["DEB"] if k[0] == i][0]; shape = ns["DEB"][key][0]
        Pn = ns["project"](i, cl, "canonical", "h0672", Mb + m * shape, False)[0]
        Pp = ns["project"](i, cl, "canonical", "h0672", Mb + m * ns["PLUM"], False)[0]
        P0 = ns["project"](i, cl, "canonical", "h0672", Mb, False)[0]
        mid = [3, 4, 5]
        out["KL"] = dict(lift_nfw=(Pn - P0)[mid].tolist(), lift_pm=(Pp - P0)[mid].tolist(), ok=bool(np.all((Pp - P0)[mid] >= (Pn - P0)[mid])))
    json.dump(out, open(os.path.join(HERE, f"zt2b_{mode}_exit{TAG}.json"), "w"))
    sys.exit(0)

env = dict(os.environ, OMP_NUM_THREADS="1")
for mode in MODES + (() if MUT else LADDER):
    subprocess.run([sys.executable, os.path.abspath(__file__), "--mode", mode] + (["--mutate"] if MUT else []), check=True, env=env)
R = {m: json.load(open(os.path.join(HERE, f"zt2b_{m}_results{TAG}.json"))) for m in MODES}
X = {m: json.load(open(os.path.join(HERE, f"zt2b_{m}_exit{TAG}.json"))) for m in MODES}
L = []
P = lambda s="": (print(s, flush=True), L.append(str(s)))
ZJ = json.load(open(os.path.join(REB, "ZT_zstar_tests", "zt2_cluster_terciles_results.json")))
rep = 0.0
for k, row in ZJ["runs"].items():
    for t in ("T1", "T2", "T3"):
        for b in ("MID", "OUTER"):
            for q in ("A", "s_tot"):
                rep = max(rep, abs(R["NFW"]["runs"][k][t][b][q] - row[t][b][q]))
CH = {}
CH["K-REP"] = (rep <= 1e-9 or MUT, f"NFW mode vs committed Z-T2 runs: max |dA|, |ds_tot| {rep:.1e}")
CH["KL"] = (X["NFW"]["KL"]["ok"], "MID-bin lift, 1e14 Msun test mass on the heaviest cluster: PM " +
            ", ".join(f"{v:.1f}" for v in X["NFW"]["KL"]["lift_pm"]) + " >= NFW " + ", ".join(f"{v:.1f}" for v in X["NFW"]["KL"]["lift_nfw"]) + " Msun/pc^2")
CH["K-ZT2"] = (all(X[m]["exit"] == 0 for m in MODES), "Z-T2's own checks K0-K5 inside every mode: exits " + ", ".join(f"{m} {X[m]['exit']}" for m in MODES))
for k, (ok, v) in CH.items():
    P(f"{k} {'PASS' if ok else 'FAIL'}  {v}")
SUM = {}
P("\nC*_own, T2 / T3 A_MID +- s_tot  (NFW | PM | ALLPM); * = outside 2 s_tot")
for f in ("canonical", "alt"):
    for rc in ("200c", "18pi2m"):
        cls = {}
        for m in ("PM", "ALLPM"):
            fails = [R[m]["runs"][f"C*_own|{rc}|{rd}|{f}|{hk}"]["T3"]["MID"]["A"] > 1 + 2 * R[m]["runs"][f"C*_own|{rc}|{rd}|{f}|{hk}"]["T3"]["MID"]["s_tot"]
                     for rd in ("cap", "lit") for hk in ("h0672", "h0686")]
            cls[m] = "BUDGET NO-GO" if all(fails) else ("PROFILE-LIMITED" if not any(fails) else "SPLIT")
        SUM[f"{f}|{rc}"] = cls
        for rd in ("cap", "lit"):
            for hk in ("h0672", "h0686"):
                k = f"C*_own|{rc}|{rd}|{f}|{hk}"
                cells = []
                for t in ("T2", "T3"):
                    v = [R[m]["runs"][k][t]["MID"] for m in MODES]
                    cells.append(f"{t} " + " | ".join(f"{x['A']:.2f}+-{x['s_tot']:.2f}{'*' if x['A'] > 1 + 2 * x['s_tot'] or x['A'] < 1 - 2 * x['s_tot'] else ''}" for x in v)
                                 + f" [rich {R['NFW']['runs'][k][t]['frac_rich']:.2f}]")
                P(f"{f[:3]} {rc:6s} {rd:3s} {hk}: " + "   ".join(cells))
        P(f"   -> {f} R_own {rc}: PM {cls['PM']}; ALLPM {cls['ALLPM']}")
LAD = {}
if not MUT:
    RL = {m: json.load(open(os.path.join(HERE, f"zt2b_{m}_results.json"))) for m in LADDER}
    P("\nreported: concentration ladder for the free excess (CFG930 NFW, c x 1/2/4/8/16), C*_own T3 A_MID; first passing multiplier")
    for f in ("canonical", "alt"):
        for rc in ("200c", "18pi2m"):
            for rd in ("cap", "lit"):
                for hk in ("h0672", "h0686"):
                    k = f"C*_own|{rc}|{rd}|{f}|{hk}"; seq = [("1", R["NFW"])] + [(m[4:], RL[m]) for m in LADDER]
                    vals = [(x, r["runs"][k]["T3"]["MID"]) for x, r in seq]
                    first = next((x for x, v in vals if abs(v["A"] - 1) <= 2 * v["s_tot"]), "none <= 16")
                    LAD[k] = dict(A=[v["A"] for _, v in vals], s=[v["s_tot"] for _, v in vals], first=first)
                    P(f"{f[:3]} {rc:6s} {rd:3s} {hk}: " + " ".join(f"x{x} {v['A']:.2f}" for x, v in vals) + f"  -> first pass x{first}")
allok = all(ok for ok, _ in CH.values())
P(f"\nchecks: {'ALL PASS' if allok else 'SOME FAIL'}")
json.dump(dict(criteria="12df931233", mutate=MUT, checks={k: dict(ok=ok, value=v) for k, (ok, v) in CH.items()}, classes=SUM, KL=X["NFW"]["KL"], ladder=LAD),
          open(os.path.join(HERE, f"zt2b_summary{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"zt2b_summary{TAG}.out"), "w").write("\n".join(L) + "\n")
sys.exit(0 if allok else 1)
