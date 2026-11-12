> **Forward correction, 2026-11-12:** The projection, beam, flux units and universal detectability/shape conclusions below are superseded by [the corrected calculation](../../research_closure_2026_11_12/combined_route/gas_corrections/RESULT.md). The original body and frozen criteria remain historical. The corrected model and its outputs are in `correction_2026_11_12/` beside this file; the original script and outputs are unchanged. No guaranteed 100-sigma detection or universal mass-conservation exclusion is established.
>
> *Audit note, 2026-11-12 (lead session):* this notice was written by another session and is committed here on the owner's instruction after an independent check, `reviews/codex_corrections_audit_2026_11_12/C4_gas_signal_and_combined_route.md` (grade: CORRECT). The auditor recomputed the signal independently in SI on both footings and matched the corrected numbers to four digits. The folder `research_closure_2026_11_12/` it links to was not committed with it, so those links may not resolve; the audit file is the checked record. The committed text, labels and outputs below this notice are not edited by this commit.

# FINAL5 — the decisive observation: is the fixed column `Sigma_gas = a0/(pi G x_b^2)` there?

Observing proposal. Criteria frozen in `FROZEN_CRITERIA.md` (committed alone, before any script or
number). Arithmetic in `final5_signal.py` -> `final5_signal.out` / `.json`. TEST lane: adopts nothing,
relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10), never
pooled. Form B = the a0 law with cold dark energy counted once; kappa = 1/2 FITTED; not theory closed.

---

## 0. The one-line version

GAS1 left Form B's galaxy leg closed as an *argument* but not as a *measurement*: it needed a gas mass at
Mpc radii around isolated galaxies that nothing has measured. The observation that supplies it is a
**stacked thermal SZ measurement on a Compton-y map that is already on this disk**, around **17,335
KiDS isolated L\* lenses**. `y` is linear in the predicted column, immune to clumping, and — for a
fixed column — **flat in impact parameter out to 2.6 Mpc**, which is itself the discriminating shape.
The predicted plateau is `y = 1.76e-7 (kT/0.2 keV)`; the stack measures the column to **about 1 %
of the required value**, so either the plateau is there at ~100σ or the reading is dead by the same factor.

---

## 1. The target class

