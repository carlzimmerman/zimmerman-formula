# Independent source-first non-Born contraction

Saved 2026-10-19 before opening nonborn_proton/DERIVATION.md, its code,
inputs or result. Scope: a fixed-positive-pion-mass soft photon ball in the
standard on-shell Born convention, not the full proton mass or curved vacuum.

Independence limitation: a broad normalization search inadvertently displayed
common_response/RAW_DERIVATION.md lines 146–166, including its claimed
3(a-b)/(32 pi) factor. Its proof and code were not read. Accordingly the
common-response factor check is an independently reconstructed check with
prior answer exposure, not a blind audit. No nonborn_proton author derivation
or implementation has been read.

## Primary source and state normalization

AHLP, arXiv:2005.09518v2, source Pol-draftvfinal.tex, Eq.(1), (6), (7),
uses the two tensors (-g+qq/q²) and p_perp p_perp/M². In this basis its
Born amplitudes are T1=-u F1²/M+u nu_el² GM²/[M(nu_el²-nu²)] and
T2=2u nu_el A/(nu_el²-nu²). WLCM's relativistically normalized,
charge-stripped amplitudes are t_i=2M T_i/u: with nu=iQx and z=Q/(2M)
this gives t1=2[z² GM²/(z²+x²)-F1²], t2=2A/(z²+x²).
Both amplitudes, including the non-pole Dirac term, fix this mapping.
It is also the mapping of Nevado–Pineda arXiv:0712.1294v2 Eq.(2.4)
current tensor and Eq.(2.6) Born amplitudes to AHLP's reduced tensor.

The exact source archives were retrieved independently from
https://arxiv.org/src/2005.09518v2 and https://arxiv.org/src/0712.1294v2.
The first archive matches the author's stored archive byte for byte
(SHA256 c1de1fb8ec31c1cd7bc16e4c7366e2d49213102de3e183ed45cae51465eff8dd).
Final receipts will pin both archives and extracted members. An initial
unprivileged curl failed DNS resolution; the public retrieval then succeeded
through the authorized network path. The web PDF reader returned cache misses.

## Effective action and the complete SO(4) contraction

The rest-frame polarizability action is L_pol=2 pi N†N
(alpha_E E²+beta_M B²), where the physical polarizabilities include u.
Its second source derivative gives a transverse two-current tensor. For a
transverse real photon it yields 4 pi(alpha_E+beta_M)nu²; for a static
transverse magnetic source it yields 4 pi beta_M Q². Transversality fixes
the remaining longitudinal response. Equivalently, in AHLP's tensor basis,

 T1_NB=4 pi[beta_M Q²+(alpha_E+beta_M)nu²]+O(q4),
 T2_NB=4 pi(alpha_E+beta_M)Q²+O(q4).

Write a=alpha_E/u and b=beta_M/u, holding strong parameters fixed at u=0.
Then t1_NB=8 pi M Q²[b-(a+b)x²] and
t2_NB=8 pi M Q²(a+b). The full trace kernel is

 -3t1+(1-x²)t2=8 pi M Q²[(a-2b)+2(a+b)x²]+O(Q4).

Since integral_-1^1 sqrt(1-x²) dx=pi/2 and its x² moment is pi/8,
the integrated kernel is 6 pi² M Q²(a-b)+O(Q4). Inserting it into
the inherited WLCM response gives

 M_u^NB(0<Q<Lambda)/M = 3 Lambda4(a-b)/(32 pi M)+O(Lambda6),
 M_u^NB(0<Q<epsilon M)/M =
       [3 M³(a-b)/(32 pi)] epsilon4+O(epsilon6).

The static subtraction alone would give -3 b Lambda4/(16 pi);
it misses the electric contribution and a magnetic compensation. The
Baldin sum alone likewise does not determine this contraction. All stated
remainders assume the analytic gapped tensor near q=0 at fixed m_pi>0.

## Unfitted pi-N infrared benchmark and nonsinglet logs

The leading HB pi-N loop polarizabilities are
a=5g_A²/(384 pi² F_pi² m_pi), b=g_A²/(768 pi² F_pi² m_pi).
Thus a=10b and a-b=3g_A²/(256 pi² F_pi² m_pi), yielding

 C_NB=lim_Lambda->0 M_u^NB/Lambda4
     =9g_A²/(8192 pi³ F_pi² m_pi).

This is a pi-N sector expression in independently supplied strong inputs.
It is not a full physical polarizability or a solved numerical alpha.
At fixed positive m_pi take Lambda->0 first. Taking m_pi->0 first
invalidates the Taylor expansion and cannot justify a finite photon band.

BKSM hep-ph/9309211v1 Eq.(7), (8), (10), cross-checked in
hep-ph/9311354v1 Eq.(15), has C/u=1/(96 pi² F_pi²),
x_p=9, x_n=3, x'_p=3+kappa_s, x'_n=1-kappa_s.
The log coefficient of a_i-b_i is proportional to
(x_i-3x'_i)g_A²/M: -3 kappa_s for p, +3 kappa_s for n.
Both c2 logarithms cancel in a_i-b_i. In the Dirac pi-N sector with
kappa_s=0, these order-log terms vanish in each difference even though
the individual electric and magnetic polarizabilities carry logs.
For p-n the surviving order-log term is
-6 kappa_s g_A² log(m_pi/lambda)/(96 pi³ F_pi² M).
An anomalous-moment insertion and higher-order contacts must be separately
declared; the source's phenomenological fitted contacts are excluded.

## Exact flavor comparison has a different target

With m_u=m_d and a flavor-exchange-invariant regulator, flavor relabeling
gives W(q_u,q_d)=W(q_d,q_u) for an unconditioned vacuum. In coordinates
q_s=(q_u+q_d)/2, q_v=(q_u-q_d)/2, the derivative at q_v=0 of a
flavor-odd variation is zero. In the one-baryon sector the same operation
maps proton to neutron, so it gives P(q_s,q_v)=N(q_s,-q_v) rather than
forcing the individual proton derivative to vanish. A nonzero p-n
response is therefore compatible with the vacuum null. Neither identity
equates these sectors or their global metric responses.

The full all-Q non-Born tensor, its sea classes and independent subtraction,
finite matching, common calibration-path changes, and the unconditioned
curved QCD coefficient A_rho remain open. A soft photon-ball coefficient
cannot determine A_rho, R or alpha.
