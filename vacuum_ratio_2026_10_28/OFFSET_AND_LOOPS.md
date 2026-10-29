# VR28 continuation: what could protect the ratio?

These are two additional structural checks after the successful classical
calculation. They do not alter the frozen DERIVATION.md or its run inputs.

## 1. Internal symmetries cannot prohibit the constant term

Claim. Consider an action S[g,fields] with Einstein gravity and a positive
scalar kinetic term. Let the proposed protecting transformations act only on
matter/internal fields, leaving the metric, integration measure and domain
fixed. If S respects them, then so does

    S_C=S-C integral sqrt(-g) d^4x

for every constant C. The extra term has zero variation under every such
transformation. This proof also covers field-independent boundary variations
of the original action: the added term contributes no new internal variation.

For a minimally coupled scalar potential with U(0)=V>0, U_s(0)=0 and
U_ss(0)=9B>0, S_C retains the same stationary scalar and its positive mass
and kinetic coefficients. Its maximally symmetric vacuum instead has
H_C^2=(V+C)/(3M^2). For any sufficiently small C it is still de Sitter and
locally healthy in this vacuum sector, but

    d[B/(V+C)]/dC=-B/(V+C)^2 != 0.

Therefore an internal symmetry plus these vacuum equations/health conditions
cannot select the ratio to the *full* gravitating energy. The constant is
physically measurable through gravity; the argument changes the theory
within the allowed class, rather than treating it as a gauge shift.
Only an open interval of C is needed, with curvature below any EFT cutoff.
No arbitrary-large-curvature extrapolation is part of the argument.

This explains why the internal response A=U_s-3U is not automatically a
Noether or trace-anomaly Ward identity. The proposed equation A_s=-3delta A
excludes a constant term, whereas an internal transformation alone does not.
A genuine symmetry involving physical metric scaling, a specified global
constraint, or a microscopic vacuum-energy prescription could change the
hypotheses. None has been derived for this parent. Ordinary coordinate
diffeomorphism invariance permits a cosmological constant and is insufficient.

## 2. One-loop scalar fluctuations generate additional potential shapes

This is a deliberately stated additional hypothesis: take the vacuum scalar
sector to be a four-dimensional canonical relativistic real scalar
phi=F_s s with potential U_delta, and compute its local flat-space one-loop
potential. It is not an assertion that the original nonrelativistic stream
action has been covariantly quantized. No graviton, particle, or extra-field
loop has been included, and no cancellation by such sectors is ruled out.

For a constant background the quadratic fluctuation operator is
-partial^2+m^2(s), m^2(s)=U_ss/F_s^2>0. The Gaussian contribution is
one half of its log determinant. Differentiating with respect to m^2 gives
one half of integral d^d p/(2pi)^d [p^2+m^2]^(-1); dimensional continuation
therefore produces a local ultraviolet pole proportional to m^4(s).
This argument applies order by order in the local EFT expansion even though
an exponential potential is not a polynomial renormalizable theory.

In modified minimal subtraction the single-real-scalar finite term is

    Delta U=m^4/(64pi^2)[ln(m^2/mu_R^2)-3/2].                 (L1)

Its normalization agrees with the primary source in SOURCES.md. It is used
only where the one-loop expansion is small. It is not used to extrapolate
the potential or a halo into a loop-dominated regime.

For the two-exponential branch, define a=V_sector delta/(1+delta)>0. Then

    U=a exp(3s)+(a/delta)exp(-3delta s),
    m^2=(9a/F_s^2)[exp(3s)+delta exp(-3delta s)],
    m^4=(81a^2/F_s^4)[exp(6s)
            +2delta exp(3(1-delta)s)+delta^2 exp(-6delta s)]. (L2)

For every delta>0 the exp(6s) term has nonzero coefficient and cannot be
absorbed into {constant, exp(3s), exp(-3delta s)}. Even allowing changes of
delta and field normalization only adds polynomial factors multiplying the
old exponents at first order; it does not create exp(6s). A nonlinear field
redefinition can move terms into the kinetic/matter couplings, but would
not preserve the stated canonical kinetic term and Z=exp(2s) construction.
The bare two-exponential scalar family is thus not closed under this
one-loop vacuum-sector calculation. The special delta=1 makes the cross
term constant but leaves both doubled exponents.

Equivalently, acting on a mode exp(lambda s) with

    L_delta=(partial_s+3delta)(partial_s-3)

multiplies it by (lambda+3delta)(lambda-3). The generated lambda=6 mode has
factor 9(2+delta)>0. It breaks the differential condition that selected the
two-exponential shape. Changing the subtraction scale moves this local
term between the explicit loop and counterterm coefficients; it does not
provide a physical reason for the total breaking term to vanish.

Hence choosing delta to look like a loop factor is not a derivation. One
must specify a particle spectrum, interactions, symmetry and matching
condition that actually calculate it and protect the relevant functional
relation. Additional fields might cancel the offending contributions;
that is an untested new model, not a consequence of this calculation.

## 3. Precise surviving microscopic target

If the conditional vacuum-medium dictionary is adopted, define the
equilibrium-family energy V_eq(q)=epsilon(q)-q epsilon_q(q). Unlike the
fixed-mu scalar potential, this compares equilibria with different chemical
potentials mu=epsilon_q(q). Direct differentiation gives

    -dV_eq/dln q=q^2 epsilon_qq=B(q),
    B(q)/V_eq(q)=-dln V_eq/dln q             when V_eq>0.      (L3)

For the scaling branch, V_eq=V_sector(q/q0)^(-delta), so the response ratio
is delta. For PN28, V_eq=V-B ln(q/q0), with constant B. A microscopic
calculation of this response and the full energy offset would address the
actual missing input. Defining the response, selecting a subtraction, or
fitting delta does not do so.

The classical and one-loop checks leave that physical route open. They
establish why the current minimal candidate and the tested symmetry shortcut
cannot yet deliver the requested predicted number.
