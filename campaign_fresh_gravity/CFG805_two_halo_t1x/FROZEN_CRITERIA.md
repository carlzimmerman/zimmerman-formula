# CFG805 FROZEN CRITERIA: the framework's own two-halo term (neighbours' cold energy) on KiDS lensing beyond 0.4 Mpc (committed before any script)

**Context.** CFG804 showed that the derived catchment supply fits KiDS-1000 inside 0.31 Mpc, but falls short over all
radii (Δχ² +149) beyond each galaxy's catchment edge (320–450 kpc). Neighbours' cold energy and baryons also lens. That is
the two-halo term, and it was not computed.

**Two-halo template, framework-native.**
- Source: T1x's own gravitating power spectrum P_grav(k) at z = 0.2562 (CFG650 T1x snapshot x0.2562; comoving Mpc/h,
  h = 0.6736).
- ξ(r) is its Fourier transform.
- Exclusion: ξ = 0 inside each bin's derived catchment edge (CFG804), so the galaxy's own catchment is not counted twice.
- Projection: Σ_2h(R) = b ρ̄_m ∫ ξ(√(R² + t²)) dt, then ΔΣ_2h = Σ̄(<R) − Σ(R). Converted to physical units at
  z = 0.256, with ρ̄_m = Ω_m ρ_crit, Ω_m from T1x's own parameters.
- b ≥ 0 is the effective lens–matter bias of the isolated sample, profiled per bin together with M_b. It is the same
  freedom for both models; the isolation criterion suppresses neighbours, so b_eff < 1 is allowed.

**Inherited caveat (disclosed).** T1x used inherited ΛCDM initial conditions and background. The NC1x native rerun is
queued.

**Models.**
- **B + 2h:** no edge plus two-halo.
- **D_der + 2h:** CFG804 derived catchment edge plus two-halo.

**Classes** (all radii, the CFG804 failing range):
- **OUTER GAP CLOSED** if Δχ²(D_der + 2h − B + 2h) ≤ 4 AND p(D_der + 2h) ≥ 0.01.
- **NARROWED** if Δχ² falls by more than half from +149 but the CLOSED test fails.
- **OPEN** otherwise.

Report b per bin and the primary range as well.

**Controls.**
- K1: b = 0 reproduces CFG804's all-radii Δχ² (+148.7) within 0.5.
- K2: σ8 recomputed from P_grav at z = 0.2562 matches the snapshot's sigma8_grav (0.779) within 2%.
- MUTATE (separate outputs): the exclusion radius set to 0 (no exclusion) must change b by more than 10%, showing the
  exclusion bites.

κ fitted; not theory closed. Bin masses provisional, as in CFG801.
