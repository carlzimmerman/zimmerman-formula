# Independent fixed-anchor derivation, frozen before FGF030 worker inspection

Auditor /root/metric_intake. This source was derived from the FGF030 task and pinned FGF027 parent only; no new FGF030 author proof, code or output was read. It is a fixed-physical-coefficient Q diagnostic family, not an observational comparison or metric theory.

## Common physical scales

Write C=4piG and fix a_c=9.3619e-11 m/s², cs=1e6 m/s, L_c=cs²/a_c, t_c=cs/a_c. Use x=L_c X, t=t_c S, phi=cs² Phi, B=a_c b, g=a_c f, rho_phys=[a_c²/(C cs²)] r, xi=L_c z, delta phi=cs² P and unchanged chi,eta. Energy per transverse area has common scale E_c=a_c cs²/C. All scales are fixed across the four reference choices.

The prescribed physical parameters J=cs^4, S0=a_c², K=c²/cs² and v_chi=cs give tau=K/c²=1/cs² and sigma=J/v_chi²=cs². The dimensionless kinetic form is therefore integral[r z_S²+P_S²+eta_S²]/2; there is no alpha in its two field inertias or in the physical time unit. Physical squared frequencies restore as Omega²/t_c²=(a_c/cs)² Omega² for every member.

Set alpha=a_ref/a_c. The local dimensionless scale is a=alpha exp chi. The common-unit background ODE is

b'=r, r'=−r f, Phi'=f=sqrt(b²+ab), chi'=w,
w'=sinh(2chi)/2−T(f,a).

S0 and J do not acquire alpha² factors: the potential remains U=[cosh(2chi)−1]/4. Initial b=r=1, chi=0, w=1/10000, Phi=0 and endpoint D=.01 are identical in these units and in the specified physical variables. The reference ratio must not be absorbed by redefining units or physical couplings.

Let A=b_f=2f/sqrt(a²+4f²), q=fA−b>0, T_f=q, T(0,a)=0. As alpha is held constant within each static member, T_chi=2T−f q still holds. Thus m=cosh(2chi)−2T+f q. The unchanged full dimensionless potential and kinetic mass forms are

Q=integral{[(r z)']²/r−2(r z)'P+A P'^2−2q eta P'+eta'^2+m eta²}dX,
N=integral[r z²+P²+eta²]dX.

All three perturbations have zero Dirichlet traces. The MOND flux source remains b'=r. Right-wall fields/pressure and total background mass depend on the resulting member; fixed mass means each member's perturbations, not equality across alpha choices.

## Four choices and one independent coarse uniform certificate

The four ratios are1, r_a=112790/93619, E=sqrt(641/200), and r_a E. Since1<r_a<121/100 and1<E<9/5, every ratio is in[1,11/5]. The broader continuous alpha interval is used only as an analytic envelope of the declared four cases, not as a numerical sweep.

Take bootstrap b,r in[.9,1.1], |chi|<=.01, |w|<=.03. Then a>=.99 and a< (11/5)/(1−.01)=220/99<9/4. Therefore1.3<f<2, A>=52/89>1/2 and0<q<=9/8.

For a lower T bound, integrate q(v,a) over the fixed interval[13/20,13/10], which is contained in[0,f]. Rationalizing the constitutive expression gives

q(v,a)=2 a v²/[S(S+a)], S=sqrt(a²+4v²).

Here S<7/2 because (9/4)²+4(13/10)²=4729/400<49/4. Hence S+a<23/4 and

q(v,a)>=[2(99/100)(13/20)²]/[(7/2)(23/4)]
=16731/402500.

Thus T>=217503/8050000>27/1000. The upper bound q<=a/2 gives T<9/4. Also |sinh(2chi)/2|<11/1000. Consequently

−23/10 < w' < −2/125.

Before a first box exit and through D=1/100, these estimates imply

1<=b<=1011/1000,
489/500<=r<=1,
−229/10000<=w<=1/10000,
|chi|<=3/10000.

All are strictly inside the bootstrap box; Phi is bounded by integrating f<2. Smooth local existence and the first-exit contradiction give a regular solution throughout the same physical full length for every declared alpha.

Strictly decreasing w has its first zero Dstar in(1/23000,1/160), obtained by integrating the strict derivative bounds until w0 would be exhausted. Therefore every declared member has a first turn beforeD=.01, and D−Dstar>3/800. These are deliberately coarse analytic bounds, not numerical orbit locations or the worker's constants.

## Independent all-field energy estimate

Using r'=-r f and zero traces, the same valid Young allocations as FGF027 retain (r/2)z'^2+(A/2)P'^2+eta'^2. The negative z² coefficient is bounded by

(11/10)*4+4(11/10)²/(1/2)=352/25=14.08.

Since m>=1−2(9/4)=−7/2, the eta² penalty is at most

4(9/8)²/(1/2)+7/2=109/8=13.625.

Therefore Q>=(1/4)||u'||²−15||u||², u=(z,P,eta). All norms use the same anchor-scaled components. Dirichlet Poincare with pi²>9 andD=.01 gives

Q>=22485||u||²,
Q>=(1499/6000)||u'||²,
N<=(11/10)||u||²,
inf Q/N>=224850/11>20000.

The physical lower bound is (224850/11)(a_c/cs)² for all four members, not a_ref²/cs² times this common dimensionless value. The two dynamical field inertias remain present. No field was statically eliminated, and no Dirichlet rank-one contribution was set to zero as an equality.

This independent coarse certificate establishes a feasible audit route before inspecting the worker. A different sharper or looser valid certificate can be accepted after proof review. Alpha=1 recovers the old anchor Q family; the old sharper bounds remain a control for that member, not automatic bounds for all four. Frozen H(z=1) references are separate stationary comparisons, not cosmological trajectories. Actual a(x) varies, leaving literal pointwise constant-vacuum compatibility unresolved. No RAR/M or filtered-MONO/metric/empirical transfer is claimed.
