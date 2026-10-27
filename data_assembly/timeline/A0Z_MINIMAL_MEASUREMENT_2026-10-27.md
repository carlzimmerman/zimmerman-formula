# The minimal measurement that decides a₀ at z ≈ 2 (scope, 2026-10-27)

**This is a synthesis of committed lanes. No new computation and no data query.** κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework.

## The question, and why it is the right one
The framework's distinctive claim is a₀ = (c/2)√(Gρ_Λ): **a₀ is set by dark energy, so it stays (nearly) the same at high redshift.** Three readings make different predictions at z ≈ 2–2.5:

| reading | a₀(z)/a₀(0) at z 2.0 | at z 2.5 | source |
|---|---|---|---|
| **framework** (Λ constant / DESI-evolving DE) | 1.00 / 0.87–0.94 | 1.00 / ≈ 0.8 | CFG571, CFG689, CFG385 |
| a₀ ∝ H(z) (the "coincidence" reading) | 3.03 (+0.48 dex) | 3.8 (+0.58 dex) | CFG571, CFG385 |
| ΛCDM + feedback, RAR-equivalent scale | ≈ 2.8 (+0.45 dex) | — | CFG565 (CFG566 caveat: diluted through the committed estimators) |

- **Flat vs H(z) is 0.5–0.67 dex.** 3σ needs σ(log a₀) ≤ 0.22 dex (CFG385). This is **reachable**.
- **Framework vs ΛCDM-feedback is a similar size**, but it needs measured gas, because a halo can stand in for a different a₀.
- **Λ vs evolving DE inside the framework is 0.03–0.13 dex.** That is **out of reach** near-term; it needs the ngVLA / SKA era.

## Why no existing data can do it
- **The calibration wall (CFG240):** with an unknown baryon normalisation f, σ(log a₀) ≥ 3σ/√N. At z ≳ 1.6, absolute baryon masses are uncertain by 0.35–0.7 dex per object (GAS_ANCHOR_SCOPING), so a shared calibration cannot reach 0.22 dex.
- **The way around it, self-calibration (CFG385):** if one galaxy's curve spans both regimes, its **inner Newtonian points (y ≳ 3) fix its own baryon scale** and its **outer points (y ≲ 0.3) fix a₀**. No absolute stellar or gas calibration is needed. One such disc with 7–12 points at ~5 % velocity precision, spanning y ≈ 0.1–5, reaches about 0.2 dex.
- **No such galaxy exists in any data set the record holds or has searched:**
  - KMOS3D curves span only ~2× in radius (CFG386).
  - KURVS has deep outer points but no inner anchor (CFG386).
  - Genzel+2017 is shape-degenerate, with 6–8 beam-resolved points (CFG401/402/405).
  - 0 of 442 z 1–3 discs have an AO-resolved inner curve, a deep outer curve and resolved gas together (CFG403).
  - MUSE-DARK's a₀ rise depends on how the masses are measured (CFG262 / CFG303 / CFG356).
- **The structural reason (arithmetic):** a disc reaches y = 0.3 at r = √(GM_b/0.3a₀). That is about **22 kpc for M_b ~ 10¹¹ M☉** (beyond any Hα curve) and about **7 kpc for M_b ~ 10¹⁰ M☉** (observable). The massive cosmic-noon discs that dominate today's samples are baryon-dominated wherever they are measured (CFG256). **The deciding galaxies are low-mass discs.**

## The specification
**Per galaxy (z ≈ 1.5–2.6, M_b ≲ 3 × 10¹⁰ M☉, a rotating disc):**
1. **Inner anchor:** rotation points at y ≳ 3, i.e. ≲ 1 kpc. At z ≈ 2, 1″ ≈ 8.5 kpc, so this needs ≲ 0.1″: adaptive-optics, space-based IFU or ALMA at long baselines. A cold-gas (CO / [CI]) curve is best: σ_CO ≲ 15 km/s, so no pressure correction is needed (Lelli+2023, CFG278).
2. **Outer reach:** rotation points at y ≲ 0.3, i.e. 3–5 R_e (~6–15 kpc, ~0.7–1.8″), at **≤ 5 % velocity precision** and **on both sides of the disc**. From this thread (arXiv:2507.10544, CFG405): one-sided faint outskirts are exactly where curves mislead. Any point beyond the radius both sides reach is reported but not used.
3. **Outer velocity-dispersion profile,** for the pressure-support term (CFG140 / 141 / 160).
4. **Baryon profile shapes, not normalisations:** stars from rest-frame near-IR imaging, gas from CO / [CI] / dust maps. Their normalisations are fitted per galaxy, so the calibration wall drops out.
5. **Inclination ≥ ~35°,** with kinematic and morphological values agreeing. Faint high-z discs read too face-on (arXiv:2507.10544), and the face-on cases drove the Genzel residual (CFG401 / 405).
6. **3-D forward modelling of beam smearing,** not 2-D velocity maps.

**How many:**
- **3–5 spanning discs** decide flat vs H(z) at ≳ 3σ jointly, while the kernel-shape systematics (P2 vs exp-RAR, 0.03–0.05 dex) stay below the gap.
- **10–20** make it a sample-level result robust to per-galaxy systematics (CFG385's specification).
- **Measured gas masses** on the same discs separate the framework from ΛCDM-feedback.

**Route:**
- **Gravitationally lensed low-mass discs:** magnification gives both resolution and surface brightness, which beats the (1+z)⁴ dimming at the outer edge.
- **Space-based IFU Hα for the outer curve**, plus **near-IR imaging for the stellar shape**, plus **ALMA CO / [CI] for the cold inner curve and the gas shape.**

## What arrives soon, and what it can and cannot do
- **ALMA U4_27928 (z 1.42, public 2026-11-06) and GS4_24110 (z 2.0, public 2026-11-28):** predictions are pre-registered (CFG571; plans CFG806 / CFG809, the owner's governing choice on 10-20) and the harnesses are ready (CFG942). They are **single massive discs**, so they are demonstrations: "one disc excludes nothing." CFG942 expects S/N below 5 at native resolution, so the likeliest result is an upper limit.
- **Gaia DR4 (2026-12-02):** wide binaries test low-acceleration gravity locally. It separates the framework from plain MOND, not a₀(z).
- **Neither gives the z ≈ 2 a₀ measurement.** That needs new observations of the specification above.

## Next concrete steps (each needs the owner's go)
1. **Target search (metadata only):** lensed and unlensed rotating discs at z 1.5–2.6 with M★ ≲ 10¹⁰·⁵. Rank by expected r(y = 0.3) against the reachable radius, and by archive coverage (space IFU, AO, ALMA). It uses the same machinery as CFG403, aimed at low mass.
2. **Freeze the analysis before any data:** self-calibrated a₀ per disc (CFG385's estimator), the two-sided cut and inclination cut above, the pressure term, the kernel bracket, and kill lines for flat and for H(z).
3. **Proposals:** a space-IFU and ALMA programme on the 3–5 best spanning candidates.

Sources: CFG240, CFG256, CFG262, CFG278, CFG303, CFG356, CFG385, CFG386, CFG401–405, CFG565 / 566, CFG570 / 571, CFG689, CFG806 / 809, CFG942; `data_assembly/GAS_ANCHOR_SCOPING_2026-09-30.md`; `READING_deAraujoCarvalho2025_2507.10544.md`.
