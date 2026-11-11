# PAR1 RESULT: the parent action as an inverse problem (2026-11-10)

**Label, canonical and alt: NO VERDICT / NO VERDICT**, as frozen and under AMENDMENT A1 (post hoc). Every known answer
passes, every MUTATE arm bites, and the Lean file compiles. The label is NO VERDICT because two branches stay open and
no member of them was written and graded here.

**Answer.** No parent action built from one single-valued carrier exists. That is a theorem (branch B-Ts, EMPTY under
A1), and with branches B0 and B-L it closes every parent whose cold dark energy is a single-valued field. Any parent that
works everywhere and gives (A)'s law in galaxies must carry the cold dark energy on a **multi-valued field** (a wave
field that can multi-stream). Two versions are left:

- **Law keyed on the wave's own phase frame** (B-Tm-fine; WV1's variant V1 is in it). It survives only for a wave mass
  between **4.2e-24 and 1.84e-23 eV** (canonical; alt to 1.93e-23). The record's own forest line is too weak to close
  that window. Published forest bounds (2e-21 eV and up, PROVISIONAL, not graded) would close it by 8 to 109 times.
- **Law on a separate smooth frame that follows the wave's coarse-grained mean flow** (B-Tm-smooth). Nothing here
  closes it. Its minimal structure is fixed by the spec (section 3): a second field, a charge exchange, and a new
  length. It needs at least two new constants beyond the wave mass, and nothing in the record fixes them.

**The theorem that closes the single-valued class.** It is a pair of conditions:

1. Cold dark energy must be cold on the web. The record's forest line gives c_s <= 9.2 km/s at z = 3.
2. It must stand still in galaxy wells. Their depth is at least 120 km/s squared at 10 kpc.

These conflict for every equation of state:
- **S7 (exact).** A static state deeper than c_s^2/2 needs the equation of state to stiffen with compression somewhere
  between the web's density and the well's (P''(tau) > 0).
- **S8 (exact).** Cold infall that crosses that stiffening either steepens into a jump whose energy flux is not
  conserved: +(m/12) P''(tau)(Delta tau)^3, which no single-valued variational field continues.
- **S5 (exact), S3 (exact), S10 (computed).** Or the infall meets no pressure at its own scale, because the law's
  polarization screens pressure above the carrier's Jeans wavenumber, and it folds.

Margin: the shallowest graded well is 340 / 372 times (canonical / alt) deeper than c_s^2/2.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled; a0 enters S9, S15
and the well depths. Cold dark energy is a gravitating field, never a particle.

## 1. The spec: necessary conditions on any parent

Each condition is a theorem with its hypotheses. "Exact" means sympy residual 0 (`par1_spec.out`); "Lean" means a
compiled algebraic core (`PAR1.lean`); "read" means quoted from the lane, not recomputed.

