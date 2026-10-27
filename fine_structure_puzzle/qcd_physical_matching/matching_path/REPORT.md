# FSP-006 matching path: a real QED finite-volume effect and an exact vacuum cancellation

Parent FSP-005. Scope: this directory only. Prior reports and the original target are unchanged. No measured alpha, cosmic density, fitted QCD scale, proton electromagnetic mass, installation, Git command, or large job was used.

**Result.** Holding a finite-volume charged-proton mass fixed by retuning the strong scale can create an apparent alpha Lambda^3/L change in the flat vacuum baseline. Its universal torus factor is -c1/2=1.4186487397403..., but its remaining coefficient is an independent flat-vacuum derivative. It cancels exactly when each vacuum is subtracted against the flat vacuum of the same microscopic theory. This is a concrete calibration effect that can imitate the proposed scaling; it is not an evaluated intrinsic QCD vacuum response and does not transfer from a QED_L torus to S4.

## 1. The constrained current insertion is an operator, with scalar and trace terms

Use alpha=e^2/(4 pi), ell=ln Lambda, and declared QCD+QED invariant quark masses mhat_i. Let M be the infinite-volume proton rest threshold in one infrared prescription. Hold all mhat_i and M fixed, with M_ell != 0. Define matched action derivatives at a common regulator:

    I_hat_alpha,g = partial_alpha S_mat |_ell,mhat,
    O_ell,g = partial_ell S_mat |_alpha,mhat,
    K_alpha,g = I_hat_alpha,g - (M_alpha/M_ell) O_ell,g.       (1)

At alpha=0, I_hat_alpha=4 pi I_hat, where I_hat contains (1/2) integral j D_g j and the counterterms required by the fixed invariant-mass and charge convention. The action has S_eff=S_QCD+e^2 I_hat+O(e^4). Every sea, valence, disconnected and contact contribution is included.

If m_i(mu)=mhat_i exp u_i(alpha,ell), the scalar insertion integral m_i qbar_i q_i is multiplied by u_i,alpha-u_i,ell M_alpha/M_ell; analogous strong-coupling and charge-threshold derivatives are present. Holding invariant masses does not eliminate running-mass retuning. In arbitrary coordinates y^A, the exact formula is K=partial_alpha S|y+sum_A (dy^A/dalpha)partial_A S. This remains valid with mixed mass/coupling conversion matrices.

At alpha=0 the RG trace realizes the strong-scale insertion:

    O_ell = integral [Theta_QCD-sum_i m_i qbar_i q_i]
            + identity and curvature contacts,
    Theta_QCD = beta_s [G^2]_R/(2g_s)
                 +sum_i(1+gamma_i)[m_i qbar_i q_i]_R,
    M_ell = M-sum_i sigma_i,     sigma_i=mhat_i partial_mhat_i M.         (2)

Here beta_s=mu dg_s/dmu, gamma_i=-mu dln m_i/dmu, and G is canonically normalized. In rescaled gauge variables mathcalG=g_s G, S_g=integral mathcalG^2/(4g_s^2); dg_s/dell=-beta_s gives the same sign in (2). At nonzero alpha, the full QED trace, mixed beta functions and matching must be retained through (1); the pure-QCD expression alone is insufficient.

The proton functional H_p[X]=lim_T[<N(T)Nbar(0)X>/<N(T)Nbar(0)>-<X>]/T obeys H_p[K]=0. Its sign follows from C(T) proportional to exp(-MT) and dln C=-<X>_connected. Meanwhile dW_g/dalpha=<K_g>, plus independently prescribed gravitational-counterterm derivatives. Vanishing connected proton response does not imply vanishing vacuum response.

