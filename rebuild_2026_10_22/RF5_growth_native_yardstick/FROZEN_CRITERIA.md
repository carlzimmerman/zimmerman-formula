# RF5_growth_native_yardstick: FROZEN CRITERIA (committed alone with ASSUMPTION_LEDGER.md, before any script or RF5 number)

**Question (THEORY_PROGRESS_SUMMARY_2026-10-31 §4).** Does the cold dark energy sector of v3s, and the flagship's cold core
law treated as a cosmological component, fail growth and the CMB when the background and the yardstick are the framework's own?

κ = ½ FITTED. Footings canonical (ρ_DE) and alt (ρ_total), graded separately, never pooled. Cold dark energy is a gravitating
field component, never a particle. Not "theory closed". Nothing here says the data favour the framework.

**Disclosed before freezing.** The author has read X34's table (Δχ² against a ΛCDM refit, z_on grid) and X4's R_B. Those numbers
are the reason this lane exists. They are not targets. No RF5 number exists at this commit.

## 1. Model family

Component content: photons, baryons, 3.044 massless neutrinos, GR background (the switch acts only in bound systems, X54 A1),
dark energy as a CPL fluid (w0, wa free, Ω_Λ = 0), cold component with an energy-conserving turn-on.

- **F-R1, the scanned family.** X34's patch unchanged (`x34_turnon.patch`, built by `x34_make_patch.py`, outside the repo):
  ρ_c = ρ_c0 a⁻³ S(a), tanh in ln a, width 0.05, fed by a w = −1 reservoir. This is the construction the v3s verdict quotes
  at its §Recombination block (line 234).
- **z_on grid (frozen):** 1e6, 3e5, 1e5, 5e4, 3e4, 2e4, 1.2e4, 7000, 4000, 2500, 1500, 1100, 300, 30.
- **F-K, the v3s rows.** Q6's khronon CLASS build (read-only binary, `class_khronon_build_2026_10_23`) at S4's μ_K = 0.03 and
  0.1 Mpc⁻¹ (the X4 cells), on the same background and the same channels. No turn-on knob. If that binary rejects the fluid or
  fails to converge, the rows are labelled UNDETERMINED with the error text.

## 2. Fit

Free per cell: ω_b, ω_c, 100θ_s, ln10¹⁰A_s, n_s, τ, w0, wa, A_planck. ω_c ∈ [5e-4, 0.5]. Gauss–Newton/Broyden as X54, steered on
plik-lite + A prior + τ steering prior (X54 A8, never in a graded χ²) + DESI DR2 BAO + DES-SN5YR. Fits run from high z_on down, each
cell started at the previous cell's best. C7's refit is the first start point only. Stop: |Δχ²| < 0.1 or 10 Jacobian-steps.

Shear and forest do not steer the fit; they are evaluated at each cell's best fit. So the summed statistic is an upper bound on
that cell's joint minimum. To bound this: **A_shear**, the single amplitude factor on the matter power that best fits the shear at
that cell, is reported for every cell (reported, not gated).

## 3. Channels and gates (absolute, on raw-data χ²; nothing is differenced against ΛCDM)

| channel | statistic | gate |
|---|---|---|
| G-CMB | χ²_plik, 613 bins, dof 605 | p ≥ 1e-3. Low-ℓ TT and EE have no absolute reference (likelihoods offset to a reference spectrum): reported; they enter S_full, not the gate |
| G-BAO | χ²_BAO, 13 values | p ≥ 1e-3, dof 13 |
| G-SN | χ²_SN, M marginalised | p ≥ 1e-3, dof n − 1 |
| G-SHEAR | DES Y3 ξ+ (see §4), full-block covariance, A_IA profiled, m_i and Δz_i marginalised linearly | p ≥ 1e-3, dof n_keep − 1. Needs n_keep ≥ 10, otherwise shear is UNDETERMINED |
| G-FOREST | DESI DR1 P1D, z 3.6–4.4 (see §5) | **G0 adequacy first**: at the surface's best forest cell, joint p ≥ 0.01 and each z p ≥ 1e-3, with the 2 % floor. If G0 fails the forest is NOT DIAGNOSTIC (as P1D1–P1D4) and the χ² surface is reported without entering any verdict. If G0 passes, each cell needs p ≥ 1e-3 |
| G-A0 | √X(z) = √(ρ_DE(z)/ρ_DE(0)) at z = 1, 1.5, 2.33 inside CFG689's curvature-free band [0.76,1.03], [0.71,1.12], [0.33,1.21] | all three |

**Surface statistic.** S = χ²_plik + A prior + χ²_BAO + χ²_SN + χ²_shear (+ χ²_forest only if G0 passes). S_full adds low-ℓ TT + EE
where finite. S is defined at every cell. **G-S:** S − S_min ≤ 25, where S_min is the minimum over the F-R1 surface itself. The line 25
is the record's (C2 §148–149). S_min is this lane's own family, framework-built; it is not a ΛCDM number.

**Window.** A z_on is in the window if G-CMB, G-BAO, G-SN, G-SHEAR, G-A0, G-S (and G-FOREST if live) all pass. Reported too: the edge
from the absolute gates alone, so a reader sees what the 25 line adds.

## 4. Shear (RAW two-point data; linear-safe)

