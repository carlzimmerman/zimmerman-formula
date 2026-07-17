# VERIFY — relational σ-spread discriminator, adversarial both-ways audit (2026-07-17)

Re-ran all four lane scripts (`mi_spread.py`, `mg_zero.py`, `observable.py`, `power.py`) —
**all exit 0**. Confirmed the load-bearing cross-checks (`prep_2026/mi_integrator/`,
equation-book `E-S3.5`/`E-S2-5`) exist and carry the quoted numbers. Then ran an
independent adversarial probe (`scratchpad/probe.py`, `fair.py`) targeting the two killer
questions. Verdict below is **UPHELD with two sharpened demotions**; no lane number was
manufactured in either direction.

---

## 1. Is MG *really* exactly 0? Can baryonic / anisotropy / substructure mimic the spread?

**Field channel — exactly 0, theorem intact.** Every theory that (P1) sources a field g(x)
and (P2) moves tracers as WEP geodesics gives every star the same g(r): orbit/velocity/history
label the tracer and appear nowhere in g. `d(v²)/dL = 0` symbolically; numeric ptp = 0 across
{canonical, alt} × {framework ν, MOND ν, exp-RAR}. **Confirmed.**

**Fair anisotropy test (the decisive new check).** I built a *proper steady-state* DF with
strongly radially-varying anisotropy (β running +0.13 → −0.72 outward, anisotropy a function of
apocenter = a function of integrals), **no MI**, and recovered the orbit-family mass split:

    STEADY-STATE radially-varying β, NO MI:  dlnM(MG) = +0.033   (Δβ~9 between subsamples)

This sits **squarely in the MG zero-point band (+0.03…+0.05)** and does **not** reach the
MI-signed signal. So *valid equilibrium anisotropy — even strong, radially varying — cannot
fake the MI signature.* The discriminant is **genuinely not re-labeled anisotropy** (see §2).

**Shared / baryonic channels that ARE nonzero (the honest confounds):**
- **Tidal heating (C6):** ~2–8%, present in MG *and* Newton+DM, **same sign** as MI, separable
  only by radial profile + r_p-correlation (grows to core; MI peaks outward). Already banked.
- **Non-equilibrium / substructure (NEW, potent):** probe 2 — a radius-correlated,
  *non-steady-state* mix of orbit populations (mimicking unrelaxed substructure or a
  radius-sorting tag) drives **dlnM = −0.71**, i.e. a large **MI-signed false signal ~35× the
  real MI amplitude**. This is a genuine false-detection route the observable lane under-guards.
- **Binaries / rotation:** unresolved binaries inflate σ (confound only if binary fraction
  correlates with the orbit tag); mild dSph rotation is an ordered-velocity term, separable.

→ **MG *field* spread = 0 (airtight); the *observable* carries same-signed non-field confounds.**
The literal "MG = 0" is the field channel, not the total observable — as `mg_zero.py` C6 states,
now reinforced: substructure/non-equilibrium is the dominant practical mimic, not tidal heating.

## 2. THE KILLER — is the discriminant anisotropy-immune, or re-labeled anisotropy?

**Answer: genuinely immune for equilibrium DFs; NOT re-labeled anisotropy — but immunity is
conditional and the residual systematic is signal-sized.**

