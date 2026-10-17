"""Shared helpers for ARGON11 (same definitions as ARGON10 Part F; copied so that importing does not run ARGON10's script body)."""
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

def U(c, M):   return M**2*c**2/2 - M*c**3/8 + c**4/4
def Up(c, M):  return M**2*c - 3*M*c**2/8 + c**3
def Upp(c, M): return M**2 - 0.75*M*c + 3*c**2

def coexistence(M, Lq=None):
    L = (2 - 1.0/M) if Lq is None else Lq
    R = lambda x: 1 - 2*M*x + 2*math.sqrt(L*U(-x, M))
    r = minimize_scalar(R, bounds=(1e-6, 3*M), method='bounded', options={'xatol': 1e-12})
    return math.sqrt(U(-r.x, M)/L), r.fun

def background(M, I0, Lq=None):
    L = (2 - 1.0/M) if Lq is None else Lq
    a = 2.0*M
    chi0 = brentq(lambda c: Up(c, M) + a*I0, -5*M, 5*M)
    om2 = 1 + 2*L*I0 + a*chi0
    return L, a, chi0, om2

def growth_curve(M, I0, ks, Lq=None):
    L, a, chi0, om2 = background(M, I0, Lq)
    om = math.sqrt(max(om2, 0))
    Bh = Upp(chi0, M); A = 4*L*I0; h = a*math.sqrt(2*I0)
    out = np.empty(len(ks))
    for n, k in enumerate(ks):
        k2 = k*k
        W = np.zeros((3, 3)); W[0, 0] = A + k2; W[1, 1] = k2; W[2, 2] = Bh + k2; W[0, 2] = W[2, 0] = h
        Gs = np.zeros((3, 3)); Gs[0, 1] = -2*om; Gs[1, 0] = 2*om
        Ac = np.block([[np.zeros((3, 3)), np.eye(3)], [-W, -Gs]])
        out[n] = np.linalg.eigvals(Ac).real.max()
    return out
