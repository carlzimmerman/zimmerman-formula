#!/usr/bin/env python3
"""ET4_upsilon_trend: can Upsilon changing with mass explain ET2's low-mass rise?
python3 et4_ups.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
HERE4 = os.path.dirname(os.path.abspath(__file__)); REB4 = os.path.dirname(HERE4); ET2 = os.path.join(REB4, "ET2_free_core_low_mass")
MUT4 = "--mutate" in sys.argv; SRC2 = open(os.path.join(ET2, "et2_free.py")).read()
__file__ = os.path.join(ET2, "et2_free.py"); sys.argv = [sys.argv[0]]; exec(compile(SRC2[:SRC2.index('P(f"ET2 free')], "et2_head", "exec"))
L = []
def W(s): print(s, flush=True); L.append(s)
BIN3 = ((20, 60), (60, 100), (100, 150)); NM = [q["name"] for q in SAMPLE]; IUS = np.arange(len(UPS))
def iu_of(v, s): return int(np.argmin(abs(UPS - np.clip(0.50 * (v / 80) ** s, UPS[0], UPS[-1]))))
def clipped(s): return int(sum((0.50 * (v / 80) ** s < UPS[0]) or (0.50 * (v / 80) ** s > UPS[-1]) for v in Vf))
def grade(S, tag, mask=None, need_bins=True):
    S = np.asarray(S, float); m = (Vf < 150) if mask is None else mask; rng = np.random.default_rng(RS); out = dict(n=int(m.sum()), bins={})
    for lo, hi in BIN3:
        b = m & (Vf >= lo) & (Vf < hi)
        out["bins"][f"{lo}-{hi}"] = dict(n=int(b.sum()), med=float(np.median(S[b])), ci=boot(S[b], rng)) if b.sum() >= 2 else dict(n=int(b.sum()), med=None, ci=None)
    x, y = rankdata(np.log10(Vf[m])), rankdata(np.log10(S[m])); rho = float(np.corrcoef(x, y)[0, 1]); pr = np.random.default_rng(RS); p = float(np.mean(np.abs([np.corrcoef(pr.permutation(x), y)[0, 1] for _ in range(20000)]) >= abs(rho)))
    out.update(rho=rho, p=p, rise=bool(rho > 0 and p < 0.01), vrange=[float(Vf[m].min()), float(Vf[m].max())]); out["floor"] = {}
    if all(b["ci"] for b in out["bins"].values()):
        for f, v in FL.items():
            side = [0 if b["ci"][0] <= v <= b["ci"][1] else (1 if b["ci"][0] > v else -1) for b in out["bins"].values()]; out["floor"][f] = "HOLDS" if all(s == 0 for s in side) else ("REJECTED" if side.count(1) >= 2 or side.count(-1) >= 2 else "MIXED")
    W(f" {tag:12s} n {out['n']:3d} V {out['vrange'][0]:.0f}-{out['vrange'][1]:.0f} " + " ".join((f"{b['med']:6.1f}[{b['ci'][0]:.0f},{b['ci'][1]:.0f}]" if b["ci"] else f"n={b['n']}") for b in out["bins"].values()) + f" rho {rho:+.3f} p {p:.4f} floor {out['floor']}"); return out
def truth(q, S0, s):
    iu = iu_of(TAB[q["name"]]["vf"], s); return np.log10(np.maximum(q["GB"][:, iu] + gh(q, S0, r0_et1(q, S0)), 1e-300))
def split(q):
    a, b = int(np.argmin(abs(UPS - 0.40))), int(np.argmin(abs(UPS - 0.80))); A = (q["GB"][:, b] - q["GB"][:, a]) / (UPS[b] - UPS[a]); return q["GB"][:, a] - UPS[a] * A, A
def fstar(q):
    G, A = split(q); ok = q["OK"][:, I05]; return float(np.sum(0.50 * A[ok]) / max(np.sum(np.abs(q["GB"][ok, I05])), 1e-300))
def fit_floor(q, S0):
    """Minimise over Upsilon and r0 at fixed S."""
    best = (1e99, 0, 0); ok0 = q["OK"]; o = np.log10(q["GO"])
    H = [S0 * gh(q, 1.0, r0) for r0 in RG]
    for iu in IUS:
        ok = ok0[:, iu]
        if ok.sum() < 2: continue
        W_ = q["W"][ok]; sw = max(W_.sum(), 1e-300); gb = q["GB"][ok, iu]
        for j, h in enumerate(H):
            m = float(np.sum(W_ * (o[ok] - np.log10(np.maximum(gb + h[ok], 1e-300))) ** 2) / sw)
            if m < best[0]: best = (m, iu, j)
    return best
W(f"ET4 Upsilon trend; kappa = 1/2 FITTED; footings never pooled; not theory closed{' [MUTATE]' if MUT4 else ''}\nsample {len(SAMPLE)}, below 150 km/s {(Vf < 150).sum()}")
RES = dict(mutate=MUT4); code = 0
if MUT4:
    G1 = [truth(q, FL["canonical"], 0.5) for q in SAMPLE]
    a = grade([fit(q, iu_of(TAB[q["name"]]["vf"], 0.5), g)[0] for q, g in zip(SAMPLE, G1)], "right trend"); b = grade([fit(q, I05, g)[0] for q, g in zip(SAMPLE, G1)], "fit at 0.50")
    code = int(a["p"] < 0.01 or b["rho"] < a["rho"]); RES.update(right=a, fixed=b); W(f"MUTATE correct trend p {a['p']:.4f}; unmodelled rho {b['rho']:+.3f} vs modelled {a['rho']:+.3f}: {'bites' if not code else 'NO BITE'}")
else:
    et2 = json.load(open(os.path.join(ET2, "et2_results.json")))["ups"]["0.50"]["gal"]
    W("\nChecks"); S0 = [fit(q, iu_of(TAB[q["name"]]["vf"], 0.0))[0] for q in SAMPLE]; k1 = all(s == et2[n]["S"] for s, n in zip(S0, NM)); W(f"K1 s = 0 equals ET2 per galaxy: {'PASS' if k1 else 'FAIL'}"); code |= not k1
    i6 = int(np.argmin(abs(UPS - 0.60))); k2 = 0.0
    for q in SAMPLE:
        G, A = split(q); ok = q["OK"][:, i6]; k2 = max(k2, float(np.max(np.abs((G + 0.60 * A)[ok] / q["GB"][ok, i6] - 1))))
    W(f"K2 g_bar linear in Upsilon, max rel {k2:.1e}: {'PASS' if k2 < 1e-10 else 'FAIL'}"); code |= k2 >= 1e-10
    k3 = []
    for q in sel(100, 150)[:3]:
        iu = int(np.argmin(abs(UPS - 0.70))); g = np.log10(np.maximum(q["GB"][:, iu] + gh(q, SG[80], RG[20]), 1e-300)); ok = q["OK"][:, iu]; c = dict(q); c["GO"] = 10 ** g; m, a, b = fit_floor(c, SG[80]); k3.append(a == iu and b == 20)
    W(f"K3 planted Upsilon, r0 returned at fixed S: {k3}: {'PASS' if all(k3) else 'FAIL'}"); code |= not all(k3)
    W("\nTest 1 real curves with a trend"); T1 = {}
    for s in (0.25, 0.5, 1.0):
        r = grade([fit(q, iu_of(v, s))[0] for q, v in zip(SAMPLE, Vf)], f"s={s}"); r["clipped"] = clipped(s); r["verdict"] = "SURVIVES" if r["p"] < 0.01 else "ERASED"; T1[str(s)] = r; W(f"   -> {r['verdict']}; clipped {r['clipped']}")
    W("\nTest 2 gas and star groups"); F = np.array([fstar(q) for q in SAMPLE]); gas = (F < 0.5) & (Vf < 150); star = (F >= 0.5) & (Vf < 150); T2 = {}
    for u in (0.50, 0.30, 0.80):
        iu = int(np.argmin(abs(UPS - u))); Su = [fit(q, iu)[0] for q in SAMPLE]; T2[f"gas_{u:.2f}"] = grade(Su, f"GAS U={u}", gas)
        if u == 0.50: T2["star"] = grade(Su, "STAR U=0.5", star)
    g0 = T2["gas_0.50"]; t2 = "UNDERPOWERED" if g0["n"] < 20 else ("RISE WITHOUT LEVER" if g0["rise"] else "NO RISE IN GAS GROUP"); W(f"   -> {t2}; median f* gas {np.median(F[gas]):.2f}, star {np.median(F[star]):.2f}")
    W("\nTest 3 needed Upsilon at the floor"); T3 = {}
    Fr = [fit(q, I05)[0:2] for q in SAMPLE]; Ms = []
    for q, (s, r) in zip(SAMPLE, Fr):
        ok = q["OK"][:, I05]; Ms.append(float(np.sum(q["W"][ok] * (np.log10(q["GO"][ok]) - np.log10(np.maximum(q["GB"][ok, I05] + gh(q, s, r)[ok], 1e-300))) ** 2) / np.sum(q["W"][ok])))
    Ms = np.array(Ms)
    for f, v in FL.items():
        rs = [fit_floor(q, v) for q in SAMPLE]; U = UPS[[r[1] for r in rs]]; Mf = np.array([r[0] for r in rs]); rng = np.random.default_rng(RS); bn = {}
        for lo, hi in BIN3:
            m = (Vf >= lo) & (Vf < hi); bn[f"{lo}-{hi}"] = dict(n=int(m.sum()), med=float(np.median(U[m])), ci=boot(U[m], rng), ends=int(((U[m] == UPS[0]) | (U[m] == UPS[-1])).sum()), mse_ratio=float(np.median(Mf[m] / np.maximum(Ms[m], 1e-12))))
            W(f" {f:9s} {lo}-{hi}: needed U {bn[f'{lo}-{hi}']['med']:.2f} {np.round(bn[f'{lo}-{hi}']['ci'], 2).tolist()} at ends {bn[f'{lo}-{hi}']['ends']}/{m.sum()}; mse ratio {bn[f'{lo}-{hi}']['mse_ratio']:.2f}")
        out = [k for k, b in bn.items() if not 0.39 <= b["med"] <= 0.64]; T3[f] = dict(bins=bn, verdict="IN BAND" if not out else "OUT " + str(out)); W(f"   -> {T3[f]['verdict']}")
    W("\nTest 4 forward"); T4 = {}
    for f, v in FL.items():
        T4[f] = {}
        for s in (0.25, 0.5, 1.0):
            r = grade([fit(q, I05, truth(q, v, s))[0] for q in SAMPLE], f"{f[:3]} s={s}"); a, c = r["bins"]["20-60"]["med"], r["bins"]["100-150"]["med"]; r["verdict"] = ("FAKED" if a <= 77.3 and c >= 136.6 else "PARTIAL") if r["rise"] else "NOT FAKED"; T4[f][str(s)] = r; W(f"   -> {r['verdict']}")
    lever = t2 == "RISE WITHOUT LEVER"; ok = lambda ss: any(T1[ss]["verdict"] == "ERASED" and T4[f][ss]["verdict"] == "FAKED" for f in FL)
    inb = any(T1["0.25"]["verdict"] == "ERASED" and T4[f]["0.25"]["verdict"] == "FAKED" and T3[f]["verdict"] == "IN BAND" for f in FL)
    ov = "Y EXPLAINS IT" if inb and not lever else ("COULD EXPLAIN IT ONLY BEYOND THE BAND" if (ok("0.5") or ok("1.0")) and not lever else "NOT EXPLAINED BY Y"); W(f"\nOVERALL: {ov} (Y = Upsilon)")
    RES.update(T1=T1, T2=T2, t2=t2, T3=T3, T4=T4, overall=ov, K=dict(K1=k1, K2=k2, K3=k3))
t = "_MUTATE" if MUT4 else ""
json.dump(RES, open(os.path.join(HERE4, f"et4_results{t}.json"), "w"), indent=1, default=lambda o: o.item()); open(os.path.join(HERE4, f"et4{t}.out"), "w").write("\n".join(L) + "\n"); sys.exit(int(code))
