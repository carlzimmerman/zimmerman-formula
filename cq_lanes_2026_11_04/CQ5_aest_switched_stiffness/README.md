# CQ5_aest_switched_stiffness: GRAFT FAILS: G2c, G4 (both footings, both inherited). The graft cures AeST's Cassini and planet failures, keeps γ = 1, leaves the FRW background exactly unchanged and keeps the law outside L★, but AeST's preferred-frame sector and v4's twist ill-posedness stay

κ = ½ FITTED; not theory closed. Footings never pooled. Nothing here says the data favour the framework. No particle; the cold sector stays retired. This lane adopts nothing. **Not blind:** every input is on record, and the by-hand expectation in `FROZEN_CRITERIA.md` (7cb86f471a, committed alone first) came true.

Script `cq5_graft.py`. It execs `common/ax1_engine.py`, a byte-identical copy of AX1's engine (SHA-256 9751e781…), unedited. Outputs: `cq5_graft.{json,out}`; MUTATE twin `cq5_graft_MUTATE.*` (stiffness off, exit 1 by design); rerun `cq5_graft_RERUN.*`, whose JSON is byte-identical (SHA-256 849d95fd…). The engine's own byproduct files (`AeST/`, `v3s/`) are regenerated on every run and are not committed; KA1 and KA2 record their comparisons in `cq5_graft.json`. 63 s, one thread, `nice -n 10`, peak memory footprint 0.35 GB; max RSS 1.26 GB, which counts shared and file-backed pages, and the unedited engine alone reaches 0.76 GB RSS; 0 swaps; no download.

## Record check: PARTLY ON RECORD
The **unswitched** graft is already on record:
- the term itself (C1);
- its Cassini and planets as C3's V1;
- its health as v4/I1;
- AeST's PPN in AS3;
- the Sun's D·P sign in X3 D2.

No lane had grafted the **switched** term onto AeST and graded it as one theory. AX1's line that AeST's "stiffened, switched form is v3s" is a static-limit identification. v3s sits on the khronon, not on AeST's twisting aether.

## 1. The grafted action
S = S_AeST − ∫d⁴x √−g (γ_L/2K²)[max(D·V, 0)]², with:
- V^μ = q^{μν}∇_νφ, where q^{μν} = g^{μν} + A^μA^ν;
- D·V = q^{μν}∇_μ∇_νφ + θ𝒬 (the leaf divergence D_μV^μ);
- θ = ∇_μA^μ and 𝒬 = A^μ∇_μφ;
- K = 8πG̃/(2−K_B) = 4πG and γ_L = K L★²/2.

