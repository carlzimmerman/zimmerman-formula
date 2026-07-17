# SYNTHESIS — cluster-member infall-phase EFE σ-spread

`prep_2026/cluster_efe_channel/` · 2026-07-17 · de Sitter–Unruh MODIFIED-INERTIA framework
(a₀ = cH_Λ/Z = 9.36e-11 canonical) · both footings shown (canonical / alt 1.13e-10) ·
**MI-CLASS-GENERIC (MI-vs-MG), NOT this-framework-vs-Milgrom** · amplitude KERNEL-HOSTAGE ·
a₀ value + s = −1 are POSTULATES · **no "proves" for the framework.**

Five scripts, all exit 0: `predict.py` · `mg_efe_zero.py` · `observable.py` · `power.py` · `verify.py`.
This synthesis applies the VERIFY-lane corrections (three banked claims softened, both ways).

---

## 1. Headline

A cluster galaxy's internal boost depends on its **infall history** under modified inertia (the
non-local kernel K(□_u) makes inertia acceleration-history-dependent) but **only on its current
position** under modified gravity (QUMOND/AeST EFE is instantaneous). So at **fixed current external
field**, MI predicts a relational **spread** in (σ_int / σ_baryon) across members of different infall
phase; **MG predicts exactly zero.** This is a real MG-impossible discriminator **in principle** — but
its 2026 realization is **UNDERPOWERED, MITIGATION-DEPENDENT, and sign-postulate-contingent.** The one
theorem-grade claim is MG = 0 at fixed *true* 3D field; the magnitude (6–13% fiducial) is kernel-hostage
and the *sign* is not theorem-grade.

---

## 2. Outcome

### Powerable NOW / with reanalysis / needs-X? → **NEEDS-X for a clean detection.**
No existing 2026 dataset delivers a clean, mitigation-free bite.
- **SDSS stacked (N ~1e5, redMaPPer/Yang × single-fiber):** statistically over-powered (z ~8/10) BUT
  **systematics-limited, not statistics-limited** — the ~1% ln-σ slope sits under a 1–5% single-fiber
  σ-systematic floor + a 2–8% same-signed tidal/environmental (C6) confound, and single-fiber σ is
  reliable only for σ ≳ 90–100 km/s (Sohn+2017, Zahid+2016), which **excludes the diffuse deep-MOND
  carriers (σ 15–50) that carry the signal.** More galaxies cannot buy the missing systematic control.
- **Single rich cluster (Coma ~1000+):** statistics-limited, z ~2.0–2.5.
- **NEAREST BITE NOW = MaNGA/SAMI IFU diffuse-dE reanalysis** at HeCS/GalWCat19/Rhee-2017 phase tags
  (resolved σ down to ~20 km/s, signal ~4% clears the ~0.3–1% IFU σ floor): **EXPLORATORY ~2–3σ hint
  only** at a defensible N ~300–500 tagged diffuse members (SAMI 8 clusters, Owers+2017 — the banked
  N ~800–1000 is optimistic). Firewalled: cannot confirm or kill.
- **Clean detection X =** ELT-HARMONI diffuse-UDG carrier σ (~2032) OR a dedicated wide nearby-cluster
  IFU dwarf survey (~1e3–1e4 diffuse members, resolved σ, sub-percent systematics). **The binding
  resource is systematic σ control, which a stacked SDSS N cannot buy.**

### Sharpened prediction (magnitude + sign)
- **Magnitude:** fiducial band **6–13%** for a diffuse deep-MOND member (a_in ~0.3 a₀, a_ex ~a₀ at the
  transition shell): θ(0)=√2 floor 5.5%, θ(0)=2 rational fiducial 9.5%, θ(0)=e ceiling 11.5% (y ≤ 1.5).
  Honest model-independent cone ~4–15% (kernel-hostage: θ(y) is NOT derived by the dS-Unruh foundation
  — only the cone endpoints are fixed). **Existence + MG = 0 are theorem-grade; the amplitude is a band.**
- **Radial structure:** the spread **RISES OUTWARD**, peaks at the MOND-transition shell a_ex ~0.3–1 a₀
  (~R500–R200), **dies toward the core** — the *opposite* radial slope to tidal heating (the primary
  confound separator).
- **Sign — DE-RATED to postulate+kernel-contingent (VERIFY V3):** the memory kernel gives felt
  y_eff = y_cur + (y_hist − y_cur)·exp(−t/τ_M), τ_M ~0.45 Gyr. The *memory branch* → first-infall
  pre-pericentre members run a DEFICIT (−3%, memory of the cold isolated past), post-pericentre/
  backsplash run an EXCESS (+3%), sign flips across pericentre. **BUT** raw adiabatic loading gives
  the OPPOSITE sign (+6.7%, plungers hotter). The observed sign is the *competition* set by τ_M and
  y_hist: **if memory is weak (t ≫ τ_M) the sign is POSITIVE and would self-trip GAP_STATEMENT E7's own
  KILL condition.** GAP E4/E7 (negative) and predict.py §2 (positive) are internally inconsistent for
  the mixed "infalling" class. **Only MG = 0 is theorem-grade; the sign and sign-flip ride on s = −1 +
  τ_M.** Pre-registration MUST pin the sign statistic to a SINGLE phase zone (first-infall pre-peri
  only) before firing, or it risks killing itself.

