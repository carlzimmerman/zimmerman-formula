# FSP-003: fresh chiral and metric derivations

Written 2026-10-19 UTC before opening electromagnetic/REPORT.md, its code, self-reviews, coordinator/METRIC_RESPONSE.md, or parent verdicts. This is a bounded independent reconstruction in a fresh subagent, not a full QCD calculation. The parent supplied the three candidate formulas and source locators, so this is adversarial verification of those candidates, not a blind search. electromagnetic/SOURCES.json was read to locate/authenticate cached primary PDFs; its source-application summaries were visible. That is a provenance limitation, though no target report or implementation was opened before this file was saved.

## Claim card

At fixed renormalized light-quark masses, fixed QCD matching convention and scale, and positive nonzero pion mass, derive the leading electromagnetic charged-pion determinant contribution to the two-flavor susceptibility, and the individual nucleon electromagnetic local and nonanalytic loop contributions. Check whether chiral/gauge/isospin symmetry alone forces their independent low-energy constants (LECs) to cancel in A_H/m_p^3. Independently derive the isotropic stress from a Euclidean round-S4 effective action and identify the observable represented by a current-current insertion.

The chiral formulas below concern flat-space effective field theory. They do not by themselves determine a coefficient linear in H, or establish that susceptibility determines cosmological stress. Expansions in e^2 are derivatives at e^2=0 with M>0 held fixed. The limit M->0 is nonuniform for the expansion in the pion splitting.

## Primary inputs

- Marco Gorghetto and Giovanni Villadoro, *Topological Susceptibility and QCD Axion Mass: QED and NNLO corrections*, arXiv:1812.01008v2, 7 December 2025. Appendix A.1, equations (27)-(36), printed pp.10-11. Version authenticated against https://arxiv.org/abs/1812.01008v2 on 2026-10-19 UTC. Local PDF SHA-256: `6b470086b514106044472c0a18fb607b6799a74455c0ef54b77a714f01296c92`; extracted text SHA-256: `3a1231d492f201691d25c58be83f00cfe81c6eead297475e7525f3cd70f0e84e`.
- Guido Mueller and Ulf-G. Meissner, *Virtual photons in baryon chiral perturbation theory*, arXiv:hep-ph/9903375v1, 17 March 1999. Equations (2.16)-(2.17), (2.28)-(2.29), (3.4), and printed (3.8). Version authenticated against https://arxiv.org/abs/hep-ph/9903375v1 on 2026-10-19 UTC. Local PDF SHA-256: `557da4348f9bea82d8e553bc6f86e0a8d67b365adeafd4f4c38c650b48b32f89`; extracted text SHA-256: `eafa3bc6d8ef860c6ec86097a49d2472327610473f287d18bb020178014c823e`.

Both exact-version lookups in the existing project literature cache returned no entry. Existing temporary primary files were used; no duplicate full source was retained. All necessary page extraction is read-only source inspection. Rendered page excerpts are retained here for review. These commands do not execute a numerical or symbolic mathematical experiment; all derivations below were performed by hand.

## 1. Charged-pion determinant at fixed quark masses

Let M^2=B(m_u+m_d), r=m_um_d/(m_u+m_d)^2=z/(1+z)^2, and F be the QCD chiral-limit decay constant. Use d=(m_d-m_u)/(m_d+m_u) for isospin asymmetry, reserving Delta_EM for a mass-squared splitting. The aligned LO potential has pion mass parameter

    x(theta)=M^2 sqrt(1-4r sin^2(theta/2)).

At theta=0, x=M^2, x'=0, x''=-r M^2. The tree susceptibility is chi_0=r F^2 M^2. The LO electromagnetic meson operator is constant on the diagonal aligned vacuum because the charge matrix commutes with that vacuum; it does not add a theta-dependent tree potential. It raises the charged pion mass-squared by

    Delta_EM = 2 e^2 F^2 Z.

