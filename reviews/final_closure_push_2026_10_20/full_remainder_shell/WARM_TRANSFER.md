# Exact radial warmth for the full saturating interaction

20 October 2026. New analytic continuation FCP-FULL-R-WARM. This is an
existence result for the separately specified spherical, zero-stiffness,
two-species reciprocal energy. It does not establish warm stability,
selection by formation, a microscopic medium or the full physical theory.

## Exact target

Fix a positive central point baryon mass B=M_b, G>0 and a0>0. The point
source is fixed and its own constant self-energy is excluded. Put

    R(u)=u^2/(a0-u),
    C_b(r)=M_b/2 [sqrt(1+4 a0 r^2/(G M_b))-1].

Choose 0<r0<r1<r2<Rout and 0<f<=(3-sqrt(5))/2, for example f=1/64.
Use the same reciprocal energy as `../reciprocity/SOURCE_RESPONSE.md`, with
T=f M and F=(1-f)M. On [r1,r2] require **total** cold mass M=C_b. Do not
identify T alone with C_b or add the free mass to the target a second time.

Let S(z)=chi(z)/(chi(z)+chi(1-z)), chi(z)=exp(-1/z) for z>0 and zero
otherwise. Set M=0 for r<=r0, and on r0<r<r1 set

    M(r)=C_b(r) S((r-r0)/(r1-r0)).

Continue M=C_b through [r1,r2]. For r2<r<Rout set

    M(r)=C_b(r2)+integral_r2^r C_b'(s)
                  [1-S((s-r2)/(Rout-r2))] ds,

and hold M constant after Rout. This is C-infinity, has M'>0 on its hollow
interior, finite mass, M<=C_b everywhere, and exact target mass on the law
annulus. The density tapers have the same quantitative flatness as the
pinned smooth-inverse construction below.

Claim: for each sufficiently small fixed delta>0, there exist bounded
nonnegative C-infinity invariant distributions f_i(E_i,L), with f_i,E<0
where physically occupied, whose exact shell densities are f M' and
(1-f)M'. Both have strictly positive radial dispersion on the closed law
annulus, compact phase-space support in the closed shell [r0,Rout],
a fixed positive angular-momentum interval and a fixed negative energy cap.
Positive-density points lie in r0<r<Rout; the support closure touches both
flat zero-density edges. Their summed
mass, potentials and tracer galaxy law are exactly the selected ones.
The width, profile and population fraction are chosen inputs.

## General hypotheses actually used by the density inverse

The raw prior construction is
`real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`
(all sections, read for this transfer). Its opening chooses a deep-cubic
model, but its density inversion after that uses only these properties of
each **fixed** potential Phi_i and target shell density mu_i:

1. L_c(r)=r^3 Phi_i'(r) is globally strictly increasing from zero to infinity;
   on [r0,Rout] it has positive lower derivative and bounded smooth
   derivatives. Its circular energy E_c=Phi_i+L_c/(2r^2) has a fixed negative
   upper bound there. Additive constants are chosen at infinity.
2. The interior density is positive and smooth, with inner behavior
   d^(-2)exp(-D_inner/d) and outer behavior exp(-D_outer/d), multiplied by
   positive smooth factors. It is flat at both edges.
3. For h(r)=(r-r0)^2(Rout-r)^2/(Rout-r0)^3, the intrinsic coordinate
   dr/dx=h(r) has bounded logarithmic derivatives of mu and of h. Powers of
   inverse edge distance or h are dominated by the target's flatness.

No cubic force coefficient, special M=A r identity, or cold self-energy
sign is used in the subsequent density operator, Fourier inverse, positivity
or endpoint argument. This is a check of the actual proof's hypotheses;
it does not import that paper's separate deep-cubic stability assertion.

