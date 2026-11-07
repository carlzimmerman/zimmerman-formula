# All-gates search, 2026-11-06: where it converges

Synthesis only: no new lane, no new number, adopts nothing. Kappa = 1/2 FITTED; not theory closed.
Sources: GB1 (e9464bc8ce / 7ca0d54d47), KD1 (6c7f83ed02 / c4008a456c), HC1 (c207d70254 / 27edbba890), QX12 iter_3
(b605c9fd7c), QX20-QX26, QX3.

## What an all-gates ingredient has to do (numbers from the record)

On top of the a0 law, the extra gravitating mass, as a fraction f of the baryons, must be (KD1 diagnostic, canonical / alt):

| Where | Needed f |
|---|---|
| SPARC discs | <= 0.33 / 0.19 |
| X-COP clusters | ~4.2 / 3.8 |
| groups | 1.2-3.5 / 0.9-2.9 |
| X-ray ellipticals | ~0.9 / 0.8 (about half of it is IMF, QX26) |
| dSph satellites | ~1.7 / 1.3 |
| Coma UDGs | ~80 |
| the CMB | cold at z 3400 (w <= 0.01), and lensing chi^2 <= 18.5 at L <= 400 |

## Three physical classes, three walls

| Class | Example lane | What kills it |
|---|---|---|
| Cold fluid (cold early, small sound speed) | KD1, QX3, QX7 | Every well captures it, discs included (f_cap 4.1 vs <= 0.33). The CMB and BBN need mu_K >= 8.9e6 Mpc^-1; galaxies need <= 0.1-79. The gap is >= 1e5 |
| Warm sea (one fixed temperature) | QX12 iter_3 | Retention exp(depth/c_s^2) is too sharp: no single c_s gives extended cluster profiles. The temperature would have to track each host's virial temperature |
| Hot collisionless fermion (phase-space capped) | HC1, HF1, VW1 | At 11 eV it stays out of discs, but under-fills clusters (X-COP +0.39), cannot fill dSphs or UDGs, and fails CMB lensing (chi^2 166-194). A mass cold enough for the CMB lets discs capture it. No window (VW1) |

**The common reason.** An ingredient that tracks each host's virial temperature has to be collisionless and virialise
with the host. If it is also cold early, nothing then keeps it out of discs.
- Phase-space caps exclude discs only for masses that are too hot for the CMB.
- A fixed temperature cannot track hosts.
- A cold fluid enters everything.

## Keys already dead for the switch between discs and hot systems

p/rho, gas temperature, host temperature, virial heating, khronon velocity, enclosed density, gas-g, depth (QX6),
kinematic support (QX22: slow rotators match fast ones to +0.002 +- 0.045 ln), cold gas (QX23), morphology (QX25).
Environment (QX24) is killed but fragile.

## Exits not yet closed (logical, not lanes)

1. **The step has several causes, not one.** IMF for ellipticals and KiDS (QX26: 56-61 % of it), tides or
   non-equilibrium for dSph satellites (QX24 T3b: offset falls with tidal susceptibility, partial rho -0.75), and UDG
   mass systematics. Then only clusters and groups need a new ingredient, which relaxes HC1's dSph/UDG constraints.
   The CMB wall would still stand alone.
2. **Environment, re-read.** Field UDGs (AGC 114905) sit below the law and Coma UDGs sit above it. Satellite offsets
   rise with the host field (QX24 T3b, +0.71). QX24's kill rests on one reading of two Virgo ellipticals.
3. **A disc-specific exclusion mechanism.** A process that removes or heats a collisionless component in rotating discs
   only. QX22's slow-vs-fast null argues against rotation as the key in early types.

None of these is a candidate. Each would need its own frozen lane and would still have to pass GB1 plus the CMB row.
