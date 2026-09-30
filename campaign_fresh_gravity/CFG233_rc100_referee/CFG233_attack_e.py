"""CFG233 attack (e): the frozen decision rule: sensitivity map, leave-one-out, bootstrap, permutation, honest total significance."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *
from scipy import stats

start("CFG233_attack_e")
d = load_rc100(); z = d["z"]; n = len(z); zmed = np.median(z); dz = z - zmed
R = {}
f_, r_ = delta_pair(d["D"], d["gbar"], z)
a0c = A0["canonical"]
prim = dict(flat=ts(z, f_), rival=ts(z, r_))
ex = expected_slopes(d["gobs"], z)
print("primary slopes", prim, "expected", ex)
t0 = time.time()
# ------------------------------------------------ 1 sensitivity map
print("\n=== e1 sensitivity map (243 cells, B=2000, seed 233); class per cell")
cells = {}
for zlo, zhi, fw, gc, mc in itertools.product((0.61, 0.8, 1.0), (2.52, 2.3, 2.0), ("all", "0.05-0.95", "0.10-0.90"), ("all", "<3a0", "<a0"), ("none", ">=10.3", ">=10.6")):
    m = (z >= zlo) & (z <= zhi)
    if fw != "all":
        lo, hi = map(float, fw.split("-")); m &= (d["f"] >= lo) & (d["f"] <= hi)
    if gc == "<3a0": m &= d["gbar"] < 3 * a0c
    if gc == "<a0": m &= d["gbar"] < a0c
    if mc != "none": m &= d["logM"] >= float(mc[2:])
    nn = int(m.sum())
    key = f"z{zlo}-{zhi}|f{fw}|g{gc}|M{mc}"
    if nn < 15 or len(np.unique(z[m])) < 5:
        cells[key] = dict(n=nn, small=True); continue
    bs = boot_ts(z[m], [f_[m], r_[m]], 2000, SEED_MAIN)
    cf, cr = ci(bs[0]), ci(bs[1])
    cells[key] = dict(n=nn, small=False, sf=ts(z[m], f_[m]), sr=ts(z[m], r_[m]), ci_f=cf, ci_r=cr, cls=classify(cf, cr))
big = {k: v for k, v in cells.items() if not v["small"]}
from collections import Counter
cnt = Counter(v["cls"] for v in big.values())
print(f"  cells {len(cells)}; usable (n>=15) {len(big)}; class shares: " + ", ".join(f"{c} {cnt[c]} ({cnt[c]/len(big):.2f})" for c in ("W-flat", "W-none", "W-mixed", "W-rival")))
neg = sum(v["sf"] < 0 for v in big.values()); print(f"  flat slope negative in {neg}/{len(big)} usable cells; rival slope CI<0 in {sum(v['ci_r'][1]<0 for v in big.values())}/{len(big)}")
share_ok = (cnt["W-flat"] + cnt["W-none"]) / len(big)
print(f"  share W-flat or W-none: {share_ok:.2f}; W-rival cells: {cnt['W-rival']}; cells whose class differs from the primary W-flat: {len(big)-cnt['W-flat']} ({(len(big)-cnt['W-flat'])/len(big):.2f})")
# by the number of cuts: full-sample-ish cells
full_cells = {k: v for k, v in big.items() if v["n"] >= 90}
print("  cells with n>=90:", {k: (v['n'], v['cls'], round(v['sf'], 3)) for k, v in full_cells.items()})
wr = [(k, v["n"], round(v["sf"], 3), v["cls"]) for k, v in big.items() if v["cls"] == "W-rival"]
print("  W-rival cells:", wr[:10])
R["map"] = dict(counts=dict(cnt), usable=len(big), share_ok=share_ok, cells=cells)
print("  time", round(time.time() - t0, 1))

# ------------------------------------------------ 2 leave-one-out
print("\n=== e2 leave-one-out (100 fits, B=1000, seed 235)")
loo = []
for i in range(n):
    m = np.ones(n, bool); m[i] = False
    bs = boot_ts(z[m], [f_[m], r_[m]], 1000, 235)
    loo.append(dict(i=i, name=d["name"][i], sf=ts(z[m], f_[m]), sr=ts(z[m], r_[m]), cls=classify(ci(bs[0]), ci(bs[1])), hi=ci(bs[0])[1]))
sfs = np.array([l["sf"] for l in loo]); cl = Counter(l["cls"] for l in loo)
print(f"  flat slope over LOO: {sfs.min():+.4f} .. {sfs.max():+.4f} (primary {prim['flat']:+.4f}); max |change| {np.abs(sfs-prim['flat']).max():.4f}; classes: {dict(cl)}; share not W-flat {1-cl['W-flat']/n:.2f}")
infl = np.argsort(-np.abs(sfs - prim["flat"]))[:5]
print("  5 most influential (flat slope on removal):", [(loo[i]["name"], round(loo[i]["sf"], 4)) for i in infl])
m5 = np.ones(n, bool); m5[infl] = False
print(f"  with all 5 removed: flat {ts(z[m5], f_[m5]):+.4f}, rival {ts(z[m5], r_[m5]):+.4f}")
print("  mean of LOO CI upper edges (flat):", float(np.mean([l["hi"] for l in loo])), "; share with upper edge > 0:", float(np.mean([l["hi"] > 0 for l in loo])))
R["loo"] = dict(min=float(sfs.min()), max=float(sfs.max()), classes=dict(cl), top5=[(loo[i]["name"], loo[i]["sf"]) for i in infl], remove5=(ts(z[m5], f_[m5]), ts(z[m5], r_[m5])))

# ------------------------------------------------ 3 bootstrap over discs
print("\n=== e3 bootstrap over discs (N=10000; seeds 233 and 234)")
for seed in (233, 234):
    bs = boot_ts(z, [f_, r_], 10000, seed)
    cf, cr = ci(bs[0]), ci(bs[1])
    print(f"  seed {seed}: flat CI ({cf[0]:+.4f},{cf[1]:+.4f}) rival CI ({cr[0]:+.4f},{cr[1]:+.4f}) class {classify(cf, cr)}; share flat slope > 0: {(bs[0]>0).mean():.4f}; share rival slope > -0.030: {(bs[1]>-0.030).mean():.4f}; SD {bs[0].std():.4f}/{bs[1].std():.4f}")
    R[f"boot{seed}"] = dict(ci_f=cf, ci_r=cr, share_pos=float((bs[0] > 0).mean()), share_rival_gt=float((bs[1] > -0.03).mean()), cls=classify(cf, cr))
# difference 62 vs 38 (bootstrapped within groups)
m41, *_ = rc41_match(d)
i62, i38 = np.where(~m41)[0], np.where(m41)[0]
rng = np.random.default_rng(233); dd_ = []
for _ in range(4000):
    a = rng.choice(i62, len(i62)); b = rng.choice(i38, len(i38))
    dd_.append(ts(z[a], f_[a]) - ts(z[b], f_[b]))
obsd = ts(z[i62], f_[i62]) - ts(z[i38], f_[i38])
print(f"  flat-slope difference (62 non-RC41 minus 38 RC41): {obsd:+.4f}, bootstrap SD {np.std(dd_):.4f} -> {obsd/np.std(dd_):+.2f} sigma; 95% CI ({np.percentile(dd_,2.5):+.3f},{np.percentile(dd_,97.5):+.3f})")
R["diff62_38"] = dict(obs=obsd, sd=float(np.std(dd_)))

# ------------------------------------------------ 4 permutation
print("\n=== e4 permutation null (N=20000, seed 236)")
rng = np.random.default_rng(236); NP = 20000
zs = np.array([rng.permutation(z) for _ in range(NP)])
s_axis_f = ts_batch(zs, np.broadcast_to(f_, (NP, n))); s_axis_r = ts_batch(zs, np.broadcast_to(r_, (NP, n)))     # regression axis shuffled only
drs = delta_of(np.broadcast_to(d["D"], (NP, n)), np.broadcast_to(d["gbar"], (NP, n)), zs, "rival")
s_full_r = ts_batch(zs, drs)                                                                                       # a0(z) shuffled together with the axis
p2 = lambda null, x: float((np.abs(null - null.mean()) >= abs(x - null.mean())).mean())
print(f"  flat slope {prim['flat']:+.4f}: two-sided p (axis shuffled) {p2(s_axis_f, prim['flat']):.4f}; null SD {s_axis_f.std():.4f}")
print(f"  rival slope {prim['rival']:+.4f}: two-sided p vs axis-shuffled null (mean {s_axis_r.mean():+.4f}, SD {s_axis_r.std():.4f}) {p2(s_axis_r, prim['rival']):.5f}; vs full-shuffle null (mean {s_full_r.mean():+.4f}, SD {s_full_r.std():.4f}, the mechanical -0.5 log E term stays) {p2(s_full_r, prim['rival']):.4f}")
R["perm"] = dict(p_flat=p2(s_axis_f, prim["flat"]), p_rival_axis=p2(s_axis_r, prim["rival"]), p_rival_full=p2(s_full_r, prim["rival"]), full_null_mean=float(s_full_r.mean()))
# label permutation of the RC41 split
lab = np.array([rng.permutation(m41) for _ in range(4000)])
dnull = []
for L in lab:
    a, b = np.where(~L)[0], np.where(L)[0]
    dnull.append(ts(z[a], f_[a]) - ts(z[b], f_[b]))
print(f"  RC41-split label permutation (N=4000): observed difference {obsd:+.4f}; two-sided p {float((np.abs(dnull)>=abs(obsd)).mean()):.3f}")
R["perm"]["p_split"] = float((np.abs(dnull) >= abs(obsd)).mean())

# ------------------------------------------------ 5 honest total sigma
print("\n=== e5 honest total significance: declared Gaussian priors on the analysis's own inputs (N=20000, seed 233)")
rc = load_rc41(); m41n, _, _, rc_ = rc41_match(d)
idx = {r["id"].replace("_", " "): r for r in rc_}
lmu = np.array([float(idx[nm]["logMgas"]) - float(idx[nm]["logMstar_SED"]) for nm in d["name"] if nm in idx]); zz = np.array([z[i] for i, nm in enumerate(d["name"]) if nm in idx])
cb, *_ = np.linalg.lstsq(np.vstack([zz, np.ones(len(zz))]).T, lmu, rcond=None)
mu = 10 ** (cb[1] + cb[0] * z)
P = 2 * d["s0"] ** 2 * 1.678
sdf, sdr = 0.0185, 0.0188
expR = ex["rival"][0]
def honest(sig_t, sig_q=0.02, sig_tau=0.02, N=20000, seed=233, press=True):
    rng = np.random.default_rng(seed)
    t = rng.normal(0, sig_t, N); q = rng.normal(0, sig_q, N); tau = rng.normal(0, sig_tau, N)
    s = rng.uniform(1, 3, N) if press else np.full(N, 3.0)
    sf_out = np.empty(N); sr_out = np.empty(N); clipped = 0
    for a in range(0, N, 2000):
        sl = slice(a, a + 2000)
        kf = (1 + mu)[None] / (1 + mu[None] * 10 ** (t[sl, None] * dz[None])) * 10 ** (tau[sl, None] * dz[None])
        Vc2 = d["Vc"][None] ** 2 - (1 - s[sl, None] / 3) * P[None]
        Vc2 = Vc2 * 10 ** (2 * q[sl, None] * dz[None])
        Vb2 = (1 - d["f"])[None] * d["Vc"][None] ** 2 / kf
        f2 = 1 - Vb2 / Vc2
        clipped += int(((f2 <= 0.01) | (f2 >= 0.99) | (Vc2 <= 0)).sum())
        f2 = np.clip(f2, 0.01, 0.99)
        go = np.maximum(Vc2, 1.0) * 1e6 / (d["Re"][None] * KPC); gb = (1 - f2) * go; D = 1 / (1 - f2)
        zb = np.broadcast_to(z, D.shape)
        sf_out[sl] = ts_batch(zb, delta_of(D, gb, zb, "flat")); sr_out[sl] = ts_batch(zb, delta_of(D, gb, zb, "rival"))
    return sf_out, sr_out, clipped / (N * n)
res5 = {}
for sig_t in (0.0, 0.05, 0.10, 0.20):
    sfo, sro, clp = honest(sig_t)
    sd_mod_f, sd_mod_r = sfo.std(), sro.std()
    tot_f = (expR - prim["flat"]) / math.sqrt(sdf ** 2 + sd_mod_f ** 2)     # flat-slope side, expected minus observed
    tot_r = (0 - prim["rival"]) / math.sqrt(sdr ** 2 + sd_mod_r ** 2)
    tdraw_f = (expR - sfo) / sdf; tdraw_r = (0 - sro) / sdr
    pmin3 = float(np.mean((tdraw_f > 3) & (tdraw_r > 3))); pmin4 = float(np.mean((tdraw_f > 4) & (tdraw_r > 4)))
    res5[sig_t] = dict(mean_f=float(sfo.mean()), sd_f=float(sd_mod_f), mean_r=float(sro.mean()), sd_r=float(sd_mod_r), tot_f=tot_f, tot_r=tot_r, p3=pmin3, p4=pmin4, clipped=clp,
                       p3f=float((tdraw_f > 3).mean()), p4f=float((tdraw_f > 4).mean()))
    print(f"  sigma_t={sig_t:.2f} dex/z (q~N(0,0.02), tau~N(0,0.02), s~U[1,3]): modified flat slope mean {sfo.mean():+.4f} SD {sd_mod_f:.4f}; total tension flat-slope-vs-rival-exp {tot_f:.2f}, rival-slope-vs-0 {tot_r:.2f}; P(both > 3) {pmin3:.3f}, P(both > 4) {pmin4:.3f} (flat side alone > 3: {res5[sig_t]['p3f']:.3f}); clipped fraction {clp:.3f}")
# without the pressure prior
sfo, sro, clp = honest(0.10, press=False)
print(f"  central prior with the pressure scale fixed at the table (s=3): SD {sfo.std():.4f}; total tension flat {(expR-prim['flat'])/math.sqrt(sdf**2+sfo.std()**2):.2f}")
R["honest"] = res5
# POST-FREEZE decomposition (labelled): which declared prior dominates the total sigma
print("  POST-FREEZE decomposition of the modified-slope SD by source (one source active at a time; flat slope):")
dec = {}
for lab, kw in (("gas tilt t ~ N(0,0.10)", dict(sig_t=0.10, sig_q=0.0, sig_tau=0.0, press=False)), ("V_c tilt q ~ N(0,0.02)", dict(sig_t=0.0, sig_q=0.02, sig_tau=0.0, press=False)),
                ("M* tilt tau ~ N(0,0.02)", dict(sig_t=0.0, sig_q=0.0, sig_tau=0.02, press=False)), ("pressure s ~ U[1,3]", dict(sig_t=0.0, sig_q=0.0, sig_tau=0.0, press=True))):
    a_, b_, c_ = honest(**kw)
    dec[lab] = dict(mean=float(a_.mean()), sd=float(a_.std()), clipped=c_)
    print(f"    {lab:26}: mean {a_.mean():+.4f}, SD {a_.std():.4f} (clipped fraction {c_:.3f}); tension if it were the only systematic: {(expR-prim['flat'])/math.sqrt(sdf**2+a_.std()**2):.2f}")
R["honest_decomp"] = dec
cen = res5[0.10]
print(f"\n  central prior (sigma_t 0.10): total tension {cen['tot_f']:.2f} / {cen['tot_r']:.2f} sigma; map share W-flat|W-none {share_ok:.2f}; W-rival cells {cnt['W-rival']}; rule: survives if tension >= 4 AND share >= 0.70 AND no W-rival: "
      + ("SURVIVES" if min(cen['tot_f'], cen['tot_r']) >= 4 and share_ok >= 0.7 and cnt['W-rival'] == 0 else ("WEAKENED" if min(cen['tot_f'], cen['tot_r']) >= 3 and share_ok >= 0.5 else "FAILS")))
print(f"  class stability: map cells not W-flat {(len(big)-cnt['W-flat'])/len(big):.2f} (line 0.40); LOO fits not W-flat {1-cl['W-flat']/n:.2f} (line 0.30)")
savejson("CFG233_attack_e", R)
print("total time", round(time.time() - t0, 1))
