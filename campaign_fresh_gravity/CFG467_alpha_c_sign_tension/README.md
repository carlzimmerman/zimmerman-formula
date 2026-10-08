# CFG467: the alpha_c axis of the relativistic chassis, and the sign tension

Criteria frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit 13d623cf4, committed alone before any script.
Theory only, offline, no downloads. Every source lane is read-only here.

| run | output files | checks | exit code |
|---|---|---|---|
| main | `cfg467_alpha_c_axis.out`, `cfg467_results.json` | 9/9 pass | 0 |
| MUTATE (`CFG467_MUTATE=1`: G1's sign convention flipped) | `cfg467_alpha_c_axis_MUTATE.out`, `cfg467_results_MUTATE.json` | 9/10 (K1 fails, as required) | 1, as required |

    python3 campaign_fresh_gravity/CFG467_alpha_c_sign_tension/cfg467_alpha_c_axis.py
    CFG467_MUTATE=1 python3 campaign_fresh_gravity/CFG467_alpha_c_sign_tension/cfg467_alpha_c_axis.py

Each run takes about 5 s.

## Verdict: TENSION (frozen rule)

**Bottom line.**
- With every gate at its strict reading, no value of alpha_c passes them all, at any c_2 in the window. The intersection
  is empty.
- It opens only if the black-hole gate is read leniently. That reading accepts CFG319's "option C", a mild singularity
  hidden on the universal horizon. With it, the surviving interval is exactly the record window,
  **alpha_c in [9.624e-14, 3.2e-9]**.
- No other relaxation opens it, alone or in any combination.
- With the strict black-hole criterion, the emptiness holds even when every other gate is relaxed. So under that
  criterion alone the result is **INCONSISTENT**.

**Where the clash sits.**
- It is a point against an open set. Fully regular moving black holes exist only at alpha_c = 0.
- Five gates exclude alpha_c = 0: hyperbolicity, lapse ellipticity, the F2a lapse kernel, strong coupling and the
  negative-lobe health condition. Four of them (G1, G2, G3, G5) are proofs within their scope.
- So the two sets do not merely miss each other. They touch only at a point that is itself excluded.

**How "TENSION" was reached.**
- The frozen rule counts the black-hole criterion choice as one of the stated uncertainties.
- CFG318 and CFG319 both state it that way: under the strict reading G11 is a KILL, and that call is the owner's.
- If the owner adopts the strict criterion, the verdict for the chassis is INCONSISTENT.

## The interval table

Setup:
- beta = 0, lambda_K = 1 + c_2, with c_2 on CFG320's 9-point grid over L340's window [7.29e-3, 0.0667] (leaf-average
  branch).
- c_S^2 = c_2 (2 - alpha)/(alpha (2 + 3 c_2)).
- Where an edge depends on c_2, it is shown at c_2 = 7.29e-3 / 0.0667.

Kinds of evidence:
- PROOF: exact symbolic or certified algebra, within the source's own scope.
- NUM: computed.
- LIT: an external bound read through a summariser, so PROVISIONAL.
- ARG: an argument or a count.

| ID | gate | source lane(s) | strict allowed alpha_c | lenient allowed alpha_c (stated uncertainty / alternative reading) | shown excluded | kind |
|---|---|---|---|---|---|---|
| G1 | strong hyperbolicity + criterion B (F2a gauge) | CFG292, CFG294 S1, XC2 B6 | (0, 1/2) U (1/2, 2) | (0, 2); alpha = 1/2 is an F2a gauge artefact | (-inf, 0] U [2, inf) | PROOF, linear frozen-coefficient principal symbol |
| G2 | lapse/U leaf system: ellipticity and UV positivity | CFG294 S4b (det = 4 N alpha k^4), CFG329 (coefficient (2C + alpha(1+C))/(1+C), C -> 0 at k >> 1/xi) | (0, inf) | same | (-inf, 0] | PROOF |
| G3 | F2a lapse kernel with W <= 0 | CFG294 S4c, CFG312 (Hardy factor 1/2 - alpha) | (-inf, 0) U (0, 1/2) | same | {0} U [1/2, inf) | PROOF, homogeneous class; Hardy is sufficient |
| G4 | strong coupling G8 | XC1 A4 (GSS2018 eq. 15) | [1.80e-16 / 3.67e-16, 2 - 3.3e-13 / 2 - 3.9e-14] (k_sc >= 1e3 x LHC) | [1.80e-20 / 3.67e-20, ~2] (k_sc >= LHC) | alpha <= 0 (no UV kinetic term) and the rest | NUM from a LIT formula, tree level, decoupling limit |
| G5 | negative-phantom-lobe health | L340 H4 | [9.624e-14, inf) (L340's estimate) | [2.75e-14, inf) (bisected on L340's own symbol; galaxy-in-group lobe) | (-inf, 2.75e-14) | PROOF that alpha <= 0 fails (large-k limit); NUM edge |
| G6 | PPN alpha2 (exact khronometric formula) | L340 P1, CFG291 | [-3.2e-9, 3.2e-9] U a tiny island at alpha = c_2/(1+2c_2), where c_S = 1 (\|alpha2\| <= 1.6e-9) | [-4.8e-7, 4.8e-7] U island (\|alpha2\| <= 2.4e-7) | the complement | LIT |
| G7 | PPN alpha1 = -4 alpha | CFG291, L340 P1 | [-2.75e-6, 2.75e-6] (1.1e-5) | (-8.25e-6, 8.75e-6) (Shao & Wex 2012) | the complement | LIT |
| G8 | binary-pulsar dipole | CFG291, CFG311 | [9.624e-14, 3.2e-9] (tested, 625/625) | (0, 3.2e-9] (CFG291 C6: the flux vanishes as alpha -> 0+) | none; alpha <= 0 and alpha > 3.2e-9 are untested | NUM with LIT formulas |
| G9 | cosmological G / BBN | L350 G1, G5 | (-0.2, 0.2) (leaf-average branch, \|alpha\|/2 < 0.1) | same | the complement | PROOF formula + LIT bound |
| G10 | G_N = G/(1 - alpha/2) > 0 | L350 G1, CFG320 K4 | (-inf, 2) | same | [2, inf) | PROOF |
| G11 | radiative stability G12 | CFG320 | without the hierarchy: [9.624e-14, alpha_rs(c_2)], with alpha_rs = 5.80e-14 / 1.18e-13. Empty for c_2 < 0.038; it reaches 1.18e-13 at 0.0667 | Pospelov-Shang hierarchy granted (M_* <= 9.9e8 GeV): [9.624e-14, 3.2e-9] | strict only: (alpha_rs, 3.2e-9] | NUM + LIT |
| G12 | black-hole regularity G11 | CFG318, CFG319 (+ RB2019, FHB2021) | reading S (regular everywhere outside r = 0): **{0}** | reading W (option C accepted): {0} U [9.624e-14, 1e-3] | strict: **(0, inf)**; alpha < 0 untested | NUM + ARG (count) + LIT |

**Gates that do not depend on alpha_c** (listed, not scored):
- Cassini Q2 (CFG357; the khronon is not in Q2).
- CFG312's W itself.
- GW170817 (it fixes beta only).
- L340's tracking condition (c_2 only).
- CFG318's exterior observables. They pass at every window alpha; even alpha = 0.1 is not flagged.
- PPN gamma and beta. In khronometric theory they do not depend on alpha (a literature reading); they are not computed
  for C-H/K on the record.
- Lanes that use alpha_c without imposing an interval on it: CFG321, CFG348, CFG373, CFG381. CFG172D's PPN formulas belong
  to V0, not to this chassis.

### What the black-hole lanes say, stated precisely

- **On the record, a fully regular slowly moving black hole exists only at alpha_c = 0**, the stealth maximal-slicing
  solution (CFG319 control C1).
- **For alpha_c > 0 there is none.**
  - The boundary-condition count is 4 constants against 5 conditions, for every alpha > 0, in the test-khronon limit.
  - This is confirmed numerically at the five window points and on a ladder from 1e-7 to 1e-3 (CFG319).
  - It agrees with RB2019 and FHB2021 (literature, provisional).
- **What does exist at alpha_c > 0 is option C.**
  - It is regular everywhere outside the universal horizon (UH).
  - On the UH it has an integrable gradient singularity, x^-0.382, hidden from every signal.
  - Its exterior imprint is at most 3e-13.
  - Kovachik & Sibiryakov 2023/25 (as recorded in the extra_crispy README, provisional) find regular solutions "outside
    the universal horizon" for small alpha. That matches option C, not reading S.
- **alpha_c < 0 is examined by no lane.** The record does not say "regular for alpha_c <= 0".
  - Reading r2 (not scored): for alpha < 0 and c_2 > 0, CFG319's S22 = -8 Y^4 (n W^2 + l Y^2)/(...) never vanishes. So
    there is no spin-0 horizon, and the r_S condition drops out of the count.
  - That is a count, not an existence result.
  - Either way, alpha < 0 is excluded by G1, G2, G4 and G5 (three of them proofs), so it cannot open the intersection.

## The intersections

- **I_strict = EMPTY** at all nine c_2 values.
- **NX = EMPTY.** NX is the set not shown excluded by any strict gate, so every point of the real line is positively
  excluded by at least one gate. alpha <= 0 is excluded by G1, G2, G4 and G5 (G3 too at 0); alpha > 0 by G12 reading S.
- **I_len = [9.624e-14, 3.2e-9]** at every c_2.
  - Its edges are where the lanes were tested, not physical edges.
  - The lower edge is set by G11/G12's tested ranges, which start at L340's alpha_min estimate.
  - The upper edge is set by G8/G11's tested ranges, which stop at the PPN alpha2 bound.
  - G5's bisected threshold (2.75e-14) and G4's (1.8e-16) lie below it.
- **Lenient everywhere except G12 held strict: EMPTY.** This is the robustness statement for the strict black-hole
  reading.

**Who excludes what** (strict sets; the same at every c_2 except where noted):

| alpha_c | shown excluded by | not shown allowed (untested) by |
|---|---|---|
| -1e-9 | G1, G2, G4, G5 | G8, G11, G12 |
| 0 | G1, G2, G3, G4, G5 | G8, G11 |
| 1e-15 | G5, G12 | G8, G11 |
| 1e-13 | G11 (at c_2 = 7.3e-3 and 0.022, not at 0.0667), G12 | none |
| 1e-11 | G11, G12 | none |
| 3e-9 | G11, G12 | none |
| 1e-6 | G6, G12 | G8, G11 |
| 0.1 | G6, G7, G12 | G8, G11 |
| 0.5 | G1, G3, G6, G7, G9, G12 | G8, G11 |
| 1 | G3, G6, G7, G9, G12 | G8, G11 |

## The minimal change that would open it

All 2^8 combinations of the eight relaxable gates were enumerated. **The only minimal opening set is {G12}.**
- Relaxing G12 alone, with G11 still strict (no hierarchy), opens [9.624e-14, alpha_rs(c_2)]:
  - only for c_2 >= 0.038;
  - [9.624e-14, 9.93e-14] at c_2 = 0.0383, up to [9.624e-14, 1.18e-13] at 0.0667;
  - this is CFG320's own "3/81 points" sliver.
- Adding G11's hierarchy reading opens the full record window.

The changes, from the record:

1. **Adopt reading W for black holes.** The criterion becomes regularity outside the universal horizon, with an
   integrable, signal-hidden singularity on it allowed.
   - **No new constant.**
   - It is a change of criterion, and it is the owner's call already flagged by CFG318 and CFG319.
   - It is a strong-cosmic-censorship-type choice, not a mechanism.
2. **A UV sector that regularises the universal horizon at alpha_c > 0.** These are Horava higher-spatial-derivative
   terms, acting at the scale where CFG319's x^-0.382 gradients diverge.
   - **+1 constant** (the anisotropic scale M_*).
   - It might be the same M_* <= 9.9e8 GeV that CFG320's hierarchy reading already names. That would be one constant
     serving G11 and G12 together.
   - **Untested.** CFG319 lists it as an argument, not a computation.
3. **Move the chassis to alpha_c <= 0.** This needs G1, G2, G4 and G5 to change at once; three of them are proofs.
   - In this khronometric family the scalar's only UV kinetic coefficient is alpha_c.
   - So this means a new kinetic operator for the khronon with its own coefficient: **at least +1 constant**.
   - Black-hole regularity would then have to be re-derived from scratch.
   - **Not minimal.**

One reading row points the other way (r1, not scored):
- CFG294's physical velocity-fixed lapse form, alpha |k|^2 + W, is resonance-free with W < 0 only for alpha <= 0.
- CFG294 records that resonance, and states that F2a, the operator the scheme actually inverts, has none.
- It is not a gate, but it is a second place on the record where alpha_c > 0 costs something.

## MUTATE

G1's sign convention is flipped (alpha -> -alpha), as CFG292's own C4 did.
- K1 fails, because the flipped gate contradicts CFG292's committed characteristic polynomial. rc = 1.
- **The intersection logic responds:**
  - I_len goes from [9.624e-14, 3.2e-9] to EMPTY;
  - the verdict goes from TENSION to INCONSISTENT;
  - no relaxation opens it.
- M1, computed in the same process, confirms that the two intersections differ.
- **Control K8:** flipping every gate's convention at once mirrors I_strict, I_len and NX exactly, and leaves the verdict
  unchanged (mirrored I_len = [-3.2e-9, -9.624e-14]).

## Controls (main run, all pass)

| control | what it checks |
|---|---|
| K1 | G1 is derived from CFG292's committed F2a scalar polynomial (parsed): c_S^2 reproduced exactly, real speeds iff 0 < alpha < 2 at every grid c_2; the committed lapse coefficient (2 alpha - 1)/4 vanishes only at 1/2 |
| K2 | the G4 formula reproduces XC1's committed minimum k_sc, 8.479852e8 GeV, exactly |
| K3 | the re-implemented L340 H4 symbol reproduces all eight committed booleans; the inertia at the top k is negative for alpha = 0 and -1e-20 in every negative lobe |
| K4 | the exact alpha1 and alpha2 reproduce CFG291's four committed PPN corners to 1e-6 |
| K5 | Lambda_sc reproduces CFG320's min and max (8.479852e8, 3.555315e12 GeV); the no-hierarchy sub-window holds exactly CFG320's three committed grid points |
| K6 | CFG319's committed JSON: full_regular all False at the five window points, option C admissible at all five, C1 (alpha = 0) passed |
| K7 | the set engine on toy sets, and mirror() |
| K8 | the mirror control above |
| K9 | no gate takes a0: the sets are identical under the canonical and alt footing labels. This is a bookkeeping check; both footings give the same axis |

## What this implies for candidate B

**Untested for B.** B has no action, so none of these gates has been computed for it.

The tension lives in the khronon sector:
- the alpha_c a.a term;
- the UV principal symbol;
- the universal horizon of black holes.

At those wavenumbers the heat filter removes the MOND sector entirely:
- XC1 A3;
- CFG318: a suppression of exp(-552) at M87*.

So a bound-only switch acting on the MOND law cannot reach it. Any action for B built on this chassis inherits the same
TENSION, unless B's khronon sector differs from L340's. If the owner adopts the strict black-hole criterion, the
inheritance is INCONSISTENT. This is a statement about the chassis B would sit on, not a test of B.

## Disclosures

- **Not blind.** Every source lane was read before the criteria were frozen, and the outcome was anticipated: empty under
  strict S, open under W. The strict and lenient sets were fixed in FROZEN_CRITERIA before the script existed, and
  nothing was changed after the run.
- **The verdict word depends on one framing.** TENSION depends on counting the black-hole criterion choice among the
  "stated uncertainties". The source lanes state it as an owner call. Read as a settled criterion, the strict reading
  gives INCONSISTENT.
- **New computation here, beyond reading:**
  - G5's bisected threshold, 2.75e-14, against L340's estimate of 9.624e-14. It does not move the verdict, because I_len's
    lower edge is set by the tested ranges of G11 and G12.
  - G4's exact roots.
  - The exact PPN alpha2 island at c_S = 1.
- **Edges that are tested ranges, not bounds.** G8, G11 and G12 (lenient) are allowed only where their lanes computed.
  That is why I_len equals the record window: the window is where everything was run.
- **Literature is PROVISIONAL**, as in the source lanes: the PPN bounds, BBN, Pospelov-Shang, RB2019, FHB2021 and
  Kovachik-Sibiryakov.
- **Inherited, not re-adjudicated.** CFG291 flagged that L340's alpha1 bound of 1.1e-5 matches no tabled value; it is
  used here as the strict alpha1 row and is non-binding. The c_2 axis's own problem is out of scope: the plain-branch
  Planck-era ceilings lie below L340's c2_min (L350).
- **Implementation.** Three parsing/robustness edits were made before the first run, with no change of rule: the scalar
  factor is read by polynomial coefficient extraction instead of solve(lam^2); "lambda" in the committed sympy strings
  is renamed before parsing; mpmath numbers are converted to sympy Floats through strings. After the first run, the
  edge-binding report and the G4 upper-edge print were added (reporting only). Both kept runs come from the final script,
  and the first run's verdict and sets were identical.

## What this lane cannot say

- It maps committed results. It does not prove that any gate holds outside its source lane's scope, which is linear,
  frozen-coefficient, test-khronon, tree-level and so on.
- It does not compute black-hole regularity with Horava UV terms, a coupled-metric moving black hole, or anything at
  alpha_c < 0.
- It is one axis of one chassis. It is not "the theory works", and not "theory closed". kappa = 1/2 is FITTED. No
  dark-matter particle is added, and the cold fluid's mass is still required.
