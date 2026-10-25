# X31 AMENDMENT A1 (PRE-RESULT: committed before any script has run; implementation details the criteria left open)

No threshold, label, class, proxy, constant, verdict line or check changes. This amendment only fixes how §2 is read for each
row. The values below are inputs, and no F has been computed.

- **MW stellar mass.** The criteria do not say how to split the MW's M_b = 6.646e10 M☉ (P4 B1). M★ = M_b − M_gas, where
  M_gas is the McMillan17 HI + H₂ discs as P4 encodes them (Σ_HI = 10 M☉ pc⁻² and Σ_H₂ = 2 M☉ pc⁻² at R = 8.33 kpc, with
  the P4 radial shapes), integrated over R = 0–100 kpc. M_den = M_b. G = 0.
- **SPARC and UMa.** M★ = U₀ L[3.6] (CFG695 U₀ per footing). M_den = 1.33 M_HI + M★ (X19's M_b). G = 0.
- **TDGs.** M★ = `M_star_1e8` from Lelli+15. M_den = `M_bar_1e8` (X19's M_b). G = 0.
- **X1 / S1 dwarfs and DF2/DF4.** M★ is the record's stellar mass (X19's M_b). M_den follows C1, C0 or C2.
- **Clusters.** Members without KT (KT ≤ 0) get no F, exactly as X19 treats σ. The class interval is over members with KT.
- **P1 (per-system dwarfs).** Every X20 row (both footings) that joins X1 by (footing, name) is used. That includes the
  rows outside X19's classes (M31 dEs, Sagittarius, Canes Venatici I), which get G = 1 (PROVISIONAL). The per-system
  labels are X20's `lab_B_iso` and `lab_B_EFE`.
- **Spearman ordering statistic.** E is the class's B_iso E on that footing (B_EFE for the B_EFE qualifier). The cosmic
  background is excluded because its F is not placeable.

κ = ½ FITTED. Footings never pooled. Not "theory closed".
