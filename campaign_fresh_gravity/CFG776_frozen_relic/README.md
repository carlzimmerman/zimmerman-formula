# CFG776: the frozen relic (H-FR). Dead on the framework's own dynamics

**Label: T1 FAIL (Z = 4.3), and the sign is reversed.**
- Cold energy tethered at a galaxy's peak condensed mass does NOT stay after the baryons leave.
- Under the record's collisionless tether dynamics (CFG747), the surplus is expelled within ~50–100 t0, and the expulsion
  **overshoots into a deficit**.
- So H-FR predicts early types −0.08 dex *below* the law, against the observed +0.28 ± 0.083. Every mass, quench time and
  peak factor gives a negative prediction.

**The lasting result: surplus tethered cold energy is dynamically unstable.** Any persistent core excess must live in
something the cubic push does not act on.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (e2863f3ae). Block CFG770–779.
- **Script:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg776.py` (~10 min, exit 0). `CFG776_MUTATE=1` exits 1 as designed.

## D1: what happens to a surplus (sudden loss; units G = a0 = M_now = 1; m/r = 1 is the law)

| p | t (t0) | r = 2 | 5 | 8 | 11 | 25 r_M |
|---|---|---|---|---|---|---|
| 1 (control) | all | 0.999 | 1.001 | 1.000 | 0.999 | 1.000 |
| 1.5 | 50 | 1.051 | 0.993 | 0.799 | 0.810 | 1.176 |
| | 100 | 0.992 | 1.002 | 0.958 | 0.826 | 1.036 |
| | 300 | 0.993 | 1.009 | 0.951 | 0.976 | 0.789 |
| | 3000 | 1.001 | 1.001 | 0.995 | 0.986 | 0.993 |
| 3 | 50 | 0.797 | 0.503 | 0.366 | 0.301 | 1.421 |
| | 300 | 0.880 | 0.569 | 0.417 | 0.331 | 0.194 |
| | 3000 | 0.979 | 0.768 | 0.563 | 0.437 | 0.218 |

The push grows as m², so a surplus is not merely relaxed away: a large one (p = 3) blows most of the cold energy out of the
halo, and the halo then refills only slowly. K1 PASS (control within 1%); K2 PASS (ΔE/E ≤ 3.8e-4). MUTATE (no push): the
relic stays at m/r ≈ 1.1–2.6. The tooth bites, so the erasure is the push's work.

## T1: KiDS early types (pred = −0.027 + Δ; obs +0.280 ± 0.083)
- Clocks: t0 = 41–85 Myr ⇒ n = 94–242 t0 since quenching. KiDS radii sit at 2.3–16 r_M.
- Tacconi p = 1.87 (z_q 1.5; coefficients provisional).
- Headline (log M_b 11.0, τ 10 Gyr): **−0.081 canonical (Z +4.35), −0.079 alt (Z +4.33) → FAIL.**
- Every row gives −0.03 to −0.45. Larger p gives a *larger deficit*.

## T2: UFDs (frozen line |f| ≤ 0.1 at 25 r_M; n capped at 3000)
- **FAIL as frozen.** f = −1.07: a deep **deficit**, not survival.
- The first run's printed label ("relic SURVIVES") was wrong wording. It was fixed in the rerun, with the numbers identical
  (first output kept as `cfg776_firstrun_jsoncrash.log`, which also ends in a JSON serialisation crash, fixed).
- Either way, H-FR cannot explain the UFDs' +0.33 dex.

## Reading
1. **My hand estimate was wrong.** I expected expulsion only at ~1000–2000 t0, because CFG747 reported only late-time
   averages. The D1 tables show it happens at 50–100 t0. The criteria's estimate (borderline FAIL) understated the failure.
2. **The constraint this lane establishes.** Within the tether dynamics, the law is a stable attractor from below *and* from
   above. A surplus is expelled and overshoots. So the extra mass in early types (KiDS, SLACS) and cluster cores (eRASS1)
   **cannot be surplus tethered cold energy.** It must be one of:
   - (a) a component the cubic push does not act on (untethered/free cold energy, as in H-HT / CFG727);
   - (b) uncounted baryons;
   - (c) a change in the law in those systems.
3. **CFG777's frozen-relic assumption for clusters is contradicted.** A pre-run addendum labels its result a
   phenomenological upper bound.

## Disclosures
- Radial shells; sudden loss (gradual loss is not modelled); point-mass baryons; enclosed-mass proxy for ESD.
- Tacconi coefficients are from memory.
- κ fitted; cold energy mass required; not theory closed.
