# All angular static sectors of the joined critical body

VC4-ANGULAR-001. 15 October 2026. Candidate analytic theorem, awaiting an
independent audit of the new shape derivatives. This is an extension of the
pinned joined two-fluid Newtonian comparison model, not of an Einstein theory.
The requested starting revision is a553a4a663d393f29ec5da69c8cae68c164bb5b0;
the actual immutable input copies and observed checkout revision are recorded
in `inputs/source_manifest.json`. No earlier proof is amended.

**New result.** In the actual spherical equilibrium of `inputs/CRITICAL_PROOF.md`,
every angular sector l>=2 has a positive static constrained density/shape
Hessian, with the explicit bound (16) below. Both fluids vary independently,
the common finite-density boundary moves, its entire area rest mass gravitates,
and the electric field and exterior Maxwell phase vary. The l=1 kernel is
exactly translation, apart from fluid relabelings. There are additional static
vortical/relabeling nulls in all angular sectors. Thus strict positivity on all
material displacement fields would be false. Adding the previously proved
radial result gives static nonnegativity modulo those symmetries. No angular
initial-boundary evolution, hyperbolicity or radiation theorem is asserted.

## 1. Exact objects and admissible tangents

Use the frozen scales R=D0=rho_b0=1, c=100, G=10^-8,
f=rho_c0=1341/250, Kc=1/100, Kb=f(1+f)/100 and
zeta^2=4piG. Let Omega be the unit ball. The actual profiles rho_a(r),
fields D(r), E(r), masses M_a and selected tension sigma are those of the
frozen fixed-point and wall-root construction. Set rho=rho_b+rho_c,
M=M_b+M_c and s=sigma/c^2; s is the wall's mass per actual area.

The static energy is

    integral_Omega sum K_a rho_a^2 + W_ff + W_fw + W_ww
      + W_e[rho_c,Omega] + sigma Area(boundary Omega),                 (1)

where W_ff is the complete Newtonian self/cross energy of the two fluid rest
densities, W_fw is their interaction with mass s dA on the actual wall,
W_ww is that wall's self-energy, and W_e is the minimum of
integral_Omega H_in(D)+integral_out |D|^2/2 subject to the actual Gauss law
and no free surface charge. Minimization is only over the electric field,
not either density or the shape. Convexity H_in,DD>0 makes this the
ordinary static electrostatic reduction. An arbitrary extra admissible
Gauss-field tangent adds its nonnegative convex quadratic remainder.
The separately conserved masses M_b,M_c are the constraints. Wall area mass
is variable and is not an additional conserved particle stock.

Take one real spherical harmonic Y=Y_lm normalized by integral_S2 Y^2=1.
Write L=l(l+1). The common wall is r=1+epsilon hY+O(epsilon^2), and the
interior Eulerian density tangents are eta_a(r)Y. Define

    S=sum_a integral_0^1 eta_a^2 r^2 dr,
    eta=eta_b+eta_c, rho_R=rho(1),
    U=integral_0^1 eta(r) r^(l+2) dr.

Both distributions contain their actual moving-edge terms:

    delta(rho_a 1_Omega)=eta_a Y 1_Omega +rho_a(1) hY delta_boundary.    (2)

For l>=1 the first mass constraints hold automatically. Every smooth such
tangent is realizable by separately conserved material maps with common
normal trace hY: solve div(rho_a xi_a)=-eta_aY with xi_a.n=hY. The usual
Neumann compatibility is precisely the first mass constraint; a direct
construction is the Neumann Poisson solution for rho_a xi_a. Its tangential
boundary component is immaterial to the first physical configuration.
Second-order maps can enforce the two exact masses and the shared shape;
chemical multipliers remove their acceleration-dependent terms from the
Hessian. This specifies all angular compressional and relative species
directions, not a homology or locked-fluid restriction.

Two displacements represent the same static tangent when their difference
satisfies div(rho_a z_a)=0 and z_a.n=0. These include toroidal modes. They
are retained static nulls; a moving vortical current can still have positive
kinetic energy.

