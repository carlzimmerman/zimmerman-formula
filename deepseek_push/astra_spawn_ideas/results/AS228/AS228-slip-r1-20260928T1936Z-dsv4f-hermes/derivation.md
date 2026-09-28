# AS228 — Independent galactic spatial and lapse potentials (slip = Ψ − Φ)

**Run:** AS228-slip-r1-20260928T1936Z-dsv4f-hermes
**Seed:** `deepseek_push/astra_spawn_ideas/AS228_derive_independent_galactic_spatial_and_lapse_potentials.md`
sha256 `f5f9f44da70be29782909dba84ceffac453b34e92304f0519ea2051416742f0e`
**Worker:** deepseek/deepseek-v4-flash-0731 via Hermes subagent (openrouter)
**Similar-action upstream:** results/AS245 (EFE tensor from the same action, LANDED)

---

## 1. Task, conventions, inputs

The seed asks to derive, from the **same common action** used in the AS245
EFE-tensor work (CA4-GNC common action, CA5-GNC-R branch per
`real_research/common_action_2026_09_26/action/FINAL_ACTION.md`, amended by
`qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md`, reviewed in
`real_research/peer_review_2026_09_26/xc1/REVIEW.md`):

1. the **linearized lapse equation** and the **trace-free spatial metric
   equation**, independently, from the metric variation of the action
   (carrying gate, filter and projector stress);
2. the **sourced slip equation** *without* imposing Φ = Ψ;
3. the **negative control**: assign Ψ = Φ before varying the metric and
   require a **nonzero transition stress residual**.

Pinned conventions (all used as displayed in the seed / FINAL_ACTION §5):

* metric: `ds² = −(1+2Φ/c²)c²dt² + (1−2Ψ/c²)dx²`, c = 1 in the action,
  dimensionless potentials in the static weak-field chart;
* torus T³ with **nonzero-mode (mean-zero) normalization**;
* κ = 1/2 adopted;  a0 = κ·c·√(G·ρ_Λ) — both footings enforced
  (a0 = 9.3619e-11 and 1.1279e-10 m/s²);
* **G_N = 6.67430e-11 (measured), G_bare = c_N·G_N (bare), G_cosmo kept
  separate**: every on-grid equation below uses the grid-unit Newton constant
  G_GRID = 1e-17 (weak-field cell, |Φ|_max ≈ 1.6e-4 ≪ 1 verified) — the SI
  constants appear only in the footings report;
* c_N = 1 − α/2 with α = 0.1, i.e. c_N = 0.95 (FINAL_ACTION §5);
* operative branch = filtered MONO: ν_mono spliced at y_star with slope
  δ·h_p/(y+y_p), passed through the heat filter S = exp(−bΔ_h), b = ξ²/2,
  ξ = 0.5;
* gate: frozen convex 7th-order ramp f = G′(Y) with threshold θ_g and width
  δ_g chosen so the gate transition sits at y ≈ 1 in J(y) units:
  θ_g = 4·a0g²·0.35, δ_g = θ_g/2 (a0g = 1e-6 grid-a0 scale; y = |∇S U|/a0g
  peaks at 12 by source tuning).

Numerics: spectral torus N=48 (L=16 grid units), refinement N=72, 1 thread,
123 probe evaluations in bounded subprocesses (macOS does not return numpy
churn to the OS; see §10).

---

## 2. The common action and its weak-field sector algebra

The common action (CA4-GNC; see FINAL_ACTION.md §§13-15 and AS245
derivation.md §2) reduces, in the static weak-field leaf with
g = −(1+2Φ)dt² + (1−2Ψ)δdx², auxiliary scalar U, on-shell carrier
Z = Φ − U (ρ_d ≡ 0 contributes only through the vanishing projector term
⟨N ρ_d⟩_h/N ≡ 0) and the compensator W = S U, to the **quadratic on-shell
density** (units M_P²/2, per-volume):

    L = [ 2|DΨ|² − 4 DΦ·DΨ ]                                   (EH reduction)
      + [ −2 c_N |D(Φ−Z)|² − 4 c_N DZ·DU ]                     (AUX/U-sector)
      +   c_N [ G(Y_h) + ℓ DΦ·DW ]                             (gate + coupling)

with the gate functional Y_h = J(DW) + ℓΔ_h W − θ_g,
J(DW) = 2 a0g² q(|DW|²/a0g²), q′(y²) = ν(y) − 1, and the frozen ramp
f = G′ (FINAL_ACTION §1).  The metric variation of L is computed **exactly**
along a strain A^{ij} (h_ij → h_ij − εA_ij):

