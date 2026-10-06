# Root independent reconstruction

The reviewer derives the full stress from the metric variation, not from canonical field energy. With f=|chi|², D=Re(chi*chidot), E=|chidot|², the raw scalar flows are fdot=2D, Ddot=E−3HD−xi R f, Edot=−6HE−2xi R D. They give

rho_c=E+12xi H D+6xi f H²,
p_c=(1−4xi)E+4xi H D+2xi f[(2xi−1/3)R+H²].

Direct symbolic differentiation yields rhodot_c+3H(rho_c+p_c)=0 identically after Hdot=R/6−2H². The difference rho_c−(3M H²−rho_d−rho_r) is exactly minus the Friedmann constraint C. The pressure difference from −M(R/3−H²)−rho_r/3 equals [B R−rho_d−2(6xi−1)E−C]/3. Thus the pressure identity requires both trace and Friedmann closure; using E as the carrier density would fail it.

Root independently validates all five current execution manifests. The exact main has 22/22 checks, the bounded homogeneous history has 40/40. Negative controls fail their declared density, trace and actual-vector geometric checks. Across two DOP853 tolerances and Radau, endpoint scale factors agree within roughly 2e−10 and 5e−11 for the two respective examples. Maximum sampled geometric curvature errors are below 6.1e−13; forward recovery in the declared physical-vector norm is below 3.4e−7. These are bounded floating-point checks, not certified enclosures or an early-era likelihood.

An additional independent endpoint check finds Fdot positive: about 1373.6591 at xi=100 and 25017.7162 at xi=1000. Holding endpoint quantities fixed, the cancellation-safe constraint root has the finite F→0 limit H=(rho_d+rho_r+E)/(3Fdot), about 969.79065 and 19283.64367. This algebraic limit does not prove the evolving solution crosses F=0 regularly, but rules out inferring a homogeneous metric divergence merely from the displayed denominator 2F. F=0 still destroys the positive graviton normalization and the nonsingular Einstein-frame dictionary. The declared positive-F guard is appropriately neither a proved spacetime singularity nor a cold-abundance result.

The archived componentwise forward norm and its failed check remain preserved. The current physical-vector norm is a different specified observable, appropriate for complex fields with zero initial imaginary component; the earlier failed criterion is not retrospectively passed. No author execution input was edited by this review.
