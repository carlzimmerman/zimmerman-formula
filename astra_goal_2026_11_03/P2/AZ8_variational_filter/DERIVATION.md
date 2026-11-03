# AZ8 — FAIL for the plug-in variational shortcut

κ = ½ FITTED; not theory closed

Periodic integration by parts gives delta J=integral [u-rho-d_x(Du_x)+D' u_x²/2] delta u. Thus inserting D(u) into AZ2's conservative equation AFTER variation omits a term. Integrating the true Euler equation gives integral rho=integral u+integral D' u_x²/2. If D'>0 and u is nonconstant the last term is positive; the filtered field's integral is not the original source mass. This is a statement about this particular functional, not a universal action obstruction.

For u=1+0.5 cos x and D=0.01(1+u²), the extra integral is 0.01*pi/4=0.007853981633974483. The manufactured conservative solution is not stationary for J: derivative 0.006872233915267144 against the correct oracle 0.0068722339297276735, error 1.45e-11. Constant D gives 2.22e-11, below 1e-8. Omitting the term yields error 0.00687223 and MUTATE bites. All values are from results.json; they are synthetic dimensionless quantities, not astrophysical coefficients.

For D depending on a separate gravitational field Phi, the auxiliary u equation can still conserve its mass, but variation with respect to Phi supplies extra stress terms. Those terms and their effect on the law remain uncomputed. AZ2 remains an incomplete operator construction rather than an action for gravity. Both footings: same identity, empirical rows NOT EVALUABLE.
