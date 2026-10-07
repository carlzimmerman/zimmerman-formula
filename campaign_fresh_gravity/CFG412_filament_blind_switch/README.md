# CFG412: a filament-blind switch? No reader screened is PROMISING. Most of the "filament" ON mass is inside host turnaround spheres

Criteria: `FROZEN_CRITERIA.md`, committed alone first (ed842ae0e). Script: `cfg412_screen.py` (rc 1: the K3 check failed and is kept).
MUTATE: `cfg412_screen_MUTATE.out` (rc 1, detected). Reported-only diagnostics: `cfg412_diag.py` / `.out`, written after the frozen run.
Light CPU: one process, one FFT thread, nice 15. The input is CFG410's BASE z0 snapshots, re-deposited at 256³. No PM run was made.

## Verdict
**Lane: no candidate is PROMISING. Every scored candidate is PARTIAL, and each passes only one of the two numerical criteria.**

The most useful finding is a ceiling, not a candidate:
- 81% of T1's ON mass in l3 < 0 cells lies inside the turnaround sphere of a resolved host (a peak whose ON ball reaches ≥ 1.56 Mpc/h). The canonical and alt values are 0.805 and 0.811.
- 75% of it sits in cells whose own density already passes the spherical test (1 + δ ≥ Δ_ta).
- 31% sits at 1 + δ ≥ 50, which is halo interiors, not filament cores.
- At the 0.78 Mpc/h mesh, l3 < 0 marks mostly the radially stretched outskirts and interiors of hosts. The analytic sphere has l_r < 0 wherever the density slope γ > 1.
- So any reader that stays ON out to r_ta around every host can remove only about **13–19%** of CFG410's "filament" ON mass.
- On this snapshot, then, the requirement (OFF in filament cores, ON to r_ta) cannot remove most of the excess. The growth excess and the KiDS edge conflict directly. CFG410's FILAMENT-DOMINATED label (from l3 < 0) overstates how much of the excess lives in true filaments.

| candidate | R_fil (can / alt) | Xhat excess share (estimate) | sphere edge / r_ta | legality, constants | verdict |
|---|---|---|---|---|---|
| A1: T1 AND all V-web axes converging | 0.999 / 0.999 | 0.89 / 0.86 | **≤ 0.376** (nonlinear infall) | legal (= T1 × l3-sign step in linear theory), 1 | PARTIAL (fails KiDS) |
| A2: V-web middle eigenvalue | 0.000 / 0.000 | 0 | 1.000 | legal, 1 (identical to T1) | PARTIAL (no removal) |
| B1: turnaround cover around density peaks | 0.007 / 0.009 | −0.26 / −0.23 | 1.000 | CONDITIONAL, 1 | PARTIAL |
| B1T: T1 AND B1 | 0.126 / 0.121 | 0.094 / 0.088 | 1.000 | CONDITIONAL, 1 | PARTIAL (best KiDS-safe) |
| B1xT (exclusive peaks, reported only) | 0.153 / 0.148 | 0.12 / 0.12 | 1.000 | CONDITIONAL, 1 | not scored |
| l3 veto (CFG410 reference) | 1.000 / 1.000 | 0.89 / 0.86 | fails KiDS (+52, CFG355) | | reference |

Column definitions:
- R_fil = 1 − M_fil(candidate)/M_fil(T1), with CFG410's (1 + δ) weighting.
- Xhat = X_CFG410 × (the fraction of the l3 < 0 RES excess source removed). It is a linear-response **estimate**, not a PM result.

Because nothing is PROMISING, no confirming PM run is proposed.

