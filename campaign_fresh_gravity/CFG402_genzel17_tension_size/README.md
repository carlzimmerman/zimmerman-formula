# CFG402: how strong is CFG401's "possible high-z tension"? One galaxy

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 1d58728ee. CFG401's shape and data code is reused read-only. Light CPU (niced).

**Frozen verdict (primary shape: stars + gas at 2 R_d):** WEAK (canonical, summed DE penalty 7.99) / TENSION REAL (alt, 9.63). This sits on the 9 line.

| summed chi2 penalty vs each galaxy's own best a0 | DE-tracking law | rival a0 ~ H(z) | pure Newton |
|---|---|---|---|
| gas 2 R_d, canonical | 7.99 | 21.31 | 15.51 |
| gas 2 R_d, alt | 9.63 | 23.31 | 15.52 |
| stars-only, canonical (reported) | 12.47 | 18.91 | 46.84 |

**POST-FREEZE (labelled, `cfg402_robustness.py`): it is ONE galaxy.**
- Without zC 406690 the other five sum to **2.05 / 2.46**: noise.
- zC 406690 alone costs **4.0-5.9** across its inclination prior (13 / 25 / 37 deg). That makes it a ~2-2.4 sigma single-object outlier, the steeply falling curve (outer slope -2.36). It also carries the sample's largest systematics: gas fraction 0.70 (prior), sigma0 = 74 km/s (pressure), and a poorly known inclination.

**Reading.**
- STANDING's "possible high-z tension" should read: **one ~2 sigma outlier (zC 406690). The other five Genzel+2017 discs are consistent with the DE-tracking a0(z) within noise.** It is not a sample-level tension.
- Reported, not a claim: in every shape the rival a0 ~ H(z) pays 2-3x the DE law's penalty. Pure Newton (no boost) is ALSO penalised (15.5) relative to the best-fit a0, driven mainly by COS4 01351. These six discs need some boost, of about the local size.
- This is NOT a measurement of a0(z): the shapes are declared, not measured, there are 6-8 points per disc, and CFG401's consistency gate failed. Nothing here says the data favour the framework.

MUTATE (errors halved) multiplies every sum by about 4.0 (e.g. 7.99 -> 31.95), as expected, rc 1.
