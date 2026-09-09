# L26 — is σ > 1 admissible to the construction itself, independent of Cherenkov?

2026-09-08. Lane L26 of [CHARTER.md](CHARTER.md), the other half of the fork L19 is testing.
Script: [L26_sigma_above_one.py](L26_sigma_above_one.py) → [L26_sigma_above_one.out](L26_sigma_above_one.out).
Exit 2 by design: **34 checks, 33 PASS, 1 designed FAIL** (L26-P1, the stronger outcome that is false).

Nothing under `closure_2026/integrable_clock_construction_2026/` was imported, executed or modified. Every
coefficient was transcribed by hand from `IC4_ACTION.md` / `IC5_ACTION.md` / `TENSOR_BALANCE.md` /
`IC6_EVEN_CHARACTERISTICS.md` / `IC7_CURVATURE_SQUARE.md` / `LOCAL_WAVE_REPORT.md` into sympy, differentiated
symbolically, and evaluated at 60 digits with mpmath. Both mandatory controls reproduced before anything moved:
`S_4'(1)|_{σ=1/3} = −11.1407711251147987` (L26-C2) and `S_4'(1)|_{σ=1} = −20.194205022906776` (L26-C3).

---

## The one-line answer

**σ = 1.679 is admissible.** All fourteen health conditions the construction states for itself hold there,
none of them has an upper edge at σ = 1, and the interval (0, 1] turns out to be an **undefended subluminality
convention** — declared once in prose, copied into two metadata strings, and never evaluated by any code path.
The construction's own first internal ceiling on σ is **J_T > 0 at σ = 1.7716**, above σ\*.

---

## 1. Why IC-4 bounds σ at 1 — category (b), with a documentary edge of (c)

`IC4_ACTION.md`, lines 69–70 and 77–78, **verbatim**:

> Define $a_*=3-81/(4\mathcal T)>0$ and select the **fixed design parameter**
> $\sigma=1/3$. More generally the calculation covers $0<\sigma\le1$.

> These coefficients are fixed before any sector is tested. The squared-speed
> parameter $\sigma$ is a construction choice, not a prediction fitted to data.

That is the entire statement of the bound. There is no derivation attached to it — no stability,
hyperbolicity, positivity, well-posedness, "because", "requires" or "excluded" anywhere in the eighteen lines
around it (**L26-D1**).

The interval appears 11 times in the lead's directory, in 11 files. Every one of those is either the prose
sentence above or a copy of one of two `domain` metadata strings that get printed into the run record:

| file | line | what it is |
|---|---|---|
| `IC4_ACTION.md` | 70 | the prose declaration |
| `local_clock_wave.py` | 229 | `"domain":"...; 0<sigma<=1"` — a printed string |
| `quadratic_dirac.py` | 352 | `domain="...0<sigma<=1; ..."` — a printed string |
| `wave_contract.json` + 7 `wave_run_001/*` records | — | copies of the same two strings |

**No `assert`, `if`, `while` or `raise` anywhere in the construction mentions σ at all.** The only executable
restriction ever placed on it is `sigma = s.Symbol("sigma", positive=True)` in `local_clock_wave.py` — i.e.
**σ > 0** (**L26-D2**). The upper limit is prose, not a condition any calculation was ever tested against.

**Where the preference *is* executable, and this matters.** One sector away, `ic11_clock_pressure.py:56–57`
encodes subluminality as a live predicate:

```python
healthy = bool(PX > 0 and Q >= PX and energy > 0 and physical_H > 0
               and A != 0 and Qbare != 0)
```

`Q >= PX` **is** `cs² ≤ 1`, since `cs² = PX/Q`. `IC11_CLOCK_PRESSURE.md:63` says so:
*"They are necessary and sufficient for `PX>0`, `Qclock>0`, `0<cs^2<=1`."* It sits there as **one deletable
conjunct beside five genuine positivity and rank conditions** (**L26-D3**). So the construction's own code
already distinguishes health from subluminality, and then adds subluminality on top.

**But it is a different number** (**L26-D4**). IC-10/IC-11's `cs²` is an *output* of the pressure function
P(X,w) and runs with S (0.0956, 0.1271, 0.2265, 0.2577 at S = .03, .05, .10, .20); IC-4's σ is an *input*
fixed once at 1/3 on the IC-4 expanding witness. Two backgrounds, two action revisions, and no IC file states
their relation. **This lane speaks only to the IC-4/5/6/7 handle. The σ decision has to be taken twice.**

