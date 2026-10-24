# O1_ownership_action: can an action in the v3s family give Z★ its rule R2 (ownership)?

## Verdict (frozen rule, FROZEN_CRITERIA §5): NO-GO. Reading: CRISP FINDING (a theorem with its premises stated)

**No local action in the v3s family lets a satellite carry a held phase.** The blocking must-keep is **M3, the host's own
law**: the host's held phantom inside the satellite's orbit. The law also forces α = 1 (held dust carries Ξ-charge equal
to its mass), which is the second premise.

- **Theorem W (composite weight).** Take a compact satellite in any local, translation-invariant theory of this family.
  The net force on it is (M_b + M_τ) g_host − M_τ |∇Ξ_amb|, whatever drag, alignment, gate, stiffness or multi-stream
  microphysics acts inside it. This is exact in 1D (K2, K3) and follows from the stress identity in 3D (K4; U1 N4 checked
  it nonlinearly).
- **Gauss (K5).** For a spherical host, the ambient gradient is |∇Ξ_amb| = f⁻¹(G M_τ,host(<r)/r²), however the
  khronon moves. For the held AQUAL host this equals g_host exactly, so **ε = 1**: the held phase has no weight.
- **What OWN would cost.** With ε ≤ ε_B (the ownership pass line, M1a), the host could keep at most φ_max of its own
  phantom inside the orbit:

  | radius | φ_max (canonical / alt) | MW v_c, law → with φ_max |
  |---|---|---|
  | 50 kpc | 0.106 / 0.085 | 173 → 88 km/s (canonical) |
  | 100 kpc | 0.052 / 0.042 | 169 → 63 km/s (canonical) |
  | 250 kpc | 0.020 / 0.016 | 167 → 40 km/s (canonical) |

- **Z★'s own supply-edge statics do not help.** Beyond r_s = 55.2 / 50.2 kpc, ε is still 0.85–0.89.
- **The labelled escape (one khronon per owner) fails twice.**
  - **No merging (M3(ii), K6).** Each label's charge is a separate Noether charge, so labels never merge. A galaxy built
    from N progenitors then has a law floor at x = N − 1. With a capacity limit it over-holds by up to √N instead:
    +0.15 dex for N = 2.
  - **Caustics (M5, K11).** Each label's zero-charge exterior flow is geodesic in the host. It reaches the host centre at
    t = √(π/2) r₀/v_c, which is 6–306 Myr for r₀ = 1–50 kpc. If the exterior flow hovers instead, ε = 1 again.

So R2 stays **POSTULATED, NON-VARIATIONAL**, as Z1 declared. Every action-level route on record ends either at the hover
(ε ≈ 1) or at a label sector with no action.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy, no particle. Not "theory closed". Nothing
here says the data favour the framework.

**Checks: 15/15 PASS (exit 0).** `O1_MUTATE=1` fails K3 (Mu4), N1-OWN (Mu1), K6 (Mu2) and VS-GC (Mu3), as frozen
(11/15, exit 1). Run time 1 s, 0.09 GB, one thread, nice 15. Nothing downloaded.

## 1. Record check

No ownership rule in the record was derived from an action.

| item | what it is | why it does not give an action-level R2 |
|---|---|---|
| FG001/CFG7, PAPER36 ("hierarchical ownership"), CFG31, CFG333 | scoring rules | posited; CFG333's ultra-faints fail under every class |
| CFG244 / CFG245 | bound part of an early cold fluid | Gate A binding FAIL; "ownership does NOT follow from the local form" (ratio up to 3.16) |
| CFG693 | free-fall basin | a definition, not an action |
| CFG915 / CFG916 | history labels, lock-and-release | CONTRADICTED / UNDERDETERMINED |
| CFG842 | capture from the host | Liouville ceiling 1.5e-8 to 1.8e-5 of the need |
| CFG882 / 883 / 888 | clump retention | needs a gate; the clump has no self-gravity in the action |
| CFG939 | no-capture criterion | derived (r_cap); the free population (S4) is not derivable |
| CFG941 (D-T, hover 1.02–1.11), CFG946 (D-T′, L-G), X6 (α ≡ 1), U1 T3 | the obstruction | stated for tethers and static hosts |
| CFG945 H1, CFG950 LDT, CFG953 SCT | per-label constructions | resolve the hover only with a non-variational label sector |
| CFG947 | non-local causal parent | no action (retarded kernels are not Euler–Lagrange) |
| G2 | PAPER36's ζ retention | fails on native inputs |
| N0 audit tile 50 | "ownership from an action" | OPEN |

What this lane adds:
- **W generalises T3 and Theorem S** from "static host, same point" to "any composite, any internal coupling".
- **K5 removes the "static host" premise.** Only the host's enclosed khronon charge matters, not how the khronon moves.

