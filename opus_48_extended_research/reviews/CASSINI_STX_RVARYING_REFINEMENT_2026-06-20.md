# Cassini s^TX — the r-varying refinement: the ~1.5× margin STANDS, front stays LIVE (no flip possible)

*Workflow `witcowdji` (3 agents), banked 2026-06-20. Addendum to FRONT_CASSINI_STX_2026-06-20.md.
The one open computational door on the framework's tightest test — now closed. Framework footing:
a0=9.36e-11 (INPUT). Quarantine intact (this pins the kernel-weighting O(1) only; derives nothing
about a0/Z/κ).*

## The question
The Hees-2016 bound on s̄^TX assumes a **CONSTANT** preferred-frame background; the framework's induced
s̄ = (a0/2|a|)(uu)_traceless **VARIES as ~r²** around each orbit (since |a|=GM/r²). Does the proper
orbit-integral make the ~1.5× margin TIGHTER (toward excluded) or LOOSER (toward safe)?

## The answer: TIGHTER, but only sub-percent at the binding corner — the margin STANDS

The secular orbital-element drift (Bailey-Kostelecký 2006 gr-qc/0603030 Eq.165–171; Hees+2015
arXiv:1508.03478 = PRD 92 064049 Eq.7) averages the perturbation over the true anomaly. The dt→df
Kepler areal law supplies a net **+r² time-weighting** biased toward aphelion. The framework's
s̄(r)~r² then enters as ⟨(r/a)²⟩_t — a small **POSITIVE** inflation (so "evaluate-at-a" slightly
*under*-estimates |s|, margin tightens slightly):

| body | ⟨(r/a)²⟩ inflation | corrected margin |
|---|---|---|
| **Saturn (binding corner)** | **+0.5%** | **1.49× (eta~1.004)** |
| Mars | +1.3% | 58.9× |
| Mercury (highest e) | +6.3% | 912× |
| Venus / Earth | ~0% | ~261× / ~137× |

**Convention-free bracket (zero kernel-modeling assumption), Saturn:** margin ∈ **[1.344×, 1.679×]**
across the full s̄·(1±e)² range. **Even the absolute aphelion-extremal corner gives 1.344× > 1 → LIVE
survives EVERY treatment. NO FLIP to excluded is possible.** The O(1) kernel-power uncertainty (p=1..3)
spans at most +0.2%..+12.8% — nowhere near the ~1.5× that would flip the verdict.

## Verdict
**The ~1.5× worst-corner margin is ROBUST; Front A stays LIVE / FALSIFIABLE.** The r-varying treatment
tightens it by <1% at the binding Saturn corner — confirmed, not on the edge. The decisive test stays a
~10× ephemeris improvement to ~1.3e-10 (~2028–32).

> *Adversarial note (caught by the workflow):* my workflow prompt cited "arXiv:1509.06868 / Eq.19" —
> the WRONG paper (a Gaia/SF2A conference note with no secular formulas). The agent corrected it to the
> right primaries (Hees+2015 arXiv:1508.03478 = PRD 92 064049; Bailey-Kostelecký 2006 gr-qc/0603030)
> and extracted the actual equations by PDF. The numbers above use the correct formalism.

### Scripts (exit 0, under opus_48_extended_research/reviews/front_cassini/)
hees_secular_kernel_rpower.py · hees_rvarying_secular_integral.py · hees_rvarying_adversarial.py
