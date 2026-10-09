# CFG513: the Milky Way's own cold-energy profile vs NFW, and where an NFW assumption biases MW-based measurements

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (548396b05).
- **Script:** `cfg513_mw_profile.py`, about 2 min, 7/7 checks pass. Outputs: `cfg513.out`, `cfg513_results.json`, `cfg513_profiles.csv`, `cfg513_profile.png`.
- **MUTATE:** `CFG513_MUTATE=1`, 8/8 checks pass. The truth in every row is set to that row's assumed NFW, and every bias vanishes (max |b/σ| 4e-8). Outputs: `cfg513_MUTATE.out`, `cfg513_results_MUTATE.json`.
- **Settings:** κ = ½ is FITTED. Both footings are used throughout. The kernel is ν_mono. On-disk data only; nothing downloaded. The Gaia DR4 prereg was read, not edited. The cold energy's MASS is still required (no particle is added). This is not "theory closed", and nothing here says the data favour the framework.

## Bottom line

1. **The edge is close in.** For M_b = 6e10, r_M = √(GM_b/a₀) is 9.5 kpc (canonical) and 8.6 kpc (alt). So the f_ret = 1 edge sits at **55 / 50 kpc**, and the MW's whole mass is then only **3.8e11 M☉**.
   - My pre-freeze note guessed about 175 kpc. That came from an arithmetic slip (I used r_M ≈ 30 kpc). The note did not enter any criterion.
   - With the record's census retention (f_ret = 0.18), the edge is at **287 / 261 kpc** and the total mass is **1.85e12 M☉**.
2. **Inside about 50 kpc, an NFW cannot tell itself apart from the framework.** An NFW fitted to the framework's own rotation curve (N-F) matches it to χ² ≈ 0.3 over 6–27 kpc. Within 50 kpc, M(<r) agrees to 1–3%, and the spherical local density agrees to 1–2%.
3. **Beyond about 50 kpc, the bias is large, and its sign depends on f_ret.**
   - If f_ret = 1, an NFW analysis overstates the MW's mass: by +52–61% at 100 kpc, +130–140% at 200 kpc, and ×2.3–2.4 in M200 versus the framework's total.
   - If f_ret = 0.18, it understates it: by 8–16% at 100 kpc, 28–36% at 200 kpc, and about 50% versus the total.
4. **The MW's own data choose between these readings. This is a framework test, verified as hard as a pass would be.**
   - **f_ret = 1 is excluded three ways:**
     - The LG timing argument predicts an approach of only −8.9 km/s, against the measured −109.3 ± 4.4 (z = −22.8).
     - CFG433's satellite V_c at 78 kpc sits 4.06σ above it.
     - 24 of Fritz's 39 satellites come out unbound, against 6 in the light NFW.
   - **f_ret = 0.18 passes LG timing to within 3.1σ** (−122.8 km/s, a little fast). Post hoc, the timing needs f_ret = 0.206. That is not a fit, and it is close to the census 0.18. The satellites keep CFG433's existing 2.5–2.9σ lean high.
5. **DR4 and the other decisive tests:**
   - The MW profile does not bias Gaia DR4's Arm C / settling prediction (γ = 1.000). The effect is ≤ 0.03 σ_tot.
   - Arms A/B use the observed g_ext, which does not depend on the profile.
   - Cassini Q2: no bias.
   - The prereg's statement that the MW phantom tide is 1.6–2.6e-31 s⁻² is reproduced (2.2 / 2.5e-31, spherical).
   - The things that do move are the MW-mass-dependent inputs to the satellite / LG / EFE-rival analyses, and the local midplane density, if the phantom disc is realised.

## The profile (M_b = 6.0e10; canonical / alt)

