# CFG269: can the highest-redshift galaxies (z ≥ 4 to z ≈ 14) tell FLAT a₀ from the rival a₀ ∝ H(z)? (scoping + pre-flight, 2026-10-01)

> **κ = ½ is FITTED.** a₀(z) FLAT is the framework's distinctive law; a₀ ∝ H(z) (a₀ E(z)) is the rival. ΛCDM has no a₀; its line here is CFG222's effective-a₀ PROXY, reported only.
>
> **What this lane is.** Every outcome is a **discrimination between two a₀(z) laws under a declared dynamical estimator and a declared baryon calibration. It is not a measurement of a₀**, and no sentence here says the data favour the framework.
>
> **How the data were read.** Page reads only: arXiv abstract, HTML and PDF pages through the fetch tool. The tool cached some PDFs in the session folder, outside the repository; nothing was downloaded into the repository.
>
> **Status.** Not committed. Criteria: `FROZEN_CRITERIA.md`, written before any observed D of this lane was computed, plus Addendum 1 (sha256 of the file with the addendum 4cb4b384…).
>
> **Scope.** The owner extended the lane to z ≥ 4 (relayed by the coordinator before any D_obs was computed).

## Bottom line
1. **No redshift bin separates FLAT from the rival under the frozen rule.** The deciding pool in each bin is the one with stars plus gas (COMPLETE).

   | bin | COMPLETE pool | P (c = 0.15 dex) | verdict | at the 0.30 dex band | where the pool sits |
   |---|---|---|---|---|---|
   | 4 ≤ z < 6 | 14 objects | 1.45–1.94 | **MARGINAL** | NOT POSSIBLE | closer to FLAT: z_F −0.06 to +0.84, z_rival −1.80 to −1.28. No statement |
   | 6 ≤ z < 8 | REBELS-25 only | 0.40 | **NOT POSSIBLE** | NOT POSSIBLE | — |
   | 8 ≤ z ≤ 14 | JADES-GS-z14-0 + MACS0416_Y1 | 1.28–1.32 | **MARGINAL** | NOT POSSIBLE | — |

   - **Pooled over everything: NOT POSSIBLE to separate the two laws with today's public data at z ≥ 4.** The best result is MARGINAL, and only at the optimistic 0.15 dex calibration band.
   - **No row anywhere carries a ROBUST discrimination statement.**
2. **The stars-only (LOWER-LIMIT) pools are not a discrimination, although they reach P ≥ 2.**
   - Their power reaches P ≥ 2 in all three bins.
   - But the stars alone fall short of the dynamics for BOTH laws: median baryon shift needed 0.5–0.8 dex for the rival and 0.7–1.2 dex for FLAT.
   - Their "both disfavoured" readings are therefore GAS-LIMITED (gate G4): missing gas can remove them. They do not discriminate.
3. **The owner's premise holds only where the baryons are stars-dominated and y ≈ 0.3–10.**
   - JADES-GS-z14-0 with stars only sits at y = 2–5.5, where the rival gives D ≈ 3–4.4 against FLAT's 1.1–1.3: a gap of 0.42–0.53 dex.
   - With the DLA-based gas (Heintz+25), y rises to 17–21 and the gap shrinks to 0.25–0.27 dex. Both COMPLETE rows then sit at the floor (D_obs 0.54–0.64).
   - GHZ2 is so compact (r = 105 pc or 39 pc) that y = 76–549. There the rival is Newtonian too: gap 0.01–0.09 dex.
   - The z ≥ 8 objects that do reach y ≲ 1 (MACS1149-JD1, S04590) have stars-only baryons and widths that the literature flags as merger- or outflow-affected.
