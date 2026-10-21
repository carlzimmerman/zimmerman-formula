# A9 — the ΛCDM audit of the evidence chain, and a clean-data protocol

## Claim

Every headline number in the framework's evidence chain was computed on data that had
already been passed through a ΛCDM filter, and the filters are not all the same size.
Auditing the seven channels item by item, and recomputing on the data that are actually
on disk, the result is sharply split. **Three of the four headline numbers are not
ΛCDM-limited at all; the fourth is, but only through a parameter the record has already
marginalised. The priors that can actually move the other three are stellar, not
cosmological:**

- **κ = 1/2**: the H0 tension does *not* reach κ (the CMB-measured combination `Ω_Λ h²`
  makes κ exactly invariant under H0: 67.4 → 73 changes κ by 1.11e-16), but the stellar
  mass-to-light ratio does: `κ ∝ a0 ∝ Υ^-1.23`, so the Chabrier→Salpeter IMF bracket moves
  κ by a factor 1.98. **κ = 1/2 is an M/L statement, not a cosmological one.**
- **The shear Δχ² = +21.47/+23.85 (KiDS)**: freeing `Ω_m` with the covariance untouched moves
  it by −11.8 to +9.4 (DES Y3, the only shear ξ± with a full covariance on disk) — it cannot
  flip. Freeing `S8` takes it to +0.18, and that is already in the record. **This is the one
  number that is ΛCDM-limited, and the limiting parameter is σ8, which is already free in the
  published table.** The yardstick it is measured against (S0) is a separate, unquantified risk.
- **The 5.364× catchment**: the multiplier is a 1.20%-precision CMB measurement and the
  predicted excess is linear in it, so the number itself moves the excess by 0.005 dex.
  **Immune.** What is not immune is the framework's own postulate about *what fraction of
  the turnaround ball is available* (E = +0.715 or −0.000), which is A28, not ΛCDM.
- **The 1.45× red-lens excess**: replacing B21's ΛCDM distances with framework-native ones
  moves `A_red` from 1.451 to 1.536–1.686 — all one sign, none of it toward zero. The
  ΛCDM prior is *flattering* the framework here. The prior that can remove the excess is
  the stellar IMF (CFG926 R5, conditional).

The cleanest structural finding is about the RAR itself. **The RAR's slope, zero point
shape and scatter are prior-free, but `a0` is not: it is exactly degenerate with the
absolute distance scale, for every interpolation function, to machine precision**
(`a0 → a0/f` under `D → fD`, residuals identical to 1.44e-15). 55.43% of SPARC's galaxies have
distances from a Hubble flow at H0 = 73. The framework's `a0` therefore inherits an
H0-dependent zero point and an M/L-dependent zero point, and with the standard M/L it
lands at 1.1033e-10 m/s² — 17.87% above the canonical footing and 2.47% *below* the alt one.

## Derivation

**D1 (the RAR distance degeneracy is exact and law-independent).** Write any RAR as
`g_obs = g_bar φ(g_bar/a0)` with φ an arbitrary function (this covers ν_simple,
ν_standard, the RAR-exp, the canonical `g = (g_N/2)(1+√(1+4a0/g_N))`, and the quadratic
`g = √(g_N²+a0g_N)`). A distance rescaling `D → fD` sends `r → fr` and therefore
`g_obs → g_obs/f`, `g_bar → g_bar/f` (V_obs is a Doppler quantity and does not move).
Then
```
(g_bar/f) φ( (g_bar/f)/(a0/f) ) = (g_bar/f) φ(g_bar/a0) = g_obs/f ,
```
so the model with `(fD, a0/f)` reproduces the rescaled data *identically*. Every residual,
every rms, every slope is invariant; only `a0` moves, as `a0 ∝ 1/D`. ∎
Verified numerically on 155 curves / 2788 points: `a0·f/a0_0 = 1` to 1.335e-7 (fit
tolerance) and `Δrms = 1.44e-15 dex` (K2).

**D2 (κ and its two levers).** `κ = a0/(c√(Gρ))`. With `ρ = ρ_DE = 3Ω_ΛH0²/(8πG)`,
```
κ = a0 √(8π) / (c H0 √(3Ω_Λ)) .
```
Two ways to move H0: (i) hold `Ω_Λ` fixed → `κ ∝ 1/H0`, so H0 67.4→73 gives
κ: 0.4999 → 0.4615 (−7.67%); (ii) hold `Ω_Λ h²` fixed, which is what the CMB measures →
`Ω_Λ ∝ h^-2` and `κ ∝ 1/(h√(Ω_Λ)) = 1/√(Ω_Λh²)` is **invariant**. Measured: 1.11e-16 (K5).
The second is the physically correct one, so the Hubble tension does not propagate to κ.
The M/L lever is a separate and larger one: with `Υ_b = 1.4Υ_d` and a joint fit, the ridge
slope is `dln a0/dln Υ = −1.230` (K4), i.e. `κ ∝ Υ^-1.23`. Chabrier→Salpeter is +0.24 dex
in Υ (×1.74), hence ×0.506 in κ.
Which density you divide by is itself a ΛCDM choice: `ρ_DE/ρ_crit = Ω_Λ`, so
`κ_DE/κ_crit = √Ω_Λ = 0.8276`. The free SPARC fit gives 0.5893 (DE) or 0.4876 (total).
The same a0, two "κ"s, 20.85% apart, decided by which ΛCDM density is called "the" density.

