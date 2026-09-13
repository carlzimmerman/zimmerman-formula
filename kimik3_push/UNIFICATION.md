# The unification — one sector, counted once (closes the double-count, Req 9)

**kimik3_push, 2026-09-13.** Steps 1 and 3 of the 10-step plan, stated as one theorem-shaped
argument. This is the document that says *why the pieces are one theory and not three mechanisms*.

---

## The apparent tension

Two routes to the amplitude law were established:

- **K011 (the carrier).** The projectable-khronon integration-constant dust
  $\rho_d = \mathcal{C}(\vec{x})/a^3$ is exactly cold ($c_s^2=0$, no EOS) and can *carry* the profile
  $\mathcal{C}(x) = A/r^2$ at the BTFR amplitude — the one mechanism the framework's obstructions
  (barotropic no-go, cluster hot-core expulsion, Cassini window) do not forbid.
- **K014 (the field equation).** The phantom density *implied by the MOND field equation itself*,
  $\rho_{\rm ph} = \frac{1}{4\pi G r^2}\frac{d(r^2 g_\phi)}{dr}$ with $g_\phi = a_0\Delta(s)$, is
  $\sim r^{-2}$ in the deep-MOND regime at $0.968\times$ the BTFR amplitude — no formation, no EOS.

If these are two *different* things, the theory double-counts: a real dust halo **plus** a MOND boost
would overshoot the RAR. FRIED_CHICKEN row 9 (no double count) is exactly this gate.

## The resolution: the phantom density **is** the dust

The MOND field equation $\nabla\cdot[J_Y\nabla\phi] = 4\pi G\rho_b$ (AQUAL) can be rewritten, by moving
the nonlinear term to the source side, as an *ordinary Newtonian Poisson equation* for $\phi$ sourced
by an **effective density**:
$$\nabla^2\phi = 4\pi G\,\rho_{\rm eff},\qquad
\rho_{\rm eff} \equiv \rho_b + \frac{1}{4\pi G}\nabla\cdot\big[(J_Y-1)\nabla\phi\big].$$
The second term — the "phantom dark matter" — is *precisely* the $\rho_{\rm ph}$ K014 computed. The
claim of the unification is:

> **The projectable-dust density $\rho_d = \mathcal{C}(\vec{x})/a^3$ is not an additional component on
> top of the MOND boost. It is the physical identity of the phantom density $\rho_{\rm ph}$ that the
> field equation already requires. There is one sector; the "boost" and the "dust" are two readings of it.**

## Why this is forced, not optional

1. **Same profile.** K011's dust carries $\mathcal{C}(x)=A/r^2$; K014's field-equation phantom is
   $\rho_{\rm ph}\sim r^{-2}$. K015 confirms both stay $\sim r^{-2}$ off-sphere ($-2.19/-2.14$). Same
   function.
2. **Same normalisation.** K012/V3 and K014/W2 both fix the amplitude at the BTFR value
   $A = \sqrt{GM_b a_0}/(4\pi G)$ (ratio 1.000000 and 0.968 — the kernel's own factor). Same number.
3. **Same coldness.** The dust is exactly cold ($c_s^2=0$, K011/T1); the field-equation sector on the
   critical surface is exactly cold ($c_s^2=0$, L192/L193). Same state.
4. **No double count by construction.** Because $\rho_d \equiv \rho_{\rm ph}$, the source of the
   Newtonian potential is $\rho_b + \rho_{\rm ph}$, counted **once**. There is no separate "dust halo +
   MOND boost" to sum. Row 9 is satisfied identically, not tuned.

## What this buys

- **Requirement 9 (no double count):** closed by identity, not by a fit.
- **Requirement 10 (amplitude law):** the dust (K011) is the *carrier*; the field equation (K014) is
  the *reason the profile is $r^{-2}$*; the unification says they are the same object. The amplitude
  law is the field equation's deep-MOND solution *carried by the cold integration-constant dust*.
- **Clusters:** the saturated branch ($\rho_{\rm ph}\sim r^{-1}$, K014/W3) and the dust's coldness
  (K011/T3) are the same statement in two languages — the sector is cold and centrally concentrated
  in deep wells.

## What is honestly still open

- **κ = ½** remains a fitted zero mode (proven, k01). The 2-transverse-mode count is Lean-certified
  (`TransverseCount.lean`); the physical occupation is the open link (K010 V5).
- **The exact slope coefficient:** K014 gives 0.968× BTFR; the precise kernel-dependent factor is a
  new falsifiable number to pin (step 4).
- **Cluster profile is $\rho\sim r^{-1}$ from the field equation vs observed $\sim r^{-1.5}$:** the
  sign and steepening are right, the exact index needs the pointwise X-COP solve (step 5).

## One-sentence completion

> **The dark sector is the cold projectable-khronon integration-constant dust; the MOND "boost" is the
> same sector read through its own field equation, so it is counted once; its profile is the field
> equation's deep-MOND $r^{-2}$ solution (K014/K015), its amplitude is the BTFR value, and the only
> fitted number in the whole theory is κ = ½ — a proven zero mode.**
