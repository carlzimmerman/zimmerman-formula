#!/usr/bin/env python3
"""
decisive_reduction.py  -- THE decisive object for FC-KH.

Frozen-background quadratic khronon action on a locally-constant static MOND
background, unitary gauge, CORRECT FC-KH ADM convention:

  L = N sqrt(gamma) [ (1-beta) K_ij K^ij - (1+lambda) K^2 + ^3R + f_FC(a) ]
      (overall M_Pl^2/2 or 1/16piG drops out of speeds/signs-of-ratios; we keep
       the bracket, whose Hessian signs ARE physical.)

Background: gamma_ij = delta_ij, K_ij = 0 (static), a_i = D_i lnN = gbar zhat,
  gbar = a0*y0.  Perturbations (unitary gauge, residual spatial diff fixes E=0):
     N = e^{phi},  N_i = d_i B,  gamma_ij = e^{2 psi} delta_ij.
  a_i = gbar zhat + d_i phi  (since a_i = d_i lnN, lnN = gbar z + phi).

Acceleration term is the PHYSICAL f_FC = a0^2 F(y), F(y)=2y^2-2(2-alpha)W(y),
  W=y^2/2+(1+y)e^{-y}-1.  In the expansion the potential enters through its value
  and y-derivatives at y0: W0=F(y0), W1=F'(y0), W2=F''(y0).

Method:
  (1) Expand L to 2nd order in (phi,B,psi) -- machinery cross-validated in
      wf_flat_validation.py against Bonetti-Barausse PRD91,084053 Eq.(14).
  (2) Build the HERMITIAN Fourier quadratic form H(omega,kx,kz) by the
      period-average method (so the sign of every eigenvalue is physical).
  (3) phi (lapse) and B (shift) are NON-DYNAMICAL (H_cc block is omega-free).
      Integrate them out by the Schur complement:  G = H_SS - H_Sc H_cc^{-1} H_cS.
      G(omega,k) = A omega^2 - B_par kz^2 - B_perp kx^2 - m^2   (2-deriv => polynomial).
  (4) Read A (kinetic), B_par, B_perp (gradient), m^2 (mass).  c_par^2=B_par/A,
      c_perp^2=B_perp/A.  KILL CRITERION: A>0 AND B_par>0 AND B_perp>0 through
      the transition 0.5<~y0<~2 on the alpha=2beta branch.

CONSISTENCY CHECKS built in:
  * pure-quadratic accel f=alpha a^2 (F=alpha y^2, W1=2*alpha*y0, W2=2*alpha,
    W0=alpha*y0^2) must give c_s^2 = (alpha-2)(beta+lambda)/[alpha(beta-1)(2+beta+3lambda)]
    (BB Eq.14) INDEPENDENT of y0, and c_T^2=1/(1-beta).
"""
import sympy as sp

# ----- symbols -----
t,xx,zz = sp.symbols('t xx zz', real=True)
beta,lam,a0 = sp.symbols('beta lambda a0', positive=True)
y0 = sp.symbols('y0', positive=True)
W0,W1,W2 = sp.symbols('W0 W1 W2', real=True)   # F(y0), F'(y0), F''(y0)
gbar = a0*y0

phi=sp.Function('phi'); Bf=sp.Function('B'); Psi=sp.Function('Psi')
ph=phi(t,xx,zz); Bb=Bf(t,xx,zz); Ps=Psi(t,xx,zz)
dt=lambda f: sp.diff(f,t); dx=lambda f: sp.diff(f,xx); dz=lambda f: sp.diff(f,zz)

# ---- extrinsic curvature K_ij^(1) = dPsi/dt delta_ij - d_i d_j B ----
def dd(i,j,f):
    D={'x':dx,'y':(lambda q: q*0),'z':dz}; return D[i](D[j](f))
K1={(i,j):((dt(Ps) if i==j else 0)-dd(i,j,Bb)) for i in 'xyz' for j in 'xyz'}
KK  = sum(K1[(i,j)]**2 for i in 'xyz' for j in 'xyz')
Ktr = sum(K1[(i,i)] for i in 'xyz')
Ksec = (1-beta)*KK - (1+lam)*Ktr**2        # <-- CORRECT FC-KH convention (1-beta)

# ---- ^3R sector (2nd order), measure factor e^{phi+3psi} ----
lap=lambda f: dx(dx(f))+dz(dz(f))
R3_1=-4*lap(Ps); R3_2=8*Ps*lap(Ps)-2*(dx(Ps)**2+dz(Ps)**2)
Rsec=R3_2+(ph+3*Ps)*R3_1