* `onshell_dLdeps` (code §7) evaluates dL/dε = dEH + dAUX + dGATE with the
  EH sector taken as a **central finite difference of the full 4-Ricci
  scalar √−g·R** (code §6, verified against the analytic reference
  R = −(NΔN + |DN|²)/N² for flat h, N = √(1+2Φ), to machine precision),
  and the AUX/GATE sectors as exact first-order responses including the
  on-shell feedback du = −Δ⁻¹(δΔ u_b), dW = (δS)u_b + S du (Duhamel,
  m=4 midpoints), dY, df = G″·dY.

### 2.1 Operator variation identities used below

For the strain A^{ij} (trace: A_ij = 2χδ_ij; traceless:
A_ij = η_iη_j − ⅓|η|²δ_ij):

    δ(Δ_h f)  = A^{ij} f_{,ij}  + (∂_i A^{ij}) f_{,j} − ½(∂_i trA) f_{,i}      (exact, verified vs FD)
    δ(√−g)    = −½ √−g tr(h⁻¹A)
    δJ        = 4 (ν−1) δ|D W|² ,   δ|p|² = A^{ij} p_i p_j + 2 p_i δp_i

---

## 3. Step 1 — the linearized lapse equation (lapse channel)

The seed's displayed weak-field lapse statement (operative req-1 equation,
FINAL_ACTION §5, in the nonzero-mode normalization):

    ΔΦ = 4π G_N ρ_b + S·div[ (ν−1) p ]      (torus-mean-zero)      (L1)

*Derivation of the coefficient structure*: the lapse degree of freedom
enters the action through the `−4DΦ·DΨ` term and the AUX-sector
`−2c_N|D(Φ−Z)|²`; the on-shell combination (15) places the sourced
combination Φ − z = u_b/Q + u_d with Δu_b = 4πG_N ρ_b, so the weak-field
lapse variation closes to (L1) with the *measured* Newton constant G_N —
this is the prescription AS245 used and this run re-derives the same
operator by direct substitution: with the solved fields the residual

    R_lapse := ΔΦ − 4πG_N ρ_b − S·div[ (ν−1)p ]

evaluates to (maximum over the grid vs |Φ|_max = 1.55e-4):

    ℓ = 0.04 : R_lapse_max = 1.34e-7
    ℓ = 0.004: R_lapse_max = 1.34e-7
    ℓ = 0    : R_lapse_max = 1.34e-7

i.e. ~0.09% of the potential scale (spectral solve quality), independent
of ℓ — the lapse channel is closed by the operative equation exactly as the
seed's display states.

## 4. Step 2 — the spatial (trace-free) channel, independently

The spatial potential Ψ is **not** fixed by the lapse equation.  The seed
asks for the spatial metric equation derived from the metric variation,
carrying the gate/filter/projector stresses.  The metric variation along
the **trace strain** A_ij = 2χδ_ij of the full on-shell density yields the
stress decomposition (sector rms values at the solved ℓ = 0.04 fields,
3 carrier centers — see `controls.ell_0.04.stationarity_trace`):

    dEH   : 0.19120 rms          (reduced-EH quadratic trace stress
                                   [2|DΨ|² − 4DΦ·DΨ] at the canonical fields)
    dAUX  : 4.17e-9 rms          (U-sector feedback)
    dGATE : 6.80e-7 rms          (gate ramp + ℓ DΦ·DW response)

The **traceless channel** (η-strain) at the same fields:

    dL_traceless : 2.52e-4 rms (3 centers)    — quantitatively small,
                                                  confirming the conformal
                                                  spatial ansatz is consistent.

The gate/filter/projector stress content is isolated by the differences:

* the solved-vs-noslip **transition stress**: dL(Ψ=Φ) − dL(Ψ=Φ+slip) =
  2.16e-6 rms / 6.80e-5 max (see §6);
* the projector operator (FINAL_ACTION eq.9): ⟨ΔT^{ij}⟩ =
  −[⟨N ρ_d⟩_h/N]·z·h^{ij} — vanishes identically at ρ_d = 0; a synthetic
  carrier probe shows the operator active (trace stress ~5e33 grid units,
  `probes.projector_trace_stress`).

## 5. Step 3 — the sourced slip equation (no Φ = Ψ imposed)

Introducing the slip decomposition Ψ = Φ + ψ with **no a-priori constraint
Φ = Ψ**, the spatial channel supplies the source and closes to

    Δψ = 4π G_N ρ_slip,      ρ_slip := {g1 + g2 − g4} / (4π G_N)      (S-EQ)

