#!/usr/bin/env python3
"""ET3_low_mass_systematics: beam, pressure support, inclination, distance, quality on ET2's low-mass rise; forward models from a flat floor.
python3 et3_sys.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
HERE3 = os.path.dirname(os.path.abspath(__file__)); REB3 = os.path.dirname(HERE3); ET2 = os.path.join(REB3, "ET2_free_core_low_mass")
MUT3 = "--mutate" in sys.argv; SRC2 = open(os.path.join(ET2, "et2_free.py")).read()
__file__ = os.path.join(ET2, "et2_free.py"); sys.argv = [sys.argv[0]]; exec(compile(SRC2[:SRC2.index('P(f"ET2 free')], "et2_head", "exec"))
L = []
def W(s): print(s, flush=True); L.append(s)
iu = I05; KM = 1e3; ARC = np.pi / 180 / 3600; MPC = 1e3 * KPC
X = {}
for l in open(os.path.join(REB3, "..", "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = l.split()
    if p and p[0] in TAB:
        try: X[p[0]] = dict(D=float(p[2]), eD=float(p[3]), inc=float(p[5]), einc=float(p[6]))
        except ValueError: pass
BIN3 = ((20, 60), (60, 100), (100, 150))
def beam(q, fw): return fw * ARC * X[q["name"]]["D"] * MPC
def rd(q): return TAB[q["name"]]["rd"] * KPC
def var(q, fw=0, sig=0, f=1.0, inc2=1.0):
    """Returns (galaxy copy, observed log g) for the real curve with changes applied."""
    c = dict(q); ok = q["OK"].copy(); R = q["Rm"] * f; c["Rm"] = R
    if fw: ok[R < beam(q, fw) * f, :] = False
    go = q["GO"] * inc2 / f + (sig * KM) ** 2 / rd(q) if sig else q["GO"] * inc2 / f
    c["OK"] = ok; return c, np.log10(go)
def grade(names, S, tag):
    N = np.array([s is not None for s in S]); Sv = np.array([s if s is not None else np.nan for s in S], float); V = np.array([TAB[n]["vf"] for n in names]); rng = np.random.default_rng(RS)
    out = dict(n=int((N & (V < 150)).sum()), bins={}); ok = True
    for lo, hi in BIN3:
        m = N & (V >= lo) & (V < hi); out["bins"][f"{lo}-{hi}"] = dict(n=int(m.sum()), med=float(np.median(Sv[m])), ci=boot(Sv[m], rng))
    m = N & (V < 150); x, y = rankdata(np.log10(V[m])), rankdata(np.log10(Sv[m])); rho = float(np.corrcoef(x, y)[0, 1]); pr = np.random.default_rng(RS); p = float(np.mean(np.abs([np.corrcoef(pr.permutation(x), y)[0, 1] for _ in range(20000)]) >= abs(rho)))
    out.update(rho=rho, p=p, rise=bool(rho > 0 and p < 0.01)); out["floor"] = {}
    for f, v in FL.items():
        side = [0 if b["ci"][0] <= v <= b["ci"][1] else (1 if b["ci"][0] > v else -1) for b in out["bins"].values()]
        out["floor"][f] = "HOLDS" if all(s == 0 for s in side) else ("REJECTED" if side.count(1) >= 2 or side.count(-1) >= 2 else "MIXED")
    W(f" {tag:8s} n {out['n']:3d} " + " ".join(f"{b['med']:6.1f}[{b['ci'][0]:.0f},{b['ci'][1]:.0f}]" for b in out["bins"].values()) + f" rho {rho:+.3f} p {p:.4f} floor {out['floor']['canonical']}/{out['floor']['alt']}"); return out
def run(tag, keep=lambda q: True, **kw):
    S = []; nd = 0
    for q in SAMPLE:
        if not keep(q): S.append(None); continue
        c, go = var(q, **kw)
        if c["OK"][:, iu].sum() < 5: S.append(None); nd += 1; continue
        S.append(fit(c, iu, go)[0])
    r = grade([q["name"] for q in SAMPLE], S, tag); r["dropped_points"] = nd; return r, S
def forward(q, S0, fw, sig, truth_r0=None):
    """Observed log g at real points: true V, 1D smoothed, minus pressure term."""
    R = q["Rm"]; r0 = r0_et1(q, S0) if truth_r0 is None else truth_r0
    Vb2 = q["GB"][:, iu] * R; s = beam(q, fw) / 2.355 if fw else 0.0
    gh0 = gh(q, S0, r0); V2 = np.maximum(Vb2 + gh0 * R, 0)
    if s == 0: g = V2 / R
    else:
        rmax = R.max() + 5 * s; rr = np.linspace(rmax / 4000, rmax, 4000); c2 = dict(q); c2["Rm"] = rr
        vb = np.interp(rr, R, Vb2, left=np.nan); inner = rr < R[0]; vb[inner] = Vb2[0] * (rr[inner] / R[0]) ** 2; vb[rr > R[-1]] = Vb2[-1]
        Vf_ = np.sqrt(np.maximum(vb + gh(c2, S0, r0) * rr, 0)); Vs = np.array([np.trapz((Vf_ * np.exp(-0.5 * ((rr - x) / s) ** 2) - Vf_ * np.exp(-0.5 * ((rr + x) / s) ** 2)), rr) / (s * np.sqrt(2 * np.pi)) for x in R]); g = Vs ** 2 / R
    g = g - (sig * KM) ** 2 / rd(q) if sig else g
    return np.log10(np.maximum(g, 1e-14))
def frun(tag, S0f, fw=0, sig=0):
    return grade([q["name"] for q in SAMPLE], [fit(q, iu, forward(q, S0f(q), fw, sig))[0] for q in SAMPLE], tag)
W(f"ET3 systematics; kappa = 1/2 FITTED; footings never pooled; not theory closed{' [MUTATE]' if MUT3 else ''}\nsample {len(SAMPLE)}, below 150 km/s {(Vf < 150).sum()}")
RES = dict(mutate=MUT3); code = 0
if MUT3:
    r = frun("V^1", lambda q: 100 * (TAB[q["name"]]["vf"] / 80)); RES["mut"] = r; code = int(not r["rise"]); W(f"MUTATE real rise seen: {r['rise']}")
else:
    et2 = json.load(open(os.path.join(ET2, "et2_results.json")))["ups"]["0.50"]["gal"]
    W("\nChecks"); b0, S0 = run("base"); k1 = all(s == et2[q["name"]]["S"] for q, s in zip(SAMPLE, S0)); W(f"K1 zero change equals ET2 per galaxy: {'PASS' if k1 else 'FAIL'}"); code |= not k1
    q = sel(100, 150)[0]; k2 = []
    for i, j in ((61, 15), (89, 19), (117, 27)):
        a, b, _, _ = fit(q, iu, np.log10(np.maximum(q["GB"][:, iu] + gh(q, SG[i], RG[j]), 1e-300))); k2.append(a == SG[i] and b == RG[j])
    W(f"K2 on-grid plants exact: {k2}: {'PASS' if all(k2) else 'FAIL'}"); code |= not all(k2)
    d3 = max(float(np.max(np.abs((forward(g, 100.0, 0, 0) - np.log10(g["GB"][:, iu] + gh(g, 100.0, r0_et1(g, 100.0))))[g["OK"][:, iu]]))) for g in SAMPLE); W(f"K3 forward with no systematics, max |d log g| {d3:.1e}: {'PASS' if d3 < 1e-3 else 'FAIL'}"); code |= d3 >= 1e-3
    k3b = [abs(np.log(fit(g, iu, forward(g, 100.0, 0, 0))[0] / 100)) <= 1.01 * np.log(SG[1] / SG[0]) for g in SAMPLE]; W(f"K3b refit S within a grid step: {np.mean(k3b):.3f} of galaxies; median galaxy {'PASS' if np.mean(k3b) >= 0.5 else 'FAIL'}"); code |= np.mean(k3b) < 0.5
    g = max(sel(60, 100), key=lambda z: z["Rm"].max()); m = g["Rm"] < beam(g, 30); a = forward(g, 100.0, 30, 0)[m]; b = forward(g, 100.0, 0, 0)[m]; k4 = bool(m.sum() and np.mean(a < b) >= 0.5); W(f"K4 smoothing lowers inner V: {m.sum()} points, fraction lower {np.mean(a < b) if m.sum() else None}: {'PASS' if k4 else 'FAIL'}"); code |= not k4
    W("\nPart 1 real curves (bins 20-60, 60-100, 100-150)"); P1 = dict(base=b0)
    P1["B15"], _ = run("B15", fw=15); P1["B30"], _ = run("B30", fw=30); P1["P8"], _ = run("P8", sig=8); P1["P12"], _ = run("P12", sig=12)
    P1["I45"], _ = run("I45", keep=lambda q: TAB[q["name"]]["inc"] >= 45); P1["Q1"], _ = run("Q1", keep=lambda q: TAB[q["name"]]["Q"] == 1)
    P1["WORST"], _ = run("WORST", keep=lambda q: TAB[q["name"]]["inc"] >= 45 and TAB[q["name"]]["Q"] == 1, fw=30, sig=12)
    gen = np.random.default_rng(RS); MC = []
    for d in range(20):
        S = []
        for q in SAMPLE:
            x = X[q["name"]]; i = np.clip(gen.normal(x["inc"], x["einc"]), 15, 89); f = float(np.exp(gen.normal(0, x["eD"] / x["D"]))); c, go = var(q, f=f, inc2=(np.sin(np.radians(x["inc"])) / np.sin(np.radians(i))) ** 2); S.append(fit(c, iu, go)[0])
        MC.append(grade([q["name"] for q in SAMPLE], S, f"MC{d}"))
    nmc = sum(m["rise"] for m in MC); W(f" MC rise in {nmc}/20; rho {min(m['rho'] for m in MC):+.3f} to {max(m['rho'] for m in MC):+.3f}")
    fails = [k for k in ("B15", "B30", "P8", "P12", "I45", "Q1") if not P1[k]["rise"]]; wl = P1["WORST"]
    wread = "UNDERPOWERED" if wl["n"] < 30 else ("RISE" if wl["rise"] else "LOST")
    v1 = ("FRAGILE " + str(fails + ([f"MC {nmc}/20"] if nmc < 19 else []))) if fails or nmc < 19 else ("ROBUST-BUT-WORST-LOST" if wread == "LOST" else "ROBUST")
    W(f"\nVERDICT 1 RISE: {v1}; WORST reads {wread} (n {wl['n']})")
    v2 = {}
    for f in FL:
        vs = {k: P1[k]["floor"][f] for k in ("B15", "B30", "P8", "P12", "I45", "Q1", "WORST")}; vs["MC"] = sorted({m["floor"][f] for m in MC}); flat = set(sum([[x] if isinstance(x, str) else x for x in vs.values()], [])); v2[f] = dict(table=vs, verdict="STABLE " + flat.copy().pop() if len(flat) == 1 else "VARIATION-DEPENDENT"); W(f"VERDICT 2 FLOOR {f}: {v2[f]['verdict']} {vs}")
    W("\nPart 2 forward from flat floor"); P2 = {}
    for f, v in FL.items():
        P2[f] = {}
        for tg, fw, sig in (("F15", 15, 0), ("F30", 30, 0), ("F30P8", 30, 8), ("F30P12", 30, 12)):
            r = frun(f"{f[:3]} {tg}"[:8], lambda q: v, fw, sig); a, c = r["bins"]["20-60"]["med"], r["bins"]["100-150"]["med"]; r["verdict"] = ("FAKED" if a <= 77.3 and c >= 136.6 else "PARTIAL") if r["rise"] else "NOT FAKED"; P2[f][tg] = r; W(f"   -> {r['verdict']}")
    order = ("NOT FAKED", "PARTIAL", "FAKED"); v3 = max((r["verdict"] for f in P2 for r in P2[f].values()), key=order.index); W(f"VERDICT 3 FORWARD: {v3}")
    RES.update(P1=P1, MC=MC, P2=P2, verdicts=dict(rise=v1, worst=wread, floor=v2, forward=v3), K=dict(K1=k1, K2=k2, K3=d3, K3b=float(np.mean(k3b)), K4=k4))
t = "_MUTATE" if MUT3 else ""
json.dump(RES, open(os.path.join(HERE3, f"et3_results{t}.json"), "w"), indent=1, default=lambda o: o.item()); open(os.path.join(HERE3, f"et3{t}.out"), "w").write("\n".join(L) + "\n"); sys.exit(int(code))
