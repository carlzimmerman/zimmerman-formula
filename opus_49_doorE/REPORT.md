# DOOR E — EXPLICIT X_d HUNT: the hunt for numeric c1, c2 in Yarotsky's cluster-expansion theorem (2026-09-22)

**Mandate:** the I15 many-plaquette rung (`real_research/reviews/spectral_spine_closure_2026_09_22/i15/PROOF.md` §4) reduces the
volume-uniform strong-coupling window to `x >= X_d`, `X_d = max(1, sqrt(2*A_d/c1), sqrt(2*c2*A_d))`,
`A_d = (32/3)·d(d-1)/2`, with c1, c2 the constants of Yarotsky's Theorem 1 (arXiv:math-ph/0411042v1, pp. 2-4).
Prior audit (OPUS49_BRIDGE_CLOSURE_2026-09-22.md §3) registered c1, c2 as EXISTENCE constants whose "values live in"
the 2004 J. Math. Phys. paper (DOI 10.1063/1.1705718). This door ran the hunt in the three mandated lanes, committed
results to `opus_49_doorE/`. **House rule kept: no constant is fabricated. Where no explicit constant exists in the
accessible record, that statement with its citations IS the deliverable.**

---

## 1. LANE (a) — are c1, c2 explicit in any accessible primary or secondary source?

**VERDICT: NO. c1, c2 are existence constants throughout the accessible record; the 2004 JMP paper that allegedly
holds their values is inaccessible (paywalled + bot-walled, no OA copy, no arXiv version), so its contents cannot be
verified. X_d is NOT numerically evaluable from published sources.**

Evidence, every item checked against the actual source text:

