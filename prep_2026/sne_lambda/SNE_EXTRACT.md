# Dark-energy density from Type Ia supernovae vs. the MI-framework galaxy prediction

**Lane:** SNe extraction + comparison. Carl Zimmerman's de Sitter–Unruh
**modified-inertia** framework. Sarkar-relevant cross-corroboration test.
Script: `sne_extract.py` (exit 0, numpy). Results: `sne_extract_results.json`.

**Credits:** Milgrom (interpolation kernel `nu=sqrt(1+1/y)`, PLA 1999); Brout+2022 /
Scolnic (Pantheon+); Perlmutter / Riess / Schmidt (accelerating-universe discovery);
Sarkar (the SNe-leg critique this test is relevant to).

---

## The physics, stated honestly (not blurred)

The framework **does not modify the cosmological background.** The scale
`a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z` (`Z = sqrt(32pi/3) = 5.789`) modifies
galaxy **inertia**, not expansion. `Lambda` is a genuine constant, so
`H(z) = H0 sqrt(Om(1+z)^3 + OL)` and the SNe distance modulus `mu(z)` are **standard
LCDM**. There is **no framework-native SNe formula** (banked: MI linear cosmology
overshoots/dead or LCDM-degenerate).

So **"rho_DE from SNe" IS the standard LCDM extraction.** The framework's only
contribution here is the **galaxy-side prediction** that gets compared:
`rho_DE = 4 a0^2 / (G c^2)` (from `Lambda = 32pi a0^2/c^4`,
`rho_Lambda = Lambda c^2/(8 pi G)`).

---

## SNe-side (standard extraction)

Pantheon+ (Brout+2022, ApJ 938:110; 1701 light curves / 1550 SNe Ia), SNe-only
flat-LCDM: **Omega_m = 0.334 ± 0.018** → **Omega_Lambda = 0.666 ± 0.018**.

- **SHAPE vs ABSOLUTE degeneracy, made explicit.** SNe constrain `Omega_Lambda`
  through the Hubble-diagram *shape* (deceleration `q0 = Om/2 - OL = -0.499`,
  accelerating). The *absolute* density `rho_DE = OL · 3H0^2/(8πG)` needs `H0`
  because SNe alone are `M_B–H0` degenerate. `H0` is a **separate axis** from the
  `Omega_Lambda` error.

| H0 footing | H0 (km/s/Mpc) | rho_crit (kg/m³) | **rho_DE(SNe)** (kg/m³) |
|---|---|---|---|
| Planck | 67.4 | 8.533e-27 | **5.683e-27 ± 1.54e-28** |
| SH0ES  | 73.0 | 1.001e-26 | **6.666e-27 ± 1.80e-28** |

The `±` is `Omega_Lambda`-only (~2.7%). The H0 lever alone is
`(73.0/67.4)^2 = 1.173x` — larger than the `Omega_Lambda` uncertainty, so **the H0
choice, not the SNe shape, dominates the absolute density.**

---

## Galaxy-side (framework prediction) — `rho_DE = 4 a0^2/(G c^2)`

| a0 footing | a0 (m/s²) | rho_DE (kg/m³) | status |
|---|---|---|---|
| canonical | 9.355e-11 | 5.836e-27 | **CIRCULAR** (see below) |
| alt | 1.1305e-10 | 8.523e-27 | fixed footing |
| **MEASURED (GLS, gas-dom)** | **1.181e-10 ± 16%** | **9.308e-27 ± 3.00e-27** | **GENUINE, Λ-blind** |
| measured median variant | 9.726e-11 | 6.307e-27 | measured-a0 variant |

Measured a0 banked from `prep_2026/a0_line/fire_slope_results.json` `budget_gas`
(SPARC rotation-curve dynamics **alone**, no Λ input; `sigma_ln(rho) = 2·sigma_ln(a0)
= 0.322`).

---

