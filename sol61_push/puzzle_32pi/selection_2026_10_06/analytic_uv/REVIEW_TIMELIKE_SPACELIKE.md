# Fresh independent audit: one P(X), clock and physical metric

Verdict: **the force normalization and local principal-symbol obstruction are correct under the stated frozen weak-field source and fixed-clock assumptions**. The lapse calculation is a scoped failure of the displayed baryon-dominated rescue, not a fully backreacted no-go. The report correctly separates Einstein vacuum curvature from observed Jordan cosmology and leaves32pi unselected. I reconstructed the equations and inspected the actual checks, rather than adopting the test count as a verdict.

Audited source hashes: `../timelike_spacelike/REPORT.md` SHA256`f68d2740a06a5f86c2c842a77032e787b4a90ae8a415740b4db06c9c6cc48bd9`; `checks.py` SHA256`8d513b123adc3cecd376ee723ed1b6c6bc6ba6470a1298183bca5abc43583bd2`. I did not run the peer script because it writes its peer folder. Independent symbolic reconstruction was read-only and confirmed determinant, normalized force and vacuum factors.

## Variation and actual normalization

With signature(-+++), X=−(partial phi)²/2, scalar variation gives div(P_X partial phi)=−alpha T_m. Conformal A=exp(alpha phi) gives delta S_m=alpha T_m delta phi, so for nonrelativistic matter at the comparison epoch A=1 the positive monopole source is alpha rho_b. The scalar stress divergence is−alpha T_m partial^nu phi, opposite the reported matter exchange. The weak Jordan test potential is Phi_E+alpha phi, hence inward acceleration magnitude G_T M_b/r²+alpha u for u=psi'>0. Both source and test factors of alpha are required.

On P=P0−C(−X)^(3/2), X=−u²/2, P_X=3C u/(2sqrt2)=gamma u. Spherical flux yields r² gamma u²=alpha M_b/(4pi). Squaring the test scalar force gives (alpha u)²=G_T M_b a0/r² with a0=alpha³/(4pi gamma G_T). The report's normalized coefficient is exact in this declared approximation. It does not identify tensor G_T with a Cavendish constant containing scalar exchange, or supply a screened high-acceleration completion.

At a vacuum timelike condensate P_X(X_t)=0, T_phi=P(X_t)g, rho_v=−P(X_t). Then Lambda_E/a0²=128pi³ gamma² G_T³ rho_v/alpha⁶. The target32pi is equivalent to rho_v=4a0²/G_T; no scalar stationarity equation fixes this value. Adding a constant to P exactly changes this curvature while preserving derivatives and scalar source equations; gravitational predictions need not remain unchanged. The field-rescaling dictionary alpha→alpha/s,gamma→gamma/s³ preserves a0, as claimed. The polynomial offset-shape example leaves stated derivative jets and leading small-|X| coefficient; it does not prove intermediate/global health.

## Principal tensor and clock obstruction

Linearizing the scalar equation at fixed metric gives K^{mu nu}=P_X g^{mu nu}−P_XX partial^mu phi partial^nu phi. On a pure timelike background, time coefficient P_X+2X P_XX and spatial coefficient P_X have the stated signs. At the condensate with X_t>0,P_XX=kappa>0 the time coefficient is2X_t kappa but the k² spatial term vanishes. Higher-derivative completion is therefore an extra obligation.

On the pure spacelike cubic, P_XX=−gamma/u, so longitudinal coefficient P_X+2X P_XX=2gamma u; transverse/time coefficients gamma u. Thus longitudinal speed²2 is correct relative to the Einstein light cone and its conformal Jordan light cone. Hyperbolicity and stipulated subluminality are distinct requirements.

