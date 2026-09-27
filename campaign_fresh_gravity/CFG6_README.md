# CFG6 — should a₀ follow the dark energy through cosmic time?

The core framework ties a₀ to the vacuum: a₀ = κ c √(G ρ_Λ), with κ = ½ **fitted** (equivalently Z = 5.7888). With a
true cosmological constant, a₀ is exactly flat in redshift. That flatness is the framework's distinctive prediction
against the rival law a₀ ∝ H(z). If the dark energy evolves, as DESI's fits hint, the natural extension is
a₀(z) ∝ √ρ_DE(z) (FP0 R3b). This lane decides whether and how that evolving branch belongs in the record's calculations.

**Founding principle (plain words).** a₀ is set by the vacuum's energy. When that energy is not constant, the principle
does not say which scalar of the dark-energy sector a₀ reads. This lane writes each reading down and asks three
things of it. Can it be put into an action with no new constant and no harm? What does it predict under the published
fits? What do the data say?

Scripts (each writes its own `.out` and `_results.json`, plus `_MUTATE` versions); run from the repository root:
- `CFG6_common.py`: shared machinery. It covers the footings, the DESI chains, the four readings, the thawing field,
  the two MOND kernels in two-field form, and the ΛCDM-native emergent scale.
- `CFG6_a0z_branches.py`: the branches, their actions and health, and their a₀(z) for z = 0–5 on both footings. Its
  main run also writes `CFG6_a0z_branches_thawgrid.json`, the thawing-field tracks (10⁻⁷ dex, z ≤ 3.5) that part 2
  reads. The MUTATE run does not write it, because the grid does not depend on the MUTATE switch.
- `CFG6_a0z_evidence.py`: the branches against the record's a₀(z) evidence. It also covers the erosion of the z ≈ 2.5
  test, the number of objects that separates the branches, and what changes elsewhere on the scorecard.

Nothing outside `campaign_fresh_gravity/CFG6_*` was written. **κ = ½ stays fitted; nothing here derives it. The theory
is not closed. The data do not favour the framework over ΛCDM.**

## The answer

1. **Branch A (the unimodular tie, XR20 T1 and XR30) remains the framework's prediction.**
   - a₀ reads the Henneaux–Teitelboim integration constant, so it is exactly flat for *any* dark-energy history.
   - It has a healthy action and adds no local mode.
   - It is what PAPER7 pre-registered: 0.00 dex at z ≈ 2.5.
2. **The evolving branch has one healthy realisation that adds no constant.** This is the density tie read as a
   *leaf average* on the khronon's CMC leaves: α² = κ²G⟨ρ_DE⟩_h.
   - The local realisations are unhealthy. The density tie is ill-posed and the pressure tie is a ghost (details below).
   - The potential tie √V (XR20) is healthy but reads V = (ρ − p)/2, not ρ.
3. **Under the DESI DR2 fits the branches move a₀(2.5) by −0.10 to +0.14 dex.**
   - Following the fits, which cross w = −1: B −0.098, C −0.034, D +0.030. The crossing needs a ghost or a braided dark
     energy.
   - A healthy thawing field conditioned on the posterior: B +0.027, C +0.035, D +0.045.
   - A thawing field matched only to each fit's w₀ rises more: +0.08 to +0.14.
4. **The data do not prefer any branch.**
   - The rising branches win only while the fork likelihood's drift prior is below the record's headline (up to
     +4.0 in log₁₀ B at P-MAG), and all of that comes from MUSE-DARK III.
   - Without MUSE-DARK III, every branch is within |log₁₀ B| ≤ 0.37 of flat.
   - RC100's slope leans against a rise, with its caveat.
5. **The z ≈ 2.5 test.** At 0.13 dex per object the flat law is 2.57σ from ΛCDM-native.
   - The density branch following DESI sharpens it to 3.22σ.
   - A healthy thawing field erodes it to 2.20–2.35σ (conditioned) or 1.48–1.93σ (w₀-matched).
   - Telling the branches apart needs 15 or more objects at 0.13 dex and a systematic floor well below 0.05 dex. That is
     not a near-term observable.
6. **Elsewhere, the evolving branch is negligible on every scorecard gate at z ≲ 0.5 and in the forest.** It matters in
   three places:
   - the z ≈ 2.5 flagship and its pre-registered statistic;
   - cosmic shear's thin alt-footing margin (for the pressure tie following DESI);
   - eRASS1's cluster η-trend, which a rising a₀ worsens.

## 1. Novelty, stated precisely