## 2. The moving-phase electric Hessian

At the material edge let D=D(1), Delta=E(1)-D=D^2/(1-D)>0. Let d be the
linear electrostatic Gauss-field perturbation, with radial harmonic traces
d_- inside and d_+ outside. The complete finite-density Gauss jump is

    d_+-d_-=zeta rho_c(1) h,
    D'_-=zeta rho_c(1)-2D.                                            (3)

Let A=H_in,DD, whose radial and transverse eigenvalues are respectively
(1-x)^-2 and (1-x)^-1. Put

    F_e=integral_Omega d.A.d +integral_out |d|^2.

The second variation of the electrostatic energy, after combining the
chemical first-integral terms with the two material energies, contributes

    F_e + Delta h(d_++d_-) +Delta D'_- h^2,                            (4)

in addition to the material surface term specified in section 3. In
particular it is not merely the positive bulk electric square.

Here is a derivation that fixes the trace and phase signs. Choose electric
potential phi with E=-grad phi. The minimized electric first variation is

    zeta integral_Omega phi eta_c
      + integral_boundary [zeta phi rho_c+Delta H] h,

where Delta H=H_in(D)-D^2/2. The material potential phi is continuous on
the actual interface. Its tangent satisfies

    delta phi_in-delta phi_out=Delta h.