| # | condition (hypotheses -> statement) | source | status |
|---|---|---|---|
| C1 | A phantom that is the leaf divergence of a polarization and the charge of a current conserved along a single-valued flow has zero net charge in any region bounded where P = 0. With spherical symmetry and zero shift, Y = sqrt(gamma) P^r is frozen, so a static halo cannot grow | LFS1 S1(a), (c), (d) | **known answer reproduced**: residuals 0 (3D generic, with shift) |
| C2 | One fixed length (mass term 1/mu) cannot serve KiDS hosts (mu <= 0.063 per Mpc) and the lensing web (mu >= 10 per Mpc). Bound H-inf: mu R <= 12.3 | EW2 | **known answer reproduced**: 12.288; gap 158.7. The same structure for a sound horizon or a Jeans length is argued, not recomputed |
| C3 | A zero-charge cold stream crossing a mass sheet folds at tau_f = w/(K Sigma_b) | X14 F2 | **known answer reproduced**: residual 0 |
| C4 | Quadratic dust term: the clock's self-growth around free fall is K nbar/(1 + k^2/mu_K^2) | TPA1, COL1 | **known answer reproduced**: residual 0 |
| C5 | **T-SCR (new, exact).** Any dust term P(h) with susceptibility chi = dn/dh >= 0, plus the law's J with J''(0) = 1/K (forced by deep MOND; ROOT note). Around free fall, omega^2 = -K nbar K chi/(K chi + k^2). There is no restoring force at any k, and pressure is screened above k_J. The screening scale is the carrier's Jeans scale, k_J^2 = K chi, and chi is also the static well's dust per unit depth. With a background field, omega^2 = -K nbar (K chi + (eps_r - 1) k^2)/(K chi + eps_r k^2), which tends to K nbar (1/eps_r - 1) at high k | new; generalizes C4 | exact (derived from the reduced Lagrangian, charge conservation checked); Lean `scr_nonpos`, `scr_identity`; MU1 bites |
| C6 | **T-DEP (new, exact).** For any dust term, the static dust is n_d = P'(hbar + DeltaPhi). It is one function of the well depth, the same in every galaxy, group and cluster | new; generalizes MK1 | exact |
| C7 | **T-SPAN (new, exact).** If n^2 c_s^2 does not increase on the compression path, then h - hbar <= cbar^2/2. The bound is attained by the Chaplygin P = -A/n. So a static state deeper than cbar^2/2 needs a point with P''(tau) = n^2 d(n^2 c_s^2)/dn > 0 | new | exact; Lean `span_lt`; MU3 bites (a convex EOS reaches 18 times the bound) |
| C8 | **T-SHK (new, exact; sign per A1).** A barotropic jump that conserves charge and momentum has energy-flux jump +(m/12) P''(tau)(Delta tau)^3 + O(Delta tau^4). For a quadratic P(tau) this is exact. It is negative for a compressive jump (dissipation; Landau-Lifshitz's weak shock). Wherever P''(tau) != 0 the jump cannot conserve charge, momentum and energy together | new | exact; Lean `shock_defect`; MU2 bites (Chaplygin: 0) |
| C9 | **T-TRI numbers.** The record's forest line (comoving Jeans length <= 0.42/h Mpc at z 3; QX28 G6c) gives cbar <= 9.20 km/s, so cbar^2/2 = 42.3 (km/s)^2. Galaxy wells from 10 kpc to R_ta, Plummer baryons with the law: sqrt(depth) = 120 / 260 / 314 / 364 km/s (canonical; alt 126 / 272 / 327 / 379) at log M_b 9.4 / 10.45 / 10.7 / 10.9 | new | line met: every well is at least 340 / 372 times deeper |
| C10 | A single-stream clock folds at first infall (centre, 0.06 to 0.15 Gyr, every mu_K). Caustics are generic, and every completion needs a new scale | COL1, X14 | read |
| C11 | The KiDS inner / middle window edges (272 / 362 / 456 and 637 / 849 / 1069 kpc) lie beyond R_ta(z 0) (268 / 325 / 378 kpc). A static clock region ends inside R_ta | FLD1, LFS1 A3 | read |
| C12 | No dust stiffness keyed on the offset (MK1), on one sound speed (MK2), on theta (TK1) or on A (AKD1). The law cannot use matter's acceleration (REL1: fourth order) | those lanes | read; REL1's runaway root reproduced (residual 0; Lean `rel1_root_pos`) |
| C13 | (A) has no cluster state and no dispersion support (CLS1). No held wall (HE1, SWT1), and law-on filling is at most 0.0231 (Lean `mg_bound`). A dust lump in galaxies wrecks discs, and X-COP sits between Newtonian (1+R) M_b (+0.12) and law plus full share (-0.21) (QX28, HY1) | those lanes | read |
| C14 | Data: KiDS-Legacy consistent at 1.71 / 1.88 widths (KL1, post hoc). X-COP at the ceiling (XCV1, post hoc). Hosted dwarfs high, but the FAILS do not survive the budget (RB2, DG1) | those lanes | read |
| C15 | **T-GR (new, estimate).** Take a wave carrier with the law keyed on its fine-grained frame. In multi-stream regions the frame's acceleration fluctuates by about sigma^2/lambda_dB. In an isotropic Gaussian model the mean polarization along g halves at s = 1.04 a0 (g = 0.1 a0), 1.38 a0 (0.3) and 2.55 a0 (1). So the law holds only where lambda_dB >= sigma^2/(s_half a0): 0.9 to 5.2 kpc. That needs m <= 2.45e-22 / 4.00e-23 / 2.60e-23 / 1.84e-23 eV (canonical; alt 2.57e-22 to 1.93e-23). The record's forest line asks only m >= 4.20e-24 eV | new | numbers (10^6 samples, seed 1); MU4 bites (no fluctuation: R = 1) |

Lemma 0 (exact): on FRW the leaves carry no gradient, so P = 0 and the charge is P'(h) alone. Under counted once and
cosmology, the 5.41 is a dust state of the carrier that becomes phantom in galaxies. So the law has to be keyed on the
carrier's state.

## 2. The class and its branches

The class Pi has four conditions:
- **Pi1.** A local, variational action that obeys the equivalence principle, with matter second order.
- **Pi2.** The static galaxy limit is (A)'s law with v3s screening, and the phantom lenses.
- **Pi3.** Counted once (form B).
- **Pi4.** The cold dark energy is cold dust on FRW at 5.41 Omega_b.

| branch | what it is | label (A1; frozen in brackets where it differs) | the conflicting pair |
|---|---|---|---|
| B0 | the law is not keyed on the carrier's state (sourced by matter or by an independent field) | **EMPTY** | Lemma 0 (the FRW phantom is zero, so the 5.41 must turn into phantom) x Pi3 with route C's uniqueness (SHAPE_search: one conserved medium coupled by gravity only has (A)'s Lagrangian; contact coupling gives a phonon force that does not lens, i.e. counted twice) |
| B-L | the law region is set by a fixed length (mass term, sound horizon, Jeans length) | **EMPTY** | C2: KiDS hosts x the lensing web (factor 159). The mass-term case is EW2's; the others are argued |
| B-Ts | a cold, single-valued, barotropic carrier, i.e. (A) plus any dust term: route C's class | **EMPTY** [frozen: OPEN, because C8's frozen sign line fails] | late-time coldness (C9) x a static state reached by a classical solution: C7 forces a convex point; crossing it ends in a jump with an energy defect (C8) or, where the law screens pressure (C5), in a fold (C3, C10) |
| B-Tm-fine | a multi-valued wave carrier with the law on its own phase frame | **OPEN** | not closed: C15 leaves m in [4.2e-24, 1.84e-23] eV. It closes only under published forest bounds (PROVISIONAL) |
| B-Tm-smooth | a multi-valued carrier plus a separate smooth law frame that follows its coarse-grained mean flow | **OPEN** | no theorem found; minimal structure in section 3 |

Hypotheses behind B-Ts, stated plainly:
- The steepening step uses Lax's 1964 breakdown theorem for a compressive simple wave in a genuinely nonlinear region.
  It is a planar statement and a PROVISIONAL citation.
- Where the law's high-k restoring frequency is nonzero (eps_r < 1), the steepened front could be a dispersive bore
  instead of a jump. For the Mach numbers here (cbar <= 9 km/s against infall of 100 km/s and more) such bores break,
  which means trajectories cross: a fold. This is argued from cold-plasma wave-breaking (Dawson 1959, PROVISIONAL), not
  computed.
- Spherical, three-dimensional infall is covered by COL1's computation for the quadratic term only.

## 3. What a parent must contain (the open branches)

From the spec, any parent that survives needs all of the following.

1. **A multi-valued cold field.** Folds must be passable (C3, C10) and clusters need dispersion support (C13, CLS1).
   The minimal choice is one complex field Psi with mass m and a conserved U(1) charge equal to the 5.41.
2. **A law frame that is static where the law is seen and comoving on the web.** The law acting on matter's
   acceleration is excluded (C12). A frame set by a length is excluded (B-L). The frame must therefore follow the cold
   field's state:
   - its fine-grained phase (B-Tm-fine, which needs the ultralight window of C15), or
   - its mean flow averaged over a length ell (B-Tm-smooth).
3. **For B-Tm-smooth, a separate single-valued frame tau.** It carries (A)'s P sector, a coupling that aligns it with
   Psi's current over ell, and a charge exchange between Psi's U(1) and the frame's polarization charge, with only the
   sum conserved. Without the exchange, C1 freezes the frame's halo and makes it neutral, and counted once fails
   (Lemma 0). The frame must also carry charge on FRW: with J''(0) = 1/K an uncharged frame has zero speed for every
   khronometric beta and lambda (ROOT note; QG1: "every charged background passes").
4. **A new length ell.** It must lie between Psi's de Broglie length and the smallest radius where the law is tested
   (about 1 kpc), and nothing in the record fixes it. Counting constants beyond (A)'s (kappa, the 5.41, L* and v3s's
   screening): m, ell (or a frame stiffness and an alignment coupling) and an exchange rate. That is at least three.
