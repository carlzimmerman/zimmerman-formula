# AS3 amendments, all after first results. No label line moved.
A1. Part 1 RUN1 (`as3_part1_RUN1.log`, 13/17). Four failures. Three were my test's faults, fixed after seeing them:
- A3: oblique velocity needs T^xz in the source; I had left it out.
- B1: my perturbation of A_mu left the unit constraint, so a.V had a first variation; the constraint is part of the theory, so the perturbation is now normalised.
- C1: at the release and source points the 1D potential is long-range, so my first test line (closer to bare than static) was the wrong test. Replaced with the exact prediction: bare + frozen charge, 1e-6.
The fourth, K3b, stands as FAILED: see README.
A2. Part 2 RUN1, RUN2 (`as3_part2_RUN1.log`, `as3_part2_RUN2.log`) failed on my faults: a sign of one term in my copy of as2_indep's block (now checked against its committed determinant), M1's radiation term left out of E(a) (0.3702, then 0.3908), a(1 MeV) without the g* step (6.4e7, then 1.76e8 h/Mpc), a unit error in e-folds (km/s/pc to /Gyr, off by 1000; caught against H4's numbers), and a frozen-coefficient test of Gamma^2 that can't work when Gamma ~ H.
- R0a's frozen-root comparison, as framed in the criteria's wording "(a), (c) agree", became a coefficient-by-coefficient comparison of the Lagrangians plus a time-dependent check (R0i). Same tolerance, 1e-3.
- Q2e added: closed form against the extrapolated Fourier form. F3a added at nu = 1e4, where friction is small; the first try at nu = 1 failed because the leading terms cancel there.
A3. Added beyond the criteria: `as3_record_ladder.py` and a repair of the record's action in a copy, to explain K3b. Reported only.
