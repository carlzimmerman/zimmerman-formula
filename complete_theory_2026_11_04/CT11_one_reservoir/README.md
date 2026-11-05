# CT11_one_reservoir: CONVERSION DOES NOT DERIVE THE DUST AMOUNT. It moves CT8's pure number into a rate and an onset (M1, M2), an epoch or integration constant (M3), or a seed (M4). Every model that predicts a number FAILS G5 and the BAO check. G6, growth and the a0 tie not reached

Criteria `FROZEN_CRITERIA.md` (written first). Script `ct11_one_reservoir.py`; numbers `ct11_one_reservoir.out` (cited as out:line), `ct11_one_reservoir.json`. Vanilla CLASS 3.3.4, CT3's peak finder and raw TT file, DESI DR2 BAO table as transcribed in CFG681, Pantheon+ from prep_2026. 18 s on one thread, 0.42 GB. No download. Graded under owner decision D1 ("Yes, grade it"): a go to grade, not an adoption. The cold sector retired on 2026-11-01 stays retired. No particle. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## Why conversion cannot fix the number, in one line
A w = -1 receiver never dilutes, so whatever is transferred accumulates, and a transfer proportional to the dust is dominated by its earliest moment: rho_DE0 ~ (Gamma/H_on) rho_x(z_on). The link exists, but it runs through the onset epoch and the rate, which are new constants. A transfer proportional to rho_DE instead (the only clustering-safe form, CFG131) grows from a seed, which is an initial datum.

## The models
| | Model | Free constants | Where CT8's number goes | Prediction at the natural value | G5 | BAO |
|---|---|---|---|---|---|---|
| M1 | Q = Gamma rho_x, Lambda_bare = 0, onset z_on | Gamma, z_on | Gamma/H_Lambda = 1.1e-6 (z_on 3e4) to 7.8e-9 (z_on 1e6) (out:6-7) | Gamma = a0/c or de Sitter rate: omega_x(rec)/omega_b 3e-5 / 6e-6 (out:2-5) | **FAIL** 0.519-0.535 (out:15-16) | **FAIL** chi2 6744 (out:19-20) |
| M2 | Q = xi H rho_x (interacting DE) | xi, z_on | xi = 2.8e-13 (z_on 3e4), 7.7e-18 (1e6) (out:10); onset at a -> 0 diverges (out:8) | xi = kappa = 1/2 (hand choice): ratio 7e-13 (out:9) | **FAIL** 0.519-0.535 (out:17) | **FAIL** 6744 (out:21) |
| M3 | threshold / unified fluid (generalized Chaplygin, kinetic k-essence, sharp transition) | B/A or a_* (integration constant) | a_* = 0.731, z_* = 0.37 (out:12) | a_* = 1 (dust reaches the vacuum it becomes, today) = CT8's R5: ratio 13.7 (out:11) | **FAIL** 1.352-1.373 (out:18) | **FAIL** 522 (out:22) |
| M4 | Q = xi H rho_DE (autocatalytic) | xi, seed | the seed; dust amount stays the shift charge | none (out:13) | NO PREDICTION | not graded |

Check: CT3's row reproduces 0.992 (out:14). Window H3/H2 0.969-0.989, ratio 4.9-5.4.

## Reading
- **M1/M2 also fail before the amount matters.** With a Lorentz-invariant receiver and Q depending on rho_x, CFG131 D1 showed the dust has no comoving density contrast (growth ratio 2.7e-3). So even the fitted Gamma or xi that hits ratio 5.36 would not give dust that clusters. The CLASS runs treated the dust as clustering, the most favourable reading.
- **M3 at its fitted epoch collides with the record.** Full conversion at z_* 0.37 is close to Route C's line (clustering must survive to z < 0.30, commit 840d6ccfea). Route C used Planck LCDM numbers (pre 10-25 rule), so this is a note, not a grade. W4_09 already graded Chaplygin as a TRADE.
- **The approximation.** Dust at z >= 1090 was run as omega_cdm and the DE as a constant Lambda. For M1 at the natural rates, 21-74 % of the dust present at recombination converts by today (out:2-5), but that dust is 1e-7 of omega_b. At the fitted rates the fraction is below 1e-6 (out:6-7).
- **Background row.** The reference row (fitted omega_x 0.12, flat closure h 0.670) gives BAO chi2 46.8 (out:23). That is above the frozen 28.3 line too, so the line is tight with h set by closure. The model failures are 11-140x larger, so the verdict does not depend on the line. SN chi2 uses diagonal errors and is reported, not graded.

## Step 3 (not reached)
No model passed G5, so growth and the a0 tie were not graded. In M1/M2 at the fitted values, rho_DE is made at onset and is constant afterwards to 1e-6. The tie a0 = kappa c sqrt(G rho_DE) is then that of a constant Lambda: unchanged, but carrying no information about the conversion.

## Hand-set constants
kappa = 1/2 (M1 natural rate, M2's hand choice). M1: Gamma, z_on. M2: xi, z_on. M3: B/A or a_*, alpha. M4: xi, seed. Inherited from CT3: A_s, tau, YHe; n_s bracketed.

## Literature (from memory, provisional, not graded)
Adiabatic generalized Chaplygin needs alpha near 0 for the matter spectrum (Sandvik et al. 2004). Scherrer's purely kinetic k-essence (2004) has dust amount and vacuum level as independent constants.
