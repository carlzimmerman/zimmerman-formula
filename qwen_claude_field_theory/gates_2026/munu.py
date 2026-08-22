"""Shared, numerically stable mu_n / nu_n family (Carl's Gate-1 microscope).

    mu_n(x) = x/(1+x^n)^(1/n)
    nu_n(y) = [ (1+sqrt(1+4 y^-n))/2 ]^(1/n)     (exact conjugate: nu(x mu(x)) * x mu(x) = x)

Asymptotics are n-INDEPENDENT by construction:
    mu->x, nu->y^(-1/2)  (deep MOND)        mu->1, nu->1  (Newtonian)
so n moves ONLY the transition shape.  Everything is evaluated in log space, so
n up to several hundred and y over 20 decades are safe.
"""
import numpy as np
LN4 = np.log(4.0)
TINY = 1e-300

def ln_nu_n(y, n):
    lny = np.log(np.maximum(np.asarray(y, float), TINY)); n = float(n)
    a = np.logaddexp(0.0, -n*lny + LN4)      # ln(1+4y^-n)
    b = np.logaddexp(0.0, 0.5*a)             # ln(1+sqrt(1+4y^-n))
    return (b - np.log(2.0))/n

def ln_mu_n(x, n):
    lnx = np.log(np.maximum(np.asarray(x, float), TINY)); n = float(n)
    return lnx - np.logaddexp(0.0, n*lnx)/n  # ln x - (1/n) ln(1+x^n)

def nu_n(y, n):  return np.exp(ln_nu_n(y, n))
def mu_n(x, n):  return np.exp(ln_mu_n(x, n))
def nu_n_fn(n):  return lambda y: nu_n(y, n)
