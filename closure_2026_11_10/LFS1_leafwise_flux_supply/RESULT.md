# LFS1 RESULT: can the khronon's leafwise flux supply the law's halo? (2026-11-10)

**Label, canonical and alt: ILL-POSED.** Every known answer passes. A1, A2 and A4 fail on both footings; any one of
them sets the label.

**Answer: no.** In action (A) the leafwise flux is not a separate supply. It is the normal equation's own bookkeeping, and
it adds no charge.
- The normal equation fixes lambda so that lambda N^2 = d_t X along the clock, with X = N (1 + gamma_L Pi_+).
- So the flux lambda N^2 P carries exactly the change of the factor X in rho_Q, and nothing more (exact, sympy, any
  geometry).
- **Spherical consequence:** the polarization flux Y = sqrt(gamma) P^r through a sphere is carried with the clock's
  flow: d_t Y = N^r d_r Y. If the clock is static (zero shift), Y is frozen.
- So the halo's charge inside a sphere that moves with the clock changes only by Y dX. That is a fraction of order
  |Phi|/c^2, about 1e-6. Everything else the halo holds is charge the clock carried in.

"The polarization of a static clock needs no advected dust" (CLOSURE.md, "The amount") is therefore false in this
action. A static halo cannot grow. A halo that grows needs its charge brought in by the clock's flow, the same charge
COL1 and FLD1 found short.

Two more failures do not depend on A1:
- **The edge (A2).** A static region ends where the clock falls freely (P = 0). Its total polarization charge is then
  exactly zero. So the law's positive halo is matched by a layer of negative clock charge at its edge, equal to
  -34 to -68 M_b at FLD1's turnaround radius. That is a gravitating density of about -1200 to -2300 times the mean cold
  dark energy (for a layer one tenth of the radius thick).
- **The match (A4).** The match to the expanding clock outside is a wall: the clock's acceleration jumps from g to 0.
  That is the switch class's wall, which HE1 says cannot be held.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled. Part B (stability of
the supply flow, SPARC rows) was **not graded**: the criteria grade it only under SUPPLIES or SUPPLIES-SHORT.

Commits (local / origin): criteria 8ddf81950c / see below (alone, before any script or number); result: see the
commit-id record at the end.

## Table (canonical; alt in brackets where it differs)

