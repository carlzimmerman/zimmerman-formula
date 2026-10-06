# A covariant trajectory-stealth repair removes the clock kinetic crossings

A local scalar deformation can preserve the exact chosen radiation+dust background while raising its constrained clock kinetic coefficient above a strictly positive floor at every finite epoch and nonzero Fourier mode. The previously derived simple-zero pole mechanism then disappears: the full six-state linear equations have smooth coefficients through every formerly problematic crossing. The explicit construction is covariant but encodes one cosmic trajectory and breaks scalar shift symmetry. It does not preserve the original continuous vacuum-shift map, prove full gradient/nonlinear health, or establish the MOND source action and 32pi selector.

## Exact local deformation and first variations

Add to the retained scalar action

`Delta K(X,phi)=Z(phi)/2 [X-B(phi)]²`, `B(phi)=Xbar(phi)`.

X=-g^(mu nu)phi_mu phi_nu/2; Z and B are prescribed scalar functions, not external time functions or new dynamical fields. Let Y=X-B(phi). Along the chosen background, Y is identically zero. Direct differentiation gives

`Delta K_X=Z Y`,

`Delta K_phi=(Z_phi/2)Y²-Z Y B_phi`.

With natural units and phi of mass dimension1, X and B have dimension4, M dimension2, H_star dimension1, Z dimension-4 and lambda is dimensionless; the added Lagrangian has density dimension4.

Thus the value and both first derivatives vanish on the entire trajectory. The additional metric stress is `Delta T_mu_nu=Delta K_X phi_mu phi_nu+Delta K g_mu_nu`; its density `2X Delta K_X-Delta K` and pressure Delta K vanish exactly. The extra scalar equation is `nabla_mu(Delta K_X nabla^mu phi)+Delta K_phi`. Since Y vanishes as a function on the spacetime, its spacetime derivative also vanishes. Therefore this scalar equation vanishes identically, including the derivative of Delta K_X. Both Einstein and clock equations, not merely the background Lagrangian value, remain unchanged.

The mixed second derivatives are retained: on the trajectory `Delta K_XX=Z`, `Delta K_Xphi=-Z B_phi`, `Delta K_phiphi=Z B_phi²`. Omitting B_phi would give the wrong perturbation operator even though the value of the action vanishes on the background.

## An explicit smooth trajectory function

Use the actual tuned four-dimensional logKGB background of ../REPORT.md, with 0<eta=c/(3M H_star²)<1, positive dust and radiation, and 0<r_f<3/4. Normalize x=a_FRW/a_f and define

`j_hat=j_crit/a_f³=eta exp(eta/2-r_f/3)`.

The analytic monotone background h(x)>1 is fixed by

`L((h-1)/eta)+(eta/2)[(h-1)/eta-1]²`

`=d_f(x^-3-1)+r_f(x^-4-1)+3ln x`,

where L(u)=u-ln u-1 and d_f=1-4r_f/3. The existing background charge gives

`qbar(x)=q* x³[h(x)-1]/j_hat`,

`phibar(x)=phi_0+[q*/(H_star j_hat)] integral_0^x du u²[h(u)-1]/h(u)`.

The integrand is positive and converges at zero. Its derivative times xdot=H_star h x is exactly qbar, so phi is strictly monotone even if X is not. It maps finite positive x to an open clock interval (phi_0,infinity). Define B and hbar by

`B(phibar(x))=qbar(x)²/2`, `hbar(phibar(x))=h(x)`.

These are fixed smooth, locally analytic functions on that interval by the inverse-function theorem. The action evaluates them locally at phi. Their construction is a reconstruction from a specified trajectory, not an instruction to infer the cosmological scale factor nonlocally at runtime. The normalized x form makes the construction independent of the arbitrary scale-factor normalization. It nevertheless encodes the chosen eta, r_f, q*, H_star and clock origin. Those are substantive inputs, not newly selected outputs.

## Quadratic operator with all scalar reactions

Because the background and first variations vanish, the complete added quadratic action is

`Delta L_2/a_FRW³=Zbar/2 [delta X-B_phi delta phi]²`.

Along the trajectory B_phi=Xdot/qbar, so the bracket is precisely the gauge-invariant clock-surface observable `delta X_clock=delta X-(Xdot/qbar)delta phi`. In unitary clock gauge delta phi=0 and delta X=-qbar² nu; hence

