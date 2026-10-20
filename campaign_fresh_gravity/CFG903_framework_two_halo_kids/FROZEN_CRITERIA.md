# CFG903 FROZEN CRITERIA: the framework's own catalogue two-halo term for the KiDS isolated lenses, added to CFG804/CFG902's one-halo model (committed alone, before any script)

## Why

- CFG804 (catchment supply, cold energy = 5.364 N M_b, N = 1/f_ret, census floor caps N at 10) fits B21 Fig. 3 inside
  R ≤ 0.31 Mpc but FALLS SHORT over all radii. After CFG902's unit fix (declared Msun/h ramp, h 0.674) the all-radii
  Δχ²(D_der − B) is **+100.10 canonical / +123.12 alt** (primary +0.84 / −0.27). CFG803: a one-halo model needs N_min 16–24.
- Both lanes name the framework's two-halo term (neighbours' baryons and cold energy along the line of sight) as the next step.
- Record context, stated so nothing is double-claimed:
  - CFG805 added a two-halo term built from T1x's P_grav (inherited ΛCDM initial conditions) with a **free bias per bin**
    (b_eff 0.2–0.5). That narrowed CFG804's pre-unit-fix +149 to +11.
  - CFG502/503 built a ΛCDM halo-model environment term. It is not usable for a verdict here.
  - CFG644 asked for "a framework-native neighbour-lensing model".
- **This lane has no free amplitude.** The neighbours are the observed KiDS-bright galaxies around each lens. Each carries
  the framework's own mass: its baryons plus its catchment cold energy, with CFG804's profile.

## Inputs (on disk; no download)