**Not new.** These are overlaps, reported honestly. None was re-read here, because nothing was downloaded.
- **The a₀–cosmology coincidence**, a₀ ≈ cH₀/2π ≈ c√(Λ/3)/2π:
  - Milgrom 1983;
  - Milgrom 1999 (Phys. Lett. A 253, 273), which ties a₀ to the de Sitter radius;
  - the review of Famaey & McGaugh 2012 (Living Rev. Relativ. 15, 10);
  - Milgrom 2020 (arXiv:2001.09729), on a₀ ∝ H versus a₀ ∝ √Λ and their time dependence.
- **a₀ tracking √ρ_DE for an evolving dark energy, and its Tully–Fisher test.** These are credited to Limbach, Psaltis &
  Özel 2008 (arXiv:0809.2790). This is the record's own mandatory-credit standing
  (`book/BOOK_AUDIT_LEDGER_2026-07.md`), and it is kept here.
- **a₀ and Λ in one field or action:**
  - Zhao 2007 (ApJ 671, L1);
  - Blanchet & Le Tiec 2009 (Phys. Rev. D 80, 023524): dipolar dark matter, with Λ ~ a₀²/c⁴;
  - Milgrom 2009 (Phys. Rev. D 80, 123536): BIMOND;
  - Zhao & Li 2010 (ApJ 712, 130): the "dark fluid".
- **a₀'s epoch dependence at the action level:** Bekenstein & Sagi 2008 (Phys. Rev. D 77, 103512), in TeVeS.
- **The unimodular Λ** (Henneaux & Teitelboim 1989). The *tie* of a₀ to it is XR20's step; XR30's search found no prior
  paper.
- **The phantom-divide no-go** for a single minimally coupled field (Vikman 2005, Phys. Rev. D 71, 023515), and stable
  crossing with kinetic braiding (Deffayet, Pujolàs, Sawicki & Vikman 2010, JCAP 10, 026).
- **The ΛCDM-native emergent scale** (Kaplinghat & Turner 2002; Mayer et al. 2023), as the record uses it.

**New, to the best of my knowledge.** No literature search was run in this lane.
- (a) **The κ = ½ form tied to the evolving density:** a₀(z) = ½ c √(G ρ_DE(z)), equivalently a₀ = c H_DE(z)/Z with
  Z = 5.7888. That is, the framework's own normalisation carried into the evolving law.
- (b) **Its predictions under the current dark-energy fits.** These are the DESI DR2 + CMB + {Pantheon+, Union3, DESY5}
  chains propagated for z = 0–5 on both footings (L273/L275 for two readings; this lane for all of them, including
  healthy fields).
- (c) **The reading split and its health.**
  - A field tie reads V = (ρ − p)/2 (XR20).
  - The local derivative ties for ρ and −p fail health (B3).
  - The leaf-averaged ties are healthy and add no field or constant (B4).
- (d) **A healthy dark energy conditioned on DESI's posterior** moves a₀(2.5) by only +0.01 to +0.05 dex.
- (e) **The erosion and sharpening of the z ≈ 2.5 test, and the object counts.**

The campaign treats √ρ_DE as a framework result to develop. The record's mandatory credit to Limbach, Psaltis & Özel
2008 for the scaling is kept; what is the framework's own is items (a) to (e).

## 2. The branches

| branch | a₀(z)/a₀(0) | field content | constants | action? | ghost or crossing? |
|---|---|---|---|---|---|
| **A** unimodular | 1, exactly (a₀ reads Λ₀ of HT) | the HT 3-form multiplier: 1 global DOF, 0 local | κ (fitted) + Λ (measured); with an evolving DE component, also the HT share of today's DE (one choice, which moves κ's fitted value, not the flat law) | **yes, healthy** (XR20 T1, XR30) | none: flat for any dark-energy history |
| **B** density | √(ρ_DE(z)/ρ_DE(0)) | none new if leaf-averaged; one derivative coupling if local | κ + the DE history | **leaf-averaged α² = κ²G⟨ρ_DE⟩_h: yes, healthy (B4).** Local α(φ, X): ill-posed for 1 + w ≳ 0.05 (B3b) | following the CPL fits: a ghost or braided DE past z_cross; healthy DE: a thawing field, rising |
| **C** potential | √(V(z)/V(0)), V = (ρ − p)/2 | none beyond the DE scalar (α(φ)) | κ + the DE history | **yes, local, healthy** (XR20 E7; B3d) | as B |
| **D** pressure | √(p(z)/p(0)); stage-17's own law is flat to < 1% for z ≤ 5 | none new if leaf-averaged; stage-17's form sits in the v9 sector, which the record has closed | κ + the DE history | leaf-averaged: yes. Local α(φ, X), and the stage-17 form: **a ghost within 558–722 AU of every solar-mass star** (B3a) | following the fits: a ghost; with a w = −1 vacuum: flat (= A) |

