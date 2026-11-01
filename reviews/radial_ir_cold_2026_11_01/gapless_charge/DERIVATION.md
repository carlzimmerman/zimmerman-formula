# Residual gauge spectrum, radiative thresholds and anomalous phase charge

This is TP04 on the same canonical-K SU(5) action as TP01–03. It does not
replace that action by ordinary Standard Model matter. Put L=16pi²,
Delta=30h²+lambda² and mu=sqrt(f). The valley is

    A=i a D, B=b D, Tr D²=30, D=diag(2,2,2,−3,−3),
    a²=2fh/Delta, b=hX/lambda,
    W_A=0, W_X=f lambda²/Delta, W_B=(fh lambda/Delta)D,
    T=sqrt(Delta)X/lambda, V0=f²lambda²/Delta.

Here W_i denotes the superpotential derivative. The superspace auxiliary is
F_aux^i=−W_i*. This sign matters for a signed Majorana benchmark; physical
pole masses are nonnegative. At h=lambda=e, g=sqrt(29/200)e,
z=hX/sqrt(c), c=fe/31 and z0=7.367143721278508,
X0=mu z0/sqrt(31e), |T0|²=mu²z0²/e and F_eff²=V0=mu⁴/31.

## 1. Spectrum and the finite-splitting gaugino calculation

The unbroken gauge group is SU(3)×SU(2)×U(1), with GUT-normalized U(1).
The adjoint decomposes into (8,1)_0+(1,3)_0+(1,1)_0 plus
(3,2)_{−5/6}+conjugate. At tree level twelve gauge bosons and their gauginos
are massless. The flat complex scalar and chiral Goldstino are distinct.
The twelve eaten scalar zeros are gauge directions, not additional matter.

For the unbroken adjoints the chiral matrix is

    M_r=[[m,iq],[iq,0]], m=(1+r)hX, q=r lambda a,
    beta=(1+r)c, r=2 (multiplicity 8), r=−3 (multiplicity 3).

Its determinant depends only on A. Thus W_A=0 screens the leading small-F
holomorphic logdet gaugino mass. It does not screen the exact finite-splitting
answer: beta/q²=3/8 and−1/9. In the broken sector r=−1/2, the gauge mixing
L_g=5ga, R_g=5gb enlarges the rephased real Weyl block to

    [[m,q,L_g],[q,0,R_g],[L_g,R_g,0]],
    m_V²=25g²(a²+b²).

