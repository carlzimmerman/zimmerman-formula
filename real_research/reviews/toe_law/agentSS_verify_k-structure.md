# agentSS HOSTILE VERIFICATION — is the dS heat-kernel symmetry REAL and does it FORCE the edge surface, or merely PERMIT? (referee pass, 2026-06-13)

**REGRADE: CONFIRMED. The route's verdict NEEDS-NEW-INPUT stands, and survives the sharpest attack.**
All five load-bearing computations independently re-derived (separate code path, separate methods);
every number reproduced. The claimed symmetry is REAL (the static-patch SL(2,R)~SO(2,1) / modular
structure of the GH state genuinely exists and organizes the QNM tower) but it PERMITS, does not
FORCE — there is NO zero-parameter forcing of 4 j3/j2^2 onto G_sat. The route did NOT manufacture a
win and did NOT re-invoke PP's passive object to fake forcing.

## CENTRAL MISSION ANSWER

- **Is the symmetry REAL or IMPOSED?** REAL. The dS static-patch SL(2,R) (the QNM ladder is its
  lowest-weight discrete-series rep) and the modular/Tomita–Takesaki flow of the KMS GH state (= the
  static-patch boost) are genuine structures of the banked dS heat-kernel, not hand-inserted. Verified:
  the discrete-series rep data (Casimir, uniform spacing, offset Δ, ladder matrix elements) is exactly
  what fixes the only normalizable spectral measure.
- **Does it FORCE or PERMIT?** PERMITS. Two independent reasons, both re-derived:
  (1) the rep fixes the moment ratio only up to the FREE probe dimension Δ: **R = 4 j3/j2² = 8Δ**, a
      sliding knob — landing on G_sat needs Δ = G_sat/8 (tuning);
  (2) modular flow is a DILATION and **4 j3/j2² has scaling weight −1**, so a dilation can slide it to
      any finite value but pins none (scale-fixed points only 0, ∞). The edge equation matches G_sat at
      exactly one rapidity frame = tuning.
