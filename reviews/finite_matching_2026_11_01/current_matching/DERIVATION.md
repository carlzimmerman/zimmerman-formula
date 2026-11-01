# Component phase-current coefficient about the broken-SUSY valley

The tree kinetic action is canonical. Set scalar phase charges Qs=(1 for X,0 for A,1 for B), and Weyl phase charges Qf=(+1/2 for X,B and gauginos,-1/2 for A). The common phase theta is half the R rotation. At fixed phase its background is the specified commuting valley; this calculation is not an unbroken-SUSY/small-F Kahler shortcut.

## Scalar determinant and Ward seagull

On98 real canonical coordinates let J=[[0,-Qs],[Qs,0]]. For a fixed common phase H(theta)=exp(theta J)H exp(-theta J), so Htheta=[J,H] and Hthetatheta=[J,[J,H]]. The theta² seagull and bubble cancel at zero momentum because this is an isospectral rotation; it cannot generate a theta potential. The seagull has no external-momentum dependence. Expanding the real-scalar determinant gives

    deltaFs=1/(64pi²) sum_ordered_ij |Htheta_ij|²
             integral_0^1 dx x(1-x)/[x mi²+(1-x)mj²].

In a real H eigenbasis Htheta_ij=(mj²-mi²)Jij. Thus an **unordered** i<j pair contributes

    Jij²/(32pi²) G(mi²,mj²),
    G(a,b)=(a+b)/2 -ab ln(a/b)/(a-b).

G(a,a)=0, G(a,0)=a/2 and the near-equal series is positive. This finite scalar graph vanishes when H commutes with the charge generator, including a free charged gapped scalar below its density threshold. It is not inferred by differentiating the effective potential alone.

## Fermion determinant with the actual mass/phase vertex

The unbroken adjoint2x2 blocks and broken3x3 block can be made real symmetric by constant unitary congruence. Keep their **signed** Majorana eigenmasses mu_i; do not replace signs before evaluating the chirality-flip term. If M is such a real block and Q its Weyl charges, Mtheta=-i{Q,M}=iA with A=-{Q,M} real symmetric. In its orthogonal eigenbasis Aij is the actual pseudoscalar vertex.

The Majorana determinant -Tr ln D/2 gives after minimal pole subtraction

    deltaFf=sum_ordered_ij Aij²/(16pi²)
       integral_0^1 dx x(1-x)
          [-3 ln(Dij/Q²)+mu_i mu_j/Dij-1],
    Dij=x mu_i²+(1-x)mu_j².

Both momentum numerator and chirality-flip term are retained. For a single Majorana mass m exp(i theta) this becomes -m² ln(m²/Q²)/(32pi²). The zero-momentum mass seagull is fixed by the same phase rotation, rather than discarded when evaluating the Ward identity. This does not imply that the momentum coefficient vanishes in a supersymmetric theory.

For SU3/SU2 use Q=diag(-1/2,+1/2) and M=[[m,q],[q,0]]. For each broken root use Q=diag(-1/2,+1/2,+1/2) and M=[[m,q,L],[q,0,R],[L,R,0]]. Here m=(1+r)hX,q=r lambda a,L=5ga,R=5gb. Multiplicities are8,3,12. The remaining singlet mass matrix is phase independent on this valley and massless unbroken gauginos have no local mass-phase vertex. Full-matrix vertex norms and singular masses are checked numerically, rather than treating this omission as a degeneracy guess.

## Landau scalar-vector derivative mixing

Vector masses are common-phase independent, but that does **not** remove the broken gauge-current contribution. Expanding |D z|² about a slowly varying phase, and integrating by parts using partial_mu A^mu=0, gives

    Lmix=-4g(partial_mu theta)A_a^mu Re[delta z^dagger R_a Qs z]
        =-2sqrt(2)g(partial_mu theta)A_a^mu C_aI chi_I,
    C_aI=(Re[R_a Qs z], Im[R_a Qs z]).

The Gaussian block determinant gives, in d=4-2epsilon,

    deltaF_SV=-4g² (d-1)/d sum_aI C_aI² B(mVa²,mSI²).

After subtracting its pole, B=[1/epsilon-integral ln(D/Q²)]/(16pi²). The transverse factor is (d-1)/d=3/4-epsilon/8+..., so the finite coefficient is

    deltaF_SV=g²/(16pi²) sum_aI C_aI²
                    [3 integral_0^1 dx ln(D/Q²)+1/2].

The +1/2 is the evanescent projector times the pole; setting d=4 before subtraction would omit it. In dimensional reduction the epsilon vectors have no external-theta-derivative SV vertex, since the external phase momentum has no extra-dimensional component, and their background mass is phase independent. Linear Landau ghosts have no background-scalar vertex. Gauge Goldstones remain in the scalar eigenbasis and in this mixed graph; no unitary-gauge deletion is made.

This fixes a component finite subtraction convention. No unknown finite field counterterm is chosen to obtain a desired pressure result. The algebra reviewer independently reconstructed the scalar unordered/ordered factor, fermion kernel and SV projector finite term from the raw Gaussian determinants; code and combined physics require their own review.

## Ultraviolet/current check

The scalar graph is UV finite. The fermion scale derivative is Tr(A²)/(16pi²), which sums here to [87h²X²+600g²b²]/(16pi²). The full scalar-vector current norm is sum C²=150b², so its scale derivative is -900g²b²/(16pi²). The total is therefore

    d deltaF/dln Q=[87h²X²-300g²b²]/(16pi²).

This is 2[gammaX_component X²+30gammaB_component b²] with gammaX=12h²/(16pi²), gammaB=(21lambda²/20-5g²)/(16pi²). The gauge coefficient is the Landau **component-scalar** one. Substituting the chiral-superfield gauge anomalous dimension would spoil this current identity.

The result is a genuine local one-loop finite graph coefficient, not complete occupied-state derivative matching. The conserved-current anomaly, gauge/IR dynamics, radial kinetic matching, higher derivatives and the phase state/lifetime remain separate. The fixed original-X chart and fixed renormalization Q must be retained when combining it with the finite potential and heavy geometric pullback.
