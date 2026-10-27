# Independent review of the reference-density moment conditions

2026-10-19. Reviewer: `occupied_spectrum`; author of the reviewed note:
parent/coordinator. The author requested this review after the occupied
source-spectrum derivation. The algebra below was rederived from the
operators; agreement is not a physical certificate for a dipole medium.

**Primary verdict for the final reviewed revision: proved as written**
within its explicit retained-NR, continuum/operator-domain and source
hypotheses. The earlier revision needed the regulator restriction below;
the follow-up addendum verifies that it has been incorporated. Equations
(1)-(8) have the stated algebraic factors and the joint dipole-gap moments
are correct. Equation (1) is the continuum **quadratic-dispersion** identity
when the displayed local operators and double commutators are defined on
the state. An arbitrary finite UV or momentum regulator does not preserve
that identity unchanged. The lattice control correctly uses its own
dispersion/hopping identity; it does not certify `k^2 rho_I` at a finite
lattice spacing. The note already distinguishes lattice and continuum
kinematics, but should make this operator/regulator restriction explicit
where (1) is called exact for a regulated Hamiltonian.

The discussion of the initially missing restriction below is retained as
historical review evidence, rather than a claim that the final revision
still lacks it.

Reviewed bytes:

- `sum_rules/SUM_RULES.md`: SHA-256
  `9b5bbcd142bbc90fb7a697c7ee48c098e103e0a8f08897f47dc18cf968c023e1`.
- `sum_rules/check_sum_rules.py`: SHA-256
  `830963e09c46650e4f1c1dd4014835afa4a3b79407150b84a85e0af689f09089`.
- `sum_rules/contract.json`: SHA-256
  `81592f46b4a968f7fb628a558286c3315006d707e031cdb5a07f0715bb10d622`.
- `sum_rules/run_001/manifest.json`: SHA-256
  `be88e763c0565fe79ccded71e1de0d8d0821c9ed69ee44ee938766f469cacc12`.

## Independent reconstruction and obligation matrix

1. **Reference-density source, passed in the stated conservative NR
   truncation.** For `rho_k=sum_j w_j exp(-ik x_j)`, the first-quantized
   kinetic commutator is
   `[rho_-k,[T,rho_k]]=sum_j w_j^2 k^2/m_j` for quadratic kinetic energy.
   Taking `w_psi=m`, `w_b=2m` gives `m N_psi+4m^2 N_b/M`. Local conversion
   has zero reference weight because `2m-2m=0`, and local density
   interactions commute. The signed relativistic charge and the positive
   retained inventory are correctly distinguished; hard reactions outside
   that truncation cannot be included without rederiving its conservation.

2. **Spectral first moment, passed with the domain restriction above.** In
   the stationary ground state,
   `sum_n omega_n (|rho_k,n0|^2+|rho_-k,n0|^2)` is the expectation of the
   double commutator. The factor `1/(2V)` in the symmetrized measure thus
   gives exactly `k^2 rho_I/2`, rather than twice or half that result.
   Ground-state passivity and a well-defined first moment are hypotheses.
   On a lattice the corresponding commutator contains hopping expectations
   and `2(1-cos k)`; it cannot be replaced by a particle-density constant
   away from a controlled continuum limit.

3. **Bare-rest reactive correction, passed.** With `A=b^dagger psi^2`,
   `[rho_R,k,A(x)]=delta exp(-ikx) A(x)`. Hence
   `[rho_R,-k,[H_c,rho_R,k]]=-delta^2 H_c`, including at zero momentum.
   This operator can have reactive spectral strength because total bare
   rest mass is not conserved. Total energy is `H`, which has no such
   zero-momentum off-diagonal matrix elements. The note correctly declines
   to identify this NR rest-density sum rule with the full stress-energy
   source.

4. **Inverse moment and normalization condition, passed under the declared
   source convention.** For the real longitudinal force channel with the
   note's symmetrized Fourier normalization, the positive static ground
   susceptibility is `2 M_-1`. Dividing the density moment by `k^2` gives
   `M1=rho_I/2`, and `chi=1/K` therefore gives
   `M1/M_-1=K rho_I`. This is a condition on the actual strengths and
   frequencies. It is not a consequence of merely having a gravitational
   frequency in the spectrum. The all-mode exhaustion qualification and
   possible divergent zero-mode inverse moment are essential and present.
   The Fourier-derived longitudinal coordinate is nonlocal, as stated.

