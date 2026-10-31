#!/usr/bin/env python3
"""UN1_unseen_neighbours (FROZEN_CRITERIA.md, 2950d10ef6): mass below G3C's r 19.8 in the neighbour term of both models, on SI2's stack.
    OMP_NUM_THREADS=1 nice -n 15 python3 un1_grade.py <kids_source_cache_dir> <work_dir> [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math
HERE3 = os.path.dirname(os.path.abspath(__file__)); RB3 = os.path.dirname(HERE3); SI2F = os.path.join(RB3, "SI2_spec_isolated_colour", "si2_grade.py")
MUT3 = "--mutate" in sys.argv; sys.argv = [SI2F] + [a for a in sys.argv[1:] if not a.startswith("--")]
src2 = open(SI2F).read(); cut2 = "J1 = None if MUT2"; assert src2.count(cut2) == 1; __file__ = SI2F; exec(compile(src2[:src2.index(cut2)], "si2_head", "exec"))
OUT3 = []
def W(s): print(s, flush=True); OUT3.append(str(s))
PC, PJ, PD, MLIM, zbin, lMb_nat = (N[k] for k in ("PC", "PJ", "PD", "MLIM", "zbin", "lMb_nat"))
AMB = json.load(open(os.path.join(RB3, "AM1_native_abundance_match", "am1_bmf.json"))); PHI = np.maximum(np.interp(LMB_T, np.array(AMB["grid"]), np.array(AMB["all"]), left=0.0, right=0.0), 0.0)
LIMB = np.round((lMb_nat(MLIM[zbin], z_g) - LMB_T[0]) / 0.05).astype(int)   # limit per galaxy on the type grid, catalogue (blue) inventory
INB = (lMb_g >= LMB_T[np.clip(LIMB, 0, len(LMB_T) - 1)] - 1e-9) & (lMb_g < LMB_T[np.clip(LIMB, 0, len(LMB_T) - 1)] + 0.5)
SEL = np.where(INB[PJ])[0]; T1 = int(np.argmin(np.abs(LMB_T - 7.5)))
W(f"\nUN1 faint neighbours on SI2's stack; reference pairs {len(SEL):,} of {len(PC):,}; median limit lg M_b {np.median(LMB_T[np.clip(LIMB[idxS1], 0, len(LMB_T) - 1)]):.2f}; kappa = 1/2 FITTED; footings never pooled; not theory closed" + (" [MUTATE phi tilted]" if MUT3 else ""))
LS = np.unique(LIMB[PJ[SEL]]); NT = len(LMB_T); MT = 10 ** LMB_T
def weights(tilt=0.0, tlo=T1, thi=None):
    """W[L index in LS, t]: phi(t)/sum over the reference band, for t below limit L."""
    Wm = np.zeros((len(LS), NT))
    for i, L in enumerate(LS):
        nb = PHI[L:L + 10].sum(); top = min(L, NT if thi is None else thi)
        if nb > 0 and top > tlo: Wm[i, tlo:top] = PHI[tlo:top] / nb * (MT[tlo:top] / MT[min(L, NT - 1)]) ** tilt
    return Wm
def tfaint(key, Wm):
    """per-centre faint term (Ncentres, 15): tnbr's interpolation and exact point part, node 0."""
    G0 = GT[key][:, 0]; Fh = np.einsum("lt,tbd->lbd", Wm, G0); Me = Wm @ MT; lidx = np.searchsorted(LS, LIMB); out = np.zeros((len(N["CEN"]["ra"]), 15))
    for c0 in range(0, len(SEL), 8000):
        s = SEL[c0:c0 + 8000]; pd_ = PD[s].astype(float); gd = np.clip((np.log(np.maximum(pd_, DGR[0])) - np.log(DGR[0])) / (np.log(DGR[1]) - np.log(DGR[0])), 0, len(DGR) - 1.001); d0 = gd.astype(np.int64); fd = (gd - d0)[:, None]; l = lidx[PJ[s]]
        ctr = (1 - fd) * Fh[l, :, d0] + fd * Fh[l, :, d0 + 1] + point_part(Me[l], pd_)
        for k in range(15): out[:, k] += np.bincount(PC[s], ctr[:, k], len(out))
    return out
