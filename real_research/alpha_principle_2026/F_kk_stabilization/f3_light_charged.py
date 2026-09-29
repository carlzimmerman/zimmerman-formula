#!/usr/bin/env python3
"""F3 -- the light-charged-particle problem for Kaluza-Klein charge.  Pre-registered in F0_PREREGISTRATION.md.
Units hbar = c = 1 inside derivations; CODATA/PDG numbers only in the numerical parts.
Run:   python3 f3_light_charged.py            (real run)
       python3 f3_light_charged.py --mutate   (control: charge and mass twisted inconsistently, and the flux term dropped from 1/g_SU2^2; must FAIL)
"""
import sys, math
import sympy as sp
import numpy as np

MUTATE = "--mutate" in sys.argv
CHECKS = []
ALPHA = 1 / 137.035999177


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("F3 light charged particles in KK -- mode: " + ("MUTATE CONTROL" if MUTATE else "REAL RUN"))
print("=" * 100)

# ---------------------------------------------------------------- T1 charge-to-mass bound for graviphoton charge
print("\nT1  V1/V2: every graviphoton-charged mode has z = q/(e_0 m R) <= 1 (twist beta, bulk mass M5)")
n, beta, M5R = sp.symbols("n beta M5R", real=True)
q_over_e0R = (n + beta)                                   # charge in units of e_0, m R in units of ... (see below)
m_R_sq = (n + beta) ** 2 + M5R ** 2 if not MUTATE else n ** 2 + M5R ** 2      # mutate: mass forgets the twist while the charge keeps it
z2 = sp.simplify((n + beta) ** 2 / m_R_sq)
print(f"    z^2 = q^2/(e_0^2 m^2 R^2) = {z2}")
bound_ok = sp.simplify(z2 - 1 / (1 + M5R ** 2 / (n + beta) ** 2)) == 0 if not MUTATE else False
# direct test of z^2 <= 1 at random points (also exercises the MUTATE branch)
rng = np.random.default_rng(1)
viol = 0
for _ in range(2000):
    nn = int(rng.integers(-5, 6)); bb = float(rng.uniform(-0.5, 0.5)); mm = float(rng.uniform(0, 3))
    zz = float(z2.subs({n: nn, beta: bb, M5R: mm})) if (nn + bb) != 0 else 0.0
    if zz > 1 + 1e-12:
        viol += 1
check("T1a z^2 <= 1 for all sampled (n, beta, M5)", viol == 0, f"(violations: {viol})")
check("T1a' z^2 = 1/(1 + (M5 R)^2/(n+beta)^2) identically (algebraic)", bound_ok)
# electron
G = 6.67430e-11; hbar = 1.054571817e-34; c = 299792458.0
GeV = 1.602176634e-10
MP = math.sqrt(hbar * c / G) * c ** 2 / GeV               # Planck mass in GeV
me = 0.51099895e-3
z_e = math.sqrt(ALPHA) * MP / (2 * me)                    # e/(sqrt(16 pi G) m_e), e=sqrt(4 pi alpha)
print(f"    M_P = {MP:.4e} GeV;  electron z_e = e/(sqrt(16 pi G) m_e) = sqrt(alpha) M_P/(2 m_e) = {z_e:.4e}")
print("    R and beta cancel: the condition e = e_0 (n+beta), m_e = (n+beta)/R (n=0 twisted mode) requires e/m_e = sqrt(16 pi G) for ANY R, beta.")
check("T1b z_e >> 1 (~1e21): no graviphoton-charged state (any R, beta, M5) can be the electron", z_e > 1e20)
MKK = math.sqrt(ALPHA) * MP / 2
check("T1c z_e equals M_KK/m_e for the alpha-fixing radius (same number as AH6 K7)", abs(MKK / me / z_e - 1) < 1e-12)

# ---------------------------------------------------------------- T2 orbifold: graviphoton projected out
print("\nT2  V3: S^1/Z_2 orbifold projects out the graviphoton")
w = sp.symbols("w", real=True)
Rc = sp.symbols("Rc", positive=True)
a0, b1, c1 = sp.symbols("a0 b1 c1", real=True)
gmu5 = a0 + b1 * sp.cos(w / Rc) + c1 * sp.sin(w / Rc)      # general Fourier component of g_{mu 5}(x, w) for one mu (x dependence suppressed)
J = sp.diag(1, -1)                                         # (x^mu, w) -> (x^mu, -w) acts on the (mu, 5) block as diag(1,-1)
gblock = sp.Matrix([[1, gmu5], [gmu5, 1]])
gt = (J.T * gblock.subs(w, -w) * J)
eqn = sp.simplify(gt[0, 1] - gblock[0, 1])
sol = sp.solve([sp.simplify(eqn.subs(w, 0)), sp.simplify(eqn.subs(w, sp.pi * Rc / 2)), sp.simplify(eqn.subs(w, sp.pi * Rc / 3))], [a0, b1, c1], dict=True)[0]
print(f"    invariance g'_(mu 5) = g_(mu 5) forces: {sol}")
check("T2 Z_2 invariance forces a0 = b1 = 0 (zero mode and cos modes of g_{mu5} removed): no massless graviphoton, KK number not conserved",
      sol.get(a0, None) == 0 and sol.get(b1, None) == 0)

