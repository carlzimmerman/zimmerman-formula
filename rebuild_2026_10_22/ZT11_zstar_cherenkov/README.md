# ZT11_zstar_cherenkov: do stars radiate Z★'s khronon/dust pair (Cherenkov)? (Z-T11)

Test frozen in `Z1_successor_design/TEST_PLAN.md` (0d1959a4f5). Criteria and ledger: `FROZEN_CRITERIA.md`,
`ASSUMPTION_LEDGER.md` (9ecd65dbd4, committed alone before any script). Design Z★ = v3s-OC (`Z1_successor_design/DESIGN.md`).
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". Nothing
here says the data favour the framework.

## Verdict: **PASS** (frozen rule, both footings, L★ = 24 and 90 pc)

The shortest energy-loss time in any row is 1.8e4 t_H (a 20 M☉ star at R = 4 kpc, alt footing, conservative envelope).
For the Sun it is ≥ 7.8e5 t_H, and for 1 M☉ disc stars ≥ 3.2e5 t_H. The line is 10 t_H.

| footing | L★ | Sun (230 / 250 km/s), envelope | Sun, g = 1, r_min = r_acc | min over disc stars (1, 20 M☉; R 4–16 kpc), envelope | pair speed c_s at R₀ | Mach of the Sun |
|---|---|---|---|---|---|---|
| canonical | 24 pc | 9.3e5 / 1.2e6 t_H | 1.3e6 / 1.6e6 | 2.0e4 (20 M☉, 4 kpc); 1 M☉: 3.7e5 | 0.96 km/s | 240 |
| canonical | 90 pc | 9.8e5 / 1.2e6 | 1.3e6 / 1.6e6 | 2.1e4; 1 M☉: 3.8e5 | 3.6 km/s | 64 |
| alt | 24 pc | 7.8e5 / 9.9e5 | 1.1e6 / 1.4e6 | 1.8e4; 1 M☉: 3.2e5 | 1.0 km/s | 224 |
| alt | 90 pc | 8.3e5 / 1.1e6 | 1.1e6 / 1.4e6 | 1.8e4; 1 M☉: 3.4e5 | 3.8 km/s | 60 |

Every row is supersonic (Mach 37–365), so the Cherenkov channel is open everywhere. The full 48-row table is in
`zt11_cherenkov.out` / `_results.json`. The margin survives a ×10 denser medium: the minimum is then 1.8e3 t_H.

## What was derived (sympy; all residuals 0)

1. **The pair is the sound mode of the held medium.**
   - Source: X3's PN Lagrangian of v3/v3s with μ_K = 0. Z★ removes K(Q) (DESIGN §3), so both μ_K terms of P3's G and Z
     are dropped.
   - In that Lagrangian ρ_τ = D·P enters as a fluid density: the term ρ_τ(σ̇ − |∇σ|²/2) has inertia ρ_τ, and the fluid
     gravitates as −ρ_τφ.
   - Linear dispersion: ω² = Kρ₀(M − 1) + γ_Lρ₀k². This equals X3's B1-S at μ_K = 0 (K2).
   - Sound speed c_s² = γ_Lρ₀ = 2πGρ₀L★², which grows with L★. Gap ω_g² = Kρ₀(M − 1).
   - P3's decoupled pair (G = D·P, Z = k²/(K M + γ_L k²)) is the same mode without self-gravity. The difference is
     exactly Kρ₀ (K3).
   - P3's Solar-System c_π = 1.0e-4 c (29.8 km/s at 1 AU) is reproduced to 2e-5 (K1). There c_π = √(GM/r), the local
     circular speed.
2. **Coupling of a star to the pair: gravitational, not MOND-strength. Inside L★ screening makes it exactly Newtonian.**
   - Matter enters only through φ (S_m[g]).
   - The forced equation is δρ̈ − c_s²∇²δρ + ω_g²δρ = Kρ₀M★δ³(x − vt) (K2).
   - The static coupling at wavenumber k is G_eff/G = (M + L★²k²/2)/(M − 1 + L★²k²/2) (K5).
     - It is 1 for kL★ ≫ 1: screened, no enhancement.
     - It reaches at most M/(M − 1) = (1+x)/x ≈ 1.5–2.1 beyond L★, the EFE-limited value in the Milky Way.
     - At M = 1 it equals X15's hedgehog U_N.
   - The self-consistent linear drag already contains this response, so the exact linear result is g = 1. The verdict
     envelope multiplies by g² = (G_eff/G)², an over-count kept as the conservative choice.
