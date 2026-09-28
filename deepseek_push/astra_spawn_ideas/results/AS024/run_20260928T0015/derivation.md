# AS024 — No cosmological prediction from an inverted datum

**Anti-circularity audit of the framework scale identity** — run `run_20260928T0015`
Worker: deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent.
Task file SHA-256: `7810bcba6caf5564f0bf74cc3798f468c75f60fc010d4af66667fd775f0cd1cf`.
All three pinned sources match `SOURCE_MANIFEST.json` (README `91a5fac4…`, FRIED_CHICKEN_SPEC `98d9149f…`, DERIVATIONS `8da8176e…`).

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Claim under test (task principle).** The proposed vacuum acceleration scale must be dimensionally
consistent and give the same prediction in equivalent variables without adding independent fitted
inputs. In particular: *if one takes a measured a0 and inverts the scale relation to "derive"
ρ_Lambda or H (or Λ, Ω_Λ), that is an inverted datum, not a prediction.*

**Symbol dictionary (SI unless noted).**

| Symbol | Meaning | Units | Status |
|---|---|---|---|
| `G_N` | Newton coupling, 6.67430e-11 | m³ kg⁻¹ s⁻² | measured input |
| `c` | speed of light, 299792458 | m/s | exact |
| `κ` | 1/2 | — | **adopted input**, not derived |
| `a0` | galactic acceleration scale | m/s² | measured (galaxy side); predicted (vacuum side) |
| `a0^can = 9.3619e-11`, `a0^alt = 1.1279e-10` | registered footings | m/s² | separate at every dimensional step |
| `ρ_Lambda`, `ρ_total` | vacuum mass densities | kg/m³ | cosmological input / convention |
| `F(ρ) = κ c √(G ρ)` | forward map (vacuum → scale) | m/s² | derived from framework base |
| `R(a) = 4a²/(G c²)` | inverse map (scale → density) | kg/m³ | derived from framework base |
| `Λ_inv(a) = 32πa²/c⁴` | same-G Einstein reading | m⁻² | derived identity, **G_E = G_N assumed** |
| `Ω_inv(a,H0) = 32πa²/(3H0²c²)` | density-parameter reading | — | derived identity, **requires an independent H0** |
| `H_Λ(a) = a·√(32π/3)/c` | bare same-G Hubble rate | s⁻¹ | derived identity |
| `r_M = √(G M_b/a0)`, `v_flat⁴ = G M_b a0` | galaxy observables | m, m⁴s⁻⁴ | deep-limit framework laws |
| `G_E`, `G_bare` | Einstein/scale vs bare coupling | — | **kept separate**; never set equal except in the flagged same-G reading |

