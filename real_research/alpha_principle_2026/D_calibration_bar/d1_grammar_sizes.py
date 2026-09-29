"""D1: grammar sizes, expected chance hits at 1e-3/1e-5/1e-9, decoy calibration, self-tests. See D_PREREGISTRATION.md.
Usage: python3 d1_grammar_sizes.py [MUTATE]   (MUTATE mis-scales the predicted density by 1/50 in the flatness test and must exit 1)"""
import sys, json, math, time
import numpy as np
import bar_lib as B

MUTATE = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
W = 1e-2
TOLS = [1e-3, 1e-5, 1e-9]
FAIL = []
cal = {}
out = {}


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        FAIL.append(name)


def flatness(arr, tag):
    """S3: predicted lambda(1e-3) from the w=1e-2 window vs observed count in the 1e-3 window, on 100 decoys."""
    dec = B.decoys(400)[:100]
    pred, obs = [], []
    for c in dec:
        c2 = B.count_window(arr, c, 1e-2)
        c3 = B.count_window(arr, c, 1e-3)
        pred.append(c2 / 10.0 * (0.02 if MUTATE else 1.0))
        obs.append(c3)
    pred, obs = np.array(pred), np.array(obs)
    ratio = pred.sum() / max(obs.sum(), 1)
    ok = 0.8 <= ratio <= 1.25
    check(f"S3 flatness {tag}: sum(pred)/sum(obs) in [0.8,1.25]", ok, f"ratio={ratio:.3f}")
    return ratio


def decoy_stats(arr, w):
    d = B.decoys(400)
    c = np.array([B.count_window(arr, x, w) for x in d])
    return c.mean(), c.std()


