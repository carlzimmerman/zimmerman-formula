# Independent raw review: radiation-epoch transfer

Accepted within the stated ideal-fluid action, admitted-background and finite-interval scopes. No blocking correction is required. The exact constraint transport does pass through ordinary equality; the numerical experiment demonstrates dependence on independent carrier/radiation seed data at the same evolved dust amplitude. It does not prepare a unique primordial mode, identify a positive cold abundance, or certify full scalar/tensor health.

## Pinned inputs and independent procedure

Reviewed on 2026-10-06 at HEAD `1db53a670a09a76c023e70784fddc5f351fb8a81`. Frozen REPORT SHA256 `560997eff96991faec5b28e661c4ace882ba419ac2ab2834113ae09186de2fc7`; transfer.py SHA256 `86775cc43cca02628b0eafe1249ecbce43e1b9be959280626d18b8218f830833`. Both match the requested revisions. Dependency hashes are listed at the end.

I read the raw action/closure, background equations, transfer script, contract, results and preserved preflights. I reconstructed the trace/Bianchi closure, residual k0 preparation, source decomposition and constrained transport argument independently. I extracted only pure function definitions from the background/closure AST for bounded independent evaluations, without executing the transfer/import harness or writing author inputs. Standard validation independently accepts all three current manifests. The author's passing verdict was not treated as proof.

## Exact constrained transport through equality

For `F=M−2xi|chi|^2`, the raw metric residual is `E_mu_nu=F G_mu_nu−T_mu_nu−nabla_mu nabla_nu F+g_mu_nu box F`. Klein–Gordon with provisional Ralg gives `box F=−4xi[X+xi Ralg f]`. Its trace is therefore exactly `E^mu_mu=F(Ralg−Rgeo)`, using `B Ralg=rho_d−2(6xi−1)X` and B=F+12xi²f.

Canonical stress divergence is `xi Ralg partial_nu f=−Ralg partial_nu F/2`. The derivative commutator in the metric row then gives `nabla_mu E^mu_nu=(partial_nu F/2)(Ralg−Rgeo)`. For a homogeneous background the linear spatial right side vanishes. With momentum and traceless spatial equations imposed and k!=0, its spatial component forces the residual isotropic pressure P=0. The trace reduces to the mixed00 residual C. The temporal identity consequently gives

`dot C=[Fdot/(2F)−3H]C`.

I independently checked this off-constraint identity at unrelated nonzero perturbation vectors at the two initial backgrounds: complex-step directional residuals were approximately 3.0e−16 and1.5e−16 relative to1+abs(prediction). These evaluations corroborate the analytic identity; they do not turn it into a universal numerical proof.

The nine-dimensional real coefficient matrix is continuous on every compact smooth interval with F,B,H bounded away from zero and finite background. Its fundamental matrix is invertible by the determinant identity. Integration gives the nonzero constraint multiplier `sqrt(F/F_initial)(a_initial/a)^3`. The constraint row is nonzero: its coefficient of ordinary delta_d is rho_d>0, since momentum contains no delta_d. Thus it defines an eight-dimensional hyperplane, and the full fundamental matrix maps its kernel bijectively to the corresponding kernel at any other time. This conclusion is for all compatible data, even though the executable transports only three selected columns.

Ordinary equality rho_r=rho_d at a=.01 introduces no denominator in this system. It is not equality of all effective stress or a proof of textbook radiation-to-matter expansion. A failure of the chart that solves for Phi would not by itself singularize transport: the constraint can instead solve for delta_d. F=0 and absence of a admitted earlier history are separate boundaries. The finite solver's sampled positive-F checks are corroboration, not a certified between-node bound or a completion across that boundary.

## k0 residual family and finite-k preparation

Set `delta chi=−chidot T`, `Phi=HT−ell`, `Psi=−Tdot`, with constant spatial dilation ell. Since `delta F=−Fdot T`, slip requires exactly `Tdot+(H+Fdot/F)T=ell`. Its solution is `[C_T+ell integral aF dt]/(aF)`.

The ordinary equations give delta_d=3HT, delta_r=4HT, v_d=v_r=T. Dust Euler is Tdot=−Psi; radiation Euler is Tdot=HT−Psi−delta_r/4; both continuity equations reduce to the derivative of Phi. Momentum reduces to the actual background acceleration identity, with Y=Hdot T. The trace gives delta R=−Rdot T, and the differentiated scalar background equation supplies the KG rows. Thus the family solves the displayed k0 rows directly; it does not rely on extending the k>0 spatial constraint proof to k0. Independent initial-point complex-step checks gave row errors below1.6e−16 and Hamiltonian residuals below1e−15.

At k0 this is a residual coordinate/time-shift family, not a unique physical primordial state. Selecting its integral lower boundary or C_T requires additional early history. For finite k the script retains its ordinary entropy-free/equal-velocity coordinates but projects Phi to enforce the actual Hamiltonian constraint. That changes the metric datum and does not prove an exact growing adiabatic continuation. At equality p/H~.745,.717 it is not an asymptotically superhorizon approximation. The report correctly retains all these caveats. Direct fluid subtraction gives `dot(delta_d−3delta_r/4)=p²(v_d−v_r)`.

## Source and stress dictionary

Eliminating slip/momentum from mixed00 gives

