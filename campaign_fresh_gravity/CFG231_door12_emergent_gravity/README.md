# CFG231 — Door 12: covariant and elastic completions of emergent gravity against the CFG44 target (phase 2)

- **Criteria:** `CFG231_FROZEN_CRITERIA.md` (revision 2, sha256 `55e3220c…`, committed as "CFG230 / CFG231 / CFG232: frozen criteria" before any script). The shared gates G1–G5 are in `closure_map/TEN_DOORS_GATES_2026-09-29.md`. **The menu of variants was written knowing the target, door 2's result (CFG117) and the CFG44 B1 N5 output; the hand estimates were not blind.**
- **Scripts (numpy / scipy / sympy / mpmath; the whole set runs in about 15 s):** `CFG231_common.py`, `CFG231_A1_point_mass_algebra.py`, `…A2_sphere_charge_function.py`, `…A3_vector_class.py`, `…A4_cosmology.py`, `…A5_reaction_energy.py`, `…A6_solar_stability.py`, `…A7_normalisation_ledger.py`, `CFG231_verdict.py`, `CFG231_run_all.sh`. Outputs: `*.out`, `*_results.json`, and `*_MUTATE_<mode>.out/.json`.
- **Repo untouched.** `Bcommon` (CFG44) and `Gcommon` (CFG48) are imported read-only for constants and controls. Repo root from `ZF_REPO` or by walking up from `__file__`; printed as `<repo>`. No absolute home path appears in any output.
- **Re-run:** `ZF_REPO=<repo> bash CFG231_run_all.sh` from the lane directory (or without `ZF_REPO` when the directory is `<repo>/campaign_fresh_gravity/CFG231_door12/`). A re-run reproduces every `.out` and `.json` byte-for-byte apart from timing lines (checked). Exit convention: a main script exits 0 iff its reproduction controls pass; a `MUTATE=<mode>` run exits 1 iff the control **bites** (the named headline differs from the main run), 0 otherwise (a declared control failure, kept).
- κ = ½ and Ω_c h² stay fitted. **Nothing here says the theory is closed or that any data favour it, and nothing says emergent gravity is refuted outside the frozen class.**

## Bottom line

**A scoped no-go on G1 for every variant of the frozen class; nothing passes G1, so nothing is flagged for the independent re-derivation of a pass (§ "G1 as a derived mechanism").** Binding gate: G1 for all eight variants. The one variant that reproduces the point-mass target (K1, the P2 kernel restated) fails G1 strict on the exponential spheres and on the alt a₀ footing, and independently fails G5 (Solar-System tail, Q₂ = 6.1e3 × the bound).

Three findings that were not in the frozen file and that the scripts produced:
1. **Point mass:** R = f′(1+f)/x = d[(1+f)²]/d(x²), so R ≡ 1 iff (1+f)² = 1+x² — the P2 law and nothing else (sympy, C2). Verlinde-type laws give R = (1+x)/x (C3); the "simple wall" gives R = 1 + 1/√(1+4x²) (C4).
2. **A vector with an attractive static force needs a wrong-sign (ghost) kinetic term** (A3.1, A3.2): like charges of a spin-1 field repel. The frozen V1 assumed an attractive drag and never set the sign; with s = −1 both the radial and the transverse kinetic coefficients (s D′, s D/E) are negative for K1, K2, K3, although D′ > 0, D/E > 0 and 0 < c_s² ≤ ½ (the frozen G5 (i) conditions) hold.
3. **The total-mass reading (B4) passes an R-only test on the point mass** (R = 1 exactly) but has negative dark mass and g_tot < g_N for x < 1; the admissibility line added in revision 2 is what fails it (MU8).

## Gate table per variant (H_Λ primary; H₀ in the A2 / A7 outputs)

PASS / FAIL / UNDEFINED / NOT ADDRESSED; **p\*** = passes only trivially or by construction. Each cell cites its script. Variant definitions: `CFG231_FROZEN_CRITERIA.md` §1.

