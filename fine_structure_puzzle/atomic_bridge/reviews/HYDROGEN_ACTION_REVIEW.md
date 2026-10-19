# Independent derivation from the frozen stiff-medium action

Coordinator derivation from `campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md`, S2, before reading the hydrogen agent's final report. This is an independent action/normalization check within the team. Its physical application to a microscopic quantum atom remains conditional.

Use the frozen action density

`L=-|grad Phi-K P|^2/(2K)-rho Phi-W_rem(u)-(gamma/2)|grad P|^2`,

with `K=4 pi G`, `u_vec=K P`, `u=|u_vec|`, `gamma/K=L_*^2/2`, and `K W_rem'(u)=u^2/(a_M-u)`. The physical acceleration points inward, while `g_vec=grad Phi` points outward for a positive central mass.

Variation of Phi gives `div(g_vec-u_vec)=4 pi G rho`. Variation of P gives

`g_vec=u_vec+[u^2/(a_M-u)] u_hat-(L_*^2/2) Delta u_vec`.

On the spherical regular-source branch, the Gauss relation gives `g_vec-u_vec=g_N_vec`, hence

`g_N_vec=[u^2/(a_M-u)]u_hat-(L_*^2/2) Delta u_vec`.

For u<<a_M in the gradient-dominated short-distance limit, the leading equation is `-(L_*^2/2) Delta u_vec=g_N_vec`. Since the vector Laplacian of `f(r) r_hat` is `(f''+2f'/r-2f/r^2) r_hat`, a point source has the local particular solution `u_vec=(GM/L_*^2) r_hat`. It adds a constant attractive acceleration; the corresponding potential is `delta Phi=+GM r/L_*^2`, up to an additive constant and matched homogeneous terms.

The reciprocal kernel independently confirms the coefficient. In longitudinal Fourier components, `u_vec=2 g_N_vec/(L_*^2 k^2)`. The additional potential kernel is `-8 pi G/(L_*^2 k^4)` with the usual Newtonian transform `-4 pi G/k^2`. Using `FT^-1[1/k^4]=-r/(8 pi)` modulo infrared homogeneous/constant ambiguities yields `delta V_12=+G m_1 m_2 r/L_*^2`. The factor 1/2 in total source-field energy removes double counting; the two cross terms leave this pair energy, not half of it.

For reduced-mass Coulomb hydrogen, `<r>_1s=3a_H/2` and `<r>_2s=6a_H`. First-order perturbation theory consequently gives

`delta nu_(1s->2s)=(9/2) G m_e m_p a_H/(h L_*^2)`.

Its sign is positive for the chosen local linear potential. The leading coefficient contains **no a_M**. The dark-energy-related acceleration scale enters the neglected nonlinear response and the large-distance matching, not this leading short-distance particular solution. This is a useful mechanism distinction; replacing the stiff action with the unstiffened deep-MOND force at a proton would be a different theory.

For a small uniform spherical source of radius R and mass M, the angularly averaged distance kernel outside the nucleus gives `delta Phi=(GM/L_*^2)[r+R^2/(5r)]`. Its leading transition correction relative to the point-source result is `-R^2/(30 a_H^2)`. When an rms radius is used, R^2=5 r_rms^2/3, giving `-r_rms^2/(18 a_H^2)`. Interior integrals and any physical mass/charge-radius identification are separate checks of the hydrogen implementation.

There are real application gaps. The macroscopic S2 action does not supply a quantized proton/electron source operator, a microscopic validity scale, the quantum material state or a complete short-distance matching condition. Homogeneous terms are not fixed by the local differential equation alone. The Fourier kernel is the regular, translationally invariant reciprocal local continuation; any global boundary contribution must be computed rather than asserted zero. A source-independent constant cancels from transition frequencies; nonconstant homogeneous/environmental pieces do not automatically cancel. These restrictions are required before calling a tiny number a prediction of the frozen framework.

Verdict on the central local mathematical implication: **proved under the stated linear-response, reciprocal-kernel and boundary interpretation**. Verdict on a literal physical atom prediction from S2 alone: **conditional on microscopic source/state and matching inputs**. The independent finite checks and actual boundary/nucleus treatment are in the hydrogen route; this note does not authenticate them merely from the action variation.

## Subsequent bounded perturbation review

The coordinator subsequently checked the global isotropic screened model directly. With lambda^2=L_*^2/2, q=sqrt(A)/lambda, A>0, its pair correction is -G m_e m_p(1-exp(-qr))/(A r). Subtracting its origin constant gives W=C[1-(1-exp(-qr))/(qr)], with C=G m_e m_p q/A. Hence 0<=W<=C and the coefficient of r is Cq/2=G m_e m_p/L_*^2, agreeing with the local action calculation.

In a fixed-angular-momentum radial sector, the isolated 1s and 2s gaps are respectively 3 E_h/8 and 5 E_h/72. The radial perturbation preserves these sectors, so the 2s/2p Coulomb degeneracy does not invalidate this use of the gap. For C<Delta/2, the shifted projected resolvent has norm at most 1/(Delta-2C); its Schur-complement contribution beyond first order is bounded by C^2/(Delta-2C). Summing the two level bounds and dividing by h bounds the transition remainder. This independently establishes the displayed norm estimate; it is not a bound on an arbitrary anisotropic nonlinear medium or on the A=0 global limit.

For the linear local perturbation in dimensionless Coulomb units, the normalized first-order 1s correction f(x)=(3-x^2)/2 gives d< x >/d epsilon=-3, hence relative mean-radius shift -2 epsilon. The coordinator derived this susceptibility rather than subtracting physically unresolved energies. The uniform-ball exterior correction above agrees with the exact convolution. Numerical values and the full finite interior implementation remain supported by the route's run003 and its declared finite checks, not by a claim of independently rerunning that script here.
