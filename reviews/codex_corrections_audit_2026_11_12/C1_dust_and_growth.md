# C1 audit: the dust term's clustering threshold and the growth gate (2026-11-12)

Slice: the uncommitted forward notices in MK1, KD1, fable52_push CLOSURE.md / README.md (MK1 and growth parts only),
FINAL4, and the changed committed output qx17c.json. Cited evidence (untracked, read only):
research_closure_2026_11_12/closure_push_02/ (RESULT.md, CORRECTIONS.md, growth_gate_audit/).
Read only on every file except this one. Checks were run on copies in the session scratchpad.

## Verdict table

| item | grade | one line |
|---|---|---|
| MK1 notice: factor mu_K^2/(mu_K^2+k_phys^2), not 1-k_phys^2/mu_K^2 | CORRECT WITH LIMITS | My own derivation from action (A) gives the same equation. It holds only while the clock's gradient stays well below a0 (W quadratic) and gamma_L k^2 is small. The notice does not state the a0 condition. |
| MK1 notice: "archived number cannot be transferred unchanged" | CORRECT, OVERSTATED IN EFFECT | Formally true. In numbers, near 2.5e4 per Mpc the two factors agree to first order: growth ratios differ by < 1 % (z 1090 start). The line moves by about 0.2 to 40 % depending on scale and start, not by orders of magnitude. CP02's word "withdrawn" overstates. |
| MK1's label NO VALUE / NO VALUE | UNCHANGED | Row 1 (198 per Mpc, background, P = 0) is untouched, and row 3 (X-COP) is empty. The label never needed row 2. |
| KD1 notice | CORRECT WITH LIMITS | Same physics as MK1's notice. B1b numbers reproduced independently. Pure addition. |
| CLOSURE.md, first notice (MK1 / growth part) | CORRECT WITH LIMITS | The growth sentence is right. Its first sentence (a "scoped physical instability counterexample") is outside this slice: NOT CHECKED. |
| CLOSURE.md second notice, README.md notice | not in slice | They cover only PIK1 and FRM1 (another auditor). Neither mentions MK1 or growth. |
| growth_gate_audit table (power ratios) | CORRECT (reproduced independently) | My own ODE code reproduces all 15 entries to 6 digits. |
| growth_gate_audit BBN ratio | CORRECT (reproduced independently) | 1.3472385e8 at 198.254, 8392.46 at 25118.86, mu_BBN 8.8901135e6 per Mpc. |
| FINAL4 notice | CORRECT | Each of its four statements checks against FINAL4's own text and table. It has typos ("ratio.87978", "means12.02%", "later3.6%"). |
| qx17c.json (4 lines) | HARMLESS, but an overwritten output | Only four "seconds" timing fields change (0.3->0.4, 0.6->0.8, 0.3->0.4, 0.7->0.6). No result number changes. Per the coordinator it is an older (11-07) leftover, not part of the 11-12 notices. It plays no part in the growth question. |
| claims of a pass / rescue / complete theory (question c) | NONE in slice | CP02 claims negative results only. It says outright that no replacement likelihood or CMB verdict is produced. Its new negative claims (instability, 450 per Mpc pressure bound) are outside this slice and are not re-graded here. |
| rule breaches | minor wording | MK1's notice says "cold dark self-gravity factor". It should say "cold dark energy's". No "cold dark matter", no kappa / 5.41 derivation claim, no home paths. |

All four slice notices are pure additions at the top of the file (checked with `git diff`). No committed line was deleted
or rewritten, and no label moved.

## Decisive checks

### (a) The linear growth equation, derived independently

Action (A) (QX17 RESULT section 0), weak field, gamma_L = 0, c = 1, K = 4 pi G. Write tau = t + sigma and v = -grad_X sigma / a.
Then

    x = Q - 1 = sigma_dot - Phi - |grad_X sigma|^2/(2a^2),   A_i = -d_i x / a  (leaf gradient of ln Q).

For K|P| << a0, W(K|P|) = (a0^2/K)[-p/a0 - ln(1 - p/a0)] = K|P|^2/2 + O(|P|^3). The non-GR Lagrangian is then

    L = mu^2 x^2/(2K) + P.A - K|P|^2/2 = mu^2 x^2/(2K) + x Pi - K|P|^2/2   (integrating by parts, Pi = div_X P / a).

- Vary P: K P = -grad_X x / a, so Pi = -Laplacian_X x / (K a^2).
- Vary sigma: the charge n = dL/dx = mu^2 x/K + Pi is conserved, d_t(a^3 n) + a^2 div_X(n v) = 0. This matches QX17 (E3)
  at leading order.
