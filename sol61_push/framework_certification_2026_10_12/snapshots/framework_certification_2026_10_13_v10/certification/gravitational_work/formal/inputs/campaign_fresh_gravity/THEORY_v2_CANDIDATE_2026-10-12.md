# Theory v2 (CANDIDATE, 2026-10-12): condensed-sourced settling of cold energy

Status: **candidate**. It supersedes Theory v1's settling rule (excluded on raw KiDS-1000, CFG596) and is awaiting its own
framework-native raw-data test (CFG650 job T12, 1024³; then T1). κ = ½ is fitted; the cold energy's mass is an input; this
is not "theory closed". Every claim below cites a committed lane.

## 1. Statement (one sentence)

Gravity's acceleration scale is set by dark energy, a₀ = κc√(Gρ_DE); a cold, collisionless, gravity-only component ("cold
energy", Ω_c/Ω_b = 5.364) settles into the profile that this law demands **only around a bound system's own condensed
baryons (stars + cold gas) and only from that system's own supply**, handing the released energy to dark energy; everywhere
else (hot halo gas, cluster outskirts, filaments, mergers, the early universe) cold energy remains ordinary cold matter.

## 2. Axioms (inputs)

| | axiom | status |
|---|---|---|
| A1 | a₀ = κc√(Gρ_DE), κ = ½; footings 9.36e-11 / 1.13e-10 m s⁻², never pooled | κ FITTED (CFG493: 0.42 ± 0.10) |
| A2 | Kernel g = ν(g_N/a₀) g_N, repaired ν_mono (= 1/(1−e^{−√y}) for y ≲ 2.5, monotonic tail) | as in v1 |
| A3 | Cold energy: Ω_c/Ω_b = 5.364, cold, collisionless at cosmic scale, gravity-only, no particle species added | amount measured, not derived (CFG642: no formula beats chance) |
| A4 | a₀ tracks dark energy: a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)) | CFG549 |
| **A5 (new)** | **The law's target ("phantom") is sourced by a system's CONDENSED baryons only**: ρ_ph = (1/4πG)∇·[(ν−1)g_N,d], g_N,d from stars + cold gas | CFG634 / CFG636 / CFG640 / CFG650-M2 |
| **A6 (new)** | **Supply is per host**: a system settles only cold energy from its own catchment (no pooling across overlapping catchments) | CFG647 / CFG650-M1 |
| A7 | Ordinary gravity sees all mass (baryons hot + condensed, settled + unsettled cold energy); only real mass gravitates (G9) | v1 |
| A8 | No external-field effect on internal dynamics (R7) | CFG447 / CFG478 |
| A9 | Baryons not retained by a halo (census, CFG515) are expelled from it | CFG646 / CFG650-M3 |

## 3. Equations

1. **Law**: g = ν(g_N/a₀) g_N with a₀ from A1, A4.
2. **Target**: ρ_ph = (1/4πG) ∇·[(ν(|g_N,d|/a₀) − 1) g_N,d], g_N,d sourced by condensed baryons (A5). Spherical: M_ph(r) = (ν−1) M_d(r).
3. **Supply (per host, A6)**: M_c,supply,h = 5.364 × M_b,catchment,h; settled ≤ supply of host h only.
4. **Deficit**: d = max(ρ_ph − ρ_c, 0) inside host h's catchment.
5. **Settling drift** (CFG539/541): ∂_tρ_c + ∇·(ρ_c v_s) = 0, v_s = −α 1_B 1_C τ_ff ∇ψ, ∇²ψ = 4πG d, τ_ff = (4πGρ_m)^{-1/2}; α free O(1) (mergers allow α ≈ 0, CFG623, provisional).
6. **Energy hand-off** (CFG542): Q = ρ_c α τ_ff ∇ψ·∇Φ ≥ 0 to a dynamical dark-energy partner (passive vacuum excluded, astra local_sink_reaction; candidate receiver: ghost-condensate sketch, CFG635); cosmic total Δρ_DE/ρ_DE ≈ 1e-6 since z = 1 (CFG630).
7. **Unsettled cold energy**: ordinary collisionless matter in the total potential (A7); its halo profile follows from its own infall (CFG637 solver).
8. **Velocity part**: relaxation toward the maximum-entropy stationary F(E,L) of the settled halo; with the repaired kernel the target is near-isotropic (CFG620/626).
9. **Field form of the law** (astra stress_closure): ∇·[(B(g)/g)∇Φ] = 4πGρ_b,d, from I[Φ] = ∫[e(g) + ρ_b,d Φ], e(g) = (1/4πG)∫₀^g B(s)ds.

