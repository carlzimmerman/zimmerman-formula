# ALL-FRONTS FRAMEWORK-INTERNAL PUSH — 2026-06-26 (LOCAL, do NOT git-push)

AXIOM (held throughout): inertia = nonlocal-in-time response to the de Sitter cosmic-horizon
Unruh bath. Deser-Levin T(a) = (ħ/2π k_B c)·√(a²+(cH_Λ)²). a₀ = (c/2)√(G ρ_DE) = cH_Λ/Z = 9.36e-11,
Z = 2√(8π/3) = 5.789. Framework's OWN interpolation μ_fw(x) = (√(1+4x²)−1)/(2x); μ_fw(1) = 1/φ = 0.618
(golden ratio, exact). Footing a₀ = 9.36e-11, framework's own interpolation, NEVER McGaugh ν. No
comparison to anyone — every result below is framework-INTERNAL consistency/derivation, NOT a
data-confirmation. SM walled (not a TOE); Z a posit; a₀/κ NOT derived (quarantine held).

Scripts: opus_48_extended_research/reviews/mi_kernel_bath/{theta_from_bath.py, theta_finite_y.py,
stress_test.py}; scratchpad/{front2_allepochs.py, phi_front3.py, front4.py}.

---

## LEAD RESULT — FRONT 1: the memory kernel θ(y) is now PARTIALLY FORCED by the bath (was FREE)

**LANDED: PLAUSIBLE** (with a FORCED core and a flagged ansatz).

This is the biggest framework-internal advance of the push. θ(y), y = ω_ext/ω_internal, sits INSIDE
the inertia argument A(ω_in) = a_in + a_ex·θ(y). It was a FREE function — every relational
(dwarf/cluster) prediction carried a factor-~2 uncertainty. The bath now PARTIALLY FORCES it.

**The naive attempt FAILED (recorded honestly).** The "ratio of bath spectral response at ω_ex vs
ω_in" ansatz gives θ(0) = tanh(Ω)/Ω with Ω = ω_in/H_Λ ~ 1e2–1e5 for every bound system → θ(0) → 0,
which contradicts the static EFE (needs finite O(1) θ(0)). This reproduced the prior workflow's
"opposite adiabatic limits" obstruction quantitatively. Negative result, kept on the record.

**The CORRECT derivation (FORCED pieces):**
- **θ(0) FINITE and O(1).** Equivalence principle in the bath frame: a static (DC) external
  acceleration is just part of the proper acceleration that sets T_eff. sympy O(a_ex) matching of
  √((a_in+θ₀·a_ex)²+a_dS²) to the actual √(|a_in+a_ex|²+a_dS²) gives the physical DC weight = 1
  EXACTLY. The EFE-normalized θ(0) = (DC weight)/(weight at y=1).
- **θ(1) = 1 automatic**, the −3dB corner = the internal orbital clock (the only fast clock between
  the Hubble-slow bath and ω_in).
- **The −3dB theorem pins θ(0) to the CLOSED interval [√2, 2] = [1.414, 2.000].** Power reading
  (inertia ~ a²) → θ(1)/θ(0) = 1/2 → θ(0) = 2; amplitude reading (inertia ~ a, Milgrom's A is
  degree-1) → 1/√2 → θ(0) = √2. Narrowed from Milgrom's open "a few."
- **Large-y tail y⁻² or steeper** (finite bandwidth; single-pole gives exactly 1/y², 1/y² = slowest
  allowed = an upper bound).
- **First-order-memory kernel θ(y) = 2/(1+y²)** instantiates all of it: θ(0)=2, θ(1)=1, ~2/y² tail.

