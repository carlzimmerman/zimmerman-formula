# Conserved-fluid interior: a regular-center density bound before shooting

No regular weakly normalized high-density source interior is obtained for the stated logKGB+critical fixed-A response. The decisive obstruction is an exact leading center constraint, not a failed integration. It survives UV turn-off modifications that preserve the small-gradient quadratic response. A regular weak-source mass integral is also derived, closing the leading mass-normalization implication conditionally; a full exact source/global connection remains unbuilt.

The same action is the source_asymptotics logKGB action with Einstein coefficient M>0, H>0, eta=c/(3MH²) in(0,1), selected fixed vacuum U(N)=-3MH²+2c lnN, and response M Q(a), Q=a²-2W(a;A), A>0. For P2, W_a=sqrt(a²+A²/4)-A/2, so Q=a²-2a³/(3A)+O(a^5). The low-gradient limit is fixed; modifying only high acceleration does not change the proposition. Matter is a static Killing-frame perfect fluid, with proper rest-frame density rho(r), pressure p(r). The target toy interior has constant rho0>0,p0>=0. The local proposition needs only smooth rho=rho0+O(r²),p=p0+O(r²).

## Exact physical fluid sources, including momentum

Use ds²=-N²dt²+B²(dr+Vdt)²+r²dOmega², F=N²-B²V²>0, and u^mu=(1/sqrtF,0,0,0). Direct Hilbert variation of T=(rho+p)u u+p g gives matter Euler contributions perunit solidangle

    E_Nmatter=-Br² epsilon,
    E_Bmatter=Nr² Srad,
    E_Vmatter=NB³r²(rho+p)V/F,
    epsilon=(rho+p)N²/F-p,
    Srad=p+(rho+p)B²V²/F.

Thus E_Ngravity=Br²epsilon and E_Bgravity=-Nr²Srad. The exact momentum equation is

    V[Bprime/B+Nprime/N-N²B²r(rho+p)/(2MF)]+eta H r Nprime=0.

A diagonal-static fluid is not zero ADM momentum when V is nonzero. Its conservation equation is

    pprime=-(rho+p)Fprime/(2F).

This uses the physical metric redshift, not the clock lapse acceleration. The earlier exact Noether current identity remains valid with sources: inserting these three matter contributions makes their weighted combination vanish identically. Hence the exact static interior metric equations imply j_total^r=0; no freely adjustable scalar charge is introduced.

## Proposition: necessary regular center data

Assume finite positive N0, Euclidean regular spatial center, finite clock expansion and enough differentiability to have

    N=N0[1+n2 r²+o(r²)], B=1+b2 r²+o(r²),
    V=N0 x r+o(r), rho=rho0+o(1), p=p0+o(1),

with remainders controlled under the derivatives in the Euler equations. Define R=rho0/M,P=p0/M and u0=-3H²+6etaH² lnN0. The response's signed derivative is Q_signedprime=2Nprime/(NB)+o(r); this leading term is independent of the sign of n2. Neither positive clock acceleration nor static dust is assumed.

The exact action's order-r² B,N equations respectively give

    2b2-4n2+3x²+u0=-P,
    6b2-12n2+3x²+6etaHx+u0+6etaH²=R.

The -12n2 term is -(r²Q_signedprime)prime/r². The Q-aQ_a terms in B,N enter at higher order. Eliminating b2 cancels n2 and yields

    x²-etaHx-(1+eta)H²+2etaH²lnN0+(R+3P)/6=0.

Therefore a necessary real-center condition is

    Delta=(eta+2)²H²-8etaH²lnN0-(2/3)(R+3P)>=0,
    rho0+3p0 <= (3M/2)[(eta+2)²H²-8etaH²lnN0].

The full momentum equation adds

    (3x+etaH)n2=(3/2)etaH x(x+H),
    b2=2n2-(3/2)x²-u0/2-P/2.

Thus a real quadratic root is necessary, not sufficient. At x=-etaH/3 the trace constraint is inconsistent for0<eta<1; that denominator cannot be ignored. The cosmic vacuum branch N0=1,R=P=0 has x=-H,n2=b2=0. The alternate quadratic root x=(1+eta)H is different center data, not the selected cosmological branch.

Physical inward force near the center depends on

    F=N0²[1+f2 r²+o(r²)], f2=2n2-x²,
    p=p0-(rho0+p0)f2 r²/2+o(r²).

Consequently n2>0 alone does not imply inward physical gravity. These coefficients and the pressure equation constrain any proposed inward-source branch.

## Weak lapse, source normalization and the exterior continuation

With the selected outer clock/lapse normalization N->1, a weak central gravitational redshift means |lnN0|<<1 because V(0)=0 and F(0)=N0². An overall clock/time rescaling cannot remove this relative lapse while leaving the selected U(N) and cosmological normalization fixed. At eta=.5,N0=1 the bound is rho0+3p0<=9.375MH². A galaxy-like rho0/(MH²)>>1 therefore has no such regular weak center. Allowing an exponentially small N0 is a strong-redshift changed premise, not a regular weak galaxy construction.

