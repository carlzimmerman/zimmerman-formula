# The finite-k rank point is a velocity-chart failure

The exact quadratic radiation/shear action has a regular four-dimensional canonical phase space at every k>0 with A,B,D,Gamma,g,j>0. Its primary and secondary auxiliary constraints are second class with nonzero determinant. The zero of the previously reduced Lagrangian auxiliary determinant is not a singularity of this canonical system and does not introduce a new gauge or remove a physical mode. This resolves the rank-point question at the inherited quadratic level. It does not prove stability, full nonlinear admission or health; the parent ultraviolet gradient instability remains.

## Frozen action and assumptions

Use precisely section 3 of the parent radiation report, including its time-boundary convention, after the already varied shifts/relative-shear rows and common gauge choice. The coefficients may be arbitrary smooth functions of time on a compact interval, with the stated strict positivity. Keep general Gamma>0; ell and e are real finite rates. The physical arithmetic radiation branch has e>0. Define Tw=w_dot−e w and Y=chi_dot+e w. The raw remaining action is

L=A(Tw−n_g)²+B n_g²+D n_h²+2g(u+chi)n_g+2j u n_h
  +Gamma(Y−ell u+n_g−n_h)²−g e w².

u,n_g,n_h are auxiliary coordinates without time derivatives. No old eta=0 clock condition or second spatial gauge has been inserted. This audit is n=3 in its physical fixture, but its algebra treats these six coefficients abstractly. It is not a uniform higher-dimensional covariant result.

## Legendre transform before auxiliary elimination

p_w=2A(Tw−n_g), p_chi=2Gamma(Y−ell u+n_g−n_h),
w_dot=p_w/(2A)+n_g+e w,
chi_dot=p_chi/(2Gamma)+ell u−n_g+n_h−e w.

Let a_c=p_w−p_chi−2g chi and
H_base=p_w²/(4A)+p_chi²/(4Gamma)+e w(p_w−p_chi)+g e w².
The raw Hamiltonian is

H_raw=H_base+a_c n_g+p_chi n_h+ell p_chi u
      −B n_g²−D n_h²−2g u n_g−2j u n_h.

Its auxiliary stationary matrix is C_H=[[B,0,g],[0,D,j],[g,j,0]], with determinant −(B j²+D g²) strictly negative. It is independent of the velocity-chart determinant. Thus every canonical phase point has a unique auxiliary solution:

S=g²/B+j²/D>0,
Z=g a_c/B+j p_chi/D−ell p_chi,
u=Z/(2S),
n_g=(a_c−2g u)/(2B), n_h=(p_chi−2j u)/(2D).

Substitution gives the actual remaining phase Hamiltonian

H_red=H_base+a_c²/(4B)+p_chi²/(4D)−Z²/(4S).

This is a rational polynomial in the four canonical coordinates (w,chi,p_w,p_chi), with only strictly positive A,B,D,Gamma,S denominators. Its canonical equations are smooth even where the velocity-based auxiliary chart fails. Time dependence of the boundary convention supplies the displayed e term; another legitimate time-dependent boundary/canonical transformation changes the Hamiltonian’s instantaneous coefficients, not this regularity result.

## Dirac constraints and physical count

Let P_aux be the three auxiliary canonical momenta and s_aux=partial H_raw/partial(n_g,n_h,u). The six constraints P_aux=0,s_aux=0 have bracket matrix

D_Dirac=[[0,−H_auxaux],[H_auxaux,Omega]], H_auxaux=−2C_H,
Omega=[[0,−2g,−2g ell],[2g,0,0],[2g ell,0,0]].

Omega is the actual secondary-secondary Poisson block; it must not be omitted even though it does not change the determinant. The determinant is 64(B j²+D g²)²>0. With ten original phase coordinates and six second-class constraints, four remain: two physical scalar canonical pairs. There is no additional gauge constraint at the velocity-chart rank point. Since the primary constraints set P_aux=0, the pullback symplectic form on the remaining coordinates is the standard dp_w wedge dw+dp_chi wedge dchi, even though the auxiliary solution depends on them. Preservation fixes the auxiliary multipliers; it adds no tertiary constraint in this regular block.

