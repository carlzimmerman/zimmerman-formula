"""Independent closed-form, exact-rational audit of the tree recursion."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

p=Path(__file__).parent
data=json.loads((p/'neutral_four_to_two_v2_run/results.json').read_text())
m=F('0.001'); g=F('0.000002168'); lam=F('0.00881292')
M2=4*m*m*(1+F('0.02')**2)
Delta=M2-4*m*m
Kt=4*(lam-g*g/Delta)
Kc=4*(lam-g*g/(M2+2*m*m))
Kh=4*(lam+g*g/(16*m*m-M2))
# Nine unordered splits of the six external legs, each containing two
# external positive legs and one negative leg on its selected side.
A31=Kt*(3*Kh/F(8)-6*Kc/F(4))/(m*m)
A22=(Kt*Kc/F(2)-Kt*Kt/F(4)-Kc*Kc)/(m*m)
negative_square=-((Kt-Kc)**2+3*Kc**2)/(4*m*m)
checks=dict(exact_negative_square=A22==negative_square,
    positive_kernels=Kt>0 and Kc>0,
    recursion_31=abs(float(A31)/data['channels']['31']['amplitude_GeV_minus2']-1)<1e-10,
    recursion_22=abs(float(A22)/data['channels']['22']['amplitude_GeV_minus2']-1)<1e-10)
out=dict(checks=checks,all_pass=all(checks.values()),
    exact_amplitudes={'31':str(A31),'22':str(A22)},
    numeric_amplitudes={'31':float(A31),'22':float(A22)},
    kernels={'threshold':float(Kt),'crossed':float(Kc),'hard':float(Kh)},
    statement='At zero incoming momentum, the balanced-channel amplitude is -[(Kt-Kc)^2+3 Kc^2]/(4m^2). The existing positive lambda_rep benchmark cannot cancel it. This is a tree-level vacuum statement, not a finite-density destruction theorem.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
sys.exit(0 if out['all_pass'] else 1)
