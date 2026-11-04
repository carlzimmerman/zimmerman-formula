# Independent final CC10 audit

**Claim audited.** The post-memory passive peak bounds the remaining pair loss from the specified endpoint; the fixed-pole neutral-decay benchmark produces the reported conditional hard-χ source; and the exact angular backend and explicit-hole adapter implement the declared finite quantum number operator and its Jacobian.

**Primary verdict: correct only after a stated restriction.** These local mathematical and numerical claims pass the independent checks described below. They do not establish that the supplied endpoint or a new warm trajectory is a complete physical history. I found no material normalization error in the 142.43×/37.97× tail comparison, the conditional decay/free-streaming calculation, or the number-Jacobian sign chain.

The first missing full-history implication is the physical closure: the finite, diagonal group-population generator must represent the common evolving state, including the fourfold neutral-singlet sector or a justified reduction of its density matrix. Exact angular integration removes an angular discretization error; it does not establish that reduction, momentum/phase convergence, or a bridge from the early warm state to the prescribed late memory endpoint. Those obligations precede interpreting either endpoint as a completed cosmology. The root is auditing the neutral coherence issue separately; no outcome from that unfinished audit is assumed here.

## Passive peak and future tail

Let Γ₀ be a positive definite lower form bound for the lab-frame neutral exit operator after removing its common boost factor, and let B(t) be additional positive local absorption. Hermitian, possibly noncommuting, time-dependent detuning contributes zero to the real period-averaged energy identity. With constant forcing v, if R is the actual neutral exit rate, then

    R ≤ 2 Re<a†v>
      ≤ 2 sqrt(<a† bΓ₀ a>) sqrt(v†(bΓ₀)⁻¹v)
      ≤ 2 sqrt(R) sqrt(v†Γ₀⁻¹v/b).

Thus `R ≤ 4 v†Γ₀⁻¹v/b`. This also proves the stated extension to a stronger time-dependent neutral exit matrix: use its actual R in the first and last inequalities. A positive decomposition of the production Gram and the physical source prefactor then give

    σv ≤ Tr(G Γ₀⁻¹)/(E₁E₂M) ≤ Tr(G Γ₀⁻¹)/(m_min²M).

The boost cancellation and the factor of four at `m=M/2` are correct. Source normalization that varies with time requires the corresponding upper bound in the Γ₀⁻¹ forcing norm. This argument requires periodic passive local dynamics; it is not a result for an unspecified active/nonlocal kernel, arbitrarily varying production Gram, or spectrum that leaves the retained mass envelope.

For `n=n₊+n₋`, charge symmetry gives `n₊n₋=n²/4`. Removing two carriers per event yields `dY/dt=−sσvY²/2`. With conserved comoving entropy and the declared radiation continuation, `s/H=(s_end/H_end)/a`, hence

    Δ(1/Y) ≤ s_end σ_peak/(2H_end),
    Y_future ≥ [Y_end⁻¹+s_end σ_peak/(2H_end)]⁻¹.

The stated sufficient extension `H(a)≥H_end/a²` is valid under its assumptions. For a conserved positive total stress tensor in a flat Friedmann background, `ρ−3p≥0` implies `d(ρa⁴)/d ln a≥0`. Changes in entropy, additional loss reactions, or a different microscopic spectrum require a different argument.

Independent reconstruction from the raw width/Gram matrices and endpoint, followed by direct integration of the **yield** equation rather than its inverse, gives:

| Width lower bound | Peak σv [μ⁻²] | Future floor | Floor / charged gate | Required total peak multiplier |
|---|---:|---:|---:|---:|
| Vacuum Γ | 15741.99983725 | 8.09083838256e-14 | 142.434919602 | 267.576325821 |
| SSS floor | 97360.19095551 | 2.15708537002e-14 | 37.974344157 | 43.263950452 |

The direct nonlinear yield integration agrees within 7.3e-12 relatively. The inner-turning-point correction is 1.000000254938, as reported. These are conditional continuation bounds from `Y_end=1.72351105362e-13`, not exclusions of all early histories or additional depletion processes. The SSS-only width is a favorable auxiliary envelope, not an independently evolved occupied bath.

