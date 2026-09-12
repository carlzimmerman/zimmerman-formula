# Independent unitary-chi ADM check at finite wavelength

Base `196f84653fec06a359314ec705d69647c5bd05a4`. The calculation derives the
full quadratic scalar action directly from the same fixed covariant action in
a different gauge from `../../../cubic_finite_wavelength/`. It introduces no
coefficient functions, histories, source couplings, or fits. The result is an
independent gauge and normalization check, not a new sourced transfer or
nonlinear field solution.

## Exact ADM representative and conventions

Use signature `-+++`, proper background time, constant `M2` and gamma, and

    N=1+n, h_ij=a² exp(2zeta)delta_ij, N^x=partial_x B,
    chi=chibar(t), q=chibar_dot, tau=t+sigma.

The gauge needs `q!=0`. Let `beta=B_x`, `ell=B_xx`, and denote spatial x
derivatives by subscripts. For a plane scalar perturbation,

    d=H+zeta_dot-beta*zeta_x,
    K^x_x=(d-B_xx)/N, K^y_y=K^z_z=d/N,
    R3=a^(-2)exp(-2zeta)[-4zeta_xx-2zeta_x²].

The clock invariants are retained before expansion:

    T=1+sigma_dot-beta*sigma_x,
    s²=T²/N²-a^(-2)exp(-2zeta)sigma_x²,
    X=q²/N²,
    Y=(q²/N²) a^(-2)exp(-2zeta)sigma_x²/s².

In unitary chi gauge, `grad^mu chi=-(q/N)n^mu`. With `Q=q/N`,

    gamma X Box chi = -gamma Q² n(Q)-gamma Q³K
                    = -(2gamma/3)Q³K
                      -(gamma/3)div(Q³ n).

Thus the exact cubic ADM representative, including its density, is
`-(2gamma/3)N sqrt(h)(q/N)³K`. No qdot term is dropped: its effects enter
when time-dependent coefficients are integrated by parts. The Einstein
representative is `M2 N sqrt(h)(R3+Kij Kij-K²)/2`.

Write `F=P(q²,t)-V(t)-M2 Lambda` if the constant cosmological term is
present, and `F=P-V` otherwise. Clock partial derivatives are taken at fixed
X: `Ft=P_tau-V_tau`, `Ftt=P_tautau-V_tautau`. Lambda is constant and does
not affect these derivatives. Including the existing Lambda is necessary
when applying the canonical history's background Einstein equations.

## Full quadratic action and legitimate background cancellations

All following coefficients are evaluated at `X=q²,Y=0,tau=t`. Define

    c=gamma q³, Theta=M2 H+c,
    Sigma=q²PX+2q⁴PXX-3M2 H²-12Hc,
    C=Ft-2q²PXtau,
    D=Ftt-3H Wtau,
    Sclock=W-2q²WY.

After spatial and time integration by parts, the quadratic density is

    L2/a³ = -3M2 zeta_dot²+6Theta n zeta_dot+Sigma n²
      +2(M2 zeta_dot-Theta n)B_xx
      +(M2/a²)(zeta_x²+2n_x zeta_x)
      +C n sigma-3W sigma zeta_dot+W sigma B_xx
      +(D/2)sigma²-Sclock sigma_x²/(2a²)
      +3E0 n zeta+3Et zeta sigma+(9/2)Ea zeta²,

where the exact background residuals are

    E0=3M2 H²+6Hc+F-2q²PX,
    Et=Ft-3H W,
    Ea=M2(2Hdot+3H²)+F+W+2gamma q²qdot.

These last three terms disappear only on a background satisfying the
corresponding lapse, clock and spatial Einstein equations. Their cancellation
is an explicit symbolic assertion; they are not silently discarded. Extra
homogeneous matter requires its action and perturbations to be included when
applying those equations. This package includes no ordinary-matter source.

