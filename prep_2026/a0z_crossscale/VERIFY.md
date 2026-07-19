# ADVERSARIAL VERIFY -- cross-scale a0(z) lane (galaxy_a0z.py + confront.py)

Both scripts re-run **exit 0** (2026-07-18) and reproduce the banked numbers
(Big Wheel a0_eff = 1.54(+1.10/-0.61)e-10; S_all = 0.80 sigma; z=0 tie 1.26/1.44 sigma
Planck-H0). Verdict of the lane -- **UNDERPOWERED-CONSISTENT-WITH-BOTH** -- SURVIVES.
It is honest, and where it errs it errs AGAINST the framework. Two forecast
caveats below are the only real corrections.

---

## (1) Is the galaxy a0(z) REAL, or M_bar systematics in disguise? -- NOT SEPARABLE (correctly stated)

The galaxy-side a0 is read **entirely** from the BTFR zero-point / V^4 = a0 G M_bar.
That map is `Delta log a0 = -Delta log M_bar` at fixed V (deep-MOND slope 4). So a
mis-estimate of M_bar propagates **1:1** into a0 -- they are algebraically
degenerate for this estimator. Rising molecular-gas fractions (~10% z=0 -> ~50%
z=2), alpha_CO, dust, and IMF evolution all move the BTFR zero-point and are
**indistinguishable** from an a0 shift with the BTFR/point-mass method. The
only a0-separable observable is the **RAR transition radius / full-RC shape**,
which this lane does NOT use. The scripts state this plainly ("NOT a clean a0",
"M_bar systematic EXCEEDS the signal"). **No overclaim** -- they do not pretend
the BTFR readout isolates a0. CONFIRMED by the Big-Wheel lever below.

## (2) Distance/cosmology circularity -- QUANTIFIED, genuinely MILD (not fatal)

M_bar ~ D^2, and D needs a cosmology. I computed D_L(z) for the flat-LCDM vs the
DESI-w0wa background and propagated to M_bar:

| z | D(DESI)/D(flat) | Delta log M_bar |
|---|---|---|
| 1.00 | 0.9827 | -0.015 dex |
| 2.30 | 0.9931 | -0.006 dex |
| 3.25 | 0.9955 | -0.004 dex |

The background-choice shifts M_bar by **<=0.015 dex** -- ~10x below the 0.155-dex
signal and ~15x below the 0.23-dex Big-Wheel error. A wrong background moves all
points together and cannot manufacture a decline. **The lane's "mild, not fatal-
circular" claim holds and is now numeric.** (Testing a0-tracks-rho_DE is not the
same as assuming the DE evolution.)

## (3) Manufactured agreement OR tension? -- NEITHER; conservative choices throughout

- The z=2.3 point is placed at 1.86 (**RISING**, the WRONG sign for the framework
  decline) and left in the fit. Q1 chi2 therefore mildly prefers FLAT/rising over
  the framework decline -- they did **not** hide the adverse lean.
- The z=1 point is the median of a hand-picked straddle {2.75, 0.068, 1, 1} = 1.0;
  arbitrary but carries 0.35-dex error and ~zero weight. Not load-bearing.
- The Big-Wheel central value uses the **M_dyn-capped stellar mass (1.7e11)**,
  which gives the HIGH a0 (ratio 1.27) -- the ANTI-framework choice. The full-SED
  stellar mass (3.7e11) would land the point at ratio **0.86, right on the DESI
  decline** -- yet they did NOT use it. No deck-stacking toward a "win."

## (4) Is the data constraining, or is confront overstating a weak signal? -- Not overstating

S_all = 0.80 sigma, S_clean = 0.73 sigma, Big-Wheel-alone = 0.73 sigma. The
headline is UNDERPOWERED and the "prefer flat" |Delta chi2| = 1.28-1.97 is
explicitly called not significant. The confront lane **understates rather than
overstates**. Correct posture.

## (5) Big Wheel is ONE galaxy -- weighted honestly, and it CANNOT resolve the decline

Independent lever check (V, gas fixed; vary the M_bar inputs the scripts flag):

