# Independent derivation: constrained insertion and finite-volume matching

FSP-006, parent FSP-005. Work confined to this lane. This derivation was developed from the supplied definitions and then checked against the primary finite-volume formula. It evaluates matching algebra and a geometry constant, not a QCD vacuum matrix element.

## 1. Define the family before differentiating

Use natural units, canonical Thomson charge, and alpha=e^2/(4 pi). Write the renormalized material theory in coordinates

    (alpha, ell=ln Lambda, h_i=ln mhat_i),

where the hats denote a declared full QCD+QED invariant-mass convention. They are scheme-dependent input coordinates, not free-quark pole masses. Fix theta and all other dimensionless inputs. For this derivation the material theory contains quarks, gluons and photons; extra massive species would require extra held mass coordinates and corresponding insertions. The same regulator, finite matching conditions and source operator normalization are used on both geometries.

Keep the local gravitational action separate:

    S_grav = integral sqrt(g) [v + b_R R + b_1 R^2 + b_2 R_ab R^ab + ...].

The renormalized cosmological coefficient v is independent of the proton and quark masses. A matter vacuum subtraction convention and v together define the total vacuum energy. A reshuffling of a local identity term between them cannot change a fixed total theory. Changing v independently changes that gravitational theory.

Let M=m_p^infinity(alpha,ell,h) be the infinite-volume rest threshold in one charged-state infrared prescription. Assume a differentiable branch with M_ell != 0. The physical calibration used here imposes M=M_* and dh_i=0. At fixed metric,

    ell_alpha = -M_alpha/M_ell.

This is not yet an insertion formula. In particular, holding h_i fixed generally changes the running masses and the renormalized couplings at a fixed reference scale.

## 2. Retuning as an action insertion

Let y^A be any chosen renormalized or bare coordinates at fixed regulator and renormalization scale, including g_s and each running quark mass. Define renormalized composite insertions by differentiating the regulated matched action, including its counterterms:

    O_A = partial S_mat/partial y^A,
    I_alpha = partial S_mat/partial alpha |_y.

If y=y(alpha,ell,h), the two matched insertions are

    I_hat_alpha = I_alpha + sum_A y^A_alpha O_A,
    O_ell = sum_A y^A_ell O_A.

The constrained material insertion is therefore

    K_alpha,g = I_hat_alpha,g - (M_alpha/M_ell) O_ell,g.       (1)

The coefficient is determined by the flat proton constraint and then used in the vacuum geometry. It must not be fitted independently in the vacuum sector. The complete insertion additionally contains v_alpha V_g and the prescribed curvature-counterterm tangents. If v is a held independent coordinate, v_alpha=0. A condition such as zero total flat vacuum energy supplies a different v_alpha; the proton constraint supplies none.

For example, at a fixed reference scale let z_i=ln m_i(mu)=h_i+u_i(alpha,ell). Then

    dz_i/dalpha = u_i,alpha - u_i,ell M_alpha/M_ell.

These coefficients multiply the scalar insertions integral m_i qbar_i q_i. There is also the strong-coupling insertion with coefficient dg_s/dalpha, and charge-matching terms if the action charge is not alpha(0). Thus setting the scalar coefficients to zero merely because the invariant masses are held would be wrong. The exact two-flavour conversion algebra is checked in check_matching.py; the sum over A gives the arbitrary-flavour result without diagonal-mixing assumptions.

At alpha=0, integrate the canonically normalized Gaussian photon with Euclidean coupling i e A.j. The sign follows by completing the Gaussian square:

    S_eff = S_QCD + e^2 I_g + O(e^4),
    I_g = (1/2) integral_(x,y) j_mu(x) D_g^(mu nu)(x,y) j_nu(y) + I_g^ct,
    I_hat_alpha,g = 4 pi I_hat_g.

