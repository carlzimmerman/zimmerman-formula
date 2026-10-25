# DF1_dwarf_floor_origin: no named-physics origin of the faint-dwarf extra survives

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (3ef24ec383, committed alone before any script; **POST-HOC**: X24's c₀
and X28's n were known, disclosed in §7). κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², scored separately and never
pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework or ΛCDM. Every number
comes from `df1_dwarf_floor_origin.out` / `_results.json`.

## Question

The faint-dwarf extra is described empirically as a velocity floor, σ² = σ_iso² + c₀². Its cross-system form is
g_floor ∝ r₁₂^(−0.8), and it is mass-driven, not host-driven. Is there a physical origin whose shape follows from named
physics with no fitted shape constant? Twelve ideas were screened against the record (criteria §1). Seven forms were
graded on X1's 82 dwarfs (13 LG field for calibration; 61 hosted H plus 8 MW classical graded).

## Verdict (frozen rule): NONE SURVIVE. All seven are RULED OUT on both footings.

| candidate | shape (n, m) | T1 Δχ²_shape can. / alt (pass ≤ 5.99) | T2 out of sample | T3 physical normalization | verdict |
|---|---|---|---|---|---|
| P0 Γ = 0: Chaplygin / logatrope unified dark fluid (= Burgers) | (0, 0) | +230.0 / +218.0 | FAIL: UFD Z +3.3 / +4.0 | **VIOLATED**: forest c_s 58 / 29 km/s against the 13 km/s gate | RULED OUT |
| **P1 Γ = 1: isothermal medium (= X24's floor)** | (1, 0) | **+17.5 / +13.4** | FAIL: UFD Z −3.9 / −3.0 | PASS (c₀ 4.59 / 4.05 km/s, below the gate) | RULED OUT |
| P4/3 Γ = 4/3 | (2, 0) | +369.9 / +326.6 | FAIL: UFD Z −8.2 / −7.7 | PASS | RULED OUT |
| P5/3 Γ = 5/3 adiabatic | (5, 0) | +1046.6 / +836.4 | FAIL | PASS | RULED OUT |
| TK Kolmogorov cascade | (1/3, 0) | +74.8 / +73.4 | **PASS** (all \|Z\| < 2; χ²_H 210 / 244) | NA | RULED OUT |
| SI secondary infall on the baryon seed | (5/4, 3/4) | +1068.7 / +905.7 | FAIL (field calibrates it to zero) | NA | RULED OUT |
| IMF remnant-loaded stellar mass | E = s log F | +779.3 / +693.3 | FAIL | PASS as frozen (see below) | RULED OUT |

**What the data want.** The free power law on all 82 gives, with m = 0, n = 0.78, 95 % [0.68, 0.88] (canonical) and
n = 0.80, 95 % [0.70, 0.90] (alt). With m free, the best fit is n ≈ 0.92 and m ≈ +0.05. There is **no stellar-mass dependence
at fixed r₁₂**: the mass trend is entirely the size trend plus the fact that σ_iso is small in small dwarfs. In polytrope
language, the data want **Γ = 0.88 [0.81, 0.94] / 0.89 [0.82, 0.95]**. That is softer than isothermal and far from every
named equation of state (0, 1, 4/3, 5/3).

**Checks 9/9 PASS** (exit 0, 76 s, 0.18 GB, one thread):
- **K0** reproduces X28's n = 0.78 [0.73, 0.83] / 0.80 [0.75, 0.85] with X28's own method, and X24's c₀ 4.587 / 4.051 km/s.
- **K1** P1's χ²_H = 217.0 / 194.8 equals X28's F_v.
- **K2** on synthetic Kolmogorov data, T1 passes TK (Δχ² +0.69 / +0.67) and rejects P1 (+86 / +73). So the test has power, and
  it can pass a true shape.
- **K3** nesting holds. **K4** memory is under the limit.

**MUTATE** (`DF1_MUTATE=1`, r₁₂ permuted in the g_x term) fails K0 and K1 (n → −0.25), exit 1.

## Reading

- **The equation-of-state ladder fails.** A hydrostatic cold medium that fills the stars' radius has n = Γ/(2 − Γ). No named
  Γ lands in the band.
  - **Γ = 0** (a unified Chaplygin-type dark fluid, c_s² ∝ 1/ρ) is also killed by cosmology: the strength the dwarfs need
    gives c_s = 58 / 29 km/s in the Lyman-α forest, against X22's 13 km/s gate.
  - **Γ ≥ 4/3** puts the extra far too steeply into the smallest systems, and the UFDs are overshot by 0.4–2 dex.
- **The isothermal floor is the nearest named form, and it is still not the answer.** It is excluded by the shape at
  Δχ² 17.5 / 13.4 and by the UFD overshoot (Z −3.9 / −3.0), which is X24's known failure.
  - Post-hoc caveat, not graded: the reference fit has χ²/dof = 7.3 / 7.9, so the per-system errors understate the
    scatter. If Δχ² is rescaled by that factor, P1's shape penalty drops to 2.4 / 1.7, which would pass T1. P1 would then
    be PARTIAL rather than RULED OUT. It still fails T2 through the UFDs, so the lane result (no survivor) is unchanged.
    TK stays excluded under the same rescaling (10.2 / 9.3).
- **Kolmogorov turbulence is the mirror image of isothermal.** Its n = 1/3 is too shallow, so it under-supplies the
  compact systems relative to the diffuse ones in the shape test. But out of sample, calibrated on the field, it leaves no
  H class above 2σ. That happens because it puts more extra into the diffuse M31 dwarfs. It makes Crater II (+0.53
  predicted against −0.44) and Antlia II (+0.47 against +0.06) much worse.
- **Infall onto the baryons and remnant-loaded IMFs are mass-keyed, and the data show no mass key** at fixed size
  (m ≈ 0.05). The field calibration drives both to zero.
  - The IMF needs Υ multiplied by 14 / 11 in the UFDs and 31 / 22 in "M31 others", against the record's bound of 2.
  - The frozen T3 rule did not fire, because the bootstrap sd of the median F_req is very wide (12 / 10 for the UFDs). The
    candidate is excluded by T1 and T2, not by T3.
- **Excluded at screening, with reasons in criteria §1:**
  - Relaxation, perturber heating and internal redistribution: the deep-law virial theorem makes σ a function of M alone.
  - Ambient pressure: stars are collisionless.
  - Quantum pressure: it needs a particle.
  - SM neutrinos: they fall 16 orders of magnitude short of the phase-space limit.
  - Retained warm gas.
  - A law-boosted clump: CFG888 says the record has no self-boost.
  - Any function of g_bar alone.
- **Crater II and Antlia II.** Every additive form with n < 2 makes them worse, as X24 found. Only the steep forms (Γ ≥ 4/3,
  SI, IMF) leave them alone, and those forms fail everywhere else.

## Parameter-space consequence

The second blank on the cold-sector recipe card stays blank:
- c₀ ≈ 4–4.6 km/s remains a phenomenological constant;
- its shape (n ≈ 0.8, Γ ≈ 0.88, no M★ key) now also excludes every named single-EOS medium, a Kolmogorov cascade,
  baryon-seeded infall and remnant IMFs.

A future origin has to supply a velocity scale that **rises weakly with system size** (σ_x² ∝ r^0.2) and ignores M★ at fixed
size. It must also do so without a density-keyed sound speed strong enough to break the forest.

## What this does not show

- **A5 is load-bearing.** The cross-system mapping assumes each dwarf's extra component scales with r₁₂. An origin whose
  scale is set by something else (formation epoch, environment history) is not tested.
- **Not blind.** These are the same 82 systems that defined the description, and the target was known (A15, A16).
- **Not tested here:** composite forms, such as an isothermal medium with a weak temperature–density anti-correlation
  (Γ ≈ 0.88). Fitting Γ would be a knob scan. Deriving it would need new physics, such as the sibling dark-energy-heater
  lane (DH1).

## Files and run

`FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `df1_dwarf_floor_origin.py` → `.out`, `_results.json`; `*_MUTATE.*`.

    OMP_NUM_THREADS=1 python3 df1_dwarf_floor_origin.py              # exit 0, 9/9
    DF1_MUTATE=1 OMP_NUM_THREADS=1 python3 df1_dwarf_floor_origin.py # exit 1, K0/K1 fail

Inputs are read only: X1's per-system CSV, the X24 and X28 JSON, and CFG257's binary table. Nothing was downloaded.
