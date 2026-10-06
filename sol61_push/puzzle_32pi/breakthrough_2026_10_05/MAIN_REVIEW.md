# Independent audit of the conservative formation switch

Primary verdict: **correct only after a stated restriction**. The local stress,
constraint, dispersion and smooth cold-transition results reconstruct under the
report's frozen-current/frozen-B hypotheses. Its quoted exact formation-ramp
solution additionally requires B f'(q)=0 throughout the ramp, for example B=0.
This condition is not stated explicitly in the ramp subsection and fails for a
nonzero restored gate during the interpolation. The complete gravitating model
remains incomplete for the reasons below.

Audit owner: independent sibling agent `puzzle_32pi`. Shared base
`a36191815030afddf1277d413f488fb0c3ac520f`. This audit writes only this file;
no main-folder scripts were executed because their default execution writes
results there. An independent in-memory symbolic reconstruction and 40-digit
spot calculation were executed. No author's test count was used as evidence
for the mathematical implications.

Pinned inputs read and reviewed:

- `sol61_push/main_theory/breakthrough_2026_10_05/REPORT.md`, SHA256
  `76ed046b31f22d9a9803299105059cf4fd3a34e1e6630c84da117ed75e1813e8`.
- `sol61_push/main_theory/breakthrough_2026_10_05/formation_checks.py`, SHA256
  `d16600024078a4e768ee77256536a2a32ea467e1190c4fb32a12d39f985ae22a`.

## Claim card and dependency scope

The object audited is an appended material internal state with conserved baryon
current, signature (-,+,+,+), and local action

    S_int = integral sqrt(-g) [n I/2 (u dot dq)^2
                 -n K/2 (q-Q(n))^2+B f(q)] d^4x,
    I,K>0.

The report permits Q(n/nbar); derivatives Q_n below mean derivatives with
nbar frozen in the local patch. Its nonlocal varied leaf-average extension
is not part of the local dispersion calculation. B is a signed Lagrangian
energy density; physical internal static energy is nK(q-Q)^2/2-Bf. The audit
checks exact plateaus, a regular single-stream material evolution, local
longitudinal linearization, and a smooth stable stationary interpolation.
These objects are not the full baryon/metric/MOND constrained action.

Dependency chain: conserved-current kinematics -> internal first variation and
q equation -> local static energy Hessian -> positive local kinetic matrix ->
local mode signs. Identification of this chain with the physical degrees of
freedom of the fully assembled theory is unproved. The frozen-B step excludes
constitutive/gravitational reaction, and the frozen nbar step excludes global
mean-density reaction.

## Saturated stress and the transport/production claims

Let h=u dot dq and d=q-Q. At h=d=0,

    delta[n I h^2/2-n K d^2/2]
      =(I h^2/2-K d^2/2)delta n+n I h delta h-n K d delta d=0.

This is valid for variations of metric, current, q and even a nonlocal Q,
provided the branch satisfies the equalities pointwise. Multiplication by
sqrt(-g) adds another term proportional to the vanishing integrand. Thus
the appended oscillator's first functional variation and its stress vanish
there. This conclusion does not need one to hold n, u or Q fixed during
variation. At q=0 on the flat OFF plateau, f=f'=0 removes the gate variation
as well. At q=1 on flat ON, f=1,f'=0 leaves precisely the original B sector's
variation; its stress is not zero. These conclusions are correct.

This does not establish that dynamically collapsing matter stays on h=d=0:
if Q_n is nonzero then Dq=Q_n Dn need not vanish. Nor does the vanishing of one
appended sector establish that the complete FRW gravitational action is OFF.
The report generally keeps these distinctions correctly.

The passive-label equation Dq=0 preserves constant OFF initial data on each
regular characteristic. It cannot produce ON through collapse. This is
correct until the supplied smooth timelike single-fluid description fails.
It supplies no merger or multistream ownership prescription.

For the fixed homogeneous current production attempt, L=J lambda qdot-
J lambda R(q)+B f(q) gives constraints p_lambda=0 and p_q-J lambda=0.
Their Poisson bracket is nonzero with magnitude J. Eliminating them leaves
canonical q,p_q, not an additional constraint on p_q, and

    H=p_q R(q)-B f(q).

At any admissible q with R(q)!=0, an unconstrained real p_q makes H unbounded
below. This is an exact reduced fixed-current result. The R=0 control removes
the linear momentum energy and therefore escapes this objection. The report's
explicit limitation to this minimal completion is warranted; a gravitational
constraint or extra species restriction has not been derived here.

## Local oscillator/fluid dispersion and gas response

At B=0, stationary q=Q, E=e_gas(n)+nK(q-Q)^2/2 has

    Eqq=nK, Enq=-nK Q_n, Enn=e_gas''+nK Q_n^2.

Its Schur complement equals e_gas''. I independently differentiated E to
verify the cancellation. In the homogeneous material rest frame use
longitudinal displacement xi, delta n=-n div xi, and delta q. Under the stated
NR kinetic approximation the inertias are nm and nI. The stiffness matrix is

    [[n^2 Enn k^2, +/-n Enq k],
     [ +/-n Enq k, Eqq]].

