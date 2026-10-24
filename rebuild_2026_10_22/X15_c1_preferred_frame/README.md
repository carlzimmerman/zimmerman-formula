# X15_c1_preferred_frame: does C1, inside its X14 window, survive the preferred-frame PPN bounds, and does it leave galaxy statics and dynamics intact in v3s?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` + `LITERATURE_MAP.md` (87867a70a4, committed alone before any script or
number). Amendments A1 (PRE-RESULT implementation) and A2 (POST-RESULT, MUTATE-path check code only), below. Launched from
X14's "What this does not show" (C1's preferred-frame PPN and galaxy dynamics were not checked).
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". The only
data used are published PPN bounds as transcribed in the record; nothing here says the data favour the framework.

## Verdict: C1 SURVIVES PPN (the whole X14 window, both footings, both μ_K)

- **At PPN order C1 adds no preferred-frame effect.** On the screened Solar-System branch, α₁,∞ = 0 and α₂,∞ = 0 exactly,
  for every β > 0 (`PPN_order`; checks P-A1, P-A2).
- **The non-PPN residuals are far below every bound.** They are set by L★, not by β. The worst values over the
  μ_K = 0.1 windows (`worst_alpha_eq`) are listed below, against the bounds transcribed in DOOR11.

  | quantity | test radius | canonical | alt | bound |
  |---|---|---|---|---|
  | α₁-equivalent | 30 AU | 3.60e-10 | 3.24e-10 | 1e-4 |
  | α₂-equivalent | 30 AU | 2.25e-11 | 2.03e-11 | 2.4e-7 |
  | α̂₁ proxy | binary J1738 | 5.35e-17 | 4.82e-17 | 2.1e-5 |
  | α̂₂ proxy | NS radius | 1.61e-28 | 1.45e-28 | 1.6e-9 |

  The two strong-field rows are weak-field proxies (FROZEN §2).
- **The surviving window equals X14's window** (41/41 grid points in every cell, `surviving_windows`):
  - canonical: β ∈ [1.9935e-6, 1.0049e-5] at μ_K = 0.1 Mpc⁻¹, and up to 1.1168e-4 at μ_K = 0.03;
  - alt: β ∈ [2.1976e-6, 1.0049e-5] at μ_K = 0.1, and up to 1.1168e-4 at μ_K = 0.03.
- **PPN neither closes nor narrows C1's window.** No relation between constants is needed.
- **Galaxy statics and dynamics (step 3, reported, no verdict weight): intact only while subsonic.**
  - Where a galaxy moves subsonically through the khronon, its rotation curve shifts by ≤ 0.023 dex (β_min) and
    ≤ 0.036 / 0.041 dex (β_max at μ_K = 0.1) at 10–100 kpc.
  - Subsonic is not guaranteed. At μ_K = 0.1 a CMB-dipole speed (369 km/s) is Mach 0.48–2.2 at the top of the window
    and up to 4.9 at the bottom, in galaxy outskirts. There the linear estimate fails and X14's caustic cure (FT-COND)
    does not apply.
  - See "Step 3" below.

## Step 0: reproductions (stop rule; all pass)

| check | result |
|---|---|
| **S0-1** A22's own script | `a22_checks.py` (sha256 f20cf27b…ff95) was run read-only, with its JSON redirected into this lane. It exits 0 with 13/13 PASS and `alpha1_ppn_order = alpha2_ppn_order = 0` (`a22_rerun.out`, `a22_rerun.json`). |
| **S0-2** X14's window | Recomputed from X14's copied formulas: β_min = 1.993547e-6 (canonical), 2.197554e-6 (alt); β_max = 1.004925e-5 (μ_K = 0.1), 1.116754e-4 (μ_K = 0.03). Maximum relative difference from X14's JSON is 0.0. |
| **S0-3** this lane's system ↔ X3/X14 | The quadratic unitary-gauge action of FROZEN §1 has exactly one scalar root, ω² = βk²(L★²k² + 2M − 2)/(2(3β + 2)) on Θ = 1 and βk²(M − 1)/(3β + 2) on Θ = 0. That is X14's (Bk²/K)(k²/χ − K) at ρ_τ = 0, with B = β/(2 + 3β), residual 0. So X3 E2's "ESTIMATE" factor 2 + 3β is the exact khronometric scalar speed. |
| **S0-4** GR control | With the P sector removed and β = 0: α₁ = α₂ = 0 and U_N = KM/k². The gauge-invariant combinations Ñ_x and Φ_inv = ñ − (Ω/k)Ñ_z do not contain the free gauge amplitude. |
| **S0-5** A22 at β = 0 | The static source gives n = ψ = −(KM/k²)(1 + 2/(L★²k²)), which is A22 eq. 8, Φ = Ψ = −GM/r + (GM/L★²)r (residual 0). The moving source at β = 0 gives PPN-order α₁ = α₂ = 0. |

