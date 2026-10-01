/* B3 CK7: 4D Z_N gauge theory (N=2,3), action beta*sum cos(theta), Metropolis. Prints <cos theta> per plaquette. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
static uint64_t s[2];
static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static uint64_t nxt(void){uint64_t s0=s[0],s1=s[1],r=s0+s1;s1^=s0;s[0]=rotl(s0,55)^s1^(s1<<14);s[1]=rotl(s1,36);return r;}
static double ur(void){return (nxt()>>11)*(1.0/9007199254740992.0);}
int L,N;
static int *U; /* U[site*4+mu] in 0..N-1 */
#define SITE(x,y,z,t) ((((t)*L+(z))*L+(y))*L+(x))
static int nb(int site,int mu,int d){int c[4];int r=site;c[0]=r%L;r/=L;c[1]=r%L;r/=L;c[2]=r%L;r/=L;c[3]=r;c[mu]=(c[mu]+d+L)%L;return SITE(c[0],c[1],c[2],c[3]);}
static double cosk[8];
static inline int md(int a){a%=N;if(a<0)a+=N;return a;}
/* staple sum contribution: for link (site,mu), for each nu!=mu, the plaquette angle = U_mu(x)+U_nu(x+mu)-U_mu(x+nu)-U_nu(x) ; the link enters with +; return list of 'rest' angles */
static void rest(int site,int mu,int *r,int *n){int k=0;for(int nu=0;nu<4;nu++){if(nu==mu)continue;
 int xm=nb(site,mu,1),xn=nb(site,nu,1);
 r[k++]=md(U[xm*4+nu]-U[xn*4+mu]-U[site*4+nu]);
 int xmm=nb(site,nu,-1),xmmm=nb(xm,nu,-1);
 /* backward plaquette: U_mu(x)-U_nu(x+mu-nu)... plaquette angle = U_mu(x) - U_nu(x+mu-nu) - U_mu(x-nu) + U_nu(x-nu) */
 r[k++]=md(-U[xmmm*4+nu]-U[xmm*4+mu]+U[xmm*4+nu]);}
 *n=k;}
int main(int argc,char**argv){
 N=atoi(argv[1]);L=atoi(argv[2]);double beta=atof(argv[3]);int hot=atoi(argv[4]);int therm=atoi(argv[5]),meas=atoi(argv[6]);s[0]=0x9E3779B97F4A7C15ULL^(uint64_t)(N*1000+hot);s[1]=0xD1B54A32D192ED03ULL^(uint64_t)L;for(int i=0;i<20;i++)nxt();
 for(int k=0;k<N;k++)cosk[k]=cos(2*M_PI*k/N);
 int V=L*L*L*L;U=malloc(sizeof(int)*V*4);for(int i=0;i<V*4;i++)U[i]=hot?(int)(ur()*N):0;
 double sum=0,sum2=0;int cnt=0;
 for(int sw=0;sw<therm+meas;sw++){
  for(int site=0;site<V;site++)for(int mu=0;mu<4;mu++){int r[6],n;rest(site,mu,r,&n);int old=U[site*4+mu];int nw=(old+1+(int)(ur()*(N-1)))%N;
   double eo=0,en=0;for(int i=0;i<n;i++){eo+=cosk[md(old+r[i])];en+=cosk[md(nw+r[i])];}
   double dS=beta*(en-eo);if(dS>=0||ur()<exp(dS))U[site*4+mu]=nw;}
  if(sw>=therm){double p=0;for(int site=0;site<V;site++)for(int mu=0;mu<4;mu++)for(int nu=mu+1;nu<4;nu++){int xm=nb(site,mu,1),xn=nb(site,nu,1);p+=cosk[md(U[site*4+mu]+U[xm*4+nu]-U[xn*4+mu]-U[site*4+nu])];}
   p/=(6.0*V);sum+=p;sum2+=p*p;cnt++;}
 }
 double m=sum/cnt;printf("N=%d L=%d beta=%.4f start=%s <cos>=%.5f sd=%.5f\n",N,L,beta,hot?"hot":"cold",m,sqrt(sum2/cnt-m*m));return 0;}
