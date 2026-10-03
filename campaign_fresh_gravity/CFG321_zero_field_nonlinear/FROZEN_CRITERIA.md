# CFG321 — FROZEN CRITERIA: nonlinear evolution of the ungated chassis at an open zero-field region (recipe G5/G10)

Frozen 2026-10-03, before any CFG321 lane script was run. Nothing below may be edited after the commit that adds this
file. Corrections go in a dated section appended at the end.

**Disclosure before freezing.** A numerical feasibility prototype was run in a scratch directory (outside the repo):
1-D only, a pure-power-law stand-in for the kernel, N = 63/127, eps = 1e-2, data defined on the khronon instead of on
the MOND potential, T <= 100. It was used to choose the solver (chord Newton with a residual merit near the minimum),
the time step rule, T and the window. It showed growth from yhat ~ 1e-4 and a bounded, strongly fluctuating late state
with rms yhat of order 0.1–1. A short 1-D run of the MUTATE kernel (below) hit an indefinite leaf Hessian at t ≈ 11.
No convergence, pair or eps-ladder comparison was run before freezing. No 2-D dynamics beyond a 10-unit timing run.

## 1. What is being tested (committed, not chosen here)

- **The chassis.** The filtered C-H/K khronon completion (L340), ungated: C-H (ACTION.md:95-106) + alpha_c a^2 −
  c_2 (K − <K>)^2, beta = 0, kernel ν_mono through the heat filter S = exp((xi^2/2) Delta) (user decision 2026-09-26),
  causality criterion B. kappa = ½ is FITTED and plays no role here.
- **The record being extended.**
  - FP5 G-2f (a26136bc4) C3: at an open zero-field region the linearisation is BPS khronometric gravity with
    alpha_eff = 2 + alpha_c > 2, so omega^2 < 0 at every k (Hadamard ill-posed). C4 (reported, not load-bearing): below
    y* the band is bounded, k_max xi = sqrt(ln(C/C*)), and the instability saturates at y ~ y*.
  - FP2 D4 (24aae971e): the ungated core's linear cosmology fails; L341 (e9f450b10): sigma_8 = 18–27.
  - CFG294: conditional local well-posedness AWAY from zero-field regions (A1–A5, C3 excludes Z_0). CFG312: the lapse
    condition W <= 0 holds on FRW + Lambda + dust.
- **Parameters.** alpha_c = 3.2e-9 (L340 P1 maximum: the fastest corner, as FP5 C4) for the kernel normalisation and
  y*; alpha_min = 9.624e-14 reported. c_2 enters only the time unit (shown in Part A); conversions use FP5 C4's corner
  c_2 = 0.0667 and xi = 0.04513 pc (L340 S1, canonical ν_mono xi_M).

## 2. The reduced system (to be derived in the script, Part A; the script's result stands if it differs)

Prediction, worked out by hand from FP5's committed scalar block (fields hs, phi, n_z, u; xi_B = 1, lambda = 1 + c_2,
eta = alpha_c, c_CH = 2): the shift is eliminated by the momentum constraint, the lapse by its elliptic equation
(phi = (2u − h)/(2 + alpha_c)), and U is solved per leaf. With alpha = alpha_c, Lambda = 4/alpha^2,
eps = 1/(Lambda − 1), slow time tau = t (c/xi) sqrt(c_2 alpha/((2 + alpha)(2 + 3c_2))), lengths in xi, the MOND field
yhat = |grad S u|/(y* a0) and C* = (2 − alpha)/alpha, the system is

    psi_tautau = −Delta psi + (1 + eps) Delta u[psi],
    u[psi] = argmin_u Int { eps |grad u|^2 − 2 grad psi . grad u + Qhat(|grad S u|^2) },  Qhat'(s^2) = C_T(y* s)/C*,

with conserved energy E = Int{psi_tau^2 − |grad psi|^2} − (1 + eps) min_u F. Its linearisation must give
omega^2/k^2 = (1 + eps)/(Chat sigma^2 + eps) − 1, which equals FP5 B3's c_2(2 − E)/(E(2 + 3c_2)) exactly at
eps = 1/(4/alpha^2 − 1), Chat = C/C*. The only nonlinearity kept is the MOND kernel: at the relevant amplitudes
(y ~ y* ~ 1e-18 a0) the metric perturbations are ~1e-30 and GR's own nonlinearity is negligible (to be quantified).