The sign depends on Fourier phase convention and cancels from the determinant.
With c_gas^2=n e_gas''/m, A=c_gas^2 k^2, b=K/I and
G=n^2 K Q_n^2 k^2/m, its characteristic polynomial is

    w^2-(A+G+b)w+Ab
      =(A+G-w)(b-w)-Gb.

For A,b>0 and G>=0 its discriminant is
(A-b)^2+2G(A+b)+G^2, and both roots are positive. This verifies the reported
coupled dispersion rather than merely its symbolic polynomial identity.
At A=0 there is a zero root; strict positivity does not extend to cold B=0
matter or k=0. The report states its positive-A restriction.

For the low eigenvalue, w_low<=A. Requiring w_low>=.9A, with b>.9A, is
equivalent to evaluating the polynomial at .9A on the lower side of its vertex:

    p(.9A)=A(10b-9A-90G)/100 >=0,
    hence G<=b/9-A/10.

The restriction b>.9A is needed; the exactly uncoupled equality boundary can
be included separately. Therefore the reported squared-frequency fidelity
criterion is correct. It tests omega^2, not an equal fractional tolerance
on omega itself or a complete gas-pressure transfer function.
At K large, G/b=n^2 I Q_n^2 k^2/m remains. Increasing K alone cannot ensure
finite-frequency gas fidelity. This is a valid obstruction to that proposed
way of suppressing the response cost.

The positive material-state oscillator evades a strictly positive free-space
scalar spatial-propagation premise: it has no standalone spatial-gradient
term and is carried by the material. This is not a proof of covariant
hyperbolicity, collisionless transport, or the full theory's characteristic
cone. The report explicitly withholds these claims.

## Restored gate and transition obstruction

For frozen B>0, E=e(n)+nK(q-Q)^2/2-Bf(q), independent differentiation gives

    Eqq=nK-B f'',
    Enq=K(q-Q)-nK Q_n,
    Enn=e''-2K(q-Q)Q_n+nK Q_n^2-nK(q-Q)Q_nn.

These match the implemented formulas, including the terms proportional to
q-Q. A stationary q_*(n) with Eqq>0 obeys q_*'=-Enq/Eqq, so

    E_eff''=Enn-Enq^2/Eqq.

The proof using h=E_eff-mn, constant plateau values 0 and -B, and zero endpoint
slopes is correct: h''>=0 would force its nondecreasing derivative to vanish
identically, contradicting the step. Continuity gives a region of negative
curvature. The quantitative lower bound sup(-h'')>=2B/L^2 follows from the
stated weighted integral; it does not require that this bound be sharp.

At a negative Schur point with Eqq>0 the density/internal Hessian determinant
is negative. Multiplication by positive n and k factors preserves its sign
for every k!=0. With the assumed positive local inertias, one eigenvalue is
negative and one positive. Thus the pressureless frozen-patch claim is correct.
If Enn>0, the low high-k eigenvalue approaches
(Eqq-Enq^2/Enn)/(nI), which is finite and negative. Calling this automatically
a Hadamard instability would be unjustified; the report avoids that claim.

Independent 40-digit spot checks of the explicit stationary solution give:

| n | Schur complement |
|---|---:|
| 1.10 | -0.000388899642780 |
| 1.25 | -0.0636734277947 |
| 1.50 | +0.000130782494933 |
| 1.75 | +0.0636251103904 |
| 1.90 | +0.000388861560371 |

These corroborate existence of the claimed negative region, rather than prove
the theorem by sampling. Pressure adds e'' to the Schur complement and can
remove it. The numerical high-pressure/small-inertia control is a costed,
dimensionless example; it does not establish astrophysical gas fidelity.
The general obstruction is conditional on smooth stationary plateaus,
pressureless mass energy, the nonzero frozen energy step, and a physical
negative direction surviving the full constraints. These restrictions matter.

## Formation-ramp restriction and smallest missing implication

Current conservation and variation of q give

    I D^2 q+K(q-Q)=B f'(q)/n.

For B f'(q)=0 and a prescribed linear Q=t/T, the reported solution
q=t/T-sin(omega t)/(omega T), omega=sqrt(K/I), and persistent amplitude
2|sin(omega T/2)|/(omega T) reconstruct exactly. This demonstrates absence
of damping in the gate-free driven oscillator.

For restored B!=0 with a non-flat interpolating f, the right-hand side is
nonzero during crossing, so these are not exact solutions of the quoted
full switch action. The amplitude/energy figures must be labeled **B=0
formation controls**, or the forcing term must be included in a new calculation.
They also do not conserve the internal sector energy: the prescribed driver
supplies work. The report correctly notes that this work needs a fluid reaction
budget in a self-consistent collapse solution.

The smallest missing arrow toward the assembled construction is to show that
the negative reduced transition direction is a physical mode after varying
B, nbar and the full baryon/gravity constraints, or explicitly show which
constraint/reaction removes it. Neither a sector stress cancellation nor a
fixed-patch positive control supplies this reduction. Beyond that arrow,
formation from OFF initial data, merger ownership, multistream transport,
physical parameter fitting and the cold-sector source map remain unproved.

Strongest safe statement: a conservative material oscillator supplies an exact
unexcited OFF sector and a healthy positive-compressibility frozen local
branch, while a smooth zero-cost pressureless frozen-energy switch necessarily
contains a negative local stiffness region. The complete requested sourced,
conserved gravity model has not been established.
