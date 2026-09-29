#!/usr/bin/env python3
"""J4 -- can the FL1 order parameter supply the species count and the cutoff of an emergent photon?

Pre-registration: J_PREREGISTRATION.md (H4: J4a, J4b, J4c, J4d).  SI inputs below; natural units hbar = c = 1 for mass formulas; Heaviside-Lorentz e^2 = 4 pi alpha.
FL1 facts used (real_research/dark_fluid_2026/README.md, read): one complex field psi, Schroedinger-Poisson, kernel-invisible (feels/sources only the Newtonian potential u),
m declared >= 2e-19 eV, classical (occupation >= 1) up to m ~ 3 eV, amount free.  N_charged = 0 by construction.

J4a  charge would Higgs the photon:  m_gamma^2 = f^2 e^2 rho_d/m^2  (f = charge in units of e).  Compare with the 1e-18 eV photon-mass bound (recalled, order of magnitude).
J4b  FL1 energy scales versus m_e (the Thomson-limit IR scale of the QED log); decay constant f_theta^2 = rho/m^2 (report only).
J4c  Hubble-IR table, 24 scored trials: 1/alpha = (N_eff/3 pi) ln(E_UV^2/E_IR^2); E_UV in {M_Pl, M_red}, E_IR in {hbar H0, hbar H0 sqrt(Omega_L), rho_L^(1/4)}, N_eff in {1, 8/3, 8, 16}.
     HIT iff |pred/137.035999177 - 1| < 1e-3.  Post-observation family (see pre-registration); a hit is NOT a derivation whatever it returns.
J4d  m-dependence of FL1 dimensionless numbers (sympy): occupation N_cell ~ m^-4, f_theta ~ m^-1.
MUTATE control: argv `MUTATE` (exit code 1): the dark density is set to zero, so the charged-condensate exclusion check must fail.
"""
import sys, math, itertools
import sympy as sp

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = 0
def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails += 1

hbar = 1.054571817e-34; c = 299792458.0; G = 6.67430e-11; eV = 1.602176634e-19
Mpc = 3.0856775814913673e22
H0 = 67.4e3 / Mpc; OL = 0.6847; Oc = 0.120 / 0.674**2
alpha = 1 / 137.035999177; TARGET = 137.035999177
rho_c0 = 3 * H0**2 / (8 * math.pi * G)            # kg/m^3
hbarc_eVm = hbar * c / eV                         # eV m
def rho_to_eV4(rho_kg_m3):                        # energy density -> eV^4
    return rho_kg_m3 * c**2 / eV * hbarc_eVm**3
me = 0.51099895e6                                 # eV
Mpl = math.sqrt(hbar * c / G) * c**2 / eV         # eV
Mred = Mpl / math.sqrt(8 * math.pi)
EH0 = hbar * H0 / eV; EHL = EH0 * math.sqrt(OL)
rhoL = rho_to_eV4(OL * rho_c0); ErhoL = rhoL**0.25
print("inputs: M_Pl = %.4e eV, M_red = %.4e eV, hbar H0 = %.4e eV, hbar H_L = %.4e eV, rho_L^(1/4) = %.4e eV, Omega_c = %.4f" % (Mpl, Mred, EH0, EHL, ErhoL, Oc))

# ---- J4a
m = 2e-19
rho_d = rho_to_eV4(Oc * rho_c0) * (0.0 if MUT else 1.0)
e2 = 4 * math.pi * alpha
mgam = math.sqrt(e2 * rho_d) / m
bound = 1e-18
print("\nJ4a: rho_d = %.3e eV^4 ; f=1 photon mass m_gamma = e sqrt(rho)/m = %.3e eV ; bound %.0e eV ; excess factor %.2e" % (rho_d, mgam, bound, mgam / bound))
check("J4a: a charged FL1 (f=1) would give m_gamma above the photon-mass bound (it must be neutral)", mgam > bound)
if rho_d > 0:
    fmax = bound / mgam
    print("     maximum allowed charge fraction f_max = %.2e (millicharge scale), from m_gamma = f e sqrt(rho)/m" % fmax)
    for mm in (2e-19, 1e-15, 1e-10, 1e-5, 1.0):
        mg = math.sqrt(e2 * rho_d) / mm
        print("     m = %.0e eV: m_gamma(f=1) = %.3e eV, f_max = %.2e" % (mm, mg, bound / mg))
