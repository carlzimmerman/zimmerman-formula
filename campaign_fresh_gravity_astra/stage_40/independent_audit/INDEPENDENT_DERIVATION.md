# FGF053 independently reconstructed continuation argument

Reviewer /root/fgf053_reviewer. This file is frozen before exposure to any new FGF053 author proof, result, preview, or stage40 root proof. The 12 task ancestry pins and the task pin matched before ancestry use. Old ancestry reviews were read as dependency records. This is independent reconstruction of the new implication, not blind rediscovery of inherited FGF047/048/049/052 mechanisms. Zero mathematical executable computations; SHA checks are provenance only.

## Claim card and exact objects

Fix positive C=4pi G, tau,sigma,J,S0,c=cs,nref,L,v0,a_ref and a smooth hydrostatic background on a regular open interval U around x*. Set g=phi_x>0,p=phi_t,k=chi_x,w=chi_t,a=a_ref exp chi,
B=(sqrt(a^2+4g^2)-a)/2, W=int_0^g B(s,a)ds, T=-W_chi,
U_s=S0[cosh(2chi)-1]/4. The actual equations are

n_t+(nv)_x=0; v_t+v v_x+c^2(log(n/nref))_x=-g;
tau p_t=B_x-Cn, g_t=p_x;
sigma w_t=J k_x+T-U_s', k_t=w_x, chi_t=w.

Initial n=rho,phi=phi0,chi=chi0,p=w=0; hydrostatics obey B0_x=C rho, c^2(log rho)_x=-g0, J chi0_xx+T0-U_s'=0. Initial v=V f((x-x*)/ell), V=v0 N, ell=L N^-3, f=(1-y^2)^2 for |y|<1 and zero elsewhere. The exact C1,1 joins stay unchanged. No speed, pressure or coupling depends on N except this prescribed datum. No static source equation is imposed after t=0.

Use fixed FGF048 units x/L,t v0/L,v/v0,n/nref,phi/v0^2; suppress hats below. Thus ell=N^-3,V=N and physical time=(L/v0)t. All sums of norms below are in these fixed units. Let Bdag>15/8 be fixed, Theta=Bdag N^-4, and choose an auxiliary ceiling H=2Theta. All arguments below can use H in the protected-edge and amplitude bounds. The true endpoint lies at or before Theta, so this ceiling cannot create it.

## One common physical germ with collars

Choose a fixed closed J contained in U, with a larger fixed interval Jplus compactly in U; the packet is centrally located in J. Use the pinned FGF052 endpoint construction A=-ell-d N^-7/2, D=ell+d N^-7/2, with its fixed d,r>0. For sufficiently large N the known edge solutions exist through H, and their exterior cones contain neighborhoods of A,D of radius at least r N^-7/2/2 throughout [0,H]. Their equality to hydrostatics is exact in those open neighborhoods, including the potentials and every available derivative. This is the proved FGF052 section2 consequence of the FGF051 edge theorem; a bounded edge value alone would not suffice.

Take representatives on [0,t] times a neighborhood of J, t<H, of the full compatible positive classical system, equal to the hydrostatic tuple on J outside [A,D]. Require the seven first-order variables to be spacetime C1, with uniformly Lipschitz first spatial derivatives on each compact time slab; phi,chi are C2. Potential phi uses its actual initial additive constant. Two representatives are identified by equality on J and its physical collars. We use restrictions of local continuations, not a chosen global auxiliary Cauchy solution.

This class is nonempty for all sufficiently large N: the actual FGF048 branch exists past kappa N^-4 on a physical cone containing J, after taking J inside its R/2 interior. FGF052 comparison forces equality to the edge solutions on the protected endpoint neighborhoods. Restrict to [A,D] plus those neighborhoods and glue to the exact stationary background on Jplus outside [A,D]. On overlaps the functions and derivatives agree identically, so this is a solution of the actual equations, with original initial data on Jplus. Thus the lower branch belongs to precisely this germ.

