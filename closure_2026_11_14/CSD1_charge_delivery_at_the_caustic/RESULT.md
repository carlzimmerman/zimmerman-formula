# CSD1 RESULT (2026-11-14, written from 15:01 EST by the clock): does the falling clock's own flow deliver, inside the k-th caustic, the charge the law's halo needs there?

Criteria 127a25a942 (committed alone, before any script or number). AMENDMENT A1 6e2d39d50d (before any graded number).
AMENDMENT A2 689e3a5513 (post hoc: a NaN-handling fix in KA7 after the first grader output was read). Scripts
c7b3195af1, grader fix af929db57f. TEST lane, not blind. Adopts nothing, relabels nothing, registers nothing. Footings
never pooled. Nothing here can say the theory is closed or that the data favour it.

## 1. Labels (tolerance |log10 D_k| <= 0.10; headline = caustics k = 2 and 3)

| supply | canonical | alt |
|---|---|---|
| **S-seed** (FLD1's isolated seed, the record's own infall) | **SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3** (also k = 1 and 0.5 R_fold) | **SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3** (same) |
| **S-ref** (the reference layout's cold mass as the delivered charge; D_k = XJ1's s) | **DEPENDS ON MASS AT CAUSTIC 2 / 3** (k = 3 crossing at log M_b 10.09 at z 0, 8.72 at z 2.2, 8.62 at z 3.0, 8.88 at z 4.4) | **DEPENDS ON MASS AT CAUSTIC 2 / 3** (k = 3 crossing at 10.42, 9.08, 8.97, 9.22) |
| **S-cos** (the clock's own shell equation, patch tuned to PD1's share 59.5 with the law off; graded law on, 3 masses) | **SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3** | **SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3** |

In plain words: **the clock's own flow does not deliver the law's charge at any caustic, at any mass, at any redshift
graded.** It delivers 1 to 7 % of it (S-seed), and 2 to 12 % even when the patch is seeded with the cosmological share
(S-cos). The reference layout (S-ref) holds about the law's charge at the caustics, from 0.49 to 1.67 of it, under at low
mass and over at high mass; it is not a flow, so it shows only what a delivery would have to supply, not that any flow
supplies it. The missing transport is not supplied by QX17's non-advective flux: that channel carries about 1e-6 of
what is missing.

## 2. Numbers

### 2a. S-seed, D_3 = Q_flow(< R_3) / C_law(R_3) (D_1, D_2, D_half agree with D_3 within 35 %; all in `csd1_grade.out`)

| log M_b | can z 0 | 2.2 | 3.0 | 4.4 | alt z 0 | 2.2 | 3.0 | 4.4 |
|---|---|---|---|---|---|---|---|---|
| 8 | 0.0171 | 0.0114 | 0.0107 | 0.0095 | 0.0155 | 0.0103 | 0.0097 | 0.0086 |
| 9 | 0.0251 | 0.0166 | 0.0150 | 0.0126 | 0.0226 | 0.0150 | 0.0135 | 0.0112 |
| 9.4 | 0.0293 | 0.0193 | 0.0174 | 0.0149 | 0.0266 | 0.0173 | 0.0156 | 0.0134 |
| 10 | 0.0371 | 0.0245 | 0.0224 | 0.0197 | 0.0337 | 0.0220 | 0.0200 | 0.0178 |
| 10.45 | 0.0444 | 0.0296 | 0.0273 | 0.0248 | 0.0402 | 0.0266 | 0.0244 | 0.0220 |
| 10.7 | 0.0491 | 0.0329 | 0.0305 | 0.0285 | 0.0445 | 0.0296 | 0.0272 | 0.0249 |
| 10.9 | 0.0531 | 0.0361 | 0.0332 | 0.0311 | 0.0481 | 0.0322 | 0.0298 | 0.0277 |
| 11.2 | 0.0603 | 0.0413 | 0.0382 | 0.0368 | 0.0543 | 0.0375 | 0.0342 | 0.0320 |
| 11.5 | 0.0681 | 0.0473 | 0.0443 | 0.0432 | 0.0616 | 0.0423 | 0.0390 | 0.0379 |

