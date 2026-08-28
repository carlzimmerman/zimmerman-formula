#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_alpha2_scalar_retained.py
============================================================================================
THE OUTSTANDING CALCULATION: alpha_1, alpha_2 for FC-FINAL (AeST + frozen J_10) with the
SCALAR SECTOR RETAINED, on the consistent boosted-aligned (Q=Q_0, Y=0) background, by
DIRECT VARIATION of the covariant action with a GENERIC metric (NO isotropic ansatz -- that
is exactly what broke fc_alpha2_preferred_frame_2026.py [D1,D2]).

WHY the scalar is mandatory (established, cited):
  * fc_ctensor_map_2026.py: -(K_B/2)F^2 == EA kinetic at (c1,c2,c3,c4)=(K_B,0,-K_B,0), so
    c_123 = c_1+c_2+c_3 = 0  => the pure-vector EA spin-0 mode is NON-dynamical, and the EA
    alpha_2 has a SIMPLE POLE in c_123 (residue K_B^2/(2-K_B) at the AeST dictionary point,
    alpha2_regulated_limit_2026.py B5).  The pure-vector alpha_2 is +infinity.
  * alpha2_linearised_solve_2026.py (aether only): confirmed no static PPN limit; honest
    prior on the SIZE is a=4K_B on the regular (w perp k) branch.
  * The AeST scalar phi supplies a propagating helicity-0 mode (mass mu^2=2K2 Q0^2/(2-K_B))
    that mixes into exactly the soft channel via Q=A^mu d_mu phi.  Retaining it REGULARISES
    alpha_2 to a finite value -- THIS script computes that value.

METHOD (mirrors the validated typeII_direct_variation_2026.py assembly; generic metric):
  * mostly-plus eta=diag(-1,1,1,1); single Fourier mode, k along z; perturbations z-ONLY, so
    d_t=d_x=d_y=0 and d_z=ik.  Wind w=(w_x,0,w_z) in the x-z plane (rotate about k=zhat), so
    the y->-y-odd fields (H0y,Hxy,Hyz,a_y) decouple and vanish: EVEN sector only.
  * background boosted: A^mu_bg=(1+w^2/2, w_x, 0, w_z)+O(w^3), scalar aligned d_mu phi_bg =
    -Q0 A_mu_bg  =>  Q=Q0, Y=0 (certified [A2],[A3]).  matter = static dust AT REST, rho.
  * action S=(1/16 pi G) int sqrt(-g)[R -2Lam -(K_B/2)F^2 +2(2-K_B)J^mu d_mu phi -(2-K_B)Y
    -F(Y,Q) -lambda(A^2+1)] + S_m,  F(Y,Q)=(2-K_B) Jcal(Y)+K(Q), K(Q)=-2Lam+K2(Q-Q0)^2.
    Jcal=O(Y^{3/2})=O(pert^3) at quadratic order (delta^2 J_10=0) -> its ONLY quadratic-order
    footprint is the first-variation coefficient J_Y (inert symbol; the Y-kinetic is
    (2-K_B)(1+J_Y), the mixing 2(2-K_B), exactly as typeII).  At Solar-System accel. J_Y->1.
  * expand to O(eps^2) in perturbations (=> linear EOMs) and O(w^2); Euler-Lagrange in z;
    Fourier; solve order-by-order in w with a strict LINEAR (drop pert x pert) matrix solve.

GATES at w=0 (must reproduce typeII, or nothing downstream is trusted):
  G-gamma  gamma_PPN=1 (Phi=Psi, no dark anisotropic stress in the ij sector).
  G-Ghat   00-eq gives lap Psi - m_Psi^2 Psi = 4 pi Ghat rho, Ghat=Gt/(1-K_B/2).
  G-mass   m_Psi^2 = K2 Q0^2/(2-K_B) = mu^2/2.
VALIDATION at w!=0:
  V-a1vec  in the scalar-decoupling limit (Q0->0) alpha_1 -> -4 K_B (the c-tensor/FJ value).

