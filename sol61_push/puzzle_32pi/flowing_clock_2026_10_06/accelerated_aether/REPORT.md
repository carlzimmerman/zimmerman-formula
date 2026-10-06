# Accelerated aether: full local constraints do not remove the continuous-path obstruction

Entry base/observed HEAD `07fa64b44891fc87697f53f86812287946481586`. Own writes confined to this folder. The genuine acceleration escape was tested, including propagating transverse vector perturbations. It does not produce a healthy continuous matching path in the stated c13=0, positive-F_K, zero-offset action class. A perpendicular wave direction retains a physical negative scalar kinetic interval after every auxiliary constraint. There are also disconnected accelerated coefficient regions with positive full local principal Hamiltonian: negative Q by itself is not a universal ghost criterion.

## Action and frozen-background scope

Use signature(-+++), c=1, Einstein coefficient E>0, and minimal physical matter:

    S=E/2 int sqrt(-g)[R+M² F(K)+lambda(A²+1)]+S_m[g],
    c1=-1,c2=-1/2,c3=+1, c13=0.

For a unit congruence, K=(c2 theta²-c1 a²+2c1 omega_ij omega^ij)/M². The background is hypersurface orthogonal, so omega=0 and A is the normal to a local foliation. Perturbations are NOT restricted to be hypersurface orthogonal: transverse vector velocities and their vorticity are retained. Background shear need not vanish; its invariant coefficient cancels at c13=0. Work in a local orthonormal rest frame, freezing theta,a_i,F_K,F_KK. Frequencies and wavenumbers are large compared with curvature and background variation scales. Background lapse gradients are kept in K and the Hessian, but undifferentiated background-gradient corrections to a perturbation are lower principal order. No unknown UV cutoff or higher-derivative completion is assumed harmless; this is a two-derivative principal result.

Put h=F_K, s=F_KK/M². The quadratic derivative terms from the aether action are exactly

    h[c2(delta theta)²-c1(delta a)²+2c1(delta omega)²]
       +2s[c2 theta delta theta-c1 a dot delta a]².

Consequently the acceleration/expansion mixing is retained, rather than importing the homogeneous scalar cone. For our coefficients define

    ell=1+h/2-s theta²/2, eta_ij=h delta_ij+2s a_i a_j,
    u_i=-s theta a_i.

The trace kinetic coefficient from EH plus F is -ell; the mixed term is 2 delta theta u dot delta a.

## Every nondynamical constraint

At linear principal order write A=n+v. The unit norm fixes its temporal component; it is not an additional scalar velocity. Choose the time coordinate gauge v_long=0 for each nonzero k, and spatial gauge h_ij=e^(2zeta)delta_ij+TT. This is a coordinate gauge on the longitudinal vector, not the deletion of its physical scalar, which resides in zeta and the metric constraints. The covariant spatial component is A_i=v_i, while A^i=v^i-N^i. Direct differentiation gives

    delta theta=n zetadot-div N,
    delta a_i=partial_i nu+vdot_Ti,
    delta omega_ij=(partial_i v_Tj-partial_j v_Ti)/2.

Thus no time derivative of the shift is hidden in delta a. The transverse shift appears only through the EH term k²|N_T|²/2 and its algebraic constraint eliminates it. TT has its ordinary positive luminal principal block. The transverse vector orthogonal to the plane of a and k has h(vdot²-|grad v|²) and is retained. For the coupled vector in that plane let W=vdot, Z=zetadot, B=Delta beta, j=partial_k nu and P=partial_k zeta. Set Nbar=n-1, L=ell-1, a_parallel=a_L and a_transverse=a_T, and

    p=-s theta a_L, t=-s theta a_T,
    eta_L=h+2s a_L², eta_T=h+2s a_T², eta_LT=2s a_L a_T.

