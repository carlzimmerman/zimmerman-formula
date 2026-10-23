# U1_v3_dust_content: how much dust, and how much gravity, can v3's own equations give a system?

## Verdict: CRISP FINDING

v3's own dust dynamics fixes the range; history cannot widen it where the tiles need more gravity.

1. **Held dust never adds gravity beyond static AQUAL inside μ_K⁻¹.** Literal static v3 is unique (dust = the AQUAL
   phantom). Isotropic hot dust stays at or below the phantom at every radius (theorem T1, checked on 14,373 equilibria:
   the largest ratio is 0.666). Anisotropy and infall exceed it only near the centre, never at r½.
2. **Held dust is weightless in its host (theorem T3).** In a static host, the khronon acceleration that makes the
   external-field effect (EFE) is exactly the force that pulls a hosted system's stars away from its dust. A system that
   falls with its host therefore carries no dust and is Newtonian.
3. **Consequences:**
   - The satellites and Coma UDGs move further from v3 (+2.0 dex, +1.4 dex): STRUCTURAL.
   - TDGs and DF2/DF4 become a NATIVE pass with no knob.
   - MW K_z is STRUCTURAL in literal v3 and HISTORY-DEPENDENT for multi-stream dust.
   - Field galaxies keep their phantom at the BS cap (relative speed ≲ 2 km/s). Group members lose it in v3 if the group's
     dust is held, but Ursa Major's members contradict that branch.

**Checks.** κ = ½ is FITTED. Footings are canonical / alt, never pooled. The extra mass is cold energy (BS dust), not a
particle. Not "theory closed". Nothing here says the data favour the framework.

| Run | Checks | Notes |
|---|---|---|
| main | **15/16 PASS** | N4 FAILS as frozen on grid resolution (A3) |
| field-frame (A2) | **6/6 PASS** | |
| `--mutate` | D4, D7, N1 / F1, F2 FAIL as required | |
| reruns (10-23) | main mutate 10/16, exit 1 (962 s, 0.32 GB): D4, D7, N1 FAIL as required (also N2, N3, N4); D1–D3, D5, D6, N0 PASS. A deterministic rerun of the main script and clean reruns of the A2 script (normal + mutate) match the committed JSONs in every number; only runtime/RSS differ | |

## The two readings of the dust

- **LIT**: BS's literal khronon. Single-stream and irrotational (v = −∇σ, σ single-valued). ρ_τ is whatever the hold
  equation gives, with no sign requirement.
