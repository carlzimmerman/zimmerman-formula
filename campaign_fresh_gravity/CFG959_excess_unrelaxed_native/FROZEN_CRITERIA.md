# CFG959 FROZEN CRITERIA: the excess family as UNRELAXED native cold energy (H-UNR), one kinematic rule for all classes

- **Block:** CFG950–959 (LEDGER row "CFG950–959", reserved for this lane). Date 2026-10-21.
- **Kind:** HYPOTHESIS TEST, zero fitted constants in the primary form. Committed alone, before any script or number of this lane.
- **Not blind (disclosed).** H-UNR was written after the excess record was read (CFG687, CFG919, CFG921, CFG928, CFG930, CFG932,
  CFG933, CFG936, CFG939, CFG940, CFG949, CFG953–CFG955). Pre-freeze expectations are listed in §9, including hand estimates made
  from record numbers before freezing. No number of this lane exists yet.
- **Settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻² scored separately, never pooled. Raw data and
  framework-native inputs only. "Cold energy" is the framework's own cold component, not a particle species. Not "theory closed".
  Nothing here may say the data favour the framework. A FAIL is reported as plainly as an EXPLAINS.

## 1. Question

Can the excess family (dSphs, Coma UDGs, cluster cores, red lenses above the law; SPARC discs and cluster outskirts on it; TDGs and
NGC 1052-DF2/DF4 at Newton) be explained, with zero new constants, by: the law is the RELAXED end state of a system's cold energy;
relaxation needs a coherent rotating baryonic structure; dispersion-supported systems keep their native collapse debris unrelaxed?

## 2. The hypothesis and the derived criterion

**Rule (H-UNR, a NEW RULE, no new constant).** Cold energy relaxes to the law state only by handing energy and angular momentum to
a coherent (ordered) baryonic flow. Status: CFG919 proved that the record's cold-energy equation (CFG638) cannot make any
kinematic selector; H-UNR is therefore a posit outside the record's equations, in CFG919's family 2 ("kinematics-dependent
retention"). It brings no constant in the primary form.

**Derivation of the retained fraction u (primary, P-LIN).** Write the baryons' kinetic energy K = K_ord + K_rand,
K_ord = ½Mv², K_rand = (3/2)Mσ².
1. Random motions have zero mean azimuthal momentum flux on every annulus, so they exert no secular torque on the debris. Only the
   ordered flow can carry the time-dependent, non-axisymmetric patterns (bars, spirals) that transport angular momentum. (CFG919's
   symmetry note says a steady axisymmetric flow transports nothing radially; the channel must be the non-axisymmetric part of an
   ordered flow.)
2. The two components share one potential. By the virial theorem each supplies a share of the support against gravity equal to
   its share of K. The debris in a system's domain is therefore assigned to the two channels in the ratio K_ord : K_rand.
3. Bang-bang limit: the ordered channel relaxes its share completely over the system's age (discs complete ≳ 20 orbits; SPARC sits
   on the law), and the random channel relaxes none of its share.

   ⇒ **u = K_rand/K = f_P = 3σ²/(v² + 3σ²)**, i.e. CFG919's own pressure-support measure, applied per system from kinematics on
   disk. u = 0 for a cold disc, u = 1 for a pressure-supported system. There is no threshold and no constant. The linear map is the
   argument's consequence, not a fit; items 2–3 are the posit.

