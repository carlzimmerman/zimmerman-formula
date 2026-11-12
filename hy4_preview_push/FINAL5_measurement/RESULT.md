# FINAL5 RESULT — the decisive observation is *runnable today, with archival data*

TEST lane, quarantined. Criteria committed alone **before** this script and **before any number**
(`FROZEN_CRITERIA.md`). Adopts nothing, relabels nothing, registers nothing. Form B = the a0 law
with cold dark energy counted once; kappa = 1/2 FITTED; not theory closed. Footings canonical and
alt, never pooled.

---

## 1. Answer first

The observation that closes the amount question is **not** a new instrument and **not** a new
exposure. It is a **stacked thermal Sunyaev-Zel'dovich measurement in the ACT DR6.02 needlet-ILC
Compton-y map already on this disk** (`/Users/carlzimmerman/new_physics/_external_data/act_dr6_nilc/`),
centred on the **17,335 KiDS host-free isolated L\* lenses** the record has already built, run
through **GO1's existing Part A pipeline** which already stacks KiDS shear *and* this y map with
randoms, jackknife errors, a gNFW beam correction, two CIB treatments and three nulls.

**What makes it decisive** is that `y` is *linear in the very quantity the budget fixes*:

    y(b) = (sigma_T / m_e c^2) kT_e * N_e(b),     N_e(b) = Integral n_e dl = Sigma_proj(b) / (mu_e m_p)

`N_e` **is** the required surface density, in cm^-2. There is no clumping factor, no `<n²>` bias, and
in the budget-forced (`rho ~ R^-1`) reading the plateau is **flat in b**. And there is a sharper
form still: because `g_bar = G M_bar(<R)/R²`, the fixed column is exactly the statement

    g_bar(R) = pi G Sigma_gas = a0 / x_b^2 = 2.699196e-12 m/s^2   (canonical), 3.262001e-12 (alt)

— **a parameter-free flat baryonic-acceleration plateau from ~66 kpc to 2.6 Mpc.**

**The amount:** a straight stack of 17,335 lenses measures the projected gas column to
**~1 % of the requirement at 2.6 Mpc** (σ(Σ)/Σ_gas = 0.0101) and **~9 % at 0.3 Mpc**
(0.0879, beam-limited). If the column is real, this is a ~100σ detection; if it is not, the
reading is dead by the same factor. There is no outcome in between.

## 2. The numbers

    Sigma_gas = a0/(pi G x_b^2),  x_b^2 = 34.6781
      canonical 1.287355e-02 kg/m^2 = 6.1627 Msun/pc^2
      alt       1.555779e-02 kg/m^2 = 7.4477 Msun/pc^2
    R_budget = x_b r_M = 65.9 kpc (canonical) / 60.0 kpc (alt) for <M_b> = 8.42e10 Msun

| R (Mpc) | θ @0.308 (′) | `rho` (Msun/Mpc³) | δ/ρ_b | δ/ρ_m | `n_e` (cm⁻³) | `M_gas,req` (Msun) | `N_e` (cm⁻²) | `EM` (cm⁻⁵) | `y` @0.2 keV | ΔT_CMB (µK) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.3 | 1.06 | 1.027e13 | 2483 | 388 | 3.65e-4 | 1.658e12 | 6.75e20 | 3.11e17 | 1.76e-7 | −0.96 |
| 1.0 | 3.55 | 3.081e12 | 745 | 116 | 1.09e-4 | 1.928e13 | 6.75e20 | 7.53e16 | 1.76e-7 | −0.96 |
| 2.0 | 7.10 | 1.541e12 | 372 | 58 | 5.47e-5 | 7.736e13 | 6.75e20 | 2.19e16 | 1.76e-7 | −0.96 |
| 2.6 | 9.23 | 1.185e12 | 286 | 45 | 4.21e-5 | 1.308e14 | — (edge) | 0 | 0 | 0 |

- `n_e`, `EM`, `y` canonical; **alt = ×1.2086 in `n_e`, `N_e` and `y`; ×1.461 in `EM` and `S_X`.**
- `S_X` (0.5-2 keV, z = 0.308, `Lambda = 3.0e-23` **[memory]**): `2.14e-14` / `5.19e-15` / `1.53e-15`
  erg s⁻¹ cm⁻² arcmin⁻² at 0.3 / 1 / 2 Mpc; **total L_X ≈ 3.0e44 erg/s, F_X ≈ 9.1e-9 erg/s/cm²**
  within 2.6 Mpc — a rich-cluster X-ray luminosity from every isolated L\* galaxy.

