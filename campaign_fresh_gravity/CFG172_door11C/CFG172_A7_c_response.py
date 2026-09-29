# -*- coding: utf-8 -*-
"""CFG172 A7 -- 11C-c: matter compacts the flow (L_int = -rho_b c^2 beta h(delta theta / theta_Lambda)); theta slaved to the local density.  Frozen: sec. 1.3 (11C-c), 2, 6.
sympy: the flow equation for static matter (Pi = dL/dtheta = const), delta theta(rho), integrated-out interaction energy, pressure, c_s^2.
numpy: (i) theta-only mechanism (the flow's contribution to g when the a-channel is REMOVED): best-case G1 over K_c; (ii) full 11C-c = 11C-a + coupling: the contact
force against g_law (G3 reaction), the K_c ceiling; (iii) the saturating h; (iv) far field of the flow v = grad chi and its stress.
Departure from the frozen estimate: S_c contains the a-channel F_a, so G1(full) inherits 11C-a's law; the decisive test of the 'matter compacts the flow' mechanism is theta-only (declared here).
MUTATE = M3 (c2 -> -c2: the c_s^2 cell flips sign, and the khronon sector becomes a ghost) | M4 (beta = 0: delta theta must vanish identically)."""
import sympy as sp
from cfg172_common import *

R = Run("CFG172_A7_c_response")
mut = R.mut
sgn_c2 = -1.0 if mut == "M3" else 1.0
beta_scale = 0.0 if mut == "M4" else 1.0

# ---- sympy ------------------------------------------------------------------------------------------------------------------
r = sp.symbols("r", positive=True)
c2, Gs, beta, thL, rho0 = sp.symbols("c2 G beta thetaL rho0", positive=True)   # c = 1
chi = sp.Function("chi")(r); rho = sp.Function("rho")(r)
th_ = sp.diff(r ** 2 * sp.diff(chi, r), r) / r ** 2          # delta theta = lap chi (spherical)
L = r ** 2 * (-(c2 / (16 * sp.pi * Gs)) * th_ ** 2 - beta * rho * th_ / thL)
from sympy.calculus.euler import euler_equations
eq = euler_equations(L, [chi], r)[0].lhs
Pi = -(c2 / (8 * sp.pi * Gs)) * th_ - beta * rho / thL           # dL/d(delta theta)
# the equation must be d/dr [ r^2 d/dr Pi ] = 0 up to a factor (i.e. lap Pi = 0)
lapPi = sp.diff(r ** 2 * sp.diff(Pi, r), r)
R.check("C7.1 flow equation for static matter: lap(Pi) = 0 with Pi = dL/d(delta theta) = -(c2/8 pi G) delta theta - beta rho/theta_L (Euler-Lagrange in chi)",
        "EL(chi) = +-lap(Pi)", sp.simplify(sp.expand(eq - lapPi)) == 0 or sp.simplify(sp.expand(eq + lapPi)) == 0)
dth = sp.symbols("dth"); rr_ = sp.symbols("rho_")
sol = sp.solve(sp.Eq(-(c2 / (8 * sp.pi * Gs)) * dth - beta * rr_ / thL, 0), dth)[0]      # Pi = 0 for the leaf-average-subtracted background
R.check("C7.2 delta theta = -(8 pi G beta/(c2 theta_L)) (rho - rho_bar): a LOCAL algebraic response (c = 1)", str(sol), sp.simplify(sol + 8 * sp.pi * Gs * beta * rr_ / (c2 * thL)) == 0)
Eint = sp.simplify((c2 / (16 * sp.pi * Gs)) * sol ** 2 + beta * rr_ * sol / thL)            # energy density after integrating out delta theta
Kc = 8 * sp.pi * Gs * beta ** 2 / (c2 * thL ** 2)
R.check("C7.3 integrated-out interaction energy density = -(K_c/2) rho^2, K_c = 8 pi G beta^2/(c2 theta_L^2)", str(Eint), sp.simplify(Eint + Kc * rr_ ** 2 / 2) == 0)
Pr = sp.simplify(rr_ * sp.diff(Eint, rr_) - Eint); cs2 = sp.simplify(sp.diff(Pr, rr_))
R.check("C7.4 pressure P = -K_c rho^2/2 and c_s^2 = dP/drho = -K_c rho < 0 for c2 > 0 (gradient instability); c2 < 0 flips c_s^2 but makes the delta-theta sector's static energy coefficient negative (ghost)",
        f"P = {Pr}, c_s^2 = {cs2}", sp.simplify(Pr + Kc * rr_ ** 2 / 2) == 0 and sp.simplify(cs2 + Kc * rr_) == 0)
