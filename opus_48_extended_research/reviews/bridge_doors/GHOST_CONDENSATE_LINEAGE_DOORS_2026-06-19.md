# Ghost-Condensate Lineage — Connection Map + COMPUTATIONAL DOORS (GAP-1/2 spine)
Date: 2026-06-19. Topic: web "ghost_condensate_lineage". Both-ways + quarantine (a0/Z/kappa/I0 NEVER
asserted derived). DM-particle people skipped per Carl's ask.

This note turns the verified people/connection web (the parallel scouts mapped it; I re-verified the
load-bearing technical conditions by WebFetch this session) into CONCRETE RUNNABLE computational doors —
each a sympy/numpy calc with a definite PASS/KILL or NUMBER, tied to a person + a gap + a both-ways outcome.
A door that is "read more papers" does NOT count and is not listed here.

================================================================================
## THE CONNECTION CHAIN (verified this session + by the bridge_scout arm)
================================================================================

Horava (preferred foliation; Ricci-flow "shift symmetry" 2020-21 = arXiv:2010.15369/2011.06230/2011.11914)
  --[shift symmetry = the GC time-translation symmetry, BUT Horava's recent shift is a TOPOLOGICAL/BRST
     gauge artifact, NO propagating MOND sector -> tangential, NOT a UV origin]-->
ACLM / Arkani-Hamed–Cheng–Luty–MUKOHYAMA 2004 (hep-th/0312099, the ghost condensate; omega^2 ~ k^4/M^2;
  oscillatory-force distance scale M_Pl/M^2, time scale M_Pl^2/M^3; Jeans IR instability cured by dS)
  --[Mukohyama = the M in ACLM; ghost-condensate-AS-dark-matter; Minimal Modified Gravity (MMG)]-->
Lim–Sawicki–VIKMAN "Ghost Dark Matter" 2010 (arXiv:1001.4634; GC scalar -> a^-3 cold dust = the Q-mode;
  abundance set by M + IC, M >~ 1 eV (LSS pushes >~10 eV) -> CONFIRMS GAP-4 amount FREE)
  --[Vikman = CEICO k-essence/derivative-VEV/time-crystal authority; "Imperfect Dark Matter" 1412.7136]-->