| item | verdict | numbers |
|---|---|---|
| S1 (a) sqrt(gamma) rho_Q = d_i(X Y^i) + sqrt(gamma) mu_K^2(1/N - 1)/K | **exact** | sympy residual 0, generic 3D functions (QX17's printed rho_Q) |
| S1 (b) normal equation: lambda N^2 = (d_t - N^j d_j) X | **exact** | residual 0 (QX17's printed E2 normal part) |
| S1 (c) khronon equation = d_i[X d_t Y^i + (N^j d_j X) Y^i - N^i d_j(X Y^j)] (+ mu_K terms) | **exact** | residual 0, 3D, shift, mu_K kept |
| S1 (d) spherical | **exact** | zero shift: X d_t Y = 0, so **Y frozen**; with shift: d_t Y = N^r d_r Y, so **Y is carried with the clock's flow** (residual 0; regular centre assumed) |
| S1 (e) with mu_K | **exact** | in a sphere moving with the clock, d(enclosed charge)/dt = Y dX/dt (residual 0); the dust part converts to polarization only along the flow |
| S2 / KA6 numeric check (finite-volume charge, lambda from the normal formula, non-weak N varying by 30 %) | **PASS** | zero shift: Y conserved to 1.0e-11 while X moves by 1.4 %; lambda set to a supply value: Y moves by 1.00 (order 1) |
| **A1** lambda demanded vs the normal equation's | **FAIL** both | lambda_s = d_t ln C_law is finite and positive everywhere: 0.014-0.028 per Gyr at z 0, 0.19-0.25 at z 2. The allowed lambda_n / lambda_s is **negative and 1e-8 to 5e-6 in size** on every grid point: worst -5.0e-6 at log M_b 10.9, 10 kpc, z 0 (alt -5.0e-6). The allowed flux drains, because the lapse deepens as M_b grows. Integrated from z 2 to 0: the halo needs ln(C(t0)/C(t2)) = 0.52-0.80; the flux allows ln X change -2.4e-8 to -2.6e-6 |
| A1 brackets (accretion alpha 0.4 / 1.5, potential to 10 Mpc) | same | largest size 6.3e-6; no verdict moves |
| Frozen-halo deficit (a clock static since z_s) | reported | static since z 2 / 1 / 0.5 holds 0.45 / 0.67 / 0.82 of the law's charge at z 0 (100 and 300 kpc, every mass) |
| Creep the law would need (shift speed v = d_t Y / d_r Y, inward) | reported | z 0: 0.1-0.2 km/s at 10 kpc, 2.4-2.6 at 100 kpc, 7.8-8.0 at 300 kpc, 9.4-17.3 at R_cap. Slow enough that the clock still carries the law (A changes by v/t, about 1e-4 of g) |
| Where today's charge was (along the clock's flow) | reported | charge now inside 100 kpc was inside 213-221 kpc at z 2 = 1.4-4.6 x R_ta(z 2); inside 300 kpc: 443-447 kpc at z 1 (1.9-6.0 R_ta), 658-666 kpc at z 2 (4.2-13.8 R_ta). So it was in still-expanding, free-falling clock, where P = 0, and arrived as dust |
| **A2** net charge, edge | **FAIL** both | Net polarization charge of any region bounded where P = 0 is exactly 0 (sympy S1(a) + Lean `net_zero`, `edge_is_minus`). Edge charge at R_s = R_ta: -61.5 / -40.9 / -37.1 / -34.3 M_b (log M_b 9.4 / 10.45 / 10.7 / 10.9; alt -67.7 / -45.0 / -40.9 / -37.7). At R_cap: -59.5 M_b. Edge density (width 0.1 R_s): -1190 to -2120 x the mean cold dark energy (alt to -2330) at R_ta; -400 to -2270 at R_cap |
| A2 reservoir | none reachable | the leafwise flux cannot cross a surface where P = 0. Neutralizing the edge needs C(R_s) = 34-68 M_b of dust there: 6-13 x form B's cosmic share 5.41 M_b, and 20 x FLD1's arrival (1.75-3.45 M_b). With mu_K = 1 per Mpc (KiDS's bound) the clock's own dust part inside R_s is 0.6-9 % of the edge at R_ta (0.5-19 % at R_cap), so it cannot fill it |
| A3 reach (reported; label-setting only under rule 3) | short | R_s <= R_ta(z 0) = 120 / 268 / 325 / 378 kpc against R_cap 116 / 389 / 518 / 652 (alt 106 / 354 / 472 / 594): short of the cap at 3 of 4 masses; short of KiDS's inner edge (272 / 362 / 456) at 3 of 4 and of every middle edge (190-1069). Beyond R_s lensing sees M_b only. The edge layer raises Delta Sigma by 2.5 % at 0.5 R_s and by 46 % at 0.9 R_s |
| **A4** matching | **WALL** both | inside A = g(R_s), outside A = 0: g/a0 = 0.015-0.029 at R_ta, 0.017 at R_cap, so A jumps at every finite R_s. The jump carries the A2 layer: sigma_edge 0.85-1.67 M_sun/pc^2, Delta g / g = -0.97 to -0.985. At R_cap the clock outside also moves: WALL + FOLD. Never SMOOTH |
| Known answers KA1-KA6 | 6 of 6 PASS | below |
| MUTATE MU1, MU2, MU3 | all bite | below |
| Lean | compiles | `LFS1.lean` exit 0, 6 theorems, standard axioms only (`compile.txt`); `LFS1_MUTATE.lean` fails on all 6 false statements (`compile_MUTATE.txt`) |

## Why, in plain words

1. **The flux is accounting, not supply.**
   - The khronon charge is rho_Q = D.P with a lapse factor and a stiffness factor in front: sqrt(gamma) rho_Q =
     d_i(X Y^i), X = N (1 + gamma_L Pi_+).
   - The normal part of the P equation fixes the multiplier, and with it the flux: lambda N^2 = dX/dt along the clock.
   - So the flux moves exactly the charge that the changing X creates or removes, and the khronon equation reduces to
     X dY/dt = 0 along the clock.
2. **Around a growing mass that means a static clock keeps its halo frozen.**
   - X changes by about |Phi|/c^2, about 1e-6, so the frozen halo is the one the clock had when it became static.
   - The allowed flux even runs the wrong way: as M_b grows the well deepens, N falls, and the flux drains.
   - The law needs the halo to grow by e^0.5 to e^0.8 between z 2 and today. A clock static since z 2 holds 45 % of
     today's law.
3. **To grow, the halo needs the clock to flow in.**
   - With a shift, Y is carried with the clock. The law then needs an inward creep of 2-17 km/s at 100 kpc to R_cap
     today, slow enough to keep the law.
   - The charge it brings was, at z 1-2, 1.4 to 14 turnaround radii out, in free-falling clock that carried no law.
     It arrives as dust.
   - So the halo's charge is advected charge. This is the case COL1, FLD1 and MK1 already graded, and FLD1 found that
     only 1.6 to 5.1 % arrives.
4. **The static region is neutral as a whole.**
   - A region whose boundary lies in free-falling clock (P = 0) has zero polarization charge. Gauss's theorem does this,
     not the dynamics.
   - The law's positive halo therefore sits inside a negative layer of equal size at the edge, about -1000 to -2000
     times the mean cold dark energy density for a layer a tenth of the radius thick.
   - This is SWT1's T1 again: a law-on region shows only its baryons from outside. The R541 note says the same
     ("the law's halo is a slice divergence and carries no net charge").
5. **The edge is a wall.** The clock's acceleration jumps from g to 0 there, at any radius. The layer sits on the jump.
   That is the switch class's wall (HE1: it cannot be held). It is not a fold the dynamics could pass through.

## Known answers (all pass)

| KA | what | result |
|---|---|---|
| KA1 | deep-law hydrostatics, p = J(g) = g^2/(2K) holding rho_ph: sigma^2 = (1/2) sqrt(G M_b a0) | sympy residual 0; dp/dr + rho g residual 0 |
| KA2 | Gauss on law S: 4 pi R^2 P_r = M_b (nu - 1) = R^2 g a0 / (G (g + a0)) | residual 0 (and Lean `gauss_lawS`) |
| KA3 | QX17's printed equations: (a) unitary E3 from the covariant current; (b) lambda from projecting E2 on n (explicit ADM metric with shift); (c) T^P_{0i} = 0 for a static clock (Noether cross-check of S1(d) through the 0i metric equation) | residuals 0 / 0 / 0 |
| KA4 | sqrt(M_sun a0 / G) = 25,914 M_sun per kpc | 25,914.5 (rel 1.9e-5) |
| KA5 | R_cap = 116 / 389 / 518 / 653 kpc (FLD1) | 116.0 / 388.6 / 518.2 / 652.4 (within 0.11 %) |
| KA6 | S2 conserves Y with lambda from the normal formula | 1.0e-11 (line 1e-6) |

## MUTATE (all bite)

- **MU1** (flip lambda's sign in E3; QX17's own mutation). S1(c), (d) and (e) and KA3(a), (c) fail with non-zero residuals.
  The grader turns both footings to NO VERDICT (`lfs1_grade_MUTATE_MU1.out`). S2 under the flip moves Y by 2.7e-2
  against 1.0e-11 unmutated. That is exactly the X^-2 law the flipped equation predicts (X moved 1.4 % net over the
  run).
  - **Disclosed:** the criteria's wording "by order 1" for this run was mis-set: the flip's effect is 2 dX/X, not order
    1. The bite is certain (a factor 2.6e9) and no label depends on it.
- **MU2** (lambda := lambda_s by hand). A1 turns to PASS on both footings (rho_lambda = 1). The label stays ILL-POSED
  through A2 and A4 (`lfs1_grade_MUTATE_MU2.out`).
- **MU3** (P continued past the edge). A2 turns to PASS on both footings. The label stays ILL-POSED through A1
  (`lfs1_grade_MUTATE_MU3.out`).

## What this does not cover

- **Disclosed inputs:**
  - Point-mass baryons, with graded radii >= 10 kpc.
  - The static constitutive law at gamma_L = 0 for P. gamma_L Pi_+ is kept in X; it is 1e-16 to 7e-13 at these radii and
    drops out exactly in S1 anyway.
  - The accretion history M_b0 exp(-alpha z) is generic, not fitted. The ratio rho_lambda is near |Phi|/c^2 for any
    history, because both lambdas scale with dM_b/dt.
- **R_ta and the KiDS edges** are FLD1's canonical table, used for both footings (FLD1: alt R_fold within 0.5 %).
- **The exact results** S1(d) and (e) are for spherical symmetry. S1(c) holds in any geometry, but its non-spherical
  consequence was not worked out. A non-spherical flux could circulate charge; it cannot change the charge inside a
  surface where P = 0 (S1(a)).
- **mu_K != 0** is covered only as the bracket and in S1(e): the dust part converts to polarization along the flow, so
  it is advected charge.
- **Not checked:** no fully nonlinear time-dependent solve, and no claim about what the clock does behind a fold.

## Files

- `FROZEN_CRITERIA.md`: committed alone, first.
- `lfs1_sym.py` -> `lfs1_sym.out/.json`: S1, KA1-KA3, about 1 s.
- `lfs1_num.py` -> `lfs1_num.out/.json`: S2/KA6, KA4, KA5, A1-A4, brackets, about 1 s.
- `lfs1_grade.py` -> `lfs1_grade.out/.json`.
- MUTATE twins: `*_MUTATE_MU1/2/3.*`.
- `LFS1.lean`, `LFS1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`.
- Re-run: `python3 lfs1_sym.py && python3 lfs1_num.py && python3 lfs1_grade.py` (and with `LFS1_MUTATE=MU1|MU2|MU3`,
  then `python3 lfs1_grade.py _MUTATE_MU<n>`).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