**Verdict on the question as posed:** category **(b)** — a physics choice, keep the clock inside the shared
null cone, the same choice Cherenkov would make for a subluminal mode — carried out with the documentary
character of **(c)**: never derived, never tested, and separable in the one place it is coded.

---

## 2. σ\*, re-derived rather than transcribed

L15's closed form was reproduced here by an independent route: symbolic implicit differentiation along the
constraint branch, giving my own expression for `S_4'(1;σ)` which **simplifies to exactly zero** against L15's
(**L26-G1**). Its single zero is at

    σ* = 4T/(4T−27) = 3/a_* = 1.679312732187113,   c_s = 1.29588299 c   (29.588% superluminal)

and it is the root of the single factor `3 p_R − 44`, i.e. `p_R(σ*) = 44/3` exactly; the other two factors
`(p_R T − 9)` and `(3 p_R + 4)` are strictly positive for every σ > 0 (**L26-G2**). The **full numerical
implicit-function derivative** — the same machinery that returned −11.1408 and −20.1942 — returns
`S_4'(1;σ*) = 0` to 40 digits (**L26-G3**), so the cancellation is a property of the branch, not of the
closed form alone.

| σ | p_R | S_4'(1) | J_T'(1) |
|---:|---:|---:|---:|
| 0.05 | 3.024 | −5.0734 | −1.043 |
| **1/3** (published) | 5.049 | **−11.1408** | −1.893 |
| 0.75 | 8.026 | −18.7291 | −3.143 |
| **1** (L15) | 9.812 | **−20.1942** | −3.893 |
| 1.25 | 11.599 | −17.6606 | −4.643 |
| 1.5 | 13.385 | −9.7514 | −5.393 |
| **1.6793 = σ\*** | **44/3** | **0** | −5.931 |
| 1.8 | 15.529 | +8.7740 | −6.293 |

---

## 3. The construction's own health conditions at σ\* = 1.679

Each computed, none assumed.