4. **Dominant systematic: the baryon inventory.**
   - **Gas:** unmeasured, or geometry-dependent, at z ≥ 6 for every object except REBELS-25.
   - **Stellar-mass route:** for example 10^9.05 against 10^8.27 for GHZ2, and 10^8.14 against 10^7.41 for MACS1149-JD1.
   - **At z 4–6:** the common-mode baryon calibration. Widening the band from 0.15 to 0.30 dex drops the COMPLETE pool's P from 1.45 to 0.62.
   - **Second:** the virial coefficient. Its factor-2 bracket is 0.30 dex in D, the same size as the 0.25–0.45 dex gap.
   - **Third, for the ultra-compact objects:** the size definition (GHZ2 39 against 105 pc).
5. **ΛCDM (reported only):**
   - **The PROXY lies within 10% of the rival at z ≥ 10:** 19.5 against 21.7 at z 10.6, and 33.4 against 32.4 at z 14.2. It is an extrapolation of the Dutton & Macciò concentrations, valid to z ≈ 5. **At z ≥ 8 any statement about the rival applies to this proxy too.**
   - **Dark matter inside r_e:**
     - TNG50 (de Graaff, Pillepich & Rix 2024, abstract verified) gives f_baryon(<1 kpc) ~ 0.25 for M★ ~ 10^8–9 at z = 6, i.e. D(<1 kpc) ≈ 4.
     - For the z > 10 compact galaxies (r_e ≲ 300 pc): **UNKNOWN**. No published value was found.

## Method in one paragraph
Per row (one object, one baryon branch, one radius):
- **Predictions:** y = g_bar/a₀; D_F = ν(y) and D_R = ν(y/E(z)), with E = √(0.3(1+z)³ + 0.7); gap G = log D_R − log D_F.
- **Residuals:** r_L = log D_obs − log D_L.
- **Errors:** σ_L = statistical ⊕ calibration. The calibration is a common baryon shift of ±c dex, with c = 0.15 primary and 0.30 as gate G1.
- **Power:** P = G / max σ, computed with symmetric σ so that it never depends on D_obs.
- **Verdict:** P ≥ 2 SEPARATES, 1–2 MARGINAL, < 1 NOT POSSIBLE.
- **Position:** z_L = r_L/σ_L. A statement is made only for SEPARATES rows, and is ROBUST only if gates G1–G5 pass:
  - G1: the 0.30 band;
  - G2: four kernel/footing cells;
  - G3: K/2 and 2K;
  - G4: stars-only rows (a statement survives missing gas only if the disfavoured law over-predicts);
  - G5: floors are never counted.
- **Reused lanes:** the committed (D, y) and committed uncertainties.
- **New rows:** D_obs = M_dyn(<r) / M_bar(<r), from the paper's own estimator.
  - Monte Carlo of the published errors, plus a 0.15 dex lognormal on the virial coefficient (factor 2 = ±2σ).
  - Explicit K/2 and 2K runs.
- **Pools:** one row per object; COMPLETE and LOWER-LIMIT never pooled together; the calibration treated as common-mode, so it does not average down; every branch combination, floors in and out, must agree.

**Kernel:** the record's ν_mono (FP1's monotone repair of ν_RAR; Addendum 1). P2 = √(1 + 1/y). Both footings are carried: 9.3603e-11 primary, 1.1312e-10.

## B3: z ≥ 8 (the census; primary cell ν_mono, canonical, c = 0.15)
C = COMPLETE (stars + gas); LL = LOWER-LIMIT (stars only). "pool" marks the row that enters the bin pool.

