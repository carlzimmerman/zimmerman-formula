"""Assemble crg1_results.json from partials. Canonical is primary; alt reported, never pooled."""
from crg1_core import *
import sys, numpy, scipy

P = load_part
NR_ = "NOT RECOMPUTED (Tier C: later stage)"; NG = "NOT GRADED"

def sp(cell_rows, passes):
    S = {t: dict(Y_med=r["S"]["Y_med"], rms=r["S"]["rms"], skipped_galaxies=r["S"]["skipped"]) for t, r in cell_rows.items()}
    Tl = {t: r["Tl"] for t, r in cell_rows.items()}
    LT = {t: dict(median_E=r["LT"]) for t, r in cell_rows.items()}
    extra = {t: {k: v for k, v in r.items() if k not in ("S", "Tl", "LT")} for t, r in cell_rows.items()}
    return dict(S=dict(by_background=S, passed=passes["S"], tier="A", tags=["[recomputed]"]),
                Tl=dict(by_background=Tl, passed=passes["Tl"], tier="A", tags=["[recomputed]"]),
                LT=dict(by_background=LT, passed=passes["LT"], tier="A", tags=["[recomputed]"]), SPARC_LT_detail=extra)

def verdict(lines):
    failed = sorted(k for k, v in lines.items() if isinstance(v, dict) and v.get("passed") is False)
    ng = sorted(k for k, v in lines.items() if isinstance(v, dict) and v.get("status") == NG)
    nr = sorted(k for k, v in lines.items() if isinstance(v, dict) and v.get("status") == NR_)
    return dict(state=("FAILS on recomputed lines" if failed else "PASSES EVERY RECOMPUTED LINE; Tier C lines still to enter at COMPARE"), failed_lines=failed, not_graded=ng, not_recomputed_tier_C=nr)