**What S0-5 also shows (reported, not gated): at β = 0 the moving-source linear solution does not carry the hedgehog.**
- For any w with k·w ≠ 0, the β = 0 solution is GR with the bare G. Its Fourier potential is U_N = KM/k², with no
  (1 + 2/(L★²k²)) factor, and α₁(k) = α₂(k) = 0 at every k (`S0_5.moving_beta0`).
- For every β > 0 the static hedgehog is carried: U_N = KM(L★²k² + 2)/(L★²k⁴) (`D.U_N_k`).
- So the limits β → 0⁺ and w → 0 do not commute. At β = 0 the linear khronon has zero longitudinal stiffness, so it
  cannot move the Sun's charge.
- Consequence: A22's a_P = GM/L★² and C8 K8's (w·n̂)² anisotropy hold for a Sun **at rest in the khronon frame**. For the
  real, moving Sun at β = 0 they are open; the nonlinear charge transport this lane does not solve decides.
- Cassini passes either way, because both GR and the hedgehog pass.

## Step 1: the derivation (sympy, `D`, `X_BPS`, `PPN_order`, `residual_coeffs`)

The setup (FROZEN §1):
- v3s linearised about Minkowski, with the khronon at rest, in its unitary gauge. Screened branch: M = 1, since u/a₀ is
  about 2.6e-6, and Θ = 1, since D·P > 0.
- Source: a point mass moving at w = (w_x, 0, w_z) relative to the khronon. Wavevector k along z.
- Extraction from the gauge invariants Ñ_x and Φ_inv.

With η(k) ≡ 2/(1 + L★²k²/2), which is P integrated out:

    α₁(k) = −16/(L★²k² + 2) = −4η(k)                                         (D1; α₁ + 4η = 0)
    α₂(k) = 2(4 + 6β − βL★²k²)/(βL★²k²(L★²k² + 2)) = η(η(1 + 2β) − β)/(β(2 − η))   (D2; residual 0)
    γ(k) = 1 (static),   U_N(k) = KM(L★²k² + 2)/(L★²k⁴)

- **Cross-checks (X-BPS):**
  - At leading order in small (η, β), these equal BPS 2011 Eq. 91, α₁ = −4α and α₂ = α(α − λ′)/(2λ′), with α_BPS = η,
    β_BPS = 0 and λ′ = β (residual 0; PROVISIONAL source).
  - Exactly, α₂ equals the record's Einstein-aether c₁₃ = 0 formula c₁₄(c₁₄ + 2c₂c₁₄ − c₂)/[c₂(2 − c₁₄)], at c₁₄ = η(k)
    and c₂ = β (residual 0).
  - So v3s + C1, screened and linear, is khronometric with a scale-dependent a² coefficient η(k) and Hořava λ = 1 + β.
    Note the name clash: the record's β is BPS's λ′.
- **PPN order.** α₁,∞ = α₂,∞ = 0, because η → 0 as kL★ → ∞. The stiffness is load-bearing (MUTATE m2).
  - α₁ is β-independent at every k. It comes from G_N(k) ≠ G: the Newtonian potential carries the hedgehog, the
    transverse g_0i does not.
  - C1 enters only α₂, through the 1/β terms.
- **Residuals.** In powers of u = (L★k)⁻²:
  - α₁: 0, −16u, 32u², −64u³;
  - α₂: 0, −2u, (16 + 8/β)u², −(32 + 16/β)u³.

  Mapped to position space with the exact transforms of 1/k²ⁿ, the leading terms are α₁^eq ≈ 8(r/L★)² and
  α₂^eq ≈ (r/L★)²/2. The 1/β term enters only at (r/L★)⁴/β and is negligible across the window. Values: α₁^eq = 4.00e-13
  (canonical) / 3.60e-13 (alt) at 1 AU, and 2.64e-18 / 2.38e-18 Earth–Moon.
