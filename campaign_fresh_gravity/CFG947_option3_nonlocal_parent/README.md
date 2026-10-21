# CFG947: option 3, a non-local causal parent of the class-A engine

**Lane label: NO-GO (exact parenthood).** No non-local, causal parent can have the class-A engine as its exact
non-relativistic (NR) limit and also pass the static law, satellite and SPARC tests. Three obstructions show this, and each is
a property of the engine's own equations:
- **T-M:** the relocation rule (E8) cannot be covariantly conserved.
- **T-R:** RMIN switches the law off for 128 of 175 SPARC galaxies.
- **T-X:** the phantom (E4) carries the host external-field effect (EFE) that CFG478 excludes.

The T1x / T2x / NC1x shear passes transfer to no parent tested here.

On the positive side:
- The hover of CFG941 does not arise. Class-A-type parents leave free fall universal (Δa/g_host = 0).
- Zero-sum is forced by conservation rather than chosen.
- Linear growth is a¹.

**Settings and provenance.**
- **Criteria:** `FROZEN_CRITERIA.md`, 9c683a634, committed alone first. **A1** (pre-result, committed alone): fad3a6b86. Block
  940–949.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy; no particle species. Framework-native inputs only.
- Not "theory closed". Nothing here says the data favour the framework.

## The construction tested

**Chassis.** G_μν = 8πG(T^b + T^c + 𝒮)_μν, built from three pieces:
- geodesic baryons;
- cold dust with no tether;
- a non-local sector 𝒮.

𝒮 is conserved by construction. Its current is J_s = ∂·𝒬 with 𝒬 antisymmetric, so in the NR limit ρ_s = −∇·𝒫 and
j_s = ∂ₜ𝒫 + ∇×M. Every kernel is retarded.

**No action principle.** Retarded non-local equations are not Euler–Lagrange equations of any action. The action form uses the
time-symmetric kernel and is acausal: Mu2 finds a precursor of ½ the static value before the source switches on. So option 3
cannot satisfy both CFG678's one-action rule and causality.

**A code-reading finding.** The engine's phantom (E4, in forces()) is the pointwise QUMOND phantom of the *global*
retained-baryon field. It is not the "own-baryon per structure" rule that CFG941 and the brief describe.

| candidate | domains | phantom | class |
|---|---|---|---|
| N1 | first-turnaround labels (latched; optional merge rule M-R) | own domain | **NOT VIABLE**: a FAIL (S2 kernel), d FAIL (T-M), g FAIL; f PASS, h CONDITIONAL |
| N2-E | engine-verbatim: balls of r_ON ≥ RMIN, M1 partition | global (E4) | **NOT VIABLE**: g PASS, but a, d, f, h FAIL |
| N2-B | basins of a retarded turnaround potential ψ (smoothed at L*) | own domain | **NOT VIABLE**: a FAIL (S2 kernel), d FAIL, g FAIL; f, h PASS |
| N3 | none (Deser–Woodard-type smooth gate) | global | **NOT VIABLE**: d3 FAIL (negative density), f FAIL, g FAIL, h FAIL |

## Key results (all from `cfg947.py`, both footings)

