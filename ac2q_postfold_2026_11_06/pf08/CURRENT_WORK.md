# Latest PF08 checkpoint — read this before historical notes

Scientific objective remains unachieved. Do not claim full-action failure,
unavoidable new physics, or uniquely selected singular continuation.
Current result: STATUS.md; independent exact derivation:
principal_review/RIEMANN_SOURCES.md. All numerical evolution jobs finished.

New numerics:
- reduced_system_v2.py checks independent/reconstructed means and unaugmented
  tangent equation. reduced_validation002 passes6 checks.
- evolve_reduced.py/v2/v3 implement reduced evolution, valid-checkpoint Fourier
  prolongation, and optional evaluation padding. All used sizes odd and adequate.
- r511: first spectrum failure1.4125, peak qgrad1.5991.
- r1023_a: first spectrum failure1.441875, qgrad2.5277.
- r2047_a valid checkpoint1.39703125; r2047_b spectrum failure1.45984375,
  qgrad3.9844. Started by prolonging valid g1023_a checkpoint.
- r4095_a/b/c valid wall checkpoints1.423046875,1.444453125,1.467578125;
  r4095_d spectrum failure1.47125, qgrad6.3067. All requested1.8 NOT reached.
  Initial fine eval8191; b onward uses12285. No longer pure same-padding refinement.
  r4095_c is the latest valid saved checkpoint suitable for another restart.
- comparison001 passes t1.4 extrema/time/space gradient diagnostics;
  comparison is not full-state norm convergence. Plot refinement.png shows
  accepted steps only. Every failing final step remains excluded.
- riccati002 passes5 exact quadratic/weight identities. riccati_contract.json
  was rejected pre-run because bounds empty; corrected v2 contract used.
- manifest_validation.json records hashes/checks; validation of a failed run
  means its evidence is intact, NOT that evolution passed its acceptance checks.

New analytic results:
- Curved weighted coercivity includes missing -2P E_beta K/r forcing.
- Exact Riemann sources, Cartan spin cancellation, algebraic base curvature.
- Direct w_sigma=K+sigma e(log r)/c has self coefficient G/4>0; a positive
  r,A weight removes the mixed family product, with linear-gradient remainder.
- Covariant conservative gradient equation gives localized TV bound independent
  of peak compression; localized packet avoids large global-TV problem.
- Audited periodic auxiliary small-amplitude solve in C1 unknowns/C0 prescribed r
  is uniform in packet width. beta flat, E0,Bconstant,K=(rho/M-B²)/(2B) satisfies
  ADM constraints with bounded initial geometry and arbitrarily steep r.
- Conditional Riccati argument gives short finite-gradient breakdown IF native
  local classical existence and suitable continuation/constraint propagation hold.
- Clock gauge ds²=-r^-2 dτ²+L²dx²+e2βdy² yields symmetrizable a,K block and
  nB=-aE+(-3B²+E²-Tee/M)/2. No principal derivative-loss obstruction found.
  BUT W_PP(P) has a |P| cusp at0: naive high Sobolev theorem does not apply.
  Need tailored characteristic/Lipschitz or mixed-regularity existence proof,
  and all differentiated/Einstein constraints propagated. Not illposedness proof.
- Singular selection remains separate and unresolved. PF07 excludes bounded
  layers under explicit hypotheses; does not exclude all degenerating native limits.

Next useful work: prove clock-gauge local evolution at actual hold-law regularity
without smoothing/altering action, then finish constraint propagation. Further
refinement can test event approach but cannot select a singular weak solution.
Keep use of python3 (recordedSciPy1.11.4), immutable hashed experiment scripts,
runner, and scope ac2q_postfold_2026_11_06 only. No background evolution remains.

---
Historical mid-phase checkpoint follows (superseded where above differs):

# Live PF08 checkpoint (not a final result)

Current user explicitly asks to keep working until full coupled formation/
avoidance and singular native selection are decided. Do not claim completion.
Base d7aba1da7f; PF08 criteria committed9979f1a817. All other PF08 edits currently
uncommitted. Keep all evidence. Earlier PF07 result remains valid with its limits.

Numerics completed:
- fft_constraints.py matches dense constraints/RHS, validation001 seven checks.
  n255 stops raw momentum at1.33375, n511 at1.389375. n1023 initial fails Newton
  at3.89e-9, above2e-9 criterion. This is roundoff, not physics.
