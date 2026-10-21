/* Same explicit Psi/X/chi action, axisymmetric head-on diagnostics.
 * Cell-centred cylindrical finite volumes; conservative kick-drift-kick.
 * No damping, target profile or friction. Zero Dirichlet face boundaries.
 * Snapshot arrays and diagnostics use the same weighted discrete action.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <sys/resource.h>
#include <time.h>

static const double M=100., aq=200., g=.002168, mx2=4.0016;
static double lam;
static int nr,nz; static size_t cells; static double dx,dt;
static double *q[5],*v[5],*acc[5],*lap[5];
static long pn; static double pdr,*profile[6];
static const char *outdir;

static double at(const double *f,int j,int i){return f[(size_t)j*nr+i];}
static void laplace(const double *f,double *out){
    const double h2=1/(dx*dx);
    for(int j=0;j<nz;j++)for(int i=0;i<nr;i++){
        size_t k=(size_t)j*nr+i; double x=f[k];
        double rp=i+1<nr?f[k+1]:-x;
        double rm=i>0?f[k-1]:x;
        double zp=j+1<nz?f[k+nr]:-x;
        double zm=j>0?f[k-nr]:-x;
        out[k]=h2*(((i+1)*(rp-x)-i*(x-rm))/(i+.5)+zp+zm-2*x);
    }
}
static void acceleration(void){
    for(int a=0;a<5;a++)laplace(q[a],lap[a]);
    for(size_t k=0;k<cells;k++){
        double pr=q[0][k],pi=q[1][k],xr=q[2][k],xi=q[3][k],h=q[4][k];
        double I=pr*pr+pi*pi, mass=1+2*lam*I+aq*h;
        acc[0][k]=lap[0][k]-mass*pr-2*g*(xr*pr+xi*pi);
        acc[1][k]=lap[1][k]-mass*pi-2*g*(xi*pr-xr*pi);
        acc[2][k]=lap[2][k]-mx2*xr-g*(pr*pr-pi*pi);
        acc[3][k]=lap[3][k]-mx2*xi-2*g*pr*pi;
        acc[4][k]=lap[4][k]-M*M*h+3*M*h*h/8-h*h*h-aq*I;
    }
}
static void load_profile(const char *path){
    FILE *f=fopen(path,"rb");if(!f){perror(path);exit(2);}
    int64_t n;if(fread(&n,8,1,f)!=1||fread(&pdr,8,1,f)!=1||n<10){exit(2);}
    pn=(long)n;
    for(int a=0;a<6;a++){
        profile[a]=malloc(pn*sizeof(double));
        if(fread(profile[a],8,pn,f)!=(size_t)pn)exit(2);
    }
    fclose(f);
}
static double interp(int a,double r){
    double s=r/pdr;long k=(long)s;
    if(k>=pn-1)return 0.;
    if(k<0)k=0;
    double t=s-k;return profile[a][k]*(1-t)+profile[a][k+1]*t;
}
static void add_fragment(double zc,double vel,double phase,double omega){
    double ga=1/sqrt(1-vel*vel);
    for(int j=0;j<nz;j++)for(int i=0;i<nr;i++){
        size_t k=(size_t)j*nr+i;
        double R=(i+.5)*dx,z=(j+.5-.5*nz)*dx-zc;
        double r=sqrt(R*R+ga*ga*z*z), adv=-ga*ga*vel*z/r;
        double f=interp(0,r),fp=interp(1,r),b=interp(2,r),bp=interp(3,r);
        double h=interp(4,r),hp=interp(5,r);
        double p=phase-omega*ga*vel*z,c=cos(p),s=sin(p),c2=cos(2*p),s2=sin(2*p);
        q[0][k]+=f*c;q[1][k]+=f*s;
        v[0][k]+=adv*fp*c-omega*ga*f*s;v[1][k]+=adv*fp*s+omega*ga*f*c;
        q[2][k]+=b*c2;q[3][k]+=b*s2;
        v[2][k]+=adv*bp*c2-2*omega*ga*b*s2;v[3][k]+=adv*bp*s2+2*omega*ga*b*c2;
        q[4][k]+=h;v[4][k]+=adv*hp;
    }
}

/* Strict initial data input only. This is not a general checkpoint restart. */
static void load_initial_state(const char *path){
    FILE *f=fopen(path,"rb");if(!f){perror(path);exit(2);}
    char magic[8];int32_t dims[2];double h,t;
    if(fread(magic,1,8,f)!=8||fread(dims,4,2,f)!=2||fread(&h,8,1,f)!=1||fread(&t,8,1,f)!=1
       ||memcmp(magic,"CEPAIR1",8)||dims[0]!=nr||dims[1]!=nz||h!=dx||t!=0.){
        fprintf(stderr,"initial state header mismatch\n");fclose(f);exit(2);
    }
    for(int a=0;a<10;a++){
        double *target=a<5?q[a]:v[a-5];
        if(fread(target,8,cells,f)!=cells){fprintf(stderr,"truncated initial state\n");fclose(f);exit(2);}
        for(size_t k=0;k<cells;k++)if(!isfinite(target[k])){
            fprintf(stderr,"nonfinite initial state\n");fclose(f);exit(2);
        }
    }
    if(fgetc(f)!=EOF){fprintf(stderr,"trailing initial state data\n");fclose(f);exit(2);}
    fclose(f);
}