Metric measures and all sea, disconnected and valence contractions are included. The current product mixes into identity, quark-mass and gluonic operators. Those counterterms implement the declared matching conditions; they cannot be omitted as harmless contacts. This structure is checked directly in de Divitiis et al., arXiv:1303.4896v1, section 2, equations (2)-(7). The Gaussian normalization and any photon determinant also belong to the vacuum functional, even when independent of alpha at this order.

For any insertion X define the proton functional

    H_p[X] = lim_(T->infinity) [<N(T) Nbar(0) X>/<N(T) Nbar(0)> - <X>]/T,

including matched endpoint/contact effects and one fixed charged-state prescription. Then H_p[I_hat_alpha]=M_alpha, H_p[O_ell]=M_ell, and H_p[K_alpha]=0.

For a general path with action derivative X, the Euclidean sign follows from dln C/dalpha=-[<N Nbar X>/<N Nbar>-<X>] for a normalized path integral and ln C=-MT+O(1). Thus dM/dalpha=+H_p[X] along that path, with endpoint derivatives included in the O(1) overlap or explicitly matched when required. In particular X=K gives the constrained derivative zero. For W_g=-ln Z_g the vacuum identity is

    dW_g/dalpha |_M,h = <K_alpha,g> + v_alpha V_g + curvature terms.       (2)

Identity terms vanish from H_p but contribute to (2). A proton calculation alone therefore cannot fix the vacuum identity term. This is a genuine additional observable/renormalization condition, not just an unfamiliar notation for the same proton derivative.

## 3. RG trace realization and its scope

At alpha=0, beta_s=mu dg_s/dmu and gamma_i=-mu dln m_i/dmu. The pure-QCD trace identity in the canonical gauge-field normalization is

    Theta_QCD = beta_s/(2 g_s) [G^2]_R + sum_i (1+gamma_i)[m_i qbar_i q_i]_R.

Metz, Pasquini and Rodini, arXiv:2006.11171v2, equations (12), (23), (26), fixes this convention and <p|Theta|p>=2M^2 in relativistic normalization. Its separate quark/gluon pieces are scheme dependent.

At fixed mu and invariant masses,

    dg_s/dell = -beta_s,       dln m_i(mu)/dell = gamma_i.

One way to check the gauge sign is to use the rescaled gauge field with S_g=integral mathcalG^2/(4g_s^2). Then -beta_s partial_g S_g gives beta_s mathcalG^2/(2g_s^3), equal to beta_s G^2/(2g_s) after returning to the canonical field. Consequently, modulo equation-of-motion/contact operators fixed by the derivative definition,

    O_ell = integral sqrt(g) [Theta_QCD - sum_i m_i qbar_i q_i]
            + c_ell V_g + curvature contacts
          = integral sqrt(g) [beta_s G^2/(2g_s) + sum_i gamma_i m_i qbar_i q_i]
            + c_ell V_g + curvature contacts.                 (3)

Here c_ell is an identity coefficient required if the chosen vacuum subtraction is not already included in Theta_QCD. It is not obtained from connected hadron matrix elements. Equation (3) is a statement about differentiated renormalized operators, not about their expectation values having been evaluated.

The proton denominator is fixed by Feynman-Hellmann and the trace normalization:

    sigma_i = mhat_i partial M/partial mhat_i,
    M_ell = M - sum_i sigma_i.                               (4)

In a homogeneous matter-vacuum convention, E_M=Lambda^4 B(x), x_i=mhat_i/Lambda, the vacuum counterpart is

    E_M,ell = 4E_M - sum_i mhat_i partial E_M/partial mhat_i
            = Lambda^4 [4B - sum_i x_i partial_i B].           (5)

The total E_0=E_M+v instead has E_0,ell=E_M,ell+v_ell along a chosen gravitational family. A finite subtraction can reshuffle (5) and v_ell. The total is fixed only when that family is specified.

