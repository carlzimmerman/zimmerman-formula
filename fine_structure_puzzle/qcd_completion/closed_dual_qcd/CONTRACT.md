# FSP-004 closed dual-QCD route CDQ-001

Base checkpoint: FSP-003, navigation bytes at `fine_structure_puzzle/checkpoints/FSP-003_navigation/CHECKPOINT.json.snapshot.txt`. Owner: closed_dual_qcd. Scientific write scope is this directory only. The original physical goal R(alpha)=A_rho(alpha)/mp(alpha)^3 remains open.

Compute a different geometry from the prior centered-ball calculation: center-stabilized pure SU(2) Yang–Mills on a round, closed spatial S3_R times a circle of fixed circumference L. Assume 2 Lambda L << 1, m_W=pi/L, g(m_W)<<1, m_W R>>1, and positive dual mass m with m/m_W<<1. The large-radius stress limit also requires mR>>1. No identification L~R or continuation to physical QCD is authorized by this calculation.

Use f>0 for each individual signed fundamental-monopole insertion, including its matched flat-space one-loop measure and core action. There are two species and their two antiparticles. Their (magnetic,topological) charges are (+1,+1/2), (-1,+1/2), (-1,-1/2), (+1,-1/2). Derive potential -4f cos(theta/2) cos(phi) directly. Write kappa=g²/(8pi²L), kinetic term kappa/2 (d phi)², u=4f|cos(theta/2)| and m²=u/kappa. This fixes convention independently of a factor-two mismatch in the printed source. Stay away from theta=pi mod 2pi, where the leading monopole potential vanishes and omitted operators control the gap.

Required outputs: exact neutral gas/compact-field identity with stated UV prescription; exact constant-sector integral and topology sum; canonical compact measure; full leading saddle plus one-loop massive S3 determinant with bulk subtraction; spatial metric derivative and explicit distinction from W/(LV) and temporal stress. Retain the hard matching functional N_hard[g,L]; no assumption N_hard=1. State any conditional result at fixed local fugacity and curvature coefficients. Do not import a truncated single-monopole ball norm into f.

Success: an actual derived zero or nonzero 1/R coefficient for these retained contributions, with global factors and canonical zero mode treated. Failure: an identified missing matching operator/measure, not an inference solely from a mass gap. Finite numerical checks support formulas only over their declared grid; analytic reductions supply any all-radius/asymptotic statements.

First physical arrow left open: full common-regulator gauge-theory matching on S3_R x S1_L -> curvature/global matching functional and monopole fugacity in the same compact measure. Physical QCD, QED dependence, proton matching, Lorentzian state and fixed-proton path are later arrows.