# ---- acceleration sector: a^2 = e^{-2psi}[(gbar+d_z phi)^2 + (d_x phi)^2] ----
a2_1 = 2*gbar*dz(ph) - 2*gbar**2*Ps
a2_2 = dx(ph)**2 + dz(ph)**2 - 4*gbar*Ps*dz(ph) + 2*gbar**2*Ps**2
delta_1 = a2_1/(2*gbar*a0)                       # delta y (1st order)
delta_2 = a2_2/(2*gbar*a0) - a2_1**2/(8*gbar**3*a0)
W_eps1 = W1*delta_1
W_eps2 = W1*delta_2 + sp.Rational(1,2)*W2*delta_1**2
Accel = a0**2*( W_eps2 + (ph+3*Ps)*W_eps1 + (ph+3*Ps)**2*sp.Rational(1,2)*W0 )

L2 = sp.expand(Ksec + Rsec + Accel)

# ============ Hermitian Fourier quadratic form via period-average ============
kx,kz,w = sp.symbols('k_x k_z omega', real=True)
I = sp.I
P,Bc,S = sp.symbols('P B_c S')                 # complex amplitudes
Pb,Bcb,Sb = sp.symbols('Pb B_cb Sb')           # their conjugates
E = sp.exp(I*(kx*xx + kz*zz - w*t))

# each real field -> (1/2)(v E + v* E^*)
subs_field = {
    ph : sp.Rational(1,2)*(P*E + Pb/E),
    Bb : sp.Rational(1,2)*(Bc*E + Bcb/E),
    Ps : sp.Rational(1,2)*(S*E + Sb/E),
}
def to_fourier(expr):
    # build a simultaneous xreplace map for every Derivative node and bare field,
    # then xreplace ONCE (xreplace does not recurse into the replacement images).
    e = sp.expand(expr)
    xmap={}
    for node in e.atoms(sp.Derivative):
        base=node.expr
        if base in subs_field:
            d=subs_field[base]
            for v,n in node.variable_count:
                d=sp.diff(d,v,n)
            xmap[node]=d
    for fld,rep in subs_field.items():
        xmap[fld]=rep
    return e.xreplace(xmap)

Lf = to_fourier(L2)
Lf = sp.expand(Lf)
# period-average: keep only terms independent of xx,zz,t (E and E* fully cancel)
# i.e. drop anything still containing xx,zz,t.
Lf = Lf.rewrite(sp.exp)
Lf = sp.expand(Lf)
def avg(expr):
    expr=sp.expand(expr)
    out=0
    for term in expr.as_ordered_terms():
        if term.has(xx) or term.has(zz) or term.has(t):
            continue
        out+=term
    return out
Lavg = avg(Lf)
Lavg = sp.expand(Lavg)

# Hermitian matrix H: Lavg = (1/2) v^dagger H v with v=(P,Bc,S), v^dagger=(Pb,Bcb,Sb)
# H_ab = d^2 Lavg / d(conj_a) d(amp_b)
amps=[P,Bc,S]; conj=[Pb,Bcb,Sb]
H=sp.zeros(3,3)
for i in range(3):
    for j in range(3):
        H[i,j]=sp.simplify(sp.diff(Lavg,conj[i],amps[j]))
# Hermiticity check
herm_err=sp.simplify(H - H.conjugate().T)
print("Hermiticity max error:", sp.simplify(sp.Matrix(herm_err).norm()) if herm_err!=sp.zeros(3,3) else 0)

# ---- Schur complement: eliminate c=(phi=P, B=Bc), keep S(psi) ----
# order (P,Bc,S): cc block = indices 0,1 ; s index = 2
Hcc = H[0:2,0:2]
Hcs = H[0:2,2:3]
Hsc = H[2:3,0:2]
Hss = H[2,2]
detHcc=sp.simplify(Hcc.det())
print("\ndet H_cc (phi,B block) =", sp.factor(detHcc), "  (omega-free:", not detHcc.has(w),")")
Gred = sp.cancel(Hss - (Hsc*Hcc.inv()*Hcs)[0,0])
Gred_e = sp.expand(sp.cancel(Gred))
# kinetic coefficient A = coeff of omega^2 (verified k-independent below)
A_coef = sp.cancel(Gred_e.coeff(w,2))
print("\nA (kinetic, coeff of omega^2) =", sp.factor(A_coef), "  (k-free:", not A_coef.has(kx) and not A_coef.has(kz),")")
# omega-independent part:  G = A*omega^2 - V(kx,kz)   =>  dispersion omega^2 = V/A
Vk = sp.cancel(-(Gred_e - A_coef*w**2))
print("\nV(kx,kz) [dispersion omega^2 = V/A], factored numerator/denominator:")
Vn,Vd = sp.fraction(sp.cancel(Vk))
print("   num =", sp.factor(Vn))
print("   den =", sp.factor(Vd), "   <-- lapse-constraint operator D_lapse (carries W1=f', W2=f'')")

