#!/usr/bin/env python3
"""
ROUTE 1 -- DIRECT boosted PPN solve for AeST preferred-frame alpha_2 (FAST).
Full DYNAMICAL linearised gravity. Fourier quadratic-form -> perturbative-in-w solve.

S2 = S_EH2[h] + S_AeST2[h,a,varphi] + S_int[h;rho], Minkowski, boosted aether
A^mu=(1+w^2/2, w,0,0), d_mu phi_bg=-Q0 A_mu. Stationary (d_t=0), q=(0,qx,qy,0).

alpha_2 = D / C_N :
  C_N = coeff of rho/q^2 in h00 at w=0            (=2U)
  D   = coeff of rho*w^2*qx^2/q^4 in h00 at O(w^2)
(from g00^PF=-(a1-a2-a3)w^2U - a2 w^iw^j U_ij, U_ij=dij U-2qiqj U/q^2
 => coeff of (qx^2/q^2)w^2 U in g00 is 2 a2, U=h00^(0)/2 => a2=D/C_N).
EH sign fixed by pure-GR check.
"""
import sympy as sp

KB, lam, Q0, K2, w = sp.symbols('K_B lambda_s Q0 K2 w', real=True)
qx, qy, rho, k0 = sp.symbols('q_x q_y rho k0', real=True)   # k0=omega regulator
kap=sp.Integer(1)
I=sp.I
eta=sp.diag(-1,1,1,1)

# amplitudes (complex) : A_* and their conjugates Ac_*
names=[f'h{m}{n}' for m in range(4) for n in range(m,4)]+['a1','a2','a3','vf']
A ={nm:sp.Symbol('A_'+nm)  for nm in names}
Ac={nm:sp.Symbol('Ac_'+nm) for nm in names}
def key(m,n): return f'h{min(m,n)}{max(m,n)}'

# plane wave; work to O(w^2), so keep A0bg series
E=sp.Symbol('E')          # e^{i q.x}; Ei=1/E its conjugate
Ei=sp.Symbol('Ei')
kv=[k0,qx,qy,0]           # lower wavevector; k0=omega regulator (->0 at end)
# field value and derivatives as functions returning (value)  with E,Ei symbolic
def fld(nm):    return A[nm]*E + Ac[nm]*Ei
def dfld(nm,mu):return sp.I*kv[mu]*A[nm]*E - sp.I*kv[mu]*Ac[nm]*Ei
# metric
def h(m,n): return fld(key(m,n))
def dh(m,n,mu): return dfld(key(m,n),mu)
hmat=sp.Matrix(4,4,lambda m,n:h(m,n))

# ---- backgrounds (O(w^2)) ----
A0bg=1+w**2/2
Abg_up=[A0bg,w,0,0]; Abg_low=[-A0bg,w,0,0]
dphibg=[-Q0*Abg_low[mu] for mu in range(4)]

# ---- aether A^0 perturbation from unit norm (linear) ----
# g_{mn}A^mA^n=-1 ; A^m = Abg + pert.  Linear: 2 Abg_low_m dA^m + h_{mn}Abg^mAbg^n =0
# dA^i = (a1,a2,a3); dA^0 = P0. Solve for P0.
aup_pert=[sp.Symbol('P0'),fld('a1'),fld('a2'),fld('a3')]
P0=sp.Symbol('P0')
lin = 2*sum(Abg_low[m]*aup_pert[m] for m in range(4)) \
      + sum(hmat[m,n]*Abg_up[m]*Abg_up[n] for m in range(4) for n in range(4))
P0sol=sp.solve(sp.expand(lin),P0)[0]
def Aup(mu):
    if mu==0: return A0bg+P0sol
    return Abg_up[mu]+[0,fld('a1'),fld('a2'),fld('a3')][mu]
def _dexpr(expr,nu):
    # derivative wrt coord nu: E->i k_nu E, Ei-> -i k_nu Ei
    return sp.expand(expr.subs({E:sp.I*kv[nu]*E, Ei:-sp.I*kv[nu]*Ei},simultaneous=True))
def dAup(mu,nu):
    if mu==0: return _dexpr(P0sol,nu)
    return dfld(['','a1','a2','a3'][mu],nu)
# A_low_m = g_{mn}A^n
def Alow(m):
    return sum((eta[m,n]+hmat[m,n])*Aup(n) for n in range(4))