For phi=q t+psi(r), X=(q²−u²)/2. A static sourced u=A_M/r requires P_X=gamma u along its branch, hence P=P(X_t)−gamma(q²−2X)^(3/2)/3 and P_XX=−gamma/u. Direct reconstruction gives

    K^{tt}=gamma(q²/u−u),
    K^{tr}=−gamma q,
    K^{rr}=2gamma u,
    det(K_tr)=gamma²(q²−2u²).

With transverse gamma u>0, determinant<0 is exactly the Lorentzian regime u>|q|/sqrt2. Below it, K_rr>0 and positive determinant make the entire two-coordinate block positive definite. At equality it degenerates. The original matter t-slicing has positive scalar time kinetic coefficient only for u>|q|; Lorentzian signature between thresholds does not make that slicing suitable. These are scalar fixed-background principal statements, not a full coupled metric/matter Hamiltonian or characteristic audit.

The radius uses sqrt2 A_M/|q|; the report's positive-q formula agrees with its numerical/check convention. The q=0 limit removes this fixed-clock obstruction and is not a timelike condensate. For a smooth time-healthy endpoint, delta X=−u²/2 gives P_X=−kappa u²/2+O(u⁴)<0. Positive baryon charge and attractive u>0 then have incompatible flux signs. This separate local argument correctly avoids dependence on an exact cubic law.

## Lapse, source stationarity and Jordan caveats

In ds²=−N²dt²+A_r²dr²+r²dOmega², sqrt(-g) times the radial scalar current is N r² P_X psi'/A_r=N r² P_X u. Integration of the source has matching lapse/radial-volume weights, so the exact kinematical dictionary in the report is correct. Expanding N=1+Phi_E gives delta X=−q² Phi_E−u²/2: a negative gravitational potential can change the near-condensate flux sign. It invalidates an extrapolation of the flat-clock obstruction to every gravitational solution.

For the explicitly assumed baryon lapse Phi_E=−G_T M_b/r, substituting u=v/r gives leading flux kappa v q²G_T M_b−kappa v³/(2r). Matching alpha M_b/(4pi) gives v=alpha/(4pi kappa q²G_T), independent of source mass. This fails MOND's sqrt(M_b) amplitude. Scalar density perturbation is delta rho≈q² kappa delta X, with leading kappa q⁴G_T M_b/r. Its enclosed mass grows asr², so the baryon-lapse approximation eventually fails. The report explicitly leaves the backreacted repair open; no global conclusion follows from taking its formal r→infinity limit beyond the controlled region.

The conformal coupling also makes source stationarity approximate: masses/stress in Einstein variables can change with A=exp(alpha q t), and the full matter action is not shift symmetric. Thus the fixed static monopole used for the local analysis is a frozen-epoch assumption, not an exhibited exact stationary solution of all matter/scalar equations. This is already consistent with the report's declared slowly changing weak conformal background. Corrections require care near vanishing P_X or principal margins, where small absolute changes can dominate. An exact full-action stationary interpretation would require an additional source/time-evolution argument.

Finally d tau=A dt,a_J=A a_E implies H_J=(H_E+alpha q)/A and G_T,J=A²G_T for the tensor normalization. Therefore generic Einstein deSitter with a nonzero conformal clock is not constant-H_J physical deSitter. With signed q there is the trivial exceptional cancellation H_E+alpha q=0, giving H_J=0 and a static flat physical cosmology, not observed positive-curvature deSitter. The check uses q>0, where no such cancellation occurs. G_T,J is not a measured total fifth-force-inclusive Newton constant. The report's C_v is consequently an Einstein-frame diagnostic rather than an observed Jordan-frame ratio.

## Smallest remaining implication

A sourced, physically normalized, coupled scalar/metric/matter solution must first establish the common clock/galaxy boundary and principal health, including lapse/backreaction and any higher-derivative operators, while retaining sqrt(M_b) force scaling. It must then predict a vacuum-to-force coefficient and physical-frame cosmology. The current report proves useful failures of simpler hypotheses; it does not provide either implication or a32pi selector. No material algebraic error was found in the audited revision.