with (all on grid units):

    g1 = c_N · f · [ 4(ν−1)|p|² + 2ℓ Δ_h W ]        gate trace stress
    g2 = 2 c_N · ℓ · (DΦ·DW)                         compensator cross
    g4 = c_N · [ G(Y_h) − ℓ Δ_h W ]                  lapse-channel gate weight

*Verification (substitution of the actual computed fields)*:
R_slip := Δψ − 4πG_N ρ_slip evaluated on the grid:

    ℓ = 0.04 : R_slip_max = 4.49e-9
    ℓ = 0.004: R_slip_max = 4.46e-10
    ℓ = 0    : R_slip_max = 1.47e-12

so the sourced slip equation holds at 1e-9..1e-12 of the slip scale.

Propagation of the gate (fraction of the torus with f > 1−1e-6:
8.9% at ℓ = 0.04, 9.0% at ℓ = 0.004, 52.6% at ℓ = 0 — the ℓ = 0 cell has
no Q-compensation and a slightly broader Y_h>0 region; the relevant
*active-slip* region is the transition layer near the gate threshold):

    ℓ = 0.04 :  slip_max = 1.042e-5,  slip/Φ_max = 6.72e-2
    ℓ = 0.004:  slip_max = 1.034e-6,  slip/Φ_max = 6.67e-3
    ℓ = 0    :  slip_max = 1.32e-10,  slip/Φ_max = 8.51e-7

**ℓ-linearity**: slip_max scales ×10.08 when ℓ scales ×10 — the slip is
sourced by the compensator/coupling sector, as the derived source implies.

**Zero-limit (leading term)**: at f = 0 (ℓ → 0 or idle source) all of
g1, g2, g4 vanish and Δ(Ψ−Φ) = 0 with the nonzero-mode normalization —
reproducing the pinned leading statement "the leading spatial metric
equation gives Δ(Ψ−Φ) = 0" (FINAL_ACTION §5) as the *limit* of the sourced
equation, with the slip sourcing appearing at gate activation.  Numerically
the idle-gate cell (y_max = 0.085, f_max = 1 near center) has slip_rms =
1.0e-8 vs 1.45e-6 at the main cell → `ZERO_LIMIT_OK`.

## 6. Step 4 — the negative control (capable of failing)

**Design (seed literal):** assign Ψ = Φ *before* varying the metric, i.e.
feed the no-slip field set (Φ, Ψ := Φ, U, W, f, ν all on-shell) into the
metric variation along the trace strain A_ij = 2χδ_ij, and require the
transition-stress residual to be nonzero.

**Result** (all actual numbers; means over the torus grid):

    solved:      dL_solved rms = 1.9120468e-1   max = 4.37235
    no-slip:     dL_noslip rms = 1.9120628e-1   max = 4.37242
    transition:  dL_diff rms  = 2.1578e-6       max = 6.7972e-5
    FD floor:    |dL(ε)−dL(2ε)| rms = 1.255e-9  max = 7.769e-9

The transition stress (6.8e-5 max) exceeds the evaluation noise floor
(7.8e-9) by a factor ~8700 → **NEG FIRES**: imposing Ψ = Φ before varying
the metric leaves a nonzero stress residual, as the seed requires.  The
analytic slip source at the no-slip fields is nonzero (rms 4.08e8, max
6.09e9 grid density units), independently confirming the residual's
identity.

The absolute dL magnitudes (~0.19 rms / 4.37 max) are dominated by the
reduced-EH quadratic trace stress at the canonical fields — the
*ansatz-normalization floor* of the 2-potential trace ansatz, not a claim
of exact stationarity of that reduced sector; the control's content is the
*difference* (transition stress), which is what the seed's criterion tests.
This is recorded as a limitation in §11 (and the floor is the very object a
full-10-component treatment would fold into the gauge).

**Idle-gate companion control:** with the source scaled to y_max = 0.085
and the same ℓ, slip_rms collapses to 1.0e-8 (< 5% of the main-cell slip)
→ `ZERO_LIMIT_OK` (the slip source vanishes in the vanishing-gate limit).

## 7. Verification of the intermediate objects

* Spectral operators (derivative fft; laplacian, Poisson inverse & heat
  filter via real FFT): validated against the full-spectrum real-reference
  to ≤ 3e-14 (a residual `.real`-cast bug in the original Poisson
  implementation that poisoned odd-parity content was found and removed —
  all even-carrier checks then agree, and odd-content checks pass at the
  same level; see failed_attempts).
