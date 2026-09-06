#!/usr/bin/env python3
"""
g03t -- the candidate's FLRW linear equations for the clock and the MOND scalar, derived from the action
===========================================================================================================
The action as the PPN pipeline actually uses it (f33 line 121; THE_ACTION's displayed formula omits the third term):

   L = sqrt(-g) [ R - 2 Lambda - c1 T1 - c2 T2 - c3 T3 + c4 T4 + 2(2-K_B) J^mu d_mu phi - (2-K_B) J(Y) - K(Q) ] + L_m

with n_mu = -d_mu tau / N (the clock's unit normal), T1 = (grad n)^2, T2 = (div n)^2, T3 = grad_mu n_nu grad^nu n^mu,
T4 = J.J, J^mu = n^nu grad_nu n^mu (the clock's 4-acceleration), Q = n.d phi, Y = q^{mu nu} d_mu phi d_nu phi,
K(Q) = K2 (Q - Q0)^2, c1 = -c3 = K_B, c14 = c1 + c4, and J(Y) with J'(0) = J_Y0 (0 in the deep-MOND regime J ~ Y^{3/2}).

Perturbed flat FLRW in Newtonian gauge, scalar sector, perturbations varying along x:
   ds^2 = -(1 + 2 e Psi) dt^2 + a^2 (1 - 2 e Phi) dx^2,   tau = t + e T,   phi = phibar(t) + e P,   phibar' = Qbar(t).
The clock+scalar sector of the Lagrangian is expanded to second order in e with sympy (no truncation shortcuts: every
tensor is built from the metric), the quadratic Lagrangian L2 is varied with respect to P, T and Psi, and:

  D1 [background]   the e^0 Lagrangian gives the clock's contribution to the Friedmann constraint: rho_clock = -3 c2 H^2 x (norm),
                    i.e. G_cos/G = 1/(1 + 3 c2/2) at c13 = 0 -- must agree with g03e;
  D2 [structure]    the clock's acceleration is J_i = d_i (Psi - T') at linear order; the scalar's kinetic variable is
                    dQ = P' - Qbar Psi (T drops out at linear order);
  D3 [scalar eq.]   the P equation is  d_t[a^3 2K2 (P' - Qbar Psi)] = 2(2-K_B) a d_x^2 (Psi - T') - 2(2-K_B) J_Y0 a d_x^2 P
                    up to signs fixed by the convention -- printed exactly; in the static limit with T = 0 it is the AeST law
                    J_Y d_x^2 phi = d_x^2 Psi (the pipeline's static law), which fixes the normalisation;
  D4 [clock eq.]    the T equation, exactly, and its sub-horizon (k >> aH) reduction: which combination of Psi, Phi, P' the
                    clock's T' tracks;
  D5 [THE ANSWER]   substituting the sub-horizon clock into D3: the effective source of the scalar's linear equation,
                    S_eff = coefficient of d_x^2 Psi, relative to the static coupling 2(2-K_B).  S_eff -> 1 means the
                    source survives (the (c_* k t)^2 build-up of g03s is the theory's), S_eff -> 0 means the clock falls
                    freely (J -> 0) and the linear scalar is metric-coupled only (LambdaCDM growth);
  D6 [dust]         the sector's energy density from the lapse variation: delta rho at linear order, its relation to dQ.
  D7 [pincer]       the |K_2| that keeps the linear growth within 10% of LambdaCDM at k = 0.2/Mpc versus the dark-sector window.
Checks that can fail: D1 against g03e's G_cos; D3's static limit against the pipeline's static law; the linear-order absence
of T in Q; D5 with its closed formula; D7.  Sub-horizon means: the c_2 k^4 term of the clock equation dominates its O(k^2) terms.
"""
import sympy as sp, time, sys, json
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
t, x, y, z = sp.symbols('t x y z', real=True); e = sp.symbols('epsilon', real=True)
KB, c2, c14, K2, Q0, JY0, k = sp.symbols('K_B c_2 c_14 K_2 Q_0 J_Y0 k', real=True)
a = sp.Function('a', positive=True)(t); Psi = sp.Function('Psi')(t, x); Phi = sp.Function('Phi')(t, x); Tf = sp.Function('T')(t, x); P = sp.Function('P')(t, x); phib = sp.Function('phibar')(t)
X = [t, x, y, z]
g = sp.diag(-(1 + 2*e*Psi), a**2*(1 - 2*e*Phi), a**2*(1 - 2*e*Phi), a**2*(1 - 2*e*Phi))
def ser(expr, n=3):
    """expand in epsilon to order e^(n-1) by explicit Taylor differentiation (sympy's series cannot handle mixed Derivative objects)"""
    out = sp.expand(sum(sp.diff(expr, e, j).subs(e, 0)*e**j/sp.factorial(j) for j in range(n)))
    return sp.expand(out.subs(sp.sqrt(a**6), a**3).subs(sp.sqrt(a**2), a))
