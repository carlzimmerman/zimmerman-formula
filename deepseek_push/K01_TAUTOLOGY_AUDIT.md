# K01 — ANTI-TAUTOLOGY AUDIT of the JWST Moment Channel (J01–J05, J07–J09)

**2026-09-23 · adversarial audit, opposite of cheerleading · the user is a rigorous physics referee**
Source files read (recorded numbers quoted verbatim): `J01_MIXED_MOMENT.md` + `J01_results.json`,
`J02_MOMENT_HIERARCHY.md` + `J02_results.json`, `J05_TRANSFER_FUNCTION_READING.md` + `J05_results.json`,
`J07_SPECTRAL_ENVELOPE.md` + `J07_results.json`, `J09_two_component_law.py` + `J09_two_component_law.out` (0 bytes),
`J00_MOMENT_CHANNEL_LEDGER.md`, frozen `real_research/reviews/bhstar_scattering_clock_2026_09_21/density_free/THEOREM.md`.
**No numbers invented in this audit; every quote below appears in the listed records.**

## Classification scheme (per the audit brief)

- **(A) CLOSED-ONE-LINER** — identity that follows trivially from the simulation's own definition
  (e.g. v|traj Gaussian *because the engine draws Gaussian kicks*). Label: consistency check only.
  Mathematically valid; **circular as evidence** (engine verifies itself against its own sampling rule).
- **(B) GENUINE-MODEL-STATEMENT** — statement about the joint law of path functionals that does **not**
  follow from kick-Gaussianity alone (path geometry must supply it). Not circular.
- **(C) NEW-OBSERVABLE** — phrased so an observer can falsify with velocity-resolved RM, independent of
  κ, n_e, geometry. Not circular as a test.

## §1. Per-claim audit (16 claims)

### J01 — mixed moment

**J01-C1 “Conditional on the trajectory, v is Gaussian with variance exactly 2·ang”; per-kick
Var = 2T(1−μ). — CLASS (A).**
Derivation (2 lines): each kick Δv = T(r_j)e·(u′_j−u_j) with e Maxwellian ⟹ E[e²]=1, Var(e·(u′−u)) = T²|u′−u|²
= 2T²(1−μ); kicks conditionally independent ⟹ v|traj ~ N(0, 2·Σ_j T(r_j)(1−u_j·u′_j)) = N(0, 2·ang).
This **is the engine's kick-generation rule** (J02_moment_hierarchy.py draws Gaussian e per scatter).
Circular as discovery: **YES** — the engine draws Gaussian kicks by construction.
Recorded evidence: E[v⁴] = 67.05 vs 12·E[ang²] = 67.34 (J01 S4b); E[v²] = 2E[ang] to 0.02% isothermal.
Disposition: **label-only / consistency check.** Not a discovery; keep only as the spine that the (B)/(C)
claims hang on (and only for exposing where the real content sits).

**J01-C2 “E[D v²] = 2·E[D·ang] — exact, every scattering order.” — CLASS (A).**
Derivation (2 lines): E[Dv²] = E[E[Dv²|traj]] = E[D·Var(v|traj)] = E[D·2ang] = 2E[D·ang] (tower property).
A one-line consequence of C1; no path-geometry content appears (the joint law of (D,ang) never enters).
Circular as discovery: **YES**.
Recorded evidence: 3.7316 vs 3.7237 (Δ 0.2%); q=10: 192.67 vs 192.38; τ₀=2,q=3,h=2: 234.16 vs 234.04 (J01).
Disposition: **label-only / consistency check.**

