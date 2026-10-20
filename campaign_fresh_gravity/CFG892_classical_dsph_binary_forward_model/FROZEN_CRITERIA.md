# CFG892 FROZEN CRITERIA: can UNDETECTED binaries make the classical dSphs' excess? (before any script)

**Why.** CFG861 (PARTIAL) cleaned the classical dSphs' multi-epoch member sets M (Walker+2023 per-epoch catalogue through
CFG51's reducer) and found that detected binaries move the excess by only −0.045 ± 0.030 dex. Its open caveats: (1) δ is a
lower bound, because most stars in M have 2 epochs and long-period or low-amplitude binaries escape the χ² test (CFG93: the
flagging catches 9–13% of realistic binaries at ultra-faint cadences); (2) no instrument zero-point offset is modelled, and
Sextans pools three instrument files; (3) the ~4.5 km/s single-epoch bound (McConnachie & Côté 2010, used by CFG29/CFG861)
was not re-checked. This lane forward-models the binaries that pass the cleaning, at each member's real epochs and errors,
and asks whether law + binaries can produce the cleaned dispersions. Block CFG890–899 (orchestrator reservation; this is CFG892).

## Data path (reuse CFG861 exactly)
CFG51's `reduce_walker.py` imported unchanged; the three Walker+2023 files; `build_stars`, `load_lvd`, `membership` as CFG861
calls them; classical = LVD-matched and M_V ≤ −7.7; M = members with ≥ 2 quality epochs. Per-epoch arrays (HJD, Vlos, e_Vlos,
instrument file) are rebuilt with the same quality filter, row order and stable HJD sort as `build_stars`. Δ_LVD from CFG852's
`delta_ups2` (extracted with `ast` as CFG860/CFG861 did; Υ_V = 2, Wolf at r_1/2 = 4/3 r_h, kernel ν_e), canonical
a0 = 9.3603e-11 (graded), alt 1.1312e-10 (reported, same grid). σ_law² = law(g_bar)·r_1/2/3 = σ_LVD²·10^(−Δ_LVD).