FIELDS = {}
def symb(expr):
    """replace every derivative of the perturbation fields (and the fields) by plain symbols so that .coeff works"""
    global FIELDS
    if not FIELDS:
        for f, nm in ((Psi, 'Psi'), (Phi, 'Phi'), (Tf, 'T'), (P, 'P')):
            for nt in range(0, 3):
                for nx in range(0, 5):
                    if nt == 0 and nx == 0: FIELDS[f] = sp.Symbol(nm); continue
                    d = f
                    if nt: d = sp.Derivative(d, (t, nt))
                    if nx: d = sp.Derivative(d, (x, nx))
                    FIELDS[d] = sp.Symbol(nm + '_' + 't'*nt + 'x'*nx)
        FIELDS[sp.Derivative(phib, t)] = sp.Symbol('Qbar'); FIELDS[sp.Derivative(phib, (t, 2))] = sp.Symbol('Qbar_t'); FIELDS[phib] = sp.Symbol('phibar')
    out = expr
    for d in sorted([k for k in FIELDS if isinstance(k, sp.Derivative)], key=lambda d: -sum(c for _, c in d.variable_count)):
        out = out.subs(d, FIELDS[d])
    for f in (Psi, Phi, Tf, P, phib): out = out.subs(f, FIELDS[f])
    return sp.expand(out)
def S(nm): return sp.Symbol(nm)
gi = sp.Matrix(4, 4, lambda i, j: 0)
for i in range(4): gi[i, i] = ser(1/g[i, i])
sqrtg = ser(sp.sqrt(-g.det()))
print("  metric, inverse, sqrt(-g) expanded", flush=True)
Gam = [[[sp.expand(ser(sp.Rational(1, 2)*sum(gi[r, s]*(sp.diff(g[s, n], X[m]) + sp.diff(g[s, m], X[n]) - sp.diff(g[m, n], X[s])) for s in range(4)))) for n in range(4)] for m in range(4)] for r in range(4)]
print(f"  Christoffels ({time.time()-T0:.0f}s)", flush=True)
tau = t + e*Tf; dtau = [sp.diff(tau, v) for v in X]
N2 = -sum(gi[m, n]*dtau[m]*dtau[n] for m in range(4) for n in range(4)); Ninv = ser(1/sp.sqrt(sp.expand(N2)))
n_dn = [sp.expand(ser(-dtau[m]*Ninv)) for m in range(4)]                                        # n_mu
n_up = [sp.expand(ser(sum(gi[m, n]*n_dn[n] for n in range(4)))) for m in range(4)]                # n^mu
def cov_dn(v_dn, nu, mu):                                                                          # grad_nu v_mu
    return sp.diff(v_dn[mu], X[nu]) - sum(Gam[l][nu][mu]*v_dn[l] for l in range(4))
