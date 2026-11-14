"""AGB3 two-component host-age model (criteria: FROZEN_CRITERIA.md, section "The two host-age models").

A host of stellar mass M and specific star-formation rate s, seen at redshift z, is split into
  (1) stars formed at a constant rate psi0 = s M over the last T_c, and
  (2) an old population formed in one burst at the formation redshift z_f,
with the burst mass set so that the surviving mass adds up to M (if the constant part alone already exceeds M, there
is no burst and T_c is shortened until it gives M). Progenitor ages follow SFR(t - tau) x DTD(tau), the delay-time
distribution and mass-loss law being those of agb2_galaxy.py. No supernova magnitude is read here."""
import numpy as np

GYR = 977.7922216807891
H0, OM = 70.0, 0.30
SLOPE = 0.030


def t_of_z(z):
    return (2.0/(3.0*np.sqrt(1 - OM)))*np.arcsinh(np.sqrt((1 - OM)/OM)*(1.0 + np.asarray(z, float))**-1.5)*GYR/H0


def f_ml(t_gyr):
    return 0.046*np.log(t_gyr*1.0e3/0.276 + 1.0)


def dtd_childress(t, tp=0.3, alpha=20.0, s=-1.0):
    x = np.asarray(t, float)/tp
    return x**alpha/(x**(alpha - s) + 1)


def dtd_powerlaw(t, tmin=0.04, s=-1.13):
    t = np.asarray(t, float)
    return np.where(t >= tmin, np.maximum(t, 1e-9)**s, 0.0)


DTDS = {"S": dtd_childress, "W": dtd_powerlaw}
_TAU = np.concatenate([[0.0], np.logspace(-4, np.log10(13.5), 6000)])       # Gyr


def _cum(dtd):
    """Cumulative integrals over age on the fixed grid: of DTD, of tau x DTD, and of the surviving mass fraction."""
    phi = DTDS[dtd](np.maximum(_TAU, 1e-12)); phi[0] = 0.0
    tr = lambda y: np.concatenate([[0.0], np.cumsum(0.5*(y[1:] + y[:-1])*np.diff(_TAU))])
    return tr(phi), tr(phi*_TAU), tr(1.0 - f_ml(np.maximum(_TAU, 1e-12)))


_C = {k: _cum(k) for k in DTDS}


def age(logm, logssfr, z, zf=3.0, dtd="S", stat="mean"):
    """Mean progenitor age (Gyr) of each host. logssfr in log10(yr^-1), clipped to [-13, -8]."""
    logm, logssfr, z = np.broadcast_arrays(np.asarray(logm, float), np.asarray(logssfr, float), np.asarray(z, float))
    I0, I1, S = _C[dtd]
    Tf = np.maximum(t_of_z(z) - float(t_of_z(zf)), 0.05)                     # age of the burst, Gyr
    s = 10.0**np.clip(logssfr, -13.0, -8.0)*1.0e9                             # per Gyr
    Sf = np.interp(Tf, _TAU, S)                                               # surviving mass per unit rate after Tf
    full = s*Sf <= 1.0                                                        # constant part fits inside the mass
    Tc = np.where(full, Tf, np.interp(1.0/s, S, _TAU))                        # else shorten it: s x S(Tc) = 1
    burst = np.where(full, (1.0 - s*Sf)/(1.0 - f_ml(Tf)), 0.0)                # formed burst mass per unit surviving mass
    w_c = s*np.interp(Tc, _TAU, I0); m_c = s*np.interp(Tc, _TAU, I1)
    w_b = burst*DTDS[dtd](Tf)
    return (m_c + w_b*Tf)/(w_c + w_b)


def parts(logm, logssfr, z, zf=3.0, dtd="S"):
    """(share of supernovae from the constant part, T_c, burst age) for inspection."""
    I0, I1, S = _C[dtd]; z = np.asarray(z, float)
    Tf = np.maximum(t_of_z(z) - float(t_of_z(zf)), 0.05); s = 10.0**np.clip(np.asarray(logssfr, float), -13.0, -8.0)*1.0e9
    Sf = np.interp(Tf, _TAU, S); full = s*Sf <= 1.0; Tc = np.where(full, Tf, np.interp(1.0/s, S, _TAU))
    burst = np.where(full, (1.0 - s*Sf)/(1.0 - f_ml(Tf)), 0.0); w_c = s*np.interp(Tc, _TAU, I0); w_b = burst*DTDS[dtd](Tf)
    return w_c/(w_c + w_b), Tc, Tf


if __name__ == "__main__":
    print("burst age T_f (z_f = 3) at z 0, 0.05, 0.5, 1.0:", np.round(t_of_z([0, 0.05, 0.5, 1.0]) - float(t_of_z(3.0)), 2))
    ss = [-13.0, -12.0, -11.0, -10.5, -10.0, -9.5, -9.0, -8.5, -8.0]
    print("mean age (Gyr), rows z, columns log sSFR = " + " ".join(f"{x:6.1f}" for x in ss))
    for z in (0.05, 0.3, 0.5, 0.7, 1.0):
        print(f"   z {z:4.2f}  " + " ".join(f"{float(age(10.5, x, z)):6.2f}" for x in ss))
    print("share of supernovae from the constant part at z 0.05:", np.round(parts(10.5, ss, 0.05)[0], 3))