- **arXiv:math-ph/0411042v1** (Yarotsky, "Quasi-particles in weak perturbations of non-interacting quantum lattice
  systems", 11 Nov 2004 — the paper the bridge cites): Theorem 1 reads verbatim *"There exists a constant c1,
  depending only on the perturbation range Λ0, such that if sup_x ||φ_x|| < c1 ... There exists a constant c2 =
  c2(Λ0) such that Spec(H̃_Λ) ⊂ ∪_{a∈Spec(H_Λ,0)} {z : |z−a| ≤ c2 sup_x ||φ_x|| a}"* (pp. 2-4, eqs. (4)-(5)). The
  constants are pure existence objects. **A literal scan for decimal numeric literals across the entire paper text
  returns empty** — no explicit value of c1 or c2 appears anywhere in the arXiv source.
- **arXiv:math-ph/0412040v1** (Yarotsky, "Ground states in relatively bounded quantum perturbations of classical
  lattice systems", 13 Dec 2004; published **Comm. Math. Phys. 261 (2006) 799-819**, DOI 10.1007/s00220-005-1456-9):
  Theorem 1: *"There exist positive α and β, depending only on the dimension ν and the interaction range Λ0"*;
  Theorem 2: *"For any κ>1 there exists δ = δ(κ,ν,Λ0) > 0"*. Same picture: existence constants, **zero decimal
  literals in the paper text**.
- **J. Math. Phys. 45 (2004) 2134-2152**, DOI 10.1063/1.1705718 — the alleged holder of the values. Access attempts:
  (i) OpenAlex API: `open_access.oa_status = "closed"`, best/location OA URL = None; (ii) Semantic Scholar API:
  `openAccessPdf = CLOSED`, no PDF; (iii) AIP pubs.aip.org page: hard Cloudflare bot-wall ("Just a moment…",
  cannot pass headlessly); (iv) arXiv title search "Perturbations of ground states": **no arXiv version exists**;
  (v) MaRDI portal entry: metadata only, no full text. **Result: the paper's text is not accessible. Whether it
  contains numeric c1, c2 is UNVERIFIABLE from here.** What can be said: the abstract (per OpenAlex) states only
  the same qualitative claims; the author's own accessible arXiv papers contain zero numeric constants; and no
  citing paper quotes numeric values (17 citations audited at the title level via MaRDI/Crossref; the ones
  checked in depth do not).
- **J. Stat. Phys. 118 (2005) 119-144**, DOI 10.1007/s10955-004-8780-x (uniqueness paper): abstract-only access
  (Springer paywall); no numeric constants in any accessible layer.
- **Later restatements treat the constants as existential.** Henheik–Teufel–Wessel, "Local stability of ground
  states in locally gapped and weakly interacting quantum spin systems", Lett. Math. Phys. 112 (2022) 9,
  arXiv:2106.13780: their Theorem 3/Theorem 7 (Yarotsky) read *"There exist constants c, c1, c2 > 0 depending
  only on R and g"* — existential, never evaluated. Szehr–Wolf (arXiv:1402.4175), the Lie–Schwinger line
  (arXiv:1908.07450) and the gamma/gap literature likewise invoke Yarotsky without numerical thresholds.

**Exact obstruction, restated tightly:** the bridge's c1, c2 are *"there exists"* constants in the only arXiv
sources that state Theorem 1; the paper that would hold their values is closed access with no OA mirror. Evaluating
X_d therefore requires *reproducing Yarotsky's cluster expansion with tracked constants* — a research paper, exactly
as the 2026-09-22 audit concluded. Nothing in this door changes that; it upgrades the statement from "paywalled" to
"inaccessible to us and without numeric content in every accessible primary/restatement layer, with exact citations".

---

## 2. LANE (b) — is there an EXPLICIT, quantitative, volume-uniform spectral-gap theorem for SU(N) lattice gauge
theory at strong coupling anywhere?

**VERDICT: NO such theorem was found in the accessible literature. The quantitative strong-coupling results that
exist are (i) area-law statements with NON-explicit decay constants, or (ii) existence/mass-gap statements with
non-explicit thresholds.** Details:

- **Cao–Nissim–Sheffield, arXiv:2509.04688** (Sep 2025, "Dynamical approach to area law for lattice Yang–Mills") —
  the closest cousin and the only *explicit-regime* strong-coupling bound found. Theorem 1.6: Wilson-loop area
  law for G ∈ {U(N), SU(N), SO(2(N−1))}, d ≥ 2, N ≥ 2, for β < β*_G with **explicit thresholds**
  β*_SU(N) = β*_U(N) = 1/(8(d−1)), β*_SO(N) = 1/(16(d−1)) − 1/(8N(d−1)) (Def 1.4). BUT: (i) the area-law decay
  constants are `C = C(β,d,N)`, `c = c(β,d,N)` — **non-explicit and not claimed uniform in N**; (ii) it is an
  area-law (Wilson-loop expectation) statement about the Euclidean measure, **not a transfer-matrix / Hamiltonian
  spectral gap**; the "mass gap condition" it verifies is the [DF80] slab-σ-model exponential-clustering condition
  (Durhuus–Fröhlich, Comm. Math. Phys. 75 (1980) 103-151), which implies area law, not a volume-uniform quantum
  gap; (iii) its usual regime is 't Hooft (`βN` bounded, N → ∞), the *opposite* limit from the bridge's
  "x strong-coupling, N arbitrary". Physically the two are the same strong-coupling regime (large electric
  coupling ⟺ small Wilson β), so this is the right *regime* anchor, but it does NOT supply X_d-style numbers.
- **Osterwalder–Seiler**, Ann. Phys. 110 (1978) 440-471 ("Gauge field theories on a lattice"): strong-coupling
  mass gap proven via cluster expansions — existence, non-explicit β_0 and gap.
- **Seiler**, "Gauge Theories as a Problem of Constructive QFT and Statistical Mechanics", LNP 159 (1982):
  systematic strong-coupling cluster expansion; estimates carried with generic constants; no numerical threshold.
- **Borgs**, Comm. Math. Phys. 116 (1988) 309-342 (and Borgs–Seiler, CMP 91 (1983) 329-380): confinement/area-law
  phase at strong coupling, incl. continuous-time (Hamiltonian) lattice Yang–Mills — existence, no explicit
  constants.
- **Shen–Zhu–Zhu**, "A stochastic analysis approach to lattice Yang–Mills at strong coupling", Comm. Math. Phys.
  400 (2023) 805-851, DOI 10.1007/s00220-022-04609-1: Bakry–Émery/log-Sobolev in the
  't Hooft regime — explicit β-dependence in the curvature but N-dependent constants; yields Poincaré/exponential
  clustering, not a volume-uniform spectral gap.
- **d = 2** is exactly solvable (confinement exact), but a single-dimension fact, not the bridge's general d.

So the alternative lane has no drop-in replacement: every quantitative strong-coupling result stops at either a
non-explicit constant or a non-gap observable. **This corroborates (independently, via the physics literature)
that the only route to a numeric X_d is re-deriving a strong-coupling cluster expansion with tracked constants.**

---

## 3. LANE (c) — computation.

**VERDICT: not performed with real constants, because no real constants exist.** The mandated computation
(`X_2, X_3, X_4` numerically) would have required fabricating c1, c2. Instead `verify.py` machine-checks the
exact parametric content and the sensitivity SHAPE:

1. **Exact A_d** (verified with `Fraction`): A_2 = 32/3 ≈ 10.6667, A_3 = 32, A_4 = 64, A_5 = 320/3 ≈ 106.6667,
   A_6 = 160, A_8 = 896/3 ≈ 298.6667. (Also the hunt caught a slip in an early hand value — A_2 is 32/3, not
   16/3; fixed by the assert before committing.)
2. **Consolidation identity** (verified over 200,000 random (c1, c2) pairs, d = 2, 3, 4): the two independent
   constants collapse to one effective parameter θ := min(c1, 1/c2), via `max(sqrt(2A_d/c1), sqrt(2c2 A_d)) =
   sqrt(2A_d/θ)`. Hence
   **X_d = max(1, sqrt(2A_d/θ)), θ = min(c1, 1/c2)**.
   The two source conditions `η ≤ A_d/x² ≤ c1/2` and `c2·η ≤ 1/2` are re-verified at x = sqrt(2A_d/θ).
3. **Sensitivity shape** (explicitly-labelled hypothetical θ, NOT sourced): X_d ∝ θ^(−1/2) — a change of θ by
   10^4 moves X_d by 10^2. E.g. (hypothetical θ): θ=1e-2 → X_2≈46.2, X_3≈80, X_4≈113; θ=1 → X_2≈4.62, X_3=8,
   X_4≈11.3. No entry on this table is claimed to be Yarotsky's θ; it exists only to show the functional shape.
   **No numeric X_2, X_3, X_4 is asserted anywhere in this door.**

Arithmetic summary (what is true, exactly): `X_d = max(1, sqrt(2A_d/θ))` with A_d exact as above; the *value* of θ
is unknown in the accessible record, so X_d is determined only up to an arbitrary multiplicative constant
√(1/θ). That multiplicative undetermination IS the exact obstruction, now stated in the cleanest form.

---

## 4. What this door does and does not change for the bridge

- **UPGRADES the obstruction** from "values allegedly live in a paywalled 2004 JMP paper" to the verified statement:
  (1) c1, c2 are existence constants in every accessible primary source (both arXiv papers, machine-scanned: zero
  numeric literals); (2) the JMP paper is inaccessible (paywalled, Cloudflare-blocked, no OA per OpenAlex+Semantic
  Scholar, no arXiv version, no MaRDI full text) — its contents cannot be verified, and no citing literature
  quotes numeric values; (3) the alternative strong-coupling literature (OS78, Seiler, Borgs, SZZ23, CNS25) offers
  no explicit volume-uniform spectral gap either, only non-explicit-constant area law or existence.
- **DELIVERS the honest completed lane** (per the mandate): the exact statement "c1, c2 are not explicit in any
  accessible form; the JMP 2004 text is not accessible; no alternative explicit quantitative volume-uniform
  spectral-gap theorem exists" IS the deliverable, with citations 10.1063/1.1705718, 10.1007/s10955-004-8780-x,
  10.1007/s00220-005-1456-9, arXiv:2106.13780, arXiv:2509.04688, [OS78], [Borgs88], [SZZ23], [DF80].
- **Specifies the rescue lane** (unchanged, named): re-running Yarotsky's cluster expansion with tracked constants
  for the specific gauge model (H_0 = normalized on-site Casimir gap 1, perturbation = plaquette trace terms,
  b_N ≤ 2N) — a research paper; or an independent OS/reflection-positivity + explicit strong-coupling cluster
  expansion producing an explicit mass gap. Neither exists on the record today.
- **KEEPS the rung honest**: "many-plaquette gap proven to EXIST uniform in N and volume for x ≥ X_d, X_d
  finite-but-unknown" stands exactly as audited. No `X_d = [number]` is added, because none can be sourced.

---

## 5. Files

- `opus_49_doorE/REPORT.md` — this report.
- `opus_49_doorE/verify.py` — runnable arithmetic: exact A_d, the consolidation identity (200k random pairs),
  the source-condition re-check at the threshold, and the explicitly-labelled hypothetical sensitivity table.
  `python3 verify.py` → "ALL CHECKS PASSED".
- Commit `opus_49d doorE EXPLICIT X_d HUNT`, new folder only.


---

**2026-09-22 addendum (append-only).**
- Lane (c)'s "no numeric X_d" is superseded by an independent route. A cluster expansion
  with tracked constants gives X_3 = 185.3, uniform in N
  (`real_research/reviews/ym_door_swings_2026_09_22/ym1_hamiltonian/`). Yarotsky's c1 and c2
  are still unknown and are no longer needed.
- Lane (b) is refined: Shen–Zhu–Zhu 2023 does give an explicit strong-coupling threshold for a
  strictly positive mass gap (β_W < N²/(16(D−1))). Its rate is not explicit and degrades with
  N. An explicit-rate Dobrushin bound is in `.../ym1_euclidean/`.