File: `campaign_fresh_gravity/_external_data/cfg679_des/2pt_maglim.fits`, xip, the xip block of COVMAT, nz_source. ξ− is not used
(it is dominated by non-linear scales). HMcode, halofit and every N-body boost calibrated on ΛCDM are banned, and the framework has no
per-z_on non-linear model, so the prediction is Limber + linear P(k, z) from this cell's CLASS run, with a **scale cut fixed once**, at
the z_on = 1e6 cell's best fit, before any shear χ² is computed, by a rule that does not read the data vector: keep (i, j, θ) only if
replacing P(k, z) by 0 for k > k_NL = 0.2 h/Mpc changes the ξ+ prediction by ≤ 20 %. The same kept set is used at every cell.

IA: NLA with A_IA free, profiled on [−3, 3]; no z evolution parameter. m_i and Δz_i (source bins): linear templates at this cell's
best fit, published prior means and widths added to the covariance.

KiDS-1000 ξ± are not on disk as a data vector. KiDS is reported as missing, not rebuilt from the catalogue.

## 5. Forest (RAW flux power; native model)

`forest3d.py` from P1D4 read-only, its table recipe with no M6 (μ = 0), γ {1, 1.3, 1.6}, R_J {0.05, 0.12, 0.20} Mpc/h, b 7 nodes,
F̄ 10 nodes, N = 256, L = 64 Mpc/h, seed 0, stride 4 (P1D4's frozen stride before its A1). DESI DR1 per-z covariance blocks with a 2 %
model floor (P1D4's declared V-floor2). z 3.6, 3.8, 4.0, 4.2, 4.4 only, because P1D4 found lower z the model's worst. P(k, z) and
f(z) come from this cell's CLASS run, in Mpc/h on this cell's h, and cz from its H(z). 4 nuisances per z.

**Reported variant V-Fbar:** F̄(z) held at the Becker+13 fit (LITERATURE-INPUT) ± 5 %. It shows whether free F̄ hides an amplitude
deficit. Reported only. The b-cutoff correction of the record (0.4–0.9σ channel, never the withdrawn 6–8σ) enters as: b is free over
6–35 km/s; no separate b-cutoff penalty is used. Boera+19 is on disk but saturated at these amplitudes (P1D2); not graded.

The forest is run from high z_on down; whatever is not finished at the wall-time stop is labelled UNDETERMINED.

## 6. Footings

a₀ is absent from the linear FRW equations (Q6 D0, X34 A3), so both footings share the χ² surface. They are graded separately through
what each one reads off that surface: a₀(z) on canonical is κc√(Gρ_DE(z)) with G-A0 as in §3. On alt, a₀(0) = κc√(Gρ_total,0) is read at
each cell, and the same √X factor applies as in X54's convention (FOOT × √X). Reported per cell and per footing: native a₀(0) at κ = ½, and
a₀(2.33). The record's 9.3603e-11 and 1.1312e-10 inherit a Planck background and are shown for comparison only, never graded.

## 7. Verdict

Per footing, frozen wording:
- **"FAILS on raw forest + CMB spectra + shear at every turn-on epoch"** if no grid z_on is in the window.
- **"a window exists at z_on ∈ [lo, hi]"** otherwise, lo and hi being the window's grid edges. Which channels are live is stated in the same
  line (forest NOT DIAGNOSTIC is not a pass).
- F-K rows: "v3s khronon: FAILS / PASSES the same gates at μ_K = ..".
- Any channel whose data are not on disk, or whose run was not finished, is named: UNDETERMINED, with the reason.

Rule 7 of the summary: a verdict that changes because an outside input was removed reads "not a framework failure", not "the framework
passes". A window whose fit is nothing but early dust is called that: X34's reading "reduces to ordinary dust" stays unless the window
reaches below z_eq.

A dated addendum to `covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` relabels the F3 / X4 / L1 rows "measured against ΛCDM σ₈" and
points here; committed text there is not rewritten. If that file has others' uncommitted edits only the appended hunk is staged.

## 8. Checks (each required) and twin

- **K1** patched binary with the turn-on off reproduces vanilla: max |ΔC/C| ≤ 1e-4 (TT, EE, φφ).
- **K2** harness reproduction only: vanilla CLASS at C7's parameters gives the record's χ² within 2 (tool check, not a yardstick).
- **K3** energy identity at z_on = 1100 on the background: violation ≤ 2e-3 (X34 K1).
- **K4** shear Hankel: a Gaussian C_ℓ gives its analytic ξ+ within 1e-3 over the graded θ range.
- **K5** shear inputs: sha256 frozen in the script's output; xip has 200 rows; xip covariance block positive definite.
- **K6** forest shim: with P1D4's Background passed through the shim, tables equal direct forest3d within 1e-5; Gaussian P1D against the
  analytic projection within 5 % (P1D4 S0c).
- **K7** no banned constant in the graded path: grep for 5.364, 0.674, HMcode, halofit in the script fails only on the guard lines themselves.
- **K8** rerun identity: the z_on = 1e6 first-iteration χ² is identical on a second evaluation (±1e-6).
- **K9** preemption: a cell sent SIGTERM exits 75, and the resumed cell continues from its checkpoint with no repeat of a finished step.

**MUTATE (`RF5_MUTATE=1`, separate outputs, one cell z_on = 1e6, one iteration):** m1 plik data sign flipped; m2 shear data vector sign
flipped; m3 K1 target ×1.01 applied to patched output. G-CMB, G-SHEAR and K1 must FAIL.

**Stop rule.** Wall time near 3 hours: commit what is done and label the rest UNDETERMINED. Amendments only in `AMENDMENTS.md`, dated, stated
as before or after the numbers they concern.
