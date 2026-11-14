# BJ1 FROZEN CRITERIA (2026-11-14, written 15:12 EST by the clock): the charge-budget junction, the law's halo as far as the delivered charge pays for

Committed alone, before any script of this lane exists and before any number of this layout has been computed by
anyone. TEST lane, NOT blind: adopts nothing, relabels nothing, registers nothing. Footings (canonical a0 = 9.3603e-11
m/s^2, alt a0 = 1.1312e-10 m/s^2) are graded separately and never pooled. Cold dark energy is a gravitating field
component; no particle is added. kappa = 1/2 and the share 5.41 are FITTED. Rule 6 is a candidate, NOT ADOPTED. A HOLDS
is a hit that awaits a frozen, blind re-grade; it is not a pass of the theory. Nothing here can say the data favour the
framework.

## 0. Why, and what was seen before this freeze

Today's lanes left three facts.
- XJ1: with the law's layout unscaled inside the settled radius ("exact junction") the forest holds at flux level only
  for settled radii inside the fold; the second and third caustic of the clock's infall hold in one build (hits, post
  hoc). That junction keeps the law inside R_k and pays for it by rescaling the whole outside by a factor t (0.85 to
  1.06 on the forest's haloes): charge is moved across the caustic by fiat.
- The junction note of the Codex session and its audit (`codex_mass_budget_2026_11_14/latest_review/`,
  `reviews/codex_mass_budget_audit_2026_11_14/`): with no surface reservoir a conserved current obeys
  [J^r] - Rdot [J^t] = 0 at an interface, the action's non-advective flux is 3e-7 to 5e-7 of the advective one in the
  weak field, and in 3,706 of 7,110 snapshots of XJ1's caustic layouts a standing interior with a growing boundary
  would need outflow.
- CSD1: in the clock's shell equation the static balance is the law exactly, so charge that stands is the law's halo
  of exactly that charge; the integrated no-reservoir condition is D_k = Q_delivered(< R_k) / C_law(R_k) = 1; with the
  reference layout as the delivered charge, D_3 is 0.49 to 1.67 (under at low mass, over at high mass; it crosses 1
  near log M_b 10.1 / 10.4 today and near 8.6 to 9.2 at z 2.2 to 4.4), and where the reference is over, the radius
  where the two enclosed charges agree is 0.6 to 2 fold radii today and 1.4 to 16 at z 2.2 to 4.4.

Seen, therefore: every committed number of XJ1, CSD1, the audit and the earlier forest lanes (FZS1's junction: 0.024 /
0.029 at f 2, 0.57 / 0.69 at f 3, 8.8 / 10.9 at f 5, 194 / 288 at f 10; exact junction: 0.51 / 0.69 at the third
caustic, 3.94 / 5.37 at the fold, 16.4 / 25.7 at f 2). No number of the layout defined below exists.

## 1. The layout

All in FRZ1's halo model as FZS1 and XJ1 use it (their files are read-only; XJ1's `xj1_lib2.py` supplies the caustic
reader and may be imported). For a halo at redshift z on a footing: C_B(r) = M_B(r) - Bar(r) the law's enclosed cold
mass (FRZ1 mode "B"), C_R(r) = M_R(r) - Bar(r) the reference's (mode "Rb"), C_tot = C_R(r_ta) = C_B(r_ta), R_k the k-th
caustic (XJ1's reader on its shell runs, capped at r_ta).

- **Boundary (unchanged):** a halo with v_vir > v*(z) keeps the reference at every radius.
- **Capture:** the charge that stands is the charge the reference flow has delivered inside the caustic,
  Q_k = C_R(R_k). Nothing else is moved.
- **The standing region:** the law's layout, unscaled, out to the radius R_set that this charge pays for:
  - if C_B(R_k) >= Q_k (the law needs at least what was delivered; "under"): R_set <= R_k is the root of
    C_B(R_set) = Q_k. Between R_set and R_k there is no cold charge: C(r) = Q_k. Beyond R_k: C(r) = C_R(r).
  - if C_B(R_k) < Q_k ("over"): the standing region grows until the law's enclosed charge equals the reference's:
    R_set is the first radius beyond R_k where C_B(r) = C_R(r) (the equal-charge radius); if there is none inside r_ta,
    R_set = r_ta. Beyond R_set: C(r) = C_R(r).
  - In both branches C(r) = C_B(r) for r <= R_set and C(r) = C_R(max(r, R_k)) for r > R_set, so the layout is one
    formula, the reference is untouched beyond max(R_k, R_set), no factor multiplies anything, and the charge inside
    the capture surface is conserved identically.
- M(r) = Bar(r) + C(r). The total at r_ta is the halo's turnaround mass.
- Cases: **B1, B2, B3** (capture at the first, second, third caustic).

What this is not: a flow. The delivered charge is the halo model's reference layout (rule 3's cold dust), which the
clock's own shell equation does not produce (CSD1). The emptied shell between R_set and R_k in the "under" branch is an
idealisation (charge in transit is neglected).

## 2. Gates

