# Source-critical note, pinned before author inspection

## Authentication and extraction

The exact-ID cache lookup `arxiv:1812.04100v3` returned one exact hit. It is Stephen P. Martin, *Matching relations for decoupling in the Standard Model at two loops and beyond*, PDF cover stamped arXiv:1812.04100v3, 25 January 2019, primary locator <https://arxiv.org/pdf/1812.04100v3>. The cached PDF SHA-256 is `dd48e1f2a843c5cc3c8355511013d45f5995c5cfa2979ea028e1335ac5742f71`; extracted layout text SHA-256 is `7b3debfca831f340aaf2f55d9078e4fb7caa300d1dfb73bdc2e9738d948d7170`. The metadata record has an empty authors array, so authorship was authenticated from the PDF itself, not inferred from that field. The cache is ignored under the repository's root `.gitignore` rule. No new network fetch was required.

I read the PDF-layout extraction and visually inspected printed PDF pages 11, 12, 14 and 16, including (2.15)-(2.16), (2.20), (2.26), and (3.7). Numbering below is the PDF numbering: generic light mass at one loop is (2.20), mixed light mass is (2.26), strong heavy-fermion QED is (3.7). The HTML equation numbers are not used.

The source provides explicit renormalized MSbar finite matching formulas, not merely beta functions. Equations (2.1)-(2.3) expand fractional alpha, alpha_s and masses in `(16 pi^2)^(-ell)`. Section III instead expands in `(4 pi)^(-ell)` while using alpha and alpha_s inside its vartheta; replacing alpha=e^2/(4 pi), alpha_s=g_s^2/(4 pi) restores the same two-loop convention. Its underlined quantities are the lower-energy ones.

## Hierarchy and sequential composition

Let `r=W/Z`, `s=1-r`, and `Lx=log(x/Q^2)`. Keep g,g',v and h,W,Z fixed and take `t=y_t^2 v^2/2` to zero. This is a mathematical extraction limit outside the source's preferred physical hierarchy; it is not the limit `t -> 0` at fixed nonzero y_t. From PDF (1.15), `F(t,M^2)=O(log(t)/t)` for fixed positive M^2. Each prefactor in the y_t^2 sector of (2.16) cancels at most that inverse t, so the entire y_t^2 sector is `O(t log t)` and vanishes. Also `t/(t-W) log(t/W)` vanishes. Pure QCD top pieces are kept separate.

The surviving mixed part of PDF (2.16), divided by g_s^2 g^2, is

```
S = -8s/9 Lt + 3 LW
    + (25/(18r)-13/9+14r/9) LZ
    -49/27-r/18-163/(216r).
```

The QED top part from PDF (3.7), in the same normalization, is

```
T = -s T_F Q_t^2 (4 Lt + 13/3),   T_F=1/2, Q_t=2/3.
```

There is a further term from the one-loop top mass threshold. Equation (2.20), continued to a negligibly light top in the EW-first theory, gives

```
A = theta_mtop^(1)/g^2
  = (6+3/r)/16 + s(4r-1)/(9r) (3 LZ-5/2).
```

This use of (2.20) is justified by the vanishing of top Yukawa interactions and the equivalence of the up-type external fermion in this limit. It is not a quoted explicit top-matching theorem in Martin. One can keep t finite until both sides are composed; then `ln t_low = ln t + 2 a theta_mtop^(1)`. Inserting this in `(2/3) a g_s^2 ln t_low` gives `(4/3) a^2 g_s^2 theta_mtop^(1)`. Consequently the EW-only six-flavor hard coefficient is `S-T-(4/3)A`, not just `S-T`.

Exact algebra gives

```
S-T-(4/3)A
 = 3 LW + (11/(6r)-11/3+10r/3) LZ
   + 1/2-5r/2-11/(8r).
```

This cancels the infrared top logarithm and gives the charged/neutral factorization below. Those are separate checks: cancellation of Lt alone would not check the finite mass-composition subtraction.

## Coupling dictionary and vector projection

For a colorless neutral gauge boson coupled as `V_mu bar q gamma^mu (c_L P_L+c_R P_R) q`, the massless quark gluon amplitude depends on the sum of the two chiral squares. The two-loop strong threshold inferred from the preceding factorization is

```
a^2 g_s^2 sum_q T_F(c_Lq^2+c_Rq^2) [2 LM-3/2].
```

