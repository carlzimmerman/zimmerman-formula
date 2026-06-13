# agentPP — ROUTE 1: QNM spectral moments — does the dS QNM ladder PEAK enough to bound the fold? (2026-06-13)

**The decisive question (banked setup).** agentOO (851e7649) proved the dS horizon bath FORCES the
bend sign sigma4 < 0, but the SMOOTH Gibbons-Hawking thermal continuum gives sigma6 < 0 (UNBOUNDED —
Cauchy-Schwarz ratio I2^2/(I1 I3) ~ 0.33-0.63 << 1) and a free-floating k*. A CONTROLLED bounded fold
needs sigma6 > 0, i.e. CS -> 1, which requires a SHARPLY PEAKED horizon response. agentS computed the
dS QNM ladder: purely DAMPED (Re omega = 0, |Im/Re| ~ 1e-15), damping rates Gamma_n = sinh((Delta+n)lambda),
a geometric/linear-semiclassical tower. **THE QUESTION: does this geometric ladder of damped modes push
CS above 1 (sigma6 > 0, bounded fold) — or, being purely damped / zero-centered, is it just another
broad/featureless response that stiffens (CS < 1, still unbounded)?**

**Coefficient quarantine ENFORCED.** STRUCTURE only: sign of sigma4, sign of sigma6 (CS vs 1), and
whether k* is edge-pinned. q=1/4 / zeta-tilde / (16pi/3)^{1/4} NOT asserted anywhere, downstream.

**Both-ways honesty, maximum hostility.** Framework-favorable = maximum stakes. The hostile prior
(purely-damped => zero-centered Lorentzians => BROAD, while a He-II roton needs a peak at FINITE k =>
default-expect the QNM response FAILS to peak) is the null I must try hardest to break, and report if it holds.

---

## The construction (what was computed)

The khronon's in-medium secular dispersion (OO Route 2, exact):
    omega^2 = c0^2 k^2 + k^2 * int dW rho(W)/(omega^2 - W^2)
IR-expanded (rho >= 0, gapped support W > 0, so all moments finite):
    1/(omega^2 - W^2) = -1/W^2 - omega^2/W^4 - omega^4/W^6 - ...
    => I1 = <W^-2>, I2 = <W^-4>, I3 = <W^-6>   (rho-weighted inverse moments)
    c_chi^2 = c0^2 - I1,   sigma4 = -I2 c_chi^2 (< 0, BEND),   sigma6 = c_chi^2 (I2^2 - I3 c_chi^2)
    => sigma6 > 0  IFF  I2^2 > I3 c_chi^2, governed by the Cauchy-Schwarz ratio CS = I2^2/(I1 I3) -> 1.

Cauchy-Schwarz on measure d-mu = rho dW with vectors W^-1, W^-3:
    (int rho W^-4)^2 <= (int rho W^-2)(int rho W^-6)  =>  I2^2 <= I1 I3,  CS <= 1.
**Equality (CS = 1) iff the measure is a single DELTA (W^-1 prop W^-3 mu-a.e.) — i.e. rho concentrates
at ONE frequency.** Any spread (broad response) gives CS < 1. This is the exact criterion OO named.

The dS QNM ladder spectral density: each rung deposits weight at the scale W ~ Gamma_n. Because
agentS proved Re omega = 0 (PURELY damped, overdamped, quality factor Q ~ 1/2), each rung is a
RELAXATIONAL / overdamped resonance whose "center" and "width" are the SAME scale Gamma_n — modeled as
a normalized bump at W_n = Gamma_n of fractional width qfac*Gamma_n, with qfac ~ O(1) (overdamped) the
physical case. Ladder = sum over rungs n, geometric weights decay^n.

## RESULT (computed) — the ladder STAYS BELOW the Cauchy-Schwarz ceiling

(A) PHYSICAL overdamped ladder (qfac = 1.0 down to 0.3), Delta in {0.5,1.0}, lam in {0.357,0.693} (q=0.7,0.5),
geometric weights decay in {0.5,0.3}, N=8 rungs:

    CS = I2^2/(I1 I3) ranges 0.38 - 0.63  ACROSS THE ENTIRE GRID — ALWAYS < 1.
    => sigma6 < 0 (UNBOUNDED) for every parameter choice. SAME class as OO's smooth GH continuum (0.33-0.63).

The hostile prior is CONFIRMED at the spectral-moment level: a GEOMETRIC LADDER of overdamped (zero-centered,
Re omega=0) dS QNMs does NOT push CS above 1. It sits in the SAME 0.4-0.6 band as the smooth Gibbons-Hawking
continuum — the laddered structure does not help.

## Why the ladder fails — the crux (dissected, both ways)

The Cauchy-Schwarz ceiling CS = 1 is reached IFF the spectral measure concentrates at a SINGLE
frequency (one delta). Verified analytically: single delta at any W => CS = 1 exactly; two deltas
=> CS = 0.938; the 8-rung dS ladder, **even with INFINITELY SHARP (delta) peaks**, => CS = 0.952 < 1.

- **It is NOT a peakedness problem.** A single sharp resonance DOES give CS -> 1 (Gaussian-bump check:
  single peak CS -> 0.9996 as width -> 0; the Lorentzian's apparent CS -> 0.017 was a fat-power-law-tail
  artifact, not the true delta limit — caught and corrected). The dS QNM modes could be arbitrarily sharp
  and it would not help.
