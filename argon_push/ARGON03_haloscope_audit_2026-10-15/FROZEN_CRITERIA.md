# ARGON03 FROZEN CRITERIA — haloscope re-audit + the framework-native sub-mm search

Written and committed ALONE, before any script. Date 2026-10-15.
Home: `argon_push/ARGON03_haloscope_audit_2026-10-15/`. κ = ½ FITTED. Canonical a₀ = 9.3603e-11 only.
Audits the newest lane (CFG790, commit 7ababab3e: "cold-energy haloscope — HARVEST CLOSED (1.8e-19 W per
10 m²), DETECTABLE for a dark-photon-like portal (ε = 1e-12: ~1e4–1e5 photons/day); visible single line at
2–3 eV mass"). CFG790's own README: "All external coupling bounds are quoted from memory (provisional)."
This audit anchors those bounds and re-scores the claim. No new particles added; the portal remains a
hypothetical extension (CFG723 E6: the framework derives no visible channel for P).

## Questions
- Q1 (evidence re-audit): does ε = 1e-12 at m = 2–3 eV survive stellar-coupling bounds (Sun/HB/RG)? Anchors:
  An et al. 2013 (arXiv:1302.3884): solar bound for m_V < 0.1 eV is κ·(m_V/eV) < 1.4e-11, i.e. κ_max = 1.4e-11/(m/eV);
  Caputo, Millar, O'Hare, Sanfilippo, "Dark photon limits: a handbook", PRD 104, 095029 (2021): the stellar-cooling
  exclusion band at 0.1–10 eV sits at ε ~ 3e-15–1e-14 (Stückelberg case; Higgs-mass case plateaus at χ ~ 1e-13 for
  m ≲ 100 eV). If ε = 1e-12 is excluded by ≥ 2 orders, the DETECTABLE class at the claimed parameters dies; the
  surviving class is CFG790's own ε = 1e-14 line (1–10 photons/day), which sits at the boundary.
- Q2 (knob audit, G6): the 2–3 eV line mass is assumed, not derived. The framework's only vacuum-induced quantum
  mass (CFG723 D5 route) is m_native⁴ = ρ_DE ħ³/c³ with ρ_DE = 4a₀²/(Gc²) (canonical) — compute it, its wavelength
  and frequency, and show the optical "line colour" claim (620/413 nm) rests on an un-derived knob.
- Q3 (positive flip): at m_native (~meV), the An et al. solar relation gives ε_max = 1.4e-11/(m_native/eV) ≫ 1e-12,
  so ε = 1e-12 is ALLOWED at the framework-native mass with several orders of margin; the absorption power is
  mass-independent (P = ε²ρcA) so the photon rate scales ∝ 1/m: rate(m_native) ≈ 4e7 photons/day per 10 m².
  Verdict to state: the haloscope survives ONLY at the framework-native frequency (sub-mm, ~0.55 mm / ~540 GHz),
  not as a visible-light line — and it becomes a pre-registered KILL TEST of CFG723 E6 (line found ⇒ P has a
  visible channel ⇒ framework dead; null ⇒ E6 consistent and the portal is bounded at ε ≲ 1e-12).

## Gates (all required)
- G1 Rate consistency: recompute P = ε²ρcA and photons/day at (ε, m) = (1e-12, 1 eV) with CFG790's own density
  (0.38 GeV/cm³, 10 m²) and reproduce their 1.8e-19 W / 9.8e4 day⁻¹ to <1% — the audit must not misquote the lane.
- G2 Stellar-bound scoring at m = 2–3 eV: ε_max band 3e-15–1e-14 (provisional, anchored); ε = 1e-12 excluded by
  ≥ 2 orders → class DETECTABLE@1e-12 dies; ε = 1e-14 sits at the boundary (survives provisionally).
- G3 Native mass: m_native = (4a₀²ħ³/(Gc⁵))^{1/4}; check λ = hc/m_native·c²... in eV → λ_nm and ν; expect
  ~2.2 meV, ~0.55 mm, ~5.4e11 Hz (sub-mm, NOT optical).
- G4 Knob check: the 2–3 eV mass is not expressible in framework constants (a₀, G, c, ħ, ρ_DE) to better than
  ~0.1%; the optical claim is a free parameter (G6 violation as stated).
- G5 Allowed-portal margin at m_native: ε_max(m_native) = 1.4e-11/(m_native/eV) vs ε = 1e-12 — margin ≥ 10³
  (provisional); CMB-era and other bounds NOT re-audited here (marked provisional, out of scope).
- G6 Kill-test statement: sub-mm line search pre-registered: 4e7 photons/day per 10 m² at ε = 1e-12; honest
  background caveat: CMB broadband flux over 10 m² ≈ 1e-12 W; in-band (R ≈ 1e3) ≈ 1e-15 W — signal 1.8e-19 W is
  ~4 orders below; search needs spectral resolution R ≳ 1e4 and/or photon-counting bolometer arrays. The null is
  E6-consistent; a line KILLS the framework (E6 dead), regardless of the portal's hypothetical status.
- K1/K2 (house): no new species; no claim of detection; bounds provisional; κ fitted; not theory closed.

## Verdict
- PASS: G1–G6 hold with stated margins → CFG790 re-scored (DETECTABLE@ε=1e-12 at 2–3 eV → closed on stellar
  bounds; framework-native sub-mm search → OPEN with ε = 1e-12 allowed, pre-registered kill test of E6).
- FAIL: any gate miss; the re-score is then not made and the obstruction is named.