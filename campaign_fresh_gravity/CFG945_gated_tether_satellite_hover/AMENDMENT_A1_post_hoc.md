# CFG945 amendment A1 (POST HOC, 2026-10-21, after the first MUTATE run, before any main-stage number)

**What happened.** The first MUTATE run (kept as `cfg945_MUTATE_firstrun_M5toothless.out` / `.json`) exited 2: tooth M5, as frozen,
did not bite. M1–M4 and M6 bit. No main-stage number existed at that point; the K stage had passed.

**Why M5 is toothless as frozen.** At ε = 100 every dwarf is stripped, the 11 isolated dwarfs included. A stripped dwarf's residual
rises by log₁₀ ν_e(g_bar/a₀), which depends on g_bar alone. CFG874's statistic is a matched-g_bar regression (intercept, slope in
log g_bar, isolated offset c), so a shift that is a smooth function of g_bar and common to both groups is absorbed by the intercept
and slope. c moves from −0.1003 to −0.101. The tooth was mis-designed by me.

**What it reveals (a property of the bound, stated plainly).** c sees only **satellite-specific** (environment-dependent) stripping.
Stripping that falls equally on satellites and isolated dwarfs at matched g_bar is invisible to c (it would need CFG874's E, which
these criteria do not use). The hover's differential is ε g_host with g_host ≈ 4–20 × larger for satellites than for isolated
dwarfs at ≥ 300 kpc, so at hover-size ε it strips satellites first. ε_B as frozen therefore bounds the satellite-specific part of
the differential, which is the part CFG925 R3 and CFG873–875 speak to. ε_B is not changed by this amendment.

**Changes (labelled post hoc).**
1. **M5b (added tooth):** strip every matched satellite and no isolated dwarf (injection). c must fall below −2 se_c. M5 as frozen
   stays in the output, reported as TOOTHLESS (flagged).
2. **Exit code 3** (new): a frozen tooth is toothless (flagged) while its labelled replacement and every other tooth bite. Exit 1
   and 2 keep their frozen meaning.

Nothing else in FROZEN_CRITERIA.md changes. κ = ½ FITTED; footings never pooled; not theory closed.
