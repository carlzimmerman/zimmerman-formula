# Independent audit of the low-field moment relation

Verdict: the asymptotic force deficit, strict all-positive-lambda moment inequality, and sharp small-lambda limit are correct for the declared auxiliary NR branch. No covariant vacuum normalization follows. I reconstructed the root comparison and improper integral independently of the check counts.

Inspected checkout HEAD: `30568b15bff7b740146b213ac7d113a8d2897e38`. Frozen REPORT SHA-256: `83b8a127d0a324d77358ece6b9aa0c631c16d031d8ed46c029b363aae2d2ffc4`; checks.py: `2d19275ba24452e38a67214454d4e5b6e3e95c78370bbf5f30c7b35e485f0a5c`. Parent REPORT/action were read as the branch premise. No author input was modified.

## Independent reconstruction
At fixed positive lambda, stationarity gives T^4 ~ 8 y^(7/2)/(7 lambda). Set d=(y/T)^2. Thus d=sqrt(7 lambda/8)y^(1/4)[1+o(1)]. The exact force ratio is sqrt(y)+sqrt(y)b(y)/(1+d). Since sqrt(y)b(y)=sqrt(1+y)−sqrt(y), the ordinary corrections are O(sqrt(y)), smaller than y^(1/4). Consequently the leading deficit is A=sqrt(7 lambda/8), with precisely the stated order of limits. The coefficient is not a finite-radius fitting theorem.

Under v=lambda y and w=lambda T, rationalizing b gives B_lambda(u)=1/[u(sqrt(1+lambda/u)+1)]. The stationary equation is 1=4 integral_0^v u^3 B_lambda(u)/(w^2+u^2)^2 du. Its right side strictly decreases in w. The strict bound B_lambda<1/(2u) therefore implies w_lambda<w0, where the limiting equation integrates to w0=atan(z)−z/(1+z^2), v=z w0. Both maps are strictly increasing in z, and w0<pi/2.

The integrands converge for every v>0: on a finite u interval and a fixed positive trial w, u^3 B_lambda <= u^2/2 is integrable; bracketing the unique limiting root proves convergence without interchanging a zero-w singularity. The scaled moment is integral_0^infinity v B_lambda(v)/[1+(v/w_lambda)^2] dv. It is strictly below the limiting integrand at every positive v and is dominated by 1/[2(1+(2v/pi)^2)]. This latter majorant has integral pi^2/8; it supplies domination only, not the sharp coefficient.

For the actual limiting integral, put v=zJ(z), J=atan(z)−z/(1+z^2), J'=2z^2/(1+z^2)^2. The value is

(1/2) integral_0^infinity (J+zJ')/(1+z^2) dz
=pi^2/16−1/4+1/4=pi^2/16.

The integrands are positive and strictly unequal for positive lambda, hence 0<lambda C<pi^2/16. Dominated convergence yields equality only in the lambda-down-to-zero limit. Multiplication by A^2/lambda=7/8 gives the strict product bound 7pi^2/128 and its sharp supremum. Sequences inside the parent's sufficient elliptic interval approach zero, so restricting to that interval does not change sharpness.

## Scope and evidence
The proof uses an auxiliary, nonsmooth-at-vacuum branch, a fixed ansatz for its potential, and the actual varied spherical force law. It proves a relation between two constitutive features, not a cosmological constant, material cold mass, observational fit, general propagating health, or uniqueness of a microscopic model. It leaves lambda free; measuring A would measure that parameter in this ansatz.

I inspected checks.py: its exact split and three negative controls address the constant-cutoff doubling, lost rational cancellation, and incorrect deep exponent. They do not replace the analytic root-convergence proof. Independently validated all four current main/control manifests against actual files; each validator returned success. No additional astronomical computation or fresh numerical claim was made.

## Conditional kappa corollary

Independently checked `CONDITIONAL_KAPPA_TEST.md` (SHA-256 `e64a4fb5e812ab2dc3ba444fef47bdc5bfc995b909bb45c81b54deb4ba102a86`): the audited conversion gives 8pi G_EH/G_n=2Omega chi_n, so the imposed empirical a0=kappa c sqrt(G_n rho_Lambda), conventional Lambda=8pi G_EH rho_Lambda/c^2, and conditional symmetric dictionary imply Ctarget=2Omega/kappa^2. The strict moment bound then requires lambda<kappa^2 pi^2/(32Omega) and A<kappa pi sqrt(7)/(16sqrt(Omega)). For n=3, Omega=4pi and kappa=1/2, this is A<sqrt(7pi)/64 and lambda<pi/512; the pi is inside the square root in the specialized A bound. The file's arithmetic is correct. These are necessary inequalities conditional on the radial auxiliary response, chosen UV normalization, vacuum mass-density convention, admitted covariant extension and its unproved full health; they neither select kappa/lambda nor support replacing vacuum density by total density. This analytic corollary is outside author execution inputs and adds no new computational or cosmological claim.
