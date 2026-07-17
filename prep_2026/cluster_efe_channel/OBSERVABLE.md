# OBSERVABLE-DESIGN LANE — isolating the MI infall-phase σ-spread from the shared radial EFE gradient

**Date:** 2026-07-17 · **Script:** `observable.py` (this dir, exit 0, numpy/scipy/sympy, both footings) · log `observable.out`.
**Framework:** de Sitter–Unruh MODIFIED INERTIA (Zimmerman) — NOT standard MOND.
g_obs = ν(y)·g_bar, ν(y)=√(1+1/y), y = g_bar/a₀, a₀ = cH_Λ/Z, Z = √(32π/3). MI = inertia is a
time-nonlocal functional of the member's own worldline via K(□_u); the subsystem EFE loads the boost
by a_ext·θ(y), y = ω_ex/ω_in (Milgrom 2022, PRD 106 064060). Milgrom 1983/1999 (PLA 253:273) wellhead
credit; distinctive content = the **cH_Λ/Z coefficient** + the MI completion. **a₀'s value and s = −1
remain postulates. MG = 0 (at fixed true g_ext) is the sole theorem-grade claim.**

Companion lanes this builds on (does not reinvent): `PREDICT.md`/`predict.py` (the MI prediction),
`MG_EFE_ZERO.md`/`mg_efe_zero.py` (MG=0 theorem + the projection/interloper mimics),
`sigma_spread/GAP_STATEMENT.md` (frozen estimator E1–E7), `reviews/residual_doors_2026_07/D3_*` (the
dated sign-flip pre-registration, DOI 10.5281/zenodo.21179352).

---

## The problem this lane solves — THE KEY DEGENERACY

Both MI and MG have an External Field Effect that loads the member's internal boost with the **current**
g_ext. So in **both** theories `(σ_int/σ_bary)` varies with cluster-centric radius — the shared **radial
EFE gradient**. That radial trend is NOT the MI signal; it is the killer common mode. The distinctive
MI signal is the **residual spread at FIXED cluster-centric radius (fixed current g_ext), correlated
with infall phase (history)** — MG predicts exactly zero infall-phase correlation at fixed radius.

**The design principle (`observable.py` §[A]).** Project `(σ_int/σ_bary)` onto the **(radius × phase)**
plane. The shared radial gradient is a common mode on the radius axis — it carries **no phase label**.
Difference **along the phase axis within a fixed-radius bin**: the radial gradient cancels identically,
MG's residual is exactly 0 at fixed true radius (theorem), and only the MI history signal (and a
controllable projection alias) survives.

## The isolating statistic — Rhee+2017 phase-space zone contrast at fixed radius

Within one deprojected external-field bin (a_ext from the caustic mass profile, width ≤ 0.3 dex):

    D(zone) ≡ ⟨ ln[ σ_int / σ_bary ] ⟩_zone  −  ⟨ same ⟩_ancient

with the **infall-phase proxy = Rhee+2017 (ApJ 843:128) projected-phase-space zone** (ancient-infall /
first-infall / recent-infall / backsplash) from `(R_proj/r200, |v_los−v_cl|/σ_cl)`, and σ_bary from the
β-immune Wolf half-mass. **MG: D(zone) = 0 for every zone at fixed true radius** (symbolic d/dy = 0,
§[C]). **MI: the memory-weighted sign-flipping pattern** (§[B], both footings, fiducial θ₀=2):

| Rhee zone | y_eff | D (θ₀=√2) | D (θ₀=2) | D (θ₀=e) |
|---|---|---|---|---|
| ancient-infall (settled, reference) | 0.55 | 0.0% | 0.0% | 0.0% |
| **first-infall (pre-peri, cold past)** | 0.46 | **−1.6%** | **−3.0%** | **−3.3%** |
| **recent-infall (post-peri, hot past)** | 0.90 | **+1.2%** | **+2.2%** | **+2.3%** |
| backsplash (out again, decaying) | 0.33 | +0.1% | +0.1% | +0.2% |

The **sign-flip** (pre-peri DEFICIT → post-peri EXCESS across pericentre) is the primary MG-impossible
statistic. The phase-contrast `|D(recent) − D(first)|` at these conservative memory weights is ~5%; the
full max-min infall-window envelope is the banked 6–13% (`predict.py`), deepest plungers (D3 Crater II)
reach +13…26%. **Footing-invariant** (identical to printed precision — a₀ cancels at fixed dimensionless
depth). **Kernel-hostage** in amplitude.

## What MG cannot reproduce (`observable.py` §[C])

- **Theorem:** `d(σ_MG)/d(infall-phase y) = 0` identically (sympy, any a₀, any interpolation). At fixed
  TRUE radius, MG's zone-contrast is exactly zero — the sourced field carries no worldline/history label.
- **The one MG evasion is PROJECTION**, and it is controllable. At fixed *projected* radius, radial
  plungers sit at a different true r → MG's real radial trend aliases into the phase axis. The compact MC
  reproduces the alias (~1–2%; banked authoritative 2.25%/2.35%) and shows it is **killed to ~0.01% by
  binning on TRUE r**. The **Rhee zones ARE the orbit-class-aware deprojection** (calibrated on N-body
  *orbital history*, not a scalar radial mean) — exactly the class-aware correction `MG_EFE_ZERO.md`
  proved a class-BLIND scalar deprojection cannot supply. Plus the mandatory DS cut + caustic membership
  (GAP E5) for interlopers.

## Velocity-anisotropy control (`observable.py` §[D])