- **Linear validity (P-LIN).** C1 dominates the khronon's charge transport, B/(Kρ_τr²) ≥ 3.3e13, at every test radius
  for every scored β. The khronon is far from sonic: c_S(1/r) ≥ 3.2e10 m/s at 30 AU at β_min (canonical).
  - New fact: with C1, the khronon on the stiff side is a **propagating, superluminal, dispersive scalar** at
    Solar-System scales, ω² ≈ (Bγ_L/K)k⁴.
  - At β = 0 there is no such mode (C8: "no radiative channel").
- **Unscreened branch (reported; not PPN, the field is not 1/r):** Θ = 0, M = M_θ ∈ [1 + x, (1 + x)²] at X14's fold radii.
  - α₁ = −8/M_θ ∈ [−7.53, −1.51] (canonical) and [−7.57, −1.74] (alt).
  - α₂ = (2 + 4β − M_θβ)/(M_θβ(M_θ − 1)) ∈ [8.7e3, 1.5e7] (canonical) and [1.2e4, 1.5e7] (alt).
  - The O(w²) frame-dependence α₂(w/c)² reaches 0.82 / 0.83 at w = 70 km/s and 22.9 / 23.0 at 369 km/s. In galaxy
    outskirts the khronon wind is an O(1) effect near Mach 1, which is step 3's question.

## Step 3 (reported only, ESTIMATES; no verdict weight)

**(3a) Mach numbers w/c_A** (`T3a_mach`):
- c_A is X14's khronon speed at its five fold radii, read at β_max(0.1) and scaled. The speeds are illustrative.
- In the table, cells read canonical / alt, and each Mach entry is the range over the fold radii.

| β | c_A (km/s) | w = 70 | 220 | 369 | 600 | 1000 |
|---|---|---|---|---|---|---|
| β_min | 75–342 / 75–336 | 0.20–0.94 / 0.21–0.94 | 0.64–2.94 / 0.65–2.94 | 1.08–4.93 / 1.10–4.93 | 1.76–8.02 / 1.78–8.02 | 2.93–13.4 / 2.97–13.4 |
| β_max(0.1) | 168–768 / 160–719 | 0.09–0.42 / 0.10–0.44 | 0.29–1.31 / 0.31–1.38 | 0.48–2.20 / 0.51–2.31 | 0.78–3.57 / 0.83–3.75 | 1.30–5.95 / 1.39–6.25 |
| β_max(0.03) | 560–2558 / 533–2397 | 0.03–0.13 | 0.09–0.39 / 0.09–0.41 | 0.14–0.66 / 0.15–0.69 | 0.23–1.07 / 0.25–1.13 | 0.39–1.79 / 0.42–1.88 |

- The X8/X10 regime (about 70 km/s) is subsonic across the window, by X14's construction.
- A Sun-like speed relative to a Galaxy-static khronon (220 km/s) or a CMB-dipole speed is supersonic in outskirts at
  μ_K = 0.1. At μ_K = 0.03 with β near its top, only cluster-like speeds (≥ 600–1000 km/s) are.

**(3b) Rotation curve of a galaxy moving through the khronon** (`T3b_rotation`; **S3-1** passes).
- **Derived from the 3D PN Lagrangian (X3 L1 in 3D) + C1:**
  - the σ equation is ∂_tρ_τ + ∇·(ρ_τv) + (B/K)∇⁴σ = 0;
  - the O(w) steady equation is −w·∇ρ_τ − ∇·(ρ_τ∇δσ) + (B/K)∇⁴δσ = 0;
  - δσ = −w·x (fully held) is an exact particular solution for any ρ_τ and B;
  - on a ρ_τ ∝ r⁻² phantom, the ℓ = 1 indicial polynomial is R p(p−1)(p+2)(p−3) = (p−2)(p+1), with R = B/(Kρ_τr²)
    (all residual 0).
- **Streaming exponent p₁:**
  - 2 at β = 0: the khronon is held, and the relative flow falls as r/R_h;
  - 1.08–1.09 at β_min;
  - 1.018–1.022 at β_max(0.1);
  - 1.002 at β_max(0.03).
  - So C1 makes the khronon stream through the galaxy rather than be held. The galaxy's charge is carried by C1's current.
- **The estimate.** δ ln g ≈ (dg/dg_N − 1)(p₁ − 1)(p₁² + 2)/3 (w/v_c)²(r/R_h)^(2(p₁−1)), for the 6e10 M☉ AQUAL point mass
  at r = 10, 30 and 100 kpc and R_h = 1 and 10 Mpc.