`2F p²W=−delta rho+3Hdelta q+6H²delta F−3Fdot Y`.

Substituting actual dust, radiation and canonical-carrier density/momentum gives the displayed Wd,Wr,Wchi exactly. In particular the carrier momentum term is `−6H Re(chidot*delta chi)` and the nonminimal `+6H²delta F−3Fdot Y` terms survive. This is an additive identity on one coupled solution, not independent Poisson laws with other species held fixed.

With fixed M Einstein gravity, `delta rho_chi,EH=−2M[p²Phi+3HY]−rho_d delta_d−rho_r delta_r`. The improved trace is `M delta R=rho_d delta_d+delta rho_chi,EH−3delta p_chi,EH`; ordinary radiation cancels from this trace. This verifies the operational pressure formula. Nonzero Newton-gauge pressure excludes an exact ordinary pressureless stress for those prepared columns, but does not measure rest-frame sound speed or exclude approximately cold modes from another preparation.

The same-evolved-dust comparison is genuine normalization of each full column by its nonzero Delta_d, not a comparison of equal initial density alone. Independently reading main_a gives equality W/Delta_d about (−156.5405,−208.9310,−1601.3433) for xi100 and (−1.7930265,−1.8530261,−4.8469163) for xi1000. The instantaneous bare-M dust-only coefficients on those same backgrounds are −1.48514481038 and−1.48514814449. This reference is algebraic, not a GR transfer solution with identical expansion and removed carrier. Actual dust Wd includes1/F; ordinary radiation and improved carrier source still depend on the seed. All decomposed sources were evaluated on the actual evolved columns, so no inferred lensing residual is created merely by substituting an unperturbed source.

The phase seed is a phase-velocity/charge-density kick; a constant U(1) rotation would be different. Its Fourier charge need not alter the spatially averaged background charge. Unit-column amplitudes and large backward coefficients are not observational perturbations; linear physical amplitudes can be rescaled arbitrarily small over this compact interval.

## Numerical evidence and resource reconciliation

The final32-state integration carries five shared background entries plus three nine-state columns. DOP853 and Radau use the same finite endpoints,102 common nodes including exact equality, rtol1e−9/atol1e−12. Radau's complex-step Jacobian differentiates the analytic equations rather than their absolute-value diagnostic scales; the positive Friedmann-root formulas are locally equivalent analytic branches. This supplies a numerical Jacobian, not a symbolic full-background Jacobian theorem.

The160000 nfev condition is a post-run acceptance threshold. The200000 total RHS-call guard is enforced inside the function and includes all complex-step Jacobian calls; the external runner additionally caps wall/CPU execution. All current paths satisfy the declared thresholds. For xi100, DOP853/Radau nfev are3596/45708 and total calls3596/53580. For xi1000 they are9968/130780 and total calls9968/149180. Common-vector solver discrepancies are2.17e−7 and6.68e−7. These norms do not certify individual relative accuracy near zero, but the finite same-dust differences dwarf solver spread, and the ratio is only used where Delta_d is nonzero. No solver rerun or parameter extension was needed for this audit.

The two preserved failed development cases are real: preflight37/38 and preflight_b45/46 exceed the old60000 nfev bound for xi1000 Radau with130841 and130626 evaluations. Their exact scripts/results remain archived. The final larger-resource run is a newly declared bounded case, not a retroactive relabeling of those failures.

Current main_a is46/46. Control_trace_a is38/46, failing Hamiltonian and actual-source decomposition in exactly the four solver/background paths. Control_source_a is42/46, failing only the four decomposition comparisons when carrier source is erased. All three current manifests validate against pinned inputs/outputs; REPORT is outside execution inputs as declared. Validation authenticates execution records and does not replace the above mathematical interpretation.

## Verdict and first missing physical implication

The child closes a bounded action-consistent transport/decomposition calculation through ordinary equality. It does not choose the eight-dimensional primordial covariance, admit the F boundary, establish positive cold abundance, or supply actual photon/baryon/recombination transport. A healthy earlier background and justified initial-state preparation remain the first load-bearing physical inputs. No32pi or particle-identity selector follows from these columns.

Dependency hashes:

- sol61_push/recombination_and_structure_growth/curvature_carrier_radiation_matching_2026_10_06/self_consistent_history/physical_growth_closure/radiation_epoch_transfer/REPORT.md: `560997eff96991faec5b28e661c4ace882ba419ac2ab2834113ae09186de2fc7`
- sol61_push/recombination_and_structure_growth/curvature_carrier_radiation_matching_2026_10_06/self_consistent_history/physical_growth_closure/radiation_epoch_transfer/transfer.py: `86775cc43cca02628b0eafe1249ecbce43e1b9be959280626d18b8218f830833`
- sol61_push/recombination_and_structure_growth/curvature_carrier_radiation_matching_2026_10_06/self_consistent_history/physical_growth_closure/growth.py: `3d5934f3e00344f47e6dc6dd042c84f9fb92ddec084c53cf3e0fbcbe83b62367`
- sol61_push/recombination_and_structure_growth/curvature_carrier_radiation_matching_2026_10_06/self_consistent_history/equations.py: `f28552fae9281b3e7bbdfea3f77ad6702c0c425595228cc8fc8059998529cbbf`
