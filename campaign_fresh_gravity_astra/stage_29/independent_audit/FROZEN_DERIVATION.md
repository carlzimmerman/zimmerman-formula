# FGF042 independently frozen exact-energy compactness argument

Frozen before new author/root proof or previews. Proof-only. Fix the actual reviewed static Q crossing restricted to I=(-d,d), length ell; physical coefficients C,tau,sigma,J,S0,u=cs²>0 remain fixed. Background rho>0, g=phi', a=a_ref exp chi, with B'=C rho, u rho'=-rho g, Jchi''=U'-T and U=S0(cosh(2chi)-1)/4. Once d is chosen its induced mass M and walls remain fixed during comparisons. Nonnegative n has mass M and finite entropy. At n=0 kinetic j²/n means0 when j=0 and infinity otherwise. Finite kinetic energy requires j=0 on vacuum. Allow psi,eta in H1_0, ||eta||infinity<=1/4, arbitrary finite-action gradients and field velocities. No density pointwise cap.

## Full identity and retained exact remainder

Let z=psi', a_eta=a exp eta and D_a(g,z)=W(|g+z|,a)-W(|g|,a)-B(g,a)z. Define

 K=integral[j²/(2n)+(tau phi_t²+sigma chi_t²)/(2C)],
 q_psi=rho exp(-psi/u)/Z, Z=integral rho exp(-psi/u)/M,
 H(n|q)=integral[n log(n/q)-n+q].

