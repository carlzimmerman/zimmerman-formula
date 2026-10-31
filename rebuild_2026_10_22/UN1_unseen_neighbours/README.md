# UN1_unseen_neighbours: neighbours below r 19.8 do not close route E's shortfall on clean lenses

Criteria: `FROZEN_CRITERIA.md` (2950d10ef6), committed before any script or number. Frozen run: `un1_grade.py`, `un1.out`, `un1_results.json`. `AMENDMENT_A1.md` (f1ad722b18 and its note), committed before any number from it: `un1_a1.py`, `un1_a1.out`, `un1_a1_results.json`, `un1_a1_MUTATE.*`. Post-result, reported: `un1_a1_efe.py`, `un1_a1_efe.out`, `un1_a1_efe.json`.

## Frozen class: SHORTFALL CLOSES. Void in substance, never quote it
That is what the frozen text outputs on canonical S1 at R2 (A_O1 1.89 → 1.05, law χ² about 4,850). It comes from two errors of mine:
1. MLIM is a 95th-percentile limit, and 57 % of catalogued neighbours lie below it, so visible galaxies were counted twice.
2. `am1_bmf.json`'s `all` is cumulative n(> M), and I read it as φ.

K1–K3 pass on the frozen run and could catch neither. The law's χ² was the alarm.

## Amended reading (post-result): NO HELP on S1 at R2, both footings, B 1 and 0.7, both n_ref
Only φ minus the catalogue's own density at each z enters. No parameter. K1 (B 0 reproduces SI2) 0, K4 1.7e-18, MUTATE φ × 1.3 raises the O1 term: all PASS.

| canonical, n_ref catalogue, B 1 | route E χ² (p) | route E A_O1 | δ | law y_e 0 χ² |
|---|---|---|---|---|
| S1 R2, no faint term (SI2) | 22.3 (0.099) | 1.89 ± 0.39 | +2.28 | 22.7 |
| **S1 R2, faint term** | **21.2 (0.132)** | **1.76 ± 0.36** | **+2.10** | 48.4 |
| S1 R0, no faint term | 24.4 (0.058) | 2.89 ± 0.60 | +3.17 | 15.8 |
| S1 R0, faint term | 22.4 (0.098) | 2.60 ± 0.53 | +2.99 | 44.3 |
| S3 R2, faint term | 8.5 (0.903) | 1.18 ± 0.70 | +0.25 | 30.5 |

The term adds about 0.1–0.2 M☉/pc² to route E at 0.4–0.75 Mpc, where σ is 1.1–1.8 and the data want about 1–2 more. It's too small by nearly an order of magnitude. Route E's δ falls by 0.18, and the frozen rule needs 0.5 for HELPS. S3's "SHORTFALL CLOSES" is no change: it had δ +0.84 at R0 before the term.

## The law's rise is its y_e = 0 superposition, not the data (`un1_a1_efe.py`)
With y_e = 0 the law gets about 35 replica tails per reference neighbour, added linearly, and its class on S3 moves to ROUTE E PREFERRED. AQUAL doesn't superpose that way. Under P2's catalogue external field (R0, n_ref catalogue, B 1):

| canonical, R0 | law y_e 0 | law catalogue field | route E |
|---|---|---|---|
| S1 | 15.8 → 44.3 | **11.3 → 10.4** | 24.4 → 22.4 |
| S3 | 17.8 → 26.5 | 14.4 → 14.8 | 12.6 → 12.1 |

Alt reads the same way: S1 12.1 → 12.1, S3 14.4 → 15.2. So **the ROUTE E PREFERRED lines in `un1_a1.out` must not be quoted.** They depend on a law model this test shows is the wrong one once faint mass is added. y_e = 0 is SI1's frozen L(a), and SI2's R2 rungs were not run with the field here.

## What this leaves
- Wound 10 is answered: unseen neighbours don't supply S1's 0.4–1.1 Mpc shortfall. It stands at about 2.1σ at R2, and at about 3σ at R0.
- Comparisons on SI1's and SI2's frozen L(a) are exposed to the y_e = 0 choice wherever neighbours matter. At R0 on S1, the law with its field has χ² about half route E's, with or without the faint term.

## Limits
Replicas take the reference band's positions, so faint galaxies follow its clustering (B 0.7 reported, B 1 generous). φ is 1/V_max on the same catalogue down to lg M_b 7.5. Not done: the law's field at R2, and any isolation effect on the replicas inside a veto radius. It doesn't test R2 or KiDS's Δχ².

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
