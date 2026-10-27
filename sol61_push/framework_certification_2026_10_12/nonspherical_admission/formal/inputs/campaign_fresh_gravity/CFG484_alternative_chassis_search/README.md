# CFG484: is there a relativistic chassis for candidate B that passes every gate?

Criteria frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit a93772934, committed alone before any script.
Theory survey plus checks. Offline, no downloads. Every other lane is read-only here.

| run | output files | checks | exit code |
|---|---|---|---|
| main | `cfg484_chassis_search.out`, `cfg484_results.json` | 18/18 pass | 0 |
| MUTATE (`CFG484_MUTATE=1`: known-failing completions fed as the candidate) | `cfg484_chassis_search_MUTATE.out`, `cfg484_results_MUTATE.json` | 22/23 (the final "candidate WORKS" check fails, as required) | 1, as required |
| run 1 (kept verbatim) | `cfg484_chassis_search_run1.out`, `cfg484_results_run1.json` | 16/17 (K3 failed, see Disclosures; same ranking, top candidate and verdict) | 1 |

    python3 campaign_fresh_gravity/CFG484_alternative_chassis_search/cfg484_chassis_search.py
    CFG484_MUTATE=1 python3 campaign_fresh_gravity/CFG484_alternative_chassis_search/cfg484_chassis_search.py

Each run takes about 15 s. The record table is data in `cfg484_record.py`; every status cites its lane.

## Verdict: NONE (frozen rule)

**No completion passes every gate.** Nothing on the record does, and neither of the new classes does yet.

**The top candidate is new: NC1, "gravity is plain GR + Lambda; MOND lives only in the cold fluid".**
- Its gravity sector passes, or is shown not to need, every gate of CFG467's table, plus GW170817. The reason is simple:
  it is GR. There is no khronon, so there is no alpha_c axis and no sign tension. It adds zero chassis constants.
- It is still INCOMPLETE. Four items are open:
  - **G1:** the cold fluid's own relaxation rule has not been shown well-posed.
  - **G14:** Cassini passes only if the Sun cannot hold its own settled fluid (CONDITIONAL).
  - **H3:** nobody has shown that the fluid actually reaches the target and holds it.
  - **H4:** the switch.
- **The honest one-line reading: moving MOND into the fluid does not solve CFG467's tension. It moves it out of
  gravity and into the fluid's own dynamics.**

