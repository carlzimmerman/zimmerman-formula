"""CFG183 main run and MUTATE=k (k=1..8). Exit: main 0 if internal controls pass; MUTATE 1 = bites, 0 = does not."""
import os, sys, json, math
import numpy as np
import CFG183_common as C
from CFG183_common import M, pr

MUT = int(os.environ.get("MUTATE", "0"))

# ---- README targets (READ from CFG175_README.md before any run; not blind predictions)
T_K = [(1.007, .616, 1.465), (4.335, 3.547, 5.267), (5.655, 4.636, 6.876), (6.261, 5.126, 7.627), (6.470, 5.294, 7.887), (10.19, 8.23, 12.60)]
F_K = [None, (2.109, 1.596, 2.705), (3.096, 2.423, 3.887), (3.565, 2.808, 4.462), (3.730, 2.942, 4.665), (6.845, 5.407, 8.611)]
R_K = [None, (.621, .289, 1.006), (1.257, .822, 1.766), (1.567, 1.076, 2.144), (1.676, 1.165, 2.279), (3.829, 2.873, 4.994)]
T_R = [(.377, .227, .538), (1.528, 1.324, 1.744), (1.947, 1.723, 2.186), (2.140, 1.906, 2.390), (2.207, 1.969, 2.460), (3.391, 3.090, 3.710)]
RT_T = [2.67, 2.84, 2.90, 2.93, 2.93, 3.00]
STAT_T = ["allowed"] + ["excluded"] * 5
STAT_F = ["over", "allowed", "allowed", "allowed", "allowed", "excluded"]
STAT_R = ["over"] + ["allowed"] * 5

def setup(mut):
    S, AS, K = C.load("inc_star_deg")
    lawT_K = C.make_law("T"); lawT_R = C.make_law("T")
    if mut == 1: lawT_K = lawT_R = C.make_law("flat")
    if mut == 2: lawT_K = lawT_R = C.make_law("rival")
    if mut == 3: lawT_K = lawT_R = C.make_law("Trecip")
    if mut == 4: lawT_K = lawT_R = C.make_law("EdS")
    if mut == 5: lawT_K = C.make_law("Tconst", z=float(np.median(K.z)))
    if mut == 6:
        S.V = S.V * 10 ** 0.3; S.eV = S.eV * 10 ** 0.3
    if mut == 8:
        rng = np.random.default_rng(183); p = rng.permutation(len(S.z))
        S.sig = S.sig[p]; S.esig = S.esig[p]; S.grad2 = S.grad2[p]
    return S, AS, K, lawT_K, lawT_R

def analyse(mut):
    S, AS, K, lawK, lawR = setup(mut)
    R = {}
    for nm, s in (("s1", 1.0), ("s0", 0.0)):
        c = C.cell(S, AS, s, 0.67, lawK)
        cr = C.cell(S, AS, s, 0.67, None)
        R["dec_" + nm] = {"flat": c["flat"], "rival": cr["H"], "T": c["H"]}
    R["be_K"] = {"flat": [], "rival": [], "T": []}
    R["be_R"] = {"flat": [], "rival": [], "T": []}
    for s in C.S_PUB:
        for smp, tag, law in ((S, "be_K", lawK), (K, "be_R", lawR)):
            R[tag]["flat"].append(C.breakeven(lambda m: C.cell(smp, AS, s, m, None)["flat"]))
            R[tag]["rival"].append(C.breakeven(lambda m: C.cell(smp, AS, s, m, None)["H"]))
            R[tag]["T"].append(C.breakeven(lambda m: C.cell(smp, AS, s, m, law)["H"]))
    R["stat"] = {L: [C.status(b) for b in R["be_K"][L]] for L in ("flat", "rival", "T")}
    R["fit_K"] = {}; R["fit_R"] = {}
    for L, law in (("flat", None), ("rival", None), ("T", lawK)):
        which = "flat" if L == "flat" else "H"
        R["fit_K"][L] = C.s_root(lambda s: C.cell(S, AS, s, 0.67, law)[which])
        lawr = lawR if L == "T" else None
        R["fit_R"][L] = C.s_root(lambda s: C.cell(K, AS, s, 0.67, lawr)[which])
    R["RT"] = [(t["mu"] / r["mu"]) if (t["mu"] and r["mu"]) else None for t, r in zip(R["be_K"]["T"], R["be_R"]["T"])]
    stT = {s: R["stat"]["T"][i] for i, s in enumerate(C.S_PUB)}
    R["sentence"] = C.headline_sentence(stT)
    zT = R["dec_s1"]["T"][0] / R["dec_s1"]["T"][1]
    R["strong"] = bool(all(stT[s] == "excluded" for s in (1.0, 1.42, 1.62, 1.69, 3.0)) and zT > 3)
    R["signature"] = (tuple(R["stat"]["T"]), R["sentence"], R["strong"])
    R["R0"] = (R["dec_s1"]["T"][0] - R["dec_s1"]["flat"][0], R["dec_s1"]["T"][1])
    return R

