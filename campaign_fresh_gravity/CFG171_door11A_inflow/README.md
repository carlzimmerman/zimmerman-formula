# CFG171 — Door 11A (radial inflow of the Λ-medium, the CONTROL reading): a scoped no-go

Frozen criteria: `FROZEN_QUESTION.md` (written before any script). Governing file: `closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`, including Addendum 1 (11A is the control reading; 11B′ is primary and is not tested here), Addendum 2 (the medium has no rest mass and is not a particle; state its stress-energy) and Erratum 1 (P2 is ν = √(1 + a₀/g_N), which is what this lane used from the start). κ = ½ is FITTED. Nothing here says the theory is closed. Nothing outside this directory was edited, and nothing was committed.

## Bottom line

No dynamical inflow law in the tested class produces the law as a mechanism. The only law that reproduces P2 (to 4 × 10⁻¹⁵, point mass and exponential sphere, 10⁹–10¹² M☉, both footings) is **AQUAL/QUMOND written for Ψ = v²/2**. That is a restatement. The flow is the Hamilton–Jacobi free-fall congruence of the potential (S1 1g): it has no dynamics of its own and no frame. Taken literally as a medium, it would have to be destroyed away from the baryons (≥ 99.9% of the required sink), and it would carry 16–205× the baryons' orbital energy (dust-like inertia ρ_Λ/c²), or 10⁷–7 × 10⁸× for a massless w = ⅓ medium.

The genuine flow laws fail G1 by construction:
- GR's own river adds Newton and Λ in v² with no cross term (verified).
- A linear velocity superposition gives an r^(−½) cross term that is 0.2–3% of the law's anomaly, with a catastrophic frame dependence.
- No algebraic superposition of the Newtonian and Λ flows can give deep MOND: the only term with the right scalings is r-independent, so it exerts no force.
- A pure Λ vacuum (w = −1) has no velocity at all.
- A conserved medium attracts outside its sink only if c_s² < 0 (a gradient instability). The massless radiation-like w = ⅓ medium cannot attract at all.
- The negative-c_s² isothermal branch gives a flat curve whose V_c² is set by the medium, not by M. Getting the BTFR would need the medium slaved to the enclosed mass, which is CFG44's postulate again.

The planets fail independently of the flow. P2's α = 1 tail is 1257–1540× the Earth/Mars bound, and that is a property of the target.

## Hypotheses (all results)

- The flow is spherical, steady and Newtonian (v ≪ c).
- **PG postulate:** test bodies are carried by the flow, so their acceleration is Dv/Dt. For a steady radial flow the inward acceleration is g = −d(v²/2)/dr. S1 1a′ verifies that the PG congruence is geodesic, with d²r/dτ² = v v′, for any v(r).
- The Λ tie per footing is H = Z a₀/c with Z = √(32π/3):
  - canonical: a₀ = 9.3603e-11 → H_Λ;
  - alt: a₀ = 1.1312e-10 → H₀.
- ρ_Λ = 3H²/(8πG).
- Baryons are a point mass or an exponential sphere. The primary sizes are CFG118's h = 2, 3, 4, 5 kpc; the secondary is h = 0.5 r_M (CFG124). CFG44's `Bcommon` was imported read-only.
- Each system's inflow is in its own rest frame. That is the variant's definition, and it is a switch: which systems own an inflow is assigned, not derived (Gap 1).

## The medium's stress-energy (Addendum 2)

| law | stress-energy | gravitates? |
|---|---|---|
| L0 GR river | none beyond Λ: T = −ρ_Λc² g (w = −1). The "flow" is a slicing (PG free-fall observers), not a medium | Λ as in ΛCDM |
| L1 linear v superposition | none. No T^μν produces it; GR superposes v², not v (S1 1a) | — |
| L2 conserved sink medium | a fluid with inertia ρ_in; incompressible limit | yes (ρ + 3P) |
| L3 barotropic medium | P = wρc², inertia (1 + w)ρ/c². Massless options: w = −1 has no velocity (S1 1d); w = ⅓ gives c_s,eff² = +c²/4, so no attraction (S1 1e). Attraction needs w < 0, which is unstable | yes; with ρ = ρ_Λ and w ≠ −1 it is no longer the dark energy (the background changes) |
| L4 potential reading | the field Ψ with Lagrangian −(a₀²/8πG) F(\|∇Ψ\|²/a₀²): a static non-canonical scalar with anisotropic (non-perfect-fluid) stress and no rest frame. At the Newtonian order used here it does not gravitate separately; its relativistic stress is 11C's question | OPEN (11C) |
| L4 literal medium | frozen reading: dust-like inertia ρ_Λ/c² (this has rest mass, so it is excluded by Addendum 2 and kept as frozen). Addendum-2 reading: w = ⅓, inertia (4/3)ρ_Λ/c², enthalpy flux (4/3)ρ_Λc²v | yes |

