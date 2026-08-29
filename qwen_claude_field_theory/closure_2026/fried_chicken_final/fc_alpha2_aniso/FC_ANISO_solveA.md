# PHASE 2 route-A — FC-AeST + c_2* preferred-frame alpha_2 (direct anisotropic O(w^2) solve)

**Script:** `fc_solveA_setupM.py` (self-checking, `ALL GATES PASS`, exit 0, ~107 s).
**Output:** `fc_solveA_setupM.out`.

## Bottom line (honest, load-bearing labels)

- **`alpha_2 = 1/lam_s + 2/(K_B lam_s^2) + O(lam_s^-3)`** at the Maxwell corner, in the massless
  (Solar-System / PPN) limit — **DERIVATION** (direct coupled `{E_mn, E_Ai, E_phi}` O(w^2) solve;
  leading coefficient `= 1` verified to ~0.4 %, K_2-independent, over K_B∈[1e-4,0.3]).
- **`alpha_1 = -4 K_B + O(1/lam_s)` → `-4 K_B`** — **DERIVATION** (reproduces the established
  vector value in the scalar-decoupling limit; the scalar correction is 1/lam_s-suppressed).
- **Screening is REAL and DERIVED:** the scalar's preferred-frame contribution is `~1/lam_s`,
  **NOT** O(1). This settles the decisive `FC_AEST_STATUS` gate — the retracted worry ("screening
  the static profile ≠ suppressing the 1PN coefficient") is resolved *in favour of suppression* by
  the actual 1PN solve. `lam_s = J_Y`, and `beta_0 = 1/lam_s`, so `alpha_2 ≈ beta_0` exactly the
  proposed-then-retracted form — here **verified**, not assumed.
- **Physical verdict (CONDITIONAL PASS):** with `lam_s = J_Y = 2 g_bar/a_0 ≈ 1.3e8` at 1 AU
  (typeII F3, **EXTERNAL-INPUT**), `alpha_2 ≈ a_0/(2 g_bar) ≈ 8e-9 < ~1e-7` (lunar/planetary bound)
  — cleared by ~1 order. The pass **hinges on** evaluating the environment-dependent preferred-frame
  parameter at the *local* J_Y (huge in the Solar System), not the frozen cosmological `lam_s=1`
  (where `alpha_2 ≈ 20`, K_2-dep, would kill). This J_Y identification is EXTERNAL-INPUT.

`basis = DERIVATION` for the number; the viability conclusion carries one EXTERNAL-INPUT
(`lam_s=J_Y=2g/a_0`) and is honestly CONDITIONAL on it.

## The machinery, and why it is trustworthy (validation gates, all PASS)

Setup **M** (the GR-gate-validated realization): aether **at rest** `A^mu=(1,0,0,0)`, scalar
background `phi=Q_0 t` (so `Q=Q_0`, `Y=0`), **matter source moving at w** with rigid retardation
`omega=k.w`; full generic 10-component `h_{mn}`; unit constraint `A.A=-1` solved **algebraically to
O(eps^2)** (`dA_0` at O(eps) *and* `b_0` at O(eps^2) — the latter was the missing piece that made
the O(w) sector diffeo-consistent; without it the scalar EOM is inconsistent by one equation);
**harmonic gauge** `K^mu hbar_{mu n}=0` imposed *after* the field equations; **gauge-invariant
extraction** `alpha_1=-2(a+b)-(4gamma+4)`, `alpha_2=-(2b+d)-1` (folds g_0i's `b` into g_00's `d`).

| Gate | Result | Meaning |
|---|---|---|
| **GR** (dark off) | `(a,b,d)=(-4,0,-1)`, `alpha_1=alpha_2=0` | reproduces `fc_aniso_grgate.py` (16/16) exactly |
| **EA Maxwell corner** (scalar off) | `alpha_1=-4K_B`, **`alpha_2=0` EXACTLY** ∀K_B | matches Foster-Jacobson / `fc_maxwell_vs_c4_corner` / route-B `fc_solveB_partA_fj` |
| **static Ghat** | `Ghat/Gt = 40/39 = 2/(2-K_B)` | matches typeII `Ghat=Gt/(1-K_B/2)` |
| **large lam_s** | `alpha_2·lam_s → 1`, `alpha_1 → -4K_B` | scalar decouples correctly at large kinetic |
| **consistency** | rotational (`h_02/w2=h_03/w3`) + `c_F,d_F` fit across 3 w-samples | the anisotropic solve is valid (the isotropic ansatz FAILED exactly this) |

The two nontrivial *known* gauge-invariant answers (GR `=0`; EA `alpha_1=-4K_B, alpha_2=0`) are both
reproduced by the *same* extraction that yields the AeST number — that is what licenses the AeST
value.

## The c_2* sign, resolved

Route-B / `fc_ctensor_map` use `L_EA = -(c1 T1 + c2 T2 + c3 T3 + c4 T4)`, `T2=(∇·A)^2`. The Maxwell
corner (`alpha_2^EA=0`) is EA `c2 = +K_B/(1-2K_B)`, i.e. a **Lagrangian term
`-K_B/(1-2K_B)(∇·A)^2`**. In this file's `+c2s(∇·A)^2` convention that is `c2s = -K_B/(1-2K_B)`
(`maxwell_c2s`), where the direct solve independently finds `alpha_2^EA=0` — consistent with the
committed EA reference. (Note: an overall EH sign — genuine `√-g R = -(1/2)h·G1[h]` — was calibrated
against GR and the EA `alpha_1=-4K_B`; a sign slip there flips `alpha_1 → +4K_B`, caught by the gate.)

## The "two channels" (task §Extraction) — honestly

The originally-specified **g_00-ALONE** channels (`P_A` from the `w^2 U` coeff `c`; `P_Aparallel`
from `(w.x)^2U/r^2` coeff `d`) **disagree even for GR** (test point: iso `≈ -5.29`, aniso `≈ -1.15`)
— this is the GR gate's `[I1]` finding: `g_00` alone is gauge-dependent and `c` is source-convention
dependent (GR `c=5` Fourier vs `4` oracle). The **fix**, and the value reported, is the single
gauge-invariant `alpha_2=-(2b+d)-1` that folds in the g_0i coefficient `b`. `channels_agree=AGREE` is
reported in the sense of `[I2]` ("the two determinations are the SAME gauge-invariant"): the
anisotropic solve is internally consistent (rotational + multi-sample fits all pass), which is the
meaningful version of the test the isotropic ansatz could not satisfy.

## Numbers (from `fc_solveA_setupM.out`)

```
alpha_2 * lam_s   (K_B=0.05, K2=1, masses<<1):
  lam_s=1     -> 20.24        lam_s=100  -> 1.381
  lam_s=10    -> 4.499        lam_s=1000 -> 1.038 ;  lam_s=1e4 -> 1.004   (-> 1)
alpha_1(lam_s):  -4.10 (1) -> -0.2078 (1e3) -> -0.2008 (1e4)  (-> -4K_B=-0.2)
C(K_B)-1 = 2/(K_B lam_s)  (finite-lam_s), i.e. C -> 1 universally ; K2-independent.
```

## Residual open / caveats

- The *identification* `lam_s = J_Y` (local MOND-function derivative) and its Solar-System value
  `J_Y = 2 g_bar/a_0` are **EXTERNAL-INPUT** (typeII). The frozen-candidate `lam_s=1` is the
  *cosmological/FLRW* value; the preferred-frame bound is a *local* Solar-System test and must be
  evaluated at the *local* (large) J_Y. If instead one insists `lam_s=1` applies locally, `alpha_2≈20`
  kills the theory. The physics (environment-dependent PPN parameters in MOND) favours the local
  reading, giving the ~1-order-of-magnitude pass.
- Extraction uses harmonic gauge; gauge-invariance is inherited from the two validated limits (GR, EA)
  rather than from an independent dual-gauge AeST solve.
- The J^i sector is retained to O(eps) and J^0 to O(eps^2) (sparse `A_bg=(1,0,0,0)`); the O(eps^2)
  action is complete and diffeo-consistent (verified by the rank test after the `b_0` fix).
