# L56 — the potential-depth trigger: the one door L51 priced and declined to close

2026-09-09. Lane L56. Script: [`L56_potential_trigger.py`](L56_potential_trigger.py) →
[`L56_potential_trigger.out`](L56_potential_trigger.out). **30 checks, 17 PASS / 13 FAIL.**
Both a₀ footings (9.3619e-11 / 1.1279e-10 m s⁻²) on every dimensional number.

Method: nothing under `closure_2026/` or the lead agent's directories was imported, executed or copied.
The symbolic algebra was built here in sympy. The cluster, group, galaxy and dwarf data were read directly
from the on-disk public archives (X-COP FITS, Herbonnet 2020 Tables 2–3, SPARC rotmod, Lovisari et al.
2015, McConnachie 2012). **L51's eight load-bearing numbers are re-derived as controls, not inherited** —
including the acceleration/density overlap and the potential-depth non-overlap this whole lane rests on.

---

## The verdict, first

**The trigger survives the covariance obstruction — that is a real positive and it is the first thing this
lane found. It then fails on what the covariant carrier costs, and the failure is convention-free.**

- **B4 PASS.** A potential-depth trigger **can** be written covariantly in this theory. It is carried by
  `X = 1 − Q/Q₀` with `Q = n^μ∂_μφ`, the clock-projected gradient of the theory's **own** MOND scalar:
  statically `Q = Q₀/N`, so `1 − Q/Q₀ = Φ/c² + O(Φ²)`. It escapes L31 Step E precisely because it is not
  built from the metric alone — a matter-sector scalar with a nonzero cosmological background supplies the
  reference the metric cannot. L51's objection (i) is therefore **answered, not upheld**.
- **B1 FAIL, and it is stronger than L31 stated it.** A constant deepening of Φ is an **exact isometry**
  (a rescaling of `t`), not merely a linear-order degeneracy. No functional of the metric and its
  derivatives, of any order, local **or nonlocal**, can measure a potential depth. Every scalar the
  deposited action is built from — `R`, `R_μν n^μn^ν`, `θ`, `a²`, `Y` — is depth-blind (B3).
- **B5 FAIL — the price of the escape, and it is structural.** `Q₀` is the clock's *cosmological*
  background rate, so `X` is the depth relative to the cosmos: **the total potential at a point**,
  additive over sources. There is no local field that sees a host and not its substructure.
- **C3 FAIL, the crux, and it needs no convention at all.** The cluster does not require a slip *value*,
  it requires a slip *profile*. Matching it pointwise gives `W′(X) = 2 g_P/g_fw`, so the fractional slip
  suffered by any object embedded at cluster depths is **exactly `M_P(<r)/M_fw(<r)`** —
  **0.806 (canonical) / 0.669 (alt)**, which is **8.1e3 / 6.7e3 ×** the deposited theory's own `Φ = Ψ`
  to 1e-4 and **4.0 / 3.3 ×** a generous 20% empirical bound. No truncation, no zero point, no steepness,
  and **no five-cluster scatter** enters this number.
- **E3 FAIL — the window is empty.** Cassini caps the amplitude from **below** (a weaker cluster slip needs
  a shallower weight, and a shallow weight is nearly scale-free, so it leaks into the Solar System) while
  the embedded-galaxy consistency caps it from **above**. **No amplitude satisfies the lensing/dynamics
  gate, Cassini and the trigger's own consistency at once**, on either pinning arm, on either footing.

**So: the shear-shape residual stays at 8.8σ / 9.0σ.** L51's 4.9σ / 4.7σ is recovered exactly (E1) and is
the answer to a *narrower* question — the two named gates only, with the trigger's own internal
consistency not yet imposed.

---

## 1. Controls (A1–A8) — L51 reproduced, not inherited

