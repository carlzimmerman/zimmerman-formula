# CFG25 — the ΛCDM control for FG016's infall

Script: `CFG25_fg016_lcdm_control.py`, about 10 min on 6 processes.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. The halo scale is capped at log M_ta ≤ 11, and H1 fails (rc = 1).
- The main run exits 1, because H1 failed.

## Question

"Where does the cold fluid go?" has one computed answer in the record: **FG016** (`CFG7_edge_fg016.py`).
- **The picture:** outside a bound system the cold fluid falls in like CDM. At the edge it becomes the phantom (T5).
- **The edge:** FG016 put it at the splashback caustic of spherical collisionless infall, with the accretion rate set by the law's own demand.
- **The KiDS test:** FG016 scored KiDS with the law inside the edge and the collapse's own infall outside, with no free amplitude. It cost Δχ² +50 to +95 against the untruncated law, and was killed.

CFG23 then showed that this KiDS machinery shortchanges standard halos at R ≥ 0.6 Mpc. So the fair test of FG016's kill uses the same engine and the same runs, but scores them as a standard halo:
- the collapse's own collisionless interior *and* its infall;
- the mass scale free in each KiDS bin, as CFG23 gave NFW.

## Results

**Controls pass exactly.**
- FG016's six reading-N collapse runs are re-run and reproduce its committed table (s, x_sp87, Δ_sp87) to 0.
- They also reproduce FG016's committed KiDS numbers for its framework profile to 0.
- CFG23's fitter reproduces BASE and CFG21's framework best.

**KiDS χ², by accretion rate:**

| s | standard halo, A = 0 | standard halo, A ≤ b_Tinker | FG016's framework profile, A = 0 |
|---|---|---|---|
| 2.21 | **173.0** | 156.0 | 223.6 |
| 1.60 | 177.9 | 156.6 | 224.6 |
| 1.20 | 181.9 | **149.5** | 206.3 |
| 1.00 | 289.6 | 228.9 | 190.9 |
| 0.80 | 324.1 | 256.5 | 191.7 |
| 0.60 | 508.4 | 405.7 | 180.6 |

For reference, good fits reach 99–105 (CFG21's framework best; CFG23's c × 0.7 NFW).

- The standard-halo fits land on the halo masses CFG23's NFW fits found: log M200m 11.96 / 12.41 / 12.56 / 12.71 at s = 2.21, against 11.90–12.60. The profile construction is sane.
- The misfit sits at R ≥ 0.6 Mpc: 98 of the 173 comes from there. That is the same transition region CFG23 found for vanilla NFW.
- **H1 FAILED:** a standard halo from this engine does not come within +9 of 104.7 at any accretion rate on FG016's grid.

**Caveat.** The standard halo's χ² keeps falling as the accretion rate rises. Its best point sits at the grid's highest rate (s = 2.2), and higher rates were not run.

## Standing

**The KiDS side of FG016's kill is not framework-specific** (the pre-declared reading). The spherical-infall engine misses KiDS's outer signal for standard halos too: 149–173 at best, against 99–105 for good fits.

What survives from FG016 is its derived edge, 0.18–0.27 r_ta, which sits below CFG4's window [0.31, 0.48]. But the window's lower end was set by the same KiDS machinery (the floor with the linear 2-halo). So that comparison inherits the same caveat.

**Where this leaves "follow the fluid":** the inflow-derived edge is not killed by KiDS in this machinery. Neither model gets KiDS's outer profile from spherical infall around an isolated power-law seed. The untested ingredient is a realistic environment for the infall: the peak's own correlated surroundings instead of a power-law profile, and accretion rates above 2.2. That is what the next lane runs, for both models.

Nothing here says the theory is closed.
