# CFG645: energy-bounded settling (H-EB). Verdict: NOT DERIVABLE KNOB-FREE. Every derived capacity is inert (= candidate B) or zero; only a free efficiency binds where clumping is decided (KNOB)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone in 21b7b0857 before any CFG645 code or number. Date 2026-10-12.
- **Settings:** κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10, never pooled. "Cold energy" throughout; its mass is
  required. No particle species. Not "theory closed". No ΛCDM or standard-MOND yardstick enters a verdict; T6 (halo model) is CONTEXT ONLY.
- **Scripts** (repository root, `OMP_NUM_THREADS=1 nice -n 10`, one process, well under 1 GB, about 10 s each):
  - `cfg645_lib.py`: capacities and the cap (unit-agnostic).
  - `cfg645_derive.py`: S1, S2, D1–D4, T5 bound, T6 (CFG556 executed from its source), EB-η boundary. Writes `cfg645_derive.out` / `_results.json`.
  - `cfg645_gates.py`: T1 SPARC (CFG487 harness as CFG634 runs it), T2 groups, T3 X-COP, T4 Bullet: CFG634's committed code executed from its
    source with one patch per function (the cap on the settled phantom), as CFG637 did. Writes `cfg645_gates.out` / `_results.json`.
  - `CFG645_MUTATE=1` writes `*_MUTATE.out` / `*_MUTATE.json`.
- Nothing downloaded. No other lane touched. `PM_SPEC.md` is the native PM spec, not run.

## The physics question

Settling must shed energy: CFG541's infall path loses energy, CFG542 hands it to a dark-energy partner, CFG643 shows baryon heating has
the wrong sign, and astra's collective_energy_gate needs export of 0.27–0.39 M V_f². H-EB asks whether the amount that settles is set
by how much energy the system can dispose of, with the capacity fixed by the framework's own quantities. The one identity used is
A2: **ρ_DE c² = a₀²/(κ² G)**, so a local capacity is ρ_cap = a₀²/(κ² G e), with e the energy exported per unit settled mass.

## Capacity derivations and knob count

| route | capacity | knobs | result |
|---|---|---|---|
| **EB-R** global rest energy | C = ρ_DE c² V_ta, efficiency 1 (CFG542 Q carries all of ΔW) | 0 | **INERT.** C/E_Φ ≥ 7.99e3 at every mass, both footings (galaxies 2–3e6, clusters 0.8–1.0e4), even with the upper export bracket. The capacity never binds: EB-R = candidate B exactly. (astra: a constant V₀ is not available energy, so this route is also inadmissible as stated.) |
| **EB-K** receiver kinetic capacity (astra exact channel) | L = π₀²/2 = (1 + w) ρ_DE c² V/2 | 0 at w = −1 | **BINARY.** Solved for the export sign (D < 0), which astra's note left open: π² = π₀² + 2\|D\|x GROWS as the receiver absorbs, so there is no ceiling. Endpoint x → A for every π₀ ≠ 0 (π₀² = 1e-6, 1e-2, 1 all reach 1.000000), x ≡ 0 for π₀ = 0. π₀ sets only a logarithmic lag (t_half 7.26 vs 0.47). Exact Λ (the framework's input) has π₀ = 0: nothing settles, which breaks galaxies (M0). Any π₀ ≠ 0 settles everything: B. No intermediate amount exists. For import (D > 0) the endpoint is min(A, L), reproducing astra (0.25 / 0.99 / 1.00). |
| **EB-L** local energy density (CFG635-native) | ρ_set ≤ a₀²/(κ² G e), e = V_c² or Φ(r_ta) − Φ(r) | 0 | **INERT where it matters.** It binds only at high g (r ≤ 2.6e-3 r_ta, g = 1–57 a₀), removing 5–11e-5 of the settled mass (e_Φ) and nothing with e_V. Removed fraction inside 0.2–0.5 r_ta: **0** at every mass, both brackets, both footings. |
| **EB-η** free efficiency | C = η ρ_DE c² V_ta | 1 (η) | **KNOB.** η_crit = E_Φ/C_rest runs from 3.8–5.0e-7 (1e11) to 0.98–1.25e-4 (1e15): spread ×253 / ×258. Any η that binds in groups/clusters while galaxies stay full is a free constant with a strongly mass-dependent effect. |