| control | L51 / L24 | here |
|---|---|---|
| A1 the two combinations, map determinant | `S₁ = 2∇²(2Ψ−Φ)`, `S₂ = ∇²Φ`, det −4 | identical |
| A2 projection machinery vs analytic NFW | 1.2e-6 / 2.2e-6 | 1.23e-6 / 2.15e-6 |
| A3 the 9σ shear-shape failure | +0.516 ± 0.058 / +0.521 ± 0.058 | **identical, 8.8σ / 9.0σ** |
| A4 measured cluster `g_lens/g_dyn` | 1.148 ± 0.146 | **1.148 ± 0.146** |
| A5 the 3σ-budget ceiling | 8.8 → 4.9 at f ≤ 0.73; 9.0 → 4.7 at f ≤ 0.88 | **8.8 → 4.9 at f = 0.72; 9.0 → 4.7 at f = 0.86** |
| A6 acceleration and density triggers overlap SPARC | 100% of cluster rows inside | **100% / 100%** |
| A7 potential depth does **not** overlap | clusters 1.87–4.67e11, SPARC ≤ 8.42e10, gap 2.22 | **identical, gap 2.22** |
| A8 required steepness on the surviving trigger | 16.0 / 6.5 canonical, 15.8 / 6.2 alt | **identical** |

## 2. The trigger, written covariantly (B1–B6)

    metric sector:   every scalar is built from DERIVATIVES of Phi  =>  depth-blind (B1, B2, B3)
    clock sector:    Q = n^mu d_mu phi = Q0 / N   =>   X = 1 - Q/Q0 = Phi/c^2 + O(Phi^2)   (B4)
    the price:       Q0 is COSMOLOGICAL  =>  X is the TOTAL depth, additive over sources     (B5)

**B6, the one formula.** For `s = W(X)`, an object digging its own well `δΦ` on an ambient `X` sees the
slip vary by `W′(X)δΦ/c²` against its own lensing signature `2δΦ/c²`, so the fractional slip is
`R = W′(X)/2`, **independent of the object**. That covers `γ_PPN − 1` at Cassini, the wide-binary regime,
satellites, and galaxies at cluster radii with a single expression.

## 3. The trigger re-measured on its own definition (C1–C4)

L51's non-overlap was established for the *local proxy* `g_bar r`. On the covariant variable (integrated
depth, truncated at `T × R200` with `R200` from the baryonic mass; T = 1, 2, 4 all carried):

| T | E_cl (canonical / alt) | gap cluster/galaxy | p required to reach the galaxy bound |
|---|---|---|---|
| 1 | 0.591 / 0.468 | 1.50 / 1.56 | 22.4 / 20.0 |
| 2 | **0.306 / 0.203** (= A4 exactly) | 3.82 / 3.96 | 6.99 / 6.54 |
| 4 | 0.270 / 0.331 | 6.04 / 6.26 | 5.39 / 5.42 |

- **C1 FAIL, but the FAIL is mild and half of it favours the door.** The separation is **real** on the
  covariant variable — the isolated-galaxy population never reaches cluster depths at any truncation, so
  L51's non-overlap is **not** an artefact of its proxy. What fails is the *margin*: at the tightest
  convention the gap is 1.50 rather than 2.22, and the required steepness moves to 5.4–22.4.
- **C2 PASS.** Every one of the five clusters carries **1.9e12–1.0e13 M⊙ of measured stellar mass** in the
  0.5–2 Mpc shell — i.e. galaxies, sitting at the cluster's trigger value by B5. The population the crux
  needs is measured, not hypothetical.
- **C3 FAIL, the crux.** `R = M_P/M_fw = 0.806 / 0.669`; per cluster 0.21–1.65 (canonical), so no single
  cluster carries it.
- **C4 FAIL, and reported as convention-dependent rather than banked.** `p_local`, measured directly from
  the required slip gradient at cluster depths, is **1.5–4.6**; `p_connect`, needed to reach the galaxy
  bound, is **5.4–22.4**. They differ by 1.18× at the loosest truncation and 15× at the tightest. What is
  convention-free is that `p_local` exceeds the chameleon/symmetron 1–3 on most conventions.