print("     N_charged(FL1) = 0 (read); a charged condensate is a superconductor: Meissner mass, no massless photon. The order parameter cannot be the source of the photon it would Higgs.")

# ---- J4b
m_lo, m_hi = 2e-19, 3.0
print("\nJ4b: FL1 energy scales: m in [%.0e, %.0f] eV; m_e = %.4e eV; largest FL1 scale / m_e = %.2e ; ln = %.2f" % (m_lo, m_hi, me, m_hi / me, math.log(m_hi / me)))
check("J4b: no FL1 scale reaches m_e (cannot be the UV cutoff of the QED log at the Thomson limit)", m_hi < me)
if not MUT:
    for mm in (2e-19, 1e-10, 1.0):
        f_theta = math.sqrt(rho_d) / mm
        print("     m=%.0e eV: f_theta = sqrt(rho)/m = %.3e eV (%.2e m_e); a Lambda=f_theta 'cutoff' would need N_eff = %.2f (inf = below m_e, no log; report only; depends on free m)" % (
            mm, f_theta, f_theta / me, TARGET * 3 * math.pi / (2 * math.log(f_theta / me)) if f_theta > me else float('inf')))
print("     superfluid phase in 3+1 is dual to a 2-form (Kalb-Ramond) field with coupling 1/f_theta^2 of mass dimension -2: dimensionful, not an alpha.")

# ---- J4c
UV = {"M_Pl": Mpl, "M_red": Mred}
IR = {"hbar*H0": EH0, "hbar*H_L": EHL, "rho_L^1/4": ErhoL}
NEFF = [("1", 1.0), ("8/3", 8 / 3), ("8", 8.0), ("16", 16.0)]
print("\nJ4c: Hubble-IR table (post-observation family), 24 scored trials")
hits = 0; ntr = 0
for (un, u), (inn, i) in itertools.product(UV.items(), IR.items()):
    L = 2 * math.log(u / i)
    req = TARGET * 3 * math.pi / L
    line = "  UV=%-5s IR=%-9s ln(UV^2/IR^2)=%7.3f  N_eff required = %7.4f ;" % (un, inn, L, req)
    for nn, N in NEFF:
        ntr += 1
        pred = N * L / (3 * math.pi)
        dev = pred / TARGET - 1
        hit = abs(dev) < 1e-3
        hits += hit
        line += "  N=%s: %.2f (%+.1e)%s" % (nn, pred, dev, " HIT" if hit else "")
    print(line)
chance = ntr * 2e-3 / math.log(1e3)
print("trials = %d, hits = %d, expected chance hits = %d x 2e-3/ln(1e3) = %.4f" % (ntr, hits, ntr, chance))
check("J4c: trial count is the declared 24", ntr == 24)
check("J4c: zero hits (no forced value; even a hit would be post-observation, wrong scale, N_eff chosen)", hits == 0)
print("     required N_eff for the natural pairs is non-integer (see column); e.g. UV=M_Pl, IR=hbar*H0 needs N_eff = %.3f" % (TARGET * 3 * math.pi / (2 * math.log(Mpl / EH0))))

# ---- J4d
mS, nS, rS, vS, hb = sp.symbols('m n rho v hbar', positive=True)
Ncell = (rS / mS) * (2 * sp.pi * hb / (mS * vS))**3
ftheta = sp.sqrt(rS) / mS
exp_N = sp.simplify(sp.diff(sp.log(Ncell), mS) * mS)
exp_f = sp.simplify(sp.diff(sp.log(ftheta), mS) * mS)
print("\nJ4d: d ln N_cell / d ln m = %s ; d ln f_theta / d ln m = %s" % (exp_N, exp_f))
check("J4d: N_cell ~ m^-4 and f_theta ~ m^-1: every FL1 dimensionless number carries the free m (no forced value)", exp_N == -4 and exp_f == -1)
print("SUMMARY: FL1 supplies no charged species, no cutoff above m_e, and only m-dependent dimensionless numbers. fails =", fails)
sys.exit(1 if fails else 0)
