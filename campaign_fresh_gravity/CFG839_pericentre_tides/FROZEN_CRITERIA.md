# CFG839 FROZEN CRITERIA: does the satellite excess track PAST tidal stress (pericentre in the framework's own MW field)? (before any script)

**ID note:** last free ID of the owner-chat block 830–839.

**Why.** CFG838: no correlation with present-day tides. Satellites on eccentric orbits may have been heated at pericentre.
Gaia proper motions exist for the MW satellites, so orbits can be integrated in the framework's OWN Milky Way field (the law
applied to MW baryons; no ΛCDM halo).

## Sample and inputs
- The MW satellites among CFG828's 29 dwarfs with LVD pmra, pmdec, vlos_systemic, distance (heliocentric); Δ from CFG828
  (canonical, ν_e).
- Phase space → Galactocentric with astropy's default `Galactocentric` frame (R0 8.122 kpc, z_sun 20.8 pc,
  v_sun (12.9, 245.6, 7.78) km/s).
- MW field: spherical, g(r) = the law applied to G M_MW / r², M_MW = 6.0e10 M_⊙ (CFG821's value; bracket 8.0e10);
  Φ(r) = ∫ g dr. Turning points from E = v²/2 + Φ(r), L = |r × v|: roots of 2(E − Φ) − L²/r² = 0 → r_peri, r_apo.
- Tidal parameter at pericentre: T_p = |dg/dr|(r_peri) × r_1/2 / g_int, with g_int the law's field at r_1/2 from the dwarf's
  own stars (Υ_SFH, as CFG838). Also reported: the number of pericentres in 10 Gyr, n_p = 10 Gyr / T_r (radial period), and
  the cumulative stress S = n_p × T_p.

## Statistic and classes (primary M_MW)
- One-sided Spearman ρ(Δ, log T_p).
- **PAST TIDES IMPLICATED** if N ≥ 10, ρ > 0 with p < 0.05, and the 8e10 bracket keeps p < 0.10.
- **OPPOSITE** if ρ < 0 with one-sided p < 0.05. **NO SIGNAL** otherwise.
- Reported, not classed: ρ(Δ, log S), ρ(Δ, r_peri).

## Controls
- K1: Draco and Fornax r_peri / r_apo printed; energy conservation of a direct leapfrog integration of Draco's orbit over
  5 Gyr matches the turning-point solution to 2%.
- MUTATE (separate output): Δ_inj = 0.3 log T_p + N(0, 0.1) (seed 839) must class IMPLICATED; a shuffle must not.

κ = ½ fitted; cold energy mass required; not theory closed.