## Relation to the earlier Lagrangian rank loss

The parent velocity-auxiliary matrix, ordered (n_g,n_h,u), is

C_L=[[A+B+Gamma,−Gamma,g−Gamma ell],
     [−Gamma,D+Gamma,j+Gamma ell],
     [g−Gamma ell,j+Gamma ell,Gamma ell²]].

Direct differentiation of H_red gives

det(H_red,pp)=−det C_L/[4A Gamma(B j²+D g²)].

At det C_L=0 the Hamiltonian momentum Hessian loses rank: velocities do not form valid independent coordinates for an ordinary second-order Lagrangian chart. The full phase evolution and the Dirac constraint determinant stay regular. A first-order Hamiltonian system needs no invertible momentum Hessian. Consequently the previous use of C_L inverse was a chart restriction, not evidence of an actual quadratic singularity.

This is not a stability result. In the ell!=0 infrared range det C_L>0 gives an indefinite instantaneous momentum form, while high k gives a positive kinetic Lagrangian block. For the actual radiation e>0, the pure coordinate potential is g e w²+g²j² chi²/(B j²+D g²)>0; phase cross terms remain. Under a time-independent canonical change, indefiniteness of the same quadratic Hamiltonian is preserved, but labeling one negative momentum coefficient a physical ghost is not invariant under exchanging coordinates and momenta. A time-dependent cosmological quadratic Hamiltonian also has no assumed conserved energy. A canonical mode/adiabatic/UV analysis remains necessary for physical health. The already established parent high-k negative spatial stiffness is separate and is not repaired by this calculation.

## Bounded rank-crossing discriminant

Use a single admitted instantaneous radiation fixture M=a=h=1, H=2, L=1/8, b=2, H2=1/8, eta=1/4, rho/M=9, W=12, e=3, ell=45/8. Then A=18,B=36,D=9,g=2p,j=p/32,Gamma=5p/16 with p=P_g. It is a different admitted radiation normalization from the parent’s H=sqrt(2) example, not a relabeling of it. One may choose q0 accordingly and the integration origin for b³; all Friedmann/number relations are satisfied.

det C_L=−p(21125p²−348912p−78732000)/16384.
Its positive root is p*=69.8631229678. Exact arithmetic verifies det H_pp=0 there; the canonical auxiliary determinant stays nonzero. Three bounded samples p*(1−10^-5),p*,p*(1+10^-5) evaluate the finite 4x4 phase matrix J Hess(H_red), with relative matrix change about2.0e−5 across the samples. At the center its frozen instantaneous eigenvalues are approximately ±5.37335 and ±3.78022i, all finite. These eigenvalues are only a discriminant of absence of a chart-induced divergence. Coefficients actually evolve on the radiation background; no physical growth rate, adiabatic mode or all-wavelength stability conclusion is inferred from freezing this fixture.

## Reproducibility and remaining arrow

checks.py reconstructs momenta, raw Legendre transform, all auxiliary rows, full Dirac block/determinant, reduced Hamiltonian and envelope equations, the relation to the Lagrangian determinant, positive coordinate potential and exact fixture root. The two controls change the reduced square’s sign or assert that the physical canonical constraint determinant vanishes at the velocity-chart root. Both are genuinely discriminated by these identities. The bounded phase samples do not prove the general regularity: strict positivity of S and the exact constraint determinant do.

Initial development preflight22/22 omitted Omega from the written Dirac matrix while obtaining the unchanged determinant; its original script and result are preserved. The corrected actual Omega block adds its own check, preflight23/23. Fresh standard records, not development preflights, are authoritative. This package does not identify a cold source, repair the arithmetic operator, select a0/32pi or establish full nonlinear DOF/health. The first unresolved physical arrow is the actual time-dependent canonical mode and cutoff interpretation; the rank-point obstruction alone is now resolved.
