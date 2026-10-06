# Independent tail-floor review

Verdict: the proposed bound is correct under the stated additive vacuum
normalization and full NR source-map condition. Strict health makes its
nonzero-endpoint tail inequality strict. This is a conditional falsification
test for a fixed coefficient, not a mechanism selecting 32pi.

Let e(y)>=0 and f(y)=y e(y). Assume f is locally absolutely continuous on
[Y,infinity), with f'(y)>-1/2 almost everywhere; equivalently the source-map
radial coefficient D=1+2e+2ye'=1+2f' is positive almost everywhere. Then for
all t>=0,

    f(Y+t)>=f(Y)-t/2,
    f(Y+t)>=max(f(Y)-t/2,0).

Integration over 0<=t<=2f(Y) yields

    integral_Y^infinity f(y)dy >= f(Y)^2,
    C>=integral_0^Y y e(y)dy+[Y e(Y)]^2.

No asymptotic endpoint assumption is needed for this inequality; an infinite
tail also satisfies it. Local absolute continuity is essential for using a
derivative bound to control finite changes: differentiability almost
everywhere alone would permit singular variation. For f(Y)>0 and strictly
positive D almost everywhere, integration gives f(Y+t)>f(Y)-t/2 at every
positive t, hence the tail is strictly greater than f(Y)^2. Equality is only
possible in the relaxed D>=0 class, with the descending triangle slope -1/2
through its nonzero support and zero tail thereafter. That region has D=0,
a degenerate radial source map, not strict convex health. Additional analytic
or smoothness constraints can raise a sharp achievable minimum; they cannot
invalidate this necessary bound.

The current same-action NR dictionary C=integral_0^infinity y e(y)dy requires
the exchange-symmetric conventions, fixed M(infinity)=0, no independent vacuum
term and the proportional-vacuum assumptions of the prior audit. Without that
normalization the bound constrains this response integral, not the total
measured cosmological curvature. D>0 is the full six-gradient NR radial
condition from that action, not a proof of covariant scalar/tensor health.
Nonnegative e is also required; a negative excess tail can defeat the triangle
area argument. These are physical premises, not consequences of data alone.

For exact P2 on 0<y<=Y,

    e(y)=sqrt(1+1/y)-1,
    f(y)=sqrt(y^2+y)-y=1/[sqrt(1+1/y)+1],
    P(Y)=integral_0^Y f(y)dy
       =(Y+1/2)sqrt(Y^2+Y)/2-Y^2/2
         -log(2Y+1+2sqrt(Y^2+Y))/8.

The lower bound is L(Y)=P(Y)+f(Y)^2, with

    L'(Y)=f(Y)[1+2f'(Y)]=f(Y)D(Y)>0.

It starts at zero and diverges to infinity, since f(y) tends to 1/2. Hence
there is exactly one solution of L(Y)=32pi. Independent 70-digit root finding
and quadrature in the bounded provenance run give

    Y_crit=202.1125602487055988690622565634061604340155468455942135,
    P(Y_crit)=100.2815814762173238813922992304971165094,
    f(Y_crit)^2=.2493834386560597494122890344469757849572.

The earlier rough estimate about 203 should be replaced by 202.11256. With
strict D>0 and e(Y)>0, a model with C=32pi must cease being exactly P2 before
this threshold: Y<Y_crit. At equality the strict tail bound already excludes
the target. This is not a predicted cutoff or transition shape, and approximate
measurements cannot be replaced by an exact functional premise.

A finite-error observational version would require a rigorous simultaneous
lower envelope e_min on 0<y<=Y and an endpoint lower bound e(Y)>=ell>=0.
Then C>=integral_0^Y y e_min(y)dy+(Y ell)^2 remains a necessary inequality.
For a uniform relative error bound e>= (1-delta)e_P2 it gives the conservative
floor (1-delta)P(Y)+(1-delta)^2 f_P2(Y)^2. Noise, distance/mass calibration,
a0/G normalization and the sampled acceleration range must justify such an
envelope. No current galaxy data analysis or empirical exclusion is claimed
by this lemma.

Reproduction: `tail_check.py`, `tail_contract.json`, and
`runs/tail_a/{manifest.json,results.json,stdout.txt,stderr.txt}`. The standard
runner completed with wall30s/CPU20s, 1MiB log cap and cooperative one-thread
libraries; its manifest validates with unchanged inputs. Exact symbolic
L'=fD and an independently integrated primitive are checked, while the
universal inequality is established by the proof above. Only reviewer-owned
files were written.
