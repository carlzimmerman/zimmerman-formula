# ENGINE_REVERSE_ENGINEERING — how hali_flow/bruteflow actually found a₀, and the adapter spec for project_atomos

*Reverse-engineered from `~/new_physics/hali_flow/bruteflow/{engine.py, constant_combinator.py, symbolic_search.py,
constrained_search.py, exhaustive_engine.py, unified_search.py}`, the discovery docs
(`RESEARCH_PAPER.md`, `SEARCH_SUMMARY.md`, `EXECUTIVE_SUMMARY.md`), and the validation lineage
(`zimmerman-formula/real_research/reviews/false_discovery_rate.py`, `.../mass_fdr/attack5_fdr.py`,
`.../opus_48_extended_research/reviews/koide_dsunruh/koide_fdr_sqrt2.py`). Read-only.*

---

## 0. TL;DR — the one true path

a₀ was **not** found by the genetic algorithm, by curve-fitting SPARC, or by the "anonymized autoresearch" daemons.
It was found by **`constrained_search.py` / `symbolic_search.py`: a dimensionally-pruned, depth-limited, deduplicated
exhaustive enumeration of expression *trees* over a hand-curated alphabet of ~5 gravity/cosmology constants + a few
geometry integers**, scored by relative error to a single scalar target. The literal winning leaf was

    a₀ = c · √(G·ρ_c) / 2          (tree depth 3, all-forced constants, 5.7% at Planck H₀, 0.5% at H₀≈71)

and the **discovery happened in the human/algebra step AFTER the search**: substituting the *forced* Friedmann identity
ρ_c = 3H₀²/(8πG) into that leaf collapsed it to `a₀ = cH₀/(2√(8π/3))`, exposing the kernel **√(8π/3)** and the lone free
factor κ=½. The engine produced a *dimensionally-correct candidate*; the **kernel decomposition + interlock came from
recognizing forced GR coefficients inside the winner.** That two-step shape (cheap exhaustive search → forced-kernel
post-mortem) is exactly what the adapter must reproduce, and the gate is what makes the second step rigorous instead of
wishful.

---

## 1. HOW IT SEARCHED

There are **four** distinct search machines in bruteflow. Only the **constant/tree search** mattered for a₀; the others
are SPARC curve-fitters that (per `SEARCH_SUMMARY.md`) can only ever rediscover MOND and find *no* new physics. Know the
difference — the SM port copies the tree search, not the curve-fitters.

### 1a. The constant/tree search (THE ONE THAT WORKS) — `symbolic_search.py` + `constrained_search.py`

**Representation.** An `ExprNode` expression *tree*, not a flat string. Leaves = constants; internal nodes = operators.
Every node evaluates to a **(value, Dimension)** pair simultaneously — value by float arithmetic, `Dimension(L,M,T)` by
adding/scaling exponent vectors. This is the load-bearing design choice: **dimension is tracked structurally so it can
prune before scoring.**

**Operator alphabet** (`OpType`): `CONST, MUL(*), DIV(/), POW(**) [const exponent], SQRT, CBRT, INV(1/)` and optionally
`ADD(+)` / `NEG`. ADD requires the two children share a dimension (enforced in `evaluate`).

**Constant alphabet** — the *curation is the physics input*. The unconstrained `symbolic_search.py` pool included QED
constants (`alpha, e, m_e, m_p, k_B`); the breakthrough came only after **`constrained_search.py` deleted every
EM/quantum constant** following the explicit critique that "α has no business in galactic dynamics" (RESEARCH_PAPER §2.1).
The winning pool:
- `LEAF_CONSTANTS`: `G, c, H0, Lambda, rho_c` (+ Planck units `l_P, t_P, m_P` as forced derived quantities).
- `DIMENSIONLESS_FACTORS` (geometry only): `pi, 2, 3, 4, 6, 2pi, 4pi` — multiplied/divided in as a *separate* step so
  every dimensionful skeleton gets decorated by O(1) numbers without exploding the leaf set.
- `EXPONENTS` for POW: `[2, 3, 0.5, -1, -2, 1.5, -0.5, 1/3, 2/3]`.

