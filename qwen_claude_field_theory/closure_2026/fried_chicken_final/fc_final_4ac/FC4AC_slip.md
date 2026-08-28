# FC-FINAL 4-AC Type-II MMG — THE SLIP `Phi − Psi` (Embedding I, kernel on `q`)

**Certificate:** `fc4ac_slip.py` → `ALL BOOLEAN CHECKS PASS (exit 0)`, 15/15 (sympy 1.13.1,
numpy 1.26.4). Frozen output: `fc4ac_slip.out`. Builds on the constructed `H_can` of
`FC4AC_construct_B.md` / `inverse_chain_B.py` (Embedding I: kernel rides on `q`).

**Task.** On the constructed `H_can`, compute the multipliers `lambda_A = −(Delta^{-1})_AB r_B`
(`r_A = {S_A, H_can+H_m}`, static galactic branch), the full auxiliary traceless stress
`(Pi^aux_ij)_TF = sum_A lambda_A (delta S_A/delta gamma_ij)_TF`, and the slip decider `A_slip(y)`.
Solve `(d_i d_j − delta_ij D^2/3)(Phi−Psi) = (Pi^aux_ij)_TF` **two independent ways** (full ij
eqns; traceless projection) and **require agreement**. Evaluate `A_slip` & `Phi−Psi` at `y≫1`,
`y~1`, `y≪1`. **PASS iff `Phi=Psi`.**

Honesty labels: `THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED`.
Frozen kernel `mu_10(y)=y/(1+y^10)^{1/10}` (`mu_10>0`, `mu_10+y mu_10'>0`). Phenomenological input,
never derived: `a0²=κ²c²Gρ_Λ`, `a0(z)~√ρ_DE`, `κ=1/2`, `Z~21`.

---

## VERDICT: **FAILED** — `Phi ≠ Psi` in the MOND regime (deep-MOND slip `Phi'/Psi' → 2`).

The decider `A_slip(y) = 0 ⟺ Phi=Psi` is **nonzero for every `y≲3`** and reaches its maximum
(`A_slip=1`, slip `=2`) across the entire deep-MOND band. `gamma_PPN=1` is **structurally
excluded** in Embedding I.

---

## 1. The one-line physics — one frozen flux, **two moduli** (DERIVATION, cert Part 1)

The frozen AQUAL flux is `F(q') = mu_10(y) q'`, `y = q'/a0` (radial). The two metric potentials
are fixed by **different moduli of the same flux**:

| potential | fixed by | which variation | modulus | value |
|---|---|---|---|---|
| `Phi` (spatial **curvature** `q=−(1/6)ln det γ`; lensing) | `C_M = 0` (the AQUAL **flux law** `r²μ_10 q' = const`) | vary `N` | **SECANT** `F/q'` | `mu_10` |
| `Psi` (**lapse** `ln N`; dynamics) | the **generated** `S_3 = σ L̂[p_q]` acting through the `q`-EOM (`L̂[N]=0`) | vary `q` | **TANGENT** `dF/dq'` | `mu_10 + y mu_10'` |

These are exactly the **transverse vs radial eigenvalues** of the generated frozen Hessian
`A^{ij} = mu_10 δ^{ij} + y mu_10' n^i n^j` (`L̂ = D_i A^{ij} D_j`, committed in
`inverse_chain_B.out`). They differ by `y mu_10' > 0` for **every** `y>0` (strict, since
`mu_10'>0`). **This modulus mismatch IS the slip** — and it is *forced*: linearising `C_M` in its
own field `q` (which is what the generated `S_3`, and the `q`-EOM that fixes the lapse, do) is the
**Hessian**, while `C_M=0` itself is the **flux**. One kernel, two moduli.

## 2. Multipliers and the auxiliary stress (COMPUTATION, cert Part 2)

Single propagating mode (from `inverse_chain_B` Part 3): `Delta` is the antidiagonal second-class
block pairing `(π_N↔S_4)`, `(C_M↔S_3)`, `det Delta = σ⁴ L_N⁸`. Solving `lambda_A=−(Delta^{-1})_AB r_B`:

```
lambda_2 (= C_M multiplier = the LAPSE) = +r_3/(σ L_N²)   -- depends on r_3, NOT r_2
lambda_4 (pairs with π_N)               = −r_1/(σ L_N²)   -- density-sourced, r_1=−(H_g+eps_n)
```

- **`lambda_2 ≠ 0` even when `r_2(=r_M)=0`** — the off-diagonal `(C_M↔S_3)` pairing feeds `r_3` in.
  This is **exactly the slip-decider spec** ("even `r_M=0` does NOT give `lambda_M=0`, `r_2,r_3`
  feed in"). `lambda_4` inherits the matter charge via `r_1=−(H_g+eps_n)` (committed
  `fc4ac_matter_conservation`).
- Static branch: `lambda_3` multiplies `δS_3/δγ ∝ p_q = 0`, so it **drops**. The operative
  multipliers are `lambda_2` (on `δC_M/δγ`) and `lambda_4` (on `δS_4/δγ`).
- **The only spin-2 (traceless) content** of both `δC_M/δγ` and `δS_4/δγ` is the kernel anisotropy
  `y mu_10' (n_i n_j − δ_ij/3)`; the `mu_10 δ^{ij}` and `√g` pieces are pure trace. Hence
  `(Pi^aux_ij)_TF = [O(1)] · y mu_10' (n_i n_j − δ_ij/3)` — the natural `A_slip` normalisation.

## 3. The slip, two independent ways — **they agree** (DERIVATION, cert Part 3)

Charitable source-matching (best case for the theory; **forced** by the Newtonian boundary
condition, where both moduli `→1` and both potentials `→ −GM/r`): the **same** MOND charge `C` for
both. In the spherical exterior:

- **Method A ("full ij eqns"):** solve each potential's own elliptic law and subtract —
  `Phi' = C/(r²μ_10)`, `Psi' = C/(r²(μ_10+y μ_10'))`.
- **Method B ("traceless projection"):** the auxiliary anisotropic stress
  `D_i[y μ_10' n^i n^j ∂_j Psi]` sources the difference through the `Phi`-operator:
  `μ_10 (Phi−Psi)' = y μ_10' Psi'`.

```
Method A:  (Phi−Psi)' = C (y¹⁰+1)^{1/10} / (r² y (y¹⁰+2))
Method B:  (Phi−Psi)' = C (y¹⁰+1)^{1/10} / (r² y (y¹⁰+2))     ✓ IDENTICAL (sympy: A−B ≡ 0)
```

The two methods give the **identical** `(Phi−Psi)'`. The normalisation-independent slip ratio
(`C` cancels):
```
Phi'/Psi' = (mu_10 + y mu_10')/mu_10 .
```

## 4. `A_slip(y)` and the three limits (COMPUTATION + sympy limits, cert Part 4)

The dimensionless, `r`-independent, normalisation-independent invariant the decider reduces to is
the **slip excess** `A_slip(y) = slip − 1 = y mu_10'/mu_10 = (normalised (Pi^aux)_TF)`.
`A_slip = 0 ⟺ y mu_10' = 0 ⟺ Phi=Psi`.

| `y` | `mu_10` | slip `Phi'/Psi'` | `A_slip` | verdict |
|---|---|---|---|---|
| 0.03 | 0.030 | **2.000000** | 1.000 | `Phi≠Psi` FAIL |
| 0.10 | 0.100 | **2.000000** | 1.000 | `Phi≠Psi` FAIL |
| 0.30 | 0.300 | **1.999994** | 1.000 | `Phi≠Psi` FAIL |
| 1.00 | 0.933 | **1.500000** | 0.500 | `Phi≠Psi` FAIL |
| 3.00 | 1.000 | 1.000017 | 1.7e−5 | `Phi=Psi` PASS |
| 10.0 | 1.000 | 1.000000 | 1e−10 | `Phi=Psi` PASS |

- **`y≫1` (NEWTONIAN, solar system):** `slip→1`, `A_slip→0` ⇒ **`Phi=Psi` (genuine PASS)**. Verified
  as hard as the FAIL — this is *not* the source-free chassis' `gamma_PPN=0` (which fails the solar
  system too). Cassini `gamma` is **safe** for this obstruction.
