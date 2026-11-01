"""Independent energy-shell orbit quadrature for the fast-scalar response.

No computation occurs on import. Background.values(r) supplies psi,dpsi,s,ds,n;
R is its occupied radius. Units: h0=alpha*p^2/2-psi, alpha=exp(-2s), E=0.
Exact radial/circular endpoints are excluded: integrate L with open quadrature.
"""
import math

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq, minimize_scalar


FSTAR = 3.0 / (4.0 * np.pi * 2.0**1.5)
PLANAR_Y2 = {-2: math.sqrt(15.0/(32.0*math.pi)),
             0: -math.sqrt(5.0/(16.0*math.pi)),
             2: math.sqrt(15.0/(32.0*math.pi))}


def _cumulative_simpson_uniform(values, step):
    """Cumulative integrals of pairwise quadratic interpolants on an even grid."""
    y = np.asarray(values)
    if y.ndim != 1 or (y.size - 1) % 2:
        raise ValueError("An odd number of uniform nodes is required")
    a, b, c = y[:-2:2], y[1:-1:2], y[2::2]
    pair = step*(a + 4*b + c)/3
    start = np.r_[0.0, np.cumsum(pair)[:-1]]
    out = np.empty_like(y)
    out[0] = 0
    out[1::2] = start + step*(5*a + 8*b - c)/12
    out[2::2] = np.cumsum(pair)
    return out


