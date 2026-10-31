#!/usr/bin/env python3
"""SI2_spec_isolated_colour (criteria 9f87d6aef2): SI1's models by lens colour and on S2's red stellar-mass ladder, both models, spectroscopic samples.
    OMP_NUM_THREADS=1 nice -n 15 python3 si2_grade.py <kids_source_cache_dir> <work_dir> [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math
HERE2 = os.path.dirname(os.path.abspath(__file__)); RB2 = os.path.dirname(HERE2); SI1F = os.path.join(RB2, "SI1_spec_isolated_route_e", "si1_grade.py")
MUT2 = "--mutate" in sys.argv; sys.argv = [SI1F] + [a for a in sys.argv[1:] if not a.startswith("--")]
src = open(SI1F).read(); cut = 'RES = dict(criteria="ed3c0f8bb1"'; assert src.count(cut) == 1; __file__ = SI1F; exec(compile(src[:src.index(cut)], "si1_head", "exec"))
OUT2 = []
def Q(s): print(s, flush=True); OUT2.append(str(s))
SHIFT = 0.295; stack, town_per_lens, meff_lens, lMa, valid, kk, inb, read_fits_cols, DKB, NG, lMb_g = (N[k] for k in ("stack", "town_per_lens", "meff_lens", "lMa", "valid", "kk", "inb", "read_fits_cols", "DKB", "NG", "lMb_g"))
_lh = read_fits_cols(os.path.join(DKB, "KiDS_DR4_brightsample_LePhare.fits"), ["MAG_ABS_u", "MAG_ABS_r"], rowmask=inb); _ur = _lh["MAG_ABS_u"].astype("f8") - _lh["MAG_ABS_r"].astype("f8"); del _lh
UR_g = np.full(NG, np.nan); UR_g[valid] = _ur[kk[valid]]; red_g = valid & (UR_g > 2.0); blue_g = valid & ~(UR_g > 2.0)
if MUT2: red_g, blue_g = blue_g.copy(), red_g.copy()
RL = red_g[idxS1]; BL = blue_g[idxS1]; ok_c = RL | BL; NLn = len(idxS1); inS3 = N["inS3"]
Q(f"\nSI2 colour split on spectroscopic lenses; u-r > 2.0 red; R2 red +{SHIFT} dex; kappa = 1/2 FITTED; footings never pooled; not theory closed" + (" [MUTATE labels swapped]" if MUT2 else ""))
RES2 = dict(criteria="9f87d6aef2", mutate=MUT2, foot={}, k={}); OK2 = True
k1 = int(valid.sum()) == int(np.isfinite(UR_g).sum()) ; OK2 &= k1
fr1 = float(RL.sum() / max(ok_c.sum(), 1)); fr3 = float(RL[inS3].sum() / max(ok_c[inS3].sum(), 1)); Q(f"K1 colour for every LePhare match: {'PASS' if k1 else 'FAIL'} ({int(valid.sum()):,}); red fraction S1 {fr1:.3f} ({int(RL.sum())}/{int(ok_c.sum())}), S3 {fr3:.3f} ({int(RL[inS3].sum())}/{int(ok_c[inS3].sum())})"); RES2["k"].update(K1=k1, red_S1=fr1, red_S3=fr3)
lMs_g = lMs_nat(lMa, z_g); sh_g = np.where(red_g, SHIFT, 0.0); lMb2 = np.log10(10 ** lMb_g + 10 ** lMs_g * (10 ** sh_g - 1))
TIX0, MBN0 = N["tix"].copy(), N["MBN_g"].copy(); TIX2 = np.clip(np.round((lMb2 - LMB_T[0]) / 0.05).astype(int), 0, len(LMB_T) - 1); MBN2 = 10 ** lMb2
OATS["red"] = {}
def law_table(foot, dMs):
    tab = np.empty((len(LMG), 15)); Rpe = EDGES * 1e6
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * np.log10(0.70 / H0N); lmc = lm + (-0.69 * lm70 + 6.63); M, tail = meff_lens(foot, lm + dMs, lmc, 0.5 * 10 ** lm, 0.0); tab[gi] = bin_avg(Rpe, lambda R: AQ.delta_sigma(R, RG, M, tail))
    return np.stack([tab, tab], 1)
def own(key, lad):
    """T_own for all lenses (S1 superset) at the ladder step."""
    ye = np.zeros(NLn); base = town_per_lens(key, "central", lM70[idxS1], z_g[idxS1], ye)
    if lad == "R0" or not RL.any(): return base
    alt_ = town_per_lens(key, "red", lM70[idxS1], z_g[idxS1], ye); return np.where(RL[:, None], alt_, base)
def modl(key, tn, lad):
    m = tn.copy(); m[:NLn] += own(key, lad); return m
SETL = SETS["L"]
def st(mod, sample, sub, raw=False):
    Lc = SETL[inS3] if sample == "S3" else SETL; sel = {"all": np.ones(NLn, bool), "red": RL, "blue": BL}[sub][Lc]; Lc = Lc[sel]; Ic = SETS["R"] if raw else (SETS["I3"] if sample == "S3" else SETS["I1"])
    return stack([(Lc, +1, mod), (Ic, -1, mod)])
def row(lab, sL, sH):
    c = compare(sL, sH); rin = compare(sL, sH, RANGE["in"]); rout = compare(sL, sH, RANGE["out"]); aH = amps(sH); aL = amps(sL); g = cls(c)
    Q(f"   {lab:22s} chi2 L {c['chi2_L']:6.1f} (p {c['pL']:.3f}), H {c['chi2_H']:6.1f} (p {c['pH']:.3f}); dchi2 {c['dchi2']:+6.1f}; D {c['D']:.2f} -> {g}; inner {rin['dchi2']:+.1f}, outer {rout['dchi2']:+.1f}; A_in H {aH['A_in']:.2f}+-{aH['sA_in']:.2f}, L {aL['A_in']:.2f}+-{aL['sA_in']:.2f}; A_O1 H {aH['A_O1']:.2f}+-{aH['sA_O1']:.2f}, L {aL['A_O1']:.2f}+-{aL['sA_O1']:.2f}")
    return dict(all=c, inner=rin, outer=rout, cls=g, amps_H=aH, amps_L=aL, d=sL["d"].tolist(), sig=np.sqrt(sL["var"]).tolist(), m_L=sL["m"].tolist(), m_H=sH["m"].tolist())
J1 = None if MUT2 else json.load(open(os.path.join(RB2, "SI1_spec_isolated_route_e", "si1_results.json")))["foot"]; dk2 = dk3 = 0.0
for foot in FOOTS:
    N["tix"], N["MBN_g"] = TIX0, MBN0; key, TNH0 = build(foot); TNL0 = N["TN"][(foot, "a")]; F = {}
    TOWN[(foot, "red")] = law_table(foot, SHIFT); TOWN[(key, "red")] = town_H(foot, dMs=SHIFT)
    N["tix"], N["MBN_g"] = TIX2, MBN2; TNH2 = tnbr(key, node=0); TNL2 = tnbr(foot, node=0); N["tix"], N["MBN_g"] = TIX0, MBN0
    # the neighbour halo table is indexed by M_b, so shifted neighbours read their own row
    mL0, mH0, mL2, mH2 = modl(foot, TNL0, "R0"), modl(key, TNH0, "R0"), modl(foot, TNL2, "R2"), modl(key, TNH2, "R2")
    for sm in ("S3", "S1"):
        Q(f"\n  [{foot} {sm}]"); G = {}
        G["all_R0"] = row("all, R0 (K2)", st(mL0, sm, "all"), st(mH0, sm, "all"))
        if not MUT2:
            for nm in ("chi2_L", "chi2_H"): dk2 = max(dk2, abs(G["all_R0"]["all"][nm] - J1[foot][sm]["all"][nm]))
        G["blue_R0"] = row("blue, R0", st(mL0, sm, "blue"), st(mH0, sm, "blue")); G["red_R0"] = row("red, R0", st(mL0, sm, "red"), st(mH0, sm, "red")); G["red_R2"] = row("red, R2", st(mL2, sm, "red"), st(mH2, sm, "red")); G["all_R2"] = row("ALL, R2", st(mL2, sm, "all"), st(mH2, sm, "all"))
        G["all_R2_raw"] = row("all, R2, raw L-R", st(mL2, sm, "all", raw=True), st(mH2, sm, "all", raw=True))
        P_ = lambda x: " ".join(f"{v:6.2f}" for v in x); Q("     R    " + " ".join(f"{x:6.3f}" for x in RCEN)); Q("     d    " + P_(G["all_R2"]["d"])); Q("     sig  " + P_(G["all_R2"]["sig"])); Q("     L R2 " + P_(G["all_R2"]["m_L"])); Q("     H R2 " + P_(G["all_R2"]["m_H"]))
        for sub in ("blue_R0",): Q(f"     blue d   " + P_(G[sub]["d"])); Q(f"     blue sig " + P_(G[sub]["sig"])); Q(f"     blue L   " + P_(G[sub]["m_L"])); Q(f"     blue H   " + P_(G[sub]["m_H"]))
        F[sm] = G
        if sm == "S3":
            Lc = SETL[inS3]; WW_ = MEAS["WW"]; blk = lambda ss: stack([(Lc[ss[Lc]], +1, mH0)])["m"] * WW_[Lc[ss[Lc]]].sum(0); wa = WW_[Lc[ok_c[Lc]]].sum(0); ma = stack([(Lc[ok_c[Lc]], +1, mH0)])["m"]; dk3 = max(dk3, float(np.max(np.abs((blk(RL) + blk(BL)) / wa / ma - 1))))
    RES2["foot"][foot] = F
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
if not MUT2:
    k2 = dk2 <= 1e-9; k3 = dk3 <= 1e-9; OK2 &= k2 and k3; Q(f"\nK2 R0, no split reproduces SI1 (chi2 H, L, S3 and S1, both footings): {dk2:.1e}: {'PASS' if k2 else 'FAIL'}; K3 blue + red = all, model stack: {dk3:.1e}: {'PASS' if k3 else 'FAIL'}"); RES2["k"].update(K2=dk2, K3=dk3)
    F = RES2["foot"]["canonical"]; s1, s3 = F["S1"]["all_R2"], F["S3"]["all_R2"]
    gone = s1["cls"] != "LAW PREFERRED" and s3["cls"] != "LAW PREFERRED" and s1["all"]["pH"] >= 0.05 and s3["all"]["pH"] >= 0.05; rem = (s1["cls"] == "LAW PREFERRED" and s1["all"]["pH"] < 0.05) or (s3["cls"] == "LAW PREFERRED" and s3["all"]["pH"] < 0.05)
    lab = "LENSING TENSION GONE ON CLEAN LENSES" if gone else "TENSION REMAINS" if rem else "MIXED"; lab = lab if OK2 else f"NOT DECIDED ({lab})"; RES2["combined"] = lab; Q(f"COMBINED READING [canonical, ALL at R2]: {lab}")
else:
    B0 = json.load(open(os.path.join(HERE2, "si2_results.json")))["foot"]["canonical"]["S1"]["red_R2"]["all"]["chi2_H"]; A1 = RES2["foot"]["canonical"]["S1"]["red_R2"]["all"]["chi2_H"]; Q(f"MUTATE labels swapped: red R2 chi2 H {B0:.2f} -> {A1:.2f}: {'PASS' if abs(A1 - B0) > 1e-3 else 'FAIL'}")
tag = "_MUTATE" if MUT2 else ""; json.dump(RES2, open(os.path.join(HERE2, f"si2_results{tag}.json"), "w"), indent=1, default=float); open(os.path.join(HERE2, f"si2{tag}.out"), "w").write("\n".join(OUT2) + "\n")
