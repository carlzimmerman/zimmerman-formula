# FGF038: an exact coupled lower bound on capped finite-action Q states

Proof-only worker derivation fixed before reading any new root/auditor proof.
This changes the failed FGF037 upper/Taylor question to a reverse lower bound.
No numerical run, fitted coefficient, new physical potential or mechanism.

## 1. Background, admissible finite states and exact cancellation

Restrict the SAME FGF035 central solution to I_d=(-d,d), length ell=2d.
Keep physical coefficients C=4piG, cs²,J,S0>0 and the positive reference fixed.
Write g=phi', a=a_ref exp(chi), B=sgn(g)b(|g|,a),
b(s,a)=(sqrt(a²+4s²)−a)/2, W_s=b, T=−a W_a.
The background obeys

 B'=C rho, cs²rho'=−rho g, J chi''=U'−T,
 U=S0[cosh(2chi)−1]/4.

It has rho bounded positive, a bounded positive, A=b_s(|g|,a) comparable
to sqrt(|x|) near the center, and integral1/A finite. Its induced endpoints
and mass are fixed once d is selected. They generally change if d is changed;
this is a sufficient-shortness family, not a fixed-mass family across d.

Admissible Eulerian perturbations are measurable r with integral r=0 and
|r|<=rho/2 almost everywhere, psi in ordinary H1_0(I_d), eta in H1_0(I_d)
with ||eta||infinity<=1/4. The new density is rho+r, potential phi+psi and
scale a exp(eta), corresponding to chi+eta. Density is positive and scale
stays bounded above/below. The exact action is finite: Q energy has at most
quadratic gradient growth; all other terms are integrable under these caps.
No exact nonlinear displacement map r=−(rho xi)' is assumed. Perturbed states
need not themselves be equilibria; they are admissible energy comparisons.

