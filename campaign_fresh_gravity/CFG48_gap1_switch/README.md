# CFG48 -- Gap 1 (the switch as a legal action term): a scoped no-go, one stability result that overturns an expectation, and what is left

kappa = 1/2 is FITTED. Both a0 footings apply (scripts use the canonical 9.3603e-11; DE12's layers carry both). Nothing here says the theory is closed, and no gate in `closure_map/GATES.md` was moved or touched. Nothing in the repository outside this directory was edited; nothing was committed.

**Bottom line.** No construction I could write passes all of the frozen action-level gates for a bound-only, top-level-owned, baryon-reading, covariant, source-confined switch (gates GA-GG in `GATES_FROZEN.md`). Four separate obstructions, each with exact hypotheses below:
1. **Gauss (lead 1, verified).** A gate multiplying a shift-symmetric MOND field whose only source is the baryons gives M_dyn = M_b exactly beyond the edge; B's target is M_b sqrt(1+x_e^2) (15-33 M_b), so the phantom inside the edge becomes a negative shell of 1.4e13-3.2e11 Msun. The form that does keep the mass (gate on the phantom DENSITY, not its flux) is not the Euler-Lagrange system of any Lagrangian in those fields (Helmholtz test fails, proportional to W').
2. **History (verified).** Ownership (accreted satellite vs formed-embedded tidal dwarf) is not a function of the baryon state, and a history variable placed inside an action makes the Euler-Lagrange residual at t depend on the future trajectory. The only causal carrier is a prescribed label, i.e. ownership as initial data.
3. **Exchange (task 3, verified).** CFG44's enclosed-mass energy exchange, written as a bilocal action term, reacts on the baryons outward with 0.06 g_law at x = r/r_M = 0.3, 0.4-0.5 at x = 1 and 11-22 at x = 30 (pass line 0.10 at every x in [0.3, 30]) and must supply 23-50 times the baryons' orbital kinetic energy.
4. **Top-level detection is not smooth.** The maximal-ball functional detects top-level status and puts the edge at r_e with no new constant, but it jumps by a factor 2 at every merger, so a variation needs a smoothing width.

**One expectation overturned.** I expected every baryon-reading gate to inherit DE12/DE13's stiffness obstruction (N14). It does not. A NONLOCAL enclosed-mass (Volterra) gate that reads baryon mass has no negative mode on all 48 layer x width cases (the local gate fails 44 of 48); the rank-one top-level-ball gate is second-variation stable on all 48 with either reading. The dynamical-mass reading of the Volterra gate does fail (29/48, every z <= 1 layer). So Gap 1's obstruction is NOT stability; it is Gauss + history + the exchange's reaction. That is a real narrowing, and it also shows that my own pre-declared instability hypotheses failed (see Disclosures).

## Scope and history of this directory
- `GATES_FROZEN.md` was written before any script. Two deconfliction messages narrowed the lane after the plan was drafted: CFG49 covers a dynamical gate scalar chi sourced by a baryon-only invariant, CFG50 a tidal-tensor fluid tested for reciprocity; this lane covers (1) ownership/boundness as a nonlocal or history functional, (2) hierarchical top-level detection as an action term, (3) CFG44's enclosed-mass exchange as an explicit nonlocal-kernel action with causality and reciprocity checks, plus the calculation-owner session's six back-of-envelope leads, treated as unverified hypotheses. Gates were frozen once, for this scope; no dynamical-gate-field construction was built.
- One typo in the frozen file ("BAROQ... BARYONS ONLY" in the GC heading) was corrected right after writing it, before any script existed. No criterion changed.
- Lead 5 (a bistable self-stiff gate) overlaps CFG49's territory; only its kinematic edge-balance exponent was run (G5), no gate field.

## Scripts (each < 10 s; each with a MUTATE control that exits 1)
| script | what it tests | result |
|---|---|---|
| `G1_gauss_noether.py` | leads 1, 2: Gauss lemma (sympy, general gate W(r) and kernel), the P2 profile for flux-gated QUMOND/AQUAL and the source-switched form, Helmholtz test, Noether identity and its size on DE12's layers | L1 HOLDS; source-switched form is non-variational; L2 identity exact; reaction/weight 0.55-2.2 |
| `G2_boundness_and_top_level.py` | energy boundness, monotone functionals at the Sun, the maximal-ball functional, state-vs-history | boundness edge 0.05-0.11 r_e; Sun ON by every monotone gate; ball gives top-level detection but jumps at mergers |
| `G3_history_action_causality.py` | memory/latch/label inside a discrete action | advanced dependence for memory and latch; label causal but initial data |
| `G4_exchange_action.py` | task 3: exchange action, energy budget, reaction, cross-block symmetry, Volterra structure | reaction 0.06 (x=0.3) to 22 (x=30) g_law outward; energy 23-50 x baryon KE; symmetric and enclosed-only |
| `G5_edge_stress_mediator_wall.py` | leads 3, 4, 5 | L3 PARTIAL, L4 PARTIAL, L5 HOLDS |
| `G6_nonlocal_gate_stiffness.py` | varied second variation of the Volterra and top-level-ball gates on DE12's 24 layers x w in {0.25, 1} | see "the stability result" |
| `Gcommon.py` | shared (imports CFG44's Bcommon and DE12's transition read-only) | |