def within(x, ref, rel, ab):
    return abs(x - ref) <= max(rel * abs(ref), ab)

def controls():
    out = {}
    z = np.array([0.85, 1.5, 2.5])
    out["C1_0.3111"] = np.log10(C.t_ratio(z, 0.3111)).tolist()
    out["C1_0.315"] = np.log10(C.t_ratio(z[:2], 0.315)).tolist()
    out["C1_quad_vs_closed"] = float(max(abs(float(C.t_ratio_quad(zz, 0.3111)) - float(C.t_ratio(zz, 0.3111))) for zz in z))
    S, AS, K = C.load()
    c = C.cell(S, AS, 1.0, 0.67, C.make_law("T"))
    out["C3_anchor_diff_dex"] = float(c["r"]["H"]["anchor"] - c["r"]["flat"]["anchor"])
    ce = C.cell(S, AS, 1.0, 0.67, C.make_law("flat"))
    out["Cimp_E1_H_minus_flat"] = float(abs(ce["H"][0] - ce["flat"][0]))
    cr = C.cell(S, AS, 1.0, 0.67, C.make_law("rival"))
    cr0 = C.cell(S, AS, 1.0, 0.67, None)
    out["Cimp_rival_replay"] = float(abs(cr["H"][0] - cr0["H"][0]))
    out["C2_dec_flat_rival"] = [cr0["flat"][0], cr0["H"][0]]
    be_f = C.breakeven(lambda m: C.cell(S, AS, 1.0, m, None)["flat"])
    be_r = C.breakeven(lambda m: C.cell(S, AS, 1.0, m, None)["H"])
    bk_f = C.breakeven(lambda m: C.cell(K, AS, 1.0, m, None)["flat"])
    bk_r = C.breakeven(lambda m: C.cell(K, AS, 1.0, m, None)["H"])
    out["C2_be_K"] = [be_f["mu"], be_r["mu"]]; out["C2_be_R"] = [bk_f["mu"], bk_r["mu"]]
    return out

def jclean(be):
    return {k: (None if v is None or (isinstance(v, float) and not np.isfinite(v)) else v) for k, v in be.items()}

