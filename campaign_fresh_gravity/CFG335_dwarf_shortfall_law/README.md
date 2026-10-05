# CFG335: empirical law for the dwarfs extra-mass need

**Verdict (frozen 4167d42db): NO SIMPLE LAW.** The scatter is 0.6-0.7 dex, against the frozen 0.25 dex line.

The sample is 92 resolved dwarfs: MW 45, M31 34, field 13. Under the law, 69 have a shortfall and 23 are already sufficient.

**Reported, not graded: a consistent slope.** The shortfall grows as Delta M proportional to M_b^(0.52 +- 0.06) (canonical; alt 0.50 +- 0.07). The slope is the same for MW (0.51) and M31 (0.53).

A slope of 0.5 is the deep-MOND phantom scaling itself, since M_dyn is proportional to r sqrt(a0 M_b / G). So on average the dwarfs look like the law with a larger multiplicative boost, the familiar dwarfs-prefer-a-higher-effective-a0 signature. The 0.6 dex scatter means no single equation describes them. This is descriptive: no mechanism is claimed, and kappa = 1/2 is fixed.

Controls: C1 and C2 pass to 1e-14. MUTATE (shuffled sigma) raises the scatter from 0.62 to 0.96 dex, as required.

Run: `python3 campaign_fresh_gravity/CFG335_dwarf_shortfall_law/cfg335_shortfall.py` (and `CFG335_MUTATE=1` for the control), a few seconds each.
