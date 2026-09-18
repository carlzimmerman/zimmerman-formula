# a₀(z) Confronted: MUSE-DARK III (2026) vs the Framework's Constant/Declining Reading

**C. Zimmerman, 2026-06-05.** *The first multi-point DIRECT measurement of the RAR acceleration scale's
redshift evolution now exists and postdates every a₀(z) file in this repo. It measures a strong **rise**.
This document confronts it honestly against the framework's **canonical** prediction (a₀ constant under
ΛCDM, mildly declining under DESI), resolves a long-standing internal inconsistency about which branch is
"the prediction," retracts a prior overclaim, and grades the result. Numbers are recomputed in
[`reviews/project_a0z_MUSE_DARK_III_confrontation.py`](reviews/project_a0z_MUSE_DARK_III_confrontation.py);
all paper values were verified against the primary sources on 2026-06-05 (re-verified verbatim), not memory.*

---

## TL;DR (the grade)

**MIXED / METHOD-SPLIT / NON-DIAGNOSTIC — not falsified, not confirmed, and not framework-distinctive.**
At face value the single most direct, multi-point a₀(z) measurement contradicts the canonical
constant/declining reading (~12–16σ on the slope/point; the authors quote ~30σ for a₁≠0), and the authors
*disown* the stellar-mass systematic that would reconcile it. But it does **not** falsify the reading,
because the rise is **method-localised** to exactly the regime where ΛCDM's *apparent* a₀ rises ~×3
(Magneticum), runs **"faster than H(z)"** (so it matches no cosmological a₀(z) law at all), and the **other
arm of the data — including the repo's *own* real KMOS³D/KROSS kinematics and the BTFR/massive-disk
literature — is flat/declining**, consistent with the canonical reading. It is no win either: the
framework's distinctive √ρ_DE *decline* is far below current detectability, "constancy" is equally
consistent with standard constant-a₀ MOND, and the repo's earlier "MUSE confirms our *rising* a₀" claim
stays **retracted** (that rise overshoots E(z), is ΛCDM-degenerate, and is the ρ_total footing-bug branch).

---

## 1. Which branch is the prediction? (resolving the repo's internal fork)

The framework writes **a₀ = (c/2)√(G ρ)**. Everything turns on which ρ — and the repo has been inconsistent:

| reading | ρ | a₀(z) | status |
|---|---|---|---|
| **CANONICAL** ("a₀ *is* dark energy") | ρ_Λ (dark energy only) | **CONSTANT** (ΛCDM); **DECLINES ~26% by z=3** (DESI w₀=−0.752, wₐ=−0.86) | the reading the coefficient-footing audit + memory endorse |
| footing-bug | ρ_total | a₀ = cH(z)/Z ∝ E(z) → **RISES ×3 by z=2** | the ρ_total conflation the audit flags; *not* canonical |

Several older files (`project_a0z_muse_test.py`, `A0Z_STATUS_CORRECTED.md`, `project03c_covariant_rising_a0.py`,
`a0_constant_vs_evolving_fork.py`, `a0_z_empirical_rigorous.py`) treat the **rising ρ_total branch** as "the
framework's distinctive prediction." Per `reviews/COEFFICIENT_FOOTING_AUDIT_2026-06.md` and the canonical
a₀=(c/2)√(G ρ_Λ) reading, **that is the wrong branch** — the same ρ_total/ρ_DE conflation that inflates
a₀(0), now in the time domain. The canonical, distinctive prediction is **constant-to-declining**.

So MUSE's rise is in tension with the *canonical* reading; it is the *sign* of the disfavoured ρ_total
branch — but even that branch undershoots (see §3), and it is the branch the repo's own audit calls a bug.

## 2. The data (verified verbatim 2026-06-05 against the primary sources)