| stellar mass | M_bar | a0 | ratio/SPARC |
|---|---|---|---|
| 0.9e11 (low) | 3.35e11 | 1.87e-10 | 1.58 |
| **1.7e11 (capped, chosen)** | 4.15e11 | 1.51e-10 | **1.27** |
| 3.7e11 (full SED) | 6.15e11 | 1.02e-10 | 0.86 |

The stellar mass alone swings the ratio across the **entire** flat(1.0)-to-
decline(0.70)-to-rise span. One object, fully M_bar-degenerate: it can exclude
the alt-cH0 ~5x rise (~2 sigma) but **cannot** distinguish the 0.70 decline from
flat. Weighted as exactly that (1 of 2 clean points, 0.23-dex error). Honest.

## (6) Both footings -- present and correct

Ratios cancel the footing; it re-enters only in the Big-Wheel absolute
(SPARC/canonical/alt = 1.31/1.65/1.37, all consistent with constant on their own
footing). The alt rho_total/cH0 footing (a0 RISING as E(z) -> ~5x by z~3) is
shown and is the ONLY thing the data disfavor (~2 sigma). Both banked forks run.

## (7) Is the ELT/JWST forecast honest? -- TWO CORRECTIONS (the only real ones)

**(7a) Asym-drift alpha=3.4 is FIXED, not in the MC.** Varying it: alpha=0 ->
a0 ratio 0.95; alpha=2 -> 1.13; alpha=3.4 -> 1.27. This unpropagated systematic
is ~0.1-0.15 dex and would WIDEN the Big-Wheel error beyond the quoted 0.23 dex.
(It also pushes a0 UP = anti-framework, so it does not rescue a "win"; it just
means the true error bar is even larger and the point even less constraining.)

**(7b) The forecast assumes PURELY INDEPENDENT per-object errors (~1/sqrt(N)).**
The dominant M_bar error (alpha_CO, IMF, dust prescription applied identically to
a sample) is largely **common-mode / correlated**, which does NOT beat down with N.
Required sigma_mean = 0.052 dex. With a common-mode floor:

| M_bar common-mode floor | N for 3 sigma |
|---|---|
| 0.00 dex | 24 |
| 0.05 dex | 362 |
| >=0.08 dex | **never reaches 3 sigma (any N)** |

Since realistic high-z M_bar calibration floors are ~0.08-0.15 dex (alpha_CO alone
is 0.1-0.2 dex systematic), the "N~20-40 makes it decisive" claim is **optimistic**:
it is decisive ONLY if the common-mode M_bar systematic can be driven below ~0.05
dex, which is the actual hard problem -- not the object count. Also, "clean
deep-MOND z~2-3 disks" are RARE (the intermediate-z KMOS3D rotators are g>~a0, as
the script itself notes); the Big Wheel is exceptional, so assembling 20-40 like it
is itself optimistic.

---

## VERDICT

**HONEST BOTH WAYS -- lane verdict UPHELD, with the forecast tempered.**

- Neither a manufactured agreement nor a manufactured tension. The lane picks
  the anti-framework option at every fork (M_dyn stellar cap, high asym-drift,
  keeps the adverse rising z=2.3 point) and STILL lands "consistent with both."
- The distance-circularity is mild (<=0.015 dex), now quantified -- **not** fatal.
- The galaxy a0(z) is **not separable** from M_bar evolution with the BTFR/point-
  mass estimator (they are 1:1 degenerate); the scripts say so and do not overclaim.
- Genuine result: **z=0 tie holds ~1 sigma (canonical footing, definitional
  anchor); the predicted 0.60-0.75 decline is neither detected nor excluded;
  S ~ 0.8 sigma -> UNDERPOWERED.**
- **Two corrections, both shrinking the future promise, not the present result:**
  (a) propagate asym-drift alpha in the Big-Wheel MC (error is wider than 0.23 dex);
  (b) the forecast must carry a COMMON-MODE M_bar floor -- with a >=0.08-dex floor
  the test never reaches 3 sigma at ANY N, so the decisive lever is M_bar
  CALIBRATION (alpha_CO/IMF to <~0.05 dex common-mode), not raw rotator count.
- No "proves"; a0 magnitude inherits the posited Z; only the ratio/tracking is tested.
