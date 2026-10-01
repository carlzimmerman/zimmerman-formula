# B3: modified-gravity horizon equations -- can kappa r_h = 1/2 and Lambda r_h^2 = 8 pi sit at one horizon?  (c = G = 1; kappa f-normalised)

## Bottom line
Verdict: **NOTHING NEW (with one sharp structural no-go).** (1) Every theory whose static vacuum branch is an Einstein space (f(R) constant-curvature branch, Horndeski stealth SdS, Rastall vacuum, no-hair scalar-tensor) has the *identical* horizon relation 1-2 kappa r_h = Lambda_e r_h^2 (b01, b02, b04), so T=(1/2, 8 pi) is excluded for every coupling. (2) Only theories that change the *form* of f can host T; the only exact one checked, 4D Glavan-Lin/EGB, hosts it only at a dimensionful coupling alpha = -(8 pi/3) r_h^2 = -2 pi/(3 a0^2) (Lambda_b reading) on the non-GR branch with G_eff<0; in the Lambda_e reading no single-branch solution exists (b03). The needed coupling contains pi only because T was imposed, and is a new length tied to 1/a0: it re-inserts the coefficient. (3) The Wald/first-law factor 4 is rigid (8 pi/2 pi) and is not produced non-trivially (b03 E4/E5, b05). No principle declared in advance fixes any coupling. kappa = 1/2 stays FITTED.

## What was done (principles declared and hashed first: `PRINCIPLES_DECLARED.txt`, sha256 dd2353ba...fce4)
Scripts (all exit 0): `b01` 9/9, `b02` 15/15, `b03` 30/30, `b04` 9/9, `b05` 9/9 (72/72), each with controls/mutations that fail when the claim is wrong. Two of my own first-draft slips were caught by the checks and fixed (a dropped 1/r_h in f'(r_h); a double application of (D-3)(D-4)).

## Results per theory
| theory | exact horizon relation | free parameter? | T allowed? | G_eff / Wald |
|---|---|---|---|---|
| GR (control = p12) | 1-2 kappa r = 8 pi rho(r_h) r^2; with N_h: kappa r = N_h(1-8 pi rho r^2)/2 (b01) | no | no | G, S=A/4 |
| any "SdS-form" vacuum | 2 kappa r_h = 1 - Lambda_e r_h^2 exactly (K2) | irrelevant | **no for every coupling** | -- |
| f(R), constant R (b02) | same as above, Lambda_e=R0/4 with R f'=2f (Lambda_e != Lambda_b once cubic term present) | no | no | G/F(R0), c_W = F(R0) |
| f(R), non-constant R (b02 F2) | F_h(1-2 kappa r_h/N_h) = (r_h^2/2)(F_h R_h - f(R_h)) + (kappa r_h^2/N_h) F'_h (N'_h and B2 drop out) | F'_h, R_h are horizon data of the solution, not theory constants | formally yes (free data); no Lambda_e tie | c_W=F_h |
| EGB, D-dim, exact Boulware-Deser (b03; D=5,6 field eqs verified; D=4 H_mn=0 control) | (2 kappa r_h+2)(1+2a) = (D-1)(1+a-lam r_h^2), a=alt/r_h^2, alt=(D-3)(D-4)alpha | alt (dimensionful) | yes, for one a | G_eff=G/(1+2a); Wald (Om r^(D-2)/4)(1+2(D-2)alt/((D-4)r^2)) = int dM/T (D=5,6 exact) |
| Lovelock (any P(psi)) | P'(psi_h)(2 kappa r_h+2) = (D-1) r_h^2 (P(psi_h)-lam) (b03) | one coupling per order; 4D Lovelock = GR | trivially yes (D3) | 1/P'(psi_h) |
| 4D Glavan-Lin (D->4 limit of the above) | a = -Lambda_b r_h^2/3 at kappa r_h=1/2 | alt | Lambda_b reading: a=-8 pi/3 on the NON-GR root (1+2a=-15.8, G_eff<0), solution ends at r_b=1.236 r_h (branch point). Lambda_e reading: a=-0.1177, but horizon root has 1+2a>0 while the Lambda_e=8 pi vacuum is the other root (1+2a psi_vac=-0.97): no single-branch solution | first-law entropy S=pi r^2+4 pi alt ln r (not Wald A/4(1+..)) |
| Horndeski G^{mn}phi_m phi_n (Babichev-Charmousis, b04, all 4 field eqs verified) | exact SdS, Lambda_e=-eta/beta independent of the bare Lambda; Lambda_b only sets q^2 | eta/beta (dimensionful) | **no** (K2) | -- |
| DHOST/other stealth | NOT VERIFIED beyond the same structure (K2 applies if the metric is SdS-form) | | | |
| Rastall (b02 R1) | vacuum fluid: Lambda_e = 8 pi rho/(1-4 k l); T=0 vacuum = GR | k l (dimensionless, free) | horizon relation unchanged (K2); only the rho<->Lambda map changes: G rho_Lambda = (Lambda/8 pi)(1-4kl)... free factor | -- |
| MOND-type (b05 M1) | Newtonian-limit phantom rho_ph = (M/4 pi r^2) d(nu-1)/dr >= 0 for every monotone nu, but T needs rho_extra(r_h)=-rho_Lambda<0 | -- | no in the weak-field estimate; at T g_N(r_h)=a0 exactly (x=1). Strong-field, so not a proof | -- |
| Einstein-aether, Horava/khronon (universal horizon), AeST, TeVeS, BIMOND, record CA5/V0 | **NOT computed** (no verified static horizon equation; the record's actions keep a GR+Lambda metric sector, so p12 applies with rho_extra = carrier stress at r_h, unknown) | dimensionless c_i, lambda, K_B | unknown | G_N = G/(1-c14/2) (literature, not verified here) |

## The four findings that matter
1. **Allowed-ness is uninformative (D3).** Any single-coupling extension F(kappa r, Lambda r^2; a)=0 reaches T for some a. Only whether the coupling is fixed counts.
2. **Fixing fails (D2).** The one exact host (GL) needs a length alt = -(8 pi/3)/(4 a0^2): dimensionful, tied to a0 by hand, with pi supplied by T. Dimensionless-coupling theories that were computable (Rastall, Horndeski ratio, f(R)) never reach T.
3. **Factor 4 (D4).** The GR first law gives S=A/4 from T=kappa/2 pi and Einstein's 8 pi (b05); Wald in EGB agrees with int dM/T; the EGB entropy factor at T is 1+4a = 1 - 32 pi/3 = 1 - Z^2, but this is just 4 x (8 pi/3) for any imposed Lambda r^2 (decoy y gives 1-4y/3): arithmetic, not a result. G_eff rescaling leaves the G-free statement Lambda r_h^2=8 pi untouched.
4. **BH normalisation.** At T even in GR the mass is negative (M=-3.69 r_h), f is monotone and there is no free-fall point, so Bousso-Hawking normalisation is undefined (b01 K4).

## NOT established
Einstein-aether/Horava/AeST/TeVeS/BIMOND/record-action horizons; non-spherical or time-dependent horizons; whether GL 4D EGB is a consistent theory (only its exact f was used); the weak-field MOND sign argument at a strong-field radius. T remains a statement about a global or nonlocal tie, as p12 concluded.
Files: `b01..b05_*.py/.out`, `PRINCIPLES_DECLARED.txt`, `PRINCIPLES.sha256`.