**Why the local capacity cannot reach the clumping region (the theorist's reading).** CFG635's ratio R = ρ_ph V_c²/(ρ_DE c²) =
κ²g²/(4πa₀²) in the deep regime. It is largest where g is large and falls as g² outward. The boundary R = 1 sits at
g* = √(4π)/κ a₀ = 7.09 a₀ in the deep formula; with the real kernels it is set by their tails (S1: exponential-kernel peak 0.428 at
y = 23.9, so with e = V_c² it never binds; repaired ν_mono reaches R = 1 at y = 36.05). At the 0.2–0.5 r_ta band where CFG596's excess
lives, g ≲ 0.05 a₀ and R ~ 5e-5. "Settle only what the local dark energy can absorb" therefore trims galaxy cusps and BCG cores, not the
outer settled mass. The boundary IS mass-dependent (it exists only in systems whose g exceeds ~7 a₀), but it is an inner hole, not an
outer edge.

**Why the global capacity is so large.** C_rest/E ~ (ρ_DE/ρ̄_ta)(c²/V_f²) ~ 0.4 × (c/V_f)². The catchment's dark-energy rest energy
exceeds the settling export by 4–6 orders of magnitude, matching CFG630 / CFG542 K7 (the cosmic hand-off is ~1e-6 of ρ_DE).
Rest energy is huge and available kinetic energy is zero, and neither one gives an intermediate cut.

## Settled amount vs mass (D1, candidate B's profile; CFG556 machinery, context ingredients as in CFG556)

Canonical / alt. M_set/M_ta = 0.843 at every mass (B settles the whole supply, CFG637).

| M200m [M☉/h] | log M_ta | f_ret | V_f [km/s] | E_V/(M_set V_f²) | E_Φ/(M_set V_f²) | C_rest/E_Φ | η_crit | EB-L removed (e_Φ) |
|---|---|---|---|---|---|---|---|---|
| 1e11 | 11.37 | 0.10 | 82 / 86 | 0.84 | 1.44 / 1.46 | 2.0e6 / 2.6e6 | 4.9e-7 / 3.8e-7 | 6.1e-5 / 5.9e-5 |
| 1e12 | 12.39 | 0.10 | 148 / 155 | 1.02 | 1.63 / 1.66 | 5.6e5 / 7.2e5 | 1.8e-6 / 1.4e-6 | 7.7e-5 / 8.6e-5 |
| 1e13 | 13.40 | 0.43 | 382 / 400 | 0.78 | 1.28 / 1.30 | 1.1e5 / 1.4e5 | 9.5e-6 / 7.3e-6 | 1.1e-4 / 1.1e-4 |
| 1e14 | 14.42 | 0.78 | 795 / 834 | 0.80 | 1.24 / 1.27 | 2.5e4 / 3.3e4 | 4.0e-5 / 3.1e-5 | 9.9e-5 / 9.6e-5 |
| 1e15 | 15.44 | 0.90 | 1486 / 1558 | 0.82 | 1.12 / 1.16 | 8.0e3 / 1.0e4 | 1.3e-4 / 9.8e-5 | 5.4e-5 / 5.2e-5 |

(3e11 and 3e12 are in the JSON.) Both export brackets exceed astra's net-export bounds (0.27–0.39) because they keep no kinetic energy:
they are upper brackets, so the inertness of EB-R and EB-L is conservative. **Under every derived route the settled amount vs mass is
B's: 0.843 M_ta (galaxy, group and cluster alike), minus ≤ 1.1e-4 in the innermost cusp.**

## Per-test table (canonical / alt)

| test | B (capacity ∞) | EB-R | EB-L e_V | EB-L e_Φ |
|---|---|---|---|---|
| T1 SPARC rms (dex) | 0.1003 / 0.1013 PASS | same, PASS | 0.1003 / 0.1012 PASS | 0.0999 / 0.1001 PASS (cusp trims, ≤ 5.6% of one galaxy's phantom) |
| T2 Tian groups | +0.060 (Z 1.65) / +0.043 (Z 1.20) CLOSES | same | same | same |
| T3 X-COP η headline | 1.820 ± 0.067 / 1.679 ± 0.062 FAIL | same | same | same (cap never binds at ≥ 30 kpc: max ρ_set/ρ_cap 0.68) |
| T3 inner band 200–420 kpc | 3.163 / 2.927 FAIL | same | same | same |
| T4b Bullet B1 Δκ (z) main / sub | +0.021 (−3.41) / +0.001 (−2.30); +0.025 (−3.36) / +0.005 (−2.24) FAIL | same | same | sub +0.0006 / +0.0046, FAIL |
| T4c main M(<250)/P16 (PROVISIONAL) | 0.32 / 0.35 | same | same | same |
| T5 KiDS f30 | CFG529 record: FAIL | = record FAIL | removed/M_law(<R_min) ≤ 5.2e-4 (ν_mono), 0 (exp): UNCHANGED, FAIL | ≤ 9.2e-4 / 7.7e-4: UNCHANGED, FAIL |
| T6 growth (context) R(k=0.3), R(k=1), σ8 ratio | 1.124, 1.716, 1.040 / 1.140, 1.885, 1.046 | UNCHANGED | UNCHANGED | UNCHANGED (excess cut 3.7e-4 / 2.9e-4) |
| inert vs B (frozen tolerances) | — | all gates | all gates | all gates |

T5 sign rule: EB-L only removes mass, and CFG529's f30 miss is an inner-bin deficit, so no EB-L variant can pass T5. CFG596
(raw KiDS-1000, canonical EXCLUDED, Δχ² +68.7) is inherited unchanged by every derived route.

**Does H-EB remove the clumping excess without a deficit?** Not on any derived route: the excess (k = 1: +0.72 / +0.89) is untouched.

## Reported only (no verdict weight)

- **EB-η at its derived boundary** η_gal = 3.55e-6 / 2.73e-6 (the smallest η that keeps every halo ≤ 3e12 fully settled; one evaluation,
  no scan): settled fraction of B's amount 1.000 for galaxies, 0.26 at 1e13, 0.053 at 1e14, 0.015 at 1e15. T6 flips to a large DEFICIT,
  R(k=1) 0.225 / 0.271, R(k=0.3) 0.81 / 0.83, σ8 ratio 0.939 / 0.945 (frozen label "REDUCES", but it overshoots into a deficit). Clusters
  keeping 1.5% of their settled cold energy cannot meet X-COP or the Bullet unless the unsettled reservoir alone supplies the core mass
  (not derived for partial settling). Mass dependence is the right direction ("tensions sit in massive systems"), but the amplitude is
  one free constant and overshoots.
- **Local-reaction flag** (astra local_sink_reaction): a deposit held locally as vacuum energy needs a reaction force |∇(ρ_set e)|. At
  EB-L's outer binding radius that force is 0.7–65 × ρ g (rising with mass). EB-L as passive local absorption is therefore also
  inconsistent with local conservation unless the reaction is modelled.
- **MUTATE Mc as a knob probe:** a local cap 1000× tighter gets T6 near no excess (R(k=1) 0.87 / 0.97) but breaks SPARC (rms 0.364 /
  0.356), groups, X-COP and the Bullet. The local route binds inside-out (high g first), so any factor that reaches the clumping region has
  already emptied the galaxies.

## Checks and MUTATE

- S1a (frozen control) **FAILED as frozen**: the deep-limit deviation at y = 1e-4 is +5.0e-3. It equals the analytic next-order term
  +√y/2 exactly, so the tolerance (1e-3) was mis-specified, not the code. Disclosed post-freeze check at y = 1e-6: +5.0e-4, PASS (reported
  only). S1b PASS (peak 0.428 at y 23.9). S1c PASS (y(R=1) = 36.05).
- S2a/S2b PASS (sympy residual 0; dE/dt = 0). S2c PASS (binary endpoint).
- S3 / M∞ PASS: capacity → ∞ reproduces CFG624's SPARC rms, CFG634 B R0 and CFG637 B RD (T2, T3, T4) and CFG556's primary R(k) to 0.0e+00.
- M0 PASS: capacity 0 breaks galaxies (SPARC rms 0.397 / 0.397), groups go ABOVE (+0.81, Z 15), X-COP η 6.73, T6 R(k=1) 0.18 / 0.22.
- Mc PASS: the cap ×1e-3 moves T1, T2, T3 and T4 beyond tolerance (SPARC 0.364 / 0.356; X-COP 5.56 / 5.26).

## Verdict (frozen rule)

- EB-R: INERT (= candidate B; inherits CFG596 and CFG637 fails).
- EB-L (e_V and e_Φ): INERT (= candidate B at every gate; binds only in high-g cusps).
- EB-K: BINARY (exact Λ gives zero settling and breaks galaxies; any nonzero receiver motion settles everything = B).
- EB-η: KNOB (η_crit spread ×253–258).
- **H-EB is NOT DERIVABLE KNOB-FREE.** The framework's own energy budget is either far too large (rest energy) or exactly zero (receiver
  kinetic energy at w = −1), and its local version acts at the wrong radii. Settling's disposal is EXPORT, and an export receiver never
  fills: its capacity grows as it absorbs, and canonical waves carry the energy away (CFG542 K8). Energy disposal does not decide how much
  settles. The settled amount stays a supply/edge question, which is where CFG596, CFG637 and CFG593 already place the open problem.

Inherited (labelled): CFG556's halo ingredients (NFW shape for the unsettled shell, r200c, SHMR stars, Tinker HMF/bias) in D1/T6;
Δ_ta = 11.81; CFG634's per-scale supply conventions; point-mass interiors inside the first data point (SPARC, KiDS bound); no removal
inside 30 kpc for X-COP; e_Φ beyond the data uses flat-V (iso) extension to r_ta (upper bracket).
