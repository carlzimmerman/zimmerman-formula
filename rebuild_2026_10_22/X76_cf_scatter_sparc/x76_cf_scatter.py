#!/usr/bin/env python3
"""X76_cf_scatter_sparc (criteria 12d45b6b56): native per-galaxy c_f scatter on the SPARC line.
X74's script (X73 PRIMARY, shape S, native, slope 2.7774, f* 0.034, c_f 4 base exec) is executed with its outputs redirected
here; then each SPARC galaxy is refitted with eta(c) for every c in A3's nine ng 64 per-seed values, and 10 000 independent
assignments (rng 20261029) re-index those fits.  python3 x76_cf_scatter.py [--mutate]
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv
X74F = os.path.join(REB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
END = '{"__file__": os.path.join(HERE, "x74_native_cf.py"), "__name__": "__main__"}'
assert TX.count(END) == 1; TX = TX.replace(END, "X76NS")
os.environ.update(X74_CF="const4", X74_CFMULT="1", X73_FSTAR="0.034", X73_SLOPE="2.7774425603108597", PYTHONHASHSEED="0")
NS = {"__file__": os.path.join(HERE, "x76_base.py"), "__name__": "__main__"}
D = {"__file__": X74F, "__name__": "x74_ro", "X76NS": NS}
argv0 = sys.argv
try:
    exec(compile(TX, X74F, "exec"), D)
except SystemExit:
    pass
sys.argv = argv0
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("X76 cf scatter on SPARC (criteria 12d45b6b56); kappa = 1/2 FITTED; footings never pooled; not theory closed" + ("  [MUTATE c x 2]" if MUT else ""))
k3 = bool(NS["RES"]["x74"].get("k1", {}).get("ok")); P(f"K3 base exec X74 K1 identity (c_f 4 vs X73): {'PASS' if k3 else 'FAIL'}")
GALS, fit_one, pooled, line = NS["GALS"], NS["fit_one"], NS["pooled"], NS["line"]
B, solve_r0, sigma_coll, eta_of, SIG, BGS = NS["B"], NS["solve_r0"], NS["sigma_coll"], NS["eta_of"], NS["SIG"], NS["BGS"]
GE, MSUNE, MPCE, PC2 = NS["GE"], NS["MSUNE"], NS["MPCE"], NS["PC2"]
FEET, TAGS = ("canonical", "alt"), ("A_c2b_refit", "B_cfg886_bg")

def fits(f, tag, c):
    """per-galaxy (wr2, ws, iu, active) at a single c for all galaxies, exactly as X73's sparc() with eta = eta_of(c)."""
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); eta = eta_of(c); rows = []
    for q in GALS:
        lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
        sc = eta * sigma_coll(tag, M200)[0] * MSUNE / PC2; s = max(SIG[f], sc)
        r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)
        w, ws_, iu = fit_one(q, np.log10(np.maximum(q["GB"] + (GE * Mh / q["Rm"] ** 2)[:, None], 1e-300)))
        rows.append((float(w), float(ws_), int(iu), sc > SIG[f]))
    return rows
def stat(rows):
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]); st["n_active"] = int(sum(r[3] for r in rows)); return st

# K1 / K2 identities
X73J = json.load(open(os.path.join(REB, "X73_smooth_core_all_measured", "x73_results_fs0.034_S_nat_s2.7774.json")))
P2J = json.load(open(os.path.join(REB, "X74_all_measured_native_cf", "preread_P2_fs0.034_x74_results_fs0.034_nat_s2.7774.json")))
def ident(c, J):
    d = 0.0
    for f in FEET:
        for t in TAGS:
            s = stat(fits(f, t, c)); j = J["footings"][f]["sparc"][t]
            d = max(d, abs(s["rms"] - j["rms"]), abs(s["U_median"] - j["U_median"]), abs(s["n_active"] - j["n_active"]))
    return d
d1 = ident(4.0, X73J); d2 = ident(7.7395930714417345, P2J)
k1, k2 = d1 == 0, d2 == 0
P(f"K1 all galaxies c = 4 reproduce X73 PRIMARY SPARC: max |d| {d1:.1e}: {'PASS' if k1 else 'FAIL'}")
P(f"K2 all galaxies c = 7.74 reproduce pre-read P2 SPARC: max |d| {d2:.1e}: {'PASS' if k2 else 'FAIL'}")

def cset(name):
    X48 = os.path.join(REB, "X48_native_cf_zoom")
    srcs = [("x48_analyze_results_ng64_A3.json", 64)] + ([("x48_analyze_results_ng48_A2.json", 48)] if name == "pooled18" else [])
    v = [o["cf"] for f_, ng in srcs for o in json.load(open(os.path.join(X48, f_)))["runs"].values()
         if o.get("flag") == "ok" and o.get("ng") == ng and abs(o["M"] / 1e12 - 1) < 1e-6]
    return np.array(sorted(v)) * (2.0 if MUT else 1.0)
RES = dict(criteria="12d45b6b56", mutate=MUT, checks=dict(K1=d1, K2=d2, K3=k3), sets={})
for name in ("A3_nine", "pooled18"):
    C = cset(name); G = len(GALS)
    P(f"\n=== set {name} ({'graded' if name == 'A3_nine' else 'sensitivity, reported'}): {len(C)} c values " + ", ".join(f"{c:.2f}" for c in C))
    RES["sets"][name] = dict(c=C.tolist(), feet={})
    for f in FEET:
        W = {t: np.array([[r[:3] for r in fits(f, t, c)] for c in C]) for t in TAGS}       # (nc, G, 3)
        rng = np.random.default_rng(20261029); idx = rng.integers(0, len(C), (10000, G))
        ar = np.arange(G)[None, :]; per = {}; ok = np.ones(10000, bool)
        for t in TAGS:
            w2, ws, iu = W[t][idx, ar, 0], W[t][idx, ar, 1], W[t][idx, ar, 2].astype(int)
            rms = np.sqrt(w2.sum(1) / ws.sum(1)); U = np.median(NS["UPS"][iu], axis=1)
            lin = (rms <= 0.110) & (U >= 0.50) & (U <= 0.80); ok &= lin
            per[t] = dict(rms_q=np.percentile(rms, [16, 50, 84]).tolist(), U_q=np.percentile(U, [16, 50, 84]).tolist(), P_line=float(lin.mean()))
        Pl = float(ok.mean()); lab = "SCATTER PASSES" if Pl >= 0.5 else "SCATTER FAILS"
        RES["sets"][name]["feet"][f] = dict(per_bg=per, P_line=Pl, label=lab)
        P(f"  [{f}] P_line (both backgrounds) {Pl:.3f} -> {lab}")
        for t in TAGS:
            p = per[t]; P(f"     {t}: median U 16/50/84 {p['U_q'][0]:.2f}/{p['U_q'][1]:.2f}/{p['U_q'][2]:.2f}; rms 50% {p['rms_q'][1]:.4f}; P_line {p['P_line']:.3f}")
ck = k1 and k2 and k3
P(f"\nchecks {'ALL PASS' if ck else 'FAIL -> UNDECIDED'}; HEADLINE (canonical, A3_nine): {RES['sets']['A3_nine']['feet']['canonical']['label'] if ck else 'UNDECIDED'}")
tag = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"x76_cf_scatter{tag}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x76_cf_scatter_results{tag}.json"), "w"), indent=1, default=float)
sys.exit(0 if ck else 1)