| variant | G1 strict (cells passing, N-shape / canon / alt, of 14) | G1-P2 reading | G1 mechanism | G2 | G3 reaction / energy | G4 | G5 |
|---|---|---|---|---|---|---|---|
| **V0** canonical vector | FAIL 0/0/0 (R = 0 on the point mass; A2) | FAIL | n/a (no scale; A1 C9) | FAIL on growth ratio 1.093, literal G_eff line P (0.024); CMB, no-cold UNDEFINED (A4) | p\* / mixed (sphere 0.57–6; point mass cutoff-dominated 1e3) (A5) | FAIL (no acceleration scale) (A7) | Solar System p\*; stability FAIL (ghost sign) (A3, A6) |
| **V2** gravitating vector (K1) | FAIL 0/0/0; inadmissible (M_D < 0); R ~ 1e-11 to 8e-5 (A2, A3.4) | FAIL | n/a | p\* (modification ~1e-6); CMB UNDEFINED (A3.4) | p\* / FAIL 3.4–6.3 (A5) | FAIL (A7) | p\*; stability FAIL (ghost, negative dark mass) |
| **B1** Verlinde, derivative form | FAIL 0/0/0 (point mass (1+x)/x; spheres up to 18.5) (A2) | FAIL (1.18) | M1 | FAIL (A4) | p\* / UNDEFINED (no action); K2 reading FAIL | P count only (A7) | Q₂(a) FAIL 1.0e7×; Q₂(b) pass; stability UNDEFINED (A6) |
| **B2 = K2** derivative-free | FAIL 0/0/0 (spheres up to 11.2) (A2, C10) | FAIL (0.414) | M1 | FAIL, growth ratio 1.27–24.5 (A4) | p\* / FAIL 3.9–15.3 (A5) | P count only | Q₂(a) FAIL 1.0e7×; Q₂(b) pass; ghost sign FAIL (A3, A6) |
| **B3** B1 + onset gate | FAIL 0/0/0 (R = 0 for x < 0.577) (A2) | FAIL | M1 | FAIL (A4) | p\* / UNDEFINED | P count only | Q₂(a) pass **only by the gate**; Q₂(b) pass; a varied gate meets DE12/13 (statement) (A6) |
| **B4** total-mass reading | FAIL 0/0/0: R-only passes 7/7 point masses in N-shape but inadmissible (A2, MU8) | FAIL | M1 | FAIL (A4) | p\* / UNDEFINED | P count only | Newtonian force removed (Q₂ 1.8e10×); γ FAIL (g_tot/g_N = 1.2e-3 at Saturn) (A6) |
| **K3** simple wall | FAIL 0/0/0 (R = 1 + 1/√(1+4x²); in band only for x ≥ 4.98) (A1 C4, A2) | FAIL (0.155) | M1 | FAIL, growth ratio 1.24–23.7 (A4) | p\* / FAIL 3.7–7.2 (A5) | P count only (one declared wall ratio) | Q₂(a) FAIL 1.2e4×; Q₂(b) pass; ghost sign FAIL |
| **K1** P2-inverse (wall a/2) | **FAIL 9/10/0** (point mass 7/7 in N-shape and canonical, 0/7 on alt; spheres pass only for M ≥ 3e11 (N-shape) or ≥ 1e11 (canonical); A2) | **PASS** (6.7e-16: K1 is P2) | M1 (declared, P2 restated); KODE control M0 (C8) | FAIL, growth ratio 1.22–23.1 (A4) | p\* / FAIL 3.4–6.3 (A5) | **FAIL strict** (wall fixed with knowledge of the target) (A7) | Q₂(a) FAIL **6.1e3×**; Q₂(b) pass; ghost sign FAIL (A6, A3) |

