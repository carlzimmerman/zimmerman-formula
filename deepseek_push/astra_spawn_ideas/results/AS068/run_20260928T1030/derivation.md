# AS068 — Can a boundary condition remove the zero mode? — derivation

**Run:** `run_20260928T1030` · **Worker:** `deepseek/deepseek-v4-flash-0731` (OpenRouter), Hermes Agent subagent (single-run seed worker)
**Task hash:** `7bc8080a4a28054cb268c261a27d6ee908dfeb7c62c9a9f91420e13897fec576` (verified before execution)
**Branch:** CORE coefficient / conditional MU_n statistical response (n ≥ 1, real) — the declared branch of this seed. No other branch (Q, RAR, EXP, MONO) is used for any conclusion.

---

## 0. Result in one paragraph

The boundary condition **does** remove the additive zero mode of the MU_n primitive, exactly:
`J(Y_ref) = 0` with the specified kernel `J' = mu_n(Y) = 1 − (1+Y)^(−n)` fixes `J(0) = −∫₀^{Y_ref} mu_n(Y) dY`
(closed form for n = 2: `J(0) = −Y_ref²/(1+Y_ref)`; general-n closed form derived below; exact FTC,
verified symbolically and at 60-digit precision). But it does **not** remove the *freedom*: the constant
is relocated into the adopted datum `Y_ref` (one real dimensionless parameter in, one out; no equation of
the action fixes it — the pinned action class has no second scale, k01). And the determined vacuum
density is **negative for every finite positive reference and every n > 0** (`J(0) < 0`, theorem, Lean-certified),
so it cannot reproduce the positive `rho_Lambda` at any of the diagnostic references
`λ = Y_ref ∈ {1/2, 1, 2}` — counterexamples with ratios
`rho_vac/rho_Lambda = −5.9601e14, −1.7880e15, −4.7680e15` (K_B = 0; ×0.875 at K_B = 0.25).
A magnitude fine-tune `Y_ref* ≈ 1.672e-8` (K_B = 0) still lands **negative**. The kappa-closure use of the
boundary condition is therefore falsified in this action class; the removal identity itself is exact and
delivered as a scoped lemma.

**Outcome: counterexample** (to the constructive use of the claim) **+ derived identity** (the removal).

---

## 1. Precise claim, symbol dictionary, boundaries, assumptions