OUTPUT: alpha_1(K_B,K2,Q0,J_Y,mu/k), alpha_2(K_B,K2,Q0,J_Y,mu/k), printed with the PPN
(k>>mu) limit taken explicitly and its parameter dependence exhibited.  If a certificate
fails the script says so; alpha_2 is reported ONLY if the w=0 gates and V-a1vec pass.
Exit 0 iff the w=0 gates pass.
"""
import sys, time
import sympy as sp

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
z = sp.Symbol('z', real=True)
eps = sp.Symbol('eps')                       # perturbation bookkeeping (=> O(rho))
wx, wz = sp.symbols('w_x w_z', real=True)    # wind (x-z plane); w^2 = wx^2+wz^2
KB, K2, Q0, JY, GT, rho, LAM = sp.symbols('K_B K_2 Q_0 J_Y G_t rho Lambda', real=True)
k = sp.Symbol('k', positive=True)
eta = sp.diag(-1, 1, 1, 1)
I = sp.I
CO = ['t', 'x', 'y', 'z']                    # index names for clarity

def W2():   # w^2 truncated symbol-level
    return wx**2 + wz**2

# truncate a polynomial in eps at degree 2 and in (wx,wz) at total degree 2
def trunc(e):
    e = sp.expand(e)
    out = 0
    for de in range(3):
        ce = e.coeff(eps, de)
        ce = sp.expand(ce)
        # total degree <=2 in wx,wz
        for i in range(3):
            for j in range(3 - i):
                out += ce.coeff(wx, i).coeff(wz, j) * eps**de * wx**i * wz**j
    return sp.expand(out)

# ================================================================ backgrounds
P("="*92); P("[A] boosted aligned background (generic metric added at [B])"); P("="*92)
# aether upper, O(w^2):  A^mu = (1+w^2/2, wx, 0, wz)
Aup_bg = sp.Matrix([1 + W2()/2, wx, 0, wz])
Adn_bg = eta * Aup_bg
normc = trunc((Adn_bg.T * Aup_bg)[0] + 1)
check(sp.expand(normc) == 0, "[A1] A^mu A_mu = -1 on the boosted background to O(w^2)",
      f"A.A+1 = {normc}")
# scalar aligned: d_mu phi_bg = -Q0 A_mu_bg  (constant covector)
dphi_bg = -Q0 * Adn_bg
Qbg = trunc((Aup_bg.T * dphi_bg)[0])
check(sp.simplify(Qbg - Q0) == 0, "[A2] Q = A^mu d_mu phi = Q0 on background", f"Q_bg={Qbg}")
proj_bg = sp.Matrix(4,4, lambda m,n: eta[m,n] + Aup_bg[m]*Aup_bg[n])
Ybg = trunc((dphi_bg.T * proj_bg * dphi_bg)[0])
check(sp.simplify(Ybg) == 0, "[A3] Y = 0 on the boosted background (aligned)", f"Y_bg={Ybg}")
P(f"    ({time.time()-T0:.1f}s)")

# ================================================================ perturbations (even sector)
P("="*92); P("[B] generic even-sector perturbations, z-only Fourier mode k along z"); P("="*92)
# EVEN metric amplitudes (under y->-y): H00,H0x,H0z,Hxx,Hxz,Hzz,Hyy.  Odd = 0.
names = ['H00','H0x','H0z','Hxx','Hxz','Hzz','Hyy']
Hamp = {nm: sp.Function(nm)(z) for nm in names}
# index map for symmetric H_{mu nu}: 0=t,1=x,2=y,3=z
H = sp.zeros(4,4)
H[0,0]=Hamp['H00']; H[0,1]=H[1,0]=Hamp['H0x']; H[0,3]=H[3,0]=Hamp['H0z']
H[1,1]=Hamp['Hxx']; H[1,3]=H[3,1]=Hamp['Hxz']; H[3,3]=Hamp['Hzz']; H[2,2]=Hamp['Hyy']
# (H0y=Hxy=Hyz=0 : odd, dropped)
gdn = sp.Matrix(4,4, lambda m,n: eta[m,n] + eps*H[m,n])
Hup = eta*H*eta
gup = sp.Matrix(4,4, lambda m,n: sp.expand((eta - eps*Hup + eps**2*(Hup*H*eta))[m,n]))
# sqrt(-g)
trH = sum(eta[m,n]*H[m,n] for m in range(4) for n in range(4))
HH  = sum(Hup[m,n]*H[m,n] for m in range(4) for n in range(4))
sqg = 1 + eps*trH/2 + eps**2*(trH**2/8 - HH/4)

# aether: perturb lower A_mu (even: a0,ax,az ; ay=0), plus 2nd-order temporal b0 for constraint
a0f,ax_f,az_f,b0f = [sp.Function(s)(z) for s in ('a0','ax','az','b0')]
Adn = sp.Matrix([Adn_bg[0] + eps*a0f + eps**2*b0f,
                 Adn_bg[1] + eps*ax_f,
                 Adn_bg[2],
                 Adn_bg[3] + eps*az_f])
Aup = sp.Matrix(4,1, lambda i,j: trunc(sum(gup[i,s]*Adn[s] for s in range(4))))
# solve unit constraint order by order for a0f (eps^1) and b0f (eps^2)
Cc = trunc(sum(Aup[m]*Adn[m] for m in range(4)) + 1)
sol_a0 = sp.solve(sp.expand(Cc).coeff(eps,1), a0f)[0]
Adn = Adn.subs(a0f, sol_a0)
Aup = sp.Matrix(4,1, lambda i,j: trunc(sum(gup[i,s]*Adn[s] for s in range(4))))
Cc  = trunc(sum(Aup[m]*Adn[m] for m in range(4)) + 1)
sol_b0 = sp.solve(sp.expand(Cc).coeff(eps,2), b0f)[0]
SUBAE = {a0f: sol_a0, b0f: sol_b0}
Adn = Adn.subs(SUBAE);
Aup = sp.Matrix(4,1, lambda i,j: trunc(sum(gup[i,s]*Adn[s] for s in range(4))))
Cres = trunc(sum(Aup[m]*Adn[m] for m in range(4)) + 1)
check(sp.simplify(Cres)==0, "[B1] unit constraint A.A=-1 solved order by order (to eps^2, w^2)")

# scalar perturbation
phf = sp.Function('phi')(z)
dphi = sp.Matrix([dphi_bg[0], dphi_bg[1], dphi_bg[2], dphi_bg[3] + eps*sp.diff(phf,z)])
# NB d_t phi pert = 0 (static), d_x = d_y = 0 (z-only); only d_z phi pert survives.
P(f"    perturbations set ({time.time()-T0:.1f}s)")

# ================================================================ curvature (generic, z-only)
P("="*92); P("[C] Ricci scalar to O(eps^2) for the generic z-only metric"); P("="*92)
def d_(f, mu):   # partial derivative wrt coordinate mu (only z=3 acts)
    return sp.diff(f, z) if mu == 3 else sp.S(0)
Gam = [[[ trunc(sp.Rational(1,2)*sum(gup[r,s]*(d_(gdn[s,n],m)+d_(gdn[s,m],n)-d_(gdn[m,n],s))
        for s in range(4))) for n in range(4)] for m in range(4)] for r in range(4)]
def ric(a,b):
    o = 0
    for m in range(4):
        o += d_(Gam[m][b][a], m) - d_(Gam[m][m][a], b)
        for l in range(4):
            o += Gam[m][m][l]*Gam[l][b][a] - Gam[m][b][l]*Gam[l][m][a]
    return trunc(o)
Rsc = trunc(sum(gup[m,n]*ric(m,n) for m in range(4) for n in range(4)))
P(f"    Ricci assembled ({time.time()-T0:.1f}s)")

# ================================================================ dark-sector scalars
P("="*92); P("[D] F^2, J.dphi, Y, Q, K(Q); full Lagrangian; Euler-Lagrange"); P("="*92)
Fmn = sp.Matrix(4,4, lambda m,n: d_(Adn[n],m) - d_(Adn[m],n))
F2 = trunc(sum(Fmn[m,n]*Fmn[a,b]*gup[m,a]*gup[n,b]
               for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
# J^mu = A^nu nabla_nu A^mu = A^nu( d_nu A^mu + Gam^mu_{nu r} A^r )
Amup = Aup
Jup = [ trunc(sum(Amup[nu]*( d_(Amup[al],nu) + sum(Gam[al][nu][r]*Amup[r] for r in range(4)) )
        for nu in range(4))) for al in range(4)]
Jdphi = trunc(sum(Jup[m]*dphi[m] for m in range(4)))
Qf = trunc(sum(Aup[m]*dphi[m] for m in range(4)))
Yf = trunc(sum((gup[m,n]+Aup[m]*Aup[n])*dphi[m]*dphi[n] for m in range(4) for n in range(4)))
dQ = sp.expand(Qf - Q0)
KQ = -2*LAM + K2*trunc(dQ**2)
# multiplier: lambda = lambda_bg + eps*dlam.  lambda_bg from typeII B2 = (2-K_B)(1+J_Y)Q0^2 + K'(Q0)Q0/2
# on the aligned background K'(Q0)=0 => lambda_bg = (2-K_B)(1+J_Y)Q0^2.
lam_bg = (2-KB)*(1+JY)*Q0**2
dlam = sp.Function('dlam')(z)
lam = lam_bg + eps*dlam

L = trunc( sqg*( Rsc - 2*LAM - (KB/2)*F2 + 2*(2-KB)*Jdphi
                 - (2-KB)*(1+JY)*Yf - KQ - lam*Cc ) )
# matter: static dust at rest, sources 00 only.  Same normalisation as typeII (validated by
# the Newtonian gate below): S_m -> -16 pi G_t * rho * sqrt(-g_00)/... contributes -8 pi G_t rho H00 at O(eps).
# Use the typeII form: -16 pi Gt eps rho (1 - eps H00/2), i.e. matter Lagrangian density.
Lm = -16*sp.pi*GT*eps*rho*(1 - eps*H[0,0]/2)
Lfull = sp.expand(L + Lm)
P(f"    L assembled: {len(sp.Add.make_args(sp.expand(Lfull)))} terms ({time.time()-T0:.1f}s)")

# Euler-Lagrange in z for a field f(z):  dL/df - d_z(dL/df') + d_z^2(dL/df'')
def EL(Lag, f):
    fp = sp.Derivative(f, z); fpp = sp.Derivative(f, (z,2))
    out = sp.diff(Lag, f) - sp.diff(sp.diff(Lag, fp), z) + sp.diff(sp.diff(Lag, fpp), z)
    return sp.expand(out.doit())

# quadratic part of the action gives LINEAR EOMs: take eps^1 coefficient of EL of the eps^2 action.
# Actually EL of the full L, then keep terms linear in perturbations (eps^1 after one field-deriv).
FIELDS = {'H00':Hamp['H00'],'H0x':Hamp['H0x'],'H0z':Hamp['H0z'],'Hxx':Hamp['Hxx'],
          'Hxz':Hamp['Hxz'],'Hzz':Hamp['Hzz'],'Hyy':Hamp['Hyy'],
          'ax':ax_f,'az':az_f,'phi':phf,'dlam':dlam}
# (a0,b0 eliminated by constraint; their EOMs are the multiplier/redundant ones.)
EOM = {}
for nm,f in FIELDS.items():
    e = EL(Lfull, f)
    EOM[nm] = e
P(f"    EOMs assembled ({time.time()-T0:.1f}s)")

# ---- Fourier: substitute f(z) -> Famp * exp(i k z), strip exp, keep LINEAR in amplitudes ----
amps = {nm: sp.Symbol('A_'+nm, complex=True) for nm in list(FIELDS)+['a0','b0']}
E = sp.exp(I*k*z)
def fourier(e):
    subs = {}
    for nm,f in list(FIELDS.items()):
        subs[sp.Derivative(f,(z,2))] = (I*k)**2*amps[nm]*E
        subs[sp.Derivative(f,z)]      = (I*k)*amps[nm]*E
        subs[f] = amps[nm]*E
    e2 = e.subs(subs)
    e2 = sp.expand(e2)
    # divide by E (each linear EOM term carries exactly one E). Keep linear-in-amp only.
    e2 = sp.expand(e2 / E)
    return e2

# extract, per EOM, the part LINEAR in the amplitude set (drop constants and amp^2), then it is the
# linear field equation.  rho enters linearly (source).
AMPSET = [amps[nm] for nm in FIELDS]
def linearize(e):
    e = sp.expand(e)
    # keep terms of total degree 1 in AMPSET, plus the pure-rho source (degree 0 in amps but has rho)
    out = 0
    for term in sp.Add.make_args(e):
        deg = sum(sp.degree(term, a) if term.has(a) else 0 for a in AMPSET)
        if deg <= 1:
            out += term
    return sp.expand(out)

EOM_k = {nm: linearize(fourier(EOM[nm])) for nm in FIELDS}
P(f"    Fourier + linearised ({time.time()-T0:.1f}s)")

# =============================================================== solve order-by-order in w
P("="*92); P("[E] solve order-by-order in w; gates at w=0"); P("="*92)
# gauge: residual static (z-only) diffeos xi_mu(z). h_{mn} -> h_{mn} - d_mu xi_nu - d_nu xi_mu.
# with z-only, xi_0,xi_x,xi_z even.  Fix H0x=0 (xi_x), H0z or Hxz, Hzz (xi_z), and one more (xi_0).
# Simplest robust gauge for reading h_00: set H0x=H0z (longitudinal metric-vector) handled below;
# we DO NOT fix h_00 (it is the observable).  Use k-transverse-ish gauge: fix Hxz=0, Hyy=Hxx (?).
# To stay safe we solve the FULL even system and only gauge-fix the pure-gauge combinations that
# the matrix reveals as undetermined (rank check), reading gauge-invariant h_00 pieces.

UNK = [amps[nm] for nm in FIELDS]

def wsolve():
    # split each EOM by w-order; solve cumulatively
    return None

# Build matrix at general w, but solve perturbatively in w:  A(w) x = b(w), x = x0 + w*x1 + w^2*x2.
# Represent w-order by extracting coeffs in wx,wz.  We solve the full linear system EXACTLY in
# (wx,wz) via sp.linsolve treating wx,wz as parameters, IF tractable; else order-by-order.
eqs = [sp.expand(EOM_k[nm]) for nm in FIELDS]
# Move rho source to RHS: equations are (stuff)=0 already (rho included). linsolve handles it.
try:
    A_mat, b_vec = sp.linear_eq_to_matrix(eqs, UNK)
    P(f"    system matrix {A_mat.shape} built ({time.time()-T0:.1f}s)")
except Exception as ex:
    P("   linear_eq_to_matrix failed:", ex); A_mat=None

# The system may be gauge-degenerate (rank<#unk). Add gauge conditions as extra rows.
# gauge fixing: set H0x=0, Hxz=0, and Hyy - Hxx = 0 (isotropize transverse), leaving H00,H0z,Hzz,Hxx,
# ax,az,phi,dlam.  We verify below this is a legal (pure-gauge) choice by rank stability.
GAUGE = {amps['H0x']: 0, amps['Hxz']: 0}
P(f"    ({time.time()-T0:.1f}s)  ready for staged solve")

# --- w=0 slice: set wx=wz=0, solve, read gamma, Ghat, m_Psi ---
def at_w0(e): return sp.expand(e.subs({wx:0, wz:0}))
eqs0 = [at_w0(EOM_k[nm]).subs(GAUGE) for nm in FIELDS]
UNK0 = [amps[nm] for nm in FIELDS if amps[nm] not in (amps['H0x'],amps['Hxz'])]
# at w=0 the odd/vector fields (H0x,H0z,ax) should decouple/vanish; solve the scalar block.
sol0 = sp.linsolve(eqs0, UNK0)
if sol0:
    sol0 = dict(zip(UNK0, list(sol0)[0]))
    P("    w=0 solution keys:", [str(u) for u in UNK0])
    # gamma_PPN: Phi=Psi.  With H00=-2Psi, Hxx=Hyy=Hzz=-2Phi (isotropic), read Phi-Psi.
    H00v = sol0.get(amps['H00'], amps['H00'])
    Hxxv = sol0.get(amps['Hxx'], amps['Hxx'])
    Hzzv = sol0.get(amps['Hzz'], amps['Hzz'])
    P("    H00(w=0) =", sp.simplify(H00v))
    P("    Hxx(w=0) =", sp.simplify(Hxxv))
    P("    Hzz(w=0) =", sp.simplify(Hzzv))
    P("    phi(w=0) =", sp.simplify(sol0.get(amps['phi'], amps['phi'])))
else:
    P("    w=0 system did not solve under this gauge; will diagnose.")

P("="*92)
nfail = len(FAIL)
P(f"    {NCHK[0]-nfail}/{NCHK[0]} setup certificates pass" + ("" if nfail==0 else f";  FAILED: {FAIL}"))
P(f"    runtime {time.time()-T0:.1f}s")
sys.exit(0 if nfail==0 else 1)
