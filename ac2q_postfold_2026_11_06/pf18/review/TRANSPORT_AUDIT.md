# Independent audit: native cross-weight and conditional signed transport

**Verdict: the cross-weight, exact clock-chart source, and conditional
Osgood variation theorem pass. The native estimates do not establish
the Osgood hypothesis, and fixed-speed uniqueness does not establish
coupled uniqueness.** This yields a genuine conditional native estimate,
not an unconditional continuation theorem.

Independent delegated audit, 2026-11-06. Actual files read:

- `NATIVE_WEIGHT.md`, SHA256 `94caf75a056466935b110c1c1ee5cd47c737604a40d4df44ec34a128b2aa84e0`.
- `CONDITIONAL_TRANSPORT.md`, SHA256 `f2baa76b60a11d60b577fe356c7d012fc81d8ae60906bdbfc2838f757334755c`.
- `MODULUS_TEST.md`, SHA256 `8b26041dbafb16f6b16acac0e80e03df7aad3ed80f73048b6be1c0c7171ad29e`.
- `COUPLED_COMPARISON.md`, SHA256 `d261f35762833514699fda3dc37eed8edd3bdfd414f6dfff32b99f9e436bce4f`.

## 1. Opposite-family cancellation is real but incomplete

Set a_clock=e r/r and w_sigma=K+sigma a_clock/c. The covariant
W_sigma differs from w_sigma only by the bounded parameter derivative
sigma I_A eA. The exact leading equations give

    div D_sigma=K+sigma(r c_r-c)a_clock+bounded
               =A_q w_sigma+B_q w_-sigma+bounded,
    D_sigma r=-r c^2 w_-sigma+bounded,

where A_q=(1-c^2+r c c_r)/2 and B_q=(1+c^2-r c c_r)/2. Consequently

    rho_r/rho=B_q/(r c^2)

cancels the opposite-family term in div(rho D_sigma), leaving

    div(rho D_sigma)=rho A_q W_sigma+bounded.

The positive weight is uniformly regular on the compact state domain.
Its A derivative multiplies D_sigma A=r u+sigma c W_P/r, a bounded
quantity. The sign is the reciprocal of the earlier Riccati weight.
The actual file's formulas and their diffuse-measure interpretation pass.

The remaining coefficient A_q is positive in the genuinely nonlinear
packet neighborhood, but W_sigma is a signed derivative measure with
no asserted spatial sign or upper bound. Thus genuine nonlinearity is
not spatial monotonicity or a bounded-divergence estimate. This weight
cannot by itself provide the requested renormalization.

Equivalently, in normalized coordinate Riemann equations, a local
density can cancel the opposite-state derivative in the divergence of
its acoustic field. The self coefficient remains proportional to
partial_(z_sigma) lambda_sigma, which is nonzero. A nonlocal density
solving a full continuity equation would need a controlled flow or
Jacobian estimate; assuming it exists with positive bounded values
would insert the transport control being sought. This argument does
not exclude deriving such control by another native mechanism.

## 2. Exact native measure equation in a general clock chart

For tau=phi and regular periodic x write

    n=r partial_tau+nu partial_x,
    e=l^-1 partial_x,    dVol_2=(l/r)d tau dx.

No uniform-arclength gauge is needed. The normal flux of the covariant
gradient is the signed slice measure

    mu_sigma=D_x z_sigma+l omega(e)dx,
    lambda_sigma=nu/r+sigma c/(r l).

Multiplying the conservative gradient identity by the volume density
gives exactly

    partial_tau mu_sigma+partial_x(lambda_sigma mu_sigma)=q_sigma,
    q_sigma=D_x(F_sigma/r)+(l R_base/(2r))dx.

The spatial flux subtracted in the kinematic identity is F_sigma/r.
Thus the sign and the factor r in the source are fixed without any
assumption about characteristic regularity. Continuous slice BV r,F
give the equivalent expansion r^-1 D_x F-F r^-2 D_x r. PF17 therefore
supplies ||q_sigma||<=C(1+Z)^2, where Z=sum ||mu_sigma||, on slices
and intervals retaining that result's compact/regularity hypotheses.

## 3. Verified transport input and conditional conclusion

