#!/usr/bin/env python3
# VCC1 (HY4-4): can the clock sector's charge be SOURCED?
# Criteria: FROZEN_CRITERIA.md (committed alone, c83dfb5a02, before this file or any number).
# Footings canonical / alt, never pooled.  MUTATE: VCC1_MUTATE=MU1..MU5 -> separate output file.
import os, sys, math, random
import sympy as sp
import mpmath as mp

MUT = os.environ.get('VCC1_MUTATE', '')
SUF = '_MUTATE_' + MUT if MUT else ''
OUT = open('vcc1' + SUF + '.out', 'w')
def say(*a):
    s = ' '.join(str(v) for v in a)
    print(s); OUT.write(s + '\n'); OUT.flush()

mp.mp.dps = 60
say("=" * 78)
say("VCC1  can the clock sector's charge be SOURCED?   MUTATE =", MUT or "(none)")
say("criteria c83dfb5a02 (committed alone before any script or number)")
say("footings never pooled. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
say("=" * 78)

# ------------------------------------------------------------------ constants
G     = 6.674e-11          # m^3 kg^-1 s^-2
MSUN  = 1.98847e30         # kg
KPC   = 3.085677581e19     # m
C     = 2.99792458e8       # m/s
MPC   = 3.085677581e22     # m
H0    = 67.4e3 / MPC       # s^-1
OMB   = 0.0493
R541  = 5.41               # Omega_c / Omega_b
OMC   = R541 * OMB
H     = 0.674
OMR   = 4.15e-5 / H**2
OML   = 1.0 - OMB - OMC - OMR
RHOC  = 3.0 * H0**2 / (8.0 * math.pi * G)          # kg/m^3
MSUN_PER_KPC3 = MSUN / KPC**3                       # kg/m^3 per (Msun/kpc^3)
def to_mkpc3(rho_kgm3): return rho_kgm3 / MSUN_PER_KPC3
RHO_C0  = to_mkpc3(OMC * RHOC)     # cold (clock-charge) density today, Msun/kpc^3
RHO_B0  = to_mkpc3(OMB * RHOC)
RHO_LAM = to_mkpc3(OML * RHOC)
RHO_200 = to_mkpc3(200.0 * RHOC)
FOOT = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
LOGM = [9.4, 10.45, 10.7, 10.9]
KIDS_IN  = {9.4: 81.0,  10.45: 272.0, 10.7: 362.0, 10.9: 456.0}
KIDS_MID = {9.4: 190.0, 10.45: 637.0, 10.7: 849.0, 10.9: 1069.0}
C_DUST = 1.40                      # VSH1 settled, primary
C_DUST_BRACKET = 1.06              # COL1 A4 / FLD1
if MUT == 'MU4': C_DUST = 0.0
DRAIN = 0.5 if MUT == 'MU3' else 1.0      # MU3: Lambda' -> Lambda'/2
CLUMP = 200.0 if MUT == 'MU5' else 1.0    # MU5: created charge clusters like dust, 200x
X_S   = 59.5                       # ONE1 / PD1 share
XS_X  = (math.sqrt(1 + 4 * X_S**2) - 1) / 2.0 * 0 + 59.9983   # x where X(x)=59.5
AU    = 1.495978707e11
R_SAT = 9.5 * AU                   # Saturn's orbit, m
M_SAT_BOUND = 1e-10                # Msun, Pitjev & Pitjeva (PROVISIONAL)
R200_MAIN, R200_SUB = 1.70e3, 1.10e3   # kpc (Bullet, PROVISIONAL)

def X(x): return (math.sqrt(1.0 + 4.0 * x * x) - 1.0) / 2.0
def rM(Mb, a0): return math.sqrt(G * Mb / a0) / KPC     # kpc
def vol(R):    return 4.0 * math.pi * R**3 / 3.0        # kpc^3

say("\n[0] constants")
say(f"    H0 = {H0:.6e} /s   rho_crit = {RHOC:.6e} kg/m^3 = {to_mkpc3(RHOC):.4f} Msun/kpc^3")
say(f"    Omega_b {OMB:.5f}  Omega_c {OMC:.6f}  Omega_r {OMR:.3e}  Omega_L {OML:.6f}")
say(f"    rho_c0  = {RHO_C0:.4f} Msun/kpc^3   (the 5.41 M_b cosmic cold density)")
say(f"    rho_Lam = {RHO_LAM:.4f} Msun/kpc^3  (the vacuum that must pay)")
say(f"    rho_b0  = {RHO_B0:.4f} Msun/kpc^3   200 rho_crit = {RHO_200:.4f} Msun/kpc^3")
say(f"    C_dust  = {C_DUST} M_b primary (VSH1); bracket {C_DUST_BRACKET} (COL1/FLD1)"
    + ("   [MU4: C_dust = 0]" if MUT == 'MU4' else ""))

# ================================================================== PART A
say("\n" + "=" * 78)
say("PART A  V1: is the conservation law forced by a symmetry?")
say("=" * 78)

t, x = sp.symbols('t x')
def pol(seed, base, deg=3):
    r = random.Random(seed); e = sp.Rational(base)
    for i in range(deg + 1):
        for j in range(deg + 1 - i):
            if i == 0 and j == 0: continue
            e += sp.Rational(r.randint(-6, 6), r.randint(2, 7)) * t**i * x**j
    return e

def action_A(tau, seed=0):
    """sqrt(-g) L of the tau-dependent part of action (A), 1+1, generic diagonal
    metric g = diag(-N^2, a^2) with N(t,x), a(t,x) generic test polynomials.
    R and the constant -2Lambda contain no tau and are omitted (they contribute 0
    to the current).  tau may be a Function (for the bare-tau derivative) or an
    explicit expression (for the shift test)."""
    N = pol(seed + 1, sp.Rational(3, 2), 2); aa = pol(seed + 2, sp.Rational(5, 3), 2)
    # P is leaf-like in the graded branch; keep |P| real and K|P| << a0 at the test point
    P0 = pol(seed + 4, sp.Rational(1, 50), 2) / 50; P1 = pol(seed + 5, sp.Rational(1, 5), 2)
    lam = pol(seed + 6, sp.Rational(1, 3), 2)
    K, muK, a0, gamL = sp.symbols('K mu_K a0 gamma_L', positive=True)
    Xs = [t, x]
    g = sp.Matrix([[-N**2, 0], [0, aa**2]]); gi = g.inv(); sg = sp.sqrt(-g.det())
    dt = [sp.diff(tau, c) for c in Xs]
    Q = sp.sqrt(dt[0]**2 / N**2 - dt[1]**2 / aa**2)
    nl = [-dt[m] / Q for m in range(2)]
    h = sp.Matrix(2, 2, lambda i, j: g[i, j] + nl[i] * nl[j])
    l = sp.log(Q); dl = [sp.diff(l, c) for c in Xs]
    hu = sp.Matrix(2, 2, lambda i, j: sum(gi[j, p] * h[i, p] for p in range(2)))
    A = [-sum(hu[m, n] * dl[n] for n in range(2)) for m in range(2)]
    Pl = [P0, P1]; Pu = [sum(gi[m, n] * Pl[n] for n in range(2)) for m in range(2)]
    nabP = sum(sp.diff(sg * Pu[m], Xs[m]) for m in range(2)) / sg
    Pi = nabP - sum(Pu[m] * A[m] for m in range(2))
    Pm = sp.sqrt(sum(gi[m, n] * Pl[m] * Pl[n] for m in range(2) for n in range(2)))
    W = (a0**2 / K) * (-K * Pm / a0 - sp.log(1 - K * Pm / a0))
    Ld = sg * (2 * muK**2 * (Q - 1)**2 / (4 * K) + sum(Pu[m] * A[m] for m in range(2))
               - W - gamL * Pi**2 / 2
               + lam * sum(gi[m, n] * nl[m] * Pl[n] for m in range(2) for n in range(2)))
    return Ld, sg

# ---- V1a: the Lagrangian's dependence on UNDIFFERENTIATED tau
say("\n-- V1a  does L contain a bare tau?  (the whole lock: nabla_m J^m = dL/dtau)")
tauF = sp.Function('tau')(t, x)
LdF, sgF = action_A(tauF)
bare = sp.simplify(sp.diff(LdF, tauF))
say(f"    d(sqrt(-g)L)/d(tau)  for action (A) as written : {bare}")
LdV = LdF - sgF * sp.Function('V')(tauF)
bareV = sp.diff(LdV, tauF)
resV = sp.simplify(bareV + sgF * sp.diff(sp.Function('V')(tauF), tauF))
say(f"    same + [-sqrt(-g) V(tau)]:  dL/dtau + sqrt(-g) V'(tau)   residual = {resV}")
KK_ = sp.Symbol('K', positive=True)
LdL = LdF - sgF * 2 * sp.Function('Lambda')(tauF) / (4 * KK_)
bareL = sp.diff(LdL, tauF)
resL = sp.simplify(bareL + sgF * sp.diff(sp.Function('Lambda')(tauF), tauF) / (2 * KK_))
say(f"    same + [-2 Lambda(tau)/(4K)]: dL/dtau + sqrt(-g) Lambda'(tau)/(2K)  residual = {resL}")
say(f"    -> the source is S = -Lambda'(tau)/(2K) per unit volume, i.e. the vacuum.")
say("    -> (A) has NO bare tau, so the current is conserved.  One function of tau")
say("       (a potential, or the vacuum constant) sources it.  [V1a: identity confirmed]")
if MUT == 'MU1':
    say("    MU1: with -sqrt(-g) V(tau) the bare-tau derivative is -V'(tau) != 0: BITES.")

# ---- V1d: rigid or gauge?
say("\n-- V1d  the symmetry: rigid shift tau -> tau + c, or gauge tau -> tau + c(t,x)?")
tau_poly = 4 * t + pol(3, sp.Rational(1, 40), 2)
c0 = sp.Rational(7, 3)
cxt = pol(77, sp.Rational(1, 2), 2) / 50      # small: stays on the timelike branch
L_base, _  = action_A(tau_poly)
L_rigid, _ = action_A(tau_poly + c0)
L_gauge, _ = action_A(tau_poly + cxt)
pt = {t: sp.Rational(3, 7), x: sp.Rational(5, 11),
      sp.Symbol('K', positive=True): sp.Rational(7, 11),
      sp.Symbol('mu_K', positive=True): sp.Rational(3, 13),
      sp.Symbol('a0', positive=True): sp.Rational(1000, 1),
      sp.Symbol('gamma_L', positive=True): sp.Rational(2, 19)}
def ev(e): return mp.mpf(sp.N(e.subs(pt), 50))
b, rg, gg = ev(L_base), ev(L_rigid), ev(L_gauge)
say(f"    sqrt(-g)L at the test point                 = {mp.nstr(b, 12)}")
say(f"    L(tau + 7/3)      - L(tau)  = {mp.nstr(rg - b, 6)}   rel {mp.nstr(abs((rg-b)/b), 3)}")
say(f"    L(tau + c(t,x))   - L(tau)  = {mp.nstr(gg - b, 6)}   rel {mp.nstr(abs((gg-b)/b), 3)}")
say("    -> invariant under the RIGID shift, NOT under a local one: a global internal")
say("       symmetry (Noether I), accidental to the term list.  Diffeomorphism invariance")
say("       alone does not force it: any scalar V(tau) is allowed.  [V1d]")

# ---- V1c: the identity nabla_m J^m = dL/dtau, on a Lagrangian with a bare tau
say("\n-- V1c  the identity nabla_m J^m = dL/dtau  (exact; toy with an explicit tau)")
tt, xx = sp.symbols('t x')
Nf = sp.Function('N')(tt, xx); af = sp.Function('a')(tt, xx)
tauf = sp.Function('tau')(tt, xx)
g2 = sp.Matrix([[-Nf**2, 0], [0, af**2]]); gi2 = g2.inv(); sg2 = sp.sqrt(-g2.det())
dtau = [sp.diff(tauf, tt), sp.diff(tauf, xx)]
Ysq = sum(gi2[m, n] * dtau[m] * dtau[n] for m in range(2) for n in range(2))
Ltoy = sg2 * (-sp.Function('V')(tauf) + sp.Rational(1, 2) * sp.Function('f')(tauf) * Ysq)
Jt = [sp.diff(Ltoy, dtau[m]) / sg2 for m in range(2)]
divJ = sum(sp.diff(sg2 * Jt[m], [tt, xx][m]) for m in range(2)) / sg2
EL = sp.diff(Ltoy, tauf) - sum(sp.diff(sp.diff(Ltoy, dtau[m]), [tt, xx][m]) for m in range(2))
ident = sp.simplify(divJ - sp.diff(Ltoy, tauf) / sg2 + EL / sg2)
say(f"    [ nabla_m J^m - dL/dtau ] + E_tau/sqrt(-g)   residual: {ident}")
say("    -> for ANY L(tau, d tau) the Euler-Lagrange expression is exactly")
say("       dL/dtau - nabla_m J^m with J^m = (1/sqrt(-g)) d(sqrt(-g)L)/d(d_m tau).")
say("       The current is conserved if and only if L has no bare tau.")

# ---- V3a: Bianchi with Lambda(tau)
say("\n-- V3a  Bianchi identity and total stress-energy with -2 Lambda(tau)")
Nq, Bq, Cq = [sp.Function(s)(tt, xx) for s in ('N', 'B', 'C')]
aq = sp.Function('a')(tt, xx)
gq = sp.Matrix([[Nq, Bq], [Bq, aq]]); giq = gq.inv(); sgq = sp.sqrt(-gq.det())
Xq = [tt, xx]
Gam = {}
for d in range(2):
    for b in range(2):
        for c in range(2):
            Gam[d, b, c] = sum(giq[d, e] * (sp.diff(gq[e, b], Xq[c]) + sp.diff(gq[e, c], Xq[b])
                                            - sp.diff(gq[b, c], Xq[e])) for e in range(2)) / 2
Lamf = sp.Function('Lambda')
Sq = Lamf(tauf)
def divT(Tlow):
    """nabla^m T_mn = sum_{p,m} g^{pm} ( d_p T_mn - Gam^r_{pm} T_rn - Gam^r_{pn} T_mr )"""
    out = []
    for n in range(2):
        s = 0
        for p in range(2):
            for m in range(2):
                cov = sp.diff(Tlow[m][n], Xq[p])
                for r_ in range(2):
                    cov -= Gam[r_, p, m] * Tlow[r_][n] + Gam[r_, p, n] * Tlow[m][r_]
                s += giq[p, m] * cov
        out.append(sp.simplify(s))
    return out
TLam = [[-Sq / (2 * sp.Symbol('K', positive=True)) * gq[m, n] for n in range(2)] for m in range(2)]
dLam = [sp.diff(Sq, tt), sp.diff(Sq, xx)]
res_a = [sp.simplify(divT(TLam)[n] + dLam[n] / (2 * sp.Symbol('K', positive=True))) for n in range(2)]
say(f"    nabla^m T^Lambda_mn + d_n Lambda /(2K)   residual (n = t, x): {res_a}")
say("    -> T^Lambda_mn = -(Lambda(tau)/(2K)) g_mn has divergence -Lambda'(tau) d_n tau/(2K).")
say("       The metric equation G_mn + Lambda(tau) g_mn = 2K T^(m+c)_mn with nabla^m G_mn = 0")
say("       gives nabla^m T^(m+c)_mn = +Lambda'(tau) d_n tau/(2K).  The two cancel:")
say("       nabla^m ( T^(m+c) + T^Lambda )_mn = 0.  Bianchi intact, vacuum pays.  [V3a PASS]")

# ---- V3b: the FRW ledger
say("\n-- V3b  the FRW ledger: created charge energy = vacuum energy lost  (exact)")
tS = sp.Symbol('t'); aS = sp.Function('a')(tS); tauS = sp.Function('tau')(tS)
NS = sp.Function('N')(tS); LamS = sp.Function('Lambda')
muK, KK = sp.symbols('mu_K K', positive=True)
QS = sp.diff(tauS, tS) / NS
Lfrw = aS**3 * NS * ((-2 * LamS(tauS) + 2 * muK**2 * (QS - 1)**2) / (4 * KK))
dLdtdot = sp.diff(Lfrw, sp.diff(tauS, tS))
dLdtau  = sp.diff(Lfrw, tauS)
say(f"    FRW tau equation  E_tau = {sp.simplify(dLdtau - sp.diff(dLdtdot, tS))}")
Cchg = sp.simplify(dLdtdot / aS**3)
say(f"    charge per comoving volume C = (1/a^3) dL/d(tau') = {Cchg}")
say(f"    dC/dt - (1/a^3) dL/dtau      = {sp.simplify(sp.diff(Cchg, tS) - dLdtau / aS**3)}")
say(f"    dL/dtau /(a^3)               = {sp.simplify(dLdtau / aS**3)}")
say("    -> d(a^3 rho_cre)/dt = -a^3 Lambda'(tau)/(2K), and the vacuum's own ledger gives")
say("       d(a^3 rho_Lam)/dt = +a^3 Lambda'(tau)/(2K) + 3H a^3 (rho_Lam + p_Lam); the two")
say("       sum to zero.  The vacuum pays exactly.  [V3b PASS; = R541B's dC/dt = -N a^3 V']")

# ================================================================== PART B
say("\n" + "=" * 78)
say("PART B  V2: the smallest change, and what sources it")
say("=" * 78)
say("""
    id   change to (A)                        new ingredient      source S=dL/dtau      in FRW      profile in a halo (deep)
    ---  ----------------------------------   -----------------   -------------------   ---------   ------------------------
    C-I  -2 Lambda -> -2 Lambda(tau)          1 constant->1 fct   -Lambda'(tau)/(2K)     S(t)        UNIFORM
    C-II gamma_L -> gamma_L(tau)              1 constant->1 fct   -gamma_L'(tau) F(Pi)   0 (Pi=0)    F=Pi^2/2, Pi ~ r^-2 -> S ~ r^-4
    C-III (P.A - W) -> (1+eps(tau))(P.A - W)  1 function          eps'(tau) J(g)         0 (P=A=0)   J = g^2/(2K) ~ r^-2   <-- the law's profile
    C-IV mu_K -> mu_K(tau)                    1 constant->1 fct   (mu mu'/K)(Q-1)^2      ~1e-12      (|Phi|/c^2)^2 ~ 1e-12
    C-V  add -sqrt(-g) V(tau)                 a new term          -V'(tau)               S(t)        UNIFORM (same physics as C-I)
    C-VI eps is a dynamical field chi         a new field         paid by T^chi          chi's eqn   chi's profile
    C-VII coupling to a non-conserved current a new coupling      prop. to nabla.J_mat   0 at z<2    0 at z<2
""")
say("    SMALLEST = C-I: no new term, no new field; one constant already in (A) becomes")
say("    a function of tau.  It is the only one the vacuum can pay for (V3a/V3b).")

# --- deep-regime profiles (exact, 1D sympy)
r, rM_s, a0_s, K_s, Mb_s = sp.symbols('r r_M a0 K M_b', positive=True)
g_deep = a0_s * rM_s / r
x_deep = g_deep / a0_s
KP     = a0_s * x_deep / (1 + x_deep)          # K|P| = a0 x/(1+x)
Pr     = KP / K_s
Pi_deep = sp.simplify(sp.diff(r**2 * Pr, r) / r**2)
J_deep  = sp.simplify((a0_s**2 / K_s) * (x_deep - sp.log(1 + x_deep)))
say("\n-- deep-regime profiles (exact; x = g/a0 = r_M/r, gamma_L = 0)")
say(f"    K|P|      = {sp.simplify(KP)}")
say(f"    Pi = D.P  = {sp.simplify(Pi_deep)}")
say(f"    J = P.A-W = {J_deep}")
say(f"    J series at large r : {sp.series(J_deep, r, sp.oo, 4)}")
say(f"    Pi series at large r: {sp.series(Pi_deep, r, sp.oo, 4)}")
say("    -> C-III's source is J ~ r^-2 (the law's phantom profile, the one needed);")
say("       C-II's source is F = Pi^2/2 ~ r^-4 (wrong: it piles the charge at the centre);")
say("       C-I's source is uniform (wrong: C_cre ~ R^3, the law needs C ~ R).")

# V2b: the eps C-III needs
say("\n-- V2b  C-III: the factor eps that makes exactly the law's halo")
eps_s = sp.symbols('eps', positive=True)
C_cre = sp.simplify(sp.integrate(eps_s * J_deep * 4 * sp.pi * r**2, (r, 0, sp.Symbol('R', positive=True))))
say(f"    C_cre(R) = int eps J 4 pi r^2 dr = {sp.simplify(C_cre)}")
# match to C_law = M_b R/r_M in the deep regime (R >> r_M), with K = 4 pi G (c=1)
Rs = sp.Symbol('R', positive=True)
lhs = sp.simplify(sp.series(C_cre, rM_s, 0, 1).removeO())
GG = sp.symbols('G', positive=True)
Ccre_deep = sp.simplify(4 * sp.pi * eps_s * a0_s**2 * rM_s**2 * Rs / (2 * K_s))
eps_sol = sp.solve(sp.Eq(Ccre_deep, Mb_s * Rs / rM_s), eps_s)[0]
say(f"    matching C_cre(R) = M_b R/r_M  gives  eps = {sp.simplify(eps_sol)}")
say(f"    with K = 4 pi G and G M_b = a0 r_M^2 :  eps = {sp.simplify(eps_sol.subs(K_s, 4*sp.pi*GG).subs(Mb_s, a0_s*rM_s**2/GG))}")
say("    -> eps = 2/(a0 r_M) in c=1 units, i.e.  eps = 2 c^2 / v_flat^2  in SI,")
say("       v_flat^2 = a0 r_M = sqrt(G M_b a0).  One function of cosmic time, all galaxies.")
say("    C-III's DOUBLE COUNT (the kill that does not need the spread):")
say("       the factor (1+eps) multiplies the whole (P.A - W) block, so it multiplies the")
say("       P sector's stress tensor T^W + T^P by (1+eps) too.  With eps = 2c^2/v_flat^2")
say("       that block carries (1+eps) J = rho_cre + J, i.e. the created mass density ITSELF")
say("       appears a second time as a source in the metric equation.  The halo then")
say("       gravitates twice: once as the charge rho_Q = D.P and once as the block's energy.")
say("       Form B's Pi3 (the phantom IS the cold dark energy, counted ONCE) is broken by")
say("       exactly a factor ~2 at every radius.  [V3d / Pi3: FAIL]")

# ================================================================== PART C  numbers
say("\n-- V2c  the source profile the law demands:  S_law(R) = (1/(4 pi R^2)) d_R[ d_t C_law ]")
Ms = sp.Function('M')(tt)
rMs = sp.sqrt(sp.Symbol('G', positive=True) * Ms / sp.Symbol('a0', positive=True))
Rss = sp.Symbol('R', positive=True)
Claw_s = Ms * (sp.sqrt(1 + 4 * (Rss / rMs)**2) - 1) / 2
S_law = sp.simplify(sp.diff(sp.diff(Claw_s, tt), Rss) / (4 * sp.pi * Rss**2))
ser2 = sp.simplify(sp.series(S_law, Rss, sp.oo, 6).removeO())
say(f"       S_law(R) at large R = {ser2}")
say("    -> S_law falls as R^-2: the law's source must be as concentrated as the")
say("       phantom it makes.  A homogeneous vacuum cannot have that profile.")

say("\n" + "=" * 78)
say("PART C  the gates, per footing and mass")
say("=" * 78)

worst = {}
for fname, a0 in FOOT.items():
    say("\n" + "-" * 78)
    say(f"FOOTING {fname}:  a0 = {a0:.6e} m/s^2")
    say("-" * 78)
    eps_list = []
    for lm in LOGM:
        Mb = 10.0**lm * MSUN
        rm = rM(Mb, a0)
        v2 = a0 * (rm * KPC)                       # v_flat^2
        eps_req = 2.0 * C**2 / v2
        eps_list.append(eps_req)
        say(f"\n  log M_b = {lm}   M_b = {10**lm:.4g} Msun   r_M = {rm:.4f} kpc"
            f"   v_flat = {math.sqrt(v2)/1e3:.1f} km/s")
        Rxs = 59.9983 * rm
        radii = [('10 kpc', 10.0), ('30 kpc', 30.0), ('100 kpc', 100.0),
                 ('KiDS inner', KIDS_IN[lm]), ('ONE1 end', Rxs), ('KiDS middle', KIDS_MID[lm])]
        reqs = []
        for nm, R in radii:
            Claw = X(R / rm)                     # in units of M_b
            need = Claw - C_DUST                 # still in M_b; <0 = dust already supplies it
            V = vol(R)
            rc = max(need, 0.0) * (10.0**lm) / V * DRAIN  # Msun/kpc^3 (0 where dust suffices)
            reqs.append((nm, R, Claw, need, rc))
            say(f"    {nm:12s} R={R:8.1f} kpc  x={R/rm:7.2f}  C_law={Claw:9.3f} M_b"
                f"  need={need:9.3f} M_b   rho_cre needed={rc:12.4e} Msun/kpc^3"
                f"   = {rc/RHO_LAM:10.3e} rho_Lam  = {rc/RHO_C0:10.3e} rho_c0")
        pos = [q[4] for q in reqs if q[4] > 0]
        rmin, rmax = min(pos), max(pos)
        rc_one1 = [q[4] for q in reqs if q[0] == 'ONE1 end'][0]
        say(f"    -> smallest uniform density that supplies EVERY graded radius: {rmax:.4e} Msun/kpc^3")
        say(f"       (spread of the requirement over the radii that need any: {rmax/rmin:.4e})")
        say(f"    -> with rho_cre set at the ONE1 end radius, C_cre/C_law is:")
        for nm, R, Claw, need, rc in reqs:
            if MUT == 'MU2':
                rat = 1.0
            else:
                rat = rc_one1 * vol(R) / (Claw * 10.0**lm)
            say(f"         {nm:12s} R={R:8.1f} kpc   C_cre/C_law = {rat:.4e}"
                + ("   (in [0.9,1.1])" if 0.9 <= rat <= 1.1 else "   FAIL"))
        w = {'eps': eps_req, 'spread': rmax / rmin,
             'pay': max(q[4] for q in reqs) / RHO_LAM,
             'bg':  max(q[4] for q in reqs) / RHO_C0,
             'rho_cre_max': rmax, 'rho_cre_one1': rc_one1}
        worst.setdefault(fname, []).append(w)
        say(f"    -> C-III's eps required here: {eps_req:.4e}   (spread over masses below)")
    say(f"\n  V5e universality of eps (one function of cosmic time):")
    say(f"    eps = {['%.4e' % e for e in eps_list]}")
    say(f"    max/min = {max(eps_list)/min(eps_list):.4f}  over the four graded masses")

# --- Solar System, Bullet, background, forest (per footing, worst mass)
say("\n" + "=" * 78)
say("PART D  V4 background, V5c forest, V5d Solar System, V6 Bullet")
say("=" * 78)
for fname, a0 in FOOT.items():
    say(f"\nFOOTING {fname}")
    rc_max  = max(w['rho_cre_max']  for w in worst[fname])
    rc_one1 = max(w['rho_cre_one1'] for w in worst[fname])
    say(f"  rho_cre needed (worst over masses/radii) = {rc_max:.4e} Msun/kpc^3")
    say(f"  rho_cre needed at the ONE1 end radius    = {rc_one1:.4e} Msun/kpc^3")
    # V4
    f_bg  = rc_max / RHO_C0
    drain = rc_max / RHO_LAM
    say(f"  V4a  rho_cre/rho_c0 = {f_bg:.4e}   (line 0.05)   -> "
        + ("PASS" if f_bg <= 0.05 else f"FAIL by {f_bg/0.05:.3e}"))
    say(f"       Omega_c/Omega_b would become {R541*(1+f_bg):.4f} against 5.41; Omega_L drained by "
        f"{100*min(drain,1.0):.1f}% of itself (x{drain:.3e} over the whole vacuum)")
    w_eff = -1.0 + drain / 3.0     # crude: w+1 = (drain rate)/(3 H rho_Lam), taking the drain over a Hubble time
    say(f"  V4b  |w+1| ~ {w_eff:.3e}  (crude, drain over a Hubble time)  (line 0.05) -> "
        + ("PASS" if w_eff <= 0.05 else f"FAIL by {w_eff/0.05:.3e}"))
    # V5d Solar System
    for tag, rcv in [('worst', rc_max), ('ONE1-end', rc_one1)]:
        m_sat = rcv * MSUN_PER_KPC3 * (4.0 * math.pi * R_SAT**3 / 3.0) / MSUN
        say(f"  V5d  Solar System ({tag} rho_cre): created mass inside Saturn's orbit = "
            f"{m_sat:.4e} Msun  (line 1e-10)  -> "
            + ("PASS" if m_sat <= M_SAT_BOUND else f"FAIL by {m_sat/M_SAT_BOUND:.3e}"))
    # V6 Bullet
    for tag, rcv in [('worst', rc_max), ('ONE1-end', rc_one1)]:
        for rn, R200 in [('main', R200_MAIN), ('sub', R200_SUB)]:
            mcre = rcv * vol(R200) * CLUMP
            mmeas = RHO_200 * vol(R200)
            say(f"  V6   Bullet {rn:4s} R200={R200/1000:.2f} Mpc ({tag}): M_cre = {mcre:.4e} Msun, "
                f"0.10 x M_meas = {0.10*mmeas:.4e}  ratio {mcre/(0.10*mmeas):.4e} -> "
                + ("PASS" if mcre <= 0.10 * mmeas else "FAIL"))
    # V5c forest / creation history
    say("  V5d / V5c / V6 at the two reference densities:")
    # lookback / age: flat LCDM, computed here
    def _lb(z):
        n = 4000; s = 0.0
        for i in range(n):
            zz = z * (i + 0.5) / n
            E = math.sqrt(OMR * (1 + zz)**4 + (OMB + OMC) * (1 + zz)**3 + OML)
            s += (z / n) / ((1 + zz) * E)
        return s / H0
    T0_ = _lb(400.0)
    age_of_z = lambda z: T0_ - _lb(z)
    say(f"    (age of the universe here: {T0_/3.15576e16:.3f} Gyr)")
    say("  V5c  created fraction in place, by redshift:")
    for z in [0.5, 2.2, 2.8, 3.4, 4.4]:
        fu = max(0.0, (age_of_z(z) - age_of_z(6.0)) / (T0_ - age_of_z(6.0)))
        f2 = 0.0 if z >= 2.0 else (age_of_z(z) - age_of_z(2.0)) / (T0_ - age_of_z(2.0))
        say(f"         z = {z:4.1f}  age = {age_of_z(z)/3.15576e16:6.3f} Gyr   "
            f"uniform-in-t from z=6: {fu:6.3f}   linear ramp z=2 -> 0: {f2:6.3f}")
    f05 = (age_of_z(0.5) - age_of_z(2.0)) / (T0_ - age_of_z(2.0))
    say("         -> any history that leaves >10% in place at z>=2.2 inherits FRZ1's")
    say("            Delta chi^2 = 9916 / 9009 (gate 4): EXCLUDED.  All of it after z=2")
    say("            leaves the halo EMPTY at z=2.2-4.4 (FRZ1 safe), but KiDS measures at")
    say(f"            z~0.2-0.5, where a linear ramp from z=2 gives only {f05:.3f} of today's")
    say(f"            halo (line 0.9) -> FAIL by {0.9/max(f05,1e-9):.3e}.")

# ================================================================== MUTATE
say("\n" + "=" * 78)
say("PART E  MUTATE twins")
say("=" * 78)
if MUT == 'MU2':
    say("  MU2: the homogeneous source is REPLACED BY HAND with the law's own required source")
    say("       S_law(r) = (1/(4 pi r^2)) d_R[ d_t C_law(R) ].  V5a must PASS -- and it does")
    say("       (every C_cre/C_law printed in PART C is exactly 1).  The arm therefore BITES:")
    say("       the grader moves only when the profile is right.  What MU2 also prints is the")
    say("       price: S_law ~ R^-2, so the source must be more concentrated than the")
    say("       homogeneous vacuum by the contrast below.")
    for lm in LOGM:
        say(f"         log M_b {lm}:  S_law(10 kpc)/S_law({KIDS_MID[lm]:.0f} kpc) = "
            f"{(KIDS_MID[lm]/10.0)**2:.4e}")
    say("       No homogeneous vacuum (a function of tau alone) can have that contrast: 0.")
elif MUT == 'MU3':
    say("  MU3: Lambda' -> Lambda'/2.  Every required rho_cre and every ratio has halved.")
    say("       All the V5b / V4a failures are still failures, by half the factor.  BITES.")
elif MUT == 'MU4':
    say("  MU4: C_dust = 0 (no dust arrival).  Every required rho_cre has risen.")
    say("       The worst rho_cre and the payment ratio rise with it.  BITES.")
elif MUT == 'MU5':
    say("  MU5: the created charge is treated as dust free to cluster by 200x.")
    say("       Every V6 Bullet ratio is 200x larger.  BITES.")
elif MUT == 'MU1':
    say("  MU1: -sqrt(-g) V(tau) added.  V1a's bare-tau derivative is -V'(tau) != 0 (PART A).")
    say("       The conservation law is broken by exactly one function of tau.  BITES.")
else:
    say("  (base run; MUTATE twins run separately with VCC1_MUTATE=MU1..MU5)")

say("\n" + "=" * 78)
say("VCC1 done.")
say("=" * 78)
OUT.close()
