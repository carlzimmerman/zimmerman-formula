# T12 — the epoch-elasticity of completeness

**The sensitivity face of the settling law:** how hard does completeness
respond to formation epoch? The law f = 1 − e^{−Γt} answers exactly, with
Γ and t cancelling:

    ε(f) := d ln f / d ln t = Γt·e^{−Γt}/(1 − e^{−Γt})
          = (1 − f)·[−ln(1 − f)]/f          — a pure function of f alone

## Results (6/6 checks PASS, rc 0; MUTATE flips C1–C4, rc 1)

| f (clock) | ε | meaning |
|---|---|---|
| 0.14 (MW floor, 30 kpc) | **0.9265** | near-linear branch: the MW is young in settling terms — 1% longer history ⇒ ~0.93% more settled |
| 0.60 (groups, R500) | **0.6109** | mid-curve |
| 0.43 (clusters, R500) | **0.7451** | clusters respond ~1.22× MORE per unit log-epoch than groups (0.7451/0.6109 = 1.2198) |

Asymptotes verified: ε(0.01) = 0.995 (→ 1 as f → 0, the linear branch);
ε(0.99) = 0.047 (→ 0 as f → 1, saturation). Monotone decreasing:
max dε/df = −4.9e-4 on [0.01, 0.99].

## The three-clock read: one λ everywhere

At the R500 convention (ρ = 500ρ_crit(z), z_c = 0.75 → t_c = 6.7 ± 1.0
Gyr from the z₁₄ ≈ 0.8 formation epoch; z_g = 0.15 → t_g = 11.9 ± 1.5
Gyr), the two solid clocks recover the coupling independently:

    λ_c = 0.0290 ± 0.0142   (cluster clock)
    λ_g = 0.0376 ± 0.0161   (group clock)
    JOINT [0.0215, 0.0432]  →  contains CFG382's λ = 0.028

**The MW-calibrated coupling is confirmed by both cluster-scale clocks**
within errors — the settling law's absolute scale is not free. The MW
floor itself is deliberately NOT re-fitted here: CFG382's floor
calibration used the diluted supply-ball density (a different
convention); the lane registers that as a limitation, consistent with
CFG382's own PARTIAL verdict.

## Falsifier (registered)

Epoch-split completeness stacks (split by red-sequence age / halo
concentration / formation redshift): measured d ln f/d ln t must follow
the curve ε(f) = (1−f)·[−ln(1−f)]/f, with the ordering
ε(0.43) > ε(0.60). A flat sensitivity kills the exponential law's
empirical face (the linear branch would predict ε ≡ 1 — exactly the
MUTATE).

## CFG382 cross-reference

CFG382: groups 0.722, clusters 0.714 (both at τ since z = 2, equal
epochs) — the cluster FAIL that sank the local-density reading. T11:
the 0.43/0.60 gap IS the epoch gap (ratio 0.6135). T12: the sensitivity
of that reading is the curve above — and with the corrected epochs the
cluster and group clocks agree with each other and with λ = 0.028.
CFG382's PARTIAL verdict stands on its own criteria; the positive law
furnishes the resolution it lacked.

## Lean certificate (`../lean_certs/cert_epoch_elasticity.lean`)

`epoch_elasticity_closed`: given the law 1 − f = e^{−x} (x = Γt),
x·e^{−x}/(1−e^{−x}) = (1−f)·[−ln(1−f)]/f — Γ and t cancel exactly.
rc 0, zero sorry, axioms = {propext, Classical.choice, Quot.sound}.
The derivative step (d ln f/d ln t) rides in the lane (house pattern).

## Bottom line

The law's sensitivity curve is fixed, mass- and density-independent, and
killable. And the absolute scale passes a three-clock audit: the same
λ that the MW floor was fixed by is independently recovered by the
cluster and group clocks at the R500 convention. One coupling, three
clocks, all agreeing.