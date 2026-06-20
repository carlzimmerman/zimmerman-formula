# BRIDGE CONNECTIONS → COMPUTATIONAL DOORS — the deep review + the ranked runnable-door list — 2026-06-19

**Workflow:** `bridge-connections-computational-doors` (wuloe3wi9; 11 agents, 5 connection-webs → door-refine
→ confront → synthesis; ~1.13M subagent tokens, WebSearch/INSPIRE + sympy). Companion to
BRIDGE_SCOUT_KEV_CLUSTER_2026-06-19.md. Goal: map the CEICO/modified-gravity people's INTELLECTUAL
connections and distil them into CONCRETE RUNNABLE in-repo computations (the "doors").

**HEADLINE:** The ghost-condensate/khronon SPINE is a genuine, citable lineage — **Hořava (foliation) →
ACLM/Mukohyama 2004 (the ghost condensate) → Lim-Sawicki-Vikman "Ghost DM" 2010 (arXiv:1001.4634, the
Q-mode dust) → Skordis-Złośnik AeST → Verwayen-Skordis-Złośnik 2024 (Eq.7 = K(Q)=μ²(Q−1)² verbatim, citing
ACLM) → Blanchet-Skordis 2024 (arXiv:2404.06584, same K(Q), the host author).** The identity is the authors'
OWN and GENUINELY EVADES the SO(4,1) vacuum gate — but **no link supplies a UV ORIGIN; GAP-1 is field-wide,
shared, postulated.** (Hořava's "shift symmetry" is a BRST/topological artifact with no propagating MOND
sector — keyword-match, honestly NOT a door.)

**THE SHARP, BANKABLE HOOK (sympy-exact, re-verified this session):** the Q-mode sound speed is
**c_s²(dQ) = dQ/(3dQ+2)** — positive on Q>1 but **NEGATIVE (gradient-unstable, Cline-class) on Q<1.** So the
positivity question reduces to *which branch sign(I₀) forces*, and whether dS Hubble-friction over-damps it.