| item | value | provenance |
|---|---|---|
| Parent catalogue | KiDS-1000 / KiDS-DR4 bright lenses, `real_research/data/lensing_rar/lr_lenses.npz` | **ON DISK** |
| Candidates | **181,477** lenses over **1000 deg²**, z < 0.5 | **ON DISK** (GAS1 KA6) |
| Isolation criterion | **KO1 "host-free"**: reject any lens with a neighbour Δ = **0.3 dex** more massive in stellar mass inside a **comoving line-of-sight window W = 230 Mpc** (KO1's plain float tie rule); additionally veto any companion inside **F R_h** with **R_h = min(3 Mpc, sqrt(G Mgal / 1e-15))** | **ON DISK** (GAS1 FROZEN §3; `campaign_fresh_gravity/CFG96_kids_split_isolation.py` derives and re-runs the cut) |
| Veto factor F (primary) | **1.6** — the radius ONE1 graded KiDS at | **ON DISK** |
| Surviving sample P1 | **17,335** lenses (23 % of candidates) | **ON DISK** (GAS1 KA6; counts 40,667 / 25,708 / 17,335 at F = 1.0 / 1.3 / 1.6) |
| Redshift | median **0.308**; 5-95 pct **0.161 – 0.432** | **computed here** from `lr_lenses.npz` |
| Baryon mass `Mgal` (catalogue column; the repo's convention `Mgal = M*(1+f_cold)`) | median log10 = **10.674**; 5-95 pct **9.82 – 11.00** | **computed here** from `lr_lenses.npz` |
| Lensing-weighted `<M_b>` of the graded bins | **8.42e10 Msun** → `r_M = 11.20 kpc` → **`R_budget = x_b r_M = 65.9 kpc`** | **ON DISK** (GAS1 §2 table) |
| Brackets | F = 1.0, 1.3, 1.6; z = 0.05-0.20 and 0.20-0.43 | frozen |

**Why this class, in three sentences.**

1. **The requirement is radius-only.** GAS1's (L1) condition is `M_bar(<R) >= (a0/G) R²/x_b²`; nothing in the galaxy enters. So the test is purely "how much gas is at 0.3 → 2.6 Mpc", and the only thing that can ruin it is contamination by *someone else's* gas — which is exactly what the isolation cut removes.
2. **Isolation is not a nicety, it is the experiment.** Any neighbour, group, or filament supplies its own Mpc-scale gas. The KO1 host-free cut at Δ = 0.3 dex / W = 230 Mpc / 1.6 R_h is the strictest such cut the record has already run and reproduced exactly (GAS1 KA6, KO1 E7). It is also the same cut that produced the outer amplitudes GAS1's G4 gate relies on, so the sample is internally consistent with the anomaly being tested.
3. **L\* specifically, because it is where the prediction is not merely wrong but impossible.** GAS1 §8: at cluster scale the required column is *within a factor ~1* of X-COP's measured gas (0.37-1.26) — clusters cannot decide it. At L\* the requirement is 16x the *entire halo mass* inside 1 Mpc (see §4.1). Dwarfs sit at radii where no gas is measured either, but their smaller `r_M` pushes `R_budget` inward where the stellar contamination is worst.

**Pre-registered consequence of the geometry.** `R_budget = x_b r_M` with `x_b = 5.8888` gives 65.9 kpc (canonical) / 60.0 kpc (alt) for the representative lens — an order of magnitude *outside* the SPARC radii that fit the law, and safely *inside* the innermost graded radius here (0.3 Mpc). That is what makes the four-radius test clean: the prediction applies across all four, with no inner cutoff ambiguity.

---

## 2. The signal

### 2.1 The prediction in its cleanest form: `g_bar` is a constant

The requirement is only about the *enclosed baryon mass*, and in a spherical RAR `g_bar(R) = G M_bar(<R)/R²`. Inserting `M_bar(<R) = pi R² Sigma_gas`:

    g_bar(R) = pi G Sigma_gas = a0 / x_b^2 = 2.699196e-12 m/s^2   (canonical)
                                           = 3.262001e-12 m/s^2   (alt)

**So the reading demands a flat baryonic acceleration plateau of `a0/34.678` from ~66 kpc to 2.6 Mpc
around every isolated L\* galaxy.** Where KiDS measures the enclosed mass (and hence `M_bar`), it should
find `M_bar ∝ R²` there. This is the statement to test — it has no free normalisation, no free shape, and
no dependence on `M*`.

### 2.2 The two radial shapes I computed

* **PROFILE A — the required sheet.** `M(<R) = pi R² Sigma_gas` ⇒ `rho(R) = Sigma_gas/(2R)`, i.e. `rho ~ R^-1`. This is GAS1's own identification ("the profile is a uniform sheet: M ∝ R², rho_3D ∝ 1/R"). It is the only shape that holds the column constant, so it is *forced* by the budget condition, not chosen.
* **PROFILE B — a plausible hot halo.** `rho ~ R^-2` (the β ≈ 2/3 / outer `r^-2` behaviour measured in groups and clusters, quoted in `GO1/DATA_PLAN.md` from Matsushita+2025 β ≈ 0.4-0.65 and Bahar+2024), matched to A at `R_ref = 1 Mpc`.

**The dilemma (this is the argument, spelled out):** a flat column forces `rho ~ R^-1`, which at 0.3 Mpc is
**388x the cosmic mean matter density and 2483x the cosmic mean baryon density** — a mass concentration
no isolated L\* halo can hold. A normal halo shape with the same normalisation at 1 Mpc falls to
**0.77x the requirement at 2.6 Mpc**. There is no third shape, because the budget fixes the
normalisation *and* forces the slope to −1. Both branches are separately excluded; that is why the
measurement decides the amount question rather than merely constraining it.

### 2.3 The amplitudes (canonical / alt, `x_b^2 = 34.6781`)

Column: `Sigma_gas = 6.1627 / 7.4477 Msun/pc^2`. Densities below use PROFILE A, `rho = Sigma/(2R)`;
`R_out = 2.6 Mpc` (the minimum the reading requires — a larger sheet only raises `y` and `EM`).

| R (Mpc) | θ @ z=0.308 (′) | `rho` (kg/m³) | `rho` (Msun/Mpc³) | δ/ρ_b | δ/ρ_m | `n_e` (cm⁻³) |
|---|---|---|---|---|---|---|
| 0.3 | 1.06 | 6.953e-25 | 1.027e13 | 2483 | 388 | 3.65e-4 / 4.41e-4 |
| 1.0 | 3.55 | 2.086e-25 | 3.081e12 | 745 | 116 | 1.09e-4 / 1.32e-4 |
| 2.0 | 7.10 | 1.043e-25 | 1.541e12 | 372 | 58 | 5.47e-5 / 6.61e-5 |
| 2.6 | 9.23 | 8.023e-26 | 1.185e12 | 286 | 45 | 4.21e-5 / 5.09e-5 |

| R (Mpc) | `M_gas,req(<R)` (Msun) | in `M_b` | `N_e` flat (cm⁻²) | `y` @0.1 keV | `y` @0.2 | `y` @0.5 | ΔT_CMB @0.2 (µK) | `EM(b)` (cm⁻⁵) | `S_X` 0.5-2 keV @0.2 keV (erg/s/cm²/arcmin²) |
|---|---|---|---|---|---|---|---|---|---|
| 0.3 | 1.658e12 / 2.022e12 | 20 / 24 | 6.752e20 / 8.159e20 | 8.79e-8 / 1.06e-7 | 1.758e-7 / 2.124e-7 | 4.40e-7 / 5.17e-7 | −0.96 / −1.16 | 3.11e17 | 2.14e-14 |
| 1.0 | 1.928e13 / 2.331e13 | 229 / 277 | same | same | same | same | −0.96 / −1.16 | 7.53e16 | 5.19e-15 |
| 2.0 | 7.736e13 / 9.351e13 | 919 / 1111 | same | same | same | same | −0.96 / −1.16 | 2.19e16 | 1.53e-15 |
| 2.6 | 1.308e14 / 1.581e14 | 1553 / 1877 | — | — | — | — | — | 0 (edge) | 0 (edge) |

Units and conventions:
- `n_e = rho/(mu_e m_p)`, `mu_e = 1.14` (**repo convention, `go1.py` line 13**); standard text value 1.17-1.18 differs by ≤ 3 %.
- `N_e = ∫ n_e dl = Sigma_gas/(mu_e m_p)` — the *electron column*, i.e. the required surface density itself, in cm⁻².
- `EM(b) = ∫ n_e n_H dl`, `n_H = X_H rho/m_p`, `X_H = 0.76`; analytic closed form `EM ∝ arccosh(R_out/b)/b`, verified against quadrature to < 1e-5 (**KA5 PASS**).
- `y(b) = (sigma_T/m_e c²) kT_e N_e(b)`. **Linear in column. Independent of clumping. Flat for a sheet.**
- `ΔT_CMB = -2 y T_CMB`, `T_CMB = 2.7255 K`.
- `S_X = EM · Lambda / (4 pi (1+z)^4)` — the standard emission-measure conversion; `Lambda` is **from memory** (§6).

**The shape signature, which does not need `Lambda` at all:**
`EM(b) ∝ arccosh(R_out/b)/b`, i.e. **`S_X ~ b^(-1)`** (computed ratios: 4.12 / 1.00 / 0.29 at
0.3 / 1 / 2 Mpc — a pure `b^-1` law would give 3.33 / 1.00 / 0.30), while **`y` is flat**
(identical to the printed precision at 0.3, 1 and 2 Mpc). A normally-shaped hot halo gives
`S_X ~ b^(-2)` to `b^(-3)` and `y` falling as `b^(-0.5)` to `b^(-1)`. The flattening of `y` is the
cleanest possible discriminator because it is a *prediction of the budget condition itself*, and it
survives an unknown temperature normalisation.

### 2.4 Integrated quantities (for quoting against the literature)

| `R_out` (Mpc) | L_X (0.5-2 keV, erg/s) | F_X at z = 0.308 (erg/s/cm²) |
|---|---|---|
| 1.0 | 1.149e44 | 3.497e-9 |
| 2.0 | 2.297e44 | 6.994e-9 |
| 2.6 | **2.986e44** | **9.092e-9** |

For scale (**from memory**): real isolated L\* galaxies have diffuse `L_X(0.5-2 keV) ~
1e39-1e41 erg/s`. The reading requires ~3e44 from *every one of them* — a rich-cluster X-ray
luminosity in an object that X-ray surveys have looked at repeatedly and not seen.

---

## 3. Instrument and exposure

### 3.1 Primary: **ACT DR6.02 needlet-ILC Compton-y map (LAMBDA)** — **ON DISK**, no new telescope time

| field | value | provenance |
|---|---|---|
| Files | `/Users/carlzimmerman/new_physics/_external_data/act_dr6_nilc/strip_ComptonY.f32be` (829,785,600 B) and `strip_ComptonY_deproj_cib_1.0_10.7.f32be` | **ON DISK** |
| Headers / geometry | `header_ComptonY.fits`, `header_ComptonY_deproj_cib_1.0_10.7.fits`, `strip_geometry.txt` | **ON DISK** |
| Grid | 43200 × 10320 CAR, CDELT = 0.0083333 deg = **0.5 arcmin/pixel** | **ON DISK** (FITS header, printed in `final5_signal.out`) |
| Strip | rows 3239-8040 ⇒ **Dec −36° to +4°** — the KiDS-S footprint; lens catalogue and map overlap by construction | **ON DISK** |
| **Beam** | **1.6 arcmin FWHM** Gaussian | **ON DISK** (`FETCH_LOG.md`) |
| Citing | Coulton et al. 2024, PRD 109, 063530 + the DR6.02 release | **ON DISK** |
| Exposure requested | **None.** Archival. | — |

**Why this instrument settles the amount question and the X-ray cannot, on its own:** `y` is *linear* in
the electron column and therefore in `Sigma_gas` directly, with (i) no `<n²>` clumping bias, (ii) no
cooling-function or metallicity dependence, and (iii) a *predicted flat plateau* whose flatness is a
parameter-free consequence of the budget condition. X-ray SB is quadratic in density, so it is both
clumping-biased in the direction that *mimics* the signal and steeply radius-dependent.

**Noise — taken from disk, not memory.** GO1's own measured stacked y error, printed in
`closure_2026_11_10/GO1_group_outskirts/go1.json` (`primary/full/sig_at/2.83/Gy`):
`sigma(M_gas^y) = 6.9e12 Msun` for the shell 1 → 2.83 R500 (aperture radius 1.868 Mpc), N = 102,
z_med = 0.143. For a flat column the enclosed mass is `pi R² Sigma`, so that error *is* a column
error: `sigma(Sigma) = 6.9e12/(pi × 1.868²) = 6.294e11 Msun/Mpc² = 0.102 × Sigma_gas (1σ)`.
Scaling as `1/(theta_ap sqrt(N))` to P1 (N = 17,335, z = 0.308, D_A = 968 Mpc):

| R (Mpc) | θ (′) | beams in aperture | `sigma(Sigma)/Sigma_gas` | S/N if the plateau is real |
|---|---|---|---|---|
| 0.3 | 1.06 | 1.2 | 0.0879 | 11 |
| 1.0 | 3.55 | 13.6 | 0.0264 | 38 |
| 2.0 | 7.10 | 54.6 | 0.0132 | 76 |
| 2.6 | 9.23 | 92.3 | 0.0101 | 99 |

So: **the stack measures the projected column to ~1 % of the requirement at the outermost radius.**

**Honest limitation, priced in now.** At z = 0.308, R = 0.3 Mpc subtends 1.06′ — *below* the 1.6′
ACT beam. The inner point is beam-limited at the median lens. Pre-registered fix: (i) quote the
beam-convolved prediction there (computed: the smearing suppresses the spherical reading by 8 % and
leaves the flat reading unchanged, since a plateau convolves to a plateau), and (ii) grade the 0.3 Mpc
point on the lowest-redshift third of P1 (z ≲ 0.245, where 0.3 Mpc > 1.5′).

### 3.2 Secondary: **SRG / eROSITA eRASS1 DR1** — archival, *not* downloaded

- The 50-tile plan covering GO1's own 11 DE-footprint groups is priced at **726,234,784 bytes (0.73 GB)**; central tiles alone 154 MB; exposure maps ~32 MB per band per tile (`GO1/DATA_PLAN.md`, **ON DISK**).
- Scaled to the full KiDS footprint (mean tile 14.5 MB over 10.67 deg² unique ⇒ 1.36 MB/deg²): **≈ 1.4 GB of events**, **≈ 3.0 GB of exposure maps for one band** over 1000 deg².
- **Depth:** eRASS1 gives GO1's groups **80-210 s**. That is too shallow for any single system at 3-5 R500 (GO1's own judgement, flagged as such there), but it is exactly what a **17,000-object stack** needs.
- **Request to the owner:** approve the ~1.4 GB event fetch (+ ~3 GB expmap) for the KiDS-S footprint. No proprietary data.

### 3.3 Tertiary / confirmatory (all facility numbers **from memory**)

- **O VII (21.60 Å) and O VIII (18.97 Å) absorption** against background AGN — linear in column, and the only channel that gives temperature *and* column for the *cooler* phase. **Athena X-IFU** (or its US successor **LEM**, or **XRISM/Resolve** for the brightest few sight lines).
- **FRB dispersion measure** through isolated L\* haloes (currently limited by the number of well-localised FRBs behind isolated hosts; **CHORD/DSA-2000/CRAFTS** counts from memory).
- Neither is graded here — no O VII survey or FRB catalogue for isolated L\* hosts is on disk.

---

## 4. Systematics

### 4.1 The non-systematic: the reading is already physically impossible at 0.3-1 Mpc

An L\* halo of `M200 ~ 1.2e12 Msun` **[memory]** can hold at most `Omega_b/Omega_m × M200 ~ 0.16 M200
~ 1.9e11 Msun` of baryons *in total*. The reading requires, in **gas alone**:

| R (Mpc) | required gas (Msun) | required / 0.16 M200 |
|---|---|---|
| 0.3 | 1.658e12 | 8.7 |
| 1.0 | 1.928e13 | 101 |
| 2.0 | 7.736e13 | 407 |
| 2.6 | 1.308e14 | 688 |

This needs no instrument model, no foreground subtraction and no temperature prior. It is
mass conservation, and it is why the *measurement* (rather than more theory) is the right next
move: the answer is already over-determined, and the proposal exists to make that explicit and
auditable.

### 4.2 Systematics that could MIMIC the signal (false positive for the reading)

| # | systematic | direction | pre-registered control |
|---|---|---|---|
| X1 | **CIB / dusty star-forming galaxies** correlated with the lens sample leaking into the y map | positive | Run on **both** `ComptonY` and `ComptonY_deproj_cib_1.0_10.7`; the lane reports a verdict only if the two agree. GO1 already ran this bracket. |
| X2 | **2-halo term**: undetected neighbours/filaments supply Mpc-scale gas, not the lens | positive | Repeat in z = 0.05-0.20 vs 0.20-0.43 and at veto F = 1.0 / 1.3 / 1.6 R_h. Require the null **N2 random-minus-random** ≈ 0. |
| X3 | **Unmasked AGN / X-ray binaries** in the lens or along the LOS | positive | Mask on the eRASS1 point-source catalogue (GO1 already uses a y mask); re-run with a doubled mask radius. |
| X4 | **Galactic soft foreground** (Local Hot Bubble, Galactic corona, eROSITA bubbles) | positive (X-ray) | Hard-band-minus-soft-band test; restrict to |b| > 30° (GO1's DATA_PLAN flags the inner-Galaxy sight lines). |
| X5 | **Clumping** `C = <n²>/<n>²` (2-3 at these radii **[memory]**) | **positive in X-ray, ZERO in SZ** | This is precisely why the SZ is primary: any X-ray excess above the SZ-predicted column *is* clumping, and it is measured, not assumed. |
| X6 | **Non-thermal / inverse-Compton** contamination of the y signal | positive | Bulbul+2026 quote a residual non-thermal component ~30 % of the thermal flux **[memory]** — treat 30 % as the mimickable ceiling and require the signal to exceed it. |

### 4.3 Systematics that could HIDE the signal (false negative)

| # | systematic | direction | pre-registered control |
|---|---|---|---|
| H1 | **Beam dilution** at small θ (inner radius) | negative | Use the computed beam-convolved prediction; grade 0.3 Mpc on the low-z third. |
| H2 | **ILC / needlet filtering** removing the large-scale plateau — the signal is smooth and extends to ~9′, exactly the scales an ILC suppresses | negative | Re-run with GO1's gNFW beam/filter correction ON and OFF; require < 25 % difference at 1 Mpc (bracket B2). Also cross-check against an independently produced y map (**[memory]**: Planck NILC / MILCA). |
| H3 | **Temperature prior**: `Sigma_meas ∝ 1/T_model`. A hotter halo *hides* the column | negative | Evaluate at kT = 0.1 / 0.2 / 0.5 keV; label must agree at all three (bracket B7). This is the single largest freedom in the proposal. |
| H4 | **Metallicity / cooling function** for the X-ray leg | ±0.5 dex | Quote EM (astrophysics-free) as the primary X-ray number; flux is secondary. |
| H5 | **Outer truncation**: `y` and `EM` depend on where the sheet ends (∝ arccosh(R_out/b)) | negative | Always quote R_out = 2.6 Mpc, the *minimum* the reading requires. Every larger R_out increases the signal. |
| H6 | **Stellar-mass bias**: the record's fitted mass factor k = 2.0-2.8 (ONE1) would raise the requirement by `sqrt(k)` | strengthens the kill | Reported, not applied — it only makes the exclusion stronger. |
| H7 | **Redshift / distance errors** | ± | Frozen catalogue; no refitting of z. |

---

## 5. The pre-registered decision rule

### Primary statistic `S1`

    f_col  ==  M_gas,meas(< R_ref = 1 Mpc)  /  M_gas,req(< 1 Mpc)
    M_gas,req(<R) = (a0/G) R^2 / x_b^2  -  M_star  =  pi R^2 Sigma_gas - M_star
    M_gas,req(<1 Mpc) = 1.928e13 Msun (canonical) / 2.331e13 Msun (alt)

Obtained by deprojecting the stacked, beam-corrected ACT DR6 Compton-y profile around P1 with the
frozen T model (GO1 Part A pipeline; `onion_A`).

### The two numbers

| outcome | condition |
|---|---|
| **KILL** the missing-baryon reading on the galaxy leg | **`f_col <= 0.10`** with the +3σ bound still `<= 0.10` |
| **KEEP** the reading (it survives to the next test) | **`f_col >= 0.50`** with the −3σ bound still `>= 0.50` |
| **NO VERDICT** | anything else, or any bracket/null below fails |

**Why 0.10 is the kill line.** GAS1 runs the requirement two ways: the law-driven route (L1), which needs `pi R² Sigma_gas`, and the *footing-free, data-driven* route (L3), which needs only `M_3D,obs/6.41 − M_b`. Across the record's own KiDS bins the ratio is **L3/L1 = 0.02 to 0.11**, and it is footing-independent to within 25 %. So 0.10 is exactly the level below which **even the cheapest escape in the record fails** — the gas cannot supply L3, and a fortiori cannot supply L1.

**Why 0.50 is the keep line.** It is the literal mirror of the condition CRUX.md registered *before* GAS1 reported: "if GAS1 finds that the gas on disk can supply less than half of the 11.0x, then form B's halo is not the cold charge." Supplying at least half keeps the reading inside the record's own survival condition.

### Secondary statistic `S2` (shape — kills independent of temperature)

Fit `S_X ~ b^(-gamma)` over 0.3-2.6 Mpc (equivalently `y ~ b^(1-p)` with `gamma = 2p - 1`).
**Predicted: `gamma = 1.00`, `y` flat.**

| outcome | condition |
|---|---|
| **KILL** (normalisation-independent) | **`gamma >= 1.5` at ≥ 3σ** — the column falls faster than `b^(-0.25)` and cannot sustain the required flat column to 2.6 Mpc |
| **KEEP** | `gamma <= 1.25` at ≥ 3σ **and** `f_col >= 0.50` |
| **NO VERDICT** | otherwise |

### Brackets — a verdict counts only if **all** pass

| # | bracket |
|---|---|
| B1 | CIB: both y maps give the same label |
| B2 | Beam/filter: with and without GO1's gNFW correction agree within 25 % at 1 Mpc |
| B3 | Environment: same label in z = 0.05-0.20 and z = 0.20-0.43 |
| B4 | Purity: same label at veto F = 1.0, 1.3, 1.6 R_h |
| B5 | Nulls: GO1's N1 cross-shear and N2 random-minus-random both pass |
| B6 | Mocks: GO1's 200-mock bias test satisfies \|bias\| <= 0.3 sd |
| B7 | Temperature: same label at kT = 0.1, 0.2, 0.5 keV |

Fail any ⇒ `NO VERDICT` for that footing. One label per footing; if they differ, both are printed
and the difference is named.

---

## 6. Provenance — what is on disk, what is mine, what is from memory

**Computed here from files on disk.**
- The KiDS lens catalogue `lr_lenses.npz` (181,477 rows; z and `Mgal` percentiles are computed here).
- Every constant is quoted from a repo file and printed in SI in `final5_signal.out`: `a0` (canonical/alt), `G`, `x_b^2 = 34.6781`, `R_b = 5.41`, `mu_e = 1.14` and `sigma_T` (both `go1.py` l. 13), `rho_b = 6.205e9` and `rho_m = 3.975e10 Msun/Mpc^3` (from `omega_b`, `omega_d`, h in `go1.py` l. 15 / R541B / PAR1 A2).
- GO1's measured y-gas table and its errors, quoted from `RESULT.md` / `go1.json` (ON DISK). **Independent check: this lane's scaling of GO1's own printed error reproduces GAS1's published +8.0 σ shortfall at x = 2.83 exactly.**
- eRASS1 tile sizes and depth, from `GO1/DATA_PLAN.md` (ON DISK); tile geometry, beam and citation from `_external_data/act_dr6_nilc/FETCH_LOG.md` (ON DISK); the ACT grid from its FITS header (ON DISK).
- GAS1's law-driven requirements and its X-COP cluster comparison (ON DISK, `HY4-1_.../RESULT.md`); `<M_b> = 8.42e10 Msun` and `r_M = 11.20 kpc` from GAS1 §2 table (ON DISK).
- Known answers: **KA1, KA2, KA3, KA5 all PASS** (Σ, `g_bar = a0/x_b²` to 1e-12, `M_req` cross-check against GAS1's bin-3 value 3.234e13 → 3.186e13, and the EM closed form against quadrature). **KA6 was not verifiable here** (it needs CFG96/CFG110 stacked-shear files and exact cut reproduction) — recorded as unverified, not as a pass.

**Explicitly from memory (not on disk anywhere in this repo):**
1. The APEC-like soft-band (0.5-2 keV) cooling function, `Lambda = 5.0e-23 / 3.0e-23 / 1.2e-23 erg cm^3 s^-1` at kT = 0.1 / 0.2 / 0.5 keV, Z = 0.2 Z_sun. **Dominant systematic on the X-ray flux.** The EM column is independent of it.
2. The fiducial outer-halo / WHIM temperature, **kT = 0.2 keV**. Bracketed by 0.1 and 0.5 keV (bracket B7).
3. L\* halo scaling used for the mass-conservation check, **M200 ≈ 1.2e12 Msun**.
4. Typical observed diffuse `L_X(0.5-2 keV) ~ 1e39-1e41 erg/s` for isolated L\* galaxies.
5. Typical clumping factor **C ≈ 2-3** in outer halos.
6. Published ACT DR6 per-beam y noise **~1e-5** — used only as a cross-check; the graded noise is rescaled from GO1's own printed error (ON DISK).
7. All future-facility numbers: Athena X-IFU, LEM, XRISM/Resolve, CMB-S4, Simons Observatory, CHORD/DSA-2000.
8. Real L\* hot-halo gas masses at Mpc radii — **the quantity this proposal exists to measure**.

**My modelling choices, flagged.**
- `R_out = 2.6 Mpc` as the outer edge of the sheet: the reading requires the column out to *at least* the last KiDS bin, so this gives the **minimum** predicted signal.
- Profile A taken as **spherical** (`rho = Sigma/(2R)`), following GAS1. Under the alternative "uniform projected sheet" reading (`Sigma_proj = Sigma_gas` exactly, no 1/R spherical extension), `y` is smaller by a factor 1.61 at 1 Mpc; both are printed, and **the flat/nearly-flat shape holds in either reading**, which is what makes the shape test robust.
- Profile B's slope `p = 2` is a representative outer-halo slope, not a fit.
- `z_ref = 0.308` (catalogue median) for all angular conversions; the beam limitation at 0.3 Mpc is disclosed above.
- The ACT per-beam noise used for S/N is rescaled from GO1's measured stack error at N = 102 and a 1.868 Mpc aperture via `sigma ∝ sqrt(Omega)/sqrt(N)`; this assumes map-noise (not sample-variance) domination, which is why brackets B3 and B5 are mandatory.

---

## 7. How to run it (the executable part of the proposal)

Everything below uses files that exist on this disk. No new data, no new telescope time.

**Step 0 — reproduce this lane's numbers (seconds, ~50 MB).**

    cd /Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/FINAL5_measurement
    python3 -I final5_signal.py            # -> final5_signal.out / .json
    python3 -I final5_signal.py --mutate   # -> final5_signal_MUTATE.out

**Step 1 — build the P1 lens list** (17,335 lenses) by re-running the KO1 host-free cut:
`Delta = 0.3` dex, `W = 230 Mpc` comoving line-of-sight window, KO1 float tie rule,
veto `1.6 R_h` with `R_h = min(3 Mpc, sqrt(G Mgal/1e-15))`. Reference implementation and the
counts to reproduce: `campaign_fresh_gravity/CFG96_kids_split_isolation.py` and GAS1 `KA6`
(40,667 / 25,708 / 17,335 at F = 1.0 / 1.3 / 1.6). **This step is the only place a
verification could fail in this lane: I quote the counts rather than regenerate them.**

**Step 2 — stack the ACT y map** on P1 using GO1's machinery unchanged:

    # template/geometry/beam/CIB/mocks, all already exercised
    closure_2026_11_10/GO1_group_outskirts/go1_measure.py   <kids column dir> <checkpoint.npz>
    closure_2026_11_10/GO1_group_outskirts/go1.py               <checkpoint.npz>

    # map: /Users/carlzimmerman/new_physics/_external_data/act_dr6_nilc/strip_ComptonY.f32be
    #      and strip_ComptonY_deproj_cib_1.0_10.7.f32be   (bracket B1)
    # 43200 x 10320 CAR, 0.5 arcmin/pix, 1.6 arcmin beam, rows 3239-8040 = Dec -36..+4 deg

**Step 3 — deproject to the enclosed gas mass** `M_gas(<R)` with GO1's `onion_A` and the frozen
`T(R) = T500 x^-0.6` (bracket B7: also kT = 0.1 and 0.5 keV flat), then form

    f_col = M_gas,meas(<1 Mpc) / 1.928e13 Msun     (canonical)
    f_col = M_gas,meas(<1 Mpc) / 2.331e13 Msun     (alt)

**Step 4 — report the label** from the frozen table (KILL ≤ 0.10 at ≥3σ / KEEP ≥ 0.50 at ≥3σ /
NO VERDICT otherwise), **after** brackets B1-B7 and nulls N1, N2 have each passed. Any bracket
failure forces NO VERDICT regardless of f_col.

**What is staged but not fetched:** the eRASS1 DR1 event tiles covering the KiDS-S footprint
(≈1.4 GB events + ≈3.0 GB per band of exposure maps, scaled from GO1's priced 0.73 GB for 50
tiles / 11 groups). Fetching these is the owner's call; the SZ result does not depend on it.

**Cross-checks that would raise confidence without changing the design:** an independently
produced y map (Planck NILC / MILCA **[memory]**); and a positive control — rerun the identical
stack on GO1's 102 eRASS1 groups, where the pipeline is known to detect gas at 2σ in the
1 → 2.83 R500 shell. A pipeline that fails its own positive control cannot produce a kill.

---

## 8. What this lane does NOT do

- It does not grade the theory, adopt a label, or register a result. Form B's labels stand.
- It does not download anything, including the eRASS1 tiles whose price is quoted here.
- It does not select radii, veto factors, temperatures or aperture sizes after seeing numbers —
  all are frozen in `FROZEN_CRITERIA.md`.
- It does not claim the missing-baryon reading is excluded by *measurements of isolated galaxies*,
  because those measurements do not exist yet. It makes the case that they are the only thing left,
  prices the experiment, fixes the decision rule in advance, and states plainly which inputs are
  from memory (`Lambda(T,Z)`, `kT = 0.2 keV`, `M200 ≈ 1.2e12 Msun`, typical L\* `L_X`, clumping
  `C ≈ 2-3`, the published ACT per-beam noise, and every future-facility number).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
