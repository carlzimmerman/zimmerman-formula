#!/usr/bin/env python3
"""CG1 parts B, C: SPARC profile likelihood on three kernels, rivals on both footings, scrambled-scalar kernel test. --mutate: E = 7 pi, a0 grid x 1.25. kappa = 1/2 FITTED; not theory closed."""
import glob, itertools, json, math, os, resource, sys
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); OUT = []; RES = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
PI = math.pi; Z = math.sqrt(32 * PI / 3); kpc = 3.0857e19; c_l = 2.998e8
FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10); REC_A0 = (c_l / 2) * math.sqrt(6.674e-11 * .685 * 3 * 2.184e-18 ** 2 / (8 * PI * 6.674e-11)); REC_M = c_l * 2.184e-18 / (2 * PI)
GSCALE = 1.25 if MUT else 1.0  # MUTATE: the a0 passed to the kernel is wrong by this factor
K_ = dict(framework=lambda g, a: np.sqrt(g * g + g * a), mcgaugh=lambda g, a: g / (-np.expm1(-np.sqrt(g / a))), simple=lambda g, a: .5 * g + np.sqrt(.25 * g * g + g * a))
UG = np.linspace(.05, 3., 119)
def load():
    gs = []
    for f in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        d = np.genfromtxt(f, comments="#")
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, V, e, Vg, Vd, Vb = (d[:, i] for i in range(6)); m = np.isfinite(R) & np.isfinite(V) & (R > 0) & (V > 0)
        if m.sum() < 3: continue
        gs.append(dict(R=R[m] * kpc, V=V[m], e=np.clip(e[m], 1., None), Vg=Vg[m], Vd=Vd[m], Vb=Vb[m]))
    return gs
def prep(gs):
    out = []
    for g in gs:
        Vb2 = np.sign(g["Vg"]) * g["Vg"] ** 2 + UG[:, None] * g["Vd"] ** 2 + 1.4 * UG[:, None] * g["Vb"] ** 2
        gb = Vb2 * 1e6 / g["R"]; go = (g["V"] * 1e3) ** 2 / g["R"]; ok = (gb > 0) & (go > 0) & np.isfinite(gb); s = g["e"] / g["V"] * 2 / math.log(10)
        out.append(dict(gb=np.where(ok, gb, 1.), lgo=np.log10(np.where(go > 0, go, 1.)), ok=ok, s2=s * s, any=ok.any(1)))
    return out
def chi_gal(p, a0, si, kern):
    r = p["lgo"] - np.log10(K_[kern](p["gb"], a0 * GSCALE)); v = (r * r / (p["s2"] + si * si) * p["ok"]).sum(1); v = np.where(p["any"], v, np.inf); i = int(np.argmin(v))
    return (float(v[i]), int(p["ok"][i].sum())) if np.isfinite(v[i]) else (0., 0)
def prof(ps, a0, si, kern="framework"):
    a = [chi_gal(p, a0, si, kern) for p in ps]; return np.array([x[0] for x in a]), sum(x[1] for x in a), sum(1 for x in a if x[1] > 0)
gs = load(); ps = prep(gs)
lo, hi = .001, .6
for _ in range(45):
    mid = .5 * (lo + hi); v, n, nu = prof(ps, REC_A0, mid)
    if v.sum() / (n - nu - 1) > 1: lo = mid
    else: hi = mid
SI = .5 * (lo + hi); v0, N, NU = prof(ps, REC_A0, SI); DEFL = N / NU
P(f"loaded {len(gs)} galaxies; npts {N}, Upsilon free {NU}; sig_int {SI:.4f} dex (at record's a0 {REC_A0:.4e}); deflation N/n {DEFL:.2f}")
# grid: log spaced, plus exact rivals later by interpolation
AG = np.exp(np.linspace(math.log(.55e-10), math.log(2.0e-10), 261)); LAG = np.log(AG)
def matrix(ps_, kern): return np.array([prof(ps_, a, SI, kern)[0] for a in AG]).T  # gal x a0
def best(curve):
    i = int(np.argmin(curve)); i = min(max(i, 1), len(AG) - 2); y = curve[i - 1:i + 2]; d = y[0] - 2 * y[1] + y[2]; h = LAG[1] - LAG[0]
    return LAG[i] + (.5 * h * (y[0] - y[2]) / d if d > 0 else 0)
