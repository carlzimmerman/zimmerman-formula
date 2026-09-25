#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D03 -- THE OTHER THREE READERS OF THE CORPUS MASS-TO-LIGHT RATIOS: g03d (EFE refit), g03e (equipartition refit), G119 (break factor).
=====================================================================================================================================
Companion to D02 (same sandbox and variants; these lanes read only the corpus and run in under a second).  g03d's "bare deep-regime
a0 = 0.692 a0_DE" is the "G03D register" that G208 quotes, and falsifier-matrix row 17 cites "G03D 0.692 -> 0.534" as the reason the
EFE-boosted leg is rejected "on direction".  Both lanes fit a0 on a FIXED GRID (read from their source below), so a value on the
edge of the grid is a bound, not a measurement; this script reports every edge hit.
Checks can fail.  MUTATE=1 builds the "corrected" variants from the unchanged corpus: the change checks must then FAIL (rc = 1).
Run from the repository root:  python3 real_research/reviews/deep_a0eff_audit_2026_09_25/D03_corpus_side_lanes.py
"""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sandbox as sb

MUTATE = os.environ.get("MUTATE", "0") == "1"
A0_DE = 9.3619e-11
CH = []
def P(*a): print(*a, flush=True)
def check(name, measured, ok, reading="", load_bearing=True):
    CH.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}" + (f"\n         reading:  {reading}" if reading else ""))
P(__doc__)

def grid(lane):
    """the fit grid as written in the lane: np.linspace(lo, hi, n)"""
    m = re.search(r"for a0 in np\.linspace\(([0-9.e+-]+),\s*([0-9.e+-]+),\s*(\d+)\)", open(os.path.join(sb.DS, lane)).read())
    lo, hi, n = float(m.group(1)), float(m.group(2)), int(m.group(3))
    return lo, hi, (hi - lo) / (n - 1)
GD, GE = grid("g03d_efe_refit.py"), grid("g03e_equipartition.py")
edge = lambda a, G: "FLOOR" if a <= G[0] + 0.5 * G[2] else ("CEILING" if a >= G[1] - 0.5 * G[2] else "interior")
P(f"  fit grids: g03d [{GD[0]:.2e}, {GD[1]:.2e}] step {GD[2]:.1e};  g03e [{GE[0]:.2e}, {GE[1]:.2e}] step {GE[2]:.1e}")

VARIANTS = {"std05_cut": dict(ud=0.5, ub=0.7, qcut=0.10), "std06_cut": dict(ud=0.6, ub=0.7, qcut=0.10),
            "std07_cut": dict(ud=0.7, ub=0.7, qcut=0.10), "std05_nocut": dict(ud=0.5, ub=0.7, qcut=None)}
LANES = ("g03d_efe_refit.py", "g03e_equipartition.py", "G119_break_factor.py")
FILES = {"g03d": "g03d_efe_refit_results.json", "g03e": "g03e_equipartition_results.json", "G119": "G119_results.json"}
def run(cj, tag):
    S = sb.build(cj, tag="d03_" + tag)
    try:
        rc = {L: sb.run(S, L)["rc"] for L in LANES}
        return {k: sb.load(S, f) for k, f in FILES.items()}, rc
    finally:
        sb.destroy(S)
def row(R):
    d, e, g = R["g03d"], R["g03e"], R["G119"]
    return dict(d_bare=d["bare"]["a0"], d_bare_ratio=d["bare"]["ratio"], d_efe=d["EFE-boosted"]["a0"], d_efe_ratio=d["EFE-boosted"]["ratio"],
                d_bare_edge=edge(d["bare"]["a0"], GD), d_efe_edge=edge(d["EFE-boosted"]["a0"], GD),
                e_bare=e["refit"]["bare"]["a0"], e_bare_ratio=e["refit"]["bare"]["ratio"], e_bare_edge=edge(e["refit"]["bare"]["a0"], GE),
                g119_rms=g["sample"]["anchor_isolated_subset"]["pooled_rms_dex"], g119_pass=f"{g['n_pass']}/{g['n_total']}",
                g119_algebra=all(v.get("pass") for k, v in g["verdicts"].items()))

committed = {k: json.load(open(os.path.join(sb.DS, f))) for k, f in FILES.items()}
base, base_rc = run(sb.corpus_variant(), "base")
def flat(x, pre=""):
    out = {}
    if isinstance(x, dict):
        for k, v in x.items(): out.update(flat(v, pre + str(k) + "/"))
    elif isinstance(x, list):
        for i, v in enumerate(x): out.update(flat(v, pre + str(i) + "/"))
    elif isinstance(x, (int, float)) and not isinstance(x, bool): out[pre] = float(x)
    return out
worst = max(abs(a - flat(base[k]).get(key, a)) / max(abs(a), 1e-300) for k in FILES for key, a in flat(committed[k]).items())
check("B1 the sandbox reproduces the three committed result files with the committed corpus (every numeric field, rel. 1e-9)",
      f"worst relative difference {worst:.1e}; exits {base_rc}", worst < 1e-9 and not any(base_rc.values()))

rows = {"committed": row(committed)}
for tag, kw in VARIANTS.items():
    rows[tag] = row(run(sb.corpus_variant() if MUTATE else sb.corpus_variant(**kw), tag)[0])
P("\n  " + f"{'':12s}{'g03d bare a0':>16s}{'(ratio, grid)':>20s}{'g03d EFE a0':>14s}{'(ratio, grid)':>20s}{'g03e bare a0':>14s}{'(ratio, grid)':>20s}{'G119 rms':>10s}{'G119 checks':>12s}")
for t, r in rows.items():
    P(f"  {t:12s}{r['d_bare']:16.3e}{f'({r['d_bare_ratio']:.3f}, {r['d_bare_edge']})':>20s}{r['d_efe']:14.3e}{f'({r['d_efe_ratio']:.3f}, {r['d_efe_edge']})':>20s}"
      f"{r['e_bare']:14.3e}{f'({r['e_bare_ratio']:.3f}, {r['e_bare_edge']})':>20s}{r['g119_rms']:10.4f}{r['g119_pass']:>12s}")
T = list(VARIANTS)
check("C1 [g03d, the 'G03D register'] the bare deep-regime a0 is ABOVE a0_DE in every corrected variant (committed 0.692 a0_DE)",
      ", ".join(f"{rows[t]['d_bare_ratio']:.3f}" for t in T), all(rows[t]["d_bare_ratio"] > 1 for t in T),
      "G208's staircase note 'brief 0.69 = G03D bare ratio 0.692' quotes the corpus artefact")
check("C2 [g03e] the equipartition refit's bare a0 is ABOVE a0_DE in every corrected variant (committed 0.748 a0_DE)",
      ", ".join(f"{rows[t]['e_bare_ratio']:.3f} ({rows[t]['e_bare_edge']})" for t in T), all(rows[t]["e_bare_ratio"] > 1 for t in T),
      "the grid matters: " + "; ".join(f"{t} {rows[t]['e_bare_edge']}" for t in ["committed"] + T)
      + f" (g03e grid [{GE[0]:.2e}, {GE[1]:.2e}]) -- the committed 0.748 is a bound on the floor, not a measurement")
check("S1 [g03d -> falsifier row 17] the committed EFE-boosted a0 (0.534 a0_DE) is the FLOOR of g03d's fit grid, not a fit minimum",
      f"committed EFE-boosted a0 = {rows['committed']['d_efe']:.3e} = grid floor {GD[0]:.2e} ({rows['committed']['d_efe_edge']}); corrected: "
      + ", ".join(f"{rows[t]['d_efe']:.3e} ({rows[t]['d_efe_edge']})" for t in T),
      rows["committed"]["d_efe_edge"] == "FLOOR",
      "the 'EFE leg rejected on direction (G03D 0.692 -> 0.534)' reading compares a corpus artefact with a grid bound; neither is a measurement")
check("S2 [G119] the algebraic results (r_efe/r_M = sqrt(a0/g_ext), the 0.62 derivation) do not depend on the corpus; only the sample-rms consistency check does",
      f"verdict checks pass in every run: {[rows[t]['g119_algebra'] for t in ['committed'] + T]}; checks {[rows[t]['g119_pass'] for t in ['committed'] + T]}; sample rms {[round(rows[t]['g119_rms'], 4) for t in ['committed'] + T]}",
      all(rows[t]["g119_algebra"] for t in ["committed"] + T))
nfail = sum(1 for _, ok, lb in CH if lb and not ok)
P(f"\n  {sum(1 for _, ok, _l in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nfail}" + ("  (MUTATE: C1 and C2 must fail)" if MUTATE else ""))
json.dump({"mutate": MUTATE, "grids": {"g03d": GD, "g03e": GE}, "rows": rows, "checks": [{"name": n, "ok": ok} for n, ok, _ in CH]},
          open(os.path.join(HERE, "D03_results" + ("_MUTATE" if MUTATE else "") + ".json"), "w"), indent=1)
sys.exit(1 if nfail else 0)
