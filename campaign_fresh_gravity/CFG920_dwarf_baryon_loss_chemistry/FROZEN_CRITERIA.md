# CFG920 FROZEN CRITERIA: is the D-i route's post-formation baryon loss compatible with the dwarfs' own chemistry? (before any script or number)

Block CFG920–929 (LEDGER.md row "CFG920–929 RESERVED"). Label: **CONDITION TEST** of CFG915/CFG916's dwarf route D-i.
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are kept apart and never pooled. Cold energy is real gravitating mass; no
particle species is added. Raw data and framework-native quantities only (no ΛCDM mass function, no simulation calibration).
Not "theory closed". Nothing here can say the data favour the framework.

## 1. The condition under test

CFG915 (route D-i; inherited by CFG916's LR-c reading) holds the faint dwarfs' excess as cold energy bound at the dwarf's formation
(population t, α_t = 0, retained) while the baryons were later lost. In the deep regime, t dominant:
M_obs/M_law = (M_b,form/M_b,now)^½, so the required post-formation loss factor of each dwarf is

  **L_req = M_b,form / M_b,now = exp(4E)**, E = ln(σ_obs/σ_law) (CFG827: Υ_SFH at [M/H] −1.31, Wolf estimator, ν_e kernel, stars only).

CFG915 found median L_req = 4.32 (16–84%: 1.18–17.8; 3 of 28 need none) over CFG827's 28 out-of-sample dwarfs, and called the
formation-epoch baryon masses unmeasured. CFG852 tested a *correlation* of the excess with the metallicity residual (none). This lane
tests the **absolute amount**: can each dwarf's chemistry (mean stellar [Fe/H], present gas, SFH) hold its own L_req?

## 2. What was read before freezing (disclosure; the test is NOT blind to inputs)

- CFG915 README, its D-i code (`np.exp(4 * E827)`) and `cfg915_results.json` D block; CFG916 ledger row only (its dir untouched).
- CFG827 README, `cfg827.py`, `cfg827_results.json` (per-dwarf E_SFH values were seen). CFG824 rows (σ, errors, τ50, τ90) seen.
- CFG852 README, criteria, `cfg852.py`, `cfg852.out` (MZR slope 0.508, partial ρ −0.108; secondary 0.344 / −0.024).
- CFG845 README; CFG860 README; THEORY_CANONICAL_2026-10-18.md (dwarf lines).
- **CFG317** README, its leaky-box estimator (`elnx`, `leaky`) and the structure of its stored `EST` block. Pre-knowledge from it:
  population median R_ind (homogeneous leaky box, yield −0.2) ≈ 117 UFD, 30 MW classical, 22 M31, 6 gas-rich field; Draco η 55,
  Sculptor 18, Leo T 14.7, WLM 4.0. LEDGER rows CFG317, CFG336, CFG338, CFG339, CFG834, CFG846, CFG873 read.
- LVD columns, the sample's LVD `metallicity` / `mass_HI` values and the Collins+13 [Fe/H] availability were listed (input inventory).
- Not done before: no lane compares D-i's L_req with a chemical-evolution bound (CFG317/338/339 used R_ind for other hypotheses).
- No CFG920 number has been computed. From CFG317's numbers the author expects the homogeneous leaky box to demand *more* loss than
  L_req for many metal-poor dSphs; this expectation is stated so it cannot be read as a discovery.

## 3. Sample and inputs (on disk only; nothing downloaded)

- **Graded sample:** CFG827's 28 out-of-sample dwarfs (CFG824 rows with train = False).
- **Metallicity (primary):** LVD `metallicity` (mean stellar [Fe/H]); error s = hypot(err, 0.1), err = mean of
  `metallicity_em`/`metallicity_ep` (0.2 if absent), 0.1 dex = CFG317's MDF-shape allowance. **A dwarf with no LVD metallicity is
  NOT TESTED** in the graded result.
- **Present gas:** M_g = 1.33 × 10^`mass_HI` (LVD detection). Dwarfs with only `mass_HI_ul` are gas-free (M_g = 0).
- **Stellar mass:** M★ = Υ_SFH([M/H] −1.31) × 10^{0.4(4.83 − M_V)} by CFG827's code path (needed only for gas-bearing dwarfs).
- **SFH clock:** Weisz+14 cumulative SFH (tables 5/6, CFG827's reader), onset F = 0 at 13.3 Gyr (CFG827's first-bin age), linear in
  log age between grid nodes; τ50, τ90 from CFG824 rows (τ90 = quench proxy).
- **Required loss:** L_req = exp(4E) per footing (E recomputed on both footings through CFG827's code path). Error
  σ_E² = (eso/so)² + (ln10 · 0.15/2)² (CFG827's per-dwarf variance).

## 4. The declared chemical-evolution bound (never fitted per dwarf)

One-zone **leaky box**: instantaneous recycling and mixing; **no inflow**; primordial start (Z₀ = 0, the favourable choice for a
small L); all baryons bound at formation are gas at star-formation onset; outflow rate η × SFR (η ≥ 0 constant) at the ISM
metallicity (ζ = 1). Then Z(u) = y u/(1 + η), u = ln(M_g0/M_g), stars distributed ∝ e^{−u} du. Matched observable: the model's
mass-weighted mean log₁₀(Z/Z_Fe,⊙) of the stars = the observed mean [Fe/H].

- **Yield bracket:** log₁₀(y_Fe/Z_Fe,⊙) ∈ {−0.5, −0.2 (nominal), +0.1} (CFG317's bracket, unchanged).
- **Outflow-form bracket:**
  - **W1 continuous wind** (CFG317's estimator exactly): gas-free dwarfs processed to exhaustion (μ → 0), L_W1 = 1 + η;
    gas-bearing dwarfs keep their present gas, L_W1 = (M_g + (1+η)M★)/(M_g + M★), η solved with u_q = ln((M_g + (1+η)M★)/M_g).
  - **W2 continuous wind + terminal removal** of the gas left at quench (unprocessed), gas-free dwarfs only: free u_q ∈ (0, ∞]
    (μ_q = e^{−u_q}), η(u_q) from the metallicity, η ≥ 0; L = (1+η)/(1 − μ_q); **L_min,W2 = min over u_q**. For gas-bearing dwarfs
    W2 ≡ W1.
- **Unseen loss:** gas lost without ever mixing into the star-forming ISM is invisible to the chemistry and can only raise L. The
  allowed set in corner k (yield × form) is therefore **[L_min,k, ∞)**, L_min,k = L_W1 (W1) or L_min,W2 (W2).
- If the model cannot reach the observed [Fe/H] even with no loss (closed box below the observation at that yield), η = 0, L_min = 1,
  flagged "chemistry under-produces [Fe/H]" (pre-enrichment would be needed; not modelled).

**Direction of a contradiction (stated in advance).** A dwarf "cannot hold" its L_req when L_req < L_min: the chemistry demands
*more* post-formation loss than D-i allows, so D-i, with that loss after binding, would over-predict the dwarf's excess
(E_pred = ln L_min / 4 > E_obs). A dwarf with L_req ≤ 1 (no excess) cannot hold any loss.

## 5. Classes

**Per dwarf, per footing** (corners k = 3 yields × applicable forms; "holds" = L ≥ L_min,k):
- favourable values: L⁺ = exp(4(E + σ_E)), [Fe/H]⁺ = [Fe/H] + s; unfavourable: L⁻ = exp(4(E − σ_E)), [Fe/H]⁻ = [Fe/H] − s.
- **COMPATIBLE:** holds in every corner at the unfavourable values.
- **CONTRADICTED:** holds in no corner at the favourable values (even the most favourable bracket cannot hold L_req).
- **UNDERDETERMINED:** otherwise (the bracket and the 1σ errors span both).
- The same rule at central values is reported (not graded).

**Sample median, per footing** (tested set T): M_req = median L_req over T; M_k = median L_min,k over T (form W2 means W2 for
gas-free and W1 for gas-bearing dwarfs); ratio r_k = M_req/M_k. Bootstrap over dwarfs, 2000 draws, seed 920 (same draw for both
medians): **COMPATIBLE** if the 16th percentile of r_k ≥ 1 in every corner; **CONTRADICTED** if the 84th percentile of r_k < 1 in
every corner; **UNDERDETERMINED** otherwise. CFG915's headline median (4.32, all 28) against M_k and the median of per-dwarf ratios
are reported.

**Overall CFG920 class** = the sample-median class if both footings agree; otherwise "SPLIT (canonical X / alt Y)".

## 6. Timing map (reported; not part of the amount class)

CFG915 needs the loss *after* the cold energy was bound at formation. Primary amount test binds at SF onset (all chemistry-traced loss
post-binding). Map: if binding follows a fraction F of the star formation, the post-binding loss is
- gas-free: L_post(F) = min over the W1/W2 family of [(1+η)/(1 − μ_q) − ηF] (the strip happens at quench, after binding);
- gas-bearing: L_post(F) = L_W1 − ηF M★/(M★ + M_g).

At yields −0.5 and −0.2 (central values): F_need = the smallest F ∈ [0, 1] with L_post(F) ≤ L_req; t_need = the lookback time at
which the Weisz+14 cumulative SFH reaches F_need; reported beside τ50 and τ90. Readings: **AT FORMATION** (F_need = 0), **EARLY**
(0 < F_need ≤ 0.5), **LATE** (F_need > 0.5: binding would follow most of the star formation, not "at formation"), **NONE** (no F ≤ 1).
For dwarfs whose L_req exceeds the chemistry-traced loss (needs unseen loss), the extra loss must fall between binding and quench;
τ90 is reported as that window's end for gas-free dwarfs.

## 7. Escapes outside the graded bracket (reported map, no class weight)

- **Metal-enhanced winds:** wind metallicity ζ Z_ISM, ζ > 1: dZ/du = [y − (ζ−1)ηZ]/(1+η). ζ_need = the smallest ζ ∈ [1, 1000] for
  which the W2-type family (wind at ζ + terminal strip) at yield −0.5 holds the central L_req; "> 1000" if none. Reported per dwarf
  and as a median. No ζ > 1 is declared standard here; ζ_need states the price.
- **Pristine inflow after binding** (later lost) decouples [Fe/H] from L; the leaky box excludes it by definition. Disclosed, not
  modelled.

## 8. Reported variants (not graded)

- V-COL: Collins+13 [Fe/H] (e_[Fe/H]) for M31 dwarfs lacking an LVD metallicity (CFG317's precedent).
- V-TR: the 8 MW training dwarfs of CFG824/827 (classes as in §5).
- V-GAS: HI-bearing dwarfs with all gas counted in the law's baryons, E_gas = ln(σ_obs/σ_law(M★ + 1.33 M_HI)) (CFG873's "all-gas" end).
- V-2σ: the §5 rule at 2σ.
- V-NOUNSEEN: allowed set [L_min,k, L_W1,k] (no unseen loss); counts of dwarfs whose L_req exceeds L_W1 even at yield +0.1.
- Reported per dwarf: L_min at every corner, E_pred = ln(L_min)/4 at (−0.5, W2) and (−0.2, W1), the unseen-loss factor
  L_req/L_W1 at the nominal yield.

## 9. Controls

- **K1** (CFG827/CFG915 through this code path): every CFG827 row's E_SFH (36 rows) to |Δ| ≤ 1e-9; CFG827's stored alt-footing
  ρ to 1e-9; CFG915's loss-factor median, p16, p84 (relative 1e-9) and n_le1 = 3, N = 28 exactly.
- **K2** (CFG852): primary MZR slope and partial ρ, and secondary slope and ρ, to 1e-9 against `cfg852_results.json`.
- **K3** (CFG317): this code's W1 estimator reproduces every non-null stored CFG317 `EST` entry (η relative 1e-8, log R_ind 1e-9) at
  all three yields from CFG317's own stored (feh, Ms, Mg).
- **K4** (numerics): the ζ > 1 closed form Z(u) against direct ODE integration (relative 1e-6); the quadrature mean log Z at ζ = 1
  against CFG317's closed form (1e-9); W2's η = 0 endpoint against the closed-box truncation formula (1e-9).
- **MUTATE** (separate outputs, `CFG920_MUTATE=1`): replace every L_req by 1 (M1) and by 20 (M2), chemistry unchanged. The tooth
  bites if the canonical sample-median class differs between M1 and M2 **and** at least half of the tested dwarfs change per-dwarf
  class. MUTATE exits 1 when it bites (record convention), 0 when it does not.
- Main run exits 0 only if every K passes.

## 10. Approximations stated now

- D-i's amount relation is deep-regime, t-dominated and order of magnitude (CFG915); it is used as given. Stars-only E is CFG915's
  definition and overstates L_req for gas-rich dwarfs (V-GAS shows the size).
- Instantaneous recycling for Fe (SN Ia delay) is carried by the yield bracket; mean [Fe/H] (number-weighted RGB) vs mass-weighted
  mean log Z by the 0.1 dex allowance.
- The leaky box is one zone; no MDF-shape fit is graded.

## 11. Compute and wording

One core (OMP_NUM_THREADS=1, nice -n 10), < 1 GB, one process at a time, beside the live 1024³ job; no other process touched; nothing
downloaded. Any change after this commit is a dated, labelled amendment. CONTRADICTED is reported as plainly as COMPATIBLE.
κ = ½ FITTED; footings never pooled; not theory closed.
