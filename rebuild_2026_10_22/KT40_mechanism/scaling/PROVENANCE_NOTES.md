# Retained scalar normalization error

run_001 correctly checked the dimensionless leading Solar quadrupole q,
all curvature identities and all dwarf decompositions. Its two dimensional
Solar-output fields omitted the frozen factor3/2 in Q2=(3/2)q*a0/rM.
Those dimensional Q2 fields and their coefficient labels are withdrawn.
The run did not test dimensional conversion against the raw reference,
so its execution completed despite that semantic defect.

calculate_v2.py restores the exact existing convention, exposes both the
q*lambda and Q2/(a0/ell) coefficients, and adds an explicit dimensional
comparison against the accepted raw Solar result. run_002 is the accepted
complete table. Historical code/contracts/results remain unchanged.

## Individual virial-component refinement

refinement_001 retained a failed1e-5 relative convergence assertion comparing
finite outer domains1 and2. It failed before writing its result artifact;
its traceback and failed manifest remain. The unchanged total-dispersion
gates in KT39 are not affected. The residual was the small positive A tail,
not a large compensating A/B cancellation.

refinement_002 keeps both original grids as references and adds domains2,4,8
with4000/8000/8000 radial points. The same1e-5 component gate is met across
those expanded domains (maximum6.4521e-6); original-domain A shifts are
at most2.7095e-5 relative, while B changes much less. This records additional
integration coverage, not a relaxed gate or modified physical parameter.
