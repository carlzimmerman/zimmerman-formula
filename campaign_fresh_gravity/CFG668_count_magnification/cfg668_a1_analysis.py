"""CFG668 A1 analysis (criteria 461d16c55). Per survey: R = N(behind clusters)/N(blank) per annulus x mag bin x photo-z gap;
slope s from blank counts; verdict per the frozen rules; combined KiDS+DES by inverse variance. MUTATE=1: half the blanks play clusters."""
import json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE") == "1"
ANN = [(0, 2), (2, 4), (4, 6)]; MAG = [(20, 22), (22, 23), (23, 24)]; GAPS = [0.1, 0.2, 0.3, 0.4, 0.5]
allc = np.loadtxt(os.path.join(HERE, "redmapper_all_positions.tsv"))
def near_any(ra, dec):
    d = np.degrees(np.arccos(np.clip(np.sin(np.radians(dec))*np.sin(np.radians(allc[:,1])) + np.cos(np.radians(dec))*np.cos(np.radians(allc[:,1]))*np.cos(np.radians(ra-allc[:,0])), -1, 1)))
    return (d < 0.25).any()
def load(sv):
    meta = json.load(open(os.path.join(HERE, f"cfg668_a1_{sv}_meta.json"))); raw = np.load(os.path.join(HERE, f"cfg668_a1_{sv}_raw.npz"))
    pts = [(m, raw[f"p{i}"]) for i, m in enumerate(meta) if m["ok"]]
    med = np.median([len(g) for m, g in pts if m["kind"] == "rnd" and len(g) > 0])
    pts = [(m, g) for m, g in pts if len(g) >= 0.7 * med]                       # footprint/edge cut (frozen)
    cl = [(m, g) for m, g in pts if m["kind"] == "cl"]
    bl = [(m, g) for m, g in pts if m["kind"] == "rnd" and not near_any(m["ra"], m["dec"])]
    if MUT:
        rng = np.random.default_rng(668); idx = rng.permutation(len(bl)); h = len(bl)//2
        cl, bl = [bl[i] for i in idx[:h]], [bl[i] for i in idx[h:]]
    return cl, bl, med
def cube(pts, gap):
    out = np.zeros((len(pts), len(ANN), len(MAG)))
    for k, (m, g) in enumerate(pts):
        g = g[g[:, 2] > m["z"] + gap]
        for i, (a, b) in enumerate(ANN):
            sel = (g[:, 0] >= a) & (g[:, 0] < b)
            for j, (m0, m1) in enumerate(MAG): out[k, i, j] = (sel & (g[:, 1] >= m0) & (g[:, 1] < m1)).sum()
    return out
def ratio_boot(C, B, nb=2000, seed=1):
    rng = np.random.default_rng(seed); R = C.mean(0) / B.mean(0)
    bs = np.array([C[rng.integers(0, len(C), len(C))].mean(0) / B[rng.integers(0, len(B), len(B))].mean(0) for _ in range(nb)])
    return R, bs.std(0)
def slopes(bl, gap):
    r = np.concatenate([g[g[:, 2] > m["z"] + gap][:, 1] for m, g in bl]); s = []
    for m0, m1 in MAG:
        h, e = np.histogram(r, bins=np.arange(m0, m1 + 1e-9, 0.25)); c = 0.5 * (e[1:] + e[:-1]); ok = h > 0
        s.append(float(np.polyfit(c[ok], np.log10(h[ok]), 1)[0]))
    return s
def verdict(R, sig, s):
    z = (R - 1) / sig; flat = [j for j in range(3) if s[j] < 0.4]; steep = [j for j in range(3) if s[j] > 0.4]
    for i in (0, 1):
        if flat and steep and any(z[i, j] <= -2 for j in flat) and any(R[i, j] >= 1 for j in steep): return "LENSING"
    if all(z[i, j] <= -2 for i in (0, 1) for j in range(3)) or any(all(z[i, j] <= -2 for j in range(3)) for i in (0, 1)): return "OBSCURATION"
    if any(all(z[i, j] >= 2 for j in range(3)) for i in (0, 1)): return "CONTAMINATED"
    if np.all(np.abs(z) < 2): return "NULL"
    return "MIXED (no frozen pattern)"
res = {"mutate": MUT}; comb = {}
for sv in ["kids", "des"]:
    if not os.path.exists(os.path.join(HERE, f"cfg668_a1_{sv}_meta.json")): continue
    cl, bl, med = load(sv); res[sv] = {"n_clusters": len(cl), "n_blank": len(bl), "median_blank_total": float(med), "gaps": {}}
    print(f"\n=== {sv.upper()}  clusters {len(cl)}  blank fields {len(bl)}  MUTATE={MUT}")
    for gap in GAPS:
        C, B = cube(cl, gap), cube(bl, gap); R, sig = ratio_boot(C, B); s = slopes(bl, gap); v = verdict(R, sig, s)
        res[sv]["gaps"][gap] = dict(slope=s, N_cl=C.mean(0).tolist(), N_bl=B.mean(0).tolist(), R=R.tolist(), sig=sig.tolist(), verdict=v)
        comb.setdefault(gap, []).append((R, sig, s))
        print(f"gap +{gap}: slopes s = " + ", ".join(f"{x:.2f}" for x in s) + f"   verdict: {v}")
        for i, a in enumerate(ANN):
            print(f"   {a[0]}-{a[1]}'  " + "   ".join(f"r{MAG[j][0]}-{MAG[j][1]}: {C.mean(0)[i,j]:6.2f}/{B.mean(0)[i,j]:6.2f} R={R[i,j]:.3f}±{sig[i,j]:.3f}" for j in range(3)))
print("\n=== COMBINED (inverse variance)")
res["combined"] = {}
for gap, L in comb.items():
    w = np.array([1/x[1]**2 for x in L]); R = (np.array([x[0] for x in L]) * w).sum(0) / w.sum(0); sig = 1/np.sqrt(w.sum(0))
    s = list(np.mean([x[2] for x in L], 0)); v = verdict(R, sig, s)
    res["combined"][gap] = dict(R=R.tolist(), sig=sig.tolist(), slope=s, verdict=v)
    print(f"gap +{gap}: verdict {v}   0-2': " + "  ".join(f"R={R[0,j]:.3f}±{sig[0,j]:.3f}(s={s[j]:.2f})" for j in range(3)))
json.dump(res, open(os.path.join(HERE, "cfg668_a1_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)
