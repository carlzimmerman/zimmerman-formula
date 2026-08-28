# FC-4AC INVERSE-DESIGN VERDICT

**VERDICT: MOND-SPECIFIC-NO-GO** (for the analyzed 4-auxiliary-constraint, linear-in-N / Embedding-I
construction with frozen kernel `mu_10`). One open door survives (sf42 auxiliary-Legendre pair) — this
is **not** "theory closed."

## One line
An explicit H_can was written and the Dirac chain **does** close at rank Δ=4 / N_grav=2 for a genuine
spatial-gradient `C_M^(10)` (evading the guessed `D²q=0` kill), but the **same linear-in-N structure that
delivers `C_M` structurally forces the lensing slip `Φ'/Ψ'=(μ+yμ')/μ : 1→2`, so `Φ=Ψ` fails in the MOND
regime, and `α_3=-1` fails independently by >5×10¹⁹×** — the theory dies on the slip, not the DOF count.

## Status of the required object (H_can)
`h_can_written = TRUE`. This is **not** INCONCLUSIVE-needs-explicit-Hcan. Two explicit canonical
Hamiltonians were constructed and run through the Dirac algorithm:

- **Attempt A (minimal, kinetic-free, kernel on the lapse):** chain closes **early** at rank Δ=2
  (`det=L_N²`). Preserving `C_M` merely fixes the lapse-velocity multiplier `u_1`; no independent `S_3`.
  ⇒ N_grav = 2(T)+0(V)+**1(S)** = **3**, a residual conformal scalar. FAILED for the 2-DOF goal.
  `{MOND exterior} XOR {rank-4}` from the minimal H_can.
- **Attempt B (kernel on q + conformal kinetic term (σ/2)p_q²):** chain **generates 4 constraints**
  `S_1=π_N, S_2=C_M, S_3=σL^[p_q], S_4=σ²Ĉ−σL̂²[N]`, `det Δ = σ⁴ L_N⁸`, **rank Δ=4** per propagating mode
  (lattice rank 4(n−1)). ⇒ **N_grav=2**. The DOF gate is passable with a spatial-gradient constraint.

## Closure vector (verified, sympy 1.13.1, all scripts re-run exit 0)

| quantity | result | basis | verdict |
|---|---|---|---|
| rank Δ (attempt B) | 4 per mode, `det=σ⁴L_N⁸` | COMPUTATION | closes |
| N_grav (attempt B) | 2 | COMPUTATION | ok |
| **Φ = Ψ (slip)** | `Φ'/Ψ' = (μ+yμ')/μ`: 1(y→∞)→3/2(y~1)→**2(y→0)** | DERIVATION (2 methods agree) | **FAIL in MOND regime** |
| γ_PPN (solar, y≫1) | 1 | DERIVATION | pass (solar only) |
| α_1 | 0 | DERIVATION | pass |
| α_2 | 0 | DERIVATION | pass |
| **α_3** | ∈[−3,−2] ≈ −1 | DERIVATION/STRUCTURAL | **FAIL >5×10¹⁹×** |
| **∇_μ T^{μν} (w.r.t. g)** | = 0; F5=0 on Σ | DERIVATION | **PASS** (corrects earlier transfer) |
| c_T | 1 | MODEL-ASSUMPTION | assumed |

## Why it is a NO-GO (and why it is MOND-specific)
The obstruction is **not** the guessed-chain `D²q=0` death — attempt B evades that (generated `S_2` is the
nonlinear AQUAL flux `D_i[μ_10 D^i q]`, not `D²q`). The obstruction is **relocated to the slip and is
structural**: to make `π_N`-preservation deliver `C_M`, H_can must be **linear in N**
(`∂²H_can/∂N²=0`). That linearity forces the generated `S_4` onto the **tangent modulus `μ+yμ'`**
(radial stiffness) while `S_2` fixes the curvature on the **secant modulus `μ`**. Their ratio is the slip,
and the frozen kernel makes it swing by a factor of 2 across the acceleration scale — precisely a
**MOND-specific** effect (it lives entirely in `y μ_10'/μ_10`, zero only at `y→∞`). No constant
normalisation repairs both regimes. `α_3=−1` (elliptic instantaneous lapse response, embedding-independent)
kills it a second, independent way.

## Honest caveats / open doors (NOT "theory closed")
1. **sf42 auxiliary-Legendre escape is OPEN.** A non-minimal H_can with an independent canonical pair
   `(χ,Φ)` carrying MOND **off the lapse** yields 2 DOF **without** forcing linear-in-N, so the slip
   argument does not obviously transfer. It was **not** executed here.
2. **Scalar/TT (York) decoupling is a MODEL-ASSUMPTION.** Full `q–h_TT` coupling is a residual OPEN
   (same class as FC4AC_DOF.md Part IV); it underlies both the rank-4 count and the matter PASS.
3. The matter-conservation **PASS** does not rescue the theory — the same linear-in-N structure that
   secures it forces the slip.
4. `a0²=κ²c²Gρ_Λ`, `a0(z)~√ρ_DE` remain TARGET/phenomenological; `κ=½`, `Z~21` FITTED. Untouched here.

## Files (this task)
- `closure_results.json` — machine verdict + closure vector
- `FC4AC_INVERSE_REPORT.md` — full derivation narrative
- Certificates: `inverse_chain_A.{py,out}`, `inverse_chain_B.{py,out}`, `fc4ac_slip.{py,out}`,
  `fc4ac_matter2.{py,out}`, `fc4ac_alpha_ppn.{py,out}` (all exit 0, all boolean checks pass)
