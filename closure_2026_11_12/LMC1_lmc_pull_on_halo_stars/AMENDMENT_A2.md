# LMC1 AMENDMENT A2 (2026-11-12, written before run 3)

## What happened

Run 2 (`lmc1_run2_K4_FAIL.out`, after A1) passed K6 and K1 and stopped at K4: the LMC's Galactocentric distance
from the frozen inputs is 49.082 kpc, against the frozen reference 50.1 +/- 1.0 kpc (fails by 0.02 kpc).
Speed 320.09 (321 +/- 24), v_rad 68.19 (64 +/- 7), v_tan 312.74 (314 +/- 24) pass. No simulation of tracers
had been run and no star had been read.

## Why

The frozen reference 50.1 kpc is wrong as a Galactocentric distance. It is the HELIOCENTRIC distance that
Kallivayalil et al. 2013 adopted (distance modulus 18.50), copied into the repository's hunt_2026/h37 notes as
"50.1 kpc, Galactocentric". With that heliocentric distance the published Galactocentric position is about
(-1, -41, -28) kpc, |r| about 49.7 kpc (PROVISIONAL: from memory, magnitude checked by a web summary,
components not found in a primary source). This lane uses Pietrzynski et al. 2019's 49.59 kpc, which
scales the published |r| to about 49.2 kpc. The computed 49.08 agrees with that.
Disclosure: this reference was changed AFTER the computed value 49.082 was seen. It is not blind.

## Change (nothing else changes)

A2.1 K4 r_GC: |r_GC - 49.7| <= 1.0 kpc (published Galactocentric position at K13's distance), and each
     Cartesian component within 1.0 kpc of (-1, -41, -28) kpc after scaling by 49.59 / 50.1 (reported, also
     a gate). Speed and velocity checks unchanged.

The failed output is kept.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
