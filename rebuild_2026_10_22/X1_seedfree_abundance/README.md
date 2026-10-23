# X1_seedfree_abundance — evolving the actual high-H quantum state through bath formation, with no seed

**Verdict: UNDETERMINED by the frozen word rule, with two crisp results inside it.** (1) Every light-spectator (ξ = 0)
point that was computed fails the CMB isocurvature bound by 2e8–6e8 in power, for every closure. (2) In the kinetic
(perturbative) description the X condensate is absorbed by the Φ bath as soon as it starts to oscillate (Γ/H = 22.6 at the
primary input, from Codex's own five-point amplitude extended here to the hot bath). That gives Ω_c h² ≈ 1.4e-8. 0.12 is
reached only if the condensate never interacts (the ceiling closure), which this rate contradicts. The frozen rule still
reports UNDETERMINED because the X-onset epoch is bracketed, not computed at its physical ~1e5 hierarchy (A3). It does not
say SCOPED NO-GO only because G2 was computed for closures L and C at all 28 grid points (all FAIL) and for K only at the
primary point (FAIL); every computed ξ = 1/6 point is far below 0.12.

κ = ½ is FITTED (it does not enter). No dark-matter particle is added: Φ and X are the record's scalar carrier, unchanged.
Not "theory closed". Owner's request (verbatim): "Find a scalable way to evolve the actual high-H quantum state through
bath formation, retaining coherence and non-Gaussian correlations. Include reactions and inverses and calculate the cold
abundance without assuming a seed." Frozen criteria and amendments A1–A3: `FROZEN_CRITERIA.md`; ledger:
`ASSUMPTION_LEDGER.md`; Codex inputs copied with sha256: `PROVENANCE.json`, `provenance/`.

## The method (frozen) in one paragraph

Start from the actual quantum state at the end of inflation. The box zero mode is a stochastic-inflation sample: Codex's
Langevin is reproduced bit for bit, then noise is stopped ln(1/k_min) e-folds early. Every other lattice mode carries the
de Sitter Bunch–Davies Hankel state, sampled as a Wigner Gaussian with its half-quantum. No population is inserted.
Evolve the full nonlinear equations of the action on a 3D expanding lattice with truncated Wigner (TW). Normal ordering
enters as its exact Weyl counterterm. Coherence (the zero modes) and every connected correlation ride along, and every
reaction and its inverse is implicit, with classical Bose enhancement. Hand over to a momentum-resolved quantum Boltzmann
equation only where TW is certified. Across X onset, where the ~1e5 hierarchy cannot be resolved, use three frozen closures:
L = prompt thermalisation, K = kinetic (perturbative reactions only), C = no interaction (ceiling). Then run a freeze-out
network with r1–r4 and their detailed-balance inverses.

**The brief's premise is corrected.** Φ does not start to roll at H ~ 10 m. Its quartic makes it roll at
H ≈ √λ|Φ| ≈ 0.1 H_inf, a few H_inf⁻¹ after inflation. X rolls at H = M, at a = 2.59e6. The radiation-era quartic sector
is conformal and ξ drops out of it (a″ = 0). So ξ enters only through the inflationary state and any non-radiation era.

## Results

### Validation of TW against Codex's exact reduced Hamiltonians (V0–V3)
- **V0.** My zero-momentum Fock builder reproduces Codex's `Model` Hamiltonian exactly (difference 0.0, 25 states).
- **V3, error versus occupation.** Fixed classical density ν = n/V ∈ {2, 8}, window t ≤ 500 m⁻¹, exact Fock evolution
  (RWA where full H is too large, A1).

| scenario | n = 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| A: X condensate → ΦΦ, occupations O1/O2 (ν = 8) | 0.033/0.045 | 0.025/0.046 | 0.017/0.038 | 0.034/0.064 | 0.007/0.015 | over budget |
| A: same, ν = 2 | 0.020/0.033 | 0.033/0.056 | 0.010/0.018 | 0.004/0.004 | 0.0015/0.0005 | over budget |
| B: quartic Φ condensate, coherent fraction O3 (ν = 8) | 0.99 (revival) | 0.99 | 0.041 | 0.014 | 0.010 | 0.007 |
| B: normalised κ₄/κ₂² error O5 (ν = 8; median over t) | 3.4 | 4.0 | 2.4 | 2.1 | 1.8 (0.016) | 1.9 (0.011) |

  Occupation and conversion errors fall to ≤ 1.5 % at n = 16. Coherence errors fall from order 1 (quantum revivals)
  to < 1 % at n ≥ 16. The normalised connected cumulants are **not** certified. At instants where the quadrature
  distribution is thin and phase-aligned, κ₄/κ₂² ≈ 10 and TW misses it by ~2, even at n = 32; the time-median error is 0.01.
  By the frozen rule no n* ≤ 32 exists. The occupation-only diagnostic gives n* = 16.
- **V1 (one-cell wavefunction).** Coherent Φ with n = 1, 2: occupation error 1.6 % and 1.1 % over t ≤ 50. Codex's
  one-excitation state: the true signal (7e-5) is below the TW sampling floor (2.4e-3, 4e5 signed trajectories).
- **V2 (12-oscillator absorption).** P_abs ≈ 1.35e-8, against a TW sampling floor of 0.07 at 4000 trajectories. Resolving
  it would need ~1e17 trajectories. TW cannot see few-quantum reactions, which is expected at n ~ 1.

### Bath formation (E1 prototypes, 32³/48³/64³ to τ = 2000; production queued)
- The Φ condensate fragments by τ ≈ 100–400 (Lamé resonance seeded by the inflationary modes) but **stays partly
  coherent**. The windowed |φ̄|²/⟨|φ|²⟩ is 0.80 → 0.56 → 0.52 → 0.47 at τ = 100/500/1000/2000 (64³, TW_full). The spread
  is 0.23–0.69 across TW_full, TW_kc, CSA, seeds and resolution, so this number is **not converged** in the prototype.
- X stays fully coherent: f₀(X) = 1.0000 in every run. Its cubic coupling is ~1e-14 of the quartic in this epoch.
- **Non-Gaussianity persists.** The connected complex 4th cumulant of the fluctuations is g₄ = −0.19 (sub-Gaussian).
  The excess kurtosis of Re δφ swings by ±0.2–3 with the zero-mode phase.
- About 30 % of the non-vacuum fluctuation energy sits in modes with n < 16 at τ = 2000, so the hand-over is not reached.
  A classical Boltzmann equation without the condensate fails the TW overlap test: L1 = 1.41 against the frozen 0.15
  (0.07 with no evolution at all). Kinetic theory is not valid while the condensate persists, consistent with Codex.
- The E2 Boltzmann (CONDITIONAL, from τ = 2000) keeps number to 1e-13. Energy moves 2 % because the Hartree mass is
  self-consistent, and the conservation projection was large (A3). At X onset the bath is overpopulated 7.3× against
  thermal, so its Hartree mass gives a tachyonic-window ratio r = 2g|X|/m_H² = 0.02 (0.66 for a μ = 0 thermal bath). The
  coherent tachyonic window is therefore not open at onset; it opens later as r ∝ a^{1/2}.

### Cold abundance (Ω_c h² = 2.744e5 · Y; target 0.12 is a ΛCDM-processed comparison line, never a fit)
Primary inputs: H_inf = 1.3445e10 GeV (Codex's value, itself chosen from a free-condensate estimate), N_e = 60, instant
reheating, ξ = 0, median patch.

| closure | Ω_c h² | 10–90 % patch range (|X|² percentiles) |
|---|---|---|
| L prompt thermalisation at H = M | 9.8e-9 | 6.3e-9 – 1.7e-8 |
| K kinetic: condensate as X at rest, absorbed via XΦΦ̄ → ΦΦ (Γ/H = 22.6) | 1.40e-8 | 7.1e-9 – 2.8e-8 |
| C ceiling: condensate never interacts | 0.167 | 0.024 – 0.55 |

Sensitivities at the primary point (Ω_L / Ω_K):
- Crossed RIS channel counted ×1 of D: 9.78e-9 / 1.40e-8.
- Codex power-law D above 2m instead of the MC: unchanged.
- PB rule (X chemistry integrated instead of the frozen μ = 0 rule): 1.07e-8 / 1.51e-8.
- No 4→2 above T = m ("relcut"): not completed within its 25-minute budget.

The dark sector freezes out chemically near T_d ~ m, because it is ~1e-4 colder than the visible sector. So the
non-ceiling yield is set by the dark entropy at X onset.

**Isocurvature (G2).** At the primary point P_S = 1.6e-2 (L), 1.7e-2 (K) and 5.0e-2 (C), against the bound 8.3e-11, so
every closure FAILS by 2e8–6e8. The levers are dlnY/dln|X| = 0.80/1.07/2.0 and dlnY/dln|Φ| = 0.69/0.42/0. The map rows
below give G2 for L and C at every computed point.

**ξ = 1/6 control.** There is no light spectator, so the yield comes only from linear conformal production:
Ω ≈ 6.1e-30 for every H_inf with T_rh ≥ 1e9, and ≈ 1e-31 for production during a w = 0 era (T_rh = 1e6). The exact
solution is a half-line problem whose number is 0.371 of the full-line formula named in K14.

### Input map (frozen grid; median patch, N_e = 60)

| H_inf (GeV) | T_rh | Ω_L | Ω_K | Ω_C (ceiling) | G1 | G2: P_S for L / C (bound 8.3e-11) | Ω at ξ = 1/6 |
|---|---|---|---|---|---|---|---|
| 1e+08 | instant | 7.78e-12 | 1.09e-10 | 9.26e-06 | BELOW | 1.7e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+08 | 1e+12 | 5.65e-12 | 1.15e-10 | 9.26e-06 | BELOW | 2.1e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+08 | 1e+09 | 4.90e-12 | 1.22e-10 | 9.26e-06 | BELOW | 2.9e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+08 | 1e+06 | 1.32e-13 | 1.68e-10 | 2.64e-07 | BELOW | 2.5e-02 / 5.0e-02: FAIL | 1.1e-31 |
| 1e+09 | instant | 2.29e-10 | 3.39e-10 | 0.000926 | BELOW | 1.8e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+09 | 1e+12 | 1.50e-10 | n/c | 0.000926 | BELOW | 2.7e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+09 | 1e+09 | 1.45e-10 | 3.54e-10 | 0.000926 | BELOW | 3.0e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+09 | 1e+06 | 4.00e-12 | 2.68e-10 | 2.64e-05 | BELOW | 2.9e-02 / 5.0e-02: FAIL | 1.1e-31 |
| 1e+10 | instant | 6.43e-09 | 9.21e-09 | 0.0926 | BELOW | 1.7e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+10 | 1e+12 | 4.14e-09 | n/c | 0.0926 | BELOW | 2.8e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+10 | 1e+09 | 4.11e-09 | n/c | 0.0926 | BELOW | 2.9e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+10 | 1e+06 | 1.18e-10 | 1.79e-10 | 0.00264 | BELOW | 3.0e-02 / 5.0e-02: FAIL | 1.1e-31 |
| 1.345e+10 | instant | 9.80e-09 | 1.40e-08 | 0.167 | BRACKETS | 1.6e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1.345e+10 | 1e+12 | 6.31e-09 | n/c | 0.167 | BRACKETS | 2.8e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1.345e+10 | 1e+09 | 6.28e-09 | n/c | 0.167 | BRACKETS | 2.0e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1.345e+10 | 1e+06 | 1.83e-10 | 2.88e-10 | 0.00477 | BELOW | 3.0e-02 / 5.0e-02: FAIL | 1.1e-31 |
| 1e+11 | instant | 1.65e-07 | 2.35e-07 | 9.26 | BRACKETS | 1.5e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+11 | 1e+12 | 1.06e-07 | n/c | 9.26 | BRACKETS | 2.5e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+11 | 1e+09 | 1.06e-07 | n/c | 9.26 | BRACKETS | 2.5e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+11 | 1e+06 | 3.37e-09 | n/c | 0.264 | BRACKETS | 2.9e-02 / 5.0e-02: FAIL | 1.1e-31 |
| 1e+12 | instant | 4.34e-06 | 6.21e-06 | 926 | BRACKETS | 1.5e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+12 | 1e+12 | 2.78e-06 | 4.91e-06 | 926 | BRACKETS | 2.5e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+12 | 1e+09 | 2.78e-06 | n/c | 926 | BRACKETS | 2.5e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+12 | 1e+06 | 8.75e-08 | n/c | 26.4 | BRACKETS | 2.5e-02 / 5.0e-02: FAIL | 1.1e-31 |
| 1e+13 | instant | 1.16e-04 | 1.65e-04 | 9.26e+04 | BRACKETS | 1.5e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+13 | 1e+12 | 7.39e-05 | 1.31e-04 | 9.26e+04 | BRACKETS | 2.6e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+13 | 1e+09 | 7.39e-05 | n/c | 9.26e+04 | BRACKETS | 2.5e-02 / 5.0e-02: FAIL | 6.1e-30 |
| 1e+13 | 1e+06 | 2.29e-06 | 1.66e-03 | 2.64e+03 | BRACKETS | 2.5e-02 / 5.0e-02: FAIL | 1.1e-31 |

G1 is BELOW (the ceiling is under 0.12, so no seed-free route exists whatever X onset does) for H_inf ≤ 1e10 GeV, and for
T_rh = 1e6 GeV up to the primary H_inf. It is BRACKETS everywhere above. No point is ABOVE: Ω_L stays ≤ 1.2e-4 even at
H_inf = 1e13 GeV. n/c means closure K did not complete within its solver budget at that point (the slow-absorption
branch, Γ/H < 10 at onset; 11 of 28). K never decides G1. G2 FAILS at all 28 points for L and C, by 1.8e8–3.6e8 (L)
and 6e8 (C). The ξ = 1/6 control sits 2e28–1e30 below 0.12 everywhere.

## Which inputs the action does not fix
- H_inf, N_e (Y_C ∝ N_e through ⟨|X|²⟩ ∝ N_e), the reheating history T_rh, ξ, and which stochastic patch we live in.
- The physics, not the action, of the X-onset epoch: whether the coherent condensate dissipates at the kinetic rate, by
  the tachyonic window or not at all. Here it is bracketed by L/K/C. The kinetic rate says "promptly".
- Gaps stated, not filled: the crossed channel's RIS-subtracted kernel (×0/×1 bracket, no effect); thermal widths in the
  absorption rate (an O(1) reduction at onset is possible); the relativistic 4→2 rate (the threshold C is used, with the
  frozen μ = 0 rule).

## Checks (`x1_seedfree_abundance.py`; `--mutate` breaks K5)
| check | result | value |
|---|---|---|
| K1 | PASS | dphi=0.0e+00 dX=0.0e+00 bitwise=True |
| K2 | PASS | maxdiff=0.0e+00 states=25 |
| K3 | FAIL | V3 norm 1.5e-12 energy 1.6e-12; V1 norm 5.2e-13 energy 7.0e-06 — V3 exact runs pass (1.5e-12); Codex's one-cell Strang solver drifts 7e-6 in energy over t = 50 at dt = 0.01 |
| K4 | FAIL | Anu2: n=16 0.082 vs n=1 0.079; Anu8: n=16 0.055 vs n=1 0.058; Bnu2: n=32 1.935 vs n=1 3.328; Bnu8: n=32 1.911 vs n=1 3.385 — scenario A at the largest n is limited by the TW sampling floor of κ₄/κ₂² (≈ 0.08); B is limited by phase-aligned cumulant spikes |
| K5 | PASS | max \|TW-exact\|/SEM = 0.77 |
| K6 | FAIL | P32_CSA_p50_s1:5.6e-05 P32_TW_p10_s1:1.0e-04 P32_TW_p50_s1:1.1e-04 P32_TW_p50_s1_dt2:2.8e-05 P32_TW_p50_s2:1.2e-04 P32_TW_p90_s1:3.6e-04 P32_TWkc_p50_ — bounded Verlet oscillation of the vacuum-noise energy at fixed dt = dx/20 (CSA 1.6e-5; dt/2 → 4× smaller); XI16 has E_phys ≈ 0 |
| K7 | PASS | max 5.9e-15 |
| K8 | PASS | sha_equal=True exits=[75, 75, 0, 0] diag_rel=3.3e-14 |
| K9 | FAIL | f0(500) 0.2445 vs 0.8613 (window means 0.6024/0.8027) — 32³ is chaotic past τ ≈ 300: dt/2 gives a different realisation (instantaneous 0.24 vs 0.86, window 0.60 vs 0.80); 64³ window at τ = 2000: 0.470 vs 0.453 |
| K10 | FAIL | eq 1.2e-15 number 9.6e-14 energy 1.9e-02 (max projection/collision 64.8) — equilibrium and number exact; energy moves 2 % because the Hartree mass is self-consistent and the projection was large |
| K11 | FAIL | L1 1.409 (no-evolution 0.071; f0 window 0.72->0.47) — 2↔2 kinetics without the condensate cannot follow TW while the coherent fraction is 0.5–0.7 |
| K12 | FAIL | x1e3 max\|W/Weq-1\| (T>=m/30) 5.57e+04 [diagnostic, only where scaled r4/H>10: 9.33e-15]; x0 \|dW/W\| 1.1e-15 — the dark plasma freezes out near T ≈ m, so ×1e3 rates cannot hold equilibrium down to m/30; where the scaled r4/H > 10 the deviation is 9e-15 |
| K13 | PASS | 1.0e-06 |
| K14 | FAIL | half-line/full-line 0.3708 — the inflation → radiation conformal problem is a half-line one: 0.371 of the full-line formula named in the check |

6/14 PASS (exit 1). `--mutate` (no symmetric-ordering −½ in the TW occupation estimator) breaks K5 (66 SEM) → 5/14.

## What this lane does not show
- No converged bath-formation endpoint: the prototype coherent fraction is unconverged, and production is queued.
- No calculation of the condensate–bath dissipation at the physical hierarchy. L and K agree with each other; C is a ceiling.
- No certified TW non-Gaussian (normalised-cumulant) dynamics. Occupations and coherence are certified at n ≥ 16.
- Nothing about the scalar-carrier → identified-medium bridge (unspecified in the record), structure formation, or the
  self-interaction of the carrier.

## ENQUEUE (not run by this lane; the owner or the coordinator adds these)

Engine `x1_lattice.py` meets `compute_queue/JOB_CONTRACT.md`: SIGTERM/SIGINT → checkpoint at the next chunk (≤ 200 steps,
≤ ~10 s at 256³) → exit 75; `--resume` exits 0 at once if the result exists, else continues from the newest checkpoint;
the evolved state is byte-identical after interruption (K8; also identical for 1 vs 4 threads at 128³), FFT diagnostics
agree to 1e-12 relative; atomic writes (tmp + fsync + os.replace); rolling checkpoint every 20 outputs. Footprint measured
at 128³: peak phys_footprint 0.525 GB (max RSS 1.04 GB); 256³ scaled ×8 = 4.2 GB. est-gb = measured × 1.2.
Checkpoint sizes: 64³ 17 MB, 128³ 134 MB, 256³ 1.07 GB. Done-file = `lattice/<ID>.json`.

```bash
cd <repo root>
L=rebuild_2026_10_22/X1_seedfree_abundance
q() { python3 compute_queue/heavyq.py add --id "$1" --cwd $L --cmd "python3 x1_lattice.py --job $1 $2" \
      --resume-cmd "python3 x1_lattice.py --job $1 $2 --resume" --est-gb "$3" --threads "$4" --priority "$5" \
      --done-file "lattice/$1.json" --note "X1 E1 TW lattice; ckpt $6; lane X1_seedfree_abundance"; }
q X1_E1_N128_TW_p50_s1   "--N 128 --variant TW_full --patch p50 --seed 1 --tau-end 4000 --out-every 10 --threads 4" 0.7 4 249 134MB
q X1_E1_N128_TWkc_p50_s1 "--N 128 --variant TW_kc   --patch p50 --seed 1 --tau-end 4000 --out-every 10 --threads 4" 0.7 4 248 134MB
q X1_E1_N128_CSA_p50_s1  "--N 128 --variant CSA     --patch p50 --seed 1 --tau-end 4000 --out-every 10 --threads 4" 0.7 4 247 134MB
q X1_E1_N128_TW_p50_s2   "--N 128 --variant TW_full --patch p50 --seed 2 --tau-end 4000 --out-every 10 --threads 4" 0.7 4 246 134MB
q X1_E1_N128_TW_p10_s1   "--N 128 --variant TW_full --patch p10 --seed 1 --tau-end 4000 --out-every 10 --threads 4" 0.7 4 245 134MB
q X1_E1_N128_TW_p90_s1   "--N 128 --variant TW_full --patch p90 --seed 1 --tau-end 4000 --out-every 10 --threads 4" 0.7 4 244 134MB
q X1_E1_N256_TW_p50_s1   "--N 256 --variant TW_full --patch p50 --seed 1 --tau-end 3000 --out-every 25 --threads 8" 5.0 8 243 1.07GB
q X1_E1_N256_CSA_p50_s1  "--N 256 --variant CSA     --patch p50 --seed 1 --tau-end 3000 --out-every 25 --threads 8" 5.0 8 242 1.07GB
q X1_E1_N64_TW_p50_long  "--N 64  --variant TW_full --patch p50 --seed 1 --tau-end 20000 --out-every 50 --threads 2" 0.6 2 241 17MB
```

## Files
- `x1_stochastic.py`: R0 reproduction and box zero modes.
- `x1_fock.py`, `x1_tw_reduced.py`, `x1_validation.py`, `x1_valsummary.py`: V0–V3, results in `validation/`.
- `x1_lattice.py` + `x1_lattice_kernel.c`: the E1 TW engine (queue-contract compliant). Prototypes are in `lattice/`.
  Plumbing resume evidence (including a real SIGTERM) is in `lattice_resume/`; K8 reruns it in `lattice_resume_check/`.
- `x1_boltzmann.py`, `x1_handover.py`: E2 and the K11 overlap, in `handover/`.
- `x1_dmc.py`: XΦΦ̄ → ΦΦ for T ≫ m. It is validated to ≤ 0.74 % against Codex's table; results in `x1_dmc_results.json`.
- `x1_relic.py`, `x1_abundance.py`: E3 closures, the E4 network, controls, isocurvature and the map, in `abundance/`.
- `run_*.sh`: the exact batch commands used (single-thread, nice).
