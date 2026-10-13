# Continuum moving-source response for the detuned carrier

## What this establishes

The homogeneous Gaussian conversion result does not establish spatial
survival. In a controlled auxiliary calculation, a stationary isotropic
Gaussian daughter shell drives moving source modes with a secular connected
variance. Its lowest momenta are excluded by the earlier small spatial
boxes. A direct reuse of those boxes would therefore be inadequate.

This is a forced linear response with prescribed daughters, not the actual
produced-state evolution and not an instability eigenvalue. It does not
show that the detuned candidate fails. Charge is not conserved after imposing
the external, undepleted daughter field; the approximation must fail before
its predicted source fraction becomes order one.

## Derivation

Use the earlier classical envelopes, with time x=m epsilon t/hbar and
momentum q=p/(m u):

    i dB/dx = L_b B + A^2,
    L_b(Q) = [sqrt(R^2+u^2 Q^2)-R]/epsilon,
    R=M/m=2 sqrt(1+u^2).

Take a mean-zero homogeneous isotropic Gaussian daughter field with all
power on |q|=1 and mean |A|^2=F. These free daughter modes have L_a=0.
Set the initial moving source to zero. For a pair of daughter directions
with cosine mu, Q^2=2(1+mu) and the forced source kernel is

    |integral_0^x exp(i delta s) ds|^2
       = 4 sin^2(delta x/2)/delta^2, delta=L_b(Q).

Wick contraction gives two identical normal contractions in the connected
variance. The anomalous contraction, if present, contributes to the mean
uniform source and is removed from this connected moving response. Thus

    F_B,Born(x) = 2 F^2 integral_0^D (a+b delta)
                        4 sin^2(delta x/2)/delta^2 d delta,
    D = [sqrt(R^2+4u^2)-R]/epsilon,
    a = R epsilon/(2u^2), b=epsilon^2/(2u^2).

Here (a+b delta) is the normalized angular probability density obtained
from uniform mu in [-1,1]; its integral equals one. For a continuum angular
distribution, exactly Q=0 has measure zero. This calculation does not replace
the coherent uniform source already retained in the Gaussian production run.

The integral is analytic:

    I0 = 2x Si(Dx) + 2[cos(Dx)-1]/D,
    I1 = 2[gamma + log(Dx) - Ci(Dx)],
    F_B,Born = 2 F^2 (a I0 + b I1).

It starts as 2 F^2 x^2. For Dx >> 1 its leading term is
2 pi a F^2 x, approximately 2 pi epsilon F^2 x/u^2. Detuning suppresses
this response but does not eliminate it at arbitrary duration.

## Finite example and interpretation

At the detuned parameters u=0.01, epsilon=1e-7, F=1:

| Elapsed envelope time x | Forced source charge |
| ---: | ---: |
| 1 | 0.00627950 |
| 10 | 0.0628310 |
| 30 | 0.188501 |
| 100 | 0.628346 |
| 200 | 1.25670 |

The value above one is a breakdown diagnostic for the undepleted-forcing
approximation, not a physical charge fraction. The response reaches 0.1
at x=15.9153 and one at x=159.148. Neither is the survival time of the
actual production state: its daughter fraction builds dynamically, its
radial bandwidth is finite, its anomalous phases evolve, and quartic shifts,
backreaction and source remnants alter the response.

Modes satisfying delta x <=1 have

    Q <= sqrt(2 R epsilon/x + epsilon^2/x^2)/u.

At x=200 this is Q<=0.00447225. Resolving even one nonzero grid momentum
below this scale while retaining Nyquist Q>=2 requires about 895 points
per spatial axis on a uniform cubic grid. This is a necessary scale screen,
not a sufficient convergence criterion. The old dq=0.4 boxes contain none
of these low-momentum moving modes; their detuned reuse could artificially
remove the response. Alternative continuum or multiscale methods are needed
before making a spatial survival claim.

## Evidence and next step

`detuned_moving_response.py` evaluates the closed form, checks the angular
normalization and early-time limit, and compares against direct oscillatory
quadrature at four times. All six checks pass. The contract and result are
saved with the validated manifest in `detuned_moving_response_run`.

Next, integrate the angular response over the saved produced radial spectrum
and then include its time-dependent unequal-time correlations. This tests
whether finite bandwidth dephases or enhances the moving-source response
before choosing a spatial discretization. The vacuum acceleration law and
halo formation remain separate unresolved requirements.
