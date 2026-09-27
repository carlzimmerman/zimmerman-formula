# CA4-GNC-PQ: projected quadratic repair of the vacuum de Sitter scalar

This is an explicitly different action from both `FINAL_ACTION.md` and
`PERSPECTIVE_VARIANT.md`. Preserve their definitions and their failure
controls. To the full CA4-GNC-P action add, **outside** the carrier `Wd/t`,

\[
 \boxed{S_Q=-\int d^4x\sqrt{-g}\,V_0\zeta z^2,\qquad
 z=Z-\langle Z\rangle_h=t-1,\quad
 \zeta=4/\ell-1.} \tag{Q1}
\]

Keep bare `Lambda=0`, `V0>0`, the same five-field potential, C4 ramp,
geometric heat operator, fixed compensator and h-volume means. The new
all-mode de Sitter result below uses `0<alpha<=1`, `0<ell<=1`, `c2>0`
and `3H^2 xi^2 ell/4<=1/10`, with `H^2=V0/(3M_P^2)`. Thus `zeta>=3`.
The choice tying `zeta` to `ell` cancels a specific infrared coefficient;
it is an explicit constitutive choice, not a unique action derived from
symmetry or an observational determination. No new dimensional scale is
introduced. Sending `ell` to zero while holding arbitrary inhomogeneous
`z` fixed is singular and is not included in the parameter domain.

## Exact first variations and covariance

Write `A_Q=V0 zeta`. The local source and lapse density are

\[
 \sigma_Q=\partial_z{\cal L}_Q=-2A_Qz,\qquad
 \rho_Q=A_Qz^2. \tag{Q2}
\]

The full projected Z equation therefore becomes

\[
 2M_P^2c_N\operatorname{div}_N(DZ-a+DU)
 +\sigma_{PQ}-\langle N\sigma_{PQ}\rangle_h/N=0,
 \quad\sigma_{PQ}=\rho_{d,P}/t-2A_Qz. \tag{Q3}
\]

Its source has exactly zero `N dvol_h` integral. The exact lapse constraint
uses `rho_b+rho_d,P+A_Q z^2`. The U and heat equations are unchanged.
The carrier equations, carrier current exchange and carrier canonical
momenta are unchanged because (Q1) contains no carrier field. The
gravitational canonical momentum and shift constraint also receive no new
term in unitary gauge: (Q1) contains no physical time derivatives or shift.
This observation does not replace the complete Dirac analysis.

At fixed clock the extra physical spatial stress is

\[
 T_Q^{ij}=\left[-A_Qz^2+
      \frac{2A_Q\langle Nz\rangle_h}{N}z\right]h^{ij}. \tag{Q4}
\]

The first contribution is the local potential stress. The second is the
metric variation of the mean, since
`delta_h <Z>_h=(1/2)<z h^{ij}delta h_ij>_h`.
It must not be omitted even though it starts at higher order about the
homogeneous unit-lapse vacuum. In covariant normal/spatial decomposition,
the same contribution is
`T_Q^{mu nu}=-A_Q z^2 g^{mu nu}+2A_Q<Nz>_h z h^{mu nu}/N`;
its normal-frame energy density is (Q2), and its normal/spatial momentum
vanishes at fixed clock. This stress is not separately conserved off the
Z and clock equations.

For the clock variation at fixed `g,Z`, define `B_Z=n(Z)+Kz`. The exact
mean contribution is

\[
 E_{\tau,Q}=\langle N\sigma_Q\rangle_h B_Z
       -\sigma_Q\langle NB_Z\rangle_h
 =-2A_Q[\langle Nz\rangle_h B_Z-z\langle NB_Z\rangle_h]. \tag{Q5}
\]

It follows from the same geometric leaf deformation as the existing
projector, not from freezing the leaf. At fixed flat geometry the added
energy has derivative `partial_time rho_Q=-zdot sigma_Q`; combining with
the carrier energy gives the source `-zdot sigma_PQ`, which is exchanged
with the common host. No independent energy supply is inserted.

The leaf integral defines a scalar mean on the clock level set. Therefore
`z` and the added spacetime density transform covariantly under spacetime
diffeomorphisms, and the exact redundancy `Z->Z+c(tau)` survives. This is
covariance of a foliation-dependent, spatially nonlocal action, not local
Lorentz invariance of the carrier relative to ordinary matter. It requires
the same timelike global clock and compact leaves as the parent action.

## Background and canonical effects

At `z=0`, (Q1) and **every first variation** vanish. The homogeneous
carrier equations, vacuum density `V0`, pressure `-V0`, and
`H^2=V0/(3M_P^2)` are unchanged. The extra term contributes no quadratic
pure-tensor action on this homogeneous background.

For vacuum perturbations the source susceptibilities are now

