#!/usr/bin/env python3
"""QX22 iter_1: is the law's hot/cold step keyed on kinematic support (lambda_Re)? Criteria FROZEN_CRITERIA.md (f2ac9999a5).
python3 qx22.py [--mutate]   (MUTATE: M1 lambda shuffled within cells; M2 Newton in place of the law). One thread, seconds.
KU2's MaNGA DynPop cuts/model choice/accelerations/cells/Dstat are reproduced verbatim (KA1 checks against ku2.json).
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx22_MUTATE" if MUT else "qx22"; OUT = []; RES = dict(criteria="f2ac9999a5", mutate=MUT); fail = 0
def P(s): print(s, flush=True); OUT.append(s)
G, MS, MPC, C = 6.6743e-11, 1.98892e30, 3.0857e22, 2.99792458e5; H0 = 70.0; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; NB = 2000
nu = lambda y: 0.5 + np.sqrt(0.25 + 1 / y)
phi = lambda y: (nu(y) - 1) / nu(y)
F = os.path.join(REPO, "_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits")
with fits.open(F) as h:
    d = h[1].data; lam, eps, sig, me, msr, z, q = (np.array(d[k], float) for k in ("Lambda_Re", "Eps_MGE", "Sigma_Re", "nsa_elpetro_mass", "nsa_sersic_mass", "z", "Qual"))
    AB = np.array(d["nsa_elpetro_absmag"], float)
    MT = np.array([np.array(h[i].data["log_Mt_rhalf"], float) for i in range(2, 12)]); RH = np.array([np.array(h[i].data["rhalf_arcsec"], float) for i in range(2, 12)]); X2 = np.array([np.array(h[i].data["chi2_dof"], float) for i in range(2, 12)])
nfin = np.sum(np.isfinite(MT) & np.isfinite(RH) & (RH > 0), axis=0)
sel = (q >= 1) & np.isfinite(me) & (me > 0) & np.isfinite(msr) & (z > 0.005) & np.isfinite(lam) & np.isfinite(eps) & (sig > 0) & (nfin >= 8)
lam, eps, sig, me, msr, z, MT, RH, X2, AB = lam[sel], eps[sel], sig[sel], me[sel], msr[sel], z[sel], MT[:, sel], RH[:, sel], X2[:, sel], AB[sel]
ur = AB[:, 2] - AB[:, 4]; red = np.isfinite(ur) & (ur >= 2.5); blue = np.isfinite(ur) & (ur < 2.5)
slow = (lam < 0.08 + eps / 4) & (eps < 0.4); n = len(z)
DA = C * z / H0 / (1 + z) * MPC
def accel(mt_log, rh_arcsec, mstar_log):
    r = rh_arcsec * math.pi / 648000 * DA; return G * 10 ** mt_log * MS / r ** 2, G * 0.5 * 10 ** mstar_log * MS / r ** 2
X2v = np.where(np.isfinite(X2) & np.isfinite(MT) & np.isfinite(RH) & (RH > 0), X2, np.inf); order = np.argsort(X2v, axis=0, kind="stable"); b1, b2 = order[0], order[1]; jj = np.arange(n)
mtm, rhm = MT[b1, jj], RH[b1, jj]; mt2, rh2 = MT[b2, jj], RH[b2, jj]
lm = me; cm = np.floor(lm / 0.2).astype(int); cs = np.floor(np.log10(sig) / 0.1).astype(int); cell = cm * 1000 + cs
lam_use = lam.copy()
if MUT:
    rng0 = np.random.default_rng(20261106)
    for c in np.unique(cell): i = np.where(cell == c)[0]; lam_use[i] = rng0.permutation(lam[i])
def law(gb, a0): return np.zeros_like(gb) + 1.0 if (MUT and MODE[0] == "newton") else nu(gb / a0)
MODE = ["law"]
def resid(go, gb, a0): return np.log(go) - np.log((1.0 if MODE[0] == "newton" else nu(gb / a0)) * gb)
def Dstat(r, sl, cl, idx=None):
    if idx is not None: r, sl, cl = r[idx], sl[idx], cl[idx]
    o = np.argsort(cl, kind="stable"); r, sl, cl = r[o], sl[o], cl[o]; u, st = np.unique(cl, return_index=True); en = np.r_[st[1:], len(cl)]
    num = den = 0.0; nc = 0
    for a, b in zip(st, en):
        s = sl[a:b]; ns = int(s.sum()); nf = (b - a) - ns
        if ns >= 2 and nf >= 2:
            w = min(ns, nf); rr = r[a:b]; num += w * (np.median(rr[s]) - np.median(rr[~s])); den += w; nc += 1
    return (num / den if den else float("nan")), nc
def s_map(m, lamv):
    if m == "M-step": return ((lamv < 0.08 + eps / 4) & (eps < 0.4)).astype(float)
    if m == "M-lin": return np.clip(1 - lamv / 0.8, 0, 1)
    if m == "M-sq": return 1 - np.clip(lamv / 0.8, 0, 1) ** 2
MAPS = ("M-step", "M-lin", "M-sq")
# calibrations from the record (QX20 class means / SPARC anchor; LW1 bright M31 median)
Q20 = json.load(open(os.path.join(REPO, "closure_2026_11_06/QX20_failure_ladder/qx20.json")))
LW = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/LW1_law_scorecard/lw1_dwarfs.json")))
KU2 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/KU2_kappa_universality_model_choice/ku2.json")))
KG = np.array([1.298e-13, 2.291e-13, 4.042e-13, 7.131e-13, 1.258e-12, 2.220e-12, 3.917e-12])   # QX21 T1 K1 bins (qx21.out)
RES["foot"] = {}
for foot, a0 in A0.items():
    MODE[0] = "law"
    anchor = Q20[foot]["sparc_mean"]; m31 = LW["footings"][foot]["rows"]["plain"]["bright M31"]["median"]; ell = Q20[foot]["class_means"]["E"]
    F0 = 10 ** (m31 - anchor); F0e = 10 ** (ell - anchor)
    go, gb = accel(mtm, rhm, lm); ok = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
    # KA1: KU2's D (all colours, binary slow/fast)
    r_all = np.full(n, np.nan); r_all[ok] = resid(go[ok], gb[ok], a0); g_ = np.isfinite(r_all)
    Dku, _ = Dstat(r_all[g_], slow[g_], cell[g_]); ka1 = abs(Dku - KU2[foot]["D"]) <= 1e-6
    if not MUT: fail += not ka1
    P(f"\n[{foot}] KA1 KU2 D reproduced: {Dku:+.6f} vs {KU2[foot]['D']:+.6f} -> {'PASS' if ka1 else 'FAIL'}")
    P(f"[{foot}] F0 (bright M31 dSphs - SPARC anchor) = {F0:.4f}; systematic F0 (ellipticals) = {F0e:.4f}")
    y = np.where(ok, gb / a0, np.nan)
    A = (lam_use < 0.2); B = (lam_use > 0.5)
    base = ok & red & (A | B)
    def Dfor(mt, rh, mstar=lm, mask=base, grp=A):
        gk, bk = accel(mt, rh, mstar); okk = mask & np.isfinite(gk) & np.isfinite(bk) & (gk > 0) & (bk > 0)
        rk = resid(gk[okk], bk[okk], a0); return Dstat(rk, grp[okk], cell[okk])[0], okk, rk
    D, okk, rk = Dfor(mtm, rhm); _, nc = Dstat(rk, A[okk], cell[okk])
    rng = np.random.default_rng(20261107); idxs = np.where(okk)[0]
    bs = [Dstat(rk, A[okk], cell[okk], rng.integers(0, len(rk), len(rk)))[0] for _ in range(NB)]; st = float(np.nanstd(bs))
    D2 = Dfor(mt2, rh2)[0]; Ds = Dfor(mtm, rhm, msr)[0]; sD = math.sqrt(st ** 2 + (D - D2) ** 2 + (D - Ds) ** 2)
    R = dict(n=int(okk.sum()), n_low=int((A & okk).sum()), n_high=int((B & okk).sum()), cells=nc, D=D, sigma_stat=st, sigma_model=abs(D - D2), sigma_mass=abs(D - Ds), sigma_D=sD, F0=F0, F0_ell=F0e, maps={})
    P(f"[{foot}] T1 red (u-r>=2.5): n {R['n']} (low lambda<0.2: {R['n_low']}, high >0.5: {R['n_high']}), cells {nc}; D(low-high) = {D:+.4f} +- {sD:.4f} ln (stat {st:.4f}, model {abs(D-D2):.4f}, M* {abs(D-Ds):.4f}); median y {np.nanmedian(y[okk]):.2f}")
    verdicts = {}
    for m in MAPS:
        out = {}
        for tag, FF in (("F0", F0), ("F0_ell", F0e)):
            s = s_map(m, lam_use); inc = np.log(1 + (FF - 1) * s * phi(np.where(ok, y, 1.0)))
            Dp = Dstat(inc[okk], A[okk], cell[okk])[0]; out[tag] = Dp
        Dp = out["F0"]; kill = D < Dp - 3 * sD; cons = abs(D - Dp) <= 2 * sD and D > 3 * sD
        verdicts[m] = "KILLED" if kill else ("CONSISTENT" if cons else "neither")
        R["maps"][m] = dict(D_pred=Dp, D_pred_F0_ell=out["F0_ell"], z_vs_pred=(D - Dp) / sD, verdict=verdicts[m])
        P(f"[{foot}]   {m}: D_pred {Dp:+.4f} ln (ellipticals F0: {out['F0_ell']:+.4f}); (D - D_pred)/sigma = {(D - Dp) / sD:+.2f} -> {verdicts[m]}")
    R["T1"] = verdicts
    if not MUT:   # C-inj power check, M-lin
        s = s_map("M-lin", lam); inc = np.log(1 + (F0 - 1) * s * phi(np.where(ok, y, 1.0)))
        Dinj = Dstat(rk + inc[okk], A[okk], cell[okk])[0]; Dp = R["maps"]["M-lin"]["D_pred"]; cinj = abs((Dinj - D) - Dp) <= 0.2 * abs(Dp); fail += not cinj
        R["C_inj"] = dict(rise=Dinj - D, want=Dp, ok=bool(cinj)); P(f"[{foot}] C-inj (M-lin injected): D rises {Dinj - D:+.4f} vs D_pred {Dp:+.4f} (within 20 %): {'PASS' if cinj else 'FAIL'}")
    # T2 KiDS compatibility (dex)
    m10 = ok & (lm >= 10) & (lm <= 11)
    T2 = {}
    for m in MAPS:
        s = s_map(m, lam); sr = float(np.mean(s[m10 & red])); sb = float(np.mean(s[m10 & blue])); ph = phi(KG / a0)
        Dk = float(np.mean(np.log10((1 + (F0 - 1) * sr * ph) / (1 + (F0 - 1) * sb * ph)))); comp = abs(0.158 - Dk) <= 2 * 0.064
        T2[m] = dict(s_red=sr, s_blue=sb, D_KiDS_pred=Dk, compatible=bool(comp)); P(f"[{foot}] T2 {m}: s_red {sr:.3f} s_blue {sb:.3f} -> D_KiDS pred {Dk:+.3f} dex vs 0.158 +- 0.064: {'COMPATIBLE' if comp else 'NOT compatible'}")
    R["T2"] = T2
    # T3 type at fixed support (report)
    m3 = ok & (lam_use > 0.5) & (red | blue); g3, b3 = accel(mtm, rhm, lm); r3 = resid(g3[m3], b3[m3], a0); D3, nc3 = Dstat(r3, red[m3], cell[m3])
    bs3 = [Dstat(r3, red[m3], cell[m3], rng.integers(0, len(r3), len(r3)))[0] for _ in range(500)]
    R["T3"] = dict(D_red_minus_blue_ln=D3, sigma_stat=float(np.nanstd(bs3)), cells=nc3, n_red=int((red & m3).sum()), n_blue=int((blue & m3).sum()))
    P(f"[{foot}] T3 (report) red - blue at lambda > 0.5, matched M*/sigma: {D3:+.4f} +- {np.nanstd(bs3):.4f} ln ({D3 / math.log(10):+.4f} dex); n red {R['T3']['n_red']}, blue {R['T3']['n_blue']}, cells {nc3}; blue gas bias negative")
    # T4 dwarfs by morphology (report)
    ps = LW["footings"][foot]["per_system"]
    poor = ["Cetus", "Tucana", "Phoenix", "Leo T", "Pegasus dIrr", "Aquarius", "UGC 4879", "Antlia B"]; rich = ["IC 1613", "Leo A", "NGC 6822", "Sagittarius dIrr", "WLM"]
    mp = float(np.median([ps[k]["plain"] for k in poor])) - anchor; mr = float(np.median([ps[k]["plain"] for k in rich])) - anchor
    R["T4"] = dict(gas_poor_median_minus_anchor=mp, gas_rich_median_minus_anchor=mr, n_poor=len(poor), n_rich=len(rich))
    P(f"[{foot}] T4 (report, provisional types) LG field gas-poor dSph/transition (N {len(poor)}): {mp:+.3f}; gas-rich dIrr (N {len(rich)}): {mr:+.3f} dex vs SPARC anchor")
    # T5 residual after support key (report)
    full = 0.5 * ((m31 - anchor) + (ell - anchor)); x = Q20[foot]["class_means"]["X"] - anchor; gr = Q20[foot]["class_means"]["G"] - anchor
    R["T5"] = dict(full_dispersion_mean=full, XCOP_minus_that=x - full, groups_minus_that=gr - full)
    P(f"[{foot}] T5 (report) fully dispersion-supported classes (bright M31 dSphs, ellipticals) mean {full:+.3f}; X-COP left {x - full:+.3f}, groups left {gr - full:+.3f} dex")
    if MUT:  # M1 shuffle check; M2 Newton sensitivity
        R["M1_ok"] = bool(abs(D) <= 2 * sD); P(f"[{foot}] M1 (lambda shuffled within cells) |D| <= 2 sigma: {'PASS' if R['M1_ok'] else 'FAIL'}")
        MODE[0] = "newton"; lam_save = lam_use.copy(); lam_use[:] = lam
        Dn = Dfor(mtm, rhm, lm, ok & red & ((lam < 0.2) | (lam > 0.5)), lam < 0.2)[0]; MODE[0] = "law"
        Dl = Dfor(mtm, rhm, lm, ok & red & ((lam < 0.2) | (lam > 0.5)), lam < 0.2)[0]; lam_use[:] = lam_save
        R["M2"] = dict(D_newton=Dn, D_law=Dl, differs=bool(abs(Dn - Dl) > 3 * sD)); P(f"[{foot}] M2 Newton D {Dn:+.4f} vs law D {Dl:+.4f}: differs > 3 sigma: {'YES' if R['M2']['differs'] else 'NO'}")
    RES["foot"][foot] = R
if not MUT:
    k = all(all(v == "KILLED" for v in RES["foot"][f]["T1"].values()) for f in A0)
    c = all(any(v == "CONSISTENT" for v in RES["foot"][f]["T1"].values()) and any(t["compatible"] for t in RES["foot"][f]["T2"].values()) for f in A0)
    RES["label"] = "SUPPORT KEY KILLED (gas-poor dynamics, r_half)" if k else ("SUPPORT KEY CONSISTENT" if c else "NO VERDICT")
    P(f"\nLABEL: {RES['label']}")
RES["fail"] = fail; P(f"failed checks: {fail}")
json.dump(RES, open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if (MUT or fail) else 0)
