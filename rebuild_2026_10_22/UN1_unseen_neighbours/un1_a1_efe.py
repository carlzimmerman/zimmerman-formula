#!/usr/bin/env python3
"""UN1, post-result, reported: the amended faint term under the law's catalogue external field (P2 case b), R0, against y_e = 0. kappa = 1/2 FITTED; not theory closed."""
import os, sys
HA = os.path.dirname(os.path.abspath(__file__)); MUTA = "--mutate" in sys.argv; UF = os.path.join(HA, "un1_grade.py"); srcu = open(UF).read(); cutu = "WM = weights(tilt"; assert srcu.count(cutu) == 1
sys.argv = [UF] + [a for a in sys.argv[1:] if not a.startswith("--")]; __file__ = UF; exec(compile(srcu[:srcu.index(cutu)], "un1_head", "exec"))
from scipy.integrate import cumulative_trapezoid as ctz
OMEGA = 0.05481; ZG = np.linspace(0, 1.0, 4001); CHIG = ctz(299792.458 / (100 * NH * np.sqrt(NOM * (1 + ZG) ** 3 + 1 - NOM)), ZG, initial=0); CHI = lambda z: np.interp(z, ZG, CHIG); SCALE = 1.3 if MUTA else 1.0
zmax = N["zmax"]; Vm = OMEGA / 3 * (CHI(zmax) ** 3 - CHI(0.02) ** 3); ok_ = (z_g > 0.02) & (z_g < 0.30) & (Vm > 0); tg = np.clip(np.round((lMb_g - LMB_T[0]) / 0.05).astype(int), 0, NT - 1)
PHID = np.bincount(tg[ok_], 1 / Vm[ok_], NT) / 0.05 * SCALE; RHO = float(np.sum(PHID * MT * 0.05)); nz = N["NZB"]; ZE = N["ZB_"]
W(f"A1: phi on lMb_g by 1/Vmax; n(>10^9.5) {PHID[LMB_T >= 9.5].sum() * 0.05:.3e}, n(>10^10.5) {PHID[LMB_T >= 10.5].sum() * 0.05:.3e} /Mpc^3" + (" [MUTATE phi x 1.3]" if MUTA else ""))
ZS = np.unique(zbin[PJ[SEL]]); def_k4 = 0.0
def wz(ref):
    Wm = np.zeros((len(ZS), NT)); global def_k4
    for i, b in enumerate(ZS):
        lo, hi = ZE[max(b - 1, 0)], ZE[min(b + 2, nz)]; V = OMEGA / 3 * (CHI(hi) ** 3 - CHI(lo) ** 3); m = (z_g >= lo) & (z_g < hi); ncat = np.bincount(tg[m], minlength=NT) / V / 0.05; miss = np.maximum(PHID - ncat, 0.0); miss[:T1] = 0.0
        def_k4 = max(def_k4, float(np.max(PHID - (ncat + miss))) if T1 == 0 else float(np.max((PHID - (ncat + miss))[T1:])))
        L = int(np.median(LIMB[m])) if m.any() else NT - 1; nref = INB[m].sum() / V if ref == "cat" else PHID[L:L + 10].sum() * 0.05
        if nref > 0: Wm[i] = miss * 0.05 / nref
    return Wm
def tf(key, Wm):
    G0 = GT[key][:, 0]; Fh = np.einsum("lt,tbd->lbd", Wm, G0); Me = Wm @ MT; lidx = np.searchsorted(ZS, zbin); out = np.zeros((len(N["CEN"]["ra"]), 15))
    for c0 in range(0, len(SEL), 8000):
        s = SEL[c0:c0 + 8000]; pd_ = PD[s].astype(float); gd = np.clip((np.log(np.maximum(pd_, DGR[0])) - np.log(DGR[0])) / (np.log(DGR[1]) - np.log(DGR[0])), 0, len(DGR) - 1.001); d0 = gd.astype(np.int64); fd = (gd - d0)[:, None]; l = lidx[PJ[s]]
        ctr = (1 - fd) * Fh[l, :, d0] + fd * Fh[l, :, d0 + 1] + point_part(Me[l], pd_)
        for k in range(15): out[:, k] += np.bincount(PC[s], ctr[:, k], len(out))
    return out
