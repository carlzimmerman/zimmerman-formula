# CFG521 FROZEN CRITERIA: does growth still pass with the census placement when galaxy-mass hosts (f_ret ~ 0.1) are resolved?

Committed alone, before any run.

## Question

CFG518 passed growth with the census (depletion-consistent) placement of cold energy: GROWTH OK on both footings at 256^3 and CONFIRMED at 512^3 (canonical). Its 200 Mpc/h box resolves only hosts with r_ON >= 1.56 Mpc/h (log M_ta >~ 13.2 at z = 0), so the census f_ret there is 0.43-0.90. The galaxy regime (log M_ta ~ 11.5-12.5, f_ret ~ 0.10; KiDS lenses, the MW), where the census edge sits 2.9x farther out, was not tested. This lane runs the CFG518 rule, unchanged, in a smaller box that resolves galaxy-mass hosts.

## Engine (cfg521_pm.py = cfg518_pm.py copied; the physics is unchanged)

Changes, listed in full:

1. **Box size from the environment:** L = CFG521_L (default 200). Everything that depends on L (mesh, k grid, IC amplitudes through P_lin, the in_cover radius grid geomspace(dx, 8, 14)) follows automatically, as in the original code.
2. **Resolution threshold:** "resolved" = r_ON >= 2 cells of the 256^3 mesh, CFG413's frozen definition (1.56 Mpc/h at L = 200). It is set by CFG521_RMIN = 2 L / 256: 0.3906 Mpc/h at L = 50, 0.1953 at L = 25, 0.78125 at L = 100. At L = 50 the smallest resolved r_ON grid point is 0.460 Mpc/h, log M_ta = 11.62 at z = 0 (about 650 particles).
3. **Diagnostics only (no effect on the dynamics):** sigma(R) at R = 2 and 4 Mpc/h from the same box modes as sigma8; the catchment mass fraction painted with f_ret <= 0.20; the phantom-excess-weighted mean f_ret; the count of resolved hosts per r_ON grid value.
4. **Bookkeeping:** environment names CFG521_*, outputs to ../_external_data/cfg521_work/, file tags carry _L<L> when L != 200.

Unchanged from CFG518: CFG416 fret_of (0.10 below 10^12.5, ramp to 0.55 at 10^13.5, +0.30/dex capped at 0.90), painted over each host's turnaround ball (largest wins); phantom sourced by the retained baryons f_ret(x)(1 + delta); census edge r_M(M_b,now)/ln(1 + f_ret f_b/(1 - f_b)) capped at r_ON; e = f_sw max(s_ph - s_c, 0) inside the edge balls and catchments; per-catchment compensation comp = s_c (Sum_C e / Sum_C s_c); cap q > 1 -> e/q; MIX-A filter; T1 switch eps = 0.077; nu_mono; FLAT a0; kappa = 1/2 FITTED (footings 9.3603e-11 canonical / 1.1312e-10 alt, never pooled); Lambda-CDM background; EH ICs at z_i = 49 (the only Lambda-CDM input); step grid; seed 359, NSEED 256; 256^3 particles and mesh.

## Box choice and the box-mode limitation (declared)

- **Primary box: L = 50 Mpc/h, 256^3** (cell 0.195 Mpc/h, particle mass 6.5e8 Msun/h).
- **Fallback box: L = 25 Mpc/h, 256^3.** It is used as the primary only if the L = 50 census canonical run does NOT reach the galaxy regime (f_ret achievement test below). In that case the full run set is repeated at L = 25 and the L = 50 results are reported, not scored.
- **Secondary box (reported, not gating; only if time allows): L = 100 Mpc/h, 256^3,** S0 + census canonical.
- A small box has no modes with k < k_f = 2 pi/L (0.126 h/Mpc at L = 50). The Fourier mean is zero, so the box as a whole cannot collapse or expand, and the most massive hosts (groups and clusters) are missing or too small. This is the intended effect here (the box is dominated by galaxy-mass hosts), but the z = 0 box is not a fair cosmological volume and its absolute sigma8 is below 0.811. Every growth statistic is therefore a ratio against **a matched S0 (Newtonian) control at the same box, seed, NSEED, particle number and mesh**, run in this lane with the same engine (switch S0). The ratio isolates the effect of the phantom source; it does not test the missing large modes.
- **sigma definition:** sigma(R) = sqrt(Sum_box-modes P W_TH(kR)^2 / L^3), the CFG518 estimator. In a 50 Mpc/h box, sigma8 is a box-mode sigma8 (all modes k >= k_f). It is gated together with sigma(4 Mpc/h), which is well sampled (L/R = 12.5). sigma(2 Mpc/h) is reported.

