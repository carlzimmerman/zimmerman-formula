# CQ2 sealed prediction: v3s wide binaries for Gaia DR4

Sealed 2026-11-04, before Gaia DR4 (due about 2026-12-02). Criteria 532e0dc567. κ = ½ FITTED; not theory closed.
Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. A prediction, not a result; nothing here says the data favour the
framework. Scoring is the frozen pipeline's own; this seal adds no rule.

## The prediction: v3s wide binaries are screened and Newtonian

- **Screened.** The Galactic phantom keeps D·P > 0 around every DR4 binary: binary margin ≥ 7.06e+03 at M_tot
  2.5 M☉ (line 10), near zone +0.0449 M☉/pc³. So the switch is on the stiff side and v3s's binary is v3's.
  The Galactic field does not lift the screening: the response is linear (ε ≤ 1.21e-05) and the hedgehog GM/L★² does not
  depend on a₀ or x_e; the field enters only through F below.
- **V3S-REST** (static hedgehog, L★ floor 21.682 / 22.849 pc, primary field 1.9e-10 m/s²): γ_r(s) − 1 = (s/L★)² F,
  independent of M_tot (0.5–2.5 M☉ give identical rows). Larger L★ lowers it as L★⁻².
- **V3S-MOVE** (X15: at β = 0 a moving binary carries no hedgehog): γ_r ≡ 1, Newton exactly.

| s (kAU) | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| γ_r − 1, canonical | 4.998e-08 | 1.998e-07 | 4.495e-07 | 1.248e-06 | 2.443e-06 | 4.981e-06 | 1.119e-05 | 1.985e-05 | 4.450e-05 |
| field range, canonical | 4.998e-08–4.998e-08 | 1.998e-07–1.998e-07 | 4.494e-07–4.495e-07 | 1.247e-06–1.248e-06 | 2.443e-06–2.444e-06 | 4.979e-06–4.982e-06 | 1.118e-05–1.119e-05 | 1.983e-05–1.986e-05 | 4.444e-05–4.452e-05 |
| γ_r − 1, alt | 4.501e-08 | 1.800e-07 | 4.048e-07 | 1.124e-06 | 2.201e-06 | 4.488e-06 | 1.008e-05 | 1.789e-05 | 4.013e-05 |
| field range, alt | 4.500e-08–4.501e-08 | 1.800e-07–1.800e-07 | 4.048e-07–4.048e-07 | 1.124e-06–1.124e-06 | 2.201e-06–2.201e-06 | 4.486e-06–4.488e-06 | 1.008e-05–1.008e-05 | 1.788e-05–1.790e-05 | 4.009e-05–4.015e-05 |

F on the sealed grid: 0.9876–0.9997. Anisotropic part at 30 kAU ≤ 1.7e-07 of Newton (not injected).

## Pushed through CW1's machinery (primary field)

| footing | Q_pred V3S (DR3 z) | Q_pred Newton | Q_pred plain | γ_inf V3S (spread) | γ_inf Newton | γ_inf plain | V3S − Newton, paired |
|---|---|---|---|---|---|---|---|
| canonical | -0.001018 (+0.077, CONSISTENT) | -0.001018 | +0.051396 | 1.0019 (0.0200) | 1.0019 | 1.1494 | +0.0000 +0.0000 +0.0000 +0.0000 |
| alt | -0.003007 (+0.154, CONSISTENT) | -0.003007 | +0.054172 | 1.0100 (0.0068) | 1.0100 | 1.2081 | +0.0000 +0.0000 +0.0000 +0.0000 |

- [canonical] DR3: Q_obs +0.0011 ± 0.0280; Q(V3S) − Q(N) = +2.46e-07. Pipeline bin medians V3S / Newton 1.000001–1.000034; γ_inf identical to Newton's in every realisation (fit grid 0.0025).
- [alt] DR3: Q_obs +0.0016 ± 0.0300; Q(V3S) − Q(N) = +4.82e-09. Pipeline bin medians V3S / Newton 1.000000–1.000029; γ_inf identical to Newton's in every realisation (fit grid 0.0025).

**Separation labels** (CW1's rule: dQ / 0.020 and dγ_inf / 0.028; SEPARABLE ≥ 3, MARGINAL ≥ 2):

- [canonical] V3S vs plain QUMOND: 2.62, 5.27 → **SEPARABLE**; V3S vs Newton: 0.0000, 0.0000 → **NOT SEPARABLE**.
- [alt] V3S vs plain QUMOND: 2.86, 7.08 → **SEPARABLE**; V3S vs Newton: 0.0000, 0.0000 → **NOT SEPARABLE**.

So DR4, read by the frozen pipeline, cannot tell v3s from Newton; a DR4 γ_inf like plain QUMOND's would contradict v3s on
either footing and in either reading (REST or MOVE).

## Verdict lines and checks

- [canonical] NEWTONIAN: max γ_r − 1 4.45e-05, |ΔQ| 2.46e-07, paired |Δγ_inf| 0.0000 (lines 1e-3).
- [alt] NEWTONIAN: max γ_r − 1 4.01e-05, |ΔQ| 4.82e-09, paired |Δγ_inf| 0.0000 (lines 1e-3).
- Checks: K1 PASS, K4 PASS, K5 PASS, K6 PASS, K7 PASS, K2 PASS, K3 PASS. Known answers: C6's 24 numbers, CW1's DR3 Q and every
  pipeline realisation reproduced exactly.
- MUTATE (switch inverted, unscreened stand-in): γ_inf V3S 1.1631 / 1.2025, vs Newton SEPARABLE / SEPARABLE: **BITES**.

## Provenance

- Frozen pipeline SHA-256 as recorded by CW1 (not recomputed): `7c884e0e0a4cb9cb5d6280d558cf64c829974ed14143a90261bd6a6fbf3007c9`; imported read only, bytecode off.
- Seeds as CW1 (20261216, 2026110302, 2026110402, 11, 12); master 1,000,000, N_data 30,000, 4 realisations.
- `cq2.py` SHA-256 `6fbf2abfe5e06d0b7e09a6dc31f907afd0f3e86eceb40f936ed24f69a13a9b5c`
- `cq2.json` SHA-256 `a73f754ced4fd4af67fe34963780550f9f5bd8fe8551965a3ca15971c4cae61c`
- `cq2.out` SHA-256 `7c68348e2ea3da35b4da6f39b123d63daec841c598b50c9a01b2774fa4e54103`
- `cq2_MUTATE.json` SHA-256 `22e83b65e7ac61b8123a6ad4dc0aa76c2769fbaa569c4495d275d6986d9c2b60`
- `cq2_MUTATE.out` SHA-256 `51b482eb7ad11aefe7dc536e2c596a5ac085d7bd19340b33352d20136b263eb1`

κ = ½ FITTED; not theory closed.
