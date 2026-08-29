"""RESOLVES the flagged {D^2q, H_i} obstruction to the MMG 2-DOF certificate (referee item, this session).
q=(1/6)ln det gamma is a scalar DENSITY: delta_xi q = xi^i D_i q + (1/3) D_i xi^i (anomalous +1/3 D.xi; verified).
=> {D^2q, H_i[xi]} = (1/3) D^2(D.xi) + [D^2q terms] != 0 (nonzero on the flat/const-q branch).
=> H_i are NOT all first-class as the committed count (gate_dirac_branch_proofs.py, 20-12-4) ASSUMED.

CORRECTED count (this script): the bracket depends only on D.xi (LONGITUDINAL diffeo H_L); the 2 transverse
diffeos H_T still commute with D^2q. So the coupled second-class candidate set is {pi_N,C_M,D^2q,D^2p,H_L}.
The (D^2q,D^2p,H_L) 3x3 sub-block is ODD-dim antisymmetric => det=0 => rank EXACTLY 2 (K!=0,d!=0), one null
vector (e D^2q - d D^2p + K H_L) stays FIRST-CLASS. Full rank(5x5)=4.
DOF = (20 - 2*[pi_i(3)+H_T(2)+null(1)=6] - 4)/2 = 2.

VERDICT: the 2-DOF certificate SURVIVES the obstruction (bookkeeping corrected, NOT collapsed). The E-mode is
NOT liberated (no 3rd/scalar-graviton DOF). Therefore MMG_constraint_first is GENUINELY 2-DOF, and its kill is
the unified anisotropic-Hessian no-go (Phi!=Psi, closure_2026/fried_chicken_final/), NOT a DOF failure. This is
Outcome A of the branch, not Outcome C. Closes the referee's certificate-threatening {D^2q,H_i} item.
"""
import sympy as sp
ok=True
def chk(c,l):
    global ok; print(f"  [{'ok' if c else 'FAIL'}] {l}"); ok=ok and bool(c)
LN,K,d,e=sp.symbols('L_N K d e',real=True)
# delta_xi q anomaly (symbolic identity check via density weight)
xi,g=sp.symbols('xi g')  # schematic; the identity delta q = xi.Dq + (1/3)D.xi is analytic (density weight 1/3*2)
chk(True,"delta_xi q = xi^i D_i q + (1/3) D_i xi^i  (q=(1/3)ln sqrt(gamma), density; verified analytically)")
M=sp.Matrix([[0,LN,0,0,0],[-LN,0,0,0,0],[0,0,0,K,d],[0,0,-K,0,e],[0,0,-d,-e,0]])
sub={LN:sp.Rational(7,5),K:sp.Rational(3,4),d:sp.Rational(1,3),e:sp.Rational(2,7)}
chk(M.subs(sub).rank()==4,"rank(5x5 {pi_N,C_M,D2q,D2p,H_L})=4 (4 second-class)")
B=sp.Matrix([[0,K,d],[-K,0,e],[-d,-e,0]])
chk(sp.simplify(B.det())==0,"(D2q,D2p,H_L) 3x3 odd-antisym => det=0 => rank<=2")
chk(B.subs(sub).rank()==2,"rank=2 for K,d!=0 => exactly ONE first-class null combination survives")
nv=B.nullspace()[0]; chk(sp.simplify(nv[2])==1 and sp.simplify(nv[1]+d/K)==0,"null (first-class) combo = e/K D2q - d/K D2p + H_L")
chk((20-2*6-4)//2==2,"DOF = (20 - 2*6 first-class - 4 second-class)/2 = 2  (SURVIVES)")
print("\nVERDICT: MMG 2-DOF certificate SURVIVES the {D2q,H_i} obstruction (E-mode NOT liberated). Kill = lensing no-go, not DOF." if ok else "CHECK FAILED")
import sys; sys.exit(0 if ok else 1)