**J01-C3 “The two-moment closure E[Dv²] = 2E[D]E[ang] is false: R = 2.6446 ± 0.018 / 2.0235 ± 0.012 /
1.6971 ± 0.009 (q = 0/3/10, n = 5×10⁵), 5σ+ shape-separated.” — CLASS (B).**
Derivation (3 lines): R − 1 = Cov(D, ang)/(E[D]E[ang]). Kick-Gaussianity fixes the *conditional* moments
E[Dv²|traj] = 2D·ang but says **nothing** about Corr(D,ang) — that is a property of the scattering-walk
geometry (the path law), i.e. genuinely beyond the model input. Measured, not closed-form (MC with SEs).
Circular: **NO.**
Recorded: R values as above (J01_results.json closure_q0/3/10); the target's demanded counterexample —
the angular correlation Cov(D,ang) is load-bearing.
Disposition: **REAL CONTENT (negative/constraint on the joint law).** The strongest J01 item, but MC-grade:
the 5σ separations are engine-internal; the statement is about the model's joint law, not yet data.

**J01-C4 “The p,k BVP hierarchy reproduces the identity: F⁰² = −2E[ang] = −E[v²],
F¹² ⟹ E[Dv²] with source 2κT∫P(u,u′)(1−u·u′)F¹⁰.” — CLASS (A).**
Derivation (3 lines): expand e^{−k²T(1−u·u′)} = 1 − k²T(1−u·u′) + …; ∂²_k at 0 = −2T(1−u·u′); the p,k²
order of the tilted BVP re-derives C2 order-by-order. This is the target's own candidate BVP, re-verified;
it is the *analytic image* of C2 in transfer-operator form — no new statistical content.
Circular: **YES** (as evidence for the mixed moment; it verifies the BVP reproduces the engine identity).
Disposition: **label-only** beyond C2 — but legitimately valuable as the machinery the target commissioned.

### J02 — even-moment hierarchy + volume face

**J02-A “E[D v^{2m}] = (2m−1)!!·2^m·E[D·ang^m] for every m, every order, central or volume.” — CLASS (A).**
Derivation (2 lines): Gaussian moments E[v^{2m}|traj] = (2m−1)!!(2ang)^m; tower property.
This is the task brief's own example of (A): **model input** (Gaussian moment recursion), not discovery.
Circular as discovery: **YES**.
Recorded evidence: central m=1,2,3: 3.7254 vs 3.7142 (0.30%), 122.04 vs 121.57 (0.38%), 8502 vs 8762
(3.1% — flagged in-file as MC tail of v⁶); volume: 2.2634 vs 2.2598, 68.60 vs 68.24, 4834 vs 4672.
Disposition: **label-only — must be labeled a consistency check** (the ledger's P1 “PROVEN” entry is
accurate as a proof statement but carries zero discovery weight; the honest framing is J05 §1's own
“consistency family”).

**J02-B “Volume source: E[τ]_vol = ∫₀¹ rκ dr + E[μ_exit] − ½E[F(r₀)] (Dynkin, exact; F(r) = 2∫₀^r sκ ds,
r₀ ~ 3r²), and E[D]_vol = E[τ]_vol − E[Q], Q = Σ_j ℓ_j(u_j·u_final) retained.” — CLASS (B).**
Derivation (4 lines): f = F(r) + 2x·u solves Lf = 2c (streaming 2c + scattering −2cκ x·u since E[u′|u]=0);
Dynkin: 2cE[τ] = F(R) + 2R·E[μ_exit]; subtract the propagation advance and decompose the volume birth
position ½E[F(r₀)]; D = τ − Q pathwise (B4). No velocity moment anywhere — **does not follow from
kick-Gaussianity** (involves no kicks); it is a statement about the *spatial* stopping-time law.
Circular: **NO.**
Recorded evidence: B3: E[τ]_vol = 0.93465 vs ½ + 0.73527 − 0.3 = 0.93527 (E[μ_exit] = 0.73527 ± 0.00052,
n = 1.5×10⁵); B4 bookkeeping exact to 6.66e-16 (E[Q] = 0.59715); B2: E[D]_vol = 0.3376 ≠ ½ at > 8 SE.
Disposition: **REAL CONTENT.** Exactly locates the domain boundary of the frozen Theorem 1
(E[D] = ∫rκ dr is central-only) — an applicability-domain correction with a new retained functional Q.

