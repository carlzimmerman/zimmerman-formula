# QX7 frozen criteria: one cold dark energy sector whose stiffness is switched by something other than its own density

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (owner 11-04 rule), reopening a
dust-like sector. Name: COLD DARK ENERGY, never cold dark matter. No particle, no LCDM inputs. Rules: ../SWARM_BRIEF.md.

## Why

QX3 (6a9896ee4b) showed that a K(Q) dust fixes the CMB-lensing shape (chi^2 8.57 on raw PR4) but must be pressureless at
lambda_J <= 0.16 kpc, while galaxies need lambda_J >= ~40 kpc. Every barotropic switch fails, because the early universe is
denser than galaxies. QX5/QX6 (00f9e19c9b, eaafef24d0) showed that clusters need about 4x the law's phantom; that the only
cluster key left is potential depth; and that group depths overlap galaxy depths. QX7 tests a sector whose Jeans length is set
by a variable other than its own density, in two covariant readings:

- iter_1: potential depth read through a scalar that sees the lapse (the owner's hypothesis).
- iter_2: cosmic time read through the khronon / clock (a sector that heats up late), which separates systems by mass and epoch.

Each iteration has its own frozen file, and both share these rules:

- The new constants are fixed ONLY by non-cluster gates: CMB-lensing growth (QX3 machinery, unchanged), galaxy capture, the
  Ly-alpha forest gate, and law-obeying ellipticals. X-COP (35 points, HO1 line |mean| <= 0.05, rms <= 0.10) and the 20
  Lovisari groups (QX5 group rule) are then PREDICTED with no cluster input, over the whole allowed window.
- Both footings, never pooled. QX3 iter2's G1 worst-corner best fit (omega_b 0.0215, H0 65, n_s 0.95, omega_d 0.1196,
  A_s 2.04e-9, framework-native fitted amplitude) is the single background. No Planck parameter value is used.
- Labels per iteration: PASS only if a non-empty window exists AND both cluster predictions pass AND the galaxy-side rechecks
  hold. FAIL otherwise. Every MUTATE must bite, or the label is NO VERDICT.
