# The Faber–Jackson / Velocity-Dispersion Channel for a₀(z) — Explored, with Literature

**C. Zimmerman, June 2026.** *Following the suggestion that pressure-supported systems (ellipticals, bulges) give an
independent test of a₀(z) via σ ∝ E(z)^¼. Worked, and the literature combed (`reviews/project_faber_jackson_a0z.py`).
Honest result: the prediction is real and standard, but the channel is **not a clean test** — it inherits the ΛCDM
degeneracy, the available high-z data are in the wrong acceleration regime, and the closest **published** tests
already **disfavor the evolving coupling and favor the constant/geometric one.** No new door.*

---

## The prediction is real and standard

The deep-MOND **Faber–Jackson relation** is σ⁴ = (4/9) G M a₀ — Milgrom (1984, ApJ 287, 571, "Isothermal spheres in
the modified dynamics"), with the (4/9) coefficient from the isotropic deep-MOND Jeans solution in Sanders (2010,
MNRAS 407, 1128). It is the pressure-supported analog of the Baryonic Tully–Fisher V⁴ = G M a₀, and it is
well-supported *locally* across globular clusters, dwarf spheroidals, and ellipticals on a single a₀.

With a₀(z) = cH(z)/Z, at **fixed baryonic mass** σ ∝ a₀^¼ ∝ **E(z)^¼**: +16% at z=1, +32% at z=2. Arithmetically
correct, and not previously written down as a dedicated a₀(z) test — so there is a narrow novelty gap. But it is not
worth promoting, for three reasons.

## Why it is not a clean test — three strikes

1. **Degeneracy (worse than the disk RAR).** High-z quiescent galaxies are a factor ~2–4 **more compact** at fixed
   mass (Belli, Newman & Ellis 2014; van Dokkum 2011). Since σ² ~ GM/R, a factor-2 size shrink alone raises σ by
   ~√2 = **+41%** — *larger than, the same sign as, and degenerate with* the +32% MOND effect, for purely
   Newtonian/structural reasons. The **mass Fundamental Plane is already in place by z~2** (Bezanson 2013; de Graaff
   2021), i.e. the dynamics look like ordinary gravity + structural growth, with no clean room for an evolving a₀.

2. **Wrong acceleration regime.** The FJ relation requires the *global, large-radius, low-acceleration* (g ≪ a₀)
   dispersion. High-z dispersions are **central**, at **g ~ 3–11 a₀** (Milgrom 2017, arXiv:1703.06110) — near
   Newtonian — so σ⁴ = (4/9)GMa₀ is **not even the operative physics** there. The deep-MOND dispersion regime is
   reached observationally only in **globular-cluster outer profiles and dwarf spheroidals** (Scarpa & Marconi),
   none of which exist at z>1. The one observable that would make this clean is exactly the one you can't get.

3. **The published direct tests already disfavor evolving a₀ — and favor the geometric core.** This is the most
   important finding, and it connects straight to `THE_GEOMETRIC_CORE_VS_THE_EVOLVING_CLAIM.md`:
   - **Limbach, Psaltis & Özel (2008, arXiv:0809.2790)** test Tully–Fisher to z=1.2 against *exactly* two couplings —
     **a₀ ∝ cH₀** and **a₀ ∝ √Λ**. Both are excluded within formal errors, but the data **marginally favor the √Λ
     (constant/geometric) coupling over the H(z) one.** That is a published comparison of *our two versions*, landing
     on the geometric core.
   - **Milgrom (2017, arXiv:1703.06110)** finds high-z disks "all but exclude ~4 a₀ at z~2, excluding a₀ ∝ (1+z)^1.5."
     The framework's E(2) = **3.0 a₀** is milder than the excluded (1+z)^1.5 = 5.2, but sits uncomfortably close to
     the ~4 a₀ exclusion line.

## A correction this forced (honest record-keeping)

The repo's `highz_kinematic_test.py` had concluded that de Graaff et al. (2024, JADES/NIRSpec z~6) dispersions
"mildly favor" evolving a₀. **That is retracted.** Those are *central* dispersions (g ~ 3–11 a₀, not deep-MOND), and
their high M_dyn/M_* (up to 40) is explained equally well by dark-matter domination **or low star-formation
efficiency** (de Graaff's own reading) — so they neither validly test the FJ relation nor favor evolving over
constant a₀. A superseded banner is now on that file.

## Verdict

The Faber–Jackson channel is the **existing a₀(z) door wearing different clothes** — and it points the same way the
disk data do: **against the evolving extension, for the geometric/constant core.** It is degenerate with compactness
evolution, the high-z data sit in the wrong (near-Newtonian) regime, and the published disk-based tests (Limbach
2008; Milgrom 2017) already disfavor a₀ ∝ cH(z) while favoring a₀ ∝ √Λ. So: **no new door, no independent
confirmation** — but a genuinely useful outcome, because Limbach (2008) is a *published* head-to-head of the
evolving vs geometric couplings, and it lands on the geometric one. That sharpens, with external authority, the same
split we drew internally: the geometric core is the defensible bet; the evolving claim is the one the data resist.

### Key citations
Milgrom 1984 (ApJ 287, 571); Sanders 2010 (MNRAS 407, 1128); **Limbach, Psaltis & Özel 2008 (arXiv:0809.2790)**;
**Milgrom 2017 (arXiv:1703.06110)**; Belli, Newman & Ellis 2014 (ApJ 783, 117); van Dokkum 2011 (ApJ 736, L9);
Bezanson 2013 (ApJ 779, L21); de Graaff 2021 (arXiv:2012.05935); de Graaff 2024 (A&A 684, A87); Scarpa & Marconi
(NGC 6171/7099 outer-dispersion deep-MOND tests).
