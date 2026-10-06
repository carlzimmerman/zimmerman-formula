# Norm-cube force and the regularity of the cosine correction

The inherited norm cube supplies a nonpolynomial second-order relative-lapse force. The added shear operator gives an invertible finite-mode relative system, but does not automatically smooth its high Fourier modes. For a cosine decaying seed and zero second-order propagating initial data, the resulting formal correction has a physical metric cusp. This is a chosen-data regularity obstruction, not a theorem excluding all seeds, weak solutions or the shear-repaired action.

## Action variation before reduction

Use n=3, chi=1, geometric a0>0, K>0, coincident de Sitter with scale a, and the actual projected action with

M_eff(I)=−A_offset+I/2−I^(3/2)/12+O(I²).

For a pure relative first-order lapse r=nu, I=|grad nu|²/(a² a0²) to leading order and geometric-mean volume is a³. Therefore the cubic action, before any metric constraints are substituted, is

S3=−K/(6a0) integral dt d³x |grad nu|³.

The scale-factor cancellation is exact at this order. Its relative-lapse Euler source is

Jnu=K/(2a0) div(|grad nu| grad nu).

This is the variation with respect to the relative logarithmic lapse. It is not the source for each individual lapse without the corresponding split factors. Smooth exchange-even Einstein, vacuum and shear actions have no cubic term along a purely relative first-order configuration. Their second-order relative forcing therefore cancels between sectors. The norm cube is exchange even but is not a cubic polynomial: its derivative is odd and survives directionally. Spatial-metric variation of this cubic term starts at third order. Thus the displayed relative source is the relevant new second-order force in this restricted pure-relative seed calculation. Mean quadratic sources are a separate calculation, not duplicated here.

The expansion is directional for epsilon>0: an epsilon v seed produces epsilon|epsilon| v|v| in the force. A two-sided analytic amplitude expansion or C3 action cannot be assumed. The action is C2 in gradient jets; the force need not be spatially C1.

## Actual node and Fourier structure

For nu=v(t) cos(kx),

Jnu=−K k³ v|v|/a0 |sin(kx)| cos(kx).

It vanishes at all x=m pi/k (gradient nodes) and x=(m+1/2)pi/k. The latter zeros are smooth. At a gradient node its leading behavior is a nonzero multiple of |x−x_node|, with opposite one-sided slopes; hence the force is continuous Lipschitz, not C1, unless v=0.

The exact Fourier series is

|sin X| cos X = sum_(positive odd j) 4/[pi(4−j²)] cos(jX).

To derive it, integrate on 0<X<pi, where |sin X|=sin X, and use sin X cos X=sin(2X)/2. The coefficient is (2/pi) integral_0^pi sin X cos X cos(jX)dX. Even j vanish; odd j give the expression above. This is an infinite series with coefficients O(j^-2), not a finite second harmonic. Its zero mean does not remove the nonzero harmonics.

## Actual finite-mode constrained inversion

Use the new shear action with fixed 0<eta<1. Write c=K a³, P_j=(jk)²/a², and A_s=−3(1−eta)/eta<0; A_s is not the vacuum offset. The inherited full relative quadratic action after the actual shift and retained shear constraints is

L/c=−A_s(zdot−Hnu)²+P_j(nu+z)²+(J_j/c)nu.

The shift gives t=−3(zdot−Hnu)/eta and the retained volume row gives D=0. The relative lapse is

nu=[A_s H zdot+P_j z+J_j/(2c)]/[A_s H²−P_j].

The denominator never vanishes. Eliminating it gives Kr=A_s P_j/(A_s H²−P_j)>0 and a forced curvature row

d_t[2c Kr(zdot+Hz)]−2c Kr H(zdot+Hz)
 =J_j P_j/(A_s H²−P_j)−d_t[J_j A_s H/(A_s H²−P_j)].

This is the actual constrained scalar equation, not an isolated elliptic lapse inversion. The finite-mode initial-value problem is regular on every compact finite time interval. It does not by itself certify convergence in a classical metric space.

## Controlled high-mode correction

Normalize a(t0)=1, select nu1=v0 a^-1 cos(kx), v0 nonzero, and impose z2_j(t0)=zdot2_j(t0)=0. The second-order lapse is then constraint-selected and is not set independently to zero. Odd modes have

J_j=−4K k³ v0|v0|/[pi a0(4−j²)] a^-2.

On a compact interval 0<a_min<=a<=a_max<infinity, define delta=j^-2. All coefficients of the constrained ODE are analytic near delta=0, uniformly in time, and J_j=delta J_infinity a^-2+O(delta²), J_infinity=4K k³v0|v0|/(pi a0). The limiting kinetic coefficient is −A_s, an order-zero spatial symbol; the force factor tends to −1. Ordinary finite-interval variation of constants, or differentiating its integral equation with respect to delta and bounding the remainder, therefore gives uniformly

z2_j=Z(t)/j²+O(j^-4),

including the finite number of time derivatives used here. The limiting equation and zero data are

Zddot+3H Zdot+2H²Z=C a^-5,
C=J_infinity/(2K A_s)=2k³v0|v0|/(pi a0 A_s),

Z=C/(12H²)[a^-5+3a^-1−4a^-2].

The bracket equals (a−1)²(3a²+2a+1)/a^5, so Z is nonzero away from the initial slice. This is a uniform fixed-time asymptotic, not a large-time/high-mode interchange.

The periodic function sum_(positive odd j) cos(jX)/j² equals pi²/8−pi|X|/4 for |X|<=pi. Hence z2 has a Lipschitz cusp plus a C2 remainder: the O(j^-4) remainder and its first two spatial derivatives converge absolutely. For these selected data it is not C1 at the nodes for t!=t0.

This cusp is not removed by relative scalar shear. In the report's scalar conventions B=beta+edot/P=t/P=−3(zdot−Hnu)/(eta P). It is O(j^-4). The separate-metric Bardeen relative curvature is Phi_rel=−z−HB, so its leading cusp is −z. The lapse constraint similarly gives nu2=−z2+O(j^-4), and Psi_rel=nu+Bdot retains the cusp. These are separately defined gauge-invariant combinations, not an attempt to put both metrics in Newtonian gauge simultaneously.

Consequently this natural cosine second-order initial preparation does not yield C2 classical metric perturbations on a later open interval, even though every finite Fourier ODE is invertible. A finite cutoff or a weak solution class is a different question. Canonical positivity does not supply missing spatial regularity.

## What remains open

Different second-order propagating initial data and full nonlinear solution spaces are not classified here. Flattened gradient nodes can improve the force regularity; the root is pursuing that changed seed separately. Neither the cosine cusp nor its signed linear dust-like mode proves a positive homogeneous cold abundance. This report does not establish the full sourced mean/clock/tensor system, nonlinear health, matter-era transfer or coefficient selection.

Exact checks validate action normalization, force sign, node/Fourier benchmarks, constrained high-mode limits and the temporal response. The uniform Fourier remainder argument and explicit nonsmooth series are the proof for the stated chosen-data regularity claim; finite check counts are corroboration. Controls halve Fourier normalization, falsely label the node force C1, or assume high-mode kinetic inversion gains spatial smoothing. Scientific inputs and standard bounded manifests are frozen separately from run summaries.
