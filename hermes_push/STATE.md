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
