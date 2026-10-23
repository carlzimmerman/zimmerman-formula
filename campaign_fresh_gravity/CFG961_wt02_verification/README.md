# CFG961: independent check of WT-02 and WT-05 against CFG938 and PAPER57

## Plain summary

WT-02 is right that CFG938's covariant parent breaks down whenever the cold medium expands or contracts. The term that lets the
cosmic background absorb the mean density turns the tether pair into a forward and a backward heat equation, whose small-scale
modes grow at a rate c²k²/(3|H|). This is a real defect, not a bookkeeping artefact of a Lagrange multiplier: the growing mode
pushes the medium and bends the metric, and in full general relativity the offending equation follows from Einstein's own
equations. WT-02 is also right that gravitational waves do not travel exactly at c in this parent, but its GW170817 margin is too
generous: the hidden cosmic clock χ̄(t) contributes along the whole path and caps L* at about 1.0 kpc (not 16–33 kpc). PAPER57's
"linear well-posedness" therefore holds only for static media and needs a v1.1 correction; drafts are in this folder.

## Status

- **Lane.** Block CFG960–969, reserved for this check in the LEDGER (89bccf7d3).
- **Criteria.** `FROZEN_CRITERIA.md` (**83b04219e**), committed alone before any script.
- **Amendment A1** (`AMENDMENT_A1.md`, **f3cbd85e5**). Post hoc relative to scratch development runs, committed alone before
  the graded run. It adds the full-GR scalar sector because the frozen quasi-static gravity model mis-models the fast modes.
- **Settings.**
  - κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled.
  - Cold energy is gravitating mass; no particle species.
  - Not "theory closed". Nothing here says the data favour the framework.
- **Independence.**
  - No WT-02, WT-05, WT-06–09 or CFG938 code was imported, copied or run.
  - Inputs read: CFG938's action (DERIVATION §3.4) and printed numbers; the record SPARC file for NGC 3198 (Υ = 0.61);
    CFG4_common footings; LEDGER line 38 (h72 bounds).
  - No downloads. No other lane's file was edited.