For completeness, in those variables s=L_c^(-1)(L), y=x(s), omega^2=L_c'/s^3,
sigma=omega^2 h^2 and t=(E-E_c)/sigma, its distribution is

    f_i(E,L)=H_i(t,y)/(4 pi^2 L_c'(s) omega(s) h(s)^2 Z).

The exact change of variables gives the shell-density operator

    A H(x)=Z^(-1) integral H(w^2/2+W(x,y),y) dw dy,

where W is the actual orbital energy difference divided by sigma. Taylor
expansion gives W=(x-y)^2/2+O((x-y)^3), uniformly with all intrinsic
derivatives. Monotonic L_c excludes remote pieces of a sufficiently narrow
energy tube. The frequency-dependent widths

    b_n=delta^2/[4+(delta k_n/zeta)^2]

give a local right inverse R_delta with
`A R_delta=I+E_delta`, operator norm `O(delta)` on each weighted X_s, and
one derivative of smoothing. Inverting at X_5 and bootstrapping supplies a
smooth correction. Applied to the positive broad baseline
`H_0=mu(y) delta^(-2) psi(t/delta^2)`, this correction has relative height
and first-t-derivative errors O(delta), and is confined to t<delta^2/4.
Thus the total remains positive and strictly energy-decreasing. The
unmodified outer portion of the tube gives positive radial dispersion.
The pinned raw proof supplies the estimates and exact constants/conventions;
this paragraph records which parts are being transferred.

## Verification for the full-remainder candidate

The circular-shell derivation in this work package gives

    kappa_t,bg^2=kappa_t,coherent^2
         +G M'/r^2 [(1-f)-f R'(f G M/r^2)],
    kappa_f,bg^2=G(B+M)/r^3+G(B'+M')/r^2.

Here bg means the actual fixed-field orbit frequency, rather than the
coherent displacement frequency. Since M<=C_b, u_t=f G M/r^2<=f a0 and

    (1-f)-f R'(u_t) >= (1-3f+f^2)/(1-f)^2 >= 0.

The coherent term contains the strictly positive baryon contribution and
`[2uR'(u)-3R(u)]/r=u^2(a0+u)/[r(a0-u)^2]>=0`. Hence L_c'=r^3 kappa_bg^2>0
globally. For r<r0 the force is the point baryon's Kepler force; for
r>Rout the finite exterior masses give L_c tending to infinity. The
uniform saturation gap u_t<=f a0<a0 ensures smooth bounded force
derivatives on the closed target range. These facts verify property 1's
orbital geometry, including actual single-orbit rather than merely coherent
stability.

Also R(fu)<=f^2 R(u)<=f^2 g_b. Integrating the inward tethered force and
using nondecreasing B,F proves

    E_c,t(r)<=-G[(1/2-f^2)B+F(r)/2]/r,
    E_c,f(r)<=-G[B+M(r)]/(2r).

Our fraction bound is smaller than 1/sqrt(2). Both therefore have a fixed
negative cap on [r0,Rout], independent of the later small width delta.
The exterior force is integrable, so the chosen potential constants exist.

Finally, C_b and C_b' are positive and smooth on this closed positive-radius
range. The explicit inner/outer tapers have exactly the two edge forms in
property 2, with D_inner=r1-r0 and D_outer=Rout-r2. Differentiation in the
intrinsic coordinate verifies property 3 just as in the raw proof: h is
proportional to d^2 at an edge and log(mu)=-D/d plus a logarithmic term and
a smooth remainder. Thus all three hypothesis groups hold.

Apply the verified density inverse separately to the two fixed potentials.
The resulting distributions reproduce mu_t=f M' and mu_f=(1-f)M' exactly,
so neither potential changes when they are installed. This is the required
self-consistency, rather than a tracer approximation. Their common compact
law annulus has the actual simple-law tracer acceleration

    g=G(B+M)/r^2,    G B/r^2=g^2/(g+a0).

The inversion supplies radial dispersion comparable to
`delta^2 omega_i(r)^2 h(r)^2`. It is positive on [r1,r2], tends smoothly to
zero at both boundaries, and requires no wall or extra exterior population.
The widths can be fixed small enough to keep both energy caps below half
the circular reserve.

## What is and is not closed

This transfer removes a specific restriction of the existing exact warm
existence construction: its full-interaction version need not replace the
canonical remainder by a deep-cubic approximation. It also replaces the
formal infinite-mass warm comparison with one finite-stock spherical
existence family, for the **total** law profile and a chosen partition.

The density inverse is a stationary construction. Its proof does not select
the population fraction or temperature, derive capture, establish warm
linear/nonlinear or nonspherical stability, prove actual-path all-time
confinement, include finite stiffness, or derive the metric and abundance.
The separate circular-shell positive energy must not be used as a stability
certificate for these smooth distributions. None of the frozen empirical
scores has been recomputed for this new candidate.

Review: coordinator proof transfer after reading the complete pinned raw
inverse, followed by the separately recorded audit. This is an internal
analytic result conditional on that inherited inverse's estimates; it is
not a formal certificate or external peer review. Exact hashes and the
auditor's restriction/acceptance belong in the checkpoint before any
stronger statement is used.
