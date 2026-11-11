# NBC1_neutral_baryon_contact: RESULT

## Verdict: KILLED (K2 PROVISIONAL) / KILLED (K2 PROVISIONAL)

a0 cannot be a contact strength between cold dark energy and neutral gas. With an opacity of order G/a0, gas on a
circular orbit in the law's own halo hands its angular momentum to the halo in less than one orbit, at every radius
and for every galaxy mass. The only way out is a halo that turns with the gas, and that halo settles into a layer the
local vertical force does not allow.

Criteria `FROZEN_CRITERIA.md` (0316ed0624, committed alone first, no amendment). Footings canonical / alt, never pooled.
kappa = 1/2 FITTED; not theory closed. Adopts nothing. Nothing here says the data favour the framework.
Every number below is from `nbc1.out` / `nbc1.json`.

## The hypothesis

H: cold dark energy is conserved, cold and normally self-gravitating (form B), and exchanges momentum with neutral
baryons only, f = kappa_c rho_c rho_n |dv| dv, kappa_c = k G/a0 with k in {1, pi, 2 pi}
(7.13 / 5.90, 22.4 / 18.5 and 44.8 / 37.1 cm^2/g). It is MEDIUM_DESIGN's section 3 with the word "neutral" added to
remove that note's two kills, and a microphysical version of PAPER49's rule T.

## Tests

| Test | k = 1 | k = pi | k = 2 pi |
|---|---|---|---|
| K1 orbits for gas to lose its angular momentum, x in [0.1, 3] (fail below 10) | **FAIL** 0.58 to 3.46 | **FAIL** 0.18 to 1.10 | **FAIL** 0.09 to 0.55 |
| K2 dark column inside 1.1 kpc at the Sun, Msun/pc^2 (fail above 36.7; PROVISIONAL inputs) | **FAIL** 64.8 / 69.6 | **FAIL** 74.2 / 83.9 | **FAIL** 74.4 / 84.6 |
| K3 cold component's drag over the expansion rate, largest value at z >= 900 | NOT DECIDED BY HAND 0.21 / 0.18 | NOT DECIDED BY HAND 0.67 / 0.55 | **FAIL (by hand)** 1.34 / 1.11 |
| K5 heating per H nucleus over the [C II] cooling (reported, PROVISIONAL) | 7.4 / 6.8 | 23.3 / 21.4 | 46.6 / 42.8 |
| Verdict | KILLED (K2 PROVISIONAL) | KILLED (K2 PROVISIONAL) | KILLED |

Values are canonical / alt where they differ. K1 is the same on both footings because it depends only on k.

**K1 in closed form.** From the law's halo, rho_c r = a0 / (2 pi G sqrt(1 + 4 x^2)), so

    N_orb = c(x) sqrt(1 + 4 x^2) / k,      c(x) = v_c^2 / D = 0.56 to 0.58,

with no dependence on the baryon mass or on a0. Inside r_M the gas loses its angular momentum in 0.58 / k orbits.
The gas layer is optically thin at every k (0.006 to 0.12), so the estimate applies. The largest k that lets gas
survive 10 orbits on the whole grid is 0.058 (0.41 / 0.34 cm^2/g); for 50 orbits it is 0.0115 (0.082 / 0.068 cm^2/g).
G/a0 is 87 times above the 50-orbit bound.

**K2, the co-rotation escape.** K1's drag vanishes only if the cold component moves with the gas. An inner-halo
element at the solar circle scatters off the gas layer 1.8 / 1.5 times in 10 Gyr at k = 1 (5.6 / 4.7 and 11 / 9.3 at
the larger k), so 83 / 77 per cent of it has settled. A rotation-supported layer that gives the law's own in-plane
field needs 74.4 / 84.6 Msun/pc^2; the round halo it replaces gives 16.9 / 18.8, which fits the budget of 21 +- 5.2.
The budget, the gas column (13 Msun/pc^2), R0 and v0 are from memory and PROVISIONAL.

**K3, recombination.** Neutral helium (from z about 2000) and then neutral hydrogen couple the cold component to the
plasma at 0.07 to 0.21 of the expansion rate at k = 1 between z 2500 and z 900, and the baryons to the cold
component at about 1 (1.15 / 0.95 at z 1100). No Boltzmann run was made, so k = 1 and k = pi are not decided here.

**K4, the Bullet.** Not a test: H was built to pass it, the gas is ionised.

**K7, the curve.** NOT EVALUATED. It is moot once K1 and K2 fail.

## What the kill says (post hoc readings; no label moves)

1. **The "optical depth 1/(2 pi)" coincidence is gravity's own statement.** The law's halo has column a0 / (2 pi G)
   because its field saturates at a0. Any coupling of strength G/a0 therefore acts once per orbit at every radius.
   That is dimensional analysis, not evidence of a contact.
2. **A speed dependence does not rescue H.** K1 has to hold at every speed where old gas discs are seen (roughly 20 to
   300 km/s), so k must be below 0.058 across that whole range, while the reading needs k of order 1 in galaxies.
   Raising the coupling at low speed makes K3 worse.
3. **Every medium class the record can name now has a failing verdict.** MEDIUM_DESIGN's table (M5, Z1, FA3, TM1 and
   the rest), its section 3 (contact with all baryons) and this lane (contact with neutral baryons). What is left is
   not a medium in contact with anything: it is the joint itself, a time-dependent state of the action.

## Known answers and mutations

KA1 to KA6 PASS on both footings (drag limits 1.00001 / 1.00020; quadrature against the closed form 3.6e-9; KA3
reproduces MEDIUM_DESIGN's 0.73 / 0.61 as 0.731 / 0.605; Saha half-ionisation at z 1369, x_e(1100) 0.146,
x_e(200) 3.4e-4; round-halo column 16.9 / 18.8).
M1 (k / 100): K1 turns to PASS at k = 1 (57.6 orbits). M2 (no gas in K2): K2 turns to PASS (16.9 / 18.8).
M3 (all baryons in K3): the drag at z 1100 rises from 0.213 to 0.239. All three bite.

## Disclosures

- Run 1 (`nbc1_run1_KA1_quadrature_overflow.out`) had KA1 failing: numpy's 400-node Gauss-Hermite and 200-node
  Gauss-Laguerre weights overflow. The quadrature was changed to Gauss-Legendre on a finite box; every K line is
  identical before and after (the K lines use the closed form, which the quadrature now matches to 3.6e-9).
- Hand estimates were made in the coordinating chat before the criteria were frozen (listed in the criteria).
- K2 and K5 rest on values quoted from memory, not looked up. K2's margin is large (65 to 85 against a fail line of
  36.7), but the label carries PROVISIONAL because of it.
- The halo is taken isotropic with the Jeans dispersion, around a point mass; the drag is the hard-sphere form.
- Helium is by Saha, which overstates neutral helium above z about 1800 (stated in the criteria).
- No Lean file: the lane is arithmetic and one ODE.

## Not claimed

Not that no coupling between cold dark energy and baryons exists: only that one of order G/a0 with neutral gas does
not. Not a statement about a field-mediated force. Not a CMB computation.

## Re-run

    python3 nbc1.py > nbc1.out
    for m in M1 M2 M3; do python3 nbc1.py $m > nbc1_MUT_$m.out; done

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