| object [dynamics; M★; gas] | z | cls | y | D_F | D_R | G | D_obs | z_F | z_R | P | verdict | closer to | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| JADES-GS-z14-0 [Carniani+25 M_dyn 10^9.0; M★ 10^8.29; + Heintz+25 DLA gas] pool | 14.18 | C | 17.3 | 1.04 | 1.93 | 0.27 | 0.64 | −0.55 | −1.42 | 0.63 | NOT POSSIBLE | FLAT | FLOOR; the outer band restores the rival |
| JADES-GS-z14-0 [Schouws+25 FWHM 136 ± 31, K = 5; M★ 10^8.7; + DLA gas] pool | 14.18 | C | 20.6 | 1.03 | 1.82 | 0.25 | 0.54 | −0.93 | −2.10 | 0.62 | NOT POSSIBLE | FLAT | FLOOR; never counted |
| JADES-GS-z14-0 [Carniani+25; 10^8.29; stars only] | 14.18 | LL | 2.15 | 1.30 | 4.41 | 0.53 | 5.13 | +1.17 | +0.15 | 1.29 | MARGINAL | rival | gas-limited |
| JADES-GS-z14-0 [Schouws+25; 10^8.7; stars only] | 14.18 | LL | 5.52 | 1.12 | 2.96 | 0.42 | 2.01 | +0.44 | −0.52 | 0.85 | NOT POSSIBLE | FLAT | gas-limited (FLAT) |
| JADES-GS-z14-0 [Scholtz+25 KinMS 10^9.4; 10^8.7; stars only] | 14.18 | LL | 5.52 | 1.12 | 2.96 | 0.42 | 5.01 | +1.04 | +0.43 | 0.57 | NOT POSSIBLE | rival | KinMS radius not stated |
| GHZ2 [Zavala+24 σ 79 ± 25, K = 5, R 105 pc; M★ 10^9.05 (Castellano+24)] pool | 12.33 | LL | 75.8 | 1.01 | 1.23 | 0.09 | 0.68 | −0.43 | −0.70 | 0.22 | NOT POSSIBLE | FLAT | FLOOR; possible AGN (Castellano+26) |
| GHZ2 [same; M★ 10^8.27 (Mitsuhashi+25)] pool | 12.33 | LL | 12.6 | 1.05 | 2.01 | 0.28 | 4.09 | +1.25 | +0.72 | 0.69 | NOT POSSIBLE | rival | gas-limited |
| GHZ2 [R 39 pc; 10^9.05 / 10^8.27] | 12.33 | LL | 549 / 91 | 1.00 / 1.01 | 1.03 / 1.19 | 0.01 / 0.07 | 0.25 / 1.52 | — | — | 0.03 / 0.17 | NOT POSSIBLE | — | sensitivity |
| GN-z11 [Xu+24 M_dyn(<2R_e = 418 pc) 4.6 ± 2.7e9; M★ 10^9.1] pool | 10.60 | LL | 8.0 | 1.08 | 2.20 | 0.31 | 4.90 | +1.25 | +0.75 | 0.65 | NOT POSSIBLE | rival | AGN host; CIII] partly broad-line (Maiolino+24) |
| GN-z11 [Álvarez-Márquez+25 M_dyn(<64 pc) 1.1e9; 10^9.1] pool | 10.60 | LL | 121 | 1.01 | 1.12 | 0.05 | 3.31 | +1.23 | +1.17 | 0.11 | NOT POSSIBLE | rival | C8 flag (the printed inputs give about half) |
| MACS1149-JD1 [Álvarez-Márquez+24 σ 69.2, K = 6, R 332 pc; M★ 10^8.14 (Stiavelli+23)] pool | 9.11 | LL | 0.94 | 1.61 | 4.85 | 0.48 | 15.9 | +4.71 | +2.69 | 2.33 | SEPARATES | rival | BOTH DISFAVOURED; G1, G3 and G4 fail; merger favoured (Marconcini+24) |
| MACS1149-JD1 [same; M★ 10^7.41 (Marconcini+24)] pool | 9.11 | LL | 0.17 | 2.94 | 10.6 | 0.56 | 86.4 | +7.66 | +4.97 | 2.95 | SEPARATES | rival | BOTH DISFAVOURED; G4 fails (gas-limited) |
| S04590 [Heintz+23 M_dyn(<1.1 kpc [CII]) 9e8; M★ 10^7.15] pool | 8.50 | LL | 0.017 | 8.09 | 30.9 | 0.58 | 63.7 | +2.32 | +0.81 | 1.29 | MARGINAL | rival | [CII] read as an outflow by Fujimoto+22 |
| MACS0416_Y1 [Bakx+20 M_dyn 1.2e10; M★ 10^9.0 (Harshan+24); + [CII] gas 5.6e9 (Takechi+26)] pool | 8.31 | C | 3.69 | 1.18 | 2.59 | 0.34 | 1.83 | +0.71 | −0.61 | 1.35 | MARGINAL | between | broad-line AGN (Takechi+26); merger (Harshan+24); C8 flag −0.30 |
| MACS0416_Y1 [same; stars only] | 8.31 | LL | 0.56 | 1.89 | 5.78 | 0.48 | 12.0 | +3.02 | +1.21 | 1.85 | MARGINAL | rival | gas-limited |

