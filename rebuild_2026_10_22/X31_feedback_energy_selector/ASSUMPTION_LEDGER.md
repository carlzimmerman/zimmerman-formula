# X31 assumption ledger (committed with FROZEN_CRITERIA.md, before any script or number of this lane)

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed".

## Inputs and their class

| input | class | used for |
|---|---|---|
| X19 class table, labels, intervals, per-system rows (exec'd from X19's committed source and inputs) | FRAMEWORK-NATIVE (record result) + RAW catalogues X19 reads | labels, σ, M_b |
| X20 `x20_per_system.csv` (E, labels per dwarf) | FRAMEWORK-NATIVE | P1 |
| X1 `x1_per_system.csv` (log M★, σ per dwarf) | RAW → record | P1, dwarf F |
| X24 results JSON (matched-mass medians, Spearman) | FRAMEWORK-NATIVE | context row |
| SPARC Lelli 2016c table (M_HI, L[3.6]); CFG695 U₀ | RAW; FRAMEWORK-NATIVE | g_ref, SPARC F |
| Lelli+15 TDG table (M_star, M_bar, V_circ) | RAW | TDG F |
| CFG657 DF2/DF4 inputs (M★, σ) | RAW (record transcription) | DF2/DF4 F |
| Tian+26 groups (logMbar, logSigma) | RAW | groups F band |
| eRASS1 primary v3.2 (KT, MGAS500, M500, R500) | SURVEY-CALIBRATION (M500 from scaling relations) | cluster F |
| X21 / X7 / X2 committed machinery and arrays | FRAMEWORK-NATIVE | P2 |

## Adopted constants (standard; none fitted; none scanned)

| constant | value | status |
|---|---|---|
| E_SN | 10⁵¹ erg | standard; PROVISIONAL (from memory) |
| IMF | Kroupa 2001, slopes 1.3 (0.1–0.5 M☉) / 2.3 (0.5–100 M☉) | PROVISIONAL (from memory) |
| SN progenitor range | 8–100 M☉ | PROVISIONAL (from memory) |
| η_SN | computed in-script from the IMF above (closed form) | derived |
| return fraction R | 0.4 | PROVISIONAL (from memory) |
| ε_SN | 1 (primary; total injected); 0.1 reported | convention / PROVISIONAL |
| T_re (reionization photo-heating) | 2×10⁴ K | PROVISIONAL (from memory) |
| μ | 0.6 | transcribed in the record (X19) |
| f★ (clusters) | 0.20 of the gas | transcribed in the record (F1, X19) |
| f★,cos (C2) | 0.07 | PROVISIONAL (from memory) |
| groups M★/M_bar | band [0.1, 1] | PROVISIONAL (composition not on disk) |
| gas-expelled flag G | per morphology (FROZEN_CRITERIA §2d) | PROVISIONAL (from memory) |

## Assumptions (named, so a reader can attack them)

- **B1. Injected energy is not retained energy.** For galaxies, e_SN counts what was injected, not what stayed. Most of
  it is radiated or carried out. ε_SN = 1 is an upper bound. ε_SN rescales every galaxy-scale F by one factor, so it
  matters only for cluster-vs-galaxy comparisons. ε_SN = 0.1 is reported.
- **B2. Cluster energies are present-day thermal energies**, not cumulative AGN output. The gravitational and the
  non-gravitational parts cannot be separated without entropy profiles, which are not on disk. F_exc is the crude
  proxy. M500 comes from eRASS1's scaling relations, so F_cl and F_exc are not fully independent of the X-ray data.
- **B3. One R for all ages.** TDGs and gas-rich dIrrs have younger stars, so R = 0.4 overstates their formed mass by up
  to 1/(1 − 0.4). That shifts their F up by up to 0.22 dex.
- **B4. One g_ref for all dwarfs (C1).** The expelled gas is set by a gas-rich dwarf's present gas-to-star ratio. C0 and
  C2 bracket that choice.
- **B5. Binding at the measurement radius.** σ_b is X19's velocity at the radius where E is measured, not a global
  binding energy. This keeps F local, as X19's V were.
- **B6. Reionization** adds the same per-baryon energy everywhere. It matters only where e_SN is small.

## Disclosures (not blind)

- X19's class medians of σ and M_b were known while these criteria were written, and so were its result that σ fails
  (offenders T1, ultra-faints, bright M31, M31 others).
- For systems whose inventory is stars only, C1 gives F ∝ 1/σ² up to the common factor (1 + g_ref) and e_re. Inside the
  dwarfs, F is therefore close to a monotone transform of σ. **The expectation, stated before any number, is that F
  inherits σ's galaxy-scale offenders** (Crater II, at σ 2.3 km/s, should have the largest dwarf F while it is NONE). The
  lane tests this rather than assuming it.
- Clusters enter through a different energy (kT) and a different binding (M500), so their place relative to the
  galaxies is not known in advance.
- No F value, ordering or threshold of this lane has been computed. No new data are downloaded.