Notes on the table.
- H₀ instead of H_Λ: K1 gives 9 / 0 / 10 cells (N-shape / canonical / alt); the two footings swap roles (a_V/a₀ = 1.166 canonical, 0.965 alt), so **no H choice passes both footings**; B4's R-only counts move the same way. G4 additionally fails the tie clause for H₀ (tie to the critical density, κ_V′ = 0.5829).
- G2 "no-cold" and the CMB TT/TE/EE are UNDEFINED for every variant: the linear theory about E = 0 has vanishing stiffness (A3.6, A4) and no Boltzmann treatment exists. At z = 1000 the K-law modification is small (y_lin = 25, Newtonian regime), so the estimate does not exclude the CMB epoch; it does not decide it either.
- G3 reaction is p\* for every variant: a spherical E(r) is a potential force, so the force beyond the gradient of a potential is identically zero (A5.4). The G3 energy is 3.4 to 15 times the baryons' orbital energy for the K laws (logarithmic in r_e/r_M, see the failed hand estimate below), in both r_ta conventions (which reproduce the CFG48 referee's table, C-rta).
- Gate G5 c_T = c and γ: statements (minimal coupling, potential force); P for every variant except B4 (γ).

## Binding gate per variant

V0: G1 (no scale) and G5 (ghost). V2: G1 (dark mass ~1e-6 of the needed and negative). B1, B2, B3, K3: G1 (shape; the point-mass ratio is fixed analytically). B4: G1 admissibility. **K1: G1 strict on the spheres and the alt footing, and independently G5 (Q₂ 6.1e3×).** Confirms the frozen expected binding gate.

## G1 as a derived mechanism — the flag asked for

**Nothing passes G1 strict, and nothing is graded M2.** A1.2 recorded five attempts to derive the constitutive function D(E) = E²/(a−2E) (Born–Infeld has no deep regime; the AQUAL power law has no wall; a walled family reproduces K1 only at its fitted point (p, E_w) = (1, a/2); dimensional analysis leaves F(E/a) free; and D(E) is exactly the inverse of P2, so deriving it is deriving P2). So the independent re-derivation reserved for a pass (frozen §7) is **not triggered**. What remains useful is a referee re-run of the no-go headlines (the point-mass algebra, the sphere charge function, the Q₂ figures, the ghost-sign statement).

## What transfers to Hossenfelder's paper only if her action lies inside class V

Class V is a **reconstruction** (frozen §1.2): what the repo records of her paper is one abstract-level sentence and a few second-hand statements (§0B, L2–L5, all from memory and unverified). Every statement below is about the frozen class and reaches her paper only if her action reduces, in the static spherical weak-field limit, to the local electrostatic Gauss law D(E) = ε g_N with a linear sum g_tot = g_N + E (or to one of the algebraic readings B1–B4).
- **Transfers if inside V:** (i) the point-mass charge function R = f′(1+f)/x: a deep-only law (her reported limit, L4) gives R = (1+x)/x, in band only for x ≥ 10 (CFG117 [S], reproduced by C3); passing G1 on the point mass needs exactly P2, i.e. an added Newtonian-regime function, which her theory reportedly does not have (L4) and which is then an extension whose shape is declared; (ii) the sphere result: for any local deep-limit law the core limit is R → 5/2 (C6, sympy), so the exponential-sphere target is missed at small x for diffuse spheres (R(0.1) = 2.3 to 2.6 at 1e9 M☉; B1 up to 19.5 for compact ones); (iii) the Solar-System tail: the isolated-Sun tide/bound ratios 1.0e7 (K2/B1/B2), 1.2e4 (K3), 6.1e3 (K1) are properties of any law whose anomalous acceleration at Saturn is √(a g_N) or a/2 (and become zero only if a mask switches the force off, B3); (iv) the sign: a single spin-1 electrostatic sector with a real coupling repels like charges, so an attractive drag is a ghost (A3.1).
- **Does NOT transfer, and is not claimed:** her stability statements (L5: the corrected de Sitter solution and the growth of perturbations) — A3.6 finds the elastic sector's quadratic action vanishes about E = 0 (UNDEFINED) and the background vector value is not fixed by V; her exact field content, any scalar or Lagrange-multiplier sector, a non-minimal curvature coupling, a constraint that changes the kinetic sign, a nonlocal or derivative term that would produce the d(M_B r)/dr piece of B1, and any coupling to photons (lensing). If her action contains such a term, none of the verdicts above applies to it.

