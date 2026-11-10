# SCS3 RESULT: is the static clock stable around a disc in a uniform external field?

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11 m/s^2) and alt (1.1312e-10) are reported separately and never pooled. The component is cold dark
energy, never a particle. Criteria eff0ae1861; amendments A1 f51866c8d4, A2 63ed365df0, A3 fe9811fe03, A4 b34295ebcd, all
post hoc, each committed alone before any number under it (disclosures below).

## Labels (canonical / alt)

| Family | Frozen | A1 | A2 | **A4 (last reading)** | Rule alone, per background (A4) |
|---|---|---|---|---|---|
| External field along the axis (2D; 0.01 and 0.1 a0) | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | **NO VERDICT / NO VERDICT** | UNSTABLE on 11 of 16 / 10 of 16 backgrounds |
| External field in the plane (3D; 0.01 and 0.1 a0) | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | **NO VERDICT / NO VERDICT** | UNSTABLE on 4 of 8 / 4 of 8 |
| Thick-disc twin, axial (criteria 2c) | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | 2 of 8 / 3 of 8; RATE UNBOUNDED on 1 / 1 (the disc-centre null, below) |
| Thick-disc twin, in the plane | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | NO VERDICT / NO VERDICT | 2 of 4 / 1 of 4 |

The labels are read off the outputs by scs3_labels.py (scs3_labels.out / .json).

**Why every label is still NO VERDICT.**
- **Frozen, A1, A2:** known answer **KA3 fails**. My frozen convergence rule had a "flat" clause: when both differences are
  within 2 %, it returned the finest value without extrapolating. On KA3's test sequences it missed the known limit by up to
  2.4e-2 (line 1e-6), while claiming an error about half the true one. A known answer failing makes every label NO VERDICT.
  The frozen reading also has the inner-boundary artefact on 11 of 32 axial backgrounds at R3 (A1).
- **A4** (flat clause removed; KA3 then passes at 1e-15) requires every background in a family to converge. It does not:
  - **Axial family.** 21 of 32 backgrounds converge to UNSTABLE.
    - Five canonical and six alt do not.
    - On six of those eleven, route L's finest three e-folding times still creep, by 0.55-0.84 % across R4-R6, too evenly
      for the observed order to fall inside [0.5, 6].
    - On the others, route 2 has not converged by R4. R5 for route 2 needs 5.4-7.1 GB, above A1's 4 GB line, so R5 is not
      used.
    - One (alt expo 10.7 at 0.01 a0) also fails KA5 (ratio 0.51) and its inner radius.
  - **In-plane family.** Its three grids (R0-R2) are not in the asymptotic range (finest-three spread 6-12 %). R3 does not
    fit in memory.

**What is nonetheless true, on every background, both footings, both families.**
- The region where the law's phantom density D.P is negative exists on every grid.
- Both routes find growth on every grid they ran:
  - route L: every resolution;
  - route 2 (axial): R0-R4;
  - route 2 (in-plane): a negative Rayleigh certificate at R0-R2.
- Nothing about the sign is in doubt. **STABLE is excluded.**
- What the rule cannot certify is the last percent of the rate on a third of the axial backgrounds and the last ~10 % on
  the in-plane ones.

## The answer in plain words

Around a disc held in a uniform external field, form B's static clock is unstable in a region of its halo. The growth is
slow and far outside the disc.

- **Where.** In a shell from 0.74-0.85 r_e outward, where r_e = sqrt(G M a0)/g_e. It is strongest on the flank of the total
  field's null, at about 0.85-0.95 r_e, 40 degrees off the axis through the null. In units of the disc, the region starts at
  10-35 R_d (0.1 a0) and 105-325 R_d (0.01 a0). It never comes inside 5 R_d: no negative cell reaches the disc on any
  background or grid.
- **How fast.** The e-folding time is about one fifth of the Kepler period of the baryons at that radius
  (t_e / T_Kepler(r*) = 0.15-0.21 on every axial and in-plane background).
  - At 0.1 a0: 0.73-0.85 Gyr for log M_b 9.4, rising to 1.7-2.0 Gyr for log M_b 10.9.
  - At 0.01 a0: 22-61 Gyr.
  - Against the disc's own orbital time at 2.2 R_d, the growth is 3.6-14 times slower at 0.1 a0 and 110-430 times slower
    at 0.01 a0.