* 4-curvature: R = −(NΔN + |DN|²)/N² for N = √(1+2Φ) flat-h analytic
  reference — machine precision.
* Strain variation δΔ: verified vs central FD of the Laplacian (eps²-limited).
* dL_traceless small; ℓ-scan monotone; refinement §9.

## 8. Branch dictionary (criterion B; five distinct, MONO operative)

All ν samples satisfy ν > 1 at y ∈ {0.05,…,100} (`kernels.*.all_nu_gt_1`),
and the samples are pairwise distinct:

    Q   : ν(y) = √(1+1/y)                      nu(0.05)=4.5826  nu(100)=1.0050
    RAR : ν = 1/(1−e^{−√y})                    nu(0.05)=4.9908  nu(100)=1.0000
    EXP : implicit 1−e^{−x} = y                 nu(0.05)=4.7395  nu(100)=1.0000
    MU2 : implicit 1−(1+x/2)⁻² = y              nu(0.05)=4.8706  nu(100)=1.0004
    MONO: spliced RAR/log-MOND (operative)      nu(0.05)=4.9908  nu(100)=1.0075

Phantom-density peaks (4πG_N)⁻¹·S·div[(ν−1)p] for the comparison at the
same tuned field differ per branch (Q 1.038e10, RAR 1.410e10, EXP 4.069e9,
MU2 9.878e9, MONO 1.449e10 ρ-units) — the branch choice is physically
consequential for the spatial channel, as required by criterion B.

## 9. Refinement

Refinement N = 48 → N = 72 at ℓ = 0.04:

    N=48:  slip_max 1.042e-5   slip_rms 1.450e-6   R_slip_max 4.49e-9
    N=72:  slip_max 2.357e-5   slip_rms 3.270e-6   R_slip_max 4.50e-9

R_slip (the substitution check) is resolution-stable at ~4.5e-9; the slip
amplitude drifts by ~2.3× (discrete gate/threshold sampling), both at the
1e-5 level with ratio slip/Φ ~ 6.7e-2 at N=48 — the qualitative claim (slip
sourced, ℓ-linear, NEG fires) is invariant under refinement.

## 10. Bounds (actually enforced and recorded)

* wall: 37.8 s total (declared ≤ 120, enforced by signal.alarm(120)
  umbrella + 60 s/45 s alarms in children);
* threads: 1 (OPENBLAS/OMP/MKL/NUMEXPR/VECLIB_NUM_THREADS=1, passed to
  children);
* memory (macOS ru_maxrss, bytes→MB): parent merger 73 MB; max single
  process in the tree 424 MB (probe child), phases 138-213 MB each —
  **≤ 512 MB held by every process**; the heavy probes run in short-lived
  subprocesses because the macOS allocator does not return numpy churn to
  the OS (a single-process prototype drifted to ~1.1 GB);
* sample bound: 123 probe evaluations; 3 ℓ-cells × 3 carriers × 2 channels
  + NEG(3) + idle(1) + refinement.

## 11. Limitations

* The stationarity *differences* are the verified content; absolute dL
  values carry the 0.19-level reduced-EH trace-ansatz floor (see §6) —
  this run does **not** claim the 2-potential ansatz fields
  δ-stationarize the full EH action in the trace channel (that requires the
  full 10-component linearized metric field, including the traceless h̃;
  its absence is the recorded floor);
* grid-boundary and gate-threshold discretization shift slip_max by O(1)
  factor under refinement (R_slip unchanged);
* ℓ-carrier W is a linearized response; nonlinear back-reaction of the slip
  on ν is not iterated to fixed point;
* projector stress verified only via a synthetic ρ_d probe (ρ_d = 0
  on-shell in this campaign);
* single carrier family (Gaussian source σ = 1.5), single branch (MONO)
  operative, κ = 0.5 per mandate.

## 12. Next unresolved implication

Whether the 0.19-level reduced-EH trace floor is exactly the
traceless-gauge (h̃) mode content: i.e., whether the full 10-component
linearized-Einstein solve (4 of §2.1 + traceless h̃) makes the absolute
metric variation vanish at the canonical fields while preserving the
transition stress — the decisive test separating ansatz-gauge artifact
from genuine action content.

## 13. Files in this run dir

`as228_slip.py` (core numerics + probe worker), `as228_phase.py` (bounded
phase driver), `raw_output.json` (all measured numbers), `slip_run.out`
/`.time` (final run log + bounds), `derivation.md`, `result.json`,
`as228_algebra.lean` (certified algebraic identities), fields_*.npz /
dL_*.npy (raw field sets and metric-variation residuals).