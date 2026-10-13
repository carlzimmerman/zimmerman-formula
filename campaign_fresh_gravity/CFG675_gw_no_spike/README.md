# CFG675: no cold-energy spike around black holes — SEALED vacuum-GR prediction for LISA IMRIs

Criteria 1d8d97ca6 (committed alone first; block CFG670–679). `cfg675.py` → `cfg675_predictions.json`,
**sha256 d153665c211737c120ff548e9d3056c2f54f0007d1292bafac804d1ae86c37ac**. MUTATE bites (ρ→0 gives ΔN = 0; ρ×1e6 gives 542
cycles; exit 1). κ = ½ FITTED; footings separate; cold energy mass required; no particle species; not "theory closed".

| system (last 5 yr to ISCO) | vacuum cycles | framework ceiling ΔN (can / alt) | particle-DM static spike ΔN (context) |
|---|---|---|---|
| 1e3 + 1.4 M☉ | 5.0e6 | **7.4e-4 / 9.2e-4** | γ 7/3: **1.5e6**; γ 9/4: 5.0e5; γ 3/2: 0.85 |
| 1e4 + 10 M☉ | 1.35e6 | **5.6e-6 / 2.9e-5** | — |

Spike benchmark ρ_sp = 226 M☉/pc³, r_sp = 0.54 pc, γ = 7/3, verified in Kavanagh+2020's own TeX (arXiv 2002.12811); static dress,
no feedback (feedback lowers DM dephasing; Kavanagh+2020 show it stays large for this benchmark).

**Sealed prediction.** Cold energy is arranged by the law, so its density near any mass is fixed by a0 and that mass alone — no
free amplitude, no spike. Even the ν_mono ceiling (whose constant-a0 tail is already Solar-System-excluded; the real kernel is
silent, so the true value is lower) gives **< 10⁻³ cycles of dephasing**: the framework predicts **vacuum-GR IMRI waveforms**.
ρ_c(1e-3 pc) ≈ 1.1e5 M☉/pc³ ceiling vs 5.4e8 for the γ = 7/3 spike.

**Kill line (frozen):** a LISA / deci-Hz IMRI whose waveform requires an environmental density ≥ 10× the framework ceiling at
r ≤ 1e-3 pc, with the baryonic environment bounded below that, excludes the "cold energy = the law's profile" reading. A spike as
dense as the benchmark would exceed the ceiling by ~5000× at 1e-3 pc.

**Honest weight:** lopsided. A detected spike kills the framework; a null does not much favour it, because ΛCDM spikes can be
destroyed (mergers, stellar heating, off-centre formation). What is distinctive: the framework allows **no** environmental
dark dephasing around isolated IMBHs, at any time, anywhere.

## CORRECTION v2 (2026-10-12, same day; sealed v1 kept untouched)
Two defects in v1, found while answering the GW questions (CFG677): (1) the record's ν_mono is **not** ½ + √(¼ + 1/y) (my hand
estimate's form) but FP1/L340's ν = 1 + h(y)/y (h = exponential-RAR phantom to its peak, then a slow monotone tail, h(1e14) = 1.64);
(2) in the IMRI band (y ~ 1e12–1e16) ν_mono − 1 cancels to machine precision, so v1's density there was numerically corrupted.
v2 computes the phantom field directly as a0·h(y) from the record's own table (no cancellation): `python3 cfg675.py` (default)
→ `cfg675_predictions_v2.json`, **sha256 4c2cc32ece2a570f0d5ee3e7dac3559a56c8bfdc47975c1e11f4bbb8066689f1**; `CFG675_V1=1`
reproduces v1 byte-identically. **v2 ceiling dephasing: 1.6e-4 / 1.9e-4 cycles (1e3+1.4), 2.3e-5 / 2.8e-5 (1e4+10)** — the
prediction (vacuum-GR IMRI) and the kill line are unchanged; cite v2.
