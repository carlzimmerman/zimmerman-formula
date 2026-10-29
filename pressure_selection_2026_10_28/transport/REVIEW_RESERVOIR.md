# Independent derivation of the PN28 reservoir result

Reviewer: `/root/empirical_audit`, 2026-10-28. Requested checkpoint base:
`66c45c5082f651dd54e171f98c11acd9cb3d9086`. Live HEAD when the audited text
was read: `7954d48377463cafcae3e8dbb09454134aef384f`.

The initial exact audited input is `../reservoir/DERIVATION.md`, SHA256
`e8aeec7e98cd5d607ba1702bcd8fe10afbcdd720d1cfa8130ecf756670884f0b`.
Line references below refer to that initial revision. After the author applied
the requested qualifications, the reviewer reread the complete final text,
SHA256 `3ccd3ea33c0f1b9addddcfd18e758f55c15f235db90e244a18c9e83ffd864d7c`.
Its lines 22-24 now state the physical pressure domain, line 95 requires
nonzero enthalpy, and lines 118-120 correctly identify the degenerate boundary.
The proof-level verdict below applies to this corrected final revision too.
The reviewer knew the proposed sound-speed formula before deriving it. This is
an independent reconstruction from the stated equations, not a blind review,
formal certificate, or validation inferred from the author's numerical checks.
No reservoir file was changed, and no numerical program was needed for this
algebraic review.

**Verdict:** the exchange solution, total pressure, and proposed acoustic
formula are correct under the stated instantaneous, fixed-parameter, local
perfect-fluid closure. The negative squared acoustic speed at `p>A` follows.
Two precision fixes were sent to the author and incorporated before the final
verdict: explicitly
state the physical kinetic domain `p>=0` (strictly positive for an interior
state admitting ordinary two-sided linear perturbations), and identify
`p=A` as a degenerate acoustic boundary. The general formula also requires
nonzero total enthalpy. These qualifications do not change the MC27 dense-core
conclusion.

## 1. Derivation of the reciprocal exchange

Take the raw hypotheses at lines 14-33: conserved mass density, isotropic
nonrelativistic random energy `K=3p/2`, no random-energy flux, fixed positive
`A,rho_ref`, and `p=A log(rho/rho_ref)`. Set `z=log(rho/rho_ref)`.
Continuity gives `Dz=-theta`, and therefore

    DK+(K+p)theta = (-3A/2+5p/2)theta = Q.

For a reservoir with `b=1+w` and `De+b e theta=-Q`, a state family `e=e(z)`
obeys

    e_z-b e = A(5z-3)/2.

This statement is conditional on following the prescribed material state
family through compression/expansion; a static trajectory alone supplies no
such derivative. The caveat at lines 45-47 is necessary and correct.

For `b!=0`, write `e=C exp(bz)+alpha z+beta`. Matching the linear and constant
terms gives

    alpha = -5A/(2b),
    beta  = -5A/(2b^2)+3A/(2b).

For `b=0`, direct integration instead gives

    e_V=C+5A z^2/4-3A z/2=C+5p^2/(4A)-3p/2.

These reproduce equations (5)-(7), including the `-9A/32` radiation constant.
The `b=0` expression is a separate parametrization; taking `b->0` in (5) with
the same fixed numerical `C` need not have a finite limit.

`C` is an advected integration constant, not a selected amplitude. On any
compact state interval, `exp(bz)` is positive and bounded away from zero, so
the stated large-`C` positive-energy construction is valid. In the vacuum
case an even stronger elementary check is available:

    e_V=(5A/4)(z-3/5)^2+C-9A/20.

Thus `C>9A/20` makes the reservoir positive on the entire physical log branch
`z>=0`, for every positive `A`. Positivity cannot remove the normalization
freedom or the acoustic sign below. A constant vacuum energy fails the
exchange condition except at `theta=0` or the isolated state `p=3A/5`;
nonzero compression immediately changes that state. The MC27 interval
`p/A>=2/3` excludes even that instantaneous exception.

## 2. Pressure and inertia require momentum conservation

The energy equations alone do not establish a perfect-fluid stress or lock
two non-vacuum components to a common velocity. Equation (8), lines 75-83,
adds that constitutive hypothesis. Under it, define

    epsilon=rho c^2+3p/2+e,
    P=p+w e,
    H=epsilon+P=rho c^2+5p/2+b e.

Adding the two internal energy equations and the rest-mass equation gives
`D epsilon+H theta=0`. At fixed `C,A,rho_ref`, the state derivatives are

    rho e_rho = b e+(5p-3A)/2,
    rho epsilon_rho = rho c^2+5p/2+b e=H,
    rho P_rho = A+w[b e+(5p-3A)/2].

These independently reproduce (9)-(10). If `C` is allowed as a state
coordinate, the residual in the total energy equation is `e_C DC`, where
`e_C=exp(bz)` or `1`, respectively. Hence conservation makes `DC=0` in this
model. An advected entropy/composition mode is consistent with fixed `C`
for the propagating acoustic perturbations.

For a vacuum reservoir this momentum accounting is compulsory. With metric
signature `(-,+,+,+)`,

    T_V^{mu nu}=-e_V g^{mu nu},
    nabla_mu T_m^{mu nu}=+nabla^nu e_V.

