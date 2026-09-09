# Grand-prize research flow

Every candidate action now traverses these gates in order; a later gate cannot
be called passed while an earlier one is only asserted.  Failed lanes remain
in the repository as evidence and are not deleted.

1. **Action and variation:** write one covariant action and vary every field.
2. **Static constitutive law:** derive the exact exponential μ and the
   Newtonian/high-acceleration limit from the same variation.
3. **Independent lensing potentials:** solve Φ and Ψ separately and derive
   γ rather than identifying them by hand.
4. **Canonical/Dirac closure:** list primary and secondary constraints,
   preserve them to closure, compute the bracket matrix, and separate k=0 from
   k≠0.
5. **Degree-of-freedom audit:** count tensor, vector, scalar, clock, and
   auxiliary modes with first/second-class constraints distinguished.
6. **Matter Ward identity:** derive ordinary-matter conservation from the
   single physical metric and the full action.
7. **PPN and preferred-frame:** derive β, γ, α₁, α₂, α₃ on the actual
   screened branch; no values are inserted.
8. **Wave/stability gate:** derive tensor/vector/scalar principal symbols,
   kinetic signs, gradient signs, causal cones, and strong-coupling scales.
9. **FLRW gate:** vary before specializing, require H≠0, derive all density/
   pressure components and perturbation transfer through recombination.
10. **Empirical gate:** fit the fixed law to rotation curves, binaries,
    clusters, CMB and supernova data; record falsifiable new predictions.
11. **Scale relation:** derive or explicitly label the (a_0\)-\Lambda) relation
    as an input; never promote dimensional coincidence to a derivation.

The machine-readable status of the current acceleration-locked-clock lane is
in `GRAND_PRIZE_REQUIREMENTS.json`; exact local calculations are in
`alc_gate.py` and `alc_parameter_scan.py`.  The current lane is **OPEN** and
must not be advertised as a completed theory until every gate reaches a
derived PASS.