- **It IS a MULTI-SCALE problem.** The dS QNM ladder deposits weight at GEOMETRICALLY SEPARATED scales
  Gamma_n = sinh((Delta+n)lambda). Inverse moments W^-2, W^-4, W^-6 all weight the lowest rung, but the
  higher rungs add just enough high-W weight to break the single-scale (delta) condition. A >= 2-scale
  tower CANNOT saturate Cauchy-Schwarz. Hostile stress test: 200,000 random >= 2-rung spectra — the only
  cases reaching CS = 1 are DEGENERATE (two coincident frequencies, e.g. 6.593, 6.593, fractional spread
  0.0000 = a disguised single scale). The geometric dS ladder (fractional spacing O(1)) is the OPPOSITE
  of that degenerate limit. MAX geometric-ladder CS over 240 cases = 0.9952 < 1.
- **The single-mode rescue is foreclosed by agentS's own data.** CS -> 1 needs the ladder to collapse onto
  rung-0 (weights decay -> 0). But agentS measured a GENUINE multi-rung tower: the matrix pencil returns
  multiple rungs (q=0.7,Delta=1.0: 0.3643, 0.7064; q=0.9,Delta=0.5: 0.0527, 0.1507), >= 19 e-folds of
  clean ladder, O(1) offset/spacing. The physical dS residues are NOT exponentially collapsed, so the
  CS-saturating single-mode limit is NOT what the dS horizon supplies.

## The damning coincidence with the banked GH continuum

The infinitely-sharp-peak dS QNM ladder lands at **CS ~ 0.92-0.96**, which is the SAME band as the
banked smooth Gibbons-Hawking continuum (commit 851e7649: GH ratios 0.94-0.97, hostile-verified,
0/20000 random positive spectra cross 1). The overdamped (physical, qfac~O(1)) ladder lands even lower,
CS ~ 0.4-0.6, the SAME band as OO's GH coth spot-check (0.33-0.63). **Structuring the horizon response
into a geometric QNM tower buys NOTHING on the boundedness axis** — peaked or smooth, multi-scale =>
CS < 1 => sigma6 < 0 => UNBOUNDED.

## Edge-pinning — k* is still cutoff-free

With sigma6 < 0, omega^2 = c_chi^2 k^2 + sigma4 k^4 + sigma6 k^6 has NO stabilized minimum and omega(k)
has NO inflection k* for k > 0 (verified: zero omega''(k) crossings). **There is nothing to pin.** The
ladder's only internal scale is Gamma_0 = sinh(Delta*lambda) (a frequency/energy scale setting the moment
scales I_m ~ Gamma_0^{-2m}); even if a stabilizer were added by hand, k* would track this QNM energy scale,
which is UNRELATED to the sonic-edge condition b -> c_chi (a separate tuning on c_chi^2 = c0^2 - I1). The
ladder spacing lambda does NOT pin k* to the b -> c_chi edge. k* stays edge-UNPINNED / cutoff-free-floating.

Clean sign reading (c_chi^2 = c0^2 - I1 > 0, rungs scaled to keep it positive): sigma4 = -2.31 (< 0, BEND
HELD), sigma6 = -4.38 (< 0, UNBOUNDED HELD), CS = 0.952. Both signs are robust at the sharp-peak limit.

---

## VERDICT — QNM RESPONSE IS BROAD (multi-scale); the fold STAYS UNBOUNDED. STILL-UNBOUNDED.

- **sigma4 < 0 (bend): HELD.** The ladder preserves the OO-forced bend sign. The roton operator stays
  non-free on the sign axis.
- **sigma6 > 0 (bounded fold): NOT delivered.** CS < 1 for EVERY dS QNM ladder, at every peak width, in
  the overdamped physical case (0.4-0.6) AND at the infinitely-sharp delta limit (0.92-0.96). The geometric
  multi-scale tower cannot saturate Cauchy-Schwarz; sigma6 < 0 (unbounded) survives. **HOSTILE PRIOR
  CONFIRMED.** The purely-damped (Re omega = 0), multi-scale QNM response is NOT the sharp single-resonance
  the He-II roton minimum needs — it is a structured-but-broad response that STIFFENS like the smooth bath.
- **k* edge-pinning: NOT delivered.** No inflection exists (sigma6 < 0); the ladder scale Gamma_0 is not
  the sonic edge b -> c_chi; k* stays cutoff-free.

The named unbanked input — "a peaked dS QNM horizon resonance lifts sigma6 > 0 and edge-pins k*" — is
**REFUTED on the boundedness and edge axes** by this Route-1 spectral-moment computation. The dS QNM ladder
does NOT supply the peak that bounds the fold. The single thing that WOULD (collapse to one resonance) is
foreclosed by agentS's measured genuine tower. Link 5's roton fold remains bend-forced but UNBOUNDED and
edge-unpinned; the controlled Airy fold still needs an input the dS QNM spectrum does not provide.

**Coefficient quarantine held**: q=1/4 / zeta-tilde / (16pi/3)^{1/4} never asserted; only the SIGNS of
sigma4, sigma6 and the edge-pinning structure were computed.

**Scripts:** /tmp/agentPP_route2.py (overdamped ladder CS scan), route3 (ladder-vs-single dissection),
route4 (delta-limit + Gaussian-tail correction), route5-7 (clean signs, hostile stress test, degeneracy
inspection, edge-pinning).