- **MUSE-DARK III** — **B. I. Ciocan, N. F. Bouché, J. Fensch** et al. (Krajnović, Freundlich, Desmond,
  Famaey, Techi), **A&A 709, L16 (2026)**, [arXiv:2604.22613](https://arxiv.org/abs/2604.22613). 79
  star-forming galaxies (M\* > 10^8.8 M⊙), **0.33 < z < 1.44**, MUSE Hubble Ultra Deep Field, pressure-support
  (asymmetric-drift) corrected. *(First author is **Ciocan**, re-verified — not "Mercier"; Mercier led the
  earlier MUSE-DARK I/II.)*
  - Fit **a₀(z) = a₀(0) + a₁z**, with **a₀(0) = 1.0 ± 0.04**, **a₁ = +1.59 (+0.11/−0.10)** ×10⁻¹⁰ m/s² *(verbatim)*.
  - **a₀|z~1 = 2.38 (+0.12/−0.10)**; four quantile bins climb **~1.99 → 2.71**; intrinsic scatter ~0.17 dex.
  - Authors *(verbatim quotes)*: evolution detected **"at a ∼30σ level"**; **"Our measured a₀(z) is faster
    than that of H(z)"**; reconciling to a₀=1.2 at all z "would require systematically larger stellar masses,
    with offsets ranging from ∼+0.2 dex...to ∼+0.45 dex," which "are **not supported by independent
    consistency checks**"; "excluding measurements within the central 2 kpc...changes the inferred a₀ by
    **less than 10%**." Robust across DC14/NFW/Burkert halos.
  - **Note:** the "second study, 1.99→2.71" in the briefing is **not independent** — it is the *binned* form
    of this same measurement. There is **one** direct multi-point a₀(z) dataset, not two.
- **Magneticum** — Mayer, Teklu, Dolag, Remus, **MNRAS 518, 257 (2023)**,
  [arXiv:2206.04333](https://arxiv.org/abs/2206.04333). A **ΛCDM hydrodynamical simulation** — it has **no
  fundamental a₀**. Fitting a MOND RAR to its galaxies yields an **apparent** a₀ that **increases by a factor
  ~3 from z=0 to z≈2** (×2.3 endpoint in the journal version), "without requiring fundamental modifications to
  gravity." Framed as a MOND-vs-ΛCDM discriminant — and here ΛCDM produces the rise. *(The MUSE paper cites
  this as "a₀ grows by a factor of ~3 from z=0 to 2," calling it "slightly less than the factor of ~4
  increase inferred here.")*
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
- **Authors' headline:** the evolution is detected at **~30σ** (a₁≠0, from the full RAR likelihood; the
  *marginalised* a₁=1.59±0.105 is ~15σ — both real, the gap is full-likelihood vs binned-parameter error).

The stellar-mass escape hatch (+0.2→+0.45 dex M\*) that *would* flatten this is **disowned by the authors** —
so I do **not** invoke it as the framework's rescue. Even the disfavoured ρ_total (rising) branch undershoots:
MUSE rises **"faster than H(z)"** (E(z)) — at z~1, MUSE ×2.6 vs E(1)=1.79.

## 4. Is the rise fundamental or apparent? (the only legitimate rescue — and it cuts both ways)

The framework predicts a constant/declining **fundamental** a₀ (a vacuum/horizon scale). MUSE measures the
**fitted RAR** a₀ in real, assembling galaxies. **Mayer+2023 proves these are not the same object:** ΛCDM
with *no* fundamental a₀ produces a fitted a₀ rising ~×3 by z≈2, purely from baryon-fraction / galaxy-assembly
evolution. (MUSE infers ~×4 by z=2 — its own comparison calls Mayer's ×3 "slightly less than" its own ×4, i.e.
~a third steeper; consistent with extra high-z systematics on top of assembly.)

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

| reading | vs MUSE at face value | after method-split + degeneracy + systematics | overall |
|---|---|---|---|
| canonical **constant** (ΛCDM) | refuted ~15σ (slope), ~30σ (a₁≠0) | rescued by Mayer degeneracy; favoured by McGaugh/Milgrom **and the repo's own KMOS³D/KROSS**; rise is method-localised | **survives within systematics, non-distinctive** |
| canonical **declining** (DESI) | refuted ~16σ | same rescue; distinctive √ρ_DE signal too small for MUSE to test anyway | **survives, untested** |
| ρ_total **rising** ∝E(z) (footing-bug branch) | right *sign*, but undershoots ("faster than H(z)") + ΛCDM-degenerate | "confirmation" retracted | **NOT confirmed** |

**Net:** the a₀(z) front is, honestly, **non-diagnostic** for the framework right now — the evidence is
genuinely **split by method**, the one clear rise is ΛCDM-degenerate, and the constancy results are not
framework-distinctive. The canonical reading is **not falsified** (it sits with the BTFR/massive-disk arm and
the repo's own high-z kinematics), but it earns **no positive confirmation** (its distinctive √ρ_DE decline is
below detectability, and "constancy" is equally standard-MOND). The repo's "settled declining reading" is
defensible as *not-refuted*, but **"settled" overstates it** while MUSE stands. a₀(z) currently adjudicates
nothing for or against this framework.

**What would actually decide it:** one clean **deep-MOND** (g ≪ a₀) extended rotation curve at **z~3** measured
to a few percent — a regime where the assembly/apparent-a₀ contamination is minimised and a true fundamental
a₀(z) would show. MUSE's intermediate-z star-forming disks (often g ≳ a₀, assembly-active) are exactly the
regime where fitted ≠ fundamental. Until that measurement exists, a₀(z) does not adjudicate this framework.

## 6. Deeper dig — the split tracks *method*, systematics are bounded, data are clean

**The rise is method-localised.** The disagreement in the literature is not random scatter — it splits by
*method*, and the rise sits exactly in the arm where ΛCDM's apparent a₀ is expected to inflate:

| method / regime | a₀(z) trend | sources |
|---|---|---|
| **RAR-fit on intermediate-z star-forming disks** | **rises** | MUSE-DARK III (×4 by z=2); Vărăşteanu+25 ([2504.20857](https://arxiv.org/abs/2504.20857), MIGHTEE-HI, tentative **2.4σ**) |
| ↳ *= the regime Mayer's ΛCDM apparent-a₀ inflates* | *(contaminated)* | baryon-fraction / galaxy-assembly structure |
| BTFR / outer-disk / massive-disk | flat / declining | McGaugh+24 (no evol.); Milgrom 2017 (excl. ~4×a₀) |
| **repo's *own* real high-z kinematics** | flat / declining | KMOS³D (Übler+17) + KROSS (Harrison+17) loaders (per `INTEGRITY_AUDIT.md`) |
| direct high-z disks | a₀_eff ≈ local | Big Wheel z=3.25 ([2409.17956](https://arxiv.org/abs/2409.17956)); RC100; Genzel |

The constancy arm is **substantial and includes the repo's own real data**. The rise is confined to RAR-fits
on star-forming disks — precisely where *fitted a₀ ≠ fundamental a₀* (Magneticum).

**Systematics, now bounded (from the MUSE paper itself, re-verified):**
- **Beam smearing / resolution** — excluding r<2 kpc shifts a₀ by **<10%** (verbatim). *Cannot* produce a ×2.6 rise. **Not the culprit.**
- **Pressure support (asymmetric drift)** — applied (Dalcanton & Stilp 2010) but **never quantified, no error budget**; high-z disks are hotter (larger, more uncertain v_AD), and the intrinsic scatter grows **0.13→0.19 dex** with z. **This is the live, uncontrolled systematic.**
- **Stellar mass / M\*L** — a +0.2→+0.45 dex shift would flatten to constant a₀, but the authors **disown it** ("not supported by independent consistency checks"). Not invoked as the framework's rescue.
- **3D forward modelling** — total and baryonic accelerations come from the *same* GalPaK³D disk–halo decomposition (model-dependent); v_c was cross-checked against the 2D CAMEL line-fit ("good agreement").

**Integrity clearance.** The repo's own 20-agent audit (`INTEGRITY_AUDIT.md`) grades the a₀(z) compilation
(SPARC 1.20, Vărăşteanu 1.69, MUSE 2.38) as **literature-values — attributed, not fabricated**; the single
"suspect" file is an unrelated units bug. This confrontation rests on real, cited numbers. *(One residual
caveat: I could not independently re-extract Vărăşteanu's a₀=1.69 at z≈0.05 from its abstract; the repo's own
fit code already flags the SPARC-1.20-vs-Vărăşteanu-1.69 near-local pair as an inter-method systematic that
deflates the evolution significance to ~2σ — i.e. it is treated skeptically, not as a clean detection.)*

---

*Supersedes the a₀(z) framing in `A0Z_STATUS_CORRECTED.md` and `project_a0z_muse_test.py` on **which branch is
canonical** and on the **"MUSE confirms the rise"** claim. Consistent with — and sharpens —
`project_a0z_reconciled.py` (the rise is real but ΛCDM-degenerate) and `DESI_AND_THE_A0Z_TEST.md` (the
declining √ρ_DE signal is too small for current data to test).*

---

## 7. Method audit (2026-09-18, from the letter's own text, arXiv:2604.22613 / A&A 709 L16)

**How the data were taken.** MUSE, the VLT integral-field spectrograph (1′×1′ field, 4750–9350 Å, R ≈ 3000), on the MUSE Hubble Ultra Deep Field survey: ESO programmes 094.A-0289, 095.A-0010, 096.A-0045 (the 3′×3′ mosaic and UDF-10, seeing-limited, ~0.6″) and 1101.A-0127 (the MXDF, the 140-h field taken with GALACSI ground-layer adaptive optics; the letter itself does not spell out which galaxies come from which field or quote a PSF). 79 star-forming galaxies, complete above M* > 10^8.8 M☉, 0.33 < z < 1.44, kinematics from whichever of [O II] λ3727, Hβ, [O III] λ5007, Hα is in the band, S/N 10 to >100. At z ≈ 1, 0.6″ is ≈ 5 kpc, comparable to the galaxies' sizes: the rotation curves are marginally resolved and everything rests on 3D forward modelling.

**How the accelerations were obtained.** GalPaK3D fits a 3D disc model, convolved with the PSF and line-spread function, directly to the cube (beam smearing handled by construction). The model is a disc–halo decomposition: stellar disc (+ bulge where present), a neutral-gas disc from a parametric constant-Σ_HI law (v ∝ √(Σ_HI r); HI is not observed at these redshifts), and a dark-matter halo (DC14 as baseline; NFW and Burkert tested). Stellar masses are *dynamically inferred inside that decomposition*, not fixed from photometry. Pressure support is corrected with Dalcanton & Stilp (2010), v_c² = v_⊥² + v_AD², with no error budget quoted. Both a_tot and a_bar are therefore outputs of one model fit.

**How a₀ was fitted.** RAR a_tot = a_bar/(1 − e^{−√(a_bar/a₀)}) with a₀ free; per quantile bin (four bins) and globally with a₀(z) = a₀(0) + a₁z: a₀(0) = 1.0 ± 0.04, a₁ = 1.59 ± 0.10 (×10⁻¹⁰). The local SPARC value 1.2 ± 0.26 enters only as a comparison, never as a prior. Appendix E repeats the exercise with MOND in the forward model and reports "similar results".

**What is wrong with reading it as a fundamental a₀ (in order of weight).**
1. *Circularity of the baryonic acceleration.* a_bar comes from a decomposition in which the stellar mass is a fitted dynamical parameter and the halo is a ΛCDM feedback profile (DC14) whose structure is tied to ΛCDM assembly. A rising fitted a₀ is exactly what Mayer et al. 2023 obtain by fitting the RAR to ΛCDM simulations with no a₀ at all (×3 by z = 2). The measurement is consistent with ΛCDM's *expectation for the apparent scale*; it does not isolate a fundamental one. In a MOND-type model a₀ and M* set the same amplitude and are degenerate, which is why the authors can say +0.2 to +0.45 dex in M* would flatten the trend.
2. *Gas is modelled, not measured.* At z ≈ 1 gas fractions are ~50%; a parametric constant-Σ_HI disc with no direct HI or CO measurement is a large, unquantified term in a_bar.
3. *Pressure support is corrected but not budgeted.* σ/v ≈ 0.3–0.5 at these redshifts makes v_AD² 10–25% of v_c²; the intrinsic scatter grows 0.13 → 0.19 dex with z, the signature of an unbudgeted term.
4. *Regime.* Compact star-forming discs at z ≈ 1 are probed at g ≳ a₀, where the fitted a₀ is set by the transition and is most sensitive to M*/L and gas systematics; the deep-MOND regime that would pin a fundamental scale is not sampled.
5. *Resolution.* Marginal (5 kpc at 0.6″ for the seeing-limited fields); the r < 2 kpc exclusion test (< 10% change) bounds but does not remove the dependence on the forward model.
6. *The z = 0 intercept is 1.0, below SPARC's 1.2 (0.08 dex),* an inter-method offset present already at z → 0.

**Net (unchanged from §5):** real data, honestly analysed, and *not diagnostic* of a fundamental a₀(z): the same method applied to a ΛCDM universe returns the same rise. It is not a confirmation of anything and not a refutation of the flat law; a robust rise in the deep-MOND, outer-disc regime (the BTFR arm, which currently reads flat) would be.
