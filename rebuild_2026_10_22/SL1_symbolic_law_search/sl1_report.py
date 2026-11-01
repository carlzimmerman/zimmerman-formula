#!/usr/bin/env python3
"""SL1 read: merges runs/, regrades candidates through dvecN, applies the gauntlet. Writes discover.out, hall_of_fame.json, pareto.json, SURVIVORS.md if any. kappa = 1/2 FITTED; not theory closed."""
import glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ["SL1_HERE"] = HERE
exec(compile(open(os.path.join(HERE, "discover_law.py")).read().split('if __name__ == "__main__" and "--sweep"')[0], "discover_law", "exec"), globals())
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
fx = lambda t: t if isinstance(t, str) else tuple(fx(c) if i else c for i, c in enumerate(t))
D = Data(); base = D.grade("1", "1"); P(f"SL1 read; baseline NR1 PRIMARY on train: gate {base['gate']:.3f} (g1 {base['g1']:.2f} g2 {base['g2']:.2f} g3 {base['g3']:.2f} g4 {base['g4']:.2f}), failing {base['detail']['bad']}; kappa = 1/2 FITTED; not theory closed")
ALLC = {}; PAR = {}; HOF = dict(gram={})
for gram in ("SPEC", "NATIVE"):
    recs = []; near = []; hits = []; par = []; dist = 0; t1n = t1p = 0
    for f in sorted(glob.glob(os.path.join(HERE, "runs", f"genome_bank_{gram}_s*.json"))):
        J = json.load(open(f)); recs += J["best"]; near += J.get("near", []); hits += J["hits"]; par += J["pareto"]; dist += J["n_distinct"]; t1n += J["n_t1"]; t1p += J["n_t1_pass"]; b = min(J["best"], key=lambda x: x["gate"]); P(f"{gram} seed {J['seed']}: gen {J['gen']}, {J['n_eval']} evaluated, {J['n_distinct']} distinct this session, Tier 1 pass {J['n_t1_pass']}/{J['n_t1']}, hits {len(J['hits'])}, near {len(J.get('near', []))}, best gate {b['gate']:.3f}: {b['A']} | {b['B']}")
    S = json.load(open(os.path.join(HERE, "runs", f"sweep_{gram}.json")))
    for k in "AB":
        s = S[k]; P(f"{gram} sweep {k}: completed size {s['completed_size']}, counts {s['counts']}, Tier 1 trees {s['tier1_survivors']}, finite graded {s['finite_graded']}, all graded {s['all_graded']}, hits {len(s['hits'])}; best " + "; ".join(f"{x['tree']} {x['gate']:.3f}" for x in s["top"][:3]))
    c = S["cross"]; recs += c["best"]; near += c["near"]; hits += c["hits"]; par += c["pareto"]; P(f"{gram} cross {c['n']} pairs: hits {len(c['hits'])}, near {len(c['near'])}, best {c['best'][0]['gate']:.3f}: {c['best'][0]['A']} | {c['best'][0]['B']}")
    u = {}
    for r in sorted(recs, key=lambda x: x["gate"])[:200] : u.setdefault((r["A"], r["B"]), r)
    cand = dict(list(u.items())[:20])
    for r in hits + sorted(near, key=lambda x: x["gate"])[:60]: cand.setdefault((r["A"], r["B"]), r)
    ALLC[gram] = cand; pm = {}
    for r in par: pm[(r["A"], r["B"])] = r
    pv = list(pm.values()); PAR[gram] = sorted([r for r in pv if not any(o is not r and o["g123"] <= r["g123"] and o["g4"] <= r["g4"] and (o["g123"] < r["g123"] or o["g4"] < r["g4"]) for o in pv)], key=lambda x: x["g123"]); HOF["gram"][gram] = dict(n_hits_surrogate=len({(h["A"], h["B"]) for h in hits}), n_near=len({(h["A"], h["B"]) for h in near}), distinct=dist, t1=[t1p, t1n])
L = [[r["At"], r["Bt"], ["canonical", "alt"]] for g in ALLC for r in ALLC[g].values()]; P(f"exact regrade: {len(L)} pairs through dvecN")
os.environ.update(SL1_LANE=HERE, SL1_TREES=os.path.join(HERE, "cache", "cand.json"), SL1_OUT=os.path.join(HERE, "cache", "cand_exact.json")); json.dump(L, open(os.environ["SL1_TREES"], "w"))
if "--noexact" not in sys.argv: subprocess.run(["nice", "-n", "15", sys.executable, os.path.join(HERE, "sl1_harvest.py"), os.path.join(HERE, "sl1_tail_exact.py")], stdout=open(os.path.join(HERE, "cache", "cand.log"), "w"), stderr=subprocess.STDOUT, check=True)
X = {(r["A"], r["B"]): r for r in json.load(open(os.environ["SL1_OUT"]))["res"]}
def viol(Z, f="canonical"): w = np.maximum(np.abs(Z[f][HKS[0]]), np.abs(Z[f][HKS[1]])); return float(np.sum(np.maximum(0, w - 2))), [KEYS[i] for i in np.where(w > 2)[0]]
ET = json.load(open(os.path.join(RB, "ET1_core_strength_needed", "et1_results.json")))["ups"]["0.50"]["gal"]; HO = D.split["holdout"]; rng = np.random.default_rng(20261030); IVH = []
for l, h in BINS:
    x = np.array([ET[D.gals[i]["name"]]["S"] for i in HO if D.gals[i]["name"] in ET and (l <= D.gals[i]["vf"] < h or (h == 400 and D.gals[i]["vf"] == 400))]); IVH.append(tuple(np.percentile(np.median(x[rng.integers(0, len(x), (20000, len(x)))], axis=1), [2.5, 97.5])))
