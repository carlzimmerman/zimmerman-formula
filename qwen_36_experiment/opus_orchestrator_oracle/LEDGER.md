# LEDGER — append-only record of every door attempted

Read the last ~40 lines before starting a cycle. Never redo a door marked `CLOSED` or `CONFIRMED`.
Format is specified in `07_WRITING_RULES.md`. Newest entries at the bottom.

---

## SEEDED — what is already settled, do NOT redo

These come from committed, script-backed work in `real_research/reviews/`. Each has a script; re-run it if you
doubt it, but do not re-derive it from scratch.

| already done | verdict | script |
|---|---|---|
| a₀ from dark energy | a₀ = ½c√(Gρ_Λ) = 9.3614e-11 canonical; **the ½ is FITTED** | `mi_2Z_is_the_friedmann_root_2026.py` |
| ν(y) = √(1+1/y) reproduces Milgrom 1999 | yes, identically — it **is** his eqs 6–9 | corpus-wide |
| the crossover of any temperature functional | q_cross = 2/r, r free — class does NOT close | `mi_crossover_master_formula_2026.py` |
| combining Gρ_Λ with c²Λ to fix the coefficient | impossible — relabelling theorem | `mi_zeropoint_interference_audit_2026.py` |
| ρ_local instead of ρ_Λ | dead: 1076× too large in the solar neighbourhood | `mi_local_floor_target_2026.py` |
| standard local rates giving ¼ | none; closest 12.84% off | `mi_local_floor_target_2026.py` |
| Deser–Levin temperature from a computed response | reproduced to 1e-15…1e-17 at zero rotation | `mi_circular_dS_response_2026.py` |
| how much orbital motion breaks KMS | O((v/c)²) — **8.6e-07 at galactic speeds** | `mi_circular_dS_response_2026.py` |
| the auxiliary-field localization + exact circular orbit | localization exact; suppression verdict hinges entirely on ω_c | `mi_auxfield_exact_circular_2026.py` |
| is ω_c fixed? | **no — free fifth constant**, committed window 1.78–2.21e-14 | `mi_kernel_axis_separation_omegac_2026.py` |
| equilibrium dS linear response → MOND | no: KMS ⇒ ρ(ω) ≥ 0 ⇒ δm > 0, anti-MOND | `linear_response_anti_mond_proof.md` |

## WITHDRAWN — never re-assert (see `04_FRAMEWORK_FACTS.md` for the full list)

- "the dS–Unruh mechanism cannot yield a smaller coefficient" — it can, q_cross = 2/r
- "the two MOND limits jointly force q_cross = 2" — five scale-free examples, not a theorem
- "a quadrature torque obstructs circular orbits for any kernel" — kernel-shape dependent
- "S(Ω)=0 on an interval ⇒ K ∝ δ" — refuted by K = b·J₀(bs)
- "1/C inside 3.8e5–3.8e7 cross-validates two routes" — same (c/v)² twice
- "2Z carries a √π no normalisation supplies" — its √π **is** the Friedmann 8π/3's

## DO NOT REPEAT (from the qwen RESEARCH_LOG, still valid)

- do not retry the tn07–tn09 embedding-space Z² computation (branch-cut bugs; tn10 supersedes)
- do not re-verify ν(y) = √(1+1/y) against Milgrom 1999 — done at multiple y
- do not re-derive a₀ from the dark energy density — done
- do not use h_spectral(x) from ρ via a Stieltjes integral as if it equalled K(x) — it does not (tn12)

---

# ENTRIES

<!-- append below this line, newest last -->

