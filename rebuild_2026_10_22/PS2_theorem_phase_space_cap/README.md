# PS2_theorem_phase_space_cap: RESULT

Frozen criteria: `FROZEN_CRITERIA.md` (898f293122). Script: `ps2_theorem_cap.py`. It runs PS1's preamble read-only and
re-implements Q_prog independently (K3 = 0 against PS1).

Standing rules:
- κ = ½ FITTED.
- Footings canonical / alt are graded separately and never pooled.
- Cold dark energy, not a particle.
- Not "theory closed". Nothing here says the data favour the framework.

## Headline: TRADES | HSE-MISS | CF-FRAGILE (both footings agree on every label; checks 5/5)

By §3 this is the "counts against PT outright" outcome. The cap neither lands on the gas core nor frees the inner band
from c_f.

**Where the cap binds:** 326/326 clusters at both h, all at interior roots and none at the floor. It binds in 0 SPARC
galaxies and 0 group calls, and there are 0 saturations.

**G-15: TRADES (not blind; expected TRADES via G-OUT-M3, and that is what happened).**
- G-IN-Mall: Z −2.41 → −1.65 / −1.43 (PASS). Its pred falls by 16.5 %.
- The only failing cell is **G-OUT-M3: Z +2.11 (h 0.672) / +1.78 (h 0.686), UNDER**. Its pred/meas is 1.15/1.37
  (canonical).
- The other 13 cells pass.
- SPARC (0.0650 / 0.0657) and groups (Z +1.53) are untouched.
- The footings give identical Z. As in X48, the cluster rule is footing-blind on the collapse branch.

**G-HSE: HSE-MISS.** The median Σ_core/Σ_HG on the 106 KT clusters is **1.90** (16–84 %: 1.26–2.82), against a window of
[0.67, 1.5]. The baseline gives 2.56. The cap moves the core a quarter of the way to the gas's own hydrostatic core.

**G-CF: CF-FRAGILE.** G-IN-Mall's Z with the cap off is shown in brackets.

| c_f | G-IN-Mall Z (h 0.672 / 0.686) | pred move vs graded | other cells that fail |
|---|---|---|---|
| × 0.5 | +0.55 / +0.43 (−0.16 / −0.16) | −57 % | G-MID-T3, G-MID-b, G-OUT-M3, all UNDER |
| × 2 | −5.11 / −4.42 (−5.63 / −4.86) | +91 % | G-IN-all, G-MID-T1, G-MID-T3, G-IN-Mall, all OVER |

The cap tracks c_f almost as strongly as the uncapped rule does. The reason is that the progenitor's core is itself set by
η(c_f) Σ_coll, so the bound inherits c_f. **PT does not remove the dependence on the unconverged c_f.**

## Reported, not graded

- **MGAS OUTER terciles (h 0.672):** M1 Z −0.33, M2 −0.62, M3 +2.11. The miss grows with gas mass. This is IB1's open piece
  (an outskirt normalisation tied to M_b), and a core rule does not reach it.
- **Per-bin pred/meas (h 0.672):** 2.81, 1.78, 1.49, 1.28, 1.18, 1.12, 1.21, 0.83. It is still OVER inside ~1 Mpc.
- **Recursive progenitor (one level):** identical to graded (G-IN-Mall −1.65 / −1.43, M3 +2.11). The M/2 progenitor's own
  cap does not bind.
- **Background B:** G-15 TRADES, the same single failure (M3), SPARC 0.0658 / 0.0665.
- **Two-sided anisotropy (bare halos, at 0.1 r₀):** Q_desc/Q_prog is 0.51 / 0.42 / 0.41 at 10¹³ / 10¹⁴ / 10¹⁵ for both
  isotropic and β = 0.5. The anisotropy cancels when it is shared. But for bare M200 / R200 halos the cap does **not** bind
  (ratio < 1). See below.

## Post-result diagnostic (not graded; scratch script, not committed)

For the 326 graded clusters at the baseline Σ, Q_core/Q_prog has a median of **1.33** (16–84 %: 1.23–1.43) with baryons,
and 1.40 cold-only.
- **The binding is mild,** about 1.3×.
- **It does not come from the baryons.**
- **It comes from X43's cluster geometry.** The cold mass is Mfair, spread out to r_ta (median 6.2 Mpc). The same mass
  inside R200 would not bind (the bare-halo item above).

So PT's cluster selection rests on the inherited Mfair / r_ta budget, the one carrying the 5.364 abundance the owner's 10-25
rule flags. It is not a property of the posit alone.

## Checks

| check | result |
|---|---|
| **K0** | PASS: with the cap off, the script reproduces X48 ng 48 to 1e-9. |
| **K1** | PASS: Plummer −3e-12. |
| **K2** | PASS: monotonic on all 652 solver brackets, 0 saturations, root residual ≤ 6.6e-14 over 7873 solves. |
| **K3** | PASS: 0.0 against PS1's `q_form_thm`. |
| **K4** | PASS: 0.69 GB. |
| **MUTATE** | K1 fails (−0.50) and the script exits 1, as required. |

## Reading

The theorem-strength phase-space cap is a real native cluster-only selector: it leaves galaxies and groups alone. But:
- it only trims the cluster cores by ~16 %;
- it inherits c_f through the progenitor;
- its binding depends on the Mfair / r_ta convention.

The inner band then passes, but G-OUT-M3 fails for the IB1 reason. Do not re-try PS-family caps for the inner band. The
remaining lever is still a gas-mass-tied outskirt normalisation without 5.364.
