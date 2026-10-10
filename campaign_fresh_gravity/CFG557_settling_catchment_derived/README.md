# CFG557: which cold energy can have settled by today? Catchment NOT DERIVABLE exactly (needs α); the α-free free-fall ceiling is derived and tested. It halves the growth excess but still FAILS growth, worsens KiDS, keeps groups / MW / LG timing passing

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (5149a12f1). Date: 2026-10-10.
- **Scripts** (all run with `nice -n 10`, ≤ 4 threads; no PM runs, no downloads):
  - `cfg557_lib.py`: the derivation library (spherical collapse in ΛCDM, EPS main-progenitor δ_L(M), self-consistent edge, capture time).
  - `cfg557_derive.py` (about 10 s): task 1. Writes `cfg557_derive.out` and `cfg557_derive_results.json`; `CFG557_MUTATE=1` writes the `_MUTATE` files (MU3).
  - `cfg557_tests.py` (about 25 s): halo model, groups, MW, LG. Writes `cfg557_tests.out` and `cfg557_tests_results.json`; `CFG557_MUTATE=1` writes the `_MUTATE` files (MU1, MU2).
  - `cfg557_kids.py` (about 5 min, 4 worker processes): KiDS. Writes `cfg557_kids.out` and `cfg557_kids_results.json`; `CFG557_MUTATE=1` writes the `_MUTATE` files (MU1/KK1). Tables are cached outside git in `_external_data/cfg557_work/`.
  - Every MUTATE run exits 1, meaning all its teeth bite.
