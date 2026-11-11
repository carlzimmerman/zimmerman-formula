# SS5 RESULT: NO VERDICT / NO VERDICT (criteria 12c42eef04)

This lane grades variant L, the outside source's baryon-component segregation. The component (5.41 omega_b) feels only g_N;
baryons feel the law nu(g_N / a0) g_N. There is no conversion and no pressure. TEST lane, quarantined; adopts nothing; no
particle adopted. kappa = 1/2 FITTED; not theory closed. Footings are never pooled.

## Label

**The frozen label is NO VERDICT on both footings.** The known answers pass: KA-L1, KA-L2 (multi-shell Newtonian collapse z
0.992 / 0.985) and KA-L3. ML1 does **not bite**: a v_stiff drift planted between the species at z 1.2 leaves an offset of only
0.035 Mpc at z 0 on both footings, against the line of 0.35 Mpc. Under the frozen rule that makes the D2(b) test powerless, so
the label is NO VERDICT.

**Why ML1 does not bite (reported).** The law re-binds the planted drift, so the test itself is not blind:
- the same planted drift with Newtonian baryons leaves 2.105 Mpc at z 0;
- D2(b) can therefore see an offset whenever nothing pulls the baryons back;
- with the law, nu is of order 500-800 in the 1D wells, and the baryons are pulled straight back onto the component's peak.

That re-binding is the mechanism's failure, not the code's. The frozen rule did not foresee it.

**D3 was not run.** The frozen label is not D-SEP. The only offsets are transient and mid-collapse (below).

**Count beside the label:** 0 fitted constants. The source's form choices: the 1/sqrt(3) cap, the u^4 (1 + u^2) capture law,
R_seg = v_stiff / H(z_turn), and z_turn = 1.2.

## Reading (post hoc, reported, no label): no segregation

| test | canonical | alt |
|---|---|---|
| D1 delta_b / delta_chi, k 0.1 / 1 / 3 h/Mpc, z 0 | 6.5 / 11.4 / 17.6 (nu 13-32) | 7.2 / 12.7 / 19.6 |
| D1 r(k, z), all 12 cells | 1.000 | 1.000 |
| D2(a) collapse z, half-mass shell: chi / baryons (2x steps) | 3.85 / 8.74 (3.86 / 8.78) | 4.06 / 9.34 (4.06 / 9.39) |
| D2(a) R_half chi / b at z 1.2 (kpc; 2x steps) | 110 / 47 (214 / 47) | 217 / 48 (192 / 44) |
| D2(b) peak offset, z 3 / 1.2 / 0 (Mpc) | 0.430 / 0.240 / 0.095 | 1.410 / 0.075 / 0.200 |
| D2(b) at 4x steps | 0.475 / 0.395 / 0.075 | 1.465 / 0.100 / 0.185 |
| claimed R_seg | 3.45 Mpc | 3.74 Mpc |
| ML1 planted v_stiff (law baryons), z 0 | 0.035 | 0.035 |
| ML1 with Newtonian baryons (power check), z 0 | 2.105 | 2.105 |
| ML2 Newtonian baryons | 0 / 0 / 0 | 0 / 0 / 0 |

- **D1.** Baryons fall nu times harder into the *same* wells: r = 1 everywhere, and delta_b exceeds delta_chi by 4-20x.
  delta_b,rms is above 1 at k >= 0.3 h/Mpc by z 1.2, so linear theory breaks there. The drift points along the same
  gradient; it is not a displacement.
- **D2(a).** Baryon shells collapse at z of about 9, the component's at z of about 4. Baryons end more concentrated
  (R_half_b < R_half_chi at every z and step count).
  - The z 0 radii (chi 1.4-1.8 Mpc, b 0.16-0.42 Mpc) are **not** step-converged. Pure radial orbits bounce after collapse;
    there is no angular momentum. The direction is robust; the sizes are not.
- **D2(b).** At z 0 the two species' peaks sit 0.08-0.20 Mpc apart: 2-6 % of the 3.45 / 3.74 Mpc claimed. The z 3 offsets (0.43 / 1.41 Mpc) are taken mid-collapse, before the component's peak forms. Baryons
  (nu-boosted) caustic first, so the "peak" of the still-shallow component is a broad maximum.
  - Canonical's z 1.2 offset is not step-converged (0.24 vs 0.395).
  - **The offset line was frozen without a redshift**, and ss5.py applies it at all three. Under that coding the z 3
    transients alone would mark "separation". The z 0 reading is the one the claim (a present-day R_seg) is about.
    Both are reported; neither sets the label, which is NO VERDICT by ML1.

**Answer to the lane's question:** construction L does not segregate. The component-only-feels-g_N split makes baryons
*trace and over-concentrate* on the component's peaks, never leave them. The source's v_stiff drift is re-bound by the
same law that drives it. The source's R_seg = v_stiff / H(1.2) is a kinematic estimate with no restoring force; the dynamics
include one, and it wins by about a factor of 60 (2.1 Mpc unbound vs 0.035 Mpc bound).

## Disclosures (changes after the first runs; none of them moves the label)

1. **D2(a), radiation in the background force.** H included radiation; the first force term did not. Fixed:
   gbg = (a''/a) r.
2. **D2(a), collapse amplitude.** The first run scaled 1.686 D(200)/D(1), which is wrong once radiation is in. Fixed by
   bisecting the mean delta_i so the Newtonian single shell collapses at z 1, as the criteria specify (delta_i = 0.01129 on
   both footings).
3. **D2(a), centre crossings.** Shells passing r = 0 were pushed outward. Fixed: the force is multiplied by sign(r).
4. **D2(a), integrator.** The first integrator was solve_ivp RK45, rtol 1e-6, atol 1e3 m. That run did not finish in 33 h
   of CPU: with stiff centre crossings and a scalar atol of about 1 km, the step collapses. It was stopped (SIGTERM) by the
   coordinating session on the owner's word. It is replaced by a fixed-step kick-drift-kick leapfrog uniform in t: 400,000
   steps (dt 0.034 Myr, about ten steps per crossing of the 1 kpc softening at 3000 km/s), with a 2x-step run reported. The
   integrator is not in the frozen criteria.
5. **D2(a), collapse finder.** It now finds the first fall below 10 % of the running maximum, so a post-bounce re-expansion
   cannot be taken for turnaround. Before this fix, KA-L2 read -1.
6. **The ML1 power check** (planted drift with Newtonian baryons) was added after the freeze. It is reported only.

## Files

- Criteria: `FROZEN_CRITERIA.md` (12c42eef04).
- Scripts: `ss5.py`, `ss5_grade.py`, `run_both.sh`.
- Outputs: `ss5.json` / `ss5.out`, `ss5_MUTATE.json` / `.out`, `parts/ss5_<footing>.json`, `run_canonical.txt`,
  `run_alt.txt`.
- Run: `./run_both.sh && python3 ss5_grade.py` (about 1 min per footing, one thread).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
