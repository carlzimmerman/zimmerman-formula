# VR1 FROZEN CRITERIA: a vacuum-response identity behind kappa = 1/2? (2026-11-08)

Owner named this lane on 2026-11-08 (it overrides the 11-07 "no new lanes" and the 11-03 "do not reopen kappa" notes
for this lane only). Written and committed ALONE, before any script, Lean file or derived number. Adopts nothing.

## 0. Question

The law is a0 = kappa c sqrt(G rho_DE); kappa = 1/2 is FITTED (CFG493: kappa_Lambda 0.417 +- 0.095, kappa_crit
0.345 +- 0.078). `KAPPA_LOGIC_2026_10_20.lean` (fable_independent_2026/lean_2026/) proves `half_not_derivable`: the
structure `Framework` with premises
- `einstein`  Lambda = 8 pi G rho / c^2
- `friedmann` H^2 = 8 pi G rho / 3
- `tie`       a0^2 = kappa^2 G rho c^2
- `fourform`  kappa^2 = 2 beta^2 / (Z + 2 b0 beta^2)
admits kappa = 1/2 and kappa != 1/2 (and stays so with the CFG493 window added).
FINAL_THEORY_2026_11_07 section 4 names the missing piece: "the vacuum-response identity behind kappa = 1/2".

VR1 asks: is there ONE new, physically stated premise about how the vacuum (dark energy) responds to the khronon
acceleration A that (a) forces kappa = 1/2 exactly and (b) is not a restatement of the answer? Secondary: does that
identity say anything about the cold component (COLD DARK ENERGY, 5.41 x baryons at recombination, held by
clusters, absent from galaxies)?

## 1. What counts as a derivation (all required for DERIVED)

D1. The identity is written in words and in one equation below, BEFORE kappa is computed from it.
D2. It is a new premise outside `Framework`: it is not any of einstein / friedmann / tie / fourform, and not a
    forbidden input of KAPPA_CAMPAIGN_RULES section 2 (no Lambda = 32 pi a0^2/c^4, G rho = 4 a0^2/c^2, W_v = 4,
    J = 1, xi = 1, "couples through G not 8 pi G" (premise A), no measured a0, kappa, Z, Omega ratio).
D3. No free number chosen after seeing 1/2: every admissible variant (convention, identification, branch) is listed
    in the option space below now, with equal weight. If more than one option is admissible and they disagree, the
    candidate is at best CONDITIONAL.
D4. Counterfactual (rules S2): the identity must fail for kappa != 1/2. An identity that every kappa satisfies is an
    IDENTITY in the sense of RESTATEMENT (it carries no information on kappa).
D5. Mutation twin: a stated change of the identity gives a different kappa (or no solution). If the mutation leaves
    kappa unchanged, the candidate fails D5.
D6. Mass-independence (rules S1): kappa may not depend on a host mass, radius or any fitted record constant
    (L*, mu_K, gamma_L); if it does, the candidate is NO IDENTITY (TRADE).
D7. Lean: the implication (Framework + identity => kappa = 1/2) compiled with Mathlib, standard axioms only, no sorry,
    plus a _MUTATE twin whose false statements FAIL to compile (record procedure, V3_PICTURE_2026_10_23_MUTATE).
    Compile with `lake env lean <abs path>` from "new_physics copy/zimmerman-formula/fable_independent_2026/lean_2026".
D8. Second prediction (rules S4): the identity must fix one other measurable quantity. Without one, the best label is
    CONDITIONAL even if D1-D7 pass.

## 2. Labels (per candidate; fixed now)

- DERIVED: D1-D8 all pass and kappa = 1/2 exactly.
- CONDITIONAL: kappa = 1/2 exactly on one admissible option only, or D8 missing, or one unforced auxiliary premise.
- RESTATEMENT: the identity is algebraically equivalent, under `Framework`, to kappa = 1/2 (or to xi = 1, premise A,
  G rho = 4 a0^2/c^2, the 32 pi relation), OR every kappa satisfies it (fails D4).
- DERIVES OTHER: a determinate kappa != 1/2; reported in or out of the CFG493 window (Lean `Win` of KAPPA_LOGIC).
- NO IDENTITY: no solution for any kappa > 0, or kappa depends on a host mass / fitted constant (D6).
Lane label: DERIVED if any candidate is DERIVED; else CONDITIONAL if any is; else NO IDENTITY (with each candidate's
own label reported). An honest NO IDENTITY is a valid outcome.

## 3. Known-answer controls (must come out RESTATEMENT; if not, the apparatus is broken and the lane stops)

KA-1 (KF1 / KC1 reduction, rebuild_2026_10_22/KF1_argon_kappa_routes, 5abc2d1ae6): with l = c/sqrt(G rho_DE),
     a0 = c^2/(2 xi l) <=> kappa = 1/(2 xi). Posit xi = 1 => kappa = 1/2. Expected label RESTATEMENT (xi = 1 is the
     answer). sympy reproduces kappa = 1/(2 xi) exactly.
KA-2 (GF2 SIS ratio, AUDIT_GF2 a755b66ca): in the law's log potential Phi = v_f^2 ln r, isothermal hydrostatics with
     rho ~ r^-2 gives sigma^2 / v_f^2 = 1/2 for every kappa (sympy, with kappa = 1/2 and kappa = 1/3). Expected
     RESTATEMENT (fails D4: the 1/2 does not move with kappa).