- **Read-only reuse:** CFG556's halo model (exec'd up to its run block), CFG543's group code (imported), CFG529's table and score code (imported or exec'd, as CFG531 does), CFG522's timing code (exec'd; it pulls in CFG515/CFG513's `Prof`), and CFG548's JSON.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled. Flat a0, kernel ν_mono, candidate B, G9, no EFE. The cold energy's MASS is still required; no particle species. This is not "theory closed", and nothing here says the data favour the framework.
- **Numbers:** all come from the three `*_results.json` files. Pairs are canonical / alt.

## 1. Derivation (task 1)

**D1. Candidate B's switch selects the turnaround ball.**
- For a spherical profile the tidal eigenvalues are δ̄(<r)/3 (twice) and δ(r) − 2δ̄/3. So λ₂ = δ̄/3 at every radius, and B = {1 + δ̄ ≥ Δ_ta} is exactly the turnaround ball.
- Numerically, on the CFG556 extended NFW at log M = 11–15: |r_B/r_ta − 1| ≤ 2.6e-14.
- So the mobility region B ∩ C is candidate (a). "The switch acts inside bound systems" does not pick the virial or splashback ball (b). In candidate B, "bound" already means "past turnaround".

**D2. The stationary state is (a).** CFG541 V4: the minimiser is the inside-out fill using the whole B ∩ C supply, and it does not depend on α. The z = 0 state reaches it only where the shells have had time.

**D3. The dynamical catchment.**
- A shell enters B ∩ C when it turns around. Its cold energy counts as settled at t_obs only if t_reach(r_e) + t_cap ≤ t_obs:
  - t_reach is the free-fall-limited time for the shell's spherical-collapse trajectory (ΛCDM, Λ term) to reach the edge.
  - t_cap = r_e/(αV_f), the CFG541 relaxation time at the edge.
- δ_L(M) comes from the EPS main-progenitor ODE (Neistein+06 form, q = 2.2, recalled, PROVISIONAL).
- The edge uses the derived supply itself, so s_c is solved as a fixed point.
- Controls pass:
  - Δ_ta(0) = 11.806 against 11.816 (rel 8.8e-4).
  - δ_c(0) = 1.6767.
  - t0 = 13.820 Gyr against 13.796 (1.7e-3; no radiation term).
  - Every fixed point converged.

**s_c = M_c/M_ta at z = 0.** Each cell gives s_c / r_c/r_ta / r_c/r200m. The canonical footing is shown; alt agrees to ≤ 0.01 in s_c.

| log M_ta | free-fall ceiling (α→∞) | α = 2 | α = 1 | α = 0.5 | collapsed shell (δ_c) | More+15 M_sp/M_ta (context) |
|---|---|---|---|---|---|---|
| 11 | 0.798 / 0.554 / 1.66 | 0.783 | 0.767 | 0.736 | 0.783 | 0.740 |
| 12 | 0.770 / 0.526 / 1.59 | 0.740 | 0.710 | 0.651 | 0.740 | 0.705 |
| 13 | 0.702 / 0.450 / 1.38 | 0.677 | 0.653 | 0.607 | 0.677 | 0.664 |
| 14 | 0.616 / 0.369 / 1.15 | 0.589 | 0.563 | 0.516 | 0.588 | 0.617 |
| 15 | 0.500 / 0.281 / 0.89 | 0.462 | 0.428 | 0.372 | 0.459 | 0.562 |

**Derivation verdict (frozen rule).**
- **(a) is kinematically excluded at z = 0.** The free-fall ceiling is at most 0.798 everywhere. Shells that turned around within roughly the last collapse time cannot yet have delivered their cold energy to the edge.
- **NOT DERIVABLE exactly.** A = min s_c(0.5)/s_c(2) = 0.806 (canonical, log M_ta 15), below 0.90. At α ≤ 2 the settled supply is rate-limited, which agrees with CFG539's "the coefficient acts as a knob".
  - **What is missing:** the mobility prefactor α, or a derived velocity-space settling law that fixes the capture time.
- **The single tested choice is the α-free free-fall ceiling s_c,∞**, the DERIVED UPPER BOUND on the settled supply.
  - It sits within 0.01–0.06 of the collapsed (δ_c) shell and within about 10% of the More+15 splashback mass (r_c ≈ 0.28–0.55 r_ta, about 0.9–1.7 r200m).
  - So the derivation lands near candidate (b) in amount, but it gets there through dynamics (finite age), not through B's definition.
  - Finite α only lowers s_c.

## 2. Tests with the tested catchment s_c,∞ only

| test | rule | canonical | alt |
|---|---|---|---|
| (i) growth, CFG556 halo model | max\|R−1\| ≤ 0.10 (k 0.05–1) and σ8 within 5% | **FAIL**: E +0.382 at k 0.99, σ8 ratio 1.0170 | **FAIL**: E +0.458, σ8 1.0203 |
| (ii) groups, CFG543 P2 (Tian+26 M_bar incl. X-ray gas) | \|Z\| < 2 | **PASS** (marginal): +0.073, Z +1.97 | **PASS**: +0.059, Z +1.58 |
| (iii) KiDS f30, CFG529 | p > 0.01 in A and B | **FAIL**: χ² 59.13 (p 3.6e-7) / 66.04 (p 2.2e-8) | **FAIL**: 50.44 (p 1.0e-5) / 55.50 (p 1.5e-6) |
| (iv) MW inside 30 kpc | r_e > 30 kpc | **PASS (unchanged)**: edge 512 → 389 kpc | **PASS**: 466 → 351 kpc |
| (v) LG timing, CFG522 M1 | \|z_full\| < 2 | **PASS**: z_full −0.42 | **PASS**: z_full −0.41 |

**(i) Growth.**
- R(k) is 1.046 / 1.054 at k = 0.3, 1.148 / 1.174 at k = 0.5 and 1.385 / 1.462 at k = 1. CFG556 had 1.716 / 1.885 at k = 1. **The excess is halved but not removed.**
- Ratio form: +0.295 / +0.354.
- Drivers at k = 1: log M_ta 14–15 gives +0.270 / +0.310.
- The cause: a smaller supply pulls the edge inward, to r_e/r_ta = 0.19–0.27. The reduced settled mass is then packed even tighter. At log M_ta 13–15, M_F/M_L at 0.2 r_ta is 1.33–1.55 (canonical) and 1.46–1.58 (alt); at log M_ta 12 it is 1.08 / 1.18. The law's isothermal phantom with a supply edge is more concentrated than NFW on group and cluster scales at any supply that is O(1) of the collapsed mass.
- Context, not verdicts:
  - α = 1 gives E +0.339 / +0.413, and α = 0.5 gives +0.307 / +0.378. Both still fail.
  - Supply = M200m in ta scope gives +0.380 / +0.467.
  - CFG556's r200m-ball scope gave −0.081 / −0.047, so the halo-model scope bracket still decides the sign there (see the disclosures).

**(ii) Groups.**
- s_c* median 0.738 / 0.721.
- The reduced supply moves P2 from +0.060 / +0.043 (CFG543) to +0.073 / +0.059. It still closes, but canonical is right at the line (Z 1.97).
- Reported:
  - With s_c at a galaxy-scale progenitor: +0.071 / +0.056.
  - With R_e = Re/1.563: +0.052 / +0.036.
  - With the addendum's aperture (σ inside R < Re): +0.032 ± 0.021 / +0.013 ± 0.020 (k = 1), and +0.022 / +0.003 (k(c20)).
- So the smaller supply does not break the CFG543 closure. It does remove most of the canonical margin.

**(iii) KiDS.**
- The derived edge moves inward: median x = r_e/r_ta goes from 0.279 to 0.196 (canonical) and from 0.242 to 0.169 (alt).
- KiDS prefers x ≈ 0.45–0.50, so χ² rises by 12–15 over the census edge, which already failed. Δ vs the best node is +18.5 / +15.0 (canonical, A / B) and +22.0 / +18.1 (alt).
- The damage is in the outer six bins: χ²_outer6 is 33.6 against 22.9 for the census edge.
- **Inner bins:**
  - χ²_inner9 is 20.0 / 20.3 (census 20.3 / 20.5) on canonical and 14.2 / 14.4 (census 13.1 / 13.2) on alt.
  - Only 0.19% / 0.47% of f30 lenses have an edge inside 98 kpc. The frozen wording therefore labels K-in "affected", but the inner-band χ² barely moves.
  - The CFG531 inner shortfall (ε K-in +0.342 / +0.231) and the early-type excess are not helped. A smaller catchment can only remove mass outside the edge, and these tests need more mass inside it.
  - Early-type edges: minimum 98 / 89 kpc.

**(iv) MW.**
- With CFG513's Prof (M_b 6e10, census f_ret 0.10), s_c* is 0.758 / 0.752.
- The edge moves from 512 to 389 kpc (canonical) and from 466 to 351 kpc (alt). That is far beyond 30 kpc, so the CFG532 rotation curves and CFG553 K_z are unchanged by construction.

**(v) LG.**
- s_c* is MW 0.753 / 0.749 and M31 0.741 / 0.737. The edges move from 302/427 to 229/318 kpc (canonical).
- The unsettled cold energy (4.7e11 + 9.8e11 Msun) is kept as drained-shell mass out to r_ta (1047 / 1319 kpc).
- The mass inside 780 kpc drops from 5.845e12 to 5.37e12 / 5.39e12.
- Timing results:
  - z_full is −0.42 / −0.41: PASS.
  - The strict radial z_meas improves from +4.37 to +3.07 / +3.14, but it is still above 3.
  - With the shell omitted (a lower bound): z_meas −2.26 / −2.35, z_full −1.35.
- **Zero-velocity radius:**
  - The mass inside R0 is 5.83e12, almost all of F-M1's 5.845e12, because R3 conserves the mass inside the turnaround and R0 ≈ r_ta.
  - So R0_pred = 1439 kpc and Z = +2.77 (F-M1 +2.78), a ΔZ of −0.01. The catchment does not move the LG toward the flow mass (1.12e12).
  - This is NOT DIAGNOSTIC per the CFG548 line, and ΛCDM's timing mass sits at the same place.

## 3. Overall

**No single derived catchment satisfies growth AND groups AND KiDS AND MW AND LG.**
- With the derived ceiling, groups, MW and LG timing still pass on both footings. Groups pass only marginally on canonical.
- Growth improves (the k = 1 excess is halved, σ8 +1.7% / +2.0% now within 5%), but it still FAILS the 10% bar.
- KiDS gets WORSE. Its outer bins want a larger edge (more supply), which is the opposite direction from growth.
- The LG zero-velocity mass cannot move: mass inside the turnaround is conserved.
- **Plain reading.** The catchment amount is not the whole lever. The growth excess comes from the *concentration* of the law's phantom inside a supply edge. Shrinking the supply shrinks the edge and keeps the halo compact. KiDS wants the opposite.
  - Growth and KiDS pull the supply in opposite directions, and α does not fix that (it only lowers s_c further).
  - What is missing is either a derived α (rate) or a change in where settled cold energy sits relative to the law's profile (for example the kinetic softening of CFG544/554), not the catchment.

## 4. MUTATE (all teeth bite)

- **MU1 (catchment = turnaround, s_c ≡ 1):**
  - The halo model reproduces CFG556's primary R(k) and σ8 exactly (max |ΔR| 0, |Δσ8| 0).
  - Groups give +0.05961 / +0.04349, equal to CFG543's P2.
  - The LG pair gives z_full −0.1059 / −0.1020, equal to CFG522's M1.
  - KiDS tables for 20 random groups match CFG529's census tables to 0 relative difference. KK0: the census χ² is reproduced exactly.
- **MU2 (catchment = 0):**
  - In the halo model R ≡ 1 (max |R − 1| = 0).
  - Groups give the Newtonian baryons-only +0.8098 = CFG543's M3 P2.
- **MU3 (infinite age):** s_c = 1.000000 at every mass and α. The reduction comes only from the finite age, and the stationary state is (a).

## 5. Disclosures (dated 2026-10-10)

- **MU2 in the halo model.**
  - The E-cen device truncates the retained baryons at r_e, so at r_e → 0 it is degenerate. s_c = 0 was implemented as the declared L-ta profile, as frozen, which makes that tooth a code-path check.
  - Information only: s_c = 1e-6 through the general E-cen path gives E +0.240. The baryons are then compressed inside a vanishing edge, so part of the halo-model excess is the E-cen baryon truncation itself.
- **Halo-model scope.** CFG556's r200m-ball scope (both models truncated at r200m) gave a deficit; the frozen primary is the turnaround scope with the drained shell. The tested result follows CFG556's primary. The scope bracket that CFG556 disclosed (halo-model double counting) still applies.
- **MW edge value.** CFG553 quotes a census edge of 287 / 261 kpc (its McMillan17 baryons). This lane's Prof-based value (CFG513 baryons, 6e10) is 512 / 466 kpc. Both are ≫ 30 kpc, and scaling CFG553's value by this lane's ratios (0.760 / 0.753) gives about 218 / 197 kpc.
- **KiDS inner-bin label.** By the frozen wording ("every edge beyond 98 kpc") K-in is "affected", because 0.19% / 0.47% of lenses have smaller edges. The inner-9 χ² changes by −0.3 (canonical) and +1.1 (alt).
- **Inherited inputs.**
  - The EPS main-progenitor form and q = 2.2 are recalled and PROVISIONAL. The ceiling at q = 1.6 / 3.0 is 0.707 / 0.805 at log M_ta 12 and 0.525 / 0.670 at 14. This is a bracket, not a scan.
  - The ΛCDM accretion history is used as the framework's, because outside B ∩ C cold energy is cold matter and R3 conserves the turnaround mass.
- **The capture time** t_cap = r_e/(αV_f) uses the point-mass deep-law edge density with ρ_c/ρ_m = 1. The ceiling (t_cap = 0) does not depend on it.
- **KiDS lens epochs.** s_c* is interpolated between epoch tables at z = 0.10–0.50 in steps of 0.05.
- **Pre-freeze hand estimates** are listed in the criteria (§5). The EdS guess of a 0.4–0.6 ceiling was low: the computed value is 0.50–0.80, because shells reach r_e somewhat before full collapse.

Commits: criteria 5149a12f1; results in the commit that adds this README.
