# Same-action current and stationary radial flux

The unchanged action does **not** permit a regular, genuinely charge-stationary ball with no center source to carry nonzero net outward shift flux. This is charge conservation, not a no-go for time-dependent charge depletion. Moreover, zero radial flux does **not** force the scalar gradient to vanish once the cubic term is retained. The local nontrivial branch found here is not an Einstein solution, is not stationary in charge, and has negative shift density on the recorded first slice.

## Action-derived current

Use signature \((-+++)\), \(X=-\nabla_\mu\chi\nabla^\mu\chi\), \(h^{\mu\nu}=g^{\mu\nu}+n^\mu n^\nu\), \(Y=h^{\mu\nu}\chi_\mu\chi_\nu\), and the unchanged action
\[
L=P(X,\tau)-V(\tau)+sW(Y,\tau)+\gamma X\Box\chi,\qquad \gamma=\mathrm{constant}.
\]
There is no explicit \(\chi\)-dependence. Integrating the \(X\Box\delta\chi\) variation once by parts gives
\[
\delta S_\chi=\int\sqrt{-g}\,J^\mu\nabla_\mu\delta\chi,\qquad
J^\mu=-2(P_X+\gamma\Box\chi)\nabla^\mu\chi
 +2sW_Yh^{\mu\nu}\chi_\nu-\gamma\nabla^\mu X.
\]
Thus \(\nabla_\mu J^\mu=0\) on the scalar equation. The sign convention gives the archived homogeneous current \(J^0=2P_XQ-6\gamma HQ^2\) on isotropic zero-gradient data. The code derives the generalized Noether momentum in a normal frame; metric compatibility gives the displayed covariant expression. No gravitational field equation was used.

## Static metric is not stationary charge