def delta(st_): a = amps(st_); return (a["A_O1"] - 1) / a["sA_O1"], a
def cl(d, d0): return "SHORTFALL CLOSES" if abs(d) <= 1 else "HELPS, NOT CLOSED" if (d0 - d >= 0.5 and d > 1) else "NO HELP"
WM = weights(tilt=-0.3 if MUT3 else 0.0); WLOW = weights(thi=T1 + 10); J2 = json.load(open(os.path.join(RB3, "SI2_spec_isolated_colour", "si2_results.json")))["foot"]
RES3 = dict(criteria="2950d10ef6", mutate=MUT3, foot={}, k={}); dk1 = 0.0; dk2 = 0.0; dk3 = 0.0; O1 = RANGE["O1"] if "O1" in RANGE else None
for foot in FOOTS:
    N["tix"], N["MBN_g"] = TIX0, MBN0; key, TNH0 = build(foot); TNL0 = N["TN"][(foot, "a")]; TOWN[(foot, "red")] = law_table(foot, SHIFT); TOWN[(key, "red")] = town_H(foot, dMs=SHIFT)
    N["tix"], N["MBN_g"] = TIX2, MBN2; TNH2 = tnbr(key, node=0); TNL2 = tnbr(foot, node=0); N["tix"], N["MBN_g"] = TIX0, MBN0
    TFL, TFH = tfaint(foot, WM), tfaint(key, WM)
    if foot == FOOTS[0] and not MUT3:
        ts = int(np.argmin(np.abs(LMB_T - 9.0))); Wd = np.zeros_like(WM); Wd[:, ts] = 1.0; a_ = tfaint(key, Wd)      # K2: all weight at one type vs tnbr on relabelled pairs
        sv = (N["PC"], N["PJ"], N["PD"], N["tix"], N["MBN_g"]); N["PC"], N["PJ"], N["PD"] = PC[SEL], PJ[SEL], PD[SEL]; N["tix"] = np.full_like(TIX0, ts); N["MBN_g"] = np.full_like(MBN0, MT[ts]); b_ = tnbr(key, node=0); N["PC"], N["PJ"], N["PD"], N["tix"], N["MBN_g"] = sv
        dk2 = float(np.max(np.abs(a_ - b_)) / np.max(np.abs(b_))); dk3 = float(np.max(np.abs(tfaint(key, 0.7 * WM) - 0.7 * TFH)) / np.max(np.abs(TFH)))
    F = {}
    for sm in ("S1", "S3"):
        G = {}
        for lad, TL, TH in (("R0", TNL0, TNH0), ("R2", TNL2, TNH2)):
            for B_ in (0.0, 1.0, 0.7):
                sL = st(modl(foot, TL + B_ * TFL, lad), sm, "all"); sH = st(modl(key, TH + B_ * TFH, lad), sm, "all"); c = compare(sL, sH); dH, aH = delta(sH); aL = amps(sL)
                if B_ == 0.0 and not MUT3:
                    j = J2[foot][sm][f"all_{lad}"]["all"]; dk1 = max(dk1, abs(c["chi2_L"] - j["chi2_L"]), abs(c["chi2_H"] - j["chi2_H"]))
                G[f"{lad}_B{B_:g}"] = dict(all=c, cls=cls(c), dH=dH, amps_H=aH, amps_L=aL, m_L=sL["m"].tolist(), m_H=sH["m"].tolist())
                W(f"  [{foot} {sm} {lad} B {B_:g}] chi2 L {c['chi2_L']:.1f} (p {c['pL']:.3f}), H {c['chi2_H']:.1f} (p {c['pH']:.3f}); dchi2 {c['dchi2']:+.1f}; D {c['D']:.2f} -> {cls(c)}; H A_in {aH['A_in']:.2f}+-{aH['sA_in']:.2f} A_O1 {aH['A_O1']:.2f}+-{aH['sA_O1']:.2f} delta {dH:+.2f}; L A_in {aL['A_in']:.2f} A_O1 {aL['A_O1']:.2f}+-{aL['sA_O1']:.2f} A_O2 {aL['A_O2']:.2f}+-{aL['sA_O2']:.2f}")
            for b in ("1", "0.7"): G[f"{lad}_B{b}"]["frozen"] = cl(G[f"{lad}_B{b}"]["dH"], G[f"{lad}_B0"]["dH"])
            W(f"    CLASS [{foot} {sm} {lad}] B 1: {G[f'{lad}_B1']['frozen']}; B 0.7: {G[f'{lad}_B0.7']['frozen']}")
        zero = np.zeros_like(TFL); s_tL = st(TFL, sm, "all"); s_tH = st(TFH, sm, "all"); s_lw = st(tfaint(key, WLOW), sm, "all"); s_lwL = st(tfaint(foot, WLOW), sm, "all")
        G["term"] = dict(L=s_tL["m"].tolist(), H=s_tH["m"].tolist(), H_lowest=s_lw["m"].tolist(), L_lowest=s_lwL["m"].tolist())
        W("     R        " + " ".join(f"{x:6.3f}" for x in RCEN)); W("     term L   " + " ".join(f"{x:6.2f}" for x in s_tL["m"])); W("     term H   " + " ".join(f"{x:6.2f}" for x in s_tH["m"])); W("     d        " + " ".join(f"{x:6.2f}" for x in s_tH["d"])); W("     sig      " + " ".join(f"{x:6.2f}" for x in np.sqrt(s_tH["var"])))
        W("     H lowest " + " ".join(f"{x:6.2f}" for x in s_lw["m"])); F[sm] = G
    RES3["foot"][foot] = F
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
if not MUT3:
    k1 = dk1 <= 1e-9; k2 = dk2 <= 1e-9; k3 = dk3 <= 1e-9; RES3["k"] = dict(K1=dk1, K2=dk2, K3=dk3); W(f"\nK1 B 0 vs SI2 chi2: {dk1:.1e} {'PASS' if k1 else 'FAIL'}; K2 one-type weights vs tnbr: {dk2:.1e} {'PASS' if k2 else 'FAIL'}; K3 linear: {dk3:.1e} {'PASS' if k3 else 'FAIL'}"); RES3["ok"] = bool(k1 and k2 and k3)
else:
    B0 = json.load(open(os.path.join(HERE3, "un1_results.json")))["foot"]["canonical"]["S1"]; A1 = RES3["foot"]["canonical"]["S1"]; bins = (RCEN > 0.4) & (RCEN <= 1.1)
    for m_ in "LH": W(f"MUTATE term {m_} sum O1: {np.sum(np.array(B0['term'][m_])[bins]):.3f} -> {np.sum(np.array(A1['term'][m_])[bins]):.3f}")
    W(f"MUTATE chi2 H R2 B1: {B0['R2_B1']['all']['chi2_H']:.3f} -> {A1['R2_B1']['all']['chi2_H']:.3f}")
tag = "_MUTATE" if MUT3 else ""; json.dump(RES3, open(os.path.join(HERE3, f"un1_results{tag}.json"), "w"), indent=1, default=float); open(os.path.join(HERE3, f"un1{tag}.out"), "w").write("\n".join(OUT3) + "\n")
