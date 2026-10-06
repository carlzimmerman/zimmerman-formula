# Independent review: fully varied transition completion

Reviewed 2026-10-05 by the reciprocal-cold lane. Read-only review of the main
lane; this file is written only in the reviewer-owned directory. Verdict:
the reported local action, Schur reduction, uniform endpoint bound and
positive-gradient cutoff are correct with the report's stated hypotheses.
No concrete algebraic error was found. This is a local conditional result,
not a global halo/formation or cosmological completion.

Exact reviewed source SHA256:

- REPORT.md: `abff9f8f71071d759e0bda0e44bca3d5839a5b365638f3e0e95a2e4d88729ff5`
- checks.py: `4b052ef2aa69073a4a9f8f3262b8acfbe6c8d1e6a59043e27d98af6b39ba7b6e`

Both paths are below
`sol61_push/main_theory/new_doors_2026_10_05/constrained_transition/`.
I reconstructed the equations and numerical witnesses independently; I did
not import or execute the peer script or write to its directory. Check
counts are not used as a proof.

## Action and physical reduction

The minus-U and minus-mnPhi terms yield div(U_g)=mn. For the displayed U,
U_g=[(1-f)+f|g|/a0]g/(4piG), so the sourced equation and the longitudinal and
transverse Hessians have the reported signs. With constant background q and
velocity, the quadratic kinetic terms have no advective cross term: density
inertia is m/(n k^2), q inertia is nI. Both are positive at nonzero k. Varying
Phi gives the positive static coefficient a_field k^2. Eliminating its
constraint subtracts C C†/(a_field k^2), hence cannot improve a negative
frozen direction after normalization by that same positive kinetic matrix.
The complex nq entry is E_nq+i m h/(a_field k), up to Fourier convention;
its modulus squares to E_nq^2+m^2h^2/(a_field^2 k^2). This verifies both
extra terms in the reported characteristic polynomial.

A constant density and constant nonzero field do not solve the globally
sourced equation. The report correctly calls this a WKB/Jeans patch or an
externally supported, mean-subtracted perturbation construction. Its formal
k-to-zero endpoint cannot be transferred to an isolated halo without a
background and boundary calculation. The q stationary equation is likewise
local: it is not a solved global sourced moving transition.

## Exact uniform bound, including endpoint attainment

Write alpha=n E_nn/m>0, beta=(E_qq-h^2/a)/(nI)>0, J=nm/a>0,
L=E_nq^2/(mI)>=0 and M=mh^2/(a^2I)>=0. The normalized Hermitian matrix has
diagonal alpha k^2-J and beta, with off-diagonal modulus squared L k^2+M.
Its upper eigenvalue is at least beta, thus strictly positive. At w=-s,

    P(-s)=k^2[alpha(beta+s)-L]+(s-J)(beta+s)-M.

Define s_inf=L/alpha-beta and the nonnegative root
s_0=(J-beta+sqrt((J+beta)^2+4M))/2. If s>=max(s_inf,s_0), the coefficient
of k^2 is nonnegative and the remaining quadratic is nonnegative, because
its other root is <=0. Since w_+>0, P(-s)>=0 is exactly the condition
w_->=-s. This proves the upper bound on every k, without a grid argument.
As k approaches zero, the negative eigenvalue tends to -s_0. As k approaches
infinity, w_- tends to beta-L/alpha=-s_inf. The larger endpoint is therefore
approached on the positive-k domain, establishing the exact supremum. A
maximum at a finite physical halo wavelength is not implied. If beta<=0 or
E_nn<=0, this proof must be changed; the report explicitly assumes the
positive cases for this statement.

Independent brent-root/background reconstruction gives q=.5004333326823726,
E_nn=527.1812502441103, E_nq=-281.20666673176277,
E_qq=150.00045066565116, a_parallel=1.3990250019528818 and
h=-.5999990986697131. With I=.01, s_inf=17.12494575819619 and
s_0=1.0740175105011076, giving sup gamma=4.13822978557211. With I=1,
s_inf=.17124945758197896 and s_0=1.073998097909893, giving
sup gamma=1.036338794945887. These independently reproduce the claimed
endpoint behavior and bounded rate, subject to the local background premise.

## Gradient repair and warm response cost

Adding positive kappa|grad q|^2/2 to static energy changes E_qq to
E_qq+kappa k^2 before elimination. Direct determinant expansion yields

    kappa E_nn y^2
    +[E_nn(E_qq-h^2/a)-E_nq^2-m^2 kappa/a]y
    -m^2 E_qq/a,              y=k^2.

The h terms in the constant coefficient cancel against the constitutive
source-mixing square; replacing that constant by a frozen-gravity expression
would be wrong. For E_nn,E_qq,kappa positive, the two y roots have opposite
signs. The determinant is negative below the positive cutoff and positive
above it. At and above that cutoff the upper root is positive, since the
cutoff cannot lie below alpha y=J (at that point the determinant is
nonpositive). The leading speed squares n E_nn/m and kappa/(nI) are positive;
this is a principal local result, not nonlinear global strong hyperbolicity.

Independent positive roots give k_cut=50.69057824416539, 5.143683281891853
and .7734404152753025 for kappa=.0001,.01,1. The finite grid formation maxima
remain grid estimates, exactly as the report says.

The warm-response cost has a direct interpretation beyond its numerical
comparison. In the fast-I limit with m=1, the followed fluid eigenvalue tends
at fixed k to

    w_fluid=n E_nn k^2-J
       -n[E_nq^2 k^2+h^2/a^2]/[E_qq+kappa k^2-h^2/a].

A growing positive gradient suppresses q's density relaxation, exposing the
large frozen reader stiffness E_nn rather than preserving the ordinary gas
stiffness. Thus high-k warm gas becomes much stiffer even though the cold
short-wave instability is removed. In the stated e''=20,I=1e-8 midpoint,
independent signed fractional fluid shifts at k=1,10 are:

| kappa | k=1 | k=10 |
|---|---:|---:|
| .0001 | -.0469385857 | -.0434777364 |
| .01 | -.0451283306 | +.1299805653 |
| 1 | +.1346964116 | +10.5310883034 |

The report's absolute maxima are correct. The sign makes the large-gradient
cost concrete: kappa=1 increases the k=10 gas frequency squared by more than
a factor of eleven relative to the stated baseline. These controls have an
unambiguous fast-response fluid branch; they are not astrophysical temperature
or wavelength constraints. No dimensionful parameter selection follows.

## Remaining implication

The construction establishes that a positive spatial internal-state term can
turn a finite-rate local spinodal instability into a finite unstable band,
with an explicit pressure response price. It does not select its width,
parameters, saturation, cold abundance or desired halo, and does not preserve
the adopted P2/QUMOND kernel by inheritance. A conserved global background
and moving edge under this same action are the next missing implication.
No result here licenses splicing this q action into the reciprocal cold
flux action without varying the combined sources and reactions again.
