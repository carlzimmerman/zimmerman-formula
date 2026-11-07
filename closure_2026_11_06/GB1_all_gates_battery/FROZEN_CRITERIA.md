# GB1 frozen criteria: one all-gates battery, and every live candidate graded through it

Frozen before any GB1 script or GB1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No
dark-matter particle of any kind. Both footings, never pooled. No new data and no downloads: every input is already on
disk and named below with its source. Compute: one thread, under 1 GB, minutes.

Footings (each graded separately; "passes" needs both):
- canonical: a0 = 9.3603e-11 m/s^2 (QX5's 9.360324825027975e-11), Lstar = 21.7 pc;
- alt: a0 = 1.1312e-10 m/s^2 (QX5's 1.1312035414413022e-10), Lstar = 22.9 pc.

## 1. Candidate interface

A candidate is a fixed function of per-point PHYSICAL features. It never sees a class label (the class name, the
sample a point came from, or a per-class constant). It returns either
- a baryon-mass factor b >= 0 and a phantom multiplier F >= 0, giving g_pred = b g_N + F [g_law(b g_N) - b g_N], or
- an additive offset T (dex) on top of that, or
- a direct offset Delta (dex) (the L2 reference only).
Its prediction is Delta = log10(g_pred / g_law(g_N)) + T, the predicted log offset from the plain law at that point.
At fixed radius a mass ratio equals the acceleration ratio, so the same Delta applies to M_obs/M_law.

**Features** (per point; None where the data do not carry it):

| Feature | SPARC | ellipticals | X-COP | groups | Coma UDGs | dSphs | KiDS bins | Solar System |
|---|---|---|---|---|---|---|---|---|
| x = g_N/a0 | yes | yes | yes | yes | yes (G M*/2 / r_h^2, QX20) | yes (inverted, below) | yes (g_bar) | yes |
| M_b, r, r/r_M | yes | yes | yes | yes | yes (QX20) | M*, r_h | r = R_med | yes |
| v_obs (circular) / sigma (dispersion) | V / None | sqrt(GM/r) / sigma_e | sqrt(GM/r) / None | sqrt(GM/r) / None (gas kT only) | sigma / sigma | sigma / sigma | sqrt(g_obs R_med) / None | Kepler v / None |
| f_gas | yes | 0 (hot gas not modelled, QX18) | yes | 1/(1+f*) | 0 | None | None | 0 |
| f_sp (photometric-star share of M_b) | disc and bulge shares | 1 | 1 - f_gas | f*/(1+f*) (an allowance) | 1 | 1 | 1 (lens M* photometric) | 0 (GM_sun is dynamical) |
| Salpeter/Kroupa M/L ratio | 1/0.63 | us/uk per galaxy (Humphrey table) | 1/0.63 | 1/0.63 | 1/0.63 | 1/0.63 | 1/0.63 | n/a |
| depth Phi/c^2 | QX20 V6 | QX20 V6 | QX20 V6 | QX20 V6 | None | None | None | None |
| x_e | None | None | None | None | S1 x_e_dmean | LW1 xe | None | None |
| exact-field geometry T_geom | QX8 parts, U = 0.50 | 0 (spherical) | 0 (spherical) | 0 (spherical) | 0 (base is already the action) | 0 (spherical model) | 0 (R_med >= 0.1 Mpc, monopole) | 0 (spherical Sun) |
| assembly redshift z_f | None | None | None | None | None | None | None | None |

- Elliptical sigma_e = 0.87 sigma_0, sigma_0 the HyperLEDA values transcribed in QX26 (qx26.py SIG0, AP).
- dSph x is inverted from the record so that it is exactly the x the record used: nu(x) = 10^(Newton - plain),
  with plain = LW1 per_system[*].plain and Newton = X1 x1_per_system.csv Delta[Newton], same footing and name.
- SPARC v_obs, f_gas, depth and r/r_M follow QX20's build exactly. SPARC disc and bulge shares are vd2/vb2 and vbu2/vb2.
- The KiDS v_obs uses the bias-corrected ESD of each colour bin converted as in QX5's lensing() and R_med from CFG61's
  printed K1 rows.

**Missing features.** If a candidate needs a feature that is None for a class, that gate is NO VERDICT, and NO VERDICT
counts as not passing. A candidate "needs" a feature if its value changes the prediction (L1 needs sigma only where
f_sp > 0). Where the record states a bracket for the missing value, the gate is also evaluated over the bracket and
reported as a "bracket reading" (PASS for all / FAIL for all / MIXED). The bracket reading never replaces the graded
cell. Brackets (frozen now):
- stellar sigma: SPARC bulges {100, 150, 200} and SPARC discs {60} (any disc sigma < 86 km/s gives the Kroupa floor),
  X-COP BCGs {250, 300, 350}, groups {200, 250, 300}, KiDS early {130, 170, 210} and KiDS late {60} (all QX26);
- a0(z_f)/a0(0) for F2: {0.33, 0.91, 0.94, 1.00, 1.21} (CFG689's central values and the 68 % envelope to z = 2.33).

## 2. The battery (one row per gate; tolerances from the record)

Offsets D are the plain law's, built exactly as in QX20 (QX5's QX16-fixed loaders, read-only). Residual = D - Delta.

| Row | Data | Statistic | PASS line | Source of the line |
|---|---|---|---|---|
| G1 SPARC | QX20's SPARC points (Upsilon 0.5 / 0.7, Q <= 2, i >= 30) | Z = mean residual; rms of residual | \|Z\| <= 0.057 AND rms <= rms(L0) + 0.010 | 0.057: PAPER67 scatter line as QX20 used it (QX20 criteria f3967a1aa9); +0.010: QX2's SPARC/RAR rms allowance (QX2 criteria 2f84fed672) applied to L0's own fixed-Upsilon rms |
| G2 X-COP | QX20's 35 X-COP points | mean and rms of residual | \|mean\| <= 0.05 AND rms <= 0.10 | HO1 line, QX2 gate G-X |
| G3 groups | Lovisari+2015, 20 groups x (R2500, R500) | per point \|residual\| <= 2 sigma_log, sigma_log = eM/(M_obs ln 10) | >= 16 of 20 groups with both points inside, for BOTH f* = 0 and f* = 1 (strict) | QX5 group rule as QX7 iter_2/iter_3 froze it (f9020230b6) |
| G4 ellipticals | 7 Humphrey+2006 x (2, 4, 8 Re), Kroupa | mean residual | \|mean\| <= 0.15 | G7 line (QX18 criteria 032ceedf31) |
| G5 Coma UDGs | S1's 9 Coma UDGs (offset vs the action with Coma's EFE, E_v3_dmean/ln 10) | mean residual | \|mean\| <= 2 sigma_U, sigma_U = hypot(se, sigma_sys)/ln 10 of S1's S4 v3 dmean L*floor E-W row | S1 sigma as QX20 used it |
| G6 dSph classes | LW1 plain offsets (no EFE): bright M31 (25), MW classical (8), LG field | per class: median residual minus the SPARC anchor (SPARC mean residual under the same candidate), bootstrap 95 % CI (10,000 resamples, seed 21) | every one of the three classes' CI contains 0 | QX21 T2 statistic and resampling (criteria 55374ee57a); LG field promoted from "reported" to graded here because it is the no-step anchor. MW ultra-faints and M31 others: reported only (tides, QX21) |
| G7 KiDS colour split | Brouwer+2021 Fig. 8, K1 bins 8-14 | R = (D - D_law) - D_cand, D_cand = mean over K1 of Delta_early - Delta_late | \|R\| < 2 sigma_tot, sigma_tot = hypot(sigma_stat, 0.05) | QX21 T1 statistic and its "NO STEP" line (< 2 sigma) |
| G8 Solar System | C6P (8c5703da06) | F_SS = the candidate's multiplier on the non-Newtonian field at the planet / Cassini radius | max over Earth, Mars, Saturn of F_SS(r_p) x ratio_p AND F_SS(9.58 AU) x Q2_ratio, both <= 1 | C6P: planet hedgehog/bound at 24 pc (Mars 0.1728, Earth 0.0278, Saturn 0.0346) scaled by (24 pc / Lstar)^2 (C6P: the hedgehog is GM/Lstar^2); Q2 max over Hees at 24 pc (1/4.85e7, 1/5.70e7) scaled by (24 / Lstar)^3 (Q2 = -(2GM/5 pi Lstar^3) I2) |
| G9 CMB lensing shape + growth | none here | none | NOT EVALUATED in v1 (no growth solver) | QX3 |

- For a (b, F) candidate F_SS = F at the Solar-System features (b = 1 there since f_sp = 0). For a direct-Delta
  candidate F_SS = (10^Delta g_law - g_N)/(g_law - g_N) with the algebraic law at that radius (a conversion
  convention, stated), applied to C6P's screened field.
- A winner on G1-G8 on both footings is labelled "PASSES ALL STATIC GATES", never "passes all gates": G9 is not
  evaluated.

## 3. Labels

Per candidate and footing, each row is PASS / FAIL / NO VERDICT (with the bracket reading where defined). Candidate
labels:
- **PASSES ALL STATIC GATES**: PASS on G1-G8 on both footings.
- **FAIL (rows)**: at least one FAIL on either footing; the failing rows are listed.
- **NOT GRADABLE (rows)**: no FAIL but at least one NO VERDICT.

## 4. Candidates (all written here before grading; no parameter is fitted in GB1)

**L0, the plain law.** b = 1, F = 1, T = 0.

**L1, law + IMF (QX26).** F = 1. b = (1 - f_sp) + sum over stellar components of share x f_IMF(sigma), with
f_IMF = max(alpha(sigma) R_SK, 1), log alpha = 0.38 log10(sigma/200) - 0.06 (Posacki+2015, vs Salpeter), R_SK the
Salpeter/Kroupa M/L ratio feature. Needs sigma wherever f_sp > 0.

**L2, QX20's best single-variable power law (reference, expected to fail the anchors).** Delta = A (v/v_med)^b, the
V2 v_obs fit read from qx20.json per footing (A, b, v_med fitted by QX20 on the 75 hot points). v is v_obs, or sigma
for dispersion-measured systems (QX20's UDG convention; also used for dSphs).

**F1, the action's exact static field (fresh).** b = 1, F = 1, T = T_geom.
- Motivation: the v3s / AC2q static sector is AQUAL, div[mu(|grad psi|/a0) grad psi] = 4 pi G rho_b
  (EQUATIONS_IN_ORDER 2.5). The algebraic law is exact only in spherical symmetry; in discs the curl field lowers g
  (QX8: median T -0.012, larger in low-surface-density discs). This is the only per-point difference between the
  adopted action and the law in the static weak field that the record has computed; it is a property of the baryon
  geometry, not a class.
- Fixed: T from QX8's committed parts at U = 0.50, log-U interpolation over its nodes (QX8's own rule); 0 for every
  system modelled spherical.
- Not a dead key: it is the field equation itself, not morphology (QX25 graded a type label; this is the solved field).

**F2, formation-epoch a0 memory (fresh, history).** b = 1, F = 1, Delta = log10[g_law(g_N; a0 r_z) / g_law(g_N; a0)],
r_z = a0(z_f)/a0(0) piecewise-linear in z_f through CFG689's primary values (0, 1.00), (1, 0.91), (1.5, 0.94),
(2.33, 0.91), constant beyond.
- Motivation: a0 = kappa c sqrt(G rho_DE) (EQUATIONS 3.1) tracks rho_DE(z). If a system's phantom is frozen when it
  assembles (a history effect the static action does not have), its offset today is set by a0(z_f).
- Fixed: CFG689's measured a0(z) (6c064b83a3); no parameter.
- Not a dead key: it is keyed on assembly time, not on temperature, depth, density, support, gas, environment or
  morphology. It needs z_f, which no class carries, so every gate is NO VERDICT; the bracket reading states what any
  z_f could do.

**F3, exact field + IMF (fresh combination of the two live corrections).** T = T_geom and b from L1, F = 1.
- Motivation: the two corrections the record has measured to move the anchors in opposite directions (the exact field
  lowers discs, the IMF raises early-type baryons) graded together, so neither is credited alone.
- Fixed: as F1 and L1. Not a dead key for the same reasons.

Every other key in the record's dead list (p/rho, gas or host temperature, virial heating, khronon velocity, enclosed
density, gas-g, depth QX6, kinematic support QX22, cold gas QX23, environment QX24, morphology QX25, the switched
cold-dark-energy sector QX7/QX10) is not re-proposed. L2 is a reference only.

