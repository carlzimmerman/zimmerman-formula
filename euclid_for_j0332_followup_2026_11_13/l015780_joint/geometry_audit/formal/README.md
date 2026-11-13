# Exact finite four-source certificate

`FiniteCapacity.lean` proves source-association incompatibility of the stored
inclination90,logM11.925 field, at zero external convergence, for every
beta in[0,1] and arbitrary real constant-shear components. It proves a finite
algebraic claim under explicit premises, **not** the accuracy of the AQUAL
solver, correctness of the observational association, or an empirical
full-theory exclusion.

The proof includes the exact four-source pair identity, the Euclidean-diameter
implication, an explicit rational nuisance-null functional, and the concrete
field instance. With source coordinatesx_i,y_i, the functional is

    P=-72x0-69y0+7x1-61y1+130x2-65x3+130y3.

Its weights annihilate both constant source offsets and both unrestricted
shear components. For the actual released marker coordinates, its value on
the model sources is

    P(b)=1033.6-beta*P(alpha).

The.3arcsec Euclidean pair-diameter gate implies P(b)<=100.2. The declared
component field box, of halfwidth.05arcsec around the stated four-decimal
centers, implies P(alpha)<=750. Since0<=beta<=1, P(b)>=283.6, a contradiction.
The stored binary floating-point deflections are imported as exact rational
constants and proved inside that box by Lean's rational arithmetic. The box
is a mathematical robustness fixture; it is not a claim that true physical
field errors are bounded by.05arcsec.

`instance.json` records the exact extracted rational numbers, field/source
hashes, inclination and mass. `make_certificate.py` generated the instance
from the frozen supplied table. The accepted source was not edited during
root or independent-agent proof review. The separate independent review is
`independent_review.md`.

The authoritative verification is `run_02` under `contract_v2.json`:

- Accepted Lean source compiles with exit0.
- Changing the actual gate to3arcsec while retaining the certificate makes
  the proof fail with an affirmative `linarith failed to find a contradiction`
  diagnostic. This is a genuine proof negative control, not a launch error.
- Guards reject file-not-found and module/import failures as negative-control
  evidence.
- Input hashes are unchanged before and after. The v2 bounded manifest
  validates against current inputs.
- Lean4.34.0-rc2 reports only standard axioms `propext`, `Classical.choice`,
  `Quot.sound`; no custom axioms or admitted proofs occur.

`run_01` and `verify_certificate.py` are preserved for provenance. That first
verifier passed a relative mutation path to Lean's different working directory:
its negative exit was file-not-found and **does not validate a negative
control**. Its accepted-source compile was valid. The versioned
`verify_certificate_v2.py` fixes the path and requires an actual proof-failure
diagnostic; cite `run_02` for complete positive/negative evidence.

Direct reproduction, writing to a new output directory:

    python3 euclid_for_j0332_followup_2026_11_13/l015780_joint/geometry_audit/formal/verify_certificate_v2.py --output NEW_OUTPUT_DIRECTORY

The verifier invokes the existing canonical project's `lake env lean` on the
new file by absolute path. It does not edit the canonical project. No novelty
or breakthrough claim is made; this certificate closes a specific arithmetic
obligation used by the finite source-position capacity diagnostic.
