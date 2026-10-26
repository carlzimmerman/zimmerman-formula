#include <cmath>
#include <vector>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string>
#include <stdexcept>
using namespace std;
int main(int argc,char**argv){
 if(argc!=10) return 2;
 string path=argv[1];double d=stod(argv[2]),amp=stod(argv[3]),width=stod(argv[4]),rad=stod(argv[5]),dx=stod(argv[6]),dt=stod(argv[7]),end=stod(argv[8]);bool mutate=stoi(argv[9]);
 const double pi=acos(-1.),qvac=2*asin(sqrt(1./6));double bg=d==0?qvac:0;int n=lround(rad/dx),steps=ceil(end/dt);dt=end/steps;
 vector<double> q(n),p(n),vol(n),r(n),damp(n),acc(n),cell(n);double lost=0,maxq=0,maxledger=0,maxcompact=0;
 for(int i=0;i<n;i++){double lo=i*dx,hi=lo+dx;r[i]=(lo+hi)/2;vol[i]=(pow(hi,3)-pow(lo,3))/3;q[i]=bg+(d==0?-amp:amp)*exp(-pow(r[i]/width,2));double t=max(0.,(r[i]-(rad-15))/15);damp[i]=2*t*t;}
 auto potential=[&](double a){double s=pow(sin(a/2),2),z=s/(sqrt(1-s)*(1+sqrt(1-s)));if(d==0)return 10*pow((z+1)*(z+1)-1.2,2);return (d-8)*z+36*z*z+40*pow(z,3)+10*pow(z,4);};
 auto acceleration=[&](){for(int i=0;i<n;i++){double right=(i==n-1?2*(bg-q[i]):q[i+1]-q[i])/dx;double left=(i==0?0:(q[i]-q[i-1])/dx);double x=1/cos(q[i]/2);double force=(40*x*x*x-48*x+d)*.5*x*tan(q[i]/2);acc[i]=(pow((i+1)*dx,2)*right-pow(i*dx,2)*left)/vol[i]-force;}};
 auto damping=[&](){for(int i=0;i<n;i++){double old=p[i];p[i]*=exp(-damp[i]*dt/2);lost+=(mutate?-1:1)*4*pi*.5*vol[i]*(old*old-p[i]*p[i]);}};
 auto energy=[&](){for(int i=0;i<n;i++)cell[i]=vol[i]*(.5*p[i]*p[i]+potential(q[i]));for(int i=0;i<n-1;i++){double eg=.5*pow((i+1)*dx,2)*pow(q[i+1]-q[i],2)/dx;cell[i]+=.5*eg;cell[i+1]+=.5*eg;}cell[n-1]+=rad*rad*pow(bg-q[n-1],2)/dx;double total=0,core=0,prefix=0,metric=0;for(int i=0;i<n;i++){total+=cell[i];if(r[i]<10)core+=cell[i];prefix+=cell[i];metric=max(metric,prefix/((i+1)*dx));}maxcompact=max(maxcompact,metric);return pair<double,double>(4*pi*total,4*pi*core);};
 auto initial=energy();ofstream log(path+"_series.csv");log<<setprecision(17)<<"time,total_energy,core_energy,absorbed,ledger_relative,q_center\n";vector<double> late;int stride=max(1,int(1/dt));
 for(int step=0;step<=steps;step++){
  if(step%stride==0 || step==steps){auto en=energy();double err=abs(en.first+lost-initial.first)/initial.first;maxledger=max(maxledger,err);log<<step*dt<<","<<en.first<<","<<en.second<<","<<lost<<","<<err<<","<<q[0]<<"\n";if(step*dt>=end*.75)late.push_back(en.second);}
  if(step==steps)break;
  damping();acceleration();for(int i=0;i<n;i++){p[i]+=.5*dt*acc[i];q[i]+=dt*p[i];maxq=max(maxq,abs(q[i]));if(!isfinite(q[i])||abs(q[i])>=pi-.01)throw runtime_error("physical branch / resolution failure");}acceleration();for(int i=0;i<n;i++)p[i]+=.5*dt*acc[i];damping();
 }
 auto final=energy();double mean=0;for(double a:late)mean+=a;mean/=late.size();ofstream result(path+".json");result<<setprecision(17)<<"{\"initial_energy\":"<<initial.first<<",\"final_energy\":"<<final.first<<",\"final_core_energy\":"<<final.second<<",\"late_core_mean\":"<<mean<<",\"retained_fraction\":"<<mean/initial.first<<",\"absorbed\":"<<lost<<",\"max_ledger_relative\":"<<maxledger<<",\"max_abs_q\":"<<maxq<<",\"max_integrated_energy_over_radius\":"<<maxcompact<<"}\n";
 ofstream state(path+"_state.csv");state<<setprecision(17)<<"r,q,p\n";for(int i=0;i<n;i++)state<<r[i]<<","<<q[i]<<","<<p[i]<<"\n";
 if(maxledger>.005){cerr<<"Energy ledger failed "<<maxledger<<"\n";return 1;}return 0;
}