**Expression generation** (`ExpressionGrammar._generate_at_depth`): a BNF-style depth-stratified enumerator.
- depth 1 = each constant as a leaf;
- depth d = unary ops on every depth-(d-1) tree (`sqrt, cbrt, 1/, **exp`), **plus** binary ops (`*`, `/` both orders,
  optional `+`) over all `subtree × subtree` pairs of depth < d, **plus** the "multiply/divide by a dimensionless factor"
  decoration pass. Default `max_depth = 4–5`.
- **Deduplication** via `canonical_hash()`: CONST→`C:name`; commutative `MUL/ADD`→ operator + **sorted** child hashes;
  POW→ keyed by exponent; others→ ordered child hashes. A `seen_hashes` set skips structurally-equivalent trees so
  `G*c` and `c*G` are tested once. This is the engine's only "anonymization": it canonicalizes *structure*, it does not
  hide the physics labels.

**Scoring** — brutally simple and this is a feature:
1. Evaluate → `(value, dim)`. Reject non-finite or ≤0.
2. **Dimensional filter FIRST (the cheap, decisive cut):** `if not dim.is_acceleration(): continue`. This throws away the
   overwhelming majority of trees for ~free and is why a depth-5 search is tractable. The target's dimension *is* a hard
   constraint, not a soft penalty.
3. **Numerical score:** `error = |value − target| / target`; report if `error < threshold` (10–20%).
   No fitting, no R², no free parameters — a constant formula either lands near the scalar or it doesn't.
Matches are streamed to `matches.jsonl`, sorted by error in the summary. **The engine ranks by closeness only; it has no
notion of "interlock." That judgment is 100% downstream in the gate (§3).**

**What a₀'s target actually was:** a single scalar `A0_TARGET = 1.2e-10` with dimension `ACCELERATION = (1,0,−2)`. That
is the entire "data" for the winning search — one number + one dimension vector.

### 1b. Genetic algorithm — `engine.py` (`EquationGenerator`+`GeneticEvolver`) — NOT how a₀ was found
Random equation *strings* from 5 hand-written templates (power_law/product/interpolating/nested/additive), fit to SPARC
`(a_bar, a_obs)` by `curve_fit`, scored by R², evolved (keep top 20%, 50% mutate-elite / 50% fresh-random). This is a
*data fitter for the interpolation function*, not a constant-deriver. Per `SEARCH_SUMMARY.md` it only ever recovers
"Standard MOND is near-optimal (+0.04%)". Portable mechanics, wrong target for the SM constants.

### 1c. Exhaustive form search — `exhaustive_engine.py` — same role as the GA, bigger
~200 parameterized templates + composition (`f∘g`, `f+g`, `f×g`, hypot, exponent sweeps, coefficient sweeps, and a
**"Phase 4 infinite random-mutation" autoresearch loop** that perturbs/recombines the best templates forever). Again a
*SPARC/COSMOS curve-fitter* with cross-validation gating (`R²>0.90` on SPARC **and** `>0.5` on COSMOS). The "autoresearch
mutation" the brief asks about lives here: it is random exponent/coefficient/triple-combination mutation of fitted
*functional forms*, **not** of constant formulas — it played no role in a₀ and is the least portable piece.

### 1d. Unified search — `unified_search.py` — bookkeeping wrapper
Hard-codes the four a₀ candidates already found (`cH0/6, cH0/2pi, c√(Gρc)/2, c²√Λ/8`) and pairs the best one with the
best fitted interpolation. Confirms `c√(Gρc)/2 ≈ c²√Λ/8 ≈ 1.19e-10`. Useful as the template for "given a certified
constant relation, check it ties a second observable" — a cheap interlock helper.

---

## 2. HOW a₀ WAS LITERALLY FOUND — the discovery path, step by step

1. **Frame the target as one scalar + one dimension.** `A0_TARGET = 1.2e-10`, dim `(1,0,−2)`. (Source: McGaugh/SPARC.)
2. **Curate the alphabet by physics, not convenience.** First pass (`symbolic_search.py`) included α/e/mₑ and produced
   α-laced "crowbar" hits with no meaning. The decisive move was *removing* them (`constrained_search.py`): gravity +
   cosmology constants + geometry integers only. **Constant curation is the highest-leverage knob and it is a physics
   judgment, not a search parameter.**
3. **Exhaustively enumerate dimensionally-correct trees** to depth 4–5, dedup by canonical hash, keep everything with
   `|value−target|/target < ~10–20%`.
