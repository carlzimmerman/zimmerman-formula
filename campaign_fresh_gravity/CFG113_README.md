# CFG113 — does GC orbital anisotropy rescue the law's SLUGGS deficit?

- **Criteria:** frozen in `CFG113_FROZEN_CRITERIA.md` (8ef01b411), before any number.
- **Script:** `CFG113_sluggs_anisotropy.py`, about 30 s, both footings.
- **Runs:**
  - The main run passes 10 of 10 and exits 0.
  - The MUTATE run (the law's mean deficit at β = +0.5 removed from the data, scatter kept) fails H1 at 0.00σ and exits 1.
  - The two runs differ on H1, so the control is informative.

## Bottom line

**Orbital anisotropy inside the measured range does not rescue the law.** This lane keeps each galaxy's published GC density slope (CFG111) and gives the GCs a constant anisotropy β from −0.5 (tangential) to +0.5 (radial). Across that range the law's JAM-calibrated deficit never falls below:
- **+0.074 ± 0.022 dex, 3.4σ**, at β = +0.5;
- alt: +0.064, **2.9σ**.

The bracket covers the anisotropies measured for early-type GC systems:
- NGC 5846: red GCs β ≈ 0.4 and blue ≈ 0.15 outside about 3 R_e, both isotropic near 1 R_e (Napolitano+2014);
- NGC 1407: metal-rich GCs radial, metal-poor tangential (Wasserman+2018);
- M87: red GCs tangential, blue near isotropic (Li+2020).

**What the law would need:**
- **No constant β below 1 nulls its mean offset.** At β = 0.99 the mean is still +0.041 (alt +0.029), on an extended radial grid (R7).
- **Per galaxy, only NGC 3607 (β = 0.08) and NGC 4649 (β = 0.93) can be nulled.** M87, NGC 4365, NGC 4374 and NGC 5846 cannot, at any β < 1.
- **Why anisotropy is so weak here.** In a flat-rotation-curve potential with a power-law tracer, σ_los²/v_c² = (γ − β(γ − 1))/(γ(γ − 2β)). At γ = 3 this does not depend on β at all, and the published slopes are 2.5–3.4. The declared physics expectation said this before any number (frozen file).

| β | law, canonical | law, alt | rule, canonical | rule, alt |
|---|---|---|---|---|
| −0.50 | +0.086 (3.66σ) | 3.31σ | +0.036 (2.06σ) | 2.10σ |
| −0.25 | +0.084 (3.64σ) | 3.28σ | +0.032 (1.84σ) | 1.91σ |
| 0 (CFG111) | +0.082 (3.60σ) | 3.22σ | +0.028 (1.55σ) | 1.64σ |
| +0.25 | +0.079 (3.53σ) | 3.12σ | +0.021 (1.13σ) | 1.26σ |
| +0.50 | **+0.074 (3.38σ)** | **2.93σ** | +0.011 (0.56σ) | 0.69σ |
| +0.75 (beyond the bracket) | +0.064 (2.99σ) | 2.48σ | −0.005 (−0.21σ) | −0.10σ |
| +0.90 (beyond the bracket) | +0.053 (2.46σ) | 1.91σ | −0.019 (−0.75σ) | −0.68σ |

- **Only near-radial orbits,** β ≈ 0.9 and beyond anything measured, bring the law below 2σ, and only on the alt footing.
- **The rule moves the other way:**
  - it fits for isotropic and radial GC orbits;
  - it goes just past 2σ for tangential orbits (β = −0.5: 2.06σ, alt 2.10σ).
  - So CFG111's restored SLUGGS pass for the rule holds unless the GC orbits are tangential.

## Other rows (canonical)

- **R4, γ = 3 for every galaxy (CFG55's baseline):**
  - β barely matters, and pushes the other way: the law is 3.87σ at β = −0.5, 3.99σ at 0 and 4.20σ at +0.5.
  - The residual comes from the inner potential, which is not flat.
- **R5, SLUGGS's population masses:** the law is 2.44σ at β = −0.5 and 2.24σ at +0.5. The rule is −0.24σ and −1.31σ.
- **R6, the four group and cluster centrals excluded,** at β = +0.5 (N = 12): the law is 1.93σ and the rule 0.28σ.

## Controls

- **C1:** at β = 0 the machinery reproduces CFG111's 64 committed per-galaxy offsets exactly: law and rule, both footings.
- **C2:** in a flat-rotation-curve potential, h50's Jeans solver with β reproduces the analytic dispersion to 2.3 × 10⁻⁴. It was checked at γ = 2.5 and 3.43, β = ±0.5.
- **MUTATE:** with the law's mean deficit at β = +0.5 removed from the observed dispersions (D = 0.074 dex canonical, 0.064 alt), H1 fails at 0.00σ and the script exits 1.

## Caveats

- **Constant β only.** Radially varying β(r) is not tested. At every radius, a constant +0.5 is at least as radial as the measured profiles above.
- **One β for all GCs.** The red and blue subpopulations differ, and the tracer mixes them.
- **Slopes and orbits are varied separately.** The corners (the lower γ bracket together with radial β) are not explored.
- **The solver's grid edge.** h50's radial grid ends at 3 × 10⁴ kpc, which biases σ low at β ≥ 0.9.
  - R7 bounds the bias: on a grid extended to 3 × 10⁶ kpc the law's mean moves by 0.0009 dex at β = 0.9 and 0.0025 dex at β = 0.99.
  - Inside the bracket the mean is unchanged to 10⁻⁴.

## Disclosures

- **R7 was added after the first run,** as a reported row. Every other line of both logs is unchanged apart from timing.
- **The literature values were read from the arXiv abstract pages** of arXiv:1401.1501, 1712.01229 and 2005.09410 on 2026-09-29. No files were downloaded.

## Reading

- **The law.** Its SLUGGS deficit survives both halves of the mass–anisotropy degeneracy, within measured ranges:
  - with realistic GC slopes (CFG111) and any measured-range anisotropy (this lane) it stays at 2.9σ or more;
  - the γ caveat and the β caveat each fail to explain it away.
- **The rule** fits unless the GC orbits are tangential.
- **Not computed here:** CFG112 answered whether one debris fraction fits all ten populations at 2σ only at β = 0. At β = +0.5 the rule's SLUGGS offset falls from 1.55σ to 0.56σ, which could open CFG112's narrow gap.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
