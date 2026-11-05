# UD1: the a0 law on AGC 114905: FAILS at the measured inclination (no clean label: two checks tagged)

κ = ½ FITTED; not theory closed; footings never pooled; not blind; one galaxy excludes nothing (owner rule). Criteria:
FROZEN_CRITERIA.md (8fe67ae925), AMENDMENTS.md A1 (f7b9430d35) and A2 (dc36beaadf), all committed before any law
number. Run: `python3 ud1.py law` and `python3 ud1.py MUTATE` (about 13 s each); outputs ud1.{out,json},
ud1_MUTATE.{out,json}.

## Inputs

Mancera Piña+2024 (arXiv:2404.06537), which supersedes 2022 with an optical inclination: i0 = 31° ± 2°, D = 78.7 Mpc.
V_circ is read as exact path coordinates from the authors' vector figures (inputs/, sha256 in the commit). The two figures
agree to 0.00 km/s. Five rings: R 1.1-9.9 kpc, V_circ 10.8, 18.1, 24.8, 27.2, 26.9 ± 1.8-2.2 km/s. Baryons are built
from 2024's published functional forms (stars 8.3e7, gas 1.22e9 Msun; 94 % gas). Outer V_bar is 21.4 km/s. The
outermost point sits at g_N ≈ 0.016 a0, deep below a0.

## Grade (published i0, published M*)

| footing | a0 (m/s²) | V_law, outer point | χ²/5 | label | inclination escape |
|---|---|---|---|---|---|
| canonical | 9.3603e-11 | 62.2 km/s (data 26.9) | 843.6 | **FAIL** | needs i 12.9-15.6°: **NOT RESCUED** (7.7 σ_i below i0) |
| alt | 1.1312e-10 | 65.1 km/s | 995.8 | **FAIL** | needs i 12.3-14.9°: **NOT RESCUED** (8.1 σ_i) |

- M* ± 1σ: χ² 823-1020. EFE at an assumed g_e = 0.03 a0: χ² 61-65, still FAIL. The EFE rows are reported, not graded.
- Paper-consistent inclination variant (A2, reported only): needs i 10.3-13.7°.
- Secondary, 2022 figure (i0 32° ± 3°, D 76 Mpc, errors include its inclination Monte Carlo): χ² 191 and 221 → FAIL;
  the escape needs i 8.1-16.9° → NOT RESCUED. Never pooled.
- Newtonian baryons alone (reported): χ² 55/5 on 2024, which also fails. On 2022 Newton gives χ² 3.2, CONSISTENT.

## Checks

- K0z ring-sum potential vs Freeman disc: 0.5 %, PASS.
- K0a: the paper's plotted V_*, V_gas and sum (D 80.27, i 35.86) are reproduced to medians of 1.5, 1.2 and 0.9 %. PASS.
- **K0b: the paper's plotted MOND curve (a0 1.2e-10) is reproduced to a median of 0.0301 against a line of 0.03: FAIL by
  0.0001.** With the gas profile cut at 40″ it was 0.029. The line is not moved. A 3 % curve offset cannot move a
  χ² of 840.
- K0c: the paper's "i ≈ 12°" rescue comes back at 11.5°. PASS.
- K1: no optimiser in the script. PASS. Rerun: byte-identical.
- **MUTATE (ν ≡ 1) as frozen FAILS**: the check required Newton to fit worse than the law. Newton fits better, χ² 55 vs
  844. This is not a wiring fault, since K0b and K0c reproduce the paper's own MOND curve and rescue angle. The check
  assumed the law fits, so here it inverts.

Per §6 a failed check means no clean label. The tags are [K0b 0.0301 vs 0.03] and [MUTATE INVERTED]. Neither changes
the size of the miss: the law over-predicts the outer rotation by a factor of 2.3. The only way out is an inclination
7.7-8.1 σ below the measured one.

## Context (read, not graded)

This matches the authors' own MOND comparison (a0 must be ~60× lower, or i ≈ 12°). Banik+2022 (arXiv:2204.06569) argue
the inclination is overestimated. arXiv:2408.05269 claims gas-rich UDGs are consistent with the BTFR and MOND; it was
not checked here. Nothing here is a verdict on a theory.