| test | result |
|---|---|
| T-Z zero-sum | forced: 𝒮 ≡ 0 on FRW plus ∇·𝒮 = 0 give ∫ρ_s = 0 for all time. Removing it (Mu3) creates 53.65 M_b of 𝒮 at switch-on |
| T-M momentum | constant weights conserve (identity to 7e-18), even though F_ms ≠ 0. E8's relocation gives R = −ε(M̈_e X + 2Ṁ_e Ẋ) ≠ 0, i.e. π²ε/4 of the domain's weight scale (0.25 at ε = 0.1). The engine is not conservable in asymmetric catchments |
| T-E forced edge | M_law(< r_ON)/M_ta = 1.85–9.72 for M_b = 1e7–1e15. Zero-sum plus positivity force the law to end at r_e < r_ON. E7's ln formula is exactly the ν_RAR / ν_mono supply root (q − 1 = 5e-9); for the S2 kernel q = 1 + x²/24 |
| T-R RMIN | resolved iff M_b ≥ 4.815e10 M⊙ (either footing). NGC 3198 (4.72e10) is just below (2%); 128 of 175 SPARC galaxies are below |
| T-X EFE fork | global phantom −0.10 to −0.73 dex on CFG882's dwarfs at 50–250 kpc; own-domain phantom 0 |
| T-L labels | deep factor √f + √(1 − f). NGC 3198 errors: 8.6% at f = 0.01, 24% at 0.1, ×9 for 100 equal labels. N1 needs M-R |
| T-N3 | a domain-free gate leaves negative total density (−7.6 to −69 ρ̄_m): domains are forced |
| T-F hover | Δa/g_host = 0 at monopole order (retardation ≤ 1.2e-6), against CFG941's 1.02–1.11; Mu1 (local tether) brings theorem D-T back |
| (a) NGC 3198 | N3 exact. N1 / N2-B fail only on the S2 kernel (cap trims 1.2e-5; ν_mono 4e-9; kernel's own supply root 2e-16). N2-E is unresolved, so the law is off (0.83) |
| (b), (c) | PASS for all (𝒮 ≡ 0 on FRW and in the linear regime; n = 1; gates open only at turnaround, top-hat 9π²/16) |
| (d) | all FAIL on d5 (T-M). N2 also fails d4 (r_ON jumps 20.6%, edge 41%); N3 also fails d3 |
| (e) slip | worst 1.63e-5 (the cold's own isothermal pressure); 𝒮 stress 1.30e-5 / 1.42e-5; all ≤ 1.9e-5 |
| (f) satellites | f1 PASS for all. f2: N1 / N2-B 0 dex, N2-E / N3 up to −0.73 dex. N2-B's basin cap keeps only 0–16% of the phantom under the settled cold profile (reported) |
| (g) | only N2-E reproduces E1–E11 |
| (h) SPARC | N1 / N2-B / N3 0.1003 / 0.0991 (= local); N2-E 0.257 / 0.262 (FAIL). N1 without M-R (0.9 / 0.1 labels): TENSION |
| (h) binaries | QUMOND EFE for all, CFG653's 1.179 / 1.244 (PASS / TENSION) |
| (h) satellites | CFG478: own-domain candidates PASS, global-phantom candidates FAIL |

**Escaping CFG653.** Option 3 separates by *membership* (labels, basins), not by *scale*, so own-domain phantoms have zero host
EFE. Three further differences:
- The zero-sum compensation sits at 6–54 r_M, beyond the SPARC data.
- The cap prevents CFG653's overshoot below Newton.
- Binaries behave as in CFG653's L ≥ 30 kpc candidates.

The global-phantom candidates fail the satellites exactly as CFG653 and CFG478 do.

**Open, not tested.** An approximate parent may exist: N1 with the merge rule, a dipole-free draw, the engine's kernel, a
non-variational latch, and no action. It would be "a non-local theory, not class A's parent". Its shear performance would need
its own PM engine and a 1024³ run.

## Controls

**K: all pass.**
- K1 CFG938's NGC 3198 law: 2.2e-16.
- K2 CFG941's exponents: 0.60954 / 0.69433 / 1.
- K3 CFG653 / CFG4 SPARC: 0.1003 @ 0.61 / 0.0991 @ 0.57; Newton 0.2755.
- K4 CFG938 slip: 1.5398e-5.
- K5 CFG941 hover and EFE: 1.017–1.107; −0.73 to −0.10 dex.

**MUTATE: all teeth bite (exit 1 by design).**
- Mu1: the local tether brings D-T back.
- Mu2: the time-symmetric kernel is acausal.
- Mu3: without zero-sum, 𝒮 is created.
- Mu4: the global field brings the EFE back.
- Mu5: with no cap, the shell density goes negative.

## Files and commands

Everything runs on one core, nice 10, at peak RSS 0.18 GB, about 5 s per stage. Nothing was downloaded, and no other lane was
touched.
- `CFG947_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg947.py` → `cfg947_K.out`, `cfg947_results_K.json` (exit 0).
- `CFG947_MUTATE=1 …` → `cfg947_MUTATE.out`, `cfg947_results_MUTATE.json` (exit 1 by design).
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg947.py` → `cfg947.out`, `cfg947_results.json` (exit 0).
- `DERIVATION.md`: equations, every number, the (g) table, the CFG653 comparison and the disclosures.
- `cfg947_firstrun_TLcheck.out`: run 1. Its only difference is the T-L line, a sympy simplification defect fixed by a numeric
  check.
- Final script sha256: 48fa85c8….

## Disclosures

Full list in DERIVATION §10:
- A1 (pre-result) corrected T-M's falsifier.
- Implementation choices were made in code before the first run.
- Run 1's T-L check was fixed.
- The d5 flag is now derived from computed values; all stages were rerun with identical outputs.
- NGC 3198 sits 2% below the RMIN threshold, so N2-E's (a) on that galaxy alone is fragile. Its SPARC failure is robust.