def main():
    pr("CFG183 main; MUTATE=%d; repo=<repo>" % MUT)
    ctl = controls() if MUT == 0 else None
    R0_ = analyse(0) if MUT else None
    R = analyse(MUT)
    res = {"MUTATE": MUT}
    lines = []
    def P(name, ok, txt):
        lines.append((name, ok)); pr("  [%s] %s: %s" % ("PASS" if ok else "MISS", name, txt))
    pr("== decision cells (mu=0.67)")
    for nm in ("s1", "s0"):
        d = R["dec_" + nm]
        pr("  %s: flat %+.4f +- %.4f (z %+.2f) | rival %+.4f +- %.4f (z %+.2f) | T %+.4f +- %.4f (z %+.2f)" % (
            nm, *d["flat"], d["flat"][0] / d["flat"][1], *d["rival"], d["rival"][0] / d["rival"][1], *d["T"], d["T"][0] / d["T"][1]))
    pr("  R0 = D'_T - D'_flat at decision cell: %+.4f  (%.2f sigma)" % (R["R0"][0], R["R0"][0] / R["R0"][1]))
    pr("== KURVS break-evens (mu_be [1sig interval]) and status (ceiling %.2f)" % C.CEIL)
    for L in ("flat", "rival", "T"):
        for i, s in enumerate(C.S_PUB):
            pr("  %-5s s=%.2f  %-34s %s" % (L, s, C.fmt_be(R["be_K"][L][i]), R["stat"][L][i]))
    pr("== KROSS break-evens")
    for L in ("flat", "rival", "T"):
        for i, s in enumerate(C.S_PUB):
            pr("  %-5s s=%.2f  %s" % (L, s, C.fmt_be(R["be_R"][L][i])))
    pr("== R_T:", ["%.2f" % x if x else None for x in R["RT"]])
    pr("== fit points s0 at mu=0.67  KURVS:", R["fit_K"], " KROSS:", R["fit_R"])
    pr("== headline:", R["sentence"], "| strongly disfavoured:", R["strong"])
    lo1 = R["be_K"]["T"][1]["lo"]
    margin = (lo1 - C.CEIL) if lo1 else None
    pr("== T s=1 lower edge minus ceiling: %s" % ("%.4f" % margin if margin is not None else None))
    res.update(dec_s1=R["dec_s1"], dec_s0=R["dec_s0"], R0=R["R0"],
               be_K={L: [jclean(b) for b in R["be_K"][L]] for L in R["be_K"]},
               be_R={L: [jclean(b) for b in R["be_R"][L]] for L in R["be_R"]},
               stat=R["stat"], fit_K=R["fit_K"], fit_R=R["fit_R"], RT=R["RT"], sentence=R["sentence"], strong=R["strong"], margin=margin)
    dump = lambda o: None if o is None else (float(o) if np.isfinite(o) else str(o))
    if MUT == 0:
        pr("== controls (own code; internal)")
        c1a = all(abs(a - b) <= 0.01 for a, b in zip(ctl["C1_0.3111"], [-0.3256, -0.5089, -0.7220]))
        c1b = all(abs(a - b) <= 0.002 for a, b in zip(ctl["C1_0.315"], [-0.3264, -0.5099]))
        P("P1 t/t0 (Om 0.3111) vs CFG174 target", c1a, str(np.round(ctl["C1_0.3111"], 4)))
        P("P1 t/t0 (Om 0.315) vs README", c1b, str(np.round(ctl["C1_0.315"], 4)))
        P("P1 quadrature vs closed form 1e-6", ctl["C1_quad_vs_closed"] < 1e-6, "%.2e" % ctl["C1_quad_vs_closed"])
        P("C-import E:=1 gives H==flat (1e-9)", ctl["Cimp_E1_H_minus_flat"] < 1e-9, "%.1e" % ctl["Cimp_E1_H_minus_flat"])
        P("C-import rival replay (1e-9)", ctl["Cimp_rival_replay"] < 1e-9, "%.1e" % ctl["Cimp_rival_replay"])
        P("P2 decision cell flat/rival to 5e-4", abs(ctl["C2_dec_flat_rival"][0] - .1441) < 5e-4 and abs(ctl["C2_dec_flat_rival"][1] + .0060) < 5e-4, str(np.round(ctl["C2_dec_flat_rival"], 4)))
        P("P2 KURVS break-evens 2.109/0.621 (0.01)", abs(ctl["C2_be_K"][0] - 2.109) < .01 and abs(ctl["C2_be_K"][1] - .621) < .01, str(np.round(ctl["C2_be_K"], 4)))
        P("P2 KROSS break-evens 0.636/0.052 (0.005)", abs(ctl["C2_be_R"][0] - .636) < .005 and abs(ctl["C2_be_R"][1] - .052) < .005, str(np.round(ctl["C2_be_R"], 4)))
        P("P3 anchor T-flat < 0.01 dex", abs(ctl["C3_anchor_diff_dex"]) < .01, "%.2e" % ctl["C3_anchor_diff_dex"])
        ctl_ok = all(ok for _, ok in lines)
        res["controls"] = ctl
        d1, d0 = R["dec_s1"]["T"], R["dec_s0"]["T"]
        pr("== pass lines P4-P10 against README targets (misses reported, not an exit failure)")
        pl = []
        def Q(name, ok, txt): pl.append((name, ok)); pr("  [%s] %s: %s" % ("PASS" if ok else "MISS", name, txt))
        Q("P4 D'_T decision +0.323+-0.010, sigma 0.047+-0.004, z 6.9+-0.3", within(d1[0], .323, 0, .010) and within(d1[1], .047, 0, .004) and abs(d1[0] / d1[1] - 6.9) <= .3, "%+.4f %.4f z %.2f" % (d1[0], d1[1], d1[0] / d1[1]))
        zf0 = R["dec_s0"]["flat"][0] / R["dec_s0"]["flat"][1]; zr0 = R["dec_s0"]["rival"][0] / R["dec_s0"]["rival"][1]
        Q("P5 D'_T(P0) +0.046+-0.010, sigma .054+-.005, z .85+-.2; flat z -2.3+-.2, rival -4.6+-.3", within(d0[0], .046, 0, .010) and within(d0[1], .054, 0, .005) and abs(d0[0] / d0[1] - .85) <= .2 and abs(zf0 + 2.3) <= .2 and abs(zr0 + 4.6) <= .3,
          "T %+.4f %.4f z %.2f; flat z %.2f; rival z %.2f" % (d0[0], d0[1], d0[0] / d0[1], zf0, zr0))
        Q("P6 R0 +0.179+-0.010; 3.8+-0.3 sigma", within(R["R0"][0], .179, 0, .01) and abs(R["R0"][0] / R["R0"][1] - 3.8) <= .3, "%+.4f %.2f sigma" % (R["R0"][0], R["R0"][0] / R["R0"][1]))
        def be_ok(be, ref):
            if ref is None: return be["mu"] is None and be["note"] == "over"
            if be["mu"] is None: return False
            hi = be["hi"] if np.isfinite(be["hi"]) else 1e9
            return within(be["mu"], ref[0], .04, .05) and within(be["lo"], ref[1], .06, .1) and within(hi, ref[2], .06, .1)
        for L, tab in (("T", T_K), ("flat", F_K), ("rival", R_K)):
            oks = [be_ok(R["be_K"][L][i], tab[i]) for i in range(6)]
            Q("P7 KURVS break-evens %s (6 s)" % L, all(oks), str(oks))
        oks2 = [within(R["be_R"]["T"][i]["mu"], T_R[i][0], .05, .03) for i in range(6)]
        Q("P8 KROSS T break-evens central (6 s)", all(oks2), str(oks2))
        Q("P8 KROSS flat/rival at s=1 (0.636 / 0.052)", within(R["be_R"]["flat"][1]["mu"], .636, .05, .03) and within(R["be_R"]["rival"][1]["mu"], .052, .05, .03), "%.3f %.3f" % (R["be_R"]["flat"][1]["mu"], R["be_R"]["rival"][1]["mu"]))
        Q("P8 R_T within 0.08", all(abs(a - b) <= .08 for a, b in zip(R["RT"], RT_T)), str(np.round(R["RT"], 3)))
        st_ok = R["stat"]["T"] == STAT_T and R["stat"]["flat"] == STAT_F and R["stat"]["rival"] == STAT_R
        Q("P9 18 status labels EXACT", st_ok, "T %s | flat %s | rival %s" % (R["stat"]["T"], R["stat"]["flat"], R["stat"]["rival"]))
        Q("P9 sentence and strongly-disfavoured flag", R["sentence"].startswith("T is gas-excluded under every published prescription and gas-allowed only") and R["strong"], R["sentence"] + " / strong=%s" % R["strong"])
        fk, fr = R["fit_K"], R["fit_R"]
        okfit = (isinstance(fk["rival"], float) and abs(fk["rival"] - 1.03) <= .04 and abs(fk["flat"] - .39) <= .04 and fk["T"] == "<0"
                 and abs(fr["rival"] - 1.87) <= .08 and abs(fr["flat"] - 1.04) <= .06 and abs(fr["T"] - .26) <= .06)
        Q("P10 fit points", okfit, "KURVS %s KROSS %s" % (fk, fr))
        res["pass_lines"] = {n: bool(ok) for n, ok in lines + pl}
        pr("== controls internal: %s ; P4-P10 pass lines %d / %d" % ("PASS" if ctl_ok else "FAIL", sum(ok for _, ok in pl), len(pl)))
        json.dump(res, open(os.path.join(C.HERE, "CFG183_main_results.json"), "w"), indent=1, default=dump)
        sys.exit(0 if ctl_ok else 1)
    base = R0_
    sig_changed = R["signature"] != base["signature"]
    info = {}
    if MUT in (1, 2):
        ref = "flat" if MUT == 1 else "rival"
        eq = max(abs(R["dec_s1"]["T"][0] - R["dec_s1"][ref][0]), abs(R["dec_s0"]["T"][0] - R["dec_s0"][ref][0]))
        eqb = max(abs(R["be_K"]["T"][i]["mu"] - R["be_K"][ref][i]["mu"]) for i in range(1, 6))
        pr("  C-mut%d T rows == %s rows: max |dD'| %.2e, max |d mu_be| %.2e (require < 1e-9)" % (MUT, ref, eq, eqb)); info["eq"] = eq
        bite = sig_changed and eq < 1e-9 and eqb < 1e-6
    elif MUT in (3, 8):
        bite = sig_changed
    elif MUT == 5:
        bite = R["stat"]["T"][1] != base["stat"]["T"][1]
    elif MUT == 6:
        bite = R["stat"]["T"][0] != base["stat"]["T"][0]
    elif MUT == 4:
        d1 = R["dec_s1"]["T"]
        away = [not within(d1[0], .323, 0, .010)] + [not within(R["be_K"]["T"][i]["mu"], T_K[i][0], .04, .05) for i in range(6)]
        bite = any(away); pr("  M4 T numbers leave their P4/P7 lines:", away)
    elif MUT == 7:
        sw = {"flat": R["stat"]["T"], "T": R["stat"]["flat"], "rival": R["stat"]["rival"]}
        bite = sw != R["stat"]
        pr("  M7 swapped matrix T row:", sw["T"], " flat row:", sw["flat"])
    pr("== MUTATE %d: baseline T status %s ; mutated %s" % (MUT, base["stat"]["T"], R["stat"]["T"]))
    pr("   baseline sentence: %s | mutated: %s | strong %s -> %s" % (base["sentence"], R["sentence"], base["strong"], R["strong"]))
    pr("   BITES: %s (exit %d)" % (bool(bite), 1 if bite else 0))
    res.update(baseline_stat=base["stat"]["T"], bite=bool(bite), info=info)
    json.dump(res, open(os.path.join(C.HERE, "CFG183_MUTATE_%d_results.json" % MUT), "w"), indent=1, default=dump)
    sys.exit(1 if bite else 0)

if __name__ == "__main__":
    main()
