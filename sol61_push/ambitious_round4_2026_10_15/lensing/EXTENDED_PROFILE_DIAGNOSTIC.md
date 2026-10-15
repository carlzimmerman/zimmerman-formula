# Additional post-data physical profile falsifier

This diagnostic is registered after the baseline failure and linear profile
relaxations, before its own fit. It does not alter baseline closure criteria.
Replace compact baryons by finite-total-mass Plummer baryons, with cumulative
m_b(x)=x³/(x²+u²)^(3/2), u=rb/rM, total Mb. Apply the same spherical exact
acceleration algebra to the actual distributed source:
m_ex(x)=[sqrt(m_b(x)²+4*x²*m_b(x))-m_b(x)]/2.
Differentiate this enclosed excess to obtain density. Terminate its mass at
m_ex(e)=5.364*N, solve e at each trial, and use this actual physical edge
for the environmental exclusion. Baryons retain the finite Plummer tail.

All-radius native_h data and covariance, same environmental template. Fit
four log Mb in [9.5,12], four physical Plummer radii rb in [0,.3] Mpc and
four NNLS-profiled nonnegative biases. Four deterministic starts and
least-squares cross-check. Nominal n-12 p only. Controls before its fit:
rb=0 returns baseline point profile to .1%; 64/128-node projection
stability <=.1%; exact cold mass boundary residual <=1e-9; positive density
on 1000 test radii per fixed input. Double environmental table resolution
or direct evaluation at best-fit edges must alter chi² by <.5.

Decision: p>=.01 with bounded radii would identify baryon extent as a
viable profile-level explanation in this expanded family, needing external
baryon/gas constraints and full metric/action treatment. Failure even with
this freedom rejects this particular simple profile remedy at the stated
footing. No free-shape diagnostic is a physical production or ownership proof.
Each command remains <=60 sec wall, <=55 sec per-process CPU, threads=1.
