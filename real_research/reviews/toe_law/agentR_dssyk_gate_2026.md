# Agent R — DSSYK vacuum-placement gate watch (literature sweep, 2026-06-10)

**Task.** The repo's derivation rung is GATED on the banked DSSYK verdict (2026-06-09, `dssyk_problem1_STRUCTURED_OUTPUT.json`,
`chord_vacuum_placement_test.py`, `steelman_both_ways.py`): **CONTESTED-TERMINAL** — the deep-MOND sign is a 1:1 readout of the
ASSUMED vacuum placement (Narovlansky–Verlinde center θ=π/2, E=0 → p=1/2, MOND; Okuyama edge θ→π, E=E0 → p=3/5, anti-MOND), the
chord algebra supplies BOTH a natural center state (N̂-vacuum / infinite-T) and natural edge states (H-extremal) and cannot pick,
and the placement is a holographic-dictionary choice, not a derivation. This sweep asks one question: **has anything published
since ~May 2026 moved that?** Hostility rule applied throughout: a paper that *assumes* a placement and then matches observables
*at* that placement does not settle it; only a derivation of θ_vac or a contrastive (both-placements) discriminator moves the gate.

**Method.** arXiv API date-sorted sweeps on "double-scaled SYK"/"DSSYK" (40 most recent) and "sine dilaton" (20 most recent);
author sweeps (Okuyama, Narovlansky, Verlinde-camp); Semantic Scholar forward-citation pulls on Okuyama 2505.08116 (all 5 citers)
and N–V 2310.16994 (2026 citers); targeted abstract/full-text interrogation of every candidate; SCGP workshop program check.
Cutoff of the sweep: arXiv postings through 2026-06-10 (no June-2026 DSSYK/dS-holography paper had appeared in hep-th yet).

---

## 1. The hits, classified

### Strict window (≥ May 2026)

| Paper | One-line claim | Placement question |
|---|---|---|
| **2605.03037** Goto–Milekhin–H.Verlinde–Xu, *Generalized Free Fields in de Sitter from 1D CFT* (May 4) | A pair of large-N 1D CFTs contains a generalized-free-field algebra on a timelike geodesic in dS_{d+1}; for dS3 the map extends into the bulk as a dS-adjusted HKLL prescription; "comment on the relevance ... to the de Sitter/DSSYK correspondence." | **IGNORES.** Deepens the center-camp toolkit (a bona-fide bulk-reconstruction map for the N–V-type setup) but never asks where the dS state sits in the spectrum, and computes no edge comparison. |
| **2605.13956** Aguilar-Gutierrez–Kukolj–Seitz, *q-Askey Deformations of DSSYK* (May 13) | Microscopic deformations → q-Askey-scheme transfer matrices; discrete-level transition in sine dilaton gravity; type II₁/I∞ algebras. | **IGNORES.** No statement on which limit gives dS. |
| **2605.13490** Banks, *What does it mean to have a quantum gravitational theory of de Sitter Space?* (May) | If dS is a finite-dimensional quantum system, "any theoretical model of it is ambiguous" (semiclassics + measurement theory); local detectors access a tiny fraction of the qubits. | **IGNORES** the specific center/edge question (no DSSYK engagement). Meta-level it *rhymes with* the banked verdict — a principled argument that finite-dim dS models are inherently ambiguous — but it is a philosophical position, not a calculation; do not bank it as support. |
| **2605.30423** Espíndola–Farag Ali, observer admissibility in Euclidean dS (May) | Form-domain criterion for which observer sectors couple to the dS saddle. | **IGNORES.** "Spectral" here = operator-domain admissibility, not the DSSYK spectrum. |
| **SCGP workshop**, *Double Scaled SYK: From Gravity to Many-Body Quantum Chaos*, May 11–15 2026 | Narovlansky ("Chaos in de Sitter and quantum mechanics"), H. Verlinde ("soft mode of DSSYK and 3D near-dS gravity"), Susskind, Zhao (HH state for dS observers) all presented. | **IGNORES (so far).** Both camps active in the same room; no adjudication artifact has emerged. This is the most likely incubator of the paper that eventually moves the gate. |

### Jan–Apr 2026 (after the banked file's citation horizon, before the strict window)

