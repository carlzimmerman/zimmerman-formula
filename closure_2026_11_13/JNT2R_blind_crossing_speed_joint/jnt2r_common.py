"""JNT2R (READING.md, 5abea0324b): the crossing speed v*(z) and the membership rule. This lane's own code.
v* = a0 / (10 (1 + X) H) is where the lemma's clustering relation v^3 = 10 G M H with M = (1 + X) M_b meets the law's
v^4 = G M_b a0. v*(z) = v*(0) H0 / H(z), a0 constant, the lemma's H0 = 67.4 km/s/Mpc and OL = 0.6847 (flat).
Primary speed: v_cl = (10 G H(z) (1 + X) M_b)^(1/3); above iff v_cl > s v*(z) (s = 1; twins 0.5, 2), i.e. M_b > M_b*(z).
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import math
G = 6.6743e-11; MSUN = 1.98892e30; MPC = 3.0857e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; X = 5.41
H0 = 67.4e3 / MPC; OL = 0.6847; OM = 1.0 - OL
def E(z): return math.sqrt(OM * (1 + z) ** 3 + OL)
def H(z): return H0 * E(z)
def vstar(ft, z, s=1.0):
    """crossing speed in km/s"""
    return s * A0[ft] / (10 * (1 + X) * H(z)) / 1e3
def mbstar(ft, z, s=1.0):
    """M_b*(z) in Msun from v_f = (G M_b a0)^(1/4) = v*"""
    v = vstar(ft, z, s) * 1e3; return v ** 4 / (G * A0[ft]) / MSUN
def mbstar_from_vcl(ft, z, s=1.0):
    """the same boundary from v_cl = (10 G H (1+X) M_b)^(1/3) = v* (KA4)"""
    v = vstar(ft, z, s) * 1e3; return v ** 3 / (10 * G * H(z) * (1 + X)) / MSUN
def vcl(Mb_sun, z):
    return (10 * G * H(z) * (1 + X) * Mb_sun * MSUN) ** (1 / 3) / 1e3
def above(ft, Mb_sun, z, s=1.0):
    return bool(Mb_sun > mbstar(ft, z, s))
