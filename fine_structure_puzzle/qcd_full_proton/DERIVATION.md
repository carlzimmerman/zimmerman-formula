# FSP-011 author derivation: what the full proton response needs, and the one missing observable

**Alpha is not derived here. No R(alpha), A_rho, finite-alpha dependence or alpha value is computed.** The package addresses only item 1 of the handoff ("full proton response"). It asks which first-order two-current proton data the stuck step needs, which of them exist, what can be assembled from published numbers without fitting, and what single observable remains.

Numbers quoted below come from [run_001/result.json](run_001/result.json). Sources and their authentication are in [SOURCES.json](SOURCES.json). An independent re-derivation of the critical step (section 3) and of the kernel normalization is in [REDERIVATION.md](REDERIVATION.md).

## 0. Target and path

Write u=e^2. The proton datum in

    R_u = A_u/M^3 - 3 A M_u/M^4

is M_u^p = dM_p/du at u=0 along one fixed renormalized QCD path P. Here P holds the MS-bar g_s(mu0) and m_f(mu0) fixed, with f=u,d,s,c, mu0=2 GeV and heavier flavours decoupled. The path also fixes infinite volume, the continuum limit and leading order in u. The common-UV-ratio note shows that only the scale direction of a path change cancels in R_u; a quark-mass direction does not (FSP-010 COMMON_UV_RATIO eq. (1); re-checked symbolically in REDERIVATION R5). The vacuum coefficients A and A_u must be computed on the same path. They are not touched here.

## 1. Master formula

Use the Euclidean Cottingham representation in Feynman gauge with a sharp O(4) photon cutoff Lambda, followed by matching:

    M_u^p = lim_{Lambda->inf} [ I(Lambda) + M_u,ct(Lambda, mu0) ],
    I(Lambda) = 1/(32 pi^3 M) int_0^{Lambda^2} dQ^2 int_{-1}^{1} dx sqrt(1-x^2)
                [ -3 T_1(iQx, Q^2) + (1-x^2) T_2(iQx, Q^2) ].                    (1)