| Paper | One-line claim | Placement question |
|---|---|---|
| **2604.21014** Marini–Qi–H.Verlinde, *3D near-de Sitter gravity and the soft mode of DSSYK* (Apr 22) | The DSSYK soft mode (with time-dependent Maldacena–Qi coupling) is dual to 3D Einstein–dS with energy on a dS₂ slice; a Gibbons–Hawking-type entropy calculation with k=−1 boundary conditions reproduces the **full semiclassical DSSYK entropy curve** S(θ)=(2πθ−2θ²)/λ; dS3 boundary Green functions = (DSSYK 2-pt)². | **CONFIRMS-center-consistency, does not derive.** Full-text check: works across the whole spectrum (v∈[−1,1]), takes the N–V-side framework as input (follows Lensky–Qi soft-mode dynamics), and **never mentions Okuyama or the edge identification**. The entropy match is a whole-dictionary check, not a placement pick. By the hostility rule: assumed placement + matched observables ≠ settled. |
| **2602.06113** Aguilar-Gutierrez, *Deforming DSSYK & Reaching the Stretched Horizon* (Feb 5) | Sequences of T²(+Λ₁) deformations **in the upper tail of the spectrum** concretely realize Susskind's cosmological stretched-horizon proposal. | **IGNORES the vacuum question.** Touches the *edge*, but for the stretched horizon (the entropy carrier), not the dS vacuum, and the upper-tail target is engineered by the chosen deformation, not derived. Mild bridge note: it is at least compatible with "vacuum at center, horizon DOF toward the edge" — but that is our reading, not the paper's claim. |
| **2602.05939** Zhao, *"It from Bit": the HH state and QM for dS observers* (Feb 5) | One-state property of closed universes is compatible with finite-dim observer QM (baby-universe vs bulk Hilbert space distinction). | **IGNORES.** |
| **2602.16088** Okuyama (Feb 17) | Laguerre/matrix-model technicalia. | **IGNORES — and diagnostic: the edge camp's author has published nothing on the dS-edge claim since 2505.08116** (v4 revisions only). |
| **2601.09801**, **2601.17698** | chaos→integrability transition; sine-dilaton c-function (UV Liouville → IR JT). | **IGNORE.** |

### Late-2025 items the banked file did not cite (context, flagged for completeness)

