# agentSS VERIFY — adversarial referee of route HEAT-KERNEL-SYMMETRY (2026-06-13)

**Central mission (from the brief):** is the claimed hidden symmetry REAL (a genuine structure of the
banked dS heat-kernel / QNM ladder) or IMPOSED, and does it FORCE or merely PERMIT the edge surface
4 j3/j2^2 = G_sat? Default posture: assume 'forces' is overclaimed and the honest answer is
NEEDS-NEW-INPUT until a ZERO-parameter forcing is shown.

The route already self-reports **PERMITS-NOT-FORCES / NEEDS-NEW-INPUT.** So the referee's job is NOT to
catch a forcing overclaim (there is none) but to check the OPPOSITE failure modes:
- (i) is the named symmetry actually real, or did the route invent structure?
- (ii) is the PERMITS verdict itself built on a sound object, or on a smuggled/wrong one?
- (iii) did the route's symmetry quietly re-invoke the PASSIVE QNM that agentPP's no-fold theorem
  already killed, and dress a passive result as a statement about the active fold?
- (iv) is any of the "separation/decoupling" an artifact of an arbitrary convention (Carl's working rule:
  verify a 'fails/permits' claim as hard as a 'works' claim)?

All load-bearing numbers re-derived by methods NOT sharing the route's code path.

---

## 1. INDEPENDENT RE-DERIVATION OF THE LOAD-BEARING RESULTS — ALL CONFIRMED

### (A) R = 4 j3/j2^2 = 8 Delta for the normalized-descendant measure  ✓ CONFIRMED
Script `agentSS_verify_p1_moments.py`. Two methods, neither the route's hand-summed central-moment loop:
- METHOD 1 — generating function Z(t)=0F1(;2D;t), raw power moments via the theta=t d/dt operator
  evaluated with mp.diff at t=1, then central j2,j3 by the standard raw->central conversion.
- METHOD 2 — independent direct Pochhammer summation with mp.fsum.

| Delta | R (method1) | R (method2) | 8·Delta | R−8D |
|------:|------------:|------------:|--------:|-----:|
| 0.5 | 4.313679028 | 4.313679028 | 4.0 | 0.3137 |
| 1.0 | 8.124665077 | 8.124665077 | 8.0 | 0.1247 |
| 2.0 | 16.03829557 | 16.03829557 | 16.0 | 0.0383 |
| 4.0 | 32.00839671 | 32.00839671 | 32.0 | 0.0084 |
| 8.0 | 64.00142641 | 64.00142641 | 64.0 | 0.0014 |
| 16  | 128.0002086 | 128.0002086 | 128.0 | 0.0002 |

Both methods agree to 10 digits and reproduce the route's tabulated values EXACTLY. R = 8Δ + O(1/Δ),
**monotone in the free probe dimension Δ.** The ratio is a SLIDING knob → on the residue axis the
SL(2,R) rep **PERMITS** any value ≥ ~4, lands on a specific G_sat only for Δ = G_sat/8 (tuning). ✓

### (B) Modular / dilation scaling weight of 4 j3/j2^2 = −1  ✓ CONFIRMED
Script `agentSS_verify_p2_dilation.py`. Explicit numeric dilation s_n → scale·n, measured weight
w = log(R/R_base)/log(scale): **w = −1.0000** at scale ∈ {0.5, 2, 5} (clean). Dimensional argument
re-derived from scratch: central j_n carries [s]^n ⇒ 4j3/j2^2 carries [s]^{3−4}=[s]^{−1}. A pure
dilation (= the static-patch boost = the Tomita–Takesaki modular flow of the KMS state) rescales a
weight−1 quantity freely; its only scale-fixed points are 0 and ∞. So modular flow **cannot pin**
4j3/j2^2 to a finite nonzero G_sat. ✓ The route's modular argument is sound.

### (C) Character-weight (2Δ)_n/n! divergence  ✓ CONFIRMED
Script `agentSS_verify_p3_kstruct_edge.py`. a_n ~ n^{2Δ−1}/Γ(2Δ) verified (ratio→1.0); the 2nd-moment
sum Σ a_n n^2 grows without bound (3.3e5→3.3e8→3.3e11 at Δ=0.5). So the character/Plancherel weight is
**not a normalizable line shape** and the normalized-descendant measure is the only normalizable
canonical residue. ✓ (This matters for §3 below.)

