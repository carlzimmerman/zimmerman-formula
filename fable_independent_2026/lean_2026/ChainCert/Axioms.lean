import ChainCert.Chain
import ChainCert.Fluid

/-! `lake build ChainCert.Axioms` prints the axioms of every theorem in the library; every line must show only
    [propext, Classical.choice, Quot.sound] (checked by `verify_chain.sh`). -/

#print axioms C1_exponent_matrix_det
#print axioms C1_a0_form_unique
#print axioms C2_nuBeta_one
#print axioms C2_nuBeta_mul_sqrt
#print axioms C2_nuBeta_deep
#print axioms C2_deep_mond_flat_speed
#print axioms C2_btfr_from_vacuum
#print axioms C3_conservation
#print axioms C3_max_rule_monotone
#print axioms C4_rival_exceeds_flat
#print axioms C4_rival_strictMono
#print axioms C4_E_at_two_point_five
#print axioms C4_flat_iff_rho_const
#print axioms C5_kappa_free
#print axioms nuMono_aux
#print axioms nuMono_deep
#print axioms nuMono_btfr_from_vacuum
#print axioms ChainPremises.a0_pos
#print axioms ChainPremises.a0_flat
#print axioms ChainPremises.btfr_limit
#print axioms ChainPremises.btfr_limit_redshift_independent
#print axioms zero_point_linear_in_kappa
#print axioms rhoFluid_hasDeriv
#print axioms fluid_pressure
#print axioms fluid_pressure_bounds
#print axioms cap_a0_tie
#print axioms cap_a0_eq