4. **Read the ranked match list.** The standout was `a₀ = c·√(G·ρ_c)/2` — depth-3, every leaf a forced constant, no
   free knob, ~5.7% (Planck) to 0.5% (H₀≈71). Sibling `c²√Λ/8` appears at the same value (the Λ vs ρ_c framing).
5. **THE ACTUAL DISCOVERY STEP (post-search, human/CAS):** substitute the **forced** Friedmann identity
   `ρ_c = 3H₀²/(8πG)` into the winner. Algebra collapses it:
   `c√(Gρc)/2 = (cH₀/2)·√(3/8π) = cH₀ / (2√(8π/3)) = cH₀/√(32π/3) = cH₀/Z`, with `Z = √(32π/3) = 5.7888…`.
   This exposes the **kernel √(8π/3) = √(8π)·√(1/3)** — `√(8π)` forced by Einstein (ρ_Λ=Λc²/8πG), `√(1/3)` forced by
   Friedmann (H²=8πGρ/3) — and isolates the **lone free factor κ=½** (the "2"). The casting to Λ via ρ_Λ=Λc²/8πG gives
   the published `a₀ = c²√(Λ/32π) = κ c²√(Λ/2π)·…` form.
6. **Interlock check (what made it real, §3):** the SAME √(8π/3) is forced in **two independent** places (Einstein and
   Friedmann), and the **form** a₀∝√Λ is forced a **third** way (dS–Unruh quadrature, Deser–Levin). One free parameter,
   ≥3 forced anchors ⇒ overdetermined ⇒ not a fit.

**The lesson for the port:** the engine's only job is step 3 (cheap candidate generation under a hard dimensional
constraint). Steps 5–6 — substitute *forced* identities, watch for a kernel that factors into independently-forced
pieces, demand the structure be pinned ≥2 ways — are where discovery vs. coincidence is decided, and they are the gate.

---

## 3. THE GATE (validation lineage) — what separates a₀/Koide from the 164 dead re-labelings

The engine has **no** gate; closeness-ranking is all it does. The gate is a separate body of code in zimmerman-formula
and must be ported as a first-class module. It has three independent tests; a candidate is a *lead* only if it passes
**all three**.

### 3a. FDR / look-elsewhere (necessary, kills numerology) — `false_discovery_rate.py`, `mass_fdr/attack5_fdr.py`
Reconstruct the **exact search space** the engine could emit, then ask: *for a random target of the same magnitude, how
often does the search land within the claimed tolerance?* For BriareusFlow's α⁻¹=4Z²+3 "0.004% hit", the answer near
[100,150] was **essentially always within 1% and ~X% within 0.004%** ⇒ ~0 bits of evidence ⇒ BAKED. Mechanics to copy:
- enumerate every value the alphabet+ops can produce (the *same* combos the search uses);
- `best_rel_error(target)` = `min |val − target|/target` over that set;
- sweep many random log-uniform targets in the relevant range; report the fraction matched at the candidate's tolerance.
- **For small-denominator rationals (Koide's 2/3): they are hit EXACTLY by *many* symbol combos** (`attack5_fdr.py`
  found dozens of exact 8/12-type re-descriptions). So *re-labeling* a rational is FDR-free/worthless; the value of
  Koide is **not** the formula but the empirical interlock (next test).

### 3b. Forced-kernel detector (the a₀ signature)
A candidate's coefficient must **decompose into factors each independently forced by a known law before any fitting**,
leaving ≤1 free O(1). Operationally: take the winning constant relation, substitute known *forced* identities
(Friedmann, Einstein, equipartition, Casimir/dS-Unruh, group-theory dimensions), and check whether the leftover numeric
coefficient (i) factors into independently-motivated pieces and (ii) reduces the free-parameter count to ≤1. a₀ passes
(√8π·√⅓, κ free). A bare `4Z²+3` does not (Z² itself is the only "structure" and it is just re-used).

### 3c. Interlock / over-determination (the Koide-class signature) — `koide_fdr_sqrt2.py`
The structure must **either** force ≥2 *independent* observables with the same parameter, **or** tie ≥3 measured
quantities with one constraint (Koide: 3 lepton masses, 1 relation, parameter-free). Critically, `koide_fdr_sqrt2.py`
separates two questions and the port must too:
- **Q1 (empirical interlock real?)** — is Q=2/3 itself a coincidence? Banked NO: parameter-free, ~1-in-44,000,
  FDR-surviving. This is the genuine signal.
