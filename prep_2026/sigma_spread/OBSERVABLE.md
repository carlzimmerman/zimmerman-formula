# OBSERVABLE-DESIGN LANE — isolating the MI orbit-history σ-spread from anisotropy β(r)

**Date:** 2026-07-17 · **Script:** `observable.py` (this dir, exit 0, numpy/scipy/sympy, both footings) · log `observable.out`.
**Framework:** de Sitter–Unruh MODIFIED INERTIA (Zimmerman) — NOT standard MOND.
ν(y)=√(1+1/y), y=g_bar/a₀, a₀=cH_Λ/Z=9.36e-11; MI = inertia is a time-nonlocal functional of the
body's own worldline (kernel K(□_u/a₀²), τ_mem=2c/a₀=2Z/H_Λ, E10). **a₀'s value and s=−1 remain
postulates.** Milgrom 1983/1999 wellhead credit; dSph kinematics Walker/Wolf/Battaglia; Gaia dSph PMs.

Companion lanes this builds on: `MI_SPREAD.md` (MI amplitude, honestly ~0.2–1% in σ, sign negative),
`MG_ZERO.md` (MG spread = exactly 0, theorem), `POWER.md`/`GAP_STATEMENT.md` (power/no-go).

---

## The problem this lane solves

The MI signal is a **relational** σ-spread: at a fixed radius, different orbital families (eccentricities)
carry different effective inertia → a spread in dispersion beyond the mean. But **velocity anisotropy
β(r) ALSO makes the dispersion depend on orbit family** — that is the killer degeneracy. A naive
"intrinsic σ-scatter at fixed r" estimator cannot tell an MI spread from a wiggle in β(r): both live in
σ_LOS(R) and h4(R) (demonstrated in `observable.py` §[A]: sweeping β tangential→radial moves σ_LOS by
tens of % and flips the sign of h4).

**Task:** design the statistic that ISOLATES MI from β(r) + projection; show which statistic MG cannot
reproduce at ANY β(r); quantify the separation — honestly, including where it fails.

## The design principle — magnitude vs direction

Split each star's velocity at radius r into **magnitude |v|** × **direction**.

- **β(r) = 1 − ⟨v_t²⟩/(2⟨v_r²⟩) is by definition a DIRECTION statement** — the radial/tangential split of
  the velocity ellipsoid. The classic mass-anisotropy degeneracy lives entirely in this **angular** sector.
  In ANY sourced-field theory a tracer obeys |v|² = 2(E − Φ(r)): the **speed magnitude at fixed (r,E) does
  not depend on angular momentum / eccentricity**, for every β.
- **MI lives in the MAGNITUDE sector:** the effective inertia is a functional of the body's own worldline,
  so an eccentric orbit carries a lower effective ν → a lower **speed magnitude**. Crucially MI multiplies
  (v_r, v_t) by the **same** per-orbit factor f(e), so it **cancels in the ratio β** and instead surfaces in
  the enclosed-**mass** normalisation. MI is orthogonal to β by construction.

## What was rejected, and why (honest)

**Rejected — the naive per-star "speed vs eccentricity at fixed r" slope** (`observable.py` §[B]).
Tempting, but CONFOUNDED: in an MG mock it already gives a large slope (**≈ −0.5** across the whole β
sweep), because the distribution function has its own **E–e correlation at fixed r** (radial orbits
reaching r carry a different mean energy). Conditioning on an E-quantile does not remove it (E computed
from v is circular). A per-star speed–eccentricity slope therefore cannot isolate MI. Killed.

## The isolating statistic — orbit-family enclosed-mass consistency

**dlnM ≡ ⟨ ln M(r)|radial-tagged − ln M(r)|circular-tagged ⟩**, where each subpopulation's enclosed mass
is recovered from the spherical Jeans equation using **its own directly-measured** ρ(r), σ_r(r), β(r):

    M(r) = −(r/G) σ_r² ( dlnρ/dlnr + dlnσ_r²/dlnr + 2β ).

The move that beats the degeneracy: **with 3D velocities (Gaia PM + LOS) β(r) is MEASURED, not fit — the
mass-anisotropy degeneracy is BROKEN.** So M(r) can be recovered separately from eccentricity-tagged
subpopulations with **no free β**.

- **MG (theorem):** every orbit family is a WEP geodesic of the SAME field Φ → every family returns the
  **same** M(r). `observable.py` §[C](i): even though the radial-tagged and circular-tagged subsamples
  differ in β by **~7–10**, and across the entire parent-anisotropy sweep, the MG mass split stays in a
  narrow **+0.03…+0.05** band — vs σ_LOS moving tens of %, vs the naive slope's ~0.5. Symbolically
  (§ backbone): d(v²)/dL = 0 (same Φ), and f(e) cancels in β so MI leaves β unchanged and shifts only
  M ∝ f²σ_r².
- **MI:** eccentric tracers run cooler → lower recovered M → **negative** dlnM. §[C](ii): injecting the
  cored Jensen gap and sweeping amplitude gives a monotonic, negative response
  (amp 0→8: +0.045 → −0.072; differential from MG **−0.02 at the fiducial amp=1**, ~−0.015/amp at large
  amplitude). Sign negative = eccentric orbits cooler = the MI fingerprint.

**This — not σ_LOS(R), not raw h4(R), not the per-star speed slope — is the MG-impossible statistic.**

