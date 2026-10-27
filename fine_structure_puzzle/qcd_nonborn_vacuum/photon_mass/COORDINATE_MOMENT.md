# Full-trace coordinate second moment

Separate post-run analytic companion. It changes no frozen computation input
and claims no execution of a QCD coordinate-moment dataset.

Use the same Euclidean continuation and state/current normalization as the
canonical mass convolution:

    H_mu,nu(x)=<p|T j_mu(x)j_nu(0)|p>_vacsub/(2M),
    M_u(s)=(1/2) integral d^4x H_tr(x) D_s(|x|)+matching.

Spin average is understood. The trace is the Euclidean trace consistent with
that convolution; all Ward contacts and a complete same-convention Born
subtraction are included. For the non-Born part the Bessel kernel in the
frozen derivation gives

    G3(s)=1/(256pi^2 M) integral d^4x
                  |x|^2 H_tr^NB(x) K2(sqrt(s)|x|).         (1)

The soft tensor, independently reconstructed from both scalar amplitudes, is

    Htilde_tr^NB(Q)
      =4pi[(a-2b)Q^2+2(a+b)Q4^2]+O(Q^4),
    a=alpha_E/u, b=beta_M/u.                               (2)

In particular `integral H_tr^NB=Htilde_tr^NB(0)=0`. Fourier differentiation
and `Delta_Q Q^2=8`, `Delta_Q Q4^2=2` give

    integral d^4x |x|^2 H_tr^NB(x)
      =-Delta_Q Htilde_tr^NB(0)=-48pi(a-b).                (3)

Consequently

    C_NB=-1/(512pi^2 M) integral d^4x |x|^2 H_tr^NB(x)
        =3(a-b)/(32pi M).                                (4)

There is a useful direct justification of the Bessel limit. The Schwinger
representation implies

    r^2 K2(sqrt(s)r)
       =(2/s) integral_0^infinity du u exp(-u-sr^2/(4u)).

Since `0<=1-exp(-v)<=v` for v>=0,

    |r^2 K2(sqrt(s)r)-2/s|<=r^2/2.                        (5)

Pointwise the subtracted kernel tends to `-r^2/2`. If the nonlocal part of H
has finite absolute second moment, dominated convergence using (5), together
with `integral H=0`, proves (4) from (1). Any local distributions must be
treated in their fixed matching prescription and their action on this kernel
included explicitly. They cannot be silently removed from a lattice tensor.
The QCD gap motivates tail control but is not, by itself here, an audited
uniform lattice-continuum/moment bound. UV renormalization and the connected
vacuum subtraction must be respected.

This uses the full trace and full four-dimensional `r^2=t^2+|x_space|^2`.
The earlier sea datum `integral dt t^2 integral d^3x sum_i H_ii` is one
different component moment. It neither supplies the temporal component nor
the spatial second moments and complete Born/contact subtraction in (4).
No new numerical full-QCD moment is inferred from that datum.

A QCD-only coordinate implementation could convolve an infinite-volume
photon kernel and reconstruct the long-distance QCD tail, rather than
simulate a tiny photon mass on a huge QED_M lattice. This changes the
practical finite-volume problem, but does not solve it automatically:
finite-QCD-volume effects, the Born prescription, current normalization,
all sea contraction classes and tail reconstruction still require control.
It would compute an independent physical polarizability combination, while
the full hard mass response and curved-vacuum coefficient remain separate.
