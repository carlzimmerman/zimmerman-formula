"""CFG668 A3 + A3G (criteria 87dbbb55b, eeb916a58): quasar magnification beyond cluster baryons (8-40'), self-calibrated against
each pointing's own 60-90' ring, and the lens-geometry fit K_b = A*beta_b + C with beta = D_ls/D_s from raw DESI DR2 BAO.
No cosmology model. MUTATE=1: half the blanks play clusters."""
import json, os, numpy as np, gzip
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE") == "1"
# ---- raw geometry: DESI DR2 BAO (arXiv 2503.14738) D_M/r_d; BGS D_V converted with D_H extrapolated from LRG1/LRG2 ----
zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DM = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DH_bgs = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); DM_bgs = np.sqrt(7.942**3 / (0.295 * DH_bgs))
zz = np.r_[0, 0.295, zb]; dd = np.r_[0, DM_bgs, DM]; pch = PchipInterpolator(zz, dd)
def DMf(z):
    z = np.asarray(z, float); out = pch(np.minimum(z, 2.33))
    hi = z > 2.33   # beyond Lya: D_H ∝ (1+z)^-1.5 from 8.632 at 2.33, integrated analytically
    out[hi] = 38.988 + 8.632 * (1 + 2.33)**1.5 * 2 * ((1 + 2.33)**-0.5 - (1 + z[hi])**-0.5)
    return out
def beta(zl, zs): return np.where(zs > zl, 1 - DMf(zl) / DMf(np.maximum(zs, 1e-6)), 0.0)
# ---- pointings ----
def xyz(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec); return np.c_[np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)]
def chord(am): return 2*np.sin(np.radians(am/60)/2)
def readtsv(fn):
    rows = []
    for l in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        p = l.strip().split("\t")
        if len(p) != 4: continue
        try: rows.append([float(x) for x in p])
        except ValueError: pass
    return np.array(rows)
cl = readtsv(os.path.join(HERE, "redmapper_all_z01_06.tsv")); cl = cl[cl[:, 3] >= 20]
tcl = cKDTree(xyz(cl[:, 0], cl[:, 1]))
sel = cl[:, 2] >= 0.2; C = cl[sel, :3]
# jackknife patches: 6 Dec bands x 8 RA slices, equal count over the selected clusters
patch = np.zeros(len(C), int); ob = np.argsort(C[:, 1]); bands = np.array_split(ob, 6)
for bi, b in enumerate(bands):
    for si, s in enumerate(np.array_split(b[np.argsort(C[b, 0])], 8)): patch[s] = bi*8 + si
rng = np.random.default_rng(668); reps = 3
a = rng.uniform(0, 2*np.pi, (len(C), reps)); s = rng.uniform(1, 3, (len(C), reps))
bra = (C[:, :1] + s*np.cos(a)/np.maximum(0.2, np.cos(np.radians(C[:, 1:2])))) % 360; bdec = np.clip(C[:, 1:2] + s*np.sin(a), -89.9, 89.9)
B = np.c_[bra.ravel(), bdec.ravel(), np.repeat(C[:, 2], reps)]; bpatch = np.repeat(patch, reps)
keep = np.array([len(x) == 0 for x in tcl.query_ball_point(xyz(B[:, 0], B[:, 1]), chord(15))]); B, bpatch = B[keep], bpatch[keep]
if MUT:
    idx = rng.permutation(len(B)); h = len(B)//2; C, patch, B, bpatch = B[idx[:h]], bpatch[idx[:h]], B[idx[h:]], bpatch[idx[h:]]
ANN = [(0, 4), (8, 12), (12, 20), (20, 40), (60, 90)]; AREA = np.array([b*b - a*a for a, b in ANN], float)
CATN = ["FG", "B1", "B2", "B3", "A3bg"]; BETA_EDGES = [(0.0, 0.55), (0.55, 0.70), (0.70, 1.01)]
CATS = {"quaia": ("quaia_g20_ra_dec_z_g.tsv.gz", [(17, 19.0), (19.0, 19.6), (19.6, 20.0)]),
        "dr16q": ("dr16q_ra_dec_z_imag.tsv.gz", [(14, 19.5), (19.5, 20.5), (20.5, 22)])}
