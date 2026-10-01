# CFG242 -- phase 2: the two frozen routes against G1-G5 (L14a: a causal ownership latch with a vacuum-funded exchange; L13: BIMOND with a lapse-free, preferred-foliation interaction). Two scoped no-gos.

Criteria frozen and committed before any script: `campaign_fresh_gravity/CFG242_FROZEN_CRITERIA.md` (commit d0bc9eb85, sha256 31033942...f7074a08, identical to the file I wrote). Run as frozen; every departure is listed in section 8. Nothing here says the theory is closed, nothing here says any data favour or disfavour the framework, and nothing is a theorem: each FAIL is a scoped no-go on its frozen class. **kappa = 1/2 stays FITTED. There is no dark-matter particle and no new species; the cold mass (Omega_c h^2 = 0.12) is still REQUIRED by both routes, and neither supplies it.** Nothing in the repository was edited; the two routes are scored separately and never pooled. No arm reached G1, so there is no derived-mechanism pass to flag; the freeze already said a derived G1 is impossible for route A, and the selectivity control confirms it (section 4).

**Re-run (about 70 s):** from this directory, `ZF_REPO=<repo root> bash CFG242_run_all.sh` (inside the repository the root is found by walking up, so `bash CFG242_run_all.sh` suffices; `CFG242_A_run_all.sh` and `CFG242_B_run_all.sh` run one route). It runs every main script (all exit 0), every MUTATE control (expected exit codes printed next to the observed ones; `unexpected outcomes: 0`), then `CFG242_A_verdict.py` and `CFG242_B_verdict.py`. No output prints an absolute home path (`<repo>` and `<lane>` are substituted; checked by grep).

## 1. Bottom line

- **Route A (L14a): binding failure G0, row B3 (bound-shell persistence).** Under the frozen latch equation E3, a bound shell after its own turnaround has n = 0.791 at one free-fall time, a minimum of 0.143 over t >= t_ff, and a late-time range 0.147-0.848 (mean 0.310), against the frozen line n >= 0.99 within one free-fall time and staying. The cause is in E3 itself: its decay term acts whenever theta_b >= 0, so a static bound system has no memory (n decays as exp(-t/2.05 t_dyn)) and an orbiting one is "contracting" only half the time. Causality (C1: c_adv exactly 0 at N = 200 and 400, A2 and A3; the mediator C2) and bound-only rows B1, B2, B4 PASS. Arms A2 and A3 stop there. Arm A1 (the strict arm) stops at G4 (tau_bar is scanned, untied); its G3 strict is evaluated anyway and FAILS (reaction 22.5 g_law against 0.10; energy 23-318 x the orbital energy).
- **Route B (L13): binding failure G5a, cell HYPERBOLIC, on flat space at the frozen point mu/b = -1/4.** The TT dispersion is omega^2 = c_T^2 kappa^2 with c_T^2 = 1 + 4 mu/b = 0, so the system is d_t^2 h = 0 (a Jordan block, linear growth), not strongly hyperbolic; the cell DETERMINED also FAILS (the quadratic action has nullity 2: the relative time diffeomorphism and the longitudinal spatial diffeomorphism are unbroken at quadratic order, so the helicity-0 sector is undetermined). The ghost cell PASSES (TT residue +1, no higher-order mode), speeds PASS (c_T^2 = 0 lies in [0, 1]). The route stops there; G4, G0, G3, G5b, G1, G2 are NOT ADDRESSED.
- **Reported, not part of any verdict:** for route B the flat-space TT sector is healthy for -1/4 < mu/b < 0 (0 < c_T^2 < 1); the helicity-0 sector is undetermined for every mu/b != 0 (section 5.2). For route A, the post-hoc continuation shows the vacuum ledger is not the obstacle (the heat needs at most 1.9e-4 of the vacuum energy of its ball; local a0 shift at most 9.5e-5), and the funded reaction needs eps_c <= 0.0045 (an untied coupling): with eps_c = 1 and the Lambda-tied memory time tau_L = 101.5 Gyr the reaction is 22.4 g_law and the fluid's heat store reaches only 0.118 of its target by 13.79 Gyr.

