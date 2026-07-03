# Bulge-unlock verdict — the two named L1 caveat knobs, turned (2026-07-02)

**Scripts (committed, exit 0):** `real_research/reviews/inhand_2026_07/lane_L1b_bulge_sigma_knobs.py`
(gated: V1 banked-baseline repro + V2 mock injection through the unlocked machinery + grid convergence)
and `real_research/reviews/inhand_2026_07/VERIFY_L1b_prior_sensitivity.py` (adversarial prior-width/center check).
Convention: the banked CORRECTED data-space likelihood (headline of `VERIFY_L1_inclination_norm_fork.py`).
Framework nu(y)=sqrt(1+1/y); canonical a0=9.36e-11; fork 1.13e-10. Full SPARC N=171, gas-dom N=37.

## Knob table (full sample unless noted; Dchi2 vs 9.36e-11; boot = 500-resample galaxy bootstrap)

| Configuration | a0_hat | Dchi2(9.36e-11) | boot-z(9.36e-11) | Dchi2(1.13e-10) |
|---|---|---|---|---|
| BASELINE locked U_bul=1.4*U_disk (banked) | 1.372e-10 | 269.7 | ~3.5 | 63.9 |
| Knob 1: U_bul unlocked 0.05 dex | 1.242e-10 | 150.0 | — | 16.2 |
| Knob 1: U_bul unlocked 0.10 dex | 1.181e-10 | 116.3 | ~4.2 | 5.2 |
| Knob 1: U_bul unlocked 0.15 dex | 1.171e-10 | 105.2 | ~4.0 | 3.3 |
| Knob 1 extreme: U_bul near-free 0.30 dex | 1.167e-10 | 99.2 | ~4.0 | 2.5 |
| Knob 1 (0.10) MINUS top-3 bulge influencers | 1.158e-10 | 91.6 | ~4.7 | 1.5 |
| Knob 2: per-galaxy sigma_int (half-normal, tau profiled) | 1.354e-10 | 273.6 | ~5.4 | 57.2 |
| JOINT both knobs | 1.275e-10 | 164.2 | ~2.9 | 18.5 |
| Gas-dom cut, any knob combo | 0.98–1.02e-10 | 0.7–3.0 | — | 5.9–7.9 |

Adversarial checks: V1 reproduces the banked corrected numbers exactly (1.372e-10 / 9.816e-11 / boot z~3.5);
V2 mock (truth 9.36e-11) recovered at 9.40e-11 (+0.4%, Dchi2(truth)=0.00) through the unlocked machinery;
prior-center shift 0.5/0.7/0.9 gives Dchi2(fw)=92/116/137 (never near 9); U_bul posterior modes interior
(0/64 grid-edge pins; IC4202 wants U_b~0.22); grid convergence OK (a0_hat moves <0.6% under step/span changes).

## Pre-registered reading that fired: **MIXED — survives-leaning, not a clean HARDEN**

- **COLLAPSE did NOT fire.** No knob (nor both jointly, nor the near-free prior, nor dropping the top-3
  bulge influencers) brings the full-sample a0_hat into [0.9,1.1]e-10 or Dchi2(9.36e-11) below ~9.
  Minimum across everything tried: Dchi2=91.6, bootstrap-honest z~2.9 (joint-both-knobs). The full-sample
  exclusion of 9.36e-11 is **not a bulge-M/L or error-model artifact**.
- **Clean HARDEN did NOT fire either**: each knob alone stays >3 sigma (z~4.2 and z~5.4), but stacking
  both knobs dips the bootstrap to z~2.9, just under the pre-registered bar. Quote the exclusion as
  **z ~ 2.9–4.2 bootstrap-honest across error-model choices**, not ">3 sigma under all knobs".
- **What the unlock actually does**: it moves the optimum, not the exclusion — 1.37e-10 → 1.17–1.28e-10.
  The **1.13e-10 fork becomes statistically compatible** under honest bulge M/L (Dchi2=2.5–5.2, boot
  P(<=fork)~0.17–0.27), while the gas-dominated cut stays centered at 9.8e-11–1.02e-10 (canonical-compatible,
  0.8–1.7 sigma).

## Which-a0 paper, Sec 3 update note (suggested text)

"Unlocking Upsilon_bul (independent per-galaxy lognormal prior, 0.05–0.30 dex) and replacing the global
profiled sigma_int with a per-galaxy hierarchical form does not remove the full-sample exclusion of
a0=9.36e-11 (Dchi2 >= 92 in all variants; galaxy-bootstrap z ~ 2.9–4.2), so the exclusion is not a
bulge-M/L systematic. It does, however, shift the full-sample optimum from 1.37e-10 to 1.17–1.28e-10,
rendering the rho_total/cH0 fork value 1.13e-10 compatible at <~2 sigma; the gas-dominated subsample
remains centered on the canonical value (0.98–1.02e-10, <~1.7 sigma). The star-dominated/gas-dominated
split, not bulge M/L, is the open systematic."

## Coefficient standing

Unchanged for the canonical footing (a0=cH_Lambda/Z is horizon-derived, not fit to SPARC). What changes:
the fork 1.13e-10 gains empirical standing — under honest bulge M/L it is the full-SPARC-compatible value,
while gas-dominated galaxies anchor 9.36e-11. The footing fork now maps onto a real data split
(star-dom vs gas-dom), which is a named open tension for the framework on its own terms, at
bootstrap-honest z~2.9–4.2, not a closed door and not an artifact.

Runs: `L1b_full_run2.log` (98 s, EXIT 0), `VERIFY_L1b_prior.log` (26 s, EXIT 0), archived alongside the scripts.