Differentiating the charge term and cancelling the conserved-mass chemical
terms gives the pairing of delta phi with (2). Integration by parts of
integral d.A.d on the two fixed domains gives that pairing minus
Delta h d_+. Differentiating Delta H on the moving surface gives
Delta h(d_-+hD'_-). Their sum is exactly (4). The remaining curvature
term is 2 Delta H h^2 and is combined with the background pressure in
section 3. Derivatives of field magnitudes introduce no extra first-order
normal-vector term because the background is purely radial electric.

Exterior Maxwell electrostatics has delta phi_out=b r^(-l-1)Y. Hence

    integral_out |d|^2=(l+1)b^2=d_+^2/(l+1).

Using (3), (4) becomes

    F_e+2Delta h d_+-2D Delta h^2
      >=-[ (l+1)Delta^2+2D Delta ]h^2.                                (5)

This is a completion of the exterior Maxwell square. The term proportional
to the charged boundary density cancels exactly; it has not been frozen.
For l=0, fixed total charge gives d_+=0 and the residual surface term is
-2D Delta h^2, agreeing with the frozen radial load derivative. For h=0,
(4) is simply F_e>=0, including independent relative density perturbations.

## 3. Full density, common-shape and gravity Hessian

Let delta Phi_f be the Newtonian potential of the full fluid distribution
(2), including its boundary sheet. Its quadratic pairing is

    N_l=integral_0^1 eta delta Phi_f r^2 dr
           +rho_R h delta Phi_f(1)
       =-4piG/(2l+1)[ I_l(eta)+2rho_R h U+rho_R^2 h^2 ],                (6)

    I_l(eta)=integral_0^1 integral_0^1 eta(r)eta(t) r^2t^2
                      min(r,t)^l/max(r,t)^(l+1) dr dt.

No baryonic or dark source is held. The two local chemical first integrals
are 2K_a rho_a+Phi_f+Phi_w+zeta_a phi=mu_a, with zeta_b=0,
zeta_c=zeta and constant interior Phi_w=-4piG s. They remove all path
accelerations and all eta_a h cross terms from the local material energies.
Their surviving surface coefficient, before wall balance, is

    -[P_b'(1)+P_c'(1)+2(P_b(1)+P_c(1))]h^2.

The hydrostatic gradients make -(P_b'+P_c') strictly positive. The electric
curvature term 2Delta H and area variation sigma(L+2) combine with the
actual wall-load equation

    P_b+P_c-Delta H=2sigma-GsM-6piG s^2

to give sigma(L-2)+2GsM+12piG s^2. Combining these last two gravitational
load terms with the actual wall gravitational second variation yields

    W_l= -GsM(L-2)h^2
       +8piGs(l-1)/(2l+1) h[U+rho_R h]
       -8piG s^2 l(l+2)(l-1)/(2l+1) h^2.                              (7)

Therefore the exact reduced static Hessian, with Q=d^2 energy/depsilon^2,
is

    Q_l=sum_a 2K_a integral eta_a^2 r^2 dr +N_l
       -[P_b'(1)+P_c'(1)]h^2 +sigma(L-2)h^2 +W_l
       +F_e+Delta h(d_++d_-)+Delta D'_-h^2.                            (8)

Both independent densities, the moving boundary, all field work, the wall's
changing rest mass, its self-gravity and its interaction with the varied
fluids appear in this formula.

## 4. Derivation and checks of the shell terms

For fixed interior point r<1 the first perturbation of the wall potential
is

    delta Phi_w(r)=4piGs(l-1)/(2l+1) r^l hY.                           (9)

Indeed a surface mass element varies by 2h dA, while the radius derivative
of the interior harmonic kernel is -(l+1) times that kernel. This gives
2-(l+1)=1-l before the Newtonian minus sign. The monopole part of the
second wall-potential variation is spatially constant inside and equals
-Gs L h^2: use

    integral_boundary dA/|x|=integral_S2 [r+|grad_S r|^2/(2r)]dOmega
      =4pi+epsilon integral hY+epsilon^2 Lh^2/2+O(epsilon^3).

At separately fixed total fluid mass, the complete wall/fluid interaction
Hessian is consequently

    Q_fw=8piGs(l-1)/(2l+1) h[U+rho_Rh]-GsML h^2.                      (10)

The finite-density edge uses the interior value of (9). An equivalent
calculation from the fluid potential uses its **exterior** radial derivative
at the common boundary. Mixing an interior trace with the exterior
background derivative introduces a spurious 4piGs rho_R h^2. As checks,
(10) vanishes for l=0 at fixed M except its zero cross term (delta M=0),
and for a translation its value is -2GsMh^2, exactly cancelled by the
wall-load term +2GsMh^2.

For completeness, the wall self term follows directly from its nonsingular
surface double integral. Write k=|n-n'| and t=hY(n), t'=hY(n'). The
coefficient of epsilon^2 in dA dA'/|x-x'| is

    1/k [3(t^2+t'^2)/8 +9tt'/4
         +( |grad t|^2+|grad t'|^2 )/2 -(t-t')^2/(2k^2)].

The last divided difference is integrable for smooth t. The harmonic
identities

    integral_S2 1/k=4pi,
    integral integral tt'/k=4pi h^2/(2l+1),
    integral integral (t-t')^2/k^3=4pi l h^2

give

    Q_ww=-piG s^2[4l^2+2l+3+9/(2l+1)]h^2.

The first identity is elementary polar integration; the second follows by
expanding the harmonic kernel. For the third, the zonal integral is
2pi integral_-1^1 [1-P_l(u)]/(2-2u)^(3/2) du=2pi l.
It follows by integration by parts and the Legendre recurrence, starting
with l=0,1. Polarization gives the displayed double integral. Adding the
load term +12piGs^2 gives the last term of (7), using

    4l^2+2l-9+9/(2l+1)=8l(l+2)(l-1)/(2l+1).

The l=0 derivative reproduces the spherical wall-self energy
-8pi^2G s^2R^3. The l=1 coefficient vanishes after equilibrium load is
included. These checks distinguish the variable area mass from a falsely
conserved shell mass.

## 5. Uniform coercivity for every l>=2

Here all estimates use the actual frozen equilibrium, not a constant-density
surrogate. The frozen strict bounds imply

    rho_R<7, M<38, 0<D<1/1000,
    Delta<1/999000, 3/10<sigma<1/3, 0<s<1/30000.                      (11)

For the new lower tension bound, P_b+P_c>(49/50)P0,
Delta H<10^-9 and the wall root gives
2sigma>P_b+P_c-Delta H. With
P0=f(1+2f)/100 this implies sigma>3/10. The frozen upper test root gives
sigma<(51/100)P0<1/3.

The positive kernel operator in I_l has norm <=1/2 on L2(r^2dr): replace
its kernel by 1/max(r,t), whose integral in t^2dt is
1/2-r^2/6<=1/2, and use the symmetric Schur bound. Therefore

    I_l<=S, |U|<=sqrt[2S/(2l+3)].

Using 2rho_R |hU|<=S+2rho_R^2 h^2/(2l+3) and pi<4 gives

    N_l >=-(32G/5)S -(1008G/5)h^2,       l>=2.                        (12)

The positive rho_Rh^2 term in (7) can be discarded. Its remaining cross
term has magnitude <=16Gs |h|sqrt[2S/(2l+3)], so

    W_l >=-Gs S-Gs[M(L-2)+128/(2l+3)]h^2
             -16G s^2(L-2)h^2.                                      (13)

The last bound uses l/(2l+1)<1/2. Since L-2=(l-1)(l+2)>=4 and
(l+1)/(L-2)<=3/4, (5), (8), (12), (13) imply

    Q_l >= A_* S+B_* (L-2)h^2,
    A_*=1/50-32G/5-Gs,
    B_*=sigma-GsM-16Gs^2-252G/5-32Gs/7
                    -(3/4)Delta^2-(1/2)D Delta.                      (14)

We discarded only the positive background pressure-gradient coefficient.
Substituting the conservative rational bounds (11), with G=10^-8, gives

    A_*>1/100, B_*>1/4.                                               (15)

Consequently, uniformly in every integer l>=2 and every m,

    Q_l >= (1/100)sum_a integral_0^1 eta_a^2r^2dr
                    +(1/4)(l-1)(l+2)h^2.                            (16)

This includes l=2 common shape and arbitrary independent relative fluid
profiles; mixed shape/relative directions are controlled in the same
estimate. At l=2 the shape coefficient is at least one in the normalized
harmonic units. Small G and a counted capillary area term are the mechanism.
The first failed attempt—discarding the shape/field cross term—would not
justify this theorem. The exterior Maxwell square (5) is what repairs it.

## 6. Translation, relabelings and the exact scope

In l=1 a translation has eta_a=-h rho_a' and normal boundary displacement
hY. Translation invariance of the entire counted energy and of both mass
constraints implies that its Hessian pairs this tangent to zero against
all admissible tangents. Hence

    Q_1[eta_b,eta_c,h]=Q_1[eta_b+h rho_b',eta_c+h rho_c',0].            (17)

At h=0 the wall terms vanish; the field term is nonnegative and the same
Schur estimate gives N_1>=-(16G/3)S. Therefore

    Q_1 >=(1/100)sum_a integral_0^1(eta_a+h rho_a')^2 r^2dr.            (18)

Thus the physical l=1 kernel consists precisely of translations. In material
displacement variables one must additionally quotient the relabeling/vortical
nulls specified in section 1. Relative tangential currents have not been
called strictly restoring modes.

Smooth harmonic sums extend by closing the positive density/shape norm in
(16), while respecting the Gauss-field form domain. Rotation of the sphere
is a relabeling null. The monopole with its two mass constraints is covered
by the frozen radial proof. A static magnetic perturbation adds
integral_inside beta|delta B|^2+integral_outside|delta B|^2, subject to
magnetic flux matching. Its coefficient is positive; at the actual witness
the occupied smooth beta0 branch applies everywhere. Its shape dependence
starts at cubic order because B=0 on the background. Extra electric
Gauss-field tangents add a positive Hessian remainder around the minimizing
static electrostatic field.

These are static configuration-energy statements. No positive angular
Rayleigh gap on arbitrary displacement fields is claimed: their relabeling
nulls obstruct that. The dark-frame velocity/magnetic mixing, electromagnetic
radiation, choice of boundary characteristic conditions, strong
hyperbolicity and a nonlinear moving-interface evolution require their own
dynamical analysis. No covariant metric, relativistic shell junction, wall
microphysics, formation, abundance or galaxy/lensing prediction follows from
this hybrid static coercivity theorem.
