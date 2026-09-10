# L99 — no purely-dark gravitating structure: the cuscuton source forbids dark subhalos, a clean discriminator against ΛCDM

**The distinctive prediction.** Because L95 proved a consistent relativistic MOND scalar is a **cuscuton** —
a non-propagating, instantaneous elliptic constraint `div[μ(|∇Φ|/a₀) ∇Φ] = 4πG ρ_baryon` sourced **entirely**
by the baryons — the phantom ("dark") mass is a **deterministic functional of the baryon distribution that
vanishes where the baryons vanish**. So there are **no purely-dark gravitating structures**: no dark
subhalos, no dark satellites, no starless dark clumps. Every gravitationally-detectable structure must
contain baryons, and there is **no free "dark subhalo mass function"** to populate. ΛCDM predicts the
opposite — an abundant, mostly-**starless** subhalo population (`dN/dM ~ M⁻¹·⁹`, hundreds above 10⁷ M⊙ per
Milky-Way host), the very substructure invoked to explain strong-lens flux-ratio anomalies and gaps in cold
stellar streams.

2026-09-09. A **prediction** lane (not a CHARTER L1–L4 lane), building on the cuscuton theorem in
[L95_closure_forces_cuscuton.py](L95_closure_forces_cuscuton.py) and companion to the no-dynamical-friction
prediction [L96_no_halo_dynamical_friction.py](L96_no_halo_dynamical_friction.py) and the early-structure
prediction [L97_early_structure_jwst.py](L97_early_structure_jwst.py).
Script: [L99_no_dark_subhalos.py](L99_no_dark_subhalos.py) → [L99_no_dark_subhalos.out](L99_no_dark_subhalos.out).
**16 checks, 16 PASS / 0 FAIL; exit 0; runtime < 1 s.** Both a₀ footings (9.3619e-11 / 1.1279e-10 m s⁻²)
carried where dimensional.

**Polarity.** Each check asserts a *statement* and PASS means the statement is true. A PASS on a verdict
line is not a win for the theory — read the statement. Self-contained numpy; nothing under
`qwen_claude_field_theory/` (or any other agent's directory) is imported, executed, or read; no HASH or
PREREGISTRATION files are touched.

---

## 1. The structural prediction, stated precisely (PART 0–1)

The cuscuton field carries **no independent dark degree of freedom**. Solving the constraint for an isolated
spherical baryonic mass `M_b` in deep MOND (`g_N ≪ a₀`) gives `g(r) = √(G M_b a₀)/r`, so the enclosed
**dynamical** mass and the enclosed **phantom** mass are

    M_dyn(r) = √(M_b a₀ / G) · r          M_phantom(r) = M_dyn(r) − M_b .

Two facts follow, both verified numerically as controls (CTRL-1, CTRL-2, CTRL-3):

1. **The phantom is a deterministic `√(M_b)` functional** — quadrupling `M_b` doubles the phantom
   (`M_ph(4M_b)/M_ph(M_b) = 1.95 ≈ √4`), with **no** free normalization, concentration, or scatter to choose.
2. **The phantom vanishes with the baryons** — `M_ph(M_b = 0) = 0` identically, and `M_ph ~ √(M_b) → 0`
   continuously (`M_ph(10⁻⁶ M_b)/M_ph(M_b) = 10⁻³`). **A starless region sources no extra gravity.**

From these the prediction is exact:

> **PRED-1.** No purely-dark gravitating structure — no dark subhalos, no dark satellites, no starless dark
> clumps. Every gravitationally-detectable structure must contain baryons.
>
> **PRED-2.** The phantom around a baryonic body is a deterministic functional of *that body's* baryons, so
> there is **no free dark subhalo mass function** — the amount and shape of the extra gravity are set by the
> baryon distribution, not drawn from a halo population with its own masses and concentrations.

---

## 2. The ΛCDM contrast, quantified (PART 2)

| ΛCDM prediction | number | cuscuton prediction |
|---|---|---|
| subhalo mass function slope | `dN/dM ~ M⁻¹·⁹` (cumulative `N(>M) ~ M⁻⁰·⁹`) | no dark subhalos at any mass |
| count per MW-mass host | `N(>10⁷)~500`, `N(>10⁸)~64`, `N(>10⁹)~8` (order-of-magnitude, calibrated to ~300 above 10⁻⁵ M₂₀₀, Aquarius) | 0 dark |
| starless fraction | most below the ~10⁸ M⊙ atomic-cooling / reionization threshold form no stars | — |
| flux-ratio-anomaly / imaging perturbers | ~10⁷–10⁹ M⊙, `f_sub ~ 0.5–2%` (Dalal & Kochanek 2002); imaging detections ~2×10⁸ M⊙ (Vegetti+2010 SDSS J0946+1006; Vegetti+2012 B1938+666) | any real perturber is **baryonic** |
| cold-stream gaps | GD-1 perturber ~10⁶–10⁷ M⊙, < ~20 pc (Bonaca+2019); Pal 5 similar | a dwarf, a GC, or a baryonic clump |

The slope is the robust part (`α = 1.9`, Springel+2008 and others); the normalization is order-of-magnitude
and flagged as such in the script. The load-bearing contrast is structural, not normalization-dependent:
ΛCDM has an **abundant, mostly-starless** low-mass population and a **free** subhalo mass function; the
cuscuton framework has **neither**.

---

## 3. The falsifier (PART 3)

A perturber's gravitational strength is set by its enclosed dynamical mass `M_dyn`. In the cuscuton picture
`M_dyn` is produced by baryons **plus their phantom**, so an inferred `M_dyn` implies a **baryonic** mass
that should be detectable if it is above the stellar/gas floor. Inverting the deep-MOND relation at `r ≈ 1
kpc`:

    inferred 10⁸ M⊙  →  M_b ≈ 1.5×10⁷ (can) / 1.2×10⁷ (alt) M⊙
    inferred 10⁹ M⊙  →  M_b ≈ 1.5×10⁹ (can) / 1.2×10⁹ (alt) M⊙

Both are far above the ~10⁶ M⊙ detection floor for a dwarf or gas clump.

> **FALSIFIER (FALS-1).** A robust gravitational perturber — a lensing substructure or a stream gap — at an
> inferred ~10⁸–10⁹ M⊙, with **no baryonic counterpart** at a location where a counterpart *should* be
> detectable, falsifies the baryon-sourced (cuscuton) picture.
>
> **CONVERSE (FALS-2).** If every robustly-detected perturber turns out to have a baryonic counterpart once
> searched to the appropriate depth, that supports the cuscuton picture over an abundant dark-subhalo
> population. It is a genuine two-sided test.

---

## 4. Honest nuance — MOND is *not* "no perturbers" (PART 4)

The prediction is about **dark (starless)** perturbers specifically. Four edges are stated in the script so
the claim is not overstated:

- **NUANCE-1 — baryonic perturbers do perturb, with a boosted mass.** A baryonic satellite carries its own
  phantom, so `M_dyn/M_b = r/r_M` is boosted by a factor of several-to-tens at kpc scales (`r_M ≈ 0.12 kpc`
  for 10⁷ M⊙; boost ≈ 4/8/41 at 0.5/1/5 kpc, canonical; ≈ 4.5/9/45 alt). **A ~1.5×10⁷ M⊙ baryonic dwarf
  mimics an inferred ~10⁸ M⊙ perturber** — the inferred "mass" overstates the baryonic mass and must be read
  through the MOND boost.
- **NUANCE-2 — the test is at masses where baryons should be seen.** Very low-mass baryonic clumps (faint
  dwarfs, GCs) can sit below detection, so a baryonic and a "dark" perturber are degenerate below the floor.
  The clean falsifier is a perturber above the baryon-detection floor.
- **NUANCE-3 — the external-field effect weakens satellite phantoms inside the host.** At the GD-1
  galactocentric radius the MW external field `g_ext ≈ 1.05×10⁻¹⁰ m s⁻² ≈ a₀`, which suppresses a satellite's
  internal deep-MOND phantom, so the isolated boost is an **upper bound**. This weakens MOND's baryonic
  perturbers (it does not help the framework) and is stated, not hidden.
- **NUANCE-4 — nothing currently falsifies.** GD-1's perturber is **not** confirmed dark (Bonaca+2019 cannot
  exclude a globular-cluster / baryonic origin), and the lensing-substructure detections have luminous
  counterparts at or below detection limits. The prediction awaits a **confirmed starless perturber** above
  the baryon-detection floor — an open, future-decided test.

