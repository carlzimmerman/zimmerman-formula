"""QX17B S-sph step 2: solve the exact static spherical v3s equations (sph_reduce.py) as a BVP.
Criteria FROZEN_CRITERIA.md (9684f63ba8). Geometrized units G = c = 1 (lengths in m), K = 4 pi, mu_K = 0, Lambda = 0.

Exact equations (areal gauge, B = (1 - 2m/r)^(-1/2), Phi = ln N, P = p dr, Pi = D.P):
  m'   = K r^2 (rho_b + Pi + W + gam F)                        Hamiltonian constraint (G_tt)
  Phi' = [ (B^2 - 1)/r + 2K r B^2 (gam F - W + p_m) ] / 2       rr equation, P equation used on shell (checked below)
  gam Pi' = B K W'(Kp/B) - (1 + gam Pi) Phi'                  P equation (E2)
  (r^2 p/B)' = B r^2 Pi                                         definition of Pi
  p_m' = -(rho_b + p_m) Phi'                                    matter (TOV), uniform ball of radius R
Scaled: s = r/Lstar, Y = Kp/a0, Z = K Pi Lstar/a0, Mh = m/M, Pm = K p_m/a0^2, eps = a0 Lstar, ystar = M/(Lstar^2 a0).
WEAK mode: B = 1, eps -> 0, Phi' = m/r^2 (Newtonian), no p_m.  Body: uniform ball, regular centre (Y = s Z/3);
outer: no growing mode, (Z - Z_S) = -k (Y - Y_S) with law-S values at s_out.
Modes: main | KNOWN (galaxy, Lstar = 1e-3 pc) | MUTATE (gamma = 0: algebraic law S, Sun).
"""
import json, os, sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp

HERE = os.path.dirname(os.path.abspath(__file__))
Gs, cs, Msun, pc, AU = 6.674e-11, 2.998e8, 1.989e30, 3.0857e16, 1.496e11
FOOT = {"canonical": (9.3603e-11, 21.7), "alt": (1.1312e-10, 22.9)}
out = {"checks": {}}

# ---- on-shell rr check: T_rr with Pi' from the P equation equals B^2 (gam F - W) ----
B_, p_, Pi_, Phi1, gam_, K_, Wv, Wp = sp.symbols("B p Pi Phi1 gamma K W Wp", positive=True)
Pi1 = (B_ * K_ * Wp - (1 + gam_ * Pi_) * Phi1) / gam_
F_ = Pi_**2 / 2
Trr = -B_**2 * Wv + K_ * Wp * p_ * B_ - p_ * Phi1 * (1 + gam_ * Pi_) - gam_ * p_ * Pi1 + gam_ * B_**2 * F_
out["checks"]["rr_on_shell"] = {"residual": str(sp.simplify(Trr - B_**2 * (gam_ * F_ - Wv))),
                                "pass": sp.simplify(Trr - B_**2 * (gam_ * F_ - Wv)) == 0}

def fW(q):      # K W'(q a0)/a0 with q = K|P|/a0
    return q / (1 - q)
def wW(q):      # K W/a0^2
    return -q - np.log1p(-q)

def lawS_y(gN, a0):         # y = g - g_N, g = [gN + sqrt(gN^2 + 4 gN a0)]/2
    return (-gN + np.sqrt(gN**2 + 4 * gN * a0)) / 2

