# CFG720: the one-action construction C* on the merger stopwatch

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (7687ef48c), 2026-10-13. Block CFG720–729.
- **Question:** C* (CFG658/694/695, the other chat) passes the EFE gates, SPARC and cluster shear but has not faced mergers. Its bound
  charge responds to all baryons; with instant response it is CFG623's excluded α = ∞ class. Which response time t_resp (set by its
  inertia (I/2)|Ṗ|², a free constant) do the Bullet + Harvey data require?
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

## Status: QUEUED

`run_720.sh` (nohup) waits until no 1024³ PM job (cfg596/636/640/650) or other merger lane is live and ≥ 16 GB is free, then runs
`cfg720.py`: C-R control (ν_mono, t_resp 0 must reproduce CFG623 `ainf_can`) → field-mode calibration with ν_s → 10 grid runs (t_resp 0,
0.1, 0.3, 1, 3 Gyr × both footings). Log: `../../../_external_data/cfg720_work/waiter.log`. Outputs are not committed automatically.

## Pre-run disclosure (2026-10-13)

Smoke test (code check only, 1.5 GB): Sim720 built in field mode with ν_s and t_resp 0.3 Gyr, two steps: field mass ratio 0.9999997,
finite; the kernel swap changes the initial field mass by +0.8% against ν_mono.