As a separate implementation control, I solved a three-state noncommuting periodic system in Fourier space, including a neutral exit matrix that varies above Γ₀ and positive charged absorption. Its output is 0.273886866 of the derived peak; its energy identity residual is 2.25e-16 of the peak normalization. This tests the stronger-exit extension by an algorithm distinct from the author's periodic ODE control. It does not replace the analytic proof.

## Conditional hard-χ source

The decay-source normalization and units reconstruct correctly. For nonrelativistic parents present well before decay, the conditional source has `u=Γt` distributed as `e⁻ᵘ du`, rest-frame momentum `p*=M/2`, conserved comoving momentum, and

    α=p₀/mχ=(M/2mχ)a_birth,
    v(a)=α/sqrt(α²+a²),
    λ_FS=c ∫ v(a) da/(a²H).

I independently built the entropy-conserved EOS scale factor, solved the cosmic **log-time ODE** instead of using the production cumulative trapezoid clock, and integrated propagation adaptively from each birth epoch. The raw source inputs give:

| Source | p*/mχ | Conditional one-χ branch | Lifetime | Independent mean λ_FS |
|---|---:|---:|---:|---:|
| S8_0 | 2.526395897e7 | 0.381805664 | 4.39262604 ms | 302.732512 Mpc |
| S3_0 | 9.648601439e7 | 0.162569886 | 9.18241567 μs | 80.778217 Mpc |

The independent means differ from the pinned 302.731278/80.777828 Mpc by at most 4.82e-6 relatively. The median temperatures agree within 5.07e-6. The large margin over a 1-kpc benchmark is robust in this stated early-NR, fixed-mass, collisionless source model. Neither a long distance for a small component nor the finite width scan is an all-DM exclusion or a transfer-function calculation.

Every χ yield and mixed branching fraction remains conditional on converting the soft gaugino insertion into a gauge-complete on-shell amplitude. The earlier 15.3% triplet gauge-parameter variation is not repaired by this cosmological propagation. Gauge-only rows with zero χ branch are hypothetical shape diagnostics, not extra χ production.

The gauge-radiation formula `Σ Y_i M_i(1−B_i)<a_decay>` is correctly normalized **for direct gauge-pair branches**. Division by `3Tγ0/(2g_s0)` and the standard one-neutrino photon ratio gives the stated gauge energy-equivalent ΔN_eff. This is not a total mixed-decay energy ledger: a mixed decay also emits a hard nonabelian gaugino, and χ kinetic energy is distinct from its quoted rest-density fraction. Their subsequent energy/decay/interactions are not tracked by this module. The root has been notified of this scope requirement.

The late and warm yield normalizations are explicitly different packets. In particular the warm values are a transplanted checkpoint sensitivity, not parents proven to arrive at the pole with those yields. EOS central-value interpolation and numerical refinement also do not propagate the tabulated physical EOS errors, microscopic branching uncertainty, or the few-percent background-backreaction approximation.

## Exact angular operator and explicit holes

On each daughter-energy stencil interval the weights have the form `a+b u`. With strictly positive occupations and availabilities, the forward/reverse products are exponentials of affine functions of u. The number RHS therefore needs only moments I₀ and I₁; differentiating its physical-number dependence adds I₂ and a single `1/measure` per differentiated occupation. The implemented small-slope series and large-slope formulas agree with independent adaptive integrals through `|B|=1000` and across the small/large branch, with maximum relative scale error 4.54e-14.

For two physical scalar→fermion+fermion test reactions, with distinct and identical daughter species, I reconstructed daughter energies directly as functions of the original decay angle. Independent adaptive vector quadrature used its own energy brackets and did not consume the exact backend's segment arrays. The RHS agrees within 4.66e-16. Duplicate daughter indices are correctly accumulated by the sparse scatter.

I then differentiated that pointwise daughter-energy integrand before quadrature. Its full number Jacobian agrees with `AngularExact.number_jacobian` within 1.39e-15. The source frozen at

    angular_exact.py: 40e83d3bd666b7642af8766bef057e634cd82c1c921aaead06a6b5620a2b1d9a

implements the claimed finite-projection angular integral to floating accuracy. It is not the continuum momentum collision integral. At zero fractional child factors the finite projection is non-Lipschitz; the documented `1e-280` denominator is a numerical one-sided regularization, not an exact Fréchet derivative there. Separately supplied f and availability are two numerical representations of the same physical state; the Jacobian follows the physical tangent `d availability=η df`, not a derivative holding that supplied availability artificially fixed.