The full relative total energy is exactly

 E=K+u H(n|q_psi)+Fmin(psi)
   +(1/C) integral[D_(a_eta)(g,z)+(B(g,a_eta)-B(g,a))z
                   +R_scale+Jeta'²/2+U_rel],
 Fmin=-u M log Z-integral rho psi,
 R_scale=W(|g|,a_eta)-W(|g|,a)+T(g,a)eta.

All hydrostatic mass, potential source and scale first variations cancel using fixed walls and actual signed flux, with no center boundary term. This is exact finite-increment algebra. Nonnegative n including vacuum obeys it by 0log0=0. The tilted entropy proof supplies Fmin>=-alpha E_p, alpha=C M I_A/(8u), E_p=integral A z²/C, I_A=integral1/A.

From prior globally proved D_(a_eta)>=k A z², k=exp(-1/4)/64, retain HALF of the exact remainder. Define qhat,Dhat as the suprema of q and |T_chi| at fixed background g over |theta|<=1/4. Then

 D_(a_eta)+(B_eta-B)z+R_scale
 >=(1/2)D_(a_eta)+(k/2)Az²-qhat|eta z|-Dhat eta²/2
 >=(1/2)D_(a_eta)+(k/4)Az²-R2 eta²,
 R2=qhat²/(k A)+Dhat/2.

Use Young qhat|eta z| <= (k/4)Az²+qhat² eta²/(k A). At g=0 set R2=0; qhat=Dhat=0 and exact D remains nonnegative. Since U_rel>=S0 eta²/2 and ||eta||2²<=ell²||eta'||2², strengthened gates

 alpha<=k/8, beta2=ell² max(R2)/J<=1/4

imply the full lower bound

 E>=K+u H(n|q_psi)+(1/(2C))integral D_(a_eta)(g,z)
          +(k/8)E_p+(1/4)E_eta+(S0/(2C))integral eta²,
 E_eta=J integral eta'²/C.                                      (1)

Every summand is nonnegative. The gates are nonempty on restrictions of the same central solution: M=O(d), I_A=O(sqrt d), qhat²/A and Dhat=O(d^(3/2)), hence alpha=O(d^(3/2)), beta2=O(d^(7/2)). No physical coefficient or cap is retuned, and there is no universal measured radius. Mass and induced walls change between restrictions, not between comparison states on the chosen interval.

## A uniform finite-increment estimate, not uniform quadratic curvature

For any real g,z and a>0,

 D_a(g,z)=z² integral_0^1(1-t)A(|g+t z|,a)dt,
 A(s,a)=2s/sqrt(a²+4s²).

For z nonzero, the set with |g+t z|<|z|/4 has t-length at most1/2. Within [0,3/4] its complement therefore has measure at least1/4; on that complement1-t>=1/4. Monotonicity of A yields

 D_a(g,z)>=z² A(|z|/4,a)/16.                              (2)

This handles any sign reversal and every background g; at z=0 both sides vanish. The scale cap bounds a_eta<=a_bar=exp(1/4)max_I a, a FIXED positive physical acceleration. For every physical acceleration threshold delta>0, split |z|<=delta and |z|>delta to get

 integral z² <= ell delta² +16 integral D_(a_eta)/A(delta/4,a_bar)
              <= ell delta² +32 C E/A(delta/4,a_bar).      (3)

Consequently E_m->0 first with delta fixed and then delta->0 gives ||psi_m'||2->0 UNWEIGHTED. This does not assert quadratic coercivity with a fixed positive constant: at g=0 and z->0, D_a(0,z)=|z|³/(3a)+O(|z|5), so D/z²->0. This failed stronger assertion is explicitly preserved. The result is a convergence modulus, not nondegenerate Hessian recovery.

## All components and matter convergence

Equation(1) gives eta'->0 in L2, phi_t and chi_t->0 in L2, and integral j²/n->0. Fixed zero traces give eta and psi uniform convergence to0. Weighted bound already suffices for ||psi||infinity²<=C I_A E_p, but (3) additionally gives the requested unweighted gradient convergence. These statements keep actual fixed kinetic coefficients rather than interpreting sum norms across incompatible units.

Entropy H(n|q_psi)->0 and elementary bound ||n-q_psi||1²<=4M H imply n-q_psi->0 in L1. Since psi->0 uniformly, Z->1 and q_psi/rho->1 uniformly; thus n->rho in L1. Background entropy convergence is separate:

 H(n|rho)=H(n|q_psi)+integral n log(q_psi/rho),
 |integral n log(q_psi/rho)|<=2M||psi||infinity/u ->0.

This includes n=0 exactly and asserts no no-vacuum property or density L2 bound. In addition, write the pointwise entropy integrand relative to rho as h>=0. Then

 e(n)-e(rho)=u h+u log(rho/rho_ref)(n-rho).

Because rho is bounded positive, its logarithm is bounded, so e(n)->e(rho) in L1. Matter momentum satisfies ||j||1<=sqrt(M integral j²/n)->0. Only density-weighted L2 velocity is controlled; unweighted fluid velocity need not converge or even be defined at vacuum.

## Identified products and density versus flux

Strong L2 convergence of g+z to g and uniform convergence of a_eta to a imply B(g+z,a_eta)->B(g,a) in L2: B is1-Lipschitz in g and |B_log a|=q<=a/2 on the cap. W converges in L1 by its linear growth gradient derivative and |W_log a|=T<=a|G|/2 (T(0)=0 and T_s=q<=a/2). Hence B G, W, kinetic field squares, field momenta phi_t G and chi_t(chi'+eta'), scale-gradient square and U all converge in L1. The scale source T converges in L1 by continuity plus the same capped linear growth, or splitting a bounded-gradient set and using L2 tails. Matter kinetic density j²/(2n), kinetic momentum flux j²/n and pressure u n converge in L1. Interaction n(phi+psi)->rho phi in L1 since phi bounded and psi uniform. Thus full energy DENSITY and combined momentum density/stress converge strongly in L1. Their concentration defects vanish.

Field energy flux -[phi_t B+J chi_t(chi'+eta')]/C converges in L1 to0. This does NOT identify general fluid energy advection v[j²/(2n)+e(n)+u n+n(phi+psi)]. K controls neither cubic velocity nor velocity-weighted entropy. A single illustrative admissible-state counterexample: n=rho, psi=eta=0, and v_N=v0 N f(N³(x-x*)/L), f>=0 smooth compact nonzero, supported away from walls. Its kinetic energy is O(1/N)->0, but cubic advective energy-flux integral tends to a positive constant proportional to rho(x*) v0³ L integral f³/2. Lower enthalpy/potential advection vanishes. This is not a trajectory or residual approximation; it isolates precisely the missing general energy-flux moment. No claim about arbitrary finite nonzero energy compactness or strong force product nG follows.

## Conditional time statement only

For already-existing admissible trajectories on a fixed time slab with fixed reference/walls/mass, correct vacuum convention, finite entropy, eta continuous in H1, initial quarter-cap strict, and an ASSUMED full relative energy inequality E(t)<=E(0), suppose E_m(0)->0. The bound E>=E_eta/4 and endpoint inequality ||eta||infinity²<=ell||eta'||2²/4 imply E>=J||eta||infinity²/(C ell). The first exit at ||eta||infinity=1/4 would cost J/(16C ell). For sufficiently small initial energies it is excluded by continuity and the assumed inequality. The lower bound therefore holds throughout the already-existing slab, yielding each stated spatial convergence uniformly in time by (1)-(3). No source work or evolving-reference work is omitted under the fixed-reference premise. Existence, wall/initial traces, energy inequality, continuation and uniqueness are NOT derived. Density need not stay positive.

## Controls and scope

At fixed density/scale the interaction cancels exactly and full relative energy is K+integral D_a(g,z)/C, so (2)-(3) directly apply without absorbing cross terms. FGF041's main packet fails E->0 because it retains E_*>0 initially; its small-amplitude control satisfies the changed hypothesis and converges strongly. No packet rerun or concentration scan is needed.

The result is a local exact static energy-to-compactness gate and a separately conditional time statement. Both registered positive a0 normalizations, constant-vacuum and frozen-H cases remain separate; an evolving-H reference needs exchange accounting. Signed Q MOND source and actual tau are preserved. No RAR/M/filtered-MONO, physical metric/photon, physical reservoir, observations, novelty or theory closure follows.