| | f_ret = 1 | f_ret = 0.18 (census) | bare law (record's CFG286/433/463 reading) |
|---|---|---|---|
| edge | 55.4 / 50.4 kpc | 286.5 / 260.7 kpc | none |
| M_cold (settled cold energy) | 3.22e11 | 1.79e12 | unbounded |
| M(<50 kpc) | 3.47e11 / 3.79e11 | same | same |
| M(<100 kpc) | 3.82e11 | 6.65e11 / 7.27e11 | same as 0.18 |
| M(<200 kpc) | 3.82e11 | 1.30e12 / 1.42e12 | same |
| V_c,sph(100 kpc) | 128 km/s (Keplerian) | 169 / 177 km/s (flat) | 169 / 177 |
| ρ_cold at R₀, spherical | 0.0064 / 0.0073 M☉ pc⁻³ | same | same |
| ρ_cold at R₀, midplane with phantom disc (algebraic QUMOND) | 0.067 / 0.078 | same | same |

- **Baryons.** The bulge is 0.90e10 (Hernquist, 0.7 kpc). The stellar disc is 4.03e10 (R_d 2.6 kpc). The gas is 1.08e10 (R_d 6 kpc). These are L172's shapes rescaled to the record's 6.0e10; 7.3e10 is run as a variant.
- **Rotation-curve test (nothing fitted).** At M_b = 6.0e10 the in-plane law runs 7–10% low against Gaia: V(R₀) = 211 / 216 km/s, χ² = 306 / 150 for Ou+24's 37 points. At 7.3e10 it fits: χ² = 44 / 12, with V(R₀) = 227 / 232. This test does not depend on the edge.
- **NFW references.**
  - N-F for the canonical 6.0e10 truth: M200c(NFW) = 8.1e11, c = 9.5. Including baryons, the inferred total M200c is 8.8e11.
  - N-D, fitted to Ou+24 itself: M200c = 6.0e11, c = 19 (χ² 10/35).
  - The literature halos are RECALLED and UNVERIFIED: 1e12 with c = 10, McMillan17, and Bovy15 at 0.8e12 and 1.6e12.
- **Ownership.**
  - Under O-MW, the MW owns its phantom out to the radii in the table.
  - Under O-LG, the MW-centric profile is defined only inside r_split = 323 kpc. That is the deep-law field-equality point toward M31 at 780 kpc.
  - O-LG timing, with one LG phantom at the barycentre, is far too fast in every cell (−213 to −750 km/s). So O-MW is the reading the timing allows.

## Bias table: b = Q(assumed NFW) − Q(true framework); verdict = worst cell

| row | measurement | verdict | size (cell range) | touches |
|---|---|---|---|---|
| b-N-F-100/200/300, M200 | MW mass from an NFW fitted to the inner curve, extrapolated | **MATERIAL** | M(<100): +52–61% (f_ret 1) / −8 to −16% (0.18); M(<200): +123–138% / −28 to −36%; M200 vs total: +131–142% / −50 to −52% | MW mass, satellites' host, f_ret readings |
| b-N-F+T (adds M(<50), M(<100) tracers) | same, with tracer masses | **MATERIAL** | M(<200): +78–88% / −25 to −32% | same |
| b-N-F-50 | M(<50) | NONE | ±3% | — |
| b2 | LG timing mass read as point-mass Kepler from the framework's own orbit | NONE | −0.1 to −0.5% (the timing argument measures the framework's total faithfully) | LG timing |
| a1 / a2 | satellite pericentres in Fritz's 0.8e12 / 1.6e12 potentials | NONE / MINOR | medians −0.1σ / −0.3 to −0.6σ (1.6e12 gives pericentres 13–17% smaller); 18–31% of objects beyond 1σ for 1.6e12 | satellites, UFD tidal history |
| a3 | the record's bare-law host (CFG433/463/286) vs the edge, pericentres | NONE | ≤ 0.01σ. But apocentres are 23% smaller under the bare law than under the f_ret = 1 edge (median), so CFG463-type infall orders inherit an f_ret-dependent outer orbit | CFG463 |
| a4 | CFG433's predicted V_c at 78 kpc (bare law used) vs the f_ret = 1 edge | **MATERIAL** (f_ret 1) / NONE (0.18) | +1.2 / +1.5σ: the bare law flatters f_ret = 1 | CFG433 |
| c-spherical | local cold density, RC-based NFW | NONE | +1 to +2% | — |
| c-midplane / c-slab | local cold density if the phantom disc is realised | **MATERIAL (conditional)** | NFW reads 0.0065–0.0079 against the framework's 0.067–0.081 midplane (−90%) and 0.016–0.020 slab (−60%) | vertical-force / Oort-limit tests |
| d1 | DR4 Arm C / settling (γ = 1.000): the effect of the MW-model tide on γ_v at 30 kAU | NONE | ≤ 0.03 σ_tot (σ_tot 0.0278 from the prereg) | **DR4 (decisive)** |
| d2 | DR4 Arms A/B: model g_ext at the Sun | NONE | +0.4–0.5% (the arms use the observed g_ext) | DR4 Arms A/B |
| e-LMC / e-SMC, S-model | compact-object halo fraction bound with the MACHO S-model | **MATERIAL** (canonical) / MINOR (alt) | τ_F/τ_S = 0.73 / 0.81, so an S-model bound is 19–27% too tight for a framework-shaped halo | CFG510 PBH reading only |
| e-…-N-F | the same with N-F | NONE | −3% | — |
| f-Vc GD-1 / Pal 5 / Orphan 40 | stream V_c | MINOR | +0.8–1.8% (2% scale) | streams |
| f-Vc Orphan 60 / Sgr 100 | stream V_c | **MATERIAL** | Sgr 100 kpc: +23–27% (f_ret 1) / −6 to −8% (0.18) | streams |
| f-q | halo flattening at GD-1, spherical NFW vs the framework's phantom force | **MATERIAL** | q_F = 0.891 (both footings): a prediction 0.4σ from Koposov+10's 0.87 and 1σ from Bovy+16's 0.94 ± 0.05 (both recalled) | streams; a framework test |
| g1 | Cassini Q2, Galactic tidal-tensor difference | NONE | 1e-3σ (3.4–4.0e-30 against 3e-27) | **no-EFE claims (PAPER44)** |
| g2 | vertical Galactic tide 4πGρ₀ in Oort / TNO models | **MATERIAL (conditional on the phantom disc)** | NFW 31–34% low | PAPER44 TNO run (already inconclusive) |
| h-100 / h-200 | the EFE rival's satellite dispersion from the host field | **MATERIAL** at 200 kpc (f_ret 1) | g_ext(N-F)/g_ext(F) = 2.3–2.4 at 200 kpc (f_ret 1) or 0.64–0.67 (0.18): Δlog σ up to 0.19 dex | no-EFE comparisons that use distant MW satellites |

