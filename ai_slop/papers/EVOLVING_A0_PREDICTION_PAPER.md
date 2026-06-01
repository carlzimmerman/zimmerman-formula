# An Evolving MOND Acceleration Scale a₀ ∝ H(z): A Falsifiable Prediction for High-Redshift Galaxy Kinematics

**Carl Zimmerman** · Draft, 2026-05-31

*A standalone statement of the one distinctive, forward-testable prediction. It does not
depend on the Z²/orbifold framework — the value of Z cancels — and is presented here on its
own scientific merits.*

---

## Abstract

The MOND acceleration scale satisfies the long-noted coincidence a₀ ≈ cH₀ (Milgrom). We take
this literally and **dynamical**: we hypothesize that a₀ tracks the *instantaneous* cosmic
expansion rate,

> **a₀(z) = a₀(0) · H(z)/H₀ = a₀(0) · √(Ω_m(1+z)³ + Ω_Λ)**,

rather than being constant (a₀ ∝ √Λ). The two options are observationally identical today and
diverge at high redshift. In the deep-MOND regime the baryonic Tully–Fisher relation
v_flat⁴ = G M_bar a₀(z) is parameter-free, so an evolving a₀ **shifts the BTFR zero-point by
E(z)^{1/4}** — an order-unity effect at z > 10. We give **pre-registered, fixed-coefficient**
predictions for named JWST galaxies: evolving-a₀ predicts flat velocities of **120–140 km/s**
at z > 10 versus **50–65 km/s** for constant-a₀, a cleanly separable factor of 2.2–2.4. The
single z > 10 galaxy with measured kinematics (GN-z11) is consistent at ~1σ. The decisive test
is the z > 12 sample now becoming accessible to JWST/NIRSpec and the ELT.

---

## 1. Background

MOND (Milgrom 1983) reproduces galaxy rotation curves and the baryonic Tully–Fisher relation
with a single acceleration scale a₀ ≈ 1.2×10⁻¹⁰ m/s². It has long been noted that
a₀ ≈ cH₀/(2π), tying the scale to cosmology. Two readings are possible:

- **a₀ ∝ √Λ** (constant): a₀ is set by the cosmological-constant scale and does not evolve.
- **a₀ ∝ H(z)** (evolving): a₀ tracks the full expansion rate, which was larger in the past.

Both match all z ≈ 0 data. They are distinguished only by **how galaxy dynamics behaved when
the universe was expanding faster** — i.e. at high redshift. We make the evolving choice
explicit and falsifiable. We do not claim a first-principles derivation of a₀ ∝ H(z); it is a
phenomenological hypothesis, and the present paper is about its **prediction**, not its origin.

## 2. The prediction

In the deep-MOND regime (internal accelerations a < a₀), the asymptotic flat rotation velocity
obeys the exact relation

> **v_flat⁴ = G · M_bar · a₀(z)** ,  and for pressure support, σ = (4/9)^{1/4} v_flat.

With a₀(z) = a₀(0) E(z), the BTFR zero-point shifts: at fixed baryonic mass, **galaxies rotate
faster at higher redshift**, by the factor

> **E(z)^{1/4} = [√(Ω_m(1+z)³ + Ω_Λ)]^{1/4}**.

This is the clean, distinctive signature. It is independent of the absolute normalization a₀(0)
(which divides out of the *ratio* of evolving to constant), so it survives the few-percent
uncertainty in a₀ itself.

## 3. Pre-registered predictions (coefficients fixed in advance)

We fix the geometric coefficients **now**, before the measurements exist: f_geom = 1 for
v_flat (the exact MOND BTFR) and 0.816 = (4/9)^{1/4} for the isothermal dispersion. **No
per-galaxy tuning.** (Computation: `a0_evolution_predictions.py`, run 2026-05-31.)

| Galaxy | z | M⋆ (M☉) | E(z) | **v_flat, evolving (km/s)** | v_flat, constant | E^{1/4} |
|---|---|---|---|---|---|---|
| GN-z11 | 10.60 | 1.0×10⁹ | 22.2 | **137** | 63 | 2.17 |
| GHZ2 / GLASS-z12 | 12.34 | 8×10⁸ | 27.4 | **137** | 60 | 2.29 |
| JADES-GS-z14-0 | 14.32 | 4×10⁸ | 33.7 | **121** | 50 | 2.41 |
| MoM-z14 (candidate) | 14.44 | 5×10⁸ | 34.1 | **128** | 53 | 2.42 |

The evolving and constant predictions differ by a **factor 2.2–2.4** — larger than the stellar
mass uncertainty (~0.3–0.5 dex → ~20–30% in v_flat), so the two hypotheses are cleanly
separable once kinematics are measured.

## 4. Current status (honest)

**GN-z11** (z = 10.6) is the only z > 10 galaxy with resolved kinematics (Xu et al. 2024):
v_rot = 257(+138/−117) km/s, σ = 91(+18/−32) km/s. With the *fixed* coefficients the prediction
is v_flat = 137 and σ = 112 km/s — **consistent within ~1σ**, but with large observational
errors. We stress this is *honest consistency*, not the tuned "exact" match obtainable by
adjusting f_geom. The z ≈ 6 JADES dispersion sample (de Graaff et al. 2024) scatters by several
σ in both directions, where stellar-mass uncertainties dominate and the E(z)^{1/4} signal
(~75% at z ≈ 6) is comparable to the noise — *not yet discriminating.*

The robust observable is the **redshift trend** of the BTFR zero-point across a sample, not any
single galaxy.

## 5. The decisive test and falsifier

At z > 12 the evolving (120–140 km/s) and constant (50–65 km/s) predictions separate by more
than a factor of two — beyond the mass-uncertainty budget. Within a few years, JWST/NIRSpec-IFU
and the ELT will measure dispersions/rotation for GHZ2, JADES-GS-z14, and others.

> **Falsifier:** if the measured v_flat/σ of z > 12 galaxies track the **constant-a₀** values
> (~50–65 km/s), or the higher values expected from ΛCDM dark-matter halos with a different
> mass–velocity scaling, then a₀(z) ∝ H(z) is falsified.

## 6. Caveats

- **No relativistic completion.** MOND lacks a fully successful covariant theory; a
  time-varying a₀ raises questions (energy conservation, the relativistic formulation) that we
  do not resolve. This is a phenomenological prediction, not a complete theory.
- **Clusters.** MOND under-predicts mass in galaxy clusters (the residual-mass / Bullet-Cluster
  problem). An evolving a₀ does not obviously cure this.
- **Deep-MOND regime.** v_flat is the asymptotic value (a < a₀(z)); compact high-z cores may be
  partly Newtonian, so the test is the BTFR *trend*, robust to overall normalization.
- **Masses.** Stellar masses carry ~0.3–0.5 dex error; gas raises v_flat by ~2^{1/4} = 1.19.

## 7. Conclusion

a₀ ∝ H(z) is a sharp, falsifiable, parameter-free (once coefficients are fixed) hypothesis that
makes a definite prediction for high-redshift galaxy kinematics, distinct from both constant-a₀
MOND and ΛCDM. It is independent of any particle-physics framework. The z > 12 galaxies now
within JWST/ELT reach will confirm it (v_flat ≈ 120–140 km/s) or kill it (≈ 50–65 km/s) within
a few years. That is the entire scientific content of this proposal — one number, written down
in advance, that the universe has not yet shown us.

---

*Prediction and figures reproducible from `reviews/a0_evolution_predictions.py`.*
