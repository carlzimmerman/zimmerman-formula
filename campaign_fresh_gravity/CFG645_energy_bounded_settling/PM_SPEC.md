# CFG645 native PM spec (written, NOT run)

Status: specification only. Nothing here was run. The analytic lane (README) shows every derived capacity is inert (= candidate B) or
zero, so a native run of a DERIVED route would reproduce CFG596's canonical result (EXCLUDED on raw KiDS-1000) by construction. The spec
is kept so that the owner can decide whether the KNOB route (EB-η) is worth a native run as an explicitly enlarged theory.

## Engine

- Base: `cfg596_pm.py` at its committed hash (read-only copy into a new `cfg645_pm.py`; never edit `cfg596_pm.py`, `cfg636_pm.py`, the
  cfg640 waiter or the cfg625 driver). 1024³, L100, same seeds and same S0 as CFG596, so the comparison is same-pipeline.
- Footings run separately (canonical, alt), never pooled. κ = ½ fitted.

## The only change: a per-catchment energy ledger

At every census refresh, for each bound region (B's switch, baryon-read segmentation as MS1 requires):
1. E_req = Σ over cold-energy particles newly assigned to the settled phantom of m_i [Φ(r_ta) − Φ(r_i)] (e_Φ, the upper bracket), using
   the gravitating-field potential the engine already computes. Optional bracket: e_V = G M(<r_i)/r_i.
2. Capacity C = η ρ_DE c² V_ta with ρ_DE c² = a₀²/(κ² G), V_ta the region's turnaround volume.
   - η = 1: EB-R. The analytic lane gives C/E_req ≥ 8.0e3 for every mass (D1), so the ledger never binds. A run is a no-op check of the code
     path only (must reproduce CFG596 bit for bit).
   - η = η_gal (2.7–3.5e-6 by footing, D1/EB-η): the KNOB route. Settle inside-out (CFG598 front) until the cumulative E_req reaches C.
     Cold energy that does not settle stays unsettled in the reservoir shell (R5), collisionless.
3. Ledger is cumulative and never refunded (settled cold energy is never drawn back, R5).

## Diagnostics to write

- per-host settled fraction vs M_ta (compare the analytic boundary table: galaxies 1.000, 1e13 0.26, 1e14 0.05, 1e15 0.015);
- gravitating-field P(k, z)/S0 at k 0.3, 0.5, 1;
- raw KiDS-1000 ξ± Δχ² vs S0 with CFG596's scorer unchanged (T-OWN tooth, NZ1);
- X-COP-like hosts: M(<R200)/M_HSE from the run's own clusters (the analytic boundary leaves clusters ~1.5–5% settled, so expect a large
  shortfall unless the reservoir concentrates).

## Frozen expectations (from the analytic lane, to be contradicted or confirmed)

- η = 1: identical to CFG596.
- η = η_gal: the halo model (context only) flips the k = 1 excess (+0.72 / +0.89) into a deficit (R(k=1) 0.22 / 0.27, σ8 ratio 0.939 /
  0.945). Clusters keep only ~1.5% of B's settled amount, which should break X-COP and the Bullet unless the unsettled reservoir alone
  supplies the core mass. That reservoir shape under partial settling is not on the record (CFG637 derived B's reservoir only at full
  settling, where it is empty; its H-CB reservoir is core-concentrated but leaves R200-scale mass 33-40% short).

## Resources (estimate)

Comparable to CFG596 at 1024³ (CFG634's PM spec quotes about 29 GB). Must run alone, after the queued CFG636/CFG639/CFG640/CFG641 work. Not queued by this lane.