**Why the local density and pressure ties fail (B1–B3, sympy plus both kernels).** A tie α² = κ²GΦ with
Φ = uρ + v(−p) reads (u + v)V + (u − v)X for a canonical field.
- So B and D need the kinetic scalar X. On FRW they are exact, but they are derivative couplings.
- On a static MOND background, FP7's MOND term −(1/8πG)A J(Y/A) makes the dark-energy field a k-essence with:
  - P_X = 1 + b εF;
  - P_XX = −b² ε s²J″/Φ;
  - where ε = κ²/8π and b = u − v.
- Waves transverse to the MOND field decouple at *any* inertia of the MOND scalar.

The consequences:
- **D (b = −1).** 1 − εF < 0 from y = 204 / 139 (J_P2, canonical / alt) and 144 / 101 (ν_mono). That is a ghost
  within 558–722 AU of every solar-mass star, which covers the whole Solar System.
  - Stage-17's promotion a₀² ∝ −K(Q) has this structure if it is coupled to this MOND term. Its K″ term flips with
    1 − εF; the charge suppression covers only K′.
  - This answers stage 17's "owed" no-ghost check (its F2) against it, for this coupling.
- **B (b = +1).** c_s² < 0 for transverse modes once ε(1+w)s²J″ > 1 + εF.
  - For DESI-like 1 + w = 0.16–0.33 that happens at y > 15–26 (J_P2) and y > 34–142 (ν_mono).
  - ν_mono's threshold on 1 + w is 0.054 at 1 AU and 0.042 at the Sun's surface.
  - The longitudinal mode is stable on FP14's λ = 0 root.
- **C (b = 0).** No derivative coupling. The mass term is positive for an exponential V, because s²J″ ≥ F at every
  y (10⁻³ to 10¹³).
- **The leaf average (B4).** With α² = κ²G⟨Φ⟩_h:
  - every site sees the kinetic coefficient 1 + b⟨εF⟩;
  - the cross terms fall as 1/N;
  - today ⟨εF⟩ ≈ 2.4×10⁻⁹ (an order-of-magnitude estimate).

  No local derivative coupling survives. The price is the khronon's preferred foliation, which the chain already
  has; the same kind of term appears in FP14's ⟨K⟩_h.

**The crossing (B5).** 99.8–100% of every combination's posterior crosses w = −1 inside 0 < z < 2.5, at a median
z_cross of 0.36–0.44. A minimally coupled single field cannot follow the fits past that point.

## 3. Predictions under the DESI DR2 fits

The fits are DESI DR2 BAO + CMB + SNe w₀wₐCDM (DESI Collaboration 2025, arXiv:2503.14738):
- DESY5 (−0.752, −0.86), with DES-SN5YR (arXiv:2401.02929);
- Pantheon+ (−0.838, −0.62), with Scolnic et al. 2022 and Brout et al. 2022;
- Union3 (−0.667, −1.09), with Rubin et al. 2023 (arXiv:2311.12098).

