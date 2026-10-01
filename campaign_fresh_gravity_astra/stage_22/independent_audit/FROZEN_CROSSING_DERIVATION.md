# Independent FGF035 coupled zero-flux crossing derivation

Auditor /root/metric_intake. Derived from task035 and pinned original Q scale/fluid action before reading any new author or root proof or receiving a preview. Fix C=4piG, a=a_ref exp(chi)>0, J>0, cs²>0, U=S0(cosh(2chi)-1)/4. Physical a_ref is time independent in this pass. The task prescribes at x=0 the signed MOND flux B=0, rho=rho_*>0, finite chi_*,w_*,phi_*.

## Signed constitutive law and equations

For a real scalar gradient g=phi', the flux is B=sgn(g)b(|g|;a), with b(v;a)=(sqrt(a²+4v²)-a)/2. Thus

 g=G(B,chi)=sgn(B)sqrt(B²+a|B|), G(0,chi)=0.

The static action gives B'=C rho and J chi''=U'(chi)-T(|g|,a); T=-a W_a is even in the signed gradient, nonnegative and zero at g=0. Matter hydrostatic balance is rho'=-rho g/cs², with the signed g, not its magnitude. On the negative side the matter gradient therefore has the opposite sign to the positive side. Physical acceleration is -g.

## B-coordinate existence and uniqueness

Since B'=C rho>0 locally, use B as the independent coordinate. Chain rule gives

 x_B=1/(C rho), rho_B=-G/(C cs²),
 chi_B=w/(C rho), w_B=(U'-T(|G|,a))/(JC rho),
 phi_B=G/(C rho).

Here G is only Holder1/2 in the independent variable B at0, but is locally Lipschitz in state chi uniformly for small B: its chi derivative away from0 is sgn(B)a|B|/[2sqrt(B²+a|B|)], of order sqrt(|B|), continuously extending to0. On a compact state neighborhood with rho bounded below and chi bounded, all remaining denominators and state derivatives are bounded. The T composition is likewise continuous in B and locally Lipschitz in chi; near0, T(|G|,a) is of order |B|^(3/2), and its state derivative is bounded. U is smooth. The nonautonomous RHS is therefore continuous in B and uniformly locally Lipschitz in all states.

The elementary local IVP theorem gives a unique C1 solution of this system on both sides of B=0, with rho>rho_*/2 after shrinking the interval. x_B>0 reconstructs a unique monotone C1 inverse B(x) through0. All spatial equations follow by chain rule; no undefined derivative of G with respect to B at0 is needed for these first-order equations. Uniqueness is claimed in the corresponding regular weak/flux class with positive continuous density and continuous first field variables, not for arbitrary singular or measure-valued solutions. No arbitrary endpoint data or total mass is prescribed; the local solution induces its walls and mass.

## Actual local regularity and energy

Set k=sqrt(a_* C rho_*)>0, a_*=a_ref exp(chi_*). Since B(x)=C rho_* x+o(x), a(x)=a_*+O(x), the actual signed gradient has leading behavior

 g(x)=k sgn(x)sqrt(|x|)+o(sqrt(|x|)).

Using hydrostatic balance and chi' continuous sharpens this to g=k sgn(x)sqrt(|x|)+O(|x|^(3/2)). Consequently

 phi(x)=phi_*+(2k/3)|x|^(3/2)+O(|x|^(5/2)),
 rho(x)=rho_*[1-(2k/(3cs²))|x|^(3/2)+O(|x|^(5/2))].

The density expression can also be checked exactly from rho=rho_* exp[-(phi-phi_*)/cs²]. In particular rho has a local maximum and phi a local minimum at the crossing.

Away from0, differentiating the exact constitutive relation gives

 g'=[(2|B|+a)/(2sqrt(B²+a|B|))] C rho
       +[sgn(B)|B|/(2sqrt(B²+a|B|))] a',

so g'=k/(2sqrt(|x|))+O(sqrt(|x|)). Thus phi is C^{1,1/2} and W^{2,p} locally for1<=p<2, but is not H2 across0 because |phi''|² has a logarithmically divergent integral. The same calculation yields rho''=-rho_* k/(2cs² sqrt(|x|))+O(sqrt(|x|)), so rho is C^{1,1/2} and W^{2,p} forp<2 but not H2 either. B'=C rho implies B is C^{2,1/2}.

T(|g|,a)~|g|³/(3a)=k³|x|^(3/2)/(3a_*), and its exact chain derivative extends continuously as0 at the crossing; it is C^{1,1/2} locally. The scale equation therefore gives chi at least C^{3,1/2} and w=chi' at least C^{2,1/2}. In particular chi''(0)=U'(chi_*)/J and chi'''(0)=U''(chi_*)w_*/J. No differentiability of g at0 is assumed.

There is no delta source: B is continuously differentiable with B'=C rho pointwise, and w is continuous, so neither flux nor scale gradient has a jump. The singular phi'' is locally integrable and is not the MOND source; replacing B' by phi'' would change the theory. The inherited static energy density is locally integrable: W(|g|;a)~k³|x|^(3/2)/(3a_*), while rho phi, the isothermal internal energy, J w²/2 and U are continuous and finite. This is finite local energy, not a global lower-bound or stability theorem.

## Full Hessian and failure of standard H1 coercivity

For smooth compact perturbations xi,psi,eta, set r=-(rho xi)', A=b_v(|g|)=2|g|/sqrt(a²+4g²), q=T_v(|g|), s=T_chi at fixed |g|, and m=U''-s. The actual mixed sign is

 Q=integral[cs²r²/rho+2r psi+
   (A psi'²-2 sgn(g)q eta psi'+J eta'²+m eta²)/C]dx.

The signed coefficient sgn(g)q tends to0 at the crossing. All coefficients are bounded; the smooth-variation second variation defines a continuous quadratic form on H1_0 triples. This does not assert a C2 nonlinear functional calculus on bare H1 or the positive-gradient H2 inverse theorem. The original mass representation remains meaningful because rho is positive C1 with bounded rho'. The terms shown are retained for general perturbations.

To disprove standard full H1 coercivity it suffices to use xi=eta=0. Then Q=integral A psi'²/C>=0. Near0, A~(2k/a_*)sqrt(|x|). For nonzero f in C_c^infinity(-1,1), let psi_epsilon(x)=sqrt(epsilon) f(x/epsilon), supported inside the crossing patch. Its derivative L2 norm is the fixed positive norm of f', its L2 norm tends to0 like epsilon, while Q is O(sqrt(epsilon)) and tends to0. No constant c>0 can satisfy Q>=c||(xi,psi,eta)||_H1² for all such perturbations.

This is failure of a specific norm lower bound. The exhibited energies are nonnegative, not unstable directions. Their L2 kinetic size also shrinks, so this sequence alone does not produce a zero squared-frequency limit. It proves neither negative energy, nonlinear instability, ghost, PDE ill-posedness nor failure of every weighted space. The base phi is not H2 and the standard H1-coercivity gate fails, so the FGF034 positive-gradient branch/inverse proof cannot simply be used across this crossing, even though the static crossing itself exists.

Q is the only law derived here. RAR transfer remains open, and no M action is imported. Both a0 reference choices remain separate positive constants; frozen H comparisons and evolving H prescriptions are distinct. The responsive local scale is the inherited added diagnostic premise, not a literal scale-vacuum identity or a conserved physical vacuum sector. No fixed-wall family, autonomous physical V, metric/photon/DOF result, instrument calibration, historical novelty or physical theory closure follows. No numerical computation executed.