## MUTATE outcomes (each flips a load-bearing cell; exit 1 = the control bites)

| mode | script | what it does | result |
|---|---|---|---|
| MU1 prescribe the profile | A2 | replace every variant's M_D by the target's own ODE solution (KODE) | **bites**: G1 strict flips F → P for all 8 variants on every cell; mechanism grade M0 |
| MU2 area-law only | A6, A7 | a_V → 0 (no volume term) | **bites** (both): K1's Q₂ flips F (6.1e3×) → P (0); G1 stays F (R = 0); the normalisation cell a_V/a₀ 0.965 → 0 |
| MU3 flip the sign (healthy vector) | A6 | s = +1: the drag becomes repulsive | **bites via G1** (K1 point mass R(0.1, 1, 10, 30) = −0.99, −0.41, 0.80, 0.93; P → F). **Frozen expectation wrong in direction:** the stability cell moves F → P (the main run is already a ghost), not P → F. Kept |
| MU4 swap the footing | A2, A7 | K1 at H_Λ scored against alt instead of canonical | **bites** (both): point-mass N-tie cell P → F (7/7 → 0/7; a_V/a₀ 0.965 → 0.7985); H₀ vs canonical is 0/7 |
| MU5 point mass only | A2 | K1 restricted to the point-mass grid | **does NOT bite** as frozen (exit 0): strict still F because the alt footing fails on the point mass too (R → 0.7985); only the shape + canonical sub-line flips F → P. A declared control failure of a frozen claim; kept |
| MU6 remove the onset gate | A6 | B3 → B1 | **bites**: Q₂ P (0) → F (1e7×); G1 R(0.1) point mass 0 → 11 |
| MU7 gravitating reading | A6 | V1 drag → V2 field-energy source | **bites**: K1 G1 P → F (R → −6e-7 at x = 0.1, negative) |
| MU8 admissibility off | A2 | B4 without the admissibility line | **bites**: B4's point mass passes 7/7 in N-shape (R = 1); the line is what fails it |

## Reproduction controls (frozen §4)

