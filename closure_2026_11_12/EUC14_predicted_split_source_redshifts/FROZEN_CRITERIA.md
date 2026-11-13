# EUC14 (PREDICTED-SPLIT SOURCE REDSHIFTS): FROZEN CRITERIA

2026-11-12. Committed alone, before any prediction has been compared with the spectrum of any ECLIPSE lens or grade-X
object and before the truth lens's image has been opened. TEST lane; adopts nothing. κ = ½ FITTED; not theory closed.
Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. The gate it feeds (EUC1-F) is
one-sided; no outcome of this lane may be described as the data favouring the framework.

The brief named this lane EUC12; EUC12 and EUC13 were taken by other lanes first, so it is EUC14.

## 0. What this lane is

EUC9 (`../EUC9_grism_spectra_source_redshifts/RESULT.md`) found that in Euclid's individual dither spectra an emitter
off the extraction centre appears at λ + s in one grism position and λ − s in the other, recovered the truth lens's
source redshift that way, and failed its grade-X purity null because a slightly off-centre emitter in a non-lens looks
the same in a 1D spectrum. Its §5 item 4 names the repair: **predict each lens's shift before looking**, from the arc's
position on the sky and each dither's dispersion direction. A non-lens has no arc to predict from.

This lane builds the two inputs and grades EUC1-F with them. EUC1-F is not redesigned.

## 1. The two inputs (built before freezing)

**Dispersion direction per dither.** No public Euclid table states it. ESA's Euclid archive (TAP, `dr1.raw_frame`)
gives, for every NISP pointing id, a position angle `pa`, equal to 0.01° to the position angle of one edge of the
frame's footprint polygon in 500 of 500 frames checked: it orients the focal plane on the sky, but nothing public
says which focal-plane direction it names or how the grism disperses relative to it (the dither headers carry no angle:
DITH_ID, PTGID, DET_ID, GWA_POS, GWA_TILT). The pointing ids are the `PTGID` of EUC9's dither cache; 10,286 of its
10,289 pointings have a frame, and the grism position agrees in every one of 19,030 dithers checked. The
dispersion direction (towards longer wavelength) is then

    φ = pa + C0 + (180° for RGS180) + ST · tilt,   carried from the pointing centre to the object (tangent plane),

