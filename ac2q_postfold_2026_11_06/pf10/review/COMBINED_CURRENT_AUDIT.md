# Independent audit: combined escape with a finite scalar current

**Verdict: correct only after explicitly retaining identified regular
outer current traces in the product-identity step.** Under that trace
hypothesis (already used in the preceding regular-corner class), the
candidate excludes total matter surface stress even with simultaneous
unbounded r and clock rapidity. It does not exclude every singular limit.

Audited statement: the parent's PF10 candidate message beginning
"Full-switch before-IBP aux L=E[H-mu(Ar-1)]". No PF10 input file existed
at inspection. Requested base was `043b85ce2f`; working HEAD at inspection
was `ede3afcf5b5b9eb1ce495f049721eb4d973a9dfe`. This report records an
independent derivation, not a numerical test or an audit of an unseen file.

## Precise claim and required limits

Consider native smooth layers approaching a regular timelike planar
interface. Retain regular nondegenerate metrics converging uniformly,
uniform cap separation, compact clock-label and potential ranges,
r>=r_min>0, and 0<A_min<=A<=A_max. Retain uniform phi convergence to a
continuous scalar with a regular interface trace, strong uniform
same-clock endpoint Pi matching, and regular common outer A traces.
The coordinate components of the total stress and the specific current
derived below must have uniform total-variation bounds on compact sets.
Assume identified piecewise-regular outer bulk limits, including the
scalar current, and no unaccounted bulk oscillatory measures. Stress
conservation must have no normal dipole with well-defined limiting metric
contractions. Explicit scalar sources must remain bounded.

These are assumptions on a sequence of solutions, not deductions from
the pointwise constitutive law. No upper bound on r, phi_t, or unit-clock
rapidity is used. The conclusion is zero total matter surface stress.

## Current from the native action

Let E denote the volume density, Pi=exp(2 beta)P, Q=Ar, and

    H=r^2/2-V-W+(Ar-1-gamma r^2)^2/(2 gamma),
    D_eff=(Ar-1)/gamma-r^2,
    D=D_eff-mu,   mu>=0,   mu(Ar-1)=0.

The before-integration-by-parts density is

    L=E[H-mu(Ar-1)]-A(phi_t Pi_x-phi_x Pi_t).

Use the future unit clock n=-grad(phi)/r, so dphi(n)=r and the variation
of r with respect to phi_a equals n^a. With h=H_r at fixed A,P, its
canonical density current is exactly

    J^t=E(h-mu A)n^t-A Pi_x,
    J^x=E(h-mu A)n^x+A Pi_t.

Thus J=J_base-A curl(dPi), where curl(dPi)=(Pi_x,-Pi_t).
The scalar equation is div J=-E(V_phi+W_phi). In the shift-symmetric
case the right side is zero. For a regular rolling potential it is a
bounded explicit source on the declared clock/cap range.

This is a specified native Noether-current representative for the displayed
boundary-reduced action. The Q-to-Ar change depends on dphi, but its extra chain-rule term is
proportional to the Q stationarity equation including the multiplier.
That equation vanishes on shell. This does not prove identity with a
canonical higher-derivative current assigned to the original P.acceleration
action: replacing that term by -D already removed a divergence whose
boundary density depends on the clock derivatives. Such representatives
can differ by an identically conserved improvement. Integrating the
topological term by parts introduces the explicit improvement curl(A Pi).
The finite-current assumption here concerns the before-topological-IBP
representative explicitly displayed; finite variation is not invariant
under an uncontrolled improvement. Its native scalar divergence equation
and contraction are nevertheless exact.

Since phi_t Pi_x-phi_x Pi_t=E r D,

    J.dphi/E=r h-mu Ar-ArD
             =r h-Ar D_eff
             =r^2(1-2 gamma D_eff)
             =r^2(3-2Ar+2 gamma r^2).

The multiplier cancels exactly. All signs and factors in the candidate
contraction pass. For bounded A and gamma>0 this polynomial is bounded
below by gamma r^4-C.

## Multiplier mass and transverse coercivity

On each clock crossing,

    e Pi=exp(2 beta)D,    eA=W_P/r.

The positive part of D is uniformly bounded, because
D<=A_max r/gamma-1/gamma-r^2, whose positive maximum is finite for all r.
A conformal clock graph has |dt/dx|<1 and proper length O(epsilon)
through a shrinking timelike strip. The interface's strict timelike
margin makes this uniform on each compact segment even for large boosts.
Hence positive Pi variation is O(epsilon). Uniform endpoint matching
makes negative variation o(1), and mu<=D_- gives slice multiplier mass
o(1). The same argument bounds Pi's entire oscillation in the crossing;
eA and cap separation bound A's oscillation by O(epsilon).

Lorentzian coarea is exactly dVol_base=r^{-1}dphi d ell. Uniform phi
convergence on a compact enlarged coordinate region bounds the relevant
label range. Uniform slice estimates and r>=r_min therefore imply
vanishing spacetime multiplier mass. No upper bound on phi_t is needed.
Strong exterior traces supply continuous common limits Pi_Sigma,A_Sigma
uniformly across the layer. Mere pointwise-in-label matching is not enough.