\[
 \delta\rho_{PQ}=-V_0 z,\qquad
 \delta\sigma_{PQ}=-2V_0(1+\zeta)z. \tag{Q6}
\]

The nonzero-mode projected source also retains `+V0 delta ln N` about the
unit-lapse state. Hence this repair changes the linear auxiliary response;
it does not restore the original finite-amplitude density-subtraction law
or leave the previous floor susceptibility unchanged.

At fixed canonical data the Z-dependent Hamiltonian becomes

\[
 H_{Z,PQ}=\int N\,d\mathrm{vol}_h
  [M_P^2c_N|Dt-(a-DU)|^2+\epsilon_0/t+A_Q(t-1)^2]. \tag{Q7}
\]

Its simultaneous momentum/t second variation adds
`2A_Q (delta t)^2` to the nonnegative perspective Hessian (P7). Thus the
fixed-coordinate canonical joint convexity is preserved and strengthened.
The positive reciprocal floor remains essential at `t=0`; the finite
quadratic term alone is not a boundary barrier. Root records the extension
of the fixed-smooth-data barrier proof separately. This report proves no
coupled global-in-time continuation from (Q7).

## Independent de Sitter quadratic reduction

The evolution lane's on-shell ADM expansion for the actual inactive
vacuum de Sitter background includes the second variation of the h-volume
projector. Let `x=q^2=(k/a)^2>0`,

\[
 K_s=2(2+3c_2)/c_2>0,\quad r_0=\ell/4,\quad
 S=e^{-\xi^2x/2},\quad r=r_0S,\quad
 \alpha_e=2-(2-\alpha)(1-r)^2.
\]

The unaltered U constraint gives `z_1=r Phi`. In units `M_P^2/2`, (Q1)
adds precisely `-6H^2 zeta r^2 Phi^2` to the quadratic Lagrangian. Hence
the old coefficient `D_P=alpha_e x+6H^2r(1-r)` becomes

\[
 \boxed{D=\alpha_e x+6H^2r_0S(1-S).} \tag{Q8}
\]

The scalar action after the shift and U equations is

\[
 L_2=K_s(\dot\psi+H\Phi)^2+2x\psi^2-4x\Phi\psi+D\Phi^2.
\]

Eliminating the lapse with `E=K_s H^2+D` gives coefficients

\[
 A=K_sD/E,\qquad B=4K_sHx/E,\qquad C=2x-4x^2/E
\]

in `a^3[A psidot^2+B psi psidot+C psi^2]`. Integrating the cross term
in time is essential. Since `xdot=-2Hx`, its final coefficient is

\[
 C_I=\frac{2xD}{E}-\frac{4x^2}{E}
                  -\frac{4K_sH^2x^2D_x}{E^2}. \tag{Q9}
\]

These identities are independently checked here by exact differentiation
and quadratic substitution. They rely on the evolution lane's explicitly
expanded de Sitter ADM starting action; they are not imported from a flat
frozen host result.

For an analytic all-nonzero-mode sign bound put

\[
 u=\xi^2x/2>0,\quad\eta=3H^2\xi^2r_0,\quad
 g(u)=\frac{e^{-u}(1-e^{-u})}{u},\quad
 d(u)=D/x=\alpha_e+\eta g(u).
\]

Then `0<g<=1`, `0<d<=23/16+1/10=123/80<2` under the stated window.
Moreover

\[
 2u\alpha_{e,u}=-4(2-\alpha)u r(1-r)\ge-4r_0,
\]
\[
 2u\eta g_u=2\eta[-S+2S^2-g]\ge-4\eta,
 \quad d+2+2u d_u\ge2-4r_0-4\eta\ge3/5.
\]

The first bound uses `u exp(-u)<=1/2`, which follows for instance from
`exp(u)>=1+u+u^2/2>2u`. The second uses `S,g<=1`. Equation (Q9) factors
exactly as

\[
 \boxed{C_I=-\frac{2x^2}{E^2}
 [K_sH^2(d+2+2u d_u)+x d(2-d)]<0.} \tag{Q10}
\]

Also `D>0`, so `A>0`. Thus on this **actual homogeneous vacuum de Sitter
background**, every finite nonzero scalar mode has positive reduced
kinetic energy and restoring spatial stiffness within the displayed
parameter window. This repairs the old perspective candidate's negative
infrared stiffness without claiming that the old failure implied
unbounded future growth.

As `q->0`, `A` still vanishes proportionally to `q^2`. No uniform
zero-mode kinetic coercivity or homogeneous degree count follows. The
inhomogeneous gate, excited carrier backgrounds, full constraint system,
nonlinear evolution, and old empirical targets remain separate obligations.
The new source/stress and quadratic identities are recorded in
`pq_run1/`; the all-mode inequalities above are analytic, not a sampled
numerical campaign or a full PDE theorem.
