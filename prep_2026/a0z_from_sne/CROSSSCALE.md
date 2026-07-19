# Cross-scale / decline-comparison lane — a0(z) from Type Ia SNe

**Framework:** de Sitter–Unruh **modified-inertia** (Carl Zimmerman). Dark-energy leftover is
read off the SNe point-by-point (no Λ, no w(z) assumed) and converted to the galaxy
acceleration scale:

    rho_DE(z) = 3[H(z)^2 - Om H0^2 (1+z)^3] / (8πG)
    a0(z)     = (c/2) sqrt(G rho_DE(z)) = (c/Z) sqrt(H(z)^2 - Om H0^2 (1+z)^3),  Z = sqrt(32π/3) = 5.789

This is the **canonical rho_DE footing** by construction. **Z is POSITED** — the a0 *magnitude*
inherits it (not derived here). The **ratio** a0(z)/a0(0) is independent of Z, of H0, and of M_B;
it depends only on the reconstructed shape E(z)=H/H0 and on Om.

Data: PantheonPlusSH0ES, cut `IS_CALIBRATOR==0 & zHD>0.01` → **N = 1580** cosmology SNe, z ∈ [0.010, 2.261].
Inputs that remain (stated, not circular): Om (Planck 0.315, range 0.29–0.35; matter ≠ dark energy),
GR/Friedmann background (framework keeps GR for the background), H0 (67.4 and 73.0; SNe are M_B–H0
degenerate so a0(0) carries H0, the shape does not). Diagonal errors only (documented caveat; the
full covariance would widen the reconstruction bands, not tighten them).

Script: `crossscale.py` (exit 0). Machine output: `crossscale_results.json`.
Credits: Milgrom (a0 kernel); Brout+2022 / Scolnic (Pantheon+SH0ES); Seikel-Clarkson-Smith 2012 (GP model-independent H(z)).

---

## (a) SNe-derived a0(0) vs SPARC-measured a0 — sigma-tension, both H0

`a0(0) = (c/Z) H0 sqrt(1-Om)` — the exact z→0 limit (E(0)=1 by definition), so **no reconstruction
noise enters a0(0)**. SPARC (GLS gas-dominated, Λ-blind) = **1.1814e-10 ± 1.89e-11 (16%)**.

| H0 (km/s/Mpc) | a0(0) [Om=0.315] | a0(0) over Om 0.29–0.35 | tension vs SPARC |
|---|---|---|---|
| 67.4 | 9.362e-11 | 9.12e-11 – 9.53e-11 | **+1.29 σ** |
| 73.0 | 1.014e-10 | 9.88e-11 – 1.03e-10 | **+0.88 σ** |

(tension error = quadrature of SPARC's 16% and the Om-spread; the latter is sub-dominant, ~2e-12.)

**Result:** the SNe-derived a0(0) sits **~1σ below** the independently SPARC-measured a0 —
**consistent, not in tension**. With the local (SH0ES) H0=73.0 the agreement is better (0.88σ).
Note the Planck-H0 value 9.36e-11 reproduces the framework's canonical a0 to 3 figures (it is the
same `(c/Z)H0√(1-Om)` construction). No footing lean was applied — this is the rho_DE/cH_Λ footing
by construction.

## (b) a0(z=3)/a0(0) — SNe vs framework 0.60–0.75

`a0(z)/a0(0) = sqrt[(E(z)^2 - Om(1+z)^3)/(1-Om)]` (H0-independent; Om=0.315).

**Reference hypotheses (clean analytic):**

| model | z=1 | z=2 | z=3 |
|---|---|---|---|
| DESI CPL w0wa=(−0.83,−0.75) | 0.960 | 0.814 | **0.696** |
| ΛCDM (constant Λ) | 1.000 | 1.000 | 1.000 (flat) |

The DESI-preferred decline gives **a0(z=3)/a0(0) = 0.696 — inside the framework's 0.60–0.75 band.**
So *a DESI-like evolving dark energy is quantitatively the kind of a0(z) decline the framework wants.*

**Model-independent SNe reconstruction (GP on binned m_b_corr, analytic-limit normalization,
finite-difference E(z), 600 posterior draws):** rho_DE is a **small residual E²−Om(1+z)³ = difference
of two large numbers**, and getting it requires differentiating d_L. The reconstruction is only
trustworthy where SNe are dense:

- sign of rho_DE(z) is pinned (f_phys≥0.9) **only out to z≈0.40**;
- deepest reliable point z=0.40: rho-ratio +1.90 [+0.36, +5.49] → a0-ratio ≈1.4, a band that
  **overlaps both flat (=1) and the framework (0.36–0.56 in rho-ratio)**;
- by z≈0.5–0.7 the posterior is **sign-indefinite** (rho_DE consistent with <0);
- **z=3 is beyond the data (zmax=2.26): there is no SNe a0(z=3) measurement to report.**

So SNe alone **cannot measure** a0(z=3)/a0(0) model-independently. The 0.696 figure is the DESI-model
reference, **not** a SNe measurement.

## (c) Constraining, or consistent-with-flat?

Robust, **differentiation-free** test — offset-marginalized χ² fit of the two hypotheses to all
1580 SNe (M_B+5log₁₀(c/H0) marginalized analytically; Om=0.315 both):

    chi2(flat-LCDM) = 697.87
    chi2(DESI-CPL)  = 694.77   ->  Delta-chi2 = -3.10   (~1.8 sigma, mild preference for the decline)

**Non-decisive: SNe cannot separate flat from the DESI-like decline at 2σ.** Consistent with the
banked expectation (SNe alone Δχ²~O(1) for evolving DE). Both routes — the model-independent
reconstruction (band overlaps flat *and* 0.60–0.75) and the direct fit — say the same thing:

> **SNe alone are NON-CONSTRAINING on a0(z) evolution.** They neither detect nor exclude the decline.
> The robust SNe output is **a0(0)** (≈9.4e-11 at H0=67.4, ≈1.01e-10 at H0=73.0), which agrees with
> the SPARC-measured a0 at ~1σ. da0/dz is **not distinguishable from zero** from SNe alone; the clean
> decline numbers (0.696 at z=3) come from the DESI/ΛCDM model references, not a SNe reconstruction.

## Footing / caveats

- Primary = **rho_DE / cH_Λ footing** (the `a0=(c/2)√(G rho_DE)` construction). Alt rho_total/cH0
  footing (~1.13e-10) uses the full H² rather than the DE part; the (b)/(c) **ratios are footing-robust**
  (Z and the absolute scale cancel).
- **Z is posited**; the a0 magnitude inherits it. No "proves" — a0(0) agreement and the decline
  comparison are consistency statements, not derivations.
- Diagonal-only SNe errors: including the full Pantheon+ covariance broadens the reconstruction
  bands, strengthening (not weakening) the "SNe non-constraining on a0(z)" conclusion.
- The careful nonparametric H(z) with full error band is the reconstruction lane's deliverable;
  this lane consumes the z→0 limit (robust) and demonstrates the high-z reconstruction is
  noise-limited.