def solve(M, R, a0_si, Lstar_pc, full, s_out_pc, nodes=6000, tol=1e-7, guess=None):
    """state (x = ln s): Yh = Y/Yref, Zh = Z s/Yref, Mh = m/M, Ph = Pm/Pref (all O(1))."""
    a0 = a0_si / cs**2; L = Lstar_pc * pc
    eps = a0 * L; ystar = M / (L**2 * a0); Sh = R / L
    kb = 3.0 / Sh**3                      # K Lstar^3 rho_b / M inside the ball
    Yref = min(ystar, 1.0)
    Pref = 3 * ystar**2 / (2 * Sh**4)     # Newtonian central Pm of the ball
    def H(s):                             # smoothed ball edge
        return 0.5 * (1 - np.tanh((s - Sh) / (2e-3 * Sh)))
    def rhs(x, U):
        s = np.exp(x)
        Y = Yref * U[0]; Z = Yref * U[1] / s; Mh = U[2]; Pm = Pref * U[3]
        if full:
            twoU = 2 * M * Mh / (L * s)
            B2 = 1 / (1 - twoU); B = np.sqrt(B2)
            q = Y / B
            G = (twoU / (1 - twoU)) / (2 * eps * s) + eps * s * B2 * (Z**2 / 4 - wW(q) + Pm)
            dMh = s**2 * (kb * H(s) + (Z + eps * (wW(q) + Z**2 / 4)) / ystar)
            dB_ds = B**3 * (2 * M * dMh / L - twoU) / (2 * s)   # 2K r^2 rho_tot = 2 dm/dr = 2 (M/L) dMh/ds
            dY = B2 * Z + Y * dB_ds / B - 2 * Y / s
            dZ = 2 * (B * fW(q) - (1 + eps * Z / 2) * G)
            dPm = -(kb * ystar * H(s) + eps * Pm) * G
        else:
            G = ystar * Mh / s**2
            dMh = s**2 * (kb * H(s) + Z / ystar)
            dY = Z - 2 * Y / s
            dZ = 2 * (fW(Y) - G)
            dPm = 0 * s
        return np.vstack([s * dY / Yref, (s * Z + s**2 * dZ) / Yref, s * dMh, s * dPm / Pref])
    s_in = 1e-3 * Sh; s_out = s_out_pc / Lstar_pc
    gN_out = ystar / s_out**2
    Y_S = lawS_y(gN_out, 1.0)
    Z_S = Y_S / s_out
    kk = np.sqrt(2 * (1 / (1 - Y_S)**2 - 1))
    def bc(Ua, Ub):
        # inner: Y = s Z / 3 (no 1/r^2 mode)  <=>  Yh = Zh/3 ; mass of the inner core ; outer decaying mode ; p_m(out) = 0
        return np.array([Ua[0] - Ua[1] / 3, Ua[2] - (s_in / Sh)**3,
                         Yref * (Ub[1] / s_out - Z_S) + kk * (Yref * Ub[0] - Y_S), Ub[3]])
    x = np.linspace(np.log(s_in), np.log(s_out), nodes)
    s = np.exp(x)
    gN = ystar * np.minimum((s / Sh)**3, 1) / s**2
    YS = lawS_y(gN, 1.0)
    Yh0 = ystar * np.minimum(s / Sh, 1.0)
    Y0 = 1 / (1 / np.maximum(YS, 1e-300) + 1 / Yh0)
    Z0 = np.gradient(s**2 * Y0, s) / s**2
    P0 = np.where(s < Sh, 1 - (s / Sh)**2, 0.0)
    U0 = np.vstack([Y0 / Yref, Z0 * s / Yref, np.minimum((s / Sh)**3, 1.0), P0])
    if guess is not None:                 # start from a converged solution (e.g. the weak one)
        x = guess.x; U0 = guess.sol(x).copy()
        if full:                          # Newtonian ball pressure as the p_m start (Ph = 1 - (s/Sh)^2 inside)
            sx = np.exp(x); U0[3] = np.where(sx < Sh, 1 - (sx / Sh)**2, 0.0)
    sol = solve_bvp(rhs, bc, x, U0, tol=tol, max_nodes=3_000_000, verbose=0)
    return sol, dict(a0=a0, L=L, eps=eps, ystar=ystar, Sh=Sh, s_in=s_in, s_out=s_out, Yref=Yref)

def g_of(sol, par, M, s, full):
    x = np.log(s); Y = par["Yref"] * sol.sol(x)[0]
    a0 = par["a0"]
    gN = M / (s * par["L"])**2              # exterior Newtonian field of the bare mass
    return gN, a0 * Y                        # (g_N, extra field y)

mode = sys.argv[1] if len(sys.argv) > 1 else "main"
res = {}
M_sun = Gs * Msun / cs**2; R_sun = 6.957e8
M_gal = Gs * 1e10 * Msun / cs**2; R_gal = 0.5e3 * pc

