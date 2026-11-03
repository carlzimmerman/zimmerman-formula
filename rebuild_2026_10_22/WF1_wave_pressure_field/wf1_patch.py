p=open('source/perturbations.c').read()
hdr='''
/* ---- WF1 wave field: c_s^2(k,a) = q/(1+q), q=(k/2ma)^2, m in eV via env WF1_M; unset = DF2's behaviour ---- */
static int wf1_read=0; static double wf1_m=-1.;
static double wf1_cs2(double a,double kk,double df2val){ if(!wf1_read){const char*s=getenv("WF1_M"); wf1_m=s?atof(s)*1.56373e29:-1.; wf1_read=1;} if(wf1_m<=0.) return df2val; double q=kk/(2.*wf1_m*a); q=q*q; double v=q/(1.+q); return v>1./3.?1./3.:v; }
/* ---- end WF1 ---- */
'''
i=p.index('/* ---- end DF2 ---- */')+len('/* ---- end DF2 ---- */'); p=p[:i]+hdr+p[i:]
a='cs2=df2_cs2(df2_a), cv2=df2_cv2(df2_a), w_=df2_w();'; assert p.count(a)==1; p=p.replace(a,'cs2=wf1_cs2(df2_a,k,df2_cs2(df2_a)), cv2=df2_cv2(df2_a), w_=df2_w();')
a='cs2=df2_cs2(df2_a), aH='; assert p.count(a)==1; p=p.replace(a,'cs2=wf1_cs2(df2_a,k,df2_cs2(df2_a)), aH=')
open('source/perturbations.c','w').write(p)