## 2. Gate tables (P = PASS, F = FAIL, U = UNDEFINED, N = NOT ADDRESSED, p* = trivially; each cell cites its script; MAIN = the frozen stop-rule verdict, PH = post-hoc continuation after the stop, labelled and never part of the frozen verdict)

### Route A (L14a) -- arms never pooled

| gate | A1 (strict: iota = 0, r = 1, tau_bar free) | A2 (funded, iota = 0, tau_bar = tau_L) | A3 (funded, inhibitor) |
|---|---|---|---|
| controls | P: C-A1..C-A3 (`CFG242_A_controls.py`: reaction 0.0647 / 0.530 / 2.13 / 7.46 / 22.5 vs the frozen numbers 0.5%; energy 72.8 / 49.6 / 23.0 and 318 / 179 / 57 in 1%; CFG72 committed reaction table to 2e-16) | same | same |
| G0 legality (MAIN) | not in the frozen order for A1 | **F** (`CFG242_A_g0_legality.py`): B3 fails; C1, C2, B1, B2, B4 pass | **F** (same B3; the inhibitor is not a fix for it) |
| G4 | **F, MAIN, STOP** (tau_bar free; `CFG242_A_g4_ledger.py`) | N in MAIN; PH: G4a (tied) P, G4b (eps_c = 1 is a number put in by hand) F: strict **F** | N in MAIN; PH: **F** (beta = 1 untied) |
| G3 | **F** strict (`CFG242_A_g3_exchange.py`; evaluated after the stop, kernel-independent) | N in MAIN; PH funded: reaction **F** (22.4 g_law with eps_c = 1), ledger P | N in MAIN; PH funded: same as A2 |
| G5 | N | N in MAIN; PH: Q2 **F** (n x 6.3e3 x the bound; `CFG242_A_g5_solar_stability.py`), stability N | N in MAIN; PH: Q2 P only through the inhibitor (by construction), stability N: **U** |
| G1 | N (and p* at best: the target is supplied; `CFG242_A_g1_target.py`) | N | N |
| G2 | N | N | N |

### Route B (L13) -- never pooled with route A

| gate | 13d (foliated, lapse-free interaction; primary mu/b = -1/4) |
|---|---|
| controls | P (`CFG242_B_controls.py`): EH gauge invariance; the 4D class reproduces WF2/L70 (a fourth-order vector, c_T^2 = 1); 13c row reproduces CFG232's committed row (3 verdicts, 4 checks identical) |
| G5a flat space (MAIN) | **F, STOP** (`CFG242_B_g5a_ghost.py`): GHOST P, SPEEDS P (c_T^2 = 0), HYPERBOLIC **F**, DETERMINED **F** (nullity 2); the exact static MOND background cell: N |
| G4 | N in MAIN; PH: **F** (gamma/beta, mu/b and the direction are numbers beyond kappa and Omega_c h^2; `CFG242_B_g4_ledger.py`) |
| G0 legality | N |
| G3, G5b (Q2), G1, G2 | N, N, N (`CFG242_B_not_reached.py`), N |

## 3. Binding failures (named)

- **Route A, G0 / B3.** n(t_ff) = 0.791, min n over t >= t_ff = 0.143, late-time mean 0.310 (min 0.147, max 0.848) for a bound probe shell started at rest at q = 1 (GM = 1, softening 0.05, H = 0.01 in units of t_dyn(q = 1) = 1); the line is >= 0.99 within one free-fall time and stays. A static bound system (theta_b = 0) obeys tau_n dn/dt = -n, tau_n = 2.05: no memory.
- **Route A, A1 strict, G4 then G3.** tau_bar is an untied grid; and the late-time reaction is theta^T_M/g_law = 0.0647 (x = 0.3) to 22.49 (x = 30), crossing 0.10 at x = 0.378 (pressure-slaved; sigma-slaved 0.396, 11.26 at x = 30), kernel-independent; energy 72.8 / 49.6 / 33.8 / 23.0 x (CFG48 r_ta) and 318.4 / 179.1 / 100.8 / 56.7 x (committed r_ta) at 1e9 / 1e10 / 1e11 / 1e12 Msun.
- **Route B, G5a / HYPERBOLIC** (and DETERMINED), as in section 1.

