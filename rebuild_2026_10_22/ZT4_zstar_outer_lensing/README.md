# ZT4_zstar_outer_lensing: Z-T4 of Z★ (v3s-OC), outer isolated-galaxy lensing with the truncated law

## Verdict: PASS on both footings (frozen line), at both f_own ends and on both backgrounds

The test line is Z1 `TEST_PLAN.md` §2 "Z-T4" (0d1959a4f5). It asks for Δχ²(Z★ − zero-field v3) ≤ +4 on P2's
spectroscopic sample at both ends of f_own ∈ {5.364, 50}. Every one of the 8 verdict numbers is negative.

What the PASS means, and what it does not:
- **It is a test the truncated law could have failed and did not.** It is not evidence for Z★ over anything else.
- P2's outer stack sits **below** zero-field v3: at 1.1–2.6 Mpc, A_O2 = −0.16 ± 0.42. Any model that is lower out
  there gains χ². Z★'s supply edge lowers the model, so it gains.
- The gain is modest. Zero-field v3's outer χ² is 14.2 (canonical) / 16.3 (alt) on 7 bins.
- **Cost inside, reported only.** At f = 5.364 the edge sits at 73 / 67 kpc for the median lens. That costs
  Δχ² = +4.9 / +5.6 on the inner range (0.03–0.31 Mpc), where the data already sit at 1.8× v3's baryons-only profile.
  At f = 50 the inner cost is −0.1.
- Nothing here says the data favour the framework.

κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m/s² (alt), scored separately, never pooled. No
dark-matter particle: the cold sector is one pressureless medium. Not theory closed.

## The numbers

Outer range 0.4 < R ≤ 3 Mpc (7 bins), S3 Δ = L − I3 (2,251 lenses), P2's 36-patch jackknife covariance with Hartlap
0.771. Each cell is Δχ² = χ²(Z★) − χ²(v3, y_e = 0). Two-halo bias b = 1.

| footing | χ²(v3 a) | f 5.364, bg A | f 5.364, bg B | f 50, bg A | f 50, bg B | verdict |
|---|---|---|---|---|---|---|
| canonical | 14.19 | −8.39 | −8.47 | −4.82 | −5.02 | **PASS** |
| alt | 16.25 | −10.45 | −10.54 | −6.53 | −6.74 | **PASS** |

**Profiles, canonical (M☉/pc²)**, at R = 0.41, 0.55, 0.75, 1.02, 1.39, 1.89, 2.57 Mpc:

| | values |
|---|---|
| data Δ | 8.0, 0.3, 1.9, 0.4, 0.4, −0.8, 0.1 |
| v3 (a) | 5.3, 4.0, 3.0, 2.3, 1.7, 1.3, 1.0 |
| Z★ f 5.364 (A) | 1.4, 0.8, 0.6, 0.4, 0.4, 0.4, 0.4 |
| Z★ f 50 (A) | 5.5, 4.2, 3.0, 1.9, 1.2, 0.8, 0.6 |

The two-halo term (b = 1, z 0.225) is 0.16–0.33 (A) and 0.14–0.30 (B) over the outer bins.

**Reported only, not verdict lines** (canonical / alt; the A background is shown, B differs by ≤ 0.2):
- No two-halo term: f 5.364 −9.24 / −11.30; f 50 −7.08 / −8.84.
- Full 15 bins: f 5.364 −2.84 / −3.92; f 50 −3.49 / −4.87.
- Inner 6 bins: f 5.364 +4.87 / +5.58; f 50 −0.12 / −0.11.
- Diagonal-only outer: f 5.364 −8.2 / −10.4; f 50 −5.2 / −7.2.
- Two-halo without T_nbr (double-count bracket): f 5.364 −8.4 / −10.4; f 50 −6.1 / −7.9.
- Sheth–Tormen bias of (1+f) M_b (S3 median b 0.87 / 1.08): f 5.364 −8.6 / −10.6; f 50 −4.7 / −6.4.
- S1 (10,620 lenses, L − I1, P2's secondary): f 5.364 +3.1 / +0.8; f 50 −9.1 / −11.5.
- P2 amplitudes for Z★, canonical: f 5.364 A_O1 2.9 ± 1.8, A_O2 −0.6 ± 1.5; f 50 A_O1 0.59 ± 0.38, A_O2 −0.24 ± 0.67.
  For v3 (a): 0.57 ± 0.38, −0.16 ± 0.42.
- Supply radius of the median S3 lens (log M_b 11.02): r_M 12.5 / 11.4 kpc; r_s 73 / 67 kpc (f 5.364) and
  632 / 575 kpc (f 50).

## What was done

The criteria and ledger were committed alone first (8cdfbc843e). There is no amendment.

**Pipeline.**
- P2's script is executed read-only in this lane's process up to its verdict loop, on a copy of P2's scratch caches.
- That reuses P2's samples, KiDS measurement, estimator, covariance, neighbour pairs and v3 machinery.

**Owner (lens and every neighbour).**
- Isolated AQUAL with μ = x/(1+x), in the owner frame, so there is no EFE.
- Enclosed mass capped at (1+f) M_b, with M_b = M★ + cold gas + hot CGM.
- For a point mass this is exactly r_s = r_M √(f(f+1)) (Z1 K5).

**Two-halo term.**
- Formula: b ρ̄_c (1+z)² ∫ k dk/2π P_lin(k, z) J₂(kR(1+z)), with P_lin from CLASS.
- Background A is the C2 refit and background B is CFG886, both with F3 K2 parameters.
- b = 1 is POSITED. Only the lenses carry it; random points carry b = 0.

**Checks: 6/6 PASS.**
- K0: P2 replay. The profile matches exactly, and the committed v3 outer χ² reproduces at 14.1927 / 16.2518.
- K1: the f → ∞ limit equals P2's model to 4e-8.
- K2: the cap identity is exact.
- K3: σ₈ agrees with CLASS and F3 to 7e-6, and the J₂ Gaussian test to 7e-16.
- K4: the covariance is positive definite.
- K5: peak RSS is 0.52 GB in phase C and 0.81 GB in phase S.

`--mutate` (cross shear as data) fails K0, and the run exits 1 (`*_MUTATE.*`).

**Run.** `OMP_NUM_THREADS=1 nice -n 15 python3 zt4_outer_lensing.py <KiDS reader cache> <copy of P2 work dir>`. It takes
about 1 min, single thread, with no downloads.

## Scope and limits

- **The verdict rests on P2's outer deficit.** P2 itself is UNDECIDABLE for the EFE question because its sample is
  small. The same noise lets a truncated profile score well.
- **The two-halo term is the unconditioned linear mean.** S3 lenses are selected as isolated, and that conditioning
  is not modelled. b = 1 is posited, and the Sheth–Tormen alternative is reported.
- **Catalogued neighbours' owned mass is counted twice**, once in T_nbr and once inside ξ_lin. The bracket without
  T_nbr changes no class.
- **f_own is history-dependent**, and one f is used for every galaxy at each end. No f was scanned.
- **Mixed backgrounds.** P2's distances use h 0.679 and Ω_m 0.3085, while P(k) uses background A or B.
- **F2 (the secondary) was not run.** Its B21 g_bar-binned model is a different pipeline, so scoring it would need its
  own frozen implementation. F2's verdict is also not robust to host leakage (its A1).
