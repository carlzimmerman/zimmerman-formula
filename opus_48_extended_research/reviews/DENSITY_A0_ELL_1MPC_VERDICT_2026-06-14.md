# Density-law a0 at ell = 1/mu = 1 Mpc (AeST scalar Compton wavelength) — VERDICT: BREAKS-GALAXY-RAR **and** OVER-CLOSES-CLUSTERS (2026-06-14)

*The density reading a0(x) = (c/2)√(G ρ_total,smoothed-over-ell) tested on the HARD double constraint with
ell DERIVED from the framework (the CMB-pinned AeST scalar mass scale 1/μ ~ 1 Mpc), NOT tuned. Real 175 SPARC
rotation curves + real eRASS1 (9,830 clean clusters). Script: `density_a0_ell_1mpc_test.py`. Quarantine held:
a0/Z never asserted derived; μ flagged a CMB-pinned AeST input. Honest both ways, per the #1 working rule.*

---

## Is ell DERIVED or TUNED? — genuinely DERIVED (this is the honest strength of the proposal)

ell = 1/μ ≈ 1 Mpc is the **AeST scalar Compton wavelength**, pinned by the CMB acoustic fit
(Skordis–Złošnik 2021; Verwayen–Skordis–Złošnik 2024 require m²/f_G ≲ 1 Mpc⁻² ⟹ 1/μ ≳ 1 Mpc). It is the
framework's own dark-field coherence scale — below 1/μ the field is locally uniform, above it tracks
structure — and it was fixed by cosmology **before** this test, not chosen to land clusters at 1.2–1.5. So
this is the rare case where the smoothing scale the cluster deep-dive flagged as "UNDERIVED" is, in fact,
framework-native and derived. **That makes the verdict load-bearing: a genuinely derived ell is tested, and
it fails — this is not "we couldn't find a scale," it is "the framework's own scale doesn't work."**

## The two numbers (real data, framework dS–Unruh ν, Υ=0.70)

| test | baseline (universal 9.36e-11) | density-a0 at **ell = 1 Mpc** | verdict |
|---|---|---|---|
| **GALAXY RAR scatter** | 0.1448 dex | **0.1943 dex** (+0.0495, **+34%**) | **BREAKS** (robustly +0.03–0.07 dex) |
| **CLUSTER η(R500) median** | 2.33 | **0.47** (a0 boost ~27×) | **OVER-CLOSES** (η≪1; only 1% in [1.2,1.5]) |

**A single ell = 1 Mpc fails BOTH simultaneously.** Not one or the other — both.

## Why it breaks galaxies (the RAR smears)

A 1 Mpc ball is **small enough to register a galaxy's own halo**. An L* halo (~10¹² M⊙) in a 4.19 Mpc³ ball
gives ⟨ρ⟩ ~ 4 ρ_DE → a0 ~ 1.5–2.1× cosmic; a dwarf (10¹¹) ~ 1.3×; a group (10¹³) ~ 5.4×. So a0 becomes a
**function of host halo mass** and is no longer universal across galaxies — the RAR ridge **smears**, inflating
the scatter from 0.145 → 0.194 dex. The inflation is **robust** to the baryon→halo retention assumption
(+0.033 dex at Mb/Mh=0.05, +0.049 at 0.03, +0.074 at 0.017) and appears on McGaugh ν too (+0.076 dex). This is
exactly the framework's distinctive falsifiable prediction (a0_dense-env > a0_field) — **and on real SPARC it
goes the wrong way: it inflates, it does not tighten.**

## Why it over-closes clusters (the smoothing does NOT dilute)

The deep-dive memo *hoped* a Mpc smoothing would dilute a cluster to a ~15× "ambient" boost (η→1.2–1.5). It
does not, because **the eRASS1 median cluster has R500 ≈ 0.77 Mpc — comparable to ell = 1 Mpc.** A 1 Mpc ball
centered on the cluster is **dominated by the dense core** (mean enclosed ~700–830 ρ_crit), not diluted to
ambient. That gives a a0 boost of **~27–33×**, far past the ~15× sweet spot, pulling η down to **~0.42–0.47**
— a gross **over-closure** (the cluster predicts ~2× too MUCH gravity). To hit the 1.2–1.5 band the cluster
density must be diluted to **~10 ρ_crit**, which needs a smoothing scale of **~8–12 Mpc** (full-ν scan: η
median 1.27 at 8 Mpc, 1.39 at 10 Mpc, 55% in band at 10 Mpc). **That ell is ~10× larger than 1/μ — it is the
supercluster/turnaround scale, NOT the AeST Compton wavelength, and adopting it would be pure tuning.**

