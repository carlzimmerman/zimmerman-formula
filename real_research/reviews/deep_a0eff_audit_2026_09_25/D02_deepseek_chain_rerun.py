#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D02 -- THE deepseek_push SPARC-DEEP CHAIN, RE-RUN CORRECTLY.
=============================================================
D01 showed that the "SPARC-deep a0_eff = 0.724 a0" channel is carried by the per-galaxy disc mass-to-light ratios `m2l_disk` of
glm53_push/data/rotation_curve_corpus_v7.json.  This script (1) establishes WHAT those numbers are, (2) re-runs every deepseek
lane that reads them, and every lane downstream, with THEIR OWN CODE on corrected inputs, and (3) reports, lane by lane, which
registered verdicts change.

(1) ROOT CAUSE.  SPARC tabulates no mass-to-light ratio.  The corpus values correlate at r = 0.92 (log) with the ratio at which
    Newtonian baryons ALONE reproduce each rotation curve (least squares over the curve): they are kinematic fits, not stellar-
    population values.  Feeding them back into a measurement of a0 puts part of the mass discrepancy into the stars before a0 is
    measured -- a circular input that drives a0_eff down.

(2) THE RE-RUN (sandbox.py, lanes.py).  A sandbox mirrors the repository (copy-on-write clones of every deepseek_push top-level
    file, read-only symlinks for directories and every other repository entry) with one file replaced: the corpus.  The SPARC
    entries get the standard 3.6-micron convention (Lelli+2016, McGaugh+2016): Y_disc = 0.5, 0.6 or 0.7 and Y_bul = 0.7 (the
    bulge ratio applied by rescaling V_bul inside the unmodified lane expression m2l*(V_disk^2 + V_bul^2)), and, in three of the
    four variants, the velocity-error cut err/V < 10 per cent (2803 of 3391 rings).  V_obs, V_disk, V_gas, radii, distances
    and inclinations are untouched.  Lanes run in dependency order, 25 of them.  The only edits to lane code are the input
    LOOKUPS listed in lanes.py (O04b and P02 selected the SPARC entry of N05's results by a value range that assumes a deficit;
    G183 asserted a fixed ring count; ZD08 and ZD11 hard-code the G183 a0*).  A BASELINE sandbox with the committed corpus must
    reproduce every committed result exactly before any corrected number is believed.

(3) CHECKS can fail.  MUTATE=1 builds the "corrected" variants from the UNCHANGED corpus (no mass-to-light correction, no cut):
    every check that says a verdict changes must then FAIL (rc = 1).