def boot(M, n=2000, seed=11):
    rng = np.random.default_rng(seed); ng = M.shape[0]; out = np.empty(n)
    for b in range(n): out[b] = best(M[rng.integers(0, ng, ng)].sum(0))
    return out
LIK = {}
for kern in K_:
    M = matrix(ps, kern); C = M.sum(0); lh = best(C); bs = boot(M); sb = float(bs.std()); cmin = float(np.interp(lh, LAG, C))
    # Dchi2=1 crossings
    d = C - cmin; il = np.where((d[:-1] > 1) & (d[1:] <= 1))[0]; ir = np.where((d[:-1] <= 1) & (d[1:] > 1))[0]; sind = float((LAG[ir[-1] + 1] - LAG[il[0]]) / 2) if len(il) and len(ir) else float("nan")
    LIK[kern] = dict(C=C, a=math.exp(lh), lh=lh, sb=sb, sind=sind, sclu=sind * DEFL ** .5, cmin=cmin, q16=float(np.exp(np.quantile(bs, .16))), q84=float(np.exp(np.quantile(bs, .84))))
    P(f"kernel {kern:<10} best a0 {math.exp(lh)*1e10:.4f}e-10, chi2 min {cmin:.1f}; sigma ln a0: points {100*sind:.2f} %, sqrt(N/n) {100*sind*DEFL**.5:.2f} %, bootstrap {100*sb:.2f} %")
RES["likelihood"] = {k: {x: v[x] for x in ("a", "sb", "sind", "sclu", "cmin", "q16", "q84")} for k, v in LIK.items()}
def dchi(kern, a): return float(np.interp(math.log(a), LAG, LIK[kern]["C"])) - LIK[kern]["cmin"]
# K1 exact, not interpolated
v1 = prof(ps, REC_A0, SI)[0].sum(); v2 = prof(ps, REC_M, SI)[0].sum(); ref = LIK["framework"]; k1a = float(v1 - ref["cmin"]); k1b = float(v2 - ref["cmin"])
# record's min is on its coarser grid at 1.0766; report ours
RES["K1"] = dict(sig_int=SI, d_can=k1a, d_mil=k1b, ok=bool(abs(SI - .0808) < .001 and abs(k1a - 63.9) < .3 and abs(k1b - 5.34) < .3)); P(f"K1 record: sig_int {SI:.4f} vs 0.0808; Dchi2 at {REC_A0:.4e}: {k1a:.2f} vs 63.90; at cH0/2pi {REC_M:.4e}: {k1b:.2f} vs 5.34; tolerance +- 0.3: {RES['K1']['ok']}")
# K4 plant
rng = np.random.default_rng(31); gp = []
a_pl = FOOT["alt"]
for g in gs:
    U = float(np.exp(rng.normal(math.log(.5), .25))); Vb2 = np.sign(g["Vg"]) * g["Vg"] ** 2 + U * g["Vd"] ** 2 + 1.4 * U * g["Vb"] ** 2; gb = Vb2 * 1e6 / g["R"]; ok = gb > 0; go = (g["V"] * 1e3) ** 2 / g["R"]; s = g["e"] / g["V"] * 2 / math.log(10)
    tr = np.where(ok, K_["framework"](np.where(ok, gb, 1.), a_pl * GSCALE) * 10 ** rng.normal(0, np.sqrt(s * s + SI * SI)), go); h = dict(g); h["V"] = np.sqrt(tr * g["R"]) / 1e3; gp.append(h)
Mp = matrix(prep(gp), "framework"); lhp = best(Mp.sum(0)); sbp = float(boot(Mp, 500).std()); RES["K4"] = dict(a=math.exp(lhp), sb=sbp, off=(lhp - math.log(a_pl)) / sbp, ok=bool(abs(lhp - math.log(a_pl)) < 2 * sbp)); P(f"K4 PLANT a0 {a_pl:.4e}: recovered {math.exp(lhp):.4e}, {RES['K4']['off']:+.2f} sigma_boot (sigma {100*sbp:.2f} %, no correlated within-galaxy error in the plant)")
# registry
PL = dict(E=(7 if MUT else 8) * PI, F=3., U=2 * PI, P=4 * PI, V=4 * PI / 3, A=4.)
def members(pl, kset, eset, n):
    out = {}
    names = list(pl)
    for combo in itertools.combinations(names, n):
        for es in itertools.product(eset, repeat=n):
            base = sum(e * math.log(pl[p]) for p, e in zip(combo, es))
            for k in kset: out[(k, combo, es)] = base + math.log(k)
    return out
