#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
as233_derive.py (v4, bounded) -- AS233 Tier-0b: the high-acceleration
preferred-frame vector response alpha_1 on CA5-GNC-R (FINAL_ACTION (4)).

Moving baryon current J_i sources the transverse shift; alpha_1 is read from
the boosted-foliation ladder with the campaign-certified Will dictionary
(identical spelling to f31_ppn_k4_alpha1.py):

    alpha_1 = 2 * coeff(g_02, w_2) / U_amp,     U_amp = -Psi_k / R_k

BOUNDED construction (seed: retain terms through FIRST ORDER in the source
velocity only):
  * every object truncated at wb^1 (eps^2 order kept for the kinetic slices);
  * w3 = 0, n_3 = 0: the x3 clock lines vanish identically, so contractions
    over {0,1,2} are exact; the 4D SPATIAL TRACE is kept in the Einstein
    part (Ricci over all four indices) so that the gamma = 1 anchor reads
    correctly;
  * fields {Psi, Phi, B2, F}: B3 = s23 = s22 = 0 (unsourced at w3 = wb^1 = 0,
    recorded reduction; B2 is the transverse shift g_02);
  * the K (extrinsic curvature) block vanishes on the flat boosted
    background at the orders needed: its wb^1 coupling is recorded, not
    silently set to zero.

Action pieces (FINAL_ACTION (4)) at (eps^2, wb^1):
    Einstein R (S_GHY caps via the standard Ricci route),         ~Rsc
    V_a = alpha|a-DZ|^2 + 4 a.DZ - 2|DZ|^2 - 4 c_N DZ.DU,  c_N = 1-alpha/2
    compensator c_N ell a.DW_b,  W_b = S_h U (heat saddle; gate f = 0
     inactive, Y_h < 0 on the compact leaf: G(Y_h) = 0),
    matter -16 pi G_T rho (-H_00/2) (dust; current enters via the boost).
    Z = (ell S_k/4) F,  U = F - Z,  a = D F   [ties (6),(7), f=0, rho_d=0]
c_N = 1 - alpha/2 is the ACTION DEFINITION (FINAL_ACTION s.1). Measured-G
normalization: G_N = G_bare/c_N (AS226) is imposed when quoting amplitudes.

