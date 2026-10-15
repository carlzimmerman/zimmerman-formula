# ARGON06 — The last window, re-audited: why CFG795's P6b couldn't push — and the right closure

**Date:** 2026-10-15. **Home:** `argon_push/ARGON06_last_window_audit_2026-10-15/`.
**Target:** the single conditional window the whole CFG789–795 chain left open — CFG795's P6b
"phase-locked coherent extraction" at the framework-native 2.24 meV (η ≤ 0.6 at ε ≈ 4–6×10⁻⁹).
**Run:** 0 FAIL, exit 0, wall 0.00 s, 13 MB. All external bounds PROVISIONAL (anchored below).
κ = ½ FITTED. Not theory closed.

## Where the track couldn't push

CFG795 (`70b244f65`) closed P6b citing **"the XENON10 bound (κm < 3×10⁻¹² eV ⇒ ε ≤ 1.3×10⁻⁹)."** That
closure is **kinematically wrong**: a 2.24 meV quantum deposits ≤ 2.24 meV — it cannot ionize xenon
(binding ~12.1 eV; XENON10's electron-recoil analysis sits at keV thresholds). The XENON10/SENSEI/SuperCDMS
dark-photon absorption limits live at m ≳ 10 eV (provisional, Caputo et al. handbook figure); `κm < 3e-12 eV`
is a re-scaled curve used outside its validity range. The verdict class (window closed) was right; the
obstruction was not derivable from the record's own bounds at the native mass.

## The right closure: cosmology, not detectors

At m = 2.24 meV the operative bound is the **CMB spectral-distortion bound** — resonant γ→X conversion
during the μ/y eras. Provisional anchor: ε ≲ 10⁻¹³ at m ~ 10⁻³ eV (Caputo et al. 2021 handbook curve),
and the reanalysis of Cyr, Chluba et al. (MNRAS 535, 1874, 2024) states that the constraints in exactly the
window 10⁻⁴–10⁻³ eV — the native mass's window — **were previously underestimated**, i.e. are even stronger.

- The window needs ε ∈ [3.97e-9, 6.25e-9] (floor = 1/√N_cell for any conversion at all; η = 0.6 at the top).
- The CMB bound ε_CMB ≈ 1e-13 excludes this by **4.6 orders**.
- Robustness (named kill condition): the closure survives even a 100× weakening of the provisional CMB
  value (ε_CMB = 1e-11 still excludes by 2.6 orders); reopening would require ε_CMB > 3.9e-11 — i.e. the
  standard cosmology bound would have to be wrong by nearly three orders at the native mass.
- At every cosmology-allowed ε the phase is unmeasurable (ε√N ≤ 2.5e-5 ≪ 1): the phase-locked channel
  gives **η = 0 exactly** — the 0.6 formula never operates, so no dish gain can resurrect the window.

## The single obstruction across the entire design space

> **The only ε that converts anything is excluded by cosmology; the only ε cosmology allows converts
> nothing.** (Stellar bounds + CMB spectral distortions at the framework-native mass.)

This is the end of the line for the ramjet/harvest programme as derivable physics: every conversion
channel now closes on data (stellar, CMB, natural-matter, detector) — the framework itself contributes the
exact rest-mass conservation theorem and the (d/L*)² stiffness screening. A working converter requires a
term outside the committed action that breaks cold-mass continuity (∂ₜρ_c + ∇·j = −Γ) **and** a coupling
that sits at currently-excluded strength: a theory-level obstruction, not an engineering one.

## The E6 kill test sharpens

CFG795 said "a sub-mm search at ε ≳ 1e-10 decides." Correction: ε = 1e-10 is already excluded by cosmology
for a standard portal, so the deciding search must sit at **ε ~ 1e-13** (CMB-consistent) — where the
ARGON03 rate is still **4.4×10⁵ photons/day per 10 m² at 0.55 mm / 542 GHz**. A null at that sensitivity
closes the chain definitively; a line kills the framework (CFG723 E6). The search band is therefore both
allowed and decisive — the framework's own native scale puts the experiment on the table at exactly the
coupling where it matters.

## Honest scope
- ε_CMB = 1e-13 is provisional (handbook curve at ~1e-3 eV; the 2024 MNRAS reanalysis direction strengthens
  it). The closure's robustness margin (2.6 orders under a 100× weakening) is the hedge against this.
- XENON10 inapplicability is kinematic and robust; the "limit curves start ≳ 10 eV" statement is provisional.
- The haloscope rate assumes the CFG790 ε²ρcA absorption bookkeeping (reproduced in ARGON03/04).
- No new physics asserted; κ = ½ stays FITTED.

## Verdict
**PASS — the last window closes on the correct bound. CFG795's XENON10 mechanism is replaced by the CMB
spectral-distortion bound at the native mass (4.6 orders, robust to 100× weakening); at any allowed
coupling the phase-locked channel is exactly zero; the deciding experiment sharpens to a 542 GHz search at
ε ~ 1e-13. The design space is closed end-to-end with one clean obstruction, and the framework's kill test
has a sharper, still-viable target.**