"""AGB2 host-age model (criteria: FROZEN_CRITERIA.md, section "The host-age model").

Progenitor age of a Type Ia supernova as a function of host stellar mass and redshift, from the galaxy model of
Childress, Wolf & Zahid (2014, arXiv:1409.2951; "C14"): a galaxy grows from a 10^6 Msun seed along the star-forming
main sequence, with a mass-quenching penalty and stellar mass loss; the progenitor-age distribution of its supernovae
is P(tau) proportional to SFR(t_obs - tau) x DTD(tau). No supernova magnitude is read here.
"""
import numpy as np
from scipy.special import erf

GYR = 977.7922216807891                 # 1 / (1 km/s/Mpc) in Gyr
H0, OM = 70.0, 0.30                     # C14's cosmology (flat)
SLOPE = 0.030                           # mag / Gyr (Son et al. 2025)
SEED = 1.0e6                            # Msun
SIG_Q = 1.5


def t_of_z(z):
    return (2.0/(3.0*np.sqrt(1 - OM)))*np.arcsinh(np.sqrt((1 - OM)/OM)*(1.0 + np.asarray(z, float))**-1.5)*GYR/H0


def z_of_t(t):
    x = np.sinh(1.5*np.sqrt(1 - OM)*np.asarray(t, float)*H0/GYR)
    return (np.sqrt((1 - OM)/OM)/x)**(2.0/3.0) - 1.0


def log_mq(z, kind="nominal"):
    z = np.asarray(z, float)
    if kind == "eq11":
        return 10.077 + 0.636*z
    return np.where(z <= 1.5, 10.43 + 0.9*np.log10(1 + z), 8.56 + 5.6*np.log10(1 + z))


def p_q(m, z, kind="nominal"):
    return 0.5*(1.0 - erf((np.log10(m) - log_mq(z, kind))/SIG_Q))


def f_ml(t_gyr):
    return 0.046*np.log(t_gyr*1.0e3/0.276 + 1.0)


def dtd_childress(t, tp=0.3, alpha=20.0, s=-1.0):
    x = t/tp
    return x**alpha/(x**(alpha - s) + 1)


def dtd_powerlaw(t, tmin=0.04, s=-1.13):
    return np.where(t >= tmin, t**s, 0.0)


DTDS = {"S": dtd_childress, "W": dtd_powerlaw}


def tracks(dt=0.004, dform=0.024, quench="nominal"):
    """Mass formed per step m[track, step] and stellar mass M[track, step] on a uniform cosmic-time grid."""
    t0 = float(t_of_z(0.0)); K = int(np.floor(t0/dt))
    tk = (np.arange(K + 1) + 0.0)*dt + (t0 - K*dt)            # grid ends exactly at t0
    zk = np.minimum(z_of_t(np.maximum(tk, 1e-3)), 30.0)       # no track is alive before lookback 13 Gyr (z about 10)
    every = max(1, int(round(dform/dt)))
    kf = np.arange(int(np.ceil((t0 - 13.0 - tk[0])/dt)), K - 5, every)   # formation: lookback 13 Gyr ... about now
    kf = kf[kf >= 1]
    n = len(kf); m = np.zeros((n, K)); M = np.zeros((n, K + 1))
    g = 1.0 - f_ml((np.arange(1, K + 2) - 0.5)*dt)             # surviving fraction after (n - 1/2) steps
    c = 2.00*np.exp(1.33*zk)/(1.0e10)**0.7                     # Msun^0.3 / yr
    dty = dt*1.0e9
    for k in range(K):
        alive = kf <= k
        if not alive.any():
            continue
        Mk = m[:, :k] @ g[k - 1::-1][:k] if k > 0 else np.zeros(n)   # mass formed in step j, surviving after k - j - 1/2 steps
        Mk = np.where(alive, Mk + SEED, 0.0)
        M[:, k] = Mk
        grow = (Mk[alive]**0.3 + 0.3*c[k]*p_q(Mk[alive], zk[k], quench)*dty)**(1/0.3) - Mk[alive]
        m[alive, k] = grow
    M[:, K] = m @ g[K - 1::-1][:K] + SEED
    return dict(dt=dt, tk=tk, zk=zk, kf=kf, m=m, M=M, K=K)


def ages_at(tr, z_obs, dtd="S"):
    """(log10 mass, mean age, median age, supernova rate) of every live track at redshift z_obs, sorted by mass."""
    t_obs = float(t_of_z(z_obs)); k = int(round((t_obs - tr["tk"][0])/tr["dt"])); k = min(max(k, 2), tr["K"])
    live = tr["kf"] <= k - 2
    m = tr["m"][live, :k]; tau = (k - np.arange(k) - 0.5)*tr["dt"]
    w = m*DTDS[dtd](tau)[None, :]
    tot = w.sum(1); ok = tot > 0
    mean = (w[ok]*tau[None, :]).sum(1)/tot[ok]
    cw = np.cumsum(w[ok][:, ::-1], axis=1); ts = tau[::-1]                    # ascending age
    med = np.array([np.interp(0.5*cw[i, -1], cw[i], ts) for i in range(cw.shape[0])])
    lm = np.log10(tr["M"][live, k][ok]); o = np.argsort(lm)
    return lm[o], mean[o], med[o], tot[ok][o]