## Anisotropy ↔ MI separation, quantified (both ways)

| statistic | anisotropy nuisance | realistic MI signal | verdict |
|---|---|---|---|
| raw σ_LOS(R) | moves ~tens of % | ~1% | signal buried — **not usable** |
| per-star speed-vs-e slope | MG ≈ −0.5 (confounded) | ~ | **rejected** |
| **mass-consistency dlnM** | compressed to a **~0.02 DF-dependent zero-point** | **~ −0.02 (amp=1)** | **right statistic**, but signal ≈ systematic at 1% |

The mass-consistency statistic compresses the anisotropy nuisance from "tens of %" (σ_LOS) / "fully
confounded" (naive slope) down to a **~0.02 residual DF-dependent estimator zero-point** — a genuine,
large improvement, and β-immune in structure. **But honestly:** at the realistic ~1% MI amplitude the
signal (dlnM ~ −0.02) is **comparable to that residual systematic**. Clean isolation therefore requires
(a) a **forward MG distribution-function model** (Schwarzschild / made-to-measure) to calibrate the
zero-point, and (b) the **deepest-MOND diffuse dSph/UDG** to amplify the ~1% Jensen gap. The statistic is
the correct one; it is not free of a DF systematic at the 1% level.

## Projection and power (consistent with the other lanes)

- **Needs 3D velocities.** Gaia(+HST) proper motions + LOS give (v_r, v_t) per star → β measured
  (degeneracy broken) AND the per-star eccentricity tag (orbit integrated in the fitted Φ). LOS-only
  cannot measure β or tag e per star and falls back to raw h4(R), which is β-degenerate (§[A]). The test
  **requires per-star 3D velocities on a nearby dSph** (Sculptor / Fornax / Draco / UDGs).
- **Underpowered now, different route, same verdict.** The MI amplitude is sub-percent to ~1% (MI_SPREAD),
  so dlnM ~ 0.02 sits at the DF-systematic floor; today's per-star velocity errors (≳10–20%) on a single
  ~10³-star dSph cannot resolve it. **Powered by:** ELT/MICADO per-star velocities (≲5%) on a deep,
  kinematically clean, deep-MOND diffuse dSph WITH Gaia orbit tags, plus a forward MG DF model. This is a
  DIFFERENT route than the cluster-member EFE observable (`POWER.md`) — single dSph, Gaia-3D, stars not
  member galaxies — reaching the SAME "underpowered until ~ELT" conclusion.

## Frozen estimator spec (the β-immune MI mass-consistency discriminator)

- **O1 Sample.** Member stars of ONE nearby, deep-MOND diffuse dSph with LOS velocity + Gaia(+HST) PM →
  full 3D (v_r, v_t) + projected radius. Deepest-y diffuse systems maximise the signal.
- **O2 Model + tags.** Fit an anisotropic-Jeans / Schwarzschild / made-to-measure model (free Φ, free
  β(r)); from Φ assign each star (E,L) → integrate → eccentricity e, pericenter r_p. β measured, not
  marginalised.
- **O3 Statistic.** dlnM = ⟨ ln M(r)|radial-tagged − ln M(r)|circular-tagged ⟩ via Jeans with each
  subsample's own ρ, σ_r, β. MG: 0 (any β, any a₀, both footings). MI: < 0, ~ few×10⁻² (fiducial cored
  ~ −0.02), monotonic in the Jensen amplitude.
- **O4 Anisotropy immunity.** β reweights the angular sector and is measured directly (3D); MI rescales
  (σ_r, σ_t) by the same f(e) → β unchanged, signal only in the mass normalisation (§[C](i); f cancels
  symbolically).
- **O5 Zero-point + confounds.** Calibrate the ~0.02 DF zero-point on forward MG mocks matched to the
  fitted DF. Tidal heating / substructure correlate with r_p and grow toward the core; the MI split grows
  OUTWARD into the low-g zone → use the r_p / radial-trend split (`GAP_STATEMENT.md` E6). PM errors inflate
  e randomly → bias dlnM toward 0 (conservative); forward-model the e-error.
- **O6 Decision.** Support: dlnM significantly NEGATIVE at the cored magnitude WITH the outward radial
  trend. Kill: dlnM significantly POSITIVE (eccentric hotter) → falsifies the Jensen sign. Zero dlnM at
  adequate power kills THIS channel (not the framework).
- **O7 Footings.** Both reported (dσ(e) is <20%-footing-invariant); a₀ value + s=−1 remain postulates;
  MG=0 is the only theorem-grade claim.

## Verdict

- **The isolating statistic exists and is identified:** orbit-family enclosed-mass consistency dlnM, made
  β-immune by measuring β directly from 3D velocities and by MI's f(e) cancelling in β while surfacing in
  the mass normalisation. **MG gives dlnM = 0 for any β(r)** (theorem + numeric across Δβ~8); the naive
  per-star speed slope is **confounded and rejected**; raw σ_LOS/h4 are degenerate.
- **Honest limit:** at the realistic ~1% MI amplitude the signal ≈ the ~0.02 DF-dependent estimator
  zero-point, so isolation needs a forward MG DF model + the deepest-MOND diffuse dSph + ELT-tier per-star
  velocities. **Underpowered now**; a distinct single-dSph / Gaia-3D route to the same conclusion as the
  cluster-member lanes. No "proves" language for the framework value/sign; MG=0 is the sole theorem.
