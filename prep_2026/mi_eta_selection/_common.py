#!/usr/bin/env python3
r"""
Shared footing + Herglotz-measure machinery for the eta-selection lane.
Framework: Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA (judged on its own terms).
  S_matter = -1/2 INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],  s = -1,
  K(z) = (sqrt(1+4z)-1)/(2 sqrt z),   nu(y)=sqrt(1+1/y),  mu(x)=K(x^2),
  a0 = c H_Lambda / Z,  Z = sqrt(32 pi/3),  T_dS = H_Lambda / 2 pi,
  kappa_eff = sqrt(H_Lambda^2 + (a/c)^2)   (Pythagorean dS-Unruh pole, Deser-Levin).
BOTH footings carried: canonical a0 = 9.36e-11 (rho_DE, cH_L/Z),
                       alt       a0 = 1.13e-10 (rho_tot/cH0).
The Herglotz measure of (1-K),  1-K(z) = INT_0^inf dmu(t)/(t+z), dmu>=0, INT dmu/|t| = 1,
IS the dS-Unruh bath spectral density J (established: mi_closure_pin/ostro_nonlocal_verify.py,
opus_48_extended_research/reviews/mi_kernel_bath/). This module only supplies constants + K + rho.
No verdict booleans here.
"""
import mpmath as mp
mp.mp.dps = 40

# ---- footing (both) ---------------------------------------------------------
c      = mp.mpf('2.998e8')
Z      = mp.sqrt(32*mp.pi/3)                 # = 2 sqrt(8pi/3) = 5.7873...
A0_DE  = mp.mpf('9.36e-11')                  # canonical (rho_DE)
A0_TOT = mp.mpf('1.13e-10')                  # alt       (rho_tot/cH0)
HL_DE  = A0_DE  * Z / c                       # dS Hubble rate, canonical
HL_TOT = A0_TOT * Z / c                       # dS Hubble rate, alt
Gyr    = mp.mpf('3.156e16')
FOOTINGS = [("canonical rho_DE", A0_DE, HL_DE), ("alt rho_tot/cH0", A0_TOT, HL_TOT)]

# ---- the framework kernel K and its Herglotz spectral density ---------------
def K(z):
    """K(z)=(sqrt(1+4z)-1)/(2 sqrt z); mu(x)=K(x^2), nu(y)=sqrt(1+1/y)=? via K."""
    z = mp.mpf(z) if not isinstance(z, mp.ctx_mp_python.mpf) else z
    return (mp.sqrt(1+4*z)-1)/(2*mp.sqrt(z))

def Kc(z):
    """K on complex argument (for branch-cut / spectral evaluation)."""
    return (mp.sqrt(1+4*z)-1)/(2*mp.sqrt(z))

def rho_measure(t):
    """Spectral density rho(t)=dmu/dt = +(1/pi) Im K(-t+i0) of the deviation 1-K.
       t = mass^2 / a0^2 >= 0.  (Herglotz-positive; sum rule INT rho/t dt = 1.)"""
    t = mp.mpf(t)
    zz = -t + mp.mpf('1e-30')*1j
    return mp.im(Kc(zz))/mp.pi

def kappa_eff(a, HL):
    """Pythagorean dS-Unruh memory pole scale (angular freq): sqrt(H^2 + (a/c)^2)."""
    return mp.sqrt(HL**2 + (mp.mpf(a)/c)**2)

def banner(s):
    print("\n" + "#"*94 + "\n# " + s + "\n" + "#"*94)

class Checker:
    """Accumulates computed (never hard-coded) boolean checks; exit code = all()."""
    def __init__(self): self.ok = True; self.n = 0; self.p = 0
    def __call__(self, name, cond):
        c = bool(cond); self.n += 1; self.p += int(c); self.ok = self.ok and c
        print(f"   [{'PASS' if c else 'FAIL'}] {name}")
        return c
    def done(self):
        print(f"\n   >>> {self.p}/{self.n} checks passed.")
        return 0 if self.ok else 1

if __name__ == "__main__":
    banner("FOOTING + KERNEL SELF-CHECK")
    print(f"  Z = sqrt(32pi/3) = {mp.nstr(Z,7)}")
    for name, a0, HL in FOOTINGS:
        print(f"  {name:18s}: a0={mp.nstr(a0,4)}  H_L={mp.nstr(HL,4)} 1/s  "
              f"1/H_L={mp.nstr(1/HL/Gyr,4)} Gyr  T_dS=H_L/2pi={mp.nstr(HL/(2*mp.pi),4)}")
    print(f"  K(1)={mp.nstr(K(1),8)} (=1/phi golden? {mp.nstr((mp.sqrt(5)-1)/2,8)})")
    print(f"  rho(0.1)={mp.nstr(rho_measure(mp.mpf('0.1')),5)}  rho(1)={mp.nstr(rho_measure(1),5)}")
    sr = mp.quad(lambda t: rho_measure(t)/t, [0, mp.mpf(1)/4, 1, 10, 1e3, 1e6, mp.inf])
    print(f"  sum rule INT dmu/|t| = {mp.nstr(sr,8)} (target 1)")
