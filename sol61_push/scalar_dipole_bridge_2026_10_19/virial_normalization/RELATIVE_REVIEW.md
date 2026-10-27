# Independent review of the live relative-mode construction

Claim normalized: in the threshold-matched one-component Newtonian GP model,
a prescribed harmonic baryonic potential has an exact uniformly driven COM
mode. For two live spherical rigid profile coordinates, gravitational recoil
cancels the common affine drive, but unequal form factors can support an
intermediate-wavelength relative-source response. These statements do not
construct the rigid-profile manifold as a stable microscopic material state.

**Primary verdict: proved as written**, for those explicitly stated conditional
identities and finite-profile examples. The passage to a stable live scalar plus
baryon phase remains conditional on the named background/eigenmode input; it
is not passed as an unconditional physical realization. No algebraic correction
is required in the reviewed formulas.

Reviewed raw note:
`../relative_modes/RELATIVE_MODES.md`, SHA-256
`9a726b50fb9b2d6b077cf4ad06613ebf3e4fe25385846c587980f7015976eb2f`.
Reviewed script SHA-256
`51532fc32b9c11f61108d5ae9c83c239fd2f4c1a166b542fa63e669426e0bb10`.
Review checkpoint: CE087. This review was independently reconstructed by the
virial-normalization subagent in the same parent session/model family; it is
not independent external review. Only this review file was written for the
review, and no relative_modes input was changed.

## Dependency and obligation checks

| Required arrow | Evidence type | Result |
|---|---|---|
| translation-invariant GP self terms plus prescribed harmonic field -> COM oscillator | direct substitution | passed |
| prescribed-core response -> 1/G factor times density ratio | algebra | passed |
| live mass coordinates -> relative inertia and cancellation of common g | exact coordinate calculation | passed |
| spherical mutual potential -> overlap curvature | angular isotropy plus Poisson equation | passed |
| complete linear source -> form-factor difference and infrared k^3 | source expansion | passed |
| Gaussian size separation -> constant finite-band form-factor window | elementary exponentials, finite checks | passed |
| quantized oscillator -> one gap and oscillator strength | canonical oscillator matrix element | passed |
| gravitational profile potential -> rational saturating material law | explicit mismatch; no implication claimed | passed as obstruction for these profiles |
| rigid live profile coordinate -> stable GP-baryon normal-mode pole | missing state/eigenmode construction | conditional |
| selected host distribution -> requested occupied rational spectrum and unit multiplier | not derived; explicitly left open | not addressed |

## Fresh reconstruction of the critical steps

For the GP ansatz in (8), the gradient terms cancel, and the coefficient of x
is `-qddot=omega_b^2 q-g_e`. The constant coefficient is
`-betadot=(m/2)(qdot^2-omega_b^2 q^2)`. Thus both the acceleration equation and
the phase in (8) have the stated signs. Carrier contact and self-gravity depend
on relative positions and translate with the profile. This exact statement
requires the trap to be harmonic over the whole occupied state. The finite
core/tail qualification in the raw note is necessary and correctly stated.

For live coordinates, substituting
`q_d=C+(M_b/M_T)s`, `q_b=C-(M_d/M_T)s` gives kinetic energy
`M_T Cdot^2/2+mu sdot^2/2` and mass-weighted relative force
`mu (gbar_d-gbar_b)`. Hence sending `M_b/M_d` large leaves a common g in each
acceleration and does not create an anchor. The field drives the total COM;
it does not drive the relative coordinate in an affine field.

The rigid-profile mutual-energy curvature is
`kappa_ij=int rho_d partial_i partial_j U_b`. Its trace is
`4pi G int rho_d rho_b` and isotropy divides by three. Division by
`mu=M_d M_b/M_T` yields exactly
`omega_rel^2=(4pi G/3)M_T I_db`. This is a positive Hessian of the declared
translation manifold, not a proof of its invariance under full live dynamics.

