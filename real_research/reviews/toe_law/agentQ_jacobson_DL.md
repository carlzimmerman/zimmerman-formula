# Agent Q — Jacobson 1995 redone with the Deser–Levin temperature: the H² term propagates NOWHERE in the well-defined reading; the only reading where it survives produces EXACTLY μ_F4 on the WRONG LEG (anti-MOND, total shutoff below cH); the finite-(H/a)² coefficient is provably pure scheme

*agentQ, 2026-06-10. Task: redo the Einstein equation of state (Jacobson, arXiv:gr-qc/9504004 — Clausius
δQ = TδS on local Rindler horizons with T = Unruh a/2π) using instead the Deser–Levin temperature
T_DL = √(a²+H²)/2π (arXiv:gr-qc/9706018; machine-verified on the stationary dS family in
`agentN1_nonhuygens_commutator.md`), carry the full κ_DL at finite a/H, expand in (H/a)², and decide among
three pre-registered outcomes: (i) the correction is a Λ-term (Λ re-derived, no MOND); (ii) the correction is
an acceleration-keyed modified equation of state (sign? form?); (iii) the construction breaks at finite a/H
(say precisely where). This EXTENDS the banked Door-5/horizon-thermodynamics verdict
(`reviews/ESTABLISHED_PATHS_LEDGER.md` + `reviews/clausius_sign_calculation.py`: temperature-modification
route → anti-MOND, decisive) with tonight's substrate — it does not re-litigate it. Artifacts:
`agentQ_jacobson_DL.py` + `.out` (26 sympy machine checks, ALL PASS, including a full-Christoffel covariant
computation of the static-observer acceleration). Units ħ = c = k_B = 1 except SI tables. Verdict at the end,
both ways, full weight.*

## 0. The three pre-registered outcomes (locked before the run)
- **(i)** the (H/a)² correction is exactly a cosmological-constant term → Λ re-derived, no MOND: the null
  result, reported at full weight.
- **(ii)** the correction is acceleration-dependent → characterize sign and form; does it carry the
  MOND/N3 sign (a deficit on the **inertia** side growing toward low a)?
- **(iii)** the construction is ambiguous — the local-Rindler limit a → ∞ is REQUIRED, so finite a/H breaks
  the setup: state exactly where, because that failure mode is itself the sharpest statement of why horizon
  thermodynamics cannot reach MOND.

## 1. Literature check FIRST (is Jacobson-with-DL published?) — pinned, June 2026
Four web-search passes (Jacobson + dS + modified Unruh; DL/GEMS + equation of state; Clausius + MOND +
de Sitter; Cai–Kim lineage). What EXISTS:
- **Jacobson, gr-qc/9504004** — the baseline: T = κ/2π (boost Unruh), δS = ηδA, Einstein with Λ as the
  Bianchi **integration constant**. Error budget of the approximate local boost Killing field made explicit
  in **Guedens–Jacobson–Sarkar, arXiv:1112.6215** (fails Killing's equation at O(x²·Riemann)).
- **Deser & Levin, gr-qc/9706018** (and **Narnhofer–Peter–Thirring, Int. J. Mod. Phys. B10 (1996) 1507**,
  earlier): T_DL = √(a²+H²)/2π for accelerated worldlines in dS — the GEMS result; KMS at κ_DL/2π on the
  full stationary family machine-verified in this repo (agentN1, to 10⁻²⁵).
- **Milgrom, astro-ph/9805346** (Phys. Lett. A 253 (1999) 273): the ΔT = T_DL − T_GH **vacuum-effect
  conjecture** — a worldline/inertia ansatz, NOT a Clausius/horizon derivation; its bath reading is already
  dead in this repo (ephemerides ×54,000; `TOE_TRILEMMA.md` lineage).
- **Ho–Minic–Ng, arXiv:1005.3537** (+ 1201.2365, 1308.3252, 1601.00662): the closest published object —
  dS-Unruh/GEMS-type temperature **inside Verlinde's entropic-force screen route** ("MONDian dark matter" /
  "modified dark matter": CDM ontology with MOND scaling). Different machinery (holographic screen force
  law, not the local-Rindler equation of state), different output (a dark-matter profile, not a modified
  Einstein equation).
- **Cai–Kim, hep-th/0501055**: Clausius at the FRW **apparent horizon** with the horizon-scale temperature
  T = 1/(2πR_A) → Friedmann equations. Horizon temperature, not the worldline DL temperature; no MOND.
- **Padmanabhan** (equipartition 0912.3165; emergence-of-space 1206.4916): dS-horizon T = H/2π variants;
  recover the standard equations.
