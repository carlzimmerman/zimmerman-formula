import ChainCert.Chain
import ChainCert.Fluid
import ChainCert.PointMass
import ChainCert.Profile

/-! `lake build ChainCert.Axioms` prints the axioms of every theorem in the library; every line must show only
    [propext, Classical.choice, Quot.sound] (checked by `verify_chain.sh`). -/

#print axioms C1_exponent_matrix_det
#print axioms C1_a0_form_unique
#print axioms C1_a0_form_iff
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
#print axioms ChainB.sx_sq
#print axioms ChainB.sx_pos
#print axioms ChainB.sx_hasDeriv
#print axioms ChainB.Mc_hasDerivAt
#print axioms ChainB.rhoC_eq_dMc
#print axioms ChainB.target_ODE
#print axioms ChainB.total_u_sq
#print axioms ChainB.gtot_eq_P2
#print axioms ChainB.charge_identity
#print axioms ChainB.hydrostatic
#print axioms ChainB.dispersion_half_vc_sq
#print axioms ChainB.rhoC_hasDeriv
#print axioms ChainB.Pfun_logderiv
#print axioms ChainB.rhoC_logderiv
#print axioms ChainB.GammaEff_eq
#print axioms ChainB.GammaX_eq
#print axioms ChainB.GammaX_bounds
#print axioms ChainB.GammaX_eq_two_iff
#print axioms ChainB.GammaX_strictAntiOn
#print axioms ChainB.GammaX_tendsto_zero
#print axioms ChainB.GammaX_tendsto_atTop
#print axioms ChainB.no_single_polytrope
#print axioms ChainB.GammaEff_tendsto_zero
#print axioms ChainB.GammaEff_tendsto_atTop
#print axioms ChainC.identity_P
#print axioms ChainC.hydrostatic_general
#print axioms ChainC.charge_nonneg
#print axioms ChainC.rhoC_nonneg
#print axioms ChainC.Pext_tendsto_zero
#print axioms ChainC.pressure_unique
#print axioms ChainC.pressure_nonneg
#print axioms ChainC.pressure_pos
#print axioms ChainC.dispersion_ratio
#print axioms ChainC.target_iff_ode
#print axioms ChainC.ode_hasDerivAt
#print axioms ChainC.w_eq
#print axioms ChainC.gtot_pointMass
#print axioms ChainC.pointMass_target
#print axioms ChainC.Pext_pointMass
#print axioms ChainC.pointMass_config
#print axioms ChainC.pointMass_decay
#print axioms ChainC.pointMass_pressure_pos
#print axioms ChainC.pointMass_hydrostatic
#print axioms ChainC.pointMass_ode
#print axioms ChainC.isothermal_config
#print axioms ChainC.exp_profile_identity_P
#print axioms ChainC.exp_profile_decay
