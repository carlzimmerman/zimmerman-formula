# Source family and failed-branch continuation

Preserve the false-phase run, including its gamma8 Sigma0.1 root failure:
a BVP failure inside a valid bracket returned None to brentq, causing a TypeError.
This is an incomplete numerical attempt, not evidence of physical nonexistence.
Retry with radial continuation from nearby converged profiles. Also test source
multipliers0.5 and2 for gamma8 Sigma0.2 DeltaV=-0.03, comparing the baseline S1.
Use radial scan0.5..40,20 points, continued BVPs and coupled moving-wall grids
96/144. No fitting to1/2 or observational masses.240seconds single thread.
Record all failures, root branches, radial eigenvalues, flatness and speed/supply
ratios. This is a conditional family with fixed phase inputs, not proof of
unique phase microphysics, nonspherical stability or cosmological survival.
