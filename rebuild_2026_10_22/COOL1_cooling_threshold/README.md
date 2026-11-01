# COOL1_cooling_threshold: CHOICE-DEPENDENT, NO LINK. t_cool = t_dyn with no astrophysical input gives 10^10.88 today, 10^11.04 by formation, more than 1.1 dex under T; the free inputs span 2.4–2.7 dex against T's 0.20 dex window. T stays located, not derived

Criteria: `FROZEN_CRITERIA.md` (b154df6559), committed alone first. `cool1.py`, `cool1.out`, `cool1_results.json`; twin `cool1_MUTATE.out`; `cool1_posthoc.py`, `.out`. κ = ½ FITTED, unused in the cold branch. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** the classic ~1e12 and T were both known.

**Scope.** T belongs to PAPER64's switch picture. Working rule N (owner 10-31) has no switch, so nothing here feeds N. No rule is proposed, so no SPARC, key, group or X-COP line is regraded.

## Target
T is an M200c mass from EM1's relation, summed over a basin, z = 0. **W = [12.19, 12.39]:** LEE1's lower edge and BS1's LG basin 12.3925, width 0.20 dex. The upper edge is one object's margin. W' to 12.6 is LEE1's box edge, not a measured edge. T has a target on canonical only (LEE1 alt 0/24).

