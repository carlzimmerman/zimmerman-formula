# CFG839 — does the satellite excess track past tidal stress (pericentre in the framework's own MW field)?

Criteria: `FROZEN_CRITERIA.md` (288ab33eb, before the script). Run: `python3 cfg839.py` (MUTATE `CFG839_MUTATE=1`). ~1 min.
Orbits: Gaia proper motions + LVD systemic velocities and distances, astropy default Galactocentric frame, in the
framework's own Milky Way field (the law applied to 6e10 M_⊙ of baryons, spherical; no ΛCDM halo).

## Result — CLASS: **NO SIGNAL**
- 12 MW satellites: ρ(Δ, log T_peri) = +0.08 (p 0.41); 8e10 bracket +0.10 (p 0.37). Cumulative stress ρ(Δ, log S) = +0.15
  (p 0.32); pericentre distance ρ = −0.06.
- Framework pericentres: Draco 53, Ursa Minor 47, Sculptor 64, Fornax 82, Carina 107, Leo I 56, CVn II 21, Sagittarius
  16 kpc. Tidal stress at pericentre is still weak for all but Sagittarius (log T_p ≤ −1.4).
- Post-hoc (not a class): dropping Sagittarius (being disrupted; Δ = 0) gives ρ = +0.40, p = 0.11 — a weak hint that the
  most-stressed bound satellites (CVn II, UMi, CVn I, Draco) carry more excess. Not significant.
- **Reading:** neither present-day (CFG838) nor pericentric tides explain the satellite excess at the frozen bar. What is
  left: binaries / kinematic systematics in faint systems, non-equilibrium beyond the tidal estimate, or real bound mass in
  satellites. CFG829 stands: isolated galaxies at the same g_bar show no excess.

## Controls
- K1 PASS: Draco turning points 53.4 / 120.0 kpc = a 5-Gyr leapfrog integration (53.4 / 120.0).
- MUTATE bites: injected Δ = 0.3 log T_p → IMPLICATED (ρ +0.74); shuffle → not (ρ −0.31).

κ = ½ fitted; cold energy mass required; not theory closed.
