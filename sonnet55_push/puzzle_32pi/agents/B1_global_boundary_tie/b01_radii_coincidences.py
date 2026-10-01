"""b01: global conditions on the static spherical SdS / Schwarzschild-dS system (c=G=1, L=1 so Lambda=3, M_N=1/(3 sqrt3))."""
import sympy as sp, mpmath as mp, itertools, sys
mp.mp.dps=40
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
Lam=mp.mpf(3); MN=1/(3*mp.sqrt(3)); TARGET=8*mp.pi
f=lambda r,M: 1-2*M/r-Lam*r**2/3
def hor(M):
    if M>=MN: return None
    rts=sorted([mp.re(z) for z in mp.polyroots([1,0,-1,2*M],maxsteps=200,extraprec=100) if mp.re(z)>0])
    return rts[0],rts[1]
fp=lambda r,M: 2*M/r**2-2*Lam*r/3
def rad(M,name):
    if name=='s': return 2*M
    if name=='zf': return (3*M/Lam)**(mp.mpf(1)/3)
    if name=='j': return (6*M/Lam)**(mp.mpf(1)/3)
    h=hor(M)
    if h is None: return None
    return h[0] if name=='b' else h[1]
# ---- sympy identities
r,M,Lm,rho,w=sp.symbols('r M Lambda rho w',positive=True)
chk("1 SdS horizon: 1 - 2 kappa_f r = Lambda r^2 (kappa_f=f'/2, f=1-2M/r-Lambda r^2/3, f(r)=0)",
    sp.simplify((1-2*(sp.diff(1-2*M/r-Lm*r**2/3,r)/2)*r-Lm*r**2).subs(M,(r-Lm*r**3/3)/2))==0)
chk("2 shell-free junction f_in=1-2M/R, f_out=1-Lambda R^2/3: R^3 = 6M/Lambda",
    sp.solve(sp.Eq(2*M/r,Lm*r**2/3),M)[0]==Lm*r**3/6)
# ES: SdS interior (M) to FRW exterior; Misner-Sharp: 2m_FRW/R=(8pi/3)(rho_m+rho_L)R^2 ; interior 2M/R+(8pi/3)rho_L R^2 -> M=(4pi/3) rho_m R^3, Lambda cancels
rm,rL=sp.symbols('rho_m rho_L',positive=True)
Msol=sp.solve(sp.Eq(2*M/r+sp.Rational(8,3)*sp.pi*rL*r**2,sp.Rational(8,3)*sp.pi*(rm+rL)*r**2),M)[0]
chk("3 Einstein-Straus radius is Lambda-independent: M=(4 pi/3) rho_m R^3 (Lambda cancels between interior and FRW)", sp.simplify(Msol-sp.Rational(4,3)*sp.pi*rm*r**3)==0)
chk("4 r_J = r_ES(rho_m = rho_L) exactly (Lambda=8 pi rho_L)", sp.simplify(sp.solve(sp.Eq(Msol.subs(rm,rL),M),r)[0]**3/(6*M/(8*sp.pi*rL)))==1)
chk("5 mean density inside r_ZF = Lambda/4pi = 2 rho_L (rho+3p of dust 2rho_L cancels the vacuum -2 rho_L): so r_ZF = r_ES(w=2) exactly",
    sp.simplify(Msol.subs(rm,2*rL)-sp.Rational(4,3)*sp.pi*2*rL*r**3)==0)
# numeric: r_ZF^3 = 3M/Lambda <=> w=2
Mx=mp.mpf('0.1'); chk("6 numeric: (3M/Lambda)^(1/3) = ES radius for w=2 (L=1: 3M/(4 pi 2 Lambda/8pi)=3M/Lambda)",
    abs(rad(Mx,'zf')-(3*Mx/(4*mp.pi*2*(Lam/(8*mp.pi))))**(mp.mpf(1)/3))<1e-30)