## 4. Legality-test outcomes (route A, G0; exact numbers; `CFG242_A_g0_legality.py`)

- **Derivation check D1 (control).** The numpy action's residual (complex step on the action itself) equals the sympy derivative of the same action at Delta = 0 at N = 5: max rel dev 5.6e-15; the exact sympy Jacobian has 0 nonzero entries for j > i + 1; exact reciprocity asymmetry 0.0.
- **C1 causal band (frozen: N = 200 and N = 400, Jacobian <= 1e-12).** c_adv = max_{i <= J-2}|dR_i|/max|dR| over 12 cut points: 0.0 (exactly) at N = 200 (A2), N = 400 (A2) and N = 200 (A3, with an external-host inhibitor). PASS. The zero is structural (the retarded kernel never references later steps), and the control MA1 shows the detector can fire: symmetrising the kernel gives 3.45e-3 / 7.67e-4 / 5.42e-3.
- **C2 mediator.** Characteristic speed c_m sqrt(1 + beta)/c = 1.000000000000 <= 1 (beta = 1 untied, as in CFG72); the leapfrog Green function outside the numerical cone is exactly 0.0 (<= 1e-12) after 600 steps (by construction of the explicit stencil); the elliptic stencil is the failing control: 0.349 (CFG72: 0.25). PASS.
- **B1 FRW background (theta_b = 3H).** max n = 0.0 (n(0) = 0). PASS; reported: from n(0) = 1e-3 the latch decays below 1e-6 at t = 16.0 t_dyn.
- **B2 outgoing positive-energy shell.** max n = 0.0; the exchange force c_f(theta - n thT) n thT' and the heat target n thT are identically 0 at n = 0 (r = 0). PASS.
- **B3 bound shell, frozen E3: FAIL** (numbers above).
- **B4 inertness.** Force and heat target are proportional to n: exactly 0 at n = 0 (the closed arm A1, r = 1, would leave a heat offset -r/c and is not legality-tested in the frozen order). PASS.
- **Hierarchy rows (reported, not legality).** Frozen E3, inhibitor off: (i) embedded n_sub max 0.847; (ii) accreted late min 0.147, mean 0.296. Frozen E3, inhibitor on: (i) 0.000; (ii) accreted late min 0.000, mean 0.000 (the latch decays). Post-hoc E3'' (decay driven by the baryon-shell energy, labelled), inhibitor off: (i) 1.000, (ii) 1.000; inhibitor on: (i) 0.000, (ii) 1.000.
- **Post-hoc E3'' for B3 (labelled, not the frozen verdict).** B1, B2 max n = 0.0; n(t_ff) = 0.791 (the same: growth is limited by tau_n during the first contraction), min over t >= t_ff = 0.791, and n first reaches 0.99 at 5.6 t_dyn = 5.0 free-fall times: so even the repaired latch misses the frozen "within one free-fall time" line; it keeps its value afterwards.
- **Top-level (iii) for the Sun, reported (`CFG242_A_g5_solar_stability.py`).** A local latch (A2) gives the Sun's own cold cloud Q2 = n x 6.31e3 x the bound at Saturn (canonical; 7.62e3 alt; the bound needs n <= 1.6e-4 / 1.3e-4); this recipe reproduces CFG230's 6.28e3 and differs from CFG251's 1258-1545 x (a different convention). The inhibitor (A3) removes it by construction (embedded collapse n <= 1e-6, post-hoc E3'') at the price of the untied beta = 1.
- **G1 selectivity control (`CFG242_A_g1_target.py`).** The class's static equilibrium reproduces the P2 target AND a Verlinde-shaped target handed to it, both with max relative deviation 0.0: it reproduces whatever it is given, so a P-derived G1 is impossible for class A, as frozen.

## 5. What the scripts showed

### 5.1 Route A, post-hoc continuation (funded reading; labelled; not the frozen verdict)