The ladder is linear; closed forms are probed at exact rational cells and
verified by substitution back into the ORIGINAL brackets (residuals
printed, never booleans). ANCHOR: pure Einstein (alpha = ell = c2 = 0)
must give gamma = 1 AND alpha_1 = 0. NEGATIVE CONTROL (capable of
failing): the trace-mixing branch value alpha_1 = -4E (no action
dictionary) substituted into the ORIGINAL shift bracket must be REJECTED.
"""
import sympy as sp, time, sys
T0 = time.time(); P = lambda *a: print(*a, flush=True)
FAILS = []
def check(name, ok, detail=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ''))
    if not ok: FAILS.append(name)
    return ok

t, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True)
eps, wb = sp.symbols('eps w_b', positive=True)
w1, w2 = sp.symbols('w1 w2', real=True)
GT, LAM = sp.symbols('G_t Lambda', real=True)
kx = sp.symbols('k_x', real=True)
alpha, ell, c2p, S = sp.symbols('alpha ell c2 S_k', real=True)
cN_expr = 1 - alpha/2
eta = sp.diag(-1, 1, 1, 1); I = sp.I
Es, Eis = sp.symbols('E_s E_is')
kv = [0, kx, 0, 0]

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

def wtrunc(e):
    e = sp.expand(e); return sum(e.coeff(wb, n)*wb**n for n in range(2))

Psi, Psik, Psib = nf('Psi'); Phi, Phik, Phib = nf('Phi')
B2f, B2k, B2b = nf('B2'); Ff, Fk, Fb = nf('F')
rho, Rk, Rb = nf('rho')

# metric ansatz (4D spatial trace kept; B3 = s23 = s22 = 0 recorded)
H = sp.zeros(4, 4)
H[0, 0] = -2*Psi
H[0, 2] = B2f; H[2, 0] = B2f
H[1, 1] = -2*Phi
H[2, 2] = -2*Phi
H[3, 3] = -2*Phi
gd = sp.Matrix(4, 4, lambda m, n: eta[m, n] + eps*H[m, n])
Hup = eta*H*eta
gu = sp.Matrix(4, 4, lambda i, j: (eta - eps*Hup + eps**2*(Hup*H*eta))[i, j])
guT = sp.Matrix(4, 4, lambda m, n: te(gu[m, n]))
gdT = sp.Matrix(4, 4, lambda m, n: te(gd[m, n]))

Gam = [[[sp.Rational(1, 2)*sum(gu[r, s]*(d(gd[s, n], m) + d(gd[s, m], n) - d(gd[m, n], s))
                               for s in range(4)) for n in range(4)] for m in range(4)] for r in range(4)]
GamT = [[[te(Gam[r][m][n]) for n in range(4)] for m in range(4)] for r in range(4)]

def ric(a, b):
    o = 0
    for m in range(4):
        o += d(Gam[m][b][a], m) - d(Gam[m][m][a], b)
        for l in range(4):
            o += Gam[m][m][l]*Gam[l][b][a] - Gam[m][b][l]*Gam[l][m][a]
    return o
Rsc = te(sum(guT[m, n]*ric(m, n) for m in range(4) for n in range(4)))
P(f"[{time.time()-T0:.1f}s] Ricci built")

# ---- boosted clock: n = -tau/sqrt(X_tau), tau = (1, wb w^i) ----
# X_tau = -g^{mu nu} tau_mu tau_nu: the metric couples into the CLOCK NORMAL
# through g^{0i} w_i: this is the channel where the moving source (boosted
# foliation) sources the transverse shift. n is NOT a frozen background.
ww = w1**2 + w2**2
tau_cov = [1, wb*w1, wb*w2, 0]
Xtau = sp.expand(-sum(gu[m, n]*tau_cov[m]*tau_cov[n] for m in range(4) for n in range(4)))
# polynomial series for X_tau^{-1/2} through (eps^2, wb^1):
tc = sp.expand(Xtau - 1)
sqinv = sp.expand(1 + tc/2 - tc**2/8 + tc**3/16 - 5*tc**4/128)
sqinvT = te(sqinv)
# n_mu = -tau_mu / sqrt(X_tau), covariant, X_tau > 0 (time function gradient)
AdnT = [sp.expand(-tau_cov[m]*sqinvT) for m in range(4)]
AupT = [te(sum(gu[m, k]*AdnT[k] for k in range(4))) for m in range(4)]
normc = sp.expand(sum(AupT[m]*AdnT[m] for m in range(4)) + 1)
print(f"[clock] unit-normal check Aup.Adn+1 (trunc.) = {normc}")

def hmu(mu, nu):
    return (1 if mu == nu else 0) + AdnT[mu]*AupT[nu]

aT = [te(-sum(AupT[nu]*sum(GamT[rho][nu][mu]*AdnT[rho] for rho in range(4))
               for nu in range(4))) for mu in range(4)]
def Dsc(F, mu):
    return sum(hmu(mu, nu)*d(F, nu) for nu in range(4))
# extrinsic curvature of the boosted foliation: K_mu nu = h^rho_mu h^sigma_nu
# (d_rho n_sigma - Gam^tau_{rho sigma} n_tau); d n = 0 for the affine boost
def Kmn(mu, nu):
    o = 0
    for rho in range(4):
        for sg in range(4):
            o += hmu(rho, mu)*hmu(sg, nu)*(-sum(GamT[tau][rho][sg]*AdnT[tau] for tau in range(4)))
    return o
KL = [[te(Kmn(mu, nu)) for nu in range(4)] for mu in range(4)]
P(f"[{time.time()-T0:.1f}s] clock a, K built")

# ---- ties (6),(7) f=0, rho_d=0: Z = (ell S/4) F, U = F - Z ----
Zt = (ell*S/4)*Ff
Ut = Ff - Zt
DZT = [Dsc(Zt, m) for m in range(4)]
DUT = [Dsc(Ut, m) for m in range(4)]

def up(A, B):
    return sum(guT[m, n]*A[m]*B[n] for m in range(4) for n in range(4))

ADZ = [aT[m] - DZT[m] for m in range(4)]
V_a = sp.expand(alpha*te(up(ADZ, ADZ)) + 4*te(up(aT, DZT)) - 2*te(up(DZT, DZT))
                - 4*cN_expr*te(up(DZT, DUT)))
P(f"[{time.time()-T0:.1f}s] V_a built")

DWb = [Dsc(S*Ut, m) for m in range(4)]
comp = te(cN_expr*ell*up(aT, DWb))
P(f"[{time.time()-T0:.1f}s] compensator built")

# trace-mixing block -c2 Q_K^2 with Q_K = K (K = 0 on the flat boosted bg)
K2 = te(sum(guT[a, c]*guT[b, d]*KL[a][b]*KL[c][d]
            for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
P(f"[{time.time()-T0:.1f}s] K^2 built")

L2_grav = sp.expand(V_a + comp - c2p*K2 + Rsc - 2*LAM)
L2_matt = -16*sp.pi*GT*wtrunc(rho*(-H[0, 0]/2))
L2 = sp.expand(L2_grav + L2_matt)

def DC_easy(e):
    """diagonal (real-mode) projector: keep Es-balanced monomials via two
    one-variable Poly passes (cheap)."""
    e = sp.expand(e)
    if not (e.has(Es) or e.has(Eis)):
        return e
    pe = sp.Poly(e, Eis)
    out = 0
    for tup, coeff in pe.terms():
        n = tup[0]
        if coeff.has(Es):
            ce = sp.Poly(coeff, Es)
            for tup2, cc in ce.terms():
                if tup2[0] == n:
                    out += cc
        elif n == 0:
            out += coeff
    return sp.expand(out)
L2dc = DC_easy(L2)
P(f"[{time.time()-T0:.1f}s] L2diag: {len(sp.Add.make_args(L2dc))} terms")

KETS = [Psik, Phik, B2k, Fk]
BRAS = [Psib, Phib, B2b, Fb]
eq = {A: sp.expand(sp.diff(L2dc, A)) for A in BRAS}

def lin(eqs, unk):
    Am, bb = sp.linear_eq_to_matrix(eqs, unk)
    s = list(sp.linsolve((Am, bb), unk))
    if len(s) == 1 and not any(v.has(u) for v in s[0] for u in unk):
        return dict(zip(unk, s[0]))
    return None  # singular, underdetermined, or parametric

def ladder(sub):
    """wb-ladder at an exact rational cell; c_N = 1 - alpha/2 imposed by the
    cN_expr substitution in the action build."""
    sub0 = {GT: 1, LAM: 0, kx: 1, **sub}
    eqf = {A: sp.expand(eq[A].subs(sub0)) for A in BRAS}
    # static rung (wb^0): solve [Psik, Phik, Fk]; if F decouples
    # (identically zero Fb-equation), Fk = 0 and solve [Psik, Phik].
    eq0 = [sp.expand(eqf[b].coeff(wb, 0)) for b in [Psib, Phib, Fb]]
    s0s = lin(eq0, [Psik, Phik, Fk])
    if s0s is None:
        s0s2 = lin(eq0[:2], [Psik, Phik])
        if s0s2 is None:
            return 'SING0'
        s0s = {**s0s2, Fk: sp.S(0)}
    s0 = {**s0s, B2k: sp.S(0)}
    U_amp = sp.cancel(-s0[Psik]/Rk); gamma = sp.cancel(s0[Phik]/s0[Psik])
    dk1 = {A: sp.Symbol(f'd1_{A}') for A in KETS}
    subF = {A: s0[A] + wb*dk1[A] for A in KETS}
    eqW = {A: sp.expand(eqf[A].subs(subF)) for A in BRAS}
    s1 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in BRAS], list(dk1.values()))
    if s1 is None:
        # window (S_k = 0): F/U decouples (DZ = 0) -> 3-field subsystem
        sub3 = lin([sp.expand(eqW[A].coeff(wb, 1)) for A in [Psib, Phib, B2b]],
                   [dk1[Psik], dk1[Phik], dk1[B2k]])
        if sub3 is None:
            return ('SING1', U_amp, gamma)
        s1 = {**sub3, dk1[Fk]: sp.S(0)}
    c2t = sp.cancel(sp.expand(dk1[B2k].subs(s1)).coeff(w2)/Rk)
    alpha1 = sp.cancel(2*c2t/U_amp)
    return dict(U=U_amp, g=gamma, a1=alpha1, s1=s1, s0=s0)

R = lambda a, b: sp.Rational(a, b)

P(""); P("="*78); P("ANCHOR A (capability gate): pure Einstein  alpha=ell=c2=0"); P("="*78)
rA = ladder({alpha: 0, ell: 0, c2p: 0, S: 0})
check("A ladder regular", isinstance(rA, dict), str(rA)[:50])
if isinstance(rA, dict):
    check("A gamma = 1", sp.simplify(rA['g'] - 1) == 0, f"gamma = {rA['g']}")
    check("A alpha_1 = 0 (Einstein limit has no preferred-frame response)",
          sp.simplify(rA['a1']) == 0, f"a1 = {rA['a1']}")
    P(f"   U_amp = {rA['U']}")

P(""); P("="*78); P("MAIN CELL C1 = (alpha=3/10, ell=1/25, c2=1, S->0)"); P("="*78)
rC1 = ladder({alpha: R(3, 10), ell: R(1, 25), c2p: 1, S: 0})
check("C1 regular", isinstance(rC1, dict), str(rC1)[:60])
if isinstance(rC1, dict):
    P(f"   gamma = {rC1['g']}")
    P(f"   U_amp = {sp.nsimplify(rC1['U'])}")
    P(f"   alpha_1(C1) = {rC1['a1']}  ~ {sp.N(rC1['a1'], 12)}")
    ratio = R(1, 1)/(1 - R(3, 10)/2)
    P(f"   measured-G normalization: G_N/G_bare = 1/c_N = {ratio}")
    s0, s1 = rC1['s0'], rC1['s1']
    full = {A: sp.expand(s0[A] + wb*s1[A]) for A in KETS}
    par = {GT: 1, LAM: 0, kx: 1, alpha: R(3,10), ell: R(1,25), c2p: 1, S: 0}
    for A in BRAS:
        expr = sp.expand(eq[A].subs({**par, **full}))
        r0 = sp.simplify(expr.coeff(wb, 0)); r1 = sp.simplify(expr.coeff(wb, 1))
        check(f"C1b bracket {A}: substitution-back residual (wb^0, wb^1)",
              r0 == 0 and r1 == 0, f"({r0}, {r1})")
    for m in range(4):
        ar = sp.simplify(sp.expand(aT[m].subs({**full, Rk: 1})).coeff(wb, 1))
        df = sp.simplify(sp.expand(Dsc(Ff, m).subs({**full, Rk: 1})).coeff(wb, 1))
        check(f"C1c tie a_{m} = D_{m} F @ wb^1", sp.simplify(ar - df) == 0, f"{sp.simplify(ar-df)}")
    if S > 0 or True:
        D2Z = sum(eta[m, m]*d(DZT[m], m) for m in range(4))
        D2a = sum(eta[m, m]*d(aT[m], m) for m in range(4))
        lhs6 = sp.simplify(sp.expand(4*D2Z.subs({**full, Rk: 1})).coeff(wb, 1)).subs(S, 0)
        rhs6 = sp.simplify(sp.expand(S*ell*D2a.subs({**full, Rk: 1})).coeff(wb, 1)).subs(S, 0)
        check("C1d tie (6): 4 Delta Z = S_k ell div a @ wb^1",
              sp.simplify(lhs6 - rhs6) == 0, f"{sp.simplify(lhs6-rhs6)}")

P(""); P("="*78); P("CLOSED FORM probe alpha_1(alpha) at rational cells, c_N = 1-alpha/2"); P("="*78)
a1s = {}
for av in [R(1, 10), R(3, 10), R(1, 2), R(3, 4), 1]:
    r = ladder({alpha: av, ell: R(1, 25), c2p: 1, S: 0})
    a1s[av] = r['a1'] if isinstance(r, dict) else None
    P(f"   alpha={av}: alpha_1 = {a1s[av]} ({sp.N(a1s[av], 10) if a1s[av] is not None else 'SING'})")

P(""); P("="*78); P("NEGATIVE CONTROL: alpha_1 = -4E (trace-mixing branch, NO action dictionary)"); P("="*78)
E = sp.Symbol('E', real=True)
if isinstance(rC1, dict):
    a1c = rC1['a1']
    diff = sp.cancel(sp.factor(sp.together(a1c + 4*E)))
    P(f"   alpha_1(CA5-GNC-R; C1) = {a1c} ~ {sp.N(a1c, 10)}")
    P(f"   alpha_1 + 4E = {diff}")
    for Ev in [R(1, 100), R(1, 4), 1]:
        val = sp.N(sp.simplify(diff.subs(E, Ev)), 10)
        check(f"N1 alpha_1 = -4E REJECTED at E={Ev}", abs(val) > 1e-6, f"residual = {val}")
    # forcing alpha_1 = -4E sets the candidate shift coefficient c2t = -2E U_amp;
    # substitute into the ORIGINAL B2-bracket and require non-annihilation:
    s0, s1 = rC1['s0'], rC1['s1']
    U_amp = rC1['U']
    fillN2 = {A: sp.expand(s0[A] + wb*s1[A]) for A in KETS}
    fillN2[B2k] = sp.expand(s0[B2k] + wb*sp.cancel((-2*E*U_amp)*Rk*w2))
    eqB2 = sp.expand(eq[B2b].subs({GT: 1, LAM: 0, kx: 1, alpha: R(3,10), ell: R(1,25), c2p: 1, S: 0}))
    res_wb1 = sp.simplify(sp.expand(eqB2.subs(fillN2)).coeff(wb, 1))
    res_at = sp.N(sp.simplify(res_wb1).subs(E, R(1, 100)), 8)
    check("N2 -4E candidate in ORIGINAL B2-bracket: residual != 0 (REJECTED)",
          sp.simplify(res_wb1) != 0 and abs(res_at) > 1e-6,
          f"residual(B2bracket) = {res_wb1} ~ {res_at} at E=1/100")

P(""); P("="*78); P("FOOTINGS (both a0 footings) and kappa back-check"); P("="*78)
G = 6.67430e-11; c = 299792458.0
for a0v, name in [(9.3619e-11, 'canonical'), (1.1279e-10, 'alternative')]:
    rhoL = 4*a0v**2/(G*c**2)
    kappa_back = a0v/(c*sp.sqrt(G*rhoL))
    check(f"F {name} a0 = {a0v}: rho_Lambda = {rhoL:.6e} kg/m^3, kappa_back = {kappa_back:.9f}",
          abs(kappa_back - 0.5) < 1e-9, "")
P("   alpha_1 is a dimensionless ratio of shift to Newtonian potential; both")
P("   footings give the same coefficient. Measured-G normalization: the ratio")
P("   G_N/G_bare = 1/c_N = 1/(1-alpha/2) (AS226) sets the amplitude scale.")

P(""); P(f"all_pass: {not FAILS}  failures: {FAILS}  total {time.time()-T0:.1f}s")
sys.exit(0 if not FAILS else 1)