5. **KiDS's outer windows must be carried by non-static cold mass.** They lie beyond R_ta (C11), so the cold mass there
   is infalling Psi. KO1 does not separate that from the law. Any member must pass this as a data row; it is not graded
   here.

No member was written as a full action and graded here, so the lane label is NO VERDICT.

**WV1** (another session, read-only; its criteria 174870d2fe and A1 589c2738df were read, not its results):
- Its **V1** (the frame is Psi's phase) is in B-Tm-fine. Condition C15 is the one that decides it: the law survives in
  multi-stream regions only if m <= 1.8e-23 eV. Not duplicated here.
- Its **V2** (a separate khronon with no dust term, Psi not coupled to it) is in B0. This spec excludes it two ways:
  - By Lemma 0 and Pi3: the phantom is the frame's own polarization charge, not Psi's, and WV1's static reduction
    sources the law with rho_b + m f^2, so the wave dust sits inside the law and is counted twice.
  - By C1: the frame's charge is conserved along its own flow and is zero on FRW, so a halo bounded where P = 0 is
    neutral, and a static one cannot grow.

## 4. Table

| item | canonical | alt |
|---|---|---|
| KA S1 (LFS1), S2 (EW2), S3 (X14), S4 (TPA1/COL1), S12 (REL1) | 5 / 5 PASS | 5 / 5 PASS |
| MU1 (polarization charge dropped: Jeans support returns) | bites | bites |
| MU2 (Chaplygin: no energy defect) | bites | bites |
| MU3 (convex EOS: span 18 x the bound) | bites | bites |
| MU4 (no fluctuation: R = 1) | bites | bites |
| Lean `PAR1.lean` | exit 0, 8 theorems, standard axioms | |
| Lean twin `PAR1_MUTATE.lean` | exit 1, 5 of 5 false statements fail | |
| C5 T-SCR, C6 T-DEP, C7 T-SPAN | exact | exact |
| C8 T-SHK | as frozen FAIL (sign); A1 exact | same |
| C9 line, depth at 10 kpc > cbar^2/2 at every mass | PASS (min ratio 340) | PASS (372) |
| C9 bracket, GRW1's 300 km/s edge (reported) | deeper at 10.45 to 10.9, not at 9.4 | same |
| C15 | m window [4.20e-24, 1.84e-23] eV, OPEN | [4.20e-24, 1.93e-23], OPEN |
| Label as frozen | NO VERDICT (B0, B-L EMPTY; B-Ts, B-Tm OPEN) | same |
| Label under A1 (post hoc) | **NO VERDICT** (B0, B-L, B-Ts EMPTY; B-Tm-fine, B-Tm-smooth OPEN) | same |

## 5. Disclosures

- **AMENDMENT A1 (post hoc, committed alone before grading).** C8's frozen statement had the sign slip "-(m/12)". The
  series gives +(m/12) P''(tau)(Delta tau)^3, and the hand algebra for a quadratic P gives exactly b Delta^3/12. As
  frozen, C8's residual line fails and B-Ts is OPEN. Under A1 it is EMPTY. The conclusion C8 is used for (the defect is
  nonzero wherever P''(tau) != 0) holds with either sign.
