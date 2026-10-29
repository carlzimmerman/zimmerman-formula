# IN1_ic1613_inclination: one near face-on inclination (i ≈ 19–27°) makes IC 1613 consistent with the law on both tracers

Criteria: `FROZEN_CRITERIA.md` (f4d9ab5eea, committed alone, before any script or number); no amendment.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **INCLINATION RESOLVES IC 1613** (canonical and alt, every q_σ)

| | I_σ (stellar σ consistent) | I_HI (HI rotation consistent) | both |
|---|---|---|---|
| canonical, q_σ 0.6 (PRIMARY) | 10–48.5° | 18.5–26.5° | **18.5–26.5°** |
| canonical, q_σ 0.4 / 0.8 | 20.5–50.5° / 10–43° | 18.5–26.5° | 20.5–26.5° / 18.5–26.5° |
| alt, q_σ 0.6 | 10–41° | 18–25° | **18–25°** |

**E at the literature inclinations** (canonical, q_σ 0.6):

| i | E_σ | E_HI | |
|---|---|---|---|
| 48° (Oh+15) | −0.154 | −0.593 | the HI fails |
| 39° (3D BAROLO) | −0.107 | −0.448 | |
| **20°** (independent estimate) | **+0.006** | **+0.081** | both consistent |
| 15° | +0.033 | +0.323 | |

## What changed relative to the record's failure (HO3/RT1)

1. **Stellar mass.** LITTLE THINGS' SED M★ (2.9e7 M☉) replaces X1's 1.9e8. With half the HI counted, the baryons inside
   r₁₂ fall about 2×.
2. **Disc geometry.** IC 1613 is a rotating disc (stellar rotation detected by MUSE 2024). The spherical estimator
   3σ_los² under-counts a near face-on disc's kinetic energy, because σ_los samples mostly σ_z. The disc estimator
   with q_σ = σ_z/σ_R = 0.6 corrects it, and the rotation term is kept.
3. **Inclination.** HI V_rot scales as sin 48° / sin i. **The HI tracer is the one that pins i.** The stellar-σ tracer is
   already consistent at 48° after (1) and (2), at Z ≈ −1.9.

## The prediction this makes

IC 1613 is consistent with the law **only if** its true inclination is ≈ 19–27°.
- Oh+15's fixed 48° is ruled out.
- Their free ring fits (15–85°) and the independent estimate (≈ 20°) allow it.

**Falsifier:** an independent inclination from stellar tracers (the MUSE 2024 analysis provides one; not on disk) or
from deep optical isophotes. **i ≥ 30° keeps IC 1613 a failure.**

## Disclosed

- The inclination is a nuisance parameter. This lane shows the failure is **consistent with a data geometry**; it does
  not confirm the law.
- Literature values are PROVISIONAL web summaries.
- The baryon inputs change from X1's to LITTLE THINGS'. The stellar mass is the largest single lever (FD1, RT1).

## Checks: 4/4

- **K0:** the spherical estimator with X1's baryons reproduces HO3 (−0.5352).
- **K0b:** the HI tracer at 48° reproduces RT1 (−0.5928).
- **K1:** the isotropic disc estimator equals the spherical one.
- **K2:** E_σ rises toward face-on.
- **Rerun:** byte-identical.
- **MUTATE twin** (sin²/cos² swapped): K2 fails, exit 1.