K3 = [1., 2., .5]; K11 = sorted({p / q for p in range(1, 5) for q in range(1, 5)}); E12 = (-.5, .5); E1 = (-1, -.5, .5, 1)
T = members(PL, K3, E12, 2); S = members(PL, K3, E1, 1); W = members(PL, K11, E1, 2); TS = {k: v for k, v in T.items() if set(k[1]) != {"E", "F"}}
CL = dict(T=T, S=S, W=W, T_strict=TS)
def distinct(d): return np.unique(np.round(np.array(list(d.values())), 9))
CV = {k: distinct(v) for k, v in CL.items()}; RES["class_sizes"] = {k: [len(CL[k]), len(CV[k])] for k in CL}; P(f"class sizes (formal, distinct): { {k: RES['class_sizes'][k] for k in CL} }")
x_Z = math.log(1 / Z); inT = bool(np.min(np.abs(CV["T"] - x_Z)) < 1e-8); inTS = bool(np.min(np.abs(CV["T_strict"] - x_Z)) < 1e-8); RES["K5"] = inT; P(f"K5 a0 x = 1/Z in T: {inT}; distinct value also reachable without the E, F pair: {inTS}")
if inTS:
    for k, v in TS.items():
        if abs(v - x_Z) < 1e-8: P(f"   strict-class spelling of 1/Z: kappa {k[0]}, places {k[1]}, exponents {k[2]}"); RES["strict_spelling"] = [k[0], list(k[1]), list(k[2])]; break
def cover(vals, hw, dex):
    lo_, hi_ = x_Z - dex * math.log(10), x_Z + dex * math.log(10); v = np.sort(vals); a = np.clip(v - hw, lo_, hi_); b = np.clip(v + hw, lo_, hi_); tot = 0.; cur = lo_
    for s, e in zip(a, b):
        if e > cur: tot += e - max(s, cur); cur = max(cur, e)
    return tot / (hi_ - lo_)
def mc(vals, hw, dex, n=2000000, seed=5):
    v = np.sort(vals); x = x_Z + dex * math.log(10) * np.random.default_rng(seed).uniform(-1, 1, n); i = np.searchsorted(v, x); d = np.minimum(np.abs(x - v[np.clip(i, 0, len(v) - 1)]), np.abs(x - v[np.clip(i - 1, 0, len(v) - 1)])); return float((d <= hw).mean())
# windows, as ln a ranges
F = LIK["framework"]; env = [(k["lh"] - 2 * k["sb"], k["lh"] + 2 * k["sb"]) for k in LIK.values()]
WIN = dict(W1=(F["lh"] - 2 * F["sb"], F["lh"] + 2 * F["sb"]), W2=(min(e[0] for e in env), max(e[1] for e in env)), W3=(math.log(.72e-10), math.log(1.68e-10)), W4=(math.log(1.2e-10 * .95), math.log(1.2e-10 * 1.05)))
RES["windows"] = {k: [math.exp(v[0]), math.exp(v[1])] for k, v in WIN.items()}
RATE = {k: Z * v / c_l for k, v in FOOT.items()}
P("\nKERNEL TEST. P = fraction of scrambled scalars with a member of the class in the window. Bits only if the real formula is in the window")
KT = {}
for wn, (a, b) in WIN.items():
    hw = (b - a) / 2; row = dict(hw=hw, range=[math.exp(a), math.exp(b)]); P(f"{wn} a0 in [{math.exp(a)*1e10:.3f}, {math.exp(b)*1e10:.3f}]e-10, half width {100*hw:.1f} % (ln)")
    for cn in ("T", "T_strict", "S", "W"):
        p1 = cover(CV[cn], hw, 1); p05 = cover(CV[cn], hw, .5); m = mc(CV[cn], hw, 1); se = (max(p1 * (1 - p1), 1e-12) / 2e6) ** .5; row[cn] = dict(P_1dex=p1, P_05dex=p05, mc=m, k3=bool(abs(m - p1) <= 4 * se + 1e-9))
        P(f"   class {cn:<9} P {p1:.4f} (+-1 dex), {p05:.4f} (+-0.5 dex), MC {m:.4f}, ceiling bits if it hits {-math.log2(max(p1,1e-300)):.2f}")
    for fn, v in FOOT.items():
        hit = bool(a <= math.log(v) <= b); pt = row["T"]["P_1dex"]; row[fn] = dict(hit=hit, bits_T=-math.log2(pt) if hit else 0.); P(f"   {fn:<9} Z formula {v*1e10:.4f}e-10 {'IN window' if hit else 'no hit'}, bits on T {row[fn]['bits_T']:.3f}")
    KT[wn] = row
