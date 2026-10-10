# LEPTON_CHAIN_2: sharper certificates (frozen before any Lean, 2026-10-09)

Owner: "keep going, swing harder on the lean certificate." This extends LEPTON_CHAIN (0a6eec49e). It certifies implications only.
The quoted ranges are inputs: NuFIT 6.0 3σ for s23² (union of both variants, [0.43, 0.596]) and a padded s13² box [0.020, 0.025].

**Theorems (zero sorry, standard axioms):**
- L9 `tm1_cp_large`: TM1 (as in L4), s13² ∈ [0.020, 0.025] and s23² ∈ [0.43, 0.596] give cos²δ ≤ 0.21, so sin²δ ≥ 0.79. Then δ lies
  within 27.4° of 90° or 270°. TM1 FORBIDS CP conservation (δ = 0 or 180°) anywhere in today's 3σ octant range. A Python scan of
  the box gives max cos²δ = 0.2061, so 0.21 has margin. The proof uses decoupled bounds; the scan only sets the constant.
- L10 `tm1_jarlskog_floor`: same hypotheses give J² ≥ 0.00077, where J = s12 c12 s13 c13² s23 c23 sin δ, so |J| ≥ 0.0277. The scan
  minimum is 0.02826 and the box maximum of |J| is 0.0358. So TM1 means CP violation at ≥ 77% of the largest value the measured
  angles allow.
- L11 `io_excluded_by_desi`: inverted ordering with |Δm²32| ≥ 2.40e-3 and Δm²21 ≤ 7.62e-5 eV², all masses ≥ 0, gives
  Σ > 0.0970 > 0.0642. So DESI DR2 (ΛCDM, quoted) forces normal ordering. This removes A3's ordering choice as a free assumption.
- L12 `desi_caps_m1`: normal ordering with Δm²21 ≥ 7.38e-5 and Δm²31 ≥ 2.49e-3, m1 ≥ 0 and Σ < 0.0642 gives m1 < 0.0046 eV. This
  tightens FS11's 7.35 meV Dirac window using data alone, independent of the conjecture.
- L13 `desi_caps_a0_under_A3`: if m1⁴ a0_c² = m_c⁴ a0² (L7's scaling, with m_c = 2.24 meV at a0_c) and m1 < 0.0046 eV, then
  a0 < 4.22 a0_c. Under A3, cosmology's neutrino-mass bound becomes an upper bound on the MOND scale. It is weak, but it is a
  genuine cross-sector link, and both committed footings (ratio 1.21) pass it.

**MUTATE (all must FAIL, each with a concrete counterexample in the header):**
- M4: cos²δ ≤ 0.20 (the box maximum is 0.206).
- M5: m1 < 0.0040 (m1 = 4.2 meV gives Σ = 0.06384 < 0.0642).
- M6: IO Σ ≥ 0.10 (the lower-edge splittings give 0.0972).

**Statement match:** an independent reviewer checks the docstrings against the Lean statements before the commit.
