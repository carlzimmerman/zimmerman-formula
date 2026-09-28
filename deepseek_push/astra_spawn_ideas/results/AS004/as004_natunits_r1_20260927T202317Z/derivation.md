# AS004 — Natural units and reduced Planck mass: derivation

**Run:** `as004_natunits_r1_20260927T202317Z`
**Task:** `deepseek_push/astra_spawn_ideas/AS004_natural_units_and_reduced_planck_mass.md`
(task_sha256 `3a292121793d3c6cf1031a78d91be150a285b882a7c2ebdcf06ff933928647a5`)
**Branch:** CORE scale identities (no kernel, gate or filter is selected by this task; the
operative MONO/RAR/MU2/EXP distinction is untouched).
**Worker:** hermes subagent `sa-3-92aefb6d`, model `deepseek/deepseek-v4-flash-0731`
(provider openrouter), running on the Hermes runtime of the repository host.

---

## 0. Precise claim, symbol dictionary, assumptions (task step 1)

**Claim under test (named in the task, "Mathematics and principal test box"):**

> In c = ħ = 1 units define M_L⁴ = ε_L (energy density), M_Planck = G^(−1/2),
> M̄_P = (8πG)^(−1/2); then a0 = M_L²/(2 M_Planck) = M_L²/(2√(8π) M̄_P).
> These symbols must not be interchanged with an action using reduced M_P.

Restated as an exact theorem over positive reals: the framework relation
a0 = κ c √(G ρ_Lambda), κ = 1/2 **adopted** (STANDING.md rev. 9/11: κ measured
0.465 ± 0.076 / 0.551 ± 0.043, consistent with ½, **fitted, not derived**; every
derivation route in the corpus is closed) is **exactly equivalent** to

```text
SI:        a0 = (1/2) (c^3/hbar) M_L^2 / M_Planck,
           M_L^4 = hbar^3 rho_Lambda / c^3  (= hbar^3 eps_Lambda / c^5),
           M_Planck^2 = hbar c / G.
Natural:   a0_nat = M_L^2 / (2 M_Planck) = M_L^2 / (2 sqrt(8 pi) Mbar_P)
           (c = hbar = 1; a0_nat has mass dimension 1).
```

**Symbol dictionary** (all SI unless stated; G_N, G_bare, G_cosmo kept separate —
this derivation only ever uses `G`, the coupling in the declared framework identity):

| symbol | definition | units |
|---|---|---|
| a0 | vacuum acceleration scale (framework input on each footing) | m·s⁻² |
| κ | kappa = 1/2, **adopted input**, not derived here | — |
| ρ_Lambda | mass density of the vacuum | kg·m⁻³ |
| ε_Lambda | energy density, ε = ρ c² | J·m⁻³ |
| M_L | vacuum mass scale, M_L⁴ = ħ³ρ_Lambda/c³ = ħ³ε_Lambda/c⁵ | kg |
| M_Planck | Planck mass, M_Planck = √(ħc/G) (NOT reduced) | kg |
| M̄_P | reduced Planck mass, M̄_P = √(ħc/(8πG)) = M_Planck/√(8π) | kg |
| Λ | geometric cosmological constant, Λ = 8πG_E ε/c⁴; at G_E = G: Λ = 32π a0²/c⁴ | m⁻² |
| r_M | MOND radius, r_M = √(G M_b/a0) | m |
| v_flat | deep-law flat speed, v_flat⁴ = G M_b a0 | m·s⁻¹ |
| l0 | MOND length, l0 = c²/a0 (Λ l0² = 32π) | m |