**G-RC, rotation curves (the gate this layout can fail outright).** PD1's P2-SPARC statistic and gate, code copied
as XJ1's `xj1_sparc.py` copied it (QX8's loader and exact-field term, per-galaxy best mass-to-light ratio on QX8's
grid, pooled weighted rms and mean, all 175 galaxies and the massive tail), with the model at z = 0
g = law(g_N) for r <= R_set and g = g_N + G C(r) / r^2 beyond, C as in section 1, from SRH1's lens `profile` chain
at the galaxy's M_b (PD1's). PD1's gate: rms <= L0 + 0.010 and |mean| <= 0.05 for all galaxies and for the massive
tail. Also reported: how many galaxies have their last point beyond R_set, with names and ratios; the same at
mass-to-light 0.3 and 0.8.

**G-L, lensing.** JNT2's G4 chain (ONE1's KiDS gate as SRH1 ran it), lens profile from section 1 at the lens redshift;
JNT2's gate words.

**G-F, the forest.** Reported first at matter level (JNT2's G1 route, gate 4, with the word PASS or FAIL). At flux
level, build B (FWN1R's library, 4 seeds in all 12 bins, the estimator, D, SE, gate 4, known answers, twins, brackets
and label rule exactly as XJ1's second pass, with fields R, B1, B2, B3 and the twin R + 2 (B1 - R) at the anchors):
labels FOREST ROW HOLDS AT FLUX LEVEL / FOREST ROW FAILS AT FLUX LEVEL / NO VERDICT, FRAGILE with the bracket named.
The flux-level run is heavy; it is launched only for cases that pass G-RC, and only when no more than two other heavy
processes are alive. If it has not run when RESULT.md is first written, that is stated and it is added by a dated note.

**Known answers (profile level, every halo below v*(z), every z and footing, all three cases):**
(i) C(r) = C_B(r) at every node r <= R_set to 1e-12 relative; (ii) C(r) = C_R(r) at every node r >= max(R_k, R_set)
to 1e-12; (iii) C(r_ta) = C_tot to 1e-12; (iv) C non-decreasing; (v) C(R_k) = C_R(R_k) in the "under" branch and
C(R_set) = C_R(R_set) in the "over" branch (the zero-flux identity) to 1e-9; (vi) forcing R_k to r_ta gives mode "B"
at every node and forcing R_k to 0 gives the reference exactly; (vii) haloes above v*(z) have the reference row
exactly; (viii) for G-RC, cap charge set to infinity reproduces PD1's stored L0 to 1e-9; (ix) for G-L and matter
level, the anchors XJ1 used (JNT2's stored f = 2 rows) reproduce.

## 3. Lane words, per footing and per case

- "BUDGET JUNCTION HOLDS AT CAUSTIC k" if G-RC passes, G-L passes and G-F reads HOLDS at flux level (FRAGILE carried);
- "FAILS ON ROTATION CURVES (caustic k)" if G-RC fails;
- "FAILS THE FOREST (caustic k)" if G-F reads FAILS at flux level;
- "FAILS LENSING (caustic k)" if G-L fails;
- otherwise "NOT RESOLVED (caustic k)", the cause named (including "flux level not run").
More than one failing word may be given. A HOLDS is a hit awaiting a blind re-grade.

Reported whatever the words: the share of haloes in each branch by mass and redshift; R_set / R_k and R_set / R_fold;
the Milky Way's outer-mass reading (XJ1's `xj1_mw.py` with this layout); t-free check (no factor anywhere).

## 4. What counts against (whatever the labels)

- Post hoc, and the fourth settled-radius variant of the day (f R_fold with a rescale; the exact junction at f R_fold
  and at the turnaround surface; the exact junction at a caustic; this). A hold needs a frozen, blind lane.
- The capture surface is again a choice of k.
- The delivered charge is the halo model's reference, not a flow of the action; the mu_K = 0 shell equation cannot
  gather it (CSD1), and no dust term joins the two regimes (MK1, MK2, PIK2).
- Conserving charge at the capture surface is necessary for a dynamical junction, not sufficient: momentum, energy,
  the approach to rest and stability are untouched.
- The gas inputs of the forest gate are provisional and inherited.

## 5. Hand estimate (before any number)

"Under" haloes are the light ones today (log M_b below about 10.1 / 10.4 at the third caustic) and very few at the
forest's redshifts; "over" haloes are the rule at z 2.2 to 4.4.
- G-RC: R_set is about D_3 R_3 for under systems, 0.28 to 0.5 fold radii for log M_b 8 to 10, against last measured
  points at a median 0.15 and a worst 0.41 of the fold radius. Guess: 0 to 8 galaxies beyond R_set at k = 3, fewer at
  k = 2 and 1; the gate passes at k = 1 and 2 (70 %) and at k = 3 (55 %).
- G-L: passes for every k (70 %).
- G-F, matter level: the over branch puts the law out to 1.4 to 16 fold radii in the heavier forest haloes with no
  charge moved; FZS1's junction, which also moves no charge across R_set, read 8.8 at f 5 and 194 at f 10. Guess: 5 to
  100 on canonical for every k, FAIL (65 %); flux level FAILS (55 %), HOLDS (25 %).
- Most likely lane word: FAILS THE FOREST for every k, on both footings (50 %). Low confidence: nobody has computed it.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
