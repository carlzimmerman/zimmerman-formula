#!/usr/bin/env python3
"""CFG652 test (FROZEN_CRITERIA.md): raw KiDS-1000 lensing around eFEDS X-ray groups (Bahar+22, measured hot gas M_gas500)
against Theory v2 (a: condensed-sourced phantom) and candidate B (b: all-baryon phantom), both footings, never pooled.
Stages (CFG652_MODE):
  inputs   group sample + condensed mass M_cond from the KiDS bright sample (frozen recipe)      -> work/cfg652_inputs.npz
  measure  stacked ESD (tangential + cross) around groups and random points, per jackknife patch -> work/cfg652_esd.npz
  models   per-group DeltaSigma for (a) and (b), both footings, M_cond x 10^{0, +0.2, -0.2}, gas to 1 / 4 R_X      -> work/cfg652_models.npz
  score    statistics and verdict -> cfg652_test.out, cfg652_test_results.json (MUTATE=1: _MUTATE outputs)
Run from the repository root, one stage at a time:
  CFG652_MODE=<stage> OMP_NUM_THREADS=1 nice -n 10 python3 -u campaign_fresh_gravity/CFG652_hot_group_discriminator/cfg652_test.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg652_work"))
os.makedirs(WORK, exist_ok=True)
sys.path.insert(0, HERE)
try:
    os.nice(10)
except OSError:
    pass
MODE = os.environ.get("CFG652_MODE", "score")
MUT = os.environ.get("MUTATE") == "1"
T0 = time.time()
c_ms = 2.998e8; G_SI = 6.674e-11; Mpc = 3.0857e22; H0SI = 70 * 1e3 / Mpc
TO_MSUN_PC2 = (3.0857e16) ** 2 / 1.989e30
RB = np.geomspace(30, 3000, 13); RC = np.sqrt(RB[1:] * RB[:-1]); NB = len(RC)
USE = (RC >= 50) & (RC <= 1000)                     # 8 bins, 53-783 kpc (frozen)
BAND = (RC >= 250) & (RC <= 1000)                   # outer band, 248-783 kpc (frozen)
NPATCH = 30
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def DC(z, n=4096):                                   # comoving distance, flat (0.3, 0.7), H0 70 (June estimator convention)
    zz = np.linspace(0, max(float(np.max(z)), 2.0), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_ms / H0SI) / Mpc
    return np.interp(z, zz, chi)


def kpc_per_arcmin(z):
    return DC(z) / (1 + z) * 1000.0 * math.pi / 180 / 60


# ============================================================================================== inputs
if MODE == "inputs":
    from astropy.io import fits
    lines = [l.rstrip("\n") for l in open(os.path.join(REPO, "real_research", "data", "efeds_bahar2022_table2.tsv"))
             if not l.startswith("#") and l.strip()]
    H = {h: i for i, h in enumerate(lines[0].split("\t"))}
    rows = [l.split("\t") for l in lines[3:]]
    f = lambda r, k: float(r[H[k]]) if r[H[k]].strip() else np.nan
    E = np.array([[f(r, "RAJ2000"), f(r, "DEJ2000"), f(r, "z"), f(r, "R500"), f(r, "Mgas500"), f(r, "e_Mgas500"),
                   f(r, "E_Mgas500"), 1.0 if r[H["l_Mgas500"]].strip() == "<" else 0.0, f(r, "recno")] for r in rows])
    S = np.load(os.path.join(WORK, "cfg652_sources.npz"))
    sra, sde = S["RAJ2000"], S["DECJ2000"]
    from scipy.spatial import cKDTree
    tree = cKDTree(np.c_[sra * np.cos(np.radians(sde)), sde])
    # mean source density (per deg^2) over the occupied area: 0.1 deg cells with any source
    cells = np.unique(np.c_[np.floor(sra * 10), np.floor(sde * 10)], axis=0)
    dens = len(sra) / (len(cells) * 0.01)
    sel = (E[:, 2] >= 0.1) & (E[:, 2] <= 0.5) & (E[:, 7] == 0) & np.isfinite(E[:, 4]) & (E[:, 4] > 0)
    cov = np.zeros(len(E))
    for i in np.where(sel)[0]:
        kpa = kpc_per_arcmin(E[i, 2]); th1, th2 = 500 / kpa / 60, 1500 / kpa / 60     # deg
        n2 = len(tree.query_ball_point([E[i, 0] * math.cos(math.radians(E[i, 1])), E[i, 1]], th2))
        n1 = len(tree.query_ball_point([E[i, 0] * math.cos(math.radians(E[i, 1])), E[i, 1]], th1))
        cov[i] = (n2 - n1) / (dens * math.pi * (th2 ** 2 - th1 ** 2))
    sel &= cov >= 0.6
    E = E[sel]; cov = cov[sel]
    P(f"  groups: {len(E)} (0.1 <= z <= 0.5, measured M_gas500, source coverage >= 0.6 in 0.5-1.5 Mpc); source density {dens / 3600:.2f}/arcmin^2")
    # ---- condensed mass from the KiDS bright sample (frozen recipe)
    b = fits.open(os.path.join(REPO, "real_research", "data", "lensing_rar", "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
    lp = fits.open(os.path.join(REPO, "real_research", "data", "lensing_rar", "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
    bra = np.asarray(b["RAJ2000"], "f8"); bde = np.asarray(b["DECJ2000"], "f8")
    box = (bra > 122) & (bra < 150) & (bde > -7) & (bde < 9)
    bra, bde = bra[box], bde[box]
    bz = np.asarray(b["zphot_ANNz2"], "f8")[box]; bmk = np.asarray(b["masked"])[box]
    bm = np.asarray(lp["MASS_MED"], "f8")[box]
    ok = (bmk == 0) & (bm > 5) & np.isfinite(bz)
    bra, bde, bz, bm = bra[ok], bde[ok], bz[ok], 10 ** bm[ok]
    btree = cKDTree(np.c_[bra * np.cos(np.radians(bde)), bde])
    Mc = np.zeros(len(E)); Mbcg = np.zeros(len(E)); Rx = np.zeros(len(E)); Nmem = np.zeros(len(E))
    for i, e in enumerate(E):
        kpa = kpc_per_arcmin(e[2]); Rx[i] = e[3] * kpa                               # kpc, X-ray aperture
        th = e[3] / 60.0
        p = [e[0] * math.cos(math.radians(e[1])), e[1]]
        zw = np.abs(bz - e[2]) <= 0.05 * (1 + e[2])
        kin = np.array(btree.query_ball_point(p, th), int); kin = kin[zw[kin]]
        kout = np.array(btree.query_ball_point(p, 6 * th), int); kout = kout[zw[kout]]
        k3 = np.array(btree.query_ball_point(p, 3 * th), int); k3 = k3[zw[k3]]
        ann = np.setdiff1d(kout, k3)
        bkg = bm[ann].sum() * (1.0 / (36 - 9))
        net = bm[kin].sum() - bkg
        inner = np.array(btree.query_ball_point(p, 0.2 * th), int); inner = inner[zw[inner]]
        Mbcg[i] = bm[inner].max() if len(inner) else 0.0
        Mc[i] = max(net, Mbcg[i]); Nmem[i] = len(kin) - len(ann) / 27.0
    Mh = E[:, 4] * 1e12
    fh = Mh / (Mh + Mc)
    P(f"  M_cond median {np.median(Mc):.3e}; M_hot500 median {np.median(Mh):.3e}; f_hot quartiles {np.percentile(fh, [25, 50, 75]).round(3)}")
    np.savez(os.path.join(WORK, "cfg652_inputs.npz"), ra=E[:, 0], dec=E[:, 1], z=E[:, 2], R500_arcmin=E[:, 3], Rx_kpc=Rx,
             Mhot=Mh, Mcond=Mc, Mbcg=Mbcg, fhot=fh, cov=cov, Nmem=Nmem, eid=E[:, 8], src_dens_arcmin2=dens / 3600)
    P(f"  wrote inputs ({time.time() - T0:.0f} s)")

# ============================================================================================== measure
if MODE == "measure":
    from scipy.spatial import cKDTree
    I = np.load(os.path.join(WORK, "cfg652_inputs.npz"))
    S = np.load(os.path.join(WORK, "cfg652_sources.npz"))
    sra, sde, e1, e2, w, zB = (S[k] for k in ("RAJ2000", "DECJ2000", "e1", "e2", "weight", "Z_B"))
    tree = cKDTree(np.c_[np.radians(sra), np.radians(sde)])
    chiS = DC(zB)
    rng = np.random.default_rng(652)
    # random points: uniform in the occupied source cells, z drawn from the group z's, 20 per group
    cells = np.unique(np.c_[np.floor(sra * 10), np.floor(sde * 10)], axis=0)
    NR = 20 * len(I["z"])
    pick = cells[rng.integers(0, len(cells), NR)]
    rra = (pick[:, 0] + rng.uniform(0, 1, NR)) / 10; rde = (pick[:, 1] + rng.uniform(0, 1, NR)) / 10
    rz = rng.choice(I["z"], NR)

    def stack(ra, de, z):
        n = len(z); WG = np.zeros((n, NB)); WX = np.zeros((n, NB)); WW = np.zeros((n, NB)); NN = np.zeros((n, NB))
        chil = DC(z)
        for i in range(n):
            th = 3000.0 / (chil[i] / (1 + z[i]) * 1000.0)
            ii = np.array(tree.query_ball_point([math.radians(ra[i]), math.radians(de[i])], th), int)
            if ii.size < 5:
                continue
            ii = ii[zB[ii] > z[i] + 0.2]
            if ii.size < 5:
                continue
            dra = (np.radians(sra[ii]) - math.radians(ra[i])) * math.cos(math.radians(de[i])); dde = np.radians(sde[ii]) - math.radians(de[i])
            R = np.hypot(dra, dde) * chil[i] / (1 + z[i]) * 1000.0
            phi = np.arctan2(dde, dra)
            et = -(e1[ii] * np.cos(2 * phi) - e2[ii] * np.sin(2 * phi))
            ex = (e1[ii] * np.sin(2 * phi) + e2[ii] * np.cos(2 * phi))
            Dl = chil[i] / (1 + z[i]); Dls = (chiS[ii] - chil[i]) / (1 + zB[ii]); Ds = chiS[ii] / (1 + zB[ii])
            isc = np.clip(4 * math.pi * G_SI / c_ms ** 2 * (Dl * Mpc) * (Dls / Ds), 0, None)
            k = np.digitize(R, RB) - 1
            ok = (k >= 0) & (k < NB) & (isc > 0)
            ww = (w[ii] * isc ** 2)[ok]; kk = k[ok]
            np.add.at(WG[i], kk, ww * et[ok] / isc[ok] * TO_MSUN_PC2)
            np.add.at(WX[i], kk, ww * ex[ok] / isc[ok] * TO_MSUN_PC2)
            np.add.at(WW[i], kk, ww); np.add.at(NN[i], kk, w[ii][ok])
        return WG, WX, WW, NN

    G_ = stack(I["ra"], I["dec"], I["z"]); P(f"  groups stacked ({time.time() - T0:.0f} s)")
    R_ = stack(rra, rde, rz); P(f"  randoms stacked ({time.time() - T0:.0f} s)")
    # jackknife patches: NPATCH equal-count RA slices of the groups; randoms assigned by the same RA edges
    edges = np.quantile(I["ra"], np.linspace(0, 1, NPATCH + 1)); edges[0] -= 1; edges[-1] += 1
    pg = np.clip(np.digitize(I["ra"], edges) - 1, 0, NPATCH - 1); pr = np.clip(np.digitize(rra, edges) - 1, 0, NPATCH - 1)
    np.savez(os.path.join(WORK, "cfg652_esd.npz"), WG=G_[0], WX=G_[1], WW=G_[2], NN=G_[3], rWG=R_[0], rWX=R_[1], rWW=R_[2],
             rNN=R_[3], pg=pg, pr=pr, rra=rra, rde=rde, rz=rz)
    P(f"  wrote esd ({time.time() - T0:.0f} s)")

# ============================================================================================== models
if MODE == "models":
    import cfg652_model as M
    I = np.load(os.path.join(WORK, "cfg652_inputs.npz"))
    n = len(I["z"]); VAR = (("x1", 1.0, 2.0), ("p02", 10 ** 0.2, 2.0), ("m02", 10 ** -0.2, 2.0), ("g1", 1.0, 1.0), ("g4", 1.0, 4.0))
    out = {}
    for foot in ("canonical", "alt"):
        for vk, fac, gt in VAR:
            for model in "ab":
                arr = np.zeros((n, NB))
                for i in range(n):
                    if I["Mcond"][i] <= 0:          # post-freeze disclosure: no condensed mass found -> excluded (NaN)
                        arr[i] = np.nan; continue
                    o = M.system(I["Mcond"][i] * fac, I["Mhot"][i], I["Rx_kpc"][i], I["z"][i], foot, model, N=600, gas_trunc=gt)
                    arr[i] = M.delta_sigma(o["rg"], o["Mbound"], RC, rmax=o["rta"])
                out[f"{foot}|{vk}|{model}"] = arr
                P(f"  models {foot} {vk} {model} done ({time.time() - T0:.0f} s)")
        arr = np.zeros((n, NB))                       # MUTATE M1: (a) with the hot gas relabelled condensed
        for i in range(n):
            if I["Mcond"][i] <= 0:
                arr[i] = np.nan; continue
            o = M.system(I["Mcond"][i], I["Mhot"][i], I["Rx_kpc"][i], I["z"][i], foot, "a", N=600, hot_as_condensed=True)
            arr[i] = M.delta_sigma(o["rg"], o["Mbound"], RC, rmax=o["rta"])
        out[f"{foot}|M1|a"] = arr
        P(f"  models {foot} M1 done ({time.time() - T0:.0f} s)")
    np.savez(os.path.join(WORK, "cfg652_models.npz"), **{k.replace("|", "__"): v for k, v in out.items()})

# ============================================================================================== score
if MODE == "score":
    I0 = np.load(os.path.join(WORK, "cfg652_inputs.npz")); D0 = np.load(os.path.join(WORK, "cfg652_esd.npz"))
    MD = np.load(os.path.join(WORK, "cfg652_models.npz"))
    # post-freeze disclosure: groups whose frozen M_cond recipe returns 0 are excluded (the models are undefined there);
    # POSTHOC=1 restricts further to groups with a bright-sample central (M_bcg > 0) and M_cond >= 1e11 (no verdict weight)
    keep = I0["Mcond"] > 0
    if os.environ.get("POSTHOC") == "1":
        keep &= (I0["Mbcg"] > 0) & (I0["Mcond"] >= 1e11)
    I = {k: (I0[k][keep] if np.ndim(I0[k]) and len(I0[k]) == len(keep) else I0[k]) for k in I0.files}
    D = {k: (D0[k][keep] if k in ("WG", "WX", "WW", "NN", "pg") else D0[k]) for k in D0.files}
    MODELS = {k.replace("__", "|"): MD[k][keep] for k in MD.files}
    n = len(I["z"]); fh = I["fhot"].copy(); Mh = I["Mhot"].copy(); Mc = I["Mcond"].copy()
    RES = {"lane": "CFG652", "script": "cfg652_test", "mutate": MUT, "N_groups": int(n)}
    P(__doc__.split("Stages")[0].strip())
    P(f"  N groups {n}; z median {np.median(I['z']):.3f}; M_cond median {np.median(Mc):.3e}; M_hot median {np.median(Mh):.3e};"
      f" f_hot median {np.median(fh):.3f}")

    def esd(sel_g, sel_r, comp="t"):
        WG = D["WG"] if comp == "t" else D["WX"]; rWG = D["rWG"] if comp == "t" else D["rWX"]
        Wg = D["WW"][sel_g].sum(0); Wr = D["rWW"][sel_r].sum(0)
        g = WG[sel_g].sum(0) / np.where(Wg > 0, Wg, np.nan); r = rWG[sel_r].sum(0) / np.where(Wr > 0, Wr, np.nan)
        boost = (D["NN"][sel_g].sum(0) / max(sel_g.sum(), 1)) / (D["rNN"][sel_r].sum(0) / max(sel_r.sum(), 1))
        return boost * g - r, boost

    def model_stack(arr, sel_g):
        W = D["WW"][sel_g]
        return (W * arr[sel_g]).sum(0) / np.where(W.sum(0) > 0, W.sum(0), np.nan)

    allg = np.ones(n, bool); allr = np.ones(len(D["rz"]), bool)

    def jk(fun):
        vals = []
        for p in range(NPATCH):
            vals.append(fun(D["pg"] != p, D["pr"] != p))
        vals = np.array(vals); m = vals.mean(0)
        return (NPATCH - 1) / NPATCH * (vals - m).T @ (vals - m)

    obs, boost = esd(allg, allr)
    cross, _ = esd(allg, allr, "x")
    C = jk(lambda a, b: esd(a, b)[0][USE])
    Cx = jk(lambda a, b: esd(a, b, "x")[0][USE])
    nb = int(USE.sum()); hart = (NPATCH - nb - 2) / (NPATCH - 1)
    Ci = np.linalg.inv(C) * hart; Cxi = np.linalg.inv(Cx) * hart
    sig = np.sqrt(np.diag(C))
    P("\n  R (kpc)      " + " ".join(f"{x:7.0f}" for x in RC[USE]))
    P("  DS obs       " + " ".join(f"{x:7.1f}" for x in obs[USE]))
    P("  sigma (jk)   " + " ".join(f"{x:7.1f}" for x in sig))
    P("  boost        " + " ".join(f"{x:7.3f}" for x in boost[USE]))
    P("  cross        " + " ".join(f"{x:7.1f}" for x in cross[USE]))
    from scipy.stats import chi2 as CHI2
    chx = float(cross[USE] @ Cxi @ cross[USE]); pX = float(CHI2.sf(chx, nb))
    Wr = D["rWW"].sum(0); rsig = D["rWG"].sum(0) / Wr
    P(f"  [CONTROL K1] cross-shear chi2 {chx:.1f}/{nb}, p = {pX:.3f} -> {'PASS' if pX > 0.01 else 'FAIL'} (p > 0.01)")
    P("  random-point signal (subtracted) " + " ".join(f"{x:6.2f}" for x in rsig[USE]))
    RES.update(R=RC[USE].tolist(), obs=obs[USE].tolist(), sigma=sig.tolist(), boost=boost[USE].tolist(), cross=cross[USE].tolist(),
               K1_cross=dict(chi2=chx, p=pX, ok=pX > 0.01), random_signal=rsig[USE].tolist(), hartlap=hart)
    bandw = 1.0 / sig[BAND[USE]] ** 2

    def aout(o, m):
        return float(np.log10(np.sum(o[BAND] ) / np.sum(m[BAND])))

    VERD = {}
    for foot in ("canonical", "alt"):
        VERD[foot] = {}
        for vk in ("x1", "p02", "m02", "g1", "g4"):
            st = {}
            for model in "ab":
                ms = model_stack(MODELS[f"{foot}|{vk}|{model}"], allg)
                d = obs[USE] - ms[USE]
                ch = float(d @ Ci @ d); p = float(CHI2.sf(ch, nb))
                A = aout(obs, ms)
                # jackknife sigma of A
                Aj = np.array([aout(esd(D["pg"] != q, D["pr"] != q)[0], model_stack(MODELS[f"{foot}|{vk}|{model}"], D["pg"] != q))
                               for q in range(NPATCH)])
                sA = float(math.sqrt((NPATCH - 1) / NPATCH * np.sum((Aj - Aj.mean()) ** 2)))
                st[model] = dict(model=ms[USE].tolist(), chi2=ch, p=p, A_out=A, sA=sA)
            dchi = st["b"]["chi2"] - st["a"]["chi2"]
            if st["a"]["p"] < 0.01 and st["b"]["p"] < 0.01:
                lab = "BOTH EXCLUDED"
            elif dchi >= 9 and st["a"]["p"] >= 0.01:
                lab = "(a) FAVOURED"
            elif dchi <= -9 and st["b"]["p"] >= 0.01:
                lab = "(b) FAVOURED"
            else:
                lab = "NOT DIAGNOSTIC"
            st["dchi2_b_minus_a"] = dchi; st["label"] = lab
            VERD[foot][vk] = st
            P(f"\n  [{foot[:3]}] M_cond {vk}: (a) chi2 {st['a']['chi2']:.1f}/{nb} p {st['a']['p']:.3g} A_out {st['a']['A_out']:+.3f} +- {st['a']['sA']:.3f};"
              f" (b) chi2 {st['b']['chi2']:.1f}/{nb} p {st['b']['p']:.3g} A_out {st['b']['A_out']:+.3f} +- {st['b']['sA']:.3f};"
              f" dchi2(b-a) {dchi:+.1f} -> {lab}")
            P("     model (a) " + " ".join(f"{x:7.1f}" for x in st["a"]["model"]))
            P("     model (b) " + " ".join(f"{x:7.1f}" for x in st["b"]["model"]))
        labs_m = {VERD[foot][v]["label"] for v in ("x1", "p02", "m02")}
        labs_g = {VERD[foot][v]["label"] for v in ("x1", "g1", "g4")}
        VERD[foot]["robust"] = len(labs_m) == 1 and len(labs_g) == 1
        frag = [n_ for n_, l_ in (("M_cond", labs_m), ("gas extent", labs_g)) if len(l_) > 1]
        VERD[foot]["final"] = VERD[foot]["x1"]["label"] + ("" if not frag else f" (FRAGILE: {', '.join(frag)})")
    if VERD["canonical"]["final"] == VERD["alt"]["final"]:
        final = VERD["canonical"]["final"]
    else:
        final = f"FOOTING-DEPENDENT (can: {VERD['canonical']['final']}; alt: {VERD['alt']['final']})"
    if "(b) FAVOURED" in final:
        final += " [conditional: no 2-halo term in either model; its omission favours (b)]"
    RES["verdicts"] = VERD; RES["final"] = final
    P(f"\n  PRIMARY VERDICT: {final}")

    # ---------------- secondary: hot-fraction split (reported) + MUTATE M2 (shuffled hot fractions)
    med = np.median(fh); hi = fh > med; lo = ~hi

    def split_D(hi, lo):
        oh = esd(hi, allr)[0]; ol = esd(lo, allr)[0]
        return float(np.log10(np.sum(oh[BAND]) / np.sum(ol[BAND])))

    Dobs = split_D(hi, lo)
    Dj = np.array([split_D(hi & (D["pg"] != q), lo & (D["pg"] != q)) for q in range(NPATCH)])
    sD = float(math.sqrt((NPATCH - 1) / NPATCH * np.sum((Dj - Dj.mean()) ** 2)))
    SP = dict(Dobs=Dobs, sD=sD, fhot_median=float(med), Mcond_med_hi=float(np.median(Mc[hi])), Mcond_med_lo=float(np.median(Mc[lo])),
              Mhot_med_hi=float(np.median(Mh[hi])), Mhot_med_lo=float(np.median(Mh[lo])))
    for foot in ("canonical", "alt"):
        for model in "ab":
            arr = MODELS[f"{foot}|x1|{model}"]
            mh_, ml_ = model_stack(arr, hi), model_stack(arr, lo)
            SP[f"Dpred_{foot}_{model}"] = float(np.log10(np.sum(mh_[BAND]) / np.sum(ml_[BAND])))
    P(f"\n  SPLIT at median f_hot {med:.3f}: D_obs = log10[DS_band(high f_hot)/DS_band(low)] = {Dobs:+.3f} +- {sD:.3f};"
      f" predicted (a) {SP['Dpred_canonical_a']:+.3f}/{SP['Dpred_alt_a']:+.3f}, (b) {SP['Dpred_canonical_b']:+.3f}/{SP['Dpred_alt_b']:+.3f} (can/alt)")
    P(f"     medians high/low: M_cond {SP['Mcond_med_hi']:.2e}/{SP['Mcond_med_lo']:.2e}, M_hot {SP['Mhot_med_hi']:.2e}/{SP['Mhot_med_lo']:.2e}")
    rng = np.random.default_rng(6520)
    Dsh = []
    for s in range(200):
        perm = rng.permutation(n); fsh = Mh[perm] / (Mh[perm] + Mc)
        h2 = fsh > np.median(fsh); Dsh.append(split_D(h2, ~h2))
    Dsh = np.array(Dsh)
    SP["M2_shuffle_median"] = float(np.median(Dsh)); SP["M2_shuffle_sd"] = float(np.std(Dsh))
    SP["M2_trend_killed"] = bool(abs(np.median(Dsh)) < sD)
    P(f"  [MUTATE M2] shuffled hot fractions (200): D median {np.median(Dsh):+.3f}, sd {np.std(Dsh):.3f}"
      f" (trend killed if |median| < sigma_D = {sD:.3f}: {'YES' if abs(np.median(Dsh)) < sD else 'NO'})")
    RES["split"] = SP

    if MUT:     # MUTATE M1 at data level: (a) re-derived with the hot gas relabelled condensed must reproduce (b)'s chi2
        P("\n  [MUTATE M1] (a) with hot gas relabelled condensed vs (b):")
        RES["M1"] = {}
        for foot in ("canonical", "alt"):
            ms = model_stack(MODELS[f"{foot}|M1|a"], allg); d = obs[USE] - ms[USE]; ch = float(d @ Ci @ d)
            chb = VERD[foot]["x1"]["b"]["chi2"]; ok = abs(ch - chb) < 0.01
            RES["M1"][foot] = dict(chi2_relabelled_a=ch, chi2_b=chb, ok=ok)
            P(f"    [{foot[:3]}] chi2 (a, relabelled) {ch:.3f} vs (b) {chb:.3f} -> {'PASS (bites: (a) collapses onto (b))' if ok else 'FAIL'}")
    tag = ("_MUTATE" if MUT else "") + ("_POSTHOC" if os.environ.get("POSTHOC") == "1" else "")
    json.dump(RES, open(os.path.join(HERE, f"cfg652_test_results{tag}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg652_test{tag}.out"), "w").write("\n".join(LOG) + "\n")
    P(f"  done ({time.time() - T0:.0f} s)")
