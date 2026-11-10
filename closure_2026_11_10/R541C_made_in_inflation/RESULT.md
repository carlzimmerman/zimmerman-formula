# R541C RESULT: a Gauss-Bonnet source gamma tau G_GB makes no lasting cold dark energy. EXCLUDED / EXCLUDED (canonical / alt)

2026-11-10. Criteria: `FROZEN_CRITERIA.md` (committed alone first, 21ab4cac19; a hand estimate made before freezing is
disclosed there). No amendment. Adopts nothing. kappa = 1/2 FITTED; not theory closed. The two footings give the same
numbers: a0 does not enter any gate, and both share omega_d 0.1209, h 0.674 (R 5.410 / 5.412).

## Label: EXCLUDED / EXCLUDED

The term cannot make the 5.41. In a flat expanding background sqrt(-g) G_GB = 8 d/dt(adot^3/N^3) exactly, so the
clock's charge equation with gamma tau G_GB integrates to

  a^3 n - 8 gamma (aH)^3 = C   (n = mu_K^2 (Q - 1)/K; covariantly nabla_m J^m = gamma G_GB).

The charge the term makes is n_GB = 8 gamma H^3 at every moment. It is made during inflation and handed back as H falls;
none of it is left as a^-3 dust. The lasting dust is C / a^3, and C is the same free integration constant as before.
With inflation, C is the pre-inflation value diluted by exp(-3 N_e). By the frozen rule this is EXCLUDED: Arm I gives no
lasting a^-3 charge at any gamma. The only reading that reproduces the amount with the term's own charge
(8 gamma H0^3 = rho_d0, ell = 222 Mpc) breaks three gates by large factors (table).

## Gates

| gate | result | line, source | verdict |
|---|---|---|---|
| GC0 dilution | x7.2e-66 / 6.7e-79 / 6.3e-92 at 50 / 60 / 70 e-folds | none (reported) | with inflation, "primordial initial condition" means a value set after inflation by some other process; without inflation C stays an initial datum, as in the record |
| GC1 generation | G_GB = 24 H^4 (de Sitter), -24 H^4 (radiation), -12 H^4 (matter), -12 (1+3w) H^4 in general. Steady density in inflation 8 gamma H_I^3, then it decays as H^3. Lasting a^-3 charge from the term = 0 for every gamma, H_I, T_reh and history (numerical run through inflation, radiation and matter: late value 1e-12 of the peak, integration error). R = C / rho_b0: still one fitted constant; gamma adds none to the dust; no natural value is singled out | R = 5.410 / 5.412 with no new fitted constant | fails: R is not produced |
| GC2 local (at ell_A = 222 Mpc) | the Sun must make or carry away 4.5e27 Msun per Gyr; a neutron star 1.7e42; a 10 Msun hole 5.9e42; Sgr A* 1.4e37. Charge inside Saturn's orbit >= 6.9e14 Msun | <= 1e-10 Msun (ephemerides, Pitjev and Pitjeva 2013; PROVISIONAL) | broken by 6.9e24 |
| GC3 cold | n_GB scales as H^3: w = 0.75 at z 3400, 1/2 in matter, 1 in radiation; and the term's net Friedmann contribution is -16 gamma H^3, negative (-2 rho_d0 today at ell_A) | w <= 0.01 by z 3400 (MK1 RESULT.md:113, KD1 B1a) | broken by 75 |
| GC3 isocurvature | not computed: nothing lasting is made, so there is nothing to be isocurvature | Planck 2018 X (indicative) | moot |
| GC4 coincidence | no baryon term in the charge equation; nothing ties C or the term to n_B | an explicit relation | none |
| GC5 tensor speed | c_T^2 = (1 + 16 ell Qdot)/(1 + 16 ell H Q); at ell_A c_T - 1 = -0.254 | -3e-15 <= c_T - 1 <= +7e-16 (Abbott et al. 2017, ApJL 848 L13; PROVISIONAL) | broken by 8.5e13 |
| GC5 static state / law | argued, not solved: in a static weak field the new metric terms are of order ell g / (c^2 r); at the ephemeris-allowed ell (about 1 m) that is far below anything measured. The law's form is unchanged where the term is allowed at all | none | reported |

