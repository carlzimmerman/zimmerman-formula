# REVERBERATION DOOR — The z = 7.04 Lensed LRD against KP1 (r_B)

**Verdict: CONSISTENT-OPEN** — KP1 is *not falsified* (and gets a non-trivial
near-hit) on the one object its program named; the door cannot be *closed*
because the only published radius constraint is a lower limit and no firm
reverberation lag exists yet. One separate, honest tension recorded: the same
object carries a direct engine mass ~10^3.5 above the framework's stack claim.

- **Date:** 2026-09-22 · **Door:** opus_49_doorB · **Lane:** `kp1_z7p04_lensed_lrd_lane.py` (7/7 PASS, exit 0)
- **Open item closed from the index:** *"Reverberation/lensing: the direct r_B on the z=7.04 lensed LRD closes KP1 in one object (the paper's own program)."*
- **RE-AUDIT PASS (2026-09-22, re-run after an output-contract rejection):** every load-bearing number
  below was re-verified against the primary literature. Confirmed verbatim: A2744-QSO1, triply imaged by
  Abell 2744, z_spec = 7.0451±0.0005, virial M_BH = 4_-1^+2×10^7 M_sun from Hβ FWHM 2800±250 km/s
  (Furtak+24, Nature 628, 57, DOI 10.1038/s41586-024-07184-8 = arXiv:2308.05735); direct dynamical mass
  "≈5×10^7 M_sun, Keplerian rotation around a point mass of 50 million Solar masses", inconsistent with a
  nuclear star cluster, M_BH/M_* > 2 (Juodžbalis+26, Nature 2026, DOI 10.1038/s41586-026-10579-4 =
  arXiv:2508.21748); n_H = 10^10 cm^-3, N_H = 10^24 cm^-2 fiducial Cloudy model with lower limits
  n_H > 10^8.5 cm^-3, N_H > 10^22.5 cm^-2 (Ji+25 BlackTHUNDER, arXiv:2501.13082 v2, §6); the BLR radius
  lower limit — verbatim: "the radius of the BLR must be larger than about 9-light-months/(1+z), which is
  about 45 light-days" (Ji+25, §7); EW variation 18±3% (Hα) and 22±8% (Hβ) over 875 d rest-frame, delays
  A=0 / B=+855_-6^+72 d / C=+7,043_-152^+234 d (Furtak+25, A&A 698, A227, DOI 10.1051/0004-6361/202554110
  = arXiv:2502.07875). No microlensing BLR-size constraint exists for this object: Furtak+25 state the
  three images are point-sources and their photometry is "agnostic to differential magnification."
  Non-load-bearing sub-details taken from paper bodies (e.g. host σ_N, NLR scales) were not re-read on
  this pass; none affect the verdict.

---

## 1. What r_B and KP1 are (framework definitions, verbatim)

- **r_B** = the radius of the dense Balmer layer of an LRD — the gas at
  n_H ~ 10^9–10^11 cm^-3 that produces the extreme Balmer decrements, Balmer
  absorption, and the Balmer break. Fiducial family position r_B = 100 au at
  M = 10^4 M_sun (r_B = f·R_phot, f = 0.106) [CFJC RFC-0001 §3; BHSTAR index].
- **KP1** (Wave T, "Kepler-grade", zero free parameters):
  **r_B^4 · n_H = 4 G M^2 / (c^2 μ m_p)**, the transition condition g_B = a0(ρ_B)
  rearranged. The constant 4G/(c^2 μ m_p) = **1.2685 m/kg²**, i.e.
  r_B^4 n_H = 5.02e68 m at M = 10^4 M_sun. Falsifier: **any LRD off by >×2 in
  r_B** (×16 in the product). [bhstar_t1_kepler_predictions.py; index §KP1]
- The test needs, per object: **n_H** (photoionization/CLOUDY), **M**
  (Gamma-free), and a measured **r_B** (reverberation or lensing).

