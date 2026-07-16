# ONE-LOOP FINITE PARTS — RESULT
dS-Unruh MODIFIED-INERTIA framework (a0 = cH_Λ/Z = 9.36e-11 canonical / 1.13e-10 alt),
reasoned from its OWN premises. Date 2026-07-16. Repo FROZEN; all work in this directory.

**Headline (earned, not assumed):** the first quantum (one-loop) correction to the MOND
interpolation ν(y) is **computable in closed form**, and it splits cleanly:

- **Around exact de Sitter (O(du²)): a PROTECTION THEOREM holds** — the finite one-loop
  frame self-energy (diagram D1) is *exactly shape-uniform*, so it renormalizes only the
  overall coefficient (ρ_m / c_W) and gives **δν(y) ≡ 0** after the Newtonian anchor. This is
  proved from three independent legs, each a live machine check (no hard-coded pass).
- **On the quasistatic accelerated background: a GENUINE δν(y) channel exists** (diagram D2),
  the μ-independent nonanalytic Coleman-Weinberg piece — but its magnitude is either
  (physical fork) **~10⁻⁸⁶, structurally unobservable**, or (proxy-literal fork) catastrophic,
  in which case the honest reading **indicts the ρ_m = m²φ² proxy**, not the framework.
- The δν-carrying coefficient is **scheme-independent** (verified by an adversarial second
  regulator); the scheme-dependent parts are analytic and absorbed by c_W / an unpinned c_WW.

All five scripts exit 0; **37/37 checks PASS, 0 FAIL**, including three live negative controls.

---

## 1. Object and diagram organization
One-loop effective action for the external (u,g) background with the matter loop:

  Γ₁[u,g] = (1/2) Tr ln P,   P = −□ + m²(1 + sW),   W = u·K(□_u/a0²)u,  s = −1.

W is a **local multiplication operator** on the matter field (all K-nonlocality external —
banked, `oneloop_laneA_divergences.py`). Expanding Tr ln P in W:

  Γ₁ = (1/2)Tr ln(−□+m²) + (s m²/2)Tr[G W] − (s² m⁴/4)Tr[G W G W] + …

- **D1** = (s m²/2)∫√g G(x,x) W — the complete O(du²) dressing around dS (linear vertex zero
  by geodesy ⇒ Tr[GWGW] starts at O(du⁴)).
- **D2** = V_CW(M²(y)) on the quasistatic background, M²(y) = m²(1+sW(y)).
- **D3** (two-vertex bubble) suppressed by (q0/m)² ~ 10⁻⁸⁶; **D4** (graviton) out of scope.

## 2. D1 — the renormalized coincident dS propagator (`finite_D1_selfenergy.py`)
Schwinger-DeWitt coincidence-limit series, minimal coupling, on dS (R = 12H², Einstein space):

  [G(x,x)]_ren = (1/16π²){ m²[ln(m²/μ²) − 1] − 2H² ln(m²/μ²) + (29/15)H⁴/m² + … }

- Coefficients a₀ = 1, a₁ = R/6 = **2H²**, a₂ = **29/15 H⁴** (computed, not assumed).
- **Flat limit H→0 reproduces the CW route** 2 dV_CW/dm² = (m²/16π²)(ln(m²/μ²) − 1) — a genuine
  cross-check, not a fit.
- **H-dependent (a0 = cH/Z-sensitive) part is O(H²/m²)-suppressed** relative to the leading
  m² term (H²-coefficient exactly −2 ln(m²/μ²)/16π²); proton (H/m)² ~ **1.6e-84** (canonical),
  2.3e-84 (alt).
- **Shape-uniformity:** because dim-reg preserves dS invariance, [G(x,x)] is a **constant** on
  dS, so D1 multiplies the tree frame form ∫W by a z-independent constant: K_eff^D1 = (1+λ)K_tree,
  d(K_eff/K_tree)/dz = 0. **Condition N absorbs λ at every anchor y* ⇒ δν(y) ≡ 0 from D1.**

## 3. D2 — quasistatic δν, both honesty forks (`finite_D2_quasistatic_dnu.py`)
V_CW(M²(y)) with M²(y) = m²(1−W(y)). The μ-independent nonanalytic piece is
**(m⁴/64π²)(1+sW)² ln(1+sW)**. Taylor in x = sW: (1+x)²ln(1+x) = x + (3/2)x² + O(x³).

- The **linear** piece (coeff 1) is absorbed by condition N (renormalizes c_W / ρ_m).
- The **residual leading deformation is quadratic**: δL_res = (3 m⁴/128π²) W² — a *genuine*
  shape channel (not absorbable by a single normalization), sign fixed positive, vanishing at
  exact dS (W=0) as it must.