Mersini-Houghton phantom-DE => time-crystal 2502.08894 (g'<0, g''>0, rho>=0 -> FORCES GC structure; a
  near-theorem candidate ORIGIN for P(X) — but Cline 2502.19448 shows the explicit realization drives
  rho_DE NEGATIVE = the very instability the framework's mu^2(Q-1)^2 minimum must cure)
  --[the AeST identification]-->
Verwayen–SKORDIS–Zlosnik 2024 (arXiv:2404.06584/2404.06584 Eq.7) + Blanchet-Skordis Khronon
  (arXiv:2404.06584, JCAP 11(2024)040): K(Q)=mu^2(Q-1)^2 LITERALLY, explicitly citing ACLM 2004, PLUS a
  vetted DBI alternative K(Q) (Sec 4.3.3). mu = inverse length; Hamiltonian bounded for k > ~10^-31 eV.

POSITIVITY/CAUSALITY cross-cut (the consistency test of GAP-1):
  Grall–Melville "Positivity Bounds without Boosts" 2102.05683 (PRD 105 L121301) — bounds that DO apply
    to a GC (no LI UV completion required).
  Serra–Trombetta 2412.19745 — the IR-side decisive condition: PERMISSIVE, with a concrete kinematic
    check — GAPPED excitations must propagate SLOWER than the GAPLESS Goldstone below the mass gap.
  Creminelli–Janssen–Senatore 2207.14224 — companion bounds but REQUIRE a CONFORMAL UV completion ->
    INAPPLICABLE to the GC (must NOT be mis-cited as a kill).

================================================================================
## WHAT IS ALREADY DONE (do not re-bank) — ghost_condensate/ scripts, all exit 0
================================================================================
- expand_PX_around_condensate.py: P(X) bilinear coefficients PROVEN — time-kinetic = P'(X0)+2 X0 P''(X0),
  spatial-grad = -P'(X0); at P'(X0)=0 the ordinary (grad pi)^2 VANISHES, time-kinetic = 2 X0 P''(X0)>0,
  leaving omega^2 ~ k^4/M^2. This is the FOUNDATION every door below builds on.
- map_aest_to_ghost.py: K(Q)=mu^2(Q-1)^2 minimum at Q0=1, K''(1)=2mu^2>0, a^3 K'(Q)=I0 -> dQ~a^-3 dust.
- The verdict: EVADES the SO(4,1) vacuum gate (proven, symmetry-theorem level); does NOT DERIVE (P(X) shape
  postulated, relocated one-for-one); amount I0 FREE. The doors below are the NEXT calcs past this verdict.

================================================================================
## THE COMPUTATIONAL DOORS (calc + tool + inputs + both-ways outcome)
================================================================================

### DOOR A — Serra-Trombetta positivity gate on the framework's OWN K(Q): PASS or KILL
GAP-1. Person: Serra-Trombetta (2412.19745) + Grall-Melville (2102.05683). Tool: sympy + numpy.
WHAT: The framework's Q-sector has a gapped radial mode (mass ~mu, the Psi mass term) and a gapless
shift-Goldstone (the pi with omega^2~k^4/M^2). Serra-Trombetta's PERMISSIVE bound is a *condition*: the
gapped mode's low-k group velocity must be <= the gapless mode's. COMPUTE both dispersion relations from
the AeST/GC quadratic action {K_B, mu^2, the k^4 coefficient alpha/M^2}, extract v_gapped(k->0) and
v_gapless(k), and CHECK the inequality v_gapped <= v_gapless across the AeST stability window {0<K_B<2,
mu^2>0, lambda_s>0}.
INPUTS: in-repo — the bilinear coefficients from expand_PX_around_condensate.py + the AeST mass term mu
(banked ~(50 kpc-1 Mpc)^-1) + K_B window. NO external pull needed.
BOTH-WAYS: PASS (v_gapped <= v_gapless on the whole window) = the framework's P(X) survives the strongest
applicable boost-broken positivity bound -> a genuine, falsifiable consistency WIN (the bound is real and
the framework passes it). KILL (the inequality is VIOLATED somewhere in the window) = positivity EXCLUDES
the framework's wrong-sign-then-stabilized P(X) on that sub-window -> squeezes {K_B,mu} or kills the form.
A KILL here is as valuable as a bridge. FEASIBILITY: ready-now. IMPACT: high (this is THE consistency test
of GAP-1, and it has a definite numeric output).

### DOOR B — Quadratic vs DBI K(Q) head-to-head: does the framework's mu^2(Q-1)^2 sit on the SAME
dispersion/stability locus as Skordis's own vetted DBI form?
GAP-1. Person: Blanchet-Skordis (2404.06584). Tool: sympy (series-expand both K's around Q0=1) + numpy.
WHAT: Skordis's own paper offers TWO vetted kinetic functions — quadratic mu^2(Q-1)^2 (= the framework's)
and a DBI form (Sec 4.3.3). Expand BOTH to bilinear order around the condensate Q0=1, extract {K''(1),
K'''(1), k^4 coefficient}, and compute (i) whether they agree at leading order (they must: both are
ghost-condensate minima), (ii) where they DIVERGE (the K''' / cubic-interaction + the strong-coupling scale
M_strong ~ K''(1)/K'''(1)). Then check the framework's quadratic K against the Hamiltonian-bounded cutoff
Skordis reports (k > ~10^-31 eV) by plugging the framework's mu.
INPUTS: K(Q)=mu^2(Q-1)^2 (in-repo) + the DBI form (pull the explicit Sec-4.3.3 expression from 2404.06584;
if only "DBI-type" is given, use the canonical DBI K(Q)=mu^2(1-sqrt(1-(Q-1)^2/Q*^2))-type ansatz and note
the assumption). NO data needed.
BOTH-WAYS: AGREE-at-leading-order + framework's mu inside the bounded cutoff = the framework's postulated
form is the leading member of Skordis's own vetted family, strong-coupling scale computed -> consistency
WIN + a concrete M_strong number. DIVERGE-badly OR framework mu BELOW the 10^-31 eV cutoff = the quadratic
form is an outlier / hits the cosmological-scale unboundedness Skordis flags -> a real cost, names the
cutoff the framework must respect. FEASIBILITY: needs-setup (pull DBI form). IMPACT: high.

### DOOR C — Vikman / Deffayet ghost-stability CRITERION applied to the framework's K(Q): is the
wrong-sign-stabilized mode CLASSICALLY + (toy-)QUANTUM stable, or does it fail Lyapunov boundedness?
GAP-1. Person: Vikman/Deffayet (2305.09631 classical Lyapunov; 2604.21823 unitary quantum stable ghost).
Tool: numpy ODE integration (scipy.integrate) of the reduced mechanical model.
WHAT: Reduce the framework's K(Q)=mu^2(Q-1)^2 + the gravitational coupling to the Deffayet-class mechanical
toy (a "ghost" DOF polynomially coupled to a positive-energy DOF), and NUMERICALLY integrate the EOM for a
grid of initial displacements off Q0=1 (= the off-minimum I0). CHECK Lyapunov boundedness (does <q^2(t)>
stay bounded, per 2305.09631?) and measure the runaway/oscillation timescale. Cross-check against the ACLM
analytic antigravity timescale M_Pl^2/M^3 and distance M_Pl/M^2 at the framework's M~0.04-1 eV.
INPUTS: in-repo K(Q), banked M~0.04-1 eV, M_Pl. NO external data.
BOTH-WAYS: BOUNDED (orbits stay bounded for the physical I0 range, timescale > Hubble) = the framework's
ghost mode is classically stable in the Deffayet sense AND the Jeans instability is dS-slow -> confirms the
banked "dS cures Jeans" at the ODE level with a number. UNBOUNDED (runaway faster than H_0^-1 for physical
I0) = a real instability the mu^2(Q-1)^2 minimum does NOT cure -> squeezes M or the amount. FEASIBILITY:
ready-now. IMPACT: medium-high (turns the banked "non-fatal pathology" claim into a checked number).

### DOOR D — Mersini-Houghton "phantom-DE => time-crystal" near-theorem: do the framework's K(Q) coefficients
SATISFY the {g'<0, g''>0, c_s^2>0, rho>=0} forcing conditions — i.e. is the GC structure FORCED for it?
GAP-1 (origin). Person: Mersini-Houghton (2502.08894) + Cline counter (2502.19448). Tool: sympy.
WHAT: Mersini-Houghton claim ANY stable phantom-DE non-canonical scalar with {g'(X)<0, g''(X)>0, rho>=0}
is FORCED to be a time-crystal (GC) breaking time-translation. Map the framework's K(Q)=mu^2(Q-1)^2 (in the
X=Qdot^2/2 variable) to g(X), compute g'(X), g''(X), the sound speed c_s^2 = g'/(g'+2X g''), and the energy
density rho, and CHECK the four conditions hold at/near the condensate. Then check Cline's instability
direction (does rho_DE run NEGATIVE for this specific K?).
INPUTS: in-repo K(Q). Map to (g, X). NO data.
BOTH-WAYS: ALL FOUR HOLD (and Cline's negative-rho channel is closed for mu^2(Q-1)^2 specifically) = the
framework's GC structure is FORCED by the phantom-DE stability theorem, a near-origin for GAP-1 (the kinetic
SHAPE is no longer arbitrary — it is the unique stable phantom-DE form) -> the strongest GAP-1 bridge
available. SOME CONDITION FAILS / rho runs negative (Cline) = the framework's K is NOT in the
Mersini-Houghton forced class, or shares the Cline instability -> the "time-crystal forces the GC" origin
does NOT transmit, postulate stays. FEASIBILITY: ready-now. IMPACT: high (this is the one route that could
DOWNGRADE GAP-1 from "postulated" to "forced-up-to-coefficient").

### DOOR E — Lim-Sawicki-Vikman "Ghost Dark Matter" abundance: numerically reproduce Omega_dm from
(M, I0) and check whether ANY dS/Lambda number pins it (GAP-4), or it stays a free IC.
GAP-4 (amount). Person: Lim-Sawicki-Vikman (1001.4634). Tool: numpy (background FRW integration).
WHAT: Integrate the GC scalar on an FRW background with the shift current a^3 K'(Q)=I0, evolve
rho_dust(a)=I0/a^3 + corrections from matter-radiation through today, and compute Omega_dm(M, I0). Then
SCAN whether fixing M to any dS scale (hbar H_Lambda, k_B T_GH, rho_DE^1/4, hbar a0/c) + any
single-parameter relation lands Omega_dm/Omega_Lambda = 0.387 WITHOUT a free I0. This is the field-theory
restatement of the banked dK'/dLambda=0 orthogonality, made numerical.
INPUTS: in-repo K(Q), banked dS scales, Omega_dm/Omega_Lambda target. NO external data.
BOTH-WAYS: NO (I0 must be tuned for every M; no dS number hits 0.387) = CONFIRMS GAP-4 amount FREE at the
background-integration level (the honest expected outcome — and a KILL of "amount is pinned" is exactly as
valuable as a bridge). YES (some M + a fixed relation gives 0.387 with I0 not free) = a genuine GAP-4
closure. FEASIBILITY: ready-now. IMPACT: medium (most likely a confirming null, but a definite one).

### DOOR F — ACLM "twinkling"/oscillatory-force + Jeans bound numerically at the framework's M: is the
viable window {M, mu} actually OPEN, or squeezed shut?
GAP-1 pathology / GAP-5-adjacent. Person: ACLM (hep-th/0312099) + Mukohyama MMG. Tool: numpy.
WHAT: Plug the framework's M~0.04-1 eV and the AeST mu into the ACLM analytic scales: oscillatory-force
onset distance M_Pl/M^2, time scale M_Pl^2/M^3, the dS Hubble-friction cure condition H_0 > Gamma_Jeans,
and the twinkling/caustic upper bound on M. Compute the actual viable (M, mu) rectangle and report its
area / whether the framework's banked point sits inside it with margin.
INPUTS: banked M, mu, M_Pl, H_0 — all in-repo. NO external data.
BOTH-WAYS: OPEN with margin (framework's point inside, oscillatory range > galaxy, Jeans slower than
Hubble, M below twinkling) = the pathology window is genuinely open, with explicit margins -> confirms
banked "viable window exists" with numbers. SHUT/marginal (no M satisfies all simultaneously, or only a
fine-tuned sliver) = a real cost -> the GC embedding survives only on a tuned sliver. FEASIBILITY:
ready-now. IMPACT: medium.

================================================================================
## DOORS DELIBERATELY NOT PROPOSED (and why — anti-vaporware)
================================================================================
- "Derive K(Q) from Horava Ricci-flow shift symmetry": Horava's recent shift symmetry is a TOPOLOGICAL/BRST
  gauge artifact (no propagating sector) -> there is NO runnable calc that bridges it. Verified tangential.
  Honestly NOT a door.
- "Derive the frame from the dS vacuum / Sengor UIRs / Kiritsis hidden sector": every vacuum-level dS-QFT
  construction is manifestly SO(4,1)-INVARIANT (it codifies WHY induction fails) -> no calc closes the gate
  from the vacuum side. The static-patch-observer break (SO(4,1)->SO(d)xR) is GAUGE/relational, not a
  dynamical-field derivation -> no runnable derivation-door. Honestly NOT a door (it is the wall, sharpened).
- "Match to Mukohyama MMG dispersion": MMG fixes the gravity sector to 2 dof by Hamiltonian constraints; it
  does NOT supply the scalar P(X) shape -> a consistency check, not a derivation; folded into Door B's
  family rather than over-sold as its own bridge.

================================================================================
## BOTH-WAYS / QUARANTINE
================================================================================
- The doors are split by likely outcome: Door A could KILL (positivity), Door D could BRIDGE (forced GC),
  Door E is a likely CONFIRMING NULL (amount free) — all three reported at equal value, per the #1 rule.
- a0, Z, kappa, I0 never asserted derived anywhere. No door asserts a derivation as its premise; each has a
  definite both-ways output.
- The connection web is the scouts' (verified); the DOORS (the runnable calcs) are this note's contribution.