The transverse identity T_perp=H+P W_P and the cap bound give a uniform
L1 bound for H from the finite total stress measures. Also
H>=c r^4-C for bounded A and potentials, so r^4 has bounded layer mass.
This step bounds that mass; it does not yet prove it vanishes.

## The base-current split

In a regular orthonormal frame with time component n^0=C>=1, write
k=r h-mu Q. The exact identities are

    T_00=-H+k C^2,
    J_base^0=k C/r=(T_00+H)/(r C).

Every other base-current component has absolute value at most this
time-component absolute value. Coordinate and orthonormal estimates are
equivalent by regular metric bounds. On r C>L, its layer mass is bounded
by C/L times the uniformly bounded stress-plus-H mass. On r C<=L,
r and C are bounded (using r>=r_min), h is bounded, and
|J_base|<=C_L(1+mu). Its layer integral tends to zero. Let epsilon tend
to zero first and then L to infinity: J_base has no surface mass.

This proves the needed vanishing layer mass, not a gratuitous global
uniform-integrability theorem for all possible bulk concentration sets.
It permits cancellation inside total T; no separate bound on mu n n is
used.

## Why the total current has no surface measure

Finite total J and bounded layer mass of J_base imply a bounded measure
norm for A curl(dPi). Since A>=A_min, dPi has bounded variation locally.
The strong continuous Pi trace gives no derivative jump measure on the
interface. Strong uniform A convergence across the layer permits the
weighted derivative limit to be multiplied by A_Sigma, with error bounded
by the A sup-norm error times that variation bound. Thus A curl(dPi),
and hence J, have no surface measure. This step controls rapid tangential
oscillations that the earlier stress-only arguments did not control.

The lower bound on A is load-bearing here. Finite total current alone
does not bound the unweighted Pi derivative if A can tend to zero.

## Product identity and its exact trace obligation

At every smooth stage,

    div(phi J)=J.dphi+phi div J.

Uniform phi convergence and the finite J measure bound permit passing
phi J to the limit without multiplying weak gradients. The source term
passes by the explicit bounded-source hypothesis. The identified regular
outer current has normal jump zero because div J has no surface source.
Since phi has a common trace, the surface coefficient in div(phi J) is

    [phi J.N]=phi_Sigma [J.N]=0.

Therefore the positive-coercive contraction J.dphi has no surface
measure. Its lower bound gamma r^4-C forces the layer mass of r^4 to
vanish. This establishes the desired exclusion of simultaneous large-r
and boost concentration within this finite-current class.

The regular identified outer-current trace is the important qualification.
Absence of a surface measure in J does not by itself imply absence of a
surface measure in its divergence: even a bounded piecewise constant
current can have a delta divergence. The scalar equation removes the
normal jump of J, and the regular trace product removes the jump of
phi J. If one allows arbitrary unidentified singular bulk currents, this
step requires a separate normal-trace/product theorem; the assumptions
"finite J" and "uniform phi" alone must not be quoted as that theorem.

## Completion and scope

With vanishing r^4 and mu layer masses,

    tr_base T=2H-r h+mu,    T_perp=H+P W_P

both have no surface measure. Uniform metric convergence and total stress
variation bounds justify contraction of the limiting measure. Symmetry
and no normal dipole make the longitudinal surface tensor s T_a T_b
for a unit timelike interface tangent T. Zero base trace gives s=0;
planar symmetry and the transverse estimate remove the other components.

All algebraic, coarea, base-current and trace steps pass. The product step
passes with the regular bulk/outer-current trace assumption explicitly
retained. The PF09 constitutive counterexample is not contradicted: it
never supplied differential solutions with this finite matched current
and identified regular outer limits. This result supplies neither native
post-breakdown existence nor an outgoing selection principle. Cap escape,
A approaching zero, clock degeneration, nonmeasure currents, singular
metric products and unidentified bulk defects remain outside its scope.

## Actual-file follow-up

Subsequently audited `pf10/COMBINED_CURRENT_EXCLUSION.md`, SHA256
`8f818cb02a142aede4753207d6fe96f36b973604c19caebeba4ecaf6a35a5905`.
It explicitly includes the identified piecewise-regular outer-current
trace qualification in its layer class and Step 5. Therefore the primary
verdict for **that exact file is proved as written**, with the finite
total-variation hypothesis applying to its specified native Noether-current
representative. The earlier qualified verdict addressed the initial message.

Its derivation of A bounds from anchored positive regular outer traces
and eA=W_P/r is valid: it need not assume an additional independent upper
r bound. The D-positive-part bound and all six subsequent steps agree
with the independent calculation above. The phrase "exact native current"
must mean a native representative with the displayed divergence equation,
not a proved identity with the canonical higher-derivative current of the
pre-boundary-reduction action. The original P.acceleration divergence and
the later topological integration by parts are distinct boundary operations.