## 2026-08-07 — overnight sweep, ~500 checks, all re-run before commit   STATUS: see 04_FRAMEWORK_FACTS.md
Nine theorems added, four claims withdrawn (including two of mine). Full table in FRAMEWORK_FACTS §2026-08-07.
DO NOT REDO: admissibility bounds on r (sup = +∞, four routes); the CTP Gaussian order (a₀ = 0 exactly); the
cubic tadpole (structure yes, coefficient r < 1 and magnitude 1.27e-42 — both dead); composite operators,
squeezed states, two-level/N-level inversion, super-ohmic equilibrium, linear-dressing KMS, the Ward identity,
the geometric lock (priced p = 0.480), the disformal completion (photon decay).
NEXT: the TASKS/ queue. M-tasks are the uncovered open items; W-tasks are unrelated.

## 2026-08-07b — a_0(z) is r-BLIND, and THE PRESENTATION THEOREM   STATUS: 25/25 + 40/40
`real_research/reviews/mi_a0z_r_blindness_2026.py` (25/25) — the redshift law a_0(z)/a_0(0) is
EXACTLY independent of r (symbolic, and for an ARBITRARY rho(z)); the framework/Milgrom separation
is the CONSTANT 2Z at every z, so redshift is NOT a coefficient lever. What redshift DOES separate
is WHICH HORIZON the GHY term sees (apparent -> rises as E(z), 1.84x by z=1, opposite sign to the
framework's decline; asymptotic dS -> z-degenerate, attack fails). New armed test: the residual
after dividing out the pure-Lambda law measures r(z)/r(0), forcing the two-scale escape scale to be
Lambda-pure to p <= 0.072 in matter-density power. Hostage to w != -1 on every branch.

`real_research/reviews/mi_local_presentation_grading_2026.py` (40/40) — **THE PRESENTATION
THEOREM.** In the LOCAL presentation (a_0 = lambda c sqrt(G rho_L)) the framework's lambda = 1/2 is
RATIONAL and all three Milgrom coefficients are transcendental (alg x pi^(+-1/2)); in the HORIZON
presentation (a_0 = q cH_L) the parities SWAP exactly. Since sqrt(pi) is transcendental, an
algebraic-output derivation can reach ONLY the pi-even member of its own presentation ==> **no
horizon/area/boundary argument can EVER output the framework's coefficient, and no local/matter-side
argument can ever output Milgrom's.** This RETRODICTS the corpus's 18-route null: every route that
produced a definite coefficient went through the horizon and produced Milgrom's. MI's own premise
(inertia = response to the vacuum's stress-energy, not to curvature) selects the LOCAL side, so the
open problem collapses from "derive the transcendental 2Z" to "derive the rational 1/4":
**floor k = (1/4) c sqrt(G rho_L) = c/(4 t_Lambda), a_0 = c/(2 t_Lambda), a_0 t_Lambda = c/2 EXACTLY**
(t_Lambda = (G rho_L)^(-1/2) = 50.74 Gyr; footing-invariant). Also: Z = sqrt(32 pi/3) = 4 sqrt(2pi/3),
Z^2 = 4 x (8pi/3) exactly, and the framework's form is Friedmann-factor-free while Milgrom's local
lambda moves >2x over d = 2..9. DO NOT OVERSTATE: pi-evenness admits EVERY rational (control NC2
fires on 1/3, 1, 2/5, 7/8) so **kappa = 1/2 is still FITTED**; the parity swap makes this a
statement about which side is PRIMITIVE, i.e. a postulate; the "1/4 is Bekenstein-Hawking's 1/4"
identification is a NAMED CONJECTURE priced at a post-hoc p = 0.028 over a 36-rational menu.
NEW FALSIFIABLE CONSEQUENCE if it holds: a_0 must shift with any change in the horizon-entropy
NORMALISATION (Wald/Gauss-Bonnet) at fixed rho_Lambda — the first coefficient test in the corpus
that does not run through a horizon area.
SM HINT (flagged, not claimed): the corpus's number-field obstruction was computed in the HORIZON
presentation; in the LOCAL one a_0 is rational, so that obstruction is PRESENTATION-DEPENDENT and
does not apply on the side MI's own premise selects. Next door = re-run it on c sqrt(G rho_L).