## Forward model (one realization)
For each star i in M with epochs t_ij, quoted errors e_ij and instrument k_ij:
v_ij = u_i + b_i(t_ij) + z_k + e_ij·n_ij, with u_i ~ N(0, σ_true), n_ij ~ N(0, 1), b_i a Keplerian radial velocity if the star
is a binary (probability f), else 0; z_k = instrument offset (0 except in the Sextans Z2 variant). Then CFG51/CFG861's own
steps on the simulated M: inverse-variance star means and χ² (dof n−1); the membership velocity window
|v̄_i − v_c| < 4√(σ_seed² + ē_i²) with σ_seed = max(σ_LVD, 3) km/s, pass 1 about the true systemic (0), pass 2 about the median
of the pass-1 means (one recentring); kept set K; σ_single,sim = Gaussian MLE (known errors, free mean, σ ≥ 0, CFG51's
likelihood) on the first epochs of K; cleaned set = K minus stars with χ² p < 0.01; σ_clean,sim = MLE on their all-epoch means.
A paired no-binary twin (same u_i, n_ij, z_k; b = 0; own window and cleaning) gives σ_single,0 and σ_clean,0.
σ_true = σ_law (the law's prediction; H0 = "law + binaries"). R = 1000 realizations per cell; seeds from
numpy SeedSequence([892, system, population, f, footing, variant]).

**Binary populations** (P in days; sources are values already in the repo, otherwise stated as brackets):
- **P1** log-normal, mean log P = 5.03, σ = 2.28: the values CFG93 used (`cfg93.py`, labelled "DM91" there; they are the
  Raghavan et al. 2010 field values).
- **P2** log-normal, mean log P = 4.8, σ = 2.3: Duquennoy & Mayor 1991, as used in CFG334.
- **P3** log-normal, mean log P = 4.0, σ = 2.28: CFG93's short-period-heavy variant.
- **P4** flat in log P on [0.5, 8]: CFG93's flat variant.
- **P5** P1 with thermal eccentricities f(e) = 2e on [0, 0.95] for P > 10 d (a bracket, not a value cited in the repo).
- Common (CFG93): q = M2/M1 ~ U[0.1, 1]; M1 = 0.8 M_⊙ (old giants; also the Arroyo-Polonio+2026 primary, CFG259);
  e ~ U[0, 0.8] for P > 10 d and e = 0 for P ≤ 10 d; 1 < P < 1e10 d; isotropic inclination; uniform ω and mean anomaly;
  periastron a(1−e) ≥ 3 R1 with **R1 = 10 R_⊙** (CFG334's value; CFG93's 15 R_⊙ removes more short orbits, so 10 is the more
  generous); orbits failing the cut are redrawn (CFG93's rule, which keeps f).
- **Graded binary fraction f ∈ {0.3, 0.5, 0.7}.** Reported only: f = 1.0; **P6** = P1 with no periastron cut (unphysical for
  giants, an upper bracket) at f 0.7 and 1.0; P1 with R1 = 15 R_⊙ (CFG93's setting) at f 0.5 for the catch-rate comparison.

## Need and graded statistic
- σ_obs,W = σ_clean(M) (CFG861, Walker data, the same stars and pipeline as the simulation).
- σ_obs,L = σ_LVD·σ_clean(M)/σ_single(M) = σ_LVD·10^(δ/2) (CFG861's Δ_clean frame).
- **Graded σ_obs = min(σ_obs,W, σ_obs,L)** (the smaller, i.e. the more generous to binaries).
  **σ_need = √max(σ_obs² − σ_law², 0)** (extra dispersion over the law, in quadrature).
- Simulated excess σ_ex = sgn(σ_clean,sim² − σ_law²)·√|σ_clean,sim² − σ_law²| (includes sampling noise, which is generous at
  the 95th percentile). Paired binary inflation I2 = the same with σ_clean,0 in place of σ_law (reported).
- **Per graded dwarf: Q95 = the maximum over the 15 graded cells (P1–P5 × f 0.3/0.5/0.7) of the 95th percentile of σ_ex.**
  The dwarf's need is **reached** if Q95 ≥ σ_need (equivalently, the 95th-percentile simulated σ_clean ≥ σ_obs). The largest
  P(σ_clean,sim ≥ σ_obs) over cells is printed.
- **Graded dwarfs:** CFG861's graded five (Crater II, Sextans, Ursa Minor, Draco, Carina), canonical footing. A dwarf with
  σ_need = 0 is "nothing to explain" and is not counted.

## Classes (canonical, graded)
1. **NOT DIAGNOSTIC** if fewer than 3 graded dwarfs have σ_need > 0.
2. **BINARIES CANNOT EXPLAIN** if no dwarf with σ_need > 0 is reached.
3. **BINARIES COULD EXPLAIN** if every dwarf with σ_need > 0 is reached.
4. **PARTIAL** otherwise (the reached dwarfs named).

## Reported, not graded
1. Alt footing on the same grid (class printed).
2. σ_obs,W only and σ_obs,L only (classes printed).
3. f = 1.0, P6 and P1/R1 = 15 R_⊙: per-dwarf Q95 and the class they would give.
4. **The 4.5 km/s bound replaced by the forward model:** the 95th percentile of the single-epoch excess (σ_single,sim in place
   of σ_clean,sim), maximum over the graded cells, against CFG861's σ_bin = σ_LVD√(1 − 10^(−Δ_LVD)) (the binary dispersion for
   the whole excess, pre-cleaning), both footings. Also the binary-only single-epoch dispersion at σ_true = 0.2 km/s on each
   graded dwarf's M epochs and errors (P1–P5, f 0.7; median and 95th percentile), the kind of number McConnachie & Côté 2010
   quote. The paper itself is not re-read (no download), so this is a re-derivation under this lane's populations, not a check
   of its text.
5. Per cell: paired inflation I2 (median, 95th), catch rate (flagged binaries / binaries in K), flag fraction against the
   observed n_rm/|M|, window rejections, simulated δ = 2 log10(σ_clean,sim/σ_single,sim) and P(δ_sim ≤ δ_obs). The observed
   flag fractions are a diagnostic of f and of the error calibration; they are NOT used to narrow the bracket.
6. Other classical systems with |M| ≥ 15 (Antlia II, Leo II, Sculptor, Fornax, Leo I): σ_need and Q95 over the graded bracket,
   both footings.

## Sextans instrument zero point (reported; the class it would give is printed)
- **Z1 measured.** From Sextans stars in M with quality epochs in two instrument files: per star and instrument, the
  inverse-variance mean; per-star difference d = v̄_B − v̄_A with error √(ē_A² + ē_B²); offset = inverse-variance weighted
  mean of d with iterative 3σ clipping (|d − offset| > 3·error removed, to convergence, at most 20 passes); error = weighted
  mean error × max(1, √(χ²/dof)). Pairs (Hectochelle → M2FS HiRes) and (M2FS HiRes → M2FS MedRes); MedRes − Hectochelle = the
  sum. The offsets are subtracted (Hectochelle reference) and CFG861's like-for-like shift is recomputed on the same M
  (σ_single(M), σ_clean(M), n_rm, δ, Δ_clean both footings); the new σ_obs and σ_need are compared with the zero-offset
  simulations. The count of M stars whose membership would change on a re-run is reported.
- **Z2 bracket.** Sextans simulations with injected offsets z = (0, +x, −x) km/s for (Hectochelle, HiRes, MedRes),
  x ∈ {0.5, 1, 2, 3}, and with the measured offsets, at the most generous graded cell (largest 95th percentile) and at P1
  f 0.5: Q95, flag fraction, δ_sim, against the uncorrected σ_obs.

## Controls
- **K1 (binary fraction 0 reproduces CFG861):** with zero binary motion on the real velocities, the lane's data path and
  pipeline (window with the real v_c and σ_seed, χ² cleaning, CFG51's `mle_sigma`) reproduce `cfg861_results.json` for all 10
  systems with |M| > 0: |M|, n_rm, σ_single(M) and σ_clean(M) (sig, +err, −err), difference exactly 0; every M star passes the
  re-applied window. Δ_LVD (both footings) equals CFG861's JSON exactly; σ_law from law(g_bar)·r_1/2/3 equals
  σ_LVD·10^(−Δ_LVD/2) to 1e-12 relative.
- **K1b:** the vectorised MLE used in the simulations reproduces `mle_sigma` on the 20 real sets (single and clean, 10
  systems) to ≤ 1e-4 km/s.
- **K2 (f = 0 simulations, σ_true = σ_law, R = 1000):** median σ_clean,sim/σ_law within 1 ± 0.05 and false-flag fraction in
  [0.003, 0.03] for every graded dwarf.
- **K3 (Kepler):** the 29.78 km/s constant equals 2π AU/yr from SI constants to 1e-3; a circular orbit's RV amplitude equals
  K to 1e-9; the RV averaged over a uniformly sampled period is 0 to 1e-6 K at e = 0.6.
- **MUTATE** (`CFG892_MUTATE=1`, separate outputs `cfg892_MUTATE.out`, `cfg892_results_MUTATE.json`): population log-normal
  log P mean 1.5, σ 0.3 (P ~ 16–63 d), q ~ U[0.5, 1], e = 0, no periastron cut, f = 0.7, σ_true = σ_law canonical, the five
  graded dwarfs, R = 1000. Must hold: (a) median catch fraction ≥ 0.70 in every graded dwarf; (b) median σ_ex(clean) < median
  σ_ex(single) in every graded dwarf; (c) the single-epoch class (95th percentile of the single-epoch excess against
  √max(σ_single(M)² − σ_law², 0)) is COULD EXPLAIN. If any fails, the main result is labelled UNCONTROLLED.

## Hand expectations (disclosed before any script)
CFG861's committed numbers were read. By hand (σ_law = σ_LVD·10^(−Δ/2), canonical): σ_law ≈ Draco 4.6, Ursa Minor 4.6,
Sextans 4.4, Carina 5.2, Crater II 3.9 km/s; graded σ_obs ≈ 9.07 (W), 8.71 (L), 6.57 (L), 6.14 (W), Crater II below the law;
σ_need ≈ 7.8, 7.4, 4.9, 3.2, 0 km/s. CFG93's ultra-faint simulations suggest undetected binaries bias σ_clean by +3–5% at
σ ≈ 4 km/s (about 1–1.5 km/s in quadrature), so Draco, Ursa Minor and Sextans are not expected to be reached; Carina
(need ≈ 0.6 σ_law) is the closest call. No simulation has been run.

## Declared limitations
Uniform intrinsic σ (no radial profile); Δ's own systematics (Υ_V, distance, r_h) are not varied; zero points between runs or
configurations within one instrument are not modelled; errors are taken as quoted; triples are ignored; q and M1 are fixed and
the old metal-poor giants are assumed to have field-like period shapes (the bracket spans the shape); single-epoch stars are
not used (as in CFG861). Any change after the first run is labelled POST HOC in the README.

## Resources
A 1024³ run is live. One process, numpy/scipy only, `OMP_NUM_THREADS=1 nice -n 10`, under 10 min per invocation (cells may
be split across invocations without changing anything else), under 2 GB, nothing downloaded.

κ = ½ fitted; cold energy mass required; not theory closed.
