# Padding and saved-state checks

Independent review asks for nonlinear padding sensitivity, raw momentum
residuals before reconstruction, and spectra of fields besides q. Extend
padding factor to 5 for n31 at t=.5, same dt=.0025. Compare physical q,N,b,pb
on the common n31 grid against factor3 n31/63 and half dt runs. Record raw
coarse/lifted momentum, projection correction and idempotence. Require raw
normalized momentum<1e-7 and inspect relative physical-field changes.
Inspect upper-third spectral energy of beta,r,pb,N as well as q. Do not call
finite padding an exact Galerkin method for nonpolynomial expressions.
