# Focused review of the static restoring-kernel discriminator

19 October 2026. Reviewer: `/root/collective_restoring`, a sibling mathematical lane. This review changes no source in the reviewed `static_kernel/` scope.

**Primary verdict: proved as written**, for the finite-dimensional fixed-source stable material Legendre class explicitly stated in the note. The finite-band bound is sharp, and the at-most-one Jeans crossing claim follows. This verdict does not extend the claim to all quantum phases, all matter response functions, or a full relativistic metric constraint problem.

Reviewed sources and SHA-256:

| Artifact | SHA-256 |
|---|---|
| `../static_kernel/STATIC_KERNEL.md` | `66decd0ab054f7a986aaba7b84c4c6a3d2e6f9b508ba4672a9e63755215e9d04` |
| `../static_kernel/check_kernel.py` | `57399afcf5dd1abe869e3b19b850aa026fa201c1bedb9a454fcf7711f9ab2c2b` |
| `../static_kernel/contract.json` | `def06b8c7c6b6a10fd8fc5333aa10537caaf23f3dfd54df80a99224e0040aa30` |
| `../static_kernel/run_001/results.json` | `1f3ff03814cf6e1bd4641e54eff54c74bab2154001cafa5a8c54ade72b2fce5e` |
| `../static_kernel/run_001/manifest.json` | `81454919e3899b0f87c38c4816c629a491ac344dc47e5ce05af9ec7018b7e4fc` |

The mathematical checkpoint is `CE-PARTICLE-2026-10-18 / CE-FM-085`, requested initial revision `9516ee01c79f35c04b7556050669ba77b0c98b99`. The reviewed manifest records the actual concurrent repository revision and dirty state; this review relies on the listed bytes rather than an assumption that HEAD stayed fixed.

## Exact reviewed claim

For every finite Hermitian pair `A,B`, `B>=0`, every connected positive-real interval `I` on which `K(z)=A+zB>0`, every fixed source vector `q`, and fixed real `s>=0`, assume `chi(z)=s+q^dagger K(z)^-1 q>0`. Then `h=1/chi` is nondecreasing. Here `z=k^2`, and `h` is interpreted as a constrained material density curvature only under the declared linear density-source/Legendre convention.

For positive `K_g` and `[z_a,z_b]` contained in that admitted interval, uniform relative approximation of `K_g/z` by `h` to error `epsilon<1` requires

\[
\epsilon\ge\frac{z_b-z_a}{z_b+z_a}.
\]

The bound is sharp in the nondecreasing class. The gravitationally dressed material curvature `h(z)-K_g/z` is strictly increasing, hence has at most one zero on each admitted connected interval. Existence needs a sign change or the separately stated endpoint range conditions.

## Dependency reconstruction

1. **Inverse differentiation, internal proof.** Differentiating `K K^-1=1` gives `(K^-1)'=-K^-1 B K^-1`. Since `K^-1` is Hermitian, `chi'=-(K^-1 q)^dagger B(K^-1 q)<=0`. Consequently `h'=-chi'/chi^2>=0`. The sign of any component of `q` is immaterial. Positive semidefiniteness of `B`, not commutation of `A` and `B`, is the required sign input. `A` itself may be indefinite if the admitted `K(z)` is positive.
2. **Density curvature interpretation, internal constrained minimization.** Without a local auxiliary, `x=K^-1 q delta_rho/(q^dagger K^-1 q)` satisfies the density constraint and Euler equation; substitution gives energy `|delta_rho|^2/[2q^dagger K^-1q]`. Uniqueness follows from positive `K`. For `s>0`, append a variable `sigma`, energy `|sigma|^2/(2s)`, and total density `q^dagger x+sigma`. The enlarged positive kernel is `diag(K,1/s)` and its susceptibility is exactly `q^dagger K^-1q+s`. At `s=0`, omit the auxiliary. This checks the convention rather than identifying an unrelated response with an energy curvature.
3. **Finite-band necessity, internal endpoint argument.** The approximation implies `h(z_a)>=(1-epsilon)K_g/z_a` and `h(z_b)<=(1+epsilon)K_g/z_b`. Monotonicity requires the first lower bound to be no larger than the second upper bound. Rearranging gives the claimed error. No interpolation assumption or small-`k` expansion is used.
4. **Sharpness, explicit construction.** Set `h_*=2K_g/(z_a+z_b)`. The relative error `h_*z/K_g-1` is linear in `z`, with equal opposite endpoint extrema of magnitude `(z_b-z_a)/(z_b+z_a)`. This construction is available even within the theorem's matrix class: a one-dimensional constant positive `K` with `B=0`, `q=1`, `s=0` realizes any desired `h_*>0`. Thus there is no hidden mismatch between monotone-class sharpness and the allowed finite matrix setting.
5. **Jeans crossing, internal proof.** Differentiation gives `(h-K_g/z)'=h'+K_g/z^2>0`. Continuity on the admitted band then gives at most one zero, and exactly one if two admitted endpoints have opposite signs. The note correctly distinguishes this uniqueness statement from an assertion that a zero always exists. Positive `B` does not turn the attractive Newton term into a positive restoring term.
6. **Scalar comparison, internal elimination.** Minimizing `g_0 rho^2/2+[(z+M_s^2)phi^2]/2+g_s rho phi` over a healthy real static scalar gives `(g_0-g_s^2/(z+M_s^2))rho^2/2`. Its derivative and the critical tuning in equation (8) have the stated signs. A positive Coulomb constraint sector is outside this elimination problem and is correctly kept separate.
7. **Physical dictionary, checked and restricted.** The displayed retained-source NR amplitude matrix, gradient matrix and source vector agree with the pinned prior single-sign response note. The phase stationary equation eliminates the background linear terms; the density-source vector contains the negative source amplitude as displayed. That sign does not change step 1. A same-charge matching correction changes static entries, while the canonical gradient matrix remains positive. In the neutral calculation the even sector has the same no-flow static form, but the full homogeneous neutral state has a separate odd instability and cannot be declared stable using only the even block. The reviewed note states this caveat.

