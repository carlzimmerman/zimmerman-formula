# CFG878 — FROZEN CRITERIA: derive the cold-energy fragment (clump) mass

Frozen before any script (owner block 870–879; owner: "derive the fragment mass"). κ = ½ fitted; not theory closed.

## Target
CFG877: one bound cold-energy clump per faint dwarf, σ ≈ 7.5 km/s, M ≈ 5e6 M_⊙. CFG872: per-dwarf clump mass scales as
M★^s with s = 0.241 ± 0.163 (canonical), 0.253 ± 0.253 (alt).

## Part A — mass from velocity (derivation, the law only)
Integrate the self-gravitating isothermal sphere under the full law, dρ/dr = −ρ g/σ², g = g_N ν_e(g_N/a0), for
σ ∈ {7.36, 7.53, 8.23} km/s and ρ0 ∈ [0.01, 3] M_⊙/pc³; report M_total / [81σ⁴/(4Ga0)] = f(ρ0).
- K-A1: as ρ0 → 0.01 the ratio must approach 1 (deep limit) within 6%.
- K-A2: the integrator conserves the hydrostatic identity (checked on a Newtonian run with a0 → 1e-20: M grows ∝ r at large r).

## Part B — what the record's OWN bath gives (derivation + comparison)
The record's bath (CFG544/554/558) is the cold energy's own isotropic Jeans dispersion,
σ_J²(r) = (1/ρ_c) ∫_r^∞ ρ_c g dr', in the settled state ρ_c = ρ_ph (the law's phantom density). A fragment relaxed to the bath has
σ_f = σ_J(r12) and, by Part A, M_frag = f · 81 σ_J⁴/(4 G a0), with f = 0.85 (mid of Part A; range reported).
- Analytic limit (deep regime, ρ_c ∝ r⁻²): σ_J² = V_flat²/2, V_flat⁴ = G M_b a0, so M_frag = (81/16) f M_b — clump mass ∝ host baryons (s = 1).
  *(81/16 = 5.06 is close to the record's 5.364; this is not used and is flagged as a coincidence.)*
- Numerics: for CFG872's dwarfs (its rows: M★ from Υ_SFH, r_h from LVD), Plummer baryons (scale = r_h), law g(r), ρ_ph from
  Poisson, σ_J at r12 from the integral (outer limit 300 r_h); fit log M_frag = c + s_rec log M★.
- **Classes:** RECORD BATH EXCLUDED if |s_rec − s_meas| / se_meas ≥ 3 (CFG872 canonical s, se); TENSION if 2–3; CONSISTENT if < 2.
  The alternative footing is reported with CFG872's alt numbers.
- Also reported: median M_frag vs CFG872's median clump mass 4.3e6 M_⊙, and M_frag for Fornax and Leo I (CFG853 over-fill check).

## Part C — a universal velocity scale from outside the cold sector (hypothesis, POST-HOC)
If Part B excludes the record's bath, the bath needs a universal velocity. Candidates are listed with fixed physics only:
(i) thermal speed of neutral primordial gas (μ = 1.22) at the hydrogen-cooling floor, T = 8000 K (Lyα cooling cutoff) to 10⁴ K
(atomic-cooling threshold): σ = √(kT/μ m_H); (ii) the same for ionized gas (μ = 0.59); (iii) σ² = a0 L* with L* ≥ 24 pc (CFG820).
For each, M_frag from Part A. **Label:** H-GASBATH (candidate i) is CONSISTENT if CFG877's σ (7.53 / 7.49 km/s) lies inside its
σ bracket. This comparison is post-hoc (the target σ is known), and candidate (i) needs a cold-energy–gas coupling that the record
does not contain. Its merger constraint (α ≈ 0 in mergers, CFG623/641) is stated, not tested.

## Controls
K-A1, K-A2 as above. K-B1: the Part B code reproduces the analytic deep limit M_frag/M_b = (81/16) f within 10% for a test
system with M_b = 1e5 M_⊙ and r_h = 1 kpc (deep). MUTATE (`CFG878_MUTATE=1`): bath σ_J replaced by a constant 7.5 km/s
→ s_rec must be ≈ 0 (|s_rec| < 0.1), showing the slope tracks the bath.