if mode == "main":
    for foot, (a0si, Ls) in FOOT.items():
        row = {}
        # ---- Sun ----
        sols = {}
        for full in (False, True):
            sol, par = solve(M_sun, R_sun, a0si, Ls, full, s_out_pc=1e5, guess=sols[False][0] if full else None)
            sols[full] = (sol, par)
            row[f"sun_{'full' if full else 'weak'}_status"] = [int(sol.status), sol.message, int(sol.x.size)]
        sol, par = sols[True]
        gstar = M_sun / par["L"]**2
        rs = np.array([1, 10, 100]) * AU
        _, y = g_of(sol, par, M_sun, rs / par["L"], True)
        row["sun_y_over_gstar_1_10_100AU"] = (y / gstar).tolist()
        grid = np.geomspace(10 * AU, 1e-3 * par["L"], 200)
        _, yg = g_of(sol, par, M_sun, grid / par["L"], True)
        row["sun_hedgehog_maxdev_10AU_1e-3L"] = float(np.max(np.abs(yg / gstar - 1)))
        row["sun_hedgehog_pass"] = bool(row["sun_hedgehog_maxdev_10AU_1e-3L"] <= 1e-2)
        far = np.array([1, 3, 10, 30, 100]) * Ls * pc
        gN_far, y_far = g_of(sol, par, M_sun, far / par["L"], True)
        gS = gN_far + lawS_y(gN_far, par["a0"])
        row["sun_g_over_gS_at_1_3_10_30_100_Lstar"] = ((gN_far + y_far) / gS).tolist()
        xs = sol.x; row["sun_min_Z"] = float(np.min(sol.y[1]))  # Zh = Pi-like charge x s; > 0 means on-branch
        # GR remainder: full vs weak on the common exterior grid
        solw, parw = sols[False]
        ext = np.geomspace(2 * R_sun, 1e3 * par["L"], 400) / par["L"]
        yf = sol.sol(np.log(ext))[0] * par["Yref"]; yw = solw.sol(np.log(ext))[0] * parw["Yref"]
        Umax = M_sun / R_sun
        row["sun_GR_remainder_max_rel"] = float(np.max(np.abs(yf - yw) / np.abs(yw)))
        row["sun_Umax"] = Umax
        row["sun_GR_pass"] = bool(row["sun_GR_remainder_max_rel"] <= 10 * Umax)
        # ---- galaxy ----
        sols = {}
        for full in (False, True):
            sol, par = solve(M_gal, R_gal, a0si, Ls, full, s_out_pc=3e6, guess=sols[False][0] if full else None)
            sols[full] = (sol, par)
            row[f"gal_{'full' if full else 'weak'}_status"] = [int(sol.status), sol.message, int(sol.x.size)]
        sol, par = sols[True]
        rk = np.geomspace(1e3, 3e4, 60) * pc
        gN_k, y_k = g_of(sol, par, M_gal, rk / par["L"], True)
        gS = gN_k + lawS_y(gN_k, par["a0"])
        dev = np.abs((gN_k + y_k) / gS - 1)
        row["gal_lawS_maxdev_1_30kpc"] = float(np.max(dev))
        row["gal_lawS_pass"] = bool(np.max(dev) <= 1e-2)
        row["gal_min_Z"] = float(np.min(sol.y[1]))
        solw, parw = sols[False]
        ext = np.geomspace(2 * R_gal, 1e5 * pc, 400) / par["L"]
        yf = sol.sol(np.log(ext))[0] * par["Yref"]; yw = solw.sol(np.log(ext))[0] * parw["Yref"]
        Umax = M_gal / R_gal
        row["gal_GR_remainder_max_rel"] = float(np.max(np.abs(yf - yw) / np.abs(yw)))
        row["gal_Umax"] = Umax
        row["gal_GR_pass"] = bool(row["gal_GR_remainder_max_rel"] <= 10 * Umax)
        res[foot] = row
        print(foot, json.dumps(row), flush=True)
elif mode == "KNOWN":
    for foot, (a0si, Ls) in FOOT.items():
        sol, par = solve(M_gal, R_gal, a0si, 1e-3, False, s_out_pc=3e6)
        rk = np.geomspace(1e3, 3e4, 60) * pc
        gN_k, y_k = g_of(sol, par, M_gal, rk / par["L"], False)
        gS = gN_k + lawS_y(gN_k, par["a0"])
        dev = float(np.max(np.abs((gN_k + y_k) / gS - 1)))
        res[foot] = {"status": [int(sol.status), sol.message], "lawS_maxdev": dev, "pass": dev <= 1e-3}
        print(foot, res[foot], flush=True)
elif mode == "MUTATE":
    for foot, (a0si, Ls) in FOOT.items():
        a0 = a0si / cs**2; L = Ls * pc
        gN = M_sun / (10 * AU)**2
        y = lawS_y(gN, a0)
        ratio = y / (M_sun / L**2)
        res[foot] = {"y10AU_over_gstar_gamma0": ratio, "hedgehog_check_fails": bool(abs(ratio - 1) > 1e-2),
                     "pass_as_mutate": bool(ratio >= 1e3)}
        print(foot, res[foot])
out["mode"] = mode; out["results"] = res
json.dump(out, open(os.path.join(HERE, f"sph_solve_{mode}.json"), "w"), indent=1, default=str)
print("rr_on_shell", out["checks"]["rr_on_shell"])