At nonzero alpha, the full trace also contains beta_e F^2/(2e), mixed-coupling beta functions, full mass anomalous dimensions, and identity/curvature terms. The pure-QCD expression (3) alone is then incomplete. The safe all-alpha definition is (1), using the full parameter map. Equivalently, if (Lambda,mhat_i,alpha(0)) is a complete matched set of material coordinates, the simultaneous dimensional-scale Ward identity gives the integrated full trace as O_ell+sum_i O_hi, with O_hi=partial S_mat/partial h_i in that same convention. At nonzero alpha these O_hi need not be the naive MSbar scalar insertions: charge-threshold matching is part of keeping alpha(0) fixed. Additional fixed dimensionful species require corresponding O_hi terms. No mixed beta or threshold coefficient is silently set to zero here.

## 4. Apply to the actual sphere coefficient

This paragraph concerns smooth round S4 and does not import the torus mass formula below. For the parent's fixed-theory prescription,

    f_g=W_g/V_g,       rho_E=(1-D/4)f_g,       D=H partial_H,
    A_rho=lim_(H->0+) P(D)rho_E/(3H),       P(D)=D(D-2)(D-4).

The derivatives in D are metric derivatives at fixed microscopic comparison theory, including its gravitational couplings. If the alpha derivative, metric response and limit commute, (2) gives

    dA_rho/dalpha |_M,h
      = lim P(D)(1-D/4)[<K_alpha,g>/V_g]/(3H).               (6)

Local counterterm tangents are annihilated at fixed comparison data. Since M is held, d(A_rho/M^3)/dalpha=M^-3 dA_rho/dalpha. In logarithmic notation (6) reduces to the supplied constrained formula h_alpha-(3-Q)p_alpha/(1-P). That chain-rule identity is recovered, but (1)-(3) specify the operators that must actually be evaluated.

There is no Ward identity equating the vacuum functional of K to its connected proton functional. The latter is zero by construction; the former need not be zero. This identifies the new measurable subtraction/retuning problem while leaving the dynamical QCD numerator open.

## 5. Actual QED_L mass effect

The primary source is Davoudi and Savage, arXiv:1402.6741v2, section II and the leading terms of equation (19). The setting is infinite time times a cubic spatial torus of side L, periodic photons with every spatial zero mode removed at each time (QED_L), and a hadron at rest. For positive hadron masses and large L,

    M_L(theta)-M_infinity(theta)
      = alpha Q_p^2 c1/(2L) [1+2/(M_infinity L)]
        + O(alpha L^-3) + higher electromagnetic orders + strong exponential terms,
    c1 = -2.83729... .                                  (7)

Only its universal leading term is needed. Let k=Q_p^2 c1/2; for a proton Q_p=1, k is negative. No measured alpha, radius, magnetic moment or polarizability from the source is imported. Later corrections to higher-order fermion finite-volume terms are irrelevant to the retained 1/L term.

QED_L modifies the global zero-mode constraint so that an isolated charged state can exist. The infinite-time torus vacuum has an energy density and generally a separate spatial pressure; it is not an S4-invariant state. Its length L is not the de Sitter radius by definition.

## 6. Retune finite-volume proton mass, then compare the vacuum

Fix alpha and the declared h_i. Let theta_0 denote the theory with M_infinity(theta_0)=M_*, and choose ell_L so M_L(ell_L)=M_*. To first order,

    delta ell = ell_L-ell_0 = -alpha k/(L M_ell) + O(L^-2,alpha^2/L).     (8)

M_ell and the retained flat vacuum derivatives on the right can be evaluated at alpha=0 when working only to O(alpha). Define the intrinsic same-theory vacuum difference by

    F_L(theta) = E_L(theta)-E_0(theta),

where E_0 is the infinite-volume flat energy and includes the same v. Do not assume anything about F_L except sufficient smoothness in the parameter direction; it may or may not contain an intrinsic 1/L term.

There are three useful comparisons.

**One fixed reference theory.**

    Delta_ref(L)=E_L(theta_L)-E_0(theta_0)
      = F_L(theta_L) + [E_0(theta_L)-E_0(theta_0)].

