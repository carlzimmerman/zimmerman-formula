# EM1: route E (cold energy clumps like dust, law emergent). As frozen: ROUTE E FAILS ON SPARC, on the Υ leg only. With Υ pinned at 0.5, dust ties the law, so SPARC does not separate them. Adopting route E turns a₀ = κc√(Gρ_Λ) into a coincidence, and halo structure alone predicts the same flat a₀(z)

Criteria and ledger were committed first: **1b0dbd6eef**. Script: `em1_emergent.py` (55 s, 1 thread, 0.73 GB, run beside the
live L1 384³ job). `--mutate` (halo × 0) fails KH as it should (exit 1). `--ups05` is AMENDMENT A1 (see below). κ = ½ FITTED. Footings
never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

**The question.** The v3s verdict leaves two roads. One is a new mechanism (PH1_two_phase_cold_energy, another session). The
other is route E: the cold sector is dust everywhere, there is no law force, and the RAR is emergent. Route E passes clusters,
growth/CMB, the radiation era, hosted dwarfs and TDGs **by construction**, because its cold sector is ΛCDM's. EM1 scores what is
left, framework-natively. It uses the record's own refit backgrounds A and B and CLASS P(k), with no abundance matching and no
ΛCDM stellar-to-halo relation. Halo masses follow one SPARC-internal global relation log M200 = a + b(log M_b − 10).

| row | A (C2 refit) | B (CFG886) | class |
|---|---|---|---|
| T0: acceleration from {G, M, H} | G^⅓ M^⅓ H^{4/3}, unique, mass-dependent | same | a₀ = κc√(Gρ_Λ) is **not a law** of route E |
| R1 NFW dust, Υ per galaxy (law: 0.0541 / 0.0537) | rms 0.0656, median Υ **0.36**; a, b = 11.18, 0.90 | 0.0655, Υ 0.35 | **FAIL** (Υ leg; the rms leg passes) |
| R1-DC14 (EXTERNALLY CALIBRATED feedback) | 0.0573, Υ 0.47 | 0.0573, Υ 0.48 | FAIL (Υ leg, by 0.02–0.03) |
| R2 allowed (free M200, c ± 2σ, f_b imposed) | 0.031, Υ 0.32; halos scatter 0.51 dex about R1's relation | 0.031, Υ 0.32; 0.52 dex | line fails (Υ) |
| R3 emergent g† (model / data at the same Υ) | 1.18e-10 / 1.19e-10; drift 0.17 / 0.18 dex; vs a₀ +0.102 can, +0.019 alt | 1.23e-10 / 1.22e-10; +0.118 / +0.035 | DOES NOT EMERGE (misses the canonical 0.10 line by 0.002 / 0.018) |
| R4 halo g₋₂(z = 2.33)/g₋₂(0) at fixed M200 1e11 / 1e12 | 0.99 / 1.06 | 0.97 / 1.04 | **NOT DISTINCT** from the framework's flat a₀(z) (1.00; CFG689 0.91–0.94) |

Checks (all PASS): KT (T0), KP (P4's law rms and Υ reproduced exactly), KC (own σ8 equals F3's to 1e-5), KN, KH, KR.

**Overall (frozen rule): ROUTE E FAILS ON SPARC.**

## AMENDMENT A1 (post-result, reported only; the classes above are unchanged)

A fail gets checked as hard as a win. Both R1 failures come from the median-Υ leg alone: dust cusps soak up the inner mass,
so per-galaxy Υ drops below stellar-population values. Two diagnostics were added after the result:

- **Υ pinned at 0.50 for law and dust alike** (`--ups05`, outputs `_UPS05`). Dust NFW with one global relation gives **0.1020**
  (A and B). The law gives **0.1124** canonical and 0.1029 alt. At equal freedom, dust ties or beats the law. The R1 FAIL is
  real but soft: SPARC alone does not separate route E from the law.
- **Low-g shape.** The frozen unweighted slope differs (model 0.25 vs data 0.58), but the weighted slopes nearly agree (0.63 vs 0.67).
  The gap sits in about 100 low-weight dwarf points below g_bar = 10^−11.75, where the dust model overshoots by a median 0.25 dex
  (the cusp problem). This agrees with CFG477's DC14 slope reading.

## What this means

1. **Route E is not killed by galaxies.** Its SPARC failure is a soft Υ-leg failure, and with Υ pinned it ties the law.
   Clusters, growth/CMB, the radiation era, hosted dwarfs and TDGs pass, but because route E inherits ΛCDM's sector, not as
   framework results.
2. **Route E erases the framework's content.** By T0, a₀ = κc√(Gρ_Λ) becomes a z = 0 coincidence (R3 lands within 0.02–0.12 dex
   of the footings), and κ stops being a constant of nature. By R4, dust halos at fixed mass already predict a flat a₀(z). The
   a₀(z) test can then separate route E from the framework only through galaxy-formation evolution (CFG565's SHMR and size terms,
   ×2.8 by z = 2), not through halo structure.
3. **The no-particle rule binds.** Dust that multistreams is collisionless matter, or a classical wave field whose wave scale is
   a new constant (L374). Route E is ΛCDM with the dark matter renamed "cold energy".
4. So the converged answer is: route E is a consistent fallback, but adopting it means giving up the theory, not completing it.
   The only road that keeps a₀ tied to Λ is a new mechanism (PH1, in progress elsewhere).

Scope: NFW with Bullock+01 c(M) applied to M200c (a mass-definition mismatch, disclosed); DUST-N-BODY calibrations not run here;
no adiabatic contraction; spherical g_bar; (a, b) fitted in-sample like κ. The record's ΛCDM-machinery versions are CFG476 (DMO
FAILS 0.205), CFG477 (DC14 MARGINAL 0.120), CFG545 (s ≤ 0.16) and CFG565 (g†(z) rises).
