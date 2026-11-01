import json,sys,resource
from pathlib import Path
import sympy as S
import mpmath as mp
root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from pressure_scan import cw
mp.mp.dps=60
h,l,g,f,X,k=S.symbols('h l g f X k',positive=True)
D=l*l+30*h*h;gx=12*h*h*k;ga=(h*h+S.Rational(21,10)*l*l-10*g*g)*k;gb=(S.Rational(21,20)*l*l-10*g*g)*k
betas={h:h*(gx+2*ga),l:l*(gb+2*ga),g:-5*k*g**3,f:f*gx,X:-gx*X}
def flow(expr):return S.simplify(sum(S.diff(expr,v)*b for v,b in betas.items()))
U0=f*f*l*l/D;C1=6*f*f*h*h*l*l*(29*l*l-200*g*g)/D**2*(k/2)
ge=(l*l*gx+30*h*h*gb)/D
checks={'one_loop_CS':S.simplify(flow(U0)-C1)==0,
        'T_transport':S.simplify(flow(S.sqrt(D)*X/l)/(S.sqrt(D)*X/l)+ge)==0,
        'feff_transport':S.simplify(flow(f*l/S.sqrt(D))/(f*l/S.sqrt(D))-ge)==0,
        'feffT_invariant':S.simplify(flow(f*X))==0,
        'b_transport':S.simplify(flow(h*X/l)/(h*X/l)+gb)==0,
        'a_transport_mismatch':S.simplify(flow(S.sqrt(2*f*h/D))/S.sqrt(2*f*h/D)+ga-l*l*(gx-gb)/D)==0}
H=L=mp.mpf('.03');G=mp.sqrt(mp.mpf(29)/200)*L*mp.mpf('.91');xx=mp.mpf(10)
s4=6*H*H*L*L*(29*L*L-200*G*G)/(30*H*H+L*L)**2
def uq(t):return cw(xx,H,L,G)-2*t*s4/(64*mp.pi**2)
qdiff=mp.diff(uq,0);expected=-s4/(32*mp.pi**2)
checks['full_threshold_Q_derivative']=abs(qdiff-expected)<mp.mpf('1e-50')
out={'claim_id':'TP02_CS1','checks':checks,'symbolic_CS_coefficient':str(S.factor(flow(U0))),
     'gamma_eff':str(S.factor(ge)),'Q_derivative':str(qdiff),'Q_derivative_expected':str(expected),
     'a_mismatch':str(S.factor(l*l*(gx-gb)/D)),'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
     'scope':'One-loop reduced CS plus characteristic field identities only; heavy normal relaxation and finite two-loop matching not computed.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
