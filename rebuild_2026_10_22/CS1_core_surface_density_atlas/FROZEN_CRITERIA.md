# CS1_core_surface_density_atlas — FROZEN CRITERIA (committed alone, with the assumption ledger, before any script or number)

Written 2026-10-27 at the owner's request ("follow the real data"): measure each system's cold-sector core surface density
Σ₀ = ρ₀r₀ directly from its own data, with one uniform method across all classes, then see which law the data trace.
κ = ½ FITTED. Footings canonical (a₀ 9.3603e-11) / alt (1.1312e-10), scored separately, never pooled. Route E: gravity
Newtonian, cold dark energy = observed − baryons (a gravitating field component, never a particle). No ΛCDM input: no
concentration–mass relation, no borrowed c_f, no halo-mass function, no cosmic baryon fraction. Not "theory closed".
Nothing here says the data favour the framework or ΛCDM. This lane is descriptive: the classes name the law found.

## 0. The one method

For every system: cold mass (or acceleration) = observed − baryons, fitted by a cored halo.

- **Primary profile: Burkert,** ρ = ρ₀ / ((1+x)(1+x²)), x = r/r₀, M(<r) = π Σ₀ r₀² B(x),
  B(x) = ln(1+x²) + 2 ln(1+x) − 2 arctan x, Σ₀ ≡ ρ₀r₀ (X38's definition).
- **Variant (reported): pseudo-isothermal core,** ρ = ρ₀ / (1+x²), M = 4π Σ₀ r₀² (x − arctan x), Σ₀ ≡ ρ₀r₀.
- The model is linear in Σ₀ at fixed r₀ (and fixed Υ). Σ₀ is solved analytically by weighted least squares on a grid of
  log r₀ (and Υ where profiled). The profile χ²(log Σ₀) is the minimum over r₀ (and Υ).
- **Uncertainty:** the Δχ² = 1 interval of the profile, after scaling χ² by max(1, χ²_min/dof).
  - Both ends inside the grid: **two-sided** (σ_logΣ = half width).
  - Only the lower end inside: **lower bound**.
  - Only the upper end inside: **upper bound**.
  - Neither: unconstrained.
  - Grids: log Σ₀ [M☉ pc⁻²] from −1 to 5 in steps of 0.01. log r₀ spans 3 decades beyond the data on each side.

## 1. Classes, data, σ conventions (all on disk; nothing downloaded)

| class | data | fit | σ (record convention) |
|---|---|---|---|
| SPARC (175) | EM1's loader, mask and Υ grid 0.30–1.20 (bulge 1.4Υ) | V² − V_b²(Υ) = Σ₀ K(R; r₀) with σ_V² = 2V·max(eV, 1); **Υ profiled per galaxy, as EM1** | V_last/√2 (SC1) |
| Milky Way | Ou+24 (37 points, S3's error model); McMillan B1 baryons from S3 via GD1 (s = 1 primary; the five-value band reported) | as SPARC, baryons fixed | Ou+24 last point/√2 (GD1/SC1 literal) |
| X-COP (7 with measured stars) | matched-clumping lane's six radii 0.1–1.0 R500: M_HSE (M_FORW) − M_gas − M_star | M_cold(r) = π Σ₀ r₀² B(r/r₀); σ_M from EM_FORW, gas and star half-ranges in quadrature | V_c,HSE(R500)/√2 (no kT on disk) |
| eRASS1 stacks (X30's 106 KT clusters, 3 KT terciles) | X30 machinery read-only; bands INNER / MID / OUTER, X30's measured A and σ | per tercile: one common Σ₀ and a common x₀ = r₀/R500,i; halo truncated at X30's r_ta (as X38); predicted A = Σ model / Σ C* | median √(kT/0.6 m_p) per tercile (X30) |
| LG dwarfs (X1's 89 per footing) | X1: r₁₂ = 4/3 r_h, g_obs = g_N 10^Δ[Newton], M★ (half inside r₁₂) | **two-point only:** one cold mass M_c(<r₁₂) = (g_obs − g_N) r₁₂²/G | √(g_obs r₁₂/3) (OS1) |
| groups (P4 T3, 63) | Tian+2026: σ, M_bar, Re; same Wolf estimator as dwarfs: g_obs = 3σ²/r₁₂, r₁₂ = 4/3 Re, baryons M_bar/2 inside | **one-point only** | observed σ |

**Dwarfs and groups give only a degenerate band.** One cold mass at one radius cannot fix (ρ₀, r₀). For Burkert,
Σ₀(r₀) = M_c x²/(π r₁₂² B(x)), x = r₁₂/r₀, which diverges at both small and large r₀. So:
- each such system gives a **strict lower bound Σ_min** (the minimum over r₀) with its 1σ error from the dispersion error;
- the band Σ₀(r₀) for r₀ ∈ [r₁₂/3, 3 r₁₂] is reported.

They are never presented as measured Σ₀. Systems with no detected cold mass (Δ ≤ 0, or (g_obs − g_N)/g_N < 0.1, OS1's
rule; or M_c ≤ 0 for groups) are counted and excluded.

## 2. The law the data pick

**PRIMARY sample:** every two-sided Burkert Σ₀ from SPARC, the Milky Way, X-COP and the eRASS1 terciles (h 0.672 cell;
h 0.686 reported). Fitted in log Σ₀ vs log(σ / 70.50 km/s), by maximum likelihood with an intrinsic scatter s_int.
Per-system variance is σ_logΣ² + s_int².

| model | form | k |
|---|---|---|
| M0 FLAT | log Σ = c | 2 |
| M1 SINGLE POWER LAW | log Σ = a + q log(σ/σ_ref) | 3 |
| M2 BROKEN | continuous, slopes q₁ below and q₂ above σ_b; σ_b free in [15, 600] km/s | 5 |
| M3 FLOOR + RISE | Σ = Σ_f + A (σ/σ_ref)^q | 4 |

**Selection:**
- BIC = −2 ln L + k ln N.
- The selected model is the lowest-BIC model, unless a model with fewer parameters lies within ΔBIC < 6 of it. Then the
  simplest such model is selected.
- Class: M0 → **FLAT FLOOR**; M1 → **SINGLE POWER LAW**; M2 → **BROKEN**; M3 → **FLOOR + RISE**.
- M2 and M3 are only allowed to win if their break or floor lies inside the sample's σ range. Otherwise they are
  degenerate with M1 and are not selected.

**Override → NO SIMPLE LAW** if either:
- the selected model's s_int > 0.35 dex; or
- any class with ≥ 3 points has a mean residual both > 3 standard errors and > 0.25 dex from the selected law (the Milky
  Way alone: |residual| / √(σ² + s_int²) > 3).

**WHOLE-RANGE fit (second graded read-out).** The same four models and rules, adding the censored points:
- dwarf and group lower bounds, plus SPARC one-sided bounds, as Tobit terms Φ(±(model − bound)/√(σ² + s_int²));
- this answers "the best simple law over the whole range".

**Dwarf and group read-out vs the PRIMARY law.**
- A bound **exceeds** the law if log Σ_min − law(σ) > 2√(σ² + s_int²).
- ABOVE LAW: ≥ 25% exceed. CONSISTENT: < 5%. PARTIAL: otherwise.

The verdict needs both footings to agree, otherwise UNDECIDED. Σ₀ is a₀-free except the eRASS1 terciles, which are
measured relative to the footing's C* template.

## 3. Read-outs (reported, no class)

- Σ₀ against σ, M_b, r₀ and X43's formation proxy (its own z_f(M) table, labelled non-native). Spearman ρ for each.
- Candidates, per footing, as median and rms residual by class and as χ² on the PRIMARY sample:
  - X38 flat Σ_a₀ = 107 / 129;
  - OS1 Σ_a₀ (σ/70.50)^q_f with q_f 0.892 / 0.748;
  - X43 max(Σ_a₀, 14.83 Σ_coll(M200)), on X43's own mass conventions: SPARC and MW from EM1's relation; X-COP M200 from
    Ettori+19; eRASS1 from X30's Mfair. These are the candidate's own (borrowed) inputs, used only to draw that candidate.
- The Milky Way: its fitted Σ₀ against the law and against the Σ GD1 says Eilers needs (≈ 3.5 Σ_a₀); the s band.
- Dwarfs: where Σ_min sits relative to the law and to Σ_a₀, by X1 class.
- Variants:
  - isothermal core;
  - SPARC at Υ ≡ 0.50 (EM1 A1);
  - X-COP all 12 with M★ ≡ 0 for the five without a stellar profile;
  - eRASS1 h 0.686.

## 4. Checks

- **K0a** EM1 rows:
  - this lane's SPARC loader equals EM1's GB/GO arrays (max relative difference < 1e-12);
  - EM1's law rms 0.0541 / 0.0537 and its Newtonian row are reproduced to 1e-4 by executing EM1 read-only.
- **K0b** X-COP: g_obs and M_HSE500 of the matched-clumping lane's `run/targets.csv` cluster rows reproduced to relative
  1e-6.
- **K0c** eRASS1: with X38's halos (Σ_a₀, Mfair root), this lane's band predictor reproduces X38's committed canonical
  h 0.672 cell predictions to 1e-6.
- **K1** Burkert and isothermal closed forms vs quadrature, to 1e-6.
- **K2** Planted recovery (noise-free):
  - a synthetic SPARC-like curve with Σ₀ = 300 M☉ pc⁻², r₀ = 3 kpc is recovered to 0.01 dex;
  - the dwarf Σ_min of a planted Burkert equals the brute-force minimum to 1e-4 dex.
- **K3** Inputs: 63 groups; 89 dwarfs per footing; 7 X-COP primary clusters; 106 KT clusters.
- **K4** Peak RSS < 1 GB, one thread.

**MUTATE** (`CS1_MUTATE=1`, separate `_MUTATE` outputs):
- σ is permuted across the PRIMARY systems (seed 20261027) before the law fit.
- The control **bites** if M1's slope is under 2σ from zero and ΔBIC(M0 − M1) < 6. Then exit 1, as frozen.
- If a trend survives the shuffle, the lane reports an ALARM and exits 0.
- Reported in MUTATE too: the Tobit whole-range fit on the shuffled σ.

## 5. Disclosed before freezing

- **Hand expectations from the record (not results):**
  - OS1 found SPARC prefers Σ rising with σ (q 0.75–0.89).
  - X40b found cluster cores need ≈ 3–5 Σ_a₀.
  - GD1 found the Milky Way needs ≈ 3.5 Σ_a₀ for Eilers with McMillan baryons.
  - OS1 found the dwarfs need 3–5× its cap.
- **SPARC degeneracy.** Burkert Σ₀ in SPARC is often unconstrained above (r₀ beyond the last point) and degenerate with
  Υ. A sizeable fraction of SPARC is expected to be one-sided. The PRIMARY sample keeps only two-sided points, which
  selects galaxies whose core is resolved. That selection is disclosed; the WHOLE-RANGE fit uses the bounds too.
- **eRASS1 terciles.** INNER is uninformative (σ_IN ≈ 1.5), so each tercile has about two informative bands for two
  parameters. These points may come out one-sided.
- **Correlated radii.** X-COP radial points are model-derived and correlated. The χ² scaling partly absorbs this; the
  quoted σ_logΣ may still be optimistic.
- **No knob scans.** The model grid and Υ grid are fitting grids for measured quantities, not law knobs. No constant of
  any candidate is tuned here.