chk("7 horizon equation numerically, 30 masses: kappa_b r_b=(1-3 r_b^2)/2, kappa_c r_c=(3 r_c^2-1)/2 (signed f'/2 convention) ",
    all(abs(fp(rad(m_,'b'),m_)/2*rad(m_,'b')-(1-3*rad(m_,'b')**2)/2)<1e-30 and abs(-fp(rad(m_,'c'),m_)/2*rad(m_,'c')-(3*rad(m_,'c')**2-1)/2)<1e-30
        for m_ in [MN*k/31 for k in range(1,31)]))
# ---- G12: |kappa_f| r = |1-Lam r^2|/2 = 1/2 at horizons of SdS
sol=sp.solve(sp.Eq(sp.Abs(1-3*r**2),1),r)
print("G12 roots of |1-3x^2|=1 :",sol)
xb=0; xc=sp.sqrt(sp.Rational(2,3))
Mc=(xc-xc**3)/2
print("   |kappa_c| r_c = 1/2 at r_c^2 Lambda = 2: r_c/L=%.6f, M/M_N = %s = %.6f"%(float(xc),sp.nsimplify(sp.simplify(Mc/(1/(3*sp.sqrt(3))))),float(Mc*3*sp.sqrt(3))))
chk("8 G12: BH horizon has kappa_f r = 1/2 only as Lambda r_b^2 -> 0 (M->0); cosmological horizon has |kappa_c| r_c = 1/2 exactly at r_c^2 Lambda = 2, M = M_N/sqrt2 (value 2, not 8 pi)",
    sp.simplify(Mc*3*sp.sqrt(3)-1/sp.sqrt(2))==0 and abs(mp.mpf(2)-TARGET)>20)
# horizon radii limits (normalisation independent): r_b^2 Lambda<=1, r_c^2 Lambda<=3 
ms=[MN*k/200 for k in range(1,200)]
mxb=max(Lam*rad(m_,'b')**2 for m_ in ms); mxc=max(Lam*rad(m_,'c')**2 for m_ in ms)
chk("9 horizon-radius bounds r_b^2 Lambda <= 1, r_c^2 Lambda <= 3 (independent of Killing normalisation) so 8 pi is unreachable by any SdS horizon (max %.4f, %.4f vs 25.13)"%(mxb,mxc), mxb<=1 and mxc<=3 and mxc<3)
# G13 existence: BH exists iff M<M_N iff r_s=2M<2L/(3 sqrt3); r_s^2 Lambda <= 4/9
chk("10 G13: SdS horizons exist iff r_s^2 Lambda < 4/9 (= 12 M^2 Lambda... M<M_N); the puzzle r_s^2 Lambda=8 pi is %.1f times above this bound"%(float(8*mp.pi/(mp.mpf(4)/9))), abs(Lam*(2*MN)**2-mp.mpf(4)/9)<1e-30)
# ---- coincidences G1-G9
names=['s','b','c','zf','j']
def diff(a,b,M):
    ra,rb=rad(M,a),rad(M,b)
    return None if ra is None or rb is None else ra-rb
rows=[]
for a,b in itertools.combinations(names,2):
    grid=[mp.mpf(k)/400*6 for k in range(1,401)]
    roots=[]
    for m0,m1 in zip(grid[:-1],grid[1:]):
        d0,d1=diff(a,b,m0),diff(a,b,m1)
        if d0 is None or d1 is None: continue
        if d0*d1<0:
            roots.append(mp.findroot(lambda m_: diff(a,b,m_),(m0,m1),solver='anderson',tol=1e-30))
    # endpoint coincidence at Nariai
    dN=diff(a,b,MN*(1-mp.mpf(10)**-25))
    if dN is not None and abs(dN)<1e-10 and not roots: roots=[MN]
    rows.append((a,b,roots))