### The observable that beats the EFE-gradient + confounds
**D(zone) = ⟨ln[σ_int/σ_bary]⟩_zone − ⟨…⟩_ancient**, computed WITHIN a fixed deprojected external-field
bin (a_ext from the caustic mass profile, ≤ 0.3 dex), tagged by Rhee+2017 (ApJ 843:128) projected-
phase-space zones (ancient / first-infall / recent-infall / backsplash), σ_bary from the β-immune
Wolf+2010 half-mass. Difference *along the phase axis at fixed radius*:
- **Beats the shared radial EFE gradient (the key degeneracy):** at fixed TRUE radius MG's phase-
  contrast is EXACTLY 0 (sympy d(σ_MG)/dy = 0, any a₀/interpolation). The gradient is a common mode on
  the radius axis with no phase label → cancels.
- **Beats anisotropy:** Wolf β-immune normalisation; residual β-leak ≤ ~1.8%, monotone, no sign-flip.
- **Beats same-signed tidal/ram/quench:** joint fingerprint — F1 nonzero fixed-r contrast, F2 sign-flip
  (tides only heat), F3 outward-rising profile (tides rise inward), F4 baryon-blind. **CAVEAT (VERIFY
  V4):** F3 (radial slope) is the robust separator; **F4 degrades for a dry tidal-heating episode on
  gas-poor dE** (heats σ with only subtle morphology) — treat F4 as corroborating, not decisive. The
  baryon-split toy recovers the MI intercept *by construction*, showing separation is POSSIBLE if the
  confound is linear-in-proxy, not that real confounds obey that.

### Both footings
**Identical at fixed dimensionless depth** — a₀ cancels in the spread (~0% relative shift), so the
channel is **NOT footing-hostage.** Footing only shifts which physical member/radius maps to a given
depth (~9% shell-radius shift; carrier-shell R = √(GM/a₀) = 0.39 Mpc at 1e14, 1.22 Mpc at 1e15 M⊙).
Alt footing needs ~×0.8 the N. MG mimic and MI band scale together (~20%).

### Best cluster/sample + S/N
- **Clean:** ELT-HARMONI UDG carriers (~2032) or dedicated wide nearby-cluster IFU dwarf survey → the
  only route to > 5σ with sub-percent σ systematics.
- **Nearest exploratory (2026):** MaNGA/SAMI diffuse-dE at Rhee-2017 tags, N ~300–500 → **z ~2–3, hint-
  grade, firewalled.**
- **NOT usable:** SDSS single-fiber stack (systematics-limited; excludes the σ 15–50 carriers).

---

## 3. Thesis statement

**Post-lensing-no-go, this is the program's most distinctive *in-principle* front — but it is NOT a
confrontable one today, and its single theorem-grade claim is narrow.** The channel is genuinely
MG-impossible at its core: at fixed *true* 3D external field MG = 0 is an airtight theorem (memoryless,
survives a time-varying potential and retardation, any a₀, both footings), and the fixed-radius Rhee-
zone phase-contrast correctly differences out the shared radial EFE gradient. That is the real,
distinctive, MI-vs-MG discriminant the program has been missing. **But the honest standing is three
notches softer than the banked headline:** (1) MG's *observational* floor is ~1–2%, NOT ~0.01% — the
projection alias is killed only PARTIALLY by observable (statistical, purity-p) deprojection, and
unmodeled filamentary/triaxial infall can push the raw mimic to ~7% (band-sized); the mitigation chain
(class-aware caustic deprojection + DS cut + caustic membership + relaxed-cluster selection) is
LOAD-BEARING, not optional. (2) The *sign* is not theorem-grade and is internally inconsistent across
the banked docs; it rides on s = −1 + τ_M. (3) No clean 2026 dataset bites. **Scope, stated plainly:
this is MI-CLASS-GENERIC (MI-vs-MG; Milgrom's linear no-EFE MI, arXiv:2503.07106, also spreads) — it is
NOT this-framework-vs-Milgrom, and it does NOT test a₀'s value or s = −1.** So: the best *distinctive*
front the program has, worth pre-registering and reanalysing at MaNGA/SAMI for a hint — but the honest
verdict is **prediction, not confrontation**; it neither manufactures a win nor a deficit.

---

## 4. Next
1. **Fire the MaNGA/SAMI exploratory reanalysis** (nearest bite): pull SAMI/MaNGA cluster diffuse-dE
   with resolved σ 20–50 km/s, cross-match Rhee-2017/HeCS/GalWCat19 phase tags, run D(zone) at fixed
   caustic-a_ext bins. Pre-register **the sign statistic on first-infall pre-pericentre ONLY** (VERIFY
   V3) to avoid self-tripping the kill switch; report as firewalled ~2–3σ hint.
2. **Quantify the filamentary/triaxial projection mimic** (VERIFY V2 gap): replace the isotropic MC
   with a triaxial potential + infall-axis model to pin whether the raw alias is 2% or 7%, and
   propagate the orientation error in the spherical caustic a_ext(R).
3. **Reconcile the sign inconsistency** GAP E4/E7 (negative) vs predict.py §2 (positive): compute the
   raw-loading-vs-memory competition as a function of τ_M and y_hist to bound the population sign.
4. **Do NOT push SDSS N harder** — it is systematics-limited and excludes the carriers; buying N does
   not buy the σ control. Route the effort to IFU + (long-horizon) ELT-HARMONI instead.
