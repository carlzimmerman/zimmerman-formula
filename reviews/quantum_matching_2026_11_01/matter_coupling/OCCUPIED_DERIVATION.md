# Finite occupied heavy relaxation and its pressure ledger

This includes one computable finite contribution to the actual phase-current state. It does not stand for all finite two-loop vacuum graphs, finite derivative graphs, light/gauge dynamics or higher derivatives. The tested RG interface and full spectral normal gradients identify the approximations precisely.

At a fixed reference X0 let a0,b0 be the tree heavy singlet valley coordinates. For a rotating common phase of X and B, the angular coefficient before heavy relaxation is F0=X^2+30b^2. A does not rotate under the stated R symmetry. At fixed X the tree normal Hessian is diagonal,

    Haa=120fh, Hbb=60lambda^2 a0^2,
    F_b=60b0, F_a=0.

The normal sources in the grand potential at phase frequency omega are CWa and CWb-omega^2 F_b. Eliminating those two normal displacements to quadratic order gives

    Omega=U_RG-omega^2 F_RG
          -1/2[CWa^2/Haa+(CWb-omega^2 F_b)^2/Hbb].

This is evaluated once. It contains a vacuum energy correction, a finite angular-coefficient correction and an occupied quartic term simultaneously. Adding the vacuum/metric corrections separately to this square would double count them. Define

    V=U_RG-1/2(CWa^2/Haa+CWb^2/Hbb),
    F=F_RG-CWb F_b/Hbb,
    J=F_b^2/Hbb >=0.

Then Omega=V-F omega^2-(J/2)omega^4. These normal coordinates are canonical local fields at the matched RG scale in the supplied interface; finite kinetic matching beyond this known relaxation is not supplied.

For s=ln(X0/Xref), write subscripts for derivatives at fixed omega. With q=omega^2, the connected small-frequency stationary root obeys

    V_s-F_s q-(J_s/2)q^2=0,
    q=2V_s/[F_s+sqrt(F_s^2+2J_s V_s)].

The branch's phase charge, partial susceptibility, mixed derivative and fixed-charge radial Hessian are

    n=-Omega_omega=2omega(F+Jq),
    C=-Omega_omegaomega=2F+6Jq,
    M=Omega_somega=-2omega(F_s+J_s q),
    N=Omega_ss=V_ss-F_ss q-(J_ss/2)q^2,
    D=partial_s^2 epsilon_at_fixed_n=N+M^2/C.

The last expression is a Legendre-transform Schur complement. It requires C>0. Along Omega_s=0,

    dn/domega=C+M^2/N=C D/N,
    c_IR^2=n/[omega dn/domega]=n N/(omega C D).

When C,D,n,omega are positive, the pressure sign boundary is N=0, with the limiting interpretation as dn/domega diverges. It is not a radial-D zero. P=-Omega+Vvac and epsilon_ex=Omega+omega n-Vvac give explicitly

    P=Fq+(J/2)q^2-V+Vvac,
    epsilon_ex=Fq+(3J/2)q^2+V-Vvac.

No radial kinetic coefficient was invented to turn D into a full physical frequency. These formulas are the local, timelike-current thermodynamic/IR response of the retained effective grand potential; its finite-wavelength range needs matched derivative coefficients.

The twelve massless unbroken gauginos have q_R=1, hence q_theta=1/2. An optional free, zero-temperature equilibrated reservoir would contribute

    Omega_light=-12(omega/2)^4/(24pi^2)=-omega^4/(32pi^2),
    J_light=1/(16pi^2), epsilon_light=3omega^4/(32pi^2).

This assumed reservoir changes n,C,D and the pressure/energy ratio. It has no explicit X derivative, so it leaves the stationary q(X) and N(X) unchanged in this free-reservoir approximation. The Goldstino is not included without a nonlinear-current derivation. Gauge interactions, confinement, anomaly, equilibration and a selected occupation are not thereby controlled.

## Structural coldness restriction before the quartic correction

For the simpler two-derivative phase action, F>0, a=(lnF)'>0 and N=Uss-(a+a'/a)Us>=0 on a connected branch from F0 imply

    omega^2=Us/(aF), d(omega^2)/ds=N/(aF)>=0.

Consequently DeltaU=integral omega^2 dF <=omega(s)^2(F-F0). With E=F omega^2, the vacuum-subtracted w=(E-DeltaU)/(E+DeltaU) therefore obeys

    w >= F0/(2F-F0).

For canonical F proportional to X^2 this is w >=1/[2(X/Xmin)^2-1]. Thus a stable connected phase branch spanning only X/Xmin about1.214 cannot approach cold excess energy through density selection alone; the bound there is about0.514. This is a conditional integral argument, not a claim about disconnected branches, a full matched microscopic action, or the quartic-grand-potential correction above. The coordinator independently reconstructed the phase fluctuation and this bound in `../PHASE_RESPONSE_AUDIT.md`; the thermodynamic calculation here agrees.