## 4. The systems in between (D1–D5)

Ladder at T = 2, canonical, on the arm that survives the Solar System:

| system | `X = Φ/c²` | E (excursion) | R = W′/2 (embedded) |
|---|---|---|---|
| isolated dwarf spheroidal (median) | 2.08e-9 | 5.7e-25 | 4.0e-24 |
| SPARC disc outskirt (median) | 2.63e-7 | 2.2e-12 | 1.6e-11 |
| Milky Way at the Sun (Cassini, wide binaries) | 1.35e-6 | 4.1e-8 | 2.9e-7 |
| X-ray group at R500 (median) | 2.29e-6 | 9.8e-7 | 6.8e-6 |
| deepest SPARC galaxy (the pinning point) | 4.96e-6 | 1.0e-4 | 7.0e-4 |
| cluster at R500 (where the slip is required) | 1.89e-5 | 3.1e-1 | **0.81** |

- **D1 FAIL** — the worst X-ray group response reaches **3.3e-3**, 33× the theory's own 1e-4 bound, at the
  worst convention (5.2e-17 at the best). Twenty X-ray groups, Lovisari 2015, gas mass held constant
  beyond R500 (conservative).
- **D2 PASS** — disc outskirts are the one intermediate scale the weight passes cleanly: worst response
  1.3e-5, **0.13×** the 1e-4 bound on the surviving arm.
- **D3 PASS** — dwarfs are safe by many orders, isolated and as Milky Way satellites. The channel decides
  nothing on its own; what it exposes is that the shallow pinning arm is nearly scale-free.
- **D4 FAIL, and the two arms separate cleanly.** At the Milky Way's ambient depth the **shallow (20%)
  pinning arm gives a Solar-System response of 1.8e-2 – 2.0e-1, i.e. 8.7e3 × Cassini** — decisive. The
  **steep arm is marginal**: 1.1e-11× to 0.12× Cassini across conventions and Milky Way models, and it is
  reported as marginal, not quoted as a kill.
- **D5 PASS, and it retracts a tempting kill.** Read at their innermost points, 20/20 groups sit *below*
  the deepest SPARC galaxy in the trigger. Read at a matched fractional radius (0.5 R200, the R500
  analogue) the ordering is **correct**. The un-matched comparison is a reference-radius artefact and is
  stated as one rather than banked.

## 5. The two gates, and the best achievable improvement (E1–E3)

Four constraints act on the amplitude f of the added lensing phantom, and **two pull opposite ways**:

    (1) lensing/dynamics ratio          caps f from ABOVE
    (2) isolated-galaxy no-slip gate    does not cap f -- it FIXES the steepness p(f)
    (3) embedded-galaxy consistency     caps f from ABOVE:  R_emb = f x M_P/M_fw
    (4) CASSINI                         caps f from BELOW:  small f => shallow weight => scale-free

| f | shape σ | lens/dyn σ | R_emb | p (theory) | R_Cassini (theory) | p (20%) | R_Cassini (20%) |
|---|---|---|---|---|---|---|---|
| 1.1e-4 | 8.83 | 1.01 | 8.7e-5 | 0.17 | 2.9e-4 | −5.50 | 4.6e-4 |
| 1.2e-2 | 8.63 | 0.95 | 9.4e-3 | 3.67 | 1.1e-5 | −2.01 | 5.0e-2 |
| 1.0e-1 | 7.47 | 0.46 | 8.1e-2 | 5.27 | 2.0e-6 | −0.40 | 4.3e-1 |
| 3.4e-1 | 5.91 | 0.86 | 2.7e-1 | 6.19 | 7.2e-7 | 0.51 | 3.8e-1 |
| 7.0e-1 | 4.92 | 2.85 | 5.6e-1 | 6.73 | 3.9e-7 | 1.05 | 2.0e-1 |
| 1.0e0 | — | 4.50 | 8.1e-1 | 6.99 | 2.9e-7 | 1.32 | 1.7e-1 |

