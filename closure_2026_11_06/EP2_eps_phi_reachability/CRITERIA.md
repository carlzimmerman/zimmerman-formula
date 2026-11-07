# EP2 frozen criteria: does any record background history reach eps_phi = 2? (corrected bound, both footings)

Frozen before any EP2 script exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Successor to EP1's
separate REACHED / NOT REACHED label. EP1's frozen label stays NOT DECIDED as EP1 froze it.

## Disclosure (what is already known before freezing)

EP1 (criteria d8fc918584) found its frozen worst-case bound 2.163 at z = 0.4, only because that bound dropped
rho_DE from rho_tot. EP1 also printed a post-data variant (rho_DE kept at node - 2 sd, slope still from the
crossed node +/- 2 sd ends): 1.179. That number is known, so it is not EP2's graded statistic. EP2's graded
worst case is a single self-consistent history (below), which no lane has computed.

## Derivation (exact, written before computing)

For a canonical clock phi, eps_phi = phidot^2 / (2 H^2), and phidot^2 = rho_phi + p_phi. Continuity,
rho_phi' (z) = 3 (rho_phi + p_phi) / (1 + z), gives rho_phi + p_phi = (1 + z) rho_phi'(z) / 3. With
3 H^2 = rho_tot (8 pi G = 1):

    eps_phi(z) = (1 + z) rho_phi'(z) / (2 rho_tot(z)),   rho_tot = rho_m (1+z)^3 + rho_r (1+z)^4 + rho_k (1+z)^2 + rho_phi(z).

rho_phi is the dark-energy density (a0 = kappa c sqrt(G rho_DE)), so a history of a0(z) or rho_DE(z) fixes
eps_phi(z) exactly. EP1's mistake was to drop rho_phi from rho_tot, which is not a bound on the true
eps_phi. Keeping it is the exact expression. eps_phi < 0 (rho_phi' < 0) means the history is phantom there and
no canonical clock can follow it; that is reported, not graded (it does not reach +2).

## Histories (the record's own, no LCDM input)

Units: omega = rho / rho_crit,100. rho_m = omega_b + omega_c = 0.02236 + 0.1202 (CFG654 A1 pair, the record's
pre-switch values); rho_r = omega_gamma (1 + 0.2271 x 3.044), omega_gamma = 2.47e-5; flat unless stated.
Footing sets the present dark-energy density from a0 at kappa = 1/2:
omega_DE0 = (8 pi / 3) (a0 / (kappa c))^2 / H_100^2, with a0 = 9.360324825027975e-11 (canonical) and
1.1312035414413022e-10 m/s^2 (alt).

- H-flat (footing background): rho_DE constant. eps_phi = 0 exactly, every z.
- H-native: rho_DE(z) = omega_DE0 (a0(z)/a0(0))^2 from CFG689's committed a0_node_q (BAO+SN primary), linear
  in z between nodes 0, 0.4, 0.7, 1.0, 1.5, 2.33, held constant beyond 2.33 (as SV5 iter_3 does). Graded on
  the median nodes and on a worst-case history (below).
- H-CFG689 (footing-free): CFG689's own fitted omega_DE nodes and omega_k (EP1's input), graded on the best fit
  and the worst-case history.
- H-CPL (reported only, not graded): w0 = -0.838, wa = -0.62 (SV5's CPL), to z = 1100.

Worst-case history (graded): on each node interval [z_i, z_i+1], rho_DE runs linearly from its low edge
(lowest committed quantile at z_i: a0_node_q[0]^2 scaled, or node - 2 sd for H-CFG689) to its high edge (highest
quantile a0_node_q[4]^2, or node + 2 sd), clipped at 0. That maximises the slope on the interval, and the same
history enters both the numerator and rho_tot. For H-CFG689, omega_k takes its -2 sd edge (lowest rho_tot).

Grid: z step 0.001 on [0, 2.33]; for H-flat and H-CPL also log-spaced to z = 1100 (2000 points).

## Lines and labels

- Per history and footing: NOT REACHED if max eps_phi < 2 on the graded span; REACHED if >= 2.
- Door label: NOT REACHED if H-flat, H-native (median and worst) and H-CFG689 (best and worst) are all NOT
  REACHED on both footings. REACHED if any graded history reaches 2; then EP1's witness grade decides the door.
- Beyond z = 2.33 the native and CFG689 histories have no node. There EP2 states only the condition (eps_phi = 2
  needs Omega_phi >= 2/3 and w_phi >= 1/3: a clock dominating the budget while redshifting at least as fast as
  radiation, not a dark-energy phase) and grades the held-constant reading (eps_phi = 0).

## Known answers

- KA1: EP2's code, run with EP1's frozen bound (rho_DE dropped from rho_tot, EP1's slope rule), reproduces EP1's
  REACH.json worst_max 2.16276121853809, bound_best_max 0.5421219955861971, best_full_E2_max 0.2205182284922488
  and post_data max 1.1788178001976903 to 1e-12 relative.
- KA2: H-flat gives eps_phi = 0 to machine precision on both footings.
- KA3 (reported): omega_DE0 on the canonical footing against CFG689's fitted node 0 (0.3116).

## MUTATE (must bite, else NO VERDICT)

- M1: a planted kination-like clock, rho_phi = omega_DE0 + A (1+z)^6 on the canonical footing, with A set so that
  its kination part equals the matter density at z = 3 (A 4^6 = rho_m 4^3, so A = rho_m / 64), must read REACHED
  on the z grid to 1100.
- M2: H-native with rho_DE's slope multiplied by 100 on [0.4, 0.7] must read REACHED on the worst-case rule, or
  the rule has no sensitivity at the location that set EP1's 2.16 (reported whether it bites; M1 is the gate).

## Scope

NOT REACHED says: on the record's measured dark-energy histories (z <= 2.33) and on the footing background, the
AC2q clock never has eps_phi = 2, so EP1's decelerating fixtures describe no physical AC2q epoch in that span.
It is not a statement about 2.33 < z < 1100 beyond the held-constant reading and the stated condition, and it
is not adoption.
