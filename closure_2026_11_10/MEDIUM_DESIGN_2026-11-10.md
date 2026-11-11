# The medium, designed against the record (2026-11-10)

A design note, not a lane: no criteria, no label, nothing graded. Every verdict quoted is a lane's own first line, and
where this note and a lane differ the lane is right. Section 3's numbers are a hand check in SI (`MEDIUM_DESIGN_check.py`,
`MEDIUM_DESIGN_check.out`). Adopts nothing. kappa = 1/2 FITTED; not theory closed. Cold dark energy is a gravitating
field component, never a particle.

## Answer first

**No local medium with the four properties exists in any class the record or this note can name.** The owner asked for
the medium to be designed and solved. It was designed by elimination; the one class the record had not tried was worked
out here and dies on arithmetic. What is complete is form B as a set of rules that predicts every row
(`THEORY_ASSEMBLED_2026-11-10.md`). What does not exist is an equation of motion that produces those rules.

## 1. The four properties, from data

| Property | Where it comes from |
|---|---|
| Conserved, and cold in the expanding universe at 5.41 times the baryons | CMB peaks, CMB lensing, growth rate (CO1, CO2) |
| Passes through itself and through gas | the Bullet's offset (RB1) |
| Hot and at full share in clusters | clusters at the ceiling (RB1; XCV1 under its post hoc reading) |
| Locked to the baryons in galaxies, with no second halo beside the law | the cold component's shape from raw data (SHP1) |

## 2. What the record already closes

| Class of medium or theory | Verdict | Lane |
|---|---|---|
| Any local, momentum-conserving medium whose equilibrium is the law and which self-gravitates normally | NO-GO, a theorem: the stress that makes the law an equilibrium for every baryon profile is unique, cannot depend on the medium's density, is not an attractor, and cancels the medium's own self-gravity | M5 |
| Any local selector that holds the cold mass (gates in theta and u, label-free tethers, any local hold, pressure, potential depth, density) | closed by theorem, six ways | Z1's family 6 (Theorems G and S, D-T', the mu-pincer, J1, V1) |
| One clock field with a dust term keyed on its offset, its expansion or its acceleration | NO VALUE; BREAKS AT TURNAROUND; BREAKS AT A1 | MK1, MK2; TK1; AKD1 |
| One clock field, the collapse itself; its sideways flux; a cluster state | BREAKS DOWN; ILL-POSED; no state at form B's dust constant | COL1; LFS1; CLS1 |
| A wall or switch between a law region and a dust region | closed on every exit | SWT1, HE1 and the switch lanes |
| The tethered medium (PAPER49's action) | does not resolve law against clumping: no self-gravity, so no growth | TM1 |
| Two phases, condensed and normal | NO-GO | PH1 |
| Superfluid with phonons (Berezhiani-Khoury class) | FAILS five gates | QX28 |
| Self-interacting, isothermal inner halo | FAILS | IJ1 |
| Dipolar medium (Blanchet-Le Tiec) | a ghost in its kinetic matrix; unscreened; its cold-matter limit fails at recombination | Z1 (K1 to K3) |
| A light fermion beside the law; a warm component beside the law | FAILS gate 1 at 5 of 6 masses; FAIL AT SEEDING | HF1; WM1 |
| The law as an emergent regularity of ordinary cold halos (route E) | retired by the owner on 2026-11-01 after its data gates failed | the 11-01 decision |
| Nonlocal, history and global actions | no candidate survives | FA3 |

M5's theorem has three hypotheses: local, momentum-conserving, normally self-gravitating. Dropping locality is FA3.
Dropping normal self-gravity is the tethered medium (TM1) and action (A) itself. That leaves dropping momentum
conservation by the medium alone: a medium that exchanges momentum and heat with something else.

## 3. The class the record had not tried: a medium coupled to the baryons

**The idea.** The law's halo is an isothermal halo with sigma^2 = (1/2) sqrt(G M_b a0) (FB1 note). That is half the
square of the baryons' own circular speed at the radius where their acceleration is a0. A collisionless medium in
thermal contact with the baryons only where their acceleration exceeds a0 would be heated to that dispersion and keep it
outside. It would dissipate infall energy, conserve its charge, need no dust term at all, and it is not an ideal medium,
so M5 does not apply. The record has one dissipative medium (the entropy-memory stress with heat transport under
`rebuild_2026_10_22/X48_native_cf_zoom/stable_stress_search/`, a route E construction whose cosmological formation was
left open). A search found no lane on a medium coupled to the baryons.

**What the contact requires.** A column of baryons with mean enclosed acceleration a0 has surface density a0 / (pi G).
For contact to switch on there, that column must be one optical depth, which fixes an opacity per unit baryon mass:

    kappa = pi G / a0 = 22.4 / 18.5 cm^2/g   (canonical / alt),   3.8e-23 / 3.1e-23 cm^2 per proton.

**It dies twice, on arithmetic** (`MEDIUM_DESIGN_check.out`):

1. **Recombination.** With that opacity the medium's mean free path against baryons at z 1100 is 26 / 31 pc, about
   7,000 times smaller than the Hubble radius. At the 30 km/s relative speed a decoupled cold component has against the
   plasma, its drag rate is 0.73 / 0.61 of the expansion rate at z 1100 and 3.2 / 2.7 at z 3400. The cold component
   that fits the acoustic peaks has to stay decoupled from the plasma. This one does not.
2. **The Bullet.** A cluster's gas column of 0.006 to 0.03 g/cm^2 is 0.1 to 0.7 optical depths. The medium would be
   dragged with the gas, where the lensing mass is seen to pass through with the galaxies.

**The only repair is already in the record.** Restricting the contact to condensed baryons at low relative speed removes
both failures. That is PAPER49's tether, stated there as a postulate and scored by TM1: no growth, satellites fail,
cluster cores fail.

These are hand estimates with stated inputs, not a Boltzmann computation and not a lane.

## 4. What is left

- **One engineered function:** a single kinetic function with a narrow interval of changed compressibility (DT2). Its
  linear and static checks pass; whether a forming halo can reach its static state is not computed.
- **Form B as rules:** complete as a predictive theory. Every row of `THEORY_ASSEMBLED_2026-11-10.md` is computed from
  the falling state, the standing state and the counting rule, without the joint.

## 5. What is not claimed

No completion exists. The table in section 2 quotes lanes; it does not prove that no theory can exist, only that every
class named here has a failing verdict. Section 3 is one evening's design work on a class nobody had laned, and its
kill is arithmetic, not a graded result.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
