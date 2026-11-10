# COL1 RESULT: does a free-falling clock end in the static-clock state? (2026-11-10)

Criteria d84a0d88ba; amendments A1 08ae05efd7, A2 ddacb4c383, A3 ba3212d8f0, A4 bf7fe43b6b (local hashes; origin ids at
the end). TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled.

## Label

**BREAKS DOWN / BREAKS DOWN** (canonical / alt) at every mu_K the brief asked for: 3.71, 1.78 / 1.74 and 0.1 per Mpc, at all
four masses (log M_b 9.4, 10.45, 10.7, 10.9). Every known answer the law-on rows rest on passes (KA1-KA2, KA4-KA7). KA3 (the
law-off polytrope) fails at its innermost shell, so the law-off rows (MUTATE M1) and the mu_K 198 bracket are NO VERDICT (A3).

The clock starts as cold dust in Hubble flow at z = 10 and a baryon point mass (softened over 1 kpc) ramps on over 1 Gyr.
Within 0.063 to 0.154 Gyr the innermost clock shells reach the centre together and fold there: a caustic. The two
resolutions agree on the time to better than 0.2 % in every row. The radius (about 1e-5 kpc) is set by the grid. **The
equations give no answer beyond that moment.** At that time the clock at 10 to 300 kpc has hardly moved.

## What it means, in plain words

**The clock does not settle into the law's halo. It falls in like test particles and folds.**
- With the law on, the clock's own gravity is cancelled by the law's force on every scale below 1/mu_K. Part 1 shows this
  from the reduced action; it is TPA1's suppressed self-growth K nbar/(1 + k^2/mu_K^2). So the clock falls onto the baryons
  as test particles would.
- On those scales it also has no pressure. SCS1's frequency does not depend on k at mu_K = 0, so nothing propagates.
- Nothing in action (A) removes infall energy. A shell overshoots its static radius and comes back.
- The first event is at the centre. Inside the baryon core every cold shell reaches r = 0 at the same time (a harmonic
  core). The innermost shells hold almost no polarization charge, so the law's flux-cap wall (r_w = sqrt(G m/a0), X14) is
  too small to stop them. A test shell reproduces the event time to 1e-3 (`col1_focus_check.out`).
- The damped bracket (artificial viscosity) and the at-rest bracket end the same way. So do the sign flips of the
  polarization coupling (M2) and of the flux cap (M3).

**Outside the core the answer is the same, and the clock also arrives in far too small an amount.** This comes from a
reported diagnostic, not a label (A4). It integrates X14's exact shell equation in the law-dominated limit (mu_K r << 1,
so it stands for mu_K = 0.1).
- Shells that reach the centre bounce off the law's walls and come back out through shells still falling in.
- The first crossing outside 10 kpc comes 0.43 to 1.04 Gyr after z = 10 (z 6.2 to 4.1). Outside 100 kpc it comes at 1.8
  to 2.4 Gyr (z 2.8 to 2.3). This holds at every mass, on both footings.
- By z = 0 only about one baryon mass of clock charge has turned around. The clock charge inside 10 to 300 kpc is
  1.0 to 4.0 % of the law's halo, even if crossed shells are counted as if they could pass through each other.
- So a completion of the caustics (dissipation, multi-streaming) would still leave the halo short by a factor of 25 to 100
  at mu_K = 0.1.