Checked [Ambrosio--Bernard, *Uniqueness of signed measures solving the
continuity equation for Osgood vector fields*](https://arxiv.org/pdf/0807.1592),
arXiv:0807.1592v1, July 10, 2008, conditions (O),(B) and Theorem 1,
PDF pages 2--3. In one dimension its two-sided condition is the stated
Osgood velocity modulus. It gives the pushforward formula for bounded-
mass signed solutions; continuous velocities give the corresponding
flow solution. No local full-text cache or source hash is claimed.

With q integrable in measure norm, the proposed Duhamel measure solves
the forced equation by testing along flow paths and Fubini. Subtracting
it leaves a bounded-mass homogeneous solution with zero initial trace,
so the verified theorem identifies it with the actual solution.
Pushforward decreases total variation. Thus

    ||mu_sigma(t)||<=||mu_sigma(0)||+integral_0^t ||q_sigma(s)||ds,
    Z(t)<=Z(0)+C integral_0^t(1+Z(s))^2 ds.

The scalar comparison formula in the candidate follows until its
denominator reaches zero. Bounded wave masses, integrable source norms,
and the Osgood modulus remain explicit hypotheses; they have not been
deduced from bare spacetime BV membership.

The circle adaptation used in the file is valid. A smooth annular
extension of the continuous tangent velocity has modulus bounded by
C(t)rho(C0 distance)+D(t)distance. Adding a linear modulus preserves
the Osgood property: if rho(s)<=s at arbitrarily small s, choose disjoint
intervals [s/2,s], each contributing a fixed positive amount to the
integral of 1/(rho+s); otherwise rho>s eventually and compare with
1/(2rho). Scaling the argument also preserves divergence. The flow
preserves the circle, so pushing a circle measure into this extension
and applying the Euclidean result recovers the intrinsic theorem.

This answers one part of the proposed route positively: a fixed-speed
uniqueness theorem can prove a one-solution native TV inequality with
that solution's own source held fixed. A native source-difference bound
is not needed for this conditional one-solution statement. It is needed,
or must be replaced by another coupled estimate, for uniqueness of
the nonlinear evolution.

## 4. The native constraint-compatible modulus test passes

The cusp profiles have uniformly small amplitude and total variation,
and the local periodic auxiliary construction gives uniformly Lipschitz
A_epsilon,P_epsilon independently of r_epsilon's slope. With E_beta=0
and constant nonzero B, setting
K=(T_nn/M-B^2)/(2B) satisfies Hamiltonian and momentum constraints.
The earlier initial metric construction realizes these expansions.
These are finite-regularity admissible slice data, not a promised
uniform-lifespan or postbreak approximation family.

At gamma=1/10,r=1,A=11/10, exact differentiation gives

    c^2=10/91, (c^2)_r=7911/8281,
    partial_r(c^2/r^2)=6091/8281>0.

At the initial theta=0 conformal slice, l=1 and nu=0, so the actual
clock-chart speed is sigma c/r. Its r derivative retains a positive
magnitude in a fixed small neighborhood. Uniform Lipschitz variation
of A contributes at most C s between 0 and s; the prescribed clock
cusp contributes at least k delta s^a in the limiting profile. Hence
any common modulus with a common finite coefficient would satisfy
rho(s)>=constant s^a near zero. For 0<a<1 this is incompatible with
the Osgood integral. All coefficients, signs and domain statements in
the actual modulus test pass.

This is a new native slice-level obstruction to deducing the modulus
from compact values, TV and the initial constraints. It does not rule
out a dynamical estimate with a time-integrable coefficient: an isolated
initial time and a degenerating family of individual Lipschitz constants
do not decide that question. The actual file makes this distinction.

## 5. Coupled comparison remains different

The subtraction in `COUPLED_COMPARISON.md` is exact:

    partial_t delta mu+partial_x(lambda1 delta mu)
       =delta q-partial_x[(lambda1-lambda2)mu2].

Although the product on the right is a finite measure, its derivative
need not be one. Its norm is not controlled by the mass of mu2, even
when mu2 has a density. The forced transport theorem therefore does
not supply a total-variation comparison of two native solutions.
Likewise separate estimates for q1 and q2 are not a difference estimate.
Comparing integrated states or a weaker measure metric is possible in
principle but requires another coupled proof.

All four actual files pass within their stated scope. No change to
their mathematical claims is required by this audit. The new result
is a precise conditional variation theorem plus a native constraint
test showing why its extra hypothesis is not already supplied. It
does not prove existence, uniqueness, Cantor exclusion, or a necessary
physical extension for the full weak system.
