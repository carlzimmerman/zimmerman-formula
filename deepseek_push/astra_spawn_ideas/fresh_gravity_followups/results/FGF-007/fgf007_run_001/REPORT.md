# FGF007 bounded energy comparison

One audited run evaluated all72 declared cases:Q and RAR separately, g0/a in {.1,.01,.001}, amplitude/background ratios {.001,.03,.3,1}, and positive parallel, negative parallel and transverse orientations. K=2. The negative parallel case at ratio1 reaches zero gradient. No parameter grid beyond this domain was added.

The exact field spatial increment after linear subtraction is positive in every tested case. The Hessian estimates cease to be accurate when the perturbation is comparable to its background; decreasing the background with the ratio fixed does not remove the normalized error.

| Amplitude/background | Maximum absolute (exact/Hessian−1) | Maximum absolute (Hessian/exact−1) |
|---|---:|---:|
| .001 | .000333332001 | .000333443148 |
| .03 | .00999996089 | .0101009702 |
| .3 | .0999996846 | .111110722 |
| 1 | .333332800 | .499998800 |

These are maxima over the stated finite cases, not universal error bounds. In percentage terms the worst error relative to exact energy is about0.0333%,1.0101%,11.1111% and49.9999%, respectively. All per-law/per-background/per-orientation values, dimensional restorations and zero-background cubic controls are in numeric_001/results.json.

The separate analytic deep-limit proof gives exact/Hessian ratios1+r/3 and1−r/3 for signed parallel increments and2[(1+r²)^(3/2)−1]/(3r²) transversely. Fixed-background small-amplitude errors scale as r and r², respectively. At zero background the leading energy is cubic and the spatial quadratic stiffness vanishes, while the adopted K=2 time kinetic coefficient remains positive.

There is no claim that the raw energy limits fail to commute:both raw iterated limits are zero. The failure is nonuniformity of the normalized Hessian approximation. At a fixed nonzero absolute perturbation the zero-background Hessian vanishes while the exact increment remains positive; at fixed nonzero background an infinitesimal perturbation is accurately described by the Hessian.

RAR inversion used expm1 and monotone bracketing; its maximum relative inverse residual at60 digits was4.65e-53. Direct increment quadrature and endpoint-primitive evaluation agreed within5.92e-47 at60 digits. The maximum60/90digit relative difference was1.07e-46, below the declared1e-40 tolerance. Q primitive/inverse controls and positive Hessian/speed controls passed. These are high-precision floating checks, not interval-certified error bounds. The independent reviewer has separate responsibility for implementation and interpretation.

The approved runner completed in2.086607 seconds, exit0, with120-second wall,110-second per-process CPU,1 cooperative library thread and1MiB combined-log caps. No memory or CPU-affinity cap was claimed. The manifest validator returned:valid evidence record; mathematical interpretation requires review. Source and artifact hashes were checked; no failed run occurred.

Dimensional outputs restore both9.3619e-11 and1.1279e-10 m/s². W=a²w and field energy density is W/(4piG), with G left symbolic. Fixed x,r frozen-H comparisons rescale gradients by E and energies by E²; this does not hold gradients fixed. Constant-vacuum and evolving-H cases remain distinct, and the latter retains its explicit energy-exchange obligation. No registered M action, empirical source correction, nonlinear PDE/global stability conclusion, ghost, metric/photon result, or theory closure is established.
