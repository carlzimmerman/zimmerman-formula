# Independent algebra and scope review

2026-10-20. Root review of the three separately derived analytic packets.
This is a correctness audit, not a formal proof or microscopic health
certificate. Each author also cross-reviews the other packets in
REVIEW_PHASE.md, REVIEW_WEYL.md and REVIEW_CLOCK.md. No target was used
as a premise and no parameter scan was run.

## Gravitational phase: independent checks

Starting from y=1+chi^2 and x=h/(3a0), I reproduced

    1/y+x^2 y-2x=(xy-1)^2/y.

This proves the stated global broken minimum. At x>=1 the excess over
y=1 is (y-1)(x^2-1/y)>=0. Differentiating the reduced functional gives
the reported mu(h), including its quartic correction. Varying -E-rho Phi
gives div[(E_h/h)grad Phi]=rho; hence positive mass is attractive and
G=1/(8pi M^2), with no separate scalar charge. This differs physically
from the earlier repulsive electric construction.

At the minimum V_yy=2M^2 h^2/y^3 and (dy/dchi)^2=4chi^2 give
m_chi^2=8M^2 h^4[1-h/(3a0)]/(9Z^2 a0^2). Direct differentiation of
chi_*(h) reproduces the gradient cost and the point-source coefficient
9/16. The finite-Z algebraic limit therefore cannot be uniform at large
radius. A regular positive chi mass leads to the stated quadratic
inequality for the finite symmetry-breaking interval and restores IR
quadratic response.

For the bounded A deformation, y=s/h gives the leading functional
M^2/s+M^2s/(9a0^2)+A/s^3. Multiplying its derivative by s^4 gives

    M^2 s^4/(9a0^2)-M^2 s^2-3A=0.

Its unique positive solution for s^2 agrees with the packet. The second
derivative is positive, and the envelope derivative is 1/s_A^3>0.
The deformation vanishes to sixth order at chi=0, so its complete first
and second variations vanish there, not just its chi mass variation.
This is a concrete local EFT nonselection witness. It is not promoted
to a family of healthy, same-state covariant MOND halos.

I separately differentiated the normal-fluid density and obtained the
packet's Euler current from S_n=-(2M^2/3)int sqrt(-g)n_f Box F.
At chi=0, F=1 and delta F=0, so the displayed truncation has no bulk
normal-fluid quadratic kinetic term. That statement alone does not
identify a propagating ghost. For its flat-rest diagnostic, setting
z=h/(3a0), the exact algebraic Gauss relation gives
z=b_r/r+b_r^2/(3r^2)+O(r^-3), hence
F=2b_r/r-b_r^2/(3r^2)+O(r^-3). Its Laplacian is nonconstant at the
next order. The actual covariant normal-fluid/metric solution must be
found rather than assumed. This calculation is explicitly not a full
retained-Z solution or a global no-go.

The source card's constant-Y de Sitter curvature calculation is accepted
only as a fixed-background diagnostic. Finite-density charge conservation
does not generally permit that state. No additive sqrt(6)H halo-window
bound has been established. The source's higher-time-derivative/cutoff
argument is not a microscopic completion.

## Weyl scalar: independent checks

The invariant b=dtheta-dlog(phi/phi0)=d sigma survives Einstein gauge.
For a consistently varied auxiliary unit vector, ell=M^2(Box sigma+X)
cancels the metric normalization stress. Combining that operator with
R_W=R-6Box sigma-6X gives precisely -(alpha+4)M^2 X/2. The scalar
principal coefficients then follow by twice differentiating X^(3/2).
Their finite-gradient positivity does not remove the vanishing vacuum
rank at alpha=-4.

The point action -yint phi ds_g=-yphi0int ds_ghat and the metric/scalar
chain rule independently establish zero direct sigma charge for literal
S_m[ghat]. A pre-gauge matter trace cannot be retained without its
compensator variation; the original scalar equation also combines with
the metric trace under the invertible change of variables. The external
vector recipe is a different closure, whose stress/source cannot be
silently imported. The criticism is correctly restricted to that missing
off-shell implication.

Granting the stated phenomenological source map gives
xi=32pi/(lambda beta^2), as reported. The transformation
phi->sphi, xi_W->xi_W/s, beta->s^2 beta, lambda->lambda/s^4 preserves
M,C3,V0 and lambda beta^2. The unfixed ratio is therefore physical, not
a Planck or compensator naming convention. The changed q matter action
has a different unscreened UV Newton coefficient; its q-dependent formula
cannot be used as a derivation of the original source map.

## Curved clock: independent raw-action reduction

For a longitudinal unit vector aligned with the ADM normal,
nabla u.nabla u=K_ij K^ij-a_i a^i. I independently reduced EH+c1 to

    (A K_ij K^ij-B K^2+B R3+M a_i a^i)/2,
    A=B-M, S_c=2B+M.

Expanding K_ij gives the raw bracket -3S_c U^2+2S_c U b-Mb^2.
The intrinsic curvature and acceleration give
X(2Bzeta^2+4Bnzeta+Mn^2). The background constraint cancels the
remaining nondifferentiated terms after the displayed background boundary.
Thus the packet did not merely assume a flat aether dispersion relation.

Eliminating b gives C U^2, C=2AS_c/M. Lapse variation then yields
n=(CHzetadot-2BXzeta)/(CH^2+MX). With D=CH^2+MX, the remaining mixed
bracket coefficient is 4CBHX/D. Writing it as 2Jzeta zetadot, where
J=2CBHX/D, the temporal boundary changes the bracket potential by
-(Jdot+3HJ). Using Xdot=-2HX reproduces exactly

    K_z=CMX/D,
    V_z=2BX^2[M(2B-M)X+CS_cH^2]/D^2.

Both are positive at finite k and 0<M<B. I also reproduced
3H+Kdot/K=H+2MHX/D. The positive derivative of
X(aX+b)/(c+dX) verifies decreasing Omega_z^2 during expansion.
The limiting first-order matrix has eigenvalues 0,-H and integrable
coefficient errors, which justifies future boundedness at fixed k.
This does not prove a uniform high-k or nonlinear bound.

The transverse shift square gives s=-MV/A and the stated positive
c_V^2. Rewriting with U=aV leaves exactly the quoted temporal boundary
and a conformal oscillator. The homogeneous Killing generator has zero
metric Lie derivative and produces the acceleration-free a^-1 tilt;
the a^-2 mode has nonzero invariant acceleration. Neither the finite-k
inverse nor the k=0 gauge interpretation is transferred across that
constraint-rank change.

For finite h, differentiating the Bianchi minisuperspace action gives
the four stated background equations. E>=V0 implies H>=H0 on the expanding
root, and the shear integral gives v<=0 before any H_perp bound is used.
Therefore h<=h_i exp(-H0t), making the explicit smallness argument
noncircular. The quoted condition implies H_perp>3H0/4 and
m_t^2<H0^2/8, hence mu_theta^2>H0^2. The coefficient errors decay
integrably towards limiting roots -H0,-2H0. I confirm the controlled
homogeneous decay. This is a genuine repair of the broad flat-tilt
inference, with no implication for the uncomputed finite-k finite-h halo.

## Disposition and formal scope

The accepted new conclusions are universal attractive metric response in
the stated local window, an explicit allowed cubic deformation, a precise
variational source obligation, and a constrained curved-clock health
improvement. No selecting equation for R, healthy microscopic completion
or independent second prediction is obtained. The original goal remains
open. The nine inherited Lean modules and their genuine false controls
passed their five evidence validators freshly; new calculations above are
analytic and have not been claimed as kernel checked. The actual-pi
adapter remains unverified under the resource limit.