def cube(P, q, tq, mags):
    X = xyz(P[:, 0], P[:, 1]); out = np.zeros((len(P), len(ANN), len(mags), len(CATN)), np.float32); mlist = [[] for _ in CATN]
    for k, L in enumerate(tq.query_ball_point(X, chord(90))):
        if not L: continue
        qq = q[np.array(L)]; d = np.degrees(np.arccos(np.clip(xyz(qq[:, 0], qq[:, 1]) @ X[k], -1, 1)))*60; zl = P[k, 2]
        b = beta(zl, qq[:, 2])
        cats = [qq[:, 2] < zl - 0.1] + [(qq[:, 2] > zl) & (b > lo) & (b < hi) if lo == 0 else (b >= lo) & (b < hi) for lo, hi in BETA_EDGES] + [qq[:, 2] > zl + 0.5]
        ai = np.full(len(d), -1)
        for i, (r0, r1) in enumerate(ANN): ai[(d >= r0) & (d < r1)] = i
        for j, (m0, m1) in enumerate(mags):
            mj = (qq[:, 3] >= m0) & (qq[:, 3] < m1) & (ai >= 0)
            for c, cm in enumerate(cats):
                np.add.at(out[k, :, j, c], ai[mj & cm], 1)
    return out
def betabar(P, q, tq, cidx):  # mean beta of blank pairs in 8-40' per beta-bin
    X = xyz(P[:, 0], P[:, 1]); acc = []
    for k, L in enumerate(tq.query_ball_point(X, chord(40))):
        if not L: continue
        qq = q[np.array(L)]; d = np.degrees(np.arccos(np.clip(xyz(qq[:, 0], qq[:, 1]) @ X[k], -1, 1)))*60
        acc.append(beta(P[k, 2], qq[d >= 8, 2]))
    b = np.concatenate(acc); lo, hi = BETA_EDGES[cidx]; m = (b > lo) & (b < hi) if lo == 0 else (b >= lo) & (b < hi)
    return float(b[m].mean())
def slope_from(Bc, mags, mag_list_counts):
    return mag_list_counts
res = {"mutate": MUT, "DM_bgs_derived": float(DM_bgs)}; stash = {}
for name, (fn, mags) in CATS.items():
    q = readtsv(os.path.join(HERE, fn)); q = q[np.isfinite(q).all(1)]; tq = cKDTree(xyz(q[:, 0], q[:, 1]))
    n30c = np.array([len(x) for x in tq.query_ball_point(xyz(C[:, 0], C[:, 1]), chord(30))]); n30b = np.array([len(x) for x in tq.query_ball_point(xyz(B[:, 0], B[:, 1]), chord(30))])
    med = np.median(n30b); okc, okb = n30c >= 0.5*med, n30b >= 0.5*med
    Cc, Bc = cube(C[okc], q, tq, mags), cube(B[okb], q, tq, mags)
    # slopes per (mag bin, category) from blank quasars at 8-40', 0.2-mag steps (A2 method)
    sl = np.zeros((len(mags), len(CATN)))
    Xb = xyz(B[okb, 0], B[okb, 1]); mm = [[] for _ in CATN]
    for k, L in enumerate(tq.query_ball_point(Xb, chord(40))):
        if not L: continue
        qq = q[np.array(L)]; d = np.degrees(np.arccos(np.clip(xyz(qq[:, 0], qq[:, 1]) @ Xb[k], -1, 1)))*60; qq = qq[d >= 8]; zl = B[okb][k, 2]
        b = beta(zl, qq[:, 2])
        cats = [qq[:, 2] < zl - 0.1] + [(qq[:, 2] > zl) & (b > lo) & (b < hi) if lo == 0 else (b >= lo) & (b < hi) for lo, hi in BETA_EDGES] + [qq[:, 2] > zl + 0.5]
        for c, cm in enumerate(cats): mm[c].extend(qq[cm, 3])
    for c in range(len(CATN)):
        m_all = np.array(mm[c])
        for j, (m0, m1) in enumerate(mags):
            lo = max(m0, np.percentile(m_all, 0.5)) if len(m_all) else m0
            h, e = np.histogram(m_all, bins=np.arange(lo, m1 + 1e-9, 0.2)); cc = 0.5*(e[1:]+e[:-1]); ok = h > 0
            sl[j, c] = np.polyfit(cc[ok], np.log10(h[ok]), 1)[0] if ok.sum() >= 2 else np.nan
    bb = [0.0] + [betabar(B[okb], q, tq, i) for i in range(3)]
    stash[name] = dict(Cc=Cc, Bc=Bc, pc=patch[okc], pb=bpatch[okb], sl=sl, bb=bb)
    res[name] = dict(n_clusters=int(okc.sum()), n_blank=int(okb.sum()), slopes=sl.tolist(), beta_bar=bb, mags=mags)
