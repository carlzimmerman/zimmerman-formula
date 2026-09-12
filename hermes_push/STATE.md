# STATE — read at session start, rewrite at session end

iteration: 1
current candidate: C001 ("MOND-state-gated" component, M8-invert + M1, gating variable x = g_N/a_0) — tested, KILLED
last verdict: KILLED at G5 (forest). x = g_N/a_0 ~ 1e-21 on Mpc modes on BOTH footings (a_0 = 9.3619e-11 /
   1.1279e-10) → kernel INERT → forest "preserved" only by inertness (consistent-by-construction, NOT a
   win); transfer T = nu/sqrt x ~ x^{-1/2} is non-universal (distorts, not preserves); the active window
   1 < x_dark < 10 sits at r ~ 1-50 kpc (the galactic-disc MOND regime, the RAR fit) and does not reach
   the Mpc masses (forest x ~ 1e-21) or the cluster anchor (inert, f(R500) = 1.00 vs 0.576); the M8-invert
   c* ~ 0.4 is the closed C000c swing.  3 free parameters, 0 ledger doors passed.  H-entry H001; script
   hermes_push/H001_mondstate_gate_forest.py (+ .out, .json); Lean regime-split certificate
   hermes_push/lean/HermesLean.lean (compiled exit 0, 0 sorry, 0 axioms).
