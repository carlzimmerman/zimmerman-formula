# L73 — even a healthy integrable-clock action is complete only below a galaxy: excess-spent-once binds it

**The excess-spent-once theorem binds the lead's integrable-clock action, for the same structural reason
it binds every other single-metric branch: ordinary matter is minimally coupled to ONE physical metric
`g`, so a cold component in the CMB's amount — which the action still needs for clusters and the CMB —
transmits its Newtonian pull to baryons with `η = 1` in galaxies and overshoots the rotation curves by
median ×1.69. Keeping MOND inside the clock changes WHERE the anomaly is produced (a genuinely different
channel — which is how L66 found it escapes the L60/L69 deep-MOND kill) but NOT the transmission factor
`η`, which is a property of the cold-matter→baryon channel the clock leaves untouched.** This lane's
verdict is **conditional on L71/L72** establishing galactic health; it assumes nothing about health and
asks only whether, IF healthy, the cluster+cosmology sector can be complete. It cannot.

2026-09-09. Lane L73 of [CHARTER.md](CHARTER.md), the "complete theory" question against
[L61_PERMITTED_BRANCHES.md](L61_PERMITTED_BRANCHES.md) / [L55_COMPOSITION_KERNEL.md](L55_COMPOSITION_KERNEL.md)
and the lead-action escape recorded in [L66_LEAD_ACTION_HEALTH.md](L66_LEAD_ACTION_HEALTH.md) /
[L69_HEALTHY_DEEPMOND.md](L69_HEALTHY_DEEPMOND.md).
Script: [L73_lead_completeness.py](L73_lead_completeness.py) → [L73_lead_completeness.out](L73_lead_completeness.out).
**16 checks, 16 PASS / 0 FAIL; exit 0; runtime 0.5 s.**

**Polarity.** Each check asserts a **statement** and PASS means the statement is true. Most PASSes here are
**negative for the construction** — read the statement. Both a₀ footings on every dimensional number:
9.3619×10⁻¹¹ / 1.1279×10⁻¹⁰ m s⁻². Nothing under `closure_2026/` was imported or executed; the lead's
action structure was read from its own markdown (`IC4_ACTION.md`, `IC23_MIXTURE.md`,
`VACUUM_DENSITY_RECOMBINATION.md`) offline and its reference numbers hard-coded as reproduction targets.
The dark-sector no-go (g03w–g04j) and L6/L55's screening closures are **cited, not re-run**.

---

## 1. Controls, first — all five PASS

| control | reproduced here | published |
|---|---|---|
| **A0** mode counts, `N = (P−2F−S)/2` | GR **2**, GR+scalar **3**, Einstein-aether **5**, khronometric **3** | L61 A1–A4 |
| **A1** L61's overshoot | median `g_pred/g_obs` = **1.692** at η = 1, 2059 deep-MOND points, weakest (baryon-sourced) kernel | L61 B1: 1.692 |
| **A2** L61's transmission ceiling | galaxies admit η ≤ **0.582 / 0.486** (baryon-src) or **0.355 / 0.276** (total-src); CMB requires **1.000** | L50 / L49 |
| **A3** L61's ordering closures on (c) | range η(r_s)=**1.3e-7**; density **498×**; acceleration **0.99 dex** / clusters at-or-below galaxies; potential **64×** — all wrong ordering | L61 B4–B7 |
| **A4** cluster residual amount | MOND kernel post-residual `g_HSE/g_kernel` = **2.07** at r ≥ 500 kpc; required source/baryon = **6.96** | L7/L41 (~5.7×) |

Every control passes and reproduces L61's numbers exactly, so nothing below is quotation.

---

## 2. The transmission channel in the lead's action (PART B) — the crux, answered

From `IC4_ACTION.md`'s own equations. The full action is

```
S4 = INT sqrt(-g) { (m/2)[ R4 - 2Λ + 4KW - 6W^2 + 2(1-u^2) a.a - 2 a0^2 U(u^2)
                           + (Q^2/a0^2)(J + Rhat F) ] + κ X }  +  S_m[g,ψ]
```

Two facts stated verbatim in the file fix the two channels:

1. **The cold-matter transmission channel (B1 PASS).** *"The independently diffeomorphism-invariant
   `S_m[g,ψ]` is unchanged. Its own on-shell Ward identity remains `∇_μ T^{μν}=0`. No extra force on
   ordinary matter is inserted."* A pressureless component — whatever supplies it — enters through its
   stress `T^{μν}`, sourcing the **same** physical metric `g` via the Einstein–Hilbert `(m/2)R4`. Baryons
   are minimally coupled to that **same** `g`. So a cold component's Newtonian pull reaches a baryon by
   **ordinary gravity in `g`**, the identical channel at recombination and in a galaxy, because it is **one
   metric at both epochs**. The transmission factor is `η = 1` at both, with no scale- or
   environment-dependence available.

