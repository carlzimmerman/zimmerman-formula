# Actual-vacuum layer research: current status

Checkpoint **YM-LAYER-2026-10-28-C1**, 28 October 2026.

**The requested uniform weak-coupling layer bound that survives exact coarse
graining is not proved. The Yang–Mills mass gap remains open.** This attempt
establishes two useful extensions for the actual finite-volume vacuum,
proves conditional layer criteria, and rules out several insufficient
shortcuts. It does not establish a new interacting gap regime or a novelty
claim. The published paper and Zenodo record were not changed by this work.

## What the attempt established

| Claim | Current mathematical status | Scope and limitation |
|---|---|---|
| The verified fixed-block vacuum bound survives arbitrary coordinate marginalization with exactly the same constant. | **Proved; independently audited.** | Actual SU(N) finite-volume vacuum, all couplings x>0, original link geometry and original x,a. No loss proportional to the number of integrated variables. This is not a rescaled Wilson-action theorem. |
| Restricting the ground form to retained-coordinate functions gives precisely the weighted gradient form of the marginal measure. | **Proved; independently audited.** | Exact Galerkin compression. Energy-minimizing Schur elimination is a different operation. |
| Every fixed compact coordinate split has a bounded minimizing graph correction and the exact closed-form domain required for one-step normalized Schur elimination. | **Proved; independently audited.** | Applies to the actual smooth positive vacuum. The bound uses score derivatives whose volume and weak-coupling behavior are uncontrolled. Direct-original and unnormalized nested coordinate graphs are also covered. |
| Local conditional bounds plus a specified influence matrix bound give a layer-cardinality-uniform lower bound. | **The implication is proved; its actual weak-coupling input is open.** | Three alternatives are available: Dobrushin influences, mixed log-density Hessians, or triangular score influences of successive marginals. |
| Links sharing no bare plaquette can still be conditionally dependent in the actual vacuum. | **Proved; independently audited.** | Explicit two-adjacent-square SU(2) example; dependence appears at order g², where g=2b/x² is small, hence in a strong-coupling expansion. This does not show large influence. |
| Finite-volume log-vacuum coefficients have connected-plaquette support. | **Proved after an audited scope correction.** | Ordinary square plaquettes with four distinct link variables. No coefficient norm, volume-uniform convergence or weak-coupling conclusion. |
| Good bounded-block conditional gaps alone force a whole-layer gap. | **Refuted as a general inference.** | Gauge-invariant compact SU(2) measures, local compact rotor actual vacua on trees, and local oscillator actual vacua provide distinct counterexamples. None is a Wilson cubic-lattice counterexample. |
| Conditional-expectation Schur elimination automatically preserves a Markov diffusion form. | **Refuted.** | An exact four-state reversible example loses the Markov contraction property before and after metric normalization. |
| A full-kinematic layer containing a vertex star can have a lower bound c/a with c>0 independent of x as x→0. | **Refuted under full vertex gauge symmetry.** | A charged admissible trial gives D_F≤x C_F/(2a). It is excluded from the physical gauge-invariant sector. An x/a lower bound is compatible. |

## The positive coarse-stability statement

