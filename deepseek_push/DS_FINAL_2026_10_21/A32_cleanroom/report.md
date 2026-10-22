# A32 — Clean-room re-derivation

**Scope.** Independent referee lane. I opened no lane directory `A1_*` … `A30_*`, no `FINAL_THEORY.md`,
no `README.md`, nothing in `_parent/`, and I searched for no answer anywhere. Everything below is
derived from the equations quoted in the assignment, using `sympy` 1.13.1 / `numpy` 1.26.4.
My numbers are in `a32_results.json` under `my_numbers`, and every result is re-computed and
reported PASS/FAIL by `a32_checks.py` (output in `a32.out`, 0 failures).

Constants used: `c = 2.99792458e8`, `G = 6.67430e-11`, `Lambda = 1.0890e-52 m^-2`,
`a0_can = 9.36e-11 m/s^2`, `K = 4 pi G`.

---

## R1 — `a0/(c H_Lambda)`, and the number 12

Starting from `rho_Lambda = Lambda c^2/(8 pi G)`:

```
G rho_Lambda = G Lambda c^2/(8 pi G) = Lambda c^2/(8 pi)
sqrt(G rho_Lambda) = c sqrt(Lambda/(8 pi))
a0 = kappa c sqrt(G rho_Lambda) = kappa c^2 sqrt(Lambda/(8 pi))          (exact)
H_Lambda^2 = 8 pi G rho_Lambda/3 = 8 pi G/3 * Lambda c^2/(8 pi G) = Lambda c^2/3
H_Lambda = c sqrt(Lambda/3)                                             (exact)
```

Therefore

```
a0/(c H_Lambda) = kappa c^2 sqrt(Lambda/(8 pi)) / (c^2 sqrt(Lambda/3))
                = kappa sqrt(3/(8 pi)) = sqrt(6) kappa/(4 sqrt(pi))       (exact in kappa)
```

Numerically `sqrt(3/(8 pi)) = 0.345494149471336`, so

| quantity | value |
|---|---|
| `a0/(c H_Lambda)` at `kappa = 1/2` | **0.172747074735668** |
| `a0` at `kappa = 1/2` (from the constants) | **9.354173e-11 m/s^2** |
| `H_Lambda` | **1.806234e-18 s^-1** |
| `a0_can` quoted | 9.36e-11 (my value is 0.062 % lower — consistent) |

The factor `kappa = 1/2` therefore gives `a0 = 0.1727 c H_Lambda`, **not** `12 c H_Lambda`.
The number 12 is nowhere in this ratio: `12/kappa` would require `kappa = 34.73`.

**`2 sqrt(32 pi/3)`:** `= 11.5776200729`. So **12 is not equal to `2 sqrt(32 pi/3)`; 12 is
3.6482 % larger** (equivalently `2 sqrt(32 pi/3)` is 3.5198 % smaller than 12). The identification
"12 = 2 sqrt(32 pi/3)" is a 3.6 % numerical coincidence, not an identity — `2 sqrt(32 pi/3) =
4 sqrt(8 pi/3) = 4/sqrt(3/(8 pi))`, whereas the ratio derived above is `kappa sqrt(3/(8 pi))`,
i.e. the reciprocal structure, and no value of `kappa` makes `kappa sqrt(3/(8 pi)) = 12` unless
`kappa = 34.733`.

---

## R2 — the two galactic laws

Both laws are solved for `g` at fixed `g_N`. Write `y = g_N/a0`, `nu = g/g_N`.

**Canonical:** `g_N = g^2/(g+a0)` ⟹ `g^2 - g_N g - g_N a0 = 0` ⟹

```
g/a0 = (y + sqrt(y^2 + 4y))/2 ,      nu = (1 + sqrt(1 + 4/y))/2
```

**Alternative:** `g^2 - g_N^2 = a0 g_N` ⟹

```
g/a0 = sqrt(y^2 + y) ,               nu = sqrt(1 + 1/y)
```

### (a) Strong-field limit of `g - g_N` as `g_N → ∞` (the constant term)

```
canonical  : g - g_N = (sqrt(g_N^2 + 4 g_N a0) - g_N)/2  →  a0        (exactly a0)
alternative: g - g_N = sqrt(g_N^2 + a0 g_N) - g_N        →  a0/2
```

So the two laws differ by a **constant offset `a0` vs `a0/2`** at high acceleration — an
`O(1)` difference in the offset, un-suppressed as `g_N → ∞`. This is the sharpest
observational discriminator between them.

### (b) Leading large-`y` behaviour of `nu(y) - 1`

```
canonical  : nu - 1 = 1/y - 1/y^2 + 2/y^3 -   5/y^4 + O(y^-5)
alternative: nu - 1 = 1/(2y) - 1/(8y^2) + 1/(16y^3) - 5/(128 y^4) + O(y^-5)
```

