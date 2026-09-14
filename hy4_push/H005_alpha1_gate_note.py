#!/usr/bin/env python3
"""H005 -- THE alpha_1 GATE: what decides whether H004's completion stands.

STATUS: note + pre-registration.  The deciding computation is the repo's own
f31_ppn_k4_alpha1.py (hunt_2026/), which runs the generalised-AeST PPN
pipeline VERBATIM with the biharmonic term added:

    - (2 - K_B) J_Y xi^2 (D^2 phi)^2

built from the pipeline's own metric, aether and Christoffel objects, to the
same orders (eps^2, w_b^2), so the metric and aether mixings are included and
not hand-waved.  This lane records the physics of the gate and the
pre-registered reading of both outcomes.  It does NOT restate f31's numbers
as its own.

THE PROBLEM (the lock).  On a boosted aether background the generalised-AeST
pipeline gives the closed form

    alpha_1 = -4 c_14 - 4 (2 - K_B)/(J_Y + 1)

The second term is the MOND scalar's drag.  Setting alpha_1 = 0 (the
solar-system requirement |alpha_1| < 1e-4) then forces c_14 < 0, which is a
spin-1 ghost.  So the class is closed: either alpha_1 is over the bound or
the aether carries a ghost.  The lock comes from the scalar having a 1/r
static field, since every PPN parameter is the coefficient of a 1/r-type
potential.

THE ESCAPE (what H004's biharmonic term does).  With the k^4 term the
scalar's static Green's function is Coulomb minus Yukawa,
phi = -G M (1 - e^{-r/xi})/r, which inside xi has NO 1/r piece.  In the
ladder the dimensionless parameter is XI2 = (xi k)^2; at the solar-system
scale of the bounds (1 AU for lunar laser ranging, R_sun for alpha_2) with
xi >= 0.045 pc = 9300 AU, one has

    XI2 >= 8.6e7

i.e. the screening is overwhelmingly in force exactly where the bounds live.
The question is whether the ladder's alpha_1(XI2) then admits

    alpha_1 = 0   with   c_14 > 0   (no spin-1 ghost)

which is what H004 needs.

ANCHORS f31 must reproduce (its own registered controls):
  * XI2 = 0 reproduces the banked alpha_1 = -4(2 + K_B J_Y)/(1 + J_Y) on the
    wf3 grid, with gamma = 1 and alpha_3 = 0.  If it does not, the added term
    is wrong, not the conclusion.

PRE-REGISTERED READING OF THE TWO OUTCOMES
------------------------------------------
IF alpha_1 = 0 is reachable with c_14 > 0 at physical XI2:
    H004 stands.  The completed action survives the preferred-frame gate with
    a healthy aether, and the remaining open items are the perturbation
    amplitudes and xi's value.  This is the result H004 assumes.

IF alpha_1 = 0 still forces c_14 < 0 (or the pipeline fails to reproduce the
XI2 = 0 anchor):
    H004's solar-system escape fails as stated, and the completion is dead as
    a SCREENED AeST host.  The honest fallback is then the equilibrium
    reading already certified in the glm53 track: the RAR as the hydrostatic
    equilibrium of the cold sector, with the relativistic completion left
    open.  That fallback is not a consolation -- it is already a working,
    parameter-free description that passes every gate it faces.

No outcome is massaged.  Whatever f31 prints, this note's reading stands.
"""
print(__doc__)
print("H005 is a pre-registration note.  The deciding run is:")
print("    hunt_2026/f31_ppn_k4_alpha1.py")
print("Run it and read its verdict against the two outcomes above.")