**Declared alternative forms (reported; they do not govern the class):**
- **V-EQ (step, no constant):** u = Θ(f_P > ½). A system relaxes as a whole iff its ordered kinetic energy exceeds its random
  kinetic energy (v/σ > √3; CFG919's F2 step).
- **V-OP (step, ONE IMPORTED constant):** u = Θ(f_P > 0.72). A self-gravitating system can sustain the coherent global mode iff
  t = T_rot/|W| ≥ 0.14 (Ostriker–Peebles 1973, N-body calibrated, Newtonian). With 2K + W = 0, t = (1 − f_P)/2, so t < 0.14 ⇔
  f_P > 0.72. The 0.14 is imported, not derived in the framework. If V-OP were the only form to EXPLAIN, the result would be
  CONDITIONAL on that imported constant.

## 3. The model

For a system with baryons M_b(<r), the law g_law = g_N ν(g_N/a0) (each class's own record kernel, §4), the phantom
M_ph(<r) = (g_law − g_N) r²/G, a native cold supply M_c, a native profile M_cNFW(<r) and retained fraction u:

- **Primary reading R-C (mass-conserving; the record's "identity" form, CFG930 R1, with settled fraction 1 − u):**

      g_model(r) = g_N(r) + G [ min(M_ph(<r), (1 − u) M_c) + u · M_cNFW(<r) ] / r²

  At u = 0 this is the (supply-capped) law. At u = 1 it is Newtonian baryons + native debris, i.e. CFG949's B0 reading, as the
  hypothesis states ("as in CFG949").
- **Secondary reading R-A (additive; NOT mass-conserving, the most generous bracket for an excess):**

      g_model(r) = g_law(r) + u · G M_cNFW(<r) / r²

  R-A double-counts u·M_c (the law's phantom and the debris are the same cold energy). It is reported as an upper bracket. It cannot
  govern the class; a rescue by R-A alone would need a dated, labelled amendment that re-states the hypothesis.
- **Systems that captured no cold energy** (TDGs; NGC 1052-DF2/DF4: in situ / no capture, CFG936 route (i), CFG939's derived
  no-capture criterion, CFG953 C-DF): M_c = 0, so g_model = g_N for every u (the hypothesis' own third clause).

**Native debris rule (inherited, no new input):**
- Supply M_c = (1 − f_b) M_ta = 5.364 × catchment baryons, with M_ta from CFG804's fixed point and the census f_ret (CFG416/556/804,
  `mta_fixed`, verbatim in CFG930/CFG949; S-cen). Baryons entering the supply = the system's total current baryons (stars + 1.33
  M_HI where present), as in CFG930/CFG949.
- Profile: truncated NFW with ρ_s = C ρ̄_m(z_c), C = 3000, z_c from the native EPS half-mass condition (CFG654 native tables),
  boundary r_ta (CFG930 rule R930; CFG949's copy `prof930`).
- Observation epoch z_i: z_i = 0 for every galaxy-scale system (CFG930 verbatim; dwarfs, SPARC, rotators, Coma UDGs, lenses);
  each cluster's own redshift (CFG949's primary). Variant: clusters at z_i = 0 (CFG949's one-at-a-time variant).

## 4. Classes, data, kinematic measure, estimator (each class's own record estimator; read-only reuse)

| item | sample (record) | f_P (u in P-LIN) | estimator and kernel | observed (stored) |
|---|---|---|---|---|
| (a) SPARC discs | 175 galaxies, CFG695's S2 recipe (CFG4 statistic, Υ grid 0.30–1.20, bulge 1.4Υ) | 3σ²/(V_flat² + 3σ²), σ = 10 km/s (CFG919); V_flat = 0 → max V_obs | weighted rms of log g_obs − log g_model, ν_simple (CFG695), FP0 a0 | 0.1009 @ 0.60 / 0.0994 @ 0.55 |
| (a2) rotation-supported lenses | B21 isolated n < 2 (CFG919 LD cells), point mass log M = 10.45 (CFG921) | 0.20 (CFG919 proxy) | CFG919 cells_lens, ν_e, 0.05-dex floor, class GLS | +0.008 ± 0.091 / −0.083 ± 0.091 ln |
| (b) dSphs | CFG880's 83 LVD dwarfs (CFG914/919 DWR), Υ_V 2, M*/2 + gas inside r12 = (4/3) r_h | 1 (no rotation data on disk; CFG919) | E = 2 ln(σ/σ_law), CFG919 cells_persys + 0.05-dex floor + class GLS, ν_e | +0.856 ± 0.102 / +0.765 ± 0.102 ln |
| (c) Coma UDGs | CFG933's 9 admitted Coma UDGs (stars only, r12 = (4/3) R_e) | 1 | CFG928/933 sealed estimator (ν_e, isolated); mean and se = max(meas, scatter) | +0.760 / +0.669 ln, se 0.262 |
| (d) cluster cores + outskirts | 318 eRASS1, CFG687's raw KiDS stack, CFG949 machinery (β 2/3, r_c 0.15 R500, f* 0.20) | 1 (thermal ICM) | A_MID, A_OUTER (30-patch jackknife), outer slope s; law kernel ν_mono (CFG687) for R-A | law: 1.910/1.754, 1.012/0.927 |
| (e) red lenses | B21 isolated n > 2 (CFG919 LS cells, +0.123 M* shift), point mass log M = 10.81 + 0.123 (CFG921) | 0.80 (CFG919 proxy) | as (a2) | +0.293 ± 0.067 / +0.203 ± 0.067 ln |
| (e-IMF) | same, IMF alternative: n > 2 masses +0.172 dex more (CFG926 R5), in g_bar AND in the supply | 0.80 | as (a2) | (rebuilt) |
| (f) TDGs; DF2/DF4 | CFG936's 6 Lelli+15 TDGs; CFG655/657 DF2, DF4 | — (M_c = 0) | CFG936 route (i) rows (Newton) | TDG −0.690 / −0.728 dex vs law |
| (g) faint rotators | CFG940's 25 McQuinn+22 rotators (stored table: R, V_cor, log g_obs, log g_bar A/B, lMb, E, sE); V_rot from Table 2 | 3σ²/(V_rot² + 3σ²), σ = 10 km/s | E = log10(g_obs/g_law), ν_e; mean, se = √(se_of² + 0.05²) (CFG940 WS) | B −0.083 ± 0.064 / −0.121 ± 0.064 dex; A −0.304 / −0.340 |

Notes. Rotating UDGs: none in the record → (g) for UDGs is NOT TESTABLE. Lens radii: R = √(G M / g_bar) for the class point mass
(CFG921's lens convention). B21's g_obs = 4GΔΣ is compared with the 3D g_model, as the record compares it with the 3D law
(declared; the NFW-vs-SIS conversion difference is a stated systematic, not corrected). For SPARC the supply uses
M_b = Υ L[3.6] + 1.33 M_HI (CFG930 convention) at each Υ of the grid.

## 5. Per-item grading (per footing)

- **Residual** E_res = E_obs − E_pred, E_pred = ln (or log10, in the class's units) of g_model / g_law at the class's radius; for
  lens and cluster stacks the model replaces the law in the record's amplitude estimator.
- **Labels** (z = class mean residual / its error): |z| < 2 CONSISTENT; 2 ≤ |z| < 3 TENSION; |z| ≥ 3 CONTRADICTED.
- **(a) SPARC:** PASS iff rms ≤ 0.110 dex with best Υ in 0.50–0.80 (the record's tolerance, CFG4 H2 / CFG695 C2), both footings. Δrms
  against 0.1009 / 0.0994 is reported.
- **(a2) n < 2 lenses:** label as above; CONSISTENT required.
- **(b) dSph class mean:** label as above.
- **(b2) per-dwarf scatter:** hierarchical E_res,i = c + δ_i + ε_i, δ ~ N(0, s²), ε ~ N(0, sE_i²), profile likelihood on s (c
  maximised). The same for E_obs about a free constant (the record's scatter in this estimator; the analogue of CFG880's s_int 0.38,
  which is in ln σ_x of the clump model and is not the same quantity). PASS iff the 95% upper bound on s under H-UNR is below the
  constant model's best s (H-UNR must remove a significant part of the per-dwarf scatter). Δ(−2 ln L) between the two at equal
  parameter count, and the slope of E_obs on E_pred, are reported.
- **(c) Coma UDGs:** label as above (se of the residual = max(√Σ sE²/N, sd/√N), CFG933's convention).
- **(d) clusters:** CFG949's rule: EXPLAINS iff |A_MID − 1| < 2σ, |A_OUTER − 1| < 2σ and |s − s_obs| < 2 s_err; PARTIAL if MID or
  OUTER passes; FAILS otherwise. EXPLAINS counts as CONSISTENT.
- **(e) red lenses:** label as above, as observed and under e-IMF. If the two labels agree, (e) enters the overall class with that
  label; if they differ, (e) is IMF-DEPENDENT and is excluded from the overall class (reported).
- **(f) TDGs, DF2/DF4:** label of the residual against g_model = g_N, per sample. Inherited from the hypothesis' no-capture clause,
  so it carries no evidential weight; reported diagnostic: DF2/DF4 if they had kept native debris (u = 1).
- **(g) rotators:** label of the mean residual under bracket B (CFG940 found B matches the 7 SPARC overlaps; A runs 0.18 dex low);
  A reported. Reported, no class weight (g2): the H-UNR predicted dSph − rotator difference in the matched cell
  [10⁻¹², 10⁻¹¹·⁵) (dSphs: the 83; rotators: bracket B) against the observed difference in the same cell and groups.

## 6. Overall class (per footing; the primary form P-LIN, reading R-C, primary corner)

- **H-UNR EXPLAINS:** (a) PASS, (a2) CONSISTENT, (b) CONSISTENT, (b2) PASS, (c) CONSISTENT, (d) EXPLAINS, (e) CONSISTENT (or
  IMF-DEPENDENT), (f) CONSISTENT, (g) CONSISTENT. Zero new constants.
- **H-UNR FAILS:** the rotation-supported anchor breaks ((a) FAIL, or (a2) or (g) CONTRADICTED), OR none of the excess items (b),
  (c), (d), (e) is CONSISTENT/EXPLAINS, OR (f) is not CONSISTENT.
- **H-UNR PARTIAL:** otherwise. The README names which excess classes are explained and which are not, with numbers.
- **Footings:** classes are given per footing. If they differ, both are shown and the headline is the less favourable.
- **Robustness:** the primary class is recomputed at 12 corners: profiles {C 1500, 3000, 6000} × {r_ta, r_vir} × supply {census, ×2}
  (CFG930's corner family). ROBUST iff the class is the same at all 12; else FRAGILE with counts.
- **Forms and readings:** V-EQ, V-OP and reading R-A are reported with their own classes (primary corner). They do not change the
  governing class. Brackets reported: dSph f_P (CFG919 V3a: HI-bearing v/σ = 1, others v/σ = 0.5), SPARC/rotator σ = 6 / 20
  km/s, lens f_P (0.43, 0.57) and (0.10, 0.97) (CFG919 V3a/V3b), clusters at z_i = 0.

## 7. K tests (all must pass; a failed K stops the lane with no class)

| K | target | tolerance |
|---|---|---|
| K1 | CFG919 stored class means DW, LD, LS (E, se; both footings), from this lane's rebuilt cells | 1e-9 |
| K2 | CFG687 A_MID, A_OUTER (value + jackknife, both footings) through CFG949's machinery | 1e-6 relative |
| K3 | CFG949 B0 primary corner (A_MID 1.011 ± 0.063, A_OUTER 1.047 ± 0.089, s 0.661; stored JSON) | 1e-9 relative |
| K4 | CFG930's stored SPARC halo facts (median z_c, c, r_s, r_b, M_ta/M_b; 147 galaxies, CFG930's sample and conventions) through this lane's galaxy halo code | 1e-9 relative |
| K5 | CFG695 S2 rms and Υ (law, both footings) through this lane's SPARC engine | 1e-6 |
| K6 | CFG933 Coma mean E_obs and se_obs (both footings) | 1e-9 |
| K7 | CFG936 route (i) T and U statistics recomputed from its stored per-object rows | 1e-9 |
| K8 | CFG940 WS means and se (A and B, both footings) from its stored per-galaxy table | 1e-9 |
| K9 | CFG880 sample N = 83 and its committed per-dwarf σ_law (both footings) | 1e-9 relative |

## 8. MUTATE (separate outputs, `_MUTATE` in the names)

- **M-DISC:** u = 1 for every system, discs, n < 2 lenses and rotators included. Bites iff SPARC (a) FAILS on both footings.
- **M-ZERO:** u = 0 for every system with the uncapped law (no retained debris). Bites iff the record's offsets come back exactly:
  dSph class mean = CFG919 DW, Coma = CFG933, red lenses = CFG919 LS, clusters = CFG687 A, SPARC = CFG695 rms (tolerances as K).
  The excesses then reappear as model deficits.
- **M-PLANT:** synthetic observed values = the H-UNR primary prediction (dSphs, Coma UDGs, rotators: + Gaussian noise with each
  object's errors, seed 959; lenses: g_obs := g_model, noiseless). Bites iff the planted items come out CONSISTENT on both footings
  (the classifier can return EXPLAINS-level labels).

## 9. Pre-freeze expectations (from record numbers and hand estimates; disclosed)

- **E1 dSphs:** CFG930 D4 puts native debris at Q_ap = 0.14–0.32 of the settled phantom at every dwarf aperture. R-C at u = 1 should
  put dSphs well BELOW the law (hand estimate −0.5 to −0.8 dex); R-A should give at most ~+0.06–0.13 dex (CFG930 F*, ε = 0). Expect
  (b) CONTRADICTED in both readings. CFG955's T-EX already argued this for any τ; this lane tests the kinematic selector jointly.
- **E2 clusters:** R-C at u = 1 is CFG949's B0 (EXPLAINS at the primary corner, FRAGILE). R-A (law + debris) should overshoot the
  core (hand estimate A_MID ≈ 0.7).
- **E3 red lenses:** for log M ≈ 10.9 the native supply is ~30–60 M_b and its NFW holds several M_b inside 100 kpc (CFG954: native
  dust exceeds the phantom at 20–50 kpc in M_b ≥ 1e10 galaxies). Expect H-UNR to overshoot the n > 2 lenses, and the n < 2 lenses
  under P-LIN (u = 0.2).
- **E4 Coma UDGs:** apertures r12 = 2–6 kpc are far larger than dSph apertures; the native debris may exceed the phantom there.
  Outcome not known before running.
- **E5 SPARC:** f_P ≤ ~0.1, small change; expect (a) PASS. **E6** (f) Newtonian by construction. **E7** slow rotators get u ≈ 0.4–0.75;
  expect a small shift.

## 10. Compute and hygiene

- One core (OMP_NUM_THREADS=1), `nice -n 10`, one process at a time, in-script RSS guard 0.95 GB (abort above). No downloads.
  Running processes are not touched.
- Other lanes' code is exec'd read-only from slices, with every file write refused by a guard on `builtins.open`/`io.open`; other
  lanes' JSON/npz are only read. No other lane, no LEDGER row and no THEORY_CANONICAL file is edited.
- Outputs: `cfg959_K.out`, `cfg959_results_K.json`; `cfg959_MUTATE.out`, `cfg959_results_MUTATE.json`; `cfg959.out`,
  `cfg959_results.json`. Earlier failed runs are kept and disclosed.
- Any change after this commit is a dated, labelled amendment (pre-result or POST HOC), committed before the affected number where
  possible.
