#!/usr/bin/env python3
"""KO1 shape checks (AMENDMENT_A2.md, a52e709b22).  REPORTED ONLY, post hoc where A2 says so: no label rests on anything here.
PH1  R_s = A(outer bins 0-3) / A(inner bins 7-12) per lens set, joint jackknife; the law's exact floor for R_s.
E7   the frozen cut with the veto radius widened to 1.3 and 1.6 R_h (the tapered edge of the hole leaves the graded range).
PH2  B21's published KiDS-bright isolated and GAMA isolated tables: inner amplitude and R_s with the joint covariance.
PH3  (added after E7 was seen; post hoc) the two-phase exterior in the same calibration-free form: with the enclosed-mass
     factor k that the inner window asks for, R_s(X) = k A_II(X) / A(inner); the share X the outer bins need.
Run: python3 ko1_shape.py -> ko1_shape.json, ko1_shape.out.    kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
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
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar"); B21 = os.path.join(DATA, "brouwer2021_rar")
T0 = time.time(); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt"); NPAT = 50
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
f30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"]; patch = np.load(os.path.join(DATA, "cfg96_stack.npz"))["patch"]
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
ALL = np.ones(NL, bool); LATE = typ == 0; EARLY = typ == 1
OUTER, OUT3, INNER = [0, 1, 2, 3], [1, 2, 3], [7, 8, 9, 10, 11, 12]; USED = OUTER + INNER
XG, WGL = np.polynomial.legendre.leggauss(24); R3 = (3.0 * Mpc) ** 2
def cells(a0, k=1.0):
    m = np.zeros((NL, 15))
    for b in USED:
        t_lo = G * Mg / EDGES[b + 1]; t_hi = np.minimum(G * Mg / EDGES[b], R3); ok = t_hi > t_lo
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            f = glaw(k * G * Mg[:, None] / t, a0)
        m[:, b] = np.where(ok, (f * WGL[None, :]).sum(1) / 2, 0.0)
    return m
def tp_unit():                                    # (4 / pi) x cell-averaged g: the two-phase exterior per unit (1 + X)
    m = np.zeros((NL, 15))
    for b in OUTER:
        t_lo = G * Mg / EDGES[b + 1]; t_hi = np.minimum(G * Mg / EDGES[b], R3); ok = t_hi > t_lo
        with np.errstate(divide="ignore", invalid="ignore"):
            v = (4 / math.pi) * G * Mg * np.log(t_hi / t_lo) / (t_hi - t_lo)
        m[:, b] = np.where(ok, v, 0.0)
    return m
TPU = tp_unit(); X_SHARE = 0.11958060485606123 / 0.0215; X_CAP = 53.64
KGRID = np.array([0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0])
LAWK = {f: [cells(A0[f], k) for k in KGRID] for f in FOOT}
LAW = {f: LAWK[f][4] for f in FOOT}
P(f"KO1 shape checks.  model cells on {len(KGRID)} enclosed-mass factors  [{time.time() - T0:.0f} s]")
def psum(arr, mask):
    pm = patch[mask]; a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, c], minlength=NPAT) for c in range(arr.shape[1])], axis=1)
def amp(mask, Mo, cols, Mnum=None):
    """data amplitude over cols; if Mnum is given, the amplitude of the model Mnum against Mo with the data's weights."""
    Sg = psum(WG[:, cols], mask); Sw = psum(WW[:, cols], mask); Sm = psum((WW * Mo)[:, cols], mask)
    tg, tw, tm = Sg.sum(0), Sw.sum(0), Sm.sum(0)
    D = 4 * G * tg / tw; M = tm / tw
    Dl = 4 * G * (tg - Sg) / (tw - Sw); Ml = (tm - Sm) / (tw - Sw)
    sk = np.sqrt((NPAT - 1) / NPAT * ((Dl - Dl.mean(0)) ** 2).sum(0))
    if Mnum is not None:
        N = (WW * Mnum)[mask][:, cols].sum(0) / tw
        return float((N * M / sk ** 2).sum() / (M * M / sk ** 2).sum())
    A = float((D * M / sk ** 2).sum() / (M * M / sk ** 2).sum())
    Al = (Dl * Ml / sk ** 2).sum(1) / (Ml * Ml / sk ** 2).sum(1)
    s = float(np.sqrt((NPAT - 1) / NPAT * ((Al - Al.mean()) ** 2).sum()))
    return dict(A=A, s=s, Al=Al, per=[float(a / b) for a, b in zip(D, M)], per_err=[float(a / b) for a, b in zip(sk, M)], n=int(mask.sum()), w=float(tw.sum()))
