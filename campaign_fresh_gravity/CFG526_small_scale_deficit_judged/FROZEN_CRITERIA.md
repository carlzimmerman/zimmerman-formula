# CFG526 FROZEN CRITERIA: judge the small-scale power deficit on the framework's own terms (A) and against data (B)

Committed alone, before any analysis of halo profiles or any data comparison. Date 2026-10-09.

## Finding being judged (CFG521, CFG524, CFG518, CFG506)

In the zero-knob PM engine (cfg518/521 physics), once halo interiors are resolved, P/P_S0 at k = 4 h/Mpc falls 0.89 (L200) -> 0.80 (L100) -> 0.63 (L50) -> 0.59 (L25), growing with time; every per-catchment compensation draw tried (s_c, R2, R1) de-concentrates halos; no compensation (NOCOMP) does not. CFG506 (512^3) saw P ratio -16..-20% at k 2-3. The gate that calls this TENSION compares with S0 (cold energy evolved as ordinary cold matter = the LCDM-equivalent) up to k_Nyq/4. That yardstick is inherited. This lane asks two other questions: (A) is the de-concentration what the framework's own law requires, and (B) does the predicted suppression conflict with observations of small-scale matter power. A fail is verified as hard as a win; nothing is tuned.

Settings: kappa = 1/2 FITTED; footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) never pooled; a0 flat; kernel nu_mono; the cold energy's MASS is still required; not "theory closed".

## Inputs (existing arrays only; no new PM run is planned)

z = 0 particle positions (256^3, seed 359) in `_external_data/cfg521_work`, `cfg524_work`, `cfg518_work`, `cfg359_work`; P(k) at z = 1, 0.5, 0 from the run JSONs.

| box | runs used |
|---|---|
| L50 | S0, census canonical (DC-can, old draw), census alt (DC-alt), K1 (f_ret = 1), NOCOMP; CFG524 R2-can / R2-alt (reported) |
| L25 | the same |
| L100 | S0, DC-can (alt not run there) |
| L200 | S0 (CFG359 N256), CFG518 DC-can, DC-alt |

A new PM run (nice 10, <= 4 threads, <= 2 runs, never 512^3) is allowed only if a frozen statistic below cannot be computed from these arrays; any such run is disclosed as a dated departure.

## Engine gravitating field (how "measured M(<r)" is defined)

For each run, the engine's own force routine (`forces`, cfg521_pm.py / cfg524_pm.py, imported unchanged, diag = True, a = 1, RC = 0, MIXA, FLAT, the run's footing, f_ret mode and NOCOMP flag, L and RMIN = 2L/256 as launched) is called once on the CIC density of the saved z = 0 positions. The total potential's Fourier transform is captured exactly from the three acceleration inverse transforms (no finite differences), and the gravitating overdensity is delta_grav = -k^2 phi_k a / (1.5 Om). The engine gravitating density is rho_grav = 1 + delta_grav (mean matter units). It equals particles + (e - comp) of the engine (k = 0 dropped, as in the engine).

Integrity (all must pass, else A = NOT DIAGNOSTIC for that run):
- **K1 state reproduction:** the diag values returned by this call (e_sum, src_sum, q_max, n_catch) match the run JSON's z0 snapshot: e_sum and q_max within 1e-3 relative, n_catch exactly, |src_sum - src_sum_JSON| <= 1e-6 e_sum.
- **K2 S0 null:** for S0 runs, max |delta_grav - delta| <= 1e-4 (1 + delta)_max.
- **K3 conservation:** Sum over the box of (rho_grav - rho_particles) equals 0 to 1e-6 relative (k = 0 dropped).

## Question A: internal consistency (framework-native)

### Candidate B's halo (the law's profile)

B (CFG515/516 round enclosed-mass rule RM) says that inside a bound host's census edge the total gravitating enclosed mass is the law's: M_law(<r) = r^2 g_law(r)/G, g_law = nu_mono(g_b/a0) g_b, g_b = G M_b,ret(<r)/r^2, with the phantom made of settled cold energy. Built from the run's OWN baryons:

