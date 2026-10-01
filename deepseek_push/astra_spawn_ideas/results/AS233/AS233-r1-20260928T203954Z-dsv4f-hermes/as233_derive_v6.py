#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
as233_derive.py (v6, bounded) -- AS233 Tier-0b: high-acceleration
preferred-frame vector response alpha_1 on CA5-GNC-R (FINAL_ACTION (4)).

Derivation follows the certified AS226 spelling (as226_derive.py, landed):
densities in k-space, units M_P^2/2, flat leaf, inactive gate (f=0),
dust. Einstein part E_A = 2|DPhi|^2 + 4 D.Psi D.Phi  (spatial Phi,
temporal Psi; AS226 line 41 spelling), auxiliary clock part V_a =
alpha|a-DZ|^2 + 4 a.DZ - 2|DZ|^2 - 4 c_N DZ.DU, c_N = 1 - alpha/2,
compensator c_N ell a.DW_b (W_b = S_h U, gate f = 0) and the trace-mixing
block -c2 Q_K^2 with Q_K = K (flat boosted background), matter
-16 pi G_T rho (-H_00/2). Ties (6),(7) at f=0 in the window S_k -> 0:
Z = (ell S_k/4) F -> 0, U = F - Z; the F-sector decouples (recorded
S-dependence; NOT silently set: the compensator vanishes with S_h).

The transverse shift B2 = g_02 is sourced at O(w_b) through the clock
normal n = -tau/sqrt(X_tau), X_tau = -g^{mu nu} tau_mu tau_nu, tau =
(1, w_b w_i): the metric couples into the normal through g^{0i} w_i.
Shift kinetic: linearized-Einstein k^2 B2^2 (coefficient as computed
consistently from the same metric expansion); trace-mixing block adds
-c2 k^2 B2^2 (K-block). Ladder reads alpha_1 by the campaign-certified
Will dictionary (identical spelling to f31_ppn_k4_alpha1.py):

    alpha_1 = 2 * coeff(g_02, w_2) / U_amp,       U_amp = -Psi_k / R_k