**D3 (cluster η is a distance measurement only at second order).** At R500,
`η = (M500/Mbar)/ν(g_bar/a0)` and `g_bar = G Mbar/R500²`, `R500 = θ500 D_A`. The mass ratio
is distance-free; in the deep limit (`g_bar/a0 = 0.0369`, so ν ≃ √(a0/g_bar)) this gives
`η ∝ 1/D_A` via R500, or `η ∝ ρ_c^+1/3` via the overdensity definition at fixed M500. Both
are computed on 9830 eRASS1 clusters (K6): the largest lever over {Planck, DESI w0wa,
H0=73, Ω_m 0.25, Ω_m 0.40} is +7.95% (H0 = 73), the second route gives −0.10%, and **all
four levers are positive** — every cosmology in the bracket makes the cluster deficit
slightly *worse*, none of them better. η = 2.3335 needs a factor 2.33; the lever is 8%.

**D4 (Ω_m in the shear is one power per kernel).** `C_ℓ^{ij} = ∫dχ W_iW_jχ^-2 P(ℓ/χ)` with
`W_i = (3/2)Ω_m (H0/c)² (χ/a)∫n_i(χ')(χ'-χ)/χ' dχ'`, so at **fixed P(k)** every `C_ℓ`
carries exactly `Ω_m²` — one factor per leg — and nothing else except the χ(z) mapping.
Amplitude is therefore exactly degenerate with `σ8²`/`A_s`. This is why the K8 re-score
separates "amplitude held" from "amplitude profiled".

**D5 (the CMB ruler is not a late-time quantity).** `r_s = ∫ c_s dz/H(z)` from z* to ∞;
Λ contributes to H(z) only at z ≲ 3, where the integrand weight is ~1e-9 of the total.
Switching Λ off entirely changes r_s by 1.1e-10 (K7). r_s = 144.565 Mpc and
100θ_s = 100 r_s/χ(z*) = 1.0413 (Planck: 1.0410). The ruler is clean. What is *not* clean
is the step from θ_s to `Ω_m = 0.315, H0 = 67.4` — that step is a GR+ΛCDM+CDM fit, and the
framework imports its output as A25.

## The inventory: every ΛCDM-dependent number, and where it enters

