# Independent derivation saved before opening the target arguments

Date: 2026-10-19. Reviewer: fresh isolated subagent `/root/uv_sea_review`.
Before this file was written I opened only the task instructions, skills, the
allowed `sea_ope/SOURCE_RECEIPTS.json`, and the three source PDFs/text files it
located. I have not opened `sea_ope/DERIVATION.md`, `REPORT.md`, `compute_uv.py`,
its run records, or the coordinator target arguments/code. The receipts include
author translation labels; these were visible, but the calculation below was
reconstructed from definitions and source equations, not their claimed result.

## Definitions and extraction

Take metric signature +---, covariantly normalized hadron states, and
`<O> = (1/2) sum_s <p,s|O|p,s>`, with vacuum/disconnected identity contributions
removed. Let `j^mu = sum_f Q_f qbar_f gamma^mu q_f`, without a factor of e, and
`e^2 = 4 pi alpha`. Define `H^{mu nu} = i integral d^4x exp(i q.x)
<T j^mu(x) j^nu(0)>`. This equals Hill--Paz's spin-averaged W tensor, not
Gasser's T tensor: Gasser A.3 has an additional factor 1/2, so `H=2 T_G`.

For `P^{mu nu}=-g^{mu nu}+q^mu q^nu/q^2`, Hill--Paz v2 Eq.7 is

`H^{mu nu} = < P^{mu nu} C_1/q^2
 + P^{mu nu} q_a q_b C_2^{ab}/q^4
 + P^mu_a P^nu_b C_3^{ab}/q^2 > + higher dimension`,

where `C_1=sum c_1f m_f qbar_f q_f+c_1g G_c^2` and
`C_i^{ab}=sum c_if O_f^{(2)ab}+c_ig O_g^{(2)ab}`. Eq.6 defines canonical
`G_c^2=G^A_ab G^{Aab}`, and all spin-two operators are d-dimensional traceless.
The rendered v2 PDF, physical page 5 (printed page 4), Eq.9 gives
`2 c_1f = c_2f = -c_3f = 4 Q_f^2`. The text extraction contains obsolete
overlapping signs, so the rendered equation is decisive. Rendered physical
page 8, Eq.19 gives, writing `S=sum Q_f^2`,

`c_1g=alpha_s S/(12 pi)`,
`c_2g=(alpha_s/(4 pi)) S[-14/3+(8/3) log(Q^2/mu^2)]`,
`c_3g=(alpha_s/(4 pi)) S[2-(8/3) log(Q^2/mu^2)]`.

These are leading coefficients, not all-order formulae.

## Full tensor contraction and O(d) shell

The scalar trace is `g_mn H_0^{mn}=-(d-1)<C_1>/q^2`.
The spin-two trace is

`g_mn H_2^{mn}= - q_a q_b [(d-1)<C_2^{ab}>+<C_3^{ab}>]/q^4`.

The `g_ab C_3^{ab}` term vanishes by tracelessness. On an O(d)-invariant
Euclidean shell, `<Q_a Q_b/Q^2>_Omega=delta_ab/d`; the analytically continued
version contracts each spin-two tensor with its trace and is exactly zero.
This works for arbitrary scalar Wilson functions of Q^2, including their
logarithms/poles. It is not a statement that W_1 at nu=0 has no spin-two term.
Taking only that subtraction function would discard the compensating tensor
piece. Isotropy of the regulator and a full Euclidean angular shell are premises.

## Scalar photon band, including normalization and sign

Gasser Eq.58, its tensor decomposition, and `H=2 T_G` give the Minkowski
expression `delta m= i e^2/(4m) integral d^4q/(2pi)^4 H^mu_mu/(q^2+i0)`
plus local counterterms. Wick rotation of its UV region gives
`delta m_band=e^2/(4m) integral_band d^4Q/(2pi)^4 H^mu_mu(q_0=iQ_4)/Q^2`.
For the scalar term, `H^mu_mu=3<C_1>/Q^2`. The radial shell integral is
`integral_band d^4Q/(2pi)^4 Q^-4=log(Q_h^2/Q_l^2)/(16 pi^2)`.
Thus

`delta m_band/m = [3 e^2 c_1g <G_c^2>/(64 pi^2 m^2)] log(Q_h^2/Q_l^2)`.