**Virial-coefficient bracket (gate G3; full list in the .out):**
- JADES-GS-z14-0 [Schouws, stars only]: D_obs 1.01 at K/2, 4.02 at 2K. The position flips from FLAT to the rival.
- MACS0416_Y1 COMPLETE: D_obs 0.91 at K/2 (z_R −2.32), 3.66 at 2K (z_F +2.17). The coefficient alone moves the row from one law to the other.

**Listed, not scored (reason):**
- **MoM-z14, z 14.44:** prism only. "the FWHM is completely unconstrained" (Naidu+25). A deep 24 h G235M programme (Cycle 5 GO 10361) is planned; no data are published.
- **No usable line width:**
  - JADES-GS-z13-1-LA: Lyα only;
  - JADES-GS-z12-0: lines unresolved;
  - JADES-GS-z14-1: no lines;
  - CAPERS z 10.56 / 11.01: prism;
  - CEERS2-588: no MIRI detection;
  - UHZ1 and UNCOVER-37126: [OIII]88 not detected;
  - GHZ1: prism and LRS.
- **MACS0647-JD (z 10.17):** the authors say the two components are "in the process of merging", and the MIRI widths blend them.
- **Gz9p3 / DHZ1 (z 9.31):** a merger per the authors. **Reported plainly:** Algera+26 give M_dyn 1.3 (+1.1/−0.6)e10, "∼4−15×" M★.
- **UNCOVER-10646 (z 8.51):** the authors say its FWHM "likely does not represent only the gravitational potential".
- **CEERS-1019 (z 8.68):** broad-line AGN (Larson+23); no system r_e; no M_dyn.
- **A2744-YD4:** now at z 7.88, not 8.38 (Hashimoto+23).

## B2: 6 ≤ z < 8

| object | z | cls | y | D_F | D_R | G | D_obs | z_F | z_R | P | verdict | closer to | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GO1871-11 (Saldana-Lopez+25) | 7.61 | LL | 1.22 | 1.49 | 3.89 | 0.42 | 5.01 | +1.55 | +0.38 | 1.26 | MARGINAL | rival | gas-limited |
| GO1871-10 | 7.60 | LL | 0.12 | 3.36 | 11.1 | 0.52 | 38.0 | +3.10 | +1.69 | 1.45 | MARGINAL | rival | outflow component |
| GO1871-12 | 7.50 | LL | 1.05 | 1.56 | 4.13 | 0.42 | 12.6 | +4.49 | +2.59 | 2.10 | SEPARATES | rival | BOTH DISFAVOURED; G1, G3, G4 fail; outflow; companion |
| JADES-NS-00047100 (de Graaff+24) | 7.43 | LL | 0.56 | 1.89 | 5.40 | 0.46 | 20.9 | +4.93 | +2.95 | 2.21 | SEPARATES | rival | BOTH DISFAVOURED; G1, G4 fail; three components |
| **REBELS-25** [Rowland+24 M_dyn 1.2e11; M★ 10^9.30; + CO(3–2) 1.0e11 at α_CO = 3 (Cescon+26)] | 7.31 | **C** | 15.7 | 1.04 | 1.50 | 0.16 | 1.18 | +0.14 | −0.30 | 0.41 | NOT POSSIBLE | FLAT | near-Newtonian; the M★ 8e9 branch gives the same |
| JADES-NS-20086025 | 7.26 | LL | 0.15 | 3.12 | 9.86 | 0.50 | 28.8 | +3.16 | +1.53 | 1.61 | MARGINAL | rival | fit did not converge |
| GO1871-40 | 7.09 | LL | 0.40 | 2.13 | 6.13 | 0.46 | 18.2 | +2.26 | +1.36 | 1.18 | MARGINAL | rival | outflow |
| GO1871-1032 | 7.09 | LL | 2.43 | 1.27 | 2.82 | 0.35 | 2.19 | +0.75 | −0.40 | 1.11 | MARGINAL | rival | |
| GO1871-70 | 7.03 | LL | 1.21 | 1.50 | 3.73 | 0.40 | 3.72 | +1.01 | −0.01 | 1.06 | MARGINAL | rival | |
| GO1871-912 | 6.72 | LL | 3.88 | 1.17 | 2.29 | 0.29 | 0.98 | −0.30 | −1.68 | 1.11 | MARGINAL | FLAT | FLOOR |
| GO1871-105 | 6.57 | LL | 0.31 | 2.34 | 6.57 | 0.45 | 33.9 | +2.03 | +1.50 | 0.84 | NOT POSSIBLE | rival | outflow |

