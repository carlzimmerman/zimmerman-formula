# CFG850 — does the red/spheroidal low-g lensing excess survive the known LePhare M★ bias?

Criteria: `FROZEN_CRITERIA.md` (3cd64882b, before the script; first ID of owner block 850–859). Run: `python3 cfg850.py`
(MUTATE `CFG850_MUTATE=1`). Seconds.

## Result — CLASS: **SPLIT SURVIVES** (smaller, not erased)
At the dwarfs' g_bar, canonical (alt in the .out, same pattern):
| shift applied to red/spheroidal M★ | A_red | A_blue | colour split | A_sph | A_disc | Sérsic split |
|---|---|---|---|---|---|---|
| none (= CFG829/849) | 1.587 | 1.016 | 5.0σ | 1.602 | 1.066 | 4.6σ |
| **+0.123 dex (CFG667's measured LePhare–Taylor offset)** | **1.451** | 1.016 | **4.0σ** | 1.486 | 1.066 | 3.8σ |
| +0.20 dex (bracket) | 1.324 | 1.016 | 2.9σ | 1.357 | 1.066 | 2.7σ |
| +0.123 red, +0.05 blue | 1.451 | 1.017 | 3.9σ | 1.486 | 1.022 | 4.1σ |

- After the known stellar-mass correction, red / spheroidal isolated lenses still sit ~1.45× (+0.16 dex) above the law at the
  dwarfs' accelerations, blue / disc lenses on it (4σ). The excess is partly stellar-mass (it shrinks by ~0.04 dex) but not
  explained by it. MUTATE (a +0.8 dex M★ error) erases it, as it should. K1 reproduces CFG829/849.
- **Reading:** the empirical rule stands, with a corrected amplitude: at g_bar ≲ 10⁻¹² m/s², rotating / gas-rich systems obey the
  law; spheroidal / gas-poor systems carry ~+0.12–0.16 dex (lenses) to ~+0.44 dex (satellite dSphs) more. CFG848 shows maximum-
  entropy relaxation does not produce it; the cause remains open.

κ = ½ fitted; cold energy mass required; not theory closed.
