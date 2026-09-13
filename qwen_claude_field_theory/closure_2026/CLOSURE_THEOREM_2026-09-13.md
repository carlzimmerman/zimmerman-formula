# Conditional closure theorem for the explored MOND architectures

## Theorem (local first-gradient York/QUMOND class)

Assume one physical metric, two static scalar potentials, locality, isotropic
dependence on the spatial invariant `u=h^{ij} Psi_i Psi_j/a0^2`, and the
first-gradient action

```text
L = -2 A(u) h^{ij} Phi_i Psi_j + a0^2 F(u).
```

Exact measured-normalisation Poisson response requires

```text
dL/d(Phi_i) = -2 Psi_i  =>  A(u)=1.
```

The independently varied Hilbert trace-free metric source on `Phi=Psi` is

```text
C_TF(u) = F'(u) - 2(A(u)+u A'(u)).
```

After `A=1`, exact no-slip for arbitrary anisotropic gradients requires
`F'(u)=2` identically.  The required exponential QUMOND flux requires instead

```text
F'(u) = nu_exp(sqrt(u)) = 1/(1-exp(-sqrt(u))),
```

which is nonconstant and equals two only at `sqrt(u)=log(2)`.  Therefore the
three requirements (exact Poisson, exact exponential MOND, and no slip) are
mutually inconsistent in this entire class.

The factorization, the nonconstant exponential witness, and the required
normalization are reproduced by
`general_york_no_slip_no_go_2026.py` and its Lean certificate
`GeneralYorkNoSlipNoGoFormal.lean`; all checks exit `0`.

## Independent action-level closures

This theorem is not the only obstruction.  The explicit matter-sourced
elliptic phantom action was varied and its actual finite-`k` Dirac block has
computed rank `8`, leaving three auxiliary/scalar configuration DOF after the
stated diffeomorphism subtraction.  Its homogeneous source equation rejects
positive `rho_0`, its Hilbert stress produces slip unless the MOND multiplier
is switched off, and its `S_m` Ward divergence is nonzero.  The standalone
gate and its two tests exit `0` while reporting those failures.

The source-matched AeST host independently leaves one finite-`k` scalar mode:
`p_Phi=0`, `C1=Q0 p_chi-p_v`, a zero Poisson-bracket matrix, and a reduced
positive-kinetic scalar with

```text
omega^2=(2-K_B)(K_2 Q_0^2+k^2)/(K_2 K_B).
```

Thus strict `N_grav=2` is false for that action; the `k=0` degeneracy does not
remove the finite-`k` mode.

## Empirical branch versus theory closure

The parameter-free family
`mu_n(Y)=1-(1+Y)^(-n)` has `n=2` as the preferred member on 155 SPARC curves
under both density conventions, including equal-galaxy weighting and a
1000-draw galaxy bootstrap.  This is a reproducible curve-level clue for
`kappa=1/2`, not an action derivation, and it is not the exact exponential law.
The published PAPER27 source also contains a notation overload in its scale
display; the corrected relation is `a0=s/n`, `kappa=1/n` (see
`PAPER27_SCALE_ERRATUM.md`).

## Phantom-source trilemma (new executable gate)

The direct elliptic-phantom route has an additional obstruction independent of
the candidate's detailed multiplier Hessian. If its effective source is an
isotropic, separately conserved stress on a static no-slip branch, the
linearized spatial trace gives `p_aux=0`, and the static Ward identity gives
`rho_aux=0` wherever `grad Phi != 0`. Exact exponential MOND requires instead
`rho_aux=(4 pi G)^(-1) div[(1-mu) grad Phi]`, generically nonzero; the gate's
explicit witness is `Phi'=x`, `a0=1`, `x=2`. The Python gate, regression test,
and `PhantomNoSlipWardFormal.lean` all exit `0`. This result is conditional on
the isotropic/local source class, not a universal claim against every
nonlocal or multimetric action.

The same gate checks the spherical vacuum strengthening: conservation integrates
the phantom flux to `r^2(1-mu)g=C`, while the baryonic MOND flux is
`r^2 mu g=GM`; their sum gives `g=(GM+C)/r^2` but would require `mu=GM/(GM+C)`
constant, contradicting the strictly varying exponential `mu(g/a0)` on every
positive-flux branch. This rules out a non-Newtonian spherical solution in the
stated class, not merely one local field profile.

The latest L236 architecture audit independently sharpens the remaining open
door: a relativistic merge cannot use a separate cuscuton potential to drive
the background while also deriving the normalization from the gradient
function. Any surviving construction must make the same function control the
homogeneous expansion and the MOND gradient sector, with no independent
zero-mode potential. That is a design constraint, not yet an action-level
solution.

## Final status

The original ten-gate objective is **OPEN**: no single explicit action in the
repository is certified to satisfy all ten gates.  The local single-metric
first-gradient York/QUMOND class, the displayed elliptic phantom action, and
the direct AeST host are **DEAD** under their computed necessary gates.  No
universal no-go for arbitrary nonlocal, multimetric, or explicitly anisotropic
actions is claimed.

The unavoidable next calculation is therefore not another coefficient fit: it
is a complete nonlinear covariant action outside this theorem's hypotheses,
with its lapse/shift-retained Dirac chain, matter Ward identity, both metric
potentials, PPN parameters, tensor cone, FLRW perturbations, and nonlinear MOND
branch derived from that same action.