Uniqueness for this class does not require every backward characteristic to stay inside [A,D]. Stop it at its initial contact or first contact with a lateral boundary of J. In the latter case the two representatives agree because both equal hydrostatics in an open outer collar. On a compact slab their coefficient ranges and first derivatives are bounded. Subtracting the diagonal equations along the first solution's characteristics gives D(t)<=K int_0^t D(s)ds, with zero initial/lateral data; iteration gives D=0. Potential constants agree from p and the initial phi. Consequently representatives agree on overlaps, admissible times form an interval, and their union defines a unique maximal germ up to a supremum T_N<=H.

The imposed stationary exterior is not an arbitrary wall condition. The already proved one-sided edge comparison forces the exact stationary collar at A,D for any existing positive whole-packet solution on the common edge domains, independently of its internal fluid speed. One glues there to a stationary solution with fixed outer physical buffers. Conversely each germ representative solves the physical equations on the original packet and those edge domains. Any auxiliary extension away from U has no role in this definition. Its initial restrictions yield the same branch by the uniqueness argument, and an auxiliary global lifespan is never called T_N.

The FGF052 upper contradiction applies verbatim to this same branch on [A,D]. If T_N>Theta it exists on a neighborhood of the closed slab through Theta, contrary to that theorem. Hence kappa N^-4<=T_N<=Theta<H. Equality with Theta as a limiting endpoint is not excluded or asserted. The truncation ceiling and fixed exterior boundaries lie strictly beyond the relevant obstruction.

## Actual margins on every existing truncated branch

FGF052's source proof works on each existing [0,t], t<=H, without assuming existence to H: mass M=int_A^D n=int_A^D rho=O(ell), exact stationary lateral values, and first initial/lateral contacts suffice. Set b=sqrt(B_g/tau), d_s=sqrt(J/sigma), h_g=b,
z=(Rplus,Rminus,Zplus,Zminus,chi), Rplus=p+h,Rminus=p-h,Zplus=w+d_s k,Zminus=w-d_s k.
The full equations are

