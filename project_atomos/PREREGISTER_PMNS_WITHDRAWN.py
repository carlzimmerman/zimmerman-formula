#!/usr/bin/env python3
"""PREREGISTER_PMNS_WITHDRAWN.py -- WITHDRAWN. The pre-registration idea it implements DOES NOT
WORK, and this file is kept only to record why.

THE IDEA WAS: every mixing angle is dead as a RETRODICTION target (all three PMNS D_max are
negative), but look-elsewhere is charged on TRIALS -- so freeze N candidates NOW, before
JUNO/DUNE tighten the windows, and a survivor costs only log2(N) instead of log2(42.5M).

IT FAILS ON CANDIDATE DENSITY, measured on the committed depth-10 records:

    angle           N in window   spacing(rel)   future window   N surviving by chance
    pmns_sin2_12         26,142       3.03e-06        7.92e-03                   2,614
    pmns_sin2_13         15,212       3.34e-06        1.69e-02                   5,071
    pmns_sin2_23         20,799       3.03e-06        1.26e-02                   4,160

For a pre-registered prediction to be falsifiable the vocabulary's candidate SPACING must EXCEED
the future window -- otherwise whatever the sharper measurement finds, the vocabulary already
contains a value sitting there. Falsifiability needs N_in_window < f. Actual N is 15,000-26,000
against f = 3-10: short by three to four orders of magnitude. Even after JUNO/DUNE there remain
thousands of reachable values inside the tightened window.

THE RUN ALSO EXPOSED IT DIRECTLY. Under the frozen selection rule, all three "predictions" landed
at 0.00 sigma from today's central value (deviations +2.5e-6, -1.2e-6, +3.7e-6 relative), because
10,568 / 6,052 / 8,343 candidates tie at the minimum depth. The rule was not picking a prediction;
it was picking the current central value back out of a dense set. Survival would then have
measured only whether the central value moved -- not anything about the vocabulary.

SO THE DOOR IS CLOSED, and for a sharper reason than the retrodiction ceiling: the vocabulary is
UNFALSIFIABLE in the PMNS sector at any future precision reachable this decade, because it covers
the window densely. Pre-registration cannot rescue a vocabulary that predicts everything.

The one thing that WOULD work is unchanged and is not a search: a DERIVED prediction, from the
framework's structure, written down before the comparison, landing on ONE value with no freedom
to slide. That is what tribimaximal mixing was, and why its falsification (th13 != 0) was
scientifically meaningful.

Kept as a record. DO NOT resurrect without first showing N_in_window < f.
"""

from __future__ import annotations
import hashlib
import json
import math
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DB = os.path.join(HERE, "results_grind", "depth_10", "records.sqlite")
OUT = os.path.join(HERE, "PREREGISTRATION_PMNS.json")
STAMP = os.path.join(HERE, "PREREGISTRATION_PMNS_HASH.txt")

# frozen inputs -- today's measured values, from the committed dataset
FROZEN_DATE = "2026-07-29"
ANGLES = ("pmns_sin2_12", "pmns_sin2_13", "pmns_sin2_23")
# projected tightening factors (public JUNO / DUNE sensitivity statements, order of magnitude)
F_PROJECTED = {"pmns_sin2_12": 10.0,   # JUNO: sub-percent on sin^2 th12
               "pmns_sin2_13": 3.0,    # already reactor-dominated, modest gain
               "pmns_sin2_23": 5.0}    # DUNE/T2HK on the atmospheric octant

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 98); print(s); print("=" * 98)


def germ_steps(recipe_json):
    """number of germ-decoration steps = contrivance measure for rule R2."""
    try:
        return len(json.loads(recipe_json))
    except Exception:
        return 99