The complete coupled scalar/vector principal density (inside E/2) before the two scalar constraints is

    n(1-n ell)Z²+2(n ell-1)ZB+(1-ell)B²
    +eta_L j²+2eta_LT jW+eta_T W²
    +2(nZ-B)(pj+tW)+2Nbar jP+Nbar(n-2)P²-h|grad v|².

Shift variation gives B=[(n ell-1)Z-(pj+tW)]/L. It leaves

    A Z²+(pj+tW)²/L-2Nbar Z(pj+tW)/L
      +eta_L j²+2eta_LT jW+eta_T W²+2Nbar jP+Nbar(n-2)P²,
    A=Nbar(n ell-1)/L.

Define C=eta_L+p²/L, r=eta_LT+pt/L and q=Nbar p/L. Lapse variation gives

    j=-(rW-qZ+Nbar P)/C.

These steps require L,C nonzero. Both are nonzero at the ghost witnesses and at the positive coefficient point below. No transverse propagating field was frozen before constraint elimination.

## General-angle reduced symbol

For U=(zeta,v), the reduced density is

    Udot^T Kmat Udot+2 Udot^T Jmat partial_k U
      -(partial_k U)^T Vmat partial_k U,

where integration by parts symmetrizes the time/space mixed term and

    Kzz=A-q²/C,
    Kzv=-Nbar t/L+qr/C,
    Kvv=eta_T+t²/L-r²/C,
    Jzz=Nbar q/C, Jzv=-Nbar r/(2C), Jvv=0,
    Vzz=Nbar²/C-Nbar(n-2), Vvv=h, Vzv=0.

The characteristic equation is det(v_phase² Kmat-2v_phase Jmat-Vmat)=0. Positive definite Kmat and Vmat suffice for positive frozen quadratic Hamiltonian and real characteristic speeds; the mixed term cancels from the Hamiltonian. This sufficient local test does not establish nonlinear energy, global evolution, observational viability or an on-shell background. Negative Kzz after constraints already rules out positive kinetic energy regardless of vector mixing.

For k parallel a, t=0 and the transverse vector decouples. The scalar gets the lapse correction Kzz=A-q²/C and a tilted cone through Jzz. For k perpendicular a, p=eta_LT=0, C=h and

    j=-Nbar P/h,
    Kmat=[[A,-Nbar t/L],[-Nbar t/L,h+2s a²+t²/L]],
    Vzz=Nbar²/h-Nbar(n-2).

In particular Kzz=A exactly. Setting only the physical vector velocity to zero is now a legitimate test direction of the already reduced kinetic form. If 1/n<ell<1, A<0. Off-diagonal coupling cannot make this form positive. If a kinetic degeneracy were asserted elsewhere, it cannot erase this strictly negative restriction at the nonsingular witness; a zero vector diagonal plus nonzero cross term itself has indefinite determinant.

## Continuous matching theorem

Assume F is C² over the connecting negative-K interval, F(0)=0, h=F_K>0, and a nonzero comoving vacuum FRW root with alpha=c1+n c2+c3=n c2<0. The correct general-d lapse equation is

    F-2K F_K+(n-1)K/alpha=0.

Writing K=-z, h(z)=F_K(-z), I=int_0^z h, Q=1+2K F_KK/F_K=1+2z hprime/h, this root requires I-2zh=-(n-1)z/alpha>0. If Q>=0 throughout, sqrt(z)h is nondecreasing, so I<=2zh, a contradiction. There is therefore a negative-Q point with s>0 and

    ell_geo=1+hQ/2<1.

On ANY accelerated omega=0 state at the same K=-z,

    theta²=2(M²z+a²),
    ell_theta=1+h/2-(z+a²/M²)F_KK
             =ell_geo-(a²/M²)F_KK <=ell_geo<1.