# ---------- IR expansion (k->0): omega^2 = m^2 + c_par^2 kz^2 + c_perp^2 kx^2 ----------
s,ex,ez = sp.symbols('s ex ez', positive=True)
Vscaled = Vk.subs({kx:s*ex, kz:s*ez})
Vser = sp.series(sp.cancel(Vscaled), s, 0, 3).removeO()
V0  = sp.cancel(Vser.subs(s,0))
V2  = sp.cancel(sp.expand(Vser).coeff(s,2))
Bpar_IR  = sp.cancel(V2.coeff(ez,2).subs({ex:0,ez:0}) if False else sp.expand(V2).coeff(ez,2).coeff(ex,0))
Bperp_IR = sp.cancel(sp.expand(V2).coeff(ex,2).coeff(ez,0))
mass2 = sp.cancel(V0)
A_over = A_coef
cpar2_IR  = sp.cancel(Bpar_IR/A_over)
cperp2_IR = sp.cancel(Bperp_IR/A_over)
print("\n----- IR (k->0) -----")
print("m^2_eff = V0/... (=A*omega^2|k=0) : V0 =", sp.factor(mass2), "  => m_eff^2 = V0/A =", sp.factor(sp.cancel(mass2/A_over)))
print("B_par,IR  (coeff kz^2 in V) =", sp.factor(Bpar_IR))
print("B_perp,IR (coeff kx^2 in V) =", sp.factor(Bperp_IR))
print("c_par^2,IR  = B_par,IR /A =", sp.factor(cpar2_IR))
print("c_perp^2,IR = B_perp,IR/A =", sp.factor(cperp2_IR))

# ---------- UV expansion (k->inf): omega^2/k^2 ----------
cpar2_UV  = sp.cancel(sp.limit(Vk.subs({kx:0})/kz**2, kz, sp.oo)/A_over)
cperp2_UV = sp.cancel(sp.limit(Vk.subs({kz:0})/kx**2, kx, sp.oo)/A_over)
print("\n----- UV (k->inf) -----")
print("c_par^2,UV  =", sp.factor(cpar2_UV))
print("c_perp^2,UV =", sp.factor(cperp2_UV))

import pickle
pickle.dump({'A':sp.srepr(A_coef),'Vk':sp.srepr(Vk),
             'Bpar_IR':sp.srepr(Bpar_IR),'Bperp_IR':sp.srepr(Bperp_IR),'mass2':sp.srepr(mass2),
             'cpar2_IR':sp.srepr(cpar2_IR),'cperp2_IR':sp.srepr(cperp2_IR),
             'cpar2_UV':sp.srepr(cpar2_UV),'cperp2_UV':sp.srepr(cperp2_UV),
             'H':sp.srepr(H)}, open('decisive_symbols.pkl','wb'))
print("\nsaved decisive_symbols.pkl")

# ================= CONSISTENCY CHECK 1: pure quadratic f=alpha a^2 =================
print("\n"+"="*72)
print("CHECK 1: pure-quadratic accel f=alpha a^2  => must reproduce BB Eq(14), y0-free")
print("="*72)
al=sp.symbols('alpha', positive=True)
# F=alpha y^2 => W0=alpha y0^2, W1=2 alpha y0, W2=2 alpha
subq={W0:al*y0**2, W1:2*al*y0, W2:2*al}
BB14=(al-2)*(beta+lam)/(al*(beta-1)*(2+beta+3*lam))
print("BB Eq(14)   =", sp.factor(BB14))
for nm,expr in [('c_par^2,IR',cpar2_IR),('c_perp^2,IR',cperp2_IR),
                ('c_par^2,UV',cpar2_UV),('c_perp^2,UV',cperp2_UV)]:
    q=sp.simplify(expr.subs(subq))
    print(f"  {nm}(quad) = {sp.factor(q)}   ; minus BB14 = {sp.simplify(q-BB14)}")
print("m^2(quad) =", sp.factor(sp.cancel(mass2.subs(subq))), " (expect 0: pure-quadratic Minkowski-like, no Jeans mass)")