def K_of(Cc, Bc, sl, ann_idx):
    """self-calibrated double ratio per (mag, cat) in pooled annuli ann_idx vs control ring; then slope-weighted K per cat"""
    def dens(X): return X[:, ann_idx].sum((0, 1)) / AREA[ann_idx].sum(), X[:, 4].sum(0) / AREA[4]
    ca, cc = dens(Cc); ba, bc = dens(Bc); R = (ca/cc) / (ba/bc)
    w = 2.5*sl - 1; w = np.where(np.isfinite(w), w, 0)
    return (w*(R - 1)).sum(0) / (w*w).sum(0), R
def all_K(ann_idx, drop=None):
    Ks = {}
    for name, S in stash.items():
        mc = S["pc"] != drop if drop is not None else slice(None); mb = S["pb"] != drop if drop is not None else slice(None)
        Ks[name] = K_of(S["Cc"][mc], S["Bc"][mb], S["sl"], ann_idx)[0]
    return Ks
def analyse(ann_idx, label):
    full = all_K(ann_idx); jk = {n: [] for n in stash}
    for p in range(48):
        kk = all_K(ann_idx, drop=p)
        for n in stash: jk[n].append(kk[n])
    out = {}; cov = {}
    for n in stash:
        J = np.array(jk[n]); cov[n] = (47/48) * ((J - J.mean(0)).T @ (J - J.mean(0))); out[n] = dict(K=full[n].tolist(), sig=np.sqrt(np.diag(cov[n])).tolist())
    # combined per cat by inverse variance (weights fixed from full-sample diag), jackknife for the combination
    wv = {n: 1/np.diag(cov[n]) for n in stash}; W = sum(wv.values())
    def comb(kd): return sum(wv[n]*kd[n] for n in stash) / W
    Kc = comb(full); Jc = np.array([comb({n: jk[n][p] for n in stash}) for p in range(48)]); covc = (47/48)*((Jc - Jc.mean(0)).T @ (Jc - Jc.mean(0)))
    out["combined"] = dict(K=Kc.tolist(), sig=np.sqrt(np.diag(covc)).tolist())
    # A3 frozen: K of the z_Q > z_l + 0.5 sample (index 4)
    a3 = (Kc[4], np.sqrt(covc[4, 4]))
    # A3G: GLS fit K_b = A*beta_b + C over FG,B1,B2,B3 (combined beta_bar = mean of the two catalogues' weighted)
    bbar = np.array(sum(wv[n][:4]*np.array(stash[n]["bb"]) for n in stash) / W[:4])
    def gls(Kv, cv, x):
        M = np.c_[x, np.ones_like(x)]; Ci = np.linalg.pinv(cv); F = M.T @ Ci @ M; p = np.linalg.solve(F, M.T @ Ci @ Kv); return p, np.sqrt(np.diag(np.linalg.inv(F)))
    p, e = gls(Kc[:4], covc[:4, :4], bbar)
    pc = {}
    for n in stash:
        pn, en = gls(full[n][:4], cov[n][:4, :4], np.array(stash[n]["bb"])); pc[n] = dict(A=float(pn[0]), sA=float(en[0]), C=float(pn[1]), sC=float(en[1]))
    out["A3_K"] = [float(a3[0]), float(a3[1])]; out["A3G"] = dict(A=float(p[0]), sA=float(e[0]), C=float(p[1]), sC=float(e[1]), beta_bar=bbar.tolist(), per_catalogue=pc)
    print(f"\n--- {label} ---")
    for n in list(stash) + ["combined"]:
        print(f"  {n:9s} K by bin  " + "  ".join(f"{CATN[c]}={out[n]['K'][c]:+.4f}±{out[n]['sig'][c]:.4f}" for c in range(5)))
    print(f"  beta_bar (FG,B1,B2,B3) = {np.round(bbar, 3).tolist()}")
    print(f"  A3  K(z_Q>z_l+0.5) = {a3[0]:+.4f} ± {a3[1]:.4f}  ({a3[0]/a3[1]:+.1f}σ)")
    print(f"  A3G A = {p[0]:+.4f} ± {e[0]:.4f} ({p[0]/e[0]:+.1f}σ)   C = {p[1]:+.4f} ± {e[1]:.4f}   K_FG z = {Kc[0]/np.sqrt(covc[0,0]):+.1f}")
    for n in stash: print(f"      {n}: A = {pc[n]['A']:+.4f} ± {pc[n]['sA']:.4f} ({pc[n]['A']/pc[n]['sA']:+.1f}σ)  C = {pc[n]['C']:+.4f} ± {pc[n]['sC']:.4f}")
    return out