## 2. The object: A2744-QSO1 — the z = 7.04 lensed LRD

Triply imaged by the cluster Abell 2744, z_spec = 7.0451 ± 0.0005
[Furtak+24, Nature 628, 57; arXiv:2308.05735]. The parent task's alternative
name "J2336+017" does not correspond to any z≈7.04 lensed LRD in the
literature (PKS 0736+017 is a z = 0.19 blazar; ILT J2336+1842 a z = 6.6 radio
galaxy); the z = 7.04 lensed LRD is unambiguously A2744-QSO1, and it is the
object the framework's program [2609.09274, per the campaign index] names.

## 3. The real published data on this object (all MEASURED)

| Quantity | Value | Source |
|---|---|---|
| Redshift | z = 7.0451 ± 0.0005 | Furtak+24 (Nature) |
| Engine mass, virial (Hβ FWHM 2800 ± 250 km/s) | M = 4e7 M_sun (4_-1^+2 ×10^7) | Furtak+24 |
| Engine mass, **direct dynamical** (Keplerian rotation of narrow Hα, lensed) | **M ≈ 5×10^7 M_sun** (headline: "point mass of 50 million Solar masses"), inconsistent with an NSC, consistent with the virial 4×10^7; M_BH/M* > 2. Inclination caveat: a companion Keplerian fit gives 5.6×10^6 M_sun as the inclination-unconstrained **lower limit** (Nature figure caption) — see §9 | Juodžbalis+26, Nature 2026, DOI 10.1038/s41586-026-10579-4 (arXiv:2508.21748) |
| Dense absorbing gas density (non-stellar Balmer break fit) | **n_H ~ 10^10 cm^-3**, nearly dust-free, N_H ~ 10^24 cm^-2 | Ji+25 BlackTHUNDER (arXiv:2501.13082) |
| **BLR radius, lower limit** | **R_BLR ≳ 45 light-days** (EW(Hβ) of image C ~2× the rest, 2-epoch "first attempt of AGN reverberation mapping at such an early epoch"; consistent with the local Hβ R–L scatter) | Ji+25, §7 |
| Line variability | EW(Hα) up to 18 ± 3%, EW(Hβ) up to 22 ± 8%, rest-frame 875 d; no photometric variability | Furtak+25 (A&A 698, A227; arXiv:2502.07875) |
| Lensing time delays between images | Observed-frame delay set A=0, B=+855_-6^+72 d, C=+7,043_-152^+234 d (Furtak+25 Tab. 1). Arrival order: C first, A 18–19 yr (2.2–2.4 rest) later, B another ~2.2–3 yr later (Ji+25 §7); full C→B observed span ≈ 22 yr (2.7 yr rest). Used only as a timing lever to re-order epochs — not a size | Furtak+25; Ji+25 §7 |
| Microlensing signatures | **none published** for QSO1 (no differential-microlensing size constraints exist for this object) | — |
| Host/dynamical scale | σ_N = 22 km/s; NLR traced to ~200 pc; spectroastrometric scale r_spec = 12.5 pc; sphere of influence ~270 pc | Juodžbalis+26 |

No firm reverberation lag (τ) has been measured: two epochs of image C bracket
a factor-2 continuum drop with the Hβ flux not yet adjusted — the raw
ingredient of an RM measurement, not the measurement.

## 4. The framework's parameter-free prediction (COMPUTED this door)

KP1 evaluated at the object's *own* measured observables
(lane: `kp1_z7p04_lensed_lrd_lane.py`, 7/7 PASS):

| Input | Value |
|---|---|
| M (direct dynamical, log 7.7) | 5×10^7 M_sun |
| n_H (BlackTHUNDER dense gas) | 10^10 cm^-3 |
| **r_B(KP1) = [4GM²/(c²μm_p n_H)]^{1/4}** | **7,083 au ≈ 0.034 pc ≈ 40.9 light-days** |