`CFG242_A_g3_exchange.py`: with r = 0, eps_c = 1 (CFG70's N6 value, a departure), tau_bar = tau_L = 101.5 Gyr (from the tie; rho_Lambda = 86.33 Msun/kpc^3), t_f = 1 and 10 Gyr, the peak of (Thetabar * mdot) is 0.995 / 0.953 and the maximum reaction over x in [0.3, 30] is 22.38 / 21.43 g_law (pressure-slaved; 11.20 / 10.73 sigma-slaved); the 0.10 line needs eps_c <= 0.0045 / 0.0047 (0.0089 / 0.0093) -- an untied coupling. The vacuum ledger: E_c/E_vac(<r_e) between 9.9e-7 and 1.9e-4 over the four masses and both r_ta conventions; local a0 shift 5.0e-7 to 9.5e-5 (line 1e-2); every ball is within reach of light in 1 Gyr (c t_f/r_e >= 201). Not checked: how a w = -1 vacuum delivers energy locally (door 8's untested premise, the non-Lorentz-invariant or dynamical vacuum). Tracking (reported; G1 not addressed): with tau_bar = tau_L the heat store reaches 0.118 of its target by 13.79 Gyr for a 1-Gyr formation (the G1 line is 10%).

### 5.2 Route B, flat space (`CFG242_B_g5a_ghost.py`)

Helicity 2 (TT): M_TT = b omega^2 - (b + 4 mu) kappa^2, so c_T^2 = 1 + 4 mu/b and the residue 1/b > 0. Helicity 1: determinant -2 b kappa^4 mu, constant in omega: no propagating mode. Helicity 0: the quadratic form is degenerate; the two zero directions are the Stueckelberg directions of the relative time diffeomorphism and of the longitudinal spatial diffeomorphism (nullity 2, verified symbolically); at mu = 0 the nullity is 4 (the full relative gauge symmetry). The scan (reported only): c_T^2 < 0 for mu/b < -1/4, = 0 at -1/4, in (0, 1) for -1/4 < mu/b < 0, > 1 for mu/b > 0; the nullity is 2 throughout. The 4D class on flat space (control, `CFG242_B_controls.py`): helicity-1 determinant -2 mu (b + 4 mu)(kappa - omega)^2 (kappa + omega)^2 (a fourth-order vector), TT entry -(b + 4 mu)(kappa^2 - omega^2) (c_T^2 = 1): WF2/L70's structure from fresh code; at mu = -b/4 both vanish identically (the kinetic degeneracy of the record's tuned point). In the foliated class the same tuned value removes only the TT gradient energy.

## 6. Requirements R01-R12 re-scored by what the scripts showed (CFG230 labels; "N" = not tested by any script here)

