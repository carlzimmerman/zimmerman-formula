#!/usr/bin/env python3
"""SI3 AMENDMENT A1 (post-result, reported only; changes no frozen line): Delta_m = L - I_m, with I_m the frozen I points matched to the lenses on source coverage. si3_grade.py's own text up to its lines.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 si3_a1_grade.py <work_dir>
kappa = 1/2 FITTED; footings never pooled; cold dark energy is never a particle."""
import os, sys
AH = os.path.dirname(os.path.abspath(__file__)); SG = os.path.join(AH, "si3_grade.py"); gsrc = open(SG).read(); CUT = 'VARS = (("D", "Delta = L - I"), ("L", "raw L"))'; assert gsrc.count(CUT) == 1
__file__ = SG; exec(compile(gsrc[:gsrc.index(CUT)], "si3_head", "exec"))
sys.path.insert(0, AH); from si3_a1_measure import a1_nbar, NC, CEDGES
OUT.clear(); Q("SI3 AMENDMENT A1: post-result, reported only. The frozen verdict stays NO VERDICT. kappa = 1/2 FITTED; footings never pooled"); Q("frozen checks recomputed in this run: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in KOK.items()))
A = [dict(np.load(os.path.join(WORK, f"si3_a1_{r}.npz"))) for r in ("north", "south")]; AH_ = {}; dk = 0.0
for s in SAMPLES:
    AH_[s] = {k: A[0][f"I_{s}_{k}"] + A[1][f"I_{s}_{k}"] for k in ("WG", "WX", "WW", "NN", "n")}
    for k in ("WG", "WX", "WW", "NN"):
        ref = HOLE[f"I_{s}"][k]; dk = max(dk, float(np.max(np.abs(AH_[s][k].sum(3) - ref)) / np.max(np.abs(ref))))
kA1 = dk <= 1e-9; Q(f"A1 check: c bins sum to the frozen I sums, max relative |d| {dk:.1e}: {'PASS' if kA1 else 'FAIL'}"); RES = dict(lane="SI3_nested_isolation AMENDMENT A1", post_result=True, frozen_verdict="NO VERDICT (hole-term check failed)", check_c_bins_sum=dk, ok=kA1)
# coverage of real lenses
PL_ = np.load(os.path.join(DATA, "cfg110_perlens.npz")); NNL = PL_["NN"].sum(1); ldec = np.array(NF["LN"]["dec"], "f8"); lzz = np.array(NF["LN"]["z"], "f8"); lMg = np.array(NF["LN"]["Mgal"], "f8"); NBAR, LCELL, FREG = a1_nbar(lzz, lMg, LBIN, ldec, NNL)
cL = NNL / (NBAR[LCELL] * np.where(ldec > -15.0, FREG["north"], FREG["south"])); jL = np.digitize(cL, CEDGES) - 1; RES["field_factors"] = FREG
# plain weight ratios, from the frozen sums (the table that prompted this amendment)
cats_ = np.load(os.path.join(WORK, "si3_cats.npz")); RAT = {}; WM = {}; Q("\nsource weight per centre, mean over the range: lens/I, lens/R, I/R; then lens/I_m after matching. Coverage c: mean and 16, 50, 84 % points, lenses then I points")
for s in SAMPLES:
    idx = SAMP[s] & OKL; nl = np.bincount(LBIN[idx], minlength=4); twl = LSUM[s]["sw"].sum(0) / nl[:, None]; nR = np.bincount(LBIN[cats_[f"R_{s}_li"]], minlength=4); twi = HOLE[f"I_{s}"]["WW"].sum((0, 1)) / NI[s][:, None]; twr = HOLE[f"R_{s}"]["WW"].sum((0, 1)) / nR[:, None]
    nL_bj = np.zeros((4, NC)); np.add.at(nL_bj, (LBIN[idx], jL[idx]), 1.0); nI_bj = AH_[s]["n"].sum((0, 1)); fL = nL_bj / nL_bj.sum(1, keepdims=True); fI = nI_bj / nI_bj.sum(1, keepdims=True)
    w = np.where(fI > 0, fL / np.where(fI > 0, fI, 1.0), 0.0); WM[s] = w; unm = float(np.sum(nL_bj[nI_bj == 0]) / nL_bj.sum())
    def wsum(k): return np.einsum("hpbjk,bj->hpbk", AH_[s][k], w)
    HOLE[f"M_{s}"] = {k: wsum(k) for k in ("WG", "WX", "WW", "NN")}; twm = HOLE[f"M_{s}"]["WW"].sum((0, 1)) / np.sum(nI_bj * w, axis=1)[:, None]
    with np.errstate(all="ignore"): r1, r2, r3, r4 = twl / twi, twl / twr, twi / twr, twl / twm
    RAT[s] = {lab: dict(L_over_I=float(np.mean(r1[RAN[lab]])), L_over_R=float(np.mean(r2[RAN[lab]])), I_over_R=float(np.mean(r3[RAN[lab]])), L_over_Im=float(np.mean(r4[RAN[lab]]))) for lab in ("in", "O1", "O2")}
    centres = 0.5 * (CEDGES[:-1] + np.minimum(CEDGES[1:], 2.4)); cumI = np.cumsum(nI_bj.sum(0)) / nI_bj.sum(); pc = [float(CEDGES[1:][np.searchsorted(cumI, q)]) for q in (0.16, 0.5, 0.84)]; meanI = float(np.sum(nI_bj.sum(0) * centres) / nI_bj.sum()); cs = cL[idx]; plc = [float(x) for x in np.percentile(cs, [16, 50, 84])]
    RAT[s].update(c_lens=dict(mean=float(cs.mean()), p16_50_84=plc), c_I_binned=dict(mean=meanI, upper_edge_p16_50_84=pc), unmatched_lens_fraction=unm, N_eff_fraction_of_I=float(np.sum(nI_bj * w) ** 2 / np.sum(nI_bj * w * w) / nI_bj.sum()))
    Q(f"  {s:8s} O2: L/I {RAT[s]['O2']['L_over_I']:.3f}, L/R {RAT[s]['O2']['L_over_R']:.3f}, I/R {RAT[s]['O2']['I_over_R']:.3f}, L/I_m {RAT[s]['O2']['L_over_Im']:.3f};  in: L/I {RAT[s]['in']['L_over_I']:.3f}, L/R {RAT[s]['in']['L_over_R']:.3f}, L/I_m {RAT[s]['in']['L_over_Im']:.3f};  c lens mean {cs.mean():.3f}, {plc[0]:.2f}/{plc[1]:.2f}/{plc[2]:.2f}; c I mean {meanI:.3f}, bin tops {pc[0]:.2f}/{pc[1]:.2f}/{pc[2]:.2f}; unmatched lens fraction {unm:.1e}; effective I fraction {RAT[s]['N_eff_fraction_of_I']:.2f}")
RES["ratios"] = RAT; del cats_
# nulls on I_m, then the lines
WXL = -np.load(os.path.join(DATA, "cfg116_perlens.npz"))["WX"]; NUL = {}
for s in SAMPLES:
    dl, djl = ratio(psum(SAMP[s], WXL), LSUM[s]["sw"], fdat); dh, djh = ratio(*hsum("M_" + s, "WX"), fdat); d_, dj_ = dl - dh, djl - djh; var_ = JKF * np.sum((dj_ - dj_.mean(0)) ** 2, axis=0); bk = blocks_J(d_, dj_, var_, RALL); c4 = chi2b(bk, d_); n4 = sum(x[3] for x in bk)
    da, dja = ratio(*hsum("M_" + s, half=0), fdat); db, djb = ratio(*hsum("M_" + s, half=1), fdat); d_, dj_ = da - db, dja - djb; var_ = JKF * np.sum((dj_ - dj_.mean(0)) ** 2, axis=0); bk = blocks_J(d_, dj_, var_, RALL); c5 = chi2b(bk, d_); n5 = sum(x[3] for x in bk)
    NUL[s] = dict(cross_chi2=c4, cross_n=n4, cross_p=float(stats.chi2.sf(c4, n4)), halves_chi2=c5, halves_n=n5, halves_p=float(stats.chi2.sf(c5, n5)))
    d0, dj0 = ratio(LSUM[s]["sg"], LSUM[s]["sw"], fdat); dm, djm = ratio(*hsum("M_" + s), fdat); d_, dj_ = d0 - dm, dj0 - djm; DV[(s, "M")] = (d_, dj_, JKF * np.sum((dj_ - dj_.mean(0)) ** 2, axis=0))
del WXL; RES["nulls_on_I_m"] = NUL; Q("\nnulls on I_m: " + "; ".join(f"{s} cross {NUL[s]['cross_chi2']:.1f}/{NUL[s]['cross_n']} p {NUL[s]['cross_p']:.3g}, halves {NUL[s]['halves_chi2']:.1f}/{NUL[s]['halves_n']} p {NUL[s]['halves_p']:.3g}" for s in SAMPLES))
F0 = json.load(open(os.path.join(AH, "si3_results.json")))["lines"]; TAB = {}
for foot in FOOTS:
    TAB[foot] = {"M": {}, "D": F0[foot]["D"]}
    for rg in RUNGS:
        TAB[foot]["M"][rg] = {s: line(foot, rg, s, "M") for s in SAMPLES}
        Q(f"\n=== [{foot}] Delta_m = L - I_m (post-result), {rg}; frozen Delta in brackets. dchi2 = chi2(route E) - chi2(law), no fitted parameter")
        for s in SAMPLES:
            o = TAB[foot]["M"][rg][s]; c = o["all"]; f = F0[foot]["D"][rg][s]["all"]; t = o["two_halo"]; e = o.get("route_E_to_r_ta"); lb_ = label(c["dchi2"], c["D"], c["p_H"]); o["label"] = lb_
            Q(f"  {s:8s} chi2 L {c['chi2_L']:7.1f} (p {c['p_L']:.2g})  H {c['chi2_H']:7.1f} (p {c['p_H']:.2g})  dchi2 {c['dchi2']:+8.1f} [{f['dchi2']:+.1f}]  D {c['D']:5.2f} [{f['D']:.2f}]  Q {c['Q']:+6.2f} [{f['Q']:+.2f}] +- {2 / c['D']:.2f} (jack {o['sQ_jack']:.2f})  {c['cls']} [{f['cls']}]; label {lb_}; inner {o['inner']['dchi2']:+.1f}, outer {o['outer']['dchi2']:+.1f}")
            al, ah = o["amps_L"], o["amps_H"]; Q(f"           law A_in {al['A_in']:.2f}+-{al['sA_in']:.2f} A_O1 {al['A_O1']:.2f}+-{al['sA_O1']:.2f} A_O2 {al['A_O2']:.2f}+-{al['sA_O2']:.2f} | route E A_in {ah['A_in']:.2f}+-{ah['sA_in']:.2f} A_O1 {ah['A_O1']:.2f}+-{ah['sA_O1']:.2f} A_O2 {ah['A_O2']:.2f}+-{ah['sA_O2']:.2f}")
            Q(f"           (reported) X53 two-halo: L2H {t['chi2_L']:.1f}, H2H {t['chi2_H']:.1f}, dchi2 {t['dchi2']:+.1f}, D {t['D']:.2f}, {t['cls']}; halo to r_ta: dchi2 {e['dchi2']:+.1f}, D {e['D']:.2f}, {e['cls']}")
LADDER = {}
for foot in FOOTS:
    LADDER[foot] = {}
    for rg in RUNGS:
        r = TAB[foot]["M"][rg]; LADDER[foot][rg] = {f"S10-{s}": dict(d=r["S10"]["all"]["Q"] - r[s]["all"]["Q"], s=float(math.sqrt(JKF * np.sum(((r["S10"]["_qp"] - r[s]["_qp"]) - (r["S10"]["_qp"] - r[s]["_qp"]).mean()) ** 2)))) for s in ("S_strict", "S_x300")}
    Q(f"\nQ(S10) - Q(sample) on Delta_m, paired jackknife [{foot}]: " + "; ".join(f"{k}: " + ", ".join(f"{a} {b['d']:+.2f}+-{b['s']:.2f}" for a, b in x.items()) for k, x in LADDER[foot].items()))
IRM = {}; Q("\nHole's own size with I_m: inverse-variance mean, jackknife error, Msun/pc^2 native")
for s in SAMPLES:
    di, dji = ratio(*hsum("M_" + s), fdat); dr, djr = ratio(*hsum("R_" + s), fdat); dd, djd, vard = dvec(s, "M"); vi = JKF * np.sum(((dji - djr) - (dji - djr).mean(0)) ** 2, axis=0); IRM[s] = {}
    for lab in ("O1", "O2"):
        def mean_of(dd_, djj, va):
            sel = RAN[lab] & np.isfinite(dd_) & (va > 0); w_ = np.where(sel, 1 / np.where(va > 0, va, 1), 0.0); m_ = float(np.sum(w_ * dd_) / np.sum(w_)); mj_ = np.sum(w_[None] * djj, axis=(1, 2)) / np.sum(w_); return m_, float(math.sqrt(JKF * np.sum((mj_ - mj_.mean()) ** 2)))
        IRM[s][lab] = dict(I_m_minus_R=mean_of(di - dr, dji - djr, vi), Delta_m=mean_of(dd, djd, vard))
    Q(f"  {s:8s} " + "  ".join(f"{lab}: I_m-R {IRM[s][lab]['I_m_minus_R'][0]:+.3f}+-{IRM[s][lab]['I_m_minus_R'][1]:.3f}, L-I_m {IRM[s][lab]['Delta_m'][0]:+.3f}+-{IRM[s][lab]['Delta_m'][1]:.3f}" for lab in ("O1", "O2")))
RES["hole_size_I_m"] = IRM; RES["ladder"] = LADDER
# Argon's lines on Delta_m, printed for reading; its text's own function
exec(compile(gsrc[gsrc.index("def argon("):gsrc.index('if HAVE:\n    RES["argon"]')], "si3_argon", "exec"))
RES["argon"] = dict(graded=argon("M", "all"), two_halo=argon("M", "two_halo"))
for nm, A_ in (("graded statistic", RES["argon"]["graded"]), ("X53 two-halo line", RES["argon"]["two_halo"])):
    Q(f"\nArgon's lines at R2 on Delta_m (post-result), canonical, on the {nm}:")
    for s in ("S10", "S30", "S_strict"): Q(f"  {s}: dchi2 {A_[s]['dchi2']:+.1f}, band {A_[s]['band']}: {A_[s]['score']}")
    Q(f"  S_strict A_O1 data/route E {A_['A_O1_data_over_routeE']['value']:.2f}+-{A_['A_O1_data_over_routeE']['err']:.2f}: {A_['A_O1_data_over_routeE']['score']}; A_O2 data/law {A_['A_O2_data_over_law']['value']:.2f}+-{A_['A_O2_data_over_law']['err']:.2f}: {A_['A_O2_data_over_law']['score']}; pass line on route E's reading {A_['pass_line']['met_on_routeE_reading']}; fail line (D >= 5, dchi2 >= +25) {A_['fail_line']['met']}; falsifier (above +30) {A_['falsifier_above_30']}")
Q("\nThe frozen verdict stays NO VERDICT. This amendment cannot change it.")
for foot in FOOTS:
    for rg in RUNGS:
        for s in SAMPLES: TAB[foot]["M"][rg][s].pop("_qp", None)
    TAB[foot].pop("D")
RES["lines_Delta_m"] = TAB; Q(f"runtime {time.time() - T00:.0f} s; peak RSS {rss():.2f} GB")
json.dump(RES, open(os.path.join(AH, "si3_a1_results.json"), "w"), indent=1, default=float); open(os.path.join(AH, "si3_a1.out"), "w").write("\n".join(OUT) + "\n")