**J02-C “Closure ratios R_m = E[Dv^{2m}]/((2m−1)!!·2^m·E[D]·E[ang^m]) = 2.635 / 3.574 / 4.563 (q = 0,
n = 10⁶) — grows with m.” — CLASS (B).**
Derivation (3 lines): R_m − 1 is the normalized Cov(D, ang^m)/E[D]E[ang^m]-type term; Gaussianity fixes
conditional moments only; the growth with m is a joint-law measurement. Same non-circularity as J01-C3;
extends the closure failure to every order.
Circular: **NO.**
Disposition: **REAL CONTENT** (MC-grade, with SEs). Also the seed of the J05/J07 falsifiers.

### J05 — transfer-function reading

**J05-F1 “Renormalized consistency family E[ang^m] = E[v^{2m}]/((2m−1)!!·2^m); every velocity-resolved TF
of a Thomson LRD must satisfy the hierarchy simultaneously, whatever the density.” — CLASS (A).**
Derivation (2 lines): invert Gaussian recursion (J02-A) for the hidden ang-moments. Same model input;
the only new thing is the re-expression in observable variables (pure line-profile moments E[v^{2m}]).
Circular as discovery: **YES** (as evidence); not circular as a *joint-consistency* battery **provided the
ang-terms are eliminated** — see F4 finding: the observable-form test actually used in J05 §5(a) is
q-conditional as written.
Disposition: **label-only** (consistency family). The D-side of the family (E[Dang^m] = E[Dv^{2m}]/((2m−1)!!2^m))
is untestable directly: E[D·ang^m] ≠ E[D]E[ang^m] in general and ang is unobservable.

**J05-F2 “E[D²] ≥ 3·E[Dv²]²/E[v⁴] — density-free, isothermality-free.” — CLASS (C).**
Derivation (3 lines): Cauchy–Schwarz: E[D·ang]² ≤ E[D²]·E[ang²]; insert E[D·ang] = E[Dv²]/2 and
E[ang²] = E[v⁴]/12 (both from A); solve ⟹ E[D²] ≥ 3E[Dv²]²/E[v⁴]. All three inputs are velocity-resolved
RM observables; no κ, no n_e, no geometry appears. The inequality is theorem-rigid (C–S is universal);
inputs are observer-measurable — the test is not circular (cf. THEOREM.md's own no-circularity clause:
R and T_e separately measured; nothing derived-from-D is fed back).
Circular: **NO** (as a falsifier). Recorded: 4-cloud verification, E[D²] vs bound: 0.7651 vs 0.6141
(slack 1.25), 3.3615 vs 2.9666 (1.13), 16.213 vs 15.235 (1.06), 11.222 vs 10.497 (1.07).
Disposition: **REAL CONTENT — the channel's single cleanest density-free observable.** Caveat: tightness
(“slack → 1.06”) is MC-measured, not proven (ledger N2); the bound itself is rigid.

**J05-F3 “An observer using the frozen identity on a shell/volume emitter is wrong by exactly
E[Q] + ½E[F(r₀)] (E[D]_vol = 0.338 vs central ~0.501; E[Q] = 0.597).” — CLASS (B).**
Derivation (3 lines): J02-B + Theorem 1: E[D]_vol − ∫rκdr = E[μ_exit] − ½E[F(r₀)] − E[Q] (combining
E[τ]_vol and D = τ − Q). Direct applicability-domain statement; no kicks involved.
Circular: **NO.** Disposition: **REAL CONTENT** (applied-domain correction), carried entirely by J02-B.

**J05-F4 “Falsifier §5: (a) hierarchy ratios R = 2.64 / 3.57 / 4.56 must hold jointly … any ≥ 3σ
violation kills the Thomson-scattering interpretation for any density.” — CLASS (C) as stated, but
**OVERSTATED AS RECORDED.****
Problem (3 lines): R_m are *measured q = 0 values* — R₁ itself ranges 2.6446 → 1.6971 across q = 0 → 10.
An observer does not know q, so “the ratios must equal 2.64/3.57/4.56” is a test of the *quadratic-family
q = 0 cloud*, not of conservative Thomson scattering. The genuinely q-free, density-free knifes are
(b) the J05-F2 bound (rigid) and the joint hierarchy only in renormalized angles-free form
(E[v⁴] ≥ 3E[v²]²-type line-profile statements), not the fixed numbers 2.64/3.57/4.56.
Circular: **NO**; overstated: **YES** — must be re-scoped (e.g. “R₁ as a *function of measured shape*” or
dropped in favor of F2) before it is promoted as a universal falsifier.

