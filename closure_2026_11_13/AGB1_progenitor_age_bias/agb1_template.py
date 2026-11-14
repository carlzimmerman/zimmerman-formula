"""AGB1 correction templates (criteria: FROZEN_CRITERIA.md, section "The correction template").

T(z) = 0.030 mag/Gyr x [median progenitor age at z = 0 - median progenitor age at z].
The progenitor-age distribution at redshift z weights each age tau by SFH(z_form(t(z) - tau)) x DTD(tau)
(Childress et al. 2014). No supernova magnitude is read here.

  kind "S": Behroozi et al. (2013) star-formation history, Childress et al. (2014) delay-time distribution with a
            prompt time of 0.3 Gyr and slope -1 (the recipe Son et al. 2025 state, as described by Wiseman et al. 2026).
  kind "W": Madau & Dickinson (2014) star-formation history, power-law delay-time distribution of slope -1.13 from 40 Myr.
"""
import numpy as np

GYR = 977.7922216807891            # 1 / (1 km/s/Mpc) in Gyr
BG = (63.6, 0.353, -0.42, -1.75)   # H0, Omega_m, w0, wa of the age-redshift relation (frozen)
SLOPE = 0.030                      # mag / Gyr (Son et al. 2025)


def e_cpl(z, om, w0, wa):
    a = 1.0/(1.0 + z)
    return np.sqrt(om*(1 + z)**3 + (1 - om)*a**(-3*(1 + w0 + wa))*np.exp(-3*wa*(1 - a)))


def t_of_z_table(h0, om, w0, wa, zmax=30.0, n=6000):
    """Cosmic time t(z) in Gyr on a grid (matter-dominated tail beyond zmax)."""
    x = np.linspace(0, np.log(1 + zmax), n); z = np.expm1(x)
    f = 1.0/e_cpl(z, om, w0, wa)                      # dt = dx / H
    cum = np.concatenate([[0.0], np.cumsum(0.5*(f[1:] + f[:-1])*np.diff(x))])
    tail = (2.0/3.0)/np.sqrt(om)*(1 + zmax)**-1.5
    return z, (cum[-1] - cum + tail)*GYR/h0


def sfh_b13(z):
    return 0.180/(10**(-0.997*(z - 1.243)) + 10**(0.241*(z - 1.243)))


def sfh_md14(z):
    return 0.015*(1 + z)**2.7/(1 + ((1 + z)/2.9)**5.6)


def dtd_childress(t, tp=0.3, alpha=20.0, s=-1.0):
    x = t/tp
    return x**alpha/(x**(alpha - s) + 1)


def dtd_powerlaw(t, tmin=0.04, s=-1.13):
    return np.where(t >= tmin, t**s, 0.0)


KINDS = {"S": (sfh_b13, dtd_childress), "W": (sfh_md14, dtd_powerlaw)}


def median_age(zs, kind, bg=BG):
    sfh, dtd = KINDS[kind]
    zt, tt = t_of_z_table(*bg)
    out = []
    for z in np.atleast_1d(zs):
        t = np.interp(z, zt, tt)
        tau = np.logspace(-3, np.log10(t - tt[-1]), 4000)
        zform = np.interp(t - tau, tt[::-1], zt[::-1])
        w = sfh(zform)*dtd(tau)
        cw = np.concatenate([[0.0], np.cumsum(0.5*(w[1:] + w[:-1])*np.diff(tau))])
        out.append(np.interp(0.5*cw[-1], cw, tau))
    return np.array(out)


_cache = {}


def table(kind, bg=BG):
    """(z grid, age fall since z = 0 in Gyr, T in mag) on z = 0 ... 1.6 in steps of 0.005."""
    key = (kind, bg)
    if key not in _cache:
        zg = np.linspace(0, 1.6, 321)
        age = median_age(zg, kind, bg)
        _cache[key] = (zg, age[0] - age, SLOPE*(age[0] - age), float(age[0]))
    return _cache[key]


def T(z, kind="S"):
    zg, _, tm, _ = table(kind)
    return np.interp(z, zg, tm)


def dage(z, kind="S", bg=BG):
    zg, da, _, _ = table(kind, bg)
    return np.interp(z, zg, da)


if __name__ == "__main__":
    for k in ("S", "W"):
        zs = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.2])
        print(f"template {k}: median age at z = 0: {table(k)[3]:.2f} Gyr")
        print("   z      " + " ".join(f"{z:6.2f}" for z in zs))
        print("   dage   " + " ".join(f"{v:6.2f}" for v in dage(zs, k)))
        print("   T mag  " + " ".join(f"{v:6.3f}" for v in T(zs, k)))
    print(f"flat Om 0.3, H0 70 background, template S: dage(1.0) = {dage(1.0, 'S', (70.0, 0.3, -1.0, 0.0)):.2f} Gyr")
