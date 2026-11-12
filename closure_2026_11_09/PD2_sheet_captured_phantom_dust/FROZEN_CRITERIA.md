# PD2 (sheet-captured phantom dust, the outside source's variant P): FROZEN CRITERIA, committed alone before any PD2 script or number

TEST lane, quarantined; registered RUNNING by the orchestrator. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11, v_stiff 265.8 km/s) and alt (1.1312e-10, 288.1), never pooled; QX15 footing h and omega. Read-only
machinery: PD1 (pd1.py data loaders, KiDS / SPARC evaluators; pd1_a1.py's halo rule; pd1_a2.py's DB1 child), WL1, GSMF.

## 1. Construction P, frozen once

**Single counting.** Poisson's equation is sourced by rho_b + rho_d only. Inside shell-crossed halos an auxiliary flux J sets
rho_d = div J / (4 pi G), with |J| = (nu(g_N,b / a0) - 1) g_N,b. So g_tot = nu g_N,b: the law once.

**Galaxy share (the source's defining formulas, graded as stated)**
- L_web = v_stiff / H0: 3.943 / 4.274 Mpc on the record's footings.
- Sigma_sheet = f_sheet rho_bar_d,0 L_web, with f_sheet = 0.60.
- R_ta^2 = 2 sqrt(G M_b a0) / (c_ta H_ta^2), with c_ta (H_ta / H0)^2 = pi / 2, read as c_ta H_ta^2 = (pi / 2) H0^2.
- M_share = pi Sigma_sheet R_ta^2.
- The phantom profile is truncated at R_trunc, where M_ph(<R) = M_share. Outside R_trunc the halo is Newtonian with M_b + M_share.
- Closed form, since both the phantom and the share scale as sqrt(M_b): R_trunc = 4 G Sigma_sheet / H0^2 = (3 f_sheet / 2 pi) Omega_d
  L_web, independent of M_b and z.

**Bracket S-claim (reported, never graded).** The source's stated closed form, R_trunc = (3/2) Omega_d (H0 / H)^2 L_web, at z 0
(KiDS) and at z of each P1 epoch.

**Disclosure (hand arithmetic, before any script).** The defining formulas give M_share of about 25 M_b at M_b 1e11 and R_trunc of
about 0.30 Mpc. The source's claimed 143 M_b and 1.48 Mpc correspond to c_ta H^2 = f_sheet H0^2 / 2 = 0.3 H0^2, not pi/2. So the
claimed numbers do not follow from the stated formulas. The lane grades the formulas and reports the claim as the bracket.

**Groups and clusters.** The source's filament / node rule is not stated precisely. Per the orchestrator, the frozen cluster rule
is PD1 A2's prefactor-1 profile scaled to 0.40 of the cosmic share:
- share = 0.40 x 5.41 M_b,sys;
- f_core = 1 - (v_stiff / v_vir)^2 of the share in a Duffy NFW core (v_vir > v_stiff);
- the phantom capped by the rest, and the remainder isothermal to R_ms;
- run through pd1_a1.py with PD1_SHARE = 2.164 and PD1_FCPRE = 1.0.
- This is disclosed as an orchestrator-supplied stand-in, not the source's rule.

**Screening.** Inside L* = 22 pc, div J -> 0 as (r / L*)^4 (inherited from the Pi^6 blend). Cassini and the moving Sun are carried
from the record's v3s results (MS3 PASS scoped). The suppression factor at Saturn's orbit is reported.

**Form choices beside the label:** f_sheet 0.60, the pi/2, L_web = v_stiff / H0, the 0.40 cluster fraction with the prefactor-1
profile, and the J equilibrium (if it is a closure, section 3). Fitted: 0.

## 2. Gates (order Q1, Q2 KiDS, Q2 SPARC, Q3 groups, Q3 X-COP, Q4, Q5 Bullet, Q6)

| gate | quantity | line |
|---|---|---|
| Q1 conservation | q_P(z) = [GSMF-summed M_share] / rho_bar_d at z 0.5, 1, 2 | <= 1 |
| **Q2 KiDS** | 59 points, pointwise. M(<r) = M_b + M_ph(min(r, R_trunc)) | \|shift\| <= 0.05 each (SS1 gate 1) |
| Q2 SPARC | PD1's QX8 evaluator with R_trunc | SS1 G5 |
| Q3 groups | pd1_a1 cluster rule (above) | >= 16 / 20 at f* 0 and 1 |
| Q3 X-COP | likewise; f_miss per bin vs TR1 0.71 / 0.66 / 0.58 | SS1 gate 3 |
| Q4 cosmology | cold reference by construction (J acts only inside shell-crossed halos), carried as PD1 P4; the 1-halo term NOT EVALUATED | carried |
| **Q5 Bullet** | graded: galaxy-traced Newtonian (PD1 A2's DB1 child, a0 -> 0) with each subcluster's cluster-rule dark mass inside R200. Gas-locked reading (DB1 law row + core / remainder galaxy-traced) reported | DB1 label |
| Q6 | Cassini and moving Sun carried (screening factor reported); Ursa Major carried as the law (P equals the law inside R_trunc) | carried |

**Label:** PASS iff Q1, Q2 (both), Q3 (both), Q4 and Q5 pass on that footing. Otherwise FAIL, naming the first failing gate.

## 3. P7: does the J equilibrium follow from an action?

**Check (computed as known answer KA-Q3).** An auxiliary Lagrangian term a0^2 F(|J| / a0) - J . grad Phi_b, varied in J, gives
|J| = a0 (F')^-1(g_N,b / a0). For |J| = (nu - 1) g_N,b with the record's nu, x = |J| / a0 satisfies y = x^2 / (1 - x) (x < 1), so
the required F'(x) = x^2 / (1 - x).
- The source's dF/dy = y / (y + 1) gives |J| = a0 y / (1 - y) instead. That is not the law.
- Separately: the conserved dust's own continuity and Euler equations are not shown to place rho_d = div J / (4 pi G).
- RESULT states whether P is action-derived or a closure.

## 4. Known answers

- **KA-Q1:** the sqrt(M_b) cancellation. R_trunc computed numerically (root of M_ph = M_share with the full spherical phantom) at
  log M_b 8-12, against the closed form. Equal within 2 % where the deep limit holds; deviations at high mass reported.
- **KA-Q2:** PD1's evaluators reproduce PD1's law-only replay (truncation off): KiDS 0, X-COP +0.4675 / +0.4345.
- **KA-Q3:** the inverse map y(x) = x^2 / (1 - x) checked numerically against nu at 20 points (1e-10).

## 5. Hand estimates and expected kills

- **Graded R_trunc about 0.30 / 0.36 Mpc.** KiDS fails beyond about 0.3 Mpc at every bin, about -1 dex at 3 Mpc (as PD1 A2's basin
  share).
- **S-claim 1.6 / 1.7 Mpc.** KiDS points at 1.6-3 Mpc go Newtonian: about log(1.6 / 3) = -0.27 dex. FAIL.
- **SPARC passes** (R_trunc is beyond every R_last).
- **Q1 passes:** the share sum is about 25 x sqrt-weighted rho_* / rho_d, about 0.1.
- **Clusters at 0.40:** f_miss is about 0.4 of the PD1 A2 prefactor-1 bracket (0.93 / 0.84 / 0.75), i.e. 0.37 / 0.34 / 0.30.
  X-COP under-filled: FAIL. Groups FAIL.
- **Bullet:** galaxy-traced with 0.40 of the share. Sub M300 low: FAIL.
- **P7:** a closure (section 3).
- **Expected label: FAIL / FAIL at Q2 KiDS.**

## 6. MUTATE

- **MQ1, f_sheet x 5** (3.0, close to the S-claim's normalisation): KiDS must move toward the S-claim value.
- **MQ2, cluster fraction 1.0:** X-COP must move (it reproduces PD1 A2's prefactor-1 PASS).

## 7. Operational

- One thread, nice 10; RSS < 1 GB; small json / out.
- Explicit-path commits via a sparse temporary worktree (scripted, plain bash), removed after.
- Files: pd2.py, pd2.json / .out, the pd1_a1 readings (pd1_a1_share2.164_fcpre1.0 and the MQ2 share 5.41), RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
