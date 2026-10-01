# Independent audit: quantitative Q-slab continuum gap

**Primary verdict: proved as written**, for the explicitly chosen diagnostic Q action, dimensionless initial data, couplings and induced fixed-wall interval. The exact rational checks corroborate arithmetic; the analytic first-exit and quadratic-form arguments establish the continuum conclusions. No numerical orbit, discrete spectrum, calibrated physical coupling or operative filtered-MONO claim is accepted.

Auditor `/root/metric_intake`, 2026-09-30. The root-origin candidate was audited against completed FGF023/FGF026 sources. The new FGF027 worker proof/code was **not** read or used. The separately supplied root arithmetic script, contract and completed record were inspected without rerunning them. Exact source hashes and seven matching manifest input/output hash checks are recorded in `audit_result.json`.

## Claim and dependency structure

The selected dimensionless Q family has b(0)=rho(0)=1, chi(0)=0, w(0)=1/10000 and phi(0)=0; constants C=cs²=J=S0=tau=sigma=1; U=[cosh(2chi)−1]/4; full interval D=1/100. It solves

b'=rho, rho'=−rho g, chi'=w, w'=sinh(2chi)/2−T(g,a), phi'=g,
g=sqrt(b²+ab), a=exp chi.

The claim is existence/enclosure of this same regular IVP through D, a unique first scale-gradient zero Dstar in (1/10000,1/800), and a full continuum longitudinal Rayleigh quotient bound Q2/Mkin>=359910/11>32000 on [0,D], with zero traces for all three perturbations. Its post-turn length is greater than7/800 in the chosen dimensionless coordinate.

Dependencies: declared physical scaling -> Q constitutive identities -> compact-box coefficient inequalities -> first-exit/continuation existence -> strict turn bracket -> original constrained Hessian -> trace-valid integration and Young inequalities -> Dirichlet Poincare -> positive kinetic comparison. No mesh approximation or field elimination occurs in this chain.

## 1. Physical units and kinetic normalization

With Cphys=4piG, x=Lr X, t=sqrt(Lr/ar) T, phi=ar Lr Phi and rho_phys=ar Rho/(Cphys Lr), the source equation becomes b_X=Rho. Thus the actual MOND constitutive flux, not a substituted Newtonian force, supplies the mass source. All reference quantities Lr,ar are fixed and positive for a member of the family.

The choices cs_phys²=ar Lr, Jphys=ar²Lr², S0phys=ar², tau_phys=1/(ar Lr), sigma_phys=ar Lr are dimensionally consistent with SD1. In its original notation tau=K/c² and sigma=J/v_chi², they correspond to K=c²/(ar Lr)>0 and v_chi²=ar Lr>0. They are selected couplings, not values derived from observations or a relativistic causal cone.

Use xi=Lr Xi, delta phi=ar Lr Psi and unchanged dimensionless eta. Both full kinetic and potential energies per area have common positive factor ar²Lr/Cphys. For example tau_phys(delta phi_t)²=ar² Psi_T², sigma_phys eta_t²=ar² eta_T² and rho_phys xi_t²=ar² Rho Xi_T²/Cphys. Dividing by that energy factor leaves kinetic norm integral(Rho Xi²+Psi²+eta²)dX for the mode amplitudes. Consequently a dimensionless squared-frequency lower bound restores with factor ar/Lr. The claimed physical bound is therefore dimensionally correct:

omega_phys² >= (359910/11) ar/Lr >32000 ar/Lr.

It is a result for this chosen scaled family, not a frequency prediction at a measured length. Changing ar also changes the stated physical couplings. The reference-scaled product norms do not add unscaled quantities of different physical dimensions.

## 2. Constitutive q, A and T bounds

At fixed a, inverse Q flux is b(g,a)=[sqrt(a²+4g²)−a]/2. Differentiating gives

A=2g/sqrt(a²+4g²)=2g/(2b+a),
q=gA−b=(a/2)[1−a/sqrt(a²+4g²)].

For a,g>0, q>0 and q<a/2; A>0 and A<1. Homogeneity of W supplies T_g=q and T(0,a)=0, so T(g,a)=integral_0^g q(v,a)dv at fixed a. The identities and signs match the inherited action, with T_chi=2T−gq at fixed g.