Both footings: the lanes carry a0 = 9.3619e-11 (canonical); the alternative a0 = 1.1279e-10 is 1.2048 x larger, so every
a0_eff/a0 below divides by 1.2048 on the alternative footing -- printed for the anchors.
Run from the repository root:  python3 real_research/reviews/deep_a0eff_audit_2026_09_25/D02_deepseek_chain_rerun.py
(about 15 minutes; G183 alone takes 2-3 minutes per variant).  Writes D02_results[_MUTATE].json next to this file.
"""
import os, sys, json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sandbox as sb
import lanes as LN

MUTATE = os.environ.get("MUTATE", "0") == "1"
A0, A0_ALT = 9.3619e-11, 1.1279e-10
FOOT = A0_ALT / A0
CH = []
def P(*a): print(*a, flush=True)
def check(name, measured, ok, reading="", load_bearing=True):
    CH.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}" + (f"\n         reading:  {reading}" if reading else ""))
def banner(t): P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)

# ------------------------------------------------------------------------------------------------------------ (2) runs
VARIANTS = {"std05_cut": dict(ud=0.5, ub=0.7, qcut=0.10), "std06_cut": dict(ud=0.6, ub=0.7, qcut=0.10),
            "std07_cut": dict(ud=0.7, ub=0.7, qcut=0.10), "std05_nocut": dict(ud=0.5, ub=0.7, qcut=None)}
def run_chain(corpus_json, tag, archive=False, hash_probe=False, patch_a0star=True):
    t0 = time.time()
    S = sb.build(corpus_json, patches=LN.STATIC_PATCHES, tag=tag)
    rcs, outs = {}, {}
    try:
        for L in LN.LANES:
            if L[:4] in ("ZD08", "ZD11") and patch_a0star:          # corrected variants only: the baseline runs the committed constants
                sb.patch(S, L, LN.a0star_patch(L, sb.load(S, "G183_results.json")["registers"]["SPARC_deep_free_a0"]))
            r = sb.run(S, L); rcs[L] = r["rc"]; outs[L] = r["stdout"] + ("\n[stderr tail]\n" + r["stderr"] if r["rc"] else "")
        res = {L: sb.load(S, f) for L, f in OUTFILES.items()}
        if hash_probe:                                 # which G199 outputs depend on Python's per-process string-hash order?
            probe = []
            for seed in ("11", "12"):
                sb.run(S, "G199_deep_universality.py", env={"PYTHONHASHSEED": seed}); probe.append(sb.load(S, "G199_results.json"))
            res["_G199_hash_probe"] = probe
        if archive:                                    # the corrected lane outputs, kept as evidence
            A = os.path.join(HERE, "D02_rerun_outputs", tag); os.makedirs(A, exist_ok=True)
            for k, f in OUTFILES.items():
                if res[k] is not None: json.dump(res[k], open(os.path.join(A, f), "w"), indent=1)
            for L, o in outs.items():
                open(os.path.join(A, L.replace(".py", ".out")), "w").write(o)
            json.dump(rcs, open(os.path.join(A, "exit_codes.json"), "w"), indent=1)
    finally:
        sb.destroy(S)
    P(f"    {tag}: {len(LN.LANES)} lanes in {time.time() - t0:.0f} s; nonzero exit: {[k for k, v in rcs.items() if v] or 'none'}")
    return res, rcs

OUTFILES = {"L06": "L06_results.json", "N05": "N05_results.json", "N01": "N01_results.json", "Q02": "Q02_results.json", "R03": "R03_results.json",
            "S01": "S01_results.json", "G158": "G158_results.json", "G183": "G183_results.json", "G199": "G199_results.json", "G208": "G208_results.json",
            "O04b": "O04b_joint_update.json", "P02": "P02_results.json", "S02m": "S02_results.json", "T03": "T03_mightee_subpop.json",
            "U01": "U01_deep_structure_results.json", "U02": "U02_arbitration_refresh_results.json", "U03": "U03_digitization_audit_results.json",
            "W03": "W03_wallaby_card_results.json", "S02p": "S02_a0z_plane_results.json", "ZD08": "ZD08_results.json", "ZD11": "ZD11_results.json"}

def g(d, path, default=None):
    cur = d
    for k in path.split("/"):
        if cur is None: return default
        if isinstance(cur, list):
            k = int(k)
            cur = cur[k] if k < len(cur) else None
        else:
            cur = cur.get(k) if isinstance(cur, dict) else None
    return default if cur is None else cur

def headline(R):
    """the registered headline of every lane, read from its own results file"""
    l06d = [r for r in R["L06"]["results"] if r.get("N") and "deep" in str(r.get("label", r.get("name", ""))).lower() and "SPARC" in str(r.get("label", r.get("name", "")))]
    l06d = l06d[0] if l06d else R["L06"]["results"][1]
    chk = lambda d, key: [c for c in d.get("checks", []) if str(c.get("name", "")).startswith(key)]
    return {
        "L06 SPARC-deep a0_eff/a0 (alpha=1 moment)": 1 + l06d["Delta"] / (A0 * l06d["E_gbar"]),
        "L06 SPARC-deep z": l06d["z_Delta"],
        "N05 SPARC-deep a0_eff/a0": g(R["N05"], "deep_sparc_L06/a0eff_a0"),
        "N05 SPARC-deep z (clustered)": g(R["N05"], "deep_sparc_L06/z_clustered"),
        "N05 SPARC-deep rings": g(R["N05"], "deep_sparc_L06/N"),
        "N05 MIGHTEE-deep a0_eff/a0": g(R["N05"], "mightee_deep/a0eff_a0"),
        "N05 card N_req (rings to kill the SPARC deviation at 5 SE)": g(R["N05"], "n_requirement/N_req_ring_level"),
        "N01 kill (c) fired, gas/tot": f"{g(R['N01'], 'kills/4bins.gas/kill_c_fired')}/{g(R['N01'], 'kills/4bins.tot/kill_c_fired')}",
        "Q02 SPARC anchor (weighted mean a0_eff/a0)": g(R["Q02"], "main/weighted_mean"),
        "Q02 anchor SE": g(R["Q02"], "main/weighted_mean_se"),
        "Q02 onset slope z": g(R["Q02"], "main/slope_z"),
        "Q02 verdict": g(R["Q02"], "verdict"),
        "R03 verdict": g(R["R03"], "verdict"),
        "S01 fraction of comparisons within 3 SE": g(R["S01"], "universality/fraction_within_3SE"),
        "S01 C1 (collapse) pass": g(R["S01"], "c1_pass"),
        "S01 SPARC Phi, deepest three bins (mean)": float(np.mean([b["Phi"] for b in R["S01"]["sparc"]["bins"][:3]])),
        "S01 MIGHTEE - SPARC offset at the same x": g(R["S01"], "universality/comparisons/0/offset"),
        "S01 MIGHTEE vs SPARC z": g(R["S01"], "universality/comparisons/0/z"),
        "S01 law": str(g(R["S01"], "law", ""))[:60],
        "G158 SPARC-deep n amplitude": g(R["G158"], "measurements/SPARC/n_amp"),
        "G158 slope channel n (pooled per galaxy)": g(R["G158"], "discriminator/slope_channel/n_pooled_per_gal"),
        "G158 slope channel sigma from n = 2": g(R["G158"], "discriminator/slope_channel/sep_from_2_000_sigma"),
        "G158 pooled amplitude n": g(R["G158"], "pooled/n_amp_pooled"),
        "G183 pooled n-free fit n": g(R["G183"], "M1_nfree/n"),
        "G183 pooled n-free fit n SE": g(R["G183"], "M1_nfree/n_se"),
        "G158 SPARC-deep a0 [1e-11]": (g(R["G158"], "discriminator/amplitude_channel/SPARC_deep/a0") or 0) * 1e11,
        "G183 SPARC-deep free a0* [1e-11]": g(R["G183"], "registers/SPARC_deep_free_a0") * 1e11,
        "G199 SPARC deep fit a0 [1e-11]": g(R["G199"], "deep_end_readings/SPARC/a0_eff_fit_deep") * 1e11,
        "G208 staircase SPARC_deep_fit [1e-11]": g(R["G208"], "staircase/SPARC_deep_fit") * 1e11,
        "G208 staircase spread (x)": g(R["G208"], "staircase/spread_x"),
        "O04b SPARC channel": g(R["O04b"], "channels/0/x"),
        "O04b joint a0_eff/a0": g(R["O04b"], "joint/xbar"),
        "O04b joint chi2 (df 2; 5.991 = heterogeneous)": g(R["O04b"], "joint/chi2_df2"),
        "O04b joint z vs canonical": g(R["O04b"], "joint/z_vs_a0"),
        "O04b verdict": str(g(R["O04b"], "verdict", ""))[:70],
        "P02 deviation |Delta|/a0E": g(R["P02"], "registered/Delta_deep_a0E"),
        "S02 mirror: SPARC anchor": g(R["S02m"], "anchor_q02/mean"),
        "S02 mirror: MIGHTEE z vs anchor": g(R["S02m"], "z_vs_q02"),
        "S02 mirror verdict": g(R["S02m"], "verdict"),
        "T03 gap MIGHTEE - anchor": g(R["T03"], "gap"),
        "T03 verdict": g(R["T03"], "verdict"),
        "U01 z(slope difference vs Q02)": g(R["U01"], "q02_slope_comp/z_diff"),
        "U02 SPARC deviation (a0E units)": g(R["U02"], "f3/delta_sparc_a0E"),
        "U03 share of digitization draws with z < 3 vs the anchor": g(R["U03"], "frac_z_lt3_both_axis"),
        "U03 verdict": g(R["U03"], "verdict"),
        "W03 verdict": g(R["W03"], "verdict"),
        "S02 plane: alpha_SPARC [per unit z]": g(R["S02p"], "impossibility_leg/alpha_lin_SPARC_per_unit_z_ref_0.044"),
        "S02 plane: SPARC-to-MIGHTEE step [dex]": g(R["S02p"], "impossibility_leg/delta_log10_a0_between_dex"),
        "ZD08 a0*(velocity) / registered a0*": (g(R["ZD08"], "a0_star_velocity_domain") or 0) / (g(R["ZD08"], "a0_star_registered_sparc_deep") or 1),
        "ZD08 C2 two-scale clash count": str([c.get("detail", "") for c in chk(R["ZD08"], "C2")])[:90],
        "ZD11 median log residual at a0* [dex]": g(R["ZD11"], "msa3d/median_log_resid_WEDGE"),
    }

def flat(x, pre=""):
    out = {}
    if isinstance(x, dict):
        for k, v in x.items(): out.update(flat(v, pre + str(k) + "/"))
    elif isinstance(x, list):
        for i, v in enumerate(x): out.update(flat(v, pre + str(i) + "/"))
    elif isinstance(x, (int, float)) and not isinstance(x, bool): out[pre] = float(x)
    return out


def main():
    P(__doc__)
    # ------------------------------------------------------------------------------------------------------------ (1) root cause
    banner("R  THE ROOT CAUSE: what the corpus m2l_disk values are")
    corpus = json.load(open(sb.CORPUS))
    ml_c, ml_n = [], []
    for g in corpus["galaxies"]:
        if g.get("survey") != "SPARC" or not g.get("m2l_disk"): continue
        v = g.get("data") or []
        Vo = np.array([p["Vobs"] for p in v]); Vg = np.array([p["Vgas"] for p in v]); Vd = np.array([p["Vdisk"] for p in v]); Vb = np.array([p["Vbul"] for p in v])
        S_ = Vd ** 2 + Vb ** 2; T_ = Vo ** 2 - np.sign(Vg) * Vg ** 2; ok = S_ > 0
        if ok.sum() < 3: continue
        ml_c.append(g["m2l_disk"]); ml_n.append(np.sum(T_[ok] * S_[ok]) / np.sum(S_[ok] ** 2))
    ml_c, ml_n = np.array(ml_c), np.array(ml_n)
    r_ml = float(np.corrcoef(np.log10(ml_c), np.log10(np.clip(ml_n, 1e-3, None)))[0, 1])
    ratio = np.median(ml_c / ml_n)
    check("R1 the corpus m2l_disk is a KINEMATIC fit: log-correlation with the Newtonian no-dark-matter ratio exceeds 0.8",
          f"r = {r_ml:.3f} over {len(ml_c)} SPARC galaxies; median corpus/Newtonian = {ratio:.2f}; corpus median {np.median(ml_c):.2f}, max {ml_c.max():.1f}",
          r_ml > 0.8, "a 3.6-micron population ratio is set by photometry (0.5-0.7) and would not track the kinematics at r = 0.92")


    # ------------------------------------------------------------------------------------------------------------ baseline
    banner("B  BASELINE: the committed corpus in a sandbox must reproduce every committed result")
    base_R, base_rc = run_chain(sb.corpus_variant(), "base", hash_probe=True, patch_a0star=False)
    committed = {k: json.load(open(os.path.join(sb.DS, f))) for k, f in OUTFILES.items()}
    # G199 bootstraps over galaxy groups taken from a Python set: its seeded RNG draws indices into a list whose ORDER follows the
    # per-process string-hash randomisation, so the outputs built from its bootstraps differ from run to run.  They are not listed
    # by hand: G199 is re-run twice in the baseline sandbox under two fixed PYTHONHASHSEED values, and exactly the fields that
    # differ between those two runs are excluded (and printed).  Every other field of all 21 files must match to 1e-9.
    p1, p2 = (flat(x) for x in base_R.pop("_G199_hash_probe"))
    G199_VAR = sorted(k for k in p1 if k in p2 and abs(p1[k] - p2[k]) > 1e-12 * max(abs(p1[k]), 1e-300))
    P(f"    G199 fields that change with the hash seed alone ({len(G199_VAR)}): {G199_VAR}")
    worst, where, nfield, boot_worst = 0.0, "", 0, 0.0
    for k in OUTFILES:
        A_, B_ = flat(committed[k]), flat(base_R[k])
        for key in A_:
            if key not in B_: continue
            d = abs(A_[key] - B_[key]) / max(abs(A_[key]), 1e-300)
            if k == "G199" and key in G199_VAR:
                boot_worst = max(boot_worst, d); continue
            nfield += 1
            if d > worst: worst, where = d, f"{k}:{key}"
    check("B1 the sandbox reproduces all 21 committed result files with the committed corpus and every lookup patch in place (every numeric field to 1e-9)",
          f"{nfield} fields; worst relative difference {worst:.1e} {('at ' + where) if worst > 0 else ''}; nonzero exits {[k for k, v in base_rc.items() if v] or 'none'}; "
          f"the {len(G199_VAR)} G199 fields that change with the hash seed alone excluded; against the committed file they move by up to {boot_worst:.1%}",
          worst < 1e-9 and not any(base_rc.values()), "the machinery and the patches are neutral on the committed inputs: any difference below comes from the corpus alone")

    # ------------------------------------------------------------------------------------------------------------ corrected
    banner("C  THE CORRECTED RUNS" + ("   [MUTATE: built from the UNCHANGED corpus -- the correction is NOT applied]" if MUTATE else ""))
    RUNS = {}
    for tag, kw in VARIANTS.items():
        cj = sb.corpus_variant() if MUTATE else sb.corpus_variant(**kw)
        RUNS[tag], _ = run_chain(cj, tag, archive=not MUTATE)
    H = {"committed": headline(committed)}
    H.update({t: headline(R) for t, R in RUNS.items()})
    cols = ["committed"] + list(VARIANTS)
    P("\n  " + f"{'headline':60s}" + "".join(f"{c:>16s}" for c in cols))
    for key in H["committed"]:
        cells = []
        for c in cols:
            v = H[c][key]
            cells.append(f"{v:16.4g}" if isinstance(v, (int, float)) and not isinstance(v, bool) else f"{str(v)[:15]:>16s}")
        P(f"  {key[:60]:60s}" + "".join(cells))
    P("\n  alternative footing (a0 = 1.1279e-10): divide every a0_eff/a0 by 1.2048 -- SPARC anchors: " +
      ", ".join(f"{c} {H[c]['N05 SPARC-deep a0_eff/a0'] / FOOT:.3f}" for c in cols))

    # -------------------------------------------------------------------------------------------------------- (3) verdicts
    banner("V  WHAT CHANGES, LANE BY LANE (each check reads the lanes' own corrected outputs; under MUTATE the change checks must FAIL)")
    T = list(VARIANTS)
    col = lambda key: [H[t][key] for t in T]
    lane_checks = lambda R, lane, prefix: [c for c in (R[lane] or {}).get("checks", []) if str(c.get("name", "")).startswith(prefix)]
    v = col("N05 SPARC-deep a0_eff/a0")
    check("C1 [L06/N05] the SPARC-deep alpha=1 a0_eff is ABOVE 1 in every corrected variant: the 'deficit' reverses (committed 0.724, z = -4.17)",
          f"{', '.join(f'{x:.3f}' for x in v)} (z {', '.join(f'{x:+.1f}' for x in col('N05 SPARC-deep z (clustered)'))}); alternative footing /1.2048: {', '.join(f'{x / FOOT:.3f}' for x in v)}",
          all(x > 1 for x in v), "the N05 program card (N_req = 1656 rings to kill the deficit), P02's power audit, U02's refresh and W03's census premise all target a deficit that is not there")
    v = col("O04b joint chi2 (df 2; 5.991 = heterogeneous)")
    check("C2 [O04b] the joint 'deep a0_eff = 0.7172 +/- 0.0593, 4.77 sigma below canonical' is NOT banked: O04b's own heterogeneity test fires in every variant",
          f"chi2 = {', '.join(f'{x:.1f}' for x in v)} (df 2, limit 5.991); SPARC channel {', '.join(f'{x:.2f}' for x in col('O04b SPARC channel'))} vs dwarfs 0.638 and Milky Way 0.797",
          all(x > 5.991 for x in v), "the dwarf (O01) and Milky Way (O03) channels are measured on their own inputs and stand as measured; only the joint and the '0.73' comparisons fall")
    v = col("Q02 SPARC anchor (weighted mean a0_eff/a0)")
    check("C3 [Q02 -> S02/T03/U01/U03] the SPARC deep-band anchor is ABOVE 1 in every variant (committed 0.8314 +/- 0.042)",
          f"{', '.join(f'{x:.3f}' for x in v)} (SE {', '.join(f'{x:.3f}' for x in col('Q02 anchor SE'))}); alternative footing: {', '.join(f'{x / FOOT:.3f}' for x in v)}",
          all(x > 1 for x in v))
    q = col("Q02 verdict")
    check("C4 [Q02/R03] the registered CONSTANT-OFFSET verdict depends on the disc mass-to-light ratio: the variants do not all return it",
          f"Q02 {', '.join(map(str, q))}; R03 {', '.join(map(str, col('R03 verdict')))}; onset-slope z {', '.join(f'{x:.2f}' for x in col('Q02 onset slope z'))}",
          len(set(q)) > 1)
    v = col("S02 mirror: MIGHTEE z vs anchor")
    check("C5 [S02 mirror] MIGHTEE agrees with the corrected SPARC anchor within 3 sigma at Upsilon_disc = 0.5 and 0.6 (committed z = +6.99, 'CHANNEL-DEPENDENT')",
          f"z = {', '.join(f'{x:.2f}' for x in v)}; verdicts {', '.join(map(str, col('S02 mirror verdict')))}",
          v[0] < 3 and v[1] < 3, f"at Upsilon_disc = 0.7 MIGHTEE sits {v[2]:.1f} sigma above: what remains is a difference inside the range of the disc mass-to-light convention, not a sign mirror")
    v = col("S01 SPARC Phi, deepest three bins (mean)")
    check("C6 [S01] the SPARC deep bins sit ABOVE 1 in every variant (committed 0.87): MIGHTEE and SPARC are on the SAME side, the 'sign mirror' is gone",
          f"SPARC deepest-bin Phi {', '.join(f'{x:.2f}' for x in v)}; MIGHTEE-SPARC offset {', '.join(f'{x:.2f}' for x in col('S01 MIGHTEE - SPARC offset at the same x'))} "
          f"(z {', '.join(f'{x:.1f}' for x in col('S01 MIGHTEE vs SPARC z'))}; committed 1.24, z 4.1); within-3-SE fraction {', '.join(f'{x:.2f}' for x in col('S01 fraction of comparisons within 3 SE'))}",
          all(x > 1 for x in v), "S01's pre-registered NO-COLLAPSE outcome formally stands in every variant (its C1 and C2 never pass together: "
          + ", ".join(f"C1 {bool(RUNS[t]['S01']['c1_pass'])}/C2 {bool(RUNS[t]['S01']['c2_pass'])}" for t in T)
          + "), but its reading 'the sign-mirror is a genuine systematics divide' does not; the O01 deep-tail point (Phi = 0.31, N = 7) is O01's own and still sits below")
    v = col("S02 plane: alpha_SPARC [per unit z]")
    check("C7 [S02 a0(z) plane] the SPARC slope has the SAME sign as MIGHTEE's in every variant: the 'opposite-signed' impossibility premise fails (the lane's own C4 check fails)",
          f"alpha_SPARC = {', '.join(f'{x:+.1f}' for x in v)} per unit z (committed -6.2) vs MIGHTEE +26.3; SPARC-to-MIGHTEE step {', '.join(f'{x:.3f}' for x in col('S02 plane: SPARC-to-MIGHTEE step [dex]'))} dex (committed 0.475); "
          f"lane C4 passes: {[bool(lane_checks(RUNS[t], 'S02p', 'C4')[0].get('result', lane_checks(RUNS[t], 'S02p', 'C4')[0].get('pass'))) for t in T]}",
          all(x > 0 for x in v), "the conclusion 'the staircase cannot be a0(z)' still holds by MAGNITUDE (a 0.06-0.18 dex step over dz = 0.044 is still 1e5 x any registered a0(z) rate), not by sign")
    v = col("G183 SPARC-deep free a0* [1e-11]")
    check("C8 [G071 -> G158/G183/G199/G208] the SPARC-deep scale a0* is ABOVE the canonical a0 in every variant: the 'wedge' 6.4e-11 is the corpus mass-to-light ratios",
          f"G183 a0* = {', '.join(f'{x:.2f}' for x in v)} x 1e-11 (committed 6.41; canonical 9.36, alternative 11.28); G199 {', '.join(f'{x:.2f}' for x in col('G199 SPARC deep fit a0 [1e-11]'))}; "
          f"G208 staircase spread {', '.join(f'{x:.2f}' for x in col('G208 staircase spread (x)'))} x (committed 2.92)",
          all(x > 9.3619 for x in v))
    v = col("ZD08 a0*(velocity) / registered a0*")
    zd8 = [[bool(c.get("pass")) for c in (RUNS[t]["ZD08"] or {}).get("checks", [])] for t in T]
    import re as _re
    def clash(R, which):
        det = [c.get("detail", "") for c in (R["ZD08"] or {}).get("checks", []) if str(c.get("name", "")).startswith("C2")]
        m = _re.search(("one-scale" if which == 1 else "two-scale") + r"[^:]*:\s*(\d+)/(\d+)", det[0]) if det else None
        return f"{m.group(1)}/{m.group(2)}" if m else "?"
    two = [clash(RUNS[t], 2) for t in T]; one = clash(RUNS[T[0]], 1); two_c = clash(committed, 2)
    check("C9 [ZD08 -> falsifier row 27] the velocity-domain a0*(V) = 6.0e-11 no longer matches the SPARC-deep scale: ratio < 0.6 in every variant, and ZD08's own C1 fails",
          f"a0*(V)/a0*(SPARC-deep) = {', '.join(f'{x:.2f}' for x in v)} (committed 0.94, '6% agreement'); ZD08 own checks C1-C4 per variant: {zd8}",
          all(x < 0.6 for x in v) and not any(c[0] for c in zd8 if c), f"ZD08's two-scale ladder loses its edge: {', '.join(two)} never-doubling dwarfs clash with the corrected two-scale reading against {one} for one scale (committed two-scale {two_c}); ZD08 prints its percentages as fixed text, so read the counts")
    v = col("G183 pooled n-free fit n"); se = col("G183 pooled n-free fit n SE")
    check("C10 [G183] the pooled n-free exponent moves from 3.16 +/- 0.35 (above the subluminality line 2.01) to within 2 sigma of n = 2 in every variant",
          f"n = {', '.join(f'{a:.2f} +/- {b:.2f}' for a, b in zip(v, se))}", all(abs(a - 2) < 2 * b for a, b in zip(v, se)))
    v = col("G158 slope channel n (pooled per galaxy)"); zz = col("G158 slope channel sigma from n = 2")
    check("S1 [G158 -> falsifier row 11] a verdict the correction does NOT change: the slope channel stays at n = 1.2 and more than 10 sigma from n = 2 in every variant",
          f"n = {', '.join(f'{x:.3f}' for x in v)} ({', '.join(f'{x:.1f}' for x in zz)} sigma from 2; committed 1.203, 12.7 sigma); the AMPLITUDE channel moves "
          f"{', '.join(f'{x:.2f}' for x in col('G158 pooled amplitude n'))} (committed 2.21), so the 'two-scale' explanation that reconciled the channels loses its wedge",
          all(abs(x - 1.203) < 0.1 for x in v) and all(x > 10 for x in zz), "the per-galaxy log slope barely moves with a per-galaxy mass-to-light ratio, so the correction leaves row 11 where it was; whether row 11 tests the law at all is D04's question")
    check("S2 [N01] a verdict that does NOT change: the density-locality law a0(rho_local) stays killed (kill (c)) in every variant",
          ", ".join(col("N01 kill (c) fired, gas/tot")), all(x == "True/True" for x in col("N01 kill (c) fired, gas/tot")),
          "N01's quoted 'measured deep a0_eff ~6.4-6.8e-11' is replaced, but a0(rho_local) at disc densities misses by 2-3 orders either way")

    banner("VERDICT")
    P("  The corpus v7 m2l_disk values are kinematic fits (R1). Run on 3.6-micron population ratios, the lanes' OWN code (B1: faithful)")
    P("  reverses the SPARC 'deficit' (C1), un-banks the O04b joint (C2), lifts the SPARC anchor above 1 (C3), makes Q02's verdict")
    P("  mass-to-light dependent (C4), dissolves the MIGHTEE 'mirror' at Upsilon_disc 0.5-0.6 (C5, C6), removes the opposite-sign")
    P("  premise of the a0(z) impossibility leg (C7), removes the 6.4e-11 'wedge' (C8, C9) and moves the pooled n-free exponent")
    P("  (C10: consistent with 2). Unchanged by the correction: the G158 slope channel (n = 1.2, falsifier row 11; D04 asks whether")
    P("  it tests the law) and the N01 kill (S1, S2).")
    P("  Even corrected, the alpha = 1 moment a0_eff is not the in-force kernel's a0 (D01 D5: +17-26 per cent for nu_RAR data).")
    nfail = sum(1 for _, ok, lb in CH if lb and not ok)
    P(f"\n  {sum(1 for _, ok, _l in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nfail}" + ("  (MUTATE: the C-checks must fail)" if MUTATE else ""))

    json.dump({"mutate": MUTATE, "root_cause": {"r_log": r_ml, "median_ratio_corpus_over_newtonian": float(ratio)}, "headline": H,
               "variants": VARIANTS, "checks": [{"name": n, "ok": ok, "load_bearing": lb} for n, ok, lb in CH]},
              open(os.path.join(HERE, "D02_results" + ("_MUTATE" if MUTATE else "") + ".json"), "w"), indent=1, default=str)
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
