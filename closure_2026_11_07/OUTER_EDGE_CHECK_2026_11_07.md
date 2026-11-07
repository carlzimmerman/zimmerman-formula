# Outer-edge check, 2026-11-07: does the v3s / AC2q switch give an isolated galaxy an outer radius?

Analysis only, no lane, no graded number. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

## Why this was asked
A proposal made on 11-07 (this chat) suggested deriving the radius where the stiffness switch turns the a0 law off
around an isolated galaxy and grading it on the KiDS isolated-lens stacks (Brouwer+2021 Fig. 8, bins to 3 Mpc), as a
second, independent appearance of rho_DE in the theory. Before freezing criteria the record was checked. The proposal
is WITHDRAWN on that check.

## What the action says (record, not new)
- v3s stiffness: -(gamma_L/2) [max(D.P, 0)]^2. The switch is off only where D.P < 0 (V3_FULL_PICTURE section 4.7).
- AC2q: Sigma = D.P + 2X, switch on the sign of Sigma; AC21's blend differs from the step only in 0 < Sigma < X.
- Static census (TC1 N2, sympy exact): spherical QUMOND phantom density gives Sigma/X = 2 + rho_ph/rho_DE. So the
  switch is off only where the phantom density is negative, and the AC21 layer sits at rho_ph between -rho_DE and
  -2 rho_DE.
- For an isolated galaxy with a monotone nu, rho_ph >= 0 everywhere; SPARC's minimum Sigma/X over 175 galaxies and
  3389 radii is 992 (canonical) and 748 (alt), 100 % IN (TC1).

## Conclusion
There is NO outer edge in the action for an isolated galaxy. D.P stays positive out to infinity, v3s equals v3 there,
and the law's phantom halo continues as 1/r^2 until an external field (neighbours, the web) makes rho_ph negative.
That radius is the standard external-field radius r_EFE ~ sqrt(G M a0)/g_ext, already the subject of QX24, EV1, the
Chae-field rows and SV4 (AGC 114905), not a new door. The density coincidence rho_ph = rho_DE at a few Mpc has no term
in the action behind it and predicts nothing.

Orders of magnitude (estimate only, point mass, g_ext = 0.02 a0; not graded):

| a0 (m/s^2) | M_b (Msun) | r where rho_ph = rho_DE (Mpc) | r_EFE (Mpc) |
|---|---|---|---|
| 1.2e-10 | 1e+10 | 1.3 | 0.17 |
| 1.2e-10 | 1e+11 | 2.3 | 0.54 |
| 1.2e-10 | 1e+12 | 4.1 | 1.70 |
| 1.1e-10 | 1e+10 | 1.4 | 0.18 |
| 1.1e-10 | 1e+11 | 2.4 | 0.56 |
| 1.1e-10 | 1e+12 | 4.3 | 1.78 |

Negative-rho_ph regions do exist (outer globulars' lobes, 180-1555 pc; X3), and the switched statics there are
UNCHANGED (X3, 13/13). Nothing is left to compute for this door.

Label: NO EDGE IN THE ACTION (analytic, from the record). No lane id was taken; no criteria were frozen.