### (D) k0 vs k_H scale separation  ✓ CONFIRMED (and convention-robust)
k0/k_H = c_chi^2/√a0 (symbolic). k0==k_H ⟺ c_chi = a0^{1/4}, which contradicts banked super-luminal
c_chi^2≫1 (agentU/EE). The scales are **structurally** forced apart — and the qualitative decoupling
(k_H carries no a0 information, so it cannot place a feature at k0(a0)) does not depend on the
magnitude. NOT a tuned-convention artifact. ✓

### (E) Edge-window algebra σ6/σ6* = 8Δ/G ⇒ 6Δ<G<8Δ  ✓ CONFIRMED symbolically. ✓

**On the arithmetic and the named symmetry, the route is clean.** The static-patch SL(2,R)~SO(2,1)
discrete-series structure of the dS QNM ladder (Casimir Δ(Δ−1), uniform spacing, offset Δ, ladder
matrix elements (n+1)(2Δ+n)) is GENUINE, standard dS static-patch physics — not invented. The modular
flow = static-patch boost identification is the well-known Gibbons–Hawking KMS fact. So the symmetry is
REAL. The question is whether it FORCES — and the route correctly says no.

---

## 2. IS THE SYMMETRY REAL OR IMPOSED?  →  REAL, but it constrains the WRONG invariant

- **The rep is real.** SL(2,R) discrete-series ladder structure of the dS QNM tower is standard; the
  route did not invent it. ✓
- **The residue choice a_n=1/[n!(2Δ)_n] is the only normalizable canonical one** (§1C: the character
  weight diverges). So it is not cherry-picked among normalizable options — it is forced-by-normalizability
  among the SL(2,R)-canonical candidates. That is as close to "real" as the residue can get.
- **HOWEVER — the honest weakness the route names and I confirm:** the symmetry fixes the ladder
  STRUCTURE only **up to the free rep label Δ and an overall spectral SCALE.** The edge target is a
  weight−1 (scale-covariant) ratio measured against a scale-DECOUPLED external constant G_sat (c_chi
  physics). A dilation symmetry structurally cannot pin a covariant quantity to an external scale. So the
  symmetry is REAL but **constrains the wrong invariant** → it PERMITS, never FORCES. This is not an
  overclaim dressed down; the route states it plainly and the math (§1A,B,D) backs it.

## 3. DID THE SYMMETRY RE-INVOKE THE PASSIVE QNM agentPP KILLED?  →  NO (brief sub-question 3)

The sharpest adversarial worry: agentPP proved any PASSIVE (ρ≥0) spectrum → Herglotz → monotone → NO
fold. The route's moment ratio 8Δ comes from the **passive, all-positive** normalized-descendant measure
(§4G: a_n>0 for every Δ, min 6e-16…4e-21 — strictly passive). So PP's theorem applies to it directly:
this object CANNOT fold. Did the route smuggle this non-folding passive object in as a forcing mechanism?

**NO.** The route's logic, verified consistent:
- It uses the passive QNM moment ratio only to test the moment-RATIO coincidence (8Δ = G_sat ⇒ tuned Δ)
  → PERMITS on the residue axis.
- It then **explicitly** (Parts 6–7) notes the passive/bare heat-kernel memory is KMS → Herglotz → cannot
  fold (PP), and that a fold requires an ACTIVE line whose {center,width,Q,sign} are the agentRR N=4 FREE
  ratios — not heat-kernel-forced. The active branch is handled head-on; the passive object is never
  claimed to deliver a fold.

**The active-branch spine (Part 7) independently re-derived (§4F) — CONFIRMED:**
Im(δ1) = R·γ·(ω0−ωb) / [2ωb(γ²+(ω0−ωb)²)] ⇒ sign = sign(ω0−ωb). An active (negative-residue) gain line
destabilizes modes BELOW its center; the roton fold band (k<k0) IS the below-center band ⇒ the fold band
is the unstable band ⇒ a scalar clamp cannot fix it and a k-resolved clamp can only stabilize by KILLING
the gain there (no fold). The dS symmetry sector carries no spatial-k label (Part 8) and the heat-kernel
non-locality scale k_H is forced FAR from k0 (§1D), so the dS structure forces neither the stabilizing
k-step nor the fold. This is the correct structural reason the symmetry only PERMITS. ✓

