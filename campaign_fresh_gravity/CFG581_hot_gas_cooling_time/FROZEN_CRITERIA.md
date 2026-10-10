# CFG581 FROZEN CRITERIA — can the hidden gas of CFG580 persist? (cooling time vs free-fall time)

(owner chat 10-09, "yes do the cooling time check"). Committed alone before any script. No new downloads: AtomDB
v3.1.3 already local (CFG580).

Gas: CFG580's required mass f·M*, f = 0.8 (canonical) / 0.55 (alt), M* = 10^10.8 (variants 10.7, 10.9), in a
uniform sphere of 100 kpc (minimum density for that mass inside 100 kpc → the LONGEST cooling time; most
favourable to the escape). Only the cells where CFG580 found the gas HIDDEN (L < 1.9e40 erg/s) are scored:
kT ∈ [0.10, 0.13] keV, Z ∈ {0.1, 0.3, 1.0} Z☉, per footing.
Cooling: Λ(T, Z) = APEC bolometric radiative emissivity (0.001–20 keV) per n_e n_H from pyatomdb (same abundances
as CFG580); t_cool = (3/2)(n_e + n_ion) kT / (n_e n_H Λ), n_e = 1.2 n_H, n_ion = 1.1 n_H.
Free fall at r = 100 kpc in the law's own field: v_c⁴ = G M_b a0 (deep-law limit, M_b = (1 + f) M*), each footing's
a0; t_ff = √2 r / v_c. (Also reported: the circular speed and the hydrostatic kT ≈ μ m_p v_c² / 2.)
Verdict per footing:
 ESCAPE UNPHYSICAL iff t_cool / t_ff < 10 in EVERY hidden cell (the gas would condense out: precipitation
  threshold of thermally unstable halos, ~10, PROVISIONAL literature value declared now), at log M* 10.8.
 ESCAPE PHYSICALLY ALLOWED if t_cool / t_ff ≥ 10 in some hidden cell.
 Overall = same call on both footings, else SPLIT.
Reported: t_cool, t_ff, the ratio, t_cool vs the Hubble time (13.8 Gyr), the radiated power needed to keep the gas
 hot (E_th / t_cool) and the fraction of it emitted below 0.5 keV; M* variants; a more concentrated β-model
 (r_c 10 kpc, central t_cool).
Controls: C1 Λ(T, Z = 0) at 1 keV within 30% of analytic bremsstrahlung (Gaunt 1.2); C2 Λ(Z = 1)/Λ(Z = 0) at
 0.12 keV > 3 (metal-line cooling dominates at this temperature).
MUTATE (CFG581_MUTATE=1): gas density × 0.01 (mass × 0.01): t_cool must rise ×100 and the escape must become
 PHYSICALLY ALLOWED.
κ = ½ fitted; footings never pooled; cold energy's mass required; not theory closed.