_cache = {}


def table(dtd="S", quench="nominal", dt=0.004):
    key = (dtd, quench, dt)
    if key not in _cache:
        tr = tracks(dt=dt, quench=quench)
        zg = np.linspace(0.0, 1.6, 81); lmg = np.linspace(7.5, 12.4, 99)
        mean = np.empty((len(zg), len(lmg))); med = np.empty_like(mean)
        for i, z in enumerate(zg):
            lm, a, b, _ = ages_at(tr, z, dtd)
            mean[i] = np.interp(lmg, lm, a); med[i] = np.interp(lmg, lm, b)
        _cache[key] = (zg, lmg, mean, med, tr)
    return _cache[key]


def age(logm, z, stat="mean", dtd="S", quench="nominal", dt=0.004):
    """Model progenitor age in Gyr at host log mass and redshift (bilinear on the table; mass clipped to 7.5 ... 12.4)."""
    zg, lmg, mean, med, _ = table(dtd, quench, dt)
    tab = mean if stat == "mean" else med
    logm = np.clip(np.asarray(logm, float), lmg[0], lmg[-1]); z = np.clip(np.asarray(z, float), zg[0], zg[-1])
    iz = np.clip(np.searchsorted(zg, z) - 1, 0, len(zg) - 2); im = np.clip(np.searchsorted(lmg, logm) - 1, 0, len(lmg) - 2)
    fz = (z - zg[iz])/(zg[iz + 1] - zg[iz]); fm = (logm - lmg[im])/(lmg[im + 1] - lmg[im])
    return ((1 - fz)*(1 - fm)*tab[iz, im] + fz*(1 - fm)*tab[iz + 1, im] + (1 - fz)*fm*tab[iz, im + 1] + fz*fm*tab[iz + 1, im + 1])


def schechter_population(z=0.0, dtd="S", quench="nominal", dt=0.004):
    """Supernova-weighted population at z = 0 with C14's double Schechter function: median and mean progenitor age."""
    tr = table(dtd, quench, dt)[4]
    t_obs = float(t_of_z(z)); k = min(int(round((t_obs - tr["tk"][0])/tr["dt"])), tr["K"])
    live = tr["kf"] <= k - 2
    lm = np.log10(tr["M"][live, k]); m = tr["m"][live, :k]; tau = (k - np.arange(k) - 0.5)*tr["dt"]
    o = np.argsort(lm); lm = lm[o]; m = m[o]
    sel = (lm >= 7.5) & (lm <= 12.5); lm = lm[sel]; m = m[sel]
    phi = (np.log(10)*(1.39e-3*10**((lm - 11.12)*(1 - 1.42))*np.exp(-10**(lm - 11.12))
                       + 6.57e-3*10**((lm - 10.66)*(1 - 0.45))*np.exp(-10**(lm - 10.66))))
    wgt = phi*np.gradient(lm)                                   # galaxies per track
    w = (wgt[:, None]*m).sum(0)*DTDS[dtd](tau)
    cw = np.cumsum(w[::-1]); ts = tau[::-1]
    return float(np.interp(0.5*cw[-1], cw, ts)), float((w*tau).sum()/w.sum())


if __name__ == "__main__":
    import time
    t = time.time(); zg, lmg, mean, med, tr = table()
    print(f"tracks {len(tr['kf'])}, steps {tr['K']}, dt {tr['dt']*1e3:.0f} Myr, built in {time.time() - t:.1f} s; age of the universe {t_of_z(0):.3f} Gyr")
    print(f"quenching mass: log M_Q(0.35) = {float(log_mq(0.35)):.3f} (C14 anchor 10.55); continuity at z 1.5: {float(log_mq(1.5)):.3f} vs {8.56 + 5.6*np.log10(2.5):.3f}")
    lms = [8.0, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]
    for stat in ("mean", "median"):
        print(f"{stat} progenitor age (Gyr), rows z, columns log M = " + " ".join(f"{x:5.1f}" for x in lms))
        for z in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.2):
            print(f"   z {z:4.2f}  " + " ".join(f"{float(age(x, z, stat)):5.2f}" for x in lms))
    for z in (0.0, 0.5):
        lm, a, b, r = ages_at(tr, z)
        print(f"z {z}: track masses {lm.min():.2f} ... {lm.max():.2f}; monotonic in formation time: {bool(np.all(np.diff(np.log10(tr['M'][tr['kf'] <= tr['K'] - 2, -1])) <= 1e-9))}")
    print("z = 0 population (C14 double Schechter, supernova-weighted): median %.2f Gyr, mean %.2f Gyr" % schechter_population())
