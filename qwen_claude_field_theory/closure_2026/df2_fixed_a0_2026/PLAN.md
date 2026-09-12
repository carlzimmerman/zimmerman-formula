# DF2 fixed-global-a0 test

Base: 593612171. User approved the DF2 follow-up; preserve all old/concurrent
work. No local a0, coefficient reconstruction, prescribed dark halo or dust
retention fraction is allowed. Canonical a0=9.3619e-11 m/s^2 is an input from
Carl's fitted vacuum-density relation, not newly derived here.

Three independent routes:

1. data/: verify primary stellar and distance inputs, including actual host
   line-of-sight geometry and observed aperture; distinguish missing priors.
2. bridge/: audit the link from the current relativistic P/W/gamma action to
   the requested exponential MOND law and derive observable conventions.
3. solver.py: extend the existing nonrelativistic exponential AQUAL branch
   to a finite stellar source, varying its action and solving the full
   axisymmetric elliptic equation with external-field boundary data. Validate
   against exact Newtonian and isolated solutions, flux and mesh/domain tests.

The static action is independently explicit, not silently a weak-field
reduction of the unfinished relativistic candidate. If that bridge is absent,
the result is conditional static-sector evidence only. A globally weighted
virial second moment is not automatically the measured finite-aperture
dispersion. No likelihood/exclusion may ignore this distinction.

Use a spherical Plummer stellar profile as a controlled numerical benchmark;
compare with primary photometry before treating it as an empirical fit.
Retain successful and failed controls. Bounded individual numerical runs,
deterministic float64 with exact/SymPy checks where useful; no global theorem
or all-requirements PASS inferred from script exits.
