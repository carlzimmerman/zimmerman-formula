# CFG629: is the merger cluster-core shortfall real? (quick check, 2026-10-11)

Post hoc diagnostic, no frozen criteria; it reads the CFG599 progenitors (`cfg599_lib.Progenitor599`) and adds no new model.
Run: `python3 cfg629_supply.py` → `cfg629_supply.out`, `cfg629_supply_results.json`.

**Question.** CFG625's static stage found the merger progenitors carry only 16–36% of the Bullet's strong-lensing mass inside
250 kpc (Paraficz+16, PROVISIONAL) and the assessment read that as "the law on measured baryons cannot reach the core mass".
But the merger lanes run CASE L: the unsettled cold-energy reservoir (candidate B's supply 5.364 M_b minus the settled phantom)
is set to zero. Does putting it back close the gap?

**Result (projected M(<250 kpc) / lensing, can = alt to 0.03):**

| progenitor | settled only | + unsettled (NFW c=4 placeholder shape) | whole system (all baryons + full supply) / lensing(<250) |
|---|---|---|---|
| main (M200 1.5e15) | 0.33 / 0.36 | **0.84** | 5.67 |
| sub (M200 1.5e14) | 0.16 / 0.18 | 0.19 / 0.18 | **0.71** |
| sub 4:1 (3.75e14) | 0.25 / 0.27 | 0.39 / 0.38 | 1.77 |

**Reading.**
- Main cluster: most of the shortfall is the case-L omission; with the reservoir it reaches 0.84 of the lensing mass (the
  reservoir's shape is an inherited NFW c=4 placeholder, so the exact number is not a framework prediction).
- Sub (the bullet): even the WHOLE system, every baryon plus the full cold supply, is only 0.71 of the mass measured inside
  250 kpc. No distribution can fix that: the sub's input mass (M200 1.5e14 from a simulation line) is too small for the
  measured lensing. The sub shortfall is a mass-INPUT problem, not evidence against the law.
- Caveat: the sub's projected lensing mass may include the main cluster's outskirts along the line of sight; the Paraficz
  numbers are recalled, not read from the paper.

**Consequence.** The assessment's "law cannot reach the Bullet core mass" is withdrawn as stated: the main-cluster gap is mostly
case L, the sub's is the input mass. Merger α verdicts (CFG621–625) remain provisional; a valid merger lane needs progenitors
with the full cold supply (settled + reservoir) and masses anchored to measured lensing/X-ray, not simulation M200.
kappa = 1/2 FITTED; cold energy mass required; not theory closed.
