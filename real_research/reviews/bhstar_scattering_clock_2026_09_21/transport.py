"""Independent continuous-flight Thomson transport; no diffusion approximation.

Units: sphere radius=c=k_B*T0/m_e=1. Density is represented by the
inverse scattering mean free path a(r)=tau0*(1+q*r**2). Null-collision
tracking handles the variable density. All photons, including unscattered
ones, escape. No absorption, bulk velocities, recoil or frequency selection.
"""
import numpy as np


def isotropic(rng, n):
    x = rng.normal(size=(n, 3))
    return x / np.linalg.norm(x, axis=1)[:, None]


def thomson_mu(rng, n):
    mu = np.empty(n)
    todo = np.arange(n)
    while len(todo):
        trial = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + trial**2) / 2
        mu[todo[take]] = trial[take]
        todo = todo[~take]
    return mu


def integrated_rate_temperature(pos, direction, ds, tau0, q, h):
    """Exact integral of tau0*(1+q*r^2)*(1+h*r^2) along a segment."""
    a = np.sum(pos * pos, axis=1)
    b = np.sum(pos * direction, axis=1)
    i2 = a * ds + b * ds**2 + ds**3 / 3
    i4 = (a*a*ds + 2*a*b*ds**2 + (2*a+4*b*b)*ds**3/3
          + b*ds**4 + ds**5/5)
    return tau0 * (ds + (q+h)*i2 + q*h*i4)


def simulate(n, tau0, q, h, source, seed):
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    if source == "volume":
        pos = isotropic(rng, n) * rng.random(n)[:, None]**(1/3)
    origin = pos.copy()
    direction = isotropic(rng, n)
    speed_shift = np.zeros(n)
    elapsed = np.zeros(n)
    exposure = np.zeros(n)
    angular_exposure = np.zeros(n)
    collisions = np.zeros(n, dtype=int)
    alive = np.arange(n)
    rate_max = tau0 * (1 + q)
    steps = 0
    while len(alive):
        steps += 1
        if steps > 10000:
            raise RuntimeError("Transport cap exceeded; do not drop survivors")
        p, d = pos[alive], direction[alive]
        pd = np.sum(p*d, axis=1)
        boundary = -pd + np.sqrt(pd*pd + 1 - np.sum(p*p, axis=1))
        flight = rng.exponential(1/rate_max, len(alive))
        escape = flight >= boundary
        ds = np.minimum(flight, boundary)
        elapsed[alive] += ds
        exposure[alive] += integrated_rate_temperature(p, d, ds, tau0, q, h)
        pos[alive] += d * ds[:, None]
        alive = alive[~escape]
        rr = np.sum(pos[alive]**2, axis=1)
        real = rng.random(len(alive)) < (1 + q*rr)/(1 + q)
        ids = alive[real]
        old = direction[ids].copy()
        mu = thomson_mu(rng, len(ids))
        # Construct a uniformly oriented transverse vector without pole cases.
        transverse = isotropic(rng, len(ids))
        transverse -= np.sum(transverse*old, axis=1)[:, None] * old
        transverse /= np.linalg.norm(transverse, axis=1)[:, None]
        new = old*mu[:, None] + transverse*np.sqrt(1-mu*mu)[:, None]
        temperature = 1 + h*rr[real]
        # Draw full 3D Maxwell velocities, rather than imposing the claimed variance.
        electron = rng.normal(size=(len(ids), 3))*np.sqrt(temperature)[:, None]
        speed_shift[ids] += np.sum(electron*(new-old), axis=1)
        direction[ids] = new
        angular_exposure[ids] += temperature*(1-mu)
        collisions[ids] += 1
    delay = elapsed - np.sum((pos-origin)*direction, axis=1)
    assert np.all(delay >= -1e-12)
    assert np.all(delay <= 2*elapsed + 1e-12)
    if source == "central":
        assert np.all(delay <= elapsed + 1e-12)
    return dict(v=speed_shift, time=elapsed, exposure=exposure,
                angular=angular_exposure, n=collisions, delay=delay, steps=steps)


def paired_z(values):
    return float(values.mean() / (values.std(ddof=1)/np.sqrt(len(values))))


def run_suite():
    cases = [(.1, 0., 0., "central"), (.5, 0., 0., "volume"),
             (1., 0., 0., "central"), (3., 0., 0., "volume"),
             (10., 0., 0., "central"), (1., 3., 2., "central"),
             (2., 2., 3., "volume")]
    rows = []
    for i, (tau0, q, h, source) in enumerate(cases):
        x = simulate(60000, tau0, q, h, source, 9212600+i)
        v, a, integ = x["v"], x["angular"], x["exposure"]
        z = [paired_z(v*v-2*integ), paired_z(a-integ),
             paired_z(v*v-2*a)]
        assert max(abs(t) for t in z) < 6, z
        # Transfer-function triangle inequality, checked on identical raw paths.
        for omega in (.01, .1, 1., 10.):
            transfer = np.mean(np.exp(1j*omega*x["delay"]))
            assert abs(transfer) >= 1-omega*x["delay"].mean()-1e-12
        row = dict(tau0=tau0, density_gradient=q, temperature_gradient=h,
                   source=source, photons=len(v), seed=9212600+i,
                   mean_N=float(x["n"].mean()), mean_residence=float(x["time"].mean()),
                   mean_delay=float(x["delay"].mean()),
                   v2_over_2_exposure=float(np.mean(v*v)/(2*integ.mean())),
                   paired_z_scores=z, steps=x["steps"],
                   unscattered_fraction=float(np.mean(x["n"] == 0)))
        if i == 0:
            sel = x["n"] > 0
            row["INVALID_scattered_only_ratio"] = float(
                np.mean(v[sel]**2)/(2*integ[sel].mean()))
            assert row["INVALID_scattered_only_ratio"] > 2
        rows.append(row)
    return rows
