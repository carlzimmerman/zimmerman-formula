# SV4 iter_1: pressure support (asymmetric drift) in the thick, low-mass gas disc (FROZEN)

Shared rules: ../FROZEN_CRITERIA.md. Committed before any script or number.

## AGC 114905

Published inputs (Mancera Pina+2024, arXiv:2404.06537, as already read by UD1; all from the authors' vector figure
inputs/plot_kinematics.pdf, right panel, read with UD1's own marker and error-bar functions):
- V_rot(R_k) with errors (red markers), V_circ(R_k) with errors (grey), sigma_HI(R_k) with errors (blue), 5 rings.
- Gas surface density: UD1's published functional form sig_gas (Sigma0 3.953 Msun/pc^2, R1 0.676", R2 375.220",
  alpha 559.231); gas vertical profile Gaussian with constant z_d = 1.3 kpc (the authors' value, UD1 A1).
- The published V_circ already contains the authors' asymmetric-drift term AD2_pub = V_circ^2 - V_rot^2.

Frozen form (Jeans equation in the midplane of an axisymmetric, isotropic gas layer, density rho = Sigma/(sqrt(2 pi) h)):

    V_c^2 = V_rot^2 + AD2,   AD2 = -sigma^2 [ dln Sigma/dln R + dln sigma^2/dln R - dln h/dln R ]

- dln Sigma/dln R: analytic-numerical derivative of the published sig_gas at R_k (arcsec scale at D = 78.7 Mpc).
- dln sigma^2/dln R: centred finite difference in ln R between neighbouring rings, one-sided at the two ends.
- Errors on V_c: E_new = E_pub x V_c,new / V_c,pub (the published fractional error kept).

Corners (declared):
- C0 central: sigma_k, h constant. KA-AD: C0's AD2 against AD2_pub; reported ratio per ring, consistency line
  median |ln(AD2_C0/AD2_pub)| <= ln 2. A miss is a tag (no clean label), not a stop.
- C1 IN ERRORS, maximal: sigma_k + 2 e_k in the prefactor; the slope term the most negative of {central,
  (sigma_{k-1} + 2 e_{k-1}, sigma_{k+1} - 2 e_{k+1}) pairs}; h constant (the authors held it fixed, no published error).
- C2 GENEROUS (outside published errors): C1 plus linear flaring, dln h/dln R = 1. Reported; cannot carry RESCUED.
- Also reported: the AD2 each ring would need (V_model^2 - V_rot^2) and the sigma that would need at C0's slope factor.

Grade: data V_c,new against the exact-field V_model (unchanged baryons), both footings; labels per ../FROZEN_CRITERIA.md.

MUTATE: wrong sign, V_c^2 = V_rot^2 - AD2(C1) (clipped at 0). Must give chi2 above the uncorrected exact-field chi2
on both footings.

Direction, stated before computing: AD raises V_c, the direction the law needs (the law over-predicts). QX4 iter3's
"wrong sign" note referred to the term's sign inside the published V_c; it is not used here.

## Malin 1

Lelli+2010 Table 3 as typed by UD2 gives V_c and its error only; no sigma_HI profile is on disk (UD2 inputs hold the
mass-model figures only). Label: NOT EVALUABLE; NEEDS_OWNER.md names the input (the paper's sigma_HI(R), or its
statement of the asymmetric-drift term). Reported, not graded: the AD2 Malin 1's rings would need, and the sigma that
needs at a slope factor of 3.