## 2. Candidates (FROZEN §2; derivations in `o1_ownership_action.py`, all residuals 0)

| candidate | action term | held phase's EOM / frame | blocking must-keeps | constants | class |
|---|---|---|---|---|---|
| a1 drag | −(β/2)ρ_b\|v_τ − v_b\|² | **K9**: enters as a charge flux, ∂_tρ + ∇·[ρv_τ + βρ_b(v_τ − v_b)] = 0; Dv_τ/Dt = −∇(Φ − Ξ) unchanged; frame not aligned | M1a (W: ε = 1); M3 (discs feel the term); M5 (can make ρ < 0 where ρ = 0) | +1 (β) | EXCLUDED BY THEOREM |
| a2 alignment | λ·ρ_b(v_τ − v_b) | **K7**: (∇×v_b)_z = v_c/R ≠ 0, while v_τ = −∇σ is curl-free | M3 (no solution in any rotating disc); M1a (W) | 0 | EXCLUDED BY THEOREM |
| a3 gate \|Φ_int\| > \|Φ_ext\| | — | **K1**: Ξ is a Milne scalar, so the split into Φ_int and Φ_ext is not a local field | M8; local proxies reduce to a1 or a2 | — | NOT VIABLE |
| b owner-CM frame | ∇Ξ → ∇Ξ + Ẍ_q, X_q = baryon centroid of D_q | single Ξ: W unchanged; a separate Ξ per domain is candidate e | M8 (non-local); M1a | 0 | EXCLUDED BY THEOREM |
| c multi-stream, mean-flow khronon | slave v_τ to ⟨v⟩ | same point + W: ε = 1; mean flow not curl-free (K7) | M1a, M3, M8 | 0 | EXCLUDED BY THEOREM |
| d formation memory | none | **K10**: P is algebraic (β = η = 0); the PN state (ρ_τ, v_τ, Ξ) has no memory | M1a | 0 | EXCLUDED BY THEOREM |
| e per-owner khronons τ_q | Σ_q W(∇Ξ_q) | own frame inside the owner (no EFE) **only if** the exterior label flow falls freely | M3(ii) (K6: no merging, floor x = N − 1 or √N over-hold); M5 (K11: caustic at the host centre); a hovering exterior gives ε = 1 | 0 continuous; one field per owner | EXCLUDED BY THEOREM |
| f e + exchange | −V(τ₁ − τ₂) | **K8**: ∂_tρ₁ + … = −V′, ∂_tρ₂ + … = +V′ | M5 (creates opposite-sign charge pairs, one negative); M7 | +1 function | NOT VIABLE |
| g free (Ξ-neutral) dust (reported) | Z★ R1 release, no R2 | weightful: falls at g_host (W with M_τ = 0) | needs R1 (non-variational) | 0 | reported only |

**Reported (g).** Suppose satellites keep only released free dust, because the held part is stripped at ε = 1. Then the gas
loss needed is larger than Z★'s:

| class | gas loss needed, free dust only (canonical / alt) | Z★ |
|---|---|---|
| MW classical | 0.882 / 0.867 | 0.72 / 0.67 |
| MW ultra-faints | 0.964 / 0.958 | — |
| bright M31 | 0.870 / 0.855 | — |
| M31 others | 0.965 / 0.958 | — |

Δ = log₁₀(√(M_o/M_n) − 1) in the deep limit.

**A discriminator: gas-rich hosted dwarfs, which have released nothing.** Leo T (U1 csv, PROXY speed 166 / 174 km/s):
- literal single-stream reading (LIT/VS): **+1.447 dex**;
- acceleration-only (MS) stripping: +0.273 / +0.233 dex.

This decides only if Leo T moves faster than its baryonic V_hold = √(2GM_b/r) (of order 10 km/s, not computed here)
relative to its local khronon. Its 3-D speed is a PROXY.

## 3. The coordinator's VS (H5 velocity screening), with γ_L removed

**What VS gets right, natively and with no γ_L.** A system moving at V through its host's held khronon holds no phantom
beyond r_cap = 2GM_b/V² (H5 A2/A3; U1). Systems that formed from material moving through a host's khronon therefore never
own dust, and come out Newtonian.

