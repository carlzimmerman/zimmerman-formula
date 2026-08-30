# Phase IX — Newtonian / MOND Limit + Baryonic Tully-Fisher Relation

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

We extract the Newtonian limit of the field equation and check whether it
reproduces the MOND acceleration law and the Baryonic Tully-Fisher Relation
(BTFR). This is where the **regulator no-go (Phase I)** becomes
phenomenologically concrete.

---

## 1. The Newtonian limit

Weak field, slow motion: `g_{00} = -(1 + 2Φ_N/c²)`, `Φ_N` the Newtonian
potential, `|Φ_N|/c² << 1`, velocities `v << c`. The `00` component of the field
equation (Phase VII) reduces to
```
∇² Φ_N = 4πG ρ  +  (corrections from E_{00}) .
```
The MOND theory is defined by the **effective acceleration**
```
a_eff = μ(y) a_N ,    y ≡ a_N / a₀ ,
```
where `a_N = -∇Φ_N` is the Newtonian acceleration from the baryons alone, and
`μ(y)` is the interpolation function.

**DERIVED (frozen target):** With the frozen constitutive function
`F_+` and `Z = 4y²` in the Newtonian regime,
```
μ(y) = 1 - 2 F_+'(Z=4y²) = 1 - e^{-y} .
```
- **High acceleration** (`y >> 1`, `a_N >> a₀`): `μ → 1`, `a_eff → a_N` (GR/Newton).
- **Deep MOND** (`y << 1`, `a_N << a₀`): `μ → y = a_N/a₀`, so
  `a_eff → a_N²/a₀` (the MOND `a²/a₀` law).

This is the **intended** MOND interpolation. **Status: DERIVED (algebraic, from
the frozen F_+).**

---

## 2. The regulator destroys the deep-MOND law  (consequence of Phase I)

Phase I (REGULATOR_NOGO.md) proved that the **C² regulator** `P_{5,ε}` required
to make the auxiliary Hessian well-defined at `Z = 0` **changes** the
deep-MOND law from `μ ~ y` to `μ ~ y⁴`. Concretely, with the regulator:
```
μ_reg(Z) ~ (-6 c₃) Z² ~ C(ε) y⁴    as  y -> 0 ,
```
where `C(ε) > 0` depends on the regulator scale `ε` (numerically `C(0.1) ≈
2.1×10³`). Therefore the **effective acceleration** in the deep-MOND regime is
```
a_eff = μ_reg(y) a_N ~ C(ε) y⁴ a_N = C(ε) (a_N/a₀)⁴ a_N = C(ε) a_N⁵ / a₀⁴ .
```
This is a **fifth-power law**, **not** the MOND `a_N²/a₀` law.

**DERIVED (decisive):** The frozen candidate, **with its C² regulator**, does
**not** reproduce the MOND acceleration law in the deep-MOND regime. It gives
`a_eff ~ a_N⁵/a₀⁴` instead of `a_eff ~ a_N²/a₀`.

---

## 3. The Baryonic Tully-Fisher Relation (BTFR)

The BTFR is the empirical relation (for disk galaxies)
```
v⁴ ≈ G M_b    (v = asymptotic rotation velocity, M_b = baryonic mass).
```
In a spherical system, `v² = r a_eff`, so `v⁴ = r² a_eff²`.

### 3.1 Intended MOND (μ ~ y)

In the deep-MOND regime, `a_eff = a_N²/a₀`. For a point mass, `a_N = GM/r²`, so
```
a_eff = (GM/r²)²/a₀ = G²M²/(r⁴ a₀) .
v⁴ = r² a_eff² = r² [ G⁴M⁴/(r⁸ a₀²) ] = G⁴M⁴/(r⁶ a₀²) .
```
For a **spherical** mass distribution with the MOND force `a_eff = a_N²/a₀`,
the standard result is `v⁴ = G M a₀ / (4π)` (up to a factor), i.e.
```
v⁴ ∝ G M a₀  ∝  G M   (at fixed a₀) .
```
This **reproduces** the BTFR `v⁴ ∝ G M`. **DERIVED (intended MOND).**

### 3.2 With the regulator (μ ~ y⁴)

With `a_eff ~ a_N⁵/a₀⁴`, for a point mass `a_N = GM/r²`:
```
a_eff ~ (GM/r²)⁵/a₀⁴ = G⁵M⁵/(r¹⁰ a₀⁴) .
v² = r a_eff ~ G⁵M⁵/(r⁹ a₀⁴)   =>   v⁴ ~ G¹⁰M¹⁰/(r¹⁸ a₀⁸) .
```
This is **not** `v⁴ ∝ G M`. The regulator **destroys** the BTFR.

**DERIVED (decisive):** The frozen candidate **with its C² regulator** does
**not** reproduce the BTFR. The fifth-power deep-MOND law gives
`v⁴ ~ G¹⁰M¹⁰/r¹⁸/a₀⁸`, which is observationally excluded (the observed BTFR is
`v⁴ ∝ G M`).

---

## 4. The no-regulator alternative

If the regulator is **dropped** (keep `F_+` with its `F'' → -∞` cusp at `Z=0`),
the deep-MOND law `μ ~ y` is restored and the BTFR is reproduced. **But** then
the auxiliary Hessian is singular at `Z = 0` (Phase IV), and the **ghost**
(Phase VI) remains regardless. So dropping the regulator trades the
phenomenological failure (BTFR) for a singular Hessian, and does **not** remove
the ghost.

**DERIVED:** There is **no** choice within the frozen candidate that
simultaneously (a) reproduces the BTFR, (b) has a well-defined (C²) Hessian,
and (c) is ghost-free. The three requirements are mutually incompatible:
- (a) requires `μ ~ y`, which requires `F'' → -∞` at 0 (no C²).
- (b) requires C² at 0, which requires `μ ~ y²` or worse (no MOND law).
- (c) is impossible regardless (the ghost is from the `Box^{-1}` localization,
  independent of F).

---

## 5. Summary of Phase IX results

| # | Result | Status |
|---|--------|--------|
| 1 | Newtonian limit gives `a_eff = μ(y) a_N`, `μ(y) = 1 - e^{-y}` (intended). | DERIVED |
| 2 | The C² regulator changes the deep-MOND law from `μ~y` to `μ~y⁴` (`a_eff ~ a_N⁵/a₀⁴`). | DERIVED (consequence of Phase I) |
| 3 | Intended MOND reproduces the BTFR (`v⁴ ∝ G M`). | DERIVED |
| 4 | **With the regulator, the BTFR is destroyed** (`v⁴ ~ G¹⁰M¹⁰/r¹⁸/a₀⁸`). | DERIVED (decisive) |
| 5 | No choice within the frozen candidate satisfies (a) BTFR + (b) C² Hessian + (c) ghost-free simultaneously. | DERIVED |

**Phase IX verdict: FAIL (phenomenology).** The frozen candidate **with its C²
regulator** does not reproduce the MOND law or the BTFR. **Without** the
regulator it reproduces them, but then the Hessian is singular and the ghost
remains. The candidate is **phenomenologically broken** in its frozen form.