- log10 D over every cell and k: -2.07 to -1.17 canonical, -2.12 to -1.21 alt. History (every output z 0 to 4.4):
  D_3 never exceeds 0.069 (canonical) / 0.062 (alt). Background-subtracted D (Dexc) differs by under 2 %.
- D grows with mass about as M_b^{0.17} (hand estimate M_b^{1/6}) and with time.
- **Equal-charge radius: none.** On every mass, footing and graded redshift, D(r) = Q_flow(< r)/C_law(r) stays below 1
  from 1 kpc to R_ta; its largest value is 0.008 to 0.096, at 0.003 to 1.0 R_fold.
- **One-sided densities at R_3 (w = 0.10; 0.05 / 0.20 brackets within about 30 %):** N_in / N_out = 27 to 102 at z 0,
  27 to 102 at z 2.2, 34 to 149 at z 3.0, 48 to 173 at z 4.4 (both footings).
- **Front speed and required inflow at R_3:** Rdot_3 = 0.6 to 8.3 km/s at z 0 and 1.2 to 23.6 km/s at z 2.2 to 4.4. A
  standing interior needs inflow v_req = Rdot (1 - N_in/N_out) = -52 to -258 km/s at z 0 and -113 to -1173 km/s at z
  2.2 to 4.4. The flow's own net radial velocity there (all streams) is -54 to +34 km/s, mostly within 10 km/s of zero.
  The required inflow exceeds the flow's by a factor of 10 to several hundred.
- **Surface supply rate** (the charge a reservoir at R_3 would have to supply, per Gyr, in units of C_law(R_3)): 0.05 at
  z 0, 0.41 to 0.47 at z 2.2, 0.68 to 0.92 at z 3.0, 2.1 to 3.9 at z 4.4.

### 2b. S-cos (A* = 11.3; law-off confirm 59.32 M_b turned around against 59.49, -0.3 %)

| log M_b | can z 0 | 2.2 | 3.0 | 4.4 | alt z 0 | 2.2 | 3.0 | 4.4 |
|---|---|---|---|---|---|---|---|---|
| 9 (D_3) | 0.0443 | 0.0273 | 0.0240 | 0.0195 | 0.0402 | 0.0246 | 0.0216 | 0.0173 |
| 10.45 | 0.0782 | 0.0481 | 0.0436 | 0.0376 | 0.0709 | 0.0438 | 0.0391 | 0.0335 |
| 11.5 | 0.1208 | 0.0764 | 0.0691 | 0.0634 | 0.1093 | 0.0695 | 0.0624 | 0.0565 |

- **With the law on, the same seeded patch turns around 2.0 M_b, not 59.3.** In FLD1's shell equation the clock's own
  charge excess does not bind itself: the shell force is -g_N - y + U(y) and U(y) - y = y^2/(a0 - y) > 0, a second-order
  outward push. Only the baryons' g_N pulls the clock in. A cosmological overdensity of the clock therefore roughly
  doubles the delivered charge (S-cos / S-seed = 1.6 to 1.8) and no more.
- Reported, law off (Newtonian dust in the same device): D_3 at z 0 = 0.14 / 0.24 / 0.35 (log M_b 9 / 10.45 / 11.5);
  the history max of D_3 reaches 0.90 / 1.60 / 2.50; an equal-charge radius exists only at 11.5 (1.02 R_fold).

### 2c. S-ref (D_k = s; the reference's cold mass at R_k over the law's)

