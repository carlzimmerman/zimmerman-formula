#!/usr/bin/env python3
"""PARAMRED lane B (SUPPLY). Deterministic, pure python, no arrays, < 1 s.

Modes (environment variable PARAMRED_B_MODE):
  PREDICT  : derives the closure predictions. Contains NO target constant and reads NO ledger file.
             Writes B_predictions.json next to this script.
  COMPARE  : (run only after Part 2 of FROZEN_CRITERIA.md is written) reads B_predictions.json, the target, and the
             CFG721 ladder (read-only, control N1 only). Writes B_results.json and B_compare.out.
  With PARAMRED_B_MUTATE=1 (COMPARE): the same analysis on the mutated closures; writes B_results_MUTATE.json.
Every margin is taken from the JSON it writes. See FROZEN_CRITERIA.md.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.98847e30
GYR = 3.15576e16
KAPPA = 0.5
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
BASE = dict(t0=13.8 * GYR, f_c=0.10, omega_b=0.02237, omega_m=0.14237, rho_crit_h=1.87847e-26,
            omega_lambda=0.685, ell_mult=1.0, rho_kind="b", mass_in_zerog="tot")
GRID = [9, 10, 11, 12, 13, 14, 15]
LADDER = os.path.join(HERE, "..", "..", "CFG721_supply_overflow", "cfg721_results.json")


def h_f(a0):                       # footing-native Hubble rate: a0 = kappa c sqrt(G rho) , H^2 = 8 pi G rho / 3
    return math.sqrt(8 * math.pi / 3) * a0 / (KAPPA * C)


def h_lambda(foot, p):
    h = h_f(A0[foot])
    return h if foot == "canonical" else h * math.sqrt(p["omega_lambda"])


def solve_pow(a, e):               # x = a (1+x)^e, e < 1, positive root by bisection
    lo, hi = 0.0, (2 * a + 2) ** (1.0 / (1.0 - e)) + 10.0     # f(hi) > 0 for any a, e < 1
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid - a * (1 + mid) ** e > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def x_cap(M, foot, p):             # C1 / C2a : supply edge = turnaround basin edge
    a0 = A0[foot]
    Mcat = M / p["f_c"]
    A = math.sqrt(M * a0 / G) * (8 * G * Mcat * p["t0"] ** 2 / math.pi ** 2) ** (1 / 3) / Mcat
    return solve_pow(A, 1 / 3)


def a_cap(M, foot, p):             # the same A(M), used for the analytic cap/supply ratio (control N1)
    a0 = A0[foot]
    Mcat = M / p["f_c"]
    return math.sqrt(M * a0 / G) * (8 * G * Mcat * p["t0"] ** 2 / math.pi ** 2) ** (1 / 3) / Mcat


def x_c2b(M, foot, p):             # supply edge = zero-gravity basin edge
    a0, H = A0[foot], h_lambda(foot, p)
    if p["mass_in_zerog"] == "tot":
        nu = a0 ** 0.75 / ((G * M) ** 0.25 * H)
    else:                          # MUTATE m3: zero-g radius from the source mass only
        nu = a0 ** 0.5 / ((G * M) ** (1 / 6) * H ** (2 / 3))
    return p["f_c"] * (nu - 1.0)


def x_c3a(M, foot, p):             # capacity saturated by the catchment-averaged supply surface density at r_ta
    a0 = A0[foot]
    Mcat = M / p["f_c"]
    B = a0 * (8 * G * Mcat * p["t0"] ** 2 / math.pi ** 2) ** (2 / 3) / (G * Mcat)
    return solve_pow(B, 2 / 3)


def x_c3b(foot, p, diameter):      # capacity saturated by the cosmic baryon column
    a0, H = A0[foot], h_f(A0[foot])
    om = p["omega_b"] if p["rho_kind"] == "b" else p["omega_m"]
    rho = om * p["rho_crit_h"]
    ell = (2.0 if diameter else 1.0) * p["ell_mult"] * C / H
    return (a0 / (math.pi * G)) / (rho * ell)


def native_masses(foot):
    a0, H = A0[foot], h_f(A0[foot])
    return {"M_H": C ** 3 / (2 * G * H) / MSUN, "M_a": C ** 4 / (G * a0) / MSUN}


def families(foot, p):
    """Return {closure: {logM: x}} for the declared grid and native masses, plus the mass-free C3b numbers."""
    out = {"C2a": {}, "C2b": {}, "C3a": {}}
    for lg in GRID:
        M = 10.0 ** lg * MSUN
        out["C2a"][lg] = x_cap(M, foot, p)
        out["C2b"][lg] = x_c2b(M, foot, p)
        out["C3a"][lg] = x_c3a(M, foot, p)
    nat = {}
    for k, v in native_masses(foot).items():
        M = v * MSUN
        nat[k] = {"M_src_msun": v, "C2a": x_cap(M, foot, p), "C2b": x_c2b(M, foot, p), "C3a": x_c3a(M, foot, p)}
    return out, nat


def slope(d):                      # d ln x / d ln M over the grid, least squares
    ks = sorted(d)
    xs = [math.log(10.0 ** k) for k in ks]
    ys = [math.log(d[k]) if d[k] > 0 else float("nan") for k in ks]
    if any(math.isnan(y) for y in ys):
        return None
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)


def predict(p):
    res = {"settings": {k: v for k, v in p.items()}, "grid_log10_Msrc": GRID, "footings": {}}
    n_pred = 0
    for foot in A0:
        fam, nat = families(foot, p)
        entry = {"a0": A0[foot], "H_f": h_f(A0[foot]), "H_L": h_lambda(foot, p), "native_masses_msun": native_masses(foot)}
        for k in fam:
            vals = {str(g): v for g, v in fam[k].items()}
            pos = [v for v in fam[k].values() if v > 0]
            entry[k] = {"x_pred": vals, "slope_dlnx_dlnM": slope(fam[k]),
                        "max_over_min": (max(pos) / min(pos)) if len(pos) == len(GRID) else None}
            n_pred += len(GRID)
        entry["C3b_R"] = x_c3b(foot, p, False)
        entry["C3b_D"] = x_c3b(foot, p, True)
        n_pred += 2
        entry["native_rows"] = nat
        n_pred += 3 * len(nat)
        # C1 bound table: the largest x with no overflow up to M_max
        entry["C1_bound_xle"] = {str(g): fam["C2a"][g] for g in (13, 14, 15)}
        entry["C4"] = None            # no numeric prediction on the record (needs F_S4 and M_typ)
        # regime/identity table: set of x for which the tether holds ALL supply is the interval [0, x_cap(M)]
        entry["tether_holds_all_interval_upper"] = {str(g): fam["C2a"][g] for g in GRID}
        res["footings"][foot] = entry
    res["n_distinct_predictions_per_footing"] = n_pred // 2
    res["n_hypotheses"] = 7
    return res


def main():
    mode = os.environ.get("PARAMRED_B_MODE", "").upper()
    if mode == "PREDICT":
        res = predict(dict(BASE))
        with open(os.path.join(HERE, "B_predictions.json"), "w") as f:
            json.dump(res, f, indent=1)
        lines = ["PARAMRED B_SUPPLY PREDICT (no target, no ledger file)"]
        for foot, e in res["footings"].items():
            lines.append(f"-- footing {foot}  a0={e['a0']:.4e}  H_f={e['H_f']:.4e} 1/s  H_L={e['H_L']:.4e} 1/s")
            for k in ("C2a", "C2b", "C3a"):
                v = e[k]["x_pred"]
                lines.append(f"  {k}: " + " ".join(f"{g}:{v[str(g)]:.4g}" for g in GRID)
                             + f" | slope {e[k]['slope_dlnx_dlnM']} max/min {e[k]['max_over_min']}")
            lines.append(f"  C3b_R {e['C3b_R']:.4g}   C3b_D {e['C3b_D']:.4g}")
            for k, v in e["native_rows"].items():
                lines.append(f"  native {k} M_src={v['M_src_msun']:.3e}: C2a {v['C2a']:.4g} C2b {v['C2b']:.4g} C3a {v['C3a']:.4g}")
        lines.append(f"N distinct predictions per footing = {res['n_distinct_predictions_per_footing']}; hypotheses = {res['n_hypotheses']}")
        txt = "\n".join(lines)
        with open(os.path.join(HERE, "B_predict.out"), "w") as f:
            f.write(txt + "\n")
        print(txt)
        return 0
    if mode == "COMPARE":
        return compare()
    print("set PARAMRED_B_MODE=PREDICT or COMPARE")
    return 2


# ---------------------------------------------------------------- COMPARE stage (target enters only here)
TARGET, SIGMA_T = 5.364, 0.065
W = 2 * SIGMA_T
P1 = (2 * W / TARGET) / math.log(10)
R0_LIMIT = 1 + 2 * SIGMA_T / TARGET


def crossing_logM(fn, foot, p, lo=5.0, hi=30.0):
    """Mass at which fn(M)=TARGET (bisection on log10 M); None if no sign change. POST-HOC."""
    f = lambda lg: fn(10.0 ** lg * MSUN, foot, p) - TARGET
    a, b = f(lo), f(hi)
    if a * b > 0:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if a * fm <= 0:
            hi, b = mid, fm
        else:
            lo, a = mid, fm
    return 0.5 * (lo + hi)


def analyze(p, pred_path=None):
    res = {"settings": {k: v for k, v in p.items()}, "footings": {}}
    pred = predict(p)               # recomputed from the same functions; equality with frozen file checked for baseline
    for foot in A0:
        e = pred["footings"][foot]
        fe = {"closures": {}}
        for k, fn in (("C2a", x_cap), ("C2b", x_c2b), ("C3a", x_c3a)):
            vals = e[k]["x_pred"]
            hits = [int(g) for g in GRID if abs(vals[str(g)] - TARGET) <= W]
            fe["closures"][k] = {
                "x_pred": vals, "hits_in_window_at_grid": hits,
                "R0_mass_independent": (e[k]["max_over_min"] is not None and e[k]["max_over_min"] <= R0_LIMIT),
                "max_over_min": e[k]["max_over_min"], "slope": e[k]["slope_dlnx_dlnM"],
                "implied_crossing_log10Msrc_POSTHOC": crossing_logM(fn, foot, p),
            }
        for k in ("C3b_R", "C3b_D"):
            v = e[k]
            fe["closures"][k] = {"x_pred": v, "R0_mass_independent": True, "in_window": abs(v - TARGET) <= W,
                                 "rel_dev": (v - TARGET) / TARGET}
        nat = {}
        for nk, nv in e["native_rows"].items():
            nat[nk] = {kk: (vv if kk == "M_src_msun" else vv) for kk, vv in nv.items()}
            nat[nk]["any_in_window"] = any(abs(nv[c] - TARGET) <= W for c in ("C2a", "C2b", "C3a"))
        fe["native_rows"] = nat
        # C4 implied free fraction (post-hoc; uses the target)
        fe["C4_implied_free_fraction_at_target"] = {str(g): max(0.0, 1.0 - e["C2a"]["x_pred"][str(g)] / TARGET) for g in GRID}
        res["footings"][foot] = fe
    res["N_pred"] = pred["n_distinct_predictions_per_footing"]
    res["p1"] = P1
    res["p_LE"] = 1 - (1 - P1) ** res["N_pred"]
    return res, pred


def verdict(res):
    out = {}
    for k in ("C2a", "C2b", "C3a", "C3b_R", "C3b_D"):
        r0 = all(res["footings"][f]["closures"][k]["R0_mass_independent"] for f in A0)
        if k.startswith("C3b"):
            r1 = all(res["footings"][f]["closures"][k]["in_window"] for f in A0)
        else:
            r1 = all(len(res["footings"][f]["closures"][k]["hits_in_window_at_grid"]) > 0 for f in A0)
        native_hit = all(res["footings"][f]["native_rows"][n]["any_in_window"] for f in A0 for n in res["footings"][f]["native_rows"])
        out[k] = {"R0": r0, "R1_both_footings": r1, "native_mass_rule_hits": native_hit}
    out["C1"] = {"note": "identical numbers to C2a (same equation at M_max); bound x <= x_cap(M_max), equality only at the boundary"}
    out["C4"] = {"note": "no numeric prediction possible on the record (F_S4, M_typ not derived); implied F(M) reported"}
    return out


def n1_control(p):
    """Analytic cap/supply vs the CFG721 ladder (read-only): trend and onset mass."""
    with open(LADDER) as f:
        D1 = json.load(f)["D1"]
    out = {}
    ok = True
    for foot in A0:
        key = f"z0.0|mono|{foot}|all|fc1.0"
        d = D1[key]
        lm, cs, lof = d["lMb"], d["cap_over_supply"], d["lMb_OF"]
        # ledger slope per dex between 9 and 15
        sl_led = (math.log(cs[-1]) - math.log(cs[0])) / (lm[-1] - lm[0])
        # analytic cap/supply at x_ref = TARGET (the ladder's own supply normalisation): phi = A (1+x)^(1/3) / x
        phi = [a_cap(10.0 ** g * MSUN, foot, p) * (1 + TARGET) ** (1 / 3) / TARGET for g in lm]
        sl_an = (math.log(phi[-1]) - math.log(phi[0])) / (lm[-1] - lm[0])
        sl_pred = -math.log(10) / 6
        # analytic onset (phi = 1), log interpolation
        onset = None
        for i in range(len(lm) - 1):
            if (phi[i] - 1) * (phi[i + 1] - 1) <= 0:
                t = (math.log(1) - math.log(phi[i])) / (math.log(phi[i + 1]) - math.log(phi[i]))
                onset = lm[i] + t * (lm[i + 1] - lm[i])
        c_slope = abs(sl_an / sl_pred - 1) < 0.01 and abs(sl_led / sl_pred - 1) < 0.02
        c_onset = onset is not None and abs(onset - lof) <= 0.25
        ok = ok and c_slope and c_onset
        out[foot] = {"ledger_slope_per_dex": sl_led, "analytic_slope_per_dex": sl_an, "predicted_slope_per_dex": sl_pred,
                     "ledger_onset_log10M": lof, "analytic_onset_log10M": onset,
                     "ratio_analytic_over_ledger_phi": [a / b for a, b in zip(phi, cs)],
                     "pass_slope": c_slope, "pass_onset": c_onset}
    out["N1_pass"] = ok
    return out


def ladder_variant():
    """POST-HOC. x_cap(M) normalised to the CFG721 ladder (PM r_ta). Circular at the calibration mass: the ladder was run with
    supply = 5.364 x catchment baryons, so cap/supply = 1 reproduces 5.364 by construction. Only the slope is information."""
    with open(LADDER) as f:
        D1 = json.load(f)["D1"]
    out = {}
    for foot in A0:
        d = D1[f"z0.0|mono|{foot}|all|fc1.0"]
        xs = []
        for phi in d["cap_over_supply"]:
            a = TARGET * phi / (1 + TARGET) ** (1 / 3)
            xs.append(solve_pow(a, 1 / 3))
        lm = d["lMb"]
        out[foot] = {"lMb": lm, "x_cap_ladder": xs, "max_over_min": max(xs) / min(xs),
                     "F_implied_free_fraction_at_target": [max(0.0, 1 - x / TARGET) for x in xs],
                     "R0_mass_independent": (max(xs) / min(xs)) <= R0_LIMIT,
                     "note": "circular at the calibration mass; slope only is information"}
    return out


def posthoc_total_matter():
    """POST-HOC, noticed AFTER the COMPARE stage showed C3b-R canonical = 6.405 close to Omega_m/Omega_b = 6.364.
    Reading: the TOTAL matter column rho_m c/H_L (not the tethered cold column) saturates a0/(pi G). Not a frozen closure.
    R_m = rho_m c/H_L / (a0/(pi G)) = (3/8)(Om/OL) / (kappa sqrt(3/(8 pi)))  (canonical footing; H_L from a0 and kappa)."""
    out = {}
    for name, om in (("Omega_m=0.315 (CMB-like)", 0.315), ("Omega_m=0.2975 (DESI DR2 BAO-alone, on disk in CFG642 criteria)", 0.2975)):
        ol = 1 - om
        a0_over_cH = KAPPA * math.sqrt(3 / (8 * math.pi))
        rm = 0.375 * (om / ol) / a0_over_cH
        kappa_impl = 0.375 * (om / ol) / math.sqrt(3 / (8 * math.pi))
        out[name] = {"R_m_canonical": rm, "kappa_implied_if_R_m_equals_1": kappa_impl}
    # alt footing: H_f = H0 and Omega_m h^2 fixed -> R_m = Omega_m * pi sqrt(3/(8 pi)) / kappa
    out["alt_footing_R_m (Omega_m=0.315)"] = 0.315 * math.pi * math.sqrt(3 / (8 * math.pi)) / KAPPA
    x_r = x_c3b("canonical", dict(BASE), False)
    out["canonical: (1+x) read as Omega_m/Omega_b from C3b-R"] = {"one_plus_x": x_r, "x": x_r - 1.0,
                                                                   "dev_sigma_from_target": (x_r - 1.0 - TARGET) / SIGMA_T}
    x_ra = x_c3b("alt", dict(BASE), False)
    out["alt: (1+x) read as Omega_m/Omega_b from C3b-R"] = {"one_plus_x": x_ra, "x": x_ra - 1.0,
                                                             "dev_sigma_from_target": (x_ra - 1.0 - TARGET) / SIGMA_T}
    out["trials_counted_including_this_one"] = 30
    out["p_LE_30"] = 1 - (1 - P1) ** 30
    return out


def mutants():
    ms = {}
    p = dict(BASE); p["rho_kind"] = "m"; ms["m1_C3b_rho_m_for_rho_b"] = p
    p = dict(BASE); p["ell_mult"] = 3.0; ms["m2_C3b_ell_3c_over_H"] = p
    p = dict(BASE); p["mass_in_zerog"] = "src"; ms["m3_C2b_zerog_from_source_mass_only"] = p
    p = dict(BASE); p["f_c"] = 0.90; ms["m4_f_c_0p90"] = p
    p = dict(BASE); p["t0"] = 2 * BASE["t0"]; ms["m5_t0_doubled"] = p
    return ms


def compare():
    pf = os.path.join(HERE, "B_predictions.json")
    if not os.path.exists(pf):
        print("run PREDICT first"); return 2
    frozen = json.load(open(pf))
    mut = os.environ.get("PARAMRED_B_MUTATE", "") == "1"
    if not mut:
        res, pred = analyze(dict(BASE))
        # frozen-prediction integrity: the recomputed numbers must equal the frozen file exactly
        same = json.dumps(pred["footings"], sort_keys=True) == json.dumps(frozen["footings"], sort_keys=True)
        res["frozen_predictions_unchanged"] = same
        res["verdict_by_closure"] = verdict(res)
        res["N1_control"] = n1_control(dict(BASE))
        res["ladder_variant_POSTHOC"] = ladder_variant()
        res["total_matter_reading_POSTHOC"] = posthoc_total_matter()
        any_pass = any(v.get("R0") and v.get("R1_both_footings") for k, v in res["verdict_by_closure"].items() if k.startswith("C2") or k.startswith("C3"))
        res["REDUCTION_DERIVED_any"] = bool(any_pass and res["p_LE"] < 0.05)
        res["overall"] = "REDUCTION DERIVED" if res["REDUCTION_DERIVED_any"] else "NO REDUCTION"
        outj, outt = "B_results.json", "B_compare.out"
    else:
        base, _ = analyze(dict(BASE))
        res = {"mutants": {}}
        for name, p in mutants().items():
            r, _ = analyze(p)
            r["verdict_by_closure"] = verdict(r)
            # crossing-mass shift relative to baseline, mass-dependent families only
            shifts = {}
            for foot in A0:
                for k in ("C2a", "C2b", "C3a"):
                    b = base["footings"][foot]["closures"][k]["implied_crossing_log10Msrc_POSTHOC"]
                    m = r["footings"][foot]["closures"][k]["implied_crossing_log10Msrc_POSTHOC"]
                    shifts[f"{foot}|{k}"] = {"base": b, "mutant": m, "delta_dex": (None if b is None or m is None else m - b)}
            r["crossing_shift"] = shifts
            for foot in A0:
                for k in ("C3b_R", "C3b_D"):
                    r.setdefault("c3b", {})[f"{foot}|{k}"] = {"base": base["footings"][foot]["closures"][k]["x_pred"],
                                                              "mutant": r["footings"][foot]["closures"][k]["x_pred"],
                                                              "mutant_in_window": r["footings"][foot]["closures"][k]["in_window"]}
            res["mutants"][name] = r
        outj, outt = "B_results_MUTATE.json", "B_compare_MUTATE.out"
    with open(os.path.join(HERE, outj), "w") as f:
        json.dump(res, f, indent=1)
    # text summary from the JSON just written
    J = json.load(open(os.path.join(HERE, outj)))
    L = []
    if not mut:
        L.append(f"TARGET {TARGET} +- {SIGMA_T}; window +-{W:.3f}; p1 {J['p1']:.4f}; N_pred {J['N_pred']}; p_LE {J['p_LE']:.4f}")
        L.append(f"frozen predictions unchanged: {J['frozen_predictions_unchanged']}   N1 control pass: {J['N1_control']['N1_pass']}")
        for foot in A0:
            fe = J["footings"][foot]
            L.append(f"-- {foot}")
            for k, c in fe["closures"].items():
                if k.startswith("C3b"):
                    L.append(f"  {k}: x_pred {c['x_pred']:.4g} rel dev {c['rel_dev']:+.3f} in_window {c['in_window']}")
                else:
                    L.append(f"  {k}: slope {c['slope']:.3f} max/min {c['max_over_min']} R0 {c['R0_mass_independent']} hits {c['hits_in_window_at_grid']} crossing(post-hoc) log10M {c['implied_crossing_log10Msrc_POSTHOC']}")
            L.append("  native rows: " + "; ".join(f"{n}: any_in_window {v['any_in_window']}" for n, v in fe["native_rows"].items()))
            L.append("  C4 implied free fraction F(M) at x=target: " + " ".join(f"{g}:{v:.2f}" for g, v in fe["C4_implied_free_fraction_at_target"].items()))
        L.append("verdict_by_closure: " + json.dumps(J["verdict_by_closure"]))
        for foot in A0:
            n = J["N1_control"][foot]
            L.append(f"N1 {foot}: slope ledger {n['ledger_slope_per_dex']:.4f} analytic {n['analytic_slope_per_dex']:.4f} predicted {n['predicted_slope_per_dex']:.4f}; onset ledger {n['ledger_onset_log10M']:.3f} analytic {n['analytic_onset_log10M']}")
        for foot in A0:
            lv = J["ladder_variant_POSTHOC"][foot]
            L.append(f"ladder variant (POST-HOC, circular at calibration) {foot}: x_cap " + " ".join(f"{g}:{v:.3g}" for g, v in zip(lv['lMb'], lv['x_cap_ladder']))
                     + f" | max/min {lv['max_over_min']:.2f} R0 {lv['R0_mass_independent']}")
            L.append(f"   implied free fraction F(M) at x=target: " + " ".join(f"{g}:{v:.2f}" for g, v in zip(lv['lMb'], lv['F_implied_free_fraction_at_target'])))
        L.append("POST-HOC total-matter column reading (noticed after COMPARE): " + json.dumps(J["total_matter_reading_POSTHOC"]))
        L.append("OVERALL: " + J["overall"])
    else:
        for name, r in J["mutants"].items():
            L.append(f"== {name}")
            L.append("  verdict: " + json.dumps(r["verdict_by_closure"]))
            for kk, v in r["crossing_shift"].items():
                L.append(f"  crossing {kk}: base {v['base']} mutant {v['mutant']} delta_dex {v['delta_dex']}")
            for kk, v in r.get("c3b", {}).items():
                L.append(f"  C3b {kk}: base {v['base']:.4g} mutant {v['mutant']:.4g} mutant_in_window {v['mutant_in_window']}")
    with open(os.path.join(HERE, outt), "w") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    if not mut:
        return 0 if J["N1_control"]["N1_pass"] and J["frozen_predictions_unchanged"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