print("\nCOINCIDENCES (L=1; r^2 Lambda = 3 r^2):")
alg_ok=True; hits8pi=0
for a,b,roots in rows:
    if not roots: print("  r_%s = r_%s : none for M>0 (b,c exist only M<M_N)"%(a,b)); continue
    for m_ in roots:
        rr=rad(m_,a) if rad(m_,a) is not None else (1/mp.sqrt(3))  # fixed: earlier version used the Nariai radius for every M>M_N
        Lr=3*rr**2
        poly=mp.findpoly(m_,6,maxcoeff=5000,tol=1e-25)
        if poly is None: alg_ok=False
        if abs(Lr-TARGET)<0.25: hits8pi+=1
        print("  r_%s = r_%s : M/M_N = %.6f, r^2 Lambda = %.6f, algebraic poly(M)=%s"%(a,b,m_/MN,Lr,poly))
chk("11 every coincidence mass is algebraic (findpoly deg<=6) -> r^2 Lambda algebraic, never 8 pi (transcendental)", alg_ok)
chk("12 no coincidence gives r^2 Lambda within 0.25 of 8 pi", hits8pi==0)
chk("13 control: findpoly CANNOT find an algebraic relation for 8 pi/3 at the same settings (the detector discriminates)", mp.findpoly(TARGET/3,6,maxcoeff=5000,tol=1e-25) is None)
# explicit table: s=j etc
print("\nExact points: r_s=r_J -> M=1/2 (2.598 M_N), r_s=L; r_s=r_ZF -> M=1/(2 sqrt2) (1.837 M_N), r^2 Lambda=3/2 ; r_J=r_c -> r_c^2=1/2")
chk("14 r_s=r_J at M=1/2: r_s^2 Lambda=3 (the Hubble-radius hole); r_s=r_ZF at M^2=1/8: r_s^2 Lambda=3/2; both are above M_N (no SdS horizon)",
    abs(rad(mp.mpf(1)/2,'s')-rad(mp.mpf(1)/2,'j'))<1e-30 and abs(rad(1/(2*mp.sqrt(2)),'s')-rad(1/(2*mp.sqrt(2)),'zf'))<1e-30 and 1/(2*mp.sqrt(2))>MN)
# ---- target masses for r^2 Lambda = 8 pi per radius, and ordering at that mass (Schwarzschild interior validity)
print("\nMass needed for each radius to satisfy r^2 Lambda = 8 pi, and radii at that mass (L=1):")
rT=mp.sqrt(TARGET/3)
Ms=rT/2; Mzf=rT**3/3*Lam/3*1; Mzf=Lam*rT**3/3; Mj=Lam*rT**3/6
for lab,mm in [('r_s',Ms),('r_ZF',Mzf),('r_J=r_ES(1)',Mj)]:
    print("  %-12s M=%.4f L = %.2f M_N : r_s=%.4f r_ZF=%.4f r_J=%.4f (L)"%(lab,mm,mm/MN,rad(mm,'s'),rad(mm,'zf'),rad(mm,'j')))
chk("15 at the mass where r_s^2 Lambda = 8 pi, the shell-free junction radius r_J=%.3f L is INSIDE r_s=%.3f L (junction would sit inside the horizon): no consistent vacuole with w=1"%(rad(Ms,'j'),rad(Ms,'s')), rad(Ms,'j')<rad(Ms,'s'))
chk("16 mutation: if Lambda were 4 pi rho (wrong coupling) r_J=ES(w=1) identity (check 4) fails",
    sp.simplify(sp.solve(sp.Eq(Msol.subs(rm,rL),M),r)[0]**3/(6*M/(4*sp.pi*rL)))!=1)
# G11: kappa_BH(c)=H only for M=0
vals=[abs(fp(rad(m_,'c'),m_)/2)/mp.sqrt(f(m_**(mp.mpf(1)/3),m_)) for m_ in [MN*k/50 for k in range(1,50)]]
chk("17 G11: de Sitter-regular normalisation kappa_BH(c)=H holds only at M=0 (min over M>0 of kappa_BH(c)/H = %.6f > 1)"%float(min(vals)), min(vals)>1)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
