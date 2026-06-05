# a₀(z) Confronted: MUSE-DARK III (2026) vs the Framework's Constant/Declining Reading

**C. Zimmerman, 2026-06-05.** *The first multi-point DIRECT measurement of the RAR acceleration scale's
redshift evolution now exists and postdates every a₀(z) file in this repo. It measures a strong **rise**.
This document confronts it honestly against the framework's **canonical** prediction (a₀ constant under
ΛCDM, mildly declining under DESI), resolves a long-standing internal inconsistency about which branch is
"the prediction," retracts a prior overclaim, and grades the result. Numbers are recomputed in
[`reviews/project_a0z_MUSE_DARK_III_confrontation.py`](reviews/project_a0z_MUSE_DARK_III_confrontation.py);
all paper values were verified against the primary sources on 2026-06-05, not quoted from memory.*

---

## TL;DR (the grade)

**WEAKENED & CONTESTED, leaning UNFAVOURABLE — not falsified, not confirmed.** The single most direct,
multi-point a₀(z) measurement contradicts the canonical constant/declining reading at face value (~12–16σ
on the slope/point, ~30σ on the authors' offset), and the authors *disown* the stellar-mass systematic that
would reconcile it. It is spared outright falsification only because the rise is **ΛCDM-degenerate** (a
ΛCDM sim with *no* fundamental a₀ produces the same apparent rise), runs **"faster than H(z)"** (so it
matches no cosmological a₀(z) coupling at all), and the broader high-z data are **split** (two other
analyses favour constant a₀). But that rescue is **double-edged**: it also makes the framework's a₀(z)
prediction non-distinctive, and it **retracts** the repo's earlier "MUSE confirms our rising a₀" claim.

---

## 1. Which branch is the prediction? (resolving the repo's internal fork)

The framework writes **a₀ = (c/2)√(G ρ)**. Everything turns on which ρ — and the repo has been inconsistent:

| reading | ρ | a₀(z) | status |
|---|---|---|---|
| **CANONICAL** ("a₀ *is* dark energy") | ρ_Λ (dark energy only) | **CONSTANT** (ΛCDM); **DECLINES ~26% by z=3** (DESI w₀=−0.752, wₐ=−0.86) | the reading the coefficient-footing audit + memory endorse |
| footing-bug | ρ_total | a₀ = cH(z)/Z ∝ E(z) → **RISES ×3 by z=2** | the ρ_total conflation the audit flags; *not* canonical |

Several older files (`project_a0z_muse_test.py`, `A0Z_STATUS_CORRECTED.md`, `project03c_covariant_rising_a0.py`,
`a0_constant_vs_evolving_fork.py`, `project_a0z_reconciled.py`, `a0_z_empirical_rigorous.py`) treat the
**rising ρ_total branch** as "the framework's distinctive prediction." Per
[`reviews/COEFFICIENT_FOOTING_AUDIT_2026-06.md`](reviews/COEFFICIENT_FOOTING_AUDIT_2026-06.md) and the
canonical a₀=(c/2)√(G ρ_Λ) reading, **that is the wrong branch** — it is the same ρ_total/ρ_DE conflation
that inflates a₀(0), now in the time domain. The canonical, distinctive prediction is **constant-to-declining**.

So MUSE's rise is in tension with the *canonical* reading; it is the *sign* of the disfavoured ρ_total
branch — but even that branch undershoots (see §3), and it is the branch the repo's own audit calls a bug.

## 2. The data (verified 2026-06-05 against the primary sources)

- **MUSE-DARK III** — Ciocan, Bouché, Fensch, Krajnović, Freundlich, Desmond, Famaey, Techi, **A&A 709, L16
  (2026)**, [arXiv:2604.22613](https://arxiv.org/abs/2604.22613). 79 star-forming galaxies (M\* > 10^8.8 M⊙),
  **0.33 < z < 1.44**, MUSE Hubble Ultra Deep Field, pressure-support (asymmetric-drift) corrected.
  - Fit **a₀(z) = a₀(0) + a₁z**, with **a₀(0) = 1.0 ± 0.04**, **a₁ = +1.59 (+0.11/−0.10)** ×10⁻¹⁰ m/s².
  - **a₀|z~1 = 2.38 (+0.12/−0.10)**; four quantile bins climb **~1.99 → 2.71**; intrinsic scatter ~0.17 dex.
  - Authors: evolution detected **"at a ~30σ level"**; **"our measured a₀(z) is faster than that of H(z)"**;
    reconciling to a₀=1.2 at all z "would require systematically larger stellar masses, with offsets ranging
    from ∼+0.2 dex to ∼+0.45 dex," which are **"not supported by independent consistency checks."** Robust
    across DC14/NFW/Burkert halos.
  - **Note:** the "second study, 1.99→2.71" in the briefing is **not independent** — it is the *binned* form
    of this same measurement. There is **one** direct multi-point a₀(z) dataset, not two.
- **Magneticum** — Mayer, Teklu, Dolag, Remus, **MNRAS 518, 257 (2023)**,
  [arXiv:2206.04333](https://arxiv.org/abs/2206.04333). A **ΛCDM hydrodynamical simulation** — it has **no
  fundamental a₀**. Fitting a MOND RAR to its galaxies yields an **apparent** a₀ that **"increase[s] by a
  factor ≃3 from z=0 to z=2.3"**, "without requiring fundamental modifications to gravity." Framed as a
  MOND-vs-ΛCDM discriminant — and here ΛCDM produces the rise.
- **The split** — McGaugh, Schombert, Lelli & Franck **2024** (ApJ 976, 13,
  [arXiv:2406.17930](https://arxiv.org/abs/2406.17930)): **"no clear sign of evolution"** in BTFR/DM-fraction
  to z~2.5 (favours **constant**). Milgrom **2017** ([arXiv:1703.06110](https://arxiv.org/abs/1703.06110)),
  the one direct high-z RC MOND analysis: **"all but exclude(s)"** ~4×a₀ at z~2 and the (1+z)^1.5 law
  (favours **constant**; bounds steep rises).

## 3. The tension, quantified (taking the measurement at face value)

Framework canonical a₀(z)/a₀(0), recomputed:

| z | LCDM (ρ_Λ const) | DESI w₀wₐ (ρ_DE) | MUSE 1+1.59z | [contrast] ρ_total E(z) |
|---|---|---|---|---|
| 0.5 | 1.00 | 1.06 | 1.79 | 1.32 |
| 1.0 | 1.00 | 1.01 | 2.59 | 1.79 |
| 2.0 | 1.00 | 0.86 | 4.18 | 3.03 |
| 3.0 | 1.00 | 0.74 | 5.77 | 4.57 |

The data **climb**; the canonical reading is **flat-to-declining** — opposite sign. In σ:

- **Slope test** (a₁ = +1.59 ± 0.105 ×10⁻¹⁰): vs ΛCDM (a₁=0) → **15.1σ**; vs DESI (effective a₁ ≈ −0.11) → **16.2σ**.
- **Point test** at z~1 (a₀|z~1 = 2.38 ± 0.11, normalised to MUSE's own a₀(0)=1.0): vs flat/declining → **12.5σ**.
- **Authors' headline:** the evolution is detected at **~30σ** (offset of intermediate-z a₀ above the local value).

The stellar-mass escape hatch (+0.2→+0.45 dex M\*) that *would* flatten this is **disowned by the authors** —
so I do **not** invoke it as the framework's rescue. Even the disfavoured ρ_total (rising) branch undershoots:
MUSE rises **"faster than H(z)"** (E(z)) — at z~1, MUSE ×2.6 vs E(1)=1.79.

## 4. Is the rise fundamental or apparent? (the only legitimate rescue — and it cuts both ways)

The framework predicts a constant/declining **fundamental** a₀ (a vacuum/horizon scale). MUSE measures the
**fitted RAR** a₀ in real, assembling galaxies. **Mayer+2023 proves these are not the same object:** ΛCDM
with *no* fundamental a₀ produces a fitted a₀ rising ~×3 to z=2.3, purely from baryon-fraction / galaxy-
assembly evolution. (MUSE extrapolated to z=2.3 is ~×4.7 — *steeper* than Mayer's ×3 and than E(2.3)=3.5,
i.e. it overshoots even the ΛCDM apparent rise, consistent with extra high-z systematics on top of assembly.)

**Consequence — stated honestly, both edges:**

- ✅ **Saves the canonical reading from outright falsification:** a rising *fitted* a₀ does **not** establish a
  rising *fundamental* a₀. Against a constant/declining fundamental a₀ + the standard assembly forward-model,
  MUSE is consistent to ~1–2σ, not 15σ. And "faster than H(z)" *cannot* come from any background-density law
  (ρ_Λ or ρ_DE), which actively points to an assembly/measurement origin rather than a cosmological a₀(z).
- ❌ **Destroys the prior "MUSE confirms our rising a₀=cH(z)/Z" claim** (`A0Z_STATUS_CORRECTED.md`,
  `project_a0z_muse_test.py`): that rise is ΛCDM-degenerate *and* overshoots E(z). **Retracted.**
- ❌ **Removes the framework's distinctiveness here:** if the observable is assembly-dominated, it is identical
  in ΛCDM and in the framework — a₀(z) stops being a place the framework can earn evidence.

## 5. Grade and net

| reading | vs MUSE at face value | after degeneracy/systematics | overall |
|---|---|---|---|
| canonical **constant** (ΛCDM) | refuted ~15σ (slope), ~30σ (offset) | rescued by Mayer degeneracy; *also* favoured by McGaugh/Milgrom | **WEAKENED, survives, non-distinctive** |
| canonical **declining** (DESI) | refuted ~16σ | same rescue; signal too small for MUSE to test anyway | **WEAKENED, survives, untested** |
| ρ_total **rising** ∝E(z) (footing-bug branch) | right *sign*, but undershoots ("faster than H(z)") + ΛCDM-degenerate | "confirmation" retracted | **NOT confirmed** |

**Net:** the a₀(z) front is, honestly, **empirically mute-to-unfavourable** for the framework right now. The
one direct measurement leans **against** the canonical reading; survival hinges on a degeneracy that also
strips distinctiveness; and the analyses that *do* favour constant a₀ (McGaugh, Milgrom) don't test the
framework's distinctive a₀↔H₀/Λ coefficient either. This neither kills the framework nor rescues it — it
**removes a₀(z) as a near-term source of support** and leaves the canonical reading on the back foot.

**What would actually decide it:** one clean **deep-MOND** (g ≪ a₀) extended rotation curve at **z~3** measured
to a few percent — a regime where the assembly/apparent-a₀ contamination is minimised and a true fundamental
a₀(z) would show. MUSE's intermediate-z star-forming disks (often g ≳ a₀, assembly-active) are exactly the
regime where fitted ≠ fundamental. Until that measurement exists, a₀(z) does not adjudicate this framework.

---

*Supersedes the a₀(z) framing in `A0Z_STATUS_CORRECTED.md` and `project_a0z_muse_test.py` on the question of
**which branch is canonical** and on the **"MUSE confirms the rise"** claim. Consistent with — and sharpens —
`project_a0z_reconciled.py` (the rise is real but ΛCDM-degenerate) and `DESI_AND_THE_A0Z_TEST.md` (the
declining √ρ_DE signal is too small for current data to test).*
