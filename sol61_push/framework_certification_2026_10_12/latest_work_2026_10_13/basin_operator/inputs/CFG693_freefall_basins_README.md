# CFG693: the gap as a definition — each system reads its own free-fall basin

**Label: THE GAP IS DEFINED (frozen tests T1–T3 pass). POST-HOC: the definition alone turns every star "on" (about 51 M☉ of
phantom per M☉ inside its basin). A hierarchy rule is required. CFG691's stiffness supplies one; the combination is not yet
computed. Definition, not action: R0, B1, M1a unchanged.**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (45ff137aa), 2026-10-12. Block CFG690–699.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory
  closed"; nothing here says the data favour the framework.
- **Script:** `python3 cfg693.py` (sympy, seconds, exit 0) → `cfg693.out`, `cfg693_results.json`. `CFG693_MUTATE=1` exits 1 as
  designed (both teeth bite).

## The definition
- **Free-fall potential.** Φ_F is the potential in a system's non-rotating free-fall frame: the external field's value and
  uniform gradient are removed (equivalence principle; in GR, g₀₀ in Fermi normal coordinates along the system's centre).
- **Basin.** The system's basin is the largest closed level surface of Φ_F around its minimum. Basins form a merge tree, as in
  Morse theory or watershed segmentation in image analysis.
- **Reading.** Each node's response reads its own baryons through the Gauss flux density 4πG m_b/A. In CFG692's polarizable
  vacuum, this sets the susceptibility per node instead of from the local |g|.

## Results

| test | result |
|---|---|
| **T1** EFE-blind | a uniform g_e has zero flux through every closed surface, and the free-fall subtraction removes it from Φ_F exactly. PASS. *Honest note: this is true by construction; the content is in T2.* |
| **T2** basin edge vs the data's aperture | free-fall saddle r_J = V_s/√T_h. **r_J/r_bg = √((3 − α)/(α − 1)) = 1 exactly for an isothermal host (α = 2)**: 1.73 / 1.29 / 1.00 / 0.78 / 0.58 at α = 1.5 / 1.75 / 2 / 2.25 / 2.5. The plain static saddle sits at only 0.05–0.28 r_bg (V_s/V_h = 0.05–0.3). PASS |
| **T3** the Sun | Galactic tide T = 8.5e-31 s⁻² ⇒ the Sun's basin r_J = **1.74 pc**; r_M(Sun) = 0.034 pc. Wide binaries (≤ 0.1 pc) are inside, so they follow the law with their own mass and no EFE. Cassini: the Sun's own node has Q2 = 0; the Galactic tide is 1.6e-4 of the Q2 ceiling. PASS |
| T4 (reported) | across r_J a deep satellite's own field drops to 0, a jump of V_s/V_h (10–20%) of the host's field there. At a merger the parent node switches on from 0. Persistence weighting is named as the smoothing; not built |
| MUTATE | M1 plain static potential: the basin depends on g_e (saddle √(GM/g_e)), and the static saddle/r_bg at V_s/V_h = 0.15 is 0.147. M2 local \|g\| depends on g_e. Both bite |

## Reading
1. **The equivalence principle supplies "own baryons".** A system in free fall cannot feel a uniform external field, so a
   response that reads Gauss flux over its own free-fall basin is EFE-blind with no new constant.
2. **The basin ends where the data's aperture ends.** For an isothermal host, the free-fall basin's edge is exactly Sifón et
   al.'s density-match radius. So the satellites keep their own boost over the whole lensing aperture, which reproduces
   PAPER44's no-EFE fit (χ² 0.7) and not the excluded "ownership" model (131.6). Without the free-fall subtraction the basin
   would end 4–20× too early. That is why the equivalence principle is the needed ingredient, not just plain level sets.
   (Tidal radius ≈ density-match radius is a standard result; what is new here is its role as the switch's edge.)
3. **The Solar System is clean.** The Sun reads only itself (Q2 = 0), consistent with the record's own finding that removing
   the EFE gives Q2 = 0.

## POST-HOC caveat (found after the frozen run; not in the criteria)
**Every star is a node.**
- The Sun's own phantom inside its basin would be M_ph = M r_J/r_M ≈ **51 M☉**. Neighbouring stars cut the basins to about
  0.6 pc (watershed), which still leaves about 17× the stellar density.
- Local vertical dynamics put the solar neighbourhood's dynamical density close to its baryonic density, not 17×. This is a
  standard result, quoted here as order of magnitude; it is not a committed lane.
- Scale invariance makes a star's basin look like a dwarf galaxy's, so no dimensionless basin property separates them. The
  record already flags this as "Sun ON by every monotone gate" (CFG48 G2).

**A candidate resolution, not computed:** CFG691's stiffness screens compact bodies and not extended ones.
- ℓ_γ(Sun) ≈ 430 pc ≫ its basin, so inside the basin only the constant pull GM/L*² survives. The star's phantom is then
  M (r/L*)² ≤ 0.09 M☉ at L* = 5.75 pc.
- ℓ_γ(10⁷ M☉) ≈ 0.14 pc ≪ a dwarf's half-light radius, so dwarfs keep their boost.

**The combined construction** (critical polarizable vacuum + stiffness + free-fall basins) predicts:
- full boost for satellites;
- Newtonian wide binaries (screened, despite being inside the Sun's basin);
- partially screened faintest UFDs.

It has not been run. The stiffness result is for astra's sector, not CFG692's medium.