## 5. Known answers (KA FAIL means stop and fix the loader; nothing is graded)

- KA1: L0 class means reproduce QX20's KA dict (qx20.py) to 1e-6, per footing: canonical X 0.467499, E 0.209888,
  S 0.027383, G(f* 0) 0.358644, G(f* 1) 0.195519; alt X 0.434523, E 0.188763, S -0.000603, G0 0.320274, G1 0.158280.
- KA2: the UDG mean offset equals S1's meanE / ln 10 to 1e-9.
- KA3: QX21's numbers from qx21.json to 1e-9: KiDS D, sigma_stat, D_law; and the dSph class medians and 95 % CIs
  of all five classes (QX21's resampling order replayed).
- KA4: L1 reproduces QX26's elliptical IMF class mean (qx26.json D_imf) to 1e-6, per footing.
- KA5: L2 reproduces QX20's V2 SPARC prediction (sparc_pred) to 1e-9, per footing.
- KA6: every dSph inverted x is finite and positive; C6P's Mars ratio and Hees margin are read from
  c6p_cassini_hp.json and equal the values above to 1e-4 relative.

## 6. MUTATE twin (separate outputs gb1_MUTATE.*)

Newtonian gravity, b = 1, F = 0 (no law), graded on the same battery. It must FAIL (at least G1). If it does not, the
battery has no power and the run says so.

## 7. Outputs

gb1.py writes gb1.json / gb1.out; gb1.py --mutate writes gb1_MUTATE.json / gb1_MUTATE.out. RESULT.md gives the
candidate x gate x footing table with numbers and the candidate labels. Any change after this freeze is disclosed in
RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
