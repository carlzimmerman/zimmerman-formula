"""argon_clues: what the pasted 'single action' derives and what it inserts."""
import sympy as s
u,a0,K,g,gN,chi = s.symbols('u a0 K g g_N chi', positive=True)
# 1. W_rem'(u) and the law
Wfull = a0**2/K*(-s.log(1-u/a0)-u/a0)
Wrem = Wfull - u**2/(2*K)
print('1. K*W_rem\'(u) - u^2/(a0-u) =', s.simplify(K*s.diff(Wrem,u) - u**2/(a0-u)), ' (W_rem is CHOSEN so that this holds)')
sol = s.solve(s.Eq(gN*(a0-(g-gN)), (g-gN)**2), gN)
print('2. static EL with u=g-g_N, g_N = u^2/(a0-u):', [s.simplify(x) for x in sol], '-> law g_N = g^2/(g+a0) (given W_rem)')
# 3. chi_tether in (B) only is not an EL equation of L; chi in the action changes Gauss
x=s.symbols('x'); Phi=s.Function('Phi')(x); P=s.Function('P')(x); chif=s.Function('chi')(x); rho=s.Function('rho')(x)
L = -chif*(Phi.diff(x)-K*P)**2/(2*K) - rho*Phi
EL_Phi = s.simplify(s.diff(L,Phi) - s.diff(s.diff(L,Phi.diff(x)),x))
print('3. EL_Phi with chi inside the action:', EL_Phi, ' -> Gauss law becomes (chi (Phi\'-KP))\' = K rho: where chi=0 the hot gas would not source gravity')
print('   chi only in the P-equation (as pasted) has no Lagrangian: no L gives (A) unweighted AND (B) weighted.')
print('4. A_slip, L_kin(f_c,...) and the conversion law (C) (P_hot -> rho_free) are not given as functions; a decoherence/irreversible transfer is not an EL equation of a conservative action (it needs a defined dissipative channel or an environment).')
print('5. Conservation (C): int(-div P)dV = -(surface flux of P at the basin edge); with P->0 at the edge the polarisation charge integrates to 0 and (C) would give M_free = R0 M_b for ANY gas state. M_free = R0 M_hot needs the edge flux to carry exactly R0 M_cond: a boundary condition, not a result.')