C1 CFG44 point-mass identities (A1, sympy + Bcommon target to 7e-12): PASS. C2 uniqueness (A1): PASS. C3 (1+x)/x (A1): PASS. C4 K3 closed form (A1): PASS. C5 P2 phantom on the N5 profiles (A2): R ∈ [1.000, 2.279] compact, [1.000, 2.484] diffuse — matches CFG44 B1 N5 to 2%: PASS. C6 core limit 5/2 and g_T² = (2/5) a g_N (A2): PASS. C7 Q₂ recipe 6.3e3 (A6): PASS (6.306e3). C8 KODE passes every cell, M0 (A2): PASS. C9 canonical-vector null (A1, A3.5 mpmath Yukawa Green's function): PASS. Additional: C10 B2 ≡ K2 (A2), C-rta (A5), C-FCKH (A6), G4.1/G4.1b (A7): PASS.

## Failed controls and wrong expectations (all kept)

- **C9b (reported, FAIL):** the frozen hand estimate "Yukawa effect at galactic r ≲ 1e-12" is wrong by 1.7 (the correction (mr)²/2 is 1.7e-12 at 10 kpc, 1.6e-9 at 300 kpc); inert.
- **Script bugs found on the first runs, fixed before any result was recorded:** C4 compared to closed forms at nominal x instead of the actual grid nodes; the C8 threshold I added (Bcommon agreement 1e-5) was too tight: my deep-core-start solver differs from Bcommon's target g_tot by 2.9e-4 on the 1e10 sphere because Bcommon starts from the algebraic P2 value at 1e-3 r_M; started exactly as Bcommon starts, my solver reproduces it to < 1e-6 (C8b, added). The first draft of A4's G2.4 said the force is "enormous" at z = 1000; wrong (y_lin = 25, the Newtonian regime), corrected before recording.
- **G3 energy hand estimate wrong:** the frozen text said "O(1) × r_e/r_M ≈ 10–300". The field energy density is cubic in E, so the energy is (4/3)√(a/a₀) ln(r_e/r_in) × ½ M V_f² (A5.2, closed form matched to 0.1%), i.e. 3.4 to 15, not tens to hundreds. The verdict (F) is unchanged.
- **MU3's stability prediction (P → F) wrong in direction**, and the ghost-sign finding was not in the frozen file (above). The G5 verdict was already F through Q₂.
- **MU5 does not bite** (above).
- **V0 on G2:** the frozen estimate was F; the outcome is a split (literal |G_eff/G − 1| line P at 0.024, growth ratio 1.093 F), headline F.
- **K1 on the spheres is mass-dependent** (not anticipated in that form): R(0.1) = 2.31, 2.11, 1.75, 1.36, 1.11, 1.03, 1.01 for 1e9 … 1e12 M☉; the strict cell passes only for M ≥ 3e11 (N-shape) and ≥ 1e11 (canonical). "Same constants at every mass" fails on the low-mass side.
- **B4 spheres:** R(0.1) goes negative for the heavy compact spheres (−1.8, −4.8, −7.6 at 1e11, 3e11, 1e12): negative dark density, not anticipated.
- **Frozen estimates that held:** K1 point mass R = 1 (P); K3 R = 1 + 1/√(1+4x²) with the band at x ≥ 4.98 (hand 4.98); Q₂ tails 6.3e3, 1.2e4 (hand 1.3e4), 1.0e7; K3 G1-P2 15.5% (hand ~14%); V2 R ~ 1e-6 (measured 1e-11 to 8e-5, negative); G4 K1 F, K2 and K3 P-count, V0 and V2 F; Verlinde on the mean density M_D/M_b = 137 at 1 Mpc (G2.5).

## Prior work inherited (frozen §0A; what the scripts showed)

| earlier file | its verdict | inherited | what this lane showed |
|---|---|---|---|
| CFG117 README + criteria (b09ca1480, lane bb504274c) | door 2: G1 F; (1+x)/x; G2/G3 UNDEFINED; G5 F | the formula, the a_V/a₀ table, the untested list | (1+x)/x re-derived (C3); a_V/a₀ table reproduced (G4.1); the untested item is this door: **no action-based variant passes G1** |
| `VERLINDE_DEEP_DIVE_2026-06.md` | Hossenfelder 2017 covariant form: no interpolating function, one parameter fixed, partial and disputed | claims L2–L7 for the data chat; 12c scoped as an extension | K1/K3 (declared Newtonian-regime functions) fail G1 strict; the deep-only K2/B1 fails by (1+x)/x; nothing is attributed to her paper |
| `verlinde_foundation_stress_test.md`, `agentP…`, `agentH1…` | covariant version unstable around de Sitter; dead at the Solar System (Hees et al.) | L5 as a claim to check | A3.6: the elastic sector's quadratic action vanishes about E = 0 (UNDEFINED), the Proca sector with the attractive sign is a ghost; L5 neither confirmed nor refuted; Solar System: K2 Q₂ 1.0e7× (Hees's seven orders reproduced in kind) |
| Route 3 (`route3_entropic_gravity_2026.py`, `route3B…`) | DEAD as a survivor; Theorem V1 (M_D as total deep-MOND mass); "covariantisation dilemma" | V1 → variant B4; the dilemma as a hypothesis | B4: R = 1 on the point mass but inadmissible (MU8), γ FAIL; the dilemma's direction is consistent with A3/A6 (Q₂ FAIL for every ungated variant, ghost sign), but Route 3's Q₂ (assumed external field, 17×) is a different recipe and is not compared; the k-essence static-stress theorem is a scalar theorem: for the vector, p_r = −ρ and p_t = (s/4πG)Λ, so p_t + ρ ≠ 0 (A3.3) |
| `COVARIANT_MI_FIELD_THEORY.md` (v7) | the framework's own modified-inertia theory | nothing (different sector) | not scored |
| AeST files citing Mistele–McGaugh–Hossenfelder | AeST lensing; a different class | nothing | not scored |
| `E_literature_a0_coefficient/README.md` row | tie "by order of magnitude"; 1/6 imported from Verlinde (grouped, unresolved) | L8 as a G4 caution | G4: B-variants P (count only) with κ_V = 0.4824 replacing κ; tie clause fails for H₀ |
| the rest (bibliographies, dossier, sweeps) | citations; a "✅" tick | nothing | see tension 4 |