- **B21 Fig. 3:** four mass bins plus the full covariance, read by CFG804's own code.
- **Bright sample:** `KiDS_DR4_brightsample.fits` with `_LePhare.fits` (1,239,422 objects, IDs matched).
  - log M★ = MASS_MED + 0.15 (the record's flux scale).
  - M_b = M★ (1 + f_cold), f_cold = 10^(−0.69 log M★ + 6.63), the record's recipe as in lr_lenses.
- **`lr_lenses.npz`:** the record's 181,477 isolated lenses.
- **`cfg96_isoflags.npz`:** the f30 flags.
- **KiDS-1000 SOM n(z):** `_external_data/cfg592_work/.../xipm_KIDS1000_*.fits`, NZ_SOURCE, used only for the lens weights.
- **Distances:**
  - χ uses the record's DC (flat, Ω_m 0.3, H0 70), as in lr_lenses' `chi` column.
  - Projected radii are physical, at the lens: d = θ χ_l/(1+z_l), in h70⁻¹ Mpc.
  - Masses are in h70⁻² Msun. These are B21's units; CFG804 compares in the same units.

## Lens samples (stellar-mass bins = B21's: log M★ ∈ [8.5, 10.3, 10.6, 10.8, 11.0))

Isolation is rebuilt for all lens candidates with CFG502's verbatim pool and candidate definitions:
- pool = r < 20, 0.1 < z < 0.5, masked = 0, finite log M★ > 7;
- candidates = pool, log M★ < 11, finite u−r; expected 605,531.

A candidate is vetoed by a pool galaxy with log M★_j > log M★_l − 1 inside the stated cylinder (chord < r/χ_l, |Δχ_phot| < W).

| id | criterion | role |
|---|---|---|
| **I0** | comoving 3 Mpc, W = 10 Mpc (the record's reconstruction; must equal lr_lenses) | **primary** |
| I1 | comoving 3 Mpc, W = 30 (the record's f30) | stricter photo-z window |
| I2 | **physical** 3 Mpc (comoving 3(1+z_l)), W = 10 | fiducial-units radius (B21 quote 3 h70⁻¹ Mpc) |
| I5 | comoving 3 Mpc, W = W_B chosen (0.1 Mpc steps in 1–30) so that the number of candidates passing is closest to B21's 259,383 | count-matched to B21 (the record's 181,477 is stricter than B21's sample) |

W_B is set from counts only, never from lensing.

## Neighbour mass model (framework-native, no fitted constant)

**Neighbour pool.**
- Bright-sample objects with r < 20, 0.02 ≤ z_phot ≤ 0.8 and finite log M★ > 7.
- Primary: masked = 0 only (as B21 and the pool). Bracket M1 adds masked = 1 objects.
- The lens itself is excluded.

**Mass of each neighbour j.**
- Baryons M_b,j: a point mass.
- Catchment cold energy 5.364 N_j M_b,j.
  - N_j = 1/f_ret from **CFG902's declared fixed point**: log M_ta[Msun/h] = log M_b − log10(f_ret f_b) + log10 0.674,
    with CFG416's ramp and f_b = 1/6.364.
  - It is evaluated at the centre of the neighbour's 0.05-dex log M_b cell.

**Cold-energy profile.**
- CFG804's law profile ρ(s) = M_b/r_M³ · 1/(2π s √(1+4s²)), truncated at s_max = edge(N_j), with
  r_M = √(G M_b/a0) for each footing.
- The shape uses the nearest N in NGRID ∪ {1.25, 1.5, 1.75}, and is renormalised to the exact mass 5.364 N_j M_b,j.
- The lens one-halo model is CFG804 verbatim (snapped NGRID).

## Two-halo estimator

**The neighbour mass inside each radius.**
- For each lens l, M_l(R) is the neighbour mass (baryons + cold) projected inside the circle of radius R about the lens.
- Neighbours contribute if their projected physical separation is d < 4.61 Mpc and |Δχ_phot| < W.
- Off-centre profiles are handled exactly: tabulated F(R/r_M, d/r_M; N), the fraction of the projected profile inside
  the lens circle.

**Bin averages over B21's 15 log bins (0.03–3 Mpc).**
- ΔΣ_bin = (1/A_bin)[∫ 2M(R)/R dR − (M(R₂) − M(R₁))].
- Point masses are done analytically. Extended cold energy uses 16-node Gauss–Legendre quadrature in ln R per bin.
- The bin average is disclosed. The one-halo stays point-evaluated as in CFG804.
- Neighbours are histogrammed in d (240 log bins, with B21's edges on bin edges) and log M_b (0.05 dex). Every variant is a
  kernel-stage sum over the same histograms.

**Stack.**
- Weighted mean over lenses, with B21-like per-lens weights W_l = S2(z_l)/D_A(z_l)².
- S2 is the Σ_crit⁻² source sum with the Z_B > z_l + 0.2 cut, from CFG885's S1 source model at B21's fiducial Ω_m 0.2793.

**Random subtraction (removes the uniform background and the catalogue's mask holes).**
- ΔΣ_2h = ΔΣ(lenses) − ΔΣ(randoms).
- Each lens gets one clone at a random footprint position, inheriting z, M, weight and flags.
- A random position is accepted if its nearest bright-sample object (any flag) is within 4′ and has masked = 0, so
  randoms, like lenses, sit off the mask.

**Exclusion (no double counting of the lens's own catchment, E1, primary).**
- Neighbours less massive than the lens (M_b,j < M_b,l, catalogue masses) with d < r_x are dropped.
- r_x is the D model's own edge for the bin's trial mass, edge(N_snap) r_M, so the exclusion is recomputed inside the fit.
- More massive neighbours are kept: they are hosts, and the lens sits in their catchment (CFG644's basin rule).

**Jackknife.**
- 50 sky patches (agentK's RA-quantile scheme on the I0 lenses; the boundaries are applied to all lenses and randoms).
- Delete-one gives the noise on the two-halo vector and on Δχ².

## Score (CFG804's own χ², unchanged)

**Fit.**
- CFG804's `cfg804.py` (blob b1749cb85e…, as in CFG902) is exec'd with CFG902's replacements R1 and R2 (the declared
  convention) plus output redirection into this lane.
- That gives CFG804's data, covariance, `model`, `f_for`, `N_of`, GRID, ZK, and the primary (R ≤ 0.31 Mpc) and all-radii
  index sets.
- Model D+2h = CFG804's D_der + ΔΣ_2h(r_x(L_b)). Bin masses are profiled exactly as in CFG804: grid 9.00–12.00 in 0.01,
  3 sweeps from ZK.

**Statistic.**
- **B is CFG804's fixed reference** (the no-edge law, nothing added; its unlimited isothermal phantom already includes
  "everything").
- Δχ² = χ²(D+2h) − χ²(B), per footing (canonical 9.3603e-11, alt 1.1312e-10), never pooled.

**Primary variant.** I0, W = 500 Mpc, completeness C1, profile P1, exclusion E1, unmasked neighbours, B21 weights.

**Classes (all radii, per footing).**
- **TWO-HALO CLOSES** if Δχ²_all ≤ 4 (CFG804's threshold).
- **PARTIAL** if 4 < Δχ²_all ≤ ½ × CFG902's value (≤ 50.05 canonical, ≤ 61.56 alt).
- **DOES NOT CLOSE** otherwise, labelled "WORSENS" if Δχ²_all rises above CFG902's value.

**Also reported:**
- the primary-range Δχ² and whether SUFFICES (≤ 4) survives the two-halo term;
- χ²(D+2h) and its p-value;
- the profiled masses and edges;
- σ_jk(Δχ²), with a note if the class threshold is within 2σ_jk.

## Brackets (each reported with its class; varied one at a time from the primary)

| bracket | what changes |
|---|---|
| Completeness | **C1 (primary)**: per lens, the neighbour sum is scaled by R_c1(z_l) = S(m₁)/S(max(m₁, m_lim(z_l))). S(m) is the total mass Σ M_b(1 + 5.364 N) of pool galaxies with log M★ ≥ m in the slice 0.10 ≤ z < 0.12; m₁ = m_lim(0.11); m_lim(z) = 5th percentile of log M★ in \|z_phot − z\| < 0.01 (CFG502's definition). **C0**: none (lower). **C2**: the same with the deeper slice 0.06 ≤ z < 0.08 (upper). Assumes the missing faint neighbours cluster per unit mass like the observed ones (an upper-side assumption) |
| Photo-z window | W = 300, W = 1000 (W = 100, 200 reported only) |
| Isolation | I1, I2, I5 (above) |
| Cold-energy distribution | **P0**: all cold energy at the neighbour (point, most concentrated). **P2**: the same mass on the law shape cut at 2 s_max (more diffuse) |
| Exclusion | **E0**: none (upper; double counts the lens's satellites). **E2**: all neighbours with d < r_x dropped, hosts included (lower) |
| Weights | uniform per lens |
| Mask | M1: masked-flag objects added as neighbours |

**Robustness line.** The verdict states the primary class per footing and lists every bracket that changes it.

**Stated bound direction.** Per-galaxy catchments are not shared (CFG522's sharing rule is not applied), so neighbour
supply in groups is **over-assigned**. Sharing can only lower it (f_ret rises with mass; CFG525). The primary is therefore
an upper bound with respect to catchment sharing.

## Controls (binding unless marked)

- **K0a:** I0 reproduces lr_lenses exactly (181,477 lenses; ra, dec, z, logM, Mgal, chi equal).
- **K0b:** I1 restricted to I0 equals cfg96 f30 (57,265).
- **K0c:** 605,531 candidates.
- **K1a:** the exec'd CFG804 (R1/R2) reproduces CFG902's committed `cfg902_results_declared{,_alt}.json` (χ², Δχ², p_D,
  logMb) to ≤ 1e-9.
- **K1b:** this lane's D+2h fit with ΔΣ_2h ≡ 0 reproduces the same numbers to ≤ 1e-9: all radii +100.10 / +123.12,
  primary +0.84 / −0.27.
- **K2a:** this lane's projected cold profile reproduces CFG804's one-halo f(X) (its `profile`) to ≤ 5e-3 relative, for
  N = 1, 5.5, 10 over X ∈ [0.01, 0.95 s_max].
- **K2b:** F = 1 when the neighbour disc lies inside the lens circle and 0 when outside, to 1e-6. F(x, u = 0) matches
  direct integration to 1e-3.
- **K2c:** a synthetic uniform neighbour field gives |ΔΣ_bin| ≤ 2e-3 Σ₀ in all 15 bins. This is checked for log M_b 10.5
  and 12.0, with P1, on both footings.
- **K3 (random machinery):** split the randoms into halves A and B. The weighted mean over the 28 outer points
  (R ≥ 0.4 Mpc) of ΔΣ_A − ΔΣ_B must be within 3σ_jk of zero.
- **MUTATE** (`CFG903_MUTATE=1`, separate outputs): every neighbour's M_b is doubled, with N and r_M re-derived at 2M_b.
  It **bites** if |Δχ²_all(MUTATE) − Δχ²_all(primary)| ≥ 1 on both footings. Zeroing the neighbours is K1b.

## Reported only (no verdict weight)

- **Amplitude scan:** Δχ²_all of D + A·ΔΣ_2h for A in 0–6 (step 0.1), with masses re-profiled. Reports A_best and the
  range of A with Δχ² ≤ 4: how much catalogue two-halo the data would need.
- The two-halo vector per bin and the host share (neighbours more massive than the lens).
- The random-only signal (size of the mask term).
- Lens counts per sample, W_B, and the completeness factors.

## Limits and disclosures (stated in advance)

**Compute.**
- One core (OMP_NUM_THREADS=1, nice 10); each process < 1.5 GB and < 15 min, enforced by a watchdog.
- Staged as `cfg903_stage.py` (isolation, randoms, weights, completeness), then `cfg903_pairs.py BIN` (one process per mass
  bin), then `cfg903_score.py`.
- Large arrays go to `../../../_external_data/cfg903_work/` and are not committed.
- If a bin's pair run exceeds the limits, it is rerun on a seeded (903) random subsample of that bin's lenses (and their
  clones), sized to fit, and the fraction is reported. If nothing fits, the lane stops and reports what it needs.

**Not modelled.**
- True-z lensing efficiency of neighbours: correlated neighbours sit at the lens redshift, and uncorrelated ones cancel
  against the randoms.
- Neighbour mass errors from photo-z.
- Mass not attached to any catalogued galaxy's catchment (beyond the C1/C2 completeness scaling).
- The lens's own share of a host's catchment.
- Correlated neighbours beyond 4.61 Mpc. P1 and MUTATE extents are ≤ 1.37 Mpc, so they are exact to 3 Mpc. P2 extents
  reach 2.1 Mpc for the rarest neighbours (log M_b ≳ 12.5).

**Other.**
- The one-halo masses stay profiled per bin (CFG804).
- The census f_ret is an observational input carried in the record, not derived (CFG804, CFG806).
- B21's actual isolated sample (259,383) differs from the record's reconstruction (181,477). I5 brackets this.

κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; raw KiDS data, framework-native model (no ΛCDM halo-model two-halo term); not theory closed.
