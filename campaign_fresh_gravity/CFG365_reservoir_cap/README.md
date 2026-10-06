# CFG365: the supply cap keyed to the ORIGINAL baryon reservoir

Criteria: `FROZEN_CRITERIA.md`, committed alone first in f40786eea. Inputs are CFG364's committed rows (5e44cd0d9).

**Verdict: VIABLE (galaxy level), both footings.**

The rule is dark mass = min(phantom, 5.364 x M_b,now/f_ret). The cap does not bind in a galaxy as long as it kept at most f_req of its original baryons.

| | canonical | alt |
|---|---|---|
| smallest required retention f_req (at R_last) | 0.353 (UGC 5750) | 0.318 |
| massive galaxies, smallest f_req | 0.843 | 0.761 |
| galaxies needing f_ret < 0.18 (the census, all collapsed phases) | 0/175 | 0/175 |
| galaxies needing f_ret < 0.07 (the census, galaxies only) | 0/175 | 0/175 |
| observed-dark-mass version | 0 and 0 | 0 and 0 |
| system edge (EFE-frozen phantom), g_e = 0.01 / 0.03 a0 | f_req 0.56 / 1.01 | same |

The benchmark is the global baryon census, Shull, Smith & Danforth 2012 (ApJ 759, 23): galaxies, groups and clusters hold ~10% of the baryons, and collapsed phases including the CGM hold 18 +- 4%.

**Reading.**
- If each galaxy's cold supply is the cosmic share of the baryons it ORIGINALLY collected, every SPARC galaxy has enough. The worst case only needs to have lost about two-thirds of its baryons. The census says galaxies on average kept ~10%, so the supply exceeds the phantom by a factor of ~3-10. The cap is then inert inside galaxies, and the a0 law is untouched.
- **Consistency with cm10.** At census retention the law uses only ~10-35% of each system's cold supply. The remainder (~65-90%) is cold mass the phantom does not need. That brackets cm10's independently derived "75-81% must sit outside halo apertures".

**What this does NOT show.**
- Galaxy level only. Whether a reservoir cap removes the growth / lensing double count needs the PM run. The orchestrator's CFG361 machinery would source dark = min(phantom, local real cold mass).
- The census is a cosmic mean. Per-galaxy retention is not predicted by the framework.
- Supply is a COUNT, not a location: this does not show the cold mass sits where the phantom profile needs it. The mechanism that arranges it (CFG9's equilibrium; CFG60: none committed) is still missing.

Controls 2/2 plus T-MUT. MUTATE (supply x 0.1): 16-24 galaxies need f_ret < 0.07 and the verdict flips to DEAD, rc 1.

Run: `python3 cfg365_reservoir_cap.py` (seconds).
