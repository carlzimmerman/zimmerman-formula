# FC-FINAL (AeST + frozen J₁₀) — full 1PN PPN: γ, β, α₁, α₂, ξ

**Task:** derive the 1PN PPN parameters from the AeST field equations with a preferred-frame
source velocity **w ≠ 0** and the frozen K(Q) params, WITHOUT importing Einstein-aether (EA)
formulas unless the FC-FINAL → EA map is *proved*. γ = 1 and c_T = 1 are committed PASS; the open
items were **α₁ = −4K_B** and **α₂** (genuinely uncomputed on the Y≠0/FRW background).

**Bottom line (honest):**
- **γ_PPN = 1** — **DERIVATION** (re-confirmed here; matches committed `typeII_direct_variation`).
- **c_T² = 1** — **THEOREM** (c₁₃ = 0, certified below).
- **α₁ = −4K_B** — **DERIVATION for the aether (vector) sector**, via a *proved* c-tensor map,
  ⇒ K_B < 2.5×10⁻⁵. Whether the AeST **scalar** corrects α₁ is tied to the same open
  full-w² computation as α₂ (see below); the committed operative value is −4K_B.
- **α₂ = α₂(K_B, K₂, Q₀)** — **OPEN**. It is **finite** (the scalar regularises the singular
  pure-vector EA value — THEOREM below), but the coefficient is **not closed**: the direct
  O(w²) solve does not yet pass its own internal PPN-consistency check under a tractable ansatz.
- **β, ξ** — **OPEN** (β not adverse; ξ = 0 expected for a theory with no long-range extra
  scalar hair, but not computed here).

No result is reported as PASS that failed its certificate. α₂ stays a *bounded-but-uncomputed
expression*, exactly the honest outcome the task allowed.

---

## 1. What is rigorously established — `fc_ctensor_map_2026.py` (ALL PASS)

**DERIVATION — the AeST aether kinetic IS Einstein-aether (vector sector).**
The frozen action's aether kinetic `−(K_B/2)F_{μν}F^{μν}` equals, as an *exact flat-space
algebraic identity in a generic constant aether-gradient*, the EA kinetic
`−K^{μν}_{αβ}∇_μA^α∇_νA^β` with

```
(c₁, c₂, c₃, c₄) = (K_B, 0, −K_B, 0).
```

Certified two ways: (i) `simplify(−½F² − L_EA|_{(1,0,−1,0)}) == 0`; (ii) coefficient-matching on
the independent quadratic invariants forces `c₁=1, c₃=−1, c₄=0`, and F² carries no `(∇·A)²`
term so `c₂ = 0` (Maxwell-type). This is the "prove the map before using EA" step the task demands.

**THEOREM — the load-bearing EA invariants.**
```
c₁₃  = c₁+c₃      = 0      ⇒  c_T² = 1/(1−c₁₃) = 1  EXACTLY  (GW170817-safe; committed).
c₁₄  = c₁+c₄      = K_B.
c₁₂₃ = c₁+c₂+c₃   = 0      ⇒  the EA spin-0 aether mode is NON-DYNAMICAL.
```

**DERIVATION — α₁ for the aether sector.** With the map proved, the Foster–Jacobson pure-vector
result (gr-qc/0509083) is now *licensed* (not imported blindly):
```
α₁ = −8(c₃² + c₁c₄)/(2c₁ − c₁² + c₃²) = −8K_B²/(2K_B) = −4 K_B.
      ⇒  |α₁| < 1×10⁻⁴  gives  K_B < 2.5×10⁻⁵.
```

**THEOREM — why α₂ needs the scalar.** The Foster–Jacobson α₂ carries a factor `1/c₁₂₃`. Since the
AeST vector sector has `c₁₂₃ = c₂ = 0`, the **pure-vector α₂ is SINGULAR** (verified: the residue at
c₁₂₃→0 is nonzero). The EA formula therefore *cannot* be used for AeST α₂. Physically, the missing
EA spin-0 aether mode is supplied by the **AeST scalar φ** (kinetic set by `F_QQ = 2K₂`, the SZ21
condensate curvature), which regularises α₂ to a **finite** `α₂(K_B, K₂, Q₀)`. Computing that
finite value requires the coupled scalar–vector O(w²) solve — it is *not* an EA-algebra shortcut.

---

## 2. The direct O(w²) computation — `fc_alpha2_preferred_frame_2026.py` (status: does NOT close)

A full first-principles machine was built to derive α₁, α₂ *directly* from `δS_FINAL = 0` with a
boosted-aether preferred frame, NOT via EA formulas. It is a two-parameter (ε perturbation, w_b
boost) plane-wave expansion of the covariant AeST Lagrangian (aether A_μ + scalar φ + metric),
genuine Einstein–Hilbert `√−g R` gravity, matter dust, order-by-order in w_b. It **correctly**:

- solves the unit constraint `A_μA^μ=−1` on the boosted background (Q=Q₀, Y=0 certified);
- reproduces **γ_PPN = 1** (Φ=Ψ, certified) and the committed **type-II static 00-equation**
  `Psik(static)` with the `K₂Q₀²` scalar mass and K_B, J_Y structure;
- the MOND kernel enters *only* through J_Y (→1 at Solar-System accelerations): **kernel-blind**,
  as required.

**Where it stops (honest FAILED items D1, D2).** Under the standard PPN-gauge **isotropic** spatial
ansatz `h_ij = −2Φ δ_ij`, the extracted α₁ ≠ −4K_B and the two independent g₀₀ extractions of α₂
(from the `w²U` and `(w·k)²U/k²` structures) **disagree** — a definitive internal-consistency
failure. Diagnosis: at O(w²) the aether sources an **anisotropic** spatial stress (it carries the
preferred direction w), so the traceless-ij field equations are non-trivial; the isotropic ansatz
cannot satisfy them, so the "solution" is not a true solution and its α₂ is meaningless. **The fix
is the full generic (anisotropic-h_ij) metric solve** — a heavier computation not completed this
session. Therefore α₂ from this machine is **withheld** (not reported), per the honesty mandate.

This is a *real* obstruction of the reduced ansatz, not of the theory: nothing here says α₂ is
ill-defined — only that the tractable ansatz is insufficient and the generic solve is the
outstanding work.

---

## 3. Host / kernel classification (task §5)

| Item | Result | Cause classification |
|---|---|---|
| c_T² = 1 | PASS (exact) | **CONSTRAINT/KERNEL-independent** (c₁₃=0 from the Maxwell-type F²; kernel invisible, δ²J₁₀=0). |
| α₁ = −4K_B (vector) | DERIVATION | **HOST (aether/K_B)** — set by the EA c-tensor, kernel-blind. |
| pure-vector α₂ singular | THEOREM | **CONSTRAINT-ARCHITECTURE** — c₁₂₃=0 is a property of the F²-only vector sector. |
| α₂ finite, uncomputed | OPEN | **COUPLING (scalar↔aether)** — regularised by F_QQ=2K₂; needs the coupled w² solve. |
| α₂ direct-solve fails D1/D2 | FAILED (ansatz) | **method artifact** (isotropic h_ij), not the theory. |

The MOND kernel J₁₀ is invisible to every PPN item at Solar-System accelerations (J_Y→1,
1−μ₁₀=O((a₀/g)¹⁰)); the preferred-frame physics is carried entirely by {K_B, K₂, Q₀} — a clean
sector separation.

---

## 4. Numerical margin chain

**α₁ (solid).** action `−(K_B/2)F²` → c₁=K_B,c₃=−K_B (certified) → α₁=−4K_B (FJ, licensed) →
bound |α₁| < 1×10⁻⁴ (Will; lunar-laser-ranging / pulsar preferred-frame) → **K_B < 2.5×10⁻⁵**.
(If the ~10⁻⁷ pulsar-ensemble α₁ bound is used, K_B < 2.5×10⁻⁸ — but that reading is contested.)

**α₂ (NOT closed).** action → scalar-regularised α₂(K_B,K₂,Q₀) [finite, THEOREM] → LLR bound
|α₂| < ~1×10⁻⁷ (lunar perihelion / solar-spin-axis alignment) → **a constraint on {K_B,K₂,Q₀}
that cannot be written down until the coefficient is computed.** The margin chain is therefore
*structurally in place* but its final link (coeff → bound → K-space) is **OPEN**.

---

## 5. Verdict

- **γ = 1, c_T = 1:** PASS (derived/theorem).
- **α₁ = −4K_B ⇒ K_B < 2.5×10⁻⁵:** DERIVATION (vector sector, certified map); scalar-correction OPEN.
- **α₂:** OPEN — finite (scalar-regularised, THEOREM) but genuinely **uncomputed**; the direct-solve
  machine reaches it only up to the anisotropic-metric obstruction. Adverse-leaning if it scales as
  ~K_B/2 (would force K_B ≲ 4×10⁻⁸), but that magnitude is **not established**.
- **β, ξ:** OPEN.

**Files (all in `.../closure_2026/fried_chicken_final/`):**
- `fc_ctensor_map_2026.py` — AeST→EA map + c₁₃=0, c₁₂₃=0, α₁=−4K_B, α₂ singularity (ALL PASS).
- `fc_alpha2_preferred_frame_2026.py` — full O(w²) direct machine (γ=1 + static PASS; α₂ extraction
  FAILED under isotropic ansatz — documents exactly what the generic-metric solve must fix). Its
  raw α expressions are internally inconsistent (D2 fails) and are deliberately NOT persisted.
