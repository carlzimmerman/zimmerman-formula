# Can existing data prove (or strengthen) a0 = (c/2)√(Gρ)?

*9-route workflow + adversarial verify; C.Z. independently verified the load-bearing Z-identity subtlety: the chain a0=(c/2)sqrt(G rho)=cH/Z, Z=2sqrt(8pi/3)=5.789 is EXACT only for ONE (rho,H) pair -- (rho_crit,H0)->a0=1.13e-10 OR (rho_Lambda,H_Lambda)->a0=9.36e-11. The framework value uses rho_Lambda+H_Lambda; mixing rho_Lambda with the full H0 gives Z=7.0. Headline confirmed: universality (a0 set by a uniform cosmic density, local excluded at >10sigma) is the genuine strengthening; NOT causal proof (needs z~3).*


*An honest ledger. Constants used: c = 2.998×10⁸ m/s, G = 6.674×10⁻¹¹; ρ_Λ = 5.83×10⁻²⁷, ρ_crit = 8.5×10⁻²⁷ kg/m³. All on-disk numbers below re-derived on the real SPARC (175 *_rotmod.dat + Lelli2016c.mrt) and eRASS1 (9830-cluster) data; algebra re-checked in sympy; literature re-fetched from primary sources.*

---

## 1. The honest headline

**No — existing data cannot PROVE the relation in the causal sense.** What it can do, and does do strongly, is establish two distinct, weaker claims:

- **VALUE-CONSISTENCY (established, but a coincidence):** a0 ≈ (c/2)√(Gρ_Λ) = **9.35×10⁻¹¹ m/s²** matches the observed a0 (9.1×10⁻¹¹ simple-μ → 1.20×10⁻¹⁰ McGaugh-RAR) to ~20%. This is a match of the *present-epoch value only* — numerically identical to Milgrom's 40-year-old a0 ≈ cH₀/6, which ΛCDM reproduces with no causal link. The prefactor c/2 (equivalently Z = 5.789) is a posited, **underived** coefficient (the repo's own number-field work shows it is not entropy-derivable; the closest *derived* value is Verlinde's 6). So this is an unfixed-freedom match, **not causation**.

- **UNIVERSALITY (genuinely established now, real evidence):** a0 is **one uniform number** across 175 SPARC galaxies (factor ~1100 in baryonic surface density, ~5 dex in mass) and across every independent determination method, with intrinsic scatter ≤ 0.057 dex (Li & McGaugh 2018). A *uniform* a0 selects a **uniform cosmic density source** (consistent with ρ_Λ) and **excludes a local/environmental density source** (the ρ_local fork, which would make a0 ∝ √ρ_local). This is provable today and the strongest existing-data argument.

**What existing data CANNOT do** is show a0 *tracks* ρ as ρ *changes* — the only test that distinguishes "a0 is set by ρ_Λ" from "a0 is some other universal constant near that value." That requires the a0(z~3) deep-MOND evolution measurement, which is telescope-limited (~2027). Claiming the present universality + value-match amounts to "proof" is exactly the manufacturing trap. **This ledger asserts consistency + universality, not proof.**

