# CFG313 — B's cold-mass rule with a framework-native collapse mass

- **Criteria:** `FROZEN_CRITERIA.md`, committed before any score (c64a87dd0).
- **Scripts:**
  - `cfg313_native_rescore.py`, about 10 s. Main run: 8/8 checks pass, exit 0. MUTATE run: 8/9, exit 1. The failure is the predicted one (below).
  - `cfg313_preflight.py`, about 3 s. It reproduces the frozen hand pre-flight: 3/3. Its MUTATE run gives 2/3, failing P2 by design.
- **Outputs:** `.out` and `_results.json` for each script, plus the `_MUTATE` pairs.

## Bottom line

**With M_c = M_b/f_b the rule never switches on.** The native mass is the framework's own: the cold component and the baryons collapse together at the cosmic ratio, f_b = 0.157126 (CFG35's `FB`, Planck 2018 ω_b and ω_c).

The rule's leftover is f_ex = max(0, 1 − M_ph,edge/[(1 − f_b) M_c]). The native cold share is (Ω_c/Ω_b) M_b = 5.36 M_b. The law's own phantom inside the edge is 50 to 6700 M_b at every mass scored, so f_ex = 0 for every object under either profile:
- V1 is the committed Dutton–Macciò NFW, whose c(M) comes from ΛCDM simulations.
- V2 is a parameter-free isothermal truncated at the law's own turnaround radius.

The native rule is therefore the bare law, exactly, in every population. Inertness margin: the cold share would have to be 7.0× larger before any scored object is touched (M_b = 9.5e11, canonical). CFG35 already noted that the cosmic share of today's baryons is "only a floor"; this lane makes that floor the input and scores it.

The ΛCDM collapse masses are 1–5 decades larger than the native mass:

| object | native / Moster | native / Mandelbaum |
|---|---|---|
| ultra-faint | 6e-6 to 6e-5 | — |
| classical dwarf | 1e-3 to 5e-3 | — |
| L* galaxy | 0.16 | 0.14–0.32 |
| massive elliptical | 0.010 | 0.039 |

All of the rule's effects, good and bad, came from those larger masses.

## Table (offset in dex, then z on the canonical | alt footings)

| population | law alone | committed rule (Moster / Mandelbaum + NFW) | native rule (V1 = V2) | gate: committed → native |
|---|---|---|---|---|
| MW ultra-faints | +0.325 (+3.77 \| +3.55) | −0.059 (−0.41 \| −0.41) | +0.325 (+3.77 \| +3.55) | **PASS → FAIL** |
| MW classical | +0.027 (+0.32 \| +0.09) | −0.118 (−1.78 \| −1.90) | = law | pass → pass |
| M31 Collins+13 | +0.064 (+0.78 \| +0.55) | −0.024 (−0.22 \| −0.15) | = law | pass → pass |
| M31 LVD | +0.044 (+0.60 \| +0.42) | −0.107 (−2.67 \| −2.66) | = law | **FAIL → PASS** |
| LV field dwarfs | −0.044 (−0.60 \| −0.85) | −0.105 (−3.47 \| −2.70) | = law | **FAIL → PASS** |
| UGC 2487 | +0.064 (+0.90 \| +0.68) | −0.075 (−1.05 \| −1.02) | = law | pass → pass |
| Di Teodoro four S0 | +0.004 (+0.05 \| −0.17) | −0.105 (−0.80 \| −0.75) | = law | pass → pass |
| Di Teodoro all 15 (reported) | −0.028 (−0.43 \| −0.69) | −0.057 (−0.71 \| −0.85) | = law | pass → pass |
| SLUGGS, h50 masses (19) | +0.080 (+3.28 \| +2.67) | +0.007 (+0.39 \| +0.10) | = law | **PASS → FAIL** |
| SLUGGS, JAM masses, γ = 3 (CFG55) | +0.097 (+3.99 \| +3.65) | +0.046 (+2.58 \| +2.60) | = law | FAIL → FAIL |
| SLUGGS, SLUGGS masses (16) | +0.077 (+2.75 \| +2.23) | +0.007 (+0.36 \| +0.12) | = law | **PASS → FAIL** |
| SLUGGS, JAM masses, literature γ (CFG111) | +0.082 (+3.60 \| +3.22) | +0.028 (+1.55 \| +1.64) | = law | **PASS → FAIL** |
| X-ray ellipticals | +0.280 (+1.70 \| +1.58) | +0.125 (+1.04 \| +1.03) | = law | pass → pass |
| Ogle super spirals (reported) | +0.107 (+1.42 \| +1.25) | same | = law | — |
| SPARC dwarfs / log M★ ≥ 10, fraction with d log v < 0.03 | 100% / 100% | 100% / 98% | 100% / 100% | pass → pass |
| SPARC rms (CFG39) | 0.1003 | 0.1012 (+0.0009) | 0.1003 (+0.0000) | pass → pass |

Gated rows passed: law alone 7/12; committed rule 9/12; native rule 7/12.

## Controls

- **C1 passes.** With the committed masses, the hooked harness reproduces 130 committed numbers from CFG45, CFG58, CFG55, CFG111 and CFG39. The worst deviation is 9e-10 of tolerance.
- **C2 passes.** With M_c → 0, every rule row equals the law row (31 comparisons, deviation 0).
- **C3 passes.** Over 13,852 native evaluations, M_c f_b/M_b = 1 to 2e-16, and V2 has the declared shape.
- **MUTATE (f_b × 0.5) fails, as the pre-flight predicted.** No population moves (largest shift 0.0 dex). The cold share rises only to 11.7 M_b, which is still below every edge phantom, so the specified check "every population shifts in the predicted direction" fails. That failure is kept.

## Caveats

- **The UFD error recipe.** The primary error maps CFG42/45's collapse-mass floor (1e8–1e10, i.e. ×0.1–×10 about the clamp) onto ×0.1–×10 of the native mass. Under that mapping the native UFD error equals the law's, giving 3.77σ.
  - With CFG45's floor **values** substituted verbatim, the UFD row would read +1.93 | +1.90σ (error 0.168 dex).
  - That variant injects Moster-scale masses into the error budget, so it is not native. It is reported only.
- **The baryons.** M_b is each lane's own baryon inventory: stars plus cold gas, and no hot gas for SLUGGS or the X-ray ellipticals.
  - Adding the hot halos of the massive ellipticals would raise their native M_c.
  - It would not switch the rule on unless it raised M_b by about 7× (the margin k*).
- **What this does not test.** These rows are the rule's only. The law-only failures (MW ultra-faints 3.5–3.9σ; SLUGGS 4.0σ with JAM masses) use raw inputs and are unchanged; here they reappear as the native rule's values.

## Reading

With a framework-native, parameter-free collapse mass, B's derived cold-mass rule is inert: it adds nothing anywhere. Its two fixes (the ultra-faints, SLUGGS) and its two breaks (M31 LVD, LV field dwarfs) were both effects of the ΛCDM collapse masses. Without those inputs, B stands on the bare law:
- it passes the classical satellites, M31, the field dwarfs, SPARC, the discs and the X-ray ellipticals;
- it fails the MW ultra-faints (3.8 | 3.5σ) and SLUGGS (3.3σ with h50 masses, 4.0σ with JAM masses, 3.6σ with literature slopes).

The cold mass is still required (the native rule assigns the cosmic share), and no dark-matter particle is added. κ = ½ remains fitted. Nothing here says the theory is closed.
