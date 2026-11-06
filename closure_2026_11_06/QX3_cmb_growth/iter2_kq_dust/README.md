# QX3 iter2: v3s's K(Q) sector as the clustering component: FAIL (no window)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane reopening a cold-dark-energy sector (owner 11-04 rule);
no particle. Criteria: FROZEN_CRITERIA.md (93562260e2). Amendment A1 (4c2426c123): a CLASS output bug was found after the
first G1 print, which is void and kept on record; numerics changed to implicit midpoint (A1b) before any G2 number.

## Derived (Lean: fable_independent_2026/lean_2026/QX3_dust_eos.lean, 0 sorry, standard axioms)

v3s's K = mu_K^2 (Q-1)^2, read as a fluid:
- rho = A(Q^2 - 1) and p <= rho^2/(4A): an n = 1 polytrope.
- Jeans wavenumber k_J = mu_K, physical and the same at every density and time.
- Every self-gravitating core has radius pi/mu_K.
The sector clusters like dust above lambda_J = 2 pi/mu_K and not below it.

## Results (iter2.json)

- **G1, CMB-lensing shape at mu_K -> infinity: PASS.** Worst corner chi^2 = 8.57 against the 18.48 line, all 8 bracket corners
  between 8.22 and 8.57. Raw PR4 bandpowers, CMB-marginalised covariance. omega_d fitted at 0.112-0.124; implied A_s
  2.02-2.31e-9. MUTATE (baryons only, amplitude refit) gives chi^2 869-929 at every corner, so the gate has power.
  - K1: FFP10 gives 8.86. K1b: CLASS against FFP10 is 0.95-1.00 at L 10-400.
- **G2, how small the Jeans length must be:** mu_min = 2.5e4-4.0e4 Mpc^-1 (worst 4.0e4). That is lambda_J <= 0.16 kpc
  physical, and the result is generous to the mechanism (no Jeans suppression before z = 3400). K2: mu = 1e6 reproduces dust to 2.2e-4.
- **G3, dust stays out of galaxies:** mu_max = 79 Mpc^-1 (core radius >= 40 kpc, Jeans mass at turnaround above the galaxy's halo).
  At mu = 100 the captured core already puts 0.41 M_b of dust inside R_opt; at mu >= 1e3 it puts 4.2 M_b (line 0.3).
- **Gap: mu_min/mu_max = 500.** No value of mu_K lets this sector make the CMB-lensing shape and also leave the a0 law alone
  in galaxies.

## Label

**FAIL (no window).** The sector that fixes the CMB-lensing shape (it is CDM-like once lambda_J is below about 0.2 kpc)
collapses into every galaxy, adding about 4 M_b of dust inside the optical radius. That breaks the law's SPARC/RAR pass. This
is the X22 / FG1 wall seen from the action. Linear growth gets the same label.

## Assumptions and limits

- A-web: the a0 law is OFF on the linear web. If it is on, WG2 says lensing overshoots 11-14x, which is worse.
- Galaxy capture uses f_cap 0.76 (X22). A core radius of pi/mu_K is generous, because baryons would compress it.
- Linear CLASS spectrum; no halofit (an LCDM-calibrated tool), L <= 400.
- This does not grade the CMB TT/EE peaks, clusters, or the dust's coupling to J(Y) beyond linear order.
