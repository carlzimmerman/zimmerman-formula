# EDG1 FROZEN CRITERIA: can real cold dark energy charge be held in the edge layer? (2026-11-11)

TEST lane, quarantined. Committed alone, before any script or number of this lane. Adopts nothing, relabels nothing,
registers nothing. Cold dark energy is a gravitating field component, never a particle; a "collisionless carrier" below
is a description of the field's state, not an added species. Footings canonical a0 = 9.3603e-11 m/s^2 and alt
a0 = 1.1312e-10 m/s^2, never pooled.

## 0. The question and what is read

SMF1 (RESULT.md lines 26-38) left one branch ungraded: the law's halo as the image of a held edge layer of real cold
charge. The law's halo is the frame's polarization charge; by Gauss's theorem (SMF1 S0b, LFS1 A2) a static region whose
boundary lies where the frame free-falls (P = 0) has zero net polarization charge, so the positive halo C(R_s) inside is
matched by a layer -C(R_s) at the edge R_s. This lane grades: can real cold charge Q sit in that layer, be held there,
be put there by infall, and close the books?

Read (no other lane file is edited; values copied with their source):
- LFS1 `lfs1_num.py` / `lfs1_num.json`: the law's phantom C(r) = r^2 (g_S - g_N)/G with g_S = g_N/2 + sqrt(g_N^2/4 + g_N a0)
  (point-mass baryons), R_cap = sqrt(G M_b X (X+1)/a0), FLD1's R_ta table (120 / 268 / 325 / 378 kpc at log M_b 9.4 /
  10.45 / 10.7 / 10.9, used for both footings as LFS1 did), layer width w = 0.1 R_s, edge charges A2.
