# LD-2 correction to numerical route, not a new mechanism

LD-1 includes nonstationary and unphysical saturation-continuation states;
none establishes equilibrium. Change density variables to direct nonnegative
cell masses, constrain their sum exactly, and require actual enclosed-T u<=.97
with analytic Jacobian. Endpoints touching this numerical cap are not physical
solutions. Quadratic radial mesh resolves inner .5b..5b at n64. Same energy
and no imposed dark profile. Test the four explicit parameter cells in code.
Check density KKT residual including empty-cell activation, constraint slack,
phase residual, law, outer mass, phase and saturation. SLSQP stopping is not
proof of stationarity. This corrects softmax freezing rather than interpreting
LD-1 failures as physics. Total available mass, supplied Q and gas closure
remain explicit assumptions from LD-1.
