# CFG353 auxiliary action: lapse-weighted adjoint and a different global zero

**Primary verdict:** the stated action does give the ordinary leaf Poisson constraint. A variable lapse does not turn the multiplier equation into weighted-divergence Poisson. However its adjoint equation and global zero convention differ from the N=1 equations tested in the script. Thus the reported legality/adjoint test is a constant-lapse reduced check, not an audit of the full metric-coupled auxiliary action. This gap does not rescue the reader from its zero-point obstruction.

Read-only inputs are pinned in lapse_provenance.json, including the frozen criteria reference c9d9a1d7b7a7accbf773424a5180f35ac85896f4 and actual working-tree hashes. No Claude script or Lean file was executed or edited. README SHA256 is 0ee04098ae5ccf5a2c507326f1a65535f207b8dda431ea17ba2b333a0f776a1f; frozen criteria 88d15b904b2fdd34c8ba61d76d5420d087e24779ba7f372ae51b23e7db35ce43; script 5db5b63b1bf9c86cc52c7b05eeacafd6fba95d5b9c4c893a8bc1d9d7e2d05a68. These are working-tree inputs, not an assumption that a commit authenticates the new outputs.

## Direct variation of the actual action

On a compact/periodic leaf with fixed h,N during the auxiliary variation, positive lapse N, and Δ_h self-adjoint under dV_h=√h d³x, the proposed sector is

Saux+Sgate=∫dt∫dV_h N{μ[Δ_hΦ−k(ρ−ρbar_h)]+ν(t)Φ+f(Φ,DΦ)L_M},
k=4πG, ρbar_h=∫dV_hρ/∫dV_h.

Use smoothed f for ordinary Euler equations; a sharp gate has distributional variations. Assuming the quoted L_M has no independent Φ dependence, varying the local μ gives

N[Δ_hΦ−k(ρ−ρbar_h)]=0.

N>0 therefore gives exactly Δ_hΦ=k(ρ−ρbar_h). The h-average source subtraction makes the Poisson compatibility condition hold. It is a legitimate leaf-scalar equation. There is no rule requiring this primal operator to be self-adjoint in the N-weighted measure: its multiplier has a different adjoint.

Varying Φ and integrating by parts in the h measure instead gives

Δ_h(Nμ)+Nν+N L_M f_Φ−D_i[N L_M f_{D_iΦ}]=0.

Thus the auxiliary adjoint is Δ_h(Nμ), not NΔ_hμ and not D_i(ND^iμ). Equivalently NΔμ+2DN·Dμ+μΔN appears. Integration determines the global ν from

ν∫dV_hN=−∫dV_h N L_M f_Φ,

when the divergence terms have vanishing surface flux. The multiplier kernel is μ→μ+C(t)/N: Nμ is shifted by a leaf constant. This is also a gauge freedom of the auxiliary action because both ∫ΔΦ and ∫(ρ−ρbar_h) vanish. A solvable elliptic adjoint therefore need not introduce a growing unconstrained conjugate, but this observation is not a complete gravity/clock Dirac or health audit.

Varying the global ν gives

∫dV_h NΦ=0.

This is N-weighted zero mean. The frozen E0 convention was ∫dV_hΦ=0. They coincide only for a lapse constant across the leaf (including exact FRW), or accidentally for a particular profile. The stated action does not enforce the stated h-mean E0 for an arbitrary physical lapse.

## Exact countercontrols and density reaction

On a flat periodic circle take N=1+ε cos x with 0<ε<1, Φ=cos x and μ=cos x. Then ∫Φ=0 but ∫NΦ=πε≠0. The action's solution convention shifts the same Poisson field to Φ=cos x−ε/2. Its gradient is unchanged, while the denominator of the estimator changes.

For the adjoint, (Nμ)″=−cos x−2ε cos 2x whereas (Nμ′)′=−cos x−ε cos 2x. The difference is −ε cos 2x, an explicit variable-lapse term. Neither alternative is the original adjoint.