RES["kernel_test"] = KT
# scrambled registry
P("\nSCRAMBLED REGISTRY: six places log-uniform [2, 30], class T, fraction with a member in the real window on x = a0/(cR)")
rng = np.random.default_rng(19); RS = {}
idx = [(i, j, ei, ej, k) for i, j in itertools.combinations(range(6), 2) for ei in E12 for ej in E12 for k in K3]; I = np.array([q[0] for q in idx]); J = np.array([q[1] for q in idx]); EI = np.array([q[2] for q in idx]); EJ = np.array([q[3] for q in idx]); LK = np.log([q[4] for q in idx])
LP = np.log(rng.uniform(1, 1, (1, 1))) * 0 + np.log(2) + rng.uniform(0, 1, (20000, 6)) * math.log(15); VALS = LP[:, I] * EI + LP[:, J] * EJ + LK
for wn in WIN:
    for fn in FOOT:
        a, b = WIN[wn]; r = math.log(c_l * RATE[fn]); lo_, hi_ = a - r, b - r; f = float(((VALS >= lo_) & (VALS <= hi_)).any(1).mean()); RS[f"{wn}_{fn}"] = f; P(f"   {wn} {fn:<9} {f:.4f}")
RES["scrambled_registry"] = RS
# power
P("\nPOWER: half width w at which P = 2^-10, +-1 dex")
PW = {}
for cn in ("T", "S", "W"):
    lo_, hi_ = 1e-8, .3
    for _ in range(60):
        mid = (lo_ * hi_) ** .5
        if cover(CV[cn], mid, 1) > 2 ** -10: hi_ = mid
        else: lo_ = mid
    PW[cn] = hi_; P(f"   class {cn}: w = {100*hi_:.4f} %")
RES["power"] = PW
# rivals
RIV = [("Z", Z, "framework kappa=1/2"), ("2pi", 2 * PI, "Milgrom cH0/2pi on alt; c^2 sqrt(L/3)/2pi on canonical"), ("6", 6., "Verlinde 2017 cH/6"), ("8/sqrt3", 8 / 3 ** .5, "sibling c^2 sqrt(L)/8"), ("4pi", 4 * PI, "cH/4pi")]
def smallest(N):
    x = math.log(1 / N)
    for cn in ("S", "T", "W"):
        if np.min(np.abs(CV[cn] - x)) < 1e-8: return cn
    return None
