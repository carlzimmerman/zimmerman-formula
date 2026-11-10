#!/usr/bin/env python3
"""ONE1 row 2 (FROZEN_CRITERIA.md a967a38851; AMENDMENT_A1.md, numerics of the neighbour kernel only): KiDS host-free lenses (KO1), shape ratio R_s = A(outer 0-3) / A(inner 7-12) and the
per-bin outer profile, all / late / early, veto 1.0 / 1.3 / 1.6 R_h, against the counted-once halo (the law's own halo of each galaxy,
ending where nu = 1 + X), with every catalogued neighbour carrying the same share as its own truncated halo (exact annulus kernel,
shuffled positions subtracted) and the mass factor k fitted on the inner window (refitted in every jackknife sample).
Known answers KA2-KA7; MUTATE M1 (share x 0.1), M2 (share x 10, KiDS reading), M3 (neighbour positions shuffled).
    python3 one1_kids.py   -> one1_kids.json / one1_kids.out, one1_kids_MUTATE.json / one1_kids_MUTATE.out
Reads one1.json (the share X per footing, from PD1's share_table). Reads the shear sums WG (KO1's per-lens files) for the data side.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar"); KO1D = os.path.join(REPO, "fable52_push", "KO1_kids_outer_points")
CRIT = "a967a38851"; T0 = time.time(); OUT, OUTM = [], []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def PM(s=""): print("[MUTATE] " + s, flush=True); OUTM.append(str(s))
def tm(): return f"[{time.time() - T0:.0f} s]"
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt"); NPAT = 50; A0C = A0["canonical"]
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
ONE = json.load(open(os.path.join(HERE, "one1.json")))
XP = {f: float(ONE["foot"][f]["X"]) for f in FOOT}                      # PD1's Lagrangian share at z 0, per footing
P(f"ONE1 KiDS (criteria {CRIT}). Primary share X = {XP['canonical']:.4f} / {XP['alt']:.4f} M_b (canonical / alt), from one1.json (PD1 share_table).")

# =================================================================== 1. the halo's projection (own code: cosh substitution)
def dsig(u, X):
    """DeltaSigma of the halo, units M_b / r_M^2, at projected u = R / r_M; X = inf: no end. Baryons a central point."""
    xt = math.sqrt(X * (X + 1)) if np.isfinite(X) else np.inf; out = np.empty(len(u))
    for i, ui in enumerate(u):
        if ui >= xt: out[i] = (1 + X) / (math.pi * ui * ui); continue
        T = math.acosh(xt / ui) if np.isfinite(xt) else 45.0
        t = np.linspace(0.0, T, 6001); x = ui * np.cosh(t); dm = x / np.sqrt(0.25 + x * x)
        Sig = np.trapz(dm / np.cosh(t), t) / (2 * math.pi * ui)
        Mc = 0.5 + math.sqrt(0.25 + ui * ui) + ui * np.trapz(dm * np.tanh(t) * np.exp(-t), t)
        out[i] = Mc / (math.pi * ui * ui) - Sig
    return out
UG = np.geomspace(1e-2, 1e5, 900); LUG = np.log(UG); D_INF = dsig(UG, np.inf)
RHO = {}
def rho_tab(X):
    if X not in RHO: RHO[X] = dsig(UG, X) / D_INF
    return RHO[X]
P(f"projection: untruncated against the isothermal form 1 / (4 u) at u = 50, 300: {np.interp(np.log(50), LUG, D_INF) * 200:.4f}, {np.interp(np.log(300), LUG, D_INF) * 1200:.4f}  {tm()}")

# =================================================================== 2. the neighbour kernel H(rho, delta) (units of the neighbour's end radius r_t)
NW = 641; NTH = 96
_TH, _WTH = np.polynomial.legendre.leggauss(NTH); _TH = (_TH + 1) * math.pi / 2; _WTH = _WTH * math.pi / 2
def sigma_ph(X, n_log=2000, n_lin=6000):
    """phantom-only surface density of the unit-mass halo in units of r_t; cumulative projected mass M(s); normalised to unit mass."""
    xt = math.sqrt(X * (X + 1))
    s_rm = np.unique(np.concatenate([np.geomspace(1e-6 * xt, 0.05 * xt, n_log), np.linspace(0.05 * xt, xt, n_lin)]))
    Sg = np.empty(len(s_rm))
    for i, si in enumerate(s_rm):
        if si >= xt: Sg[i] = 0.0; continue
        T = math.acosh(xt / si); t = np.linspace(0.0, T, 1501); x = si * np.cosh(t)
        Sg[i] = np.trapz((x / np.sqrt(0.25 + x * x)) / np.cosh(t), t) / (2 * math.pi * si)
    s = np.concatenate([[0.0], s_rm / xt]); S = np.concatenate([[Sg[0]], Sg * xt * xt])
    dM = 2 * math.pi * s * S; Mc = np.concatenate([[0.0], np.cumsum(0.5 * (dM[1:] + dM[:-1]) * np.diff(s))]); tot = Mc[-1]
    return s, S / tot, Mc / tot, tot / X
def Qfun(rho, dl, s, S, Mc):
    """unit phantom mass inside a disc of radius rho centred dl from the halo's centre: exact inner part from the cumulative mass, the
    crossing band by Gauss-Legendre in theta (s = s_lo + (s_hi - s_lo)(1 - cos theta) / 2 removes the square-root ends)."""
    base = np.where(rho > dl, np.interp(np.minimum(rho - dl, 1.0), s, Mc), 0.0)
    slo = np.abs(rho - dl); shi = np.minimum(rho + dl, 1.0); act = slo < shi
    out = base.copy()
    if act.any():
        a, b = slo[act][:, None], shi[act][:, None]; ss = a + (b - a) * (1 - np.cos(_TH[None, :])) / 2; jac = (b - a) * np.sin(_TH[None, :]) / 2
        r_, d_ = rho[act][:, None], dl[act][:, None] if np.ndim(dl) else dl
        with np.errstate(divide="ignore", invalid="ignore"):
            cosa = (ss * ss + d_ * d_ - r_ * r_) / (2 * ss * d_)
        al = np.arccos(np.clip(cosa, -1.0, 1.0)); Si = np.interp(ss, s, S)
        out[act] += (al * 2 * ss * Si * jac * _WTH[None, :]).sum(1)
    return out
def build_H(X, nd=480):
    """H_ph(rho, delta) = 2 int_0^rho Q / rho' d rho' - Q(rho), tabulated on two half-bands per delta row: lower rho in [max(0, delta - 1), delta],
    upper rho in [delta, delta + 1]; the upper band is stored minus 2 ln(1 + rho) (smooth in ln delta)."""
    s, S, Mc, norm = sigma_ph(X); w = np.linspace(0.0, 1.0, NW); DG = np.geomspace(1e-4, 300.0, nd)
    HL = np.zeros((nd, NW)); HU = np.zeros((nd, NW)); CC = np.zeros(nd)
    for i, dl in enumerate(DG):
        lo = max(0.0, dl - 1.0); rl = lo + w * (dl - lo); ru = dl + w
        rho = np.concatenate([rl, ru[1:]]); q = Qfun(rho, np.full(rho.size, dl), s, S, Mc)
        with np.errstate(divide="ignore", invalid="ignore"):
            integ = np.where(rho > 0, q / rho, 0.0)
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(rho))])
        H = 2 * cum - q; HL[i] = H[:NW]; HU[i] = H[NW - 1:] - 2 * np.log1p(ru); CC[i] = H[-1] - 2 * math.log(dl + 1) + 1
    return dict(X=X, DG=DG, LD=np.log(DG), HL=HL, HU=HU, CC=CC, fb=1.0 / (1 + X), norm=norm)
def H_eval(rho, dl, T):
    """full H for the unit-mass halo (baryon point fb + phantom (1 - fb)); vectorised."""
    fb = T["fb"]; dl = np.maximum(dl, 1e-12)
    Hpm = np.where(rho > dl, 2 * np.log(np.maximum(rho, 1e-300) / dl) - 1.0, 0.0)
    ld = np.clip(np.log(dl), T["LD"][0], T["LD"][-1]); fi = (ld - T["LD"][0]) / (T["LD"][1] - T["LD"][0])
    i = np.clip(np.floor(fi).astype(np.int64), 0, len(T["DG"]) - 2); a = fi - i
    lo = np.maximum(0.0, dl - 1.0); above = rho >= dl + 1.0; below = rho <= lo; upper = (rho >= dl) & ~above
    with np.errstate(divide="ignore", invalid="ignore"):
        wl = np.clip(np.where(dl > lo, (rho - lo) / (dl - lo), 0.0), 0.0, 1.0)
    wu = np.clip(rho - dl, 0.0, 1.0)
    ww = np.where(upper, wu, wl) * (NW - 1); j = np.clip(np.floor(ww).astype(np.int64), 0, NW - 2); b = ww - j
    def row(ii):
        hl = (1 - b) * T["HL"][ii, j] + b * T["HL"][ii, j + 1]; hu = (1 - b) * T["HU"][ii, j] + b * T["HU"][ii, j + 1]
        return np.where(upper, hu, hl)
    hmid = (1 - a) * row(i) + a * row(i + 1) + np.where(upper, 2 * np.log1p(np.maximum(rho, 0.0)), 0.0)
    cc = (1 - a) * T["CC"][i] + a * T["CC"][i + 1]
    Hph = np.where(above, cc + 2 * np.log(np.maximum(rho, 1e-300)) - 1.0, np.where(below & (dl >= 1.0), 0.0, hmid))
    return fb * Hpm + (1 - fb) * Hph

# =================================================================== 3. lenses, data sums, catalogue, host-free sets
ln = np.load(os.path.join(DATA, "lr_lenses.npz")); PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WG, WW, EDGES = PL["WG"], PL["WW"], PL["gbar_edges"]; patch = np.load(os.path.join(DATA, "cfg96_stack.npz"))["patch"]
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
OUTER, INNER = [0, 1, 2, 3], [7, 8, 9, 10, 11, 12]; USED = OUTER + INNER; CO, CI = list(range(4)), list(range(4, 10)); R3 = (3.0 * Mpc) ** 2
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); bb = HB[1].data
HL_ = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL_[1].data
r_ = np.array(bb["MAG_AUTO_CALIB"], dtype="f8"); z_ = np.array(bb["zphot_ANNz2"], dtype="f8")
logM_ = np.array(Lp["MASS_MED"], dtype="f8") + 0.15; ra_ = np.array(bb["RAJ2000"], dtype="f8"); dec_ = np.array(bb["DECJ2000"], dtype="f8")
del bb, Lp; HB.close(); HL_.close()
inb = np.where((r_ < 20) & (z_ >= 0.02) & (z_ <= 0.8) & np.isfinite(logM_) & (logM_ > 7))[0]
xN = unitvec(ra_[inb], dec_[inb]); chiN = DC(z_[inb]); logMN = logM_[inb]; mN = mgal_of(logMN) * Msun
key = {(a, d): i for i, (a, d) in enumerate(zip(ra_[inb], dec_[inb]))}
selfN = np.array([key[(a, d)] for a, d in zip(ln["ra"], ln["dec"])]); treeN = cKDTree(xN); xL = xN[selfN]
del r_, z_, logM_, ra_, dec_, key
RH = np.minimum(3.0, np.sqrt(G * mgal_of(logMs) * Msun / 1e-15) / Mpc)
def hostfree(fac, tie=0.0, dm=0.3, W=230.0, CH=300):
    chord = 2 * np.sin(fac * RH * (1 + zl) / chil / 2); dmin = np.full(NL, np.inf)
    for i0 in range(0, NL, CH):
        i1 = min(i0 + CH, NL); lists = treeN.query_ball_point(xL[i0:i1], r=chord[i0:i1])
        c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(c.sum())
        if tot == 0: continue
        li = i0 + np.repeat(np.arange(len(c)), c); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot)
        keep = (j != selfN[li]) & (logMN[j] >= logMs[li] + dm - tie); li, j = li[keep], j[keep]
        np.minimum.at(dmin, li, np.abs(chiN[j] - chil[li]))
    return dmin >= W
FS = (1.0, 1.3, 1.6); HF = {}; HFT = {}
for F in FS:
    HF[F] = hostfree(F); HFT[F] = hostfree(F, tie=1e-9)
P("host-free lenses, KO1 tie rule: " + ", ".join(f"{F} R_h {int(HF[F].sum()):,}" for F in FS) + " (KO1 40,667, 25,708, 17,335); KO1R tie rule: "
  + ", ".join(f"{int(HFT[F].sum()):,}" for F in FS) + f"  {tm()}")
assert all(np.all(HFT[F] <= HF[F]) and np.all(HF[F] <= HF[1.0]) for F in FS)
idx1 = np.where(HF[1.0])[0]; n1 = len(idx1)
WG1, WW1, P1 = WG[idx1][:, USED], WW[idx1][:, USED], patch[idx1]; Mg1 = Mg[idx1]; typ1 = typ[idx1]
TLO1 = np.stack([G * Mg1 / EDGES[b + 1] for b in USED], 1); THI1 = np.stack([np.minimum(G * Mg1 / EDGES[b], R3) for b in USED], 1); OKC1 = THI1 > TLO1
XG, WGL = np.polynomial.legendre.leggauss(24)
GB1 = G * Mg1[:, None, None] / (TLO1[:, :, None] + (THI1 - TLO1)[:, :, None] * (XG[None, None, :] + 1) / 2)        # g_bar at the nodes (catalogued mass)
MASKS = {}
for F in FS:
    for tie, H_ in (("KO1", HF), ("KO1R", HFT)):
        m = H_[F][idx1]
        MASKS[(tie, F, "all")] = m; MASKS[(tie, F, "late")] = m & (typ1 == 0); MASKS[(tie, F, "early")] = m & (typ1 == 1)
def psum(arr, mask):
    pm = P1[mask]; a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, c], minlength=NPAT) for c in range(arr.shape[1])], axis=1)
def cells(a0, k=1.0, X=np.inf):
    g = k * GB1; f = glaw(g, a0)
    if np.isfinite(X):
        u = np.sqrt(a0 / g); f = f * np.interp(np.log(u), LUG, rho_tab(X))
    return np.where(OKC1, (f * WGL[None, None, :]).sum(-1) / 2, 0.0)
LAW = {f: cells(A0[f]) for f in FOOT}
SD = {mk: dict(Sg=psum(WG1, m), Sw=psum(WW1, m), Sm={f: psum(WW1 * LAW[f], m) for f in FOOT}) for mk, m in MASKS.items()}
P(f"data sums ready for {len(MASKS)} lens sets  {tm()}")

# =================================================================== 4. estimator (KO1's, unchanged)
def base(mk, f):
    d = SD[mk]; tg, tw, tm_ = d["Sg"].sum(0), d["Sw"].sum(0), d["Sm"][f].sum(0)
    Dl = 4 * G * (tg - d["Sg"]) / (tw - d["Sw"]); sk = np.sqrt((NPAT - 1) / NPAT * ((Dl - Dl.mean(0)) ** 2).sum(0))
    M = tm_ / tw; Ml = (tm_ - d["Sm"][f]) / (tw - d["Sw"]); return tw, sk, M, Ml
BASE = {(mk, f): base(mk, f) for mk in MASKS for f in FOOT}
def amps(mk, f, Snum, data=False):
    """A(outer), A(inner), per-bin ratio N_k / M_k (outer), each full and per jackknife sample. Snum: patch sums of the numerator (WW x model or WG)."""
    tw, sk, M, Ml = BASE[(mk, f)]; d = SD[mk]; t = Snum.sum(0)
    fac = 4 * G if data else 1.0
    N = fac * t / tw; Nl = fac * (t - Snum) / (tw - d["Sw"]); w2 = 1 / sk ** 2
    def A(Nx, Mx, cols): return (Nx[..., cols] * Mx[..., cols] * w2[cols]).sum(-1) / (Mx[..., cols] ** 2 * w2[cols]).sum(-1)
    return dict(out=A(N, M, CO), in_=A(N, M, CI), out_l=A(Nl, Ml, CO), in_l=A(Nl, Ml, CI), per=N[CO] / M[CO], per_l=Nl[:, CO] / Ml[:, CO])
DAT = {(mk, f): amps(mk, f, SD[mk]["Sg"], data=True) for mk in MASKS for f in FOOT}
def jk(x): x = np.asarray(x); return float(np.sqrt((NPAT - 1) / NPAT * ((x - x.mean(0)) ** 2).sum(0))) if x.ndim == 1 else np.sqrt((NPAT - 1) / NPAT * ((x - x.mean(0)) ** 2).sum(0))

# KA6 data side against KO1 E7
SH = json.load(open(os.path.join(KO1D, "ko1_shape.json")))["foot"]; KA = {}
for f in FOOT:
    for F in FS:
        e = SH[f]["E7"][f"{F:.1f}"]; d = DAT[(("KO1", F, "all"), f)]; Rs = d["out"] / d["in_"]; sRs = jk(d["out_l"] / d["in_l"])
        vals = [(Rs, e["Rs"][0]), (sRs, e["Rs"][1]), (d["in_"], e["inner"][0]), (d["out"], e["outer"][0])] + list(zip(d["per"], e["per_bin"]))
        mx = max(abs(a - b) / abs(b) for a, b in vals); n_ok = int(MASKS[("KO1", F, "all")].sum()) == e["n"]
        KA[f"KA6 {f} {F}"] = dict(max_rel=mx, n_ok=n_ok, ok=bool(mx <= 1e-6 and n_ok))
P("KA6 data side vs KO1 E7 (R_s, its error, inner, outer, 4 bins; counts): " + ", ".join(f"{k[4:]} {v['max_rel']:.1e}" for k, v in KA.items()) + " -> "
  + ("PASS" if all(v["ok"] for v in KA.values()) else "FAIL"))

# =================================================================== 5. lens-own model on a k grid, k fits
KGRID = np.geomspace(0.25, 60.0, 46); LKG = np.log(KGRID)
OSC = {}
def own_sums(f, X):
    """patch sums of WW x lens-own model cells, for every mask, on the k grid: dict mk -> array (nk, 50, 10). Cached."""
    if (f, X) in OSC: return OSC[(f, X)]
    out = {mk: np.zeros((len(KGRID), NPAT, 10)) for mk in MASKS}; OSC[(f, X)] = out
    for ik, k in enumerate(KGRID):
        C = WW1 * cells(A0[f], k, X)
        for mk, m in MASKS.items(): out[mk][ik] = psum(C, m)
    return out
def fit(mk, f, S_of_k, kvalid=None):
    """S_of_k: (nk, 50, 10) model patch sums on KGRID. k from the inner window (full and per jackknife); model R_s, per-bin profile."""
    d = DAT[(mk, f)]; ain = np.zeros(len(KGRID)); aout = np.zeros(len(KGRID)); ainl = np.zeros((len(KGRID), NPAT)); aoutl = np.zeros((len(KGRID), NPAT))
    per = np.zeros((len(KGRID), 4)); perl = np.zeros((len(KGRID), NPAT, 4))
    for ik in range(len(KGRID)):
        if kvalid is not None and not kvalid[ik]: ain[ik] = np.nan; continue
        a = amps(mk, f, S_of_k[ik]); ain[ik], aout[ik], ainl[ik], aoutl[ik], per[ik], perl[ik] = a["in_"], a["out"], a["in_l"], a["out_l"], a["per"], a["per_l"]
    ok = np.isfinite(ain); L = LKG[ok]
    def solve(target, curve):
        c = curve[ok]
        hit = np.where((c[:-1] - target) * (c[1:] - target) <= 0)[0]                      # first crossing (the curve rises with k)
        if len(hit) == 0: return np.nan
        i = int(hit[0]); return float(L[i] + (target - c[i]) * (L[i + 1] - L[i]) / (c[i + 1] - c[i])) if c[i + 1] != c[i] else float(L[i])
    lk = solve(d["in_"], ain); lkl = np.array([solve(d["in_l"][l], ainl[:, l]) for l in range(NPAT)])
    if not (np.isfinite(lk) and np.all(np.isfinite(lkl))): return None
    def at(curve, lkx): return float(np.interp(lkx, L, curve[ok]))
    mo = at(aout, lk); mi = at(ain, lk); mol = np.array([at(aoutl[:, l], lkl[l]) for l in range(NPAT)]); mil = np.array([at(ainl[:, l], lkl[l]) for l in range(NPAT)])
    pm = np.array([at(per[:, c], lk) for c in range(4)]) / mi; pml = np.array([[at(perl[:, l, c], lkl[l]) for c in range(4)] for l in range(NPAT)]) / mil[:, None]
    Rd = d["out"] / d["in_"]; Rdl = d["out_l"] / d["in_l"]; Rm = mo / mi; Rml = mol / mil
    pdd = d["per"] / d["in_"]; pdl = d["per_l"] / d["in_l"][:, None]
    D = pdd - pm; Dl = pdl - pml; C = (NPAT - 1) / NPAT * ((Dl - Dl.mean(0)).T @ (Dl - Dl.mean(0))); chi2 = float(D @ np.linalg.solve(C, D)) * (NPAT - 4 - 2) / (NPAT - 1)
    return dict(k=float(math.exp(lk)), k_l=np.exp(lkl), Rs_data=Rd, s_data=jk(Rdl), Rs_model=Rm, diff=Rd - Rm, s_diff=jk(Rdl - Rml), diff_l=Rdl - Rml,
                z=(Rd - Rm) / jk(Rdl - Rml), z_data_only=(Rd - Rm) / jk(Rdl), p_data=pdd, p_model=pm, p_err=np.sqrt(np.diag(C)), chi2=chi2,
                A_in_data=d["in_"], A_out_data=d["out"], A_out_model=mo)

# =================================================================== 6. neighbours: tiered pair search, exact kernel on a lambda grid
TIERS = [(7.0, 9.5), (9.5, 10.3), (10.3, 10.8), (10.8, 11.2), (11.2, 11.6), (11.6, 14.0)]
TREES = []
for lo, hi in TIERS:
    ii = np.where((logMN >= lo) & (logMN < hi))[0]; TREES.append((ii, cKDTree(xN[ii]) if len(ii) else None))
z1, chil1, RH1 = zl[idx1], chil[idx1], RH[idx1] * Mpc; DAl1 = chil1 / (1 + z1) * Mpc
R1e, R2e = np.sqrt(TLO1), np.sqrt(THI1)
def scan(Lx, Lself, X, lams, Htab, mode="ext", CH=400):
    """per-unit-k neighbour term (n1, 10) for each lambda: 4 G <DeltaSigma_t> over each cell, from every pool object j != Lself with
    |chi_j - chi_l| < 230 Mpc and d < R_h + r_t,j (ext) or d < R_h (point, E8's set). Neighbour j: total (1 + X) M_b,j (times k outside),
    end radius r_t = lambda x_t sqrt(G M_b,j / a0_canonical)."""
    xt = math.sqrt(X * (X + 1)) if np.isfinite(X) else 0.0; out = np.zeros((len(lams), n1, 10)); npair = 0; lmax = max(lams)
    rt0 = xt * np.sqrt(G * mN / A0C)
    for (ii, tree) in TREES:
        if tree is None: continue
        rext = (lmax * rt0[ii].max()) if mode == "ext" else 0.0
        for i0 in range(0, n1, CH):
            i1 = min(i0 + CH, n1); th = (RH1[i0:i1] + rext) / DAl1[i0:i1]
            lists = tree.query_ball_point(Lx[i0:i1], r=2 * np.sin(np.minimum(th, math.pi) / 2))
            c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(c.sum())
            if tot == 0: continue
            li = i0 + np.repeat(np.arange(len(c)), c); j = ii[np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot)]
            keep = (j != Lself[li]) & (np.abs(chiN[j] - chil1[li]) < 230.0); li, j = li[keep], j[keep]
            d = 2 * np.arcsin(np.minimum(np.linalg.norm(xN[j] - Lx[li], axis=1) / 2, 1.0)) * DAl1[li]
            keep = d < (RH1[li] + lmax * rt0[j]) if mode == "ext" else d < RH1[li]
            li, j, d = li[keep], j[keep], d[keep]; npair += len(j)
            if len(j) == 0: continue
            pref = 4 * G * (1 + X) * mN[j] / math.pi
            for il, lam in enumerate(lams):
                rt = lam * rt0[j] if mode == "ext" else None
                for cb in range(10):
                    r1, r2, okc = R1e[li, cb], R2e[li, cb], OKC1[li, cb]
                    if mode == "point":
                        dd = np.maximum(d, 1e-300)
                        K = np.where(dd < r1, 2 * np.log(r2 / r1), np.where(dd < r2, 2 * np.log(r2 / dd) - 1.0, 0.0))
                    else:
                        K = np.zeros(len(j)); act = okc & (d < r2 + rt)
                        if not act.any(): continue
                        a_ = np.where(act)[0]; rta = rt[a_]; dl = d[a_] / rta
                        inside = r1[a_] > d[a_] + rta                                  # wholly inside both circles: point-like
                        K[a_[inside]] = 2 * np.log(r2[a_[inside]] / r1[a_[inside]])
                        g_ = a_[~inside]
                        if len(g_): K[g_] = H_eval(r2[g_] / rt[g_], d[g_] / rt[g_], Htab) - H_eval(r1[g_] / rt[g_], d[g_] / rt[g_], Htab)
                    val = np.where(okc, pref * K / (r2 ** 2 - r1 ** 2), 0.0)
                    out[il, :, cb] += np.bincount(li, weights=val, minlength=n1)
    return out, npair
rngS = np.random.default_rng(52); PERMS = [rngS.permutation(n1) for _ in range(5)]
XL1, SELF1 = xL[idx1], selfN[idx1]
def neighbours(X, lams, Htab, mode="ext"):
    t0 = time.time(); Tr, npr = scan(XL1, SELF1, X, lams, Htab, mode); P(f"   neighbour scan X {X:.3f} ({mode}, {len(lams)} lambda): real positions {npr:,} pairs, {time.time() - t0:.0f} s")
    S0 = None; Ssum = np.zeros_like(Tr)
    for ip, p in enumerate(PERMS):
        t_, _ = scan(XL1[p], SELF1[p], X, lams, Htab, mode); Ssum += t_
        if ip == 0: S0 = t_.copy()
    P(f"   shuffles done, {time.time() - t0:.0f} s")
    return Tr, (S0, (Ssum - S0) / (len(PERMS) - 1), Ssum / len(PERMS)), npr

# =================================================================== 7. known answers on the kernel and the projection
P("\nKnown answers (kernel, projection)")
x53 = 53.64; xt53 = math.sqrt(x53 * (x53 + 1)); r53 = rho_tab(x53)
far = float(np.interp(np.log(2000.0), LUG, r53)); want = 4 * (1 + x53) / (math.pi * 2000.0)
KA["KA4 far field ratio at u 2000 (X 53.64)"] = dict(value=far, ref=want, ok=bool(abs(far / want - 1) <= 1e-3))
cont = float(dsig(np.array([xt53 * (1 - 1e-9)]), x53)[0] * math.pi * xt53 ** 2 / (1 + x53))
KA["KA4 continuity at x_t: DeltaSigma pi u^2 / (1 + X)"] = dict(value=cont, ref=1.0, ok=bool(abs(cont - 1) <= 1e-3))
ub = np.geomspace(xt53, 10 * xt53, 7); pm_ = dsig(ub, x53) * math.pi * ub ** 2 / (1 + x53)
KA["KA4 point mass beyond x_t"] = dict(value=float(np.max(np.abs(pm_ - 1))), ref=0.0, ok=bool(np.max(np.abs(pm_ - 1)) <= 1e-4))
r8 = rho_tab(1e8); sel = (UG >= 0.3) & (UG <= 2000); dev = float(np.max(np.abs(r8[sel] - 1)))
KA["KA3 untruncated returns the law (X 1e8, u 0.3-2000)"] = dict(value=dev, ref=0.0, ok=bool(dev <= 1e-3))
P(f"KA4 far field: ratio at u = 2000 {far:.6f} vs 4 (1 + X) / (pi u) {want:.6f}; continuity at x_t {cont:.6f}; point mass beyond x_t max |dev| {np.max(np.abs(pm_ - 1)):.1e}")
P(f"KA3 untruncated (X = 1e8): max |rho - 1| on u 0.3-2000 = {dev:.1e}")
# lead's dsig at a few points (his code, reproduced here for the comparison only)
def dsig_lead(u, xt):
    out = np.zeros_like(u); XMAX = 3e5 if not np.isfinite(xt) else xt
    for i, ui in enumerate(u):
        if ui >= XMAX: out[i] = (0.5 + np.sqrt(0.25 + XMAX ** 2)) / (np.pi * ui ** 2); continue
        x = np.geomspace(ui, XMAX, 6000); dm = x / np.sqrt(0.25 + x * x); m_u = 0.5 + np.sqrt(0.25 + ui * ui)
        M2 = m_u + np.trapz((1 - np.sqrt(np.clip(1 - (ui / x) ** 2, 0, 1))) * dm, x)
        T = np.arccosh(XMAX / ui); t = np.linspace(0, T, 6000); xx = ui * np.cosh(t); rho = (xx / np.sqrt(0.25 + xx * xx)) / (4 * np.pi * xx * xx)
        out[i] = M2 / (np.pi * ui ** 2) - 2 * np.trapz(rho * xx, t)
    return out
uc = np.array([1.0, 5.0, 20.0, 50.0, 59.0, 100.0, 500.0]); X59 = XP["canonical"]
mine = dsig(uc, X59) / dsig(uc, np.inf); lead = dsig_lead(uc, math.sqrt(X59 * (X59 + 1))) / dsig_lead(uc, np.inf)
KA["KA2a projection ratio vs the lead's dsig"] = dict(value=float(np.max(np.abs(mine - lead))), ref=0.0, ok=bool(np.max(np.abs(mine - lead)) <= 2e-3))
P(f"KA2a my projection ratio vs the lead's dsig at u {uc.tolist()}: max |diff| {np.max(np.abs(mine - lead)):.1e} (mine {np.round(mine, 4).tolist()})")
HT = {}
def Htab_of(X):
    if X not in HT: HT[X] = build_H(X)
    return HT[X]
Tp = Htab_of(X59); P(f"kernel table X {X59:.3f}: phantom grid normalisation {Tp['norm']:.6f} (1 = exact)  {tm()}")
# KA7 (i): continuity at the band edges against the analytic branches
dl_ = np.geomspace(1e-3, 200, 400); e1 = H_eval(dl_ + 1 - 1e-9, dl_, Tp) - H_eval(dl_ + 1 + 1e-9, dl_, Tp)
big = dl_ > 1.0; e2 = H_eval(dl_[big] - 1 + 1e-9, dl_[big], Tp) - 0.0
e3 = np.abs(H_eval(dl_ + 1.5, dl_, Tp) - H_eval(dl_ + 1.2, dl_, Tp) - 2 * np.log((dl_ + 1.5) / (dl_ + 1.2)))
k7i = float(max(np.max(np.abs(e1)), np.max(np.abs(e2)), np.max(e3)))
KA["KA7i kernel = point-mass kernel where the halo is wholly inside / outside"] = dict(value=k7i, ref=0.0, ok=bool(k7i <= 1e-4))
P(f"KA7(i) band-edge continuity and point-like differences: max |dev| {k7i:.1e}")
# KA7 (ii): centred kernel against the direct projection (annulus averages)
pairs = [(0.05, 0.088), (0.2, 0.35), (0.5, 0.88), (0.8, 1.4), (1.2, 2.1)]; dev2 = 0.0; xt59 = math.sqrt(X59 * (X59 + 1))
for a, b_ in pairs:
    hk = (1 + X59) * (H_eval(np.array([b_]), np.array([1e-4]), Tp) - H_eval(np.array([a]), np.array([1e-4]), Tp))[0] / (math.pi * (b_ ** 2 - a ** 2))     # units (M_b)/r_t^2
    uu = np.linspace(a * xt59, b_ * xt59, 801); ds = dsig(uu, X59); direct = np.trapz(ds * 2 * uu, uu) / ((b_ * xt59) ** 2 - (a * xt59) ** 2) * xt59 ** 2
    dev2 = max(dev2, abs(hk / direct - 1))
KA["KA7ii centred kernel vs direct projection"] = dict(value=dev2, ref=0.0, ok=bool(dev2 <= 1e-3))
P(f"KA7(ii) centred kernel vs the direct projection, annulus averages: max rel dev {dev2:.1e}")
# KA7 (iii): uniformly scattered halos give zero net annulus shear
rng = np.random.default_rng(52); Dd = 6.0; r1u, r2u = 2.0, 3.4; dd_ = Dd * np.sqrt(rng.uniform(0, 1, 2_000_000))
Kc = H_eval(np.full(dd_.size, r2u), dd_, Tp) - H_eval(np.full(dd_.size, r1u), dd_, Tp)
ka3 = float(Kc.mean() / (2 * math.log(r2u / r1u) * (r1u / Dd) ** 2))
KA["KA7iii uniform halos give zero net shear"] = dict(value=ka3, ref=0.0, ok=bool(abs(ka3) < 0.02))
P(f"KA7(iii) uniform halos: mean kernel / its inner part = {ka3:+.4f} (|.| < 0.02)  {tm()}")

# KA7 (iv): E8 reproduced (point masses, X 5.562, k 1, E8's pairs and shuffles)
X_SH = 0.11958060485606123 / 0.0215
Tr, Ts, npr = neighbours(X_SH, [1.0], None, mode="point")
net = Tr[0] - Ts[2][0]
for f, ref in (("canonical", 0.00181), ("alt", 0.00165)):
    mk = ("KO1", 1.0, "all"); tw, sk, M, Ml = BASE[(mk, f)]; Sn = psum(WW1 * net / (1 + X_SH), MASKS[mk]); t = Sn.sum(0); N = t / tw
    a = float((N[CO] * M[CO] / sk[CO] ** 2).sum() / (M[CO] ** 2 / sk[CO] ** 2).sum())
    KA[f"KA7iv E8 a_nb {f}"] = dict(value=a, ref=ref, pairs=npr, ok=bool(abs(a / ref - 1) <= 0.02 + 0.5e-5 / ref))
    P(f"KA7(iv) E8 point-mass net term per unit (1 + X), {f}: {a:.5f} vs E8 {ref} ({npr:,} pairs; E8 1,001,712)")
NB_POINT = net / (1 + X_SH)                                                       # per unit (1 + X), k = 1, point masses inside R_h
P(f"{tm()}")

# =================================================================== 8. the grid of readings
def graded_set(X, lams, Htab, foots=FOOT, with_nb=True, k1=False):
    """for share X: lens-own sums on KGRID per footing; neighbour sums on the lambda grid; fits for every mask."""
    res = {}
    NB = None
    if with_nb:
        Tr, Ts, npr = neighbours(X, lams, Htab); NB = dict(real=Tr, shuf0=Ts[0], shuf_rest=Ts[1], net=Tr - Ts[2], pairs=npr)
    for f in foots:
        OS = own_sums(f, X); res[f] = {}
        lam_of_k = np.sqrt(KGRID * A0C / A0[f])
        if NB is not None:
            kval = (lam_of_k >= min(lams)) & (lam_of_k <= max(lams))
            NBS = {mk: np.stack([psum(WW1 * NB["net"][il], m) for il in range(len(lams))]) for mk, m in MASKS.items()}
        for mk in MASKS:
            S_own = OS[mk]
            if NB is not None:
                cs = CubicSpline(np.log(lams), NBS[mk], axis=0)
                S_nb = np.stack([KGRID[ik] * cs(math.log(min(max(lam_of_k[ik], min(lams)), max(lams)))) for ik in range(len(KGRID))])
                r_nb = fit(mk, f, S_own + S_nb, kvalid=kval)
            else: r_nb = None
            r_no = fit(mk, f, S_own)
            res[f][mk] = dict(no_nb=r_no, nb=r_nb)
    return res, NB
def k1_reading(X, f, mk, NB=None, lams=None):
    """the bracket k = 1 (catalogued masses): model R_s with / without neighbours, data error only and difference error."""
    C = cells(A0[f], 1.0, X); m = MASKS[mk]; S = psum(WW1 * C, m); a = amps(mk, f, S); d = DAT[(mk, f)]
    out = dict(Rs_model=a["out"] / a["in_"], Rs_data=d["out"] / d["in_"], s_data=jk(d["out_l"] / d["in_l"]))
    out["z"] = (out["Rs_data"] - out["Rs_model"]) / out["s_data"]
    if NB is not None:
        lam = math.sqrt(A0C / A0[f]); cs = CubicSpline(np.log(lams), np.stack([psum(WW1 * NB["net"][il], m) for il in range(len(lams))]), axis=0)
        a2 = amps(mk, f, S + cs(math.log(lam))); out["Rs_model_nb"] = a2["out"] / a2["in_"]; out["z_nb"] = (out["Rs_data"] - out["Rs_model_nb"]) / out["s_data"]
    return out

# KA2: the lead's pre-freeze table (k = 1, no neighbours, his estimator: weighted outer, plain mean inner)
P("\nKA2 the lead's pre-freeze table (k = 1, no neighbours), canonical / alt")
LEADREF = {("canonical", 1.0): {53.64: 0.460, 59.5: 0.510, 80.0: 0.685}, ("canonical", 1.3): {53.64: 0.464, 59.5: 0.515, 80.0: 0.691}, ("canonical", 1.6): {53.64: 0.473, 59.5: 0.525, 80.0: 0.704},
           ("alt", 1.0): {53.64: 0.417, 59.5: 0.464, 80.0: 0.623}, ("alt", 1.3): {53.64: 0.421, 59.5: 0.468, 80.0: 0.629}, ("alt", 1.6): {53.64: 0.429, 59.5: 0.477, 80.0: 0.641}}
LATEREF = {("canonical", 1.0): (0.512, 0.513), ("canonical", 1.3): (0.517, 0.517), ("canonical", 1.6): (0.527, 0.527), ("alt", 1.0): (0.466, 0.466), ("alt", 1.3): (0.470, 0.471), ("alt", 1.6): (0.480, 0.480)}
k2dev = 0.0
for f in FOOT:
    for F in FS:
        e = SH[f]["E7"][f"{F:.1f}"]; w = 1 / np.array(e["per_bin_err"]) ** 2; row = []
        for X in (53.64, 59.5, 80.0, np.inf):
            C = cells(A0[f], 1.0, X)
            def lead_ratio(m):
                tw = WW1[m].sum(0); al = (WW1[m] * LAW[f][m]).sum(0); am = (WW1[m] * C[m]).sum(0); a = am / al
                return float((a[CO] * w).sum() / w.sum()) / float(a[CI].mean())
            rs = lead_ratio(MASKS[("KO1", F, "all")]); ref = 1.0 if not np.isfinite(X) else LEADREF[(f, F)][X]; k2dev = max(k2dev, abs(rs - ref)); row.append(f"X {X}: {rs:.3f} (lead {ref})")
            if X == 59.5:
                for sub, rr in zip(("late", "early"), LATEREF[(f, F)]):
                    v = lead_ratio(MASKS[("KO1", F, sub)]); k2dev = max(k2dev, abs(v - rr)); row.append(f"{sub} {v:.3f} (lead {rr})")
        P(f"  {f} {F} R_h: " + "; ".join(row))
KA["KA2 lead's table to 0.01"] = dict(value=k2dev, ref=0.0, ok=bool(k2dev <= 0.01))
P(f"KA2 max |diff| {k2dev:.4f} (line 0.01) -> {'PASS' if k2dev <= 0.01 else 'FAIL'}  {tm()}")

# lambda grid from lens-own fits (no neighbours) for the primary and brackets
def lam_grid(X, extra=()):
    lam = list(extra)
    for f in FOOT:
        OS = own_sums(f, X)
        for mk in MASKS:
            r = fit(mk, f, OS[mk])
            if r is not None: lam += [math.sqrt(r["k"] * A0C / A0[f]) * s for s in (np.min(r["k_l"]) / r["k"], np.max(r["k_l"]) / r["k"], 1.0)]
    lo, hi = 0.85 * min(lam), 1.15 * max(lam); return list(np.geomspace(lo, hi, 7))
RES = dict(lane="ONE1", row="2 KiDS", criteria=CRIT, X_primary=XP, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed", readings={}, KA=KA)
MUT = dict(lane="ONE1", row="2 KiDS", criteria=CRIT, readings={})
def summarize(lbl, res, foots, store, printer=P, X=None):
    for f in foots:
        printer(f"--- {lbl}, {f}")
        for tie in ("KO1", "KO1R"):
            for F in FS:
                line = []
                for sub in ("all", "late", "early"):
                    r = res[f][(tie, F, sub)]; key_ = f"{f}|{tie}|{F}|{sub}"; store[key_] = {}
                    for which in ("nb", "no_nb"):
                        q = r[which]
                        if q is None: continue
                        store[key_][which] = {kk: (vv.tolist() if isinstance(vv, np.ndarray) else vv) for kk, vv in q.items() if kk not in ("diff_l", "k_l")}
                        store[key_][which]["k_range_jk"] = [float(np.min(q["k_l"])), float(np.max(q["k_l"]))]
                    q = r["nb"] if r["nb"] is not None else r["no_nb"]; q0 = r["no_nb"]
                    line.append(f"{sub}: data {q['Rs_data']:.3f}+-{q['s_data']:.3f} model {q['Rs_model']:.3f} (no nb {q0['Rs_model']:.3f}) k {q['k']:.2f} z {q['z']:+.2f}"
                                + (f" chi2 {q['chi2']:.1f}" if sub == "all" else ""))
                if tie == "KO1" or F == 1.6: printer(f"  {tie} {F} R_h | " + " | ".join(line))

# ---------------- primary
P(f"\n=== PRIMARY: X = PD1's share, k fitted on the inner window, neighbours carrying the same share  {tm()}")
PRIM = {}
for f in FOOT:
    X = XP[f]; lams = lam_grid(X, extra=[1.0, math.sqrt(A0C / A0["alt"])]); P(f"[{f}] X {X:.4f}: lambda grid {np.round(lams, 3).tolist()}  {tm()}")
    res, NB = graded_set(X, lams, Htab_of(X), foots=(f,)); PRIM[f] = (res, NB, lams)
    P(f"[{f}] neighbour pairs (real positions): {NB['pairs']:,}  {tm()}")
    store = RES["readings"].setdefault("primary", {}); summarize("primary", res, (f,), store)
# gate
GATE = {}
for f in FOOT:
    res = PRIM[f][0]; g = {}
    for sub in ("all", "late", "early"):
        q = res[f][("KO1", 1.6, sub)]["nb"]; g[f"G-K1 {sub}"] = dict(diff=q["diff"], sigma=q["s_diff"], z=q["z"], ok=bool(abs(q["diff"]) <= 2 * q["s_diff"]))
    qa = res[f][("KO1", 1.6, "all")]["nb"]; g["G-K2 all profile"] = dict(chi2=qa["chi2"], line=9.49, ok=bool(qa["chi2"] <= 9.49))
    qe, ql = res[f][("KO1", 1.6, "early")]["nb"], res[f][("KO1", 1.6, "late")]["nb"]
    dd = qe["diff"] - ql["diff"]; sd = jk(qe["diff_l"] - ql["diff_l"]); g["G-K3 type difference"] = dict(data=qe["Rs_data"] - ql["Rs_data"], model=qe["Rs_model"] - ql["Rs_model"], diff=dd, sigma=sd, z=dd / sd, ok=bool(abs(dd) <= 2 * sd))
    st = "PASS" if all(v["ok"] for v in g.values()) else "FAIL"; GATE[f] = dict(lines=g, status=st, failing=[k for k, v in g.items() if not v["ok"]])
    P(f"[{f}] ROW 2 KiDS gate at 1.6 R_h: " + "; ".join(f"{k} " + (f"z {v['z']:+.2f}" if "z" in v else f"chi2 {v['chi2']:.2f}") + (" ok" if v["ok"] else " FAIL") for k, v in g.items()) + f" -> {st}")
RES["gate"] = GATE
# reported at 1.0 / 1.3 (type difference) and the neighbour term
for f in FOOT:
    res = PRIM[f][0]
    for F in (1.0, 1.3):
        qe, ql = res[f][("KO1", F, "early")]["nb"], res[f][("KO1", F, "late")]["nb"]
        dd = qe["diff"] - ql["diff"]; sd = jk(qe["diff_l"] - ql["diff_l"]); RES.setdefault("type_difference_reported", {})[f"{f}|{F}"] = dict(diff=dd, sigma=sd, z=dd / sd)
        P(f"[{f}] reported {F} R_h type difference (early - late), data minus model: {dd:+.3f} +- {sd:.3f} ({dd / sd:+.2f} sigma)")
# the neighbours' term: point masses (E8 pairs, lead's hand scaling) against extended halos
for f in FOOT:
    res, NB, lams = PRIM[f]; X = XP[f]
    for F in (1.0, 1.6):
        mk = ("KO1", F, "all"); m = MASKS[mk]; C1 = cells(A0[f], 1.0, X); S1 = psum(WW1 * C1, m); a1 = amps(mk, f, S1)
        Sp = psum(WW1 * NB_POINT * (1 + X), m); ap = amps(mk, f, S1 + Sp); lam = math.sqrt(A0C / A0[f])
        cs = CubicSpline(np.log(lams), np.stack([psum(WW1 * NB["net"][il], m) for il in range(len(lams))]), axis=0); ae = amps(mk, f, S1 + cs(math.log(lam)))
        q = res[f][mk]
        RES.setdefault("neighbour_term", {})[f"{f}|{F}"] = dict(k1_point=ap["out"] / ap["in_"] - a1["out"] / a1["in_"], k1_extended=ae["out"] / ae["in_"] - a1["out"] / a1["in_"],
                                                                 fitted_k_extended=q["nb"]["Rs_model"] - q["no_nb"]["Rs_model"], k=q["nb"]["k"])
        v = RES["neighbour_term"][f"{f}|{F}"]
        P(f"[{f}] neighbours' term in R_s, {F} R_h, all: k = 1 point masses (the lead's 'about 0.1') {v['k1_point']:+.3f}; k = 1 extended {v['k1_extended']:+.3f}; fitted k {v['k']:.2f} extended {v['fitted_k_extended']:+.3f}")
# k = 1 bracket (the lead's convention), with and without neighbours
for f in FOOT:
    res, NB, lams = PRIM[f]
    for F in FS:
        row = []
        for sub in ("all", "late", "early"):
            r = k1_reading(XP[f], f, ("KO1", F, sub), NB, lams); RES.setdefault("bracket_k1", {})[f"{f}|{F}|{sub}"] = r
            row.append(f"{sub} model {r['Rs_model']:.3f} / with nb {r['Rs_model_nb']:.3f} vs {r['Rs_data']:.3f}+-{r['s_data']:.3f} (z {r['z_nb']:+.2f})")
        P(f"[{f}] bracket k = 1, {F} R_h: " + "; ".join(row))
# the law as the lens's own field, no end, no neighbours (k fitted): the floor
for f in FOOT:
    OS = own_sums(f, np.inf)
    for F in FS:
        r = fit(("KO1", F, "all"), f, OS[("KO1", F, "all")]); RES.setdefault("law_no_end", {})[f"{f}|{F}"] = dict(Rs_model=r["Rs_model"], z=r["z"], k=r["k"])
    P(f"[{f}] the law with no end (k fitted, no neighbours): R_s " + ", ".join(f"{F} R_h {RES['law_no_end'][f'{f}|{F}']['Rs_model']:.3f} (z {RES['law_no_end'][f'{f}|{F}']['z']:+.2f})" for F in FS))
# KA5: X -> infinity returns the law
for f in FOOT:
    OSa = own_sums(f, 1e6); OSb = own_sums(f, np.inf); dv = 0.0
    for F in FS:
        ra = fit(("KO1", F, "all"), f, OSa[("KO1", F, "all")]); rb = fit(("KO1", F, "all"), f, OSb[("KO1", F, "all")]); dv = max(dv, abs(ra["Rs_model"] - rb["Rs_model"]))
    KA[f"KA5 X 1e6 = the law, {f}"] = dict(value=dv, ref=0.0, ok=bool(dv <= 1e-3)); P(f"KA5 X = 1e6 against the law (k fitted), {f}: max |dR_s| {dv:.1e}")
# monotonicity of the projected stack in X (premise of the Lean lemma), canonical, all, 1.6 R_h, k = 1 and fitted k
mono = []
for X in (5.0, 10.0, 23.0, 40.0, 53.64, 59.5, 80.0, 120.0, 300.0, 1e6):
    C = cells(A0C, 1.0, X); a = amps(("KO1", 1.6, "all"), "canonical", psum(WW1 * C, MASKS[("KO1", 1.6, "all")])); mono.append((X, a["out"], a["in_"], a["out"] / a["in_"]))
RES["monotonicity_k1"] = mono
P("monotonicity premise (canonical, all, 1.6 R_h, k = 1, no neighbours): X: A_out, A_in, R_s = " + "; ".join(f"{X:g}: {o:.3f}, {i:.3f}, {r:.3f}" for X, o, i, r in mono))
okm = all(mono[i + 1][1] >= mono[i][1] - 1e-9 for i in range(len(mono) - 1)); oki = all(mono[i + 1][2] <= mono[i][2] + 1e-9 for i in range(len(mono) - 1) if mono[i][0] >= 23.0)
P(f"  A_out non-decreasing in X: {okm}; A_in non-increasing in X for X >= 23: {oki}; R_s non-decreasing: {all(mono[i + 1][3] >= mono[i][3] for i in range(len(mono) - 1))}")
RES["monotonicity_premise"] = dict(A_out_nondecreasing=okm, A_in_nonincreasing_from_23=oki)

# ---------------- brackets X = 53.64, 80
for Xb in (53.64, 80.0):
    P(f"\n=== BRACKET X = {Xb} (k fitted, neighbours)  {tm()}")
    lams = lam_grid(Xb); res, NB = graded_set(Xb, lams, Htab_of(Xb)); store = RES["readings"].setdefault(f"X {Xb}", {})
    summarize(f"X {Xb}", res, FOOT, store)
    for f in FOOT:
        g = [res[f][("KO1", 1.6, s)]["nb"] for s in ("all", "late", "early")]
        P(f"[{f}] X {Xb} at 1.6 R_h: z all / late / early {g[0]['z']:+.2f} / {g[1]['z']:+.2f} / {g[2]['z']:+.2f}; chi2 {g[0]['chi2']:.1f}")

# ---------------- MUTATE
PM(f"M1 share x 0.1  {tm()}")
for f in FOOT:
    Xm = 0.1 * XP[f]; lams = lam_grid(Xm); res, NB = graded_set(Xm, lams, Htab_of(Xm), foots=(f,))
    g = {s: res[f][("KO1", 1.6, s)]["nb"] for s in ("all", "late", "early")}; qe, ql = g["early"], g["late"]; sd = jk(qe["diff_l"] - ql["diff_l"])
    ok = all(abs(q["diff"]) <= 2 * q["s_diff"] for q in g.values()) and g["all"]["chi2"] <= 9.49 and abs(qe["diff"] - ql["diff"]) <= 2 * sd
    MUT["readings"][f"M1 {f}"] = dict(X=Xm, z={s: q["z"] for s, q in g.items()}, Rs_model={s: q["Rs_model"] for s, q in g.items()}, k={s: q["k"] for s, q in g.items()}, chi2=g["all"]["chi2"], status="PASS" if ok else "FAIL")
    PM(f"[{f}] M1 X {Xm:.3f}: R_s model all / late / early {g['all']['Rs_model']:.3f} / {g['late']['Rs_model']:.3f} / {g['early']['Rs_model']:.3f} (k {g['all']['k']:.2f}); z {g['all']['z']:+.2f} / {g['late']['z']:+.2f} / {g['early']['z']:+.2f}; "
       f"chi2 {g['all']['chi2']:.1f} -> KiDS {'PASS' if ok else 'FAIL'} (must FAIL)")
PM(f"M2 share x 10 (KiDS reading, lens's own halo only: the neighbours' halos would end beyond 10 Mpc and are not scanned)  {tm()}")
for f in FOOT:
    Xm = 10 * XP[f]; OS = own_sums(f, Xm); rr = {s: fit(("KO1", 1.6, s), f, OS[("KO1", 1.6, s)]) for s in ("all", "late", "early")}
    MUT["readings"][f"M2 {f}"] = dict(X=Xm, z={s: q["z"] for s, q in rr.items()}, Rs_model={s: q["Rs_model"] for s, q in rr.items()}, k={s: q["k"] for s, q in rr.items()})
    PM(f"[{f}] M2 X {Xm:.1f}: R_s model all / late / early {rr['all']['Rs_model']:.3f} / {rr['late']['Rs_model']:.3f} / {rr['early']['Rs_model']:.3f}; z {rr['all']['z']:+.2f} / {rr['late']['z']:+.2f} / {rr['early']['z']:+.2f} "
       "(reported; row 0 is M2's graded bite, in one1_MUTATE.out)")
PM("M3 neighbours' positions shuffled (shuffle 1 used as the real set, the other four as the reference)")
for f in FOOT:
    res, NB, lams = PRIM[f]; il = int(np.argmin(np.abs(np.array(lams) - math.sqrt(res[f][("KO1", 1.0, "all")]["nb"]["k"] * A0C / A0[f]))))
    for F in (1.0, 1.6):
        mk = ("KO1", F, "all"); m = MASKS[mk]; tw, sk, M, Ml = BASE[(mk, f)]
        def a_of(T):
            S = psum(WW1 * T, m); t = S.sum(0); N = t / tw; Nl = (t - S) / (tw - SD[mk]["Sw"])
            A = float((N[CO] * M[CO] / sk[CO] ** 2).sum() / (M[CO] ** 2 / sk[CO] ** 2).sum()); Al = (Nl[:, CO] * Ml[:, CO] / sk[CO] ** 2).sum(1) / (Ml[:, CO] ** 2 / sk[CO] ** 2).sum(1)
            return A, Al
        real, rl = a_of(NB["net"][il]); fake, fl = a_of(NB["shuf0"][il] - NB["shuf_rest"][il]); s = jk(rl)
        bite = abs(real - fake) > 3 * s
        MUT["readings"][f"M3 {f} {F}"] = dict(lam=lams[il], real=real, shuffled=fake, sigma=s, z=(real - fake) / s, bites=bool(bite))
        PM(f"[{f}] M3 {F} R_h (lambda {lams[il]:.2f}): net neighbour term, outer amplitude per unit k: real {real:+.5f} +- {s:.5f}, shuffled-as-real {fake:+.5f}; change {(real - fake) / s:+.1f} sigma -> "
           + ("bites" if bite else "DOES NOT BITE"))

# =================================================================== outputs
kok = all(v["ok"] for v in KA.values()); RES["KA_all_pass"] = kok
P(f"\nKnown answers: {sum(v['ok'] for v in KA.values())} of {len(KA)} PASS -> {'ALL PASS' if kok else 'A KNOWN ANSWER FAILED'}")
for k, v in KA.items():
    if not v["ok"]: P(f"   FAIL {k}: {v}")
KO2R = os.path.join(REPO, "closure_2026_11_09", "KO2_kids_own_field_by_type", "RESULT.md"); RES["KO2_RESULT_exists_at_grading"] = os.path.exists(KO2R)
P(f"KO2 RESULT.md exists at grading: {RES['KO2_RESULT_exists_at_grading']}")
RES["seconds"] = time.time() - T0; P(f"runtime {RES['seconds']:.0f} s"); P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {(str(k) if not isinstance(k, tuple) else "|".join(map(str, k))): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "one1_kids.json"), "w"), indent=1); open(os.path.join(HERE, "one1_kids.out"), "w").write("\n".join(OUT) + "\n")
json.dump(clean(MUT), open(os.path.join(HERE, "one1_kids_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "one1_kids_MUTATE.out"), "w").write("\n".join(OUTM + ["kappa = 1/2 FITTED; not theory closed. Adopts nothing."]) + "\n")
