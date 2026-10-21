# CFG953: the minimal source-changing non-local theory (SCT), built and tested

**Lane label: SCT CONDITIONAL.** In the primary form, SCT-M, cold energy is ordinary untethered dust until a system collapses. At
collapse the system's dust is *converted* into a phantom body. The body's shape is the law's phantom of the system's own baryons,
taken as a monopole and cut at the supply edge. Its centroid, momentum, spin and internal energy absorb each conversion and merge
inelastically.

SCT-M passes every graded test. Two of them rest on named conditions:
- **C-E:** energy closes only through a non-dynamical internal energy carried by each body. This is CFG935's "sink outside matter".
- **C-DF:** DF2/DF4 are in-situ debris.

The variant **SCT-Q** (pointwise QUMOND phantom of the own baryons) is **INCONSISTENT**: in-situ systems inherit the host EFE, which the
Lelli+15 tidal dwarfs exclude at z −3.48 / −3.79.

**Settings and provenance.**
- **Criteria:** `FROZEN_CRITERIA.md`, 049a0f867, committed alone first.
- **A1:** `AMENDMENT_A1_pre_result.md`, 611bb324a, pre-result for the main stage, committed alone. It adds a reported-only diagnostic in
  (g).
- Block 950–959.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy; no particle species. Framework-native inputs only.
- Not "theory closed". Nothing here says the data favour the framework.

## The theory (DERIVATION §1)

| rule | content |
|---|---|
| R0 | G_μν = 8πG(T^b + T^c + 𝒮)_μν; baryons and dust geodesic, the dust untethered, so ∇_μ𝒮^{μν} = 0 |
| R1 | a domain is born at first turnaround from the Hubble flow, with baryons present (no RMIN), and labels are latched; a system formed inside a collapsed domain (stars, binaries, tidal dwarfs, debris) is not a domain and finds no unlabelled dust |
| R2 | 𝒮 = Σ_q Σ_q − T_c,lab. Labelled dust is gravitationally inert, because its whole stress-energy is cancelled; NR gravitating density ρ_b + ρ_c,unl + Σ_q σ_q |
| R3 | SCT-M: σ_q spherical about its centroid X_q, M_σ(<r) = min{r²[g_law(ḡ) − ḡ]/G, M_c}, ḡ = G M_b,own(<r)/r²; edge at the kernel's own supply root. SCT-Q: the pointwise own-baryon phantom |
| R4 | M_c V̇_q = ∫σ_q g between events; conversions are inelastic (mass, centroid and momentum add) |
| R5 | spin S_q absorbs angular momentum at events (magnetic part of 𝒬); a sphere feels no torque about its centre |
| R6 | internal energy E_int,q absorbs the reshaping work ∫Φ ∂ₜσ and the event terms |
| R7 | merge when bound fraction < ½ or when the baryon centroids coalesce; inelastic |
| R8 | retarded kernels; 𝒮 updates and body signals propagate at c; the rigid body is the NR limit |
| R9 | no action principle (the time-symmetric form is acausal) |

**The key step: S-TM.** CFG947's T-M obstruction (an un-conservable relocation) disappears. A conversion keeps the 𝒮 dipole and its
rate continuous, and between events the body's centroid law *is* the momentum condition, so the relocation term is R ≡ 0 (sympy, any
history). The price is that the body is centred on the dust it converted, so the baryons sit off its centre until mutual gravity
re-centres them.

## Results (both footings)

| test | result | grade |
|---|---|---|
| (a) law, one domain | NGC 3198: 2.2e-16 at 43 radii, both kernels, identical for dust profiles P-S / P-I / P-X (inert dust: no C-ρ). Deep points y = 1e-2, 1e-3 exact (V⁴/(G M_b a₀) 1.105 / 1.032). Edge 454 / 413 kpc = (N + ½) r_M; flat to y_e = 3.4e-4 (V⁴/(G M_b a₀) 1.019), Kepler beyond. By construction for one domain | PASS |
| (b) FRW, growth | 𝒮 ≡ 0 on FRW; dust w = 0; n = 1 exactly; no domain before turnaround; the body gas also grows as a¹ | PASS |
| (c) no hover / no EFE | Δa/g_host ≤ 2.7e-3 / 2.1e-3 (tidal order, H3 at 50 kpc) against ε_B 0.344 / 0.317; EFE 0 by construction, plus ≤ 2.6e-3 dex from the equilibrium baryon–body offset (δ_eq/a ≤ 7e-3), against 0.082 | PASS |
| (d) slip | worst 1.35e-5 (alt cluster) ≤ 1.9e-5; the dust's own pressure is cancelled (CFG947's 1.63e-5 term is gone) | PASS |
| (e) conservation | momentum and angular momentum exact (toy 1e-15 through 260 conversions, satellite infall and a merger; third law between overlapping bodies 1.4e-11). Energy only with E_int: formation releases 0.70–0.99 \|W\| (4e-11 – 4e-5 M_c c²); the toy merger draws 0.21 \|E\| (the merged law is 25% weaker than the two own-domain bodies, T-L) | CONDITIONAL (C-E) |
| (f) dwarfs, no RMIN | every collapsed system with baryons has a domain; the edge moves dwarf σ²_ap by ≤ 0.024 dex (UFD-e, edge at 1.5 a). Excess family: **NO HANDLE** (SCT predicts the EFE-free law for every dwarf) | PASS |
| (g) below-law | SCT-M: Newton. TDGs +0.055 ± 0.114 dex, χ² 1.17/6: EXPLAINS; DF2/DF4 +0.028 ± 0.539 ln: EXPLAINS (both footings). SCT-Q: host EFE, TDGs −0.381 / −0.414 (z −3.48 / −3.79): FAILS | M: CONDITIONAL (C-DF); Q: FAIL |