### J07 — spectral envelope

**J07-E “|H(ω)| ≥ max(0, 1 − ½ω²·E[D²]) (T3′) and |H(ω)| ≥ max(0, 1 − ½ω²·L), L = 3·E[Dv²]²/E[v⁴]
(T3″); T3′ asymptotically exact at ω → 0 (log–log slope 3.99); L ≤ E[D²] holds.” — CLASS (C).**
Derivation (3 lines): |E[e^{iωD}]| ≥ E[cos ωD]; cos x ≥ 1 − x²/2 ⟹ T3′; substitute the J05 bound
E[D²] ≥ L ⟹ T3″; cos x = 1 − x²/2 + O(x⁴) gives the O(ω⁴) remainder (slope 4). The cosine inequality is
universal (any delay law); the model content is only which moments enter, and T3″ needs *no* κ, n_e,
geometry — just mixed line moments. J07 itself concedes: “Not claimed: novelty of cos x ≤ 1 − x²/2.”
Circular: **NO** (as a spectral falsifier; the verification uses model-D for the *envelope test*, while
the bound statement is for measured H(ω) — the transfer caveats are registered in J07's honest edges).
Recorded: 20/20 checks on 4 clouds; ω* = 1.308 (uniform); at ω·E[D] = 0.5: |H|_meas 0.9413 vs T3′ 0.9045
vs T3 0.7501; T3″ numbers 0.9809 / 0.9235 / 0.6939 / clips; ω = 2.0: linear 0.0002, both envelopes clip.
Disposition: **REAL CONTENT** as an observable envelope package — with the caveat that the *mathematical*
step is elementary (self-acknowledged); the value is the moment-chain substitution and its verification,
not a new inequality of nature.

### J09 — two-component law (per `J09_two_component_law.py` docstring)

> **Evidence-status finding (F1): there is NO recorded J09 result. `J09_two_component_law.out` is
> 0 bytes; no `J09_results.json` exists in `deepseek_push/` (file census). The script's `print`-only
> output was never captured. Every J09 claim below is therefore UNVERIFIED-AS-RECORDED.** An
> independent re-run was launched during this audit (see Appendix R): it reaches **19/20 — A5_volume
> FAILS** (m=5 volume ratio 0.6992, half-splits [0.746, 0.648]), and the m = 3–5 ratios trend
> systematically below 1 for *both* sources, so “every m” is not cleanly verified even on re-run.

**J09-A “W := v²/(2ang) | (D, ang) ~ χ²₁ — W independent of the whole path geometry; hierarchy for every
m (tested m = 1..5, 7!! = 105, 9!! = 945).” — CLASS (A).**
Derivation (3 lines): v|traj ~ N(0, 2ang) ⟹ W|traj ~ χ²₁ for *every* trajectory; for any g measurable in
(D,ang): E[f(W)g(D,ang)] = E[g·E_χ[f]] = E[g]·E_χ[f] — independence is a two-line tower-property
consequence of the Gaussian spine. “Trajectory geometry carries no kick information beyond the variance”
is exactly the content of C1 — **model input, not a new discovery**. (The task brief listed this as a (B)
candidate; the audit verdict is (A): the lemma's variance being a *trajectory-measurable functional* is
the whole assumption.) The m = 4,5 extension is the same Gaussian recursion (J02-A).
Circular as discovery: **YES**. Disposition: **label-only** (consistency family), and unverified as recorded
— re-run: m = 1,2 ratios ~0.997–0.995 hold; m = 3–5 sink (central 0.9787 / 0.9035 / 0.7444; volume
0.9518 / 0.8618 / 0.6992), A5_volume FAILS the script's own tolerance (tolerance itself miscalibrated:
the se_pure factor uses (2m−3)!! — prod(range(1,2m−1,2)) — where (2m−1)!! is the relevant moment, so
the claimed tail budget is not the pure-χ²₁ budget).