- Virial-mass read (4×10^7 M_sun): r_B = 36.5 ld.
- Mass band log M = 7.7 ± 0.3 → r_B ∈ **[29, 58] light-days**.
- Density dial 10^9 ↔ 10^11 cm^-3 (at 5×10^7) → r_B ∈ [23, 73] ld.

## 5. Confrontation

- **Measured:** R_BLR ≳ **45 light-days** (Ji+25). **Predicted (KP1): 40.9 ld.**
  Ratio limit/prediction = **1.10×** — inside the ×2 falsifier band by a wide
  margin; in product space the measured-side r_B⁴n_H (at the limit) exceeds
  the KP1 product by 1.46× (x2-band ⇒ ×16 product band). The 45-ld limit also
  sits inside the full predicted mass band [29, 58] ld.
- Direction of the remaining slack: the *true* BLR radius is only bounded
  below. A firm RM lag placing R_BLR in ~30–60 ld ⇒ **quantitative PASS**
  (≤×1.5 off the fiducial). R_BLR ≳ 82 ld at fixed M = 5×10^7 ⇒ **FAIL** at the
  fiducial mass (>×2). R_BLR ≲ 20 ld ⇒ FAIL low. Today: **not falsified,
  not confirmed** — OPEN, with the single measured bound agreeing.

## 6. The second, separate finding (honest tension, must be recorded)

The index's program assumed this object would carry the framework's BH*
engine mass (10^3.4–4.3 M_sun stack). The object's *direct Keplerian* mass —
the most Gamma-free measurement possible — is **5×10^7 M_sun, ~10^3.5 above
the framework's claimed engine band**. Consequences, both computed here:

1. **KP1 read at the stack mass is falsified on this object by ×78**
   (r_B = 0.58 ld vs R_BLR > 45 ld). The law resolves the read-out only when
   evaluated at the object's *actual* mass — i.e. the object itself decides
   M, and at the measured M the law holds (×1.10). KP1 as a *two-observable
   law* survives; KP1 as a *test of the 10^4-Msun engine class* fails on
   QSO1, which is independently not a 10^4-Msun engine.
2. The direct mass measurement reproduces the virial Hβ mass (4×10^7) and
   rules out the electron-scattering/low-mass alternatives for *this* object
   (Juodžbalis+26) — so the framework's engine-mass claim for the LRD class
   faces a head-on 5×10^7 M_sun anchor at z = 7.04 on the very object its
   KP1 program nominated. Whether 2609.09274's 10^3.4–4.3 estimators apply to
   other LRDs is untouched by this door; the claim that they apply to *this*
   one is dead on arrival.

## 7. Verdict (per the house rule: verdict is the deliverable)

**CONSISTENT-OPEN.**

- KP1 is not falsified on the z = 7.04 lensed LRD: measured lower limit
  45 ld vs predicted 40.9 ld → 1.10× (x2 band), product 1.46× (x16 band).
  This is the first-ever quantitative confrontation of KP1 with a direct
  radius proxy on a single LRD, and it agrees.
- The door cannot close: only a 2-epoch, lower-limit radius exists. What is
  missing: (1) a **firm continuum–Hβ reverberation lag** (multi-epoch,
  high-cadence photometric+spectroscopic monitoring of image C/A, which the
  Furtak+25/Ji+25 papers both call for), or (2) a **microlensing size
  constraint** on the BLR (none exists yet for QSO1), or (3) any resolved
  imaging of the BLR (continuum unresolved; only the NLR is resolved at
  12.5–200 pc). With (1) or (2): R_BLR ∈ [30, 60] ld closes the door PASS;
  R_BLR ≳ 82 or ≲ 20 ld closes it FAIL.
- Separate record: the framework's 10^3.4–4.3 engine-mass band is
  contradicted on this object by the direct dynamical 10^7.7±0.3 mass — a
  measured fact the next campaign index entry must absorb.

## 8. Measured vs computed (explicit accounting)

