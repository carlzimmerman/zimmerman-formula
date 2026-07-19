# SYNTHESIS -- a0(z) from Type Ia Supernovae (de Sitter-Unruh MODIFIED-INERTIA framework)

Carl Zimmerman | 2026-07-18 | outputs in `prep_2026/a0z_from_sne/` (frozen repo untouched)

The idea: LCDM *assumes* the dark-energy leftover is a constant Lambda and fits it. This
framework instead reads the leftover density off the Pantheon+SH0ES supernovae point-by-point
and converts it to the galaxy acceleration scale a0(z) -- a number galaxies can independently
check. No Lambda, no w(z) assumed; rho_DE(z) is *measured*, not modeled.

    H(z) --(GP, nonparametric)--> rho_DE(z) = 3[H^2 - Om H0^2(1+z)^3]/(8 pi G)
      -> a0(z) = (c/2) sqrt(G rho_DE(z)) = (c/Z) sqrt(H^2 - Om H0^2(1+z)^3),  Z = sqrt(32pi/3) = 5.789

Inputs (stated, not circular): Om (matter is not dark energy -- no circularity), the GR/Friedmann
background (the framework keeps GR for the background), and the POSITED Z (the a0 magnitude
inherits it). Both H0 = 67.4 and 73.0 carried throughout; a0(z) SHAPE is H0-robust, absolute
a0(0) carries H0. Canonical rho_DE / cH_Lambda footing by construction; alt rho_total/cH0 footing
noted separately (it RISES with z as E(z), opposite sign of the rho_DE reading).

Credits: Milgrom (a0 kernel; nu = sqrt(1+1/y) is his 1999 form -- the framework's distinctive
content is the cH_Lambda/Z coefficient); Brout+2022 / Scolnic+2022 (Pantheon+SH0ES);
Seikel-Clarkson-Smith 2012 (GP model-independent H(z)).

---

## 1. HEADLINE

**a0(0) is a clean, model-independent SNe deliverable and it agrees with the independently
SPARC-measured galaxy a0 at ~1 sigma -- a genuine cross-scale (cosmic <-> galactic) consistency
through one number. The a0(z) DECLINE, however, is NOT measurable from SNe alone: differentiating
the luminosity distance to extract the small dark-energy residual is noise-limited past z~0.4, so
a0(z) is consistent-with-flat AND consistent with the framework's 0.60-0.75 -- weakly constraining,
not a discriminator. No decline manufactured; no win manufactured.**

---

## 2. OUTCOME (honest both ways)

### a0(0) -- the robust output
z->0 limit is E(0)=1 exact, so a0(0) = (c/Z) H0 sqrt(1-Om) carries essentially no SNe-reconstruction
noise (the GP H(z0=0.01) recovers 73.5 km/s/Mpc, self-consistent with the M_B=-19.253 calibration):

| H0 (km/s/Mpc) | a0(0), Om=0.315 | Om range 0.29-0.35 | tension vs SPARC 1.181e-10 +/-16% |
|---|---|---|---|
| 67.4 | 9.36e-11 (= canonical 9.355e-11 by construction) | 9.12 - 9.53e-11 | +1.29 sigma (low) |
| 73.0 | 1.014e-10 | 9.88e-11 - 1.032e-10 | +0.88 sigma (low) |

Both footings sit inside the SPARC z=0 band at ~1 sigma (better at local H0=73). This is a genuine
cross-scale consistency between the cosmic-Lambda leftover and the galaxy-measured scale, on the
framework's own rho_DE footing. **Honest caveat:** a0(0) is INPUT-DRIVEN -- it is the framework's
known Lambda -> a0 identity re-confirmed (SNe data does not enter the z->0 value; Om spread only
+/-2.3%), not a new SNe *measurement* of a0. It should not be oversold as such.

### a0(z) -- is the slope distinguishable from zero? NO, not robustly.
- Model-independent GP reconstruction of rho_DE(z)/rho_DE(0): the SIGN of rho_DE is pinned
  (f_phys >= 0.9) only out to **z ~ 0.40**; it goes sign-indefinite by z~0.5-0.7, and z=3 is pure
  extrapolation beyond the data (zmax = 2.26). No SNe a0(z=3) measurement is possible.
- Om-marginalized a0(z)/a0(0): z=0.5 = 1.077 [1.03, 1.12]; z=1 = 1.172 [0.92, 1.39] (consistent
  with 1); z=2 = 1.342 [0.75, 2.26] (consistent). The one sub-z=0.5 >1sigma excursion is a RISE
  that is a pure Om artifact (fixed-Om a0(0.5)/a0(0) slides 1.119 at Om=0.29 -> 1.028 at Om=0.35).
