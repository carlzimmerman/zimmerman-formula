"""CFG668 A2 (criteria a17b552d1): quasar counts behind redMaPPer clusters vs blank fields. Quaia G<20 + SDSS DR16Q.
Raw angular counts, z_Q > z_cl + 0.5, bootstrap errors, slope from blanks. MUTATE=1: half the blanks play clusters."""
import json, math, os, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE") == "1"
def xyz(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec); return np.c_[np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)]
def chord(arcmin): return 2*np.sin(np.radians(arcmin/60)/2)
def readtsv(fn, gz=False):
    import gzip; f = gzip.open(fn, "rt") if gz else open(fn)
    rows = []
    for l in f:
        p = l.strip().split("\t")
        if len(p) != 4: continue
        try: rows.append([float(x) for x in p])
        except ValueError: pass
    return np.array(rows)
cl = readtsv(os.path.join(HERE, "redmapper_all_z01_06.tsv")); cl = cl[cl[:, 3] >= 20]
Xc = xyz(cl[:, 0], cl[:, 1]); tc = cKDTree(Xc)
rng = np.random.default_rng(668); reps = 3
a = rng.uniform(0, 2*np.pi, (len(cl), reps)); s = rng.uniform(1, 3, (len(cl), reps))
bra = (cl[:, :1] + s*np.cos(a)/np.maximum(0.2, np.cos(np.radians(cl[:, 1:2])))) % 360; bdec = np.clip(cl[:, 1:2] + s*np.sin(a), -89.9, 89.9)
bz = np.repeat(cl[:, 2:3], reps, 1)
B = np.c_[bra.ravel(), bdec.ravel(), bz.ravel()]; Xb = xyz(B[:, 0], B[:, 1])
B = B[np.array([len(x) == 0 for x in tc.query_ball_point(Xb, chord(15))])]; Xb = xyz(B[:, 0], B[:, 1])
C = cl[:, :3]
if MUT:
    idx = rng.permutation(len(B)); h = len(B)//2; C, B = B[idx[:h]], B[idx[h:]]
Xc, Xb = xyz(C[:, 0], C[:, 1]), xyz(B[:, 0], B[:, 1])
ANN = [(0, 1), (1, 2), (2, 4)]
CATS = {"quaia": ("quaia_g20_ra_dec_z_g.tsv.gz", [(17, 19.0), (19.0, 19.6), (19.6, 20.0)], (0, 4)),
        "dr16q": ("dr16q_ra_dec_z_imag.tsv.gz", [(14, 19.5), (19.5, 20.5), (20.5, 22)], (1, 4))}
def counts(X, zc, q, tq, mags):
    lists = tq.query_ball_point(X, chord(4)); out = np.zeros((len(X), len(ANN), len(mags)))
    for k, L in enumerate(lists):
        if not L: continue
        L = np.array(L); qq = q[L]; qq = qq[qq[:, 2] > zc[k] + 0.5]
        if not len(qq): continue
        d = np.degrees(np.arccos(np.clip(xyz(qq[:, 0], qq[:, 1]) @ X[k], -1, 1)))*60
        for i, (r0, r1) in enumerate(ANN):
            for j, (m0, m1) in enumerate(mags): out[k, i, j] = ((d >= r0) & (d < r1) & (qq[:, 3] >= m0) & (qq[:, 3] < m1)).sum()
    return out
