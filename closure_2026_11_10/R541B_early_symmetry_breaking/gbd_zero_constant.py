"""R541B family (d): V built only from rho_DE, a0, mu_K, G, c (grammar frozen in FROZEN_CRITERIA.md section 1 (d)).
V = beta rho_DE c^2 y^p shape(tau / T), T = y^-q / sqrt(G rho_DE) (and c/a0 = 2 / sqrt(G rho_DE)), y = mu_K c / sqrt(G rho_DE).
Step 1 (all forms): Q ~ 1 quadrature C = -int a^3 V'(t) dt on the background with the cold share already present.
Step 2: the p = q = 0 forms have no free number: R is printed. Forms with p or q != 0: the mu_K that gives R = 5.41
is solved (that is fitting mu_K: TRADES at best by the frozen rule) and checked against the record's mu_K lines and
GB2a; a subset is re-run with the full ODE (stiff regime included)."""
import os, sys, math, warnings, itertools
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from r541b_core import cosmo, m_of_mu, Pot, run, t_rad, OMEGA_R, OMD, H0_PER_MPC

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G, c = 6.674e-11, 2.99792458e8
H0SI = 67.4e3 / 3.0856775814913673e22
rhoc0 = 3 * H0SI**2 / (8 * math.pi * G)

# background t(a) with the cold share present (for the quadrature)
cpc = cosmo("canonical")
def Hbg(a):
    return math.sqrt(cpc["Or"] / a**4 + (cpc["Ob"] + OMD) / a**3 + cpc["OL"])
lna = np.linspace(math.log(1e-16), 0, 4001)
sol = solve_ivp(lambda N, t: [1 / Hbg(math.exp(N))], (lna[0], 0), [t_rad(1e-16, cpc)], t_eval=lna, rtol=1e-10, atol=1e-40)
T_OF_LNA = sol.y[0]
t0 = T_OF_LNA[-1]
print(f"background age t0 = {t0:.4f} / H0")

def lna_of_t(t):
    return np.interp(np.log(t), np.log(T_OF_LNA), lna)

def C_quad(shape, V0, T):
    """C = int a^3 (-V') dt with tau = t (Q ~ 1, anchored clock), up to today."""
    if shape == "step":
        if T >= t0:
            return 0.0
        return V0 * math.exp(3 * lna_of_t(T))
    # exp: integrand a^3 V0/T exp(-t/T); integrate in ln t
    f = lambda lt: math.exp(3 * lna_of_t(math.exp(lt))) * V0 / T * math.exp(-math.exp(lt) / T) * math.exp(lt)
    lo = math.log(T_OF_LNA[0]); hi = math.log(min(t0, 60 * T))
    if hi <= lo:
        return 0.0
    return quad(f, lo, hi, limit=400, epsabs=0, epsrel=1e-8)[0]

def frac_by_z(shape, T, z):
    """fraction of the charge made by redshift z (exp: by quadrature; step: 1 if switch before z)."""
    tz = np.interp(math.log(1 / (1 + z)), lna, T_OF_LNA)
    if shape == "step":
        return 1.0 if T <= tz else 0.0
    f = lambda lt: math.exp(3 * lna_of_t(math.exp(lt))) / T * math.exp(-math.exp(lt) / T) * math.exp(lt)
    lo = math.log(T_OF_LNA[0])
    tot = quad(f, lo, math.log(min(t0, 60 * T)), limit=400, epsrel=1e-8)[0]
    part = quad(f, lo, math.log(min(tz, 60 * T)), limit=400, epsrel=1e-8)[0] if tz > T_OF_LNA[0] else 0.0
    return part / tot

P_SET = (0, 0.5, 1, 1.5, 2)
BETA = {"1/(8pi)": 1 / (8 * math.pi), "1/(4pi)": 1 / (4 * math.pi), "1/4": 0.25, "1/2": 0.5, "1": 1.0, "2": 2.0,
        "4": 4.0, "4pi": 4 * math.pi, "8pi": 8 * math.pi}
TIMES = {"1/sqrt(G rho_DE)": (0.0, 1.0), "c/a0": (0.0, 2.0), "y^-1/2/sqrt(G rho_DE)": (0.5, 1.0),
         "1/(mu_K c)": (1.0, 1.0)}
SHAPES = ("exp", "step")
MU_JEANS, MU_BBN = 2.512e4, 8.89e6