2. **The MOND-production channel (B2 PASS).** The a₀ scale rides the **clock's own** acceleration invariant
   `2(1−u²)a_μa^μ − 2a₀²U(u²)`, with `a_μ = D_μ ln N` and `N=(2X)^{−1/2}` a functional of the clock `T`.
   There is **no separate MOND scalar φ and no AeST coupling `2(2−K_B)a^μ∂_μφ`** — exactly the L66 escape
   from the deep-MOND lapse kill. This IS a different channel from B1's.

**B3 [THE CRUX] PASS — the different channel does NOT change η.** Excess-spent-once needs η *smaller* in
galaxies than at recombination (≤ 0.58 vs 1.00). But η is a property of the **cold-matter→baryon channel
alone** (B1). Producing MOND in a separate clock channel (B2) changes `A_K`, the anomaly the kernel adds; it
leaves the cold-matter channel — minimal coupling to the single metric `g` — **untouched**. To make η < 1 in
galaxies the lead would have to break B1's channel itself, by one of:

| lever | available in the lead's action? |
|---|---|
| a **second metric** for the cold component | **No** — *"the barred metric is a change of variables on the clock slices, NOT a second metric for matter or light"* |
| a **non-minimal** (disformal/conformal) matter coupling | **No** — `S_m[g,ψ]` minimal, *"no extra force on ordinary matter"* |
| a **range** (graviton mass / Yukawa) | **No** — wrong ordering (A3): suppresses long range, not short |
| **monotone environmental screening** (ρ, g, Φ) | **No** — wrong ordering (A3): recombination is denser/deeper |

**No single-metric, minimally-coupled lever suppresses the cold pull in galaxies relative to
recombination.** Hypothesis (c) binds. The MOND channel and the cold-matter channel are **different, but
they carry the same transmission factor.**

---

## 3. The decisive test (PART C) — both sub-cases run

### 3.1 Sub-case (i): it still needs a cold component → the overshoot fires

**C-i-1 PASS.** MOND — in the clock or anywhere — under-predicts clusters (A4: `g_HSE/g_kernel = 2.07`) and
cannot make the CMB acoustic peaks without a pressureless component `Ω_c h² = 0.12`. The lead's own
`VACUUM_DENSITY_RECOMBINATION.md` concedes it: its z=1100 fractions *"use reference-model matter, INCLUDING
its inferred nonbaryonic component; it must not be presented as a baryon-only IC cosmology prediction."*

**C-i-2 PASS — EXCESS-SPENT-ONCE FIRES.** That required cold component, at the CMB amount, reaches baryons
through `g` with η = 1 (B1), and MOND-in-clock does not lower η (B3). It overshoots the rotation curves by
median **×1.69** while the admissible galaxy window is η ≤ **0.582 < 1**. A working kernel and a full cold
cosmology are alternatives, not complements — the same conclusion as L55/L61 for the deposited action.

### 3.2 Sub-case (ii): the clock sector supplies structure itself

Three tests, all closing the route:

- **(ii-a) PASS — a dust-like clock is a cold component.** `VACUUM_DENSITY_RECOMBINATION.md`: *"A dust-like
  clock would behave gravitationally as an additional matter component; renaming it does not remove its
  abundance, lensing, perturbation and conservation obligations."* A dust-like clock gravitates through `g`
  like cold matter (η = 1) and **inherits the overshoot**. Renaming the cold component "the clock" changes
  nothing.

- **(ii-b) PASS — a non-dust clock structure sector must reproduce a ΛCDM cold-halo signature.** The
  pair/cluster ladder is non-monotone in scale: at a **fixed** radius (132 kpc) pairs need a boost ratio
  **30.9 ± 1.5** while clusters measure **9.20 ± 1.30** — a factor **3.4 at 11σ** (L41/FINDINGS). L41 proved
  no single host-blind profile `M_X = C·M_bar^a·r^b` serves both scales — the ratio, shear, and
  galaxy-non-overshoot gates open **three pairwise-disjoint windows** in the exponent. And the ladder simply
  **is** ΛCDM's stellar-to-halo-mass relation (abundance matching gives 31.8 vs 30.9, 0.6σ). A clock
  structure sector would have to reproduce a cold-DM-halo signature with no cold-DM halo to produce it; none
  has been exhibited.