The second bracket is present even when F_L has no 1/L term. Its leading coefficient is

    Delta_ref(L) contains A_art/L,
    A_art = -alpha Q_p^2 c1/2 * E_0,ell/M_ell.              (9)

If v is held as a dimensionful coordinate, and E_M=Lambda^4 B(x), M=Lambda C(x), this becomes

    A_art = -alpha Q_p^2 c1/2 * Lambda^3
              [4B-sum_i x_i partial_i B]/[C-sum_i x_i partial_i C].       (10)

Thus the requested alpha Lambda^3/L scaling does arise algebraically, with a known geometric factor -c1/2=1.4186487397403... multiplying an unevaluated, convention-dependent flat-vacuum derivative ratio. There is no universal sign for A_art because the vacuum derivative is not sign-fixed. Near M_ell=0 this expansion fails; that is not an enhancement that can be trusted.

**One theory at each L, subtracted against its own flat limit.**

    Delta_same(L)=E_L(theta_L)-E_0(theta_L)=F_L(theta_L).     (11)

The bracket producing (9) cancels exactly, to every order, before an asymptotic expansion. If F_L has no 1/L term uniformly in a smooth neighborhood and its parameter derivatives do not generate one, (11) does not create a 1/L term. If F_L already contains A_int(theta)/L, retuning changes A_int only at higher order through delta ell=O(1/L). This cancellation therefore removes the calibration contribution while preserving a possible genuine intrinsic coefficient.

**Correct the finite-volume mass before tuning.** Tuning M_L-alpha k/L=M_* makes ell_L-ell_0 start at O(L^-2) at the retained electromagnetic order, and therefore avoids (9) already at calibration. Taking the continuum and infinite-volume matching limit first gives the same leading conclusion.

At alpha=0 the operator form makes the contamination visible directly:

    partial_alpha M_L = partial_alpha M_infinity + k/L + ...,
    K_alpha,L = 4pi I_hat_L - [(M_alpha,infinity+k/L)/M_ell] O_ell,L + ... .

The additional vacuum term is -k <O_ell,L>/(L V M_ell). Subtracting a flat functional with the same ell_L derivative cancels its flat part. Subtracting a flat functional tuned independently with M_infinity does not. The sign and factor in (9) agree with this insertion-level derivation.

## 7. Cosmological counterterm and metric differentiation

If v is independently allowed to vary with ell across the family, replace E_0,ell in (9) by E_M,ell+v_ell. Imposing the extra renormalization condition E_0(theta)=0 throughout the family gives v(theta)=-E_M(theta), hence E_0,ell=0 and A_art=0. Keeping v fixed generally retains (9). Neither choice is selected by holding the proton and quark masses fixed. A pure subtraction-scheme change at fixed total theory shifts E_M and v together and leaves E_0,ell unchanged; one must not call a change of physical v merely a scheme change.

A local cosmological term v is independent of L at fixed theory and cannot imitate an intrinsic 1/L torus response or linear H sphere response. But its coefficient composed with ell(L), v(ell(L)), can acquire that dependence across theories. This is precisely why applying the sphere projector P(D) to an already retuned cross-theory curve is insufficient: P(D)H=3H retains the artificial linear term. Flat subtraction and the matching path must first be fixed.

Likewise, dW[g,theta(g)]/dg includes (partial_theta W) dtheta/dg. That total derivative is not the stress tensor delta W/delta g at fixed couplings. On R times T^3, vacuum energy follows a time-length variation; spatial variation defines pressure. The familiar 3/4 factor for f proportional to H on a round S4 belongs to its separate, fixed-coupling uniform metric variation. It cannot be attached to (9). No local generally covariant bulk counterterm proportional to H Lambda^3 is introduced here.

If one were to define a formal cross-theory sphere curve rho_S4(H;theta(H))-rho_flat(0;theta_0), an analogous baseline Taylor term would survive. Its coefficient would require the charged-state response in that sphere prescription. Equation (7) supplies no such coefficient: a closed S4 has different topology, zero modes, curvature and charged-state constraints.

