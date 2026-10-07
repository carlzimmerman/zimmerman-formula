# CFG472 (lead L2): the law's target is NOT a Newtonian hydrostatic equilibrium of a pressure-supported cold fluid. Both of FL1's channels fail; the target is LESS concentrated near baryons than any such equilibrium

Criteria 73a141cee (committed before the script). Script `cfg472_l2.py` (~5 s). Units G = a₀ = M_b = 1; a footing only rescales r_M, so the dimensionless result holds on both. κ = ½ fitted. No DM particle; the cold mass is still required.

**What holds (K-A, sympy, PASS).** In the deep regime, ρ_ph = V_f²/(4πG r²) with V_f⁴ = G M a₀. That is exactly the singular isothermal sphere, and an isothermal fluid in a flat-curve potential has slope −V_f²/σ² = −2 iff σ² = V_f²/2. So far from the baryons, the law's target *is* a plain isothermal equilibrium, and the law only fixes its normalisation (the BTFR).

**What fails (the transition region, where baryons set the target).** Best-fit max deviation D of M_c(<r) from M_ph(<r) over 0.5–30 r_M:

| baryon scale a / r_M | Model I: isothermal, σ² = V_f²/2 fixed, 1 free ρ₀ | Model P: Thomas–Fermi P = Kρ², 2 free |
|---|---|---|
| 0.1 (compact) | **2.715 dex** | 0.486 |
| 0.3 | 0.334 | 0.474 |
| 1.0 | 0.108 | 0.513 |
| 3.0 (diffuse) | 0.276 | 0.482 |
| **verdict** | **SHAPE FAILS** | **SHAPE FAILS** |

**Reading.**
- Any equilibrium fluid piles up in the baryons' potential (Boltzmann factor exp(−Φ/σ²) for the isothermal, linear in −Φ for the polytrope). The law's phantom grows only like √M_b near the baryons.
- So **the target is under-concentrated relative to every Newtonian equilibrium of a cold fluid**, worst for compact (HSB) baryons.
- This agrees with CFG443: real collisionless cold matter in CFG378's halos is also more concentrated than the target.
- A settling force that holds the fluid at the target must therefore act *outward* relative to gravity wherever y ≳ 1: a repulsive, baryon-keyed term, not a pressure. That is a sharper statement of the G9 obstruction T3 found ("the force cannot be gravity-only").
- FL1's two pressure channels, alone, cannot be the settling force.

**Controls.**
- K-A PASS.
- **K-B FAILED as frozen** (no-baryon isothermal M_c/r over 10–100 = 0.944 vs 1 ± 0.05). The non-singular isothermal sphere oscillates about its SIS asymptote and had not converged there. Post-hoc (`cfg472_kb_posthoc.py`) it converges: 1.017 over 100–1000, and 0.995 with a smaller core. So the integrator is right, and the main run exits 1 because of K-B.
- **MUTATE** (target × r^0.3) gives D = 0.475 at a = 0.3: detected, exit 1.
