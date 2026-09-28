import Mathlib
import Mathlib.Tactic
import AS081_cert

/- Axioms transcript for the AS081 certificate. Run (from fable_independent_2026/lean_2026):
     LEAN_PATH=<run_dir>:$(lake env printenv LEAN_PATH) lean --root=<run_dir> <run_dir>/AS081_axioms.lean
   Expected: every printed axiom set subseteq {propext, Classical.choice, Quot.sound}. -/

#print axioms AS081.deriv_const_log
#print axioms AS081.second_deriv_const_log
#print axioms AS081.laplace_log
#print axioms AS081.deriv_const_inv_neg
#print axioms AS081.newton_laplace
#print axioms AS081.laplace_log_pos
#print axioms AS081.wells_separate
#print axioms AS081.laplace_add
#print axioms AS081.no_imposed_baryon_log_well
#print axioms AS081.poisson_source
#print axioms AS081.enclosed_mass
#print axioms AS081.gauss_flux
#print axioms AS081.coincidence_iff
#print axioms AS081.inner_edge_equipartition
#print axioms AS081.exterior_mass_exceeds
#print axioms AS081.double_mass_negative_control
#print axioms AS081.finite_shell_mass
#print axioms AS081.source_invariant