D_(v+c) r=-g, D_(v-c) s=-g, r=v+cq,s=v-cq,q=log n;
D_-b Rplus=B_chi k/tau+h_chi(w-bk)-Cn/tau;
D_+b Rminus=B_chi k/tau-h_chi(w+bk)-Cn/tau;
D_-d_s Zplus=D_+d_s Zminus=(T-U_s')/sigma; chi_t=w.

Bootstrap z in a fixed compact positive g chart about z0(0). Under |g|<=Gbar and |lambda_Q|<=Lambda, both r,s are bounded below by -L0 with L0=cQ0+Gbar for H<=1. Their initial values are bounded below by -cQ0 because v>=0 initially; lateral values are hydrostatic. Thus v>=-L0. On the actual set v<=Vcut=Lambda+1, n<=exp((Vcut+L0)/c)=Ncut, using both invariants and r+s=2v. This is independent of N and does not assume a gradient bound.

For m(t,x)=int_A^x n, m_x=n,m_t=-nv. Along either Q path, m'=-(v-lambda)n. On v>Vcut the relative speed exceeds1. On v<=Vcut, |v-lambda| is bounded and n<=Ncut. One signed integration over the whole path gives int n ds<=M+C t; there is no repeated mass charge per excursion. Consequently integration of the two Q equations and both scale equations gives sup_[A,D]|z-z0(0)|<=C1 ell+C2 t<delta/2 for all t<=H and N large. This strict improvement excludes a first compact-chart exit while the branch exists.

Therefore g>=gmin>0, a>=amin>0, g,a,p,w,k,chi are bounded there independently of N. On the exterior the background supplies fixed margins. It is important that this is a truncated-time consequence of the proof, not an illicit application of a theorem requiring a future surviving branch.

The upper acoustic estimates also follow from first initial/lateral contact: r,s<=N+cQ0+Gbar H (one may use the less sharp absolute bound). Together,
|r|,|s|<=N+cQ0+Gbar H,
|q|<=(N+cQ0+Gbar H)/c,
exp(-(N+cQ0+Gbar H)/c)<=n<=exp((N+cQ0+Gbar H)/c).
Restoring density multiplies these by nref. These are positive and finite for each fixed N, and explicitly are NOT uniform in N. The fluid speed is bounded by N+cQ0+Gbar H; fields by fixed speeds. Spatial paths hitting [A,D] boundaries have stationary data; paths on the larger physical domain either remain there or contact known hydrostatic collars. No unaccounted lateral incoming data enter.

## Coupled derivative continuation, derived at the actual trace

Suppose for one fixed N that limsup_(t up T_N) D1(t)<infinity, where
D1=max(||r_x||,||s_x||,max_i||z_i,x||) on J in the fixed units. Compact earlier slabs then make D1 bounded on all [0,T_N). This norm is equivalent, with fixed-N finite constants, to the first-gradient maximum of q,v,p,g,w,k,chi; n_x is also equivalent after using the proved density margins. It is a combined fluid/field norm: its divergence alone does not identify which component fails.

The preceding margins give a compact full state range for this fixed N. Extend smooth coefficients by cutoffs on a slightly larger chart; finite derivative constants then control differences even when a joining line leaves the original range. Let A=max(||r_x||,||s_x||), B=max_i||z_i,x||; let Hf=max(Lip r_x,Lip s_x), Hz=max_i Lip z_i,x. From differentiated characteristic equations,

Hf(t)<=Hf(0)+int_0^t [3A Hf+G Hz+G2 B^2]ds,
Hz(t)<=Hz(0)+int_0^t [(3L1 B+P)Hz+(P/c)Hf+L2 B^3+Q(B+A/c)^2]ds.

Here L1,L2 bound derivatives of field speeds, G,G2 derivatives of g(z), and P,Q first and second derivatives of the full field sources in (q,z). In particular derivatives of -C exp(q)/tau, B_chi k/tau, h_chi(w +/- bk), (T-U_s')/sigma remain in P,Q. Field source derivatives are not set to zero or estimated from static inversion.

For clarity the factor3 has three origins: the coefficient times the differentiated gradient, variation of lambda_x, and differentiating the separation used to divide pair-characteristic differences. More explicitly, D_i z_i,x=-lambda_i,x z_i,x+(H_i)_x. Taking differences at two points on same-family trajectories and dividing by their separation bounds lambda_i,x by L1 B, its Lipschitz constant by L1 Hz+L2 B^2, and Lip(H_i,x) by P(Hz+Hf/c)+Q(B+A/c)^2. Combining gives the second line. The first follows identically from lambda=v +/- c, lambda_x=v_x, Lip(v_x)<=Hf, and source -g(z). These estimates use spatial difference quotients, so they apply at the original Lipschitz joins without assigning a classical second derivative there.

On J one can use pairs up to first exterior-collar contact, where all data are fixed background; alternatively extend the solution by hydrostatics across J into Jplus, take a slightly larger compact interval with stationary collars, and charge its fixed background derivative bounds. A maximum of these fixed bounds and Hf,Hz has the same linear Gronwall estimate after enlarging the finite initial/forcing constants. Thus A,B bounded implies Hf+Hz remains bounded through T_N. There is no additional higher-norm obstruction.

Write U=(r,s,z). The equation U_t=-lambda(U)U_x+F(U) gives a uniform bound for U_t. Since U_x is uniformly spatially Lipschitz,
(U_i,x)_t=-lambda_i U_i,xx-(Dlambda_i.U_x)U_i,x+D F_i.U_x
holds distributionally with every right-hand term uniformly bounded for this fixed N. Integrating in time and choosing continuous spatial representatives makes U_x uniformly Lipschitz in time in sup norm on a smaller buffered interval containing [A,D]. Thus U and U_x have actual uniform endpoint limits U*,U*_x, and spatial integration proves that U* has derivative U*_x. Its derivative remains Lipschitz. No convergence in the C1,1 norm itself is required. The inherited chart/density margins persist at the trace.

Compatibility also survives: chi_x=k in the uniform C1 trace; phi(t,x)=phi0(x)+int_0^t p(s,x)ds converges, phi*_x=g*, and both potentials agree with the hydrostatic ones in the endpoint neighborhoods. Gluing the endpoint trace to hydrostatic data outside [A,D] is exact on overlapping neighborhoods, so it is compatible C1,1 data on Jplus. Extend q*,chi*,g* smoothly in the C1,1 sense outside Jplus by cutoffs to constants, retaining positive g; set k*=chi*_x and phi* to an antiderivative of g* matching the existing potential. The phrase C1,1 extension does not mean smoothing or altering any data in Jplus. Retain the actual endpoint p*,w*,v*. The pinned FGF047 construction supplies a strictly positive restart time for these exact data.

The restart solves the full diagonal system and its constraints: k_t=w_x and chi_t=w imply chi_x=k from initial compatibility; subtraction of the Q equations gives g_t=p_x, while addition gives p_t=b^2g_x+A+b h_chi(chi_x-k), so the extra term vanishes. Reconstruct phi by integrating p in time. It solves tau phi_tt=B_x-Cn, and the scale equation is the actual one. Uniqueness identifies it with the old solution on overlap. Local hydrostatic comparison in the positive-width endpoint neighborhoods preserves smaller stationary collars for a positive restart time; restrict to them and glue back to the fixed background. Because T_N<=Theta<H, this time can be shortened to stay below H without becoming zero. This extends the germ and contradicts maximality.

Thus limsup D1=+infinity. In physical time,
kappa (L/v0)N^-4<=T_N<=Bdag (L/v0)N^-4
for each fixed Bdag>15/8 and all sufficiently large N in each fixed coefficient/background cell. The upper coefficient is neither sharp nor attained by this reasoning. State amplitudes and density remain in fixed-N positive compact sets; the obstruction is a first spatial gradient of the actual coupled state. We have not proved a limit rather than a limsup, a fluid shock, a gravitational instability, or a weak continuation.

## Energy, controls, scope, and dependency verdict

For fixed reference,
e=c^2 n[log(n/nref)-1],
E=nv^2/2+e+n phi+[tau p^2/2+W+sigma w^2/2+J k^2/2+U_s]/C,
F=nv[v^2/2+c^2 log(n/nref)+phi]-(pB+Jwk)/C.
Direct differentiation gives E_t+F_x=0: matter interaction gives +np, Q gives -np-Tw/C, scale gives +Tw/C. Moving endpoints add beta'E(beta)-alpha'E(alpha); no unsigned global coercivity is assumed. Stationary collars give zero flux at fixed A,D. With v initially zero, hydrostatic data give the exact stationary solution with p=w=0 and F=0; its initial packet momentum is zero and the upper moment contradiction is not triggered.

Both a_ref=9.3619e-11 and 1.1279e-10 m/s^2 are separate coefficient/background choices. Constant vacuum and separately frozen a0 E(z), E^2=.315(1+z)^3+.685, are distinct; evolving reference is excluded from the stationary/autonomous argument. The adopted scale relation and diagnostic chi are not a physical vacuum/two-DOF closure. Q, RAR, registered M and filtered MONO remain distinct. No calibration, criterion B, metric/photon, cosmological, observational, novelty, or physical-theory closure follows. No verified observational velocity window is supplied for the high-N nonrelativistic family. FGF049's adverse-gradient gate remains unproved and was bypassed by the source method.

Dependency graph: exact diagonal formulation and compatible local restart (FGF047) -> actual small-kappa branch and difference-quotient inequalities (FGF048) -> protected stationary collars (FGF052 section2, with its pinned FGF051 dependency) -> actual truncated source margins and upper moment obstruction (stage39 ROOT_TRANSFER_BOOTSTRAP) -> common-domain union, fixed-N trace, exact gluing/restart (this derivation) -> two-sided lifespan and combined-gradient limsup.

Obligation matrix: exact data/couplings passed; source ancestry passed; same-domain lower/upper matching passed through stationary overlap gluing; positivity/amplitude margins passed; fixed-N fluid bounds passed; linear higher-norm propagation passed; endpoint trace/compatibility passed; exterior gluing and no auxiliary lifespan substitution passed; energy/control passed; physical closure and shock type out of scope. There is no external PDE theorem leaf or computation leaf. The protected-edge theorem is an internal ancestry leaf, not rederived here beyond the FGF052 comparison proof. Primary provisional verdict for this reconstructed implication: proved as written in the precise buffered-germ formulation above. This does not audit the still-unseen author proof; any missing author domain step must be reported separately.
