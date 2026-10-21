# CFG930 AMENDMENT A1 (2026-10-20): implementation clarifications

**Timing.** Written while coding cfg930.py, BEFORE any run of it: no K, MUTATE or main output existed, and no number of this
lane had been computed. No class rule, threshold, calibrator, corner or primary choice changes. Each item below either
resolves an ambiguity in FROZEN_CRITERIA.md (3dec25afe) or records a numerical detail.

1. **Cluster primary corner.** §4.1 names an AGN bracket {0, 3e62 erg} but no primary value. The primary cluster point is
   therefore M_b = 1.2 × median MGAS500 with bcg_med, and BOTH AGN values must lie in the window for CONSISTENT. CONTRADICTED
   stays as frozen: all 12 corners lie outside, on the same side. Anything else is UNDERDETERMINED. Under R1 the cluster
   class is NOT EVALUATED, because the debris-projection comparison is defined only for the sum form.
2. **f_s edge cases.**
   - In the sum form, ε = 0 gives f_s = 0.
   - If no debris lies inside r_e (ΔE = 0), f_s = 1, since there is nothing to settle.
   - In R1, ΔU ≤ 0 gives f_s = 1 at every ε (criteria §3.4).
   - ε → ∞ gives f_s = 1.
3. **SPARC Υ-floor worlds.** A point whose g_bar ≤ 0 at the varied Υ_disk/Υ_bulge is dropped in that world only. The number
   dropped is recorded. A galaxy with no points left is skipped in that world.
4. **Numerics.**
   - ΔE and ΔU: Simpson's rule on 2401-point logarithmic grids, from 1e-6 r_e to r_e and from 1e-7 R_max to R_max.
   - Form-B table: cumulative trapezoid.
   - σ(M): a 0.01-dex grid in log M from 1 to 1e17 M☉; k from 1e-4 to 1e5 h/Mpc on 9001 logarithmic points.
   - Native D(z): inverted by linear interpolation of the CFG654 table.
   - Δ_ta(z_ta): linear interpolation in z of cfg654_delta_ta_cmb.json.
   - Native t(a): integrated from a = e^-20, with the radiation-era start term.
   - Projected debris mass: the 3D mass inside R plus the shell integral with r = R cosh u (4001 points).
5. **K-world constants.** K1b, M0, the K half of M∞ and MK use CFG42's own hunt_lib footing values (9.36e-11 / 1.13e-10) and its
   kernel (a_int), so that CFG42 is reproduced exactly. All native runs use the exact footings 9.3603e-11 / 1.1312e-10. In
   the K-world the collapse mass follows CFG42's conventions:
   - halo_mass(2 L_V), held fixed in the Υ-floor worlds;
   - SPARC: halo_mass(0.5 L[3.6]);
   - isolated dwarfs: halo_mass(2 L_V).
6. **R1's f_s = 1 limit is the supply-capped law,** M_set(<r) = min(M_ph(<r), M_c). Where the census supply is below the phantom
   at an aperture, R1 at f_s = 1 lies below the bare law. This is possible for the most diffuse dwarfs (CFG823: q_settled > 1
   for Antlia II and Crater II). M∞ therefore checks N-A and N-B against the bare law, checks R1 against the capped law, and
   reports the number of capped objects.
7. **D2 at the primary corner.** Under N-A there is no debris (ΔE = 0), so f_s is undefined. D2 is evaluated with the N-B
   debris energy at the same (C, r_b, supply), i.e. corner NB|C3000|rta|x1, and at F*. ε is that corner's ε*, or else the
   A-set midpoint (the middle positive grid point of A).
8. **A-set beside a root:** computed at every corner on the 42-point grid and stored. It carries no weight when a root exists.
9. **D5:** the per-object maximum over f_s ∈ {0, 0.005, …, 1}, then the class statistic of §4 on those maxima.
10. **S2 and S3 construction.**
    - S2 dSph comparator: M_formed = M*/M(*+remn) of a 13.3-Gyr burst at [M/H] −1.31.
    - S2 rotator: M_formed = M*/m_rem for a constant SFR at [M/H] −1.31.
    - The aperture is set by g_bar = G (M_b/2)/r_ap², with the Plummer half-mass radius at r_ap.
    - Numbers are written for the primary corner and for F*, at each footing's ε* or A-set midpoint.
    - S3 uses the 14 MW classicals of class C. The non-blind check uses CFG827's 8 MW training dwarfs (Sculptor, Draco,
      Ursa Minor, Canes Venatici I, Leo II, Carina, Fornax, Leo I).
11. **Name matching for M_formed:** lower case; "andromeda" → "and"; spaces, underscores and dots removed; plus aliases
    And1–And13 → Andromeda I–XIII. The match list is printed in the K run. Unmatched objects use the burst rule.

κ = ½ is FITTED. The footings are never pooled. Not "theory closed".
