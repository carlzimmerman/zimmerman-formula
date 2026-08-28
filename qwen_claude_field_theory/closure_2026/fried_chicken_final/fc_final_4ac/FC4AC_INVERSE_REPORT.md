# FC-4AC INVERSE-DESIGN REPORT
### Is the 4-auxiliary-constraint Type-II MMG Hamiltonian + frozen kernel `mu_10` a real relativistic MOND theory?

**Bottom line: MOND-SPECIFIC-NO-GO** for the linear-in-N (Embedding-I) class. The rank-4 / 2-DOF Dirac
closure is *achievable* with a genuine spatial-gradient constraint, but `Φ=Ψ` (hence `γ_PPN=1`) is
*structurally excluded in the MOND regime* by the same H_can structure that generates the constraint, and
`α_3=−1` fails independently. Matter conservation, by contrast, holds. One construction class (sf42
auxiliary Legendre pair) is untested and remains genuinely open.

All numbers below come from committed scripts in this directory, each printing sympy `simplify(...)==0`
certificates and exiting 0 (re-run 2026-08-28, sympy 1.13.1 / numpy 1.26.4).

---

## 0. Control: the analytic kill of the *guessed* chain (reproduced)
`DERIVATION`. The hand-picked partner choice `S_2=D²q, S_3=D²p_q` is dead. In spherical vacuum `D²q=0 ⇒
q'=A/r²`; the MOND exterior needs `r² μ_10(y) q' = const`. Since `μ_10` is strictly monotone (injective),
the only common solution is `q'=0` — no nontrivial MOND exterior. This is why the scalar partners must
**not** be hand-picked spatial PDEs for q, and motivates generating the chain by the Dirac algorithm.
(inverse_chain_A.py Part 5, cert PASS.)

---

## 1. Attempt A — minimal (kinetic-free) H_can: chain closes early, N_grav=3

`H_can = ∫d³x [ W_AQUAL(N,γ,ρ) + N^i H_i + H_m ]`, with `W_AQUAL` the Legendre dual of `μ_10` chosen so
that `δW/δ(lnN) = C_M^(10)`. MOND is carried on the **lapse** (operative arm = modified gravity), so slow
matter feels `a = −∇Ψ`, `Ψ=c²lnN` — correct flat rotation curves; `C_M=0` reduces to exact AQUAL,
`D_i[μ_10(|DΨ|/a0)D^iΨ]=4πGρ` (sympy residual 0).

**Dirac chain (generated, not guessed):**
- `S_1 = π_N` (primary)
- `S_2 = C_M^(10)` (from `π̇_N ⇒ 0`; `1/N>0` inert)
- `{π_N, C_M} = L_N ≠ 0` — the ONE generated second-class pair (elliptic, `L_N = μ k² + yμ' k_par²`)
- `S_3 = {C_M, H_can}_red ≈ 0` **weakly**: (i) `{C_M,∫N C_M}=0` (C_M momentum-free), (ii) `{C_M,∫N^i H_i}
  = L_ξ C_M = ∂_i(ξ^i C_M) ∝ C_M ≈ 0` because `lnN` is a genuine weight-1 scalar density (a q-carrier
  would NOT be covariant: `δ_ξ q − ξ·dq = −(1/3)div ξ ≠ 0`, cert 6b), (iii) `{C_M,H_m}=0` in vacuum.
- Preserving `C_M` therefore **fixes the lapse-velocity multiplier `u_1`** via `{C_M,π_N}=L_N≠0`.
  `S_4` is never reached.

**Result:** `rank Δ = 2`, `det = L_N²`. `N_grav = 2(T)+0(V)+1(S) = 3` — a **residual conformal scalar**,
the same extra-scalar disease the F(A²) lapse-carrier no-go predicts, now seen from the Dirac side.
`{MOND exterior} XOR {rank-4}`: attempt-A keeps the MOND exterior (`C_M=0` *is* the MOND equation,
`q'~1/r ⇒ v²~const`, verified numerically) but pays N_grav=3. FAILED for the Type-II 2-DOF goal.
(inverse_chain_A.out, ALL BOOLEAN CHECKS PASS.)

---

## 2. Attempt B — conformal kinetic term: chain closes at rank 4, N_grav=2

`H_can = ∫d³x [ N·C_M^(10)(q,γ) + (σ/2)p_q² + H_TT + H_m ]`, kernel on `q=−(1/6)ln det γ`,
`p_q=−2γ_ij π^ij`, `{N,π_N}={q,p_q}=1`. H_can is **linear in N** with coefficient `C_M`, so
`{π_N,H_can}=−C_M` yields **exactly** `C_M^(10)` on preservation (residual 0 on the exact lattice). Only
the `(σ/2)p_q²` term is a MODEL-ASSUMPTION (the replaced GR refoliation sector); scalar/TT decoupling is a
stated MODEL-ASSUMPTION.