For completeness, the baseline contribution to an **evaluated stress** and to a **total-path derivative** differ. Suppose solely for this bookkeeping test that ell(H)=ell_0+dH+o(H), f(H,ell)=E_0(ell)+f_intr(H,ell), and A_base=d E_0,ell. The actual sphere stress is evaluated at each point using the partial metric derivative:

    rho_true(H;ell(H))=[1-(H/4)partial_H|ell]f(H,ell)|ell=ell(H).

Its flat-baseline contribution is E_0(ell_0)+A_base H. If one instead differentiates the composed function with a total D, then

    rho_pseudo=(1-D_total/4)f(H,ell(H))
              =rho_true-(H/4)ell'(H)partial_ell f,

and the baseline coefficient becomes 3 A_base/4. That extra factor is an error in the stress definition. Equation (9) is the coefficient in the evaluated vacuum energy (and in the flat-baseline part of evaluated stress), not in this pseudo-stress. The legitimate fixed-parameter sphere stencil keeps ell independent of H; its alpha-dependent matching at the flat reference is a separate operation.

## 8. Independent shape constant calculation

Define the regulated cubic lattice constant by

    pi c1 = lim_(eta->0+) [sum_(n != 0) exp(-eta |n|^2)/|n|^2 - 2 pi^(3/2)/sqrt(eta)].

Poisson summation of the three-dimensional theta series gives the derivative of the bracket as

    1 - (pi/eta)^(3/2) sum_(m != 0) exp(-pi^2 |m|^2/eta).

Integrating this identity from 0 to eta and evaluating the elementary Gaussian tail gives

    c1 = (1/pi) sum_(n != 0) exp(-eta |n|^2)/|n|^2
         - 2 sqrt(pi)/sqrt(eta) - eta/pi
         + sum_(m != 0) erfc(pi |m|/sqrt(eta))/|m|.

At eta=pi both sums share the same integer lattice, producing the absolutely convergent formula implemented in check_matching.py:

    c1 = -3 + sum_(n != 0) [exp(-pi |n|^2)/(pi |n|^2)
                            + erfc(sqrt(pi)|n|)/|n|].

The summation includes every nonzero vector in [-N,N]^3. Since erfc(x)<=exp(-x^2)/(sqrt(pi)x), both summands together are at most 2 exp(-pi |n|^2)/(pi |n|^2). A union bound over three coordinates outside the cube, followed by a geometric bound on the Gaussian tail, gives, with a=N+1,

    omitted absolute sum <= 12 theta_bound^2 exp(-pi a^2)
                             /[pi a^2 (1-exp(-pi(2a+1)))],
    theta_bound = 1+2 exp(-pi)/(1-exp(-3pi)).

The two runs internal to run_001 use (N,dps)=(3,40),(4,60); their difference is below the first tail bound plus the stated loose roundoff allowance. The second gives c1=-2.837297479480619476665917104607738836... with analytic truncation bound 1.41e-35. The arithmetic is arbitrary-precision floating point, not interval-certified; the exact symbolic cancellation is independent of this numerical approximation.

## 9. What this discriminates

The 1/L proton effect is an ordinary physical finite-volume self-energy in the specified QED_L regulator. It provides a concrete calibration contamination of the same dimensions as a proposed alpha Lambda^3/L vacuum term. It does not establish a new intrinsic vacuum response, and it does not explain de Sitter acceleration or alpha. If a physical mechanism actually made a strong coupling adjust with cosmological size, its dynamics and gravitational counterterm would need to be specified; a numerical tuning condition is not that mechanism.

The decisive next observable is the common-regulator, same-theory difference of the constrained insertion (1) between the target vacuum geometry and its flat reference, with independent proton Feynman-Hellmann and quark matching data. A surviving nonanalytic term after that subtraction would be independent physical evidence. The present exact cancellation settles this particular induced-baseline loophole and leaves the intrinsic QCD geometry problem open.
