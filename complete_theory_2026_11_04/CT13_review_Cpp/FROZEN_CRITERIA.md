# CT13: independent review of candidate C'' (frozen before any number)

Candidate: v3s action (V3_FULL_PICTURE.md §1) with a0^2 = kappa^2 G rho_phi, rho_phi = 2 X P_X - P, P = X - V(phi), plus phi's action.
In the static/weak J sector: L = X - V + L_M, L_M = (a^2/4 pi G) f(g/a), f(s) = s - ln(1+s), g = |khronon acceleration|.
Review, not adoption. kappa = 1/2 FITTED. Not theory closed. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2.

Checks (own sympy/numpy, `ct13_review.py`; the CT10 README/report are not read before the numbers):
- R1 field equations: dL_M/drho at fixed g; phi EOM; khronon flux with a(rho).
- R2 quadratic action on (a) FRW (g = 0) and (b) static weak field (phi rolling, g != 0): K_t, K_s, khronon mixing B, khronon L_gg, effective mass. PASS iff K_t > 0, K_s > 0 and the mixed (phi, Xi) system has no ghost, for 1e-3 <= s <= 1e22, 0 < 1+w <= 1.9.
- R3 rho_phi at X < 0: well defined? is X < 0 reached for |grad dphi| from the local solve?
- R4 c_s^2 = K_s/K_t, its maximum, with and without mixing; hyperbolicity = K_t, K_s > 0 (cone Lorentzian). Literature reading provisional.
- R5 local response: solve div[(1+eps h) grad dphi] = -2 eps h V' (quasi-static, spherical) for void, MW, cluster, Sun with law-S g(r); delta log10 a0 vs 0.015 dex (G2) and vs G1 0.01 dex; Cassini inherits v3s C6 (<= 3.6e-8 Park, CT2_REPORT.md:7) iff delta a/a is negligible.
- R6 FRW: phi EOM unmodified at g = 0 (h(0) = 0, f(0) = 0); a0^2 propto rho_phi exactly; w >= -1.
- R7 (coordinator add): early universe with eps<h> = E up to 6e5 (CT12 out:29-35): K_t, K_s, c_s^2, mixing, background drift of rho_phi, from recombination to BBN.
Gate verdicts per CT_GATES_COMMON.md G0-G4; first fail stops.
