# Explicit geometric part of the localized-packet bootstrap

Candidate internal lemma for audit, using PF08 RIEMANN_SOURCES and PF09 local
strong evolution/constraint propagation if established. Not an independent
singular-continuation result.

Use conformal base ds²=e^(2alpha)(-dt²+dx²)+e^(2beta)dy_perp². Native frame
pressures are rho=rh-H,p=H,pperp=H+PWp. Base trace and transverse Einstein
components yield exactly
 beta_tt-beta_xx=e^(2alpha)(rho-p)/(2M)-2 beta_t²+2 beta_x²,
 alpha_tt-alpha_xx=beta_t²-beta_x²+e^(2alpha)(p-rho-2pperp)/(2M).
These follow from tr_base G=2 box beta+4(grad beta)² and
G_perp=box beta+(grad beta)²-R_base/2. No matter derivative enters.
Crucially their sources use rest-frame invariants rho,p,pperp, not clock rapidity.

For initial bounded conformal metric first derivatives and compact r,A,P,
integrate along the two metric-null families. The sum of first-derivative
suprema obeys M(t)<=M0+C integral_0^t(1+M(s)²)ds while alpha is bounded.
The zeroth metric fields stay bounded by integrating their first derivatives.
Thus there is a uniform short conformal time independent of initial r_x.
This estimate can be formulated on the portion of the solution already existing;
its use does not assume a separate Einstein evolution with prescribed matter.
A regular conformal chart exists locally for the two-dimensional Lorentz metric;
continuation of the null coordinate maps is subject to the same nondegeneracy
bounds, not to a pointwise bound on r_x. This chart assertion must be audited.

Bootstrap r,A,P,theta in a fixed compact neighborhood and alpha,beta and their
first derivatives in a fixed larger bounded set. Then B=n beta,E=e beta and
omega(n),omega(e) are bounded by metric derivative bounds and bounded rapidity.
The proper clock-slice variation functional Z in PF08 satisfies
 Z'<=C(1+Z)² and controls slice length on a uniform short clock time. Hence the
auxiliary inverse gives ||u,v||infinity<=C(1+Z). It follows that along clock
worldlines nA=ru,nP=rv change A,P by O(T). Along acoustic characteristics the
exact z_sigma equations have bounded sources, so z_sigma changes by O(T).
As z_sigma=theta+sigma I(r,A), with I_r uniformly positive and bounded away
from zero, this keeps theta and r within their compact neighborhoods. The
metric-null bounds close the geometric part. Choose T0 uniformly small enough
to improve every bootstrap bound. Clock and conformal times are comparable
because r,theta,alpha stay compact. Domain margins remain positive.

Initial localized packet amplitude is fixed sufficiently small; its width
epsilon may tend to zero. The auxiliary initial solve is uniform in width,
and initial conformal metric first derivatives are uniformly bounded. Z0 is
uniformly bounded, while negative weighted compression q0 is order1/epsilon.
Thus the compact bootstrap time T0 is independent of epsilon. PF08 weighted
Riccati comparison forces unbounded a,K by time<=2/(a0 q0)<T0 for sufficiently
small epsilon, unless the exact strong evolution ceases earlier. The PF09
continuation theorem is what identifies any earlier endpoint with loss of the
same gradient control, rather than an unproved local-theory failure.

The construction would prove existence of finite-gradient breakdown for this
periodic planar constant-potential native subfamily; not breakdown of every
initial datum, not a measured astrophysical time, and not any postbreak rule.
