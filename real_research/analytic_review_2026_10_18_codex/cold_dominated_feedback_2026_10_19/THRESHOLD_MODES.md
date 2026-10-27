# Energy-mode bootstrap and the circular force trace

19 October 2026. Owner `/root/threshold_bootstrap`. Assigned base revision
`915b108f82629d3e794a6a3a3b6ad5e793355172`. Analytic only. This is the only
write by this worker. No scientific scripts, numerical calculations, arrays,
process operations, repository edits, or external mathematical sources were
used.

## Exact result and its limitation

There is a useful regularity improvement which does **not** require small cold
mass or small susceptibility. Under the finite nondegenerate resonant geometry
specified below, every actual energy eigenmode has radial field in `C^(1,1)`.
The proof uses the kinetic eigen-equation and the actual shell field equation,
and bounds the radial density directly. It does not assume an inverse of a
boundary feedback operator. Consequently the previously unresolved quadratic
receiving quotient at an eccentric interior Morse extremum is bounded for such
an energy mode.

At a simple circular epicyclic extremum this bootstrap leaves a different exact
condition. For a mode with frequency `nu=k*kappa(s_c)`, the resonant quotient is
automatically bounded for `|k|>=2`. For the fundamental positive harmonic
`k=1`, it is bounded near `(J,s)=(0,s_c)` **if and only if**

    phi_j'(s_c)=0.                                           (CF)

Here `j` is the receiving/source species and `phi_j` is that mode's own radial
potential. An energy mode can satisfy the local energy condition with a nonzero
value of this force trace. The new bootstrap supplies no cancellation of this
trace. No actual self-consistent mode with nonzero trace is constructed, and no
absence theorem is asserted. The global homogeneous field equation implying
(CF), or an actual mode violating (CF), remains the first missing implication.

## 1. Definitions and explicit geometric scope

Use exactly the actual two-species model in the input `full_feedback/RESULT.md`:

    dGamma=C_Gamma dr dv dL,
    dm=2*pi*C_Gamma dJ dL,
    w_j=-F_(j,E)>0 in the open occupied set,
    omega_(j,k)=k*Omega_j,
    h_(j,k)=-w_j*omega_(j,k)*phi_(j,k)/(omega_(j,k)-nu).

