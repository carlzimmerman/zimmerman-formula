# Coordinator reconstruction and symmetric-buffer optimization

Candidate only, pending independent audit. This note was written AFTER the
FGF054 author's progress preview of the R=2 stationary-collar route and the
reviewer's preview that O(epsilon) exterior buffers may suffice. Neither new
raw proof was read. This is not an independent discovery or a blind derivation.
The algebra below reconstructs that cue and isolates the exact sharp condition
within this particular symmetric stationary-endpoint moment method.

Work in fixed physical units. V, sound speed cs, C,tau,sigma,J,S0,a_ref and
the smooth hydrostatic background near x* are fixed independently of epsilon.
Put initial v=V f((x-x*)/epsilon), f=(1-y²)² on |y|<1 and zero elsewhere,
with unchanged background density rho and field data. Let S strictly exceed
all hydrostatic characteristic magnitudes in a small fixed neighborhood:
cs, sqrt(B_g(g0,a)/tau), sqrt(J/sigma), with B=(sqrt(a²+4g²)-a)/2.
No RAR/M/MONO replacement or Newtonian source is made.

Choose R>1 and endpoints A=x*-R epsilon,D=x*+R epsilon. Hydrostatic
comparison cones centered there can have initial radii below (R-1)epsilon.
For a horizon T=Btime epsilon/V, a strict stationary overlap is possible if

    Btime < (R-1) V/S.                                      (1)

This comparison follows along the known hydrostatic solution's bounded-speed
characteristics. The coefficient difference multiplies the existing unknown
solution's first gradients, finite on each compact classical prefix. An
integral uniqueness inequality therefore gives zero difference on that cone.
It does not assert a universal propagation-speed bound on arbitrary nonsmooth
solutions. A fixed open collar remains if the inequality has a strict margin.

For an existing classical solution with those exact endpoints, mass is
M=int_A^D rho and P=int_A^D n v. Integrating the full fluid conservative
momentum equation yields

    P'=-int_A^D n g - cs²[rho]_A^D
      =-int_A^D (n g-rho g0),

where the exact hydrostatic relation cs² rho_x=-rho g0 supplies the second
line. No pressure boundary stress is omitted. Let F'=int(ng-rho g0),F(0)=0;
then P=P0-F. For I=int_A^D(x-A)n, I'=P and strict positivity implies
I<M(D-A). Thus survival through T requires

    int_0^T F(t)dt > P0 T - Delta0,
    Delta0=M(D-A)-I(0).                                   (2)

Let rho*=rho(x*)>0. Direct rescaling of initial integrals, keeping R,V,Btime
fixed and using smooth rho, gives

    M=2R rho* epsilon+O(epsilon²),
    Delta0=2R² rho* epsilon²+O(epsilon³),
    P0=(16/15)rho* V epsilon+O(V epsilon²).

Therefore the leading positive-capacity condition is

    Btime > (15/8) R².                                    (3)

If actual field bootstrap bounds |g|<=G uniformly in epsilon, (2)'s transfer
has magnitude at most M(G+sup|g0|)T²/2=O(epsilon³), whereas its positive
moment margin is rho* epsilon²[(16/15)Btime-2R²]+O(epsilon³).
This gives a contradiction for sufficiently small epsilon provided (1),(3)
and the actual compact-field/source conditions are proved. This note does
not replace the worker's necessary source/bootstrap and local-existence proof.

The open interval for Btime is nonempty exactly when

    V/S > (15/8) R²/(R-1).

Since R²/(R-1)=4+(R-2)²/(R-1), its minimum on R>1 is4 at R=2.
Hence this particular symmetric-buffer moment certificate has a nonempty
strict leading-order parameter cell iff V/S>15/2. R=2 realizes the least
required ratio in this method. This is NOT a necessary condition for gradient
breakdown of the PDE, a sharp lifespan constant, or a physical speed theorem.
At V/S=15/2 there is no Btime satisfying both strict conditions; this fact
only excludes this strict-margin leading-order certificate, not finer boundary
scalings, equality analysis or another method. At V=0, P0=0 and no positive
moment contradiction is available, as required by the hydrostatic control.

A matter speed ceiling alone is not enough: V must have a strict margin below
Vmax and the actual solution must obey |v|<=V+O(epsilon) on the tested interval.
The centered acoustic invariants v +/- cs log(n/rho*) plausibly give that
bound once |g| is bounded, since initial/lateral density differs from rho*
by O(epsilon). They also give epsilon-uniform density caps depending on finite
V/cs. These are obligations for the full author proof, not assumed observational
facts. If a required field speed S is too large relative to Vmax, this
certificate's cell is empty for those coefficients; changing coefficients to
make it nonempty would be a different fixed physical cell and must be declared.

Both a0 normalizations9.3619e-11 and1.1279e-10 m/s² require their own compatible
background and b_Q speed. Constant vacuum and separate frozen a0 E(z) values
are distinct autonomous cases; no evolving-reference extension here. No metric,
photon, two-DOF, criterion B, empirical calibration or historical novelty claim.
Analytic algebra only; zero mathematical executable computations. The exact
coupled energy and both field fluxes remain requirements of the underlying model.
