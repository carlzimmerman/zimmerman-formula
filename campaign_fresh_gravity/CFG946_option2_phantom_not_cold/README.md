# CFG946: option 2, cold energy is NOT literally the law's phantom

**Lane label: NO-GO (theorem T-O2).**

Option 2 says cold energy is ordinary self-gravitating dust and the law's extra force comes from a separate sector. Every
construction tested is NOT VIABLE, and a theorem covers the whole class of local constructions:
- **The theorem.** A local, second-order field that supplies the profile-independent deep law must carry an external-field
  effect (EFE).
- **What that forces.** With CL-AR and CFG925 R3 read as "no EFE", the deep-regime extra force has to be the dust's own mass. So
  cold energy *is* the phantom, which is the opposite of option 2.
- **The fallback fails too.** A static rule that makes dust follow the law needs held dust. Its holding force cancels the dust's
  self-gravity (D-T′, which generalises CFG941's D-T).
- **What is left.** Only a non-static, non-local supply survives, and that is option 3 (CFG947).
- **Particle in disguise, plainly.** Option 2's cold energy is, in every gravitational respect, a cold collisionless matter
  species. No species is added beyond cold energy itself, but option 2 makes cold energy indistinguishable from one.

**Lane facts.**
- **Criteria:** `FROZEN_CRITERIA.md` (08f3b30a6, committed alone first). Block 940–949.
- **Amendment:** `AMENDMENT_A1_post_result.md` (23e0a5765). It is code and reporting only. One post-result fix corrected a
  printed fail list; no class changed.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled. Framework-native inputs only.
- Not "theory closed". Nothing here says the data favour the framework.

## The four lemmas (all pass; DERIVATION §2)
- **L-AR.** In an action, the species that feels a field also sources it. "Sourced by baryons, felt by dust" is therefore not
  variational: a baryon + dust pair self-accelerates at 0.13 a₀.
- **L-G.** Exact uniform-field superposition means the equations depend only on ∂∂φ.
  - Then φ_μ(x) = μ²φ(x/μ) solves the system with mass ×μ³, so the flat amplitude scales as μ².
  - The deep law needs μ^{3/2}.
  - Hence a no-EFE field cannot supply the deep law, and its share falls as μ^{1/2}.
  - Deep AQUAL and QUMOND fail superposition, so they have an EFE. A cubic Galileon passes superposition but has no flat regime.
- **D-T′.** A static holding force F(u) on dust in the law has F′(0) = m′, the self-gravity coefficient the dust feels. This holds
  for any source multiplicity and any deep-limit law.
- **N-L.** A field-supplied deep law responds as √g_N at zero field. So there is no linear regime about FRW, and the Cauchy
  problem there is not unique.

## Results (canonical / alt)

| construction | key numbers | class |
|---|---|---|
| **O2a-1** QUMOND-type X sourced by baryons, felt by all (literal) | (a) dust in galaxies double counts: D-A 0.83, D-F 0.50 (0.18 dex), D-U 2e-4; (b) n = 1.88 at the largest linear field (a¹ needs y ≥ 593, actual ≤ 0.037); (c) EFE −0.52 … 0 dex for H1–H3; (d) non-variational, non-Lipschitz; (e) light misses X: s up to 0.92; (f) net source 12.8× the catchment; (g) TDGs z −3.5 | NOT VIABLE |
| **O2a-2** same, baryon-only (variational) | as O2a-1; (b) n = 1.60 | NOT VIABLE |
| **O2a-3** universal ("MOND + cold dust") | (a) BTFR at r_ta 6.56 (all catchment dust enters ν); D-A 1.74 / 1.86; (b) n = 2.70; (c) −0.58 … 0 dex | NOT VIABLE |
| **O2a-G** gated X | (b) PASS, but the gate's kinetic term is a ghost band, k_g R = 0.09–3.1; (a), (c), (e), (f), (g) as O2a | NOT VIABLE |
| **O2b** X sourced by the dust's settled excess | (a) needs slaved dust (M_ex/M_ph = 0.15) that nothing selects: a second equilibrium misses by 0.26; (b) n = 2.61; (c) −0.43 … 0 dex; (d) non-variational | NOT VIABLE |
| **O2c** tether without cancellation (c₂ ≠ 1) | the law becomes g_N = R(u) − (1 − c₂)u, with floor a₀(1 − c₂)/(2 − c₂) for c₂ < 1 and rescaled Newton for c₂ > 1; growth needs c₂ ≤ 3.5e-3, where the law misses by 1.64 / 1.88; hover Δa/g_host = 1; slip 3.3e-5 | NOT VIABLE |
| **O2d1** Galilean-symmetric field | (c) passes by construction; (a) fails by L-G (best cubic-Galileon fit to NGC 3198 misses by 0.15, with a fifth force 4.9× Newton, n = 2.73); (e) light-blind | NOT VIABLE |
| **O2d2** dispersion-supported dust = phantom | (b)–(e) pass (slip 1.54e-5); (a) fails: nothing selects the law (a second Jeans equilibrium misses by 0.41), and assembly needs ℓ = 26 R (CL-AR budget). It is S3 with dispersion, i.e. option 3 with a supply rule | NOT VIABLE |

**Satellites in the record (CFG925 R3, read only).** An option-2 field EFE is CFG925's E1/E2.
- It lowers the satellite predictions by 0.48–0.71 dex.
- Option 2 could only compensate if satellites held 0.28–0.37 dex more bound cold mass than isolated dwarfs (z 2.7–3.7), against
  tidal stripping.

**Below-law systems.**
- Field-supplied branches act on every baryonic system. Tidal dwarfs then stay −0.38 ± 0.11 dex below the field law, even with
  its EFE (CFG936 route iii, z −3.5 / −3.8). DF4 lies below Newton.
- Dust-supplied branches give Newton at zero dust (route i). The zero-supply label is not derived.

**Excess family.** Dust can supply it, but only through class-dependent fractions: dwarfs 1.35, clusters 0.75, red lenses 0.34,
against large-SPARC 0.002. There is no derived selector, so this re-describes the excess rather than explaining it.

**Shear.** No construction has class A as its non-relativistic limit. The T1x/T2x/NC1x passes do not transfer.

## Controls
- **K: all pass.**
  - K1: NGC 3198 law 2.2e-16.
  - K2: CFG941's a^0.69433; dust n = 1.
  - K3: CL-AR Theorem 1, three bodies, sympy.
  - K4: CL-AR transport budget 494.7 / 513.9 kpc (record 495 / 514).
  - K5: Gauss-flux boost 4.2485 (CFG925 K7: 4.249).
  - K6: O2c(c₂ = 0) = CFG938 M3, 1.6445 / 1.8844.
- **MUTATE: all bite** (exit 1 by design).
  - M1, sector off: dust + Newton, NGC 3198 0.827 / 0.841, n = 1, no EFE.
  - M2, double counting breaks the law: 0.83 / 1.74, and multiplicity 2 gives 6.40 / 7.16 = CFG941 M2a.
  - M3, linear X: no EFE and no BTFR.
  - M4, external field → 0: factor 1.

## Files and commands
One core, nice 10, ~5 s each, peak RSS 0.15 GB, nothing downloaded, no other lane touched.

| command | outputs | exit |
|---|---|---|
| `CFG946_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg946.py` | `cfg946_K.out`, `cfg946_results_K.json` | 0 |
| `CFG946_MUTATE=1 …` | `cfg946_MUTATE.out`, `cfg946_results_MUTATE.json` | 1 by design |
| `OMP_NUM_THREADS=1 nice -n 10 python3 cfg946.py` | `cfg946.out`, `cfg946_results.json` | 0; all checks pass |

- `cfg946_firstrun_npbool.*` is the first main run, which had the A1 item-6 listing bug. Same numbers.
- `DERIVATION.md` has every equation, number, implementation choice and disclosure.

## Open (not tested here)
- Non-static, non-local supply: option 3, CFG947.
- Non-local or higher-derivative field sectors.
- Modified inertia.
- EP-violating charges.

All of these lie outside assumption A2 of T-O2.
