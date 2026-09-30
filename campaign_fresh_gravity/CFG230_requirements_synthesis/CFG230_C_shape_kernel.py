"""CFG230 script C (CROSS-CHECK): R03 shape and kernel. nu_mono is a transcription of the CFG44 Bcommon construction
(monotone repair of the exponential RAR kernel), rebuilt here from its description in the source, not imported.
MUTATE=M4: the target kernel is swapped from P2 to the simple kernel."""
import math
import numpy as np, sympy as sp
from scipy.optimize import brentq
import CFG230_common as C

R = C.Run("CFG230_C_shape_kernel")
M = C.mode()
R.p(f"CFG230 C. repo=<repo> mode={M or 'main'}")

from CFG230_kernels import *
R.p(f"  nu_mono construction: Y_P = {Y_P:.4f}, h(Y_P) = {H_P:.5f}")

x = np.logspace(-1, math.log10(30), 400); y = 1 / x ** 2     # y = g_N/a0 = 1/x^2 for a point mass
def Mph(nu): return nu(y) - 1.0                              # phantom mass / M under the real-mass reading
# charge function R(x) = 4 pi r^3 rho_ph g / (a0 M) = -2 nu y^2 nu'(y)
def charge(name):
    if name == "P2":   nu = nu_p2(y); dnu = -1 / (2 * y ** 2 * np.sqrt(1 + 1 / y))
    elif name == "simple": nu = nu_simple(y); dnu = -1 / (y ** 2 * 2 * np.sqrt(0.25 + 1 / y))
    else: nu = nu_mono(y); dnu = DHf(y) / y - HMf(y) / y ** 2
    return -2 * nu * y ** 2 * dnu
Rp = {k: charge(k) for k in KERN}
R.p("\n== charge function R(x) = C_model/C_target for the kernel's own phantom (point mass), x in [0.1, 30]")
for k in KERN:
    R.p(f"  {k}: R(x=1) = {float(np.interp(1.0, x, Rp[k])):.4f}; max|R-1| on [0.1,30] = {np.max(np.abs(Rp[k]-1)):.4f}")
R.check("CROSS-CHECK", "P2: R = 1 exactly (Lean PointMass; CFG44 R = 1.0000)", np.max(np.abs(Rp["P2"] - 1)) < 1e-9)
xs1 = np.array([1.0]); y1 = np.array([1.0])
Rm1 = float((-2 * nu_mono(y1) * y1 ** 2 * (DHf(y1) / y1 - HMf(y1) / y1 ** 2))[0])
R.check("CROSS-CHECK", "nu_mono R(x = 1) = 1.4629 (CFG44 B1 N5; correction of the 'up to 2%' line)", abs(Rm1 - 1.4629) < 0.015, f"{Rm1:.4f}")
# the CFG44 statement 'max|R-1| over x in [1e-3,1e3] = 1.021'
xw = np.logspace(-3, 3, 4000); yw = 1 / xw ** 2
Rw = -2 * nu_mono(yw) * yw ** 2 * (DHf(yw) / yw - HMf(yw) / yw ** 2)
R.check("CROSS-CHECK", "nu_mono max|R-1| over x in [1e-3,1e3] = 1.021 (CFG44)", abs(np.max(np.abs(Rw - 1)) - 1.021) < 0.03, f"{np.max(np.abs(Rw-1)):.3f}")
R.p("  VERDICT GATES_STATUS 5.12 ('nu_mono departs by up to 2%'): stale as worded, as CFG44's own appended correction says; this script recomputes R(1) = 1.4565 with a transcription of the construction (CFG44 prints 1.4629; 0.4% apart, not bit-exact).")

R.p("\n== phantom mass under the real-mass reading, M_ph/M = nu - 1, against P2's sqrt(1+x^2) - 1")
dev = {}
for k in ("simple", "nu_mono"):
    d = Mph(KERN[k]) / (np.sqrt(1 + x ** 2) - 1) - 1
    dev[k] = float(np.max(np.abs(d)))
    R.p(f"  {k}: max |M_ph/M_ph(P2) - 1| over x in [0.1,30] = {dev[k]:.4f}")
R.res["phantom_deviation_vs_P2"] = dev
# Verlinde (sympy): C_V/C_target
xs, rr, Mv, a0s, Gs = sp.symbols("x r M a0 G", positive=True)
rMs = sp.sqrt(Gs * Mv / a0s)
MD = sp.sqrt(a0s * rr ** 2 / Gs * sp.diff(Mv * rr, rr))
rho = sp.diff(MD, rr) / (4 * sp.pi * rr ** 2)
gtot = Gs * (Mv + MD) / rr ** 2
CV = sp.simplify(rho * rr ** 3 * gtot / (a0s * Mv / (4 * sp.pi)))
CVx = sp.simplify(CV.subs(rr, xs * rMs))
R.p(f"\n  Verlinde point mass C_V/C_target = {CVx}")
vals = [float(CVx.subs(xs, v)) for v in (0.1, 1, 3, 10, 30)]
R.p(f"  at x = 0.1, 1, 3, 10, 30: {['%.4f' % v for v in vals]}")
R.check("CROSS-CHECK", "Verlinde (1+x)/x: 11, 2, 1.33, 1.10, 1.03", sp.simplify(CVx - (1 + xs) / xs) == 0 and abs(vals[0] - 11) < 1e-9)
R.p("  note: C_target = a0 M/(4 pi) does not depend on the kernel, so the Verlinde ratio is kernel-independent (see M4).")

if M == "M4":
    # swap the target kernel to 'simple': which R03 numbers move?
    moved = {"phantom mass, P2 vs simple (max rel diff)": dev["simple"], "Verlinde C_V/C_target at x = 1": (2.0, 2.0)}
    p2_vs_simple = float(np.max(np.abs(Mph(nu_simple) / Mph(nu_p2) - 1)))
    ratio11 = float(nu_simple(np.array([1.0]))[0] / nu_p2(np.array([1.0]))[0])
    R.p(f"  M4: with the simple kernel as target, the required phantom mass differs from P2's by up to {p2_vs_simple:.3f} (relative) on [0.1,30]; nu ratio at y = 1: {ratio11:.4f}")
    R.p("  the Verlinde ratio does NOT move under M4 (C_target is kernel-independent): my frozen expectation that it moves was WRONG, kept.")
    R.res["M4"] = {"phantom_rel_diff": p2_vs_simple, "verlinde_moves": False}
    C.bite(R, p2_vs_simple > 0.10, f"R03 phantom-mass profile moves by {p2_vs_simple:.2f} > 10% between kernels; kernel-independent items: C_target, the Verlinde ratio, R01 window, R02 dimensional statement")
R.write()
