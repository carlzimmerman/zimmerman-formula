# CD26-5 static/auxiliary evidence

The result is `DUAL_AUXILIARY.md`: the actual canonical U/Z saddle reduces
to the convex functional `I(U)=E_gate(U)+F0*(-BU)`. Its Schur operator is
`E_gate''+B* [F0'']^-1 B`. The compensated gate lower bound and actual
nu_mono superlinear tail give global existence/uniqueness of the joint
positive response on each fixed smooth finite spectral space. Continuum
existence, uniform estimates and gravity evolution remain open.

`run1/` completed with exit code zero: **26 checks passed**, comprising
exact symbolic identities and declared bounded numeric controls. The
computation-audit manifest validator accepted the record. The same script,
contract, raw stdout/stderr and results remain under their recorded hashes.

The deterministic one-harmonic controls use 768 leaf quadrature nodes,
64 nodes for the low-branch kernel primitive, three carrier excitation
levels, and the actual XC4 monotone splice/tail. They solve the finite
variational saddle, not an unlabelled continuum PDE. Largest joint residual
was `7.774336729937659e-13`. Minimum carrier lapse t in the three controls
was approximately `1`, `0.7571651464`, `0.5736884301`; all dual Hessians
were positive. These controls illustrate the theorem and are not its proof.

The weak-source negative control is decisive at its declared scope:
the gate argument stays below `-0.0491288`, its nonlinear variational force
is exactly zero, and the ungated J derivative is approximately `0.06073468`.
The report proves the corresponding open-neighborhood mismatch analytically;
no kernel-tail error estimate can turn an identically inactive nonlinear
gate into the exact ungated law.

`VACUUM_AUDIT.md` records the independent acceptance of root's new action
and fixed-data barrier proof, including the maximum/minimum multiplier
signs and the Taylor-extension domination. No files outside this static
directory were edited, and no commit was made.

`source_provenance.json` records source and output hashes, observed HEAD,
runtime evidence and exact scope. There is no Lean certificate in this lane
and no claim that bounded computation proves continuum or physical closure.
