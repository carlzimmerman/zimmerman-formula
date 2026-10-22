# A68 — mutations

Nine dials. Each changes **exactly one input** — one coefficient of the frozen action, one term of the
action, one sign in the derived bracket, or one symmetry assumption — and each makes at least one named
check fail and exits 1. Reproduce any of them with

```bash
python3 a68_checks.py --mutate <name>
```

`none` is the canonical run: **39/39 PASS, exit 0** (`a68.out`, `a68_results.json`).

| mutation | what it changes (one input) | checks broken | measured (from the run) | why that is the right failure |
|---|---|---|---|---|
| `eta_neg` | `η → −1` | **D15** | `(β,η,α,γ) = (1,−1,1,1)`: `Q = +4.9999`, `ω² = +2.0e−9`, **`m_T² = −1.0`**, `c_s² = +2.0e−5` | the P kinetic term's sign is the mass sign: `m_T² = K/η`. With `η < 0` the two transverse P modes are tachyons even though the scalar stays healthy — the two conditions are independent. |
| `beta_neg` | `β → −0.25` | **D7**, **D11**, **D15** | `c_s² = −2.0e−7, −2.0e−5, −2.0e−3`; `Q(β=−0.25) = −5.000`; `ω² = −2.0e−9` | `Q = K(2+3β)/β` changes sign with `β` on the branch `2+3β>0`: the fifth mode becomes a ghost **and** a gradient instability in one stroke. This is the load-bearing sign. |
| `gamma_zero` | `γ → 0` (and therefore `α = γ → 0`, since the frozen action has one stiffness) | **D7**, **D15** | `c_s² = 0.000e+00` at every `p`; `ω² = +0.000e+00` | removing the `(D·P)²` operator removes the scalar's only restoring term: `V = αp⁴ = 0`, the mode is not an oscillator but a zero-frequency constraint on that slice. |
| `alpha_zero` | `α → 0` **only** (keeping `γ = 1`) | **D7**, **D15** | `c_s² = 0.000e+00`; `(β,η,α,γ) = (1,1,0,1)` | the same failure, isolated to the longitudinal gradient: it shows that `α` and `γ` are separate dials in the code but **one** coefficient in the frozen action (D16 checks the ratio of the two gradient coefficients is exactly 2). |
| `pp_term` | adds `+P_i D_j P^j` to `H_i^(P)` with unit coefficient (A66's claimed term, put in by hand) | **A5**, **A6**, **B1**, **B2**, **B8**, **B9** | coefficient of `P_i D_j P^j` `= 1.00000000000000`; linear in `(P,∂P)`: **False**; `H_i^(P)|_(π_P=0) = 1.0(P²)(D·P)²`; bracket `3/9`; `max|lhs−rhs| = 1.684e+01`; `{h_i, D·P}` `6/9` | this is the mutation that *tests A66's mechanism from the inside*: if the term existed, `H_i^(P)` would not be linear in `π_P`, the `π_P` bracket would acquire a `P`-dependent piece, `{h_i, P_k}` would stop being the diffeomorphism generator, and the `D·P` bracket would change too. All of them fail. |
| `bracket_sign` | flips the sign of the `−δ_i^j(D·π_P)δ` term in the derived bracket | **B1**, **B2**, **B5**, **B6** | bracket `6/9`; `max|lhs−rhs| = 3.034e+00`; eigenvalues `+0.85−4.46j` vs expected `−0.85−4.46j` | the sign of the ultralocal piece is what makes the eigenvalues `−b+ia` and not `+b+ia`; the check compares against the mode algebra of the action, not against the formula itself. |
| `drop_W` | removes the `W(u)` potential from the action | **C4**, **D9**, **D12**, **D14**, **D15** | `W''(0) = 0`; `m_T² = (K/2)/(η/2) = 0`; `0/36` grid points healthy; `H_perp − [|π_P|²/2√hη + √hK/2|P|²] = −K√hP²/2` | `W` is the **only** source of the P mass: `W''(0) = 1/K` ⇒ mass term `(K/2)|P|²` ⇒ `m_T² = K/η`. Without it the transverse modes are massless and the fifth mode's would-be mass disappears with them. |
| `eta_eq_gamma` | imposes `η = γ` (A67's assumption) as a symmetry of the action | **D10** | `c_T²(1,1) = 1.000`, `c_T²(2,1) = 1.000` — two different inputs give the same observable | `η` and `γ` are independently observable: the Jacobian `d(η, γ/η)/d(η,γ) = 1/η ≠ 0`. Forcing `η = γ` collapses the map to one parameter, which is exactly what makes A67's `m² = 2/L★²` an identity rather than a prediction. |
| `central_charge` | adds `10⁻³·δ_i^j` (a field-independent central charge) to the bracket | **B3**, **B4**, **B5**, **B6**, **B7**, **C5**, **C7** | `max|{H_i,π_P^j}|` on `π_P = 0` `= 1.0e−03`; rank there `= 3`; `SC` block rank `3` | a central charge is precisely what would make the pair second-class *on* the surface. It breaks the on-surface vanishing (B3), hence the count (C5/C7). Since the computed bracket has no such term, Route C cannot borrow it. |

Exit codes, recorded from the runs:

```
$ for m in eta_neg beta_neg gamma_zero alpha_zero pp_term bracket_sign drop_W eta_eq_gamma central_charge; do
    python3 a68_checks.py --mutate $m >/dev/null 2>&1; echo "$m -> $?"; done
eta_neg -> 1
beta_neg -> 1
gamma_zero -> 1
alpha_zero -> 1
pp_term -> 1
bracket_sign -> 1
drop_W -> 1
eta_eq_gamma -> 1
central_charge -> 1
none -> 0        (39/39 PASS)
```

## Checks that could not be made to fail, and what happened to them

* **An earlier `B2` (smeared Euler-derivative vs. a hand-guessed density kernel)** did not have a
  mutation-independent meaning: the two routes differed by a total derivative in the test function, and the
  "failure" under mutation was indistinguishable from the mismatch that was already there. It was **deleted**
  and replaced by a numeric instantiation of the verified mode-algebra identity (five random momentum pairs,
  random mode values, two independent code paths). The old version is not in the file.
* **A count check that asserted `DOF = 4` under Route C's added constraints** was deliberately *not* kept as a
  pass/fail check on the physics: it is arithmetic on a hypothesis. It survives only as `C7`, whose content is
  the *conditional* "4 requires `SC = 2`", paired with the computed `SC = 0`.
* **`β = 0` and `β = −2/3`** are not in the dial set. `β = −2/3` makes the θ Legendre map singular (A54 L8)
  and `β = 0` makes `Q` diverge: those are different theories, not perturbations of this one. They are
  discussed in the report, not mutated.
* **`N` and `√h`**: no mutation of the lapse normalisation was kept, because every check that involves them
  (A1, A2, C4) is homogeneous in `N` and a rescaling would pass trivially. That is a real limitation of the
  check set, not a hidden pass: the lapse dependence is fixed by A1/A2's closed forms, which carry `N`
  explicitly.