Leading terms: **`1/y` (canonical)** and **`1/(2y)` (alternative)** — the alternative law's
correction is exactly half the canonical one at leading order, consistent with (a).

### (c) Maximum fractional difference in `g` at fixed `g_N`

Define `f(y) = (g_can - g_alt)/g_can`. With `s = sqrt(y)`,

```
g_can/a0 = (s^2 + s sqrt(s^2+4))/2 ,   g_alt/a0 = s sqrt(s^2+1)
f(s) = 1 - 2 sqrt(s^2+1)/(s + sqrt(s^2+4))
f'(s) = 0  ⟺  s sqrt(s^2+4) = s^2 + 1  ⟺  s^2(s^2+4) = (s^2+1)^2  ⟺  2 s^2 = 1
```

so the extremum is at `s^2 = 1/2`, i.e. **`g_N/a0 = 1/2` exactly**, and

```
f_max = f(1/2) = 1 - sqrt(3)/2 = 0.133974596215561   =  13.3975 %
```

`f(0+) = 0` and `f(∞) = 0`, so this is the global maximum (confirmed by a 2×10^6-point
numerical scan: max 0.1339745962 at `y = 0.499998`). At `g_N = a0/2` the canonical law gives
`g = a0` exactly and the alternative gives `g = (sqrt(3)/2) a0`.

Other normalisations of the same maximum, for completeness:
`(g_can-g_alt)/g_alt = 15.470 %`, `(g_can-g_alt)/g_N = 26.795 %`.

---

## R3 — quadratic tensor action and `c_T^2`

Setup: flat FRW, `N = 1`, zero shift, `h_ij = a^2 (delta_ij + gamma_ij)` with `gamma_ij`
transverse-traceless (`gamma^i_i = 0`, `D_i gamma^ij = 0`). I used the explicit mode
`gamma_ij = eps sigma(t) cos(kz) diag(1,-1,0)`, which is exactly TT, and expanded the ADM
Lagrangian

```
L = (N sqrt(h)/(4K)) [ R3 + K_ijK^ij - (1+beta) theta^2 - 2 Lambda ] + L_P
```

to second order in `eps`, with `K_ij = d_t h_ij/(2N)` and `theta = h^ij K_ij`. The `P`-sector
contributes nothing here: on FRW `Pbar = 0` by isotropy, and every `P` operator is at least
linear in `P` (the tadpole) or quadratic, so nothing mixes with `gamma` at quadratic order.

**Result (the averaged quadratic Lagrangian, exact in `a(t)`):**

```
<L2> = a^3/(16K) * [ sigma_dot^2 - (k^2/a^2) sigma^2 + 4(2+3 beta) H sigma sigma_dot
                     + ((6+9 beta) H^2 + 2 Lambda) sigma^2 ]
```

i.e. in covariant form

```
S_2 = (1/(4K)) ∫ dt d^3x a^3 [ (1/4) gamma_ij' gamma^ij' - (1/(4a^2)) d_k gamma_ij d^k gamma^ij
                               + H (gamma_ij gamma^ij)' + (1/2)(3H^2 + Lambda) gamma_ij gamma^ij + beta-terms ]
```

with `' = d/dt` and `H = a_dot/a`. The kinetic coefficient is `A = a^3/(16K) = a^3/(64 pi G)`
and the gradient coefficient is `B = -a/(16K)`:

```
omega^2 = -(B/A) k^2 = k^2/a^2      ⟹      c_T^2 = a^2 omega^2/k^2 = 1
```

**`c_T^2 = 1` exactly** — the ratio is `1` symbolically (`cT2 == 1` returns `True` in sympy),
with no dependence on `beta`, `Lambda`, `H`, `a0`, `eta` or `gamma`.

**Why.** The two coefficients come from different operators and neither is deformed:

* `gamma_dot^2` comes only from `K_ijK^ij`, whose TT part is `(1/4) gamma_ij' gamma^ij'` with the
  canonical weight; `theta^2` cannot contribute because `delta theta = 0` at first order for a TT
  mode (`theta = 3H - (1/4)(gamma^2)'`, so `theta^2`'s second-order piece is a total derivative
  plus a mass-type term).
* `(d gamma)^2` comes only from `R3`; for TT modes `R3 = -(1/4) d_k gamma_ij d^k gamma^ij`
  (up to a total derivative), and `R3` carries no `beta`, `Lambda` or `P` dependence.
* `Lambda` enters only through `sqrt(h) = a^3(1 - gamma^2/4)`, i.e. only the mass sector.
* the `P` sector is `O(P)`/`O(P^2)` with `Pbar = 0`, so it cannot correct either coefficient.