**The dwarf/cluster relational profile is now a DERIVED SHAPE, not a free factor-2.** With the
bath-forced θ(y): peak dispersion boost over the plunging band y~0.4–0.7 is **+14 to +25%** (the
softer √2 endpoint gives ~+17%, the firm 2-endpoint up to ~+37% at very small y), **exact
ZERO-crossing at y=1**, and **SUPPRESSION (negative) for y>1**. The banked "+19–28% factor-2
uncertainty" collapses to a specific profile: the **SIGN, the y=1 crossing, and the ~+15–20% scale
are bath-FORCED.** The +19–28% now sits at y~0.4–0.55.

**It dissolves the prior workflow's two structural "kills"** by re-reading them as consistency
checks: (1) "analytic memory / no √(adot)" — θ is the smooth EFE WEIGHT; the MOND non-analyticity
lives in μ_fw OUTSIDE the kernel. (2) "nonlocal correction vanishes as adot→0" — that IS θ saturating
to its DC plateau θ(0), not an obstruction.

**HONEST (why PLAUSIBLE not FORCED):** (1) "internal orbit = the bath's averaging bandwidth" is
structurally motivated (no third frequency exists) but is a linear-response/Kubo MODELING choice, not
a first-principles QFT derivation — the corner's EXISTENCE near y=1 is forced, its precise O(1)
location is not. (2) The exact kernel SHAPE (Lorentzian vs Gaussian vs higher-order memory) is NOT
fixed — only the endpoints [√2,2], θ(1)=1, monotonicity, and the y⁻² tail-bound are pinned; an
infinite family still fits. (3) The within-interval value (√2 vs 2) is the SAME power-vs-amplitude
response→inertia ambiguity that leaves a₀/κ un-derived (Op1/Op2 in the repo) — inherited, not newly
closed. **QUARANTINE HELD:** θ lives inside A, a₀ sits outside in μ_fw[A/a₀], so a pinned θ does NOT
derive a₀. The +14–25% profile is a PREDICTION awaiting ELT-era resolved cluster-member σ (~2030s),
NOT a measurement.

**Delta vs the 2026-06-19 prior verdict** ("PARTIALLY-CONSTRAINED, θ(0) in [1,~e], shape free"):
this NARROWS θ(0) to [√2,2], ADDS a forced y⁻² tail-bound and a forced relational PROFILE with a
sign/zero-crossing, and reframes the two prior obstructions as non-kills. A real but modest firming
of the quasi-static + leading-y piece; the full covariant kernel still postulated.

---

## FRONT 2 — ALL-EPOCHS a₀(z), evolving-DE (DESI CPL) declining branch

**LANDED: PLAUSIBLE** (FORCED core for the safety verdicts, PLAUSIBLE for the new structure claim).

a₀(z)/a₀_0 by epoch (DESI CPL w0=−0.752, wa=−0.86, ρ_DE(a)/ρ0 = a^{−3(1+w0+wa)}·exp{−3wa(1−a)}):
today=1.000; **bump z=0.405 = 1.062** (banked +6% non-monotonic peak, reproduced from the w=−1
crossing); z=2 = 0.862; z=10 = 0.358; **recombination z=1089 = 0.00591** (a₀_rec = 5.53e-13);
BBN z=1e9 = 1.99e-8 (a₀_bbn = 1.86e-18).

- **(a) RECOMBINATION CMB-safe-on-evolving-branch = FORCED.** ρ_DE declines as ~a^1.836, so a₀(z_rec)
  is **~169× SMALLER than today.** Acoustic fluid accel at peaks 1–5 = 2.3e-9..1.2e-8 m/s²; ratio
  a_fluid/a₀(z_rec) ~ 4e3..2e4 → μ_fw → 1, fractional boost 1e-4..2e-5. The evolving branch shifts
  recombination ~169× DEEPER-Newtonian than the flat branch (where it was ~1–2%). Evolving a₀(z)
  makes the CMB MORE safe, not less. (The acoustic estimate is a heuristic single-acceleration
  c_s²k·δ argument, NOT a CLASS/CAMB run — the deep-Newtonian verdict is forced by the 3–4 order
  margin, but a precise power-spectrum number is not computed here.)
