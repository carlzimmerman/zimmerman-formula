# SV4 iter_2: thick-disc projection and non-circular motions at low inclination (FROZEN)

Shared rules: ../FROZEN_CRITERIA.md. Committed before any script or number.

## (a) Thickness in the inclination (AGC 114905)

The optical inclination i0 = 31 +- 2 deg comes from the stellar isophote axis ratio. A disc of intrinsic axis ratio
q0 has cos^2 i = (q^2 - q0^2)/(1 - q0^2). The record does not say whether i0 was derived thin or thick, so both
directions are graded:
- a+ (i0 read as thin, true i larger): q = cos i0, i = arccos sqrt((q^2 - q0^2)/(1 - q0^2)).
- a- (i0 already thickness-corrected, true thin value smaller): q = sqrt(cos^2 i0 (1 - q0^2) + q0^2), i = arccos q.
- q0 corners: 0.10 (published stellar z_d / R_e: UD1's zd_star() = 0.27 kpc over R_e 2.80 kpc, rounded), 0.13
  (published gas z_d 1.3 kpc over the outer ring 9.9 kpc), and GENEROUS 0.30.
- Applied to the published V_circ as in UD1's frozen scan: V and E x sin(i0)/sin(i), baryons fixed. Also graded at
  i0 - 2 sigma_i = 27 deg combined with a- (the most favourable in-errors corner).

## (b) Line-of-sight integration through the thick layer, on the action's own field

The authors' 3D model is a thick layer rotating on cylinders. In the action's exact field the circular speed falls
with height, so the density-weighted line-of-sight speed is below the midplane V_c. Frozen form, per ring R_k, on
the major axis (sky point x0 = R_k, LOS direction n = (0, -sin i, cos i) in disc coordinates, s along the LOS):

    C_k = Int rho(R,Z) V(R,Z) x0/R ds / Int rho(R,Z) V(R,0) x0/R ds,   R = sqrt(x0^2 + s^2 sin^2 i), Z = s cos i

with V(R,Z)^2 = R dPhi/dR at fixed Z from the exact AQUAL solution (gradients on the solver grid, bilinear in
(ln r, theta)), rho the gas density used by the solver, i = i0. Corrected data: V_rot,mid = V_rot / C_k, then
V_c^2 = V_rot,mid^2 + AD2_pub, E as iter_1. Corners: published h (AGC 1.3 kpc Gaussian; Malin 1 the QX4 disc,
h = 1 kpc), and GENEROUS h x 2. Malin 1 is graded the same way at i0 = 38 deg on V_c directly (V_c / C_k), on the
QX4 A2 density (QX4's A1/A2 rule: A1 reported beside at the published h).

## (c) Non-circular (bisymmetric / radial) flows

The bias they put on V_rot depends on a harmonic decomposition of the velocity field (residual amplitudes), which
is not on disk for either galaxy. Label: NOT EVALUABLE (NEEDS_OWNER.md). Reported: the line-of-sight amplitude
each ring would need, v_nc,k = (sqrt(V_model^2 - AD2_pub) - V_rot) sin i0, against sigma_HI(R_k).

## (d) All at once (AGC 114905), declared row

iter_1 C1 + (a-) at q0 0.13 and i 27 deg + (b) at the published h, applied together in that order. Labelled per the
shared rule (in errors).

MUTATE: (b) with the wrong sign (V_rot x C_k instead of / C_k) and (a) a+ must both give chi2 above the uncorrected
exact-field chi2 on both footings (a+ is wrong-direction by construction).