- **Zero tuned parameters?** NO. Forcing would require Δ pinned AND the gain amplitude G driven into the
  25%-wide window 6Δ<G<8Δ AND G simultaneously equal to the κ-set saturation value — 3 conditions on
  effectively 1–2 free knobs. Generically unequal (matches agentRR's measured 10–266× roam).

## RE-DERIVATIONS (independent code path, not the route's scripts)

### 1. The level-repulsion SPINE theorem — CONFIRMED (symbolic + full nonlinear root-find)
Re-derived `Im δ₁ = R γ (ω₀−ω_b)/[2 ω_b((ω_b−ω₀)²+γ²)]` from a self-energy I built independently, and
verified `Im Sigma_R(ω₀)>0` (genuinely GAIN). The **full complex Newton root-find** of
ω²−c²k²−Σ_R(ω)=0 reproduces the linearized sign at every k: pole UHP for ω_b<ω₀ (below gain center),
LHP for ω_b>ω₀. So the fold band k<k₀ IS the UHP-unstable band — exact, not perturbative.
*Branch check:* the PASSIVE line (positive residue, PP's object) is LHP everywhere below center
(stable, cannot fold); the ACTIVE line (negative residue, QQ's required deliverer) is the unstable one.
The spine acts on the ACTIVE branch — no passive smuggle. The would-be fold (dip in dω²/dk²) sits at/below
the gain center, inside the unstable band, so it is unreachable on the stable side. *(Minor: my dispersive
min dω²/dk²=+0.88 vs route's +0.97 — both positive, difference is the chosen R/γ; the structural fact holds.)*

### 2. The moment ratio R = 8Δ — CONFIRMED to the digit, by THREE methods
- Direct discrete summation of a_n=1/[n!(2Δ)_n]: R = 4.314, 8.125, 16.038, 32.008, 64.001, 128.000,
  256.000 at Δ=0.5…32 — matches the route's table exactly.
- Origin-independent (absolute s_n=Δ+n vs detuning s_n=n agree to machine precision — central moments).
- Poisson asymptotic (a_n→(1/2Δ)ⁿ/n!, rate p=1/2Δ, j2=j3=p ⇒ R=4/p=8Δ) — independent, agrees.
- The OTHER canonical residue (character weight (2Δ)_n/n!) genuinely DIVERGES (a_n~n^{2Δ-1}, second
  moment cutoff-dominated) — not a normalizable line shape, correctly discarded. So the normalized
  descendant is the only canonical choice, and its ratio SLIDES with the free Δ. **PERMITS.**

### 3. Modular dilation weight −1 — CONFIRMED (numeric + dimensional)
Scaling the spectral axis s→αs gives j2 ratio=α², j3 ratio=α³ exactly, and **R·α=const** (16.038 at
every α). Dimensionally 4 j3/j2² = [s³]/[s²]² = [1/frequency], weight −1. A weight-(−1) quantity hits a
finite target at exactly one rapidity a=ln(R₀/G) ⇒ tuning. The smooth GH thermal continuum is moreover
broad (moments diverge with cutoff), scale-free, no finite-Q peak — modular flow carries no intrinsic
scale to place a feature at k₀. (Independently reproduces the banked "smooth GH continuum → no fold".)

### 4. k-structure / scale separation k₀/k_H = c_χ²/√a₀ — CONFIRMED, robust, harder test passed
- Symbolic: k₀=(c_χ/√a₀)H, k_H=H/c_χ ⇒ ratio c_χ²/√a₀; k₀=k_H needs c_χ=a₀^{1/4}≪1, contradicted by the
  banked super-luminal c_χ²=O(γ/α)≫1 (agentEE line 66, a flat/PPN datum). Scales FORCED APART, k₀≫k_H.
- The route's Part 4/5b tested k_H~k₀ (O(1)). I ran the HARDER, more honest k_H≪k₀ (the actually-forced
  separation): all four admissible smears (screened-Coulomb, Lorentzian, Gaussian-horizon, hard-sphere)
  give R_below/R_above ~ O(1), NEVER ~0 — the kernel is decayed long before k₀, depletes nothing on the
  fold band. **Steelman (mine):** an ideal hard low-pass produces the required step-down ONLY if its
  cutoff = k₀; with the forced k_H≪k₀ it fails. To get the step you must inject k₀ into the kernel by
  hand. Robust to a0's value (even a0~O(1) ⇒ ratio=c_χ²≫1). PERMITS-not-FORCES.

### 5. Edge-window geometry 6Δ<G<8Δ — CONFIRMED (pure algebra)
σ6/σ6* = (4 j3/j2²)/G = 8Δ/G; bounded-fold window (1,4/3) ⇒ 6Δ<G<8Δ (25% wide); edge-exact G=8Δ sits at
σ6/σ6*=1 (the soft sonic-edge boundary). One equation on two free knobs = codim-1 PERMITS. Reproduces
agentRR exactly.

## THE SHARPEST ADVERSARIAL CHECK (did the route fake forcing via a passive→active smuggle?)
The symmetry route computes moments of the PASSIVE QNM descendant tower (positive weights), but the
deliverer must be ACTIVE (negative residue, per QQ). Does the dilation obstruction even apply to the
active line? **YES, and it makes the verdict stronger.** I built a SKEWED ACTIVE (negative-residue)
line shape and confirmed R·α=const (weight −1) for it too — the overall residue sign cancels in the
RATIO 4 j3/j2². So "a dilation cannot pin the ratio to G_sat" is residue-sign-INDEPENDENT and applies
to the active deliverer. If anything the symmetry is LESS constraining on the active line (its residues
are extra free data beyond the passive tower). The route argues the symmetry CANNOT force REGARDLESS of
branch — it did NOT re-invoke PP's passive object to manufacture forcing. HONEST.

## ONE HONEST DEPENDENCY (flagged, both directions per the working rule)
The entire "permits not forces" verdict hinges on the **c_χ ↔ H decoupling**: G_sat is c_χ-set (sonic-edge
dispersion, a flat/PPN khronon datum present at H=0), the spectral axis is H-set. Because they do not
co-dilate, the edge equation is NOT scale-covariant and the modular dilation genuinely breaks the match.
If a future input TIED c_χ to a power of H (making the edge eq scale-covariant), the dilation could no
longer break it and the verdict could shift toward PERMITS-MODEL-DEPENDENT. None is banked (agentRR
CHECK5: no c_χ↔H collapse; agentEE: c_χ from γ/α). Absent that, forcing is genuinely absent. This is the
single load-bearing external assumption and it is structural, not a convention artifact.

## QUARANTINE
Held. Only computed: pole-shift signs, R_crit ceiling, the moment RATIO R=8Δ (a ratio/scaling, not the
coefficient), the modular weight (−1), scale ratios (k₀/k_H), the edge window (6Δ,8Δ), Herglotz
monotonicity. q=1/4, ζ̃, (16π/3)^{1/4} never asserted.

## VERDICT
**CONFIRMED — NEEDS-NEW-INPUT.** The claimed symmetry is REAL but PERMITS, does not FORCE: every
candidate (SL(2,R), modular/KMS, SO(4,1)) reduces to a scale label + a scale-free dilation, and the edge
condition needs a weight-(−1) ratio pinned against a scale-decoupled external constant — the one
configuration a dilation provably cannot force. No zero-parameter forcing exists; landing on G_sat is
tuning (Δ=G_sat/8, or G into the 25% window). The dS heat-kernel symmetry supplies no intrinsic
spatial-k label to k-resolve the clamp either. The forcing symmetry is NOT in the banked machinery; the
deliverer remains a hand-set finite-Q active-but-stable line (RR's N=4 free ratios).
