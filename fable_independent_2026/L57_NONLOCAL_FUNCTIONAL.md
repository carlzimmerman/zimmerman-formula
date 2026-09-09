# L57 — the nonlocal functional: the one successor L56's theorem does not cover

2026-09-09. Lane L57. Script: [`L57_nonlocal_functional.py`](L57_nonlocal_functional.py) →
[`L57_nonlocal_functional.out`](L57_nonlocal_functional.out). **35 checks, 23 PASS / 12 FAIL; all 13
controls PASS.** Both a₀ footings (9.3619e-11 / 1.1279e-10 m s⁻²) on every dimensional number. 43 s.

Method: nothing under `closure_2026/` or the lead agent's directories was imported, executed or copied.
The symbolic algebra — the linearised Ricci tensor from first-order Christoffels, the Euler–Lagrange
variation on the ten components of a general static `h_μν`, the elliptic kernel tower and its exact
normalisation — was built here in sympy. The cluster, group and galaxy data were read directly from the
on-disk public archives (X-COP FITS, Herbonnet 2020 Tables 2–3, SPARC rotmod, Lovisari et al. 2015).
**L51's and L56's load-bearing numbers are re-derived as controls, not inherited**, including L56's
convention-free crux, which is the number this lane had to beat.

---

## The verdict, first

**The successor works as a mechanism, and that is a real result: it does make the host/substructure
distinction L56 proved no local field can make. It then fails to be a *prediction*, and it does not cure
the failure it was built for.** Three things have to be kept apart.