Let e(rho)=cs²rho[log(rho/rho_ref)−1] and define

 H_r=e(rho+r)−e(rho)−e'(rho)r,
 U_rel=U(chi+eta)−U(chi)−U'(chi)eta,
 F_rel=W(|g+psi'|,a exp eta)−W(|g|,a)−B psi'+T eta.

Direct expansion of the FULL static energy gives the exact identity

 Delta E=integral[H_r+r psi]dx
            +(1/C)integral[F_rel+J eta'²/2+U_rel]dx. (1)

All first variations were canceled, not omitted. Hydrostatic balance makes
e'(rho)+phi a constant, so its integral against r is zero. Fixed phi walls and
B'=C rho give integral(B psi'/C+rho psi)=0. Fixed scale walls and its actual
equation give integral[J chi' eta'+(U'−T)eta]=0. These integrations remain
valid across the crossing: B is C1, chi sufficiently regular and the tests
have zero outer traces. There is no center boundary term or delta source.
The coupling r psi and the finite scale change remain in (1).

## 2. A global scalar Q inequality, including sign reversal

For fixed a>0 define the even signed-gradient function V_a(y)=W(|y|,a).
It is C2, V_a'(g)=sgn(g)b(|g|,a), and

 V_a''(y)=A(|y|,a)=2|y|/sqrt(a²+4y²).

A(s,a) is increasing for s>=0, and A(s/2,a)>=A(s,a)/2.
For every signed g and signed increment z,

 V_a(g+z)−V_a(g)−V_a'(g)z
       =z² integral_0^1(1−t)A(|g+t z|,a)dt
       >=c_* A(|g|,a)z², c_*=1/64.                 (2)

Here is a global elementary proof. For g=0 the right side is zero and
convexity proves the inequality; for z=0 both sides vanish. Otherwise:
if |z|<=2|g|, use t in [0,1/4], where |g+t z|>=|g|/2.
Its integral of1−t is7/32, yielding at least7A(|g|)/64.
If |z|>2|g|, use t in [3/4,1], where the reverse triangle inequality gives
|g+t z|>|g|/2. Its integral of1−t is1/32, yielding A(|g|)/64.
This proves the claimed conservative universal constant. It is not claimed
sharp. Opposite signs, crossing zero inside the segment, exact reversal and
arbitrarily large |z| are all covered; no deep-MOND truncation is used.

## 3. Finite scale response, without a small-gradient assumption

Set cap e0=1/4 and k=c_* exp(−e0)>0, fixed universally. For each background
point put

 q(s,a)=s A(s,a)−b(s,a)=a b(s,a)/(2b(s,a)+a),
 D(s,a)=T_chi(s,a)=2T(s,a)−s q(s,a),
 qhat(x)=sup_(|theta|<=e0) q(|g(x)|,a(x)exp theta),
 Dhat(x)=sup_(|theta|<=e0) |D(|g(x)|,a(x)exp theta)|.

For fixed signed g, the scale derivative of signed flux is
partial_theta[sgn(g)b(|g|,a exp theta)]=−sgn(g)q(|g|,a exp theta).
Also A(|g|,a exp eta)>=exp(−e0)A(|g|,a). Decompose F_rel exactly at the
NEW scale a exp eta:

 F_rel = {V_(a exp eta)(g+z)−V_(a exp eta)(g)
                               −V_(a exp eta)'(g)z}
        +{V_(a exp eta)'(g)−V_a'(g)}z
        +{V_(a exp eta)(g)−V_a(g)+T(|g|,a)eta}, z=psi'.

The first brace is at least k A z² by (2). The second has absolute value
at most qhat|eta z|. The third is the exact scale Taylor remainder at the
FIXED BACKGROUND gradient, not at g+z; its second theta derivative is −D,
so it is bounded below by −Dhat eta²/2. Therefore

 F_rel>=k A z²−qhat|eta z|−Dhat eta²/2
       >=(k/2)A z²−R(x)eta²,
 R(x)=qhat²/(2k A)+Dhat/2.                           (3)

The last step is elementary Young inequality. At x=0 set the quotient to0:
g=0 implies qhat=Dhat=0; the original first brace is nonnegative, so the
inequality is still valid. No division at the zero point is required.

These background remainder coefficients are uniformly small upon shortening.
For Q at s tending to0 with a in a fixed compact positive interval,

 b=s²/a+O(s4), q=s²/a+O(s4), T=s³/(3a)+O(s5),
 D=−s³/(3a)+O(s5).

The omitted coefficients depend boundedly on powers of a inverse. The expansions
are uniform also for a exp theta with |theta|<=e0. Thus qhat=O(g²),
Dhat=O(|g|³), and qhat²/A=O(|g|³)=O(|x|^(3/2)). Hence
R is continuous after extension by0, and Rmax=O(d^(3/2)). This uses only the
BACKGROUND deep behavior to bound its coefficients, not a restriction on the
new gradient g+z. Arbitrarily large finite-action z remains admissible.

For the scale potential, U''=S0 cosh(2chi)>=S0 globally, so exactly

 U_rel>=S0 eta²/2.                                  (4)

No actual equilibrium potential V is introduced or fitted.

## 4. Entropy curvature and the full coupled bound

The exact density remainder is

 H_r=cs² r² integral_0^1(1−t)/(rho+t r) dt
                     >=cs²r²/(3rho),               (5)

because |r|<=rho/2 implies rho+t r<=3rho/2. In particular the density cap
supplies a uniform lower curvature, not an uncontrolled entropy expansion.
Put

 E_r=integral cs²r²/rho,
 E_p=(1/C)integral A psi'²,
 E_eta=(J/C)integral eta'²,
 I_A=integral_I_d 1/A.

Weighted endpoint Cauchy-Schwarz yields ||psi||_2²<=ell I_A integral A psi'².
Since ordinary H1_0 is included in this weighted space, it applies to every
admissible psi. Young inequality gives the retained density-potential coupling

 |integral r psi|<=E_r/6+(3/2)integral(rho/cs²)psi²
                       <=E_r/6+alpha E_p,
 alpha=3C rho_max ell I_A/(2cs²).                    (6)

The scale remainder in (3) is absorbed with the ordinary endpoint estimate
||eta||_2²<=ell²||eta'||_2². Combining (1),(3)-(6) gives

 Delta E>=E_r/6+(k/2−alpha)E_p
                    +(1/2−beta)E_eta+(S0/(2C))integral eta²,
 beta=ell² Rmax/J.                                  (7)

The exact sufficient gates are

 alpha<=k/4, beta<=1/4,
 k=exp(−1/4)/64.                                    (8)

Under them the requested uniform lower bound is

 Delta E>=E_r/6+(k/4)E_p+E_eta/4
                               +(S0/(2C))integral eta². (9)

Both gates hold on all sufficiently short restrictions of the SAME central
solution: rho extrema remain positive and bounded, I_A=O(sqrt(d)), so
alpha=O(d^(3/2)); Rmax=O(d^(3/2)), so beta=O(d^(7/2)). No physical radius or
numerical margin is claimed. The constants1/6,k/4,1/4 are independent of the
admissible r,psi,eta once the background interval satisfies (8). The cap1/4
was not adjusted per perturbation, and no bound on psi' supremum was added.

All distances in (9) are nonnegative. If Delta E=0, then r=0, eta=0 and
psi'=0 almost everywhere away from the single zero of A. Since psi is H1_0,
this implies psi=0. Thus the background is a strict energetic minimum on the
stated capped finite-action class. This is a restricted nonlinear STATIC
energy statement, with a quantitative lower distance bound, not a dynamical
stability theorem. Perturbed profiles are not asserted to satisfy the field
or hydrostatic equations; the comparison is on the admissible energy class.

## 5. Controls and the exact surviving distinction

- At eta=0 the scalar bound (2) remains global in signed z, including z=−2g
  and arbitrarily large gradients; no same-sign restriction is hidden.
- At g=0 its RHS is zero but the exact field increment is nonnegative.
- At r=0,eta=0, (9) is compatible with the FGF037 concentrating smooth bumps:
  their exact positive energy may diverge while E_p tends to zero. A lower
  bound supplies no upper bound or continuity in the weighted topology.
- FGF037's singular weighted directions remain outside the finite-action
  H1 class and retain infinite energy at nonzero amplitude. They are not
  silently included by extending (9) as a finite nonlinear Taylor theorem.
- Density and scale caps are assumptions on comparison states. Their
  preservation by an evolution is NOT proved. The proof does not use
  r=−(rho xi)' as an exact finite material-displacement formula.
- The mixed r psi and scale flux-change terms are both retained and absorbed.
  Positivity of the scalar brace alone would not have established (9).

The earlier weighted linear operator and evolution remain separate results.
Even combining them with (9) does not prove nonlinear Cauchy existence,
conservation on nonlinear solutions, invariant caps or a nonlinear response
map through the cusp. Such dynamical conclusions need their own hypotheses
and proof. The previous upper/Taylor route remains refuted.

## 6. Units, branches and limitations

W has acceleration-squared units and W/C is energy density; integrated
Delta E,E_r,E_p,E_eta are energies per transverse area. A is dimensionless,
q has acceleration units, D,R have acceleration-squared units, and both
alpha,beta are dimensionless. All physical reference units and coefficients
are held fixed under perturbation and under the sufficient-shortness argument.

Use a_ref=9.3619e-11 and1.1279e-10 m/s² separately; each gives its own
background and small-interval gate. Frozen-H choices a_ref=a(0)E(z),
E²=.315(1+z)^3+.685, are separate stationary hypotheses, not the actual
evolving-H action or literal constant-vacuum actual-scale relation. An evolving
reference retains an exchange/reservoir obligation absent from this static
comparison. The spatially responsive scale is an explicit diagnostic premise.

The source remains signed MOND Q flux B'=C rho. No Newtonian missing mass,
RAR transfer, registered M action, physical V, imported mechanism, historical
novelty, calibrated empirical fit, filtered-MONO/metric/photon/DOF or theory
closure follows. The exact new result is a restricted coupled energetic lower
bound on finite-action capped states. Further dynamical/physical claims require
an independently justified target and evolution, not another parameter sweep.