**The ceilings.**

| constraint set | canonical | alt |
|---|---|---|
| gates 1+2 only — **L51's question** | f ≤ 0.715 → **8.8 → 4.9σ** | f ≤ 0.865 → **9.0 → 4.7σ** |
| + Cassini, steep arm | f ≤ 0.715 → 8.8 → 4.9σ | f ≤ 0.865 → 9.0 → 4.7σ |
| + Cassini, shallow (20%) arm | **no amplitude** → 8.8σ | **no amplitude** → 9.0σ |
| **+ Cassini + embedded consistency, either arm** | **no amplitude → 8.8σ** | **no amplitude → 9.0σ** |

The admissibility condition used is `p ≥ 1`, and it is not a matter of taste: `p < 1` means the weight
rises more slowly than the potential, so an isolated galaxy's own fractional slip would exceed the
cluster's — contradicting the premise. Algebraically `p ≥ 1` is exactly `f E_cl ≥ tolerance`.

## 6. The price (F1–F3)

- **F1 FAIL — three parameters against six numbers.** `W = W₀(X/X*)^p` plus a floor is amplitude,
  threshold and steepness, plus the *choice* of variable, fitted to five cluster shear log-slopes and one
  lensing/dynamics ratio. The deposited action already carries `K(Q)`; `W(Q)` is a **second free function
  of the same argument**, so the cost is a function, not a coupling.
- **F2 FAIL — the steepness is forced twice over, and that is what makes it tuned.** Cassini **alone**,
  with no input from the galaxy pinning, forces the leading power of the expansion about the cosmological
  background to **n ≥ 5** at the most generous convention and **n ≥ 9** at the least, on both footings.
  That is at least four tuned cancellations. The galaxy pinning independently asks for **p = 5.4–22.4**.
  Chameleon and symmetron screening are powers 1–3.
- **F3 FAIL — nothing independent fixes the threshold.** The theory has one intrinsic length (`c/H₀`) and
  one intrinsic acceleration (`a₀`, itself fitted). Their one dimensionless potential
  `a₀/(cH₀) = 0.143` overshoots the required `X* ≈ 1.9e-5` by **3.9 dex**. A free integer power can be
  made to land within 0.42 dex — but consecutive powers are 0.85 dex apart, so **any** target is within
  0.42 dex of some power by construction; that exponent is then a fitted parameter, not a prediction.

## 7. THE THEOREM

**No scale-selective metric slip from a single local trigger.** Let the slip be `s = W(X)` for a
single-valued `W` of one local scalar `X` built from the metric, the preferred unit normal, and the
theory's scalars. Then:

1. **If `X` is built from the metric alone** it is blind to the potential depth — a constant deepening is
   an *exact* isometry (B1) — and blind to a uniform field (B2, L31 Step E). What remains is a curvature,
   i.e. an acceleration or a density, and L51 C9–C11 showed those overlap SPARC completely: 100% of the
   cluster weak-lensing rows sit inside the galaxy range, overshooting the theory's own no-slip bound by
   3.2e6 (reproduced here, A6).
2. **If `X` uses the theory's clock**, the unique carrier of a depth is `X = 1 − Q/Q₀` with
   `Q = n^μ∂_μφ` (B4) — a genuine escape from (1). But its zero is the cosmological background, so `X` is
   the **total** potential at a point, additive over sources (B5), and cannot be referenced to an object
   rather than to the cosmos. **There is no local field that sees a host and not its substructure.**
3. **Under (2)**, any object embedded at ambient `X` suffers `R = W′(X)/2`, independent of the object
   (B6). And `W′` is not free: matching the required lensing phantom pointwise gives `W′ = 2 g_P/g_fw`,
   so **`R = M_P(<r)/M_fw(<r)` exactly** — 0.669–0.806 on the X-COP weak-lensing sample, i.e.
   6.7e3–8.1e3 × the theory's own `Φ = Ψ` result and 3.3–4.0 × a 20% empirical bound. It scales with the
   amplitude, so it can be reduced only by giving up the repair — and Cassini then caps the amplitude
   from below. **The interior is empty.**

