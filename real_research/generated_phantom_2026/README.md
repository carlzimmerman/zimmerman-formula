# generated_phantom_2026: a MOND kernel sourced only by bound baryons

The record closes three routes to a phantom that follows galaxies without spoiling cosmology:

- A **conserved** phantom carried by a dark fluid. BSX3 and PAPER33 v2 close the khronon-dust aether for any kinetic function.
- A kernel that reads the **whole web's field**. The external-field effect excludes it on KiDS-1000 (BS2, BS3, L355).
- A switch on the kernel's **flux**. It is Gauss-cancelled at its edge (L352), which gives the KiDS–forest pincer (L358, L362).

These lanes build the route the record listed but had not built: switch the kernel's **source**, not its flux. Only baryons in bound regions feed the kernel. The web's gas, the forest and the dark component are invisible to it. By reciprocity they feel Newtonian gravity only. Light sees the phantom.

GP0 is a census library that the other lanes import. It has no MUTATE control; its checks are sum rules plus documentary tables.

| Lane | Script | Checks | Result |
|---|---|---|---|
| GP0 | `GP0_bound_baryon_census.py` | 4/4 | **Halo-model census of bound baryons.** Built on Sheth–Tormen (sum rules exact), Moster+13 with satellites (Ω_* = 0.0029 at z = 0), and cold and X-ray gas. The bias-weighted bound-baryon fraction at z = 0.25 is β_B = 0.0089 (stars), 0.013 (stars + cold gas), **0.042 (observed: plus group/cluster gas)** and 0.106 (every halo baryon). It also includes a Monte Carlo of discrete bound clumps at KiDS-isolated lenses. |
| GP1 | `GP1_generated_phantom_construction.py` | 6/6 (MUTATE w ≡ 1: N1 fails, rc = 1) | **The construction.** It is L353's action with the subtraction pair extended to unbound baryons, `λ(∇²v − 4πG[ρ_d + (1 − w)ρ_b])`, where w = w(x_m) is a switch on the matter density.<br>**N1:** the Euler–Lagrange equations show the kernel reads only the bound baryons. The metric is Newtonian(all) + phantom. Unbound gas and the dark component feel Newtonian(all).<br>**N2 (Gauss):** past a 250 kpc edge, M_dyn(1 Mpc) = 101–106 M_b, against 1.0 for a flux switch.<br>**N3:** the linear response of the Lagrangian form `S* div[q′∇S u_B]` is reciprocal to 1.6e-5. **BK1's one-S form is not (3.3e-2)**, and the action's form lowers the lensing mass by 6–11% at 1 Mpc and by 22–35% at 2.6 Mpc.<br>**N4:** a baryon entering a bound region falls down a potential step of speed √(2\|Φ_ph\|) ≈ 176 / 402 / 682 / 954 km s⁻¹ (dwarf / Milky Way / group / cluster, λ = 2 Mpc), about 2–3 v_flat².<br>**N5:** the density switch's back-reaction is ≤ 2e-6 on the metric and ≤ 2e-2 on the khronon. A switch built from the leaves' curvature would be 0.07–2.3. The density switch is tensor-blind, so c_T = 1. |
| GP2 | `GP2_kids_bound_source_kernel.py` | 11/12 (W1 fails, recorded; MUTATE whole matter field: E2, W1 fail, rc = 1) | **KiDS-1000**, using BK1's machinery unedited and the Lagrangian form.<br>The kernel's field at isolated lenses (observed census) has a median below KiDS's bound for every λ ≤ 2 Mpc (E2).<br>**Kernel alone:** best +9.7 / +9.2 at λ = 3 Mpc against BK1's comparator, which is a Gauss-forbidden retained-mass profile. The realizable floor (one uniform external field) is +8.2 / +8.3, and **no physical QUMOND lens reaches W1's ≤ 4**.<br>Against L352's acceptance (isolated MOND + 2-halo, ≤ +4): **−17.9 / −18.7**, passing for λ = 1–10 Mpc.<br>**Adding the carrier's surviving halo** (f_s ≈ 0.17–0.27 of ΛCDM's): −0.4 / +0.4 against the floor given the same freedom. An uncleared CDM halo costs about +120 and is excluded. |
| GP3 | `GP3_lensing_power_and_growth.py` | 9/10 (L1 fails, recorded; MUTATE kernel off: L1 passes, inverted control, rc = 0) | **Cosmic shear, the new gate.** A nonlinear mock at z = 0.5 (200 Mpc, 256³; converged against 100 Mpc at twice the resolution) solves the construction's phantom on the grid. Against ΛCDM's halo-model P_NL, the lensing/matter power ratio has a maximum over k ≤ 1 h/Mpc of **1.49 / 2.31 / 2.91** at λ = 1 / 2 / 3 Mpc (canonical; alt 1.56 / 2.48 / 3.18). The stars-only and galaxy readings give 1.6–2.1; unscreened, 2.8–3.2. **Gate L1 (≤ 1.2): FAIL.**<br>**Growth:** D(z = 0) at k = 0.2 h/Mpc rises +0.8 / +2.0 / +3.1%. **Forest:** gas sits below the switch.<br>**Replacement lead:** smooth the dark share below R_fs = 3 Mpc at λ = 2 and the ratio is 0.97 / 0.98 / 1.13 / 1.27 / 1.66 at k = 0.1 / 0.3 / 0.5 / 0.7 / 1. |
| GP4 | `GP4_generated_phantom_plus_kicked_carrier.py` | 5/5 (MUTATE, no free streaming: W1 fails, rc = 1) | **The replacement, scored.** GP1's kernel with L319's kicked, free-streaming carrier (L364's committed scan), on L364's pre-declared gates, both footings. The controls reproduce GP3 (4e-16), L364's X-COP ratios (0) and GP2's KiDS scores (0). **A window on the alternative threshold set** at λ = 1 Mpc:<br>• f_d(0) = 0.95, v_k = 1200 km s⁻¹: cosmic shear 1.09 / 1.15; KiDS −6.2 / −4.6 against L352's base; X-COP 0.97 / 1.00 (raw); galaxies +0.004 dex; S_8 0.762; forest 0.9917.<br>• f_d(0) = 0.9, v_k = 1400 km s⁻¹: 1.13 / 1.19; −4.8 / −2.2; 0.89 / 0.92; +0.010 dex; 0.755; 0.9934.<br>**No strict window:** the strict forest (≥ 0.9952) and strict S_8 (≥ 0.767) block it; strict X-COP passes in the first cell. The screening pulls X-COP toward 1 (L364's unscreened 1.17 / 1.22 becomes 0.97 / 1.00). Without the free streaming (MUTATE), cosmic shear fails at every λ (1.49 / 1.56 at λ = 1). |

