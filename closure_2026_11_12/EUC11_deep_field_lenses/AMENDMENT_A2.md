# EUC11 AMENDMENT A2 (disclosed; before any grism row and before any `b`)

2026-11-12. Committed alone. At this point the lane has fetched only the deep MER objects and photo-z at the lens
positions (as when A1 was written) and three 30″ footprint chunks; **no control has been drawn, no grism row of any
lens or control has been queried, and no `b` has been computed**.

## What happened

The frozen criteria draw control candidates from 20″–300″ around each lens. A 300″ cone in the deep catalogue holds
about 16,000 objects, the archive applies the flux filter after the spatial join, and the join costs about 23 s per
lens (70 s for three lenses, measured). A synchronous job is ended after about five minutes, so the frozen query fails
for any useful chunk, and one lens at a time would take about three hours for 458 lenses.

## The amendment

- **Control annulus: 20″–100″** instead of 20″–300″. The same cuts, the same draw (six at random, seed 20261112,
  sorted by object id), the same photo-z match and the same limit of three controls per lens. The probe at 300″
  returned about 70 candidates per lens, so about 8 per lens are expected inside 100″.
- Nothing else changes. Results stay labelled "under A1" (footprint) "and A2" (annulus); the frozen word is still
  NOT EVALUABLE (A1).

## What this could change

Controls nearer the lens share its depth and dither pattern more closely, which is what the null needs. They are also
more likely to sit in the lens's own group; a group member is still a non-lens galaxy of matched brightness and
photo-z, and the 20″ inner limit keeps the lens's arcs out of every control aperture (largest aperture 3″).
