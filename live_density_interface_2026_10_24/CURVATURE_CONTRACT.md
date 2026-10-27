# LD-9: exact species transfers and relaxed-density curvature

Independently vary T and F masses between cells at fixed total mass and
compare finite energy differences with the species chemical potentials.
Check the joint Hessian against a directional gradient difference.
For the two admissible LD-3 states, project density Hessian to occupied-cell
mass-conserving tangent space (m_i>1e-7 Mb). If positive, compute the Schur
complement and translated-phase curvature using dx/dr in kpc. Report both
frozen and relaxed values and the minimum relaxed phase eigenvalue.
This local finite-grid quantity is not a proof of radius recovery, particularly
at phase endpoints or changes of density active set. No empty-cell activation
or global nucleation stability is inferred. It gives the actual mixed-curvature
correction omitted by the previous fixed-density analysis.