The implemented one-loop formula is the chirality-violating self-energy of
[Martin0509115v2](https://arxiv.org/pdf/hep-ph/0509115v2), Eqs.(3.2),(3.4),(3.6),
with delta_MS=0. In a nonnegative Takagi basis, projected onto raw unbroken
external legs u,v,

    Omega_uv = −1/L sum_I,k y_uIk y_vIk m_I B0(m_I²,m_k²)
               −1/L sum_I,a G_auI G_avI m_I
                    [3B0(m_I²,m_Va²)+xi B0(m_I²,xi m_Va²)],
    B0(x,y)=−integral_0^1 dt log[(tx+(1−t)y)/Q²].

All scalar/Weyl and massive-vector/Weyl terms are retained. At xi≠0 the
Goldstone masses are shifted consistently. The external mass is tree zero,
so wave-function multiplication changes this leading mass only at higher
loop order. Changing the normal vacuum fields at one loop likewise changes
this threshold at the next order: unbroken gauginos have no tree mass anywhere
on the aligned a,b slice. At z0 this is a leading vacuum pole threshold; at
1.21z0 it is only an off-shell background self-energy, not a rotating-state
quasiparticle spectrum.

The complete finite result at z0 is

    (m_3,m_2,m_1)/mu = e^(5/2)
       ×(4.6325552731e−5,6.7076021633e−5,1.1164161506e−4).

At e=.01 this is (4.63255527e−10,6.70760216e−10,1.11641615e−9);
at e=.03 it is (7.22143899e−9,1.04561170e−8,1.74032055e−8).
The multiplicities are8,3,1. Both scalar and vector classes matter: at e=.01
the U(1) contributions are −5.02920603e−10 and+1.61933675e−9.
The residual U(1) photino is gauge neutral and is therefore a separate
possible cold fermion candidate. Its stability requires the Goldstino decay
calculation, not a claim of exact R-charge conservation.

The ordinary messenger control uses auxiliary F_aux=−W_X* and agrees with
the exact finite-F function in [Giudice–Rattazzi9801271v2](https://arxiv.org/pdf/hep-ph/9801271v2),
Eqs.(2.19),(2.20). The initially positive expected signed mass in run_002
was inconsistent with this auxiliary convention; its magnitude was already
correct. The changed expectation is explicit in the code, not a fit to the
SU(5) answer. run_001 failed JSON serialization before writing a result.
Both failures are preserved. run_003 passes 22 controls: finite messenger,
subgroup degeneracy, Q and xi independence, SUSY limit and scaling. The
largest Q/xi discrepancy is 3.44e−11 relative; observed RSS 93.7MB.

The additional run_null_001 includes the chiral Goldstino in the entire
thirteen-dimensional tree-null external space. At e=.01,.03 the mixed
gaugino/Goldstino entries are below 3.1e−14 relative to the photino mass.
The Goldstino diagonal is5.5e−21 and −4.8e−20 in mu units, consistent with
the leading loop-stationary z0. Thus neutral degeneracy does not replace the
reported leading photino pole by an untested two-state eigenvalue.

The full finite-CW radial mass instead scales as mu e^(3/2)/sqrt(L).
Consequently m_lambda/m_rad scales as e/sqrt(L), with a shape-dependent
coefficient. Weakening e makes the radiative gauginos lighter relative to
the radial mode. An earlier progress message used the old leading-log radial
power e^(5/2); that comparison was corrected before interpreting these runs.

## 2. Gauge threshold matching and far infrared scales

Use beta(g)=b g³/L. Above all thresholds b_SU5=−5. Below massive matter but
above the radiative gaugino, b_r=−3 C_r, with C=(3,2,0). Below m_lambda it
is b_r=−11 C_r/3 for the two nonabelian pure-gauge factors. The U(1) has no
charged light particle and no perturbative self-running. Its photon remains
massless; a neutral photino does not generate a U(1) beta function.

The broken real representation has T_X=(2,3,5). Its physical vector carries
b_V=−7T_X/2, including the eaten mode. Each physical real scalar contributes
T/6 and each Weyl fermion2T/3. The actual mass-basis traces, including finite
SUSY splittings, give total heavy b=(4,1,−5). Goldstones are excluded from
the physical scalar threshold and are counted in b_V. This is essential.

At the TP03 fixed Q0²=mu²e(1+z0²)/31,

    1/g_r,low²(Q0)=1/g_SU5²(Q0)
                  +sum_heavy b_j log(Q0/m_j)/(8pi²),
    Delta(1/g²)=(.1239022517,.1034183304,.1249548291).

The MS physical-vector constant cancels in DR: the MS threshold has
−T_X/(48pi²), while 1/g_MS²=1/g_DR²+C(G)/(48pi²) above and below adds
+T_X/(48pi²). See the physical-scalar matching convention in
[Ellis–Wells, PRD91,075016](https://link.aps.org/accepted/10.1103/PhysRevD.91.075016),
Eqs.(2),(3), and the conversion in [Martin–Vaughn9308222v2](https://arxiv.org/pdf/hep-ph/9308222),
Eq.(2.4). No supersymmetric common-mass approximation is made here.

Define i_r=1/g_r,low²(Q0). To the computed logarithmic order,

    i_r(m_lambda)=i_r+3C_r log(m_lambda/Q0)/(8pi²),
    log(Lambda_YM/mu)=log(m_lambda/mu)
                         −8pi² i_r(m_lambda)/[(11/3)C_r].

The formal log10(Lambda_YM/mu) values for SU3,SU2 are

| e | SU3 | SU2 |
|---|---:|---:|
| .01 | −214990.37 | −322484.23 |
| .03 | −23889.89 | −35833.72 |
| .0001 | −2.1498757e9 | −3.2248136e9 |

These huge exponents establish a perturbative hierarchy. They are not
precision predictions for confinement gaps or a proof of a universal gap.
Two-loop running and finite higher-order matching change logarithmic/prefactor
terms; the one-loop definition of Lambda is scheme dependent. In particular,
m_lambda is vastly above the putative strong scale, so treating the far IR
as exactly supersymmetric massless-gaugino Yang–Mills is inappropriate. A
supersymmetric condensate formula cannot be substituted unchanged. Pure-YM
susceptibility remains a nonperturbative input. Lattice results such as
[Cè et al.1607.05939](https://arxiv.org/pdf/1607.05939) support a nonzero
susceptibility in their pure-YM theories; no lattice coefficient is borrowed
to certify this model's dynamics.

## 3. R anomaly and the actual zero-temperature charge channel

Assign original scalar R charges R(X)=R(B)=2, R(A)=0. The Weyl charges are
q_R=(+1,−1_adj,+1_adj,+1_gaugino). For each embedded subgroup the full trace
Tr(q_R T_r²)=5. With

    q_top,r=g_r² F_r^a Ftilde_r^a/(32pi²),
    partial_mu j_R^mu=10 q_top,r,
    theta→theta+2alpha, j_theta=j_R/2,

the theta-charge anomaly is5 q_top,r. Light nonabelian gauginos carry C_r
units in this last normalization. Integrating out the charged heavy states
therefore leaves

    L_WZ=−sum_r K_r theta q_top,r, K=(2,3,5),

up to the overall theta/sign convention. The coefficient also follows from
the heavy R-anomaly matching of [Intriligator–Sudano1001.5443v2](https://arxiv.org/pdf/1001.5443v2),
Eq.(2.49). A rephasing of a light gaugino moves terms between its derivative
current, its theta-dependent Majorana mass and the local WZ term; it cannot
remove the anomaly. Below a nonabelian gaugino mass its phase contributes
the remaining C_r, giving total coefficient 5. At frequencies above that mass
one must keep its nonlocal triangle/current response. **For U(1), C_1=0:
the photino is neutral and K_1=5 is unambiguous throughout the heavy-gap EFT.**

A homogeneous rolling theta=omega t in an initially empty, locally flat,
infinite U(1) vacuum gives

    A_ddot,±+[k²±k kappa_1 omega]A_±=0,
    kappa_1=5g_1²/(8pi²),
    0<k<|kappa_1 omega|,
    k_fast=|kappa_1 omega|/2,
    gamma_max=|kappa_1 omega|/2=5g_1²|omega|/L.

This is a perturbative zero-temperature helicity instability, with no
instanton or thermal activation factor. The Maxwell derivation is the same
local helicity equation as [Anber–Sorbo0606534v2](https://arxiv.org/pdf/astro-ph/0606534),
Eqs.(7),(15)–(18); no inflationary solution or assumption is imported.
Using the matched U(1) coupling, gamma_max/|omega| is4.59110782e−7,
4.13193714e−6 and4.59111613e−11 for e=.01,.03,.0001. Thus an infinite
constant rolling vacuum cannot simply be declared stable from tiny
nonabelian instantons.

With suitable closed boundary conditions the perturbative Abelian equations
can conserve a combination of the phase charge and magnetic helicity. The
statement above concerns transfer out of the rotating matter carrier; it
does not assert that every improved phase-plus-gauge quantity decays. Helical
gauge radiation and a coherent matter rotation have different stresses.

For a finite patch, growth requires an allowed mode k_min<|kappa_1 omega|;
the best possible rate is reduced if k_fast is unavailable. With constant
conductivity sigma the optimal amplitude growth is

    gamma_sigma=[sqrt(sigma²+kappa_1²omega²)−sigma]/2,

not the vacuum value. Expansion changes physical k and the available time;
the flat constant-coefficient estimate requires its variation to be slow.
If an admitted growing band initially has energy rho_seed, its linear
backreaction timescale is approximately

    t_backreaction≈log(rho_rotation/rho_seed)/(2gamma),
    rho_rotation≈F omega², F≈|T|².

The logarithm and finite-band prefactor depend on the state and the switch-on
history. This is an onset estimate, not a calculated fractional charge
lifetime or nonlinear endpoint. Even without absolute mu, the quantities
gamma/omega, k_fast/omega and omega t_backreaction are meaningful conditional
outputs. An uncharged radial oscillation has omega=0 and does not source
this constant-rolling helicity channel.

## 4. Nonperturbative potential, thermal drift and locality

Well below the nonabelian gauginos, write the unknown pure-YM vacuum energies
E_r(theta_r+5theta). The susceptibility is chi_r=E_r''(0), so

    m_theta²=25(chi_3+chi_2)/(2F).

If chi_r=C_chi,r Lambda_r⁴, this produces an exponentially small phase
potential at the trial weak couplings, conditional on finite C_chi,r. The
unknown coefficient and the strong dynamics are not computed here. At scales
near or above the gap, replacing the gauge system by this local potential
is unjustified. A constant theta in the perturbative noncompact U(1) theory
does not acquire an instanton potential; monopole effects or compact-space
sectors would require their own specified state and matching.

At zero temperature one must not insert a high-temperature sphaleron rate.
In a specified pure-YM bath Lambda≪T_bath≪m_lambda, weak alpha(T_bath), small
chemical bias5|omega|≪T_bath and coherent susceptibility chi_Q=2F, define
Gamma_CS=lim Var(Delta N_CS)/(Vt). Detailed balance then gives

    gamma_Q=25 Gamma_CS/(2T_bath chi_Q)
           =25 kappa_CS alpha^5 T_bath³ log(1/alpha)/(4F).

Here kappa_CS is an unknown group-dependent diffusion coefficient. The
thermal scaling and its plasma assumptions are those of
[Arnold–Son–Yaffe9810216v1](https://arxiv.org/pdf/hep-ph/9810216), Eqs.(1.1),(1.2).
For tau=T_bath/mu, gamma_Q/mu is this expression with
F/mu²=z0²/e. At a reference alpha evaluated at m_lambda, its coefficient
per kappa_CS tau³ is about3.22e−32 (e=.01),4.79e−27 (.03),5.39e−54 (.0001).
Alpha must be run to the actual bath temperature before using the formula.
Above m_lambda additional gaugino chemical susceptibilities and exchange
rates require coupled kinetic equations. The U(1) helicity channel is not a
nonabelian sphaleron rate and is analyzed separately above.

Finally, the local two-derivative radial/current coefficients from TP03 can
coexist with massless sectors. Purely massless-pair vertices vanish in those
specific one-loop coefficients; this does not make the full effective action
local. Gauge/Goldstino cuts, anomalous gauge response and light radiative
gaugino thresholds require their fields or nonlocal kernels whenever the
frequency reaches them. The radiative gauginos are far below the heavy tree
gap, so that gap is not the cutoff for a scalar-only time-dependent EFT.