**Detectability** (noise rescaled from **GO1's own printed stacked error**, ON DISK):

| R (Mpc) | θ (′) | beams | σ(Σ)/Σ_gas | S/N if real |
|---|---|---|---|---|
| 0.3 | 1.06 | 1.2 | 0.088 | 11 |
| 1.0 | 3.55 | 13.6 | 0.026 | 38 |
| 2.0 | 7.10 | 54.6 | 0.013 | 76 |
| 2.6 | 9.23 | 92.3 | **0.010** | **99** |

## 3. The existing data already point that way

GO1's ACT-y stack of **102 eRASS1 groups** (M500 ~ 1e14 — **~10x an L\* halo**, so expected to carry
*more* gas, not less) supplies `f_col = 0.187 ± 0.102` of the requirement at R = 1.87 Mpc, a deficit of
**+8.0σ**; the deficit reaches **+13.3σ** at 7.46 Mpc. Against the only Mpc-scale electron densities
in the repo (Bulbul+2026, 827 groups, quoted in `GO1/DATA_PLAN.md`), the required column is over by
**2.5x (+5.7σ) at 0.9 Mpc** and **10.5x (+26σ) at 1.9 Mpc**.

That is **not yet inside the frozen kill region** (0.19 ± 0.10 sits +0.9σ above the 0.10 line), and it is
groups, not isolated galaxies. Both facts are the reason to run P1 rather than declare victory.

## 4. The dilemma the measurement resolves

The budget condition fixes the *normalisation* and forces the *slope* (`rho ~ R^-1`):

- **Flat column** ⇒ `rho ~ R^-1` ⇒ **2483x the cosmic mean baryon density at 0.3 Mpc**, and a gas mass inside
  1 Mpc of **101x** the total baryons an L\* halo can hold. Impossible.
- **Normal halo shape** (`rho ~ R^-2`) matched at 1 Mpc ⇒ **0.77x the requirement at 2.6 Mpc**, and it
  over-supplies at 0.3 Mpc, which GAS1's amplitude gate (G4) shows drives the outer points to 0.03-0.04
  of the law. Short.

No third shape exists. Both branches are excluded by measurements already on disk; the P1 SZ stack makes
that exclusion explicit at the radii where it counts.

## 5. Known answers, mutations, disclosure

- **KA1 PASS** — Σ_gas reproduces GAS1's 6.1627 / 7.4477 to <1e-3.
- **KA2 PASS** — `pi·G·Sigma_gas = a0/x_b^2` to 1e-12 (both footings).
- **KA3 PASS** — `M_gas,req(R)` formula reproduces GAS1's bin-3 law-driven value (3.234e13 → 3.186e13).
- **KA5 PASS** — analytic EM (`arccosh(R_out/b)/b`) matches quadrature to <1e-5.
- **KA6 NOT VERIFIED IN THIS LANE** — the host-free counts (40,667 / 25,708 / 17,335) are quoted from
  GAS1; reproducing them needs the CFG96/CFG110 stacked-shear files and the exact cut code.
- **MUTATE: 4 of 4 arms run** — M1 (a0 × 10) scales Σ and M_req by exactly 10.000; M2 (ρ ~ R^-2 halo)
  gives the 7.01 / 2.01 / 1.00 / 0.77 enclosed-mass ratios; M3 shows clumping C = 3 raises X-ray
  `S_X` by 3 and leaves `y` unchanged; M4 round-trips the noise model against GO1's own printed error.
- **Disclosed limitations:** ACT's 1.6′ beam is larger than θ(0.3 Mpc) = 1.06′ at the lens median
  redshift (graded on the low-z third instead); `Lambda(T, Z)` is from memory (±0.5 dex on X-ray flux only);
  the sheet's outer edge `R_out` is not predicted — 2.6 Mpc is the *minimum*, so all `y`/`EM` values are lower
  bounds; the S/N scaling assumes map-noise domination, which brackets B3/B5 test.

## 6. Files

`FROZEN_CRITERIA.md` (committed alone, first) · `final5_signal.py` → `final5_signal.out` / `.json` ·
`final5_signal_MUTATE.out` · `PROPOSAL.md` (the write-up) · this file.
One thread, seconds, well under 3 GB; the 48 GB ACT blackbody map and the 16 GB shear catalogue were not read.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