- **Modified-ENTROPY Jacobson class** (the other thermodynamic dial, NOT touched tonight): Eling–Guedens–
  Jacobson gr-qc/0602001 (f(R), nonequilibrium δS); Pazy 1302.4411; the 2025 entropic-MOND papers
  (2510.14345 "inverse approach", 2511.05632 MCMC-fitted) — all already adjudicated in
  `ESTABLISHED_PATHS_LEDGER.md`; Rényi/finite-heat-capacity modified Unruh thermodynamics 2509.03470
  (emergence of Einstein preserved).

**What does NOT exist (to this search depth): Jacobson's local-Rindler Clausius derivation carried with
T_DL = √(a²+H²)/2π at finite a/H, with the Tolman/normalization analysis and the (H/a)² expansion.** The
in-repo `clausius_sign_calculation.py` (the coarse integrand swap, G_eff = G/W) is itself the closest
existing object. Tonight's calculation is, to our knowledge, the first careful version — stated with the
usual humility of a four-pass search.

## 2. Baseline reproduced (the validation anchor) — `.out` Part A
Boost Killing χ = −κλk on the local Rindler horizon; δQ_χ = −κ∫λT_kk; Raychaudhuri at leading order
θ = −λR_kk ⇒ δA = −∫λR_kk; Clausius with T = κ/2π ⇒ **T_kk = (η/2π)R_kk** for all null k (κ cancels, [A1])
⇒ Einstein, G = 1/4η, **Λ only as the Bianchi integration constant** ([A3]: d(R/2 + f) = 0 ⇒ f = −R/2 + Λ).
Machine-verified side fact used throughout: **g_kk ≡ 0** for null k ([A2], explicit dS static-patch null
vector) — the kk-balance is structurally **Λ-blind**: no temperature substitution can make it "see" Λ.

## 3. The central exact fact: T_DL **is** the Tolman-shifted Gibbons–Hawking temperature — so the H² term cancels IDENTICALLY (reading R1) — `.out` Parts B, C
Full covariant computation in the dS static patch (Christoffels from the metric, no shortcuts, [B1–B2]):
the static observer at radius r has a = H²r/√(1−H²r²), and
> **√(a²+H²) · |ξ| = H exactly** ([B3]), |ξ| = √(1−H²r²), κ_b = H —
i.e. **T_DL = κ_b/(2π|ξ|): the Deser–Levin temperature is nothing but the Tolman blueshift of the
cosmological-horizon temperature.** (In proper-distance form: a(ℓ) = H·cot(Hℓ), κ_DL(ℓ) = H/sin(Hℓ),
[B4a–b].) Consequence, machine-verified ([C1]): the per-observer Clausius ratio
δE_loc/T_DL = (δQ_ξ/|ξ|)·(2π|ξ|/κ_b) = 2πδQ_ξ/κ_b is **observer-independent and H-free in quadrature** —
the √(a²+H²) in the temperature cancels against the Tolman factor of the locally measured heat, **exactly,
at all orders in H/a**. The balance is identical to Jacobson's; Einstein comes out unchanged; Λ stays an
integration constant.

**Jacobson-with-Deser–Levin = Jacobson, identically.** The reason Jacobson's original works at all is that
the Unruh temperature is strictly LINEAR in a — and the DL temperature in exact dS is precisely the unique
Tolman-consistent completion of that linearity, so it adds nothing. This is the sharpest form of the null:
the H² term does not produce a correction; it does not even produce a Λ term (the balance can't see one,
§2); **it propagates nowhere.**

