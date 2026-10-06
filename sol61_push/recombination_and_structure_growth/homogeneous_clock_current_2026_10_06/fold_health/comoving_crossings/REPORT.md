# A fixed comoving clock mode can cross a finite intermediate kinetic band twice

Every fixed nonzero comoving mode on the tuned dust history is positive in the early asymptotic limit and on the late branch. Sufficiently low comoving wave numbers nevertheless encounter an intermediate interval where the reduced unitary-curvature kinetic coefficient is negative, bounded by at least two zero crossings. This corrects interpreting the instantaneous early-branch physical-wave-number band as negativity throughout the history of any fixed mode. The sign and crossings remain coefficient statements, not a physical singularity or invariant ghost diagnosis.

## Exact background and comoving normalization

Use only the parent four-dimensional positive-charge tuned dust branch, eta in(0,1), kappa>0. Let z=rho_d/(2c)=D a_FRW^-3, h=H/H*, and t=(h-1)/eta. To avoid confusing this dimensionless branch coordinate with physical time, all derivatives tprime below mean dt/dz. The parent relation is

    L(t)+(eta/2)(t-1)²=L(z), L(x)=x-ln x-1.

For z>1 use the unique upper t>1 branch; for z<1 use the lower0<t<1 branch. Each is strictly monotone and the tuned signed-fold continuation joins them. Let a_fold=D^(1/3), so a_FRW/a_fold=z^-1/3. Define kbar=p(z=1)/H*>0. A fixed comoving mode then has

    p/H*=kbar z^(1/3),
    Kclock/M=[kappa kbar² z^(2/3)-3eta²(t-1)]/(1+eta t-eta)².

The denominator stays positive. On the early t>1 branch define

    S(z)=3eta²(t(z)-1)/(kappa z^(2/3)).

Negative coefficient is exactly kbar²<S(z), not a test at fixed physical p. A fixed physical p would compare different comoving modes as the universe expands.

## Endpoint proof and guaranteed crossings

At z->1+, the signed-fold slope is t-1=(z-1)/sqrt(1+eta)+O((z-1)²). Hence

    S(z)=[3eta²/(kappa sqrt(1+eta))](z-1)+O((z-1)²) ->0.

For z->infinity, the exact implicit relation gives t~sqrt(2z/eta), so

    S(z)~[3sqrt(2)eta^(3/2)/kappa] z^-1/6 ->0.

To justify the latter rather than insert an assumed GR law: for fixed eta>0 the eta t²/2 term dominates L(t)+eta(t-1)²/2 as t->infinity, while L(z)/z->1. Monotonicity forces t->infinity with z, giving the asymptotic ratio.

For every fixed kbar>0, the same relation gives

    Kclock/M~[kappa kbar²/(2eta)]z^-1/3>0

as z->infinity. The negative bare contribution is only order z^-1/2. This coefficient tends to zero from above; no inference of a controlled strong-coupling scale is drawn from the sign limit. On the lower t<1 branch both numerator terms are positive. As z->0, t~exp(eta/2)z, and

    Kclock/M ->3eta²/(1-eta)²>0.

S is continuous, positive on1<z<infinity and tends to zero at both ends, so it attains a positive finite maximum. If0<kbar²<S(z0) at any selected finite z0, continuity and both endpoint limits guarantee at least one crossing on each side of z0, with a negative open interval between some crossing pair. This does not prove uniqueness of the maximum or exhaustively count crossing pairs. At exactly the maximum value a tangency rather than a sign interval is possible; higher kbar² exceed the band if they exceed the true maximum.

## Exact stationary equation and a rigorous finite upper bound

Differentiating the actual branch gives

    tprime=t(z-1)/[z(t-1)(1+eta t)].

Consequently

    Sprime=eta²[3t(z-1)-2(t-1)²(1+eta t)]
            /[kappa z^(5/3)(t-1)(1+eta t)].

Every interior stationary point therefore obeys

    3t(z-1)=2(t-1)²(1+eta t).

