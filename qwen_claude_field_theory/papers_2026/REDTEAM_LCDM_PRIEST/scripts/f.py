from lib import *
exec(open('e.py').read().split("x=brentq")[0].split("cos,_=setc()",1)[1])
cos,_=setc();x=1.345
print('base check',stack(cos,x)[0]/A0)
for z in [1,1.5,2.33]: print('tuned none z',z,'%.2f'%(stack(cos,x,z=z)[0]/stack(cos,x)[0]))
for z in [1,1.5,2.33]: print('blum z',z,'%.2f'%(stack(cos,1.,cm='blumenthal',z=z)[0]/stack(cos,1.,cm='blumenthal')[0]))
for M in [1e12]:
    h=H(cos,M);Mb=smhm(M);Mb=(Mb+Mb*fgas(Mb))*Msun
    for R in [100,300,1000]:
        r=R*kpc;gc=G*h.m(min(r,h.R))/r**2;print(R,'log(gCDM 1-halo/glaw) %.2f'%np.log10(gc/law_g(G*Mb/r**2)))
for M200 in [3e14,7e14,1.5e15]:
    h=H(cos,M200);R500=brentq(lambda r:h.m(r)/(4/3*np.pi*r**3*500*h.rc)-1,.1*h.R,h.R)
    M5=h.m(R500);gb=G*(.13*M5+smhm(M200)*Msun)/R500**2;print('M500 %.1e M/Mlaw %.2f'%(M5/Msun,(G*M5/R500**2)/law_g(gb)))
Ml=brentq(lambda lm:np.log10(smhm(10**lm)/1e8),9,12);r,gb,gt,h,Rd,ms=galaxy(cos,10**Ml,cmode='none',dsize=x);
print('M*=1e8 M200 %.2e'%10**Ml,'V rival/law at Rd..5Rd',np.round(np.sqrt(gt/law_g(gb))[[3,6,9,11]],2))
h=H(cos,1e9);r=30*3.0857e16;print('UFD sigma ratio %.2f'%np.sqrt((G*h.m(r)/r**2)/law_g(G*3e3*Msun/r**2)))