- Raw σ_LOS(R)/h4(R): fully β-degenerate (anisotropy moves σ_LOS tens of %, flips h4 sign). Dead.
- Naive per-star speed-vs-e slope: MG already gives ≈ −0.5 (DF's intrinsic E–e correlation).
  Correctly **rejected**.
- The `dlnM` mass-consistency statistic **survives the fair test** (§1): equilibrium β variation
  → dlnM stays at the +0.033 zero-point, does not reach the MI signal. Real immunity, not a label.

**Two honest demotions of the "β-immune" headline:**
1. The MG zero-point is **DF-shape-dependent at signal size**: probe 1 spans **+0.009 → +0.062**
   across global anisotropy (wider than the lane's quoted +0.03…+0.05); probe 3 spans +0.043 →
   +0.051 across density slope. The realistic MI amp=1 differential is only **−0.022**. So the
   zero-point drift (~0.02–0.05) is **comparable to the signal** — calibration needs a full
   forward DF (Schwarzschild / M2M) model, and the post-calibration residual is *not* shown to be
   sub-signal.
2. Immunity **requires** (a) full 3D velocities (β measured, not fit), (b) equilibrium, (c) good
   per-star eccentricity tags. Break any one (non-equilibrium, substructure, tag that sorts by
   radius) and dlnM swings ≫ signal (probe 2). `observable.py`'s "β-immune in structure" is
   defensible; its own caveat ("not free of a DF systematic at 1%") is the accurate statement,
   and should read **"β-immune for equilibrium DFs only."**

## 3. Is the MI magnitude honestly re-derived (not inflated)?

**Yes — and it is conservative, not inflated.**
- `tau_mem = 2c/a0 = 2Z/H_Λ = 203 Gyr (canonical) / 168 Gyr (alt)`, exact and footing-free,
  banked as equation-book **E-S3.5 / E-S2-5** (verified: tau_mem·H_Λ = 2Z = 11.5776 exactly).
- Every pressure-supported system is **deep adiabatic**: tau_mem/T_orb = 22× (Coma) to 1367×
  (Draco). The memory freezes at the orbit mean → **no resonant amplification**. Robust.
- Independent real-kernel cross-check (`mi_integrator`, 19/19): eccentric-orbit RAR offset
  **−0.0007 dex at e~0.24**, i.e. **~3× smaller** than `mi_spread.py`'s cored instantaneous
  estimate (−0.002 dex) — the honest magnitude is if anything *below* the lane's fiducial.
- Fiducial RMS **0.2–0.35% in σ**, ~1% peak/point-mass ceiling, <0.1% strongly cored.
  **An order of magnitude below the banked 6–13%**, which is correctly re-identified as a
  *different* observable (Milgrom-2022 two-frequency EFE subsystem-boost, kernel-hostage θ(y)).
  Correction is in the honest direction.

## 4. Footing / interpolation dependence

At **fixed depth y, a0 cancels** — `mi_spread.out` shows byte-identical dσ(e) tables for both
footings. Footing enters only through tau_mem/system (both deep adiabatic regardless), shifting
the number <20% and N_3σ <44% — **not footing-hostage**. Interpolation: the gap is set by ν's
convexity; framework ν and standard-MOND ν have comparable deep-MOND curvature → same order (not
separately swept, but the a0-cancellation is solid). OK.

## 5. Manufactured detection AND manufactured null

- **False-detection guards present:** EFE-trap (constant boost is MG-degenerate; only y-dependence
  is MI) + rejection of the naive per-star slope. **Gap found:** probe 2's non-equilibrium
  −0.71 is an un-guarded MI-signed false detection — flagged here as the primary systematic.
- **No manufactured null:** power null calibrated (f=0 → z = +0.000 ± 1.006, 20k trials); the
  sign/kill-switch (O6: positive dlnM falsifies the Jensen sign) is symmetric. Clean.

## 6. Does the claimed powered dataset exist? NO — no-go confirmed.

Fisher floor MC-validated (analytic z vs score-MC agree <2%; √N scaling 1.99). Real dSph catalog
sizes correct (Fornax 2600, Sculptor 1500, Draco 700). Two independent walls, either fatal:
- **Count:** need N ~ 7e4 (1% ceiling) to ~6e5 (0.2% fiducial) clean per-star velocities in one
  deep-MOND system; deepest-y systems (Crater II/Antlia II) have the *fewest* stars (150–200).
- **Orbit tag (binding):** Gaia per-star internal PM S/N ≈ 0.03–0.05 → bulk systemic PM only,
  D_Gaia≈0; only HST/JWST 3D reaches D~0.3–0.4 for ~300–500 stars in 2–3 systems. Best real
  single-system **z ≈ 0.05**. No existing dataset (Walker+2009, Gaia DR3, MaNGA/ATLAS3D, Coma)
  comes within 1–6 orders. Powered only by ELT/MICADO (<5% per-star) + space-astrometry 3D tags
  beyond Gaia. **Honest no-go.**

---

## VERDICT

**UPHELD, with a sharper systematics caveat — standing unchanged.**

The MG-field-channel exact-0 is an airtight theorem, and it **survives the killer test**: valid
equilibrium anisotropy (even strong, radially varying) cannot reproduce the orbit-family mass
split, so the MI spread is **genuinely not re-labeled anisotropy**. The MI magnitude is honestly
and *conservatively* re-derived — sub-percent to ~1% in σ (real-kernel integrator even smaller),
an order below the banked 6–13% (a different EFE observable, correctly demoted), tau_mem exact
and footing-free, all deep-adiabatic. Footing-robust (<20%).

Two demotions beyond the lanes' own text, both toward *more* caution:
1. The `dlnM` estimator's zero-point is **DF-shape-dependent at ~0.02–0.05 = signal size**
   (probe 1/3), and **catastrophically fragile to non-equilibrium / substructure**
   (probe 2: MI-signed −0.71, a false-detection route not guarded). "β-immune" holds only for
   equilibrium DFs with 3D data and clean tags; the post-DF-model residual is unproven sub-signal.
2. The practical systematic floor is set by equilibrium + tagging fidelity, **not** the optimistic
   ~0.02 estimator zero-point.

Net: the cleanest MG-*impossible* discriminant in principle, with a genuinely exact field-sector
baseline that resists equilibrium anisotropy — but demoted in practice by (a) a same-signed
substructure/non-equilibrium confound that can *manufacture* the MI sign, and (b) statistical
power (needs N~1e5–1e6 clean per-star velocities **plus** a 3D orbit tag Gaia cannot deliver).
**Real, not currently powerable, not powerable near-term.** a0's value and s=−1 remain postulates;
MG-field = 0 is the sole theorem-grade claim. No "proves" language used for the framework.
