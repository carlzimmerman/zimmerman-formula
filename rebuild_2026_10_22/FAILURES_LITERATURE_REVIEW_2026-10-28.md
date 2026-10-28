# The four failures: an adversarial literature check (2026-10-28)

**Purpose.** For each failure in `THEORY_EQUATIONS_2026-10-28.md`, ask what independent studies say and what the data
gatherers assumed.

**Status: PROVISIONAL.**
- These are web-search summaries (standing rule: web look-ups are provisional until the source text is read).
- Nothing here changes a graded verdict.
- Each item ends with a **testable lane** that can be frozen and graded.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## 1. IC 1613: the law over-predicts about 4× (HO3 stellar σ; RT1 HI rotation)

**What the literature says.**
- **The inclination is contested.** Oh+15's inclination of 48° ± 0° conflicts with its own free-ring fits, which scatter
  from 15° to 85°. Independent analysis argues that i ≈ 20° would put IC 1613 back on the baryonic Tully–Fisher scatter.
  A tilted-ring fitter (3D BAROLO) is shown to overestimate low inclinations, so the true value could be about 15°.
  ([arXiv:1601.01026](https://arxiv.org/pdf/1601.01026); [arXiv:1601.05821](https://arxiv.org/pdf/1601.05821))
- **It is a known bad case for MOND fits.** The MOND rotation-curve roster lists IC 1613 as dubious, because of very
  uncertain inclination and asymmetric drift. Inclination enters MOND fits as sin⁴ i.
  ([MOND fit roster](https://astroweb.case.edu/ssm/mond/fitroster.html))
- **New stellar kinematics.** A 2024 MUSE study detects stellar rotation for the first time and gives a new inclination
  from stellar tracers alone; its HI value is 39.4°.
  ([arXiv:2402.01631](https://arxiv.org/pdf/2402.01631))
- **An inclination-free check.** Kirby+14's σ and r_h give V_c ≈ 18.7 km/s at about 1.4 kpc. That is the same data
  as HO3's stellar-σ tracer.

**Adversarial reading.**
- RT1's HI tracer is **inclination-limited**. At i ≈ 20°, V_rot would rise by sin 48°/sin 20° ≈ 2.2×. That removes most
  of RT1's −0.59 dex.
- The **stellar-σ tracer has no inclination** and still over-predicts. A deep-MOND isolated estimate with LITTLE THINGS'
  baryons (8.7e7 M☉) gives σ ≈ 15 km/s against 10.8 measured, about 0.3 dex over, which matches FD1's −0.31.
- **So IC 1613 reduces to about 0.3 dex on the σ tracer alone.** That residual has one native lever the record has not
  graded: the **external field**.
  - X1's EFE column used d_host 731 kpc (the MW) and found no effect.
  - In the basin picture, IC 1613 sits inside the Local Group basin. Its total mass (≈ 10^12.4 M☉, cold dark energy
    halos included) gives g_e/a₀ ≈ 0.015 at about 500 kpc. That is comparable to IC 1613's own g_N/a₀ ≈ 0.02.
  - An AQUAL external field of that size suppresses the boost, the right direction.

**Testable lane.** IC 1613 and the other field dwarfs under AQUAL with the external field of the LG basin's **total**
mass, computed from the dwarf's barycentric distance. Grade with the stellar σ, which is inclination-free.

## 2. X-COP cluster profiles: right mean, wrong shape (HO1: cores under-pulled +0.19, outskirts −0.12)

**What the literature says.**
- X-COP's hydrostatic masses need little correction. The median non-thermal pressure is about 6 % at R500 and 10 % at
  R200 (Eckert+19), and the bias is 0.03 in half the sample (Ettori & Eckert 2022).
  ([arXiv:1805.00034](https://arxiv.org/abs/1805.00034v1); [arXiv:2112.07554](https://arxiv.org/pdf/2112.07554))
- **The assumption:** hydrostatic masses assume fully thermalised gas, and Eckert+19 uses a universal gas fraction as a
  reference.

**Adversarial reading.**
- The hydrostatic **masses** are unlikely to be the problem: a 6–10 % bias is far below the 0.12–0.19 dex shape miss.
- The suspect is the **baryon side at small radius.** At 0.1 R500 (about 100 kpc), the brightest cluster galaxy's stars
  are a large fraction of the baryons. If HO1's M★(<r) under-counts the BCG, for example with a stellar profile that
  is too extended or a light Υ★, the cores are under-pulled exactly as seen.

**Testable lane.** Regrade HO1(a) with an explicit BCG component (a Hernquist profile, with M★ from each cluster's BCG
K-band light at Υ_K = 0.6–0.8). Grade only the inner points.

## 3. X-ray-bright groups: the sign is opposite (HG2 D −0.29; it survives GA1 and DY1)

**What the literature says.**
- No eRASS1 study compares bright and faint groups at matched σ.
- **Group σ is under-estimated below about 10 members**
  ([astro-ph/9812032](https://arxiv.org/pdf/astro-ph/9812032)). DY1 found σ sound for these groups, with medians
  matching to 7 %.
- **The choice of aperture changes the scatter of dynamical mass.** An X-ray-based r200 gives less scatter than
  optical radii ([arXiv:2402.08453](https://arxiv.org/html/2402.08453v2)).

**Adversarial reading.**
- HG2's g_obs = 3σ²/r at (4/3) R_h uses the **galaxies' projected half-number radius**.
- X-ray-bright groups are more relaxed and centrally concentrated, so their R_h is smaller. That *raises* g_obs, the
  wrong way to explain D < 0.
- But the reference comparison is made at g_bar, which also rises steeply as 1/r². A systematic difference in R_h
  between the arms moves g_bar more than g_obs, so it can *create* a negative D. This is an **estimator geometry**
  effect, and DY1 left it un-audited.

**Testable lane.** Regrade HG2 at a common physical aperture for both arms: a fixed radius in kpc, or the X-ray R500
for the bright groups with the same σ-scaled radius for the faint ones. Test whether D's sign survives.

## 4. SLUGGS ellipticals: under-predicted by 0.15 dex (HO2)

**What the literature says.**
- NGC 5846's GC subpopulations break the mass–anisotropy degeneracy. Red GCs are radially anisotropic (β ≈ 0.4) beyond
  3 R_e; blue GCs have β ≈ 0.15 (Napolitano+14).
  ([arXiv:1401.1501](https://arxiv.org/pdf/1401.1501))
- SLUGGS dark-matter fractions are fairly insensitive to β in some galaxies (Alabi+17).
  ([arXiv:1701.05904](https://arxiv.org/pdf/1701.05904))

**Adversarial reading.**
- **The data gatherers' key assumption is the stellar IMF.** Massive ellipticals are widely reported to need heavier
  (bottom-heavy) IMFs than Chabrier/Kroupa, with Υ★ higher by about 1.5–2×. A heavier IMF adds baryons and lifts the
  law's prediction toward the data.
- HO2's M★/M_JAM of 0.87–0.95 suggests the record's M★ may already be JAM-like, i.e. heavy. That has to be checked
  before this lever is claimed.
- The **hot gas around these ellipticals** (they are X-ray luminous) is the other un-counted baryon. GT1 could not test
  it, because there is no kT on disk.

**Testable lane.** SLUGGS with (a) an IMF-heavy Υ★ variant, bounded by M_JAM, and (b) the X-ray gas from published
β-models of M87, NGC 4374 and NGC 5846, a download that needs owner approval.

## Summary

| failure | most likely cause from the literature | native or data? | cheapest lane |
|---|---|---|---|
| IC 1613 | inclination (HI tracer); external field of the LG basin (σ tracer) | data + **native EFE** | AQUAL EFE from the basin mass |
| X-COP shape | BCG stars under-counted in the cores | data | add a BCG component |
| HG2 sign | aperture geometry of 3σ²/r against g_bar | data (estimator) | common-aperture regrade |
| SLUGGS | IMF and un-counted hot gas | data | IMF variant; X-ray gas (download) |

None of these is graded yet. Each becomes evidence only through a frozen lane.