- **`y~1` (knee):** `slip=3/2`, `A_slip=1/2` ⇒ `Phi≠Psi` FAIL.
- **`y≪1` (DEEP MOND, galaxies):** `slip→2`, `A_slip→1` ⇒ `Phi≠Psi` FAIL. Curvature gradient is
  **twice** the lapse gradient; the `y`-dependent factor-2 swing admits **no constant
  normalisation** giving `gamma_PPN=1` at all accelerations.

`mu_10` is a **sharp** kernel: the slip is pinned at **exactly 2.000** across the whole deep-MOND
band `y≲0.3` (a wide plateau covering all galactic phenomenology), not a thin edge.

## 5. Consequence and scope (COMPUTATION, cert Part 5)

Point-mass (`M=6×10¹⁰ M_⊙`, `a0=9.36e−11`): the deep-MOND weak-lensing efficiency
`(Phi'+Psi')/(2Psi') → 1.5` — a **50% lensing excess** over the `Phi=Psi` baseline at galactic
radii (`r≳20 kpc`). This is in tension with the `Phi=Psi` Mistele+24 KiDS RAR (committed slip-1
stack), **milder** than the source-free chassis' factor-2 deficit but nonzero and structural. The
solar system sits at `y≫1` (`slip=1`), so this is a **galactic-lensing** FAIL, sharply distinct
from `gamma_PPN=0` which fails everywhere.

## 6. What this settles

This **derives the origin** of the committed FC-4AC slip verdict, no longer as a free design
choice: the **generated** `S_3 = σL̂[p_q]` and `S_4 = σ²Ĉ − σL̂²[N]` *force* the lapse `Psi` onto
the **tangent** modulus `mu_10+y mu_10'`, while `C_M` fixes the curvature `Phi` on the **secant**
modulus `mu_10`. Because `H_can` must be linear in `N` (that is what makes `π_N`-preservation
deliver `C_M`), `N` enters every generated constraint linearly and the lapse is pinned to the
linearised Hessian — the mismatch is **structural**, `gamma_PPN=1` is excluded in Embedding I.

**Sector-orthogonal, unchanged by the slip (EXTERNAL-INPUT, committed):**
- `alpha_3 = −1` (elliptic instantaneous lapse response; `ppn_mmg_gate_2026.py`).
- `∇_μ T^{μν} ≠ 0` at Newtonian order (density-sourced `C_M` multiplier `lambda_2=lambda_M`;
  `fc4ac_matter_conservation.py`).

---

### Provenance
- **This task:** `fc4ac_slip.py` (+ `.out`) — secant/tangent moduli; `lambda_A=−(Delta^{-1})_AB r_B`
  with `lambda_2∝r_3`, `lambda_4∝r_1`; `(Pi^aux)_TF ∝ y mu_10'(n n−δ/3)`; two-method
  `(Phi−Psi)'` agreement; `A_slip=y mu_10'/mu_10`; three limits; point-mass lensing efficiency.
- **Builds on:** `inverse_chain_B.py` / `FC4AC_construct_B.md` (generated chain `S_1..S_4`,
  `A^{ij}=mu δ+y mu' n n`, `det Delta=σ⁴L_N⁸`), `fc4ac_setup_scaffold.py` (`C_q→Phi→slip` map).
- **Committed cross-refs (sector-orthogonal):** `ppn_mmg_gate_2026.py` (`alpha_3=−1`),
  `fc4ac_matter_conservation.py` (`∇T≠0`, `lambda_M` density-sourced),
  `gate_lensing_weakfield_derivation.py` (the mirror-image source-free `gamma_PPN=0`).
- **EXTERNAL-INPUT:** DFMP arXiv 2302.02090 (Type-II 4-AC, consistent matter coupling); Iyonaga–
  Kobayashi arXiv 2109.10615 (2-DOF spatially-covariant MMG `gamma_PPN=1`, `c_T=1` — but with GR
  recovered **locally**, the opposite of a *local* MOND modification).
