# Frozen criteria (written before the script was run)
Question: does the cold->dark-energy conversion model (rho_DE rises as rho_b0 (1+z)^3 dR; R: 5.364 -> 4.80; conversion rate shape psi(z) = (1+z)^2.6/(1+((1+z)/2.6)^6.2), the shape the pasted script used) reproduce the DESI DR2 CPL a0(z)/a0(0)=sqrt(rho_eff/rho_eff0) bands (p13c CSV, four fits, 68% and 95%) at z = 0.5, 1, 2?
Mapping: a standard analysis assumes matter = Omega_m0 (1+z)^3 and calls the rest 'dark energy': rho_eff(z) = rho_crit E^2 - rho_m_assumed(z). Two anchorings of the assumed matter: A) today (rho_b0(1+R(0))), B) early (rho_b0(1+R_prim)).
PASS for an anchoring and fit: model sqrt(rho_eff/rho_eff0) inside the 95% band at all of z=0.5,1,2. Model 'survives' if some anchoring passes in some fit; it is 'excluded' if no anchoring passes in any fit. Report per-z too.
Mutations: (M1) psi concentrated at z>3 must fail; (M2) conversion into baryon-like w=0 (no (1+z)^3 weight) must fail to reproduce a z=2 dip.
Footing: p13c CSV only; no chains (_external_data absent). Not a refit of the expansion history, so 'survives' means not excluded by the CPL summary, not a detection.
