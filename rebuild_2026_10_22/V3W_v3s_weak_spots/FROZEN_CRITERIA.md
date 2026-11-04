# V3W_v3s_weak_spots: FROZEN CRITERIA (committed alone, before any script or number)

**Owner 11-04:** "Test weak spots first", in reply to whether to adopt v3s as the galaxy law's action. Test lanes may
reopen frozen items under the 11-04 lift. **This lane adopts nothing.** The 10-24 v3s verdict
(`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md`) stands unless the owner changes it in writing. No file under
`covariant_push_2026_10_22/` is edited; their code is imported read-only (bytecode writing off).

κ = ½ FITTED. Footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not blind: AX1, C6, C6P, C5,
C8, X3, X15, X53, GH1 and X75 numbers were seen first. Not theory closed. Nothing here says the data favour the
framework. The cold sector stays retired. CMB and clusters are out of scope and open. a0 is put in by hand.

Lane id checked free: `ls rebuild_2026_10_22 | grep V3W` and `git log --all --oneline | grep V3W` both empty (11-04).

## The action tested (frozen 10-24 form, C4/C5/C6, X3 switch)

    S = (c⁴/16πG) ∫ √−g [ R − 2Λ + 2μ_K²(Q − 1)² ] + ∫ √−g [ P^i A_i − W(K|P|) − (γ_L/2)[max(D_iP^i, 0)]² ] + S_m

with τ = t on static backgrounds, N = e^Φ the lapse, A_i = ∂_i ln N, h_ij the spatial metric, P an independent spatial
covector, K = 4πG/c², W = (a0²/K)[−u/a0 − ln(1 − u/a0)], u = K|P|, γ_L = K L★²/2, L★ ≥ 21.7 / 22.9 pc. In the static weak
field with h_ij = δ_ij this is C6's Lagrangian −|∇Φ|²/2K + P·∇Φ − W − (γ_L/2)(∇·P)² − ρΦ (the GR part at Ψ = Φ).

## W1. PPN γ and β, derived from the action

**Method.** sympy. Static, spherically symmetric, isotropic gauge (fully general for a static spherical 3-metric):
ds² = −e^{2Φ(r)}c²dt² + e^{−2Ψ(r)}(dr² + r²dΩ²), P = P_r(r) dr. Reduce the action exactly (no truncation) to a 1D
Lagrangian in r; the GR part is checked against √−g R computed from the 4-metric (same Euler–Lagrange equations,
residual 0). Derive the three exact Euler–Lagrange equations (Φ, Ψ, P_r) in vacuum outside a point mass M.
Then expand in GM: first order gives γ, second order gives β. The P sector is expanded about |p| = 0, valid where
|p| ≪ a0 (the screened isolated Sun: p ≈ GM/L★² ≈ 2.4e-16 m/s², |p|/a0 ≈ 2.6e-6).

- **γ.** γ − 1 is read from Ψ − Φ at O(GM). Also derive the exact linear-in-solar-field source of the Ψ equation when
  the Sun sits in a uniform Galactic background (P_e, ∇Φ_e) in 3D (sympy), and bound |Φ − Ψ|/U from it with the cap
  |p_e| < a0 and the hedgehog size, out to r = 10 AU (Cassini's path ≤ 8.4 AU), with a cutoff at L★.
- **β.** β − 1 is the coefficient of (GM/c²r)² in g_00 beyond GR's, from the O((GM)²) solution. Terms that are not of
  the PPN form U² (e.g. ∝ GM·(GM/L★²)·r or ∝ a0) are reported as non-PPN remainders with their size at Mercury.
- **Grade (frozen).** γ: Cassini γ − 1 = (2.1 ± 2.3)e-5 (Bertotti, Iess & Tortora 2003); PASS iff the derived γ − 1,
  including the bounded remainder at r ≤ 10 AU, lies in the 2σ band [−2.5e-5, 6.7e-5]. β: PASS iff |β − 1| plus the
  remainder at Mercury (0.387 AU) ≤ 1e-4 (lunar laser ranging, as given). FAIL iff outside. **UNDECIDED** iff the action
  cannot be expanded to the needed order (say where it breaks) or a W1 check fails.
- **Known answer (check W1-K1).** Law switched off (P sector removed, Λ = μ_K = 0): isotropic Schwarzschild
  e^Φ = (1 − m/2r)/(1 + m/2r), e^{−Ψ} = (1 + m/2r)² must solve the derived equations exactly (residual 0), giving
  γ = β = 1 exactly. **W1-K2:** the 1D reduction of √−g R gives the same Euler–Lagrange equations as the ADM form
  (residual 0). **W1-K3:** the first-order P equation reproduces C6's (P_L) linearised, and the first-order solution
  reproduces the hedgehog p = GM/L★² r̂ of C6/C8 (residual 0). **W1-K4:** expansion validity |p|/a0 ≤ 1e-4 at 24 pc.

## W2. C6's carried checks, rerun

Rerun C6's C1, C3, C4, C5, C6, C7 and C8 (C2 is C6P's) with C6's code (`c6_solver.py`, `d7d_solver.py`) imported
read-only and C6's own inputs (a0 9.36e-11 / 1.13e-10, D7b fields, E2 anchors, D7d json), C6's own pass lines.
Each is reported **reproduced** (same pass/fail, |Δ|/|value| ≤ 1e-9 against `c6_literal_cassini_results.json`, or exact
where C6 recorded 0), **changed** (same pass/fail, larger difference) or **failed** (pass/fail flips, or fails now).

