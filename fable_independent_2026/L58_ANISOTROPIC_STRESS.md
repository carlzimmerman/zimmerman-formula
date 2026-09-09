# L58 — the MOND scalar's anisotropic stress, and whether the deposited no-slip result survives it

**2026-09-09.** Script: [`L58_anisotropic_stress.py`](L58_anisotropic_stress.py) →
[`L58_anisotropic_stress.out`](L58_anisotropic_stress.out) (exit 0; 30 checks, **1 FAIL**, and the FAIL
is a correction to a stated error bar, not to a result).

---

## The headline

**No slip survives, and for a better reason than anyone had written down.** The MOND sector's anisotropic
stress is real, is not small, does not vanish in spherical symmetry, and does not vanish off it. But it is
one order down in the potentials, and — the part that was not known — it enters with the **opposite sign**
to general relativity's own second-order term and **partially cancels it**. The net second-order slip
source is `2 g g_N`, against pure general relativity's `2 g²`. In the deep-MOND regime, where `g_N ≪ g`,
**this theory has less slip than general relativity does.**

Numerically: `|M_lens/M_dyn − 1|` is **7 × 10⁻⁹** for the median SPARC galaxy, **5 × 10⁻⁷** for the worst
of the 175, **2.4 × 10⁻⁶** for the worst X-COP cluster, and **2.8 × 10⁻⁵** for a 2 × 10¹⁵ M⊙ cluster at
1 Mpc — the genuine worst case. The deposited claim, Φ = Ψ to better than 10⁻⁴ out to 1 Mpc, **stands**,
on both footings and both kernels, with a 3.6× margin at the worst point.

**The one correction owed to the deposited paper** (DOI 10.5281/zenodo.22667688) is to the *bound*, not to
the *result*: `L11` B4b's quoted `|Φ−Ψ|/|Φ| ≤ a₀L/(6c²)` has the wrong functional form. The slip scales as
the **potential depth** (Φ_N/4, exactly as in Schwarzschild), not as `a₀L`, and it is **mass-dependent**,
which `a₀L/(6c²)` is not. At 1 Mpc the stated bound is exceeded by 4.26× for the most massive clusters. The
numbers a gate depends on do not move.

---

## 1. The relayed identity: correct, and already committed

The relay was

```
E_A − (1/2) E_B = 2 b J'(s0²) s0²
```

flagged as "not in any committed file". **It is committed.** It appears verbatim in the lead's own
`qwen_claude_field_theory/closure_2026/USER_ACTION_BACKGROUND.md`: *"Hence E_A−E_B/2=2 b J1 s0^2. A
cosmological constant cannot cancel this anisotropic stress."* That file also gives the full background
block, `E_P = −C − bJ0`, `E_A = −C − bJ0 + 2bJ1s0²`, `E_B = −2C − 2bJ0`, `E_phi = 0`.

Derived here from my own rebuild of the density and my own Euler–Lagrange operator, it is **correct as
stated** (B1), and so is the rest of the block (B1b). Two further facts:

- the coherence operator `ξ²|∇⊥V|²` contributes **nothing** on that background (`φ'' = 0`, `B' = 0`), so
  the anisotropy is the bare `J'` term and not a healing-length artefact (B2);
- Λ cancels identically in `E_A − E_B/2`, which is why the lead's own conclusion — that the flat metric
  with a uniform scalar gradient is not a solution — is right.

### Which convention

The repository's live dispute (`L52_REPAIR_SCOPE_REVIEW.md`: `g_N = 2 J_Y w` at L52 line 633 against
`g_N = J_Y w` in `THE_ACTION` §3) turns out to be **the wrong axis**, twice over.

1. Carrying the coupling and J normalisations as free symbols `k_c`, `k_J`, the action's **own** static
   reduction gives `J_Y w = (k_c/k_J) × g`, i.e. proportional to the **total** acceleration
   `g = g_N + g_φ`, not to `g_N`. The theory's μ-function is `J_Y/(8πGb) − 1 = g_N/g_φ`. **Neither** side
   of the dispute is what this action produces (B3a). Both are bookkeeping about where `8πGb` lives.
