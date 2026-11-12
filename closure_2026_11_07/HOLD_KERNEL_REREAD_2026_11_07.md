# HOLD, 2026-11-07 ~16:00: the CMB-lensing Limber kernel, and what rests on it

Status: v1.1 deposit ON HOLD until GL2 (independent rebuild) reports and GL1/GL3 re-read the affected labels.
v1.0 (DOI 10.5281/zenodo.24040313) stands as deposited; v1.1 carries an erratum line if the finding holds.
No label is rewritten here. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

## The finding (CK4 ea06286d99, post-freeze; confirmed from the code by the Field equations session)
`limber_ratio` (QX3 iter2) weights with w = ((chi* - chi)/(chi chi*))^2 (1+z)^2 / H and then multiplies by
P_delta / chi^2. The Limber kappa kernel is W_kappa^2 / chi^2 proportional to (1+z)^2 (chi* - chi)^2 / chi*^2, so the
code carries an extra chi^-4, the missing k^-4 = (chi/L)^4, and over-weights z < 0.1. L-only factors cancel in the
ratio S(L); this one does not. CK4's measurement: the Limber/CLASS C_L^phiphi shape over L 20-400 runs 0.045-33
with the error, 0.98-1.006 with k^-4 restored.

## What imports it (origin, per the Field equations session's grep)
KD1, SE1, QX3 iter2/iter3, QX7 iter3, QX10 iter1, QX27, QX28, QX29, QX31, SV5 (t0_iter3 and sv5_web = the W1
web-lensing line r <= 1.072), OQ1, OQ2, LD1 (import; use unchecked), CE2, CK4, EW2, FA2, FA3, NA1, NA2, RS3.
HC1's CMB-lensing chi^2 does not appear to use it. WG1-WG6 used a separate pipeline (to be stated by GL1).

## Labels that rest on it, pending re-read (not moved)
- Wall 1's CMB side: KD1 G9a mu_K >= 8.9e6 (the 1e5 gap against galaxies' <= 0.1-79); SE1 arm (a).
- Every "web row": WL1's 0.0354 line (SV5), NA1 r 72-86, FA3 r 75-79, EW2's mu >= 10 window, OQ2's F_web,max.
- CE2's CMB-lensing chi^2 8.70-11.69 and its M3 bite; CK4's GL gate.
- QX3 iter1-3 shape verdicts; QX7 iter_3/iter_4 G2' Jeans lines; QX10 iter1; QX27-QX29, QX31 web/lensing rows.

## Lanes
GL2 (EV1 session): independent rebuild of C_L^phiphi vs CLASS, own code. GATE: no label moves before GL2 reads
     CONFIRMED.
GL1 (KD1 session): sector side re-read with the corrected kernel: KD1 G9a, SE1 arm (a), QX3 iter1-3, QX7 iter_3/4,
     QX10 iter1, CE2, CK4. Old vs new per label; MOVES reported, not rewritten.
GL3 (Field equations session): web-line side re-read: SV5 t0_iter3 and sv5_web (the r <= 1.072 line), then WL1,
     NA1, FA3, EW2, OQ1/OQ2, QX27-QX29, QX31, LD1's D1 use. Old vs new per label; MOVES reported, not rewritten.
Both re-reads: both footings; KA = with the error re-inserted, reproduce the old numbers to 0; MUTATE = a wrong power
(k^-2) gives a different shape. Frozen criteria first. Push via temporary index. One message each to "Theory
completion".

## Consequence if CONFIRMED
The deduction's walls and the web-off door were partly graded with an over-weighted low-z lensing kernel. Which
labels move is for GL1/GL3; the owner decides what is rewritten; v1.1 carries the erratum and the re-stated labels.

## Update ~16:30: GL2 CONFIRMED (d0c3692fc6)
Independent rebuild (own code, Poisson + Weyl potential, vs CLASS): with k^-4 the shape ratio is within 0.0007 of 1
over L 20-400; without it, 0.045-33.9, matching CK4 to 1-3 %. The code reading agrees: net weight chi^-4, correct
power chi^0. The error is REAL. GL1 and GL3 may now report which labels move; nothing is rewritten until the owner
decides; v1.1 carries the erratum.