The Fourier expansion of each displaced component is
`M_a F_a exp(-ik.q_a)`. Its linear relative part is therefore
`-i mu (k.s)(F_d-F_b)`, with the sign in (18). For isotropic centered profiles,
`F_d-F_b=-k^2(<r^2>_d-<r^2>_b)/6+o(k^2)`, reproducing (20).
Equal normalized profiles cancel pointwise at this linear order. They need
not have zero quadratic energy: their total second-order source is
`(mu/2)s_i s_j partial_i partial_j f`, whose contraction with the background
potential gives `kappa s^2/2`. This correctly retains the gravitational spring
without falsely assigning an uncompensated first-order dipole.

The probe force projected onto s is
`mu (F_d-F_b)g_e`, while the source projected back out has the same factor.
The response therefore contains its **square**:
`chi_rhorho=mu k^2 |F_d-F_b|^2/(omega_rel^2-(omega+i0)^2)`.
At small k this is O(k^6), and its longitudinal polarization coefficient is
O(k^4). A COM pole at zero frequency is a distinct contribution. This resolves
the possible false inference that any gravitational spring automatically has
a nonzero uniform gravity source.

For Gaussian width ratio q, write `u=(k sigma_d)^2/2`. Then
`DeltaF=exp(-u)-exp(-q^2 u)`, maximized at
`u=log(q^2)/(q^2-1)`. This independently yields maxima 0.45617799047 for q=3
and 0.89303061727 for q=10 after squaring. For q=30 and q=100 the stated band
endpoints give squared differences 0.9 within double rounding. They provide
a real finite band for the projected response, while respecting the k->0
cancellation. The plateau normalization follows directly:
`4pi G alpha=3 nu_h mu/(M_T I_db)`. The remaining inventory, overlap and
packing factors are not canceled by the gravitational spring.

The Gaussian mutual energy expansion is
`E(s)=E(0)+A s^2/(6S^3)-A s^4/(40S^5)+...`, with
`A=G M_d M_b sqrt(2/pi)`. Thus `kappa=A/(3S^3)` and the fractional quartic
coefficient is `-3/(20S^2)`, as in (27). The top-hat polynomial gives the
likewise softening leading correction `-9s/(16R)` to force divided by
`kappa s`. The target derivative expands as
`K_G Pi+K_G^2 Pi^2/a+...` and diverges at finite Pi; these profile springs
do not produce it. Their bounded binding energy also permits escape under a
constant differential tilt. This mismatch concerns the declared examples;
it is not a classification of all scalar/baryon nonlinear states.

## Source and computation checks

The recorded v2 manifest in `../relative_modes/run/manifest.json` was validated
against current inputs with the installed computation-audit validator; it
reported `valid evidence record (run status: completed)`. The implementation
was read. Its exact-rational polynomial and reduced-inertia checks match their
stated finite population; the Gaussian code uses stable expm1 in the infrared
and the correct analytic peak. I did not rerun its writer or overwrite its run.
An independent read-only Python calculation of the analytic Gaussian peak and
each recorded band endpoint reproduced the quoted values. This is a narrow
cross-check, not a certified interval computation or a live-mode simulation.

Wu and Zaremba, arXiv:1310.7934v2, header 31 October 2013, title/author page and
Sec. 2 Eqs. (1)-(8), were read in the exact primary PDF. Their harmonic
Hamiltonian with relative-coordinate pair interactions separates into COM and
internal terms, supporting the narrowly used Kohn comparison. The GP phase
and live-source calculations above were rederived, so no unverified extension
of that theorem to a deformable baryon background carries the result.
[Exact primary source](https://arxiv.org/pdf/1310.7934v2).
No PDF was retained; no retained-content hash is claimed.

## Remaining gap and cheapest discriminator

The first missing implication is existence of a stable self-consistent
scalar/baryon equilibrium whose actual l=1 eigenfunction has the proposed
compact/diffuse separation and retains the finite-band oscillator residue.
The cheapest meaningful next check is its coupled linearized
Bogoliubov/Euler-Poisson l=1 operator, including baryon shape response and the
complete mass source. The raw note already names this continuation. A fitted
profile overlap or host count is not a substitute for that input.

The strongest safe result is a conditional finite-wavelength response bridge
with a natural inverse-G scale, an exact uniform-force cancellation, and an
explicit residual state-normalization factor. It supplies neither a stable
occupied host continuum nor the full rational constitutive law.
