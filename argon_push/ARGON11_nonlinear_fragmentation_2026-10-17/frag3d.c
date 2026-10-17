/* ARGON11: 3+1D nonlinear evolution of the charged host Psi + real mediator chi (astra's CPB-UV model).
 *   L = -|dPsi|^2 - (1/2)(dchi)^2 - V,  V = I + Lq I^2 + a chi I + U(chi),  I=|Psi|^2,
 *   U = M^2 chi^2/2 - (M/8) chi^3 + chi^4/4,  units m_h = 1.
 * EOM: Psi_tt = lap Psi - (1 + 2 Lq I + a chi) Psi ;  chi_tt = lap chi - U'(chi) - a I.
 * Periodic cube, 4th-order Laplacian, kick-drift-kick (velocity Verlet), double precision.
 * Conserved: Q = sum 2 Im(Psi* Psi_t) dV ;  E_h = sum [ |Psi_t|^2 + chi_t^2/2 + V - Re(Psi* lap_h Psi) - chi lap_h chi /2 ] dV.
 * usage: frag3d tag N dx dt M Lq a I0 chi0 omega eps seed tend snapint outdir [resume]
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>

static int N; static double dx, dt, Mm, Lq, aq;
static double *pr,*pi_,*vr,*vi,*c,*vc,*ar,*ai,*ac,*lapr,*lapi,*lapc;
static int *ip1,*ip2,*im1,*im2;

static uint64_t rs;
static double urand(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return ((rs>>11)+0.5)*(1.0/9007199254740992.0); }
static double grand(void){ double u1=urand(),u2=urand(); return sqrt(-2*log(u1))*cos(2*M_PI*u2); }

static inline double Up(double x){ return Mm*Mm*x - 3.0*Mm*x*x/8.0 + x*x*x; }
static inline double Uf(double x){ return Mm*Mm*x*x/2 - Mm*x*x*x/8 + x*x*x*x/4; }

static void laplace(const double *f, double *out){
  double h2=1.0/(12.0*dx*dx);
  for(int k=0;k<N;k++) for(int j=0;j<N;j++){
    long base=((long)k*N+j)*N;
    for(int i=0;i<N;i++){
      long id=base+i;
      double ctr=f[id];
      double sx=-f[base+ip2[i]]+16*f[base+ip1[i]]+16*f[base+im1[i]]-f[base+im2[i]];
      long bj1=((long)k*N+ip1[j])*N+i, bj2=((long)k*N+ip2[j])*N+i, bjm1=((long)k*N+im1[j])*N+i, bjm2=((long)k*N+im2[j])*N+i;
      double sy=-f[bj2]+16*f[bj1]+16*f[bjm1]-f[bjm2];
      long bk1=((long)ip1[k]*N+j)*N+i, bk2=((long)ip2[k]*N+j)*N+i, bkm1=((long)im1[k]*N+j)*N+i, bkm2=((long)im2[k]*N+j)*N+i;
      double sz=-f[bk2]+16*f[bk1]+16*f[bkm1]-f[bkm2];
      out[id]=(sx+sy+sz-90.0*ctr)*h2;
    }
  }
}
static void accel(void){
  long n3=(long)N*N*N;
  laplace(pr,lapr); laplace(pi_,lapi); laplace(c,lapc);
  for(long id=0;id<n3;id++){
    double I=pr[id]*pr[id]+pi_[id]*pi_[id];
    double m2=1.0+2*Lq*I+aq*c[id];
    ar[id]=lapr[id]-m2*pr[id];
    ai[id]=lapi[id]-m2*pi_[id];
    ac[id]=lapc[id]-Up(c[id])-aq*I;
  }
}
static void diagnostics(double *Q,double *E,double *Ifl,double *Imax,double *Imean){
  long n3=(long)N*N*N; double dV=dx*dx*dx;
  laplace(pr,lapr); laplace(pi_,lapi); laplace(c,lapc);
  double q=0,e=0,im=0,imx=0,mr=0,mi=0;
  for(long id=0;id<n3;id++){
    double I=pr[id]*pr[id]+pi_[id]*pi_[id];
    q+=2*(pr[id]*vi[id]-pi_[id]*vr[id]);
    double V=I+Lq*I*I+aq*c[id]*I+Uf(c[id]);
    e+=vr[id]*vr[id]+vi[id]*vi[id]+0.5*vc[id]*vc[id]+V-(pr[id]*lapr[id]+pi_[id]*lapi[id])-0.5*c[id]*lapc[id];
    im+=I; if(I>imx) imx=I; mr+=pr[id]; mi+=pi_[id];
  }
  mr/=n3; mi/=n3; double var=0;
  for(long id=0;id<n3;id++){ double dr=pr[id]-mr, di=pi_[id]-mi; var+=dr*dr+di*di; }
  *Q=q*dV; *E=e*dV; *Ifl=var/n3; *Imax=imx; *Imean=im/n3;
}
static void snapshot(const char *outdir,const char *tag,double t){
  long n3=(long)N*N*N; float *buf=malloc(sizeof(float)*n3*3);
  double h2=1.0/(2*dx);
  for(int k=0;k<N;k++) for(int j=0;j<N;j++) for(int i=0;i<N;i++){
    long id=((long)k*N+j)*N+i;
    double I=pr[id]*pr[id]+pi_[id]*pi_[id];
    double n=2*(pr[id]*vi[id]-pi_[id]*vr[id]);
    /* 2nd-order central gradients for local energy */
    long xp=((long)k*N+j)*N+ip1[i], xm=((long)k*N+j)*N+im1[i];
    long yp=((long)k*N+ip1[j])*N+i, ym=((long)k*N+im1[j])*N+i;
    long zp=((long)ip1[k]*N+j)*N+i, zm=((long)im1[k]*N+j)*N+i;
    double g2=0;
    long p[3][2]={{xp,xm},{yp,ym},{zp,zm}};
    for(int d=0;d<3;d++){
      double gr=(pr[p[d][0]]-pr[p[d][1]])*h2, gi=(pi_[p[d][0]]-pi_[p[d][1]])*h2, gc=(c[p[d][0]]-c[p[d][1]])*h2;
      g2+=gr*gr+gi*gi+0.5*gc*gc;
    }
    double V=I+Lq*I*I+aq*c[id]*I+Uf(c[id]);
    double e=vr[id]*vr[id]+vi[id]*vi[id]+0.5*vc[id]*vc[id]+g2+V;
    buf[id]=(float)I; buf[n3+id]=(float)n; buf[2*n3+id]=(float)e;
  }
  char fn[512]; snprintf(fn,sizeof fn,"%s/snap_%s_t%07.1f.bin",outdir,tag,t);
  FILE *f=fopen(fn,"wb"); fwrite(buf,sizeof(float),n3*3,f); fclose(f); free(buf);
}
static void ckpt_write(const char *outdir,const char *tag,long step){
  long n3=(long)N*N*N; char fn[512],fn2[512];
  snprintf(fn,sizeof fn,"%s/ckpt_%s.tmp",outdir,tag); snprintf(fn2,sizeof fn2,"%s/ckpt_%s.bin",outdir,tag);
  FILE *f=fopen(fn,"wb"); fwrite(&step,sizeof step,1,f);
  double *arr[6]={pr,pi_,vr,vi,c,vc}; for(int a=0;a<6;a++) fwrite(arr[a],sizeof(double),n3,f);
  fclose(f); rename(fn,fn2);
}
static int ckpt_read(const char *outdir,const char *tag,long *step){
  long n3=(long)N*N*N; char fn[512]; snprintf(fn,sizeof fn,"%s/ckpt_%s.bin",outdir,tag);
  FILE *f=fopen(fn,"rb"); if(!f) return 0; if(fread(step,sizeof *step,1,f)!=1){fclose(f);return 0;}
  double *arr[6]={pr,pi_,vr,vi,c,vc}; for(int a=0;a<6;a++) if(fread(arr[a],sizeof(double),n3,f)!=(size_t)n3){fclose(f);return 0;}
  fclose(f); return 1;
}
int main(int argc,char **argv){
  if(argc<15){ fprintf(stderr,"usage\n"); return 2; }
  const char *tag=argv[1]; N=atoi(argv[2]); dx=atof(argv[3]); dt=atof(argv[4]); Mm=atof(argv[5]); Lq=atof(argv[6]); aq=atof(argv[7]);
  double I0=atof(argv[8]), chi0=atof(argv[9]), om=atof(argv[10]), eps=atof(argv[11]); uint64_t seed=strtoull(argv[12],0,10);
  double tend=atof(argv[13]); double snapint=atof(argv[14]); const char *outdir=argv[15]; int resume=(argc>16);
  long n3=(long)N*N*N; double *all=malloc(sizeof(double)*n3*12); if(!all){fprintf(stderr,"alloc\n");return 3;}
  pr=all; pi_=all+n3; vr=all+2*n3; vi=all+3*n3; c=all+4*n3; vc=all+5*n3; ar=all+6*n3; ai=all+7*n3; ac=all+8*n3; lapr=all+9*n3; lapi=all+10*n3; lapc=all+11*n3;
  ip1=malloc(sizeof(int)*N*4); ip2=ip1+N; im1=ip2+N; im2=im1+N;
  for(int i=0;i<N;i++){ ip1[i]=(i+1)%N; ip2[i]=(i+2)%N; im1[i]=(i-1+N)%N; im2[i]=(i-2+N)%N; }
  long step=0; long nsteps=(long)llround(tend/dt); long snapsteps=(long)llround(snapint/dt); long diagsteps=snapsteps/10>0?snapsteps/10:1;
  char logfn[512]; snprintf(logfn,sizeof logfn,"%s/log_%s.txt",outdir,tag);
  if(resume && ckpt_read(outdir,tag,&step)){ fprintf(stderr,"resumed at step %ld\n",step); }
  else {
    rs=seed*0x9E3779B97F4A7C15ULL+88172645463325252ULL; for(int w=0;w<20;w++) urand();
    double s0=sqrt(I0);
    for(long id=0;id<n3;id++){
      double nr=grand()/M_SQRT2, ni=grand()/M_SQRT2;
      pr[id]=s0*(1+eps*nr); pi_[id]=s0*eps*ni;
      vr[id]=-om*pi_[id]; vi[id]=om*pr[id];     /* Psi_t = i om Psi */
      c[id]=chi0; vc[id]=0;
    }
    FILE *lf=fopen(logfn,"w"); fprintf(lf,"# tag=%s N=%d dx=%g dt=%g M=%g L=%.10g a=%g I0=%.10g chi0=%.10g om=%.10g eps=%g seed=%llu\n",tag,N,dx,dt,Mm,Lq,aq,I0,chi0,om,eps,(unsigned long long)seed);
    fprintf(lf,"# t Q E Ifl Imax Imean\n"); fclose(lf);
  }
  accel();
  double Q0=0,E0=0,x1,x2,x3; 
  { double Q,E,Ifl,Imax,Imean; diagnostics(&Q,&E,&Ifl,&Imax,&Imean); Q0=Q; E0=E; (void)x1;(void)x2;(void)x3;
    if(step==0){ FILE *lf=fopen(logfn,"a"); fprintf(lf,"%.4f %.12e %.12e %.8e %.8e %.8e\n",0.0,Q,E,Ifl,Imax,Imean); fclose(lf); snapshot(outdir,tag,0.0); } }
  for(;step<nsteps;){
    for(long q=0;q<diagsteps && step<nsteps;q++,step++){
      for(long id=0;id<n3;id++){ vr[id]+=0.5*dt*ar[id]; vi[id]+=0.5*dt*ai[id]; vc[id]+=0.5*dt*ac[id]; }
      for(long id=0;id<n3;id++){ pr[id]+=dt*vr[id]; pi_[id]+=dt*vi[id]; c[id]+=dt*vc[id]; }
      accel();
      for(long id=0;id<n3;id++){ vr[id]+=0.5*dt*ar[id]; vi[id]+=0.5*dt*ai[id]; vc[id]+=0.5*dt*ac[id]; }
    }
    double t=step*dt; double Q,E,Ifl,Imax,Imean; diagnostics(&Q,&E,&Ifl,&Imax,&Imean);
    FILE *lf=fopen(logfn,"a"); fprintf(lf,"%.4f %.12e %.12e %.8e %.8e %.8e\n",t,Q,E,Ifl,Imax,Imean); fclose(lf);
    if(!isfinite(E)){ fprintf(stderr,"non-finite at t=%g\n",t); return 4; }
    if(step%snapsteps==0){ snapshot(outdir,tag,t); ckpt_write(outdir,tag,step); }
  }
  return 0;
}
