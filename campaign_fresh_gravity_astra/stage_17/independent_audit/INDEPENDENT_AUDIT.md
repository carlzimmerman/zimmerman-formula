# Independent FGF032 energy-protocol audit

**Verdict: proved as written within the smooth, fixed-domain Q diagnostic action.** The exact physical energy source is minus T lambda_dot/(4piG). The theta coordinate change preserves this driven system; its canonical Hamiltonian and flux differ from the original physical energy and flux. It does not supply the missing driver or select a cosmological history.

## Independence and exact claim

The independent local energy and theta transformation were frozen in FROZEN_ENERGY_DERIVATION.md at 2026-09-30T11:31:05.444227+00:00, before reading the new worker or root derivation. The initial inputs were only FGF032 and the pinned original stage04 action. The worker DERIVATION.md and final result were then audited, followed by the root derivation and proof record. No other stage17 audit was read. This is a proof audit with source-hash verification; neither the worker nor this reviewer executed a numerical experiment, symbolic test program, sampled history or synthetic on-shell solution. There is no numerical runner manifest to validate or imply.

## Local physical energy, work and source signs

Write C=4piG, tau=K/c² and sigma=J/v_chi². The physical action has -rho phi once and field potential -W(g,a), with a=a_c exp(chi+lambda(t)). Its signed equations are tau phi_tt-div P=-C rho and sigma chi_tt-J Delta chi+U'=T, P=mu grad phi, T=-a W_a. The dynamic source is div P=C rho+tau phi_tt, not its static specialization. For the Q inverse response, b_a=(a/sqrt(a²+4g²)-1)/2 is negative for g>0, proving T>0. No Newtonian replacement of the constitutive flux is made.

The independently rederived barotropic balance is

 (rho|v|²/2+e)_t+div[(rho|v|²/2+e+p)v]=-rho v dot grad phi,

where p=rho e'-e and e+p=rho h. Adding rho phi and its advective flux cancels the material force work, leaving +rho phi_t. This checks both the enthalpy flux and the single interaction-energy count. The scalar field contributes -rho phi_t-T(chi_t+lambda_dot)/C and the scale field contributes +T chi_t/C. Thus all internal exchanges cancel while the explicit reference work remains:

 E_t+div S=-lambda_dot T/C,
 d/dt integral_V E=-integral_boundary S dot n-lambda_dot integral_V T/C.

Here E includes material kinetic/internal, interaction and both field energies, and S includes enthalpy/interaction advection and the signed field fluxes -phi_t P/C and -J chi_t grad chi/C. The result also agrees with minus the explicit partial-time derivative of the original Lagrangian. For positive lambda_dot and nonzero Q field it extracts energy from the specified system. Physical energy here refers to the original preferred-frame diagnostic action; positivity of arbitrary self-gravitating states or a covariant gravitational energy is not asserted.

The integrated identity uses a fixed spatial volume and outward flux. Impermeable fluid and fixed original field Dirichlet values can set the physical boundary flux to zero. Other traces need their work terms. Closed reference loops need not have zero work because T depends on the actual responding fields; the proof does not claim any particular loop produces a prescribed nonzero amount without a solution.

## Exact coordinate and canonical transformation

Independently substituting theta=chi+lambda(t) yields kinetic velocity theta_t-lambda_dot, unchanged spatial gradient grad theta, and potential U(theta-lambda). The transformed equation is sigma(theta_tt-lambda_ddot)-J Delta theta+U'(theta-lambda)=T. All these terms are needed. The map preserves solutions only with transformed initial and boundary data.

The momentum density is pi_theta=sigma(theta_t-lambda_dot)/C, so the Legendre transform gives the positive correction H_theta=E+lambda_dot pi_theta. The corresponding canonical flux is S_theta=S-J lambda_dot grad theta/C. Their exact source is

 H_theta,t+div S_theta=lambda_ddot pi_theta-lambda_dot U'(theta-lambda)/C.