The term acts on **AeST's scalar φ**, through its aether-projected spatial gradient.
- **P = V/K.** In the static weak field, K P = ∇χ + Q₀a (C1's field map).
- **D** is the derivative on the aether's orthogonal space, so D·P = (∇²χ + Q₀∇·a)/K (S2).

F is AX1's AeST law candidate: C1's capped 𝓕, μ = x/(1+x).

## 2. Static limit and the Solar System
**Equations.** In the static weak field Φ = Ψ, p ≡ KP and L★_F² = 2K_B/((2−K_B)Q₀²):
- ∇²Φ = 4πGρ + ∇·p
- ∇Φ + (L★²/2)∇[max(∇·p, 0)] − (L★_F²/2)∇×∇×p = a₀p/(a₀ − |p|)

At AeST's physical curl length (C3 K5b, read), p is curl-free on Solar-System scales. Then p = ∇ψ, Φ = Φ_N + ψ, and:
- ∇·[|∇ψ|∇ψ/(a₀ − |∇ψ|)] − (L★²/2)∇²[max(∇²ψ, 0)] = 4πGρ.

Linearised in the Galactic field: ψ̂ = −4πGM/(S⊥k⊥² + S∥k_z² + (L★²/2)k⁴), with S⊥ = x_e and S∥ = x_e(2 + x_e). The closed-form Q2 follows. It reproduces AS3 Part 2's 16 cells to 5.5e-13 and C3's V1 24 cells to 7.7e-10 (KA3).

**Is the switch on?** The Sun's own D·V in this linear model has equatorial negative lobes. They are at most −2.8e-7 M☉/pc³ deep, at r = 1.33 L★ (canonical, E3, floor). X3 D2's Galactic floor is +0.0055 / +0.0062 M☉/pc³ (read). The margin is 1.98e4 to 6.2e5, so the switch is on throughout and the switched Q2 equals the unswitched one. This reproduces X3 D2 (≤ 3.1e-7, ≥ 1.8e4).

| gate | canonical (L★ 21.7 / 50 pc) | alt (L★ 22.9 / 50 pc) |
|---|---|---|
| G2a Q2/Hees, E0–E3 | 1.78–3.53e-8 / 1.45–2.88e-9 **P** | 1.34–2.47e-8 / 1.29–2.37e-9 **P** |
| G2a Q2/Park | ≤ 6.1e-8 **P** | ≤ 4.3e-8 **P** |
| G2b GM/L★² (+GMμ_K²/2) / bound | Mars 0.211, Saturn 0.042, Earth 0.034 / Mars 0.040 **P** | Mars 0.190, Saturn 0.038, Earth 0.031 / Mars 0.040 **P** |
| G2γ γ − 1 | 0: D·V has no Ψ or Φ at O(ε), so Φ = Ψ is kept (S2) **P** | same **P** |
| G2c preferred frame | **F**, carried (below) | **F** |

**MUTATE (stiffness off)** gives AeST back: Q2/Hees 2.444–4.552 (canonical), 2.85–5.147 (alt), Saturn 1.34e4 / 1.62e4×. That is AX1's AeST to 1e-12. Label: GRAFT FAILS: G2a, G2b, G2c (M1 PASS).

**G2c, carried from AX1/AS3.**
- **Branch (a), no sound speed.** S3 shows the graft adds no ∂_tχ at linear order, so no kinetic term. AS3's zero-speed transported charge therefore stays, and moving systems still lose the law.
- **Branch (b), with a sound speed (c2*).** AS3's static-branch α1 = −4(2 + K_B J)/(1 + J) gives −22/5 at J = 1, which is reproduced. The stiffness drives J_eff → ∞ at r ≪ L★, so α1 → −4K_B = −0.8 at K_B = 1/5. It passes |α1| < 1e-4 only if K_B < 2.5e-5. This is **a READING, not a solve**; α2 in that limit is not computed.
- So neither branch passes both the PPN bounds and the law for moving systems, as in AX1.

## 3. Background
On flat FRW, V^μ ≡ 0 and D·V ≡ 0 identically, for any a(t), φ(t) and comoving unit aether (S1). This also holds with a finite TT tensor mode (S4). The term and its first variation vanish, so **AeST's background equations are unchanged exactly**.

On perturbations, the switched term lies between 0 and the unswitched one (C3's k⁴χ²). Relative to the scalar's gradient term it is (L★k(1+z))²/2, with no cosmological model input. At L★ 21.7:

| k (Mpc⁻¹) | z = 1100 | z = 1e5 |
|---|---|---|
| 0.1 | 2.9e-6 | 0.024 |
| 0.3 | 2.6e-5 | 0.21 |

The ratio reaches 1 at k(1+z) = 6.5e4 / 6.2e4 / 2.8e4 Mpc⁻¹ (L★ 21.7 / 22.9 / 50).

The background sits exactly on the switch's kink (D·V = 0). Linear perturbations therefore see the stiffness only where δ(D·V) > 0. The perturbation equations are piecewise, not one linear operator. X3 showed that smoothing the switch is not allowed. **The CMB itself is not recomputed.**

## 4. Galaxy law
Where D·V < 0 the static equation is AeST's exactly. Elsewhere the stiffness changes the scalar kernel by (L★/r)²/(2x). At r ≥ 1 kpc and x ≥ 0.05 that is at most 0.0020 / 0.0023 / 0.0107 dex for L★ = 21.7 / 22.9 / 50 pc. **Kept (P).** This is a reading, not a SPARC solve.

The graft does not choose AeST's own static form. That form is AQUAL at ℓ_F → 0 (C1, AX1), but curl-free two-field at AeST's physical ℓ_F (C3).

## 5. c_T and health (AX1's level)
- **c_T.** The term is absent from the tensor sector on FRW to all orders (S4), so c_T is AeST's: c by construction [PROVISIONAL].
- **Health: F (I1, read).** Wherever D·V > 0 the graft is v4, which is ill-posed wherever the aether twists. The twist is forced off symmetry (I1 K5). The switch removes the stiffness only where D·V < 0, and the whole Solar neighbourhood has D·V > 0. X3's cure is for ρ_τ < 0 saddles, a different defect.

## Checks
All pass:
- KA0, the engine copy's hash;
- KA1, the copy as AeST matches AX1 to 0.0;
- KA2, the copy as v3s matches AX1's hedgehog and C6 margins to 0.0;
- KA3;
- S1–S4 (sympy);
- SW0, the isotropic self-check, at 5.5e-8.

The engine's own K1–K4 and V1 pass.

## Reading
Grafting v3s's switched stiffness onto AeST does what it was built for: it screens the Sun. Q2 drops from 2.4–5.1× Hees to ≤ 3.5e-8 of it, and the planets sit at ≤ 0.21 of their bounds. It costs nothing on the homogeneous background. The switch itself changes nothing in the Solar System or on FRW.

It does not make one theory that passes the Solar System. AeST's preferred-frame failure (AS3) is in a sector the term never touches, and putting the stiffness on AeST's twisting aether brings in v4's I1 ill-posedness. The khronon (v3s) avoids I1 by being twist-free, and that is the difference between v3s and this graft. κ = ½ FITTED; not theory closed.
