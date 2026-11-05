import argparse,json,mpmath as mp
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
rows=[]
for bn,bd in [(1,3),(2,3),(9,10)]:
 for lam in [10,100]:
  vals=[]
  for prec in [40,80]:
   with mp.workdps(prec):
    beta=mp.mpf(bn)/bd;Ob=1/mp.cosh(1)**2
    H=lambda n:mp.sqrt(Ob*mp.exp(-3*n)+(1-Ob)*mp.exp(-3*(1-beta)*n))
    I=lambda N:mp.quad(lambda n:mp.exp(-2*n)/H(n),[0,N])
    J=lambda N:1-lam*I(N)
    assert J(0)>0>J(1)
    root=mp.findroot(J,(mp.mpf(0),mp.mpf('.2')));vals.append(root)
    if prec==80:
     N=root/2;j=J(N)
     def x(q):
      p=-lam*q*mp.exp(-q*q)
      return q+mp.quad(lambda n:p*mp.exp(-2*n)/(H(n)*mp.sqrt(1+p*p*mp.exp(-2*n))),[0,N])
     fd=[(x(h)-x(-h))/(2*h) for h in [mp.mpf('.00001'),mp.mpf('.000005')]]
     coarse=[(x(h)-x(-h))/(2*h) for h in [mp.mpf('.0001'),mp.mpf('.00005')]]
     order_ratio=abs(fd[0]-fd[1])/abs(coarse[0]-coarse[1])
     rows.append(dict(beta=float(beta),lambda_over_H0=lam,N_caustic=float(root),root_residual=float(abs(J(root))),precision_error=float(abs(vals[1]-vals[0])/(1+abs(vals[1]))),J_at_half=float(j),fd_coarse=float(fd[0]),fd_fine=float(fd[1]),fd_difference=float(abs(fd[0]-fd[1])),fd_fine_error=float(abs(fd[1]-j)),order_ratio=float(order_ratio),mutant_J_at_caustic=float(1+lam*I(root)),H_at_caustic=float(H(root))))
checks={'six_witnesses':len(rows)==6,'precision':all(r['precision_error']<1e-25 for r in rows),'roots':all(r['root_residual']<1e-25 and 0<r['N_caustic']<1 for r in rows),'positive_slope_control':all(abs(r['mutant_J_at_caustic']-2)<1e-12 for r in rows),'refined_fd':all(r['fd_difference']<1e-5 for r in rows),'second_order':all(.009<r['order_ratio']<.011 for r in rows)}
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(dict(checks=checks,rows=rows,scope='Exact admissible geodesic-clock branch loses smooth foliation; not every selected branch or all modified actions.'),indent=2));print(json.dumps(dict(checks=checks,rows=rows),indent=2));raise SystemExit(0 if all(checks.values()) else 1)