**The eps ladder (forced by stiffness, declared here).** The physical eps is alpha^2/(4 − alpha^2) ≈ 2.56e-18 (alpha_max).
eps enters only the speed of modes the filter decouples from the MOND sector (Chat sigma^2 ≲ eps), where the healthy
khronon speed is sqrt(1/eps). Explicit time stepping at the physical eps is impossible (dt ∝ sqrt(eps)). The runs use
eps ∈ {1e-2, 1e-3, 1e-4} (1-D) and {1e-2, 1e-3} (2-D). Transfer to the physical eps is claimed ONLY if R4 passes.
This is a numerical continuation of a stiffness parameter, not a knob tuned to a result; no other parameter is varied.

## 3. Data class D (fixed now)

- The initial MOND potential u0 is a Gaussian random field with fixed integer-mode content (grid independent): all
  modes with 0 < |k| xi <= 3, amplitude N(0,1) × exp(−|k|^2 xi^2/4), drawn in a fixed order from seed 321.
- Scaled so that the grid rms of the filtered field yhat = |grad S u0| is 1e-4 (y = 1e-4 y*: "grad U ≈ 0").
- Zero khronon velocity; zero mean khronon gradient g = 0 (an exact zero-field background); the leaf's mean field
  gradient G is solved from g = 0. psi0 follows from the leaf equation.
- Pair data: u0 + delta × (an independent field of the same class, seed 322, scaled to the same rms), delta ∈ {1e-3, 1e-5}.
- Domains: 1-D periodic, L = 16 xi; 2-D periodic, L = 8 xi.

## 4. Runs (fixed now)

- 1-D: N ∈ {63, 127, 255}; eps ∈ {1e-2, 1e-3} at all three N, each with the base run and both pair runs; eps = 1e-4
  base runs at N ∈ {63, 127}. T = 80.
- 2-D: n ∈ {15, 21, 29} per side; eps = 1e-2 base + both pairs at all three; eps = 1e-3 base runs at all three. T = 60.
- Fourier pseudo-spectral space (odd N), kick-drift-kick leapfrog, dt = 0.25/m with m the smallest integer giving
  omega_max dt <= 1 (omega_max = k_max sqrt(1/eps)); the leaf solved to relative residual 1e-10 (accepted at 1e-8).
  Outputs every 0.25.
- Statistics window: [T/2, T]. Growth-phase reference time tau_s: the first output time at which rms yhat >= 0.1 in the
  finest run of that set (dimension, eps); all resolutions and pairs of that set are compared at tau_s.
- Comparisons across resolutions use the Fourier coefficients (normalised by the number of points) of the filtered
  field w = grad S u on the modes common to all grids.

## 5. Decision rule

**R1 — regular and bounded** (every run of §4): no blow-up (finite, max yhat < 1e6); the leaf solved at every step
(residual <= 1e-8); zero indefinite leaf Hessians; energy drift max|E(tau) − E(0)| <= 1e-3 × max E_kin; in the finest
runs the khronon's gradient energy in the top third of resolved |k| <= 1e-6 at every output; the leaf-uniqueness probe
(warm start vs the healthy start u = psi/eps, at tau = T/4, T/2, 3T/4, T of the finest base runs) differs by <= 1e-6
and the leaf Hessian at the solution is positive definite.

**R2 — resolution convergence.**
- (a) Pointwise, growth phase: at tau_s the relative L2 difference of w between the two finest grids is <= 1e-3, and the
  observed order p (fitted against the actual dt, three grids) is >= 1.5, or the finest difference is <= 1e-9.
- (b) Saturated state: for S ∈ {<rms yhat>, <median yhat>, <p90 yhat>, <E_kin>/Vol, <f_pin>} (f_pin = fraction of
  points with yhat < 1, i.e. C_T > C*), |S(finest) − S(next)| <= max(0.10 S(finest), 2 sigma), sigma = the two runs'
  block-bootstrap errors (5-unit blocks) in quadrature.

