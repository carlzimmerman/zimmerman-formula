# Interpretation corrections; original evidence retained

* run_compare_runs compared an earlier final trace sample against the other
  run's later termination time. run_compare_checked corrects equal sample times.
* run_warm_audit included its rejected third root in final diagnostics. It was
  never a production accepted trajectory. run_warm_checked keeps only the first
  two accepted roots: time.005Myr, energy error2.77e-10, charge1.14e-13. The third
  root fails. No long global success follows from recovering the first step.
* run_homotopy_audit's scope string inherited the old phrase about a diagonal
  preconditioner. Its actual script/contract and stage records test coupling
  homotopy inside the root. No coefficient is changed during physical time.
* Local wave records label density_perturbation_bound=.05. This is the initial
  modal normalization, not an established supremum on all later density values.
* The early bare triad with added radiation was an incomplete conservative
  reduction of CC. Its failure does not refute the full operator. Complete
  cc_vertex.py and the stationary-elimination audit supply the missing term.
* The node-refined global initial states are conservative PCHIP transfers from
  inherited data. They are not newly force-certified stationary solutions. The
  allF seed is transferred from the inherited coarse negative phase direction,
  not claimed to be a freshly diagonalized fine-grid eigenvector.
* Completed audit processes can contain deliberately failed solver trials.
  Nonconverged comparisons and their state differences are numerical evidence,
  never accepted physical dynamics or a proof of galaxy formation.
* The early cc_mode_wave pilot inherited an irrelevant global-infall bounds
  object in its contract. Its frozen script and result explicitly record the
  actual local150Myr case; no broad coverage is inferred. wave_baseline150 is
  a fresh reproduction with explicit matching bounds for the final baseline
  comparison. Several algebra audits also retain irrelevant inherited bounds;
  their tested finite coefficient cases are explicit in assertion/script/result.
  No universal range or registration claim is made from the inherited object.
