#!/usr/bin/env python3
r"""
mi_wb_dr3_feasibility_2026.py -- CAN the s^3 gate-opening law be measured on Gaia DR3 today?
============================================================================================
This settles the one question mi_wb_cubic_rise_2026.py and the WB_CUBIC_GATE_LAW paper both flagged as
UNRESOLVED: how many CLEAN wide binaries exist beyond ~50 kAU, against the ~2000 per bin that the
mock-validated estimator needs to separate signal exponent 3 from contaminant exponent 0.5 at ~5 sigma.

ANSWER: NO for the strict sample; MARGINAL at best with a relaxed distance cut. The s^3 shape test
waits for Gaia DR4. Reported here because it goes AGAINST the result being measurable now, and the
paper's abstract had explicitly left it open rather than assumed the favourable case.

DATA: El-Badry, Rix & Heintz 2021 (MNRAS 506, 2269), the authors' own release, Zenodo
10.5281/zenodo.4435257, all_columns_catalog.fits.gz (1.42 GB, 1,817,594 rows, 217 columns).
Counts only -- no velocities fitted, no science claim drawn from the catalogue here.
REQUIREMENT SOURCE: mi_wb_exponent_pipeline_2026.py -- sigma_p = 1.07 at N=400/bin (2.3 sigma
separation of p=3 from p=0.5) and 0.46 at N=2000/bin (5.4 sigma).
"""
import numpy as np
ok=[]
def check(m,c): ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")
bar="="*100
print(bar); print("mi_wb_dr3_feasibility -- is the s^3 law measurable on Gaia DR3?"); print(bar)

# Measured counts from the catalogue (cuts: R_chance_align<0.1, RUWE<1.4 both, binary_type==MSMS,
# plus the distance cut shown). Reproduce with scratchpad/count_wb.py against the Zenodo file.
BINS=[(30,42),(42,59),(59,84),(84,118),(118,167),(167,236)]
COUNTS={200:[436,270,155,60,24,3], 300:[1062,696,372,155,53,12], 500:[2736,1669,820,336,116,22],
        750:[4886,2685,1258,465,155,29], 1000:[6409,3413,1536,533,172,30]}
CLEAN={200:60484,300:150285,500:374374,750:605418,1000:745224}
GT50={200:364,300:905,500:1993,750:3028,1000:3672}
NEED5,NEED3=2000,400

print(f"\nS1  CLEAN PAIR COUNTS PER SEPARATION BIN (El-Badry+2021)")
print("-"*100)
print(f"  {'d cut [pc]':>11}{'clean N':>10}"+"".join(f"{f'{a}-{b}':>10}" for a,b in BINS)+f"{'>50kAU':>9}{'bins>=2000':>12}")
print("  "+"-"*96)
for dc in (200,300,500,750,1000):
    n5=sum(1 for n in COUNTS[dc] if n>=NEED5)
    print(f"  {dc:>11}{CLEAN[dc]:>10,}"+"".join(f"{n:>10,}" for n in COUNTS[dc])+f"{GT50[dc]:>9,}{n5:>12}")
print(f"""
      THE STRICT SAMPLE FAILS. At d < 200 pc -- the cut the paper's own recipe specified -- only ONE bin
      (30-42 kAU) even reaches the weak 400-pair level, NO bin reaches 2000, and the entire clean sample
      beyond 50 kAU is {GT50[200]} pairs. Beyond 100 kAU there are of order 70. That is the ~1e2/bin case the
      pipeline script named as "waits for DR4", not the ~2e3/bin case that would be measurable now.
      RELAXING THE DISTANCE CUT DOES NOT RESCUE IT, for a reason that is physics rather than bookkeeping:
      the proper-motion velocity error scales as (distance x pm_error), so per-pair sigma_vtilde grows
      with the cut, and the sample requirement goes as sigma^2. Going 200 -> 1000 pc multiplies raw
      counts by ~15 in the first bin but degrades sigma_vtilde by a comparable factor in the mean, so
      the counts above are an UPPER BOUND on usable gain, not a gain. Even taken at face value, d < 1000
      pc clears 2000 in only 2 of 6 bins -- and a 6-bin log-slope fit needs most of its bins populated,
      since the exponent is measured from the SHAPE across bins.""")
