# AS652 — Four-form flux equation with a MOND-dependent scale

**Run:** `AS652-r1-20260928T140620Z-dsv4f-hermes`
**Worker:** dsv4f-hermes (subagent; deepseek/deepseek-v4-flash-0731 via openrouter, Hermes platform)
**Task:** `deepseek_push/astra_spawn_ideas/AS652_four_form_flux_equation_with_a_mond_dependent_scale.md`
**Task sha256:** `9f3281d9697c338ef70adb08f74f33f009a4a07ea2a86682a51b477613b50b2e` (verified == pinned)
**Branch (declared):** k04 four-form promotion (`kappa_closure/k04_four_form_promotion_consistency.py`, pinned sha256 `15c0a7e13eb9b7a5fdb403c8826bd01912d68dc81614609fddb6cd6ed9d32399`, verified == SOURCE_MANIFEST entry) × frozen-saturated RAR kernel. Conclusions are scoped to this branch only; Q, RAR, MU2, EXP, MONO enter nowhere except as the kernel's historical RAR ancestry, and filtered MONO / CA5-GNC-R are untouched.
**Mandatory framework:** a0 = κ c √(G_N ρ_Λ), κ = 1/2 **adopted as input** (this run derives what follows from it, not the half itself); r_M = √(G_N M_b/a0); v_flat⁴ = G_N M_b a0; G_N = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16 (SI), AU = 1.495978707e11 (IAU 2012).

---

## 1. Source equation, variables, boundary conditions, measure (seed step 1)

From the cited k04 branch the object of study is the local four-form sector with a
MOND-dependent scale:

```
F = q ε            (four-form field strength; ε = √−g d⁴x volume form; q the flux amplitude)
L(q) = P(q) + L_MOND(a0(q)),     P(q) = (Z/2) q² + b β² q²
a0(q) = β √(G_N) |q|,            L_MOND = −(2−K_B) J / (16π G_mon)
J = a0² j(s),   s = g_N / a0,    g_N = G_N M_b / r²   (quasi-static spherical sector)
branch identities (k04):  Y J_Y = a0² s Δ(s)  (phantom-force identity)
                          dJ/da0|_Y = (2/a0)(J − Y J_Y) = −2 a0 W(s),   W = s Δ − j
Δ(s) = s/(e^{√s} − 1) the RAR kernel, frozen at its peak for s ≥ s_sat:
s_sat = 2.53963828219, Δ_sat = 0.647610237892, j_sat = 0.452524896675 = I_rar (computed here,
matching k04's I = 0.4525).
```

- **Independent variables / measure:** spacetime volume measure √−g d⁴x on a compact
  domain; q is a spacetime *constant* on the smooth branch (the four-form is closed in 4D:
  dF = 0, a single global degree of freedom).