2. It does not matter, because the **physical** anisotropic stress is normalisation-free: `J'` and the
   scalar's gradient rescale inversely, and `8πG(T_xx − T_yy)` comes out to `2 g g_φ` independently of both
   `k_c` and `k_J` (B3b). In the lead's own display normalisation the relayed combination is exactly
   `2 b J'(s0²) s0² = g g_φ/(4πG)` — i.e. `(1/8πG) × 2 g g_φ` (B3c).

**Answer to "in which convention":** the relay is right in the lead's display convention (`k_c = k_J = 1`),
where it equals `g g_φ/(4πG)`; and its physical content, `2 g g_φ`, is the same in every convention.

---

## 2. The relay names only one of the two blocks that carry anisotropic stress

This is the substantive correction to the relay's *reading*, and it is what flips the sign of the answer.

**Two** blocks of the action depend on the spatial metric through `h^{ij}` and therefore carry traceless
spatial stress, not one:

| block | contribution to `8πG(T_xx − T_yy)` |
|---|---|
| `−(2−K_B) J(Y)` — the MOND function (the one the relay names) | **+2 g g_φ** |
| `+2(2−K_B) J^μ ∂_μφ` — the AeST coupling of `∇φ` to the clock's 4-acceleration | **−4 g g_φ** |
| **MOND sector total** | **−2 g g_φ** |
| general relativity's own second-order block `\|∇Ψ\|² − 2∇Φ·∇Ψ` | **+2 g²** |
| **net second-order slip source** | **2 g g_N** |

with `g_N = g − g_φ`. Derived symbolically in C2 from the planar action's own O(ε²) Euler–Lagrange
equations, with the theory's own first integrals (`g_φ = 8πGb χ'`, `J' χ' = Φ' = g`) substituted.

Every remaining piece of the O(ε²) source carries `ξ²` or higher and is suppressed by
`(ξ/L)² ≤ (0.15 pc/kpc)² = 2.3 × 10⁻⁸` (C2b). The aether block adds `−c₁₄ g²`, at most `10⁻⁶` of the net
source anywhere including the Solar System (D6).

---

## 3. What the slip actually is, and the equation it obeys

In the planar ansatz the invariant slip is `Φ − Ψ` read in the isotropic spatial gauge — in the lead's
`(P, A, B)` variables, `P = Φ` and `A = B = −Ψ`, so the traceless spatial combination is **exactly** the
one the relay names, `E_A − E_B/2`. **The lead's background identity is the zeroth-order instance of the
slip source.** The observable is `M_lens/M_dyn = 1 − (Φ−Ψ)'/(2Φ')`.

At **linear** order the planar traceless equation is purely geometric, `(Φ−Ψ)''/(8πG) = 0` (C1). So the
deposited theory's no-slip result **holds in the non-spherical planar setting** the lead's exact identity
lives in — this was the specific worry, and it is discharged.

At **second** order the equation is

```
(Φ − Ψ)'' − (Φ − Ψ)'/r  =  −( 2 g g_N − c₁₄ g² ) / c⁴          (spherical form)
```

**Calibrated against a known exact solution** (C4): with `g_φ = 0`, `c₁₄ = 0`, `g = GM/r²` this ODE is
solved exactly at this order by the isotropic-coordinate Schwarzschild slip `Φ − Ψ = −(GM/2rc²)²`, giving
`|Φ−Ψ|/|Φ| = GM/(4rc²) = Φ_N/4`. The numerical pipeline reproduces that to 1.4 × 10⁻⁵ (D0).

### Is the anisotropic stress zero, small, or order one?

**Order one as a stress, and `J'` is indeed not small** — `J'/(8πGb) = g/g_φ` runs from 1.25 in the
deep-MOND outskirts through 4.9 at the transition peak to 9.9 × 10⁷ at Saturn (D1). What is bounded is
`g_φ`, which saturates at `0.6476 a₀` (ν_RAR) or `a₀/e` (exponential carrier). So `2 g g_φ` is always
**≤ general relativity's own `2 g²`**, and the two subtract.

### Spherical symmetry is not a protection, and not a source

The radial-minus-tangential stress in spherical symmetry is `2 b J' Y`, the identical expression to the
planar `T_xx − T_yy` (C3). The anisotropy neither vanishes on symmetry nor appears only off it. **No-slip
is an order statement, not a symmetry statement.**

---

## 4. Reconciling the three results — all three were right