Within b,rho in[.9,1.1], |chi|<=.01, |w|<=.01, the elementary exponential bounds give .99<=a<=1.02. Indeed exp(.01)<=100/99<51/50, while exp(−.01)>=99/100. The nonnegative monotonic polynomial b²+ab is bounded by1701/1000 and583/250, giving1.3<g<1.6. Hence

A>=(13/5)/(161/50)=130/161>4/5,
0<q<=51/100.

For v in[g/2,g], v>=13/20. Then a²+4v²>=(99/100)²+(13/10)²>(8/5)², so sqrt(a²+4v²)>8/5. Both factors in q are positive, and

q(v,a)>=(99/200)[1−(51/50)/(8/5)]=2871/16000.

Integration over only the upper half of [0,g] therefore gives T>=37323/320000>11/100. The full integral upper bound gives T<=ag/2<=102/125<41/50. These are uniform analytic bounds over the box, not values sampled along a proposed orbit.

Finally |sinh(2chi)/2| is at most [1/(1−1/50)−(1−1/50)]/4=99/9800<11/1000. Thus w'>−831/1000>−21/25 and w'<−99/1000<−9/100. All inequalities used by the candidate are valid conservative relaxations.

## 3. First-exit argument and the same continued interval

The initial state is strictly inside the box. On any initial interval before its first exit, b'=rho>0 and rho'=−rho g<0 give 1<=b<=1+(11/10)D=1011/1000 and rho<=1. The lower derivative bound rho'>=−(11/10)(8/5) gives rho>=1−(44/25)D=614/625=.9824. Also

w>=1/10000−(21/25)D=−83/10000,
w<=1/10000,
|chi|<=D/100=1/10000.

These remain strictly inside b,rho in[.9,1.1], |w|<=.01, |chi|<=.01 for all D<=.01. This contradicts a first exit on [0,.01]. The state stays in a compact subset of the smooth b>0,a>0 vector-field domain; phi is separately bounded by integrating g<1.6. Ordinary ODE continuation therefore supplies the entire regular IVP through D, rather than merely a conditional statement about a hypothetical trajectory. No vanishing-density or constitutive singularity is approached.

Because w'<−.09 throughout that interval, w decreases strictly and has at most one zero there. At X=1/10000 the lower bound gives w>=1/62500>0, whereas at X=1/800 the upper bound gives w<=−1/80000<0. Continuity supplies exactly one Dstar strictly between those endpoints. Therefore the **same** initial-data solution reaches D=.01 and D−Dstar>7/800=.00875. The strict length inequality uses the analytic open turn bracket; the script's arithmetic equality D−1/800=7/800 is not by itself a proof of strictness.

The interval family has induced wall fields, pressures and mass. Each member's perturbations preserve its own mass, but the total background mass changes when the chosen prefix length changes. This is not a fixed-right-boundary continuation problem or a moving-wall evolution. The asserted physical source balance remains B(Dphys)−B(0)=4piG integral rho_phys dx.

## 4. Full continuum energy, all fields and boundaries

With dimensionless rho'=-rho g, the original FGF023 Hessian is exactly