- **Main run.** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg961.py` → `cfg961.out`, `cfg961_results.json`.
  - 137 s, peak RSS 0.28 GB (`/usr/bin/time -l`). Exit 0.
  - All checks pass except K_a1_quasi_static, which fails for the reason A1 gives.
- **MUTATE run.** `CFG961_MUTATE=1 …` → `cfg961_MUTATE.out`, `cfg961_results_MUTATE.json`.
  - 41 s, 0.20 GB. Exit 2: four of five teeth bite fully, and MU1 bites only partly (below).
- **Scratch development runs** (outside this folder) came before the graded runs and are disclosed in A1. The graded outputs come
  from the committed script bytes.

## What the newer record already settles (read before this lane was finished)

- **sol61 cold-covariant audit** (`sol61_push/cold_covariant_audit_2026_10_20/RESULT.md`, in the repo at a67f9ed9c, 2026-10-20,
  before WT-02).
  - It had already refuted A5 through the FRW tensor coefficient Q_T = 1 − 3γχ̇²/K.
  - It found Q_T < 0 at BBN if the medium exists then.
  - This lane reproduces both (Q_T(z = 4e8) = −1325.41 / −2.3028e6 against the audit's −1325.42 / −2.3028e6). WT-02's GW170817
    path model omitted this term.
- **WT-06** (449576b33, committed) uses WT-02's FRW smear as an input. It does not test it.
- **WT-07, WT-08 and WT-09** have committed frozen criteria only (ed636472e, 1bf29e407, 8812ac047), with no committed results:
  - WT-08 will build the intrinsic-Laplacian repair (this lane's MU2);
  - WT-09 will classify c_T = c stiffness terms. Its hand expectation, δ(c_T²) ∝ u² + C² + 2uC cos θ, matches this lane's result.
  - Nothing there settles a WT-02 claim yet.
- **THEORY_V3_DRAFT** (H4 9fe0dcb5b, I1, V1 03174c72a; V1_DENSITY_SCREEN 0429deb41). These concern the v3/v4 covariant forms,
  whose γ_L stiffness makes them ill-posed somewhere: v3 where ρ_τ < 0, v4 where the aether twists. They are different actions and
  different defects. They do not test CFG938's FRW constraint, and PAPER57's statement is about CFG938.

## Results

| claim | class | key numbers |
|---|---|---|
| **(a)** CFG938's parent is ill-posed off static backgrounds | **CONFIRMED, physical (not multiplier-only).** Frozen rule: UNDERDETERMINED. A1 as written: UNDERDETERMINED (one rank-test point) | see (a) below |
| **(b1)** A5 "c_T = c (structural)" is wrong | **CONFIRMED** | δ(c_T²/c²) = (3/2)L*²[u_⊥² + (u_∥ + ∂₀χ)²]/c⁴ |
| **(b2)** c_T − c = 0.75 L*²u²/c⁴ | **CONFIRMED** | coefficient 3/2 for every angle and polarisation |
| **(b3)** GW170817 passes on the path average | **passes for L* ∈ [24 pc, 1 kpc]; WT-02's margin NOT CONFIRMED** | see (b3) below |
| local limit at L* ≈ 1 kpc | **CONFIRMED** | wall: 0.951 / 0.787 kpc (can/alt) |
| **(c)** χ̄(t) is a hidden cosmic clock | **CONFIRMED** | see (c) below |
| **WT-05 vs CFG955 / CFG958** | **CONSISTENT; no recorded class changes** | see below |

**(a) Key numbers.**
- Fast root σ = c²k²/(3|H|) to 1e-9 at the top k, in gravity-off and full GR, at z = 0 and 10, for H > 0 and H < 0, at both L* ends.
- χ is forward-parabolic and λ backward-parabolic for H > 0; for H < 0 the roles swap.
- Max Re σ/|H| = 1.1e16 at c/k = 24 pc (z = 0).

**(b3) Key numbers.**
- Full path average (cosmic clock |∂₀χ̄| = cΩ_cH/2 = 8.66e-11 m/s², plus two galaxies): 3.9e-19 (24 pc) to 6.8e-16 (1 kpc).
- L*_max = 1.015 kpc, not 16–33 kpc.
- With the measured distance, the line is 3.9e-16 and L*_max = 0.76 kpc (no class weight).

**(c) Key numbers.**
- u_v = (Ω_cH₀/2)v = 2.888e-19 s⁻¹ × v. At 370 km/s that is 1.142e-3 a₀ (canonical) and 9.45e-4 a₀ (alt).
- NOT VISIBLE in SPARC, wide binaries or the Solar System.
- KiDS tail ends: UNDERDETERMINED (r_×/r_end 2.4–4.1 at 370 km/s; ≤ 1 only for lenses moving ≳ 1000 km/s).
- It already enters two recorded quantities: CFG941's growth inertia (1 − Ω_c/6) and c_T (b3).

**WT-05 vs CFG955 / CFG958.**
- **CFG955.** WT-05's statements match CFG955's L7 (T_J bath) and PH4 (Bonnor–Ebert / Antonov collapse). The isothermal
  thresholds 32.13 / 708.6 are reproduced.
- **CFG958.**
  - Its T-S PASS (S1–S3, SCT) is untouched.
  - Its V2 bracket "class-A drift admissible" holds only for the GENERIC entropy. With the Boltzmann entropy, dS/dt = ∫f ∇·v_s < 0
    for deficit filling.
  - So that bracket needs the qualifier, but the class is unchanged.

**Why (a) reads UNDERDETERMINED by the rules.**
- **Frozen rule.** The frozen primary gravity model (quasi-static Φ = Ψ) mis-models modes that evolve faster than ck:
  - its fast root falls to 0.25 (z = 0) and 0.08 (z = 10) of c²k²/3H at kL* ≫ 1, with L* = 1 kpc;
  - K-a1 fails for it.

  The gravity-off system, which is exact for the matter sector's principal part, gives σ = c²k²/3H exactly.
- **A1 as written.** A1 replaces the quasi-static model with the full GR scalar sector. There, one rank-test point fails its
  literal line: z = 10, c/k = 1 Mpc, s_min 2.3e-5 against 1e-6. That residual is 1.11 (H/ck)², the frozen-coefficient error. At
  c/k = 24 pc the same test gives 1.4e-14.
- **Substantive reading.** Every computed system that is valid for these modes shows the same unbounded root. The substantive
  reading is therefore CONFIRMED. It carries no frozen-rule weight, and it is stated as such.

## Multiplier vs physical

The multiplier reading fails on four counts:
1. **λ is χ's conjugate momentum on FRW.** The quadratic action has −(3a²ȧ/c)δλ∂_tδχ, and the Dirac constraints are second
   class. One degree of freedom appears that is absent at θ = 0, and its Hamiltonian is linear in p_χ.
2. **The growing mode moves physical fields.**
   - The medium's acceleration equals the full λ force: |σ²ξ| = 1.046 (gravity off) and 1.049 (full GR) × |k·Kδλ|.
   - The Bardeen potential is Φ = 0.397 (H/ck)² Kδλ.
   - The control MU5 (λ decoupled from the medium, gravity off) gives a pure-λ eigenvector. So the test can tell the two cases
     apart.
3. **In full GR the λ equation is an Einstein equation.** Dropping it keeps the fast root as long as the Hamiltonian constraint and
   the trace-ij equation are kept. Dropping it together with either one loses the root. This is the contracted Bianchi identity
   with χ̄̇ ≠ 0.
4. **Posing λ with final data changes the theory.** The result is a teleological two-point problem: the anticipation is
   3|H|/(c²k²), i.e. 0.22 yr at 10 kpc and 2.2e3 yr at 1 Mpc. By item 3 the metric would need final data too.

## Controls

| check | result |
|---|---|
| Tadpoles (all three gravity models) | vanish with Friedmann and S1d |
| K-a1, gravity off | PASS: degree drops at H = 0; fast roots ±c²k²/3H leave to infinity (singular limit); static u₀ = 0 roots recovered |
| K-a1, quasi-static | FAIL (A1.1) |
| K-a2 (CFG938 S5a + inertia) | PASS, symbolic |
| K-a3 (slip, 10 rows) | PASS: all rows within 0.3%; worst 5.792e-6 |
| K-a4 (NGC 3198 law) | PASS: 2.2e-16 both footings; θ ≡ 0 for static media |
| K-b0 (EH normalisation) | PASS |
| b2 (coefficient 3/2) | PASS |
| exact FRW τ_ij = −(a²/2)∂₀h_ij ∂₀χ̄ | PASS |
| D1 (drift entropy identity) | PASS |
| D2 (isothermal thresholds) | PASS |

**MUTATE.**
- **MU2** (intrinsic Laplacian): WELL-POSED (roots ≤ 3.02|H|), but S1d fails without an explicit ρ̄ subtraction. Bites.
- **MU3** (no Christoffel in τ): c_T = c. Bites.
- **MU4** (no clock): the path average drops to galaxies only, ≤ 2.3e-18. Bites.
- **MU5** (multiplier-only control): MULTIPLIER-ONLY. Bites.
- **MU1** (sign of −θu·∂χ flipped): bites only partly.
  - The forward/backward labels swap, and the system is ILL-POSED at z = 0 for both signs of H.
  - At z = 10, L* = 1 kpc it reads UNRESOLVED. The flipped operator keeps a medium-tilt coupling 2χ̄̇δθ that the original lacks, and
    at kL* ≫ 1 this turns the fast root oscillatory.
  - The frozen tooth therefore does not fully bite. This is reported, not repaired.

## Files

- `DERIVATION.md`: equations, tables and classes.
- `cfg961.py`: the one script.
- Outputs: `cfg961.out`, `cfg961_results.json`, `cfg961_MUTATE.out`, `cfg961_results_MUTATE.json`.
- `CORRECTION_PAPER57_v1.1_DRAFT.md`: the dated "Correction (v1.1)" box and line replacements for lines 18, 24, 51, 54, 165, 206
  and 213.
- `CORRECTION_CANONICAL_DRAFT.md`: a note for THEORY_CANONICAL (2026-10-18 note; v4 draft §3.6 and obligation 9).

None of the paper, canonical, LEDGER or what_is_time files is edited.

## Caveats

1. **Frozen coefficients, linear order, sub-horizon.**
   - The growth rate ≫ H justifies frozen coefficients for the fast modes. Their e-fold time at c/k = 1 kpc is about 1 day, at
     1 Mpc about 2e3 yr.
   - Nonlinear behaviour, shell crossing and inhomogeneous backgrounds are not computed.
2. **The full-GR system is gauge-fixed after variation** (Newtonian gauge). Roots are accepted through the 8 × 6 rank test, and
   only at the frozen-coefficient precision (H/ck)².
3. **The GW170817 path uses the background clock rate.** Inhomogeneity along the path is not modelled. Linear theory makes the
   rate uniform on sub-horizon scales, because χ diffuses with D = c²/3H.
4. **Early-universe Q_T < 0** applies only if the medium exists then. It is quoted from, and reproduced against, the sol61 audit.