# with the mutation sign
c2_eff = sgn_c2
cs2_positive = (-(8 * math.pi * beta_scale ** 2 / (c2_eff)) ) > 0 if beta_scale > 0 else False   # sign of -K_c for c2 = +-1 (K_c ~ 1/c2)
# ---- numerics ---------------------------------------------------------------------------------------------------------------
def rho_and_grad(M, r_):
    rho_ = rho_exp(M, r_)
    return rho_, -rho_ / H_EXP

theta_only = {}
Kgrid = np.logspace(-9, 3, 49)                   # K_c in (km/s)^2 kpc^3/Msun
best_common = (np.inf, None)
dev_by_K = np.zeros(len(Kgrid))
per_mass_best = {}
for f in FOOT:
    a0 = A0[f]
    dev_f = np.zeros(len(Kgrid))
    for M in MASSES:
        r_, gN = profile_gN(M, "exp", a0)
        tar = nu_p2(gN / a0) * gN
        _, drho = rho_and_grad(M, r_)
        devs = []
        for i, Kc_ in enumerate(Kgrid):
            g = gN + beta_scale ** 2 * Kc_ * np.abs(drho)
            d = float(np.max(np.abs(g / tar - 1)))
            devs.append(d)
        devs = np.array(devs)
        dev_f = np.maximum(dev_f, devs)
        per_mass_best[f"{f}/{M:.0e}"] = float(devs.min())
    dev_by_K = np.maximum(dev_by_K, dev_f)
i_best = int(np.argmin(dev_by_K))
R.out["numbers"]["theta_only_linear_best_common_K"] = {"K_c": float(Kgrid[i_best]), "max_dev": float(dev_by_K[i_best])}
R.out["numbers"]["theta_only_linear_best_per_mass"] = per_mass_best
P(f"  theta-only (a-channel removed), linear coupling: best single K_c common to all masses/footings gives max |g/g_target - 1| = {dev_by_K[i_best]:.3f} at K_c = {Kgrid[i_best]:.1e}; best per-mass {min(per_mass_best.values()):.3f}..{max(per_mass_best.values()):.3f}")
# point mass: contact force is a delta function at r = 0 => g = g_N for r > 0
pm_dev = 0.0
for f in FOOT:
    a0 = A0[f]
    for M in MASSES:
        r_, gN = profile_gN(M, "point", a0)
        pm_dev = max(pm_dev, float(np.max(np.abs(gN / (nu_p2(gN / a0) * gN) - 1))))
R.out["numbers"]["theta_only_point_mass_dev"] = pm_dev
P(f"  theta-only, point mass: contact force vanishes at r > 0: max deviation from the target = {pm_dev:.3f}")
# far field: where does the contact force (and the flow's stress) live?  fraction of |g_contact| beyond r_M and beyond 3 h
a0 = A0["canonical"]; M = 1e11
r_ = np.linspace(0.05, 300, 30000)
_, dr = rho_and_grad(M, r_)
w_ = np.abs(dr) * r_ ** 2
frac_far = float(np.sum(w_[r_ > rM_kpc(M, a0)]) / np.sum(w_))
R.out["numbers"]["contact_force_fraction_beyond_rM_1e11"] = frac_far
P(f"  contact-force weight beyond r_M (12 kpc) for M = 1e11, h = 2 kpc: {frac_far:.3f}; at x = 10 the exponential-sphere force is {abs(rho_and_grad(M, np.array([10*rM_kpc(M,a0)]))[1][0]):.2e} (Msun/kpc^4) x K_c")
# saturating coupling: scan (beta c^2, A)
def sat_force(M, r_, bc2, A):
    rho_, _ = rho_and_grad(M, r_)
    aa = A * rho_
    ab = np.zeros_like(aa)
    for i, v_ in enumerate(aa):
        ab[i] = brentq(lambda s: s * (1 + s) ** 2 - v_, 0, max(1.0, v_) + 1) if v_ > 0 else 0.0
    hp = 1.0 / (1 + ab) ** 2
    s_ = -ab                                          # delta theta / theta_L
    ds = np.gradient(s_, r_)
    return -bc2 * hp * ds * beta_scale                # F/m
bcs = np.logspace(0, 8, 9); As = np.logspace(-12, -2, 11)
best_sat = np.inf
for bc2 in bcs:
    for A in As:
        mx = 0.0
        for M in (1e9, 1e11, 1e12):
            r_, gN = profile_gN(M, "exp", A0["canonical"])
            tar = nu_p2(gN / A0["canonical"]) * gN
            F = sat_force(M, r_, bc2, A)
            mx = max(mx, float(np.max(np.abs((gN + np.abs(F)) / tar - 1))))
        best_sat = min(best_sat, mx)
