#!/usr/bin/env python3
"""UN1 AMENDMENT A1: only mass the catalogue lacks at each z enters the neighbour term. Post-result diagnostic; the frozen class stays on record.
    OMP_NUM_THREADS=1 nice -n 15 python3 un1_a1.py <kids_source_cache_dir> <work_dir> [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
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
WS = {r: wz(r) for r in ("cat", "phi")}; RA = dict(amendment="A1", mutate=MUTA, foot={}, k={}); bO1 = (RCEN > 0.4) & (RCEN <= 1.1); J2 = json.load(open(os.path.join(RB3, "SI2_spec_isolated_colour", "si2_results.json")))["foot"]; dk1 = 0.0
for r in WS: W(f"  mean missing mass per reference neighbour, ref {r}: lg M_b weighted {np.log10(max(np.median(WS[r] @ MT), 1)):.2f}, median replica number {np.median(WS[r].sum(1)):.2f}")
for foot in FOOTS:
    N["tix"], N["MBN_g"] = TIX0, MBN0; key, TNH0 = build(foot); TNL0 = N["TN"][(foot, "a")]; TOWN[(foot, "red")] = law_table(foot, SHIFT); TOWN[(key, "red")] = town_H(foot, dMs=SHIFT)
    N["tix"], N["MBN_g"] = TIX2, MBN2; TNH2 = tnbr(key, node=0); TNL2 = tnbr(foot, node=0); N["tix"], N["MBN_g"] = TIX0, MBN0; F = {}
    for r, Wm in WS.items():
        TFL, TFH = tf(foot, Wm), tf(key, Wm); F[r] = {}
        for sm in ("S1", "S3"):
            G = {}; s_tL, s_tH = st(TFL, sm, "all"), st(TFH, sm, "all"); G["term"] = dict(L=s_tL["m"].tolist(), H=s_tH["m"].tolist())
            for lad, TL, TH in (("R0", TNL0, TNH0), ("R2", TNL2, TNH2)):
                for B_ in (0.0, 1.0, 0.7):
                    sL = st(modl(foot, TL + B_ * TFL, lad), sm, "all"); sH = st(modl(key, TH + B_ * TFH, lad), sm, "all"); c = compare(sL, sH); dH, aH = dl(sH); aL = amps(sL)
                    if B_ == 0.0: j = J2[foot][sm][f"all_{lad}"]["all"]; dk1 = max(dk1, abs(c["chi2_L"] - j["chi2_L"]), abs(c["chi2_H"] - j["chi2_H"]))
                    G[f"{lad}_B{B_:g}"] = dict(all=c, cls=cls(c), dH=dH, amps_H=aH, amps_L=aL)
                    W(f"  [{foot} ref {r} {sm} {lad} B {B_:g}] chi2 L {c['chi2_L']:.1f} (p {c['pL']:.3f}), H {c['chi2_H']:.1f} (p {c['pH']:.3f}); dchi2 {c['dchi2']:+.1f}; D {c['D']:.2f} -> {cls(c)}; H A_in {aH['A_in']:.2f}+-{aH['sA_in']:.2f} A_O1 {aH['A_O1']:.2f}+-{aH['sA_O1']:.2f} delta {dH:+.2f}; L A_in {aL['A_in']:.2f} A_O1 {aL['A_O1']:.2f}+-{aL['sA_O1']:.2f} A_O2 {aL['A_O2']:.2f}+-{aL['sA_O2']:.2f}")
                for b in ("1", "0.7"): G[f"{lad}_B{b}"]["amended_class"] = cl(G[f"{lad}_B{b}"]["dH"], G[f"{lad}_B0"]["dH"])
                W(f"    A1 CLASS [{foot} ref {r} {sm} {lad}] B 1: {G[f'{lad}_B1']['amended_class']}; B 0.7: {G[f'{lad}_B0.7']['amended_class']}")
            W("     R      " + " ".join(f"{x:6.3f}" for x in RCEN)); W("     term L " + " ".join(f"{x:6.2f}" for x in s_tL["m"])); W("     term H " + " ".join(f"{x:6.2f}" for x in s_tH["m"])); W("     sig    " + " ".join(f"{x:6.2f}" for x in np.sqrt(s_tH["var"]))); G["O1_sum"] = dict(L=float(s_tL["m"][bO1].sum()), H=float(s_tH["m"][bO1].sum())); F[r][sm] = G
    RA["foot"][foot] = F
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
k1 = dk1 <= 1e-9; k4 = def_k4 <= 1e-9; RA["k"] = dict(K1=dk1, K4=def_k4, ok=bool(k1 and k4)); W(f"\nK1 B 0 vs SI2 chi2: {dk1:.1e} {'PASS' if k1 else 'FAIL'}; K4 n_cat + missing >= phi: {def_k4:.1e} {'PASS' if k4 else 'FAIL'}")
if MUTA:
    B0 = json.load(open(os.path.join(HA, "un1_a1_results.json")))["foot"]["canonical"]["cat"]["S1"]["O1_sum"]; A1_ = RA["foot"]["canonical"]["cat"]["S1"]["O1_sum"]; W(f"MUTATE O1 term sum: L {B0['L']:.3f} -> {A1_['L']:.3f}, H {B0['H']:.3f} -> {A1_['H']:.3f}: {'PASS' if A1_['L'] > B0['L'] and A1_['H'] > B0['H'] else 'FAIL'}")
tag = "_MUTATE" if MUTA else ""; json.dump(RA, open(os.path.join(HA, f"un1_a1_results{tag}.json"), "w"), indent=1, default=float); open(os.path.join(HA, f"un1_a1{tag}.out"), "w").write("\n".join(OUT3) + "\n")
