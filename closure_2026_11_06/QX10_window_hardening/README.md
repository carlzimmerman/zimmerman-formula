# QX10: hardening QX7 iter_4's CMB/galaxy window. KILLED (all four cells, by iter_2: galaxy lensing)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (cold dark energy, never cold dark matter; no particle;
no LCDM inputs). Criteria c1f0cadb7a (cells C1-C4 chosen by rule before any grade); iter_2 Amendment A1 168db297bd.

| Cell (lambda_0 Mpc, p) | iter_1 primary CMB | iter_2 capture / end state | iter_3 SPARC | Overall |
|---|---|---|---|---|
| C1 (2.61, 4.25) | NO VERDICT (J1) | **FAIL** (G6 -0.24) | PASS | **KILLED** |
| C2 (1.47, 3.5) | NO VERDICT (J1) | **FAIL** (G6 -0.27) | PASS | **KILLED** |
| C3 (8.25, 5.625) | NO VERDICT (J1) | **FAIL** (G6 -0.15) | PASS | **KILLED** |
| C4 (2.15, 3.75) | NO VERDICT (J1) | **FAIL** (G6 -0.25) | PASS | **KILLED** |

**Why the window dies.**
- QX7 iter_4 kept galaxies free of the sector by giving each captured core the self-gravitating size lambda_J/2 >= 0.73
  Mpc, which is larger than a galaxy's turnaround radius. That idealisation ignored the host.
- In the host's own potential, with the a0 law on, the same n = 1 fluid stays bound. It forms a 150-230 kpc halo of
  4.2 M_b around every galaxy. For C3, half the captured mass still sits inside r_ta.
- That halo is invisible to rotation curves: SPARC still passes, at 0.056-0.062 rms. It does not show up inside the
  ellipticals' radii either. But it raises isolated-galaxy lensing by 0.15-0.27 dex against KiDS's 0.05 line.
- A time-dependent heating run from z of about 1 reaches the same end state, so the heating is quasi-static.

**What iter_1 shows.**
- With the switch, the sector is cold through the primary-CMB epoch. As a cold component it fits raw Planck PR3 TT/TE/EE
  on the footing background (chi^2 6718 / 6497, peaks within 1 sigma) at omega_d 0.121, consistent with the window's 0.120.
- That is not independent evidence, because the footing values encode the background. The late-lensing bound J1 is too
  loose to certify the proxy (NO VERDICT).
- The kill does not depend on iter_1.

**Door labels.** CMB-lensing shape and linear growth go back to FAIL for every mechanism tried: QX3 iter1-3, QX7 iter1-3,
and now QX7 iter_4's window under the host's own pull. Clusters stay FAIL. What would be needed is a sector that clusters
on the linear web, does not stay bound in galaxy potentials, and is still captured by clusters. That would be a new
mechanism (for example a switch keyed on the local acceleration). It is not in this action and was not tested here.