**Named claim under test** (from the seed's Mathematics): *"Impose J(Y_ref) = 0 and J' = specified kernel;
J(0) = −∫₀^{Y_ref} J'(Y) dY"* — can this remove the zero mode of the MOND scalar's primitive, i.e. fix the
additive constant that k01 proved blocks the a0–Lambda derivation (k01 theorem K1–K2)?

| Symbol | Meaning | Status |
|---|---|---|
| `s` | `c·sqrt(G·rho_L)` — the vacuum's own rate, m/s² | framework input (units as declared by the seed) |
| `rho_L` | vacuum mass density entering `s`, kg/m³ | input; `rho_Lambda = 4 a0²/(G c²)`, `rho_Lambda = rho_L` at κ = 1/2 (A1 of the framework base) |
| `Y` | `g/s`, dimensionless drive | input |
| `Y_ref` (λ) | position of the boundary `J(Y_ref) = 0`, dimensionless, **finite positive** | the new external datum under test |
| `n` | MU_n exponent, **real n ≥ 1** | symbolic parameter of the conditional MU_n response |
| `mu_n(Y)` | `J'(Y) = 1 − (1+Y)^(−n)` — the specified static kernel (MU2 member at n = 2 on the adopted footing) | framework kernel (branch: conditional MU_n) |
| `J(Y)` | kinetic function of the MOND scalar (PD08 action, `S_kin = (1/8πG)∫ s² J(Y) d³x`; k01: statics depend on J only through J′ — the zero-mode theorem) | framework structure (sources PD08/k01) |
| `J(0)` | value of the primitive at the origin — the k01 additive constant (it enters the vacuum as `rho_vac = (2−K_B)·s²·J(0)/(16πG)` in s-units; k01 K3 structure) | to be determined by the boundary |
| `K_B` | coupling in `[0, 0.25]` (k01 band) | input |
| `kappa` | `a0/s`, **adopted = 1/2** | adopted input (not derived here) |
| `a0` | `kappa·s`; canonical `9.3619e-11`, alternative `1.1279e-10` m/s² | registered footings (READMe/STANDING) |

Assumptions (all stated, none imported from another branch):
1. The static response is the conditional MU_n family with the L230 normalisation `mu_n(∞) = 1` and slope `mu_n(0) = n` (PD01 A1–A4; PD08 B1–C1; k01 K1). This is the seed's declared branch.
2. The vacuum contribution of the primitive is `rho_vac = (2−K_B)·s²·J(0)/(16πG)` — the k01 K2/K3 structural result carried from the pinned source (sign conventions identical to k01: `J(0) < 0 ⇒ rho_vac < 0` there; this run recomputes `J(0)` in s-units).
3. `Y_ref` finite and positive (physical domain `Y ≥ 0`; `Y = 0` is the Newtonian end, `Y → ∞` the deep end — the seed's limiting regimes).

Framework inputs vs conclusions established here:
- **Inputs:** `s`, `rho_Lambda`, `kappa = 1/2`, `K_B ∈ [0, 0.25]`, `mu_n` kernel, boundary `J(Y_ref) = 0`, constants `G = 6.67430e-11`, `c = 299792458`.
- **Conclusions:** (i) removal identity `J(0) = −∫₀^{Y_ref} mu_n dY` (exact); (ii) closed forms; (iii) sign theorem `J(0) < 0 ∀ n>0, Y_ref>0`; (iv) relocated-freedom diagnosis (1 external datum introduced); (v) vacuum ratio formula and counterexamples; (vi) limiting behaviour.

---

## 2. The determined constant and the count of external data

**Derived constant (n = 2, the adopted MU2 footing, s = 2a0):**

```
J(0) = −∫₀^{Y_ref} [1 − (1+Y)^(−2)] dY = −[ Y − (1+Y)^(−1) ]₀^{Y_ref} = −Y_ref²/(1+Y_ref)   [exact]
```

**General n ≥ 1 (n ≠ 1):** `J(0) = −[ Y_ref − ((1+Y_ref)^(1−n) − 1)/(1−n) ]`; **n = 1:** `J(0) = ln(1+Y_ref) − Y_ref`.
(Sympy Piecewise result; verified by direct differentiation `dJ(0)/dY_ref = −mu_n(Y_ref)` at n ∈ {1, 2, 3, 5/2, 4} and by 60-digit quadrature below.)

**Freedom count (the seed's step 2):** before the boundary, the primitive carried one free real additive
constant (the k01 zero mode). After `J(Y_ref) = 0`, the constant is fixed but one **real dimensionless datum
`Y_ref`** enters, fixed by no equation of the action. Net independent real DOF: **1 → 1**.
Verdict: the boundary condition is an **adopted convention**, not a physically derived boundary — nothing in
the pinned action (single scale `s`, k01's no-second-scale theorem) selects a value of `Y_ref`. The freedom
is relocated, not removed; kappa = 1/2 remains adopted and the k01 closure gap remains open at exactly the
same dimensionality. **This is the counterexample core:** the claim "a boundary condition removes the zero
mode" is true only in the trivial relocation sense; it supplies no independent derivation of the kappa
premise.

---

## 3. Intermediate algebra, scale factors, signs, units

The seed's configuration with signs and units spelled out:

```
s = c·sqrt(G·rho_L)                     [m·s⁻²]
Y = g/s                                 [1]
mu_n(Y) = 1 − (1+Y)^(−n)                [1]  ;  mu_n(0) = n (Newtonian slope = channel count, PD01)
J(Y_ref) = 0                            [1]  (the boundary)
J(0) = −∫₀^{Y_ref} mu_n(Y) dY           [1]  (FTC, exact — the constant is determined by the reference)
rho_vac = (2−K_B)·s²·J(0)/(16πG)        [kg·m⁻³]  (k01 K3 structure in s-units; s²/G = kg/(m·s²) = J·m⁻³·... check: s² [m²s⁻⁴] / G [m³kg⁻¹s⁻²] = kg·m⁻¹·s⁻² = J·m⁻³ ✓)
rho_Lambda = 4a0²/(G c²) = s²/(G c²)    [kg·m⁻³]  (framework; = rho_L exactly at κ = 1/2)
R(Y_ref) := rho_vac/rho_Lambda = −(2−K_B)·c²·Y_ref²/(16π·(1+Y_ref))      [1, fully dimensionless]
```

Diagnostic counterexamples at λ := Y_ref ∈ {1/2, 1, 2} (exact rationals, n = 2):

| λ | J(0) | G0 := −J(0) | R (K_B = 0) | R (K_B = 0.25) |
|---|---|---|---|---|
| 1/2 | −1/6 | 1/6 | −5.9600554e14 | −5.2150485e14 |
| 1 | −1/2 | 1/2 | −1.7880166e15 | −1.5645145e15 |
| 2 | −4/3 | 4/3 | −4.7680443e15 | −4.1720388e15 |

All negative, all distinct, and the prediction **changes with λ** (control 1). Dimensional examples on the
two footings (λ = 1, K_B = 0): canonical `a0 = 9.3619e-11 m/s²`, `rho_Lambda = 5.844412454e-27 kg/m³`
→ `rho_vac = −1.0450e-11 kg/m³` (energy density `eps_vac = −9.3919e5 J/m³`); alternative `a0 = 1.1279e-10`
at **same κ = 1/2** → `rho_Lambda = 8.483089620e-27 kg/m³` → `rho_vac = −1.5168e-11 kg/m³`
(`−1.3632e6 J/m³`). At **fixed** canonical density the alternative acceleration implies
`kappa_eff = 0.60238840` — the footing-separation rule (never both fixed) is respected; the dimensionless
ratio R is footing-independent and applies to both footings as stated.

**Limiting regimes (leading neglected terms, domains):**
- Newtonian end `Y_ref → 0⁺`: `J(0) = −Y_ref² + O(Y_ref³)` → 0⁻. The boundary at the origin decides
  nothing (trivial empty vacuum; the constant returns as an undetermined limit). Domain `Y_ref ≪ 1`.
- Deep end `Y_ref → ∞`: `J(0) = −Y_ref + 1 − 1/(1+Y_ref) → −∞` for n = 2 (in general `−Y_ref + O(1)`
  because `mu_n → 1`). **No finite reference exists in the deep limit** — this is where the MU_n class
  differs from k01's class, whose kernel `Δ(s) → 0` made the primitive's span finite (`I = 2∫s dΔ`).
  Domain `Y_ref ≫ 1`.
- Kernel asymptotics (n = 2): `mu_2(Y) = 2Y − 3Y² + 4Y³ − 5Y⁴ + O(Y⁵)` (leading neglected term `−3Y²`,
  domain `|Y| ≪ 1`); `1 − mu_2(Y) = 1/Y² − 2/Y³ + O(Y⁻⁴)` (domain `Y ≫ 1`).

**Sign theorem (the counterexample's mathematical core):** `mu_n(Y) > 0` on `(0, ∞)` for every `n > 0`
(since `(1+Y)^(−n) < 1`), hence `∫₀^{Y_ref} mu_n > 0`, hence `J(0) < 0` for **every** finite positive
reference **and every n > 0**. In this action's sign convention (`rho_vac = (2−K_B)s²J(0)/(16πG)` with
`2−K_B > 0`), a boundary condition at any positive reference gives a **negative** vacuum density:
`R < 0` always. Only the *size* can be tuned: `|R| = 1` requires `G0(Y_ref*) = 16π/((2−K_B)c²)` i.e.
`Y_ref* = 1.6722424e-8` (K_B = 0) or `1.7877023e-8` (K_B = 0.25) — a boundary essentially at the origin,
itself an adopted fitted datum, and **still negative at that point** (`R(λ*) = −1.0`).

---

## 4. Independent checks (different representations; actual residuals)

1. **FTC by direct differentiation (symbolic, exact):** `d/dλ[J(0)] = −mu_n(λ)`, verified at n = 2
   (`d/dλ[−λ²/(1+λ)] = −(λ²+2λ)/(1+λ)² = −mu_2(λ)`, sympy residual 0) and at n ∈ {1, 3, 5/2, 4}
   (per-n symbolic residuals all 0).
2. **60-digit quadrature (mpmath, dps = 60):** `∫₀^λ mu_2 dY` vs closed form at λ = 1/2, 1, 2:
   relative residuals **0.0, 0.0, 0.0** (< 1e-30 threshold set before evaluation). General n at
   (n, λ) = (1,1), (3,1/2), (5/2,2), (4,1): relative residuals **3.8894e-62, 0.0, 0.0, 7.7788e-62**
   (< 1e-30). The identity is exact; the numerics confirm, not fit.
3. **Asymptotics:** `(mu_2−2Y)/(−3Y²) − 1 = 1.3333e-8` at Y = 1e-8 (expected (4/3)Y = 1.33e-8);
   `(1−mu_2)·Y² − 1 = −2/Y + O(3/Y²)`, residual 3.0e-12 at Y = 1e6 — the stated leading terms verified.
4. **Kernel limits (exact):** `mu_n'(0) = n`, `mu_n(∞) = 1` (symbolic) — the kernel saturates and its
   Newtonian slope is the channel count (PD01 consistency).
5. **Primitive limits:** at λ = 1e-10, `R = −3.576e-5 → 0⁻` (Newtonian end); at λ = 1e12,
   `J(0) = −1.0e12` matching `−λ + 1 − 1/(1+λ)` to relative residual 0.0 (deep end divergence).

All thresholds were set before evaluation (1e-30 relative for exact identities, 1e-6/1e-8 for the
asymptotic ratios); an exact identity is distinguished from finite consistency by the symbolic
differentiation (residual exactly 0) and the Lean certificate (§6).

---

## 5. Controls (each capable of failing) and the strongest surviving statement

**Control 1 — vary Y_ref, keep the kernel fixed (the seed's first control):**
`J(0)` at `Y_ref ∈ {1e-4, 1e-2, 1/2, 1, 2, 100}` = `−9.999e-9, −9.901e-5, −1/6, −1/2, −4/3, −99.01`
with corresponding `R = −3.576e7, −3.541e11, −5.960e14, −1.788e15, −4.768e15, −3.541e17` (K_B = 0):
**all distinct, strictly monotone** (`dG0/dλ = (λ²+2λ)/(1+λ)² > 0`, Lean-certified via `g0_strict_mono`).
Capable of failing: it *would* fail (i.e., the strong removal claim would survive) only if all Y_ref gave
the same vacuum prediction; they differ at every sampled reference. → The zero mode is **relocated**, the
freedom survives as the choice of Y_ref.

**Control 2 — limiting regimes (the seed's second control):** Newtonian end `Y_ref → 0⁺` → `J(0) → 0⁻`
(no information; the boundary trivializes). Deep end `Y_ref → ∞` → `J(0) → −∞` (no finite reference
exists for a kernel saturating to 1). Both exact statements; the deep-end divergence is the sharp
difference between the MU_n primitive and k01's convergent kernel class.

**Strongest surviving statement (exact, quantified):**
> For every real n > 0 and every finite positive reference Y_ref, the boundary condition `J(Y_ref) = 0`
> with kernel `J′ = mu_n` determines `J(0) = −∫₀^{Y_ref} mu_n(Y) dY < 0`; consequently, in the pinned
> action's sign convention (2−K_B > 0), `rho_vac/rho_Lambda = −(2−K_B)c² G0(Y_ref)/(16π) < 0` with
> `G0 = Y_ref²/(1+Y_ref)` at n = 2 — for every positive reference the determined vacuum has the wrong
> sign to be the positive rho_Lambda, and its magnitude is a monotone function of the adopted datum
> Y_ref. The boundary condition removes the additive constant but not the independent freedom; it does
> not close the k01 gap, and kappa = 1/2 remains adopted.

Statement class: counterexample for the constructive (closure) use, exact derived identity for the
removal algebra. Domain: MU_n class, all n > 0, all Y_ref > 0 (algebraic); numerically sampled
λ ∈ [1e-10, 1e12], n ∈ {1, 2, 2.5, 3, 4}, K_B ∈ {0, 0.25}, both registered footings.

---

## 6. Lean certificate

`AS068_boundary_zero_mode_certificates.lean` (self-contained, in this run dir) certifies the n = 2
algebraic core: `mu2_closed` (kernel rational form), `g0_pos` (G0 > 0), `j0_negative` (J(0) < 0 for all
positive references — the sign obstruction), `g0_deriv_eq_mu2` (G0 is the exact primitive of the kernel —
the FTC content of the removal identity), `g0_deriv_pos`, `g0_strict_mono` (prediction strictly monotone in
Y_ref — control 1, analytic form), `ratio_negative` (the vacuum ratio < 0 for c² > 0, 2−K_B > 0, Y_ref > 0),
`diagnostics_distinct` (1/6 ≠ 1/2 ≠ 4/3 — three distinct changed predictions).
Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` — **exit 0, zero `sorry`
(grep count 0), unfiltered `#print axioms` for all eight theorems = [propext, Classical.choice, Quot.sound]**
(⊆ the allowed set; full output in `lean_check.out`).

---

## 7. Both footings — application of the dimensionless result

The ratio `R(Y_ref)` is dimensionless and footing-independent; it applies to both registered footings
identically with the footing entering only through the conversion to absolute densities:
- **Canonical** `a0 = 9.3619e-11 m/s²` (`κ = 1/2` by construction): `rho_Lambda = 5.844412454e-27 kg/m³`,
  `s = 1.87238e-10 m/s²`.
- **Alternative** `a0 = 1.1279e-10 m/s²`: at **same κ = 1/2** → `rho_Lambda = 8.483089620e-27 kg/m³`,
  `s = 2.2558e-10 m/s²`; at **fixed canonical density** → `kappa_eff = 0.60238840`.
The two footings never share both fixed ρ and fixed κ (framework contract); examples given in §3.

---

## 8. Branch discipline and transfer

All conclusions live in the declared branch (CORE coefficient; conditional MU_n). The counterexample
does **not** transfer to the operative filtered-MONO target (Requirement 1) without a bridge: MONO's
continuation kernel `h'_mono = max(h'_RAR, δ h_p/(y+y_p)) > 0` is also positive, so a same-sign theorem
would hold there, but the primitive's span and the crossing structure differ (h_mono is not mu_n) —
deriving the MONO analogue is an explicit open step, not performed here. Q, RAR, EXP and MU2-as-branch
are not used for any conclusion (MU_n is the seed's own conditional branch). No causality criterion B
statement is made. G_N = 6.67430e-11 is used; G_bare/G_cosmo are separate symbols, untouched.

---

## 9. Contribution to common-theory closure

**Gate:** Requirement 13 (a0–vacuum relation: preserved as input or genuinely derived), gate-map cell
A03 (coefficient mechanism / kappa missing premise). The result sharpens the A03 status: the 
boundary-condition family "J(Y_ref) = 0" is the **only** static-kernel freedom available to the pinned
action besides the additive constant (k01 K1), and it fails on sign for every positive reference —
so the missing premise A03 must come from *outside* this static-kernel class (a sign-reversing
contribution, a phantom/negative-drive kernel, or a principle fixing Y_ref). It also hands a ready input
to catalog seed **AS075** (constructive missing-premise work order for kappa; prereqs AS059, AS067, AS072):
AS075 must not spend its constructive budget on positive-reference boundary conditions of the MU_n class.

**Common-action/parameter-domain compatibility:** same action class as k01 (pinned `8df5a3ab...`);
parameter cell: s-units, κ = 1/2, K_B ∈ [0, 0.25], n > 0; applicable to both footings as per §7.

---

## 10. Reproducibility

- `compute_AS068_boundary_zero_mode.py` → `raw_output.txt` (16/16 checks PASS, exit 0),
  `residuals.json`, timing/memory in `err_time.txt`: wall 0.49 s, max RSS 60.6 MiB, CPU capped
  `ulimit -t 120`, single-threaded CPython + sympy/mpmath (mpmath dps = 60).
- Lean: `lake env lean AS068_boundary_zero_mode_certificates.lean` → `lean_check.out` (exit 0).
- Source pins (verified against SOURCE_MANIFEST and the seed): PD01 `37e39d1a...`, PD08 `83f6054c...`,
  k01 `8df5a3ab...`; task `7bc8080a...`; AS067 seed `c7fd82f8...` (prerequisite, still running under
  another worker; this run uses the pinned sources directly as instructed).

## 11. Limitations

- No mechanism fixes Y_ref; no claim that some other boundary family (e.g., at negative argument, outside
  the physical Y ≥ 0 domain, or a sign-reversing kernel) fails identically — only the declared class is
  covered.
- The vacuum formula `rho_vac = (2−K_B)s²J(0)/(16πG)` inherits k01's static/FLRW construction and sign
  conventions; a different action normalization would rescale the ratio, not the sign argument.
- Not a derivation of kappa; kappa = 1/2 remains the adopted input. No dynamics, no MONO transfer, no
  criterion-B statement, no observational claim.
- Numerics at 1e-58…1e-62 are finite evidence; the exact statements rest on the symbolic identities and
  the Lean certificate.