5. **Joint dipole-gap measure, passed.** For one ground-state site the
   off-diagonal source matrix element is `d` and its gap is `Omega=2dDelta`.
   Number density `n=w/d` therefore gives
   `S=int w d delta(omega-2dDelta) dDelta`. Direct integration yields
   `chi=int w/Delta` and `M1=2 int w d^2 Delta`. These remain valid if
   `Omega(Delta)` is not one-to-one; a Jacobian is needed only if the
   push-forward is explicitly solved as a density in `omega`. The moment
   matching coefficient in (6) is consequently 4. For a positive subset
   the left side is at most `rho_I`, and every omitted inverse moment must
   also be accounted for before claiming the full static response.

6. **Constant-dipole obstruction and variable-dipole loophole, passed in
   their stated scope.** The antiderivative in (7) differentiates to
   `Delta w/(p_sat a)` and diverges logarithmically. For
   `d=d0(Delta/a)^(-alpha)`, the four endpoint tests are independently
   reproduced: the first moment requires `alpha>0` in the UV and
   `alpha<3/2` in the IR; finite number requires `alpha<1` in the UV and
   `alpha>-2` in the IR. Thus `0<alpha<1` passes both. At `alpha=1/3`,
   `2 Omega d^2=4d0^3 a=m` is a compatible **ground-state** coordinate
   oscillator-strength budget. It is not an operator sum rule for an exact
   finite two-level representation of a canonical coordinate: higher
   levels and their field-dependent strength remain a physical obligation.
   Also, this particular `d` diverges in the soft limit, so physical
   localization cannot be inferred from the finite integrated moments.
   The note's locality/source caveats prevent either inference.

7. **Actually excited emitted-energy interpretation, passed.** If each
   occupied site's excitation energy is paid as `Omega`, then
   `int n Omega=2 int Delta w`, independently of how `d` varies. The target
   logarithm diverges. This is a finite *production-energy* obstruction
   only when those gaps really are occupied excitation costs. It does not
   apply to sites prepared in ground states with unoccupied high gaps.
   This distinction is correctly and explicitly retained in (8).

8. **Finite-temperature/nonstationary use, passed as a restriction.** The
   response weights are population differences, not emitted particle
   counts. Ground-state positive-frequency measures cannot be carried
   unchanged into a nonstationary produced state. This prevents a false
   identification between this lane's `rho_s` occupations and the parent's
   sum-rule spectral density.

## Computation and source checks

I read the complete fixed-charge basis enumerator, operator construction,
lattice identity and spectral-moment controls. The basis covers all
compositions at `Q=2,4` on four sites (dimensions 14 and 85), and the tested
matrix/parameter iterator covers 24 identities. The independent eigenbasis
moments use the same constructed Hamiltonian but a distinct calculation of
the spectral first moment. The claimed 24 spectral checks, eight zero-mode
controls and seven integral controls agree with the code. The mass/source
correction and zero-mode restrictions are actually exercised.

The existing manifest was validated read-only with the installed
computation-audit validator and `--root`; it reports valid evidence with run
status `completed`. I did not rerun the numerical experiment. The primary
external reference is used only for conventions; the inspected arguments
for (1)-(8) are internal calculations and do not depend on its theorem.

The source/exhaustion qualifications are sufficient for a necessary-condition
result after the continuum/regulator restriction above. They do not supply
the still-missing local scalar dipole, its actual occupied state, or gravity
normalization. The smallest requested edit is an explicit sentence beside
(1) that generic finite UV regulators change the kinetic sum rule and that
the continuum formula requires its own canonical operator/domain hypotheses.

## Follow-up after the author applied the restrictions

I reread the amended paragraphs beside (1) and the variable-d family. The
final reviewed `SUM_RULES.md` SHA-256 is
`ef6c75ddba6bbbb122115fd34812aa5aad58ff54d6e29f6c760674a879d0b421`.
It now explicitly requires continuum quadratic dispersion, canonical local
commutators, a well-defined domain and a finite ground-state first moment;
it disclaims arbitrary finite-regulator preservation and separates the
actual lattice sum rule. It also explicitly retains the divergent soft
size and the lack of an exact finite two-level canonical coordinate.
These edits address the requested mathematical restrictions. The original
numerical code and its finite evidence were not changed or rerun by this
reviewer. No physical scalar dipole or source exhaustion is inferred.