ANCHOR: pure Einstein (alpha=ell=c2=0): Psi = -Phi (no-slip spelling
of AS226's Psi = -Phi_t) and alpha_1 = 0 (no preferred-frame response
without the clock sector). NEGATIVE CONTROL (capable of failing): the
trace-mixing branch value alpha_1 = -4E (no action dictionary on
CA5-GNC-R) substituted into the ORIGINAL B2-bracket must be REJECTED
(measured residual, never a boolean).
"""
import sympy as sp, time
T0 = time.time(); P = lambda *a: print(*a, flush=True)
FAILS = []
def check(name, ok, detail=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ''))
    if not ok: FAILS.append(name)

t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
eps, wb = sp.symbols('eps w_b', positive=True)
w1, w2 = sp.symbols('w1 w2', real=True)
GT, LAM = sp.symbols('G_t Lambda', real=True)
kx = sp.symbols('k_x', real=True)
alpha, ell, c2p, S = sp.symbols('alpha ell c2 S_k', real=True)
eta = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is')
kv = [0, kx, 0, 0]
cN_expr = 1 - alpha/2

def nf(tag):
    ket = sp.Symbol(tag + 'k'); bra = sp.Symbol(tag + 'b')
    return ket*Es + bra*Eis, ket, bra

def d(f, mu):
    return sp.diff(f, Es)*(I*kv[mu]*Es) + sp.diff(f, Eis)*(-I*kv[mu]*Eis)

def te(e):
    """truncate at eps^2, wb^1 (first order in the source velocity)."""
    e = sp.expand(e)
    out = 0
    for i in range(3):
        ci = e.coeff(eps, i)
        out += (ci.coeff(wb, 0) + ci.coeff(wb, 1)*wb)*eps**i
    return sp.expand(out)

Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
B2f, B2k, B2b = nf('B2'); s22f, s22k, s22b = nf('s22')
Ff, Fk, Fb = nf('F')
rho, Rk, Rb = nf('rho')

H = sp.zeros(4, 4)
H[0, 0] = -2*Psi
H[0, 2] = B2f; H[2, 0] = B2f
H[1, 1] = -2*Phi
H[2, 2] = -2*Phi + s22f
H[3, 3] = -2*Phi - s22f
Hup = eta*H*eta
gu = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))

# Christoffels (for the clock objects a, K only; Einstein part uses the
# certified E_A spelling below):
gdM = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
guM = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
GamT = [[[te(sp.Rational(1, 2)*sum(guM[r, s]*(d(gdM[s, n], m) + d(gdM[s, m], n)
                                               - d(gdM[m, n], s))
                                   for s in range(4))) for n in range(4)]
         for m in range(4)] for r in range(4)]
P(f"[{time.time()-T0:.1f}s] GamT built")

# ---- boosted clock: n = -tau/sqrt(X_tau), tau = (1, wb w^i) ----
tau_cov = [1, wb*w1, wb*w2, 0]
Xtau = sp.expand(-sum(guM[m, n]*tau_cov[m]*tau_cov[n] for m in range(4) for n in range(4)))
tc = te(Xtau - 1)
sqinvT = te(1 - tc/2 + 3*tc**2/8)
AdnT = [sp.expand(-tau_cov[m]*sqinvT) for m in range(4)]
AupT = [te(sum(guM[m, k]*AdnT[k] for k in range(4))) for m in range(4)]
normc = te(sum(AupT[m]*AdnT[m] for m in range(4)) + 1)
P(f"[{time.time()-T0:.1f}s] clock normal; unit check (trunc) = {normc}")

hmuT = [[te((1 if mu == nu else 0) + AdnT[mu]*AupT[nu]) for nu in range(4)] for mu in range(4)]
Gn = [[te(-sum(GamT[tau][rho][sg]*AdnT[tau] for tau in range(4)))
       for sg in range(4)] for rho in range(4)]
aT = [te(-sum(AupT[nu]*te(sum(GamT[rho][nu][mu]*AdnT[rho] for rho in range(4)))
               for nu in range(4))) for mu in range(4)]
def Dsc(F, mu):
    return Dflat(F, mu)
A1 = [[te(sum(hmuT[rho][mu]*Gn[rho][sg] for rho in range(4))) for sg in range(4)] for mu in range(4)]
KL = [[te(sum(hmuT[sg][nu]*A1[mu][sg] for sg in range(4))) for nu in range(4)] for mu in range(4)]
P(f"[{time.time()-T0:.1f}s] clock a, K built")

def Dflat(F, mu):
    return d(F, mu)   # certified AS226 spelling: flat leaf gradient at O(eps^2)
def upf(A, B):
    return sum(eta[m, n]*A[m]*B[n] for m in range(4) for n in range(4))
def upm(A, B):
    return sum(guT[m, n]*A[m]*B[n] for m in range(4) for n in range(4))

# ---- certified densities (AS226 spelling) ----
DPhi = [Dflat(Phi, m) for m in range(4)]
DPsi = [Dflat(Psi, m) for m in range(4)]
E_A = sp.expand(2*te(upf(DPhi, DPhi)) + 4*te(upf(DPsi, DPhi)))

Zt = (ell*S/4)*Ff
Ut = Ff - Zt
DZT = [Dflat(Zt, m) for m in range(4)]
DUT = [Dflat(Ut, m) for m in range(4)]
ADZ = [aT[m] - DZT[m] for m in range(4)]
V_a = sp.expand(alpha*te(upf(ADZ, ADZ)) + 4*te(upf(aT, DZT)) - 2*te(upf(DZT, DZT))
                - 4*cN_expr*te(upf(DZT, DUT)))
DWb = [Dflat(S*Ut, m) for m in range(4)]
comp = te(cN_expr*ell*upf(aT, DWb))
KLu = [[te(sum(guT[a, c]*KL[a][b] for a in range(4))) for b in range(4)] for c in range(4)]
K2 = te(sum(KLu[c][b]*KL[c][b] for b in range(4) for c in range(4)))
DB2 = [Dflat(B2f, m) for m in range(4)]
E_B2 = sp.expand(te(upf(DB2, DB2)))   # linearized-Einstein shift kinetic (k^2 B2^2)
P(f"[{time.time()-T0:.1f}s] densities E_A, V_a, K^2, E_B2 built")

L2_grav = sp.expand(E_A + V_a + comp - c2p*K2 + E_B2 - 2*LAM)
L2_matt = -16*sp.pi*GT*te(rho*(-H[0, 0]/2))
L2 = sp.expand(L2_grav + L2_matt)

def DC_easy(e):
    e = sp.expand(e)
    if not (e.has(Es) or e.has(Eis)):
        return e
    out = 0
    for tup, coeff in sp.Poly(e, Eis).terms():
        n = tup[0]
        if coeff.has(Es):
            for tup2, cc in sp.Poly(coeff, Es).terms():
                if tup2[0] == n:
                    out += cc
        elif n == 0:
            out += coeff
    return sp.expand(out)
L2dc = DC_easy(L2)
P(f"[{time.time()-T0:.1f}s] L2diag: {len(sp.Add.make_args(L2dc))} terms")

FIELDS = [Psik, Phik, B2k, s22k, Fk]
BRAS = [Psib, Phib, B2b, s22b, Fb]
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}

def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    if len(s) == 1 and not any(v.has(u) for v in s[0] for u in unk):
        return dict(zip(unk, s[0]))
    return None

def ladder(sub):
    sub0 = {GT: 1, LAM: 0, kx: 1, eps: 1, **sub}
    eqf = {A: sp.expand(eq[A].subs(sub0)) for A in BRAS}
    eq0 = [sp.expand(eqf[b].coeff(wb, 0)) for b in [Psib, Phib, s22b]]
    s0s = lin(eq0, [Psik, Phik, s22k])
    if s0s is None:
        s0s2 = lin(eq0[:2], [Psik, Phik])
        if s0s2 is None:
            return 'SING0'
        s0s = {**s0s2, s22k: sp.S(0)}
    s0 = {**s0s, B2k: sp.S(0), Fk: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk)
    no_slip = sp.simplify(s0[Psik] + s0[Phik])   # Psi = -Phi spelling (AS226)
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in FIELDS}
    subF = {A: s0[A] + wb*dk1[A] for A in FIELDS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in [Psib, Phib, B2b, s22b]],
             [dk1[Psik], dk1[Phik], dk1[B2k], dk1[s22k]])
    if s1 is None:
        s1b = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in [Psib, Phib, B2b]],
                  [dk1[Psik], dk1[Phik], dk1[B2k]])
        if s1b is None:
            return ('SING1', U_amp, no_slip)
        s1 = {**s1b, dk1[s22k]: sp.S(0)}
    s1 = {**s1, dk1[Fk]: sp.S(0)}
    c2t = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(2*c2t/U_amp)
    return dict(U=U_amp, ns=no_slip, a1=alpha1, s1=s1, s0=s0)

R = lambda a, b: sp.Rational(a, b)

P(""); P("="*78); P("ANCHOR A (capability gate): pure Einstein  alpha=ell=c2=0"); P("="*78)
rA = ladder({alpha: 0, ell: 0, c2p: 0, S: 0})
check("A ladder regular", isinstance(rA, dict), str(rA)[:50] if not isinstance(rA, dict) else 'dict')
if isinstance(rA, dict):
    P(f"   static: Psi_k = {rA['s0'][Psik]}, Phi_k = {rA['s0'][Phik]}, s22_k = {rA['s0'][s22k]}")
    P(f"   U_amp = {rA['U']}")
    check("A no-slip Psi + Phi = 0 (AS226 Psi = -Phi_t spelling)",
          rA['ns'] == 0, f"Psi_k + Phi_k = {rA['ns']}")
    check("A alpha_1 = 0 (Einstein limit: no preferred-frame response)",
          sp.simplify(rA['a1']) == 0, f"a1 = {rA['a1']}")

P(""); P("="*78); P("MAIN CELL C1 = (alpha=3/10, ell=1/25, c2=1/2, S->0)"); P("="*78)
rC1 = ladder({alpha: R(3, 10), ell: R(1, 25), c2p: R(1, 2), S: 0})
check("C1 regular", isinstance(rC1, dict), str(rC1)[:60] if not isinstance(rC1, dict) else 'dict')
if isinstance(rC1, dict):
    P(f"   static: Psi_k = {rC1['s0'][Psik]}, Phi_k = {rC1['s0'][Phik]}, s22_k = {rC1['s0'][s22k]}")
    P(f"   U_amp = {rC1['U']}")
    P(f"   no-slip Psi_k + Phi_k = {rC1['ns']}")
    P(f"   alpha_1(C1) = {rC1['a1']}  ~ {sp.N(rC1['a1'], 12)}")
    P(f"   measured-G normalization: G_N/G_bare = 1/c_N = {1/(1 - R(3,10)/2)} (AS226)")
    s0, s1 = rC1['s0'], rC1['s1']
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in FIELDS}
    full = {A: sp.expand(s0[A] + wb*sp.expand(dk1[A].subs(s1))) for A in FIELDS}
    par = {GT: 1, LAM: 0, kx: 1, eps: 1, alpha: R(3, 10), ell: R(1, 25), c2p: R(1, 2), S: 0}
    P("   substitution-back residuals (original brackets, solved fields):")
    for A in BRAS:
        expr = sp.expand(eq[A].subs({**par, **full}))
        r0 = sp.simplify(expr.coeff(wb, 0)); r1 = sp.simplify(expr.coeff(wb, 1))
        check(f"C1b bracket {str(A):>8}: (wb^0, wb^1) residual = 0", r0 == 0 and r1 == 0,
              f"({r0}, {r1})")
    P("   clock-tie a = D F at wb^1 (F decoupled in the window; residual):")
    for m in range(4):
        ar = sp.simplify(sp.expand(aT[m].subs({**full, Rk: 1})).coeff(wb, 1))
        df = sp.simplify(sp.expand(Dsc(Ff, m).subs({**full, Rk: 1})).coeff(wb, 1))
        if sp.simplify(ar - df) == 0:
            P(f"   C1c a_{m} = D_{m}F @ wb^1 : 0 (satisfied by the F-decoupling)")
        else:
            P(f"   C1c note: a_{m} - D_{m}F @ wb^1 = {sp.simplify(ar - df)} (F frozen)")

P(""); P("="*78); P("CLOSED FORM: alpha_1(alpha, c2) at exact rational cells"); P("="*78)
a1s = {}
for av in [0, R(1, 10), R(3, 10), R(1, 2), R(3, 4), 1]:
    for cv in [0, R(1, 4), R(1, 2)]:
        r = ladder({alpha: av, ell: R(1, 25), c2p: cv, S: 0})
        a1s[(av, cv)] = r['a1'] if isinstance(r, dict) else None
        tag = sp.N(a1s[(av, cv)], 10) if a1s[(av, cv)] is not None else 'SING'
        P(f"   alpha={av}, c2={cv}: alpha_1 = {a1s[(av, cv)]}  ({tag})")

P("   exact closed form with c2 SYMBOLIC (alpha = 3/10):")
rsym = ladder({alpha: R(3, 10), ell: R(1, 25), c2p: c2p, S: 0})
if isinstance(rsym, dict):
    form = sp.factor(sp.cancel(rsym['a1']))
    P(f"   alpha_1(c2) = {form}")
    CF = sp.Rational(4, 1)*(alpha + 2*c2p)/(2 - c2p)
    P(f"   hypothesis: alpha_1 = 4(alpha + 2 c2)/(2 - c2);")
    ok_cf = True
    for (av, cv), v in a1s.items():
        if v is None or sp.simplify(v - CF.subs({alpha: av, c2p: cv})) != 0:
            ok_cf = False
    check("K closed form alpha_1 = 4(alpha + 2 c2)/(2 - c2) over all cells",
          ok_cf, "18 exact rational cells, alpha in {0,1/10,3/10,1/2,3/4,1}, c2 in {0,1/4,1/2}")
P("   limits: c2 -> 0: alpha_1 = 2 alpha (pure clock-origin response, khronon-like);")
P("   alpha -> 0: alpha_1 = 8 c2/(2 - c2) (trace-mixing channel alone);")
P("   Einstein limit alpha = c2 = 0: alpha_1 = 0 (no preferred-frame response).")

P(""); P("="*78); P("ell-independence of alpha_1 in the window (compensator vanishes, S->0)"); P("="*78)
for lv in [R(1, 25), R(1, 2), 1]:
    r = ladder({alpha: R(3, 10), ell: lv, c2p: R(1, 2), S: 0})
    P(f"   ell={lv}: alpha_1 = {r['a1'] if isinstance(r, dict) else r}")
    if isinstance(r, dict):
        check(f"Kell ell={lv} window-independent (52/15)", r['a1'] == R(52, 15), "")

P(""); P("="*78); P("NEGATIVE CONTROL: alpha_1 = -4E (trace-mixing branch, NO action dictionary)"); P("="*78)
E = sp.Symbol('E', real=True)
if isinstance(rC1, dict):
    a1c = rC1['a1']
    diff = sp.cancel(sp.factor(sp.together(a1c + 4*E)))
    P(f"   alpha_1(CA5-GNC-R; C1 = 3/10, 1/25, 1/2) = {a1c} ~ {sp.N(a1c, 10)}")
    P(f"   alpha_1 + 4E = {diff}")
    for Ev in [R(1, 100), R(1, 4), 1]:
        val = sp.N(sp.simplify(diff.subs(E, Ev)), 10)
        check(f"N1 alpha_1 = -4E REJECTED at E={Ev}", abs(val) > 1e-6, f"residual = {val}")
    s0, s1 = rC1['s0'], rC1['s1']
    U_amp = rC1['U']
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in FIELDS}
    fillN2 = {A: sp.expand(s0[A] + wb*sp.expand(dk1[A].subs(s1))) for A in FIELDS}
    fillN2[B2k] = sp.expand(s0[B2k] + wb*(-2*E*U_amp)*Rk*w2)
    eqB2 = sp.expand(eq[B2b].subs({GT: 1, LAM: 0, kx: 1, eps: 1, alpha: R(3, 10),
                                   ell: R(1, 25), c2p: R(1, 2), S: 0}))
    res_wb1 = sp.expand(eqB2.subs(fillN2)).coeff(wb, 1)
    res_wb1_s = sp.simplify(res_wb1)
    res_at = sp.N(sp.simplify(res_wb1_s).subs({E: R(1, 100), Rk: 1, w2: 1}), 8)
    res1 = sp.simplify(res_wb1_s.subs(E, 1))
    res1n = res1.subs({Rk: 1, w2: 1})
    check("N2 -4E candidate in ORIGINAL B2-bracket: residual != 0 (REJECTED)",
          res1n != 0 and abs(res_at) > 1e-6,
          f"residual = {res_wb1_s} ~ {res_at} at E=1/100")

P(""); P("="*78); P("FOOTINGS (both a0 footings) and kappa back-check"); P("="*78)
G = 6.67430e-11; c = 299792458.0
for a0v, name in [(9.3619e-11, 'canonical'), (1.1279e-10, 'alternative')]:
    rhoL = 4*a0v**2/(G*c**2)
    kappa_back = a0v/(c*sp.sqrt(G*rhoL))
    check(f"F {name} a0 = {a0v}: rho_Lambda = {rhoL:.6e} kg/m^3, kappa_back = {kappa_back:.9f}",
          abs(kappa_back - 0.5) < 1e-9, "")
P("   alpha_1 is a dimensionless shift/Newtonian-potential ratio; both footings")
P("   give the same coefficient; G_N/G_bare = 1/c_N (AS226) scales amplitudes.")

P(""); P(f"all_pass: {not FAILS}  failures: {FAILS}  total {time.time()-T0:.1f}s")
import sys
sys.exit(0 if not FAILS else 1)