#!/usr/bin/env python3
"""CFG487 library (FROZEN_CRITERIA.md section 2a): the settled-fraction clock on ΛCDM top-hat shell histories, and the
mass-conserving edge.  Nothing here is a result; the scripts import it.

Units inside the shell model: H0 = 1 (time in 1/H0), densities in units of the present mean matter density rho_m0.
  shell:   R'' = -GM/R^2 + Omega_L R,  GM = 0.5 Om (1 + d_i) R_i^3 / a_i^3  (CFG353/354 / engine delta_ta convention)
  phases:  start (a_i = 1e-3, pure growing mode) -> turnaround (R' = 0; t_ta, rho_ta) -> R = R_ta / 2 (t_c, 'virialised')
           -> rho stays 8 rho_ta.
  clock:   E = Int_{t_ta}^{t_obs} lambda sqrt(1.5 Om rho / rho_m0) dt,  m = 1 - exp(-E),  lambda = 1.
A shell observed at a_obs with mean enclosed density rho_X is mapped to its turnaround epoch by inverting its present
density; rho_X below the turnaround density at a_obs -> not latched, m = 0.
"""
import math
import numpy as np
from scipy.integrate import solve_ivp, quad

FB = 0.02237 / 0.14237                      # the engine's f_b
EDGE_FAC = 1.0 / math.log(1.0 / (1.0 - FB))  # r_edge / r_M = 5.850
LAMBDA = 1.0


class ShellClock:
    def __init__(self, Om=0.3153, ndi=320, di_lo=9.0e-4, di_hi=0.35, lam=LAMBDA, ai=1e-3):
        self.Om, self.OL, self.lam, self.ai = Om, 1.0 - Om, lam, ai
        self.E = lambda a: math.sqrt(Om / a ** 3 + self.OL)
        self.rows = []
        for di in np.geomspace(di_lo, di_hi, ndi):
            r = self._shell(di)
            if r is not None:
                self.rows.append(r)
        self._tobs_cache = {}

    def t_of_a(self, a):
        """time since a_i (units 1/H0) on the background."""
        return quad(lambda x: 1.0 / (x * self.E(x)), self.ai, a, epsabs=1e-13, epsrel=1e-11)[0]

    def _shell(self, di):
        Om, OL, ai, lam = self.Om, self.OL, self.ai, self.lam
        Ri = ai * (1 - di / 3.0)
        GM = 0.5 * Om * (1 + di) * Ri ** 3 / ai ** 3
        Mfac = (1 + di) * (Ri / ai) ** 3                    # rho / rho_m0 = Mfac / R^3
        Hi = math.sqrt(Om / ai ** 3 + OL)

        def rhs(t, y):
            a, R, V, Eacc = y
            return [a * math.sqrt(Om / a ** 3 + OL), V, -GM / R ** 2 + OL * R, 0.0]
        ev = lambda t, y: y[2]; ev.terminal = True; ev.direction = -1
        s = solve_ivp(rhs, [0, 60], [ai, Ri, Hi * Ri * (1 - di / 3.0), 0.0], events=ev, rtol=1e-10, atol=1e-13)
        if not s.t_events[0].size:
            return None
        t_ta = float(s.t_events[0][0]); a_ta, R_ta, _, _ = s.y_events[0][0]
        rho_ta = Mfac / R_ta ** 3

        def rhs2(t, y):
            a, R, V, Eacc = y
            return [a * math.sqrt(Om / a ** 3 + OL), V, -GM / R ** 2 + OL * R, lam * math.sqrt(1.5 * Om * Mfac / R ** 3)]
        ev2 = lambda t, y: y[1] - 0.5 * R_ta; ev2.terminal = True; ev2.direction = -1
        s2 = solve_ivp(rhs2, [t_ta, t_ta + 60], [a_ta, R_ta, 0.0, 0.0], events=ev2, rtol=1e-10, atol=1e-13, dense_output=True)
        if not s2.t_events[0].size:
            return None
        t_c = float(s2.t_events[0][0]); a_c, R_c, _, E_c = s2.y_events[0][0]
        return dict(di=di, t_ta=t_ta, a_ta=float(a_ta), R_ta=float(R_ta), rho_ta=float(rho_ta), t_c=t_c, a_c=float(a_c),
                    E_coll=float(E_c), Mfac=Mfac, sol=s2.sol)

    def table(self, a_obs):
        """for every shell latched by a_obs: (rho_now / rho_m0, E, E_conservative), sorted by rho_now."""
        key = round(a_obs, 12)
        if key in self._tobs_cache:
            return self._tobs_cache[key]
        tob = self.t_of_a(a_obs)
        lr, EE, EC = [], [], []
        for r in self.rows:
            if r["t_ta"] > tob:
                continue
            g_ta = self.lam * math.sqrt(1.5 * self.Om * r["rho_ta"])
            if tob < r["t_c"]:
                a, R, V, Eacc = r["sol"](tob)
                rho = r["Mfac"] / R ** 3; E = Eacc
            else:
                rho = 8.0 * r["rho_ta"]
                E = r["E_coll"] + self.lam * math.sqrt(1.5 * self.Om * rho) * (tob - r["t_c"])
            lr.append(math.log(rho)); EE.append(E); EC.append(g_ta * (tob - r["t_ta"]))
        o = np.argsort(lr)
        tab = dict(lrho=np.array(lr)[o], E=np.array(EE)[o], Econs=np.array(EC)[o], t_obs=tob,
                   rho_ta_now=self.rho_ta_at(a_obs))
        self._tobs_cache[key] = tab
        return tab

    def rho_ta_at(self, a_obs):
        """turnaround mean density (rho_m0 units) of the shell turning around exactly at a_obs (interpolated in ln a_ta)."""
        a = np.array([r["a_ta"] for r in self.rows]); rt = np.array([r["rho_ta"] for r in self.rows])
        o = np.argsort(a)
        return float(math.exp(np.interp(math.log(a_obs), np.log(a[o]), np.log(rt[o]))))

    def m_of_rho(self, rho_X, a_obs, conservative=False):
        """settled fraction for shells of present mean enclosed density rho_X (rho_m0 units, physical) observed at a_obs."""
        tab = self.table(a_obs)
        rho_X = np.atleast_1d(np.asarray(rho_X, float))
        lr = np.log(np.maximum(rho_X, 1e-300))
        Ev = tab["Econs"] if conservative else tab["E"]
        # monotone envelope in rho (cummax): a denser present shell turned around no later
        Ev = np.maximum.accumulate(Ev)
        E = np.interp(lr, tab["lrho"], Ev, left=0.0, right=Ev[-1])
        E = np.where(rho_X < tab["rho_ta_now"], 0.0, E)      # not yet turned around: latch off
        return -np.expm1(-E), E


def r_edge(Mb, G, a0):
    """mass-conserving edge r_M / ln(1/(1 - f_b)), r_M = sqrt(G M_b / a0) (any consistent units)."""
    return EDGE_FAC * np.sqrt(G * np.asarray(Mb, float) / a0)