Bounds on |ell| if the term is kept at all (Arm II, the free constant kept; reported): GW170817 <= 5.1e10 m (ell > 0) or
1.2e10 m (ell < 0); BBN (net term <= 5 % of the density at 1 MeV, indicative) <= 2.1e6 m; the Sun's charge outflow
against the ephemerides <= 1 m (crude). At ell ~ 1 m the term is irrelevant everywhere, and R is the old free constant.

## Reported only: the published mechanism

Chamseddine and Mukhanov (arXiv:2601.05931; text read through a summariser, PROVISIONAL) get lasting dust because their
coupling is f(phi) g(box phi) G_GB with g = (box phi)^3 = 27 H^3, not the plain linear term: then the source in de
Sitter integrates to 18 beta H_I^6 a^3 (reproduced, KA4) and dies with H^3 afterwards. With g = 1 their own integral is
(2/3) beta adot^3, reversible, which is this lane's result. Transplanted, a switched coupling (MU1b) leaves
8 gamma (aH)^3_end: R would then need gamma, H_I, T_reh and the switch (at least two fitted beyond the history; ell of
order 1e-54 to 1e-42 m for H_I 1e13 to 1e5 GeV), with no natural value and no link to baryons. For a falling clock
box tau is the expansion rate, the key TK1 found breaks at turnaround in a collapsing region. Not graded here; it would
be its own lane.

## Checks

- KA1 (gb_frw.out): sqrt(-g) G_GB - 8 d/dt(adot^3/N^3) = 0 with a general lapse; G_GB = 24 H^2 (Hdot + H^2); 24 H^4
  in de Sitter.
- KA2: Schwarzschild G_GB = 48 M^2/r^6 (R = 0, Ric^2 = 0).
- KA3: at gamma = 0 the tau equation is the record's a^3 mu_K^2 (Q - 1)/K = C (QX17 RESULT.md:107).
- KA4: the published integral 18 beta H_I^6 a_f^3 reproduced.
- KA5 (gb_tensor.out): a direct sympy second-order tensor action of sqrt(-g)[R/4K + xi(t) G_GB] gives
  c_T^2 = (1 + 16 K xi_ddot)/(1 + 16 K H xi_dot), equal to Kobayashi's form (difference 0); c_T = 1 at constant xi;
  no third derivatives of h in the equation.
- KA6: no dilution at N_e = 0.
- MU1a: with R^2 in place of G_GB the source is not a total derivative (residual printed); R = 0 in radiation, so an R^2
  coupling would leave a lasting charge. MU1b: a switched gamma leaves 2.763 against the 2.828 expected for this smooth
  history: the gate moves when the identity is broken.
- MU2: halving ell halves every GC2 number; doubling r_min divides the flux by 8.0.
- MU3: an a^-3 component returns w = 0. MU4: ell -> 0 gives c_T = 1; ell_A/2 gives -0.155 against -0.254.

## Weaknesses and what was not checked

- The hand estimate (the identity) was made before the criteria were frozen; the criteria say so. The scripts confirm it.
- Background only with P = 0. The P sector, W and the stiffness are untouched by the term in FRW but were not carried
  through the local (GC2) problem. GC2 is crude: it assumes the source is carried off as a stationary radial charge flux
  at speed <= c, not a solved hairy-body solution of the full equations (the analogue of the known shift-symmetric
  scalar-Gauss-Bonnet hair was not solved). The factor is so large (1e24 at ell_A, 5e10 even at the GW-allowed ell)
  that this does not decide the label, but the local bound on ell (about 1 m) is order-of-magnitude.
- ell_A, the "gamma needed", is the most generous reading (the term's total charge today equals rho_d0). No a^-3
  reading exists, so there is no other gamma_needed.
- c_T uses Q ~ 1 and Qdot ~ 0 today (the record's mu_K >= 198 per Mpc keeps Q - 1 tiny); not re-derived with the clock
  sector's own perturbations.
- External bounds (GW170817 numbers, ephemeris dark-mass limit, Read 2014 local density, Planck isocurvature) are from
  memory, not re-read: PROVISIONAL. The BBN line (5 %) is indicative and only reported.
- The paper's text was read through a summariser; its Eq. 31 coefficient (162) was not reproduced and is not used.
- The static-state / law statement is an order-of-magnitude argument, not a solution. No Lean file.
- Inflation is not adopted by the record; GC0 and GC1 state both cases.

## Files

`FROZEN_CRITERIA.md`, `gb_frw.py` / `.out`, `gb_tensor.py` / `.out`, `gb_numbers.py` / `.out` / `.json`, this file.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