def ratio(ro, ri):
    R = ro["A"] / ri["A"]; Rl = ro["Al"] / ri["Al"]
    return R, float(np.sqrt((NPAT - 1) / NPAT * ((Rl - Rl.mean()) ** 2).sum()))
def floor_of(mask, foot, A_inner):
    """the law's smallest R_s: the enclosed-mass factor k that reproduces A_inner, held constant out to the outer bins."""
    ai = np.array([amp(mask, LAW[foot], INNER, Mnum=LAWK[foot][i]) for i in range(len(KGRID))])
    ao = np.array([amp(mask, LAW[foot], OUTER, Mnum=LAWK[foot][i]) for i in range(len(KGRID))])
    if not (ai[0] < A_inner < ai[-1]): return None, None
    lk = np.interp(A_inner, ai, np.log(KGRID)); return float(math.exp(lk)), float(np.interp(lk, np.log(KGRID), ao) / A_inner)

# ------------------------------------------------------------------ catalogue: host-free at veto radius f R_h
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
r_ = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); z_ = np.array(b["zphot_ANNz2"], dtype="f8")
logM_ = np.array(Lp["MASS_MED"], dtype="f8") + 0.15; ra_ = np.array(b["RAJ2000"], dtype="f8"); dec_ = np.array(b["DECJ2000"], dtype="f8")
del b, Lp; HB.close(); HL.close()
nb = (r_ < 20) & (z_ >= 0.02) & (z_ <= 0.8) & np.isfinite(logM_) & (logM_ > 7); inb = np.where(nb)[0]
xN = unitvec(ra_[inb], dec_[inb]); chiN = DC(z_[inb]); logMN = logM_[inb]
key = {(a, d): i for i, (a, d) in enumerate(zip(ra_[inb], dec_[inb]))}
selfN = np.array([key[(a, d)] for a, d in zip(ln["ra"], ln["dec"])]); treeN = cKDTree(xN); xL = xN[selfN]
RH = np.minimum(3.0, np.sqrt(G * mgal_of(logMs) * Msun / 1e-15) / Mpc)
def hostfree(fac, dm=0.3, W=230.0, CH=300):
    chord = 2 * np.sin(fac * RH * (1 + zl) / chil / 2); dmin = np.full(NL, np.inf)
    for i0 in range(0, NL, CH):
        i1 = min(i0 + CH, NL)
        lists = treeN.query_ball_point(xL[i0:i1], r=chord[i0:i1])
        c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(c.sum())
        if tot == 0: continue
        k = np.repeat(np.arange(len(c)), c); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot); li = i0 + k
        keep = (j != selfN[li]) & (logMN[j] >= logMs[li] + dm); li, j = li[keep], j[keep]
        np.minimum.at(dmin, li, np.abs(chiN[j] - chil[li]))
    return dmin >= W
HFf = {}
for fac in (1.0, 1.3, 1.6):
    HFf[fac] = hostfree(fac); P(f"  veto radius {fac:.1f} R_h: host-free {int(HFf[fac].sum()):,}  [{time.time() - T0:.0f} s]")
HF = HFf[1.0]; assert int(HF.sum()) == 40667

RES = dict(lane="KO1", stage="shape", amendment="a52e709b22", note="reported only; PH1 is post hoc", foot={})
SETS = {"W10 all": ALL, "hosted": ~HF, "host-free all": HF, "host-free late": HF & LATE, "host-free early": HF & EARLY,
        "W30 all": f30, "W30 late": f30 & LATE, "W30 early": f30 & EARLY, "host-free and W30": HF & f30}