- **(ii-c) PASS — the lead's own cosmology hits the wall.** `IC23_MIXTURE.md` varies the IC20 action with
  radiation + matter and **no separate CDM** — exactly the "clock supplies structure" route. Its own
  continuation **fails**: a light-cone crossing (a scalar characteristic exceeds the physical light cone) is
  bracketed at **Q_cross ≈ 0.00372**, i.e. after only **~0.4% of an e-fold** of barred expansion. Its own
  words: *"This falsifies a healthy extended-history claim for this specified trajectory and coefficient
  choice."* That is the **same causality wall** the deposited action's dust doors hit — the recorded
  **g03w–g04j dark-sector no-go** (wave/de Broglie DM, thermal relic, four condensate constructions,
  environment switch), which this lane **does not reopen** without a new mechanism type, and none is
  exhibited.

---

## 4. Verdict (PART D)

| check | statement (PASS = true) |
|---|---|
| **D1** | the lead's action **is bound** by excess-spent-once: it needs a cold component, that component reaches baryons through the single metric with η = 1, and neither the dust-like nor the non-dust clock-structure route escapes |
| **D2** | the MOND channel and the cold-matter channel are **different** (MOND in the clock, cold matter through `g`) but that difference does **NOT change η** — hypothesis (c) binds anyway |
| **D3** | **even a healthy version cannot be complete**: it is complete only below a galaxy, the SAME ceiling as the deposited action — **conditional on L71/L72** establishing galactic health |

### Three-sentence verdict

**Even granting the lead's integrable-clock action is healthy at galaxy scale (L71/L72's question, not this
lane's), it is bound by the excess-spent-once theorem exactly as every other single-metric branch is:
because ordinary matter is minimally coupled to ONE physical metric `g`, a cold component in the CMB's
amount — which it still needs for clusters and the CMB — transmits its Newtonian pull to baryons with η = 1
in galaxies, overshooting the rotation curves by median ×1.69, and keeping MOND inside the clock changes
WHERE the anomaly is produced (a different channel, which is how it escaped the L60/L69 kill) but NOT the
transmission factor η, a property of the cold-matter→baryon channel the clock leaves untouched.** The one
route that could differ — letting the clock sector supply cluster mass and structure with no separate cold
component — does not escape either: a dust-like clock is a cold component that inherits the same η = 1
overshoot, and a non-dust clock structure sector must reproduce the non-monotone pair/cluster ladder (a ΛCDM
cold-halo signature) and the CMB while the lead's OWN mixed cosmology (IC23) already loses causality at 0.4%
of an e-fold, the same wall as the recorded g03w–g04j dark-sector no-go. **So even the last candidate is
complete only below a galaxy — "a healthy version is still not a complete theory" is the honest and
load-bearing result, conditional on L71/L72; κ = ½ remains fitted and nothing here favours any framework
over ΛCDM.**

---

## 5. Caveats, stated rather than buried

1. **This lane's verdict is conditional on L71/L72.** It assumes nothing about the lead's galactic health
   (L66 left the deep-MOND transverse health uncomputed and flagged a distinct indefinite-Hessian concern).
   It asks only whether, IF healthy, the cluster+cosmology sector can be complete — and the answer is no.
2. **The theorem's scope is (H-c) and the cold component's galaxy profile**, inherited from L55/L61: a
   theory that distributes the cold component away from galaxy halos escapes the theorem itself and is
   closed separately by the dark-sector no-go (cited, not re-run). The lead's action offers no such
   distribution — its cold component, whatever supplies it, gravitates through the same `g`.
3. **The generous of L49's two galaxy criteria (median RAR shift ≤ 0.11 dex) is carried throughout**, so no
   deficit is manufactured; the strict criterion would tighten every η ceiling by roughly a factor two.
4. **`Q_cross ≈ 0.00372` is read from `IC23_MIXTURE.md` offline** as a reproduction target, and is that
   file's own high-precision numerical bracket, not a rigorous interval enclosure; it is the lead's own
   result, cited, not re-run here.
5. **The cluster residual and pair/cluster ladder numbers are the repository's own** (cluster audit JSON;
   L7/L21/L41/L42). This lane recomputes the cluster residual from that JSON and reproduces the ladder
   factor; the ladder's incompatibility windows and the abundance-matching 0.6σ result are cited from L41.
6. **Nothing here favours this framework over ΛCDM and nothing here constrains ΛCDM.** The cold component,
   its amount and its ΛCDM-shaped ladder are ΛCDM's, imported wholesale; **κ = ½ remains fitted**.

---

## 6. Reproduction

```
python3 fable_independent_2026/L73_lead_completeness.py
```

Exit 0, 0.5 s. **16 checks, 16 PASS / 0 FAIL** (polarity: PASS = statement true). Five controls (A0–A4)
rebuild the four mode counts, L61's overshoot (1.692), L61's transmission ceilings (0.582/0.486,
0.355/0.276), L61's four ordering closures, and the cluster residual amount — each from committed data with
independent code or cited from the record. The lead's action structure is read from its own markdown
offline; nothing under `closure_2026/` is imported or executed.
