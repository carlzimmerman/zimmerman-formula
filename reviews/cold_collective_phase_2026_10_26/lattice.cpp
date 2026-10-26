#include <cmath>
#include <vector>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <stdexcept>
using namespace std;
int main(int argc,char**argv){
 if(argc!=9)return 2;string path=argv[1];double d=stod(argv[2]),A=stod(argv[3]),k=stod(argv[4]);int n=stoi(argv[5]);double dt=stod(argv[6]),end=stod(argv[7]),epsilon=stod(argv[8]);
 double pi=acos(-1.),m2=(d-8)/4,L=2*pi/k,dx=L/n;int count=n*n*n,steps=ceil(end/dt);dt=end/steps;
 vector<double>q(count),p(count),acc(count);vector<int>xp(count),xm(count),yp(count),ym(count),zp(count),zm(count);
 auto index=[&](int i,int j,int h){return ((i+n)%n*n+(j+n)%n)*n+(h+n)%n;};
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)for(int h=0;h<n;h++){int a=index(i,j,h);xp[a]=index(i+1,j,h);xm[a]=index(i-1,j,h);yp[a]=index(i,j+1,h);ym[a]=index(i,j-1,h);zp[a]=index(i,j,h+1);zm[a]=index(i,j,h-1);q[a]=A*(1+epsilon*(cos(2*pi*i/n)+cos(2*pi*j/n)+cos(2*pi*h/n))/3);}
 auto U=[&](double v){double c=cos(v/2),z=pow(sin(v/2),2)/(c*(1+c));return (d-8)*z+36*z*z+40*z*z*z+10*z*z*z*z;};
 auto force=[&](double v){double x=1/cos(v/2);return (40*x*x*x-48*x+d)*.5*x*tan(v/2);};
 auto acceleration=[&](){for(int i=0;i<count;i++)acc[i]=(q[xp[i]]+q[xm[i]]+q[yp[i]]+q[ym[i]]+q[zp[i]]+q[zm[i]]-6*q[i])/(dx*dx)-force(q[i])/m2;};
 // Diagnostic: E, P, virial pressure, <q q_s>, contrast, gradient fraction.
 auto diagnose=[&](){vector<double>v(6);double E2=0;for(int i=0;i<count;i++){double grad=m2*(pow(q[xp[i]]-q[i],2)+pow(q[yp[i]]-q[i],2)+pow(q[zp[i]]-q[i],2))/(dx*dx),K=.5*m2*p[i]*p[i],pot=U(q[i]),E=K+.5*grad+pot;v[0]+=E;E2+=E*E;v[1]+=K-grad/6-pot;v[2]+=grad/3+.5*q[i]*force(q[i])-pot;v[3]+=q[i]*p[i];v[5]+=.5*grad;}
 for(auto &x:v)x/=count;v[4]=sqrt(max(0.,E2/count-v[0]*v[0]))/v[0];v[5]/=v[0];return v;};
 auto init=diagnose();double drift=0,maxCV=init[4],maxGrad=0,avgE=0,avgP=0,avgV=0,startQP=0,endQP=0;int samples=0;ofstream log(path+".csv");log<<setprecision(17)<<"time,energy,pressure,virial_pressure,qp,contrast,gradient_fraction\n";int stride=max(1,int(.02/dt));
 for(int step=0;step<=steps;step++){
  if(step%stride==0||step==steps){auto v=diagnose();drift=max(drift,abs(v[0]/init[0]-1));maxCV=max(maxCV,v[4]);maxGrad=max(maxGrad,v[5]);log<<step*dt;for(auto x:v)log<<","<<x;log<<"\n";}
  if(step==steps)break;
  acceleration();for(int i=0;i<count;i++){p[i]+=.5*dt*acc[i];q[i]+=dt*p[i];if(!isfinite(q[i])||abs(q[i])>=pi-.01)throw runtime_error("branch failure");}acceleration();for(int i=0;i<count;i++)p[i]+=.5*dt*acc[i];
 }
 auto final=diagnose();ofstream out(path+".json");out<<setprecision(17)<<"{\"initial_energy\":"<<init[0]<<",\"final_energy\":"<<final[0]<<",\"max_energy_drift\":"<<drift<<",\"max_contrast\":"<<maxCV<<",\"final_contrast\":"<<final[4]<<",\"max_gradient_fraction\":"<<maxGrad<<"}\n";if(drift>.005)return 1;return 0;
}