ver_list = []
for foot in ("canonical", "alt"):
    rhoDE = (2 * A0[foot] / c)**2 / G            # a0 = (1/2) c sqrt(G rho_DE)
    OmDE_eff = rhoDE / rhoc0                       # in rho_c0 units
    sGr = math.sqrt(G * rhoDE) / H0SI              # sqrt(G rho_DE) in H0 units
    target = cpc["R"] if foot == "canonical" else 5.412
    Ob = cpc["Ob"] if foot == "canonical" else 0.02234 / 0.674**2
    print(f"\n==== footing {foot}: rho_DE from a0 = {rhoDE:.4e} kg/m^3 = {OmDE_eff:.4f} rho_c0; "
          f"sqrt(G rho_DE) = {sGr:.4f} H0; target R = {target}")
    # p = q = 0: every number fixed
    print("-- forms with no free number (p = 0, q = 0): R computed --")
    best = None
    for (bl, b), tl, sh in itertools.product(BETA.items(), ("1/sqrt(G rho_DE)", "c/a0"), SHAPES):
        T = TIMES[tl][1] / sGr
        R = C_quad(sh, b * OmDE_eff, T) / Ob
        f3000 = frac_by_z(sh, T, 3000) if R > 0 else 0.0
        print(f"  beta {bl:7s} T {tl:17s} {sh:4s}: T = {T:.3f}/H0, R = {R:.3e}, made by z 3000: {f3000:.2e}")
        if best is None or abs(math.log(max(R, 1e-300) / target)) < abs(math.log(max(best[0], 1e-300) / target)):
            best = (R, bl, tl, sh)
    print(f"  closest to {target}: R = {best[0]:.3e} ({best[1]}, {best[2]}, {best[3]}): factor {target / max(best[0], 1e-300):.2e} short")

    # p or q != 0: solve for mu_K
    print("-- forms that need mu_K: the mu_K giving R = target (Q ~ 1 quadrature), its switch redshift and the gates --")
    print("  p | beta | T | shape | mu_K* [1/Mpc] | z at T | made by z 1e5 | K V0/mu^2 | >= Jeans 2.512e4 | >= BBN 8.89e6 | GB2a")
    nhit = 0; npass = 0; rows = []
    for p, (bl, b), tl, sh in itertools.product(P_SET, BETA.items(), TIMES, SHAPES):
        q, fac = TIMES[tl]
        if p == 0 and q == 0:
            continue
        def lnR(lmu):
            mu = math.exp(lmu); y = m_of_mu(mu) / sGr
            V0 = b * OmDE_eff * y**p; T = fac * y**(-q) / sGr
            C = C_quad(sh, V0, T)
            return math.log(max(C / Ob, 1e-300)) - math.log(target)
        grid = np.linspace(math.log(1e-2), math.log(1e20), 89)
        vals = [lnR(g) for g in grid]
        roots = []
        for i in range(len(grid) - 1):
            if vals[i] * vals[i + 1] < 0 and max(abs(vals[i]), abs(vals[i + 1])) < 600:
                roots.append(brentq(lnR, grid[i], grid[i + 1], xtol=1e-10))
        if not roots:
            rows.append(f"  {p} | {bl} | {tl} | {sh} | no mu_K in 1e-2..1e20 reaches R")
            continue
        for r in roots:
            nhit += 1
            mu = math.exp(r); y = m_of_mu(mu) / sGr
            T = fac * y**(-q) / sGr; V0 = b * OmDE_eff * y**p
            zT = 1 / math.exp(np.interp(math.log(T), np.log(T_OF_LNA), lna)) - 1 if T < t0 else -1
            f5 = frac_by_z(sh, T, 1e5)
            stiff = 4 * math.pi * b * y**(p - 2)
            okJ = mu >= MU_JEANS; okB = mu >= MU_BBN
            g2a = "PASS" if f5 >= 0.99 else ("EXCLUDED" if frac_by_z(sh, T, 1e4) < 0.5 else "undecided")
            if okJ and g2a == "PASS":
                npass += 1
            rows.append(f"  {p} | {bl} | {tl} | {sh} | {mu:.3e} | {zT:.3e} | {f5:.3f} | {stiff:.2e} | {okJ} | {okB} | {g2a}")
            if foot == "canonical" and bl == "1" and okJ:
                ver_list.append((p, b, q, fac, sh, mu, sGr, OmDE_eff, Ob, target))
    print("\n".join(rows))
    print(f"  forms needing mu_K: {len(P_SET) * len(BETA) * len(TIMES) * len(SHAPES) - 2 * len(BETA) * len(SHAPES)}; "
          f"hits (a mu_K that gives R) {nhit}; hits with mu_K >= Jeans line and GB2a PASS: {npass}")

# Step 3: full ODE check on the beta = 1 hits with mu_K >= Jeans (stiff regime included), canonical
print("\n-- full ODE re-run of the beta = 1 hits (canonical), anchored clock, C_i = 0 --")
print("  p | q (T factor) | shape | mu_K* | R (ODE) | R (quadrature target) | max Q - 1")
for (p, b, q, fac, sh, mu, sGr, Om, Ob, target) in ver_list[:24]:
    m = m_of_mu(mu); y = m / sGr
    V0 = b * Om * y**p; T = fac * y**(-q) / sGr
    cp = cosmo("canonical")
    if sh == "exp":
        pot = Pot("exp", V0, T)
    else:
        pot = Pot("tanh", V0, T, D=1e-3 * T)
    a_guess = math.exp(np.interp(math.log(T), np.log(T_OF_LNA), lna))
    segs = [(math.log(a_guess) - 6, math.log(a_guess) + 6, 0.02 if sh == "exp" else 2e-4)]
    try:
        s = run(pot, cp, m, a_ini=min(1e-3 * a_guess, 1e-12), segs=segs)
        Rn = s.Cfin() / cp["Ob"]
        qm = max(s.state(a)["Q"] - 1 for a in np.geomspace(1e-3 * a_guess, 1, 200))
        print(f"  {p} | {q} ({fac}) | {sh} | {mu:.3e} | {Rn:.4f} | {target} | {qm:.2e}")
    except Exception as e:
        print(f"  {p} | {q} ({fac}) | {sh} | {mu:.3e} | ODE failed: {e}")