**J09-B “Delay-resolved line profile exactly Gaussian: in EVERY narrow D-bin, kurtosis(v|D) = 3.” — CLASS (A)
with an internal overstatement (F2), now empirically refuted in its own re-run.**
Derivation (3 lines): v|D is a scale mixture of Gaussians with scales √(2ang|D) ⟹
kurt(v|D) = 3·E[ang²|D]/E[ang|D]² **≥ 3** — which is exactly the check the script implements
(“kurt = mixture law within MC error, and kurt ≥ 3 − 0.05”). The docstring headline “kurtosis-per-bin = 3”
is **not** a consequence: = 3 iff ang|D is degenerate, which is not established or implied.
Circular as discovery: **YES** (the mixture law is the spine re-expressed per bin). Overstated: **YES**.
**Re-run evidence: measured per-bin kurtoses are 3.35–4.33 (central bins 3.4746 / 3.3477, volume
4.3303 / 3.9339) against mixture-law predictions 3.4843 / 3.3569 / 4.2740 / 3.9559 — miles from 3,
consistent with the “≥ 3” law to < 0.06.** Headline “= 3” is false as data; the mixture law holds.
Disposition: **label-only; fix the headline to “kurtosis ≥ 3 per bin, mixture law”**. Unverified as recorded.

**J09-C “Atom law: P(D = 0, v = 0) = A = exp(−τ₀(1 + q/3)) (central source, exact).” — CLASS (A).**
Derivation (2 lines): D = 0 & v = 0 ⟺ N = 0 (ballistic photon; any kick gives v ≠ 0 a.s.); for the central
source the first flight is the radial ray r: 0 → 1 with optical depth ∫₀¹ κ(r) dr = τ₀(1 + q/3);
Poisson thinning gives P(N = 0) = exp(−∫₀¹κ dr). This is the *sampler's own definitional output* — the
engine draws N from exactly this Poisson rate — so as evidence the check is sampler-self-consistency.
Circular as discovery: **YES** (definitional). Disposition: **label-only** (consistency check of the
optical-depth sampler). Unverified as recorded; re-run passes: A = 0.36826 vs exp(−1) = 0.36788;
0.013205 vs 0.013124 (q=10); 0.018405 vs 0.018316 (τ₀=2,q=3).

**J09-D “Ratio window: −ln(A)/dbar = (1 + q/3)/(1/2 + q/4) ∈ [4/3, 2], opacity-independent; a measured
ratio outside [4/3, 2] kills the conservative Thomson-sphere reading for ANY central-source geometry.” — CLASS (B)
(closed form; the second sentence is overstated — F3).**
Derivation (3 lines): dbar = E[D] = ∫₀¹ rκ(r) dr = τ₀(1/2 + q/4) (frozen Theorem 1 — a genuine stopping-time
theorem, not a definition); −ln A = τ₀(1 + q/3) (J09-C); ratio = (1 + q/3)/(1/2 + q/4) ∈ [4/3, 2] as
q ∈ [0, ∞) — q = 0 gives 2, q → ∞ gives 4/3. No kick-Gaussianity anywhere; the content is
Theorem-1 × Poisson-atom, and τ₀ cancels — that cancellation is real content.
Circular: **NO** (as a model identity). **Overstated: YES.** The window is specific to the quadratic
profile family κ(r) = τ₀(1 + qr²): for the general family κ = τ₀(1 + qr^p), −lnA/dbar = (1 + q/(p+1))/(1/2 + q/(p+2)),
whose q → ∞ limit is (p + 2)/(p + 1) — e.g. p = 4 gives 6/5 = 1.20 < 4/3, inside the same conservative
Thomson model but *outside* the window. So a measured ratio below 4/3 does **not** kill the Thomson reading
“for ANY central-source geometry” — it kills the quadratic subfamily. The honest claim: the ratio is
τ₀-free for every profile shape, and ∈ [4/3, 2] for κ = τ₀(1 + qr²) exactly.
Disposition: **conditional real content** (opacity-elimination is genuine; universality must be re-scoped;
verification currently missing). Unverified as recorded; re-run passes the window check: ratios 2.0022 /
1.4413 / 1.5980 vs exact 2.0 / 1.4444 / 1.6 (q = 0/10, τ₀=2,q=3) — all inside [4/3, 2].

