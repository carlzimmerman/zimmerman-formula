# L33 — the MOND scalar's cone: admissible, and forced

2026-09-08. Lane L33 of [CHARTER.md](CHARTER.md).
Script: [L33_scalar_cone.py](L33_scalar_cone.py) → [L33_scalar_cone.out](L33_scalar_cone.out).
**27 PASS, 5 FAIL.** All 12 controls PASS. Every FAIL is a substantive finding; none is a machinery failure.

Target: `THE_ACTION_2026-09-05.md` §§1–3, against the number [L13](L13_STRONG_COUPLING.md) produced in its
check **P8** — `c_s/c = 19` at 1 AU and `2.52e3` at Cassini conjunction — and against L13's label for it
("a quantified cost, not an exclusion; in a preferred-foliation theory superluminal propagation is not by
itself acausal"). That label was reasonable and had not been checked.

## Verdict in three sentences

**The cone is admissible, and the label was right — but for a reason sharper than "there is a preferred
foliation": the scalar's characteristic cone is built out of the *same* clock scalar τ that defines that
foliation, so `G^{μν}n_μn_ν = |K₂| > 0` is an identity independent of `c_s`, and the leaves are spacelike
at any speed.** Black holes are still black for it — the universal horizon censors arbitrarily fast modes,
and the `c_s = 2522 c` mode's own horizon sits `2.4e-4 M` outside it — and no existing observation is
violated, because gravitational Cherenkov bounds *slow* modes and is switched off entirely by
superluminality, while GW170817 bounds only the tensor. **The number is not a cost the theory chose: it is
forced, and the forcing is the Solar System's own ephemerides, not the kernel** — `c_s² = (2−K_B)g_N/(g_φ|K₂|)`
contains no `a₀` and no kernel shape, so the measured bound on an anomalous sunward acceleration bounds
`c_s` from *below* at `714 c` at Venus's orbit and `182 c` at Saturn's.

## 1. Control: the number, re-derived

The quadratic action of `δφ` was expanded from §§1–3 independently of L13's code. The acoustic (inverse)
metric is

    G^{μν} = |K₂| n^μn^ν − (2−K_B)[ J_Y q^{μν} + 2 J_YY V^μV^ν ]

with kinetic coefficient `|K₂|`, transverse stiffness `(2−K_B)J_Y`, and longitudinal stiffness
`(2−K_B)(J_Y + 2Y J_YY)`. **A2 proves symbolically, for a generic Δ, that `J_Y + 2Y J_YY = 1/Δ′(s)` exactly**
— the longitudinal stiffness *is* the inverse slope of the boost function, which is precisely what the
bounded-boost theorem constrains. `a₀` cancels from the identity.

| environment | footing | s | c_s/c at \|K₂\|=5e5 | at \|K₂\|=2e5 |
|---|---|---|---|---|
| MOND transition (galactic ambient) | either | 1 | 0.00249 | 0.00393 |
| Saturn orbit | can / alt | 6.90e5 / 5.73e5 | 1.96 / 1.78 | 3.10 / 2.82 |
| Earth orbit (1 AU) | can / alt | 6.33e7 / 5.26e7 | **18.8 / 17.1** | 29.7 / 27.0 |
| Cassini conjunction, b = 1.6 R☉ | can / alt | 1.14e12 / 9.50e11 | **2522 / 2298** | 3988 / 3633 |

A3 PASS — L13's 19/2522 and 17/2298 reproduced.

## 2. Is the cone spacelike with respect to the preferred foliation? Yes, identically

**B1 (control).** The action defines the clock through a *scalar* τ with no independent aether vector, so
hypersurface-orthogonality is an identity: `n ∧ dn = 0` was verified symbolically for a generic `τ(t,x,y,z)`.
The foliation is exact, not a solution property — unlike Einstein-aether.

**B2.** The condition for the leaves to be spacelike for a mode is that the leaf conormal be timelike for
that mode's inverse acoustic metric. Because `q^{μν}n_ν = 0` and `V·n = 0` *by construction*,

    G^{μν} n_μ n_ν = |K₂|      identically, for every J_Y and J_YY

— i.e. **the answer does not depend on the cone's width at all**. The no-ghost condition `|K₂| > 0` *is* the
spacelike condition. τ increases strictly along every characteristic (B4), so no closed causal curve exists.

**B3 (negative control, and the finding that matters).** The test has teeth, and its margin is small. If the
scalar's cone were tied to any frame boosted by `v` relative to the clock, then
`G^{μν}n_μn_ν = |K₂| − (2−K_B)J_Y(γ²−1)`, which turns negative — leaves timelike, closed causal curves — at
`v > c/c_s`. At Cassini conjunction that threshold is **119 km/s** (canonical; 131 alt), *smaller than the
Solar System's 370 km/s motion relative to the CMB and only four times Earth's orbital speed*. Explicit sign
flip printed at 0.9× and 1.1× the threshold. The theory is safe only because `Q = n·∂φ` and `V = q·∂φ` are
built from the same τ — the alignment is exact by construction. **Any future operator introducing a second
frame (a matter rest frame, a second vector) would produce closed causal curves at this cone width.** That
is a new design constraint, and it tightens as the cone widens.

## 3. The universal horizon, built explicitly

All `c_i ≤ 1e-5` here, so the metric is Schwarzschild to `O(1e-5)` and the clock is a test field. With the
`c₂` term dominant the leaves are constant-mean-curvature surfaces; the maximal (`K = 0`) family of
Schwarzschild is the textbook case and its limiting leaf is the universal horizon. Derived here, not quoted:

- **C1–C2 (controls).** `u^r = C/r²`, `s^r = √g` with `g = f + C²/r⁴`; `u·u = −1`, `s·s = +1`, `u·s = 0`
  exactly. The double root of `g` gives **`r_UH = 3M/2`**, `C = 3√3 M²/4`, `g″ = 16/(9M²)` — reproducing
  Estabrook et al. (1973)'s limiting maximal slice, identified as the universal horizon by
  Barausse–Jacobson–Sotiriou (arXiv:1104.2889) and Blas–Sibiryakov (arXiv:1110.2195).
- **C3 (control).** A ray of speed `c_s` escapes iff `g(r) > C²/(c_s²r⁴)`; at `c_s = 1` this returns the
  metric horizon `r = 2M` exactly.
- **C4–C5.** `r_h(c_s) − r_UH = √(3/8) M/c_s`, verified to 0.01%. At `c_s = 2522`, `r_h = 1.50024 M`:
  **99.95% of the way from the metric horizon in to the universal horizon, and still outside it.** At
  `c_s → ∞`, `r_h → r_UH` exactly.

| c_s/c | 1 | 10 | 18.8 | 100 | 2522 | 1e6 | 1e9 |
|---|---|---|---|---|---|---|---|
| r_h/M | 2.0000 | 1.5597 | 1.5322 | 1.5061 | 1.50024 | 1.5000006 | 1.50000001 |

So black-hole thermodynamics is not defeated: this is exactly the resolution of Dubovsky–Sibiryakov's
perpetuum mobile of the second kind (hep-th/0603158) supplied by Berglund–Bhattacharyya–Mattingly
(arXiv:1202.4497, arXiv:1210.4940) — the universal horizon carries its own surface gravity and temperature,
common to all mode speeds.

## 4. Well-posedness — the one place the published action does fail, and it is not the 2522

**D1 PASS.** The *transverse* sector is strongly hyperbolic everywhere sampled: real characteristic speeds,
positive-definite energy, finite domain of dependence. `c_s = 2522 c` is a perfectly ordinary hyperbolic
cone, just a wide one.

**D2 FAIL.** The *longitudinal* sector is not. By A2 its stiffness is `(2−K_B)/Δ′(s)`, and the carried
kernel is exactly flat beyond `s_sat = 2.540`, so **`Δ′ = 0` identically at every Solar-System background and
the longitudinal speed is not 2522 c but infinite.** That is not a closed causal curve (τ never *decreases*,
it stays constant along the ray) but it is not hyperbolic either: the sector degenerates into an elliptic
constraint on the leaf, solved with boundary conditions at infinity. This is the known khronometric
instantaneous mode (Blas–Pujolàs–Sibiryakov, arXiv:1007.3503), evolved in the literature as a mixed
elliptic–hyperbolic system (arXiv:1512.04899), not as a Cauchy problem with a finite domain of dependence.
It needs the *same* missing input L13's P9 asked for from the other side — a C² continuation of Δ past its
maximum with `Δ′ > 0`. **Note the direction: this makes the cone wider than P8's number, never narrower.**

A corollary a C² continuation does **not** remove: if Δ has an *interior* maximum (ν_RAR does, at 2.540),
then `Δ′ = 0` exactly there, so the longitudinal speed is infinite on that surface for every such kernel —
around the Sun, a sphere at **4994 AU** (canonical) / 4550 AU (alt), in the inner Oort cloud.

**D3 (control) PASS** — the hyperbolicity test flags a gradient instability when one is inserted by hand
(`K_B > 2` gives `ω²/k² = −196 c²`).

**D4 FAIL.** With the ξ² coherence operator the dispersion is `ω² = c_s²k²(1 + ξ²k²)` (Lifshitz z = 2):
`ω(k)` is real at every `k`, so the Cauchy problem is well posed in the Lifshitz sense, but the group
velocity is unbounded (`v_g = 4e1 c` at `k = 1/ξ`, `8e5 c` at `k = 1/AU`, `1e17 c` at `k = 1 m⁻¹`). There is
no cone at all in the ultraviolet, and the `2522 c` figure is a long-wavelength (`k ≪ 1/ξ`) statement only.
This is a known and accepted feature of a Hořava-type host, reported so that it is on the record rather than
because it is new.

## 5. Does any observation bound this speed? No — and none bounds it

- **E1 (control).** GW170817 bounds the *tensor* speed. Here `c_T² = 1/(1−c₁₃)` with `c₁₃ = 0` exactly, so
  `c_T = c` identically and independently of `|K₂|`, `J_Y` and the kernel. The scalar is spin-0 and does not
  enter the tensor dispersion. **No bound.**
- **E2.** Gravitational Cherenkov requires `v > c_s`, and `v < c < c_s`. **There is no emission channel into
  a superluminal mode at all.** Elliott–Moore–Stoica (hep-ph/0505211) constrain aether modes to be at or
  *above* `c` for exactly this reason, and the repo's own g03v applies that requirement to the khronon.
  A cone wider than the light cone is not merely tolerated by the strongest existing bound — it is what that
  bound asks for.
- **E3 (diagnostic, the honest flip side).** The same law makes the mode *subluminal* below
  `s_crit = Δ_max|K₂|/(2−K_B) = 1.80e5`, i.e. everywhere beyond **19 AU** of the Sun; at galactic ambient
  acceleration `c_s = 746 km/s`. That subluminal corner is where the Cherenkov bound actually lives.
- **E4 (worst case).** Milgrom (arXiv:1102.1818) showed emission of wavenumber `k` is generated at `~1/k`
  from the primary, giving `D_loss = q c²/a₀` with the cosmic-ray energy cancelling (L19 re-derived that
  published result independently; cited here, not re-derived). In *this* action the cutoff is not Milgrom's
  `r_M` but the smaller `r_c` where the cone crosses `c`, a factor `√s_crit = 424` inside it — so the
  protection is weaker than Milgrom's by `s_crit`. Even so, and with the coupling taken at full
  gravitational strength, `D_loss = 2(c²/a₀)/s_crit = 1.07e22 m`, **35× the 10 kpc Galactic path** (29× alt).
  Two suppressions were deliberately omitted and both lengthen it: the `1/J_Y` screening in exactly the
  emitting shell, and the `1/|K₂|` from the scalar's own kinetic normalisation. **PASS, but the margin is
  35, not 1e7**, and for an extragalactic 100 Mpc path this worst case would fail by 289×. This is the one
  empirical item the lane leaves open; the missing input is the scalar–matter vertex normalisation.
- **E5.** Binary pulsars bound `α₁, α₂` and the dipole *coupling*, not `c_s` (and a larger `c_s` suppresses
  scalar radiation, making those bounds easier). The CMB and growth constrain the *cosmological* value,
  where the mode is deeply subluminal. Matter is minimally coupled to `g` alone, so there is no emitter and
  no receiver for a time-of-flight test. **Stated plainly: no existing observation bounds this scalar's
  speed from above.** The Solar-System cone is untested in the strict sense that nothing measures it.

## 6. Is it forced by bounded boost? Yes — and by something stronger

**F1.** The static law of any matter-sourced scalar of this class gives `J_Y g_φ = g_N` exactly, hence

    c_s,⊥² / c²  =  (2 − K_B) g_N / ( g_φ |K₂| )

**containing no `a₀` and no kernel shape.** Both footings give identical numbers for this statement.

**F2 — the sharpest form.** Subluminality at a point therefore *requires* a scalar force
`g_φ ≥ (2−K_B)g_N/|K₂|` there, and the scalar force is exactly the anomalous sunward acceleration the
ephemerides bound (Venus 8.0e-14, Saturn 7.0e-15 m s⁻², 1σ, the repo's committed inputs):

| planet | g_N | g_φ needed for subluminality | ephemeris bound | over by | ⇒ c_s/c forced ≥ |
|---|---|---|---|---|---|
| Venus | 1.13e-2 | 4.08e-8 | 8.0e-14 | 5.1e5× | **714** |
| Saturn | 6.46e-5 | 2.32e-10 | 7.0e-15 | 3.3e4× | **182** |

So the planetary data *force the cone open* at several hundred `c`, for any kernel and both footings. The
caveat is stated: this uses the ξ = 0 static law, and the ξ² operator only stiffens the response further,
i.e. it raises `c_s`.

**F3 FAIL (⇒ forced).** Scan of the standard interpolating-function family — simple ν, standard ν, the
n-family (n = 3, 5, 10, 20), ν_RAR, exponential carrier. `Δ_max ∈ [0.250, 1.000]`, so subluminality at 1 AU
needs `|K₂| ≥ 1.14e8` even for the most generous member: **228× the dark sector's window edge and 42× the
growth pincer's 2.7e6.** To fit inside `|K₂| = 5e5` a kernel would need `Δ_max ≥ 228`, a permanent
`2.1e-8 m s⁻²` excess — 2.7e5× the Venus bound. Seven of the eight have an *interior* maximum, so the
bounded-boost theorem forces them to saturate and their longitudinal speed is infinite in the Solar System;
the one monotone member (simple ν) still gives a longitudinal cone 7959× wider than its transverse one.

**F4 (control).** The theorem is about *boundedness*, not about scalars: an unbounded `Δ = βs` (a pure `G`
rescaling, no MOND) has `J_Y = const` and is subluminal at `|K₂| ≥ 1.8`, thirteen orders below the window.

**F5.** The general statement: boundedness of Δ forces `Δ′ → 0` and `Δ/s → 0`, so both
`c_⊥² = (2−K_B)s/(Δ|K₂|)` and `c_∥² = (2−K_B)/(Δ′|K₂|)` diverge with acceleration. **There is no
bounded-boost kernel of this class with a subluminal high-acceleration scalar at any admissible `|K₂|`.**

## 7. What this changes

- L13's P8 label is **upheld and replaced by a proof**. The cone is admissible: causally (B2, an identity),
  under black-hole censorship (C4/C5, an explicit construction), and observationally (E1–E5).
- The superluminality is **structural, not a cost the theory chose**. It follows from the bounded-boost
  theorem, and independently from planetary ephemerides. It should be described as a *prediction* of the
  action — an untested one — rather than as a liability.
- **P8 should not be re-run as a `|K₂|` pincer arm.** Subluminality is not a requirement this class can
  meet, and demanding it would be demanding a Solar-System scalar force 3e4–5e5× the ephemeris bound.
- Three real costs, all new here: the **119 km/s frame-alignment margin** (B3) as a design constraint on any
  future operator; the **infinite longitudinal speed** on the published saturated branch (D2), which shares
  its missing input with L13's P9; and the **Cherenkov margin of 35**, not 1e7, in the subluminal galactic
  corner (E4), with the deciding calculation named.

## Scope — not done here

The scalar–matter vertex normalisation is not computed, so E4 is an upper bound on the loss rate and not a
rate. Lane L19 owns the Cherenkov rate machinery, for a different mode (IC10's clock) in a different action;
nothing of it is imported, and where this lane needs Milgrom's published loss distance it cites it. The
universal-horizon construction in §3 is exact for the `c₂`-dominated decoupling limit and is presented as a
verified *example* of the mechanism; existence for general `c_i` is a literature result, cited. The mixed
(khronon, δφ) characteristic determinant is not computed — the leaf is non-characteristic for the mixed
system whenever the kinetic Hessian is invertible, which L13 established (`diag(2M²c₁₄k², 2M²|K₂|)`), and
that is what B2 uses. `α₁`/`α₂` and the strong-coupling scale are L13's and are not revisited.
