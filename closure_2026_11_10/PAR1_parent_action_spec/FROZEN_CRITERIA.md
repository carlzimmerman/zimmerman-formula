# PAR1 FROZEN CRITERIA: the parent action as an inverse problem (2026-11-10)

Committed alone, before any script, derivation output or number. TEST lane, quarantined: adopts nothing, relabels
nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10), never pooled. The cold
component is cold dark energy (a gravitating field), never a particle. Read-only to every other lane (WV1 and AK1/AKD1
included).

## 0. Question

Find the parent action that works for everything (CMB, growth, lensing, clusters, galaxies, the Solar System) and whose
static galaxy limit is action (A)'s law (QX17 (A); div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b, mu = x/(1+x),
a0 = (1/2) c sqrt(G rho_DE), v3s screening), or prove that no such action exists. Method: turn the record's landed
obstructions into necessary conditions (the spec), derive the class they leave, and say whether it is empty.

## 1. The class Pi (what "parent" means here)

- **Pi1 (local, variational, EP).** A local diffeomorphism-invariant action with finitely many fields and finitely
  many derivatives; matter minimally coupled to one metric; matter's equations second order (REL1).
- **Pi2 (static galaxy limit).** In static, weak-field galaxies the total potential obeys (A)'s law with v3s screening,
  and the law's phantom gravitates and lenses (Phi = Psi).
- **Pi3 (counted once, form B).** In a galaxy's static state the law's phantom density IS the cold dark energy's
  density (not an addition to it). [PAPER72 form B; SHP1: a separate 59.5 M_b halo on top of the law is excluded.]
- **Pi4 (cosmology).** On FRW the cold component is pressureless and clusters like dust with Omega_c = 5.41 Omega_b on
  the scales the record grades (CMB, growth, KiDS amplitude, the forest).

The "carrier" is whatever field carries the cold charge (in (A): the clock tau).

## 2. The spec: conditions to be stated and checked

Each item is written as a theorem (hypotheses, statement, source lane) with a check. "Exact" = sympy residual 0 (or an
exact series); "Lean" = a compiled statement of the algebraic core with standard axioms only and a MUTATE twin of false
statements that must fail. "Read" = quoted from the lane's RESULT.md, not recomputed.

