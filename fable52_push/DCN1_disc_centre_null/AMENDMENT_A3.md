# DCN1 AMENDMENT A3 (post hoc; committed alone, after the corrected KA4 / KA5 and before any P1 / P2 local number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Criteria d603f1703c; A1 0a6e46fb52; A2 15f6f993e4.

## What was seen first (the corrected solver, A2)

- **KA5 passes as frozen.** Q converges to 1.7887e-30 s^-2 against an exact 1.7904e-30 (0.1 %; the line is 5 %).
- **KA4 fails as frozen, and under A1.**
  - Q, on the cell next to the null:
    - P1 geometry: -4.157, -4.152, -4.148, -4.145, -4.142 (1e-29);
    - P2 geometry: -4.212, -4.197, -4.184, -4.174, -4.165;
    - exact -5.331. Ratio 0.78, against the frozen 2 %.
  - The sequence creeps at observed order 0.33. That is below the rule's 0.5, so it is not Converged, and A1's reading
    fails too.
  - The cause is the null cell's own operator error, which is the same at every resolution. A1's exact-Phi diagnostic
    puts it at 0.45 x 4 pi G rho for s < 2h.
- **Away from the null the operator is right.** The maximum over cells with s >= 8h (Q_8) is:
  - P1: -5.446 down to -5.375;
  - P2: -5.715 down to -5.489.

  That is within 1-3 % of exact at the finest grid. The fitted scalings are |D.P| ~ s^-0.51 and u ~ s^0.51, Part A2's
  deep-law exponents. But Q_8's excluded ball shrinks with h, and the exact rate moves as s^(1/2) there, so Q_8 also creeps
  (order 0.35).
- **Nothing has been seen** of P1 or P2's local solves.
- **The global P2G maps** (reported only) show negative D.P on the cells next to r_min:
  - the razor-thin discs, both treatments;
  - the thick discs, variant C, at R2-R3.

  This is where SCS3 A1 found its inner-boundary artefact.

## The amendment

1. **Graded rate: Q_A** = the maximum of Gamma_loc^2 over the fixed annulus L/8 <= s <= L/2. The annulus is the same
   physical region at every resolution. Q_A goes through the frozen rule unchanged. KA4 and KA5 are regraded on Q_A with
   the frozen tolerances (2 %, 5 %) against the exact sup over the same annulus.
2. **Graded null behaviour: shell maxima.** M_k = max Gamma_loc^2 over the shells s in [L/2^(k+1), L/2^k), k = 1, 2, ...,
   keeping only shells whose inner radius is at least 8h. These are taken on the finest two resolutions.
   - **unbounded(b)** iff, on both of those grids:
     - the innermost three shell maxima are positive, rise inward, and
     - their log-slope d ln M / d ln s is <= -0.25 (the rate growing at least as s^(-1/4)).
   - Otherwise the null is bounded.
   - KA4 must give not-unbounded.
   - **The new M2:** add -|min D.P(N_R 48)| (s/L)^(-1) to D.P everywhere in the region. This plants Gamma^2 ~ s^(-1/2).
     It must give unbounded on every background.
3. **Labels per background:**
   - **unbounded(b)** by item 2.
   - **bounded-unstable(b)** if not unbounded, and either:
     - Q_A converges with Q_A,inf - E > 0, or
     - the finest grid's innermost shell maximum M_in > 0 and the next-finest grid's agrees with it in sign and to within 20 %.

     The rate reported is the larger of Q_A,inf and M_in.
   - **stable(b)** if not unbounded, Q_A converges with Q_A,inf + E < 0, and every shell maximum is negative on the finest
     two grids.
   - **open(b)** otherwise.

   Problem and lane labels follow the criteria's section 3 unchanged.
4. **M1** is applied to Q_A and the shells (it must change every stable or bounded label). M3 and M4 are unchanged.
5. **Reported, not graded:** the P2G global maps rerun with r_min = 1e-6 R_d (R1-R3). If the cells next to r_min stay
   negative when r_min moves, those negative cells are an inner-boundary artefact.
6. **The readings come in order:** frozen first (NO VERDICT: KA4 fails), then A1 (NO VERDICT: KA4's Q not Converged),
   then A3.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
