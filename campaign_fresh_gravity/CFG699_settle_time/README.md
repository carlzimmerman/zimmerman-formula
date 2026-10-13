# CFG699: the tethered cold medium cannot settle in time

**Label: T1 FAIL on both footings.** With P = −ρ̄_c ξ (CFG698) the inertia is the cold medium's own mean density. A medium element
then oscillates about the law's profile with a period of **50–156 Gyr** at y = 0.1–1: 36–113× slower than the 1.38-Gyr bar (ten
periods in 13.8 Gyr). CFG698's identification fails M1b.

- **Criteria:** `FROZEN_CRITERIA.md` (d16b81262), committed alone first.
- **Script:** `python3 cfg699.py` (seconds, exit 0) → `cfg699.out`, `cfg699_results.json`. `CFG699_MUTATE=1` exits 1 (ρ × 10⁴ cuts T
  by exactly 100×).
- **Settings:** κ = ½ FITTED; ρ_Λ from each footing via a₀ = κc√(Gρ_Λ); ρ̄_c = (0.26/0.686) ρ_Λ; the cold energy's mass is
  required; no particle species; not "theory closed".

| y = g_N/a₀ | u/a₀ | period, canonical | period, alt | inertia needed (I_req/I) |
|---|---|---|---|---|
| 0.01 | 0.095 | 311 Gyr | 257 Gyr | 2–3e-5 |
| 0.1 | 0.270 | **156 Gyr** | **129 Gyr** | 0.8–1.1e-4 |
| 1 | 0.618 | **60 Gyr** | **50 Gyr** | 5–8e-4 |
| 10 | 0.916 | 12 Gyr | 10 Gyr | 0.013–0.018 |

The stiffness term is negligible at galaxy scales (ρ̄_cγ/r² ≈ 3–4e-43 s⁻² at 10 kpc). γ = 2πG L*², independent of mass
(derived in the script).

## Reading (by the frozen rule)
1. **A real cold medium tethered to the cosmic frame responds on its own free-fall time at the cosmic mean density, about
   1/√(Gρ̄_c).** That is cosmological, not galactic. Halos could not reach the law's profile.
2. **The radiative mechanism (CFG696) survives only if P is an independent, light field,** with inertia 10⁻⁴–10⁻³ of the cold
   medium's at galaxy accelerations. Then:
   - the galaxy-scale mechanism of CFG691–697 stands (lensing, ledger, attractor, SPARC, Solar System, satellites);
   - the cosmic cold mass must come from a separate component. This reopens the two-sector problem (CFG663): the record needs
     that component to add little mass inside galaxies while supplying clusters, the Bullet, Local Group timing and the CMB.
3. **Net standing of this block (CFG690–699).** A worked mechanism for the law's phantom inside galaxies, with no law input in
   its dynamics. It is not a mechanism for the cold energy itself. Two routes were tested and closed:
   - the polarization as the cold mass (CFG697: zero cosmic mean);
   - the polarization as the cold medium's displacement (CFG699: 40–110× too slow).

   C3 and D2 are profile failures that no relaxation mechanism changes (CFG678, CFG698).