- **It is a point-mass effect, not a disc effect.** A point mass of the same baryonic mass in the same field gives the same
  e-folding time as the razor-thin exponential disc and the Kuzmin disc:
  - to within 0.7 % at R3-R5;
  - in-plane runs to within 3 % at R0-R2 (scs3_pointmass.out).

  A point mass in a uniform field is symmetric about the field. So the axial and in-plane families are the same problem at
  r ~ r_e, and disc shape and orientation do not enter. Seen this way, the in-plane family's unconverged rates are the
  axial family's rates.
- **A slow instability confined to a region of the halo, not a disc being destroyed.** Linear only: whether the growth
  saturates, reshapes the outer halo or leaves the static branch is not computed.

## Per family and footing (A4 reading; finest grid R6 axial, R2 in-plane)

E-folding times in Gyr. "Converged" means the rule's extrapolated value for the backgrounds labelled UNSTABLE by the rule
alone. Region values are in units of r_e. Route 2 is on the axial family only (R4).

| Family | Footing | g_e | n | UNSTABLE by rule | e-fold at finest grid | converged (Richardson) | route 2 at R4 | KA5 ratio | inner radius / r_e | Q_neg/Q_pos |
|---|---|---|---|---|---|---|---|---|---|---|
| Axial | canonical | 0.01 a0 | 8 | 5 | 25.8-61.2 | 25.8-61.2 | 26.8-63.6 | 0.94-1.05 | 0.737-0.755 | 0.053-0.148 |
| Axial | canonical | 0.1 a0 | 8 | 6 | 0.849-2.01 | 0.848-2.00 | 0.885-2.10 | 0.94-1.00 | 0.741-0.792 | 0.243-0.288 |
| Axial | alt | 0.01 a0 | 8 | 4 | 22.4-53.1 | 22.4-40.9 | 23.2-55.1 | 0.51-1.12 | 0.738-0.754 | 0.057-0.155 |
| Axial | alt | 0.1 a0 | 8 | 6 | 0.736-1.75 | 0.734-1.74 | 0.768-1.82 | 0.94-1.00 | 0.738-0.788 | 0.245-0.289 |
| In-plane | canonical | 0.01 a0 | 4 | 2 | 26.7-63.8 | 24.7-25.0 | Rayleigh negative R0-R2 | - | 0.780-0.784 | 0.276-0.362 |
| In-plane | canonical | 0.1 a0 | 4 | 2 | 0.876-2.09 | 0.882-1.94 | Rayleigh negative R0-R2 | - | 0.832-0.846 | 0.698-0.888 |
| In-plane | alt | 0.01 a0 | 4 | 2 | 23.2-55.6 | 52.9-53.3 | Rayleigh negative R0-R2 | - | 0.792-0.795 | 0.280-0.369 |
| In-plane | alt | 0.1 a0 | 4 | 2 | 0.761-1.81 | 1.67-1.78 | Rayleigh negative R0-R2 | - | 0.827-0.841 | 0.726-0.895 |

Notes on the table:
- **Rows by background:** each axial background's e-folding times at R0-R6, its route-2 sequence and its rule outcome are
  in scs3_labels.out under "reading: A4".
- **The gate:** KA1, KA2 and the A4 KA3 all pass; KA4 fails. A4 does not use the two-grid rule, so KA4 does not gate it.
- **Route 2 against route L** (KA5: route 2's extrapolated growth over the same operator's local symbol) agrees to 0.94-1.05
  on every converged pair but one. Route 2's growth is the high-k limit of the local symbol: no global mode lies below it.
- **The in-plane Q_neg/Q_pos is much larger** (0.70-0.90 at 0.1 a0) than the axial one. The reason is the far-field band:
  with g_e in the plane, the band perpendicular to g_e contains the disc's axis and wraps around the disc.

## Physical reading (criteria section 7)