## 4. Why this form (what each new axiom fixes)

| problem in v1 | fixed by | evidence |
|---|---|---|
| raw-KiDS exclusion, Δχ² +68.7 (CFG596) | A5 | census-capped condensed source: Δχ² +14.0 at 1024³ (CFG636), own boost 1.06 vs 1.19–1.25 |
| remaining excess | A6, A9 | per-host supply removes ~⅓ of the excess (CFG647); expulsion ~¼ of Δχ² (CFG646); 256³ preview M1+M2 within +0.5–3.1% of S0 (CFG650) |
| Bullet lensing on galaxies with α ≈ 0 | A5 + A7 | settled mass is tied to condensed baryons (CFG634 T4a: gas-tied share 0); the rest is collisionless |
| cluster cores short (CFG625/629/637) | A7 (unsettled reservoir) | derived reservoir with condensed source passes the X-COP inner band and the Bullet main (CFG637) |
| primary CMB | switch off before structure | CFG649: P1 ≡ P0 at z_i; 10^−1232 bound systems at z = 1100 |

## 5. Scoreboard (raw data, framework-native; ΛCDM tools only as labelled context)

**Passes**: SPARC RAR (0.133–0.137 dex on 2,693 points, astra; 0.100 dex on rotmod, CFG624); Tian groups; Local Group timing
(with cold energy); X-COP inner band and Bullet main core (CFG637, condensed source); primary CMB (CFG649).
**Open / failing**: X-COP at R200 (33–40% short, CFG637, depends on the supply convention); Bullet sub (input-mass-limited);
raw KiDS for the full v2 rule (T12 pending); CMB lensing CONDITIONAL (+1.3% for v1, CFG649; v2 lowers it); age dependence in
early types (CFG585/631/700; CFG651: A5 predicts the WRONG sign, −0.06 in log, so any mechanism must overcome it); α free; 5.364 underived; the receiver field's identity.
**Conditional on**: inherited ΛCDM initial conditions and background in all PM runs (astra 5c31fcad4).

## 6. Predictions (dated, falsifiable)

| prediction | test | date |
|---|---|---|
| raw KiDS-1000 / DES Y3 ξ± consistent (Δχ² < 9 vs S0, T-OWN passes) | CFG650 T12 / T1 | 2026-10-13/14 |
| a₀ flat with redshift (a₀ ∝ √ρ_DE), not ∝ H(z) | ALMA U4_27928 / GS4_24110 (demonstrations), KURVS CO (sample) | 2026-11-06, 11-28 |
| MW vertical force and wide binaries (sealed, no EFE) | Gaia DR4 | 2026-12-02 |
| hot-gas-dominated groups: beyond their galaxies, mass behaves like plain cold matter, not an extended a₀ halo | group weak lensing split by hot-gas fraction | proposed |
| no cold-energy spike around massive black holes | LISA EMRIs | 2030s |

## 7. What kills it

- T12 and T1 both EXCLUDED on raw KiDS by the frozen rule.
- a₀ rising with redshift (a robust rise ⇒ KILL of the flat law).
- Gaia DR4 MW K_z or wide binaries outside the sealed predictions.
- Any requirement for a new tuned constant to pass the gates above.

## 8. Open problems (ranked)

1. Derive the condensed/hot split from dynamics (currently a census cap; CFG640 carries phase memory; the cooling split gives the 10% floor).
2. The unsettled reservoir's profile in clusters at R200.
3. The energy receiver: a derived dynamical partner without the w = −1 singularity.
4. α (merger vs galaxy) and the early-type age signal.
5. Ω_c/Ω_b = 5.364 and κ = ½ (both inputs).