Independent confirmation: I computed the exact 4D Einstein tensor for the same metric and
extracted the TT combination `d/d eps (G^x_x - G^y_y)|_{eps=0}`, which is proportional to
`sigma'' + 3H sigma' + (k^2/a^2) sigma` with **ratio exactly 1** to the massless operator. So the
mode is exactly luminal in this action.

**Which operators could break `c_T^2 = 1`:**
1. any operator mixing the tensor with the `P` sector at quadratic order when `Pbar != 0`, e.g.
   aether-like `P^iP^j R_ij`, `K_ij P^iP^j`, or `E_i E_j gamma^ij` with `E_i ∝ K_ij P^j`
   (these re-weight the gradient term relative to the kinetic one);
2. a non-minimal coupling of the tensor to a background scalar, `f(phi) R` type, or `f(phi)`
   multiplying `K_ijK^ij` (not present here — no scalar multiplies the gravitational operators);
3. higher-derivative curvature operators: `Weyl^2`, `gamma^ij □ R_ij`, `R^2`-type terms;
4. a first-order `delta theta != 0`, which would require a non-TT (trace) perturbation to leak
   into the tensor sector.
None of these is present in the action as given, and the `(1+beta) theta^2` operator — the only
one with a free coefficient — provably does not break it.

**Honest caveats (flagged, not hidden):**

* `beta` is *not* absent from the quadratic Lagrangian: it appears as
  `4(2+3beta) H sigma sigma_dot + (6+9beta)H^2 sigma^2`. It never touches `sigma_dot^2` or `k^2`,
  so it cannot change `c_T^2`; it only shifts the mass/total-derivative sector
  (`-(3 beta H/2)(gamma^2)' = -(3 beta/2) d_t(H gamma^2) + (3 beta Hdot/2) gamma^2`).
* The mass sector `((6+9beta)H^2 + 2 Lambda) sigma^2` is background-dependent. On the only
  background the supplied (matter-free) action admits, `3H^2 = Lambda`, `Hdot = 0`, the mode
  equation reduces exactly to `sigma'' + 3H sigma' + (k^2/a^2) sigma = 0`. In a background with
  matter the pure-gravity quadratic action leaves a residual term proportional to the pressure
  `p` (I get `-16 pi G p` for `beta=0`); the matter action is not part of the supplied Lagrangian,
  so I cannot check its cancellation here. Either way it is a mass term, not a speed term, and
  `c_T^2 = 1` is unaffected.

---

## R4 — static background: `theta`, anisotropic stress, slip

**Extrinsic curvature.** On a static background (`d_t h_ij = 0`, zero shift, arbitrary static lapse
`N(x^i)`) the extrinsic curvature is

```
K_ij = (1/(2N)) (d_t h_ij - D_i N_j - D_j N_i) = 0        (background)
```

Perturb `h_ij -> h_ij + delta h_ij` with `delta h^i_i = 0` (trace-free) and keep the shift zero:

```
delta K_ij = (1/(2N)) d_t delta h_ij
delta theta = delta K^i_i = (1/(2N)) d_t (delta h^i_i) = 0
```

I verified this symbolically for a *general* trace-free perturbation (5 independent components) on
a flat static background with arbitrary `N(x,y,z)`: `theta^(0) = 0`, `theta^(1) = 0` identically,
and the Jacobi cross-check `theta = d_t ln det h/(2N)` holds. **`theta`'s perturbation vanishes at
first order for a trace-free perturbation.** (Contrast: a perturbation with trace `tr` gives
`theta^(1) = 3 d_t(tr)/(2N) != 0` — the vanishing is specific to trace-free modes.)

**Anisotropic stress.** Every operator of the extra sector is `O(P)` (the tadpole `P^i D_i ln N`)
or `O(P^2)` (`-W(u)`, with `W = (a0^2/K)[u^2/(2a0^2) + ...] = O(P^2)`; `(eta/2)E_iE^i`;
`-(gamma/2)(D_iP^i)^2`; `-(gamma/4)F_ijF^ij`). With `Pbar = 0` on the background, the stress
tensor `T^{P}_{ij} = (2/(N sqrt h)) delta S_P/delta h^ij` has **no term of order `P^0`**, so its
first-order perturbation vanishes:

```
delta Pi ≡ delta(p_r - p_t) = 0      at first order
```

(`delta theta = 0` removes the only scalar quantity that could have sourced a first-order `delta P`.)

**Consequence for the metric potentials.** In the Newtonian gauge
`ds^2 = -(1+2Phi) dt^2 + a^2(1-2Psi) delta_ij dx^i dx^j`, the traceless part of the `ij` Einstein
equation is sourced only by the anisotropic stress: `k^2(Phi - Psi) ∝ Pi`. With `Pi = 0`,