| # | condition | at σ\* | how it depends on σ |
|---|---|---|---|
| H1 | **no ghost** — kinetic `a_* = 1.78645 > 0` | ok | **exactly σ-free**. Reduced Lagrangian `a_*[ż² − σ(N₀k/A)²z²]`: kinetic sign needs `a_* > 0`, gradient sign needs **σ > 0**. Neither has an upper edge. |
| H1b | **positive mode energy** `E = ½(y² + σxz²)`, `E' = −3y² − σxz² ≤ 0` | ok | verified with σ symbolic; positive definite and monotone for **every σ > 0** |
| H1c | **reduced normalisation** `A_0 = det M/M22 > 0` | 0.461453 at the witness (σ-free), 0.46741 at j = 1.007 | σ-free at the witness (M11 = 0, M12/M22 σ-free) |
| H2 | **`c_T² = 1` exactly** | ok, and numerically 1.0000…0 at j = 1.007 | a **σ-identity**: K_T = G_T = J_T cancel. Control has teeth — the IC5 mutation returns J_T = 0.9142 ≠ 1 |
| H3 | **frozen domain `T > 27/4`** | T = 16.68651, det H_qq = 476.95 = 12(4T−27) | **T contains no σ at all** |
| H4a/b | **auxiliary constraint surface and its fold** | fold at **j = 1.21648796, identical** at σ = 1/3, 1, σ\* | `h|_{τ=0}` is **exactly σ-free** (symbolic), so the isotropic constraints, the branch, dq/dj and the fold are σ-independent identities |
| H5 | **J_T > 0 on the branch** | **0.04664 > 0** | **the one condition that genuinely moves.** Exactly *affine* in σ and monotone in j, so it reduces to its value at the fold: 0.72700 → 0.39020 → **0.04664** as σ goes 1/3 → 1 → σ\*. Zero at **σ = 1.7715257** |
| H6 | **det M ≠ 0** (IC7's normalisation) | det M\* = −13.75011, identical at every σ | M11 = 0 at the witness for every σ |
| H7 | **hyperbolic, characteristics real** | scalar 3.27085, tensor 1.94773 (squared coordinate speeds) | IC6_EVEN's exact reduced equation is `q̈ + 3q̇ + e^{2/3}k² diag(σ,1)q = 0`. Both squared speeds are positive for **every σ > 0**. σ > 1 changes *which cone is wider*, not whether either exists |
| H7b | **constraint rank / DOF count** | unchanged | LOCAL_WAVE's quadratic-Dirac matrix contains **no p_R at all**; det = 3F²h⁴(4T−27)(8T+x)/(2T) > 0, σ-free |
| H8 | **sheared fixture** exists, 0<u<1, in the η plateau | ξ = 0.235368, u = 0.660215, J_T = 0.91420 > 0, \|r²−1\| = 0.0348 ≤ 0.25 | the only place the auxiliary solve moves with σ (τ ≠ 0 makes the constraints see F) |
| X1/X2 | **clock leaves spacelike for the acoustic cone** | ok | see §4 — holds for **every σ > 0** |

**14/14 hold. Not one has an upper edge at σ = 1** (**L26-V1**).

### The one thing that does degrade, and the hard bound it gives

`J_T` on the isotropic branch is **exactly affine in σ** (the state is σ-free, F is affine in p_R, p_R is
affine in σ) and monotone decreasing in j, so the whole condition `J_T > 0` collapses to its value at the
fold. That affine law is verified against direct computation to 1e-12 and gives (**L26-H5, H5b**):

> **The construction's own first internal ceiling is σ < 1.7715257.** σ\* = 1.6793 sits below it with
> **5.49% headroom**. Any revision that moves `T`, the witness or the fold must re-check this inequality first.

---

## 4. The causality question, stated properly

In a theory with a preferred foliation, propagation outside the metric null cone is not by itself a causality
violation, because the preferred time supplies a global ordering. **That argument is available to this
construction specifically, not borrowed** (**L26-X3**): IC-4 varies a timelike clock T with X > 0 and only then
picks unitary coordinates; every object in the action (N, n_μ, h_μν, K_μν, a_μ, w, Q_μν) is built from that
foliation.

The clock mode's acoustic metric, built covariantly from the construction's own structures:

    G^{μν} = g^{μν} + (1 − 1/σ) n^μ n^ν,     G_{μν} = g_{μν} + (1 − σ) n_μ n_ν     (exact inverses, checked)

- **The leaf normal**: `G^{μν} n_μ n_ν = −1/σ`, **negative for every σ > 0**, so the normal is timelike and
  the leaves T = const are spacelike for the acoustic cone as well as the light cone (**L26-X1**).
- **Leaf tangents**: `G_{μν}v^μv^ν = g_{μν}v^μv^ν > 0` identically, because the correction ∝ (n·v)² = 0.
- **Cone nesting**: a g-null vector has `G_{μν}k^μk^ν = (1−σ)(n·k)²`, negative exactly when σ > 1 — the light
  cone sits **strictly inside** the acoustic cone above σ = 1, strictly outside below it (**L26-X2**).

So **T is a global time function for both cones, and the construction's causal-structure requirement is σ > 0
— the same condition as no-gradient-instability.** σ ≤ 1 controls which cone is wider, not whether the theory
is causal. Standard treatment cited rather than asserted: Babichev, Mukhanov & Vikman, JHEP 0802:101 (2008)
(k-essence superluminality, emergent metric, global time function); Bruneton & Esposito-Farèse, PRD 76, 124012
(2007); Blas, Pujolàs & Sibiryakov, JHEP 1104:018 (2011) and Blas & Sibiryakov, PRD 84, 124043 (2011)
(khronometric modes with speeds ≠ 1, universal horizons instead of causal pathology).

### And Cherenkov is satisfied at σ\* whichever way L19 rules

The bound this repository imposes — `1 − c_s ≤ 2e-15` (Moore & Nelson 2001; Elliott, Moore & Stoica 2005;
`g03v` V6; HANDOFF_CONTRACT A5) — is a **lower** bound: it constrains **subluminal** modes, because what a
UHE cosmic ray radiates into is a mode slower than itself. At σ\* the mode is 29.6% *super*luminal, so
`1 − c_s = −0.296` and the bound is satisfied with room (**L26-X4**).

> **L19's answer changes the lower edge of the allowed interval, never its upper edge.** σ\* is reachable
> whether or not the Cherenkov bound applies to a k-essence clock. The fork this lane and L19 were splitting
> is therefore *not* symmetric: only this half was load-bearing.

**Not settled here, named exactly.** (i) The **reverse** process: a superluminal mode can decay into ordinary
quanta if it couples to them. Matter is minimally coupled to g through the single unchanged `S_m[g,ψ]`, so the
clock reaches matter only through its metric perturbation and the exponential screening suppresses that
further — but **the rate is not computed here and is published nowhere in the IC files.** It is the one physics
gate a 29.6% superluminal clock still owes, and it is a calculation, not an assumption. (ii) Adams et al.,
JHEP 0610:014 (2006) obstructs a **Lorentz-invariant** UV completion of a superluminal EFT. This theory is not
Lorentz invariant at any scale, so the theorem does not fire; the standing cost is that no Lorentz-invariant
UV completion can ever exist for it. At σ = 1/3 that cost was already being paid.

---

## 5. What σ\* buys — at the size the numbers actually support

**The substantive gain is the SIGN, not the size** (**L26-H9**). At σ\*, `S_4 > 0` at **59/59** points of a
scan across the entire isotropic branch j ∈ (1, 1.2165), against `S_4 < 0` at 59/59 at both σ = 1/3 and σ = 1.
The reduced equation is `M_0 ζ̈ + S_4 k⁴ζ = 0` with M_0 > 0, so:

- `S_4 < 0` → IC6's real roots `λ ~ ±√(−S_4/M_0) k²`: a **growth rate rising like k²**, the Hadamard
  ill-posedness signature;
- `S_4 > 0` → `λ² < 0`: a **bounded oscillation** at frequency ~ k².

**The ill-posedness is removed on the whole branch, not merely reduced.**

`S_4` on the isotropic branch:

| j | S_4 (σ=1/3) | S_4 (σ=1) | S_4 (σ\*) |
|---:|---:|---:|---:|
| 1.002 | −0.0220564 | −0.0398048 | **+0.00114794** |
| 1.007 | −0.0752605 | −0.1343157 | **+0.0138267** |
| 1.02 | −0.2012475 | −0.3485684 | **+0.1077640** |
| 1.05 | −0.4312584 | −0.6940572 | **+0.5964019** |
| 1.10 | −0.6630800 | −0.9406589 | **+1.8362713** |
| 1.15 | −0.7537478 | −0.9726087 | **+2.8457034** |
| 1.21 | −0.7136954 | −0.9901854 | **+2.5289396** |

**And it is a window, not a point** (**L26-H10**). Both edges are computed:

| σ | S_4'(1) | S_4 > 0 on branch? | min J_T on branch |
|---:|---:|:---:|---:|
| 1.60 | −4.7742 | **NO** | 0.086749 |
| **1.6793 = σ\*** | 0 | yes | 0.046637 |
| 1.70 | +1.3716 | yes | 0.036174 |
| 1.74 | +4.1768 | yes | 0.015944 |
| **1.7716** | +6.5388 | yes | **−3.76e-5** |
| 1.79 | +7.9747 | yes | −0.009343 |

> **σ ∈ [1.6793, 1.7716)** — bounded below by the S_4 sign flip, above by J_T → 0 at the fold. 5.49% wide,
> c_s from 1.2959 c to 1.3310 c. A family, so not a fine tuning of one number — but narrow, and both edges are
> things the construction itself computes.

## 5b. What σ\* does NOT buy — the half a hopeful reading would get wrong

**IC7 is not made unnecessary** (**L26-H9b**, and the designed FAIL **L26-P1**). IC6_EVEN states its two
constructive conditions as `N_2 = N_2^T, S_4 = 0`. σ\* delivers `S_4 = 0` **only to first order at j = 1**.
The residual is quadratic at the witness, so |S_4| falls **19.2×** at j = 1.002 and **5.4×** at j = 1.007 —
but **grows away from it**: 1.38× larger at j = 1.05, 2.77× at 1.10, 3.78× at 1.15. `c_7 = −S_4/32` is still
required across the branch, now with the **opposite sign** (−0.000432 at j = 1.007 against +0.002352
published), so the narrow repair window and the tensor detuning `c_T² = 1 − 4c_7R̄_0/c` **do not disappear —
they change sign and move.**

**The sheared obstruction is untouched by anything computed here.** See the open items below.

---

## 6. What σ = 1/3 was baked into, and must be redone

| file | what moves |
|---|---|
| `IC5_ACTION.md` | *"Keep every IC-4 coefficient, including σ=1/3"* — F, A_R, B_R all move |
| `TENSOR_BALANCE.md:185` | *"These derivatives use the frozen σ=1/3 member"* — dF/dj and dJ_T/dj |
| `TENSOR_BALANCE.md:231–242` | the IC6 grid witness: residuals, Hessian eigenvalue 4.3989, J_T ≥ 0.99937 |
| `IC6_EVEN_CHARACTERISTICS.md` | the **sheared** numbers: N_2, the S_4 matrix, z² = 0.0301756, c_RR = 0.0020073 |
| `IC7_CURVATURE_SQUARE.md` | every c_7 value and the θ-cutoff window edges |
| `NONLINEAR_HAMILTONIAN.md:70`, `nonlinear_square_completion.py:53` | σ = 1/3 carried / hard-coded |
| `LOCAL_WAVE_REPORT.md:291` | *"For σ=1/3, four deterministic fundamental-matrix problems"* — cheap: the exact basis `cos r + r sin r`, `sin r − r cos r` with `r = √(σx)` is already σ-general |
| `ic11_clock_pressure.py:56` | the `Q >= PX` conjunct must be revisited, or justified |

**Verified NOT to move:** the witness itself, the isotropic constraint surface and its fold, the auxiliary
Hessian, det(M\*), `c_T² = 1`, the DOF count, `a_*`, `A_0`(witness), `T`, and every constant except
(p_R, q_R, A_R, B_R).

---

## 7. Open items, named exactly

1. **`S4_11(σ*)`, the sheared reduced quartic, and the antisymmetric mixing `N2_21`.** IC6_EVEN's
   −0.0642323935174161 and 0.000563025148110635 come from the lead's anisotropic two-mode reduction
   (`ic6_even_characteristics.py`), not reproduced in this lane. **σ\* cancels the ISOTROPIC obstruction;
   IC6_EVEN's second condition `N_2 = N_2^T` under shear is untouched by anything computed here and may well
   still fail. This is the single largest open item** — and the one the lead can settle fastest, by re-running
   that reduction with `p_R = 44/3`.
2. The finite-k correction to `c_s² = σ`, which needs the lead's background time derivatives.
3. Whether IC-4's σ and IC-10/IC-11's `cs² = PX/Q` are the same handle (L26-D4).
4. The superluminal mode's decay rate into ordinary quanta (§4).

---

## The PASS/FAIL ledger

33 PASS, 1 designed FAIL, exit 2.

```
[PASS] L26-D1  the interval is declared without a derivation
[PASS] L26-D2  it never appears as an executable condition; no assert/if/while/raise mentions sigma
[PASS] L26-D3  the one executable subluminality clause is IC-11's `Q >= PX`, separable from five health clauses
[PASS] L26-D4  IC-11's cs^2 is not IC-4's sigma
[PASS] L26-C1  the witness is stationary, F = 0, r = 1, at every sigma
[PASS] L26-C2  MANDATORY: S_4'(1)|sigma=1/3 = -11.1407711251147987
[PASS] L26-C3  MANDATORY: S_4'(1)|sigma=1   = -20.194205022906776
[PASS] L26-G1  independent symbolic re-derivation agrees with L15's closed form exactly
[PASS] L26-G2  one zero, sigma_* = 4T/(4T-27) = 3/a_* = 1.679312732, p_R = 44/3 exactly
[PASS] L26-G3  the full numerical branch derivative returns S_4'(1;sigma_*) = 0 to 40 digits
[PASS] L26-H1  no ghost; a_* = 1.78645 is sigma-free, gradient needs only sigma > 0
[PASS] L26-H1b positive mode energy, E' <= 0, symbolic in sigma
[PASS] L26-H1c A_0 = det M/M22 > 0 at the witness and at j = 1.007
[PASS] L26-H2  c_T^2 = 1 exact, a sigma-identity; IC5 control returns J_T != 1
[PASS] L26-H3  T > 27/4 holds; T contains no sigma; det H_qq = 12(4T-27) > 0
[PASS] L26-H4a the isotropic auxiliary constraints are exactly sigma-free
[PASS] L26-H4b the fold does not move: j = 1.21648796 at every sigma
[PASS] L26-H5  J_T > 0 on the branch at sigma_*, margin 0.04664; affine zero at sigma = 1.7715257
[PASS] L26-H5b sigma_* < 1.7716 with 5.49% headroom
[PASS] L26-H6  det M != 0; det M* = -13.750110 identical at every sigma
[PASS] L26-H7  hyperbolic; both squared speeds positive; the condition is sigma > 0
[PASS] L26-H7b the quadratic-Dirac constraint algebra is sigma-blind
[PASS] L26-H8  the sheared fixture exists at sigma_*, 0<u<1, J_T > 0, inside the plateau
[PASS] L26-H9  S_4 > 0 at 59/59 branch points at sigma_*: the ill-posedness is removed, not reduced
[PASS] L26-H9b and the honest half: IC7 is not made unnecessary, only sign-flipped and locally smaller
[PASS] L26-H10 a window, not a point: sigma in [1.6793, 1.7716)
[PASS] L26-X1  the clock leaves are spacelike for the acoustic cone: G^(mn) n_m n_n = -1/sigma < 0
[PASS] L26-X2  cone nesting; the causal requirement is sigma > 0, not sigma <= 1
[PASS] L26-X3  the preferred foliation is genuinely the construction's own dynamical field
[PASS] L26-X4  Cherenkov is a LOWER bound and is satisfied at sigma_* whichever way L19 rules
[PASS] L26-V1  VERDICT: sigma > 1 is admissible to the construction, 14/14 health conditions
[PASS] L26-V2  IC-4's (0,1] is an undefended subluminality convention
[PASS] L26-V3  the programme requirement is met: leading order gone, sign reversed, all health conditions hold
[FAIL] L26-P1  DESIGNED: the stronger outcome (S_4 = 0 identically, IC7 unnecessary) is FALSE
```

---

## Addendum — IC13, which appeared while this ran

`IC13_SHEAR_REPAIR.md` was written during this lane's run, on the **IC12** branch, not the IC4/5/6/7 chain
this lane computed. Nothing above was derived against it and nothing above is a claim about it. But it lands
on exactly the same question, so it is flagged rather than left for someone to rediscover:

> *"The quartic instability has been removed and the tested scalar frequency is real, but the remaining
> scalar speed is vastly superluminal."* — with `Ω²/(k²e^{2S})` reaching **5.6457e6**, i.e. **c_s ≈ 2376 c**.

Two things follow, and only two.

1. **The lead's newest step reaches the same fork independently**, and again treats a superluminal scalar cone
   as the defect to be repaired. Whatever is decided about IC-4's interval should be decided once, for both.
2. **§4's causality result is σ-uniform and therefore covers IC13's number too**: `G^{μν}n_μn_ν = −1/σ < 0`
   and leaf tangents have `G_{μν}v^μv^ν = g_{μν}v^μv^ν > 0` for **every** σ > 0, including the σ → ∞
   instantaneous limit that is the Hořava/khronometric λ → ∞ mode. So `c_s = 2376 c` is not a **causality**
   problem in a theory with this foliation either.

**What this does NOT say.** A cone that wide raises problems §4 does not touch and this lane has not computed:
the strong-coupling scale, matter-sector cone alignment (IC11_MATTER_GATE's coupled-cone condition), and the
decay gate of §4 — all of which get *worse*, not better, with σ. **σ\* = 1.679 and IC13's 5.6e6 are three and a
half orders of magnitude apart in σ, and only the first was tested here.** Do not read the σ\* result as
licence for the IC13 number.

---

## What the lead should do with this

1. **Re-run `ic6_even_characteristics.py` with `p_R = 44/3`** and read off `S4_11` and `N2_21` on the sheared
   state. That is the single decision this result now turns on. If the sheared conditions also improve, the
   IC-series has a genuinely simpler chassis; if `N_2 ≠ N_2^T` persists, σ\* buys the isotropic sector only —
   which is still the removal of a Hadamard ill-posedness.
2. **Amend `IC4_ACTION.md`'s interval or defend it.** As written it excludes the one value of its own design
   parameter that removes its own obstruction, on a preference it never states as a requirement. If the
   preference is deliberate, the file should say *why*; if it is convention, the interval should read
   `0 < σ < 1.7716` with the J_T bound as the reason.
3. **Decide whether IC-11's `Q >= PX` is a health condition or a taste.** The code already separates it from
   the five conditions that are.
4. **Do not read this as permission.** Superluminality is not free: it forecloses any Lorentz-invariant UV
   completion, and the mode's decay into ordinary quanta is an uncomputed gate.
