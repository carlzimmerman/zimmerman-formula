# Absolutely normalized connected SU(3) vacuum on a closed S4 complex

FSP-010, checked 2026-10-19. The physical round-S4 coefficient A_rho(alpha), its common-path charge derivative and R=A_rho/M_p^3 remain open. This package calculates a genuinely interacting microscopic contribution to the full unconditioned partition function, beyond the previously inherited one-plaquette Haar sector. No measured alpha, cosmological input or geometry fit enters it.

The model is Wilson SU(3) on the cubical boundary K_n of [0,n]^5, with normalized Haar measure on every link and exponent +(beta/3) sum ReTr U_p. Thus Z_n(0)=1 exactly. All links are integrated without selecting a topological charge. The coarse regulator does not itself give a continuum decomposition into integer instanton sectors. Unit weights give the polyhedral SH[N] geometry, n=N-1, distinguished in the primary source from the projected weighted sphere. It has neither physical dynamical quarks nor a photon, and is not the round smooth sphere at fixed physical QCD parameters.

## Actual new coefficient and finite normalized value

On K_1 there are 80 plaquettes and 40 elementary three-cubes. Exhaustive enumeration of every connected support of at most nine distinct plaquettes gives exactly those forty cube boundaries. The search assigns every remaining incident plaquette, including zero assignments, at the selected dangling link; it allows links with three or more occupied faces. It also continues to connected supersets of closed supports. Consequently it does not assume coherent orientability or omit possible SU(3) baryon junctions in its support reduction.

For one coherently oriented cube surface, twelve exact SU(N) matrix integrals give eight free color-index loops and a value N^(8-12). At N=3 this is 1/81. Both orientations contribute, and proper subsets have a dangling link, so their cumulant products vanish. The exact square-free coefficient is

    [product_(six cube faces) beta_p] log Z = 2/(81*6^6) = 1/1889568.

This is a connected contribution involving six distinct plaquettes in the actual normalized non-Abelian measure. A product of separate one-plaquette integrals misses it.

Put c0(beta)=integral dU exp[(beta/6)(Tr U+Tr Udagger)] and

    v(beta)=(3 c0)^(-1) integral dU Tr(Udagger)
             exp[(beta/6)(Tr U+Tr Udagger)].

The use of v here avoids confusing the character coefficient with u=e^2 elsewhere in the programme. Each link of a cube has precisely two occupied plaquettes; irreducible orthogonality therefore forces a common representation around that surface. Fundamental and antifundamental characters start at beta; all other nontrivial SU(3) characters start at beta^2 or later. Since the support enumeration finds no other connected supports through size nine, the complete finite K_1 result is

    log Z_1 = 80 log c0(beta) + 720 v(beta)^6 + O(beta^10).

Here v=beta/18+beta^2/216+O(beta^4). In particular the collective terms through beta^9 are

    720 v^6 = (5/236196) beta^6 + (5/472392) beta^7
              + (25/11337408) beta^8 + (25/204073344) beta^9
              + O(beta^10).

The complete absolute log partition function is

    log Z_1 = (20/9) beta^2 + (10/81) beta^3
              -(5/5832) beta^5 -(95/1889568) beta^6
              +(49/3779136) beta^7 +(577/181398528) beta^8
              +(11/60466176) beta^9 + O(beta^10).

The leading collective coefficient is 5/236196, or 720/18^6. It is distinct from the local c0 term, whose beta^6 coefficient is negative. The color contraction, local moments and support reduction are checked by independent constructions.

There is also a rigorous finite value, without assuming a convergence theorem or exchanging limits. At the declared algorithmic benchmark beta=10^-6, let P9 be the exact rational Taylor polynomial of Z_1 through degree nine, stored in the result file. It obeys

    P9-1 = 2.2222223456814814... * 10^-12,
    |Z_1-P9| <= 2.959181355319713... * 10^-48,
    |log Z_1-log P9| <= 2.959181355319713... * 10^-48.

The bounds follow from |sum ReTr U_p/3|<=80, Taylor's theorem, exp(x)<=1/(1-x), x=80 beta, Z_1>=1 by Jensen and P9>=1. The bound is 1.397894*10^-7 of the leading collective beta^6 contribution. This is deliberately a tiny strong-coupling test point; it is no proposed physical coupling. The complete rational P9 and exact bounds are retained, so the printed decimal is not used as evidence.

## Radius information and its limits

Direct cell generation for n=1,2,3 verifies the exact counting argument

    Nk(n)=binom(5,k)n^k[(n+1)^(5-k)-(n-1)^(5-k)].