The brief listed three live possibilities. The answer is the first, sharpened:

1. **Does it cancel against something?** Yes, partially and exactly: the AeST mixing block against the J
   block, and the remainder against general relativity's own second-order term. Net `2 g g_N`.
2. **Does it vanish in the spherical limit and appear only off symmetry?** No (C3).
3. **Is no-slip a linear-order artefact?** It is a linear-order *statement* — of exactly the same standing
   as `γ_PPN = 1` in general relativity, which is also not exact and whose own residual is `Φ_N/4`. That is
   not an artefact; it is the correct scope.

**Our own earlier lane** (`L51` B3a: a term built from the aether combination `S₂ = R⁽¹⁾₀₀` sources only
the 00 equation, every spatial component vanishing identically) **is untouched and does not cover this
case.** It is a statement at linear order in `h`, about a term built *from* `h`. The MOND scalar's stress is
built from `(∇φ)²` — second order in the field amplitude — and is invisible to a linear-in-`h` argument by
construction. Both results are right; they are about different orders.

**The lead's exact identity** makes the second-order piece visible because its "background" pairs an O(1)
scalar gradient with an exactly flat metric — a pairing that is not a solution, which is precisely what
`USER_ACTION_BACKGROUND.md` itself concludes. Restore the theory's own weak-field counting, in which the
scalar gradient is an acceleration as small as the Newtonian field, and the same term reappears one order
down.

---

## 5. The numbers

Both footings; both kernels (ν_RAR as carried, exponential carrier as cross-check). `c₁₄ = 1.98 × 10⁻⁶`.
Observable `|M_lens/M_dyn − 1| = |Φ−Ψ|'/(2Φ')`, which for Schwarzschild equals `|Φ−Ψ|/|Φ|` exactly, so the
comparison with the deposited "better than 1e-4" is like for like.

| system | slip |
|---|---|
| median SPARC disc galaxy, at its last measured radius | **7.4 × 10⁻⁹** |
| worst of 175 SPARC galaxies (UGC09133, R = 108 kpc) | **5.2 × 10⁻⁷** |
| median X-COP cluster, outermost radius | **1.0 × 10⁻⁶** |
| worst X-COP cluster (A2142, R = 1000 kpc) | **2.4 × 10⁻⁶** |
| 10¹⁵ M⊙ cluster at 1 Mpc | **1.4 × 10⁻⁵** (pure GR would give 1.2 × 10⁻⁵) |
| 2 × 10¹⁵ M⊙ cluster at 1 Mpc — **the worst case** | **2.8 × 10⁻⁵** (pure GR: 2.4 × 10⁻⁵) |

Footing-to-footing spread is under 2% (the slip is set by the potential depth, and `a₀` enters only through
`g_φ/g`); kernel-to-kernel spread is under 2%.

### Does it disturb the lensing-versus-dynamics agreement?

No, by four orders of magnitude with room to spare. `L24` measures `M_WL/M_HSE = 1.154 ± 0.147` and
`S_lens − S_dyn = +0.369 ± 0.238` (1.55σ, canonical) / `+0.341 ± 0.220` (1.55σ, alt). The largest slip
anywhere in that sample is 2.4 × 10⁻⁶, which is **1.6 × 10⁻⁵ σ** and shifts `S_lens − S_dyn` by
`+4.8 × 10⁻⁶` on a ±0.246 measurement (D5). **The 1.55σ result is untouched.**

---

## 6. The one FAIL, and what it means for the deposited paper

```
[FAIL] D4b  L11 B4b's stated bound |Phi-Psi|/|Phi| <= a0 L/(6 c^2) numerically covers the slip
            this lane computes at 1 Mpc
            (L11's a0(alt) L/(6c^2) = 6.454e-06 vs this lane's worst case 2.750e-05 at 1 Mpc,
             ratio 4.26)
```

Two things are wrong with the quoted bound, and neither changes a result:

1. **Functional form.** `a₀L/(6c²)` is mass-independent and grows linearly in `L`. The slip is
   `≈ Φ_N/4` — it grows with the depth of the potential and is mass-dependent. The two happen to be within
   a factor of a few at 1 Mpc for a cluster; that is a coincidence of scale, not an agreement.
2. **Size.** For the most massive clusters at 1 Mpc the true slip is 4.26× the stated bound, so
   `a₀L/(6c²)` is **not a bound**.