- **Subsonic cells (w below the local c_A):**
  - maximum shift 0.023 dex at β_min, 0.036 / 0.041 at β_max(0.1), and 0.047 / 0.052 at β_max(0.03);
  - the only subsonic cell above 0.05 dex is alt, β_max(0.03), w = 600 km/s at 100 kpc (0.052).
- **Supersonic cells** are flagged and not estimated. Their linear extrapolation would range from 0.007 to 4.7 dex.
- **At β = 0 every cell is supersonic** (c_A = 0), which is X8/X10's caustic regime.

**(3c) Cherenkov / supersonic drag** (`T3c_cherenkov`; Ostriker-form bound, LITERATURE_MAP L4). For a 6e10 M☉ galaxy:
- In the cosmic khronon dust (ρ ≤ ρ_crit = 8.48e-27 kg/m³): t_drag/t_H ≥ 1.8e3 at 600 km/s and 8.35e3 at 1000 km/s.
  It does not matter.
- In a 1e14 M☉ (baryons) cluster's phantom at 300 kpc (1.30e-23 / 1.47e-23 kg/m³): t_drag/t_H = 1.17 / 1.04 at 600 km/s
  and 5.43 / 4.81 at 1000 km/s.
  - This applies only where the motion is supersonic. The cluster's c_A there is 459 / 449 km/s at β_min and
    1032 / 960 km/s at β_max(0.1).
  - At β_max(0.1), members at ≤ 960 km/s do not radiate. At β_min they do, with a drag time about the Hubble time.
- That drag is ordinary dynamical friction on the khronon charge. It is present for all motion at β = 0. C1 only switches
  it off below c_A.

## Checks (`x15_c1_preferred_frame.out`, `_results.json`)

- **Main run: 13/13 PASS, exit 0.** The checks are S0-1 to S0-5, D1, D2, X-BPS, P-A1, P-A2, P-LIN, P-RES and S3-1.
  - 3–4 s, peak RSS 0.097 GB, one thread, nice 15, PYTHONHASHSEED=0.
  - A rerun is identical.
- **MUTATE (`X15_MUTATE=1`): exit 1, and every required failure bites.**

  | mutation | change | fails |
  |---|---|---|
  | m5 | A22's own `--mutate alpha1_forced` | S0-1 (12/13) |
  | m4 | H₀ doubled in β_max | S0-2 (rel diff 3.0) |
  | m1 | C1's sign flipped (2 − 3β) | S0-3 |
  | m3 | matter current dropped | S0-4 (no solution: momentum not conserved) |
  | m2 | stiffness removed in the screened system | P-A1 |

  - Also failing: D1, D2, X-BPS, P-A2 and P-RES. The MUTATE verdict line (UNDECIDED) is the control's output, not physics.

## Amendments and execution history

- **87867a70a4:** criteria, ledger and literature map, committed alone.
- **A1 (PRE-RESULT implementation, before any run).**
  - The source normalisation was made exact (M/√(1 − w²), as frozen).
  - The 3b indicial polynomial is now evaluated at two points instead of one.
  - The drag acceleration had a stray 1/G; it is now 4πG·GM·ρ lnΛ/w².
  - A loop variable that shadowed the mass symbol was renamed.
- **A2 (POST-RESULT, MUTATE-path check code only).**
  - The first MUTATE run crashed after S0-3.
    - m3 leaves the GR system with no solution. S0-4 now records "no solution" as a failure.
    - m2 makes the extraction direction-dependent. At Θ = 0 and M = 1, η = 2 and the system is degenerate (zero khronon
      stiffness, G_N → ∞). The residual evaluator now treats a non-numeric or nan coefficient as an infinite residual.
  - The main run is unchanged by A2. The development main run and the scored run have identical `.out` files (apart from
    RSS) and all 3713 shared JSON leaves equal. The only change is a new key, `S0_4.solution_exists`.
  - FROZEN §7's parenthetical expectation "(α₁,∞ = −8)" for m2 was wrong. The degenerate system gives
    α₁,∞ = −24β(a² + b²)/(…), which depends on direction. P-A1 still fails, as required.

## What this does not show

- **Weak field and linear only.** The strong-field α̂₁ and α̂₂ rows use the weak-field residual at the binary separation
  and at the NS radius. No neutron-star sensitivity is computed. No second post-Newtonian order (β_PPN, ξ) is computed.
- **The PPN identification assumes ζᵢ = ξ = α₃ = 0** (standard for aether/khronon theories; LITERATURE_MAP L2). The GR
  control validates the extraction only for GR.