**Not scored:**
- **Mergers or non-rotators by the authors' statement:** COS-3018 ("merging", GA-NIFS), COS-2987 ("not … a purely rotation-dominated disk", RIOJA), B14-65666, A1689-zD1, SPT0311-58, MACS0308-zD1.
- **Cosmic Grapes:** v_rot not found and the estimator convention is unverified.
- **Parlanti+23 Method-I rows:** M_dyn within 5 kpc, no stellar r_e.
- **Saldana-Lopez PSF rows:** upper limits only.
- **1871-63:** an AGN candidate, excluded by the authors.

**Reported plainly from the papers:**
- de Graaff+24: "all objects in our sample have dynamical masses that are greater than the estimated stellar masses", by up to ×40, and about ×3 above stars + gas.
- Saldana-Lopez+25: (M★ + M_gas)/M_dyn ≈ 0.2–0.7; stars + gas reconcile the dynamics in only 2 of 11.

## B1: 4 ≤ z < 6 (reused lanes + census)
**COMPLETE rows (the deciding pool, 14 objects):**

| object (lane) | z | y | D_F | D_R | G | D_obs | z_F | z_R | P | verdict | closer to |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CRISTAL-03 (CFG220) | 5.69 | 4.40 | 1.15 | 2.03 | 0.25 | 1.02 | −0.19 | −1.12 | 0.87 | NOT POSSIBLE | FLAT |
| CRISTAL-20 = HZ4 = DC494057 (CFG220; the CFG228 duplicate is not pooled) | 5.54 | 1.08 | 1.55 | 3.45 | 0.35 | 1.48 | −0.08 | −1.39 | 1.28 | MARGINAL | FLAT |
| DC552206 (CFG228) | 5.50 | 2.02 | 1.32 | 2.67 | 0.31 | 1.58 | +0.26 | −0.78 | 0.99 | NOT POSSIBLE | FLAT |
| CRISTAL-02 | 5.29 | 0.77 | 1.71 | 3.88 | 0.36 | 1.03 | −0.82 | −2.18 | 1.32 | MARGINAL | FLAT |
| CRISTAL-19 | 5.23 | 0.96 | 1.60 | 3.51 | 0.34 | 3.39 | +1.20 | −0.06 | 1.26 | MARGINAL | rival |
| CRISTAL-07a | 5.15 | 1.10 | 1.54 | 3.29 | 0.33 | 2.62 | +0.85 | −0.37 | 1.21 | MARGINAL | rival |
| DC881725 | 4.58 | 1.74 | 1.37 | 2.59 | 0.28 | 2.09 | +0.63 | −0.34 | 0.96 | NOT POSSIBLE | rival |
| VC5110377875 | 4.55 | 3.31 | 1.20 | 2.03 | 0.23 | 0.75 | −0.79 | −1.85 | 0.88 | NOT POSSIBLE | FLAT (FLOOR) |
| DC396844 | 4.54 | 2.58 | 1.25 | 2.22 | 0.25 | 2.17 | +0.54 | −0.02 | 0.56 | NOT POSSIBLE | rival |
| CRISTAL-11 | 4.44 | 1.58 | 1.40 | 2.64 | 0.28 | 3.21 | +1.32 | +0.32 | 1.01 | MARGINAL | rival |
| CG32 | 4.41 | 1.27 | 1.48 | 2.88 | 0.29 | 3.61 | +0.99 | +0.26 | 0.74 | NOT POSSIBLE | rival |
| J081740 [gas + corpus M★] (CFG277) | 4.26 | 12.2 | 1.06 | 1.35 | 0.11 | 0.69 | −0.84 | −1.43 | 0.42 | NOT POSSIBLE | FLAT (FLOOR) |
| SPT0418-47 (CFG228) | 4.22 | 9.99 | 1.07 | 1.41 | 0.12 | 0.61 | −0.96 | −1.64 | 0.49 | NOT POSSIBLE | FLAT (FLOOR) |
| GN20 [stars + RT gas; R_e] (CFG276, recommended row) | 4.05 | 26.2 | 1.03 | 1.16 | 0.05 | 0.90 | −0.25 | −0.51 | 0.21 | NOT POSSIBLE | FLAT (FLOOR) |