**C6′ (replacement for C6's check C6, in the physical window).** C6 passed its C6 on an unconverged Λ = 0.01 r_M solve,
below the window. The original C6 is rerun as recorded and reported. The graded replacement:
- Route N (r_F = 0, C6's `solve_v`), E2 field, both footings at the exact footing a0, at Λ = L★/r_M for L★ = 24 pc
  (canonical Λ ≈ 622, alt ≈ 683), and also at Λ = 100 for continuity with C5.
- Resolution ladder (points per decade, N_θ): (20, 32), (30, 48), (40, 64). Each solve in its own forked process.
- Q2 is extracted at three radii, r_x = 1, 10 and 100 × r_Saturn (all ≪ L★); the **graded radius is 100 r_Saturn**
  (958 AU, r/L★ ≤ 2e-4), because at r_Saturn the l = 2 part is ~1e-18 of the monopole at Λ ≈ 600, beyond float64. The
  other radii are reported.
- **Pass line (frozen):** (a) every rung converged, residual < 1e-9; (b) the ladder converges: the change from rung 2 to
  3 is smaller than from 1 to 2, and the Richardson value from rungs 2–3 (order 2, h ratio 4/3, C6's formula) differs
  from rung 3 by < 2e-2 relative; (c) the Richardson value agrees with Route F at the same L★ within 5e-2 (C5's line),
  same sign. All at the graded radius, every (footing, Λ) cell.
- Memory: every job must stay < 1 GB RSS (BK2 L2 is running). A rung that would exceed it is not run and C6′ is
  UNDECIDED for that cell, disclosed.

**W2 label per footing:** PASS iff C1, C3–C5, C7, C8 are reproduced or changed-but-passing, C6′ passes, and C6P's
24-cell Q2 result stands (Hees 2σ upper 9.0e-27; read from C6P). FAIL iff a rerun check fails on physics or a Q2 cell
leaves the band. UNDECIDED iff a check fails on numerics.

## W3. Galaxy lensing = dynamics

**What AX1's G3 PASS rests on** (to be stated): the record's φ = ψ (BS24 Eq. 24; C4 K1) plus S4's μ_K bound; it was
read, not computed against data in AX1.

**The number.** v3s's lensing-to-dynamical mass ratio for isolated galaxies is computed from W1's Ψ-equation result at
galaxy scale (Φ − Ψ at O(a0 r/c²)), so the predicted ratio is 1 up to that bound. Against data, the measured ratio is the
amplitude A of the observed ΔΣ relative to the law's ΔΣ (isolated AQUAL, μ = x/(1+x), the dynamical mass the law gives
from rotation curves): A = M_lens/M_dyn,law at fixed radius, fitted by generalised least squares.

- **D1, primary: KiDS-1000 isolated lenses** (Brouwer+21 Fig. 3, released covariance), F2's machinery executed
  read-only as X53 does (data_native, stack_model with CENTRAL0: y_e = 0, f_hot 0.5, native h 0.679), R ≤ 0.31 Mpc
  (2-halo negligible, μ_K R ≤ 0.031). All radii reported, not graded.
- **D2, matched hosts: GH1's 9,049 G09 centrals**, KiDS-1000 lensing at 50–300 kpc, GH1's committed law prediction
  `pred_L` and its jackknife covariance with Hartlap, recomputed from GH1's `gh1_esd.npz` (work file outside the repo;
  check W3-K2: the recomputed ΔΣ equals GH1's committed `DS` to 1e-12 relative).
- **Satellites** (X75 σ_sat vs the law's σ on the same hosts) are reported with their method systematic: on matched
  hosts GH1 finds lensing Δ = +0.17 [+0.05, +0.28] (canonical) against satellites +0.79 ± 0.03, so satellites carry a
  ≈ +0.6 dex method systematic. The matched-host lensing reading (D2) is used; satellites are not graded.
- **Errors (frozen).** σ_stat from the covariance, scaled by max(1, √(χ²_min/dof)). σ_sys = half the spread of A over
  lens stellar mass ±0.2 dex and cold gas ±0.2 dex (F2's own systematic rows), in quadrature, D1 only; for D2 the same
  M★ ±0.2 dex propagated by rescaling is not available from the committed tables, so D2 uses σ_stat plus a frozen 0.10
  photo-z dilution allowance (GH1's disclosed 5–10 % low bias; one-sided, A may be up to 10 % low).
- **Grade per footing (frozen):** PASS iff |A − 1| ≤ 2σ_tot on D1 **and** D2 is not more than 2σ_tot from 1;
  FAIL iff D1 is more than 2σ_tot from 1, or D2 is more than 3σ_tot from 1; otherwise UNDECIDED. χ²_min and p are
  reported (shape is not graded here; X53 already records that no model fits well in absolute terms).
- **W3-K1 known answer:** the law's stacked ΔΣ reproduces X53's committed (L) profiles to 1e-9 relative.

## W4. Stability and GW speed

Each item gets a number or a derivation line with its source, and is marked **SHOWN** (derived or computed, here or on
record with a passing check) or **ASSERTED** (stated on record without a passing check, or by a check that failed).
- **W4a c_T.** sympy: TT perturbation on a frozen background with uniform P, constant ∂P and D·P. Show the principal
  part is GR's (c_T = c exactly) and compute the mass terms including the stiffness term C8 K9 did not include. Grade
  Δv/c at 100 Hz on the Solar-System background (g = 9.81 m/s² as C8) against GW170817 −3e-15 < Δc/c < 7e-16
  (Abbott+ 2017).
- **W4b ghost / gradient, galaxy backgrounds.** Re-derive: (i) at β = η = 0 the action has no time derivative of N or P
  (structural); (ii) leaf convexity, g″ ≥ 0 on [0, a0) and the Schur complement of the principal symbol
  ≥ min(K, γ_L|ξ|²) (C8 K1), recomputed on a grid of u/a0 ∈ [0, 0.999] and angles; (iii) dust kinetic sign 𝒦″ = 2μ_K² > 0;
  (iv) stiff-side fluid c² = γ_L(D·P + ρ_d) ≥ 0 (X3).
- **W4c ghost / gradient, Solar-System background.** Same items on the Sun's screened background, plus X3's D·P > 0
  margin near the Sun; C5's frozen H5/H6 FAILs (WKB invalid at g/k ≥ 40.7) are carried and flagged.
- **Label per footing:** PASS iff every item is SHOWN and passes; FAIL iff any SHOWN item fails; UNDECIDED iff an item
  rests on ASSERTED support or on a failed record check.

## Lane checks
- **MUTATE twin** (`V3W_MUTATE=1`, outputs `*_MUTATE.*`): screening removed (γ_L → 0, i.e. L★ → 0). W1: the isolated
  Sun's p saturates toward a0, so W1-K4 must fail and the planet anomaly returns to the a0 tail. W2: Q2 is the plain
  AQUAL value (C6's C4 Route N at Λ = 0), which must leave the Hees band. W3: the lensing prediction is replaced by a
  conformal-scalar reading (lensing sees the Newtonian baryons only, AX1 G3's failing class), so A must move far from 1.
  The twin must fail at least one check in each of W1, W2, W3 and exit 1.
- **Byte-identical rerun** of every main script (SHA-256 of JSON and .out recorded).
- **Ladders** wherever a numerical solve is used (C6′ above; quadrature refinement in W1 bounds if any).
- Compute: < 1 GB RSS, one thread, minutes per job, no downloads. Web look-ups (none planned) would be PROVISIONAL.

## Output
README.md leads with a one-line verdict and a table W1–W4 × canonical/alt: PASS / FAIL (number) / UNDECIDED (reason).
One pointer line under the v3s row of `rebuild_2026_10_22/AX1_action_for_law/README.md`.
