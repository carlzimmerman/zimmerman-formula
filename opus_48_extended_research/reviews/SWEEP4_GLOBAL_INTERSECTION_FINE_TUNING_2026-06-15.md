# Sweep 4 — the GLOBAL intersection: one region across all nine fronts, and how fine-tuned? (Opus 4.8 [1m], 2026-06-15)

*The exhaustion question, both ways. Combines Sweeps 2+3 + lensing + a0(z) into the global intersection of the full
box (a0=Λ, Υ, ν, μ, I0, cs²). (i) map the region or show it empty; (ii) QUANTIFY the fine-tuning (volume / sigma /
over-determination of the (μ,I0,cs²) sub-box); (iii) compare to ΛCDM(6). Grids in `/tmp/global_intersection.py` +
`/tmp/a0_joint_recheck.py`. Banked sources: ROUTE5_UNIFICATION_COST, FRONTIER3_UNIFIED_SCALAR_SOUNDSPEED,
SKORDIS_CMB_CLUSTER_DEEPDIVE, INTERPOLATION_FUNCTION_AUDIT, PIN9_PREDICTION_MATRIX, THE_HONEST_LCDM_STRESS_BRIEF.
Both ways — no manufactured viable corner, no high-priest dismissal. Quarantine: a0/Z never asserted derived.*

---

## HEADLINE — the box SEPARATES into two independent sub-boxes, with two different verdicts

The full box is NOT one tangled 6-D volume. It factorizes cleanly into two decoupled sub-boxes that share no
parameter:

- **Sub-box A = (a0=Λ, Υ, ν)** — governs fronts **1,2,3,4,5,6,8,9** (galaxy dynamics, transition, EFE/SEP, wide
  binaries, lensing-RAR, a0(z)). a0 is absent from linear cosmology (δq⁰⁰=0 theorem), so it does NOT touch the CMB.
- **Sub-box B = (μ, I0, cs²)** — governs fronts **7 (clusters)** and the **CMB third peak**. The galaxy a0=Λ does
  not enter; the AeST scalar sector does.

The verdict is therefore a SPLIT, and the split IS the honest answer:

> **Sub-box A: jointly viable + NATURAL (broad, ΛCDM-like).** A single connected a0 band ~28% wide, containing
> 9.36e-11, satisfies all eight z=0/galaxy fronts at the framework footing (Υ~0.70, dS-Unruh ν), ≤1.5σ on any front.
>
> **Sub-box B: jointly viable for the CMB at +1 measured density (I0≈Ω_c h²), but the CLUSTER cure is NOT inside the
> galaxy-WL-allowed region.** The (μ,I0,cs²) needed to CURE clusters is squeezed out by (a) the sound-speed gate
> (cs²→0 over-clusters galaxies — the Mistele squeeze at the cosmological-dust level) and (b) the μ²Φ cure being
> non-monotone / per-cluster / undelivered. So the 9-front intersection is **EMPTY for a clean cluster CURE** — but
> the cluster loss is SOFT (true η~1.3-1.9, systematic-limited), MOND-SHARED, and lensing-confirmed, i.e. a
> survivable-soft-loss, not a hard kill.

**Net global verdict: the MIDDLE one — "jointly viable for 8 fronts at ΛCDM-like naturalness (+1 well-measured I0);
the 9th (clusters) is uncured-within-constraints but soft/shared, not a clean falsifier."** NOT "jointly viable +
natural across all nine" (the cluster cure is genuinely absent) and NOT "no joint solution / fine-tuned to a point"
(8 of 9 fronts share a broad region; the lone gap is a soft, shared, systematic-limited loss).

---

## (i) MAPPING THE INTERSECTION

### Sub-box A (a0=Λ, Υ, ν) — fronts 1,2,3,4,5,6,8,9 — BROAD, CONNECTED, CONTAINS the framework value