- gradient_constraints.py solves g=P_x+meanP instead of nodal P; same action,
  initial n1023 residual4.21e-11. gradient_validation001 nine checks pass.
  g511 same stop. g1023_a is valid wall checkpoint at1.0459375 (requested1.7 NOT
  reached). g2047_a valid wall checkpoint at.4603125 (requested.8 NOT reached).
  All jobs currently finished. Restart data include final_gvar.
- expanded_rate.py generated from exact jet algebra cancelling N_xx,beta_xxx
  using momentum and gauge constraints. derive_expanded_recorded first failed
  CLI variable shadowing; v2 recorded expanded_algebra002 passes7 identities;
  generated_rate.py equals expanded_rate.py. expanded_validation001 nine checks
  pass. e511 still raw-momentum stop1.389375. No change to physical equations.
- Independent EXPANDED_REVIEW.md derives discrepancy C_x-sensitive remainder.
- constraint_rate001 checks differentiated momentum reconstruction vs canonical
  p_lambda,t: represented errors1.6e-12 at t1;1.5e-7/1.1e-7 at n255/n511 legacy
  raw stops. Mean-only reduced formulation proposed, criteria in
  MEAN_MOMENTUM_CONTRACT.md (rate error1e-6 + physical spectra1e-3 + domains).
- reduced_system.py evolves lambda,beta,meanpl,r_mom, reconstructs full pl.
  reduced_validation001 passes3 checks, t.5 q difference5.2e-13 and rate error
  1.37e-10. Reviewer REDUCED_REVIEW.md passes architecture but requests explicit
  mean-target and unaugmented tangent residual diagnostics. Add version2 and
  validation before new evolution. Keep global periodic compatibility check.
  Cache is only initial guess; verified t1 perturb-cache differences1.6e-15.
- np.longdouble on this Mac is ordinary float64; cannot claim extended precision.

Math completed (independent reviewer /root/review_coupled_solver):
- principal_review/REVIEW.md +7 exact checks: frozen-A k-essence is genuinely
  nonlinear for0<gamma r0²<1; exact finite-K nonconstant frozen-A wave impossible
  because eA=Wp/r forcesP0 thenD0, so full formation transfer remains required.
- principal_review/COERCIVITY.md: u=nA/r,v=nP/r obey flat spatial system
  eu=a u+b v+f eθ; ev=c u-a v+g eθ.
  a=Wp D_r/(rR), b=Wpp/r+Wp²/(r³R)>0,
  c=r(1-2gamma D)/(gamma R)>0,
  f=Wp/r²*(1+h/(rR)), g=D/r-D_r*h/(rR),
  h=H_r,R=H_rr=1+gamma D_r²-2gamma D.
  Periodic proper-arclength energy e(uv)=c u²+b v²+forcing gives no kernel
  and derivative-free inverse bounds. Useful bound C[oscθ+osc(f,g)TVθ].
  Constants need positive margins and controlled slice length. This closes a
  flat inverse sublemma, not full formation.
- Reviewer currently ACTIVE on requested CURVED_COERCIVITY.md. Candidate:
  B=nβ,Eb=eβ,Kx=div2n; mixed Einstein and T_ne=0 give
  n(eβ)=-(er/r)B-B Eb. Curved u/v system trace becomes-2Eb and multiplying
  energy byexp2β cancels trace. Forcing includes er as well as eθ plus bounded
  geometry. Need independent derivation, no premature theorem claim.
- Potential next bootstrap: fixed length, amplitudeδ=k^-1/2, TV~sqrt k keeps
  oscF*TV bounded; if curved inverse and amplitude/TV/domain persist, derivatives
  of auxiliary source are only linear in gradients. Lax weighted gradients
  remove cross-family quadratic terms, potentially yielding full Riccati
  comparison. Initial Einstein constraints and geometric bounds still obligations.

Tools: runner path /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/
mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py. Max120sec jobs,
wall checkpoints105s. functions store has runFFT/runGrad/runExpVal/runExpanded/
runReducedVal templates if retained; otherwise inspect contracts exact input lists.
Use python3, NOT python (different SciPy signature). Workspace writes authorized;
.git commits require escalated tool, auto-approved so far. Scope only research dir.