typedef struct{double E,Q,Pz,Q10,Q15,Q20,Imax,zpeak,rpeak,Qz2,Qr2,Eface,E10,E15,E20;} diag;
static diag diagnose(void){
    diag d={0};
    for(int a=0;a<5;a++)laplace(q[a],lap[a]);
    for(int j=0;j<nz;j++)for(int i=0;i<nr;i++){
        size_t k=(size_t)j*nr+i;
        double R=(i+.5)*dx,z=(j+.5-.5*nz)*dx,r2=R*R+z*z,w=2*M_PI*R*dx*dx;
        double pr=q[0][k],pi=q[1][k],xr=q[2][k],xi=q[3][k],h=q[4][k];
        double I=pr*pr+pi*pi,X=xr*xr+xi*xi;
        double U=.5*M*M*h*h-M*h*h*h/8+.25*h*h*h*h;
        double V=I+mx2*X+2*g*(xr*(pr*pr-pi*pi)+2*xi*pr*pi)+lam*I*I+aq*h*I+U;
        double kinetic=0,grad=0,pz=0,gface=0;
        for(int a=0;a<5;a++){
            double fac=a==4?.5:1.;kinetic+=fac*v[a][k]*v[a][k];grad-=fac*q[a][k]*lap[a][k];
            double zp=j+1<nz?q[a][k+nr]:-q[a][k];
            double zm=j>0?q[a][k-nr]:-q[a][k];
            pz-=2*fac*v[a][k]*(zp-zm)/(2*dx);
            double rp=i+1<nr?q[a][k+1]:-q[a][k];
            double rm=i>0?q[a][k-1]:q[a][k];
            double value=q[a][k];
            gface+=fac*.5/(dx*dx)*(((i+1)*pow(rp-value,2)+i*pow(value-rm,2))/(i+.5)+pow(zp-value,2)+pow(value-zm,2));
        }
        double charge=2*(pr*v[1][k]-pi*v[0][k])+4*(xr*v[3][k]-xi*v[2][k]);
        d.E+=w*(kinetic+grad+V);d.Eface+=w*(kinetic+gface+V);d.Q+=w*charge;d.Pz+=w*pz;
        if(r2<100)d.E10+=w*(kinetic+gface+V);
        if(r2<225)d.E15+=w*(kinetic+gface+V);
        if(r2<400)d.E20+=w*(kinetic+gface+V);
        if(r2<100)d.Q10+=w*charge;
        if(r2<225)d.Q15+=w*charge;
        if(r2<400)d.Q20+=w*charge;
        if(r2<900){d.Qz2+=w*charge*z*z;d.Qr2+=w*charge*R*R;}
        if(I>d.Imax){d.Imax=I;d.zpeak=z;d.rpeak=R;}
    }
    return d;
}
static void snapshot(double t){
    char path[1024];snprintf(path,sizeof path,"%s/snap_t%09ld.bin",outdir,lround(t*1000));
    FILE *f=fopen(path,"wb");if(!f){perror(path);exit(3);}
    const char magic[8]="CEPAIR1";int32_t dims[2]={nr,nz};
    fwrite(magic,1,8,f);fwrite(dims,4,2,f);fwrite(&dx,8,1,f);fwrite(&t,8,1,f);
    for(int a=0;a<5;a++)fwrite(q[a],8,cells,f);
    for(int a=0;a<5;a++)fwrite(v[a],8,cells,f);
    if(fclose(f))exit(3);
}
static void gaussian_benchmark(void){
    double s2=9.,err=0,norm=0,sym=0;
    for(int j=0;j<nz;j++)for(int i=0;i<nr;i++){
        size_t k=(size_t)j*nr+i;double R=(i+.5)*dx,z=(j+.5-.5*nz)*dx;
        q[0][k]=exp(-(R*R+z*z)/s2);q[1][k]=exp(-(R*R+z*z)/12.)*(1+.1*z);
    }
    laplace(q[0],lap[0]);laplace(q[1],lap[1]);
    for(int j=0;j<nz;j++)for(int i=0;i<nr;i++){
        size_t k=(size_t)j*nr+i;double R=(i+.5)*dx,z=(j+.5-.5*nz)*dx,w=R;
        if(R*R+z*z<36){double exact=(4*(R*R+z*z)/(s2*s2)-6/s2)*q[0][k];err+=w*pow(lap[0][k]-exact,2);norm+=w*exact*exact;}
        sym+=w*(q[0][k]*lap[1][k]-q[1][k]*lap[0][k]);
    }
    printf("{\"benchmark_gaussian_relative_L2\":%.16g,\"weighted_self_adjoint_difference\":%.16g}\n",sqrt(err/norm),sym);
}
int main(int argc,char **argv){
    /* profile out nr nz dx dt T separation speed phase omega kind snapinterval */
    if(argc!=15&&argc!=16){fprintf(stderr,"expected14 arguments plus optional t0 snapshot\n");return 2;}
    load_profile(argv[1]);outdir=argv[2];nr=atoi(argv[3]);nz=atoi(argv[4]);dx=atof(argv[5]);dt=atof(argv[6]);
    double T=atof(argv[7]),sep=atof(argv[8]),speed=atof(argv[9]),phase=atof(argv[10]),om=atof(argv[11]);
    const char *kind=argv[12];double dsnap=atof(argv[13]);int benchmark=atoi(argv[14]);
    if(nr<8||nz<8||dx<=0||dt<=0||T<0||fabs(speed)>=1)return 2;
    lam=1.99+g*g/mx2;cells=(size_t)nr*nz;
    if(cells>2500000){fprintf(stderr,"grid exceeds declaredmemoryguard\n");return 2;}
    double *memory=calloc(cells*20,sizeof(double));if(!memory)return 3;
    for(int a=0;a<5;a++){q[a]=memory+a*cells;v[a]=memory+(a+5)*cells;acc[a]=memory+(a+10)*cells;lap[a]=memory+(a+15)*cells;}
    if(benchmark){gaussian_benchmark();return 0;}
    if(!strcmp(kind,"snapshot")){if(argc!=16)return 2;load_initial_state(argv[15]);}
    else if(!strcmp(kind,"pair")){add_fragment(-sep/2,speed,0,om);add_fragment(sep/2,-speed,phase,om);}
    else if(!strcmp(kind,"single_moving"))add_fragment(-sep/2,speed,0,om);
    else if(!strcmp(kind,"single_static"))add_fragment(0,0,0,om);
    else return 2;
    char name[1024];snprintf(name,sizeof name,"%s/log.jsonl",outdir);FILE *log=fopen(name,"w");if(!log)return 3;
    acceleration();diag initial=diagnose();long steps=lround(T/dt),diagstep=lround(1/dt),snapstep=lround(dsnap/dt);
    if(diagstep<1)diagstep=1;if(snapstep<1)snapstep=1;
    double maxEd=0,maxQd=0;clock_t started=clock();
    for(long step=0;step<=steps;step++){
        if(step%diagstep==0||step==steps){
            diag d=diagnose();double e=(d.E-initial.E)/fmax(1.,fabs(initial.E)),qq=(d.Q-initial.Q)/fmax(1.,fabs(initial.Q));
            maxEd=fmax(maxEd,fabs(e));maxQd=fmax(maxQd,fabs(qq));
            fprintf(log,"{\"t\":%.12g,\"E\":%.16g,\"Q\":%.16g,\"Pz\":%.16g,\"relative_E_change\":%.16g,\"relative_Q_change\":%.16g,\"Q10\":%.16g,\"Q15\":%.16g,\"Q20\":%.16g,\"Imax\":%.16g,\"z_peak\":%.16g,\"r_peak\":%.16g,\"Qz2\":%.16g,\"Qr2\":%.16g}\n",step*dt,d.E,d.Q,d.Pz,e,qq,d.Q10,d.Q15,d.Q20,d.Imax,d.zpeak,d.rpeak,d.Qz2,d.Qr2);
            if(fabs(d.Eface-d.E)>1e-9*fmax(1.,fabs(d.E))){fprintf(stderr,"positive face energy identity failed\n");return 5;}
            fflush(log);
            char ename[1024];snprintf(ename,sizeof ename,"%s/enclosed_energy.jsonl",outdir);
            FILE *elog=fopen(ename,step==0?"w":"a");if(!elog)return 3;
            fprintf(elog,"{\"t\":%.12g,\"E_face\":%.16g,\"E10\":%.16g,\"E15\":%.16g,\"E20\":%.16g,\"Eout20\":%.16g,\"relative_face_identity_error\":%.16g}\n",step*dt,d.Eface,d.E10,d.E15,d.E20,d.Eface-d.E20,(d.Eface-d.E)/fmax(1.,fabs(d.E)));
            fclose(elog);
            if(!isfinite(d.E)||!isfinite(d.Q)){fclose(log);return 4;}
        }
        if(step%snapstep==0||step==steps)snapshot(step*dt);
        if(step==steps)break;
        for(int a=0;a<5;a++)for(size_t k=0;k<cells;k++){v[a][k]+=.5*dt*acc[a][k];q[a][k]+=dt*v[a][k];}
        acceleration();
        for(int a=0;a<5;a++)for(size_t k=0;k<cells;k++)v[a][k]+=.5*dt*acc[a][k];
    }
    fclose(log);struct rusage ru;getrusage(RUSAGE_SELF,&ru);
    printf("{\"nr\":%d,\"nz\":%d,\"dx\":%.9g,\"dt\":%.9g,\"T\":%.9g,\"max_relative_E_change\":%.16g,\"max_relative_Q_change\":%.16g,\"initial_E\":%.16g,\"initial_Q\":%.16g,\"peak_rss_macos_bytes\":%ld,\"cpu_seconds\":%.6g}\n",nr,nz,dx,dt,T,maxEd,maxQd,initial.E,initial.Q,(long)ru.ru_maxrss,(double)(clock()-started)/CLOCKS_PER_SEC);
    return 0;
}