| id | statement to check | source | check |
|---|---|---|---|
| S1 | KNOWN ANSWER (LFS1, exact): the net polarization charge of a region bounded where P = 0 is 0; spherical, zero shift: Y = sqrt(gamma) P^r is frozen | LFS1 S1(a), S1(d) | sympy reproduce; residual 0 |
| S2 | KNOWN ANSWER (EW2, exact closed form): bound H-inf, (mu R)^2 <= 512 delta/(1 - eps), delta = 2 eps + eps^2, gives mu R <= 12.3 at eps = 10^0.05 - 1; EW2's window gap mu_w / mu_h = 10 / 0.063 | EW2 section 5, label table | reproduce 12.3 to 3 digits; gap 159 |
| S3 | KNOWN ANSWER (X14 F2, exact): a zero-charge cold stream crossing a sheet has J = 1 - K Sigma_b tau / w and folds at tau_f = w / (K Sigma_b) | X14 F2 | sympy residual 0 |
| S4 | KNOWN ANSWER (TPA1 / COL1 Part 1): with the quadratic dust term, the clock's linear self-growth around free fall is K nbar / (1 + k^2/mu_K^2) | TPA1, COL1 | sympy residual 0 |
| S5 | NEW, exact (T-SCR): for ANY dust term L_K(h) with susceptibility chi = dn/dh >= 0 and the law's J with J''(0) = 1/K (forced by deep MOND, ROOT note), the carrier's linear response around free fall (A = 0) is omega^2 = -K nbar K chi/(K chi + k^2): no restoring force at any k; the cancellation scale equals the carrier's Jeans scale, k_J^2 = K chi, and chi is also the static-well response per unit depth. With a background field (incremental permittivity eps_r = 1/(1+u)^2), the restoring frequency at high k is omega^2 = K n (1/eps_r - 1) | new; generalizes S4 | sympy residual 0; MUTATE MU1 (polarization charge dropped) must give Jeans support (omega^2 > 0 above k_J) |
| S6 | NEW, exact (T-DEP, depth lemma): for any L_K(h), the static dust in any well is n_d = P'(hbar + DeltaPhi), one function of the depth in every system | new; generalizes MK1 | sympy: static EL equation of P(h) + J(\|grad h\|) with h = hbar + DeltaPhi on a static clock |
| S7 | NEW, exact (T-SPAN): if n^2 c_s^2 is non-increasing on [nbar, n] then h(n) - hbar <= cbar^2 / 2. Hence a static state at depth DeltaPhi > cbar^2/2 requires a point on the compression path where d(n^2 c_s^2)/dn > 0, i.e. P''(tau) > 0 (tau = 1/n, genuinely nonlinear) | new | sympy (the bound attained by P = -A/n + const); Lean core |
| S8 | NEW, exact series (T-SHK): an isentropic (barotropic) jump that conserves charge and momentum has an energy-flux jump -(m/12) P''(tau) (Delta tau)^3 + O(Delta tau^4) (m = mass flux); nonzero wherever P''(tau) != 0, so it is not a weak solution of a variational single-valued field | new | sympy series, residual 0 at third order; MUTATE MU2 (P''(tau) = 0, Chaplygin) must give zero |
| S9 | NEW numbers (T-TRI): cbar from the record's forest line (comoving Jeans length <= 0.42/h Mpc at z = 3; QX28 G6c / QX3 iter3 G4') and from GRW1's late-time edge (c_s 300 km/s); galaxy well depths DeltaPhi(r) from the law's static potential of a Plummer baryon sphere (eps = 1 kpc, COL1) between r and R_ta (FLD1), at log M_b 9.4, 10.45, 10.7, 10.9, per footing | new | numbers; line: DeltaPhi(10 kpc) > cbar^2/2 at every mass |
| S10 | READ: COL1 BREAKS DOWN (centre fold, every mu_K); X14 (i) caustics generic, (ii) every completion needs a new scale | COL1, X14 | read |
| S11 | READ: FLD1 (KiDS inner / middle window edges 272 / 362 / 456 and 637 / 849 / 1069 kpc at log M_b 10.45 / 10.7 / 10.9; R_ta(z 0) 268 / 325 / 378 kpc); LFS1 A3 (R_s <= R_ta) | FLD1, LFS1 | read |
| S12 | READ: MK1 / MK2 / TK1 / AKD1 (no dust stiffness keyed on the offset, the exponential's one sound speed, theta, or A alone); REL1 (no matter acceleration: Ostrogradsky) | those lanes | read; REL1's runaway root s^2 = [K rho + sqrt(K^2 rho^2 + 4 K k)]/2 reproduced (sympy) |
| S13 | READ: CLS1 (no cluster state in (A); the clock's stress is a perfect fluid, no dispersion support); HE1 / SWT1 (no held wall; exit A filling 0.29 vs 0.0231); QX28 / HY1 (a dust lump in galaxies wrecks discs; X-COP between Newtonian (1+R) M_b at +0.12 and law + full share at -0.21) | those lanes | read; the SWT1 bound q_C <= (3/2) f/(1 - f) with line 0.0354 gives f <= 0.0231 (Lean) |
| S14 | READ data facts: KL1 (KiDS-Legacy consistent, 1.71 / 1.88 widths, post hoc); XCV1 (AT THE CEILING, post hoc); RB2 / DG1 (hosted dwarfs high; FAILS do not survive the budget) | those lanes | read |
| S15 | NEW, estimate (T-GR, granules): for a multi-valued wave carrier with the law keyed on its fine-grained frame, the frame's acceleration fluctuates by about sigma^2 / lambda_dB (lambda_dB = h/(m sigma)); in an isotropic Gaussian model the mean polarization along g is suppressed relative to the law by R(s/a0, g/a0); the law holds only where lambda_dB >= sigma^2/a0 (coherence), against the wave dust's coldness from the record's forest line | new | numbers per footing; Gaussian model integrated numerically (10^6 samples, fixed seed) |

## 3. The class decomposition (frozen; exhaustive under Pi1 to Pi4)

- **Lemma 0 (FRW, to be checked exactly):** on FRW, grad Phi = 0 on the leaves and P = 0 by isotropy, so the phantom is
  zero; under Pi3 + Pi4 the 5.41 is therefore a non-phantom (dust) state of the carrier that becomes phantom in galaxies.
- **B0, the law not keyed on the carrier's state** (law sourced by matter or by a field independent of the carrier).
  EMPTY if Lemma 0 holds and route C's uniqueness (SHAPE_search route C steps 2-3: for one conserved medium coupled by
  gravity only, the unique Lagrangian is (A)'s Newtonian limit; contact coupling gives a phonon force that does not lens,
  i.e. counted twice) is read as stated.
- **B-L, the law region set by a fixed length** (a pressure-supported carrier's sound horizon c_s/H, a mass term 1/mu,
  a Jeans length). EMPTY by EW2's window theorem if S2 reproduces (pair: KiDS hosts vs the lensing web).
- **B-T, the law region set by the carrier's own turnaround / fold (a cold carrier).** Then the law region is inside
  R_ta (S11), so KiDS's outer windows must be carried by non-static cold mass (KO1: a heavy exterior is not separated
  from the law). The carrier's microphysics splits it:
  - **B-Ts, single-valued barotropic carrier** (route C's class: (A) plus any L_K(h)). EMPTY if S5 to S9 hold: a static
    state deeper than cbar^2/2 needs a convex point on the compression path (S7); cold infall crossing it either has no
    pressure acting at its scale (screened, S5) and folds (S3, S10), or steepens through the genuinely nonlinear point
    (planar compressive simple wave; Lax 1964, PROVISIONAL citation) into a jump with an energy defect (S8), which no
    single-valued variational field continues. Pair named in the result.
  - **B-Tm-fine, multi-valued wave carrier, law keyed on its fine-grained frame.** EMPTY if S15 gives a suppression
    R <= 0.5 at the graded (sigma, m) and a coherence gap >= 3 between the needed and allowed masses, on the footing.
    Otherwise OPEN.
  - **B-Tm-smooth, multi-valued carrier with the law on a smooth frame** (a second, single-valued carrier that follows
    the cold field's coarse-grained mean frame). Not emptied by any item above unless a theorem is found during the
    derivation; if none, OPEN, and its minimal structure (fields, symmetries, what must be non-conserved, the new scale
    and its window) is stated.

WV1: if WV1's member keys the law on the wave's fine-grained frame it falls in B-Tm-fine (and S15 is the condition that
excludes it); if on a smooth frame, in B-Tm-smooth (not graded here: no duplication). Stated from WV1's own files if they
exist when this lane lands; otherwise conditionally.

## 4. Labels (per footing; a0 enters S9, S15 and the well depths)

- **CLASS EMPTY (theorem):** every branch of section 3 is EMPTY with its checks passing.
- **CANDIDATE STRUCTURE HOLDS / FAILS (name the part):** some branch is OPEN and its simplest member (at most two) is
  written explicitly as an action and graded on STEP 3's structure items: DOF, ghosts and gradients on FRW and on
  statics, GW speed, FRW dust at the CMB, turnaround without a fold, and the static limit reducing exactly to (A)'s law.
  HOLDS only if every item passes; FAILS names the first failing item.
- **NO VERDICT:** a known answer (S1-S4, S12's REL1 root) fails, a MUTATE twin does not bite, or an OPEN branch has no
  member written and graded in this lane (including when its member is WV1's, graded there).

Branch labels are reported alongside the lane label.

## 5. MUTATE twins (each must bite)

- **MU1:** drop the polarization charge from the carrier's charge in S5. Must give ordinary Jeans support
  (omega^2 = c_s^2 k^2 - K nbar > 0 above k_J): the "no restoring force" statement must fail.
- **MU2:** set P''(tau) = 0 (Chaplygin, P = -A/n) in S8. The energy defect must vanish at third order.
- **MU3:** in S7, let n^2 c_s^2 increase (P = K n^2, a convex EOS). The span must exceed cbar^2/2 for large n.
- **MU4:** in S15, remove the fluctuations (s = 0). The suppression must be R = 1 to 1e-3.
- Lean twin: the false versions of the Lean statements must fail to compile.

## 6. Process

- Scripts: `par1_spec.py` (S1-S8, S12's root, Lemma 0), `par1_numbers.py` (S9, S15, per footing), `par1_grade.py`
  (labels); MUTATE via `PAR1_MUTATE=MU1|MU2|MU3|MU4` to separate output files. `PAR1.lean`, `PAR1_MUTATE.lean`.
- Each script under 3 GB and a few minutes; no large outputs.
- Amendments: post hoc, each committed alone and disclosed in RESULT.md.
- RESULT.md leads with the verdict, then the spec (numbered, with sources), then the class, then the candidate action
  if any, then the table and commit ids (local / origin).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
