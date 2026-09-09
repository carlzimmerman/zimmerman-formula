# L32 — necessary conditions on ANY theory that derives κ

`L32_kappa_necessary.py` / `.out` — 20 checks, **10 FAIL**. Every FAIL is an obstruction
established, not a defect discovered; each check's detail line says which way it points.

Everything the programme knew about κ was about **one action** (k01–k04, L3). This lane asks
the general question: *what must any theory satisfy to make `a₀ = κ c√(Gρ_Λ)` a consequence
with a fixed dimensionless κ?* The answer is a pincer with a narrow exit, and the exit is
now named precisely.

**κ remains FITTED.** Nothing here derives it, and nothing here makes ½ preferred over 0.461.

---

## 0. What the relation actually says

Two controls fix the arithmetic:

- `c√(Gρ_Λ) = 1.8725e-10 m/s²` on Planck parameters (A1) — reproduces the corpus value to 0.03%,
  and κ(canonical) = 0.5000 as adopted.
- **G cancels identically** (A2). `a₀ = κ c√(Gρ_Λ)` *is* `a₀ = κ√(3/8π) c²/L_dS`, i.e. one
  dimensionless ratio of two lengths: ℓ₀/L_dS = **5.79** canonical, **4.81** alt, with
  ℓ₀ = c²/a₀. Equivalently Λℓ₀² = 8π/κ² = 32π at κ = ½ — **and 69.3 on the alt footing**, so
  "32π" is a canonical-footing statement, exactly the guard L3's Q8 raises about the "8".
- The same statement as a seesaw (A5): `a₀ = X²/M_Pl` with `X = (ρ_Λc²)^(1/4) = 2.240 meV`
  reproduces 1.8726e-10 m/s² — an independent route to the same number.

So the coefficient problem is a **number of order 10², not 10¹²⁰**: the natural scale of the
MOND sector's own energy density is already ρ_Λ up to 16π/κ² ≈ 200 (k01's "factor 222"). There
is no naturalness problem here to solve, and correspondingly no naturalness argument to exploit.

---

## 1. The necessary conditions

| | condition | established by |
|---|---|---|
| **N1** | **Vacuum-structural, not dynamical.** The tie must be a relation between *constants*. Λ's direct acceleration at 10 kpc is `1.1e-5 a₀` and reaches a₀ only at 928 Mpc: no term in the equations of motion can carry it. | A3 (FAIL) |
| **N2** | **An order parameter of odd mass dimension.** There must exist X, **non-vanishing on a homogeneous background**, with ρ_vac ∝ X² and a₀ ∝ X. Amplitude-independence of κ forces exactly (m,n) = (2,1) (or (2k,k)). Curvature polynomials on de Sitter are integer powers of Λ; pairing an integer power with any independent mass M gives d ln a₀/d ln Λ = k, **never ½**. | A4 (FAIL) |
| **N3** | **LOCK.** `d ln a₀ = ½ d ln Λ` along **every free-parameter direction**. This is precisely what forbids the trivial possibility. | A6 (PASS) |
| **N4** | **RIGIDITY.** κ must be fixed by discrete or structural data, not by a continuous coupling. Given N2 this is exactly `Z̃ = λβ²` with λ a pure number, i.e. a statement about the canonically normalised coupling `β/√Z̃ = κ/√2 = 0.354` (canonical) / 0.426 (alt). | C1 (FAIL), D4 |
| **N5** | **No additive freedom.** The MOND function must not enter as a field-independent coefficient × √(−g) with an unfixed additive constant. | B2 (PASS), B4 (FAIL) |
| **N6** | **Testability.** A prediction is rejectable today only if it differs from the combined κ = 0.530 by more than **24%** (total comparison uncertainty 8.0% = 7.1% statistical ⊕ 3.8% H₀ convention). The H₀ convention must be stated with any prediction. | D2 (FAIL), D3 (FAIL) |
| **N7** | **Say what a₀ tracks.** A tie to a strictly constant ρ_Λ has **no observable signature at all** beyond the coefficient itself. Only a tie to a dynamical quantity is falsifiable inside one universe: a₀ ∝ cH(z) moves the deep-MOND Tully–Fisher zero point by **+0.576 dex by z = 2.5**. | A7 (FAIL) |