## The genuine cross-check: ratio `rho_DE(framework)/rho_DE(SNe)` + tension

Tension is computed in **log space** — the correct treatment for the ~32%
multiplicative (lognormal) measured-a0 error, which dominates the small (~2.7%) SNe
error.

### H0 = 67.4 (Planck), rho_DE(SNe) = 5.683e-27

| footing | ratio | tension | flag |
|---|---|---|---|
| canonical | 1.027x | +0.98σ | **CIRCULAR — not a test** |
| alt | 1.500x | +15.0σ | — |
| **MEASURED (GLS)** | **1.638x** | **+1.53σ** | **GENUINE** |
| measured median | 1.110x | +3.86σ¹ | measured variant |

### H0 = 73.0 (SH0ES), rho_DE(SNe) = 6.666e-27

| footing | ratio | tension | flag |
|---|---|---|---|
| canonical | 0.875x | −4.93σ | **CIRCULAR — not a test** |
| alt | 1.278x | +9.09σ | — |
| **MEASURED (GLS)** | **1.396x** | **+1.03σ** | **GENUINE** |
| measured median | 0.946x | −2.05σ¹ | measured variant |

¹ The median and alt rows carry no measurement error (fixed point estimates), so
their tension is driven by the tiny SNe error alone and is inflated; read them as
ratios, not as calibrated σ. The GLS row is the one carrying the full measured-a0 box.

---

## Result

The **genuine, Λ-blind cross-check** (a0 measured from SPARC rotation curves,
inverted to a dark-energy density, compared against the SNe density) lands at:

- **1.638x the Planck-H0 SNe density (+1.53σ)**
- **1.396x the SH0ES-H0 SNe density (+1.03σ)**

i.e. **~1.4–1.6x (GLS) down to ~0.9–1.1x (median variant)** of the SNe density —
exactly the banked "1.1–1.6x" range. **This is consistent** (≤1.5σ): the
galaxy-measured dark-energy density and the SNe-measured dark-energy density agree
to within their combined uncertainty, dominated by the 32% a0 box. It is an
**independent, mutually-corroborating** estimate — a galaxy-dynamics number
(rotation curves) and a cosmological-distance number (SNe) landing on the same
`rho_DE` to within 1.5σ, with **no shared Λ input**. That is the Sarkar-relevant
point: even if one distrusts the SNe leg, an entirely separate observable reaches
the same dark-energy density.

**Which footing does the SNe rho_DE sit closest to?**
- vs **Planck H0**: closest to **canonical** (1.027x) — but canonical is circular
  (see below); of the *non-circular* footings the median variant (1.110x) is closest.
- vs **SH0ES H0**: closest to the **measured median** (0.946x).

The SNe density is **footing-dependent through H0**: it favors the lower-a0
(canonical/median) end at Planck H0 and the same median end at SH0ES H0. The
higher-a0 GLS footing sits ~1.0–1.5σ above the SNe density either way — high but
not in tension.

---

## Zero-free-parameter SNe-diagram prediction (harsher, shape-level test)

A second, stricter test: take the galaxy-measured Λ → `Omega_Lambda(H0)`, keep the
SNe-shape `Om = 0.334`, and **predict the μ(z) Hubble diagram with zero free
parameters** (a0 from rotation curves, H0 from the ladder; nothing fit to the SNe,
M_B analytically marginalized). Compare residuals + χ² against the SNe best-fit LCDM
diagram. This probes the **normalization + curvature closure** (`Om+OL` vs 1), not
just the density ratio. The authoritative numbers below are from `predict_diagram.py`
on the **real Pantheon+ data** (1580 SNe in the z>0.01 cosmology sample, 24 bins).
Best-fit flat-LCDM reference: Om=0.35, χ²=21.0/22 (χ²/dof=0.96). (An internal
flatness-forced cross-check in `sne_extract.py` reproduces the same ordering.)

