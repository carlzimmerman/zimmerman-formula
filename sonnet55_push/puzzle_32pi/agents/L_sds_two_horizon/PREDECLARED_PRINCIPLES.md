# PREDECLARED principles and success criterion (written BEFORE any script of this lane was run)

Conventions: c = G = 1, L = 1/H_Lambda = sqrt(3/Lambda), f(r) = 1 - 2M/r - r^2/L^2, x = r_b/L, y = r_c/L, mu = M/M_N with M_N = L/(3 sqrt 3).
kappa_h = |f'(r_h)|/2 ("f-normalisation" = Kodama normalisation, kappa_c(M=0) = H). "BH-normalisation" = Bousso-Hawking, xi = d_t / sqrt(f(r*)), r*^3 = M L^2.
Z = sqrt(32 pi/3), a0 := H/Z. The a0-point of a horizon is the mass at which that horizon's kappa (f-normalisation) equals a0 (the audit's H2).

Disclosure of what I already knew before declaring: from the audit (agents/I_adversarial_audit/a07) the a0-point of the black-hole horizon is M = 0.98695 M_N, r_b = 0.5226 L, r_c = 0.6304 L.
I had not computed any of the principle outcomes below; I had estimated, by hand and mentally only, that (i) thermal equalities give algebraic points, (ii) the SdS family is a monotone one-parameter family so extremum principles select endpoints.
Those expectations are NOT part of the criterion; each principle is decided by its script.

## Success criterion (fixed now)
A principle SUCCEEDS iff (a) it is stated without using Z, a0, 32 pi or any target, (b) the point it selects has kappa_b/H (f-normalisation), or kappa_c/H, or the BH-normalised kappa/H (each declared separately)
equal to 1/Z = sqrt(3/(32 pi)) = 0.17274707... to relative accuracy 1e-10, and (c) the selection is derived, not scanned.
A principle that selects an endpoint (M = 0 dS point, or Nariai M = M_N) FAILS for interior a0. A principle whose outcome requires inserting a coefficient equal to the puzzle's own (kappa_b^2 = Grho/4) is a RESTATEMENT (not a success).
Every Omega-dependent reading is DATA-DEPENDENT and is never used to fit or to select; it is reported only as a comparison.

## Principles (each is a physical statement; the formal selection equation is given)
E1  Thermal equilibrium between the horizons: T_b = T_c, i.e. kappa_b = kappa_c (either normalisation).
E2  Entropy extremisation on the family: stationary points in mu of S_tot = S_b + S_c = pi (r_b^2 + r_c^2), and of S_b S_c, S_b/S_c, S_c - S_b, each taken with the scale held fixed as
    (i) L (Lambda) fixed, (ii) M fixed, (iii) r_b fixed, (iv) r_c fixed [S_i / (pi scale^2) as a function of mu].
E3  Smarr-type balance in the extended (P = -rho_Lambda) first law: M = kappa_b r_b^2 + (8 pi/3) rho_Lambda r_b^3 (verify); principle: the surface term and the vacuum PV term contribute equally (2 T S = 2 rho V).
E4  Bekenstein-type saturation: (a) S_b = 2 pi M r_b, (b) S_b = 2 pi E_MS(r_b) r_b with the Misner-Sharp energy (check whether it is an identity), (c) Bousso/dS-entropy bound S_tot = S_dS.
E5  Unruh-effective matching in the static patch: T_eff(a) = sqrt(a^2 + H^2)/2 pi. Match T_eff(a) to the Hawking temperature of (i) a flat-space Schwarzschild hole of mass M in {M_N, L/2 (= Misner-Sharp mass of the dS horizon)},
    (ii) the SdS horizons at M = M_N in the BH normalisation, (iii) the SdS cosmological horizon at a general mu (map a <-> mu). Report the a/H each gives and which mu corresponds to a = a0.
E6  Euclidean conical regularity: with beta = 2 pi/kappa_b, Int E4 = 64 pi^2 (1 + kappa_c/kappa_b); quantisation Int E4 = 32 pi^2 n (n integer) and the orbifold condition cone angle = 2 pi/N (or rational 2 pi p/q); the same with beta = 2 pi/kappa_c (cone EXCESS at the black-hole horizon). List every allowed kappa ratio, its mu, and kappa_b/H there.
E7  (DATA-DEPENDENT) matter content read as a horizon-sized mass: M_m(R) = (4 pi/3) rho_m R^3 with R = L (dS radius) and R = R_H = 1/H_total; mu_obs = M_m/M_N as a function of Omega_m (Planck-2018-like Omega_m ~ 0.315 used only as an illustration), and which Omega_m the a0-point would imply. Never used to fit.
E8  pi-count / transcendence theorem for the family (proved, not scanned): if the selection of mu is given by an algebraic condition (algebraic in Lambda-units) then all dimensionless SdS numbers are algebraic; 1/Z = sqrt(3/(32 pi)) is transcendental. Then repeat holding G rho_Lambda (not Lambda) fixed and state what changes.
E9  Closed-form scan of every dimensionless quantity at the a0-point (with DECOY values Z' in {2 pi (Milgrom), 6 (Verlinde), 5.5, 6.5, sqrt(8 pi/3), sqrt(32 pi/3)*1.05} to calibrate the hit rate). A closed-form hit counts only if it appears at the a0-point and NOT at the decoys, at tolerance far below the false-positive rate.