- **(b) BBN-safe = FORCED.** a₀_bbn = 1.86e-18; every dynamical/expansion accel (cH ~ 6.3e6) exceeds
  it by ~25 orders. μ_fw = 1 to machine precision. Evolving a₀ makes it MORE so.
- **(c-i) compact JWST halos deep-Newtonian = banked/FORCED.** Σ_M(z) = a₀(z)/(2πG) DECLINES with z
  (107→38 M⊙/pc² by z=10), so compact high-z galaxies sit EVEN MORE securely Newtonian.
- **(c-ii) NEW structure-growth result = PLAUSIBLE.** The linear deep-MOND collapse-boost scale
  R_c(z) (below which g_N < a₀(z)) scales as a₀(z) and **SHRINKS ~3× by z=10** (R_c~a0(z) forced;
  the structure-asset reading uses a linear-collapse heuristic, the Nusser overproduction connection
  is qualitative, below detectability). Direction: LESS deep-MOND boost to early structure =
  RIGHT-SIGNED against MOND's known overproduction problem. A mild internal asset, not a liability.
- **FAR-FUTURE surprise = FORCED-given-wa<0, observationally moot.** With wa<0, w(a→∞) = w0+wa =
  −1.612 is PHANTOM, so ρ_DE grows without bound and **a₀(z) DIVERGES (Big-Rip-like)** — the
  declining branch is NOT monotonic-to-zero; it declines into the past, diverges into the far future.

Net: on the evolving declining branch, every early-universe front is MORE safe, and the one new
high-z structure consequence is mild and right-signed. Framework-internal; Z a posit; not data-confirmed.

---

## FRONT 3 — φ / golden-ratio structure

**LANDED: PLAUSIBLE — an ELEGANT ONE-OFF, not a recurring pattern. Say so honestly.**

- μ_fw(1) = 1/φ EXACTLY (sympy: −1/2 + √5/2). Confirmed.
- **The real structural finding: an EXACT general identity 1/μ_fw(x) − μ_fw(x) = 1/x** (sympy:
  simplifies to 0). At x=1 this becomes 1/μ − μ = 1 = the golden-ratio defining recurrence
  (φ − 1/φ = 1). So φ at x=1 is the x=1 SLICE of a forced one-parameter identity, WITH A REASON: the
  defining quadratic x·m² + m − x = 0 is coefficient-symmetric (same x on the m² and constant terms),
  so at x=1 it collapses to m²+m−1=0 = the golden equation. x=1 is the UNIQUE point where 1+4x² = 5.
- **NOT recurring, NOT structural elsewhere:** Z, 1/Z, √(2/Z)=0.5878 carry π and √(8/3) but NO √5 —
  no exact φ, no near-miss within 1%. μ_fw at x=φ, 1/φ, 2, 1/2 → none are clean φ-values (surds are
  √(7±2√5), √17). No nonzero fixed point (μ(x*)=x* → x*³=0 → only x*=0); iterating μ from x=1 → 0
  monotonically, no φ-cycle; μ(μ(1)) = 0.4773 ≠ 1/φ².
- **BH near-misses are COINCIDENCES, not structure:** x_ISCO = Z/9 = 0.6432 is 4.07% from 1/φ; r_cross
  = √Z = 2.406 is 8.1% from φ². Both contain π (transcendental) while φ is algebraic → no possible
  identity. μ_fw at those points (0.489, 0.814) is not clean.

So φ is genuine and forced AT x=a₀ (the a=a₀ point), elegantly tied to the coefficient-symmetry of
the framework's own interpolation quadratic — but it is an isolated slice, not a multi-point
self-similar architecture. Honest: elegant one-off.

---

## FRONT 4 — BH-interior inertia coherence check

**LANDED: PARTIAL (a clean framework-internal coherence/consistency check, no new test).**

The question: is "inertia" even DEFINED inside a black hole, given the bath axiom?

