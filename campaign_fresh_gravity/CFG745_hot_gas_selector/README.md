# CFG745: a hot-gas selector — cold mass retained in proportion to hot gas

**Label: SELECTOR CONSISTENT as frozen, with two constants (k, L*); groups in TENSION at one end; the hot gas around early types
is unmeasured.** Selector H, C = k · M_hot, is calibrated on X-COP alone. It does not fail the groups that pass without cold
mass. It asks massive early types for an amount of hot gas that eROSITA allows, and that is precisely what would supply their
missing mass (C3). A state-blind version (C = k M_b) fails groups (MUTATE bites).

- **Criteria:** `FROZEN_CRITERIA.md` (4f2fa30ea), committed alone first.
- **Script:** `python3 cfg745.py` (seconds) → `cfg745.out`, `cfg745_results.json`. `CFG745_MUTATE=1` exits 1.
- **Settings:** κ = ½ FITTED; simple μ (CFG695); the cold energy's mass is required; no particle species; not "theory closed".
  The only declared input not from a lane is the bracket f_hot,cl = 0.85–0.95.

| footing, f_hot,cl | k | groups shift (ν_g 1.6 / 3.7) vs 2σ = 0.0645 | H2 | early types: M_hot needed | eROSITA-allowed (Z 0.1 / 0.3 / 1) | H3 |
|---|---|---|---|---|---|---|
| canonical, 0.85 | 3.62 | +0.072 / +0.033 | TENSION | 0.22 M* | 1.49 / 0.90 / 0.50 M* | NOT EXCLUDED |
| canonical, 0.95 | 3.24 | +0.065 / +0.029 | TENSION | 0.25 M* | 1.49 / 0.90 / 0.50 M* | NOT EXCLUDED |
| alt, 0.85 | 3.22 | +0.065 / +0.029 | TENSION | 0.17 M* | 0.59 / 0.35 / 0.20 M* | NOT EXCLUDED |
| alt, 0.95 | 2.88 | +0.058 / +0.026 | PASS | 0.19 M* | 0.59 / 0.35 / 0.20 M* | NOT EXCLUDED |

X-COP missing mass with simple μ: median 3.0 (canonical) / 2.74 (alt) M_b (range 1.9–4.5).

## Reading
1. **One dimensionless state variable sorts all three regimes:**
   - galaxies (f_hot ≈ 0): no cold mass, so SPARC is unchanged;
   - groups (f_hot ≈ 0.08): a little, within about 2σ of their pass;
   - clusters (f_hot ≈ 0.9): about 3 M_b, X-COP by construction.
2. **A sharp prediction for C3.** Massive quiescent galaxies (log M* 10.8) must hold **M_hot ≈ 0.17–0.25 M* (≈1–1.5 × 10¹⁰ M☉)
   inside 100 kpc**. Then C = k M_hot supplies their 0.55–0.8 M* shortfall. eROSITA's 0.5–2 keV stack allows it, but the mass is
   not measured. SZ stacks or X-ray mass profiles of such galaxies decide it. If they find much less hot gas, the selector fails
   C3.
3. **Structural.**
   - Bullet: C is collisionless and retained at formation, so it follows the galaxies, not the stripped gas.
   - CMB: C is cold.
   - D2: less C in groups lowers the one-halo shear term. Not scored here.
4. **What it is not.**
   - Not a mechanism: nothing explains why cold mass should be retained in proportion to hot gas.
   - k (≈ 3, of order the cosmic Ω_c/Ω_b ≈ 5.3) is a fitted second constant.
   - The groups test brackets ν_g rather than computing it per group (the Tian table is not on disk).