**Assumptions and boundary conditions.**
1. κ = 1/2 is an input (FRAMEWORK_CONTRACT.md; task: "Treat kappa=1/2 as adopted").
2. All quantities positive; no fit to any object is performed ("no observational fit
   is requested").
3. c = 299792458 m/s, G = 6.67430e-11 m³ kg⁻¹ s⁻², ħ = 1.054571817e-34 J·s
   (task/contract numerics).
4. Two registered footings, carried separately and never conflated: canonical
   a0 = 9.3619e-11 m/s² and alternative a0 = 1.1279e-10 m/s². The alternative footing
   is an alternative density reading at the same κ = 1/2 (or, at fixed density, an
   effective κ — given explicitly in §3); it is never "the same fixed ρ and fixed κ".
5. No limiting regime is used: the identity is exact for all positive variables
   (leading neglected term: none; see §4).

**Framework inputs vs conclusions.** Inputs: κ, the two a0 footings, G, c, ħ, the
CORE relations ρ_Lambda = 4a0²/(Gc²), Λ = 32πa0²/c⁴ (coincident G), r_M, v_flat⁴.
Conclusions established here (all exact): the natural-unit identity of the task,
its SI restoration, the conversion dictionary between M_L and Λ, the √(8π) trap
exposure, the footing-rescale rule. **κ is not derived; the value of ε_Lambda is not
derived** (it is a measured/assigned vacuum density); nothing dynamical is claimed.

---

## 1. Derivation (task steps 2–3)

### 1.1 Framework base (given, not derived)

```text
a0 = kappa c sqrt(G rho_Lambda),   kappa = 1/2
rho_Lambda = 4 a0^2 / (G c^2)                  (inversion of the base)
r_M = sqrt(G M_b/a0),  v_flat^4 = G M_b a0
```

### 1.2 Energy-density form

With ε_Lambda = ρ_Lambda c²:

```text
a0 = kappa c sqrt(G rho_L) = kappa sqrt(G eps_L),                    (1)
```

since c√(Gρ) = √(G·ρc²) = √(G ε). (Sympy check S1a: exact residual 0.)

### 1.3 Natural mass scale and Planck mass (definitions)

```text
M_L^4  := hbar^3 eps_Lambda / c^5 = hbar^3 rho_Lambda / c^3        [kg^4]
M_Planck := sqrt(hbar c / G)                                        [kg]
Mbar_P   := sqrt(hbar c / (8 pi G)) = M_Planck / sqrt(8 pi)        [kg]
```

Both M_L readings (via ε or via ρ) are the same object because
ħ³ε/c⁵ = ħ³(ρc²)/c⁵ = ħ³ρ/c³ exactly (numerical round-trip residual 1.6e-51, 2.2e-51
on the two footings at 50 dps).

### 1.4 The natural-units identity (exact)

```text
(kappa (c^3/hbar) M_L^2 / M_Planck)^2
  = kappa^2 (c^6/hbar^2) (M_L^4) (1/M_Planck^2)
  = kappa^2 (c^6/hbar^2) (hbar^3 eps_L/c^5) (G/(hbar c))
  = kappa^2 G eps_L,
```

every exponent cancelling exactly (c⁶⁻⁵⁻¹ ħ³⁻²⁻¹ = 1). Since both sides are positive,

```text
a0 = kappa (c^3/hbar) M_L^2 / M_Planck  <=>  a0^2 = kappa^2 G eps_L,
```

and by (1) with κ = 1/2:

```text
a0 = (1/2) (c^3/hbar) M_L^2 / M_Planck            (SI-restored form),      (2)
```

which is the framework relation verbatim. Dimensions of (2): (c³/ħ) has units
m·kg⁻¹·s⁻²; M_L²/M_Planck has kg; product: m·s⁻² ✓. **Sign:** every factor is manifestly
positive; a0 > 0; there is no sign freedom (also see AS021 scope).

### 1.5 Natural units (c = ħ = 1)

Setting c = ħ = 1 in (2) (or directly in (1) with [G] = M⁻², [ε] = M⁴):

```text
a0_nat = M_L^2 / (2 M_Planck),   M_Planck = G^(-1/2),   M_L^4 = eps_L.     (3)
```

Dimension check in natural units: [a0] = L/T² = M (since L = M⁻¹, T = M⁻¹) and
[M_L²/M_Planck] = M·M... M_L²/M_Planck = M²/M = M ✓. Because
M_Planck = √(8π) M̄_P:

```text
a0_nat = M_L^2 / (2 sqrt(8 pi) Mbar_P).                                  (4)
```

Both halves of the task's displayed identity are therefore exact, and each
coefficient (the 2 from κ = 1/2, the √(8π) from the Planck-mass convention) is
tracked. This is the "gravitational seesaw" with an exact 2 quoted in README.md —
reproduced here as an identity, not as a derivation of κ.

### 1.6 Conversion dictionary: vacuum mass scale vs geometric Λ

```text
eps_Lambda <-> M_L:   eps_Lambda = M_L^4 c^5 / hbar^3
rho_Lambda <-> M_L:   rho_Lambda = M_L^4 c^3 / hbar^3
a0       <-> M_L:     a0 = (1/2)(c^3/hbar) M_L^2 / M_Planck
M_L      <-> Lambda:  Lambda = 8 pi G_E eps_Lambda / c^4
                      = 8 pi G_E c M_L^4 / hbar^3
                      = 32 pi (G_E / G) a0^2 / c^4     (at kappa = 1/2)
```

The last line carries the G_E/G_N ratio explicitly (FRAMEWORK_CONTRACT: Λ_eff is a
matching condition on the candidate, not permission to set distinct couplings
equal). When the Einstein and scale couplings coincide (G_E = G, the clause stated
in the contract), Λ = 32πa0²/c⁴ and a0 = c²√(Λ/32π) — normalization check S1e/N6.

**Distinction:** M_L is the *dynamical* scale of the acceleration relation (it sits
inside a0, hence inside r_M and v_flat); Λ is the *geometric* curvature scale of the
vacuum background. They are related by the dictionary but are different objects with
different units (kg vs m⁻²); the identity between them holds only through ε_Lambda
and only at the coincident-G clause.

---

## 2. Both scale footings (task requirement, carried separately)

κ = 1/2 is held fixed in both footings; the alternative footing changes the density.

| quantity | canonical (a0 = 9.3619e-11) | alternative (a0 = 1.1279e-10) |
|---|---|---|
| ρ_Lambda | 5.844412454e-27 kg·m⁻³ | 8.48308962e-27 kg·m⁻³ |
| ε_Lambda | 5.25269596e-10 J·m⁻³ | 7.624220727e-10 J·m⁻³ |
| M_L | 3.993712594e-39 kg = 2.2403085e-12 GeV = 2.2403 meV | 4.383591813e-39 kg = 2.4590147e-12 GeV = 2.4590 meV |
| M_Planck | 2.176434342e-8 kg (= 1.2208901e19 GeV) | same |
| M̄_P | 4.341358398e-9 kg | same |
| a0_nat | 2.055460153e-43 GeV | — |
| Λ (coincident G) | 1.090799763e-52 m⁻² | 1.583281848e-52 m⁻² |
| r_dS = √(3/Λ) | 5.374494e9 pc = 1.658395e26 m | 4.460987e9 pc = 1.376517e26 m |

(M_L ≈ 2.3 meV on the canonical footing is the standard vacuum-energy scale,
consistent with M_Planck = 1.2209e19 GeV and a0_nat ≈ 2.06e-43 GeV.)

**Dimensionless controls:**
- At fixed κ: ε_alt/ε_can = (a0_alt/a0_can)² = 1.204776808² = 1.4514871574
  (residual < 1e-45) and M_L_alt/M_L_can = (a0_alt/a0_can)^(1/2) = 1.097623254.
  Certified in Lean as `footing_rescale`.
- At fixed density (informational, not the registered footing): the same relation
  re-read for κ gives κ_eff = (1/2)(a0_alt/a0_can) = 0.602388404063. The framework
  contract's "cannot share both fixed vacuum density and fixed kappa" is satisfied:
  either κ = 1/2 with ε_alt = 1.4515 ε_can, or ε fixed with κ_eff = 0.6024; never
  both at once.

---

## 3. Intermediate algebra, units, signs (task step 3, continuation)

Every step of §1.4 was also verified symbolically (sympy, exact simplification to 0):
- S1a: a0 = κ√(Gε) with ε = ρc²; residual 0.
- S1b: a0 = κ(c³/ħ)M_L²/M_Planck, M_L⁴ = ħ³ε/c⁵, M_Planck² = ħc/G — unsquared and
  squared symbolic residuals both exactly 0.
- S1c: natural-unit reduction (c = ħ = 1), residual 0.
- S1d: M̄_P substitution mismatch, factor √(8π), residual 0.
- S1e: Λ = 8πGε/c⁴ = 32πa0²/c⁴ at κ = 1/2, residual 0.

**Limiting-regime obligation.** The identity (2)–(4) is exact algebra over positive
reals — there is no expansion, no limiting regime, and therefore no leading
neglected term. Domain: all positive (c, ħ, G, ρ, M_b). The only truncations in the
numerical witnesses are the finite digit counts of the input constants (a0 given to
5 significant figures; G, c, ħ to the digits listed above) and the 50-digit working
precision of mpmath; both are recorded, not hidden.

---

## 4. Independent check in a different representation (task step 4)

Different representation used: (i) sympy exact symbolic simplification (residual 0)
vs (ii) mpmath at 50 dps on the *inverted* construction — ρ_Lambda was computed from
a0 by ρ = 4a0²/(Gc²), M_L and M_Planck built from it, and a0 recomputed from (2)
(the substitution check "into the original equation"). Observed relative residuals
(50 dps):

| check | canonical | alternative |
|---|---|---|
| a0 back from (2) vs footing a0 | 3.3e-51 | 1.4e-51 |
| ρ round trip (4a0²/(Gc²)) | 5.9e-51 | 2.0e-51 |
| M_L⁴ ε-reading vs ρ-reading | 1.6e-51 | 2.2e-51 |
| v_flat⁴ = G M_b a0 substitution (M_b = 1e11 M_sun) | 2.5e-51 | 2.1e-51 |
| (v_flat = 187.747 km/s, r_M = 12202.0 pc) | | (v_flat = 196.698 km/s, r_M = 11116.7 pc) |
| Λ = 32πa0²/c⁴ vs 8πGε/c⁴ | 1.1e-52 | — |

These are finite-precision evaluations of *exact* identities: the symbolic residual
is 0; the numerical residual floats at ~1e-51 = the 50-dps working precision.
This distinction (exact identity vs finite numerics) is made explicitly, as the
task demands.

---

## 5. Negative controls and other falsifiable checks (task step 5 & controls)

**Control A (specified): substitute M̄_P for M_Planck without the √(8π) factor.**
The mismatch is exposed exactly: with M̄_P in (2),

```text
a0_wrong/a0 = sqrt(8 pi) = 5.013256549262...
```

(residual < 1e-45 on both footings), giving a0_wrong = 4.693360649e-10 m/s²
(canonical chain) and 5.654452062e-10 m/s² (alternative chain) — **neither equals
either registered footing** (9.3619e-11 / 1.1279e-10). The control is capable of
failing and fires: if the framework relations were internally inconsistent, the two
ratios could have come out equal; they differ by exactly √(8π), so any downstream
action that silently uses the reduced Planck mass inherits a 5.01× scale error in a0
(equivalently ×25.1 in ε at fixed κ). Certified in Lean (`reduced_planck_mismatch_sq`,
`reduced_trap_neq`).

**Control B (specified): deep and Newtonian regimes / normalization and boundary
cases.** The identity has no regimes — it is exact pointwise. The applicable
boundary checks are: (i) normalization a0 = c²√(Λ/32π) reproduces each footing
exactly (residual 1e-45 class); (ii) deep-law substitution v_flat⁴ = G M_b a0 with
a0 given by the natural-unit form (residuals above); (iii) r_M boundary value
consistent with the same a0 (values above); (iv) footing normalization:
ε ratio and M_L ratio (§2). All pass. Exactness is certified in Lean for the core
identities, so these checks are consistency witnesses, not the proof.

**Lean certificate (algebraic core).** `AS004_natural_units_certificate.lean`
(9 theorems + 1 helper): `framework_squared_iff`, `natural_units_core`,
`si_restoration`, `framework_natural_iff`, `reduced_planck_mismatch_sq`,
`reduced_trap_neq`, `footing_rescale`, `lambda_dictionary`.
Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs>.lean` — exit 0,
**zero `sorry`**, and `#print axioms` for every theorem reports exactly
{propext, Classical.choice, Quot.sound} (unfiltered; the printed list is quoted in
`lean_output.txt`). Only the real-algebra content is certified; units, the physical
kernel, action, gates and criterion B are outside the file's scope.

---

## 6. Strongest surviving statement

**Theorem (exact; positive reals; κ = 1/2 adopted input).** For each registered
footing (a0 = 9.3619e-11 and a0 = 1.1279e-10 m/s²), the framework relation
a0 = (1/2)c√(Gρ_Lambda) is the same equation as

```text
a0 = (1/2)(c^3/hbar) M_L^2 / M_Planck,   M_L^4 = hbar^3 rho_Lambda / c^3,
M_Planck^2 = hbar c / G,
```

which in c = ħ = 1 is a0_nat = M_L²/(2M_Planck) = M_L²/(2√(8π)M̄_P) with
M_L⁴ = ε_Lambda. The identity adds **no** independent fitted input (the only numbers
are the adopted κ, the assigned footings, and the constants G, c, ħ); the two
footings are the same identity at densities differing by (a0_alt/a0_can)²; and
substituting the reduced Planck mass without the √(8π) factor produces the
5.0133× mismatch that matches neither footing. **The scoped claim of AS004 — the
vacuum scale is dimensionally consistent and gives the same prediction in
equivalent variables — holds exactly.** What is not established: κ = 1/2 itself,
the magnitude of ε_Lambda, and any dynamical statement (this is a units/identity
result on the CORE branch, not an action, kernel or gate result).

---

## 7. Next unresolved implication (transfer to the full theory)

The first bridge to the operative thirteen-item target is **curve-choice and
coupling identification, not further scale algebra**: the natural-unit identity is
symbol-blind in G. To attach (2) to a common action, the action's vacuum-curvature
coupling G_E and acceleration-relation coupling G must be related (the contract's
Λ_eff = 32π(G_E/G_N)a0²/c⁴ matching condition), i.e. the G_N–G_bare–G_cosmo
identification is the pending step (seed AS014 covers precisely this; no duplicate
child is proposed). Secondary: an action-level embedding must show that the MONO
kernel's argument y = g_N/a0 entering the filtered operator S is numerically
invariant under the re-parameterization (trivially true given (2), but the
action-level statement, including the heat-filter cell, is a separate obligation
belonging to the A02/A06/A09 group). κ = 1/2 remains adopted (STANDING: fitted,
all derivation routes closed), so closure gate 13 is preserved-as-input, not
derived, by this result.

---

## 8. Files and provenance

| file | role |
|---|---|
| `as004_check.py` | runnable bounded computation (sympy exact + mpmath 50 dps) |
| `raw_output.txt` | actual output: 25 checks, all PASS, exit 0 |
| `AS004_natural_units_certificate.lean` | Lean 4 certificate (self-contained) |
| `lean_output.txt` | actual `lake env lean` output: exit 0, axioms printed |
| `derivation.md` | this document |
| `result.json` | RESULT_CONTRACT v2 receipt |

Source pins verified before execution (all match SOURCE_MANIFEST.json):
README.md `91a5fac4…`, FRIED_CHICKEN_SPEC.md `98d9149f…`,
DERIVATIONS.md `8da8176e…`, STANDING.md `660462eb…`; the AS004 task hash
`3a292121…` matches the dispatcher's claim reservation `claims/AS004.json`.

**Execution bounds (actually enforced):** single-process Python, 1 CPU thread,
0.075 s compute / 0.35 s wall (bound 120 s), ≪512 MB; Lean verification 4.6 s wall.
No scaling was needed; no grid was used.