# SRH1R FROZEN CRITERIA: blind re-grade of SRH1's lensing gate inside the forest window

Committed alone, before any SRH1R script exists and before any SRH1R number is computed. TEST lane, quarantined. Relabels
nothing, adopts nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded
separately, never pooled. Cold dark energy is a gravitating field component; no particle is added anywhere.
kappa = 1/2 FITTED; not theory closed.

**This family is post hoc** to FRZ1 and FZS1 (SRH1's own statement). A HOLDS reading here does not turn SRH1's frozen
label into a pass, is not a pass of form B, and nothing here is in PAPER72.

## 0. The question

For SRH1's settled layout at f = 0.40, 0.50, 0.60, 0.70 (R_set = f x R_fold), does KiDS galaxy-galaxy lensing around
host-free lenses agree with the model, on each footing? Statistic, samples and pass line are mine and are fixed here.

## 1. What I had seen before this freeze (blindness is not perfect)

- The lane brief: SRH1's label is WINDOW EMPTY on both footings; the forest allows f up to about 0.72; the lensing gate
  fails there "by a narrow margin". The one-line memory index adds: "KiDS lensing f >= 1.0 (near th...". Nothing else of
  SRH1's lensing numbers.
- In SRH1's folder: `FROZEN_CRITERIA.md` only (commit 5ed8a37ec6). It quotes ONE1's stored data-side values (R_s 0.811 +-
  0.134 / 0.809 +- 0.133 at 1.6 R_h, model 1.003 / 0.847) and hand estimates. Not opened: its RESULT, amendment, any
  `srh1_lens*`, `srh1_tilt*`, `srh1_grade*`, any run log, `srh1_lens.py`, `srh1_tilt.py`, the reruns note, the two memory
  files named in the brief.
- KO1's criteria; grep lines of KO1's AMENDMENT_A2 (the tapered veto edge; host-free amplitudes against the point law at
  1.0 R_h, canonical outer | middle | inner 1.10 | 1.82 | 1.81, late outer -0.19 +- 0.39). ONE1's criteria (k near 2.8 /
  2.4 at 1.6 R_h). KO1R's RESULT in full and the data-convention functions of `ko1r.py` (distances, masses, host finder).
- FZS1's `rfold_kpc` (18 lines); FRZ1's `halo_basics_z`, `dta_of`, `conc`, `phantom` and constants; the layout of one FLD1
  run file (canonical log M_b 10.45: R_fold 139.30 kpc at z 0); PD1's share X = 59.4861 / 59.5029; the array names and
  shapes of the staged lensing files.
- No lensing statistic of any settled layout, no pair count, no neighbour term has been computed or seen by me.

## 2. Data side (my own stack from the staged per-lens sums; said here before any number)

Files in `real_research/data/lensing_rar/` (git-ignored, passed as an argument, read as data only): `lr_lenses.npz`,
`cfg110_perlens.npz` (WG, WW, 15 g_bar bins, edges 1e-15 to 5e-12 m/s^2), `cfg96_stack.npz` (50 jackknife patches),
`KiDS_DR4_brightsample.fits` with its LePhare file (neighbour pool and host flags). Conventions are the record's (KO1
criteria): D_b = 4 G sum WG / sum WW; cell (lens l, bin b) = the annulus R_lo = sqrt(G Mgal / g_hi) to
R_hi = min(sqrt(G Mgal / g_lo), 3 Mpc) physical; pool r < 20, 0.02 <= z <= 0.8, log M* > 7; Mgal from the record's
cold-gas recipe; record constants and distances.

- **Host-free set.** KO1's definition (a pool object at least 0.3 dex more massive, |Delta chi| < 230 Mpc, projected
  inside the veto radius), written in my own code. **Veto radius 1.6 R_h (primary)**: the tapered edge of a narrower veto
  falls inside the outer bins (KO1 A2). 1.3 R_h is reported.
- **Tie rule: KO1R's** (a mass tie within 1e-9 dex counts as a host). This differs from SRH1's choice (KO1's plain float
  comparison) on purpose; the plain rule is a bracket.
