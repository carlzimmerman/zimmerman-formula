# CK2 RESULT: the adopted action releases no kick at virialisation or the acceleration crossover. NO RELEASE TERM, both footings

Criteria: FROZEN_CRITERIA.md (8f176791dc), committed and pushed alone before any script or number. Script `ck2.py`;
outputs `ck2.json`, `ck2.out`. Adopts nothing. Kappa = 1/2 FITTED; not theory closed. Both footings graded, never pooled.

## Label

**NO RELEASE TERM (canonical and alt).** Neither event changes the branch of the switch, and a branch change would
carry no latent energy anyway. The September carrier and its kick speed are therefore a postulate, not something the
action supplies. The carrier is also not a field of the action: v3s's only cold component is the K(Q) dust, and AC2q
has none.

## D1: the switch never changes branch on an isolated host

Spherical hosts were point mass, Plummer, Hernquist, and a stars + extended gas mix, with M_b from 1e8 to 1e15 Msun and
scale radii of 1-30 kpc (galaxies) or 100-500 kpc (groups and clusters). The phantom density was evaluated from 1e-3 to
1e3 r_M with the simple nu.

| | canonical | alt |
|---|---|---|
| min rho_ph / rho_DE over the grid | +0.000507 (1e15 Msun Hernquist, 1000 r_M) | +0.000462 |
| min rho_ph / rho_DE at turnaround (1-3.7 Mpc) | +0.0175 | +0.0131 |
| v3s branch change (rho_ph < 0) | none | none |
| AC2q branch change (Sigma/X = 2 + rho_ph/rho_DE < 0) | none | none |

- At r_M and at turnaround the switch stays ON on both footings.
- Virialisation runs from the FRW background (ON, q = 2, QX19) to a static host (ON). Both ends are on the same branch.
- A transient sign change during nonlinear collapse is not proved absent. D2 shows it would release nothing at the
  crossing.

## D2: a branch change carries zero latent energy (sympy, exact)

Integrating AC21 iter_6's f'' pieces with f(0) = f'(0) = 0 gives f = (122363904/44610575) q^6 on the first piece.
Continuing through every knot, the result meets f(1) = 1/2 and f'(1) = 1 exactly, so the form is consistent.

At the branch point F = F' = 0 on both sides, for the blend and for the raw step alike. The jump [gamma_L F] across
Pi = 0 is 0. A switch-off can only hand back stored stiffness energy continuously, as the field evolves. Nothing is
released at the crossing.

## D3: the stored-energy bound (reported, decides nothing)

If all of the stiffness energy, pi G Lstar^2 rho_ph^2, went to the carrier, then v_k <= Lstar rho_ph sqrt(2 pi G / rho_c).

| carrier density | canonical, Lstar 21.7 / 90 pc | alt, Lstar 22.9 / 90 pc | Lstar for 500 km/s |
|---|---|---|---|
| (b) 5.4 x local mean baryon density, max over grid | 26 / 108 km/s | 32 / 125 km/s | 416 / 361 pc |
| (b) at r_M | 0.8 / 3.4 km/s | 1.0 / 3.9 km/s | |
| (a) cosmic-mean floor | exceeds c | exceeds c | (meaningless) |

- With the carrier at the cosmic share of the local baryons, the bound stays below 500 km/s unless Lstar >= 361-416 pc.
  The record bounds Lstar only from below (21.7 / 22.9 pc). X27 found no upper bound out to 90 pc.
- The frozen floor (a) puts a cosmic-mean carrier inside galaxy cores, which gives v > c. It bounds nothing physical.
- D3 is moot in any case, because D1 finds no switch-off to release the energy.

## Controls
- KA1: the point-mass deep-MOND phantom is recovered at 1e4 r_M to 1.25e-9 on both footings. PASS.
- KA2: rho_DE = 4 a0^2/(c^2 G) = 5.843e-27 kg/m^3 on the canonical footing, matching NA1. PASS.
- MUTATE M1, wrong branch (rho_ph -> -rho_ph): D1 finds branch changes on both footings (min ratio about -3e9). **BITES.**
- MUTATE M2, kinked stiffness F = b Theta(Pi): the latent jump is b gamma_L per volume, which is nonzero. **BITES.**

## Disclosures
1. D1 is spherical and static, and uses the simple nu. It does not cover non-spherical hosts, satellites in an external
   field (where rho_ph < 0 lobes exist; X3, OUTER_EDGE), or the nonlinear collapse transient.
2. M1 is a sign flip. It shows that the census can see a branch change; it says nothing about how close a real host
   comes to one.
3. Floor (a) was a frozen choice and turned out unphysical (above). It is reported, not used.

## Consequence for RESOLUTION_2026_11_07.md
CK2 answers the owner's 09-26 rule for this cell. The adopted action does not derive the kick. If CK1, CK3 and CK4 pass,
the kicked carrier resolves the contradiction only as a new postulate (new field, new kick), not as the action's.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