Indeed the six-flavor Z sum divided by g^2 is `11/(12r)-11/6+5r/3`, with `c_L=g/sqrt(r)(T3-Qs)`, `c_R=-g/sqrt(r) Qs`. The charged W sum is `3/2` in the same units. Multiplying these by `2 LM-3/2` reproduces both logarithms and every finite rational term above. Here the charged current has g/sqrt(2), three quark doublets, two orientations, and T_F=1/2. There is no additional factor of three from color.

This factorization uses the diagram topology, not an arbitrary substitution g'->e. At order g_s^2 c^2 in the fractional alpha_s threshold, a colorless vector can occur only as an exchange joining quark lines in the gluon vacuum-polarization matching, with all placements of the two external gluons, quark self-energy/vertex contributions, and renormalization terms included. A pure colorless-vector or scalar loop has no gluon coupling. In the massless Yukawa-zero limit, chirality forbids c_L c_R terms in this gluon amplitude. No one-gamma5 anomalous triangle is required for its conserved-vector projection. The canonical Abelian vector has c_L=c_R=e Q_q, hence `sum T_F(c_L^2+c_R^2)=e^2 sum Q_q^2`.

For PDF (2.20) and the mixed g_s^2 part of (2.26), use `g'^2 Q(T3-Qs)=-c_L c_R` and `(c_L-c_R)^2=(g^2+g'^2)/4`. After separating the charged W terms, the neutral contributions are

```
theta_m^(1)|neutral
  = -c_L c_R(3 LM-5/2)+3/4(c_L-c_R)^2,
theta_m^(2)|neutral,mixed / (C_F g_s^2)
  = -3 c_L c_R(LM-17/12)
    +(c_L-c_R)^2(9/2 LM-15/8).
```

Putting c_L=c_R=eQ gives the PRETARGET mass formulas. In particular the axial coefficient cannot be used as the vector coefficient: it contains the terms proportional to `(c_L-c_R)^2`.

## Conditions and remaining bridges

Martin uses v at the Landau-gauge effective-potential minimum; summed tadpoles vanish in that convention. Keeping v fixed and taking y_t to zero is necessary. Changing to a tree-level v and selectively dropping tadpoles would change the finite bookkeeping and invalidate the sequential subtraction. The conserved-vector projection drops the chiral difference terms, so no VEV or axial finite term should be added to the canonical Abelian result.

The source obtains gauge matching from the pole residue in scattering, and mass matching by pole-mass equality; its formulas include subtraction of UV poles, matching of the massless infrared sector, and renormalized finite terms. Ward identities justify a conserved canonical Abelian vector's longitudinal decoupling. The present audit does not re-evaluate the two-loop integrals, prove region completeness independently, or independently reconstruct the d-dimensional counterterm algebra. In particular, the finite rationals have inherited evanescent-times-pole contributions from the source calculation. A four-dimensional integrand manipulation or a beta-function-only check cannot replace that input.

A photon propagator `1/(k^2+lambda^2)` specifies a smooth massive-vector prescription. It does not specify a sharp O(4) restriction on photon momentum. The finite transfer between these prescriptions requires a defined regulator kernel and a matching integral including the log-dependent mixed mass/gluon kernels. Neither the finite 5/2 or 17/4 in mass matching nor the gluon -3/2 can be relabeled a sharp-cutoff constant without that bridge.

For a proton scalar insertion, a coefficient multiplying the canonical gluon operator G^a_mu_nu G^{a mu nu} contributes through its properly normalized renormalized matrix element. The trace identity is `theta^mu_mu = beta_s/(2g_s) [G^2] + sum_q (1+gamma_mq) m_q [qbar q]` in the convention `gamma_m=-d ln m/d ln Q`. Thus the gluon matrix element scales as 1/g_s^2 in the weak-coupling counting of this identity. A Wilson coefficient of order e^2 g_s^4 can contribute to the same hadronic order as the displayed mixed e^2 g_s^2 quark-mass coefficient. The leading gluon threshold plus mixed mass threshold therefore does not by itself constitute a complete relative-order g_s^2 proton result. Operator mixing, signs for converting parameter variation into scalar action insertion, matching-scale dependence, and finite scheme conversions have to be tracked together.

Verdict before author inspection: source identity and requested formulas authenticated/extracted; exact sequential algebra and vector projection derived; their application to the canonical heavy vector is supported by the stated massless-current/topology bridge. Sharp-cutoff finite transfer and a physical proton response remain unverified here, and full QCD R or alpha cannot follow from this short-distance matching alone.
