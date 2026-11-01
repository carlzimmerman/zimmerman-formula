# Kinetic coefficient-control discretization correction

The first canonical screen computed all six cases and all case checks passed,
but its independent stretch-factor control failed the original 3e-7 accuracy
gate for A=2,D=-1. The stored centered differences were 8.0000500005,
8.0000124996 and 8.0000031204 at the three frozen halving steps, versus exact
8. Their deviations have the expected second-order truncation scaling.

kinetic_screen_v2.py uses Richardson cancellation (4D(h/2)-D(h))/3 from the
already prescribed two finest differences. The gate is unchanged; all raw
differences remain recorded. No physical coefficient, energy matrix, basis,
halo, forcing, or case-selection rule changes. The initial script and failed
manifest remain. The regression control was observed failing on v1 and
passing with this accuracy correction. New evidence is kinetic_run_002.
