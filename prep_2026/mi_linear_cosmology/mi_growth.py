#!/usr/bin/env python3
"""(A) FIRST TRACTABLE MI LINEAR COSMOLOGY -- self-consistent MI growth ODE.

Framework (Zimmerman, modified-INERTIA, dS-Unruh): mu(|a_pec|/a0) * a_pec = g_pec,
with the framework's OWN kernel a_pec = sqrt(g^2 + g*a0)  <=>  1/mu = nu(y)=sqrt(1+1/y),
y = g_pec/a0. (NOT McGaugh's nu; the framework's own interpolation.)

Growth ODE in N=ln a on an AeST-standard (=LCDM-like) background:
    delta'' + (2 + dlnH/dN) delta' = (3/2) Om(a) * nu_eff(a) * delta
nu_eff = nu(g_rms(a)/a0) evaluated SELF-CONSISTENTLY at the linear rms peculiar
gravity of the growing mode: g_rms(a) = [3/2 Om0 H0^2 / a^2] * (D(a)/D_L(1)) *
sqrt(int dlnk Delta^2_0(k)/k_phys^2), iterated D <-> g_rms to convergence.
Amplitude anchor: equal delta at a_i=1/201 (AeST fits the CMB; Skordis-Zlosnik
2021 PRL 127:161302), LCDM branch normalized to sigma8=0.811 (Planck).

NOTE (banked, honest): in the AeST=MG realization linear growth is LCDM exactly
(the delta-q^00=0 theorem). The MI realization has NO analytic linear limit
(nu->inf as y->0): growth is AMPLITUDE-dependent. This computes that
quasi-linear amplitude-dependent growth (classic MOND-structure problem:
Nusser 2002, astro-ph/0109016).

Cases per a0 footing (canonical 9.36e-11 = cH_Lam/Z; alt 1.13e-10):
  SC        : nu at the pure linear rms peculiar gravity (the parent spec)
  floor_a0  : g_arg = max(g_rms, a0) -- proxy for nonlinear/internal element
              accelerations ~ galactic g_bar ~ a0 (linear rms underestimates)
  floor_cH  : g_arg = max(g_rms, cH) -- proxy for the TOTAL element acceleration
              incl. the cosmological background (dS-Unruh floor ambiguity)
First pass: Newtonian/quasi-linear on an AeST background, NOT covariant MI
perturbation theory. Exit 0.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import os

OUT = os.path.dirname(os.path.abspath(__file__))
# --- cosmology (Planck-like; AeST-standard background) ---
h, Om, Ob, ns, sig8_t = 0.674, 0.315, 0.0493, 0.965, 0.811
OL = 1.0 - Om
MPC = 3.0857e22
H0 = h * 100e3 / MPC          # 1/s
c = 2.998e8
FOOT = {'canonical': 9.36e-11, 'alt': 1.13e-10}
CHFLOOR = {'canonical': c * H0 * np.sqrt(OL),   # cH_Lambda = 5.42e-10 (pure-Lambda footing)
           'alt': c * H0}                        # cH0       = 6.55e-10

def nu(y):
    return np.sqrt(1.0 + 1.0 / y)

# --- BBKS transfer + Sugiyama shape (first-pass accuracy; EH-class ok here) ---
Gam = Om * h * np.exp(-Ob * (1.0 + np.sqrt(2 * h) / Om))
def Tk(k):
    q = k / Gam
    return (np.log(1 + 2.34 * q) / (2.34 * q)
            * (1 + 3.89 * q + (16.1 * q)**2 + (5.46 * q)**3 + (6.71 * q)**4)**-0.25)

k = np.logspace(-4, 2, 1200)          # h/Mpc
lnk = np.log(k)
D2shape = k**(3 + ns) * Tk(k)**2      # unnormalized Delta^2(k) at z=0-LCDM

def Wth(x):
    return 3 * (np.sin(x) - x * np.cos(x)) / x**3

def Oma(a):
    return Om * a**-3 / (Om * a**-3 + OL)

Ni, Nf = np.log(1 / 201.0), 0.0
Ng = np.linspace(Ni, Nf, 500)
ag = np.exp(Ng)

def grow(nu_of_N):
    def rhs(N, y):
        a = np.exp(N)
        return [y[1], -(2 - 1.5 * Oma(a)) * y[1] + 1.5 * Oma(a) * nu_of_N(N) * y[0]]
    s = solve_ivp(rhs, [Ni, Nf], [ag[0], ag[0]], t_eval=Ng, rtol=1e-8, atol=1e-13)
    return s.y[0], s.y[1]

# LCDM baseline + sigma8 normalization
DL, DLp = grow(lambda N: 1.0)
fL = DLp / DL
A = sig8_t**2 / np.trapz(D2shape * Wth(k * 8.0)**2, lnk)
D2n = A * D2shape                      # Delta^2(k, z=0, LCDM-normalized)

# rms linear peculiar gravity today's-shape integral (SI)
k_m = k * h / MPC                      # comoving 1/m
Ibase = np.sqrt(np.trapz(D2n / k_m**2, lnk))
def grms(D):
    return 1.5 * Om * H0**2 / ag**2 * (D / DL[-1]) * Ibase

def selfconsistent(a0, gfloor=0.0):
    D = DL.copy()
    hist = []
    for it in range(120):
        g = np.maximum(grms(D), gfloor)
        nuN = interp1d(Ng, nu(g / a0), fill_value='extrapolate')
        Dn, Dp = grow(nuN)
        rel = abs(Dn[-1] - D[-1]) / Dn[-1]
        hist.append(rel)
        D = np.exp(0.5 * (np.log(D) + np.log(Dn)))   # geometric mixing
        if rel < 1e-5:
            break
    g = np.maximum(grms(D), gfloor)
    nueff = nu(g / a0)
    nuN = interp1d(Ng, nueff, fill_value='extrapolate')
    D, Dp = grow(nuN)
    return dict(D=D, f=Dp / D, nueff=nueff, g=g, iters=it + 1, rel=rel)

res = {'a': ag, 'DL': DL, 'fL': fL, 'k': k, 'D2n': D2n, 'sig8L': sig8_t}
print("=== MI LINEAR GROWTH (self-consistent mu_eff) -- first pass ===")
print(f"LCDM: D(1)={DL[-1]:.4f}  f(z=0)={fL[-1]:.4f}  sigma8={sig8_t}")
gL0 = grms(DL)[-1]
print(f"LCDM linear rms peculiar gravity today g_rms = {gL0:.3e} m/s^2")
for foot, a0 in FOOT.items():
    print(f"\n--- footing {foot}: a0={a0:.3e}  (g_rms/a0|_LCDM,z=0 = {gL0/a0:.4f}, "
          f"naive nu = {nu(gL0/a0):.2f}) ---")
    for case, gf in [('SC', 0.0), ('floor_a0', a0), ('floor_cH', CHFLOOR[foot])]:
        r = selfconsistent(a0, gf)
        D, f, nue, g = r['D'], r['f'], r['nueff'], r['g']
        rat = D[-1] / DL[-1]
        s8 = sig8_t * rat
        iz = [np.argmin(abs(ag - 1/(1+z))) for z in (0, 1, 3, 10)]
        print(f"  {case:9s} iters={r['iters']:3d} rel={r['rel']:.1e} | "
              f"D/D_L(1)={rat:7.3f}  sigma8={s8:6.3f}  f0={f[-1]:.3f} "
              f"(f0/fL={f[-1]/fL[-1]:.3f})")
        print(f"            nu_eff(z=0,1,3,10)=" +
              ",".join(f"{nue[i]:.3f}" for i in iz) +
              f" | g_rms(0)/a0={g[-1]/a0:.3f}")
        res[f'{foot}_{case}_D'] = D
        res[f'{foot}_{case}_f'] = f
        res[f'{foot}_{case}_nu'] = nue
        res[f'{foot}_{case}_g'] = g
np.savez(os.path.join(OUT, 'mi_growth.npz'), **res)
print("\nsaved mi_growth.npz")
print("Credits: Nusser 2002 (astro-ph/0109016); Skordis-Zlosnik 2021 PRL 127:161302.")
print("Caveat: Newtonian quasi-linear MI on AeST background; NOT covariant MI PT.")
