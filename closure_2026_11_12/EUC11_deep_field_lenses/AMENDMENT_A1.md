# EUC11 AMENDMENT A1 (post hoc; disclosed)

2026-11-12. Committed alone, after the first fetch stage (deep MER objects and photo-z at the lens positions) and
**before any grism row of any lens or control has been queried and before any `b` has been computed**.

## What happened

Check K2 as frozen reads: "at least 90 % of L have a lens object within 0.6″". The first fetch stage gives 460 of 576
(79.9 %). **K2 as frozen FAILS, and the lane's frozen word is therefore NOT EVALUABLE.** That word stands.

The cause is footprint, not association: 94 of the 576 Q1 lenses (81 in EDF-South, 13 in EDF-North) have no DR1
deep-survey MER object within 3″ at all, so they lie outside the area the DR1 deep catalogue covers. Of the other 482,
460 have a lens object within 0.6″ and 22 have only a more distant object. K2 was written to test association quality
and did not allow for the Q1 area being larger than the DR1 deep catalogue.

## The amendment

Everything below is reported as "under A1" beside the frozen word; it does not replace it.

- **Footprint.** A lens is inside the DR1 deep catalogue if at least 5 deep MER objects lie within 30″ of its
  position (one count query; the catalogue holds tens of objects per 30″ circle). Lenses outside are dropped and
  counted.
- **K2 (A1).** Of the lenses inside the footprint, at least 90 % have a lens object within 0.6″.
- Every sample, gate, reading, check and twin of the frozen criteria is otherwise unchanged and is applied to the
  lenses inside the footprint.

## Seen when this was written

The counts above, the nearest-object distance histogram of the lens positions, and that 458 lens objects have a
photo-z and an H flux. No Einstein radius or Sérsic value has been summarised, no mass predicted, no grism row fetched.