| Paper | One-line claim | Placement question |
|---|---|---|
| **2506.02109** Narovlansky, *Towards a microscopic description of de Sitter dynamics* (Jun 2025) | An SYK-built quantum system for a heavy object + environment in dS: correlators match QFT in rigid dS **including UV behavior**, and OTOCs reproduce dS gravitational scattering's "highly non-trivial features," including a **Lyapunov exponent twice the chaos bound** and unusual OTOC coefficients. | **CONFIRMS-center-consistency, one-sided.** This is the strongest semiclassical-check-class result the center camp has (exactly the task's category 2), but no edge-placement version of the same observables is computed by anyone, so it discriminates nothing. The banked verdict should add it to the pro-center ledger as construction-level consistency, weight unchanged. |
| **2511.10907** Susskind (Nov 2025) | Corrects his own claim: DSSYK/JT-dS entropy sits at **Planck** (not string) distance from the horizon ('t Hooft-model confinement misconception fixed). | **IGNORES** — spatial location of entropy, not spectral location of the vacuum. Shows the Susskind line is still self-correcting on basics. |
| **2511.01978** Cao–Gao, *Single-Sided Black Holes in DSSYK and No Man's Island* (Nov 2025) | Boundary algebra of a single-sided BH in DSSYK has a nontrivial commutant (type II₁); **full bulk reconstruction from the boundary is impossible**. | **IGNORES the dS dictionary** — the non-uniqueness is in the AdS/black-hole sector. This is the closest thing found to the task's category 3 (a not-1:1 result), and it does NOT touch the center/edge readout. The repo's "1:1 within the assumed dictionary" claim stands. |
| **2511.08743** van der Heijden–E.Verlinde–Xu; **2512.10101** Schouten–Isachenkov (Nov–Dec 2025) | U_q(su(1,1)) quantum-group structure of the chord algebra; vN-algebraic quantum group SU_q(1,1)⋊Z₂ with the non-negative-chord restriction built in. | **IGNORE placement; indirectly consistent with the banked closure** — the algebra's symmetry structure is now formalized to vN-algebra standard and still contains no "static patch = center" (or "= edge") clause. Do not over-claim: neither paper poses the question. |
| **2510.13986** Heller–Ori–Papalini–Schuhmann–Wang (Oct 2025) | dS holographic complexity from Krylov complexity in the **high-energy limit** of DSSYK (sine-dilaton frame). | **Edge-adjacent, third-camp.** The sine-dilaton line keeps associating dS-like geometry with the high-energy/"fake" region of an AdS-like bulk (also 2509.18462 Blommaert–Tietto–Verlinde: DSSYK G,Σ theory = complex Liouville string). This **entrenches** the contest rather than resolving it — see §2's reframing risk. |
| **2512.21366** Arundine, charged DSSYK + quasinormal modes (Dec 2025) | QNMs of charged DSSYK variants. | **IGNORES** — QNM machinery in the BH sector, no dS-placement contrast. |

**Forward-citation check on the edge paper:** Okuyama 2505.08116 has **five** citers total; the only 2026 citer is 2602.06113
(above). **No published paper anywhere engages the center-vs-edge discrepancy itself** — the only text on record stating the
conflict remains Okuyama's own "different from the proposal in Susskind et al." footnote-level remark, exactly as banked.

---

## 2. Hostile synthesis

1. **Nobody has derived θ_vac.** Every 2026 paper that uses a placement inherits it (Verlinde camp: N–V soft-mode/center
   framework; Aguilar-Gutierrez: deformation-engineered upper tail; sine-dilaton camp: dS as a high-energy/fake region).
   Zero papers compute an observable at BOTH placements and let the data pick. The banked "the chord algebra cannot fix it"
   result has not been contradicted — if anything the quantum-group formalizations (2511.08743, 2512.10101) make the
   placement-neutrality of the algebra cleaner.
2. **The evidence is accumulating asymmetrically, and honesty requires saying so in both directions.** The center camp added
   three construction-level consistency checks in twelve months (full entropy-curve match + dS3 Green functions 2604.21014;
   dS HKLL bulk map 2605.03037; rigid-dS correlators + doubled-Lyapunov OTOCs 2506.02109), is institutionally active (SCGP
   May 2026), and publishes at ~1 paper/2 months. The edge camp is **dormant**: Okuyama has not followed up, the identification
   has 5 citations and no defender computing new observables. BUT: one-sided consistency at an assumed placement is exactly
   what the banked verdict already priced in ("both camps have construction-level arguments"); volume of self-consistent
   output is sociology, not derivation. No center-camp paper has shown the edge placement *fails* anything.
3. **A reframing risk is growing (flag, not verdict).** The center identification produces **dS₃** physics (N–V, 2604.21014);
   Okuyama's edge produces **dS₂-JT**; the sine-dilaton camp gets dS-like behavior as the **high-energy/fake region of one
   AdS-like bulk** (2509.18462, 2510.13986). These may be three different duals/regions rather than two answers to one
   question — in which case "which placement is THE dS vacuum" is ill-posed, and the repo's gate question should eventually be
   restated as: *which spectral placement maps to the 4D cosmological-horizon physics that sets a₀*. No published paper poses
   that question; it is not answerable by this sweep.

---

## 3. VERDICT: **GATE-UNMOVED**

The banked CONTESTED-TERMINAL stands, unweakened and unstrengthened in its essentials. Nothing published since May 2026 (or,
checked more broadly, since the banked date's citation horizon) derives the vacuum placement, computes a contrastive
center-vs-edge observable, or establishes the dictionary is not 1:1 in the sign-relevant sector. Ledger-level updates only:

- **Add to the pro-center consistency column (weight: conditional, as before):** 2506.02109 (OTOC/Lyapunov match),
  2604.21014 (entropy curve + Green functions), 2605.03037 (dS-HKLL map).
- **Add a dormancy note to the pro-edge column:** no Okuyama follow-up through 2026-06; 5 citations, none adjudicating.
- **Record the reframing risk** (§2.3) as a watch item, not a verdict change.

### What would most plausibly move the gate next (watch list, ~6–18 months)

1. **A contrastive observable calculation** — most likely from someone fluent in both formalisms (Aguilar-Gutierrez;
   Blommaert–Mertens–Papalini; a Narovlansky/Verlinde student): compute the dS QNM ladder / late-time two-point decay or the
   2506.02109 OTOC features **at the edge placement** and show they fail (collapses the contest toward center) or succeed
   (deepens the 1:1 terminality). The center side already passes by construction; the missing half is the edge run.
2. **A sine-dilaton bulk derivation of where dS observables live in the spectrum** — the bulk geometry itself (one geometry,
   fake-region structure) could *derive* which spectral region carries Gibbons–Hawking physics rather than assuming it; the
   2509.18462 complex-Liouville line is the live candidate.
3. **Any Okuyama response** engaging N–V directly (none yet), or **SCGP-workshop follow-up papers** (2H 2026) — both camps'
   principals presented in the same week in May 2026; a direct confrontation paper is overdue.

### The specific calculation the repo should prepare NOW (so the gate-opening is pre-registered, not post-hoc)

Extend the existing machinery (`door2_dssyk_perprobe_both_maps.py`, `dssyk_wE_center_vs_edge_INDEPENDENT.py`) to the **late-time
decay rate of the matter two-point function at each placement** and compare against the dS QNM ladder Δ·H (the observable N–V
already match at the center): (i) center run = sanity check against N–V's published Green-function match; (ii) edge run = the
calculation nobody has published — can the sqrt-soft-edge spectral weight (s_E=1/2, banked) produce an exponential QNM-ladder
decay at all, or does it force a distinct (power-law-modified / Airy-type) falloff? If the edge *provably cannot* mimic the QNM
ladder, the repo will have pre-registered the first independent discriminator before the field publishes one; if it can, the
1:1/undecidable verdict deepens with a new observable. Either output is bankable. Caveat to carry: apples-to-apples requires
matching the bulk dimensionality per camp (dS₃ Green functions for center vs dS₂-JT for edge) — state this limitation in the
pre-registration rather than papering over it.

---

*Sweep artifacts: arXiv API date-sorted listings (DSSYK ∪ double-scaled SYK, 40 latest, through 2605.13956; sine dilaton, 20
latest, through 2605.13956/2601.17698); Semantic Scholar forward citations of 2505.08116 (5 total) and 2310.16994 (2026 citers:
2605.13490, 2605.05291, 2604.25035, 2604.21014, 2604.10267, 2601.09801 — each checked, none adjudicates); Okuyama author sweep
(latest dS-relevant: 2505.08116v4); SCGP program (May 11–15 2026). No June-2026 DSSYK/dS posting existed as of 2026-06-10.
Hostility rule applied: every "CONFIRMS" above is consistency-at-an-assumed-placement, none is a derivation.*
