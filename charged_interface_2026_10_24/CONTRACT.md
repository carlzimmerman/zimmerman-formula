# CI-1: conserved charge on an interface field

Base70a5f5e4d3847a8584a6021b8d69bbfba7fadc6a. Target unchanged: stable finite
T interior, outer F reservoir, preserved actual interior law. User asks to
continue solving rather than report another untested proposal.

New physical degree of freedom: an independent shift-symmetric field theta
with Ltheta=.5 chi(q,grad q)[theta_dot²-c_theta²|grad theta|²].
chi=chi_s |grad q| is supported on phase interfaces. Its Noether charge is
Q=integral chi theta_dot dV. It is NOT T number, fixed T mass or phase radius.
At fixed Q the minimum temporal kinetic energy is EQ=Q²/(2 integral chi dV).
The quasistatic reduced phase energy is therefore Eparent+k/I, where
I=integral r² |q'| dr in parent units. Positive angular gradients remain in
the underlying theory. This is a NEW effective action, not a microscopic
identification or a claim that existing data determined Q or chi_s.

Regularize |q'| by sqrt(q'²+delta²)-delta, delta1e-5 per dimensionless radius.
The exact zero-interface state has I0 and is inadmissible at nonzero Q. Charge
is confined to the material region, with no imposed radial interface. Vacuum
phase tail remains the parent response tail. Use all mass in gravity.

At a sharp unit jump, I=R² and EQ=k/R²; shrinking gives outward2k/R³.
At jump amplitude a, EQ=k/(aR²), so erasing contrast also costs divergent
energy. This fixes the missing amplitude response of the previous curvature
term, but could favor many interfaces or an overly large converted reservoir.
Those are failure modes to test, not suppress by constraints.

Start from broad local fronts at .4Rreservoir and .7Rreservoir. Both templates,
k=.1,1,10,100, n128:16 minimizations. Keep beta20, ell30 response stiffness,
untapered inherited f.95; no bulk gap, kinematic alignment or curvature term.
The same dimensionless k is a feasibility parameter; it does not yet specify
a universal physical charge-abundance relation across galaxies.

Derive full gradients/Hessian and independent T/F forces. Require phase
stationarity, positive full Hessian, qinner>=.95 in inherited interval,
qouter<=.05 beyond.8R, actual T force close to pure-T control. Count all phase
crossings and test refinement/regularization and perturbed evolution for any
candidate. No boundary or jump amplitude is held fixed during optimization.
