# CFG29 — the binary audit of the ultra-faint failure

Script: `CFG29_ufd_binary_audit.py`, under a second.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every dispersion is halved, and H1 fails (rc = 1).
- The main run exits 0.

κ = ½ is fitted. Both footings are used.

## Question

CFG28 left the ultra-faint offset (+0.30–0.33 dex, 3.5–3.8σ) robust to our analysis, to tides and to noise. Binaries were the one escape. Can unresolved binaries make it?

Two published results bound what binaries can do. Both are used as fixed inputs, not fitted:
- **Single-epoch data:** binary populations are "unlikely to produce dispersions much in excess of ~4.5 km/s", even from a near-zero intrinsic dispersion (McConnachie & Côté 2010, ApJL).
- **Multi-epoch data:** with a 10-year baseline, the residual bias reaches ~10–120% for true dispersions below ~1 km/s, and less for hotter systems (Ou et al. 2026, arXiv:2609.19407).

Binaries are strongest where the true dispersion is smallest.

## Results (CFG28's data and machinery, exec'd read-only)

**C1 (control):** CFG28's Kaplan–Meier medians are reproduced exactly.

**H1 passed: the offset persists where binaries are weakest.**

| subsample (framework-predicted dispersion) | canonical | alt |
|---|---|---|
| ≥ 1.5 km/s (19 resolved + 2 limits) | **+0.313 ± 0.031 → 3.8σ** | +0.293 → 3.5σ |
| ≥ 2.0 km/s (small) | +0.229 ± 0.146 (1.4σ) | +0.295 ± 0.122 (2.0σ) |
| < 1.5 km/s (where binaries are strongest) | +0.475 ± 0.082 → 4.2σ | +0.455 → 4.0σ |

**H2 passed: two ultra-faints far from the Milky Way exceed the single-epoch binary ceiling by more than 2σ.**
- **Eridanus II:** 6.9 ± 1.1 km/s at 372 kpc, predicted 3.05; 2.3σ above the ceiling (Li et al. 2017).
- **Ursa Major I:** 7.2 ± 1.1 km/s at 102 kpc, predicted 1.92; 2.4σ above (Geha et al. 2026).

Binaries cannot explain either, even in principle.

**The binary floor the framework would need**, √(σ_obs² − σ_pred²), has a median of 3.37 km/s. 26 of 31 systems need more than 2.0 km/s, which is about the most a 10-year baseline leaves for a true dispersion near 1 km/s. Hercules and Boötes III need none.

## Standing

**Binaries do not explain the ultra-faint failure.** With CFG28, it is robust to:
- our analysis: the upper limits restored and a systematic floor added;
- Milky Way tides;
- measurement noise;
- binary stars, as bounded by the published simulations.

It stands at **3.5–3.8σ**: the ultra-faints move about 2× faster than the law predicts from their stars. The caveat is that both binary bounds come from simulated binary populations; an extreme binary population outside them is not excluded here.

Nothing here says the theory is closed.
