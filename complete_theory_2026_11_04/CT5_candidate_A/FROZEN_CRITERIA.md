# CT5: candidate A (four-form tie inside the screened v3s action), FROZEN CRITERIA

Written before any script or number of this lane. Grading lane under owner decision D1 ("Yes, grade it", `../OWNER_DECISION_2026-11-04_D1.md`) and `../CT_GATES_COMMON.md`. A go to grade, not an adoption: nothing here is adopted, the cold sector retired on 2026-11-01 is not reinstated, no particle. kappa = 1/2 FITTED. Footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s^2, reported apart, never pooled. Not theory closed. Nothing here says the data favour the framework.

## 1. The combined action (candidate A, CT1_REPORT.md:54-59)

Signature (-,+,+,+). v3s (V3_FULL_PICTURE.md:3, 25-35) with its constant Lambda removed from J and its MOND scale promoted to a Henneaux-Teitelboim four-form flux:

    S_A = (c^3/16 pi G) ∫ sqrt(-g) [ R - 2 J_A(Y; q) + 2 K(Q) ]  -  (gamma_L/2) ∫ sqrt(-g) [max(D_i P^i, 0)]^2
          + ∫ sqrt(-g) P(q)  +  S_bdy[A_3]  +  S_m[g, matter]

    F_4 = dA_3,   q = -(1/4!) eps^{mnrs} F_mnrs   (so F_mnrs = q eps_mnrs),   P(q) = Z q^2/2 - C0
    J_A(Y; q) = -2 a_g(q)^2 [ u - ln(1+u) ],   u = sqrt(Y)/a_g,   a_g = a0(q)/c^2,   a0(q)^2 = xi G q^2
    K(Q) = mu_K^2 (Q - 1)^2,   gamma_L = K L*^2 / 2,  L* >= 21.7 / 22.9 pc   (all as v3s)

- S_bdy is the Brown-Teitelboim / Duncan-Jensen boundary term that makes the A_3 variation well posed; with it the four-form's gravitating vacuum energy is the Legendre form eps_vac = q dL/dq - L|_q (k04, kappa_closure/README.md:45).
- With x = 0 (FRW), eps_vac = Z q^2/2 + C0, so rho_DE c^2 = Z q^2/2 iff C0 = 0, and kappa^2 = a0^2/(c^2 G rho_DE) = 2 xi / Z (CT1_REPORT.md:56-57: a TRADE).
- A_3 field equation: d_m Pi = 0 with Pi = dL/dq, so Pi is one constant in space and time (an integration constant; Henneaux-Teitelboim). q has no kinetic term and no local degree of freedom; it is slaved algebraically to the local khronon acceleration.
- No dust phase is added. The action's only dust-like sector is v3s's own K(Q) khronon dust (alpha = 1, V3_FULL_PICTURE.md:85-98), which is not tied to rho_DE (C2: d rho_dust / d a0 = 0, CT3_REPORT.md:17). A does not supply a rho_DE-tied dust phase naturally; if none appears in the derivation the report says the dust phase must come from elsewhere (CT8).

## 2. Method (derive, no knob scan)