- **An LMC-like satellite** (log M_b 9.4, g_e = 0.1 a0):
  - r_e = 19.3 kpc (canonical) / 17.6 kpc (alt);
  - e-folding 0.85 / 0.74 Gyr, so 16 / 19 e-folds in t_H = 13.8 Gyr;
  - the region with more than one e-fold in t_H runs from 0.78 to 6.3-6.9 r_e, i.e. 12-97 R_d or about 15-120 kpc.
  - The disc (R_d about 1.25 kpc, orbital time 0.2 Gyr at 2.2 R_d) is not in it.
  - **The uniform-field model does not hold there.** The LMC is about 50 kpc from its host, about 2.6 r_e, so the host's
    field changes by order unity across the unstable region. For the LMC, these numbers say that the static clock's halo
    beyond about 15 kpc would not stay static over a Hubble time. They say nothing about the LMC's disc.
- **A disc galaxy in a group:**
  - At g_e = 0.1 a0: 7-10 e-folds in t_H, in a shell from about 0.8 to 3.5-4.7 r_e (about 50-390 kpc). Again outside the disc,
    and again where a real group's field is not uniform.
  - At g_e = 0.01 a0: 0.22-0.62 e-folds in t_H. In linear theory, nothing grows appreciably in a Hubble time.
- **In a cluster:** g_e is about a0 or more. Not run: the families stop at 0.1 a0.
- **Which it is.** A slow instability of the outer halo, confined to r >~ 0.75 r_e. Not a disc destroyed.

**The rate in closed form.** In the band perpendicular to g_e, the far-field rate (Lean: farfield_plane_rate) is

    Gamma_ff^2 = G M (2 + x) / (s^3 r^3),   s^2 = (2 + x)/(1 + x),   x = g_e/a0,

a Kepler rate of the baryons. At 4-8 r_e, route L's rate in the band is 1.00-1.02 times it (median per background; cells
0.78-1.23; reported, partly built in by the Dirichlet far field at 10 r_e). The maximum sits at 0.85-0.95 r_e, where it is
nonlinear, but it keeps the Kepler scaling (t_e = 0.15-0.21 T_Kepler).

## A new item found on the way: the disc-centre null (thick twin)

The thick-disc twin was run because the razor-thin sheet's surface phantom is negative at R1-R6. That negativity halves with
each refinement (-1791, -813, ... Msun/kpc^2 at 0.1 a0) and extrapolates to between -1.5 and +9 Msun/kpc^2, i.e. zero within the error, so it is
discretisation. The twin reproduces the halo's rates of the razor-thin family on 14 of 16 axial backgrounds.

On the other two (log M_b 9.4 at 0.1 a0, both footings), R4-R6 put the maximum at r = 0.0115 R_d on the axis below the disc.
- **There is a real null there.** In a thick disc with g_e along the axis, the disc's own vertical field cancels g_e at
  z = g_e / (4 pi G rho_0), about 0.01 R_d for this mass. Inside a deep-MOND bubble of size about a0 / (4 pi G rho_0) the
  law's phantom density is negative on flanks that sit inside the baryons.
- **What the grids show:**
  - D.P there is -1.6e10 to -3.3e10 Msun/kpc^3 and still deepening;
  - the route-L e-folding time falls 1.25 -> 0.87 -> 0.42 Myr at R4-R6;
  - route 2 agrees in sign;
  - the rule calls it RATE UNBOUNDED.
- **A rough deep-MOND estimate** (a sketch, not Lean-checked) says the rate there should saturate near the baryons' own
  free-fall rate, sqrt(12 pi G rho_0), a few Myr, once the bubble is resolved. The grids do not yet resolve it.
- **Other masses.** For denser discs the same null sits inside the A1 analysis mask (r < 0.010 R_d), so it is not seen. An
  isolated disc has its null at the exact centre, which SCS2 and SCS3 both mask.

So **"stable around isolated discs" (SCS2) covers r >= 0.002-0.010 R_d, not the centre.** Whether the static clock is
stable at a disc's own centre is open. It needs a dedicated, resolved local solve: a local grid around the null with the
baryonic density as a source. This lane does not answer it.

## Known answers