The cold component (Ω_c h² = 0.12) stays as in candidate B. The flow replaces only the law's phantom, so the standing rule holds: the mass is still required.

## Gate table (P = pass, F = fail, p* = passes only as a statement, U = undefined, N = not scored)

| law | G1 (10%, x ∈ [0.1, 30]) | G2 | G3 | G4 | G5 | G7 |
|---|---|---|---|---|---|---|
| **L0** GR river (PG–SdS) | **F**: Newton minus H²r, worst residual 1.01. It turns repulsive beyond GR's zero-gravity radius (0.1–1.1 Mpc), which x = 30 reaches at 10¹² M☉ | P (it is GR/ΛCDM) | p* (no medium) | P (0 new) | P (Λ term 10⁻¹¹ of the bound) | P (covariant) |
| **L1** linear v superposition | **F**: cross term H√(GM/2r) ∝ r^(−½), 0.2–3% of the anomaly; worst 0.98 | background P (v → Hr); growth U | U (no dynamics) | P (H only; the rule is postulated) | own frame: 0.83–1.26× the Earth/Mars bound (marginal). Literal Hubble frame: 17.6× the Sun's Newtonian pull | **F**: frame term 0.29–1.7 g_law at w = 100 km/s and 1.7–10 at 600 km/s (x = 1) |
| **L2a/b** conserved sink medium | **F**: the best single shared amplitude still misses by 0.967 (v_m ∝ r⁻², force ∝ r⁻⁵ or r^(−7/2)) | N | N | **F** (sink rate) | N | N (~w/\|v\|) |
| **L3a** Λ-like barotropic | **F**: \|c_s\| ~ c makes it incompressible, so it reduces to L2 (S1 1e; not separately scored) | N | N | w (a new constant unless w = −1, which cannot flow) | **F**: c_s,eff² = wc²/(1+w) < 0 | N |
| **L3b** isothermal, c_s² = −K | **F**: the best shared K still misses by 0.915 (point) / 0.966 (exp) | N | N | **F** (K; BTFR needs K ∝ √M) | **F** (c_s² < 0) | N |
| **L4** AQUAL for Ψ = v²/2 | **p\***: exact (4e-15), a restatement. **F as mechanism** | background P (\|v/Hr − 1\| = 0.028 at 10 r*); growth/CMB U | potential reading p*. Literal medium **F**: see the G3 details below | P in count (κ only, scale = P_cap = (κ²/8π)ρ_Λc²); the interpolating function is postulated | **F**: P2's α = 1 tail, 1257–1540× the Earth/Mars bound (the target's own); strict-law Q₂ 4.0–5.7× the ceiling (cited, GATES 4.01); elliptic; causality OPEN | P (frame-free by identity 1g; the flow is inert) |

L4 literal-medium G3 details:
- 99.9–100% of the required creation or destruction lies off the baryons.
- If the baryons absorb the destroyed momentum, the reaction exceeds 0.10 g_law from x = 1.3–10 onward.
- Energy carried in, as a multiple of ½M_bV_f²: 16–205× (both r_ta conventions); for massless w = ⅓, 10⁷–7 × 10⁸×.

G6 (preferred-frame PPN) was not scored. 11A defines no global frame, and L1's literal frame reading already fails G7. G8 is 11B only.

One kinematic fact survives, and it is not a mechanism. The L4 inflow comes to rest where the law's pull equals the de Sitter push, at **r* = V_f/H** (1.000 to three figures in every case). That is 0.9–6 Mpc, or 3.5–7 r_ta. Outside r* the flow is the Hubble outflow. This is the only place Λ enters the 11A flow, and it is a boundary condition, not the source of a₀.

## DERIVED / POSTULATED / FITTED / OPEN

