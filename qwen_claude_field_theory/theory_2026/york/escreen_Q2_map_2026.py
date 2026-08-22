"""
Q2(m, eps_s) MAP for the SCALAR external-field-SCREENED repaired York/CMC MOND theory.
--------------------------------------------------------------------------------------
NO new propagating field (scalar e already verified 2+0, second-class).  The screening
enters the AQUAL/QUMOND constitutive law as an eps-dependent modulation of the SAME
interpolation function; the anisotropic DIRECTION still comes from the Phi boundary
condition (the Galactic external field g_e), exactly as in the standard EFE quadrupole.

CONSTITUTIVE LAW (frozen by the task):
    div[ mu_eff(|DPhi|/a0, e/a0) DPhi ] = 4 pi G rho
    mu_eff(x, eps) = 1 - (1 - mu_gal(x)) / (1 + (eps/eps_s)^m)
    mu_gal(x) = x/sqrt(1+x^2)                      (Standard / n=2 function)
    x   = |DPhi|/a0 ,  eps = e^2/a0^2
    a0  = c q / Z  GLOBAL (spatially constant);  a0(z) = a0,0 H(z)/H0.
    e   scalar elliptic auxiliary,  BC  e -> |g_Gal| in Solar System,  e -> 0 isolated galaxy.

Write A(eps) := 1/(1 + (eps/eps_s)^m)  (the screening amplitude, 0<A<=1).  Then
    mu_eff(x,eps) = 1 - A(eps) * (1 - mu_gal(x))        [ = 1-A + A*mu_gal(x) ]
    (1 - mu_eff)  = A(eps) * (1 - mu_gal(x)).
So A(eps) LINEARLY dilutes the whole MOND deviation:
    eps -> 0   (isolated galaxy)  => A -> 1 => mu_eff = mu_gal  EXACTLY  (rotation curves untouched).
    eps large  (Solar System)     => A -> 0 => mu_eff -> 1  AND  d mu_eff/dx -> 0  => Q2 -> 0.

METHOD: reuse the VALIDATED q(eta) quadrature from referee_gateF_2026.py.  That quadrature
is QUMOND (it takes nu, the conjugate of mu, of the NEWTONIAN field).  So we build the exact
conjugate  nu_eff  of  mu_eff  (numerically, by inverting  y = x*mu_eff(x)  ) and feed it in.
At A=1, nu_eff == nu_standard (n=2) and we reproduce the referee's validation numbers; at A=0,
nu_eff == 1 and q == 0 identically.

Cassini 2026 bound (task): Q2 = (1.6 +- 1.8)e-27 s^-2 (DE440, PRD r7n8-kw38); 95% upper ~5.1e-27.

Discipline: numpy for every number; both a0 footings; verify the two limits explicitly; do not
manufacture a pass or a deficit.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "gates_2026"))
from munu import nu_n_fn          # validated stable nu_n family (callable in y); n=2 == standard

def head(t): print("\n" + "=" * 84 + "\n" + t + "\n" + "=" * 84)
def line(t): print("  " + t)

# ------------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------------
G_, MSUN = 6.6743e-11, 1.98892e30
GM = G_ * MSUN
KPC = 3.0856775814913673e19   # m
KMS = 1.0e3

# Milky-Way external field at the Sun (task): g_e = Vc^2/R0, Vc=229 km/s, R0=8.2 kpc
Vc, R0 = 229.0 * KMS, 8.2 * KPC
g_e = Vc**2 / R0
# two a0 footings
A0_STD  = 1.20e-10       # standard-MOND footing
A0_CAN  = 9.3619e-11     # framework canonical horizon-derived a0 = c H_Lambda / Z
A0_ALT  = 1.1279e-10     # framework alt footing

# ------------------------------------------------------------------------------------
# mu_gal and its conjugate nu_standard (n=2) -- reference / A=1 limit
# ------------------------------------------------------------------------------------
def mu_gal(x):
    x = np.asarray(x, float)
    return x / np.sqrt(1.0 + x * x)

nu_standard = nu_n_fn(2.0)   # exact conjugate of mu_gal = x/sqrt(1+x^2)

# ------------------------------------------------------------------------------------
# nu_eff = exact conjugate of mu_eff(x) = 1 - A + A*mu_gal(x), for a CONSTANT screening A.
# In the Solar-System patch e0 = g_e is a uniform background => eps = eps_e is constant, so
# A(eps_e) is a single number and nu_eff depends only on that scalar A.
# Build nu_eff(y) by inverting y = x*mu_eff(x) on a dense log grid (monotone => 1-1).
# ------------------------------------------------------------------------------------
def make_nu_eff(A):
    if A <= 0.0:
        return lambda y: np.ones_like(np.asarray(y, float))   # pure Newtonian
    # dense x-grid; y(x) = x*mu_eff(x) is strictly increasing
    x = np.geomspace(1e-10, 1e10, 400000)
    mu = 1.0 - A + A * (x / np.sqrt(1.0 + x * x))
    y = x * mu
    lny, lnx = np.log(y), np.log(x)
    def nu_eff(yq):
        yq = np.maximum(np.asarray(yq, float), 1e-300)
        xq = np.exp(np.interp(np.log(yq), lny, lnx))
        return xq / yq
    return nu_eff

# ------------------------------------------------------------------------------------
# VALIDATED q(eta) quadrature -- copied verbatim from referee_gateF_2026.py
# ------------------------------------------------------------------------------------
def eta_N_of(nu, eta):
    f = lambda t: t * float(nu(np.array([t]))[0]) - eta
    hi = max(10.0 * eta, 10.0)
    while f(hi) < 0:
        hi *= 2
    return brentq(f, 1e-8, hi, xtol=1e-14, rtol=1e-15)

def c2_raw(nu, etaN, nr=2600, nth=96, rmin=3e-4, rmax=400.0):
    mu_g, w_g = leggauss(nth)
    r = np.geomspace(rmin, rmax, nr)
    R, MUv = np.meshgrid(r, mu_g, indexing="ij")
    ST = np.sqrt(np.clip(1 - MUv**2, 0, None))
    gs = 1.0 / R**2
    gz, gp = etaN - gs * MUv, -gs * ST
    gN = np.sqrt(gz**2 + gp**2)
    Aq = nu(gN) - 1.0
    Ar = Aq * (gz * MUv + gp * ST); At = Aq * (-gz * ST + gp * MUv)
    dAr = np.gradient(R**2 * Ar, r, axis=0) / R**2
    dAt = np.gradient(At * ST, np.arccos(mu_g), axis=1) / (R * np.maximum(ST, 1e-12))
    S2 = 2.5 * np.sum((dAr + dAt) * (0.5 * (3 * MUv**2 - 1)) * w_g[None, :], axis=1)
    ok = np.isfinite(S2)
    return -0.2 * np.trapz((S2 / r)[ok], r[ok])

def q_of(nu, eta):
    return 2.0 * abs(c2_raw(nu, eta_N_of(nu, eta)))

# ------------------------------------------------------------------------------------
# VALIDATION of the machinery (must reproduce referee_gateF numbers at A=1)
# ------------------------------------------------------------------------------------
head("VALIDATION  (nu_eff at A=1 must reproduce the referee's validated q(eta))")
q_std_15 = q_of(nu_standard, 1.5)
line(f"standard nu_2  q(1.5) = {q_std_15:.4f}   vs Milgrom Tab.1 = 0.11   ({q_std_15/0.11-1:+.1%})")
nu_A1 = make_nu_eff(1.0)
q_A1_15 = q_of(nu_A1, 1.5)
line(f"nu_eff(A=1)    q(1.5) = {q_A1_15:.4f}   (should equal standard: diff {q_A1_15-q_std_15:+.2e})")
nu_A0 = make_nu_eff(0.0)
line(f"nu_eff(A=0)    q(1.5) = {q_of(nu_A0,1.5):.6f}   (pure Newtonian => must be ~0)")

# ------------------------------------------------------------------------------------
# Q2 helper (frozen convention)
# ------------------------------------------------------------------------------------
def pref_of(a0):
    # a0/R_M = sqrt(a0^3/GM)  [s^-2]
    return np.sqrt(a0**3 / GM)

def Q2_of(nu, a0, eta):
    return 1.5 * q_of(nu, eta) * pref_of(a0)     # |Q2| = (3/2) q(eta) a0/R_M

# ------------------------------------------------------------------------------------
# footings: eta and eps_e = eta^2 at each a0
# ------------------------------------------------------------------------------------
head("FOOTINGS  (g_e = Vc^2/R0 at the Sun; eta = g_e/a0; eps_e = eta^2)")
line(f"g_e = Vc^2/R0 = {g_e:.4e} m/s^2   (Vc=229 km/s, R0=8.2 kpc)")
footings = []
for name, a0 in (("standard  a0=1.20e-10", A0_STD),
                 ("canonical a0=9.36e-11", A0_CAN),
                 ("alt       a0=1.128e-10", A0_ALT)):
    eta = g_e / a0
    eps_e = eta**2
    footings.append((name, a0, eta, eps_e))
    line(f"{name}:  eta={eta:.4f}  eps_e={eps_e:.4f}  a0/R_M={pref_of(a0):.4e} s^-2")

# baseline (A=1, unscreened) Q2 at each footing, for reference
head("BASELINE  (A=1, unscreened standard mu -- the referee's FAILING quadrupole)")
line(f"{'footing':<26}{'eta':>7}{'q(eta)':>9}{'Q2[1e-27 s^-2]':>18}")
Q2_base = {}
for name, a0, eta, eps_e in footings:
    q = q_of(nu_standard, eta)
    Q2 = 1.5 * q * pref_of(a0)
    Q2_base[name] = Q2
    line(f"{name:<26}{eta:>7.4f}{q:>9.4f}{Q2*1e27:>18.3f}")

# ------------------------------------------------------------------------------------
# THE SCAN:  Q2(m, eps_s) at each footing
# ------------------------------------------------------------------------------------
CASSINI_95 = 5.1e-27     # 95% upper limit (task); central (1.6+-1.8)e-27

def A_screen(eps, m, eps_s):
    return 1.0 / (1.0 + (eps / eps_s)**m)

m_list   = [2, 4, 8, 16]
eps_s_list = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

# cache q as a function of A (A depends on (m,eps_s,eps_e); many collisions) per footing-eta
def q_cached(eta):
    cache = {}
    def f(A):
        key = round(A, 6)
        if key not in cache:
            cache[key] = q_of(make_nu_eff(A), eta) if A > 1e-9 else 0.0
        return cache[key]
    return f

for name, a0, eta, eps_e in footings:
    head(f"Q2(m, eps_s) MAP   [1e-27 s^-2]   footing: {name}   (eta={eta:.3f}, eps_e={eps_e:.3f})")
    line(f"Cassini 95% upper = {CASSINI_95*1e27:.1f}e-27 ;  baseline (A=1) Q2 = {Q2_base[name]*1e27:.2f}e-27")
    qf = q_cached(eta)
    pref = pref_of(a0)
    hdr = "  m \\ eps_s " + "".join(f"{es:>8.1f}" for es in eps_s_list)
    print(hdr)
    passmap = {}
    for m in m_list:
        row = f"  m={m:<7d}"
        for es in eps_s_list:
            A = A_screen(eps_e, m, es)
            Q2 = 1.5 * qf(A) * pref
            passmap[(m, es)] = Q2
            row += f"{Q2*1e27:>8.2f}"
        print(row)
    # also print the underlying A(eps_e) map (screening amplitude) for transparency
    print("  --- screening amplitude A(eps_e) at this footing ---")
    hdr = "  m \\ eps_s " + "".join(f"{es:>8.1f}" for es in eps_s_list)
    print(hdr)
    for m in m_list:
        row = f"  m={m:<7d}"
        for es in eps_s_list:
            row += f"{A_screen(eps_e, m, es):>8.4f}"
        print(row)
    # Cassini-passing region
    passing = [(m, es) for m in m_list for es in eps_s_list if passmap[(m, es)] < CASSINI_95]
    line("")
    line(f"Cassini-PASSING (Q2 < {CASSINI_95*1e27:.1f}e-27) cells: {len(passing)} of {len(m_list)*len(eps_s_list)}")
    if passing:
        # describe as: for each m, the eps_s threshold below which it passes
        for m in m_list:
            passes = [es for es in eps_s_list if passmap[(m, es)] < CASSINI_95]
            if passes:
                line(f"   m={m:2d}: passes for eps_s <= {max(passes):.1f}  (A(eps_e) <= {A_screen(eps_e,m,max(passes)):.3f})")
            else:
                line(f"   m={m:2d}: NEVER passes on this eps_s grid")

# ------------------------------------------------------------------------------------
# LIMIT CHECK (4): isolated galaxy e->0 => eps->0 => A->1 => mu_eff == mu_gal exactly
# ------------------------------------------------------------------------------------
head("(4) ISOLATED-GALAXY LIMIT  e->0 (eps->0, A->1):  mu_eff == mu_gal  =>  v^4 = G M a0")
xg = np.geomspace(1e-3, 1e3, 9)
A_iso = A_screen(0.0, 8, 2.0)   # eps=0, any (m,eps_s)
line(f"A(eps=0; m=8, eps_s=2.0) = {A_iso:.12f}   (must be 1)")
mu_eff_iso = 1.0 - A_iso * (1.0 - mu_gal(xg))
line(f"max|mu_eff(eps=0) - mu_gal| over x in [1e-3,1e3] = {np.max(np.abs(mu_eff_iso - mu_gal(xg))):.2e}")
# deep-MOND asymptotic: mu_gal -> x  => g = sqrt(g_N a0) => v^4 = G M a0
xdeep = 1e-4
line(f"deep-MOND (x={xdeep:g}): mu_eff = {1.0 - A_iso*(1.0-mu_gal(xdeep)):.6e}  ~ x = {xdeep:g}  => v^4=GMa0 EXACT")

# ------------------------------------------------------------------------------------
# LIMIT CHECK (5): strong screening kills BOTH mu_eff->1 AND d mu_eff/dx ->0
# ------------------------------------------------------------------------------------
head("(5) STRONG-SCREENING LIMIT  (A->0):  mu_eff->1  AND  d mu_eff/dx ->0  (both kill Q2)")
# d mu_eff/dx = A * d mu_gal/dx ;  d mu_gal/dx = (1+x^2)^(-3/2)
for A in (1.0, 0.5, 0.2, 0.05, 0.0):
    x_eta = 2.0
    mu_eff_val = 1.0 - A * (1.0 - mu_gal(x_eta))
    dmu = A * (1.0 + x_eta**2)**(-1.5)
    line(f"A={A:<5}:  mu_eff(x=2) = {mu_eff_val:.5f}   d mu_eff/dx|_(x=2) = {dmu:.5e}   (both ->1,0 as A->0)")
line("")
line("Q2 amplitude is carried by (nu_eff - 1) ~ A*(nu_standard - 1); A->0 drives it to 0 linearly.")

# quantify the (near-)linearity Q2(A)/Q2(A=1) at a representative footing (canonical)
name, a0, eta, eps_e = footings[1]
head(f"Q2(A)/Q2(A=1) linearity check  (footing {name}, eta={eta:.3f})")
qf = q_cached(eta)
q1 = qf(1.0)
line(f"{'A':>7}{'q(A)':>10}{'q(A)/q(1)':>12}{'A (linear ref)':>16}")
for A in (1.0, 0.5, 0.3, 0.2, 0.1, 0.05, 0.02):
    line(f"{A:>7.2f}{qf(A):>10.5f}{qf(A)/q1:>12.4f}{A:>16.2f}")

print("\nDONE.")
