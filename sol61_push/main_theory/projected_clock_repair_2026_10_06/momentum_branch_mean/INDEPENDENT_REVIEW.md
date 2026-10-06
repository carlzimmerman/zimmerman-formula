# Independent mixed-mode normal-geometry audit

Accepted in the report's stated scope. The signed a^-3 term survives in the preferred-normal proper-volume mean expansion. It cancels against intrinsic curvature in the actual averaged Einstein constraint and is absent from the calculated normal source density. This is a geometric interference result, not a positive cold population or a full classical second-order inhomogeneous solution.

Frozen pins: REPORT SHA256 `46b68b4129ecb070bb022ccb6181830b6c1a339afee80a2b631d77a119b67f81`; checks `cd54cdf99f72a93e1ecb5898fcab3a21b9ad6521c07c4339b7117fda9008fcc5`; contract `c4d88b9e0c7d040e9e77a152dad344693b0878351bc275437d9336a12a33cd37`. The actual shear-repaired action and its complete scalar reduction were read directly. Independent symbolic calculations below imported no author functions and made no author-input changes.

## Actual momentum branch and chart

For q=az the reduced action gives Pi=2KaKr qdot, Kr=bP/(bH²+P), b=3(1−eta)/eta. Hence qdot=Pi[1/(ba)+H²a/k²]/(2K); direct integration reproduces the reported q. Setting C=Pi H/(2Kk²), d=D0/a and u=CP/(bH²) gives z=C−d−u, nu=d+u, f=Hu, t=−3Hu/eta and e=2(d+u)−3C. The lapse and shift rows are both satisfied. Crucially C is constant while u_dot=−2Hu, and C=bH²u/P is an actual constraint relation, not three independent amplitudes.

Each metric has first spatial logs X=±(nu−2C)cos(kx), Y=±(C−nu)cos(kx), lapse exp[±nu cos(kx)/2], and shifts with derivative determined by the actual shear/shift constraint. Spatial volume is a³exp[∓nu cos(kx)/2]. The sign of q0 is accounted for by q0=−D0; it cannot be changed while retaining the source sign.

## Raw mean sources independently varied

I expanded the exact ADM density with common homogeneous test lapse V and spatial scale Z, retaining the shift advection and shift derivative before division by the lapse. Both Einstein/shear sectors, the geometric-mean matched vacuum and the projected critical gradient term were varied before setting V,Z to zero. Independent expansion and exact cosine/sine averages yield

JV0=Ka³[PC²+H²d²−H²(b+1)u²]/2,
JZ0=Ka³[PC²+H²d²+H²(b+1)u²]/2.

Imposing the physical momentum-branch relation makes the direct residuals against these expressions identically zero. The decay–momentum and decay–C crosses are absent. The two sourced homogeneous trace equations then consistently give F0=−[PC²+H²d²−H²(b+1)u²]/(48H). This is a real raw variation check, independent of the author's source helper.

## Normal trace and weighting independently reconstructed

The exact geometric normal trace is Theta=N^-1[partial_t ln sqrt(gamma)−S partial_x ln sqrt(gamma)−partial_xS]. Substituting the actual first-order shift gives Theta_g1=−bHu cos(kx)/2. Its spatial average is zero but it is not pointwise zero. The first-order volume perturbation is −nu cos(kx)/2.

Before this weighting, the coordinate-average quadratic trace is

average(Theta_g2)=3F0+H(d²−u²)/16.

In particular there is no du cross at this stage. The proper-volume covariance adds

average[(−nu cos(kx)/2)Theta_g1]=bH(d+u)u/8.

The second-order volume correction multiplying the background constant cancels between numerator and denominator of the normalized average. Dividing the trace by three therefore gives

delta H=F0+H(d²−u²)/48+bH(d+u)u/24
       =−PC²/(48H)+bHu²/16+bHdu/24.

The hatted sector gives the same quadratic average because both first signs reverse. The cross bHdu/24=PCd/(24H) indeed scales as a^-3 and can have either sign. Dropping the covariance would erase an actual preferred-foliation geometric effect, not merely change bookkeeping.

## Intrinsic geometry and actual source distinction

I independently integrated the exact spatial curvature with its proper measure. For diagonal logs X,Y,

integral sqrt(gamma)R3=(a/2) integral exp(−X/2+Y)Y_x²,

after the periodic boundary terms cancel. At quadratic order this gives Rbar=P(C−d−u)²/4; linear second-order inhomogeneous curvature averages to zero. The first normal trace variance is b²H²u²/8. The tracefree extrinsic components yield the separate shear average 3H²u²/(4eta²). Homogeneous tracefree corrections cannot alter this normal trace at order two, but their dynamical admission is not thereby proved.

At fixed individual Einstein coefficient M=2K, the normal constraint is Gnn=(R3+2Theta²/3−sigma²)/2. Vacuum subtraction and averaging give precisely

Rbar/2+6H delta H+Var(Theta1)/3−sigmabar²/2=rho_normal/(2K).

Using C=bH²u/P, substitution reduces the right side to rho_normal=KP(d+u)²/4−3KH²u²/(4eta). The a^-3 term contributes +PCd/4 through 6HdeltaH and −PCd/4 through Rbar/2. Those cancel; the remaining density cross KPdu/2 scales as a^-5, not a^-3. Thus neither declaring the expansion cross zero nor identifying it directly as density is correct.

The raw source derivation is also consistent with independent variation: gradient rho1=2Knu_xx/a², the direct gradient rho2=−Knu_x²/(2a²), and its first-volume covariance restores a positive averaged KP(d+u)²/4. The averaged norm-cube lapse divergence is zero at this order, not its local force. The shear lapse variation gives −eta Ksigma². A one-metric conformal spatial variation includes both the geometric-mean volume and projector variation, giving the gradient trace pressure rho_gradient/3; conformal invariance of the shear norm gives its trace pressure equal to its density. These are pressure traces of an inhomogeneous anisotropic source, not perfect-fluid equations of state or a substitute for full covariant conservation. The specified D1=D2=0 and zero relative homogeneous particular correction are essential to the quoted vacuum subtraction.

## Evidence and limitations

Independently validated all four current manifests: main_a 32/32; the covariance, curvature and inferred-dust controls each 31/32 with their sole declared failure. The archived overstrong claim that every geometry cross vanishes is correctly superseded: the faster a^-5 source interference remains. No failed preflight is treated as an admitted physical solution.

The calculation uses an admitted linear branch and solved homogeneous mean trace rows, but it does not solve all second-order inhomogeneous rows. The cosine norm-cube cusp remains a separate classical-regularity issue. The successfully prepared pure-decay f3 formal solution cannot be transferred to this different time branch without its own preparation and full source derivation. Relative homogeneous data, generic phases, matter-era evolution, optical observables, higher-order existence and positive cold abundance remain open. No canonical energy or coordinate mean source has been silently substituted for physical stress, and no coefficient selector follows.
