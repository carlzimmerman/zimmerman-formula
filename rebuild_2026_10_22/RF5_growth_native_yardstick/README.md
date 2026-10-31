# RF5_growth_native_yardstick: linear growth and the CMB on a background built from raw BAO and SN

Criteria and ledger 469657249b (alone first), script 12a29f9818, amendments in `AMENDMENTS.md`. Numbers: `rf5.out`, `rf5_results.json`, `cells/`.
The patched CLASS (X34's patch, unchanged, sha 328ac5e3) is rebuilt outside the repo. Wall time about 2.5 h, stopped at the frozen limit's approach.

## Verdict (frozen wording, per footing)

| footing | verdict |
|---|---|
| canonical | **a window exists at z_on ∈ [3e4, 1e6]** (top of the frozen grid). CMB = plik-lite only, shear = DES Y3 ξ+ linear-safe only, forest NOT DIAGNOSTIC (G0) |
| alt | **a window exists at z_on ∈ [3e4, 1e6]**, same channels |
| v3s khronon, μ_K 0.03 / 0.1 Mpc⁻¹ | **UNDETERMINED**: did not converge in 10 steps (0.1) or CLASS's stiff solver stopped (0.03). The fit ran away to n_s ≈ 1.4–1.5, w0 ≈ −3.5 and steered χ² near 4e4. No pass is in sight, and no minimum was found, so neither reads FAILS |
| z_on 4000, 2500, 1500, 1100, 300, 30 | **UNDETERMINED**: not finished. 4000 was still falling at steered χ² 1.9e4, 2.2 → 1.9 ×1e4 in 4 steps. These cells cannot reach the window unless the trend reverses, which is not shown |

The footings share one surface by construction: a₀ is absent from the linear FRW equations (Q6 D0). They differ only in what they read off it. Over the window, native a₀(0) at κ = ½
is 9.35–9.41e-11 m/s² (canonical, from ρ_DE) and 1.129–1.134e-10 (alt, from ρ_total), on this lane's own h and Ω_DE. Canonical a₀(2.33) is 7.3–8.1e-11, √X(2.33) 0.78–0.87, inside CFG689's band.

**Reading, per rule 7. This is not "the framework passes".**
- The growth yardstick was not what made X34's timing fail. With no ΛCDM reference anywhere, and the CPL background free, a late release still fails on the raw χ² surface: 2e4 misses the 25 line, 1.2e4 fails plik outright.
- The window is the same early dust X34 found. Its lower edge is about 9 × z_eq (z_eq ≈ 3400, X34), so the cold component must be dust long before recombination. "Reduces to ordinary dust" stands. Recombination is not a release boundary.
- Late σ₈ alone would not have decided this: shear at the linear-safe scales allows every cell to z_on 1.2e4 (p ≥ 1.8e-3).
- Below: the forest, if its model were adequate, would narrow this window sharply. That is not a verdict.

## The surface (raw χ² at each cell's own best fit; no Δχ² to ΛCDM anywhere)

| z_on | plik /605 dof | p | low TT | low EE | BAO /13 | SN /1819 | ξ+ /101 | A_shear | σ₈ | Ω_m | h | w0, wa | S − S_min | forest /327 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1e6 | 581.7 | 0.75 | 23.9 | 396.6 | 9.7 | 1629.5 | 103.2 | 0.95 | 0.826 | 0.312 | 0.675 | −0.81, −0.67 | 0.1 | 420 |
| 3e5 | 581.9 | 0.74 | 23.8 | 396.7 | 9.6 | 1629.4 | 103.1 | 0.95 | 0.824 | 0.312 | 0.675 | −0.83, −0.60 | 0 | 555 |
| 1e5 | 582.3 | 0.74 | 23.9 | 396.5 | 9.7 | 1629.5 | 103.3 | 0.95 | 0.816 | 0.312 | 0.675 | −0.82, −0.64 | 0.8 | 2548 |
| 5e4 | 584.0 | 0.72 | 24.4 | 396.8 | 10.3 | 1629.4 | 104.4 | 0.95 | 0.796 | 0.312 | 0.675 | −0.82, −0.66 | 4.1 | 5375 |
| 3e4 | 596.3 | 0.59 | 26.7 | 396.9 | 12.6 | 1629.6 | 107.5 | 0.95 | 0.756 | 0.314 | 0.673 | −0.78, −0.85 | **22.0** | 7165 |
| 2e4 | 663.3 | 0.050 | 32.9 | 397.6 | 16.3 | 1629.9 | 115.0 | 1.00 | 0.689 | 0.315 | 0.669 | −0.75, −1.03 | **100.5** | 8064 |
| 1.2e4 | 1077 | 5e-29 | 59.1 | 399.6 | 20.2 | 1629.8 | 146.3 | 1.21 | 0.550 | 0.314 | 0.663 | −0.74, −1.07 | 550 | not run |
| 7000 | 2556 | 3e-237 | 79.3 | 409.1 | 10.7 | 1629.9 | P(k) run failed | | | 0.299 | 0.662 | −0.84, −0.35 | | not run |

S = plik + A prior + BAO + SN + ξ+; S_min 2324.03 at 3e5. The absolute gates alone reach z_on = 2e4, so the 25 line is what sets the edge at 3e4. **That edge is near the line, 22.0, and it is a grid edge.** Shear and forest do not steer the fits (§2 of the criteria), so each S is an upper bound on that cell's joint minimum.

## The forest: NOT DIAGNOSTIC by the frozen rule, narrowly, and the surface is steep

G0 at the best cell (1e6): χ² 420/327, joint p 3.8e-4 against the line 0.01; worst z p 0.002 passes. So the channel enters no verdict.

Report it anyway, because the size is large and the failure of G0 is small:
- The χ² climbs 420 → 555 → 2548 → 5375 from z_on 1e6 to 5e4. γ and R_J sit at their floors in the worse cells. At 1e5, z = 3.6 alone is 913 with γ 1.0 and R_J 0.05.
- It is real linear power (`rf5_diag.json`, post hoc): at z 3.6, P(k)/P(k)₁ₑ₆ at k = 1, 3, 10 h/Mpc is 0.78, 0.38, 0.24 for z_on 1e5 and 0.45, 0.20, 0.12 for 5e4, while σ₈ moves only 1–4 %. The turn-on's δQ = 0 leaves a homogeneous new share of the mass on every mode already inside the horizon, which is why it reaches the forest's scales first.
- A lower R_J node (0.02, below the frozen floor) does not rescue z 3.6: 90 / 838 / 2118 for 1e6 / 1e5 / 5e4.
- **If the forest were live, only the top grid cell would stay within 25 of S_min, and the true edge could lie above 1e6.** The frozen grid stops at the edge, and its best cell is the one that failed G0. So this is a pointer, not a bound. It also depends on A6: an adiabatic release, not run here, might not suppress these modes the same way.
- V-Fbar (F̄ held at Becker+13 ± 5 %, from recollection, PROVISIONAL): 1618 at 1e6, so the model does not fit at that mean flux even in the dust limit. Free F̄ prefers 0.40–0.58 at z 4.4–3.6.

## What is missing, and what the channels are not

- **CMB:** plik-lite plus low-ℓ only. It is Planck's compressed, foreground-marginalised product. No raw maps, full Plik, or ACT/SPT spectra are on disk (ACT DR6 on disk is y and T maps).
- **Shear:** DES Y3 ξ+ only, 101 of 200 points at θ ≥ 17.9′ after the frozen k_NL cut. Its covariance is a ΛCDM-fiducial analytic one (ledger A15). There is no native non-linear model, so ξ− and small scales are not graded. **KiDS-1000 ξ± are not on disk as a data vector** (only catalogues), and were not rebuilt. m_i and Δz_i priors are from recollection, PROVISIONAL.
- **Forest:** z 3.6–4.4 at stride 4, 2 % floor. Boera+19 not graded (saturated, P1D2). Forest for z_on ≤ 1.2e4 not run.
- **Family:** one turn-on reading (X34 A9). The temperature-keyed adiabatic release is not run. The flagship's cold core law enters only as this w = 0 component: there is no separate cosmological form of it.
- **v3s khronon rows:** undetermined above. X4's own number was not re-derived on this background.

## Fit health (a parallel session's check, reported unverified; both points checked here)

1. **σ₈ = NaN in the cell JSONs: confirmed, harmless.** Fit runs have no mPk output, so CLASS prints no σ₈. The table reads it from each cell's P(k) run (K0.1 and 7000 have none or a meaningless value). No χ² uses it.
2. **The matmul warnings, "dx·dx = 0, a zero step": refuted.** The divide/overflow/invalid warnings fire on every matmul, including `r @ r`, the SN projection and the data loader. They reproduce on random finite arrays with this numpy-on-Accelerate build, with the correct product to 1e-16. No cell's Gauss–Newton history has a zero-fall step (`cells/*.json` `gn`). Different-start refit of 5e4 (ω_c +3 %, n_s +0.01, w0 −0.95, wa −0.2; starting 139 higher): S-part 2223.755 against 2223.789, difference −0.034, parameters within steps except wa −0.68 vs −0.66. Only this cell was restarted, so the others rest on the history audit. 7000 needed small line-search steps (λ to 1/16) and had 3 failed CLASS runs, so its number is the roughest; it fails plik by a wide margin either way.

## Checks and twin

K1 0.0, K2 1003.475 vs 1003.475 (harness only), K3 4.6e-5, K4 8.6e-4 (after A1), K5 sha 83efa43f, min eigenvalue > 0, K6 shim 0, Gaussian 4.9 % (range cut, A1), K7 clean, K8 0, K9 exit 75 then resume from the checkpoint. The chain itself was also preempted twice and resumed.
`RF5_MUTATE=1`: plik sign flip gives χ² 5.4e5, shear sign flip 535/94, K1 ×1.01 fails, all as required (K2 also fails, as m1 flips the data it reads). The twin's Gauss-Newton does not converge in its one step.

Script edits after 12a29f9818 are listed in A2, A3. Not re-run from scratch: the fits were done with the first-committed fit code, and the later edits touch the P(k) retry, the grader and K9 only.

κ = ½ FITTED; c_f EXTERNAL where used (not used here); cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.