| | Result |
|---|---|
| KA1 isolated discs | D.P > 0 in every unmasked cell on all 112 isolated rows (16 primaries x R0-R6; min 64 Msun/kpc^3); route 2 at R0 reproduces SCS2's 24 isolated rows (log M_b 10.45, m 0-2, both parities) exactly (relative 0), all lambda > 0. **PASS** |
| KA2 SCS2's external-field numbers | maps R0/R1, 64 axial rows: identical (relative 0); in-plane R0, 16 rows: identical; route 2 R0, 96 axial rows: identical. **PASS** |
| KA3 the rule on known sequences | frozen rule: **FAIL** (2.4e-2, the flat clause); A4 rule: PASS (1.1e-15); h^-1 labelled diverging under both |
| KA4 two-grid vs three-grid | FAIL in every reading (A4: 3 of 14 canonical, 4 of 15 alt). The two-grid rule is not trusted, which is why A2/A3 gave the in-plane family a third grid |
| KA5 route 2 vs its symbol | 0.94-1.05 on every converged axial pair but alt expo 10.7 at 0.01 a0 (0.51) |
| Solver swap (A2/A3) | MMD-ordered LU vs COLAMD at in-plane R1: Gamma_L^2 to 9e-13, min D.P to 1.4e-13. **PASS** |
| Domain (reported) | at 0.1 a0 the frozen check is vacuous (the grid already reaches 1e3 R_d, about 31 r_e); at 0.01 a0, r_max 20 r_e against 10 r_e changes the R1 e-folding time by 1.4 % / 1.6 % |

## MUTATE

| Arm | Result | Bites? |
|---|---|---|
| M1 tilt sign flipped (G -> -D.P) | the axial maximum moves to cells with D.P > 0 on all 32 backgrounds; the isolated primaries turn unstable | **BITES** (every reading) |
| M2 grid-artefact spike, 10 (h_R0/h)^2 \|min D.P\| at r_e on the axis | the rule converges on 0 of 32 axial backgrounds | **BITES** (every reading) |
| M3 inverted order formula | KA3 misses by 4.8e-3 to 0.29 | **BITES** |
| M4 Lean twin | 7 false statements, 9 errors, exit 1 | **BITES** |

## Lean (fable_independent_2026/lean_2026)

SCS3.lean compiles with exit 0. Its 13 theorems depend only on propext, Classical.choice and Quot.sound (compile.txt):
- growth_par: (1 - K m)/m = K u (2 + u) along the field;
- growth_perp: (1 - K m)/m = K u across it;
- par_beats_perp;
- growth_sign: Gamma^2 > 0 iff D.P < 0;
- growth_zero_at_null;
- farfield_plane_KDP;
- farfield_plane_rate: the closed form above;
- farfield_decreasing;
- richardson_ratio and richardson_limit;
- route2_lower_bound: lambda_min >= min G/J, the shift used by route 2;
- mediant_ge_min;
- inertia_ge_chi: H >= L_chi in scalar form.

SCS3_MUTATE.lean holds seven false versions, proved with the true proofs; all fail (compile_MUTATE.txt).

## What was not graded

- **The nonlinear outcome** of the growth: saturation, a reshaped outer halo, or a clock leaving the static branch.
- **Non-uniform fields.** The LMC and real groups have them on the scale of r_e. So do tides, orbits through the host, and
  fields above 0.1 a0 (clusters).
- **The disc-centre null** (above), and the stiffness-on case. With gamma_L > 0 the rate rises with k^2 where D.P < 0
  (SCS2's stiffness_unbounded); not evaluated.
- **The cosmological background, and the collapse.** Whether the clock reaches the static state at all is COL1's question.
- **Approximations.** As SCS2: Newtonian order, quasi-static metric, local symbol (route L), the pencil without the
  J''_r-theta cross term (route 2), smooth model discs, scale lengths from a relation quoted from memory.

## Anything wrong in SCS2

- **SCS2's coarse external-field numbers are reproduced exactly** (KA2).
- **SCS2's e-folding ranges hold up.** It quoted 0.9-2.4 Gyr at 0.1 a0 and 27-75 Gyr at 0.01 a0 from the coarse grid; the
  finest grids give 0.74-2.0 and 22-61 Gyr. The coarse grid overstates the e-folding time by 5-20 %. SCS2 called this
  NO VERDICT, correctly.
- **SCS2 placed the strongest growth at the null of the total field.** It is on the null's flank (about 40 degrees off the
  axis): at the null itself u -> 0 and the local rate vanishes (Lean growth_zero_at_null), even where |D.P| is largest.
