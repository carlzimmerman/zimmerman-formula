# EUC9 AMENDMENT A0 (PRE-DATA; disclosed)

2026-11-12. Written after the frozen criteria (bea4eacfa8) and **before the spectrum of any ECLIPSE lens or grade-X
object has been opened**. Committed alone, before any EUC9 script is in the repository. The frozen criteria are not
edited; everything in them stands. This amendment changes how the spectra are fetched and adds one stricter class.

## What happened

The fetch through IRSA's per-object spectrum service was started and stopped after 15 spectra: each lens object sits
in a different tile file and the service takes about 30 s per object, a day for the 3,184 targets. Those 15 files were
written to disk and never opened; they are not used.

Looking for a faster route, the first 300 kB of one tile file of the *field* test box (RA 140.50, Dec +71.05; no
ECLIPSE object) were read. Two things were learned from its headers:

1. The file server accepts byte-range requests, and each object's tables can be read directly (about 0.5 s).
2. Each object carries, besides its co-added spectrum, **its individual dither spectra**, each with the grism position
   in its header (`GWA_POS` = RGS000 or RGS180, `GWA_TILT` = 0 or 4). This confirms the two opposite dispersion
   directions that §0 of the criteria marked PROVISIONAL. The primary header also gives the mask bits (1 = do not use,
   64 = poor absolute flux), which is the good-pixel rule of §1.

## A0.1 Fetch route

Each target's tables are read by byte range from the tile file named in the association table
(`https://irsa.ipac.caltech.edu/ibe/data/<path>`, which redirects to IRSA's cloud file server): its META header, its
co-added spectrum and its dither spectra. One request stream. The object is located by its `OBJ_ID` in the META
headers, never by position in the file alone. UNCERTAINTY is taken as √VAR. Check added to K5: for the field objects
already fetched through the service, the co-added arrays read by range are identical to the service's.

## A0.2 The dither test and class SECURE-D

A real mirrored pair is one emitter seen on opposite sides in the two grism positions: its blue component must come
from one position and its red component from the other. A true line doublet ([O III], [S II], Hα with [N II]), a
co-addition artefact, and a symmetric feature appear the same in both.

For a pair found by the frozen rule, with its midpoint, half-split and width held: the residual spectra of the RGS000
dithers and of the RGS180 dithers (each dither prepared exactly as §3 prepares the co-add) are fitted jointly, per
position, for the two line fluxes (F_blue, F_red). With A_g = F_red − F_blue for position g:

- **D passes** if A_000 and A_180 have opposite signs and |A_000 − A_180| ≥ 3 × its error.
- A system without a usable dither in each position cannot be tested and is not SECURE-D.

**SECURE-D** = SECURE (frozen rule, same tier) and D passes. A lens whose images are equally bright on both sides of
the deflector along the dispersion fails D by construction; that loss is accepted.

## A0.3 Ladder and words

The frozen ladder is graded first and unchanged: TA, then TB, on class SECURE with gates H2, H2b, H4.
Only if both fail: **TA-D, then TB-D**, the same gates applied to class SECURE-D (grade-X null, sign-flipped null
with the dither residuals flipped as well, truth lens recovered in SECURE-D). If one passes, the readings of §5 are
made on SECURE-D and every word carries "under pre-data amendment A0". If none passes: NOT EVALUABLE, and it stays
that way. When the frozen ladder passes, SECURE-D is reported as a robustness row and D statistics are printed for
every hit, lens and null.

Instrument checks added (a failure makes the lane NOT EVALUABLE on the -D rungs only): **I3** mirrored pairs injected
into the dither spectra of 300 S systems (blue component in the RGS000 dithers, red in the RGS180 ones, combined
S/N 12) pass D in at least 60 %; **I4** the same flux injected as a true doublet (both components in every dither)
passes D in at most 5 %.

Four rungs instead of two is a multiplicity; each added rung is strictly tighter than the frozen one it follows.

κ = ½ FITTED. No outcome favours the framework.
