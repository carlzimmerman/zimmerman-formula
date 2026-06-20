# BRIDGE DOORS — people→connections→gaps→RUNNABLE computational doors (2026-06-19)
Arm: lambda_cc_desi (with reach into GAP-1/2/5 from the shared scout pool).
Both-ways + quarantine (a0/Z/kappa/I0 NEVER asserted derived). A "door" here = a CALCULATION
with a definite PASS/KILL or NUMBER, the tool, the inputs, and the both-ways outcome. Reading
lists are NOT doors. Built on the banked GHOST_CONDENSATE_* + AEST_EMBEDDING + DARK_MATTER_ILLUSION
and the five bridge_scout/ notes. Literature verified via WebSearch/WebFetch (arXiv IDs cited).

================================================================================
THE CONNECTION MAP (who → what idea → which gap)
================================================================================

GHOST-CONDENSATE SPINE (GAP-1 origin, GAP-2 frame):
  Horava (foliation/shift-sym) --tangential--> ACLM=Arkani-Hamed-Cheng-Luty-MUKOHYAMA 2004
  (hep-th/0312099, ghost condensate; the field IS the framework's Q-mode) --> Lim-Sawicki-VIKMAN
  "Ghost Dark Matter" 1001.4634 (a^-3 dust, amount FREE) --> SKORDIS-ZLOSNIK AeST 2007.00082 +
  Verwayen-Skordis-Zlosnik 2024 (K(Q)=mu^2(Q-1)^2 = the framework's postulate, cites ACLM) -->
  Blanchet-SKORDIS Khronon 2404.06584 (SAME mu^2(Q-1)^2, by the host author).
  THE NUMBER the chain shares: ALL postulate the kinetic shape; NONE derive it. GAP-1 is field-wide.

POSITIVITY/CAUSALITY (GAP-1 consistency, KILL-or-PERMIT):
  Grall-Melville 2102.05683 (boost-free positivity, no LI UV needed -> APPLIES to the GC) -->
  Serra-Trombetta 2412.19745 (the IR re-expression: "gapped modes must propagate SLOWER than the
  gapless mode below the gap" — a low-energy KINEMATIC inequality the framework can be checked
  against directly). CREMINELLI-Janssen-Senatore 2207.14224 needs a CONFORMAL UV completion -> does
  NOT apply to the GC (do not mis-cite as a kill).

dS-QFT / THE GATE (GAP-2):
  SENGOR/Anninos/Gazeau dS UIR program (SO(4,1)-invariant, CODIFIES the wall) | static-patch
  observer CLPW 2206.10780 + Chen-Xu 2511.00622 (breaks SO(4,1)->SO(d)xR, but observer=gauge) |
  KIRITSIS 1207.2325 ("LV must live in a gravitational field" -> Cerenkov/dissipation CONSTRAINT).

LAMBDA/CC + DESI (GAP-3 coeff, GAP-4 amount, a0(z) hostage):
  PADILLA-Khoury-Muntz lapse/sequestering 2604.08659 (global constraint -> Lambda = free
  integration constant fixed by <T>, RELAXES not pins) | Blanchet-SERAILLE 2502.14686 (independent
  fundamental gauge theory -> Lambda ~ a0^2/c^4 = a0 prop sqrt(Lambda), CORROBORATES the scaling) |
  CALDERON/DESI DR2 w0=-0.752 wa=-0.86 (rho_DE non-monotonic hump; a0(z) hostage).

================================================================================
THE DOORS (calc + tool + inputs + both-ways) — see structured object for the full ledger.
================================================================================
Summary of the 7 doors, ranked:

D1 [GAP-1, ready-now, HIGH]  Serra-Trombetta IR positivity gauntlet on the framework's OWN bilinear
   coefficients. The banked expand_PX_around_condensate.py already has time-coeff = P'+2X0P'' and
   space-coeff = -P' -> 0. Compute the gapless (pi, omega^2 = c_pi^2 k^4/M^2... but c_grad=0) and the
   gapped AeST transverse-vector (omega^2 = c_g^2 k^2 + mu^2) sound speeds from the AeST window
   {0<K_B<2, K2, mu, lambda_s}; impose c_gapped < c_gapless below k<mu and c_gapped<=c (subluminal).
   PASS = framework's wrong-sign-then-stabilized P(X) is positivity/causality-consistent (a real
   consistency win, the literature PERMITS). KILL = a region of the AeST window is excluded -> a NEW
   constraint on {K_B,K2,mu} (as valuable as a bridge). Tool: sympy + numpy scan of the window.

D2 [GAP-3, ready-now, HIGH]  Blanchet-Seraille coefficient confrontation. Both routes give a0 prop
   sqrt(Lambda); compute the framework's coefficient kappa_fw from a0=c^2 sqrt(Lambda/32pi) i.e.
   Lambda = 32pi a0^2/c^4, and Seraille's Lambda ~ a0^2/c^4 coefficient (their Eq. for Lambda in
   2502.14686), and form the ratio. PASS(bridge) = the two independent mechanisms give the SAME O(1)
   coefficient (would be a genuine cross-derivation of kappa). KILL/null = they differ by an O(1) that
   is mechanism-dependent -> CONFIRMS kappa is not forced (GAP-3 stays open), the scaling is shared but
   the coefficient is not. Tool: sympy/numpy, both papers' formulae.