**N3 is a condition a theory must MEET, not a fact established about nature.** The possibility
that a₀ and Λ are two independent constants that happen to satisfy the numerical coincidence is
not excluded by anything here or anywhere in the corpus.

---

## 2. The theorems (all stated in general form, all with a control)

| | theorem | control |
|---|---|---|
| **T1** | **Additive zero mode, generic.** In *any* local action whose MOND function F multiplies √(−g) with a field-independent coefficient, `F → F + C` adds `C√(−g)` — which *is* a cosmological-constant term — so every field equation depends on C only through Λ_eff. Verified on four structurally different F (one field; a squared primitive; two fields' gradients mixed; an explicit rational coefficient). | **B1 reproduces k01's K1 and K2 exactly**, independently in this script |
| **T2** | **Split degeneracy, generic.** Given N2's (m,n) = (2,1), the cosmological sector sees only the *total stiffness* Z̃ of the order parameter, because Z̃ is what its own equations contain; β is a coupling of the same order parameter to a *different* sector. κ² = 2β²/Z̃ needs the split. | generalises L3's Q5 map off its particular model |
| **T3** | **de Sitter dilution.** Any 4-volume average of a gradient sector → 0 in a Λ-dominated future: the volume grows as e^{3H_Λt} while the frozen peculiar field's contribution per comoving volume tends to a constant. Computed from a ΛCDM growth integral: `1.1e-8` at 10 t₀. | reproduces k02's 1e-8; closes the whole global-constraint class, independently of k02's 1e5 magnitude miss |
| **T4** | **Vanishing background gradient.** The MOND invariant Y = q^{μν}∂_μφ∂_νφ is identically 0 on a homogeneous background, so the MOND sector hands a boundary/horizon term nothing but J(0) — which T1 has already shown is pure Λ. | explains *why* L3's Q9 (GHY) and Q10 (Brown–York) both returned functions of Z̃ alone |
| **T5** | **Integer powers.** Every polynomial curvature scalar on de Sitter is Λⁿ, an even power of mass; a₀ needs an odd power. Excludes anomaly-induced and curvature-invariant routes. | R = 4Λ, R_{μν}R^{μν} = 4Λ², C² = 0, … enumerated |
| **T6** | **No propagating modes.** A 3-form in D = 4 has C(D−2,p) = C(2,3) = **0** polarisations, so the flux stiffness receives no loop correction from its own sector and cannot flow to a fixed point. *Caveat, stated: matter loops could renormalise Z̃ if the four-form couples to charged matter — not computed here.* | photon check C(2,1) = 2 |

---

## 3. The exclusion matrix

| structure | status |
|---|---|
| S1 local action, a₀ a Lagrangian constant | **EXCLUDED** by T1 |
| S2 conserved flux / four-form (k04, L3) | **EXCLUDED** by T2 |
| S3 global 4-volume constraint (sequestering) | **EXCLUDED** by T3 |
| S4 boundary / GHY / Brown–York | **EXCLUDED** by T4 |
| S5 anomaly / curvature invariants | **EXCLUDED** by T5 |
| S6 RG fixed point of the flux stiffness | **EXCLUDED** by T6 (with the matter-loop caveat) |
| S7 unimodular / two-measure | **weakly excluded**: the equations are invariant in *form*; C reappears as an **integration constant** — initial data, not a prediction |
| **S8 horizon thermodynamics (identification)** | **OPEN** — but an *identification*, not a derivation from field equations; κ = √(8π/3)/(2π) = 0.4607, and k03 shows it degenerate with the H₀ tension to 0.2% |
| **S9 dimensional transmutation, two condensates in one strongly coupled sector** | **OPEN** — satisfies N2 and N3 by construction; κ becomes a non-perturbatively computable ratio of two condensates. Never attempted in this corpus |
| **S10 nonlinear realisation / coset (Goldstone)** | **OPEN** — the only enumerated structure that could supply **N4**: in a coset construction the linear coupling and the quadratic stiffness of the same order parameter both descend from one breaking scale, making β/√Z̃ group-theoretic. Never attempted in this corpus |

Also flagged open by L3 and not closed here: **a membrane whose charge or tension itself depends
on a₀**. L32 sharpens what that would have to do — it must break the μ-map, i.e. make e or T
depend on β at fixed Z̃.

---

## 4. The coefficient

- Combined measurement: **κ = 0.530 ± 0.037** (BTFR and distance-free are 0.98σ apart, so
  combining is legitimate). 3σ statistical band **[0.418, 0.642]**.
- κ_meas ∝ 1/H₀ at fixed Ω_Λ: Planck → SH0ES moves it by **−7.7%**. Total comparison
  uncertainty **8.0%**; 3σ band with the convention **[0.402, 0.658]**.
- **Numerology guard (D3).** Of a catalogue of 71 principle-shaped numbers (all reduced p/q with
  q ≤ 12, plus 26 named π/e/φ/√ forms), **27 lie inside the 3σ statistical band** — including
  3/7, e/2π, 4/9, 5/11, 0.4607, 3/2π, ½, √2/e, π/6, e/5, 6/11, 5/9, √5/4, 1/√π, π/2−1, 4/7,
  1/√3, … **Landing in the band is not evidence.** Only the derivation can be evidence. Quote
  the derivation, never the proximity.
- After canonical normalisation, κ/√2 = 0.354 is an ordinary dimensionless coupling of order
  unity. The structures known to *fix* a dimensionless coupling are enumerable: a **gauge charge**
  (integer) — closed for this sector by L3 (β multiplies the field strength, not the potential;
  a 2-brane in D = 4 has no magnetic partner); a **WZW level** (integer); an **index/anomaly
  coefficient** (rational / 16π²); a **coset normalisation** (group-theoretic). The last three
  have not been tried.

---

## 5. The checklist, for running any future candidate

**To derive κ, a theory must exhibit:**

1. **X** — an order parameter, non-vanishing and dynamically determined on a homogeneous
   isotropic background, with ρ_vac ∝ X² and a₀ ∝ X (N2). *A gradient invariant of a scalar
   fails: it is identically zero on FLRW.*
2. **The LOCK** — d ln a₀ = ½ d ln Λ along every free-parameter direction (N3).
3. **The RIGIDITY relation Z̃ = λβ²** with λ a pure number fixed by discrete or structural data
   (N4). Everything else in the problem reduces to this one statement: **κ = √(2/λ)**, and
   λ = 8 is κ = ½.
4. **No additive freedom** in the MOND function (N5), and a stated answer to **what a₀ tracks**
   (N7).
5. **A prediction stated with its H₀ convention**, plus at least one *other* prediction, because
   the κ band is not discriminating (N6).

**Excluded:** S1 by T1; S2 by T2; S3 by T3; S4 by T4; S5 by T5; S6 by T6; S7 relocates the
freedom into an integration constant.

**Remain open:** S8 (horizon identification — but not a derivation, and unresolvable at 8%),
S9 (dimensional transmutation with two condensates), S10 (coset / nonlinear realisation), and
L3's a₀-dependent membrane.

---

## 6. Verdict

The problem has a shape now: **either a₀ is a constant of the Lagrangian, in which case the
additive constant of its primitive is exactly degenerate with Λ (T1, proved generically here,
with k01 recovered as the special case) and no equation can compute κ; or a₀ is promoted to a
dynamical order parameter whose square is the vacuum energy — which A4 shows is the only way to
get the half power of Λ — in which case the *form* becomes structural, the amplitude cancels,
and κ collapses to one dimensionless number, the canonically normalised coupling β/√Z̃ = κ/√2.**
Deriving κ is therefore *exactly* the problem of fixing that one coupling, and four further
routes to it are closed here in general form: global averages (T3), boundary and horizon terms
(T4), anomalies and curvature invariants (T5), RG flow of the flux stiffness (T6). What is left
is a short, named list — a WZW level, an index, a coset normalisation, or a two-condensate
transmutation — none of which this corpus has ever tried, which converts an open-ended search
into a bounded one.

Two honest limits on all of it. The search is bounded, not finished: N3 is a condition a theory
must meet, not a fact established about nature, so "a₀ and Λ are independent constants that
coincide" remains live. And even a successful derivation would be nearly untestable on the
coefficient alone — 27 simple numbers sit inside the 3σ band and the H₀ convention moves κ by
7.7% — which is why the programme's registered a₀(z) measurement, not κ, is the discriminating
observable.