- **SCS2's isolated-disc STABLE excludes the masked centre** (above). Neither file is edited.

## Disclosures

- **A1** (post hoc, after the frozen R0-R3 axial maps):
  - Seen first: at R3, on 11 of 32 axial backgrounds, route L's maximum sat on the inner-boundary artefact (r ~ 1e-5 r_e,
    e-folding 3-26 Myr), past the frozen 20-shell mask.
  - A1 adds a radial mask at R0's edge (about 0.010 R_d) and axial R4-R5.
  - A diagnostic R5 solve of one background with the frozen mask was seen before A1.
- **A2** (post hoc, after the frozen and A1 in-plane maps):
  - Seen first: the in-plane maximum sat in the 3D grid's polar-axis cells (first theta row and phi cell), with Gamma_L^2
    rising about 70 % per refinement. That is the coordinate singularity, three to four times faster than the far-field
    closed form allows there.
  - A2 excludes that row and adds in-plane R2 (direct solver if under 4 GB, else CG).
- **A3** (post hoc):
  - The frozen-solver R2 probe was killed at 5.97 GB.
  - CG with SuperLU's incomplete LU diverged: the factor is not symmetric.
  - A3 replaces it with the same exact LU under the MMD_AT_PLUS_A ordering, one process at a time, 7 GB kill line. The
    peak was 5.2 GB.
- **A4** (post hoc, after the first label pass): KA3 had failed as frozen; A4 removes the flat clause, judges the
  cell-quantised inner radius against two finest cells, and adds axial R6. All four amendments are post hoc; their readings
  are reported after the frozen one, which stays first.
- **Count slip in the criteria:** KA1 says "16 isolated primaries per footing"; there are 8 per footing (16 in all).
- **The frozen route-2 run** at R0-R3 was stopped by SIGTERM after KA3 had failed (its R3 rows on the artefact backgrounds
  took 550 s each and could change no label). Its partial rows are kept; R0 was rerun alone for KA2 (scs3_route2_AX_R0.json).
- **Route 2 at R5** (A1) was tried on four axial backgrounds: 5.4-7.1 GB peak, above the 4 GB line. The rows are kept and
  dropped by scs3_labels.py, and the run was stopped.
- **The thick twin at 0.01 a0** finds no negative cell by the frozen threshold (1e-6 of max |D.P|). The disc-centre values
  set max |D.P| about 1e7 times the halo's. So its inner radius is empty and those rows are NO VERDICT on that item; its
  rates are the razor-thin family's to <1 %.
- **The point-mass check and the 0.01 a0 domain check** were added after the A4 label pass. They are reported, not graded.
- **Resources:** at most three heavy processes at once, single-threaded BLAS. The largest process was an in-plane R2 solve
  at 5.2 GB. Solver caches are in the scratchpad, not the repo. Nothing was downloaded.

## Files

- **Criteria and amendments:** FROZEN_CRITERIA.md, AMENDMENT_A1.md to AMENDMENT_A4.md.
- **Copied from SCS2, unedited:** scs2_aqual.py and scs2_route2_copy.py. scs3_route2.py executes the copy's function
  definitions; nothing is imported from SCS2's folder.
- **Maps:** scs3_maps.py -> scs3_maps_{AX, AX_A1_p0/p1, AX_A4, PL, PL_A1, PL_A2, PL_A2_mmd, THICK_AX(_A1, _A4),
  THICK_PL(_A1, _A2), DOMAIN*}.json / .out.
- **Route 2:** scs3_route2.py -> scs3_route2_{AXKA_R0, AX_R0, AX_R0123_p0/p1 (stopped), AX_A1_R01234_p0/p1, AX_A1_R5_p*
  (over the line), PL_R01, PL_A1_R01, PL_A1_R2, THICK_*}.json / .out.
- **Checks:** scs3_swapcheck.py -> .json; scs3_pointmass.py -> .json / .out.
- **Labels:** scs3_labels.py -> scs3_labels.json / .out.
- **Lean:** SCS3.lean, SCS3_MUTATE.lean, compile.txt, compile_MUTATE.txt.

Not registered. Does not edit fable52_push/README.md, any PAPER72 file, the register, the decision files, or SCS1's / SCS2's
files.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
