# FSP-002/B: a shared scalar can stabilize a coupling without selecting its value

Parent: FSP-001; Git `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty baseline. New candidate dated 2026-10-18 America/New_York / 2026-10-19 UTC. Scope: this directory only. **No physical alpha(0) is derived.**

The strongest partial result is a concrete sign discriminator. A common inverse-gauge function can have a stable scalar vacuum because QCD generates a potential. In the specified negative-condensate model, QCD vacuum energy stabilizes a *minimum* of that function, whereas positive nonrelativistic matter stabilizes a *maximum*. Their common extremum sets the linear scalar couplings to zero; it does not set the value of the function. An exact counterfamily preserves nucleon mass, a hydrogenic size–mass product, the vacuum energy and the entire QCD-induced scalar profile while changing alpha, unless an additional physical matching scale is fixed. This is an exact statement inside the explicitly declared leading EFT truncation, not an all-orders no-go.

## 1. What is actually in the framework

The frozen [canonical theory](../../../campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md), S1–S3, supplies a cosmic dark-energy density, measured kappa, a static stiff polarization action and a required cold rest-mass medium. It does not supply photon normalization, electron Yukawa/Higgs dynamics, QCD gauge kinetics or a common scalar. [The October 15 instructions](../../../sol61_push/THEORY_NEXT_STEPS_2026-10-15.md), O0/O1/O6, explicitly require a joined reciprocal action and parameter origins. The older [carrier action](../../../sol61_push/radiative_trap_matching_2026_10_13/INPUT_CARRIER_ACTION.tex) has its own global charge, not identified with electric charge. Its symbol alpha denotes a quartic ratio, not the fine-structure constant.

The action below is therefore a **separately proposed scalar bridge**, not an amendment to the frozen theory. It does not derive the polarization action, tether, abundance or galaxy law. In particular, no microscopic extrapolation of the canonical static action is used to generate an electron charge.

## 2. Minimal explicit bridge and physical conventions

Use natural units, signature (-+++), reduced Planck mass M_P and a dimensionless scalar x whose locally canonical field is phi=f x. A metric-EFT scaffold is

\[
\begin{split}
S_B=\int\sqrt{-g}\,d^4z\,[&M_P^2 R/2-f^2(\partial x)^2/2-U(x)
 -Z_\gamma(x;\mu)F^2/4-Z_3(x;\mu)G_a^2/4\\
&+\bar e(i\!\not\!D-m_e(x;\mu))e
 +\sum_q\bar q(i\!\not\!D-m_q(x;\mu))q\\
&-(\partial X)^2/2-m_c(x)^2 X^2/2]+S_{\rm higher}.
\end{split} \tag{B1}
\]

Here X is only a minimal massive, electrically neutral cold-carrier stand-in. Its existence and identification with the programme's displacement medium remain open. For an explicit common-scalar example take m_c(x)=m_c0 exp[-p_c B(x)], with m_c0,p_c positive. All visible/cold fields exchange energy reciprocally with x through their displayed mass/kinetic functions. A time-dependent mass must not be evolved while omitting the scalar's energy. Einstein gravity in (B1) defines the trial metric/frame; it is not a claimed relativistic derivation of the canonical polarization sector.

Fix the electromagnetic generator with electron charge -1 and quark charges 2/3,-1/3. Equivalently, in a primitive integral electric lattice the electron has charge -3 and the kinetic coefficient is 9 Z_gamma. These are the same convention held fixed, never a scalar-dependent field rescaling. The gluonic connection includes its coupling and obeys Tr(T_a T_b)=delta_ab/2; hence Z_3=1/g_s^2 and the usual canonically normalized gluon field is different.

For the physical massless photon and on-shell electron pole mass,

\[
\alpha(0;x)={1\over4\pi Z_\gamma^{\rm IR}(0;x)},\qquad
Z_\gamma^{\rm IR}(0;x)=Z_\gamma(\mu;x)+\Delta_\gamma(\mu,0;x). \tag{B2}
\]

Delta_gamma contains running and finite thresholds, including charged masses, hadronic polarization and any heavy sector. Writing a UV function alone never completes (B2). Fermion kinetic coefficients have first been normalized; their rescalings and mass matching belong in m_e. Above electroweak breaking (B1)'s photon/electron mass terms must be replaced by SU(2)xU(1), Higgs and Yukawa terms and matched back; this report does not bypass that obligation.

At leading one-loop QCD order, with fixed active flavour content and fixed light-quark ratios,

\[
\Lambda_3=M_U\exp[-8\pi^2 Z_3(M_U;x)/b_0],\quad b_0=11-2n_f/3,
\qquad m_N=C_N\Lambda_3. \tag{B3}
\]

M_U below denotes a **physical matching threshold at which a common boundary condition is imposed**, not an arbitrary subtraction scale. C_N is a dimensionless strong-dynamics input; actual nucleons also depend on light-quark ratios and electromagnetism. Those corrections are held outside this chiral/leading model, not declared zero in nature. Changing M_U while holding an entire matched theory fixed is not a new physical model. The counterfamily below instead changes its physical common-boundary threshold and matching data.

The trace anomaly relates scalar response to mass. In canonical gluon variables, T^mu_mu = [beta_s/(2g_s)] G_c^2 + sum_q(1+gamma_q)m_q qbar q, plus electromagnetic terms. It gives, in the B3 limit, d ln m_N/dx=d ln Lambda_3/dx, not an equation fixing Z_3. The exact primary-source normalization is checked against Damour–Donoghue, [1007.2792v2](https://arxiv.org/abs/1007.2792v2), Eqs. (11)–(24), which separately parameterize alpha, Lambda_3, the electron pole mass and light-quark masses. Electromagnetic running was neglected in their displayed QCD relation, as their footnote 5 states.

## 3. Atomic size is a definite extra equation, not a vacuum principle

For a point nucleus of mass m_N, at leading Coulomb order,

\[
\mu_{eN}={m_e m_N\over m_e+m_N},\quad
a_H={1\over\alpha(0)\mu_{eN}},\quad
R:=a_H m_N={1+1/r\over\alpha(0)},\quad r={m_e\over m_N}. \tag{B4}
\]

The infinite-nucleus Bohr radius and a finite-mass hydrogen radius are different quantities. B4 describes a characteristic Coulomb length, not a hard atomic surface or a nuclear radius. Defining d_e=d ln m_e/dx, d_g=d ln m_N/dx and d_alpha=d ln alpha/dx yields

\[
{d\ln R\over dx}=-d_\alpha-{d_e-d_g\over1+r}. \tag{B5}
\]

Thus a hypothesized scalar-stationary size–mass product constrains *derivatives*. Its numerical value R=R_0 is a separate condition. If m_e,m_N and a_H are all independently measured, B4 measures alpha in this approximation; it does not explain its value. Total galactic baryonic mass additionally needs particle numbers, nuclear composition and observational calibration; it is not the single-nucleon m_N in B4.

## 4. New candidate B-LC: universal gauge function plus QCD vacuum response

Grant a strong closure not in the canonical framework:

\[
Z_3=k_3 B(x),\qquad Z_\gamma^{\rm IR}(0)=k_\gamma B(x),\quad
B(x)=B_*+\tfrac12\beta x^2,\quad B_*,\beta,k_i>0. \tag{B6}
\]

The IR relation in B6 is a stipulated matched relation for this truncated example, not an assertion that identical gauge functions at a UV scale remain identical after running. A UV-universal version must replace it using B2 and the electroweak charge embedding. Set a=8 pi^2 k_3/b_0>0, Lambda=M_U exp(-aB), m_N=C_N Lambda and m_e=y M_U exp(-pB), with p>0. The electron ansatz is an especially generous shared-scaling hypothesis. The independent positive y includes Higgs/Yukawa normalization; no electroweak mass-generation mechanism has been derived for it.

Now try an actual scalar potential,

\[
V_{\rm eff}(x)=U(B(x))-C\Lambda(x)^4+n_Nm_N(x)+n_em_e(x),\qquad C>0. \tag{B7}
\]

The term -C Lambda^4 is a **matched candidate term**. The trace anomaly alone does not determine its absolute cosmological value, its sign in a fully matched theory, or U. A consistent scheme change redistributes those pieces and leaves their sum invariant. This calculation assumes the displayed negative term with C fixed and asks what it actually does. Number densities are conserved, slowly varying nonrelativistic sources on the time-scale of the local stability test; it is not a full cosmological solution.

At x=0, B'=0, so V_eff'=0 and all displayed first derivatives of masses and alpha vanish. Direct differentiation and an independent chain-rule check give

\[
f^2m_\phi^2=V_{\rm eff}''(0)
=\beta\,[U_B+4aC\Lambda_*^4-a n_Nm_{N*}-p n_em_{e*}]. \tag{B8}
\]

A cold population adds -p_c n_c m_c inside the bracket. With U_B=0 and no matter, B8 is positive: the QCD vacuum creates a stable local scalar minimum for *every* admitted B_*. Positive matter contributes the opposite curvature. A maximum of B, beta<0 in a local patch, instead makes decreasing positive masses locally minimal. Damour–Polyakov's [hep-th/9401069v1](https://arxiv.org/abs/hep-th/9401069v1), Eqs. (2.9)–(2.11), (4.4)–(4.6), makes precisely that matter-attractor choice; their common B is at a maximum. Their more complete Einstein-frame mass includes a B^(-1/2) factor. It changes magnitudes, not the decreasing-mass sign used here.

This exposes a new physical obligation: a light least-coupling matter attractor cannot simply inherit an uncancelled negative QCD vacuum potential. Canceling U(B_*)-C Lambda_*^4 to the observed tiny vacuum energy fixes one *value*. It does not imply U_B(B_*)=-4aC Lambda_*^4 or cancel B8. For f of gravitational size and dimensionless coefficients of ordinary size, the QCD-induced mass scale is Lambda_*^2/f, not the Hubble scale. Calling the scalar cosmic dark energy would require independently justified suppression/cancellation of its curvature as well as its vacuum value. No numerical naturalness bound or present experimental exclusion is claimed.

There is no generic equivalence-principle exclusion at x=0: all first derivatives in this common-extremum ansatz vanish. Away from it, composition-dependent scalar charges are derivatives of nuclear/electron/electromagnetic mass contributions, as in Damour–Donoghue Eqs. (71)–(76). Those tests constrain derivatives and displacement, not B_* by themselves. A density-driven sign change of B8, or a tilt in U, is a relevant environmental discriminator; its existence/magnitude depends on the actual matched U and C. The calculation does not assume an unavoidable observed alpha variation.

## 5. Exact mass–size–vacuum counterfamily and the strongest exception

Even with B6, prescribe fixed positive nucleon mass M, fixed R_0 and fixed cosmic vacuum value rho_DE. For every t in an open interval

\[
0<t<{R_0\over4\pi k_\gamma}
\]

(restrict it further to any shared EFT-valid/perturbative window), set

\[
\begin{split}
B_*&=t,& M_U(t)&={M\over C_N}e^{at},\\
y(t)&={C_Ne^{-(a-p)t}\over R_0/(4\pi k_\gamma t)-1},&
U_0&=\rho_{\rm DE}+C(M/C_N)^4. \tag{B9}
\end{split}
\]

Take U=U_0 and keep a,p,beta,C,C_N,k_gamma,f fixed. Substitution yields exactly

\[
m_N(0)=M,\quad a_Hm_N=R_0,\quad V_{\rm vac}(0)=\rho_{\rm DE},\quad
\Lambda(x)={M\over C_N}e^{-a\beta x^2/2},\quad
\alpha(0)={1\over4\pi k_\gamma t}. \tag{B10}
\]

The whole QCD scalar profile and its positive vacuum curvature are unchanged while alpha changes. The electron mass compensates, m_e(0)=M/[R_0/(4 pi k_gamma t)-1]. The scalar has a common extremum with zero linear couplings throughout this family. This does **not** preserve a separately specified electron/nucleon mass ratio. If that ratio and R_0 are both supplied, B4 already contains alpha.

A parameter count makes the remaining input precise. In coordinates (B_*, log M_U, log y, U_0), let r=m_e/m_N, Q=C Lambda_*^4 and w=1/(1+r). The rows for (log m_N, log R, rho_vac) are

\[
J=\begin{pmatrix}
-a&1&0&0\\
1/B_*-(a-p)w&0&-w&0\\
4aQ&-4Q&0&1
\end{pmatrix},\quad
v=\begin{pmatrix}1\\a\\(1+r)/B_*-(a-p)\\0\end{pmatrix}. \tag{B11}
\]

The minor in columns 2,3,4 is -w, so rank J=3 on the whole positive domain. Jv=0, while d log alpha(v)=-1/B_* is nonzero. Stationarity at x=0 adds no row involving B_*; its satisfaction is structural. B9 is the finite integrated family and prevents mistaking a tangent degeneracy for an exact one. Gauge anomaly cancellation and the charge lattice remain intact; this is not a scalar-dependent redefinition of electric charge.

**Strongest surviving exception.** Add a separately fixed physical M_U. The augmented determinant is a/(1+r)>0. In this four-parameter truncated model m_N then fixes

\[
B_*={1\over a}\log{C_N M_U\over m_N},\qquad
\alpha(0)^{-1}={4\pi k_\gamma\over a}\log{C_N M_U\over m_N}. \tag{B12}
\]

This is a genuine conditional mass-to-coupling map, not a claim that scalar vacuum stationarity can never select alpha. Its independent premises must fix M_U, k_i, flavour spectrum, C_N/light-quark ratios and *the complete functions and finite matching in B2*. With a UV-universal gauge function, B12's last expression receives the actual running/matching functional; it is not already physical alpha(0). If M_U is independently fixed by gravitational theory, the kernel used by B9 is no longer admissible. The canonical framework presently fixes neither that common threshold nor B6 nor the electron amplitude y. No repeated SM-desert/unification numerical fit is performed here.

## 6. New candidate B-EXP: can QCD and a gravitational runaway select x?

To test a scalar extremum with B' nonzero, take Z_3 linear in x so Lambda=Lambda_0 exp(-a x), and independently posit a positive runaway potential A exp(-p x):

\[
V(x)=\rho_0+A e^{-p x}-C\Lambda_0^4e^{-4a x},\qquad a,p,A,C>0. \tag{B13}
\]

For p different from 4a there is at most one stationary point,

\[
x_*={\log[pA/(4aC\Lambda_0^4)]\over p-4a}. \tag{B14}
\]

Writing X=A exp(-p x_*) and Y=C Lambda_0^4 exp(-4a x_*), stationarity is pX=4aY. Consequently

\[
V''(x_*)=p(p-4a)X,\qquad V(x_*)-\rho_0=(1-p/(4a))X. \tag{B15}
\]

The stable branch requires p>4a and lies below the constant offset. Without rho_0 it is AdS, not the positive observed vacuum. With rho_0 an independent uplift can fix the vacuum value, but A/(C Lambda_0^4) still fixes x_*; choosing it to hit alpha is a fit. At p=4a, equal amplitudes make the displayed potential constant (no isolated minimum), and unequal amplitudes give no finite stationary point. Scalar positivity alone does not normalize the photon coefficient. If a complete theory independently fixes all B13 coefficients and photon/QCD functions, B14 could select x and B2 could predict alpha. No such action is derived from the current polarization theory.

## 7. Executed evidence, failures and first unresolved implication

`check_scalar_bridge.py` verifies 23 exact symbolic identities with Python 3.9.6 / SymPy 1.14.0. The reduced-mass identity, complete finite family, nonzero Jacobian minors and both curvature formulas are checked; B8 is cross-checked by differentiating with respect to B instead of x. These calculations support the stated truncation, not full cosmological attraction, EFT radiative closure, or a quantum-gravity completion. Mathematical checks are self-reviewed pending the coordinator's independent review.

Canonical computation: `run_002/manifest.json`, status **completed**, input hashes unchanged, validation passed. `run_001/` is retained with status **launch-failed** because a macOS RLIMIT_AS pre-exec setting failed; it produced no physical result. A preceding attempt requesting CPU affinity was rejected before creating a directory because the platform lacks that API. These are runner/environment failures, not failed physics. Exact reproduction and source/version/hash records are in `REPRODUCE.md`, `source_records.json` and `INPUTS.sha256`.

The first unresolved implication is **framework vacuum/cold dynamics => an independently fixed physical common gauge function, threshold and scalar potential**, including their finite matching. A theory supplying only a vacuum density or a common extremum has not supplied those data.

The next discriminator is to derive U(B), Z_3(B), the physical projected photon function and the Higgs/Yukawa function from one specified candidate, then compute the admissible variations with the physical gravitational matching scale held fixed. Test whether the QCD contribution to B8 is canceled as a *function*, whether the chosen extremum remains stable with the counted matter/cold populations, and whether the augmented constraint kernel still changes the fully matched alpha(0). That is the concrete place where a new physical relation can beat this counterfamily.