def dl(s_): a = amps(s_); return (a["A_O1"] - 1) / a["sA_O1"], a
def cl(d, d0): return "SHORTFALL CLOSES" if abs(d) <= 1 else "HELPS, NOT CLOSED" if (d0 - d >= 0.5 and d > 1) else "NO HELP"

YE, node_weights = N["YE"], N["node_weights"]; WMC = wz("cat"); bO1 = (RCEN > 0.4) & (RCEN <= 1.1); RB = {}
def tf_b(foot, Wm, ye):
    """faint term with the law's catalogue external field: each pair reads its reference neighbour's y_e node, as tnbr does."""
    G_ = GT[foot]; Fh = np.einsum("lt,tnbd->lnbd", Wm, G_); Me = Wm @ MT; lidx = np.searchsorted(ZS, zbin); out = np.zeros((len(N["CEN"]["ra"]), 15))
    for c0 in range(0, len(SEL), 8000):
        s = SEL[c0:c0 + 8000]; pd_ = PD[s].astype(float); gd = np.clip((np.log(np.maximum(pd_, DGR[0])) - np.log(DGR[0])) / (np.log(DGR[1]) - np.log(DGR[0])), 0, len(DGR) - 1.001); d0 = gd.astype(np.int64); fd = (gd - d0)[:, None]; l = lidx[PJ[s]]; a, b, w = node_weights(ye[PJ[s]])
        ctr = (1 - w)[:, None] * ((1 - fd) * Fh[l, a, :, d0] + fd * Fh[l, a, :, d0 + 1]) + w[:, None] * ((1 - fd) * Fh[l, b, :, d0] + fd * Fh[l, b, :, d0 + 1]) + point_part(Me[l], pd_)
        for k in range(15): out[:, k] += np.bincount(PC[s], ctr[:, k], len(out))
    return out
for foot in FOOTS:
    N["tix"], N["MBN_g"] = TIX0, MBN0; key, TNH0 = build(foot); TFa = tf(foot, WMC); TFb = tf_b(foot, WMC, YE[foot]["c10"]); TFH = tf(key, WMC); RB[foot] = {}
    for sm in ("S1", "S3"):
        sb = primary(foot, "b", sample=sm); sa = primary(foot, "a", sample=sm); sH = primary(key, "a", sample=sm, tn=TNH0); tb = st(TFb, sm, "all")["m"]; ta = st(TFa, sm, "all")["m"]; th = st(TFH, sm, "all")["m"]; Ci = HART(15) * np.linalg.inv(cov_of(sa)); d = sa["d"]; X = lambda m: float((d - m) @ Ci @ (d - m))
        row_ = dict(a0=X(sa["m"]), a1=X(sa["m"] + ta), b0=X(sb["m"]), b1=X(sb["m"] + tb), H0=X(sH["m"]), H1=X(sH["m"] + th), term_a=ta.tolist(), term_b=tb.tolist()); RB[foot][sm] = row_
        W(f"  [{foot} {sm} R0] chi2: law y_e 0 {row_['a0']:.1f} -> {row_['a1']:.1f}; law catalogue field {row_['b0']:.1f} -> {row_['b1']:.1f}; route E {row_['H0']:.1f} -> {row_['H1']:.1f}")
        W("     term a " + " ".join(f"{x:6.2f}" for x in ta)); W("     term b " + " ".join(f"{x:6.2f}" for x in tb))
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
json.dump(RB, open(os.path.join(HA, "un1_a1_efe.json"), "w"), indent=1, default=float); open(os.path.join(HA, "un1_a1_efe.out"), "w").write("\n".join(OUT3) + "\n")
