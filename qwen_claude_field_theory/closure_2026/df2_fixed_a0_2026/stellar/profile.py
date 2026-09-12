"""Spherical Sersic Abel deprojection and isolated isotropic Jeans moments.

Lengths are in circular projected Re, mass in total stellar mass. Accelerations
are in a0 and second moments in a0*Re. No empirical dispersion coefficient.
"""
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.special import gamma, gammainc, gammaincinv


class Sersic:
    """Unit-M, unit-Re spherical deprojection; supported range 0.5 <= n < 1.

    Abel integration uses R=r cosh(t) to remove the lower-end singularity.
    Interpolation is constructed once; tabulation truncates at b*r**(1/n)=80.
    The integrated mass is deliberately not rescaled to hide quadrature error.
    """
    def __init__(self, n=.6, grid_size=2049):
        if not (.5 <= n < 1) or grid_size < 129:
            raise ValueError('Require 0.5 <= n < 1 and grid_size >= 129')
        self.n = float(n)
        self.b = float(gammaincinv(2*n, .5))
        self.amplitude = self.b**(2*n)/(2*np.pi*n*gamma(2*n))
        self.rmin = 1e-8
        self.rmax = (80/self.b)**n
        self.central_density = self.amplitude*self.b**n*gamma(1-n)/np.pi
        self.grid = np.geomspace(self.rmin, self.rmax, grid_size)
        rho = np.array([self._abel(r) for r in self.grid])
        self._logrho = PchipInterpolator(np.log(self.grid), np.log(rho))
        log_grid = np.log(self.grid)
        primitive = CubicSpline(log_grid, 4*np.pi*rho*self.grid**3).antiderivative()
        enclosed = (4*np.pi*self.central_density*self.rmin**3/3 +
                    primitive(log_grid)-primitive(log_grid[0]))
        # At the exponential tail roundoff can make equal masses differ by ulps.
        enclosed = np.maximum.accumulate(enclosed)
        self.integrated_mass = float(enclosed[-1])
        self._logmass = PchipInterpolator(log_grid, np.log(enclosed))

    def _abel(self, r):
        p = 1/self.n
        upper = np.arccosh(self.rmax/r)
        if upper == 0:
            # Include beyond the table endpoint so its density is nonzero.
            upper = np.arccosh((90/self.b)**self.n/r)
        def integrand(t):
            radius = r*np.cosh(t)
            return radius**(p-1)*np.exp(-self.b*radius**p)
        return self.amplitude*self.b*p/np.pi*quad(
            integrand,0,upper,epsabs=1e-40,epsrel=2e-10,limit=150)[0]

    @staticmethod
    def _radius(r):
        r = np.asarray(r, dtype=float)
        if np.any(r < 0) or np.any(np.isnan(r)):
            raise ValueError('Radii must be nonnegative and not NaN')
        return r

    def density(self, r):
        r = self._radius(r)
        safe = np.clip(r, self.rmin, self.rmax)
        result = np.exp(self._logrho(np.log(safe)))
        result = np.where(r < self.rmin, self.central_density, result)
        return np.where(r >= self.rmax, 0., result)

    def mass(self, r):
        r = self._radius(r)
        safe = np.clip(r,self.rmin,self.rmax)
        result = np.exp(self._logmass(np.log(safe)))
        return np.where(r < self.rmin, 4*np.pi*self.central_density*r**3/3, result)

    def surface_density(self, R):
        R = self._radius(R)
        return self.amplitude*np.exp(-self.b*R**(1/self.n))

    def projected_mass(self, R):
        R = self._radius(R)
        return gammainc(2*self.n, self.b*R**(1/self.n))


def spherical_acceleration(g_newtonian):
    """Invert x*(1-exp(-x))=gN/a0 with nonnegative vectorized Newton steps."""
    y = np.asarray(g_newtonian, dtype=float)
    if np.any(y < 0) or np.any(~np.isfinite(y)):
        raise ValueError('Newtonian accelerations must be finite and nonnegative')
    x = y+np.sqrt(y)
    for _ in range(40):
        mu = -np.expm1(-x)
        derivative = mu+x*np.exp(-x)
        step = np.divide(x*mu-y, derivative, out=np.zeros_like(x),where=derivative>0)
        x = np.maximum(x-step,0.)
        if np.all(np.abs(step) <= 3e-15*np.maximum(x,1e-300)):
            break
    return x


def aperture_second_moment(profile, eta, aperture=np.inf, law='aqual'):
    """Luminosity-weighted isotropic LOS sigma²/(a0 Re) in circular aperture.

    eta=G*M/(a0*Re²). Assumes constant M/L, equilibrium, spherical symmetry,
    zero outer pressure, and isolation. aperture=np.inf is the global moment.
    This does not apply the spherical algebraic law to an external field.
    """
    if not np.isfinite(eta) or eta <= 0 or not aperture > 0:
        raise ValueError('eta must be positive finite; aperture must be positive')
    if law not in ('newtonian','aqual'):
        raise ValueError('law must be newtonian or aqual')
    global_aperture = np.isinf(aperture)
    denominator = 1. if global_aperture else float(profile.projected_mass(aperture))
    def integrand(r):
        if r == 0:
            return 0.
        rho = float(profile.density(r))
        if rho == 0:
            return 0.
        gN = eta*float(profile.mass(r))/r**2
        g = gN if law == 'newtonian' else float(spherical_acceleration(gN))
        if global_aperture or r <= aperture:
            weight = r**3
        else:
            weight = -r**3*np.expm1(1.5*np.log1p(-(aperture/r)**2))
        return rho*g*weight
    upper = getattr(profile,'rmax',np.inf)
    bounds = [0.,upper] if global_aperture or aperture >= upper else [0.,aperture,upper]
    integral = sum(quad(integrand,left,right,epsabs=1e-12*min(eta,np.sqrt(eta)),
                        epsrel=2e-8,limit=200)[0] for left,right in zip(bounds[:-1],bounds[1:]))
    return (4*np.pi/3)*integral/denominator
