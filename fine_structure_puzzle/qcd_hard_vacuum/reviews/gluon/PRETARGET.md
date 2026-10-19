# Independent pretarget (before author inspection)

Date: 2026-10-19. Scope: canonical massive Abelian vector, MSbar matching at fixed high-energy running parameters, lambda much larger than retained quark masses. This document was written from Martin arXiv:1812.04100v3, before opening any file in `gluon_matching/`. No author's candidate coefficient was supplied to this reviewer.

I expect, with `L=log(lambda^2/Q^2)` and `a=1/(16 pi^2)`, the leading vector threshold to be

```
alpha_s(low)/alpha_s(high)-1
  = a^2 e^2 g_s^2 sum_q Q_q^2 (2 L - 3/2),   T_F=1/2,
g_s(low)/g_s(high)-1
  = a^2 e^2 g_s^2 sum_q Q_q^2 (L - 3/4),
m_q(low)/m_q(high)-1
  = a e^2 Q_q^2 (-3 L + 5/2)
    + a^2 e^2 g_s^2 C_F Q_q^2 (-3 L + 17/4)
    + terms at other coupling orders.
```

For six active quarks `sum Q_q^2=5/3`; for five it is `11/9`. These sums have no extra factor N_c: the gluon two-point color trace is `T_F=1/2`, and a vector has two equal chiral couplings. Fractional strong-coupling matching means alpha_s unless explicitly labeled g_s.

The critical operation in obtaining the gluon coefficient from the Standard Model is subtraction of BOTH (i) the QED top threshold in PDF (3.7), and (ii) the one-loop top mass matching inserted into PDF (2.15). The second subtraction is `(4/3) g_s^2 theta_mtop^(1)` in Martin's two-loop theta convention. Omitting it leaves incorrect finite and neutral-current coefficients even though the infrared top logarithm cancels.

The displayed results are a prediction of this source-translation audit, not a fresh two-loop integration. The critical source note states the translation assumptions. No equality to a sharp Euclidean four-momentum photon cutoff is predicted. No physical proton electromagnetic mass derivative, QCD R, or alpha value is predicted.

The next checks will independently encode the source equations using exact rational polynomial arithmetic, freeze code/inputs/contract before execution, validate a bounded v2 manifest, and then compare with the author packet. These finite algebra checks do not prove completeness of a diagram calculation or determine a nonperturbative proton matrix element.
