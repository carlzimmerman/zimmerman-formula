"""AGB3R (blind re-grade of AGB3): the two-component host-age model, written from AGB3's FROZEN_CRITERIA.md alone.

A host's stars are (1) a part formed at a constant rate s x M over the last T_c and (2) an old part formed in one burst
at formation redshift z_f (burst age T_f = t(z) - t(z_f); flat Omega_m 0.30, H0 70, AGB2's t(z)). By default the
constant part runs since the burst, T_c = T_f (reading of the criteria, see READING.md). The burst mass is what is left
of the observed mass M after the surviving constant part, using AGB2's mass-loss law; if the surviving constant part
alone exceeds M there is no burst and T_c is shortened until it gives M. Progenitor ages are distributed as
SFR(t - tau) x Phi(tau) with AGB2's delay-time distribution; the age used is the mean. log s is clipped to [-13, -8].
Mass cancels. No supernova magnitude is read here.
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
AGB2 = os.path.normpath(os.path.join(HERE, "..", "AGB2_host_mass_step_redshift"))
sys.path.insert(0, AGB2)
import agb2_galaxy as G2                      # imported unchanged: t_of_z, f_ml, delay-time distributions, mass-only ages

LOGS_LO, LOGS_HI = -13.0, -8.0
TAU_MAX, DTAU = 14.0, 1.0e-4                  # Gyr
_TAU = np.arange(0.0, TAU_MAX + 0.5*DTAU, DTAU)


def _cum(f):
    return np.concatenate([[0.0], np.cumsum(0.5*(f[1:] + f[:-1])*DTAU)])


_SURV = _cum(1.0 - G2.f_ml(_TAU))             # S(T) = int_0^T (1 - f_ml) dtau  (surviving mass per unit formation rate)
_PHI, _I0, _I1 = {}, {}, {}
for _k, _fn in G2.DTDS.items():
    _p = _fn(_TAU); _PHI[_k] = _p; _I0[_k] = _cum(_p); _I1[_k] = _cum(_TAU*_p)


def t_of_z(z):
    return G2.t_of_z(z)


def mean_age(logs, z, zf=3.0, dtd="S", detail=False):
    """Mean progenitor age (Gyr) of the two-component host with specific star-formation rate 10**logs per yr at redshift z."""
    logs = np.clip(np.asarray(logs, float), LOGS_LO, LOGS_HI); z = np.asarray(z, float)
    logs, z = np.broadcast_arrays(logs, z)
    sg = 10.0**logs*1.0e9                                       # per Gyr (constant formation rate in units of M per Gyr)
    tf = np.asarray(t_of_z(z) - t_of_z(zf), float)              # burst age
    if np.any(tf <= 0) or np.any(tf >= TAU_MAX):
        raise ValueError("burst age outside the quadrature range")
    s_tf = np.interp(tf, _TAU, _SURV)
    over = sg*s_tf >= 1.0                                       # constant part alone gives (at least) the whole mass
    tc = np.where(over, np.interp(1.0/sg, _SURV, _TAU), tf)
    mb = np.where(over, 0.0, (1.0 - sg*s_tf)/(1.0 - G2.f_ml(tf)))
    phi_f = np.interp(tf, _TAU, _PHI[dtd])
    w_c = sg*np.interp(tc, _TAU, _I0[dtd]); m_c = sg*np.interp(tc, _TAU, _I1[dtd])
    w_b = mb*phi_f; m_b = w_b*tf
    age = (m_c + m_b)/(w_c + w_b)
    if detail:
        return dict(age=age, tc=tc, tf=tf, mb=mb, frac_burst_sn=w_b/(w_c + w_b))
    return age


def mass_age(logm, z, dtd="S"):
    """AGB2's mass-only model (mean age), imported unchanged."""
    return G2.age(logm, z, "mean", dtd)


if __name__ == "__main__":
    ls = [-13, -12, -11, -10.5, -10, -9.5, -9, -8.5, -8]
    crit = {0.05: [10.67, 10.53, 9.34, 7.31, 4.23, 1.75, 0.76, 0.37, 0.13],
            0.5: [6.31, 6.27, 5.89, 5.14, 3.62, 1.75, 0.76, 0.37, 0.13],
            1.0: [3.64, 3.63, 3.52, 3.30, 2.73, 1.70, 0.76, 0.37, 0.13]}
    print("mean age (Gyr), z_f = 3; columns log s = " + " ".join(f"{x:6.1f}" for x in ls))
    worst = 0.0
    for z, ref in crit.items():
        a = mean_age(ls, z)
        worst = max(worst, float(np.max(np.abs(a - np.array(ref)))))
        print(f"  z {z:4.2f} mine   " + " ".join(f"{v:6.2f}" for v in a))
        print(f"  z {z:4.2f} crit.  " + " ".join(f"{v:6.2f}" for v in ref))
    print(f"largest difference from the criteria's table: {worst:.3f} Gyr")