- Adversarial 4-kernel/bandwidth test: every kernel gives a0(z) flat-to-RISING, NEVER a decline;
  shape past z~0.5 is noise-dominated (center slides 1.08 -> 2.34 across kernels).
- Differentiation-free offset-marginalized chi2 (flat-LCDM vs DESI-CPL) at Om=0.315:
  Delta-chi2 = -3.10 (~1.8 sigma mild, non-decisive preference for the decline). **This hint is
  Om-FRAGILE and its sign REVERSES:** -7.17 (Om=0.29) -> -3.10 (0.315) -> **+1.78 favoring FLAT**
  (Om=0.35). Verifier correction applied: crossscale.py now prints all three so -3.10 is not read
  as a standalone decline hint.

The framework's 0.60-0.75 decline benchmark is NOT supported by SNe (data leans flat-to-mild-rise
at low z, Om-degenerate; only ~1% of z=3 draws land in [0.60,0.75]). Constant Lambda (ratio = 1,
a0 flat) is consistent across the whole probed range. **The one quantitative hook:** a DESI-like
evolving DE gives a0(z=3)/a0(0) = 0.696, squarely inside the predicted 0.60-0.75 band -- so IF
DESI's w0wa decline is real it is exactly the a0(z) drop the framework wants -- but SNe cannot
establish that decline on their own.

---

## 3. PAPER VERDICT -- worth a paper? YES, but framed as a MEASUREMENT + a NEGATIVE RESULT, and
best as a section/companion to the a0-line paper rather than a standalone claim.

**Genuinely novel:**
1. The first a0(z) extracted DIRECTLY from Type Ia supernovae -- reading the DE leftover off the
   Hubble diagram point-by-point and converting to the galaxy acceleration scale, with no Lambda
   and no w(z) assumed.
2. The cross-scale tie: one number (a0) links the cosmic-Lambda leftover (SNe) to the independently
   SPARC-measured galactic scale, and they agree at ~1 sigma. That galaxy <-> cosmology bridge
   through a single acceleration scale is the distinctive, publishable content.

**The real strength is the a0(0) measurement + cross-scale consistency, NOT an a0(z)-decline
detection** (which SNe cannot deliver alone). Selling this as "SNe show a0 declines" would be
manufacturing a detection -- the data do not support it and every robustness axis (kernel, Om,
reliability horizon) confirms SNe are non-constraining on the slope. The honest paper leads with
the consistency and reports the slope as an explicit, quantified null / target-for-DESI.

**Honest title options:**
- "The galaxy acceleration scale from Type Ia supernovae: a cross-scale consistency test of a
  de Sitter-Unruh inertia scale, and why its redshift evolution is not yet measurable from SNe alone"
- (shorter) "a0 from supernovae: a cross-scale check against SPARC, and an honest null on da0/dz"

**Standalone vs fold-in:** The a0(0) result is real but INPUT-DRIVEN (the Lambda -> a0 identity),
and the a0(z) slope is a null -- so on its own the paper is thin. Recommended: **fold it into the
a0-line paper** as the cosmological-footing section (SNe rho_DE -> a0(0) cross-checks the SPARC
GLS a0-line measurement from the other end), keeping the a0(z)-slope null and the DESI hook as an
explicit "what SNe can and cannot do" subsection. It strengthens the a0-line paper's cross-scale
story more than it stands alone. No "proves" anywhere.

---

## 4. NEXT
- **Fold into the a0-line paper** as the cosmology-footing / cross-scale section; carry both
  footings, both H0, the Om-marginalized slope null, and the Z-posited caveat verbatim.
- The a0(z) EVOLUTION is a **DESI/BAO+CMB target, not SNe-measurable**: run the same
  rho_DE(z) -> a0(z) pipeline on DESI DR2 BAO + CMB (which DO reach z=3 and DO drive the w0wa
  signal), where a0(z=3)/a0(0) = 0.696 can actually be tested against the 0.60-0.75 band.
- Keep the differentiation-free chi2 with the Om sign-flip displayed (done); never quote -3.10 alone.
- Optional: add diagonal-vs-full-covariance note (current fit uses diagonal errors -- documented).

Scripts (exit 0, reproducible): `extract_a0z.py`, `crossscale.py`. Docs: `EXTRACT.md`,
`CROSSSCALE.md`, `VERIFY.md`. Figure: `a0z_fig.png`. JSON: `crossscale_results.json`.
