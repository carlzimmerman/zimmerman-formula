# GAS1 FROZEN CRITERIA: is form B's amount problem a missing-baryon problem?

Committed alone, before any GAS1 script exists and before any GAS1 number is computed.
TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), **never pooled**.
kappa = 1/2 FITTED; not theory closed. The cold component is a gravitating field component, never a particle.

---

## 0. The question, and why it is the last open flank

AMT1 (`closure_2026_11_10/AMT1_amount_budget/AMOUNT_BUDGET.md`) closed the arithmetic of the amount: form B's halo
needs a share `X_s = 59.5 M_b` to pass KiDS host-free (ONE1), the cosmos holds `5.41 M_b` per baryon
(`Omega_c/Omega_b`, F1A / R541), and the record's own dynamics deliver 1.06-1.40 M_b (COL1 / VSH1). The share is
11.00x the entire cosmic budget.

`fable52_push/README.md` section 5 names the one thing that would move it: **"a measured gas mass at Mpc radii
around isolated galaxies"**, and records the observation that motivated it: with B21's own hot-gas estimate put into
`g_bar`, B21's published outer points drop from **1.50 to 0.47** of the law. So the reading to be killed or kept is:

> **The mass the law demands at 0.6-3 Mpc is not missing cold charge. It is real baryons (a hot circumgalactic
> medium) that B21's `g_bar` never counted.** If it is, the amount problem dissolves: the "cold" remainder is small,
> the share is inside 5.41 M_b, and nothing has to be assembled that the cosmos does not have.

This lane computes, on both footings and bin by bin, the gas column that reading needs, and grades it against every
gas constraint on disk.

**What has been seen before freezing (disclosure).**
- AMT1's whole table (the demand, the budget, the delivered charge, the budget radius `x_b = 5.8888`).
- KO1's published numbers: per-bin host-free amplitudes, `R_s`, the veto-radius table, and R6 (B21's tables:
  KiDS-bright isolated 1.50 +- 0.08; GAMA isolated 0.97 +- 0.28; hot gas 0.47 +- 0.04).
- ONE1's published numbers: the share 59.4861 / 59.5029 M_b, the fitted mass factor `k` (2.0-2.8), and its
  rejection of `X = 5.41` at +4.85 / +4.93 sigma.
- GO1's published group gas census (`closure_2026_11_10/GO1_group_outskirts/RESULT.md`): the stacked
  `M_exc` (lensing), `y`-gas and `M_b` table at x = 1..16 R500, R500 = 0.66 Mpc.
- The column names and shapes of the staged lensing files and of B21's tables.
- **Not seen / not computed:** any per-bin gas column, any required-gas number, the B21 gas-to-stellar ratio
  extracted from the two files, any X-COP gas mass at MW mass, and the value of any kill ratio below.
- **Hand estimate (mine, before freezing, to be checked and not trusted):** the reading fails on two independent
  lines, the amount (the gas needed exceeds the baryons in the same volume by 2-3 orders of magnitude) and the
  amplitude (gas that large over-predicts the outer signal and pushes it below the law). I expect
  **MISSING BARYONS EXCLUDED [AMOUNT AND AMPLITUDE]**. If the amplitude line does not fire, say so.

---

## 1. Inputs (all on disk; nothing is downloaded)

**The record's KiDS stage** (`real_research/data/lensing_rar/`, git-ignored):
- `lr_lenses.npz`: the 181,477 W10 lenses (`ra, dec, z, logM, Mgal, typ, chi`).
- `cfg110_perlens.npz`: per-lens tangential sums `WG`, weights `WW`, counts `NN`, in the 15 `g_bar` bins.
- `cfg96_stack.npz`: the 50 jackknife patch labels.
- `KiDS_DR4_brightsample.fits` + `KiDS_DR4_brightsample_LePhare.fits`: the galaxy catalogue (1,239,422 objects).
- `brouwer2021_rar/`: B21's published tables and covariances. Used here:
  `Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt` (no gas), `Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt` (B21's hot gas),
  `Fig-9_RAR-KiDS-isolated_Massbin-{1..4}.txt`, `Fig-3_Lensing-rotation-curves_Massbin-{1..4}.txt`,
  `brouwer2021_rar_README.txt` (the column definitions and B21's own `g_obs = 4 G ESD/bias` conversion, and the
  statement that the data are 1000 deg^2 of KiDS-1000). The multiplicative bias is applied as its README states.

**Other constraints read from the repo, never recomputed:**
- `closure_2026_11_10/GO1_group_outskirts/RESULT.md` (the measured group gas census; values quoted in section 5).
- `closure_2026_11_10/AMT1_amount_budget/AMOUNT_BUDGET.md` (the demand/budget arithmetic it is the flank of).
- `_external_data/xcop_thermo_2026_11_02/` (X-COP temperature profiles; used only as a stated extrapolation).

**Not on disk, and said so where used:** eROSITA/eRASS1 X-ray event files (GO1's `DATA_PLAN.md` prices the download
at 0.73 GB and finds the depth too shallow); any measured hot-gas mass at Mpc radii around isolated galaxies
(this is the flank itself); B21's provenance for their hot-gas model (their paper is not on disk; the *effect* of
their gas is, and it is extracted from the two tables).