**Dirac chain (generated, verified exactly on the lattice):**
- `S_1 = π_N`, `S_2 = C_M^(10)`
- `S_3 = {C_M,H_can} = σ L^[p_q] = σ D_i[A^{ij}D_j p_q]`, `A^{ij}=μ_10 δ^{ij}+yμ_10' n^i n^j` — the **full
  frozen AQUAL Hessian** on the trace momentum, **NOT `D²p_q`**. (Cert `S_3 − σ(∂C_M/∂q)·p_q = 0`.)
- `S_4 = {S_3,H_can} = σ²Ĉ[p_q,p_q] − σL̂²[N]` — **contains N**, hence INDEPENDENT (fixes the lapse
  multiplier). Chain terminates at length 4.

**Result:** single-mode `det Δ = σ⁴ L_N⁸`, `Pf = σ² L_N⁴`; full nonlinear lattice `rank Δ = 4(n−1)` for
n=3,4,5 (rank 4 per nonzero mode; the 4-dim null space is the single k=0 homogeneous mode). `L_N =
μ_10 k_perp² + (μ_10+yμ_10') k_par² > 0` for all `y>0` by frozen-kernel ellipticity (`μ_10>0`,
`μ_10+yμ_10' = y(y¹⁰+2)/(1+y¹⁰)^{11/10} > 0`). ⇒ **N_grav = (20−12−4)/2 = 2**, no scalar ghost. The
guessed `D²q=0` kill is **evaded** because the generated `S_2` is the nonlinear flux, not `D²q`.
Degeneracy only at the measure-zero `y=0` locus (`det ~ y⁸`). (inverse_chain_B.out, ALL BOOLEAN CHECKS
PASS.)

**So the DOF/rank gate is NOT where the theory dies.**

---

## 3. The decider — the SLIP (this is where it dies)

`DERIVATION`, two independent methods agreeing (fc4ac_slip.py):
- Method A: solve the two full elliptic laws (`S_2` fixes curvature Φ on secant modulus `μ`; generated
  `S_4` fixes lapse Ψ on tangent modulus `μ+yμ'`).
- Method B: traceless projection of the auxiliary stress `Π^aux = Σ_A λ_A δS_A/δγ` (with the multipliers
  `λ = −Δ⁻¹ r` computed from the actual Dirac inverse — `λ_2` nonzero even at `r_M=0`, fed by `r_3`,
  exactly as the corrected slip-decider spec requires).

Both give the identical `(Φ−Ψ)'`, and

```
  slip  Φ'/Ψ' = (μ_10 + y μ_10')/μ_10
        y→∞ (solar):    1     A_slip=0    Φ=Ψ  (PASS — verified as hard as the FAIL)
        y~1 (knee):     3/2   A_slip=1/2  Φ≠Ψ  (FAIL)
        y→0 (galaxies): 2     A_slip=1    Φ≠Ψ  (FAIL)
  A_slip(y) = y μ_10'/μ_10 = 0  ⟺  Φ=Ψ
```

The factor-2 swing is **y-dependent**, so **no constant normalisation sets `γ_PPN=1` at all
accelerations**. Solar system is safe (`y≫1`); the failure is a **galactic weak-lensing** slip — deep-MOND
efficiency `(Φ'+Ψ')/(2Ψ')→1.5`, a 50% excess over the `Φ=Ψ` (Mistele+24 KiDS) baseline. This is milder
than, and distinct from, the source-free chassis' `γ_PPN=0` that fails everywhere.

