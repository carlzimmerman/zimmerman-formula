"""Shared definitions for the fix-forward DeepSeek EFE audit.

Every external-field argument is named by its physical or Newtonian meaning.
Simple-mu is used on both sides; this does not identify a unique physical theory.
"""
import math
import numpy as np

G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19
MB_MSUN = 6.681e10
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
Y_EXTERNAL = 0.01273


def mu_simple(x):
    return np.asarray(x) / (1.0 + np.asarray(x))


def physical_external_from_newtonian(y):
    return 0.5 * (y + math.sqrt(y*y + 4.0*y))


def nu_simple(y):
    y = np.asarray(y)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0/y))


def aqual_asymptote(x_external):
    mu = float(mu_simple(x_external))
    L = 1.0/(1.0+x_external)
    return math.atan(math.sqrt(L))/(mu*math.sqrt(L))


def qumond_asymptote(y_external):
    x = physical_external_from_newtonian(y_external)
    L = 1.0/(1.0+x)
    K = -L/(1.0+L)
    return float(nu_simple(y_external))*(1.0+K/3.0)


def qumond_monopole(r_dimensionless, y_external, order=512):
    """Exact QUMOND flux monopole for a point source, quadrature only.

    This is not the pointwise acceleration. A separate Poisson solve is needed
    for that. Units GM=a0=1. The external Newtonian field is uniform.
    """
    c, w = np.polynomial.legendre.leggauss(order)
    r = np.atleast_1d(np.asarray(r_dimensionless, dtype=float))
    b = 1.0/r[:, None]**2
    y = np.sqrt(b*b+y_external*y_external+2*b*y_external*c)
    radial = nu_simple(y)*(b+y_external*c)
    result = r*r*(radial @ w)/2.0
    return result


def aqual_density_factor(cos_theta, L):
    """rho_eff / [M/(4*pi*mu_e*r**3)] outside the point source.

    Negative values refute identification with a nonnegative matter density;
    they do not refute use as a signed effective gravitational source.
    """
    c = np.asarray(cos_theta)
    D = 1.0+L*(1.0-c*c)
    return L*((3.0+L)*c*c-(1.0+L))/D**2.5
