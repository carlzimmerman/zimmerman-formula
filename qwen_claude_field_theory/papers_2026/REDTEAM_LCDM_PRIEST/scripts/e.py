from lib import *
cos,_=setc()
def stack(c,x,cm='none',n=400,seed=3,sc=(.11,.15,.2),z=0):
    rng=np.random.default_rng(seed);GB=[];GT=[];P=[]
    for lm in rng.uniform(10,12.7,n):
        M=10**lm;c0=H(c,M,z).cv*10**rng.normal(0,sc[0]);ds=10**rng.normal(0,sc[2])
        r,gb,gt,h,Rd,ms=galaxy(c,M,conc=c0,cmode=cm,mscale=10**rng.normal(0,sc[1]),dsize=x*ds,z=z)
        GB+=list(gb);GT+=list(gt);P.append((lm,np.log10(np.sqrt(gt[-1]*r[-1])/1e3),np.log10((1+fgas(ms))*ms/(Rd/kpc)**2),np.log10(fit_a(gb,gt))))
    GB,GT=np.array(GB),np.array(GT);a=fit_a(GB,GT);return a,(np.log10(GT)-np.log10(law_g(GB,a))).std(),np.array(P)
x=brentq(lambda x:np.log(stack(cos,x)[0]/A0),1,1.8,xtol=.005);print('tuned size multiplier on K13: %.3f -> Rd/R200=%.4f (R1/2/R200=%.4f; K13 .015)'%(x,.0089*x,.0089*x*1.678))
for s in [3,4,5]:
    a,r,P=stack(cos,x,seed=s,n=800);print('seed',s,'a %.3e rms %.3f'%(a,r))
A=np.c_[P[:,1],P[:,2],np.ones(len(P))];print('per-gal log a vs (logV, logSigma) slopes',np.linalg.lstsq(A,P[:,3],rcond=None)[0][:2],'scatter %.2f'%P[:,3].std())
print('a trend: log V slope alone %.2f; per-mass fit; a at logM 10.,11,12,12.7:'%np.polyfit(P[:,1],P[:,3],1)[0],[ '%.2e'%fit_a(*galaxy(cos,10**m,cmode='none',dsize=x)[1:3]) for m in [10,11,12,12.7]])
# fg variations at fixed x tuned: sensitivity to each choice
print('Sensitivity (a/A0):')
for nm,kw in [('blumenthal',dict(cm='blumenthal')),('gnedin',dict(cm='gnedin'))]:
    print(nm,'%.2f'%(stack(cos,x,**kw)[0]/A0))
for nm,sc in [('no scatter',(0,0,0))]:print(nm,'%.2f'%(stack(cos,x,sc=sc)[0]/A0))
print('x=.8/1.2 of tuned: %.2f %.2f'%(stack(cos,.8*x)[0]/A0,stack(cos,1.2*x)[0]/A0))
for case,law in [('rde',.5),('OL',.5),('H0',1)]:
    u,d,dl=cosmo_case(case);print(case,'tuned slope %.3f vs law %.2f'%(np.log(stack(setc(**u)[0],x)[0]/stack(setc(**d)[0],x)[0])/dl,law))
for z,b in [(0,1),(1,'.91[.76,1.03]'),(1.5,'.94[.71,1.12]'),(2.33,'.91[.33,1.21]')]:
    print('z',z,'a/a(0)=%.2f; band %s'%(stack(cos,x,z=z)[0]/A0,b))
# Omega_L shift needed: kappa_hat vs 
for ol,H0 in [(.685,67.4),(.70,67.4),(.65,73),(.685,73)]:
    c1=setc(H0=H0,OL=ol)[0];a=stack(c1,x)[0];rd=ol*3*(H0*1e3/Mpc)**2/(8*np.pi*G);k=a/(c*np.sqrt(G*rd));print('OL %.3f H0 %.1f a %.2e kappa_hat %.3f'%(ol,H0,a,k))