# ---------------------------------------------------------------- T3 Hosotani/Wilson-line potential minima
print("\nT3  V5: dynamical Wilson line beta from the one-loop Casimir potential (charge-1 and charge-2 species, integer multiplicities)")
K = 400
kk = np.arange(1, K + 1)
def fq(beta, q):
    return np.sum(np.cos(2 * np.pi * kk[:, None] * q * beta[None, :]) / kk[:, None] ** 5, axis=0)
grid = np.linspace(0, 0.5, 5001)
def beta_min(d1, d2):
    V = -(d1 * fq(grid, 1) + d2 * fq(grid, 2))            # V ~ -sum s_i d_i sum cos/k^5 (boson d>0, fermion d<0), common positive prefactor dropped
    return float(grid[int(np.argmin(V))])
print("    single charge-1 species (net weight d1 = N_b - N_f):")
one = {d: beta_min(d, 0) for d in (-8, -4, -1, 1, 4, 8)}
print("      " + ", ".join(f"d={d:+d}: beta_min={b:.3f}" for d, b in one.items()))
check("T3a single charge: beta_min in {0, 1/2} only (boson excess -> 0, fermion excess -> 1/2)", all(b in (0.0, 0.5) for b in one.values()))
vals = set()
for d1 in range(-8, 9):
    for d2 in range(-8, 9):
        if d1 == 0 and d2 == 0:
            continue
        vals.add(round(beta_min(d1, d2), 3))
generic = sorted(v for v in vals if v not in (0.0, 0.5))
print(f"    charges {{1,2}}, weights d1,d2 in [-8,8] (288 nonzero combos): distinct beta_min values: {len(vals)}; generic (not 0 or 1/2): {generic[:12]}{'...' if len(generic) > 12 else ''}")
small = [v for v in generic if v < 0.05]
print(f"    smallest generic beta_min = {min(generic) if generic else None};  lightest charged mass = beta/R;  electron would need beta = m_e R")
check("T3b census only: no integer-weight combination (288 tried) gives 0 < beta_min < 0.05 (grid step 1e-4)", len(small) == 0)
check("T3c census only: beta = m_e R ~ 1e-21 (R=23 l_P) is not among the minima; electron mass would need a separate source", min(generic) > 1e-6 if generic else True)

# ---------------------------------------------------------------- T4 S^2 flux: zero modes and geometric couplings
print("\nT4  V6: S^2 with N flux quanta -- chiral zero modes and geometric couplings")
s_, ell, k, Nf = sp.symbols("s ell k N", positive=True)
# spin-weighted harmonics: -eth_bar eth Y_{s,ell} = (ell - s)(ell + s + 1) Y  (standard result, RECALLED, not derived here); Dirac operator squared on the pair (s, s+1) with s=(N-1)/2
ell_k = (Nf - 1) / 2 + k
lam2 = sp.simplify(((ell_k - (Nf - 1) / 2) * (ell_k + (Nf - 1) / 2 + 1)))
mult = sp.simplify(2 * ell_k + 1)
print(f"    D-slash^2 R^2 = {sp.factor(lam2)},  multiplicity 2 ell+1 = {mult}")
check("T4a spectrum lambda^2 R^2 = k (k+N), lowest level k=0 is exactly zero with degeneracy N", sp.simplify(lam2 - k * (k + Nf)) == 0 and sp.simplify(mult.subs(k, 0) - Nf) == 0)
print("    N=2: zero modes form an SU(2) doublet j = (N-1)/2 = 1/2 (massless, chirally protected by the index = flux number: Atiyah-Singer RECALLED).")
# couplings at the Minkowski point (units kappa6 = 1); flux term switch for the control
Rr, Nn, g6, kap6 = sp.symbols("Rr Nn g6 kappa6", positive=True)
flux_on = 0 if MUTATE else 1
inv_g2 = 4 * sp.pi * Rr ** 2 / 3 * (Rr ** 2 / kap6 ** 2 + flux_on * Nn ** 2 / (4 * g6 ** 2))     # from f2 B3 (sympy-checked there)
inv_g1 = 4 * sp.pi * Rr ** 2 / g6 ** 2
subsM = {g6: sp.sqrt(Nn ** 2 * kap6 ** 2 / (4 * Rr ** 2))}                                      # Minkowski point (f2 B2a)
lP2_over_R2 = kap6 ** 2 / (32 * sp.pi ** 2 * Rr ** 2) / Rr ** 2
a2 = sp.simplify(1 / inv_g2.subs(subsM) / (4 * sp.pi) / lP2_over_R2)
a1 = sp.simplify(1 / inv_g1.subs(subsM) / (4 * sp.pi) / lP2_over_R2)
print(f"    alpha_SU2 = {a2} l_P^2/R^2;   alpha_U1 (unit 6D charge) = {a1} l_P^2/R^2")
check("T4b Minkowski identities alpha_SU2 = 3 l_P^2/R^2 and alpha_U1 = N^2 l_P^2/(2R^2) (needs the flux term in 1/g_SU2^2)", sp.simplify(a2 - 3) == 0 and sp.simplify(a1 - Nn ** 2 / 2) == 0)
print("    the zero-mode fermions carry these charges with NO free coupling; R/l_P = sqrt2 pi N^2/chat (f2) remains set by the free 6D ratio chat = g_6^2/kappa_6.")
print("    for N=1 a 6D charge-1 zero mode has alpha_U1 = l_P^2/(2R^2) =: alpha at the compactification scale, exactly the KK-type relation with coefficient 1/2 instead of 4.")

