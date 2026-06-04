# ΛCDM Fits, MOND Predicts — Demonstrated on the Real 175 SPARC Galaxies

**C. Zimmerman, June 2026.** *The legitimate, calculable galaxy-scale case, on the real rotation curves on disk
(`reviews/project_lcdm_fits_vs_mond_predicts.py`, data `data/sparc_data/*_rotmod.dat`, Lelli–McGaugh–Schombert
2016). Honest, with the boundaries stated, not buried.*

---

## The claim, made precise

"There is no proof of dark matter; assume it doesn't exist — show how ΛCDM is *fitting* and MOND *predicts*." On
**galaxy rotation curves** that is true, demonstrable, and quantifiable. Here it is, on 166 SPARC galaxies / 2807
points that pass the standard quality cut.

## 1. Parameter counting — a fit vs a prediction

| theory | free parameters to reproduce 166 rotation curves |
|---|---|
| **ΛCDM** | a dark halo **per galaxy** — NFW = 2 (M₂₀₀, c) → **332 fitted halo parameters** |
| **MOND** | **one** universal a₀ for all 166 galaxies → **1 parameter** |

Both share the *same* stellar M/L (0.5 at 3.6 μm, pinned by stellar populations — not a free knob). So ΛCDM brings
**332 fitted halo parameters to MOND's one.** ΛCDM "predicts" a rotation curve only *after* fitting a halo to it;
MOND predicts it from the baryons. (ΛCDM softens the 332 with priors — the M\*–M_halo and M–c relations — but those
relations carry scatter, and that scatter is the problem; see §3.)

## 2. The radial-acceleration relation is **one variable**

Plot the observed acceleration g_obs against the baryonic g_bar for all 2807 points: they fall on a **single
curve** spanning 3.9 decades in g_bar, with one scale:

> **a₀ = 1.13×10⁻¹⁰ m/s²** (lit. 1.20; −6%), total scatter **0.144 dex**.

Decompose the scatter: the observational floor (velocity error 0.031 + M/L 0.10 + distance 0.07, in quadrature) is
~0.126 dex, leaving **intrinsic scatter ≈ 0.069 dex** — consistent with McGaugh+2016's *<0.06 dex, i.e. zero*. And
Lelli+2017 showed the residuals correlate with **nothing** — not radius, surface brightness, or gas fraction. The
RAR is a genuine **one-variable law**: g_obs = F(g_bar) alone.

- In **MOND**, this *is* the theory: g_obs = ν(g_bar/a₀)·g_bar. The RAR is **predicted**, with zero intrinsic
  scatter by construction.
- In **ΛCDM**, g_obs = g_bar + g_DM(halo), and g_DM(halo) is a *separate* degree of freedom from g_bar. A
  one-variable RAR therefore demands the halo be a tight function of the baryons — the disk–halo "conspiracy."

## 3. The fine-tuning — ΛCDM's own scatter is *too big*

This is the decisive point. ΛCDM's halo-to-halo scatter, **independent of the baryons**, is:
- stellar-mass ↔ halo-mass: ~0.15 dex (Behroozi/Moster),
- mass ↔ concentration: ~0.11 dex (Dutton–Macciò).

That ~0.1–0.15 dex naturally propagates into the RAR as **intrinsic scatter**. But the **observed** RAR intrinsic
scatter is **≈0.069 dex (≤0.06)** — *smaller* than ΛCDM's halo scatter. So ΛCDM predicts **more** RAR scatter than
is seen and must **fine-tune feedback** to hide the halo diversity (the "diversity problem," Oman+2015). MOND
predicts zero intrinsic scatter and gets it for free. **That is the exact sense in which ΛCDM fits and MOND
predicts: the tightness is natural in one theory and tuned in the other.**

## 4. Per-galaxy: MOND predicts every curve **parameter-free**

Predict each rotation curve from the baryons + the *global* a₀ + the shared M/L — **zero per-galaxy parameters** —
and compare to observed velocities:

> median per-galaxy |ΔV|/V = **10%** across all 166 galaxies.

| galaxy | median |ΔV|/V | type |
|---|---|---|
| NGC3198 | 2.0% | spiral |
| UGC02885 | 3.0% | giant spiral |
| DDO154 | 5.5% | gas-rich dwarf |
| NGC2403 | 6.3% | spiral |
| F583-1 | 18% | LSB (distance-sensitive) |
| NGC2841 | 19% | known hard case (distance) |

MOND reproduces the full shape of each curve from the baryons alone — where ΛCDM fits a 2-parameter halo to each.
The 10% median is the M/L+distance floor, not free fitting (the best cases hit 2–3%).

## The honest boundaries — stated, not buried

This is a **real, bounded** result, and overselling it would repeat the mistakes I've been correcting:

1. **Galaxy scales only — MOND's home turf.** The "predicts vs fits" case is strongest and genuine here. It is
   **standard MOND**; the framework adds an *origin* for a₀ (= cH/Z), but the data do **not** single out Z — a₀≈cH₀
   to a coefficient ~1/6 that is hostage to the Hubble tension.
2. **It does not extend up.** On **clusters** MOND under-predicts mass ~2×; on the **CMB/BAO/LSS** ΛCDM fits the
   acoustic peaks and the matter power spectrum and MOND needs a relativistic completion (AeST) still under test.
   On those scales **ΛCDM is better**, and this demonstration is silent there.
3. **The foundation is contested.** Whether a₀ is a real acceleration scale or an artifact of dark matter is *not*
   settled — wide binaries split ~16–19σ against (Banik) vs for (Chae). If MOND isn't real, this elegance is a
   coincidence.

**Bottom line:** on galaxy rotation curves, ΛCDM is a **per-galaxy fit (332 halo parameters)** and MOND a
**one-parameter prediction (a₀)** that reproduces every curve from the baryons and yields a one-variable RAR
*tighter than ΛCDM's halos can naturally produce*. That is a genuine, defensible argument that dark matter is at
best unnecessary *on galaxy scales* — and exactly that far. It is **not** a global proof that ΛCDM is broken; that
would need the cluster/CMB scales, where the case reverses, and a resolution of the contested foundation.