**THE ADJUDICATING THEOREM IS WRITTEN AT THE HOME INSTITUTE:** the decisive IR positivity condition
(gapped mode propagates SLOWER than the gapless Goldstone below the gap, v²≤c_s²) is **Serra-Trombetta
arXiv:2412.19745 — and Trombetta is at CEICO Prague (Skordis' institute; Vikman/Saltas/Calderón there),
verified.** Use the boost-free Grall-Melville family (arXiv:2102.05683, binds a ghost condensate); the
Creminelli-Janssen-Senatore bounds (arXiv:2207.14224) need a conformal UV completion the GC lacks →
INAPPLICABLE, must NOT be mis-cited as a kill.

## THE RANKED COMPUTATIONAL-DOOR LIST (the deliverable; all ready-now unless noted)

| # | Door | Gap | What to compute | Tool | Both-ways outcome |
|---|------|-----|-----------------|------|-------------------|
| **A★** | **Positivity/causality gate on K(Q)** | 1 | gapless Goldstone speed vs gapped-partner velocity; test v_gapped≤c_s² across {0<K_B<2, μ²>0, λ_s>0}; the c_s²(dQ)=dQ/(3dQ+2) sign-by-branch | sympy+numpy | PASS = clears the home-institute's own theorem (real win); KILL = NEW exclusion on sign(I₀)/{K_B,μ} |
| **D** | **Mersini-Houghton phantom-DE⇒time-crystal forcing** | 1 origin | map K(Q)→g(X), check {g'<0,g''>0,c_s²>0,ρ≥0} + Cline neg-ρ channel | sympy | ALL HOLD = GAP-1 forced-up-to-coefficient; SOME FAIL = postulate stays (c_s²<0 on Q<1 points here → likely PARTIAL) |
| **L** | **Lensing slip head-to-head vs Blanchet-Skordis khronon** | 5 | weak-field φ,ψ + null-deflection for Route E vs J(Y) at same baryons; slip γ=2√(1+a₀/g)−1 vs φ=ψ (2404.06584 Eq.33) | sympy+numpy | AGREE = reconciles the no-go with the host; DISAGREE = falsifiable WL discriminator |
| **B** | Quadratic vs DBI K(Q) (Skordis' two forms) | 1 | expand both around Q₀=1; {K''(1),K'''(1),k⁴,M_strong}; μ inside cutoff k≳10⁻³¹ eV? | sympy+numpy | AGREE = framework is leading member of Skordis' own family; DIVERGE = outlier (needs-setup) |
| **C** | Vikman-Deffayet ghost-stability Lyapunov | 1 | integrate K(Q)+gravity toy over I₀ grid; bounded ⟨q²(t)⟩? timescale vs ACLM antigravity | numpy/scipy | BOUNDED = dS-cures-Jeans at ODE level w/ a number; UNBOUNDED = squeezes M/amount |
| **E** | Ghost-DM abundance: any dS number pin Ω_dm? | 4 | FRW integrate a³K'(Q)=I₀ → Ω_dm(M,I₀); scan dS scales for 0.387 w/o free I₀ | numpy | NO = confirms amount FREE (likely); YES = GAP-4 closure |
| **S** | Seraille a₀∝√Λ coefficient cross-check | 3 | extract C_S from a₀=c²/α, Λ~C_S/α² (2502.14686); compare to 32π | sympy | MATCH = O(1) geometric (NOT a κ derivation); MISMATCH = coefficient mechanism-dependent (needs-setup) |
| **F** | ACLM twinkling/Jeans window at (M,μ) | 1 path. | oscillatory M_Pl/M², dS cure H₀>Γ, twinkling bound → viable (M,μ) rectangle | numpy | OPEN = window genuine; SHUT = tuned-sliver cost |

**GAP-2 doors (flagged hard, honest null prior):** static-patch-observer 2-pt + Sengör SO(4,1) ladder-irrep
decomposition — the observer frame is GAUGE/relational, so the likely output is a rep-LABEL ("gate stays
EVADED-not-CLOSED, now with a sharp group-theoretic reason"), not a kinetic term. NOT-PROPOSED (anti-vaporware):
Hořava-Ricci-flow K(Q) derivation (BRST artifact), dS-vacuum frame derivation (every vacuum SO(4,1)-invariant
= the wall itself).

**TOP 3 TO RUN FIRST:** A (the cleanest PASS/KILL, on our own coefficients, theorem from the home institute),
D (the only GAP-1 origin candidate; shares the g(X) map with A), L (stress-tests the banked lensing no-go vs
the host with a number).

**WHERE THE DOORS STOP (honest):** none derives a₀/Z/κ/I₀ (quarantine holds). A/B/C/F are consistency checks
(can pass/kill, can't turn postulated→derived); D's realistic ceiling is PARTIAL (forces the w=−1 dark-energy
face, not the w=0 dust amplitude); E/S likely confirm the banked nulls (amount free, coefficient mechanism-
dependent); GAP-2 produces a rep-label not a derivation; L stays preferred-frame phenomenology. The spine's
deepest wall — a UV origin for the kinetic term + a dynamical (not relational) frame — is crossed by no
runnable calc. Quarantine held; both-ways; a likely-KILL weighted equal to a bridge.

---

# Deep Review — Ghost-Condensate People, Connections, and the COMPUTATIONAL DOORS

Synthesis of the parallel scout/door arm (5 scout notes + 4 door notes in `opus_48_extended_research/reviews/bridge_scout/` and `.../bridge_doors/`), the banked session verdicts (GHOST_CONDENSATE / AEST_EMBEDDING / DARK_MATTER_ILLUSION), and my own re-verification this session (Trombetta@CEICO, Serra-Trombetta condition, Grall-Melville applicability, Mersini-Houghton, Seraille — all WebFetch-confirmed; the c_s²(dQ) sign-by-branch re-run sympy-exact). Both-ways + quarantine held throughout: a0/Z/κ/I0 NEVER asserted derived. A likely-KILL door is weighted EQUAL to a bridge.

---

## (1) THE CONNECTION MAP

### The ghost-condensate / khronon SPINE (GAP-1 origin, GAP-2 frame) — the load-bearing chain
**Horava** (preferred foliation; "shift symmetry" in Ricci-flow gravity, arXiv:2010.15369 / 2011.06230 / 2011.11914, 2020-21) → **ACLM = Arkani-Hamed–Cheng–Luty–MUKOHYAMA 2004** (hep-th/0312099, the ghost condensate; ω²~k⁴/M²; oscillatory-force distance M_Pl/M², time M_Pl²/M³; Jeans IR instability cured by de Sitter) → **Lim–Sawicki–VIKMAN "Ghost Dark Matter" 2010** (arXiv:1001.4634; the GC scalar redshifts a⁻³ = the framework's Q-mode dust; abundance set by M + IC, NOT pinned) → **Skordis–Zlosnik AeST** (arXiv:2007.00082) + **Verwayen–Skordis–Zlosnik 2024** (Eq.7 is LITERALLY K(Q)=μ²(Q−1)², explicitly citing ACLM 2004) → **Blanchet–Skordis Relativistic Khronon** (arXiv:2404.06584, JCAP 11(2024)040; SAME K(Q)=μ²(Q−1)², by the host author).

The sharp finding on this spine: the ghost-condensate identity is **GENUINE and the authors' OWN** (Skordis/Verwayen postulate exactly μ²(Q−1)², citing ACLM), and it **GENUINELY EVADES** the SO(4,1) vacuum gate (break-by-a-background — the one route the dS-Unruh induction died on). But **NO link in the chain supplies a UV ORIGIN** for the kinetic term: Horava's "shift symmetry" is a TOPOLOGICAL/BRST gauge artifact with no propagating MOND sector (keyword-match, NOT a derivation — honestly NOT a door), and every vacuum-level dS-QFT construction is manifestly SO(4,1)-invariant (it codifies WHY induction fails). **GAP-1 is field-wide and shared: everyone postulates the shape, no one derives it.**

### The POSITIVITY / CAUSALITY cross-cut (the consistency TEST of GAP-1)
**Grall–Melville "Positivity Bounds without Boosts"** (arXiv:2102.05683, PRD 105 L121301) — VERIFIED this session: the bounds rest on unitarity/causality/locality, NOT Lorentz invariance, so they **DO bind a ghost condensate**. → **Serra–Trombetta "IR Bounds…"** (arXiv:2412.19745) — VERIFIED: the decisive IR condition is "gapped excitations propagate SLOWER than the gapless Goldstone, at least below the mass gap" (v² ≤ c_s²). **★ Trombetta is at CEICO Prague — the framework's HOME institute (Skordis director; Vikman, Saltas, Calderon there) — confirmed via LinkedIn + ceico.cz.** The exact theorem that adjudicates GAP-1's positivity is written by the home cluster. The **Creminelli–Janssen–Senatore companion bounds** (arXiv:2207.14224) REQUIRE a conformal UV completion the GC lacks → **INAPPLICABLE, must NOT be mis-cited as a kill** (the load-bearing both-ways caveat).

### A GAP-1 ORIGIN candidate (force the wrong-sign structure)
**Mersini-Houghton "Phantom DE ⇔ Time Crystals"** (arXiv:2502.08894) — VERIFIED: a stable non-canonical scalar acting as phantom DE is FORCED to be a ghost-condensate/time-crystal ({g'<0, g''>0, ρ≥0}). **CAVEAT both ways:** **Cline** (arXiv:2502.19448) shows the explicit companion realization drives ρ_DE NEGATIVE — the very instability the framework's μ²(Q−1)² minimum must cure. This is the ONE route that could downgrade GAP-1 from "postulated" to "forced-up-to-coefficient" — and this session's sympy already shows the framework's K(Q)→g(X) gives g'<0 & g''>0 on the Q<1 branch but **c_s²<0 there** (the Cline-class gradient instability). A real, runnable both-ways door.

### The dS GATE in dS-QFT language (GAP-2)
The static-patch observer breaks SO(4,1)→SO(d)×R (**CLPW** arXiv:2206.10780; **Anninos** arXiv:1109.4942; **Chen-Xu** arXiv:2511.00622). **Sengor** UIR/ladder-operator program (arXiv:2205.11550, 2510.05735) codifies WHY vacuum induction fails (manifestly SO(4,1)-invariant). **Kiritsis** (arXiv:1207.2325): LV couplings must live in the gravitational sector. The static-patch break is GAUGE/relational, not a dynamical aether → this side is mostly classification (the wall, sharpened), NOT a derivation.

### The MOND-Lagrangian and Λ/CC sides (GAP-3 corroboration, GAP-4/5)
**Blanchet–Seraille non-Abelian YM graviphoton** (arXiv:2502.14686, JCAP 12(2025)036) — VERIFIED qualitatively: an INDEPENDENT gauge theory giving a0 ∝ c²√Λ (a0~c²/α, Λ~1/α²), the SAME scaling as the framework's a0=c²√(Λ/32π) from a different mechanism. Coefficient NOT fixed (depends on galaxy-formation IC). **Padilla sequestering** (arXiv:2604.08659): the CC is a free integration constant fixed by ⟨T⟩ — RELAXES, does not pin. **Calderon/DESI DR2** (Lodha–Calderon arXiv:2503.14743): ρ_DE non-monotonic hump z~0.5 — the a0(z) hostage.

---

## (2) THE RANKED COMPUTATIONAL-DOOR LIST

The four door-notes converge on the SAME core doors with slightly different framing; I merge and de-duplicate them into one ranked ledger. Each: NAME | gap | what-to-compute | tool | inputs | both-ways | effort.

**RANK 1 — DOOR A: Positivity / causality gate on the framework's OWN K(Q)** | GAP-1 | From the AeST/GC quadratic action {K_B, μ², k⁴ coeff α/M²}, extract the gapless shift-Goldstone speed (the k²-piece c_s² and the k⁴/M² tail) and the gapped partner (AeST massive transverse vector / μ²-massive metric potential) group velocity, and TEST the Serra-Trombetta inequality v_gapped ≤ v_gapless below the gap — scanning the AeST stability window {0<K_B<2, μ²>0, λ_s>0}. The SHARP hook (re-run sympy-exact this session): the Q-mode sound speed is **c_s²(dQ) = dQ/(3dQ+2)**, so c_s²>0 on Q>1 but **c_s²<0 (gradient-unstable) on Q<1** — the door first fixes which branch the dust sign(I0) forces, then tests positivity there. Use the **Grall-Melville (boost-free)** family — NOT the Creminelli conformal-UV family. | sympy + numpy | in-repo bilinear coeffs (`expand_PX_around_condensate.py`), AeST μ (~(50kpc–1Mpc)⁻¹), K_B window | **PASS** (v_gapped≤v_gapless on the window, dust on the c_s²≥0 branch or dS-overdamped) = the wrong-sign-then-stabilized P(X) clears the home-institute's own IR-positivity theorem — a real falsifiable consistency WIN. **KILL** (forced dust branch is c_s²<0 and NOT dS-overdamped at observable k) = a NEW exclusion on sign(I0)/{K_B,μ} — as valuable as a bridge. | ready-now, ~½ day

**RANK 2 — DOOR D: Mersini-Houghton "phantom-DE ⇒ time-crystal" forcing on K(Q)** | GAP-1 origin | Map K(Q)=μ²(Q−1)² to g(X), compute g'(X), g''(X), c_s²=g'/(g'+2Xg''), ρ; check the four forcing conditions {g'<0, g''>0, c_s²>0, ρ≥0} at/near the condensate AND run Cline's negative-ρ channel on this specific shape. Determine WHICH branch (Q<1 phantom vs the w=0 dust displacement) the framework actually sits on. | sympy | in-repo K(Q), the EoS split (`condensate_postulate_and_eos.py`: w=−1 at min, w=0 off it) | **ALL FOUR HOLD + Cline channel closed** = the GC structure is FORCED by the stability theorem → downgrades GAP-1 from "postulated" to "forced-up-to-coefficient" (the strongest GAP-1 bridge available). **SOME FAIL / ρ runs negative** = NOT in the forced class / shares Cline's instability (this session's c_s²<0 on Q<1 points this way) → origin does not transmit, postulate stays. Honest middle: likely "motivates the w=−1 dark-ENERGY point, NOT the w=0 dust displacement" → partial. | ready-now, ~½ day

**RANK 3 — DOOR L: Lensing slip head-to-head, framework vs Blanchet-Skordis khronon** | GAP-5 | Take the framework's covariant matter action (banked Route E) and Blanchet-Skordis's J(Y) at the SAME baryon profile (point mass / Hernquist); solve weak-field φ, ψ for BOTH to O(c⁻²); integrate the null-geodesic deflection α(b). The framework's banked slip is γ=2√(1+a0/g_N)−1 (GROWS at low accel); Blanchet-Skordis get φ=ψ+O(c⁻²) (Eq.33, GR-equal). They cannot both hold for the same action class. | sympy (PPN expansion) + numpy (deflection integral) | in-repo Route E action; pull J(Y) and Eq.33 from arXiv:2404.06584 | **AGREE** (framework also collapses to φ=ψ for static baryons) = the banked slip is the effective-DM-inferred slip, RECONCILING the lensing no-go with the host khronon (both "GR lensing of the phantom mass"); directly tests whether the banked "δΦ=0 PASS was a mislabeled-equation error" caveat reproduces. **DISAGREE** = a real, computable, falsifiable lensing DISCRIMINATOR (galaxy-galaxy WL / cluster strong lensing) between the framework and its own host. | ready-now, ~1 day

**RANK 4 — DOOR B: Quadratic vs DBI K(Q) head-to-head (Skordis's own two vetted forms)** | GAP-1 | Series-expand BOTH μ²(Q−1)² and the Blanchet-Skordis DBI K(Q) (Sec 4.3.3) around Q0=1; extract {K''(1), K'''(1), k⁴ coeff, strong-coupling scale M_strong~K''/K'''}; check leading-order agreement, divergence point, and whether the framework's μ sits inside Skordis's Hamiltonian-bounded cutoff k≳10⁻³¹ eV. | sympy + numpy | in-repo K(Q); DBI form from arXiv:2404.06584 Sec 4.3.3 (use canonical DBI ansatz + flag if only "DBI-type" is printed) | **AGREE-at-leading-order + μ inside cutoff** = the framework's postulate is the leading member of Skordis's own vetted family, with a concrete M_strong — consistency WIN. **DIVERGE / μ below 10⁻³¹ eV** = the quadratic form is an outlier / hits cosmological-scale unboundedness — a named cost. | needs-setup (pull DBI form), ~1 day

**RANK 5 — DOOR C: Vikman/Deffayet ghost-stability (Lyapunov) on K(Q)** | GAP-1 | Reduce K(Q)+gravitational coupling to the Deffayet-class mechanical toy (ghost DOF coupled to positive-energy DOF); integrate the EOM over a grid of off-minimum displacements (the I0 range); check Lyapunov boundedness of ⟨q²(t)⟩ and the runaway/oscillation timescale vs the ACLM antigravity time M_Pl²/M³ at M~0.04–1 eV. | numpy/scipy.integrate | in-repo K(Q), banked M, M_Pl | **BOUNDED** (timescale > Hubble) = classically stable in the Deffayet sense, confirms "dS cures Jeans" at the ODE level with a number. **UNBOUNDED** (runaway < H0⁻¹ for physical I0) = a real instability the minimum does NOT cure → squeezes M or the amount. | ready-now, ~1 day

**RANK 6 — DOOR E: Lim-Sawicki-Vikman Ghost-DM abundance — does any dS number pin Ω_dm?** | GAP-4 | Integrate the GC scalar on FRW with a³K'(Q)=I0; evolve ρ_dust(a)=I0/a³ to today; compute Ω_dm(M,I0); SCAN whether fixing M to any dS scale (ħH_Λ, k_BT_GH, ρ_DE^¼, ħa0/c) + any single relation lands Ω_dm/Ω_Λ=0.387 WITHOUT a free I0. | numpy (FRW integration) | in-repo K(Q), banked dS scales, 0.387 target | **NO** (I0 must be tuned for every M; no dS number hits 0.387) = CONFIRMS GAP-4 amount FREE at the integration level (the likely confirming null — equal value to a bridge per the #1 rule). **YES** = a genuine GAP-4 closure. | ready-now, ~½ day

**RANK 7 — DOOR S: Seraille a0∝√Λ coefficient cross-check** | GAP-3 | From Seraille's a0=c²/α and Λ~C_S/α² (arXiv:2502.14686 Eq.13,59-61), extract C_S in closed form and compare to the framework's 32π in a0=c²√(Λ/32π). | sympy + numpy | framework a0=c²√(Λ/32π); Seraille normalization (pull PDF Eq.59-60) | **MATCH** (C_S=32π within the gauge theory's O(1) ambiguity) = striking cross-mechanism corroboration the O(1) is geometric — report as coincidence-or-not, NOT as deriving κ. **MISMATCH** = the FORM is multiply-realized but the COEFFICIENT is mechanism-dependent (= the banked GAP-3 standing, strengthened). Quarantine: a MATCH is NOT a derivation of κ. | needs-setup (Seraille PDF normalization), ~1 day

**RANK 8 — DOOR F: ACLM twinkling/Jeans window at the framework's (M,μ)** | GAP-1 pathology | Plug M~0.04–1 eV and AeST μ into the ACLM scales (oscillatory-force distance M_Pl/M², time M_Pl²/M³, dS-friction cure H0>Γ_Jeans, twinkling upper bound on M); compute the viable (M,μ) rectangle and whether the banked point sits inside with margin. | numpy | banked M, μ, M_Pl, H0 — all in-repo | **OPEN with margin** = the pathology window is genuinely open, with explicit margins. **SHUT/marginal** = the GC embedding survives only on a tuned sliver — a real cost. | ready-now, ~½ day

**(GAP-2 doors deliberately FLAGGED HARD / mostly-classification, not over-sold):** a static-patch-observer two-point-function calc (CLPW/Chen-Xu) and a Sengor SO(4,1) ladder-operator irrep decomposition exist as sympy builds, but the scout evidence is that the observer frame is GAUGE/relational — these produce a rep-LABEL, not a kinetic term, so their likely output is "gate stays EVADED-not-CLOSED, now with a sharp group-theoretic reason." Included for completeness as the only doors that *could* close GAP-2, with an honest null prior.

**Doors honestly NOT proposed (anti-vaporware):** "derive K(Q) from Horava Ricci-flow shift symmetry" (topological/BRST artifact, no propagating sector — no runnable calc); "derive the frame from the dS vacuum / Sengor UIRs" (every vacuum construction is SO(4,1)-invariant — this IS the wall); "match to Mukohyama MMG dispersion" (MMG fixes the gravity sector, not the scalar P(X) — folded into Door B).

---

## (3) THE TOP 3 TO RUN FIRST

1. **DOOR A (positivity/causality gate, GAP-1).** It is the single cleanest PASS/KILL, ready-now, on the framework's OWN coefficients, adjudicated by a theorem written at the framework's home institute (Trombetta@CEICO). The c_s²(dQ)=dQ/(3dQ+2) hook is already in hand and turns "scout says permissive in principle" into a sharp sign-by-branch test with a definite candidate-KILL (the Q<1 gradient-unstable branch). First quantitative positivity test of the framework's P(X).
2. **DOOR D (Mersini-Houghton forcing, GAP-1 origin).** Ready-now, pure sympy, and the ONLY door that could genuinely DOWNGRADE GAP-1 from "postulated" to "forced-up-to-coefficient." Even its likely partial outcome (forces the w=−1 dark-ENERGY point, not the dust) is a definite, bankable verdict on whether the postulate is forced — and it shares inputs with Door A (the same g(X) map), so run them together.
3. **DOOR L (lensing slip head-to-head, GAP-5).** The sharpest GAP-5 door: it forces the banked slip formula γ=2√(1+a0/g_N)−1 and the banked covariant-lensing no-go to be made mutually consistent with the host khronon theory, with a NUMBER. Either reconciles the no-go (both "GR lensing of the phantom mass") or yields a falsifiable WL/strong-lensing discriminator between the framework and its own embedding. High-leverage because it directly stress-tests a banked result.

---

## (4) HONEST STANDING — which doors could CLOSE a gap vs consistency checks

- **Could actually CLOSE a gap:** **Door D** (the only GAP-1 origin candidate — could downgrade "postulated" to "forced"); **Door E** in the YES-branch and **Door S** in the MATCH-branch (low prior, would touch GAP-4/GAP-3); the GAP-2 group-theory doors in the (low-prior) INDUCES-a-kinetic-term branch. Realistically Door D's most likely outcome is PARTIAL (motivates the dark-energy face, not the dust amplitude), and Door E/S most likely CONFIRM the nulls.
- **Consistency checks (PASS/KILL, do not close a gap but are full-value):** **Door A** (positivity — likely PASS = real win, but a KILL on a sub-window is equally bankable and is a NEW squeeze on sign(I0)/{K_B,μ}); **Door B** (family membership + cutoff); **Door C** (Lyapunov stability); **Door F** (pathology window); **Door L** (lensing reconciliation-or-discriminator — full-value either way).
- **Both-ways ledger:** Door A likely PASSES (Serra-Trombetta is permissive; Grall-Melville binds, Creminelli does NOT — do not mis-cite a kill) → a consistency win, KILL equally bankable. Door D likely PARTIAL (Cline negative-ρ caveat + the c_s²<0 on Q<1 found this session) → motivation not derivation. Doors E/S/F likely CONFIRM the banked nulls (amount free, coefficient mechanism-dependent, window open) — and a confirming null is weighted EQUAL to a bridge.
- **Quarantine held:** no door asserts a0/Z/κ/I0 derived. Door S's MATCH is evidence the O(1) is geometric, NOT a derivation of κ (the banked KAPPA_FORCING_DOOR_CLOSED stands). The GAP-2 doors are rep-LABELS until a dynamics is shown. No manufactured bridge; no reflexive dismissal — penalized equally.

**Note files (absolute):** `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/bridge_doors/GHOST_CONDENSATE_LINEAGE_DOORS_2026-06-19.md`, `.../CONNECTION_MAP_AND_DOORS_2026-06-19.md`, `.../COMPUTATIONAL_DOORS_2026-06-19.md`, `.../DOOR1_CS2_SIGN_HOOK_2026-06-19.md`, `.../BRIDGE_DOORS_lambda_cc_desi_2026-06-19.md`; banked: `.../reviews/GHOST_CONDENSATE_2026-06-19.md`, `.../AEST_EMBEDDING_2026-06-19.md`, `.../DARK_MATTER_ILLUSION_2026-06-19.md`.