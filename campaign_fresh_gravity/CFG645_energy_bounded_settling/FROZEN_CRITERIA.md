# CFG645 FROZEN CRITERIA: energy-bounded settling (hypothesis H-EB)

Committed ALONE, before any CFG645 code or number. Date 2026-10-12.

κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. "Cold energy" throughout; its mass is
required. No particle species. Not "theory closed". No ΛCDM or standard-MOND yardstick enters any verdict. T6 (halo model) is
CONTEXT ONLY, as in CFG556.

## 1. Hypothesis

Settling must shed energy (CFG541 infall path loses energy; CFG542 hands it to a dark-energy partner; CFG643 baryon heating has the
wrong sign; astra collective_energy_gate: diffuse states export 0.27–0.39 M V_f²). Candidate B sets the settled amount by supply
(5.364 × catchment baryons) and an edge; CFG637 shows the phantom then takes the whole supply, and CFG596 excludes the result on raw
KiDS. **H-EB:** the settled amount is limited by the energy the system can dispose of. Settling stops where (or when) the energy handed
to the receiver reaches a capacity fixed by the framework's own quantities. The capacity must be DERIVED, not fitted.

Framework identity used throughout (A2): ρ_DE c² = a₀² / (κ² G). Hence a local energy-density capacity
ρ_cap(r) = ρ_DE c² / e(r) = a₀² / (κ² G e(r)) in any consistent unit system, where e(r) is the energy exported per unit settled mass.

## 2. Capacity routes (each derived or labelled KNOB)