def dAlow(m,nu):
    return sum(eta[m,n]*dAup(n,nu) for n in range(4)) \
         + sum(dh(m,n,nu)*Aup(n) + hmat[m,n]*dAup(n,nu) for n in range(4))

# scalar gradient lower
def dphi(mu): return dphibg[mu]+dfld('vf',mu)

# ---- AeST Lagrangian (flat contractions ok to O(pert^2)) ----
_ampsyms=[A[nm] for nm in names]+[Ac[nm] for nm in names]
_s=sp.Symbol('_s')
def SL(expr):   # keep part LINEAR in perturbation amplitudes (drop bg & pert^2)
    e=sp.expand(expr).subs({a_:_s*a_ for a_ in _ampsyms})
    return sp.expand(sp.expand(e).coeff(_s,1))
Fmn=sp.Matrix(4,4,lambda a_,b_: SL(dAlow(b_,a_)-dAlow(a_,b_)))
Bi=[SL(dphi(i)+Q0*Alow(i)) for i in range(4)]
Ei_=[Fmn[0,i] for i in range(4)]
dQ=SL(sum(Aup(m)*dphi(m) for m in range(4))-Q0)
Lmax=-(KB/2)*sum(eta[a_,a_]*eta[b_,b_]*Fmn[a_,b_]**2 for a_ in range(4) for b_ in range(4))
EdotB=sum(Ei_[i]*Bi[i] for i in range(1,4))
B2=sum(Bi[i]**2 for i in range(1,4))
L_AeST=Lmax+2*(2-KB)*EdotB-(2-KB)*(1+lam)*B2+2*K2*dQ**2

# ---- EH (Fierz-Pauli, sign sEH) ----
sEH=sp.Symbol('sEH')
htr=sum(eta[m,m]*h(m,m) for m in range(4))
dhtr=lambda nu: sum(eta[m,m]*dh(m,m,nu) for m in range(4))
hup=lambda m,n: sum(eta[m,a]*eta[n,b]*h(a,b) for a in range(4) for b in range(4))
dhup=lambda m,n,nu: sum(eta[m,a]*eta[n,b]*dh(a,b,nu) for a in range(4) for b in range(4))
divh=lambda n,: None
def L_EH():
    # de Donder / harmonic gauge-fixed EH quadratic (invertible box operator):
    #   -(1/2) d_l h_{mn} d^l h^{mn} + (1/4) d_l h d^l h
    T1=-sp.Rational(1,2)*sum(dh(m,n,l)*eta[l,l]*dhup(m,n,l)
                             for m in range(4) for n in range(4) for l in range(4))
    T4=sp.Rational(1,4)*sum(dhtr(l)*eta[l,l]*dhtr(l) for l in range(4))
    return (sEH/(2*kap))*(T1+T4)

L_int=sp.Rational(1,2)*h(0,0)*(rho*E+rho*Ei)   # source mode rho

print("assembling L ...")
L=sp.expand(L_EH()+L_AeST+L_int)
# constant (x-indep) part: E*Ei=1 ; keep terms with equal powers of E and Ei
L=L.subs(E*Ei,1)
# after subs, drop remaining terms containing E or Ei (net phase != 0)
Lc=sp.expand(L)
Lc=Lc.subs({E:0,Ei:0})   # removes any surviving pure-phase terms
print("constant part built; terms:",len(Lc.as_ordered_terms()))

# ---- EOMs: d<L>/dAc_nm = 0 ----
Avars=[A[nm] for nm in names]
Acvars=[Ac[nm] for nm in names]
eqs=[sp.expand(sp.diff(Lc,Ac[nm])) for nm in names]

# build linear system M A = b  (in A vars); source from rho
rows=[]; b=[]
for e in eqs:
    rows.append([sp.expand(e).coeff(av) for av in Avars])
    r=sp.expand(e)
    for av in Avars: r=r.subs(av,0)
    b.append(-r)          # r is source term (contains rho)
M=sp.Matrix(rows); bvec=sp.Matrix(b)
print("system:",M.shape)

