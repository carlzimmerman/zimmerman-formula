# VS2_rotation_vs_central: FROZEN CRITERIA, committed alone before this lane's script or fit

Owner's go, 2026-11-02: find a sample that separates rotation from being a central. VS1's slow rotators were also its four named centrals. Reinstates nothing. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** VS1's per-galaxy offsets are read, and the neighbourhood labels below were listed by galaxy before this file, with no offset joined to them. Radii and velocity windows were chosen before that listing; the primary was picked after it, because 300 kpc leaves no slow non-central in the 16. So the primary choice saw the labels.

## Labels, no download
Central: no brighter 2MRS (Huchra+12, on disk, Ks) galaxy inside projected R and |dv|. **Primary R 500 kpc, dv 500 km/s.** Reported: 300/500, 1000/1000. Known limit: the rule misses high-velocity satellites such as NGC 1400, and Virgo's large dispersion.
Slow: Emsellem+11 F/S at Re.

## Data
CFG323 primary offsets, 16 galaxies, both footings, mass `lMjamlaw`, as VS1. Quadrants at primary: slow central 4365, 4486, 5846; slow non-central 4374; fast central 1023, 2768, 3607, 4649, 4697, 7457; fast non-central the other six.
Reported row: off_sl (K-band mass) with NGC 3608, the one further slow non-central, from CFG330's code with its quality filter relaxed, if it runs.

## Fit and labels
OLS: off = a + b (log M - mean) + r slow + e central. Each with 1 sigma from scatter, 12 degrees of freedom.
- **ROTATION:** r >= 0.10 at > 2 sigma and e within 1 sigma of 0, both footings.
- **ENVIRONMENT:** e >= 0.10 at > 2 sigma and r within 1 sigma of 0, both footings.
- **UNDECIDED:** anything else. With one slow non-central at primary this is the expected outcome, stated now.

Also reported: mean offset of each quadrant; 4374 alone against slow centrals; collinearity between slow and central.
MUTATE: central labels shuffled within mass terciles; e must fall toward 0; separate outputs.