| route | capacity | free constant? |
|---|---|---|
| **EB-R** (global, rest energy) | C = ρ_DE c² V_ta (catchment turnaround volume). Exchange efficiency 1, because CFG542's Q carries all of ΔW (K2/K7). Settling inside-out (CFG598 front) stops when cumulative export reaches C | none (but astra receiver_capacity: a constant V₀ is not available energy; reported as an admissibility flag) |
| **EB-K** (receiver kinetic capacity, astra receiver_capacity exact channel) | available receiver energy L = π₀²/2 = (1 + w) ρ_DE c² V / 2. Exact Λ (the framework's input, w = −1) gives π₀ = 0 | none for w = −1; any π₀ ≠ 0 is a free initial datum |
| **EB-L** (local, CFG635-native) | ρ_set(r) ≤ ρ_cap(r) = a₀²/(κ² G e(r)): settle only what the local dark-energy reservoir can absorb where it is deposited. Two brackets for e: **e_V = V_c(r)²** (CFG635's R) and **e_Φ = Φ(r_ta) − Φ(r)** (fall from rest at turnaround, nothing retained; upper bracket). Unsettled excess stays in the outer reservoir (R5 draws from the edge–r_ta shell): PRIMARY; bracket: the excess stays inside the capped radius (enclosed mass beyond the capped zone unchanged) | none |
| **EB-η** | C = η ρ_DE c² V_ta with η free | **KNOB** by construction; reported only (η_crit per mass, one boundary evaluation, section 5) |

The astra exact channel is solved for the EXPORT sign (D < 0) as well as for import: S2 below.

## 3. Derivation outputs (both footings)

- **D1 settled amount vs mass.** Systems: M200m = 1e11, 3e11, 1e12, 3e12, 1e13, 1e14, 1e15 M☉/h through CFG556's halo machinery
  (inherited context ingredients, labelled as in CFG556: NFW shape for the unsettled shell, r200c, SHMR stars, Δ_ta = 11.81). For each:
  M_set (candidate B), export E_V = ∫ e_V dM_set and E_Φ = ∫ e_Φ dM_set, E/(M_set V_f²), C_rest, Ξ = C_rest/E_Φ, the EB-L removed
  fraction (total and inside 0.2–0.5 r_ta) for e_V and e_Φ, the radius range where EB-L binds (in r/r_ta and g/a₀), and η_crit = E_Φ/C_rest.
- **D2 rule for EB-R.** If Ξ ≥ 10 for every mass, both footings: EB-R is INERT (≡ candidate B; the capacity never binds).
  If Ξ < 1 somewhere: EB-R binds there and is scored as a new profile.
- **D3 rule for EB-K.** If the exact export channel gives a settled amount that is either 0 (π₀ = 0) or the full target (π₀ ≠ 0) with
  no intermediate endpoint: EB-K is BINARY (amount knob-free only in the two limits; the limits are the MUTATE limits).
- **D4 rule for EB-η.** η_crit spread = max/min over the D1 masses. If > 3: a single η that keeps galaxies fully settled must change
  groups or clusters → the route is a KNOB with mass-dependent effect (reported).

## 4. Tests (light, analytic + committed code; NO PM)

Applied to each derived non-binary route (EB-R, EB-L e_V, EB-L e_Φ) on candidate B's own source (all baryons) and B's derived reservoir
(CFG637 RD = empty, i.e. CFG634 R0), both footings.

| test | code reused | label rule |
|---|---|---|
| **T1 SPARC** | CFG487 harness as CFG634 T1 executes it; EB-L cap applied per galaxy on the rotmod baryon field (point-mass interior inside the first data point, declared; e_Φ uses the census edge then Newtonian mass to r_ta, f_ret = 0.10) | PASS if rms ≤ 0.12 and \|Δrms vs B\| ≤ 0.005 both footings; FAIL if rms > 0.15; else TENSION |
| **T2 Tian+26 groups** | CFG634 `sigma_hcb` (CFG543 machinery), src = all, res = R0, one patch applying the cap to `mph` | CFG543 stats label; PASS = CLOSES both footings |
| **T3 X-COP** | CFG634 `cl_model`/`t3_cell`/`t3_label`, src = all, res = R0, cap applied on the audit profile (CA.RADII; no removal inside 30 kpc declared) | t3_label on headline η and inner band 200–420 kpc |
| **T4 Bullet** | CFG634 `dark_components`/`t4_cell` (CFG625 tools; Paraficz PROVISIONAL), src = all, res = R0, cap on ρ_set | t4_cell label for B1 both footings; core M(<250)/P16 reported |
| **T5 KiDS isolated lenses** | CFG529/531 record + lr_lenses.npz | Magnitude-and-sign rule: compute the removed fraction δ = ΔM_removed / M_law(<R_min) at the innermost RAR bin radius (g_obs = 5e-12 m s⁻²) for log M_gal at the 5/50/95 percentiles of the catalogue. EB-L only removes mass, and the recorded f30 miss is an inner-bin DEFICIT (CFG529), so EB-L cannot pass: label UNCHANGED (FAIL, = record) if δ ≤ 1e-3, WORSE if δ > 1e-3. EB-R inert → record |
| **T6 growth proxy (CONTEXT ONLY)** | CFG556 halo model executed from its source; cap applied to the settled part of `frame_profile`, removed mass returned to the drained shell (mass inside r_ta conserved) | REMOVES if R(k=1) − 1 ≤ 0.10 and R(k=1) ≥ 0.90 both footings; REDUCES if the k = 1 excess falls by ≥ 25%; else UNCHANGED |

**Inertness tolerance.** A route is INERT on a gate if the statistic changes by ≤ 0.005 dex (T1, T2), ≤ 0.01 in η (T3), ≤ 0.1 in z (T4),
≤ 1% of the excess (T6).

## 5. Reported only (no verdict weight)

- EB-η boundary: η_gal = max of η_crit over M200m ≤ 3e12 (the smallest η that keeps every galaxy-scale halo fully settled). At η_gal,
  inside-out truncation (settle the law profile from the centre until cumulative E_Φ = η_gal C_rest) gives the settled fraction for groups
  and clusters and one T6 evaluation. One evaluation at a derived boundary; NO scan over η.
- astra local_sink_reaction flag for EB-L: local deposit as vacuum needs a reaction force density ∇u (u = ρ_set e); ratio |∇u|/(ρ_tot g)
  at the binding radii.
- E_V/(M_set V_f²) and E_Φ/(M_set V_f²) next to astra's export bounds 0.27–0.39 (benchmark sanity only).

## 6. Checks

- **S1** (control) numerical R(y) = ρ_ph V_c²/(ρ_DE c²) for a point mass reproduces CFG635: deep limit κ² y/(4π) to 1e-3 at y = 1e-4;
  exponential-kernel peak 0.43 ± 0.01 near y ≈ 24; repaired ν_mono R = 1 at y = 36 ± 2.
- **S2** sympy: the astra channel solution for both signs of D satisfies the ODE and energy conservation; numerical ODE for D < 0
  (export): x → A for π₀ ≠ 0 (π₀² = 1e-6, 1e-2, 1 in units of |D|A), x ≡ 0 for π₀ = 0.
- **S3** the cap code path with capacity → ∞ reproduces CFG634/CFG637 B numbers (T2, T3, T4) and CFG556's primary R(k) to 1e-9.

## 7. MUTATE (`CFG645_MUTATE=1`, separate outputs)

- **M∞** capacity → ∞ reproduces candidate B / CFG637 exactly (S3; must hold).
- **M0** capacity → 0 (nothing settles; the receiver at rest, EB-K at w = −1): galaxies must break, T1 rms > 0.15 both footings
  (Newtonian baryons at the data radii; the unsettled reservoir is not placed, declared), and T2 must not CLOSE.
- **Mc** the EB-L cap × 1e-3 (ρ_cap/1000) must change T1, T2 or T3 visibly (beyond the inertness tolerance): the cap code can bite.

## 8. Verdict rule

- **H-EB KNOB-FREE PASS** if some derived, non-binary route passes T1, T2, T3 headline and T4b B1 on both footings, does not WORSEN T5,
  and T6 reads REMOVES (context).
- Otherwise each derived route is labelled: INERT (≡ B; inherits CFG596 / CFG637 fails), BINARY (EB-K: 0 = breaks galaxies, full = B),
  or FAILS (listed gates).
- If no derived route passes: **H-EB NOT DERIVABLE KNOB-FREE**; if the only route that can bind at the radii that decide clumping is
  EB-η, label **KNOB**.

## 9. Disclosure before any number

Hand estimates made while reading (no code run): CFG635's deep relation R = κ²g²/(4πa₀²) is small where g ≪ a₀, so EB-L is expected
to bind only at high g (inner galaxies, cluster cores), not at 0.2–0.5 r_ta; CFG630/CFG542 K7 put the cosmic settling hand-off at
~1e-6 of ρ_DE, so EB-R is expected to be inert; the astra exact channel for export has π² growing, so EB-K is expected to be binary.
These expectations are written here so that the computation can contradict them.

Machine: 1 process, ≤ 1.5 GB, nice -n 10. Do not touch cfg636_pm.py, the cfg640 waiter, or the cfg625 driver. No downloads.