**Recommended wording for the deposited paper**, replacing "Φ = Ψ to better than 10⁻⁴ out to 1 Mpc, so
lensing and dynamics share one potential — the framework's lensing requirement, met structurally rather
than fitted":

> The static weak-field limit has **no slip at Newtonian order**: `∇²(Φ − Ψ) = 0`, so lensing and dynamics
> share one potential, in planar as well as spherical symmetry. As in general relativity, this is exact
> only at that order. The second-order residual is `|Φ − Ψ|/|Φ| ≈ Φ_N/4`, the isotropic-Schwarzschild
> value, **reduced** by the MOND scalar's own anisotropic stress by the factor `g_N/g`: 7 × 10⁻⁹ for a
> typical disc galaxy, 2 × 10⁻⁶ for an X-COP cluster, and below 3 × 10⁻⁵ for the most massive cluster at
> 1 Mpc.

The word **"exactly"** should not be attached to no-slip. `γ_PPN = 1` is the right comparison and the right
standard, and this theory meets it.

---

## 7. Controls

Nothing above would mean anything without these, and all pass.

- **A1a/A1b — the reduction is licensed.** I rebuilt the covariant → static planar reduction from
  `THE_ACTION_2026-09-05` §1 (metric, clock normal, projector, 4-acceleration, `Y`, the coherence
  contraction, `√−g R`), and it equals the lead's displayed planar density up to a total x-derivative:
  the Euler–Lagrange residual of the difference vanishes for all four fields. This also fixes the
  identification `ca = c₁₄`, `b = 2 − K_B`, `C = Λ/(8πG) + K(0)`, and confirms
  `U = e^{−2A}φ'² + ξ²e^{−4A}[(φ''−A'φ')² + 2B'²φ'²]` covariantly.
- **A2 — CONTROL 1.** The lead's spatial-diffeomorphism Noether identity
  `P'E_P + A'E_A + B'E_B + φ'E_φ − (E_A)' = 0` reproduces as an **exact symbolic zero** from my own
  rebuild and my own Euler–Lagrange operator, with arbitrary differentiable `J`. **The lead's result is
  confirmed.**
- **A3.** The identity holds sector by sector (EH, aether, mixing, constant, J), not only for the sum.
- **A4b — CONTROL 2.** The deposited theory's own no-slip result reproduces at its own order and
  background: the spherical isotropic-gauge conformal equation is `∇²(Φ − Ψ) = 0` at linear order,
  rebuilt from the metric (`L11` A4c, not imported). A4c reproduces its quoted number arithmetically.
- **A5.** GR + minimally coupled static dust → Poisson with `G_N = 1/(8πm)` and no slip.
- **C4/D0.** The slip ODE and the numerical integrator are calibrated against the exact
  isotropic-coordinate Schwarzschild slip, to 1.4 × 10⁻⁵.

---

## 8. Verdict

The relayed identity is correct as stated, is already committed in the lead's own
`USER_ACTION_BACKGROUND.md`, and does read as an anisotropic stress — but it names only one of the two
blocks of this action that carry one, and the block it omits, the AeST coupling `2(2−K_B)J^μ∂_μφ`, carries
twice as much with the opposite sign. Kept exactly, the MOND sector's anisotropic stress does not create a
slip; it cancels part of the slip general relativity already has, leaving a net second-order source
`2 g g_N` that is smaller than GR's own `2 g²` by the factor `g_N/g`, which in the deep-MOND regime is the
small quantity.

No-slip therefore survives — as an order statement of exactly the same standing as `γ_PPN = 1`, in planar
symmetry as much as in spherical, and it is not a linear-order artefact but a linear-order *scope*. The
deposited claim "Φ = Ψ to better than 10⁻⁴ out to 1 Mpc" stands on both footings and both kernels with a
3.6× margin at the genuine worst case, and the lensing-versus-dynamics agreement at 1.55σ is disturbed at
the 10⁻⁵ σ level.

One amendment is owed and it is small: `L11` B4b's quoted bound `a₀L/(6c²)` has the wrong functional form
and is exceeded 4.26× by the true worst case at 1 Mpc, and the word "exactly" should not be attached to
no-slip in a paper whose own metric sector is Einstein's.