**Reported, no class weight.**
- **Disc geometry.** The monopole body sits up to 0.054 dex below the pointwise law for LSB exponential discs. SCT-M equals the record's
  law only in the spherical-equivalent convention that every parent lane used.
- **A1.** The host body's local density inside TDGs and DF2/DF4 shifts the Newton prediction by +0.02 to +0.11 dex (still EXPLAINS).
- **Satellites.** A satellite's body is not tidally truncated: H3's 9.4 kpc body against its 5.1 kpc Jacobi radius at 50 kpc. Bodies
  cause no dynamical friction.
- **Clusters (CFG954 decides).** They lie between CFG951's plain-law row (core deficit, Z_MID +7.7 / +6.9) and its X-OD row
  (memory, Z_OUTER ≤ −2.7 / −4.0), depending on the merge rule R7.

## CFG678 scorecard (SCT-M)

| status | gates |
|---|---|
| PASS | A5 |
| CONDITIONAL | A1, A2, A6, B3, C1 (Solar System Newtonian: the Sun is in situ), C2 (SPARC 0.1003 / 0.0991 = local; the law comes from the prescribed 𝒮) |
| FAIL | C3 (inherited) |
| NOT DECIDED | C4 |
| PENDING | D3 |
| UNTESTED | A3, A4, B1, B2, D1, D2 |
| DECLARED | A7, E1–E3 |

Wide binaries come out Newtonian (z −1.36 / −1.51, PASS), as the sealed DR4 prediction says. The class-A shear passes do not transfer
(D2 needs an SCT PM engine).

## Costs
1. An action-less, retarded, non-local source sector.
2. A prescribed label sector (birth at turnaround, latch, in-situ rule, merges).
3. Rigid phantom bodies with charges. These are a non-relativistic idealization, so C-c (a finite-c_u body) is open.
4. E_int, which must absorb and supply O(1) binding energies; its sign over a merger history is not established.
5. Cold energy becomes gravitationally invisible dust at collapse: its gravity moves into the body.
6. Undamped baryon–body offsets after anisotropic accretion (toy: 0.7 of the baryons' Plummer radius). The law is exact only at zero
   offset.
7. No body stripping and no dynamical friction from bodies.
8. A monopole source (the disc geometry difference above).
9. The supply N is inherited from the engine census.

Open for real systems: C-MR (the merge rule must act; T-L otherwise) and C-c.

## Controls
- **K: 8/8 PASS.**
  - CFG938's law on NGC 3198 (2.2e-16).
  - CFG947's no-hover bound (1.2114e-6) and CFG941's hover (1.017–1.107).
  - CFG941 / CFG947 growth (0.60954 / 0.69433 / 1).
  - CFG947's slip (1.6324e-5; 𝒮 stress 1.2955e-5).
  - CFG4's SPARC (0.1003 / 0.0991).
  - CFG947's T-M (π²ε/4).
  - CFG936's routes (i) and (iii).
  - CFG947's T-E (1.847) and T-R (4.815e10).
- **MUTATE: 7/7 bite** (exit 1 by design).
  - Mu1: a global source gives back the EFE (−0.73 … −0.10 dex).
  - Mu2: a tether gives back D-T (hover 1.02–1.11, n = 0.694).
  - Mu3: a body glued to its baryons loses 53% of the momentum scale.
  - Mu4: dust gravitating on top of the body breaks the law (0.83).
  - Mu5: without E_int the energy changes by 25%.
  - Mu6: the time-symmetric kernel is acausal (precursor ½).
  - Mu7: no edge creates 83–97 M_b of 𝒮.

## Files and commands

Every stage runs one process on one core at nice 10, with the in-script 1 GB RSS guard. Peak RSS is ≤ 0.51 GB. Nothing was
downloaded, and no other lane was edited.
- `CFG953_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg953.py` → `cfg953_K.out`, `cfg953_results_K.json` (exit 0; about 1 s).
- `CFG953_MUTATE=1 …` → `cfg953_MUTATE.out`, `cfg953_results_MUTATE.json` (exit 1 by design; about 7.5 min).
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg953.py` → `cfg953.out`, `cfg953_results.json` (exit 0; about 12 min).
- Kept for disclosure:
  - `cfg953_firstrun_k1crash.out`: the first main run, which crashed on a shadowed name in the reported disc diagnostic;
  - `cfg953_MUTATE_firstrun_preA1.out`: the first MUTATE run, made before A1 and the reporting edits.
- Final script sha256: fedea9c142665f91…. K, MUTATE and main were all run from it.
- `DERIVATION.md` holds every equation, number, cost and disclosure.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
