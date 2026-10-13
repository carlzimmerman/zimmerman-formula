# CFG698: the polarization as the displacement of a real cold medium

**Label: CANDIDATE B WITH A MECHANISM.** With P = −ρ̄_c ξ, the CFG694–696 action describes a real cold medium. Its critical
tether cancels the medium's Jeans term exactly (J1).
- **Tether everywhere:** cosmic growth is far too slow (δ ∝ a^0.61). This version is excluded.
- **Tether only inside bound basins:** the medium is a free cold component outside them (δ ∝ a¹, background and CMB mass
  restored) and relaxes to the law's profile inside them. That is the record's candidate B, now with a mechanism. It inherits
  B's data verdicts, including the D2 KiDS exclusion and C3.

- **Criteria:** `FROZEN_CRITERIA.md` (f713f6b27), committed alone first.
- **Script:** `python3 cfg698.py` (sympy, seconds, exit 0) → `cfg698.out`, `cfg698_results.json`. `CFG698_MUTATE=1` exits 1 (both
  bite).
- **Settings:** κ = ½ FITTED; the cold energy's mass is required; no particle species; not "theory closed".

## Results

| test | result |
|---|---|
| J1 | ξ̈ = 4πGρ̄ξ − (1/ρ̄)∂W/∂ξ = **0** with the critical tether: the tether exactly cancels the medium's self-gravity. PASS |
| J2 | tether everywhere: largest growth eigenvalue 0.140 of Ω_m = 0.309, so **p = 0.61**. FAILS cosmology, as frozen |
| J3 | tether only inside bound basins: free outside, eigenvalue 0.309, **p = 1** (a cold component). PASS |
| inherited (B) | X-COP 0.946 ± 0.080 PASS; Local Group z −0.11 / −0.10 PASS; **D2 KiDS EXCLUDED** (Δχ² +68.7, CFG596); **C3 FAIL** (CFG529); Bullet UNDETERMINED (α = 0, CFG621/623) |
| MUTATE | tether 1.1 × critical: J1 fails (net restoring force). No tether: free growth, but no static galaxy solution. Both bite |

## Reading: the mechanism, end to end
The cold energy is a real cold medium with mean density ρ̄_c.
- **Outside bound systems** it is free, falls under gravity, and grows like a cold component. It carries the cosmic mass.
- **Inside a bound system's free-fall basin** it is tethered to the cosmic frame by a critical, saturating tether:
  - the tether exactly cancels the medium's own Jeans pull, so the medium answers only to the baryons;
  - it saturates at a₀;
  - stiffness hides compact bodies.

  The medium then relaxes by radiating displacement waves onto the law's profile. The halo is cold mass literally *moved*
  toward the baryons, and its energy leaves as radiation.
- This answers the original specification:
  - it moves the cold mass into the profile;
  - it accounts for the exchanged energy;
  - gravity and lensing come from one Poisson equation.

**What it does not do.** It changes no static prediction of candidate B, so B's data failures stand:
- massive early types are 30–40% short (C3);
- raw KiDS shear excludes the canonical settled profile (D2).

Those belong to the law's profile, not to the missing mechanism (CFG678). Fixing them needs a different profile or a data
re-check: CFG667 suggests the C3 shortfall may be a stellar-mass artefact.

**Still open:**
- the tether switching on at the basin edge, which needs a variational form (B1; CFG48's edge step);
- the relativistic completion;
- κ fitted.