| # | number | where it enters (file) | measured lever | verdict |
|---|---|---|---|---|
| a1 | D for 97/175 SPARC galaxies from `v/H0`, H0=73 + Virgo infall | `sparc_master_clean.csv` f_D=1; `sparc_data/*_rotmod.dat` | a0 −4.25% (K3); a0 ∝ 1/D exactly (K2) | shifts, cannot flip |
| a2 | inclinations, TRGB/Cepheid/UMa/SNe distances (78 galaxies) | same, f_D=2,3,4,5 | not ΛCDM; ladder zero point ~2–3% | clean |
| b1 | `Υ_3.6 = 0.5/0.7` fixed, Chabrier | `fable_independent_2026/L232_sparc_parameter_free.py:42,229` | `κ ∝ Υ^-1.23`; Υ=0.570 → a0_canon (K4) | **can flip κ** |
| b2 | 3.6 μm band choice | same | band is chosen to minimise SP variation; the normalisation is the IMF | clean in shape, not in scale |
| c1 | `Ω_m` in the lensing kernel | `CFG592/cfg592_like.py:28-43`, `cfg592_native.py:52-71` | Δχ² −11.8 / +9.4 (K8) | cannot flip |
| c2 | covariance (SSC from a ΛCDM P(k)) | `cfg592_like.py`, KiDS/DES releases | not separable on disk | stated |
| c3 | NLA intrinsic alignment, `A_IA` calibrated on ΛCDM sims | `cfg592_like.py` | marginalised in CFG592 | mostly absorbed |
| c4 | photo-z | `nz_source` in the 2pt file | z-calibration is spec-z based, not ΛCDM; z→χ is | small |
| c5 | HMcode-2020 × BAHAMAS feedback (A35) | `cfg590_shear.py:61-62`, `cfg592_like.py:42,59-67` | KiDS +21.6 → +16.8 | 25%, cannot flip alone |
| c6 | S0 = ΛCDM DM-only PM as the **yardstick** (A34) | `cfg530_analysis.py:197`, all CFG556/557/559 | defines Δχ² itself | **could flip the sign** |
| c7 | `S8`/amplitude (A24 σ8 = 0.811) | `cfg592_native.py:31-43` | +21.47 → +0.18 with S8 free | **flips, already disclosed** |
| d1 | eRASS1 M500 (WL-calibrated) and R500 = θ500 D_A | `real_research/data/_load_erass1.py`; `reviews/clusters_eta_audit.py` | η +7.95% worst case, all one sign (K6) | cannot flip (needs 2.33) |
| d2 | X-COP hydrostatic masses, (1−b) ≃ 0.80 | `real_research/data/xcop/xcop_r500_ettori2019.json` (13 clusters) | +25% in M → +25% in η, wrong direction | worsens, cannot flip |
| d3 | 500c overdensity uses ρ_c(z), i.e. E(z) | same | −0.10% (K6 route ii) | clean |
| e1 | `r_s` (the ruler) | `real_research/bridge1_linear_boltzmann.py`, `aest_cmb_consistency.py` | 1.1e-10 (K7) | clean |
| e2 | θ_s → `Ω_m, H0` (the inference) | A25 background, `cfg527_pm.py:84` | not separable; imports Planck's answer | the real CMB dependence |
| f1 | EH no-wiggle transfer function, `n_s=0.965, σ8=0.811, ω_b, ω_c` | `CFG527/cfg527_pm.py:84-86,120-137` | cancels at first order in ratio verdicts (A24); σ8 0.76 → ΔE +0.023/+0.006 | yardstick, mostly cancels |
| f2 | Zel'dovich ICs at `z_i = 49` | `cfg527_pm.py:88, 121-139` | same ICs for framework and S0 | cancels in ratios |
| f3 | `Δ_ta = 11.81` from a ΛCDM spherical-collapse ODE; NFW/Duffy; Tinker08; EPS histories | `cfg527_pm.py:142-171,310-378`; `cfg556/cfg515_lib.py` | A26/A31 QC: ΔE +0.106 / +0.281 | shifts E, cannot flip |
| g1 | `a0` from the RAR | L232; every SPARC lane | exactly degenerate with D; `κ ∝ Υ^-1.23` | **not prior-free** |

Two comments on the inventory. First, `cfg527_pm.py:28` states in its own header that
"EH ICs at z_i = 49 = the ONLY LCDM input". That is false: the same file fixes
`h, ω_b, ω_c, n_s, σ8`, `Ω_m, Ω_Λ, w0 = −0.838, wa = −0.62`, and takes `Δ_ta` from a ΛCDM
collapse ODE, and the register counts 17 ΛCDM-inherited items (A24–A40). The header should
not be quoted. Second, the register's own class counts already say this: 17 ΛCDM-inherited,
7 standard-MOND-inherited, 13 framework-derived (2 posited), 10 data-forced, 12 convention.
The audit below is a quantification of that register, not a discovery of new assumptions.

## Status

**NUMERICAL.** All ten checks pass on data on disk (175 SPARC curves, 9830 eRASS1 clusters,
DES Y3 ξ± with the full covariance). No new fitted constant is introduced.

## Checks (what `a9_checks.py` proves)

| id | what it proves | result |
|---|---|---|
| K1 | the galaxy chain's actual content | 175 curves, 2788 pts, 97 Hubble-flow (55.43% of galaxies, 59.22% of points) |
| K2 | `a0` is exactly degenerate with the distance scale | `a0 f/a0_0 = 1` to 1.335e-7; Δrms 1.44e-15 dex |
| K3 | the H0 73→67.4 lever on the Hubble-flow half | a0 −4.25% (1.1033e-10 → 1.0564e-10) |
| K4 | the M/L ridge | slope −1.230; Υ_d = 0.570 for a0_canon, 0.490 for a0_alt |
| K5 | κ under two H0 levers and under a free a0 | 0.4999 → 0.4615 (Ω_Λ fixed) or 0.4999 (Ω_Λh² fixed); free a0 → 0.5893 / 0.4876 |
| K6 | the cluster η lever | η = 2.3335; max Δη/η = +7.95%; second route −0.10% |
| K7 | r_s is Λ-free | 144.565 Mpc; Δ = 1.1e-10; 100θ_s = 1.0413 |
| K8 | Ω_m free on real shear data | Δχ² −11.8/+9.4 (amp profiled) vs +18.2/+33.8 (amp held); h lever +15.8/+33.6 |
| K9 | the 5.364 multiplier | 5.3643 ± 0.0646 (1.20%); elasticity 1.00 |
| K10 | the red-lens lever | 1.451 → 1.536–1.686 (cosmology); 0.079 of 0.127 dex (IMF) |

