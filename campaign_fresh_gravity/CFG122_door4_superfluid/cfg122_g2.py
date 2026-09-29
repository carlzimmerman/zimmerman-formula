#!/usr/bin/env python3
"""CFG122 G2 (CMB and growth) -- frozen criteria G2.1-G2.5.
G2.1 sympy perturbation equations (condensed phase + baryon source; the normal phase is Vlasov CDM by declaration)
G2.2 if the cosmic-mean DM were condensed: c_s^2 = rho^2/(4 Lam^2 m^6) with Lam from the a0 tie; c_s <= c for z <= 1100 and CFG43's two-fluid growth test (within 5% at k = 30/Mpc)
G2.3 the phase at recombination: (a) thermal T > T_c(n(z)) => sigma_0 and a free-streaming length <= 0.01 Mpc; (b) cold, non-thermalised: needs a thermalisation rate the EFT does not fix -> UNDECIDED
G2.4 (i) number injection in the cosmic background if the coupling were active, over z = 1100 -> 0 (<= 1%);  [(ii) halo injection is in cfg122_g1_edge.py]
G2.5 CMB lensing/TT/TE/EE: unchanged iff G2.3 resolves to the normal phase (statement).
Run: ZF_REPO=<repo> python3 cfg122_g2.py"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import *

R = Report("cfg122_g2")
P, check = R.P, R.check
N_PL = 60
mg, ag, Mm, Aa = plane(N_PL)

# ================================================================== G2.1
R.banner("G2.1  perturbation equations (sympy), condensed phase: L2 for psi = delta phi about a homogeneous background, with the baryon source and Newtonian gravity")
t, a, k, m, al, Lam, Mpl, Xb, PXX, PX, Jb, dPhi = sp.symbols("t a k m alpha Lambda M_Pl X_b P_XX P_X delta_rho_b dPhi", real=True)
psi = sp.Function("psi")(t)
# Fourier mode (k), comoving; L2 per mode:  a^3 [ (1/2) P_XX (psi_t - m dPhi)^2 - P_X k^2 psi^2 /(2 m a^2) - (alpha Lam/M_Pl) psi delta_rho_b ]
L2 = a ** 3 * (sp.Rational(1, 2) * PXX * (sp.diff(psi, t) - m * dPhi) ** 2 - PX * k ** 2 * psi ** 2 / (2 * m * a ** 2) - al * Lam / Mpl * psi * Jb)
eq = sp.euler_equations(L2, psi, t)[0].lhs
eq = sp.expand(eq)
P("  EL equation for one Fourier mode (a, P_XX, P_X slowly varying):")
P("    " + str(sp.simplify(eq)))
# wave-equation form: psi_tt + ... + (P_X k^2/(m a^2 P_XX)) psi = ...
coef_gr = sp.simplify(sp.Poly(sp.expand(eq), sp.diff(psi, t, 2)).coeffs()[0]) if False else None
cs2 = sp.simplify(PX / (m * PXX))
Xpos = sp.symbols("X", positive=True)
Pfun = 2 * Lam * (2 * m) ** sp.Rational(3, 2) / 3 * Xpos ** sp.Rational(3, 2)
PX_, PXX_ = sp.diff(Pfun, Xpos), sp.diff(Pfun, Xpos, 2)
cs2_X = sp.simplify(PX_ / (m * PXX_))
P(f"  dispersion relation omega^2 = c_s^2 k^2/a^2 with c_s^2 = P_X/(m P_XX) = {cs2_X} (X>0: P_XX = {sp.simplify(PXX_)} > 0)")
check("G2.1a  linear condensed phase: c_s^2 = 2X/m and the forcing of psi by the baryon density perturbation is (alpha Lam/M_Pl) delta rho_b (sympy)", f"c_s^2 = {cs2_X}", sp.simplify(cs2_X - 2 * Xpos / m) == 0)
P("  Background (homogeneous, from the same L): d(a^3 n)/dt = a^3 J_b,  J_b = (alpha Lam/M_Pl) rho_b(z): the baryons inject condensate number when the condensate is present (G2.4).")
P("  Normal phase (declared, NOT derived): collisionless Vlasov CDM; no phonon exists there, so no coupling and no P(X) pressure.  The perturbation equations of that phase are those of LCDM (the door adds nothing to them).")
R.verdict("G2.1", "PASS", "equations written for both phases; the normal-phase equations are LCDM's by declaration; the condensed-phase equations carry c_s^2 = 2X/m and a baryon source")

# ================================================================== G2.2  growth
R.banner("G2.2  if the cosmic-mean DM were condensed: c_s^2(z) = A (1+z)^6 (c = 1) with A = rho_c0^2 alpha^3 /(4 a0 M_Pl m^6);  c_s <= c for z <= 1100 and growth within 5% at k = 30/Mpc")
OM, OB, OL = OMEGA_M, OMEGA_B, 1 - OMEGA_M
OC = OMEGA_C
FBAR = OB / OM
CH0 = 299792.458 / (67.4)     # c/H0 [Mpc]


def growth_ratio(A, kk, zi=1e4):
    """total-matter growth at z = 0 relative to LCDM; DM with c_s^2 = A a^-6 (pressure term c_s^2 k^2/a^2), baryons pressureless (CFG103's spec, own implementation)."""
    def rhs(la, y, use_p):
        aa = math.exp(la); E2 = OM * aa ** -3 + OL
        dlnH = -1.5 * OM * aa ** -3 / E2
        om = OM * aa ** -3 / E2
        db, dbp, dc, dcp = y
        src = 1.5 * om * (FBAR * db + (1 - FBAR) * dc)
        pres = (A * aa ** -6) * (kk * CH0) ** 2 / (aa * aa * E2) if use_p else 0.0
        return [dbp, src - (2 + dlnH) * dbp, dcp, src - (2 + dlnH) * dcp - pres * dc]
    ai = 1 / (1 + zi)
    out = []
    for use_p in (False, True):
        s = solve_ivp(rhs, (math.log(ai), 0.0), [ai, ai, ai, ai], args=(use_p,), method="LSODA", rtol=1e-8, atol=1e-13)
        db, _, dc, _ = s.y[:, -1]
        out.append(FBAR * db + (1 - FBAR) * dc)
    return out[1] / out[0]


Amax = {}
for kk in (0.5, 2.0, 10.0, 30.0):
    f = lambda lA: growth_ratio(10 ** lA, kk) - 0.95
    lo = None
    for g in np.arange(-32.0, -5.0, 2.0):                    # walk up in A; stop at the first value with ratio < 0.95 (avoids the stiff huge-A integrations)
        if f(g) < 0:
            lo = g
            break
    if lo is None or lo == -32.0:
        Amax[kk] = float("nan")
        continue
    Amax[kk] = 10 ** brentq(f, lo - 2.0, lo, xtol=1e-5)
    P(f"  k = {kk:5.1f}/Mpc: growth within 5% needs A <= {Amax[kk]:.4g}  (c_s^2(z=0) = A; c_s(z=0) <= {math.sqrt(Amax[kk]) * 299792.458:.4g} km/s)")
R.num("A_max_5pct", {str(k): v for k, v in Amax.items()})
# sensitivity (reported): start redshift 1e3 (CFG43's own) instead of 1e4 (CFG103's)
f1k = lambda lA: growth_ratio(10 ** lA, 30.0, zi=1e3) - 0.95
lo1 = next((g for g in np.arange(-32.0, -5.0, 2.0) if f1k(g) < 0), None)
A30_1k = 10 ** brentq(f1k, lo1 - 2.0, lo1, xtol=1e-5) if lo1 is not None else float("nan")
P(f"  sensitivity (reported): start z = 1e3 (CFG43's) instead of 1e4: growth within 5% at k = 30/Mpc needs A <= {A30_1k:.4g}  (a factor {A30_1k / Amax[30.0]:.3g} looser; the plane bound moves by that factor^(1/6) = {(A30_1k / Amax[30.0]) ** (1 / 6):.3g} in m/sqrt(alpha))")
R.num("A_max_30_zi1e3", A30_1k)
A30 = Amax[30.0]
A_sl = 1.0 / (1101.0 ** 6)          # c_s <= c at z = 1100
A_cond = min(A30, A_sl)
P(f"  superluminality bound at z = 1100: A <= {A_sl:.3e};  growth bound (k=30): A <= {A30:.3e}  -> binding {'growth' if A30 < A_sl else 'superluminality'}: A <= {A_cond:.3e}")
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    rho_c0 = OMEGA_C * RHOCRIT0_EV4
    Aplane = rho_c0 ** 2 * Aa ** 3 / (4 * a0n * MPL * Mm ** 6)
    okg = Aplane <= A_cond
    P(f"  [{foot}] cells (of {N_PL * N_PL}) with A(m, alpha) <= {A_cond:.2e}: {int(okg.sum())};  the boundary is m >= alpha^(1/2) * {(rho_c0 ** 2 / (4 * a0n * MPL * A_cond)) ** (1 / 6):.4g} eV")
    R.num(f"G2.2_cells_{foot}", int(okg.sum()))
    R.num(f"G2.2_m_over_sqrt_alpha_min_{foot}", (rho_c0 ** 2 / (4 * a0n * MPL * A_cond)) ** (1 / 6))
R.verdict("G2.2", "PASS", "conditional statement: a region of the plane (m >= q sqrt(alpha), q above) keeps a condensed background cold enough; it is combined with G2.3/G2.4 below")

# ================================================================== G2.4 (i)
R.banner("G2.4 (i)  number injection in the background if the coupling were active: fraction = (Omega_b/Omega_c) m alpha (Lam/M_Pl) t_age(z=1100 -> 0) <= 1%")


def age_eV(z0=1100.0):
    """cosmic time from z0 to 0 (flat LCDM + radiation), in eV^-1."""
    Or = 4.18e-5 / H_LITTLE ** 2
    Ez = lambda z: math.sqrt(OM * (1 + z) ** 3 + Or * (1 + z) ** 4 + OL)
    val, _ = quad(lambda z: 1.0 / ((1 + z) * Ez(z)), 0.0, z0, epsabs=0, epsrel=1e-10)
    return val / H0_EV


tage = age_eV()
P(f"  t(z=1100 -> 0) = {tage / GYR_EV:.3f} Gyr (H0 = 67.4)")
q1 = {}
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    frac = (OB / OC) * Mm * np.sqrt(a0n / (Aa * MPL)) * tage          # alpha Lam / M_Pl = sqrt(a0/(alpha M_Pl))
    ok = frac <= 0.01
    # the boundary in m/sqrt(alpha):
    q_ = 0.01 / ((OB / OC) * math.sqrt(a0n / MPL) * tage)
    q1[foot] = q_
    P(f"  [{foot}] cells with injected fraction <= 1%: {int(ok.sum())}/{N_PL * N_PL};  the condition is m/sqrt(alpha) <= {q_:.4g} eV;  smallest fraction in the plane {frac.min():.3g}, largest {frac.max():.3g}")
    R.num(f"G2.4_i_q_{foot}", q_)
    R.num(f"G2.4_i_cells_{foot}", int(ok.sum()))
    # intersection with G2.2:
    qg = R.numbers[f"G2.2_m_over_sqrt_alpha_min_{foot}"]
    P(f"        G2.2 needs m/sqrt(alpha) >= {qg:.4g}; G2.4(i) needs <= {q_:.4g}: {'compatible' if qg <= q_ else 'INCOMPATIBLE'} (a condensed cosmological background is {'allowed' if qg <= q_ else 'excluded'} in the plane)")
    R.num(f"G2.2_and_G2.4i_compatible_{foot}", bool(qg <= q_))
R.verdict("G2.4-i", "PASS" if all(R.numbers[f"G2.2_and_G2.4i_compatible_{f}"] for f in FOOTINGS) else "FAIL",
          f"a condensed, active-coupling background needs m/sqrt(alpha) in [{[round(R.numbers[f'G2.2_m_over_sqrt_alpha_min_{f}'], 3) for f in FOOTINGS]}, {[round(q1[f], 5) for f in FOOTINGS]}] eV: compatible = {[R.numbers[f'G2.2_and_G2.4i_compatible_{f}'] for f in FOOTINGS]}")

# ================================================================== G2.3
R.banner("G2.3  the phase at recombination: (a) thermal, T > T_c(n(z)); (b) cold and non-thermalised (rate not fixed by the EFT)")


def sigma_c0(mm):
    """today-equivalent velocity dispersion (c = 1) at which T = m sigma^2 equals T_c(n_DM,0): sigma^2 = (2 pi/m^2) (n/zeta(3/2))^(2/3)."""
    n0 = OMEGA_C * RHOCRIT0_EV4 / mm
    return math.sqrt(2 * math.pi / mm ** 2 * (n0 / ZETA32) ** (2.0 / 3.0))


Or = 4.18e-5 / H_LITTLE ** 2


def lam_fs_Mpc(s0, zmax=1e8, zmin=10.0):
    """comoving free-streaming length from zmax to zmin: int v dz / H, v = s0(1+z)/sqrt(1 + (s0 (1+z))^2)  (relativistic cap), s0 = today-equivalent rms velocity (c = 1)."""
    Ez = lambda z: math.sqrt(OM * (1 + z) ** 3 + Or * (1 + z) ** 4 + OL)
    f = lambda lz: (lambda z: (s0 * (1 + z) / math.sqrt(1 + (s0 * (1 + z)) ** 2)) * (1 + z) / Ez(z))(math.exp(lz) - 1.0)
    val, _ = quad(f, math.log(1 + zmin), math.log(1 + zmax), limit=400, epsabs=0, epsrel=1e-8)
    return val * CH0 / 1.0


rows = []
mgrid = 10 ** np.linspace(-3, 6, 91)          # the table extends beyond the frozen plane (m <= 1e3 eV) to 1e6 eV to locate m_a; labelled
lam = np.array([lam_fs_Mpc(sigma_c0(x)) for x in mgrid])
s0 = np.array([sigma_c0(x) * 299792.458 for x in mgrid])
ok_a = lam <= 0.01
m_a = float(mgrid[ok_a].min()) if ok_a.any() else float("nan")
P("  m [eV]     sigma_c0 [km/s]   lambda_fs(z: 1e8 -> 10) [Mpc]")
for i in range(0, len(mgrid), 6):
    P(f"  {mgrid[i]:9.3g}  {s0[i]:14.4g}   {lam[i]:12.4g}")
P(f"  free-streaming option (a) passes (lambda_fs <= 0.01 Mpc) for m >= {m_a:.3g} eV (on the log grid)")
R.num("G2.3a_m_min_eV", m_a)
R.num("G2.3a_table", dict(m=mgrid[::6], sigma0=s0[::6], lam=lam[::6]))
# joint constraint: condensation in the halo requires R_c >= 3 r_M for all four masses (n_DM(halo) >= n_c(sigma_halo))
mb_all = {}
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    per = []
    for Mmsun in MASSES:
        nfw = NFW(Mmsun)
        rMv = float(rM(Mmsun * MSUN_EV, a0n)); sig2 = 0.5 * float(Vf2(Mmsun * MSUN_EV, a0n))
        mmax = 0.0
        for mm in 10 ** np.linspace(-3, 3, 241):
            rc, fl = nfw.r_of_rho(mm * n_crit(mm, sig2))
            if fl != "none" and rc >= 3 * rMv:
                mmax = max(mmax, mm)
        per.append(mmax)
    mb_all[foot] = per
    P(f"  [{foot}] largest m for which the NFW halo still has a condensate out to >= 3 r_M (n_DM(r) >= n_c(sigma_halo)): " + ", ".join(f"{M:.0e}: {v:.3g} eV" for M, v in zip(MASSES, per)))
R.num("G2.3_m_max_halo_condensate", {f: v for f, v in mb_all.items()})
optionA_possible = m_a <= min(min(v) for v in mb_all.values())
P(f"  option (a) [thermal, T > T_c at recombination, free-streaming small enough] needs m >= {m_a:.3g} eV; a condensed halo core at all four masses needs m <= {min(min(v) for v in mb_all.values()):.3g} eV:"
  f" {'COMPATIBLE' if optionA_possible else 'INCOMPATIBLE'}")
R.num("G2.3a_compatible_with_halo_condensate", bool(optionA_possible))
P("  option (b) [cold, non-thermalised background]: whether cold degenerate bosons condense needs the thermalisation (2->2 / 3->3) rate, which the P(X) EFT does not fix; not computed.")
R.verdict("G2.3", "UNDECIDED", f"(a) thermal at recombination: {'compatible' if optionA_possible else 'INCOMPATIBLE'} with a condensed halo core (m >= {m_a:.3g} eV for free streaming vs m <= {min(min(v) for v in mb_all.values()):.3g} eV for condensation); (b) cold non-thermalised: rate not fixed by the EFT -> UNDECIDED")

R.banner("G2.5  CMB lensing and TT/TE/EE (statement, not computed)")
P("  By declaration unchanged if and only if G2.3 resolves to the normal phase (then the DM is LCDM's CDM at recombination and in the linear regime).  Not computed.  Option (a) is not compatible with the condensed halo core (above); option (b) is undecided.")
R.verdict("G2.5", "UNDECIDED", "conditional on G2.3, which is UNDECIDED / option (a) incompatible with a condensed halo")

R.verdict("G2", "UNDECIDED" if not optionA_possible else "UNDECIDED", "G2.1 PASS (statement), G2.2 conditional region, G2.4(i) region, G2.3 UNDECIDED (option a INCOMPATIBLE with halo condensation, option b undecidable): G2 is not an unconditional PASS (frozen rule)")
nf, gf = R.write()
sys.exit(1 if (nf or gf) else 0)