"Both directions": the reverse case (NFW true, framework assumed) has the same |b| with the opposite sign. Where it matters (fitted rows), the two f_ret readings already bracket both signs.

## Framework tests the bias rows exposed (added after the first run; reported, no verdict input)

| test | f_ret = 1 | f_ret = 0.18 | bare law |
|---|---|---|---|
| LG timing, O-MW, Λ: predicted v_r at 780 kpc vs −109.3 ± 4.4 (on disk) | −8.9 km/s, z = −22.8 | −122.8, z = +3.1 | −295 / −318, z = +42 / +47 |
| CFG433 satellite V_c at 78 kpc (231.9 ± 21.4): D, canonical / alt | +4.06 / +4.06 | +2.89 / +2.52 | +2.89 / +2.52 |
| Fritz satellites unbound at central values (of 39; light NFW 6, heavy NFW 2) | 24 | 4 | 0 |
| post hoc f_ret that LG timing needs (not a fit) | — | 0.206 (both footings) | — |

- **Local total midplane density** (recalled ρ_b 0.084 and measured total about 0.10 ± 0.01, both UNVERIFIED):
  - With the phantom disc, the framework gives 0.129 / 0.136, which is +2.9 / +3.6σ.
  - With only spherical cold energy it gives 0.090, which is −1σ.
  - So the phantom disc, if realised, is a new local-dynamics tension. But B's cold fluid is hot (σ ≈ 145 km/s, CFG484), so it probably cannot build a 300-pc phantom disc. The spherical reading is the likelier one.
  - Realising the cold energy spherically lowers the in-plane rotation curve by only 0.5–1.5%.

## What touches the decisive tests

- **Gaia DR4.**
  - Arm C and the settling model predict γ = 1.000 structurally. The MW model enters only through the Galactic tide: 1.7–2.0e-3 of a 30-kAU pair's internal pull if the phantom disc exists, about 1e-4 otherwise. Either way that is far below σ_tot. **No bias.**
  - The prereg's "about 3e-4" tide ratio is the spherical figure. It would be about 6× larger with a phantom disc, and still negligible.
  - Arms A/B use the observed g_ext. The framework model's own g_obs(R₀) of 1.76 / 1.85e-10 lies inside the prereg's frozen 1.778–2.078e-10 bracket.
- **Satellites and UFDs.**
  - The UFD law offsets use each dwarf's own baryons and do not depend on the host profile.
  - Host-dependent inputs (CFG433's V_c, CFG463's apocentres and infall, CFG286's stripping at pericentre) move with f_ret only beyond about 50 kpc. Pericentres hardly move (a3 NONE).
  - CFG433's comparison used the bare law. That is right for f_ret = 0.18. It understates the tension for f_ret = 1 (4.06σ instead of 2.89σ).
- **No-EFE claims (PAPER44).**
  - Cassini and the clusters: no bias.
  - The TNO run's Galactic-tide term would be 31–34% stronger with a phantom disc. That run was already inconclusive.
  - Any EFE-rival test that uses MW satellites beyond about 100 kpc is limited by the host model (up to 0.19 dex in σ).

## Caveats and deviations (disclosed)

- **Satellite distances.** Galactocentric distances come from Fritz's own Table 2 d_GC column (on disk, same source), not the LVD as the frozen file said. They are the authors' values, and the C4 control (median pericentre error 2.2–2.3% against Fritz's Table 3) shows they work.
- **Approximations.**
  - Static spherical potentials throughout (orbits, timing). The record's growing-host runs (CFG463) are not redone.
  - Algebraic QUMOND for the phantom disc and the flattening.
  - Exponential vertical profiles with 0.3 kpc (stars) and 0.1 kpc (gas). The model's ρ_b,mid of 0.129 is above the recalled 0.084, which is why the post-run line uses the recalled value.
  - O-LG puts one LG phantom at the barycentre. M31 is treated as a point-mass framework system with 1.2e11 baryons.
- **Recalled inputs.** Literature halos, sky positions and distances for the microlensing lines of sight, the S-model, local-density and q measurements, and the quoted-error scales (15/20% mass, 20% local density, 25% halo-model, 2% stream V_c, 0.05 in q, 0.1 dex σ) are all RECALLED and UNVERIFIED. They are labelled in the output.
- **MUTATE.** Several MUTATE rows are equal by construction (a3, a4, d1, d2, e). The non-trivial ones are a1/a2 (orbits re-integrated in the truth), b/c/f/g/h (NFW refitted to an NFW truth, recovered to 4e-8 σ) and b2 (Kepler round trip).
- **f_ret.** f_ret = 1 is PAPER45's self-consistent simulation value. 0.18 is the record's census (CFG365 / CFG390). They are never pooled. The timing's 0.206 is a post hoc diagnostic, not a fit.
