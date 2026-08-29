#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_alpha2_methodC_2026.py
============================================================================================
METHOD C -- preferred-frame PPN parameters alpha_1, alpha_2 for FC-AeST (AeST + frozen J_10
MOND kernel), by DIRECT POSITION-SPACE EULER-LAGRANGE variation of the covariant action with a
MOVING SOURCE (aether/scalar boosted by wind w), single Fourier mode k ALONG z, FULL
ANISOTROPIC even-sector metric.  INDEPENDENT of the k-along-x amplitude method.

This FINISHES fc_aest_corner/fc_alpha2_scalar_retained.py (whose stub gauge {H0x:0,Hxz:0} was
WRONG -- H0x is gauge-invariant and carries alpha_1) and mirrors the VALIDATED w=0 machinery of
real_research/reviews/typeII_direct_variation_2026.py (44/44 checks), extended to the boosted
background, the correct gauge, and the w-order solve.

ACTION (units 1/16 pi G_t, mostly-plus eta=diag(-1,1,1,1)):
  S = int sqrt(-g)[ R - 2 Lam - (K_B/2) F^2 + 2(2-K_B) J^mu d_mu phi - (2-K_B) Y
        - F(Y,Q) - lam(A^mu A_mu + 1) ] + S_matter
  Q = A^mu d_mu phi ;  Y = (g^{mn}+A^m A^n) d_m phi d_n phi ;  F_{mn}=d_m A_n - d_n A_m ;
  J^mu = A^nu nabla_nu A^mu ;  F(Y,Q) = (2-K_B) Jcal(Y) + K(Q) , K(Q)=-2Lam+K_2(Q-Q_0)^2 .
KERNEL-BLINDNESS: Jcal=O(Y^{3/2}) => delta^2 Jcal=0 at quadratic order; its ONLY footprint is
  the first-variation coefficient J_Y.  Y-kinetic coefficient = (2-K_B)(1+J_Y) (inert J_Y).

METHOD: metric background FLAT (only aether/scalar boosted).  A^mu_bg=(1+w^2/2, wx,0,wz),
  d_mu phi_bg = -Q0 A_mu_bg  =>  Q=Q0, Y=0 (certified).  lam_bg=(2-K_B)(1+J_Y)Q0^2.  Matter =
  static dust at rest, density rho, 00 only.  Perturbations static, z-only Fourier (d_3=ik,
  d_0=d_1=d_2=0).  Wind w=(wx,0,wz).  Expand to O(eps^2) (linear EOMs) and O(w^2).  Position-
  space Euler-Lagrange (real differential EOMs), THEN Fourier f(z)->A_f e^{ikz}, THEN solve the
  coupled LINEAR system order by order in w.

GAUGE (k along z, d_3=ik): gauge-invariant = H00, H0x(=H01), Hxx(=H11), Hyy(=H22); gauge-variant
  H0z,Hxz,Hzz fixed to 0 (residual static diffeos xi_0,xi_1,xi_3).

EXTRACTION (Will PPN; U = -4 pi G_t rho / k^2, the source proxy):
  alpha_1 = 2 * [coeff of (w_perp U) in H0x at O(w^1)],  w_perp = wx (perp to k=zhat)
  H00 = -2 Psi at O(w^2):  PA   = coeff of (wx^2 U) in H00 = 2 alpha_2 - alpha_1  (perp channel)
                           PApar = coeff of (wz^2 U) in H00 = PA - 2 alpha_2       (par channel)
  => alpha_2(perp)=(PA+alpha_1)/2 ;  alpha_2(par)=-(PApar-PA)/2 .

VALIDATION (report alpha_2 only if all pass):
  (G0) w=0: gamma_PPN=1 (Phi=Psi), 00-eq -> lap Psi - m_Psi^2 Psi = 4 pi Ghat rho with
       Ghat=Gt/(1-K_B/2), m_Psi^2 = K_2 Q0^2/(2-K_B).  (reproduces typeII)
  (V1) alpha_1 = -4 K_B  (independent c-tensor / Foster-Jacobson value, fc_ctensor_map_2026.py)
  (V2) [D2] alpha_2(perp) == alpha_2(par).
