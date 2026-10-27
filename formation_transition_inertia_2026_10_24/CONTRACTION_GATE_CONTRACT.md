# FT-I3: dynamically assembling protection

The diffuse FT-I2 pilot completed all 12 trajectories without persistent T.
This continuation changes the constant protection coefficient, not the
previous energy bookkeeping or initial F state. Work must precede protection.

Define Jabs=sum_b m_i |l_i|, R=sum_b m_i r_i/Mb,
Rrot=Jabs^2/(G Mb^3), C(R)=f^2 Rrot/(R+Rrot).
This compares conserved ordered angular motion with a baryonic virial
dispersion estimate G Mb/R. The latter is an effective assumption, not a
computed velocity covariance. No new length scale is fitted; the angular
momentum and initial mass determine Rrot. Contraction increases C while
the phase barrier remains zero with zero first force variation at pure T/F.
Use the same U with C(R) and INCLUDE dU/dC * dC/dR in baryonic forces.
The gate is not an externally scheduled source. A constant-C comparison is
FT-I2. This changes the action, so no previous stability pass transfers.

Initial profile 1, dark scale 30, f=.3,.95; alpha=.3,1,3,10; iota=.01,.1.
Six shells/species, nq=256, duration 12 tdyn, rtol2e-7, 18 seconds/trajectory.
16 runs. Same persistence/energy/RAR gates. New directional derivative and
energy-conservation checks precede integration. Refine an informative result;
do not treat grid/time limits as a physical failure.