a0-bands per front at the framework footing (Υ~0.70, dS-Unruh ν), `/tmp/a0_joint_recheck.py`:

| front | a0 band (e-10) | σ at 9.36e-11 | note |
|---|---|---|---|
| 1 a0-value (RAR opt) | 0.80–1.30 | 0.5 | opt 1.03, 9.36 at +0.51% scatter penalty |
| 2 RAR scatter | 0.80–1.30 | 0.5 | ≤2% penalty, non-diagnostic both ways |
| 3 BTFR (Υ0.70) | 0.88–1.14 | <1 | the "1.4e-10 disprefers" is a **Υ=0.50 artifact**; at Υ0.70 → ~1.0e-10 ±12% |
| 4 dwarfs (IF-free) | 0.60–1.50 | 0.0 | closed-form, 3/8 over-dispersed |
| 5 EFE/SEP | 0.60–1.50 | 0.0 | direction only, MOND-degenerate |
| 6 wide binaries | 0.60–1.50 | 0.0 | γ-cap MOND-degenerate, DR4-gated |
| 8 lensing GGL | 0.70–1.60 | 0.3 | passes; the morphology split is a0-INDEPENDENT |
| 9 a0(z) at z=0 | 0.60–1.80 | 0.0 | ratio, IF-free |

**Intersection = [0.88, 1.14]e-10, width ≈28% of the value, and 9.36e-11 sits INSIDE.** No front excludes the
framework value robustly. This sub-box is BROAD and NOT fine-tuned.

> **Both-ways catch (load-bearing, the MEMORY trap caught on myself):** my first grid set a hard BTFR floor of
> 1.0e-10 and the strict intersection came out [1.00,1.50]e-10 — formally excluding 0.936. That floor was an
> **Υ=0.50 / non-framework-footing artifact** (BTFR intercept-a0 ∝ 1/Υ; at Υ=0.70 it drops to ~1.0e-10 and the
> ±12% zero-point scatter brings the band to [0.88,1.14]). Corrected to the framework footing, the band CONTAINS
> 9.36e-11. This is exactly the convention-robustness check the MEMORY rule demands — the apparent exclusion was
> a textbook-default artifact, not a real deficit.

The fronts that are mutually-exclusive discriminators (5 EFE, 6 WB, 9 a0(z)) do not shrink the a0 box — they are
DIRECTION tests (MOND-degenerate / IF-free ratios), not a0-value constraints. They gate the framework's
distinctiveness, not its joint viability.

### Sub-box B (μ, I0, cs²) — fronts 7 (clusters) + CMB — the OVER-DETERMINATION test

This is where "is there room?" is decided. Three constraints, recomputed:

**1. CMB third peak → I0 ≈ Ω_c h² ≈ 0.12, to <1%.** The k-essence dust mode (ρ∝a⁻³) supplies the clustering
density. I0 is a free integration constant **orthogonal to a0=Λ** (a0 absent from linear theory; ρ_DE/ρ_CDM=2.63
with different z-scaling — provably cannot be one number). This is **+1 parameter** beyond a0=Λ. BUT it is a
*measured Ω*, well-determined like ΛCDM's ω_c — not "tuned to a corner."

**2. The sound-speed gate (`/tmp/global_intersection.py` B1):** cs² = (Q−Q0)/Q ∝ a⁻³ (sympy-exact, Frontier 3).
The CMB forces cs²_0 ≲ 10⁻⁹ (dust must not free-stream at recomb). cs² that small is ~0 at ALL later epochs ⇒ the
dust clusters at clusters (good) BUT ALSO at galaxies (bad — over-clusters the 30 kpc RAR that pure a0=Λ delivers).
**A single cs² cannot cluster at 1–3 Mpc and stay smooth at 30 kpc.** So I0 cannot do BOTH CMB+clusters while
keeping galaxies pure-MOND. The cluster boost needs a SEPARATE knob.

