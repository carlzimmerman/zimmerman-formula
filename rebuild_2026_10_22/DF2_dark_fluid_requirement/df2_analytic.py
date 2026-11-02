#!/usr/bin/env python3
"""DF2 analytic half. Order-of-magnitude values with assumptions stated in-line. omega 0.12, h 0.675, Om 0.31 from RF5's dust cell, rounded. kappa = 1/2 FITTED; not theory closed."""
import math, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); out = []
def P(s=""): print(s); out.append(s)
MP = 6.77e-20; R0 = 0.12 * 1.8784e-26 / MP; RD = 0.05; c = 299792.458; G = 6.674e-11; Mpc = 3.0857e22; Om, h = 0.31, 0.675
P(f"mean rho, Msun/pc^3: z 0 {R0:.2e}; z 115 {R0 * 116 ** 3:.3f}; z 1100 {R0 * 1101 ** 3:.1f}; z 3000 {R0 * 3001 ** 3:.0f}. Disc anchor {RD}. Mean density crosses the disc's at z {(RD / R0) ** (1 / 3) - 1:.0f}.")
P("\nP cells: c_s km/s (uncapped by c/sqrt 3 here), anchored c_s(rho_disc) = sigma")
P("Gamma  sigma  z 3000   z 1100   z 500     z 50     z 5      z 0")
for g in (7 / 3, 5 / 3, 1.0, 2 / 3, 0.0):
    for s in (30, 100):
        v = [s * (R0 * (1 + z) ** 3 / RD) ** ((g - 1) / 2) for z in (3000, 1100, 500, 50, 5, 0)]
        P(f"{g:5.2f} {s:5d} " + " ".join(f"{x:8.3g}" for x in v))
def H(z): return 100 * h * math.sqrt(Om * (1 + z) ** 3 + 8.4e-5 * (1 + z) ** 4 + 1 - Om) * 1e3 / Mpc
gk = lambda kp, phi: kp / Mpc * phi * (c * 1e3) ** 2
P("\nVariables left, order of magnitude. rec = z 1100, mode k = 0.1 /Mpc comoving, Phi 1e-5, delta 1e-3 of the dark fluid term; disc = 200 km/s at 10 kpc, rho 0.05 Msun/pc^3, scale 3 kpc, sigma 100 km/s; cluster = 1000 km/s at 500 kpc, rho 2e-3 Msun/pc^3 (M 1e14 in 500 kpc gives about 2e-4 to 2e-3), scale 300 kpc, sigma 1000 km/s.")
kp = 0.1 * 1101
g_rec = gk(kp, 1e-5); g_d = (2e5) ** 2 / (10 * 3.0857e19); g_c = (1e6) ** 2 / (500 * 3.0857e19)
P(f" acceleration m/s^2: rec {g_rec:.1e}, disc {g_d:.1e}, cluster {g_c:.1e}; a0 about 1e-10; cH(rec) {c * 1e3 * H(1100):.1e}. Rec sits at or above discs and clusters, for this mode, so an acceleration key doesn't separate rec from discs; clusters and discs overlap. X60, X19 already read this key as failing on systems.")
grad_rec = 1e-3 * kp; grad_d = 1 / 0.003; grad_c = 1 / 0.3
P(f" |grad rho|/rho per Mpc: rec {grad_rec:.3g}, cluster {grad_c:.3g}, disc {grad_d:.3g}. Orders rec < cluster < disc, the one ordering wanted here. Not tested on any system in the record that I found; a gradient key isn't an existing lane's kill. It's a higher-derivative term and has no action here. Stated as open, nothing more.")
abs_rec = R0 * 1101 ** 3 * grad_rec; abs_d = 0.05 * grad_d; abs_c = 2e-3 * grad_c
P(f" |grad rho| Msun/pc^3/Mpc: rec {abs_rec:.3g}, cluster {abs_c:.3g}, disc {abs_d:.3g}. The absolute gradient doesn't give the ordering by the same margin.")
Q = lambda r, s: r / s ** 3
P(f" phase density rho/sigma^3, Msun/pc^3/(km/s)^3: disc {Q(0.05, 100):.1e}, cluster {Q(2e-3, 1000):.1e}; rec needs v at z 1100 from VW1's v0 <= 2 km/s today, so v <= {2 * 1101:.0f} km/s, giving Q >= {Q(R0 * 1101 ** 3, 2 * 1101):.1e}. Conserved along flow, not a local switch: VW1 grades this and finds no window on the Upsilon floor.")
P(" entropy P/rho^Gamma: conserved on smooth flow, so it can't change between rec and a disc without a shock or a source. Needs an unmodelled process in the term itself. It keys on history, not local state. No value is assigned; it has none without a model.")
P("\nStanding kills from the record, not re-derived: the Bullet (no pressure fluid), CMB and transfer windows, J1 potential selector, X19 no single variable or pair separates EXTRA from NONE (keyed on systems), BOLTZ1 shift-symmetric P(X) no turn-on, X22 forest c_s <= 6 km/s at z 3. A local pressure in clusters meets the Bullet regardless of what keys it.")
P("kappa = 1/2 FITTED. Not theory closed.")
open(os.path.join(HERE, "df2_analytic.out"), "w").write("\n".join(out) + "\n")
