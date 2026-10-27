# Independent derivation, recorded before author code/reports

Auditor: isolated round2_independent_reviewer. Input only: `03_relativity/raw_derivation.md`, SHA256 `b8bbe82a317018a2182340b92757dc8cb6b733434ea90f3671b8552ec38d6c2f`. Requested base 8aa3f7046a7ae14a99f3515fd42df5bf061fb1db; observed checkout HEAD 22766173c1985526eb359f809d85a8196401f0ae. No author checks.py, report.md, self-review, or coordinator files have been read. This file records a new calculation from the ADM definitions; the proposed formulas themselves were present in the raw input, so independence means independent reconstruction, not blindness to the proposed answer.

## Claim and domain

Real linear perturbations about expanding de Sitter vacuum P=0, with K,beta,eta,gamma,H positive and Lambda=3(2+3beta)H²/2; finite comoving k>0. Additional claim: frozen leading principal polarizations at a static clock-aligned regular background, finite derivatives, E=theta=0, finite P with K|P|<a0. The latter is a high-frequency calculation only, away from a singular shift Hessian. No inference of PPN, nonlinear well-posedness or full cosmological viability is included.

## Background and independent scalar expansion

Let A=2+3beta. The homogeneous extrinsic combination is -3A(adot/aN)², so lapse variation of -3Aa adot²/(4KN)-Lambda Na³/(2K) gives 3AH²=2Lambda. Scale variation gives A(2Hdot+3H²)=2Lambda. The beta contribution alone gives rho=-9beta H²/(4K), p=3beta(2Hdot+3H²)/(4K); its continuity equation is identically zero.

For a real Fourier mode write zeta=e z cos(kx), n=e n cos(kx), shift^x=e Y sin(kx)/k. Put v=zdot. At second order q=H+e v cos(kx)+e²Yz sin²(kx), X=eY cos(kx), and the kinetic numerator is -3Aq²+2AqX-beta X². Multiply by exp(3e z cos)/(1+e n cos). With twice the spatial average (common Fourier normalization), the coefficient before 1/(4K) is

-3A v²+2AvY-beta Y²-6AHYz+(3z-n)(-6AHv+2AHY)-3AH²(9z²/2-3zn+n²).

The two Yz terms cancel. The cosmological term contributes -3AH²(9z²/2+3zn). The zn terms cancel too. Integration of -18AHzv with the a³ measure produces +27AH²z², canceling the total -27AH²z². The survivors are exactly -3A(v-Hn)²+2A(v-Hn)Y-beta Y².

For spatial curvature, sqrt(h) N R3=a(1+n)e^zeta[-4 Laplacian zeta-2(grad zeta)²]. Spatial integration gives a[2(grad zeta)²-4n Laplacian zeta]. Thus the remaining gravitational terms are (2p² z²+4p²nz)/(4K). Direct expansion of the matter pieces at P=0 yields eta p² sigmadot²/2+p² n sigma-Kp²sigma²/2-gamma p⁴sigma²/2. F vanishes on the scalar field and Lie_shift P is second order here.

Varying Y gives Y=A(v-Hn)/beta. Its Schur complement is C(v-Hn)²/2, C=A/(K beta). Defining Z=z/K+sigma, the remaining lapse equation gives n=v/H-p²Z/(CH²). Substitution leaves eta p² sigmadot²/2+p²Z zdot/H+p²z²/(2K)-Kp²sigma²/2-gamma p⁴sigma²/2-p⁴Z²/(2CH²).

Since d(a³p²)/dt=Ha³p², substituting z=K(Z-sigma) and integrating Kp²ZZdot/H yields -Kp²Z²/2. This exactly cancels the explicit square term, leaving -Kp²Z(sigmadot+Hsigma)/H. Hence Z=-CKH(sigmadot+Hsigma)/p² and the reduced Lagrangian is a³[eta p²sigmadot²+B(sigmadot+Hsigma)²-gamma p⁴sigma²]/2, B=CK². Integrating the remaining cross term with d(a³)/dt=3Ha³ gives Q=B+eta p² and V=gamma p⁴+2BH². Forgetting either integration weight changes the answer.

## Forward evolution and reconstruction

The exact equation is Q sigmaddot+H(3B+eta p²)sigmadot+V sigma=0. For E=(Q sigmadot²+V sigma²)/2 direct differentiation gives Edot=-H(3B+2eta p²)sigmadot²-2Hgamma p⁴sigma². Therefore for every finite initial time t0 and fixed k>0, E(t)<=E(t0), |sigma|²<=E(t0)/(BH²) and |sigmadot|²<=2E(t0)/B for t>=t0. This is forward boundedness; no claim of bounded solutions on the entire past-eternal patch follows.

In p, the equation is (B+eta p²)p²sigma''-2Bp sigma'+(2B+gamma p⁴/H²)sigma=0. Writing sigma=p^m sum_j c_j p^j yields

B(m+j-1)(m+j-2)c_j+eta(m+j-2)(m+j-3)c_(j-2)+(gamma/H²)c_(j-4)=0.

The roots are 1,2. The root separation causes no logarithmic obstruction: at m=1,j=1 both source coefficients vanish, and the free c1 is simply the second solution. Choosing c1=0 gives sigma1=p[1-gamma p⁴/(12BH²)+O(p⁶)]. The second solution is sigma2=p²[1-eta p²/(3B)+O(p⁴)]. Coefficients are analytic near p=0 and the recursion denominators grow quadratically, giving local convergent regular-singular expansions. These exhaust the two-dimensional solution space near future infinity.

