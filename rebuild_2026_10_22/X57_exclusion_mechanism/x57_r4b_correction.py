"""Post-result A1: regrade only R4b from immutable historical X57 inputs.

No main program or output side effects. The gate_fixes runner owns all writes.
Nonnegative density alone does not impose nonnegative excess surface density.
"""
import copy
import json
import math


def band_entry(cell, nsigma=2.0):
    pred, meas, sigma = (float(cell[k]) for k in ("pred", "meas", "s"))
    if not all(math.isfinite(x) for x in (pred, meas, sigma)) or pred <= 0 or sigma < 0:
        raise ValueError("finite positive prediction and nonnegative uncertainty required")
    lower, upper = meas-nsigma*sigma, meas+nsigma*sigma
    drop = max(0.0, pred-upper)
    return dict(lower=lower, upper=upper, pred=pred, absolute_drop=drop,
                fractional_drop=drop/pred, inside_band=lower <= pred <= upper,
                below_band=pred < lower)


def repair_bound_status(cell, fractional_budget):
    """Necessary-only diagnostic assuming budget is an upper bound on delta A/A."""
    b = band_entry(cell)
    if b["below_band"]:
        return "DOWNWARD CHANGE CANNOT REPAIR UNDERPREDICTION"
    if b["inside_band"]:
        return "BASELINE INSIDE BAND"
    # A tiny tolerance only protects arithmetic equality at an inclusive band edge.
    if b["fractional_drop"] > fractional_budget + 1e-14:
        return "INSUFFICIENT UNDER STATED BOUND"
    return "BOUND DOES NOT EXCLUDE"


def shell_delta_sigma(radius, shell_radius, mass):
    """Exact spherical thin-shell projection; exclude the divergent shell edge."""
    if radius <= 0 or shell_radius <= 0 or mass < 0 or radius == shell_radius:
        raise ValueError("positive radii away from shell edge, nonnegative mass required")
    if radius > shell_radius:
        return mass/(math.pi*radius**2)
    u = math.sqrt(1-(radius/shell_radius)**2)
    return mass/(math.pi*shell_radius**2) * (1/(1+u)-1/(2*u))


def calculate(path):
    old = json.loads(path.read_text())
    budget = old["R4b"]["D"]
    out = dict(correction="X57 post-result A1", historical_source=str(path),
               fractional_deficit_budget_D=budget, footings={},
               interpretation="General radial profiles: unresolved. No achievable deficit or full cluster fit demonstrated.",
               positivity_scope="Nonincreasing projected surface density gives DeltaSigma >= 0. Nonnegative 3D density alone does not.",
               shell_counterexample=dict(R_over_a=0.5, DeltaSigma_in_units_M_over_pi_a2=
                                         shell_delta_sigma(0.5, 1.0, math.pi)))
    for f, cells in old["step0"]["X56law_OUT"].items():
        graded = {hk: dict(**band_entry(c), budget_status=repair_bound_status(c, budget))
                  for hk, c in cells.items()}
        general = "ND (general radial response unresolved; positive density is insufficient)"
        verdicts = copy.deepcopy(old["verdicts"][f])
        for name, entry in verdicts.items():
            entry["lines"] = [[n, general if n == "R4b" else g, detail]
                              for n, g, detail in entry["lines"]]
            entry["all_fails"] = [n for n in entry["all_fails"] if n != "R4b"]
            if not entry["all_fails"]:
                nd = [n for n, g, _ in entry["lines"] if g.startswith("ND")]
                entry["verdict"] = "NOT DECIDABLE WITH RECORD DATA (" + ", ".join(nd) + ")"
        out["footings"][f] = dict(cells=graded, R4b=general, historical_R4b=old["R4b"][f]["grade"],
            monotone_addition_without_deficit="EXCLUDED CONDITIONALLY" if all(
                c["absolute_drop"] > 0 for c in graded.values()) else "NOT EXCLUDED BY BOTH-CELL RULE",
            deficit_bound_excludes_both_cells=all(c["budget_status"] == "INSUFFICIENT UNDER STATED BOUND" for c in graded.values()),
            verdicts=verdicts)
    out["overall"] = "UNDECIDED"
    out["non_claims"] = ["No revalidation of inherited M1-M4 computations", "D is only an inherited generous response-bound proxy",
                          "The shell is a mathematical counterexample, not an equilibrium or a physical rescue"]
    return out