- **Samples:** all, late (typ 0), early (typ 1).
- **Graded bins: 0 to 12** (13 bins). Bins 13 and 14 (inside the record's inner window, about 65 kpc for a typical lens)
  are reported only.

## 3. Model side (all my own code; nothing imported from SRH1 or ONE1)

**Own halo of a lens** with M_b = k Mgal at its own z_lens, spherical, baryons a central point:
- C_B(r) = min(Mph(r), X M_b), Mph = M_b [sqrt(1/4 + x^2) - 1/2], x = r / r_M, r_M = sqrt(G M_b / a0) (a0 constant).
- C_R(r) = X M_b m_nfw(r / r_s) / m_nfw(r_ta / r_s) for r <= r_ta, X M_b beyond: FRZ1's reference halo with
  M_ta = X M_b / (1 - FB) at z_lens (h 0.6736, omega_b 0.02237, omega_c 0.1200, 200 x mean density, concentration
  10.14 (M / 2e12)^-0.081 (1 + z)^-1.01, Delta_ta(z) = 5.55 + 6.26 (1 - Om(z)) / (1 - Om)), radii to physical.
- R_set = min(f R_fold(z_lens, M_b), r_ta); R_fold from FLD1's twelve primary run files, linear in z on each series, log R
  linear in log M_b, M_b^(1/3) outside 6.5 to 12 (FZS1's rule, re-written).
- Cold mass inside r: s C_B(r) for r <= R_set, C_R(r) outside, s = C_R(R_set) / C_B(R_set). Total (1 + X) M_b.
- **The model for D is 4 G DeltaSigma(R) itself**, DeltaSigma = mean Sigma inside R minus Sigma at R, from the exact
  projection of the density (pieces split at R_set and r_ta), area-averaged over each cell. This is not ONE1's convention
  (law value times a projected ratio); the difference is mine and is stated.

**Neighbours.** Every pool object other than the lens with |Delta chi| < 230 Mpc whose halo can reach the lens's
outermost circle carries its own settled halo (same f, same X, mass k Mgal_j, laid out at the lens's redshift). Its
contribution to a cell is exact for any mass distribution: the annulus average of [mass inside the circle / (pi R^2) -
circle average of Sigma], from the offset halo's projected mass inside each circle. Evaluated from tables in (log M, z, R,
d); on a k grid for the neighbour term, interpolated in log k. No shuffled-position term is subtracted in the graded
model; the same sum around permuted lens positions (3 permutations, seed 52) is reported as a null, and the gate is
re-read with it subtracted (bracket).

**Mass factor k.** One free number per sample, footing and f, fitted on the graded bins (below), bounds 0.5 to 8.

## 4. The statistic and the pass line

For a sample and a model: r_b(k) = D_b - M_b(k), M_b the WW-weighted stack of the cell models.
1. k0 minimises r^T C_D^-1 r, C_D the delete-one-patch jackknife covariance of D (50 patches).
2. C = jackknife covariance of the residual r at k0 (each replicate re-stacks data and model, k held at k0), inverse
   multiplied by the Hartlap factor (50 - 13 - 2) / 49.
3. **T = min over k of r^T C^-1 r**, 12 degrees of freedom. p from the chi-square distribution.

**Three lines per f and footing: all, late, early. A line passes iff p >= 0.05 / 3** (three lines tested, so each is held
to 0.0167; T <= about 24.5). **The gate passes at f iff all three lines pass.** One sub-sample can fail the gate alone,
at that corrected level. A fitted k on a bound makes that line NOT EVALUABLE.

## 5. Labels (per footing)

- **LENSING HOLDS IN THE WINDOW** iff the gate passes at one or more of f = 0.40, 0.50, 0.60, 0.70, every known answer
  passes and every MUTATE twin bites. The passing f are named.
- **LENSING FAILS IN THE WINDOW** iff the gate fails at all four f, with known answers and twins as above. The failing
  line and its p are named at each f.
- **NO VERDICT** iff a known answer fails, a twin does not bite, or a line is NOT EVALUABLE at every f.
- **Qualifier "does not separate":** printed if the gate's status is the same at the four f and at all three comparators
  (f = 0, the reference everywhere; f = inf, R_set = r_ta; the law's halo to x_t with no reference, ONE1's layout).
- **Qualifier "fragile":** printed if the plain tie rule, the 1.3 R_h veto, or the null-subtracted model changes the
  gate's status at any window f.

## 6. Known answers (all must pass before any gate is read)

- KA1 point mass: my projection returns DeltaSigma = M / (pi R^2) to 1e-6.
- KA2 the law's untruncated halo (X = 1e8): 4 G DeltaSigma = sqrt(G M_b a0) / R to 1e-3 for 30 <= R / r_M <= 1000.
- KA3 far field: for every layout, DeltaSigma pi R^2 / [(1 + X) M_b] = 1 to 1e-6 beyond the halo's edge; for the law's halo
  to x_t the ratio to the untruncated form at u = 2000 is 4 (1 + X) / (pi u) to 1e-3 (X = 53.64).
- KA4 mass: the cold mass is continuous at R_set, non-decreasing, and equals X M_b at r_ta (1e-9), on a grid of (M, z, f).
- KA5 R_fold: canonical log M_b 10.45 at z 0 returns the run file's stored end value to 1e-6.
- KA6 data side: host-free counts with the plain tie rule 40,667 / 25,708 / 17,335 at 1.0 / 1.3 / 1.6 R_h, and 40,149 at
  1.0 R_h with KO1R's rule; with KO1's point-law cell model, A_hf at 1.0 R_h (KO1R's rule) = 1.0822 +- 0.1583 (canonical)
  and 0.9847 +- 0.1440 (alt), to 1e-3.
- KA7 neighbour kernel: a point mass gives the step M / (pi R^2) for R > d (annulus average in closed form, 1e-6); an
  extended halo at d = 0 equals the own-halo projection (1e-3); an extended halo wholly inside or outside a cell's circles
  equals the point mass (1e-4); the table interpolation agrees with direct integration to 1 % on 200 random pairs.
- KA8 plant: WG replaced by WW x the cell model at f = 0.5, k = 2 returns k = 2 (1e-4) and T < 1e-6.

## 7. MUTATE twins (separate outputs; each must bite on each footing)

- MU1, share x 0.1 at f = 0.5: the gate must fail.
- MU2, the cold reference outside R_set removed at f = 0.5 (halo ends at R_set, mass not conserved): the gate must fail,
  or T (all) must move by at least 4 from f = 0.5's.
- MU3, f = 0.05: the gate's status must differ from f = 0.5's, or T (all) must move by at least 4.
- A twin that does not bite is disclosed and gives NO VERDICT; for MU2 and MU3 that would mean lensing has no power on
  the layout.

## 8. Reported, not graded

T, p, k per line at every f and comparator; per-bin data and model; bins 13 and 14; the neighbour share per bin; the null;
the 1.3 R_h veto; the plain tie rule; the Hotelling form of p; k fixed at 1.

## 9. What counts against (stated now)

- A pass that comes from a large error: every T is printed with its line; the twins measure power.
- The pool is flux-limited, so the neighbour term is a lower bound. The reference halo is FRZ1's (concentration and
  Delta_ta carried from that lane, PROVISIONAL). Baryons are a central point. Neighbours are laid out at the lens's z.
- The window is in a family picked after the forest fails were seen.

## 10. Hand estimate (before any number; to be checked, not trusted)

k near 2.5 / 2.2. T (all) between 12 and 30 at every window f, moving by a few units across f. Late types are the line
most likely to fail. My guess: HOLDS 55 %, FAILS 30 %, NO VERDICT 15 % (MU3 not biting), the same on both footings.

## 11. Order and files

Criteria (this file, alone) -> `srh1r_model.py` (tables, KA1-5, KA7) -> `srh1r_data.py` (host flags, pairs, KA6) ->
`srh1r_grade.py` (stack, fit, KA8, twins, labels) -> `RESULT.md` with my verdict -> only then SRH1's `RESULT.md` and
`srh1_lens.out` are opened and an "Unblinded comparison" section is added. The label is not changed after unblinding.
Later changes go in dated AMENDMENT files and are post hoc.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