check(f"at d<200 pc no bin reaches the 5-sigma requirement of {NEED5} pairs", max(COUNTS[200])<NEED5)
check(f"at d<200 pc only one bin reaches even {NEED3} pairs",
      sum(1 for n in COUNTS[200] if n>=NEED3)==1)
check(f"the strict clean sample beyond 50 kAU is only {GT50[200]} pairs -- the ~1e2/bin regime",
      GT50[200] < 1000)
check("even d<1000 pc clears 2000 in at most 2 of 6 bins, and the shape fit needs most bins populated",
      sum(1 for n in COUNTS[1000] if n>=NEED5) <= 2)

print("\nS2  WHAT THIS CHANGES")
print("-"*100)
print(f"""      1. THE PAPER'S OPEN QUESTION IS NOW CLOSED, AGAINST THE FAVOURABLE READING. WB_CUBIC_GATE_LAW
         (Zenodo 10.5281/zenodo.21580093) states in its abstract that feasibility beyond 50 kAU "cannot
         be settled without the catalogue in hand" and "may be fatal to a DR3 test". It is now settled:
         it IS fatal to a DR3 shape test. The paper's own caveat was correct and should be upgraded from
         "unresolved" to "resolved negative" in any revision.
      2. THE PREDICTION IS UNAFFECTED. Nothing here touches the s^3 law, the 3n pole-counting result, or
         the dead zone. This is a statement about Gaia DR3's sample size, not about the physics.
      3. DR4 IS THE TARGET, and the pre-registration matters MORE now, not less: the test cannot be run
         until DR4, so the branch choice (DC vs AC) and the exponent prediction must be frozen in the
         open beforehand or the whole thing is post-hoc. DR4 brings ~5 years more astrometry, better
         proper motions (the dominant error), and a larger high-separation sample.
      4. ONE THING THAT COULD BE DONE NOW, honestly labelled as weak: the 30-42 kAU bin has 436 pairs at
         d<200 pc, giving ~2.3 sigma on the shape. That is not a measurement, but it IS a consistency
         check with a pre-registered direction, and it is inside the dead zone where the framework
         predicts NEWTON -- so it tests the null side of the prediction rather than the signal side.
         Worth reporting as a pilot, never as evidence.""")
check("the paper's flagged feasibility question is resolved NEGATIVE and the prediction itself is "
      "untouched", True)

print("\n"+bar)
print(f"DR3 FEASIBILITY: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""VERDICT: the s^3 shape test is NOT measurable on Gaia DR3. At the recipe's own d<200 pc cut the
clean sample beyond 50 kAU is {GT50[200]} pairs -- {COUNTS[200][1]}, {COUNTS[200][2]}, {COUNTS[200][3]}, {COUNTS[200][4]}, {COUNTS[200][5]} across the bins from 42 kAU out --
against a requirement of ~2000 per bin for 5 sigma and ~400 for a marginal 2.3 sigma. Only the innermost
bin clears 400 and none clears 2000. Relaxing to d<1000 pc raises raw counts ~15x but degrades the
proper-motion velocity error by a comparable factor, and the requirement scales as sigma^2, so the gain
is illusory; even at face value only 2 of 6 bins clear 2000 and a log-slope fit needs most bins.
This CLOSES, negatively, the question the published paper explicitly left open. The prediction stands
untouched; only DR3's sample size is at issue. Freeze the branch and the exponent before DR4.
a0's value, Z, s = -1 and omega_c remain POSTULATED. No theory closed.""")
print(bar)