### J08

**J08 — ABSENT.** `J09_two_component_law.py` header: “Follow-on to J08 (χ²₁ spine)” — but no J08 files
(`J08*`) exist anywhere in `deepseek_push/` (file census). The W-independence theorem is attributed to J08
but the J08 record was never produced. Nothing to audit; nothing to promote until the J08 record exists.

## §2. Findings (things a referee must not miss)

- **F1 — J09 is an unverified landing.** Empty `.out`, no results JSON, no `.md`. Claims J09-A/B/C/D are
  presented as theorem+checks but *no recorded run exists*. Audit re-run: **19/20 — A5_volume FAILS**
  (0.6992) with m = 3–5 ratios sinking below 1 for both sources; "100%-style" claims ("every m",
  "kurtosis = 3") do not survive their own procedure (see F2, Appendix R).
- **F2 — J09-B headline overstates its own check.** “kurtosis-per-bin = 3” vs implemented
  scale-mixture law kurt = 3E[ang²|D]/E[ang|D]² ≥ 3. Headline and check contradict; = 3 needs ang|D degenerate.
  **The audit re-run measures per-bin kurtosis 3.35–4.33 (mixture-law predictions 3.36–4.27) — the “= 3”
  headline is empirically false; the ≥ 3 mixture law holds.**
- **F3 — J09-D's “universal … ANY central-source geometry” is false beyond the quadratic family**
  (limit (p+2)/(p+1) for κ ∝ 1 + qr^p; e.g. 6/5 < 4/3 for p = 4).
- **F4 — J05 §5(a)'s fixed ratios 2.64/3.57/4.56 are q-conditional MC values, not a density-free law.**
  The fixed-number falsifier only tests the q = 0 quadratic cloud; the density-free knife is the F2 bound.
- **F5 — The (A) family is internally consistent and 35/35-verified — but that is the point of (A):**
  35/35 checks verify that three engines draw Gaussian kicks with variance 2·ang. Zero observational weight.
- **F6 — Credits (to keep on the record):** the m = 3 MC-tail caveat is stated in-file (3.1%/3.5%,
  pre-registered tolerance); every MC number carries SEs; K1/K2/K3 kill-records are preserved in the
  ledger with no number adjusted; THEOREM.md's own no-circularity clause (R, T_e separately measured) is
  respected by the (C) claims; J07's honest edge concedes the cosine inequality is elementary.

## §3. GO / NO-GO

**GO — survives as real content (6):**
- J01-C3 (R = 2.6446 ± 0.018 / 2.0235 ± 0.012 / 1.6971 ± 0.009; closure failure, joint-law constraint) — B
- J02-B (volume Dynkin compensation, E[τ]_vol = ∫rκ dr + E[μ_exit] − ½E[F(r₀)], E[Q] = 0.59715, exact to 7e-16; Q retained) — B
- J02-C (R_m = 2.635 / 3.574 / 4.563 growing with m) — B
- J05-F2 (E[D²] ≥ 3E[Dv²]²/E[v⁴]; 4-cloud, slack 1.25/1.13/1.06/1.07) — C
- J05-F3 (volume taboos Theorem 1; wrong by Q + ½E[F(r₀)]) — B
- J07-E (T3′/T3″ envelopes; 20/20; slope 3.99; ω* = 1.308; 0.9413 vs 0.9045 vs 0.7501 at ω·E[D] = 0.5) — C