KA-3 (p32_iff): Lambda pi (c^2/a0)^2 = 32 pi^2 <=> kappa^2 = 1/4. Expected RESTATEMENT.

## 4. Kinematic input taken from the record (not a premise; checked by sympy)

AC2q (closure_2026_11_06/EQUATIONS_IN_ORDER.md section 1): the dark-energy scalar phi is the clock; in unitary gauge
X = s^2 / (2 N^2), N the lapse; the khronon acceleration is A_i = c^2 d_i ln N. Hence, exactly,
    grad ln X = -2 A / c^2                                                                       (R)
i.e. the vacuum's kinetic density responds to khronon acceleration over the RESPONSE LENGTH L_v(A) = c^2 / (2|A|).
sympy must verify (R) from the two definitions. (R) contains no kappa; it supplies the factor 2 of KA-1, with KA-1's xi
= L_v(a0) / l (the map is checked by sympy, not assumed).
Static J-sector energy density, from (c^3/16 pi G) sqrt(-g)[-2 J(Y)] with J = Lambda - 2 a_geo^2 [u - ln(1+u)]:
|eps_J(u)| = (a0^2 / 4 pi G) [u - ln(1+u)] (sympy derives the prefactor from the action; if it differs, the derived
one is used and the difference reported).

## 5. Candidate identities (declared now; option spaces fixed now; equal weights)

V1. RESPONSE-LENGTH IDENTITY. "At the khronon's transition acceleration A = a0, the vacuum's response length (R),
    c^2/(2 a0), equals the vacuum's own gravitational length l_v." Adds premise `resp`: c^2/(2 a0) = l_v.
    Option space for l_v (every GR / Newtonian length built from rho_DE and c alone):
      (a) de Sitter radius c/H_Lambda; (b) relativistic Poisson length c/sqrt(4 pi G rho); (c) c t_ff,
      t_ff = sqrt(3 pi/(32 G rho)); (d) Jeans length c sqrt(pi/(G rho)) with c_s = c; (e) 1/sqrt(Lambda);
      (f) horizon circumference 2 pi c/H_Lambda.
    The pi-free length c/sqrt(G rho) is NOT an admissible option: it is xi = 1 (KA-1), i.e. the answer.
    Mutation: replace the factor 2 of (R) by 1 (a scalar with X ~ N^-1): kappa must change by x2.
V2. VACUUM-CANCELLATION IDENTITY. "The khronon's acceleration energy cancels the vacuum term exactly where the
    foliation's acceleration reaches the horizon scale": J(Y*) = 0 with sqrt(Y*) = A*/c^2. Adds premise `cancel`.
    Option space for A*: (a) c H_Lambda (static-patch scale); (b) c H_Lambda / (2 pi) (Milgrom's form);
    (c) 2 c H_Lambda (Unruh = Gibbons-Hawking temperature root, rules section 0).
    Mutation: A* -> 2 A* (a) must change the outcome.
V3. SWITCH-EQUIPARTITION IDENTITY. "At the switch u = 1 the khronon sector's static energy density equals the clock's
    kinetic energy at its bound": |eps_J(1)| = r rho_DE c^2. Option space r in {1/2, 1} (X vs s^2/2 at s^2 = 2 rho_DE).
    Flag in advance: this sits in the excluded S7 class (energy-density matching at g = a0); it is run because it is
    the v3s-native form, and S7 is reported with it.
    Mutation: evaluate at u = 2 instead of 1.
V4. BLEND-SWITCH IDENTITY. "The vacuum switches the stiffness where the law's phantom density at the transition
    radius (g_N = a0) of an isolated point mass equals the blend's own scale b = rho_DE." Adds premise `blend`.
    Mutation: evaluate at g_N = a0/4. D6 is checked first (expected M-dependence is disclosed below).

Hand expectations, disclosed before freezing (sketches done while choosing the candidates, not graded numbers):
V1 options reproduce record values (KC1: 1.447, 1.772, 0.921, plus 0.282, 2.507, 0.230); V2(a) is expected to have
no root (u - ln(1+u) <= u^2 bounds kappa^2 [u* - ln(1+u*)] below 4 pi); V3 expected O(5) kappa, out of window;
V4 expected M-dependent. If all hold, the lane label is NO IDENTITY; the scripts decide, not these sketches.

## 6. Cold component (secondary, fixed now)

For each candidate with a determinate physical response, compute the gravitating density the identity assigns to
the vacuum response in (i) a disc galaxy (Phi/c^2 ~ 1e-6, g ~ a0), (ii) an X-COP cluster (Phi/c^2 ~ 1e-5, r500
~ 1.3 Mpc), (iii) the recombination background, and compare with the needed cold fraction: <= 0.33 / 0.19 of
baryons in discs, 4.2 / 3.8 in clusters, 5.41 cosmic. "SAYS SOMETHING" only if the response reaches >= 0.1 of the
cluster need AND stays inside the disc limit AND reaches >= 0.1 of the cosmic need; otherwise "SAYS NOTHING", with
the ratio. A response that scales with the host potential is reported as host-tracking (ARGON assessment Q1(ii)).

## 7. Outputs and procedure

- vr1.py (sympy + float), vr1.json / vr1.out; MUTATE=1 -> vr1_MUTATE.json / .out (separate outputs).
- VR1_vacuum_response.lean + VR1_vacuum_response_MUTATE.lean (+ .out of each compile).
- RESULT.md with the label table. Small files only. Every commit message and RESULT ends with the line below.

kappa = 1/2 FITTED; not theory closed.