The identity counterterm cancels from H_p but remains in W_g. In particular the local cosmological coefficient v in integral sqrt(g) v is independent of proton/quark matching. The current-product mixing is checked in [de Divitiis et al., arXiv:1303.4896v1, section 2](https://arxiv.org/abs/1303.4896v1); the pure-QCD trace and hadron normalization are checked in [Metz–Pasquini–Rodini, arXiv:2006.11171v2, equations (12), (23), (26)](https://arxiv.org/abs/2006.11171v2). Neither source evaluates the requested geometric vacuum coefficient.

## 2. Primary finite-volume input and coefficient

[Davoudi–Savage, arXiv:1402.6741v2](https://arxiv.org/abs/1402.6741v2), section II and the leading terms of equation (19), uses infinite time and a periodic cubic spatial torus of side L with all spatial photon zero modes removed at each time, QED_L. For a rest proton at large L,

    M_L-M_infinity = alpha Q_p^2 c1/(2L)+O(alpha/L^2),
    c1=-2.83729...,     Q_p=1.                              (3)

Strong finite-volume effects are exponentially small at positive hadron mass. No higher-order structure terms or numerical hadron inputs from the source are used. The leading shift is negative. Higher-order fermion subtleties do not affect the retained 1/L term.

Let ell_0 tune M_infinity=M_* and ell_L instead tune M_L=M_*. With the same alpha and invariant quark masses,

    delta ell=-alpha Q_p^2 c1/[2L M_ell]+O(L^-2,alpha^2/L).   (4)

The induced shift in a flat vacuum baseline E_0 is therefore

    E_0(ell_L)-E_0(ell_0)=A_art/L+...,
    A_art=-alpha Q_p^2 c1/2 * E_0,ell/M_ell.                 (5)

With a held independent v and a homogeneous matter convention E_M=Lambda^4 B(x), M=Lambda C(x), x_i=mhat_i/Lambda,

    A_art=-alpha Q_p^2 c1/2 * Lambda^3
       [4B-sum_i x_i partial_i B]/[C-sum_i x_i partial_i C].  (6)

This gives the requested alpha Lambda^3/L structure, including the exact factor. The derivative ratio is not universal or numerically evaluated. Its sign is not fixed. The regular-branch condition M_ell != 0 is essential.

## 3. Which subtraction retains it?

Define F_L(theta)=E_L(theta)-E_0(theta), using the same microscopic parameters and v on both terms.

| Definition | Consequence for the retuned flat baseline |
|---|---|
| E_L(theta_L)-E_0(theta_0) | Retains A_art/L: it compares different material theories. |
| E_L(theta_L)-E_0(theta_L) | Cancels that baseline exactly, before expansion. |
| Tune M_L-alpha Q_p^2 c1/(2L), then compare | Avoids the leading calibration shift at O(alpha/L). |

The exact decomposition is

    E_L(theta_L)-E_0(theta_0)
      = F_L(theta_L)+[E_0(theta_L)-E_0(theta_0)].              (7)

Equation (7) isolates the contaminating term without assuming that the genuine F_L vanishes. If F_L has no 1/L contribution uniformly on a smooth nearby parameter branch, same-theory subtraction does not generate one. If F_L already has A_int(theta)/L, the O(1/L) retuning changes its coefficient only at higher order. No claim excludes an independent global QCD response.

At insertion level partial_alpha M_L=M_alpha,infinity+Q_p^2 c1/(2L)+..., so the extra O_ell term in (1) gives precisely (5). Its flat expectation cancels only when the flat subtraction uses the same ell_L path.

## 4. The independent cosmological coefficient matters across theories

For E_0=E_M+v, replace E_0,ell in (5) by E_M,ell+v_ell. Holding v as an independent dimensionful parameter generally retains the cross-theory shift. Imposing the additional condition E_0(theta)=0 along the family requires v(theta)=-E_M(theta) and removes it. Proton matching does not select either gravitational family.

A pure finite subtraction change shifts E_M and v together at fixed total theory; that does not change E_0,ell. Independently changing the physical v is a different gravitational theory. At fixed theory a local cosmological term is independent of L and cancels from the vacuum difference. Its composition with a retuned ell(L) can have 1/L dependence across theories. Thus (5) can be meaningful for an explicitly specified family of different theories, while it is not an intrinsic geometric observable of any one of them.

## 5. Geometry and stress cannot be transferred

QED_L has a nonlocal spatial zero-mode prescription and permits a charged sector through that modified constraint. It is not the ordinary smooth theory on closed S4. No substitution L=H^-1 is established, and no torus coefficient is claimed for sphere curvature.

On the parent's S4 prescription, actual stress uses partial metric differentiation at fixed microscopic couplings: rho_E=(1-(H/4)partial_H|theta)f. A comparison path theta(H) must be inserted only after that differentiation. A flat-baseline term evaluated along ell(H)=ell_0+dH contributes A_base H to actual evaluated stress. Applying a total derivative to f(H,ell(H)) instead gives 3 A_base H/4. That is a path-derivative pseudo-stress, not the stress tensor. The coefficient in (5) belongs to the evaluated vacuum baseline; no 3/4 factor multiplies it.

Likewise P(D)=D(D-2)(D-4) removes local counterterms only when its geometric D holds couplings fixed. A cross-theory b0(ell(H)) can contain a linear H term and survive P. A fixed-parameter sphere stencil with flat matching retuned only across alpha avoids this error.

Subject to existence and interchange of the required limits, the constrained physical sphere response is the projected metric response of <K_alpha,g>/V_g, using (1), followed by division by M^3 for dR/dalpha. The source of the remaining uncertainty is the unevaluated common-regulator vacuum expectation, not the mass constraint algebra.

## 6. Executed checks, provenance and open calculation

Run run_001 completed in 0.415 seconds: 19 exact symbolic checks and 2 numerical checks pass. The exact checks cover mass conversion, proton constraint, operator retuning, the induced coefficient, counterterm tangent, exact subtraction, trace normalization and sphere projection bookkeeping. An independent Ewald evaluation gives

    c1=-2.837297479480619476665917104607738836...

The second finite sum uses [-4,4]^3 at 60 decimal precision. Its analytic omitted-sum bound is 1.41e-35; floating roundoff is not interval-certified. This approximation is unnecessary for the exact cancellation. RAW_DERIVATION.md gives the Ewald derivation and explicit bound.

Python 3.9.6, SymPy 1.14.0 and mpmath 1.3.0 were observed. Reproduce with a fresh run directory:

    python3 fine_structure_puzzle/qcd_physical_matching/matching_path/run_audit.py --run run_002

The driver enforces a 30-second wall timeout and 20-second CPU limit without Git or network commands. run_001/manifest.json records before/after input hashes, output hashes, versions and limits, and validates with the computation-audit validator. Exact Git state was not inspected; the required dirty flag is conservatively true and labeled as such. Outcome: **implementation and finite assertion verified in the stated domain**; no QCD matrix element was evaluated.

INPUTS.json pins the eight supplied input files. SOURCES.json pins exact primary versions, PDF/text hashes and locators. The new finite-volume PDF SHA-256 is 607f469de91fdcad22939f02f03f0ec58a1b2642d1fb76baf5aac98788dfd67f. Full PDFs remain only in temporary storage. The original network attempt had a DNS failure; the public source was subsequently fetched and authenticated. No source cache or prior lane was changed.

The next decisive quantity is a same-theory geometry-subtracted vacuum expectation of (1), with proton Feynman-Hellmann and quark matching data in the same convention. It could detect an intrinsic term after the calibration contribution is removed. The present result closes the induced-flat-baseline loophole and keeps that physical route open.