This equation was used with declared brackets; no unproved unimodality was substituted for it.

A universal bound also gives a finite sufficient no-crossing criterion. Put a_branch=t-1>0. Since L is increasing on x>1 and eta>0, z>t=1+a_branch. Also L(z)<z and L(t)>0 imply z>eta a_branch²/2. Thus

    S<(3eta²/kappa)a_branch/[max(1+a_branch,eta a_branch²/2)]^(2/3).

The first bound piece a_branch/(1+a_branch)^(2/3) is strictly increasing; the second is (2/eta)^(2/3)a_branch^-1/3, strictly decreasing. Their crossover is

    a_b=(1+sqrt(1+2eta))/eta.

Hence, for every z>1,

    S(z)<U=(3eta²/kappa)a_b/(1+a_b)^(2/3).

Any kbar²>=U has no negative intermediate band. This finite sufficient bound is not the exact maximum. For eta=.5,kappa=.99, U≈1.1294426131.

## Bounded actual local peak and two crossings

At eta=.5,kappa=.99,70-digit evaluation of the authentic upper branch uses

    z(t)=-W_-1[-exp(-t+ln t-(eta/2)(t-1)²)].

This is simply the inverse of z-ln z=t-ln t+eta(t-1)²/2. The branch -1 and t>1 are essential. The implementation also checks the original implicit equation at all reported roots. An initial unconstrained exploratory root search wandered outside t>1 and was discarded; the authoritative run uses domain-preserving bracketed bisection only.

Bisection of the stationary equation on5<t<10 locates

    t_peak≈7.73025382071334,
    z_peak≈20.0051826164714,
    S_peak≈.691877432735952,
    sqrt(S_peak)≈.831791700328846.

Derivative signs at the declared neighboring points corroborate a local maximum. This numerical result is not a proof that this is the unique/global maximum. The global existence and U bound above are analytical and independent of that issue.

Choose kbar²=S_peak/2, kbar≈.588165551837215. Bracketed roots on1.1<t<t_peak and t_peak<t<1000 give two distinct coefficient zeros:

| z | t | a_FRW/a_fold | p/H at crossing |
|---:|---:|---:|---:|
| 6539.89627563 | 160.693414799 | .053474046152 | .135212411727 |
| 2.01351936563 | 1.72813231890 | .791920155205 | .398434435514 |

The table follows expanding-universe time: z decreases as a_FRW increases. The mode begins positive in the asymptotic early regime, crosses into the negative coefficient region at the first tabulated point, and crosses out at the second. The bracketed computations establish these roots and a negative intermediate sample. They are not an exhaustive classification of every possible additional crossing outside or inside the brackets. The selected peak's positive S alone already suffices for the analytical at-least-two argument.

Both crossings occur at sub-Hubble physical wave numbers, so a rapid temporal WKB growth interpretation is not warranted. The chosen roots delimit approximately2.695264155 e-folds in scale factor. The coefficient zeros do not supply an invariant physical ghost or evolution singularity theorem. They define the precise finite times/scales at which the full coupled canonical/mode analysis must be performed.

## Evidence and remaining implication

main_a16/16; fixed_physical_control_a rejects the fixed-comoving sign identity and its positive early asymptotic when the calculation incorrectly freezes physical p. Both standard manifests validate with unchanged parent mathematical inputs. Exact symbolic checks corroborate the derivative/asymptotic coefficients and bound pieces;70-digit mpmath uses240 bisection iterations,73 bounded corroborating samples and821 branch evaluations, below the10k cap. Runner caps wall45s,CPU30s,1MiB logs,one cooperative thread. No computation claims uniqueness from sampling.

The parent fold_health calculation remains valid as an instantaneous coupled-coefficient result, and the tuned homogeneous background remains on shell. The next missing implication is regular nonadiabatic scalar/dust evolution through these actual fixed-comoving zero crossings, with a gauge-invariant physical transfer matrix or a demonstrated obstruction in a nonsingular canonical chart. The present analysis supplies a finite target interval for that question and leaves A/H untouched.