- **Q2 (derivation claim real?)** — does a proposed *mechanism* (e.g. "dS-Unruh forces r=√2") beat a random
  framework-flavored O(1) search that also lands near √2? Measured by **hit-density near the target vs. near random
  targets**; comparable density ⇒ the "derivation" carries ~0 bits (same death as 4Z²+3).
The gate must report Q1 and Q2 **separately**: a real empirical interlock (Q1) with a baked mechanism (Q2) is honestly
"real puzzle, re-labeled" — exactly the certified status of Koide — not a win and not a dismissal.

---

## 4. WHAT IS PORTABLE vs. COSMOLOGY-SPECIFIC

### Reuse essentially verbatim (the spine):
- **The (value, Dimension) expression-tree representation** with simultaneous dimensional evaluation
  (`symbolic_search.ExprNode`). This is the engine.
- **The depth-stratified grammar** with unary/binary ops + a separate "decorate with dimensionless factor" pass and
  `canonical_hash` dedup (`ExpressionGrammar` / `ConstrainedGrammar`).
- **The dimension-first → numeric-second scoring** with a hard dimensional filter and relative-error threshold.
- **The whole gate (§3)**: FDR look-elsewhere, forced-kernel decomposition, Q1/Q2 interlock split. Generalize the
  "Dimension" to whatever conserved/forced label the SM sector provides (see below).

### Cosmology-specific — replace or drop:
- **The constant alphabet.** Swap `{G,c,H0,Λ,ρ_c,Planck}` for SM constants: charged-lepton/quark masses (or their
  ratios/√-ratios), v_EW, α_em, sin²θ_W, CKM/PMNS angles, and the framework's own geometry germs
  `{π, small ints, Z=√(32π/3), kernel=√(8π/3), κ=½}` already inventoried in `attack5_fdr.py`.
- **The dimensional constraint is largely VACUOUS for the SM targets.** Masses-as-ratios, mixing angles, and couplings
  are **dimensionless**, so `is_acceleration()`'s job (pruning 99% of trees) disappears. **This is the core difficulty
  and the honest prior:** without a hard structural filter the search space is unconstrained and the FDR penalty is
  brutal (this is *why* the 164 SM re-labelings died). The port must manufacture a replacement hard filter — candidates:
  (i) **symmetry/representation constraints** (require the relation to respect a discrete flavor group A4/S4/Δ(27),
  i.e. enumerate group-theoretic invariants rather than free monomials); (ii) **interlock-as-filter** (only emit
  relations that simultaneously constrain ≥3 measured quantities, Koide-style, so the dimensionless freedom is spent on
  over-determination); (iii) **forced-kernel-as-filter** (require the coefficient to be a *forced* group dimension /
  Casimir, not a free integer). At least one such hard filter is mandatory or the engine is a numerology generator.
