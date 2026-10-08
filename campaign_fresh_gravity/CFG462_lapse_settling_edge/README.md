# CFG462: the khronon lapse does not make settling stop at ν = Ω_m/Ω_b. EXHAUSTION ONLY (FAIL); the energy sink is NOT SUPPLIED

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in 16518e951. The script is `cfg462_lapse_edge.py` and runs in about 4.5 minutes.
- Main run: exit 0, because controls K1–K5 pass.
- `CFG462_MUTATE=1` (a₀ → 2a₀ inside the lapse): exit 1. The teeth were detected, as designed.

κ = ½ is FITTED. Both footings are scored separately and never pooled. No dark-matter particle is added: the cold fluid's mass is still required, and its amount is an input. G9 stands. This is not "theory closed".

## The question

CFG461's lead (and item 1 of the 10-08 failure ledger): the settling temperature σ⁴ = G M_b a₀/4 holds exactly if settling stops where the law's boost equals Ω_m/Ω_b.
- That is g_N = ln²(1/(1−f_b)) a₀ = 0.0292 a₀, where the total field is 0.186 a₀.
- The radius is r_edge = 5.85 r_M, CFG424's zero-knob edge.

Does the khronon lapse (CFG373, the record's only zero-constant carrier of the local field) produce that stop, with no new constant and without the edge being put in by hand? And does the same field supply the energy sink CFG461's contraction needs?

## What was solved

**The lapse system was copied from CFG373:**
- the leaf-elliptic weak-field lapse, g = G(M_b + M_c)(<r)/r²;
- the kernel's mass-shell inverse g_N(g);
- the lapse-local target M_t[g](<r) = r²(g − g_N(g))/G.

ν_mono is scored. CFG373's own P2 closed form is reported alongside.

**Set-up:**
- The host is a Hernquist baryon profile (a = 0.3 r_M scored, a = 1 r_M reported). Wherever the fluid is settled, the lapse fixed point is the law's phantom, the SIS in the deep regime (K2).
- **Cold supply (scored, "CAT"):** the record's turnaround catchment. CFG118 gives 22.6 M_b of cold fluid inside r_ta (r_ta = 236 kpc at 10⁹ M☉, scaling as M^⅓).
- **Supply control ("SHARE"):** exactly the cosmic share, 5.364 M_b.

The SHARE run is a restatement, not a test. r_edge is defined as the radius where the phantom has used up exactly the cosmic share (T10 S6, CFG423), so any inside-out fill of that supply ends there. A no-flux edge has to appear when more fluid than that is available. On the record it is: CFG424 uses at most 30% of a catchment.

**Settling flows.** CFG373 fixes the target but not the dynamics. Four flows were declared, all scored, none dropped:
- **F-H:** the field energy of the mismatch (H⁻¹ norm).
- **F-2:** the L² norm of the density mismatch.
- **F-KL:** relative entropy, which is the T3/T10 JKO settling.
- **F-0:** the chassis as committed, which has no settling drive (CFG381).

Each of F-H, F-2 and F-KL is a mass-conserving gradient flow whose target is re-read from the lapse at every instant.

## Verdict table

Edges are given as log₁₀(r_e/r_edge), where r_edge = 5.8498 r_M. The six cells are canonical 10⁹, 10^10.5, 10^11.5, then alt in the same order.

| flow | locality of its drive | CAT (scored) | P1 | SHARE (control) | MUTATE shift (CAT) |
|---|---|---|---|---|---|
| F-H | **needs the baryons' own field g_b** (v = D[g_N(g) − g_b]) | 23.38 r_M, **+0.602** (all cells) | FAIL | 6.09 r_M, +0.018 (point mass: 5.8498, exact) | −0.149 |
| F-2 | lapse-local | 30.3 r_M, **+0.714** | FAIL | 7.99 r_M, +0.135 | −0.148 |
| F-KL | lapse-local | fills the catchment, +1.10 to +1.56 | FAIL | fills the catchment | 0 |
| F-0 | none (no drive) | stays at r_ta, +1.10 to +1.56 | FAIL | stays at R_vir, +0.13 to +0.59 | 0 |

**Lane verdict: EXHAUSTION ONLY (FAIL).**
- With the catchment supply, no flow stops at r_edge.
- The edge appears only as the exhaustion radius of exactly the cosmic share. It then appears only for F-H, which is the flow whose drive is not lapse-local.
- That is CFG423 / T10-S6 bookkeeping, not a lapse no-flux boundary.

**Sink: NOT SUPPLIED** (see below).

## What was found

1. **The lapse carries the law but has no feature at y_e.**
   - The carrier works on an extended host. With unlimited supply, the lapse fixed point equals the phantom to 5e-15 (ν_mono) and 9e-14 (P2). That is CFG373 G1, now numerical.
   - The lapse system contains only {G, a₀, kernel}. f_b is not in it, so nothing in it can place a stop at y_e(f_b).
   - Directly: in the state settled exactly to r_edge, with the catchment remainder outside, the lapse target just outside the edge is ρ_t[g]/ρ_c = 1.7–3.0. The lapse asks for *more* fluid beyond the edge.
   - No flow's flux vanishes there:
     - F-H flows inward at 1.0, 1.1 and 1.5 r_edge;
     - F-2 flows outward at the edge and inward beyond it;
     - F-KL pushes outward.
2. **With the catchment supply every flow settles past r_edge** (table above). The g_N at F-H's edge is 0.0018 a₀ against the target 0.029 a₀.
   - The f_b-test (the analogue of CFG461's c-test) gives d ln y_e/d ln f_b = **0** for every flow on CAT; a real ν = Ω_m/Ω_b edge needs 2.18.
   - Doubling the supply moves F-H's edge to 11.5 r_M (+0.29 dex). The edge is a supply-exhaustion radius.
3. **The edge only reappears with exactly the cosmic share (control K3).**
   - Point mass: 5.8498 r_M exactly. Hernquist a = 0.3: +0.018 dex in all six cells. Here f_b enters through the supply, so the f_b-test gives 2.02.
   - The lapse-local flows miss even then: F-2 by +0.135 dex, and F-KL fills the domain.
4. **The one flow that lands on the edge is not carried by the lapse.**
   - F-H's velocity is identically D[g_N(g) − g_b] (residual 7e-16).
   - It needs the baryons' own Newtonian field, or equivalently the fluid's own field: a second elliptic solve keyed to one species.
   - So the nonlocality of CFG60/CFG473 returns, with a G9 tension. CFG373's "no baryon-reading switch is needed" holds for the *target*, not for this settling drive.
5. **F-KL (the record's JKO settling) does not reproduce the law with the lapse-carried target** (post-run report, not a verdict input).
   - The target is self-referential: in a weak field the mass-shell inverse calls almost all enclosed mass phantom.
   - The equilibrium is a partial law that weakens outward: g/g_law falls from 0.96 to 0.67 over 2–20 r_M on CAT, and from 0.84 to 0.29 on SHARE. Its cold mass is spread over the catchment (r₉₀ = 57 r_M).
   - F-2 follows the law of ρ_b − μ, with its own edge. Only F-H realises the law exactly inside its edge.

## The energy sink (frozen line: some channel's capacity ≥ the requirement in all six cells)

- **Requirement.** CFG461's contraction factors are reproduced: R_vir/r_edge = 3.50 / 1.97 / 1.34 canonical, 3.85 / 2.16 / 1.47 alt (z_c = 1).
  - The energy to shed is 2.50 / 0.97 / 0.34 × the virial binding energy (toy): 8.7e48 / 1.1e51 / 1.7e52 J canonical.
  - The virial estimate with the Hernquist host gives 1.2e49 / 1.2e51 / 2.6e51 J (alt 1.4e49 / 1.5e51 / 1.3e52 J).
  - At z_c = 3 the massive end must *expand* (0.67 canonical, 0.74 alt), so it needs a source, not a sink.
- **Capacity of the same field:**
  - **The lapse constraint itself: 0.** Its field energy equals −W (K5, sympy), so contraction *releases* it. It is the energy source, not a sink.
  - **The α_c channel:** 3.2e-9 of the need.
  - **The K² channel with CFG381's gravitationally induced K:** 3e-24 to 1.5e-21.
- **Verdict: NOT SUPPLIED.** The direct fluid–khronon coupling (CFG381's +1 constant) would have to raise K above its gravitationally induced value by a factor of **2.6e10 to 2.3e17**. That is the coupling's required size over the window and the three galaxies.

## Couplings that had to be chosen (stated plainly)

- **The mobility D of every settling flow.** It is a rate constant with units of time: CFG381's direct fluid–khronon coupling, +1 constant. It does not move any edge (K4: D × 10 shifts the settled edge by 2e-16 dex). Its required size for the sink is the 2.6e10–2.3e17 enhancement of K above.
- **The settling functional itself** (H⁻¹, L² or KL) is a structural choice that CFG373 does not fix. All three were scored.
- **No constant or threshold was chosen to place an edge.** The edges come out of the supply (and, under F-0, out of the initial state).

## MUTATE (a₀ → 2a₀ inside the lapse; host and catchment held at their true values)

- Law-keyed edges move as predicted. F-H on CAT moves −0.149 dex and F-2 −0.148, against the predicted −0.1505. The K3 control moves −0.1505 for a point mass and −0.144 for Hernquist a = 0.3, and fails P1 against the true r_edge.
- F-KL and F-0 do not move: their edges are cosmological.
- No flow passes P1, so the run exits 1 as designed.
- **A coincidence was caught and is not a result.** Under MUTATE, F-2 with the share supply lands on the *true* r_edge (−0.008 dex), because its +0.135 dex miss is about the size of the √2 shift. It is a doubled-a₀ run scored against the true-a₀ edge, with the restatement supply.

## Controls

- **K1 PASS.** CFG373's identities hold symbolically (perfect square; the local target equals CFG44's; AQUAL flux). The ν_mono inverse round trip is accurate to 1e-15.
- **K2 PASS.** The lapse fixed point equals the phantom on Hernquist hosts, for both kernels.
- **K3 PASS.** This is the restatement control; it shows the gate can pass.
- **K4 PASS.** The time-dependent Lagrangian F-H run settles to the equilibrium edge to 2e-11 dex, and M_c(<r) matches to 2e-15.
- **K5 PASS.** Lapse field energy = −W (sympy).

## Disclosures (changes after the first output; none moves a verdict)

- **K4 failed in the first run because the integration span I picked (4e5/D, not frozen) was too short.** The outermost shells start at the catchment (~109 r_M) and drift in at ~1e-4 D. The inner shells had already converged (1.4e-5). The span was lengthened to 2e7/D; the criterion is unchanged.
- **The post-run report was added after the first run.** It gives the percentile radii, g/g_law and M_c/M_b of each equilibrium. It is labelled in the output and is not a verdict input.
- **My first printed reading of F-KL ("traces the baryons") was wrong.** That holds only asymptotically, where g ≪ [(1−λ)/λ] a₀. The numbers showed a partial law that weakens outward. The text is now computed from the numbers.
- The MUTATE coincidence above was noticed in the output and is reported here.

## Caveats

- Everything is spherical. The equilibria are of declared gradient flows; only F-H was also time-integrated.
- The catchment supply is CFG118's z = 0 turnaround for point cores (cold-only shells; 19.7–23.6 M_b for extended cores). Any supply well above 5.364 M_b gives the same verdict, because the edge tracks the supply.
- The flows are a declared family, not an exhaustive one. The structural fact behind the FAIL is general: f_b is not in the lapse system. So for any lapse-local flow, an edge at y_e can only come through the supply.
- The weak-field lapse absorbs the G_N renormalisation (a factor 1 + 1.6e-9 at most).
- The energy numbers are budgets: a toy truncated-SIS estimate plus a virial estimate. The law's target is not a Newtonian equilibrium (CFG472), so the final-state "virial" energy is approximate.
- The K² capacity uses CFG381's linearised induced-K formula with V = V_f.

## What this leaves (the exact gap, moved)

The missing ingredient is no longer "a carrier" (the lapse carries the target) and not a "stopping field" (the lapse has no f_b). It is on the **supply** side: why a galaxy settles the cold fluid that came with its present baryons, 5.364 M_b, and not the ~4× more its catchment holds.

**Untested hypothesis:** co-settling per Lagrangian shell. Only the cold fluid whose baryons reached the galaxy would settle.
- It would key settling to the baryons' accretion history, so it must be checked against G9 before it counts.
- What it predicts for baryon-depleted galaxies depends on whether the cold partners of ejected baryons stay settled. That was not computed here.

The energy sink still needs the +1 coupling, of the size given above.
