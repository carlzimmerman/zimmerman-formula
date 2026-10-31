# Argon's three re-sends of 10-31, scored

The owner relayed these after ZN1, X80, SI3 and KN1 had landed. Argon hadn't seen those results, so its numbers were blind even though I'm recording them afterwards. Recomputations: `argon_check2.py`, `argon_check2.out`. κ = ½ FITTED. Not theory closed.

**Still scrambled.** Audit items B, C, D and part of E; part of Q4 and the start of Q5; and in the third message, the ends of sections 3 and 6 and the closing scoreboard. Each stretch starts just after a `<` followed by a letter, such as `M_b(<R200)`. Asking Argon for "plain text" didn't fix it; it needs to write "inside R200" and avoid `<` and `>` altogether.

## The premise that doesn't hold
Argon's "A4 wall" rests on r₋₂'s c_f: 7.74, 8.67, 10.07. It compares those with c-equivalents from another estimator (5.72, 8.05), and reads a rising spike. Like for like, at ng 64:

| Estimator | 10¹² | 10¹³ | 10¹⁴ | trend |
|---|---|---|---|---|
| r₋₂ c_f (68 % wide, flagged by X77) | 7.74 | 8.67 | 10.07 | up |
| NFW fit | 7.75 | 7.15 | 6.80 | down |
| η_conv, as c-equivalent | 8.05 | 7.45 | 7.08 | down |
| ZN1's c₂₀₀ at z = 0 | 7.68 | 6.47 | 5.94 | down |

So c_f (1 + z_f) = 15.05, 15.18, 15.73 is true arithmetic on one noisy estimator. With the NFW fit the same product is 15.07, 12.52, 10.62. Its extrapolation to X80, ρ₁₀ 0.80 and ρ₁₁ 0.89, reads 1.128 [0.967, 1.301] and 0.938 [0.867, 1.316]: MISS at 10¹⁰, inside at 10¹¹. The S_A4/S_need ratios it builds (1.00, 1.62, 2.03) become 1.05, 1.33, 1.31 with η_conv. And ZN1 passes the shear with no core rule, so no "c_f = 10.07 to 4" repair is needed on the keys.

## ZN1 predictions (blind)
| Quantity | Argon, ng 64 | Measured | Result |
|---|---|---|---|
| M₂₀₀(z = 0)/M, 10¹³, 10¹⁴ | 1.08, 1.03 | 0.718, 0.683 | MISS |
| c at R₂₀₀, z = 0 | 10.85, 11.80 | 6.47, 5.94 | MISS |
| M(<r, 0)/M(<r, z_f), r/r_f 0.1, 0.2, 0.5, 1, 1.5 | 1.06, 1.14, 1.36, 1.82, 2.38 | 10¹⁴: 0.98, 1.05, 1.15, 1.19, 1.23 | MISS beyond 0.2 |
| Density slope, 1–1.8 R₂₀₀ | −3.15 ± 0.20 | −2.49, −2.50 | MISS |
| x_edge | near 1.55 R₂₀₀ | 6.35, 6.60 | MISS; its vacuum-boundary objection doesn't apply to the OUTER band |
| X-COP mean, rms | −0.145, 0.165 | −0.070, 0.116 | MISS |
| G-IN-Mall | −4.40 ± 0.50 | −1.73 | MISS |
| G-OUT-M3 | +2.65 ± 0.40 | +1.51 | MISS |
| Class | FAILS BOTH | KEYS ONLY | MISS |
| Earlier ng 48 branch: X-COP +0.022, 0.082; M3 +2.85; X-COP ONLY | | | MISS, except G-IN-Mall |

**Stop condition 1** (ZN1 FAILS BOTH, G-IN-Mall below −2.5, or X-COP rms above 0.12): not met at f★ 0.034 (0.116). At f★ 0.0615 rms is 0.121, a hair over; 38 % of seed draws pass X-COP. Not treated as met.

**Its objection to fair share inside R₂₀₀** (M₂₀₀ biased low by 13 %, anchor at r_ta instead): MA1's budget M₂₀₀ with this shape fails, 7 of 15 keys, OVER.