T_1 and T_2 are the spin-averaged forward virtual Compton amplitudes of the full current j = sum_f Q_f qbar_f gamma q_f. They use the tensor convention of Walker-Loud, Carlson and Miller ([1203.0254v2](https://arxiv.org/abs/1203.0254v2), eqs. (2)-(5)) and relativistic state normalization. Every Wick contraction is included, connected to the proton through the gauge ensemble. Equation (1) is FSP-008 proton_kernel eq. (1) with P(Q^2)=theta(Lambda^2-Q^2). REDERIVATION R0 re-derives it from the Wick rotation. The local term is

    M_u,ct = sum_f Q_f^2 sigma_f [3 log(mu0^2/Lambda^2) + 5/2]/(16 pi^2)
             + (gluon threshold, FSP-010 gluon_matching) + (unknown next gluon Wilson order) + power corrections.

## 2. Born and non-Born pieces

Split T = T^B + T^NB. T^B is the full on-shell Born amplitude in the FSP-008 convention, including the non-pole Dirac polynomial -2F_1^2:

    T_1^B = 2[z^2 G_M^2/(z^2+x^2) - F_1^2],   T_2^B = 2A/(z^2+x^2),   z = Q/(2M).

Physical form factors fall like Q^-4, so I^B converges as Lambda goes to infinity. All Lambda dependence of I, and the whole matching, therefore sits with T^NB:

    M_u^p = M_u^B + M_u^NB(mu0),   M_u^NB(mu0) = lim [ I^NB(Lambda) + M_u,ct ].     (2)

**Kernel normalization check.** A unit point Dirac particle with F_1=1 and F_2=0 has a Born term equal to its whole tensor. It must give 16 pi^2 M_u/m = 3 log(Lambda^2/m^2) + 3/2 + O(m^2/Lambda^2), where 3/2 is the sharp-loop constant behind FSP-010's 5/2 = 4 - 3/2. Both the exact primitive of the FSP-008 kernel and quadrature give 1.50000004 at Lambda/m = 10^4, and the deviation scales as 4m^2/Lambda^2 (result.json A). REDERIVATION R4 reproduces this with a separate two-dimensional code.

## 3. Critical step: isospin decomposition of the complete response

Write the light current as J_ud = alpha0 S + beta1 V3 with S = ubar gamma u + dbar gamma d, V3 = ubar gamma u - dbar gamma d, alpha0 = (Q_u+Q_d)/2 = 1/6 and beta1 = (Q_u-Q_d)/2 = 1/2. Add Q_s O_s + Q_c O_c. QCD dynamics are isospin symmetric at this order, so the nucleon matrix elements of every bilocal product fall into two groups:

* The products SS and O_g O_h, the cross terms {S,O_g}, and the I=0 part of V3V3 are equal for proton and neutron. The I=2 part of V3V3 vanishes between I=1/2 states.
* {S,V3} and {V3,O_g} are proportional to tau_3.

Hence

    M_u^p - M_u^n  depends only on the reduced amplitudes of {S,V3}, {V3,O_s}, {V3,O_c};
    (M_u^p + M_u^n)/2 depends only on those of SS, V3V3(I=0), {S,O_g}, O_g O_h.        (3)

The two sets are disjoint. **No isovector datum, at any precision, determines the isoscalar response.** REDERIVATION R2 checks this symbolically. Mixing between the sets enters only at O(u (m_d - m_u)). The exact split of the proton is

    M_u^p = M_u^(0) + (1/2) M_u^(p-n),   M_u^(0) = Born^(0) + NB^(0)(mu0).            (4)

The same statement in contraction classes, with physical charges and u,d,s,c (result.json D), is tabulated below. Each class is defined by where the two currents sit:

* X: both currents on the same valence line (maj = the doubly occupied flavour, min = the singly occupied one).
* Y: the currents on two different valence lines.
* Z: one current on a valence line, the other on a one-current sea loop of flavour l, s or c.
* W: both currents on one sea loop.
* V: the currents on two separate sea loops.

Light u and d sea loops are identical (l) in the isospin limit. Each amplitude counts every placement in its class.

| class | p | n | p-n | (p+n)/2 |
|---|---:|---:|---:|---:|
| X_maj | 4/9 | 1/9 | 1/3 | 5/18 |
| X_min | 1/9 | 4/9 | -1/3 | 5/18 |
| Y_majmaj | 4/9 | 1/9 | 1/3 | 5/18 |
| Y_majmin | -2/9 | -2/9 | 0 | -2/9 |
| Z_maj_l / Z_min_l | 2/9 / -1/9 | -1/9 / 2/9 | 1/3 / -1/3 | 1/18 / 1/18 |
| Z_maj_s / Z_min_s | -2/9 / 1/9 | 1/9 / -2/9 | -1/3 / 1/3 | -1/18 / -1/18 |
| Z_maj_c / Z_min_c | 4/9 / -2/9 | -2/9 / 4/9 | 2/3 / -2/3 | 1/9 / 1/9 |
| W_l, W_s, W_c | 5/9, 1/9, 4/9 | same | 0 | 5/9, 1/9, 4/9 |
| V_ll, V_ls, V_lc, V_ss, V_sc, V_cc | 1/9, -2/9, 4/9, 1/9, -4/9, 4/9 | same | 0 | same |

Several consequences follow.

* **Sea classes and one exchange class are invisible to p-n.** The same-loop sea (W), the separate-loop sea (V) and the connected majority-minority exchange Y_majmin are absent from p-n and present in the proton. FSP-006 had shown this for the same-loop light sea. Here it extends to the connected exchange class and, through (3), to every class.
* **Even the connected classes enter in different combinations.** p-n sees (1/3)(X_maj - X_min + Y_majmaj). The isoscalar sees (5/18)(X_maj + X_min + Y_majmaj) - (2/9) Y_majmin.
* **The Z classes cancel at the SU(3) point.** The l and s Z classes cancel for degenerate light and strange masses, so they start at O(delta), delta = m_s - m_l (FSP-008 sea_flavor eq. (5)).
* **No octet splitting fixes the same-loop class.** In the SU(3) limit the same-loop class is sum_g Q_g^2 W = W Tr Q^2, a pure flavour singlet. It shifts every octet baryon equally, so no octet splitting determines it.
* **Chiral-EFT image.** In two-flavour baryon ChPT with virtual photons, the leading e^2 nucleon mass terms are (1/2)e^2(f_1+f_3) - (1/2)e^2 tau_3 f_2 (Mueller-Meissner [hep-ph/9903375](https://arxiv.org/abs/hep-ph/9903375) eq. (3.8), as rendered by ar5iv). Only f_2 enters m_p - m_n. Independently of that source: with Q_plus/minus = (uQu^dagger +/- u^dagger Q u)/2, one finds Q_+^2 + Q_-^2 = (uQ^2u^dagger + u^dagger Q^2 u)/2. Hence the f_3 monomial <Qt_+^2 + Qt_-^2> = <Q^2> - <Q>^2/2 = e^2/2 is pion independent: f_3 is a pure isoscalar e^2 shift of the nucleon mass. The source itself describes such a term as an "unobservable" e^2 mass shift at fixed e. It becomes observable only when e varies at fixed QCD parameters, which is exactly M_u^(0).

## 4. Heavy-flavour reduction: only the u,d,s current needs nonperturbative data

**Charm same-loop class (W_c) and the charm mass counterterm.** The charm loop has size 1/m_c, so the photon momenta that matter are of order m_c and above; soft photons couple to it only through operators of dimension eight. Integrating out charm turns the class into:

1. the O(u alpha_s) shift of the three-flavour coupling at the charm threshold (a G^2 operator), which is a universal scale direction;
2. the charm mass direction;
3. dimension-six gluon operators suppressed by Lambda_QCD^2/m_c^2.

At leading power and with one-loop decoupling, m_c dM/dm_c = (2/27)[Lambda_3 d/dLambda_3] M = (2/27)(M - sigma_l - sigma_s), and R depends on m_c only through m_{l,s}/Lambda_3. Both charm directions therefore reach R_u only through the light and strange mass derivatives of R. This holds under the COMMON_UV_RATIO hypotheses.

**Charm one-current and two-loop classes (Z_c, V_c).** These need a charm loop with one photon. The photon plus two gluons coupling of a quark loop vanishes identically: Furry's theorem pairs the two orientations into the colour factor Tr[T^a,T^b] = 0 (REDERIVATION R3). By C invariance this persists with internal corrections, because the two-gluon colour tensor must be delta^ab. The first surviving coupling uses the three-gluon d^abc structure. It gives operators of dimension six or more, such as F d^abc GGG/m_c^4 or, through further gluon exchange, del^nu F_{mu nu} qbar gamma^mu q with coefficients proportional to 1/m_c^2. These are orders, not computed bounds.

The nonperturbative two-current data are therefore needed only for j^uds = (2 ubar gamma u - dbar gamma d - sbar gamma s)/3. Charm enters through the FSP-010 local matching (sigma_c, threshold) plus power corrections. Bottom and top decouple further.

## 5. Assembly from published numbers (no fit)

All values are in MeV per e^2. Two parametrisations are used: BBBA05 ([hep-ex/0602017v3](https://arxiv.org/abs/hep-ex/0602017v3) Table 1) and dipole-Galster. Their spread indicates parametrisation sensitivity; it is not an uncertainty.

| piece | BBBA05 | dipole-Galster |
|---|---:|---:|
| Born_p (full Born, all Q^2) | 6.0713 | 6.3711 |
| Born_n | -2.3366 | -2.3344 |
| Born^(0) = (p+n)/2 | 1.8673 | 2.0184 |
| Born^(p-n) | 8.4079 | 8.7055 |
| of Born_p: share of the non-pole -2F_1^2 term | 3.0474 | 3.1852 |

**Convention validation.** Born^(p-n) times 4 pi alpha_ref (the inverse of the sources' own alpha factor) gives 0.771 MeV for BBBA05 and 0.798 MeV for dipole-Galster. Published values are m_el = 0.75(2) MeV (Cao-Dai-Guo [2609.15154v1](https://arxiv.org/abs/2609.15154v1), text after eq. (14), PDF-verified) and 1.39 - 0.62 = 0.77 MeV (WLCM eqs. (19)+(21), local text copy). Dropping the non-pole term would give 0.496 MeV. The published elastic numbers therefore use the same full-Born convention as FSP-008.

**Isovector total.** Equation (4) uses the convention-free published p-n total, so no Born/non-Born split has to be matched to the source:

| (1/2) M_u^(p-n) | value |
|---|---:|
| Cao-Dai-Guo 2026, delta m_QED = 0.71 (+0.03/-0.06) MeV, eq. (19) | 3.871 (+0.164/-0.327) |
| Gasser-Leutwyler-Rusetsky [2003.13612v3](https://arxiv.org/abs/2003.13612v3), 0.58 +/- 0.16 MeV | 3.162 +/- 0.872 |

The known partial sum is Born^(0) + (1/2) M_u^(p-n). It is 5.739 (CDG with BBBA05), 5.030 (GLR with BBBA05), 5.890 (CDG with dipole-Galster) and 5.181 (GLR with dipole-Galster). **This is not M_u^p.** The isoscalar non-Born NB^(0)(mu0) is missing. Its leading local UV piece alone, the FSP-010 isoscalar sigma conversion at mu0 = Lambda, is 0.8140. Of that, 70.9% comes from the charm term (4/9) sigma_c, which by section 4 is scale-like at leading power. This anchor belongs inside NB^(0) and is not added to the partial sum.

**Alpha status.**

* Born^(0) uses charge-normalised elastic form factors, so it is alpha-free at leading order.
* In the CDG isovector total, 94% is the alpha-free elastic piece. The remaining m_F + m_Sbar = -0.044 MeV (6%) rests on cross sections normalised by alpha^2, so its per-e^2 value scales as alpha_meas^-2 through the data.
* Any alpha-selection use must therefore take NB^(0), and preferably the isovector non-elastic part, from e=0 lattice QCD.

## 6. The exact remaining observable

Define T^(0) = (T^p + T^n)/2 for the current j^uds with every contraction class, and T^(0),NB = T^(0) - (T^p,B + T^n,B)/2. Then

    N0(mu0) = lim_{Lambda->inf} { 1/(32 pi^3 M) int_0^{Lambda^2} dQ^2 int dx sqrt(1-x^2)
               [ -3 T_1^(0),NB + (1-x^2) T_2^(0),NB ](iQx, Q^2) + M_u,ct^(0)(Lambda, mu0) },    (5)

    M_u^p = Born^(0) + (1/2) M_u^(p-n) + N0(mu0)   exactly at first order in u.

The equivalent coordinate form is N0 = lim [ (1/2) int d^4x D_Lambda(x) H^(0),NB_{mu mu}(x) + ct ]. Here H is the Born-subtracted Euclidean two-current proton correlator normalised by 1/(2M), as in FSP-008 eq. M_u(reg) and the infinite-volume reconstruction of Feng-Jin [1812.09817v1](https://arxiv.org/abs/1812.09817v1).

Known constraints on N0:

* **Soft end.** The integrand starts at Q^4 with coefficient 3(a-b)^(0)/(32 pi M), the isoscalar static polarizabilities per e^2 (FSP-009).
* **Hard end.** At leading power the spin-0 quark-mass term gives the logarithm cancelled by M_u,ct. The traceless twist-2 term drops out after the O(4) angular integration, because the angular average of q_mu q_nu - delta_{mu nu} q^2/4 vanishes.

Neither constraint fixes the 0.3-2 GeV region. FSP-007 showed that one moment does not fix the integral.

Acquisition requirements are listed in [REMAINING_OBSERVABLE.md](REMAINING_OBSERVABLE.md#acquisition-requirements).

## 7. Restrictions

* The Born numbers depend on published form-factor fits. BBBA05 does not fit the neutron charge radius, so its G_En slope at Q^2 -> 0 differs from the measured one; G_En is small in the integral.
* The isovector totals are dispersive analyses with model elements: a subtraction-function ansatz (CDG eq. (18)) or Reggeon dominance (GLR).
* Equation (3) is exact for isospin-symmetric QCD dynamics; the O(u (m_d - m_u)) mixing is not evaluated.
* The charm reduction is leading power, and its power corrections are not computed.
* The isoscalar UV anchor imports FSP-010's source-calibrated sigma terms unchanged.
* Nothing here fixes A, A_u, R(alpha), the finite-alpha dependence or an alpha-selection equation.
