#!/usr/bin/env python3
"""CFG644 KiDS arm: T2 (isolated stacks, census-edge fail) and T3 (ALL parent sample, dense vs isolated sign test).
Criteria: FROZEN_CRITERIA.md (6a03c0870).  Raw ESD only in verdicts; CFG529's environment model vectors appear as CONTEXT ONLY.
Read-only reuse: cfg100_lib, cfg515_lib, CFG503 cfg503_own (kids_Md, kids_fin), the CFG525 pool rule, CFG525 tables (control),
CFG529 committed CENSUS vectors (context), cfg502_stage.npz (ALL sample).  Own-profile node tables are cached outside git in
../../../_external_data/cfg644_work/.
MUTATE (CFG644_MUTATE=1, *_MUTATE outputs): M1 r_nb = inf -> census stacks exactly; M2 shuffled neighbour sets within T3 cells;
M3 r_nb = 0.5 r_edge for every f30 lens.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg644_kids.py ; CFG644_MUTATE=1 ... (same)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, math, json, time, contextlib
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
sys.path.insert(0, HERE)
for _p in ("CFG503_two_halo_nonlinear", "CFG487_settled_fraction_switch", "CFG495_drawdown_shell"):
    sys.path.insert(0, os.path.join(LANES, _p))
import cfg644_lib as N                                                       # noqa: E402
C, L = N.C, N.L
with contextlib.redirect_stdout(io.StringIO()):
    import cfg503_own as OWN                                                 # noqa: E402  (read-only)
try:
    os.nice(10)
except OSError:
    pass
MUTATE = os.environ.get("CFG644_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg644_work"); os.makedirs(WORK, exist_ok=True)
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
FOOTS = ("canonical", "alt")
G = C.G_MPC
KG = 1.98847e30 / (3.0857e16) ** 2
NPATCH = 50
WIN, RQ, ANN = 10.0, 7.0, (4.0, 6.0)                       # |dchi| window (W10), query radius, purity annulus [comoving Mpc]
LOG, CHK = [], {}
RES = {"lane": "CFG644", "script": "cfg644_kids", "mutate": MUTATE, "criteria_commit": "6a03c0870",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
XN = np.array([0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30,
               0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80, 0.90, 1.00])
LXN = np.log(XN)


# ------------------------------------------------------------------ own-profile tables per group
def group_tables(Mg, zl):
    out = {}
    for foot in FOOTS:
        a0 = C.A0[foot]
        rta = C.r_ta_law(Mg, a0, zl)
        f = L.fret("census", Mg); re = L.r_edge_pm(Mg, G, a0, f)
        nodes = []
        for x in XN:
            r, Md = OWN.kids_Md(Mg, zl, a0, x * rta)
            nodes.append(OWN.kids_fin(Mg, r, Md))
        r, Md = OWN.kids_Md(Mg, zl, a0, min(re, rta))
        cen = OWN.kids_fin(Mg, r, Md)
        rr = np.geomspace(1e-4, rta, 1500)
        us = C._finish(lambda R: C.dsigma(R, rr, (rr / rta) ** 3), Mg)
        out[foot] = (rta, re, f, np.array(nodes), cen, us)
    return out


def build(tag, GM_, GZ_):
    path = os.path.join(WORK, f"cfg644_tables_{tag}.npz")
    if os.path.exists(path):
        T = dict(np.load(path)); P(f"  tables {tag} read from cache ({len(GM_)} groups)"); return T
    t = time.time(); T = {}
    acc = {foot: [[] for _ in range(6)] for foot in FOOTS}
    for g in range(len(GM_)):
        o = group_tables(float(GM_[g]), float(GZ_[g]))
        for foot in FOOTS:
            for i in range(6):
                acc[foot][i].append(o[foot][i])
        if g % 400 == 0:
            P(f"    {tag}: group {g}/{len(GM_)} ({time.time() - t:.0f} s)")
    for foot in FOOTS:
        for i, nm in enumerate(("rta", "re", "fret", "nodes", "cen", "usph")):
            T[f"{foot}|{nm}"] = np.array(acc[foot][i])
    np.savez(path, **T); P(f"  tables {tag} built in {time.time() - t:.0f} s")
    return T


OT3 = np.load(os.path.join(EXT, "cfg503_work", "cfg503_own_tables.npz"))
giP, GMP, GZP = OT3["gi"], OT3["GM"], OT3["GZ"]
giA, GMA, GZA = OT3["giA"], OT3["GMA"], OT3["GZA"]
P("\n== own-profile node tables (law truncated at x r_ta; census row; unit uniform sphere of radius r_ta) ==")
TP = build("P", GMP, GZP)
TA = build("ALL", GMA, GZA)
TB = np.load(os.path.join(EXT, "cfg525_work", "cfg525_tables.npz"))
k1 = 0.0
for foot in FOOTS:
    for j, x in enumerate(TB["XN"]):
        i = int(np.argmin(np.abs(XN - x))); assert abs(XN[i] - x) < 1e-12
        k1 = max(k1, float(np.max(np.abs(TP[f"{foot}|nodes"][:, i, :] / TB[f"{foot}|node|full"][:, j, :] - 1))))
    k1 = max(k1, float(np.max(np.abs(TP[f"{foot}|cen"] / TB[f"{foot}|dir|census|full"] - 1))))
check("K1 rebuilt stack-P node tables (x >= 0.06) and census rows = CFG525's committed-work tables (rel 1e-10)", k1 < 1e-10, f"max rel {k1:.1e}")


# ------------------------------------------------------------------ pool and neighbours (CFG525 rule)
c_ = 2.998e8; MPC = 3.0857e22; H0 = 70 * 1e3 / MPC


def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_ / H0) / MPC
    return np.interp(z, zz, chi)


b = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
Lp = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
rmag = np.array(b["MAG_AUTO_CALIB"], "f8"); zph = np.array(b["zphot_ANNz2"], "f8"); msk = np.array(b["masked"])
lMp = np.array(Lp["MASS_MED"], "f8") + 0.15
ra_ = np.array(b["RAJ2000"], "f8"); de_ = np.array(b["DECJ2000"], "f8")
del b, Lp
pool = (rmag < 20) & (zph > 0.1) & (zph < 0.5) & (msk == 0) & np.isfinite(lMp) & (lMp > 7)
ip = np.where(pool)[0]
chiP = DC(zph[ip]); lMP = lMp[ip]
MgP = 10 ** lMP * (1 + 10 ** (-0.69 * lMP + 6.63))
raP, deP = np.radians(ra_[ip]), np.radians(de_[ip])
xyzP = np.c_[np.cos(deP) * np.cos(raP), np.cos(deP) * np.sin(raP), np.sin(deP)]
del rmag, zph, msk, lMp, ra_, de_, raP, deP
TREE = cKDTree(xyzP)
P(f"\npool {len(ip):,} galaxies (CFG525 rule)")


def neighbours(ra, dec, chi, Mg):
    """pairs within RQ comoving projected and |dchi| < WIN, self (zero separation, same M_gal) excluded."""
    ra, dec = np.radians(ra), np.radians(dec)
    xyz = np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
    dd, jj = TREE.query(xyz, k=1)
    selfok = (dd < 1e-9) & np.isclose(MgP[jj], Mg, rtol=1e-6)
    SEG, J, RP = [], [], []
    CH = 20000
    for i0 in range(0, len(ra), CH):
        sl = slice(i0, min(i0 + CH, len(ra)))
        lists = TREE.query_ball_point(xyz[sl], r=RQ / chi[sl])
        cnt = np.array([len(x) for x in lists]); li = np.repeat(np.arange(sl.start, sl.stop), cnt)
        jx = np.concatenate([np.asarray(x, np.int64) for x in lists]) if cnt.sum() else np.zeros(0, np.int64)
        keep = (jx != jj[li]) & (np.abs(chiP[jx] - chi[li]) < WIN)
        li, jx = li[keep], jx[keep]
        rp = np.arccos(np.clip(np.einsum("ij,ij->i", xyz[li], xyzP[jx]), -1, 1)) * chi[li]
        SEG.append(li); J.append(jx); RP.append(rp)
    return np.concatenate(SEG), np.concatenate(J), np.concatenate(RP), selfok


def per_lens_rnb(Mg, z, seg, J, RP, a0, shuffle=None):
    """pairwise r_nb (closing neighbours) and bracket S (all window neighbours); physical Mpc."""
    if shuffle is not None:
        seg, J, RP = shuffle
    To = N.mtot(Mg); n = len(Mg)
    rp = np.full(n, np.inf); rs = np.full(n, np.inf)
    CHO = 60000                                                             # owner chunks (memory)
    for o0 in range(0, n, CHO):
        m = (seg >= o0) & (seg < o0 + CHO)
        sg = seg[m] - o0; Jm = J[m]; D = RP[m] / (1 + z[seg[m]])
        sl = slice(o0, min(o0 + CHO, n))
        rp[sl] = N.segmented_r_nb(Mg[sl], To[sl], sg, MgP[Jm], D, G, a0)
        rs[sl] = N.segmented_r_nb_summed(Mg[sl], To[sl], sg, MgP[Jm], D, G, a0)
    return rp, rs


def h_vectors(T, foot, g, x_nb, Mg, mode="U0"):
    """per lens own profile (15) for H-NB: census row where x_nb >= x_census, else node interpolation at x_nb (+ remainder)."""
    rta, re = T[f"{foot}|rta"][g], T[f"{foot}|re"][g]
    xc = np.minimum(re / rta, 1.0)
    out = T[f"{foot}|cen"][g].copy()
    bite = x_nb < xc
    if bite.any():
        gb = g[bite]; xb = np.clip(x_nb[bite], XN[0], XN[-1])
        lx = np.log(xb); i = np.clip(np.searchsorted(LXN, lx) - 1, 0, len(XN) - 2)
        w = ((lx - LXN[i]) / (LXN[i + 1] - LXN[i]))[:, None]
        nod = T[f"{foot}|nodes"]
        v = (1 - w) * nod[gb, i, :] + w * nod[gb, i + 1, :]
        if mode == "U0":
            a0 = C.A0[foot]
            rnb = xb * rta[bite]
            Mu = np.maximum(N.supply(Mg[bite]) - N.phantom(Mg[bite], rnb, G, a0), 0.0)
            v = v + Mu[:, None] * T[f"{foot}|usph"][gb]
        out[bite] = v
    return out, bite


def h_uncapped(T, foot, g, x_nb):
    """reported T2-U: law profile to min(r_nb, r_ta), no supply cap."""
    xb = np.clip(np.minimum(x_nb, 1.0), XN[0], XN[-1])
    lx = np.log(xb); i = np.clip(np.searchsorted(LXN, lx) - 1, 0, len(XN) - 2)
    w = ((lx - LXN[i]) / (LXN[i + 1] - LXN[i]))[:, None]
    nod = T[f"{foot}|nodes"]
    return (1 - w) * nod[g, i, :] + w * nod[g, i + 1, :]


def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)


def esd_full_loo(WG_, WW_, patch_, mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch_[mask], weights=WG_[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch_[mask], weights=WW_[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


def stack(WW_, mask, V):
    return (WW_[mask] * V[mask]).sum(0) / WW_[mask].sum(0)


def chi2(d, Cv, m, delta=None):
    Ct = Cv / hart(15) + (np.outer(delta, delta) if delta is not None else 0.0)
    r = d - m
    return float(r @ np.linalg.solve(Ct, r))


# ================================================================== T2: stack P / f30
P("\n================ T2: isolated stacks (stack P, f30 primary) ================")
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
zL, MgL, chiL = lens["z"].astype(float), lens["Mgal"].astype(float), lens["chi"].astype(float)
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
F30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
ALLP = np.ones(len(zL), bool)
segP, JP, RPP, selfP = neighbours(lens["ra"], lens["dec"], chiL, MgL)
check("K2 every stack-P lens found in the pool at zero separation with identical M_gal", bool(selfP.all()), f"{int(selfP.sum())}/{len(selfP)}")
P(f"  stack P: {len(zL):,} lenses; window pairs within {RQ} Mpc: {len(segP):,} (mean {len(segP) / len(zL):.2f} per lens)")
d30, C30 = esd_full_loo(WG, WW, patch, F30)
dP_, CP_ = esd_full_loo(WG, WW, patch, ALLP)
J377 = json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))
check("K3 stack-P raw ESD = CFG377 primary (1e-10)", np.max(np.abs(dP_ / np.array(J377["primary"]["esd"]) - 1)) < 1e-10, "data vector")
J529 = json.load(open(os.path.join(LANES, "CFG529_f30_matched_environment", "cfg529_score_results.json")))
k4 = 0.0
for cons in ("A", "B"):
    for foot in FOOTS:
        row = J529["rescore_f30"][cons][foot]["rows"]["CENSUS"]
        mM, mB = np.array(row["model"]), np.array(row["model_behroozi"])
        k4 = max(k4, abs(chi2(d30, C30, mM, mB - mM) - row["chi2"]))
check("K4 CONTEXT harness: CFG529's committed CENSUS vectors with its covariance reproduce its census chi2 (A, B, both footings)", k4 < 1e-6, f"max |d| {k4:.1e}")

T2 = {}
for foot in FOOTS:
    a0 = C.A0[foot]
    rnb, rS = per_lens_rnb(MgL, zL, segP, JP, RPP, a0)
    if MUTATE:
        rnb_m3 = 0.5 * TP[f"{foot}|re"][giP]
    rta_l = TP[f"{foot}|rta"][giP]; re_l = TP[f"{foot}|re"][giP]
    Vb = TP[f"{foot}|cen"][giP]
    out = {}
    variants = {"primary_U0": (rnb, "U0"), "U_drop": (rnb, "drop"), "bracket_S": (rS, "U0"), "M1_rnb_inf": (np.full(len(zL), np.inf), "U0")}
    if MUTATE:
        variants["M3_half_edge"] = (rnb_m3, "U0")
    for sname, smask in (("f30", F30), ("stackP", ALLP)):
        d, Cv = (d30, C30) if sname == "f30" else (dP_, CP_)
        w = WW.sum(1)
        mB = stack(WW, smask, Vb); cB = chi2(d, Cv, mB)
        row = dict(chi2_B=cB, model_B=mB.tolist())
        for vname, (rr, mode) in variants.items():
            Vh, bite = h_vectors(TP, foot, giP, rr / rta_l, MgL, mode)
            mH = stack(WW, smask, Vh); cH = chi2(d, Cv, mH)
            fb = float(w[smask & bite].sum() / w[smask].sum())
            row[vname] = dict(bite_weight_frac=fb, n_bite=int((smask & bite).sum()), chi2=cH, dchi2=cH - cB,
                              max_rel_model_change=float(np.max(np.abs(mH / mB - 1))), model=mH.tolist())
            if sname == "f30" and vname in ("primary_U0", "bracket_S", "M3_half_edge"):
                ctx = {}
                for cons in ("A", "B"):
                    rr529 = J529["rescore_f30"][cons][foot]["rows"]["CENSUS"]
                    m0, m1 = np.array(rr529["model"]), np.array(rr529["model_behroozi"])
                    c0 = chi2(d, Cv, m0, m1 - m0); dl = mH - mB
                    c1 = chi2(d, Cv, m0 + dl, m1 - m0)
                    ctx[cons] = dict(census_chi2=c0, hnb_chi2=c1, dchi2=c1 - c0)
                row[vname]["CONTEXT_CFG529_env"] = ctx
        # reported T2-U (supply cap lifted)
        Vu = h_uncapped(TP, foot, giP, rnb / rta_l)
        mU = stack(WW, smask, Vu); row["T2U_uncapped_reported"] = dict(chi2=chi2(d, Cv, mU), dchi2=chi2(d, Cv, mU) - cB,
                                                                       frac_rnb_ge_rta=float(w[smask & (rnb >= rta_l)].sum() / w[smask].sum()))
        # distribution of r_nb / r_edge (lens weight)
        q = rnb / re_l
        row["rnb_over_redge_weighted_pct"] = {p_: float(np.percentile(np.where(np.isfinite(q[smask]), q[smask], 1e9), p_)) for p_ in (1, 5, 16, 50)}
        row["frac_no_closing_neighbour"] = float(w[smask & ~np.isfinite(rnb)].sum() / w[smask].sum())
        row["min_rnb_over_redge"] = float(np.min(q[smask]))
        out[sname] = row
        pr = row["primary_U0"]
        P(f"  [{foot}] {sname:6s}: bite weight {pr['bite_weight_frac']:.5f} (N {pr['n_bite']}); chi2 B {cB:.3f} -> H-NB {pr['chi2']:.3f} "
          f"(d {pr['dchi2']:+.4f}); U-drop d {row['U_drop']['dchi2']:+.4f}; bracket S bite {row['bracket_S']['bite_weight_frac']:.5f} "
          f"d {row['bracket_S']['dchi2']:+.4f}; M1 d {row['M1_rnb_inf']['dchi2']:+.1e}; no closing nbr {row['frac_no_closing_neighbour']:.3f}; "
          f"min r_nb/r_edge {row['min_rnb_over_redge']:.2f}; T2-U d {row['T2U_uncapped_reported']['dchi2']:+.2f} "
          f"(r_nb >= r_ta weight {row['T2U_uncapped_reported']['frac_rnb_ge_rta']:.3f})")
        if sname == "f30":
            for vn in ("primary_U0", "bracket_S") + (("M3_half_edge",) if MUTATE else ()):
                cx = row[vn]["CONTEXT_CFG529_env"]
                P(f"      CONTEXT (CFG529 LCDM-built env) {vn}: A {cx['A']['census_chi2']:.2f} -> {cx['A']['hnb_chi2']:.2f}; "
                  f"B {cx['B']['census_chi2']:.2f} -> {cx['B']['hnb_chi2']:.2f}")
            if MUTATE:
                P(f"      M3 (r_nb = 0.5 r_edge): native chi2 {row['M3_half_edge']['chi2']:.3f} (d {row['M3_half_edge']['dchi2']:+.3f})")
    dn = out["f30"]["primary_U0"]["dchi2"]
    out["verdict"] = "IMPROVES" if dn <= -4 else "WORSENS" if dn >= 4 else "NO CHANGE"
    check(f"M1 [{foot}] r_nb = inf reproduces the census stacks exactly (f30 and stack P)",
          out["f30"]["M1_rnb_inf"]["max_rel_model_change"] == 0 and out["stackP"]["M1_rnb_inf"]["max_rel_model_change"] == 0, "max rel 0")
    if MUTATE:
        check(f"M3 [{foot}] tooth: r_nb = 0.5 r_edge moves the f30 native chi2 by >= 4", abs(out["f30"]["M3_half_edge"]["dchi2"]) >= 4,
              f"d chi2 {out['f30']['M3_half_edge']['dchi2']:+.3f}")
    T2[foot] = out
    P(f"  [{foot}] T2 VERDICT (f30, native): {out['verdict']}")
RES["T2"] = T2
del segP, JP, RPP

# ================================================================== T3: ALL parent sample
P("\n================ T3: ALL parent sample, dense vs isolated (sign test) ================")
S = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
zA, MgA, chiA = S["z"].astype(float), S["Mgal"].astype(float), S["chi"].astype(float)
lMA = S["logM"].astype(float)
WGA, WWA, pA = S["WG"], S["WW"], S["patch_all"]
nA = len(zA)
segA, JA, RPA, selfA = neighbours(S["ra"], S["dec"], chiA, MgA)
check("K5 every ALL lens found in the pool at zero separation with identical M_gal", bool(selfA.all()), f"{int(selfA.sum())}/{nA}")
P(f"  ALL: {nA:,} lenses; window pairs within {RQ} Mpc: {len(segA):,} (mean {len(segA) / nA:.2f})")
# cells: 10 log M* deciles x z bins
qd = np.quantile(lMA, np.linspace(0, 1, 11)); qd[-1] += 1e-9
ZB = np.array([0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5 + 1e-9])
CELL = np.clip(np.searchsorted(qd, lMA, side="right") - 1, 0, 9) * 10 + np.clip(np.searchsorted(ZB, zA, side="right") - 1, 0, 5)
GEK = C.GEDGE_K                                                             # bin k spans g in [GEK[k], GEK[k+1]]
ROUT = np.sqrt(G * MgA[:, None] / GEK[None, :-1])                            # physical Mpc, outer radius of each bin
BANDS = {"OUT": list(range(0, 9)), "K-out": [6, 7, 8], "outer6": list(range(0, 6))}
order = np.argsort(segA, kind="stable"); segA, JA, RPA = segA[order], JA[order], RPA[order]
cnt = np.bincount(segA, minlength=nA); start = np.concatenate([[0], np.cumsum(cnt)[:-1]])


def shuffled_pairs(rng):
    perm = np.arange(nA)
    for c in np.unique(CELL):
        m = np.nonzero(CELL == c)[0]; perm[m] = rng.permutation(m)
    src = perm
    n_new = cnt[src]
    seg_new = np.repeat(np.arange(nA), n_new)
    offs = np.arange(n_new.sum()) - np.repeat(np.cumsum(n_new) - n_new, n_new)
    idx = np.repeat(start[src], n_new) + offs
    return seg_new, JA[idx], RPA[idx]


def clear_zone_f(seg, J, RP, a0):
    D = RP / (1 + zA[seg])
    sig = MgP[J] >= 0.1 * MgA[seg]
    sc = np.full(nA, np.inf)
    np.minimum.at(sc, seg[sig], D[sig] - N.r_edge(MgP[J[sig]], G, a0))
    return sc


def purity(seg, J, RP, a0, re_l, dense, wl):
    """p = 1 - n_bg/n_raw for biting closing neighbours of DENSE lenses (CFG502/509 annulus method)."""
    D = RP / (1 + zA[seg]); To = N.mtot(MgA); cl = N.mtot(MgP[J]) >= To[seg]
    inn = cl & dense[seg]
    rj = N.r_pair(MgA[seg[inn]], MgP[J[inn]], D[inn], G, a0)
    n_raw = np.bincount(seg[inn], weights=(rj < re_l[seg[inn]]).astype(float), minlength=nA)
    ann = cl & dense[seg] & (RP >= ANN[0]) & (RP < ANN[1])
    sa = seg[ann]; Mo, Mj = MgA[sa], MgP[J[ann]]; target = re_l[sa]
    lo = np.zeros(len(sa)); hi = np.full(len(sa), 50.0)                     # D_b in physical Mpc
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        rr = N.r_pair(Mo, Mj, mid, G, a0, n_iter=40)
        big = rr > target
        hi = np.where(big, mid, hi); lo = np.where(big, lo, mid)
    Db_c = 0.5 * (lo + hi) * (1 + zA[sa])                                    # comoving
    A_ann = math.pi * (ANN[1] ** 2 - ANN[0] ** 2)
    n_bg = np.bincount(sa, weights=np.minimum(math.pi * Db_c ** 2, A_ann) / A_ann, minlength=nA)
    nr, nb = float((wl * n_raw)[dense].sum()), float((wl * n_bg)[dense].sum())
    return (1 - nb / nr) if nr > 0 else float("nan"), nr, nb


def amp(num, den, dense, iso):
    q = (num[dense].sum() / den[dense].sum()) / (num[iso].sum() / den[iso].sum())
    return math.log10(q) if q > 0 else float("nan")


def jk_amp(num, den, dense, iso):
    vals = []
    for k in range(NPATCH):
        m = pA != k
        vals.append(amp(num, den, dense & m, iso & m))
    v = np.array(vals); v = v[np.isfinite(v)]
    return float(math.sqrt((NPATCH - 1) / NPATCH * ((v - v.mean()) ** 2).sum()))


def relabel_null(num, den, dense, rng, nperm=200, valid=None, fn=None):
    """within-cell relabelling of DENSE among the valid lenses (lenses with kept bins in the band)."""
    valid = np.ones(nA, bool) if valid is None else valid
    fn = amp if fn is None else fn
    out = []
    cells = [np.nonzero((CELL == c) & valid)[0] for c in np.unique(CELL)]
    for _ in range(nperm):
        dd = np.zeros(nA, bool)
        for m in cells:
            nd = int(dense[m].sum())
            if nd:
                dd[rng.choice(m, nd, replace=False)] = True
        out.append(fn(num, den, dd, valid & ~dd))
    out = np.array(out)
    return out[np.isfinite(out)]


def amp_bm(numk, denk, dense, iso):
    """REPORTED (post hoc, written after the first T3 run): bin-matched amplitude; per-bin data/B ratios of DENSE and ISO combined
    with the same (DENSE kept, model-weighted) bin weights, so a radial mismatch of the B model cannot enter through the masks."""
    nd, dd_ = numk[dense].sum(0), denk[dense].sum(0)
    ni, di = numk[iso].sum(0), denk[iso].sum(0)
    ok = (dd_ > 0) & (di > 0)
    if not ok.any():
        return float("nan")
    w = dd_[ok]
    q = (w @ (nd[ok] / dd_[ok])) / (w @ (ni[ok] / di[ok]))
    return math.log10(q) if q > 0 else float("nan")


T3 = {}
wlA = WWA.sum(1)
for foot in FOOTS:
    a0 = C.A0[foot]
    re_l = TA[f"{foot}|re"][giA]; rta_l = TA[f"{foot}|rta"][giA]
    Vb = TA[f"{foot}|cen"][giA]
    runs = {"primary": None}
    if MUTATE:
        runs = {"M2_shuffled": shuffled_pairs(np.random.default_rng(644))}
    out = {}
    for rname, shuf in runs.items():
        sg, Jn, Rn = (segA, JA, RPA) if shuf is None else shuf
        rnb, rS = per_lens_rnb(MgA, zA, sg, Jn, Rn, a0)
        sc = clear_zone_f(sg, Jn, Rn, a0)
        mk = ROUT < sc[:, None]
        res_r = {}
        for vname, rr in (("primary", rnb), ("bracket_S", rS)):
            dense = rr < re_l; iso = ~dense
            Vh, bite = h_vectors(TA, foot, giA, rr / rta_l, MgA, "U0")
            p_, nr, nb = purity(sg, Jn, Rn, a0, re_l, dense, wlA) if vname == "primary" else (float("nan"), 0, 0)
            bands = {}
            rng = np.random.default_rng(6440 + (0 if foot == "canonical" else 1))
            for bn, ks in BANDS.items():
                kk = np.zeros(15, bool); kk[ks] = True
                mm = mk & kk[None, :]
                num = (WGA * mm).sum(1) / KG; denB = (WWA * mm * Vb).sum(1); denH = (WWA * mm * Vh).sum(1)
                ok = denB > 0
                dsel, isel = dense & ok, iso & ok
                if dsel.sum() < 50:
                    bands[bn] = dict(n_dense=int(dsel.sum()), note="too few dense lenses with kept bins"); continue
                Ad = amp(num, denB, dsel, isel)
                Ap = math.log10((denH[dsel].sum() / denB[dsel].sum()) / (denH[isel].sum() / denB[isel].sum()))
                sj = jk_amp(num, denB, dsel, isel)
                nl = relabel_null(num, denB, dsel, rng, 200 if (bn == "OUT" and vname == "primary") else 60, valid=ok)
                se = float(nl.std())
                rep = {}
                if bn == "OUT":
                    numk = (WGA[:, ks] * mm[:, ks]) / KG; dBk = WWA[:, ks] * mm[:, ks] * Vb[:, ks]; dHk = WWA[:, ks] * mm[:, ks] * Vh[:, ks]
                    Abm = amp_bm(numk, dBk, dsel, isel)
                    nbm = relabel_null(numk, dBk, dsel, rng, 60, valid=ok, fn=amp_bm)
                    sbm = float(nbm.std())
                    Apbm = amp_bm(dHk * 1.0, dBk, dsel, isel)
                    del numk, dBk, dHk
                    numu = WGA[:, ks].sum(1) / KG; dBu = (WWA[:, ks] * Vb[:, ks]).sum(1); dHu = (WWA[:, ks] * Vh[:, ks]).sum(1)
                    Au = amp(numu, dBu, dense, iso); Apu = math.log10((dHu[dense].sum() / dBu[dense].sum()) / (dHu[iso].sum() / dBu[iso].sum()))
                    nu_ = relabel_null(numu, dBu, dense, rng, 60, fn=amp); su = float(nu_.std())
                    rep = dict(bin_matched_POSTHOC=dict(A_data=Abm, sig_emp=sbm, Z=Abm / sbm if sbm > 0 else float("nan"), A_pred=Apbm),
                               unmasked_CONTAMINATED=dict(A_data=Au, sig_emp=su, Z=Au / su if su > 0 else float("nan"), A_pred=Apu))
                    P(f"      reported: bin-matched (post hoc) A_data {Abm:+.4f} +- {sbm:.4f} (Z {Abm / sbm:+.2f}), A_pred {Apbm:+.4f}; "
                      f"unmasked (neighbour lensing included) A_data {Au:+.4f} +- {su:.4f} (Z {Au / su:+.2f}), A_pred {Apu:+.4f}")
                Apc = Ap * p_ if np.isfinite(p_) else Ap
                if abs(Apc) < 2 * se:
                    cls = "NOT DIAGNOSTIC"
                else:
                    cls = None
                dcls = ("SUPPORT" if (Ad <= -2 * se and abs(Ad - Apc) <= 2 * se) else "NOT SUPPORTED (sign)" if Ad >= 0 else "WEAK")
                bands[bn] = dict(n_dense=int(dsel.sum()), n_iso=int(isel.sum()), w_dense_frac=float(wlA[dsel].sum() / wlA[ok].sum()),
                                 kept_bin_frac_dense=float(mm[dsel][:, ks].mean()), kept_bin_frac_iso=float(mm[isel][:, ks].mean()),
                                 A_data=Ad, sig_emp=se, sig_jk=sj, Z=Ad / se, null_mean=float(nl.mean()), A_pred=Ap, A_pred_corr=Apc,
                                 Z_pred_corr=Apc / se, data_class=dcls, power_class=cls or "DIAGNOSTIC", reported=rep)
                P(f"  [{foot}] {rname}/{vname:9s} {bn:6s}: N dense {dsel.sum():6d} (w {bands[bn]['w_dense_frac']:.3f}; kept bins {bands[bn]['kept_bin_frac_dense']:.2f} vs iso "
                  f"{bands[bn]['kept_bin_frac_iso']:.2f})  A_data {Ad:+.4f} +- {se:.4f} (Z {Ad / se:+.2f}; jk {sj:.4f}; null mean {nl.mean():+.4f})  "
                  f"A_pred {Ap:+.4f} -> x purity {Apc:+.4f} (Z {Apc / se:+.2f})  => {dcls}; {cls or 'DIAGNOSTIC'}")
            res_r[vname] = dict(bands=bands, purity=p_, n_raw_w=nr, n_bg_w=nb, frac_dense_w=float(wlA[dense].sum() / wlA.sum()),
                                n_dense=int(dense.sum()))
            if vname == "primary":
                P(f"  [{foot}] {rname}: DENSE lenses {dense.sum():,} (weight {res_r[vname]['frac_dense_w']:.4f}); purity p {p_:.3f} "
                  f"(weighted raw {nr:.1f} vs background {nb:.1f})")
        out[rname] = res_r
    if not MUTATE:
        b_ = out["primary"]["primary"]["bands"]["OUT"]
        out["verdict"] = dict(data_class=b_.get("data_class"), power_class=b_.get("power_class"))
        P(f"  [{foot}] T3 VERDICT (OUT, primary): {out['verdict']}")
    else:
        b_ = out["M2_shuffled"]["primary"]["bands"]["OUT"]
        if "A_data" in b_:
            check(f"M2 [{foot}] shuffled neighbour sets: |A_data| < 2 sigma (environment trend removed)", abs(b_["Z"]) < 2,
                  f"A {b_['A_data']:+.4f} Z {b_['Z']:+.2f}")
    T3[foot] = out
RES["T3"] = T3
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c in CHK.values() if c["load_bearing"] and not c["ok"])
P(f"\n{sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg644_kids_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg644_kids{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
