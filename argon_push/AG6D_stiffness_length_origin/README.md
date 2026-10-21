# AG6D: can the stiffness length L* be derived?

## VERDICT: SCOPED NO-GO, within the 12 pre-declared mechanisms and the 210-formula menu

No mechanism fixes L* inside [24 pc, 1 kpc].
- Every forced evaluation misses by ≥ 7 dex.
- Every landing is numerology.
- The one mechanism-bearing landing (B8) fails both of its second predictions.

The lane closes one door outright, and that door is the one the question points at. The stiffness cannot be the cold
medium's own equation of state.
- Part A shows it would be exactly a Γ = 2 pressure.
- Part C1 shows that such a pressure in the free medium cuts the cold-energy power at k ≈ 1 Mpc⁻¹ for any L* ≥ 24 pc.
  The framework's own 1024³ initial conditions allow at most 0.25 pc.

L* therefore stays a bounded constant. It belongs either to the tethered state (a switch that is not yet written) or to
an independent light field. In both cases its value is unfixed.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (b94d6b89b), before any script existed.
- **Results:** NOT committed (lane rule).
- **Standing settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No particle species is added.
  Not "theory closed".

## Part A: the identity (`ag6d_identity.py`, IDENTITY HOLDS, longitudinal)
With ∇·P = ρ_c − ρ̄_c (PAPER49 §1), the stiffness on longitudinal P is the internal energy e = (γ/2)(ρ_c − ρ̄_c)² of the medium.
- That is a Γ = 2 (n = 1) polytrope measured from the cosmic mean: p = πG L*² ρ_c² where ρ_c ≫ ρ̄_c.
- c_s² = 2πG L*² ρ̄. This recovers CFG744's c_P relation.
- **The Jeans wavenumber is k_J = √2/L* at every density and epoch.**
- **A free, Newtonian self-gravitating clump has one radius for every mass:** R_TF = πL*/√2 = 2.221 L*, i.e. 53 pc–2.2 kpc.

| check | result |
|---|---|
| A1 | radial: vector Laplacian = ∇∇·P exactly (sympy); toroidal control: ∇·P = 0 but vector Laplacian ≠ 0 |
| A2 | energies agree to ≤ 1.2e-16 relative; the difference is the boundary term −8π r p² |
| A3 | γ_eff = e″(ρ̄) is constant only for Γ = 2. It spans 4 / 8 / 12 dex for Γ = 5/3, 4/3, 3, so Γ = 2 is unique for a constant L* |
| A4 | n = 1 first zero = π (3.5e-13), R_TF/L* = π/√2; n = 1.5 gives R ∝ M^−1/3 |
| MUTATE (Γ = 5/3) | L*_eff varies over 2 dex. Bites (exit 1) |

The identity turns "derive L*" into "derive the medium's two-body contact strength K_p = πG L*²". For a dilute condensate
that means a_s/m³ = G L*²/(2ħ²). Nothing in the record fixes it.

## Part B: candidates (`ag6d_candidates.py`; flags frozen before evaluation)

| id | formula | L* canonical / alt (pc) | class |
|---|---|---|---|
| B1 | c²/a0, the only length {a0, G, c} can make | 3.1e10 / 2.6e10 | MISS |
| B2 | Jeans at ρ_DE with c_s = c, κc²/(√(2π) a0) | 6.2e9 / 5.1e9 | NO-GO (forced, miss) |
| B3a–d | light-field Compton √2ħ/(m_P c), m_P from ħa0/c, ħH∞, the DE scale, 1 MeV | 4.4e10, 7.5e9, 4e-21, 9e-30 | NO-GO |
| B4 | contact condensate with a_s = Compton, 1 MeV | 1.1e-7 | NO-GO |
| B5 | healing length (MeV, 20–220 m/s) | 6e-24 – 7e-23 | NO-GO (k⁴ operator, coefficient ∝ 1/ρ) |
| B6a | √2 r_M(baryon Jeans mass at decoupling, 2.1e4 M☉) | 7.9 / 7.2 | MISS |
| **B6b** | √2 σ²/a0, σ = 8.23 km/s (10⁴ K, μ 1.22) | **33.1 / 27.4** | NUMEROLOGY |
| B6c | √2 r_M(CFG877 M_cl) (post hoc) | 125 / 103 | NUMEROLOGY |
| B7 | σ²/a0 at 10⁴ K | 23.4 / 19.4 | MISS (just below) |
| **B8** | (√2/π) R_TF, with R_TF from CFG870's core (identity + post hoc) | **56.8 / 56.8** | eligible → **fails C1 and C2** |
| B10 | MeV two-field compact object size | 3e-9 | MISS |
| B11 | ℓ_P^{1/n}(c²/a0)^{1−1/n}, n = 2–12 | n = 7: 46.6 / 39.6; n = 8: 591 / 500 | NUMEROLOGY |
| B12 | κⁿ c²/a0, n = 1–60 | n = 25–29 land (n = 30 canonical only) | NUMEROLOGY |

**Look-elsewhere.**
- 296 dimensionally valid formulas per footing: 15 named, 71 family members, 210 menu.
- The generic menu lands 5 of 210 (2.4%) on each footing: ℓ_P^{1/7}, ℓ_P^{1/8}, and λ_e, λ_p and λ_1MeV at power 1/5, each
  times (c²/a0)^{1−α}.
- Landings on both footings total 15 of 296 (5%).
- Because the window is 1.62 dex wide, landing is generic. B6b is CFG858's V_x² ≈ a0 × 31 pc coincidence again, through
  the H-cooling σ of CFG878.
- Raising the ceiling to 2 kpc adds only κ²⁴ c²/a0. No class changes.