"""
import sys, time, itertools, os
import sympy as sp

PURE_EA = os.environ.get('PURE_EA','0') == '1'   # scalar OFF: pure Einstein-aether, alpha_1 must be -4K_B
T0 = time.time()
P = lambda *a: print(*a, flush=True)
FAIL, NCHK = [], [0]
def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    P(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok
def info(l, d=""):
    P(f"  [info] {l}" + (f"\n         {d}" if d else ""))

# ---------------------------------------------------------------- symbols
z   = sp.Symbol('z', real=True)
eps = sp.Symbol('eps')                        # perturbation bookkeeping (=> O(rho))
wx, wz = sp.symbols('w_x w_z', real=True)     # wind (x-z plane)
KB, K2, Q0, JY = sp.symbols('K_B K_2 Q_0 J_Y', real=True)
rho = sp.Symbol('rho', real=True)             # source amplitude (Fourier)
k   = sp.Symbol('k', positive=True)
eta = sp.diag(-1, 1, 1, 1)
I   = sp.I
GT  = sp.Integer(1)                           # units: G_t = 1 ; U = -4 pi rho / k^2
LAM = sp.Integer(0)                           # background gate K(Q0)+2Lam=0 holds for any Lam; 0 is consistent

def W2():
    return wx**2 + wz**2

# truncate: eps to degree 2, (wx,wz) total degree <= 2  (POLYNOMIAL inputs only)
def tw(e):
    e = sp.expand(e)
    out = 0
    for de in range(3):
        ce = sp.expand(e.coeff(eps, de))
        for i in range(3):
            for j in range(3 - i):
                out += ce.coeff(wx, i).coeff(wz, j) * eps**de * wx**i * wz**j
    return sp.expand(out)

# series-truncate the WIND to total degree 2, valid for RATIONAL w-dependence (constraint solns)
_bb = sp.Symbol('_bb')
def wseries(e):
    e2 = sp.together(e).subs({wx: _bb*wx, wz: _bb*wz})
    e2 = sp.series(e2, _bb, 0, 3).removeO().subs(_bb, 1)
    return sp.expand(e2)

# =============================================================== [A] boosted aligned background
P("="*92); P("[A] boosted aligned background (metric flat; aether+scalar boosted)"); P("="*92)
Aup_bg = sp.Matrix([1 + W2()/2, wx, 0, wz])
Adn_bg = eta * Aup_bg
normc = tw((Adn_bg.T * Aup_bg)[0] + 1)
check(sp.expand(normc) == 0, "[A1] A^mu A_mu = -1 on the boosted background to O(w^2)",
      f"A.A+1 = {normc}")
dphi_bg = -Q0 * Adn_bg
Qbg = tw((Aup_bg.T * dphi_bg)[0])
check(sp.simplify(Qbg - Q0) == 0, "[A2] Q = A^mu d_mu phi = Q0 on background", f"Q_bg = {Qbg}")
proj_bg = sp.Matrix(4,4, lambda m,n: eta[m,n] + Aup_bg[m]*Aup_bg[n])
Ybg = tw((dphi_bg.T * proj_bg * dphi_bg)[0])
check(sp.simplify(Ybg) == 0, "[A3] Y = 0 on the boosted background (aligned)", f"Y_bg = {Ybg}")
P(f"    ({time.time()-T0:.1f}s)")

# =============================================================== [B] perturbations (even sector)
P("="*92); P("[B] generic even-sector perturbations, z-only Fourier mode, k along z"); P("="*92)
names = ['H00','H0x','H0z','Hxx','Hxz','Hzz','Hyy']
Hamp = {nm: sp.Function(nm)(z) for nm in names}
H = sp.zeros(4,4)
H[0,0]=Hamp['H00']; H[0,1]=H[1,0]=Hamp['H0x']; H[0,3]=H[3,0]=Hamp['H0z']
H[1,1]=Hamp['Hxx']; H[1,3]=H[3,1]=Hamp['Hxz']; H[3,3]=Hamp['Hzz']; H[2,2]=Hamp['Hyy']
gdn = sp.Matrix(4,4, lambda m,n: eta[m,n] + eps*H[m,n])
Hup = eta*H*eta
gup = sp.Matrix(4,4, lambda m,n: sp.expand((eta - eps*Hup + eps**2*(Hup*H*eta))[m,n]))
trH = sum(eta[m,n]*H[m,n] for m in range(4) for n in range(4))
HH  = sum(Hup[m,n]*H[m,n] for m in range(4) for n in range(4))
sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)

# aether: lower A_mu = background + eps a_mu + eps^2 b0 (temporal 2nd order); even: a0,ax,az
a0f, ax_f, az_f, b0f = [sp.Function(s)(z) for s in ('a0','ax','az','b0')]
Adn = sp.Matrix([Adn_bg[0] + eps*a0f + eps**2*b0f,
                 Adn_bg[1] + eps*ax_f,
                 Adn_bg[2],
                 Adn_bg[3] + eps*az_f])
Aup = sp.Matrix(4,1, lambda i,j: tw(sum(gup[i,s]*Adn[s] for s in range(4))))
Cc = tw(sum(Aup[m]*Adn[m] for m in range(4)) + 1)                 # A.A + 1  (off surface)
sol_a0 = wseries(sp.solve(sp.expand(Cc).coeff(eps,1), a0f)[0])    # wind-series (rational in w)
Adn = Adn.subs(a0f, sol_a0)
Aup = sp.Matrix(4,1, lambda i,j: tw(sum(gup[i,s]*Adn[s] for s in range(4))))
Cc  = tw(sum(Aup[m]*Adn[m] for m in range(4)) + 1)
sol_b0 = wseries(sp.solve(sp.expand(Cc).coeff(eps,2), b0f)[0])
Adn = Adn.subs(b0f, sol_b0)
Aup = sp.Matrix(4,1, lambda i,j: tw(sum(gup[i,s]*Adn[s] for s in range(4))))
Cres = tw(sum(Aup[m]*Adn[m] for m in range(4)) + 1)
check(sp.simplify(Cres)==0, "[B1] unit constraint A.A=-1 solved order by order (to eps^2, w^2)",
      f"residual = {sp.simplify(Cres)}")

# scalar perturbation: only d_z(delta phi) survives (static, z-only)
phf = sp.Function('phi')(z)
dphi = sp.Matrix([dphi_bg[0], dphi_bg[1], dphi_bg[2], dphi_bg[3] + eps*sp.diff(phf,z)])
P(f"    perturbations set ({time.time()-T0:.1f}s)")

# =============================================================== [C] EH curvature
P("="*92); P("[C] EH sector: Fierz-Pauli linearised Einstein (flat bg, exact at O(eps^2))"); P("="*92)
def d_(f, mu):
    return sp.diff(f, z) if mu == 3 else sp.S(0)
# Christoffels (needed ONLY for the dark-sector J^mu = A^nu nabla_nu A^mu)
Gam = [[[ tw(sp.Rational(1,2)*sum(gup[r,s]*(d_(gdn[s,n],m)+d_(gdn[s,m],n)-d_(gdn[m,n],s))
        for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]
# --- Fierz-Pauli EH: L_EH = -(1/2) h^{mn} G^(1)_{mn}, computed from SECOND derivatives of h
#     (manifestly 2-derivative => no total-derivative/parity artifact; == sqrt(-g)R at O(eps^2)).
Hmix = [[ sum(eta[a,b]*H[b,n] for b in range(4)) for n in range(4)] for a in range(4)]  # H^a_n
def R1(m,n):
    t1 = sum(d_(d_(Hmix[a][n], a), m) for a in range(4))         # d_a d_m H^a_n
    t2 = sum(d_(d_(Hmix[a][m], a), n) for a in range(4))         # d_a d_n H^a_m
    t3 = d_(d_(trH, m), n)                                       # d_m d_n H
    t4 = sum(eta[a,b]*d_(d_(H[m,n], a), b) for a in range(4) for b in range(4))   # box H_{mn}
    return sp.Rational(1,2)*(t1 + t2 - t3 - t4)
R1m = sp.Matrix(4,4, lambda m,n: R1(m,n))
R1sc = sum(eta[m,n]*R1m[m,n] for m in range(4) for n in range(4))
G1 = sp.Matrix(4,4, lambda m,n: R1m[m,n] - sp.Rational(1,2)*eta[m,n]*R1sc)   # linearised Einstein
G1up = sp.Matrix(4,4, lambda m,n: sum(eta[m,a]*eta[n,b]*G1[a,b] for a in range(4) for b in range(4)))
# The EH contribution to the metric field equations is the DIRECT linearised Einstein tensor
# -G1^{mn} (2-derivative, real).  We do NOT position-space-EL the -1/2 h.G1 Lagrangian: that
# operator mis-handles a Lagrangian with second derivatives pre-baked into G1 (verified: it
# returns 1/4(d_z+d_z^2) instead of 1/2 d_z^2).  Off-diagonal carries the factor 2 that the
# dark-sector EL (varying the single function H_{mn}=H_{nm}) also carries.
P(f"    EH (linearised Einstein tensor) assembled ({time.time()-T0:.1f}s)")

# =============================================================== [D] dark sector + Lagrangian
P("="*92); P("[D] F^2, J.dphi, Y, Q, K(Q); assemble L; Euler-Lagrange"); P("="*92)
Fmn = sp.Matrix(4,4, lambda m,n: d_(Adn[n],m) - d_(Adn[m],n))
F2 = tw(sum(Fmn[m,n]*Fmn[a,b]*gup[m,a]*gup[n,b]
            for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
Jup = [ tw(sum(Aup[nu]*( d_(Aup[al],nu) + sum(Gam[al][nu][r]*Aup[r] for r in range(4)) )
        for nu in range(4))) for al in range(4)]
Jdphi = tw(sum(Jup[m]*dphi[m] for m in range(4)))
Qf = tw(sum(Aup[m]*dphi[m] for m in range(4)))
Yf = tw(sum((gup[m,n]+Aup[m]*Aup[n])*dphi[m]*dphi[n] for m in range(4) for n in range(4)))
dQ = sp.expand(Qf - Q0)
KQ = -2*LAM + K2*tw(dQ**2)

# dark + matter Lagrangian (EH handled directly via -G1^{mn}); constraint SOLVED, multiplier
# dropped (typeII route), Y-kinetic = (2-K_B)(1+J_Y).  LAM=0 (background gate K(Q0)+2LAM=0 holds).
if PURE_EA:
    Lother = tw( sqg*( -(KB/2)*F2 ) ) - 16*sp.pi*GT*eps*rho*(1 - eps*H[0,0]/2)   # aether kinetic only
else:
    Lother = tw( sqg*( -2*LAM - (KB/2)*F2 + 2*(2-KB)*Jdphi - (2-KB)*(1+JY)*Yf - KQ ) ) \
             - 16*sp.pi*GT*eps*rho*(1 - eps*H[0,0]/2)           # dark + static dust (00 only)
P(f"    Lother assembled ({'PURE_EA' if PURE_EA else 'FC-AeST'}): "
  f"{len(sp.Add.make_args(sp.expand(Lother)))} terms ({time.time()-T0:.1f}s)")

# Euler-Lagrange in z (dark+matter only)
def EL(Lag, f):
    fp = sp.Derivative(f, z); fpp = sp.Derivative(f, (z,2))
    out = sp.diff(Lag, f) - sp.diff(sp.diff(Lag, fp), z) + sp.diff(sp.diff(Lag, fpp), z)
    return sp.expand(out.doit())

# Field equations for ALL 10 fields.  Metric fields get EH = -eps^2 (2-delta_{mn}) G1^{mn}
# (direct linearised Einstein, off-diagonal factor 2) PLUS the dark/matter EL.  The 3 gauge-field
# variations (H0z,Hxz,Hzz) are constraints; imposed as conditions in the over-determined solve.
ALLF = {'H00':Hamp['H00'],'H0x':Hamp['H0x'],'H0z':Hamp['H0z'],'Hxx':Hamp['Hxx'],
        'Hxz':Hamp['Hxz'],'Hzz':Hamp['Hzz'],'Hyy':Hamp['Hyy'],
        'ax':ax_f,'az':az_f,'phi':phf}
FIELD_IDX = {'H00':(0,0),'H0x':(0,1),'H0z':(0,3),'Hxx':(1,1),'Hxz':(1,3),'Hzz':(3,3),'Hyy':(2,2)}
EOM = {}
for nm,f in ALLF.items():
    e = EL(Lother, f)
    if nm in FIELD_IDX:
        m,n = FIELD_IDX[nm]
        fac = 1 if m==n else 2
        e = sp.expand(e - eps**2*fac*G1up[m,n])
    EOM[nm] = e
P(f"    EOMs assembled ({time.time()-T0:.1f}s)")

# --- Fourier: f(z) -> A_f e^{ikz}; strip e^{ikz}; keep LINEAR in amplitudes (source rho linear)
amps = {nm: sp.Symbol('A_'+nm) for nm in ALLF}
E = sp.exp(I*k*z)
def fourier(e):
    subs = {}
    for nm,f in ALLF.items():
        subs[sp.Derivative(f,(z,2))] = (I*k)**2*amps[nm]*E
        subs[sp.Derivative(f,z)]     = (I*k)*amps[nm]*E
        subs[f] = amps[nm]*E
    # the matter source rho is the density Fourier amplitude: it carries e^{ikz} like a field,
    # so that dividing by E leaves a clean algebraic source (no stray phase).
    subs[rho] = rho*E
    return sp.expand(sp.expand(e.subs(subs)) / E)
AMPSET = [amps[nm] for nm in ALLF]
# amplitudes fixed to 0:
#   H0z,Hxz,Hzz  -- coordinate-gauge (residual static diffeos xi_0,xi_1,xi_3)
#   az           -- LONGITUDINAL aether = Stueckelberg mode degenerate with phi (only
#                   chi = phi + Q0 a_par physical; typeII D8).  Transverse a_x is KEPT (physical).
GAUGE_ZERO = ['H0z','Hxz','Hzz','phi','az'] if PURE_EA else ['H0z','Hxz','Hzz','az']
def linearize(e):
    e = sp.expand(e); out = 0
    for term in sp.Add.make_args(e):
        deg = sum((sp.degree(term, a) if term.has(a) else 0) for a in AMPSET)
        if deg <= 1:
            out += term
    return sp.expand(out)
EOM_k = {nm: linearize(fourier(EOM[nm])) for nm in ALLF}
P(f"    Fourier + linearised ({time.time()-T0:.1f}s)")
# hygiene: no stray e^{+-ikz} phases, and (after removing the rho source) no field-free tadpoles
stray = any(EOM_k[nm].has(E) or EOM_k[nm].has(sp.exp(-I*k*z)) for nm in ALLF)
check(not stray, "[B2] no residual e^{+-ikz} phase in the linearised EOMs")
tad = 0
for nm in ALLF:
    e = sp.expand(EOM_k[nm])
    for term in sp.Add.make_args(e):
        if sum((sp.degree(term,a) if term.has(a) else 0) for a in AMPSET)==0 and not term.has(rho):
            tad += 1
check(tad==0, "[B3] no field-free background tadpole terms survive (background solves its eqs)",
      f"tadpole terms found: {tad}")

# =============================================================== solver (order by order in w)
def wcoeff(e, i, j):   # coeff of wx^i wz^j
    return sp.expand(e).coeff(wx, i).coeff(wz, j)

FIELDS = list(ALLF)                       # order (all 10)
def _solve(eqlist, unklist):
    """robust over-determined exact solve; None if inconsistent/underdetermined."""
    M, b = sp.linear_eq_to_matrix(eqlist, unklist)
    sol = sp.linsolve((M, b), unklist)
    if not sol:
        return None
    vals = list(sol)[0]
    # reject residual free parameters (underdetermined)
    if any(v.free_symbols & set(unklist) for v in vals):
        return None
    return dict(zip(unklist, vals))

def solve_point(subsnum):
    """subsnum: dict of numeric params.  Solves the PERP (wz=0, expand wx) and PAR (wx=0,
    expand wz) channels INDEPENDENTLY, order by order.  Returns a dict; each channel that
    fails is flagged rather than aborting the whole point."""
    eqs = {nm: sp.expand(EOM_k[nm].subs(subsnum)) for nm in FIELDS}
    U = sp.Symbol('U')                    # U = -4 pi rho / k^2  => rho = -U k^2/(4 pi)
    ksub = subsnum[k]
    for nm in FIELDS:
        eqs[nm] = sp.expand(eqs[nm].subs(rho, -U*ksub**2/(4*sp.pi)))
    unks = [amps[nm] for nm in FIELDS]
    gauge_eq = [amps[g] for g in GAUGE_ZERO]

    # w^0 (wx=wz=0)
    e0 = [sp.expand(eqs[nm].subs({wx:0,wz:0})) for nm in FIELDS] + gauge_eq
    s0 = _solve(e0, unks)
    if s0 is None: return {'U':U, 's0':None}
    out = {'U':U, 's0':s0}

    for chan, wv, wo in (('perp', wx, wz), ('par', wz, wx)):
        e = {nm: sp.expand(eqs[nm].subs(wo, 0)) for nm in FIELDS}   # set the OTHER wind to 0
        # w^1
        u1 = {nm: sp.Symbol('u1_'+nm) for nm in FIELDS}
        sub1 = {amps[nm]: s0[amps[nm]] + wv*u1[nm] for nm in FIELDS}
        e1 = [sp.expand(e[nm].subs(sub1)).coeff(wv,1) for nm in FIELDS] + [u1[g] for g in GAUGE_ZERO]
        s1 = _solve(e1, [u1[nm] for nm in FIELDS])
        if s1 is None:
            out[chan] = None; continue
        # w^2
        u2 = {nm: sp.Symbol('u2_'+nm) for nm in FIELDS}
        sub2 = {amps[nm]: s0[amps[nm]] + wv*s1[u1[nm]] + wv**2*u2[nm] for nm in FIELDS}
        e2 = [sp.expand(e[nm].subs(sub2)).coeff(wv,2) for nm in FIELDS] + [u2[g] for g in GAUGE_ZERO]
        s2 = _solve(e2, [u2[nm] for nm in FIELDS])
        out[chan] = {'w1':{nm:s1[u1[nm]] for nm in FIELDS},
                     'w2':(None if s2 is None else {nm:s2[u2[nm]] for nm in FIELDS})}
    return out

def extract(res):
    U = res['U']
    d = {'H00_0':None,'Hxx_0':None,'Hyy_0':None,'a1':None,'PA':None,'PApar':None,'a2p':None,'a2l':None}
    if res['s0'] is None: return d
    d['H00_0']=sp.simplify(res['s0'][amps['H00']]); d['Hxx_0']=sp.simplify(res['s0'][amps['Hxx']])
    d['Hyy_0']=sp.simplify(res['s0'][amps['Hyy']])
    perp, par = res.get('perp'), res.get('par')
    if perp is not None:
        d['a1'] = sp.simplify(2*sp.expand(perp['w1']['H0x']).coeff(U,1))     # alpha_1 (perp H0x)
        if perp['w2'] is not None:
            d['PA'] = sp.simplify(sp.expand(perp['w2']['H00']).coeff(U,1))   # coeff wx^2 U
    if par is not None and par['w2'] is not None:
        d['PApar'] = sp.simplify(sp.expand(par['w2']['H00']).coeff(U,1))     # coeff wz^2 U
    if d['a1'] is not None and d['PA'] is not None:
        d['a2p'] = sp.simplify((d['PA'] + d['a1'])/2)
    if d['PApar'] is not None and d['PA'] is not None:
        d['a2l'] = sp.simplify(-(d['PApar'] - d['PA'])/2)
    return d

# =============================================================== rank diagnostic (one point)
P("="*92); P("[E0] rank diagnostic of the w=0 system"); P("="*92)
_dg = {KB:sp.Rational(3,10), K2:sp.Integer(10), Q0:sp.Rational(1,2), JY:sp.Integer(1), k:sp.Integer(1)}
_eqs = {nm: sp.expand(EOM_k[nm].subs(_dg).subs(rho,0)) for nm in FIELDS}   # homogeneous (rho=0)
_e0 = [sp.expand(wcoeff(_eqs[nm],0,0)) for nm in FIELDS]
_unk = [amps[nm] for nm in FIELDS]
_M,_b = sp.linear_eq_to_matrix(_e0, _unk)
P(f"    w=0 EOM matrix: {_M.shape}, rank = {_M.rank()} (unknowns=10)")
_Mg,_bg = sp.linear_eq_to_matrix(_e0 + [amps[g] for g in GAUGE_ZERO], _unk)
P(f"    + 3 gauge conds: {_Mg.shape}, rank = {_Mg.rank()}  (need 10 for unique)")
_Mg2,_ = sp.linear_eq_to_matrix(_e0 + [amps[g] for g in GAUGE_ZERO] + [amps['az']], _unk)
P(f"    + gauge + az=0: rank = {_Mg2.rank()}")
_ns = _Mg.nullspace()
P(f"    nullspace dim (gauge-fixed) = {len(_ns)}; vectors point along:")
for v in _ns:
    nz = [str(_unk[i]) for i in range(len(_unk)) if v[i]!=0]
    P(f"        {nz}")
# --- w1 consistency diagnostic ---
_U = sp.Symbol('U'); _rhoU = -_U*1**2/(4*sp.pi)
_eqsU = {nm: sp.expand(EOM_k[nm].subs(_dg).subs(rho,_rhoU)) for nm in FIELDS}
_e0g = [sp.expand(wcoeff(_eqsU[nm],0,0)) for nm in FIELDS] + [amps[g] for g in GAUGE_ZERO]
_M0,_b0 = sp.linear_eq_to_matrix(_e0g,_unk)
_s0 = sp.linsolve((_M0,_b0), _unk)
if _s0:
    _s0 = dict(zip(_unk, list(_s0)[0]))
    P(f"    w0 solved. full s0:")
    for nm in FIELDS:
        P(f"        {nm:5s} = {sp.simplify(_s0[amps[nm]])}")
    P(f"    raw w0 EOM[H00] = {sp.expand(wcoeff(_eqsU['H00'],0,0))}")
    P(f"    raw w0 EOM[phi] = {sp.expand(wcoeff(_eqsU['phi'],0,0))}")
    P(f"    raw w0 EOM[ax]  = {sp.expand(wcoeff(_eqsU['ax'],0,0))}")
    _ux = {nm: sp.Symbol('ux_'+nm) for nm in FIELDS}; _uz={nm:sp.Symbol('uz_'+nm) for nm in FIELDS}
    _sub1 = {amps[nm]: _s0[amps[nm]]+wx*_ux[nm]+wz*_uz[nm] for nm in FIELDS}
    _eqs1 = {nm: sp.expand(_eqsU[nm].subs(_sub1)) for nm in FIELDS}
    _ex = [sp.expand(wcoeff(_eqs1[nm],1,0)) for nm in FIELDS] + [_ux[g] for g in GAUGE_ZERO]
    _Mx,_bx = sp.linear_eq_to_matrix(_ex, [_ux[nm] for nm in FIELDS])
    _aug = _Mx.row_join(_bx)
    P(f"    w1 (perp wx) system: rank(M)={_Mx.rank()}  rank([M|b])={_aug.rank()}  "
      f"({'CONSISTENT' if _Mx.rank()==_aug.rank() else 'INCONSISTENT'})")
    def _consist(extra):
        rows = [sp.expand(wcoeff(_eqs1[nm],0,1)) for nm in FIELDS] + [_uz[g] for g in extra]
        M,b = sp.linear_eq_to_matrix(rows, [_uz[nm] for nm in FIELDS])
        aug = M.row_join(b)
        return M.rank(), aug.rank()
    for tag, extra in [("bare 10-EOM", []),
                       ("+coord gauge (H0z,Hxz,Hzz)", ['H0z','Hxz','Hzz']),
                       ("+coord + az=0", ['H0z','Hxz','Hzz','az']),
                       ("+coord + phi=0", ['H0z','Hxz','Hzz','phi'])]:
        rM,rA = _consist(extra)
        P(f"    w1-par {tag:32s}: rank(M)={rM} rank([M|b])={rA} "
          f"{'CONSISTENT' if rM==rA else 'INCONSISTENT'}")

# =============================================================== w=0 GATE (symbolic-ish, one point)
P("="*92); P("[E] w=0 gate (reproduce typeII) + V1/V2 on the grid"); P("="*92)

def cf(x):
    return None if x is None else complex(x)

def run(KBv, K2v, Q0v, JYv, kv=1):
    subsnum = {KB:sp.nsimplify(KBv), K2:sp.nsimplify(K2v), Q0:sp.nsimplify(Q0v),
               JY:sp.nsimplify(JYv), k:sp.Integer(kv)}
    return extract(solve_point(subsnum))

# --- dump perp channel structure at gate point ---
_gp = {KB:sp.Rational(3,10), K2:sp.Integer(10), Q0:sp.Rational(1,2), JY:sp.Integer(1), k:sp.Integer(1)}
_R = solve_point(_gp); _Uu=_R['U']
info("PERP channel dump at (0.3,10,0.5,1), k=1:")
if _R.get('s0') is not None and _R.get('perp'):
    for nm in FIELDS:
        v = sp.simplify(_R['perp']['w1'][nm])
        if v!=0: info(f"    w1[{nm}] = {v}")
    if _R['perp']['w2']:
        for nm in ['H00','Hxx','Hyy','H0x']:
            v = sp.simplify(_R['perp']['w2'][nm])
            info(f"    w2[{nm}] = {v}")

# --- scalar-decoupling probe: alpha_1 -> -4 K_B as Q0->0 (pure vector, c-tensor map) ---
info("alpha_1(perp) vs Q0 at K_B=0.3, K2=10, JY=1, k=1  [pure-vector target -4K_B = -1.2]:")
for q0v in (sp.Rational(1,2), sp.Rational(1,10), sp.Rational(1,100), sp.Rational(1,1000)):
    gg = run(sp.Rational(3,10), 10, q0v, 1)
    a1v = gg['a1']
    info(f"    Q0={float(q0v):8.4f}: alpha_1 = {None if a1v is None else complex(a1v).real:.6f}")
info("alpha_1(perp) vs Q0 at K_B=0.05 [target -0.2]:")
for q0v in (sp.Rational(1,2), sp.Rational(1,100), sp.Rational(1,1000)):
    gg = run(sp.Rational(1,20), 10, q0v, 1)
    a1v = gg['a1']
    info(f"    Q0={float(q0v):8.4f}: alpha_1 = {None if a1v is None else complex(a1v).real:.6f}")

# gate: representative point, print w=0 potentials, alpha_1, and channel status
GK = run(sp.Rational(3,10), 10, sp.Rational(1,2), 1)
if GK['H00_0'] is None:
    check(False, "[G0] w=0 solve")
else:
    info("w=0 potentials at (K_B,K2,Q0,JY)=(0.3,10,0.5,1):")
    info(f"    H00^(0) = {GK['H00_0']}   Hxx^(0) = {GK['Hxx_0']}   Hyy^(0) = {GK['Hyy_0']}")
    gam_ok = sp.simplify(GK['Hxx_0'] - GK['H00_0']) == 0 and sp.simplify(GK['Hyy_0'] - GK['H00_0']) == 0
    check(gam_ok, "[G0] gamma_PPN = 1  (Hxx^(0)=Hyy^(0)=H00^(0) => Phi=Psi)")
    info(f"    alpha_1 (perp channel) = {GK['a1']}  (target -4 K_B = {-4*sp.Rational(3,10)})")
    info(f"    alpha_2_perp = {GK['a2p']}   alpha_2_par = {GK['a2l']}")

# =============================================================== GRID
grid = list(itertools.product([sp.Rational(1,20), sp.Rational(3,10)],   # K_B
                              [10, 300],                                 # K_2
                              [sp.Rational(1,5), sp.Rational(9,10)],     # Q_0
                              [1, 2]))                                   # J_Y
P("")
P(f"{'K_B':>6}{'K2':>6}{'Q0':>6}{'JY':>4} | {'alpha_1':>10}(V1) | {'alpha_2_perp':>15}{'alpha_2_par':>15}  [D2]")
rows = []
for KBv,K2v,Q0v,JYv in grid:
    r = run(KBv,K2v,Q0v,JYv)
    a1,a2p,a2l = r['a1'],r['a2p'],r['a2l']
    a1ok = (a1 is not None) and sp.simplify(a1 + 4*KBv)==0
    d2   = (a2p is not None) and (a2l is not None) and sp.simplify(a2p-a2l)==0
    rows.append((KBv,K2v,Q0v,JYv,a1,a2p,a2l,a1ok,d2))
    a1s = f"{cf(a1).real:+10.5f}" if a1 is not None else f"{'None':>10}"
    a2ps= f"{cf(a2p).real:15.7g}" if a2p is not None else f"{'None':>15}"
    a2ls= f"{cf(a2l).real:15.7g}" if a2l is not None else f"{'None':>15}"
    P(f"{float(KBv):6.2f}{float(K2v):6.0f}{float(Q0v):6.2f}{float(JYv):4.0f} | "
      f"{a1s}{'ok' if a1ok else '!!'} | {a2ps}{a2ls}  {'OK' if d2 else 'DIFF'}")

P("="*92)
if rows:
    v1all = all(rw[7] for rw in rows)
    v2all = all(rw[8] for rw in rows)
    check(v1all, "[V1] alpha_1 = -4 K_B at every grid point")
    check(v2all, "[V2] [D2] alpha_2(perp) == alpha_2(par) at every grid point")
    d2rows = [rw for rw in rows if rw[8]]
    if d2rows:
        amin = min(d2rows, key=lambda rw: abs(complex(rw[5])))
        P(f"    min |alpha_2| over [D2]-consistent points = {abs(complex(amin[5])):.6g}")
        P(f"        at (K_B,K2,Q0,JY) = ({float(amin[0])},{float(amin[1])},{float(amin[2])},{float(amin[3])})")
        P(f"    bound |alpha_2| < 1e-7  =>  "
          f"{'PASS (band exists)' if abs(complex(amin[5]))<1e-7 else 'ALL POINTS EXCEED BOUND'}")

nfail = len(FAIL)
P("="*92)
P(f"    {NCHK[0]-nfail}/{NCHK[0]} certificates pass" + ("" if nfail==0 else f";  FAILED: {FAIL}"))
P(f"    runtime {time.time()-T0:.1f}s")
sys.exit(0 if nfail==0 else 1)
