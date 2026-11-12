# PIK2 RESULT: the gated dust term graded. CMB-ONLY / CMB-ONLY (canonical / alt), blind label unchanged

**Blind label (from `RESULT_BLIND.md`, commit 6652b8a845, unchanged): CMB-ONLY / CMB-ONLY** at mu_K = 2.512e4 per Mpc
(primary), and the same at 198.25 and, reported, at 8.89e6 per Mpc.
- No (S, xi) opens a window on either footing, so there is no hit.
- X-COP passes for no gate, at no threshold, at no mu_K. The best rms is 0.39 against the 0.10 line.
- Where a gate gives the groups their dust, the gated term is unhealthy on that background by 1e13 to 1e18. That is
  row 8b, at fixed metric.
- The galaxy rows pass only for F2, F3 and the step, and only at thresholds that shut the gate at every graded radius.
- The gate is VISIBLE at linear order about FRW iff S'(0) or S''(0) is non-zero. The gates with S''(0) > 0 fail linear
  health at every threshold at 2.512e4 and at 198.

All known answers pass and every mutation bites. Criteria 95edd35e0b, scripts and runs ccc4f4fc92, blind result
6652b8a845. TEST lane: adopts nothing, relabels nothing (PIK1's committed label is not touched), registers nothing.

## What was opened after the blind result was committed

After 6652b8a845 I opened:
- PIK1's `RESULT.md` at HEAD, with its two forward notices;
- `reviews/codex_corrections_audit_2026_11_12/C1_dust_and_growth.md` and `C2_pik1_and_frm1.md`;
- `research_closure_2026_11_12/closure_push_02/RESULT.md` and `CORRECTIONS.md` (untracked, read only).

I did not open CP02's sub-reports (coupled_health, health_audit, static_gate, joint_obstruction, growth_gate_audit).
Nothing below changes the blind label.

## COMPARISON (only what this lane computed; the rest is marked "not computed here")

### (i) Linear visibility

**Agree with C2 and CP02, disagree with PIK1 section 4.**
- **The quadratic action.** PIK1 dropped the dQ dPi term as "second order". That term is in the second-order action,
  which is what sets the linear equations. My certified quadratic action (C0a, exact torus integral in unitary gauge, 3D)
  is
  `Int a^3 [ -(s1/Pi_c)(F/Q)'(Qbar) P.grad dQ + (s2/2 Pi_c^2)(F/Q)(Qbar)(div P)^2 ]`,
  with S''' and higher absent. It is the same structure as C2's B alpha div P + (D/2)(div P)^2 (B from S'(0), D from S''(0)).
- **Invisibility** holds iff S'(0) = S''(0) = 0, as C2 states.
- **Strength.** My e1 = s1 (1+z)^3/xi equals C2's B = 1/(xi a^3) for E1.
- **The unhealthy wavenumber.** My k_* = mu sqrt(2/s2) xi/(1+z)^3 equals C2's k_*^2 = 2 xi^2 mu^2 a^6 for E1.
  - I went further than C2's point estimate: a grid of 281 thresholds, z 0 to 3400, both Pi branches, gamma_L included.
  - The four gates that are not flat at the origin (E1, P1, P2, P4) fail at every threshold at 2.512e4 and 198.
- **Ungated growth factor.** C1, CP02 and I agree that the ungated cold dark energy's self-gravity factor is
  mu^2/(mu^2 + k_phys^2) once the law's P sector is kept, not the polytrope's 1 - k^2/mu^2. My KA4 derives both exactly.
  - **Not computed here:** C1's a0-saturation caveat (W non-quadratic near recombination at low mu_K). My reduction
    assumes W quadratic, which holds at 2.512e4.
  - **Not computed here:** the corrected CMB-lensing line itself. C1 estimates it at about 1.5e4 to 2.5e4. I graded at the
    record's 2.512e4 as frozen, and the label is the same at 198 and 8.89e6.

### (ii) Ordering of clusters against galaxies

**Agree with the direction of PIK1's conclusion (the cluster is starved relative to the galaxy ceiling). Disagree with its
mechanism as stated and with its numbers.**
- **What PIK1 compared.** It set one dominant-radius u per system: galaxy 37, cluster 195 (C2 corrects these to 36 and
  614, a ratio of about 17).
- **What I computed.** The phantom densities at the graded radii (in rho_d0) are:
  - X-COP: 769 to 1.05e4;
  - groups: 466 to 2.1e3;
  - galaxies at 1-30 kpc: 2.2e3 to 3.2e6;
  - the KiDS range out to r_c: far lower.
  So clusters do not sit above galaxies at every radius.
- **What binds is the KiDS outskirts.** The threshold at which the groups get their dust always sits 1.15 to 1.5 dex
  above the highest threshold the galaxy rows allow:

  | gate | galaxy rows allow log xi up to | groups pass at log xi |
  |---|---|---|
  | E1 | 0.3 | 1.6 |
  | P4 | -0.5 | 0.9 |
  | F2 | 0.7 | 2.2 |
  | F3 | 0.95 | 2.4 |
  | R3 | -1.2 (rows 5-7) | 0.2 |
  | step | 1.55 | 2.7 |

  That agrees with C2's note that "the binding galaxy is the 1e10 one at 1 Mpc".
- **X-COP fails on shape as well as amount.** No gate reaches rms below 0.39. PIK1 asserted the shape failure only for
  its non-monotone case. I computed it for every graded gate, and for the band gate (reported): no pass.
- **Groups.** PIK1 wrote "groups broken". In my scan the groups do pass in narrow bands for seven of eight gates, but
  never at a threshold the galaxies allow. Wherever they pass, row 8b fails by 1e13 to 1e18.
- **Quality.** Rows 5 and 6 are a proxy inequality on point masses, not MK1's graders.

### (iii) Early-history requirement (the Codex session: mu_K >= 8.89e6 per Mpc)

**Agree that this number is gate-independent.** Pi = 0 on FRW and S(0) = 1, so the background, including the stiff
a^-6 partner, is the quadratic's exactly (row 1, C0a). The 8.89e6 line is KD1's B1b (stiff part <= 0.067 of radiation
at BBN). I took it from `kd1.json` and did not recompute it; C1 reproduces it.

My lane graded at 8.89e6 as a reported third value of mu_K. The label is the same: CMB-ONLY, with no X-COP pass. There
E1, P1, P2 and P4 pass linear health only for xi >= 10^9.5 to 10^10.15, thresholds that shut the gate in every static
system.

**Not computed here:** whether the 0.067 criterion is the right early-history line for a gated construction.

### (iv) A galaxy pressure ceiling (the Codex session: mu_K <= about 450 per Mpc)

**Not computed here.** CP02's 450 per Mpc comes from the static pressure of its repaired, non-multiplicative construction
(a Q-dependent compensator) and a lapse-flux bound. This lane graded only the multiplicative gate of PIK1's criteria and
computed no pressure bound. My nearest quantities are of a different kind:
- row 8a: the law shift from the gate, 1e3 to 1e9 times the 0.02 line where groups pass;
- row 8b: the P-block sign on halo backgrounds.
Neither is a pressure ceiling on mu_K, so I neither confirm nor dispute 450.

### (v) An instability of the flat-gate family

**Partly agree, within a narrower scope.**
- **About FRW at linear order** I find the flat gates healthy, not unstable:
  - F2 (S''(0) = -2) has 0 < beta <= 1;
  - F3, R3 and the step are invisible.
- **On static halo backgrounds** (fixed metric, gravity not coupled, local high k, gamma_L included):
  - every flat gate has S'' > 0 above u = 0.71 (F2), 0.87 (F3) or 0.79 (R3);
  - row 8b fails by 1e14 to 1e18 wherever such a gate is partly open in a halo.

  That agrees in kind with C2's checked lemma (S'' > 0 somewhere for any non-negative, non-increasing, non-constant C2
  gate) and with the P-block negativity both C2 and CP02 report.
- **This lane's own CMB-ONLY configurations** are healthy at the graded radii only because those radii end before the
  phantom density falls to about rho_c. Without the cap (reported, M-NOCAP) F2 at xi = 1 already crosses the bad band
  inside 1000 kpc: row 8b 8.9e6 / 4.3e3. Any halo that extends to where u ~ 1 crosses it.
- **Not computed here:** the full constrained GR scalar (lapse, shift, metric scalar, tangency) and the clamped-gate
  compression run on which CP02 rests its "established instability". C2 left that claim NOT CHECKED, and so do I. My
  fixed-metric result is a P-block statement, not a ghost theorem.

## Where I differ from the corrections, beyond the five points

- **PIK1's row 8(a) "PASS".** Its absolute estimate, |G| ~ (Phi/c^2)(rho_K/rho_c)|d ln S/d ln u|, is right as an
  absolute size. The line that matters, however, is |D G| against |A|, and PIK1 took |A| ~ (g/a0)(1/L). In fact
  A = grad Phi/c^2 ~ Phi/(c^2 L) carries the same Phi/c^2. In SI, c^2 Gm = mu^2 Phi^2 S'/(8 pi G rho_c) is Newtonian
  (c cancels; C0b, KA9). So the relative shift is c^2 Gm / Phi ~ (rho_K1/2 rho_c)|S'|: of order the
  dust-to-threshold density ratio, not 1e-6. My row 8a is far above its line wherever the gate does work.
- **PIK1's growth sentence** ("the dust's linear clustering is bit-for-bit MK1's") fails twice. The gate is visible, and
  even ungated, MK1's polytrope omitted the P sector (point (i)).

## Not computed here (summary)

- a CMB-lensing likelihood;
- the full covariant stress and the coupled-gravity spectrum;
- SPARC and KiDS through MK1's own graders;
- the gate's back-reaction on the law solved self-consistently;
- CP02's pressure ceiling and repaired constructions;
- the full constrained instability;
- C1's a0-saturation regime;
- any Lean.

**Commit ids and the lead's re-run (added 2026-11-12, after landing; no number or label changes).** Local / origin:
criteria 95edd35e0b / 30437ca36e; scripts and runs ccc4f4fc92 / 4958e06600; RESULT_BLIND 6652b8a845 / c1987ded02; RESULT
50b150708e / 4c424c9275. Pushed. The lead session re-ran all seven jobs from a copy at the same folder depth, one
thread, in sequence (`pik2_row0.py`, `pik2_row2.py` and `pik2_static.py`, each also with `--mutate`, then
`pik2_grade.py`): the seven JSON outputs are equal in content to the committed ones (the four large ones compared after
unpacking), `pik2_grade.out` is equal byte for byte, and the six other logs differ only in their runtime line. The lead
also confirmed in git that the criteria commit holds that one file. That is a reproduction of this lane's own code, not
an independent re-grade. A CMB-ONLY label is not a window, so no re-grade is owed for a hit; the items listed above as
not computed stay not computed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
