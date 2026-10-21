# CFG955: is the class-A engine the coarse-grained limit of a kinetic theory of relaxing cold dust?

**Frozen-rule outcome (criteria 903cd8f1d, amendment A1 d11d47794): NOT CLASSIFIED BY THE FROZEN RULE.** The conservative reading K-T
FAILS two tests:
- **(a)**, generically: its law state is neither selected nor dynamically kept;
- **(e)**, on a 4% excess over a round-off line in the merger toy: momentum 1.04e-10 against a 1e-10 line, where relaxation-off gives
  8.6e-11.

The frozen §7 requires every FAIL to have a listed generic structural statement before it can return NO KINETIC PARENT, and (e)'s miss
has none.

**Substantive reading (post hoc, A1.3; no class weight): NO KINETIC PARENT for the hypothesis as stated.**

| reading | finding |
|---|---|
| K-ρ (f_eq's density is the phantom; the only reading whose fast limit relocates mass like E8) | **Not conservative.** Its continuity equation has a source (H0, sympy), and in the planar toy it breaks the centre-of-mass theorem (slip 7.5e-3 x_e) or momentum (8.2e-3) |
| No locally mass-conserving kinetic theory | **Has E8 as its τ → 0 limit.** Gravitating mass can only cross the edge at the flow speed (L1 flow bound). The fast probe τ/10 never comes within 0.1 of the phantom in L1 |
| K-T (local Maxwellian at the law's own Jeans temperature; conserves mass and momentum exactly; T-M solved) | **Its law state is not selected:** a second hydrostatic equilibrium has the same dust mass and the same T_J (L5), and on NGC 3198 the family deviates from the law by up to 21% at the same mass (PH2). **The law state is not kept:** every toy start collapses centrally, 69–91% of the dust inside r < 0.5 against the law's 1.2% (a3). PH4 identifies this as a Bonnor–Ebert / Antonov instability of the thermostatted SIS phantom: NGC 3198 has two unstable modes with an e-folding time of 0.21–0.25 Gyr |

**Engine relation: NONE.** E6–E8 is neither K-T's τ → 0 limit nor its late-time attractor. The T1x / T2x / NC1x shear passes do not
transfer.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy is the framework's own component: no particle species.
Framework-native inputs only. Not "theory closed". Nothing here says the data favour the framework.

## The kinetic theory (equations; DERIVATION §1)

    ∂ₜf + v·∇ₓf − ∇Φ·∇ᵥf = − Σ_D 1[x ∈ D, |x − X_b,D| < r_e,D] (f − M[ρ_d, u, T_J,D]) / τ
    ∇²Φ = 4πG(ρ_b + ρ_d)          (no phantom field, no source S)
    T_J,D(r) = (1/ρ_ph,D) ∫_r^{r_e,D} ρ_ph,D g_law dr′,   M_ph,D(<r) = r²[g_law(ḡ) − ḡ]/G,   ḡ = G M_b,own,D(<r)/r²
    M_ph,D(<r_e,D) = M_d,D (supply root; zero-sum = mass conservation),   ∂ₜe_R = −(3/2)ρ_d(T_J − T)/τ

- **Domains** are born at first turnaround and latched. In-situ systems are not domains (CFG953 R1). Cells are assigned by M1.
- **Target:** the monopole own-baryon phantom, centred on the condensed-baryon centroid. It is not the pointwise phantom, which CFG953
  excludes through the tidal dwarfs.
- **Rate:** τ_π = τ_ff/(2α), α = 1 (T1: CFG638's pressure-relaxation time).

## Tests (both footings)

| test | result | grade |
|---|---|---|
| (a) law, relaxed hosts | **a1:** NGC 3198 stationary state 1.64e-6 / 2.80e-6 (simple) and 2.9e-7 / 4.8e-7 (ν_mono). Line 1e-6: FAIL for the simple kernel; PH1 shows it is discretisation (2.1e-7 / 5.3e-7 at 2× resolution). **a2:** BTFR y = 1e-2 / 1e-3 ≤ 4.5e-7 (V⁴/(G M_b a₀) 1.105 / 1.032). **L5:** NOT UNIQUE (C₂ = 0.46–0.53 NGC 3198, 0.087 toy). **a3:** IC-L, IC-I and IC-S all collapse, NOT ON THE LAW | **FAIL** (generic through L5) |
| (b) satellites | **b1:** hover ε = 3.9e-4 (planar, uniform field). **b2:** EFE 0 dex (monopole own domain; sympy covariance). **b3:** drag ε(a) ≤ 0.211 / 0.210 (T1) against ε_B 0.344 / 0.317; ≤ 0.028 for T2 / T3 | PASS |
| (c) slip | worst s_847 1.355e-5, s_grad 6.8e-6 (line 1.9e-5) | PASS |
| (d) a¹ growth | dust n = 1 exactly; C[cold stream] = 0; no domain before turnaround | PASS |
| (e) conservation | mass exact; momentum 8.4e-12 / 1.1e-12 / **1.04e-10** (E-R / E-S / E-M; line 1e-10; relaxation-off E-M 8.6e-11); energy books close at integrator level | **FAIL** (round-off; no generic statement) |
| (f) causality | local operator, finite τ; the target is a domain functional (C-ret); dissipative, so no action | CONDITIONAL |

## Task 1: the fast-relaxation limit

- **Momentum (T-M).** K-T resolves T-M exactly: the weights are the dust masses, so R ≡ 0, with momentum 8e-12 in the asymmetric
  host. K-ρ does not resolve it.
- **RMIN.** K-T needs no RMIN: every SPARC galaxy relaxes in its own domain, giving rms 0.10033 / 0.09910 = the local law, with 0 of
  3389 points beyond an edge.
  - The engine's effective RMIN at 1024³ (M_b,ret ≥ 2.19e11, K5) is a mesh device. K-T's own PM floor (r_e ≥ 2 dx) is
    M_b ≥ 1.92e10 / 2.32e10 (×11.4 / ×9.4 lower), and 51 / 48 SPARC galaxies lie between the two.
  - No SPARC galaxy has a negative discrete phantom density.
- **Global vs own-domain phantom (T-X).** K-T has no phantom field, so no EFE (L4). The engine's E4 carries −0.10 to −0.73 dex (K3).
- **Limit.** Not a τ → 0 limit (L1); not an attractor (a3). **Relation NONE.**

## Task 3: what sets τ (no knob scan; record candidates only)

- **τ-P** (rotators and cluster cores relaxed) passes for T1, T2-fast and T3-fast. **τ-F** (rotators relaxed, cluster cores native)
  passes for **no candidate**.
- **Ordering.** min over rotators of age/t, divided by the cluster's, is 1.21 / 1.17 (τ_ff) and 1.56 / 1.50 (t_orb), against the
  21.85 needed. No proportionality constant works. A universal τ would need to be ≤ 3.5 Gyr and ≥ 57 Gyr at once.
- **Two-body** relaxation never relaxes anything. **The capture gate** cannot hold the deep law (1–22% of the law-state dust in dwarfs
  lies below V_esc,b).
- **T-EX** (CFG930 D4, Q_ap 0.14–0.32 < 1): no τ gives the dSph or Coma-UDG excess.
- Below-law systems are Newtonian for every τ: in situ, or no capture (L6).
- **Clusters:** the core deficit survives every record τ (MID Z +5.4 to +7.7). Finite τ does not make clusters native by derivation,
  so CFG949's selector stays a choice.
- **No record-derived τ works.**

## Task 4: energy

- **Net exchange** per host = CFG935's E_x: 1.6e49 erg (UFD) to 7.3e63 erg (cluster core; 3e-6 M_cat c²). The sign is dust → R.
- **Power:** MW-like 2e42 – 3e44 erg/s; cluster core 7e46 – 1e48 erg/s.
- **R must be a heat bath at T_J(x)** (L7, Clausius). On the cooling branch R must absorb entropy, so a coherent zero-entropy
  dark-energy partner (CFG542 Pb) cannot be R. No drift partner is needed. No such field is in the record.
- **CFG930's SN-energy ordering is NOT APPLICABLE** (R is not baryonic feedback), so it **does not kill** K-T. T-EX does remove the
  excess family.

## Task 5: shear-run design (not run)

`FROZEN_CRITERIA_KT1024_DRAFT.md` (**DRAFT, not frozen**) specifies the K-T PM variant:
- E4 and E6–E8 off;
- per-(host, bin) momentum-preserving resampling to the monopole own-domain T_J, every step;
- RMIN only at r_e ≥ 2 dx;
- M3 unchanged;
- CFG654's native scorer against NCS0, with HOLDS / WEAKENED / FAILS readings.

**Cost estimate:** 21–25 h per footing (+100 to +185 s per step on NC1x's 361 s), about 41–42 GB peak RSS, so about 2 days serial
for both footings.

**Caution:** given (a), the run would score a theory whose relaxed state is unstable at sub-cell scales. At 98 kpc/h the mesh may
hide the central collapse, but it cannot remove it.

## Controls

**K: 8/8 PASS** (`cfg955_K.out`; MAIN repeats them identically).

| id | result |
|---|---|
| K1 | CFG947 T-M: identity 0, E8 R = −ε(M̈_e X + 2Ṁ_e Ẋ), π²ε/4 = 0.0247 / 0.2467 / 0.7402 |
| K2 | T-R: 4.8154e10; NGC 3198 unresolved; 128 / 175 |
| K3 | T-X: −0.7298 … −0.1019 dex |
| K4 | CFG938 NGC 3198 law: 2.2e-16 |
| K5 | CFG952 RMIN node: 1.0471 Mpc/h, 2.185e11 |
| K6 | CFG941 exponents: 0.60954 / 0.69433 / 1 |
| K7 | CFG935 PHYS table; toy T_J vs CFG935's σ_J²: 2.8e-4 |
| K8 | SPARC 0.10033 @ 0.61 / 0.09910 @ 0.57; Newton 0.2755 |

**MUTATE: 5/5 bite** (exit 1 by design; `cfg955_MUTATE.out`).

| tooth | result |
|---|---|
| Mu1 | a tether gives D-T's a^0.69433 |
| Mu2 | a global phantom gives back CFG947's EFE |
| Mu3 | K-ρ relocation breaks the centre-of-mass theorem and momentum |
| Mu4 | a self-consistent target (no phantom) does not reach the law (f_esc 0.80) |
| Mu5 | relaxation off: not on the law (D −0.117) |

## Post hoc (A1.3, `cfg955_posthoc.py`; no class weight)

- **PH1.** a1's miss falls with resolution, but not monotonically: the kink at 0.32 kpc. Canonical: 1.64e-6 → 2.15e-7 → 4.95e-7.
  Alt: 2.80e-6 → 5.27e-7 → 1.85e-7.
- **PH2.** NGC 3198's equilibria at the same mass (to 0.1%) span 0–21% law deviation (C 1 → C₂). The toy's second equilibrium
  holds 0.23 / 0.52 / 0.81 of the phantom at r = 2 / 5 / 8.
- **PH3.** Collapse onset at t ≈ 13 (frozen settings), 13 (N = 40000), 13.5 (softening 0.1), 17 (τ/10) and 15 (relaxation floor
  r ≥ 0.24). With relaxation off there is none to t = 40.
- **PH4.** SIS exponents (1 ± i√7)/2 (sympy), giving a threshold r_out/r_in > e^(2π/√7) = 10.75. The toy's fastest mode e-folds in
  5.1, against an onset at about 13. NGC 3198 has two unstable modes on both footings and kernels; the fastest e-folds in 0.21–0.25
  Gyr.
- **PH5.** The energy books close to ≤ 6e-4 through t = 14, while 17% of the shells fall inside r < 0.05 and E_R climbs from 0.46
  to 57. The collapse is not an integration error. The capped MAIN runs' large ε_E comes later, from the formed core.

## Not excluded

- Kinetic theories with a relocation drift (CFG638 / CFG935 PH-OU), which held the law in CFG935. Their drift is the non-conservable
  relocation of T-M, and it needs a dark-energy partner.
- Other target temperatures. The self-consistent target fails to select the law (Mu4).
- Theories with extra degrees of freedom.

None of these is the hypothesis tested here.

## Files and commands

Run from this directory, one process at a time, `OMP_NUM_THREADS=1 nice -n 10`, with the in-script 1 GB guard. Peak RSS was 0.35 GB.
Nothing was downloaded.
- `FROZEN_CRITERIA.md` (903cd8f1d), `AMENDMENT_A1.md` (d11d47794), `DERIVATION.md`, `FROZEN_CRITERIA_KT1024_DRAFT.md` (DRAFT).
- `CFG955_STAGE=K python3 cfg955.py` → `cfg955_K.out`, `cfg955_results_K.json` (exit 0).
- `CFG955_MUTATE=1 python3 cfg955.py` → `cfg955_MUTATE.out`, `cfg955_results_MUTATE.json` (exit 1 by design; 35 min).
- `python3 cfg955.py` → `cfg955.out`, `cfg955_results.json` (exit 0; 2 h 4 min, four toy runs capped at 30 min under A1.1).
- `python3 cfg955_posthoc.py` → `cfg955_posthoc.out`, `cfg955_posthoc.json` (A1.3).
- `cfg955_firstrun_stopped_toycollapse.out`: MAIN attempt 1, stopped by hand at the stalled IC-L toy (disclosed in A1).
- Final script sha256: `cfg955.py` 214bf1b0170278a9…, `cfg955_posthoc.py` 6df8e6c6303bc4e4…. K, MUTATE and MAIN all ran from the
  former.

## Disclosures

1. **Not blind.** Every record lane in the criteria §8 was read before freezing, and the expectations were written there. Expectations
   1–6 and 8 held. Expectation 7, "(a) uncertain", resolved as FAIL. The collapse was not anticipated.
2. **Implementation choices before any number:**
   - fixed-step RK4 on tables replaced an adaptive solver that was too slow for the 401-point scan;
   - the quadrature atol was scaled to the pressure;
   - a 0.05 relaxation cadence.

   Crash-only smoke tests were run on very short runs in a scratch directory.
3. **A1** (post-result for K / MUTATE and MAIN attempt 1's static lines; pre-result for the toys): the 30-min toy cap, the literal
   class rule (the code's fallback had returned NO KINETIC PARENT on any FAIL), and PH1–PH5. MAIN attempt 1 was stopped by verified PID.
   The collapse diagnostics were first run in scratch, then reproduced in `cfg955_posthoc.py` (PH3).
4. **The capped runs' energy books** are poor at the cap (ε_E 0.31–1.6). The collapsed core is integrated inside the softening. The
   collapse onset itself is robust (PH3, PH4, PH5).
5. **K and MUTATE were rerun from the final script** after the A1 code changes. Both outputs are identical to the first runs apart
   from timings.
6. **Engine constants** (the census, M_ta's 0.315) are inherited, as in CFG947.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