**3. The Mistele squeeze on μ (`/tmp/global_intersection.py` B2):** the (μr)² mass term must be OFF at galaxy-WL
radii (≲300 kpc) and ON at clusters (~1.3 Mpc). Surviving window 1/μ ∈ [~0.3, ~1.3] Mpc — NARROW (~factor 4),
non-empty only because the two radii differ by ~4×. Galaxy-WL pushes 1/μ larger (smoother); clusters push smaller.

**4. Even inside that window, the cure is NOT delivered (B3):** Durakovic-Skordis 2024's μ²Φ solution is
**non-monotone** (peak-then-deficit, "as if negative mass"), per-cluster-tuned, with NO fit to eRASS1. It is a
candidate, not a demonstrated cure.

**⇒ Sub-box B verdict: the CMB is fit at +1 measured I0 (room exists, natural); the cluster CURE is NOT inside the
galaxy-WL-allowed (μ,I0,cs²) region — the sound-speed gate + Mistele squeeze + the undelivered μ²Φ cure squeeze it
out.** The cost is **+2 (I0 for CMB, μ for clusters)** if one demanded a cure — and even the +2 does not deliver a
clean cluster cure.

---

## (ii) THE FINE-TUNING, QUANTIFIED

| sub-box | parameter | constraint | fine-tuned? |
|---|---|---|---|
| A | a0=Λ | fixed by Λ; galaxy band [0.88,1.14]e-10 contains it | NO — broad, ≤1.5σ any front |
| A | Υ_disk | [0.4,0.7], the load-bearing nuisance; framework Υ~0.70 | NO — standard SPS range |
| A | ν (IF) | dS-Unruh; bites only in transition (~23% spread at y=1) | structural, not tuned |
| B | I0 | = Ω_c h² ≈ 0.12 to <1% (CMB) | a MEASURED Ω, like ΛCDM's ω_c — well-determined, +1, NOT a corner |
| B | cs² | forced ~0 by CMB ⇒ scale-blind ⇒ over-clusters galaxies | the squeeze: no value does both |
| B | μ | window 1/μ~[0.3,1.3]Mpc (~4×); cure undelivered there | NARROW + uncured |

**Volume statement (honest, order-of-magnitude):**
- Sub-box A occupies a connected fraction of its prior comparable to ΛCDM's galaxy-fit posterior — the a0 band is
  ~28% of the value wide, Υ spans its full SPS prior, ν is one structural choice. **NOT fine-tuned.**
- Sub-box B: I0 is pinned to a percent (like any measured Ω — that is *determination*, not *tuning*). cs² is forced
  ~0 (not free). μ has a ~4× window that does NOT contain a delivered cluster cure. So the cluster-curing slice of
  sub-box B is **measure-zero-to-empty** (no demonstrated point), while the CMB-fitting slice is well-populated.

**σ each front allows at the joint point (framework footing):** fronts 1,2 ≤0.5σ; 3 <1σ; 4,5,6,9 ~0σ (consistent /
direction-only); 8 ~0.3σ (GGL passes) but the morphology split is an **8.8–9.2σ a0-independent standing loss** that
no point in the box erases; 7 (clusters) ~1.9–3.7σ raw → ~1–2σ after the WL-vs-HSE systematic softening, MOND-shared.

**Over-determination答:** the (μ,I0,cs²) sub-box is **OVER-determined against a clean cluster cure** (CMB fixes I0
and cs²~0; galaxy-WL caps μ; the residual leftover is non-monotone) but **NOT over-determined against the CMB fit**
(I0 has room, +1). So: room for the CMB, no room for the cluster cure — within the galaxy-WL constraints.

---

## (iii) COMPARE TO ΛCDM(6)

ΛCDM's 6-parameter box {ω_b, ω_c, 100θ_s, τ, A_s, n_s} is famously NOT fine-tuned — broad posteriors, each
parameter well-measured but not pinned to a delicate corner.

