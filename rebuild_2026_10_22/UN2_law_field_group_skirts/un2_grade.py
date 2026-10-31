#!/usr/bin/env python3
"""UN2_law_field_group_skirts (FROZEN_CRITERIA.md): the law's catalogue field at R2 on SI2's stack; group skirts on S1 - S3.
    OMP_NUM_THREADS=1 nice -n 15 python3 un2_grade.py <kids_source_cache_dir> <work_dir>   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys
HU = os.path.dirname(os.path.abspath(__file__)); UA = os.path.join(os.path.dirname(HU), "UN1_unseen_neighbours", "un1_a1.py"); srca = open(UA).read(); cuta = "WS = {r: wz(r)"; assert srca.count(cuta) == 1
__file__ = UA; exec(compile(srca[:srca.index(cuta)], "un1a_head", "exec"))
YE, node_weights, YN, G_GROUP = N["YE"], N["node_weights"], N["YN"], N["G_GROUP"]; WMC = wz("cat"); O2B = (RCEN > 1.1) & (RCEN <= 2.6); R_ = {}
def tf_b(foot, Wm, ye):
    G_ = GT[foot]; Fh = np.einsum("lt,tnbd->lnbd", Wm, G_); Me = Wm @ MT; lidx = np.searchsorted(ZS, zbin); out = np.zeros((len(N["CEN"]["ra"]), 15))
    for c0 in range(0, len(SEL), 8000):
        s = SEL[c0:c0 + 8000]; pd_ = PD[s].astype(float); gd = np.clip((np.log(np.maximum(pd_, DGR[0])) - np.log(DGR[0])) / (np.log(DGR[1]) - np.log(DGR[0])), 0, len(DGR) - 1.001); d0 = gd.astype(np.int64); fd = (gd - d0)[:, None]; l = lidx[PJ[s]]; a, b, w = node_weights(ye[PJ[s]])
        ctr = (1 - w)[:, None] * ((1 - fd) * Fh[l, a, :, d0] + fd * Fh[l, a, :, d0 + 1]) + w[:, None] * ((1 - fd) * Fh[l, b, :, d0] + fd * Fh[l, b, :, d0 + 1]) + point_part(Me[l], pd_)
        for k in range(15): out[:, k] += np.bincount(PC[s], ctr[:, k], len(out))
    return out
def node_table(foot, dMs):
    tab = np.empty((len(LMG), len(YN), 15)); Rpe = EDGES * 1e6
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * np.log10(0.70 / H0N); lmc = lm + (-0.69 * lm70 + 6.63)
        for ni, ye in enumerate(YN):
            M, tail = meff_lens(foot, lm + dMs, lmc, 0.5 * 10 ** lm, float(ye)); tab[gi, ni] = bin_avg(Rpe, lambda R: AQ.delta_sigma(R, RG, M, tail))
    return tab
def own_f(foot, lad, ye):
    y = ye[idxS1]; base = town_per_lens(foot, "nz0", lM70[idxS1], z_g[idxS1], y)
    if lad == "R0": return base
    return np.where(RL[:, None], town_per_lens(foot, "nz2", lM70[idxS1], z_g[idxS1], y), base)
def law_f(foot, lad, yf, faint=False):
    ye = YE[foot]["c10"] * yf
    if lad == "R2": N["tix"], N["MBN_g"] = TIX2, MBN2
    tn = tnbr(foot, ye_gal=ye); N["tix"], N["MBN_g"] = TIX0, MBN0
    m = tn.copy(); m[:NLn] += own_f(foot, lad, ye)
    if faint: m += tf_b(foot, WMC, ye)
    return m
dk1 = dk2 = 0.0; J2 = json.load(open(os.path.join(RB3, "SI2_spec_isolated_colour", "si2_results.json")))["foot"]; OATS["nz0"] = {}; OATS["nz2"] = {}
for foot in FOOTS:
    N["tix"], N["MBN_g"] = TIX0, MBN0; key, TNH0 = build(foot); TOWN[(foot, "red")] = law_table(foot, SHIFT); TOWN[(key, "red")] = town_H(foot, dMs=SHIFT); TOWN[(foot, "nz0")] = node_table(foot, 0.0); TOWN[(foot, "nz2")] = node_table(foot, SHIFT)
    N["tix"], N["MBN_g"] = TIX2, MBN2; TNH2 = tnbr(key, node=0); TNL2 = tnbr(foot, node=0); N["tix"], N["MBN_g"] = TIX0, MBN0; TFH = tf(key, WMC); F = {}
    H = {"R0": (modl(key, TNH0, "R0"), modl(key, TNH0 + TFH, "R0")), "R2": (modl(key, TNH2, "R2"), modl(key, TNH2 + TFH, "R2"))}
    for sm in ("S1", "S3"):
        pb = primary(foot, "b", sample=sm); m0 = law_f(foot, "R0", 1.0); s0 = st(m0, sm, "all"); dk1 = max(dk1, float(np.max(np.abs(s0["m"] - pb["m"]) / np.sqrt(pb["var"])))); G = {}
        zm = law_f(foot, "R2", 0.0); sz = st(zm, sm, "all"); cz = compare(sz, st(H["R2"][0], sm, "all")); j = J2[foot][sm]["all_R2"]["all"]; dk2 = max(dk2, abs(cz["chi2_L"] - j["chi2_L"]))
        for lad, cases in (("R2", (("Y0", 1.0), ("Y2", 10 ** SHIFT))), ("R0", (("Y0", 1.0),))):
            for yn, yf in cases:
                for ft in (False, True):
                    sL = st(law_f(foot, lad, yf, ft), sm, "all"); sH = st(H[lad][int(ft)], sm, "all"); c = compare(sL, sH); aL, aH = amps(sL), amps(sH); nm = f"{lad}_{yn}_{'faint' if ft else 'nofaint'}"; G[nm] = dict(all=c, cls=cls(c), amps_L=aL, amps_H=aH, m_L=sL["m"].tolist())
                    W(f"  [{foot} {sm} {nm}] chi2 law field {c['chi2_L']:.1f} (p {c['pL']:.3f}), H {c['chi2_H']:.1f} (p {c['pH']:.3f}); dchi2 {c['dchi2']:+.1f}; D {c['D']:.2f} -> {cls(c)}; law A_in {aL['A_in']:.2f}+-{aL['sA_in']:.2f} A_O1 {aL['A_O1']:.2f}+-{aL['sA_O1']:.2f} A_O2 {aL['A_O2']:.2f}+-{aL['sA_O2']:.2f}; H A_O1 {aH['A_O1']:.2f}+-{aH['sA_O1']:.2f}")
        F[sm] = G
        if foot == FOOTS[0] and sm == "S1":
            mu = st(law_f(foot, "R2", 10.0), sm, "all"); o = F[sm]["R2_Y0_nofaint"]["m_L"]; ok = float(mu["m"][O2B].sum()) < float(np.array(o)[O2B].sum()); W(f"MUTATE y_e x 10, law sum 1.1-2.6 Mpc: {np.array(o)[O2B].sum():.3f} -> {mu['m'][O2B].sum():.3f}: {'PASS' if ok else 'FAIL'}"); R_["mutate"] = ok
    R_[foot] = F
    if foot == "canonical":
        c0, c2 = F["S1"]["R2_Y0_nofaint"]["cls"], F["S1"]["R2_Y2_nofaint"]["cls"]; lab = c0 if c0 == c2 else f"FIELD-SCALE-DEPENDENT (Y0 {c0}, Y2 {c2})"; R_["Q1_class"] = lab; W(f"Q1 FROZEN CLASS [canonical S1 R2]: {lab}")
        # Q2
        gu, gc = np.unique(G_GROUP[G_GROUP > 0], return_counts=True); mult = np.zeros(len(G_GROUP), int); mult[G_GROUP > 0] = gc[np.searchsorted(gu, G_GROUP[G_GROUP > 0])]; Lall = SETL; notS3 = ~inS3; mH2 = H["R2"][0]; R_["Q2"] = {}
        for th in (5, 10):
            hit = (PD >= 1.0) & (PD <= 2.5) & (mult[PJ] >= th) & (PC < NLn); sk = np.zeros(NLn, bool); sk[np.unique(PC[hit])] = True; A = Lall[notS3 & sk]; B_ = Lall[notS3 & ~sk]; C = Lall[inS3]; assert len(A) + len(B_) + len(C) == NLn
            Am = lambda g: amps(stack([(g, +1, mH2), (SETS["I1"], -1, mH2)])); a, b, c = Am(A), Am(B_), Am(C); dif = a["A_O1"] - b["A_O1"]; sd = math.hypot(a["sA_O1"], b["sA_O1"]); nd = dif / sd; dno = (b["A_O1"] - 1) / b["sA_O1"]
            q = "SKIRT DRIVEN" if nd >= 2 and abs(dno) <= 1 else "NOT SKIRT DRIVEN" if nd < 1 else "UNDECIDED"; R_["Q2"][str(th)] = dict(n=[len(A), len(B_), len(C)], frac_S1mS3=float(sk[notS3].mean()), frac_S3=float(sk[inS3].mean()), A=a, B=b, C=c, diff_sig=nd, dno=dno, cls=q)
            W(f"Q2 mult >= {th}: S1-S3 with skirt {len(A)} (frac {sk[notS3].mean():.3f}), without {len(B_)}, S3 {len(C)} (frac with skirt {sk[inS3].mean():.3f}). A_O1 skirt {a['A_O1']:.2f}+-{a['sA_O1']:.2f}, none {b['A_O1']:.2f}+-{b['sA_O1']:.2f}, S3 {c['A_O1']:.2f}+-{c['sA_O1']:.2f}; diff {nd:+.2f} sigma; none delta {dno:+.2f} -> {q}")
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
k1 = dk1 <= 1e-6; k2 = dk2 <= 1e-9; R_["k"] = dict(K1=dk1, K2=dk2, ok=bool(k1 and k2)); W(f"K1 node table vs primary b, max |d model|/sigma: {dk1:.1e} {'PASS' if k1 else 'FAIL'}; K2 y_e 0 at R2 vs SI2: {dk2:.1e} {'PASS' if k2 else 'FAIL'}; K3 asserted")
json.dump(R_, open(os.path.join(HU, "un2_results.json"), "w"), indent=1, default=float); open(os.path.join(HU, "un2.out"), "w").write("\n".join(OUT3) + "\n")
