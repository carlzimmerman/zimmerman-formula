import Mathlib
import Mathlib.Tactic
import AS077_cert

/- Axioms transcript for the AS077 certificate. Run:
     cd fable_independent_2026/lean_2026 && lake env lean AS077_axioms.lean
   Expected: every printed axiom set subseteq {propext, Classical.choice, Quot.sound}. -/

#check AS077.amp_identity_sqrt
#check AS077.amp_identity_hyp
#check AS077.amp_equal_iff
#check AS077.matching_radius_given_Mb
#check AS077.deficit_identity
#check AS077.deficit_pos
#check AS077.deep_force_at_rM
#check AS077.shell_field_below_logwell
#check AS077.equipartition_mass

#print axioms AS077.amp_identity_sqrt
#print axioms AS077.amp_identity_hyp
#print axioms AS077.amp_equal_iff
#print axioms AS077.matching_radius_given_Mb
#print axioms AS077.deficit_identity
#print axioms AS077.deficit_pos
#print axioms AS077.deep_force_at_rM
#print axioms AS077.shell_field_below_logwell
#print axioms AS077.equipartition_mass
