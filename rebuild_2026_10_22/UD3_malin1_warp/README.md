# UD3: Malin 1 with a warped outer disc. Primary NOT RESCUED; a reported outer-two-ring warp fits on canonical only

κ = ½ FITTED; not theory closed; footings never pooled; not blind; one galaxy excludes nothing. Criteria:
FROZEN_CRITERIA.md (2dd7a0b513), committed before any number. Run: `python3 ud3.py` (under 1 s; reads UD2's committed
ud2.json). Outputs ud3.{out,json}.

The warp follows Lelli+2010: the position angle is constant inside 24 kpc and ramps outside it. Each warped ring's V and
error are scaled by sin 38° / sin i(R). The law is as UD1/UD2.

## Labels at i_out = 32° (the authors' "cannot be ruled out" value)

| model | baryons | canonical χ²/4 | alt χ²/4 | i_out with p ≥ 0.05 (canonical / alt) |
|---|---|---|---|---|
| **step, R > 24 kpc (primary)** | fixed | 113.2 FAIL | 68.5 FAIL | none / none |
| step, R > 24 kpc | deprojected | 107.8 FAIL | 66.6 FAIL | none / none |
| ramp from 24 to 101.6 kpc | fixed | 19.5 FAIL | 48.6 FAIL | none (best 28.0°, χ² 9.8) / 23.0-25.7° |
| ramp | deprojected | 21.6 FAIL | 52.5 FAIL | none / 22.3-25.1° |
| step, outer two rings only | fixed | **2.5 CONSISTENT** | 29.8 FAIL | **29.5-33.6°** / none (best 30.1°, χ² 22.8) |
| step, outer two rings only | deprojected | **3.3 CONSISTENT** | 32.5 FAIL | 29.0-33.3° / none |

**Frozen verdict, both footings: NOT RESCUED.** The primary step starts the warp where the position angle breaks
(24 kpc), so it also tilts the 37.5 kpc ring. That pushes the ring to 251 km/s against a law value of 219-228 (error
±2.6 × 1.16). No i_out in 15-60° then reaches p ≥ 0.05.

**Reported, not the frozen escape:** if only the outer two rings (62.5 and 87.5 kpc) turn to 32°, the canonical footing
fits, χ² 2.5/4, for i_out 29.5-33.6°. That is within the paper's 6° and within 2σ of i0, with or without the
deprojection. This is how the paper's "outer parts" can be read. The alt footing still fails there. Its blocker is the
37.5 kpc ring, where the law gives 228 km/s against the observed 216.2 ± 2.6, whatever the outer rings do. The alt ramp
fits only at i_out 23-26°, a 12-15° turn, beyond the stated 6°.

So for Malin 1 the result hangs on where the warp starts, which the data cannot fix. The paper itself could not
constrain i(R).
- Canonical: survives a warp of the two outermost rings to ~32°. It fails if the warp begins at the position-angle break.
- Alt: fails in every 32° model.

## Checks

- K0: every model at i_out = 38° returns UD2's χ² (69.0 and 132.5) exactly. PASS.
- K1: no optimiser. PASS. Rerun: byte-identical.
- K2 (printed beside): the paper's own MOND-fit curve under the 32° step gives χ² 195/4. It is computed by the same code
  path; it is not a pass/fail.

Nothing here is a verdict on a theory. UD1 (AGC 114905) is unaffected: its inclination comes from deep optical imaging
and the HI, and the law needs 12-16° there.
