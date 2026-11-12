# SS2 (virial-gated late conversion, the outside source's variant G): FROZEN CRITERIA, committed alone before any SS2 script or number

TEST lane, quarantined. Registered RUNNING by the orchestrator. Adopts nothing. No particle is adopted: the component is the
record's test object. kappa = 1/2 FITTED; not theory closed. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10),
graded separately, never pooled.

**Not blind, stated first.** SS1 already graded this construction as its variant G under SS1 AMENDMENT_A2 (2b866ef57a). That
result is at f3186ce8e7: FAIL / FAIL at groups, with X-COP, growth and the Bullet also failing; KiDS, SPARC, UMa and Cassini
pass. SS2 is frozen with those numbers known. SS2's labels therefore carry weight only where SS2 adds something, and every
SS2 number that repeats an SS1 G number is reported as a replay.

What SS2 adds:
- a validated CMB-lensing gate (section 4);
- the source-constant bracket;
- the per-group, per-bin amount table and TR1's falling fraction;
- the separation bounds at alpha 4.39 in Lean.

## 1. Construction G, frozen once (as relayed)

- **Onset:** z_dec where q = 0: 1 + z_dec = (2 Omega_DE / Omega_m)^(1/3).
- **Rate:** Gamma0 = 4 pi H0 sqrt(Omega_DE). alpha = Gamma0 t_dec, where t_dec is the time from z_dec to 0.
- **Product:** a non-relativistic daughter, mass kept (loss <= 2e-4), kicked at 4 v_stiff. The background is unchanged,
  with a bare Lambda and a0 fixed.
- **v_stiff = (a0 c L*)^(1/3).**
- **Gate,** on the pre-conversion dark halo only:
  - x0 = 3 max(0, (v_vir / v_stiff)^2 - 1), with v_vir = sqrt(G M500_pre / R500_pre);
  - x0 = 0 if Delta < 500;
  - members take max(x_own, x_host);
  - retention f is the root of -ln f + x0^4/4 (1 - f^4) = alpha;
  - one global x0 per halo, uniform retention over the whole pre-conversion component.
- **Conversion** (two-body) happens only inside collapsed halos: Press-Schechter collapsed fraction at z_dec above 1e6 Msun,
  with M_min = 1e10 as a bracket. The uncollapsed web stays cold. The daughter is unbound and leaves its system.
- **Constants:** the PRIMARY reading uses each footing's own values, as SS1 A2 did:
  - a0 as above, L* 21.68 / 22.85 pc, Omega's from QX15 main theta + F1A R;
  - this gives z_dec 0.631, alpha 4.367 / 4.366, v_stiff 265.8 / 288.1 km/s.

  **Bracket G-source:** the source's own constants (z_dec 0.642, alpha 4.39, v_stiff 286 km/s), full table and label
  printed, never grades.
- **Form choices** recorded beside the label: the cube root, the kick factor 4, 4 pi, the factor 3. Fitted constants: 0.
- **Bracket G-local:** v_loc(r) = v_vir (1 + (r / 0.35 R500)^2)^(-1/4) per shell, plus the 18 % expansion. Named added
  assumptions, never grades; a local dispersion gate is close to the dead keys HX1 / SK1.

## 2. Pre-conversion halos

As SS1:
- primary: KD1 P3 capture (f_cap 0.76 R M_b), SIS truncated at R200 at z_dec;
- brackets: Duffy 2008 NFW; Moster 2013 abundance matching for galaxy-scale systems; observed M500 for groups and X-COP
  (Lovisari table, X-COP R500).

Labels are printed under every bracket.

## 3. Gates and lines

SS1's gates and lines, in this order:
1. KiDS, 59 points, |shift| <= 0.05.
2. Groups: >= 16/20 at f* 0 and f* 1.
3. X-COP: |mean| <= 0.05, rms <= 0.10, every graded bin within 0.10.
4. Coma UDGs: reported (UA1).
5. SPARC + the F2 allowance.
5b. Ursa Major (EV1 W1): |Delta_pred + 0.024| <= 0.128.
6. Background: BAO + SN Delta chi^2 <= 4. The mass is kept, so this verifies SS1's BAO failure is gone.
7. (a) Primary peaks unchanged (verification). (b) CMB lensing, chi^2 <= 18.48: graded only if the validation in section 4
   passes, otherwise NO VERDICT.
8. Forest (NC2 band) + fsigma8 (CE2 rule). sigma8 / S8 reported beside KiDS-1000 S8 0.759.
9. Bullet (DB1 label).
10. Cassini.

Reported beside the gates (no new lines):
- **Per group and per radial point:** the retained component's residual, i.e. the AMOUNT question. Full retention gives
  4.1 M_b against KD1's uniform need of 3.46 (f* 0) and 1.23 (f* 1).
- **X-COP:** retained over dynamical mass per TR1 bin, beside TR1's 0.71, 0.66, 0.58, 0.46, 0.32.
- **Converted share of cosmic matter:** today's value, beside the source's 22 %.
- **KiDS 2-halo:** NOT EVALUABLE on the record's lensing machinery (KX1's two-halo term is about 1 % inside 300 kpc; no
  outer two-halo model on disk). Reported as such.

