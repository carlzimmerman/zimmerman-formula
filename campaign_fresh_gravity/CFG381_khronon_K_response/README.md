# CFG381: does the khronon equation produce K ~ Gamma/c when the cold fluid settles?

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 364e91182.

**Verdict: DOES NOT PRODUCE.** The gravitationally coupled khronon cannot be CFG373's reaction sink.

**Derivation (sympy Euler-Lagrange, linearised chassis action alpha_c a.a - c_2 K^2, beta = 0).** The chi equation is
lap[c_2 K + alpha_c d_t(chi-dot + Phi)] = 0, so K = -(alpha_c/c_2) d_t(chi-dot + Phi).
The khronon's expansion responds to matter ONLY through alpha_c, via the time-change of the lapse potential. For settling (Phi-dot ~ Gamma Phi, Phi ~ V^2), K_induced/K_needed = 2 (alpha_c/c_2)(V/c)^2 = **1.3e-18 .. 3.9e-13** over the L340 window. Even alpha_c = 1 (excluded) gives only 1e-4.

**Consequence.** CFG373's carrier result stands: the target density is local in the lapse, with zero constants. Its reaction sink needs a DIRECT fluid-khronon coupling lambda_x, which is one new dark-sector constant (baryons untouched, so G9 is intact). With it the sink exists by construction: **CONDITIONAL, +1 constant.** Without it, the record's reaction wall (CFG48 G4 / CFG70) stands.

Controls: C1 linear kinematics, C2 (alpha_c = 0 decouples chi from Phi), and the derived equation all pass. MUTATE (alpha_c -> 1) moves R_K by 3e8, rc 1.