**COROLLARY.** A scale-selective metric slip is not obtainable from **any** single local trigger in this
theory: not from the metric sector, not from the clock sector. Since the second combination is the only
linear-in-`h` freedom the preferred vector supplies (L39's operator count, reproduced in A1), and since a
frame-free addition cannot move the lensing potential at all (L51 B4), **the cluster weak-lensing shape is
not reachable by an operator freedom of this theory under any trigger.**

**What would overturn it, stated so it is falsifiable.**
- A weight built on a **non-local functional that is not a function of the local field value** — for
  instance one responding to the *size of the region over which the field is coherent* rather than to the
  field's depth there. That is a different object, it is not tested here, and the theorem does not cover
  it. It is the one live successor to this door.
- `M_P/M_fw` at cluster radii falling by 3–4 orders of magnitude (theory arm) or by 3.3× (empirical arm).
  That is an **amplitude**, not the noise-limited five-cluster scatter L51 refused to quote.

## 8. Honesty ledger, to L51's own standard, in both directions

- The five-cluster **scatter** of the required weight is not used anywhere, in either direction. L51 C13b
  showed it is noise-limited (fractional error 1.41) and this lane inherits the refusal, not the number.
- **Two findings run in the door's favour and are recorded as such:** B4 (the trigger *is* covariantly
  writable, which L51 doubted) and C1 (the non-overlap is *not* an artefact of L51's proxy).
- **Three numbers are reported as marginal or convention-dependent rather than banked:** the Cassini
  response on the steep arm (D4), the two-slope disagreement (C4), and the group ordering (D5 — where a
  matched-radius control shows the tempting "20/20 groups below the deepest galaxy" is a reference-radius
  artefact, and the check was rewritten to say so).
- **The door is not closed by failing to fit.** The fit succeeds — a unique `W` exists, the covariance
  obstruction is genuinely survived, the non-overlap is real. It is rejected on what it does elsewhere.
  A steep tuned function that fits five clusters is not a mechanism, and that is what this one is.
- No statement anywhere that data favour this framework over ΛCDM.

## 9. What this changes in the standing record

1. **L51's objection (i) is withdrawn and replaced.** `g_bar r` is not a covariant scalar, but the theory
   *does* have a covariant carrier for the depth, and it is not the lapse — it is `Q = n^μ∂_μφ`, the
   scalar the action already contains. The right objection is not "it cannot be written" but "writing it
   costs the cosmological reference".
2. **L31 Step E should be quoted in its exact form.** A constant deepening of Φ is an exact isometry, not
   a linear-order degeneracy, so the obstruction covers nonlocal metric functionals in one line.
3. **The cluster shear-shape repair has a convention-free price:** `M_P/M_fw = 0.806 / 0.669`. Any
   mechanism that repairs the shape by a metric slip pays exactly that fractional slip on everything
   sitting at cluster radii. This is a general constraint on the *next* proposal, not only on this one.
4. **The last named handle on the cluster shear shape is closed**, under the theorem's stated hypotheses.
   The named successor is a coherence-length-type functional, which is a different object.

---

## 10. The PASS/FAIL lines

```
[PASS] A1 [control] L51's two combinations reproduce: S1 = 2 lap(2 Psi - Phi) frame-free, S2 = lap Phi needs u, map determinant -4   (det -4; S2 isolates the Newtonian potential, (S1 + 2 S2)/4 = lap Psi)
[PASS] A2 [control] the projection machinery reproduces the analytic NFW Sigma and DeltaSigma to 0.5%   (max |Sigma err| 1.23e-06, max |DeltaSigma err| 2.15e-06)
[PASS] A3 [control] the 9-sigma cluster shear-shape failure is reproduced independently (L51 C2: +0.516 +/- 0.058 / +0.521 +/- 0.058)   (canonical +0.516 +/- 0.058 (8.8 sigma), alt +0.521 +/- 0.058 (9.0 sigma))
[PASS] A4 [control] the measured cluster lensing/dynamical mass ratio is reproduced   (1.148 +/- 0.146)
[PASS] A5 [control] L51's ceiling reproduces: inside the 3-sigma lensing/dynamics budget the freedom takes the shape residual from 8.8 to 4.9 sigma (canonical) / 9.0 to 4.7 (alt)   (canonical 8.8 -> 4.9 sigma at f = 0.72, alt 9.0 -> 4.7 sigma at f = 0.86)
[PASS] A6 [control] the acceleration and density triggers OVERLAP SPARC completely (L51 C9: 100% of cluster rows inside)   (g_bar 100%, rho_b 100%)
[PASS] A7 [control] the potential-depth proxy Phi_loc = g_bar r does NOT overlap SPARC over 0.5-2 Mpc (L51: clusters 1.87-4.67e11, SPARC <= 8.42e10, gap 2.22)   (canonical gap 2.22x, alt gap 2.22x)
[PASS] A8 [control] L51's required steepness reproduces (16.0 / 6.5 canonical, 15.8 / 6.2 alt)   (canonical 16.0 / 6.5, alt 15.8 / 6.2)
[FAIL] B1 [test] the potential DEPTH is a local covariant scalar of the metric alone   (NO -- a constant shift of Phi is an EXACT isometry (a rescaling of t), so no functional of the metric and its derivatives, of any order, local or nonlocal, can measure the depth.  This is L31 Step E's obstruction in its strongest form: not a linear-order degeneracy but an exact one)
[PASS] B2 [control] L31 Step E reproduces: adding a uniform field leaves every component of the linearised curvature exactly unchanged   (all 16 components identical for arbitrary g -- so the gradient is not local either, and the obstruction the earlier lane proved is confirmed here independently)
[PASS] B3 [control] every scalar the deposited action is built from is blind to the potential depth   (R, R_mn n^m n^n, theta, a^2 and Y all depend on DERIVATIVES of Phi only.  The lapse N is the one object that is not blind -- and the action does not contain it, because tau enters only through n_mu, which is invariant under tau -> f(tau) while N -> N / f'.  So the METRIC side offers nothing)
[PASS] B4 [test] the potential-depth trigger CAN be written covariantly in this theory   (YES -- carried by X = 1 - Q/Q0 with Q = n^mu d_mu phi the clock-projected gradient of the theory's OWN MOND scalar.  It evades L31 Step E because it is not built from the metric alone: it uses a matter-sector scalar whose nonzero cosmological background supplies the missing reference.  This is a genuine escape and the lane records it as one)
[FAIL] B5 [test] the covariant carrier can be referenced to the OBJECT rather than to the cosmos   (NO -- X is additive in the potential and its zero is the cosmological background, so a galaxy inside a cluster carries the CLUSTER's trigger value.  There is no local field that sees a host and not its substructure: 'the host's potential' is not a functional of anything local.  This is the price of the escape in B4, and PART C and PART D are what it costs)
[PASS] B6 [control] the response formula is the identity R = p E, with E(X_cl) measured from the shear data and p the logarithmic slope of the weight   (canonical E(X_cl) = 0.306, alt E(X_cl) = 0.203 -- this is an AMPLITUDE, not the five-cluster scatter, and it is what every kill below uses)
[FAIL] C1 [test] the NON-OVERLAP that this whole door rests on survives on the covariant trigger with a margin at least as large as L51's proxy gap of 2.22   (gap = 1.50 - 6.26 over T = 1-4 and both footings, against 2.22 on L51's local proxy.  The separation is REAL and is NOT an artefact of L51's proxy -- that is a result in the door's favour -- but at the tightest convention it is 1.48x smaller than the proxy suggested, and the required steepness moves correspondingly to 5.4 - 22.4 rather than 16.0)
[PASS] C2 [control] there is measured galaxy-scale (stellar) mass at the cluster radii the weight must switch on at   (1.93e+12 - 1.04e+13 Msun of measured stars per cluster in that shell -- i.e. galaxies, sitting at the cluster's trigger value by B5)
[FAIL] C3 [CRUX] the covariant potential-depth trigger can act at cluster depths WITHOUT acting on the galaxies that sit at those depths   (NO -- the required slip GRADIENT fixes the embedded response exactly: R = M_P/M_fw = canonical 0.806, alt 0.669, i.e. 6.7e+03 - 8.1e+03 x the theory's own 1e-4 bound and 3.34 - 4.03 x a 20% empirical bound.  No convention, no steepness and no five-cluster scatter enters this; it is the amplitude of the phantom the shear data require.  This is L51's C9 overlap argument recovered for the depth trigger)
[FAIL] C4 [test] the weight can be ONE power law: the slope measured at cluster depths matches the slope needed to connect down to galaxies (within 1.5x)   (p_connect / p_local = 1.18 - 14.57 over T = 1-4 and both footings.  THIS ONE IS CONVENTION-DEPENDENT and is reported as such, not banked: at the loosest truncation the two determinations agree to 1.18x, at the tightest they differ by 15x.  What is convention-free is that p_local is MEASURED at 1.5 - 4.6, i.e. the weight is genuinely steeper than the chameleon/symmetron 1-3 at cluster depths on most conventions.  Whether a single power law also reaches the galaxy bound is left open here)
[FAIL] D1 [test] the pinned weight passes through X-ray GROUPS without breaking them   (worst group response 5.20e-17 - 3.34e-03 on the theory arm (3.3e+01 x the 1e-4 bound at the worst convention) and 1.46e-02 - 2.85e-01 on the data arm (1.4e+00 x the 20% bound); and 20/20 groups sit BELOW the deepest SPARC galaxy CENTRE -- see D5, where a matched-radius control shows that particular comparison is a reference-radius artefact, so it is stated rather than banked)
[PASS] D2 [test] the pinned weight passes through the OUTSKIRTS OF LARGE DISCS, on the pinning arm that survives the Solar System (the steep, theory-tolerance arm; D4 excludes the shallow one)   (the EXCURSION reaches 2.39e-06 (theory arm) and 1.98e-01 (data arm) -- the gate the pinning was written against, so it holds by construction.  The RESPONSE reaches 1.29e-05 on the theory arm, which CLEARS the 1e-4 bound at 0.13 x, and 2.02e-01 on the data arm, which is 1.01 x the 20% bound -- marginal, and the data arm is separately excluded by Cassini in D4.  Disc outskirts are therefore the one intermediate scale the weight passes, and the FAIL here is marginal and is reported as marginal)
[PASS] D3 [test] the pinned weight passes through DWARFS, isolated and as satellites   (isolated dwarfs on the theory arm are safe by many orders (1.3e-09); on the DATA arm the pinning is nearly linear (p ~ 1), which makes the fractional slip almost scale-free, so even a dwarf takes 1.97e-01 (0.98 x the 20% bound).  Satellites at the Milky Way's ambient depth take 2.69e-06 (theory, 0.03 x) and 1.99e-01 (data, 1.00 x).  The dwarf channel therefore does not decide anything on its own; it is the near-linearity it exposes that Cassini then kills in D4)
[FAIL] D4 [test] the pinned weight passes CASSINI, and with it the wide-binary regime, at the Milky Way's own ambient depth   (theory arm 2.44e-16 - 2.69e-06 (0.12 x Cassini at the worst convention, 1.06e-11 x at the best) -- reported as MARGINAL, not as a kill, because it turns on the Milky Way model; data arm 1.77e-02 - 1.99e-01, which is 8.7e+03 x Cassini and IS decisive.  So the shallow 20% pinning arm is not available at all: only the steep theory arm survives the Solar System, and C3 already fails on it)
[PASS] D5 [control] the trigger ORDERS the systems the way the mechanism needs -- groups, which need the weight, above the deepest discs, which must not have it -- when both are read at a matched fractional radius   (at matched radius the median group (2.292e-06) sits above the deepest disc (1.086e-06) by 2.11x, so the trigger DOES order the populations and D1's '20/20 groups below the deepest galaxy' is a reference-radius artefact, stated here rather than banked.  What survives is the gate statement, not an ordering failure: the deepest galaxy CENTRES (4.961e-06) are deeper than every group at R500, and the no-slip gate applies at those centres)
[PASS] E1 [control] gate 1 alone reproduces L51's answer: 8.8 -> 4.9 / 9.0 -> 4.7 sigma   (canonical -> 4.9 sigma, alt -> 4.7 sigma)
[FAIL] E2 [test] gate 2 -- the deposited theory's no-slip result in galaxies -- is preserved at the amplitude gate 1 allows   (the ISOLATED-galaxy excursion is preserved by construction, which is what pins p; the EMBEDDED response at that amplitude is R = 0.58, 0.58, i.e. 5.8e+03 x the same 1e-4 bound, on the galaxies that sit at cluster depths)
[FAIL] E3 [test] subject to BOTH gates, CASSINI, and the trigger's own embedded consistency, the freedom still removes the shape failure (residual under 3 sigma)   (the window is EMPTY on both arms: no amplitude satisfies the lensing/dynamics gate, Cassini and the embedded-galaxy consistency at once, because Cassini caps f from BELOW (a shallow weight is scale-free and leaks into the Solar System) while the embedded consistency caps it from ABOVE.  The shape residual therefore stays at canonical 8.8 sigma, alt 9.0 sigma)
[FAIL] F1 [test] the addition is cheap -- one new coupling constant or fewer   (3 free parameters plus the choice of trigger variable, fitted to 5 cluster shear slopes.  A steep tuned function that fits five clusters is not a mechanism, and this lane says so rather than quoting the improvement it buys)
[FAIL] F2 [test] the required steepness is natural -- the leading term of the EFT expansion about the cosmological background can be low order (n <= 3, as chameleon and symmetron screening are)   (Cassini ALONE forces n >= 5 at the most generous convention and n >= 9 at the least, on both footings, with no input from the galaxy pinning.  That is at least 4 tuned cancellations in an expansion about the cosmological background -- and the galaxy pinning independently asks for p = 5.4 - 22.4.  Two independent routes agree the weight must be steep, which is what makes it tuned rather than mechanistic)
[FAIL] F3 [test] a scale independent of the cluster data fixes the threshold (within 0.5 dex), using only principled combinations of the theory's own constants   (closest principled candidate is (a0/(c H0))^2 at 3.03 dex.  The theory has ONE intrinsic length (c/H0) and ONE intrinsic acceleration (a0), and their one dimensionless potential a0/(c H0) = 0.143 overshoots the required 1.89e-05 by 3.9 dex.  A free integer power CAN be made to land within 0.42 dex, but that exponent is then a fitted parameter, not a prediction.  The threshold is set by the cluster data and by nothing else)
[FAIL] G1 [VERDICT] the potential-depth trigger is a USABLE handle on the cluster shear shape   (the covariance obstruction is SURVIVED (B4: the trigger is carried by X = 1 - Q/Q0, the clock's own scalar), and that is a real positive.  But the carrier's zero is the cosmological background (B5), so the trigger is the TOTAL depth; the galaxies that sit at cluster depths then take R = M_P/M_fw = 0.67 - 0.81 exactly, against 1e-4 and 20%.  Best achievable subject to both gates AND the trigger's own consistency: canonical 8.8 -> 8.8 sigma (20%) / 8.8 sigma (1e-4), alt 9.0 -> 9.0 sigma (20%) / 9.0 sigma (1e-4))
```