Dn = [[sp.expand(ser(cov_dn(n_dn, nu, mu))) for mu in range(4)] for nu in range(4)]               # grad_nu n_mu
Dn_up = [[sp.expand(ser(sum(gi[mu, r]*Dn[nu][r] for r in range(4)))) for mu in range(4)] for nu in range(4)]   # grad_nu n^mu
T1 = ser(sum(gi[nu, al]*Dn[nu][mu]*Dn_up[al][mu] for nu in range(4) for al in range(4) for mu in range(4)))
divn = ser(sum(Dn_up[nu][nu] for nu in range(4))); T2 = ser(divn**2)
T3 = ser(sum(Dn_up[nu][mu]*Dn_up[mu][nu] for nu in range(4) for mu in range(4)))
J_dn = [sp.expand(ser(sum(n_up[nu]*Dn[nu][mu] for nu in range(4)))) for mu in range(4)]           # J_mu = n^nu grad_nu n_mu
J_up = [sp.expand(ser(sum(gi[mu, r]*J_dn[r] for r in range(4)))) for mu in range(4)]
T4 = ser(sum(J_dn[mu]*J_up[mu] for mu in range(4)))
print(f"  aether operators ({time.time()-T0:.0f}s)", flush=True)
phi = phib + e*P; dphi = [sp.diff(phi, v) for v in X]
Q = ser(sum(n_up[m]*dphi[m] for m in range(4)))
Y = ser(sum((gi[m, n] + n_up[m]*n_up[n])*dphi[m]*dphi[n] for m in range(4) for n in range(4)))
Jdphi = ser(sum(J_up[m]*dphi[m] for m in range(4)))
c1 = KB; c3 = -KB; c4 = c14 - KB
Lden = sqrtg*(-c1*T1 - c2*T2 - c3*T3 + c4*T4 + 2*(2 - KB)*Jdphi - (2 - KB)*JY0*Y - K2*(Q - Q0)**2)
Lden = sp.expand(ser(sp.expand(Lden)))
L0 = Lden.coeff(e, 0); L1 = Lden.coeff(e, 1); L2 = Lden.coeff(e, 2)
print(f"  Lagrangian expanded to second order ({time.time()-T0:.0f}s)", flush=True)
H = sp.diff(a, t)/a
# ---- D2: structure ----
Ji_lin = sp.simplify(symb(J_dn[1]).coeff(e, 1)); Q_lin = sp.simplify(symb(Q).coeff(e, 1)); Q_bg = sp.simplify(symb(Q).coeff(e, 0))
print(f"    J_x (linear) = {Ji_lin}"); print(f"    Q = {Q_bg} + e ({Q_lin})")
check("D2 the clock's linear acceleration is d_x(Psi - T') and the scalar's linear kinetic variable is P' - Qbar Psi (T absent)",
      sp.simplify(Ji_lin - (S('Psi_x') - S('T_tx'))) == 0 and sp.simplify(Q_lin - (S('P_t') - S('Qbar')*S('Psi'))) == 0, "")
# ---- D1: background: the clock sector's contribution to the Friedmann constraint from the lapse variation of L0 (Psi is the lapse perturbation: rho = -(1/sqrtg) dL/dPsi at e^0 -> use L1's Psi coefficient at zeroth order in fields) ----
# The e^1 Lagrangian's Psi-coefficient (with all perturbations except Psi set to zero) gives -sqrt(-g) rho_sector; the c2 (div n)^2 = 9 c2 H^2 term at the background.
L1s = symb(L1); L1_psi = sp.simplify(L1s.coeff(S('Psi')))
rho_clock_expr = sp.simplify(-L1_psi/a**3)
print(f"    L1 coefficient of Psi / (-a^3) = {rho_clock_expr}")
# Friedmann with the pipeline's units: the GR part gives sqrt(-g) R -> lapse variation 6 H^2 a^3 (up to the common 16 pi G): 6 H^2 = 16 pi G rho_m + (sector) => H^2 (6 - sector/H^2) = 16 pi G rho_m => G_cos/G = 6/(6 - sector/H^2)
sector_over_H2 = sp.simplify(rho_clock_expr.subs(S('Qbar'), Q0)/H**2)                 # at the condensate minimum Qbar = Q0 the K sector vanishes at the background
Gcos_ratio = sp.simplify(6/(6 - sector_over_H2))
print(f"    clock-sector background density / H^2 = {sector_over_H2};  G_cos/G = {Gcos_ratio}")
check("D1 [background] G_cos/G = 1/(1 + 3 c_2/2) at c13 = 0 (g03e)", sp.simplify(Gcos_ratio - 1/(1 + 3*c2/2)) == 0, f"derived {Gcos_ratio}")
# ---- Euler-Lagrange equations from L2 ----
from sympy.calculus.euler import euler_equations
def EL(L, f):
    """Euler-Lagrange expression for field f from Lagrangian density L (handles up to second derivatives)"""
    eqs = euler_equations(L, [f], [t, x]); return sp.expand(eqs[0].lhs - eqs[0].rhs)
EP = EL(L2, P); ET = EL(L2, Tf); EPsi = EL(L2, Psi)
print(f"  Euler-Lagrange equations derived ({time.time()-T0:.0f}s)", flush=True)
# ---- D3: the scalar equation ----
EP_full = symb(EP); ETs = symb(ET); EPsis = symb(EPsi)
print("    scalar (P) equation, background Qbar general:")
for term in ['P_tt', 'P_t', 'Psi_t', 'Psi', 'Psi_xx', 'T_txx', 'P_xx', 'Phi_t', 'T_xx', 'T_ttxx']:
    cf = sp.simplify(EP_full.coeff(S(term)))
    if cf != 0: print(f"      coeff of {term}: {sp.factor(cf)}")