There are two charged real fields, hence one complex scalar determinant. Its vacuum functional per volume is integral log(p^2+x), not one-half that integral. In the GL chiral subtraction convention used by the cited formula, the finite determinant can be represented as

    g_GL(x)=x^2/(32 pi^2) [log(x/mu_chi^2)-1/2],
    g_GL'(x)=x/(16 pi^2) log(x/mu_chi^2),
    g_GL''(x)=[1+log(x/mu_chi^2)]/(16 pi^2).

Polynomial vacuum counterterms are understood in this representation. At first order in the splitting, the electromagnetic determinant difference is Delta_EM g_GL'(x(theta)). Its second theta derivative is

    delta chi_loop = Delta_EM g_GL''(M^2) x''(0)
                   = -r M^2 Delta_EM/(16 pi^2)
                     [1+log(M^2/mu_chi^2)].

Therefore

    delta chi_loop/chi_0
      = -e^2 Z/(8 pi^2) [1+log(M^2/mu_chi^2)].

The candidate has the correct charged-field multiplicity, sign, and coefficient in this subtraction convention. The sign of a numerical value depends on mu_chi and is not by itself an observable. The constant 1 is not separately scheme invariant: in conventional MS-bar, g(x)=x^2[log(x/mu^2)-3/2]/(32 pi^2) gives the log alone at this step. A finite redefinition of the analytic electromagnetic LEC combination converts between the expressions. The nonanalytic logarithm coefficient is invariant under such local finite redefinitions.

The full fixed-quark-mass result in GV Appendix A.1 (36) is

    chi/chi_0 = 1 + (pure-QCD corrections)
      + e^2 {20/9 (k5^r+k6^r) + 4/9 (1+3d) k7^r
             - Z/(8 pi^2)[1+log(M^2/mu_chi^2)]}
      + higher orders.

This agrees with the determinant reconstruction. The analytic terms are not optional: they cancel mu_chi dependence and participate in the QED scale/scheme dependence of renormalized quark masses. The formula at fixed measured neutral pion mass and decay constant uses a different analytic LEC combination (GV main-text (10)), because those physical observables themselves change when e^2 changes. Using that combination while differentiating along a fixed-quark-mass path would mix paths. Fixed renormalized masses require both the renormalization scheme and the scale to be specified; masses in QCD+QED do not run in the same way as masses in QCD.

As a sign cross-check, the theta curvature of the pion mass is negative, and the complex charged determinant's second mass-squared derivative is positive when 1+log(M^2/mu_chi^2)>0. This makes delta chi_loop negative in that range, in agreement with the formula. Neither this cross-check nor the isolated loop sign fixes the sign of the complete EM correction.

## 2. Individual proton local mass operator

Use the invariant heavy-baryon Lagrangian in MM (2.28)-(2.29):

    L_em^(2)=F_pi^2 Nbar [f1 O1+f2 O2+f3 O3] N,
    O1=tr(Qtilde_+^2-Qtilde_-^2),
    O2=tr(Q_+) Qtilde_+,
    O3=tr(Qtilde_+^2+Qtilde_-^2).

The paper includes e in Q=e diag(1,0), and its trace is the ordinary two-dimensional trace. At zero pion fields u=1:

    Q_+=Q, Q_-=0, tr Q_+=e, Qtilde_+=e tau_3/2,
    O1=O3=e^2/2, O2=e^2 tau_3/2.

It follows directly, with no use of the printed mass formula, that

    L_em^(2)|_vac = e^2 F_pi^2/2
                   Nbar [(f1+f3) 1+f2 tau_3] N.

For L=Nbar(iv.D+C)N the pole satisfies omega+C=0, so delta m=-C. Equivalently, in the relativistic convention a positive additive coefficient multiplying psibar psi reduces the mass coefficient in psibar(i slash D-m)psi. Thus

    delta m_p,local = -e^2 F_pi^2/2 (f1+f3+f2),
    delta m_n,local = -e^2 F_pi^2/2 (f1+f3-f2),
    delta(m_p-m_n)_local = -e^2 F_pi^2 f2.

These are mass shifts of dimension one: [f_i]=mass^-1. The p-n difference removes the independent isoscalar combination f1+f3. It does not determine the individual proton response. An isoscalar EM contribution may be absorbed into the reference mass at one fixed coupling, but its derivative as the coupling changes remains a matching input once the path/reference is fixed.