P("holdout's own ET1 intervals: " + ", ".join(f"[{a:.0f},{b:.0f}]" for a, b in IVH))
def qinf(t): return "Qi" if t == "q" else t if isinstance(t, str) else tuple(qinf(c) if i else c for i, c in enumerate(t))
def a0_indep(t):
    # B's own value at alt's a0: leaves xb, xc scaled together, on fixed points. The clipped gate violations are zero at both a0s for any hit, so they cannot test this (first version's bug).
    pr = np.random.default_rng(1); V = dict(xb=10 ** pr.uniform(-3, 3, 200), xc=10 ** pr.uniform(-3, 3, 200), fl=10 ** pr.uniform(-3, 1, 200), q=10 ** pr.uniform(0, 5, 200)); W = dict(V, xb=V["xb"] * 0.8, xc=V["xc"] * 0.8)
    with np.errstate(all="ignore"): a, b = ev(t, V) * np.ones(200), ev(t, W) * np.ones(200)
    ok = np.isfinite(a) & np.isfinite(b); return bool(ok.any() and np.max(np.abs(a[ok] - b[ok])) < 1e-9)
CONST["Qi"] = 1e30; SURV = []; HOF["cand"] = {}
for gram, cand in ALLC.items():
    rows = []
    for k, r in cand.items():
        A, B_ = fx(r["At"]), fx(r["Bt"]); g4, bad = viol(X[k]["Z"]); gate = r["g123"] + g4; rows.append(dict(A=r["A"], B=r["B"], g1=r["g1"], g2=r["g2"], g3=r["g3"], g4_exact=g4, g4_surrogate=r["g4"], gate_exact=gate, bad=bad, nodes=r["nodes"]))
        if gate == 0.0:
            ho = D.grade(A, B_, idx=HO, intervals=IVH, keys=False); gr = D.groups(A, B_); xc = D.xcop(A, B_); al, ba = viol(X[k]["Z"], "alt"); fu = [D.sparc_fit(D.sparc(list(range(175)), t), A, B_, D.a0["canonical"]) for t in TAGS]; line = all(0.5 <= np.median(f[0]) <= 0.8 and np.sqrt(f[1].sum() / f[2].sum()) <= 0.110 for f in fu); altg = D.grade(A, B_, foot="alt", keys=False); inert = D.grade(qinf(A), qinf(B_)); a0free = a0_indep(B_)
            pass_ = ho is not None and ho["g1"] == 0 and ho["g2"] == 0 and gr is not None and gr["PASS"] and xc is not None and xc["PASS"] and line and al == 0; rows[-1].update(holdout=None if ho is None else dict(g1=ho["g1"], g2=ho["g2"], d=ho["detail"]), groups=gr, xcop=xc, line175=bool(line), alt_keys=ba, a0_free=bool(a0free), q_inert=bool(inert is not None and inert["gate"] < 1e-9), survivor=bool(pass_))
            if pass_: SURV.append(dict(gram=gram, **rows[-1]))
    rows.sort(key=lambda x: x["gate_exact"]); HOF["cand"][gram] = rows; n0 = [x for x in rows if x["gate_exact"] == 0]; P(f"\n=== {gram}: {len(rows)} regraded; exact L_gate 0 on train: {len(n0)}; survivors {sum(bool(x.get('survivor')) for x in rows)}")
    for x in rows[:8]: P(f"  gate {x['gate_exact']:.3f} (g1 {x['g1']:.2f} g2 {x['g2']:.2f} g3 {x['g3']:.2f} g4 {x['g4_exact']:.2f}, surrogate {x['g4_surrogate']:.2f}) {x['A']} | {x['B']}; bad {x['bad']}" + (f"; holdout {x['holdout'] and (x['holdout']['g1'], x['holdout']['g2'])}, groups {x['groups'] and x['groups']['verdict']}, X-COP {x['xcop'] and (round(x['xcop']['mean'],3), round(x['xcop']['rms'],3))}, line {x['line175']}, a0-free {x['a0_free']}, q inert {x['q_inert']}, SURVIVOR {x['survivor']}" if 'survivor' in x else ""))
    P(f"  Pareto, G1-3 violation vs G4 violation (surrogate), {len(PAR[gram])} points:"); [P(f"    g123 {p['g123']:.3f} g4 {p['g4']:.3f}: {p['A']} | {p['B']}") for p in PAR[gram][:12]]
V = "SURVIVOR" if SURV else ("TRAIN ONLY" if any(x["gate_exact"] == 0 for g in HOF["cand"].values() for x in g) else "NO HIT"); P("\nVERDICT: " + V)
json.dump(HOF, open(os.path.join(HERE, "hall_of_fame.json"), "w"), indent=1, default=float); json.dump(PAR, open(os.path.join(HERE, "pareto.json"), "w"), indent=1, default=str); open(os.path.join(HERE, "discover.out"), "w").write("\n".join(OUT) + "\n")
if SURV: open(os.path.join(HERE, "SURVIVORS.md"), "w").write("# SL1 survivors: candidates from a large search, not laws. Keys and LITTLE THINGS not held out\n\n" + "\n".join(f"- [{'a0-FREE' if s['a0_free'] else 'a0-DEPENDENT'}]{' [q INERT]' if s['q_inert'] else ''} {s['gram']}: A = {s['A']}; B = {s['B']}; nodes {s['nodes']}" for s in SURV) + "\n")