ALLM = np.unique(np.round(np.concatenate([CV["S"], CV["T"], CV["W"]]), 9)); P(f"\nRIVALS, a0 = c R / N. Union of S, T, W has {len(ALLM)} distinct values")
RT = {}
for kern in K_:
    for fn in FOOT:
        r = c_l * RATE[fn]; Lk = LIK[kern]; ag = np.log(np.clip(np.exp(ALLM) * r, AG[0], AG[-1])); inside = (np.exp(ALLM) * r >= AG[0]) & (np.exp(ALLM) * r <= AG[-1]); dm = np.interp(ag, LAG, Lk["C"]) - Lk["cmin"]; dm[~inside] = np.inf
        # evidence denominator on p(ln x) log-uniform +-1 dex about 1/Z
        xs = np.linspace(x_Z - math.log(10), x_Z + math.log(10), 20001); ax = xs + math.log(r); dx = np.interp(ax, LAG, Lk["C"]) - Lk["cmin"]; dx[(ax < LAG[0]) | (ax > LAG[-1])] = np.inf; den = float(np.mean(np.exp(-dx / (2 * DEFL))))
        for nm, Nv, lab in RIV:
            a = r / Nv; d = dchi(kern, a) if AG[0] <= a <= AG[-1] else float("inf"); bits = math.log2(max(math.exp(-d / (2 * DEFL)), 1e-300) / den); cn = smallest(Nv); pen = math.log2(len(CV[cn])); rank = int((dm < d).sum()) + 1
            RT[f"{kern}|{fn}|{nm}"] = dict(a=a, d=d, sig_clu=(d / DEFL) ** .5, sig_boot=(math.log(a) - Lk["lh"]) / Lk["sb"], bits=bits, cls=cn, pen=pen, net=bits - pen, rank=rank, n=len(ALLM), hitW1=bool(WIN["W1"][0] <= math.log(a) <= WIN["W1"][1]) if kern == "framework" else None)
            P(f"  {kern:<9} {fn:<9} N {nm:<7} a0 {a*1e10:.4f} Dchi2 {d:8.2f} = {(d/DEFL)**.5:5.2f} s_clu, {RT[f'{kern}|{fn}|{nm}']['sig_boot']:+6.2f} s_boot; bits {bits:5.2f} class {cn} pen {pen:5.2f} net {bits-pen:6.2f}; rank {rank}/{len(ALLM)}")
RES["rivals"] = RT
# best T member per footing
BT = {}
for fn in FOOT:
    r = c_l * RATE[fn]; vs = np.exp(CV["T"]) * r; k = (vs >= AG[0]) & (vs <= AG[-1]); dv = np.interp(np.log(vs[k]), LAG, F["C"]) - F["cmin"]; i = int(np.argmin(dv)); cnt = int((dv < dchi("framework", FOOT[fn])).sum()); BT[fn] = dict(best_a=float(vs[k][i]), best_N=float(r / vs[k][i]), best_d=float(dv[i]), T_members_better_than_Z=cnt, T_in_grid=int(k.sum())); P(f"class T on {fn}: best member N {BT[fn]['best_N']:.4f} a0 {vs[k][i]*1e10:.4f} Dchi2 {dv[i]:.2f}; members fitting better than Z {cnt} of {int(k.sum())} in range")
RES["best_T"] = BT
# verdict
inW1 = {fn: KT["W1"][fn]["hit"] for fn in FOOT}; bestnet = {fn: max(RIV, key=lambda q: RT[f"framework|{fn}|{q[0]}"]["net"])[0] for fn in FOOT}; pT = KT["W1"]["T"]["P_1dex"]; bitsT = -math.log2(pT); RES["best_net"] = bestnet
lab = "STANDS OUT" if (all(inW1.values()) and all(v == "Z" for v in bestnet.values()) and bitsT >= 10) else "DOES NOT FIT" if not any(inW1.values()) else "FITS ON ONE FOOTING, NOT SPECIAL"; RES["label"] = lab; RES["inW1"] = inW1
P(f"\nVERDICT LABEL: {lab}; inside W1 {inW1}; best Net {bestnet}; class T ceiling on W1 {bitsT:.2f} bits")
K3ok = all(KT[w][c]["k3"] for w in WIN for c in ("T", "T_strict", "S", "W")); RES["K3"] = K3ok; P(f"K3 Monte Carlo vs exact coverage within 4 sigma: {K3ok}")
print(f"K6 RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
json.dump(RES, open(f"cg1_kernel{TAG}.json", "w"), indent=1, sort_keys=True, default=lambda o: o.item() if hasattr(o, "item") else str(o)); open(f"cg1_kernel{TAG}.out", "w").write("\n".join(OUT) + "\n")
fails = [k for k, v in dict(K1=RES["K1"]["ok"], K3=K3ok, K4=RES["K4"]["ok"], K5=RES["K5"]).items() if not v]; P(f"FAILED CHECKS: {fails}"); open(f"cg1_kernel{TAG}.out", "w").write("\n".join(OUT) + "\n"); sys.exit(1 if fails else 0)
