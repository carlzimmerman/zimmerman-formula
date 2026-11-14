# RB1R LEAD CHECK (2026-11-14): commit ids, the lead's re-run, the blindness check, and the comparison with RB1

Written by the lead session after the blind result was committed. TEST lane; adopts nothing, relabels nothing.
The blind agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| WHAT_I_SAW_AT_START.md + frozen criteria (alone) | d741bc73b4 | 4abf33b426 |
| script and run outputs | 1f972bcd8b | f2db75337d |
| RESULT_BLIND.md | 097c0d1e39 | 1efa457d33 |

## The lead's re-run

`rb1r.py` copied alone into a new folder at the same depth (not committed, removed afterwards) and run from scratch:
`rb1r.out`, `rb1r.json`, `rb1r_MUTATE.out` and `rb1r_MUTATE.json` are byte-identical to the committed files.

## Blindness

- The agent's tool calls were listed by script (30 calls). It read two files: the house rules and its specification.
  It opened nothing in RB1's, PD1's, XCV1's or TR1's folders, no scorecard, no papers folder and no memory folder, ran
  no repository search for X-COP terms, and did not use the web.
- Its starting context (`WHAT_I_SAW_AT_START.md`) held memory-index lines that name lanes by id only. None carries an
  X-COP number or word. The commit subjects it was shown did not mention X-COP. The lead's reading: no leak.
- The specification handed over was RB1's frozen text for the X-COP class (form B, the statistic, the two lines, the
  known answers and M1), without RB1's hand estimates. The two-sided word was added by the lead, who had read RB1's
  result; the agent was told so and was not shown the numbers. The word only names the conjunction of RB1's two frozen
  lines (ceiling 1, floor 0.85).

## Comparison with RB1 (made after the blind result was committed)

| quantity | RB1 | RB1R (blind) |
|---|---|---|
| graded class, 7 clusters, last radius, M_FORW | 1.095 [0.885, 1.259] | 1.095 [0.885, 1.259] |
| per cluster (A1795, A2029, A2142, A2319, A644, A85, ZW1215) | 0.885, 0.934, 1.235, 1.259, 2.216, 1.095, 0.511 | the same to three decimals |
| clusters above 1 at more than 2 sigma | 3 | 3 |
| RB1's lines | ceiling CONSISTENT; floor (T2) holds, upper end 1.259 against 0.85 | both lines hold: AMOUNT CONSISTENT ON BOTH SIDES |
| at R500 (reported) | 1.057 [1.046, 1.072], over the ceiling | 1.057 [1.046, 1.072], over the ceiling |
| R = 5.562 (reported) | 1.126 [0.910, 1.294] | 1.126 [0.910, 1.294] |
| all 12, imputed stars (reported) | 0.982 [0.859, 1.165] | 0.938 [0.904, 1.165] |
| NFW-fit hydrostatic mass, last radius (reported) | 1.032 [0.931, 1.174] | 1.031 [0.932, 1.174] |
| hydrostatic bias b = 0.1 (reported) | 0.966 | 0.966 [0.784, 1.107] |
| M1, R x 2 | bites | bites: 2.191 [1.770, 2.518] |

Reading:

- **The blind build reproduces RB1's X-COP class exactly**, and both of RB1's frozen lines read the same. The one
  bracket that differs is the 12-cluster one, where the two builds impute the missing stars differently; its word is
  the same.
- **Under RB1's own frozen lines the amount is consistent on both sides at the graded aperture, and it sits at the
  ceiling.** The median is above 1. The reported bracket at R500 is over the ceiling beyond its interval in both
  builds. Two of the four other mass models in the files (isothermal, Burkert) read over the ceiling; the NFW and
  Einasto fits do not. XCV1's caustic masses, which do not assume hydrostatic equilibrium, read 1.37 [0.74, 2.62] on five clusters (its
  post hoc A1).
- **What the scorecard quotes for row 15 is not form B.** The row reads FAILS on PD1's "FAIL +0.16". In PD1's result
  that number belongs to the reading with half of the share kept out of the core (the groups row of the same table
  names "prefactor 1/2"), where X-COP is under-filled. PD1's own bracket with the full share inside, "Cluster prefactor 1", reads
  "X-COP PASSES on both footings (+0.019 / +0.010"; RB1 used those two numbers as its known answer KA-1. Form B puts
  the whole share inside the system's edge. RB1's sentence that "the two-sided amount gate stays FAIL as PD1 graded
  it" names the groups (0 and 9 of 20) and the Bullet subcluster, not X-COP. So for X-COP the risk to form B is on the
  other side from the quote: too little cold mass for 5.41 times the baryons, not too much.
- **The scorecard word for row 15 is not changed here.** That is the owner's decision. The lead's suggestion is to
  re-source the row to RB1 and RB1R and read it as depending on an untested assumption (the hydrostatic mass to about
  10 per cent, the aperture), with the ceiling named as the live risk.
- **RB1's reported h bracket used the wrong exponent.** It scales the gas fraction as h^-1/2. At a fixed angle the gas
  mass goes as h^-5/2, the hydrostatic mass as h^-1 and the stellar mass as h^-2, so the gas fraction goes as h^-3/2
  and the stellar fraction as h^-1. The blind agent flagged this and ran both. The lead re-ran a scratch copy of
  `rb1r.py` (not committed) with the footings' own h (0.6741 canonical, 0.6740 alt, from QX15's main background):
  RB1's exponent gives 1.120 [0.903, 1.287]; the standard exponents give 1.172 [0.944, 1.349]. Both are consistent
  on both sides. At h = 0.65, which the blind agent used as a stand-in, the standard exponents read 1.252
  [1.006, 1.443], over the ceiling. Reported, post hoc, not graded.
- What this confirmation covers: the arithmetic of the frozen class, done twice with separate code. What it does not
  cover: the public profiles and the hydrostatic assumption, which both builds share; seven systems, so the interval
  ends are single clusters; A644, whose tabulated hydrostatic mass falls with radius beyond about 1.1 Mpc and gives
  its 2.22 (the blind agent's post hoc reading without it: 1.015 [0.698, 1.247], the same word).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