- **MS**: posited multi-stream particle dust, ρ_τ ≥ 0, any velocity distribution (as in L1's engine).

## Part (a): bounds

**The ψ equation (D1, sympy residual 0).** The dust feels ψ = Φ − Ξ, and

    ∇²ψ = 4πGρ_b − ∇·[μ(|∇Ξ|/a₀)∇Ξ] − μ_K²Ξ.

- So Ξ obeys AQUAL with source ρ_b − ∇²ψ/4πG. Cold dust at rest needs ψ = const, which is AQUAL.
- The single-stream Euler equation is the gradient of the definition of Ξ (Bernoulli).

**Literal statics (D2).** Static single-stream means σ = −Ct, so Ξ = Φ + C, which is BS24 Eq. 35.
- At μ_K = 0 the AQUAL flux x²/(1+x) and the hold flux x/(1+x) both increase strictly. The static solution is therefore
  unique: **dust = the phantom, a single point, not a range**.
- With μ_K ≠ 0, the constant C adds a uniform K-dust −μ_K²C/4πG, and sin(μ_K r)/r is a regular homogeneous mode. The
  zero point is free (S4 scans it).

**When μ_K can be dropped (N7).** For satellites at the BS cap (14.8 h/Mpc), ε_K has median 4.8e-3 and maximum 0.12.
- To matter, the zero point would have to move by about 1e-3 c² (cap) or 4e2 c² (BS24's own μ_K).
- For a 1e14 M☉ cluster at 0.3 / 1 Mpc, ε_K = 31 / 151 at the cap: **not negligible**. At BS24's own μ_K it is 7e-5 / 4e-4.
- For Coma UDGs, the generous zero point gives ε_K up to 8. Coma's measured local density excludes that zero point (A3).

**The hold cap (D3).** |(1−μ)∇Ξ| = a₀x/(1+x) < a₀. This gives:
- G·M_τ(V) < a₀·|∂V|/4π for any region V;
- for a sphere, M_τ(<r) < a₀r²/G;
- for a sheet, Σ_τ < a₀/2πG;
- for spherical systems, g < g_N + a₀.

The phantom sits inside the cap. The cap allows far more than the tiles need, so it is never the binding limit.

**Force on spherical dust (D4).** −ψ′ = −a₀[n − m²/(1−m)], with n = GM_b(<r)/a₀r² and m = GM_τ(<r)/a₀r². It vanishes
exactly at the phantom.
- ∂/∂m = −m(2−m)/(1−m)²: held dust is self-repulsive at m > 0 and neutral at m → 0 (the record's D-T).
- **Corollary:** ψ′ ≤ g_N,b. Held dust is bound only by the baryons' Newtonian well. For the satellites, that well's escape
  speed is a median **0.39 / 0.40 of the observed σ**, so dust moving like the stars escapes.

**T1 (MS, spherical, μ_K = 0, f = f(E) or ∂f/∂L ≥ 0, with ρ_ph(r) non-increasing): M_τ(<r) ≤ M_ph(<r) at every r.**
*Proof sketch.*
1. Let u = M_τ − M_ph. By D4, sign ψ′ = −sign u.
2. Where u > 0, ψ decreases outward, so ρ_τ(r) is non-decreasing there (∂ρ/∂ψ ≤ 0, ∂ρ/∂r|_ψ ≥ 0).
3. An excess that starts at r_a with u(r_a) = 0 needs ρ_τ > ρ_ph at some r₂.
4. Beyond r₂, ρ_τ ≥ ρ_τ(r₂) > ρ_ph(r₂) ≥ ρ_ph(r), so u keeps growing. The dust mass then grows like r³ and breaks the cap. ∎

**Geometry-free form (D5).** For any dust shape, the virial of the dust's self-interaction is W_self ≥ 0.
- This uses the Derrick identity, Thomson's theorem, and f(u) = 3(u − ln(1+u)) − u²/(1+u) − u²/2(1+u)² ≥ 0.
- So the baryons must bind the dust at least as strongly as the dust repels itself.

**Numerical check of T1 (N1).** 137 system–footing cases: S1's 45/46 satellites, 9 Coma UDGs, P4's 6 TDGs (uniform and
Plummer) and DF2/DF4, all isolated. King and polytrope families, plus A1's near-cold and n = 2–2.5 grids.
- 14,373 finite equilibria. **Largest M_τ/M_ph = 0.666.** Largest gravity gain at any radius = **−0.11 dex**.
- All 52,544 configurations that passed the phantom ran away to the cap, as the proof says.
- ρ_ph is non-increasing in every case.

**Counterexamples tried before calling T1 a theorem:**

| Attempt | Result |
|---|---|
| Radial anisotropy, f = L^(−2β) g(E) (N2) | For β ≤ 0, at most 0.36 of the phantom. For β > ¼, a central excess appears (ratio up to 34, gain up to +1.5 dex at small radii). Every excess starts where r^(2β)ρ_ph still rises (generalised T1, 0 violations). **The gain at r½ is at most −0.12 dex.** |
| Time-dependent infall (N3, shell code with angular momentum and the exact hold energy) | Excess dust is expelled: λ = 3 relaxes to 0.28–0.35. A collapsing cloud reaches 0.10 / 0.34 of the phantom. Cold radial infall overshoots transiently (1.09 / 1.15) and leaves a radial remnant at most 6 % above it at r½. Dust given the stars' kinematics (0.5 v_c) is unbound, at 1.3–5.7 × the baryonic escape speed. |
| Flattened systems | Literal statics are unique for any geometry. D5 gives a geometry-free virial bound. A pointwise disc theorem is OPEN; the MW is computed in N6. |
| Uniform external field (D6) | The held dust's self-coupling c_θ = (f_θk² − μ_K²)/((1−f_θ)k² + μ_K²) ≥ 0: **self-repulsive on scales below √f_θ/μ_K**. Hot isotropic dust holds phantom_k × k_D²/(k² + k_D²), within [0, 1] for every mode. |
| Sign of the dust density (N4) | The linear-EFE AQUAL phantom of a Plummer has 22–38 % negative mass. LIT allows it; MS dust cannot reproduce static AQUAL in a field exactly. |
| μ_K² term at r ~ μ_K⁻¹ | **The bound fails there.** For k < aμ_K the dust feels its own gravity again (s → 1), so self-bound K-dust beyond the phantom is allowed. At the BS cap this starts at about 0.1 Mpc. |

## T3: held dust is weightless in a static host (D7 + N4)

- A static host has Ξ_host = Φ_host + C, so ψ_host is constant: **the host exerts no force on any dust**. Its baryons still
  feel g_host.
- The total hold force on a localised dust blob is M_τ∇Ξ_host. This is a Bekenstein–Milgrom-type stress identity, exact
  in sympy for a linear medium. Nonlinear 3-D check (N4): self-force ≤ 8.7e-5 in 8 of 9 cells, 2.3e-3 in the strongest
  (3.6e-4 with a smoother blob).
- By momentum, a bound unit falls at **a = g_host·M_b/(M_b + M_τ)**.
- The baryons can drag dust only through their Newtonian pull. By the shell theorem they cannot drag dust outside them.
  Dust is therefore held only where the internal field exceeds |∇Ξ_host|, and **|∇Ξ_host| is the EFE strength itself**.
- So the static AQUAL-with-EFE solution needs the baryons held at rest relative to the host's dust. **A freely falling
  EFE-dominated system cannot keep its EFE phantom.**
- The host's measured field pins this: h = a₀m/(1−m) ≥ g_host − g_N,host. A weaker EFE would need a weaker host field than
  is measured.

## Part (b): velocity, and which frame

- **Reference frame.** The local khronon flow is the dust velocity field; v3 has no other frame. Inside a static host it is
  the host's held-dust frame (the host's rest frame).
- **On large scales dust and baryons move together (A2, F1, sympy).** The baryon–dust differential acceleration is
  s·∇Φ_τ with s = k²/(k² + a²μ_K²): full for k ≫ aμ_K, suppressed as (k/aμ_K)² for k ≪ aμ_K. Bulk flows matter only through
  their k > aμ_K part.
- **Literal reading.** A system moving at V_rel through its local khronon holds dust only where **2GM_b(<r)/r ≥ V_rel²**
  (D6: stream pole at ω_p; BSK1 M6). The relevant speed is the baryonic Newtonian one, not σ_sys, because the dust's own
  gravity cannot hold dust.
- **Multi-stream reading.** Uniform motion alone does not strip bound particles. Acceleration does (T3).
- **Record speeds** (MW satellites from LVD 3-D motions, 32 systems; others PROXY): median 193 / 200 km/s. Held dust inside
  r½ is a median **0 %** of the static phantom in both readings.
- **Native capture law, zero knobs:** a system that falls with its host carries no dust. Its maximum held dust is the
  isolated phantom inside r_h, where g_int(r_h) = |∇Ξ_host|, and it then falls at g·M_b/(M_b + M_τ).

## Part (c): consequence table (canonical / alt)

| Tile | Static v3 (S1/P4) | v3's own dynamics (this lane) | Class | What would have to change |
|---|---|---|---|---|
| 26 satellites (median Δ log g, central values, bootstrap sd) | +1.28 ± 0.12 / +1.28 ± 0.12 (S1 MC: +1.33 / +1.30) | Dust-free (B0) **+2.00 ± 0.08 / +1.99 ± 0.07**. Max-hold B1-MS +1.96 / +1.94. Even isolated AQUAL (not available in a host) +0.52 / +0.47 | **STRUCTURAL** | **The dust coupling**: held dust has inertia but no weight in a held host, and is bound only by the baryons' Newtonian well. **J/the law too**, since isolated AQUAL is still 6σ short |
| 29 Coma UDGs (⟨E⟩, z_sys) | +1.12 dex, z_sys 4.3 / +1.08 dex, 4.1 | **+1.41 dex, z_sys 5.4** on both footings (r_h = 0 for all 9) | **STRUCTURAL** | The dust coupling (T3). Isolated, they would be within 1.6σ, but Coma's measured field pins the EFE |
| 19 TDGs (r̄ ± se) | −0.59 / −0.62 dex | B0 **+0.055 ± 0.114** (0.5 se). B1-LIT = B0. B1-MS −0.28 / −0.30 | **NATIVE pass** | none: TDGs fall with their tidal debris and cannot hold dust (internal field < g_e = 0.15–0.28 a₀) |
| 19 DF2 / DF4 | −1.66 / −1.74 ln | B0: r = +0.30 / −0.24 ln; σ_pred 7.3 / 7.1 km/s vs 8.5 / 6.3 | **NATIVE pass** | none (B1-MS would sit at the law, −1.5 / −2.2 ln) |
| MW K_z,1.1 | 92.3 / 96.9; χ² 178 / 251 vs 67.5 | LIT: unique static AQUAL, unchanged. MS: round dust at the T1 bound gives K_z(R₀) **71.1 / 72.4**, **χ²_Kz 43.9 / 42.5**; baryons alone 62.0, χ² 88.3 | **LIT STRUCTURAL; MS HISTORY-DEPENDENT** (needs hot, round dust) | LIT: J/the law (the cold phantom is disc-like) |
| MW v_c(R₀) | 215 / 220 | **≤ 215.6 / 220.6 km/s in every branch** vs Eilers 229.1 ± 4.6 (2.9σ / 1.8σ short). Round dust tuned to K_z = 66.4 gives 196.9 | TENSION (all branches) | the law (T1 caps the dust) |
| Cluster cores | ×1.5–1.9 (F1) | Inside μ_K⁻¹ the bound holds: no excess. At BS24's own μ_K the whole core is inside: **STRUCTURAL**. At the cap (ε_K 31–151 at 0.3–1 Mpc) the bound fails: self-bound K-dust is allowed, but that is a CDM-like component (CFG946), and F1/H2 found no profile that fits. The static family is S4's | **STRUCTURAL** at BS24's μ_K; **OPEN at the cap** (S4) | μ_K (or J) |

## A2: the field-galaxy frame (frozen 616ad70e96 before any number)

**Linear v3 relative velocity at z = 0 (F2).** CLASS model B, F3's ODE, with F3 K4 reproduced to 0.0. The table gives the
rms baryon speed / rms baryon–dust relative speed.

| μ_K | k ≤ 0.3 h/Mpc | k ≤ 1 | k ≤ 50 | Share of baryon velocity not carried by dust at k = 0.01 / 0.1 / 1 / 10 |
|---|---|---|---|---|
| BS24 own (0.0228 h/Mpc) | 53 / **30** km/s | 56 / 31 | 56 / 32 | 0.35 / 0.64 / 0.65 / 0.65 |
| BS cap (14.8 h/Mpc) | 324 / **0.46** | 326 / 0.90 | 326 / 1.8 | 0 / 0.002 / 0.05 / 0.45 |
| M1 growth (411 h/Mpc) | 493 / 0.01 | 510 / 0.02 | 512 / 0.11 | 0 / 0 / 0 / 0.013 |

The post-recombination streaming today is 0.03 km/s (EXTERNAL).

**SPARC hold radii (F3, 175 galaxies, 3,391 points, Υ 0.5 / 0.7).** V_hold = √2·V_bar has median 103 km/s (64 km/s at the
last point). Fraction of RAR points not held, by V_rel:

| V_rel (km/s) | 1 | 3 | 10 | 30 | 100 | 300 |
|---|---|---|---|---|---|---|
| Points not held | 0.1 % | 0.2 % | 1.4 % | 12.8 % | 49 % | 89 % |

**Held surroundings (F4, 109 Chae-matched galaxies).** g_obs < g_e at **1.0 % / 1.2 %** of points if the environment's
dust is held. At the cap it is unheld for a source at 1 Mpc (s = 0.28): 0 % / 0.06 %.

**Ursa Major members (F5).** 28 members; σ_LOS of cz = 115 km/s, so V_rel = 199 km/s.
- 81 % of their points have V_hold < V_rel (counted at any radius, not only beyond r_f), so in a held UMa they would be dust-free: **−0.44 / −0.47 dex** below the RAR.
- Observed: **−0.042 ± 0.009 / −0.038 ± 0.010 dex** against field points in the same g_bar bins.

**Verdict (frozen readings):**
- **Field galaxies: KEPT at the BS cap and at M1's μ_K.** σ_rel ≤ 1.8 km/s leaves at most 0.2 % of points unheld, and held
  surroundings affect 1 %. Bulk flows (σ_b ≈ 326 km/s) are carried by the dust.
- **At BS24's own μ_K: DEPENDS** on the flow amplitude. v3's own σ_rel ≈ 30 km/s loses 12.8 % of RAR points (8.6 % of
  galaxies inside R_last/2). With the observed ~300 km/s flows and share 0.64, the phantom would be lost almost everywhere.
  That μ_K already fails growth (F3).
- **Group members (class UMa): LOST if the group's dust is held** (81 % of points to Newton). The data contradict this at
  ~40σ statistical (−0.04 vs −0.44 dex). So either a loose group's khronon is not held, which v3 does not establish, or v3
  fails for group members. **DEPENDS ON that unestablished assumption; the favourable one is not assumed.**
- **Tiles that change if held groups strip their members:**
  - SPARC RAR: 28 UMa members, plus other group members;
  - MeerKAT: environments not on disk;
  - isolated-lens stacks: lenses in groups;
  - cluster member lensing;
  - and tiles 26 / 29 / 19 as above (already computed).

## What this does not show

- No disc-geometry theorem; T1 is spherical. The MW round-dust result uses the monopole bound as an upper envelope. The λ
  scan is reported, not fitted.
- B1 uses the isolated, unscreened (L★ = 0) phantom inside r_h: an upper bound on held dust. r_h uses the isolated
  internal field.
- PROXY speeds (M31 satellites, TDGs, Coma) are record-derived. DF2/DF4 use CFG657's V_coll/2.
- The cluster cores at the BS cap are not decided here (S4).
- Linear relative velocities beyond k ≈ 0.3 h/Mpc are indicative only.
- No satellite acceleration is measured. T3's "satellites must be dust-free" rests on their bound orbits at V ≈ v_c,host:
  a dust-dominated satellite would fall at only M_b/M_dyn of g_host.

## Record items this changes

- S1/P4's static EFE values for hosted systems are not v3's dynamical prediction. A freely falling EFE-dominated system
  is dust-free (T3).
- P1's "supply exists but no binding mechanism" is now exact: held dust is bound by at most the baryons' Newtonian well
  (D4 corollary).
- BSK1 M6's r_follow = 2GM_b/du² is the stationary criterion here too. A uniformly moving galaxy keeps its phantom only if
  its khronon co-moves, and on scales > μ_K⁻¹ it does.

## Run, files, commits

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/U1_v3_dust_content/u1_v3_dust_content.py        # ~15 min, exit 1 (N4)
U1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/U1_v3_dust_content/u1_v3_dust_content.py
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/U1_v3_dust_content/u1_a2_field_frame.py         # seconds, exit 0
U1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/U1_v3_dust_content/u1_a2_field_frame.py
```

- On macOS the scripts re-exec themselves with MallocMediumZone=0. Without it, freed FFT buffers stay resident: N4 reached
  1.1 GB RSS with < 0.1 GB live. Peak is now 0.32 GB.
- Outputs: `*.out`, `*_results.json`, `u1_satellites_per_system.csv`, and the `*_MUTATE.*` files.
- Criteria commits: edb372c22d (criteria + ledger, alone first), fbd28ee9b7 (A1, pre-result), 616ad70e96 (A2, pre-result).
  A3 (post-result) and the result are in the same commit as this README. Nothing was downloaded.