# ---- PURE-GR sign check (h-subblock; aether off & =0) ----
print("="*60)
hidx=[i for i,nm in enumerate(names) if nm.startswith('h')]
hnames=[names[i] for i in hidx]
sub_off={KB:0,K2:0,Q0:0,w:0}
aoff={A[nm]:0 for nm in ['a1','a2','a3','vf']}
for sEHval in (1,-1):
    Mg=sp.Matrix([[M[i,j].subs(sEH,sEHval).subs(sub_off) for j in hidx] for i in hidx])
    bg=sp.Matrix([bvec[i].subs(sEH,sEHval).subs(sub_off) for i in hidx])
    try:
        sol=Mg.solve(bg)
        d0={nm:sp.simplify(sol[k]) for k,nm in enumerate(hnames)}
        print(f"sEH={sEHval}: h00={d0['h00']} h11={d0['h11']} h22={d0['h22']} h33={d0['h33']} h01={d0['h01']} h12={d0['h12']}")
    except Exception as ex:
        print(f"sEH={sEHval}: singular/FAIL ({ex})")

# ============ FULL BOOSTED SOLVE (finite w, full-rank, static k0=0) ============
# At any w!=0 the omega=0 zero mode is LIFTED (rank 14, consistent solve).
# h00(w,t)*q^2 = C_N + w^2 (f0 + f2 t) + O(w^4),  t=qx^2/q^2.  alpha2 = f2/C_N.
import numpy as np
h00i=names.index('h00')
Mf=sp.Matrix(M.subs(sEH,1)); bf=sp.Matrix(bvec.subs(sEH,1))
args=(KB,lam,K2,Q0,qx,qy,rho,k0,w)
fM=sp.lambdify(args,Mf,'numpy'); fb=sp.lambdify(args,bf,'numpy')

def h00q2(KBv,lamv,K2v,Q0v,qxv,qyv,wv):
    p=(KBv,lamv,K2v,Q0v,qxv,qyv,1.0,0.0,wv)
    Mn=np.array(fM(*p),dtype=complex); bn=np.array(fb(*p),dtype=complex).reshape(-1)
    x,_,rk,sv=np.linalg.lstsq(Mn,bn,rcond=None)
    q2=qxv**2+qyv**2
    return (x[h00i]*q2).real, float(np.max(np.abs(Mn@x-bn))), int(np.linalg.matrix_rank(Mn))

def slope_CN(KBv,lamv,K2v,Q0v,wv,Qmag,ndir=7):
    ts=[]; gs=[]; resmax=0; rkmin=99
    for th in np.linspace(0.2,1.37,ndir):
        qxv=Qmag*np.cos(th); qyv=Qmag*np.sin(th)
        g,res,rk=h00q2(KBv,lamv,K2v,Q0v,qxv,qyv,wv)
        ts.append((qxv**2)/(qxv**2+qyv**2)); gs.append(g); resmax=max(resmax,res); rkmin=min(rkmin,rk)
    ts=np.array(ts); A=np.vstack([np.ones_like(ts),ts]).T
    (b0_,slope),_,_,_=np.linalg.lstsq(A,np.array(gs),rcond=None)
    fitres=np.max(np.abs(A@np.array([b0_,slope])-np.array(gs)))
    return b0_,slope,resmax,rkmin,fitres

def alpha2_num(KBv,lamv,K2v=1.0,Q0v=1.0):
    Qmag=max(1e6, 1e3*np.sqrt(max(1.0,lamv))*Q0v)   # q >> mass ~ sqrt(lam)*Q0
    out=[]
    for wv in [3e-2,1e-2]:
        b0_,slope,resmax,rkmin,fitres=slope_CN(KBv,lamv,K2v,Q0v,wv,Qmag)
        out.append((wv,b0_,slope,resmax,rkmin,fitres))
    CNiso=out[-1][1]
    f2a=out[0][2]/out[0][0]**2; f2b=out[1][2]/out[1][0]**2
    return CNiso, f2a/0.5, f2b/0.5, out[-1][3], out[-1][4], out[-1][5]

print("="*60); print("NUMERIC alpha_2(K_B,lam)  finite-w full-rank solve [K2=Q0=1]")
print(f"{'K_B':>6} {'lam':>9} {'~iso':>9} {'a2(w=.03)':>13} {'a2(w=.01)':>13} {'res':>8} {'rk':>3} {'fitr':>8}")
for KBv in [0.05,0.1,0.25,0.5,0.9,1.0,1.3,1.7,1.95]:
    for lamv in [1.0,100.0,1e4,1e6]:
        try:
            CN,a2a,a2b,res,rk,fr=alpha2_num(KBv,lamv)
            print(f"{KBv:6.3f} {lamv:9.1e} {CN:9.5f} {a2a:13.6e} {a2b:13.6e} {res:8.1e} {rk:3d} {fr:8.1e}")
        except Exception as ex:
            print(f"{KBv:6.3f} {lamv:9.1e}  FAIL {ex}")