| log M_b | can z 0 | 2.2 | 3.0 | 4.4 | alt z 0 | 2.2 | 3.0 | 4.4 |
|---|---|---|---|---|---|---|---|---|
| 8 (D_3) | 0.533 | 0.811 | 0.828 | 0.705 | 0.485 | 0.734 | 0.747 | 0.628 |
| 9 | 0.721 | 1.084 | 1.121 | 1.048 | 0.655 | 0.979 | 1.008 | 0.930 |
| 9.4 | 0.813 | 1.218 | 1.263 | n/a | 0.738 | 1.098 | 1.133 | 1.062 |
| 10 | 0.974 | 1.455 | n/a | n/a | 0.883 | 1.309 | 1.358 | n/a |
| 10.45 | 1.114 | 1.668 | n/a | n/a | 1.010 | 1.497 | n/a | n/a |
| 10.7 | 1.201 | n/a | n/a | n/a | 1.088 | 1.615 | n/a | n/a |
| 10.9 | 1.275 | n/a | n/a | n/a | 1.154 | n/a | n/a | n/a |
| 11.2 | 1.395 | n/a | n/a | n/a | 1.262 | n/a | n/a | n/a |
| 11.5 | 1.413 | n/a | n/a | n/a | 1.344 | n/a | n/a | n/a |

n/a: no settled halo (v_vir above v*(z)) carries that M_b at that z; 17 / 14 of 36 cells. N_in / N_out at R_3 = 0.51
to 2.57, so the advective condition asks for inflow or outflow of only -1 to +5 km/s with S-seed's Rdot. R_eq (outermost
crossing of C_R and C_B inside 0.999 r_ta, A1): none below log M_b 10.45 at z 0 and 0.59 to 2.05 R_fold above; at z 2.2
to 4.4, 1.4 to 16 R_fold where the reference is over (the forest halo's own r_ta lies far beyond the seed's fold at high
z). D against the pure phantom (no linear remainder) equals D to the printed digits at z 0.

### 2d. Part 1

- **P1a (KA1, PASS):** sympy: the balance -g_N - y + U(y) = 0 has the single root y = [sqrt(g_N (g_N + 4 a0)) - g_N]/2,
  and g = g_N + y gives g^2/(a0 + g) - g_N = 0 exactly; converse residual 0. Numeric: 1.9e-13 on the law and 2.2e-13
  on m_balance / FLD1's Mph (line 1e-12). So the static balance of FLD1's equation is the law, and the enclosed charge
  excess at rest is the law's phantom mass.
- **P1b (KA2, PASS):** the delta(F) coefficient of d_t(r^2 J^t) + d_r(r^2 J^r) is r^2([J^r] - Rdot [J^t]) (residual 0);
  the advective reduction and v_out = Rdot (1 - N_in/N_out) follow; the junction note's rational example reproduces
  (t = 2/3, N_in/N_out = 3/2; (2, -1) satisfies; (0, -1) leaves -2/3). Integrated: d/dt C_in(R(t)) = 4 pi R^2 N_in Rdot =
  the charge carried across the moving boundary, so D_k = 1 is the no-reservoir condition in integrated form.
- **P1c, the non-advective term (log M_b 10.7 and 10.825, z 0, k = 1, 2, 3):** eps = |c lambda P| / |N v| is 1.8e-6 to
  4.7e-6 outside (its v.grad Phi part 4.9e-7 to 1.9e-6; the rest is d_t Phi bracketed by g R / t_age) and 6.8e-7 to
  8.8e-7 on the law's side; (v_c/c)^2 = gR/c^2 = 2.9e-7 to 3.7e-7. Against the flux the advective condition lacks,
  the channel supplies 4.8e-7 to 1.3e-6 of it. The independent SI evaluation agrees to 8e-16. The lead's estimate (order
  Phi/c^2, about 1e-6) holds. The lambda_0 piece depends on Phi and its first derivative, continuous across a layer
  with no sheet, so it does not grow as the layer narrows; the gamma_L piece grows as 1/w but is 4e-14 / 4e-13 / 4e-10 to
  9e-14 / 9e-13 / 9e-10 at w = 10 kpc / 1 kpc / 1 pc. A layer would have to be thinner than about 1e-3 pc for that piece
  to reach 1e-6, and about 1e-9 pc to reach order one.
- KA6 (PASS): C_law(100 kpc, log M_b 10.7) in SI 5.5552e11 against FLD1's units 5.5559e11 M_sun (1.3e-4).

## 3. Known answers and twins

