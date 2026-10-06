# CFG364 FROZEN CRITERIA: does the supply cap (dark mass = min(phantom, cold supply)) survive real galaxies?

Committed alone, before any script. kappa = 1/2 FITTED and fixed. nu_mono. No dark-matter particle species: the cold MASS is
still required and is kept. No knob scans. Never "theory closed". Owner (2026-10-06, chat "Nobel Prize and neutrinos"):
"yes run the supply cap test". The orchestrator was told first.

**Why.** CFG363 (additive bookkeeping) over-lenses. CFG361 (B's T5 max) is still ~20% high in early runs. A supply cap
removes the double counting by construction: if the phantom IS the cold fluid, it cannot outweigh the fluid that is there.
In bound systems, dark mass = min(M_ph, S). Its make-or-break question: how many real galaxies need more phantom than their
supply? The cap would deny them the law exactly where the law is measured to work. Already in the record: CFG245 (the
relaxation dynamics toward min(M_ph, S) failed on timescale; the static cap was never scored on galaxies) and CFG336
(the ultra-faints exceed the whole share by 1.6-11x).

## Data and model (declared)
- SPARC: 175 rotmod files + the master table, read with CFG4_common.load_sparc (the record's loader). Upsilon_disk = 0.61,
  Upsilon_bul = 1.4 Upsilon_disk (STANDING). Both footings (a0 = 9.3603e-11 / 1.1312e-10), never pooled.
- At the last measured radius R_last (spherical, enclosed-mass reading):
  - M_bar(<R) = V_bar^2 R/G;
  - law phantom M_ph(<R) = (nu_mono(g_bar/a0) - 1) V_bar^2 R/G;
  - observed dark M_obs,dark(<R) = (V_obs^2 - V_bar^2) R/G.
- Supply S = (Omega_c/Omega_b) M_b = 5.364 M_b:
  - PRIMARY S_tot uses the galaxy's TOTAL baryons from the table, M_b = 0.61 L36 + 1.33 M_HI (the bulge share of L36 is not
    separated; the disk Upsilon is used for all of L36, disclosed);
  - STRICT S_in uses M_bar(<R_last). Reported only.
- Q = M_ph(<R_last)/S. Q > 1 means the cap breaks the law AT THE DATA. The phantom keeps growing beyond R_last, so this is a
  LOWER BOUND on the cap's problem (the test is generous to the cap).
- The observational version Q_obs = M_obs,dark(<R_last)/S is model-independent, reported alongside.
- Classes by V_flat (table): dwarfs < 60 km/s, intermediate 60-150, massive >= 150; no V_flat = "unclassified". Q <= 2
  subset reported.

## Tests
**T0 (controls).**
- T0a: the law's weighted rms about SPARC at the record's Upsilon reproduces 0.098 +- 0.005 dex (canonical; the
  build-script value).
- T0b: the phantom identity (nu - 1) g_bar R^2/G = (V_law^2 - V_bar^2) R/G holds to 1e-10.
- T0c: Omega_c/Omega_b = 5.364 from 0.1200/0.02237.

**T1 (the verdict statistic: PRIMARY, canonical, all 175 with valid data).** f_break = the fraction with Q > 1.

## Verdict classes (declared)
- **VIABLE:** f_break <= 10%, AND no massive galaxy (V_flat >= 150) breaks, AND fewer than 25% of intermediates break.
- **DEAD:** f_break > 30%, OR more than 10% of massive galaxies break.
- **MARGINAL:** anything else. Name which classes break.
- Report both footings and S_in separately. Never pool.

**MUTATE.** Supply x 0.1. f_break must rise above 30%, so the verdict flips to DEAD, and the main-run controls check
(MUTATE expected verdict) fails, rc = 1.

Local compute only. No downloads.