---

## 5. Verdict

**Because relativistic MOND must be a cuscuton (L95), sourced entirely by the baryons, the phantom mass is a
deterministic functional of the baryon distribution that vanishes where baryons vanish — so the framework
forbids purely-dark gravitating structure: no dark subhalos, no dark satellites, no starless dark clumps, and
no free dark subhalo mass function.** This is the opposite of ΛCDM's abundant, mostly-starless `M⁻¹·⁹`
subhalo population — exactly the ~10⁷–10⁹ M⊙ dark perturbers invoked for flux-ratio anomalies
(`f_sub ~ 0.5–2%`, imaging detections ~2×10⁸ M⊙) and cold-stream gaps (GD-1, ~10⁶–10⁷ M⊙). The falsifier is
a robust perturber with no baryonic counterpart at a mass where the counterpart should be detectable (an
inferred ~10⁸–10⁹ M⊙ perturber needs ~10⁷–10⁹ M⊙ of baryons); the converse — all perturbers turning out
baryonic — supports it. The honest scope is that MOND **does** perturb streams and lenses through the phantom
around **baryonic** perturbers (boosted effective mass, EFE-suppressed inside the host), and very low-mass
baryonic clumps are hard to detect, so the discriminator is about **dark** perturbers specifically and
nothing currently falsifies. **The value is the derivation:** "no dark-only structure" is a consequence of
the cuscuton source theorem, not an assumption — a clean structural discriminator against particle dark
matter, on both a₀ footings.

---

## 6. What is open, named

1. **A confirmed starless perturber.** The whole test turns on finding (or failing to find) a robust
   gravitational perturber with no baryonic counterpart above the detection floor. GD-1 is a candidate whose
   baryonic origin is not excluded; no confirmed dark perturber exists yet.
2. **A full cuscuton perturbation calculation.** The `M_dyn(r) = √(M_b a₀/G)·r` boost used here is the
   isolated-spherical deep-MOND result; the actual stream-gap / lensing signal of a baryonic dwarf in the
   host's external field needs the cuscuton constraint solved on the real geometry (EFE included). This lane
   establishes the structural prediction and the order of the boost, not a precise perturbation spectrum.
3. **The baryon-detection floor as a function of environment.** The ~10⁶ M⊙ floor is a representative
   number; the mass above which a counterpart "should" be seen depends on distance, surface brightness, and
   gas content, and sets exactly where the falsifier bites.

Nothing here is closed, and κ = ½ remains **fitted**; this lane is a prediction from the cuscuton structure,
not a derivation of the coefficient.