- **Measured (published, cited):** z; virial 4×10^7 M_sun; dynamical
  10^7.7±0.3 M_sun; n_H = 10^10 cm^-3; R_BLR > 45 ld; EW variations 18/22%;
  22-yr image time delays; σ_N = 22 km/s; NLR scales 12.5–200 pc. None of
  these are from this repo.
- **Computed (this door, stdlib lane, 7/7 PASS):** the KP1 constant
  (1.2685 m/kg², reproduces the index 5.02e68 m); r_B(KP1) = 40.9 ld fiducial,
  36.5 ld virial, [29, 58] ld mass band; product ratio 1.46×; the ×78 stack-
  mass violation; the [20.5, 81.8] ld falsifier band at 5×10^7 M_sun.

## 9. Audit corrections and the mass-band representation

1. **Delay ordering corrected.** The 2022-09-22 first-draft row read "A→C 18–19 yr, C→B 2–3 yr".
   The primary sources give the reverse order: image C arrives first, A 18–19 yr observed (2.2–2.4 yr
   rest) later, then B another ~2.2–3 yr later (Ji+25 §7; Furtak+25 Tab. 1 delay set A=0, B=+855 d,
   C=+7,043 d). The full C→B observed span ≈ 22 yr (2.7 yr rest) is unchanged. The delays are a timing
   lever, not a size.
2. **Direct-mass inclination caveat recorded.** The KP1 confrontation in §4–§5 uses M ≈ 5×10^7 M_sun
   (the paper's headline, identical to the virial estimate within errors). That pass is *narrow*: the
   inclination-unconstrained Keplerian lower limit is 5.6×10^6 M_sun (Nature figure caption), at which
   mass KP1 would predict r_B ≈ 14 light-days — below the 45-ld measured limit, i.e. a FAIL. The mass
   band shown as log M = 7.7 ± 0.3 → [7.4, 8.0] in §4 is this door's adopted representation (covering
   the headline and virial reads), not a verbatim uncertainty quoted in any abstract; the audit keeps it
   as the KP1 dial but flags that the agreement margin shrinks if the true mass falls below ~1.3×10^7.
3. **No microlensing size constraint (confirmed).** Furtak+25 explicitly state that all three images are
   point-sources and their measurements are "agnostic to differential magnification." The BLR-size-by-
   microlensing technique exists in the literature (e.g. J1339, J1138, Q2237+0305, J1004+4112) but has
   not been applied to A2744-QSO1. This stays on the missing-data list.

## References

- Framework: `real_research/reviews/BHSTAR_CAMPAIGN_INDEX_2026-09-20.md` (§KP1, open item 2);
  `real_research/papers/CFJC_RFC0001_bhstar_regime_coincidence.md` (r_B def., §3–5);
  `real_research/reviews/bhstar_t1_kepler_predictions.py` (KP1, 4/4 PASS).
- Furtak+24, Nature 628, 57 (arXiv:2308.05735): z, virial M, L_bol, Hβ FWHM.
- Greene+24, ApJ 964, 39 (arXiv:2309.05714): UNCOVER broad-line confirmation.
- Ma+25 (arXiv:2410.06257, ApJ): stellar-interpretation stress test, M*≈4e9, re<30 pc.
- Furtak+25, A&A 698, A227 (arXiv:2502.07875): EW variability, 22-yr delays, DRW.
- Ji+25, BlackTHUNDER (arXiv:2501.13082): n_H=1e10, non-stellar Balmer break,
  R_BLR > 45 ld, first RM attempt at z>3.
- Juodžbalis+26, Nature (2026), DOI 10.1038/s41586-026-10579-4 = arXiv:2508.21748: direct Keplerian
  M = 5×10^7 M_sun (headline "50 million Solar masses"), NSC disfavored, M_BH/M* > 2, consistent with
  virial 4×10^7; 5.6×10^6 M_sun appears as the inclination-unconstrained lower limit in a figure caption.
- R–L context for QSO1's limit: Du+16; Bentz+13 (as invoked by Ji+25 Fig. 13).