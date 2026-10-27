# LD-6: implementation repair, not evidence for or against physics

LD-5's radius-linear cumulative-mass transfer made a finite-density central
cell singular on the quadratic target mesh (u about35). All three attempted
starts failed and are invalid physical evidence. Transfer cumulative mass
linearly in r^3 inside each source cell instead, consistent with cell volume.
Use exact uniform source edges and check constant-density transfer and initial
saturation feasibility before optimization. Repeat precisely LD-5's planned
three K values with the corrected initialization; same action and bounds.
Do not alter LD-5 historical results or call their failure a mechanism failure.