## Reliable k range (declared)

All P(k) bins from k_f up to k_max = k_Nyq/4 = pi 256/(4 L): **k <= 4.02 h/Mpc at L = 50**, k <= 8.04 at L = 25, k <= 2.01 at L = 100. (CFG518's k <= 1 at L = 200 is the same k_Nyq/4.) The k <= 1 subset is reported as well.

## Runs (256^3, seed 359, NSEED 256, nice 10, at most 6 threads each, at most 2 at once, detached with nohup; logs in ../_external_data/cfg521_work/)

Primary box:
- **S0:** Newtonian control (the reference).
- **DC-can:** census, canonical.
- **DC-alt:** census, alt.
- **MUTATE:** census, canonical, compensation off (CFG518's NOCOMP). It must NOT be GROWTH OK.
- **K1:** f_ret = 1 everywhere, canonical, same box (the f_ret = 1 control at galaxy resolution). Reported with its own verdict; it does not gate.

Engine integrity:
- **K0:** cfg521_pm.py with L = 200, RMIN = 1.56 (defaults), census canonical at 128^3 must reproduce cfg518_pm.py run at the same settings (a copy with only its output directory changed) to |d sigma8| <= 1e-6 and max|d P/P| <= 1e-5 at every snapshot. If K0 fails, the lane is INVALID.
- Reported only: cfg521 S0 at L = 200, 128^3 vs CFG359's cfg359_S0_FLAT_canonical_N128.json.

512^3: not planned in this session (each 512^3 run took ~9 h in CFG518, and a matched 512^3 S0 at the small box would also be needed). It stays PENDING.

## Growth cuts (CFG361 cuts applied to this box)

Against the matched S0 at z = 0, over all bins k <= k_Nyq/4:
- **GROWTH OK** if |sigma8 ratio - 1| <= 0.05 AND |sigma(4) ratio - 1| <= 0.05 AND max|P/P_S0 - 1| <= 0.10;
- **FAIL** if |sigma8 ratio - 1| > 0.2 or |sigma(4) ratio - 1| > 0.2;
- **TENSION** otherwise.

## f_ret achievement test (the galaxy regime must actually be reached)

On the DC-can run at z = 0: the catchment mass-weighted mean f_ret (fret_mass_mean_catch, the CFG518 diagnostic) must be <= 0.20. If it is > 0.20, the galaxy regime is **NOT ACHIEVED** in that box: no galaxy-regime growth verdict is issued from it (its growth numbers are reported), and the fallback box is run. If the fallback also exceeds 0.20, the lane verdict is NOT ACHIEVED.
Reported with it: the same quantity at z = 1 and 0.5, the catchment-mass fraction with f_ret <= 0.20, the e-weighted mean f_ret, and the resolved host counts per r_ON.

## Decision (scored box)

- **INVALID:** K0 fails.
- **NOT ACHIEVED:** the f_ret achievement test fails in the scored box.
- **INCONCLUSIVE:** MUTATE is GROWTH OK.
- **PASS:** DC-can and DC-alt both GROWTH OK.
- **PARTIAL:** exactly one footing GROWTH OK.
- **FAIL:** neither footing GROWTH OK.

A MUTATE analysis (CFG521_MUTATE=1) re-applies the decision with the MUTATE run in the DC-can slot; it must not give PASS.

## Reported (not gating)

q_max (all snapshots), overdraw mass fraction, whether the cap acted; total excess Sum e census / K1 at z = 1, 0.5, 0; P/P_S0 at k = 0.3 / 1 / 3; max|P - 1| for k <= 1; sigma(2) ratio; comparison with CFG518 (200 Mpc/h).

## Caveats (declared before running)

- One seed, 256^3. Small-box results depend on the box-mode cut; only the ratio to the matched S0 is scored.
- The PM is a mesh code: forces are softened below about one cell (0.195 Mpc/h at L = 50), so the inner structure of galaxy hosts is not resolved; the hosts' turnaround balls (r_ON >= 0.46 Mpc/h) are resolved by >= 2 cells.
- fret_of is CFG416's declared step-and-ramp; below 10^12.5 it is the constant 0.10, so the run tests that one value, not the 0.07-0.18 bracket.
- The expelled baryons stay as gravitating mass where they are (CFG518's declared bookkeeping); the cold energy is bookkeeping, not moved particle by particle.
- kappa is fitted; f_b and rho_Lambda are not derived; the cold energy MASS is still required. A pass is not "theory closed".
