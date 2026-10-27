# argon_clues

Audit of the pasted "cold energy / black holes / dark energy / horizon" synthesis.
Run: `python3 -I check_pasted_claims.py` (writes `check_pasted_claims.json`).
Related prior work: `sol61_push/cold_horizon_connection_2026_10_14/` (exact SdS horizon roots, Nariai q, r_M comparisons).

## Holds (symbolic, exact)
- a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = c H_Lambda / Z, Z = sqrt(32pi/3) (kappa = 1/2 is still FITTED, not derived).
- r_MOND^2 = GM/a0 = (Z/2) r_s R_dS, so r_MOND = sqrt(Z/2) sqrt(r_s R_dS), sqrt(Z/2) = 1.701. An identity given a0 = c H_Lambda/Z; it adds no content beyond the a0 law.
- a0 = sqrt(3pi/8) c k T_dS / hbar: a0 is a rescaled Gibbons-Hawking temperature (same statement as a0 = kappa_dS/Z; no new physics).
- BH surface gravity kappa_BH/a0 = 1e13-1e23 for M87-1 Msun, so mu_fw = 1 there: GR at the horizon.
- Numbers: a0 = 9.36e-11, T_dS = 2.20e-30 K (pasted 2.3e-30 is ~5% high), R_dS = 5.4 Gpc.

## Wrong in the pasted text (do not carry over)
1. **M_crit = c^2 R_dS/(4G) is not the Nariai mass.** Nariai is c^2 R_dS/(3 sqrt3 G); ratio 3sqrt3/4 = 1.299 (2.8e22 vs 2.2e22 Msun). kappa_BH = kappa_dS is a naive-Schwarzschild matching, not the SdS merger point. "Heat flows until T_BH = T_dS" is unsupported.
2. **mu_fw(x>>1) = 1 - 1/(2x) + 1/(8x^2)**, not 1 - 1/(8x^2).
3. **Scaling:** a0 and T_dS go as rho_DE^(1/2); r_MOND goes as rho_DE^(-1/4) (inverse, not +1/4).
4. **a0(z=3) = 0.74 a0(0) is not a geometry result.** Constant Lambda gives exactly 1. 0.747 appears only for CPL w0=-0.75, wa=-0.85 (0.85 / 0.92 for milder fits). It is conditional on the dark-energy fit and is the "a0 tracks rho_DE" branch, not the FLAT law.
5. "Cold energy = the T_dS floor in the DC/AC split" is a definition choice. It conflicts with the repo's current cold-energy work (a field-stress medium, CFG660-699, with settling/relaxation tests), so it is a proposal, not a result.

Not done: the interactive explorer (say if you want it as an HTML page here).
