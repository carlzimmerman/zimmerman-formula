# AZ18 — PASS premise audit; physical derivation NOT EVALUABLE

κ = ½ FITTED; not theory closed

The target is now explicitly to derive kappa=.5, certify the derivation in Lean, and only then commit/push the successful result. This audit does not achieve it. No push occurred.

PD07's Framework structure has two separate hypotheses: kappa=1/count and count=2. Its half theorem is logically valid conditional on these. Counting two channels does not establish the reciprocal-count hypothesis or fix their physical normalization. Q010 likewise states its physical equilibrium bridge and empirical density tie as unproved premises. Neither file was changed. The audit does not dispute their checked conditional algebra; it disputes using that algebra as an unconditional physical selection theorem.

The new Certificate.lean uses exact rationals to check this distinction without fetching Mathlib. Its normalization family is kappa(b)=1/(2b), b>0, as in the previously derived KT2 relation. TwoChannelCarrier fixes only count=2 and positive normalization. The unit-normalization conditional theorem gives half. The positive doubled-normalization carrier gives a quarter with the same count. That rational subfamily suffices to refute coefficient uniqueness under these reduced premises; it is not a complete physical model or a no-go for a future normalization mechanism.

Five theorems compile with Lean4.34.0-rc2 and print only propext, Classical.choice and Quot.sound. No sorry, admit, user axiom, native_decide or unsafe proof is used. Mutate.lean deliberately asserts the doubled normalization still gives half; Lean rejects it with exit1. check.py records six passing audit checks, input hashes and log hashes. Both footing labels carry the same algebra; physical derivation remains NOT EVALUABLE.

Implementation note: ordinary decide initially stopped at opaque rational arithmetic and produced errors, not an accepted certificate. Kernel reduction via decide +kernel resolved that elaboration issue; the successful file contains no placeholder. This changed the proof tactic, not premises or mathematics. The independent mutation is rejected as false, not merely because it fails to elaborate.

Next load-bearing obligation: derive the relative normalization from a physical action/symmetry whose premises do not already encode kappa, not from a choice of field coordinate or a channel count. A candidate must pass KC1's dimension, vacuum selection, epoch dependence and independent second-prediction conditions before a physical number is computed. The Lean interface will require a proof of that normalization rather than a structure field assuming it.