Thus N2=60n^4+20n^2 and N3=40n^4. For any n the contribution of the elementary-cube polymers at leading order is exactly 720 n^4(beta/18)^6. The explicitly calculated local and elementary-cube sectors have no n^3 term. The full K_1 series is complete through beta^9; the finite support enumeration does not prove general-n completeness. No uniform remainder in n or all-order coefficient is claimed.

At fixed cutoff spacing a, these calculated sectors have polyhedral volume 10(na)^4. Their smooth count-polynomial dilation stress through the leading cube term is

    rho = -6 log(c0)/a^4 -72(beta/18)^6/a^4
          -log(c0)/(a^4 n^2).

The displayed curvature/stratum term is proportional to (na)^-2. Its (na)^-1 coefficient vanishes in these sectors. This is not assigned the physical H of a round sphere, and is not a global mass-gap argument. The polyhedral curvature remains concentrated on strata; the fixed-cutoff strong-coupling regime and the smooth continuum physical regime are different limits. A matched radius trajectory would also need bare-parameter derivatives.

The actual d1 ranks, checked over F_1009 and F_1013 on n=1,2, agree with N1-N0+1: 49 and 559. Cubical boundary matrices obey boundary squared zero in all tested dimensions. This independently supports the topology/counting input to the separate coordinator sea-Hodge calculation; its photon and fermion action are not inputs to either frozen run here.

## Absolute integration constant and the physical continuation

For the specified microscopic regulator the exact integration anchor is

    log Z(beta)=integral_0^beta db sum_p <ReTr U_p/3>_b,

with logZ(0)=0. The calculated series supplies an actual nontrivial absolute starting value. This changes the missing normalization leaf: an unknown common geometry factor is not left free after the bare measure is specified. The usual Wilson offset +sum_p beta_p, if chosen, must be restored explicitly. It changes W by that declared local term, and is not silently identified with the displayed convention.

For a separately constructed curved fermion matrix M_f=1-kappa_f B_f, normalized by det M_f(0)=1, one can then integrate each flavor exactly:

    W(beta,{kappa_f})=W(beta,0)
      +sum_f integral_0^(kappa_f) dk
       <Tr[(1-k B_f)^(-1) B_f]>.

The other already integrated flavors remain in the expectation on each leg. All metric-dependent Grassmann Jacobians, gravitational terms and matching constants must be fixed in that same regulator. The flat Wilson source verifies the determinant convention; it does not construct a curved B_f. In particular its flat factor 16 kappa^4 is not imported into K_n.

The next physical step needs a round-sphere gauge and fermion regulator, an absolutely normalized reference measure, actual mass/gauge integration data on each sphere, local matching and a controlled common trajectory to physical quarks, followed by radius/continuum and mixed charge limits. The present calculation supplies none of those physical ensemble data. Its controlled pure-gauge coefficient and the separate declared sea-Hodge model cannot be substituted for them. No nonzero physical A or full physical zero, R, or alpha root is reported.

## Primary sources and verification

[Jersak, Lang and Neuhaus, hep-lat/9606013v1](https://arxiv.org/abs/hep-lat/9606013v1), section 2, equation (3) and the Appendix, supplies the exact cubical connectivity/counts and the distinction between unprojected SH[N] and weighted projected S[N]. It is a U(1) paper; no U(1) numerical observable is transferred to SU(3). [Langelage, Münster and Philipsen, 0710.0512v2](https://arxiv.org/abs/0710.0512v2), equations (2.1)-(2.4), (2.8), supplies Wilson/character/closed-surface conventions. Their thermal subtraction removes zero-temperature contributions; this calculation keeps the full absolute regulated logZ. [Wakabayashi et al., 2112.06340v2](https://arxiv.org/abs/2112.06340v2), equations (4)-(8), authenticates the determinant expansion convention, with the curved spinor bridge left open. Exact-version cache lookups preceded retrieval; PDF and extracted-text hashes and source-specific verdicts are in SOURCE_RECEIPTS.json. These are adjacent source applications, not a novelty claim or a worldwide search for absence.

Run closed-001 completed 2,015 exact checks in 0.186 seconds for the beta^6 calculation. The changed continuation closed-002 completed 2,052 checks in 0.456 seconds, including 45,076 support-search nodes through nine plaquettes, two independent singlet-multiplicity algorithms through tensor degree ten, direct index contractions, actual boundary ranks, chain identities and the rational endpoint bound. Both v2 manifests validate with unchanged input hashes. Bounds were 55 seconds wall, 45 seconds CPU, 64 KiB combined output and one conventional numerical thread. No address-space cap or installation was used. No failed execution occurred.

The outcome is **implementation and finite assertion verified in the stated range**. Independent constructions are inside the author program; a separate fresh physics/source review has not yet been performed by this worker. Mechanical v2 validation proves execution/freshness, not the physical continuum bridge. See REPRODUCE.md, SELF_AUDIT.md and the exact result/manifests.