**The pool:**
- With floors: r̄_F −0.010 ± 0.156 (z −0.06), r̄_R −0.236 ± 0.131 (z −1.80), P 1.45, MARGINAL.
- Floors excluded: r̄_F +0.133 (z +0.84), r̄_R −0.174 (z −1.28), P 1.94, MARGINAL.
- At c = 0.30: P 0.62 / 0.89, NOT POSSIBLE.
- The pool lies closer to FLAT, but that is a position, not a statement: the power is below 2.
- **The four floors:** VC5110377875, SPT0418-47, J081740 and GN20 (the record's baryon-calibration cases). The outer band restores the rival in every one, so **the floors do not discriminate**.

**LOWER-LIMIT rows (not deciding):**
- 33 Danhaive+25 discs (CFG273), HZ9's two M★ branches (CFG271), SGP38326-1/-2 and BRI1335-0417 (gas only, CFG277), and the census rows: de Graaff 19606 / 22251 / 16745 / 10016374, GO1871-29 / -451 / -545.
- **Danhaive:** 0 SEPARATES, 15 MARGINAL, 18 NOT POSSIBLE, 6 floors.
- **The four de Graaff rows reach P 2.10–2.48:**
  - three read "BOTH DISFAVOURED" and 22251 reads "FLAT DISFAVOURED" (z_F +3.36, z_R +1.00);
  - all have r > 0 under both laws, so **all are GAS-LIMITED (G4 fails)**, and G1 fails;
  - de Graaff+24's own scaling-relation gas (⟨M_gas/M★⟩ ≈ 10, not tabulated per object, not used) would move them by about +1 dex in baryons.
- **BRI1335-0417** (quasar host) is the one floor that the outer band does not restore. It is a floor, so it is never counted.

## ΛCDM (PROXY only)
- **PROXY residuals:** reported per row in `cfg269_rows.csv` (r_PROXY).
- **Where the PROXY sits:** at z ≥ 10 it nearly coincides with the rival; at z 4–6 it lies between FLAT and the rival (pooled COMPLETE r_PROXY −0.18).
- **Dark matter inside r_e:**
  - **TNG50 (de Graaff, Pillepich & Rix 2024, ApJL 967 L40; abstract verified):** "f_baryon(<1 kpc) ∼ 0.25" for M★ ∼ 10^8–9 at z = 6, with gas exceeding stars by ∼4.
  - **Observationally (helper-read):** Danhaive+25b gives ⟨f_DM(<r_e)⟩ = 0.73 at z 4–6, "consistent with simulations".
  - **z > 10, r_e ≲ 300 pc:** UNKNOWN.
- This is not a ΛCDM test: that would need simulated galaxies.

## MUTATE (every line width × 1.7, every D × 2.89; `*_MUTATE.*`)
- **C6 PASS:** every reused residual rises by exactly log 2.89 = 0.4609 (maximum deviation 6e-16); census residuals move by 0.4609 to within 0.001; reused P are unchanged (2e-15).
- **Positions:** 25 rows move from "closer to FLAT" to "closer to the rival". Examples: both JADES-GS-z14-0 COMPLETE rows, GHZ2 [105 pc; 10^9.05], REBELS-25, every B1 COMPLETE floor, CRISTAL-02, -03 and -20.
- **Statements:** de Graaff 22251 goes from FLAT DISFAVOURED to BOTH DISFAVOURED.
- **Pooled B1 COMPLETE:** z_F goes from −0.06 to +2.90 and z_R from −1.80 to +1.72.
- **The separation verdicts do not move:** P does not depend on the central D, by construction (criteria section 2). MUTATE moves positions exactly as it should and leaves the power verdicts alone.

## Controls, failures, hand estimates (nothing hidden)
**Controls:**
- **C1 FAILS AS FROZEN:** 1.87e-3 against 1e-4. The two CFG271 multi-radius sensitivity rows ("3 rings") carry a set-median δ, not one point. All 50 single-radius rows reproduce to 4.3e-6 (post hoc, labelled). Those two rows are never pooled and are labelled "position not interpretable". **The script exits 1 on C1.**
- **Passing:**
  - C1b: CFG228 dFLAT and dHz to 1e-8;
  - C2: CFG220 per-disc δ to 0.0013;
  - C3 and C4: kernels and E(14) = 31.83;
  - C5: PROXY = CFG222;
  - C6: MUTATE;
  - C7: census MC with zero errors equals the closed form.
- **C8 (flags):**
  - It reproduces all six de Graaff+24 M_dyn exactly from the transcribed σ₀, v, r_e, which checks that transcription.
  - Flags (paper vs recomputed):
    - Carniani+25: −0.11 dex. Its text applies a +0.1 dex correction following Übler+23;
    - Álvarez-Márquez+25 (GN-z11): −0.28;
    - Bakx+20 (MACS0416_Y1): −0.30.
- The run is byte-identical on re-run (seeded MC).

**Hand estimates (frozen before any D_obs), scored:**
- **H1 hit:** z 14.2 at y = 5.5 gives G 0.42 against the predicted 0.43. D_F was predicted with ν_RAR (1.106); with ν_mono it is 1.12.
- **H2 MISS:** a single z ≥ 8 object does reach P ≥ 2: MACS1149-JD1, P 2.33 / 2.95, through its low y and small quoted errors. It is stars-only and gas-limited.
- **H3 partial:**
  - The deciding B3 pool's P is 1.28–1.32, below the predicted 1.5–2.3.
  - The stars-only B3 pool's P is 2.06–2.97, above the range.
  - "No ROBUST statement survives G1": hit.
- **H4 hit:** B1 G 0.23–0.31; single COMPLETE rows P < 2 (maximum 1.32); the COMPLETE pool MARGINAL with no statement; stars-only rows at or above the rival and gas-limited.
- **H5 hit for the deciding pool** (REBELS-25 NOT POSSIBLE). The stars-only B2 pool reaches SEPARATES and is gas-limited.
- **H6 hit:** HZ9 [M986] G 0.40, P 1.84, closer to the rival, gas-limited.
- **H7 hit.**

## Disclosures
1. **Not blind.** I had seen committed D values of the reused lanes before writing the criteria (listed in the criteria). The helpers' census reports, which include the published line widths and M_dyn, arrived after the criteria and Addendum 1 were written, but before stage B was computed for the census rows.
2. **Addendum 1.** The criteria first wrote ν_mono as 1/(1 − e^{−√y}), which is ν_RAR. The frozen C1 caught it. The test run's stage-B rows were not read, and its files were deleted.
3. **An implementation fix after the first look at reused stage-B rows.**
   - What was wrong: P had used the side-facing σ, so it changed with the sign of r. MUTATE C6 exposed this.
   - The fix: P now uses the symmetric σ, as the frozen section 2 requires ("P does not depend on the central D_obs").
   - Its effect: some per-row P values changed. For example, Danhaive 1014130 went from 2.51 SEPARATES to MARGINAL.
4. **Exclusion rule as applied.**
   - Excluded: rows whose own authors attribute the width to a merger, outflow or AGN.
   - Scored but FLAGGED: rows where a different paper raised such a flag (GHZ2, GN-z11, MACS1149-JD1, S04590, MACS0416_Y1, two de Graaff and four Saldana-Lopez rows).
   - A post-hoc pool without the flagged rows (labelled in the .out) leaves B1 and B2 unchanged. B3's COMPLETE pool then keeps only JADES-GS-z14-0 and drops from MARGINAL to NOT POSSIBLE (P 0.62–0.63). B2's stars-only pool reads "FLAT DISFAVOURED" at P 2.21, gas-limited, and fails G1 (P 1.47 at the outer band).
5. **Profiles I chose, where the paper's radius is not r_e:**
   - GN-z11 at 2R_e and at 64 pc: an exponential extended component (r_e 200 pc) plus the point source.
   - S04590: all stars inside the 1.1 kpc [CII] radius.
   - The Heintz+25 gas inside 260 pc: an exponential with R_e,gas = 3 r_UV, enclosing 0.11.
   - JADES-GS-z14-0 C25 M★: statistical and systematic errors combined in quadrature.
6. **Uncertainty asymmetry.** The reused lanes' committed σ carry no virial-coefficient term; the census rows carry 0.15 dex. The reused rows therefore look relatively more precise.
7. **Duplicates.**
   - CRISTAL-20 = DC494057 is counted once.
   - GO1871-545 has z and M★ close to Danhaive 1086992 but r_e 0.83 against 3.42 kpc. It is not treated as a duplicate (flagged).
8. **How sources were read (page reads):**
   - **Verified by me:** Carniani+25 HTML (FWHM, Eq. 1, 9.0 ± 0.2 ± 0.2, M★); Schouws+25 HTML (FWHM 136 ± 31, M_dyn sentence, M★, dust); Zavala+24 HTML (GHZ2 FWHM 186 ± 58, σ 79, Eq. 1, radii); Xu+24 HTML (GN-z11); Saldana-Lopez+25 Tables A1–A3 (PDF page images); the de Graaff, Pillepich & Rix abstract.
   - **Read by page-read helpers through a summariser, marked helper-read:** all other numbers. Any helper item it could not confirm is UNVERIFIED and is not used. The C8 reproduction checks the de Graaff transcription.
9. **Files outside the repository.** The fetch tool cached some arXiv PDFs and one STScI programme PDF in the session folder, outside the repository. Nothing was written to the repository except this directory.

## Files and commands
Files, all in `campaign_fresh_gravity/CFG269_highest_z_dynamics/`:
- `FROZEN_CRITERIA.md`: the criteria, plus Addendum 1;
- `cfg269_discriminate.py`: the lane script;
- `cfg269_census_inputs.py`: the published inputs with sources;
- `cfg269_discriminate.out`, `cfg269_results.json`, `cfg269_rows.csv`: the main run;
- `cfg269_discriminate_MUTATE.out`, `cfg269_results_MUTATE.json`, `cfg269_rows_MUTATE.csv`: the MUTATE run;
- this file.

Commands:
```
cd campaign_fresh_gravity/CFG269_highest_z_dynamics
python3 cfg269_discriminate.py              # about 10 s; exits 1 only on the frozen C1 failure described above
MUTATE=1 python3 cfg269_discriminate.py     # needs the unmutated results first; C6 must PASS
```
Reused inputs are read in place from CFG220, CFG228, CFG271, CFG273, CFG276 and CFG277. CFG229 and CFG272 have no z ≥ 4 rows. CFG213's fit-route twelve-disc result (rival −0.161 [−0.207, −0.055], route-dependent) is quoted, not re-derived.