## Audit items
| Item | Argon | Checked | Standing |
|---|---|---|---|
| A. 18π² ρ_m against 200 ρ_c, S +7 % | R_vir/R₂₀₀ 1.792, M ratio 1.348 | 1.748, 1.413; S +6.5 % in MA1's own run | Right size, numbers slightly off |
| B. Fair-share bias | Y_b 0.90 | X-COP's own gas 0.957 of cosmic before stars, about 1.0 with | Not supported |
| C, D. Reduced shear, miscentring | scrambled | `redfac`, `offset_floor` already in the grader | No new item |
| E. Clamping above 10¹⁴ | +20.7 % in η on r₋₂ | Tested by ZN3 with real zooms | Pending ZN3 |
| F. X-COP at its own z_obs | −0.028 dex | Built into ZN1 | Done |
| G. SM1's tilt, ±0.04 dex | G-OUT-M3 ±0.35 | ±0.34, class unchanged: `../ZN1_zooms_to_z0/zn1_tilt.py` | **HIT** |

## Lanes
| Lane | Status | Outcome against Argon's lines |
|---|---|---|
| 1. ZN1 | done, 211652848c | Neither its PASS nor its FAIL. 75 of 200 draws pass both |
| 2. Joint statistic | BA1 done; older rules in BA2, running | |
| 3. X80 | done, a42ae32a01 | ρ₁₀ 1.128: between its fail (1.10) and pass (1.15). Gas-rich and LITTLE THINGS lines in ND1, running |
| 4. SI3 + SLUGGS | SI3 done, d29033b6cd; SR1 running | Frozen NO VERDICT. Post-result: S_strict Δχ² +56.5, D 7.44: its fail line. S_x300 +4.3 |
| 5. AM1 + GD1 | AM1 done, 916f4c269f; LC1 running | AM1: its fail, 11.88 against its 11.48 ± 0.08 |

**SI3 against Argon** (Δ_c, R2): S10 A_O1 3.99 (2.45), A_O2 law 1.26 (1.25, HIT), Δχ² +442.9 (+290). S30 A_O1 4.07 (1.95), A_O2 0.86 (0.70), Δχ² +95.8 (+95, HIT). S_strict A_O1 3.38 (1.45), A_O2 0.63 (0.25), Δχ² +56.5 (−5 to +15): MISS.

**AM1 against Argon:** lg M₂₀₀ 11.48 ± 0.08: measured 11.88 cold. Slopes 0.65 below 10¹⁰ and 1.65 above 10¹⁰·⁶: measured 1.07 and 1.42 over 9–10 and 10–11. SPARC Υ 0.41 ± 0.03: Υ 0.55, failing on rms instead.

## New claims in messages 2 and 3
| Claim | Check | Standing |
|---|---|---|
| X48's grid truncates P(k) at k_Nyq ∝ M^(−1/3) | True. 161.6, 34.8, 16.2, 7.50 per Mpc at ng 64; Argon's values are 3.7 × too low | Real. Tested in UV1, running |
| Missing-mode velocity, σ/V_vir 0.11, 0.24 | 0.023 at every mass, with Argon's own formula | MISS, by × 5–10 |
| Adding it takes r₋₂ c_f(10¹⁴) to 4.5–5.5 | Its own core formula gives (0.023)² r_f. UV1 runs it anyway | Pending |
| Gradient plus gravity minimum at fixed mass is (1 + x²)^(−3/2) | It's the soliton, (1 + 0.091 x²)^(−8): log slope −4.2, −7.3 at 2, 3 half-radii; ln(soliton/core) −2.0 at 3 half-radii | False. CFG119, CFG293 also closed this door |
| κ = ½ removed: it's 2π over 4π | Σ_a0 = a₀/2πG is a definition. Writing it as c√(Gρ_Λ)/4πG restates κ = ½ | Restatement, section 11 |
| Stiffness saturates ρ r at Σ_Λ = 106.85 | Its own S_need at clusters is 177, 291, above that cap | Fails on its own table |
| NZ1's M(<R₂₀₀) is half of M₂₀₀ | True, and it was worth testing. The mislabel is nominal M as M₂₀₀: zooms give 0.68 | **NZ2: F★-DEPENDENT**; 15 of 15 and X-COP at f★ 0.034 |
| Baryon retention at L★ 0.498 | 0.417: EM1's M₂₀₀ is cold mass | Small |
| FC1 failed because the budget r₀ inflates mass | True on its rule | Agreed; ZN1 and NZ2 both bypass it |

**What it got right:** the HSB/LSB test was worth running (wrong sign, right test). SM1's tilt size. SI3's S30 Δχ². G-IN-Mall on ZN1. X-COP surviving ng 64 with the zoom's r₀. NZ2 passing at f★ 0.034. **What it got wrong most often:** treating r₋₂'s c_f as the zooms' concentration.