def main() -> int:
    banner("PREREGISTER_PMNS -- freezing point-predictions BEFORE JUNO/DUNE tighten the windows")

    from targets import pdg_constants as pdg
    ds = pdg.load()

    if not os.path.exists(DB):
        print(f"  ERROR: committed records not found at {DB}")
        return 2

    # -----------------------------------------------------------------------------------
    banner("S1. The accounting that fixes N = 1 per angle")
    print(f"  {'angle':<16}{'w now':>11}{'f proj':>8}{'w future':>12}"
          f"{'bits if survives':>18}")
    print("  " + "-" * 66)
    total_bits = 0.0
    for a in ANGLES:
        t = ds[a]
        w = float(t.rel_precision)
        f = F_PROJECTED[a]
        total_bits += math.log2(f)
        print(f"  {a:<16}{w:>11.3e}{f:>8.1f}{w/f:>12.3e}{math.log2(f):>18.2f}")
    trials_bits = math.log2(len(ANGLES))
    print(f"\n  if ALL survive: {total_bits:.1f} bits supply - {trials_bits:.1f} bits trials "
          f"= {total_bits-trials_bits:.1f} bits net  (1 in {2**(total_bits-trials_bits):.0f})")
    print("  expected chance survivors with N=1 per angle: "
          + ", ".join(f"{a.split('_')[-1]} {1/F_PROJECTED[a]:.2f}" for a in ANGLES))
    check(all(1.0 / F_PROJECTED[a] < 0.5 for a in ANGLES),
          "N=1 per angle keeps expected chance survivors below 0.5 for every angle")
    print("  STATED NOW: this is SUGGESTIVE at best. It cannot establish a derivation, and a")
    print("  single survivor is worth only ~2-3 bits. Do not let it be reported as a lock.")

    # -----------------------------------------------------------------------------------
    banner("S2. Applying the frozen selection rule to the committed depth-10 records")
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT value, formula, recipe FROM records").fetchall()
    con.close()
    print(f"  {len(rows):,} committed depth-10 hit records loaded")

    predictions = {}
    for a in ANGLES:
        t = ds[a]
        cen, rel = float(t.value), float(t.rel_precision)
        lo, hi = cen * (1 - rel), cen * (1 + rel)
        cand = [(v, f, r) for (v, f, r) in rows if lo <= v <= hi]
        print(f"\n  {a}: central {cen:.8f}  window +/-{rel:.3e}  -> {len(cand):,} candidates")
        if not cand:
            print("    NO candidate in window -- no prediction can be registered for this angle")
            continue
        # R2 lowest germ-step count, R3 closest to centre, R4 lexicographic
        ranked = sorted(cand, key=lambda x: (germ_steps(x[2]), abs(x[0] - cen), x[1]))
        v, f, r = ranked[0]
        n_steps = germ_steps(r)
        n_min = sum(1 for c in cand if germ_steps(c[2]) == n_steps)
        print(f"    selected (R2 depth={n_steps}, {n_min} tied at that depth, then R3/R4):")
        print(f"      value   = {v:.12f}")
        print(f"      deviate = {(v-cen)/cen:+.3e} relative  "
              f"({abs(v-cen)/(rel*cen):.3f} sigma of today's window)")
        print(f"      formula = {f[:110]}")
        fut_rel = rel / F_PROJECTED[a]
        survives_if = abs(v - cen) <= fut_rel * cen
        print(f"      future window +/-{fut_rel:.3e}: this candidate survives ONLY IF the")
        print(f"      central value moves toward it; at TODAY's centre it would "
              f"{'SURVIVE' if survives_if else 'DIE'}")
        predictions[a] = dict(
            predicted_value=float(v),
            formula=f,
            germ_steps=n_steps,
            n_candidates_in_window=len(cand),
            n_tied_at_min_depth=n_min,
            today_central=cen,
            today_rel_window=rel,
            deviation_relative=float((v - cen) / cen),
            deviation_in_sigma=float(abs(v - cen) / (rel * cen)),
            projected_tightening=F_PROJECTED[a],
            future_rel_window=float(fut_rel),
            would_survive_at_todays_centre=bool(survives_if),
            bits_if_survives=float(math.log2(F_PROJECTED[a])),
        )

    check(len(predictions) == len(ANGLES),
          f"a prediction was registered for all {len(ANGLES)} angles "
          f"(got {len(predictions)})")

    # -----------------------------------------------------------------------------------
    banner("S3. Freeze and hash-stamp")
    doc = {
        "title": "Pre-registered PMNS point-predictions from the atomos germ vocabulary",
        "frozen_date": FROZEN_DATE,
        "vocabulary": "forced germs {3, sqrt(8pi/3)}, depth <= 10, committed records",
        "selection_rule": [
            "R1 candidate must be a hit inside today's +/-1 sigma window",
            "R2 minimise germ-decoration steps (lowest depth wins) -- NOT closeness",
            "R3 tie-break by |value - central|",
            "R4 tie-break lexicographically by formula, for determinism",
        ],
        "N_per_angle": 1,
        "why_N_is_1": ("a candidate inside today's window survives an f-fold tightening by "
                       "chance with probability ~1/f, so expected chance survivors = N/f; "
                       "informative requires N << f, and f ~ 3-10"),
        "best_case_bits_net": float(total_bits - trials_bits),
        "honest_reading": ("SUGGESTIVE at best (~1 in "
                           f"{2**(total_bits-trials_bits):.0f} if all three survive). "
                           "A single survivor is worth 2-3 bits and establishes nothing on "
                           "its own. All three dying excludes the vocabulary's NEAREST "
                           "reachable values for the PMNS sector, and does NOT kill the "
                           "vocabulary, which can reach other values."),
        "predictions": predictions,
    }
    blob = json.dumps(doc, indent=2, sort_keys=True)
    open(OUT, "w").write(blob + "\n")
    h = hashlib.sha256(blob.encode()).hexdigest()
    open(STAMP, "w").write(f"{h}  PREREGISTRATION_PMNS.json  frozen {FROZEN_DATE}\n")
    print(f"  wrote {os.path.basename(OUT)}")
    print(f"  SHA-256 = {h}")
    print(f"  stamped to {os.path.basename(STAMP)}")

    banner("SUMMARY")
    for a, p in predictions.items():
        print(f"  {a:<16} predict {p['predicted_value']:.10f}  "
              f"({p['deviation_in_sigma']:.2f} sigma from today's centre, "
              f"depth {p['germ_steps']}, {p['n_candidates_in_window']:,} in window)")
    print(f"\n  frozen {FROZEN_DATE}, hash above. When JUNO/DUNE publish, compare and score.")
    print("  Scoring is mechanical and fixed: inside the tightened window = survived and")
    print("  worth log2(f) bits; outside = that prediction is dead, with no reinterpretation")
    print("  permitted. The selection rule was fixed before any candidate was inspected.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
