# FC-FINAL 4-AC Type-II MMG — Q3: matter conservation ∇_μT^μν

**Question.** In the 4-auxiliary-constraint (Type-II MMG) structure with the frozen kernel `mu_10`,
does matter minimally coupled to `g_μν` satisfy `∇_μ T^{μν} = 0` (w.r.t. `g`, on the preferred
foliation), or is it violated as in the OLD constraint-first chassis? The DFMP claim (arXiv
2302.02090) is that adding the auxiliary constraints **from the outset** keeps matter coupling
consistent. This tests that claim by derivation, not assertion.

**Verdict: DERIVED — FAIL** (w.r.t. `g`, at **Newtonian** order) for any *local* (galactic-scale)
MOND modification. Conservation is recovered only w.r.t. an **effective metric** `g_eff` → the
theory is secretly **two-potential/bimetric**. The DFMP "consistent-from-the-outset" escape is
**MOND-incompatible**: it works only because DFMP recover GR *locally*, which a MOND theory cannot do.

**Certificate:** `fc4ac_matter_conservation.py` → 10/10 boolean checks PASS, exit 0 (sympy 1.13.1);
frozen in `fc4ac_matter_conservation.out`.

Honesty labels: `THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED`.

---

## The one identity that decides it (THEOREM, cert Part 0)

Matter minimally coupled to `g_μν` enters the ADM Hamiltonian **only** through the standard term
`H_can ⊃ ∫ [ N ε_n + N^i j_i ]`, with `ε_n = T_{μν} n^μ n^ν` the Eulerian energy density
(`= ρc²` for slow dust). Since `π_N` is conjugate to `N`,

```
{ π_N(x), H_can }  =  −δH_can/δN(x)  =  −( H_g + ε_n )(x)   ≡  −H_perp_total(x).
```

This is **exact and general** (needs only ADM linearity in `N` + minimal coupling). The matter
density `ε_n` is **irremovable** from this bracket (`∂/∂ε_n = −1`, cert). Everything follows from
where this bracket lands:

- **GR:** `H_perp_total ≈ 0` is a **first-class** constraint; `{π_N,H_can} ≈ 0` *weakly*, determines
  nothing, and `N` is a gauge multiplier. `∇_μT^{μν}=0` is then an identity (contracted Bianchi).
- **Type-II MMG (2-DOF):** the scalar sector is removed by making `π_N` **second-class** (`S_1`).
  Now `{π_N, H_T}=0` does **not** give a constraint — it **fixes a Lagrange multiplier**, and that
  multiplier inherits `ε_n`. That multiplier multiplies the matter-carrying MOND constraint `C_M`
  ⇒ an extra force on matter.

---

## Adding matter disturbs the constraint surface (COMPUTATION, cert Part 1)

`{H_matter, S_A}` for the design set `(π_N, C_M, C_q, C_p)`:

| `S_A` | `{H_m, S_A}` | matter-sourced? |
|---|---|---|
| `S_1 = π_N` | `−ε_n` | **YES (exterior)** — decisive |
| `S_4 = C_p` | `(3/2) ρc²` (density-weight of `√γ ε_n`) | **YES (exterior)** |
| `S_2 = C_M` | `~ ρ·λ_M` | interior only (vanishes in vacuum) |
| `S_3 = C_q` | `0` | matter-free |

Two of the four preservation equations (`r_1`, `r_4`) pick up the matter density — exactly the
feature that killed the old chassis, and it is **generic to minimal coupling + second-class `π_N`**,
not special to the source-free `C_q`.

---

## The C_M multiplier is density-sourced (DERIVATION, cert Part 2)

General antisymmetric 4×4 Dirac block, all entries kept free
(`{π_N,C_M}=L_N`, `{C_M,C_q}=c_M`, `{C_q,C_p}=K`, lock entry `{π_N,C_p}=E`, `{C_M,C_p}=b`).
Solving `Δ·λ = −r`:

```
λ_M  =  ( E r_3 − K r_1 ) / ( E c_M + K L_N ) ,      ∂λ_M/∂r_1 = −K/(E c_M + K L_N) ≠ 0.
```

So the density-sourced `r_1 = −(H_g+ε_n)` **feeds the C_M multiplier**. `λ_M` is the coefficient of
the *only* matter-carrying term `λ_M C_M` in `H_T` (`C_M ⊃ −4πG ρ_m`), so **the matter force is set
by `λ_M`, and `λ_M` carries `ε_n`.**

- Baseline `E=b=0` reproduces the committed `λ_M = −r_1/L_N` (Gate 8 / `gate_matter_conservation`).
- **Escape condition** `λ_M = 0` (numerator `E r_3 − K r_1 = 0`): in the baseline this is `r_1 = 0`,
  i.e. `H_g + ε_n = 0` — **reinstating the first-class Hamiltonian constraint**. But that is *not* the
  2-DOF second-class mechanism; it is architecture **A** (diffeo-covariant, keeps `H_perp`, 6+ DOF —
  the AeST route, where `Φ` is sourced and `γ_PPN=1`, but at the cost of the DOF count and requiring
  MOND to live inside `H_perp` itself). With the generic lock (`E,b≠0`), `λ_M=0` needs a **fine-tuned
  `r`-cancellation** `E r_3 = K r_1` carrying `ε_n` exactly against the gravitational pieces — nothing
  in the committed record realises it, and it must be re-derived per construction (**OPEN**).

