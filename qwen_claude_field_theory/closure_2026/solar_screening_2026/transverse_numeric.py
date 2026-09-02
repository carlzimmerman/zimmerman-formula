import sympy as sp, pickle, os
# reuse the transverse cache (b along x2, perp k); numeric b -> fast
CACHE='L2dc_screen_transverse.pkl'
if not os.path.exists(CACHE): raise SystemExit("no transverse cache")
L2dc=pickle.load(open(CACHE,'rb'))
eps,wb=sp.symbols('eps w_b',positive=True);KB,Q0,JY=sp.symbols('K_B Q_0 J_Y',real=True)
b=sp.symbols('b',real=True);w1,w2,w3=sp.symbols('w1 w2 w3',real=True);GT,LAM=sp.symbols('G_t Lambda',real=True)
kx=sp.symbols('k_x',real=True)
def S(t):return sp.Symbol(t)
names=['Psi','Phi','B2','B3','s22','s23','a1','a2','a3','chi']
KETS=[S(n+'k') for n in names];BRAS=[S(n+'b') for n in names];Rk=S('rhok')
eq={A:sp.expand(sp.diff(L2dc,A)) for A in BRAS}
CONJ=lambda e:sp.expand(e).xreplace({sp.I:-sp.I});NF=len(KETS)
def lin(eqs,unk):
    Am,bb=sp.linear_eq_to_matrix(eqs,unk);s=list(sp.linsolve((Am,bb),unk));return dict(zip(unk,s[0])) if s else None
def alpha1(sub):
    sub={GT:1,LAM:0,kx:1,**sub};eqf={A:sp.expand(eq[A].subs(sub)) for A in BRAS}
    M=[[sp.expand(eqf[BRAS[a]].coeff(KETS[bx])) for bx in range(NF)] for a in range(NF)]
    src=[sp.expand(eqf[BRAS[a]].subs({k:sp.S(0) for k in KETS})) for a in range(NF)]
    MH=[[sp.cancel((M[a][bx]+CONJ(M[bx][a]))/2) for bx in range(NF)] for a in range(NF)]
    eqf={BRAS[a]:sp.expand(sum(MH[a][bx]*KETS[bx] for bx in range(NF))+src[a]) for a in range(NF)}
    VZ={S('B2k'):0,S('B3k'):0,S('s23k'):0,S('a2k'):0,S('a3k'):0}
    stat_b=[S('Psib'),S('Phib'),S('s22b'),S('a1b'),S('chib')];stat_k=[S('Psik'),S('Phik'),S('s22k'),S('a1k'),S('chik')]
    eq0=[sp.expand(eqf[bx].coeff(wb,0).subs(VZ)) for bx in stat_b];s0s=lin(eq0,stat_k)
    if s0s is None:return 'SING0'
    s0={**s0s,S('B2k'):sp.S(0),S('B3k'):sp.S(0),S('s23k'):sp.S(0),S('a2k'):sp.S(0),S('a3k'):sp.S(0)}
    U=sp.cancel(-s0[S('Psik')]/Rk)
    if U==0:return 'U0'
    dk1={A:sp.Symbol(f'd1_{A}') for A in KETS};subF={A:s0[A]+wb*dk1[A] for A in KETS}
    eqW={A:sp.expand(eqf[A].subs(subF)) for A in BRAS};s1=lin([sp.expand(eqW[A].coeff(wb,1)) for A in BRAS],list(dk1.values()))
    if s1 is None:return 'SING1'
    c2t=sp.cancel(sp.expand(dk1[S('B2k')].subs(s1)).coeff(w2)/Rk);return sp.cancel(2*c2t/U)
R=lambda a,bd:sp.Rational(a,bd);q=sp.Symbol('q',positive=True)
print("TRANSVERSE (b perp k, theta=pi/2): alpha_1(b), K_B=1/5, J_Y=1")
for bv in [0, 1, 10, 100, 1000]:
    a=alpha1({b:sp.nsimplify(bv),KB:R(1,5),JY:sp.S(1),Q0:q})
    if a in('SING0','SING1','U0'): print(f"  b={bv}: {a}"); continue
    aq=sp.cancel(sp.limit(a,q,0)); im=sp.simplify(sp.im(sp.expand(aq)))
    re=sp.nsimplify(sp.re(aq))
    print(f"  b={bv:>5}: alpha_1 = {re}  (Im={im})  = {float(re):+.5f}")
