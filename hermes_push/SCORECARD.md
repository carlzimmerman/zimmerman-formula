# SCORECARD — the shape we want (update "best so far" every iteration; green only with a script + certificate; thresholds on BOTH footings).

| gate | requirement | threshold (both footings) | best so far (candidate, value, H-entry) | status |
|---|---|---|---|---|
| G5 forest | dark-matter power at k = 5 h/Mpc, z=2-3 | within 10% of LCDM | C001 killed at G5 (M8-invert/x-gate): forest x=g_N/a0~1e-21 (inert, "consistent-by-construction", not a win); T=nu/sqrt x~x^{-1/2} non-universal (H001) | red |
| G6 growth | S8; fsigma8 vs DESI DR1 | S8 in 0.77-0.85; chi^2/bin < 1.5 | Hubble kernel alone (L180/L181): S8 0.843-0.847, chi^2/bin 0.65-0.73 | green (no component depletion yet) |
| G3 clusters | retained fraction inside R500 | 0.576 +/- 0.10 | C001: inert in clusters, f=1.00 vs 0.576 (H001); still no survivor | red |
| G7 KiDS | CDM-like halo mass around galaxies, 0.1-1 Mpc | <= 14% of LCDM | none | red |
| G8 Omega_m | late-time matter budget | within 3% of 0.31 | none | red |
| G1 spirals | retained fraction inside 3 R_d at 1.2e10 Msun baryons | <= 0.105 strict (0.58 with kick-redistributed profile) | none | red |
| G2 Milky Way | retained fraction inside 30 kpc | 0.14 +/- 0.05 | none | red |
| G4 CMB | third peak; low l | peak3/peak2 within 5% of 0.992; D_l(30) excess < 20% | none (any clustering cold component at f >= 0.988 passes; L129/L165) | red |
| G10 stability | ghost, gradient, kinetic | c_s^2 >= 0 on the full branch; kinetic matrix positive | lead candidate: fails for z <~ 2.4 (L185/L186; astra branches) | red |
| G9 PPN | Cassini, preferred frame | gamma-1 < 2.3e-5, alpha1 < 1e-4, alpha2 < 4e-7 | double-filter static kernel + stiff clock (L169/L171) | amber (static only) |
| G11 N_eff | BBN | Delta N_eff < 0.3 | none needed unless the mechanism radiates | amber |
| G12 local kernel | wide-binary arms, dSph EFE | unchanged | preregistered (Amendment 11) | green (must stay so) |
| G13 predictions | flat a_0(z); Hubble-kernel growth eq | preserved or derived | on record (PAPER7, PAPER15); flat a_0(z) Lean-stated (HermesLean PART B) | green (must stay so) |
| D0 derived | every ingredient from an action; parameters counted | no free function of host mass | none | red |

## Ledger after iteration 1 (H001, C001)
- C001 (M8-invert + M1, x = g_N/a_0 gate) killed at G5: x~1e-21 on Mpc modes (both footings, inert),
  T = nu/sqrt x ~ x^{-1/2} non-universal, active window at r~1-50 kpc (disc), clusters inert
  (f=1.00 vs 0.576), M8 c*~0.4 = closed C000c swing.   0 doors passed.  Regime-split logic
  CERTIFIED in Lean (`HermesLean.lean` PART A, compiled exit 0, 0 sorry, 0 axioms).
- NEXT registered candidate: C002 = halo-gated LATE energy injection (M2 timing = halo formation / a
  threshold a*; M3 bookkeeping = mass redistributed but CONSERVED) — Part 5's second untested first
  look: "dynamics that make halos unrelaxed without cutting linear power, e.g. late halo-gated energy
  injection with mass conserved".  Kill: G5 first (must not cut k=5,z=2.2 forest power), then G3
  (cluster f~0.576, mass conserved => f at R500 must still reach 0.576 without a mass loss), then G8
  (Omega_m budget within 3%).
- Rows G5/G3/G1/G2/D0 remain RED. No green except the Hubble kernel (G6), preregistered G12, and flat
  a_0 / Hubble growth (G13). No complete theory; no "doors closed" beyond the named gates.