def main(outname):
    K1, K2, K4 = P("K_C1"), P("K_C2"), P("K_C4")
    X = P("X_all"); G = P("G"); Dw = P("Dw"); Ln = P("Ln")
    prim = "f%s_g%s" % (SC["fstar"]["primary"], SC["gas_dex"]["gs4"])
    def trow(t): 
        return {k: v for k, v in t.items()}
    def kline(tier, tags, r, **kw):
        d = dict(status="[recomputed]", passed=r["passed"], failing=r["failing"], n_pass=r["n_pass"], n_keys=r["n_keys"], tier=tier, tags=tags, tables=r["tables"]); d.update(kw); return d
    def xline(x, reading, **kw):
        d = dict(status="[recomputed]", passed=x["passed"], tier="A", tags=["[recomputed]", "[INPUT AS GIVEN: GS1 slope, zoom stacks ng 64/80]"], reading=reading); d.update(x); d.update(kw); return d
    TC = {k: dict(status=NR_) for k in ("MW", "DM", "IC")}
    res = {}
    # C1
    a = sp(P("sparc_C1_canonical")["rows"], P("sparc_C1_canonical")["passes"]); det = a.pop("SPARC_LT_detail")
    c1k = K1[prim]
    rep = {k: {x: v for x, v in K1[k].items() if x != "A9b_alt_Cstar" or True} for k in K1}
    lines = dict(a)
    lines["K"] = kline("A", ["[recomputed]", "[INPUT AS GIVEN: zoom stacks, GS1 slope, GS4 +0.005, BCG n/a, A_CAL, s_CAL, EFE own solve]"], c1k, reading="A7a f* 0.034 graded; A9a canonical C*; A10a own C(s)", counts_per_h=c1k["counts_per_h"],
                     A10b_max_dZ_canonical=c1k["A10b_max_dZ_canonical"], reported_rows={k: {x: K1[k][x] for x in ("tables", "failing", "n_pass", "passed", "counts_per_h")} for k in K1 if k != prim},
                     A9b_alt_Cstar={k: {x: K1[k]["A9b_alt_Cstar"][x] for x in ("tables", "failing", "n_pass", "passed")} for k in K1},
                     NA4b=c1k["NA4b_x_edge_min_all_nodes"], NA9b=c1k["NA9b_Bst_over_I"])
    gc = K1["f%s_g%s" % (SC["fstar"]["primary"], SC["gas_dex"]["xcop"])]["n_pass"] == 15 and K1["f%s_g%s" % (SC["fstar"]["reported"], SC["gas_dex"]["xcop"])]["n_pass"] == 15
    lines["K"]["GAS_CONDITIONAL_input"] = dict(K_15_of_15_at_gas_0p111_both_fstar=bool(gc), note="computed for the tag; verdict left to COMPARE")
    lines["X"] = xline(X["C1_f0.034"], "A6a; f* 0.034 graded", f0p0615=X["C1_f0.0615"], A6b={k: X[k] for k in X if "A6b" in k}, NA4b=X["C1_f0.034_NA4b"])
    lines["G"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]", "[INPUT AS GIVEN: em1 map]"], reading="A1a", **G["C1"]["canonical"], A1b=G["C1"]["canonical_A1b"])
    lines["Ln"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]", "not on NR2", "[INPUT AS GIVEN: ce1_a3_eta_med, t1x P_grav]"], reading="A12a", **Ln["canonical"]["C1"], alt_reported=Ln["alt"]["C1"], A12b_S_N=Ln["canonical"]["C1_A12b"], A12b_alt=Ln["alt"]["C1_A12b"])
    lines["Dw"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]", "[READ ND1]'s rule", "not on NR2's table", "[INPUT AS GIVEN: ce1_a4_eta_med, x80]"], reading="A14a", **Dw["C1"]["canonical"], A14b_NR2=Dw["C1_A14b_NR2"]["canonical"], NA2b=Dw["C1_NA2b_unit_set_D"]["canonical"])
    lines.update(TC); lines["detail"] = det; lines["_verdict"] = verdict(lines)
    res["C1"] = {"canonical": lines}
    # C2
    a = sp(P("sparc_C2_canonical")["rows"], P("sparc_C2_canonical")["passes"]); det = a.pop("SPARC_LT_detail"); lines = dict(a)
    lines["K"] = kline("A", ["[recomputed]", "[INPUT AS GIVEN: BCG, A_CAL, s_CAL, GS1 slope, EFE own solve]"], K2, reading="A1a, A9a, A10a, NA3a C* on M_b", A10b_max_dZ_canonical=K2["A10b_max_dZ_canonical"],
                     A9b_alt_Cstar={x: K2["A9b_alt_Cstar"][x] for x in ("tables", "failing", "n_pass", "passed")}, NA3b=K2["NA3b_Cstar_on_Mbf"], A1b=K2["A1b"])
    lines["X"] = xline(X["C2_f0.034"], "NA13a contraction on uncapped M_bx, as written", A1b=X["C2_f0.034_A1b"], NA13b=X["C2_f0.034_NA13b_capped_Mb"])
    lines["G"] = dict(status=NR_, extra_computed_not_graded=G["C2_extra_TierC"]["canonical"])
    lines["Ln"] = dict(status=NR_); lines["Dw"] = dict(status=NG); lines.update(TC); lines["detail"] = det; lines["_verdict"] = verdict(lines)
    res["C2"] = {"canonical": lines}
    # C3
    res["C3"] = {}
    for foot in ("canonical", "alt"):
        a = sp(P("sparc_C3_" + foot)["rows"], P("sparc_C3_" + foot)["passes"]); det = a.pop("SPARC_LT_detail"); lines = dict(a)
        kr = c1k if foot == "canonical" else c1k["A9b_alt_Cstar"]
        lines["K"] = kline("A", ["[recomputed]", "= C1's row" + ("" if foot == "canonical" else " with alt C* (A9b)")], kr, reading="A7a")
        lines["X"] = xline(X["C1_f0.034"], "= C1's row; no a0 enters X", note="same value at both footings")
        lines["G"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]", "C3 floor disclosed", "[INPUT AS GIVEN: x48 A2 cf]"], **G["C3"][foot])
        r = Ln[foot]["C3"]; lines["Ln"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]", "[INPUT AS GIVEN: x48 A2 cf, t1x P_grav]"], reading="A11a", passed=r["passed"], primary_range=r["prim"], A11b=r["A11b"], share_lens_grid_above_T=r["share_lens_grid_above_T"], **r["all"])
        lines["Dw"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]"], reading="A13a host flag", **Dw["C3"][foot], A13b_mass_flag=Dw["C3_A13b_mass_flag"][foot])
        lines.update(TC); lines["detail"] = det; lines["_verdict"] = verdict(lines)
        res["C3"][foot] = lines
    # C4
    res["C4"] = {}
    for foot in ("canonical", "alt"):
        a = sp(P("sparc_C4_" + foot)["rows"], P("sparc_C4_" + foot)["passes"]); det = a.pop("SPARC_LT_detail"); lines = dict(a)
        r4 = K4[foot]
        lines["K"] = kline("A", ["[recomputed]", "[INPUT AS GIVEN: A_CAL, s_CAL for the four mass keys]"], r4, reading="A8a; NA1a core-form gas(P), no tail", A10b_max_dZ=r4["A10b_max_dZ"], A8b=r4["A8b_one_template"], NA1b=r4["NA1b_GS1_tail_in_gas_P"])
        lines["X"] = dict(status=NG)
        lines["G"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]"], **G["C4"][foot])
        r = Ln[foot]["C4"]; lines["Ln"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]", "[INPUT AS GIVEN: x48 A2 cf, t1x P_grav]"], reading="A11a; ENV = L", passed=r["passed"], primary_range=r["prim"], A11b=r["A11b"], **r["all"])
        lines["Dw"] = dict(status="[recomputed]", tier="B", tags=["[recomputed]"], **Dw["C4"][foot])
        lines.update(TC); lines["detail"] = det; lines["_verdict"] = verdict(lines)
        res["C4"][foot] = lines
    res["_meta"] = dict(checks=dict(k1_math=P("k1_math")["all_passed"], k1_shear=P("k1_shear")["passed"], k1_shear_flip_must_fail=not P("k1_shear_FLIP")["passed"], k2=P("k2")["all_ok"]),
                        known_answers=dict(eta_per_seed_max_diff={k: v["max_abs_diff_vs_scalars"] for k, v in P("zoom_eta").items()}, efe_canonical=P("efe_canonical"), efe_alt=P("efe_alt"), sigma8={k: v for k, v in P("k1_math").items() if k.startswith("K_S")}),
                        A1=dict(a=dict(eta12=SC["nr2"]["eta12_anchor"]), b_median_eta={k: v["median_eta"] for k, v in P("zoom_eta").items()}),
                        A5b="see crg1_results_A5b_oneset.json if present", A15_numpy=numpy.__version__, scipy=scipy.__version__, A16="as stated", A17b="not computed, per spec",
                        shape_stacks=P("zoom_shape_info"), sample_sizes=P("k2")["sizes"], primary_verdict_footing="canonical; alt reported, never pooled",
                        wording="kappa = 1/2 FITTED. Cold dark energy is a gravitating field component. Not theory closed.")
    write_atomic(os.path.join(HERE, outname), dumps(res) + "\n")

if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else "crg1_results.json")
