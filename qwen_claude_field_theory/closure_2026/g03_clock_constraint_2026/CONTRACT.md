# Same-action clock constraint admission and flux representation

2026-09-05. Initial HEAD 8e9d8c601, dirty live research tree. Write only
this directory; do not commit/push or import Fable's different action.

Decision: can canonical constraints consistently exclude the already proved
smooth pre-caustic C-H solution? Derive its ADM constraint admission and
preservation without assigning a finite q'(0). Examine an exact algebraic
Legendre representation, and compute its fixed-k scalar quadratic Poisson
matrix directly, continuing preservation through multiplier determination.

This is a continuation of the existing G03 scalar/caustic checks, not a new
theory. The algebraic representation must reproduce the exact q and its
first variation. A pointwise stationary identity need not preserve a
globally smooth auxiliary-field domain: record that limitation explicitly.

SymPy exact real arithmetic for identities, ranks and constraints; rational
matrix controls; deterministic bounded tests; independent scalar reduction
against the earlier FLRW action. Treat k=0, zero smoothing gain, transverse
flux and the singular constitutive origin separately. No universal DOF
integer may be inferred from a quadratic scalar subsector or finite modes.

Default exit 0 certifies only listed diagnostics; any failed check exits 1.
--require-closed exits 2 because full geometric/physical closure is not
established. A correct equivalent Hamiltonian cannot exclude a smooth
Euler-Lagrange solution by adding an unproved condition. No existence,
uniqueness, gauge-identification or post-caustic continuation theorem is
assumed. No observational or global novelty claim.
