# CFG651 — does THEORY v2's condensed-source rule (A5) predict the early-type age signal? FAILS (both footings): A5 predicts the WRONG SIGN

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (5a24ec013).
- **POST-HOC MECHANISM TEST, NOT A BLIND PREDICTION.** The age signal was already seen (CFG585/586/631; CFG700 on raw ESD).
- **Script:** `cfg651_predict.py` → `cfg651_predict.out`, `cfg651_results.json`. MUTATE `CFG651_MUTATE=1` → `_MUTATE`.
  One process, nice 10, peak RSS 1.18 GB, 5 min (MUTATE 2.5 min). No downloads.
- **Settings:** κ = ½ FITTED. Footings canonical 9.36e-11 / alt 1.13e-10, never pooled. "Cold energy"; its mass is still required.
  Not theory closed. No ΛCDM or standard-MOND yardstick in the verdict. The CFG531 covariance used by the secondary D carries an
  SHMR term (labelled context). The primary A is own-law-only, with no environment term.

## Why A5 has only one lever here
The record's lens source is already the condensed source: M_gal = M*(1 + f_cold(M*)), stars plus cold gas (CFG634 T6a). It depends on
M* only, so OLD and YOUNG at fixed M* get the same source. Under A5 the only age lever is a colour-dependent cold-gas share. Hot gas
is not a source. The census also gives no hot gas to work with: the f30 hosts sit at log M_ta 10.9–12.6 [Msun/h], and 89% of the f30 groups are below
the 12.5 knee, where f_ret = f_c = 0.10 (CFG515/CFG640).

## Result (K9; A vs CFG700 raw ESD A = +0.166 ± 0.071; D vs CFG585 +0.941 ± 0.354 canonical / +0.862 ± 0.324 alt)
| route | A_pred can / alt | D_pred can / alt | class (A; D) |
|---|---|---|---|
| **R2 PRIMARY: LePhare sSFR-weighted cold gas** | **−0.061 / −0.061** | **−0.145 / −0.144** | **FAILS; FAILS** (wrong sign, 3.2σ / 3.1σ off) |
| R1 census / assembly-epoch bound | +0.001 / +0.001 | +0.003 / +0.003 | TENSION; TENSION (does not account) |
| R3a ceiling: all record cold gas in OLD | +0.087 / +0.087 | +0.212 / +0.211 | CONSISTENT; TENSION |
| R3b phase ceiling: OLD sources all retained baryons | +0.017 / +0.017 | +0.041 / +0.041 | TENSION; TENSION |

Equal-source baseline A_base = −0.0001 on both footings (composition only).

- **VERDICT (frozen, primary R2): FAILS on both footings. A5 DOES NOT ACCOUNT FOR the age signal; it predicts the opposite sign.**
  At fixed M*, YOUNG early types have median log sSFR −10.4 and OLD −14.2. A cold-gas share that follows the measured SFR puts
  more condensed source in YOUNG (mean Δf +0.21 vs −0.13 of M*). Their law phantom is then larger, so A < 0 and D < 0.
- **Verified as hard as a win:**
  - The sign does not depend on the proxy's normalisation. Any cold-gas share that rises with SFR gives YOUNG more condensed
    baryons, because the two groups differ by 3.7 dex in median sSFR. Only a cold-gas share anti-correlated with star formation
    could flip it.
  - The size is the deep-regime √M_p scaling: (1.38/1.04)^½ → |A| ≈ 0.06, which matches.
  - Linear and exact tables agree within 2% (M3).
- **Ceiling:** R3a reaches A's 2σ band (+0.087), but D stays in TENSION, and R3a is unphysical. It gives the reddest, near-zero-sSFR
  early types about 0.5 M* of cold gas and the star-forming ones none. The only census-based ceiling, R3b, gives +0.017, 10% of the
  signal. Within the record's census and the measured SFR ordering, A5 cannot produce the signal.
- **MUTATE 6/6:**
  - M1: the all-baryon source (candidate B) gives an increment of exactly 0 on A and D. The age term above comes only from A5's
    phase split.
  - M2: 200 shuffled-age relabellings give mean −4e-5 (sd 7e-4). The real-label −0.062 lies below all 200.
  - M3: linearity holds.
- **Controls 5/5:**
  - C1: CFG700 A reproduced to 1e-5.
  - C2: CFG585 D reproduced (+0.9411).
  - C3: SFR coverage 99.98%.
  - C4: Δ median log M* −0.0001.
  - C5: the law_vecs copy matches CFG531 to 1e-12.

## Implementation note (disclosed)
The criteria said `law_vecs` would be used unedited at 10^dl − 1 = Δf. The record's f_cold exceeds 1 at low M* (log M* ≈ 9.5). A
gas-poor OLD lens there has Δf < −1, which dl cannot represent. `law_vecs_df` is a verbatim copy that sets M_p = M_g + M*·Δf
directly. It equals `law_vecs` where both are defined (C5), and the bin radii stay fixed by the data's M_gal, as in `law_vecs`.

## What it means
- Theory v2's A5 does not supply the age mechanism. A5 makes the age signal harder, not easier, because star-forming (young) early
  types carry more condensed source.
- Open problem 4 (the early-type age signal) stays open. The candidates left on the record are:
  - the settling-time reading (v1 eq. 5 with α; not tested here);
  - CFG700's LePhare mass-bias nuisance: if the reddest galaxies' M* is biased low, OLD is truly heavier.
- Any v2 extension that explains the age signal must overcome this −0.06 A5 term, not just add to zero.