---

## 2. Constants, the same on both footings unless stated

    G     = 6.674e-11 m^3 kg^-1 s^-2      (KO1's / ONE1's convention)
    Msun  = 1.989e30 kg ; Mpc = 3.0857e22 m ; kpc = 3.0857e19 m ; pc = 3.0857e16 m
    c     = 2.998e8 m/s ; H0 = 70e3/Mpc s^-1 for comoving distances (the record's DC)
    a0    = 9.3603e-11 (canonical) / 1.1312e-10 (alt) m/s^2

    Budget      R_b   = Omega_c/Omega_b = 5.41            (F1A / R541 / AMT1)
                S_b   = 1 + R_b = Omega_m/Omega_b = 6.41
                x_b   = sqrt(R_b * S_b) = sqrt(5.41*6.41) = 5.8888   (the radius, in r_M, where the budget is spent)
                x_b^2 = 34.6781
    Cosmology   h = 0.674, omega_b = 0.02236 (canonical) / 0.02234 (alt), omega_d = 0.1209
                                                                     (R541B / PAR1 A2 / AMT1's own constants)
                Omega_b = omega_b/h^2 ; rho_crit = 3 H0^2/(8 pi G) with H0 = h*100 km/s/Mpc
                rho_b   = Omega_b rho_crit   (printed in kg/m^3 and Msun/Mpc^3)

    Law (form B, the record's form)   g_N = G M_b/r^2 ; g = nu(y) g_N ; nu(y) = 1/2 + sqrt(1/4 + 1/y) ; y = g_N/a0
                r_M = sqrt(G M_b/a0) ; x = r/r_M ; X(x) = (sqrt(1+4x^2)-1)/2 = nu(1/x^2) - 1
                M_c(<r) = M_b X(x)                     (EQUATIONS.md sec. 6, AMT1's DEMAND)

    Amplitude line   0.891 = 10^-0.05                  (the record's KiDS gate line, KO1's LINE)

---

## 3. Lens sets, bins and radii (the record's own, unchanged)

**Outer bins.** `O = [0,1,2,3]`, the four lowest `g_bar` bins of `cfg110_perlens.npz`
(edges 1.0000e-15, 1.7644e-15, 3.1131e-15, 5.4928e-15, 9.6915e-15 m/s^2). These are B21's four lowest bins, the
16 points SWT1 E3 put outside the wall and the bins KO1 graded.

**Lens set P1 (primary).** KO1's host-free cut, `Delta = 0.3` dex, `W = 230` Mpc, KO1's plain float tie rule, veto
radius `F R_h` with **F = 1.6** — the radius ONE1 graded KiDS at, because KO1 A2/E7 showed the frozen 1.0 R_h veto
leaves a tapered edge inside the graded range. `R_h,l = min(3 Mpc, sqrt(G Mgal_l/1e-15))`. Expected 17,335 lenses
(KO1 E7 / ONE1 KA6). **Fallback, disclosed if used:** if the catalogue scan fails or exceeds 900 s, P1 becomes the
full W10 set (181,477) and every P1 number is labelled as W10.
**Reported, not graded:** F = 1.0 (40,667) and F = 1.3 (25,708); the W10 set.

**Cell radii.** KO1's convention exactly: for lens `l` and bin `k` the annulus is
`[R_lo, R_hi] = [sqrt(G Mgal_l/g_hi), min(sqrt(G Mgal_l/g_lo), 3 Mpc)]`. Per bin, three radii are reported:
the WW-weighted mean of the area-weighted mean radius, the WW-weighted geometric mean of `R_lo R_hi`, and
`R_eff = sqrt(<R^2>_area)` (the radius whose point-mass `g_bar` equals the bin's area-averaged `g_bar`).
`R_eff` is the one used for the mass accounting, because it is the radius at which `G M_b/R^2` equals the bin's
mean `g_bar`.

**Measured amplitude.** KO1's estimator unchanged: `D_k = 4 G (sum WG)/(sum WW)`, `M_k` the law's stack model at
catalogued `Mgal`, `s_k` the delete-one-patch jackknife error of `D_k` for that set, 50 patches;
`A = sum(D_k M_k/s_k^2)/sum(M_k^2/s_k^2)`, its error the delete-one-patch jackknife of `A` with `s_k` held fixed.

---

## 4. What is computed (in this order; each step printed before the next)

### Step 1 - the demand, bin by bin, per footing
Per lens `l`, per bin `k`, the area-weighted mean over the annulus of
`M_c,law(<R) = M_b X(x(R))`, `x = R/r_M(M_b)`, `M_b = Mgal_l` (catalogued; the bracket `k_fit * Mgal` with ONE1's
fitted `k` is reported, because ONE1 showed the inner window asks for 2.0-2.8x the catalogued mass).
Stacked with `WW`. Reported per bin and footing: `<M_b>_W`, `<X>_W`, `<M_c,law>_W` (kg and Msun), and
`<M_c,law>_W / (5.41 <M_b>_W)` — the demand over the budget, which is the number AMT1 computed at fixed radii and
this lane computes on the record's own lensing bins.

### Step 2 - the gas column the reading needs
Two independent lines. They are not the same number and both are graded.

**(2a) LAW-DRIVEN (per footing; the primary, because it is what "bring the law's requirement inside the budget"
means).** The demand is inside the budget at radius `R` iff `X(x) <= 5.41` iff `x <= x_b` iff
`M_bar(<R) >= (a0/G) R^2 / x_b^2`. So the extra baryons required inside `R` are

    M_gas_req(R) = (a0/G) R^2 / x_b^2  -  M_star(<R)                     [kg]        ... (L1)

which is positive only beyond `R_budget = x_b r_M(M_star)`. Differentiating,
`dM/dR = 2 (a0/G) R/x_b^2`, so the gas is a **constant-surface-density** addition:

    Sigma_gas = (1/(2 pi R)) dM/dR = a0/(pi G x_b^2)                      [kg/m^2]   ... (L2)
    canonical 9.3603e-11/(pi*6.674e-11*34.6781)  ;  alt with 1.1312e-10
    (constant in R: a uniform sheet from R_budget outward)

Reported per bin: `M_gas_req` at `R_eff`, `Sigma_gas`, the mean column `M_gas_req/(pi R_eff^2)`, and the 3D density
`3 M_gas_req/(4 pi R_eff^3)`. `M_star(<R)` = the lens's `Mgal` (the record's convention: `Mgal = M*(1+f_cold)`,
so the cold ISM is already in it; this makes the requirement *smaller*, i.e. conservative).

**(2b) DATA-DRIVEN (footing-free; the bracket that does not assume the law holds).** From the measured `D_k`, the
enclosed projected mass within `R` is `M_2D = 2 pi R^2 DeltaSigma` (the isothermal `s = 1` conversion, which is the
law's own cold profile at these radii: `rho_c ∝ 1/r^2`); bracketed with the point-mass `pi R^2 DeltaSigma`.
Converted to a 3D sphere mass with the isothermal factor `2/pi` (bracket: 1). Then, requiring
`M_cold <= 5.41 M_bar` with `M_bar = M_star + M_gas`:

    M_gas_req(<R) = M_3D,obs(<R)/6.41  -  M_star(<R)                                  ... (L3)

### Step 3 - B21's own gas, measured from the two tables on disk
For each mass bin `m` and each of Fig-3's 15 physical radii `R_j`:
- `ESD_j` = Fig-3_m's `ESD_t` at `R_j` (the measurement; identical in both RAR versions).
- `g_bar_nogas(R_j)` = Fig-9_m's `g_bar` at which its `ESD_t` equals `ESD_j` (log-log interpolation; both
  sequences are monotone in the outer range - checked and printed).
- `ratio(ESD) = g_bar_hot(ESD)/g_bar_nogas(ESD)`, from the **unbinned** pair Fig-4 (hot gas) against
  Fig-4-5-C1 (no gas), each inverted at the same `ESD` (i.e. at the same radius).
- `M_star,m(<R_j) = g_bar_nogas(R_j) R_j^2/G`; `M_gas,B21(<R_j) = (ratio - 1) M_star,m(<R_j)`.
**Stated approximation:** the `ratio` profile comes from the unbinned sample and is applied per mass bin as a
function of `ESD`, a monotone proxy for radius; the mass-bin radii are exact. The extraction is validated by KA5
(it must reproduce the published 1.50 -> 0.47 drop) and reported with the four mass bins separately.

### Step 4 - the amplitude consequence (the line that decides whether the reading *helps*)
Put the Step-2a gas into `g_bar`: `g_bar' = g_bar (1 + M_gas_req/M_star)`, recompute the law's model
`nu(g_bar'/a0) g_bar'` per cell with the same area weighting, and recompute `A` against the **unchanged** data `D`.
This is the outer amplitude form B would show if the amount problem were solved by baryons. Graded against 0.891.

---

## 5. Kill conditions (pre-registered; a kill fires only if it holds in **every** outer bin)

Let `M_req(R)` = Step-2a's `M_gas_req`, and `M_obs(R)` the measured 3D enclosed mass at `R`.

**G1 - AMOUNT, the sphere's own baryons.**
`Q1(R) = M_req(R) / [rho_b (4/3) pi R^3]`. Even if *every* baryon in the universe inside that sphere were swept
into the galaxy, this is all there is.
*Fires if `Q1 > 3` in all four outer bins, on the footing.*

**G2 - AMOUNT, the mass that is actually there.**
`Q2(R) = M_req(R) / M_obs(R)`. Gas cannot outweigh everything.
*Fires if `Q2 > 1` in all four outer bins, on the footing.*

**G3 - AMOUNT, measured gas, two regimes.**
- **G3a (the KiDS radii):** `Q3a = M_req(R_eff) / M_gas,B21(R_eff)` with B21's gas interpolated at the same radius.
  *Fires if `Q3a > 1` in all four outer bins, on the footing.* (No error is available on B21's gas; the line is a
  factor, and the factor is reported.)
- **G3b (the group radii, the only *measured* gas at Mpc radii in the repo):** GO1's stacked census, at each
  `x = 1, 1.41, 2, 2.83, 4, 5.66, 8, 11.3, 16 R500` with `R500 = 0.66 Mpc`, `M_gas` and its jackknife error,
  against `M_req(x R500)` (which depends on `R` alone, not on the halo - that is the point of (L1)).
  *Fires if `M_req - M_gas >= 3 sigma` at every `x >= 2.83`.*
- X-COP: reported as a **stated extrapolation** to MW mass only (X-COP is cluster-scale); it is not a graded line,
  because the extrapolation is mine and is not a measurement at these radii.

**G4 - AMPLITUDE.** `A_gas` from Step 4 with its jackknife error.
*Fires if `A_gas + 2 s < 0.891` on the footing.* (The record's KiDS gate line, KO1's `LINE`.)

**G5 - CONSERVATION, global (reported, graded only if it fires by more than 3x).**
`n_lens` = the comoving number density of the W10 lenses, computed as `N / (Omega_survey * V(z < z_max))` with
`Omega_survey = 1000 deg^2` (B21's README, on disk) and the record's `DC`. This is a **strict lower bound** on the
true space density (flux-limited, and 23 % of candidates pass isolation), so `n_lens * <M_req>` is a lower bound on
the gas density the reading needs; compared with `rho_b`.

---

## 6. Label (per footing, on the primary lens set P1)

| condition | label |
|---|---|
| any known answer in section 7 fails | **NO VERDICT** (the failing KA is named; the row it feeds is NOT EVALUABLE) |
| no kill fires | **MISSING BARYONS CAN CLOSE IT** |
| G1 or G2 or G3 fires, G4 does not | **MISSING BARYONS EXCLUDED [AMOUNT]** |
| G4 fires, G1/G2/G3 do not | **MISSING BARYONS EXCLUDED [AMPLITUDE]** |
| G4 and (G1 or G2 or G3) fire | **MISSING BARYONS EXCLUDED [AMOUNT AND AMPLITUDE]** |
| G4 does not fire and G1/G2/G3 do not fire but G5 > 3 | **MISSING BARYONS EXCLUDED [GLOBAL]** |

The same label is reported for the bracket `k = k_fit` (ONE1's fitted mass factor) and for the veto radii 1.0 and
1.3 R_h. If the label differs between the two footings, both are printed and the difference is named.

---

## 7. Known answers (all must pass, else NO VERDICT)

- **KA1.** `X(x) = nu(1/x^2) - 1` to 1e-12 over `x` in [1e-3, 1e4].
- **KA2.** `X(x_b) = 5.41` to 1e-12 with `x_b = sqrt(5.41*6.41)`; and `x_b = 5.8888` to 1e-4 (AMT1's number).
- **KA3.** The constant-column identity (L2): numerical `d M_req / d(pi R^2)` equals `a0/(pi G x_b^2)` to 1e-6.
- **KA4.** The fixed point of (L1): with `M_bar = M_star + M_req(R)`, the law's own share `X(R/r_M(M_bar))` equals
  **5.41** to 1e-9, on both footings, at every R. (This checks the algebra and the code, not the physics: it is the
  statement that (L1) is exactly the budget line.)
- **KA5.** The B21 pipeline: this lane's own amplitude code on B21's four lowest `g_bar` points gives
  **1.50 +- 0.08** for `Fig-4-5-C1` and **0.47 +- 0.04** for `Fig-4` (KO1 R6), on the canonical footing, to the
  quoted 1-sigma. Errors from the published covariance diagonal, bias-corrected. (If the alt footing is used the
  values scale; both are printed, the canonical is the one graded.)
- **KA6.** The host-free counts: 40,667 / 25,708 / 17,335 at F = 1.0 / 1.3 / 1.6 (KO1 E7, ONE1 KA6).
- **KA7.** The per-lens sums reproduce `cfg96_stack.npz` for W10 to 1e-9 relative (KO1 KA1).
- **KA8.** The masses B21's tables imply, `M_star(<R_j) = g_bar R_j^2/G`, are non-decreasing in `R_j` and lie
  inside the published mass-bin edges `log10(M*/(h70^-2 Msun))` = [8.5,10.3], [10.3,10.6], [10.6,10.8],
  [10.8,11.0] at the outer radii, for every mass bin.
- **Null.** The cross-shear amplitude of the P1 set over `O` (`cfg116_perlens.npz`) is within 2.5 s of zero.

## 8. MUTATE (separate output files; each must bite, and any that does not is disclosed)

- **M1 (budget).** `R_b` set to 5.41e4. `M_req` must fall to <= 0 at every graded radius and **no kill may fire**;
  the label must become **MISSING BARYONS CAN CLOSE IT**. (Shows the kills are driven by the budget, not by the
  radii.)
- **M2 (data).** The outer-bin `WG` of the P1 set x 0.1. `M_req` from (L3) must fall by >= 5x, and G4's `A_gas`
  must rise. (Sensitivity, not a verdict flip; reported as such.)
- **M3 (footing / a0).** `a0` x 10 on the law-driven line: `M_req` from (L1) must rise by exactly 10.000 (1e-9) and
  `Sigma_gas` by exactly 10.000, while (L3) and every data-side number are unchanged to 1e-12.
- **M4 (the gas itself).** B21's gas (Step 3) replaced by the amount-fixing gas `M_req` in `g_bar`, and the
  amplitude recomputed: it must fall below 0.891 by more than 2 s. (This is G4, run the other way round, as a
  mutation of the *input* rather than a graded consequence.)

## 9. Compute and provenance

One thread, under 4 GB, under 15 minutes. The 16 GB shear catalogue is **not** read.
Every number in the result is either (i) computed here from the staged files, (ii) quoted with its file from
another lane's published `RESULT.md` / note, or (iii) explicitly flagged **FROM MEMORY** or **EXTRAPOLATION**.
No number is carried from memory silently.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