Reconstruction is z=-BH(sigmadot+Hsigma)/p²-Ksigma. For sigma1, sigmadot+Hsigma=O(p⁵), so z=-Kp+O(p³). For sigma2, sigmadot+Hsigma=-Hp²+O(p⁴), so z=BH²+O(p²). Moreover Y=p²(z+Ksigma)/H and n=zdot/H-beta p²(z+Ksigma)/(AH²). Therefore n decays and physical scalar shift Y/p decays on both branches. This proves future boundedness of reconstructed fields for each fixed finite k and finite initial data, with no uniform k->0 constraint norm established.

## Homogeneous endpoint, transverse and tensor modes

At k=0 sigma has no physical P. Direct homogeneous scalar variation gives lapse constraint zdot-Hn=0 and vanishing reduced metric-scalar action; it is a time/background normalization freedom. A homogeneous vector covector P_i has action a(eta dotP_i²-KP_i²)/2 independently for each of three components, hence damped positive oscillators. Homogeneous traceless metric perturbations obey hddot+3Hhdot=0. These results cannot be obtained by merely setting k=0 in Z's eliminated expression.

For finite k, transverse covectors have action a[eta dotP_T²-(K+gamma p²)P_T²]/2. The corresponding energy derivative is -eta HdotP_T²-Hgamma p²P_T². TT gravity has a³[dot h_ij²-p²h_ij²]/(16K), positive kinetic term and speed one. The beta-trace term has no TT derivative square. Background-dependent nondifferentiated TT terms cancel on shell.

## Static oblique block reconstructed from derivatives

Take orthonormal spatial axes, wave covector along z; spatial gauge sets metric vector and scalar shear to zero, leaving h_ij=2zeta delta_ij+h_ij^TT. For constant frozen P, the linear electric derivative is delta E_i=dot(delta P_i)-P_j partial_i shift^j: only i=z receives a shift derivative. This gives eta[(qdot-P.y)²+rdot²]/2 with y_j=ik shift_j (real quadratures can absorb i).

The ADM shift derivative square contributes -beta y_z²/(4K)+(y_x²+y_y²)/(8K), hence S0=diag(-beta/(2K),1/(4K),1/(4K)). The variation of d is partial_i deltaP_i-P_j partial_i delta h_ij+(P_j/2)partial_j trace(delta h)=ik(q+P_L zeta). TT drops out because both its trace and its longitudinal divergence vanish. F_ij has no metric derivative, and its background-derivative cross terms are lower order. The lapse coupling uses sqrt(h)P^i=barP_i+deltaP_i+zeta barP_i-h_ij^TT barP_j. Again TT vanishes upon contraction with k_i. The lapse equation imposes zeta=iKq/k+O(k^-2), up to Fourier sign convention. Consequently d's zeta term is subleading relative to ikq. Terms zdot Y are also subleading when omega scales as k. No derivative TT-P mixing remains at this order. This power counting requires fixed finite background coefficients and a nonsingular reduced branch; it is not uniform near Delta=0.

Shift elimination is the rank-one inverse of S0+eta PP^T. Its determinant is det(S0)Delta, Delta=1+eta P^TS0^-1P. The reduced longitudinal coefficient is eta/Delta, while r keeps eta. The two gradient coefficients are gamma. Thus omega_q²/k²=(gamma/eta)Delta and omega_r²/k²=gamma/eta; TT remains luminal. At Delta=0, multiplying the shift equation by P^TS0^-1 forces qdot=0, because P^TS0^-1P=-1/eta; an inverse and its mode count cannot be continued across this point.

With r0=2eta u²/(Kbeta), Delta=1-r0+(1+2beta)r0 sin²theta. Its minimum over angle is at alignment, and its infimum over u<a0 is 1-2eta a0²/(Kbeta). A strictly positive uniform margin requires beta>2eta a0²/K. Equality yields positive Delta at every admissible u<a0, with infimum zero. Strict reversal yields negative Delta on sqrt(Kbeta/(2eta))<u<a0 at alignment. The raw sentence 'If the inequality fails ... negative ... inside the cap' must say 'If the inequality is reversed strictly'; equality is a counterexample to its literal phrasing.

## Cubic statement

W's cubic coefficient K²|P|³/(3a0) follows directly from -x-log(1-x). The L-infinity bound integral|P|³<=P_amp integral|P|² gives the displayed envelope ratio 2Kp²u_amp/[3a0(gamma p⁴+2BH²)]. Maximizing in p² gives p⁴=2BH²/gamma and K u_amp/[3a0Hsqrt(2Bgamma)]. A single real sinusoid multiplies by 8/(3pi). This is only a direct potential vertex bound; no inference about all interactions or a quantum cutoff follows.

## Initial verdict before author-code comparison

Correct only after a stated restriction: in G, replace failure of the strict inequality with strict reversal when asserting interior negative modes. Interpret de Sitter boundedness as forward evolution from finite initial time. Under those exact qualifications the substantive scalar and regular static principal formulas are independently reproduced. No omitted load-bearing leading TT mixing was found for the stated static covector action. Global/nonlinear/S3/PPN conclusions remain unproved and outside this audit.