res = {"mutate": MUT}; comb = []
for name, (fn, mags, prim) in CATS.items():
    q = readtsv(os.path.join(HERE, fn), gz=True); q = q[np.isfinite(q).all(1)]
    tq = cKDTree(xyz(q[:, 0], q[:, 1]))
    nc = np.array([len(x) for x in tq.query_ball_point(Xc, chord(30))]); nb = np.array([len(x) for x in tq.query_ball_point(Xb, chord(30))])
    med = np.median(nb); okc, okb = nc >= 0.5*med, nb >= 0.5*med               # footprint cut (frozen)
    Cn, Bn = counts(Xc[okc], C[okc, 2], q, tq, mags), counts(Xb[okb], B[okb, 2], q, tq, mags)
    pi = [i for i, (r0, r1) in enumerate(ANN) if r0 >= prim[0] and r1 <= prim[1]]
    Cp, Bp = Cn[:, pi].sum(1), Bn[:, pi].sum(1)                                     # primary aperture, per mag bin
    def R(c, b): return c.mean(0)/b.mean(0)
    r = np.random.default_rng(1); bs = np.array([R(Cp[r.integers(0, len(Cp), len(Cp))], Bp[r.integers(0, len(Bp), len(Bp))]) for _ in range(2000)])
    Rp, sp = R(Cp, Bp), bs.std(0)
    bsa = np.array([R(Cn[r.integers(0, len(Cn), len(Cn))], Bn[r.integers(0, len(Bn), len(Bn))]) for _ in range(500)])
    Ra, sa = R(Cn, Bn), bsa.std(0)
    # slopes from blank counts over the whole 0-4' disk, quarter-mag bins
    allm = []
    for k, L in enumerate(tq.query_ball_point(Xb[okb], chord(4))):
        if L: qq = q[np.array(L)]; allm.extend(qq[qq[:, 2] > B[okb][k, 2] + 0.5][:, 3])
    allm = np.array(allm); sl = []
    for m0, m1 in mags:
        lo = max(m0, np.percentile(allm, 0.5)); h, e = np.histogram(allm, bins=np.arange(lo, m1 + 1e-9, 0.2)); c = 0.5*(e[1:]+e[:-1]); ok = h > 0
        sl.append(float(np.polyfit(c[ok], np.log10(h[ok]), 1)[0]) if ok.sum() >= 2 else float("nan"))
    res[name] = dict(n_clusters=int(okc.sum()), n_blank=int(okb.sum()), mags=mags, primary=prim, slope=sl, R_primary=Rp.tolist(), sig_primary=sp.tolist(),
                     N_cl_primary=Cp.mean(0).tolist(), N_bl_primary=Bp.mean(0).tolist(), R_annuli=Ra.tolist(), sig_annuli=sa.tolist(),
                     implied_mu=[float(Rp[j]**(1/(2.5*sl[j]-1))) if abs(2.5*sl[j]-1) > 0.2 else None for j in range(3)])
    comb.append((Rp, sp, sl))
    print(f"\n=== {name.upper()}  clusters {okc.sum()}  blanks {okb.sum()}  primary {prim}'  MUTATE={MUT}")
    for j, m in enumerate(mags):
        print(f"  mag {m}: s={sl[j]:.2f}  N_cl={Cp.mean(0)[j]:.4f}  N_bl={Bp.mean(0)[j]:.4f}  R={Rp[j]:.3f}±{sp[j]:.3f}  ({(Rp[j]-1)/sp[j]:+.1f}σ)")
    for i, an in enumerate(ANN):
        print(f"  annulus {an}': " + "  ".join(f"R={Ra[i,j]:.3f}±{sa[i,j]:.3f}" for j in range(3)))
# frozen verdict: steepest bin per catalogue, combined
st = [int(np.nanargmax(x[2])) for x in comb]; Rs = np.array([x[0][j] for x, j in zip(comb, st)]); Ss = np.array([x[1][j] for x, j in zip(comb, st)])
w = 1/Ss**2; Rc = (Rs*w).sum()/w.sum(); sc = 1/np.sqrt(w.sum()); zc = (Rc - 1)/sc
order_ok = all(all((x[0][a_] <= x[0][b_] + 2*np.hypot(x[1][a_], x[1][b_])) for a_ in range(3) for b_ in range(3) if x[2][a_] < x[2][b_]) for x in comb)
flat_def = any(x[2][j] < 0.4 and (x[0][j]-1)/x[1][j] <= -2 for x in comb for j in range(3))
if zc >= 3 and all(Rs > 1) and order_ok: v = "LENSING DETECTED" + (" (STRONG FORM)" if flat_def else "")
elif zc <= -3: v = "WRONG SIGN"
elif all(abs((x[0][j]-1)/x[1][j]) < 2 for x in comb for j in range(3)): v = "NULL"
else: v = "NOT DETECTED (no frozen pattern)"
res["combined_steep"] = dict(R=Rc, sig=sc, z=zc, order_ok=order_ok, flat_deficit=flat_def, verdict=v)
print(f"\nCOMBINED steepest bin: R={Rc:.3f}±{sc:.3f} ({zc:+.1f}σ); ordering ok={order_ok}; flat-bin deficit={flat_def}\nVERDICT: {v}")
json.dump(res, open(os.path.join(HERE, "cfg668_a2_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)