A continuous local path from the cosmological root K_root<0 to an isolated stationary MOND branch at K>=0 crosses every K in (K_root,0), and therefore necessarily encounters that negative-Q value. The hypotheses h>0 and C² hold over this whole negative interval, not only at the endpoints. The isolated theta=0 branch has ell=1+h/2>1 at every nonzero field with h>0. Hence ell must pass through 1/n<ell<1, regardless of acceleration size or whether the negative-Q state itself lies below1/n. The perpendicular symbol there has C=h>0,L!=0 and A<0 after all constraints. This proves a conditional obstruction to a continuous everywhere-positive-principal matching path, extending the previous homogeneous result to accelerated, spatially anisotropic backgrounds in this action class.

It is not a theorem excluding an arbitrary aether theory or every galaxy. Nonzero background vorticity, c13/c4 or extra operators, nonzero F(0), changing the sign/regularity hypotheses, singular/nonlocal matching or a changed physical action can evade the premises. Such an escape still needs a genuine solution and health check. Principal pathology is a local obstruction; the existence and boundary matching of candidate backgrounds were not assumed from a coefficient sample.

## Disconnected locally positive negative-Q coefficients

For K=-z in units M=1, put L0=h/2-zs and L=L0-s a². The exact general-angle identities are

    C=h(L0-s a_T²)/(L0-s a²),
    Kvv=h L0/(L0-s a_T²),
    det Kmat_angle=(h/C)det Kmat_perpendicular.

For n=3, Q<0 means L0<0. Then C,Kvv>0 at every orientation. Direct expansion gives

    det Kperp=2[-3h²+6hsz-4h-8s a²]/[-h+2s(z+a²)].

Thus if 0<h<2, s>0 and

    0<=a²<h(6sz-3h-4)/(8s),

the right side being positive, both Kmat and Vmat are positive for ALL wavevector orientations. Indeed C<=h<2 yields Vzz>0. At zero acceleration this condition is precisely ell_geo<1/3, the disconnected scalar-positive region. Acceleration has an explicit upper bound; it does not connect this region across the ghost band.

The earlier quintic family at midpoint z=.105 has exact h=2101/2020 and s=(1899/1010)(375/2). Taking a/M=.001 satisfies the displayed rational strict inequalities. This is an actual all-orientation positive coefficient witness with Q approximately-70.18 and ell approximately-35.50. A 401-direction corroboration finds minimum kinetic eigenvalue about1.04007 and minimum spatial eigenvalue about1.04010; five characteristic polynomials have real roots. These numbers are bounded checks, while the rational inequalities prove the orientation assertion. No full solution with this local jet has been constructed.

For comparison, the earlier ell_geo=.8 ghost witness at z=.100481201427 remains negative after introducing a/M=.001,.01,.1. The general continuous-path theorem, rather than these samples, shows why large acceleration or an alternative interpolation path cannot simply jump to the disconnected positive region.

## Evidence and unresolved implication

`checks.py` independently constructs the F Hessian, eliminates both scalar constraints, derives the full general-angle matrix, verifies the determinant identities and exact rational positive-point inequalities, and checks bounded ghost/cone controls. Authoritative fresh runs and version-2 manifests are below `runs/`; `drop_mixing_a` deletes the actual F_KK theta a cross term and must fail. Main `runs/main_a/` passes15/15; actual mixing-deletion control `runs/drop_mixing_a/` passes11/15 and fails the raw Hessian, shift, lapse and full Schur checks. Both version-2 manifests validate, with unchanged input hashes and retained stdout/stderr. Caps: wall45s, CPU30s/process,1MiB logs and one cooperative numerical-library thread; no memory/affinity cap. The check count is not the analytic proof. No astronomical calculations or peer scripts are executed. Input source hashes and primary-version conventions are in SOURCE_PROVENANCE.json.

The local accelerated principal escape closes negatively under the theorem's precise hypotheses, but a full dynamically matched galaxy is still unbuilt. A worthwhile changed-premise route must identify an operator, vorticity state or boundary/regularity change that removes the perpendicular negative direction while preserving measured source normalization. This checkpoint supplies that necessary discriminator, not a 32pi selection.