Let B be a bounded set of original links, let v be any collection of other
links to integrate out, and let z denote the remaining links. The published
actual-vacuum estimate says, uniformly in all configurations,

    psi(u,v,z)/psi(u',v,z) <= R_B,
    R_B=kappa_N(s)^|B| exp(4sbp_B/x²).

Squaring and integrating the same v on both sides proves the identical
density-ratio bound for the marginal. Therefore every such marginal has
the same conditional gradient gap

    lambda_B >= C_F/R_B²,
    C_F=(N²−1)/(2N).

No new proof of a Wilson Hamiltonian representation is needed for this
inheritance. Repeated marginalization does not multiply this local loss.
The full argument is in [coarse/PROOF.md](coarse/PROOF.md), §3, (19)–(21).

The additional domain result uses integration by parts to show that the
mixed retained/discarded form is first order. With centered conditional
score sigma, S0=sup|sigma| and S1=sup|div_rho,Y sigma|, it proves

    ||C|| <= S0/sqrt(lambda)+S1/lambda.

This verifies boundedness and the one-step Schur form domain at each fixed
finite lattice. It does not turn these constants into useful uniform ones.
See [DOMAIN_EXTENSION.md](coarse/DOMAIN_EXTENSION.md).

## The exact missing layer estimate

One sufficient route partitions a layer into bounded blocks and integrates
them successively, always using marginals of the **actual** vacuum,
conditional on the layer exterior. Let lambda_i be the conditional gradient
gap of block i. Let M_ki bound the covariance functional with the centered
score in block i when block k is integrated, as in (13) of the coarse proof.
Define the strictly lower triangular matrix

    R_ik=M_ki/sqrt(lambda_i), k<i; R_ik=0 otherwise.

If lambda_i>=lambda_* and ||R||_(ell²→ell²)<=r<1 uniformly in layer size,
volume and exterior configuration, then the proved theorem gives

    D_layer >= (x/(2a)) lambda_* (1−r)².

The inherited block theorem supplies lambda_*. It does **not** supply r<1.
The covariance involves log densities of successive actual-vacuum
marginals, not the bare plaquette potential. The SU(2) perturbative example
shows why bare plaquette separation cannot be used to set these influences
to zero. The mixed-Hessian alternative is similarly demanding when paired
with the exponentially small available lambda_*.

## What still prevents a mass-gap conclusion

1. **Actual correlation control:** prove a volume- and exterior-uniform
   influence estimate in a regime not already covered by the known
   strong-coupling theorem. No such new regime was obtained here.
2. **Exact coarse stability:** control the generated Schur forms and graph
   metrics. Their comparison losses multiply and their metric corrections
   accumulate; the current bound does not control arbitrarily many scales.
   Original one-step and unnormalized coordinate domains are now justified;
   the remaining transported-domain details of repeated normalized steps
   are still conditional. Nonlinear coarse holonomies require their own
   geometric argument.
3. **Physical scale budget:** the inherited local certificate still has
   lambda_* proportional to exp(−C/x). Even granting a uniform r<1 and all
   exact-coarse hypotheses, the illustrative profile a_j=A L^(−j),
   1/x_j=sigma+qj gives a finite certified inverse-gap sum only when
   Cq<log L, as in the already published budget calculation. The new
   constant (1−r)² does not change this convergence condition. No actual
   running-coupling trajectory or favorable all-scale budget was proved.
4. **Physical and continuum closure:** specify a nontrivial terminal
   physical sector and gap, construct the required continuum theory, and
   transfer the spectral bound. Forest coordinate marginals are exactly
   Haar, but their invariant cylinder functions are only constants; they
   do not manufacture terminal physical excitations.

Failure of a sufficient estimate or divergence of its certified budget is
not proof that the actual physical gap vanishes.

## Evidence and record

The three route proofs and the two root extensions were independently
reconstructed by separate AI audit agents. The one reported defect was
resolved by excluding degenerate repeated-link plaquettes from the formal
cluster statement; the original finding and accepted revision hashes are
preserved. This is not human peer review or formal proof-assistant
verification. No novelty or priority check is claimed for these additions.

Exact rational checks cover the four-state Schur example, all ordered leaf
pairs at tree depths 0–5, and Gaussian sizes 1–20. The all-size statements
are analytic arguments; these finite computations do not certify them.

- [Coarse proof and domain audit](audits/COARSE_REVIEW.md)
- [Tensorization and actual SU(2) audit](audits/TENSORIZATION_REVIEW.md)
- [Counterexample audit](audits/OBSTRUCTIONS_REVIEW.md)
- [Gauge-star audit](audits/GAUGE_STAR_REVIEW.md)
- [Current claim/dependency register](CLAIMS.json)
- [Continuation record](HANDOFF.md)

`CLAIMS.json` pins current proof and review hashes. Route-local metadata
describes its named version; the revision history preserves superseded
claims rather than silently treating older self-review as current evidence.
