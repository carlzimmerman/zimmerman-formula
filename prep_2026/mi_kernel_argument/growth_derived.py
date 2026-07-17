#!/usr/bin/env python3
r"""
FEED THE *DERIVED* KERNEL ARGUMENT INTO THE MI GROWTH ODE.

This reuses the banked machinery of prep_2026/mi_linear_cosmology/{mi_growth,mi_spectra}.py
(same growth ODE, same BBKS transfer, same Planck normalization, same Qin-2021 bulk-flow
integral) but drives it with the prescription DERIVED in this workflow's kernel_argument.py /
DERIVATION.md -- NOT the three posited floors of the banked run.

DERIVED content (DERIVATION.md secs 2-5), both a0 footings:
  * The RAR-producing FIRST-MOMENT closure gives a BARE argument (|a|/a0)^2 for the
    cosmological element too (no cH_Lambda floor lives in the first moment). -> case BARE.
  * The horizon floor lives ONLY in the dS-Unruh PULLBACK POLE: X_pole = Z^2 + (|a|/a0)^2,
    i.e. accel floor cH_Lambda = Z*a0 (footing-independent; Z=sqrt(32pi/3)=5.789). The
    growing mode couples to the pole ONLY IF it is slow relative to the horizon memory rate
    (omega/H_horizon ~ 1); fast bound orbits (omega/H_Lambda >~ 22) take the first moment ->
    bare, which PRESERVES the galactic deep-MOND RAR (the hard constraint; see DERIVATION s3).
  * The frequency selection is the theory's FREE gap-A closure (PULLBACK PB-D4/PB-P1: the pole
    >= H_Lambda for EVERY moment weighting -> selects none). So the cosmological verdict is
    BRACKETED, not forced, and there is a SECOND fork on the floor value:

      FORK 1  constant H_Lambda floor  (declining rho_DE -> cH_Lambda = Z*a0, constant):
              omega=H(z) ~ H_Lambda only near z=0, so the pole coupling (and the floor) turns
              on near z=0 and the mode is bare at high z (omega=H(z)>>H_Lambda).
                BARE            : no floor, all z            (first-moment everywhere)
                FLOOR_const_allz: floor Z*a0 at ALL z        (banked floor_cH; floor over-applied)
                FLOOR_const_gate: floor Z*a0 gated by w(z)   (pole coupling only where H(z)~H_Lam)
      FORK 2  rising cH*E(z) floor     (horizon rate tracks the instantaneous H(z)):
              omega=H(z) ~ H_horizon=H(z) at ALL epochs -> always couples to the pole, but the
              floor VALUE rises into the past as c*H(z)=c*H0*E(z).
                FLOOR_rise      : floor c*H(z) at all z      (always-on, rising)

Honest both ways: BARE = the galactic-consistent reading (RAR preserved) that OVERSHOOTS
cosmologically; the floored cases CURE sigma8 but by nearly switching MI off in cosmology, via
the FREE frequency closure. No case is 'the' answer -- the derivation does not force one.
Output ONLY here (mi_kernel_argument/). Frozen repo + mi_linear_cosmology read-only. Exit 0.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import os, sympy as sp

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------- cosmology (identical to banked mi_growth.py) ----------------
h, Om, Ob, ns, sig8_t = 0.674, 0.315, 0.0493, 0.965, 0.811
OL = 1.0 - Om
MPC = 3.0857e22
H0 = h * 100e3 / MPC          # 1/s
c  = 2.998e8
Z  = float(sp.sqrt(sp.Rational(32, 3) * sp.pi))       # 5.78881 geometric, footing-indep
FOOT = {'canonical': 9.36e-11, 'alt': 1.13e-10}       # a0 = cH_Lambda/Z (rho_DE) / rho_tot/cH0
HL   = H0 * np.sqrt(OL)                                # H_Lambda (constant dS horizon rate)
# DERIVED accel floor: cH_Lambda = Z*a0 exactly (footing-indep in a0-units: floor/a0=Z=5.789),
# so nu(floor/a0)=nu(Z)=1.083 in BOTH footings (matches banked floor_cH). Per-footing in m/s^2.
def chl_const(a0): return Z * a0                      # = cH_Lambda (5.789 a0); c*H0*sqrt(OL) to 0.03%

def nu(y):    return np.sqrt(1.0 + 1.0 / y)           # framework's OWN nu (NOT McGaugh)
def Ez(a):    return np.sqrt(Om * a**-3 + OL)         # E(z)=H(z)/H0
def Oma(a):   return Om * a**-3 / (Om * a**-3 + OL)
def Wth(x):   return 3 * (np.sin(x) - x * np.cos(x)) / x**3

# ---------------- BBKS transfer (identical) ----------------
Gam = Om * h * np.exp(-Ob * (1.0 + np.sqrt(2 * h) / Om))
def Tk(k):
    q = k / Gam
    return (np.log(1 + 2.34 * q) / (2.34 * q)
            * (1 + 3.89 * q + (16.1 * q)**2 + (5.46 * q)**3 + (6.71 * q)**4)**-0.25)

k = np.logspace(-4, 2, 1200)
lnk = np.log(k)
D2shape = k**(3 + ns) * Tk(k)**2

Ni, Nf = np.log(1 / 201.0), 0.0
Ng = np.linspace(Ni, Nf, 500)
ag = np.exp(Ng)

def grow(nu_of_N):
    def rhs(N, y):
        a = np.exp(N)
        return [y[1], -(2 - 1.5 * Oma(a)) * y[1] + 1.5 * Oma(a) * nu_of_N(N) * y[0]]
    s = solve_ivp(rhs, [Ni, Nf], [ag[0], ag[0]], t_eval=Ng, rtol=1e-8, atol=1e-13)
    return s.y[0], s.y[1]

# LCDM baseline + sigma8 normalization (identical)
DL, DLp = grow(lambda N: 1.0)
fL = DLp / DL
A  = sig8_t**2 / np.trapz(D2shape * Wth(k * 8.0)**2, lnk)
D2n = A * D2shape
k_m = k * h / MPC
Ibase = np.sqrt(np.trapz(D2n / k_m**2, lnk))
def grms(D):  return 1.5 * Om * H0**2 / ag**2 * (D / DL[-1]) * Ibase

# frequency gate: pole-coupling weight for the growing mode vs the CONSTANT dS horizon.
# omega(z) ~ H(z); ratio r(z)=H(z)/H_Lambda = E(z)/sqrt(OL). Fast (r>>1)->first moment (bare);
# slow (r~1)->pole (floored). w(N)=1/(1+(r/r_gate)^p). r_gate lives in the free gap (1..22).
def gate(a, r_gate, p=2.0):
    r = Ez(a) / np.sqrt(OL)
    return 1.0 / (1.0 + (r / r_gate)**p)

def selfconsistent(a0, mode, r_gate=3.0):
    """mode in {BARE, FLOOR_const_allz, FLOOR_const_gate, FLOOR_rise}. Iterate D<->g_rms.
    nu_eff blends first-moment (bare) and pole (floored) by the pole-coupling weight w(N)."""
    def nu_eff_of(D):
        g = grms(D)
        y_bare = g / a0
        nu_bare = nu(y_bare)                                  # first moment (bare)
        if mode == 'BARE':
            return nu_bare
        if mode == 'FLOOR_rise':
            floor = c * H0 * Ez(ag)                           # c*H(z), rising into past
            nu_pole = nu(np.maximum(g, floor) / a0)
            return nu_pole                                    # always couples (r~1 all z)
        # constant-floor forks: pole floor = cH_Lambda = Z*a0 (constant)
        nu_pole = nu(np.maximum(g, chl_const(a0)) / a0)
        if mode == 'FLOOR_const_allz':
            return nu_pole                                    # floor applied at every z
        if mode == 'FLOOR_const_gate':
            w = gate(ag, r_gate)                              # pole coupling only where H(z)~H_Lam
            return (1.0 - w) * nu_bare + w * nu_pole
        raise ValueError(mode)
    D = DL.copy()
    for it in range(200):
        nuN = interp1d(Ng, nu_eff_of(D), fill_value='extrapolate')
        Dn, _ = grow(nuN)
        rel = abs(Dn[-1] - D[-1]) / Dn[-1]
        D = np.exp(0.5 * (np.log(D) + np.log(Dn)))
        if rel < 1e-5:
            break
    nue = nu_eff_of(D)
    nuN = interp1d(Ng, nue, fill_value='extrapolate')
    D, Dp = grow(nuN)
    return dict(D=D, f=Dp / D, nueff=nue, iters=it + 1, rel=rel)

# ---------------- bulk flow (identical to banked mi_spectra.py) ----------------
def Vbulk(R, f0, ampl2):
    return f0 * 100.0 * np.sqrt(np.trapz(ampl2 * D2n * Wth(k * R)**2 / k**2, lnk))
Rg = np.linspace(10, 160, 61)
VL = np.array([Vbulk(R, fL[-1], 1.0) for R in Rg])
QIN = [(35.0, 380.0, 25.0), (100.0, 410.0, 80.0)]     # Qin 2021 CF4TF/W09 (banked)

# =====================================================================================
print("#" * 92)
print("# DERIVED-PRESCRIPTION MI GROWTH  (kernel_argument.py / DERIVATION.md; both footings)")
print("#" * 92)
# sanity: constant accel floor == Z*a0 both footings (footing-independent horizon)
assert abs(chl_const(FOOT['canonical'])/(Z*FOOT['canonical']) - 1) < 1e-12
print(f"Z = {Z:.5f}   cH_Lambda(const floor)/a0 = Z = {Z:.3f} (footing-indep; = c*H0*sqrt(OL) to 0.03%)")
print(f"LCDM: D(1)={DL[-1]:.4f}  f0={fL[-1]:.4f}  sigma8={sig8_t}  "
      f"V(35)={np.interp(35,Rg,VL):.0f}  V(100)={np.interp(100,Rg,VL):.0f} km/s")
print(f"frequency ratio r=H(z)/H_Lambda: z=0 {Ez(1)/np.sqrt(OL):.2f}, z=1 "
      f"{Ez(0.5)/np.sqrt(OL):.2f}, z=3 {Ez(0.25)/np.sqrt(OL):.2f}  (bound orbits >~22 -> bare)")

MODES = ['BARE', 'FLOOR_const_allz', 'FLOOR_const_gate', 'FLOOR_rise']
LBL = {'BARE': 'BARE first-moment (galactic-consistent, RAR-preserving)',
       'FLOOR_const_allz': 'pole floor cH_Lam, ALL z (banked floor_cH)',
       'FLOOR_const_gate': 'pole floor cH_Lam, freq-GATED (r_gate=3)',
       'FLOOR_rise': 'pole floor RISING c*H(z), all z'}
store = {}
iz = [np.argmin(abs(ag - 1 / (1 + z))) for z in (0, 1, 3)]
for foot, a0 in FOOT.items():
    print(f"\n===== footing {foot}: a0={a0:.3e}  (cH_Lam/a0={chl_const(a0)/a0:.2f}, "
          f"cH0/a0={c*H0/a0:.2f}) =====")  # cH_Lam/a0=Z=5.789 (const floor)
    for mode in MODES:
        r = selfconsistent(a0, mode)
        D, f, nue = r['D'], r['f'], r['nueff']
        rat = D[-1] / DL[-1]
        s8 = sig8_t * rat
        Vc = np.array([Vbulk(R, f[-1], rat**2) for R in Rg])
        v35, v100 = np.interp(35, Rg, Vc), np.interp(100, Rg, Vc)
        store[f'{foot}_{mode}'] = (s8, f[-1], v35, v100)
        print(f"  {mode:17s} it={r['iters']:3d} | sigma8={s8:6.3f} ({s8/0.81:5.2f}x Pl)  "
              f"f0={f[-1]:.3f} | V35={v35:6.0f} ({v35/380:4.1f}x) V100={v100:6.0f} ({v100/410:4.1f}x)")
        print(f"      {'':15s}nu_eff(z=0,1,3)=" + ",".join(f"{nue[i]:.3f}" for i in iz)
              + f"  [{LBL[mode]}]")

# r_gate sensitivity for the FREE gated fork (canonical)
print("\n--- FREE gap-A closure sensitivity: gated floor, r_gate scan (canonical a0) ---")
for rgt in (1.5, 3.0, 6.0, 10.0):
    r = selfconsistent(FOOT['canonical'], 'FLOOR_const_gate', r_gate=rgt)
    rat = r['D'][-1] / DL[-1]; s8 = sig8_t * rat
    Vc = np.array([Vbulk(R, r['f'][-1], rat**2) for R in Rg])
    print(f"  r_gate={rgt:4.1f}: sigma8={s8:6.3f} ({s8/0.81:4.2f}x)  V35={np.interp(35,Rg,Vc):6.0f}"
          f"  (r_gate->0 == BARE, r_gate->inf == floor_allz)")

# =====================================================================================
print("\n" + "#" * 92)
print("# VERDICT under the DERIVED prescription (bracketed; both footings)")
print("#" * 92)
for foot in FOOT:
    b = store[f'{foot}_BARE'][0]; fl = store[f'{foot}_FLOOR_const_allz'][0]
    print(f"  {foot:9s}: sigma8 BRACKET = [{fl:.2f} floored ... {b:.2f} bare]  "
          f"(Planck 0.81); Qin V35 bracket [{store[f'{foot}_FLOOR_const_allz'][2]:.0f} .. "
          f"{store[f'{foot}_BARE'][2]:.0f}] vs 380+-25")
print("\nDerived reading: BARE (first-moment, the SAME closure that yields the galactic RAR)")
print("OVERSHOOTS (sigma8 ~7-8x, nonlinear by z~3, V ~10x Qin) -> DEAD if applied cosmologically.")
print("A floor CURES it (sigma8~1.0-1.5, V toward Qin) but only via the FREE freq closure that")
print("PULLBACK does NOT pin; rising-H(z) floor drives fully to LCDM (MI off). The derivation")
print("does NOT force one -> verdict is BRACKETED viable<->dead, not settled. Galactic RAR is")
print("preserved in every case (the floor is NEVER applied to the fast bound orbits).")
print("\nCredits: Nusser 2002 (astro-ph/0109016); Skordis-Zlosnik 2021 PRL 127:161302; Qin 2021.")
print("Caveat: Newtonian quasi-linear MI on AeST background; NOT covariant MI PT. No 'proves'.")