## Families screened
**(a) V-web.**
- Particle velocities are not stored in the snapshots, so the PM leg uses the **linear-theory velocity from the z0 potential (declared)**.
- That velocity shear is the T-web up to a factor f H. After zeroing the Nyquist planes the eigenvalues agree to 3e-7 (diagnostic D1). So linear V-web readers are eigenvalue readers, and CFG354's theorem already excludes them.
- The nonlinear velocity of an analytic secondary-infall host (the record's Λ shell ODE, seed profiles ε = 1 and 2/3) gives this in the whole single-stream infall region (0.38–0.99 r_ta):
  - the radial axis is stretching in 100% of shells, for both proper and peculiar velocity;
  - (dv/dr − H)/H runs from 0.8 to 4.0;
  - both tangential axes are converging.
- So a host's infall region carries the same stretched-axis signature as a filament, in velocity as well as in tide. A1 can therefore be ON only inside the outer caustic (≤ 0.376 r_ta), and fails KiDS for the same reason as CFG351/352/355.

**(b) Non-local.**
- **B1, turnaround cover.** A cell is ON if it lies inside some density peak's turnaround sphere. The sphere is the ball where the mean density about the peak is ≥ Δ_ta, with the first crossing taken from the peak outward and T1's eps smearing.
  - It reads enclosed mass, a Gauss flux of ∇ψ, so it has no potential zero point (this evades CFG353) and no bulk-gradient dependence (this evades CFG354's T3 obstruction).
  - It adds 0 new constants.
  - On an isolated sphere its edge is exactly r_ta, as T1's is (K4: 20.000 of 20 cells). For cfg100_lib hosts with log M_b 10.5–11.5, both footings and both Δ_ta values, the edge is 1.000 r_ta.
  - It fails on removal: filament-labelled ON mass is covered by peak turnaround spheres (see the ceiling above).
- **B2, khronon lapse or potential smoothed at a host-scale filter.** Assessed analytically, not scored.
  - Raw lapse or Φ_R values carry CFG353's environmental zero point.
  - A difference Φ − Φ_R removes the zero point but adds a filter scale R, a second constant.
  - Smoothing at R dilutes a cylinder as R_f²/R² but a compact host as r³/R³. So any host-scale filter makes filaments relatively *more* prominent, which is the wrong direction.
  - One R also cannot serve hosts whose r_ta runs from 0.3 to 5 Mpc (CFG346's dwarf-starvation precedent).
  - Verdict: NO-GO.

**(c) Other.**
- Local "spherical-consistency" readers that use ∇ψ and ∂³ψ (e.g. 3|∇ψ| ∂_r l_t / (l_r − l_t), which equals Δ̄ − 1 on spheres with 0 constants) read ∇ψ. They inherit T3's obstruction: at r_ta, g_ext/g_host is 0.42–6.8 (CFG354). Screened out on the record, not scored.
- Stream-count readers (CFG351/352/355) and memory readers (CFG349) are closed in the table.

## Checks
- K1: re-computed T1 matches the stored f (agreement 1.00000). PASS.
- K2: the l3 veto's ON-mass drop is 0.640 / 0.639 against CFG410's 64%. PASS.
- **K3: FAIL** (rel 3.6e-3 / 3.1e-3 against the frozen 1e-4). The cause is Nyquist-plane odd derivatives. The reported-only D1 gives 3e-7 with them zeroed. The failure is kept.
- K4: the B1 mesh-sphere edge is 20.000 cells. PASS.
- K5: the infall solver returns Δ_ta = 11.8056. PASS.
- MUTATE: replacing every reader by T1 gives max |R_fil| = 0. Detected.

## Caveats
- One 256³ snapshot per footing at z = 0 only. The mesh is 0.78 Mpc/h, and the CIC density sets which cells pass 1 + δ ≥ Δ_ta.
- Xhat is a linear estimate. The bookkeeping reservoir is unchanged.
- Linear velocities in the PM leg. The nonlinear V-web is tested only on the analytic sphere.
- B1's peaks are mesh-scale local maxima. Sub-peaks inside a host can push the cover past r_ta by up to about r_vir (the exclusive variant is reported only). B1 has no written smooth action: the peak set, the max over peaks and the first-crossing rule are non-smooth, so its legality is CONDITIONAL. It is leaf-instantaneous (criterion B) and leaf-covariant (G9), and it reads total matter (the owner's MS1 relaxation), as T1 does.
- The ceiling uses CFG410's mass weighting. The excess-weighted estimate agrees (B1T Xhat about 0.09).
- κ = ½ is fitted. Both a₀ footings are reported separately, never pooled. The cold mass is still required, and no particle species is added.

## Run
```
nice -n 15 python3 campaign_fresh_gravity/CFG412_filament_blind_switch/cfg412_screen.py                 # rc 1 (K3 kept failed), ~3 min
CFG412_MUTATE=1 nice -n 15 python3 campaign_fresh_gravity/CFG412_filament_blind_switch/cfg412_screen.py # rc 1 (detected)
nice -n 15 python3 campaign_fresh_gravity/CFG412_filament_blind_switch/cfg412_diag.py                   # reported only
```
Input: `../_external_data/cfg410_work/cfg410_RES_Rc3_MIXA_FLAT_{canonical,alt}_N256_z0.npz` (CFG410, read-only).