## Primary: Z = 0, fair-share gas, r_s = R200c, isothermal, t_dyn = r/V, native background
| Row | Why this z | log M | Miss from 12.19 |
|---|---|---|---|
| **P0**, z = 0 | T is a z = 0 mass of a z = 0 object | **10.876** (V 60 km/s, T 1.3e5 K) | **−1.31** |
| **Pf**, z_half 1.13 (AE1's table), M = M0/2, reported as descendant M0 | the core is set at collapse, so a rule about halo presence belongs here | **11.035** | **−1.16** |
| Pfs, z(f_s) 1.73, M = 0.144 M0 | AE1's core-assembly epoch | 11.512 | −0.68 |

At 10^12.3, z = 0, primary: t_cool/t_dyn = 50. My hand estimate was 40 at 2e12 and a primary near 1e11.

## Inputs, what's free, sensitivity
| Input | Status | Values | log M_thr P0 | Pf | Spread P0 / Pf |
|---|---|---|---|---|---|
| Metallicity Z/Z☉ | **FREE**, no native value | 0, 0.03, 0.1, 0.3, 1 | 10.88, 11.36, 11.63, 11.89, 12.19 | 11.04, 11.56, 11.83, 12.10, 12.40 | **1.31 / 1.37** |
| Gas fraction f_g/f_b | **FREE** at 1e12; native f_b 0.1568 is an upper bound | 1, 0.5, 0.2 | 10.88, 10.73, 10.07 | 11.04, 10.88, 10.67 | **0.81 / 0.36** |
| Radius r_s/R200c | **FREE**, shock location | 1, 0.5, 0.3, 0.1 | 10.88, 11.03, 11.15, 11.48 | 11.04, 11.21, 11.36, 11.76 | **0.61 / 0.73** |
| Redshift, instantaneous M | a choice, stated above | 0, 1, 2, 4, 6 | 10.88, 10.75, 10.65, 10.53, 10.48 | | 0.40 |
| Density | form | isothermal / uniform | 10.88 / 11.13 | 11.04 / 11.33 | 0.25 / 0.29 |
| t_dyn | form | r/V / free fall | 10.88 / 10.90 | 11.04 / 11.06 | 0.02 |
| Halo | form | 200c / native Δ_vir, converted | 10.88 / 10.80 | 11.04 / 11.06 | 0.08 / 0.02 |
| Criterion | form | RO / Birnboim-Dekel at r_s = R | 10.88 / 11.85 | 11.04 / 12.17 | **0.97 / 1.14** |

Fixed: atomic rates, μ 0.59, X 0.76, native h, Ω_m, Ω_r.

**60 cells of Z × f_g × r_s:** P0 10.07 to 12.82, spread **2.75 dex, 13.7 × W**; Pf 10.67 to 13.07, spread **2.39 dex, 12.0 × W**. Cells in W: **6/60 and 7/60**. Each is a choice, for example Z 0.1, f_b, 0.1 R (12.24), or Z 0.3, f_b, 0.3 R (12.20). About 10–12 % of cells land in a window that is 7–8 % of the range: roughly what spread alone gives, so landing carries no information.

## The nearest row: Birnboim-Dekel, r_s = R200c, Z = 0
The coefficient re-derives here (γ_eff = 10/7 gives t_cool,post = 1.4 r_s/|u₁|, 0.01256). It gives 11.85 (z = 0) and **12.17 (formation), 0.02 dex under W.** It's close, and it isn't a landing:
- POST-HOC, no verdict depends on it: on that same form, Z 0.03 gives 12.32 and 12.58, Z 0.1 gives 12.57 and 12.82, Z 1 gives 13.15 and 13.41; f_g/f_b 0.5 gives 11.59 and 11.85. Real gas at 1e12 isn't primordial, and any measured enrichment moves it out of W upward, by up to 1.2 dex. Lowering the gas fraction then moves it back. So landing means choosing two numbers that compensate.
- BD at 0.5 R, Z 0 gives 12.19 at z = 0, but 12.59 at formation: same inputs, out of W.
- Its pre-shock density is the isothermal halo value, a further choice. Infall gas is not that.

## Footings
- **Cold branch:** no a₀ in V or T, so the number is identical on both, by construction. That's not a test.
- **Law branch** (no halo, V⁴ = G a₀ f_b M, a₀ flat, disclosed): primary P0 9.584 canonical, 9.478 alt, **−0.107 dex**, half of W. Pf 10.189, 10.092. So the same number does not come out on the side of the split where the footing matters.
- **The two branches disagree:** at the primary, law 9.58 against cold 10.88, 1.3 dex. Z 0.1 at 0.1 R: law 11.47, 11.36; Pf 12.07, 11.96, against cold 12.24. A threshold on the split needs to say which gravity the gas feels, and that is what the split decides.

## Does it say where a cold halo is absent? No. The missing link
Cooling says where gas cools. PAPER64's split needs a place where the cold fluid isn't. Nothing in the record connects them.
1. **No coupling.** The cold fluid sees only gravity. THEORY_PUSH B_condensed_rule says shock heating changes the gas's entropy, not its source. No rule or action has a term from gas's radiative state to cold density.
2. **The only channel in the record has the wrong sign.** Cooling makes a disc, the disc contracts the cold fluid: LC1 R_live 2.15, f_Q 0.87, a denser halo. UR1's response is inward at disc baryon fractions. The split wants no halo there.
3. **Energy.** At 10^12.3: cold binding 5.4e59 erg, gas thermal 1.5e59 erg, ratio **3.6**. Radiation also leaves optically thin gas. CFG930 found the same class of ordering problem.
4. **The basin.** T keys on the basin; cooling is per halo. On BS1's own LG all four halos are route E, and all are below T. Primary t_cool/t_dyn: LMC 0.46, M33 2.6, MW 25, M31 40; with Z 0.1 at 0.1 R, 0.00, 0.01, 0.26, 0.72, so all cool. A per-halo cooling key is the own-mass switch again, which PAPER64 shows needs T < 11.9 for the MW and T > 12.15 for lensing: the contradiction BS1 was built to remove. The basin at R0 795 kpc gives t_cool/t_dyn 85, but it's a turnaround surface with no shock there, so the criterion has no object.
5. **Record:** GT1's gas-state rule on hot atmospheres already FAILS (G-OUT-M3 +3.25, D +0.090).

**Missing link, named:** a term coupling baryon radiative state (t_cool or entropy) to the cold fluid's density, with the sign *cooled gas ⇒ no cold halo*, an energy source of at least 3.6 times the gas's thermal energy or a condition that stops the fluid ever collapsing, and a reach of the whole basin, not one halo. It would have to overcome LC1's measured contraction. There's no candidate in the record. Writing one would add a posit, not remove a number.

## Label (frozen)
- **Threshold: CHOICE-DEPENDENT.** Both primary rows miss W; spread ≫ 0.20 dex; some listed sets land in W, each a choice.
- **Link: NO LINK.**

Expectation held (primary near 1e11, spread over 1 dex, no link). I expected Z 0.3 at 0.1 R near 2e12; it gives 12.6 (P0).

## Checks
K1 CFG934's M_cool 2.3383e9 (2.338e9), 5.7943e8 (5.792e8), inside 0.2 %. K2 Λ(1 keV, Z 0) 8.904e-24 against CFG581's AtomDB 8.917e-24; Z 1/Z 0 at 0.12 keV 24.2 against 30.1. K3 1.4, 0.01256. K4 μ(1e7 K) 0.588. K5 root 1.000000000. K6 scalings to 1e-10. MUTATE Λ/10: P0 −0.954 dex, bites.

## Limits
- Λ, Z = 0 are KWH96's published formulas, recalled, PROVISIONAL; K2 tests them at one temperature. CFG581's AtomDB files are no longer on disk, and nothing was downloaded.
- Λ, Z > 0 is the record's Tozzi-Norman fit, linear in Z. The fit runs high below about 3e5 K (2.2e-21 at 1e5 K, clamped at 0.01 keV, against a physical peak I'd put several times lower); cells with Z > 0 reaching low M are affected. Every cell in W has T ≥ about 1e6 K, where it's within roughly 1.5.
- No UV background: it would suppress line cooling at z = 0 densities (n_H about 1e-5) and lower the low-mass rows. It can't narrow the spread's cause.
- CIE only, isothermal, no feedback, no enrichment history, spherical. AE1's z(f_s) is clamped above 1e12.
- a₀ held flat in the law branch (record's a₀(z) is 0.91–0.94 by z 2.33).
- A low-T guard (no cooling under 8e3 K) was added after the first run crashed on the grid's low end, before any threshold printed. No root is near it.
- W's upper edge rests on one basin mass, itself a lower bound (BS1), and its lower edge on LEE1's coarse draws. Widening W doesn't change the label: W' holds 8/60 and 15/60.

κ = ½ FITTED. Not theory closed.
