# FSP-011 independent re-derivation of the critical step

**Disclosure.** The author and the reviewer are the same agent; no further agents were spawned, as instructed. Independence is therefore by method, not by person:

* [rederive_fsp011.py](rederive_fsp011.py) does not import the author script.
* It uses different bases (explicit placement enumeration with symbolic charges, and isospin reduced amplitudes) instead of the author's closed-form weights.
* It integrates the Born tensor in two dimensions instead of using the one-dimensional FSP-008 kernel.
* It was executed blind ([run_001/rederive_blind.json](run_001/rederive_blind.json)) before the author output was opened ([run_001/rederive_compare.json](run_001/rederive_compare.json)).

The reviewer had nevertheless read FSP-006's earlier statement about the same-loop light sea and knew the author's intended conclusion. This is not a blind multi-agent review in the programme's earlier sense.

Sections R0-R5 were written from the re-derivation alone. The comparison with the author's verdict comes afterwards, in its own section.

## R0. Cottingham prefactor, from the Wick rotation

Start from the second-order energy shift of a relativistically normalised state, in Feynman gauge:

    dM = (1/2M) (e^2/2) int d^4q/(2pi)^4 [ i T^mu_mu(p,q) ] / (q^2 + i0).

Here T^{mu nu} = (-g + qq/q^2) T_1 + (1/M^2)(p - (p.q/q^2) q)(p - (p.q/q^2) q) T_2. Using p^2 = M^2, nu = p.q/M and q^2 = -Q^2, the trace is T^mu_mu = -3 T_1 + (1 + nu^2/Q^2) T_2.

Rotate q^0 = i q_4. Then d^4q = i d^4q_E, 1/(q^2+i0) = -1/Q^2 and nu = i nu_E. The three factors i, i and -1 combine to +1:

    dM = e^2/(2M (2pi)^4 2) int d^4q_E Q^-2 [ -3 T_1 + (1 - nu_E^2/Q^2) T_2 ](i nu_E, Q^2).

The amplitudes are evaluated at imaginary energy, where Q^4 + 4M^2 nu_E^2 > 0, so the Born denominators have no poles. In 4D polar coordinates, with nu_E = Q x, d^4q_E = 2 pi dQ^2 Q^2 sqrt(1-x^2) dx. Since e^2/(2(2pi)^4) = alpha/(2pi)^3,

    dM = alpha/(8 pi^2 M) int dQ^2 int_{-1}^{1} dx sqrt(1-x^2) [ -3T_1 + (1-x^2) T_2 ],

that is, 1/(32 pi^3 M) per e^2. This reproduces FSP-008 eq. (1). The subtraction-only piece is -(3 alpha/(16 pi M)) int dQ^2 S_1, matching FSP-006 and WLCM eq. (13).

The overall factor 2 in T^B is not assumed. It follows from requiring that a point Dirac particle (F_1=1, F_2=0) carry the textbook leading logarithm 3/(16 pi^2) log(Lambda^2/m^2) per e^2. Its angular integrand is 2(1+2x^2)/(z^2+x^2). At large z this integrates to 3 pi/(2z^2), so M_u/m tends to (3/(8 pi^2)) int dz/z = (3/(16 pi^2)) log(Lambda^2/(4m^2)). The finite constant is then an output, checked in R4.

## R1. Charge weights by explicit enumeration (symbolic charges)

Every ordered placement of two flavour-diagonal currents was enumerated. A current sits either on one of the three valence lines (uud for p, udd for n) or on a sea loop of flavour u, d, s or c. Loops are labelled A and B to separate the same-loop and separate-loop classes. The charge product was summed per isospin-invariant class, with the charges left symbolic in sympy.

Results, symbolic and at physical charges, in per-placement normalisation:

| class | p | n | p-n (factored) | p, n, p-n, (p+n)/2 at physical charges |
|---|---|---|---|---|
| X_maj | 2Q_u^2 | 2Q_d^2 | 2(Q_u-Q_d)(Q_u+Q_d) | 8/9, 2/9, 2/3, 5/9 |
| X_min | Q_d^2 | Q_u^2 | -(Q_u-Q_d)(Q_u+Q_d) | 1/9, 4/9, -1/3, 5/18 |
| Y_majmaj | 2Q_u^2 | 2Q_d^2 | 2(Q_u-Q_d)(Q_u+Q_d) | 8/9, 2/9, 2/3, 5/9 |
| Y_majmin | 4Q_uQ_d | 4Q_uQ_d | 0 | -8/9, -8/9, 0, -8/9 |
| Z_maj_l | 4Q_u(Q_u+Q_d) | 4Q_d(Q_u+Q_d) | 4(Q_u-Q_d)(Q_u+Q_d) | 8/9, -4/9, 4/3, 2/9 |
| Z_min_l | 2Q_d(Q_u+Q_d) | 2Q_u(Q_u+Q_d) | -2(Q_u-Q_d)(Q_u+Q_d) | -2/9, 4/9, -2/3, 1/9 |
| Z_maj_s, Z_min_s | 4Q_uQ_s, 2Q_dQ_s | 4Q_dQ_s, 2Q_uQ_s | +/-(Q_u-Q_d)Q_s x(4,2) | -8/9,4/9,-4/3,-2/9; 2/9,-4/9,2/3,-1/9 |
| Z_maj_c, Z_min_c | 4Q_uQ_c, 2Q_dQ_c | 4Q_dQ_c, 2Q_uQ_c | +/-(Q_u-Q_d)Q_c x(4,2) | 16/9,-8/9,8/3,4/9; -4/9,8/9,-4/3,2/9 |
| W_l, W_s, W_c | Q_u^2+Q_d^2, Q_s^2, Q_c^2 | same | 0 identically | 5/9, 1/9, 4/9 |
| V (all six pairs) | products of one-loop charge sums | same | 0 identically | as in DERIVATION |

