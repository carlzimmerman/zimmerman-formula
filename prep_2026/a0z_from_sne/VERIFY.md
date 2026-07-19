# VERIFY — a0(z) from Type Ia SNe (adversarial re-run, both ways)

Framework: de Sitter–Unruh MODIFIED-INERTIA (Carl Zimmerman). Read rho_DE(z) off the
Pantheon+SH0ES Hubble diagram point-by-point (NO Lambda, NO w(z) assumed), convert to
`a0(z) = (c/Z) sqrt(H(z)^2 - Om H0^2 (1+z)^3)`, Z = sqrt(32pi/3) = 5.78881 (POSITED).
Credits carried in-code: Milgrom (kernel), Brout+2022/Scolnic+2022 (Pantheon+),
Seikel-Clarkson-Smith 2012 (GP model-independent H(z)).

Re-ran `extract_a0z.py` and `crossscale.py`. Both **exit 0, zero stderr warnings**, and
reproduce their banked numbers exactly (1580 cosmology SNe, z 0.010–2.261). Then ran three
independent adversarial cross-checks (scratchpad only; frozen repo untouched).

---

## (1) THE KEY QUESTION — is any a0(z) DECLINE real, or reconstruction noise?

**No decline is manufactured, and this is robust.** Independent smoothing test with 4
kernels/bandwidths on the binned Hubble diagram (finite-difference derivative, a *noisier*
method than the script's analytic one, so a stress test):

| kernel / bandwidth (fitted)        | a0(0.5)/a0(0) [68%]      | a0(1)/a0(0) [68%]        |
|------------------------------------|-------------------------|--------------------------|
| RBF, ell free → 0.12               | 1.20 [0.48, 3.32]       | 4.11 [1.37, 13.4]        |
| RBF, ell forced short ~0.15        | 1.20 [0.57, 2.52]       | 3.68 [1.43, 13.5]        |
| RBF, ell forced long ~1.0          | 2.29 [0.73, 8.23]       | 2.66 [1.22, 9.11]        |
| Matern nu=1.5, ell → 0.72          | 2.34 [0.88, 7.91]       | 3.32 [1.16, 11.7]        |

Every kernel gives ratio **> 1 (flat-to-RISING), never a decline**. No smoothing choice
produces the framework's predicted 0.60–0.75 drop. The *magnitude* of the (spurious) rise
and the band width are strongly kernel-dependent — direct evidence the shape past z~0.5 is
noise-dominated, not a measurement.

**Band honesty — PASS.** `extract_a0z.py` uses the correct analytic joint [mu, mu']
posterior (SCS2012): builds Kss − Ks Ksolve(Ksᵀ), Cholesky, 3000 correlated MC draws.
This is genuine propagated GP posterior variance, not finite-difference noise, and is
correctly *tighter* than my finite-difference cross-check. Caveat surfaced: the analytic
band at a **single** kernel (a0(0.5)/a0(0)=1.077 [1.03,1.12]) understates the
**kernel/model** uncertainty — across kernels the central value slides 1.08→2.34. This does
not change the verdict (no kernel yields a decline) but reinforces "SNe cannot measure the
slope." rho_DE(z) sign is pinned (f_phys≥0.9) only to **z~0.40**; z=3 is pure extrapolation
(zmax=2.26), correctly flagged.

## (2) Is a0(0) robust, or an Om/H0 artifact?

**Robust — but INPUT-DRIVEN, not an SNe extraction.** a0(0) = (c/Z) H0 sqrt(1−Om) is
analytic (E(0)=1 exact); **the SNe data does not enter a0(0) at all.** Reproduced to 4 sig figs:

| H0    | Om=0.29    | Om=0.315   | Om=0.35    |
|-------|------------|------------|------------|
| 67.4  | 9.532e-11  | **9.362e-11** | 9.120e-11 |
| 73.0  | 1.032e-10  | **1.014e-10** | 9.878e-11 |

H0=67.4/Om=0.315 reproduces canonical 9.355e-11 by construction. Om spread is ±~2.3% (small).
This is the framework's **known Lambda→a0 identity**, robust precisely because it bypasses the
noisy reconstruction — honest to call "SNe-noise-free," but it should NOT be oversold as a new
SNe *measurement* of a0. Cross-scale vs SPARC (1.181e-10 ± 16%): **+1.29σ** (H0=67.4),
**+0.88σ** (H0=73.0) — consistent (<~1.3σ), confirmed.

## (3) GP over/under-smoothing — see (1). Two kernels + 3 bandwidths tested. Conclusion
(no decline; flat-to-rise; unconstrained past z~0.5) is smoothing-robust; point values are not.
Note: the script's optimizer **hits its ell≤0.6 cap** (marginal likelihood wants smoother) —
benign for the verdict (a shorter ell adds wiggle, not a decline) but the cap is a boundary
solution, not an interior optimum.

## (4) Inputs stated, not hidden — PASS. Om (0.315 + range 0.29–0.35) and "GR/Friedmann
background kept" are in both docstrings and print output. Om labeled "matter, not dark energy
→ no circularity." Z labeled POSITED everywhere; a0 magnitude explicitly inherits it.

## (5) Both footings / both H0 — PASS. Canonical rho_DE footing by construction; alt
rho_total/cH(z) footing noted separately (would RISE as E(z), opposite sign). Both H0 (67.4,
73.0) reported throughout; a0 shape H0-robust, a0(0) carries H0.

## (6) Manufactured detection AND manufactured null — checked EQUALLY.
- **No manufactured detection:** no kernel yields a decline (1); z=3 flagged extrapolation.
- **No manufactured null either:** at *fixed* canonical Om=0.315 the reconstruction weakly
  **excludes** flat with a mild RISE, a0(0.5)/a0(0)=1.084 [1.047,1.120] (~1.6σ off 1); only
  **Om-marginalization** restores consistency-with-flat. Shown explicitly in the script. The
  rise is the *opposite* sign of the framework's decline, so no "win" is being suppressed —
  but the flat-consistency is Om-enabled, honestly disclosed.
- **NEW gap (recommend a one-line note in crossscale.py):** the lone quantitative "decline
  hint," Delta-chi2 = −3.10 (~1.8σ pull to DESI-CPL), is **Om-fragile and reverses sign**:
  −7.17 (Om=0.29) → −3.10 (Om=0.315) → **+1.78, favoring FLAT** (Om=0.35). crossscale.py
  quotes only the −3.10 canonical-Om value. The hint is an Om artifact, exactly like the
  low-z rise — consistent with the "non-detection" verdict, but the write-up under-hedges.

## (7) Z-posited caveat — PASS, carried on the a0 magnitude in both scripts and JSON.

---

## VERDICT — HONEST BOTH WAYS. No decline manufactured, no null manufactured.

- **a0(0) is the robust deliverable** = the local Lambda leftover, (c/Z)H0√(1−Om) = 9.36e-11
  (H0=67.4, canonical) / 1.014e-10 (H0=73.0), each ~1σ from the SPARC-measured 1.181e-10. But
  it is **input-driven (H0, Om), not an SNe extraction** — the framework's Lambda→a0 identity,
  re-confirmed, not newly measured by these SNe. Z posited; magnitude inherits it.
- **The a0(z) SLOPE is NOT detectable from SNe alone.** Differentiating d_L amplifies noise;
  the sign of rho_DE(z) is pinned only to z~0.40; every kernel/bandwidth gives flat-to-rise,
  none gives the 0.60–0.75 decline. The single decline hint (Δχ²=−3.10) is non-decisive AND
  Om-fragile (reverses to +1.78 at Om=0.35). Both the mild low-z rise and the mild decline
  hint wash out under Om-marginalization — the correct honest treatment the extract slope test
  already applies.
- **Cross-scale:** a0(0) cross-checks against SPARC at ~1σ (genuine, on the rho_DE footing);
  a0(z) evolution is a DESI/BAO+CMB target, **not** measurable from SNe. If DESI's w0wa decline
  is real it gives a0(z=3)/a0(0)=0.696, inside the framework's 0.60–0.75 band — but SNe cannot
  establish that decline. No "proves."

**Scripts exit 0, reproducible, inputs/footings/credits/Z-caveat all in place.** One
recommended (non-blocking) edit: add the Om-sign-flip of Δχ² to crossscale.py so the −3.10 is
not read as a standalone decline hint.
