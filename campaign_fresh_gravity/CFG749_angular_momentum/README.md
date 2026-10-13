# CFG749: orbiting cold energy is unbound — the mechanism needs cold energy at rest, not in orbit

**Label (frozen): λ = 0 control PASS; λ = 0.3 and 0.6 OTHER.** These are neither the law nor the predicted rotation deficit: the
cold energy leaves. Total energy, computed after the runs from the same initial state, is **positive** for any orbital motion
at a fraction λ ≥ 0.3 of the law's circular speed. Because its self-gravity is cancelled by the critical tether, the cold
energy is bound **only by the baryons**, whose binding is tiny compared with the law's flat-curve kinetic energy.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first.
- **Script:** `python3 cfg749.py <lambda>` (about 6 min each) → `cfg749_lam<λ>.json`.
- **Settings:** CFG748 dynamics plus the centrifugal term L²/r³; R₀ = 200; t_end = 6000. κ = ½ FITTED; the cold energy's mass
  is required; no particle species; not "theory closed".

| λ (orbital speed / v_c,law) | m/r at r = 2 / 5 / 10 / 20 (t 5000–6000) | initial energy: baryon binding / orbital KE / push / total | ΔE/E | verdict |
|---|---|---|---|---|
| 0 (control) | 1.002 / 0.994 / 0.999 / 0.991 | −1.50 / 0 / 0.28 / **−1.22** | 3.1e-3 | K1 PASS (CFG748: 0.999 / 1.001 / 0.998 / 0.996) |
| 0.3 | 0.25 / 0.10 / 0.055 / 0.029 (core only) | −1.50 / 9.04 / 0.28 / **+7.83** | 1.1e-11 | OTHER |
| 0.6 | 0.25 / 0.10 / 0.05 / 0.025 (core only) | −1.50 / 36.2 / 0.28 / **+35.0** | 5.3e-11 | OTHER |

(m/r = 0.5/r is the fixed inner core alone: no shells remain inside 20 r_M.) K2 PASS in all three runs (≤ 1e-2).

## Reading
1. **The decisive point.** With the critical tether, cold energy does not feel its own gravity. At r ≫ r_M, the law's flat
   circular speed comes from the cold energy's field, but the cold energy itself is held only by the baryons, whose escape
   speed² is 2GM_b/r ≪ V_flat². Cold energy moving at even 30% of the flat-curve speed is **unbound**.
2. **What the mechanism therefore requires.** The cold energy must be nearly **at rest** in each system's frame, with
   v² ≲ 2GM_b/r. That is an anchored medium, not orbiting collisionless matter. It fits the tether picture (cold energy tied to
   the cosmic/vacuum frame) and conflicts with ordinary infall, which arrives at ~V_flat. CFG747/748 worked because their shells
   started at rest.
3. **Consequences.**
   - The collisionless relaxation channel (CFG747/748) is real but applies only to dynamically cold, non-orbiting cold energy.
   - Cold energy that falls in with infall speeds must lose almost all of that kinetic energy to stay. That reopens the
     dissipation question (CFG744: radiation too slow at galaxy scales).
   - An anchored medium also cannot be the collisionless component that follows the galaxies in the Bullet. That tension with
     the two-sector picture is still open.
4. **Limits.** One initial family (uniform sphere at rest radially, tangential speed λ v_c); radial-shell treatment of rotation;
   point baryonic mass; cubic W. The binding argument itself is analytic and does not depend on these.