The member's OWN internal anisotropy β enters σ_los, and infall can induce radial β (tidal) → a
potential phase alias. **Control: normalise by the Wolf+2010 half-light mass** `M(r_½)=3⟨σ_los²⟩r_½/G`,
which is β-immune to first order. The residual Wolf β-leak is ≤ ~1.8% and **monotone in β** — it cannot
produce the pre-peri deficit or the sign-flip, and folds into the same-signed heating-only confound
family. With IFU 3D internal kinematics β is measured directly and the leak is calibrated.

## Beating the same-signed confounds — the 4-part FINGERPRINT (`observable.py` §[E])

Tidal heating/stripping, ram-pressure and environmental quenching all change σ_int, correlate with
infall phase, and carry the **same sign** as the baseline MI excess. They are beaten not by the
phase-difference alone but by a **joint 4-part fingerprint that only MI trips**:

| source | F1 phase-contrast @ fixed true r | F2 sign-flip (pre-peri deficit) | F3 rises outward | F4 baryon-blind |
|---|---|---|---|---|
| **MI (this framework, MI-class)** | ✔ | ✔ | ✔ | ✔ |
| MG (QUMOND/AeST, true r) | ✗ (=0) | ✗ | ✗ | ✔ |
| MG projection alias | ✔ | ✗ | ✗ | ✔ → killed by zone deprojection |
| interlopers (uncut) | ✔ | ✗ | ✗ | ✔ → killed by DS + caustic |
| tidal heating/stripping | ✔ | ✗ | ✗ (inward) | ✗ (tidal features/truncation) |
| ram-pressure | ✔ | ✗ | ✗ | ✗ (gas stripping) |
| environmental quenching | ✔ | ✗ | ✗ | ✗ (SF-history mark) |
| member-internal anisotropy | ✔ | ✗ | ✗ | ✔ → Wolf-immune, monotone |

- **F3 radial-profile separator:** MI rises OUTWARD, peaks at the MOND-transition shell a_ex ~ 0.3–1 a₀
  (~R500–R200), dies in the core; **tidal heating rises INWARD** (peaks at small pericentre) — opposite
  slope (GAP E6). Verified numerically.
- **F2 sign-flip:** tides/ram/quench can only HEAT (monotone, one sign); MI has a pre-peri **deficit**.
- **F4 baryon-blind split:** environmental confounds **leave marks on the baryons** (gas stripping,
  truncated/burst SF, tidal morphology); the MI inertia signal does not. At matched (zone, a_ext), split
  by a baryon proxy (gas fraction / SF-history / morphology); the fit's **baryon-independent intercept**
  recovers the MI signal, the proxy-correlated slope absorbs the environmental confound (toy recovers the
  −3.0% MI deficit as the intercept). This is the environmental-vs-inertial separator.

**Only MI trips F1 ∧ F2 ∧ F3 ∧ F4.** MG/alias/interloper/anisotropy fail F2 & F3; tidal/ram/quench fail
F3 (wrong radial slope) AND F4 (they mark the baryons). The joint 4-part signature is the MG-impossible
**and** confound-impossible discriminant.

## Frozen observable spec (O1–O8, see `observable.py` §[F])

O1 diffuse/LSB deep-MOND carriers (dE/L* are adiabatic-dead → the power wall). O2 deprojected a_ext bins
≤0.3 dex (radial common mode cancels). O3 Rhee PPS zone tag (= the orbit-class-aware deprojection).
O4 D(zone) via Wolf β-immune σ_bary; sign statistic + phase-contrast (MG = 0). O5 Wolf anisotropy
immunity. O6 confound controls = radial profile (F3) + sign-flip (F2) + baryon-blind split (F4) + DS/
caustic cut. O7 SUPPORT = sign-flip + outward profile + baryon-blind intercept; KILL = positive pre-peri
sign; zero at power kills THIS channel (not the framework). O8 both footings; a₀-independent phase-contrast.

## Verdict + honest scope

The isolating statistic **exists and is identified:** the fixed-radius, Rhee-zone phase-contrast
`D(zone)`, which differences out the shared radial EFE gradient (the key degeneracy), is made MG-zero by
the d/dy=0 theorem, made projection-safe by orbit-class-aware zone deprojection, made anisotropy-immune by
the Wolf normalisation, and made confound-safe by the joint 4-part fingerprint (only MI trips all four).

**Honest scope (non-negotiable):** MI-**class**-generic — an **MI-vs-MG** test (MG = 0 at fixed true
field), **NOT** this-framework vs Milgrom's linear no-EFE MI (arXiv:2503.07106, which also produces a
spread). The 6–13% magnitude is **kernel-hostage** (θ(y) not derived; existence + sign + sign-flip + MG=0
are the theorem-grade claims). **a₀'s value and s = −1 are postulates.** MG=0 is a theorem only at fixed
true g_ext; in projection it is a mitigation-dependent baseline. **Underpowered today** — needs ELT-tier
(≤10%) σ on phase-tagged diffuse carriers (banked GAP_STATEMENT: earliest confirmatory window ~2032–2034).
No "proves" language for the framework.

## Credit

Milgrom 1983 (MOND) / 1999 PLA 253:273 (ν-kernel wellhead) / 2022 PRD 106 064060 (MOND as modified
inertia; two-frequency EFE, subsystem boost) / 2025 arXiv:2503.07106 (linear MI spread → MI-class-generic).
Phase-space membership / infall-phase: **Rhee+2017 (ApJ 843:128, PPS zones)**, Oman+2013, HeCS caustic
membership, Dressler–Shectman substructure test, Wolf+2010 (β-immune half-mass), SDSS/MaNGA dispersions.