### Printed equation (3.8): pixels checked

The actual rendered printed p.14 (retained as mm-page14.png) displays an isoscalar term +e^2(f1+f3)/2 and an isovector term -e^2 tau_3 f2/2, with no factor F_pi^2 in either EM term. This is not merely a pdftotext extraction defect. With the definitions and dimensions explicitly stated at (2.28), the formula lacks mass dimension one, and its isoscalar sign disagrees with evaluating the invariant operators and locating the mass pole. The two discrepancies are independent. A silent redefinition of f_i would be a change of conventions; it is not licensed by the displayed definitions. For this review the invariant Lagrangian fixes the local result above. No erratum or alternate convention search was conducted.

## 3. Pion loop and its expansion

At leading heavy-baryon order, each real pion species contributes the same isospin weight to a proton or neutron. The three degenerate species give the known self-energy -3 g_A^2 M^3/(32 pi F^2). With two charged species and one neutral species, the same integral is

    delta m_N,pion = -g_A^2/(32 pi F^2)
                    [M_0^3+2 M_+^3].

The factor two for charged species is necessary. Setting M_0=M and M_+^2=M^2+Delta_EM, then subtracting the e=0 pion loop at fixed M, gives

    delta m_p,loop = delta m_n,loop
      = -g_A^2/(16 pi F^2)
        [(M^2+Delta_EM)^(3/2)-M^3].

This is MM (3.4) translated to the fixed-M convention; replacing F_pi by F at this order changes higher terms. Expansion at fixed M>0 gives

    delta m_N,loop = -3 g_A^2 M Delta_EM/(32 pi F^2)+O(Delta_EM^2/M)
                  = -3 e^2 g_A^2 Z M/(16 pi)+O(e^4/M).

The e^2 M term is nonanalytic in the light quark masses, since M~sqrt(m_q). It is negative for Z>0 and is common to p and n; it cancels in p-n. It is therefore incorrect to infer the individual proton's loop response from the p-n difference. MM (3.3) also shows that the direct photon loop gives no residual mass shift at this order when omega->0 is taken before the photon regulator goes to zero. This does not exclude higher-order photon corrections.

This is the controlled e^2 derivative at fixed M. Treating the unexpanded split-mass expression as exact in e, or sending M->0 in its linearized e^2 expansion, would exceed this statement. For finite Delta_EM/M^2 the unexpanded expression is useful at the displayed chiral order, while its higher powers of e^2 are not a complete calculation at those higher electromagnetic orders.

## 4. Can independent LECs disappear from A_H/m_p^3 by symmetry?

No. Chiral/gauge/isospin symmetry allows independent meson operators with coefficients k_i and baryon operators with coefficients f_i. Setting a baryon isoscalar coefficient to a different value while leaving the meson coefficients unchanged preserves the same symmetries. The isoscalar response changes m_p but not the meson susceptibility. The p-n splitting does not detect this change. There is no Ward identity here tying f1+f3 to k5+k6 or k7.

For illustration only, if a model imposes A_H proportional to chi times additional independently specified factors, then at first order

    delta log(A_H/m_p^3)=delta A_H/A_H-3 delta m_p/m_p.

The local proton term contributes +3 e^2 F^2(f1+f3+f2)/(2m_p) to this fractional ratio; the susceptibility's analytic k_i combination and logarithm remain independently. One can vary f1+f3 continuously within the symmetry-allowed EFT and change the ratio. This is a counterexample to a claim of cancellation *solely from symmetry*. It is not a claim that arbitrary LEC choices all match physical QCD. Physical QCD would choose them through nonperturbative matching. If A_H has an additional response correlated with baryon LECs, that requires an actual dynamical relation, not symmetry alone; the two cited papers supply no such relation.

Since A_H is a curved/finite-size stress coefficient rather than flat-space chi, the stronger open issue is its definition and its response itself. Neither primary source derives A_H. Even an accurate flat-space EM correction to chi cannot establish delta A_H without an additional bridge.

