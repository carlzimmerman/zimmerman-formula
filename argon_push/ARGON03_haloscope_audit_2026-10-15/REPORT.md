# ARGON03 — Haloscope re-audit (CFG790): the optical claim dies, the framework-native sub-mm search opens

**Date:** 2026-10-15. **Home:** `argon_push/ARGON03_haloscope_audit_2026-10-15/`.
**Pre-registration:** `FROZEN_CRITERIA.md` (committed alone, `144250cd6`, before any script).
**Run:** `OMP_NUM_THREADS=1 timeout 100 python3 haloscope_audit.py` → 0 FAIL, exit 0, wall 0.02 s, 13.9 MB.
Canonical footing a₀ = 9.3603e-11 only. κ = ½ FITTED. All external coupling bounds PROVISIONAL
(anchors: An et al. 2013, arXiv:1302.3884 — solar κ·(m/eV) < 1.4e-11 for m_V < 0.1 eV; Caputo, Millar,
O'Hare, Sanfilippo 2021, PRD 104 095029 — stellar-cooling band ~3e-15–1e-14 at 0.1–10 eV for the
Stückelberg case). CMB-era bounds not re-audited (out of scope, marked provisional).

## What the audit found (CFG790, commit 7ababab3e)

**1. The arithmetic is sound.** Independently reproduced P = 1.83e-19 W and 9.8e4 photons/day at
(ε = 1e-12, m = 1 eV, 0.38 GeV/cm³, 10 m²) to 1.4% — the residual is solely CFG790's 4-sig-fig constants.
HARVEST CLOSED stands (1.8e-19 W is 5.5e18 short of 1 W). No evidence error in the bookkeeping.

**2. The DETECTABLE claim at its headline parameters is dead (provisional).** ε = 1e-12 at m = 2–3 eV is
**excluded ~100×** by the stellar-cooling band (Sun/HB/RG; Caputo et al. 2021). CFG790's own ε = 1e-14 line
(1–10 photons/day) survives at the band edge (Stückelberg case), i.e. a tabletop search is still open but
~100× slower than the headline claim, and it is excluded entirely for a Higgs-mass dark photon (χ ~ 1e-13
plateau, m ≲ 100 eV). The README's flag "coupling bounds quoted from memory" was the right flag — this is
the correction.

**3. The 2–3 eV "visible line" mass is a knob, not a prediction (G6).** No dimensionally consistent
combination of (a₀, G, c, ħ, ρ_DE) reproduces 2.5 eV (grid scan over all integer exponents, no candidate
within 5%). The framework's only vacuum-induced quantum mass (CFG723 D5 route) is

  m_native = (ρ_DE ħ³/c³)^{1/4},  ρ_DE = 4a₀²/(Gc²)  ⇒  **2.24 meV, λ = 0.553 mm, ν = 542 GHz**

— sub-millimetre, NOT optical. The "line colour" statement (620 nm / 413 nm) rests on an assumed mass.

**4. The positive flip: the haloscope survives only at the framework-native frequency — and becomes a
pre-registered kill test of the framework.** Absorption power is mass-independent (P = ε²ρcA), so the
photon rate scales ∝ 1/m: at (ε = 1e-12, m_native) the rate is **4.4e7 photons/day per 10 m² at 0.55 mm**,
and ε = 1e-12 is **allowed** there with a 6.2e3 margin against the anchored solar relation
(ε_max(m_native) = 6.3e-9). The honest background: CMB broadband over 10 m² ≈ 1e-12 W; in-band at R ~ 1e3
≈ 1e-15 W, ~5e3 above the 1.8e-19 W signal — a real search needs R ≳ 1e4 and/or cryogenic bolometer
arrays, but it is not shut by the stellar bounds the way the optical claim is.

## The kill test (pre-registered here)
A sub-mm line search at 542 GHz / 0.55 mm, sensitivity ε ~ 1e-12 (provisional):
- **Line found at m_native**(≈2.24 meV, rate ~4e7/day per 10 m² at ε=1e-12) ⇒ CFG723 E6 dead (P has a
  visible channel) ⇒ **framework dead** — regardless of the portal's hypothetical status.
- **Null** at that sensitivity ⇒ E6 consistent and the portal is bounded at ε < 1e-12.

This converts the speculative haloscope lane into falsification hardware for the core claim that the dark
mass has no non-gravitational channel. First time the framework's detector signature has a frequency,
a rate, and a kill condition.

## Honest scope
- All coupling bounds are provisional; the CMB-era/early-universe constraints on the portal are not re-audited
  here. The ε = 1e-14-at-2–3 eV surviving class and the 6.2e3 margin both carry the provisional flag.
- The sub-mm background estimate (CMB-only, R ~ 1e3) is schematic; a real instrument budget
  (atmosphere, detector NEP, filter losses) is out of scope.
- Nothing here derives the portal; the framework's position remains CFG723 E6 (no visible channel), and the
  kill test is precisely the statement that a line would falsify it.
- Footings never pooled; κ = ½ remains FITTED.

## Verdict
**PASS.** CFG790 re-scored: HARVEST CLOSED stands; DETECTABLE@ε=1e-12 at 2–3 eV → closed on stellar bounds
(provisional); DETECTABLE survives at ε = 1e-14 (band edge) or at the framework-native 0.55 mm line with
ε = 1e-12 allowed — where it doubles as a pre-registered kill test of CFG723 E6.