| status | items |
|---|---|
| DERIVED (script) | **S1:** 1a PG–SdS v² = 2GM/r + Λc²r²/3 exactly, ∂²v²/∂M∂Λ = 0; PG congruence geodesic, a = v v′. 1b cross term s H√(GM/2r), V ∝ r^¼. 1c no algebraic superposition gives deep MOND. 1d w = −1 has no velocity. 1e attraction outside a sink needs c_s² < 0 (Newton −v²/3; log flow −V²/(2 − 1/2L); Λ-like wc²/(1+w); w = ⅓ gives +c²/4). 1f isothermal g = (2K/r) v²/(v² + K). 1g Hamilton–Jacobi identity. 1h AQUAL ellipticity, the P_cap tie a₀²/(8πG) = (κ²/8π)ρ_Λc², and cH_Λ/a₀ = √(8π/3)/κ = √(32π/3) at κ = ½ (Z ≡ κ, restated). **S2:** every G1 number and the free-amplitude bounds. **S3:** r* = V_f/H; the G2, G3, G5 and G7 numbers |
| POSTULATED | the PG postulate; the medium's existence and inertia (frozen ρ_Λ/c²; Addendum-2 w = ⅓); the sink localised on the baryons (L2, L3); the linear-v rule (L1); the interpolating function (L4 = the law itself); the flow normalisation (stagnation at r*); per-system inflows (the switch); the exponential-sphere sizes |
| FITTED | κ = ½ (a₀ = κc√(Gρ_Λ)); Ω_c h² = 0.12 (the cold component stays) |
| OPEN | a causal, relativistic completion of L4 (11C); perturbations and growth for any inflow law (G2 U); how nested systems' inflows combine (Sun in the Milky Way), on which Q₂ depends; G6; non-spherical baryons; multi-body flows (the HJ congruence develops caustics behind moving or multiple masses) |

## Scripts (each < 1 min; run from this directory)

| script | content | exit (main / MUTATE) |
|---|---|---|
| `cfg171_s1_symbolic.py` | Step 1 and the symbolic Step 2 (sympy), 9 checks | 0 / 1 (`--mutate a`: a cross term inserted into the SdS metric; 1a fails) |
| `cfg171_s2_g1_law.py` | G1 for L0–L4, free-amplitude bounds, controls | 0 / 1 (`a`: L4 with μ ≡ 1 fails G1; `b`: with GR's law as the target, L0 passes) |
| `cfg171_s3_gates.py` | G2, G3, G5, G7 and controls | **1** (frozen control C3 fails, kept) / 1 (`a`: the α = 2 kernel passes the planets) |
| `cfg171_common.py` | shared (read-only import of CFG44 `Bcommon`; S3 also imports CFG48 `Gcommon` read-only) | — |

Outputs are `*.out` and `*_results.json`, named by mode.

Controls that reproduce committed numbers:
- CFG44's M_dyn = M_b√(1 + x²) (3.6e-15).
- CFG48 `Gcommon.r_ta_kpc` (exact).
- The record's Sereno–Jetzer 2σ inversion: Earth 3.661e-14, Mars 3.723e-14, a₀/2 = 1278×.
- CFG7 H1's Milky Way phantom tide at the Sun, 1.56–2.56e-31 s⁻² (deviation 0).

## Disclosures (kept as they fell)

- **C3 failed as frozen.** I wrote "r_ta(B)/r_ta(A) ∈ [1.7, 3.6]" for all four masses. The referee quoted that range for 10¹⁰–10¹⁴ M☉. At 10⁹ the ratio is 4.37; at 10¹⁰–10¹² it is 3.60, 2.97 and 2.45, which reproduce the referee's edges 0.11, 0.13 and 0.16 r_ta (C3b, added afterwards and reported only). S3's main run exits 1 because of this. The G3 energy verdict does not depend on it: convention A alone fails, at 16–49×.
- **Addendum 2 arrived while S3 was being written.** The massless w = ⅓ rows (kinetic and enthalpy flux) and the massless sign in S1 1e were added then. The frozen dust-like rows are unchanged.
- The G1 free-amplitude bounds use a log grid plus a bounded refinement. They were computed for P2 only, on the point-mass and CFG118 exponential-sphere families. They are bounds, never adopted values. L3b uses the form most favourable to it (a pure 2K/r everywhere). All the L2 bounds equal the x = 30 miss (0.967), which no steep term can repair.
- L3a was not scored numerically. At |c_s| ~ c it is the incompressible L2 (S1 1e).
- **ν_mono's Solar-System tail (reported; a spin-off, not scored).** The record's monotone repair keeps h(y) = (ν − 1)y non-decreasing. Its phantom therefore never falls below 0.648 a₀ at high g, and it is 1.18 a₀ at Earth: 2.9–3.6 × 10³ × the planetary bound, which is worse than P2. It matters only when the Sun owns its own phantom or inflow.
- The simple ν (the gates file's pre-erratum parenthetical) differs from P2 by up to 15.5% on x ∈ [0.1, 30]. It is reported, never scored. Its Solar-System tail is a₀, 2.5–3.1 × 10³ × the bound.
- The menu of flow laws was written knowing the target and the ten-door result. It is not a blind sample.
- Literature items (the PG river picture, Sereno–Jetzer) are the record's own verified inversions or were derived here. No network was used.

## What is not tested

- 11B′ (primary; CFG173) and 11C (CFG172).
- Any flow law outside L0–L4, including vector or khronon flows (11C).
- Time-dependent inflows.
- Non-spherical baryons.
- Nested systems.
- Cosmological perturbations.
