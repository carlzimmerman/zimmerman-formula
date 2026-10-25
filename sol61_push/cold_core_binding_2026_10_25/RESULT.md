# CCT017: the central peak still carries too much internal motion

The new result is stronger than the CCT016 fixed-aperture energy sign. The tested Draco regions do not show independent whole-window self-binding. Their radial phase motion ALONE exceeds their own gravitational binding, even after an optimistic bulk-motion subtraction and omission of every amplitude/angular kinetic term. This is a finite result for the actual saved trial waves, not a statement that no smaller bound subset or other assembly history can work.

## Binding, with the envelope separated

Real C1 cutoffs preserve the measured complex field inside a and taper to zero at b. K includes the cutoff cost. Phi_self is computed once from this cut wave; the surrounding halo is included only in a separate frozen-potential diagnostic, never as an extra force.

At cleanT17.30:

| Window a→b, in193.22pc units | Window mass | K/abs(Wself) | All phase K/abs(Wself) | Radial phase K/abs(Wself) |
|---|---:|---:|---:|---:|
| .75→1 | 29.95million Msun | 12.359 | 6.455 | 3.424 |
| 1→2 | 79.80million Msun | 5.760 | 3.039 | 1.935 |
| 2→4 | 235.17million Msun | 2.556 | 1.404 | 1.062 |

All three self-energies are positive. Bulk translation accounts for only about.020%,.017%,.0033% of K. It does not hide a cold moving core. Cut-wave phase energy and the original wave's phase energy weighted by the same density cutoff agree to better than1.8e-5 relative here, so the phase-energy obstruction is not manufactured by taper amplitude gradients.

The radial quantity is a **lower bound on TOTAL bulk-rest self-energy**, Kradialphase-Pz²/(2M)+Wself. It is not the radial energy component transformed to a COM frame: a boost mixes components. That lower bound is positive in all12 state/window tests: T14.74, T17.30, and T17.50 at dt.01 and.005. The outer-window margin is much weaker than the inner one and is not a continuum radial-convergence certificate. These remain fixed-snapshot diagnostics, not material tracking.

At the measured fixed density, reaching zero whole-window self-energy would require removing about91.9%,82.6%,60.9% of K. Those fractions are conditional energy deficits, not proof that a receiver can remove them. Increasing mass at the same wave shape instead would require roughly370,460,601million Msun in the respective windows; that diagnostic scaling does not solve the prior conditional Draco mass budget and is not applied to any wave.

The full-envelope frozen Hamiltonian can support negative-energy components that the isolated window cannot. Its attraction must not be advertised as an independently bound cold core. Even the SELF frozen Hamiltonian has expectation K+2W, whereas nonlinear self-energy is K+W. MATHEMATICS.md proves the finite spectral-weight bounds and explains why those weights are neither particles nor retained material masses. Positive window energy does not exclude a smaller bound component.

## A simple common assembly change gives the wrong initial ordering

We changed the ORIGINAL incoming radial carrier by one common factor lambda, preserving density, cold supply, eta, residual phase and Jz. The exact finite kinetic form is quadratic. This is a real change to the initial physical phase, not artificial cooling of an already collapsed snapshot.

| Galaxy | lambda where initial whole-wave E changes sign, ne256 |
|---|---:|
| Draco | .682048853 |
| Sextans | .674276848 |
| Fornax | .687029874 |
| Leo I | .686525548 |

As infall is slowed from lambda1, both controls reach negative total energy before the two desired dwarfs. The desired INITIAL global-energy selector would require

    .687029874 <= lambda < .674276848.

That interval is empty. ne128 gives the same ordering; the interval gap changes by1.17e-7. The sign intervals cover the declared[0,1.5] family completely, including the strict-negativity endpoint condition. This rejects only this simple initial-energy-sign selector. Negative total energy is not sufficient capture, and a positive-energy whole wave can contain a bound subset. No evolved control-galaxy overboost or retained dwarf mass is computed by this screen.

## Timestep checks: core sign improves, full-state order is still open

From the same cleanT17.30 seed toT17.50:

| dt | Global energy error | Outward core canonical energy | Core energy change | Core closure residual/transport |
|---|---:|---:|---:|---:|
| .04 | 1.100e-6 | −1.12137e-4 | +1.08205e-4 | 3.507% |
| .02 | 7.047e-8 | −1.10267e-4 | +1.08312e-4 | 1.773% |
| .01 | 4.393e-9 | −1.09206e-4 | +1.08309e-4 | .821% |
| .005 | 2.714e-10 | −1.08135e-4 | +1.08328e-4 | .178% |

The sign remains central canonical-energy GAIN. Fine-endpoint binding/phase diagnostics also remain positive and closely agree. These scalar checks are useful, but energy-defect reduction is NOT full-wave fourth-order convergence: successive complex-wave L2 differences are1.203e-4,6.087e-5,3.711e-5. Phase alignment does not fix this. Most finest error is at r4..8, with substantial higher-azimuth content. Preserve that limitation; do not transfer the scalar rate to the full state or claim a resolved formation history.

## Claude's incoming filter result

Local commit a40c03c62e adds a fixed-source planar Palatini interface with high cold-wave reflection. Its current raw result and manifest were checked read-only; no owner job was duplicated. At the representative cold momentum the d20 case reflects98.957%, and d32/d100 reflect fully. Across the reported linear cases, R+T differs from1 by at most4.12e-10. It supplies an elastic loading filter in its approximation, not an absorptive cooling receiver. Actual environments, abundance, live source work/recoil and its connection to the CCT action remain open. No model result is transferred across that missing bridge. See claude_check.json and LIVE_RECEIVER.md.

## Evidence and limits

FINAL_RESULTS.json is the final collection; the earlier summary.json/summary_v2.json and wave_error.json remain as the actual intermediate analyses rather than being overwritten. Six finite control programs cover Gaussian self-W/K, plane/radial boosts, phase partition, complex cross terms and1000 exact diagonal spectral measures. Scoped independent review found no blocking construction/sign bug and supplied the radial-frame terminology correction. Eleven producer records preserve actual hashes, source revisions, versions, argv, timings and measured memory. All measured runs remained below1GB and the750MB headroom gate; no hard allocation cap is claimed.

The result does not establish cold ontology, a current-action bridge, a settled bound remnant, Sextans formation, control-profile agreement or stellar survival. It identifies a physical task that the mechanism must perform: lower internal cold-wave energy while retaining the required mass AND deriving a selective loading/history rule. NEXT.md and LIVE_RECEIVER.md specify the next tests; none is scheduled.
