b=open('source/background.c').read()
hdr='''
/* ---- DF2 dark fluid term, lane DF2_dark_fluid_requirement. Env DF2_W, DF2_CS0, DF2_N, DF2_ZLO, DF2_ZHI, DF2_CV0, DF2_CVN, DF2_MUT. Unset = off. ---- */
#include <stdlib.h>
#include <math.h>
static double df2_w_v=0.; static int df2_w_read=0;
double df2_w(){ if(!df2_w_read){const char*s=getenv("DF2_W"); df2_w_v=s?atof(s):0.; df2_w_read=1;} return df2_w_v; }
/* ---- end DF2 ---- */
'''
i=b.index('/* ---- X34 turn-on'); b=b[:i]+hdr+b[i:]
a='''      pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3) * x34_s;
      rho_tot += pvecback[pba->index_bg_rho_cdm];
      p_tot += 0.;'''
assert b.count(a)==1
b=b.replace(a,'''      pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3*(1.+df2_w())) * x34_s;
      rho_tot += pvecback[pba->index_bg_rho_cdm];
      p_tot += df2_w()*pvecback[pba->index_bg_rho_cdm];
      dp_dloga += -3.*(1.+df2_w())*df2_w()*pvecback[pba->index_bg_rho_cdm];''')
open('source/background.c','w').write(b)
h=open('include/perturbations.h').read()
a='  int index_pt_theta_cdm; /**< cdm velocity */'
assert h.count(a)==1; h=h.replace(a,a+'\n  int index_pt_shear_cdm; /* DF2 */'); open('include/perturbations.h','w').write(h)
p=open('source/perturbations.c').read()
hdr='''
/* ---- DF2 dark fluid term ---- */
#include <stdlib.h>
#include <math.h>
extern "C" double df2_w();
static int df2_read=0; static double df2_cs0=0.,df2_n=0.,df2_zlo=-1.,df2_zhi=-1.,df2_cv0=0.,df2_cvn=0.,df2_mut=1.;
static double df2_env(const char*k,double d){const char*s=getenv(k);return s?atof(s):d;}
static void df2_init(){ if(df2_read) return; double c=299792.458; df2_cs0=df2_env("DF2_CS0",0.)/c; df2_n=df2_env("DF2_N",0.); df2_zlo=df2_env("DF2_ZLO",-1.); df2_zhi=df2_env("DF2_ZHI",-1.); df2_cv0=df2_env("DF2_CV0",0.)/c; df2_cvn=df2_env("DF2_CVN",0.); df2_mut=df2_env("DF2_MUT",0.)>0.?-1.:1.; df2_read=1; }
static double df2_win(double a){ double f=1.,wd=0.05; if(df2_zhi>0.) f*=0.5*(1.+tanh((log(a)-log(1./(1.+df2_zhi)))/wd)); if(df2_zlo>0.) f*=0.5*(1.-tanh((log(a)-log(1./(1.+df2_zlo)))/wd)); return f; }
static double df2_cs2(double a){ df2_init(); double c=df2_cs0*pow(a,-df2_n); double v=c*c*df2_win(a); return v>1./3.?1./3.:v; }
static double df2_cv2(double a){ df2_init(); double c=df2_cv0*pow(a,-df2_cvn); double v=c*c; return v>1./3.?1./3.:v; }
/* ---- end DF2 ---- */
'''
i=p.index('/* X34 (R1 turn-on)'); p=p[:i]+hdr+p[i:]
a='''    class_define_index(ppv->index_pt_theta_cdm,pba->has_cdm && (ppt->gauge == newtonian),index_pt,1); /* cdm velocity */'''
assert p.count(a)==1; p=p.replace(a,a+'''\n    class_define_index(ppv->index_pt_shear_cdm,pba->has_cdm && (ppt->gauge == newtonian),index_pt,1); /* DF2 */''')
a='''          ppv->y[ppv->index_pt_theta_cdm] =
            ppw->pv->y[ppw->pv->index_pt_theta_cdm];
'''
assert p.count(a)==1; p=p.replace(a,a+'''          ppv->y[ppv->index_pt_shear_cdm] =
            ppw->pv->y[ppw->pv->index_pt_shear_cdm];
''')
a='''        dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity); /* cdm density */

        dy[pv->index_pt_theta_cdm] = - a_prime_over_a*y[pv->index_pt_theta_cdm] + metric_euler; /* cdm velocity */
'''
assert p.count(a)==1
p=p.replace(a,'''        { /* DF2: rest-frame c_s^2, c_vis^2, constant w */
          double df2_a=pvecback[pba->index_bg_a], cs2=df2_cs2(df2_a), cv2=df2_cv2(df2_a), w_=df2_w();
          dy[pv->index_pt_delta_cdm] = -(1.+w_)*(y[pv->index_pt_theta_cdm]+metric_continuity)
            - 3.*a_prime_over_a*(cs2-w_)*y[pv->index_pt_delta_cdm]
            - 9.*(1.+w_)*(cs2-w_)*a_prime_over_a*a_prime_over_a*y[pv->index_pt_theta_cdm]/k2;
          dy[pv->index_pt_theta_cdm] = - a_prime_over_a*(1.-3.*cs2)*y[pv->index_pt_theta_cdm]
            + df2_mut*cs2*k2/(1.+w_)*y[pv->index_pt_delta_cdm] + metric_euler - k2*y[pv->index_pt_shear_cdm];
          dy[pv->index_pt_shear_cdm] = -3.*a_prime_over_a*y[pv->index_pt_shear_cdm] + 0.8*cv2*y[pv->index_pt_theta_cdm];
        }
''')
a='''      if (ppt->gauge == newtonian)
        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta + ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm]; // contribution to total perturbed stress-energy

      ppw->rho_plus_p_tot += ppw->pvecback[pba->index_bg_rho_cdm];
'''
if p.count(a)!=1:
    import re
    m=re.search(r"      if \(ppt->gauge == newtonian\)\n        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta \+ ppw->pvecback\[pba->index_bg_rho_cdm\]\*y\[ppw->pv->index_pt_theta_cdm\];[^\n]*\n\n      ppw->rho_plus_p_tot \+= ppw->pvecback\[pba->index_bg_rho_cdm\];\n",p); assert m; a=m.group(0)
p=p.replace(a,'''      { double w_=df2_w();
      if (ppt->gauge == newtonian) {
        double df2_a=ppw->pvecback[pba->index_bg_a], cs2=df2_cs2(df2_a), aH=df2_a*ppw->pvecback[pba->index_bg_H];
        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta + (1.+w_)*ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];
        ppw->rho_plus_p_shear += (1.+w_)*ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_shear_cdm];
        ppw->delta_p += cs2*ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_delta_cdm]
          + 3.*aH*(1.+w_)*(cs2-w_)*ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm]/(k*k);
      }
      ppw->rho_plus_p_tot += (1.+w_)*ppw->pvecback[pba->index_bg_rho_cdm]; }
''')
open('source/perturbations.c','w').write(p)