| item | result |
|---|---|
| KA1 static balance = the law | PASS (above) |
| KA2 interface condition, rational example | PASS |
| KA3 18 S-seed runs: FLD1's five columns and XJ1's R_1..R_3 | PASS, worst deviation 0 |
| KA4 FLD1's "1.6 to 5.1 %" (A4 grid, 8 rows x 4 radii; FLD1's reads_end and this lane's own count) | PASS, worst 6.7e-16; range 1.63 to 5.14 % |
| KA5 XJ1's s range, Ec2 and Ec3, z 2.2 / 3.0 / 4.4, both footings, via XJ1's exact_fn and via own C_R / C_B | PASS, worst 4.4e-16 |
| KA6 units in SI | PASS |
| KA7 S-cos insertion inert at A = 0 (after A2: NaN positions matched) | PASS, deviation 0 (as frozen it printed nan -> FAIL; A2) |
| TW1 U(y) with the cap's sign flipped | BITES (KA1 deviations 5e5, 3e3) |
| TW2 Rdot sign flipped in the condition | BITES (residual 2 r^2 [J^t] Rdot; the example fails) |
| TW3 charge counted by Lagrangian radius | BITES (KA4 deviation 1.0) |
| TW4 R_2 where R_3 is asked (S-ref) | BITES (KA5 fails, 7 lines, worst 0.11) |
| TW5 law off in S-seed, log M_b 10.45 canonical | BITES (D_3 at z 0 0.0444 -> 0.0510, +14.8 %) |

## 4. Hand estimate against result

- S-seed D_3 at z 0 about 0.03 to 0.08: result 0.016 to 0.068 (the low end was too high at log M_b 8 and 9). SHORT at
  every k on both footings (95 %): yes. Mass slope about M_b^{1/6}: yes (0.17). N_in/N_out 10 to 50: result 27 to 173,
  higher. Required inflow > 3x the flow's own (70 %): yes, by 10 to several hundred. R_eq none or < 0.05 R_fold (70 %):
  none at all.
- S-ref DEPENDS ON MASS at k = 3 (75 %): yes; crossing near 10.7 to 11.2 at z 0: no, 10.09 / 10.42 (XJ1's statement was
  at f >= 1.25 R_fold on SRH1's lens profile, not at R_3).
- S-cos law on, within a factor 3 of S-seed and SHORT (85 %): yes (x1.6 to 1.8). Law off D 0.5 to 2 (60 %): no at the
  graded z (0.02 to 0.35); only the history max reaches 0.9 to 2.5. Tuned A about 7 (60 %): no, 11.3 (the first three
  tuning points did not bracket the target).
- eps 1e-7 to 1e-6, width-independent; gamma_L piece < 1e-9 at w >= 1 pc (80 %): eps is 1.8e-6 to 4.7e-6 outside
  (slightly above the range), 7e-7 to 9e-7 on the law's side; gamma_L piece 4e-10 to 9e-10 at 1 pc: yes. Cannot supply
  an O(1) shortfall (90 %): yes.

## 5. What counts against (whatever the labels)

- **The device behind the fold.** R_2, R_3 and every number inside R_fold come from FLD1's independent-shell equation
  continued past crossing (each shell keeps its Lagrangian enclosed charge) and its reflecting centre. The action gives
  no answer there (COL1). A self-consistent multistream solution could move D; by how much is not computed. The SHORT
  word does not depend on k, and D_half and D_1 agree with D_3 to 35 %, so it is not a caustic-selection artefact.
- **Spherical, one seed, no mergers.** S-cos is one point-seed tail with one amplitude; real peaks, filaments and
  mergers are absent. S-cos's law-off turned-around charge is mass-independent by construction (the seed scales with
  M_b).
- **The law-dominated limit (mu_K = 0).** The self-repulsion of the clock's excess (U(y) - y > 0) is a property of this
  limit of the shell equation; at the CMB-side constants or on scales where mu_K r is not small the clock is dust
  (FLD1, COL1 Part 0), and this lane does not apply there.