- Retained baryons rho_b,ret = f_ret(x) f_b (1 + delta), with f_ret(x) the engine's own census map at z = 0 (1 for K1).
- All baryons rho_b,all = f_b (1 + delta). The engine keeps expelled baryons as gravitating mass (CFG518 convention), so the PRIMARY law total is **M_law = M_b,all(<r) + [nu(y) - 1] M_b,ret(<r)**, y = G M_b,ret(<r)/(r^2 a0). (Identical to nu M_b for K1.)
- Variant LAW-NOEXP (reported): M_b,ret + (nu - 1) M_b,ret (expelled baryons removed).
- Variant LAW-IN (reported, attribution only): the same law applied to the engine's MOND input, i.e. the retained baryons after the MIX-A pressure filter W(k) the engine uses (cool 0.28 at k_J(1e4 K), hot 0.54 at k_J(1e6 K), 0.18 unfiltered).
- a0 = the footing's a0 at a = 1 (flat). G and masses in physical units with h = 0.6736.

### Halo sample

- Field: the run's CIC density on the 256^3 mesh; candidate centres = 3^3 periodic local maxima, ordered by density.
- r_ON: the largest radius in the engine's grid Rg = geomspace(dx, 8, 14) Mpc/h at which the discrete-ball mean density (cells with centre distance <= R) is >= Delta_ta(z = 0) (from the run JSON).
- Deduplicate: a candidate within r_ON of a kept, denser candidate is dropped.
- Host: r_ON >= RMIN (2 cells). f_ret = engine fret_of(log M_ta(r_ON)) (1 for K1). Census edge r_e = x_supply(r_ON) r_ON (engine formula, the run's footing).
- **Scored halo:** host with r_e >= 1.5 cells. Keep the 100 densest scored halos per run.
- **Profile radii:** R in {1, 1.5, 2, 3, 4, 6, 8} cells; enclosed masses are discrete-ball sums (FFT ball convolution, cells with centre distance <= R) evaluated at the centre cell; the law uses r_eff = (3 N_cells / 4 pi)^(1/3) dx. Radii with r_eff <= r_e are **scored**; the rest are reported only.
- Every scored radius is also reported in units of r_M = sqrt(G M_b,ret(<r_e)/a0).

### Statistics

- **R(r) = M_grav(<r) / M_law(<r)** per scored (halo, radius); medians and 16/84 percentiles per radius. "Core" = R <= 2 cells.
- **Matched S0 halo:** the S0 density local maximum within +-2 cells (5^3 cube) of the run's centre; ball masses at that cell.
- **D_eng(r) = M_grav,run(<r) / M_S0(<r)** (engine gravitating vs S0 matter), **D_part(r)** the same with the run's particles, **D_law(r) = M_law(<r) / M_S0(<r)**.
- **Convergence:** median log10 R at shared physical radii (L50 R = 1, 2, 3, 4 cells = L25 R = 2, 4, 6, 8 cells; also L100 where present) over scored halos with log M_ta in [12.7, 14.3]; converged if |Delta| <= 0.1 dex between L50 and L25 at every shared scored radius with >= 10 halos in both.

### Verdict A (per footing: canonical = DC-can, alt = DC-alt; K1 reported alongside canonical), applied in order

Tolerance: |log10 R| <= 0.1 dex "matches the law".

1. **NOT DIAGNOSTIC** if any of K1-K3 fails for the footing's L50 or L25 census run or its S0, or if fewer than 20 scored halos exist in both L50 and L25.
2. **ENGINE ARTEFACT** if the median core R (R = 1, 1.5, 2 cells, pooled) is < 10^-0.1 in BOTH L50 and L25 (the engine removed mass from cores below what the law's own profile requires), OR if median core D_law >= 1 (the law needs no central deficit vs S0) while median core D_eng < 10^-0.05 in both boxes.
3. **LAW-REQUIRED** if the median R matches the law (|log10 R| <= 0.1) at every scored radius in both L50 and L25, the convergence test passes, AND median core D_law < 1 (the law's own halo is less centrally concentrated than S0's).
4. **MIXED** otherwise (e.g. the law requires a central deficit vs S0 but the engine's profile departs from the law by > 0.1 dex somewhere, in either direction, or the match is not converged).

L100 and L200 are reported for the trend; L200 is expected to have few or no scored halos (r_e < 1.5 cells) and is not gating.

### MUTATE (A)

- **M1 (physical):** NOCOMP (no compensation) through the same pipeline must show the opposite mismatch relative to the census run: median core R(NOCOMP) > median core R(DC-can) in both L50 and L25. If not, the test has no teeth and A is downgraded to NOT DIAGNOSTIC.
- **M2 (emptied core):** in the DC-can L50 and L25 gravitating fields, set rho_grav = 0 in all cells within 1.5 cells of each scored centre and re-run the verdict. It must return ENGINE ARTEFACT. `CFG526_MUTATE=1` writes `_MUTATE` outputs; exit code 1 = detected.

## Question B: against data

### Framework prediction used

- r(k, z) = P_run/P_S0 (particles) from the run JSONs at z = 0.5 (PRIMARY; near the effective redshift of cosmic shear, PROVISIONAL) and z = 0, at k = 1, 2, 4 h/Mpc (nearest bin), for L100 / L50 / L25 (DC-can; DC-alt where run).
- Lensing tracer variant: r_grav(k, z = 0) = P(delta_grav)/P_S0 from the A pipeline (z = 0 only, since only z = 0 positions are saved).
- Linear power P_L(k, z) = engine P_lin0(k) (D(a)/D(1))^2; nonlinear P_NL = the matched S0 box P at that k and z.

### Literature (recalled, all PROVISIONAL; nothing downloaded)

- Amon & Efstathiou 2022 (MNRAS 516, 5355), KiDS-1000 cosmic shear with Planck LCDM: P_m = P_L + A_mod (P_NL - P_L), **A_mod = 0.858 +- 0.052**.
- Preston, Amon & Efstathiou 2023 (MNRAS 525, 5554), DES Y3 cosmic shear: **A_mod = 0.82 +- 0.04**.
- Both are conditional on Planck LCDM's linear amplitude; with a lower-S8 cosmology no suppression is needed. The S0 ICs are Planck-normalised (sigma8 = 0.811), so the mapping is like-for-like.
- Hydrodynamic feedback F(k) = P_hydro/P_DMO at z ~ 0-0.5 (van Daalen+2020 MNRAS 491, 2424; BAHAMAS; FLAMINGO; OWLS), PROVISIONAL bands: fiducial/weak F(1) in [0.90, 0.98], F(2) in [0.85, 0.95], F(4) in [0.80, 0.92]; strong extreme F(1) 0.82, F(2) 0.76, F(4) 0.72. The PM has no feedback, and keeps expelled baryons as gravitating mass, so the framework total is taken as r F.
- Lyman-alpha forest small-scale power (z ~ 2-5): the boxes have no snapshot at z >= 2; Lya is NOT DIAGNOSTIC here unless r(z = 1, k <= 4) < 0.90, in which case a high-z snapshot run is listed as needed.

### Statistic

A_eq(k) = (r F P_NL - P_L)/(P_NL - P_L); A_eff = mean of A_eq over k = 1, 2, 4. Pulls z_d = (A_eff - A_mod,d)/sigma_d for each dataset d. Computed for F = 1 (no feedback) and F = fiducial band ends; for LCDM itself r = 1.

### Convergence and conservative bound

- r is converged at k if |r_L50 - r_L25| <= 0.05 and |r_L100 - r_L50| <= 0.05.
- Exclusion uses the conservative (least suppressed) estimate: if r deepens monotonically with resolution at that k (r_L100 >= r_L50 >= r_L25 within 0.02), the finest box (L25) bounds the converged value from above and is used; otherwise the maximum over boxes is used.

### Verdict B (per footing), applied in order

1. **EXCLUDED (with sigma)** if, with F = 1 and the conservative r, z_d < -3 for BOTH datasets.
2. **NOT DIAGNOSTIC** if r is not converged at any of k = 1, 2, 4 (the converged prediction may be deeper; "allowed" cannot be claimed), or if the z = 0 lensing-tracer variant moves A_eff by more than 0.04 (one sigma of the tighter dataset) from the particle value.
3. **PREFERRED-HINT** if converged, framework with fiducial feedback has |z_d| <= 1 in both datasets while LCDM with the same fiducial feedback has |z_d| > 2 in both. (Never stated as "the data favour the framework".)
4. **ALLOWED** if converged and framework with F somewhere in the fiducial band gives |z_d| <= 2 in at least one dataset.
5. **NOT DIAGNOSTIC** otherwise.

If B is NOT DIAGNOSTIC, the README lists what would decide it (public shear data vectors / covariances, suppression posteriors, Lya P1D tables) with approximate sizes, and nothing is downloaded without the owner's go.

### MUTATE (B)

r -> 0.5 r at k >= 1 for the L50 / L25 DC-can runs must return EXCLUDED; r = 1 (LCDM) must not.

## Outputs

`cfg526_profiles.py` (A) -> `cfg526_profiles.out`, `cfg526_profiles.json`; `CFG526_MUTATE=1` -> `_MUTATE` versions. `cfg526_data.py` (B) -> `cfg526_data.out`, `cfg526_data.json` (+ `_MUTATE`). `cfg526_results.json` collects both verdicts. Arrays (if any) to `_external_data/cfg526_work`. Numbers in the README come from the JSONs.