The tests hold as polynomial identities:

* The same-loop and two-loop sea weights cancel in p-n identically, for any charges.
* Every p-n weight is divisible by (Q_u - Q_d).
* Every isoscalar weight is symmetric under Q_u <-> Q_d.
* Y_majmin cancels in p-n.

## R2. Isospin route (different basis)

Write J = alpha0 S + beta1 V3 + Q_s O_s + Q_c O_c. Parametrise the nucleon matrix elements by reduced amplitudes:

* isoscalar: a for <SS>, c for <V3V3>, e_g for <{S,O_g}> and g_gh for <O_g O_h>;
* isovector: b tau_3 for <{S,V3}> and f_g tau_3 for <{V3,O_g}>.

The rank-2 part of V3V3 vanishes between I=1/2 states. Then

    p - n     = (Q_u - Q_d)[(Q_u+Q_d) b + 2 Q_s f_s + 2 Q_c f_c]/2,
    (p + n)/2 = (Q_u+Q_d)^2 a/4 + (Q_u-Q_d)^2 c/4 + (Q_u+Q_d)(Q_s e_s + Q_c e_c)/2
                + Q_s^2 g_ss + Q_c^2 g_cc + Q_s Q_c g_sc.

The isovector combination contains {b, f_s, f_c}, and the isoscalar contains {a, c, e_s, e_c, g_ss, g_cc, g_sc}. The intersection is empty. The isoscalar is therefore not a function of any isovector data, independently of the contraction-class bookkeeping in R1.

## R3. Colour algebra for the heavy-flavour reduction

Gell-Mann generators were built numerically:

* max |Tr[T^a,T^b]| = 0, and Tr(T^a T^b) = delta^ab/2 to 1e-16.
* sum d_abc^2 = 13.3333, equal to (N^2-4)(N^2-1)/N = 40/3.

Furry's theorem gives the two orientations of a quark loop with three vector vertices opposite signs. The photon plus two gluons coupling is therefore proportional to Tr(T^aT^b) - Tr(T^bT^a) = 0, while the photon plus three gluons d^abc coupling survives. This confirms the ingredient behind DERIVATION section 4. It does not compute the size of the surviving power corrections.

## R4. Born numbers by full two-dimensional integration

The integral is

    M_u/M = (1/4 pi^3) int z dz int_{-1}^{1} dx sqrt(1-x^2) [-3T_1^B + (1-x^2)T_2^B]

with the BBBA05 form factors, evaluated without the 1-D kernel:

| | MeV per e^2 |
|---|---:|
| proton, full Born | 6.071304630462451 |
| proton, pole only (non-pole -2F_1^2 dropped) | 3.0239166208168373 |
| neutron, full Born | -2.336607866236512 |
| neutron, pole only | -2.3825014270810696 |

The point-Dirac constant from the same code is 1.500003999997 at Lambda/m = 10^3 and 1.500000040350 at 10^4. Its approach to 3/2 goes as 4m^2/Lambda^2.

## R5. Path dependence

Symbolically:

* A universal O(u) scale shift, A -> A(1+3cu) and M -> M(1+cu), leaves R_u unchanged.
* A quark-mass path change, A_u -> A_u + k a_m and M_u -> M_u + k sigma, shifts R_u by k(a_m/M^3 - 3A sigma/M^4), that is k m dR/dm.

This agrees with FSP-010 COMMON_UV_RATIO eq. (2), read in its undivided form.

## Comparison with the author's verdict

The author output was opened only after R0-R5 had been produced.

| item | re-derivation | author | status |
|---|---|---|---|
| Charge weights, 19 classes | per-placement normalisation | one total amplitude per class | agree class by class. The ratio of the two normalisations is the class multiplicity (2, 1, 2, 4 for X_maj, X_min, Y_majmaj, Y_majmin; 4/2 for Z_maj/Z_min; 1 for W, V), identical for p and n. |
| Classes invisible to p-n | W, V, Y_majmin | W, V, Y_majmin | agree |
| Isoscalar not determined by isovector | yes (R1 and R2) | yes (eq. (3)) | agree |
| Born_p, Born_n (BBBA05) | 2-D quadrature | 1-D kernel B(z) | relative differences 1.0e-14, 1.4e-14 (pole only 1.8e-14) |
| Point-Dirac constant | 3/2 | 3/2 | agree |
| Scale shift cancels in R_u; mass shift does not | yes | yes | agree |

**Diagnostic history.** The first comparison draft reported V_lc and V_sc as "absent". The enumeration names two-loop classes by their flavours in sorted order (V_cl, V_cs). Only the comparison's label normalisation was changed; no physics or weight changed. Recorded in [run_001/manifest.json](run_001/manifest.json).

**Prior programme statement.** FSP-006 gave the same-loop sea coefficient for degenerate u,d,s as 0 in p-n, 4/3 in p+n and 2/3 in the proton. R1 gives W_l + W_s = 5/9 + 1/9 = 2/3 in the proton and in (p+n)/2, and 0 in p-n. These agree.

**Restrictions added by the review.** The reviewer accepts the author's critical step (DERIVATION section 3) and the normalisation and assembly arithmetic (section 5). Three points are restricted:

1. The heavy-flavour section 4 rests on Furry's theorem plus decoupling. Its "dimension six or more" power corrections are orders, not computed bounds.
2. The statement that the scale direction "cancels in R" requires A, A_u and the vacuum's own charm and threshold response on the same path. None of these has been computed.
3. The Mueller-Meissner equation is quoted through a web rendering. Only its structural content (f_2 alone in p-n) is used, and that content is re-derived here (the f_3 monomial is pion independent).