**Label.** PASS on a footing iff gates 1, 2, 3, 5, 5b, 6, 7(b), 8, 9 and 10 all pass. Otherwise FAIL, naming the first
failing gate, with the full table. If 7(b) is NO VERDICT and every other gate passes, the label is NO VERDICT.

## 4. CMB-lensing validation (new; decides whether 7(b) is graded)

CLASS cannot switch a conversion on at z_dec. The lane's method (the record's two-fluid growth ODE with a k-dependent
non-clustering fraction, GL1 / BG1 limber4 on the reference background, applied as a ratio to CLASS's baseline lensing) is
validated where CLASS can run the same physics:
- **CLASS run:** 20 % of the cold component carried from the start as a smooth matter fluid (w 0, c_s^2 1, use_ppf no; the
  background is identical because w = 0).
- **Method:** fc = 0.20 at every k and every a.
- **PASS** iff |chi^2_method - chi^2_CLASS| <= 0.15 |chi^2_CLASS - baseline| on both footings (A_s refit, the record's PR4
  machinery).

If it passes, 7(b) is graded on the method with G's time-gated fc(k, a). If it fails, 7(b) is NO VERDICT and the reading is
reported.

## 5. Known answers

- **K0:** the closed form against a numerical ODE integration, to 1e-6.
- **K-G** (the orchestrator's table, z 0.05, 500 rho_c, v_stiff 286, alpha 4.39): v_vir to 1 %, f to 0.005 at M500 3e12,
  5e12, 7e12, 1e13, 1.35e13, 2e13, 3e13. Known from SS1: the 1e13 point (on the threshold) misses, 0.148 vs 0.161. It is
  printed, not stopping.
- **Lovisari:** every group retains >= 0.992 on its table M500 / R500 (SS1: min 0.9919, printed).
- **x_crit = ((64/15)(alpha - ln 2))^(1/4)** at alpha 4.39 (1.993) and at the footing alpha.
- **Law-only replay** (component -> 0): the record's numbers on gates 1-5 to 1e-6.
- **Bullet:** the law alone gives DB1 K1. Background: Gamma0 -> 0 gives the reference.
- **Consistency:** SS2's G numbers equal SS1's G numbers (f3186ce8e7) wherever the same machinery runs.

## 6. MUTATE (must bite)

- **M1, M2:** v_stiff x 1.25 and / 1.25. Bites iff a gate status or the label changes; otherwise NO BITE, disclosed. SS1
  found NO BITE.
- **M3:** alpha -> 0. KiDS or SPARC must FAIL.
- **M4:** x0 = 0 everywhere. Groups and X-COP must FAIL.
- **M5 (new, for the lensing gate):** onset at z 2 (alpha scaled by the longer t_dec). 7(b) must read worse than the main
  run.

## 7. Frozen prediction (recorded whatever the label)

- **The prediction:** isolated M* 10^11 lens Delta Sigma excess over the bare law at 0.3 Mpc of +0.245 / +0.205 / +0.078 /
  +0.020 dex for z_lens 0.8 / 0.6 / 0.4 / 0.2.
- **Grading:** graded on any lens-redshift split on disk. SS1 found none (the KiDS-bright catalogue has redshifts, no shear
  profiles), so it is expected to be recorded only.
- **The lane's own version:** the lane also computes the excess for that lens on its primary and Moster halos at those
  redshifts (retention at the lens epoch from the closed form at tau(z_lens)).

## 8. Lean (`ss2_lean/SS2.lean`)

Compiled with `lake env lean` from the record's Lean tree; a MUTATE must fail.
- The closed form solves dy/dtau = -y/(1 + (x0 y)^4).
- x_crit identity.
- Monotonicity.
- Separation bounds at alpha 4.39 (recomputed): x0 <= 0.65 -> f < 0.0137; x0 >= 2.4 -> f > 0.83; x0 >= 3 -> f > 0.94.
  A bound that cannot be proved is left as a statement, disclosed.

## 9. Hand estimates (from SS1's G, so they are expectations, not blind)

- FAIL at groups (full retention over-fills).
- X-COP over-filled.
- Growth FAILS (40-60 % of the component converts and streams 6-7 Mpc).
- BAO PASSES (mass kept).
- Bullet FAILS on DB1's offset rule.
- The lensing validation: unknown.
- G-source: same pattern.

## 10. Operational

- **Scripts and machinery.** `ss2.py` reuses SS1's ss1v.py / ss1.py / ss1_cosmo.py / ss1_bullet.py read-only, with outputs
  redirected to this lane's parts/.
- **Limits.** One thread, RSS < 1 GB except CLASS and the DB1 child; preemptible; df check.
- **Commits.** Explicit-path commits; push via a sparse temporary worktree.
- **Outputs.** ss2.json / .out, ss2_MUTATE.json / .out, RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