next step: compute C002 ("Halo-gated LATE energy injection"): M2 timing = halo formation / a threshold a_*,
   M3 bookkeeping = mass CONSERVED (redistributed to an outer envelope, not removed).  A one-time late halo
   that does not cut the Mpc linear power.  Pre-registered first-gate kill: G5 forest — must ACTUALLY
   preserve P(k = 5 h/Mpc, z = 2-3) within 10% of LCDM on BOTH footings (not merely be inert), THEN G3
   (cluster f ~ 0.576 reachable with mass conserved), THEN G8 (Omega_m within 3%).  This is Part 5's second
   untested first look ("dynamics that make halos unrelaxed without cutting linear power").  Morph logged:
   M2 + M3 on top of the C001 corpse (keep M8-invert's "unrelaxed halos" goal, drop the inert x-gating).
one-sentence status: C001 killed at G5 (inert forest on both footings; the x = g_N/a_0 gate lives at the
   disc scale, not the Mpc/cluster window) with a compiled Lean regime-split certificate — C002 (halo-gated
   late, mass-conserving injection) is registered and queued next; rows G5/G3/G1/G2/D0 remain red.
commit policy: KEEP ALL CHANGES UNCOMMITTED this session (user directive); commit later only under
   hermes_push/ and only `git` via the commit guard (python3 hermes_push/harness.py) after a green run.

REVIEWER NOTE (2026-09-12, independent check of H001): the kill of C001 stands on D0 (an acceleration-threshold family with no host-mass dependence), but the printed x values were unit errors: x(R500, 1e15 cluster) = 0.45-0.55, x(forest k = 5 h/Mpc, z = 3, delta ~ 1) ~ 3e-3, x(3 R_d spiral) ~ 0.2. Every script that computes x = g_N/a_0 must first reproduce x(R500) in [0.33, 0.58] on both footings as a calibration check, and print it. Lean PART A (Bool lemma) is not a certificate; do not cite it. Proceed with C002 as planned, with this calibration check first.

REVIEWER NOTE (2026-09-12, second): the C002 class (local-density-gated late rate, mass removed or redistributed) has been computed in fable_independent_2026/L188 and is DEAD at G7 (KiDS) for any density-monotone rate, and at G8 if mass is removed — registered as C000i. Do not run C002 as planned; choose a gating variable outside the trilemma (density, potential/velocity, epoch) or a non-local mechanism, and pre-register the KiDS shell retention (<= 0.14 at 0.1-1 Mpc for a 1e12 halo) as the second gate after the forest.

REVIEWER NOTE (2026-09-12, third): a PARTIAL SURVIVOR exists -- C003 clock-frame kicks (see CANDIDATES.md and fable_independent_2026/L189). Your next iterations should ATTACK C003 in this order, each with a pre-registered kill: (1) replace the impulsive retention model by an orbit integration (adapt fable_independent_2026/L167_nbody_kick_test.py: Poisson kicks of 650 km/s at rate 0.38 per DE-weighted Gyr in NFW hosts of sigma = 70/110/300/1000 km/s; kill if spiral f(3R_d) > 0.15 or cluster f(R500) outside 0.45-0.70); (2) a PM simulation (adapt L187's code) with kicks applied to multi-stream particles (velocity relative to the cell mean > 0) after z = 2, DE-weighted rate; kill if P(k = 0.2-0.5 h/Mpc, z = 0.3) drops below 0.85 of LCDM or the k = 5, z = 2.2 power below 0.9; (3) the KiDS 0.1-0.3 Mpc shell of a 1e12 halo at z = 0.4 (kill if > 0.14); (4) the cluster residual profile (X-COP rho ~ r^-1.53 inside R500: does a heated NFW give it?); (5) write the coupling as an action term and check PPN/BBN irrelevance. Do not refit v_k, G0 to a failed gate; report the failure.

REVIEWER NOTE (2026-09-12, fourth): C003 has now been decided by an orbit integration (L191, 7/7) rather than the impulsive estimate: it reproduces the ledger to 22% with two parameters and predicts a UNIVERSAL galaxy-scale dark fraction (retention saturates at the unkicked fraction e^-n because v_k exceeds galactic escape speeds). Attack it there first: (1) the universal-fraction prediction against the SPARC mass range -- does the data tolerate the same dark fraction at 1e9 and 1e11 baryonic mass? kill if SPARC demands a trend steeper than 1.2x across that range; (2) the group prediction 0.168 at R500 against group-scale lensing; (3) a PM simulation of S8/shear with kicks applied to multi-stream particles after z = 2. Note also the L188 CONVENTION CORRECTION in L190: the KiDS bound is on the 1-halo amplitude inside R200, not the 0.1-1 Mpc shell; use 0.514 (not 0.75) as the density-gated number.

REVIEWER NOTE (2026-09-12, fifth -- THE MAIN LINE HAS MOVED, read this before choosing a candidate):
fable_independent_2026/L192 established GRADIENT-DRIVEN CRITICALITY and it reverses the earlier clock-instability kill. The clock-scalar
sound speed had only ever been computed at ZERO field gradient. Carried through with the background gradient invariant Y, the MOND
sector's own nonlinearity turns c_s^2 positive at a finite Y* (0.2 to 2 percent of the transition scale), monotonically and uniquely, and
Y* is a TWO-SIDED ATTRACTOR whose state is c_s^2 = 0 EXACTLY -- pressureless dust, which is the clustering cold component the necessity
certificate demands, with no tuning of the logarithm margin. Lean 109 carries the two structural drivers and the uniqueness.
What is still owed, and is now the highest-value work in the programme:
 (1) THE TRACKING CALCULATION. The sign structure is established; the dynamics are not. Integrate the back-reaction: does the instability
     below Y* actually drive the gradient to Y*, and does it hold there to the fractional precision the forest demands (3e-7 to 2e-6,
     L192 V6)? Pre-register the kill: if the tracked |dY/Y*| exceeds 1e-4 in a Hubble time, the forest gate fails and criticality does not
     save the sector. This is a PDE/ODE calculation, not a search.
 (2) THE SEARCH. `search/run_search.py` already finds coefficient histories meeting every gate in its objective to about 1e-8, with
     s0 just above 1 and Y*/l about 0.04. Run more seeds, widen the family, and ESCALATE any survivor per SEARCH.md.
 (3) C003 (clock-frame kicks) remains a separate partial survivor: L191 gives the ledger to 22% and predicts a UNIVERSAL galaxy-scale dark
     fraction. Test that prediction against the SPARC mass range.
Do not re-run anything in the closed-door list. Do not edit fable_independent_2026/ or qwen_claude_field_theory/.