- **S-ref is not a flow.** Its D says only how far the reference layout sits from the law at R_k; it has no velocity
  field, and its v_req uses S-seed's front speed. Its n/a cells (17 / 14 of 36) remove every mass above log M_b 10.45 at
  z 2.2 and above 9 to 9.4 at z 4.4.
- **One-sided densities at a caustic** are bin averages of a formally singular density; the w brackets move N_in/N_out
  by up to about 30 % and v_out is a net over streams.
- **P1c** uses the weak-field forms, P = m/(4 pi R^2) and the D Phi/Dt bracket; no field solve. It bounds QX17's
  lambda P/Q channel only; it says nothing about other non-advective physics (dissipation, pressure, a surface
  reservoir), which SET1, EDG1, AKS1, VSH1 and VSJ1 examined.
- A2 is post hoc (KA7's NaN handling, read after the first grader output). The S-cos label rests on it; the S-cos
  numbers are the same either way.

## 6. What was not done

- No multistream (self-consistent enclosed-charge) solve behind the fold; no full QX17 interface solve with P and
  lambda; no merger or 3D supply; no run at mu_K > 0. No forest box, nothing downloaded.

## 7. Errors or doubts in the files this lane was pointed at

1. **FLD1's shell equation cannot gather a cosmological share of clock charge by itself** (section 2b): with the law
   on, the clock's excess pushes itself outward at second order, and a patch tuned to turn around 59.3 M_b as dust turns
   around 2.0 M_b. Form B's cosmology needs the cold component to cluster as dust; in this limit of the equation it does
   not. This is not stated in FLD1's or COL1's results as far as this lane read them.
2. **XJ1's "s passes 1 near log M_b 10.7 to 11.2"** is a statement at f >= 1.25 R_fold on the lens profile; at R_3 the
   crossing is at log M_b 10.09 / 10.42 at z 0 and 8.6 to 9.2 at z 2.2 to 4.4. Not an error, but the two should not be
   quoted for each other.
3. **The junction note** is consistent with what was re-derived here (P1b, KA2). Its open item ("a tracked-halo
   velocity / front-speed history ... still needed") is answered for S-seed and S-cos: the advective condition fails by
   a factor 10 to several hundred in the required inflow, and the non-advective channel supplies about 1e-6 of the gap.
4. **This lane's own frozen file** had a degenerate S-ref equal-charge definition (A1) and a KA7 that could not pass on
   NaN columns (A2).

## 8. Files and commits

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `AMENDMENT_A2.md`; `csd1_shells.py` -> `runs/*.json`; `csd1_part1.py` ->
`csd1_part1.*`, `csd1_part1_MUTATE.*`; `csd1_tune.py` -> `csd1_tune.*`; `csd1_ref.py` -> `csd1_ref.*`,
`csd1_ref_MUTATE.*`; `csd1_grade.py` -> `csd1_grade.*`, `csd1_grade_MUTATE.*`; `run_csd1.sh` (its `logs/*.log` are git-ignored; every graded line is in the `.out` files). Resources: 45
shell runs, single thread, nice 19, under 0.1 GB each, 10 s to 5 min each; total about 25 minutes wall.

| commit | local |
|---|---|
| criteria, alone | 127a25a942 |
| A1, alone | 6e2d39d50d |
| scripts, before any run | c7b3195af1 |
| A2, alone (post hoc) | 689e3a5513 |
| grader KA7 fix, before re-run | af929db57f |
| runs, outputs, RESULT.md | the commit that adds this file |

## Dated note by the lead, 2026-11-14, 16:19 EST: Lean certificate

On the owner's instruction the lead added `CSD1.lean` for the lane's exact items. It certifies algebra, not physics,
and no number or label: the static balance of the shell equation is the law (`shell_push_cross`, `balance_is_law`);
the clock's own excess pushes outward at second order (`self_push`, `self_push_pos`); the advective interface
condition and its two signs (`advective_junction`, `outflow_needed`, `inflow_allowed`). `compile.txt` ends "exit 0"
with no error (two deprecation warnings). The twin `CSD1_MUTATE.lean` states four false variants; `compile_MUTATE.txt`
ends "exit 1" with one error per theorem. Nothing else in this file is changed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