**Controls.** K-B1 (planted 100 pc lands on both footings) PASS. MUTATE (√(G a0)/c) is rejected by the dimension checker,
and the run exits 1.

**Part D (scope).**
- A contact interaction at 1 MeV (ARGON10) needs a_s = 9.3e3 m, with n a_s³ ≈ 3e22 and σ/m ≈ 1e40 cm²/g. That is impossible.
- The allowed condensate band is:
  - L* = 24 pc: 1.5e-18 – 9.6e-3 eV;
  - L* = 1 kpc: 8.3e-22 – 4.8e-4 eV.
  - These limits use n a_s³ < 1, a Bullet-scale σ/m < 1 cm²/g (PROVISIONAL literature scale) and healing length < 0.1 L*.
- The light-field reading needs m_P c² = 3.8e-25 – 9.0e-27 eV. That is 8–9 dex above ħH∞ (1.2e-33 eV), so it is a new constant.
- A true condensate, without the record's mean subtraction, reaches interaction energy = rest energy at z = 7.0e5 / 5.9e4
  (24 pc / 1 kpc). A radiation-like completion would give ΔN_eff ≈ 0.03 / 0.37 (report only).

## Part C1: the identity's own second prediction, a cosmic cutoff (`ag6d_cutoff.py`, CONFLICT)
Free cold medium (CFG698 J3) carrying the stiffness, with linear growth computed from horizon entry to z = 49:

| L* (pc) | 24 | 50 | 100 | 300 | 1000 |
|---|---|---|---|---|---|
| k_1/2 (Mpc⁻¹) | 0.98 | 0.62 | 0.40 | 0.20 | 0.10 |
| M_1/2 (M☉) | 5.4e12 | 2.2e13 | 7.8e13 | 6.0e14 | 5.1e15 |

- Scaling: k_1/2 ≈ 0.98 (L*/24 pc)^−0.61 Mpc⁻¹.
- Robustness: the IC slope 0–2 gives 0.67–1.05 at 24 pc, and the causal cap c_s² ≤ c²/3 (post hoc) changes k_1/2 by ≤ 4%.
  DOP853 and Radau agree to 1e-11.
- The suppression comes from the radiation era. Pressure halts the Meszaros coasting from horizon entry until the mode
  turns Jeans-unstable at a = L*k/√2.

**L*_IC.**
- The frozen scan gives < 1 pc (its grid floor) for every IC slope and for the cap variant.
- The post-hoc refinement (uncapped, IC slope 1) gives **0.25 pc**, 97× below the globular floor.
- Frozen class: **CONFLICT.** The identity plus L* ≥ 24 pc contradicts the CDM-like initial conditions of the 1024³ shear
  runs (Nyquist 16.08 h/Mpc).

**Post hoc, framework-native spectrum (CFG654 `Plin0`), at 24 pc:**
- σ8 −0.3%;
- σ(1 Mpc/h) −20%;
- σ(0.5 Mpc/h) −33%.
- At 1 kpc, σ8 falls 41%.

**Escape.** The stiffness must not act on the free medium before z ≈ 3.7e3 (24 pc) or 1.4e3 (57 pc).
- K1, K2 (Meszaros to 8.5e-12): PASS.
- MUTATE (γ = 0) flips the class to NO CONFLICT. Bites.

## Part C2: one universal clump radius (`ag6d_dwarf_link.py`, INCONSISTENT on both footings)
- **The group is consistent.** CFG870, CFG871 and CFG877 imply L* = 56.8–106.7 pc (×1.6–1.9).
- **Sextans is not.** Sextans MP needs R ≥ 1.7 kpc, so L* ≥ 765 pc: ×7.2 canonical, ×8.3 alt above the group.
- **Supply fails at that radius.** A 1.7 kpc clump at ρ0 = 0.58 M☉/pc³ weighs 3.6e9 M☉, which exceeds 53.64 M_b for every
  M_b ≤ 1e7 M☉.
- The universal-radius reading is compatible with CFG880's non-universal σ, but not with Sextans (CFG884, PROVISIONAL
  extraction).
- B8 also needs free cold energy with Newtonian self-gravity. That is the class-A hybrid; the canonical action cancels it
  (CFG888).
- MUTATE (Sextans set to the group R) flips the class to CONSISTENT. Bites.

## Disclosures
- **ag6d_identity.py first run exited 1.** Two supplementary float thresholds (1e-20) that are not in the frozen lines were
  set too tight. They were set to 1e-12 and no frozen line changed.
- **Post hoc:** the cap variant, P1–P4 in `ag6d_cutoff_posthoc.py`, and the light-field mass line.
- **Small inconsistency:** P3 converts h/Mpc with h 0.677 against the table's 0.674 (0.4%).
- **Design-stage mental estimates** are listed in the criteria §1.
- **Run cost:** each run took < 30 s at 70–116 MB RSS, single thread, beside the live 1024³ run.

## Not verified
- Whether PAPER49's stiffness acts on the free medium. The action has no switch on it; the record does not say.
- The Newtonian c_s > c regime at z ≳ 6e4–7e5. It is handled only by the post-hoc cap.
- The transverse (curl) stiffness that CFG770's Cassini numbers used. The fluid reading has none, and this was not re-run.
- The KiDS shear impact of the cutoff. That needs a 1024³ rerun with cut initial conditions (heavy; not run or queued).
- The Bullet σ/m scale and the Sextans extraction (both PROVISIONAL).

Overlaps cited: CFG691 (L*² = 2 r_M ℓ_γ), CFG698 (J3), CFG744 (c_P), CFG820/821, CFG832, CFG858, CFG870/871/877/878/880/884/888, ARGON10.
