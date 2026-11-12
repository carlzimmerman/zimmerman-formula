# WM1 RESULT: FAIL AT SEEDING / FAIL AT SEEDING (criteria 6e40130dfa, A1 5cba17a249, A2 c830b470e0)

## A2 update: gate 0, seeding (graded first; added after the first result, disclosed in AMENDMENT_A2.md)

**Label: FAIL at seeding on canonical and alt.** Every gate below keeps its status and numbers. The first result (d45cfa36da) read
FAIL / FAIL with first failing gate 2, groups.

**What gate 0 tests.**
- CLASS transfers at z 1000 / 950 set the start: Silk-damped, drag-released baryons, and the relic's own cut.
- They run through the two-fluid ODE with the law on (A1's nu), Newton beside.
- Press-Schechter n(> M) with the sharp-k filter (c 2.5) is graded against 0.5 x the cold reference (a disclosed line).

**Known answers.**
- KA-S2: cold Newton ODE vs CLASS = 1.014 flat at k 0.5-5 h/Mpc: PASS.
- KA-S1 for W: 1.016 / 1.024 / 1.051 at k 0.5 / 1 / 2 h/Mpc: PASS.
- KA-S1 fails for the lighter MW1 and the source's relic (+20-30 % at k 2). The ODE omits free streaming after z 1000, so it
  over-states their small-scale power. That bias favours formation, so their FAILs are conservative.
- KA-S3: sharp-k / top-hat 0.94 at 1e12.

**Seeds at z 1000** (relative to the cold total matter, W):

| quantity | k 0.5 | k 1 | k 2 | k 5 h/Mpc |
|---|---|---|---|---|
| delta_b | 0.0115 | 0.0088 | 0.0030 | -0.0002 |
| delta_chi | 1.46 | 1.18 | 0.40 | -0.02 |

**Power relative to the cold reference, W, canonical:**

| z | quantity | k 0.5 | k 1 | k 2 | k 5 h/Mpc |
|---|---|---|---|---|---|
| 3 | P_m, law on | 5.1 | 5.1 | 0.99 | 0.0036 |
| 3 | P_m, Newton | 0.93 | 0.60 | 0.064 | 7.6e-5 |
| 3 | P_b, law on | 46 | 57 | 14 | 0.066 |
| 0 | P_m, law on | 25 | 34 | 10 | 0.076 |
| 0 | P_b, law on | 397 | 641 | 222 | 2.0 |

- The law amplifies the residual seed: at k 2 it turns a 0.064 Newtonian deficit into a 10x excess at z 0.
- Above about 3 h/Mpc the seed is too small to amplify. At k 5, P_m stays at 0.004 (z 3) and 0.08 (z 0).

**Halo abundance n(> M) / reference** (sharp-k; law on, Newton in brackets). Canonical; alt agrees to 10 %:

| relic | M | z 2 | z 0 |
|---|---|---|---|
| W 188.7 eV | 1e10 | 0.014 (0.003) | 0.010 (0.011) |
| W | 1e11 | 0.13 (0.024) | 0.061 (0.073) |
| W | 1e12 (reported) | 1.06 | 0.28 |
| MW2 376.7 eV | 1e10 / 1e11 | 0.12 / 0.67 | 0.065 / 0.23 |
| MW1 94.5 eV | 1e10 / 1e11 | 0.0015 / 0.013 | 0.0019 / 0.011 |
| source 107.5 eV | 1e10 / 1e11 | 0.0023 / 0.021 | 0.0025 / 0.015 |

The line is 0.5. Every relic fails at 1e10 and 1e11, at both z, on both footings, including MW2 at 377 eV.
- Galaxy-scale halos form at 1-13 % of the reference abundance.
- The law does not repair this. It raises the 1e12 and larger halos and drains mass from the smaller ones: n(> 1e10) at z 0 is
  0.010 with the law and 0.011 with Newton.
- The seeding wall that the source and the orchestrator foresaw holds. The law amplifies what exists; it cannot put back what
  free streaming removed above about 3 h/Mpc.
- **Disclosed approximation:** PS with delta_c 1.686 on law-boosted linear power is generous to formation.

**Nonlinear response (not computed).** The linear system cannot couple modes.
- In standard WDM simulations, structure below the cut forms top-down by fragmentation of larger collapsed structures, not as
  independent halos.
- Under the law, nu varies with the large-scale field. That multiplies the existing g_N and generates harmonics of the large modes
  as they collapse, i.e. power at higher k.
- Whether that yields 1e10-1e11 halos in the observed numbers needs an N-body or sheet run with the law (SS5's 1D sheet is the
  nearest tool, in another lane). Not claimed here.

**The source's round-16 numbers, checked (never adopted).**

| item | source | this lane |
|---|---|---|
| M_hm at 107.5 eV | 2.0e13 (its 1.19e10 (m / keV)^-3.33) | Viel half-mode 3.23e13 (the source's formula runs 0.62x Viel at every m; at 188.7 eV 3.07e12 vs 4.97e12) |
| k_hm at 107.5 eV | 0.43-0.44 h/Mpc | CLASS 0.81 h/Mpc. The source's k is about half; its free-streaming effects are overstated |
| capture f, its form and its M_hm: lenses at M* 10^10.5 / 11 / 11.3 / 11.5 | 1.1 / 3.3 / 6.8 / 11.2 % | 0.9 / 3.2 / 6.5 / 10.2 % (reproduced) |
| capture f, groups raw | (34 / 48 / 62 % with its asserted core) | 52 / 68 / 84 %. The core is not modelled |
| capture f at W's M_hm (lenses / groups) | | 4 / 13 / 23 / 31 % / 78 / 87 / 94 %. Under the source's form, W's heavy lens bins would exceed option (c)'s 0.05 |
| primary TT at 107.5 eV | < 0.15 % at l < 800; -1.2 % at l 2500 | max 0.51 % at l < 800; -0.48 / -0.56 % at l 2500 |
| C_L^phiphi warm / cold at L 100 / 300 / 1000 | -0.3 / -3.2 / -42 % | -0.2 / -1.3 / -11 % |
| lensing at L 1000 with the law's phantom | -12 to -22 % | **wrong sign.** On the record's law-on-web reading the law multiplies C_L^phiphi (S_B 4.3 at L 400, the last saved L; B_m >= 3 at every k), so it cannot suppress |

---

# Earlier result (d45cfa36da): FAIL / FAIL, first failing gate 2 groups (criteria 6e40130dfa, amendment A1 5cba17a249)

The lane grades a warm thermal relic (omega_chi = 5.41 omega_b) plus baryons that obey the a0 law. TEST lane, quarantined; the
no-particle rule is lifted for this lane only. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.

**Label (frozen order 1, 2, 3, 5, 5b, 6, 7a, 7b-N, 7b-L, 8, CS, 9, 10): FAIL on canonical, FAIL on alt. First failing gate: 2,
groups.**
- Also failing: 3 X-COP, 7b-L (CMB lensing with the law on the web), 8 (forest and fsigma8), CS (S8), 9 Bullet.
- Passing: 1 KiDS (spent by the M_hm rule), 5 SPARC, 5b UMa, 6 BAO+SN, 7a CMB primary, 7b-N (CMB lensing at the cutoff), 10 Cassini.
- Known answers: all pass. Fitted constants: 0. M_hm is set by the frozen rule from two record numbers.

## The relic, fixed once

- **Rule:** the suppression S(M) = (1 + M_hm/M)^-1.16 equals 0.050 (option (c)'s compact allowance) at the heaviest KiDS bin's
  primary halo, M200 4.06e11. This gives **M_hm = 4.97e12 Msun**.
- **Mass (Viel 2005 half-mode):** **m = 188.7 eV**, T_ncdm 0.2799.
- **CLASS check (KA-W3):** omega_ncdm 0.12094 = target. Half-mode k 1.488 h/Mpc vs 1.503 from the fit (ratio 0.990).
- **P_warm / P_cold at z 0:** 0.998 / 0.969 / 0.578 / 0.001 at k 0.1 / 0.3 / 1 / 3 h/Mpc.
- **Construction:** each system holds S(M200) times SS1's primary halo (KD1 P3, truncated SIS).

## Gate x footing (canonical / alt)

| gate | canonical | alt |
|---|---|---|
| 1 KiDS | PASS, max 0.042 (0/59 over) | PASS, 0.042 |
| **2 groups** | **FAIL** 7/20 and 0/20; medians -0.07 / -0.25 (over-filled) | **FAIL** 8 and 0; -0.10 / -0.28 |
| **3 X-COP** | **FAIL** mean -0.202, rms 0.230; bins -0.29 / -0.14 / -0.15. Retained / M_dyn 1.51 / 0.87 / 0.71 vs TR1 0.71 / 0.66 / 0.58. TR1 SHAPE follows (RMS 0.075) | **FAIL** -0.221 / 0.246; same fractions; SHAPE RMS 0.071 |
| 4 Coma UDGs (reported) | +1.28 dex (law alone +1.12): FAIL as HC1 | +1.25 |
| 5 SPARC | PASS | PASS |
| 5b UMa | PASS, Delta -0.004 | PASS |
| 6 BAO+SN (CLASS warm vs cold, fixed h) | PASS, +0.058; r_d 146.869 vs 146.870 | PASS, +0.058 |
| 7a CMB primary (qx15 PA, warm minus cold) | PASS, +0.016. TT warm/cold 0.993 at L 3000, 0.778 at L 5000 | PASS, -0.016 |
| 7b-N lensing at the cutoff (HC1 G9, 8 corners, footing-free) | PASS, worst 9.28, best 8.34 (line 18.48) | (same) |
| **7b-L lensing, law on the web** | **FAIL** chi^2 107.9. C_L boost S_B 17.5 / 6.3 / 4.6 / 4.2 / 4.3 at L 10 / 40 / 100 / 200 / 400; A_s refit x 0.199 | **FAIL** 128.1 |
| **8 forest + fsigma8** | **FAIL** forest Delta chi^2 1.08e6 (gas tracer 1.8e8). fsigma8 growth-rate ratio 5.57 / 5.00 / 4.59 / 4.24 (BGS to LRG3; line <= 1.001 and data within 2 sigma) | **FAIL** 1.75e6; 6.56 to 4.88 |
| **CS** | **FAIL** sigma8 x 3.64, S8 +264 % (line 5.9 %). P / P_ref 13.3 / 23.2 / 0.31 at k 0.3 / 1 / 3 h/Mpc, z 0.3 | **FAIL** x 4.17, +317 % |
| **9 Bullet** (galaxy-traced) | **FAIL** M300 Z +1.53 / -1.00 (S 0.995 / 0.960); gas-traced also FAIL | **FAIL** +1.92 / -0.66 |
| 10 Cassini | PASS | PASS |

**Linear growth with the baryons on the law** (D1, graded nu per A1). B_m is the boost of delta_m over Newton.
- At z 0.02, B_m = 4.55 / 3.21 / 3.26 / 4.17 / 7.44 / 17.9 at k 0.01 / 0.03 / 0.1 / 0.3 / 1 / 3 h/Mpc (canonical).
- delta_b / delta_chi = 8.3 / 6.4 / 6.5 / 7.8 / 11.3 / 17.5 at the same k.
- Alt runs 15-30 % higher.
- A1 bracket (the frozen warm-P nu, k <= 1 h/Mpc): B_m 4.55 / 3.21 / 3.27 / 4.22 / 9.86, which is larger.

**Newtonian warm readings (B = 1; reported).**
- S8 -0.8 %, fsigma8 ratio 0.992 (PASS).
- P / P_ref 0.97 / 0.58 / 0.0015 at k 0.3 / 1 / 3 h/Mpc.
- Forest Delta chi^2 1.67e5: FAIL. A 189 eV relic is excluded by the forest without the law (MN-W, the gate has power).

## Verifying the FAILs

- **Groups and X-COP.**
  - Clusters keep S >= 0.96, which is the full share (as SS2's G: 1.57 / 0.90 / 0.75).
  - Groups fail in every bracket and MUTATE: W3 9/1, Wthird 1/6 (alt 3/2), MW1 4/0, MW2 3/0.
  - X-COP fails at every M_hm: mean -0.18 to -0.22, inner bin -0.27 to -0.31.
  - The inner-bin over-fill (1.5 vs 0.71 of M_dyn) is independent of the cutoff. The shape follows TR1 (as SS2); the amount is 1.3-2x.
- **7b-L, 8, CS.**
  - They fail at every M_hm (7b-L 105.8-115.8, sigma8 x 3.47-3.69, fsigma8 ratio 4.0-5.7).
  - They fail under the gentler graded nu (A1). The frozen warm-P nu gives a larger boost.
  - This is SV5's wall. WM1 belongs to SV5's class W: the law on the linear web boosts baryon growth whatever the component does.
    The cutoff only removes component power above k_hm, which lowers y and raises nu there.
  - The SV5 statement applies exactly. Under the law, linear baryon growth runs 3-18x too fast at k 0.01-3 h/Mpc.
  - The component's free streaming cannot cancel that boost: it acts only above k_hm, while the boost is already 3-5x at k 0.01-0.3.
- **Bullet.**
  - It fails in every reading: W, MW1, MW2, W3, Wthird, and Racc (S = 1).
  - Its KA row (component 0, law alone) also fails, as on the record.
  - Both subclusters keep the full share, so the main subcluster's M300 is over-predicted (Z +1.5 / +1.9).

## Known answers (all pass)

| check | result |
|---|---|
| KA-W1: HC1 G9 with its 11.1377 eV relic | worst / best 194.24 / 165.96 (HC1 194.2 / 166.0) |
| KA-W2: SS5 D1 reproduced (ss5.py executed read-only) | max rel dev 3.0e-5 both footings; z 0 b/chi 6.52 / 7.87 / 11.4 / 17.6 |
| KA-W3: CLASS omega, half-mode | omega exact; k_hm ratio 0.990 |
| KA-W4: component -> 0 replay (SS1 KA3) | PASS both |
| MN0: baryons Newtonian + cold limit | forest Delta chi^2 0, lensing 8.559852 = reference |

## MUTATE and brackets

- **MW1 (M_hm x 10, 94.5 eV): NO BITE** under the frozen status-vector rule. Every gate keeps its status: groups 4/0, X-COP FAIL,
  7a +2.1, 7b-N 9.50. The numbers move: KiDS 0.003, P / P_ref at k 1 h/Mpc, z 0.3: 1.6 vs 23.
  - The label is set by gates that do not depend on M_hm (clusters, the SV5 wall). Disclosed.
- **MW2 (M_hm / 10, 377 eV): BITES.** KiDS fails (max 0.219, 45/59 over); on alt, SPARC fails too.
- **MN-W (baryons Newtonian, warm):** the forest fails (1.67e5), so the forest gate has power.
- **Brackets (reported):**
  - W3 (136 eV): no gate moves.
  - Wthird (262 eV): KiDS fails (0.109).
  - Racc (S = 1, the secondary-infall reading): KiDS 0.374, SPARC, groups, X-COP and Bullet all FAIL.
- **Which reading the dynamics favour (D1):** r = 1 and delta_b grows 6-17x the component on the same peaks. So the component sits
  in the wells the law-boosted baryons dig.
  - Linear dynamics favour R-acc (infall), not the halo-mass-function reading S.
  - Under R-acc, galaxy halos keep the full share and KiDS fails at 0.37 (as SS1 MG3 / SS4 MK1).
  - So S is an optimistic reading.
- **KiDS 2-halo:** NOT EVALUATED; the record has no 2-halo machinery. Hand estimate: the missing galaxy-halo share sits in the field
  and in groups, and isolated lenses are selected away from groups. Not a decider here.

## Reading

- **What the warm relic does.** It does the two things it was built for: it leaves galaxy-scale halos nearly empty (KiDS, SPARC
  and UMa pass), and it stays harmless to the CMB.
  - Primary: Delta chi^2 0.02. Lensing at the cutoff: 9.3 vs the 18.5 line, because k_hm 1.5 h/Mpc sits above the lensing kernel.
  - BAO+SN: +0.06.
- **What it cannot do.**
  - Groups and clusters keep their full share, which over-fills them. Groups fail first, and X-COP's inner bin holds 1.5 M_dyn
    vs TR1's 0.71.
  - Baryons on the law grow 3-18x too fast on every linear scale. This is SV5's wall: S8 x 3.6-4.2, lensing chi^2 108-128, the
    forest off by 1e6.
- **The cutoff cannot fix either failure.** Clusters sit far above any M_hm that keeps galaxies empty. The law's boost on the web is
  largest exactly where the component's power is already gone.

**What a repair would need:**
1. A cluster-scale reduction of the component to 0.4-0.7 of the share in a TR1-like extended profile. A free-streaming cutoff cannot
   do this, since S -> 1 above M_hm.
2. A linear-web rule in which the baryons' peculiar field is Newtonian (nu = 1) at y ~ 1e-3 to 1e-1. Under the a0 law as written,
   no component choice removes the 3-18x boost (SV5 class W).

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Amendment: `AMENDMENT_A1.md`.
- Scripts:
  - `wm1_local.py`: gates 1-5b, 10 and the Bullet, through SS1 and DB1, read-only.
  - `wm1_cosmo.py`: CLASS warm, D1, gates 6, 7b-L, 8, CS, KA-W2/W3, MN.
  - `wm1_cmb.py`: 7a.
  - `wm1_hc1.py`: 7b-N, KA-W1.
  - `wm1_grade.py`: the gate table.
  - `run_local_chain.sh`, `run_cosmo_chain.sh`.
- Outputs:
  - `wm1.json` / `wm1.out`, `wm1_MUTATE.json` / `wm1_MUTATE.out`.
  - `parts/` (local, uma, Bullet, cosmo, cmb7a, g9).
  - Logs `run_*.txt`.
- Compute:
  - One thread, nice 10. Local runs 0.11 GB.
  - Cosmology 0.52 GB peak with CLASS. 7a 1.67 GB peak with CLASS at l_max 8600 (disclosed).
- Operational: SS1's local battery needs PJ1's module, which is absent from this checkout's closure_2026_11_08. A read-only extract of
  origin's PJ1 lane dir was used via SS1_PJ1_DIR (as SS1 did), in scratch, outside the repo.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
