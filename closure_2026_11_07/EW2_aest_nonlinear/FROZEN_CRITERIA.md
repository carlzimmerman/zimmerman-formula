# EW2 frozen criteria (lane level): AeST, its dust-like scalar on the web, in hot wells and in discs

Frozen with iter_1..iter_4/FROZEN_CRITERIA.md, committed alone before any EW2 script or graded number. Kappa = 1/2
FITTED; not theory closed. Adopts nothing; the owner adopts. TEST lane under the owner's 11-07 instruction ("we need to
get all actions that work everywhere"), which overrides the STOP list of DIRECTION_2026_11_07.md for this lane only.
Rules: closure_2026_11_06/SWARM_BRIEF.md bind. No dark-matter particle (the AeST dust is the action's own scalar,
cold dark energy carried by a field). No LCDM inputs: the web and lensing machinery is SV5's / QX3's framework-native
corner background and raw PR4; clusters are raw X-COP / Lovisari; KiDS is the raw Brouwer+21 RAR; SPARC raw rotmod.
Both footings (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2), graded separately, never pooled. No knob scans
to find a pass; where a constant of the class is free (mu, the zero point Delta), the lane MAPS the class over the
record's declared values and a stated range and labels the class, adopting no member. No downloads. nice -n 15,
1-2 threads, small outputs.

## The candidate (iter_1 states it from the record; nothing is added)

v4 = Skordis-Zlosnik AeST (PRL 127, 161302 (2021), arXiv:2007.00082 eq. 5, record transcription C1 / I1) with C1's
capped free function (static limit = the canonical law mu = x/(1+x) exactly), K(Q) = -2 Lambda + K2 (Q - Q0)^2, and
the v3s stiffness term -(gamma_L/2K^2)(q^{mu nu} D_mu D_nu phi + theta Q)^2 (C1, C3, I1). The dust-like part is the
K2 (mass) term, mu^2 = 2 K2 Q0^2/(2 - K_B).

## Iterations (each its own frozen file; failures stay on the record)

| iter | question | graded gates |
|---|---|---|
| iter_1_action_statement | the action, free functions, constants and static equations, exactly from the record | none (known-answer checks only) |
| iter_2_web_cmb_kids | does the scalar's dust branch supply SV5's target with the law OFF on the linear web, and do KiDS hosts keep the law? | W1 SV5 lensing amplitude, W2 shape, QX15 primary CMB, G6 KiDS (QX10) |
| iter_3_clusters_beyond_hydrostatic | does the dust branch condense in deep hot wells (X-COP, groups) beyond the hydrostatic branch? | X-COP (QX10 line), groups (QX10 strict rule) |
| iter_4_static_recheck | SPARC, Cassini, c_T, galaxy lensing on v4's own equations, at the members iter_2 / iter_3 need | SPARC, Cassini, c_T, lensing = dynamics |

Labels per gate: PASS / FAIL / NOT EVALUABLE. A class label (NO-GO FOR CLASS) only where the frozen rule proves no
member of the stated class passes the stated gates together.

## MUTATE (lane level)

Remove the dust-like part (K2 -> 0, so mu = 0): the scalar has no dust branch. Gates that the main run passes only
through the dust branch must then fail (iter_2 W1 at every mu; iter_3's static dust vanishes). Plus per-iteration
MUTATEs (in each file). Separate outputs *_MUTATE.

## Lean

fable_independent_2026/lean_2026/EW2_aest_window.lean and EW2_aest_window_MUTATE.lean: (T1) the capped map
v = a0 g/(a0+g) satisfies 0 <= v < a0 and v (1 + v/(a0 - v)) = g; (T2) band leakage: for weights w_i >= 0 summing to 1
with B_i >= 1 everywhere and B_i >= b on a band set S, sum w_i B_i - 1 >= (b - 1) sum_{i in S} w_i; (T3) static dust mass
bound: sum_i c |Phi_i| v_i <= c Phimax sum_i v_i for c, v_i >= 0, |Phi_i| <= Phimax; (T4) window non-overlap: if every
member passing the web gate has mu >= mu_w and every member passing the host gate has mu <= mu_h with mu_h < mu_w, no
member passes both. The MUTATE twin states false variants (reversed leakage inequality; v = g; overlap). 0 sorry,
standard axioms, .out saved, compiled from the "new_physics copy" checkout's lake env.