- Gradient of the sigma_dot relation: v_dot + H v = -grad_X(Phi + x)/a.
- QX17 (K5): the Poisson source is n, so Laplacian Phi / a^2 = K(rho_b delta_b + nbar delta_d).

In Fourier space, delta n = (mu^2 + k_phys^2) delta x / K. Linear continuity and Euler then give

    delta_d'' + 2H delta_d' = K rho_b delta_b + K nbar delta_d - k_phys^2 delta x
                            = K rho_b delta_b + K nbar [mu^2/(mu^2 + k_phys^2)] delta_d .

Drop P (polarization off) and n = mu^2 x / K instead, which gives the n = 1 polytrope factor 1 - k_phys^2/mu^2. Baryons feel
the full source and no x force. This is identical to the audit's equations (1) to (3).

**Which factor is right, and where.** Linearizing W about P = 0 needs the clock-gradient acceleration |grad x| to stay well
below a0. When the total gradient field |A| reaches or exceeds a0, K|P| saturates near a0. A perturbation's
polarization response then drops by a factor M of about a0/(a0 + |A|): (a0/(a0+|A|))^2 along A and a0/(a0+|A|)
across it. Repeating the elimination with K delta P = -M grad delta x / a gives the self-gravity factor

    [mu^2 - (1 - M) k_phys^2] / [mu^2 + M k_phys^2],

which equals the corrected factor at M = 1 and the old polytrope factor at M = 0. My per-mode estimate in SI (script
`mine.py`; delta_d taken from typical linear amplitudes): at mu = 198 per Mpc and z = 1090, |grad delta x| is about 2 to 5 a0
for k = 0.1 to 1 per Mpc with delta = 3e-3, and about a0 for realistic amplitudes. It is 0.005 to 0.04 a0 at z = 100.
At mu = 2.5e4 it is below 0.005 a0 throughout.

- The corrected factor is right for low mu_K after about z of a few hundred.
- At mu_K near 2.5e4 it holds throughout, but there the two factors agree anyway.
- Near recombination at low mu_K, the a0 nonlinearity of W cannot be dropped. Growth there is amplitude-dependent and lies
  between the two factors.

The audit's own limits do not mention this condition (its derivation says only "near P = 0"). The stiffness term is a
smaller correction: gamma_L k_phys^2 / K = Lstar^2 k_phys^2 / 2 is about 0.03 at k = 10 per Mpc and z = 1090, and only on the Pi > 0 side.

### (b) MK1's rows, and the lensing-shape line under the corrected factor

- **Row 1 (198.25 / 198.24 per Mpc)** is the homogeneous w(z 3400) <= 0.01 line with P = Pi = 0. The correction cannot touch it.
- **Row 2 (2.51e4)** is the only row affected.
- **The label** does not move. Row 1 alone sits a factor 198 / 259 above KiDS's 1.00 / 0.77, and row 3 (X-COP) is empty on
  both footings. MK1's own text says so ("Without the CMB rows there would still be no value").

**Does the cited audit compute the corrected lensing requirement?** No. `classy` is absent, and the audit says plainly
that it runs no PR4 likelihood. So there is no corrected number to reproduce. I estimated the shift myself (script
`shift.py`). I found the mu_K at which the corrected operator gives the same growth suppression at z = 3 as the
polytrope operator at 25118.86, using the same equal-data Meszaros start:

| start | k = 3h (2.02) | k = 20/3 | k = 2 pi h / 0.42 (10.08) per Mpc |
|---|---|---|---|
| z 1090 | 25071 (-0.2 %) | 24603 (-2.1 %) | 23942 (-4.7 %) |
| z 3400 (rough: equations not built for radiation era) | 24668 (-1.8 %) | 20394 (-19 %) | 14978 (-40 %) |

So on MK1's scales the corrected line plausibly sits between about 1.5e4 and 2.5e4 per Mpc. This is not a likelihood.
The binding gap against KiDS stays at more than four orders of magnitude.

**Growth table.** My independent code (`mine.py`: its own DOP853 integration, the same background parameters, the
Meszaros initial slope) gives 0.839708 0.226380 0.122690 0.045857 0.033641 (mu 198, z 1090), 0.998022 0.906806 0.732492
0.327836 0.234619 (mu 198, z 100) and 0.999987 0.999263 0.996999 0.968908 0.933199 (mu 25118.86). All match the audit.
The polytrope operator at 25118.86 gives 0.999987 0.999263 0.996988 0.967659 0.927258, under 1 % from the corrected one.

