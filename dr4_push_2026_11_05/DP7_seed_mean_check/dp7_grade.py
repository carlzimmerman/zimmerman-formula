#!/usr/bin/env python3
"""DP7 grader: CHECK PASSED / CHECK FAILED by FROZEN_CRITERIA.md section 6 (1b87706e49) + AMENDMENT_A1, from the committed outputs only.

Reads k1.json (K1), k2.json (K2), dp7.json (the graded sweep: K3, K4, K5, K6, Delta_bar), dp7_MUTATE1.json (M1), dp7_MUTATE2.json (M2),
dp7_C1.json (AMENDMENT_A1 control C1), dp3_d6_replay.json against the DP3 dry run's sigma_sys_dr3.json (section 4, option off),
dp3_seedmean_d6inputs.json and dp3_seedmean_releasepath.json (section 4, option on: both entries, information only, DR3).
Prints every K and MUTATE with numbers, the cost table, the hand estimates HE-a..d (HIT / MISS) and the label; writes dp7_grade.json / .out.
  python3 -B dp7_grade.py
NON-SCORING: DR3 numbers are code-path tests, never results (Amendment 7(e)). kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import sys
sys.dont_write_bytecode = True
import json, math, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DRY = REPO / "dr4_push_2026_11_05" / "DP3_release_day" / "dry_run_dr3" / "sigma_sys_dr3.json"
FOOTS = ("canonical", "alt")
HE = {"canonical": dict(lo=-0.005, hi=0.015, se=0.007), "alt": dict(lo=-0.005, hi=0.010, se=0.005)}


def load(name):
    p = HERE / name
    return json.loads(p.read_text()) if p.exists() else None


def num_diff(x, y, path="", acc=None):
    """recursive max |x - y| over numbers; keys must match."""
    acc = acc if acc is not None else dict(n=0, max=0.0, bad=[])
    if isinstance(x, dict):
        if set(x) != set(y):
            acc["bad"].append((path, "keys differ", sorted(set(x) ^ set(y)))); return acc
        for k in x:
            num_diff(x[k], y[k], path + "/" + k, acc)
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        acc["n"] += 1; d = abs(x - y); acc["max"] = max(acc["max"], d)
        if d > 1e-9:
            acc["bad"].append((path, x, y))
    elif x != y:
        acc["bad"].append((path, x, y))
    return acc


def main():
    lines, G = [], {}

    def P(s=""):
        print(s, flush=True); lines.append(s)

    def C(cid, cond, detail):
        G[cid] = dict(passed=(None if cond is None else bool(cond)), detail=detail)
        P(f"{cid:4s} {'PASS' if cond else ('MISSING' if cond is None else 'FAIL'):7s} {detail}")
    k1, k2, sw, m1, m2, c1, d6 = (load(n) for n in ("k1.json", "k2.json", "dp7.json", "dp7_MUTATE1.json", "dp7_MUTATE2.json", "dp7_C1.json", "dp3_d6_replay.json"))
    sm_d6, sm_rp = load("dp3_seedmean_d6inputs.json"), load("dp3_seedmean_releasepath.json")
    P("=" * 110)
    P("DP7 GRADE (FROZEN_CRITERIA.md 1b87706e49 section 6 + AMENDMENT_A1): the DR3 code-path check for the seed-mean NSS-off entry")
    P("NON-SCORING: DR3 numbers are code-path tests, never results (Amendment 7(e)). kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    P("=" * 110)
    # K1
    if k1 and k1.get("K1"):
        r = k1["K1"]; m = r["means"]
        C("K1", r["passed"], f"DP1 P4 bit for bit, k {r['ks'][0]}..{r['ks'][-1]}: {r['n_bit_identical']}/{r['n_values']} values identical; mean rung shift "
          + "; ".join(f"{fo} {m[fo]['mean']:+.7f} (DP1 {m[fo]['dp1_mean']:+.7f}, exact {m[fo]['mean_exact']}) SD {m[fo]['sd']:.6f} (DP1 {m[fo]['dp1_sd']:.6f}, exact {m[fo]['sd_exact']})" for fo in FOOTS))
    else:
        C("K1", None, "k1.json missing")
    # K2
    if k2 and k2.get("K2"):
        r = k2["K2"]; p0 = k2
        C("K2", r["passed"], "registered fit at k = 0 = DP1 P3 to 1e-4: " + "; ".join(f"{x['catalogue']} {x['footing']} {x['quantity']} {x['dp7']:.4f} vs {x['dp1_P3']:.4f}" for x in r["rows"])
          + f"; max |diff| {max(x['abs_diff'] for x in r['rows']):.1e}; base sha registered {r['base_sha_is_registered']}, rung sha = DP1 rung {r['rung_sha_is_dp1_rung']}")
    else:
        C("K2", None, "k2.json missing")
    # sweep: K3-K6
    if sw:
        k3 = sw.get("K3") or {}
        C("K3", k3.get("passed"), f"cones-literal k = 0 base {k3.get('n_pairs')} pairs sha256 {k3.get('sha256_prefix')} (ref 6,180 / c5cb89e8f95bfe3d); bytes = dry-run csv on disk: {k3.get('equals_dry_run_csv_on_disk')}")
        k4 = sw["K4"]
        C("K4", k4["passed"], f"extract-builder base_k == G50 build: {k4['n_equal']} of {k4['n_with_g50']} k with a file; k without a file {k4['k_without_g50']}; unequal {k4['k_unequal']}")
        k5 = sw["K5"]
        C("K5", k5["passed"], f"{k5['n_files']} pinned files unchanged before/after the sweep; pipeline {k5['pipeline_sha256'][:8]} (7c884e0e: {k5['pipeline_is_7c884e0e']}); changed {k5['changed_during_run']}; off pinned value {k5['off_pinned_value']}")
        k6 = sw["K6"]
        C("K6", k6["passed"], f"pipeline self-test at seed 20261216 passed on all {k6['n_fits']} fitted catalogues; flagged k {k6['flagged_k']}")
        C("SWEEP", sw["complete"] and sw["K"] == 50 and sw["cut13"] == "cones-literal" and sw["fit_path"] == "pipeline" and sw.get("rung_missing_cones") == "extract-fallback",
          f"K = {sw['K']} {sw['cut13']} {sw['fit_path']} complete {sw['complete']} ({sw['n_k_done']} k); rung missing cones policy {sw.get('rung_missing_cones')} (AMENDMENT_A1)")
    else:
        for c in ("K3", "K4", "K5", "K6", "SWEEP"):
            C(c, None, "dp7.json missing")
    # MUTATE
    if m1 and m1.get("M1"):
        C("M1", m1["M1"]["bites"] and m1["complete"], "--mutate-k0: " + "; ".join(f"{fo} Delta_bar {m1[fo]['delta_bar']:+.6f} vs Delta_0 {m1[fo]['single_seed_shift']:+.6f} (diff {m1['M1'][fo]['delta_bar_minus_single_seed']:+.1e}), SD {m1[fo]['sd']:.1e}, "
          f"entry {m1[fo]['seed_mean_entry']:.6f} vs gamma_hat(rung_0) {m1[fo]['gamma_rung_0']:.6f}, every Delta_k == Delta_0 {m1['M1'][fo]['every_delta_k_bit_identical_to_delta_0']}" for fo in FOOTS) + f"; K {m1['K']} complete {m1['complete']}")
    else:
        C("M1", None, "dp7_MUTATE1.json missing")
    if m2 and m2.get("M2"):
        C("M2", m2["M2"]["bites"] and m2["complete"], "--keep-nss: " + "; ".join(f"{fo} Delta_bar {m2[fo]['delta_bar']:+.1e}, max |Delta_k| {m2['M2'][fo]['max_abs_delta']:.1e} (within 1e-9 every k: {m2['M2'][fo]['every_k_within_1e9']})" for fo in FOOTS)
          + f"; rung bytes == base bytes at every k {m2['M2']['rung_equals_base_bytes_every_k']}; K {m2['K']} complete {m2['complete']}")
    else:
        C("M2", None, "dp7_MUTATE2.json missing")
    # C1 (AMENDMENT_A1 item 3): informational bound; the label stands either way, the number is reported beside it
    if c1:
        G["C1"] = dict(passed=bool(c1["passed"]), detail="; ".join(f"{fo} change {c1[fo]['change']:+.6f} (ref {c1[fo]['gamma_reference']:.4f}, one flagged {c1[fo]['gamma_one_flagged']:.4f})" for fo in FOOTS),
                       below_1e3=bool(c1["passed"]), pair=c1["pick"].get("pair"), pairs_final=[c1["reference"]["n_pairs"], c1["one_flagged"]["n_pairs"]])
        P(f"C1   {'BOUND < 1e-3' if c1['passed'] else 'BOUND = measured change (reported beside the label)':7s} one of {c1['pick'].get('n_uncovered')} uncovered pairs flagged (seed 1103; fallback called once {c1['fallback_called_once']}): {G['C1']['detail']}; final pairs {c1['reference']['n_pairs']} -> {c1['one_flagged']['n_pairs']}"
          + (f"; final pair sets differ by {c1['final_pair_set_difference']['symmetric_difference']} pairs (one flag at cut 13 re-aligns the seeded stage-G vtilde-error MC: the change is one draw of the stage-G seed noise, not a one-pair bias)" if c1.get("final_pair_set_difference") else ""))
    else:
        G["C1"] = dict(passed=None, detail="dp7_C1.json missing")
        P("C1   MISSING dp7_C1.json")
    # section 4
    if d6 and DRY.exists():
        acc = num_diff(d6, json.loads(DRY.read_text()))
        C("S4", not acc["bad"], f"dp3_sigma_sys.py with the option off reproduces the dry run's sigma_sys_dr3.json: {acc['n']} numbers, max |diff| {acc['max']:.1e}, differences beyond 1e-9: {len(acc['bad'])}; (b) {d6['canonical']['b']:.4f} / {d6['alt']['b']:.4f}")
    else:
        C("S4", None, "dp3_d6_replay.json or the dry run json missing")
    # label (section 6)
    req = ("K1", "K2", "K3", "K4", "K5", "K6", "SWEEP", "M1", "M2", "S4")
    passed = all(G[c]["passed"] is True for c in req)
    label = "CHECK PASSED" if passed else "CHECK FAILED"
    P("")
    P(f"LABEL: {label}   ({sum(G[c]['passed'] is True for c in req)}/{len(req)} required checks pass; C1 bound {'below 1e-3' if G['C1'].get('passed') else G['C1']['detail']})")
    # information (section 6): Delta_bar +- SE, SD, single-seed shift, sigma_sys(b) under both entries
    info = {}
    if sw:
        P("\nInformation only, DR3 (no verdict weight):")
        for fo in FOOTS:
            r = sw[fo]
            info[fo] = dict(delta_bar=r["delta_bar"], se=r["se"], sd=r["sd"], K=r["K_done"], single_seed_shift=r["single_seed_shift"], gamma_0=r["gamma_0"], sigma_fit_0=r["sigma_fit_0"],
                            seed_mean_entry=r["seed_mean_entry"], single_seed_entry=r["single_seed_entry"], n42_seed_mean=r["n42_seed_mean"], n42_single_seed=r["n42_single_seed"])
            P(f"  {fo:9s} Delta_bar {r['delta_bar']:+.4f} +- {r['se']:.4f} (SD {r['sd']:.4f}, K {r['K_done']});  single-seed shift Delta_0 {r['single_seed_shift']:+.4f};  gamma_0 {r['gamma_0']:.4f} +- {r['sigma_fit_0']:.4f} (cones-literal, pipeline);  "
              f"seed-mean entry {r['seed_mean_entry']:.4f} vs single-seed entry {r['single_seed_entry']:.4f};  N4.2 on Delta_bar: {r['n42_seed_mean']}")
        for tag, j in (("D6 inputs (NSS-off = the D2 probe)", sm_d6), ("release-day path (NSS-off = DP1 rung)", sm_rp)):
            if j:
                for fo in FOOTS:
                    x = j[fo]
                    info.setdefault("sigma_sys_b", {})[f"{tag}|{fo}"] = dict(single_seed=x.get("b_single_seed"), seed_mean=x.get("b_seed_mean"), e_single=x.get("e_single_seed"), e_seed_mean=x.get("e_seed_mean"))
                    P(f"  sigma_sys(b) {tag:40s} {fo:9s} single-seed {x.get('b_single_seed'):.4f} -> seed-mean {x.get('b_seed_mean'):.4f};  (e) {x.get('e_single_seed'):.4f} -> {x.get('e_seed_mean'):.4f};  spread {x.get('spread_single_seed'):.4f} -> {x.get('spread'):.4f}")
            else:
                P(f"  sigma_sys(b) {tag}: json missing")
    # hand estimates
    he = {}
    if sw:
        for fo, tag in (("canonical", "HE-a"), ("alt", "HE-b")):
            r = sw[fo]; b = HE[fo]
            he[tag] = dict(hit=(b["lo"] <= r["delta_bar"] <= b["hi"] and r["se"] <= b["se"]), delta_bar=r["delta_bar"], se=r["se"], band=[b["lo"], b["hi"]], se_max=b["se"])
            P(f"{tag}: {'HIT' if he[tag]['hit'] else 'MISS'}  Delta_bar {fo} {r['delta_bar']:+.4f} in [{b['lo']:+.3f}, {b['hi']:+.3f}] with SE {r['se']:.4f} <= {b['se']}")
    if sm_d6:
        same = all(abs(sm_d6[fo]["b_single_seed"] - sm_d6[fo]["b_seed_mean"]) < 1e-12 for fo in FOOTS)
        he["HE-c"] = dict(hit=same, detail={fo: [sm_d6[fo]["b_single_seed"], sm_d6[fo]["b_seed_mean"]] for fo in FOOTS})
        P(f"HE-c: {'HIT' if same else 'MISS'}  DR3 sigma_sys(b) unchanged by the seed-mean entry (3-20 kAU rung sets the spread)? (b) " + "; ".join(f"{fo} {sm_d6[fo]['b_single_seed']:.4f} -> {sm_d6[fo]['b_seed_mean']:.4f}" for fo in FOOTS))
    if k1 and k1.get("K1"):
        he["HE-d"] = dict(hit=bool(k1["K1"]["passed"]))
        P(f"HE-d: {'HIT' if k1['K1']['passed'] else 'MISS'}  K1 reproduced bit for bit on the first run")
    # cost
    cost = {}
    for name, j in (("K1 (d2, K 8)", k1), ("K2 (pipeline, k 0)", k2), ("sweep (K 50)", sw), ("M1", m1), ("M2", m2)):
        if j and j.get("cost"):
            c = j["cost"]; fw = c.get("fit_wall_s") or []
            cost[name] = dict(builds=c["builds"], fits=c["fits"], fits_from_cache=c["fits_from_cache"], wall_s=c["wall_total_s"], wall_per_k_s_median=(sorted(c["wall_per_k_s"])[len(c["wall_per_k_s"]) // 2] if c["wall_per_k_s"] else None),
                              fit_wall_s_median=(sorted(fw)[len(fw) // 2] if fw else None), fit_rss_gb_max=c["fit_rss_gb_max"], wrapper_rss_gb=c["wrapper_peak_rss_gb"])
    P("\nCost table (per run):")
    P(f"  {'run':20s} {'builds':>6s} {'fits':>5s} {'cached':>6s} {'wall s':>8s} {'s per k':>8s} {'s per fit':>9s} {'fit RSS GB':>10s} {'wrapper GB':>10s}")
    for n, c in cost.items():
        P(f"  {n:20s} {c['builds']:6d} {c['fits']:5d} {c['fits_from_cache']:6d} {c['wall_s']:8.0f} {c['wall_per_k_s_median'] or 0:8.1f} {c['fit_wall_s_median'] or 0:9.1f} {(c['fit_rss_gb_max'] or 0):10.2f} {c['wrapper_rss_gb']:10.2f}")
    if sw and sw.get("cost"):
        c = sw["cost"]
        P("  per k in the sweep: builds " + ", ".join(f"{x}" for x in [3]) + " (base, rung, extract-builder K4 build); fits 2; wall s per k (min/median/max) "
          f"{min(c['wall_per_k_s']):.0f}/{sorted(c['wall_per_k_s'])[len(c['wall_per_k_s']) // 2]:.0f}/{max(c['wall_per_k_s']):.0f}; fit RSS GB per k (max) {max(max(x) for x in c['fit_rss_gb_per_k'] if all(x)):.2f}")
    out = dict(label=label, checks=G, information=info, hand_estimates=he, cost=cost, criteria="FROZEN_CRITERIA.md 1b87706e49 + AMENDMENT_A1",
               non_scoring="DR3 numbers are code-path tests, never results (Amendment 7(e)); kappa = 1/2 FITTED; footings never pooled; not theory closed")
    (HERE / "dp7_grade.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    (HERE / "dp7_grade.out").write_text("\n".join(lines) + "\n")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
