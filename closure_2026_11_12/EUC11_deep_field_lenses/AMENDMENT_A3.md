# EUC11 AMENDMENT A3 (disclosed; before any grism row and before any `b`)

2026-11-12, late evening. Committed alone. Nothing new has been seen since A2: the lane holds the deep MER objects and
photo-z at the lens positions and control-candidate rows (object id, position, H flux) for part of the sample. **No
control has been drawn, no grism row of any lens or control has been queried, and no `b` has been computed.**

## What happened

Under A2 the control-candidate query (a 100″ cone around each lens with the flux filter) costs 6 to 17 s per lens at
the archive tonight and hits the five-minute job limit in chunks of 20: in about three hours it completed the
requests for 200 of the 458 lenses that have a lens object, a photo-z and an H flux, returned an empty result twice for
one chunk at the time limit, and then failed outright.

## The amendment

- **Part 2 (the source search and its null) is run on the lenses whose control candidates were fetched:** the 200
  lens positions at indices 0–139 and 160–219 of the 458, in identifier order (the order of the fetch). The list is
  written to `cand_covered.csv` by the fetch script. The same rule, tiers, gates and reading apply, with L and C
  restricted to those lenses and their controls.
- The subset is fixed by fetch order, not by any property of the lenses. Identifiers begin with the tile index, so
  the subset is a set of whole tiles, not a random draw; lenses and controls share tiles by construction.
- **Part 1 is unchanged** and uses every lens inside the footprint (it needs no controls).
- Results stay labelled "under A1, A2 and A3"; the frozen word is still NOT EVALUABLE (A1).
