# Can DESI Confirm a₀(z) ∝ √ρ_DE? — An Honest Assessment

**C. Zimmerman, June 2026.** *Direct answer to "does DESI have data that can confirm the prediction?" Verified
against the DESI releases and the high-z kinematics literature. Short version: **no — DESI supplies the input curve,
not the confirmation.** It is a redshift survey, not a kinematics survey, so it cannot measure a₀'s evolution. The
decisive test is high-z galaxy kinematics (JWST/ALMA), which exists independently of DESI — and the faithful √ρ_DE
version's signal is small enough that current data *tolerate* it without confirming it.*

---

## What DESI gives you: the input, and a sharper one with DR2

- **BAO → H(z) → w(z) → ρ_DE(z).** This is exactly the input the prediction needs. **DESI DR2 (2025, arXiv:2503.14738)
  strengthened** the evolving-dark-energy preference over DR1: now **2.8–4.2σ** depending on the SN sample (3.1σ for
  DESI+CMB alone), with **w₀ = −0.752 ± 0.057, wₐ = −0.86 ± 0.22** (DESI+CMB+DESY5). The sign (w₀ > −1, wₐ < 0) is
  what the framework needs — ρ_DE was *lower* in the past — so a₀ ∝ √ρ_DE declines into the past. With the DR2 w(z),
  the predicted a₀(z)/a₀(0) = 1.01, 0.86, 0.74 at z = 1, 2, 3.
- **A growth cross-check** (RSD fσ₈, the μ/Σ modified-gravity parameters; Ishak et al. 2025, arXiv:2411.12026) — all
  consistent with GR/ΛCDM, which neither confirms nor refutes a *galactic* a₀ coupling (different physics, different
  scales).
- Caveat: DESI's evolving-DE signal is still below 5σ, SN-sample-dependent, and contested (~3σ on Bayesian grounds).

## What DESI cannot do: measure a₀'s evolution

DESI does **not** produce the resolved rotation curves / dispersion profiles that a₀ requires. Its only kinematic
component — the **Peculiar Velocity survey** (Tully–Fisher + Fundamental Plane) — is **z < 0.15 (≈75% at z < 0.1)**,
i.e. effectively *a₀ today*, with no redshift leverage on the evolution; and DESI marginalizes the TF/FP zero-point
as a nuisance for distances, not as a₀. So **no DESI product measures a₀(z).** No DESI MOND / a₀ analysis exists.

## The real test exists — and it isn't DESI's

- **Limbach, Psaltis & Özel (2008, arXiv:0809.2790)** tested *exactly* the framework's two competing couplings —
  a₀ ∝ cH₀ vs a₀ ∝ √ρ_DE — via Tully–Fisher to z=1.2, and **marginally favored the √ρ_DE (dark-energy) coupling.**
  External support for the faithful reading.
- **High-z baryonic Tully–Fisher (Nestor Shachar et al. 2023, ALMA/IFU kinematics)** shows **no significant evolution
  to z ≈ 2.5.** This **rules out a₀ ∝ cH(z)** (which would shift the BTFR a lot) and **tolerates a₀ ∝ √ρ_DE**, whose
  shift is small.

## The honest quantification — and the honest tension

The faithful √ρ_DE signal in the BTFR (V_flat ∝ a₀^¼ at fixed baryonic mass), with DESI DR2 w(z):

| z | a₀/a₀(0) | V_flat shift | in dex |
|---|---|---|---|
| 1 | 1.01 | +0.2% | +0.001 |
| 2 | 0.86 | −3.6% | −0.016 |
| 3 | 0.74 | −7.3% | −0.033 |

The BTFR intrinsic scatter is ~0.026 dex (Lelli+2019). So the z=2 signal (0.016 dex) is *below* the scatter and the
z=3 signal (0.033 dex) is ~scatter-sized — **consistent with the observed "no evolution to z~2.5," hence tolerated
but not detected.** Detecting it requires *averaging* ~tens of z~3 deep-MOND discs (the JWST/ALMA sample already
proposed) — invisible to DESI.

**The honest tension:** the version of the framework that *survives* the data (√ρ_DE, mild) is also the *hardest to
confirm* — its signal is small precisely because it tracks the slowly-varying dark energy rather than the
fast-varying Hubble rate. The disfavored Hubble version would have been easy to detect (and was, against it); the
surviving version needs precision the current data don't yet have.

## What's actually in DR1 (checked against the release, 2503.14745 + the data-products page)

DR1 is **18.7M redshifts** (13.1M galaxies, 1.6M QSOs, z=0–4) plus: the **redshift catalog**, **LSS clustering
catalogs**, and **value-added catalogs** (stellar mass, emission-line fluxes, SED fits, AGN classification). What it
does **not** contain: resolved rotation curves, velocity-dispersion *profiles*, dynamical masses — **no internal
kinematics.** DESI is single-fiber spectroscopy of positions, not a kinematics survey. So there is no direct a₀ in DR1.

**The one concrete avenue it *does* enable** — and nobody has done it: the **emission-line widths** of the millions
of ELGs (to z≈1.6) are an *integrated* kinematic tracer, so one could build a **statistical line-width Tully–Fisher
relation** vs redshift and read a₀(z) off its zero-point. The catch is quantitative:

| z (DESI reach) | a₀/a₀(0) (√ρ_DE) | V_flat shift |
|---|---|---|
| 0.5 | 1.06 | +1.5% |
| 1.0 | 1.01 | +0.2% |
| 1.5 | 0.94 | −1.7% |

Within DESI's range (z<1.6) the faithful √ρ_DE signal is **<2% in V_flat** — *below* the systematic floor of
integrated line-width TF (~5–10%: inclination, fiber aperture, seeing, line-width→V calibration). **Statistics are
not the limit** (millions of ELGs pin the mean to <0.1%); **systematics are.** To reach a 1–2% signal you'd need the
line-width→velocity systematics controlled to ~1% across redshift — hard and unprecedented, though the sample size
makes it conceivable. Even done perfectly, it would mostly **reconfirm "a₀ near-constant to z~1.6"** (killing the
steep Hubble version, consistent with √ρ_DE *and* constant). The *decisive* √ρ_DE signal (~7% in V) is at **z~3,
beyond DESI's reach** — resolved JWST/ALMA kinematics, not DESI single-fiber spectra.

## Bottom line

**DESI cannot confirm a₀(z) ∝ √ρ_DE.** It supplies the ρ_DE(z) *input* — and DR2's 4.2σ-leaning evolving-DE result
makes that input sharper and the predicted ~0.74× decline at z=3 concrete — plus a GR-consistent growth cross-check.
But confirmation is a **high-z galaxy-kinematics** measurement (JWST/ALMA BTFR at z~3), which is DESI-independent,
already underway, currently *consistent with constant a₀*, and needs ~tens of clean z~3 deep-MOND discs to reach the
small √ρ_DE signal. The honest status: **DESI sets the target; the data so far tolerate the faithful prediction
without confirming it; the decisive measurement is JWST/ALMA, not DESI.**