The clock has no quadratic time kinetic term. Its apparent `Wtau sigma
sigma_dot` and `3W zeta sigma_dot` terms are integrated with the full `a³`
measure and time derivatives of W. In particular, they generate the
`-3H Wtau` term in D and the `-3W sigma zeta_dot` term. Freezing those
coefficients during this step would change the finite-wavelength action.

## Compact independent gauge checks

For a real cosine mode, the quadratic period average is one half of each
displayed product. Treat `ell=B_xx` as the scalar shift amplitude. For
nonzero spatial k, the shift equation gives

    n=(M2 zeta_dot+W sigma/2)/Theta.

The averaged lapse/ell Hessian determinant is `-a^6 Theta²`. In the earlier
contravariant sine-shift amplitude `b`, where `ell=k b`, it is
`-a^6 k² Theta²`, exactly the archived convention. Elimination requires
`Theta!=0`; the homogeneous `k=0` mode has no independent shift row.

Define

    Bhat=2PX+4q²PXX-12gamma Hq+6gamma²q⁴/M2.

After lapse/shift elimination, the averaged zeta velocity Hessian is

    Kchi=a³ M2²q² Bhat/(2Theta²).

The remaining clock constraint Hessian and its mixing with `zeta_dot` are

    Dchi=a³[Sigma W²/(4Theta²)+C W/(2Theta)+D/2]
           -a k² Sclock/2,
    Jchi=(a³ M2/2)[Sigma W/Theta²+C/Theta].

To compare with the prior unitary-tau variables, use the linear gauge map

    zeta_tau=zeta_chi-H sigma_chi,
    delta_chi_tau=-q sigma_chi,
    u=delta_chi_tau-(q/H)zeta_tau=-(q/H)zeta_chi.

Consequently the old remaining nondynamical coefficient must be
`Dold=Dchi/H²`, and the old `zeta_tau*u_dot` coefficient must be
`Jold=Jchi/q`. Both identities, including all finite-k and zero-derivative
terms in D, are checked exactly against the saved action-derived expressions
in `../../../cubic_finite_wavelength/run_001/derivation.json`. This additional
comparison assumes `H!=0`. The kinetic coefficient also matches the old
reduced matrix entry exactly, including the real-mode averaging factor.

The canonical substitution uses the existing branch, with its current
amplitude denoted A:

    PX=A/(2q)+3gamma qH, PXX=(B0-A/q)/(4q²),
    W=U-2gamma q²qdot, WY=AU/[2q(Aq+U)],
    Hdot=-(Aq+U)/(2M2), A_dot=-3HA,
    PXtau=-3HA/(2q)+3gamma(qdot H+q Hdot)-B0 qdot/(2q).

The last expression follows by differentiating the displayed PX along the
background and subtracting `2q qdot PXX`; it is not a new coefficient choice.
The on-shell clock equation and its derivative give
`Ft=3HW` and `Ftt=3Hdot W+3H Wtau-2q qdot PXtau` for the same comparison.

## Computation contract and reproduction

`derive_chi_adm.py` differentiates the exact invariant ADM action to amplitude
degree two using rational symbolic arithmetic, then checks the off-shell
residual decomposition, integrations by parts, auxiliary Hessians and gauge
identities. Two small exact controls check canonical scalar normalization and
clock spatial sign. Archived expressions are read as mathematical data; the
old script and its entire scan are not rerun. No numerical fit or sampling
decides an identity. The existing finite-k Lean certificates are not
duplicated by this package.

From repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/adm/derive_chi_adm.py
```

The computation-audit skill determines the exact computation contract and
manifest; mathematical proofreading is limited to the new report and script
notation. No physical source response, finite-wavelength stability extension,
or nonlinear constraint completion is claimed.

Final evidence is `run_001/manifest.json` and `run_001/stdout.txt`: all 22
exact checks pass, exit zero, 3.280 seconds, Python 3.9.6 / SymPy 1.14.0.
The version 2 manifest passed validation with current input/output hashes;
stderr is empty. Mathematical self-review found no unresolved notation issue
and made no mathematical-token change.
