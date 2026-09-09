# Grand-prize research flow

Every candidate action now traverses these gates in order; a later gate cannot
be called passed while an earlier one is only asserted.  Failed lanes remain
in the repository as evidence and are not deleted.

1. **Action and variation:** write one covariant action and vary every field.
   For the displayed ALC action, the sigma variation gives (X=-1); the
   dedicated `alc_mimetic_acceleration_nogo.py` gate then proves the gradient
   clock has (a_\mu=0) identically.  This kills its acceleration-only MOND
   carrier before later gates can be combined.
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
   The ALC-specific regularisation gate is `alc_aether_regularization.py`: it
   solves the PPN tuning equations symbolically, scans the luminal-GW branch,
   and separates regular extra-scalar points from singular degenerate limits.
   The follow-up `alc_degenerate_dirac.py` derives the local ADM contraction,
   then computes the exact-luminal (k\ne0) primary/secondary chain and
   Poisson matrix.  It finds the two branches without prescribing a rank:
   (c_{123}\ne0) is an instantaneous constraint channel, while
   (c_{123}=0) is rank-degenerate.  The homogeneous (k=0) mode is evaluated
   separately.  The exact exponential primitive is differentiated in the same
   file, so a finite-acceleration completion has a nonzero longitudinal
   constitutive Hessian.
9. **FLRW gate:** vary before specializing, require H≠0, derive all density/
   pressure components and perturbation transfer through recombination.
10. **Empirical gate:** fit the fixed law to rotation curves, binaries,
    clusters, CMB and supernova data; record falsifiable new predictions.
11. **Scale relation:** derive or explicitly label the (a_0\)-\Lambda) relation
    as an input; never promote dimensional coincidence to a derivation.

The machine-readable status of the current acceleration-locked-clock lane is
in `GRAND_PRIZE_REQUIREMENTS.json`; exact local calculations are in
`alc_gate.py`, `alc_parameter_scan.py`, and the on-shell no-go gate.  The
displayed ALC lane is **DEAD_FOR_ALC_ACTION_AS_WRITTEN**; any non-mimetic or
non-gradient successor must be treated as a new theory and re-run through all
gates.
