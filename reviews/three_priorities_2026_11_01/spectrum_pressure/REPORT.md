# TP01 microscopic spectrum and pressure: result

The full rigid collective-SU(5) tree spectrum has now been constructed:
49 chiral fields, 98 real scalar coordinates, 24 gauge vectors and all 73
Weyl fields including gaugino mixing. Independent representation blocks
reproduce every dense eigenvalue. The one-loop threshold result is new
relative to the earlier leading-log radial test; it is not a completed
quantum/gravitational model. Details are in DERIVATION.md.

Three material conclusions:

1. **The canonical-s exp(6s) warning does not directly transfer to this
   microscopic action.** Its canonical field is T, so s=ln(T/v) has kinetic
   coefficient proportional to exp(2s). Exact full-spectrum traces give
   STr M^4=6f^2h^2lambda^2(29lambda^2-200g^2)/(30h^2+lambda^2)^2,
   independent of X, and zero at the old comparator coupling. The resulting
   one-loop scale cancellation does not cancel the finite thresholds or
   prove all-order protection.
2. **Those finite thresholds still fail the requested dense-pressure
   mechanism at fixed one-loop order.** They give a universal shape
   CW=c^2F(hX/sqrt(c)), c=fh lambda^2/(30h^2+lambda^2).
   With the old assumed portal, positive compressibility ends at
   X/Xmin=1.177299611124933..., while radial local stability survives to
   1.853361810233188... . Positive tree transverse gaps coexist with this
   pressure failure. It is not a hidden transverse tachyon or a missing
   scalar-pressure term.
   The stationary waterbag dictionary gives rho/rho_*=0.590811766203227
   at that boundary, independently of its unknown phase level. Density
   increases along the stable branch, so this fixed-order candidate fails
   compressibility before even reaching the old comparison density scale,
   let alone its dense logarithmic regime.
3. **Higher-order matching matters before interpreting the old coupling
   grid physically.** The omitted old leading-log two-loop curvature is
   .78,3.13,8.69 times the new finite-threshold curvature at equal couplings
   .3,.6,1. A weak-coupling .03 control reduces this known-order diagnostic
   to .00782. These are not uniform error bounds. A final physical exclusion
   or viable pressure prediction needs the consistently matched effective
   action, portal and light/IR sectors.

Evidence: five dense full-spectrum diagnostic points; independent 50-digit
block reconstruction; 729 full-threshold cases covering all nine old
h,lambda pairs and 81 field values each; step-halving and independent 60-digit
derivatives; exact symbolic supertrace identities and five actual gap/pressure
checks, plus 33 normalized-density states. Five successful v2 manifests are
recorded and validated against current hashes. A launch-failed 1 GB
address-space-limit attempt is preserved. CPU affinity is unavailable on
this macOS platform; successful runs use numerical-thread and CPU/wall caps.
Measured peak RSS is below 56 MB. No old file was changed and no Git mutation
was performed by this route.

The next decisive calculation is the same model's consistently matched
RG-improved threshold action and quantum transverse spectrum, preferably
first in its weak-coupling regime, followed by the material portal and
full pressure. It cannot be replaced by rerunning the old one-loop radial
RG curvature or by assuming the potential shape and vacuum offset.

Review provenance: author reconstruction and method-independent numerical
controls, followed by a separate agent's reconstruction of the action,
Hessian, gauge spectrum, supertraces and pressure. The separate report
INDEPENDENT_REVIEW.md passes the result only under the stated rigid,
canonical-K, fixed-order and assumed-portal restrictions. It discloses
that this was not a blind review and that numerical cases were reviewed,
not independently rerun. No literature novelty claim is made. No kappa,
alpha or B/V was selected.
