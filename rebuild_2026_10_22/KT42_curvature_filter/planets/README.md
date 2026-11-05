# Supplementary planetary test: the radial anomaly survives the full adjoint

All 16 tested planet/filter/footing combinations fail the repository's
existing AZ11 radial and AZ12 monopole-precession diagnostics. The total
anomalous inward acceleration stays close to a0 after including the full
returned B stress. These are supplementary monopole diagnostics, not a
refitted ephemeris likelihood or a replacement of the original Cassini and
Milky Way cuts.

The tested Gaussian curvature widths are 0.1, 1, 100 and 300 pc; p=9/8,
ell=3kpc, baryons, acceleration footings and external field are fixed.
The 0.1pc case is particularly useful: it passed the retained Cassini Q2
amplitude test, yet its radial anomaly fails this separate screen strongly.

## Full force and retained cuts

`DERIVATION.md` gives two independent exact expressions for the B monopole:
an integrated-by-parts Gaussian vector convolution and an enclosed-source
Gaussian-ball Hessian pairing. Both include the outer adjoint. The physical
anomaly used below is a0*(g_A+g_B), never A alone.

At Saturn:

| Filter width (pc) | Canonical A/a0 | Canonical B/a0 | Canonical total (m/s^2) | Alternate total (m/s^2) |
|---:|---:|---:|---:|---:|
| 0.1 | 1.00002848 | -0.000144445 | 9.35921e-11 | 1.13106e-10 |
| 1 | 0.99999855 | -0.0139183 | 9.23001e-11 | 1.11709e-10 |
| 100 | 0.99999855 | -5.53106e-14 | 9.36029e-11 | 1.13120e-10 |
| 300 | 0.99999855 | -9.98531e-17 | 9.36029e-11 | 1.13120e-10 |

The returned B term cancels at most 1.39% of a0 in these Saturn cases;
it does not remove the constant radial tail. At Mars the greatest tested
cancellation is 0.222% of a0. This is an evaluated property of these fixed
cases, not a sign or magnitude bound for arbitrary sources or widths.

AZ11's unchanged acceleration errors are
sigma_Mars=5.6756756757e-15 m/s^2 and
sigma_Saturn=9.6808510638e-15 m/s^2. Its gate is Z=abs(anomaly)/sigma<=2.
AZ12's unchanged generous rate errors are 0.0015 mas/year for Mars and
0.0065 mas/year for Saturn, also with Z<=2.

| Planet | Canonical radial Z range | Alternate radial Z range | Canonical orbit Z range | Alternate orbit Z range |
|---|---:|---:|---:|---:|
| Mars | 16455.4–16492.0 | 19891.1–19930.7 | 16704.8–16760.4 | 20194.8–20255.1 |
| Saturn | 9534.29–9668.87 | 11539.2–11684.9 | 9522.28–9725.32 | 11533.2–11753.1 |

The orbit numbers use the actual computed radial profile in AZ12's
first-order eccentric-anomaly average. The resulting Saturn precession is
-61.895 to -63.215 mas/year canonical, and -74.966 to -76.395 mas/year
alternate. Mars gives -25.057 to -25.141 and -30.292 to -30.383 mas/year.
Thus the large disagreement is not an artifact of replacing the radial
profile by a constant acceleration when translating its effect into a rate.

Only the monopole part of the force is orbit averaged. Higher multipoles,
orbital orientation, fitted initial conditions and parameter covariance
are not included. The archived ephemeris error summaries are reused as
requested, not reauthenticated or promoted to a joint likelihood. No
complete RQ3 scorecard or universal observational exclusion is claimed.

## Why the radial signal returns

For every fixed positive curvature-filter width, H_a is finite near the
source. The unfiltered Solar gradient instead grows as GM/r^2. Sufficiently
close to the Sun, x dominates the finite curvature contribution s^p, and
the simple high-field response gives A approximately a0 times the radial
unit vector. The returned B force is smooth there and its monopole begins
linearly in r. It cannot cancel a constant radial tail in that limiting
regime. The finite-radius calculation above establishes that the actual
tested Mars/Saturn configurations lie close to it.

The limit is ordered: first fix positive filter width, then approach the
source. It does not prove that every positive width fails at a fixed
planetary radius. Sending the filter width to zero first recovers KT39;
no uniform all-width exclusion follows from the origin argument.

## Controls, review corrections and provenance

The physical run `run_001` completed in 2.15s with 98/98 recorded controls.
Its largest coarse/fine change was 4.56e-12 in radial Z and 3.18e-10 in
orbit Z, against the fixed 1e-5 convergence gate. Both the radial grid and
angular/orbit orders were increased, and the Gaussian integration domain
expanded from 16 to 24 filter widths.

The independently evaluated enclosed-ball B acceleration differs from
the vector-convolution result by at most 3.47e-18 in units of a0, with
maximum relative difference 5.52e-16. The linear-in-radius B approximation
was reported only as a control: its largest discrepancy from the exact
force was 8.04e-12 in units of a0. All physical grades use the exact force.

Independent code review identified two control-scope gaps and one reporting
correction. They were addressed in a separately contracted `controls_001`
run; original inputs and results remain immutable:

- The original literal-zero-force check tests the orbit integrator only.
  The supplementary run injects R=1 through the actual primitive API and
  executes the A, B, Gaussian-ball and orbit pathways; every result is
  exactly zero.
- The original plain-QUMOND comparison is not an omitted-return mutation.
  The supplementary run evaluates B without its outer adjoint. For the
  canonical 0.1pc Saturn case it incorrectly gives about +1.6843e6 a0,
  compared with the correct -0.000144445 a0. The independent derivative
  refinement confirms this is a meaningful mutation.
- The original `max_i1_argument` field describes the semimajor axis.
  The supplementary record includes the larger aphelion bound. Its maximum
  is 0.0117488, within the declared 0.02 series domain; six/eight terms
  agree at working precision. The factorial series remainder is negligible
  on that domain.

All five supplementary controls pass. Constant, harmonic and inverse-square
orbital-force oracles are also checked. Successful manifests record the
contracts, exact argv, unchanged source hashes, one-thread execution,
Python 3.13.9, NumPy 1.26.4 and SciPy 1.14.1. The derivation and code were
independently reviewed by the phase auditor; see its separate planet audit.

The model retains GM=6.6743e-11*1.98892e30 in both its field and Kepler
frequency, exactly as KT39/KT42. This is 0.0256551% above AZ11/AZ12's
1.32712440018e20 ephemeris GM; that difference is explicitly recorded and
not silently absorbed by changing the Sun. The existing planet radii,
eccentricities and errors are reused. Similarly, the current raw uniform
GEXT/a0 is preserved; AZ11/AZ12's different external-field conversion is
not imported. Real Galactic gradients and Solar interior structure remain
outside this benchmark.

Use the exact argv in `run_001/manifest.json` and
`controls_001/manifest.json` with new output directories for reproduction.
No prior source, result or acceptance cut was edited.