The field kernels are

    P_ff=P_ft=P_tf=-G/max(r,r'),
    P_tt=2*c*integral_(max(r,r'))^infinity M_t(s)*s^-4 ds,
    c=G^2/a_0.

The species order remains `(t,f)`. An actual energy mode means a nonzero
`h in H` with `Lh=-i*nu*h`, `nu !=0`, `phi=P h`, and finite coercive energy
`Q[h]`, equivalently `sum integral |h|^2/w dGamma<infinity`. Its initial field
regularity is the already proved

    ||phi||C^(1,1/2) <= C ||h||Q.

There are only finitely many potentially resonant `k`, because the actual
occupied frequencies have a positive lower bound. The regularity theorem below
assumes those finite resonant sets have a finite cover by these charts:

1. **Regular trace-division chart.** The actual mode coefficient is uniformly
   `C^1` in a transverse coordinate, the detuning is a submersion, and the
   resonant coefficient vanishes on the relevant resonant branch. Thus its
   quotient is bounded there. This includes ordinary compact eccentric
   interior resonances; it includes regular circular crossings when
   `partial_L Omega !=0`, using uniform `C^1` dependence on `L`.
2. **Eccentric interior definite Morse chart.** `J_c>0`, `w(q_c)>0`, and
   `|omega(q)-nu|` is comparable to `|q-q_c|^2`.
3. **Simple circular extremum chart.** In `x=s-s_c`, `L=L_c(s)`,

       |omega(J,s)-nu| is comparable to J+x^2,

   with smooth nondegenerate orbit geometry and `L_c'>0`.
4. **Other support chart.** The actual weighted kinetic source
   `w*omega*phi_k/(omega-nu)` is bounded in physical phase variables, uniformly
   up to this chart's boundary. This is a named boundary input, not a
   consequence of arbitrary flatness alone.

The assumption in item 4 can be verified in several concrete situations.
If a cap-only touching level has nonzero normal detuning and, in inward cap
coordinate `z>=0`,

    |omega-nu| >= c z,

then smooth flatness gives `w/|omega-nu| <= C w/z`, a bounded function. If the
cap level instead enters the positive-weight interior as the regular curve
`z=g(y)>=0`, and that whole curve is available for trace division, item 1
applies. At a cap saddle `omega-nu=a z+b y^2+...` with `ab<0` and `a!=0`, the
nearby regular root is inside the occupied set, so the latter mechanism
applies. The coordinator is deriving this actual cap geometry for a narrow
tube with finitely many simple extrema of `kappa`. This note does not replace
that separate geometric proof by an assumption of the desired inverse.

The theorem does not cover degenerate critical sets, eccentric Morse saddles,
infinitely many accumulating circular extrema, or an arbitrary degenerate
cap contact. It also does not prove that all unspecified source profiles meet
this finite geometric contract.

## 2. Two elementary density estimates

### 2.1 Eccentric action singularity

Consider an eccentric chart about `q_c`. Suppose one localized harmonic has

    |h_k(q)| <= C/|q-q_c|.                                (2.1)

Its radial density is bounded. Here is a proof accounting for the orbital
turning points, rather than treating the orbital measure as bounded.

Away from turning radii, the pushforward from angle to radius has a bounded
Jacobian and the action integral of `(2.1)` is finite. Near either turning
radius, the pushforward density has the form

    B(r,q) * 1_(allowed side) * |r-r_+(q)|^-1/2

or its pericenter counterpart, with `B` uniformly bounded. The other turning
point stays a positive distance away in this eccentric chart. The turning
radius is a submersion in actions: since

    U(r_+(q),L)=E(J,L),
    partial_J r_+ = Omega/U_r(r_+,L) !=0,

one may use coordinates `x=r_+(q)-r_+(q_c)` and a complementary coordinate
`y`. Their Jacobians are bounded, and `|q-q_c|` is comparable to
`sqrt(x^2+y^2)`. Integrating the absolute value first in `y` gives

    integral_(|y|<eta) (x^2+y^2)^-1/2 dy
       <= C*(1+|log |x||).

The remaining radial density is bounded uniformly in its radial parameter
`z=r-r_+(q_c)` by

    C*integral_(|x|<eta)
       (1+|log |x||)*1_(allowed side)*|z-x|^-1/2 dx.

This is uniformly finite: the logarithm is in `L^3` on the fixed interval,
and the translated fold kernel has uniformly bounded `L^(3/2)` norm on the
same bounded interval. Ordinary Holder's inequality proves the bound.
This also applies if the singularity is `O(|q-q_c|^(eta-1))` for `eta>0`.

### 2.2 Circular singularity

Near a nondegenerate circular well at `s=s_c`, put `x=s-s_c`, `z=r-s_c`.
The physical energy expansion and the smooth positive action-energy Jacobian
give, on a sufficiently small fixed phase neighborhood,

    J is comparable to v^2+(r-s)^2,
    J+x^2 is comparable to v^2+z^2+x^2.                   (2.2)

Suppose one localized harmonic obeys

    |h_k(J,s)| <= C*sqrt(J)/(J+x^2).

The absolute value of its physical phase representative obeys, by `(2.2)`,

    |h_k e^(ik theta)|
       <= C/sqrt(J+x^2)
       <= C/sqrt(v^2+z^2+x^2).                            (2.3)

At fixed radius, `dL=L_c'(s) dx` has a smooth bounded Jacobian. Therefore its
absolute radial density is at most

    C*integral_(v^2+x^2<eta^2)
          (v^2+x^2+z^2)^-1/2 dv dx <= C*eta,

uniformly in `z`. Restricting to the actual occupied cap only decreases this
absolute bound. No singular action-angle Jacobian at `J=0` is discarded.

## 3. The actual `C^(1,1)` bootstrap

**Theorem.** Under Section 1's finite geometric contract, an actual energy mode
satisfies

    mu_j(r):=C_Gamma*integral h_j(r,v,L) dv dL in L^infinity(I),
    phi in C^(1,1)(I)^2,
    ||mu||infinity + ||phi||C^(1,1) <= C_nu ||h||Q.          (3.1)

Constants depend on the fixed actual halo and the stated geometric bounds.
There is no assumption that cold mass, `w`, or feedback is small.

**Proof.** First consider a finite resonant harmonic on an eccentric Morse
chart. Energy and positive `w(q_c)` force `phi_k(q_c)=0`: otherwise
`|h_k|^2/w` is bounded below by a positive constant times `|q-q_c|^-4`,
which is not locally integrable in two action dimensions. The initial radial
field is `C^1`, so smooth eccentric orbital extraction makes `phi_k` locally
`C^1`. Its zero value gives `|phi_k(q)|<=C |q-q_c|`. The eigen-equation then
gives `(2.1)`, and Section 2.1 gives a bounded radial density. The additional
energy-forced zero gradient is not needed for this density estimate.

On a simple circular extremum chart, every fixed nonzero harmonic of a radial
`C^1` field obeys

    |phi_k(J,s)| <= C sqrt(J).

Subtract the field value at the circular radius and use the uniform radial
excursion bound `|r(theta,J,s)-s|<=C sqrt(J)`. The detuning assumption gives
`|h_k|<=C sqrt(J)/(J+x^2)`, and Section 2.2 gives the density bound. It is
essential here that the estimate is in physical phase variables, since the
kinetic amplitude itself can be unbounded.

The source is bounded on the regular division charts and the explicitly
assumed bounded-source support charts. Thus each of their radial densities
is bounded, because physical velocity and `L` range over a fixed compact box.

Finally there is no unproved summation over infinitely many nonresonant
harmonics. For `|k|>2|nu|/Omega_-`, write

    h_k=-w*phi_k-w*nu*phi_k/(k Omega-nu).

The first infinite sum is a bounded radial field composed with the orbit,
minus a finite Fourier polynomial and its orbit average. The second sum
converges uniformly absolutely: radial `C^1` regularity and bounded
`partial_theta r` give `|phi_k|<=C/|k|`, while
`|k Omega-nu|>=c |k|`. Hence the summand is `O(k^-2)`. This entire tail is a
bounded physical phase source. A finite localization of the remaining
resonant charts completes the proof that `mu_j in L^infinity`.

For the actual shell field let `m_j(r)=integral_(r'<r) h_j dGamma`. Then
`m_j'=mu_j` distributionally. The exact field equations are

    phi_f' = G*(m_t+m_f)/r^2,
    phi_t' = -2*c*M_t*m_t/r^4 + G*m_f/r^2.                 (3.2)

All coefficient functions are smooth on the fixed hollow shell, whose inner
radius is positive. The energy estimate already bounds `m` uniformly. Since
`mu` is bounded, `(3.2)` makes `phi'` Lipschitz. Every bound above is linear
in the initial `C^1` field bound, hence in `||h||Q`; the regular division
constants and the fixed weight/kernel bounds are finite. This proves `(3.1)`.

This proof is not circular: it starts from the established energy-to-`C^1`
estimate, obtains a new density bound from the actual kinetic equation,
and only then applies the actual radial field equation.

## 4. Eccentric Morse modes: the previous divisibility gap closes

On a compact eccentric chart, composition with the smooth orbit map and angle
integration send radial `C^(1,1)` to `C^(1,1)` in actions. Let
`N(q)=phi_k(q)` near an interior definite Morse resonance. Energy forces

    N(q_c)=0,   grad N(q_c)=0.

The gradient statement follows by integrating over an angular sector in
action space on which a nonzero linear term has magnitude bounded below by
`c |q-q_c|`: it would give a logarithmic divergence of the energy integral.
The Lipschitz gradient from Section 3 now yields

    |N(q)| <= C |q-q_c|^2 <= C' |k Omega(q)-nu|.           (4.1)

Thus the mode has a bounded receiving quotient at this Morse point.
This is an actual field-equation bootstrap, not an inference from energy
integrability alone. It applies to energy modes under the stated global
geometry. A distributional threshold response not in the energy space has
neither the initial field estimate nor the energy-forced zero jets used here.

## 5. Circular modes: an exact surviving force-trace condition

Take one species and suppress its index. Let `s_c` be an interior point of the
circular-radius interval with `kappa'(s_c)=0`, `kappa''(s_c)!=0`. The exact
twist identity in `GEOMETRY_AND_SCALING.md` is

    partial_J Omega(0,L_c(s_c))=kappa''(s_c)/(4*kappa(s_c)).

Consequently for `nu=k*kappa(s_c)`, `k>0`,

    k Omega(J,L_c(s))-nu
      = [k*kappa''/(4*kappa)]*J
        +[k*kappa''/2]*(s-s_c)^2
        +O(J^2+J*|s-s_c|+|s-s_c|^3).                     (5.1)

The two leading coefficients have the same nonzero sign. On a small chart,
the absolute detuning is comparable to `J+x^2`, `x=s-s_c`.

Choose the radial angle origin at one turning point, and put

    rho=sqrt(2J/kappa(s)).

The smooth oscillator expansion has

    r(theta,J,s)=s+rho cos(theta)+O(rho^2),

uniformly with the needed smooth parameter bounds. A radial `C^(1,1)` field
has, for either sign convention for that angle origin,

    phi_1(J,s)= (rho/2)*phi'(s)+O(rho^2),
    phi_k(J,s)=O(rho^2),   |k|>=2.                       (5.2)

Changing the angle origin changes a harmless nonzero unit phase in the first
formula. For the second formula, the affine part of `phi` has no harmonics
`|k|>=2` at order `rho`, and the radial Lipschitz derivative bounds the
Taylor remainder by `C rho^2`.

For `k>=2`, `(5.1)` and `(5.2)` immediately give a bounded quotient. For the
fundamental harmonic, if `phi'(s_c)=0`, then Lipschitz regularity of `phi'`
gives

    |phi_1(J,s)| <= C*(sqrt(J)*|x|+J)
                  <= C'*(J+x^2),                       (5.3)

again giving a bounded quotient. Conversely if `phi'(s_c)!=0`, set `s=s_c`
and let `J` decrease to zero. Equations `(5.1)` and `(5.2)` give

    |phi_1(J,s_c)|/|Omega(J,L_c(s_c))-kappa(s_c)|
      = [nonzero constant+o(1)]/sqrt(J).                 (5.4)

This proves the necessary and sufficient condition `(CF)`.

Although every nonzero receiving harmonic vanishes exactly at `J=0`, that
fact does not control the supremum over nearby eccentric receiving orbits.
Equation `(5.4)` describes precisely the failed uniformity.

### Energy membership does not force `(CF)`

For a prescribed `C^1` field with nonzero derivative, the leading formal
response is locally energy-integrable at this circular point:

    integral_0^eta integral_(-eta)^eta
          J/(J+x^2)^2 dx dJ < infinity.                  (5.5)

Indeed, `x=sqrt(J)*y` bounds the inner integral by `C J^-1/2`, and its
integral in `J` is finite. The local weight is smooth and strictly positive,
so it changes no integrability conclusion. In physical phase variables the
same singularity is `O(1/R)` in three variables, also square-integrable.
The generator differentiates in the orbit angle, not in the singular action
direction; differentiating the leading angular harmonic preserves this local
energy integrability. Thus membership in the eigen-generator domain alone
does not supply an extra action derivative which would force `(CF)`.

These are checks on a locally prescribed response. They are not a
self-consistent eigenmode construction.

## 6. Why the actual radial equation is not a local uniqueness ODE

Equations `(3.2)` are local in the cumulative masses, but the modal source
which determines `m'` is not pointwise local in the field. It contains

    phi_k(J,L)=(2*pi)^-1 integral phi(r(theta,J,L))
                                         exp(-ik theta) dtheta,

and therefore samples the entire radial interval of each orbit. Eliminating
the kinetic unknown produces an integral equation, not a closed homogeneous
second-order radial ODE with a smooth pointwise coefficient.

For accessible modes each species has zero total perturbation mass, so
`m=0` and `phi'=0` both in the hollow core and beyond the outer shell.
Infinity normalization gives `phi=0` for `r>=R`; in the hollow core the
potential can instead be a nonzero constant. These are the valid endpoint
conditions.
An ODE uniqueness theorem cannot be applied to them until a local closed ODE
has actually been derived. Radial locality of the force restricts the orbital
sampling interval to a warm-tube neighborhood; it does not replace the orbit
integral by multiplication by the field at the receiving radius.

The force-trace condition `(CF)` is an interior radial condition, at an
interior circular radius. Smooth or Lipschitz field regularity, exterior zero
data, and a bounded density do not themselves connect that value to zero.
The field equation must still be used as a global spectral equation to prove
or refute that cancellation. No endpoint unique-continuation conclusion has
been established by this note.

## 7. Exact work implication and remaining research obligation

For a single mode with field `exp(-i nu t)*phi`, a receiving harmonic obeys

    W_k(t,q)=-i nu phi_k(q)*integral_0^t
                                exp(i*(k Omega(q)-nu)*s) ds.

For nonzero detuning its time supremum is

    2*|nu|*|phi_k(q)|/|k Omega(q)-nu|.

Thus `(4.1)` settles the eccentric Morse contribution under the geometric
contract. At a simple fundamental circular threshold, `(CF)` is exactly the
remaining local modal-work criterion. If an actual energy mode has a nonzero
force trace there, its receiving work is unbounded uniformly over nearby
eccentric orbits, even though work on the circle itself is zero and the
kinetic mode has finite energy.

No actual mode with that trace has been produced. Neither the full work
theorem nor its negation follows from this local result. The exact remaining
obligations are:

1. Prove the finite resonant geometry and bounded-source cap contract for the
   selected cold-mass-dominant actual halo (or retain those restrictions).
2. Derive `(CF)` from the complete homogeneous actual mode equation, exclude
   such fundamental circular modes by another spectral argument, or construct
   an actual energy eigenmode with a nonzero force trace.
3. Independently prove the regular reduced, frequency-dependent boundary
   inverse; a bounded single-mode quotient does not imply that inverse.

## 8. Proof-audit pass and provenance

Primary verdict: **proved as written under the explicit finite resonant
geometry of Section 1** for `(3.1)`, `(4.1)`, and the circular criterion
`(CF)`. This is a self-review, not an independent audit.

Dependency checks:

- Energy-to-`C^1`: existing actual source A3, retained exactly.
- Morse zero value and zero gradient: proved by local energy divergence;
  gradient cancellation is used only after bootstrap.
- Eccentric radial turning Jacobian: included explicitly, with the
  submersion `partial_J r_+=Omega/U_r` and logarithm/fold estimate.
- Circular action-angle singularity: removed using actual physical phase
  variables and the positive quadratic well estimate `(2.2)`.
- Infinite harmonic tail: summed explicitly by the order-`k^-2` identity.
- Two species and actual shell kernels: both retained in `(3.2)`; no scalar
  tracer or weak-mass replacement.
- Circular value versus nearby supremum: distinguished in `(5.4)`.
- Cap-only resonant trace: not inferred from energy; left as an explicit
  weighted-source/division input when geometry has not supplied it.
- Actual existence or absence of a circular mode: not addressed.
- Full reduced limiting absorption and nonlinear confinement: not addressed.

Research-program and proof-audit skill texts were read. The unavailable
research-attempt workflow was not substituted by an invented numerical test.
Only text reads, analytic derivations, this new text artifact, and metadata
hashes were used.

## 9. Raw inputs and SHA-256 hashes

Paths below are relative to
`/Users/carlzimmerman/new_physics/zimmerman-formula`. The parent requested
`full_feedback/RESULT.md` is actually under `claude_continuation_2026_10_19`;
the nonexistent sibling path was not used as evidence.

- `real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/CONTINUATION.md`:
  `3ec0ba51d22f172a31a771ec197678a25cd1a49f013c8cfe09a82d3457d63f81`.
- `real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/SINGULAR_PENCIL_AND_MODES.md`:
  `3c091ca4be949d0bdf3c1657897a962cb7f60b137f03657c23b8af80a25e5c94`.
- `real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/SPECTRAL_OPERATOR.md`:
  `52c042ff02f04c0e6917e2591d9527fbf07952ce64b6f674b240f83e4c9fb47c`.
- `real_research/analytic_review_2026_10_18_codex/actual_feedback_2026_10_19/GEOMETRY_AND_SCALING.md`:
  `1848347266a2254e18fc579c3c6804cd6703895ce9d298f804a69acd977558c9`.
- `real_research/analytic_review_2026_10_18_codex/claude_continuation_2026_10_19/full_feedback/RESULT.md`:
  `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
