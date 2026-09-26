#!/usr/bin/env python3
"""QF1 — Q-functional closure probe (door: L02 MEASURED-ONLY).
Reads deepseek_push/L02_results.json (published E[Q](tau0,q) tables + SEs).
Fits NEW closed-form families per q (weighted LS, residuals in SE units).
Pre-registered kill (L02 verbatim): claimed closed forms must reproduce the
table within 3 SE. Bank gate: in-fit max <= 3 SE AND leave-one-tau0-out
holdout max <= 5 SE, on central AND volume. Exit 0 only if banked; else exit 1
honestly ("closure remains OPEN"). No SE re-tuning (house rule 3).
"""
import json, sys, itertools
import numpy as np

RES = {}
BASE = 0.75  # L02: E[Q] -> 3/4 as tau0 -> 0 (disk: L02_Q_FUNCTIONAL.md / results)

def load_tables(path="L02_results.json"):
    d = json.load(open(path))
    return d["table_central"], d["table_volume"], d.get("families", {})

def fit_linear_family(design, y, w):
    W = np.sqrt(w)[:, None]
    coef, *_ = np.linalg.lstsq(design * W, y * W[:, 0], rcond=None)
    return design @ coef, coef

def resid_se(fit, y, s):
    return np.abs(fit - y) / s

def run_family(name, t, y, s, fitter):
    """fitter(t) -> design matrix (linear in params). Returns (max_se, coef, fit)."""
    design = fitter(t)
    fit, coef = fit_linear_family(design, y, 1.0 / s**2)
    r = resid_se(fit, y, s)
    return r.max(), coef, fit, design

def families_for(t):
    out = {}
    out["F8 rational-power 0.75 + A/(1+t)^p"] = [
        (p, lambda tt, p=p: np.column_stack([np.ones_like(tt), (1.0 + tt) ** (-p)]))
        for p in np.arange(0.2, 4.001, 0.005)]
    out["F9 stretched-exp 0.75 + A*exp(-t^p)"] = [
        (p, lambda tt, p=p: np.column_stack([np.ones_like(tt), np.exp(-(tt ** p))]))
        for p in np.arange(0.2, 3.001, 0.005)]
    out["F10 two-power 0.75 + A t^-p1 + B t^-p2"] = [
        ((p1, p2), lambda tt, p1=p1, p2=p2: np.column_stack(
            [np.ones_like(tt), tt ** (-p1), tt ** (-p2)]))
        for p1, p2 in itertools.product(np.arange(0.2, 3.001, 0.05), repeat=2)]
    return out

def evaluate(tbl):
    per_q = {}
    for row in tbl:
        per_q.setdefault(row["q"], []).append(row)
    results = {}
    for q, rows in sorted(per_q.items()):
        rows = sorted(rows, key=lambda r: r["tau0"])
        t = np.array([r["tau0"] for r in rows]); y = np.array([r["E_Q"] for r in rows])
        s = np.array([r["s_Q"] for r in rows])
        best = None
        for fam, variants in families_for(t).items():
            for tag, fitter in variants:
                _, design_full = tag, fitter(t)
                fit, coef = fit_linear_family(design_full, y, 1.0 / s**2)
                mx = resid_se(fit, y, s).max()
                if best is None or mx < best[1]:
                    best = (fam, mx, tag)
        # holdout: leave-one-tau0-out with the best family's fitter, refit each drop
        fam, _, tag = best
        p = tag if not isinstance(tag, tuple) else tag
        hold = None
        if len(rows) >= 6:
            fitter = families_for(t)[fam]
            lookup = {k: f for k, f in fitter}
            f = lookup[tag]
            worst = 0.0
            for i in range(len(t)):
                m = np.ones(len(t), bool); m[i] = False
                design = f(t[m])
                fit, coef = fit_linear_family(design, y[m], 1.0 / s[m]**2)
                # predict held-out cell: evaluate basis at t[i] via coef
                basis_i = f(np.array([t[i]]))[0]
                pred = float(basis_i @ coef)
                worst = max(worst, abs(pred - y[i]) / s[i])
            hold = worst
        results[q] = {"family": fam, "tag": [str(tag)], "infit_max_SE": best[1],
                      "holdout_max_SE": hold, "n_cells": len(rows)}
    return results

def main():
    tc, tv, fams = load_tables()
    out = {"title": "QF1 Q-functional closure probe",
           "pre_registered_kill": "L02 verbatim: claimed closed forms must reproduce table within 3 SE; bank gate <=3 SE in-fit AND <=5 SE holdout",
           "prior_best": {"family": "F5", "max_resid_SE": fams.get("F5", {}).get("max_resid_SE")},
           "central": evaluate(tc), "volume": evaluate(tv)}
    worst_in = max(v["infit_max_SE"] for v in list(out["central"].values()) + list(out["volume"].values()))
    holds = [v["holdout_max_SE"] for v in list(out["central"].values()) + list(out["volume"].values()) if v["holdout_max_SE"] is not None]
    worst_hold = max(holds) if holds else None
    out["verdict_infit_max_SE"] = float(worst_in)
    out["verdict_holdout_max_SE"] = None if worst_hold is None else float(worst_hold)
    banked = (worst_in <= 3.0) and (worst_hold is not None and worst_hold <= 5.0)
    out["banked"] = bool(banked)
    out["verdict"] = ("CLOSED-FORM CANDIDATE BANKED (within pre-registered gates; flagged, not promoted without Lean/verification)"
                      if banked else
                      "CLOSURE REMAINS OPEN — no new family within 3 SE in-fit (best %.2f SE vs L02 F5 21.08); honest FAIL, no re-tuning" % worst_in)
    json.dump(out, open("QF1_results.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("verdict_infit_max_SE", "verdict_holdout_max_SE", "banked", "verdict")}, indent=1))
    return 0 if banked else 1

if __name__ == "__main__":
    sys.exit(main())
