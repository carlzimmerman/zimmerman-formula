"""SRH1R data side (own code): host-free flags, the neighbour pairs of the graded lenses, and known answer KA6.
Usage: python3 -I srh1r_data.py <data dir> <work dir>.  The catalogue files are read as data only.
Outputs: <work dir>/lens.npz, <work dir>/pairs.npz (not committed), srh1r_data.json / .out (here).
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits
import srh1r_model as m

DATA, WORK = sys.argv[1], sys.argv[2]; os.makedirs(WORK, exist_ok=True)
G, MSUN, MPC = m.G_SI, m.MSUN, m.MPC; C_SI, H0 = 2.998e8, 70.0e3 / MPC; G_OUT = 1e-15; KMAX = 8.0; WIN = 230.0     # the record's rounded c (its distances use it)
OUT = []; RES = {}
def P(*a):
    s = " ".join(str(v) for v in a); print(s, flush=True); OUT.append(s)
def comoving(z, n=2048):                                    # the record's distance: flat, Omega_m 0.3, H0 70, trapezoid
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (C_SI / H0) / MPC
    return np.interp(z, zz, chi)
def xyz(ra, dec):
    a, d = np.radians(ra), np.radians(dec); return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]
def gal_mass(lm): return 10 ** lm * (1 + 10 ** (-0.69 * lm + 6.63))

LN = np.load(os.path.join(DATA, "lr_lenses.npz")); NL = len(LN["z"])
bs = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
lp = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
assert np.array_equal(np.asarray(bs["ID"]), np.asarray(lp["ID"]))
rmag = np.array(bs["MAG_AUTO_CALIB"], dtype="f8"); zph = np.array(bs["zphot_ANNz2"], dtype="f8")
lms = np.array(lp["MASS_MED"], dtype="f8") + 0.15; ra = np.array(bs["RAJ2000"], dtype="f8"); dec = np.array(bs["DECJ2000"], dtype="f8")
sel = (rmag < 20) & (zph >= 0.02) & (zph <= 0.8) & np.isfinite(lms) & (lms > 7)
xN = xyz(ra[sel], dec[sel]); zN = zph[sel]; mN = lms[sel]; chiN = comoving(zN); MgN = gal_mass(mN); del bs, lp, rmag, zph, lms, ra, dec
tree = cKDTree(xN); P(f"pool {len(mN):,} objects; log M* range {mN.min():.2f} to {mN.max():.2f}; 99.9th percentile {np.percentile(mN, 99.9):.2f}")
xL = xyz(LN["ra"], LN["dec"]); dd, selfN = tree.query(xL, k=1)
ok = (dd.max() < 1e-9) and np.allclose(mN[selfN], LN["logM"], atol=1e-6) and np.allclose(zN[selfN], LN["z"], atol=1e-6)
P(f"lenses {NL:,} matched to pool rows: max chord {dd.max():.1e}, masses and redshifts equal: {ok}"); assert ok
zl, ml, Mg = LN["z"].astype("f8"), LN["logM"].astype("f8"), LN["Mgal"].astype("f8"); chl = chiN[selfN]; typ = LN["typ"]
RH = np.minimum(3.0, np.sqrt(G * Mg * MSUN / G_OUT) / MPC)                       # Mpc physical

def pairs_of(qidx, xq, rad_mpc, chunk=2000):
    """Yield (lens index, pool index, projected physical separation in Mpc) for pool objects within rad_mpc of position xq."""
    th = rad_mpc[qidx] * (1 + zl[qidx]) / chl[qidx] * (1 + 1e-9); rq = 2 * np.sin(np.minimum(th, math.pi) / 2)
    for i0 in range(0, len(qidx), chunk):
        lists = tree.query_ball_point(xq[i0:i0 + chunk], r=rq[i0:i0 + chunk])
        cnt = np.fromiter((len(v) for v in lists), dtype=np.int64, count=len(lists)); k = np.repeat(np.arange(len(lists)), cnt)
        j = np.fromiter(itertools.chain.from_iterable(lists), dtype=np.int64, count=int(cnt.sum())); li = qidx[i0 + k]
        ch = np.sqrt(((xN[j] - xq[i0 + k]) ** 2).sum(1)); d = 2 * np.arcsin(np.minimum(ch / 2, 1.0)) * chl[li] / (1 + zl[li])
        yield li, j, d

# ---------------------------------------------------------------- host flags (KO1's definition, my code)
FV = (1.0, 1.3, 1.6); TIES = {"plain": 0.0, "tieR": 1e-9}
nh = {(F, t): np.zeros(NL, np.int64) for F in FV for t in TIES}; allq = np.arange(NL)
for li, j, d in pairs_of(allq, xL, 1.6 * RH):
    q = (j != selfN[li]) & (mN[j] - ml[li] >= 0.29) & (np.abs(chiN[j] - chl[li]) < WIN); li, j, d = li[q], j[q], d[q]
    for F in FV:
        for t, tol in TIES.items():
            hh = (mN[j] >= (ml[li] + 0.3) - tol) & (d <= F * RH[li]); nh[(F, t)] += np.bincount(li[hh], minlength=NL)
HF = {f"F{F}_{t}": nh[(F, t)] == 0 for F in FV for t in TIES}
cnt = {k: int(v.sum()) for k, v in HF.items()}; P("host-free counts:", cnt)
ka6a = (cnt["F1.0_plain"], cnt["F1.3_plain"], cnt["F1.6_plain"], cnt["F1.0_tieR"]) == (40667, 25708, 17335, 40149)
P(f"KA6 counts (40,667 / 25,708 / 17,335 plain; 40,149 KO1R rule at 1.0 R_h): {'PASS' if ka6a else 'FAIL'}")
P("by type at 1.6 R_h, KO1R rule: late", int((HF["F1.6_tieR"] & (typ == 0)).sum()), "early", int((HF["F1.6_tieR"] & (typ == 1)).sum()))

# ---------------------------------------------------------------- KA6 amplitude: KO1's point-law model on the 1.0 R_h set
PL = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WGs, WW, ged = PL["WG"], PL["WW"], PL["gbar_edges"]
patch = np.load(os.path.join(DATA, "cfg96_stack.npz"))["patch"]; NP = 50
def law_cells(a0):
    Rlo = np.sqrt(G * Mg[:, None] * MSUN / ged[None, 1:]); Rhi = np.minimum(np.sqrt(G * Mg[:, None] * MSUN / ged[None, :-1]), 3.0 * MPC)
    x, w = np.polynomial.legendre.leggauss(24); okc = Rhi > Rlo; Rh2 = np.where(okc, Rhi, Rlo * 1.001); l1, l2 = np.log(Rlo), np.log(Rh2)
    num = 0.0; den = 0.0
    for xi, wi in zip(x, w):
        R = np.exp(l1 + 0.5 * (l2 - l1) * (xi + 1)); g = G * Mg[:, None] * MSUN / R ** 2
        num = num + wi * R ** 2 * g * (0.5 + np.sqrt(0.25 + a0 / g)); den = den + wi * R ** 2
    return np.where(okc, num / den, 0.0)
def amp(mask, cm, bins=(0, 1, 2, 3)):
    b = list(bins); pg = np.zeros((NP, len(b))); pw = np.zeros((NP, len(b))); pm = np.zeros((NP, len(b)))
    for a, bb in enumerate(b):
        pg[:, a] = np.bincount(patch[mask], WGs[mask, bb], NP); pw[:, a] = np.bincount(patch[mask], WW[mask, bb], NP)
        pm[:, a] = np.bincount(patch[mask], WW[mask, bb] * cm[mask, bb], NP)
    D = 4 * G * pg.sum(0) / pw.sum(0); M = pm.sum(0) / pw.sum(0)
    Dj = 4 * G * (pg.sum(0) - pg) / (pw.sum(0) - pw); Mj = (pm.sum(0) - pm) / (pw.sum(0) - pw)
    sk = np.sqrt((NP - 1) / NP * ((Dj - Dj.mean(0)) ** 2).sum(0)); A = (D * M / sk ** 2).sum() / (M ** 2 / sk ** 2).sum()
    Aj = (Dj * Mj / sk ** 2).sum(1) / (Mj ** 2 / sk ** 2).sum(1); return float(A), float(np.sqrt((NP - 1) / NP * ((Aj - Aj.mean()) ** 2).sum()))
ka6b = True
for foot, want in (("canonical", (1.0822, 0.1583)), ("alt", (0.9847, 0.1440))):
    A, s = amp(HF["F1.0_tieR"], law_cells(m.A0[foot])); good = abs(A - want[0]) < 1e-3 and abs(s - want[1]) < 1e-3; ka6b &= good
    P(f"KA6 A_hf {foot}: {A:.4f} +- {s:.4f} against KO1R's {want[0]} +- {want[1]} -> {'PASS' if good else 'FAIL'}"); RES[f"KA6_A_{foot}"] = [A, s]
RES["KA6"] = dict(pass_=bool(ka6a and ka6b), counts=cnt)

# ---------------------------------------------------------------- neighbour pairs for the graded lenses
U = np.flatnonzero(HF["F1.3_plain"]); P(f"lenses carried (host-free at 1.3 R_h, plain rule; superset of every graded set): {len(U):,}")
lMk = np.log10(KMAX * MgN)
reach = np.maximum(np.maximum(m.ref_halo(max(m.XSH.values()) * KMAX * MgN / (1 - m.FB), 0.0)[1],
                              math.sqrt(60.6 * 61.6) * m.r_M(KMAX * MgN, "canonical")), 1.0) / 1e3      # Mpc: largest halo edge at k = 8
P(f"halo reach at k = 8: median {np.median(reach):.2f} Mpc, max {reach.max():.2f} Mpc")
RMAXQ = 3.0 + float(np.percentile(reach, 100))
def collect(xq, excl):
    L_, J_, D_ = [], [], []
    for li, j, d in pairs_of(U, xq, np.full(NL, RMAXQ)):
        pos = np.searchsorted(U, li); q = (j != excl[pos]) & (j != selfN[li]) & (np.abs(chiN[j] - chl[li]) < WIN) & (d < RH[li] + reach[j])
        L_.append(pos[q].astype(np.int32)); J_.append(j[q]); D_.append(d[q])
    L_, J_, D_ = np.concatenate(L_), np.concatenate(J_), np.concatenate(D_)
    return L_, np.log10(MgN[J_]).astype(np.float32), (D_ * 1e3).astype(np.float64)
sv = {}
li, lmj, dk = collect(xL[U], selfN[U]); sv.update(real_li=li, real_lM=lmj, real_d=dk); P(f"real pairs: {len(li):,} ({len(li) / len(U):.1f} per lens)")
rng = np.random.default_rng(52)
for a in range(3):
    perm = rng.permutation(len(U)); li, lmj, dk = collect(xL[U][perm], selfN[U][perm]); sv.update({f"null{a}_li": li, f"null{a}_lM": lmj, f"null{a}_d": dk})
    P(f"null {a} pairs (lens positions permuted among the carried lenses): {len(li):,}")
np.savez(os.path.join(WORK, "pairs.npz"), **sv)
np.savez(os.path.join(WORK, "lens.npz"), U=U, z=zl[U], Mgal=Mg[U], typ=typ[U], patch=patch[U], WG=WGs[U], WW=WW[U], ged=ged,
         **{k: v[U] for k, v in HF.items()})
RES["n_carried"] = int(len(U)); RES["n_pairs_real"] = int(len(sv["real_li"]))
json.dump(dict(lane="SRH1R", **RES, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, "srh1r_data.json"), "w"), indent=1)
open(os.path.join(HERE, "srh1r_data.out"), "w").write("\n".join(OUT) + "\n")