wtot = WW[:, OUTER].sum()
for foot in FOOT:
    L = LAW[foot]; F = {"PH1": {}, "E7": {}}
    P(f"\n================ footing {foot}")
    P("PH1 (post hoc) shape ratio R_s = A(outer 0-3) / A(inner 7-12); R_s' leaves out the outermost bin; floor = the law's smallest R_s")
    for name, m in SETS.items():
        ro, r3, ri = amp(m, L, OUTER), amp(m, L, OUT3), amp(m, L, INNER)
        R, sR = ratio(ro, ri); Rp, sRp = ratio(r3, ri); k, fl = floor_of(m, foot, ri["A"])
        F["PH1"][name] = dict(n=int(m.sum()), outer=(ro["A"], ro["s"]), outer_bins123=(r3["A"], r3["s"]), inner=(ri["A"], ri["s"]), Rs=(R, sR), Rs_no_outermost=(Rp, sRp),
                              k_inner=k, law_floor=fl, z_below_floor=(None if fl is None else (fl - R) / sR), z_below_floor_no_outermost=(None if fl is None else (fl - Rp) / sRp))
        P(f"  {name:20s} outer {ro['A']:+.3f} +- {ro['s']:.3f}  inner {ri['A']:+.3f} +- {ri['s']:.3f}  R_s {R:+.3f} +- {sR:.3f}  R_s' {Rp:+.3f} +- {sRp:.3f}  "
          + (f"k {k:.2f}  floor {fl:.3f}  below floor by {(fl - R) / sR:+.2f} sigma ({(fl - Rp) / sRp:+.2f} without the outermost bin)" if fl is not None else "floor n/a"))
    P("E7 the frozen cut with a wider veto radius (Delta 0.3 dex, W 230 Mpc); the lensing sums still end at R_h")
    for fac in (1.0, 1.3, 1.6):
        m = HFf[fac]; ro, r3, ri = amp(m, L, OUTER), amp(m, L, OUT3), amp(m, L, INNER); R, sR = ratio(ro, ri); Rp, sRp = ratio(r3, ri)
        rl, re = amp(m & LATE, L, OUTER), amp(m & EARLY, L, OUTER)
        F["E7"][f"{fac:.1f}"] = dict(n=int(m.sum()), f_w=float(WW[m][:, OUTER].sum() / wtot), per_bin=ro["per"], per_bin_err=ro["per_err"], outer=(ro["A"], ro["s"]),
                                    inner=(ri["A"], ri["s"]), Rs=(R, sR), Rs_no_outermost=(Rp, sRp), late=(rl["A"], rl["s"]), early=(re["A"], re["s"]))
        P(f"  {fac:.1f} R_h: {int(m.sum()):6,d} lenses  f_w {WW[m][:, OUTER].sum() / wtot:.3f}  bins " + " ".join(f"{a:+.2f}({b:.2f})" for a, b in zip(ro["per"], ro["per_err"]))
          + f"  outer {ro['A']:+.3f} +- {ro['s']:.3f}  inner {ri['A']:+.3f} +- {ri['s']:.3f}  R_s {R:+.3f} +- {sR:.3f}  R_s' {Rp:+.3f} +- {sRp:.3f}  late {rl['A']:+.2f} +- {rl['s']:.2f}  early {re['A']:+.2f} +- {re['s']:.2f}")
    P("PH3 (post hoc) the two-phase exterior relative to the inner level, with the inner window's enclosed-mass factor k:  R_s(X) = k (1 + X) a / A(inner)")
    F["PH3"] = {}
    for fac in (1.0, 1.3, 1.6):
        m = HFf[fac]; ro, ri = amp(m, L, OUTER), amp(m, L, INNER); R, sR = ratio(ro, ri); k, fl = floor_of(m, foot, ri["A"])
        a_unit = amp(m, L, OUTER, Mnum=TPU)                      # A_II per unit (1 + X) at the record's masses
        rs = lambda X: k * (1 + X) * a_unit / ri["A"]
        Xbest = R * ri["A"] / (k * a_unit) - 1; Xlo = (R - 2 * sR) * ri["A"] / (k * a_unit) - 1; Xhi = (R + 2 * sR) * ri["A"] / (k * a_unit) - 1
        wo = amp(ALL, L, OUTER); dW = wo["A"] - ro["A"]; dl = wo["Al"] - ro["Al"]; sW = float(np.sqrt((NPAT - 1) / NPAT * ((dl - dl.mean()) ** 2).sum()))
        F["PH3"][f"{fac:.1f}"] = dict(k=k, law_floor=fl, Rs=(R, sR), Rs_two_phase_share=rs(X_SHARE), Rs_two_phase_cap=rs(X_CAP), X_best=Xbest, X_2sigma=(Xlo, Xhi),
                                     z_law=(fl - R) / sR, z_cap=(rs(X_CAP) - R) / sR, z_share=(rs(X_SHARE) - R) / sR, w10_minus_hostfree=(dW, sW))
        P(f"  {fac:.1f} R_h: R_s {R:.3f} +- {sR:.3f} | law floor {fl:.3f} ({(fl - R) / sR:+.2f} sigma) | two-phase cap {rs(X_CAP):.3f} ({(rs(X_CAP) - R) / sR:+.2f}) | "
          f"two-phase share {rs(X_SHARE):.3f} ({(rs(X_SHARE) - R) / sR:+.2f}) | share needed X {Xbest:.0f} (2 sigma {Xlo:.0f} to {Xhi:.0f}) | W10 - host-free outer {dW:+.3f} +- {sW:.3f}")
    RES["foot"][foot] = F