The leading weak fluid Euler equations give a useful mass identity, with S=V²-H²r², a approximately Nprime, v=V+Hr and g=a-Sprime/2:

    b+S/2=rg-p r²/(2M),
    [r²(g-a+W_a+etaHv)-p r³/(2M)]prime=rho r²/(2M).

Regular center data set its integration constant to zero. At a p=0 fluid surface Rstar, a constant-density weak source yields

    m= rho0 Rstar³/(6M)=G_N,b M_baryon,
    G_N,b=1/(8piM), M_baryon=4pi rho0 Rstar³/3,

up to the stated higher weak-potential/volume corrections. This is derived from the sourced equations; it is not an independent imposed scalar charge or exact global mass theorem.

Combining this leading identification with the center cap gives r_cos/Rstar=(rho0/(6MH²))^(1/3) of order one (at most about1.16 at eta=.5,N0=1,p0>=0). There is no parametrically controlled exterior interval Rstar<<r<<r_cos required by the formal MOND mass-flux balance for this weak constant-density source. This excludes the desired controlled setup before choosing an integration algorithm; it does not forbid every finite, nonhierarchical exact exterior.

For the inspected finite exterior continuation's m=1e-12,H=1,r_start=1e-5, a constant-density source confined below r_start and identified with that baryonic m needs rho0/M>=6000, over640 times the regular weak-center cap. The corresponding necessary lnN0 is at most-998.4375 at eta=.5,p0=0. This is a mathematical unit control, not a new astronomical fit. The finite exterior success itself remains accepted as an exterior-only result; its exact inner mass/boundary identification is not assumed already proved.

## Nonanalytic central escape and regularity price

Natural NR MOND inside a uniform positive source has a~sqrt(r), N-N0~r^(3/2). It is C1 but not C2 at the center. With bounded regular unit-clock expansion V=O(r), V²=O(r²) cannot cancel that leading term in the physical F=N²-B²V². The physical tangential curvature contains Fprime/(2N²B²r), which diverges as r^(-1/2) for a regular Euclidean center. Radial curvature also diverges; the squared curvature is locally integrable but unbounded. Finite mass/action integrals are not finite curvature.

Trying V~r^(3/4) to cancel an r^(3/2) contribution to F instead gives theta=-(Br²V)prime/(NBr²)~r^(-1/4), an unbounded invariant clock derivative. A stronger exact momentum argument also rejects canceling this cusp while retaining a regular physical static metric and finite fluid source. Write J=NB and D=J²/F, so regular F=F0+O(r²),D=1+O(r²) imply Jprime/J=O(r). For N=N0(1+alpha r^p+...),1<p<2, cancellation in F forces V=O(r^(p/2)) with nonzero leading coefficient (alpha must be positive). The exact momentum equation is

    2M V Jprime/J+2M etaH rNprime=rVD(rho+p).

Its braiding term has nonzero order r^p; both other terms are at most order r^(1+p/2), which is strictly higher. Finite rho+p therefore cannot satisfy it for alpha!=0. This directly rejects the proposed cancellation, without relying only on an assumed bounded clock expansion. It was independently derived by main_theory and reconstructed here. A singular physical metric, divergent matter, different leading powers or a changed braid/source coupling changes the premises.

A singular B or non-Euclidean center likewise changes the proposition's premises. These weak/integrable or singular-clock possibilities are retained as changed-regularity escapes, not universally excluded. One must solve their field equations, distributional/source interpretation and matching before calling them regular.

Even ordinary integer leading coefficients may need nonanalytic higher terms because Q contains |a|³; this proposition uses only the controlled leading r² order and does not silently demand a complete analytic Taylor series. It rules out the high-density bounded-metric/bounded-clock regular center, not every weak solution of the action.

## Evidence and first missing implication

checks.py constructs the static-fluid Hilbert sources from the metric inverse, verifies exact source-current cancellation, derives center coefficients directly from the stationary action, and checks the discriminant/trace constraint, critical-response scaling, weak mass integral and cusp. Fresh bounded runs/controls preserve all inputs. The peer main_theory agent and root independently reconstructed the raw center equations and source signs. Their agreement is supplementary review, not a proof certificate.

No high-density interior shooting was performed: the necessary real-center condition and controlled exterior hierarchy fail in the intended weak source regime. Low-density/strong-redshift or singular-regularity branches remain open and are not promoted to a matched galaxy. The next genuine completion must alter the low-gradient quadratic criticality, relax and audit physical center regularity, or supply a different action/clock coupling while retaining conserved matter and measured force. A UV cutoff alone does not address this infrared center constraint.

Authoritative runs: main_b12/12; drop_momentum_b10/12, rejecting source Noether cancellation and exact center momentum after actual fluid shift-source deletion. Both V2 manifests validate with unchanged actual inputs and retained logs. Caps wall45s,CPU30s/process,1MiB logs,one cooperative thread; no memory/affinity cap. The a-runs preserve a caught script-only extraction error: full shift Euler starts r³ while its stripped constraint starts r². Their original source and contract are archived in historical_a/; they are historical, not current-code validation. Analytical equations above were unchanged.