3. **Loss rate (independent Ostriker-type derivation; K4, K8).**
   - Drag force: F = 4πG²M★²ρ₀/v² · ∫(dk/k) g², for v > c_s.
   - k_min = ω_g/√(v² − c_s²). This gives λ_min ≈ 1.3–6.8 kpc.
   - t_loss = v³/(8πG²M★ρ₀ lnΛ).
   - At Mach ≫ 1 the pair speed and L★ enter only through the logarithm (lnΛ 25–50). So the loss is ordinary dynamical
     friction on the held dust, at the local phantom density.
4. **The medium.**
   - ρ₀ is the law's phantom density at (R, z = 0), from S3's cached isolated AQUAL solve of McMillan17 (read-only).
   - At R₀: 0.059 / 0.068 M☉ pc⁻³, x = 1.98 / 1.72; v_c(R₀) = 215.3 / 220.6 km/s, within 0.08 % of the record (K7).

**The Sun's own neighbourhood.**
- **v3s (no cap):** c_π = √(GM☉/r). That is 29.8 km/s at 1 AU. It exceeds 230 km/s only inside 3.6 R☉, so the Sun is
  supersonic relative to its own hedgehog everywhere outside itself.
- **Z★:** R1 caps D·P ≤ ρ_d. The Sun's hedgehog density M☉/(2πL★²r) exceeds the local held density inside
  r_nl = 970 / 840 AU (24 pc) and 69 / 60 AU (90 pc). Beyond r_nl, c_π = √(γ_Lρ₀) = 0.96–3.8 km/s.

## Checks

- **Main run: 8/8 PASS, exit 0.** The checks are K1 (P3 c_π), K2 (dispersion and source vs X3), K3 (P3 vs X3), K4
  (Cherenkov integral), K5 (G_eff, X15 limit), K6 (units), K7 (MW input) and K8 (k-integral).
  - Cost: 0.15 GB RSS, one thread, nice 15, seconds.
- **`--mutate`: exit 1, 6/8.** The mutation sets c_s² → 2γ_Lρ₀ and P3's G → 2D·P. K1 and K3 FAIL, as required.
  - The MUTATE verdict line is unchanged (PASS). That is expected: c_s enters t_loss only through the logarithm.

## Provisional and posited ingredients

- **Mistele 2021 (arXiv 2103.16954), "Cherenkov radiation from stars constrains hybrid MOND dark matter models": PROVISIONAL.**
  - Only its title, author and abstract gist were obtained, from a summarising arXiv-API fetch. That gist: hybrid models
    have a mode that couples directly to matter with a non-relativistic sound speed.
  - No formula of it was text-verified, and no number from it is used. The verdict rests on the derivation above.
  - Why Z★ differs from such models, if it does, is not checked against the paper's text. Here the pair couples only
    through gravity, at the held density.
- **POSITED:**
  - the UV cutoff (R★ in the envelope; r_acc and r_nl reported);
  - the IR cutoff from the smallest stiffness M_T = 1 + x;
  - R★ ∝ M★^0.8;
  - held density = phantom (supply ≥ demand locally; Z★ R1/R2).
- **EXTERNALLY CALIBRATED:** the Sun's speed of 230–250 km/s; t_H = 1/H₀ at 67.4 km/s/Mpc.

## What this does not show

- **Linear response only.**
  - The nonlinear core (r < r_acc = 0.03 AU, or r < r_nl) is cut out. Its contribution is O(lnΛ⁻¹) of the total in
    Ostriker's treatment, which this lane does not verify.
  - The transport of the moving Sun's hedgehog charge at β = 0 (X15's open point) is not solved.
- **Anisotropy** (M_θ between 1+x and (1+x)²) enters only through the logarithm, where it is bounded by the M_T choice.
- **Not scored:** compact objects, binaries, and stars in dwarf or cluster owners. The loss rate scales as M★ρ₀/v³, so a
  slow massive body in a dense held medium is the place to look.
- **Flag for the record (not scored):** under R1 the Sun's screened hedgehog is capacity-capped inside r_nl (60–970 AU).
  Whether Z★'s Solar-System screening (Cassini, planetary hedgehog GM/L★²) is unchanged by the upper obstacle has not been
  checked. It belongs with Z-T3.

## Disclosure

Before the criteria were frozen, the agent read S3's cached solve in a scratch session to locate the local phantom density
(about 0.06 M☉ pc⁻³) and fetched the Mistele abstract. No loss time was computed before the freeze.

## Files and run

`zt11_cherenkov.py`; `zt11_cherenkov{,_MUTATE}.out`; `zt11_cherenkov_results{,_MUTATE}.json`.

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/ZT11_zstar_cherenkov/zt11_cherenkov.py            # exit 0
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/ZT11_zstar_cherenkov/zt11_cherenkov.py --mutate   # exit 1 by design
```
