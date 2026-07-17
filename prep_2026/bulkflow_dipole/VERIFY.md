# VERIFY.md — adversarial re-run of bulkflow_dipole (for a possible Sarkar exchange)

Re-ran both committed scripts (exit 0) and independently re-derived every load-bearing
number with a **different transfer function (Eisenstein-Hu no-wiggle)** and my own
sigma8 normalization + g_pec. Hunted a manufactured MOND-win and a manufactured null
equally. Framework: de Sitter-Unruh MODIFIED-INERTIA, a0=cH_L/Z=9.36e-11 (canon) /
1.13e-10 (alt), nu(y)=sqrt(1+1/y). Both footings run.

## Re-run status
- `bulkflow.py` exit 0, reproduces RESULT.md (V_MI overshoots Qin by median 10.0x, range 6.3-13.0x).
- `quasar_dipole.py` exit 0, reproduces RESULT.md (D_frame/D_excess = 0.071, ~14x too small).

## (1) Is V_LCDM honest or lowballed to flatter MI?  -> HONEST
Independent EH transfer (vs the code's BBKS), same sigma8=0.80/Om=0.30/f=0.516:

| R [h/Mpc] | code BBKS | my EH | Qin pink (approx) |
|---|---|---|---|
| 30 | 241 | 250 | ~300 |
| 50 | 199 | 209 | — |
| 100 | 139 | 149 | — |
| 300 | 64 | 67 | — |

My independent V_LCDM is ~4% **higher**, not lower — the committed curve is marginally
**conservative**, ~83% of Qin's pink at R=30, inside the stated 20-30%. Benchmark: 3D rms
bulk flow @R=50 = 209 km/s (1D = 121 km/s), a standard LCDM value for sigma8=0.80. **Not
lowballed.** Direction of any residual bias would only mildly inflate the "needed nu"
narrative, and the headline verdict is an overshoot/needs-theory, not a win — so no
manufactured win is created here either way.

## (2) Is g_pec at the right amplitude or inflated to push nu?  -> RIGHT AMPLITUDE, not inflated
Re-derived g_pec myself from the same P(k) via the standard linear relation
v = (2f/3 H0 Om) g  =>  g = (3 H0 Om / 2f) sigma_v (g and v share the delta(k)/k weight,
so g_rms/sigma_v is a scale-independent constant = 1.98e-18 /s, which I verified numerically).

- My g_pec @R=30 = 4.96e-13 vs code 4.77e-13 (~4%). Falls to ~1.3e-13 @R=300.
- g/a0 ~ 0.005-0.0014 on 30-300 Mpc => **deep-MOND**, the coherent large-scale peculiar
  acceleration is genuinely ~a0/200.
- **Inflating g would LOWER nu** (less boost), so there is zero incentive to inflate, and
  none is present. The tiny coherent g is a physical fact, and it is what drives nu -> ~14-27.

## (3) SCALE-DEPENDENCE — the decisive test.  Neither reading matches amplitude AND shape.
Sarkar/Qin's anomaly is that the flow stays HIGH at large R (non-convergence) = a **SHAPE**
anomaly (flatter-than-LCDM), not just a normalization offset. Fall factor V(R=30)/V(R=200):

| curve | fall factor (smaller = flatter = more non-convergent) |
|---|---|
| LCDM | 2.69 |
| **MI coherent-field** (nu rises as g falls at large R) | **1.64** |
| **MI environmental-a0** (const nu ~1.2-1.7) | **2.69 (identical to LCDM)** |
| data (~260-380 @30 -> ~190-260 @150-180) | ~1.3-1.5 |

Decisive, and this is UNDER-STATED in RESULT.md:
- The **coherent-field** reading DOES flatten the curve (2.69 -> 1.64) — the RIGHT
  DIRECTION and roughly the right degree — because nu rises as the coherent field weakens
  at large R. So MI naturally predicts *reduced convergence*. **But** its amplitude
  overshoots ~10x.
- The **environmental-a0** reading (the one that roughly matches AMPLITUDE, nu~1.2-1.7) is a
  near-**constant** multiplier, so it reproduces the LCDM SHAPE exactly and does **NOT**
  explain the non-convergence at all — it just rescales a curve that still converges.
- => **No single MI prescription gets amplitude AND shape.** The reading that gets the
  shape (coherent) blows the amplitude 10x; the reading that gets the amplitude
  (environmental) has the wrong (LCDM) shape.

Physics note (mild over-generosity flag in RESULT.md): for BULK-FLOW / center-of-mass
streaming, the acceleration that drives the response IS the coherent large-scale field
(~a0/200); a galaxy's internal virial acceleration is internal and does NOT push the COM.
So the **coherent-field reading is the physically-motivated one for bulk flows, and it
OVERSHOOTS ~10x**. RESULT.md's "environmental" rescue ("total acceleration dominated by the
virial environment") is a modified-gravity-flavored argument that is shaky for COM
streaming. Read straight, the literal MI result is a 10x overshoot; the environmental
reading is a generous framing, not a fix. If anything the corpus is slightly TOO KIND to
the framework here — this is not a manufactured null.

Robustness: overshoot is insensitive to sigma8 — raising sigma8 raises g, lowers nu, but
even g/a0~0.01 leaves nu~10 (~6x overshoot). Both footings agree to ~10% (alt a0 larger ->
larger nu -> overshoot marginally WORSE, nu 15-30 vs 14-27).

## (4) Quasi-linear caveat prominent?  -> YES
Docstring + RESULT.md both state clearly this is a nu-boost BRACKET, not a first-principles
P(k)-of-MI; the MI linear cosmology (MI transfer function, MI growth f, self-consistent
field-level nu-weighting) is UNBUILT/open. Correct and prominent. The "multiply V_LCDM by
nu" step also risks double-counting vs a real MI growth calculation (Nusser 2002 shows MOND
feeds growth), reinforcing that only the built linear theory can pin the number.