## Record tensions (frozen §9) and what the scripts showed

1. **`GATES_STATUS` row 5.12** ("the target gives the inner profile exactly for P2"): reproduced in kind that it holds for the point mass only. C5 recomputes CFG44 N5's charge-function ranges for the P2 phantom on extended profiles ([1.000, 2.279], [1.000, 2.484]); A2 shows K1 (= P2) fails the exponential-sphere target for M < 1e11 M☉.
2. **CFG172's G1 reading versus this lane's G1 strict:** K1 passes G1-P2 (6.7e-16, it is P2) and fails G1 strict (9/14, 10/14, 0/14): the difference of reading is real and numerically large. 11C-a/b/c are not re-scored here.
3. The first scoping message's lane label: withdrawn.
4. **TOE-dossier tick versus "partial, unstable":** not adjudicable offline; the scripts say nothing about her action beyond the class-V statements above.
5. **Two forms of Verlinde's M_D:** B1 (derivative) and B2 (M_B only) agree on the point mass and differ on spheres: worst R − 1 is 18.5 for B1 and 11.2 for B2 at H_Λ (A2; sensitivity to CFG117's h(M) in A2.3). Both fail.
6. **Added versus total M_D (L9):** the total-mass reading B4 satisfies R = 1 on the point mass and fails admissibility, γ, and the Newtonian regime; the added reading (B1–B3) fails by (1+x)/x. Neither passes.
7. **The pre-campaign a₀(z) number** (0.0060 at recombination) is not used. D1 (reported only): a_V(z)/a_V(0) = E(z) = 1.79, 3.77, 8.30 at z = 1, 2.5, 5, the rival ∝ H(z) type; a fixed H_Λ tie gives 1.
8. **Q₂ recipes:** this lane uses CFG7 H1 (tide = max(|dg/dR|, g/R); isolated Sun at 9.54 AU and the Milky-Way tide, standard budget). For the MW tide the K laws give tide/bound 2.9e-5 to 7.4e-5 (pass); the isolated-Sun tail is what fails. Route 3's assumed-EFE Q₂ is a different quantity.

## What was NOT tested

Her Lagrangian term by term (no offline access); the Pardo comment; non-minimal curvature couplings (c_T); a vector norm-fixing constraint, scalar or nonlocal sectors that could alter the kinetic sign or produce B1's derivative term from an action; time-dependent solutions and the vector's Noether momentum balance (G3 reaction is a by-construction statement); the de Sitter growth claim L5 (UNDEFINED here); Boltzmann-code CMB; nonlinear cosmology and clusters; non-spherical baryons; lensing (D2: the drag force does not deflect light, not scored); external-field and ownership physics beyond the diagnostics D-EFE and D-own: A3.7 confirms the Lean premise ν(y)√y → 1 for K1–K3 (so, as pointwise laws and by the certified no-EFE theorem, each has an EFE; the field-equation version is not formalised) and a local action cannot realise ownership ([T] + the [H] bridge). CFG250, CFG251, CFG252 and the pending ChainCert Action / Dimension / FluidLink batch are untouched (in flight elsewhere).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## In-place re-run (orchestrator)

`bash CFG231_run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`; about 15 s): the eight main runs exit 0, the ten MUTATE runs exit as expected (MU1, MU2, MU3, MU4, MU6, MU7, MU8 exit 1; MU5 exits 0 and does not bite, kept as a declared control failure), `overall: OK`. Every `.out` and `_results.json` is identical to the author's apart from one timing line. The frozen criteria are `../CFG231_FROZEN_CRITERIA.md` (revision 2, 55e3220c, committed in b31f5e705). This README was named `CFG231_README.md` in the author's scratch directory.