for n in stash: print(f"{n}: clusters {res[n]['n_clusters']} blanks {res[n]['n_blank']}  slopes (mag x [FG,B1,B2,B3,A3bg]) = {np.round(np.array(res[n]['slopes']), 2).tolist()}")
res["outer_8_40"] = analyse([1, 2, 3], f"8-40' (beyond baryons; DECISION)  MUTATE={MUT}")
for i, lab in [(1, "8-12'"), (2, "12-20'"), (3, "20-40'")]: res[f"ann_{lab}"] = analyse([i], lab + " (shape)")
res["inner_0_4"] = analyse([0], "0-4' (inside baryons; reference)")
o = res["outer_8_40"]; A, sA = o["A3G"]["A"], o["A3G"]["sA"]; K3, s3 = o["A3_K"]
v3 = "MASS BEYOND BARYONS DETECTED" if K3/s3 >= 3 and all(o[n]["K"][4] > 0 for n in stash) else ("WRONG SIGN" if K3/s3 <= -3 else ("NULL" if abs(K3/s3) < 2 else "NOT DETECTED"))
vg = "GEOMETRIC LENSING BEYOND BARYONS" if A/sA >= 3 else ("WRONG GEOMETRY" if A/sA <= -3 else ("NULL" if abs(A/sA) < 2 else "NOT DETECTED"))
if vg.startswith("GEOMETRIC") and abs(o["combined"]["K"][0]/o["combined"]["sig"][0]) < 2: vg += " (STRONG)"
res["verdict_A3"] = v3; res["verdict_A3G"] = vg
res["kappa_2sigma_upper_beta1"] = float((A + 2*sA)/2)
print(f"\nVERDICT A3 (frozen): {v3}\nVERDICT A3G (frozen): {vg}\n2σ upper limit on κ(8-40', β=1) ≈ (A+2σ)/2 = {(A+2*sA)/2:.4f}")
json.dump(res, open(os.path.join(HERE, "cfg668_a3_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)
