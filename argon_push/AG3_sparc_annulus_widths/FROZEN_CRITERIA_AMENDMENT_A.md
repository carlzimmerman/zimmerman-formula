# AG3 — FROZEN CRITERIA AMENDMENT A (committed BEFORE any data run; design-stage algebra)

**Why:** deriving the exact per-point law algebra (before touching the data) shows the
freeze's `r_lo(f) = r_M·2f/(f²−1)` corollary assumes a POINT-MASS baryon profile
(M(r) = M_b). The exact law identity for law-obeying curves is

    ρ(r) ≡ r·g_ph/C = √(M(r)/M_b) · 1/(√(u+1) + √u),     u = ḡ(r)/a₀ = G M(r)/(a₀ r²)

with M(r) = r²ḡ/G the ENCLOSED baryonic mass (directly measured per point from the
corpus baryon model). For gas-extended dwarfs M(r) ≪ M_b well outside the nominal
(4/3)r_M, so the point-mass corollary can overestimate annulus widths by factors of
several — enough to flip the K3 branch for exactly the population where the extraction
is least certain. This amendment replaces the K2 point-mass cross-check with the exact
identity. Legitimacy: no data has been run (frozen criteria committed 4560f945c; this
amendment commits before the first pipeline execution); the original file is kept
unmodified (append-only).

## K2 as amended (pre-run)

- **K2a — exact law identity in ρ-space (report; tolerance declared, not exit-gated):**
  per valid point, ρ_pred(r) = √(M(r)/M_b)/(√(u+1)+√u) with measured M(r), u. Report
  median and IQR of ln(ρ_meas/ρ_pred) over all galaxies/points. Expected scale: the
  registered law benchmark rms ~0.15 dex (G071); ρ is a difference quantity so noise is
  amplified — tolerance for a quiet flag: median |ln| < 0.25. ≥ 0.25 ⇒ loud DATA-QUALITY
  flag (K3 reported with the caveat, not silently).
- **K2b — r_lo exact prediction (EXIT-GATED pipeline sanity):** per galaxy, r_lo_pred =
  radius where ρ_pred(r) = 1/2 (log-r interpolation between consecutive valid points).
  If ρ_pred ≥ 1/2 already at the innermost valid point: left-censored (r_lo_pred =
  r_lo_meas = R_min; census of censored galaxies recorded; those galaxies contribute
  equality to K2b and are flagged in K3 as width lower-bounds).
  **PASS iff median |ln(r_lo_meas/r_lo_pred)| < 0.15** over non-censored eligible
  galaxies. Failure ⇒ the band extraction is not measuring what the law algebra says ⇒
  lane verdicts CONDITIONAL (loud).
- **K2c — point-mass corollary (report only):** median ln(r_lo_meas/((4/3)r_M)) and the
  median enclosed-mass correction ln√(M(r_lo)/M_b) that explains the offset.

## Everything else in FROZEN_CRITERIA.md stands unchanged

(K1, K3 decision bands and verdict logic, K4 interior discriminator bands, K5 band
robustness, Part B exploratory — with one algebraic correction recorded here for Part B:
with the local-hydrostatic σ²(r) = (GM_b/r + C)/2 the drift does NOT cancel; assembling
from primitives gives σ²(r)ξ″ − (GM_b/(2r²))ξ′ + (C/r² + ω²)ξ = 0 — the script assembles
this symbolically from the primitive equations and prints the coefficients rather than
typing the ODE. M1: with the exact-identity K2b, the M_b shuffle must degrade
median |ln(r_lo_meas/r_lo_pred)| > 0.3 — sensitivity check unchanged in spirit, new
number frozen here.)

**Bias ledger (frozen, both directions):** (i) M_b = outermost enclosed mass
underestimates ⇒ r_M, C underestimated ⇒ ρ_meas inflated ⇒ r_lo biased INWARD, w biased
UP ⇒ branch F favored; a verdict of S is robust against (i). (ii) Left-censoring
(dwarfs already in-band at R_min) ⇒ r_lo = R_min is the LARGEST available estimate ⇒ w
biased DOWN ⇒ branch S favored for those galaxies; census must be reported and the K3
verdict recomputed with censored galaxies excluded (robustness — flip ⇒ CONDITIONAL).