**For form B.**
- The static clock (the law's halo) is a stable end state: SCS1 shows it around a point mass, SCS2 around isolated discs.
- This lane finds no path to it from cold dust in action (A) in spherical symmetry. The single-stream clock breaks down at
  first infall. In the law-dominated limit, the charge that falls in is 1 to 4 % of what the halo needs.
- "Counted once" stays a statement about the static state, not one about how the state forms.

**For the spiral wall.**
- The ledger's wall (computed contraction 0.72 to 0.95 against a need of 0 to 0.2) assumed a collisionless cold component.
  In action (A) the clock is not collisionless. It is a single-stream field whose own perturbations do not gravitate on
  galaxy scales.
- So the wall is not crossed here; it is replaced by a harder one. On its own the clock builds no halo around a galaxy: it
  folds, and it brings in only 1 to 4 % of the charge.
- The static end state would put the law inside SPARC's radii, plus static dust. That dust is at most 0.003 of the law's
  halo at 2 to 4 R_d for mu_K <= 3.71, and 4 to 18 times the halo at KD1's 198 per Mpc (Part 0).

## Part 0 (no time evolution; `col1_part0.out`)

Static dust -mu_K^2 Phi/K on the law's point-mass potential, zero at 1 Mpc, as a fraction of the law's halo M_ph (canonical,
log M_b 10.45, at 10 / 30 / 100 / 300 kpc):

| mu_K (per Mpc) | M_d/M_ph | at SPARC radii (2-4 R_d) | Jeans length 2 pi/mu_K | c_s at today's mean | w at z 1090 | self-consistent (dust's own gravity) |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | none | no background charge exists (K nbar = mu_K^2 hbar) | n/a | - |
| 0.1 (S4 galaxy bound) | 2.5e-6 / 1.3e-5 / 9.2e-5 / 4.7e-4 | <= 2e-6 | 63 Mpc | 426 km/s (15,500 at z 10) | 0.999 | converges |
| 1.78 (QX2 clusters; alt 1.74) | 8.0e-4 / 4.2e-3 / 0.029 / 0.15 | <= 7e-4 | 3.5 Mpc | 24 km/s | 0.81 | diverges (Jeans) |
| 3.71 (brief) | 3.5e-3 / 0.018 / 0.13 / 0.65 | <= 3e-3 | 1.7 Mpc | 11.5 km/s | **0.49** | diverges (Jeans) |
| 198.25 (KD1: w <= 0.01 at z 3400) | 9.9 / 53 / 363 / 1850 | 3.6 to 8.4 | 32 kpc | 0.21 km/s | 3e-4 | diverges |
| 8.89e6 (KD1: BBN) | 2e10 to 4e12 | 7e9 to 2e10 | 0.7 pc | 5e-6 km/s | 2e-13 | no static state on galaxy scales |

The law's halo itself: M_ph/M_b = 1.12 / 4.16 / 14.9 / 45.8 at 10 / 30 / 100 / 300 kpc (log M_b 10.45). The other masses and
the alt footing are in the file; R_ref = 0.3 and 3 Mpc move M_d by factors below 3.

What "collapse onto a galaxy" can mean at each mu_K:
- **0:** there is no cosmological cold component to collapse. The static halo's charge grows like r, and nothing supplies it.
- **0.1:** the clock's dust is a hot n = 1 polytrope on its own (c_s 426 km/s today). With the law on, its perturbations on
  galaxy scales feel neither pressure nor their own gravity, so they fall as test particles. The static dust is negligible.
- **1.78 to 3.71:** the clock is pressure-supported or self-gravitating dust only on scales above 1/mu_K (270 to 560 kpc).
  Inside that it behaves as at 0.1. The static dust becomes 10 to 65 % of the halo at 100 to 300 kpc, and its own gravity
  makes a static state with the dust ending at 1 Mpc diverge (the n = 1 Jeans core has radius pi/mu_K).
