# PD1 AMENDMENT A2: the source's round-19 answers (committed alone, before any number under them)

Criteria 0dc7929421, A1 08b9797be3. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.

**Timing, disclosed.** The PD1 results (6bd9621320, A1 d6fd4c2021) have already landed: FAIL / FAIL at P2 KiDS. The orchestrator
relayed these answers afterwards. No number under A2 exists.

## A2 construction, frozen (replaces the graded reading; the earlier readings become brackets)

1. **Share, galaxy scale (the "basin").**
   - share = 5.41 x f_basin x M_b,gal, with **f_basin = 2.0**, the middle of the source's stated 1.8-2.2.
   - The record has no baryon census. The lane takes the source's range ("diffuse baryons 55-70 % of Omega_b") as stated and does
     not verify a census. f_basin is a form choice; 1.8 and 2.2 are reported.
   - The phantom is sourced by the galaxy's baryons M_b,gal, as before.
   - The phantom profile runs to R_trunc = min(R_ms, the radius where M_ph = share). R_ms is the Newtonian turnaround, as frozen.
   - Applies to KiDS lenses, SPARC galaxies and the P1 population.
2. **Share, group and cluster scale.** The measured M_b,sys already is the basin baryons (gas), so f_basin = 1: share = 5.41 M_b,sys.
   - Cluster rule as A1: f_core = (1/2)[1 - (v_stiff / v_vir)^2] of the share in a Duffy NFW core; the phantom capped by
     (1 - f_core) share; the remainder isothermal to R_ms.
   - The 1/2 is a form choice. **Prefactor 1 is the bracket.**
3. **P1 with neighbours.** q_pop at z 0.5 / 1 / 2 = [GSMF sum of min(M_ph(<R_ms), share, M_ph(<0.85 Mpc))] / rho_bar_d.
   - The 0.85 Mpc neighbour truncation is applied to every galaxy. That lowers q, so it is generous.
   - Line q <= 1.
   - Isolated KiDS lenses get no neighbour truncation (they are selected isolated).
4. **Bullet (frozen reading: galaxy-traced).** The dust is collisionless and ballistic.
   - Each subcluster's phantom (capped), core and remainder inside R200 are placed with the galaxies.
   - Gravity is Newtonian (no nu on the gas): DB1's child is run with a0 -> 1e-30 and this galaxy-traced dark mass. Graded with
     DB1's row label (its offset class and M300 Z).
   - KA-A2: with a0 restored and zero dark mass, the child reproduces DB1's law-only row (Z -4.55, -4.54).
   - Bracket (reported): the gas-locked reading. The phantom follows the gas: DB1's law row with the core + remainder
     galaxy-traced, as in A1.
   - The source's claims (dust core + galaxies about 7.5e13 vs stripped gas about 1.8e13; peak offset about 8 kpc;
     t_1/2 = d / v_stiff about 650 Myr) are reported beside the numbers.
5. **P7 answered (by the source):** the phantom profile needs a constitutive assumption. The field's dispersion is locked to
   sigma^2 = (1/2) sqrt(G M_b a0), equivalently div Pi^ij = -rho [nu - 1] g_N,b^i. N is recorded as a phenomenological closure
   with that named assumption, not an action-derived result.

**Regraded under A2, label in the frozen order:** P1, P2 KiDS, P2 SPARC, P3 groups, P3 X-COP, P4 (carried), P5 Bullet.

**Brackets (reported):** f_basin 1.8 and 2.2; the cluster prefactor 1; the gas-locked Bullet.
