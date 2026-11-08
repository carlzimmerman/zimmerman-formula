# BG1: cold-gas conversion key for the K(Q) dust component. FAIL / FAIL (canonical / alt)

Kappa = 1/2 FITTED; not theory closed. TEST lane (owner decision closure_2026_11_08/OWNER_DECISION_2026-11-08_BG1_LAUNCH.md);
adopts nothing. Cold dark energy, never dark matter; no particle. Both footings graded separately, never pooled.

- Criteria: FROZEN_CRITERIA.md (d5b23bf2d4), committed alone before any number. Brief: ../BG1_BRIEF_2026_11_08.md.
- Scripts: bg1.py (`expo`: exposures and G1-G7 on the alpha grid; `cosmic`: dark ages, neutral IGM, galaxy-hosted cold gas,
  G8-G10 with the QX3 growth ODE and GL1's corrected kernel), bg1_grade.py (label, tables, MUTATE). One thread; expo 4 s,
  cosmic 36 s per run; peak RSS 0.32 GB; SIGTERM checkpoints. Outputs bg1.json / bg1.out, bg1_MUTATE.json / bg1_MUTATE.out,
  parts/ (expo, expo_x10, expo_hot, expo_m3, cosmic, cosmic_x10), run_*.txt. Criteria hash in every output.
- Read-only use of QX8 (SPARC exact-field parts), GB1 (battery loaders and gate formulae), QX5 (X-COP, groups, lensing
  loaders), QX3 iter2 (growth, PR4 lensing), CE2 (fsigma8 statistic), F1A, KD1, QX15, ST1, DX1, AM1, U1/UX5, X1, S1, LW1.

## Label: FAIL on canonical, FAIL on alt. No alpha in [1e-3, 1e3] passes G1-G10 on either footing.

Reading (three lines):
1. The key does what the brief asked at the galaxy scale: at alpha near 1e3 (M_sun pc^-3 Gyr)^-1 the SPARC discs (G1, G1b),
   the KiDS isolated lenses (G2), the ellipticals (G7) and, on canonical only and at the line, the dSph pair (G6) all pass,
   because cold dense discs convert their dust (retained 0.4 %) while quenched hosts keep 17-36 % of theirs.
2. The same rate converts the component where the baryons were densest and coldest of all: the neutral mean-density gas of
   the dark ages (7 M_sun pc^-3 at z 1000). The dark-ages exposure E = 3.57e-3 M_sun pc^-3 Gyr is 1/7 of a SPARC disc's, so
   G9 (converted fraction by z 20 <= 0.01) holds only for alpha <= 2.5, the forest and growth gates (G8, G10) only for
   alpha <= 6.3, and the disc window (alpha >= 1000 canonical, beyond the scan on alt) sits 400 times higher. The two windows
   are disjoint, and the ratio is scale-free (the x10 replay moves both alike).
3. Independently of alpha, three hot rows fail at every grid point: Coma UDGs (G5, under-filled by 0.65-0.92 dex at any
   retention, the pre-launch kill), the groups (G4, at most 7/20 and 6/20) and X-COP (G3, over-filled by 0.06-0.10 dex at the
   CMB amount R = 5.41; it would pass at KD1's captured share f_cap R = 4.11, reported). Clusters keep >= 94 % of their dust
   under this key because the ICM is hot, so no alpha can move them.

## Exposures (M_sun pc^-3 Gyr), the frozen model's numbers

| Quantity | canonical | alt |
|---|---|---|
| SPARC disc, M_b-weighted median over 175 galaxies (at 2.2 h: median) | 0.0256 (0.0168) | same (footing-free) |
| <G> gas-history factor median; disc age (lookback to z 2) | 1.54; 10.52 Gyr | 1.54; 10.52 Gyr |
| dark ages z 20-1100, mean density neutral (z 20-800 reported) | 3.571e-3 (2.261e-3) | 3.570e-3 (2.260e-3) |
| neutral mean-density IGM z 6-20 | 8.3e-6 | 8.3e-6 |
| galaxy-hosted cold gas, cosmic mean parcel z 0-20 (z 2-20) | 8.7e-4 (3.4e-4) | 8.7e-4 (3.4e-4) |
| disc / dark-ages ratio | 7.2 | 7.2 |
| amount: R = omega_X/omega_b (F1A R_B2); f_cap R reported | 5.4096; 4.1110 | 5.4123; 4.1121 |

Member (stellar) share of the X-COP baryons at the outermost graded radius, the input of MB1's sums: 0.041-0.077 per cluster,
so a cluster keeps 1 - s_mem (1 - f_gal) >= 0.94 at any alpha. Coma UDGs (4 Gyr gas-rich phase) keep 1.00 -> 0.62 over the
scan; LG field dwarfs (3 Gyr) 1.00 -> 0.17; bright M31 dwarfs (4 Gyr) 1.00 -> 0.36; ellipticals (2 Gyr) 1.00 -> 0.02.

## Gate x footing at the best alpha (most cells passed; ties broken by summed normalised miss)

Canonical: best alpha 1000 (5 of 11 cells). Alt: best alpha 0.126 (4 of 11 cells; 22 low alphas tie, the cosmic gates
and the HX1 reading of G7 pass there and nothing else does).

| Gate | canonical at alpha 1000 | alt at alpha 0.126 |
|---|---|---|
| G1 SPARC (rms <= law + 0.010; \|mean\| <= 0.05) | **PASS** rms 0.0626 (line 0.0660), mean -0.003, disc retained 0.004 | FAIL rms 0.394 (line 0.0658), mean -0.374, retained 0.997 |
| G1b gas-rich low-density discs (107 of 175, Sigma_cold(2.2 h) < 10) | **PASS** rms 0.0660 (line 0.0673), mean -0.003 | FAIL rms 0.367 (line 0.0665) |
| G2 KiDS isolated lenses (\|shift\| <= 0.05) | **PASS** -0.003 dex | FAIL -0.416 dex |
| G3 X-COP (\|mean\| <= 0.05, rms <= 0.10; c in [2, 10]) | FAIL c 2: -0.060, 0.092 (retained 0.941; at f_cap R: +0.010, 0.069) | FAIL c 2: -0.099, 0.120 (at f_cap R: -0.029, 0.073) |
| G4 groups (>= 16/20 at f* 0 and f* 1) | FAIL 7/20, 6/20 | FAIL 7/20, 0/20 |
| G5 Coma UDGs (\|mean\| <= 2 sigma_U) | FAIL +0.782 (+2.98 sigma_U), retained 0.62 | FAIL +0.648 (+2.47 sigma_U), retained 1.00 |
| G6 LG field (\|mean - anchor\| <= 0.10); bright M31 equilibrium subset (within 2 sigma = 0.176 of ST1's +0.214 / +0.201) | **PASS** LG -0.096 (retained 0.17); M31 +0.016 (retained 0.36) | FAIL LG +0.131; M31 +0.337 |
| G7 ellipticals (IMF reading f_ret <= 0.1, or HX1 reading f_ret >= 0.9) | **PASS** retained 0.018 (IMF reading; GB1 G4 mean with IMF +0.062) | **PASS** retained 0.905 (HX1 reading; GB1 G4 mean -0.432) |
| G8 forest, f_conv(z 2) <= 0.03 | FAIL 0.980 | **PASS** 0.0005 |
| G9 dark ages, f_conv(z 20) <= 0.01 | FAIL 0.972 | **PASS** 0.0004 |
| G10 growth: PR4 lensing Delta chi^2 <= 4 and DESI fsigma8 within 2 sigma | FAIL Delta chi^2 81.8; Rf 0.000 | **PASS** 0.00; Rf 0.998 |

The alpha window per gate (grid points passing), canonical / alt:
G1 {1000} / none; G1b {1000} / none; G2 [251, 1000] / same; G3 none / none; G4 none / none; G5 none / none;
G6 [10, 50] and {1000} / [7.9, 40]; G7 [1e-3, 0.126] and [79, 1000] / same; G8 [1e-3, 6.3] / same; G9 [1e-3, 2.5] / same;
G10 [1e-3, 6.3] / same. Intersection: empty on both footings.

## The killing gates, with numbers

- **Every alpha, both footings:** G5 Coma UDGs (+0.65 to +0.92 dex, 2.5-3.5 sigma_U; the component at full retention gives
  b = 6.4 where the UDGs need about 80, and conversion only lowers it), G4 groups (7/20 at f* 0 at best, 0-6/20 at f* 1),
  G3 X-COP at the frozen amount (-0.060 to -0.077 canonical, -0.083 to -0.099 alt; the line is 0.05; retained >= 0.94 at
  any alpha). On alt G1 also fails at every alpha (G1b rms 0.0679 against 0.0665 at alpha 1000; discs clear just beyond the
  scan).
- **Disjoint windows:** G1 needs alpha >= 1000 (canonical; alt > 1000), G9 needs alpha <= 2.5, G8 and G10 need alpha <= 6.3.
  Ratio 400 on canonical. With the z 20-800 dark-ages reading (neutral fraction 1 only after z 800) G9 would allow alpha <= 4.0
  and the ratio would be 250. At alpha 1000 the converted fraction by z 20 is 97 %, which removes the clustering component the
  CMB lensing and fsigma8 need (Delta chi^2 82, Rf 0.00).

## Expected kills (brief), as they fired

| Kill named before launch | canonical | alt |
|---|---|---|
| Coma UDGs | FIRES at every alpha: +0.689 to +0.782 (+2.63 to +2.98 sigma_U); retained 1.00 -> 0.62 | FIRES at every alpha: +0.648 to +0.740 (+2.47 to +2.82) |
| LG field vs bright M31 dSph pulling opposite ways | fires at 52/61 alphas: LG field over-filled from alpha 63 to 794 (-0.10 to -0.14) while M31 passes; at alpha 1000 LG field sits 0.004 inside the 0.10 line (-0.096, retained 0.17) and M31 at +0.016 (retained 0.36): G6 PASS at the last grid point only | fires at 53/61 alphas and at alpha 1000 (LG field -0.105): the pair is never jointly inside above alpha 40 |
| gas-rich LSB discs retain (G1b) | fires at 60/61 alphas; at alpha 794 G1 passes while G1b fails (rms 0.0685 vs 0.0673); at 1000 both pass | fires at every alpha |

Both dSph classes pass at alpha 10-50 on both footings, but there the pass is relative to a SPARC anchor that is itself
still half-filled (retained 0.4-0.8); the discs fail there by 0.1-0.2 dex.

## Known answers (all PASS) and MUTATE

| Check | canonical | alt |
|---|---|---|
| KA1 law-only (f_ret 0) reproduces GB1 L0: SPARC Z/rms, X-COP mean/rms, ellipticals, UDGs, groups | \|d\| 0 | 0 |
| KA2 law-only QX8 SPARC rms and median U (0.056047, 0.58 / 0.055826, 0.52) | 0 | 0 |
| KA3 uniform-b at f_cap R reproduces DX1 O1: X-COP +0.004083/0.08200, ellipticals -0.36802, UDGs +0.74322 | \|d\| <= 1e-6 | same (-0.0201/0.0855, -0.3788, +0.7021) |
| KA4 dark-ages integral vs matter-era closed form (ratio, radiation lowers it) | 0.917 | 0.917 |
| KA5 growth identity: f_conv 0 gives Rf 1 and Delta chi^2 0 (baseline chi^2 8.560) | 0 | 0 |
| M1 catalyst -> T > 1e6 K gas (ICM, IGrM, primordial plasma z 3.7e5-3.7e8; E_plasma 3438, E_ICM 4e-4): G3 must FAIL at every alpha | FAIL at every alpha (cluster retained 0.03 at 1e-3, 0 above; X-COP back to +0.467) -> **BITES** | same (+0.435) -> **BITES** |
| M2 alpha -> 0: must FAIL G1 and G2 | G1 rms 0.405 (line 0.066), G2 shift -0.421 -> **BITES** | 0.421, -0.419 -> **BITES** |
| M3 alpha -> 10 x best alpha: must flip G5 or G6 | 1000 -> 10000: G5 FAIL -> FAIL (+0.78 -> +0.92), G6 PASS -> PASS (LG -0.096 -> -0.003; M31 +0.016 -> +0.132 inside 0.176) -> **NO BITE** | 0.126 -> 1.26: nothing moves -> **NO BITE** |
| M3' (reported, post-freeze): 10 x the first alpha at which G6 passes | 10 -> 100: G6 PASS -> FAIL (LG +0.009 -> -0.124) -> flips | 7.9 -> 79: PASS -> FAIL -> flips |
| KA replay, exposure x10 (criteria hash in every output): must flip a gate | 106 cell flips over G1, G1b, G2, G6, G7, G8, G9, G10; x10 label window still empty | same |

M3 as frozen has no power at the best alpha: G5 cannot flip in the clearing direction (the UDGs are under-filled at any
retention), and between alpha 1000 and 10000 both dSph classes stay inside their lines (the ST1 line on bright M31 is 0.176
wide). The dSph row's power to alpha is shown by M3' and by the grid itself (G6 fails below alpha 8 and between 63 and 794).
The label does not rest on M3: it rests on G3, G4, G5 failing at every alpha and on the G1 / G9 disjunction.

## Decisions taken inside the frozen model (declared; none tuned to a result)

1. Geometry identity: E(r) = N_cross 2 Sigma / v_z with N_cross = t / T_orbit, T_orbit = 2 pi r / v_orb, v_z = v_orb / sqrt(3)
   gives E(r) = sqrt(3) t <Sigma_cold(r)>_t / (pi r), independent of the orbital speed; the same for dispersion hosts.
2. SPARC Sigma_HI x 1.33 from Vgas by the spherical derivative Sigma = (dM/dr) / (2 pi r), M = Vgas^2 r / G (the HI column
   product is not on disk; SPARC's Vgas already carries the 1.33). H2: no SPARC-specific H2 rule exists on record; the
   record's H2 rule is the Milky Way gas model of U1 N6 / UX5 (Sigma_H2(8.33 kpc) = 2.0 against Sigma_* 43.6 M_sun pc^-2),
   applied here as H2 = 0.0459 x (0.5 SBdisk + 0.7 SBbul). M_H2/M_HI median 0.044.
3. Disc age = lookback time to z 2 on the footing background (QX15 fit through CLASS), 10.52 Gyr; <G> = 1 + M_*/(2 M_gas(0))
   with M_* = 0.5 L_[3.6], M_gas(0) >= 0.02 M_* (floor for the gas-poor few). Quenched hosts: <M_gas> = M_*/2 in an exponential
   gas disc of scale r_half/1.678 over the frozen phase length; f_ret is the mass-weighted mean of exp(-alpha E(r)).
4. Amount: the criteria's "omega_X 0.108" is CMB1's expansion-only decomposition; the dust phase carries F1A's R = 5.41
   (the mechanism paragraph's "5.41 x baryons"), used for the label; f_cap R = 4.11 reported.
5. Profiles: galaxy classes in the record's uniform-b convention (b = 1 + R f_ret, the dust with the baryons; the DX1/KD1
   diagnostic the class needs were derived in), with the SPARC b(r) = 1 + R fbar(<r) from the M_b-weighted enclosed
   retention and the KiDS lens dust at the disc-weighted retention of the SPARC galaxies within 0.3 dex of the bin's stellar
   mass. X-COP and groups: cold-collapse (Hernquist) profile, a = R500/c, c in [2, 10] a reported nuisance (none passes).
   Under an extended-halo reading the dust at KiDS radii would never cross a disc and G2 would fail at every alpha.
6. Cosmic galaxy-hosted term: GAMA baryonic mass function (AM1 am1_bmf.json, "all"), SPARC's own relations (log M_cold =
   4.30 + 0.533 log M_*; log R_d = -2.07 + 0.254 log M_*; log R_HI = -3.75 + 0.524 log M_HI), cold gas scaled by the raw
   Omega_HI(z) table (ALFALFA, MgII-DLA, SDSS DLA, Gemini; transcribed, PROVISIONAL under the record's look-up rule) plus the
   CO-based rho_H2(z) fit as CFG632 transcribed it. It is 24 % of the dark-ages exposure and moves no label.
7. Dark ages: full rho_b from z 1100, as frozen (neutral fraction 1); the z 20-800 reading is reported (63 % of it).
8. G6 bright M31 uses ST1's equilibrium subset (And I, XVII, XIX, XXV dropped; 21 systems) and ST1's step +0.214 / +0.201
   with 2 sigma = 0.176 from its 95 % CI; LG field uses the mean residual minus the SPARC anchor (median reported).
9. Member share for clusters from the X-COP stellar-mass profiles (the quantity MB1 summed); for groups the GB1 f* = 1
   allowance puts half the baryons in members (f* = 0: none).
10. G10 uses GL1's corrected kernel (n = 4) and CE2's DESI DR1 fsigma8 statistic; the converted fraction is removed from the
    clustering source and density in QX3 iter2's ODE with the total background unchanged (density conserved).

## Limits

Static exposure model; no orbits are integrated and the gas discs are today's (past discs were smaller, which would raise the
disc exposure and lower the ratio to the dark ages, but by factors of order unity, not 400). The quenched-host geometry is a
declared idealisation. The cosmic galaxy term rests on transcribed cold-gas densities. The Bullet is not graded (no gate).
Nothing here says the data favour the framework. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