## The structural trap (why no single ell threads)

The two failures are two sides of one scale mismatch:

- The ell **small enough to over-close clusters** (≲ a few Mpc, R500-comparable) is **also small enough to
  register galaxy halos** → breaks the RAR.
- The ell **large enough to dilute clusters to η~1.35** (~10 Mpc) is **also large enough to wash a galaxy's
  halo into the cosmic mean** (10¹² M⊙ is negligible in ~4000 Mpc³) → the RAR is preserved (+0.0001 dex,
  verified).

So a scale exists that **saves galaxies** (~10 Mpc), and it happens to be near the scale that **threads
clusters** — but it is **NOT 1/μ**, and it is **not derived**. **The framework's own derived ell (1 Mpc) sits
in the worst spot: small enough to break galaxies, small enough to over-close clusters.**

## The a0↔Λ cost (the superset question, stated straight)

The density reading **is** a cosmic superset: ρ_total,smoothed → ρ_crit (the cosmic mean) gives
a0 = 1.13×10⁻¹⁰ ~ cH₀ — still Milgrom's coincidence, still the rho_total footing. **But it trades the clean
identity** a0 = c²√(Λ/32π) = 9.36×10⁻¹¹ **for** a0 ↔ local density. The exact Λ-value 9.36×10⁻¹¹ re-emerges
*only* in the empty/de-Sitter limit ρ_smoothed = ρ_DE exactly — a limit **no real system occupies** (every
galaxy and cluster has matter). So the cost is real: the a0↔Λ lock survives only cosmically/asymptotically, and
every bound system reads a *different* a0 set by its environment. That is the price of the density reading, and
the SPARC RAR (0.13-dex tight, a0 demonstrably universal) is precisely the data that resists it.

## VERDICT: BREAKS-GALAXY-RAR **and** OVER-CLOSES-CLUSTERS

The one derived, CMB-pinned framework scale — ell = 1/μ = 1 Mpc — **does not thread the double constraint.** It
inflates the SPARC RAR scatter +34% (0.145→0.194 dex, robustly) *and* over-closes eRASS1 clusters to η~0.47.
The scale that would thread clusters (~8–12 Mpc) is ~10× larger than 1/μ, is the supercluster scale not the
AeST Compton wavelength, and would be a tuned input — and even there the galaxy RAR is only saved because the
smoothing washes the halo out entirely. **The density-law-a0 escape for clusters, with the framework's own
derived smoothing scale, is closed on real data.** This is consistent with — and independent of — the AeST
mass-term gauntlet (`AEST_SINGLE_MU_GAUNTLET`, FALSIFIED-AS-CLOSURE): there the *field* smoothed over 1/μ left
clusters at η~1; here the *density* smoothed over 1/μ over-shoots to η~0.47. Both routes at the one CMB-pinned
scale fail to deliver the eRASS1 ~2× — from opposite sides.

**Honest both ways:** ell is genuinely derived (real strength, credited); the cosmic superset holds (credited);
the falsifiable a0_env prediction is real (credited). It fails on the merits — galaxies inflate, clusters
over-close, robustly, on real data — not by a hostile convention. Not manufactured, not dismissed.

*Sources: Skordis–Złošnik 2021 PRL 127 161302; Verwayen–Skordis–Złošnik 2024 MNRAS 531 272 (2304.05134);
Durakovic–Skordis 2024 JCAP 04 040 (2312.00889); Lelli+2016 SPARC; Bulbul+2024 eRASS1 (A&A 685 A106).
Companion: AEST_SINGLE_MU_GAUNTLET_2026-06-14.md, CLUSTER_DEEPDIVE_VERDICT_2026-06-14.md.*