No external theorem is needed for these implications. The positivity and linear-source hypotheses are explicit mathematical inputs, not the output of the finite numerical samples.

## Obligation results

| Obligation | Result |
|---|---|
| Hermitian inverse derivative and monotonicity | Passed |
| Noncommuting `A,B` and arbitrary source signs | Passed |
| Local nonnegative `s` realized by an auxiliary density | Passed |
| Material density Legendre convention stated rather than assumed for arbitrary response | Passed |
| Relative finite-band bound and all intermediate momenta | Passed |
| Sharpness within the actual admitted matrix class | Passed |
| At-most-one crossing versus existence conditions | Passed |
| Critical scalar tuning and exchange sign | Passed |
| Retained-source original particle dictionary | Passed within its NR/coherent/stable-band assumptions |
| Neutral full-state stability qualification | Passed as a qualification; that particular neutral saddle is unstable |
| Full relativistic lapse/stress Legendre interpretation | Conditional/outside the scalar theorem; correctly identified as such |
| All-state/all-loop/incompressible-phase exclusion | Out of scope and explicitly unclaimed |

## Finite evidence and implementation audit

I read the complete script, contract, result and manifest. The script uses exact SymPy rational/algebraic expressions for the inverse derivative, KKT constraints/Euler equations/energies, endpoint algebra, and scalar sign identities. It has five declared matrix cases, three fixed positive `z` values per case, and four momentum-band ratios. The actual retained-source example is the documented bare-RWA convention; it is not presented as a threshold-corrected physical fit. The finite output contains 75 passing controls and its case counts agree with the iterator. Binary64 conversions occur only in displayed summaries; they do not establish the symbolic signs.

I reran only the installed manifest validator, with project-root hash verification. It reported `valid evidence record (run status: completed)`. No new scientific run was needed. The finite examples are supplementary controls for a universal argument already supplied by the inverse-matrix and endpoint proofs; their count is not used to establish that argument.

## Scope and remaining implication

The strongest safe conclusion is that the stated canonical stable homogeneous no-flow finite-amplitude/linear-source class cannot supply the positive `K_g/k^2` material stiffness, nor approximate it with small uniform relative error over a broad momentum band. This is stronger than a zero-momentum Taylor objection because it applies to any admitted finite band and retains exact massive-source spatial gradients.

The theorem does not decide whether another physically established state of the same microscopic system has a momentum-dependent source, nonlocal exact kernel, density gap, additional constraint, boundary support, nonzero flow or inhomogeneous response. Such a proposal must identify which theorem hypothesis fails and compute its actual source-specific susceptibility. The general all-phase question is left open, as the reviewed source states. No revision is required to the reviewed theorem.

Review provenance: independently reconstructed critical algebra in a sibling lane, after receiving the exact statement/proof and declared scope. This was not a fresh-context blind review: the coordinator had previously outlined the target monotonicity question. Independence here means the inverse/KKT/endpoint derivations were checked directly from their definitions rather than inferred from the author's conclusion or finite pass count. The verdict applies only to the hashed source above.