One can verify the equivalence without relying on canonical terminology: differentiate the Hamiltonian correction, take the divergence of the flux correction, and use pi_theta,t-J Delta theta/C=(T-U')/C. The two T terms cancel and give precisely the displayed source. This agrees independently with minus the explicit partial-time derivative of the transformed Lagrangian. No source has disappeared from the physical balance.

The original fixed chi wall becomes theta_t=lambda_dot. Consequently the transformed canonical boundary flux may be nonzero when the original physical boundary flux is zero. Imposing fixed theta walls instead changes the boundary problem. These identities use the exact displayed transformed Lagrangian, without adding or discarding total-time derivatives.

The zero-rate controls are correct and distinguish intervals from instants. Constant lambda implies both rates vanish, H_theta=E and identical fluxes, while a nonzero constant still translates the potential center. At an isolated instant lambda_dot=0 but lambda_ddot nonzero, energies agree in value but their time derivatives can differ by lambda_ddot pi_theta. Constant nonzero rate does not remove physical work or the translated potential. Replacing the shifted kinetic and potential with an autonomous theta action generally changes the equations. The worker's difference of the two Lagrangians and its remaining -sigma theta lambda_ddot/C after extracting a total derivative are correctly signed.

Dimensions also check: T/C is energy density, pi_theta has energy-density times time units, lambda_dot has inverse-time units, and the flux correction has energy per area per time units. The parameters J,S0,K,v_chi and physical units remain fixed; neither normalization nor a reference history changes these dimensional factors implicitly.

## Off-shell check and source obligation

The root's optional full residual identity was checked algebraically after the independent freeze. With R_c=rho_t+div(rho v) and nonconservative Euler residual R_v=rho Dv/Dt+grad p+rho grad phi, the material residual is v dot R_v+(|v|²/2+e'+phi)R_c. The field residuals are phi_t R_phi/C+chi_t R_chi/C. This matches the reported one-dimensional identity. The distinction between this R_v and a conservative momentum residual matters for the sign of the continuity coefficient; the root explicitly defines the correct choice. No arbitrary off-shell field substitution is counted as a solution or a conservation test.

A new autonomous driver must absorb +lambda_dot T/C in a local completion, or +lambda_dot integral T/C in a uniform global-driver model, along with boundary transfers. The worker's conditional global driver equation d/dt(partial L_drv/partial lambda_dot)-partial L_drv/partial lambda=integral T/C has the correct sign when L_drv has no further explicit time dependence. Multiplying by lambda_dot gives the required energy gain. This only states the necessary obligation; no positive-energy driver, local stress, stable dynamics or desired history has been constructed. The proof does not establish that such a completion exists or is unique.

## Provenance and remaining scope

Current-file SHA256 checks matched all 10 worker input pins and 3 worker artifact pins, plus the 3 root proof inputs and root artifact pin. These administrative checks establish provenance only. The worker's proof-only execution declaration is accurate. Exact hashes of reviewed materials and the frozen independent derivation follow below.

No mathematical gap was found in the scoped identities. Smooth solutions, spatially uniform C2 protocol, fixed domain, barotropic nondissipative matter and valid field chain rules remain hypotheses; global well-posedness, shocks and general g=0 behavior are not proved. Spatially varying lambda would add terms and is outside this transformation.

Both registered a0 normalizations remain separate choices. Constant-vacuum references, frozen H values and externally driven H histories are distinct. The earlier stage04 unforced prescribed-chi H-history obstruction is not removed or promoted into a new calculation. No Hubble-friction or metric equation was added. Varying actual a is not reconciled with a literal constant-vacuum actual-scale identity. There is no M action, RAR stability inference, filtered-MONO transfer, metric/photon completion, empirical evidence, historical novelty claim or theory closure.

The next physical obligation is to specify and audit a driver action, if proposed, against its equation, physical energy, stress and boundary terms. A coordinate change or another arbitrary prescribed history cannot satisfy that obligation by itself.

## Exact pins

- `campaign_fresh_gravity_astra/stage_17/independent_audit/FROZEN_ENERGY_DERIVATION.md`: `deb380c19754f764542a07a198745ebc591bebad092dbe2486ce9ff0ffaed34f`
- `campaign_fresh_gravity_astra/stage_17/independent_audit/DERIVATION_FROZEN.json`: `20b18b0e944382acf13591dca543ab6ac7f8bc7da85640feccc7012adc1a0abb`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-032.md`: `4080f6ad5cc26c1832636231818b703e6f71f05a59c9aa735b822461375d763e`
- `campaign_fresh_gravity_astra/stage_04/scale_dynamics/DERIVATION.md`: `2d00fa29165b274d7288505ffc7756c2189a6915dbec6d500fd1a775f6ffb724`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-032/fgf032_run_001/DERIVATION.md`: `593451d00dfece43f71def5426001b7b863020389f94ca088fcb308c90367590`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-032/fgf032_run_001/result.json`: `f4552c32c9fb4f28067e8f4ba69bf37a445d2472bdf0e3d54ce80d36400f4860`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-032/fgf032_run_001/REPORT.md`: `c1f1736dfd5fed57d31dfade0311caa8a549bbb09622874e80c97483998ec908`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-032/fgf032_run_001/input_sha256.json`: `aa458081076a56afb35d910f9b33c46c82695c2d964b652482cb8e0f7c6228ad`
- `campaign_fresh_gravity_astra/stage_17/energy_identity/ROOT_DERIVATION.md`: `c37b0c4831348da9676d6ab420dff375262f68da403b8275eef3925f265c50a5`
- `campaign_fresh_gravity_astra/stage_17/energy_identity/PROOF_RECORD.json`: `95eef764f305796a570f127a7e4007e476585ca1540e131c4de5889bd6d85039`
