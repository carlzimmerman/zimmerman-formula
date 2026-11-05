# NO VERDICT — no complete covariant source for FN6's window established

A native power-law stiffness screen exposes an asymptotic obstruction and
an operator mismatch. It supplies no new mechanism eligible for the five
observational gates. T0-T4 and Q2 for a new mechanism are NOT EVALUABLE;
its full tensor-speed test remains UNDECIDED. No Gaussian-engine result
is promoted to a v3s mechanism result. Kappa=1/2 FITTED; not theory closed.

Criteria0254ee485c were committed first. Main28/28; MUTATE24/28, with
the intended radial derivative and quadratic known-answer failures on
both footings. Runs take less than0.4seconds. This is a derivation screen,
not a completed nonlinear field solution or a successful action candidate.

## Native constitutive family

Keep v3s's polarization potential and replace its switched stiffness by
Fbar(d)=lambda*d^q/q for d>0, zero for d<=0, where p=K P and d=D.p.
The scalar d is defined using the existing clock's projected derivative;
this is a covariant constitutive replacement with that foliation retained.
Positive lambda and q>1 give convexity for d>0 and Fbar=Fbar'=0 at zero.
The q=2 member has lambda=Lstar²/2. These choices are assumptions, not
derived constants or a new adoption.

Varying the radial density -r²Fbar(p'+2p/r) gives +d_r Fbar'(d) in
the P equation. In the static spherical zero-charge, mu_K=0 reduction,
Poisson gives g=g_b+p, hence

    g_b = p²/(a-p) - d_r Fbar'(d), d=p'+2p/r.

On the unscreened deep-MOND asymptote p=a*rM/r, rM=sqrt(GM/a), the
stiffness-to-source ratio is

    R=2 lambda(q-1) a^(q-2) rM^(q-3) r^(3-2q).

Defining a diagnostic crossover by R=1 gives mass exponent

    p_mass=(q-3)/(4q-6).

For an inward-growing correction q>3/2; then
p_mass=1/4-3/[4(2q-3)]<1/4. At q=3/2 the ratio is independent of radius
and defines no radial crossover. The formal powers needed for FN6's
target exponents are:

| target p_mass | required q |
|---|---|
|0.30|-6|
|1/3|-3|
|0.40|-1|
|0.45|-3/8|

Even choosing negative lambda to keep Fbar'' positive for these negative
powers makes Fbar diverge to positive infinity and Fbar' to negative
infinity as d approaches zero. They cannot furnish the stated regular
FRW endpoint. This rejects those exact power-law asymptotic constructions.

## Domain matters

For q=2 the ratio is Lstar²/(rM*r). Its equality radius is Lstar²/rM.
The record also uses a core scale Lstar²/(2rM); this factor is not silently
equated across definitions. More importantly, the above estimate requires
the crossover to lie in the deep-MOND regime. In the high-field asymptote
p~a,d~2a/r instead,

    R=lambda(q-1)2^(q-1)a^(q-2)r^(2-q)/rM².

There is no justification for extrapolating the deep-MOND exponent into
that regime. Finite-radius transitions, non-power constitutive functions
and additional fields are not excluded here. A full radial boundary-value
solution is still needed before claiming a physical screening radius.

There is a further environment qualification in D10's existing own-equation
result: its embedded linear response screens at a scale proportional to
Lstar, rather than the isolated core scale Lstar²/(2rM). Thus the isolated
exponent alone does not determine hosted-dwarf observables. No D10 or
FN6 observational result is rerun or altered by this screen.

## Why FN6's engines cannot directly grade this family

Freeze an isotropic longitudinal background with Wbar_pp=M>1 and
Fbar''=gamma_eff. Linearizing the Poisson and P equations gives

    delta g/delta g_b = 1+1/(M-1+gamma_eff*k²).

FN6's reciprocal Gaussian has the corresponding form
1+C exp(-L²k²). Matching zero wavenumber and the k² coefficient fixes
C=1/(M-1), L²=gamma_eff/(M-1). The remaining k^4 coefficient differs by

    gamma_eff²/[2(M-1)³].

It is nonzero for positive stiffness. Two Gaussian filters in the
reciprocal model produce the exponential; a local constitutive gradient
term produces this rational response. Changing q changes the tangent
coefficient, not this operator identity. This is a failure of exact
operator transfer, not an observational exclusion of either operator.
Matching a mass exponent and assigning that length to FN6 does not fix it.

## Controls and numerical verification

Symbolic checks cover the radial variation, W conjugate, Poisson
elimination, both radial asymptotes, exponent and singular endpoints,
plus the transfer coefficients. Independent40/80-digit differentiation
on q=2,3,4 and r/rM=10,100,1000 agrees with the native ratio on each
footing; normalized pair discrepancy is0 at the printed precision.
The transfer pair differs by at most1.88869e-40, below1e-30. These are
coefficient fixtures with a dimensionless normalization, not fitted
screening lengths. No PDE convergence is claimed.

MUTATE drops one radial inverse power in the derivative. It fails the
symbolic radial ratio, the q=2 known answer and numerical derivative
identity for both footings. Its precision checks still pass: precision
alone does not validate a wrong equation. Separate outputs retain every
check and its value.

The first attempt asked SymPy, with q assumed positive, for a negative
formal root. It stopped before writing results. The script and sanitized
traceback remain in assumption_failure/. The explicit unrestricted
algebraic root was then substituted and checked exactly. Criteria and
tolerances did not change.

Run from the repository root:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ41_native_screening/run.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ41_native_screening/run.py --mutate

Expected exits0 and1; main/ and mutate/ contain independent JSON outputs.

## Remaining mechanism work

A surviving constitutive proposal needs a regular switch endpoint and
own-equation background solutions, including the external field. Its
response must then replace the Gaussian force operator inside the FN6
observable calculations: axisymmetric MW forces, dwarf equilibrium,
SPARC accelerations, external-field Solar quadrupole and planet response.
Those new solves, their convergence pairs and the new tensor principal
symbol have not been obtained here. No C6P Q2 margin is inherited.
Lane7's requested complete mechanism remains unresolved, rather than
being replaced by a Gaussian fit or declared impossible in every class.
