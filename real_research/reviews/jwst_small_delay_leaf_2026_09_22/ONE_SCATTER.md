# One-scattering delay leaf — conditional model mathematics, novelty unclaimed

Central emission, unit sphere, speed1, uniform scattering rate tau>0, scalar
unpolarized Thomson cosine density p(mu)=3(1+mu^2)/8, no absorption. Define
F1(e)=P(0<D<=e AND exactly one scattering); this is NOT normalized conditional
on one scattering. For0<e<=1 the following sandwich holds:

 J(d) = (3/4)log(2/d) -3/4 +3d/4 -3d^2/16,
 K(e) = (3/4)e log(2/e) +3e^2/8 -e^3/16,
 A(e) = tau exp(-tau) K(e),
 exp(-tau e) A(e) <= F1(e) <= A(e).

Consequently F1(e) ~ (3tau/4)exp(-tau)e log(1/e) for fixed tau as e->0+.
This proves ONLY the one-scattering contribution. No full-distribution
asymptotic, selected cap violation, observational prediction or novelty is claimed.

Proof. The first scattering radius r has density tau exp(-tau r),0<r<1.
After its cosine mu, remaining straight length to the boundary is
L=-r mu+sqrt(1-r^2+r^2 mu^2). Exactly one scattering contributes the independent
no-further-scattering probability exp(-tau L). At exit
Z=r mu+L, hence D=r+L-Z=r(1-mu). Fixing d gives mu=1-d/r, Jacobian1/r and
r in[d/2,1]. Thus the one-scattering density is

 f1(d)=tau integral[d/2,1] p(1-d/r) exp(-tau T(d,r)) dr/r,
 T(d,r)=d+sqrt(1-2rd+d^2).

For0<d<=1 and d/2<=r<=1, the square root lies in[1-d,1], so
1<=T<=1+d. The nonnegative integrand therefore yields
 tau exp[-tau(1+d)] J(d)<=f1(d)<=tau exp(-tau)J(d),
where direct polynomial integration of p(1-d/r)/r gives J(d) above.
Integrate from0 to e. Since exp(-tau d)>=exp(-tau e), and
integral[0,e]J(d)dd=K(e), the sandwich follows. Its two endpoints have the
same displayed leading asymptotic. The logarithmic singularity is integrable.

This is a Codex derivation/self-review. Independently written coordinate
quadratures in verify.py check tau1/4 and e=.01,.003,.001 with refinement
and a real isotropic-kernel mismatch. Numerical agreement is not the proof;
the inequalities above are. No multiple-scattering remainder has been bounded.
The full D distribution also has the separate zero-scattering atom exp(-tau).