- **(a) SIGN result (mass-independent, sympy-clean).** Exterior universe radicand a² + (cH_Λ)² is
  ALWAYS > 0 → inertia ALWAYS real, even at a=0 (the dS floor T_dS = ħH_Λ/2πk_B = 2.2e-30 K).
  **Positive Λ is exactly what guarantees a real bath at every a.** Interior (timelike-r,
  contracting, Λ_eff<0-like) radicand a² − (c·H_eff)² → **T(a) IMAGINARY for any proper acceleration
  a < c·H_eff_interior** → a detector at rest inside has NO real bath. Framework-internally, inertia
  as a bath response is **not well-defined inside the horizon** for sub-critical acceleration — a
  coherent statement, not a pathology: the framework only claims an inertia bath where the de Sitter
  (Λ>0) structure holds, i.e. the exterior expanding universe.
- **(b) Two-horizon quadrature.** Per-horizon surface gravities (Sgr A*, M87*, 10 M⊙) give a BH
  Hawking-bath term 12–21 orders larger than (cH_Λ)² in the radicand → the BH bath dominates the
  cosmic floor by ~15.8 orders for a STATIC observer. BUT for a real bound ORBIT the relevant 'a' is
  the orbit's own proper acceleration g ~ GM/r² (>> both cH_Λ and, for r<r_cross, a₀_BH), so the
  bath is orbital-a-dominated and the cosmic floor is negligible. A second horizon-bath only matters
  for a static observer held near the horizon — the non-geodesic, MHD-swamped accretion-plasma case.

Net: the bath axiom is internally COHERENT about its own domain — real inertia exactly where Λ>0
(exterior), undefined sub-critically inside, BH-bath-dominated only for static near-horizon
observers. No new falsifiable test; a consistency check that the framework does not over-claim.

---

## WHAT TO TELL CARL (straight)

The headline is FRONT 1. The dS-Unruh bath PARTIALLY DERIVES the memory kernel θ(y) that was a free
function — and that genuinely removes most of the factor-2 from your relational dwarf/cluster
predictions. The bath FORCES: θ(0) finite and O(1) in [√2, 2] (equivalence-principle DC weight = 1
plus the −3dB theorem), θ(1)=1, monotone with a corner at y=1, a y⁻² (or steeper) tail, and — most
usefully — a SPECIFIC dwarf/cluster profile: dispersion boost +14 to +25% over the plunging band
y~0.4–0.7, exactly ZERO at y=1, suppression beyond. The sign, the y=1 crossing, and the ~+15–20%
scale are now bath-forced, not free. It also dissolves the two prior "kills" by re-reading them as
consistency checks. This is a real, modest firming — PLAUSIBLE, because the load-bearing "internal
orbit sets the bandwidth" step is a motivated Kubo modeling choice, not a full QFT derivation, and
the exact kernel shape is still an ansatz.

The other three: all-epochs a₀(z) on the DESI evolving branch makes the CMB ~169× MORE Newtonian-safe
than the flat branch and gives a mild right-signed reduction of early MOND structure boost (plus a
far-future divergence, moot). The φ result is a genuine, elegant ONE-OFF — μ_fw(1)=1/φ is the x=1
slice of an exact identity 1/μ−μ=1/x forced by your interpolation's coefficient symmetry — but it
does NOT recur and is not a hidden architecture (the BH near-misses are π-vs-√5 coincidences). The
BH-interior check is clean: your bath gives real inertia exactly where Λ>0 and is undefined
sub-critically inside the horizon — coherent, no over-claim.

Quarantine intact across all four: a₀/Z/κ NOT derived (a pinned θ lives inside A, a₀ sits outside in
μ_fw), SM still walled (not a TOE), Z still a posit. Every result here is framework-internal
consistency/derivation, NOT data-confirmation. Open doors remain — the full covariant kernel is still
postulated, and the +14–25% profile is an ELT-era prediction awaiting resolved cluster-member σ.
