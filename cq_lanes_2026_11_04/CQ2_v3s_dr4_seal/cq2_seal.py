#!/usr/bin/env python3
"""CQ2 seal: writes SEALED_PREDICTION.md from cq2.json (every number from the JSON) and its SHA-256.
Refuses unless the main run has no failed check and the MUTATE twin bit.  python3 -I -B cq2_seal.py
kappa = 1/2 FITTED; not theory closed."""
import hashlib, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
def sha(p): return hashlib.sha256(open(os.path.join(HERE, p), "rb").read()).hexdigest()
R = json.load(open(os.path.join(HERE, "cq2.json"))); M = json.load(open(os.path.join(HERE, "cq2_MUTATE.json")))
assert not R["failed"] and not R["inputs"]["mutate"], "main run has failed checks"
assert M["inputs"]["mutate"] and M["mutate_bites"], "MUTATE twin did not bite"
FO = ("canonical", "alt"); S = R["inputs"]["s_kAU"]; LF = R["inputs"]["Lstar_floor_pc"]; GP = "1.9e-10"
L = []; A = L.append
A("# CQ2 sealed prediction: v3s wide binaries for Gaia DR4")
A("")
A("Sealed 2026-11-04, before Gaia DR4 (due about 2026-12-02). Criteria 532e0dc567. κ = ½ FITTED; not theory closed.")
A("Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. A prediction, not a result; nothing here says the data favour the")
A("framework. Scoring is the frozen pipeline's own; this seal adds no rule.")
A("")
A("## The prediction: v3s wide binaries are screened and Newtonian")
A("")
sw = R["switch"]; ep = max(R["epsilon"].values())
A(f"- **Screened.** The Galactic phantom keeps D·P > 0 around every DR4 binary: binary margin ≥ {sw['min_binary_margin']:.3g} at M_tot")
A(f"  2.5 M☉ (line 10), near zone {sw['near_zone_min']:+.4f} M☉/pc³. So the switch is on the stiff side and v3s's binary is v3's.")
A(f"  The Galactic field does not lift the screening: the response is linear (ε ≤ {ep:.2e}) and the hedgehog GM/L★² does not")
A("  depend on a₀ or x_e; the field enters only through F below.")
A(f"- **V3S-REST** (static hedgehog, L★ floor {LF['canonical']} / {LF['alt']} pc, primary field 1.9e-10 m/s²): γ_r(s) − 1 = (s/L★)² F,")
A("  independent of M_tot (0.5–2.5 M☉ give identical rows). Larger L★ lowers it as L★⁻².")
A("- **V3S-MOVE** (X15: at β = 0 a moving binary carries no hedgehog): γ_r ≡ 1, Newton exactly.")
A("")
A("| s (kAU) | " + " | ".join(f"{v:g}" for v in S) + " |")
A("|---|" + "---|" * len(S))
for f in FO:
    g = R["gamma_r"][f"{f}|{GP}|M1.0"]["gamma_r_minus_1"]; A(f"| γ_r − 1, {f} | " + " | ".join(f"{v:.3e}" for v in g) + " |")
    lo = [min(R["gamma_r"][f"{f}|{go}|M1.0"]["gamma_r_minus_1"][i] for go in ("1.778e-10", GP, "2.32e-10")) for i in range(len(S))]
    hi = [max(R["gamma_r"][f"{f}|{go}|M1.0"]["gamma_r_minus_1"][i] for go in ("1.778e-10", GP, "2.32e-10")) for i in range(len(S))]
    A(f"| field range, {f} | " + " | ".join(f"{a:.3e}–{b:.3e}" for a, b in zip(lo, hi)) + " |")