class OrbitFamily:
    """Cache the circular energy-shell orbit and construct noncircular ones."""

    def __init__(self, bg):
        self.bg = bg
        self.R = float(bg.R)
        if not self.R > 0:
            raise ValueError("Positive occupied radius required")
        rr = np.linspace(0, self.R, 2049)
        qq = self.q(rr)
        imax = int(np.argmax(qq))
        if imax == 0 or imax == rr.size - 1 or qq[imax] <= 0:
            raise ValueError("No interior circular energy-shell maximum")
        # A single pair of turning points is part of this library's scope.
        peak = minimize_scalar(lambda r: -float(self.q(r)),
                               bounds=(rr[imax-1], rr[imax+1]), method="bounded",
                               options={"xatol": 1e-13*self.R})
        rc = float(peak.x)
        if float(self.qprime(rr[imax-1])) > 0 > float(self.qprime(rr[imax+1])):
            rc = brentq(lambda r: float(self.qprime(r)), rr[imax-1], rr[imax+1],
                        xtol=1e-13*self.R, rtol=1e-13)
        self.r_circular = rc
        self.Lmax = math.sqrt(float(self.q(rc)))
        scale = float(self.q(rc))
        if (np.min(np.diff(qq[:imax+1])) < -1e-8*scale or
                np.max(np.diff(qq[imax:])) > 1e-8*scale):
            raise ValueError("Multiple shell potential extrema require a different orbit decomposition")
        self._gx, self._gw = leggauss(12)

    def q(self, r):
        v = self.bg.values(r)
        rr = np.asarray(r)
        return 2*np.exp(2*np.asarray(v["s"]))*np.asarray(v["psi"])*rr*rr

    def qprime(self, r):
        v = self.bg.values(r)
        rr = np.asarray(r)
        return 2*np.exp(2*np.asarray(v["s"]))* (
            rr*rr*np.asarray(v["dpsi"]) +
            2*rr*np.asarray(v["psi"]) +
            2*rr*rr*np.asarray(v["psi"])*np.asarray(v["ds"]))

    def turning_points(self, L):
        L = float(L)
        if not 0 < L < self.Lmax:
            raise ValueError("Require 0<L<Lmax; endpoints need limiting orbits")
        fun = lambda r: float(self.q(r)) - L*L
        rp = brentq(fun, 0, self.r_circular, xtol=2e-14*self.R, rtol=2e-14)
        ra = brentq(fun, self.r_circular, self.R, xtol=2e-14*self.R, rtol=2e-14)
        if not ra > rp > 0:
            raise RuntimeError("Degenerate or unresolved turning points")
        return rp, ra

    def orbit(self, L, nphase=256, dense_intervals=None):
        if nphase < 16 or nphase % 2:
            raise ValueError("Use an even nphase >=16")
        rp, ra = self.turning_points(L)
        span = ra - rp
        half = span/2
        mid = (ra + rp)/2
        fp = float(self.qprime(rp))/span
        fa = -float(self.qprime(ra))/span
        if fp <= 0 or fa <= 0:
            raise RuntimeError("Turning-point derivative signs are inconsistent")

        def factor(r):
            rr = np.asarray(r, dtype=float)
            flat = np.atleast_1d(rr).ravel()
            out = np.empty_like(flat)
            dl, dr = flat - rp, ra - flat
            left = dl <= 1e-5*span
            right = dr <= 1e-5*span
            inside = ~(left | right)
            out[inside] = (self.q(flat[inside]) - L*L)/(dl[inside]*dr[inside])
            for mask, root, endpoint, side in ((left, rp, fp, 1), (right, ra, fa, -1)):
                for idx in np.flatnonzero(mask):
                    x = flat[idx]
                    distance = abs(x - root)
                    if distance <= 1e-14*max(span, self.R):
                        out[idx] = endpoint
                    else:
                        # Integrate q' over the short root-to-point segment.
                        lo, hi = (root, x) if side == 1 else (x, root)
                        nodes = (lo + hi)/2 + (hi - lo)/2*self._gx
                        difference = side*(hi - lo)/2 * float(np.dot(self._gw, self.qprime(nodes)))
                        out[idx] = difference/(dl[idx]*dr[idx])
            if np.any(out <= 0) or not np.all(np.isfinite(out)):
                raise RuntimeError("Nonpositive factored radial momentum")
            out = out.reshape(np.atleast_1d(rr).shape)
            return float(out[0]) if rr.ndim == 0 else out.reshape(rr.shape)

        def transformed(chi):
            ch = np.asarray(chi)
            r = mid - half*np.cos(ch)
            # Exact assigned endpoints avoid cosine-roundoff outside the bracket.
            r = np.clip(r, rp, ra)
            alpha = np.exp(-2*np.asarray(self.bg.values(r)["s"]))
            dt = r/(alpha*np.sqrt(factor(r)))
            dphi = alpha*L/(r*r)*dt
            return r, dt, dphi

        # These independent adaptive integrals determine the frequencies.
        half_period, time_error = quad(lambda x: float(transformed(x)[1]), 0, np.pi,
                                      epsabs=2e-11, epsrel=2e-11, limit=400)
        half_angle, angle_error = quad(lambda x: float(transformed(x)[2]), 0, np.pi,
                                      epsabs=2e-11, epsrel=2e-11, limit=400)
        Omega_r = np.pi/half_period
        Omega_phi = half_angle/half_period

        count = max(4096, 16*nphase) if dense_intervals is None else int(dense_intervals)
        count += count % 2
        chi = np.linspace(0, np.pi, count + 1)
        _, dt, dph = transformed(chi)
        times = _cumulative_simpson_uniform(dt, np.pi/count)
        phis = _cumulative_simpson_uniform(dph, np.pi/count)
        time_dense_error = abs(times[-1]/half_period - 1)
        angle_dense_error = abs(phis[-1]/half_angle - 1)
        times *= half_period/times[-1]
        phis *= half_angle/phis[-1]
        if np.any(np.diff(times) <= 0):
            raise RuntimeError("Dense phase map is not strictly monotone")
        theta = np.arange(nphase)*2*np.pi/nphase
        outbound = theta <= np.pi
        time_out = np.where(outbound, theta, 2*np.pi - theta)/Omega_r
        chi_uniform = PchipInterpolator(times, chi)(np.clip(time_out, 0, half_period))
        r = np.clip(mid - half*np.cos(chi_uniform), rp, ra)
        radial_squared = np.maximum((r-rp)*(ra-r)*factor(r)/(r*r), 0)
        pr = np.sqrt(radial_squared)*np.where(outbound, 1.0, -1.0)
        pr[0] = 0
        pr[nphase//2] = 0
        pphi = L/r
        angle_out = PchipInterpolator(chi, phis)(chi_uniform)
        physical_phi = np.where(outbound, angle_out, 2*half_angle - angle_out)
        dphi = physical_phi - Omega_phi/Omega_r*theta
        v = self.bg.values(r)
        alpha = np.exp(-2*np.asarray(v["s"]))
        energy = 0.5*alpha*(pr*pr + pphi*pphi) - np.asarray(v["psi"])
        energy_scale = max(float(np.max(np.abs(v["psi"]))), 1e-14)
        modes = np.fft.fftfreq(nphase, 1/nphase)
        dr_dtheta = np.fft.ifft(1j*modes*np.fft.fft(r)).real
        rhs = alpha*pr/Omega_r
        phase_residual = float(np.max(np.abs(dr_dtheta-rhs))/max(np.max(np.abs(rhs)), 1e-14))
        result = {"L": float(L), "r": r, "pr": pr, "pphi": pphi,
                  "theta": theta, "dphi": dphi, "physical_phi": physical_phi,
                  "Omega_r": float(Omega_r), "Omega_phi": float(Omega_phi),
                  "turning_roots": (float(rp), float(ra)),
                  "r_pericenter": float(rp), "r_apocenter": float(ra),
                  "period": float(2*half_period), "angle_per_radial_period": float(2*half_angle),
                  "invariant_residual": float(np.max(np.abs(energy))/energy_scale),
                  "angular_momentum_relative_residual": float(np.max(np.abs(r*pphi/L-1))),
                  "dense_period_relative_error": float(time_dense_error),
                  "dense_angle_relative_error": float(angle_dense_error),
                  "quad_period_error_estimate": float(2*time_error),
                  "quad_angle_error_estimate": float(2*angle_error),
                  "sampled_radial_ode_relative_residual": phase_residual,
                  "sampled_ode_residual_is_resolution_diagnostic": True,
                  "dense_intervals": count}
        return result


def orbit(bg, L, nphase=256, dense_intervals=None):
    """Convenience function; use OrbitFamily for many L values on one background."""
    return OrbitFamily(bg).orbit(L, nphase=nphase, dense_intervals=dense_intervals)


def shell_measure_control(bg, nL=32, nphase=256):
    """Compare action-shell quadrature to independent local momentum integration.

    This includes ALL orbital harmonics, including the dynamically frozen
    zero-frequency ones. It checks measure/Parseval normalization, not causal
    static response or the permission to change orbit populations.
    """
    family = OrbitFamily(bg)
    x, w = leggauss(nL)
    Ls = family.Lmax*(x + 1)/2
    weights = family.Lmax*w/2
    action = np.zeros(3)
    maximum_invariant = maximum_time_error = maximum_angle_error = 0.0
    for L, weight in zip(Ls, weights):
        o = family.orbit(float(L), nphase=nphase)
        shell_weight = FSTAR*(2*np.pi)**3*2*L/o["Omega_r"]*weight
        action += shell_weight*np.array([1.0, np.mean(o["r"]**2), np.mean(o["r"]**4)])
        maximum_invariant = max(maximum_invariant, o["invariant_residual"])
        maximum_time_error = max(maximum_time_error, o["dense_period_relative_error"])
        maximum_angle_error = max(maximum_angle_error, o["dense_angle_relative_error"])

    def radial_integrand(r, power):
        v = bg.values(r)
        S = 1.5*math.exp(3*float(v["s"]))*math.sqrt(max(float(v["psi"]), 0))
        return 4*np.pi*r**(2+power)*S

    spatial = np.array([quad(lambda r: radial_integrand(r, power), 0, bg.R,
                             epsabs=2e-10, epsrel=2e-10, limit=400)[0]
                        for power in (0, 2, 4)])
    return {"nL": nL, "nphase": nphase, "action_moments": action.tolist(),
            "spatial_moments": spatial.tolist(),
            "relative_errors": np.abs(action/spatial-1).tolist(),
            "moment_radial_powers": [0, 2, 4],
            "maximum_orbit_energy_residual": maximum_invariant,
            "maximum_dense_period_relative_error": maximum_time_error,
            "maximum_dense_angle_relative_error": maximum_angle_error,
            "orientation_addition_theorem_error": abs(sum(v*v for v in PLANAR_Y2.values())/5 - 1/(4*np.pi))}


class HarmonicBackground:
    """Analytic external harmonic well; no self-gravitating FR01 assertion."""
    def __init__(self, omega=1.0, energy=1.0):
        self.omega = float(omega)
        self.energy = float(energy)
        if self.omega <= 0 or self.energy <= 0:
            raise ValueError("Positive oscillator frequency and cutoff required")
        self.R = math.sqrt(2*self.energy)/self.omega
        self.eps = 0.01
        self.mass = self.energy**1.5*self.R**3*np.pi/32
        self.core_radius = self.R*math.sqrt(1-4**(-2/3))

    def values(self, r):
        r = np.asarray(r)
        psi = self.energy - 0.5*self.omega**2*r*r
        return {"psi": psi, "dpsi": -self.omega**2*r,
                "s": np.zeros_like(r), "ds": np.zeros_like(r),
                "n": np.maximum(psi, 0)**1.5}


def harmonic_control(nphase=256, nL=24):
    """Exact frequencies, turning roots, orbital r^2, and shell measure controls."""
    bg = HarmonicBackground(omega=0.7, energy=1.3)
    family = OrbitFamily(bg)
    rows = []
    for fraction in (0.01, 0.1, 0.5, 0.9, 0.99):
        L = fraction*bg.energy/bg.omega
        o = family.orbit(L, nphase=nphase)
        discriminant = math.sqrt(bg.energy**2-bg.omega**2*L**2)
        rp = math.sqrt((bg.energy-discriminant)/bg.omega**2)
        ra = math.sqrt((bg.energy+discriminant)/bg.omega**2)
        exact_r2 = (bg.energy-discriminant*np.cos(o["theta"]))/bg.omega**2
        rows.append({"L_fraction": fraction,
                     "Omega_r_relative_error": abs(o["Omega_r"]/(2*bg.omega)-1),
                     "Omega_phi_relative_error": abs(o["Omega_phi"]/bg.omega-1),
                     "pericenter_relative_error": abs(o["r_pericenter"]/rp-1),
                     "apocenter_relative_error": abs(o["r_apocenter"]/ra-1),
                     "r_squared_scaled_error": float(np.max(np.abs(o["r"]**2-exact_r2))/bg.R**2),
                     "invariant_residual": o["invariant_residual"],
                     "dense_period_relative_error": o["dense_period_relative_error"],
                     "dense_angle_relative_error": o["dense_angle_relative_error"]})
    return {"scope": "Analytic oscillator controls only", "orbits": rows,
            "circular_Lmax_relative_error": abs(family.Lmax/(bg.energy/bg.omega)-1),
            "shell_measure": shell_measure_control(bg, nL=nL, nphase=nphase)}