Take
\[
ds^2=-N(r)^2dt^2+\frac{dr^2}{F(r)}+R(r)^2d\Sigma^2,\quad
\tau=t,\quad\chi=Qt+\psi(r),\quad p=\psi'(r).
\]
Here \(Q\) is the coordinate time slope; its clock-frame value is \(Q/N\). A sphere has \(R=r\), while the plane considered here has constant \(R\). For \(N,F>0\), put
\[
w=\frac{NR^2}{\sqrt F},\quad K=\frac{N'}N+\frac{2R'}R,\quad
X=\frac{Q^2}{N^2}-Fp^2,\quad s=\frac1N,\quad Y=Fp^2.
\]
The exact currents are
\[
\boxed{J^r=2F\left[-\left(P_X-\frac{W_Y}{N}\right)p
+\gamma\frac{Q^2N'}{N^3}-\gamma FKp^2\right]},
\qquad
J^t=\frac{2Q}{N^2}(P_X+\gamma\Box\chi),
\]
where \(\Box\chi=Fp'+(FK+F'/2)p\).
The \(p'\) and \(F'\) terms cancel from \(J^r\). Independently, the reduced density
\[
\mathcal L_r=w\left[P-V+\frac WN+\gamma X\,w^{-1}(wFp)'\right]
\]
gives \(wJ^r=\partial\mathcal L_r/\partial p-
\partial_r(\partial\mathcal L_r/\partial p')\). This checks the area, lapse, sign, and cubic terms without dropping the scalar's second derivative before variation.

The full scalar equation is
\[
\partial_t(wJ^t)+\partial_r(wJ^r)=0.
\]
In this geometrically static ansatz \(X,Y,N,F,p,Q\) have no time dependence, but the fixed constitutive functions depend on \(\tau=t\). Consequently,
\[
\partial_tJ^t=\frac{2Q}{N^2}P_{X\tau}(X,t),\qquad
\partial_r(wJ^r)=-\frac{2wQ}{N^2}P_{X\tau}(X,t).
\]
Extremizing the radial density alone at each time is therefore not the full scalar equation unless the density really is stationary.

For a sphere define
\[
C(<r,t)=4\pi\int_0^r w(u)J^t(u,t)\,du,\qquad
\Phi(r,t)=4\pi w(r)J^r(r,t).
\]
Then \(\dot C=\Phi(0,t)-\Phi(r,t)\). At a regular center, \(N\) is finite and positive, \(F\to1\), and the physical radial current is finite; hence \(\Phi(0,t)=0\). Therefore \(\Phi=-\dot C\). Only actual stationarity, \(\dot C=0\), forces zero net flux. A decreasing enclosed shift charge permits outward flux without any center source. In a plane the corresponding slab law is \(\dot C_{[r_1,r_2]}=\Phi(r_1)-\Phi(r_2)\) per unit transverse coordinate area; there is no regular-center condition unless a symmetry/no-flux boundary is separately imposed.

## All zero-current roots: retain the constitutive dependence

Write \(A(p^2,t)=P_X-W_Y/N\). The equation is
\[
\gamma FKp^2+A(p^2,t)p-\gamma Q^2N'/N^3=0.
\]
It is not a quadratic with a fixed coefficient \(A\). For the actual frozen action,
\[
A=\frac{dU}{\Delta}+3\gamma\bar q\bar H-\frac{d}{N\sqrt S},
\quad \Delta=U-2dQ^2/N^2+2dFp^2,\quad S=1+Fp^2/\ell.
\]
The reference \(\bar q\) is not replaced by physical \(Q\). With
\[
a=\gamma FK,\quad c=3\gamma\bar q\bar H,\quad
e=\gamma Q^2N'/N^3,\quad
B(p)=(ap^2+cp-e)\Delta+dUp,
\]
all zero-current roots are exactly the real \(p\) satisfying
\[
N^2S B(p)^2-d^2p^2\Delta^2=0,\quad
\Delta>0,\quad S>0,\quad pB(p)\ge0,
\]
assuming \(N,d>0\) and the frozen reference margin is positive. The sign condition rejects roots introduced by squaring. This polynomial has degree at most ten; no claim is made that every root is stable or timelike.

Special cases make the logical alternatives explicit:

- \(\gamma=0\): \(p=0\) or \(A(p^2,t)=0\). Inferring \(p=0\) additionally needs \(A\ne0\).
- Flat plane: the cubic radial current cancels, again leaving \(p=0\) or \(A=0\).
- Flat sphere: \(p=0\) or \(A(p^2,t)+2\gamma p/r=0\).
- If \(\gamma Q^2N'\ne0\), even \(p=0\) is not a zero-current root.

For a flat sphere, the nontrivial equation can be written \(rA(p^2,t)+2\gamma p=0\), which is regular at \(r=0\). If \(\gamma\ne0\) and \(A\) is smooth near \(p=0\), its \(p\)-derivative at \((r,p)=(0,0)\) is \(2\gamma\ne0\); the implicit-function theorem therefore supplies a local smooth branch. Writing \(A=A_0+A_Yp^2+\cdots\), SymPy checks
\[
p(r)=-\frac{A_0}{2\gamma}r-\frac{A_YA_0^2}{8\gamma^3}r^3+O(r^5).
\]
For \(A_0\ne0\) this is nontrivial; \(\psi=\psi(0)+O(r^2)\) is center-regular and \(X>0\) sufficiently close to the center if \(Q\ne0\). This is an instantaneous algebraic branch, not a persistent static solution when \(A\) changes with time.

There is also an exact limiting charge identity. Since \(\Box\chi\to3p'(0)=-3A_0/(2\gamma)\),
\[
\boxed{J^t(0)=Q(3W_Y(0)-P_X(0)).}
\]
At the first frozen slice this is negative: \(P_X(0)=0.05352035108375512\), \(W_Y(0)=0.005000000000000001\), and \(J^t(0)=-0.03497001316535539\). Thus this local branch is not an exhibited positive-charge cosmological interior.

## Executed bounded checks

All coefficients are original source evaluations at \((a,m,v)=(1,0.1,0.5)\); \(\gamma=10^{-6}\), physical \(Q=0.9078321505772312\), and the frozen reference \(\bar q=0.9090909090909091\) are distinct.

The first slice is not stationary even at \(Y=0\): \(P_{X\tau}=-0.03228726816147054\), so \(\partial_tJ^t=-0.05862284018258313\). Five tested timelike values \(Y=0,10^{-4},10^{-3},\ell,0.9Q^2\) all have negative \(P_{X\tau}\); its values range from approximately \(-0.03229\) to \(-0.005730\). This finite sample is not a theorem for every field value or epoch.

At \(r=10^{-8}\) on the flat test slice, the regular cubic branch gives
\[
p=-0.0002426015877862721,\quad
X=0.8241591547661502,\quad Y=5.885553039642029\times10^{-8}.
\]
The independently evaluated original covariant and reduced radial currents both have residual \(-1.01644\times10^{-20}\). Yet \(J^t=-0.034969928321310656\) and \(\partial_tJ^t=-0.05862283248915736\). The time derivative here is taken with the static profile held fixed, as required by the specified ansatz. A zero-current profile over a neighborhood therefore cannot simultaneously satisfy that ansatz's scalar equation at this slice.

For comparison, at \(r=1\), exact rational Sturm isolation of the polynomial built from the serialized source snapshot gives five distinct real polynomial candidates. The sign/domain filter accepts \(p\approx-4.3235480154,0,4.6933005399,19.4305563497\), rejecting \(p\approx-24.8424405820\) as a squaring artifact. All three accepted nonzero roots at \(r=1\) are spacelike, \(X<0\), and are not the timelike witness. Root intervals have width at most \(10^{-32}\); exact Sturm checks certify that the filtering signs do not change inside them. This all-roots count is only for the archived rationalized polynomial, not all frozen-action geometries.

Nine unit tests and six result checks passed in the source-pinned run, child exit 0, runtime 1.811373 seconds. The current-input manifest validator exited 0. Source SHA-256:
`fe13aa1f0b7ccbdbfa10b4892fabfacc7866195a20816c029d701079b418efec`.

The task began at commit `73877327897db83402d32e02fe301d240cb6c113`; concurrent work advanced HEAD before the run, whose manifest records `9212f4498479039fb37dba5e71ef8452d28249dd`. All pinned input hashes remained unchanged through execution.

## Exact remaining implication

A localized, positive-charge, stable completion still needs coupled Einstein constraints, the clock equation, the full time-dependent scalar equation, regular central data, exterior matching, and an admissible principal symbol. Nothing here constructs or excludes all such solutions. What is excluded is silently combining a regular stationary charge distribution with nonzero net outward current, or treating an instantaneous cubic zero-current root as a solved stationary charged galaxy.

This audit used computation-audit for bounded provenance, TDD for fail-capable tests, and mathematical proofreading for the report's notation and scope. No Lean file or coefficient function was added or changed.