---

## On-shell divergence at Newtonian order (COMPUTATION, cert Part 3)

The `λ_M C_M` term gives point-particle `H_p = (N + χ) E_p`, `χ := −4πG λ_M/c²`. Hence at `(v/c)^0`:

```
a = −∇(Ψ + X),   X = c²χ            (Newtonian order, NOT O(v²/c²))
∇_μ T^{μi}|_g = −ρ ∂^i X  ≠ 0        ← violation = the λ_M force itself
∇_μ T^{μi}|_{g_eff} = 0   EXACTLY     (g_eff = lapse N+χ; coupling universal ⇒ absorb into a metric)
```

Conservation survives **only** w.r.t. `g_eff ≠ g` — a genuine **two-potential/bimetric** theory. This
is the same disease in both committed forks:
- source-free / Newton-`C_q` baseline → `G_eff = 2G` Newtonian doubling (`gate_matter_conservation`
  `.out`: 1.6×10¹¹× the 1-AU ephemeris bound);
- lock fork `C_q = D²(q+lnN)` → violation `(1−μ)`-gated (solar system repaired) but **deep-MOND
  repulsion** below `y_crit≈0.44`, RAR/BTFR destroyed (`gate_fork_S2prime_matter_mondlaw` `.out`).

---

## Foliation-invariant root cause (Part 4)

In GR with minimal coupling, `∇_μT^{μν}=0` is **equivalent** to the hypersurface-deformation
(Dirac) algebra `{H_⊥,H_⊥}~H_i`, `{H_⊥,H_i}~H_⊥`, `{H_i,H_j}~H_k` closing first-class — that *is*
"g is a covariant spacetime metric + contracted Bianchi." Type-II MMG replaces the first-class `H_⊥`
by the **second-class** `C_M`; `{C_M,C_M}` is not `~ H_i`, so the deformation algebra does **not**
close, so `∇_μT^{μν}=0` is **not an identity**. The committed Gate 10 (`08_matter_consistency.py`
[3.2]) already flagged this qualitatively ("full 4D `D_μT^{μν}=0` is NOT an identity, preferred
foliation"); this derivation **sharpens** it: the defect is **Newtonian order `(v/c)^0`**, via
`λ_M(ε_n)`, not the `O(v²/c²)` that Gate 10 originally guessed.

---

## Why the DFMP "consistent-from-the-outset" escape does not transfer (EXTERNAL-INPUT)

DFMP (2302.02090) obtain consistent matter coupling because their Type-II construction **recovers GR
locally**: `H_perp_total → 0` in the local weak field ⇒ `λ_M → 0` ⇒ **no local extra force**, so
matter conserves w.r.t. `g` where it matters (solar system, asymptotic flatness); the modification is
effectively cosmological. A MOND theory is **defined** by `H_perp_total ≠ 0` in the local galactic
weak field (that deviation *is* the `a0` physics), which forces `λ_M ≠ 0` there. **The DFMP escape and
the MOND requirement are mutually exclusive** — this is the MOND-specific obstruction, and it is
structural (depends only on minimal coupling + second-class `π_N`), not a kernel artifact
(`mu_10 → mu_exp → mu_5` all identical, per `gate_matter_conservation` Part C).

---

## Status and the single open door

- **FAIL (THEOREM-level)** for `∇_μT^{μν}=0` w.r.t. `g` under {minimal matter coupling ∧ second-class
  `π_N` (the 2-DOF mechanism) ∧ local MOND (`H_perp_total≠0` locally)}. The violation is Newtonian
  order; conservation is only recoverable w.r.t. an effective bimetric `g_eff`.
- **OPEN (narrow):** a generic-lock `r`-cancellation `E r_3 = K r_1` making `λ_M=0` *without* imposing
  `H_perp_total=0`. Nothing in the committed record realises it; and it would additionally have to
  keep MOND sourcing, `γ_PPN=1`, and exactly 2 DOF simultaneously — i.e. it collides with the same
  three-part decider left open by `FC4AC_SETUP.md §7`. No committed construction exhibits such a set.

### Provenance
- **This task:** `fc4ac_matter_conservation.py` (+ `.out`) — the `{π_N,H_can}=−(H_g+ε_n)` identity, the
  `{H_m,S_A}` table, the general `λ_M` solve, the on-shell `divT|_g` vs `divT|_{g_eff}`.
- **Committed cross-refs (re-read this session):** `openai_push/final_closure/`
  `gate_matter_conservation_derivation.py` (baseline `G_eff=2G`, `r_4=−(H_g+ε_n)`),
  `gate_fork_S2prime_matter_mondlaw.py` (lock fork, `λ_M` with `E`, deep-MOND repulsion),
  `scripts/08_matter_consistency.py` (Gate 10 honest defect flag),
  `scripts/03_dirac_matrix.py` (Dirac block, `Pf=L_N K`).
- **EXTERNAL:** DFMP arXiv 2302.02090 (Type-II 4-AC, consistent matter coupling *with GR recovered
  locally*); Iyonaga–Kobayashi arXiv 2109.10615 (2-DOF MMG, `γ_PPN=1`, GR local).
- **ASSUMED (never derived):** `a0²=κ²c²Gρ_Λ`, `a0(z)~√ρ_DE`, `κ=1/2`, `Z~21`.