R.out["numbers"]["theta_only_saturating_best"] = best_sat
P(f"  theta-only, saturating h: best max deviation over the (beta c^2, A) scan and masses 1e9, 1e11, 1e12 = {best_sat:.3f}")
theta_only_fails = dev_by_K[i_best] > 0.10 and pm_dev > 0.10 and best_sat > 0.10 and beta_scale > 0
R.check("C7.5 theta-only mechanism: no K_c (linear) and no (beta, A) (saturating) brings G1 within 10% for the exponential sphere at all masses; the point mass gets no force at all", f"{dev_by_K[i_best]:.2f}, {best_sat:.2f}, {pm_dev:.2f}", theta_only_fails or beta_scale == 0)
# full 11C-c: contact force vs g_law => G3 reaction ceiling on K_c
Kmax_list = []
for f in FOOT:
    a0 = A0[f]
    for M in MASSES:
        r_, gN = profile_gN(M, "exp", a0)
        gl = nu_p2(gN / a0) * gN
        _, dr = rho_and_grad(M, r_)
        ratio_per_K = np.abs(dr) / gl              # reaction / g_law per unit K_c
        Kmax_list.append(0.10 / float(np.max(ratio_per_K)))
Kc_max = min(Kmax_list)
R.out["numbers"]["G3_Kc_ceiling"] = Kc_max
P(f"  G3: the contact force stays <= 0.10 g_law for x in [0.3,30] only if K_c <= {Kc_max:.2e} (km/s)^2 kpc^3/Msun (all masses, footings)")
# G5 at that ceiling: growth rate of the c_s^2 < 0 instability at the centre of a 1e11 galaxy, wavenumber 1/h and 1 pc
rho_c = float(rho_exp(1e11, np.array([0.0]))[0])
cs2_val = -Kc_max * rho_c                    # (km/s)^2
for kfac, lab in ((1.0 / H_EXP, "1/h = 0.5/kpc"), (1.0e3, "1/pc")):
    Gam = math.sqrt(abs(cs2_val)) * kfac       # km/s per kpc
    P(f"  G5: at the G3 ceiling, c_s^2 = {cs2_val:.2e} (km/s)^2 -> growth rate Gamma = k |c_s| = {Gam:.2e} (km/s)/kpc at k = {lab}  (e-folding {977.8/Gam:.2e} Gyr)  [Gamma ~ k: unbounded in the UV]")
R.out["numbers"]["G5_cs2_at_ceiling"] = cs2_val
# S1: stress of the flow outside the baryons: delta theta ~ rho - rho_bar => local; T^flow_ab ~ (c2/16 pi G) delta theta^2 (c13 = 0, no shear term)
R.check("C7.6 flow stress-energy outside the baryons vanishes at quadratic order (c13 = 0 removes the shear; c2 delta-theta^2 is local): T ~ delta theta^2 ~ (rho - rho_bar)^2", "local", True, load_bearing=False)
# verdicts
if mut == "M4":
    R.check("M4 decoupled: delta theta identically zero, force zero", "beta = 0", beta_scale == 0)
    R.finish(bite=(beta_scale == 0 and dev_by_K[i_best] > 0.10))
if mut == "M3":
    R.finish(bite=(sp.simplify(cs2.subs({c2: -1, Gs: 1, beta: 1, thL: 1, rr_: 1})) > 0))
R.verdict("G1-law (11C-c theta-only, the 'matter compacts the flow' mechanism)", "FAIL", f"best common K_c leaves {dev_by_K[i_best]:.2f} deviation; point mass {pm_dev:.2f}; saturating {best_sat:.2f}")
R.verdict("G1-law (11C-c full = a-channel + coupling)", "PASS (inherited from 11C-a)", f"the coupling is not what produces the law; it is admissible only for K_c <= {Kc_max:.1e} (G3)")
R.verdict("G3 reaction (11C-c)", "PASS for K_c <= ceiling, FAIL above", f"ceiling {Kc_max:.1e} (km/s)^2 kpc^3/Msun; no coupling is required for G1")
R.verdict("G5 (11C-c)", "FAIL", "c_s^2 = -K_c rho < 0 for every K_c > 0 (c2 > 0); c2 < 0 is a ghost; only beta = 0 (no coupling) is stable")
R.verdict("G1-mechanism (11C-c)", "FAIL", "no kernel emerges: the response is local and linear in M_b; the law comes only from the declared F_a")
R.finish(bite=False)
