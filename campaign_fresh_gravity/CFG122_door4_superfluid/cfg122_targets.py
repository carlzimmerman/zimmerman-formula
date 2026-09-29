#!/usr/bin/env python3
"""cfg122_targets -- the CFG44 target (T) for a given baryon profile, in natural units, on the solver's radial grid.
   (T):  rho_c g_tot = a0 M_b(<r)/(4 pi r^3),  g_tot = G (M_b + M_c)/r^2 self-consistent  =>  M_c' = a0 r M_b/(G M_tot)   (CFG44 Bcommon.cold_mass 'encl').
   Point mass: exactly the P2 phantom (M_c = M (sqrt(1+x^2) - 1)).  Extended baryons: the same ODE (as CFG44 B1)."""
import math
import numpy as np
from scipy.integrate import solve_ivp
from cfg122_common import G_N


def target_on_grid(prof, a0n, r_lo, r_hi, N):
    """returns dict(r, rho_t, Mc, Mtot, gtot) at the N+1 grid nodes; r0 = 1e-3 r_M start on the algebraic P2 value (as Bcommon)."""
    rgrid = r_lo * np.exp(math.log(r_hi / r_lo) / N * np.arange(N + 1))
    r0 = min(r_lo, 1e-3 * math.sqrt(G_N * prof.M / a0n))
    Mb0 = float(prof.Mb(np.array([r0]), a0n)[0])
    uN0 = G_N * Mb0
    u0 = uN0 * math.sqrt(1.0 + a0n * r0 * r0 / uN0) if uN0 > 0 else 0.0
    Mc0 = u0 / G_N - Mb0

    def rhs(s, y):
        r = math.exp(s)
        Mb = float(prof.Mb(np.array([r]), a0n)[0])
        Mt = max(Mb + y[0], 1e-3 * Mb, 1e-300)
        return [r * a0n * r * Mb / (G_N * Mt)]

    sol = solve_ivp(rhs, (math.log(r0), math.log(r_hi)), [Mc0], t_eval=np.log(rgrid), rtol=1e-11, atol=1e-30 * max(prof.M, 1.0), method="Radau")
    Mc = sol.y[0]
    Mb = prof.Mb(rgrid, a0n)
    Mt = Mb + Mc
    gtot = G_N * Mt / rgrid ** 2
    rho = a0n * Mb / (4 * math.pi * rgrid ** 3 * gtot)
    return dict(r=rgrid, rho_t=rho, Mc=Mc, Mtot=Mt, gtot=gtot, Mb=Mb)


def p2_law_g(prof, rgrid, a0n):
    Mb = prof.Mb(rgrid, a0n)
    gN = G_N * Mb / rgrid ** 2
    return np.sqrt(gN ** 2 + a0n * gN)