The timelike matter projection supplies `Q=-De_V`; the spatial projection
supplies `+grad e_V` in the instantaneous rest frame. Thus matter's Euler
force is `-grad p+grad e_V=-grad(p-e_V)`. Vacuum contributes no enthalpy:
`e_V+p_V=0`. Its pressure gradient nevertheless remains in the force.
Suppressing this transfer while retaining a spatially varying `e_V`, with
no other compensating stress, does not conserve total momentum.

This confirms the pressure-gradient reversal in (14) at uniform `C`. It also
confirms that the original MC27 hydrostatic profile is not automatically an
equilibrium of the augmented model. The acoustic argument is a local
constitutive/characteristic test; it is not a calculation of global normal
modes around an unchanged, self-consistent MC27-plus-vacuum equilibrium.

## 3. Acoustic characteristic derived directly

Freeze a uniform rest state with `rho_0>0` and `H_0!=0`. At fixed `C,A,rho_ref`,
linearized continuity and total momentum conservation are

    partial_t delta rho+rho_0 div delta u=0,
    (H_0/c^2) partial_t delta u+P_rho grad delta rho=0.

Eliminating `delta u` yields

    partial_t^2 delta rho-c_s^2 Laplacian delta rho=0,
    c_s^2=c^2 rho_0 P_rho/H_0=c^2 (dP/d epsilon)_C.

Consequently equation (11) follows from a spatial characteristic calculation,
not from a cosmological or background time-derivative ratio. If an independent
advected `C` is retained, the homogeneous local system has an additional
zero-frequency entropy/composition mode; a nonzero-frequency acoustic mode
has `delta C=0`. Background gradients enter a local frozen-coefficient
analysis at lower differential order. Delayed exchange, independently moving
reservoir matter, heat flux, or anisotropic stresses instead change the
principal system and are outside this calculation.

For `w=-1`, substitute the independently integrated reservoir directly:

    epsilon=rho c^2+C+5p^2/(4A),
    P=5p/2-C-5p^2/(4A),
    H=rho c^2+5p/2,
    rho P_rho=5(A-p)/2.

It follows exactly within this effective closure that

    c_s^2 = 5 c^2 (A-p)/(2rho c^2+5p).

The integration constant cancels from both the inertia and pressure response.
For physical positive-pressure states, `H>0`; hence `p>A` implies imaginary
acoustic characteristic speeds, or `omega^2=c_s^2 k^2<0` for the uniform local
problem at nonzero wave number. The claim concerns wavelengths for which the
continuum closure and local approximation are applicable. It neither provides
a microscopic ultraviolet extrapolation nor proves that every possible
interacting-vacuum completion has this characteristic.

Using the supplied MC27 relation `p/A=-log x+2/3`, the transition is exactly
`x=exp(-1/3)`. At `x_c<=1/4`, `p_c/A>=log(4)+2/3>1`, so continuity supplies
a nonempty neighborhood with the negative sign. This is a conditional
obstruction to the specified stable instantaneous local fluid completion.

## 4. Domain, boundary, and units audit

- The target's initial `rho>0` and logarithmic formula permit negative `p`
  mathematically when `rho<rho_ref`. An isotropic nonrelativistic kinetic
  stress has `p>=0`; impose that physical restriction explicitly. The
  unqualified positive-enthalpy sentence at line 115 otherwise does not
  follow. For general constant `w`, even `e>=0` need not imply `H>0` if
  `w<-1`. Equation (11) requires `H!=0`; an ordinary positive-inertia fluid
  interpretation requires `H>0`.
- At `p=A`, the acoustic restoring derivative vanishes. The acoustic block
  is not strictly hyperbolic there; zero `c_s^2` alone does not demonstrate
  stability. At `0<p<A`, its sign is positive, but causality requires the
  separate inequality `5A<=2rho c^2+10p`. The report already correctly
  separates a positive sign from causality and global stability.
- At `p=0`, the kinetic state lies on the boundary of admissible pressure;
  arbitrary two-sided density perturbations on the exact log curve leave
  that physical domain. The ordinary interior-state acoustic interpretation
  therefore requires care at this boundary.
- `rho` is mass per volume; `A,p,e,C,epsilon,P,H` are energy per volume.
  `z,b,w` are dimensionless, `theta` has units inverse time, and `Q` is
  energy per volume per time. Both the numerator and denominator of (11)
  have pressure units. The factor `c^2` in (12) is required for velocity
  squared. No additional factor of mass density or `c^2` is missing.
- The relativistic-looking inertia is justified by the assumed total
  perfect-fluid stress, while `K=3p/2` remains a cold-particle constitutive
  approximation. It is not an exact relativistic kinetic derivation. The
  intended physical application should retain `p<<rho c^2`; the document
  states this at lines 81-83.

Finally, direct differentiation of `a=p/z` using the isotropic trace equation
reproduces (15), including the factor `3z` in its denominator. The proposed
relaxation prescription gives `Da=gamma(A_star-a)` identically; it inserts a
target amplitude instead of predicting it. No missing conservation equation
in the audited model selects `A`.

The proof-level findings above do not use the reservoir script's pass/fail
outputs as evidence. The transport route's own self-check is likewise not an
independent peer review; its separate coordinator reconstruction is recorded
in `COORDINATOR_REVIEW.md`.