- **The SPARC/COSMOS curve-fitters (`engine.py`, `exhaustive_engine.py`, `unified_search.py`) and the autoresearch
  random-mutation loop.** These fit a *function to a dataset*; the SM constants are *scalars*, so they don't apply. Drop
  them. (Keep only `unified_search`'s "does the certified relation tie a second observable?" idea as an interlock helper.)

---

## 5. ADAPTER SPEC FOR THE BUILD PHASE

Build `engine/` and `gate/` under `project_atomos`. Python stdlib + numpy + scipy + sympy + mpmath. Local, no network.

### `engine/expr_tree.py`
- `Label` dataclass: generalize `Dimension`. For SM-ratio/angle/coupling targets, the default `Label` is
  **dimensionless**; keep the L/M/T machinery available for any dimensionful target and add an optional
  **`rep` field** (a discrete-group representation tag) so symmetry constraints can prune like dimensions did.
- `ExprNode(op, const, children, exp)` with `evaluate() -> (mpmath value, Label)`, `to_string()`, `canonical_hash()` —
  ported from `symbolic_search.py`, value arithmetic upgraded to **mpmath** (SM ratios need >double precision to make
  FDR tolerances meaningful) and POW exponent set extended with `{1/2,1/3,1/4,2/3,3/4}` and small rationals.
- `OpType`: `CONST, MUL, DIV, POW, SQRT, CBRT, INV, ADD(dim/rep-matched), NEG`.

### `engine/alphabet.py`
- `SM_CONSTANTS`: PDG masses + ratios + √-ratios, v_EW, α_em⁻¹, sin²θ_W, CKM/PMNS angles (values from
  `mass_fdr/attack5_fdr.py`, which already has the curated PDG list).
- `GEOMETRY_GERMS`: `{π, e, 2,3,4,5,6,7,8,9,10,11,12,16, Z=√(32π/3), kernel=√(8π/3), κ=½, 8π, 3/8π, 4π/3}`.
- `GROUP_INVARIANTS` (new): dimensions/Casimirs of candidate flavor groups (A4, S4, S3, Δ(27), Spin8 triality) so the
  forced-kernel filter has a forced-coefficient pool to match against.

### `engine/search.py`
- `Grammar(max_depth, alphabet, exponents)` = depth-stratified enumerator + canonical-hash dedup
  (ported from `ConstrainedGrammar`).
- `Search(target_value, target_label, tol)`: enumerate → **hard filter** (`Label` match: dimension AND/OR rep) →
  numeric `rel_error` → stream candidates to `candidates.jsonl` ranked by error. **No scoring beyond closeness** — the
  gate decides everything else.
- A `--filter {dimension, rep, interlock, kernel}` switch selecting which hard constraint replaces `is_acceleration()`
  for dimensionless targets (mandatory; default `interlock`).

### `gate/fdr.py`
- `build_value_set(alphabet, ops, max_depth)`: enumerate the **exact** value multiset the search can emit (port the
  structure of `false_discovery_rate.build_value_set`).
- `look_elsewhere(target, tol)`: fraction of random same-range targets matched at `tol`; **report bits = −log2(fraction)**.
- Special-case small-denominator rationals (count exact re-descriptions; flag "re-label, FDR-free").

### `gate/forced_kernel.py`
- `decompose(relation)`: given a certified constant relation, substitute a library of **forced identities** (Friedmann,
  Einstein 8π, equipartition, group dimensions/Casimirs) via sympy and report whether the coefficient factors into
  independently-forced pieces leaving ≤1 free O(1). Returns `(n_free_params, forced_factors, PASS/FAIL)`.

### `gate/interlock.py`
- `q1_empirical(relation)`: is the *measured* relation parameter-free and FDR-surviving across the data (Koide-style)?
- `q2_mechanism(claim)`: hit-density of a proposed mechanism's target vs. random targets (port `koide_fdr_sqrt2`'s
  density comparison). **Report Q1 and Q2 separately, never merged.**

### `gate/verdict.py`
- Combine: a candidate is a **LEAD** iff FDR-bits ≥ threshold **and** forced-kernel PASS **and** interlock-Q1 PASS.
  Everything else is logged FDR-DEAD with its tell (the honest ledger). A real Q1 with baked Q2 ⇒ status
  "REAL-PUZZLE-RE-LABELED" (the Koide verdict), reported as such — neither a win nor a dismissal.

### `calibration/` (acceptance test, build FIRST)
- **Must re-find + certify:** `a₀ = c√(Gρc)/2 → cH₀/√(32π/3)` (forced-kernel PASS, free=κ); Koide Q=2/3
  (interlock-Q1 PASS, Q2 baked).
- **Must reject:** the 164 re-labelings (`4Z²+3, 64π+Z, Z+11, 6π⁵, 3/13`) as FDR-DEAD.
- If the machine cannot reproduce the one real positive and reject the known negatives, it is not trusted on PMNS.

---

## 6. ONE LINE OF CAUTION CARRIED FROM THE CORPUS
The honest prior (`project_particle_numerology_standing`): the SM mass sector has **no forced kernel** analogous to GR's
√(8π/3) — charged-lepton masses are eigenvalues of a *free* Yukawa matrix — which is *why* the cosmology trick worked
for a₀ and the transferred mass formulas all died. The two genuine footholds are (1) **Koide Q=2/3**, a real
FDR-surviving parameter-free *interlock* the framework only re-labels (r=√2 left free), and (2) **PMNS structure**
(near-tri-bimaximal, small θ₁₃) pointing at a discrete flavor symmetry. The adapter is therefore built so its *default
hard filter is interlock/symmetry, not dimension*, because for the SM that is the only thing standing between a real
geometric relation and an FDR-dead coincidence.