D3 [GAP-3, ready-now, HIGH]  Sequestering global-constraint test of whether <T> fixes kappa. Set up
   Padilla's global constraint Lambda_eff = (1/4)<T>_spacetime-average (from 2604.08659/sequestering),
   and ask: does any combination of {a0, the dS-Unruh T_eff, the framework's matter content} make
   <T> = 32pi a0^2/c^4 forced? Expected KILL/null (the constraint relates Lambda to the matter trace
   average, an IC, NOT to a0) — but run it: PASS(bridge, unlikely) = a0 appears in <T> via the GC
   stress tensor and pins kappa; KILL = <T> is a0-independent -> sequestering RELAXES kappa (free
   integration constant), the OPPOSITE of pinning. Tool: sympy (stress-tensor trace of the GC + matter).

D4 [a0(z)/GAP-3, ready-now, HIGH]  Sharpest falsifiable a0(z) prediction vs the DESI non-monotonic
   hump. Extend the banked a0z_desi_figure.py: the scout found rho_DE RISES to z~0.5 then declines, so
   the framework's a0(z) prop sqrt(rho_DE) predicts a +X% RISE to z~0.5 then a decline — compute the
   exact bump amplitude + the z=3 split vs the rival rising-sqrt(rho_tot) reading, AND the BTFR-sign
   consequence. OUTPUT = a NUMBER (bump %, z=3 ratio) + current data status. Both-ways: this is the
   live front; w->-1 dissolves it (state that). Tool: numpy (already in-repo).

D5 [GAP-4, ready-now, MED]  Discrete-series shift-charge test of I0. Sengor/Gazeau: the framework's
   shift-symmetric Q-mode's dS-QFT home is the dS DISCRETE SERIES (tachyonic scalar w/ enhanced shift
   symmetry). Compute whether the discrete-series quantization fixes the shift-charge I0 (the conserved
   charge of the enhanced shift symmetry) or leaves it a free label. Expected KILL (classification not
   dynamics; I0 stays the free mean of a flat direction, d rho_dust/dLambda=0 banked). PASS(unlikely) =
   a quantization condition on the discrete-series charge pins I0. Tool: sympy/group-theory (so(4,1)
   Casimir + shift-charge algebra). VALUE EVEN IF KILL: names exactly why no dS number reaches I0.

D6 [GAP-1, needs-setup, MED]  Ghost-Dark-Matter abundance map (Lim-Sawicki-Vikman 1001.4634): compute
   Omega_dm(M, I0) in the framework's GC and confirm the structural d Omega_dm/dLambda = 0 AND map the
   M-window (LCDM-degenerate M>~1 eV vs the framework's M~0.04-1 eV). Both-ways: CONFIRMS the dust
   mechanism is real AND CONFIRMS the amount is free (banked, but this makes it a standalone runnable
   abundance calc with the literature's own scaling). KILL-direction = if any M-window is excluded by
   the framework's own clustering, that bounds mu. Tool: numpy.

D7 [GAP-2/5, ready-now, MED]  Kiritsis Cerenkov/dissipation bound on the framework's preferred frame.
   Kiritsis 1207.2325: a LV gravitational field generically radiates gravi-Cerenkov; compute whether
   the framework's s^TX SME background (banked ~8.7e-10) predicts a gravi-Cerenkov / dissipation rate
   above any bound (high-energy cosmic-ray gravi-Cerenkov bounds on s_munu). Both-ways: PASS = another
   gravity-sector bound the framework survives (adds to the SME ledger); KILL = a NEW live constraint
   tighter than s^TX. Tool: numpy + the known gravi-Cerenkov bound formula on s_munu.

================================================================================
BOTH-WAYS LEDGER (what each door most likely yields, stated honestly up front)
================================================================================
- D1 most likely PERMITS (Serra-Trombetta is a permissive finding; literature found no kill) -> a real
  consistency WIN, but a KILL of part of the AeST window is equally bankable. Either way it is the FIRST
  quantitative positivity test of the framework's P(X).
- D2/D3 most likely NULL on kappa (GAP-3 stays open; sequestering relaxes, Seraille's coeff is
  mechanism-dependent) -> CONFIRMS the quarantine. A coincidence of coefficients would be a real bridge.
- D4 is the live front: a NUMBER + a data status, w->-1-degenerate (do not manufacture a DESI "win").
- D5/D6 most likely CONFIRM I0/amount FREE (GAP-4 stays open) -> the value is in naming WHY.
- D7 most likely PASS (another SME-ledger bound survived) -> or a new live constraint.

QUARANTINE: nothing here asserts a0/Z/kappa/I0 derived. Penalize a manufactured bridge and a reflexive
dismissal EQUALLY. The highest-value doors are D1 (genuine consistency test, PASS or KILL both bankable),
D2 (cross-mechanism kappa check), and D4 (the live a0(z) front).