The mutation (`--mutate`) drops the distance factor from the baryonic side only — a
realistic bookkeeping slip. It breaks K2 (`a0 f/a0_0` falls to 0.7380; see `MUTATE.md`) and K3 (−11.08% instead
of −4.25%), and the script exits 1. Recorded in `MUTATE.md`.

## Ranked: the assumptions that could actually flip a conclusion

1. **Stellar IMF / 3.6 μm M/L (b1).** Flips κ by a factor 1.98 and removes 0.079 of the
   0.127 dex red-lens excess. *Re-analysis:* per-galaxy Υ with a hierarchical prior, plus an
   independent mass anchor (gas-dominated dwarfs where Υ is irrelevant, or resolved
   dynamical M/L). The repo already has half of this: CFG926 R5.
2. **S8 / the shear amplitude (c7).** Takes the KiDS Δχ² from +21.47 to +0.18. *Re-analysis:*
   joint (Ω_m, σ8) fit against the framework's own P(k) shape. Blocked by A59: the PM keeps
   too few ξ± points to be diagnostic.
3. **The S0 yardstick (c6).** The headline Δχ² is framework-minus-S0, i.e. a ratio to a
   ΛCDM DM-only simulation, not to the data. A yardstick error enters the verdict directly,
   because the yardstick is its denominator. *Re-analysis:* CFG592 native at a resolution that keeps most ξ±
   points (L ≥ 400 Mpc/h at N ≥ 1024).
4. **HMcode-2020 × BAHAMAS feedback (c5).** 25% of the shear Δχ². Cannot flip alone; adds
   to item 2.
5. **The supply fraction A28 / A23 (not ΛCDM).** E = +0.715 → −0.000 between the r_ta ball
   and the r200m ball. This is the largest single number in the halo-model claim, and it is
   a framework postulate. *Re-analysis:* measure the cold mass that actually crosses each
   host's edge (CFG595 did the first half: supply 1.5–3.6× larger than assumed).
6. **The hydrostatic bias (d2).** +25% in η, in the direction that *worsens* the cluster
   tension. Cannot flip.
7. Everything else (a1 distances, c1 Ω_m, d1/d3, e1, f1–f3, K9's 5.364): shifts a decimal.

## What this does not do

- It does not re-derive any framework result; it re-scores inputs.
- KiDS-1000 ξ± is **not on disk**; the K8 re-score is on DES Y3, which is. The KiDS
  headline is quoted from CFG592 and the DES lever is used as a *bound* on how far an Ω_m
  change could move a Δχ² of that size, not as a KiDS computation.
- The X-COP sample on disk is 13 clusters with R500/M500 only; the (1−b) lever is quoted
  from the literature, not recomputed.
- The N-body/transfer-function item (f1–f3) is not recomputed: doing so needs a PM rerun.
  The register's own QC numbers (A24, A26, A31) are quoted.
- The absolute χ² in K8 (1119.4 over 400 points) is **not** a goodness-of-fit: the model has
  no halofit, no baryons, no IA. Only χ² *differences* are used, and only as a sensitivity.
- It does not claim the framework is refuted, confirmed, or that any ΛCDM assumption is
  illegitimate. Several are unavoidable (the CMB inference, the transfer function). The
  point is which ones are load-bearing.

## Next — the clean-data protocol, in order

1. **Re-fit the RAR with Υ free and distances on one declared scale.** Report `(a0, Υ_d)`
   as a ridge, never `a0` alone: the pair is what the data measure. Fix the distance
   convention explicitly (SPARC's own H0 = 73 for the 97 Hubble-flow galaxies) and state
   the `a0 ∝ 1/D` scaling so any reader can move the answer to their H0. This alone removes
   the largest ambiguity in κ.
2. **Report κ on both densities, always.** `κ_DE` and `κ_crit` differ by √Ω_Λ = 0.828.
   Quoting one without the other is a convention choice presented as a measurement.
3. **Cluster η: declare the two distance routes.** Report η under (i) R500 = θ500 D_A and
   (ii) the overdensity definition, and quote the 8% bracket. Then state the (1−b) direction
   (+25%, against the framework) so the reader sees the tension is not a distance artefact.
4. **Shear: quote Δχ² at fixed and at free S8 side by side**, and quote Ω_m as free in the
   projection. Then the reader can see that the number is carried by the amplitude (σ8) and
   by the shape (R(k), feedback), and not by Ω_m.
5. **Red lenses: quote A_red at B21 distances, at the native h bracket, and after the IMF
   correction** — in that order, because the first two are cosmology and the third is
   stellar physics, and only the third moves it.
6. **Never quote `cfg527_pm.py:28`'s "only LCDM input" claim.** Replace it with the
   register's 17-item list. A one-line header is doing work that 130 lines of register
   contradict.
