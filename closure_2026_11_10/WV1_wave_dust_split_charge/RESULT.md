# WV1 RESULT: wave dust with a split charge (2026-11-10)

## Labels (per variant, per footing)

| Variant | canonical | alt |
|---|---|---|
| **V2** (separate frame, no dust term; Psi falls through it) | **STRUCTURE FAILS** (S1(c) FRW; S3(a) the frame focuses; S3(b) the law never appears) | **STRUCTURE FAILS** (same) |
| **V1** (frame = phase of Psi), under A1 + A2 | **STRUCTURE FAILS** (S3(b); the window [nu_min, nu_max] is empty) | **STRUCTURE FAILS** (same) |
| V1 as frozen | NO VERDICT (known answer KA4(ii) fails as frozen) | NO VERDICT |
| V1 under A1 only | NO VERDICT (the law-bracket runs at nu_max do not finish) | NO VERDICT |

S4 (static rows) is NOT GRADED for either variant. V2's label rests on neither amendment. Both of V1's amendments are
post hoc, each committed alone: A1 replaces a known answer whose observable was wrong, A2 grades four runs that cannot
finish on the outputs they reached. Under every reading, V1 also fails S3(c), but S3(c) does not decide the label,
because its MUTATE arm M4 did not bite (see the table). **The log M_b 10.7 runs are not part of this result.** The
coordinating session paused them with SIGSTOP (state intact) so that BX1's live box run could have the cores. That
leaves S3(a) at log M_b 10.7, its dx/2 convergence check, S3(c) at 10.7 and the 10.7 scan unevaluated. No label rests on
them: S3(b) and the empty window are decided at log M_b 9.4 alone, and these items could only add failing parts. As
landed, V1's S3(a) therefore reads NOT EVALUATED at 10.7 (no unresolved maxima at 9.4).

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled. The cold component is
cold dark energy, a field (Psi), never a particle.

## Answer in plain words

**The split cannot be made in an action.** The brief's premise (1) was that the law's phantom density D.P could appear
instantly, as in AQUAL, and not be a conserved charge. It fails in both variants, and the reason is the same: the law
reads the frame's acceleration, so D.P enters the frame field's own shift-symmetry current (sympy, exact).

- **V2: the separate frame carries D.P alone as its charge, and carries it along its own flow.** On FRW the charge is
  exactly 0, because there is no dust term and P = 0 by isotropy. Two failures follow:
  - **Health (S1(c)).** QG1's closed form gives omega^2 = G k^2 (b - a)/(a b) with G = 0, so omega^2 = 0 at every k and
    QG1's own code returns Lambda_s = 0 on both FRW rows. QG1's Minkowski failure moves to FRW. Giving the frame QG1's dust
    charge restores the pass (M2 bites). With khronometric beta and lambda added, the BPS speed is 0 at alpha = 2
    (ROOT note), so they do not help.
  - **The law never appears (S3(b)).** A frame that starts with zero charge keeps zero charge along its flow, and a
    regular frame with zero D.P has P_r = 0. So the frame never polarizes. In that limit it moves as zero-charge
    (mimetic) dust and focuses at COL1's time (S3(a)).