- **Two reporting bugs, fixed before grading.**
  - A symbol with different assumptions printed "b/12 - b/12" for a zero residual.
  - C15's 2 pi bracket divided where it should multiply. The bracket makes coherence stricter, so the gap grows by
    2 pi. It is still below 3, so the branch stays OPEN.
- **The first run of `par1_spec.py` stalled** in a symbolic simplification of the explicit log-form J. J is now generic
  in the conservation check; the physical J enters through its derivative and J''(0), each checked separately. No
  graded number came from the stalled run.
- **C15 is an estimate**, not a theorem: the fluctuation scale sigma^2/lambda_dB has prefactor 1 (the 2 pi bracket is
  reported), and the Gaussian model is isotropic.
- **Published wave-dust forest bounds are PROVISIONAL**, quoted from memory and not fetched: m > 2e-21 eV (Irsic+ 2017)
  and stronger later. They are reported only and decide nothing here.
- **Cosmology constants** (h 0.674, omega_b 0.02237, share 5.41) enter only cbar and m_min. The margins (340 times;
  the window's width) do not turn on them.
- **R_ta** comes from FLD1's canonical z 0 table and is used on both footings, as LFS1 did (alt within 0.5 %).

## Files and re-run

- `FROZEN_CRITERIA.md` (alone, first); `AMENDMENT_A1.md` (alone, post hoc).
- `par1_spec.py` -> `par1_spec.out/.json` (C1 to C8, C12's root, Lemma 0; about 1 s). MUTATE:
  `PAR1_MUTATE=MU1|MU2|MU3 python3 par1_spec.py`.
- `par1_numbers.py` -> `par1_numbers.out/.json` (C9, C15; about 2 s). MUTATE: `PAR1_MUTATE=MU4`.
- `par1_grade.py` -> `par1_grade.out/.json`.
- `PAR1.lean`, `PAR1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`. Compile with
  `cd fable_independent_2026/lean_2026 && lake env lean <file>`.

Commits (local / origin): criteria 51522963e0 / ORIGIN_CRIT; A1 427bc818f6 / ORIGIN_A1; result RESULT_LOCAL /
ORIGIN_RESULT.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