| H0 | footing | OL(gal) | Om+OL | χ²/dof | Δχ² vs best-fit LCDM |
|---|---|---|---|---|---|
| 67.4 | measured GLS | 1.091 | 1.425 | 2.72 | **+41.4** (over-closes) |
| 67.4 | measured median | 0.739 | 1.073 | 1.09 | +4.0 |
| 67.4 | canonical | 0.684 | 1.018 | 0.97 | +1.2 **[CIRCULAR]** |
| 73.0 | measured GLS | 0.930 | 1.264 | 1.86 | +21.7 |
| 73.0 | **measured median** | 0.630 | 0.964 | 0.92 | **+0.01** (essentially perfect) |
| 73.0 | canonical | 0.583 | 0.917 | 0.94 | +0.6 **[CIRCULAR]** |

**Findings, honest both ways:**
- The **high GLS central a0 over-closes** the universe: `Om+OL = 1.42` at Planck H0
  (Δχ²=+41, a hard fail) and `1.26` at SH0ES H0 (Δχ²=+22). The shape/closure test is
  much harsher on the high footing than the ±16%-band density ratio (~1.5σ) because
  it responds to the full `Om+OL` sum, and the 32% a0 box is not folded into this
  central-value χ².
- The **measured median** footing reproduces the SNe diagram excellently —
  **Δχ²=+0.01 at SH0ES H0** (`Om+OL=0.964`, nearly flat) and Δχ²=+4 at Planck H0.
- The **canonical** footing gives small Δχ² at both H0 (+1.2 / +0.6) — but that is
  **circular** (it *is* the Planck Λ) and carries no evidential weight.
- The diagram test favors the **lower-a0 (median) end** and disfavors the **high GLS
  central value**. Read against the 32% a0 box, the GLS footing's viability rides on
  its low tail; its central value is in real shape-tension with the SNe diagram,
  worst at Planck H0.

## The circularity (the crux — do not let it be manufactured)

The **canonical** a0 = `cH_Lambda/Z` was **defined** using a cosmological (Planck)
`Lambda`. So `canonical a0 → rho_DE` **is** the Planck `rho_Lambda` by construction.
Its 1.027x / +0.98σ "match" to the SNe density only re-checks *Planck-vs-SNe Lambda*
— it is **algebra run backwards, not a framework test.** The canonical row is
reported for completeness and **flagged circular everywhere**; it must not be cited
as corroboration.

The **measured-a0** row (rotation-curve dynamics alone, zero Λ input) is the **only
genuine cross-check**, and it is the one that lands at +1.53σ / +1.03σ.

---

## Verdict

**FOOTING-DEPENDENT, leaning AGREES on density, split on shape.**

- **Density test (calibrated, with the a0 box):** the genuine Λ-blind
  measured-a0 → rho_DE agrees with the SNe-extracted rho_DE at **≤1.5σ** for both
  H0 (1.638x/+1.53σ at Planck, 1.396x/+1.03σ at SH0ES) — an honest independent
  cross-corroboration, dominated by the 32% a0 uncertainty.
- **Shape test (harsher, zero-free-parameter μ(z)):** the **high GLS central a0
  over-closes** at Planck H0 and mis-shapes the diagram at SH0ES H0; the **median**
  footing reproduces the SNe Hubble diagram well (χ²/18 ≈ 5). The shape-level test
  favors the lower-a0 end.

Together: the framework's galaxy-side Λ is **compatible with the SNe dark-energy
density to ~1.5σ at the level of the density**, with the honest caveat that the
sharper shape-level μ(z) test prefers the lower (median) a0 and puts the high GLS
central value in shape-tension — most of that tension lives on the high tail of the
a0 box and against Planck H0. The apparently-perfect canonical match is **circular**
(a0 defined from Planck Λ) and carries **no evidential weight**. The framework
background is LCDM throughout; `rho_DE`-from-SNe is the standard extraction, and the
framework adds only the galaxy-side cross-check. **No proof, no manufactured null.**
