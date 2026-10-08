# CFG429: a settling rate keyed to the local dynamical time, with ZERO constants. EXCLUDED on T15's ledger (door 4, 10-07 list)

The script is `cfg429_tdyn.py`. MUTATE (λ = T15's cluster ceiling 0.0073) brings clusters_b0 to M_cold = 0, as required.

**Correction to the door as posed.** The record's settling law (CFG382, used by T15/T16) is already Γ = λ/t_dyn, with f = 1 − exp(−λ√(4πGρ)τ). "Zero constants" therefore means λ = 1.

**Result.**
- At λ = 1, settling completes everywhere (f = 1.000).
- The full kernel supply S/M_b = 2.9 (MW-30), 6.2 (groups) and 5.0 (clusters) then exceeds every measured deficit.
- M_cold/M_b comes out between −1.1 and −5.4 in all five rows.
- The budget needs λ ≤ 0.007–0.03 (T15/T16). So a constant-free t_dyn rate is excluded, and λ remains a fitted number on this ledger.

**Caveat.** The verdict is conditional on T15's ledger definitions (definition-A deficits, a₀ = 1.2e-10, CFG382's τ). Its supply numbers check out against the T9 closed form.

## FORWARD NOTE (2026-10-08): do NOT cite this as a kill until it is re-run on the corrected ledger
This lane was committed about 1.5 h before CFG453, which showed that T15's group and cluster rows mix two deficit definitions. Those rows used definition A, x_A = (M_tot − M_b − M_ph)/(5.364 M_b), in place of T15's own x = (M_tot − M_b)/M_b. The group and cluster rows above inherit that units mismatch.
- On T15's own definition, CFG453 finds positive cold mass in groups and clusters.
- Only the Milky Way 30-kpc row still excludes λ = 1, and its sign depends on the MW circular speed (CFG451).
- Status: **SUPERSEDED / PENDING a committed re-run on the corrected ledger** (flagged by LEDGER_failure_mechanisms_2026-10-08). The verdict above is kept as history and not re-adjudicated here.
