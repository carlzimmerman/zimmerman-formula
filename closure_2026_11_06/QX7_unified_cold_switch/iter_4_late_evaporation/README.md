# QX7 iter_4: captured early, puffed up late. CMB lensing and galaxies: WINDOW (scoped). Clusters: FAIL

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria 22af3e7b43. Script: qx7_iter4.py (one thread, about 40 min).
Outputs: qx7_iter4.json/.out, qx7_iter4_MUTATE.json/.out, run_main.txt / run_mutate.txt.

## Mechanism

iter_3's leaf-uniform switch, lambda_J = lambda_* Omega_DE(a)^p. The dust may fall into galaxies early. Today each bound system
holds f_cap R M_b = 4.2 M_b as an n = 1 hydrostatic core of radius R_c = lambda_J(0)/2. A system holds none if R_c is at least its
turnaround radius.

## Result

- **Galaxy gates** (G5 SPARC inner mass, G6 KiDS lensing shift <= 0.05, G7 Humphrey ellipticals shift <= 0.15, both footings):
  pass for lambda_0 >= 1.47 Mpc (23 of 61 values). The dust core is then at least 0.73 Mpc across. Ordinary galaxies keep no
  dust, and massive ellipticals hold it spread far outside their 40 kpc.
- With the forest gate: 857 cells. **G2' (CMB-lensing growth): 270 cells pass** (closest Delta chi^2 0.04). Window:
  lambda_0 1.47-8.25 Mpc, p 1.125-6.
- **This is the first sector in the record that builds the CMB-lensing shape (raw PR4, per bin, amplitude refit) and leaves the
  a0 law's galaxy gates alone.** It is scoped: see the caveats below.
- **Cluster predictions, no cluster input: FAIL.** No window member passes X-COP and groups on either footing (0/270).
  - X-COP's mean crosses zero near lambda_0 = 2.15 Mpc (+0.001 canonical, -0.023 alt). The rms is still 0.235 / 0.234 against
    the 0.10 line. The flat n = 1 core puts the dust at the wrong radii: too little in the centre, too much in the outskirts.
  - Groups: at most 1 of 20 pass the strict rule. The median Delta is +0.04 to +0.21 across the cluster-relevant
    lambda_0, and +0.37 once R_c exceeds a group's turnaround radius, where groups keep no dust.
  - For lambda_0 >= 10 Mpc nothing keeps dust, and X-COP returns to the plain law (+0.47 / +0.43).

## Known answers and controls

- K1: solver reuse (beta -1, mu0 1): 55.6403 = 55.6403.
- MUTATE 1 (lambda_0 1e-3 Mpc: compact cores everywhere): G5, G6 and G7 all fail. **BITES.**
- MUTATE 2 (f_cap 0): X-COP +0.4675 / +0.4345 = QX2; the lensing and elliptical baselines are reproduced exactly. **BITES.**
- MUTATE 3 (f_cap x3): moves X-COP by +0.419 / +0.414. **BITES.**

## Caveats (why the window is scoped, not a pass)

- The core is a stated idealisation. No dynamics were run: not the capture at z of about 2, not the heating, and not the
  puffing out to R_c >= 0.73 Mpc. Whether captured dust actually leaves galaxies as lambda_J grows, and on what timescale,
  is not shown.
- The linear growth gate assumes the a0 law is OFF on the linear web (QX3's assumption A-web).
- Galaxies are graded on gates only: SPARC inner mass, the KiDS mean shift and the elliptical mean shift. There is no full RAR
  refit, and no TT/EE peaks.
- The clock switch is a new term, A(tau) proportional to Omega_DE^p, with two constants (lambda_*, p) chosen from a window.
  Its tie to the dark-energy fraction is motivated, not derived.