## (5) Credit present?  -> YES
Nusser 2002 (astro-ph/0109016) + MOND bulk-flow/structure literature (Llinares, Angus, Katz)
cited in RESULT.md CREDIT. The MOND-enhances-flows/growth idea is correctly flagged as NOT
novel; framework-specific content = whether its a0+nu gives the right MAGNITUDE (it does not
under the literal estimator).

## (6) Dipole arithmetic (LANE B)  -> CORRECT
beta_cmb = 369.82/299792.458 = 1.234e-3.
D_EB = [2 + x(1+alpha)]beta = 5.4 x 1.234e-3 = 6.66e-3 (x=1.7, alpha=1.0).
D_obs = 1.54e-2 => excess = 8.74e-3.
D_frame = (1/2)beta_cmb = 6.17e-4 (a0-INDEPENDENT -> identical both footings, verified).
D_frame/D_excess = 0.071 => ~14x too small. All arithmetic reproduced. Robust to x,alpha
choices; conclusion (negligible amplitude, shared DIRECTION only) does not move.

## VERDICTS (both footings, no "proves")
- **LANE A: NEEDS-LINEAR-THEORY, with a confirmed MI-WRONG-SCALE / 10x-OVERSHOOT flag.**
  The literal, physically-motivated coherent-field MI boost overshoots the Qin bulk-flow
  data by median ~10x (6-13x). It does predict reduced convergence (right qualitative
  direction + roughly right SHAPE), but at 10x the wrong amplitude. The amplitude-matching
  "environmental" reading does NOT reproduce the non-convergence shape. No prescription
  matches both. Both footings agree ~10% (alt slightly worse). The first-principles number
  is unavailable until the framework's linear cosmology is built. **Not a MOND-win, and the
  environmental framing is if anything too generous — not a manufactured null.**
- **LANE B: NEGLIGIBLE.** Apex dipole 6.2e-4 is ~14x below the ~8.7e-3 quasar excess,
  a0-independent, identical both footings. Shared apex DIRECTION is the only
  framework-relevant datum; the Secrest amplitude excess is not a framework prediction.

## HONEST ONE-LINER for Carl (if he raises it with Sarkar)
"Modified inertia does predict qualitatively enhanced, less-convergent large-scale flows —
the direction of your anomaly — because nu rises as the coherent peculiar field drops below
a0 at large R; but the naive quasi-linear boost overshoots the Qin data by ~10x, the one
reading that matches the amplitude doesn't reproduce the non-convergence SHAPE, and the
framework's actual linear cosmology is unbuilt, so I can't yet turn this into a number. The
quasar dipole is a separate story: we share your apex direction, but our apex signature is
~14x too small to touch the amplitude excess."