- **Fork P (proxy-literal ρ_m = m²φ²):** loop/tree ~ (m⁴/64π²)/ρ_m ~ **2.8e+38** (proton,
  galactic ρ_m ~ 1e-21 kg/m³). Catastrophic — the honest conclusion **indicts the proxy**
  (vacuum gravitating through K = the cosmological-constant problem imported through the vertex),
  not the framework.
- **Fork C (composite / normal-ordered ρ_m, the physically correct reading):** the W-vertex
  couples to *connected* matter fluctuations; loop/tree ~ (1/16π²)·max[(q0/m)², (H/m)²] ~
  **1.0e-86** (canonical), 1.5e-86 (alt). Thermal exp(−m/T) underflows. **Unobservable** in
  every regime (deep-MOND, RAR transition curvature, wide binaries all >70 dex below).
- **δν(y) = [fork prefactor] × [bounded O(1) y-shape]**; the observability verdict is
  map-independent (set by the prefactor). y*-anchor-window (1e10–1e13) spread and both-footing
  spread ≤ ~1e-96 — nothing flips.

## 4. Protection theorem, proved and broken (`finite_protection_theorem.py`)
O(du²) around dS: three legs, each a machine check —
(a) W is a multiplication operator (D1 vertex loop-momentum-independent);
(b) dS invariance ⇒ [G(x,x)] constant ⇒ uniform rescale of the tree form;
(c) linear vertex zero (geodesy, K(0)=0) ⇒ no other O(du²) channel.
**⇒ finite D1 self-energy is exactly shape-uniform ⇒ δν ≡ 0 after condition N.**
Precise breakage: (i) quasistatic W(y)≠0 [D2, ~1e-86]; (ii) disformal/T_uu vertex carries loop
momentum, deformation ~(q0/m)² ~ 4.8e-86; (iii) two loops break uniformity (extra 1/16π²);
(iv) graviton loop — protected only by the TT-vertex zero, **CAS-verified n=1,2 ONLY** (see §6).

## 5. Scheme separation + adversarial second scheme (`finite_scheme_independence.py`)
- **Scheme-independent:** the invariant d³V/d(M²)³ = **1/(32π² M²)** in *both* dim-reg MS-bar
  and a proper-time hard cutoff (numerically, all M² and all Λ) — this fixes the nonanalytic
  (m⁴/64π²)(1+sW)² ln(1+sW) coefficient uniquely. So δν's **shape and sign are scheme-robust**.
- **Scheme-dependent (absorbable):** the UV scale (μ vs Λ), the additive constant, the
  quartic/quadratic UV pieces — all analytic in M² (polynomial in W), absorbed by condition N
  (c_W) and the **unpinned Wilson coefficient c_WW** (a new operator, no tree counterpart — its
  constant is *not* fixed by any single matching condition; reported, not invented).
- The scheme *difference* V_A − V_B has vanishing nonanalytic content (verified).

## 6. Honesty flags (stated plainly)
- **The Task-3 "TT-vertex-zero all orders n" script**
  (`open_doors_2026_07/mi_oneloop_tt_vertex_all_n.py`, commit e37c7144) has **both check()
  calls hard-coded True (lines 56, 66)** — confirmed by direct read. It is a printed *argument*,
  CAS-verified only n=1,2 (in laneB). The graviton-loop protection leg (iv) rests on that
  unproved all-n claim; it is flagged and left out of scope here.
- **ρ_m = m²φ² is a stated proxy.** Fork P's catastrophe is a statement about the proxy's
  domain of validity, not a framework result. The physical verdict is Fork C.
- **W(y) map** used in the δν(y) shape plot is a representative bounded interpolation
  (W = 1/(1+y)), labeled as illustration; the *magnitude/observability verdict does not depend
  on it* (it is set by the fork prefactor).
- Nothing here derives s, a0, or Z — they remain inputs, as always.

## 7. Verdict
The one-loop finite correction to ν(y) is **computed**: exactly zero at O(du²) around dS
(protection theorem), and on the quasistatic background a genuine but **quadruple-suppressed**
δν(y) ~ (1/16π²)(H/m)² ~ 10⁻⁸⁶ in the physical fork — the first quantum correction to a MOND
interpolation, with explicit suppression powers, **structurally unobservable**. The proxy-literal
fork's catastrophe indicts the proxy, not the framework. The result is footing-invariant and
scheme-robust. This does **not** close the theory — the disformal ρ_m variant, finite two-loop
parts, graviton-loop all-n TT protection, and T_μν metric variation remain open.