| tile | number | class |
|---|---|---|
| Cassini / planets | Sun r_cap = 0.037 / 0.028 AU (V 220 / 250), where x ≈ 5e10. Suppression of the would-be solar phantom at r_M ≈ 7,960 / 7,240 AU: (ω_p r_M/V)² = 5.5e-11 to 7.4e-11. Linear-wake tide ≤ 5.3e-32 s⁻² at 1–30 AU | **PASS**, 1e-5 of Park 5.2e-27 (estimate) |
| outer globulars | r_cap ≤ 0.249 pc at H5's PROXY 167 km/s and ≤ 5.35 pc at V_apo,10 ≈ 36 km/s (NGC 2419), against r_hl 15.9–27.6 pc. D10's Δχ²_Newton ≤ 2.47 in all 18 cells | **PASS** |
| wide binaries | Newtonian, the same sign as v3s's sealed prediction | prediction; DR4 decides |
| TDGs, DF2/DF4 | U1 B0: +0.055 ± 0.114 dex | **PASS** |
| isolated RAR | on FRW the chargeless khronon falls freely with the dust, so V_rel ≈ streaming (0.03 km/s) and r_cap ~ 1e10 pc for M_b 1e9 | kept |
| **satellites** | dust-free (U1 B0): **+2.00 ± 0.08 / +1.99 ± 0.07 dex**; Z2 V3D C2–C4 +1.880 / +1.885, ROBUST | **FAIL** |
| **Coma UDGs** | **+1.41 dex, z_sys 5.4** | **FAIL** |
| group members (UMa) | 12.6–14.4σ against Newton **if** the loose group's khronon is held (U1 F5) | DEPENDS |

**(i) Ownership by formation is not derivable.**
- A satellite's own khronon, whether multi-stream or the same field, is anti-weighted at ε = 1 (W, K5).
- A separate congruence is candidate e, which fails M3(ii) and M5.
- So the systems that formed in their own frame (satellites, UDGs) lose their phantom once they move through a held host.
  That is U1's +2.0 / +1.4 dex, STRUCTURAL.
- On the fixed-M_V slope (M1b), VS predicts about 0 (Newtonian satellites have no EFE), which is consistent with
  −0.05 ± 0.19. The amplitude fails.

**(ii) Removing γ_L.** Cassini and the outer globulars pass without it, because the record's reasons for γ_L (C6/D7d,
D10) assumed the static branch, and H5 A2 shows the static branch holds only in the khronon's rest frame. L★ = 0 also
lies inside P4's allowed window (≤ ~90 pc). Open items:
- **Compact systems at rest in a held khronon** (V below their V_hold, for example star clusters bound inside dwarfs at
  σ ~ 10 km/s) get the unscreened AQUAL boost. Not tested here.
- **The downstream focal line.** The velocity-screened state needs the khronon wind to cross the Danby–Camm line behind
  every moving mass. A single-stream khronon cannot do that. γ_L does not regularise it either: its sound speed
  L★√(2πGρ̄) ≈ 0.8 km/s at L★ 22 pc is Mach ≈ 300 at 220 km/s. This is the same OPEN item as V3_FULL_PICTURE §6
  (0792abedc7). It is not created by removing γ_L.

**(iii) Constants.** Without L★ the theory has:
- κ (FITTED);
- the cold abundance (FITTED, an initial condition);
- the cold-sector rule: either v3's μ_K (FREE, with no allowed value) or Z★'s R1 (non-variational);
- the postulated function J_x.

**It fails the satellites and the Coma UDGs in every variant on record. It fails Leo T as well if Leo T's PROXY speed
holds.**

## 4. What this does not show

- **The 3D nonlinear composite force** is not re-solved here. It rests on the linear far-field identity (K4) and on U1's
  N4 (≤ 8.7e-5 in 8 of 9 cells, 2.3e-3 in the strongest). The 1D identity is exact and nonlinear.
- **Spherical host for ε.** A disc host changes ε at the order of its flattening at 50–250 kpc.
- **Merger over-hold.** The √N figure assumes the deep limit and co-spatial labelled supplies. It is an illustration, not
  a solve.
- **The solar tide** is an order-of-magnitude line-mass estimate from H5's V → ∞ kernel.
- **Speeds.** Globular and Leo T speeds are PROXY (no 3-D velocities on disk).
- **Scope of the theorem.** It does not exclude a non-local or non-variational R2. It only says that R2 cannot come from a
  local action in this family.

## Files and run

- `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md`: 45d70e5e2f, committed alone first. The coordinator's VS request
  arrived before the freeze and is frozen there, so no amendment was needed.
- `o1_ownership_action.py` → `o1_ownership_action.out`, `o1_ownership_action_results.json`; `*_MUTATE.*`.
- **Fix before the scored run (disclosed).** K1's first form used sympy Functions of shifted arguments, and their `Subs`
  forms did not cancel. It now uses a quadratic polynomial with symbolic coefficients, which is fully general here
  because Ξ involves only σ_t and ∇σ at the point.
- **Candidate classes are analytic.** They are keyed to the K-checks, so they stay the same under mutate; the mutate teeth
  act on the K-checks.

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/O1_ownership_action/o1_ownership_action.py              # exit 0
O1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/O1_ownership_action/o1_ownership_action.py  # exit 1 by design
```