**NO-GO as recorded — label-only (consistency checks, zero discovery weight; keep, but relabel):**
- J01-C1, J01-C2, J01-C4, J02-A, J05-F1, J09-A, J09-B, J09-C — (A) family: model-input restatements.
  The ledger's “PROVEN P1” is accurate as math but must read “consistency family” in any promotion.

**NO-GO as recorded — must be fixed before any use (3):**
- J05-F4 — re-scope the falsifier: fixed R_m numbers are q-conditional; keep only the F2 bound as
  universal, or restate as “shape-dependent R₁ battery”.
- J09-B — headline “kurtosis-per-bin = 3” contradicts its own check; must read “≥ 3, mixture law”.
- J09-D — “universal window … ANY central-source geometry” is false in general; re-scope to
  κ = τ₀(1 + qr²) (limit (p + 2)/(p + 1) otherwise), and **verify it** (F1: no run recorded).
- J08 — absent record; referenced as the spine of J09; nothing can be audited or promoted.

**Bottom line:** the channel's real content is the *joint-law characterization* (B: closure failure at
all orders, volume domain correction) and the *density-free observables* (C: the width bound and the
spectral envelopes). Everything derived by the Gaussian-lemma recursion — the entire even-moment hierarchy,
the W-independence, the per-bin kurtosis law, the atom formula — is model input restated as discovery and
must be labeled consistency-only. J09 as recorded is an unverified landing with two overstatements; it
does not pass promotion until re-run, re-scoped, and re-recorded.

## Appendix R — independent re-run of J09 (fresh numbers, not part of the recorded lane)

`python3 deepseek_push/J09_two_component_law.py > deepseek_push/K01_J09_RERUN.out` (repo root, ~150 s, seeds
81/91/101, n = 6×10⁵). Result: **19/20 — A5_volume FAILS; the script exits 1 ("J09 CHECK FAILURE")**.
These numbers were produced by this audit for *verifiability*, not in the lane's records; the audit's
verdicts do not depend on them.

- **A-series (hierarchy m = 1..5):** m=1,2 clean for both sources (central 0.9967 / 0.9967; volume
  0.9945 / 0.9858). m=3–5 sink monotonically below 1 — central 0.9787 / 0.9035 / 0.7444; volume
  0.9518 / 0.8618 / **0.6992 (FAIL)**, half-splits [0.746, 0.648] both ≪ 1: the deviation is
  systematic-looking, not a single-tail fluke. The script's own tail budget is miscalibrated
  (se_pure uses (2m−3)!!-type products; e.g. at m=5 pure-χ²₁ relative SE is ≈ 3.5%, while the formula
  feeds ≈ 0.8%) — so m ≥ 4 "passes" are not the pure-distribution budget claimed, and under a corrected
  budget even A4_central (0.9035) and A4_volume (0.8618) sit far outside 3σ. **The "every m" claim is
  NOT cleanly verified.**
- **B-series:** per-bin kurtosis (30–70th percentile bins of the continuous part) vs scale-mixture
  prediction: central measured 3.4746 / 3.3477 vs 3.4843 / 3.3569; volume 4.3303 / 3.9339 vs
  4.2740 / 3.9559. Mixture law holds to < 0.06; **kurtosis is 3.35–4.33, nowhere near the docstring's
  "= 3"** — empirical confirmation of finding F2.
- **C-series:** atom A = 0.36826 vs exp(−1) = 0.36788; 0.013205 vs 0.013124 (τ₀=1, q=10); 0.018405 vs
  0.018316 (τ₀=2, q=3). Window ratios: 2.0022 vs 2.0; 1.4413 vs 1.4444; 1.5980 vs 1.6 — all in [4/3, 2].
  The J09-D mechanics (atom law + Theorem-1 mean + τ₀ cancellation) are internally consistent where tested.
- Audit conclusion on the re-run: J09's *definitional* content (A-series low m, B mixture law, C atom and
  window) holds; its *strong* claims ("every m", "kurtosis-per-bin = 3", "universal … ANY geometry") do
  not — and none of it was ever recorded in the lane. J09 stays NO-GO as recorded.