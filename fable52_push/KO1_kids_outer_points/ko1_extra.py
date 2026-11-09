#!/usr/bin/env python3
"""KO1 extras (AMENDMENT_A1.md, ae28af31fa, section 4).  REPORTED ONLY: no label rests on anything here.
E1 profiles in all 15 bins by type; E2 stricter and looser hosts; E3 the type split with its joint error; E4 late types by
redshift and mass half.  Added after A1 as diagnostics of items the main run already showed: E5 the permutation distribution
behind M1 (how much of hosted - host-free is composition); E6 the host excess by projected separation (R4's total is negative
because the record's isolation removes pairs at |dchi| < 10 Mpc).
Run: python3 ko1_extra.py -> ko1_extra.json, ko1_extra.out.   kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
T0 = time.time(); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt")
X_CAP = 53.64; X_SHARE = 0.11958060485606123 / 0.0215; NPAT = 50
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def glaw(g, a0): return nu(g / a0) * g
def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
def mgal_of(logMs): return 10 ** logMs * (1 + 10 ** (-0.69 * logMs + 6.63))

ln = np.load(os.path.join(DATA, "lr_lenses.npz")); PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WG, WW, EDGES = PL["WG"], PL["WW"], PL["gbar_edges"]
FL = np.load(os.path.join(DATA, "cfg96_isoflags.npz")); f20, f30 = FL["f20"], FL["f30"]
patch = np.load(os.path.join(DATA, "cfg96_stack.npz"))["patch"]
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
ALL = np.ones(NL, bool); LATE = typ == 0; EARLY = typ == 1
NB = 15; XG, WGL = np.polynomial.legendre.leggauss(24); R3 = (3.0 * Mpc) ** 2
def cells(fun):
    m = np.zeros((NL, NB))
    for k in range(NB):
        t_lo = G * Mg / EDGES[k + 1]; t_hi = np.minimum(G * Mg / EDGES[k], R3); ok = t_hi > t_lo
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            f = fun(G * Mg[:, None] / t)
        m[:, k] = np.where(ok, (f * WGL[None, :]).sum(1) / 2, 0.0)
    return m
LAW = {f: cells(lambda g, a=A0[f]: glaw(g, a)) for f in FOOT}
TPC = cells(lambda g: (4 / math.pi) * (1 + X_CAP) * g)
def psum(arr, mask):
    pm = patch[mask]; a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, c], minlength=NPAT) for c in range(arr.shape[1])], axis=1)
def amp(mask, Mo, cols, WGx=None):
    WGx = WG if WGx is None else WGx
    Sg = psum(WGx[:, cols], mask); Sw = psum(WW[:, cols], mask); Sm = psum((WW * Mo)[:, cols], mask)
    tg, tw, tm = Sg.sum(0), Sw.sum(0), Sm.sum(0)
    D = 4 * G * tg / tw; M = tm / tw
    Dl = 4 * G * (tg - Sg) / (tw - Sw); Ml = (tm - Sm) / (tw - Sw)
    sk = np.sqrt((NPAT - 1) / NPAT * ((Dl - Dl.mean(0)) ** 2).sum(0))
    A = float((D * M / sk ** 2).sum() / (M * M / sk ** 2).sum())
    Al = (Dl * Ml / sk ** 2).sum(1) / (Ml * Ml / sk ** 2).sum(1)
    s = float(np.sqrt((NPAT - 1) / NPAT * ((Al - Al.mean()) ** 2).sum()))
    return dict(A=A, s=s, Al=Al, D=D, M=M, sk=sk, n=int(mask.sum()), w=float(tw.sum()))
def jdiff(r1, r2):
    d = r1["Al"] - r2["Al"]; return float(r1["A"] - r2["A"]), float(np.sqrt((NPAT - 1) / NPAT * ((d - d.mean()) ** 2).sum()))
OUTER, MID, INNER = [0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12]

# ------------------------------------------------------------------ catalogue and scans
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
r_ = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); z_ = np.array(b["zphot_ANNz2"], dtype="f8"); masked = np.array(b["masked"]).astype(np.int64)
logM_ = np.array(Lp["MASS_MED"], dtype="f8") + 0.15; ur_ = np.array(Lp["MAG_ABS_u"] - Lp["MAG_ABS_r"], dtype="f8")
ra_ = np.array(b["RAJ2000"], dtype="f8"); dec_ = np.array(b["DECJ2000"], dtype="f8"); del b, Lp; HB.close(); HL.close()
nb = (r_ < 20) & (z_ >= 0.02) & (z_ <= 0.8) & np.isfinite(logM_) & (logM_ > 7); inb = np.where(nb)[0]
xN = unitvec(ra_[inb], dec_[inb]); chiN = DC(z_[inb]); logMN = logM_[inb]
# the lenses' rows in the pool: match on (ra, dec) exactly (KA2 of the main run shows lr_lenses is a row subset of the catalogue)
key = {(a, d): i for i, (a, d) in enumerate(zip(ra_[inb], dec_[inb]))}
selfN = np.array([key[(a, d)] for a, d in zip(ln["ra"], ln["dec"])]); assert np.allclose(logMN[selfN], logMs)
treeN = cKDTree(xN); xL = xN[selfN]
def rh_of(logM): return np.minimum(3.0, np.sqrt(G * mgal_of(logM) * Msun / 1e-15) / Mpc)
def chord_of(logM): return 2 * np.sin(rh_of(logM) * (1 + zl) / chil / 2)
DE = np.array([0.0, 0.25, 0.5, 1.0, 2.0, 3.0001]); CE = np.array([0.0, 10.0, 115.0, 230.0, 500.0])
def scan(Lx, LlogM, Lself, chord, dmass, hist2d=False, CH=400):
    n = NL; dmin = np.full(n, np.inf); H2 = np.zeros((len(DE) - 1, len(CE) - 1)) if hist2d else None
    DAl = chil / (1 + zl)
    for i0 in range(0, n, CH):
        i1 = min(i0 + CH, n)
        lists = treeN.query_ball_point(Lx[i0:i1], r=chord[i0:i1])
        c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(c.sum())
        if tot == 0: continue
        k = np.repeat(np.arange(len(c)), c); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot); li = i0 + k
        keep = (j != Lself[li]) & (logMN[j] >= LlogM[li] + dmass); li, j = li[keep], j[keep]
        dc = np.abs(chiN[j] - chil[li]); np.minimum.at(dmin, li, dc)
        if hist2d:
            d = 2 * np.arcsin(np.minimum(np.linalg.norm(xN[j] - Lx[li], axis=1) / 2, 1.0)) * DAl[li]
            H2 += np.histogram2d(d, dc, bins=[DE, CE])[0]
    return dmin, H2
P(f"KO1 extras.  lenses {NL:,}; neighbour pool {len(inb):,}  [{time.time() - T0:.0f} s]")
W = 230.0
DM = {}
for dm in (0.3, 0.0, -0.3):
    d0, H2 = scan(xL, logMs, selfN, chord_of(logMs), dm, hist2d=(dm == 0.3))
    dp = scan(xL, logMs + 0.1, selfN, chord_of(logMs + 0.1), dm)[0]; dn = scan(xL, logMs - 0.1, selfN, chord_of(logMs - 0.1), dm)[0]
    DM[dm] = dict(hf=d0 >= W, hp=dp >= W, hm=dn >= W, H2=H2)
    P(f"  Delta {dm:+.1f}: host-free {int((d0 >= W).sum()):,}  [{time.time() - T0:.0f} s]")
HF = DM[0.3]["hf"]; assert int(HF.sum()) == 40667, int(HF.sum())
perm = np.random.default_rng(52).permutation(NL)
H2s = scan(xL[perm], logMs, selfN[perm], chord_of(logMs), 0.3, hist2d=True)[1]
q1, q2 = np.quantile(logMs, [1 / 3, 2 / 3]); terc = np.digitize(logMs, [q1, q2])
def corr_factor(sel, dm, sig=0.2):
    """mass-scatter factor for the host-free lenses in `sel` at host threshold dm: e = b sigma^2, b weighted over mass terciles."""
    hf, hp, hm = DM[dm]["hf"], DM[dm]["hp"], DM[dm]["hm"]; bs, ws = [], []
    for t in range(3):
        m = sel & (terc == t)
        if hp[m].sum() == 0 or hm[m].sum() == 0: continue
        bs.append((math.log(hp[m].mean()) - math.log(hm[m].mean())) / 0.2); ws.append(WW[m & hf][:, OUTER].sum())
    ws = np.array(ws) / np.sum(ws); be = float((ws * np.array(bs)).sum())
    return be, 10 ** (be * sig ** 2 / 2)

RES = dict(lane="KO1", stage="extras", amendment="ae28af31fa", note="reported only; no label rests on these", foot={})
SUB = {"host-free all": HF, "host-free late": HF & LATE, "host-free early": HF & EARLY, "W30 all": f30, "W30 late": f30 & LATE, "W30 early": f30 & EARLY,
       "host-free and W30 all": HF & f30, "host-free and W30 late": HF & f30 & LATE, "host-free and W30 early": HF & f30 & EARLY,
       "hosted late": ~HF & LATE, "hosted early": ~HF & EARLY, "W10 late": LATE, "W10 early": EARLY, "W10 all": ALL}
for foot in FOOT:
    L = LAW[foot]; F = {}
    P(f"\n================ footing {foot}")
    # E1 ------------------------------------------------------------------------------------------------------------
    P("E1 windows: outer (bins 0-3, g_bar < 9.7e-15) | middle (bins 4-6, to 5.3e-14) | inner (bins 7-12, to 1.6e-12);  A = stack / law")
    F["E1"] = {}
    for name, m in SUB.items():
        ro, rm, ri = amp(m, L, OUTER), amp(m, L, MID), amp(m, L, INNER)
        prof = amp(m, L, list(range(NB)))
        F["E1"][name] = dict(n=int(m.sum()), outer=(ro["A"], ro["s"]), middle=(rm["A"], rm["s"]), inner=(ri["A"], ri["s"]),
                             profile=[float(a / b) for a, b in zip(prof["D"], prof["M"])], profile_err=[float(a / b) for a, b in zip(prof["sk"], prof["M"])])
        P(f"  {name:26s} n {int(m.sum()):7,d}  outer {ro['A']:+.3f} +- {ro['s']:.3f} | middle {rm['A']:+.3f} +- {rm['s']:.3f} | inner {ri['A']:+.3f} +- {ri['s']:.3f}")
    for name in ("host-free late", "host-free early", "W30 late", "W30 early"):
        e = F["E1"][name]
        P(f"  profile {name:16s}: " + " ".join(f"{a:+.2f}({b:.2f})" for a, b in zip(e["profile"], e["profile_err"])))
    tpo = {name: float(((WW * TPC)[m][:, OUTER].sum(0) / WW[m][:, OUTER].sum(0)).sum() / ((WW * L)[m][:, OUTER].sum(0) / WW[m][:, OUTER].sum(0)).sum())
           for name, m in (("host-free late", HF & LATE), ("host-free early", HF & EARLY))}
    P(f"  two-phase exterior at the census cap, unweighted over O: late {tpo['host-free late']:.3f}, early {tpo['host-free early']:.3f}")
    F["E1_two_phase_cap_by_type"] = tpo
    # E2 ------------------------------------------------------------------------------------------------------------
    P("E2 host threshold at W 230 Mpc (outer bins): Delta, lenses, outer-weight share, A pooled, late, early, mass-scatter factor (sigma_M 0.2)")
    F["E2"] = {}
    wtot = WW[:, OUTER].sum()
    for dm in (0.3, 0.0, -0.3):
        hf = DM[dm]["hf"]; ra, rl, re = amp(hf, L, OUTER), amp(hf & LATE, L, OUTER), amp(hf & EARLY, L, OUTER)
        be, cf = corr_factor(ALL, dm)
        F["E2"][f"{dm:+.1f}"] = dict(n=int(hf.sum()), f_w=float(WW[hf][:, OUTER].sum() / wtot), all=(ra["A"], ra["s"]), late=(rl["A"], rl["s"]), early=(re["A"], re["s"]), b=be, factor=cf)
        P(f"  Delta {dm:+.1f}: {int(hf.sum()):7,d}  f_w {WW[hf][:, OUTER].sum() / wtot:.3f}  all {ra['A']:+.3f} +- {ra['s']:.3f}  late {rl['A']:+.3f} +- {rl['s']:.3f}  early {re['A']:+.3f} +- {re['s']:.3f}  b {be:.2f}  factor {cf:.3f}")
    # E3 ------------------------------------------------------------------------------------------------------------
    P("E3 early minus late, outer bins, joint jackknife")
    F["E3"] = {}
    for name, base in (("host-free", HF), ("W30", f30), ("W10", ALL)):
        re, rl = amp(base & EARLY, L, OUTER), amp(base & LATE, L, OUTER); d, sd = jdiff(re, rl)
        F["E3"][name] = dict(diff=d, s=sd, z=d / sd)
        P(f"  {name:10s} early - late = {d:+.3f} +- {sd:.3f}  ({d / sd:+.2f} sigma)")
    bl, cl = corr_factor(LATE, 0.3); be_, ce = corr_factor(EARLY, 0.3)
    rl, re = amp(HF & LATE, L, OUTER), amp(HF & EARLY, L, OUTER)
    F["E3"]["mass_scatter_by_type"] = dict(late=dict(b=bl, factor=cl, A=rl["A"] * cl, s=rl["s"] * cl), early=dict(b=be_, factor=ce, A=re["A"] * ce, s=re["s"] * ce))
    P(f"  mass-scatter factors (sigma_M 0.2): late b {bl:.2f} x{cl:.3f} -> {rl['A'] * cl:+.3f} +- {rl['s'] * cl:.3f};  early b {be_:.2f} x{ce:.3f} -> {re['A'] * ce:+.3f} +- {re['s'] * ce:.3f}")
    # E4 ------------------------------------------------------------------------------------------------------------
    P("E4 host-free late types by halves (outer bins)")
    hl = HF & LATE; zm = np.median(zl[hl]); mm = np.median(logMs[hl]); F["E4"] = {}
    for name, m in (("z low", hl & (zl <= zm)), ("z high", hl & (zl > zm)), ("mass low", hl & (logMs <= mm)), ("mass high", hl & (logMs > mm))):
        ro, ri = amp(m, L, OUTER), amp(m, L, INNER)
        F["E4"][name] = dict(n=int(m.sum()), outer=(ro["A"], ro["s"]), inner=(ri["A"], ri["s"]))
        P(f"  {name:10s} n {int(m.sum()):6,d}  outer {ro['A']:+.3f} +- {ro['s']:.3f} | inner {ri['A']:+.3f} +- {ri['s']:.3f}")
    F["E4"]["medians"] = dict(z=float(zm), logM=float(mm), n=int(hl.sum()), outer_weight_share=float(WW[hl][:, OUTER].sum() / WW[HF][:, OUTER].sum()))
    P(f"  host-free late: {int(hl.sum()):,} lenses, median z {zm:.3f}, median log M* {mm:.2f}, share of the host-free outer weight {F['E4']['medians']['outer_weight_share']:.3f}")
    # E5 ------------------------------------------------------------------------------------------------------------
    cellid = typ * 6 + terc * 2 + (zl > np.median(zl)); rngm = np.random.default_rng(52); dd = []
    idx = [np.where(cellid == cid)[0] for cid in np.unique(cellid)]
    for _ in range(200):
        hp_ = HF.copy()
        for ii in idx: hp_[ii] = HF[ii][rngm.permutation(len(ii))]
        dd.append(amp(~hp_, L, OUTER)["A"] - amp(hp_, L, OUTER)["A"])
    dd = np.array(dd); dt = amp(~HF, L, OUTER)["A"] - amp(HF, L, OUTER)["A"]
    F["E5"] = dict(true=float(dt), perm_mean=float(dd.mean()), perm_std=float(dd.std()), z=float((dt - dd.mean()) / dd.std()), frac_ge=float((dd >= dt).mean()))
    P(f"E5 hosted - host-free: true {dt:+.3f}; 200 permutations within type x mass tercile x z half: mean {dd.mean():+.3f}, std {dd.std():.3f}; "
      f"true is {(dt - dd.mean()) / dd.std():+.2f} sigma above the composition level; permutations at or above the true value: {int((dd >= dt).sum())} of 200")
    RES["foot"][foot] = F
# E6 ----------------------------------------------------------------------------------------------------------------
H2 = DM[0.3]["H2"]; ex = (H2 - H2s) / NL
P("\nE6 more massive (>= 0.3 dex) pool objects per lens, lenses minus shuffled positions, by projected separation (rows, Mpc) and |dchi| (columns, Mpc)")
P("      d \\ |dchi|     0-10     10-115    115-230   230-500     (per-lens counts around the lenses in brackets)")
for i in range(len(DE) - 1):
    P(f"  {DE[i]:4.2f}-{min(DE[i + 1], 3.0):4.2f}   " + "  ".join(f"{ex[i, j]:+.4f}" for j in range(len(CE) - 1)) + "    [" + " ".join(f"{H2[i, j] / NL:.3f}" for j in range(len(CE) - 1)) + "]")
RES["E6"] = dict(d_edges=DE.tolist(), dchi_edges=CE.tolist(), excess_per_lens=ex.tolist(), count_per_lens=(H2 / NL).tolist(), shuffled_per_lens=(H2s / NL).tolist())
P(f"\nruntime {time.time() - T0:.0f} s")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "ko1_extra.json"), "w"), indent=1)
open(os.path.join(HERE, "ko1_extra.out"), "w").write("\n".join(OUT) + "\n")