**BBN.** By my own formula (KD1 B1b convention), the stiff-to-radiation ratio is 1.34723849e8 at 198.254 and 8392.4626
at 25118.864, and mu_BBN = 8.8901135e6 per Mpc. The audit's numbers match to about 1e-9 (k_B digits). This is the
historical 0.067 criterion, as the notice says, not a fresh BBN likelihood.

### (c) Does closure_push_02 claim more than a correction?

No pass, no rescue and no completed theory. CP02's headline is negative: the QX17/PIK1 density-gated implementation "is not
a closed, healthy theory". It also says "the original broad goal of a healthy predictive theory remains open". Two
over-strong phrases:

- "The 25120/Mpc likelihood threshold is withdrawn for the coupled theory" (CORRECTIONS.md). "Not validated; expected of
  the same order" is what the numbers support.
- "This uses the corrected equations ... not the old growth threshold" (RESULT.md). True, but its joint obstruction rests
  on the BBN proxy and a static pressure bound (about 450 per Mpc), which are outside this slice and not checked here.

CP02 says kappa stays fitted.

### FINAL4 notice, point by point

- "delta_b = delta_c = D exact only after dropping baryon pressure/drag." FINAL4 (R1) carries R_T and c_b^2, and (R2) does
  not. So with R1 as printed, the equality is not exact. CORRECT.
- "D1 has no explicit k factor; D2 does." D1's coefficient is (1 - psi(a)), with no k. FINAL4 line 71 says both carry k. CORRECT.
- "R_set = R_fold, psi and the NFW redistribution are modeling assumptions." FINAL4 says "No free number anywhere", but
  line 221 admits the step from falling dust to the settled halo is missing. CORRECT.
- "0.87978 at z = 0.295 is 12.02 % suppression, against the 3.6 % prose." 1 - 0.87978 = 0.12022. The "14.1 % today" figure
  matches 1 - 0.85853. The 3.6 % figure matches no ratio in the table (z 3 gives 3.8 %). CORRECT.

FINAL4's Delta chi^2 labels are untouched.

An observation, not graded: FINAL4 treats falling charge as P = 0 and pressureless. If the quadratic K(Q) with the QX17
constraint governs that charge, the linear derivation above says falling charge already loses self-gravity by
mu^2/(mu^2 + k_phys^2). That is a consistency question for the formation reading, owed to its own lane.

## PAPER72 recommendations

**Open item 3 (MK1 threshold), replacing the pending sentence once the notice is committed:**
"The CMB needs mu_K of at least 198 per Mpc for the component to be cold by z = 3400 (a background line, unaffected by
the 2026-11-12 correction). The 2.51e4 per Mpc lensing-shape line was imported from a calculation with the polarization
response switched off. With it on, and while the clock's gradient stays well below a0, the cold dark energy's
self-gravity factor is mu_K^2/(mu_K^2 + k_phys^2), not 1 - k_phys^2/mu_K^2. No replacement lensing likelihood has been run;
near 2.5e4 per Mpc the two factors agree to first order, so the line is expected to stay of order 1e4. MK1's NO VALUE does
not rest on it: the 198 line alone is 198 / 259 times above KiDS, and X-COP allows no value."

If the notice is not committed, keep the committed wording. It is the lane's record.

**Section 8.1 (FINAL4), once committed:** keep the label sentence and add:
"Its forward notice records that the 'derived' history rests on modelling choices its two equations do not derive (the
settled radius equal to the fold radius, the settled fraction psi, the NFW redistribution), and that its table's growth
ratio 0.880 at z = 0.295 is a 12.0 % suppression, not the 3.6 % its prose states. Neither changes its Delta chi^2 labels."

## Not checked

- The CP02 instability, gate-family lemma, compression run, static pressure bound (about 450 per Mpc) and joint obstruction
  (CLOSURE.md's first sentence, CP02's headline).
- The CLOSURE.md and README.md text on PIK1 and FRM1 (another auditor).
- No PR4 / CLASS likelihood exists for the corrected factor, so the true corrected lensing line is unknown. My shift
  estimate matches growth suppression at single k, not the lensing statistic.
- A nonlinear-W (a0-saturated) growth run near recombination. Its size is estimated per mode only.
- growth_derivation/ and health_audit/ beyond the CORRECTIONS cross-references.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
