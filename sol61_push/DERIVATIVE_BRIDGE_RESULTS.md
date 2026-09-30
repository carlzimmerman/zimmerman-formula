# Derivative bridge: exact local response and a rolling-scale obstruction

Verdict: correct only under the stated restricted sector and matching
assumptions. This is self-review. It tests the next bridge proposed in
SELF_TUNING_GALAXY_BRIDGE_RESULTS.md, rather than claiming a combined
self-tuning gravity theory.

## Restricted action and shift test

Use c=ħ=1, positive M²,Kc,Z and timelike X=−(∂phi)²/2>0.
Replace the earlier cubic coefficient q by a positive C² function f(X).
The tested local sector is

    L=Z X−V0−T phi+2M² P a−M²P²−Kc f(X)P³.

Here P>=0 is the algebraic outward polarization amplitude and a the
clock acceleration. Its preferred-direction structure and gravitational
action are held fixed in the local propagation test. This is not the earlier
q potential and lambda(q) action, and is not asserted to self-tune by itself.
Additional Horndeski terms necessary for well tempering have not been included.

For a minimally coupled tadpole, phi→phi+epsilon and
V0→V0−T epsilon leave this sector invariant: X and f(X) do not change.
Thus the derivative bridge passes the algebraic test that a linear phi
coefficient failed. This supplies no degeneracy or radiative-protection proof.

## Polarization, scalar current and lapse equations change together

Algebraic variation gives

    a=P+3Kc f(X)P²/(2M²).

The scalar equation from this sector is

    ∇mu[(Z−Kc f_X P³)∂mu phi]=T.

For a homogeneous metric it means d(a_scale³ J)/dt=−a_scale³ T,
with J=(Z−Kc f_X P³)phi_dot. Horndeski derivative terms would contribute
additional currents. The coefficient cannot be inserted into an old scalar
equation while neglecting these new contributions.

For zero shift and phi=omega t, X=omega²/(2N²). The cubic contribution
to the lapse variation, after removing the spatial volume factor, is

    −Kc [f(X)−2X f_X(X)]P³.

The polarization equation uses f, whereas the lapse equation uses
f−2Xf_X. Hence importing the previous constant-coefficient flux equation
would miss a stress contribution. For f=(X/Xref)^n that contribution is
(1−2n)f; it even vanishes at n=1/2 without removing the polarization term.

