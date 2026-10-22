# E2_field_equation — FROZEN CRITERIA (written before any script or number of this lane)

Wave E audit lane (`BRIEF.md`, `BRIEF_E_AUDIT.md`). κ = ½ is FITTED. Both footings (a₀ = 9.36e-11, 1.13e-10 m/s²),
never pooled. Not theory closed.

## Question

D2 (wide binaries, `qumond_fft.py`), D7b (Cassini Q₂) and D7c (Q₂ vs RAR family) computed the unscreened law with
**QUMOND** (phantom-as-gravity: ∇²Φ = ∇·[ν(|g_N|/a₀) g_N]). The owner's rule allows standard-MOND machinery only if it IS
the framework's own field equation. (1) Which nonlinear Poisson equation does the framework's own static action give for a
point mass in an external field at L★ → 0? (2) If not QUMOND, recompute D7b's Q₂, D2's γ_v(20 kAU) and D7c's family
no-go with the action's own equation. (3) Check D7d's L★ → 0 statement ("Route N = AQUAL") against (1). D7d's solve is not run.

## Record checked before freezing

PAPER49 §2–3 (`qwen_claude_field_theory/papers_2026/PAPER49_why_cold_energy_settles_2026.tex`: L = −|∇Φ − KP|²/2K − ρΦ −
W_rem(u) − (γ/2)|∇P|², K dW_full/du = a₀u/(a₀ − u)); DSF-21 THEORY.md §2 and A33 MASTER_ACTION.md §1–3 (ADM form with
clock term P·∇ln N and full W; A33 K4 "AQUAL μ = x/(1+x)" is an algebraic spherical identity, not a field-equation
derivation); A24 report (claims "the law is AQUAL", computes QUMOND, asserts QUMOND–AQUAL ≤ 0.019 in γ_v); CFG191
(an AQUAL Picard run that did not reach its residual target); D2, D7b (K5: QUMOND/BN11-AQUAL = 0.737), D7c, D7d
FROZEN_CRITERIA (its (L),(P) equations and "at L★ = 0 this is AQUAL"). No committed lane has derived the field
equation of the EFE problem from the action and recomputed Q₂ / γ_v with it.

## Part 1 — derivation (what counts as "the action gives AQUAL")

Static, weak field, O(ε), L★ → 0 (γ = 0), cold-sector density neglected in the Solar System and binary (stated, not tested).
"The action gives AQUAL" iff all of:

- **K1a (PAPER49 form, sympy).** The Euler–Lagrange equations of PAPER49's Lagrangian at γ = 0 are (Φ) ∇·(∇Φ − KP) = Kρ and
  (P) ∇Φ − KP = R(u) P̂ with R(u) = u²/(a₀ − u) (algebraic, P ∥ ∇Φ). Substituting the algebraic solution
  KP = u(|∇Φ|) ∇Φ/|∇Φ| into (Φ) gives ∇·[μ(|∇Φ|/a₀)∇Φ] = Kρ with μ(x) = x/(1+x): symbolic residual exactly 0 for a
  general 3-D field (not only spherical).
- **K1b (A33/DSF-21 ADM form, sympy).** The static weak-field reduction of A33's action (R3/4K → −|∇Φ|²/2K, clock term
  P·∇Φ, full W) is identical to PAPER49's Lagrangian up to a total derivative (difference exactly 0), so it gives the same
  equations. D7d's (L)/(P) at L★ = 0 equal these (symbolic residual 0).
- **K1c (not QUMOND).** The action imposes curl-freeness on ∇Φ only. h ≡ ∇Φ − KP = μ(|∇Φ|)∇Φ carries a divergence-free
  part that the action does not set to zero. Numerically, on the converged AQUAL solution of a point mass in an external
  field (canonical E2), the transverse (curl) part of μ(|∇Φ|)∇Φ, relative to its anomalous part at r = r_M, is ≥ 1 %.
  QUMOND sets it to zero. If it is < 1 %, the two equations are numerically interchangeable for this problem and the
  lane says so.

If K1a–K1b pass, the action's equation is AQUAL with simple μ, and QUMOND in D2/D7b/D7c is a hidden ingredient that
is not the framework's equation. Part 2 then recomputes with AQUAL.

## Part 2 — numerical machinery (validation checks; exit 0 iff all PASS)

Route A (axisymmetric, Q₂): finite volume on (ln r, θ), units r_M = √(GM/a₀) = 1, a₀ = 1. Unknown ψ = Φ − Φ_N,pt − g_e z;
analytic Newtonian point field subtracted at faces. Fixed-point iteration with the LU-factorised Laplacian:
Lψ = D[(1 − μ)F − (F_a − F_N)] (AQUAL) or Lψ = D[(ν − 1)F_N − (F_a − F_N)] (QUMOND, one solve), with Anderson
mixing. Inner boundary r_in: regular per Legendre mode (ψ_l ∝ r^l, l ≥ 1) and the isolated l = 0 increment; outer
r_out: Dirichlet with the linear AQUAL (or QUMOND) EFE monopole field. Q₂ = −3 ψ₂/r² extrapolated to r → 0 from a
fit on r ∈ [1e-3, 3e-2] r_M (BN11/Hees sign, MOND positive; sign checked by K2).
Route B (3-D, γ_v): D2's geometry (1+1 M☉, s = 1, stars at cell centres, N = 192, m = 8 production), AQUAL by the
fixed point F = g_e ê + F_N,int + P_L[(1 − μ(|F|))F − (1 − μ_e) g_e ê] with the FFT longitudinal projection.