**ONE IMPRECISION FOUND (verdict-neutral, cuts toward NEEDS-NEW-INPUT).** Part 7's "below-center =
unstable for ANY width γ" is a LEADING-ORDER (small-gain) statement. The exact finite-amplitude cubic
roots (§4F numeric, §5) show the unstable band STRADDLES the center — it extends above ω0 too — and only
collapses to exactly the below-center side as R→0+ (upper edge → ω0: 0.6008, 0.6040, 0.6081 → 0.6 as
R→0.001…0.01). So at finite gain the unstable band is WIDER than the clean theorem says. This makes
stabilization HARDER, i.e. the symmetry's failure to force a stable clamp is MORE robust. The imprecision
strengthens NEEDS-NEW-INPUT and could never produce forcing. Not a verdict-affecting error — a framing
refinement (the route should say "below-center to leading order in the gain" rather than "for any γ").

## 4. CONVENTION-ROBUSTNESS (Carl's working rule — verify a 'permits' as hard as a 'forces')

- The k0/k_H separation is NOT a convention artifact: even at the mildest super-luminality c_chi²~few it
  is ≠1, and the qualitative decoupling (k_H carries no a0 info) is magnitude-independent (§1D). ✓
- The modular weight −1 is dimensional, not convention-dependent (§1B). ✓
- Central moments are origin-independent, so the absolute-vs-detuning spectral-origin choice does not
  affect R (route Part 4; structurally true). ✓
- The PERMITS verdict therefore does NOT hinge on a textbook-default convention dressed up as a result.
  It is the convention-robust truth. ✓

---

## REGRADE — **CONFIRMED: NEEDS-NEW-INPUT** (PERMITS-MODEL-DEPENDENT at the route level)

The route claimed PERMITS-NOT-FORCES → NEEDS-NEW-INPUT. Every load-bearing number reproduces
independently:
- R = 8Δ (2 independent methods, exact to route's table) ✓
- modular dilation weight −1 (explicit numeric + dimensional) ✓
- character-weight divergence ⇒ normalized-descendant is the only normalizable residue ✓
- k0/k_H = c_chi²/√a0 forced apart; honest opening k0==k_H closed by super-luminality ✓
- edge-window 6Δ<G<8Δ ✓
- active level-repulsion spine: below-center band = unstable band ✓

The symmetry is **REAL** (genuine static-patch SL(2,R)/modular structure of the GH state) but **PERMITS,
not FORCES**: it fixes the ladder structure only up to a free rep label Δ and a free spectral scale, while
the edge target is a scale-covariant ratio against a scale-decoupled external G_sat — the one
configuration a dilation symmetry cannot force. It supplies **no spatial-k** to resolve the clamp. There
is **NO zero-parameter forcing**; landing on the edge needs a tuned Δ (or G hand-placed in (6Δ,8Δ) AND
simultaneously = the κ-set saturation AND the edge value — 3 conditions, 1 knob). The route did NOT
re-invoke the passive QNM as a forcing mechanism (it treats the active branch correctly and respects PP).

The default-skeptic posture in the brief ("assume forces is overclaimed until a zero-parameter forcing is
shown") lands exactly where the route already put it. **No overclaim to overturn; no hidden forcing to
rescue.** Regrade = **CONFIRMED**, regraded verdict = **NEEDS-NEW-INPUT** (equivalently
PERMITS-MODEL-DEPENDENT: the edge coincidence is permitted on a tuned 1-parameter line, not forced).

**Quarantine:** held throughout. Only signs, scaling weights, the RATIO 8Δ, the divergence class, the
scale-separation ratio, and pole-half-plane structure were computed. q=1/4, ζ̃, (16π/3)^{1/4} never
asserted.

**One more load-bearing structural check (§6 script):** is the modular flow REALLY a dilation (so the
weight−1 lens is right), or did the route mislabel a frequency TRANSLATION as a dilation? Settled: the
modular Hamiltonian ∝ L_0 (the boost/dilatation generator), whose spectrum IS the QNM ladder Δ+n; and
exp(a·s d/ds) generates s→eᵃs (verified infinitesimally, match=True). A translation s→s+a is a DIFFERENT
generator (d/ds) that does not preserve the lowest-weight tower. So the action is genuinely a dilation,
4j3/j2² genuinely carries weight −1, and the "cannot pin to finite G_sat" conclusion is structurally
correct — NOT an artifact of a mislabeled group action. ✓

**Scripts (this verification):** agentSS_verify_p1_moments.py (R=8Δ, 2 methods),
agentSS_verify_p2_dilation.py (weight −1), agentSS_verify_p3_kstruct_edge.py (char divergence + k0/k_H +
edge window), agentSS_verify_p4_active_theorem.py (active spine + passivity), agentSS_verify_p5_threshold.py
(finite-amplitude band direction), agentSS_verify_p6_modular_action.py (modular = dilation, not
translation). All in real_research/reviews/toe_law/.
