# H025 — PRE-REGISTRATION: the RAR's redshift evolution (H024's prediction)

**Frozen:** 2026-09-15, before any high-z scatter measurement beyond H024's
crude two-bin split.
**Lane owner:** hy4_push. **Data:** existing repository holdings, no new
acquisition.

---

## 0. What is being tested

H024 derived that the dark sector has two components with different redshift
behaviour:

- **Phantom** (equilibrated, baryon-tied): ratio to baryons `= a₀/g_ext(z)`
- **Free dust** (not equilibrated, baryon-blind): independent of `a₀`

Because `g_ext` grows with redshift, the **phantom share falls with z**. The
phantom is the component that ties dark mass to baryons — that *is* what the
radial acceleration relation is. Therefore:

> **PREDICTION: the RAR weakens with redshift. Its scatter grows as the
> inverse phantom share.**

The phantom share was computed in H024:

| z | 0 | 0.3 | 0.6 | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|---|
| share | 11.8% | 8.3% | 6.2% | 4.5% | 3.3% | 2.5% | 1.6% |

---

## 1. The prediction, in a usable form

Let `s(z)` = the phantom share. The predicted RAR scatter is

$$\sigma(z) \;=\; \sigma_0\,\frac{s(0)}{s(z)}$$

with `σ₀ = 0.064 dex` — the **registered local floor** from G013 (per-galaxy
M/L freedom, median over 155 SPARC curves). This is not a free parameter: it
was measured in a different lane, on different data, for a different purpose.

Predicted values (frozen now):

| z | 0 | 0.3 | 0.6 | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|---|
| σ [dex] | 0.064 | 0.091 | 0.122 | 0.168 | 0.229 | 0.293 | 0.44 |

---

## 2. Thresholds — FROZEN BEFORE MEASUREMENT

**PASS** — the measured high-z RAR scatter exceeds the local floor by at least
**1.5×**, *and* the increase is monotone in z across ≥ 3 bins, *and* the
normalised excess `σ(z)/σ₀` matches `s(0)/s(z)` within a factor of 2 at every
bin.

**FAIL (the kill)** — the measured high-z scatter is **≤ 1.2×** the local
floor in every bin. That kills the evolving-partition prediction: the dark
sector would then have the same character at all epochs, and H024's central
claim is false.

**INSTRUMENT-FAIL** — fewer than 10 galaxies in any bin; or no reliable
baryonic surface density per galaxy (H024's confound class: without baryons
per galaxy there is no RAR, only fDM); or the sample's z-baseline is too
narrow to span a factor 1.5 in predicted scatter.

**NOT ESTABLISHED** — the trend is in the predicted direction but below the
1.5× threshold or non-monotone. Recorded as such, not spun.

---

## 3. Data held in this repository

| Set | N | z | Has per-galaxy baryons? | Useable for a RAR? |
|---|---|---|---|---|
| SPARC (L232) | 175 | 0 | **yes** | yes — the local anchor |
| MSA-3D 2026 | 30 | 0.6–1.2 | `mstar`, `vrot`, `fDM` | **yes** (needs Σ_b from mstar) |
| WALLABY DR2 (G044) | 203 | ~0 | **no masses** | no |
| THINGS / LITTLE THINGS | 45 | 0 | inherited model | yes, with caveats |

**The honest constraint:** only MSA-3D has both redshift leverage and
per-galaxy stellar mass. 30 galaxies spanning z = 0.6–1.2 is a **factor 1.5
in predicted scatter** (0.12 → 0.17 dex) — barely at the threshold. So the
realistic outcome of THIS data is **NOT ESTABLISHED** or a weak PASS, and that
is a legitimate result.

The decisive test needs a larger high-z IFU sample. This pre-registration is
written so that when one arrives, the thresholds are already set and cannot be
moved.

---

## 4. Method — frozen

1. **Local anchor.** Recompute the SPARC RAR scatter with per-galaxy M/L
   freedom by the G013 recipe. Confirm `σ₀ = 0.064 dex`. If this fails to
   reproduce, everything downstream is void — stop.
2. **High-z sample.** From MSA-3D take `mstar`, `vrot`, `fDM`, `z`. Derive
   baryonic surface density `Σ_b` from `mstar` and the quoted radius; derive
   `g_obs` from `vrot`; derive `g_bar` from `Σ_b`. **If the file lacks the
   radius needed for `Σ_b`, declare INSTRUMENT-FAIL rather than inventing
   one.**
3. **Binning.** Bin by z into ≥ 3 bins with ≥ 10 galaxies each. If impossible,
   declare INSTRUMENT-FAIL.
4. **Measurement.** In each bin compute the rms of `log10(g_obs) −
   log10(g_obs_predicted)` where the prediction is the **zero-parameter**
   theory curve (μ₂, a₀ from Λ). Report dex.
5. **Comparison.** Plot measured `σ(z)` against the frozen prediction
   `σ₀·s(0)/s(z)`. Apply §2.

---

## 5. Why this is worth pre-registering

This is the theory's **only prediction about the epoch dependence of the dark
sector's character**. ΛCDM has no such prediction (its dark matter is the same
substance always). MOND has none (its force law has a fixed shape). If the RAR
scatter does *not* grow with z, H024's two-component partition is wrong and
the amplitude law's physical interpretation changes — even though H021's
arithmetic would survive.

So this test discriminates between the **arithmetic** of the amplitude law
(which is already certified) and its **physical reading** (which is not).

---

## 6. Rules

- Both a₀ footings throughout (9.3619e-11 canonical, 1.1279e-10 alternative).
- No new parameters. `σ₀` is G013's, `a₀` is H016's, the share is H024's.
- Every check prints measurement and threshold separately.
- A FAIL is a result; an INSTRUMENT-FAIL is a result. Neither is massaged.
- The words "confirms", "closed", "derived" are reserved for what a gate
  produced.
- Never stage another track's files.