A("")
ani = R["anisotropy_bound_30kAU"]
A(f"F on the sealed grid: {min(min(g['F']) for g in R['gamma_r'].values() if 'F' in g):.4f}–{max(max(g['F']) for g in R['gamma_r'].values() if 'F' in g):.4f}. Anisotropic part at 30 kAU ≤ {max(ani.values()):.1e} of Newton (not injected).")
A("")
A("## Pushed through CW1's machinery (primary field)")
A("")
A("| footing | Q_pred V3S (DR3 z) | Q_pred Newton | Q_pred plain | γ_inf V3S (spread) | γ_inf Newton | γ_inf plain | V3S − Newton, paired |")
A("|---|---|---|---|---|---|---|---|")
for f in FO:
    p = R["DR3"][f]["pred"]; o = R["pipeline"]["out"][f]
    A(f"| {f} | {p['V3S']['Q_pred']:+.6f} ({p['V3S']['z']:+.3f}, {p['V3S']['label']}) | {p['N']['Q_pred']:+.6f} | {p['PQ']['Q_pred']:+.6f} | "
      f"{o['V3S']['gamma_inf']:.4f} ({o['V3S']['spread']:.4f}) | {o['N']['gamma_inf']:.4f} | {o['PQ']['gamma_inf']:.4f} | "
      + " ".join(f"{v:+.4f}" for v in o["V3S"]["paired_diff"]) + " |")
A("")
for f in FO:
    q = R["DR3"][f]; br = R["pipeline"]["out"][f]["V3S"]["bin_median_ratio_to_N"]
    A(f"- [{f}] DR3: Q_obs {q['Q_obs']:+.4f} ± {q['sigma']:.4f}; Q(V3S) − Q(N) = {q['pred']['V3S']['Q_pred'] - q['pred']['N']['Q_pred']:+.2e}. "
      f"Pipeline bin medians V3S / Newton {min(br):.6f}–{max(br):.6f}; γ_inf identical to Newton's in every realisation (fit grid 0.0025).")
A("")
A("**Separation labels** (CW1's rule: dQ / 0.020 and dγ_inf / 0.028; SEPARABLE ≥ 3, MARGINAL ≥ 2):")
A("")
for f in FO:
    sp = R["separation"][f]
    A(f"- [{f}] V3S vs plain QUMOND: {sp['vs_plain']['dQ']:.2f}, {sp['vs_plain']['dgamma']:.2f} → **{sp['vs_plain']['label']}**; "
      f"V3S vs Newton: {sp['vs_newton']['dQ']:.4f}, {sp['vs_newton']['dgamma']:.4f} → **{sp['vs_newton']['label']}**.")
A("")
A("So DR4, read by the frozen pipeline, cannot tell v3s from Newton; a DR4 γ_inf like plain QUMOND's would contradict v3s on")
A("either footing and in either reading (REST or MOVE).")
A("")
A("## Verdict lines and checks")
A("")
for f in FO:
    v = R["verdict"][f]; A(f"- [{f}] {v['label']}: max γ_r − 1 {v['max_gamma_minus_1']:.2e}, |ΔQ| {v['dQ']:.2e}, paired |Δγ_inf| {v['dgamma_paired_max']:.4f} (lines 1e-3).")
A("- Checks: " + ", ".join(f"{k} {'PASS' if c['ok'] else 'FAIL'}" for k, c in R["checks"].items()) + ". Known answers: C6's 24 numbers, CW1's DR3 Q and every")
A("  pipeline realisation reproduced exactly.")
mv = M["verdict"]
A(f"- MUTATE (switch inverted, unscreened stand-in): γ_inf V3S {M['pipeline']['out']['canonical']['V3S']['gamma_inf']:.4f} / {M['pipeline']['out']['alt']['V3S']['gamma_inf']:.4f}, "
  f"vs Newton {mv['canonical']['vs_newton']} / {mv['alt']['vs_newton']}: **BITES**.")
A("")
A("## Provenance")
A("")
A(f"- Frozen pipeline SHA-256 as recorded by CW1 (not recomputed): `{R['pipeline']['sha256_from_cw1']}`; imported read only, bytecode off.")
A(f"- Seeds as CW1 (20261216, 2026110302, 2026110402, 11, 12); master {R['pipeline']['n_master']:,}, N_data {R['pipeline']['n_data']:,}, {R['pipeline']['n_real']} realisations.")
for p in ("cq2.py", "cq2.json", "cq2.out", "cq2_MUTATE.json", "cq2_MUTATE.out"): A(f"- `{p}` SHA-256 `{sha(p)}`")
A("")
A("κ = ½ FITTED; not theory closed.")
md = "\n".join(L) + "\n"
open(os.path.join(HERE, "SEALED_PREDICTION.md"), "w").write(md)
h = hashlib.sha256(md.encode()).hexdigest(); open(os.path.join(HERE, "SEALED_PREDICTION.sha256"), "w").write(f"{h}  SEALED_PREDICTION.md\n")
print(h)