for N in (6, 12):
    t0 = time.time()
    g = B.Grammar(N)
    g.build_E2()
    print(f"\n=== N = {N} (atoms {N}+3 = {len(g.avals)}) ===  build {time.time()-t0:.1f}s")
    print(f"  L1 distinct={g.L1.size} (syntactic {g.L1s});  B1 distinct={g.B1.size};  T1 distinct={g.T1.size} (syntactic {g.T1s})")
    T2tuples = 5 * (2 * 5 * g.L1.size * g.T1.size)  # tuples over deduped subexpressions, both orders, 5 ops, 5 root decorations
    dup2 = g.T2.size / T2tuples
    print(f"  E1: distinct={g.E1.size:,}  syntactic={g.E1s:,}")
    print(f"  E2: distinct={g.E2.size:,}  T2(2-op) distinct={g.T2.size:,}  syntactic(formula)={g.E2s:,}  tuples={T2tuples:,}  dup ratio distinct/tuples={dup2:.3f}")
    for tag, arr, Nd, Nsyn in (("E1", g.E1, g.E1.size, g.E1s), ("E2", g.E2, g.E2.size, g.E2s)):
        cw = B.count_window(arr, B.T, W)
        cw3 = B.count_window(arr, B.T, 1e-3)
        Dens = cw / (2 * W)                    # distinct values per unit relative deviation at T
        rho = Dens / Nd
        m3, s3 = decoy_stats(arr, 1e-3)
        z = (cw3 - m3) / max(s3, 1e-9)
        print(f"  {tag}(N={N}): count in |dv/T|<1e-2 = {cw:,}; in 1e-3 = {cw3:,}; density/unit-rel = {Dens:,.0f}; rho_frac = {rho:.4f} per unit ln; bits = {math.log2(Nd):.1f}")
        print(f"     decoys (400, w=1e-3): mean={m3:.1f} sd={s3:.1f}; real-target count z-score = {z:+.2f}")
        rows = []
        for tol in TOLS:
            lam = B.lam_from_counts(cw, W, tol)
            found = B.count_window(arr, B.T, tol)
            p = B.p_from_lam(lam)
            bits = math.log2(1.0 / (2 * tol * rho))
            print(f"     tol {tol:.0e}: expected chance hits lambda={lam:.4g}  P(>=1)={p:.4g}  found at real target={found}  match-bits={bits:.1f}")
            rows.append(dict(tol=tol, lam=lam, p=p, found=found, match_bits=bits))
        flatness(arr, f"{tag}(N={N})")
        cal[f"{tag}_{N}"] = dict(N_distinct=int(Nd), N_syntactic=int(Nsyn), density_per_rel=Dens, rho_frac=rho, bits=math.log2(Nd), rows=rows)
    # names of E2 hits at 1e-6 (a flavour of what chance produces) and everything at 1e-9
    h9 = g.find_hits_E2(B.T, 1e-9)
    h6 = g.find_hits_E2(B.T, 1e-6, limit=8)
    print(f"  E2(N={N}) expressions within 1e-9 of T (second pass, provenance): {len(h9)} {h9[:5]}")
    print(f"  E2(N={N}) sample of expressions within 1e-6 (first 8): {[(s, f'{v:.9f}') for s, v in h6]}")
    cal[f"E2_{N}"]["hits_1e-9"] = [s for s, _ in h9]
    # ---- E3 Monte Carlo
    rng = np.random.default_rng(20260928 + N)
    n1 = 2 * 5 * g.L1.size * g.T2.size
    n2 = 5 * g.T1.size ** 2
    N3t = 5 * (n1 + n2)
    M = 40_000_000
    chunk = 4_000_000
    hit = 0
    hit3 = 0
    for _ in range(M // chunk):
        part1 = rng.random(chunk) < n1 / (n1 + n2)
        op = rng.integers(0, 5, chunk)
        rd = rng.integers(0, 5, chunk)
        order = rng.integers(0, 2, chunk)
        li = rng.integers(0, g.L1.size, chunk)
        tj = rng.integers(0, g.T2.size, chunk)
        a1 = rng.integers(0, g.T1.size, chunk)
        a2 = rng.integers(0, g.T1.size, chunk)
        X = np.where(part1, np.where(order == 0, g.L1[li], g.T2[tj]), g.T1[a1])
        Y = np.where(part1, np.where(order == 0, g.T2[tj], g.L1[li]), g.T1[a2])
        r = np.empty(chunk)
        for o in range(5):
            m = op == o
            r[m] = B.binary(o, X[m], Y[m])
        for u in range(5):
            m = rd == u
            if u:
                r[m] = B.unary(u, r[m])
        ok = B.clean(r)
        hit += int(((r > B.T * (1 - W)) & (r < B.T * (1 + W)) & ok).sum())
        hit3 += int(((r > B.T * (1 - 1e-3)) & (r < B.T * (1 + 1e-3)) & ok).sum())
    f = hit / M
    D3 = N3t * f / (2 * W)
    dupE2 = dup2
    print(f"  E3(N={N}) MC (M={M:,}): tuples={N3t:,.3e}; window fraction={f:.3e}; density/unit-rel (syntactic)={D3:,.3e}; cross-check 1e-3 window scaled: {N3t*hit3/M/(2e-3):,.3e}")
    rows = []
    for tol in TOLS:
        lam_syn = D3 * 2 * tol
        lam_est = lam_syn * dupE2
        print(f"     tol {tol:.0e}: lambda_syntactic={lam_syn:.4g}  lambda_est(E2 dup ratio {dupE2:.2f})={lam_est:.4g}  P(>=1)_est={B.p_from_lam(lam_est):.4g}")
        rows.append(dict(tol=tol, lam_syn=lam_syn, lam_est=lam_est, p_est=B.p_from_lam(lam_est)))
    cal[f"E3_{N}"] = dict(N_tuples=N3t, N_est=N3t * dupE2, density_per_rel_syn=D3, rho_frac=D3 / N3t, dup_ratio=dupE2, rows=rows)

# ------- hypotheses H1, H2
E2r = {r["tol"]: r for r in cal["E2_12"]["rows"]}
E3r = {r["tol"]: r for r in cal["E3_12"]["rows"]}
print("\n=== Hypotheses ===")
h1 = 1e7 <= cal["E2_12"]["N_distinct"] <= 1e9 and E2r[1e-3]["lam"] > 100
h2a = 1e-4 <= E2r[1e-9]["lam"] <= 1e-1
h2b = 0.1 <= E3r[1e-9]["lam_est"] <= 100
print(f"  H1 (E2(12) 1e7..1e9 distinct, lambda(1e-3)>100): {'TRUE' if h1 else 'FALSE'}  N={cal['E2_12']['N_distinct']:,} lambda={E2r[1e-3]['lam']:.3g}")
print(f"  H2 (E2(12) lambda(1e-9) in [1e-4,1e-1]): {'TRUE' if h2a else 'FALSE'}  lambda={E2r[1e-9]['lam']:.3g};  (E3(12) lambda(1e-9) in [0.1,100]): {'TRUE' if h2b else 'FALSE'}  lambda={E3r[1e-9]['lam_est']:.3g}")
cal["H1"] = bool(h1); cal["H2a"] = bool(h2a); cal["H2b"] = bool(h2b)

# ------- S1, S2 through the shared bar
print("\n=== Self-tests through the shared bar ===")
rho = cal["E2_12"]["rho_frac"]
e1n = cal["E1_12"]["N_distinct"]
r_pos = B.evaluate(1e-12, e1n, cal["E1_12"]["rho_frac"], predicted_precision=0.0)
r_neg = B.evaluate(1e-12, 1e15, cal["E1_12"]["rho_frac"])
check("S1 positive control: 1e-12 match in a truthfully declared E1(12) family clears p and precision", r_pos["c1_lookelsewhere"] and r_pos["c2_precision"], f"p={r_pos['p']:.2e}")
check("S1b same match in a mis-declared 1e15-size family is rejected", not r_neg["c1_lookelsewhere"], f"p={r_neg['p']:.3f}")
g2 = B.Grammar(12); g2.build_E2()
lo, hi = np.searchsorted(g2.E2, B.T * (1 - 1e-3)), np.searchsorted(g2.E2, B.T * (1 + 1e-3))
hits = g2.E2[lo:hi]
sel = np.random.default_rng(2).choice(hits, min(1000, hits.size), replace=False)
rej = 0
for v in sel:
    r = B.evaluate(abs(v / B.T - 1), cal["E2_12"]["N_distinct"], rho)
    rej += (not r["clears"])
check("S2 negative control: all sampled E2 hits at 1e-3 are rejected", rej == len(sel), f"{rej}/{len(sel)} rejected of {hits.size:,} hits")
flat = flatness(g2.E2, "E2(12) repeated")
# reproducibility
cal2 = B.count_window(g2.E2, B.T, W)
check("V1 reproducibility: E2(12) window count identical on rebuild", cal2 == B.count_window(B.Grammar(12).build_E2(), B.T, W))

json.dump(cal, open("calibration_MUTATE.json" if MUTATE else "calibration.json", "w"), indent=1, default=float)
print("\nFAILED:", FAIL if FAIL else "none")
sys.exit(1 if FAIL else 0)
