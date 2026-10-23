// Periodic 3-D classical-statistical field evolution. Natural conformal units.
// All four real fields and both original interactions retained. No number sink.
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <vector>
#include <stdexcept>
using Vec=std::vector<double>;
int main(int argc,char**argv){
 if(argc!=5) return 2;
 double start=std::stod(argv[4]);
 std::ifstream in(argv[1],std::ios::binary);
 double h[9]; in.read(reinterpret_cast<char*>(h),sizeof(h));
 int n=int(h[0]); double L=h[1],dt=h[2],end=h[3],b=h[4],mp=h[5],mx=h[6],c0=h[7],quartic=h[8];
 size_t S=size_t(n)*n*n; double dx=L/n,idx2=1/(dx*dx);
 Vec q(4*S),v(4*S),force(4*S);
 in.read(reinterpret_cast<char*>(q.data()),q.size()*8);
 in.read(reinterpret_cast<char*>(v.data()),v.size()*8);
 if(!in) throw std::runtime_error("invalid initial file");
 std::vector<size_t> neigh(6*S);
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)for(int k=0;k<n;k++){
  size_t p=(i*n+j)*n+k;
  neigh[6*p]=(((i+1)%n)*n+j)*n+k; neigh[6*p+1]=(((i+n-1)%n)*n+j)*n+k;
  neigh[6*p+2]=(i*n+(j+1)%n)*n+k; neigh[6*p+3]=(i*n+(j+n-1)%n)*n+k;
  neigh[6*p+4]=(i*n+j)*n+(k+1)%n; neigh[6*p+5]=(i*n+j)*n+(k+n-1)%n;
 }
 auto accel=[&](double z){
  double a=1+b*z,c=c0*a,mm=mp*mp*a*a,MM=mx*mx*a*a;
  for(size_t p=0;p<S;p++){
   double f=q[p],h=q[S+p],x=q[2*S+p],y=q[3*S+p],r=f*f+h*h;
   double grad[4]={mm*f+quartic*r*f+2*c*(x*f+y*h),mm*h+quartic*r*h+2*c*(-x*h+y*f),MM*x+c*(f*f-h*h),MM*y+2*c*f*h};
   for(size_t s=0;s<4;s++){
    size_t o=s*S; double lap=-6*q[o+p];
    for(int d=0;d<6;d++) lap+=q[o+neigh[6*p+d]];
    force[o+p]=idx2*lap-grad[s];
   }
  }
 };
 // Exact explicit-time work in the discretized conformal Hamiltonian.
 auto work_rate=[&](double z){
  double a=1+b*z,sum=0;
  for(size_t p=0;p<S;p++){
   double f=q[p],h=q[S+p],x=q[2*S+p],y=q[3*S+p];
   sum+=b*a*(mp*mp*(f*f+h*h)+mx*mx*(x*x+y*y))+b*c0*(x*(f*f-h*h)+2*y*f*h);
  } return sum/S;
 };
 std::ofstream out(argv[2]); out<<std::setprecision(17);
 out<<"z,a,Econf,work,charge,phi_variance,phi_mean_squared,phi_gradient,phi_kinetic_physical,phi_potential,X_mean_physical_squared,X_variance_physical\n";
 double work=0;
 auto record=[&](double z){
  double a=1+b*z,E=0,Q=0,phi2=0,gradphi=0,kinphi=0,potphi=0,x2=0;
  double means[4]={0,0,0,0};
  for(size_t p=0;p<S;p++){
   double f=q[p],h=q[S+p],x=q[2*S+p],y=q[3*S+p],r=f*f+h*h;
   double potential=.5*a*a*(mp*mp*r+mx*mx*(x*x+y*y))+.25*quartic*r*r+c0*a*(x*(f*f-h*h)+2*y*f*h);
   E+=potential;potphi+=.25*quartic*r*r+.5*a*a*mp*mp*r;
   phi2+=r;x2+=x*x+y*y;
   Q+=f*v[S+p]-h*v[p]+2*(x*v[3*S+p]-y*v[2*S+p]);
   for(size_t s=0;s<4;s++){
    size_t o=s*S; means[s]+=q[o+p]; E+=.5*v[o+p]*v[o+p];
    if(s<2)kinphi+=.5*std::pow(v[o+p]-b/a*q[o+p],2);
    for(int d=0;d<6;d+=2){
     double gr=.5*idx2*std::pow(q[o+neigh[6*p+d]]-q[o+p],2);
     E+=gr;if(s<2)gradphi+=gr;
    }
   }
  }
  for(double &x:means)x/=S;
  double meanphi=means[0]*means[0]+means[1]*means[1],meanx=means[2]*means[2]+means[3]*means[3];
  out<<z<<','<<a<<','<<E/S<<','<<work<<','<<Q/S<<','<<phi2/S-meanphi<<','<<meanphi<<','<<gradphi/S<<','<<kinphi/S<<','<<potphi/S<<','<<meanx/(a*a)<<','<<(x2/S-meanx)/(a*a)<<'\n';out.flush();
 };
 accel(start);record(start);
 int steps=int(std::llround(end/dt)),stride=std::max(1,int(std::llround(2/dt)));
 for(int t=0;t<steps;t++){
  double z=start+t*dt,w0=work_rate(z);
  for(size_t j=0;j<q.size();j++){v[j]+=.5*dt*force[j];q[j]+=dt*v[j];}
  accel(z+dt);
  for(size_t j=0;j<q.size();j++)v[j]+=.5*dt*force[j];
  work+=.5*dt*(w0+work_rate(z+dt));
  if((t+1)%stride==0||t+1==steps)record(z+dt);
 }
 std::ofstream final(argv[3],std::ios::binary);
 final.write(reinterpret_cast<char*>(q.data()),q.size()*8);
 final.write(reinterpret_cast<char*>(v.data()),v.size()*8);
 return final?0:3;
}
