# CFG460: zero-knob growth fix at 512³, second realisation (seed 360). CONFIRMED

The criteria were committed first. The launcher is `run_460.py`, and the verdict comes from `cfg460_analysis.py`.

**Result.**
- σ₈ ratio 1.0037, max|P−1| 0.040 against the same-seed control (ΛCDM-equivalent growth): GROWTH OK.
- Overdraw is 0. The largest catchment draw is 0.53, against 0.49 for seed 359.

With CFG425/439, the rule now passes at 512³ in two realisations (0.033, 0.040), on both footings and with DE-tracking a₀. This removes PAPER45 v2.1's "one realisation at 512³" caveat.

**Caveats (unchanged).**
- The cold-fluid supply per galaxy is a postulate (CFG461/462/488/490).
- The settling is bookkeeping.
- Convergence beyond 512³ is not tested.
