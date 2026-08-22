# FIRST-PRINCIPLES VERDICT — the frozen tidal-khronon action
2026-08-22.  10-agent derivation program + hostile referee, every load-bearing claim
sympy-verified in committed scripts (`theory_2026/first_principles/`, ~250 checks green).
Adversary re-derived the EH quadratic, the Weyl/slip split, and the DOF count with
independent code: **all four attacks failed; phase-1 survives.**

## The 13 questions

| # | Question | Answer | Status |
|---|---|---|---|
| 1 | Action mathematically well-defined? | Yes. F is C^1 at X=0: the sqrt(X) pieces CANCEL between -2 sqrt(X) and 2 ln(1+sqrt(X)); F = -X + (2/3)X^{3/2} - X^2/2 + ... Quadratic action around Minkowski EXISTS; breakdown only at cubic order (deep-MOND strong coupling at sqrt(l_Pl c^2/a0) ~ 0.13 mm). | DERIVED |
| 2 | Does the variation produce the claimed weak-field equation? | Not as written. The TRUE system is two-potential: (I) lap Psi + div[(F_X - eta_K/2 + eps A'Y) grad Phi] = 4 pi G rho (lapse; carries mu AND matter); (II) lap(Psi-Phi) = -(eps c^4/a0^2) d_i d_j[A S_ij[PSI]] (spatial; carries the tidal operator, 4th order, slip at O(eps)). The single-potential schematic is recovered EXACTLY as the O(eps) on-shell effective equation **iff eta_K = 0**. | DERIVED |
| 3 | Newtonian gravity recovered? | Yes — the "1" in mu = 1+F_X is delivered by lap Psi through (II), not by an a^2 term. G_local = G/(1-eta_K/2). | DERIVED |
| 4 | Deep MOND recovered? | Yes, **iff eta_K = 0**: any eta_K != 0 shifts the kernel to 1-eta_K/2+F_X -> -eta_K/2 as x->0 and destroys the deep-MOND limit. Independently, the stability analysis finds eta_K = 0 is the UNIQUE choice keeping the khronon gradient-stable at every finite X (eta_K>0 reproduces the Blanchet-Skordis low-k instability; eta_K<0 is Newtonian-unstable). Two unrelated derivations force the same point. | DERIVED |
| 5 | BTFR? | v^4 = G M a0 exact, coefficient 1; the Y-sector changes neither asymptote (relative corrections 4 chi x^6 inward, (4/3) chi x^-5 outward). | DERIVED |
| 6 | Hidden extra DOF? | No. pi^ij unchanged by F; lapse eq is elliptic (determines N), not a constraint; count = (20-12-2)/2 = **3 = 2 tensor + 1 khronon**. Rbar^2 adds only spatial derivatives. Adversary confirmed. | DERIVED |
| 7 | Hamiltonian healthy? | Energy functional is a saddle (GR conformal-mode analogue — standard); at eps = 0 the reduced functional is convex + ray-coercive => Bekenstein-Milgrom-type uniqueness. No-ghost: lam_K > 1 (with FLRW sign requiring lam_K > 1/3; G_cosmo = 2G/(3 lam_K - 1), so BBN/CMB push lam_K -> 1). eps >= 0 required (eps < 0 gradient-unstable). | DERIVED (with the marginal boundaries noted) |
| 8 | Scalar stable? | At eta_K = 0: gradient-stable at every finite X, marginal (c_s -> 0) in deep MOND — strongly coupled, never unstable at finite x; superluminal ~ x^2 in the Newtonian regime (allowed with a global time function; Cherenkov/PPN watch). | DERIVED / marginal |
| 9 | Relativistically consistent? | gamma_PPN = 1 EXACTLY at eps = 0, at every X, parameter-free (regularity of (II)). Slip at O(eps): gamma-1 ~ -(16/5) chi x^-3, utterly negligible at Saturn. c_T = c EXACTLY around X = 0 (mu-sector cannot shift c_T at ANY background: X carries h_ij undifferentiated). alpha_1, alpha_2 derived, khronometric cross-check consistent, bounds satisfiable. FLRW: X = Y = 0, F(0,0) = 0 exactly (no induced Lambda), continuity holds, khronon redundant on FLRW. WEP holds; no tree-level fifth force. | DERIVED |
| 10 | Tidal operator natural? | The action is GENERIC at 2-derivative order but omits allowed 4th-order operators ((3)R^2, standalone Rbar^2, (Lie_u K)^2, ...) which loops regenerate. | REQUIRES NEW ASSUMPTION |
| 11 | eps natural? | No symmetry protects it. And see the kill below. | REQUIRES NEW ASSUMPTION |
| 12 | a0 derived? | **No. Input.** F contributes nothing on FLRW; the action supplies no dark energy of its own. | REQUIRES NEW ASSUMPTION |
| 13 | Extra operators required? | For consistency, no; for naturalness, yes (see 10). | UNRESOLVED |

## THE KILL — GW170817 forces the Y-sector inert

Rbar_ij is built from the spatial metric the wave lives in, so **Y is not tensor-silent**:

    omega_T^2 = c^2 k^2 [ 1 + 2 eps A(X0) (k c^2/a0)^2 ]

The (k c^2/a0)^2 factor is Lambda-ANTI-suppressed: 4e42 at LIGO frequencies.  GW170817
(|v_gw - c|/c < 1e-15) forces

    eps < ~5e-54   (Milky-Way path segment, A ~ 0.03; worst case 1.3e-57; absolute IGM floor 8e-47)

against the **eps ~ 1.1e-24** the Solar-System suppression window requires.
**Excluded by ~29 orders of magnitude.**  The same gap kills any O(1) static Y-effect at
cluster scales (needs eps A ~ 1e-11 vs allowed 3e-55).  As frozen, the tidal sector is
phenomenologically zero; the theory collapses to eta_K = 0 khronometric MOND — healthy,
but with the full DHF/Cassini tension of AQUAL mu_1.

## The minimal theoretically justified repair (identified, NOT adopted — next iteration)

Replace the spatial-curvature invariant with the ACCELERATION-tidal invariant Carl proposed
earlier in this program:

    Y_a = (c^8/a0^4) D_<mu a_nu> D^<mu a^nu>       (a_mu = D_mu ln N: built from the LAPSE)

* Static sector: D_<i a_j> = (1/c^2) S_ij[Phi] — the single-potential equation becomes
  FUNDAMENTAL, and tonight's linear-response number dq_zz/dchi = +0.30/+0.41 carries over
  UNCHANGED at O(eps) (S[Psi] = S[Phi] + O(eps)).
* Tensor sector: a_i = 0 identically at N = 1, so the operator has no (d^2 gamma)^2 content;
  the k^4 anti-suppression disappears. GW170817-safe at eps ~ 1e-24 (residual c_T shift
  ~ eps A X0 with no k-enhancement, ~ 1e-25).
* Slip: the Psi-equation is untouched at O(eps): gamma_PPN = 1 survives.

This is a NEW action and restarts the checklist (variation, DOF, stability) — not tonight's
theory.  It is recorded here as the repair the program's own rules require us to name.