Q2=integral{rho(Xi'−gXi)²−2(rho Xi)'Psi
 +A Psi'^2−2q eta Psi'+eta'^2+m eta²}dX,
m=cosh(2chi)−2T+gq.

It is the full material-density constrained Hessian from the assumed action. At fixed mass, the constant chemical potential removes second-order density-path contributions; no local source force was artificially cancelled. Dirichlet Xi=Psi=eta=0 supplies the boundary cancellation

−2integral(rho Xi)'Psi=2integral rho Xi Psi'.

The associated quadratic energy flux retains the inherited field and fluid contributions, proportional to [(A Psi'−qeta)Psi_T+eta'eta_T−rho Xi_T(delta rho/rho+Psi)] at the walls. Fixed traces imply their time derivatives vanish; no flux boundary condition is imposed in addition to the field values. A non-Dirichlet/free-wall problem would require another argument.

The algebraic inequalities used in the candidate are exact:

(a−b)²>=a²/2−b²,
A z²+2h z>=A z²/2−2h²/A,
h²=(rhoXi−qeta)²<=2rho²Xi²+2q²eta².

They retain positive gradient coefficients for **all three** fields. Since rho>=.9, A>=.8 and m>=1−2(.82)=−.64, the Xi² negative coefficient is at most

(11/10)(8/5)²+4(11/10)²/(4/5)=4433/500=8.866,

and the eta² coefficient magnitude is at most

4(51/100)²/(4/5)+16/25=3881/2000=1.9405.

Thus Q2>=integral[.45 Xi'^2+.4 Psi'^2+eta'^2−9Xi²−2eta²], hence Q2>=(2/5)||u'||²−9||u||². No scale-gradient sign restriction or division by w remains. The bound therefore applies directly across and beyond the first turn. No Dirichlet rank-one term has been set to zero and neither dynamical field has been instantaneously eliminated.

Dirichlet Poincare and pi²>9 give

Q2>=35991||u||²,
Q2>=3999/10000 ||u'||².

These hold on the entire continuum H¹₀ interval, not only on a finite element space. The kinetic norm Mkin=integral(rhoXi²+Psi²+eta²)<=11/10||u||². For every nonzero admissible perturbation,

Q2/Mkin >=359910/11>32000.

Regular bounded coefficients and positive kinetic weights give the usual conservative longitudinal quadratic-form interpretation, with a strictly positive generalized squared-frequency infimum. The proof bounds the whole continuum form; it does not require identifying or computing individual eigenmodes. The finite length is short and the candidate explicitly does not claim to defeat the earlier sufficient shortness bound.

## 5. Rational certificate and negative controls

The root `check_certificate.py` uses Fraction arithmetic for every stored margin and constructs no ODE samples or spectral grid. Its checks reproduce the exponential envelopes, g/A/q/T bounds, inward box estimates, strict sign tests bracketing the turn, Young penalties and final rational constants. I inspected the script, completed results and manifest without rerunning it. The saved run completed in .024279 seconds with exit0, bounded at120 seconds wall and110 seconds per-process CPU, with cooperative one-thread environment and no memory limit claimed. Four input hashes and three output/log hashes currently match their recorded values. These provenance checks do not replace the analytic arguments above.

The D=1 mutant gives the formal lower-bound expression (2/5)*9−9=−27/5. It rejects this particular positive-gap certificate, and the short-box continuation proof also does not certify an orbit through D=1. Neither fact proves an unstable physical mode there.

At the actual initial Q state a=b=1, g=sqrt2, A=2sqrt2/3 and A²=8/9<1. This supplies the mathematical meaning of the script's initial A>=1 mutant check. It is a genuinely false coefficient bound, not evidence of negative kinetic energy or instability in the correctly bounded action.

The certificate's row labelled postturn extension >7/800 checks only the endpoint subtraction equality; strictness comes from the separately audited w sign and IVP-continuity proof. Likewise its exp and Poincare comparisons inherit their analytic inequalities rather than proving transcendental inequalities from an unrecorded approximation. This division of responsibility is stated correctly in the candidate.

## Scope and verdict matrix

| Obligation | Outcome |
|---|---|
| Q constitutive inverse, q and T bounds | Passed analytically |
| Uniform box inequalities and first-exit closure | Passed; full IVP throughD=.01 |
| Open first-turn bracket and same post-turn interval | Passed |
| Full Hessian, boundary cancellation and retained kinetics | Passed |
| Continuum Young/Poincare bound on allfields | Passed |
| Reference units and physical ar/Lr restoration | Passed for declared couplings |
| Root rational certificate arithmetic/provenance | Code/record reviewed; hashes match; not rerun |
| Negative controls as instability claims | Correctly not interpreted that way |
| RAR, M, filtered MONO or physical observations | Not certified by this construction |

The two registered ar values, 9.3619e−11 and1.1279e−10 m/s², label separate positive scaled families. Constant-vacuum reference and frozen ar=a0 E(z) comparisons remain distinct; no H(z) evolution is solved. The actual local a=ar exp chi varies and still does not satisfy the literal pointwise constant-vacuum interpretation. No choice of the arbitrary Lr or couplings is empirically selected. Physical metric/photon coupling, causal characteristics, three-dimensional/nonlinear stability and free boundaries remain outside this result.

The earned improvement is a quantitative analytic enclosure and continuum lower bound for one explicitly chosen Q slab reaching beyond its first scale-gradient turn. No counterexample or missing mathematical implication was found within that declared scope. It does not close the physical gravity theory.