**Origin (DERIVED, not a free choice):** `γ_PPN=1` is structurally excluded in Embedding I because
`∂²H_can/∂N²=0` (linear-in-N, forced so that `π_N`-preservation delivers `C_M`) sends the generated `S_4`
onto the tangent modulus while `C_M` fixes the curvature on the secant modulus. The mismatch **is** the
kernel's `yμ'`. (fc4ac_slip.out, ALL BOOLEAN CHECKS PASS.)

---

## 4. Preferred-frame sector — α_3 kills it independently

`DERIVATION` (fc4ac_alpha_ppn.py). Given `γ_PPN=1` (kernel on q) and the spectator GR momentum
constraint:
- `α_1 = 0`, `α_2 = 0` — **PASS** (the control's `α_1=4` is a `γ=0` artifact of Embedding II and does not
  transfer; manufacturing it here would be a false deficit).
- `α_3 = C_{Φ1..4} ∈ [−3,−2] ≈ −1` — **FAIL**, `|α_3|<4×10⁻²⁰` pulsar/ephemeris bound violated by
  `>5×10¹⁹×`. Structural: the second-class `C_M` ⇒ Newtonian-order momentum non-conservation in the 0i
  (g_00) sector; elliptic instantaneous lapse response. **Slip-independent, embedding-independent.**
  (fc4ac_alpha_ppn.out, ALL 12 BOOLEAN CHECKS PASS.)

---

## 5. Matter coupling — PASS (corrects an earlier in-passing claim)

`DERIVATION` (fc4ac_matter2.py, decider). In Embedding I, `∇_μ T^{μν}=0` w.r.t. `g` **HOLDS** exactly on
the constraint surface, to all orders in v/c. Because H_can is linear in N with matter inside `C_M`
(`−√g c²ρ`), `{π_N,H_can}=−C_M=−S_2` is an **imposed constraint** (`r_1` weakly zero), NOT the nonzero
`−(H_g+ε_n)` source of the old source-free chassis. `π_N` pairs **only** with `S_4`; matter enters
`S_3,S_4` (`∂S/∂ρ≠0`) yet `{π_N,S_2}={π_N,S_3}=0` exactly. The lattice-consistent block gives
`λ_M=(S_2 e+S_4 d)/(a d)` = a combination of constraints ⇒ `λ_M=0` on Σ. Hence fifth force
`F5=Σλ_C{p_m,S_C}=0` on Σ, matter feels `a=−∇lnN` (pure geodesic of g), **no bimetric `g_eff`** (unlike
the Embedding-II control's `G_eff=2G`).

This **corrects** the in-passing transfer in FC4AC_construct_B.md Sec.5 / inverse_chain_B, which imported
the Embedding-II identity. The PASS does not rescue the theory: the same linear-in-N structure that
secures it forces the slip. Caveat: the PASS presupposes rank Δ=4 is consistently reached and
scalar/TT decoupling (full `q–h_TT` York coupling = residual OPEN). (fc4ac_matter2.out, ALL 21 BOOLEAN
CHECKS PASS.)

---

## 6. Synthesis and verdict

**Closure vector** `(rank Δ=4 ✓, A_slip≠0 ✗, α_1=0 ✓, α_2=0 ✓, α_3=−1 ✗, ∇T=0 ✓, c_T=1 assumed)`.

The 4-auxiliary-constraint Type-II count is **reachable** for a genuine spatial-gradient MOND constraint
(attempt B, evading the `D²q=0` kill) — this refutes the intuition that the gradient structure forces
early closure or degeneracy. But the theory is **not** a real relativistic MOND theory in this class:

1. **`Φ=Ψ` in the MOND regime FAILS** — slip `(μ+yμ')/μ:1→2`, structurally forced by the linear-in-N
   H_can. This is the MOND-specific obstruction, derived from the generated chain itself.
2. **`α_3=−1` FAILS** by `>5×10¹⁹×`, independently and embedding-independently.
3. Matter conservation PASSES but does not rescue.

Hence **MOND-SPECIFIC-NO-GO** for the analyzed linear-in-N (Embedding-I) 4-AC construction with `mu_10`.

**Not PARTIAL-lensing-ok:** PARTIAL presupposes `Φ=Ψ` holds (lensing ok) with only α_3/matter killing.
Here `Φ=Ψ` itself fails in the MOND regime, so lensing is *not* ok — PARTIAL does not fit.
**Not INCONCLUSIVE:** the explicit H_can was written and the chain closed at rank 4.

### Open doors (this is NOT "theory closed")
- **sf42 auxiliary-Legendre pair** `(χ,Φ)` with independent momenta carrying MOND **off the lapse**: 2
  second-class pairs ⇒ 2 DOF **without** linear-in-N, so the slip argument need not transfer. **Not
  executed — genuinely open.**
- **Full q–h_TT (York) coupling** beyond scalar/TT decoupling: OPEN, and it underlies both the rank-4
  count and the matter PASS.
- Phenomenological inputs `a0²=κ²c²Gρ_Λ`, `a0(z)~√ρ_DE`, `κ=½`, `Z~21` are untouched by this verdict.

---
*All load-bearing claims tagged THEOREM/DERIVATION/COMPUTATION/EXTERNAL-INPUT/MODEL-ASSUMPTION/OPEN in
the JSON. Every certificate re-run 2026-08-28, exit 0. External inputs: Iyonaga-Kobayashi 2109.10615,
De Felice-Mukohyama-Pookkillath 2302.02090.*