- PD1 (and LFS1's FOOT table): the Lagrangian share of a galaxy's turnaround region X = 59.486 (canonical) / 59.503 (alt) M_b.
- SMF1: S0b, the empty-core statement (Lean `jeans_empty_core`), the rotation-held spin 1/sqrt(2) = 0.71 against 0.035
  (Bullock+2001, PROVISIONAL), A1 (collisionless carrier does not escape S0b/S0c).
- PAR1: C5 (T-SCR), C6 (T-DEP: the frame's static dust is one function of well depth, n_d = P'(hbar + DeltaPhi)), the
  B-Ts theorem (single-valued carriers EMPTY).

Disclosure before freezing: the needed charges (LFS1 A2) and the share X were read before these criteria were written
(the brief itself quotes them). The E1 outcome is therefore partly foreseeable; it is graded as written below and both
R_s readings are reported.

## 1. The configuration (fixed here)

Spherical, point-mass baryons M_b (LFS1's input). Standing region r < R_s with the law (rule 4) and its polarization
charge C(r). Polarization layer of total charge -C(R_s) in [R_s - w, R_s], w = 0.1 R_s. Real cold charge Q placed in the
layer; zero real cold charge inside R_s - w (counted once: SMF1 S0a, rho_Psi = 0 where the law holds). Outside R_s the
frame free-falls (P = 0).

**Graded R_s (reading R5, form B's own rules).** R_s = min(R_ta(z 0), R_cap): the frame cannot stand beyond the
turnaround shell (it still expands there, LFS1 A3), and rule 5 ends the law where the region's charge is used up
(R_cap, where C = X M_b). **Reported reading U:** R_s = R_ta at every mass (LFS1 A2's choice).

## 2. Gates (in order; a structural fail decides the label; later gates then run only as cheap reported rows)

**E0, the books (exact, sympy).** With piecewise shells, derive (i) the mass an outside observer weighs (r > R_s),
(ii) the enclosed mass an inside orbit feels (r < R_s - w), (iii) the net charge of the layer and the pointwise condition
for its total density to be >= 0. PASS iff a Q exists with: inside = the law exactly, independent of Q; outside =
M_b + Q; net layer density >= 0 everywhere. (Expected: PASS with Q >= C(R_s), pointwise rho_Q >= |rho_pol|; at Q = C(R_s)
the layer is gravitationally invisible and g is continuous at R_s.)

**E1, supply.** Needed Q_min = C(R_s) per mass and footing against available = X M_b (PD1's share for that footing).
PASS iff Q_min <= X M_b at every graded mass (9.4, 10.45, 10.7, 10.9), reading R5. Reported: reading U; the fraction
f = Q_min/(X M_b) of the region's whole charge that must end in the layer; the 5.41 rule (5.41 M_b: the hot-branch share,
reported, not graded); FLD1's arrival (read from LFS1).

**E2, can anything hold it.** For each carrier, equilibrium first, then stability. A carrier passes E2 iff an
equilibrium exists that puts Q >= C(R_s) in the layer with none inside R_s - w, AND it is linearly stable to radial and
non-radial perturbations in the analysis stated. E2 PASS iff at least one carrier passes.
- (a) **The frame's own dust, any dust function** of the clock's offset. Hydrostatics of a barotropic medium in the
  static well gives density as one function of depth D = Phi(R_s) - Phi(r) (C6). Derive exactly: d ln rho / dD =
  1/c_s^2. A layer with less dust deeper needs drho/dD < 0 over the depth range, i.e. c_s^2 < 0 (negative
  compressibility, chi = dn/dh < 0). Stability: the local dispersion omega^2 = c_s^2 k^2 - 4 pi G rho (and C5's form
  continued to chi < 0) with c_s^2 < 0: FAIL if a growing mode exists at some k with k R_s >> 1. Also cite B-Ts.
- (b) **Isotropic pressure** (any medium, including an isotropic-dispersion collisionless one): dp/dr = -rho g with
  g = G M_enc/r^2 > 0; p = 0 at the inner (empty) edge. Equilibrium FAILS iff p <= 0 throughout (SMF1 `jeans_empty_core`
  reproduced: discrete step and continuous form).
- (c) **Collisionless shell of circular orbits in all orientations, no net rotation.** Equilibrium: v_t^2 = g(R_s) R_s
  for every orbit; thickness from small eccentricity: the apocentre/pericentre spread needed to cover [R_s - w, R_s]
  (computed in the law's g). Radial stability: epicyclic kappa^2 = (1/r^3) d(r^4 Omega^2)/dr > 0. Non-radial
  stability: fluid stand-in for the in-shell motion (2D sheet, isotropic in-surface dispersion sigma^2 = v_c^2/2,
  surface density Sigma = Q/(4 pi R_s^2)): growing iff k < 2 pi G Sigma / sigma^2 with k^2 = l(l+1)/R_s^2; stable iff no
  l >= 2 grows. This is a stand-in, not a Vlasov computation (disclosed in RESULT). Reported, not label-setting in E2:
  whether "held" is meaningful (orbital period at R_s against t0 = 13.8 Gyr; how a fixed-j shell moves as the enclosed
  mass grows while R_ta grows), which feeds E3.
- (d) **Net rotation.** A spherical layer held by solid rotation about one axis: the centrifugal support is
  Omega^2 R sin^2(theta) (cylindrical radius), zero on the axis, so the poles have no support: equilibrium of a
  spherical shell FAILS exactly. Known answer: the spin a rotation-held shell at R_vir needs, lambda' = 1/sqrt(2), and
  its ratio to 0.035 (SMF1: 0.71, 20 x).

**E3, can infall put it there** (for every carrier passing E2). The cold charge arrives from outside (LFS1: it was at
1.4-14 R_ta at z 1-2) and has zero radial velocity at turnaround. To stay in the layer it needs, at the current R_s, a
specific angular momentum j with pericentre >= R_s - w: j >= f_min R_s v_c(R_s), f_min solved in the law's potential.
Available: tidal-torque spin lambda' = 0.035 (Bullock+2001, PROVISIONAL), per-particle |j| generosity factor F in
{1, 3} (random orientations; F = 3 is the generous bracket), and lambda' up to 0.1 (upper tail, bracket):
j_avail = F lambda' sqrt(2) R_vir V_vir, with R_vir = R_s (most generous; then V_vir = v_c(R_s)) and R_vir = R_ta/2
(self-similar convention, PROVISIONAL; V_vir = v_c(R_ta/2)). Terms in the member that could raise j: stated exactly (a
spherical standing region exerts no torque; the frame's forces are gradients). PASS iff j_avail >= f_min R_s v_c(R_s)
at every graded mass in the most generous bracket (F = 3, lambda' = 0.1, R_vir = R_s). Time: the refill rate the
moving edge needs is reported, not graded.

**E4, reported only.** The lensing of the configuration: inside the law, outside the point mass M_b + Q; R_s against the
KiDS windows LFS1 used (inner edges 81 / 272 / 362 / 456 kpc). No grading.

## 3. Labels (fixed for both footings)

FAILS AT E0 / E1 / E2 / E3 (the first failing gate; the carriers tried are named), BRANCH LIVES AT STRUCTURE (every gate
passes for at least one carrier; NOT a pass for the theory; reported as needing full grading and an independent
re-grade), or NO VERDICT (a known answer fails).

## 4. Known answers (stop grading if any fails)

- KA1 SMF1 S0b: the net polarization charge of a ball whose boundary has P = 0 is 0 for generic P (sympy residual 0).
- KA2 LFS1 A2's edge charges reproduced from its formula and inputs to its printed digits: -61.5 / -40.9 / -37.1 /
  -34.3 M_b (alt -67.7 / -45.0 / -40.9 / -37.7) at R_ta; -59.5 at R_cap.
- KA3 SMF1's empty-core statement reproduced (discrete step for any rho, g, dr >= 0 gives p_n <= 0).
- KA4 SMF1's rotation-held spin 1/sqrt(2) = 0.71 and the ratio 20 to 0.035.

## 5. Mutations (must bite; separate `_MUTATE_<id>` outputs, selected by `EDG1_MUTATE`)

- MU1 P continued past the edge (no P = 0 outside): the layer charge vanishes; KA1 must fail.
- MU2 g reversed (outward, negative enclosed mass): (b)'s empty-core step no longer forces p <= 0; KA3 must fail.
- MU3 j put in by hand (v_t = v_c at turnaround): E3 must flip to PASS for (c), and the label must change.
- MU4 Q = 0.9 C(R_s): E0's pointwise positivity must fail.

## 6. Hand estimates (before any number)

- E0: Q = C(R_s) makes the layer invisible; outside sees M_b + C(R_s).
- E1: f = C(R_s)/(X M_b) between about 0.58 and 1.0 (R5 passes; U fails at 9.4 by a few to 14 %).
- E2(c): v_c(R_s) ~ (G M_b a0)^(1/4) ~ 140 km/s at 10.45; in-shell ratio 2 pi G Sigma R/sigma^2 = Q/(M_b + C) ~ 0.97,
  squared ~ 0.95 < l(l+1) = 6 at l = 2: stable; kappa^2 ~ 2 Omega^2 > 0. Orbital period at R_ta ~ 12 Gyr ~ 0.9 t0.
- E3: needed lambda' ~ 0.7 (R_vir = R_s) to ~1.4 (R_vir = R_ta/2) against 0.035: 20-40 x short; the generous bracket
  (F 3, lambda' 0.1) 2-5 x short. Expected FAILS AT E3.

## 7. Compute and files

sympy + numpy, one thread, `nice -n 19`, seconds. `edg1.py` -> `edg1.out/.json` (and `_MUTATE_<id>`), `edg1_grade.py`
-> `edg1_grade.out/.json`. Paths from the script's own location. Changes after this freeze go in a dated amendment
committed alone; both readings reported.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
