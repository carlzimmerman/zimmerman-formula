# CFG20 — the Local Group against the target law's edge

Script: `CFG20_lg_edge.py`, about 2 min.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. With the truncation off, H0 fails (rc = 1).
- The main run exits 1, because H1 and control C1b failed.

## The question

Under FG001 the Local Group (MW + M31) is a top-level bound system:
- the law acts on its baryons with **no** external field;
- its phantom ends at the target's density edge, x_e r_ta.

FP1 (committed) puts the LG's zero-velocity radius R₀ at 1.92–2.02 Mpc for the isolated law with no external field, against the observed 0.93 ± 0.12 Mpc. The derivation chain needed the web's external field to bring it down, and FG001 removes that field. So the edge is the only thing left that can.

## The model

The model is FP1's own shell integrator, exec'd read-only, with the truncation added.
- Test shells start on the Hubble flow at a = 0.02 and move in the LG's field plus Λ.
- At each epoch the edge is r_e(a) = x_e r_ta(a). Here r_ta is the law's untruncated turnaround radius at Δ_ta(z), CFG4's convention, the same one in which KiDS's floor is expressed.
- Inside r_e the law acts. Outside it the enclosed mass stays M_e(a), CFG4's density edge.
- LG baryons: FP1's 1.145e11 and 1.72e11 M☉.

## Results

**Controls**

| check | result |
|---|---|
| C1: FP1's committed E1 control (ν_RAR, 1.145e11) | 1.9290 / 2.0214 Mpc, **pass**. The chain kernel's R0_e0 of 1.9246 is also reproduced |
| C1b: the truncated integrator with no truncation equals FP1's, to 1e-6 Mpc | **FAILED as declared**: 2.7e-6 |
| C1c (reported; added after the first run): the same, fed FP1's tabulated ν | 0.0. C1b's residual is FP1's interpolation table, not the physics |
| H0: the truncation lowers R₀ by more than 0.1 Mpc | pass, in every case |

**R₀ in Mpc against the edge** (canonical P2, 1.145e11; the other rows follow the same pattern):

| x_e | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.34 | 0.40 | 0.50 | 1.0 | ∞ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R₀ | 0.685 | 0.857 | 0.979 | 1.076 | 1.159 | 1.231 | 1.283 | 1.355 | 1.459 | 1.814 | 1.925 |

**H1: at KiDS's self-consistent floor (CFG16) the LG's R₀ is within 2σ (≤ 1.17 Mpc).** **FAILED in every case.**

| row | R₀ at KiDS's floor | σ above 0.93 | largest x_e the LG allows | KiDS floor |
|---|---|---|---|---|
| canonical P2, 1.145e11 | 1.285 | 3.0 | 0.258 | 0.341 |
| canonical P2, 1.72e11 | 1.422 | 4.1 | 0.190 | 0.341 |
| canonical ν_mono, 1.145e11 | 1.300 | 3.1 | 0.252 | 0.348 |
| canonical ν_mono, 1.72e11 | 1.440 | 4.3 | 0.185 | 0.348 |
| alt P2, 1.145e11 / 1.72e11 | 1.345 / 1.490 | 3.5 / 4.7 | 0.224 / 0.165 | 0.340 |
| alt ν_mono, 1.145e11 / 1.72e11 | 1.359 / 1.505 | 3.6 / 4.8 | 0.220 / 0.160 | 0.345 |

## Standing

**A new conflict for the target law (CFG4 + FG001).**
- The Local Group's zero-velocity radius allows a phantom edge of at most x_e ≈ 0.16–0.26.
- KiDS's isolated lenses need at least 0.34 (CFG16, self-consistent bias).
- At KiDS's floor the LG comes out 3.0–4.8σ too large.

The truncation helps: R₀ falls from 1.92 to 1.28–1.51 Mpc. It does not help enough.

**Readings that make it worse, not better:**
- **The pair as two separate phantoms.** The LG has not relaxed; MW and M31 are approaching for first pericentre. Giving each galaxy its own phantom out to its own edge makes the sum larger than one pair phantom, because the phantom is sublinear in M_b.
- **The chain's external field.** FG001 removes it for top-level systems by construction.

**A pattern worth recording.** KiDS's isolated-lens signal at 0.3–1 Mpc is the one datum that wants the phantom to extend far. Everything else wants it shorter:
- the cold budget (CFG11–17), at the margin;
- the collapse's own splashback (FG016, x_e 0.18–0.27);
- now the LG timing (≤ 0.16–0.26).

The minimal conflict of the target law is **KiDS's large-radius signal against the framework's mass at 0.3–1 Mpc**.

**Not claimed:**
- that KiDS is wrong;
- that the LG's observed R₀ is final. The adopted error is 0.12 Mpc.

Nothing here says the theory is closed.