Main runs (re-run by the orchestrating session from a scratch copy with the repo layout): G2-G5 exit 0; **G1 exits 1** although all 7 of its checks pass, because the script's exit code counts its recorded gate verdicts that FAIL (`R.write()` returns that count); **G6 exits 1** because its pre-declared instability hypotheses are false (4 load-bearing failures, kept as they fell). The first draft of this line said G1-G5 exit 0; that was wrong for G1. MUTATE runs all exit 1 with the named claim failing. Controls that reproduce committed numbers: DE12's c_gate_max on all 24 layers (deviation 0.0), CFG44's target hydrostatics and virial identity to 1e-6, G4's finite-difference derivative against the closed-form reaction (1.2e-3).

## Results by gate (GATES_FROZEN.md)
| construction | GA legal action | GB varied stability | GC baryon-only | GD covariant | GE edge + Gauss | GF new constants | GG(i) history / GG(ii) Cassini |
|---|---|---|---|---|---|---|---|
| flux-gated shift-symmetric field, prescribed W | FAIL (prescribed mask; Noether reaction 0.55-2.2 of baryon weight) | OPEN | n/a | n/a | **FAIL** (M_dyn = M_b beyond edge) | | |
| source-switched (phantom-density gate) | **FAIL** (Helmholtz, asymmetry proportional to W') | | | | PASS (1.004 of M_law) | | |
| energy boundness on baryon potential | | | PASS | | **FAIL** (edge 0.05-0.11 r_e; phantom-inclusive potential needs r_ta) | | |
| monotone functionals (E<0, U, theta<=0) | | | PASS | | | | GG(ii) **FAIL** (ON at the Sun, U_sun/U_MW = 9e16) |
| maximal-ball (top-level) functional | **FAIL** (sup, jump at mergers) | **PASS** second variation (48/48, both readings); first variation is an edge potential step 0.15-3.1 v_f^2 | PASS | PARTIAL (origin-free; needs foliation) | PARTIAL (edge = r_e, but as a field gate Gauss applies) | **FAIL** (smoothing width) | (i) FAIL; (ii) PARTIAL (removes the Sun's own phantom, makes accreted satellites Newtonian) |
| Volterra enclosed-mass gate | PARTIAL | baryon-mass reading **PASS** 48/48 (eta_crit >= 13.7); dynamical-mass reading **FAIL** 29/48 (all z <= 1) | PASS | PARTIAL (spherical statement) | Gauss applies | | (i) FAIL |
| history variable in an action (memory, latch) | **FAIL** (advanced dependence, c = 8.5e-4 and 1.7e-2) | | | | | | |
| prescribed advected label | PARTIAL (causal; a postulate, ownership as initial data) | exempt | | | | 1 postulate | (i) PARTIAL |
| enclosed-mass exchange as action (task 3) | PARTIAL (legal bilocal energy) | | | | | PASS (target postulated) | GH(a) PARTIAL (cross block symmetric; full operator not diagonalised); **GH(b) FAIL**; GH(c) PARTIAL (zeroth-order Volterra, instantaneous on the leaf) |

## The six leads (verified or refuted by script; none was assumed)
| lead | status | what the script found |
|---|---|---|
| 1 Gauss | **HOLDS** for gates that multiply the flux (all action-derived forms); the mass-keeping gate on the phantom density exists but is not variational | M_dyn(3 r_e)/M_b = 1.000000 for flux-gated QUMOND and AQUAL; sympy EL residuals zero; negative shell (M_law(r_e) - M_b) = 3.2e11, 2.2e12, 1.4e13 Msun for M_b = 1e10, 1e11, 1e12 |
| 2 Noether | **HOLDS** (identity exact, sympy) | d/dx(Phi' p - L) = -Delta L W', Delta L = dL/dW = (a0^2/8 pi G)(y - F); on DE12's layers Delta L\|grad W\|/(rho_b g) = 0.55-2.2 |
| 3 edge stress | **PARTIAL** | baryons at the cosmic share supply P_b/P_c = Omega_b/Omega_c = 0.186 (short by 5.4, not ~6.4). Under the frozen line (enclosed-mean and isothermal accountings <= 0.25 for M_b to 1e13) it is NOT met: 3 g/a0 = 0.29 at 1e13 (0.06-0.20 through 1e12) |
| 4 mediator | **PARTIAL** | alpha_req = x_e^2/2 (the lead's a0/(2 g_N)) = 546, 118, 55, 25 at 1e10, 1e12, 1e13, 1e14: 1e5-1e7 over Cassini's 3e-5; the frozen line (>= 1e2 for all M_b >= 1e10) fails at >= 1e13. The mediator's own force on baryons is a0/2 = 3.5-24 g_law: it overshoots the law it must reproduce |
| 5 wall balance | **HOLDS** (kinematic exponent only) | d ln x_e/d ln M in [1/6, 2/3]; x_e in [0.31, 0.48] over at most 1.14 decades (grid maximum 1.136) against the 4 needed |
| 6 exits | not run | one-off exchange at collapse = initial data (G3 label, PARTIAL); a gate reading the fluid is excluded by MS1/XR11; screened mediators and dynamical-edge-from-ram-pressure untested (the latter FG016 fails KiDS) |

## The stability result (G6), stated precisely
- **Local gate (control):** unstable nodes (c_gate > c_s, 117 km/s) on 44 of 48 layer x width cases; reproduces DE12's committed c_gate_max on all 24 layers exactly.
- **Volterra gate, baryon-mass reading (U_enc = U_0 [1 + dM/M_0]):** no negative mode on any window or the full layer on 48/48; the first negative mode would need B multiplied by >= 13.7 (eta_crit 13.7 to 430).
- **Volterra gate, dynamical-mass reading (phantom amplification A_par = nu + y nu'):** negative modes on 29/48: 12/12 at z = 0.25, 12/12 at z = 1, 5/12 at z = 2.5, 0/12 at z = 4; growth Gamma/H up to 238.
- **Top-level-ball rank-one gate (full second variation, E2 = (1/2) dM^2 [c_s^2/M_gas + E_R L2 + E_RR L1^2]):** stable on 48/48 for both readings, Xi = -0.35 to -10. E_RR L1^2 is ~0 numerically and E_R L2 is positive (the energy is nearly linear in ln R, and ln R is concave in M).
- **Caveat that the frozen gate does not price (first variation):** the ball gate's energy has E_R L1 != 0: a potential step of 0.15-3.1 v_f^2 (0.2-8 c_s^2) at the ball boundary for each unit of baryon mass. DE12's static gas background is therefore NOT an equilibrium of the varied theory, so the second-variation pass is not a stability certificate for the full theory. This is Noether lead 2 in another form.
- Hypotheses: DE12's frozen background and gas, isothermal gas at 1e6 K, spherical layers, B = a0^2 q(y)/(8 pi G) taken at the point-mass field (the gas's own Newtonian field and its response are not included, as in DE12), a fluid description, the gate's own first variation not fed back.

## DERIVED / POSTULATED / FITTED / OPEN
| status | items |
|---|---|
| DERIVED (script) | Gauss lemma for the gated two-field class (sympy); Helmholtz failure of the source-switched form, proportional to W'; Noether identity; baryon-potential boundness edge sqrt(3) r_M (P2), 1.443 r_M (nu_mono); top-level ball boundary = 0.4 r_ta exactly when all baryons are retained (Delta_edge = Delta_ta/x_e^3); merger jump at 2^(4/3) R_1, factor 2; advanced dependence of memory/latch actions; exchange reaction (3/8) a0 (2+x^2)/(1+x^2) and (3/4) a0; E_c/(1/2 M V_f^2) = 1.5 r_e/r_M; L5's exponent bound and 1.14-decade window; the second-variation counts of G6 |
| POSTULATED | the target law shape (P2 point mass) and T5's max rule; x_e = 0.4, M_* (B's declared items); the ball threshold Delta_edge = Delta_ta/x_e^3 (inherits x_e); the choice of a sigma-slaved or P-slaved exchange; ownership as a prescribed label; isotropic exterior for the exchange; the gate width W and w (DE12's shapes) |
| FITTED | kappa = 1/2; Omega_c h^2 = 0.1200 (T4) |
| NEW CONSTANTS introduced | maximal-ball gate: 1 (merger smoothing width, needed for a variation); Volterra gate: 0; history label: 0 numeric but 1 unmodelled assignment rule; exchange action: 0 in the target; numerical step regulariser in G4 E3 is a discretisation device, not a model parameter; no knob was scanned (the L5 grid and the 4000 wall draws sample a bound, they fit nothing) |
| OPEN | a covariant field-theoretic definition of the ball/equipotential-enclosed-mass functional (GD); full coupled stability of the exchange (gravity + pressure + exchange operator not diagonalised); the first-variation backreaction of the ball gate (edge shock of 0.2-8 c_s^2 not simulated); a Schwinger-Keldysh (doubled-field) treatment of the history variable (untested exit); screened or non-universal mediators; extended, non-point-mass baryons and anisotropic f(E, L) for the exchange; non-spherical balls and the Solar System's own tide under the ball functional (Cassini margin was not recomputed); relativistic completion and the khronon foliation of every instantaneous-on-leaf coupling |

## Exact hypotheses of each obstruction (what it does NOT cover)
- **Gauss (G1 C1-C2):** spherical, static, Newtonian limit; two fields (Phi, psi) with first-derivative Lagrangian, shift-symmetric in Phi, the ONLY source rho_b, gate W(r) prescribed or reading only baryon-slaved fields. Does not cover a second source with its own stress (a real-mass fluid: MUTATE shows M_dyn changes), non-shift-symmetric couplings, or the source-switched form (which escapes Gauss but fails Helmholtz).
- **Helmholtz (G1 C3):** the same two-field class, gate a prescribed function of r. A gate that reads a dynamical field adds that field's equation and is a different system (CFG49's lane).
- **Boundness (G2 D1):** circular orbits of point-mass baryons, P2 and nu_mono, z = 0. Says nothing about non-circular or extended baryons.
- **State functional vs ownership (G2 D3e, D4):** any functional of baryon density and velocity (and fields slaved to them). Does not cover a functional that also reads the carrier (MS1 forbids) or a label.
- **History (G3):** reduced action in which the history is a functional of the path; smooth W, f; a one-degree-of-freedom toy, so the statement is structural, not a size. Does not cover advected labels (PARTIAL above) or doubled-field (in-in) actions.
- **Exchange (G4):** point-mass baryons so the exterior is isotropic (beta = 0); fluid shell masses fixed (sigma-slaved) or P-slaved; internal energy (3/2) sigma^2 per unit mass. Does not cover CFG44's Lagrange-constraint (multiplier gravitates, M_lambda/M_c up to 3.4) or density-slaved (reaction -1.2 to -4.2 g_law) versions, which are cited, not rerun.
- **Stress leads (G5):** point-mass P2, z = 0, r_e = 0.4 r_ta, gas at sigma^2 = V_c^2/2; the mediator estimate assumes a massless universal scalar with force alpha g_N and stress alpha g_N^2/(8 pi G).

## Disclosures (failures and revisions, kept as they fell)
- **G6 pre-declared hypotheses H_V and H_R (Volterra and ball gates unstable on >= 75% of cases, baryon-mass reading) were FALSE: 0/48 and 0/48.** My energy-budget argument (gate energy scale ~ a0 M r_e against gas thermal energy) predicted instability and was wrong for these functionals.
- **The first G6 run's ball formula was incomplete:** it used only the W'' part of the second variation and missed E_R L2 and the W' part of E_RR. The final script has the full expression; the first version and its 0/48 output are not committed.
- **H_V2 and H_R2 were declared after seeing round 1** (dynamical-mass reading). H_V2 failed (29/48 = 60% < 75%), H_R2 failed (0/48). The counts by redshift are what matters, and they are reported above.
- The frozen L3 and L4 lines are NOT met literally (0.29 at 1e13; alpha_req below 100 at >= 1e13); the leads' galaxy-mass conclusions hold. They are reported PARTIAL, not HOLDS.
- Not scripted, therefore not claimed: the causal escape via a multiplier with backward recursion (structure only), and the comparison of top-level-ball's Cassini margin with CFG7's 2e4-3e4.

## What this leaves for Gap 1
Gap 1 and Gap 2 collapse into one object: the cold fluid's dispersion (or stress) set by the ENCLOSED baryon mass at the edge. As a field-only gate it is impossible (Gauss). As an exchange action it has a reaction on the baryons of order or larger than the law itself and an energy budget 23-50 times the baryons' orbital kinetic energy, so the energy cannot be drawn from the baryons. As a history it is either acausal inside an action or a prescribed label. The surviving readings are all of the form "the fluid's state is initial data from collapse", which is what CFG44's temperature-slaved and locally-virialised survivors already were. The one clean positive result is negative: the DE12/DE13 stability wall is not what stops a nonlocal enclosed-mass gate.