**Standing (GP0–GP3).** The generated-phantom construction is built and derives from a Lagrangian.

- **What it fixes.**
  - Growth and the forest stay Newtonian (BK3's failure is gone).
  - The phantom is not Gauss-cancelled, so the switch threshold no longer decides where a lens's phantom ends (the KiDS–forest pincer is gone).
  - KiDS isolated lensing reaches the realizable floor once the dark component is mostly cleared from galaxy halos (f_s ≈ 0.2), which is the carrier's job (L357, L365).
- **What it breaks.** Light sees the phantom, and the weak ambient field KiDS needs (~1e-5 to 1e-4 a0) makes the kernel boost *every* clustered fluctuation of bound baryons below λ by ν ~ 100–200. At the λ KiDS prefers, the lensing power at k ≈ 0.5–1 h/Mpc is 2–3× ΛCDM's. Cosmic shear (KiDS-1000, DES Y3, HSC Y3) finds it at or below ΛCDM. **The pincer:** KiDS isolated lensing wants λ ≳ 1.5–2 Mpc, while cosmic shear wants the collective phantom confined below ~0.5 Mpc.
- **The open door.** The phantom must **replace** the dark component's small-scale lensing power, not add to it. That requires a dark component that is smooth below ~λ at late times, for example a carrier that decays everywhere with kicks and free-streams, like L319's (v_k ~ 600–1000 km/s). The mock's lead is close at k ≤ 0.5 h/Mpc and not yet at k ~ 1.
- **Not tested here.**
  - The flux-switched bound-region kernel (L359–L361) on cosmic shear. Its regions reach Mpc scale at low z, so it probably inherits the same collective boost.
  - Brouwer+21's all-galaxy lensing (Fig. A4), the direct data test of the collective phantom.

**Standing (GP4).** On the **alternative** threshold set the generated phantom (λ = 1 Mpc) with L319's kicked, free-streaming carrier (f_d(0) = 0.9–0.95, v_k = 1200–1400 km s⁻¹) passes every gate on the record together: KiDS isolated lensing, cosmic shear, X-COP, the galaxies' RAR gate, S_8 and the forest. It is the first window for any construction. The phantom replaces the carrier's small-scale lensing power instead of adding to it.

What it does **not** yet establish:
- **Thresholds:** only the lenient forest and S_8 thresholds pass. The strict ones fail by 0.4% (forest) and by 0.005–0.012 (S_8).
- **KiDS:** it passes by L352's acceptance, the reference the other lanes use. Against the realizable floor with the same carrier freedom it is still about +8 (GP2 W4).
  - ⚠️ **Correction (2026-09-26, `real_research/paper34_audit_2026/P34_paper_numbers.py`, check X1):** the "+8" is not what GP2 W4 gives. From GP2's and GP4's committed tables, the two window cells sit **+19.1 to +21.5** above the realizable floor with the same carrier freedom (GP2 W4 itself: +19.8/+18.6 for the λ = 1 Mpc kernel with the halo amplitude free). +8.2/+8.3 is the floor's own distance from the Gauss-forbidden comparator. Measured against that floor, KiDS wants λ ≳ 2 Mpc, where cosmic shear fails.
- **Cosmic shear:** scored at one epoch (z = 0.5), in a lognormal mock, with r_x held at its full-matter value and on P(k), not ξ±. It sits at the edge on the alt footing (1.15–1.19 against 1.2).
- **Free parameters:** λ and the carrier's parameters (f_d(0), v_k, trigger power p = 2) are all free.
- **Untested:** high z (RC100 and the z ≈ 2.5 flagship, where L356 found the carrier still intact) and the edge step's effect on the circumgalactic gas.

**Record.** First-run corrections, all before commit:

- GP0 S1 carried a mis-set resolved-mass clause.
- GP1 N2 had a tolerance bug, and N3 used a test mass too large to be in the linear regime.
- GP2 was first run with BK1's one-S form. GP1 N3 then showed that form is not Lagrangian, so every table was rebuilt.
- A W4 gate scored against a simple NFW ΛCDM benchmark (χ² = 286). It "passed" by about 190, meaninglessly, and was withdrawn.
- A GP3 documentary label wrongly claimed "< 1%" growth change.
- Each is described in the script docstrings.

Controls write separate outputs (`*_MUTATE.out`, `*_results_MUTATE.json`), and the main runs were last.