The average source also contributes to the reaction. At fixed h,N, the density-dependent multiplier piece gives

δSaux/δρ(y)=−k√h(y)[N(y)μ(y)−⟨Nμ⟩_h].

Factoring out the physical spacetime measure N√h gives −k[μ−⟨Nμ⟩_h/N]. One cannot use the flat-lapse μ−⟨μ⟩ formula unchanged for an inhomogeneous lapse. Additional variation is required when ρ is a metric-dependent matter observable or when h/clock is varied; this fixed-background formula does not replace those stress equations.

The script's legality block (around lines 422–477 at the pinned revision) uses Lag=μ(φ″−ρ+ρbar)+νφ+F(s)L_M with no lapse. Its periodic Fourier adjoint test likewise solves a symmetric flat Poisson operator and takes an unweighted mean. Those tests are coherent N=1 reductions. The quoted 2.3×10^-8 finite-difference agreement and translation sum were inspected, not rerun, and cannot authenticate the missing N products, weighted ν equation or metric reaction.

The on-shell value μ(ΔΦ−source)=0 also does not erase its stress: varying the metric changes Δ_h, source density and the global average before imposing the constraint. The νΦ term vanishes after leaf integration with its actual weight, not pointwise in the lapse equation. Full conserved metric/clock reaction remains a separate obligation even though Φ and μ have no explicit time derivatives in a fixed foliation.

## Why the existing zero-point no-go survives

For any strictly positive N, a nonconstant continuous Φ with ∫NΦ=0 must have positive and negative values. A generic simple nodal zero has |DΦ|≠0 and the estimator |DΦ|²/|Φ| still diverges there. The periodic control above has gradient squared 1−ε²/4>0 at each zero of cos x−ε/2. Fresh controls verify this exactly at ε=.1,.5,.9. Changing h-mean to N-mean therefore does not remove the nodal mechanism behind the E0 failure, or provide the host-local-infinity zero convention.

Weak-field lapse changes may make the numerical zero shift higher order when N−1 and Φ/c² are both small; that is an approximation needing its own bound, not an exact equality of conventions. I do not revise or authenticate the numerical host/edge/data scores from this action-level audit. Exact FRW has spatially constant N and is unaffected by this discrepancy.

## Legitimate alternative formulations and their new obligations

A multiplier redefinition μtilde=Nμ recovers the ordinary self-adjoint Δ_h acting on μtilde while keeping the primal Poisson equation. It does not turn NνΦ into an unweighted global-zero condition.

If h-mean E0 is required exactly, its global constraint term must be written explicitly with dV_hνΦ (equivalently the N-weighted integrand νΦ/N), with the appropriate time-reparametrization transformation of its global multiplier. That is a distinct specified term, not what the quoted action currently writes.

If instead one deliberately starts from −∫N dV_h Dμ·DΦ, the primal becomes D_i(ND^iΦ)=Nk(ρ−ρbar_N), or ΔΦ+D ln N·DΦ=k(ρ−ρbar_N). Its compatibility condition requires the N-weighted source mean. This is another theory and changes the reader's computed potential. Neither replacement should be silently credited with the frozen action's scores.

The immediate correction is therefore to narrow the existing legality verdict to its N=1 tested scope and declare which full zero/adjoint action is intended. The ordinary Poisson primal need not be abandoned. A tidal replacement avoids additive-potential zero dependence, but still needs this varied auxiliary action and the separate phase-information issue identified in ROOT_PHASE_INFORMATION_LEMMA.md; this audit adds no claim that density alone selects turnaround.

## Fresh independent evidence

lapse_main_a passes exact variable-lapse primal/adjoint identities, global-zero counterexample, density-average reaction and periodic nodal controls. lapse_control_adjoint fails when the lapse-product derivatives are dropped; lapse_control_zero fails when the h-mean is substituted for the actual global multiplier condition. All three standard manifests validate with current input/output hashes. These are independent bounded controls and a direct analytic derivation, not reruns of Claude's evidence or a full action-health certificate.
