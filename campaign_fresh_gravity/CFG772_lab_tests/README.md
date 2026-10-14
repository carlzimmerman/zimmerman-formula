# CFG772: laboratory tests under the framework's three forms

**Label: NULL PREDICTED in every form; one SEALED KILL LINE.**
- A Cavendish-type repeat that changes the source acceleration by ×4 must show a source-dependent |ΔG/G| < 1e-6.
- The framework predicts ≤ 4e-20 (γ = 0, local), exactly 0 (stiffened), and none (basin rule).
- Klein's model, as used by Scarpa, Falomo & Treves (2026, arXiv 2603.17770), predicts 338 ppm. **A Quinn-type repeat
  separates them cleanly: a source-dependent shift ≥ 1e-6 EXCLUDES the framework in every form.**
- No existing lab measurement tests the framework.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (756d08eaf). Block CFG770–779.
- **Script:** `python3 cfg772.py` (seconds, exit 0). `CFG772_MUTATE=1` exits 1 as designed (both teeth bite).

## Results

| test | F1 stiffened (committed) | F2 γ = 0 local | F3 γ = 0 + basin |
|---|---|---|---|
| L1 Gundlach 2007 (F = ma) | Newtonian: the framework modifies the field equation, not inertia; surroundings' anomaly 2e-42 m s⁻² | Newtonian | Newtonian |
| L2 Cavendish offset δG/G | (r/L*)² = 1.5e-36 (L* 5.75 pc) | a₀/(2g_E) = 4.8e-12 / 5.8e-12 (Earth's field sets the regime) | none: the supported source's basin is 8.7 μm, inside the 5.8-cm source |
| L2 source-dependent ΔG/G (half → twice) | 0 (linear in the source) | 3–4e-20 (second order; heuristic estimate, disclosed) | 0 |
| L3 free-fall balance | 3e-37 of Newton (1 kg, 0.1 m) | — | boost only for m < 1.3–2.3e-9 kg (drop tower), 1.9–3.3e-9 kg (LEO), 2–3.5e6 kg (interplanetary, 1 AU) |

**K2.** Klein's F with β = 1.3 reproduces Scarpa et al.'s two Quinn numbers to 8e-6. It implies a source field of
4.7e-8 m s⁻², consistent with four 11-kg masses at 0.21 m. ΔG/G = 338 ppm.

## Reading
1. **Klein's model and this framework disagree sharply in the lab.**
   - Klein applies the MOND boost to the source field alone and ignores Earth's 9.8 m s⁻².
   - The framework cannot do that in any form:
     - its local action reads Earth's field (F2);
     - its basin rule only applies to free-falling bodies (F3);
     - its stiffness screens everything below parsecs (F1).
   - A Quinn repeat at half and twice the source acceleration is therefore a direct discriminator. The framework predicts no
     change.
2. **Interplanetary free-fall test.** In F3 (γ = 0 + basins), bodies up to about 10⁶ kg in interplanetary space would show
   their own MOND boost. The committed F1 does not: it predicts Newton, because stiffness wins. So an interplanetary free-fall
   experiment would separate F1 from F3. Only F1 survives Cassini without the basin rule (CFG770).

## Disclosures
- The Quinn geometry (11 kg at 0.214 m) is quoted from memory. The verdict margin is about 14 orders of magnitude, so it is
  robust to ×10.
- F2's source-dependent term is a second-order heuristic, (a_s/g_E) × offset, not a solved AQUAL problem. The margin is about
  14 orders of magnitude.
- Scarpa et al.'s numbers come from a WebFetch summary of their HTML: provisional. Their "2200 ppm" text was not verified;
  their two G values give 338 ppm.
- The raw G-measurement table is not scored: no per-experiment source accelerations are on the record.
- κ fitted; not theory closed.