# ------------------------------------------------------------------ PH2: B21's published isolated tables
KG4 = 4 * G * Msun / (3.0857e16) ** 2
def rd_esd(fn):
    a = np.loadtxt(os.path.join(B21, fn)); a = a[np.argsort(a[:, 0])]; return a[:, 0], KG4 * a[:, 1] / a[:, 4]
def rd_cov(fn):
    a = np.loadtxt(os.path.join(B21, fn)); ru = np.unique(a[:, 2]); C = np.zeros((len(ru), len(ru)))
    C[np.searchsorted(ru, a[:, 2]), np.searchsorted(ru, a[:, 3])] = KG4 ** 2 * a[:, 4] / a[:, 6]; return C
def win(g, d, C, a0, idx, k=1.0):
    M = glaw(g[idx], a0); Ci = np.linalg.inv(C[np.ix_(idx, idx)]); den = float(M @ Ci @ M); w = Ci @ M / den
    full = np.zeros(len(g)); full[idx] = w
    return (float(w @ d[idx]) if k == 1.0 else float(w @ glaw(k * g[idx], a0))), full
P("\nPH2 B21's published isolated tables (full covariance): outer = four lowest points, inner = points 8 to 13 (bins 7-12)")
RES["PH2"] = {}
for foot in FOOT:
    a0 = A0[foot]; RES["PH2"][foot] = {}
    for name, fe, fc in (("KiDS-bright isolated", "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt"),
                         ("GAMA isolated", "Fig-4-C1_RAR-GAMA-isolated_Nobins.txt", "Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt"),
                         ("KiDS-bright, hot gas", "Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt", "Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt")):
        g, d = rd_esd(fe); C = rd_cov(fc)
        Ao, wo = win(g, d, C, a0, np.array(OUTER)); Ai, wi = win(g, d, C, a0, np.array(INNER))
        so, si, coi = math.sqrt(wo @ C @ wo), math.sqrt(wi @ C @ wi), float(wo @ C @ wi)
        R = Ao / Ai; sR = abs(R) * math.sqrt((so / Ao) ** 2 + (si / Ai) ** 2 - 2 * coi / (Ao * Ai))
        ks = np.exp(np.linspace(math.log(0.1), math.log(8), 400)); ai = np.array([win(g, d, C, a0, np.array(INNER), k)[0] for k in ks])
        kk = float(np.interp(Ai, ai, ks)); fl = win(g, d, C, a0, np.array(OUTER), kk)[0] / Ai
        RES["PH2"][foot][name] = dict(outer=(Ao, so), inner=(Ai, si), Rs=(R, sR), k_inner=kk, law_floor=fl, z_below_floor=(fl - R) / sR)
        P(f"  {foot:9s} {name:22s} outer {Ao:.3f} +- {so:.3f}  inner {Ai:.3f} +- {si:.3f}  R_s {R:.3f} +- {sR:.3f}  k {kk:.2f}  floor {fl:.3f}  below floor by {(fl - R) / sR:+.2f} sigma")
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
json.dump(clean(RES), open(os.path.join(HERE, "ko1_shape.json"), "w"), indent=1)
open(os.path.join(HERE, "ko1_shape.out"), "w").write("\n".join(OUT) + "\n")