## 5. Round-S4 variation and current-current insertion

Assume a maximally symmetric Euclidean state on round S4 of radius a=H^-1, with renormalized vacuum functional W=-log Z. Write W(H)=V_4(H) f(H); V_4=8 pi^2/(3 H^4). Hold renormalized parameters and subtraction conventions fixed while varying H. For a constant rescaling g_mu_nu->exp(2s)g_mu_nu, H->exp(-s)H and V_4->exp(4s)V_4. Therefore

    dW/ds = V_4 [4f(H)-H f_H(H)].

Define the Euclidean stress convention by delta W=(1/2) integral sqrt(g) T_E^(mu nu) delta g_mu_nu, normalized so constant f gives vacuum density rho=f. Maximal symmetry gives T_E^(mu nu)=rho g^(mu nu), hence dW/ds=4V_4 rho and

    rho(H)=f(H)-(H/4) f_H(H).

With standard continuation to de Sitter, the invariant Lorentzian vacuum stress has T_mu_nu=-rho g_mu_nu. Thus f=a_0+a_1 H gives rho=a_0+(3/4)a_1 H. More generally a_p H^p gets the factor 1-p/4. A constant W term gives f proportional H^4 and zero stress under this variation, which is a useful check on distinguishing W/V from stress. Logarithms require differentiating their H dependence as well. This derivation assumes round-S4 invariance and a differentiable W(H); it does not establish a linear-H term or justify transplanting an unrelated compact manifold result to S4.

Now integrate a canonically normalized Euclidean photon with coupling i e A_mu J^mu. The Gaussian integral yields

    S_eff=S_QCD+e^2 I+O(e^4),
    I=(1/2) integral J D J + matched counterterms,
    W(e^2,H)=W(0,H)+e^2 <I>_(0,H)+O(e^4).

The sign follows from the imaginary Euclidean current coupling; if another convention puts a different sign in S_eff, the definition of I must change correspondingly. With the displayed convention,

    partial W/partial(e^2)|_0=<I>,
    partial f/partial(e^2)|_0=<I>/V_4,
    partial rho/partial(e^2)|_0
      = [1-(H/4)partial_H](<I>/V_4).

The current-current insertion divided by volume is the coupling derivative of the free-energy density. It is not automatically the coupling derivative of gravitational stress. The propagator, current contractions, integration measures, and counterterms all depend on the metric. Their metric variation is exactly what the last differential operator encodes on round S4. For a subtracted f(H)-f(0), subtract the corresponding flat-space insertion consistently, then apply the same metric conversion. If the insertion difference is linear in H, its stress coefficient is 3/4 of that free-energy coefficient. Derivatives with respect to alpha instead of e^2 add de^2/dalpha=4pi.

## Dependency graph and preliminary obligation status

1. Aligned LO chiral potential -> x''(0) and chi_0: hand derivation, passed.
2. Complex charged determinant plus Delta_EM -> log coefficient: hand derivation, passed; finite constant restricted to specified subtraction.
3. GV (36) -> full fixed-mass analytic k_i combination: exact primary formula extracted and pixels checked, passed at stated chiral order.
4. MM invariant operator basis -> local p,n masses: direct matrix evaluation and pole sign, passed; printed (3.8) inconsistent with basis.
5. Charged/neutral loop weights -> individual common e^2 M term: hand reconstruction and primary (3.4), passed at stated order.
6. Symmetry -> cancellation of k_i and isoscalar f_i: failed, symmetry-allowed independent variation is a counterexample to the symmetry-only implication.
7. W on round S4 -> rho: hand scale variation, passed subject to stated state/geometry conventions.
8. <I>/V -> f coupling derivative: hand Gaussian integration, passed with matched counterterms and displayed sign convention.
9. Flat-space chi -> A_H -> physical ratio: not addressed by cited inputs; conditional on a missing dynamical/geometry bridge.

No computational suite was run and no new mathematical computation was executed. Commands used were exact-source cache lookup, text reads, SHA-256 checks, PDF rendering and image inspection. Subsequent comparison with project artifacts will be recorded separately without changing this saved pre-comparison derivation.