- **V1: Psi's U(1) charge is C = m|psi|^2 + D.P.** The law's halo is therefore paid for out of Psi's own charge. That
  is form B's "counted once" again, exactly, but now |psi|^2 >= 0 requires C >= D.P everywhere, which (A) never needed.
  X14's C5 objection returns: Psi's equation picks up -(i nu/2)(S/|psi|^2) psi, with S = D_t(D.P), which diverges at
  every node of the wave.
  - The P sector does not change Psi's Bernoulli equation (exact). So the frame's proper acceleration is A = -grad Q_qu:
    the law turns on only where quantum pressure holds Psi still.
  - The record's Jeans line (0.42/h Mpc at z = 1089) allows nu <= nu_max = 25.4 kpc km/s (m c^2 >= 7.6e-23 eV).
  - In the radial Schrodinger-Poisson collapses, Psi folds nowhere: its Lagrangian radii follow COL1's dust to 0.3 % up
    to 0.9 of the fold time, then the wave interferes. But Psi never becomes static. At log M_b 9.4 the static-frame radius is
    R_s = 0 at every scanned nu from 25 to 1.0e5 kpc km/s, in the primary run and in the law bracket, against 23 kpc
    (SPARC) and 81 kpc (KiDS) needed.
  - At nu_max the core is 0.32 kpc (r_c / r_ta = 0.002, against QX28's 0.15-0.26). The wave's frame acceleration is
    about 47 g inside r_ta (interference fringes), and the phantom charge it implies exceeds Psi's density on 70 % of
    Psi's mass (S3(c)).
  - Even with the frame forced static everywhere (M4), the law's own smooth phantom density exceeds Psi's local density
    on 26-27 % of the mass at nu_max. (An estimate of where: in the Newtonian regime the law's phantom density is
    a0/(2 pi G r), about 10 times the core's density at 0.3 kpc.) So V1 also lacks the local charge the law needs.
- **Does rho include the Psi dust?** Yes, in both variants. The static reduction is exactly
  div[mu(|grad Phi|/a0) grad Phi] = 4 pi G (rho_b + m|psi|^2) (S0). In V2, Psi therefore sits *inside* the law (the law
  multiplies its mass): that is QX7/QX10's form, not form B's. In V1 the gravitating cold density is the U(1) charge
  C = m|psi|^2 + D.P, which is form B's "counted once" (the halo is Psi's charge, converted).

**What this says about the route (a reading, not a label).** In any diffeomorphism-invariant action in which the law is
a function of a frame's acceleration and matter couples to g alone, D.P is part of the frame's conserved current; V1
and V2 are two instances, computed. For an aether frame in spherical symmetry the same holds, because every spherical
unit timelike vector is hypersurface-orthogonal and the aether's equations then imply the khronon's (argued, not
computed). A law whose phantom density "appears instantly" therefore needs matter coupled to the frame field (the
RAQUAL / TeVeS family), which is outside this lane's brief and the record's E5.

## The parent action (as frozen)

Units c = 1, K = 4 pi G, nu = hbar/m:

    S = Int sqrt(-g) { (R - 2 Lambda)/(4K) + P^m A_m[n] - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m
                       - (hbar^2/2m) [ g^{mn} d_m Psi* d_n Psi + (m/hbar)^2 |Psi|^2 ] } + S_m[g]

with W(p) = (a0^2/K)[-p/a0 - ln(1 - p/a0)], Pi = D_m P^m, F = the adopted Pi^6 blend, A_m = n^r nabla_r n_m,
n_m = -d_m tau/Q. This is QX17's (A) with K(Q) removed and a minimally coupled complex field added.
- **V1:** tau = -(hbar/m) arg Psi.
- **V2:** tau is an independent khronon, with no dust term.

Non-relativistic form (graded symbolically): L = -rho nu theta_t - rho nu^2 |grad theta|^2/2 - nu^2 |grad sqrt rho|^2/2
- rho Phi - |grad Phi|^2/(8 pi G) - rho_b Phi + P.A - W - gamma F(div P), where
A = grad(Phi + nu theta_t + nu^2 |grad theta|^2/2) in V1 and A = grad(Phi - chi_t + |grad chi|^2/2) in V2.

## Table (canonical; alt in brackets where it differs)

| item | verdict | numbers |
|---|---|---|
| S0 static reduction, both variants | **PASS** (exact) | the P equation is (A)'s E2 with Pi_+ -> F'(Pi); Poisson lap Phi = 4 pi G (rho_b + m f^2 + div P); together div[mu grad Phi] = 4 pi G (rho_b + m f^2), mu = x/(1+x); V1's phase equation is identically satisfied and f obeys the stationary Schrodinger equation in the total Phi; A = grad Phi. Every residual 0 (`wv1_sym.out`) |
| S1b V1 charge | exact | EL(theta) = nu [d_t C + div(C v)], C = m|psi|^2 + div P; Bernoulli unchanged by the P sector (residual 0) |
| S1b V2 charge | exact | EL(chi) = -[d_t D + div(D u_f)], D = div P, u_f = -grad chi; Psi's own charge m|psi|^2 is separate (residual 0) |
| S1(c) FRW, V2 | **FAIL** both rows, both footings | omega^2 = 0 at every k on both branches; QG1 grade_row Lambda_s L = 0 (FRW1100 and FRW1) |
| S1(c) FRW, V1 | **PASS** both rows, both footings | omega^2 = (nu^2 k^4/4)/(1 + cY q^4) - 4 pi G rho (sympy; equals QG1's form with mu^2 -> k_J^4/k^2); no ghost; max growth rate / sqrt(4 pi G rho) = 1.000000000000; no rate rising with k; at nu_max x 1 ... 4096 |
| V1 off branch (no screening) | exact | omega^2 = -4 pi G rho/(1 + q^4) at every k: the alpha = 2 P sector cancels the quantum pressure; at k_J the growth rate is half the pressureless rate (Lean `v1_offbranch_negative`) |
| S1(d) static galaxy | PASS (both variants, both footings) | QG1's point-mass rows re-run through its code: Lambda_s L 1.09e12 / 3.14e12 / 1.40e13 (alt 1.12e12 / 3.24e12 / 1.44e13) |
| S1(e) V1's psi equation | exact | i nu psi_t = H psi - (i nu/2)(S/|psi|^2) psi, with S = d_t(div P) + div((div P) v) |
| S2 nu_max | 25.37 [25.38] kpc km/s | by redshift: z 3: 418.8, z 10: 252.6, z 100: 83.35, z 1089: **25.37**; m c^2 >= 7.556e-23 [7.554e-23] eV; k_J(z 1089) = 10.1/Mpc (acoustic peaks, k <= 0.3/Mpc, kept off); k_J today 57.9/Mpc |
| S3(a) V1 fold-free | log M_b 9.4: no unresolved maxima; 10.7: **not evaluated** (runs paused) | Psi's Lagrangian radii follow COL1's dust to 3.1e-3 up to 0.9 t_f, and the focus is regularized at the de Broglie scale; at nu_max (law off) 0 narrow maxima at log M_b 9.4; the 10.7 runs and the dx/2 convergence run were paused before finishing |
| S3(a) V2 | **FAIL** | the zero-charge frame is mimetic and focuses at COL1's time: 0.07116 / 0.15333 Gyr after z 10 (log M_b 10.7 / 9.4) |
| S3(b) V2 | **FAIL** | reach 0 (exact identity + Lean `advected_zero`, `regular_centre_zero`) |
| **S3(b) V1** (A1 + A2) | **FAIL** | log M_b 9.4: R_s = 0 kpc (needs >= 81 and >= 23) at nu_max, law off over the last-Gyr set and the bracket at z 2, 1, 0.5 (A2) |
| **window [nu_min, nu_max]** | **EMPTY** | R_s = 0 at log M_b 9.4 at every scanned nu (25.4, 101.5, 406, 1624, 6495, 2.60e4, 1.04e5 kpc km/s), law off and bracket, both footings: nu_min does not exist |
| S3(c) V1 | FAIL, **not decisive** (M4 did not bite) | fraction of Psi's mass inside r_ta with D.P > m n: 0.700 [0.697] at nu_max, log M_b 9.4; median |A|/g inside r_ta = 47; M4 (A -> dPhi/dr): 0.272 [0.264] |
| S3(d) reported | - | nu_max, log M_b 9.4, law off: r_ta(z 0) = 155.7 kpc, r_c = 0.32 kpc, r_c/r_ta = 0.002 (QX28 needs 0.15-0.26). Larger nu: r_c 1.3 / 8.4 kpc at x4 / x16; from x64 up, Psi no longer collapses without the law. With the bracket: r_ta 0.2 to 1.2 Mpc and r_c 0.4 to 2200 kpc, never static |
| S4 | NOT GRADED | - |

Known answers: KA1 (X14's C5: omega^2 = nu^2 k^4/4 - 4 pi G rho) PASS; KA2 (QX17's static law) PASS; KA3 (QG1 re-run
through its own functions: FRW1100 334.0 / 316.5, FRW1 1.838e5 / 1.742e5, PM rows PASS, mu_K = 0 FRW Lambda_s = 0) PASS;
KA4(i) (COL1's focus time 0.0712 / 0.1533 Gyr reproduced: 0.07116 / 0.15333) PASS; **KA4(ii) FAILS as frozen** (the
central-density maximum sits at the run's end, 0.118 Gyr, +66 %, because shells from outside the core keep arriving;
AMENDMENT_A1); KA4(ii') under A1 PASS (worst 3.1e-3); KA5 (soliton G M r_1/2 / nu^2 = 3.920 against 3.925) PASS; KA6
(LFS1 / COL1 charge N = mu^2 h/K + div P reproduced with a dust term) PASS; KA7 (QX28's SPARC) not run (S4 not graded).

MUTATE: M1 (frame decoupled from Psi's phase: charge m|psi|^2 alone) BITES; M2 (V2's frame given QG1's dust) BITES;
M3 (static forced everywhere) BITES; **M4 (A -> dPhi/dr) DOES NOT BITE** (0.264-0.272 > 0.01 at nu_max: the smooth
law's own phantom exceeds Psi's density), so S3(c) is reported, not decisive; M5 (nu x 10 on KA4's run: peak central density
140 x lower) BITES. Lean: `WV1.lean` 9 theorems, exit 0, standard axioms only (`compile.txt`); `WV1_MUTATE.lean` fails
on all 8 false statements (`compile_MUTATE.txt`, 9 errors, exit 1).

## Added after landing: the coordinator's four requests (post hoc, reported; no label moves)

Requested by the coordinating session after the result landed. It pointed at three inputs: `MEDIUM_DESIGN_2026-11-10.md`
(origin c39b1272f1), SHP1 (`fable52_push/SHP1_cold_component_shape/`) and PAR1
(`closure_2026_11_10/PAR1_parent_action_spec/`, origin 6be0bf30d1). All three were read only. Per the coordinator's
scope note, no member of PAR1's branch B-Tm-smooth is built or graded here; that branch is lane SMF1's.

### P1. SHP1's shape measurement against a cored Psi halo (`wv1_shp1_row.py`, `.out`, `.json`)

The question: is a cored Psi halo at R_TF = 0.15-0.26 r_ta, holding the share, excluded by SHP1, or within it?
- **Method.** SHP1's own data and statistics, loaded through its own script (its SPARC loader copied with r kept; the
  copy reproduces SHP1's 2700 points exactly).
- **The rows.** SPARC is SHP1's R1 (bin medians, line 0.10 dex). KiDS is SHP1's R2 (B21's isolated lenses, full
  covariance; lens radii at log M_b 10.45, as SHP1's R4).
- **The halo.** All of S M_b inside R_TF, either uniform (the least centrally concentrated core) or the n = 1
  Thomas-Fermi shape.
- **Psi inside the law** is WV1's coupling in both variants (S0). **Psi outside the law** is QX28's coupling, run for
  contrast.

| share, R_TF, shape | SPARC worst bin, Psi inside the law (canonical / alt; line 0.10) | KiDS published chi^2 / 15, inside the law (law alone: 194 / 133) | same, outside the law (QX28's coupling) | KiDS hot-gas chi^2 / 15, inside (law alone: 346 / 395) |
|---|---|---|---|---|
| 5.41, 0.15 r_ta, uniform | 0.132 / 0.212 **FAIL** | 1292 / 1835 | 176 / 163 | 5133 / 6657 |
| 5.41, 0.15 r_ta, TF n = 1 | 0.247 / 0.330 **FAIL** | 1430 / 2000 | 216 / 208 | 5273 / 6825 |
| 5.41, 0.26 r_ta, uniform | 0.031 / 0.080 within | 861 / 1289 | 116 / 85 | 4657 / 6056 |
| 5.41, 0.26 r_ta, TF n = 1 | 0.076 / 0.158 within / **FAIL** | 1016 / 1493 | 130 / 106 | 4832 / 6284 |

The share 5.562 (QX28's R) moves every number by at most 0.005 dex and under 7 % in chi^2 (`.out`).

**Reading.**
- **With Psi inside the law, as WV1's action puts it, the cored halo is excluded by SHP1's KiDS measurement on both
  footings and at both radii.** At KiDS radii the whole share is enclosed, and the law multiplies it. The prediction
  sits 1.25 to 2.9 times the law of the baryons, against the measured 1.40 +- 0.03 (published) and 0.91 (hot gas).
- At 0.15 r_ta it is also excluded by SPARC's shape. At 0.26 r_ta, SPARC alone allows the uniform core on both footings
  and the Thomas-Fermi core on canonical only.
- **QX28's pass does not carry over.** QX28 kept the condensate outside the law, a Newtonian add-on. In that coupling
  SHP1's data allow it: KiDS published chi^2 85-216, against 194 / 133 for the law alone. That matches SHP1's R4, which
  allows the record's own share of 5.56 M_b as a separate halo.
- **V1's only way out is counting.** Its unconverted remainder S_rem sits inside the law and lifts the deep ratio to
  sqrt(1 + S_rem). SHP1's mean + 2 sigma allows S_rem <= 1.16 / 0.80 (published) and none with hot gas. So at least
  79 % / 85 % of the 5.41 (all of it, with hot gas) must have turned into the law's phantom. That is form B, not a
  second halo beside the law.
- The MEDIUM_DESIGN property "no second halo beside the law" therefore holds against WV1's coupling. It says nothing
  against QX28's coupling, where SHP1's R4 leaves room.

### P2. V1 against PAR1's branch B-Tm-fine and its C15

PAR1 puts V1 in B-Tm-fine and leaves that branch open for m in [4.20e-24, 1.84e-23] eV (canonical; alt up to 1.93e-23).
- **Its lower edge uses only the record's forest line at z = 3.** WV1's frozen S2 applies the record's line at all four
  of QX28's frozen redshifts, 3, 10, 100 and 1089 (G6c and G6a). The binding one is z = 1089:
  - m c^2 >= 7.556e-23 / 7.554e-23 eV.
  - That is 4.1 / 3.9 times above PAR1's upper edge, so on WV1's frozen line set the window is empty with no published
    forest bound needed.
  - Caveat: G6a's z = 1089 line (0.42/h Mpc) is stricter than the acoustic-peak scale. With k <= 0.3/Mpc alone at
    z = 1089, the bound would fall to about 7e-26 eV.
  - WV1's z = 3 value alone is 4.58e-24 eV, against PAR1's 4.20e-24 eV. The 8 % difference is a definition: WV1 uses
    the wave's own Jeans wavenumber, PAR1 converts through a sound speed.
- **WV1 computed what PAR1's C15 estimates.** In the collapse runs at log M_b 9.4, at m = 4.72e-24 eV (inside PAR1's
  window) and at 1.89e-23 eV (inside alt's window, just above canonical's):
  - The static-frame radius is R_s = 0 at every last-Gyr output, law off and bracket, both footings.
  - Inside r_ta the frame's acceleration has median |A| = 2.4 / 8.8 times g (law off), while |A| = 0.003 to 0.011 a0.
  - C15 at log M_b 9.4 allows m up to 2.45e-22 eV, so this closes what C15 leaves open there. At log M_b 10.45 to 10.9
    WV1's S2 bound already exceeds C15's ceilings (4.0e-23 to 1.84e-23).
- **What binds is not C15's mechanism.** C15 has the fine-grained noise halve the mean polarization once it reaches
  about a0. In the runs the noise stays well below a0, where the law is linear in A, so it averages out of the mean.
  - What fails instead is local positivity. In V1, m|psi|^2 = C - D.P has to stay >= 0 in every cell.
  - The noise's phantom charge D.P exceeds Psi's density on 74-76 % of Psi's mass inside r_ta (S3(c) at those nu), and
    on 70 % at nu_max.
  - C15's mean-field estimate does not test this condition. It is X14's C5 objection, made quantitative.

### P3. V2 against PAR1's branch B0

**Agreed: V2 is in PAR1's closed branch B0, and WV1's results reproduce both of PAR1's grounds.**
- **Counted twice (Lemma 0 x Pi3).** V2's phantom is the frame's own polarization charge. Psi's dust is a separate
  conserved mass that the law sources: S0, exact; S1b's V2 identity. P1 shows the data cost of that double count:
  KiDS chi^2 861-2097 / 15.
- **C1: neutral halo, frozen.** S1b (exact) and S3(b) give the same statement in its dynamic form: the frame's charge
  is advected from zero, so it never polarizes.
- **What WV1 adds to B0.** The health failure on FRW: QG1's own code gives Lambda_s = 0 with the frame uncharged. That
  is PAR1's section 3, item 3 ("the frame must also carry charge on FRW") as a graded row.
- **Constants and structure.** V2 adds one constant beyond (A) (nu = hbar/m; it drops mu_K). It has none of
  B-Tm-smooth's structure: no charge exchange, no alignment to Psi's current, no length ell. So it is not a member of
  that branch, and it is not counted against PAR1's at least two new constants. Per the scope note, no B-Tm-smooth
  member was built here.

### P4. M5 (MEDIUM_DESIGN section 2; PAR1's C16)

**M5 does not apply to WV1.** Its hypothesis is a local, momentum-conserving medium whose own equilibrium is the law,
for every baryon profile. In WV1 the law is not Psi's equilibrium:
- The law is the P sector's response to the frame's acceleration.
- Psi's own static states are Schrodinger states, for example the soliton.
- In V1, Psi's flow obeys the plain Madelung-Euler equation in the total potential (S1b, exact). So nothing makes Psi
  settle into the law's shape.

That is exactly why V1 fails: Psi is not static where the law is seen, so it is not M5's mechanism. V2 fails on the
frame's charge, not on M5.

## Corrections and disclosures

- Two solver bugs were found and fixed in development, before any production run: the KA5 integral used a left Riemann
  sum, and the potential's zero point at the outer boundary injected junk waves (false turnaround radii, spurious narrow
  maxima). Neither touched a frozen threshold.
- A2's parenthesis swaps the footings: the narrow-maxima counts at z = 0.5 are 35 (canonical) and 19 (alt).
- The four production runs at log M_b 10.7, nu_max were stopped once by the lead (SIGTERM, checkpointed) so that they
  record the central-density history the S3(a) convergence check needs. They resumed from their checkpoints.
- QG1's script was executed unmodified in a temporary directory. Its output files went there, not into QG1's folder.
- **The log M_b 10.7 runs were paused, not finished.** The coordinating session suspended all seven running
  `wv1_s3.py --mass 10.7` processes with SIGSTOP (11-10, about 21:00): the four at nu_max (two law off, two at dx/2 to
  z 2) and three at nu_max x 4. It did so because BX1's 512^3 box run, PAPER72 v1.1's last pending row, was starved of
  cores, and the owner's rule is no heavy compute beside a live box run. Nothing was killed. The runs checkpoint by wall
  time only, so a pause cannot change their results. They may be resumed (`kill -CONT`) once the box run has exited, and
  their rows added in a later commit. Every 10.7 number in this file comes from outputs finished before the pause: the
  two A2 bracket partials and the z = 2 output of the law-off runs, taken from their checkpoints: R_s = 0,
  r_ta = 140.6 kpc and no unresolved maxima (0 of 5697), on both footings.

## Files

`FROZEN_CRITERIA.md`; `AMENDMENT_A1.md`; `AMENDMENT_A2.md`; `wv1_sym.py` (S0, S1b, S1e, dispersions, KA1, KA2, KA6;
MUTATE M1); `wv1_s1s2.py` (S1c, S1d, S2, KA3, M2); `wv1_sp_lib.py` (solver); `wv1_ka.py` (KA4, KA5, M5); `wv1_s3.py`
(one collapse run, preemptible); `wv1_partial.py` (A2); `wv1_shp1_row.py` (post hoc row P1); `wv1_s3_grade.py` (S3, M3, M4, labels) with outputs `*.out` and
`*.json`; `runs/` (one JSON and one compressed profile file per run); `WV1.lean`, `WV1_MUTATE.lean`, `compile*.txt`.
Re-run: `python3 wv1_sym.py; python3 wv1_s1s2.py; python3 wv1_ka.py; python3 wv1_s3.py --mass M --fac F --footing FO
[--law]` (about 5 min at log M_b 9.4, nu_max; one to several hours at 10.7, nu_max); `python3 wv1_s3_grade.py`.

## Commits (local / origin)

- criteria 174870d2fe / 3fc79b5800 (alone, before any script or number)
- A1 589c2738df / 90ebdb2e5c (alone, post hoc)
- A2 022897766a / 45a1c9776d (alone, post hoc)
- result 88f3ccbe4b / fb421c3adb

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