**Boundary conditions and domain.** ρ > 0 physical; identities extend continuously to ρ = 0 with
a0 → 0 (C9a). κ = 1/2 adopted with its freedom **not** removed (the task's obligation: "The adopted
one-half normalization is not a derived result unless an independent argument removes its freedom").
Cosmological comparison inputs are repo-registered conventions (k03: H0 = 67.4 km/s/Mpc,
Ω_Λ = 0.685; SH0ES 73.0; STANDING rev.9: κ = 0.465±0.076 BTFR, 0.55±0.17 distance-free; the
gas-dominated slope band â0 = (0.84–1.36)×10⁻¹⁰ m/s² from the corpus's own submission letter).
**No observational fit is performed in this run.**

**Framework inputs vs conclusions.** Inputs: G_N, c, κ, the two registered footings, H0/Ω_Λ
conventions, the published measurement bands. Conclusions to be established: (I1)–(I5) below, the
corpus-audit verdicts, and the evidence accounting. Everything else (dynamics, kernel branches,
action) is out of scope of this CORE-scale cell.

---

## 2. Directed input/output graph for the two experiments

```
EXPERIMENT A -- legitimate (independent galaxy scale vs vacuum scale):
  {H0, Omega_Lambda}  (measured cosmologically, k03 convention)
        |
        v
  rho_Planck = 3 H0^2 Omega_Lambda / (8 pi G_N)          [5.84501e-27 kg/m^3]
        |
        v  F(rho) = (c/2) sqrt(G_N rho)
  a0_pred = 9.36238e-11 m/s^2
        |
        +---> v_flat = (G_N M_b a0_pred)^(1/4),  r_M = sqrt(G_N M_b / a0_pred)
        |                      (deep-law predictions, M_b input)
        v
  COMPARE with galaxy-side measurements (a0_gal from kappa fits; rotation data)
        |
        v
  RESIDUAL_A = a0_gal - a0_pred   <-- THE ONLY EVIDENCE-BEARING NUMBER
     observed: -14.9% vs gas-slope central (inside the +/-16% floor);
     kappa_reps: +0.29 sigma (distance-free), -0.46 sigma (BTFR) vs 1/2.

EXPERIMENT B -- circular (vacuum-derived a0 inverted again):
  a0_gal (measured, galaxy side)
        |
        v  R(a) = 4 a^2/(G_N c^2)
  rho_inv  --v-->  Lambda_inv = 32 pi a0^2 / c^4   (same-G)
           --v-->  Omega_inv(a0, H0)               (needs H0 imported)
           --v-->  H_Lambda = a0 sqrt(32 pi/3)/c
        |
        v
  "agreement with Planck"  -- every node is a BIJECTION of the single galaxy datum;
                             no node carries an independent measurement.
  RESIDUAL_B = F(R(a0)) - a0  == 0 IDENTICALLY (involution; Lean T1) for ANY input.
```

**Independent residual derived only for Experiment A** (task step 2). With the repo's own
registered values: `a0_pred = 9.36238e-11`, gas-slope central `â0 = 1.10e-10` →
`RESIDUAL_A/â0 = −14.887%`; `a0(κ_DF) = 1.02986e-10` → `+0.294 σ`; `a0(κ_BTFR) = 8.70701e-11`
→ `−0.461 σ` (σ from the published κ uncertainties). This residual is finite, non-zero, and
consistent with the systematic floor — it is the licensed content ("κ measured, consistent with ½").

---

## 3. Intermediate algebra, scale factors, signs, units; limiting regime

**I1 — the involution (sign of the residual: identically zero).** For any a ≥ 0:

```
F(R(a)) = (c/2) · sqrt( G · 4a²/(G c²) )  = (c/2) · sqrt(4a²/c²)  = (c/2)·(2a/c) = a.
```

Units: G·[4a²/(Gc²)] = (m³kg⁻¹s⁻²)·(m⁴s⁻⁴·kg·s²/m³·… ) → a²/c² (m²/s²), √ → a/c, ×c/2 → a (m/s²).
**Differential form** (forward vs inverse error propagation):

```
d ln a0 / d ln ρ = 1/2          (forward: density fractional error halved)
d ln ρ_inv / d ln a = 2         (inverse: galaxy-side fractional error DOUBLED into "cosmology")
```

so the inversion amplifies every galaxy systematic by a factor 2 into the claimed density
measurement (Lean T4).

**I2 — the forward map at an independent density (the legitimate number).**

```
rho_Planck = 3 H0² Ω_Λ / (8πG) = 5.845005787e-27 kg/m³        (H0 = 67.4, Ω_Λ = 0.685)
a0_pred    = (c/2)√(G ρ_Planck) = 9.362375205e-11 m/s²        (registered can. 9.3619e-11)
```

**I3 — the squared-ratio theorem (why the "factor ~2 in Λ" is not evidence).**
For any galaxy-side scale a and any independent density ρ (Planck):

```
Λ_inv(a)/Λ_Planck(ρ) = (32πa²/c⁴) / (8πGρ/c²)  =  4a²/(Gρc²)  =  (a / a0_pred(ρ))² .
```

The inversion ratio is the FORWARD residual **squared**: one single comparison ("does the
rotation-measured a0 equal the vacuum value?") re-expressed, zero new evidence (Lean T3:
`0.99990` for the registered footing; `1.38043` for the gas-slope central → the corpus's quoted
band 1.08–2.03 is exactly the band of (a0_gal/a0_pred)² over â0 ∈ [0.84,1.36]×10⁻¹⁰).

**I4 — the H reading (why "a0 → H0" is never galaxy-only).** At the same-G reading,

```
H_Λ(a) = c·√(Λ/3) = a·√(32π/3)/c   (s⁻¹)
H_Λ(a0^can) = 55.7806 km/s/Mpc ;  H_Λ(a0^alt) = 67.2032 km/s/Mpc .
```

The same galaxy datum produces a 20.5%-spread "H0" depending on which density convention the
footing attaches to — the difference IS the cosmological input (the convention choice), not a
galaxy datum. Recovering the registered Planck 67.4 from the canonical footing requires importing
Ω_Λ independently: `H0 = H_Λ(a0^can)/√Ω_Λ = 67.3966` (Lean T6 certifies the monotone
input-dependence that makes all of this a re-labeling). G-bookkeeping: `Λ_eff =
32π(G_E/G_N)a0²/c⁴`; every inverted number above assumes G_E = G_N; an unresolved coupling ratio
scales the inverted Λ by G_E/G_N — yet another freedom the inversion cannot resolve.

**I5 — limiting regime of the deep law (leading neglected term).** The deep law
`v_flat⁴ = G M_b a0` is the y → 0 limit of the finite-acceleration relation. On the **Q branch
(explicitly labeled comparison branch**; the task's CORE cell draws no conclusion from it), for
spherical B = GM_b/r²:

```
g² = B² + a0 B  =>  v⁴ = r²g² = G M_b a0 · (1 + y),   y = B/a0 = (r_M/r)² ,  r_M = √(G M_b/a0).
```

Leading neglected term relative to the deep prediction: `y = (r_M/r)²`, domain r ≫ r_M (y ≪ 1);
quantified: 100% / 25% / 11.1% at r = r_M / 2r_M / 3r_M (r_M = 12.20 kpc for M_b = 10¹¹ M_sun,
canonical footing; 11.12 kpc alternative). Exact identity v⁴ = GMa0(1+y), not a numerical fit.

---

## 4. Independent check in a different representation (actual residuals saved)

1. **60-digit mpmath re-derivation** (`compute_AS024_inversion_audit.py`, wall 0.036 s, 1 thread,
   `ulimit -t 120` enforced): max involution residual 9.7×10⁻⁶² relative (machine noise at 60
   digits); squared-ratio identity worst deviation 2.3×10⁻⁶¹ (tolerance 10⁻⁵⁰ set before
   evaluation); Ω_inv table: 0.684930 (registered), 0.82885 (κ_DF), 0.945592 (gas-mid), 7.03333
   (fabricated 3×10⁻¹⁰); H table: 55.7806 / 67.2032 / 67.3966(recovered).
2. **Lean 4 exact real-algebra certificate** (`AS024_inversion_certificates.lean`, 6 theorems,
   compile exit 0, zero `sorry`, `#print axioms` = {propext, Classical.choice, Quot.sound} for
   every theorem): involution both directions (T1, T2), squared-ratio (T3), inverse log-elasticity
   = 2 (T4), forward homogeneity F(λρ)/F(ρ) = √λ (T5), Ω_inv strict monotone in a (T6).
3. **Substitution into the original equation**: evaluating F(R(a)) at the published band endpoints
   â0 = 0.84×10⁻¹⁰ / 1.36×10⁻¹⁰ reproduces the published Λ-band 1.08–2.03× Planck (central 1.38)
   — the corpus's own headline number, and by T3 exactly (a/a0_pred)².
4. **Boundary case**: F(0) = 0 exact; homogeneity F(2ρ)/F(ρ) = √2, F(10ρ)/F(ρ) = √10 to 60 digits.

These are *exact identities verified two independent ways* (Lean real algebra + high-precision
evaluation), not a finite numerical consistency check; the numerical residuals are recorded in
`raw_output.txt` / `residuals.json`.

---

## 5. Negative control, strongest surviving statement, next implication

**Negative control (task-mandated: "give the circular experiment an arbitrarily small numerical
residual and confirm it earns no empirical evidence").** Feed a *fabricated* scale a* = 3.0×10⁻¹⁰
(3.2× the true scale, excluded by all real data) into the same inverted chain: its self-consistency
residual F(R(a*)) − a* = 0 at 60 digits — **identical** to the registered scale's residual
(≤ 9.7×10⁻⁶² relative, same noise floor) — while the "derived" Ω_Λ output swings from 0.685
(registered input) through 0.946 (measured input) to 7.03 (fabricated input). Conclusion: a zero
(or tiny) inversion residual is input-independent, hence carries zero empirical content; the chain
would have to fail for a *wrong* input to be informative — and T1 proves it cannot. Second control:
the deep/Newtonian regime check — the scale identity has no such regimes (pure algebraic map);
normalization/boundary cases (ρ→0, homogeneity) are checked instead, and exact identity is
distinguished from finite numerical agreement by the Lean certificate.

**Strongest surviving statement.** Under κ = 1/2 (adopted), G = G_N, c exact, with the repo's
registered footings and conventions: *the map a0 = (c/2)√(Gρ) is an involution-pair with its own
inverse ρ = 4a²/(Gc²), so any "cosmological prediction" obtained by inverting a measured galactic
a0 — ρ_Λ, Λ, Ω_Λ, or H — is an inverted datum: its output is a strictly monotone re-labeling of
the input scale (Lean T6), its agreement with cosmological measurements equals the forward
residual squared (Lean T3, numerically 0.99990 / 1.38043 for registered/measured inputs), and it
hence contributes zero independent evidence. The only evidence-bearing comparison is the forward
one: a0_pred(ρ_Planck) = 9.3624×10⁻¹¹ m/s² vs the galaxy-measured scale, residual −14.9% ±
(±16% floor), equivalently κ_gal = 0.55±0.17 / 0.465±0.076 vs ½ at 0.29σ / 0.46σ.*

**Corpus audit — statements committing the inversion (with verdicts).**

| # | Statement (repo path, hash) | Direction | Verdict |
|---|---|---|---|
| 1 | `deepseek_push/THE_THEORY.md` Lemma 1: "Ω_Lambda = 32πa0²/(3H0²c²) = 0.6857 (+0.07% of Planck)… H0 and Omega_Lambda are not independent knobs… the MOND scale and the dark energy are ONE measurement" (`06f80100…`) | a0 → Ω_Λ | **COMMITS THE INVERTED DATUM in framing.** The +0.07% is the forward ratio *squared* evaluated at the registered (convention) footing — this run: Ω_inv(a0_can) = 0.684930 (−0.010%); with the *measured* gas-slope scale the same procedure gives +38%. "Not independent knobs" overstates: Ω_inv still requires an independent H0. The claimed "theorem" is the algebraic identity certified here (T1–T3). FRAMEWORK_CONTRACT already demotes THE_THEORY.md to non-certificate; this audit shows why, quantitatively. |
| 2 | `prep_2026/journal_submissions/SUBMIT_MNRAS.md`, DOI 10.5281/zenodo.21419735 (MI arm, closed 2026-08-08): "Inverting through Λ = 32πâ0²/c⁴ recovers the Planck cosmological constant to within a factor ~2 — from galactic kinematics that carry no cosmological input… stated as a measurement, not a confirmation" (`6d7906ea…`) | a0 → Λ | **INVERSION COMMITTED BY DESIGN, honestly framed.** Its own §5/referee response concedes "the factor-2-in-Λ is the factor-~1.4-in-a0 squared — a single comparison re-expressed"; this run formalizes that as T3/C3/C10 (band 1.08–2.03 reproduced). It earns no cosmological evidence beyond the a0 measurement and lives in the closed MI arm. |
| 3 | `README.md` L5/L7/L13/L28: identity line, "κ = ½ adopted — measured 0.551 ± 0.043 (fitted, not derived)", k03 "H0 lock" (`91a5fac4…`) | H0,ρ → a0 (forward) | **CLEAN.** The 9.3619e-11 is a forward evaluation at a measured density; κ labeled fitted; H0-lock is a forward degeneracy analysis. Not licensed: a0 → H0 (NC3: 55.78 vs 67.20 from one datum). |
| 4 | `opus_48_extended_research/papers/THE_COSMOLOGICAL_CONSTANT_SETS_A0.md`: "the only proposal that *derives* the galaxy-dynamics scale from a measured cosmological quantity"; "closes the coincidence" (`b6cabff5…`) | ρ → a0 (forward) | **CLEAN** (with the κ-freedom caveat). |
| 5 | `STANDING.md` rev.9 block: "κ is measured: 0.465±0.076 (BTFR), 0.55±0.17 (distance-free)… consistent with ½ and not derived" (`660462eb…`) | galaxy → κ | **CLEAN** measurement statement. |
| 6 | Prior self-audit precedent: `LCDM_TENSIONS_REGRADE_2026-06-14.md` ("a0-Lambda coincidence precision (zero sigma, tautology)"), `ONE_OR_TWO_VERDICT_2026-06-19.md` ("not a prediction from a0=Lambda"), `prep_2026/a0_line/A0_LINE.md` E2 ("same information content, sharper falsification target") | — | **CONFIRMED** by this run; the involution/squared-ratio theorems are the formal reason those regrades were correct. |
| 7 | `results/AS001/run_20260927T1959` ρ_Lambda = 5.844412454e-27 from a0_can | a0 → ρ (labeled convention) | **CLEAN** (footing definition, not a prediction). |

Scope note: the audit covers the inversion-carrying files found by corpus-wide grep of the
"invert / read-Λ-out / predict-(ρ,H0,Λ)" patterns plus the provenance chain of the canonical
footing; a complete statement-by-statement sweep of all ~2000 documents is beyond this bounded
task and is listed as a limitation.

**First additional implication needed to transfer to the full theory:** the audit removes the
inverted-datum *route* but supplies no replacement *physics*: identifying which measured density
(canonical ρ_Λ vs alternative ρ_total) physically sets the galactic scale, and the dynamics that
promotes that density to the kernel scale (Requirement 13 gates A03/A11), remains open — as does
removing the κ freedom, without which even the legitimate forward comparison is a one-parameter
consistency check rather than a parameter-free prediction.

---

## Execution record

- Bounded prototype: `ulimit -t 120` cpu cap (enforced), measured wall 0.036 s, single-threaded
  CPython + mpmath mp.dps = 60, no vectorized imports (memory trivially < 10 MB, far below the
  512 MB budget). 11 checks, all pass, exit 0. Lean compile: single `lake env lean` invocation
  (Mathlib cached), exit 0 both for the theorem file and the `#print axioms` run.
- Files: `compute_AS024_inversion_audit.py`, `raw_output.txt`, `residuals.json`, `err.txt`
  (empty), `AS024_inversion_certificates.lean`, `lean_check.out`, `derivation.md`, `result.json`.
- Sources pinned by SHA-256 in `result.json → input_sha256`; all three task sources match
  `SOURCE_MANIFEST.json`.