# static limit: a = 1, H = 0, time-independent, T = 0: keep d_x^2 terms
static = sp.expand(EP_full.subs(a, 1).subs({S('T_txx'): 0, S('T_t'): 0, S('T_ttxx'): 0}))
cPsi = sp.simplify(static.coeff(S('Psi_xx'))); cP = sp.simplify(static.coeff(S('P_xx')))
print(f"    static limit: coefficient of d_x^2 Psi = {cPsi}, of d_x^2 P = {cP}  =>  J_Y0 d_x^2 P = -(coeff ratio) d_x^2 Psi")
check("D3 [static law] the static limit of the scalar equation is J_Y d_x^2 P = d_x^2 Psi (the AeST/pipeline static law, unit coefficient)", sp.simplify(cPsi/cP + 1/JY0) == 0 or sp.simplify(cPsi/cP - 1/JY0) == 0, f"ratio = {sp.simplify(cPsi/cP)}")
# ---- D4: the clock equation, sub-horizon reduction ----
# Fourier: fields ~ f(t) exp(i k x): replace d_x -> i k; keep the equation exact in time.
def fourier(expr):
    """fields ~ f(t) exp(i k x) on the symbolized expression"""
    out = expr
    for nm, F in (('Psi', 'Psik'), ('Phi', 'Phik'), ('T', 'Tk'), ('P', 'Pk')):
        Fk = sp.Function(F)(t)
        for nt in range(0, 3):
            for nx in range(0, 5):
                sym = S(nm + ('_' + 't'*nt + 'x'*nx if (nt or nx) else ''))
                val = (sp.I*k)**nx*(sp.Derivative(Fk, (t, nt)) if nt else Fk)
                out = out.subs(sym, val)
    return sp.expand(out)
ETk = fourier(ETs); EPk = fourier(EP_full)
Tk, Pk, Psik, Phik = [sp.Function(n)(t) for n in ('Tk', 'Pk', 'Psik', 'Phik')]
print("    clock (T) equation in Fourier space -- coefficients:")
KS = {}
for nm, F in (('Tk', Tk), ('Pk', Pk), ('Psik', Psik), ('Phik', Phik)):
    for nt in range(0, 3): KS[sp.Derivative(F, (t, nt)) if nt else F] = S(nm + '_' + 't'*nt if nt else nm)
def ksym(expr):
    out = expr
    for d in sorted([kk for kk in KS if isinstance(kk, sp.Derivative)], key=lambda d: -sum(c for _, c in d.variable_count)): out = out.subs(d, KS[d])
    for f in (Tk, Pk, Psik, Phik): out = out.subs(f, KS[f])
    return sp.expand(out)
ETks = ksym(ETk); EPks = ksym(EPk)
for term in ['Tk_tt', 'Tk_t', 'Tk', 'Psik_t', 'Psik', 'Phik_t', 'Phik', 'Pk_t', 'Pk', 'Pk_tt']:
    cf = sp.simplify(ETks.coeff(S(term)))
    if cf != 0: print(f"      {term}: {sp.factor(cf)}")
# sub-horizon: leading power of k in each coefficient
def leading_k(expr):
    expr = sp.expand(expr); pw = sp.Poly(expr, k); deg = pw.degree(); return sp.simplify(pw.coeff_monomial(k**deg))*k**deg, deg
print("    sub-horizon (leading k) form of the clock equation:")
def lk(term):
    cf = ETks.coeff(S(term)); return leading_k(cf) if cf != 0 else (0, -1)
