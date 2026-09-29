# CFG75 -- the universal-debris-fraction verdict against the acceptance level

**Why (declared after a referee audit, not before any run).** CFG59 and CFG71 answer 'is there a phi in [0,1] inside every population's 1 sigma interval?' with NO. A referee recomputed from the same committed scan tables that the answer depends on the acceptance level. This lane reproduces that from the committed tables only (no new data, no new model): `CFG75_phi_acceptance.py`.

**Result.**
| populations | 1 sigma | 2 sigma | 3 sigma |
|---|---|---|---|
| CFG59 ten (canonical | alt) | empty | [0.52, 0.71] | [0.33, 0.66] | [0.17, 1.00] | [0.11, 1.00] |
| CFG59 nine, no X-ray (canonical | alt) | empty | [0.52, 0.71] | [0.33, 0.66] | [0.17, 1.00] | [0.11, 1.00] |
| CFG71 dynamical SLUGGS (canonical | alt) | empty | empty | [0.77, 1.00] | [0.71, 1.00] |
| CFG71 without SLUGGS (canonical | alt) | empty | [0.23, 0.71] | [0.21, 0.66] | [0.12, 1.00] | [0.11, 1.00] |

So: NO at the frozen 1 sigma-per-population acceptance; at 2 sigma CFG59's ten populations DO share a common phi of about 0.5-0.7 (canonical) and 0.33-0.66 (alt); with SLUGGS's dynamical masses (CFG71) the 2 sigma intersection is empty only through SLUGGS (2.6 sigma at phi = 1); at 3 sigma all ten CFG71 populations share phi of about 0.7-1. Requiring ten independent populations to all sit inside 1 sigma of a true universal phi has probability of order 0.68^10, about 2%, so the 1 sigma NO is a demanding statement. **The verdict is a statement about tight consistency and about the shape of the tension (SLUGGS wants more than all the sum's debris, the low-mass dwarfs want less), not that any fraction is excluded at 2 sigma.** A 1 sigma band is the strict criterion, not a loose one (CFG59's remark 'the 1 sigma band is loose ... a YES would have been weak' is imprecise).

**Controls.** C1: the 1 sigma intersections are empty on both footings for CFG59 and CFG71 (the committed answers). C2: the 1 sigma SLUGGS and M31 LVD segments reproduce the committed ones. MUTATE (every error x 0.5) makes the 2 sigma claim fail, rc 1. `python3 CFG75_phi_acceptance.py` (rc 0); `MUTATE=1 python3 ...` (rc 1). Nothing here says the data favour the framework; the sum's failures at 1 sigma (CFG42/58/71) stand. kappa = 1/2 is FITTED.