- **Variation & boundary conditions:** the flux equation comes from varying the 3-form
  potential A(3) (dA = F) with **compactly supported** δA; the boundary term is the flux.
  Because L depends on q only through q itself (no ∂q), the Euler–Lagrange equation for A is
  d(∂L/∂q) = 0 — not an algebraic stationarity condition in q (the k04 note's "four-form
  equation d_μ(∂L/∂q) = 0").
- **Domain of the seed:** smooth nonzero q branch, g_N ≥ 0, s ∈ (0, ∞), compactly supported
  potential variation, no time dependence, no new particle species.
- **Constants kept independent** (seed step 3): Z, β, b (≡ (2−K_B) I_rar/16π), K_B ∈ [0, 1/4],
  q₀, G_N (acceleration route), G_mon (MOND-sector Newton coupling), G_vac (vacuum curvature
  coupling). G_N ≠ G_mon ≠ G_vac are carried separately; on the k04 single-G branch the
  matching conditions G_mon = G_N (flux equation) and G_vac = G_N (Λ-identification) are
  stated, not silently imposed.

**Units** (check, all SI): [a0] = L T⁻². β √(G_N) q has [√G_N] = L^{3/2} M^{-1/2} T⁻¹ and
[q] = M^{1/2} L^{-1/2} T⁻¹, product L T⁻² ✓. β² q² = a0²/G_N has [M L⁻¹ T⁻²] = energy
density ✓. [Z q₀] = [∂L/∂q] = (energy density)/[q] = M^{1/2} L^{-1/2} T⁻¹ = [q] ✓
(integration constant is dimensionally a flux). β and Z dimensionless; b dimensionless.

## 2. Derivation of d_μ(∂L/∂q) = 0 and the integration constant (seed step 2)

Varying the 3-form potential: δS = ∫ (∂L/∂q) δq ε with δq ε = d(δA), so
δS = −∫ d(∂L/∂q) ∧ δA + boundary. Compactly supported δA ⇒

```
d_μ(∂L/∂q) = 0   ⇒   ∂L/∂q = Z q₀            (integration constant: the four-form flux datum)
```

**This is the seed's central instruction: the constant is kept; one does NOT set P_q = 0.**
Computing with a0 = β√G_N|q| (q > 0 on the branch, da0/dq = β√G_N = a0/q):

```
∂L/∂q = Z q + 2b β² q + (2−K_B) β² q W(s) (G_N/G_mon)/(8π) = Z q₀        (full variation)
```

The three terms: (i) Z q, vacuum kinetic; (ii) 2b β² q, q-variation of the promoted
primitive b a0²/G_N (see the refinement note in §8 — on the k04 gauge-fixed branch this
term is dropped; it is a uniform renormalization); (iii) (2−K_B) β² q W (G_N/G_mon)/(8π),
from ∂L_MOND/∂a0 = +(2−K_B) a0 W/(8π G_mon) (sign convention: L_MOND = −(2−K_B)J/16πG_mon,
the AQUAL-type kinetic sign; control S11 in §9 shows the opposite sign is excluded). The
sign convention reproduces k04's flux equation

```
q [ Z + (2−K_B) β² (s Δ − j)/(8π) ] = Z q₀        (gauge-fixed branch, G_mon = G_N)
```

which is the k04 F3 equation, here **derived** from ∂L/∂q = const rather than quoted.

**Sign & consistency of W:** W(s) = sΔ(s) − j(s) = 2∫₀ˢΔ − sΔ; since Δ/s = 1/(e^{√s}−1) is
strictly decreasing, W′(s) = Δ − sΔ′ > 0 and W(0) = 0, so **W ≥ 0 and strictly increasing**;
deep asymptote W ~ s^{3/2}/3 (verified numerically: W/s^{3/2} → 0.33333332, check K4).

## 3. Solved feedback equation (the local flux response)

Dividing the flux equation by Z q₀ with q = q₀ r, r = a0_loc/a0 ∈ (0,1]:

```
r ( 1 + (2−K_B) W(s_r)/(64π) · (G_N/G_mon) ) = 1,     s_r = g_N/(a0 r)     (Z = 8 β²)
```

Z = 8 β² is precisely the κ = 1/2 constraint (§4). Properties (all verified; checks
F3–F3d, S5–S7):

1. **Unique root:** F(r) = r(1 + (2−K_B)W(g_N/a0 r)/64π) − 1 is strictly increasing
   (dF/dr = 1 + α(W + rW′)/64π > 0), F(0⁺) = αΔ_sat g_N/(64π a0), F(1) > 1 ⇒ root exists
   in (0,1) **iff** g_N < g_*; the fixed-point map is a contraction at the root
   (max |T′| = 0.644 on the tested grid, check S5).
2. **Switch-off (fold):** g_* = 64π a0 (G_mon/G_N)/((2−K_B) Δ_sat) = **155.2 a0** (K_B = 0),
   = 177.4 a0 (K_B = 1/4); r(g_*) = 0 exactly in the saturated regime (check S7b — r = 0
   solves the flux equation at g_N = g_* because q·W(s(q)) → q₀ Δ_sat g_N/a0 there); for
   g_N > g_* **no smooth root exists** (checks S7c, F3d) and the only variational solution
   is the |q| kink q = 0 (subdifferential), i.e. the MOND scale switches off. This is exact,
   not a linearization artifact: g_* = 155.2 a0 = 1.4532828e-8 m/s² (canonical, K_B = 0),
   1.7508815e-8 m/s² (alternative) = 155.23 a0_alt.
3. **Saturated linear law (k04 F4):** in the frozen-kernel regime s_r = g_N/(a0 r) > s_sat the
   flux equation is linear in q, giving the exact form r = (1 − g_N/g_*)/(1 − 2 j_sat/64π);
   verified against the numeric root at g/g_* ∈ {0.1, 0.5, 0.9} to <1e-4 (check S7) and
   **Lean-certified as the algebraic identity R5**.
4. **Deep limit:** g_N → 0 ⇒ W ~ s^{3/2}/3 → 0 ⇒ r → 1: the global a0 is restored
   (r(1e-6 a0) = 0.999999999997, check S6). The MOND scale is not destroyed by the
   feedback; it is suppressed only where the environment demands it.
5. **Galaxy RAR shift:** for g_N ≤ 100 a0, |Δ log g_obs| ≤ 0.0018 dex < 0.01 dex across
   K_B ∈ {0, 1/4} and both footings (check F3); the flux profile reproduces k04's printed
   r(s₀) values to <5e-4 (check F3c, framework numerics).

## 4. Kappa and the coefficient (seed step 3 ledger)

Four-form stress (Bousso–Polchinski): ε_vac = q P_q − P = +Z q²/2 + b β² q² (F1 sign check
PASS: the promoted primitive gravitates positive). With a0²/(G_N ε_vac):

```
κ² = 2β²/(Z + 2bβ²)   ⇒   κ = 1/2  ⟺  Z/β² = 8 − 2b
b = (2−K_B) I_rar/(16π):  K_B = 0   → b = 0.018005,  Z/β² = 7.963989
                           K_B = 1/4 → b = 0.015755,  Z/β² = 7.968491
```

Independence ledger — what fixes what:

| constant | meaning | fixed by |
|---|---|---|
| q₀ | flux datum (integration constant) | the flux equation itself (∂L/∂q = Z q₀) — replaces the a0 datum: β q₀ = a0/√G_N (both footings, §7) |
| β q₀ | observed scale combination | observed a0 (canonical 1.145938e-5, alternative 1.380600e-5 kg^{1/2} m^{-1/2} s^{-1}) |
| Z/β² | vacuum/vacuum coupling ratio | **nothing**: κ = 1/2 ⇔ Z/β² = 8−2b, one equation, two couplings (flux amplitude cancels) |
| K_B, I_rar, Δ_sat, s_sat | branch data | the kernel; enter b and g_* |
| G_N/G_mon, G_vac/G_N | coupling ratios | matching conditions on the single-G branch (stated, not derived) |

**The core finding (F2, expected FAIL, matches k04):** the flux equation uses its one
degree of freedom (the integration constant) to make a0 *environmental*; it does not fix
the half. κ = 1/2 ⇔ Z/β² = 8−2b ≈ 7.96 remains a single unexplained number — the
"per-channel slope premise (λ = 1)" is **not** selected by the four-form flux equation.
This is consistent with the upstream chain AS053 (λ free, κ = 1/(2λ)), AS059 (κ = B/(8πAGn),
action fixes no coefficient), AS067 (vacuum zero-mode gauge): the four-form relocates the
freedom (a0 datum → flux datum + coupling ratio) but does not remove it.

## 5. Verification by substitution and independent representation (seed step 5)

- **Substitution:** the symbolic solution q = 8πZ q₀/(8πZ + (2−K_B)β² W)… of
  ∂L/∂q = Z q₀ has symbolic residual 0 (sympy); the numeric fixed point reproduces the
  flux equation with worst relative residual **4.21e-41** over the whole grid at 50 dps
  (check F3b). All reported results are residuals, not booleans.
- **Independent representation:** (i) the fixed-point map is a contraction (max |T′| = 0.644)
  ⇒ unique solution (check S5); (ii) the saturated linear law is derived independently by
  taking the exact r→0 limit of q·W(s(q)) and matches the bisection root to <1e-4 (S7);
  (iii) the switch-off endpoint r(g_*) = 0 and the no-root region g_N > g_* follow from the
  monotonicity of F (exact), not from iteration — k04's own iteration converges to the
  map's spurious fixed point r = 0 at s₀ = 1000, which is **not** a solution of the flux
  equation (documented correction, check F3d).
- **Scope:** smooth-q branch, g_N ∈ [0, g_*), K_B ∈ [0, 1/4], both footings, quasi-static
  spherical sector; outside g_* no smooth solution exists (|q| kink). The derived object is
  the unique environmental profile r(g_N) and its exact limits — not the time-dependent
  sector, not the coherence-length/xi sector, not filtered MONO.

## 6. Negative control (seed step 4; control capable of failing — it does)

**Altered premise: treat q as an unconstrained algebraic scalar.** Then the stationarity
condition is ∂L/∂q = 0 (no integration constant, exactly "setting P_q = 0"):

```
q [ Z + (2−K_B) β² W/8π ] = 0.
```

Since Z > 0 and W ≥ 0 (proven, §2), the bracket is strictly positive: the only solution is
**q = 0** (symbolic: solutions {0}, check S8; Lean R3). Consequences:

1. a0_loc = β√(G_N)|q| = 0 — the MOND scale is killed; at g_N = 0.1 a0 the RAR predicts
   g_obs/g_N = 1 + Δ(0.1)/0.1 = 3.69 (+0.567 dex); the altered premise gives 0 dex: the
   RAR signal is lost by 0.567 dex (check S8b).
2. No fine-tuned pole is available (Z + αW/8π = 0 impossible for W ≥ 0), so the premise
   admits **no nonzero MOND scale at all**.
3. Lost hypothesis: the compactly supported δA(3) variation and its boundary flux — the
   integration constant Z q₀. Dropping it removes the only mechanism that balances the
   MOND-sector pull on the vacuum flux.

The control behaves as required: it is a real test (it could have passed for a nontrivial
bracket zero) and it fails for the altered premise, pinning the integration constant as
essential.

## 7. Dimensional examples — both footings, separately

κ = 1/2 is held fixed (adopted); the two footings therefore differ in ρ_Λ (the task rule:
they may not share both a fixed density and a fixed κ):

| quantity | canonical a0 = 9.3619e-11 m/s² | alternative a0 = 1.1279e-10 m/s² |
|---|---|---|
| ρ_Λ = 4a0²/(G_N c²) | 5.844412454e-27 kg/m³ | 8.48308962e-27 kg/m³ (ratio 1.45149 = (a0_alt/a0_can)² ✓) |
| ε_Λ = ρ_Λ c² | 5.25269596e-10 J/m³ | 7.624220727e-10 J/m³ |
| β q₀ = a0/√G_N | 1.145938e-5 | 1.380600e-5 kg^{1/2} m^{-1/2} s^{-1} |
| g_* (K_B = 0) | 1.4532828e-8 m/s² = 155.2 a0 | 1.7508815e-8 m/s² = 155.23 a0_alt |
| r_M(1.5 M_sun) = √(G_N M_b/a0) | 0.047258 pc | 0.043055 pc |
| v_flat⁴ = G_N M_b a0 (1.5 M_sun) | 1.8637172e10 m⁴/s⁴ | 2.2453633e10 m⁴/s⁴ |
| Λ = 32π(G_vac/G_N) a0²/c⁴ | 32πa0²/c⁴ at G_vac = G_N | same with a0_alt |

The RAR profile r(s₀) is dimensionless and footing-independent (g_N = s₀ a0 cancels);
the physical witnesses (solar system, wide binaries, g_*) are footing-dependent and carried
separately in §9. The dimensionless theorem (flux equation, solution, bounds) applies to
both footings by the same algebra (Lean R1–R6).

## 8. Refinement: q-variation of the promoted primitive (2b β² q)

The full variation includes 2b β² q (∂P/∂q with the b-primitive inside P, per k04 F1).
Its effect: a uniform deep-limit renormalization r(0) = 1/(1+2b/8) = 0.99552 (−0.45%),
absorbed by q₀ (the observed scale is a0_loc, so this renormalizes the flux datum), and a
+0.45% shift of g_* (155.93 a0 vs 155.2 a0; check S10). Under the AS067 vacuum-zero-mode
gauge (Λ-compensated J(0)), this term is part of the gauge orbit, and k04's gauge-fixed
flux equation is the physical statement; the difference is documented, not hidden. All k04
comparisons use the gauge-fixed branch. The κ-consistency with the *deep-environmental*
a0_loc instead of the bare a0 shifts the Z/β² constraint by ~0.9% (Z/β² ≈ 7.89 at K_B = 0)
without changing the conclusion: the ratio stays unfixed.

## 9. Controls — capable of failing; results

| check | content | result |
|---|---|---|
| S1/S2 | task sha256 = pinned; k04 source = manifest | PASS |
| K1–K4 | kernel landmarks; W ≥ 0, strictly increasing; deep asymptote | PASS (Δ′(s_sat) residual 6.8e-59) |
| F1 | sign: ε_vac = qP_q − P = +Z q²/2 + bβ²q² | PASS |
| F2 | **action fixes Z/β²** | **FAIL (expected)** — the seed's core finding; one number undetermined |
| F3–F3d | unique root, <0.01 dex RAR shift, k04 repro <5e-4, s₀=1000 no root | PASS (max |Δlog g_obs| = 0.0018 dex; worst flux residual 4.21e-41) |
| F4/F4b | planets in switch-off core; residual 0 < a0/(2·1278); r_off = 638.8 AU ≈ 639 AU (XR31) | PASS |
| F5 | wide binaries |γ_v shift| < DR4 ±0.015 at 2 kAU | **FAIL (expected; as k04):** −0.0187 (canonical)/−0.0152 (alt); per XR31 the point sits on the C_L,eff < 0 band and is **not** a prediction |
| S4–S4c | peak of g_φ at 2.385 a0; C_L,eff(20 a0) = −238.62 < 0; fold to switch-off | PASS (XR31 reproduced with framework numerics) |
| S5–S7c | contraction; deep limit r→1; saturated linear; r(g_*)=0; no root beyond | PASS |
| S8/S8b | negative control: only q = 0; RAR lost by 0.567 dex | PASS (altered premise fails — as required) |
| S9/S9b | both footings; canonical ρ_Λ matches AS059 bookkeeping to 1e-6 | PASS |
| S10 | b-term refinement (0.45%) | PASS |
| S11 | **sign control:** opposite-sign coupling gives r > 1 (a0_loc = 2 a0 at W = Wpole/2, pole at W = 32π): runaway, no switch-off | PASS (alternative sign excluded) |

**Stability reading (corrected, per XR31 2026-09-27):** the flux equation has exactly one
root on the smooth branch (S5/S7), and W ≥ 0 keeps the *secant* stiffness positive — but
that is **not** a stability statement. The slaved scalar's longitudinal coefficient
C_L,eff = dg_N/dg_φ at fixed flux is **negative on the whole band g_N ∈ (2.385, 155.2) a0**
(g_φ peaks at 2.385 a0, then falls linearly to the switch-off): the static scalar equation
is not elliptic there, longitudinal perturbations grow (ω² = −0.86 (ck)² at λ = 1 per
XR31's chain-root analysis, not recomputed here — recorded as review-lane result), the band
covers ~17%/15% of SPARC points and wide binaries at 2–5 kAU, and the F5 row is therefore
not a prediction. This run reproduces the fold numbers (peak 2.385082 a0, C_L,eff(20 a0) =
−238.6234, g_* = 155.2 a0, r_off = 638.8 AU) independently with the framework numerics.

## 10. First-principles inputs vs derived equations

**Primitive assumptions:** the k04 branch form L = P(q) + L_MOND(a0(q)) with the four-form
amplitude coupling a0 = β√(G_N)|q|; AQUAL-type kinetic sign of L_MOND; frozen-saturated
RAR kernel with the branch identities Y J_Y = a0² s Δ, dJ/da0|_Y = (2/a0)(J − Y J_Y);
compactly supported δA(3); κ = 1/2 **adopted** (framework input); G_N/G_mon = G_vac/G_N = 1
as stated matching conditions on the single-G branch; d ln γ_v/d ln a0 = 0.1155 imported
from k04/DR4 (used only for the F5 witness, marked non-predictive).
**Measured calibrations:** G_N, c, M_sun, pc, AU; a0 footings 9.3619e-11 / 1.1279e-10.
**Derived equations:** d_μ(∂L/∂q) = 0 ⇒ ∂L/∂q = Z q₀; the flux equation
q[Z + (2−K_B)β²W/8π] = Z q₀ (gauge-fixed); the feedback identity
r(1 + (2−K_B)W(g_N/a0 r)/64π) = 1; g_* = 64π a0/((2−K_B)Δ_sat); saturated linear law; the
existence/uniqueness/fold domain theorem; κ² = 2β²/(Z+2bβ²) with κ = 1/2 ⇔ Z/β² = 8−2b.

## 11. First missing implication and suggested follow-ups

**Next unresolved implication (the closure bridge):** the flux equation removes the
environmental a0-datum degeneracy (a0_loc is now determined by the global flux and the
environment) but does **not** select the coefficient: κ = 1/2 ⇔ Z/β² = 8−2b ≈ 7.96 remains
one unexplained number, i.e. the per-channel slope premise λ = 1 (AS053) is still an input
— now in the cleaner form "why Z = 8 β² − 2b" (k04's closing statement), with the
additional open item that the static sector is non-elliptic on the band (XR31; the
coherence-length/xi kinetic term is still required). Transfer to the amended thirteen-item
target additionally requires the same action/source conventions and healthy counted DOFs
(the four-form itself contributes zero propagating modes; the slaved scalar's longitudinal
sector is the open health item).

**Child proposals (specifications ready, not dispatched — actual dispatch requires the
orchestrator):**
- **AS652.ch1 — flux-source term for the q = 0 branch** (task's authorized extension 2):
  add a four-form source density Q₀(x) (membrane/axionic coupling), flux equation
  ∂L/∂q = Z q₀ + Q₀; new hypothesis: Q₀ has its own healthy dynamics and the four-form
  stays non-propagating; controls: the q = 0 branch becomes a genuine discharge solution,
  the fold at g_* is shifted or removed, the C_L,eff band re-analyzed with the source.
- **AS652.ch2 — selection of Z/β² = 8 − 2b** (the λ = 1 question, now in coupling-ratio
  form): any equation that fixes the ratio (e.g. flux quantization q₀ = n q_e with the
  observed a0 fixing n·β q_e, or a kernel sum rule fixing I_rar vs Z/β²); dependency:
  AS652-r1 (this run) as the branch definition; controls: must leave κ = 1/2 on exactly
  one footing at a time and reproduce the F3 profile.
- **AS652.ch3 — stability repair:** the C_L,eff < 0 band requires the coherence-length
  (xi) kinetic term; the changed model must be labelled separately; controls: ellipticity
  of the static scalar equation restored on the band with the same flux equation in the
  ξ → 0 limit.

## 12. Limitations

This run does NOT: derive κ = 1/2 (it is adopted input; the four-form leaves Z/β² free),
establish stability of the static sector (the opposite: C_L,eff < 0 on 2.385–155.2 a0,
non-elliptic band), make a wide-binary prediction (F5 sits on the unstable band), transfer
to filtered MONO or the amended thirteen-item target, cover time-dependent or
non-spherical sectors, or constitute closure of gravity. The Lean certificate certifies
the real-algebra of the flux equation (R1–R6), not the physical mapping; a program exiting
zero is not a physical result.

## 13. Execution record

- `compute_as652.py` (this run's code): symbolic (sympy) + numeric (mpmath 50 dps),
  29 checks, 27 PASS + 2 expected FAILs (F2, F5), elapsed **45.45 s** (alarm(120) hard
  wall-cap enforced), max RSS **189.9 MB** (RLIMIT_AS cap not settable on this macOS —
  memory measured, not hard-capped: 189.9 MB ≪ 512 MB declared), single thread by
  construction. Raw outputs: `raw_output.txt`, `raw_output.json`, `raw_output.stderr`.
- Lean: `AS652_four_form_flux_equation.lean` — 8 theorems (R1a, R1b, R1c, R2, R3, R4, R5,
  R6), compiled with `lake env lean` in `fable_independent_2026/lean_2026`, EXIT=0, zero
  sorry/admit, `#print axioms` for every theorem = exactly {propext, Classical.choice,
  Quot.sound}. Output: `lean_compile_out.txt`.
