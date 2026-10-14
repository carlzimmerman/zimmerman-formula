# CFG769 FROZEN CRITERIA: what condition do DF2/DF4/DF9 lack? Test the candidates, seal the out-of-sample predictions

Committed alone, before any CFG769 script exists. Last ID of block CFG760–769 (owner chat). Owner request (2026-10-14):
"what do these galaxies lack ... or what condition", then "dude yes pull what you need and do rigorously".

kappa = 1/2 FITTED; both footings (9.3603e-11 / 1.1312e-10), never pooled; no-EFE nu_mono (CFG655 frame; CFG4_common); the
cold energy's mass is required; no particle species; not "theory closed".

## Honest status (read first)
Every candidate below was named AFTER seeing the four trail dispersions (CFG655/657/768), so fitting the trail is worth
nothing. Each candidate is scored only on data it was not chosen from, or sealed for data that do not exist yet.

## Data pulled (owner's go, 2026-10-14; `_external_data/arxiv_cfg769/`, read from pdftotext of the PDFs, not summaries)
- Vaz+2026, arXiv 2610.07467 (sha256 da274d3b…0641): LEDA 4014647 V = 1600.7 +/- 1.3 km/s; sigma 15.8 +/- 2.0; "the stellar
  population properties of LEDA are inconsistent with membership of the trail as a collision product".
- Keim+2026, arXiv 2603.15860 (sha256 a952334f…d179): DF9 V = 1661 +/- 2 km/s.
- Tang+2025b, arXiv 2410.19331 (sha256 e8b26a94…251f): Table 1 (R_e major axis in arcsec, b/a, "on trail?") and Table 2
  (log M*, t_M) for every trail galaxy.

## The candidate conditions
**C-A6 (own supply).** Already the framework's rule A6 (CFG655): cold energy settles only from a system's OWN supply, the
cosmic share that arrived with its baryons. Collision debris formed from gas that separated from its supply (CFG657 channel S),
and CFG768 Part A showed a debris galaxy cannot acquire supply later (alpha_P = 0 under one c_P => capture ~1e-3). So C-A6
says debris are Newtonian FOREVER, and CFG763/764's clocks are read as the settling rate of a system's own supply, not
formation from nothing (this removes CFG768 B's conflict; it also removes the young-TDG lower bound on tau, since young TDGs
have no supply on this reading). Not scoreable on existing data beyond the trail (by construction) -> SEALED predictions only.

**C-SIGMA (compactness switch).** Cold energy is present iff the baryonic surface density inside R_e exceeds a threshold.
Trail values, Sigma_e = 0.5 M*/(pi R_e,circ^2), CFG655 inputs: DF2 7.96, DF4 9.33, DF9 18.4, LEDA 42.1 Msun/pc^2. The
threshold must lie above the debris and below LEDA. Lenient (fewest SPARC systems predicted Newtonian):
Sigma_crit = 18.4 x (1 - 0.23) = **14.2 Msun/pc^2** (DF9 at -1 sigma mass).

**C-REST (at rest in the medium) is NOT scored.** It assumed debris could acquire cold energy from the ambient group medium
if slow enough; CFG768 A closed acquisition for any speed (alpha_P = 0). Under C-A6 the motion through the medium is
irrelevant. LEDA's velocity is recorded for completeness only.

## Part 1: C-SIGMA on SPARC (the kill test; existing data the candidate was not chosen from)
- Sample: CFG4_common.load_sparc(); Q in {1, 2}, Inc >= 30 deg, >= 5 points.
- Sigma per galaxy: primary stars only, Sigma_* = 0.5 x 0.5 L36 / (pi R_eff^2); **verdict on the lenient value**
  Sigma_len = (0.5 x 0.7 L36 + 0.5 x 1.33 M_HI) / (pi R_eff^2) (more mass => fewer tested). Tested set: Sigma_len < 14.2.
- Fits per tested galaxy, both models with the same freedom: Upsilon_d free on a grid [0.10, 2.00] step 0.01, Upsilon_b =
  1.4 Upsilon_d; V_bar^2 = V_gas|V_gas| + Ups_d V_disk^2 + Ups_b V_bul^2 (signed gas as in the record). Newton: V^2 = V_bar^2.
  Law: V^2 = nu_mono(g_N/a0) V_bar^2, g_N = V_bar^2/R. chi^2 with the rotmod e_V. Delta = chi2_N,min - chi2_law,min.
- A galaxy "requires the boost" iff Delta >= 25 (5 sigma).
- **EXCLUDED** iff >= 10 tested galaxies require the boost, on both footings. **SURVIVES** iff none does. Else **TENSION**.
  Hand estimate (before any run): EXCLUDED; low-surface-brightness SPARC discs are the classic boost-dominated systems.
- Reported (no verdict weight): the same at Upsilon_d up to 5 for Newton (maximum-disc extreme); the stars-only Sigma set.

## Part 2: SEALED out-of-sample predictions (C-A6)
**2a. The six trail galaxies with no measured dispersion** (Tang+25b "on trail = Yes", in Table 2, not DF2/DF4/DF9/LEDA):
DF5 (RCP 11), DF7 (RCP 9), RCP 16, RCP 21, RCP 26, RCP 28. (RCP 17 and RCP 32 have no Table 2 mass; not sealed.)
- Inputs: log M* (Table 2), R_e,circ = R_e sqrt(b/a) (Table 1, arcsec -> kpc at D), D = 20 Mpc primary, 17.7 and 21.7 bracket
  (the measured trail range); r_1/2 = 4/3 R_e,circ; CFG655 estimator sigma^2 = nu_eff g_N r_1/2 / 3, g_N = G (M*/2)/r_1/2^2.
- Labels (pre-kinematic, vD+22 as quoted in CFG655): DF7 = T (named candidate remnant/interloper) -> sigma_law; the other five
  = E (debris) -> sigma_Newton. Both sigma_N and sigma_law are sealed for every galaxy, so a measurement scores either label.
- Kill rule, sealed: under C-A6, any of the five E galaxies measured with sigma inconsistent with sigma_N at >= 3 sigma and
  consistent with sigma_law is a FAIL for C-A6 (given the label); DF7 is scored against sigma_law.
**2b. Old tidal dwarfs** (CFG441/448/763): C-A6 says an old TDG stays Newtonian at any age; NGC 5557-E1 (~4 Gyr) circular speed
in the Newtonian band 16–24 km/s, NOT the law band 28–41 km/s (CFG763 Reading 3 / CFG441 bands; CFG763's from-nothing clock
predicts >= 68% filled). Sealed as stated; data not available (CFG448).
- Seal: the predictions JSON is written by the script, its sha256 is printed and recorded in the README and LEDGER.

## MUTATE (CFG769_MUTATE=1; separate outputs; exit 1 iff it bites)
Part 1 with V_obs := the Newtonian curve at Upsilon_d = 0.5 (same e_V): no tested galaxy may require the boost (verdict ->
SURVIVES). If it still reads EXCLUDED, the test is a construction failure.

## Not tested
EFE variants; distance/inclination errors in SPARC (Delta >= 25 is the margin); the physics that sets a galaxy's own supply.
