"""CFG843 -- MW vs M31 satellite excess at matched g_bar.  Criteria: FROZEN_CRITERIA.md.  Run: python3 cfg843.py (CFG843_MUTATE=1).
kappa = 1/2 FITTED; not theory closed."""
import os, csv, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG843_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
host = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): host[r["name"]] = r.get("host", "")
rows = [r for r in json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["canonical|nu_e"]["rows"] if host.get(r["name"]) in ("mw", "m_031")]
for r in rows: r["m31"] = 1.0 if host[r["name"]] == "m_031" else 0.0; r["d"] = r["delta"] + (0.3 if (MUT and r["m31"]) else 0.0)
def fit(S):
    x = np.array([r["lgbar"] + 12.5 for r in S]); m = np.array([r["m31"] for r in S]); y = np.array([r["d"] for r in S])
    A = np.vstack([np.ones_like(x), x, m]).T; return np.linalg.lstsq(A, y, rcond=None)[0]
P("CFG843  MW vs M31 satellites at matched g_bar" + ("  [MUTATE +0.3 dex on M31]" if MUT else ""))
RES = dict(lane="CFG843", mutate=MUT)
for lab, S in (("all", rows), ("g_bar < 1e-11.9", [r for r in rows if r["lgbar"] < -11.9])):
    nmw, nm31 = sum(1 for r in S if not r["m31"]), sum(1 for r in S if r["m31"])
    a, b, c = fit(S); rng = np.random.default_rng(843); bs = [fit([S[i] for i in rng.integers(0, len(S), len(S))])[2] for _ in range(2000)]
    sc = float(np.std(bs)); mmw = np.mean([r["d"] for r in S if not r["m31"]]); mm31 = np.mean([r["d"] for r in S if r["m31"]])
    cls = "NOT DIAGNOSTIC" if min(nmw, nm31) < 6 else ("SAME" if (abs(c) < 2 * sc and abs(c) < 0.15) else ("DIFFERENT" if abs(c) >= 3 * sc else "INCONCLUSIVE"))
    RES[lab] = dict(N_mw=nmw, N_m31=nm31, a=float(a), b=float(b), c=float(c), sc=sc, mean_mw=float(mmw), mean_m31=float(mm31), cls=cls)
    P(f"  [{lab}] MW {nmw} (mean {mmw:+.3f})  M31 {nm31} (mean {mm31:+.3f})  slope b {b:+.3f}/dex  offset c (M31-MW) {c:+.3f} +- {sc:.3f}  -> {cls}")
if not MUT:
    x = np.array([r["lgbar"] + 12.5 for r in rows]); y = np.array([r["d"] for r in rows]); pf = np.polyfit(x, y, 1)
    A = np.vstack([np.ones_like(x), x]).T; ls = np.linalg.lstsq(A, y, rcond=None)[0]
    P(f"  K1 pooled slope lstsq {ls[1]:.6f} vs polyfit {pf[0]:.6f} -> {'PASS' if abs(ls[1] - pf[0]) < 1e-9 else 'FAIL'}")
RES["cls"] = RES["all"]["cls"]; P(f"\n  CLASS (all satellites): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg843_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg843{sfx}.out"), "w").write("\n".join(OUT) + "\n")
