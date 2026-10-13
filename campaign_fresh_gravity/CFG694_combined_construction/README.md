# CFG694: the three pieces together

**Label: COMBINED CONSTRUCTION CONSISTENT (G1, G3, G4 pass). C2 as built: FAIL (Υ band, inherited from CFG690). G5b: the
smallest SI-breaking quartic that passes is c₄ = 1 — REQUIRES A SECOND CONSTANT by the frozen rule (followed up in CFG695).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (08c12aea1), 2026-10-12/13.
- **Script:** `cfg694.py`, about 1 min, exit 0 → `cfg694.out`, `cfg694_results.json`. `CFG694_MUTATE=1` exits 1 (all three bite).
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory
  closed".

## Results

| test | result |
|---|---|
| **G1** criticality | −\|∇Φ\|²/8πG + P·∇Φ − 2πG P² ≡ −\|∇Φ − 4πG P\|²/8πG exactly, and the P equation equals astra's with a = 1/4πG, α = 1. **"W″(0) = 4πG" is "P has no mass term of its own"** (a mass term would be a new constant and would break SI). **R0's criticality item removed.** CFG692's medium *is* astra's sector, with its scalar identified as the gravitational potential |
| G2 | Solar System L* ≥ 5.75 pc carries over from CFG691 (same equation) |
| **G3** stars | a star's own phantom inside min(r_J, 1.08 pc) = **3.5% of its mass** (1 and 0.3 M☉, both footings), against the 15.5% local allowance (McKee+2015). Stiffness removes "Sun ON". PASS |
| **G4** satellites | ℓ_γ = 0.001–0.008 pc for Sifón's satellites, so S = 1.00000 at 36–149 kpc. Unscreened. PASS |
| G5 | c₄ = 0: 0.1012 @ 0.46 / 0.1007 @ 0.42: FAIL (Υ band) |
| G5b | c₄ = 0.1 / 0.3 / **1** / 3 / 10: Υ 0.47 / 0.49 / **0.54** / 0.62 / 0.71 (canonical). **Smallest passing c₄ = 1** (0.1020 @ 0.54; 0.1003 @ 0.50) |
| G6 | wide binaries: anomaly/Newton 7e-7 to 7e-5 (Newtonian) |
| MUTATE | wrong normalisation breaks G1; no stiffness gives star halos ≫ 0.155; L* = 10⁴ pc screens satellites. All bite |

## Reading
One Newtonian-limit action, L = −|∇Φ − 4πG P|²/8πG − ρ_bΦ − W(P) − (γ/2)|∇P|² + (I/2)|Ṗ|², together with CFG693's free-fall
basin reading, gives:
- lensing as mass (the bound charge sits in the one Poisson equation);
- a conserved mass ledger;
- a stable medium;
- a Solar System hidden by one stiffness length;
- stars without halos;
- satellites that ignore the host's field.

The remaining data failure (the Υ band) needed one more term in W. Its passing value c₄ = 1 led to CFG695.
