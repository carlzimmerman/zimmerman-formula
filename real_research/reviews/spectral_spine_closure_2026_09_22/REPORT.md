# Spectral spine closure: results and limits

The original physical program is **not fully closed**. The work does close
an actual SU(N) strong-coupling lattice-gap theorem, the complete I14
constant-confinement discrete spectrum, and the missing type of radial
variational comparison in I13. The proposed stellar mass cutoff and the
selection of the physical acceleration coupling kappa=1/2 remain open.

Base checkpoint: `e3af62a453ca6625db8428f6d32957b27a7f1331`.
See `CONTRACT.md` for original targets and parallel ownership. Concurrent
HEAD changes did not change the relevant tracked inputs from that base.
No commit was made by this work.

## Results

| Target | Strongest supported result | Remaining implication |
|---|---|---|
| I13 actual radial eigenproblem | Exact Newtonian work identity; exact GR self-adjoint form; upper Rayleigh and lower positive-function comparisons; leading PN structural coefficient | Actual equilibrium sequence, EOS and BH-envelope boundary conditions; exact-GR evaluation or bounded PN remainder for a mass cutoff |
| I14 sharp discrete wall | Full finite spectrum for constant q; sharp uniform confinement-dependent floor; explicit negative modes; Lean-certified sharpness | Identify this particular form and norm with the framework's physical second variation; independently justify marginality |
| I15 single plaquette | Full untruncated SU(N) Hamiltonian gap at least gapN(N,x)>=1 for N>=2,x>=2 under the stated magnetic normalization | No missing spectral implication for this scope |
| I15 many plaquettes | For fixed d, all N>=2, and x>=X_d, finite open lattice and canonical infinite-volume physical GNS gap at least 3x/16 | X_d is finite but not numerically evaluated; x>=2 for arbitrary volume, continuum scaling, and scalar-framework identification are not proved |

## I13: the physical operator now has a comparison, not an assumed equality

The homologous Newtonian trial gives `3 Wbeta/J`, with
`J=integral rho r^4 dr`. I13's inertia is therefore `J/3` in that convention.
The trial quotient bounds the lowest eigenvalue from above. The exact GR
operator is derived from a pinned primary equation, and a ground-state
transform supplies a lower comparison when its endpoint assumptions hold.
Thus negative trial work proves instability; positive trial work alone
does not prove stability.

The leading PN correction is the positive structure integral

    H = integral [8G P m r + 8pi G P rho r^4 + G^2 rho m^2] dr,
    Cgr = H R/(6GM Wgr).

For n=3 it numerically gives `Cgr=3.373422935937`, or
`1.124474311979` in the conventional `Gamma1-4/3` coefficient. This
independently reproduces the published 1.1245 benchmark and corrects the
previous coefficient band. A nonuniform-density constant-Gamma polytrope
also gives an exact obstruction to identifying homology with the actual
eigenmode. Numerical examples exhibit a positive homologous trial and a
negative admissible Ritz trial on the same TOV background.

[Derivation, solver, source and benchmarks](i13/REPORT.md).
The calculations use generated polytropes, not MESA/GENEC data or an
observed black-hole-star mass sequence. Finite binary64 Ritz values are
not interval-certified eigenvalue bounds. The mass cutoff remains open.

## I14: the complete model spectrum, and the source obstruction

For N>=2 and q=q0 constant, with u0=uN=0 and norm sum u_n^2,

    lambda_j = 6 sin^2(j pi/(2N)) + 1/4-kappa^2+mu^2 q0,
    1<=j<N.

The sharp lower bound uniform in box size is
`b=1/4-kappa^2+mu^2 q0`. At b=0 every nonzero finite-box mode still has
positive energy, but no positive lower bound is uniform in N. At b<0
large boxes have negative modes. The stability wall is shifted by
confinement; it is not universally kappa=1/2. Seventeen new Lean theorems
include sharpness, confinement, sine eigenmode identities and nonzero norms.
The completeness argument and exact finite minimum are proved in prose.

[Full spectrum proof](i14/DERIVATION.md).

The source bridge does not survive as stated. Directly varying G155's
kinetic action yields a different radial weight; its deep log-coordinate
weight is constant, not the weight underlying I14's sqrt(r) dressing. The
cited action supplies no independently derived negative kappa-squared
potential. Its full interpolant also does not admit the quoted logarithmic
background exactly. These are explicit algebraic obstructions, not failed
searches. [Action and Hessian calculation](i14/SOURCE_BRIDGE.md).

## I15: the spectral comparison is supplied

For `H=(x/2)sum C_l+(b_N/x)sum(1-ReTr U_p/N)`, `0<=b_N<=2N`, the open
single square has physical character Hilbert space. Positivity of the
magnetic operator and the Haar vacuum trial give

    E1>=2x C_F, E0<=b_N/x,
    gap>=2x C_F-b_N/x>=gapN(N,x)>=1  (N>=2,x>=2).

This is a full-space min-max proof, not a truncation or an assumption that
the electric vacuum remains an eigenstate.

For arbitrary open cubic-lattice volume, group outgoing links into sites,
normalize the on-site gap to one, and use `C_F>=3/4`. The bounded local
magnetic perturbation then satisfies

    eta <= A_d/x^2, A_d=(32/3) binomial(d,2),

uniformly in N. Yarotsky's established theorem applies to these possibly
infinite-dimensional on-site spaces with constants depending only on the
fixed interaction range. This gives a common sufficiently strong-coupling
window and, after rescaling, `gap>=3x/16`. The actual ground state is
subtracted. Finite Gauss-law restriction and the physical cyclic subspace
of the canonical infinite-volume GNS representation inherit the bound.

[Complete operator proof and exact theorem dictionary](i15/PROOF.md).
[Pinned source and separate review record](i15/source_record.json).

This result is an application of existing mathematics, not a newly solved
Yang–Mills problem. The published constants were not evaluated numerically.
The original x>=2 window is certified for one plaquette only. Periodic
tori, uniqueness among all infinite ground-state representations, and the
continuum limit are not asserted. The operator theorem is not Lean-
formalized; six new Lean theorems certify its scalar bounds/interfaces.

## Verification and review

- All three final Lean files compile; their printed dependencies contain
  only `propext`, `Classical.choice`, and `Quot.sound`. No proof placeholders
  or custom axioms were introduced. I13 theorem/proof bodies are unchanged;
  its descriptions were corrected.
- I13: 17 numerical assertions and four exact symbolic identities, with
  validated v2 manifests, pinned code and declared numerical limits.
- I14: 30 directly constructed matrices agree with the analytic spectrum
  to at most 6.22e-15; exact symbolic Hessian/flux checks also pass.
- I15: 159 bounded assertions, including exact rational Casimir enumeration
  and SU(2)/SU(3) character-matrix checks. These experiments check indexing
  and constants; the analytic/operator proofs establish the universal claims.
- A separate source audit reconstructed I15's Casimir, normalization,
  boundary and gauge arguments. It required restricting infinite uniqueness
  to the canonical GNS vacuum, which the final statement does.
- Final self-review checked signs, factors, norm conventions, quantifiers,
  endpoint conditions, source versions and finite-versus-uniform scope.
  Compiler and manifest logs are in `verification/`. They certify execution
  and provenance, not every analytic step of the prose proofs.

## Remaining handoff

I13 now needs actual stellar profiles and boundary data. I14 needs a single
specified physical action, a valid background and its full constrained
quadratic action; changing an algebraic coefficient cannot close that gap.
I15 needs a quantitative weak-interaction constant or a different argument
to reach x=2 uniformly in volume. No additional scalar positivity lemma
removes any of these three distinct requirements.