- **The β = 0 moving Sun is not solved.** Linear theory says its hedgehog is not carried. The nonlinear charge transport
  (the Sun's own charge gives a local sound speed c₀ = √(γ_Lρ_τ) = √(GM/r), the local circular speed, against the
  illustrative w ≥ 220 km/s) is not solved.
- **Binary-pulsar radiation with C1 is not computed.**
  - C1 turns the khronon into a propagating scalar, so khronometric-type scalar (dipole) radiation is possible. In the
    screened regime it is suppressed by η(k).
  - C8's "no radiative channel" holds only at β = 0.
  - The stiff-side k⁴ mode is well posed only on khronon-orthogonal slices (cf. I1's v4 result). v3s has such slices;
    this was not checked here.
- **Step 3 is an estimate.**
  - The self-similar exponent is applied at 10–30 kpc, where the phantom is not yet ∝ r⁻².
  - R_h and the matching amplitude are O(1)-uncertain.
  - Only the O(w) khronon response is solved, not the O(w²) charge response.
  - The supersonic cells are not estimable.
  - The khronon's local rest frame relative to galaxies (the cosmic dust frame, or held halos) is not fixed by the record.
    The speeds are illustrative.
- **X14's caveats on C1 remain:**
  - its caustic cure is linear and subsonic only;
  - the upper window edge rests on C5's IR-band estimate;
  - the literature's ghost/gradient-instability warning for this class still stands.
- **Literature look-ups are PROVISIONAL.** BPS Eq. 91 comes from a summarising fetch. The exact agreement with the
  record's aether c₁₃ = 0 formula is the stronger cross-check.

## Suggested fixes elsewhere (not edited here)

- **A22 (`deepseek_push/DS_FINAL_2026_10_21/A22_ppn_frames/report.md` D2, `a22_checks.py` K5).**
  - The claim that "θ² has no linearised stress" is a statement about the background (d(θ²)/dh at h = 0), not about the
    linear response. It does not establish α₁ = α₂ = 0 "for every β_ADM".
  - The correct statement, from X15: α₁,∞ = α₂,∞ = 0 for every β > 0. The exact k-dependence is α₁(k) = −4η(k) and
    α₂(k) = η(η(1+2β) − β)/(β(2 − η)).
  - Also qualify a_P and D5: they hold for a Sun at rest in the khronon frame. At β = 0 the linear moving-source solution
    carries no hedgehog.
- **C8_instantaneous README, K7/K8.** "No radiative channel" holds at β = 0 only. K8's anisotropy also assumes the
  hedgehog is carried, which holds for β > 0 but not, in linear theory, at β = 0.
- **X14 README, "What this does not show" (C1).** Add:

  > Preferred-frame PPN: checked in X15. PPN-order α₁ = α₂ = 0. Residuals are ≤ 3.6e-10 (α₁) and ≤ 2.3e-11 (α₂) at
  > 30 AU. The window is unchanged.

  Also record the open galaxy-dynamics condition: the cure needs w < c_A, and c_A is 160–770 km/s at β_max(0.1).
- **V3_FULL_PICTURE §6.** Add, for any C1 adoption: a moving system is cured and statics-preserving (≤ 0.041 dex at
  μ_K = 0.1 in this estimate) only when subsonic relative to its local khronon. CMB-dipole-like speeds are supersonic in
  galaxy outskirts at μ_K = 0.1. The khronon's rest frame relative to galaxies decides this, and it is not fixed in the
  record.
- **X3 README E2.** The factor B = βc²/(2 + 3β), labelled an ESTIMATE there, is the exact khronometric scalar speed
  (X15 S0-3).

## Files and run

| file | contents |
|---|---|
| `x15_c1_preferred_frame.py` | Parts S0, D, W, T. X14's `aqual_point` and window formulas are copied with provenance. A22's script is run read-only by subprocess. |
| `x15_c1_preferred_frame.out`, `_results.json` | main run |
| `x15_c1_preferred_frame_MUTATE.out`, `_results_MUTATE.json` | MUTATE run (m1–m5) |
| `a22_rerun.out`, `a22_rerun.json`, `a22_rerun_MUTATE.*` | A22's own stdout and JSON from S0-1, redirected here |

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X15_c1_preferred_frame/x15_c1_preferred_frame.py              # exit 0
PYTHONHASHSEED=0 X15_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X15_c1_preferred_frame/x15_c1_preferred_frame.py  # exit 1 by design
```