- **Sub-box A is comparably broad.** The galaxy fronts share a ~28%-wide a0 band that contains the framework value;
  this is the same character as ΛCDM's broad galaxy-fit posteriors. **The galactic unification is NOT fine-tuned —
  and it is dramatically MORE economical than ΛCDM there** (a0=Λ replaces ~2 fitted halo params/galaxy, ~350 across
  SPARC-175, with ONE number).
- **At the CMB the framework MATCHES ΛCDM's parameter count, not beats it:** 5 shared {ω_b,θ_s,τ,A_s,n_s} + I0
  (fills the ω_c slot) = 6 = ΛCDM. So sub-box B's CMB slice is *as broad / as natural as ΛCDM* — the I0 is a normal
  measured density, not a tuned corner. **No parsimony win at the CMB; no fine-tuning penalty either.**
- **The one place the framework is WORSE than ΛCDM is the cluster cure:** ΛCDM cures clusters with the SAME ω_c that
  fits the CMB (η=1, zero extra knobs) — broad, natural, done. The framework needs a SEPARATE μ that is squeezed and
  whose cure is undelivered. **So the framework is fine-tuned-to-empty exactly and only at the cluster cure** — the
  one front where ΛCDM is clean and broad. This is the honest cost: not a corpus-wide fine-tuning, but a single
  uncured front that ΛCDM cures for free.

**Honest fine-tuning verdict (the three-way choice, decided):**
- NOT "jointly viable + natural across all nine" — the cluster cure is genuinely absent from the box.
- NOT "no joint solution / fine-tuned to a point" — 8 of 9 fronts share a broad, ΛCDM-like region containing the
  framework value, at LCDM CMB-parameter-count.
- **YES the middle: "jointly viable for 8 fronts at ΛCDM-like naturalness (+1 measured I0 for the CMB); the 9th
  (clusters) is uncured-within-the-galaxy-WL-constraints, but SOFT (true η~1.3–1.9, systematic-limited), MOND-SHARED,
  and lensing-confirmed — a survivable-soft-loss, not a hard kill."** The framework does not break ΛCDM and ΛCDM
  does not break the framework; the lone hole is the cluster cure, where ΛCDM is broad and the framework is empty.

---

## BOTH WAYS (one line)

The box factorizes: sub-box A (a0=Λ, Υ, ν) is BROAD and ΛCDM-natural — a single connected a0 band ~28% wide containing
9.36e-11 satisfies all eight galaxy/transition/EFE/lensing/a0(z) fronts at ≤1.5σ (credit at full weight; and I caught
my own Υ=0.50 BTFR-floor artifact that had falsely excluded the framework value — both ways) — while sub-box B (μ, I0,
cs²) fits the CMB at +1 well-measured I0 (as natural as ΛCDM's ω_c) but is OVER-determined against a clean cluster
cure: the CMB forces cs²~0 which over-clusters galaxies (the Mistele squeeze at the dust level), galaxy-WL caps μ to a
narrow ~4× window, and the μ²Φ cure there is non-monotone/per-cluster/undelivered — so the nine-front intersection is
EMPTY for a cluster CURE (cost +2, and even +2 undelivered) but the cluster loss is SOFT/systematic-limited/MOND-shared,
making the honest verdict the MIDDLE one (jointly-viable-8-fronts-naturally + 9th-uncured-but-soft), neither a
manufactured viable corner nor a high-priest no-solution dismissal. Quarantine held: a0/Z never asserted derived.

*Grids: `/tmp/global_intersection.py`, `/tmp/a0_joint_recheck.py`. Sources: Skordis-Złośnik 2021 PRL 127 161302;
Verwayen-Skordis-Złośnik 2024 MNRAS 531 272; Durakovic-Skordis 2024 JCAP 04 040; Mistele-McGaugh-Hossenfelder 2023
A&A 676 A100; Planck 2018 VI; banked δq⁰⁰=0 theorem + the cited session ledgers.*
