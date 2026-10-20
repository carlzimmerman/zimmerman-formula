# CFG872 — what sets the ~6e6 M_⊙ cold clump? (scaling of the self-consistent clump mass with stellar mass)

Criteria: `FROZEN_CRITERIA.md` (4851408cd, before the script). Run: `python3 cfg872.py` (MUTATE `CFG872_MUTATE=1`). Seconds.

## Result — CLASS (canonical): **FLOOR-LIKE** (alt: UNDECIDED) — and a strike against per-dwarf self-consistency
- Per dwarf, solving σ_obs² = σ_law² + f(r_1/2; r_c)·2σ_x²/3 with the law-linked core r_c = (9/2) σ_x²/a0 (CFG871's H-LINK):
  log M_cl = 5.17 + 0.241 (±0.163) log M★ (canonical; 1.5σ from 0, 4.6σ from 1); alt 0.253 ± 0.253 (1.0σ from 0, 2.9σ from 1).
  Median σ_x 7.2 km/s, r_c 80 pc, M_cl 4.3e6 M_⊙ (canonical). Residual scatter 0.52 dex (a factor ~3 per dwarf).
- **The clump mass barely tracks the stars:** a universal velocity floor (s = 0) is favoured over clumps fed by the catchment supply (s = 1,
  excluded at 4.6σ canonical, 2.9σ alt).
- **Strike against H-LINK (disclosed prominently):** 6 of 25 dwarfs have NO self-consistent solution on the canonical footing — Draco,
  CVn II, And V, And VI, And XI, NGC 205 (4 on alt). Under H-LINK a heavier clump has a larger core, which moves its mass outside r_1/2, so the
  excess it can produce has a ceiling; the largest-excess dwarfs exceed it. CFG871's pooled consistency does not survive dwarf by dwarf at the
  top end. (Draco is the clearest case.)
- K1: median σ_x 7.2 km/s, within 20% of the pooled 7.9. MUTATE (σ_obs = 1.5 σ_law for all) gives s = 1.05: the fit responds to the data.
- **Reading on the 6e6 M_⊙ question:** not derived. The data prefer a floor-like origin (a common cold-energy velocity scale ~7 km/s) over
  supply-fed clumps, but the law-linked self-gravitating clump cannot reach the largest excesses. Either the clump's own gravity is not
  law-boosted in the way H-LINK assumes, or the extra component is not a single isothermal clump.

κ = ½ fitted; cold energy mass required; not theory closed.