`Delta L_2/a_FRW³=(Zbar qbar^4/2)nu²`,

`Delta Sigma=Zbar qbar^4/2=2Zbar Xbar²`.

This factor follows independently from `X Delta K_X+2X² Delta K_XX`. There is no new lapse temporal derivative, spatial lapse operator or shift term. Theta is unchanged because G is fixed and Delta K_X vanishes on the background. Z_phi and B_phi contributions are present in the invariant square and in its time-dependent coefficients; they have not been dropped by freezing the scalar background.

The full scalar+dust+radiation action of ../perturbations/REPORT.md is changed exactly by replacing Sigma with Sigma+Delta Sigma. Its lapse reaction, radiation normalization dot(v_r)-H v_r, both matter canonical pairs, and pressure/tadpole terms remain as derived there. In particular the shift still fixes

`nu=(M zetadot+rho_d v_d/2+R_r v_r/2)/Theta`.

The lapse equation still determines the shift through nonzero Theta. The full clock kinetic Schur coefficient is

`K_new=K_old+M² Delta Sigma/Theta²`,

with `K_old/M=[3eta(1+eta-h)+kappa(p/H_star)²]/(h-eta)²`.

For the regular radiation field the two-velocity determinant is `C_r K_new`; exact dust retains its canonical density pair. A positive K_new therefore repairs the constrained velocity-form sign and Legendre invertibility, not just a frozen-matter scalar coefficient.

## Positive explicit choice and disappearance of the finite-time pole

Choose a dimensionless constant

`lambda=1+3eta²/(1-eta)²`,

and prescribe

`Z(phibar(x))= [2M H_star²/qbar(x)^4] P(h(x))`,

`P(h)=lambda(h-eta)²+3eta(h-1-eta)`.

This is strictly positive for all h>1. Indeed `P(1)=(1-eta)²>0` and for delta=h-1>=0,

`P(1+delta)=(1-eta)²+[2lambda(1-eta)+3eta]delta+lambda delta²`.

Every coefficient is positive in the declared eta range. This smooth choice avoids a nonsmooth positive-part switch. It gives Delta Sigma=M H_star²P(h), and the exact cancellation is

`K_new=lambda M+kappa M p²/[H_star²(h-eta)²] >=lambda M>0`.

The formula is a nonzero-mode constrained coefficient; it does not derive the homogeneous k=0 gauge-sector constraints by taking a singular shift limit. One may choose larger lambda if desired, with no unique value selected. Neither this kinetic floor nor lambda selects A/H_star or 32pi.

On every compact finite-time interval of the chosen background, qbar, Theta and C_r are nonzero and smooth. K_new never vanishes. Replacing S=Sigma+kappa Mp² with S_new=Sigma+Delta Sigma+kappa Mp² in the existing six-state equations therefore gives an analytic first-order linear system with no kinetic-zero division. Its generic solutions have finite local analytic continuation through the old crossing times. This is a genuine repair of the previously proved clock-norm pole, rather than a special compatibility-amplitude selection. It does not exclude ordinary exponential growth or other stability problems of that regular system.

For eta=1/2, lambda=4. The bracket P is positive at h=1.1,1.5,10 and1000; the p=0 formal Schur limit is exactly4M at all of these states. In particular the original background fold and intermediate comoving crossings are no longer zeros of the new nonzero-mode coefficient.

## Physical costs, gradients and source matching

The early radiation asymptotics have h proportional to x^-2, qbar proportional to x, and phibar-phi_0 proportional to x³. Thus B scales as (phi-phi_0)^(2/3), while Z grows as x^-8. At every finite x the functions are smooth; no smooth extension to the excluded Big Bang clock endpoint is proved. This divergence by itself is not a demonstrated strong-coupling catastrophe: canonical normalization and nonlinear interactions would need a separate analysis. At the late selected vacuum Z tends to a finite positive constant and Delta Sigma tends to M H_star²(1-eta)² for the displayed lambda.