For a number backend with `J_Y=d(dY/dτ)/dY`, represented coordinates satisfy `dY/dZ=diag(s)`, where s is −1 for holes and +1 for number coordinates. Their RHS is `diag(s) C(Y)`, so the adapter correctly uses

    J_Z=diag(s) J_Y diag(s).

There is no additional `1/measure` in the adapter. Three mixed coordinate choices in both reactions agree with the independently differentiated quadrature chain within 1.77e-15. `protocol_holes.py` frozen at `4025d729b63b5e6255c4cc9ce97888d84087ecc0e9abfd6e5b4253d57862d1bf` passes this check.

An independent 80-digit Decimal backward-Euler scalar-extent solve also reproduces the implicit adapter's fermionic holes to 4.22e-15 relatively for measures 1e-12, 1e-20 and 1e-24. At the smallest measure the retained hole is 2.33333433333e-24 even though the displayed f rounds to one. The gross-flux tolerance is an explicit floating-point allowance; this review does not turn its fixed `32 ε` prefactor into a rigorous global rounding-error theorem for arbitrary event counts.

`protocol_average.py` correctly averages number RHS/Jacobian/gross terms while retaining each phase's collision energy. A nontrivial two-phase control has local energy rates below 4.2e-17 but an averaged-energy collision rate −0.00640372569. Thus the average energy is correctly **not** treated as a local collision invariant; that rate belongs in the scalar-action covariance.

The additional frozen fast builder at `c623c5b612de6ef37216a51112c2ff7bd620970d5faffae7c362df0ef712531e` reproduces exact RHS/Jacobians exactly in the two six-node tests, including the zero parent-momentum node and duplicate daughters. I read its vectorized cuts/brackets and weighting. This is bounded implementation evidence, not an exhaustive proof for all momentum grids or a fresh full warm run.

## Provenance, failed check and coverage

The new aggregate `run001` is intentionally retained with status **failed**: two initial full-column finite-difference checks used an occupation step of 2e-6 and showed errors of order 1e-6. All other component checks passed. No mathematical source was edited. The separate `run_jac001`, status **completed**, resolves the discrepancy using independent differentiated quadrature and a step scan: the finite-difference error falls to 1.54e-8/3.39e-8 at step 1e-4, then rises as subtraction cancellation dominates. This is a limitation of that initial numerical check, not an observed Jacobian defect.

The substantive controls took 0.297 s and 0.072 s, with measured macOS peak RSS 80,756,736 and 66,650,112 bytes. Both used fresh v2 manifests, wall cap 180 s, CPU cap 175 s and one numerical thread. Both manifests validate, including the failed evidence record. The post-memory, production, angular, protocol and completed protocol-average production manifests also validate with project-root input/output hashes. Exact argv, code/data hashes, observed versions, resource limits and dirty repository revision are in `provenance.json` and the run manifests.

The EOS source was independently authenticated as [Saikawa–Shirai, arXiv:1803.01038v2](https://arxiv.org/pdf/1803.01038v2), dated 17 May 2018. Appendix A identifies the ancillary dataset; Appendix B supplies the entropy-conservation relation. The retained [exact-version table](https://arxiv.org/src/1803.01038v2/anc/standardmodel2018.dat) matches local SHA256 `a4bf5f18dacb084a00e7202a29c689b4ae385950cfeb00be69c98aeb30e8014b`. No PDF was retained and no PDF hash is asserted.

This is a fresh isolated independent audit. It reuses the declared component-model inputs and reads the production records, but the critical controls use different numerical formulations. I did not independently rerun the full angular warm-state case set, root's new action/FRW-work integration, the new warm trajectory, or a four-state warm coherence evolution. The old review is untouched. No file outside this new `independent_review/final/` directory was edited.

**Strongest safe conclusion.** The passive continuation fails the charged gate under the declared endpoint/model assumptions; the named conditional neutral-decay source is very hot; and exact finite-projection angular integration with the explicit-hole number interface is correctly normalized in the tested domain. The first unproved physical bridge remains the common evolving-state closure and its convergence, followed by the transition to late coherent memory/cascades and on-shell mixed-gaugino matching.