1. **It works.** A weight on the baryon density *smoothed on a length ℓ* suppresses a compact source's
   contribution to the trigger by the **cube of the scale ratio**. Against L56's `R_emb = M_P/M_fw =
   0.803 / 0.666`, it reaches **2.4e-4** at a galaxy probe radius of 100 kpc — a factor **3.3e3** better.
   Cassini and the wide binaries are safe by **15–25 orders of magnitude** with *no steepness assumed
   anywhere*, so **L56's pincer — in which Cassini capped the amplitude from below — is broken**. And the
   weight it needs is **gentler than chameleon screening** (`p_local = 0.60–0.68`) where L51 needed 6.5–16
   and L56 needed 5.4–22.
2. **It does not reach the theory's own number.** The suppression has a **floor**, `S ≳ (R_p/r_cl)³`,
   which no kernel order and no length beats. At the radii where a galaxy's lensing and dynamical masses
   are both measured (`R_max ≈ 100 kpc`) that floor is **2.4e-4, i.e. 2.4× the deposited theory's own
   `Φ = Ψ` to 1e-4** — and 66× at 300 kpc. It clears a generous **20% empirical** bound at every probe
   radius carried; it does not clear the theory's own.
3. **The length is fitted, not predicted.** The mechanism needs **ℓ_rms ≥ 600 kpc** (2 Mpc on the worst
   realisable kernel) against the theory's own coherence length **ξ = 4.00 pc** (L47, outside-J
   placement) — a factor **1.5e5**. The closest fixed candidate among the theory's own constants is
   **3.0 dex away**. *A tuned length fitted to five clusters is not a mechanism, and this is a tuned
   length fitted to five clusters.*

**And even at its ceiling it halves the failure rather than curing it: 8.8 → 4.9σ / 9.0 → 4.7σ** — which
is exactly L51's ceiling, set by the lensing-versus-dynamics budget, *not* by anything this mechanism
does. The new mechanism removes the constraint that emptied L56's window; it does not raise the ceiling.

**So L56's theorem does NOT become unconditional.** It stands exactly as written — it closes every single
*local* trigger, and it named this successor precisely. The successor survives, conditionally.

---

## 1. Controls (A1–A7, B1, B4, C0, C1, C3, C7a, D1, F1 — thirteen, all PASS)

| control | L51 / L56 | here |
|---|---|---|
| A1 projection machinery vs analytic NFW | Σ 1.2e-6, ΔΣ 2.2e-6 | **1.23e-6 / 2.15e-6** |
| A2 the 9σ shear-shape failure | +0.516 ± 0.058 / +0.521 ± 0.058 | **identical, 8.8σ / 9.0σ** |
| A3 measured cluster `g_lens/g_dyn` | 1.148 ± 0.146 | **1.148 ± 0.146** |
| A4 **L56's convention-free crux** `R_emb = M_P/M_fw` | 0.806 / 0.669 | **0.803 / 0.666** |
| A5 L51's 3σ-budget ceiling | 8.8 → 4.9 at f ≤ 0.73; 9.0 → 4.7 at f ≤ 0.88 | **identical, f = 0.72 / 0.88** |
| A6 the elliptic kernel tower, normalised symbolically | — | `∫K_n d³r = 1`, n = 1…6 |
| A7 the spherical smoothing machinery | — | uniform fixed point 1.2e-5, point source 1.6e-6, mass 4e-3 |
| C0 the master formula reduces to L56 | — | `\|dΦ/dr / g − 1\| ≤ 3.1e-4` (grid) |
| D1 L51's operator split | frame-free carries the slip, u-built the lensing | **identical** |
| F1 gate 1 alone reproduces L51's answer | 4.9 / 4.7σ | **4.9 / 4.7σ** |

---

## 2. Which nonlocal quantities are admissible — settled before any fitting (B1–B6)

**A nonlocal DEPTH trigger is dead, on two independent grounds, and was not built here.**

- **B1 (control).** L56's obstruction reproduces: a constant deepening of `Φ` is an **exact isometry**
  (a rescaling of `t`), so no functional of the metric — *local or nonlocal, at any order* — can measure a
  depth.
- **B2 FAIL.** Nor does the clock-carried depth `X = 1 − Q/Q₀` escape by being smoothed: **smoothing is a
  linear operation and commutes with superposition exactly** (additivity error 2.2e-16), so
  `⟨X_host + X_sub⟩ = ⟨X_host⟩ + ⟨X_sub⟩` and L56 B5 is inherited unchanged.

**What survives:**

| candidate | depth-blind | uniform-field-blind | verdict |
|---|---|---|---|
| `⟨Φ⟩_ℓ` smoothed depth | NO | NO | **excluded** (B1, B2) |
| `⟨\|∇Φ\|⟩_ℓ` smoothed acceleration | YES | NO | admissible, then killed by B5 |
| `⟨∇²Φ⟩_ℓ` smoothed density / Ricci | YES | YES | **the survivor** |
| `⟨(∂_i∂_jΦ)²⟩_ℓ` smoothed tidal invariant | YES | YES | admissible (same family) |

- **B5 FAIL, and it eliminates two of the three survivors.** By **Newton's theorem** the smoothed source's
  enclosed mass — and hence its potential and its acceleration — returns to the unsmoothed value **within
  5% by r = 5 ℓ_rms for every kernel tested**. A potential- or acceleration-triggered weight is therefore
  *exactly blind to the smoothing* outside ℓ. **Only the smoothed density is suppressed at every radius**,
  and that single fact selects the trigger the rest of the lane tests.
- **B4 PASS, a positive.** A spatial smoothing is not definable without a slicing, and the theory's clock
  supplies one that is reparametrisation-invariant (`τ → f(τ)` leaves `n_μ` unchanged). **A frame-free
  theory cannot write any spatial nonlocal functional at all** — this successor exists only because the
  clock does. That is the same shape of positive L56 recorded at its B4.
- **B6 PASS, with a named cost.** The **elliptic** operator `(1 − ℓ²D²)^{-n}` on the clock's slices adds
  **no pole and therefore no propagating mode** (denominator `1 + ℓ²k² > 0` for every real spatial `k`);
  the covariant `(1 − ℓ²□)^{-1}` adds a pole at `ω² = k² − 1/ℓ²` and is excluded. **The price is that the
  smoothing is instantaneous in the preferred frame** — the same cost the programme's York/CMC branch was
  closed on.

---

## 3. The master formula, and what the whole lane reduces to (C0)

Let `s = W(U)` for **any** trigger, local or nonlocal. Two facts fix everything.

1. **The cluster fixes `W′` pointwise:** `W′(U_cl) = (ds_req/dr)/(dU/dr)|_cl`.
2. **A slip is observable only through its gradient** — a constant `s` shifts `Φ` and `Ψ` by equal and
   opposite constants and moves neither dynamics nor lensing.

    R_emb  =  (M_P/M_fw)  ×  S ,        S  =  ratio_obj / ratio_cl ,       ratio(X) = |dU/dr| / g

**L56 is the `S = 1` corner.** For the local depth trigger `dU/dr = −g/c²` for *every* object, so
`ratio ≡ 1/c²` identically — which is exactly why L56's response was object-independent and equal to
`M_P/M_fw` with no convention entering. **S is the only thing a nonlocal trigger can buy.**

**And note what drops out.** Because only gradients are observable, there is **no requirement that the
trigger values of clusters and galaxies fail to overlap**. L51's C9 overlap argument and L56's non-overlap
bookkeeping are both *vacuous* for a nonlocal trigger. That is a structural gain, recorded as one.

**C1 (control).** `S` is a property of the two **scales**, not of the object: ten times the galaxy mass
changes it by **0.00%**, twice the disc scale radius by **0.1%**. The mass cancels exactly between the
trigger and the acceleration.

---

## 4. S(ℓ), measured, and the floor (C2–C5)

`R_emb = (M_P/M_fw) × S`, canonical footing, galaxy probe radius `R_max = 100 kpc`. Lengths are the
kernel's **rms radius**, so kernels are compared at equal physical smoothing scale. `n` is the order of
the elliptic operator `(1 − ℓ²D²)^{-n}`; `gauss` is `e^{ℓ²D²/2}`, **not realisable by any finite-order
local operator** and carried only as the most generous member.

| ℓ_rms [kpc] | gauss | n1 | n2 | n3 | n4 | n6 |
|---|---|---|---|---|---|---|
| 100 | 7.1e+1 | 1.7e+2 | 8.2e+1 | 7.7e+1 | 7.5e+1 | 7.3e+1 |
| 300 | 1.2e+0 | 1.9e+1 | 7.9e+0 | 4.8e+0 | 3.5e+0 | 2.4e+0 |
| 600 | 4.3e-2 | 5.1e+0 | 9.1e-1 | 3.1e-1 | 1.7e-1 | 1.0e-1 |
| 1000 | 5.5e-3 | 2.4e+0 | 2.1e-1 | 4.7e-2 | **2.3e-2** | 1.3e-2 |
| 3000 | 5.9e-4 | 1.1e+0 | 2.5e-2 | 2.8e-3 | 1.4e-3 | 9.1e-4 |
| 30000 | **2.4e-4** | 8.2e-1 | 5.9e-3 | 3.4e-4 | 2.6e-4 | 2.5e-4 |

**C3 — THE FLOOR, and it is a theorem, not a number.** Once ℓ exceeds both scales, every kernel factor
cancels and `S → (R_p/r_cl)^q × M_b(<r_cl)/M_b(<ball)`, with `q` fixed by the kernel at the origin,
`K′(r) ~ r^{q−2}`. A6 established symbolically that

    n = 1:  K'(r) ~ -m^2/(4 pi r^2)   =>  q = 0   -- NO discrimination at all
    n = 2:  K'(r) ~ -m^4/(8 pi)       =>  q = 2
    n >= 3: K'(r) ~ -m^5 r / (c_n pi) =>  q = 3   -- and the GAUSSIAN, the n -> infinity member, is q = 3 too

The measured floor reproduces those exponents to **3.9%**:

| kernel | q | S(100)/S(30) | (10/3)^q | S(300)/S(100) | 3^q |
|---|---|---|---|---|---|
| gauss | 3 | 36.28 | 37.04 | 27.00 | 27.00 |
| n1 | 0 | 1.00 | 1.00 | 1.00 | 1.00 |
| n2 | 2 | 11.54 | 11.11 | 8.85 | 9.00 |
| n4 | 3 | 36.27 | 37.04 | 26.97 | 27.00 |

**So the maximum host/substructure discrimination any smoothing can achieve is the CUBE of the scale
ratio. Higher order buys nothing beyond q = 3, and neither does a longer length.**

- **C4 PASS.** The distinction is real: a factor **122 – 1.2e5**, entirely by scale.
- **C5a FAIL.** At the full repair amplitude, `R_emb = 2.4e-4` at `R_max = 100 kpc` — **2.4×** the theory's
  own 1e-4, **66×** at 300 kpc. **The verdict flips at `R_max ≈ 50 kpc`**: inside that radius the theory
  gate is met, outside it is not. That dependence is the crux and is stated rather than buried.
- **C5b PASS.** The 20% empirical gate is cleared at **every** probe radius from 30 to 300 kpc, on both
  footings. This is the first mechanism in this programme to clear the embedded-galaxy gate at all.
- **C6 FAIL.** The smallest length meeting even the empirical gate is **ℓ_rms = 600 kpc**, comparable to or
  larger than the 0.5–2 Mpc shell where the repair is required. **The smoothing that hides a galaxy is not
  much smaller than the object it must not hide.**
- **C7a PASS.** The smoothed trigger is **monotone** across 0.5–2 Mpc and the required `W` is
  **increasing** in density on every kernel, length and footing — so a single-valued `W` exists, it is off
  in the field and off in the cosmological background (which every normalised kernel leaves *exactly*
  where it is, A7). **L6's cosmological-ordering kill therefore does not apply here.**
- **C7b PASS, a positive.** `p_local = 0.60–0.68` at the length the gate requires, against 1–3 for
  chameleon and symmetron and 5.4–22.4 for L56's depth trigger. The trade is explicit and printed: longer
  smoothing flattens the trigger across the cluster and steepens the weight, reaching `p_local = 7.5` at
  3 Mpc.

---

## 5. The two lengths (D1–D4)

- **D2 PASS — the escape the brief named survives.** The slip weight multiplies the **frame-free**
  curvature scalar (D1: it sources the traceless `ij` equation) while `ξ` is a property of the **MOND
  scalar's** gradient term (`J(Y + ξ²|∇⊥V|²)` in THE_ACTION §1 and PAPER8 eq. 1). Different operators;
  nothing ties their coefficients, let alone their lengths. **The two lengths can differ.**
- **D3 FAIL — and if they could not, the lane would be dead in one line.** L47's exact cone law
  `M_ph(<r)/M = r²/(2ξ²)` at `ξ = 600 kpc` gives a phantom-to-baryon ratio of **5.6e-4** at 20 kpc against
  the **1.19** the kernel itself requires — short by **2.1e3**. Galactic MOND would not survive.
- **D4 FAIL — the theory has no room for the length.** **Placement stated:** the primary `ξ` is the
  **outside-J** value, **4.00 pc**, because that is the one L47 obtains from an exact solve of the action's
  own scalar equation with a symbolically verified Green's function, identical on both footings; the
  inside-J value, 585/642 pc, is an asymptotic balance and is carried as the alternative. Neither is close.

| candidate | length | dex from the required ≥ 600 kpc |
|---|---|---|
| ξ, outside-J (L47 exact solve, both footings) | 4.00 pc | **−5.18** |
| ξ, inside-J (L47 asymptotic balance) | 585 pc | **−3.01** |
| ξ, standing PAPER8 value | 0.10 pc | −6.78 |
| c/H₀ | 4.45 Gpc | +3.87 |
| c²/a₀ (L17's unique filter length) | 31.1 Gpc | +4.71 |
| √(GM_b/a₀), the cluster MOND radius | 440 kpc | −0.13, **but mass-dependent** |
| a₀/(Gρ̄_b) | 109 Gpc | +5.26 |

The one candidate of roughly the right size is **mass-dependent** and therefore not a kernel length at
all — L17's own objection, that no single operator length serves a range of masses.

---

## 6. Pricing the length (E1–E5)

**Honesty note carried in the script:** the cluster data fix `W′(U)` only over the cluster's own range of
`U`. Below it `W` is a free function. Every number here is quoted at the reference value `W′(U_cl)` and
scales linearly with `W′(U_sys)/W′(U_cl)`, which is unknown and is **not** assumed ≤ 1. Where the margin
is many orders, the conclusion is robust; where it is a factor of a few, it is not, and the lane says so.

| system | probe radius | reference response | verdict |
|---|---|---|---|
| Cassini, Saturn's orbit | 9.58 AU | **2.5e-30** | **PASS by 9.3e24** |
| a wide binary | 10 kAU | **2.8e-21** | **PASS by 8.2e15** |
| a globular cluster | 10 pc | 2.5e-14 | safe |
| the Milky Way's own slip | 8.2 kpc | 1.4e-5 | safe |
| SPARC discs (155, own masses and sizes) | ≤ 300 kpc | 8.4e-7 – **3.6e-1**, median 1.2e-3 | 153/155 clear 20% |
| X-ray groups (20, Lovisari 2015) | R500 | 2.1e-1 – **4.5e-1**, median 3.1e-1 | **the prediction** |

- **E1 PASS, and it is the second real positive.** The suppression is geometric and needs **no steepness**,
  so **L56 E3's pincer is lifted**: Cassini no longer caps the amplitude from below, and the window is no
  longer empty for that reason.
- **E2 FAIL, not independent of C5a.** The largest values belong to the physically largest discs probed to
  300 kpc — exactly as `(R_p/r_cl)³` says they must. At ℓ_rms = 1 Mpc the empirical gate holds to about
  150 kpc; reaching 300 kpc needs ℓ_rms ≥ 2 Mpc.
- **E3 FAIL, and it is the mechanism working as designed.** Groups are **extended** against the smoothing,
  so the mechanism does not hide them: it predicts a group-scale lensing-versus-hydrostatic discrepancy of
  **20–45%**. **Whether that is excluded is NOT decided here** — this repository's own group estimators
  disagree by more than the effect (KT2017 vs g06, +0.42 dex on 19 shared hosts), so the channel is
  estimator-limited and the lane refuses to score it in either direction.
- **E4 FAIL = NOT DECIDED, and it is the measurement that would settle the door.** A nonlocal trigger *is*
  an external-field effect on the slip: at ℓ_rms = 1 Mpc a cluster sits **104×** above an isolated
  10¹¹ M⊙ galaxy in the trigger, which sits 10× above the cosmic mean. The mechanism therefore predicts a
  lensing-versus-dynamical discrepancy of **0.024% – 2.3% for galaxies at cluster radii and essentially
  none for the same galaxies in the field**. Nothing measures that today.
- **E5 PASS as a reference number only.** A perturbation longer than ℓ is not smoothed, so the slip is not
  suppressed there: **0.3% on 10 Mpc**, reported as an open channel with a named calculation (a Limber
  cosmic-shear forecast with the pinned `W`), **not** as a kill and **not** as a pass.

---

## 7. The run — the improvement as a curve (F1–F3)

Four constraints act on the amplitude `f` of the added lensing phantom, and **only one of them binds**:

    (1) the lensing-to-dynamics ratio (1.148 +/- 0.146 vs the theory's 1.000)  caps f from ABOVE
    (2) the embedded-galaxy consistency  R_emb = f x (M_P/M_fw) x S            caps f from ABOVE
    (3) CASSINI -- which emptied L56's window from BELOW --                    does NOT cap f at all
    (4) the isolated-galaxy gate                                              implied by (2)

| f | shape σ | lens/dyn σ | R_emb at the floor | R_emb n4, 2 Mpc | R_emb n4, 1 Mpc |
|---|---|---|---|---|---|
| 1.3e-2 | 8.62 | 0.94 | 3.1e-6 | 3.9e-5 | 2.8e-4 |
| 1.4e-1 | 7.10 | 0.24 | 3.4e-5 | 4.3e-4 | 3.2e-3 |
| 4.6e-1 | 5.48 | 1.51 | 1.1e-4 | 1.4e-3 | 1.0e-2 |
| 7.8e-1 | 4.78 | 3.27 | 1.9e-4 | 2.4e-3 | 1.8e-2 |
| 1.0e0 | 0.00 | 4.48 | 2.4e-4 | 3.1e-3 | 2.3e-2 |

**The ceilings, at `R_max = 100 kpc`:**

| constraint set | canonical | alt |
|---|---|---|
| gates 1+2 only — L51's own question | f ≤ 0.72 → **8.8 → 4.9σ** | f ≤ 0.88 → **9.0 → 4.7σ** |
| **+ embedded, empirical 20% (any realisable kernel, ℓ ≥ 1–2 Mpc)** | f ≤ 0.72 → **4.9σ** | f ≤ 0.88 → **4.7σ** |
| + embedded, theory 1e-4, Gaussian floor at ℓ = 30 Mpc | f ≤ 0.40 → 5.7σ | f ≤ 0.48 → 5.5σ |
| + embedded, theory 1e-4, n4 at ℓ = 2 Mpc | f ≤ 0.03 → 8.4σ | f ≤ 0.03 → 8.5σ |
| + embedded, theory 1e-4, n4 at ℓ = 1 Mpc | **nothing → 8.8σ** | **nothing → 8.9σ** |

**F2 FAIL, and the reason is not the new mechanism.** On the empirical arm the *full* L51 ceiling is
available — the embedded gate no longer binds and Cassini never did — but the lensing-versus-dynamics
budget alone still caps the phantom, so **the shape failure is halved, not cured**. On the theory's own
arm the best is 5.7σ, and only with a Gaussian at 30 Mpc, which is neither realisable by a finite-order
operator nor smaller than the objects it is meant to select.

**F3 FAIL — the price.** What is added: (i) a free function `W` of a new variable; (ii) a length
`ℓ_rms ≥ 600 kpc` supplied by nothing in the theory; (iii) the integer order `n ≥ 3` (n = 1 buys nothing,
n = 2 only the square); (iv) an instantaneous nonlocality on the clock's slices. What it is fitted to:
**five cluster shear log-slopes and one lensing-to-dynamics ratio.**

---

## 8. What this changes in the standing record

1. **L56's theorem is untouched and does NOT become unconditional.** It closes every single *local*
   trigger and it named this successor precisely. The successor survives — conditionally.
2. **Quote L56 B1 in its strongest form and add the corollary this lane found.** A constant deepening is
   an exact isometry, so a nonlocal *depth* trigger is dead; and because smoothing is linear, the
   clock-carried depth does not escape by being smoothed either. **The admissible nonlocal object is the
   smoothed CURVATURE (density or tidal invariant), and nothing else**: Newton's theorem makes the
   smoothing exactly invisible to a smoothed potential or acceleration outside ℓ.
3. **L51's overlap argument and L56's non-overlap bookkeeping are vacuous for a nonlocal trigger.** Only
   gradients are observable, so the populations may overlap freely in the trigger. The right object is the
   gradient ratio `S`, and `R_emb = (M_P/M_fw) × S` is the general form of which L56's crux is the `S = 1`
   corner.
4. **A new convention-free number for the next proposal.** `S ≥ (R_p/r_cl)³` — the best host/substructure
   discrimination any smoothing of any order and any length can achieve. Any mechanism that repairs the
   cluster shear shape by a metric slip and hides itself by scale pays at least
   `(M_P/M_fw)(R_p/r_cl)³ = 2.4e-4` at 100 kpc.
5. **The cluster weak-lensing shape now has exactly one named live mechanism** — a slip weighted by the
   baryon density smoothed on 1–2 Mpc — **live only in the sense that nothing measured excludes it.** Its
   length is fitted, its operator order is fitted, its weight is a free function, and at its ceiling it
   repairs half of the 9σ.
6. **Two decisive measurements are named**, in order: the lensing-versus-dynamical mass of galaxies
   *inside* clusters to 0.1% (predicted 0.02–2%, against essentially zero for the same galaxies in the
   field — an environmental contrast nothing else in this programme predicts); and group lensing versus
   hydrostatic masses to better than 20% (predicted 20–45%, presently estimator-limited in this
   repository by more than the effect).

---

## 9. Honesty ledger, in both directions

- **Three findings run FOR the door and are recorded as such:** the host/substructure distinction is real
  and worth a factor 122–1.2e5 (C4); Cassini's from-below cap, which emptied L56's window, is lifted (E1);
  and the required weight is *gentler* than chameleon screening, where L51 and L56 both needed steep ones
  (C7b).
- **Two approximations run AGAINST the door and are named:** the cluster's surroundings beyond 3 R200 are
  replaced by the cosmic mean, which understates the mass a large smoothing ball sees and therefore
  **understates the floor**; and the embedded galaxy's internal field carries the angle-averaged
  external-field boost rather than the smaller radial one, which **understates S**.
- **The five-cluster scatter of the required weight is not used anywhere, in either direction.** L51 C13b
  showed it is noise-limited (fractional error 1.41) and this lane inherits the refusal, not the number.
  Every kill and every pass above rests on an amplitude or on a scaling law.
- **The length was not fitted to the shear data and then quoted as a success.** It was derived from the
  gate it has to pass, then priced against everything else, and the price is recorded as a cost. **A tuned
  length fitted to five clusters is not a mechanism, and this lane says so about its own result.**
- **Three numbers are reported as undecided rather than scored:** the group prediction (E3, estimator-
  limited by more than the effect), the environmental prediction (E4, unmeasured), and the cosmological
  slip (E5, a reference value that depends on a free continuation of `W`).
- **No statement anywhere that data favour this framework over ΛCDM.** The halo, its NFW profile and its
  concentration relation are ΛCDM's, imported.

---

## 10. The PASS/FAIL lines

```
[PASS] A1 [control] the projection machinery reproduces the analytic NFW Sigma and DeltaSigma to 0.5%   (max |Sigma err| 1.23e-06, max |DeltaSigma err| 2.15e-06)
[PASS] A2 [control] the 9-sigma cluster shear-shape failure is reproduced independently (L51 C2 / L56 A3: +0.516 +/- 0.058 / +0.521 +/- 0.058)   (canonical +0.516 +/- 0.058 (8.8 sigma), alt +0.521 +/- 0.058 (9.0 sigma))
[PASS] A3 [control] the measured cluster lensing/dynamical mass ratio is reproduced   (1.148 +/- 0.146)
[PASS] A4 [control] L56's convention-free crux reproduces: the embedded response fixed by pointwise matching is M_P/M_fw = 0.806 (canonical) / 0.669 (alt)   (canonical 0.803, alt 0.666, i.e. 6.7e+03 - 8.0e+03 x the theory's own 1e-4 and 3.33 - 4.01 x a 20% bound)
[PASS] A5 [control] L51's ceiling reproduces: inside the 3-sigma lensing/dynamics budget the freedom takes the shape residual from 8.8 to 4.9 sigma (canonical) / 9.0 to 4.7 (alt)   (canonical 8.8 -> 4.9 sigma at f = 0.72, alt 9.0 -> 4.7 sigma at f = 0.88)
[PASS] A6 [control] the realisable elliptic kernel tower is generated and normalised exactly, and its small-source behaviour is fixed: K_n'(r) is linear in r for every n >= 3 (as for a Gaussian), a nonzero CONSTANT for n = 2, and divergent as 1/r^2 for n = 1
[PASS] A7 [control] the spherical smoothing machinery is exact: a uniform density is a fixed point of every kernel, a compact source returns M K(r), and mass is conserved   (worst uniform error 1.22e-05, worst point-source error 1.60e-06, worst mass error 4.07e-03)
[PASS] B1 [control] L56's exact-isometry obstruction reproduces: a constant deepening of the potential is an exact diffeomorphism, so NO functional of the metric -- local or nonlocal, at any order -- can measure a depth
[FAIL] B2 [test] smoothing the clock-carried DEPTH X = 1 - Q/Q0 escapes L56 B5 -- i.e. a smoothed depth can be referenced to the host rather than to the total   (NO -- smoothing is a linear operation and commutes with superposition exactly (additivity error 2.2e-16) ... A nonlocal DEPTH trigger inherits L56 B5 unchanged and is excluded on TWO independent grounds.  This lane does not build one)
[PASS] B3 [test] the admissible nonlocal quantities are exactly the smoothed CURVATURES (density and tidal invariant) and the smoothed ACCELERATION; the smoothed DEPTH is not admissible
[PASS] B4 [control] the theory's clock supplies the slicing a spatial smoothing needs, and it is reparametrisation-invariant (tau -> f(tau) leaves n_mu unchanged for f' > 0)
[FAIL] B5 [test] a smoothed POTENTIAL or ACCELERATION trigger suppresses a compact source at the radii where galaxy lensing and dynamics are compared   (NO -- by Newton's theorem ... within 5% by r = 5 l_rms for every kernel tested.  ONLY the smoothed DENSITY is suppressed at every radius.  That single fact selects the trigger this lane then tests)
[PASS] B6 [test] the smoothing can be made covariant without adding a propagating mode   (YES, but only in one realisation: the ELLIPTIC operator on the clock's own slices adds no pole ... The price is that the smoothing is INSTANTANEOUS in the preferred frame)
[PASS] C0 [control] the master formula reduces to L56 exactly: for the LOCAL DEPTH trigger the gradient per unit acceleration is 1 for every object, so S = 1 identically and R_emb = M_P/M_fw
[PASS] C1 [control] S is a property of the two SCALES, not of the galaxy: the trigger gradient per unit of the object's own acceleration is independent of the object's mass and insensitive to its size   (mass x10 changes it by 0.00%, size x2 by 0.1%)
[PASS] C3 [control] the floor law S_min ~ (R_p/r_cl)^q with q = 0, 2, 3 for n = 1, n = 2 and every n >= 3 (Gaussian included) reproduces the measured floor's scaling with the probe radius to 5%   (worst exponent error 3.9%)
[PASS] C4 [test] a nonlocal (smoothed) trigger makes the host/substructure distinction that L56 proved no local field can make   (YES -- it buys a factor 122 - 119140 on the embedded response, entirely by SCALE)
[FAIL] C5a [test] at the FULL repair amplitude the smoothed trigger preserves the deposited theory's OWN no-slip result (1e-4) on the galaxies that sit at cluster radii (R_max = 100 kpc)   (NO -- best achievable 2.44e-04, i.e. 2.4 x the bound.  The FLOOR is (R_p/r_cl)^3 x M_P/M_fw and no kernel order and no length beats it.  The verdict FLIPS at R_max = 50 kpc)
[PASS] C5b [test] the smoothed trigger passes a generous EMPIRICAL galaxy-lensing tolerance of 20% fractional slip, at every probe radius carried   (YES at every R_max from 30 to 300 kpc and on both footings)
[FAIL] C6 [test] the required smoothing length is smaller than the cluster radii the repair is required at (0.5-2 Mpc)   (NO -- the smallest length meeting even the generous empirical gate is l_rms = 600 kpc)
[PASS] C7a [control] the smoothed trigger is monotone across 0.5-2 Mpc and the required weight has the sign a workable mechanism needs -- W INCREASING with the smoothed density   (so the cosmological-ordering objection that closed L6's screened force does NOT apply here)
[PASS] C7b [test] the weight the mechanism needs is as gentle as chameleon/symmetron screening (logarithmic slope <= 3) at the length the gate it can meet actually requires   (YES: p_local = 0.60 - 0.68, where L51 needed 6.5-16.0 and L56 needed 5.4-22.4)
[PASS] D1 [control] L51's operator split reproduces: the frame-free term sources the traceless ij equation and therefore carries the SLIP; the u-built term sources only the 00 equation
[PASS] D2 [test] the trigger's length is free to differ from the kernel's coherence length xi   (YES -- they multiply different operators.  What it costs is a SECOND independent length in the same sector)
[FAIL] D3 [test] if the action DID force l = xi, galactic MOND would survive at the length PART C needs   (NO -- at xi = 600 kpc the cone law gives 5.56e-04 at 20 kpc against the 1.19 the kernel requires, short by 2.1e+03)
[FAIL] D4 [test] a length the theory already carries, or a principled combination of its own constants, supplies the required smoothing scale to within 0.5 dex   (NO -- closest fixed candidate 3.01 dex away; xi is 1.5e+05 x too small outside-J and 1026 x too small inside-J)
[PASS] E1 [test] the mechanism passes CASSINI and the wide-binary regime   (YES by 9.3e+24 at Cassini and 8.2e+15 at 10 kAU, with NO steepness assumed anywhere.  L56 E3's pincer is LIFTED)
[FAIL] E2 [test] disc outskirts and isolated field galaxies keep the deposited theory's no-slip result at the working point (kernel n4, l_rms = 1 Mpc)   (reaches 3.62e-01 for the largest discs probed to 300 kpc; median 1.2e-03; 153/155 clear the 20% bound)
[FAIL] E3 [test] X-ray groups keep the deposited theory's no-slip result at the working point   (NO -- 20-45%.  Groups are EXTENDED against the smoothing, so the mechanism does not hide them: that is the mechanism working as designed and it is the sharpest thing it predicts.  Whether it is excluded is NOT decided here -- the channel is estimator-limited)
[FAIL] E4 [test] the environmental dependence the mechanism predicts is already excluded by measurement   (NOT DECIDED -- 0.024% - 2.3% for galaxies at cluster radii and essentially none in the field; not measured anywhere near 0.1%.  It is the measurement that would decide this door)
[PASS] E5 [test] the REFERENCE cosmological slip on 10 Mpc scales is under 1%   (2.57e-03; reported as an open channel with a named calculation, NOT as a kill and NOT as a pass)
[PASS] F1 [control] gate 1 alone reproduces L51's answer, 8.8 -> 4.9 / 9.0 -> 4.7 sigma
[FAIL] F2 [test] subject to ALL the gates, the mechanism removes the cluster shear-shape failure (residual under 3 sigma)   (NO, and the reason is NOT the new mechanism.  On the EMPIRICAL arm the FULL L51 ceiling is available -- 8.8 -> 4.9, 9.0 -> 4.7 -- because the embedded gate no longer binds and Cassini never did.  But the lensing-versus-dynamics budget alone still caps the phantom, so the shape failure is HALVED and not cured)
[FAIL] F3 [test] the addition is cheap -- one new coupling constant or fewer   (a new free function of a new variable, plus a length that nothing in the theory supplies, plus an integer operator order, fitted to 5 cluster shear log-slopes)
[FAIL] G1 [VERDICT] the nonlocal functional is a USABLE handle on the cluster shear shape   (PARTLY -- (1) it WORKS as a mechanism and L56's pincer is broken; (2) it does NOT reach the theory's own number, floor 2.4e-04 = 2.4 x 1e-4; (3) the length is FITTED, l_rms >= 600 kpc against xi = 4.00 pc.  And at its ceiling it HALVES the failure, 8.8 -> 4.9 / 9.0 -> 4.7 sigma, because the lensing-versus-dynamics budget is what caps the phantom)
```

The complete, untruncated lines are in [`L57_nonlocal_functional.out`](L57_nonlocal_functional.out).

## 11. Scope — what is not done here

- The **cosmic-shear forecast** with the pinned `W` is not run; E5 is a reference estimate only, and it
  depends on how `W` is continued below the cluster range, which is a free function.
- The **group model** is a stated isothermal sphere normalised to `M_gas500 × 1.30`, chosen because it
  maximises the group's own trigger gradient; the groups' measured profiles are not used.
- The cluster's **surroundings beyond 3 R200** are replaced by the cosmic mean. This understates the floor
  and is recorded as running against the door.
- The nonlocal weight's effect on **structure formation** is not computed. B6 establishes that the elliptic
  realisation adds no propagating mode, but the instantaneous constraint's cosmological behaviour is a
  separate calculation.
- Nothing was written into `PREREGISTRATION_DR4.md`, any `*_HASH.txt`, `FINDINGS.md` or
  `HANDOFF_CONTRACT.md`. No file outside `fable_independent_2026/` was created or modified.