- **198 and 8.9e6 (the record's CMB and BBN values):** the clock is cold dust on every galaxy scale. Its static state puts
  4 to 18 times the law's halo inside SPARC's radii at 198 per Mpc, which is KD1's "every well captures it".
- **The ledger's f** is defined against an uncontracted cold halo (RM2's M0, LC1's Q_without). A static clock without
  baryons has no halo, so f cannot be evaluated for it. The number given in its place is M_d/M_ph at 2 to 4 R_d (table).
  KD1's diagnostic line (a uniform extra baryon fraction f <= 0.33 / 0.19) is cleared at mu_K <= 3.71 and failed at 198.

## Part 1, the system (`col1_system.out`, Lean `COL1.lean`)

- **Reduction.** Newtonian order, spherical, gamma_L = 0, P eliminated by its Legendre maximum (QX17 K0). With h = c^2 (Q - 1):

      L = mu_K^2 h^2/(2K) + J(|grad h|) - |grad Phi|^2/(2K) - rho_b Phi,   h = -(phi_t + |grad phi|^2/2 + Phi),

  J(s) = (a0^2/K)[s/a0 - ln(1 + s/a0)].
- **Equations.** The clock charge N = mu_K^2 h/K + div P (K P = a0 A/(a0 + |A|), A = -grad h) obeys d_t N + div(N v) = 0.
  Poisson is grad^2 Phi = K (rho_b + N). And dv/dt = -grad Phi + A holds identically.
- **Dropped terms.** The multiplier flux lambda P/Q and W are O(v^2/c^2) (QX17 limits table). gamma_L enters as
  (Lstar/r)^2, about 1e-8 at galaxy radii.

| check | result |
|---|---|
| R1 EL of L = the stated system (sympy, generic J) | residual 0 |
| R2 weak-field expansion of action (A): Q = 1 + eps^2 h, A_x = -eps^2 h_x, L_K = eps^4 mu^2 h^2/2K | residual 0 |
| R3 WKB of the reduced system = SCS1's omega^2 = K G [(1 - K m) k^2 - mu^2]/(mu^2 + K m k^2) | residual 0 |
| R4 P.A -> -P.A leaves the Legendre value J (MUTATE M2a cannot bite) | residual 0 |
| R5 exact shell frequency on the static law state = SCS1's high-k G (1 - K m)/m = 2 a0 u^2/r | residual 0 |
| MUTATE (J -> -J) | R1, R3 fail, as they must |
| Lean COL1.lean | 13 theorems, exit 0; COL1_MUTATE.lean 7 false statements, 7 errors, exit 1 |

**Solver (A3).** Lagrangian thin shells carry the conserved charge. The law sector is solved in its dual (flux) form: Q_j is
the polarization charge enclosed in the gap above shell j, with A = U(G Q_j/r^2). The dual problem is convex with the flux
cap as a log barrier. The law force on a shell is X14's exact finite-shell force. Gravity is thin-shell. Dust volumes come
from Lagrangian faces that make uniform states and homologous motion exact. Leapfrog with an adaptive step.

## Known answers (`col1_ka.out`)

| known answer | J 1200 | J 2400 | line | result |
|---|---|---|---|---|
| KA1 R1-R5 (symbolic) | - | - | residual 0 | PASS |
| KA2a top-hat (law off, cold) | 1.4e-6 | 1.4e-6 | 1e-3 | PASS |
| KA2b point-mass cycloid; first shell at the centre | 4.1e-4; 1.4e-5 | 4.1e-4; 1.4e-5 | 1e-3 | PASS |
| KA3 static n = 1 polytrope (law off), max v/c_s0 | 0.33 (E1 at the centre at 12 Myr) | 0.27 (E1 at 12 Myr) | 1e-3 | **FAIL** |
| KA4 static law state, residual at r >= 3 kpc (A3); mu 0.1 / 3.71 | 1.5e-4 / 1.5e-4 | 3.8e-5 / 3.8e-5 | 1e-3, falls >= 3x | PASS |
| KA4 2 Gyr hold, max v/v_c at r >= 3 kpc; mu 0.1 / 3.71 | 4.8e-5 / 9.4e-5 | 1.2e-5 / 2.4e-5 | 0.01 | PASS |
| KA4 for reference: r >= 0.1 kpc, all nodes | 7.1e-3, 7.0e-2 residual; 3.4e-2, 6.2e-2 v/v_c | 1.8e-3, 3.6e-2; 1.6e-2, 4.6e-2 | - | reported |
| KA5 shell frequency at 30 kpc (mu 0, eps 5 kpc) against -d/dr[-g_b - y + U(y)] | 2.5e-5 | 7.2e-6 | 2e-2 | PASS |
| KA6 energy, mu 0.1, 2 Gyr, dt 2e-4 / 1e-4 | 1.8e-11 / 4.9e-12 (ratio 3.7) | 2.7e-11 / 6.7e-12 (ratio 4.0) | 1e-4, ratio >= 3 | PASS |
| KA6 for reference: mu 3.71, to the outer-wall event at 0.82 / 0.67 Gyr | 2.6e-7 / 1.3e-7 | 2.8e-7 / 1.4e-7 | - | reported |
| KA7 Hubble background, M_b = 0, to z 0; mu 3.71 / 0.1 | 6.6e-7 / 4.5e-6 | - | 1e-3 | PASS |

## Part 2 rows (`col1_grade.out`, `runs/*.json`)

| mu_K (per Mpc) | footing | log M_b 9.4 | 10.45 | 10.7 | 10.9 | label |
|---|---|---|---|---|---|---|
| 3.71 | canonical | 0.1532 / 0.1533 | 0.0823 / 0.0823 | 0.0711 / 0.0711 | 0.0632 / 0.0632 | **BREAKS DOWN** |
| 1.78 | canonical | 0.1532 / 0.1533 | 0.0823 / 0.0823 | 0.0711 / 0.0711 | 0.0632 / 0.0632 | **BREAKS DOWN** |
| 0.1 | canonical | 0.1532 / 0.1533 | 0.0823 / 0.0823 | 0.0711 / 0.0711 | 0.0632 / 0.0632 | **BREAKS DOWN** |
| 3.71 | alt | 0.1532 / 0.1535 | 0.0823 / 0.0823 | 0.0711 / 0.0711 | 0.0633 / 0.0633 | **BREAKS DOWN** |
| 1.74 | alt | 0.1532 / 0.1535 | 0.0823 / 0.0823 | 0.0711 / 0.0711 | 0.0633 / 0.0633 | **BREAKS DOWN** |
| 0.1 | alt | 0.1532 / 0.1535 | 0.0823 / 0.0823 | 0.0711 / 0.0711 | 0.0633 / 0.0633 | **BREAKS DOWN** |

Each cell gives the event time in Gyr after the start (z = 10), J 1200 / J 2400. Every event lies in the core: the
innermost shell is at 3e-6 to 2e-5 kpc, and the radius is grid-limited. Most are E2: the h solve fails as the innermost
shells press against the flux cap at about 0.96 of it. The three alt rows at log M_b 9.4, J 2400, are E1. At the event,
the clock at 10 to 300 kpc is within 0.1 to 0.2 % of Hubble flow (from the event snapshots). The test-shell focusing times
are 0.1533 / 0.0824 / 0.0712 / 0.0633 Gyr (`col1_focus_check.out`).

**Brackets** (labelled, never label-setting):
- **At rest** (today's mean density, Jeans swindle): E2 at the centre at 0.0815 Gyr, every mu_K, both footings.
- **Damped** (von Neumann-Richtmyer, q = 2 rho dv^2): E2 at the centre at 0.0824-0.0825 Gyr, every mu_K, both footings. The
  viscosity is negligible for the near-homologous collapse of a harmonic core.
- **mu_K 198.25 / 198.24** (KD1's cold-at-z-3400 value): E2 at the centre at 0.0823 Gyr. Pressure dominates at r > 5 kpc,
  so KA3's failure applies: NO VERDICT.
- **X_out 16 Mpc:** E2 at 0.0823 Gyr at both resolutions, the same as X_out 8 Mpc.

**MUTATE** (primary row, J 1200):
- M1, law off: E1 at the centre at 0.0062 Gyr. It bites (the event time moves by 92 %), but through KA3's failure mode
  (the law-off pressure at the innermost shell), so it certifies nothing more.
- M2 (J -> -J): E2 at 0.0822 Gyr. **Does not bite.**
- M3 (U(y) -> y, no flux cap): E2 at 0.0824 Gyr (0.08 %). **Does not bite.** The grader prints "bites True" from an
  M_N(<100) comparison. That comparison mixes read times (the primary's only valid read is at the start), so it is not used.
- M2a (P.A -> -P.A): the same event, as R4 predicts.

M2 and M3 do not bite because the event is set by the baryons' gravity on nearly charge-free shells; the law sector's form
does not enter it. Read that as a statement about this event, not as a check of the law sector. The law sector is checked by
KA5 (shell frequency to 2.5e-5) and by R1-R5.

## The A4 diagnostic (reported; sets no label; `col1_outer.out`)

| footing | log M_b | first crossing outside 3 / 10 / 30 / 100 kpc (Gyr after z 10) | shells crossed by z 0 | charge turned around (M_b) | M_N/M_ph at 10 / 30 / 100 / 300 kpc, z 0, all shells |
|---|---|---|---|---|---|
| canonical | 9.4 | 0.54 / 0.99 / 1.22 / 2.06 | 0.42 | 1.06 | 0.010 / 0.013 / 0.016 / 0.017 |
| canonical | 10.45 | 0.29 / 0.60 / 1.11 / 2.04 | 0.55 | 1.06 | 0.023 / 0.022 / 0.028 / 0.022 |
| canonical | 10.7 | 0.25 / 0.42 / 1.05 / 2.39 | 0.59 | 1.06 | 0.040 / 0.032 / 0.032 / 0.028 |
| canonical | 10.9 | 0.22 / 0.54 / 1.15 / 2.23 | 0.61 | 1.06 | 0.034 / 0.034 / 0.036 / 0.036 |
| alt | 9.4 | 0.54 / 1.04 / 1.52 / 2.36 | 0.42 | 1.06 | 0.011 / 0.012 / 0.015 / 0.015 |
| alt | 10.45 | 0.29 / 0.66 / 1.02 / 1.82 | 0.55 | 1.06 | 0.026 / 0.017 / 0.026 / 0.020 |
| alt | 10.7 | 0.25 / 0.48 / 1.11 / 2.15 | 0.59 | 1.06 | 0.036 / 0.027 / 0.027 / 0.025 |
| alt | 10.9 | 0.22 / 0.51 / 1.05 / 2.35 | 0.61 | 1.06 | 0.025 / 0.028 / 0.033 / 0.031 |

Read with its scope: the law-dominated limit (mu_K r << 1), so mu_K = 0.1 per Mpc. Counting only shells never crossed, the charge inside 10 and 30 kpc at z 0 is zero and inside 100 / 300 kpc 0.3 / 0.6-1.3 % of the law's halo. Shells that reach their flux-cap wall, or 0.3 kpc, are reflected (passage through the centre). 2400 shells; one process per row.

## What earlier lanes already said, and whether this agrees

- **X14** (analytic, v3s PN, mu_K up to the S4 allowance) said caustics are generic: held shells oscillate at omega^2 =
  2 a0 x^2/r and phase-mix to crossing, and K(Q) is inert at the fold scale. **Agrees, and adds three things.** The first
  event in a cosmological start is the central focusing, at a stated time. Outside 3 kpc the first crossing comes at
  0.22 to 0.54 Gyr, and outside 100 kpc at 1.8 to 2.4 Gyr. And the exact frequency is 2 a0 u^2/r = 2 a0 x^2/[r (1 - x)^2]; X14 quoted the small-x form.
- **TPA1 4.4** gives the clock's self-growth K nbar/(1 + k^2/mu_K^2) with the law on. **Agrees**: this is why the clock
  accretes like test particles and brings in only about one baryon mass.
- **SCS1, SCS2:** the static state is stable. **Agrees, and the path is missing.** SCS1's own words were "stability of the
  end state is not a path to it".
- **AC15, MS1-MS3, XF1:** a source moving through its clock loses its law. **Consistent.** The clock holds the law only when
  it is held static, and here it is never held.
- **AN1 v3** (AeST dust, a different action): "none settles". **Agrees in kind.**

## What this does not settle

- **Non-spherical infall.** The central focusing is a spherical feature. In 3D the first caustic would come later and
  elsewhere. X14 argues caustics stay generic, from catastrophe theory, not from a solve.
- **Mergers and hierarchical assembly.** Here a fixed baryon mass is switched on over 1 Gyr. Real baryons and the clock
  collapse together from small seeds.
- **The cosmological setting** beyond one point perturbation on a uniform background: no neighbours, no tidal field.
- **Baryon physics:** extended and growing discs, feedback. The 1 kpc softening is a stand-in.
- **The charge budget at mu_K 1.78 to 3.71 beyond 1/mu_K** (270 to 560 kpc), where the clock self-gravitates as dust. The
  A4 diagnostic does not apply there, and the graded runs stop at the centre first.
- **The CMB-side values** (198, 8.9e6 per Mpc). They are not settled dynamically here (pressure-dominated: KA3), but Part 0
  already excludes their static state inside SPARC's radii.
- **Anything after the first caustic.** The equations give no answer there. A completion needs a new term or a new
  scale (X14 verdict ii).

## Anything in FB1, SCS1, SCS2 or the brief that this lane finds wrong

1. **FB1 section 2 item 1 (the CMB arithmetic).**
   - "w0 about 1e-8/mu_K^2, to be below 1e-9" leaves w(z 1090) = 0.56. That is not dust.
   - With KD1's I0 = 4.037e-8 per Mpc^2, w = 1/2 at z 1090 needs mu_K = 3.62 per Mpc. Cold at z 3400 (w <= 0.01) needs
     198.25 per Mpc, and BBN needs 8.89e6 (KD1 already had both).
   - **The brief's 3.71 per Mpc gives w = 0.49 at recombination: it is not a CMB value.**
2. **The brief's expectation that "the law sector off must give plain dust infall"** holds only where c_s is far below the
   infall speed. At mu_K <= 3.71 the law-off K(Q) fluid is a hot polytrope at early times (c_s 420 km/s at z 10 for 3.71,
   15,500 km/s for 0.1).
3. **FB1 section 3** expected the collapse to be "run with the record's own equations (QX17; the finite-difference solver of
   QX17C exists)". QX17C is a static solver. No certified time-dependent solver existed, and a hat-function (Galerkin)
   discretisation carries an O(1) error at the shells next to the origin (A2, A3).
4. **SCS1, SCS2:** nothing found wrong. Their stability results are confirmed where tested (KA5, R3, R5).

## Disclosures

- **Four post-hoc amendments, each committed alone before the runs they govern.**
  - A1: linear nodes inside X_in.
  - A2: lumped pressure; a quadratic central element; the first core grading radius.
  - A3: the thin-shell dual solver; KA4 graded at r >= 3 kpc; KA5 at eps 5 kpc with the frozen general frequency; KA6
    graded at mu_K 0.1.
  - A4: the outer-shell diagnostic.
  - Each lists what was seen first.
- **Development probes of the primary row** were made before the known answers passed: two with the first solver, one
  with the shell solver. They are not graded and are kept outside the repo. Their numbers equal the graded ones.
- **Timing.** The production grid was started while KA6 and KA4 were still running on the final code. The solver was
  committed first (5482cc491a, then d39d7cf1a7, which fixed the driver before any graded number). The damped bracket was
  rerun after a driver fix: the outer boundary's half-step velocity had been set to zero, so the viscosity saw a false
  compression at the edge (first damped run: E1 at 733-738 kpc at 0.014-0.027 Gyr).
- **KA3 fails** (the law-off polytrope's innermost shell carries an O(1) pressure-force error and folds within 12 Myr), so
  the law-off rows (M1) and the mu_K 198 bracket are NO VERDICT. The law-on rows are not affected: their event is the
  baryon-driven focusing, reproduced by a test shell.
- **Core events** count under A2/A3 because their times agree between resolutions (to better than 0.2 %).
  The three alt rows at log M_b 9.4, J 2400, read E1 rather than E2 at the same time.
- **Resources.** About 1-3 s per graded row, single thread; known answers about 1 h; diagnostic about 12 min per row; under 0.3 GB.
  Nothing downloaded. Snapshots kept outside the repo.

## Files

- Criteria and amendments: `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md` to `AMENDMENT_A4.md`.
- Part 0: `col1_part0.py` -> `.out` / `.json`.
- Part 1: `col1_system.py` -> `col1_system.out` / `.json` (MUTATE `_MUTATE`).
- Lean: `COL1.lean`, `COL1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`.
- Solver and driver: `col1_shell.py`, `col1_lib.py`, `col1_run.py`.
- Known answers: `col1_ka.py` -> `col1_ka.out` / `.json`.
- Rows: `runs/*.json`; grader `col1_grade.py` -> `col1_grade.out` / `.json`.
- Focusing check: `col1_focus_check.py` -> `.out`.
- A4 diagnostic: `col1_outer.py` -> `.out` / `.json`.

[ORIGIN_IDS]

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