| Req | Route A | Route B |
|---|---|---|
| R01 scale | N (the target, and with it r_M, is supplied) | N |
| R02 acceleration scale | d: a0 enters through the supplied target; the Lambda tie fixes the memory time (101.5 Gyr), not the amplitude | d: native tie "inverted" (CFG232); unchanged |
| R03 shape | declared: the class reproduces any supplied shape (selectivity 0.0 / 0.0) | N |
| R04 closure | N | N |
| R05 cold-early | within the toy model the latch is inert in the FRW and outgoing cases (n = 0 exactly); G2 N | N |
| R06 reciprocity and energy | closed class: reaction 22.5 g_law and 23-318 x orbital energy reproduced (F); funded: energy not the obstacle (<= 1.9e-4 of the vacuum energy of the ball), reaction F unless eps_c <= 0.0045 | N |
| R07 bound-only switch | legality (causal, bound-only B1/B2/B4) PASS; persistence B3 F under E3, and under E3'' the latch needs 5.0 free-fall times; top-level only through an untied inhibitor | N (G0 not reached) |
| R08 EFE branch | N | N |
| R09 Solar tail | Q2 = n x 6.3e3 x the bound for a local latch (reproduces CFG230's 6.28e3) | N |
| R10 preferred frame | N | N (the khronon decouples at quadratic order about flat space; not treated on a background) |
| R11 stability | N | F: flat space not strongly hyperbolic at mu/b = -1/4; healthy TT window (-1/4, 0); helicity 0 undetermined (nullity 2) |
| R12 medium, tie, constants | G4: tau_bar tied; eps_c and beta untied; how a w = -1 vacuum pays N | G4 F (gamma/beta, mu/b, direction) |

## 7. How the frozen hand estimates fared (kept, wrong ones included)

Route A: reproduction control within 1%: 0.9, **held**. G0 legality PASS: 0.6, **wrong** (B3 fails; I had worried about "exact zero" of a smoothstep, not about E3's decay term at theta_b = 0). G4 PASS for A2: 0.5, **partly wrong** (the memory time ties; eps_c is untied under the frozen constants rule). G3 strict FAIL: 0.99, **held**. G3 funded, reaction PASS 0.5, **wrong** (22.4 g_law; needs eps_c <= 0.0045); ledger PASS 0.7 **held**, but my hand number for the local a0 shift ("a few percent at most", 1e-4 to 3e-2 of rho_Lambda c^2) was wrong by at least two orders (the measured shift is at most 9.5e-5); a0-shift line PASS 0.4 held for the wrong reason. G5 Q2: A2 FAIL 0.95 **held**; A3 PASS 0.3, passes only by construction. G5 stability 0.5: not addressed. G1 P-declared 0.5: not addressed; P-derived 0 by construction **held**. G2: not addressed. Route B: 13c control 0.9 **held**. G5a ghost-free 0.2: the ghost cell PASSES but the gate FAILS on hyperbolicity and determinacy (the expectation named the wrong sub-question). G4 FAIL 0.8 held (post-hoc). G0 legality PASS 0.15, G3 energy FAIL 0.9, Q2 FAIL 0.8, G1 P-declared 0.5, G2 UNDEFINED 0.8: not addressed (the stop rule). The phase-1 P(all) estimates (A 9.8e-4, B 4.9e-4) were not contradicted.

## 8. Failed or non-biting controls, wrong expectations, and departures (all kept)

**MUTATE outcomes (exit 1 = bites).** MA1 (symmetrised kernel) bites: C1 flips PASS -> FAIL (c_adv 3.45e-3 at N = 200). MA2 (sign-blind source) bites: B1 flips (n rises to about 1). MA3 bites in `CFG242_A_g0_legality.py` (the reciprocity-symmetry cell: asymmetry 2.5e-2 against 1.2e-10) and in `CFG242_A_g3_exchange.py` (the funded reaction cell flips FAIL -> trivial PASS). MA4 bites (G4a flips PASS -> FAIL). MA5 bites (the funded ledger cell flips to UNDEFINED). MA6 bites (the hierarchy row (i) flips PASS -> FAIL when the inhibitor is off). **MA7 does NOT bite (declared control failure):** the main cell is already the restatement verdict (the class reproduces both targets). MB1 bites (the 4D class: GHOST flips PASS -> FAIL, a fourth-order vector). MB2 bites (sign flip: c_T^2 = 2, SPEEDS flips). **MB3 does NOT bite:** about flat space the induced spatial metric difference is unchanged at first order, so independent foliations change nothing at quadratic order. **MB4 and MB5 do NOT bite:** their target cells (G1 selectivity, G1-C) lie beyond the stop and are not addressed.

**Departures and ambiguities, each handled as the instruction required (main result as frozen, alternative labelled post-hoc):**
1. **E3 defect.** The frozen latch equation has no memory at theta_b = 0. B3 is scored on E3 as frozen (FAIL). The energy-driven decay E3'' is a labelled post-hoc alternative; it also fails the "one free-fall time" line.
2. **eps_c.** The frozen file does not fix the free-energy stiffness; I declared eps_c = 1 (CFG70's N6 value). By the frozen constants rule a number put in by hand is a constant, so G4b is scored strict (FAIL) and the lenient reading is reported beside it, not used.
3. **Order for A1.** The frozen gate order puts G4 before G3; G4 FAILS for A1 (tau_bar free), which is the stop, although the frozen text calls G3 strict A1's stop. G3 strict is evaluated anyway and reported as a labelled item.
4. **C1 method.** The frozen test is "Jacobian <= 1e-12 at N = 200 and 400". I take the Delta-variations of the action by complex step (exact to rounding) and test dependence on later steps by cut perturbations at 12 cut points per N, not the full dense Jacobian; the sympy derivation and the exact Jacobian structure are at N = 5 only. The sympy cross-check at 200 or 400 steps was not run.
5. **Test data.** Unit choices (m, c_f, dt, tau_G, H, softening, seeds, the host mass ratio 0.1, the retarded one-step delay of the host's mass in the inhibitor, the shell started at rest at q = 1) are numerical test data, not model numbers. The B1-B3 shells are 1-D radial orbits with a softened potential; theta_b = 3 qdot/q uses the softened radius.
6. **Route B reading.** "Lapse-free" is read as an interaction built from the spatial connection difference only, with the measure's lapse dependence irrelevant about flat space (M(0) = 0, so the measure does not enter the quadratic action there). The five invariants are restricted to spatial indices. The primary point mu/b = -1/4 is the 4D class's tuned degeneracy value, taken as the frozen reading; the foliated class's own degeneracy value was NOT derived (a foliated static reduction was not run). The khronon is not treated (it decouples at quadratic order about flat space).
7. **Control C-B3.** The committed CFG232 A7 was copied to a scratch directory and re-run there; the repository was not written. Only the canonical a0 is used by the closed-form A scripts (they depend on a0 only through x, except Q2, which carries both footings).
8. **A3's inhibitor** is implemented as a smoothed step of the retarded latched mass of an external host in the action (for C1) and as a prescribed-timing host in the hierarchy simulations; the Gauss-law mediator itself is tested only for causality (C2), not coupled to the latch.

## 9. What was NOT tested

Route A: G1, G2 for any arm; G5 stability of the coupled latch-fluid-mediator operator; the funded arms' G4, G3, G5 in the MAIN run (they stopped at G0); the physical identity of the vacuum reservoir and how a w = -1 vacuum delivers energy locally; the Boltzmann CMB; non-spherical baryons; the exponential sphere (only closed forms in x, which are profile-independent for the point mass); whether another latch equation (a hysteretic or energy-based one) can meet B3's "within one free-fall time" line. Route B: the exact static MOND background operator and the khronon on it; G4, G0, G3, G5b, G1, G2 in the MAIN run; a foliated static reduction (the foliated class's own tuned value and whether it has a MOND limit at all); the helicity-0 sector beyond the statement that the quadratic action leaves it undetermined; the lapse-in-measure reading; the Hamiltonian count of degrees of freedom. Both: any data fit; whether the twelve requirements are jointly satisfiable. The two routes' outcomes do not say the theory is closed or refuted; kappa = 1/2 stays FITTED; the cold mass is still required.

## 10. Files

`CFG242_common.py`, `CFG242_B_algebra.py`; route A: `CFG242_A_controls.py`, `CFG242_A_g0_legality.py`, `CFG242_A_g4_ledger.py`, `CFG242_A_g3_exchange.py`, `CFG242_A_g5_solar_stability.py`, `CFG242_A_g1_target.py`, `CFG242_A_verdict.py`, `CFG242_A_run_all.sh`; route B: `CFG242_B_controls.py`, `CFG242_B_g5a_ghost.py`, `CFG242_B_g4_ledger.py`, `CFG242_B_not_reached.py`, `CFG242_B_verdict.py`, `CFG242_B_run_all.sh`; `CFG242_run_all.py`, `CFG242_run_all.sh`; for each script its `.out` and `.json` (main) and `_MUTATE_<m>.out` / `.json` (MUTATE modes: A_g0_legality MA1, MA2, MA3, MA6; A_g4_ledger MA4; A_g3_exchange MA3, MA5; A_g1_target MA7; B_g5a_ghost MB1, MB2, MB3; B_not_reached MB4, MB5); `CFG242_A_verdict.out`, `CFG242_B_verdict.out`; this `README.md`. The frozen criteria are `../CFG242_FROZEN_CRITERIA.md` (d0bc9eb85).

## In-place re-run (orchestrator)

`bash CFG242_run_all.sh` was re-run in this directory with `ZF_REPO` set (about 70 seconds; `run_all.out`): `unexpected outcomes: 0` for both routes; every `.out` and `.json` is identical to the author's apart from timing. The frozen triage is `../CFG242_FROZEN_CRITERIA.md` (d0bc9eb85). Both routes ended in scoped no-gos at their first binding FAIL on the frozen classes; neither reached G1. Nothing here is closure, the cold mass is still required, and kappa = 1/2 stays fitted.