There is a useful restricted radial identity. In the stationary spherical
metric of SPHERICAL_CLOCK_CONSTRAINTS_RESULTS.md, let E=exp(2sigma),
F=N²−E Vshift² and phi=omega t+psi(r). Then

    X=[(omega−Vshift psi')²/N²−psi'²/E]/2.

In the non-Horndeski current sector above, zero radial current on a branch
with Z−Kc f_X P³ nonzero gives

    psi'=−omega E Vshift/F,   X=omega²/(2F).

Thus X, and generally the galaxy coefficient, vary with the redshift potential
even in a zero-flux construction. This is a kinematic/current identity,
not a stationary solution of the tadpole equation: nonzero T requires a
time-current response or additional terms. No conserved-source solution
or full Horndeski zero-current condition is supplied by it.

## Scalar propagation with the auxiliary polarization properly relaxed

Freeze the metric and a; take a locally homogeneous scalar phi=omega t,
X=omega²/2. Define temporal and spatial quadratic coefficients by
L2=(Kt/2)delta_phi_dot²−(Ks/2)|grad delta_phi|² after eliminating delta_P.
Its Hessian has

    L_PP=−2M²−6Kc f P,
    L_dotphi,P=−3Kc f_X omega P².

The nonzero negative L_PP permits algebraic elimination. The Schur
complement gives

    Ks=Z−Kc f_X P³,
    Kt=Z−Kc P³(f_X+2X f_XX)
       +18Kc² X f_X² P⁴/(2M²+6Kc f P).

The last positive term is essential. Holding P fixed gives a different
temporal coefficient and can incorrectly reject branches. These coefficients
describe this restricted fixed-metric sector, not the full constrained gravity
or Horndeski characteristics. Negative Kt or Ks fails this sector's usual
positive-kinetic/gradient test; no blanket instability theorem for a completed
theory follows.

For f=(X/Xref)^n and z=3Kc f P/M²,

    Ks=Z−Kc n f P³/X,
    Kt=Z+(Kc f P³/X)[n(n+1)−3n²/(1+z)].

Consequences at fixed positive X:

* n>0 eventually gives negative Ks as P increases.
* −1<n<0 eventually gives negative Kt.
* n=−1 also eventually gives negative Kt: its correction is
  −3M²Kc f P³/[X(M²+3Kc f P)].
* n<−1 can have positive large-P coefficients but still fail at intermediate
  P. With X=Xref=M²=Kc=Z=1 and n=−2, Kt is approximately −0.0518261
  at P=6/5 and +3.2857143 at P=2. Large-field positivity alone is insufficient.
* n=0 gives Kt=Ks=Z, retaining an independent constant coefficient.

Arbitrarily large P is a formal sector limit, not proof of effective-theory
validity there. A bounded field range or additional operators may change these
conclusions. No proposed physical cutoff was established in this audit.

## Constant acceleration versus the checked rolling vacuum

The primary-source background already extracted in
SELF_TUNING_GALAXY_BRIDGE_RESULTS.md has
phi=c0+c1 exp(3H_c t). For c1 nonzero, X=X_initial exp(6H_c t).
Its derivative coefficient therefore evolves as f(X(t)).
If one additionally assumes a time-independent Newton conversion and the
bare dictionary a0bare=1/[12πG Kc f(X)], then

    d ln(a0bare)/dt=−6H_c X f_X/f.

For a power law it is −6n H_c. A constant curvature Lambda=3H_c² and
constant a0bare require f_X=0 along the entire sampled X interval. For a
power law this requires n=0. A function with a plateau could meet that
condition on the interval, but its plateau normalization is not selected.
An asymptotic plateau could make the ratio approach a constant, also without
fixing its value. Compensating Newton evolution, a different rolling vacuum,
or local scalar screening would require an independently derived dictionary
and dynamics; none is being ruled out or assumed here.

## Research consequence and verification

A concrete candidate shows what a constant derivative invariant can and
cannot accomplish. For a future timelike unit normal
u_mu=−∂mu phi/√(2X), define Theta=∇mu u^mu. On homogeneous expanding
de Sitter with phi_dot>0, u^mu=(1,0,0,0) and Theta=3H_c, independently
of the rolling amplitude. Consider the trial cubic coefficient

    Kc f = beta M²/Theta,  beta>0.

On its positive-Theta branch, the conditional bare acceleration dictionary
gives

    a0bare=2M²/(3Kc f)=2Theta/(3beta)=2H_c/beta,
    Lambda/a0bare²=3beta²/4.

This is a possible functional scale bridge, not a numerical breakthrough:
32π would require assigning beta²=128π/3. That assignment would fit the
target rather than derive it. The interaction is singular at Theta=0 and
depends on second scalar derivatives (or the preferred foliation expansion),
so its sourced constraints and extra-mode health have not been established.
It must not be treated as an innocuous replacement of f(X) in the propagation
formulas above, which were derived for f(X) only.

There is a structural reason vacuum tests cannot fix beta here. The added
operator is proportional to P³ and is C² at P=0. Provided Theta remains
nonzero and its coefficient is smooth near the vacuum, its action and first
two variations vanish on P=0. Its normalization therefore does not enter
that vacuum's background equations or quadratic action. This extends the
earlier Kc freedom to this derivative-invariant candidate. Nonlinear matching,
a microscopic coupling calculation or a global selection rule would have to
supply the missing coefficient; none has yet done so.

This bridge removes the simple additive-shift conflict but does not yet
produce a constant selected scale. The strongest remaining opportunity is a
shift-invariant derivative combination whose value is constant on a healthy
rolling vacuum, with its coupling fixed by an independent principle. The
choice of that combination and its normalization must come from an action,
not from inserting the desired H_c/a0 ratio. Full degeneracy, local source
matching and causal stability remain necessary.

Eight exact SymPy identities and four illustrative sign assertions pass in
derivative_bridge_audit_v3.py, with the contract and bounded-run provenance
in runs/derivative_bridge_audit_v3. The functional/late-time arguments above
are analytic conditional arguments, not inferred from finite samples.
Two failed execution attempts are preserved: v1 mistakenly used the SymPy
namespace for ArgumentParser; v2 chose a threshold value with Ks=0 for a
strictly negative sign test. v3 corrects the parser and tests P=2 instead.
Their pinned scripts and manifests were not rewritten. Exact 32π remains open.
