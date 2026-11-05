# FA1 FROZEN CRITERIA: first gate for I1, the tidal-isotropy selector

Committed alone, before any script or number for this gate. Not blind: Phase 1
hand estimates (rho ~ r^-2 cluster gas gives zeta ~ 1/3; concentrated spirals
zeta ~ 0.03; gas-rich dwarfs zeta up to ~ 0.3) were written before this, and the
record's KT30 midplane lesson was read in Phase 2. kappa = 1/2 FITTED. Footings
never pooled. Adopts nothing. The cold sector stays retired; this gate grades a
selector on baryon data only and reinstates nothing.

## The selector
zeta = 1 / (1 + (3/sqrt 6) ||T_TF|| / tr T), T_ij = d_i d_j Phi_b, the baryons'
Newtonian tidal tensor (the Newtonian limit of the Weyl-electric over Ricci
ratio). For a spherical baryon distribution this is exactly
zeta = rho_b(r) / rho_bar_b(<r) = (d ln M_b / d ln r) / 3.
zeta = 1 in FRW and at a cored centre, 1/3 for rho ~ r^-2, 0 in vacuum.
The dust part's weight is F(zeta), F non-decreasing, F(0) = 0. No form of F is
assumed: the gate asks whether ANY such F can give clusters their dust and
SPARC none.

## Readings
- **Reading A (primary, graded):** spherical-equivalent zeta_A =
  (d ln M_b / d ln r)/3. SPARC: M_b(r) = r V_b^2 / G with
  V_b^2 = Vgas|Vgas| + Y Vdisk^2 + 1.4 Y Vbul^2 (CRG1's convention), Y = 0.5
  primary, 0.3 and 0.7 as variants; derivative by np.gradient in ln r on the
  tabulated radii; points with M_b <= 0 or non-monotone sign issues dropped and
  counted. X-COP: M_b = M_gas + M_star from the same FITS files and radii RQ3
  uses (x = 0.1, 0.2, 0.3, 0.5, 0.7 R500), derivative by central log difference
  at r x 1.1^{+-1}, log-interpolated.
- **Reading B (reported, analytic):** the full tidal tensor at a thin disc's
  midplane, where the vertical term dominates, gives zeta_B = 1/2 exactly. It is
  compared with zeta_c only; its effect size needs a 3D dust model and is NOT
  COMPUTED.

## Gates
- **zeta_c** = 5th percentile of zeta_A over X-COP rows (dust must weigh in at
  least 95 % of the rows that need it: RQ3's deficit Q_bracket 2.1-5.7 x gas).
- **G-SEP (graded, per footing).** Sample: SPARC points with g_b < a0 at Y = 0.5
  (g_b on the footing's a0: canonical 9.3603e-11, alt 1.1312e-10). f_SP =
  fraction of those points with zeta_A >= zeta_c. Any F that gives X-COP its
  dust gives those points at least the same weight. Line from real errors:
  cluster-level dust is at least 1.5 x the law's mass (requirement sheet),
  i.e. +0.40 dex in g; SPARC's acceptance line is rms <= 0.110 dex against the
  law's 0.069 (RQ3 A1), so the room is f_max = (0.110^2 - 0.069^2) / 0.40^2
  = 0.046.
  - SEPARATES: f_SP <= 0.046 at Y 0.5, 0.3 and 0.7.
  - DOES NOT SEPARATE: f_SP > 0.046 at all three Y.
  - UNDECIDED: otherwise.
- **G-BUL (reported with a label, sigma none).** zeta from UX6's Plummer baryon
  model (gas and galaxies, z = 0 plane) at BCG1, BCG3 (where the lensing mass
  sits) and the two gas peaks, point value and mean over a 100 kpc disc.
  WEIGHT ALLOWED AT GALAXIES if zeta >= zeta_c at both BCGs (point value);
  WRONG SIGN if zeta < zeta_c at either BCG while zeta >= zeta_c at that
  subcluster's gas peak; otherwise NO SIGN. The selector does not move the dust;
  this asks only whether it lets the dust weigh where Clowe's peaks are.
- **G-Q2.** zeta at Saturn's orbit (Sun as point mass, local disc density
  0.1 Msun/pc^3 added to the trace) must be below zeta_c, so the dust part adds
  nothing there. Label INHERITS: Q2 then rests on the MOND part (v3s L*), which
  this gate does not grade.
- **G-KEYS: NOT COMPUTED.** The 15 shear keys' gas profiles live inside the X30
  machinery reached through LW1/SL1 drivers; selector-level zeta is not wired
  there. Disclosed, not graded.

## Checks (a failed check means no clean label)
- **K0 known answer:** the candidate g = law(g_b) + F(zeta) g_dust with F = 0
  equals law(g_b) to 1e-12 on RQ3's is_law probe grid.
- **K1 code:** zeta from the Plummer Hessian equals the analytic spherical
  (d ln M / d ln r)/3 of the same Plummer at 6 radii to 1e-6; uniform sphere
  gives 1, a point mass at large r gives < 1e-6, rho ~ r^-2 gives 1/3 to 1e-3
  on a tabulated profile through the same finite-difference code used for
  SPARC and X-COP.
- **MUTATE twin (must bite):** SPARC zeta_A x 0.1 must turn G-SEP into
  SEPARATES on both footings.
- **Rerun:** the result JSON from two runs must be byte-identical.

## Labels for the lane
- I1 KILLED AT GATE 1 if G-SEP reads DOES NOT SEPARATE on both footings and all
  checks pass.
- I1 ALIVE AT GATE 1 if G-SEP reads SEPARATES on both footings, G-BUL is not
  WRONG SIGN, and all checks pass. Alive means only that a necessary condition
  holds.
- FOOTING-SPLIT or UNDECIDED otherwise.

Compute: one thread, nice 19, < 1 GB, seconds. No downloads.
kappa = 1/2 FITTED; not theory closed.