Uncertainties are propagated through the public chains (L275's thinned copies). Values are in dex, as median [16, 84]
on DESY5 (`CFG6_a0z_branches.out` P; Pantheon+/Union3 are in the JSON). **z > 2.5 extrapolates fits constrained at
z ≲ 2.3.**

| branch | z = 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 5.0 |
|---|---|---|---|---|---|---|---|
| A (unimodular) | 0 | 0 | 0 | 0 | **0.000** | 0 | 0 |
| B-CPL (density, follows the fits) | +0.025 [+0.018,+0.032] | +0.004 | −0.029 | −0.064 | **−0.098 [−0.140,−0.060]** | −0.131 | −0.245 |
| C-CPL (√V) | +0.058 [+0.044,+0.072] | +0.051 | +0.027 | −0.003 | **−0.034 [−0.063,−0.007]** | −0.064 | −0.171 |
| D-CPL (pressure) | +0.095 [+0.072,+0.120] | +0.101 | +0.084 | +0.058 | **+0.030 [+0.007,+0.053]** | +0.002 | −0.100 |
| B-thaw(post) (healthy, posterior-conditioned) | +0.017 | +0.022 | +0.025 | +0.026 | **+0.027 [+0.016,+0.042]** | +0.027 | +0.027 |
| C-thaw(post) | +0.021 | +0.030 | +0.033 | +0.035 | **+0.035 [+0.022,+0.056]** | +0.036 | +0.037 |
| D-thaw(post) | +0.026 | +0.037 | +0.042 | +0.044 | **+0.045 [+0.028,+0.072]** | +0.046 | +0.046 |
| B-thaw(w₀) (healthy, w₀-matched) | +0.050 | +0.069 | +0.077 | +0.081 | **+0.084 [+0.063,+0.107]** | +0.085 | +0.087 |
| C-thaw(w₀) | +0.064 | +0.090 | +0.101 | +0.107 | **+0.110 [+0.083,+0.140]** | +0.112 | +0.115 |
| D-thaw(w₀) | +0.080 | +0.114 | +0.130 | +0.137 | **+0.141 [+0.106,+0.181]** | +0.144 | +0.147 |
| rival H(z) | +0.133 | +0.256 | +0.373 | +0.480 | +0.575 | +0.659 | +0.920 |
| ΛCDM-native (L274, range) | +0.033 | +0.091 | +0.165 | +0.248 | +0.334 [+0.210,+0.450] | +0.419 | +0.726 |

**The healthy field conditioned on the posterior (P3).** The best thawing node on DESY5 is λ = 0.90, with CPL
equivalents (w₀, wₐ) = (−0.884, −0.161). Its χ²-proxy is 12.0, against 19.8 for Λ. It rises only 20–32% as much as the
w₀-matched field (reported H6 miss; its prediction was 30–60%).

**Both footings, absolute a₀(z) in 10⁻¹¹ m s⁻² (DESY5 medians):**

| footing | branch | z = 0 | 1.0 | 2.5 | 5.0 |
|---|---|---|---|---|---|
| canonical | A | 9.360 | 9.360 | 9.360 | 9.360 |
| canonical | B-CPL / C-CPL / D-CPL | 9.360 | 9.439 / 10.530 / 11.823 | 7.467 / 8.663 / 10.029 | 5.329 / 6.314 / 7.429 |
| canonical | C-thaw(post) / C-thaw(w₀) | 9.360 | 10.019 / 11.508 | 10.156 / 12.067 | 10.185 / 12.192 |
| alt | A | 11.312 | 11.312 | 11.312 | 11.312 |
| alt | B-CPL / C-CPL / D-CPL | 11.312 | 11.407 / 12.726 / 14.288 | 9.024 / 10.469 / 12.120 | 6.440 / 7.630 / 8.978 |
| alt | C-thaw(post) / C-thaw(w₀) | 11.312 | 12.108 / 13.907 | 12.274 / 14.583 | 12.308 / 14.734 |

**The z = 0 normalisation (P5).** Holding κ = ½, the DESI cosmologies move today's a₀ by −0.0055 (DESY5), +0.0019
(Pantheon+) and −0.0136 (Union3) dex. Holding a₀(0) instead, κ refits to 0.506 / 0.498 / 0.516. This is a
normalisation, not a redshift dependence, and it is well inside κ's measurement error (0.465 ± 0.076).

## 4. Against the record's a₀(z) evidence

**The fork likelihood** (`prep_2026/a0z_crossscale/a0z_fork_likelihood_2026.py`) was re-run with its committed head
executed read-only, so every branch gets the identical lever and drift nuisance. The table gives the largest
|log₁₀ B| of any dark-energy branch against A (E1):

| subset | face | P-HALF | P-MAG | P-MSA (headline) | P-WIDE |
|---|---|---|---|---|---|
| all 10 | +39.6 | +18.5 | +4.02 | −1.42 (B-CPL) | −0.29 |
| without MUSE-DARK III | −0.37 | −0.31 | −0.24 | −0.19 | −0.21 |
| clean near-a₀ (Jeanneau, Tiley, Big Wheel, McGaugh, Milgrom) | −0.14 | −0.20 | −0.27 | −0.30 | −0.33 |

The rising branches are favoured only by MUSE-DARK III's apparent rise, and only below the record's headline drift
prior. Otherwise every branch is indistinguishable from flat. On the clean subset the rival H(z) loses at 1.45–2.15 in
log₁₀ B, and ΛCDM-native at 0.45–0.85 (both footings).

**The other data (E2–E5, DESY5):**

| branch | RC100 slope (pull; observed −0.112 ± 0.063) | Jeanneau refit pull | bTFR max pull | MUSE gap at z = 1 |
|---|---|---|---|---|
| A | 0.000 (−1.80) | +0.51 | 1.25 | +0.377 |
| B-CPL | −0.068 (−0.71) | +0.51 | 1.24 | +0.374 |
| C-CPL | −0.054 (−0.93) | +0.65 | 1.21 | +0.327 |
| D-CPL | −0.043 (−1.11) | +0.79 | 1.18 | +0.278 |
| B/C/D-thaw(post) | +0.004 to +0.007 (−1.85 to −1.91) | +0.58 to +0.62 | 1.23 | +0.34 to +0.35 |
| B/C/D-thaw(w₀) | +0.012 to +0.022 (−1.99 to −2.15) | +0.70 to +0.83 | 1.18–1.21 | +0.27 to +0.31 |
| rival H(z) | +0.220 (−5.32) | +1.27 | 1.10 | +0.121 |
| ΛCDM-native (exact DM14) | +0.157 (−4.31) | +0.79 | 1.20 | +0.286 |

**Which branch do the data prefer? None.**
- RC100 is the one datum with power. It leans toward the declining density branch and against a rise. Its caveat
  stands: the trend is a restatement of RC100's falling f_DM, it has uncontrolled selection, and it detects no decline.
- The pre-declared H9 expectations (thawing at 2.5–3σ; |log₁₀ B| ≤ 0.5 under P-MAG) missed, and are kept as run.
  The thawing branches pull 2.0–2.2σ, and MUSE-DARK III drives P-MAG to +4.0.
- No branch reaches MUSE-DARK III. The record's reading of MUSE-DARK III as an apparent a₀ stands.

**The environment null (C7, E9).** This is BIG-SPARC's question on the public 175-galaxy SPARC
(`real_research/reviews/A0_COSMICWEB_ENVIRONMENT_2026-06.md`).
- The measured slopes d log a₀/d log(1+δ) are +0.052 ± 0.043 (2MRS) and −0.046 ± 0.081 (2M++). The ρ_local reading
  is excluded at 10.4σ and 6.7σ.
- Every branch reads a spatially uniform density: A exactly, the local √V tie ≤ 10⁻¹¹ (XR20 E6), the leaf-averaged ties
  0 in space. All pass within 1.2σ.
- The evolving branches change a₀ in time, never in space.

## 5. The z ≈ 2.5 test: erosion, sharpening, and how many objects

**Separation from ΛCDM-native (+0.334) (E6).** The per-object precisions are PAPER7's requirement (0.13) and the IFU
forecast's (0.215 / 0.257 / 0.431 dex). The branch's own band is included.

| branch | a₀(2.5) | 0.13 | 0.215 | 0.257 | 0.431 | + M*'s flagship residue (XR17, at 0.13) | factor vs A |
|---|---|---|---|---|---|---|---|
| A | 0.000 | **2.57σ** | 1.55 | 1.30 | 0.77 | 1.60–1.76σ | 1.00 |
| B-CPL | −0.101 | **3.22σ** | 1.99 | 1.67 | 1.00 | 2.29–2.44σ | 1.25 (sharpens) |
| C-CPL | −0.036 | 2.79σ | 1.71 | 1.43 | 0.86 | 1.84–2.00σ | 1.09 |
| D-CPL | +0.027 | 2.33σ | 1.42 | 1.19 | 0.71 | 1.38–1.53σ | 0.91 (erodes) |
| C-thaw(post) | +0.035 | 2.28σ | 1.38 | 1.16 | 0.69 | 1.32–1.47σ | 0.89 |
| C-thaw(w₀) | +0.106 | 1.72σ | 1.05 | 0.88 | 0.53 | 0.77–0.92σ | 0.67 |
| D-thaw(w₀) | +0.136 | 1.48σ | 0.91 | 0.76 | 0.46 | 0.54–0.69σ | 0.57 |

**Erosion or sharpening.**
- Following the DESI fits, the density and potential ties sharpen the test and the pressure tie erodes it slightly.
- A healthy field fitted to the data erodes it by ~10%.
- The w₀-matched healthy fields erode it by 25–43%.
- M*'s carrier residue (+0.106 to +0.126 dex, XR17) costs more than any dark-energy branch. With it added to the
  w₀-matched thawing field, the separation falls below 1σ (H10 as declared).

**How many objects for 3σ at z = 2.5 (E7):**

| comparison | 0.13 dex | 0.257 (IFU + CO gas) | 0.431 (IFU only) | with a 0.05 dex coherent floor |
|---|---|---|---|---|
| A vs ΛCDM-native | **1.4** | 5.3 | 15 | 1.7 / 6.7 / 19 |
| A vs B-CPL | 15 | 59 | 165 | impossible (the 0.10 dex difference is < 3 × 0.05) |
| A vs C-thaw(post) | 122 | 477 | 1341 | impossible |
| A vs C-thaw(w₀) | 13 | 53 | 148 | impossible |
| A vs D-CPL (best at z ≈ 1) | 16 at z = 1 | 62 | 173 | impossible; and D-CPL is degenerate with ΛCDM-native at z ≈ 1 |

The z ≈ 1–2.5 rotators can tell *the flat family* from ΛCDM with a few objects. Telling the dark-energy branches from
one another needs 15 to more than 100 objects, and systematics controlled below ~0.03 dex. The pre-declared H11
missed only on B-CPL vs ΛCDM (0.8 objects, below its 2–6).

## 6. What changes elsewhere if a branch other than A holds

Each gate is sized at its own epoch by the committed canonical/alt pair, which is a +0.0823 dex shift in a₀ (E8,
DESY5 medians):

| gate (epoch) | lever | largest change over the branches | margin | verdict |
|---|---|---|---|---|
| KiDS-1000 (z ≈ 0.25) | +36.7 Δχ²/dex (DE10) | +2.4 (D-CPL) | 30.3 (M*'s worst −26.28 vs +4) | negligible |
| Cosmic shear (z = 0.5) | +0.91 R/dex (MS4) | +0.084 (D-CPL): alt 1.124 → **1.208** | 1.2 − R = 0.151 / 0.076 | **D-CPL crosses 1.2 on the alt footing** (lever estimate); all others inside |
| Lyman-α forest (z = 2–3) | ×6.9/dex (DE11) | 0.0053 | line 0.10 | negligible (≥ 18× inside) |
| Flat-a₀ flagship, prediction (z = 2.5) | direct | −0.101 (B-CPL) … +0.136 (D-thaw(w₀)) | tolerance ±0.10 dex | **matters**: B-CPL and the w₀-matched thawing fields reach the tolerance; the posterior-conditioned fields do not (+0.03 to +0.05) |
| Flagship edge, M*'s cell (z = 2.5, 10¹¹ M☉) | Δlog(r_e/r_F) = ¾Δlog a₀ − 2Δlog E (+½Δlog ρ_DE if the gate reads ρ_DE) | −0.168 (B-CPL, ρ_DE-reading gate) | log(r_e/r_F) = 0.50 / 0.56 | passes |
| Clusters: eRASS1 η trend (z = 0–1) | d ln ν/d ln a₀ = 0.35 at y = 0.33–0.58 | −0.037 per unit z (D-thaw(w₀)) | observed +0.187 ± 0.013 (flat requires 0) | a rising a₀ adds up to 2.9σ(stat) to an existing tension; the record's selection caveats apply |
| Harvey (z ≈ 0.3) | none committed | Δlog a₀(0.3) up to +0.074 | knife-edge 0.096 vs 0.10 | **not sized** |
| z ≈ 0 gates (SPARC RAR, wide binaries, Solar System, EFE dwarfs, LG, Coma at z = 0.023) | direct | ≤ 0.009 dex | lever 0.082 | negligible |
| CMB lensing (FP22, undecided) | +0.68 ACT amplitude/dex × f_eff 0.14–0.26 | ≤ +0.022 | FP22's verdict (linear pass, ACT halofit ≥ 3.8σ fail) | unchanged |
| RC100 RAR carrier gate (L391) | — | the carrier's shift is untouched; a₀(z) enters the RAR prediction itself (§4) | — | unchanged |

The pre-declared H12 missed on one count, kept as run: D-CPL moves a₀(0.5) by 0.092 dex, above the 0.0823 lever. The
flagship range came out as declared (−0.101 to +0.136 against −0.10 to +0.16).

## 7. Recommendation

**Keep A as the framework's prediction.** Branch A (flat, the unimodular tie) is exact, dark-energy-agnostic, healthy
and pre-registered.

**Carry the evolving branch as one labelled variant, B-leaf.** B-leaf is the density tie a₀ = ½ c √(G⟨ρ_DE⟩_h), read on
the khronon's leaves.
- **What it adds.** It adds no constant beyond κ and the measured dark-energy history, and it is the only healthy
  realisation of √ρ_DE.
- **How to quote it.** Quote it as a band next to A's 0.00. At z = 2.5 the band is [−0.14, +0.04] dex: B following
  DESI's fits (which needs crossing physics) to a healthy field conditioned on DESI.
- **Where it belongs:**
  - PAPER7's pre-registered statistic and any JWST/ALMA target forecast, as a stated systematic on the framework's
    value;
  - the high-z Tully–Fisher and rotation-curve confrontations;
  - the flagship gate, where its ±0.10 tolerance is comparable to the band;
  - the cosmic-shear gate on the alt footing, if the pressure reading is ever used.
- **Where to drop it.** KiDS, the forest, CMB lensing, SPARC, wide binaries, the Solar System, EFE, the Local Group and
  Coma. Its effect there is below every margin by 10× or more.
- **What not to use:**
  - the local α(φ, X) realisations of B and D (ill-posed and a ghost);
  - the w₀-matched thawing numbers as "the" healthy prediction. They overstate the rise 3–5×, relative to a field
    conditioned on the posterior.

**Reading notes for other owners (flagged, not edited):**
1. **XR20's "no local coupling realises √ρ_DE".** This holds for α(φ). α(φ, X) realises it exactly on FRW but is
   ill-posed for DESI-like w. The leaf average realises it healthily.
2. **Stage-17's pressure promotion**, if coupled to the chain's MOND term, is a ghost wherever εF > 1 (within ~560–720
   AU of every star). Separately, stage 17's docstring gives "z_t ∈ [18, 36]", which is 1 + z_t; its code prints
   [16.8, 35.0].
3. **XR20's healthy thawing bracket (+0.07 to +0.16 at z = 2.5)** is w₀-matched. Conditioned on the posterior it is
   +0.015 to +0.035 (C).

## Checks

| script | main | MUTATE |
|---|---|---|
| `CFG6_a0z_branches.py` | 22/23, 0 load-bearing failures, **rc = 0**. FAIL: P2 = H6 (reported) | 21/23, **rc = 1**. HEADLINE-FLAT fails: A reads ρ_total, giving +0.576 dex at z = 2.5 |
| `CFG6_a0z_evidence.py` | 14/18, 0 load-bearing failures, **rc = 0**. FAILs: E1 = H9, E2 = H9, E7 = H11, E8 = H12 (all reported, kept as run) | 10/18, **rc = 1**. C1b (A ≠ M-FLAT: face χ² 13.08 vs 233.89) and HEADLINE fail |

**Controls, reproduced exactly:**
- **C1.** FP0 R3b's 0.7956404957595.
- **C2.** XR20's E2 table (63 numbers: three fits × seven redshifts × three readings, diff 0), including +0.051 at z = 1
  and −0.034 at z = 2.5 on DESY5.
- **C3.** L275's 72 chain bands (diff 0).
- **C4.** L273's Gaussian pressure bands and PAPER7 v2's printed strings, with L273's RNG sequence replayed.
- **C5.** XR20's thawing tracks (1.1×10⁻¹⁵).
- **C6.** Stage-17's derived law: flat to 3.6×10⁻⁴ for z ≤ 5. Its window [2.14×10⁻⁵, 1.77×10⁻⁴], its z_t [16.8, 35.0]
  and its off-switch 0.0021–0.006 are equal to what stage 17's committed code prints (run read-only), and PAPER7's
  "within 1% of flat for z ≤ 5" was located.
- **C7.** PAPER7's ΛCDM factors 1.23 / 1.76 / 2.13 / 2.82 and L274's +0.334.
- **C8.** FP0's footings.

In part 2:
- the fork likelihood's face χ² 302.086 / 15.455 / 233.886 and all of its marginalised Bayes factors (2.8×10⁻¹⁴);
- h16's "−0.1123 ± 0.0625 (N = 99)" line verbatim;
- the Jeanneau refit's 0.51σ;
- L276's max-pull line verbatim;
- XR17's residues, the IFU σ's, and the environment slopes.

## Pre-declaration and disclosures

**Hypotheses.** H1–H12 were written to a timestamped scratch file (2026-09-27T16:03Z) before any code of this lane
ran, from hand algebra, and were copied verbatim into the docstrings. H1's "z_t ∈ [18, 36]" came from stage 17's
docstring, which is 1 + z_t (reading note 2).

**Development probes** (scratch, outside the repository; none are kept):
1. The thawing solver's speed.
2. The kernel identities F = 2H − yh, s²J″ = (h/2)(h/h′ − y), J′ + 2sJ″ = 1/h′, checked against J_P2's closed form to
   40 digits.
3. The B2 sympy blocks, plus a deliberate wrong-sign test showing that the B2a identity check has teeth (residual 2.0).
4. The existence of thawing solutions at steep λ.
5. A read-only run of stage 17.

**`CFG6_a0z_branches.py` debug runs** (all MUTATE; each wrote the lane's own paths):
1. Crashed at B4: sympy differentiated with respect to an expression. C6 also failed, because the pre-declared z_t
   range was the docstring's 1 + z_t. C6 now compares against the numbers stage 17's code prints. This was the only
   check whose reference changed.
2. Crashed building the thawing grid: λ > 2 has no solution at low Ω_m. The grid was capped at λ = 2.0, which covers
   every chain sample.
3. Completed. The Λ reference χ² in P3 was then put on the same 3-d proxy as the thawing nodes (a printed number only).
   The thawing interpolator was moved into `CFG6_common.py` so that both scripts share it.

The ordered pair was then run, and re-run after `sys.dont_write_bytecode` was added. Outputs were unchanged. It was run
once more after the thawing tracks were moved out of the 6 MB results JSON into the compact companion file (rounded to
10⁻⁷ dex). In part 2 the only printed change was in three near-degenerate object counts of ~10⁴ (C-thaw(w₀) vs ΛCDM at
z = 1), which moved in their fifth digit.

**`CFG6_a0z_evidence.py` debug runs:**
1. MUTATE crashed at C6 on a JSON key.
2. MUTATE and main completed.

Before the next pair:
- the ledger line and the verdict, which had been pre-written as "no branch at > 20:1", were made data-driven (the
  computed maximum is 4.0, from MUSE-DARK III);
- "keep or sharpen" was corrected (D erodes).

After that pair, and before the final one:
- C7 and E9 (the environment null) were added at the campaign's request to build on that null, and C7's fork distance
  was restricted to the two density axes.

**Determinism.** Both main scripts were re-run after the final pair. The .out and JSON are identical apart from
timing lines.

## How it is computed

- **CPL readings.** Closed forms, per chain sample. The bands are L275's weighted percentiles.
- **Thawing field.** XR20's Copeland–Liddle–Wands system (dust + field, frozen at z = 30) on a grid of 13 Ω_m × 41 λ.
  - *w₀-matched*: interpolated per posterior sample.
  - *posterior-conditioned*: each node's least-squares CPL equivalent over z ≤ 2.5, weighted by a 3-d Gaussian of the
    chain in (w₀, wₐ, Ω_m), with flat priors on the grid.
- **Health.** Flat space, frozen coefficients, gravity decoupled: the high-k question. The dispersion relation comes
  from sympy Euler–Lagrange on plane waves. The kernels are J_P2 (closed form) and ν_mono, reconstructed from its
  phantom law in mpmath at 40 digits.
- **Evidence.** The fork likelihood's own code (its head executed read-only) with the branches registered as models.
  - The dark-energy uncertainty is marginalised over 200 (CPL) or 150 (w₀-matched) chain draws per combination, and
    over node weights for the posterior-conditioned fields.
  - The alt footing uses y_alt = y a₀,can/a₀,alt in the lever.
- **Gates.** Linear responses from committed canonical/alt pairs, at each gate's epoch.

## Said plainly

- κ = ½ is fitted, not derived. The √Λ (or √ρ_DE) power is dimensional. Every tie here is a tie, not a derivation.
- **Scope of the health analysis.** It is a UV analysis on frozen backgrounds. It does not include the khronon's own
  sector, the heat filter, or FP17's screening, which could change the Newtonian-regime F; they were not checked.
- **What the posterior-conditioned field is.** It is a projection through a Gaussian proxy, not a fit to the BAO, SNe
  and CMB likelihoods. Braided or non-minimally coupled dark energies, which can cross w = −1 stably, were not built.
- **What the gate sizes are.** They are lever estimates. The cosmic-shear crossing for D-CPL (1.208 against 1.2) flags a
  thin margin; it is not a computed failure.
- **What RC100 is.** It is a monotone restatement of RC100's falling dark-matter fractions: a constraint on a rise, not
  a detection of a decline.
- **Unchanged.** The dark mass is still required. The theory is not closed. Nothing in hand favours the framework over
  ΛCDM.

## Reproduction

From the repository root:
```
MUTATE=1 python3 campaign_fresh_gravity/CFG6_a0z_branches.py
python3 campaign_fresh_gravity/CFG6_a0z_branches.py
MUTATE=1 python3 campaign_fresh_gravity/CFG6_a0z_evidence.py
python3 campaign_fresh_gravity/CFG6_a0z_evidence.py
```
Part 1 takes about 50 s and part 2 about 15 s, on ≤ 2 threads. Part 2 reads part 1's main-run JSON, so run part 1
first.
