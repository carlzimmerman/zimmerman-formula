"""Refine only W0 after the full finite stationary solve, then export."""
import sys,json
sys.dont_write_bytecode=True
from pathlib import Path
import mpmath as mp
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import highprecision_export as export
original=export.f.solve


def refined_solve(nodes):
    row=original(nodes);p=export.p;f=export.f
    tau=mp.mpf(row['tau_real']);z=[mp.mpf(row[k])/p.MU for k in ('T_GeV','N_GeV','Q_GeV')]
    oldw=mp.mpf(row['W0_GeV3'])/(p.WBASE*p.MU**3)
    def vacuum(w):return p.data(tau,z,w)['V']+f.loop(tau,z,w,nodes)-f.DE
    neww=mp.findroot(vacuum,oldw,solver='newton',tol=mp.mpf('1e-115'),maxsteps=8)
    row['W0_GeV3']=str(neww*p.WBASE*p.MU**3)
    row['net_V_GeV4']=str((p.data(tau,z,neww)['V']+f.loop(tau,z,neww,nodes))*p.MU**4)
    row['final_fractional_W0_refinement']=str(neww/oldw-1)
    return row


if __name__=='__main__':
    export.f.solve=refined_solve
    export.main(sys.argv[1])