Static weak field: the khronon J-sector Lagrangian density is L_J(g, a) = (a^2/4 pi G) f(g/a), f(s) = s - ln(1+s), whose g-derivative gives the J-flux j = g a/(g + a) (the record's capped hold flux, X14: |KP| < a0). Together with GR's -g^2/(8 pi G) it gives the simple-mu law S (V3_FULL_PICTURE.md:47-49). Varying q at fixed Pi gives, with r = a_loc/a0 and eps = kappa^2/(8 pi):

    r [ 1 + eps h(x/r) ] = 1,   h(s) = 2 f(s) - s f'(s),   x = g/a0   (g the total static field = |grad Xi|)

(to be re-derived symbolically in the script, sign included). eps is footing-independent because kappa = 1/2 is held fixed on both footings; a reading with the alt footing's tied kappa 0.6043 (XR31 row 3) is reported beside, ungraded.

## 3. Gates (in order; stop at the first FAIL; numbers restated from the CT reports)

**G0 health** (CT_GATES_COMMON.md:6). PASS iff all of:
- (a) DOF: v3s's 3 (V3_FULL_PICTURE.md:184) plus 0 from A_3; no new propagating mode.
- (b) No ghost: Z > 0 (positive rho_DE) and the q-Legendre map is invertible, dPi/dq|_x > 0 at every x on the grid.
- (c) FRW: q constant in time and space on FRW (Y = 0), so the slaving enters perturbations only at second order.
- (d) Static backgrounds, on a log grid x = g/a0 in [1e-3, 1e-8/a0] (the G1 range: up to 106.8 / 88.4 on the two footings), on the slaved (Routh, fixed-Pi) kernel:
  - total static operator elliptic: dF/dg > 0 and F/g > 0, with F = g^2/(g + a_loc(g));
  - the khronon/dust pair's coefficients M_T = g / j and M_L = 1 / (dj/dg), with j = g a_loc/(g + a_loc) the slaved J-flux (unslaved: M_T = 1 + x, M_L = (1+x)^2, V3_FULL_PICTURE.md:60-61), must satisfy M >= 1 (Lean `switched_stable_where_positive`, V3_FULL_PICTURE.md:179). Any grid point with M_L < 1 or M_T < 1 is a FAIL of G0 (gradient instability of the khronon sector on a static background; omega^2 = 4 pi G rho_tau (M - 1 + L*^2 k^2/2) < 0 for k L* < sqrt(2(1 - M))).
- W4b (solar-background health) is recorded as inherited, UNDECIDED (CT2_REPORT.md:7); it does not decide G0 alone.

**G1 weak field** (CT_GATES_COMMON.md:7). Slaved law g^2 = g_N (g + a0 r) with r from section 2; PASS iff max |log10 g_A - log10 g_law| <= 0.01 dex over 1e-12 < g_b < 1e-8 m/s^2, both footings.

**G2 local constancy** (CT_GATES_COMMON.md:8; CT1_REPORT.md:58, 80). Probe 30 kpc from galaxies of baryonic mass 1e9, 1e10, 6e10, 2e11 Msun (point mass), total field from the law on |g_N,int + g_N,ext| (aligned, worst case; the algebraic EFE reading, labelled). Environments: void g_N,ext = 0; field g_N,ext = 0.05 a0; cluster outskirts at R = 1 Mpc and 0.3 Mpc from a cluster of baryonic mass M_b(<R) = 1e14 and 3e13 Msun (PROVISIONAL representative inputs); cluster core: 30 kpc from a BCG + ICM with M_b(<30 kpc) = 1.5e12 Msun. PASS iff the spread of log10 a_loc across environments is <= 0.015 dex for every galaxy mass, both footings.

**G3 tie** (CT_GATES_COMMON.md:9; CT1_REPORT.md:81). (a) slope d ln a0/d ln rho_DE across flux sectors (x = 0) = 0.5 +- 0.01, with C0 counted as a hand-set zero. (b) a0(z) from A's own FRW equations against sqrt(rho_DE(z)/rho_DE(0)) for the analytic CPL background w0 = -0.75, wa = -0.86 (DESI DR2 combined central, PROVISIONAL from memory) at z 1, 1.5, 2.33: PASS iff every |difference| <= 0.05 dex. If A's equations force w = -1 (q constant), the evolving part must come from another component that a0 does not see; graded as derived.

**G4 local gravity** (CT_GATES_COMMON.md:10; CT2_REPORT.md:52, 61, 97-107): only if G0-G3 pass; Q2 <= 5.2e-27 s^-2 at both host-field conventions, planets, PPN, |c_T - 1| inside [-3e-15, 7e-16], on C6/C6P with the slaved a_loc.

## 4. If a gate fails

The candidate stops there. The slaving equation of section 2 is common to G0-G2, so its G1 and G2 values may be printed as UNGRADED READINGS, labelled, with no gate verdict. No retuning: xi/Z, L*, mu_K, J_x are not varied.

## 5. Hand-set constants to count

kappa (= the ratio 2 xi/Z), C0 = 0, Pi (the flux's integration constant, sets rho_DE; an initial datum), L* (gamma_L), mu_K, J_x's form (POSTULATED, V3_FULL_PICTURE.md:30), the K(Q) dust abundance (an initial condition).

Compute: one python/sympy script, single thread, seconds, < 1 GB. Commit nothing (the parent commits).