## 4. Reading R2 — the ONLY reading where H survives: the F4 kernel on the WRONG LEG — `.out` Part D
H survives only if one breaks Tolman consistency by hand: take the bookkeeping observer's acceleration from
the **local flat frame** (a = 1/ℓ, the Rindler value) but the temperature from the **DL formula**
√(a²+H²)/2π — the reading implicitly used by the banked coarse calculation. Then the balance acquires
W = κ_DL/a and ([D1]):
> **R_kk = 8πG_eff T_kk, G_eff/G = a/√(a²+H²) = 1 − ½(H/a)² + ⅜(H/a)⁴ − 5/16(H/a)⁶ + …** ([D3])
Three exact identifications ([D2a–c]), all machine-verified:
1. **G_eff/G ≡ μ_F4 = a/κ** — the equation-of-state correction factor is EXACTLY the F4 interpolating
   kernel (the repo's selected effective shape, `TOE_STATUS_AND_DOORS.md`);
2. a/κ = T_Unruh-flat(a)/T_DL(a);
3. a/κ = 2π·dT_DL/da — F4's own susceptibility, normalized.
So Clausius (which consumes **T**) and F4 (which consumes **dT/da**) produce the SAME function by the
algebra of the quadrature — an identity, flagged as such, not a mechanism. But they hang it on opposite
legs of F = ma: F4 puts a/κ on the **inertia** side (m_eff = mμ ⇒ deep-MOND a = √(g_N·H), the observed
enhancement — [D6c]); the Clausius balance puts it on the **gravity** side, where the self-consistent
dynamics a = μ(a)g_N gives ([D6a], sympy-solved):
> **a = √(g_N² − H²) for g_N > cH; for g_N < cH the ONLY solution is a = 0.**
Not gradual weakening — **total shutoff of gravity below g_N = cH ≈ 5.8 a₀**: every galactic disk beyond a
few scale lengths unbinds. Anti-MOND in its most extreme form. And the sign is FORCED in every temperature
reading: T_DL ≥ T_U in quadrature ⇒ W ≥ 1 ⇒ G_eff ≤ G always ([D4]) — heat is worth LESS entropy at low a,
so focusing can only be suppressed. This makes the banked sign verdict exact and structural, and adds the
shape identification: **horizon thermodynamics with the DL temperature "knows" the F4 kernel — and applies
it with the anti-MOND orientation, on the leg Clausius bookkeeping can reach (the source coupling), not the
leg the data wants (inertia).** Numbers ([D5], both footings per the working rule): G_eff/G = 0.71 at
a = cH, 0.170 at a = a₀ (pure-Λ footing, (H/a₀)² = Z² = 33.51; ρ_total footing 33.60 — same regime, the
verdict is footing-independent).

## 5. Outcome (i) does NOT occur — the correction is not a Λ term — `.out` Part E
The R2 correction is 8πG(μ_F4 − 1)T_kk: proportional to **T_kk** (a source-coupling rescaling), vanishing
in vacuum ([E1]) — it can never mimic Λ, which gravitates in vacuum. A genuine Λ-term ∝ g_kk is identically
invisible to the null balance ([A2]). Λ is exactly where Jacobson left it: an undetermined integration
constant, untouched by the temperature substitution. **Horizon thermodynamics in this construction neither
derives nor modifies Λ — it cannot even see it.**

## 6. Outcome (iii), sharpened twice — `.out` Part F
**(a) The (H/a)² coefficient is pure scheme.** Four defensible pairings of (which acceleration, which
redshift weight) for the bookkeeping observer give W = 1 + c·(Hℓ)² with ([F1], all series machine-verified):
> c = **0** (exact-dS DL + exact Tolman weight = R1) · **1/6** (exact-dS a(ℓ) in DL + flat weight) ·
> **1/3** (flat a = 1/ℓ in DL + exact Tolman weight) · **1/2** (flat + flat = R2 = the banked coarse swap).
The construction's OWN neglected terms — the failure of the approximate boost Killing field, O(x²·Riemann)
(gr-qc/9504004; 1112.6215), with Riemann ~ H² in dS — are O((Hℓ)²): **exactly the order at which the
schemes disagree**. The finite-(H/a)² "correction" is therefore not determined by the construction; it is
gauge. (Off exact dS it is worse: the worldline temperature is not even known to be √(a²+H(t)²)/2π — the
repo's state-existence work found the off-dS response deceleration-driven — so the substitution inherits the
state conditionality on top of the scheme ambiguity.)
**(b) The MOND regime has no validity domain at all.** Deep-MOND onset a = a₀ = cH_Λ/Z means
(H/a)² = Z² = 32π/3 ≈ 33.5 ([F2a], exact framework identity) — the expansion parameter is ~33× past unity —
and the bookkeeping observer sits at Hℓ = arctan(Z) = 1.40 rad, **89% of the full static-patch depth π/2**
([F2b]): the "local" Rindler horizon and the cosmological horizon have MERGED (the GEMS content of DL: one
embedding horizon). Below a₀ the Clausius bookkeeping is simply Gibbons–Hawking thermodynamics of the dS
horizon — the Λ sector, already in the Einstein equation as the integration constant. **There is no separate
low-acceleration equation of state to derive: the local-horizon construction requires a ≫ H, and MOND lives
at a ≲ H/5.8.** Bonus wall ([G1]): any covariant completion G·μ(a)T_μν is killed by the Bianchi identity
(∇^μ[μT_μν] = 0 forces μ = const on the support of T) — the R2 object cannot even be promoted to a field
equation, echoing Door II's covariance wall.

## 7. What this does to the program (the extension, stated precisely)
- **The banked verdict extends to the exact temperature, at all orders.** The old result was a coarse swap;
  tonight's is the exact statement: in the only well-defined reading the DL temperature changes NOTHING
  (R1, §3), and in every Tolman-breaking reading the sign is quadrature-forced anti-MOND (§4). The
  temperature dial of horizon thermodynamics is now closed exactly, not just at leading order.
- **Tonight's substrate makes the "why" precise.** agentN1 proved the worldline physics in dS is genuinely
  TWO-variable — the dissipation kernel carries (a, H) separately — but also that the KMS **temperature**
  stays κ-only for every field mass ("thermality is not what breaks"). Clausius bookkeeping consumes
  exactly one object: T (and in exact dS even that collapses to the Tolman-trivial κ_b/2π). **The
  two-variable structure that could carry MOND lives in the response/dissipation kernel — an object the
  equation-of-state construction never touches.** Horizon thermodynamics and the MI lane are now cleanly
  disjoint: the missing object, if it exists, is in the Langevin/response sector (the N1→N2/N3 lane and the
  Door-II hybrid), not in any δQ = TδS.
- **One framework-favorable fact, full weight, raw:** the F4 kernel a/κ appears spontaneously in the
  balance (§4, three exact identities). This is a structural echo — the quadrature algebra, not a
  derivation — but it is the second independent place (after F4's own selection) where a/κ emerges as the
  natural dS-temperature interpolating function. Recorded; not oversold.
- **What stays open (unchanged):** the entropy/DOF dial (Verlinde-class, contested; the ledger's standing
  conclusion) and the nonequilibrium δS variants — tonight closes the temperature dial only, but closes it
  exactly.

## 8. Coefficient discipline (raw first, comparison after) — `.out` Part H
Raw O(1) numbers produced: series coefficients 1, −1/2, +3/8, −5/16 (binomial); scheme spread
{0, 1/6, 1/3, 1/2}; Tolman exact-dS coefficient 1/6; G_eff/G(a₀) = 1/√(1+Z²) = 0.17023; Hℓ(a₀)/(π/2)
= 0.891; temperature prefactor 1/2π (unmodified). Comparison: Z = √(32π/3) = 5.78881, 1/Z = 0.17275, 6,
2π. The 1/√(1+Z²) vs 1/Z proximity (1.5%) is the trivial large-Z identity — structurally meaningless,
flagged; 1/6 vs 1/Z (3.5%) was already flagged meaningless in agentB and is a Tolman series coefficient
here — unrelated. **No coefficient lands on Z, 6, or 2π.**

## 9. VERDICT (both ways, full weight)
- **The pre-registered trichotomy resolves as a two-horned null plus a quantified breakdown.**
  **(i) does NOT occur** — the correction is never a Λ-term; the null balance is provably Λ-blind, and Λ
  remains the Bianchi integration constant (underived, unmodified). **(ii) occurs only in Tolman-breaking
  readings**, where the correction is the acceleration-keyed rescaling G_eff/G = a/√(a²+H²) — EXACTLY the
  F4 kernel μ_F4, on the gravity side: a focusing DEFICIT at low a with total shutoff below g_N = cH. That
  is the anti-MOND orientation (the MOND/N3 sign needs the deficit on the INERTIA side, a leg Clausius
  cannot reach), and the sign is quadrature-forced in every temperature reading. **(iii) is the controlling
  fact**: the only well-defined (Tolman-consistent) reading cancels the H² term identically at all orders
  (T_DL IS the Tolman-shifted Gibbons–Hawking temperature — the central exact identity, machine-verified);
  every finite-(H/a)² coefficient is pure scheme ({0, 1/6, 1/3, 1/2}), degenerate with the construction's
  own neglected O(x²·Riemann) terms; and in the MOND regime the "local" wedge spans 89% of the static patch
  — the construction has no validity domain where MOND lives. **Horizon thermodynamics cannot reach MOND
  via the temperature, now exactly and for a precise reason: Clausius consumes T, which is κ-only and
  Tolman-trivial; the (a,H)-two-variable structure agentN1 proved real lives in the dissipation kernel,
  which the equation of state never consumes.** This is framework-neutral-to-unfavorable for any hope of an
  EoS-side mechanism and is stated at full weight; the banked Door-5 verdict is extended, not disturbed.
- **What would have changed the verdict** (pre-stated): a Tolman-consistent reading that retained an H
  correction (excluded by the exact identity B3/C1); a MOND-signed (focusing-enhancing) correction in any
  reading (excluded by quadrature, D4); a scheme-independent (H/a)² coefficient (excluded by F1).
- **What survives untouched:** the kernel a₀ = c²√(Λ/32π) as banked phenomenology; the entropy/DOF dial
  (Verlinde-class) as the one remaining — contested — horizon-thermodynamic lane; the MI/response lane
  (N1's open non-Huygens structure feeding the Door-II hybrid spec). New for the spec sheet: any future
  mechanism that turns the DL temperature into MOND must couple to **dT_DL/da on the inertia side** —
  δQ = TδS provably cannot do it.
