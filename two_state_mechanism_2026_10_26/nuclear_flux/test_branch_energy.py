import numpy as np
from branch_energy import event_sources,line_event

def main():
 # State: x,c,a1,a2s,a2p,t,K,gamma; one molecular level with D=.08.
 D=.08;omega=.375;energy=np.array([0,0,-.5,-.125,-.125,-.5-D,1,omega])
 charges=np.array([1,-1,0,0,0,1,0,0]);X=np.array([1,0,1,1,1,2,0,0]);C=np.array([0,1,1,1,1,1,0,0])
 for dr in ([1,0,0],[0,1,0],[0,0,1],[.1,-.4,.7]):
  for line in [-.3,0,.8]:
   dy=event_sources(D,dr,line)
   for inv in [energy,charges,X,C]:assert abs(inv@dy)<1e-14
 excited=event_sources(D,[0,0,1],0);assert abs(excited[6]-(.125-D))<1e-14
 cycle=excited+event_sources(D,[0,0,0],1);assert cycle[4]==0 and cycle[7]==1
 assert abs(cycle[6]+omega-(.5-D))<1e-14
 for T in [.02,.1,1.]:
  n=1/np.expm1(.375/T);ap=3*np.exp(-.375/T)
  assert abs(line_event(.2,1,ap,n))<1e-14
 print('Ground/excited DR events and emission/reabsorption conserve both constituents, charge and total energy. No DR rates supplied.')
if __name__=='__main__':main()
