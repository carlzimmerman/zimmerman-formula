# CQ1_screening_window: FROZEN CRITERIA (written and committed before any script or number)

κ = ½ FITTED; not theory closed. Footings never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s².
No particle, no cold sector, no ΛCDM input. Nothing here can say the data favour the framework. No download.

## Question
Can ONE new screening constant screen the Solar System and leave galaxies unscreened?
Three families, one constant each:
- (i) a local tidal threshold T★: screened where T ≥ T★, T = largest |eigenvalue| of the Newtonian baryonic tidal tensor (system + host);
- (ii) a Vainshtein-type radius r_V = (r_s ℓ²)^(1/3), r_s = 2GM/c²: screened where 2GM(<r)/r³ ≥ T_V ≡ c²/ℓ²;
- (iii) a fixed screening length L★: screened within L★ of each mass.
For a point mass (i) and (ii) give the same sphere, r = (2GM/T)^(1/3); they differ only for extended bodies.

## Part A (a bound)
List every s⁻² quantity built from {c, G, ρ_Λ, a0}. Mass balance forces G and ρ_Λ to enter as Gρ_Λ, so the set is
(Gρ_Λ)^p (a0/c)^(2−2p) × pure numbers. ρ_Λ is framework-native, ρ_Λ = a0²/(κ²c²G) (no Planck, no ΛCDM background).
Print Gρ_Λ, (a0/c)², 8πGρ_Λ, and the product for natural pure numbers N in [1e-3, 1e3], per footing, against:
the Sun's tide 2GM☉/r³ at its saddle r_sad = (GM☉/g_N,e)^½ (g_N,e from CW1's inversion of 2.32e-10 and 1.9e-10),
the MW midplane tide 4πGρ_b(R0, 0), and the outskirts scale a0/r at r = 10 kpc. Label: VACUUM SCALE IN GAP / NOT IN GAP.
The hand estimate Gρ_Λ ≈ 4e-37 s⁻² is VERIFIED if the computed value is within a factor 2 on each footing.

## Part B gates (record numbers only)
- **G1 Cassini.** CW1's `Solver` (plain QUMOND, form "PQ"), η from 2.32e-10 inverted, ceiling 5.2e-27 s⁻² (CW1's CEIL).
  `cw1_copy.py` is a byte copy of `cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4/cw1.py`, never edited, never run. `cq1.py`
  reads the Solver source from it and adds ONE option, `rscr` (units r_M): F_r = F_θ = 0 at nodes x < rscr, applied right
  after F is built. Scan rscr on the solver's own nodes. x_s,min = the smallest node such that q ≤ ceiling there and at every
  larger node. The upper set must be contiguous; if not, print it and use the contiguous end. Converted to AU with r_M☉.
- **G2 Planets (CZ3).** CW1's `planets()` (CZ3 / AZ12 verbatim) on the screened solver. Pass: worst Z ≤ 2. Report Z at
  x_s,min and the smallest rscr on a scan near Saturn's aphelion that passes all six (a lower bound on r_screen,☉).
- **G3 Outer globulars (D10).** (iii) L★ ≥ 21.68 (canonical) / 22.85 (alt) pc, D10's central floor. (i) and (ii): Pal 4 and
  Pal 14 (D10's binding pair) must be screened at r = a, D10's Plummer a = r_h,l, M = 1.6 L_V (D10's P1 central Υ_V), host
  tide 2G·6e10 M☉/R_GC³ added (D10's MW_Mb). Plummer: T(a) = GM/(2^1.5 a³) (tangential eigenvalue, the larger),
  2GM(<a)/a³ = 2GM/(2^1.5 a³). Screened at the centre (GM/a³, 2GM/a³) is reported as a looser variant, not the label.
  NGC 2419 and Pal 3 are reported only.
- **G4 Dwarfs.** CZ5's 24 (its selection, verbatim). Plummer a = r_h, M = Υ L_V + 1.33 M_HI at Υ = 3 (top of CZ5's grid;
  the tide rises with M, so this covers the whole grid). Υ = 2 is reported. All 24 must be unscreened at r = a:
  (i) T(a) + 2G·7e10 M☉/D³ (MW satellites only, as CZ5's E1) < T★; (ii) 2GM(<a)/a³ < T_V; (iii) L★ < a.
- **G5 MW midplane at R0 = 8.122 kpc.** (i) T★ > 4πGρ_b(R0, 0) with the largest record value, 0.1599 M☉/pc³ (CZ4's graded
  B2b); McMillan 0.1071 is reported. (ii) T_V > 2g_N/R0 (spherical-equivalent enclosed mass, g_N from CW1's inversion of
  1.9e-10 per footing); the total M_b = 7e10 M☉ (CZ5's M_MW) is reported. (iii) L★ < 90 pc, the H2 layer's sech² scale,
  the thinnest baryonic layer in the record's MW model (KT29). L★ < R0 is reported.
- **G6 SPARC.** KT19's sample and loader (verbatim), M_b = 0.5 L[3.6] + 1.33 M_HI, r_M = (G M_b / a0)^½. Line: the
  point-mass screening radius r_screen ≤ 0.1 r_M for every galaxy ("≪" frozen as one decade). r_screen ≤ r_M (outskirts
  alone) is reported, not the label.
- **G7 Wide binaries, report only.** At each window end (or, with no window, at the Cassini end), the screening radius of a
  1 and 2 M☉ binary against s = 1–30 kAU. SCREENS (r_screen ≥ 30 kAU) / PARTLY / DOES NOT (< 1 kAU).

## Labels
Per family and footing: **WINDOW [lo, hi]** if the largest lower bound is below the smallest upper bound over G1–G6;
otherwise **NO WINDOW**, naming the binding pair. Also printed: the window without G3 (information only), and whether
any vacuum combination with N in [1e-3, 1e3] lies inside a window (WINDOW CONTAINS A VACUUM SCALE / DOES NOT).

## Checks
- K0: `cw1_copy.py` SHA-256 equals CW1's `cw1.py`; the patch adds exactly one line.
- K1 (known answer): the copy at rscr = 0 reproduces cw1.json's K3 Cassini (HALF, LOC1, both footings), rel ≤ 1e-6.
- K2 (known answer): at rscr = 0, form PQ, the patched copy gives the same q as CW1's unpatched Solver source, rel ≤ 1e-12
  (CW1's plain-QUMOND Q2). AX1's plain QUMOND range 1.69–5.18× is printed for comparison only.
- K3: direct screened solves at 8 radii equal the plain solve's tail integral, rel ≤ 1e-9.
- K4: x_s,min at per_dec 400, L 96, n_μ 128 within 3 % of the default.
- K5: peak RSS < 1 GB.
- MUTATE twin `--mutate`: ν ≡ 1 (CW1's own MUTATE branch). F ≡ 0, so K1 must fail. Outputs go to `cq1_MUTATE.*`.

## Expectation (written before any number)
(i) and (ii): NO WINDOW. A mass-scaled screen sets r_screen/r_M ∝ M^(−1/6). To screen Pal 14 out to r_h (several r_M), it
would also screen small SPARC galaxies near r_M. Without G3, a window is expected between the SPARC line and Cassini.
(iii): a narrow window, or none, between D10's floor and the smallest SPARC 0.1 r_M. No vacuum scale is expected in any window.

Run: `OMP_NUM_THREADS=1 nice -n 10 python3 -I -B cq1.py [--mutate]`; single thread, < 1 GB, minutes.