**The runner-up is on the record: R04, the C-H/K khronon plus a Horava UV sector M_*** (CFG467's option 2).
- It ties NC1 on every gate count.
- The frozen ranking separates them only by the constant count: 0 for NC1, 4 for R04.

**The best fully computed record option is still R03,** the C-H/K khronon with black-hole reading W. It is TENSION:
one owner call, no new constant.

## What NC1 is

Four statements define it:
- Gravity is exactly GR with Lambda. Baryons and the cold fluid both couple minimally to one metric.
- Inside bound regions (switch ON), the cold fluid settles toward the law's target.
- The target is written as a local function of the fluid's **own 4-acceleration** A:
  rho_target = div[F(|A|) A_hat]/4 pi G, where F inverts the declared kernel.
- When the fluid sits at rest, held up by its own pressure, A equals the total gravitational field. CFG373 G1 already
  showed that the P2 target is a local function of the total field.

What this changes, compared with B's current working model (R05):
- **The messenger.** R05 uses the khronon lapse to carry the target. NC1 uses the fluid's own acceleration, so no
  khronon is needed.
- **It is scored only as a non-Lagrangian (dissipative) relaxation law.** If the rule is written as a Lagrangian term
  instead, it falls into record classes that are already closed (N1g):
  - a foliation-invariant term is a khronon dust: the BS24 class, which N8 closes by KiDS for any K;
  - a superfluid-phase term carries second derivatives of the phase (Ostrogradsky). That is the FRIED_CHICKEN banner's
    dark_sector_honesty no-go; the degenerate case is untested.

## The first gate pass for NC1 (computed here)

| item | result |
|---|---|
| N1a black holes (G12) | Schwarzschild Kretschmann computed from the metric: 48 G^2 M^2/(c^4 r^6), finite for r > 0 (K8). Kerr is regular (LIT-GR). The fluid is test matter near holes |
| N1b messenger (H2) | sympy: the static observer's 4-acceleration is grad Phi to first order. y nu(y) is strictly increasing on [1e-8, 1e8] for nu_mono and P2, so the inversion exists for both kernels (nu_mono round trip 1e-13). Zero constants |
| N1c no external-field effect (reported) | A uniform external field leaves the fluid's own A unchanged (equivalence principle), so NC1's target has no EFE. For comparison, the algebraic law's internal field at r_M drops to 0.94 / 0.84 / 0.73 (P2) and 0.94 / 0.84 / 0.67 (nu_mono) for g_e = 0.01 / 0.1 / 1 a0. This matches B's no-EFE reading (PAPER44, CFG447). If an EFE is ever detected, it kills NC1 |
| N1d Solar System (G14), reading R1: the Sun sits inside the Milky Way's settled fluid | Host fluid at R0: 0.0049 / 0.0057 Msun/pc^3, sigma 144 / 147 km/s. The Liouville cap on fluid bound to the Sun gives an anomaly of 1.5e-22 m/s^2 at Mars (1.1e-7 of the bound) and 6e-23 at Saturn (8.5e-9). The Sun's own target exceeds what Liouville allows by 2e12 at Saturn. The Milky Way fluid's tide is 2.0e-31 s^-2, consistent with Q2 = (3 +- 3)e-27. Its monopole at Saturn is 1.3e-19 m/s^2. Its contamination of gamma is 2.3e-18. Both footings pass, and also at 3x the host density |
| N1d readings R2 / R3: the Sun owns its own settled target | nu_mono gives 1.08e-10 m/s^2 at Mars (76,893x the bound) and 9.65e-11 at Saturn (13,786x); alt gives 92,430x / 16,562x. P2 gives 33,430x / 6,686x, which reproduces the record's MI numbers (K4). So the Sun must not hold its own fluid: either Gap-1 ownership forbids it, or the fluid cannot be captured |
| reported (Cassini) | Bondi-Hoyle capture radius for a collisional host fluid passing at 230 km/s: 0.024 AU. That is inside about 5 solar radii, so any captured fluid falls into the Sun |
| G14 status | **CONDITIONAL**, by the frozen rule. A PASS needs the settling to be shown to conserve phase-space density for embedded systems, and NC1's settling is dissipative |
| N1e PPN contamination (G6/G7) | Fluid mass inside 1 AU divided by M_sun = 2.7e-18. The line was 1.6e-12 |
| N1f realisability (fluid-sector analog of G5; reported) | Isolated razor-thin exponential discs (1e9 / 1e10 / 1e11 Msun), both kernels, both footings, two grids: the QUMOND phantom density is never negative off the plane (0 of 3584 cells; eta = 0). The field engine matches the Hankel form to 7e-12. **Positive control, added after run 1:** a point mass in a 0.1 a0 uniform field gives eta = 0.24 (P2) / 0.22 (nu_mono), with negative belts. So real mass can realise the target of an isolated disc, and NC1's no-EFE target never asks for the negative belts |

**What NC1 costs.**
- **In the chassis:** 0 constants. kappa = 1/2 stays fitted.
- **In the fluid sector:**
  - a settling rate (CFG464: the zero-constant t_dyn rate is not excluded);
  - the switch constants, still open.
- **H6, the a0-Lambda tie:** carried via CFG43's fluid-sector existence result in the XR20 T1 form, tied with kappa
  chosen.
- **H4, the switch:** CONDITIONAL. It rests on the fluid-phase first-order switch: CFG478 shows it is legal, and CFG482's
  two-valued SED passes in PM runs. Both are non-relativistic.

## NC2 and the argument rows

- **NC2 (alpha_c screened to 0 in strong fields): FAILS strictly.**
  - At the universal horizon, alpha_c must lie in G1's strict set (0, 0.5) U (0.5, 2) and in G12's strict set {0}.
    These are CFG467's committed sets, and their intersection is EMPTY at every c2.
  - With the lenient black-hole reading it reduces to R03 plus at least one screening constant, so it is dominated.
- **NC3 (invertible disformal or two-time-scale redefinitions): no opening** (an argument, not a calculation).
  - Gate outcomes do not change under invertible field redefinitions of the whole action, matter coupling included
    (Foster-type; literature, memory-level).
  - A non-invertible map is mimetic, which CFG124 already covers.
- **NC5 (Einstein-aether with a twisting aether): FAILS criterion B** (an argument). A twisting aether gives no global
  preferred time.

## The table (frozen ranking; "n.c." = the record does not count the constants)

| row | completion | class | FAIL (lane) | LEN / COND | untested | constants beyond kappa, Omega_c h^2 |
|---|---|---|---|---|---|---|
| **NC1** | **NEW: GR + Lambda chassis, MOND only in the cold fluid** | INCOMPLETE | - | G14 COND (N1d), H4 COND (CFG478) | G1 (fluid sector), H3 | **0 in the chassis**; fluid: settling rate, switch |
| R04 | C-H/K + Horava UV sector M_* (CFG467 option 2) | INCOMPLETE | - | G11 COND (CFG320 hierarchy via M_*), H3 COND (CFG373 G3, CFG381), H4 COND | G12 | 4: alpha_c, c_2, xi, M_* |
| R17 | GR + dark field, no MOND field (CFG2/5/9/10/FG004, CFG43/44) | INCOMPLETE | H2, H3 (CFG44, CFG5) | G14 COND | G1, H4, H5 | n.c. (principles, no Lagrangian) |
| R16 | FRIED_CHICKEN frame flip | INCOMPLETE | H2 (dark_sector_honesty) | G1, G14 COND (on mu_10) | 11 G, 5 H | n.c. |
| R12 | Astra IC28 integrable clock | INCOMPLETE | - | - | all | n.c. |
| R19 | Dipolar DM (door 3) | INCOMPLETE | H3 (CFG121) | G1, G14 COND | 12 G | 2 (CFG121 G4) |
| R10 | Blanchet-Skordis khronon dust | INCOMPLETE | H3 (BSK1, N8/BSX3) | - | 14 G | n.c. |
| R13 | Generated phantom GP0-GP5 + L357-L361 (non-relativistic) | INCOMPLETE | H3 (L363, GP5) | - | 14 G (embedding = V0) | n.c. |
| R23 | Deser-Woodard / RR (door 9) | INCOMPLETE | H3 (CFG123) | - | 14 G | n.c. |
| R25 | DBI v9 dark sector (N9); CQ gravity (L313/L314) | INCOMPLETE | H3 | - | 14 G | - |
| R03 | C-H/K with black-hole reading W | TENSION | - | G12 LEN (owner call), H3, H4 COND | - | 3, no new constant |
| R07 | Derivation-chain action | FAILS | G12 (XR25, CFG319), H4 (FP23) | - | 12 G | n.c. |
| R09 | FC-KH khronometric f(a) | FAILS | G14 (N6 Cassini-vs-ghost) | - | 13 G | n.c. |
| R15 | MOND-sector gate MS1-MS5 | FAILS | G1 (MS5 / DE7 k^4 bracket) | H4 COND | 13 G | n.c. |
| NC5 | NEW (argument): Einstein-aether, twisting aether | FAILS | G1 (criterion B, argument) | - | 13 G | n.c. |
| R08 | AeST v9 / FC-AeST | FAILS | G7 (N7: alpha1 = -2(K_B + 2)), H3 (closure map) | - | 13 G | n.c. |
| R14 | Dark-energy gate DE1-DE13 | FAILS | G1, H4 (N14: DE7, DE12, DE13) | - | 13 G | n.c. |
| R22 | Mimetic (door 10) | FAILS | G1, H3 (CFG124) | - | 13 G | n.c. |
| R24 | Modified-inertia field theory | FAILS | G14 (Reading A, a0/2 at every planet), H5 (CFG447) | - | 13 G | n.c. |
| R11 | Astra CA4/CA5 [unreviewed] | FAILS | G7 (AS233), H4, H6 (FINAL_ACTION) | - | 13 G | n.c. |
| R01 | C-H/K chassis, strict | FAILS | G12 (CFG318/319 count, RB2019) | G11 LEN, H3, H4 COND | - | 3 |
| NC2 | NEW: alpha_c screened in strong fields | FAILS | G12 (N2) | G11 LEN | - | 4 |
| NC3 | NEW (argument): disformal redefinition | FAILS | G12 (inherits R01) | G11 LEN | - | n.c. |
| R05 | **B's current working model** on C-H/K (khronon-lapse messenger) | FAILS | G12 (CFG318/319) | G11 LEN, H3 COND (CFG373 G3, CFG381 +1) | G1 (coupled system) | 4 (+ lambda_x, CFG381) |
| R20 | BIMOND (door 13) | FAILS | G1 ghost, G14 Q2, H3 (CFG232) | - | 12 G | n.c. |
| R21 | Covariant emergent gravity (door 12) | FAILS | G1 vector ghost, G14 Q2 6.1e3x, H3 (CFG231) | - | 12 G | n.c. |
| R18 | Superfluid DM, Berezhiani-Khoury (door 4) | FAILS | G1 (c_s^2 < 0), G14 (Solar System), H3, H5 (CFG122) | - | 12 G | 3 (CFG122 G4) |
| R06 | V0 covariant action | FAILS | G1 (DE12/13), G12, H4 (N14) | G11 LEN, H3 COND | - | >= 9 declared + epsilon |
| R02 | C-H/K at alpha_c = 0 | FAILS | G1, G2, G3, G4, G5 (CFG292, CFG294, XC1, L340) | H3, H4 COND | G8, G11 | 2 |

How to read the ranking:
- The ranking orders rows by gate counts only, in a fixed order: FAIL, then LEN, then UNT + COND, first over G and
  then over H.
- So a row that is mostly untested ranks above a TENSION row by construction. Only the top of the list carries
  meaning.

## The decisive next test for NC1

One lane, staged so that each part can kill it:

1. **Well-posedness (G1).**
   - Write down the dispersion relation of the relaxation system, linearised about two backgrounds: a homogeneous one,
     and the deep-MOND singular isothermal sphere.
   - Pass: no Hadamard-unstable mode, and a causal relaxation time.
2. **Attractor (H3).**
   - Start from cosmic-share infall around a point mass and around compact and diffuse exponential spheres, at 1e9 to
     1e12 Msun, in the Newtonian limit of GR.
   - Pass: the fluid reaches the law's target to within 0.05 dex over x = 0.1 to 10, in a few dynamical times.
   - The same rule must work for every object, with no per-object constant. That includes CFG44's far-shell test and
     CFG473's compactness family.
3. **Energy (H3).**
   - The fluid must be held up, and its temperature set, by heat released as it settles. No external sink is allowed
     (compare CFG375's budget), and entropy must not decrease.
4. **Capture (G14).**
   - Move an embedded point mass through the settled host at 230 km/s.
   - Pass: no fluid settles around it at AU scales. If that holds, G14 becomes PASS.

If 1 or 2 fails, NC1 is dead. The chassis question then returns to R04, whose own decisive test is CFG319's
moving-black-hole count, redone with the z = 3 Horava terms at the universal horizon.

## MUTATE

The harness was applied to four completions known to fail. Each came out FAILS at its recorded gate:

| case | completion | must fail at | result |
|---|---|---|---|
| M1 | C-H/K strict | G12 (CFG467) | FAILS at G12 |
| M2 | AeST v9 | G7 (N7) | FAILS at G7 |
| M3 | Berezhiani-Khoury superfluid | G14 (CFG122) | FAILS at G1 and G14 |
| M4 | NC1 with the Sun owning its own target | G14 (computed here, N1d R2) | FAILS at G14 |

The final check, "the candidate under test WORKS", fails, so rc = 1, as required.

What the four cases test:
- M1 to M3 test the harness's bookkeeping against the record.
- M4 tests a failure computed in this lane.

## Controls (main run, all pass)

| control | what it checks |
|---|---|
| K1 | CFG467's committed JSON reproduces: I_strict EMPTY, I_len [9.6240e-14, 3.2000e-09], verdict TENSION |
| K2 | CFG373's perfect square, g^2 + a_L^2 = (g_N + a_L)^2 with a_L = a0/2 (sympy) |
| K3 | the P2 point-mass cold mass M(sqrt(1 + x^2) - 1) (CFG44 B1), to 3e-16 |
| K4 | a constant a0/2 anomaly reproduces the MI record's exclusions: Saturn 6686x, Mars 33430x |
| K5 | CFG357's Q2 constants, 3e-27 +- 3e-27 |
| K6 | nu_mono equals nu_RAR below y*; the maximum deviation is 0.01037 dex at y = 14.35 (the 09-26 user-decision numbers) |
| K7 | the interval engine and the classification and ranking logic, on toy rows |
| K8 | the Schwarzschild Kretschmann scalar, computed from the metric |

## Disclosures

**Not blind.** Every source lane was read before the criteria were frozen. The expected outcome was written into the
frozen file: GR would clear the chassis gates, and Cassini would depend on whether the Sun can hold fluid.

**How the statuses were assigned.**
- They are readings of committed files.
- Some sources are closure-map summaries or memory-level facts, and are tagged as such. These never upgrade a status to
  PASS.
- Astra results are marked "[U]" (unreviewed).
- "LIT-GR" marks standard GR theorems (hyperbolicity, PPN, Kerr regularity, c_T). They are not re-derived here; K8 is
  the one computed instance.

**Run 1 (kept verbatim).**
- K3 failed: 1.16e-10 against a 1e-10 line.
- The cause was float cancellation at x = 1e-3, where nu - 1 is about 5e-7.
- The fix rewrites the same identity in cancellation-free form, (nu - 1) = 1/(y(nu + 1)) for P2, with the same
  tolerance.
- Nothing else changed between runs, apart from three additions:
  - the N1f positive control, added after run 1, reported and not frozen;
  - grouped notes in the per-row printout;
  - a clearer note on R17's G14.

**N1f's null result needed a positive control** to show the detector works. The control was added after run 1, and
it finds the known negative lobe near an external-field saddle.

**Judgment calls that move the ranking.**
- NC1's G1 is UNT: the relaxation target contains grad A, so the principal symbol changes.
- NC1's H6 is PASS (CFG43 existence).
- R04's G11 is COND.
- If any of these were scored differently, NC1 and R04 could swap places. They are tied on every gate count.

**Not cited.** CFG462 and CFG483 results are uncommitted in another session.

**Scope of NC1's non-spherical target.** It is the AQUAL form of the declared kernel, not QUMOND. The difference has
not been tested on SPARC.

## What this lane cannot say

- It maps the record and runs first gate passes. It does not build an action for B, and it does not solve any coupled
  field equations.
- It does not show that NC1's fluid dynamics exist. CHASSIS-CLEAN would not have meant "the theory works", and NC1 is
  not even that yet.
- Not "theory closed". kappa = 1/2 is FITTED. No dark-matter particle is added; the cold fluid's mass is still required.