**R3 — continuous dependence** (base vs pair runs, D(tau) = ||w_a − w_b||_2/||w_a||_2 on the run's own grid).
- (a) Linear in delta: D_{1e-3}(tau_s)/D_{1e-5}(tau_s) ∈ [30, 300] at every resolution.
- (b) No resolution-driven amplification: A = D_{1e-5}(tau_s)/1e-5 satisfies A(finest)/A(next) ∈ [0.5, 2].
- (c) Lyapunov exponent lambda from a fit of ln D_{1e-5} over the outputs with 1e-4 <= D <= 1e-1 (>= 8 points; if not
  reached, (c) is reported "not reached" and passes on (b)): lambda(finest)/lambda(next) ∈ [0.8, 1.25].

**R4 — eps ladder** (transfer to physical eps): at fixed resolution between the two smallest eps (1-D N = 127:
1e-3 vs 1e-4; 2-D n = 29: 1e-2 vs 1e-3): S ∈ {<rms yhat>, <median yhat>, <p90 yhat>, <E_kin>/Vol} agree within
max(0.15 S, 2 sigma), and tau_s agrees within 10%.

**FAIL signatures** (any one; checked at the finest resolutions; FAIL is KILL-class for the ungated chassis's own
cosmology):
- blow-up, or a leaf solve that fails, in a main run;
- leaf non-uniqueness (probe difference > 1e-6, or an indefinite Hessian at a solution): branching;
- R3a ratio < 3 at the finest resolution: an order-one response to infinitesimal data (discontinuous dependence);
- amplification growing with resolution at both steps: A(N2)/A(N1) > 2 and A(N3)/A(N2) > 2, or lambda(N2)/lambda(N1)
  > 1.25 and lambda(N3)/lambda(N2) > 1.25 (Hadamard-type growth surviving the nonlinearity).

**Verdict.**
- **CONDITIONAL** if R1–R4 pass in 1+1 AND 2+1 and every control passes: a regular saturated state with continuous
  dependence exists for data class D, conditional on the reduced model (§2 scope) and the eps continuation.
- **FAIL** if any FAIL signature occurs.
- **OPEN** otherwise (R2 or R4 fails, or R1's energy/spectral criteria fail without blow-up, or a control fails).
- If the MUTATE does not fail (below), the verdict is capped at OPEN: the pipeline's discriminating power is unshown.

## 6. Controls

- **C-SYM (load-bearing).** The scalar block is rebuilt in-lane from the action (FP5's ADM machinery, copied, not
  imported); the Schur reduction gives the §2 system; its dispersion equals FP5 B3's exactly; the dimensionless map is
  exact; the energy functional reproduces the linear V_k = k^2 psi^2 ((1 + eps)/(Chat sigma^2 + eps) − 1).
- **C-FP5 (load-bearing).** FP5 C4's three rows (k_max xi, max growth in c/xi, e-fold in yr) reproduced from this lane's
  kernel to 1%; y*_T = 2.5600e-18 reproduced to 1e-3.
- **C-LIN (load-bearing).** The nonlinear code, linearised about a uniform background yhat_b = 1e-4, reproduces the §2
  growth rates/frequencies to 1%: 1-D (k ∥ G: C_L) and 2-D (k ⊥ G: C_T), including at least one mode on each side of
  the band edge k xi = sqrt(ln(Chat))).
- **C-GR (load-bearing).** MOND sector off (the C → 0 limit: GR + the healthy BPS khronon): at T = 10, eps = 1e-2,
  1-D N ∈ {63, 127, 255}, the error against the exact solution converges with order >= 1.8, energy drift <= 1e-3
  relative, and pair separation stays bounded (max D/delta <= 10) and linear in delta (ratio 100 ± 1%).
- **C-BKG (reported).** FRW + Lambda + dust enters only through k = 0 (leaf average) and through W ~ H^2: report
  H xi/c, the e-fold time against 1/H, and the dust displacement over the growth phase.
- **MUTATE** (env CFG321_MUTATE=1; outputs suffixed _MUTATE): the kernel is replaced by the record's turning kernel
  μ_exp (C_L = (1 − x)/(e^x + x − 1), XC5 E4 / recipe), with a0 -> y* a0 so that its deep-MOND end has ν_mono's
  normalisation C_T -> yhat^(−1/2) and its turning point x = 1 sits at yhat = 1 − 1/e. At the record's own placement
  μ_exp differs from ν_mono by ~1e-9 at yhat ~ 1 and could not discriminate. The MUTATE runs the 1-D eps = 1e-2 set
  (three N, base + pairs) and the 2-D eps = 1e-2 set (three n, base + pairs). It must NOT return CONDITIONAL (rc = 1).

## 7. Scope (stated in advance)

- This lane says nothing about growth or sigma_8. L341's failure (sigma_8 = 18–27) and FP2's failed linear cosmology
  stand whatever the verdict.
- Reduced model: principal weak-field order of the GR + khronon block (frozen coefficients, Minkowski leaves on scales
  << c/H), MOND kernel fully nonlinear; 1+1 and 2+1 only; periodic leaves; one data class.
- A CONDITIONAL here is not well-posedness of the full chassis and not a pass for candidate B. It removes, if it
  holds, only the zero-field obstruction CFG294 excluded (its C3 / A5), for this data class.
- Reported, not graded: the post-saturation yhat distribution (percentiles, the fraction with yhat < 1e-3, i.e. whether
  open zero-field regions survive, the XC5 E6 sqrt(eps)-Osgood reading), and the saturated energy density in physical
  units against rho_Lambda c^2.