The deformation introduces no new bare spatial-gradient operator at quadratic order. The gravity-sector coefficient `F_S=(1/a_FRW)d[a_FRW M²/Theta]/dt-M` is unchanged, as are the original acceleration Hessian and tensor Einstein coefficient M. The reduced added term is `Delta Sigma[d zetadot+e_d v_d+e_r v_r]²`; besides the positive clock velocity contribution, it changes one-derivative matter couplings and their quadratic potentials. Positive kinetic Schur data do not certify full finite-p gradient/potential stability or a nonlinear cutoff. The exact regular six-state evolution, radiation acoustic response, dust growth and interaction/strong-coupling scales remain to be computed for this new action.

It is also not source-stealth. On a galaxy solution one has no reason for X=B(phi). The extra stress and scalar equation generally react to lapse, clock flow and formation state. Around a homogeneous clock, `Delta rho_phi=-Zbar qbar^4 nu` at first order; this already changes the lapse/source equation. The absence of a direct matter coupling does not make the change invisible to minimally coupled matter, whose force follows the changed metric. The nonlinear MOND law, physical Newton normalization, cold source matching and outer boundary data must be rederived in this same action. They cannot be pooled from the old galaxy action.

The new explicit phi dependence breaks shift symmetry. On the selected background the added equation vanishes, so the old conserved-charge relation remains true for that solution. For neighboring histories and inhomogeneous fields the old shift current need not be conserved; the operator does not dynamically demonstrate creation of the tuned charge, nor preserve the whole original family of dust/radiation histories. Diffeomorphism covariance and on-shell total stress conservation remain intact, and minimally coupled ordinary matter remains separately conserved.

## Limited obstructions: pure shift-symmetric K and the old vacuum map

For a pure shift-symmetric Delta K(X) with G fixed, exact stress-stealth on the same positive-X background forces Delta p=Delta K=0 and Delta rho=2X Delta K_X-Delta K=0. If the history visits an open X interval, Delta K vanishes on that interval. C² regularity then gives Delta K_X=Delta K_XX=0 there, so it cannot change Sigma. The radiation history does visit an open X range near its early limit. A deformation stealth only at one constant-X vacuum can have nonzero Hessian; that exception is not the evolving history. Coordinated changes in K and G, higher-derivative covariant operators, different matter couplings and different background-stress cancellations are outside this pure-K obstruction.

Within the squared ansatz, preserving the original continuous vacuum-rescaling map with fixed couplings is a separate restrictive requirement. Let the map be phi-phi_0 -> s(phi-phi_0), X->s²X, with s=exp[-Delta rho_v/(2c)] and unchanged metric. Comparing coefficients of X² and X in the deformed action requires

`Z(phi_0+s psi)=s^-4 Z(phi_0+psi)`,

`B(phi_0+s psi)=s² B(phi_0+psi)`.

For all positive s these imply B=b0 psi² and Z=z0 psi^-4 on the clock interval. But the chosen early trajectory has B proportional to psi^(2/3), not psi². Thus this designer square cannot be both stealth on that radiation history and invariant under the original continuous vacuum map. Retuning B and Z after a vacuum change would change the action; it is not self-adjustment of fixed couplings. This conclusion excludes that specified map within this ansatz, not every possible self-adjustment branch or every local covariant completion.

## Evidence and remaining arrow

The construction supplies an exact background-preserving kinetic and linear-continuation repair. Its missing arrow is a physical completion that keeps the required vacuum response, nonlinear galaxy law and cosmological transfer while explaining the new functions rather than encoding the desired history. The original32pi question remains open.

checks.py independently verifies the covariant first and second variations, scalar-current derivative on the trajectory, Einstein stress, mixed scalar derivatives, exact positive polynomial and Schur cancellation, radiation kinetic determinant, early endpoint scaling, vacuum-map coefficient constraints and pure-K stress obstruction. Controls use a wrong half factor, freeze Xbar despite a varying trajectory, or impose the vacuum-map homogeneous power on the radiation trajectory. SOURCES.md records retained primary-source conventions and the limited theorem scopes. REPORT.md is not an execution input. No parent inputs or peer notes were modified.


Authoritative run main_a passes all27 checks. The wrong-half, frozen-profile and vacuum-homogeneous controls reject their intended altered interpretations. All four standard manifests validate against current input and output hashes. Recorded wall-time, CPU-time and numerical-thread limits bound the executions; unsupported address-space limits were not requested. Development preflights are not authoritative evidence. The independent proof review reconstructs the full variations, normalization and constrained repair without relying on check counts.
