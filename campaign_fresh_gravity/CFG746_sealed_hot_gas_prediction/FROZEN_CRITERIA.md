# CFG746 — sealed hot-gas prediction of the selector for massive quiescent galaxies (frozen criteria, committed alone)

Block CFG740–749. Written before any CFG746 number. κ = ½ fitted; both footings; the cold energy's mass is required; no particle
species; not theory closed. **Predictions, not results.** No SZ or X-ray profile data are read.

## What is sealed
CFG745's selector (C = k M_hot) supplies the KiDS early-type shortfall (C3) only if quiescent galaxies with log M* = 10.8 hold
**M_hot(<100 kpc) = (required extra)/k**:
- required extra = 0.8 M* (canonical) / 0.55 M* (alt) (CFG531/580);
- k from CFG745, at both f_hot,cl bracket ends.

## Numbers to compute (`cfg746_predict.py`, deterministic JSON, SHA-256 sealed)
- **P1.** M_hot(<100 kpc) per footing and bracket end, in M☉ (M* = 10^10.8).
- **P2. Virial temperature** in the law + C potential at 100 kpc.
  - V_c from g = g_N + √(a₀g_N) (deep form), with M_b = M* + M_hot and the cold mass included as C(<100 kpc) = k M_hot.
  - kT = μ m_p V_c²/2, μ = 0.6.
- **P3. Thermal SZ.** Y D_A² = (σ_T/m_e c²) kT N_e, N_e = M_hot/(μ_e m_p), μ_e = 1.14, in Mpc²; isothermal, all gas within
  100 kpc.
- **P4. X-ray** L(0.5–2 keV) for a uniform 100 kpc sphere (the minimum-luminosity case). Scaled as L ∝ M² from CFG580's
  committed canonical rows (M = 5.1e10 M☉ at kT 0.10–0.13: Z 0.1 / 0.3 / 1 = 3.5e39–1.1e40 / 9.8e39–2.9e40 / 3.2e40–9.5e40
  erg/s). Reported next to the eROSITA stack 1.1 ± 0.4 × 10⁴⁰ erg/s.

## Falsifier (declared now)
A measured hot-gas mass inside 100 kpc for log M* 10.5–11.0 quiescent galaxies **below half the P1 value** (all footings and
bracket ends), from SZ or X-ray mass profiles, kills the selector as the C3 explanation.

## MUTATE (`CFG746_MUTATE=1`, exit 1 iff it bites)
k → 2k: P1 must halve exactly.