For massless SU(3) QCD with n_f active flavors, the leading trace anomaly is
`Theta^mu_mu=[beta_s(g_s)/(2g_s)] G_c^2`,
`beta_s/g_s=-beta_0 alpha_s/(4pi)+O(alpha_s^2)`,
`beta_0=11-2n_f/3`, and `<Theta>=2m^2`. Hence
`<G_c^2>=-16 pi m^2/(beta_0 alpha_s) [1+O(alpha_s)]`.
Combining factors yields

`delta m_band/m = - alpha S/(4 pi beta_0) log(Q_h^2/Q_l^2)
 + O(alpha alpha_s log)`.

For `(Q_u,Q_d,Q_s)=(2/3,-1/3,-1/3)`, `S=2/3`, `beta_0=9`, so the coefficient
is `-alpha/(54 pi)` per log of squared scales, or `-alpha/(27 pi)` per log
of scales. The sign comes from the negative canonical gluon matrix element;
there is no positivity theorem for this scalar contribution.

## Independent counterterm check and mixed beta function

The rendered corrected Gasser v3 physical pages 16--17 show
Eq.56 gluon term `-delta g G_r^2/(2g^3)`;
Eq.57 `delta g=-e^2 g^3 S log(Lambda^2/mu^2)/(256 pi^4)`;
Eq.64 `delta m_ct=delta g <G_r^2>/(4 m g^3)` in the massless theory.
The g^-3 action derivative uses the rescaled field strength, for which
`G_r=g G_c`; using canonical G_c directly in Eq.64 would miss g^2.
Substitution gives

`delta m_ct/m=+alpha S/(4 pi beta_0) log(Lambda^2/mu^2)`.

It therefore cancels the scalar UV logarithm, with the opposite sign.
Differentiating the cutoff logarithm with respect to log Lambda supplies a
factor 2. The corresponding QED contribution to the strong beta function is
`beta_s^EM=+2 S g_s^3 e^2/(16 pi^2)^2`; its sign slows asymptotic freedom.
For three flavors its mixed coefficient is `2S=4/3`. Omitting the factor of
2 between log Lambda and log Lambda^2 gives an incorrect beta coefficient.

## Scope that follows before seeing any target

This is the leading, asymptotic, short-distance local scalar term from two
electromagnetic currents on a closed charged quark loop matched to gluons.
It is consistent with calling that topology a sea contribution at this order.
It does not define an all-scale, scheme-independent separation of a hadron's
electromagnetic mass into valence and sea terms. Spin-two shell cancellation
does not remove finite lower-momentum sea response or every higher-order term.

At fixed alpha, in the same massless theory, all hadron masses are proportional
to its single dimensionful QCD scale; the displayed UV scalar rescaling is
universal. Therefore it cancels between numerator and denominator of a mass
ratio normalized using one calibrated hadron. That cancellation alone does not
fix the finite, dimensionless alpha dependence of that ratio. Nonzero alpha is
a dimensionless parameter that can change the spectrum; no all-order vanishing
of ratio response follows from the trace anomaly. At zero electromagnetic
charges, S=0 and the photon-induced coefficient vanishes; at alpha=0 the same
term vanishes. Dividing by alpha or S requires taking a limit rather than
evaluating a zero denominator. The leading coefficient can survive in such a
normalized derivative limit without creating an interaction at alpha=0.

The OPE calculation assumes asymptotic freedom with fixed active flavors,
Q_l sufficiently far above confinement, fixed finite external hadron momentum,
an admissible Euclidean continuation, vacuum subtraction and an O(d)-symmetric
shell. It is not an error-bounded estimate for a band near the hadronic scale.

## Source identity

PDF SHA-256, independently recomputed before this note:

- Hill--Paz arXiv:1611.09917v2, 30 July 2017:
  `3f9d11e18924f98dab0dcf40ff5e017738f4f6994c2dce580098e7aeabda3a1b`.
- Gasser et al. arXiv:1506.06747v3, 30 March 2020:
  `c44709743db788651e71c20874e22bad2212a8e54a07fac158140540e12cca41`.
- Hill--Solon arXiv:1409.8290v1:
  `65ea75a65f18a8ef6883aacac65fabfb55a4ff9d23095ed5c821c4bcff933158`.

The first two rendered PDFs and version stamps were inspected locally. The
versioned Hill--Paz PDF was additionally available through the web tool; the
Gasser versioned web fetch failed, so exact local PDF inspection and the pinned
receipt/hash provide the source check in this session. No source cache mutated.