```
Phi = Psi          i.e.   Phi/Psi = 1      (no gravitational slip)
```

and the lensing potential is `Phi + Psi = 2Phi`, exactly as in GR.

**Branch I cannot exclude from the stated assumptions.** The statement above uses `Pbar = 0`.
The tadpole `P^i D_i ln N` does *not* allow `Pbar = 0` in a generic static background: varying
`P^i` gives `|D ln N| = u/(1 - u/a0)` with `u = K|P|`, so any `grad N != 0` forces `Pbar != 0`
(radial). In that branch the sector carries a *background* anisotropic stress and its first-order
perturbation is sourced by `delta(D ln N) = grad Phi`, so `delta Pi != 0` at first order is
possible, and then `Phi != Psi`. The value of `Phi/Psi` in that branch needs the background
profile `Pbar(r)`, which is not determined by the equations supplied (no `P`-equation solution was
given), so I cannot quote a number. **Both branches are stated; the "no slip, `Phi = Psi`" answer
is the one that follows from `Pbar = 0` plus a trace-free perturbation.**

---

## Summary of my numbers

| Result | My value |
|---|---|
| R1 `a0/(c H_Lambda)` | `kappa sqrt(3/(8 pi))` = `0.345494 kappa` |
| R1 at `kappa = 1/2` | **0.172747074735668** |
| R1 `a0(kappa=1/2)` from constants | **9.354173e-11 m/s^2** (vs `a0_can` 9.36e-11, 0.062 % low) |
| R1 `2 sqrt(32 pi/3)` | **11.5776200729**; 12 is **3.6482 %** larger → **12 ≠ 2 sqrt(32 pi/3)** |
| R2a strong-field offset | `a0` (canonical), `a0/2` (alternative) |
| R2b `nu-1` leading | `1/y` (canonical), `1/(2y)` (alternative) |
| R2c max fractional difference | **1 - sqrt(3)/2 = 13.3975 %** at **`g_N/a0 = 1/2`** exactly |
| R3 `c_T^2` | **1 exactly** (β, Λ, H independent; exact TT Einstein eq. massless) |
| R4 `delta theta` (first order, trace-free) | **0** |
| R4 `Pi` (first order) | **0** |
| R4 `Phi/Psi` | **1** (no slip) |

---

## How the code was validated (so the numbers above are not trusted blindly)

1. The 3D Ricci-scalar routine was validated on three independent cases before use: unit `S^3`
   (must give `R3 = 6`), a flat metric in a reparametrised coordinate (must give `0`), and the
   closed form for `diag(A(z),1,1)` (must give `-A''/A + (A'/A)^2/2`). It failed the first version
   of the test (index-convention bug in `Gamma^c_ab`), which I found and fixed — the delivered
   code is the fixed one.
2. The Gauss–Codazzi identity `sqrt(-g) R = sqrt(h)(R3 + K_ijK^ij - K^2) + 2 d_t(sqrt(h) K)` was
   verified to give **residual exactly 0** symbolically for the exact (unexpanded) TT metric. An
   earlier sign error in that identity was caught this way.
3. `c_T^2 = 1` was obtained twice, independently: from the ADM quadratic action coefficients and
   from the exact linearised TT Einstein equation computed from the 4D Ricci tensor.
4. The maximum in R2(c) was obtained twice: symbolically (`s^2 = 1/2`) and by a dense numerical
   scan that knows nothing about the derivative.

## Files

```
report.md          this document
a32_checks.py      all four derivations, prints PASS/FAIL, writes a32_results.json
a32.out            captured output of a32_checks.py (0 failures)
a32_results.json   numbers under "my_numbers" (plus the per-result copies)
gr_tools.py        validated 3D metric toolbox used for the Ricci/extrinsic-curvature checks
```

## Ambiguities / where I had to choose

* **R2(c)** "maximum fractional difference between the two laws in `g` at fixed `g_N`" has no
  unique normalisation. I report `(g_can - g_alt)/g_can` as the primary number (13.3975 % at
  `y = 1/2`); the alternatives are 15.470 % (relative to `g_alt`) and 26.795 % (relative to
  `g_N`). The location `y = 1/2` and the fact that the maximum is `1 - sqrt(3)/2` are
  normalisation-independent in form.
* **R3** "the quadratic action" depends on how total derivatives and background-constraint terms
  are handled, and the supplied action contains no matter sector to fix the background. The two
  coefficients that determine `c_T^2` are unambiguous; the mass sector is not, and I say so above.
* **R4** as discussed, `Pbar = 0` vs `Pbar != 0` gives two different answers for `Phi/Psi`; I give
  both and identify which follows from the stated setup.