cT2, dT2 = lk('Tk_tt'); cT1, dT1 = lk('Tk_t'); cT0, dT0 = lk('Tk'); cPs1, dPs1 = lk('Psik_t'); cPs0, dPs0 = lk('Psik'); cP1, dP1 = lk('Pk_t'); cP2, dP2 = lk('Pk_tt')
print(f"      T'': {cT2};  T': {cT1};  T: {cT0};  Psi': {cPs1};  Psi: {cPs0};  P': {cP1};  P'': {cP2}")
# ---- D5: the effective source ----
# Sub-horizon hierarchy: the clock equation's T coefficient carries c2 k^4 (the (div n)^2 term penalises the foliation's expansion), every other
# term is O(k^2): the clock's time shift is T = O(1/k^2) x [scalar and metric terms], so T' is O(1/k^2) relative to Psi and the clock's
# acceleration Psi - T' -> Psi.  Solve the exact Fourier clock equation for Tk with the O(k^2) T', T'' terms dropped (they are O(1/k^2)
# smaller than the k^4 term after the solve), differentiate, and insert into the scalar equation; the scalar's own P'' is eliminated with
# its leading-order equation so that the K2 back-reaction on the source is kept.
Tsol = sp.solve(sp.Eq(ETks.subs({S('Tk_tt'): 0, S('Tk_t'): 0}), 0), S('Tk'))[0]
Tsol_t = sp.expand(sp.diff(Tsol.subs({S('Psik'): Psik, S('Pk'): Pk, S('Pk_t'): sp.diff(Pk, t), S('Phik'): Phik, S('Psik_t'): sp.diff(Psik, t), S('Phik_t'): sp.diff(Phik, t)}), t))
Tsol_t = ksym(Tsol_t)
# leading-order scalar equation for Pk_tt (source with T' -> 0 at this order) to eliminate Pk_tt from T'
EP0 = EPks.subs({S('Tk_t'): 0, S('Tk_ttx'): 0}); Ptt_sol = sp.solve(sp.Eq(EP0, 0), S('Pk_tt'))[0]
Tsol_t = sp.expand(Tsol_t.subs(S('Pk_tt'), Ptt_sol))
src = sp.expand(S('Psik') - Tsol_t)                                                                 # the clock's acceleration potential entering the scalar's source
S_eff = sp.simplify(sp.limit(sp.simplify(src.coeff(S('Psik'))), k, sp.oo))
S_eff_full = sp.simplify(src.coeff(S('Psik')))
print(f"    clock time shift (exact solve, leading order): Tk = {sp.simplify(Tsol)}")
print(f"    Psi - T' : coefficient of Psi_k = {S_eff_full}")
print(f"    k -> infinity: S_eff = {S_eff}")
corner = {c2: sp.Rational(1, 20), KB: sp.Rational(1, 5), K2: -250000, c14: sp.Rational(1, 100000)}
print(f"    at the corner (c2 = 0.05, K_B = 0.2, K_2 = -2.5e5): S_eff = {float(S_eff.subs(corner)):.6f}")
check("D5 [THE ANSWER] the linear scalar source survives sub-horizon: S_eff -> 1 - (2-K_B)^2/(c_2 |K_2|) (the clock is rigid through its c_2 k^4 term), within 1% of unity at the corner -- the g03s build-up is the theory's", sp.simplify(S_eff - (1 + (2 - KB)**2/(c2*K2))) == 0 and abs(float(S_eff.subs(corner)) - 1) < 0.01, f"S_eff = {S_eff}")
c2_min = sp.simplify((2 - KB)**2/(-K2)); print(f"    rigidity condition: c_2 > (2-K_B)^2/|K_2| = {float(c2_min.subs(corner)):.2e} at the corner (below it the clock-scalar mode with c_s^2 = (2-K_B)^2/(c_14 |K_2|) = {float(((2-KB)**2/(c14*(-K2))).subs(corner)):.2f} c^2 takes over; a separate branch)")
# ---- D7: the pincer ----
c_ = 2.998e8; t0 = 13.8e9*3.156e7; kk = 0.2/3.0857e22
K2_growth = 0.42*c_**2*9*kk**2*t0**2                                                                # |K_2| for which 0.9 (c_* k t_0)^2 <= 0.1 at k = 0.2/Mpc (g03s (i))
print(f"    D7: linear growth within 10% of LambdaCDM at k = 0.2/Mpc needs |K_2| >= 3.8 c^2 k^2 t_0^2 = {K2_growth:.2e}; the dark-sector window (g03r/g03s) is |K_2| <= 2e5-5e5")
check("D7 [pincer] with the source surviving (D5), the |K_2| that keeps the linear growth within 10% of LambdaCDM at k = 0.2/Mpc exceeds the KiDS/cluster window's upper edge (5e5) by more than a factor 3", K2_growth/5e5 > 3, f"ratio {K2_growth/5e5:.1f}")
# ---- D6: the sector's linear energy density from the lapse variation ----
print("    lapse (Psi) equation from the sector -- coefficients (delta rho_sector = -(1/a^3) dL2/dPsi):")
for term in ['P_t', 'Psi', 'T_xx', 'T_txx', 'Phi_t', 'Phi_xx', 'Psi_xx', 'T_t', 'P_tt', 'Phi']:
    cf = sp.simplify(EPsis.coeff(S(term)))
    if cf != 0: print(f"      {term}: {sp.factor(cf)}")
print(f"\n  notes: the GR + matter parts are not expanded here (standard); c13 = 0 makes the Maxwell combination c1(T1 - T3) = c1 J^2 for a hypersurface-orthogonal n, so the clock sector is the khronometric theory with alpha = c_14, lambda = c_2, beta = 0; the third action term 2(2-K_B) J.dphi is the AeST coupling that THE_ACTION's displayed formula omitted.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