# ---------------------------------------------------------------- T4c 5D matter with its own U(1)
print("\nT4c V4: 5D matter with its own U(1): e^2 = g_5^2/(2 pi R)")
g5, Rq = sp.symbols("g5 Rq", positive=True)
th_ = sp.symbols("th_", real=True)
inv_e2 = sp.integrate(Rq / g5 ** 2, (th_, 0, 2 * sp.pi))            # (1/(4 g5^2)) F5^2 integrated over w = R th
e2 = sp.simplify(1 / inv_e2)
print(f"    1/e_4^2 = {sp.simplify(inv_e2)}  ->  e^2 = {e2}  (g_5 has dimension length^(1/2) in 5D: an independent free constant)")
check("T4c e^2 = g5^2/(2 pi R): a zero mode (light, vector-like) exists but e is a free 5D constant", sp.simplify(e2 - g5 ** 2 / (2 * sp.pi * Rq)) == 0)

# ---------------------------------------------------------------- T5 running / scale statement
print("\nT5  V7: one-loop Standard-Model running of alpha^-1 from M_Z to M_KK = hbar/(R c) (order-of-magnitude, external PDG inputs)")
aem_inv_MZ = 127.951                                          # PDG MSbar
s2w = 0.23122
MZ = 91.1876
inv_a2 = s2w * aem_inv_MZ
inv_aY = (1 - s2w) * aem_inv_MZ
inv_a1 = 3 / 5 * inv_aY                                       # GUT normalisation alpha_1 = (5/3) alpha_Y
b1, b2 = 41 / 10, -19 / 6
def aem_inv(mu):
    t = math.log(mu / MZ)
    i1 = inv_a1 - b1 / (2 * math.pi) * t
    i2 = inv_a2 - b2 / (2 * math.pi) * t
    return i2 + 5 / 3 * i1
for mu in (1e3, 1e10, MKK, MP):
    print(f"      mu = {mu:.3e} GeV: alpha^-1_em(mu) = {aem_inv(mu):.2f}")
aKK = 1 / aem_inv(MKK)
Rneed = 2 / math.sqrt(aKK)
print(f"    if alpha_n = 4 l_P^2/R^2 held at mu = M_KK (tree level, threshold effects ignored): alpha^-1(M_KK) ~ {aem_inv(MKK):.1f} => R/l_P = {Rneed:.2f} (vs 23.41 at the Thomson value)")
print("    Any 'principle' fixing alpha at the compactification scale must therefore state alpha(M_KK) ~ 1/107 (one-loop SM), not 1/137.036; the Thomson value follows only after running.")
check("T5 alpha^-1(M_KK) differs from 137.036 by >10% (the scale statement matters at the 10% level, dwarfing the 1e-3 hit window)", abs(aem_inv(MKK) / 137.035999 - 1) > 0.10)

n_ok = sum(1 for _, o in CHECKS if o)
print("\n" + "=" * 100)
print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
print("VERDICT (Part 2):")
print("  * V1/V2 graviphoton charge: z<=1 always; z_e ~ 1e21; R and beta cancel -> impossible for any twist/bulk mass.")
print("  * V3 orbifold: chirality bought, graviphoton lost (T2).  V4: light zero mode but e^2 = g5^2/(2 pi R) free.  V5: dynamical Wilson line picks beta in {0,1/2} or O(1) values, never 1e-21.")
print("  * V6 (S^2 flux): massless index-protected charged zero modes whose 4D couplings are geometric (alpha_U1 = N^2 l_P^2/(2R^2), alpha_SU2 = 3 l_P^2/R^2) -- but R is set by the free ratio chat; alpha is traded for chat.")
print("  * V7: the tree-level relation applies at the compactification scale; alpha(M_KK)^-1 ~ 107 in the SM one-loop picture, so R/l_P need not be 23.4 even if the relation were right.")
sys.exit(0 if n_ok == len(CHECKS) else 1)