with C0 ∈ {0°, 90°, 180°, 270°} and tilt sign ST ∈ {+1, −1, 0} fixed on field calibrators (§1b). An emitter at sky
offset **D** (east, north) from the extraction centre appears at λ0 + DISP · k · (**D** · **u**), **u** the unit
vector of φ, DISP = 13.4 Å per 0.3″ pixel = 44.67 Å″⁻¹ (EUC9's value), k = 1 the prediction.

**Arc positions.** The catalogued MER objects, other than the lens object, inside the system's aperture
r_a = min(θ_E + 0.7″, 3.0″) of the catalogue position (EUC3's counted objects), with their offset from the lens object.
A system with none gets no prediction and is not evaluable. **The truth lens L015763 has no such object** (the lens
object is the only MER object within 3″); its arc is measured from its Euclid VIS image by the procedure of §4 H4.

### 1b. Field calibration (done before freezing; recomputed by the lane as check C1)

**Calibrators** (`euc14_fetch.py`, `euc14_cal.py`): field pairs (A, B) 0.8″ to 2.5″ apart, both in ESA's wide-survey
spectra table, **neither within 30″ of any ECLIPSE system of any grade, grade X included**; B's own rank-0 strongest
line (catalogue quality 212 or 252, FWHM ≤ 60 Å) gives λ_B; A has at least four dithers. Twenty boxes of 0.25° on
random NISP pointings (seed 20261112). Where B falls inside A's extraction, B's line must appear in A's dithers at
λ_B + DISP · k · (**D** · **u**_i), k = 1, **D** = B − A. First list: B's line S/N ≥ 8, flux ≥ 3e-16, by S/N; 129
chosen, **72 fetched**, then stopped because the first 62 showed the line only where B lies almost exactly along the
dispersion (A's extraction is narrow across it). Second list: pairs within 0.35″ of **either** focal-plane axis (pa or
pa + 90°, so all four C0 stay on an equal footing), S/N ≥ 6, flux ≥ 2e-16: **75, all fetched**. 147 have a usable
dither in each grism position.

For each convention the line is fitted in A's dithers with the midpoint within 30 Å of λ_B and k free in [−2, 2]:

| C0 | 0° | 90° | 180° | **270°** |
|---|---|---|---|---|
| calibrators with B's line at k = 1, S/N ≥ 6 (tilt sign +1 / 0 / −1) | 1 / 1 / 1 | 3 / 2 / 2 | 2 / 2 / 2 | **13 / 13 / 13** |

**Scale:** the 9 calibrators detected anywhere in k at S/N ≥ 8 with h ≥ 0.5″ give median k̂ = 1.000, robust
σ 0.148, none on the wrong side (k̂ < 0), 8 of 9 within 0.3 of 1; midpoint − λ_B = −1.2 Å (σ 5.8 Å). The pass rule
(≥ 5 detections, at least twice any other C0, median k̂ within 0.15 of 1 on ≥ 5) was written before any calibrator
was fetched and **passes**. **The tilt sign is not determined** (summed χ² 2121 / 2110 / 2097): +1 is taken by the
rule; it moves tilted dithers' directions by 4°.

**Frozen:** C0 = 270°, ST = +1, DISP = 44.67 Å″⁻¹, **k window |k − 1| ≤ w = 0.30** (2 × 0.148, kept within
[0.25, 0.5]).

## 2. Systems (frozen)

- **Lens side:** EUC1's sample S (6,173; contains P, 3,192). **Null:** the 2,580 grade-X systems, each given an
  Einstein radius from S as in EUC3 §2. **Truth:** EUCL-DR1-L015763 (not in S; gate H4 only).
- **Spectrum:** the lens object's dither spectra from EUC9's cache (EUC9 §2's targets: lens object within 0.6″,
  redshift interval, quality prerequisites). A dither is usable if EUC9's preparation accepts it and its pointing has
  a position angle; a usable spectrum has a usable dither in each grism position.
- **Usable arc:** predicted half-split h = median over usable dithers of DISP · |**D** · **u**| ≥ 30 Å (EUC9's
  smallest half-split), and the median projections of the RGS000 and RGS180 dithers have opposite signs.
- **Evaluable system:** usable spectrum and at least one usable arc.

## 3. The rule (frozen)

**Fit.** Each dither prepared exactly as EUC9's core prepares a spectrum. For one arc, every midpoint λ0 on EUC9's
6.7 Å grid, σ ∈ {12, 16, 20, 25} Å and k from −2 to +2 in steps of 0.05: one line flux fitted jointly over the usable
dithers, each with its own predicted centre λ0 + DISP · k · (**D** · **u**_i); a dither enters at that trial only if
80 % of the template lies on its good pixels. Per grism position, the flux fitted from that position's dithers alone
gives its own S/N.

**Candidate** at (λ0, σ, k): (a) |k − 1| ≤ w (§1b); (b) flux > 0, combined S/N ≥ c, S/N from the RGS000 dithers alone
≥ e and from the RGS180 dithers alone ≥ e; (c) **dominance**: its χ² gain is the largest over all k in [−2, 2], all four
widths and all midpoints within 2h + 27 Å, so the opposite side, the centre and other sizes fit worse; (d) its χ² gain
exceeds that of the best **centred** line (the same wavelength in every dither; σ from 12 to 130 Å, EUC9's eleven
values; centre within 2h + 27 Å) by Δ. **Tiers:** TA (primary) e = 3.5, c = 6, Δ = 9; TB (frozen fallback) 5, 8, 16.
An arc's line is its candidate of largest gain.

**Which line** (partners fitted jointly with the main line, at the same per-dither shifts, k and σ): [O III] 4960 at
λ0 · 4960.295/5008.24 with S/N ≥ 3 and flux 0.15 to 0.6 of the main line → class **O3**, z = λ0/5008.24 − 1, kept if
1.41 < z < 2.78. Otherwise Hα, z = λ0/6564.61 − 1, kept if 0.84 < z < 1.88: class **HA2** if [S II] 6725.5, [O III]
5008 or Hβ has a partner at S/N ≥ 3, else **HA1** (one line).

**Guards** (EUC3's and EUC9's): G1 z ≥ z_up + 0.15; G2 λ0 not within 66 Å of the deflector's own [S III] 9533.2,
He I 10833.3 to Pa γ 10941.1 or Pa β 12821.6 over [z_lo, z_up]. Failing only G2: **AMBIGUOUS-OWN**, never secure.

**System.** **SECURE** if at least one arc passes everything; z_s from the arc of largest gain; if another passing arc
gives a z_s more than 0.02 away: **CONFLICT** (excluded, counted).

## 4. Gates (frozen; at a tier, any failure makes that tier fail; TA first, then TB; both failing: NOT EVALUABLE)

- **H4 truth.** L015763 must be SECURE with |z_s − 1.3657| ≤ 0.004; being SECURE requires k within the window, so the
  predicted sign and size. Its arc: the VIS cutout (12″, from IRSA; only its header read before this commit, not its pixels)
  is read with its WCS; the lens light is modelled as the median in circular annuli of 0.1″ about the lens object; the
  residual is smoothed with a Gaussian of 1.5 pixels; the arc is the residual-weighted centroid of positive pixels
  within 0.3″ of the brightest smoothed residual between 0.5 θ_E and 1.5 θ_E. One arc, no other.
- **H2 purity null.** The identical search on grade X with their own catalogued neighbours: pass if
  n_X ≤ max(1, 0.20 · n_S · E_X / E_S) (EUC3's rule; E = evaluable, n = SECURE).
- **H3 scrambled prediction (signal-free in the arc's direction).** The same S systems with every arc offset rotated by
  +90° on the sky: pass if n_rot ≤ max(1, 0.20 · n_S). (A ring or a quad image at 90° can put real flux there, so this
  null can fail wrongly but cannot pass wrongly.) The mirrored offset (−**D**) is reported only: counter-images live
  there.
- **H2b sign-flipped.** The true prediction on every dither's negated residual: pass if n_flip ≤ max(1, 0.20 · n_S).
- **Coverage:** at least 30 % of S and of X have a usable spectrum. The fraction with an arc is reported.

## 5. Reading (frozen)

EUC1's `b` (law S and B, both footings) at z_s for every SECURE lens, inputs exactly as EUC1's primary run, with
`euc1.py`'s functions; the same lenses' source-free `b` beside it; lenses with z_l ≥ z_s − 0.2 dropped and counted.

- **EUC1-F exactly as frozen in EUC1 RESULT §8**, on P, if N(P) ≥ 10: median b, law S, per footing, 95 % bootstrap
  interval (`euc1.stats`). **LENS GATE HOLDS** if the upper bound ≤ 0.15; **LENS GATE FAILS** if the lower bound
  ≥ 0.25; otherwise **NO VERDICT**. If N(P) < 10: **EARLY READING, NOT A GATE**. Sample S is printed beside it and
  never gives the word. EUC5-F is not graded here.
- **Single lines.** Every HA1 lens is also read as [S III] 9533 (only where that puts the source at least 0.15 above
  z_up; otherwise it stays Hα), as [O III] 5008 and as [O II] 3727. The first lies below Hα in redshift and the others
  above, so the rule is symmetric: it can block a HOLDS as well as a FAILS. **If any of these readings changes the
  EUC1-F word on a footing, that footing's word is NO VERDICT (IDENTIFICATION-DEPENDENT)**, never a pass or a fail,
  and the RESULT says so in its first paragraph.
- Robustness (reported; cannot change a word): two-line classes only; TB only; AMBIGUOUS-OWN added; DESI deflector
  redshift where one exists.

**Selection, stated.** Only lenses whose arc MER catalogued as an object of its own, lying at least 0.67″ along the
dispersion and inside the lens object's extraction across it, with a line bright enough in both grism positions, can enter. That favours wide, bright, deblended arcs.
The reading describes those lenses, not the median of P.

## 6. Instrument checks and twins (frozen; a failed check makes the lane NOT EVALUABLE)

- **K1** EUC1 reproduced (N(P) = 3,192; source-free median b −0.019 / −0.044 to 0.001). **K2** EUC2's anchor
  (+0.231 / +0.215 to 0.002). **K5** EUC9's dither cache complete, its re-read check identical. **K6** a position
  angle for ≥ 95 % of the dithers of usable-spectrum systems. **C1** the field calibration recomputed gives the frozen
  convention and window and passes.
- **Injections** into the dithers of up to 300 evaluable S systems (seed 20261112; one random midpoint each, first
  usable arc): **I1** a line at the predicted shifts (k = 1, combined S/N 12, σ 16 Å) returned at TA within 13.4 Å in
  ≥ 70 %; **I2** a centred line (S/N 12, σ 20 Å) returned in ≤ 5 %; **I3** a line at the mirrored shifts (k = −1)
  returned in ≤ 5 % (I2 and I3 not counted where the uninjected spectrum already gives a candidate there).
- **MUTATE twins**, separate output names, each must exit 1: `EUC14_MUTATE=newton` (a₀ → 10⁻³⁰: b must rise on both
  footings on the reading sample where one exists and on the K2 anchor); `EUC14_MUTATE=anyk` (the k window replaced
  by any |k| ≥ 0.3: the number of SECURE grade-X systems at TA must rise).

## 7. Seen before freezing (disclosed)

- **EUC9 in full:** criteria, A0, A1 and its addendum, RESULT, code and hand-over note, so every count (A1-TA: S 28,
  X 6 against a limit of 2.3, sign-flipped 4), its void reading (P +0.264 / +0.252; single lines as [O III]
  +0.136 / +0.119; 22 of 28 one line), and the truth lens's dither result (peaks 15,464 / 15,598 Å, half-split
  1.50″, blue peak stronger in RGS000, D = −6.4). **The truth gate is therefore not independent evidence**: once the
  convention is fixed, EUC9's result says which side of the lens the brighter image lies. Its image has not been
  opened, so that side has not been checked. EUC9's per-system candidate file and figures were not opened.
- EUC3's criteria, EUC1 §8, EUC2's and EUC10's lines on L015763.
- **Lens-side catalogue geometry only:** systems with at least one catalogued arc candidate among EUC9's targets
  (P 169, S 321, X 156); the truth lens has none (its lens object is deblended, parent segment 3692). EUC9's dither
  cache was read by this lane for pointing ids, grism positions and tilts only; no flux array of any lens or grade-X
  object has been read, and no prediction compared with one.
- Every calibration number in §1b and `euc14_cal.out`, including a preview on the first 62 calibrators (C0 = 270° 3
  detections, 90° and 180° 1 each, 0° none; two at k̂ 1.10 and 1.15) that led to the aligned second list, and one bug
  fixed after it (the runner-up had been the same C0 with another tilt sign).
- Code tests on EUC9's 31 field spectra with injected lines (recovered at k 0.8 to 1.1; nothing at the mirrored
  prediction) and on a synthetic image (arc found at (0.86, −1.17)″ against (0.9, −1.2)″).
- **Access.** ESA archive TAP: position angles (26,092 frames) and calibrator selection. IRSA IBE byte ranges only:
  147 calibrator spectra and the truth lens's 120 × 120 VIS pixels (plus two single test requests), about 128 MB in all, one stream at one request a
  second (one 503, waited 150 s). **This stream ran alongside another lane's (EUC11's) IRSA TAP download**, with the
  agreement of the session that launched this lane; no TAP query was made at IRSA. Hash manifest outside git.
  IBE's cloud host refused cutout parameters, so the truth image is read row by row from the uncompressed mosaic
  (the procedure of §4 is unchanged: 12″ at 0.1″ per pixel).

## 8. Not claimed

- No measurement of a₀ or κ. Nothing about lenses whose arcs are not catalogued or whose sources show no line.
- A HOLDS is not a confirmation of the law; a recovered truth lens validates the geometry, not the purity.
