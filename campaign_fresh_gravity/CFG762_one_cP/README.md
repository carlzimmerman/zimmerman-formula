# CFG762: no single c_P lets P radiation export infall energy across SPARC — CLOSED by ×171–182

**Label: D1 CLOSED (both footings). MUTATE bites (exit 1: with no vacuum curvature D1 opens).** The outcome was expected from
CFG760/761 scaling, and the criteria said so in advance.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (ba35a0aae), 2026-10-13. Block CFG760–769.
- **Script:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg762.py` (seconds) → `cfg762.out`, `cfg762_results.json` (per-galaxy rows).
  Raw SPARC via CFG4_common through CFG760's `CFG691_copy.py` (K5-checked there).
- **Settings:** κ = ½ FITTED; L* = 5.754 pc; favourable inputs: V = 2V_obs at the last point, x_e = 0.71 (CFG761's smallest),
  one-crossing c_P,min = R/13.8 Gyr. The cold energy's mass is required; not "theory closed".

| footing | galaxies (y ≤ 1) | max c_P,min | min c_P,max | gap | galaxies with their own window |
|---|---|---|---|---|---|
| canonical (Υ 0.46) | 173 (2 excluded) | 7.67 km/s | 42 m/s | ×182 | 12 |
| alt (Υ 0.42) | 175 | 7.67 km/s | 45 m/s | ×171 | 16 |

## Reading
c_P is one constant. The largest SPARC discs need c_P ≥ 7.7 km/s just for P to cross their outer radius in a Hubble time, while
the export condition caps c_P at ≤ 42–45 m/s for some galaxy. A dozen small galaxies each have a window of their own, but no window
is shared. **With CFG760 and CFG761, P-wave radiation is closed as the export channel for cold-energy infall at L* = 5.75 pc on raw
SPARC** (the larger-L* hatch was closed by CFG760 G3).