- **K2 (Route A QUMOND vs D7b).** Q₂ within 2 % of D7b's Route M (y_t = none), all 4 E, both footings, same sign.
- **K3 (BN11).** Route A AQUAL, simple μ, a₀ = 1.2e-10, g_e = 1.9e-10 (total): Q₂ within 10 % of BN11's 3.8e-26
  (external, as transcribed in D7b). The QUMOND value at the same inputs must stay at D7b's 0.737 ± 0.02 of it.
- **K4 (isolated limit).** Route A AQUAL at g_e = 0: radial field equals the algebraic law g_N = g²/(g + a₀) to 1e-3
  relative at r = 0.1, 1, 10 r_M; angular (l ≥ 1) content < 1e-6.
- **K5 (Route A convergence).** Doubling N_θ, ×1.5 radial density and r_in/10 change Q₂ by < 2 % (canonical E2, AQUAL).
  Iteration converged: last update changes Q₂ < 1e-6 relative.
- **K6 (Route B linear AQUAL EFE).** The FFT anisotropic linear solve gives B_par = 1/μ_e and
  B_perp = 1/(μ_e √(1+L₀)), L₀ = d ln μ/d ln x at x_e, to ≤ 2 %.
- **K7 (Route B vs Route A).** Single point mass in the external field (canonical, x_e = 1.9): the anomalous field
  F − F_N,int − g_e ê at r = r_M on the axis (both sides) and the equator agrees between the 3-D and the axisymmetric
  AQUAL solvers within 3 % of its magnitude.
- **K8 (Route B QUMOND reproduction + convergence).** Route B in QUMOND mode reproduces D2's γ_v(20 kAU, θ = 0, PREREG
  primary, canonical) 1.1897 within 0.002; AQUAL γ_v(θ = 0) changes ≤ 0.005 from N = 192/m = 8 to N = 256/m = 11;
  the fixed point's last update changes a_rel < 1e-5 relative.

**MUTATE** (`--mutate`): the AQUAL flux is replaced by QUMOND's (the hidden-ingredient error itself). K3 must FAIL.
Outputs `*_MUTATE.out`, `*_results_MUTATE.json`.

## Result lines (frozen; physics outcomes, not in the exit code)

- **R1 Cassini (D7b recomputed).** AQUAL Q₂ of the canonical law, 4 E × 2 footings × y_t ∈ {none, 60, 66.3803, 77.876,
  140} (turn-off ν_fix = 1 + (ν−1)/(1+(y/y_t)²), its AQUAL μ by inversion). PASS iff −3e-27 ≤ Q₂ ≤ 9e-27 (Hees 2σ) at
  every E; Park 2σ [−2.0e-27, 5.2e-27] secondary. Reported: ratio to 9e-27 and the AQUAL/QUMOND factor per cell.
  "D7b's FAIL survives" iff every cell still fails; "D7b's verdict reverses" iff any footing passes at all 4 E.
- **R2 Wide binaries (D2 recomputed).** AQUAL γ_v(20 kAU), orientation-averaged (D2's 3-point GL in cos θ), g_ext =
  1.778e-10 and 2.078e-10, both footings. "γ_v CHANGES" iff |AQUAL − QUMOND| > 0.005 (D2's own convergence tolerance)
  in any of the 4 cells; else "γ_v = 1.175/1.210 STANDS". Also reported against A24's claim |Δγ| ≤ 0.019.
- **R3 Family (D7c recomputed).** AQUAL Q₂ at 4 E × 2 footings for every D7c SPARC passer on both footings (n = 2 = β = 1,
  β = 1.25, 2, 2.5, 3, 4, 5, 6, standard μ) and for the Q₂-only passer n = 8. SPARC verdicts are taken from D7c unchanged
  (its RAR fits are algebraic; the algebraic law is identical under AQUAL and QUMOND for the fitting used; thin-disc
  AQUAL/QUMOND differences are not computed and are listed as a limit). "No-go SURVIVES" iff no SPARC passer passes Hees
  2σ at all 4 E on both footings under AQUAL; "No-go BREAKS" otherwise, naming the member.
- **R4 D7d consistency.** "D7d CONSISTENT" iff K1b passes for D7d's own (L)/(P) at L★ = 0 and D7d's K4 target (BN11
  3.8e-26 within 10 %) agrees with this lane's AQUAL number within 10 %. Our AQUAL canonical E0–E3 values are reported
  as the L★ → 0 reference D7d's Route N must reach.

## What this cannot show

Uniform static external field; Sun as a point mass; no ephemeris refit; the 3-D binary is D2's single 1+1 M☉ circular
configuration, not the registered population; the cold sector's own density is neglected; the L★ > 0 (screened) case is
D7d's. A pass or fail here is about the unscreened law only.