A critical algebraic honesty point: the chain "a0 = (c/2)√(Gρ) = c²/(2R\*) = cH/Z with Z = 2√(8π/3) = 5.789" is **exact only when ρ = ρ_crit = 3H²/8πG** (the H's cancel — it is a Friedmann tautology with zero data content). With ρ = ρ_Λ, cH₀/a0 = **7.00**, not 5.789 (off by 1/√Ω_Λ); the framework's reading uses H_Λ ≡ H₀√Ω_Λ, for which cH_Λ/a0 = 5.789 holds and a0 = 9.35×10⁻¹¹ is recovered to machine precision (I verified this). The two equalities are not *simultaneously* true at the literal value cH₀/a0 with the full H₀ — a framing subtlety that must not be glossed.

---

## 2. The ledger table

| Test | Data used | What it shows | Proves: value / universality / environment / causal | The honest caveat |
|---|---|---|---|---|
| **Algebraic coverage** | sympy (exact) | a0=(c/2)√(Gρ)=c²/(2R\*) exact; Z=cH/a0=2√(8π/3)=5.78881 **for ρ=ρ_crit only**; R\* is the free-fall length c·t_dyn, NOT a horizon (R\*(ρ_Λ)≈50.8 Gly > 46 Gly particle horizon) | *(definitional — not a test)* | Z is a Friedmann tautology of the *form*; carries zero data content. The c/2 coefficient is posited, not derived. |
| **Value cross-check** | Planck/DESI ρ_Λ → a0_pred vs my fit to 175 real SPARC curves | Cosmology hands a0 = 0.94×10⁻¹⁰ (±1%); my SPARC fit recovers 1.13–1.21×10⁻¹⁰. Gap +20–29%, inside the μ-interpolation systematic band | **value** | Single-epoch value-coincidence. The +29% gap is real for McGaugh-μ; simple-μ (0.93×10⁻¹⁰) agrees to ~1%. The "consistency" uses the 0.26×10⁻¹⁰ μ-systematic as the denominator. |
| **a0 census** (8 methods) | 175 SPARC (my fit) + Begeman, McGaugh16, Li18, BTFR, KiDS lensing, Gaia wide binaries, dSph | 8 methods cluster at a0 = 1.19±0.11×10⁻¹⁰, dispersion of centers ~5%, across ~6 dex in mass & all environments | **universality** | z=0 SNAPSHOT. ~3 methods *adopt* 1.2 (shared convention); true independent N≈5. ρ_crit (1.13e-10) is marginally closer than ρ_Λ — snapshot is structurally blind to which ρ. |
| **Universality scatter → f-bound** ⭐ | 175 SPARC RAR (143 fit by me) + Li18 0.057 dex | SPARC spans factor ~1100 in surface density yet a0 uniform → local-density fraction of a0²: **f ≤ 0.33** (Li18 intrinsic), **f=1 disfavored at ~3×** | **universality / environment** | **Corrected down from the original "f≤0.19, ~5×"** — that used the wrong deep-MOND propagation factor (0.5 vs the correct 0.25). My direct per-galaxy scatter (0.30 dex) only excludes f=1 at ~1.1×. The tight bound rests on Li18's 0.057 dex, which is an *upper limit* on intrinsic. |
| **Environmental slope** ⭐ | 175 SPARC per-galaxy a0 vs **independent Spitzer** SBdisk/SBeff | d log a0 / d log SB = **+0.097 ± 0.036** (my re-derivation) → **11σ below** the +0.5 the local-ρ fork demands; consistent with 0 | **environment (genuine new)** | Robust to estimator choice on the *full +0.5 exclusion*, but a deep-MOND median estimator gives a small persistent **+0.09 to +0.11 (~3σ above 0)** — so "exactly 0" is not robust, only ">10σ below +0.5" is. Mild shared-photometry circularity (Vdisk ← same Spitzer light as SB). |
| **Environment correlation** (UMa + NED) | 175 SPARC + 21 Ursa-Major members (fD=4) + NED 3D k-NN density (122 gal, 6.4 dex range) | UMa-vs-field Δlog a0 = **−0.04 dex** (my re-derivation; p>0.6); NED slope −0.01±0.015 → +0.5 local fork excluded | **universality / environment (genuine new)** | NULL. UMa is a *loose, low-density* cluster (~5% Virgo), so the "10× contrast" is not established; signals **below ~0.1–0.15 dex are NOT excluded**. NED proxy is coarse (heterogeneous, distance-limited sample). |
| **Cluster reinterpretation** | 9830 real eRASS1 clusters (RA/Dec/z/M500/Mgas/R500) | Environment-vs-MOND-residual partial correlation = +0.004 (NULL); a0_eff vs ρ_gas slope **−0.41** (WRONG sign vs +0.5); density-a0 does not close the cluster discrepancy | **environment (null) / consistency** | A NULL for the local-density "cluster fix," not a win for any reading. The ~factor-2 MOND cluster shortfall (I recover the raw factor ~12 missing mass) stays **unsolved** — inherited from MOND, shared not distinctive. TEST-B slope is ~half real, half a built-in Mgas coupling. |
| **a0(z) bridge** | DESI w0waCDM ρ_DE(z) + repo KMOS3D/KROSS | Framework predicts a0(z=3)/a0(0) ≈ 0.74 (mild decline) under √ρ_DE; ~flat under ΛCDM | **causal (partial — the cosmology half)** | The a0(z) *measurement* half does not yet exist at z~3. **MUSE-DARK III (2026) measures a0 RISING** (a0(z~1)=2.38e-10, slope +1.59z, faster than H(z)) — a face-value tension with the declining reading, caveated by 3D-forward-model/pressure systematics. |
| **Wide-binary local-vs-cosmic** | Gaia wide-binary onset (Chae/Banik) + a0=(c/2)√(Gρ) counterfactual | Local fork predicts MOND transition at ~300–940 AU; observed deviation onsets at the *cosmic* scale (g_N≈a0 at ~5–9 kAU) → local fork excluded | **environment** | The original "2000 AU = cosmic a0" claim was numerically wrong (~24×); g_N=a0 is at ~5–9 kAU. Direction survives. The +40% boost itself is contested (Chae detect / Banik 19σ null). |

⭐ = the load-bearing universality tests.

---

## 3. The strongest existing-data argument, in full: UNIVERSALITY

This is the genuine, provable-now result. The logic chain:

**(a) The empirical fact.** Across the 175 SPARC galaxies the radial acceleration relation has an rms scatter of **0.057 dex (~13%)** after marginalizing over M/L, distance, and inclination (Li & McGaugh 2018, arXiv:1803.00022), and "no credible indication of variation in the critical acceleration scale" when galaxy-to-galaxy a0 freedom is explicitly permitted. McGaugh+2016 give 0.11–0.13 dex *total* (with measurement error). These galaxies span a **factor ~1100 in stellar surface density** (I measured σ(log₁₀ SBdisk) = 0.68 dex on the fitted sample) and ~5 dex in baryonic mass.

**(b) The fork it settles.** If a0 were sourced by the *local* matter density (a0 = (c/2)√(Gρ_local)), then a0 ∝ ρ_local^(1/2), so d log a0/d log ρ_local = +0.5. A factor-1100 spread in local density would inject ≈ 0.5 × 0.68 = **0.34 dex** of galaxy-to-galaxy a0 scatter. The data show ≤ 0.057 dex intrinsic. **The local-density source over-predicts the scatter and is excluded.**

**(c) The direct slope measurement (the cleanest single number).** Rather than argue from scatter alone, regress per-galaxy a0 directly on the **independent Spitzer photometric** surface density (not the kinematic SB used in the fit). My re-derivation on 143 galaxies:

> **d log a0 / d log SBdisk = +0.097 ± 0.036** → **11σ below** the local-fork prediction of +0.5.
> (SBeff gives +0.091 ± 0.033, 12σ below +0.5.)

**(d) The independent environmental cross-checks, all null:**
- Ursa-Major cluster members (21) vs field (122): Δ median log a0 = **−0.04 dex** (vs +0.5 the local fork needs for a denser environment).
- eRASS1 clusters: the effective a0 vs gas density slope is **−0.41** — the *wrong sign* entirely.

**(e) The honest quantitative bound.** Translating the intrinsic scatter into the maximum fraction f of a0² that local density may contribute, with the **correct deep-MOND propagation** (g_obs ∝ √(a0·g_bar) gives a factor 0.5, so RAR residual = 0.25·f·σ_logρ):

> **f ≤ 0.33** (using Li18's 0.057 dex), with **f = 1 (pure local source) disfavored at only ~3×** — *not* the ~5× the first pass claimed, and *not* 5σ. My own fixed-M/L per-galaxy scatter (0.30 dex) only excludes f=1 at ~1.1×.

**Conclusion of the strongest argument:** a0 is set by something **spatially uniform** at the ~0.06-dex level across the whole galaxy population and every independent method. That uniform thing is consistent with a *cosmic* density (ρ_Λ is uniform). The varying-local-density reading is excluded at the >10σ level on the slope. **But uniformity is necessary, not sufficient, for ρ_Λ causation** — a uniform a0 is equally consistent with ρ_Λ, ρ_crit (which differs from ρ_Λ only by the constant Ω_Λ at z=0, also uniform), any other uniform cosmic density, or a fundamental constant unrelated to density. **This argument kills fork C (local), but cannot select fork A (ρ_Λ) over fork B (ρ_total) at z=0**, and is silent on causation.

---

## 4. Genuinely new tests found, and what they yielded

Four tests went beyond re-showing the known z=0 value. **All four returned NULLS for the local-density fork — which is a valuable result, not a failure:**

1. **Per-galaxy a0 vs *independent photometric* density (the test Li18 did not run).** Li18 established a0 universality but never regressed a0 against the *environmental/density axis*. Doing so — using Spitzer SBdisk, which is independent of the kinematic fit — gives slope +0.097 ± 0.036, the **specific, direct falsification of a0 ∝ √ρ_local** (11σ). *Yield: the local-density fork is dead at the galaxy-internal scale.*

2. **Cluster environment cross-match on 9830 real eRASS1 clusters.** Computed 3D comoving positions, counted neighbors as an environment proxy, correlated with the MOND residual. Raw correlation has the sign the local fork predicts (−0.11 to −0.15), but the **partial correlation controlling M500 and z collapses to +0.004 (NULL)**, robust in a volume-limited z<0.2 subsample. *Yield: no environmental a0 signal in clusters once mass/redshift are removed; the raw signal was a mass confound.* (Caveat: 80% of clusters have zero neighbors within 20 Mpc — environment is coarsely resolved.)

3. **Cluster-RAR slope as a density discriminator.** The effective a0_eff = g_obs²/g_bar vs cluster gas density has slope **−0.41** (partial −0.27), the wrong sign vs +0.5. And keying a0 to ρ_cluster *overshoots* (drives the residual below 1) rather than closing the factor-2 cluster gap. *Yield: the density-dependent a0 that some invoke to "fix" clusters is disfavored three independent ways.* (Caveat: a0_eff and ρ_gas share Mgas with opposite powers, so ~half the negative slope is algebraic construction, not physics.)

4. **Wide-binary separation-scale discriminator.** Under a local-density fork a0_local ≈ 1000× a0_cosmic, but because the MOND transition separation scales only as ρ^(−1/4), the onset would move to ~300–940 AU; the observed Gaia deviation appears at the *cosmic* scale (~kAU). *Yield: independent of the contested Chae/Banik dispute, the deep-Newtonian anchor at 200–1000 AU is Keplerian, excluding the local fork.* (Caveat: the original "2000 AU = cosmic a0" was numerically wrong by ~24×; the true a0-crossing is ~5–9 kAU — direction survives, the specific coincidence does not.)

**The one genuinely new causal-channel datum that exists — and it currently cuts AGAINST the framework:** MUSE-DARK III (2026) measures the RAR at 0.33 < z < 1.44 and finds a0 **rising** as a0(z) = a0(0) + 1.59z (a0(z~1) ≈ 2.38×10⁻¹⁰), *faster than H(z)*. The framework's √ρ_DE reading predicts a0 roughly **constant-to-declining** (a0(z=3)/a0(0) ≈ 0.74 under DESI w0wa). This is a **real, face-value tension** in the only direct evolution data now available — caveated by 3D-forward-model, pressure-support, and beam systematics that ΛCDM (Magneticum) also reproduces. I report it as a tension, not as agreement.

---

## 5. The honest bottom line

**Existing data can establish the VALUE and the UNIVERSALITY of a0; it cannot yet establish CAUSATION.**

- **VALUE (strong consistency):** a0 ≈ (c/2)√(Gρ_Λ) = 9.35×10⁻¹¹ to ~20% — real, but a present-epoch coincidence numerically identical to the 40-year-old a0 ≈ cH₀/6, with a posited (underived) c/2 coefficient. ρ_crit (1.13×10⁻¹⁰) actually sits marginally closer to the 8-method ensemble (1.19×10⁻¹⁰) than ρ_Λ does, and at z=0 the two ρ's differ only by the constant Ω_Λ — so the snapshot **cannot tell which ρ** sources a0.

- **UNIVERSALITY (strong, genuine, provable now):** a0 is one uniform number across factor-1100 density, ~5-dex mass, and every independent method, to ≤ 0.057 dex intrinsic. This **selects a uniform cosmic source and excludes the local-density fork at >10σ** (slope +0.097±0.036 vs +0.5; f=1 disfavored at ~3×). This is real evidence that a0 is set by *a* uniform cosmic density at the right magnitude — the strongest existing-data argument the relation has.

- **CAUSATION (NOT established — and currently leaning unfavorable):** No existing dataset shows a0 *tracking* ρ as ρ *changes*. The cosmology half (DESI ρ_DE(z)) exists; the a0(z~3) measurement half does not, and is telescope-limited (~2027). The one intermediate-z datum that exists (MUSE-DARK III 2026) shows a0 **rising**, in tension with the framework's declining/constant reading.

**Plainly: this is value-consistency plus universality, not proof.** The universality result genuinely rules out the environment-dependent reading and points to a uniform cosmic origin — that is the honest, real win, and it is more than just re-showing the z=0 value. But asserting that the present value-match plus spatial uniformity *proves* a0 is caused by dark energy would be the manufacturing trap: it conflates necessary-with-sufficient and a present-value coincidence with a tracked causal law. The make-or-break is the z~3 evolution, and the early returns are not encouraging for the framework.

---

*Sources: [Li & McGaugh et al. 2018, A&A 615, A3 (arXiv:1803.00022)](https://arxiv.org/abs/1803.00022); [MUSE-DARK III, A&A 2026 (arXiv:2604.22613)](https://arxiv.org/abs/2604.22613). Re-derived on disk: SPARC 175-galaxy RAR (143 fit) + Lelli2016c.mrt; eRASS1 9830 clusters (erass1cl_primary_v3.2.fits). Algebra re-verified in sympy.*
